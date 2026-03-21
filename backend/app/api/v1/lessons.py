from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.lesson import Lesson
from app.models.admin_user import AdminUser
from app.schemas.lesson import (
    LessonCreate, LessonUpdate, LessonResponse, LessonDetail, LessonWithStage,
)
from app.api.deps import get_current_admin

router = APIRouter(tags=["课程内容"])


# ========== 公开接口 ==========

@router.get("/lessons/{lesson_id}", response_model=LessonDetail)
async def get_lesson(lesson_id: int, db: AsyncSession = Depends(get_db)):
    """获取单节课详情（含完整内容）"""
    result = await db.execute(
        select(Lesson)
        .where(Lesson.id == lesson_id)
        .options(selectinload(Lesson.stage))
    )
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    if not lesson.is_published:
        raise HTTPException(status_code=404, detail="课程未发布")
    return lesson


# ========== 管理接口 ==========

@router.get("/admin/lessons", response_model=list[LessonWithStage])
async def admin_list_lessons(
    stage_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """管理端：获取所有课程（可按阶段筛选，含所属阶段信息）"""
    query = (
        select(Lesson)
        .options(selectinload(Lesson.stage))
        .order_by(Lesson.stage_id, Lesson.lesson_number)
    )
    if stage_id is not None:
        query = query.where(Lesson.stage_id == stage_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/admin/lessons/{lesson_id}", response_model=LessonDetail)
async def admin_get_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(
        select(Lesson)
        .where(Lesson.id == lesson_id)
        .options(selectinload(Lesson.stage))
    )
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    return lesson


@router.post("/admin/lessons", response_model=LessonResponse, status_code=201)
async def create_lesson(
    data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    lesson = Lesson(**data.model_dump())
    db.add(lesson)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.put("/admin/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: int,
    data: LessonUpdate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(lesson, key, value)
    await db.commit()
    await db.refresh(lesson)
    return lesson


@router.delete("/admin/lessons/{lesson_id}")
async def delete_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="课程不存在")
    await db.delete(lesson)
    await db.commit()
    return {"message": "删除成功"}
