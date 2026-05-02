"""
Pytest 共享fixtures
"""
import os
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database.base import Base


@pytest_asyncio.fixture
async def db_session():
    """每个测试一个独立的内存DB"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with sm() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture
async def admin_user(db_session):
    """创建一个测试用的admin用户（在白名单内）"""
    from app.models.admin_user import AdminUser
    from app.core.security import get_password_hash

    user = AdminUser(
        username="admin",
        hashed_password=get_password_hash("test_password"),
        display_name="测试管理员",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def other_user(db_session):
    """另一个用户（不在白名单内），用于安全测试"""
    from app.models.admin_user import AdminUser
    from app.core.security import get_password_hash

    user = AdminUser(
        username="other_user",
        hashed_password=get_password_hash("test_password"),
        display_name="其他用户",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user
