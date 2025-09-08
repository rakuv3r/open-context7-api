"""Application enums."""

from enum import Enum
from enum import unique


@unique
class Environment(str, Enum):
    """Application environments."""

    DEV = "dev"
    BETA = "beta"
    PROD = "prod"


@unique
class LibraryStatus(str, Enum):
    """Library processing status."""

    PROCESSING = "processing"
    FINALIZED = "finalized"
    FAILED = "failed"
