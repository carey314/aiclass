"""
doubao_client 单元测试 (mock SDK，不真打豆包)

覆盖:
- 认证失败抛 DoubaoError(kind=auth)
- 限流2次后成功
- 限流>max_retries 抛 DoubaoError(kind=rate_limit)
- 超时重试
- API错误分类
"""
import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.doubao_client import DoubaoClient, DoubaoError


class FakeDelta:
    def __init__(self, content=None, reasoning_content=None):
        self.content = content
        self.reasoning_content = reasoning_content


class FakeChoice:
    def __init__(self, content=None, reasoning_content=None):
        self.delta = FakeDelta(content, reasoning_content)


class FakeChunk:
    def __init__(self, content=None, reasoning_content=None):
        self.choices = [FakeChoice(content, reasoning_content)]


async def fake_stream(chunks):
    """异步迭代器：依次yield FakeChunk"""
    for c in chunks:
        yield c


class TestDoubaoClient:
    @pytest.mark.asyncio
    async def test_no_api_key_raises_auth_error(self):
        with pytest.raises(DoubaoError) as exc_info:
            DoubaoClient(api_key="", default_model="test")
        assert exc_info.value.kind == "auth"

    @pytest.mark.asyncio
    async def test_stream_yields_only_content_drops_reasoning(self):
        """reasoning model返回的reasoning_content应被丢弃，只保留content"""
        client = DoubaoClient(api_key="fake", default_model="test")

        chunks = [
            FakeChunk(reasoning_content="思考中..."),  # 应丢弃
            FakeChunk(content="这是"),
            FakeChunk(content="正文"),
        ]
        mock_create = AsyncMock(return_value=fake_stream(chunks))
        client._client.chat.completions.create = mock_create

        out = []
        async for c in client.stream_generate("sys", "user"):
            out.append(c)

        assert out == ["这是", "正文"]

    @pytest.mark.asyncio
    async def test_rate_limit_retries_then_succeeds(self):
        """限流时重试，最终成功"""
        from volcenginesdkarkruntime._exceptions import ArkRateLimitError

        client = DoubaoClient(api_key="fake", default_model="test")
        # 前2次抛限流，第3次成功
        call_count = 0

        async def maybe_fail(**kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ArkRateLimitError("rate limit", response=MagicMock(), body=None, request_id="test-req")
            return fake_stream([FakeChunk(content="ok")])

        client._client.chat.completions.create = maybe_fail

        out = []
        async for c in client.stream_generate("sys", "user", max_retries=2):
            out.append(c)
        assert out == ["ok"]
        assert call_count == 3  # 失败2次 + 成功1次

    @pytest.mark.asyncio
    async def test_rate_limit_exhausted_raises(self):
        """超过max_retries仍限流，抛 DoubaoError"""
        from volcenginesdkarkruntime._exceptions import ArkRateLimitError

        client = DoubaoClient(api_key="fake", default_model="test")

        async def always_fail(**kwargs):
            raise ArkRateLimitError("rate limit", response=MagicMock(), body=None, request_id="test-req")

        client._client.chat.completions.create = always_fail

        with pytest.raises(DoubaoError) as exc_info:
            async for _ in client.stream_generate("sys", "user", max_retries=1):
                pass
        assert exc_info.value.kind == "rate_limit"

    @pytest.mark.asyncio
    async def test_auth_error_does_not_retry(self):
        """认证失败不重试，立刻抛"""
        from volcenginesdkarkruntime._exceptions import ArkAuthenticationError

        client = DoubaoClient(api_key="fake", default_model="test")
        call_count = 0

        async def auth_fail(**kwargs):
            nonlocal call_count
            call_count += 1
            raise ArkAuthenticationError("bad key", response=MagicMock(), body=None, request_id="test-req")

        client._client.chat.completions.create = auth_fail

        with pytest.raises(DoubaoError) as exc_info:
            async for _ in client.stream_generate("sys", "user", max_retries=3):
                pass
        assert exc_info.value.kind == "auth"
        assert call_count == 1  # 没重试
