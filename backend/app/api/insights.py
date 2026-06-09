"""
Insights API – generate and retrieve monthly carbon-footprint insights.

The ``/generate`` endpoint triggers a Gemini call (or returns a cached
result).  The ``/stream`` endpoint returns a Server-Sent Events stream
so the frontend can display the narrative progressively.
"""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.security import get_current_user
from app.models.challenge import InsightResponse
from app.services import firestore_service, gemini_service

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get(
    "/{month_id}",
    response_model=InsightResponse,
    summary="Get a monthly insight",
)
async def get_insight(
    month_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> InsightResponse:
    """Retrieve a previously generated monthly insight.

    Args:
        month_id: Month in ``YYYY-MM`` format.
        user: Decoded Firebase token.

    Returns:
        ``InsightResponse`` if found.

    Raises:
        HTTPException: 404 if no insight exists yet for this month.
    """
    uid = user["uid"]
    doc = await firestore_service.get_insight(uid, month_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"No insight found for {month_id}. "
                "Use POST /insights/{month_id}/generate to create one."
            ),
        )
    return InsightResponse(month=month_id, **doc)


@router.post(
    "/{month_id}/generate",
    response_model=InsightResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a monthly insight via Gemini",
)
async def generate_insight(
    month_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> InsightResponse:
    """Generate (or return cached) a Gemini-powered monthly narrative.

    The endpoint aggregates the user's daily logs for the requested
    month, passes the totals to Gemini, and stores the result.

    Args:
        month_id: ``YYYY-MM``.
        user: Decoded Firebase token.

    Returns:
        ``InsightResponse`` containing the AI narrative.
    """
    uid = user["uid"]

    # ── Aggregate daily logs for the month ──
    all_logs = await firestore_service.list_daily_logs(uid)
    month_logs = [
        log for log in all_logs
        if log.get("id", "").startswith(month_id)
    ]

    total_co2 = sum(log.get("totalCo2Kg", 0) for log in month_logs)

    # ── Try to get previous month's total ──
    prev_month_co2 = None
    try:
        year, month = month_id.split("-")
        m = int(month)
        y = int(year)
        if m == 1:
            prev_id = f"{y - 1}-12"
        else:
            prev_id = f"{y}-{m - 1:02d}"
        prev_insight = await firestore_service.get_insight(uid, prev_id)
        if prev_insight:
            prev_month_co2 = prev_insight.get("totalCo2Kg")
    except (ValueError, IndexError):
        pass

    month_data = {
        "month": month_id,
        "totalCo2Kg": round(total_co2, 2),
        "prevMonthCo2Kg": prev_month_co2,
    }

    narrative = await gemini_service.generate_insight_narrative(
        uid, month_data
    )

    # Re-fetch the saved insight for a clean response
    doc = await firestore_service.get_insight(uid, month_id)
    if doc is None:
        doc = {**month_data, "narrative": narrative}

    return InsightResponse(month=month_id, **doc)


@router.get(
    "/{month_id}/stream",
    summary="Stream a monthly insight via SSE",
)
async def stream_insight(
    month_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> StreamingResponse:
    """Stream the Gemini-generated narrative as Server-Sent Events.

    This allows the frontend to display the AI response progressively
    as tokens arrive.

    Args:
        month_id: ``YYYY-MM``.
        user: Decoded Firebase token.

    Returns:
        ``StreamingResponse`` with ``text/event-stream`` content type.
    """
    uid = user["uid"]

    # Build the same prompt as the non-streaming endpoint
    all_logs = await firestore_service.list_daily_logs(uid)
    month_logs = [
        log for log in all_logs
        if log.get("id", "").startswith(month_id)
    ]
    total_co2 = sum(log.get("totalCo2Kg", 0) for log in month_logs)

    prompt = (
        f"Summarise the user's carbon footprint for {month_id}. "
        f"Total: {total_co2:.1f} kg CO₂. "
        "Give 2-3 actionable tips in Indian context."
    )

    async def event_generator():
        """Yield SSE-formatted chunks."""
        async for chunk in gemini_service.generate_text_stream(prompt, uid):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
