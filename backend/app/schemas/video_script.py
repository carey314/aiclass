"""
VideoScript Pydantic schemas — 输入/输出数据结构

V2 升级：
- 增加 voiceover.segments（4段时间线分镜）
- 增加 shooting_plan（鞠姐自拍 vs 即梦B-roll 分离）
- 增加 jimeng_prompt.summary（一段直接复制的总结版）
- hook_type 标注（让用户知道用了哪种钩子）
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ============================================================
# 口播分段（按时间线）
# ============================================================
class VoiceoverSegment(BaseModel):
    time: str = Field(..., description="如 '0-3秒'")
    label: str = Field(..., description="如 '钩子'/'痛点放大'/'解决方案'/'互动+免责'")
    text: str = Field(..., description="该段文案")


class Voiceover(BaseModel):
    full_text: str = Field(..., description="完整口播稿（合并版）")
    segments: list[VoiceoverSegment] = Field(default_factory=list, description="4段分时间线版")


# ============================================================
# 拍摄计划（自拍 + B-roll）
# ============================================================
class BrollSegment(BaseModel):
    time: str = Field(..., description="如 '5-10秒'")
    scene: str = Field(..., description="即梦B-roll场景描述（不含人脸）")


class ShootingPlan(BaseModel):
    self_shot: list[str] = Field(default_factory=list, description="鞠姐自拍部分的拍摄建议")
    broll_jimeng: list[BrollSegment] = Field(default_factory=list, description="即梦B-roll时间线")


# ============================================================
# 即梦提示词 6段结构（V2: 加summary）
# ============================================================
class JimengPrompt(BaseModel):
    summary: str = Field("", description="一段总结版，可直接复制粘贴到即梦")
    subject: str = Field(..., description="主体：食材/物品/部位（不含人物全身/脸）")
    scene: str = Field(..., description="场景：环境+时间+氛围")
    motion: str = Field(..., description="运动：食材动作/手部操作")
    camera: str = Field(..., description="镜头：景别+运镜（按时间线写更佳）")
    mood: str = Field(..., description="氛围：色调+光影")
    style: str = Field(..., description="风格：写实摄影风/电影感纪录片")


# ============================================================
# 完整的视频脚本模板（V2）
# ============================================================
class ScriptTemplate(BaseModel):
    topic: str
    titles: list[str] = Field(..., min_length=1, max_length=5)
    hook: str
    hook_type: Optional[str] = Field(default="", description="反常识/纠错/痛点暴击/数字冲击")
    voiceover: Voiceover
    shooting_plan: Optional[ShootingPlan] = None
    jimeng_prompt: JimengPrompt
    reference_image_guide: str = ""
    hashtags: list[str] = Field(default_factory=list)
    shooting_tips: list[str] | str = Field(default_factory=list)
    estimated_total_duration: Optional[str] = Field(default="", alias="estimated_duration")
    # 兼容V1: estimated_duration 也接受
    model_config = {"populate_by_name": True, "extra": "ignore"}


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


class QuickTopicsResponse(BaseModel):
    """快捷主题列表（首页展示）"""
    topics: list[dict]
