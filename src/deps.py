"""Library dependency injection."""

from functools import lru_cache

from fastapi import Depends
from qdrant_client import AsyncQdrantClient

# Adapter classes
from src.adapters.ai import AIProvider
from src.core.config import settings

# Schemas only
# Service classes
from src.services.library import LibraryService

# Utility classes
from src.utils.common import md5_hash


# Singleton adapter factories with lru_cache
@lru_cache
def get_ai_provider() -> AIProvider:
    """Get AI provider singleton."""
    return AIProvider()


@lru_cache
def get_qdrant_client() -> AsyncQdrantClient:
    """Get Qdrant client singleton."""
    return AsyncQdrantClient(url=settings.QDRANT_URL)


# Service factory
def get_service(
    ai: AIProvider = Depends(get_ai_provider),
    qdrant: AsyncQdrantClient = Depends(get_qdrant_client),
) -> LibraryService:
    """Get library service with all dependencies.

    Args:
        ai: AI provider dependency.
        qdrant: Qdrant client dependency.

    Returns:
        LibraryService instance with injected dependencies.
    """
    return LibraryService(ai, qdrant)


# Utility dependencies
def get_library_id(org: str, project: str) -> str:
    """Generate library ID from organization and project names.

    Args:
        org: Organization name.
        project: Project name.

    Returns:
        MD5 hash of the combined path.
    """
    return md5_hash(f"/{org}/{project}")
