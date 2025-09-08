"""Application settings."""

import os
from typing import Any

from fastapi.responses import ORJSONResponse
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from src import __version__
from src.core.constants import APP_NAME
from src.core.enums import Environment


class Settings(BaseSettings):
    """Application settings with validation."""

    model_config = SettingsConfigDict(
        env_file=f".env.{os.getenv('ENVFLAG', Environment.DEV.value)}",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )

    # =============================================================================
    # AI SERVICE (REQUIRED)
    # =============================================================================
    # Chat service for document processing
    CHAT_API_KEY: str
    CHAT_BASE_URL: str
    CHAT_MODEL: str

    # Embedding service for vector generation
    EMBEDDING_API_KEY: str
    EMBEDDING_BASE_URL: str
    EMBEDDING_MODEL: str
    EMBEDDING_DIMENSION: int

    # =============================================================================
    # DATABASE
    # =============================================================================
    QDRANT_URL: str

    # =============================================================================
    # TASK SETUP
    # =============================================================================
    GIT_CLONE_TIMEOUT: int = Field(default=300, ge=60, le=1800)
    GIT_DEFAULT_BRANCH: str = Field(default="master")

    # =============================================================================
    # LOGGING
    # =============================================================================
    LOG_LEVEL: str = Field(
        default="INFO",
        pattern="^(TRACE|DEBUG|INFO|SUCCESS|WARNING|ERROR|CRITICAL)$",
    )
    LOG_PATH: str = Field(default="logs")
    LOG_FILENAME: str = Field(default=f"{APP_NAME}.log")
    LOG_ROTATION: str = Field(default="500 MB")
    LOG_RETENTION: str = Field(default="12 months")

    # =============================================================================
    # MONITORING (Optional)
    # =============================================================================
    SENTRY_DSN: str = Field(default="")
    SENTRY_SAMPLE_RATE: float = Field(default=0.1, ge=0.0, le=1.0)
    SENTRY_TRACES_SAMPLE_RATE: float = Field(default=0.05, ge=0.0, le=1.0)

    @property
    def ENVIRONMENT(self) -> Environment:
        """Get current environment from ENVFLAG.

        Returns:
            Environment enum based on ENVFLAG.
        """
        try:
            return Environment(os.getenv("ENVFLAG", Environment.DEV))
        except ValueError:
            return Environment.DEV

    @property
    def is_production(self) -> bool:
        """Check if environment is production.

        Returns:
            True if production, False otherwise.
        """
        return self.ENVIRONMENT == Environment.PROD

    @property
    def fastapi_config(self) -> dict[str, Any]:
        """Get FastAPI app configuration.

        Returns:
            FastAPI app config dict.
        """
        config: dict[str, Any] = {
            "title": APP_NAME,
            "version": __version__,
            "description": "open-context7 API server",
            "default_response_class": ORJSONResponse,
        }

        if self.is_production:
            config.update(
                {
                    "openapi_url": None,
                    "docs_url": None,
                    "redoc_url": None,
                }
            )
        else:
            config.update(
                {
                    "openapi_url": "/openapi.json",
                    "docs_url": "/docs",
                    "redoc_url": "/redoc",
                }
            )

        return config


settings = Settings()  # noqa
