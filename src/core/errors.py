"""Custom application exception classes."""

from fastapi import status


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        """Initialize application error.

        Args:
            message: Error message.
            status_code: HTTP status code.
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class IgnoredError(AppError):
    """Expected business errors that do not need monitoring."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        """Initialize ignored error.

        Args:
            message: Error message.
            status_code: HTTP status code.
        """
        super().__init__(message, status_code)


# Business errors - expected and don't need monitoring
class ValidationError(IgnoredError):
    """Input validation error."""

    def __init__(self, message: str):
        """Initialize validation error.

        Args:
            message: Validation error message.
        """
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class ResourceNotFoundError(IgnoredError):
    """Resource not found error."""

    def __init__(self, message: str):
        """Initialize resource not found error.

        Args:
            message: Resource not found message.
        """
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ResourceAlreadyExistsError(IgnoredError):
    """Resource already exists error."""

    def __init__(self, message: str):
        """Initialize resource already exists error.

        Args:
            message: Resource exists message.
        """
        super().__init__(message, status.HTTP_409_CONFLICT)


# System errors - unexpected and need monitoring
class ConfigurationError(AppError):
    """Configuration error."""

    def __init__(self, message: str):
        """Initialize configuration error.

        Args:
            message: Configuration error message.
        """
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChatServiceError(AppError):
    """Chat service error."""

    def __init__(self, message: str):
        """Initialize chat service error.

        Args:
            message: Chat service error message.
        """
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmbeddingServiceError(AppError):
    """Embedding service error."""

    def __init__(self, message: str):
        """Initialize embedding service error.

        Args:
            message: Embedding service error message.
        """
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)
