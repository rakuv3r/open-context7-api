"""API response utilities."""

import uuid
from datetime import UTC
from datetime import datetime

from fastapi import Request

from src.schemas.base import BaseResponse
from src.schemas.base import ErrorResponse


def get_request_id(request: Request | None = None) -> str:
    """Get request ID from X-Request-ID header or create new one.

    Args:
        request: FastAPI request object.

    Returns:
        Request ID string.
    """
    if request is None:
        return str(uuid.uuid4())

    request_id = request.headers.get("X-Request-ID")
    return request_id if request_id else str(uuid.uuid4())


def success_response[T](
    data: T | None = None,
    message: str = "Operation successful",
    request: Request | None = None,
) -> BaseResponse[T]:
    """Create success response using BaseResponse schema.

    Args:
        data: Response data of any type.
        message: Success message.
        request: FastAPI request object for request_id.

    Returns:
        Standard success response.
    """
    return BaseResponse(
        data=data,
        message=message,
        createdAt=datetime.now(UTC).isoformat(),
        requestId=get_request_id(request),
    )


def error_response(
    message: str,
    request: Request | None = None,
) -> ErrorResponse:
    """Create error response.

    Args:
        message: Error message.
        request: FastAPI request object for request_id.

    Returns:
        Standard error response.
    """
    return ErrorResponse(
        error=message,
        createdAt=datetime.now(UTC).isoformat(),
        requestId=get_request_id(request),
    )
