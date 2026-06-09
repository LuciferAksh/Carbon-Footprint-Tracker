"""
Activity API – log daily emissions and retrieve history.

All routes require a valid Firebase ID token (or mock mode).
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.activity import ActivityLog, ActivityLogResponse
from app.services import carbon_calculator, firestore_service

router = APIRouter(prefix="/activity", tags=["activity"])


@router.post(
    "",
    response_model=ActivityLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a day's carbon activities",
)
async def log_activity(
    body: ActivityLog,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ActivityLogResponse:
    """Calculate emissions for the submitted activities and save them.

    If ``date`` is omitted in the request body it defaults to today
    (server time, UTC).

    Args:
        body: Validated activity log payload.
        user: Decoded Firebase token.

    Returns:
        ``ActivityLogResponse`` containing per-category and total CO₂.
    """
    uid = user["uid"]
    date_str = body.date or date.today().isoformat()

    # ── Calculate emissions ──
    result = carbon_calculator.calc_daily_total(
        transport=body.transport,
        food=body.food,
        energy=body.energy,
        shopping=body.shopping,
    )

    # ── Persist ──
    log_data = {
        "transport": [e.model_dump() for e in body.transport],
        "food": [e.model_dump() for e in body.food],
        "energy": [e.model_dump() for e in body.energy],
        "shopping": [e.model_dump() for e in body.shopping],
        **result,
        "loggedAt": datetime.now(timezone.utc).isoformat(),
    }
    await firestore_service.save_daily_log(uid, date_str, log_data)

    return ActivityLogResponse(date=date_str, **result)


@router.get(
    "/{date_str}",
    response_model=ActivityLogResponse,
    summary="Get a single day's activity log",
)
async def get_activity(
    date_str: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ActivityLogResponse:
    """Retrieve an existing daily log by date.

    Args:
        date_str: Date in ``YYYY-MM-DD`` format.
        user: Decoded Firebase token.

    Returns:
        ``ActivityLogResponse`` for that date.

    Raises:
        HTTPException: 404 if no log exists for the given date.
    """
    uid = user["uid"]
    doc = await firestore_service.get_daily_log(uid, date_str)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No activity log found for {date_str}.",
        )
    return ActivityLogResponse(
        date=date_str,
        transportCo2Kg=doc.get("transportCo2Kg", 0),
        foodCo2Kg=doc.get("foodCo2Kg", 0),
        energyCo2Kg=doc.get("energyCo2Kg", 0),
        shoppingCo2Kg=doc.get("shoppingCo2Kg", 0),
        totalCo2Kg=doc.get("totalCo2Kg", 0),
    )


@router.get(
    "",
    response_model=List[ActivityLogResponse],
    summary="List all activity logs for the user",
)
async def list_activities(
    user: Dict[str, Any] = Depends(get_current_user),
) -> List[ActivityLogResponse]:
    """Return every daily activity log for the authenticated user.

    Args:
        user: Decoded Firebase token.

    Returns:
        List of ``ActivityLogResponse`` objects, one per logged day.
    """
    uid = user["uid"]
    docs = await firestore_service.list_daily_logs(uid)
    return [
        ActivityLogResponse(
            date=d.get("id", "unknown"),
            transportCo2Kg=d.get("transportCo2Kg", 0),
            foodCo2Kg=d.get("foodCo2Kg", 0),
            energyCo2Kg=d.get("energyCo2Kg", 0),
            shoppingCo2Kg=d.get("shoppingCo2Kg", 0),
            totalCo2Kg=d.get("totalCo2Kg", 0),
        )
        for d in docs
    ]
