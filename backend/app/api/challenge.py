"""
Challenge API – create, list, and manage weekly challenges.

Includes an AI-powered suggestion endpoint that asks Gemini for a
personalised challenge.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.challenge import (
    ChallengeCreate,
    ChallengeResponse,
    ChallengeStatusUpdate,
)
from app.services import firestore_service, gemini_service

router = APIRouter(prefix="/challenges", tags=["challenges"])


def _current_week_id() -> str:
    """Return the current ISO week as ``YYYY-WNN``."""
    today = date.today()
    return f"{today.isocalendar().year}-W{today.isocalendar().week:02d}"


@router.post(
    "",
    response_model=ChallengeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a weekly challenge",
)
async def create_challenge(
    body: ChallengeCreate,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ChallengeResponse:
    """Create a new weekly challenge for the current ISO week.

    Args:
        body: Validated challenge payload.
        user: Decoded Firebase token.

    Returns:
        ``ChallengeResponse`` with the created challenge details.
    """
    uid = user["uid"]
    challenge_id = _current_week_id()
    data = {**body.model_dump(), "status": "active"}
    await firestore_service.save_challenge(uid, challenge_id, data)
    return ChallengeResponse(id=challenge_id, **data)


@router.get(
    "",
    response_model=List[ChallengeResponse],
    summary="List all challenges",
)
async def list_challenges(
    user: Dict[str, Any] = Depends(get_current_user),
) -> List[ChallengeResponse]:
    """Return every challenge for the authenticated user.

    Args:
        user: Decoded Firebase token.

    Returns:
        List of ``ChallengeResponse`` objects.
    """
    uid = user["uid"]
    docs = await firestore_service.list_challenges(uid)
    return [
        ChallengeResponse(
            id=d.get("id", "unknown"),
            title=d.get("title", ""),
            description=d.get("description", ""),
            category=d.get("category", ""),
            targetMetric=d.get("targetMetric", ""),
            co2SavingKg=d.get("co2SavingKg", 0),
            status=d.get("status", "active"),
        )
        for d in docs
    ]


@router.get(
    "/{challenge_id}",
    response_model=ChallengeResponse,
    summary="Get a specific challenge",
)
async def get_challenge(
    challenge_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ChallengeResponse:
    """Retrieve a single challenge by its ID.

    Args:
        challenge_id: ``YYYY-WNN`` identifier.
        user: Decoded Firebase token.

    Returns:
        ``ChallengeResponse``.

    Raises:
        HTTPException: 404 if not found.
    """
    uid = user["uid"]
    doc = await firestore_service.get_challenge(uid, challenge_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge {challenge_id} not found.",
        )
    return ChallengeResponse(id=challenge_id, **doc)


@router.patch(
    "/{challenge_id}/status",
    response_model=ChallengeResponse,
    summary="Update challenge status",
)
async def update_status(
    challenge_id: str,
    body: ChallengeStatusUpdate,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ChallengeResponse:
    """Change a challenge's status (e.g. ``active`` → ``completed``).

    Args:
        challenge_id: ``YYYY-WNN`` identifier.
        body: New status value.
        user: Decoded Firebase token.

    Returns:
        Updated ``ChallengeResponse``.

    Raises:
        HTTPException: 404 if not found.
    """
    uid = user["uid"]
    doc = await firestore_service.get_challenge(uid, challenge_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge {challenge_id} not found.",
        )
    await firestore_service.update_challenge_status(
        uid, challenge_id, body.status
    )
    doc["status"] = body.status
    return ChallengeResponse(id=challenge_id, **doc)


@router.post(
    "/suggest/{category}",
    response_model=ChallengeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="AI-suggested weekly challenge",
)
async def suggest_challenge(
    category: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ChallengeResponse:
    """Ask Gemini to suggest a challenge for *category* and save it.

    The challenge is automatically persisted for the current ISO week.

    Args:
        category: One of ``transport``, ``food``, ``energy``, ``shopping``.
        user: Decoded Firebase token.

    Returns:
        ``ChallengeResponse`` with the AI-suggested challenge.
    """
    valid_categories = {"transport", "food", "energy", "shopping"}
    if category not in valid_categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category '{category}'. Choose from {valid_categories}.",
        )

    uid = user["uid"]
    suggestion = await gemini_service.generate_challenge_suggestion(
        uid, category
    )

    challenge_id = _current_week_id()
    data = {
        "title": suggestion.get("title", "Weekly Challenge"),
        "description": suggestion.get("description", ""),
        "category": category,
        "targetMetric": suggestion.get("targetMetric", ""),
        "co2SavingKg": float(suggestion.get("co2SavingKg", 0)),
        "status": "active",
    }
    await firestore_service.save_challenge(uid, challenge_id, data)
    return ChallengeResponse(id=challenge_id, **data)
