"""AI service response schemas."""

from pydantic import BaseModel


class EmbeddingResult(BaseModel):
    """Result from text embedding generation.

    This class represents the output from AI embedding services,
    containing the vector representation and token usage information.

    Attributes:
        embedding: A list of float values representing the text as a vector.
            Each float is a dimension in the embedding space.
        embedding_tokens: The number of tokens used to generate this embedding.
            This is used for billing and usage tracking.
    """

    embedding: list[float]
    embedding_tokens: int
