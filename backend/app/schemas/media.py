from datetime import datetime
from pydantic import BaseModel


class MediaResponse(BaseModel):
    id: int
    filename: str
    filepath: str
    media_type: str
    mime_type: str
    file_size: int
    lesson_id: int | None
    alt_text: str | None
    created_at: datetime
    url: str = ""

    class Config:
        from_attributes = True
