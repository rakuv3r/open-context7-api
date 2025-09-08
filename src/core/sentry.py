"""Error monitoring with Sentry."""

from typing import Any

import sentry_sdk
from loguru import logger

from src.core.config import settings
from src.core.errors import IgnoredError


def before_send(event: Any, hint: Any) -> Any | None:
    """Filter out business errors from Sentry reports.

    Prevents expected errors (like validation failures) from appearing
    in Sentry, so you only see real system problems.

    Args:
        event: Sentry event to filter.
        hint: Additional context about the event.

    Returns:
        The event if it should be sent, None if filtered.
    """
    if isinstance(hint, dict) and "exc_info" in hint:
        _, exc_value, _ = hint["exc_info"]
        if isinstance(exc_value, IgnoredError):
            return None
    return event


def setup_sentry() -> None:
    """Initialize Sentry error monitoring.

    Sets up error tracking with filtering and environment config.
    Skips setup if no Sentry DSN is provided.
    """
    if not settings.SENTRY_DSN:
        logger.debug("Sentry not configured, skipping initialization.")
        return

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        sample_rate=settings.SENTRY_SAMPLE_RATE,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
        before_send=before_send,
    )

    logger.info("Sentry initialized.")
