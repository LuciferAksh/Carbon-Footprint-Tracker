"""
Lightweight in-memory vector search.

Stores embeddings alongside metadata and supports cosine-similarity
nearest-neighbour queries.  In production you would swap this for
Vertex AI Vector Search or a dedicated store; this module is enough for
prototyping and tests.
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.services.embedding_service import embed_text

logger = logging.getLogger(__name__)


@dataclass
class VectorRecord:
    """A single record in the vector store.

    Attributes:
        id: Unique identifier.
        vector: Embedding vector.
        metadata: Arbitrary metadata dict.
    """

    id: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


# ── Global in-memory index ────────────────────────────
_index: List[VectorRecord] = []


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors.

    Args:
        a: First vector.
        b: Second vector.

    Returns:
        Cosine similarity in ``[-1, 1]``.
    """
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ──────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────


async def upsert(
    record_id: str,
    text: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    """Embed *text* and upsert it into the in-memory index.

    Args:
        record_id: Unique key for the record.
        text: Text to embed.
        metadata: Optional metadata to store alongside the vector.
    """
    vector = await embed_text(text)
    # Remove existing record with same id
    global _index
    _index = [r for r in _index if r.id != record_id]
    _index.append(VectorRecord(id=record_id, vector=vector, metadata=metadata or {}))
    logger.debug("Upserted vector record '%s' (dim=%d)", record_id, len(vector))


async def search(
    query: str,
    top_k: int = 5,
) -> List[Dict[str, Any]]:
    """Find the *top_k* most similar records to *query*.

    Args:
        query: Natural-language query string.
        top_k: Number of results to return.

    Returns:
        List of dicts with ``id``, ``score``, and ``metadata`` keys,
        sorted by descending similarity.
    """
    if not _index:
        return []

    query_vec = await embed_text(query)
    scored: List[Dict[str, Any]] = [
        {"id": r.id, "score": _cosine_similarity(query_vec, r.vector), "metadata": r.metadata}
        for r in _index
    ]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def clear_index() -> None:
    """Remove all records from the in-memory index (test helper)."""
    _index.clear()
