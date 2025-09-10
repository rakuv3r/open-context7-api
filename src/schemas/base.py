"""Base response schemas for API responses."""

from pydantic import BaseModel
from pydantic import Field


class BaseResponse[T](BaseModel):
    """Base API response format with retcode."""

    retcode: int = Field(0, description="Return code: 0=success, >0=error")
    data: T | None = Field(None, description="Response data")
    message: str = Field(..., description="Status message")
    createdAt: str = Field(..., description="Creation time in ISO format")
    requestId: str = Field(..., description="Request ID")


class ErrorResponse(BaseModel):
    """Error response format with retcode."""

    retcode: int = Field(..., description="Error code")
    error: str = Field(..., description="Error message")
    createdAt: str = Field(..., description="Creation time in ISO format")
    requestId: str = Field(..., description="Request ID")
