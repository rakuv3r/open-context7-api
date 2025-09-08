"""Common utility functions."""

import hashlib
from urllib.parse import urlparse

from src.core.errors import ValidationError


def md5_hash(text: str) -> str:
    """Convert string to MD5 hash value.

    Args:
        text: Input string to hash.

    Returns:
        MD5 hash as hex string.
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()  # noqa


def validate_url_scheme(url: str, allowed_schemes: list[str] | None = None) -> None:
    """Check that URL uses allowed schemes.

    Args:
        url: URL to validate.
        allowed_schemes: List of allowed schemes. Defaults to ['http', 'https'].

    Raises:
        ValueError: If URL scheme is not allowed.

    Examples:
        >>> validate_url_scheme('https://example.com')  # OK
        >>> validate_url_scheme('ftp://example.com')    # Raises ValueError
    """
    if allowed_schemes is None:
        allowed_schemes = ["http", "https"]

    parsed = urlparse(url)
    if parsed.scheme not in allowed_schemes:
        schemes_str = ", ".join(allowed_schemes)
        raise ValueError(f"URL must use one of these schemes: {schemes_str}")


def parse_repo_url(url: str) -> tuple[str, str]:
    """Parse repo URL to get org and project names.

    Supports HTTP/HTTPS URLs for GitHub, GitLab, and other Git hosts.
    Works with or without .git suffix.

    Args:
        url: Repository URL to parse (HTTP/HTTPS only).

    Returns:
        Tuple of (org, project) names from URL.

    Raises:
        ValueError: If URL format is invalid or missing parts.

    Examples:
        >>> parse_repo_url('https://github.com/org/project')
        ('org', 'project')
        >>> parse_repo_url('https://gitlab.com/group/project.git')
        ('group', 'project')
    """
    validate_url_scheme(url)

    parsed = urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]

    if len(parts) < 2:
        raise ValueError("Invalid repository URL format")

    org, project = parts[-2], parts[-1]
    project = project.removesuffix(".git")

    if not org or not project:
        raise ValueError("Organization and project names cannot be empty")

    return org, project


def validate_non_empty_string(v: str) -> str:
    """Check field is not empty.

    Args:
        v: String value to validate.

    Returns:
        Stripped string value.

    Raises:
        ValidationError: If string is empty or whitespace only.
    """
    if not v or not v.strip():
        raise ValidationError("Field cannot be empty or whitespace")
    return v.strip()
