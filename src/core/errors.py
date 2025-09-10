"""Custom application exception classes."""

from fastapi import status

from src.core.constants import RETCODE_CHAT_SERVICE_ERROR
from src.core.constants import RETCODE_CONFIGURATION_ERROR
from src.core.constants import RETCODE_EMBEDDING_SERVICE_ERROR
from src.core.constants import RETCODE_INTERNAL_ERROR
from src.core.constants import RETCODE_RESOURCE_ALREADY_EXISTS
from src.core.constants import RETCODE_RESOURCE_NOT_FOUND
from src.core.constants import RETCODE_VALIDATION_ERROR


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        retcode: int = RETCODE_INTERNAL_ERROR,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        """Initialize application error.

        Args:
            message: Error message.
            retcode: Return code for API response.
            status_code: HTTP status code.
        """
        self.message = message
        self.retcode = retcode
        self.status_code = status_code
        super().__init__(self.message)


class IgnoredError(AppError):
    """Expected business errors that do not need monitoring."""

    def __init__(
        self,
        message: str,
        retcode: int,
        status_code: int = status.HTTP_200_OK,
    ):
        """Initialize ignored error.

        Args:
            message: Error message.
            retcode: Return code for API response.
            status_code: HTTP status code.
        """
        super().__init__(message, retcode, status_code)


# Business errors - expected and don't need monitoring
class ValidationError(IgnoredError):
    """Input validation error."""

    def __init__(self, message: str):
        """Initialize validation error.

        Args:
            message: Validation error message.
        """
        super().__init__(message, RETCODE_VALIDATION_ERROR)


class ResourceNotFoundError(IgnoredError):
    """Resource not found error."""

    def __init__(self, message: str):
        """Initialize resource not found error.

        Args:
            message: Resource not found message.
        """
        super().__init__(message, RETCODE_RESOURCE_NOT_FOUND)


class ResourceAlreadyExistsError(IgnoredError):
    """Resource already exists error."""

    def __init__(self, message: str):
        """Initialize resource already exists error.

        Args:
            message: Resource exists message.
        """
        super().__init__(message, RETCODE_RESOURCE_ALREADY_EXISTS)


# System errors - unexpected and need monitoring
class ConfigurationError(AppError):
    """Configuration error."""

    def __init__(self, message: str):
        """Initialize configuration error.

        Args:
            message: Configuration error message.
        """
        super().__init__(
            message, RETCODE_CONFIGURATION_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ChatServiceError(AppError):
    """Chat service error."""

    def __init__(self, message: str):
        """Initialize chat service error.

        Args:
            message: Chat service error message.
        """
        super().__init__(
            message, RETCODE_CHAT_SERVICE_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class EmbeddingServiceError(AppError):
    """Embedding service error."""

    def __init__(self, message: str):
        """Initialize embedding service error.

        Args:
            message: Embedding service error message.
        """
        super().__init__(
            message,
            RETCODE_EMBEDDING_SERVICE_ERROR,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
