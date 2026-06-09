"""
Per-user rate limiter for Gemini API calls.

Enforces a minimum interval of ``RATE_LIMIT_SECONDS`` between consecutive
Gemini calls **per user**.  Uses an in-memory dict (sufficient for a
single-process deployment).  For multi-process setups swap the store for
Redis.
"""

from __future__ import annotations

import logging
import time
from typing import Dict

from fastapi import Depends, HTTPException, status

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

# uid → timestamp of last allowed Gemini call
_last_call: Dict[str, float] = {}


def check_rate_limit(
    uid: str,
    settings: Settings | None = None,
) -> None:
    """Raise ``429 Too Many Requests`` if the user is calling too fast.

    Args:
        uid: Firebase UID of the caller.
        settings: Optional settings override (resolved via DI when *None*).

    Raises:
        HTTPException: 429 when the user's last call was less than
            ``RATE_LIMIT_SECONDS`` ago.
    """
    if settings is None:
        settings = get_settings()

    now = time.time()
    last = _last_call.get(uid, 0.0)
    elapsed = now - last

    if elapsed < settings.RATE_LIMIT_SECONDS:
        wait = round(settings.RATE_LIMIT_SECONDS - elapsed, 1)
        logger.info(
            "Rate-limited user %s – retry in %.1f s", uid, wait
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Rate limit exceeded. Please wait {wait} seconds "
                f"before the next Gemini call."
            ),
        )

    _last_call[uid] = now


def reset_rate_limit(uid: str) -> None:
    """Remove the rate-limit record for *uid* (useful in tests).

    Args:
        uid: Firebase UID whose record should be cleared.
    """
    _last_call.pop(uid, None)


def clear_all_rate_limits() -> None:
    """Wipe every rate-limit record (test-only helper)."""
    _last_call.clear()
