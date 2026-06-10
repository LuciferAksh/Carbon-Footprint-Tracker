"""
Challenge API – create, list, and manage weekly challenges.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.challenge import (
    ChallengeCreate,
    ChallengeResponse,
)
from app.services import firestore_service, gemini_service

router = APIRouter(prefix="/challenge", tags=["challenges"])


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
    """Create a new weekly challenge for the current ISO week."""
    uid = user["uid"]
    challenge_id = _current_week_id()
    data = {
        **body.model_dump(),
        "status": "active",
        "difficulty": "medium",
        "durationDays": 7,
        "co2SavedTarget": body.co2SavingKg,
        "co2SavedActual": 0.0,
        "progress": 0.0,
        "participants": 124,
        "tips": ["Plan ahead", "Track progress daily"],
    }
    await firestore_service.save_challenge(uid, challenge_id, data)
    return ChallengeResponse(id=challenge_id, **data)


@router.get(
    "/current",
    response_model=ChallengeResponse,
    summary="Get the current week's challenge",
)
async def get_current_challenge(
    user: Dict[str, Any] = Depends(get_current_user),
) -> ChallengeResponse:
    """Retrieve the current week's challenge, creating a default one if none exists."""
    uid = user["uid"]
    challenge_id = _current_week_id()
    doc = await firestore_service.get_challenge(uid, challenge_id)
    
    if doc is None:
        # Create a default active challenge for the user for the current week
        default_challenge = {
            "title": "Green Commuter Week",
            "description": "Take public transit, walk, or carpool for all daily commutes this week.",
            "category": "transport",
            "targetMetric": "4 green commutes",
            "co2SavingKg": 6.5,
            "status": "active",
            "difficulty": "easy",
            "durationDays": 7,
            "co2SavedTarget": 6.5,
            "co2SavedActual": 0.0,
            "progress": 0.0,
            "participants": 154,
            "tips": [
                "Map your local bus or metro routes beforehand.",
                "Carpool with a colleague going the same way.",
                "Walk or cycle for trips under 2 km.",
            ],
        }
        await firestore_service.save_challenge(uid, challenge_id, default_challenge)
        doc = default_challenge

    return ChallengeResponse(id=challenge_id, **doc)


@router.get(
    "/list",
    response_model=List[ChallengeResponse],
    summary="List all challenges",
)
async def list_challenges(
    user: Dict[str, Any] = Depends(get_current_user),
) -> List[ChallengeResponse]:
    """Return every challenge for the authenticated user."""
    uid = user["uid"]
    docs = await firestore_service.list_challenges(uid)
    return [
        ChallengeResponse(
            id=d.get("id", "unknown"),
            title=d.get("title", ""),
            description=d.get("description", ""),
            category=d.get("category", "transport"),
            targetMetric=d.get("targetMetric", ""),
            co2SavingKg=float(d.get("co2SavingKg", 0.0)),
            status=d.get("status", "active"),
            difficulty=d.get("difficulty", "medium"),
            durationDays=int(d.get("durationDays", 7)),
            co2SavedTarget=float(d.get("co2SavedTarget", 5.0)),
            co2SavedActual=float(d.get("co2SavedActual", 0.0)),
            progress=float(d.get("progress", 0.0)),
            participants=int(d.get("participants", 124)),
            tips=d.get("tips", []),
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
    """Retrieve a single challenge by its ID."""
    uid = user["uid"]
    doc = await firestore_service.get_challenge(uid, challenge_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge {challenge_id} not found.",
        )
    return ChallengeResponse(id=challenge_id, **doc)


@router.patch(
    "/{challenge_id}/complete",
    response_model=ChallengeResponse,
    summary="Mark a challenge as completed",
)
async def complete_challenge(
    challenge_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ChallengeResponse:
    """Mark a challenge as completed."""
    uid = user["uid"]
    doc = await firestore_service.get_challenge(uid, challenge_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge {challenge_id} not found.",
        )
    await firestore_service.update_challenge_status(uid, challenge_id, "completed")
    doc["status"] = "completed"
    doc["progress"] = 100.0
    doc["co2SavedActual"] = doc.get("co2SavedTarget", 5.0)
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
    """Ask Gemini to suggest a challenge for *category* and save it."""
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
    co2_saving = float(suggestion.get("co2SavingKg", 5.0))
    data = {
        "title": suggestion.get("title", "Weekly Challenge"),
        "description": suggestion.get("description", ""),
        "category": category,
        "targetMetric": suggestion.get("targetMetric", ""),
        "co2SavingKg": co2_saving,
        "status": "active",
        "difficulty": suggestion.get("difficulty", "medium"),
        "durationDays": int(suggestion.get("durationDays", 7)),
        "co2SavedTarget": co2_saving,
        "co2SavedActual": 0.0,
        "progress": 0.0,
        "participants": 210,
        "tips": suggestion.get("tips") or [
            "Start small and build habits.",
            "Tell a friend to stay accountable.",
        ],
    }
    await firestore_service.save_challenge(uid, challenge_id, data)
    return ChallengeResponse(id=challenge_id, **data)
