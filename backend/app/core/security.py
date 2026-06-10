"""
Firebase ID-token verification middleware.

Provides a FastAPI dependency ``get_current_user`` that:
* Extracts the ``Authorization: Bearer <token>`` header.
* Verifies it against Firebase Auth (or returns a mock user when
  ``MOCK_AI=true``).
* Returns the decoded token dict on success or raises ``401``.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

_bearer_scheme = HTTPBearer(auto_error=False)


# ---------- Mock user for local development ----------

_MOCK_USER: Dict[str, Any] = {
    "uid": "mock-user-001",
    "email": "dev@carboncoach.local",
    "name": "Mock Developer",
    "email_verified": True,
}


# ---------- Firebase Admin SDK lazy init ----------

_firebase_app_initialized: bool = False


def _ensure_firebase_initialized(settings: Settings) -> None:
    """Initialise the Firebase Admin SDK exactly once.

    Skipped entirely when mock mode is active.
    """
    global _firebase_app_initialized
    if _firebase_app_initialized or settings.is_mock:
        return

    try:
        import firebase_admin  # noqa: WPS433
        from firebase_admin import credentials  # noqa: WPS433

        if not firebase_admin._apps:  # type: ignore[attr-defined]
            if settings.GOOGLE_APPLICATION_CREDENTIALS:
                cred = credentials.Certificate(
                    settings.GOOGLE_APPLICATION_CREDENTIALS
                )
                firebase_admin.initialize_app(cred)
            else:
                import os
                os.environ["GOOGLE_CLOUD_PROJECT"] = settings.GCP_PROJECT_ID
                firebase_admin.initialize_app(options={"projectId": settings.GCP_PROJECT_ID})

        _firebase_app_initialized = True
        logger.info("Firebase Admin SDK initialised successfully.")
    except Exception as exc:
        logger.error("Firebase Admin SDK init failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Firebase initialisation error.",
        ) from exc


# ---------- Token verification ----------


def _verify_firebase_token(token: str, settings: Settings) -> Dict[str, Any]:
    """Verify a Firebase ID token and return the decoded claims.

    Args:
        token: The raw JWT string from the ``Authorization`` header.
        settings: Application settings (used to check mock mode).

    Returns:
        A dict of decoded token claims (always contains ``uid``).

    Raises:
        HTTPException: 401 if the token is invalid or expired.
    """
    _ensure_firebase_initialized(settings)

    try:
        from firebase_admin import auth  # noqa: WPS433

        decoded = auth.verify_id_token(token)
        return decoded
    except Exception as exc:
        logger.warning("Token verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase ID token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


# ---------- FastAPI dependency ----------


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> Dict[str, Any]:
    """FastAPI dependency that returns the authenticated user's claims.

    In **mock mode** (``MOCK_AI=true``) a deterministic mock user is
    returned without touching Firebase at all, which is handy for local
    development and CI pipelines.

    Args:
        request: The incoming request (unused but available for logging).
        credentials: Parsed ``Authorization: Bearer`` header.
        settings: Injected application settings.

    Returns:
        Decoded Firebase token dict with at least an ``uid`` key.

    Raises:
        HTTPException: 401 when no token is present or verification fails.
    """
    if settings.is_mock:
        logger.debug("Mock mode – returning mock user %s", _MOCK_USER["uid"])
        return _MOCK_USER

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return _verify_firebase_token(credentials.credentials, settings)
