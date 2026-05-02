"""
火山引擎ARK / 豆包大模型客户端封装

提供:
- 文本生成（流式 + 非流式）
- 自动retry + 指数退避
- 错误分类（认证/限流/超时/拒答）

数据流：
    user_input → build_prompt → ARK API → JSON模板 / 流式token
"""
from __future__ import annotations

import asyncio
import logging
from typing import AsyncIterator, Optional

from volcenginesdkarkruntime import AsyncArk
from volcenginesdkarkruntime._exceptions import (
    ArkAPIError,
    ArkAuthenticationError,
    ArkRateLimitError,
    ArkAPITimeoutError,
)

from app.config import settings

logger = logging.getLogger(__name__)


class DoubaoError(Exception):
    """统一的豆包调用异常，包含可读的错误类型"""

    def __init__(self, message: str, kind: str = "unknown"):
        super().__init__(message)
        self.kind = kind  # auth | rate_limit | timeout | refused | api_error


class DoubaoClient:
    """
    豆包模型异步客户端（singleton）。

    使用方式：
        client = get_doubao_client()
        async for chunk in client.stream_generate(...):
            yield chunk
    """

    def __init__(self, api_key: str, default_model: str):
        if not api_key:
            raise DoubaoError("ARK_API_KEY 未配置", kind="auth")
        self._client = AsyncArk(api_key=api_key)
        self._default_model = default_model

    async def stream_generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        max_retries: int = 2,
    ) -> AsyncIterator[str]:
        """
        流式生成文本，逐token yield。

        约定：
            - 失败重试2次（限流和超时），认证失败和拒答不重试
            - 用户拿到的是纯文本片段，不含SSE格式

        注意：reasoning model（如Seed-2.0-Pro）会有推理过程
        我们丢弃 reasoning_content，只输出最终 content。
        """
        the_model = model or self._default_model

        for attempt in range(max_retries + 1):
            try:
                stream = await self._client.chat.completions.create(
                    model=the_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True,
                )
                async for chunk in stream:
                    if not chunk.choices:
                        continue
                    delta = chunk.choices[0].delta
                    # reasoning model: 丢弃 reasoning_content
                    if hasattr(delta, "content") and delta.content:
                        yield delta.content
                return  # 成功即退出整个函数

            except ArkAuthenticationError as e:
                logger.error("豆包认证失败: %s", e)
                raise DoubaoError(f"API认证失败，请检查 ARK_API_KEY: {e}", kind="auth")

            except ArkRateLimitError as e:
                logger.warning("豆包限流(尝试 %d/%d): %s", attempt + 1, max_retries + 1, e)
                if attempt >= max_retries:
                    raise DoubaoError("API繁忙，稍候再试", kind="rate_limit")
                await asyncio.sleep(2**attempt)  # 指数退避：1s, 2s

            except ArkAPITimeoutError as e:
                logger.warning("豆包超时(尝试 %d/%d): %s", attempt + 1, max_retries + 1, e)
                if attempt >= max_retries:
                    raise DoubaoError("API响应超时，请重试", kind="timeout")
                await asyncio.sleep(1)

            except ArkAPIError as e:
                logger.error("豆包API错误: %s", e)
                raise DoubaoError(f"API调用失败: {e}", kind="api_error")

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        max_retries: int = 2,
    ) -> str:
        """
        非流式生成（用于test/eval场景），等完整返回。
        """
        chunks = []
        async for chunk in self.stream_generate(
            system_prompt,
            user_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
        ):
            chunks.append(chunk)
        return "".join(chunks)

    async def transcribe(self, audio_bytes: bytes, audio_format: str = "webm") -> str:
        """
        语音转文字。

        注意：火山引擎ASR目前在SDK中需要使用语音相关endpoint，
        SDK里通过 audio.transcriptions.create 暴露。

        如果SDK不支持，会fallback到raw HTTP（在voice_recognition.py里实现）。
        """
        # SDK封装的audio接口（如果可用）
        if hasattr(self._client, "audio"):
            try:
                result = await self._client.audio.transcriptions.create(
                    model=settings.ARK_ASR_MODEL,
                    file=("audio." + audio_format, audio_bytes),
                )
                return result.text or ""
            except Exception as e:
                logger.error("豆包ASR调用失败: %s", e)
                raise DoubaoError(f"语音识别失败: {e}", kind="api_error")
        else:
            raise DoubaoError("当前SDK不支持音频接口，使用 voice_recognition.py", kind="api_error")


# Singleton
_client_instance: Optional[DoubaoClient] = None


def get_doubao_client() -> DoubaoClient:
    """获取豆包客户端singleton。每次调用复用同一个连接池。"""
    global _client_instance
    if _client_instance is None:
        _client_instance = DoubaoClient(
            api_key=settings.ARK_API_KEY,
            default_model=settings.ARK_TEXT_MODEL,
        )
    return _client_instance
