"""
VideoScript Pydantic schemas — 输入/输出数据结构

设计要点:
- 输入: 主题字符串(必填)
- 输出: 严格JSON结构，与豆包返回的JSON保持一致
- 历史: 列表/详情/删除的响应

为什么严格schema?
LLM输出有时会少字段，Pydantic会捕获并触发重试，避免脏数据持久化。
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ============================================================
# 即梦提示词 6段结构
# ============================================================
class JimengPrompt(BaseModel):
    subject: str = Field(..., description="人物：50+岁女性外貌+服装")
    scene: str = Field(..., description="场景：环境+时间+氛围")
    motion: str = Field(..., description="运动：人物动作+食材操作")
    camera: str = Field(..., description="镜头：景别+运镜")
    mood: str = Field(..., description="氛围：色调+光影")
    style: str = Field(..., description="风格关键词")


# ============================================================
# 完整的视频脚本模板
# ============================================================
class ScriptTemplate(BaseModel):
    topic: str
    titles: list[str] = Field(..., min_length=1, max_length=5)
    hook: str
    voiceover: str
    estimated_duration: str
    jimeng_prompt: JimengPrompt
    reference_image_guide: str
    hashtags: list[str] = Field(default_factory=list)
    shooting_tips: str = ""


# ============================================================
# 请求/响应模型
# ============================================================
class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=300, description="用户输入的主题")
    reference_hints: Optional[list[str]] = Field(
        default=None, description="参考要素（未来对接图片识别）"
    )


class TranscribeResponse(BaseModel):
    text: str = Field(..., description="识别出的文字")
    duration_ms: int = Field(default=0, description="处理耗时")


class VideoScriptResponse(BaseModel):
    """历史详情响应"""
    id: int
    topic: str
    template: ScriptTemplate
    model_used: str
    generation_ms: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VideoScriptListItem(BaseModel):
    """历史列表item（轻量，不含完整template）"""
    id: int
    topic: str
    created_at: datetime

    class Config:
        from_attributes = True


class VideoScriptListResponse(BaseModel):
    items: list[VideoScriptListItem]
    total: int
    page: int = 1
    page_size: int = 20
