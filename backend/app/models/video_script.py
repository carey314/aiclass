"""
VideoScript: 用户生成的即梦AI视频脚本记录

关系：
    admin_users (1) ─────── (N) video_scripts

每条记录保存一次完整的"主题→模板"生成结果，鞠姐能在历史里回看/复用。
"""
from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class VideoScript(Base):
    __tablename__ = "video_scripts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("admin_users.id", ondelete="CASCADE"),
        index=True,
    )
    topic: Mapped[str] = mapped_column(String(300))  # 用户输入的主题
    template_json: Mapped[str] = mapped_column(Text)  # 完整模板JSON字符串
    model_used: Mapped[str] = mapped_column(String(100))  # 哪个豆包模型
    generation_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)  # 实际耗时
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, index=True
    )

    __table_args__ = (
        # 复合索引：拉自己的历史时常用 (user_id, created_at DESC)
        Index("idx_video_scripts_user_created", "user_id", "created_at"),
    )
