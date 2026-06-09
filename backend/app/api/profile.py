"""
Profile API – create, read, update user profiles.

All routes require a valid Firebase ID token (or mock mode).
"""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.profile import ProfileCreate, ProfileResponse
from app.services import firestore_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post(
    "",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create or update a user profile",
)
async def upsert_profile(
    body: ProfileCreate,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ProfileResponse:
    """Create a new profile or update an existing one.

    The profile is stored at ``users/{uid}`` in Firestore.  If the
    document already exists the provided fields are merged in.

    Args:
        body: Validated profile payload.
        user: Decoded Firebase token (injected by security middleware).

    Returns:
        The resulting ``ProfileResponse``.
    """
    uid = user["uid"]
    data = body.model_dump()
    merged = await firestore_service.upsert_profile(uid, data)
    return ProfileResponse(uid=uid, **{k: merged.get(k, v) for k, v in data.items()}, createdAt=merged.get("createdAt"))


@router.get(
    "",
    response_model=ProfileResponse,
    summary="Get the current user's profile",
)
async def get_profile(
    user: Dict[str, Any] = Depends(get_current_user),
) -> ProfileResponse:
    """Retrieve the authenticated user's profile.

    Args:
        user: Decoded Firebase token.

    Returns:
        ``ProfileResponse`` if found.

    Raises:
        HTTPException: 404 when no profile exists yet.
    """
    uid = user["uid"]
    doc = await firestore_service.get_profile(uid)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create one first.",
        )
    return ProfileResponse(uid=uid, **doc)
