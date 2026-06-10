"""
Firestore service – all database operations in one place.

When ``MOCK_AI=true`` every method returns deterministic in-memory data
so that no real Firestore connection is required.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

# ── In-memory mock store ──────────────────────────────
_mock_store: Dict[str, Dict[str, Any]] = {}

# Simple cache store for Firestore document reads: (collection_path, doc_id) -> (timestamp, data_dict)
_cache: Dict[str, tuple[float, Optional[Dict[str, Any]]]] = {}
_list_cache: Dict[str, tuple[float, List[Dict[str, Any]]]] = {}
_CACHE_TTL_SECONDS = 60.0  # Cache profiles/documents/lists for 60 seconds


def _mock_path(parts: List[str]) -> str:
    """Join Firestore-style path segments into a flat key."""
    return "/".join(parts)


# ── Lazy Firestore client ────────────────────────────
_firestore_client = None


def _get_client(settings: Settings):
    """Return (or create) a Firestore client.  Skipped in mock mode."""
    global _firestore_client
    if settings.is_mock:
        return None

    if _firestore_client is None:
        from google.cloud import firestore  # noqa: WPS433

        _firestore_client = firestore.Client(project=settings.GCP_PROJECT_ID)
    return _firestore_client


# ──────────────────────────────────────────────────────
# Generic CRUD helpers
# ──────────────────────────────────────────────────────


async def set_document(
    collection_path: str,
    doc_id: str,
    data: Dict[str, Any],
    merge: bool = True,
    settings: Settings | None = None,
) -> None:
    """Create or update a Firestore document.

    Args:
        collection_path: Slash-delimited path to the collection
            (e.g. ``"users"`` or ``"users/uid123/logs"``).
        doc_id: Document ID.
        data: Fields to write.
        merge: If *True*, only provided fields are updated.
        settings: App settings (injected or resolved).
    """
    settings = settings or get_settings()
    
    # Invalidate cache on write
    cache_key = f"{collection_path}/{doc_id}"
    _cache.pop(cache_key, None)
    _list_cache.pop(collection_path, None)

    if settings.is_mock:
        key = _mock_path([collection_path, doc_id])
        existing = _mock_store.get(key, {})
        if merge:
            existing.update(data)
        else:
            existing = data
        _mock_store[key] = existing
        logger.debug("MOCK set_document %s → %s", key, existing)
        return

    client = _get_client(settings)
    ref = client.document(f"{collection_path}/{doc_id}")
    ref.set(data, merge=merge)


async def get_document(
    collection_path: str,
    doc_id: str,
    settings: Settings | None = None,
) -> Optional[Dict[str, Any]]:
    """Fetch a single Firestore document.

    Args:
        collection_path: Collection path.
        doc_id: Document ID.
        settings: App settings.

    Returns:
        Document data dict, or ``None`` if not found.
    """
    settings = settings or get_settings()

    cache_key = f"{collection_path}/{doc_id}"
    now = time.time()
    if cache_key in _cache:
        cached_time, cached_val = _cache[cache_key]
        if now - cached_time < _CACHE_TTL_SECONDS:
            logger.debug("CACHE hit for %s", cache_key)
            return cached_val

    if settings.is_mock:
        key = _mock_path([collection_path, doc_id])
        doc = _mock_store.get(key)
        logger.debug("MOCK get_document %s → %s", key, doc)
        _cache[cache_key] = (now, doc)
        return doc

    client = _get_client(settings)
    snap = client.document(f"{collection_path}/{doc_id}").get()
    doc = snap.to_dict() if snap.exists else None
    _cache[cache_key] = (now, doc)
    return doc


async def list_documents(
    collection_path: str,
    settings: Settings | None = None,
) -> List[Dict[str, Any]]:
    """List all documents in a collection.

    Args:
        collection_path: Collection path.
        settings: App settings.

    Returns:
        List of dicts, each containing the doc data plus an ``id`` key.
    """
    settings = settings or get_settings()

    now = time.time()
    if collection_path in _list_cache:
        cached_time, cached_val = _list_cache[collection_path]
        if now - cached_time < _CACHE_TTL_SECONDS:
            logger.debug("CACHE hit for list: %s", collection_path)
            return cached_val

    if settings.is_mock:
        prefix = collection_path + "/"
        results = []
        for key, val in _mock_store.items():
            if key.startswith(prefix):
                doc_id = key[len(prefix):]
                # Only include direct children (no sub-collections)
                if "/" not in doc_id:
                    results.append({"id": doc_id, **val})
        _list_cache[collection_path] = (now, results)
        return results

    client = _get_client(settings)
    docs = client.collection(collection_path).stream()
    results = [{"id": d.id, **d.to_dict()} for d in docs]
    _list_cache[collection_path] = (now, results)
    return results


async def delete_document(
    collection_path: str,
    doc_id: str,
    settings: Settings | None = None,
) -> None:
    """Delete a Firestore document.

    Args:
        collection_path: Collection path.
        doc_id: Document ID.
        settings: App settings.
    """
    settings = settings or get_settings()

    cache_key = f"{collection_path}/{doc_id}"
    _cache.pop(cache_key, None)
    _list_cache.pop(collection_path, None)

    if settings.is_mock:
        key = _mock_path([collection_path, doc_id])
        _mock_store.pop(key, None)
        logger.debug("MOCK delete_document %s", key)
        return

    client = _get_client(settings)
    client.document(f"{collection_path}/{doc_id}").delete()


# ──────────────────────────────────────────────────────
# Profile helpers
# ──────────────────────────────────────────────────────


async def upsert_profile(uid: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create or update a user's profile document.

    Adds ``createdAt`` on first write.

    Args:
        uid: Firebase user ID.
        data: Profile fields.

    Returns:
        The merged profile dict.
    """
    existing = await get_document("users", uid)
    if existing is None:
        data["createdAt"] = datetime.now(timezone.utc).isoformat()
    await set_document("users", uid, data, merge=True)
    return {**(existing or {}), **data}


