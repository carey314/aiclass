"""
即梦AI视频脚本生成器 API

提供5个endpoint：
- POST   /transcribe          音频→文字
- POST   /generate            主题→脚本（SSE流式）
- GET    /history             历史列表（分页）
- GET    /{id}                历史详情
- DELETE /{id}                删除（仅owner）

设计要点：
1. 白名单校验：只有 VIDEO_SCRIPT_ALLOWED_USERS 中的用户能用
2. 用户隔离：每条script属于user_id，不能访问别人的
3. SSE流式：generate返回流式token，前端累积+解析JSON
4. 健壮：超时/限流/认证错误都返回友好的错误码

数据流（generate）：
    用户输入主题 → check白名单 → build prompts → 流式请求豆包
    → 边收token边推给前端（SSE） → 收完后解析JSON → 写入DB
"""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_admin
from app.config import settings
from app.database.connection import get_db
from app.models.admin_user import AdminUser
from app.models.video_script import VideoScript
from app.schemas.video_script import (
    GenerateRequest,
    ScriptTemplate,
    TranscribeResponse,
    VideoScriptResponse,
    VideoScriptListResponse,
    VideoScriptListItem,
)
from app.services.doubao_client import DoubaoError, get_doubao_client
from app.services.prompt_builder import (
    build_system_prompt,
    build_user_prompt,
    strip_markdown_codeblock,
    QUICK_TOPICS,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/video_script", tags=["视频脚本生成器"])


# ============================================================
# GET /quick_topics — 快捷主题列表（首页展示，无需鉴权）
# ============================================================
@router.get("/quick_topics")
async def quick_topics():
    """
    返回鞠姐讲健康常用的快捷主题（祛湿/补气血/失眠等）。
    前端在主页面展示成按钮，点击直接填入主题输入框。
    无需认证，所有人都能看到。
    """
    return {"topics": QUICK_TOPICS}


# ============================================================
# 白名单校验：放在每个endpoint开头
# ============================================================
def check_allowed(user: AdminUser) -> None:
    """
    检查用户是否在 VIDEO_SCRIPT_ALLOWED_USERS 白名单内。
    不在则 403。

    白名单为空字符串 = 不限制（开发模式）
    """
    allowed = settings.video_script_allowed_users_list
    if not allowed:
        return  # 不限制
    if user.username not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此功能仅对部分用户开放，敬请期待",
        )


# ============================================================
# POST /transcribe — 音频→文字
# ============================================================
@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(
    audio: UploadFile = File(..., description="录音文件 (webm/mp3/wav)"),
    current_user: AdminUser = Depends(get_current_admin),
):
    """
    将上传的音频转为文字。

    前端使用 MediaRecorder API 录制 webm，POST multipart 上传。
    后端调用豆包ASR返回识别结果。
    """
    check_allowed(current_user)

    # 大小校验
    audio_bytes = await audio.read()
    max_bytes = settings.MAX_AUDIO_SIZE_MB * 1024 * 1024
    if len(audio_bytes) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"音频文件过大（>{settings.MAX_AUDIO_SIZE_MB}MB）",
        )
    if len(audio_bytes) < 100:  # 极小文件视为空录音
        return TranscribeResponse(text="", duration_ms=0)

    # 解析格式
    audio_format = "webm"
    if audio.filename:
        suffix = audio.filename.lower().rsplit(".", 1)
        if len(suffix) == 2:
            audio_format = suffix[1]
    elif audio.content_type:
        # audio/webm → webm
        if "/" in audio.content_type:
            audio_format = audio.content_type.split("/", 1)[1].split(";")[0]

    start = time.time()
    try:
        client = get_doubao_client()
        text = await client.transcribe(audio_bytes, audio_format=audio_format)
    except DoubaoError as e:
        logger.error("ASR调用失败: %s", e)
        # 友好降级：识别失败返回空字符串，前端提示用户重新录或手动输入
        if e.kind == "auth":
            raise HTTPException(status_code=500, detail="服务器ASR配置异常，请联系管理员")
        # 其他错误返回空字符串，前端可降级到文字输入
        return TranscribeResponse(text="", duration_ms=int((time.time() - start) * 1000))

    return TranscribeResponse(text=text, duration_ms=int((time.time() - start) * 1000))


