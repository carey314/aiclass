"""
video_script API 集成测试

覆盖：
- 白名单校验（403）
- 跨用户访问/删除防护（IRON RULE — 安全关键）
- 历史分页
- 删除404场景
"""
import pytest
import pytest_asyncio
import json
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.database.base import Base
from app.database.connection import get_db
from app.models.admin_user import AdminUser
from app.models.video_script import VideoScript
from app.core.security import get_password_hash, create_access_token
from app.config import settings


@pytest_asyncio.fixture
async def test_app():
    """每个测试一个独立的内存DB + override get_db"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def _get_db_override():
        async with sm() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[get_db] = _get_db_override

    yield app, sm

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_app):
    app_inst, _ = test_app
    transport = ASGITransport(app=app_inst)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def admin_token(test_app):
    """创建admin用户(在白名单内)，返回token"""
    _, sm = test_app
    async with sm() as session:
        user = AdminUser(
            username="admin",
            hashed_password=get_password_hash("pwd"),
            display_name="管理员",
            is_active=True,
        )
        session.add(user)
        await session.commit()
    return create_access_token({"sub": "admin"}), 1  # token, user_id


@pytest_asyncio.fixture
async def other_token(test_app):
    """创建第二个admin用户(不在白名单内)，用于测试白名单+权限隔离"""
    _, sm = test_app
    async with sm() as session:
        user = AdminUser(
            username="not_allowed_user",
            hashed_password=get_password_hash("pwd"),
            display_name="其他",
            is_active=True,
        )
        session.add(user)
        await session.commit()
    return create_access_token({"sub": "not_allowed_user"}), 2


class TestAuth:
    @pytest.mark.asyncio
    async def test_no_token_returns_403_or_401(self, client):
        """未提供Bearer token，FastAPI HTTPBearer 默认 403"""
        resp = await client.get("/api/v1/video_script/history")
        assert resp.status_code in (401, 403)

    @pytest.mark.asyncio
    async def test_invalid_token_returns_401(self, client):
        resp = await client.get(
            "/api/v1/video_script/history",
            headers={"Authorization": "Bearer fake.token.xxx"},
        )
        assert resp.status_code == 401


class TestWhitelist:
    @pytest.mark.asyncio
    async def test_non_whitelisted_user_returns_403(self, client, other_token):
        token, _ = other_token
        resp = await client.get(
            "/api/v1/video_script/history",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403

    @pytest.mark.asyncio
    async def test_whitelisted_admin_can_access(self, client, admin_token):
        token, _ = admin_token
        resp = await client.get(
            "/api/v1/video_script/history",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200


class TestHistory:
    @pytest.mark.asyncio
    async def test_empty_history_returns_zero(self, client, admin_token):
        token, _ = admin_token
        resp = await client.get(
            "/api/v1/video_script/history",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 0
        assert body["items"] == []

    @pytest.mark.asyncio
    async def test_only_own_scripts_in_history(self, client, admin_token, test_app):
        """IRON RULE: 用户只能看到自己的scripts"""
        token, my_user_id = admin_token
        _, sm = test_app

        # 在DB里塞2条admin的, 1条other的
        async with sm() as session:
            session.add_all([
                VideoScript(
                    user_id=my_user_id, topic="主题1",
                    template_json='{"x":1}', model_used="test",
                ),
                VideoScript(
                    user_id=my_user_id, topic="主题2",
                    template_json='{"x":2}', model_used="test",
                ),
                VideoScript(
                    user_id=999, topic="别人的",  # 不存在的user_id也行
                    template_json='{"y":1}', model_used="test",
                ),
            ])
            await session.commit()

        resp = await client.get(
            "/api/v1/video_script/history",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 2  # 只看到自己的2条
        topics = [item["topic"] for item in body["items"]]
        assert "主题1" in topics and "主题2" in topics
        assert "别人的" not in topics


class TestSecurityIsolation:
    """IRON RULE: 跨用户访问防护"""

    @pytest.mark.asyncio
    async def test_cannot_get_others_script(self, client, admin_token, test_app):
        """A用户不能GET B用户的script (返回404，不泄露存在性)"""
        token, _ = admin_token
        _, sm = test_app

        async with sm() as session:
            # 别人的script
            other_script = VideoScript(
                user_id=999, topic="机密",
                template_json='{"secret":1}', model_used="test",
            )
            session.add(other_script)
            await session.commit()
            await session.refresh(other_script)
            other_id = other_script.id

        resp = await client.get(
            f"/api/v1/video_script/{other_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404  # 不返回403避免泄露存在性

    @pytest.mark.asyncio
    async def test_cannot_delete_others_script(self, client, admin_token, test_app):
        """A用户不能DELETE B用户的script"""
        token, _ = admin_token
        _, sm = test_app

        async with sm() as session:
            other_script = VideoScript(
                user_id=999, topic="别人的",
                template_json='{"x":1}', model_used="test",
            )
            session.add(other_script)
            await session.commit()
            await session.refresh(other_script)
            other_id = other_script.id

        # 尝试删除
        resp = await client.delete(
            f"/api/v1/video_script/{other_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404

        # 验证没被删除
        async with sm() as session:
            from sqlalchemy import select
            result = await session.execute(select(VideoScript).where(VideoScript.id == other_id))
            still_there = result.scalar_one_or_none()
            assert still_there is not None  # 还在


class TestDelete:
    @pytest.mark.asyncio
    async def test_delete_nonexistent_returns_404(self, client, admin_token):
        token, _ = admin_token
        resp = await client.delete(
            "/api/v1/video_script/99999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_own_script_succeeds(self, client, admin_token, test_app):
        token, my_user_id = admin_token
        _, sm = test_app

        async with sm() as session:
            script = VideoScript(
                user_id=my_user_id, topic="我的",
                template_json='{"x":1}', model_used="test",
            )
            session.add(script)
            await session.commit()
            await session.refresh(script)
            script_id = script.id

        resp = await client.delete(
            f"/api/v1/video_script/{script_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 204

        # 二次删除应404
        resp2 = await client.delete(
            f"/api/v1/video_script/{script_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp2.status_code == 404


class TestTranscribe:
    @pytest.mark.asyncio
    async def test_too_small_audio_returns_empty(self, client, admin_token):
        """极小音频(<100B)视为空录音"""
        token, _ = admin_token
        files = {"audio": ("test.webm", b"x" * 50, "audio/webm")}
        resp = await client.post(
            "/api/v1/video_script/transcribe",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
        )
        assert resp.status_code == 200
        assert resp.json()["text"] == ""

    @pytest.mark.asyncio
    async def test_too_large_audio_returns_413(self, client, admin_token):
        """超过max size返回413"""
        token, _ = admin_token
        # 大于10MB
        big_audio = b"x" * (11 * 1024 * 1024)
        files = {"audio": ("test.webm", big_audio, "audio/webm")}
        resp = await client.post(
            "/api/v1/video_script/transcribe",
            headers={"Authorization": f"Bearer {token}"},
            files=files,
        )
        assert resp.status_code == 413
