from datetime import datetime
from pydantic import BaseModel


class StageBase(BaseModel):
    title: str
    subtitle: str = ""
    description: str = ""
    stage_number: int
    icon: str | None = None
    is_free: bool = False
    is_published: bool = False


class StageCreate(StageBase):
    pass


class StageUpdate(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    description: str | None = None
    stage_number: int | None = None
    icon: str | None = None
    is_free: bool | None = None
    is_published: bool | None = None


class LessonBrief(BaseModel):
    id: int
    title: str
    subtitle: str | None
    lesson_number: int
    summary: str | None
    cover_image: str | None
    duration_minutes: int | None
    is_free: bool
    is_published: bool

    class Config:
        from_attributes = True


class StageResponse(StageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StageWithLessons(StageResponse):
    lessons: list[LessonBrief] = []