# ============================================================
# POST /generate — 主题→脚本（SSE流式）
# ============================================================
async def _stream_and_persist(
    request: GenerateRequest,
    current_user: AdminUser,
    db: AsyncSession,
) -> AsyncIterator[bytes]:
    """
    内部生成器：
    1. 流式从豆包接收token
    2. 同时通过SSE推给前端
    3. 累积所有token，解析JSON，写入DB
    4. 最后发一个 'done' 事件，data是 {id, generation_ms}

    SSE格式：
        event: token
        data: {"chunk": "..."}

        event: done
        data: {"id": 123, "generation_ms": 28000}

        event: error
        data: {"detail": "...", "kind": "..."}
    """
    system_prompt = build_system_prompt(persona="jujie")
    user_prompt = build_user_prompt(request.topic, request.reference_hints)
    accumulated = []
    start = time.time()

    try:
        client = get_doubao_client()
        async for chunk in client.stream_generate(system_prompt, user_prompt):
            accumulated.append(chunk)
            payload = json.dumps({"chunk": chunk}, ensure_ascii=False)
            yield f"event: token\ndata: {payload}\n\n".encode("utf-8")

    except DoubaoError as e:
        logger.error("流式生成失败: %s (kind=%s)", e, e.kind)
        err_data = json.dumps(
            {"detail": str(e), "kind": e.kind}, ensure_ascii=False
        )
        yield f"event: error\ndata: {err_data}\n\n".encode("utf-8")
        return

    # 全部接收完成 → 解析JSON
    full_text = strip_markdown_codeblock("".join(accumulated))
    generation_ms = int((time.time() - start) * 1000)

    try:
        template_dict = json.loads(full_text)
        # Pydantic校验
        template = ScriptTemplate(**template_dict)
    except Exception as e:
        logger.error("JSON解析失败: %s, text=%s", e, full_text[:500])
        err_data = json.dumps(
            {"detail": "AI输出格式异常，请重试", "kind": "bad_json"},
            ensure_ascii=False,
        )
        yield f"event: error\ndata: {err_data}\n\n".encode("utf-8")
        return

    # 写入DB
    record = VideoScript(
        user_id=current_user.id,
        topic=request.topic,
        template_json=template.model_dump_json(),
        model_used=settings.ARK_TEXT_MODEL,
        generation_ms=generation_ms,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    done_data = json.dumps(
        {"id": record.id, "generation_ms": generation_ms}, ensure_ascii=False
    )
    yield f"event: done\ndata: {done_data}\n\n".encode("utf-8")


@router.post("/generate")
async def generate_script(
    request: GenerateRequest,
    current_user: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    流式生成视频脚本。

    返回 Server-Sent Events 流，事件类型：
    - token: 收到一段豆包返回的文字
    - done: 完成，包含 record id 和耗时
    - error: 出错，包含 detail 和 kind
    """
    check_allowed(current_user)

    return StreamingResponse(
        _stream_and_persist(request, current_user, db),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # nginx 不缓冲SSE
            "Connection": "keep-alive",
        },
    )


# ============================================================
# GET /history — 历史列表
# ============================================================
@router.get("/history", response_model=VideoScriptListResponse)
async def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """拉取自己的历史脚本（按时间倒序，分页）"""
    check_allowed(current_user)

    offset = (page - 1) * page_size

    # 总数
    count_result = await db.execute(
        select(func.count(VideoScript.id)).where(VideoScript.user_id == current_user.id)
    )
    total = count_result.scalar_one()

    # 列表
    stmt = (
        select(VideoScript)
        .where(VideoScript.user_id == current_user.id)
        .order_by(VideoScript.created_at.desc())
        .limit(page_size)
        .offset(offset)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()

    return VideoScriptListResponse(
        items=[VideoScriptListItem.model_validate(r) for r in records],
        total=total,
        page=page,
        page_size=page_size,
    )


# ============================================================
# GET /{script_id} — 历史详情
# ============================================================
@router.get("/{script_id}", response_model=VideoScriptResponse)
async def get_script(
    script_id: int,
    current_user: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    获取指定脚本详情。

    安全：用户只能看自己的脚本。如果script_id属于别的用户，返回404
    （不返回403，避免泄露"该id存在"的信息）。
    """
    check_allowed(current_user)

    result = await db.execute(
        select(VideoScript).where(
            VideoScript.id == script_id,
            VideoScript.user_id == current_user.id,
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="脚本不存在")

    template = ScriptTemplate.model_validate_json(record.template_json)
    return VideoScriptResponse(
        id=record.id,
        topic=record.topic,
        template=template,
        model_used=record.model_used,
        generation_ms=record.generation_ms,
        created_at=record.created_at,
    )


# ============================================================
# DELETE /{script_id} — 删除
# ============================================================
@router.delete("/{script_id}", status_code=204)
async def delete_script(
    script_id: int,
    current_user: AdminUser = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    删除指定脚本。

    安全：用户只能删自己的。其他人的id返回404（一致性）。
    """
    check_allowed(current_user)

    result = await db.execute(
        select(VideoScript).where(
            VideoScript.id == script_id,
            VideoScript.user_id == current_user.id,
        )
    )
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="脚本不存在")

    await db.execute(delete(VideoScript).where(VideoScript.id == script_id))
    await db.commit()
    return None
