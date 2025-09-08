"""Application middleware."""

from fastapi import FastAPI

from src.middleware.error_handler import error_handler_middleware


def register_middlewares(app: FastAPI) -> None:
    """Register all middlewares in correct order.

    Args:
        app: FastAPI application instance.
    """
    # Error handler middleware
    app.middleware("http")(error_handler_middleware)
