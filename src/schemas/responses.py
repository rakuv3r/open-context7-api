"""Response models."""

from pydantic import BaseModel
from pydantic import Field


class DocumentResponse(BaseModel):
    """Document response model.

    This class represents a single document in search results,
    containing the document content and metadata for display.

    Attributes:
        title: The document title or filename.
            Used for display in search results.
        description: Brief description of the document content.
            Auto-generated summary or manual description.
        source: The source file path or URL where this document comes from.
            Helps users locate the original document.
        language: Programming language of the document.
            Used for syntax highlighting and filtering.
        code: The actual document content or code.
            This is the main content that matches search queries.
        tokens: Number of tokens in the document.
            Used for API billing and content size tracking.
        score: Relevance score for search results.
            Higher scores indicate better matches to the query.
    """

    title: str
    description: str
    source: str
    language: str
    code: str
    tokens: int = 0
    score: float | None = None


class LibrarySearchItem(BaseModel):
    """Internal library search item from storage.

    This class represents a library entry in search results,
    containing basic library information and processing status.

    Attributes:
        org: Organization name that owns the library.
            Usually the GitHub organization or user name.
        project: Project name within the organization.
            Usually the repository name.
        title: Display title for the library.
            Can be empty if not set by user.
        description: Optional description of the library.
            Explains what the library contains or does.
        branch: Git branch being tracked.
            Defaults to "main" if not specified.
        last_update_date: When the library was last updated.
            ISO format date string, empty if never updated.
        state: Current processing state of the library.
            Values like "processing", "completed", "failed".
        total_tokens: Total number of tokens in all documents.
            Used for billing and storage tracking.
        tags: List of tags assigned to this library.
            Used for categorization and filtering.
        score: Search relevance score when used in search results.
            Higher scores indicate better matches to the query.
    """

    org: str
    project: str
    title: str = ""
    description: str = ""
    branch: str = "main"
    last_update_date: str = ""
    state: str = "processing"
    total_tokens: int = 0
    tags: list[str] = Field(default_factory=list)
    score: float | None = None


class LibraryDetail(BaseModel):
    """Internal library detail model for service layer.

    This class contains complete library information including
    repository details, processing status, and metadata.
    Used internally by services for library management.

    Attributes:
        library_id: Unique identifier for the library.
            Generated when the library is first created.
        status: Current processing status of the library.
            Values include "processing", "completed", "failed".
        repo_url: URL of the source Git repository.
            Required for repository-based libraries, None for content uploads.
        access_token: Authentication token for repository access.
            Required for private repositories, None for public ones.
        org: Organization or user name that owns the repository.
            Extracted from the repository URL.
        project: Project name within the organization.
            Usually the repository name without the organization.
        branch: Git branch being tracked for updates.
            Defaults to "main" if not specified.
        last_commit_id: SHA hash of the latest processed commit.
            Used to detect when updates are needed.
        tags: List of tags assigned to categorize the library.
            Used for filtering and organizing libraries.
    """

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
    }

    library_id: str = Field(..., description="Unique identifier for the library")
    status: str = Field(
        ..., alias="state", description="Current processing status of the library"
    )

    # Repository-specific fields
    repo_url: str | None = Field(
        None, alias="repoUrl", description="URL of the source Git repository"
    )
    access_token: str | None = Field(
        None,
        alias="accessToken",
        description="Authentication token for repository access",
    )
    org: str | None = Field(
        None, description="Organization or user name that owns the repository"
    )
    project: str | None = Field(
        None, description="Project name within the organization"
    )
    branch: str | None = Field(None, description="Git branch being tracked for updates")
    last_commit_id: str | None = Field(
        None,
        alias="lastCommitId",
        description="SHA hash of the latest processed commit",
    )

    # Tag management
    tags: list[str] = Field(
        default_factory=list,
        description="List of tags assigned to categorize the library",
    )
