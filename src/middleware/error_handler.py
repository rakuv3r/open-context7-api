"""Global error handling middleware."""

from collections.abc import Awaitable
from collections.abc import Callable

import sentry_sdk
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.responses import ORJSONResponse
from loguru import logger

from src.core.config import settings
from src.core.errors import AppError
from src.core.errors import IgnoredError
from src.utils.response import error_response
from src.utils.response import get_request_id


async def error_handler_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Handle requests and catch any errors.

    Args:
        request: The HTTP request.
        call_next: The next middleware or endpoint.

    Returns:
        HTTP response from processing or error handling.
    """
    try:
        return await call_next(request)
    except IgnoredError as e:
        request_id = get_request_id(request)
        logger.error(f"[{request_id}] {e.__class__.__name__}: {e.message}")

        response_data = error_response(message=e.message, request=request)

        return ORJSONResponse(
            status_code=e.status_code, content=response_data.model_dump()
        )
    except Exception as e:
        request_id = get_request_id(request)
        logger.error(f"[{request_id}] Unhandled error: {e}", exc_info=True)

        if settings.SENTRY_DSN:
            sentry_sdk.capture_exception(e)

        # Handle app errors vs Python errors
        if isinstance(e, AppError):
            # App errors have message and status code
            message = e.message
            status_code = e.status_code
        else:
            # Python errors - only message available
            message = str(e)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        response_data = error_response(message=message, request=request)
        return ORJSONResponse(
            status_code=status_code, content=response_data.model_dump()
        )
