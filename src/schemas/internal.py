"""Internal service layer models."""

from typing import Any

from pydantic import BaseModel


class TokenFilterResult(BaseModel):
    """Token filtering result model.

    This class holds the result of filtering documents based on token limits.
    It contains the filtered documents and the total token count for tracking.

    Attributes:
        documents: A list of document dictionaries that passed the token filter.
            Each dictionary contains document metadata and content.
        total_tokens: The total number of tokens across all filtered documents.
            This is used for API limits and billing purposes.
    """

    documents: list[dict[str, Any]]
    total_tokens: int