async def get_profile(uid: str) -> Optional[Dict[str, Any]]:
    """Retrieve a user's profile.

    Args:
        uid: Firebase user ID.

    Returns:
        Profile dict or ``None``.
    """
    return await get_document("users", uid)


# ──────────────────────────────────────────────────────
# Activity-log helpers
# ──────────────────────────────────────────────────────


async def save_daily_log(
    uid: str, date_str: str, data: Dict[str, Any]
) -> None:
    """Persist a daily activity log.

    Args:
        uid: Firebase UID.
        date_str: ``YYYY-MM-DD``.
        data: Computed emissions data.
    """
    await set_document(f"users/{uid}/logs", date_str, data, merge=False)


async def get_daily_log(
    uid: str, date_str: str
) -> Optional[Dict[str, Any]]:
    """Fetch a single day's log.

    Args:
        uid: Firebase UID.
        date_str: ``YYYY-MM-DD``.

    Returns:
        Log data or ``None``.
    """
    return await get_document(f"users/{uid}/logs", date_str)


async def list_daily_logs(uid: str) -> List[Dict[str, Any]]:
    """List all daily logs for a user.

    Args:
        uid: Firebase UID.

    Returns:
        List of log dicts.
    """
    return await list_documents(f"users/{uid}/logs")


# ──────────────────────────────────────────────────────
# Challenge helpers
# ──────────────────────────────────────────────────────


async def save_challenge(
    uid: str, challenge_id: str, data: Dict[str, Any]
) -> None:
    """Persist a weekly challenge.

    Args:
        uid: Firebase UID.
        challenge_id: ``YYYY-WW`` format.
        data: Challenge data.
    """
    await set_document(
        f"users/{uid}/challenges", challenge_id, data, merge=False
    )


async def get_challenge(
    uid: str, challenge_id: str
) -> Optional[Dict[str, Any]]:
    """Fetch a single challenge.

    Args:
        uid: Firebase UID.
        challenge_id: ``YYYY-WW``.

    Returns:
        Challenge dict or ``None``.
    """
    return await get_document(f"users/{uid}/challenges", challenge_id)


async def list_challenges(uid: str) -> List[Dict[str, Any]]:
    """List all challenges for a user.

    Args:
        uid: Firebase UID.

    Returns:
        List of challenge dicts.
    """
    return await list_documents(f"users/{uid}/challenges")


async def update_challenge_status(
    uid: str, challenge_id: str, status: str
) -> None:
    """Update only the ``status`` field of a challenge.

    Args:
        uid: Firebase UID.
        challenge_id: ``YYYY-WW``.
        status: New status value.
    """
    await set_document(
        f"users/{uid}/challenges",
        challenge_id,
        {"status": status},
        merge=True,
    )


# ──────────────────────────────────────────────────────
# Insight helpers
# ──────────────────────────────────────────────────────


async def save_insight(
    uid: str, month_id: str, data: Dict[str, Any]
) -> None:
    """Persist a monthly insight.

    Args:
        uid: Firebase UID.
        month_id: ``YYYY-MM``.
        data: Insight data.
    """
    await set_document(
        f"users/{uid}/insights", month_id, data, merge=False
    )


async def get_insight(
    uid: str, month_id: str
) -> Optional[Dict[str, Any]]:
    """Fetch a monthly insight.

    Args:
        uid: Firebase UID.
        month_id: ``YYYY-MM``.

    Returns:
        Insight dict or ``None``.
    """
    return await get_document(f"users/{uid}/insights", month_id)


# ──────────────────────────────────────────────────────
# Test utilities
# ──────────────────────────────────────────────────────


def clear_mock_store() -> None:
    """Wipe the in-memory mock store (test-only)."""
    _mock_store.clear()
    _cache.clear()
    _list_cache.clear()
