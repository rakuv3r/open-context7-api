"""GitLab adapter for repository access and library processing."""

import shutil
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import git
import gitlab
from loguru import logger
from starlette.concurrency import run_in_threadpool

from src.core.config import settings
from src.core.constants import DEFAULT_LIBRARY_TAG
from src.core.constants import GITLAB_API_TIMEOUT
from src.core.errors import ValidationError
from src.utils.common import md5_hash


class GitLabAdapter:
    """GitLab repository adapter for library extraction."""

    def __init__(self, url: str, token: str, org: str, project: str):
        """Initialize GitLab adapter for project.

        Args:
            url: GitLab repository URL or GitLab instance base URL.
            token: Personal access token for GitLab API.
            org: Organization.
            project: Project name.
        """
        self.url = url
        # Extract GitLab base URL for API calls
        parsed = urlparse(url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.token = token
        self.org = org
        self.project = project
        self.branch = settings.GIT_DEFAULT_BRANCH
        self.tag = DEFAULT_LIBRARY_TAG  # Default tag, can be set to specific tag
        self._project_info: dict[str, str] = {}

    @property
    def name(self) -> str:
        """Get readable name for this repository."""
        return f"/{self.org}/{self.project}"

    @property
    def id(self) -> str:
        """Get unique identifier for this repository."""
        return md5_hash(self.name)

    @property
    def title(self) -> str:
        """Get repository title."""
        return self._project_info.get("title", "Unknown")

    @property
    def description(self) -> str:
        """Get repository description."""
        return self._project_info.get("description", "No description")

    async def validate_access(self) -> bool:
        """Validate GitLab repository access.

        Returns:
            True if access is valid, False otherwise.
        """
        return await run_in_threadpool(self._validate_access)

    def _validate_access(self) -> bool:
        """GitLab access validation and project info cache."""
        try:
            gitlab_client = gitlab.Gitlab(
                self.base_url, private_token=self.token, timeout=GITLAB_API_TIMEOUT
            )
            # Get full project info (remove lazy=True)
            project = gitlab_client.projects.get(f"{self.org}/{self.project}")

            # Cache project metadata
            self._project_info = {
                "title": project.name or self.project,
                "description": project.description or f"Documentation for {self.name}",
            }
            return True
        except Exception as e:
            logger.error(f"Cannot access GitLab /{self.org}/{self.project}: {e}")
            return False

    async def collect_files(self) -> dict[str, str]:
        """Collect all Markdown files from GitLab repo.

        Returns:
            Dict with file paths as keys and contents as values.

        Raises:
            Exception: If repo access or clone fails.
        """
        return await run_in_threadpool(self._collect_files)

    def _collect_files(self) -> dict[str, str]:
        """Collect files from repository.

        Clones the repository and extracts all markdown files.

        Returns:
            Dict with file URLs as keys and contents as values.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / f"{self.org}_{self.project}"
            self._clone_repository(str(temp_path))
            return self._build_file_mapping(str(temp_path))

    def _clone_repository(self, local_path: str) -> None:
        """Clone GitLab repo to local directory.

        Args:
            local_path: Local directory path to clone to.

        Raises:
            Exception: If clone fails.
        """
        parsed = urlparse(self.url)
        clone_url = f"{parsed.scheme}://oauth2:{self.token}@{parsed.netloc}/{self.org}/{self.project}.git"

        if Path(local_path).exists():
            shutil.rmtree(local_path)

        repo = git.Repo.clone_from(clone_url, local_path)

        # If tag is not latest, checkout the specific tag
        if self.tag != DEFAULT_LIBRARY_TAG:
            try:
                repo.git.checkout(self.tag)
                logger.info(f"Checked out tag {self.tag}")
            except Exception as e:
                logger.error(f"Failed to checkout tag {self.tag}: {e}")
                raise

    def _build_file_mapping(self, local_path: str) -> dict[str, str]:
        """Build file mapping from local directory.

        Args:
            local_path: Local directory path to scan.

        Returns:
            Dict with GitLab URLs as keys and contents as values.
        """
        files: dict[str, str] = {}
        path_obj = Path(local_path)

        for md_file in path_obj.rglob("*.md"):
            try:
                relative_path = md_file.relative_to(path_obj)
                content = md_file.read_text(encoding="utf-8")

                # Create GitLab blob URL using the correct ref
                ref_name = (
                    self.tag
                    if self.tag != DEFAULT_LIBRARY_TAG
                    else settings.GIT_DEFAULT_BRANCH
                )
                file_url = f"{self.url}/blob/{ref_name}/{relative_path}"
                files[file_url] = content
            except Exception as e:
                logger.warning(f"Failed to read {md_file}: {e}")

        return files

    async def build_payload(self) -> dict[str, Any]:
        """Build payload for storage based on GitLab repo info.

        Returns:
            Provider-specific payload data including repo metadata.
        """
        return {
            "repo_url": self.url,
            "org": self.org,
            "project": self.project,
            "branch": self.branch,
            "tag": self.tag,
            "access_token": self.token,
            "last_commit_id": await self.get_latest_commit_id(),
        }

    async def get_latest_commit_id(self) -> str | None:
        """Get latest commit ID from repo.

        Returns:
            Latest commit ID string, or None if it can't be fetched.
        """
        return await run_in_threadpool(self._get_latest_commit_id)

    def _get_latest_commit_id(self) -> str | None:
        """Fetch latest commit ID from GitLab API."""
        try:
            gitlab_client = gitlab.Gitlab(
                self.base_url, private_token=self.token, timeout=GITLAB_API_TIMEOUT
            )
            gitlab_project = gitlab_client.projects.get(
                f"{self.org}/{self.project}", lazy=True
            )

            # Get latest commit from the branch
            commits = gitlab_project.commits.list(ref_name=self.branch, per_page=1)
            if commits:
                return commits[0].id
            return None
        except Exception as e:
            logger.error(
                f"Failed to get latest commit for GitLab /{self.org}/{self.project}: "
                f"{e}"
            )
            return None

    async def get_tags(self) -> list[str]:
        """Get all tags for GitLab repo.

        Returns:
            List of tags sorted in reverse order.
        """
        return await run_in_threadpool(self._get_tags)

    def _get_tags(self) -> list[str]:
        """Get all tags from repository.

        Fetches all tags from GitLab API and sorts them.

        Returns:
            List of tag names sorted in reverse order (newest first).
        """
        try:
            gitlab_client = gitlab.Gitlab(
                self.base_url, private_token=self.token, timeout=GITLAB_API_TIMEOUT
            )
            # Use lazy loading to avoid loading full project details
            gitlab_project = gitlab_client.projects.get(
                f"{self.org}/{self.project}", lazy=True
            )

            # Get tags directly
            tags = gitlab_project.tags.list(all=True)

            # Sort tag names in reverse order (latest first)
            return sorted([tag.name for tag in tags], reverse=True)
        except Exception as e:
            logger.error(
                f"Failed to get tags for GitLab /{self.org}/{self.project}: {e}"
            )
            return []

    @classmethod
    def from_library(
        cls,
        library: Any,  # LibraryDetail - avoid circular import
        tag: str | None = None,
    ) -> "GitLabAdapter":
        """Create GitLab adapter from library.

        Args:
            library: Library details with repo information.
            tag: Optional tag to set on the adapter.

        Returns:
            GitLabAdapter configured for the specified library and tag.

        Raises:
            ValidationError: If required repo info is missing.
        """
        if not all(
            [library.repo_url, library.access_token, library.org, library.project]
        ):
            raise ValidationError("Missing required repository information")

        # Fields are validated above, safe to use
        adapter = cls(
            url=library.repo_url,
            token=library.access_token,
            org=library.org,
            project=library.project,
        )
        if tag:
            adapter.tag = tag
        return adapter
