from datetime import datetime
from pydantic import BaseModel


class LessonBase(BaseModel):
    title: str
    subtitle: str | None = None
    stage_id: int
    lesson_number: int
    content: str = ""
    summary: str | None = None
    cover_image: str | None = None
    duration_minutes: int | None = None
    is_free: bool = False
    is_published: bool = False


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    stage_id: int | None = None
    lesson_number: int | None = None
    content: str | None = None
    summary: str | None = None
    cover_image: str | None = None
    duration_minutes: int | None = None
    is_free: bool | None = None
    is_published: bool | None = None


class StageBrief(BaseModel):
    id: int
    title: str
    stage_number: int

    class Config:
        from_attributes = True


class LessonResponse(LessonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LessonWithStage(LessonResponse):
    """课程列表项（含所属阶段信息）"""
    stage: StageBrief

    class Config:
        from_attributes = True


class LessonDetail(LessonResponse):
    stage: StageBrief
