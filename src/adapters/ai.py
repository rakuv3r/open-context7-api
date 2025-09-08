"""AI service adapter using LiteLLM."""

from typing import Any

import litellm
from loguru import logger

from src.core.config import settings
from src.core.errors import ChatServiceError
from src.core.errors import EmbeddingServiceError
from src.schemas.ai import EmbeddingResult


class AIProvider:
    """AI service provider using LiteLLM.

    Provides chat and embedding services through unified interface.
    Supports multiple AI providers.
    """

    def __init__(self) -> None:
        """Init AI service provider.

        Log configured chat and embedding service info.
        """
        logger.info(f"Chat service: {settings.CHAT_MODEL} @ {settings.CHAT_BASE_URL}")
        logger.info(
            f"Embedding service: {settings.EMBEDDING_MODEL} "
            f"@ {settings.EMBEDDING_BASE_URL}"
        )
        logger.info(f"Embedding dimension: {settings.EMBEDDING_DIMENSION}")

    @staticmethod
    async def chat_completion(
        messages: list[dict[str, Any]],
        temperature: float = 0.1,
    ) -> str:
        """Create chat completion using LLM.

        Args:
            messages: List of message dicts with 'role' and 'content' keys.
            temperature: Randomness level (0.0 to 2.0).

        Returns:
            Generated text content.

        Raises:
            ChatServiceError: If chat completion fails.
        """
        try:
            response = await litellm.acompletion(
                model=settings.CHAT_MODEL,
                messages=messages,
                temperature=temperature,
                api_key=settings.CHAT_API_KEY,
                api_base=settings.CHAT_BASE_URL,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Chat completion failed: {e}")
            raise ChatServiceError(str(e)) from e

    @staticmethod
    async def embedding(text: str) -> EmbeddingResult:
        """Create embedding for text.

        Args:
            text: Text to create embedding for.

        Returns:
            EmbeddingResult with vector and token count.

        Raises:
            EmbeddingServiceError: If embedding creation fails.
        """
        try:
            response = await litellm.aembedding(
                model=settings.EMBEDDING_MODEL,
                input=[text],
                api_key=settings.EMBEDDING_API_KEY,
                api_base=settings.EMBEDDING_BASE_URL,
                dimensions=settings.EMBEDDING_DIMENSION,
            )
            return EmbeddingResult(
                embedding=response["data"][0]["embedding"],
                embedding_tokens=response.usage.prompt_tokens,
            )
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise EmbeddingServiceError(str(e)) from e
