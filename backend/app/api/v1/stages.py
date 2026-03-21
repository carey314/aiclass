from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.stage import Stage
from app.models.lesson import Lesson
from app.models.media import Media
from app.models.admin_user import AdminUser
from app.schemas.stage import (
    StageCreate, StageUpdate, StageResponse, StageWithLessons,
)
from app.api.deps import get_current_admin

router = APIRouter(tags=["课程阶段"])


# ========== 公开接口 ==========

@router.get("/stages", response_model=list[StageWithLessons])
async def list_stages(db: AsyncSession = Depends(get_db)):
    """获取所有已发布的课程阶段（含课程列表）"""
    result = await db.execute(
        select(Stage)
        .where(Stage.is_published == True)  # noqa: E712
        .options(selectinload(Stage.lessons))
        .order_by(Stage.stage_number)
    )
    stages = result.scalars().all()
    # 只返回已发布的课程
    for stage in stages:
        stage.lessons = [l for l in stage.lessons if l.is_published]
    return stages


@router.get("/stages/{stage_id}", response_model=StageWithLessons)
async def get_stage(stage_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个阶段详情（含课程列表）"""
    result = await db.execute(
        select(Stage)
        .where(Stage.id == stage_id)
        .options(selectinload(Stage.lessons))
    )
    stage = result.scalar_one_or_none()
    if not stage:
        raise HTTPException(status_code=404, detail="阶段不存在")
    if not stage.is_published:
        raise HTTPException(status_code=404, detail="阶段未发布")
    stage.lessons = [l for l in stage.lessons if l.is_published]
    return stage


# ========== 管理接口 ==========

@router.get("/admin/stages", response_model=list[StageWithLessons])
async def admin_list_stages(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """管理端：获取所有阶段（含草稿）"""
    result = await db.execute(
        select(Stage)
        .options(selectinload(Stage.lessons))
        .order_by(Stage.stage_number)
    )
    return result.scalars().all()


@router.post("/admin/stages", response_model=StageResponse, status_code=201)
async def create_stage(
    data: StageCreate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    stage = Stage(**data.model_dump())
    db.add(stage)
    await db.commit()
    await db.refresh(stage)
    return stage


@router.put("/admin/stages/{stage_id}", response_model=StageResponse)
async def update_stage(
    stage_id: int,
    data: StageUpdate,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Stage).where(Stage.id == stage_id))
    stage = result.scalar_one_or_none()
    if not stage:
        raise HTTPException(status_code=404, detail="阶段不存在")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(stage, key, value)
    await db.commit()
    await db.refresh(stage)
    return stage


@router.delete("/admin/stages/{stage_id}")
async def delete_stage(
    stage_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Stage).where(Stage.id == stage_id))
    stage = result.scalar_one_or_none()
    if not stage:
        raise HTTPException(status_code=404, detail="阶段不存在")
    await db.delete(stage)
    await db.commit()
    return {"message": "删除成功"}


@router.get("/admin/dashboard/stats")
async def admin_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    """管理端：获取仪表盘统计数据"""
    # 阶段总数
    total_stages = (await db.execute(select(func.count(Stage.id)))).scalar() or 0

    # 课程统计
    total_lessons = (await db.execute(select(func.count(Lesson.id)))).scalar() or 0
    published_lessons = (
        await db.execute(
            select(func.count(Lesson.id)).where(Lesson.is_published == True)  # noqa: E712
        )
    ).scalar() or 0
    draft_lessons = total_lessons - published_lessons

    # 媒体总数
    total_media = (await db.execute(select(func.count(Media.id)))).scalar() or 0

    # 总时长
    total_duration_minutes = (
        await db.execute(select(func.sum(Lesson.duration_minutes)))
    ).scalar() or 0

    # 最近更新的5节课
    recent_result = await db.execute(
        select(Lesson)
        .options(selectinload(Lesson.stage))
        .order_by(Lesson.updated_at.desc())
        .limit(5)
    )
    recent_lessons = [
        {
            "id": lesson.id,
            "title": lesson.title,
            "stage_title": lesson.stage.title,
            "is_published": lesson.is_published,
            "updated_at": lesson.updated_at.isoformat() if lesson.updated_at else None,
        }
        for lesson in recent_result.scalars().all()
    ]

    return {
        "total_stages": total_stages,
        "total_lessons": total_lessons,
        "published_lessons": published_lessons,
        "draft_lessons": draft_lessons,
        "total_media": total_media,
        "total_duration_minutes": total_duration_minutes,
        "recent_lessons": recent_lessons,
    }
