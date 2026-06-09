"""
Embedding service – generates text embeddings via Vertex AI or mock.

Used by the vector-search module for semantic similarity lookups.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
from typing import List

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

_embedding_model = None


def _get_embedding_model(settings: Settings):
    """Lazily initialise the Vertex AI text-embedding model."""
    global _embedding_model
    if settings.is_mock or _embedding_model is not None:
        return _embedding_model

    import vertexai  # noqa: WPS433
    from vertexai.language_models import TextEmbeddingModel  # noqa: WPS433

    vertexai.init(
        project=settings.GCP_PROJECT_ID,
        location=settings.GEMINI_LOCATION,
    )
    _embedding_model = TextEmbeddingModel.from_pretrained(
        "text-embedding-004"
    )
    return _embedding_model


def _mock_embedding(text: str, dimensions: int = 256) -> List[float]:
    """Deterministic mock embedding based on a hash of the input text.

    Returns a list of floats with length ``dimensions`` derived from
    the SHA-256 digest so that identical inputs always yield the same
    vector.
    """
    digest = hashlib.sha256(text.encode()).hexdigest()
    # Convert hex pairs to floats in [-1, 1]
    values: List[float] = []
    for i in range(dimensions):
        byte_val = int(digest[(i * 2) % len(digest): (i * 2 + 2) % len(digest) or None], 16)
        values.append((byte_val / 127.5) - 1.0)
    return values


async def embed_text(
    text: str,
    settings: Settings | None = None,
) -> List[float]:
    """Return the embedding vector for *text*.

    Args:
        text: Input string.
        settings: App settings.

    Returns:
        List of floats representing the embedding.
    """
    settings = settings or get_settings()

    if settings.is_mock:
        return _mock_embedding(text)

    model = _get_embedding_model(settings)
    embeddings = await asyncio.to_thread(
        model.get_embeddings, [text]
    )
    return embeddings[0].values


async def embed_texts(
    texts: List[str],
    settings: Settings | None = None,
) -> List[List[float]]:
    """Batch-embed multiple strings.

    Args:
        texts: List of input strings.
        settings: App settings.

    Returns:
        List of embedding vectors (same order as input).
    """
    settings = settings or get_settings()

    if settings.is_mock:
        return [_mock_embedding(t) for t in texts]

    model = _get_embedding_model(settings)
    embeddings = await asyncio.to_thread(model.get_embeddings, texts)
    return [e.values for e in embeddings]
