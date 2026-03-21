import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.connection import get_db
from app.models.media import Media
from app.models.admin_user import AdminUser
from app.schemas.media import MediaResponse
from app.config import settings
from app.api.deps import get_current_admin

router = APIRouter(prefix="/admin/media", tags=["媒体管理"])

ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml",
    "video/mp4", "video/webm",
    "application/pdf",
}


def get_media_type(mime_type: str) -> str:
    if mime_type.startswith("image/"):
        return "image"
    if mime_type.startswith("video/"):
        return "video"
    return "attachment"


@router.post("/upload", response_model=MediaResponse, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    lesson_id: int | None = None,
    alt_text: str | None = None,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型: {file.content_type}")

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制")

    ext = os.path.splitext(file.filename or "file")[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, unique_name)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(content)

    media = Media(
        filename=file.filename or "unknown",
        filepath=unique_name,
        media_type=get_media_type(file.content_type or ""),
        mime_type=file.content_type or "application/octet-stream",
        file_size=len(content),
        lesson_id=lesson_id,
        alt_text=alt_text,
    )
    db.add(media)
    await db.commit()
    await db.refresh(media)

    response = MediaResponse.model_validate(media)
    response.url = f"/uploads/{unique_name}"
    return response


@router.get("", response_model=list[MediaResponse])
async def list_media(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Media).order_by(Media.created_at.desc()))
    media_list = result.scalars().all()
    responses = []
    for m in media_list:
        resp = MediaResponse.model_validate(m)
        resp.url = f"/uploads/{m.filepath}"
        responses.append(resp)
    return responses


@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if not media:
        raise HTTPException(status_code=404, detail="文件不存在")
    filepath = os.path.join(settings.UPLOAD_DIR, media.filepath)
    if os.path.exists(filepath):
        os.remove(filepath)
    await db.delete(media)
    await db.commit()
    return {"message": "删除成功"}
