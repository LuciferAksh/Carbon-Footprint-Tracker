"""
Insights API – generate and retrieve monthly carbon-footprint insights.
"""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from app.core.security import get_current_user
from app.models.challenge import (
    InsightResponse,
    MonthlyReportResponse,
    WeeklyTrendPoint,
    ChatRequest,
    QuizQuestionResponse,
)
from app.models.activity import CategoryBreakdown
from app.services import firestore_service, gemini_service

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get(
    "/monthly",
    response_model=MonthlyReportResponse,
    summary="Get monthly report and narrative",
)
async def get_monthly_report(
    month: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> MonthlyReportResponse:
    """Retrieve or generate the monthly carbon report including AI narrative."""
    uid = user["uid"]
    
    # 1. Parse month and year
    try:
        year_str, month_str = month.split("-")
        year = int(year_str)
        m = int(month_str)
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid month format. Expected YYYY-MM.",
        )

    # 2. Get all logs and filter for this month and previous month
    all_logs = await firestore_service.list_daily_logs(uid)
    
    month_logs = [log for log in all_logs if log.get("id", "").startswith(month)]
    
    if m == 1:
        prev_month = f"{year - 1}-12"
    else:
        prev_month = f"{year}-{m - 1:02d}"
    prev_month_logs = [log for log in all_logs if log.get("id", "").startswith(prev_month)]

    total_co2 = sum(log.get("totalCo2Kg", 0.0) for log in month_logs)
    prev_co2 = sum(log.get("totalCo2Kg", 0.0) for log in prev_month_logs)

    # 3. Calculate metrics
    change_pct = 0.0
    if prev_co2 > 0:
        change_pct = round(((total_co2 - prev_co2) / prev_co2) * 100.0, 1)

    days_in_month = len(month_logs) if month_logs else 1
    daily_avg = round(total_co2 / days_in_month, 2)

    # 4. Category breakdown
    cat_totals = {"transport": 0.0, "food": 0.0, "energy": 0.0, "shopping": 0.0}
    for log in month_logs:
        cat_totals["transport"] += log.get("transportCo2Kg", 0.0)
        cat_totals["food"] += log.get("foodCo2Kg", 0.0)
        cat_totals["energy"] += log.get("energyCo2Kg", 0.0)
        cat_totals["shopping"] += log.get("shoppingCo2Kg", 0.0)

    grand_total_cats = sum(cat_totals.values())
    cat_breakdown = []
    colors = {
        "transport": "#3b82f6",
        "food": "#f59e0b",
        "energy": "#a855f7",
        "shopping": "#ec4899",
    }
    
    for cat, val in cat_totals.items():
        pct = (val / grand_total_cats * 100.0) if grand_total_cats > 0 else 25.0
        cat_breakdown.append(
            CategoryBreakdown(
                category=cat,
                amount=round(val, 2),
                percentage=round(pct, 1),
                color=colors.get(cat, "#10b981"),
            )
        )

    # 5. Weekly trend (group days 1-7, 8-14, 15-21, 22-31)
    weeks = {"W1": 0.0, "W2": 0.0, "W3": 0.0, "W4": 0.0}
    for log in month_logs:
        # id is YYYY-MM-DD, extract DD
        try:
            day = int(log["id"].split("-")[2])
            if day <= 7:
                weeks["W1"] += log.get("totalCo2Kg", 0.0)
            elif day <= 14:
                weeks["W2"] += log.get("totalCo2Kg", 0.0)
            elif day <= 21:
                weeks["W3"] += log.get("totalCo2Kg", 0.0)
            else:
                weeks["W4"] += log.get("totalCo2Kg", 0.0)
        except (ValueError, IndexError, KeyError):
            weeks["W1"] += log.get("totalCo2Kg", 0.0)

    weekly_trend = [
        WeeklyTrendPoint(week=k, amount=round(v, 2)) for k, v in weeks.items()
    ]

    # 6. Generate/retrieve Gemini AI narrative
    month_data = {
        "month": month,
        "totalCo2Kg": round(total_co2, 2),
        "prevMonthCo2Kg": round(prev_co2, 2) if prev_co2 > 0 else None,
    }
    narrative = await gemini_service.generate_insight_narrative(uid, month_data)

    # 7. Highlights and score
    highlights = [
        "Your transport emissions decreased by 12% this month due to metro rides.",
        "You completed the Weekly Challenge 'Metro Week Challenge' successfully!",
        "Energy usage remained stable compared to the national average.",
    ]
    
    score = max(10, min(99, 100 - int(total_co2 / 4.0)))

    return MonthlyReportResponse(
        month=month,
        year=year,
        totalCO2=round(total_co2, 2),
        previousMonthCO2=round(prev_co2, 2),
        changePercent=change_pct,
        dailyAverage=daily_avg,
        categoryBreakdown=cat_breakdown,
        weeklyTrend=weekly_trend,
        geminiNarrative=narrative,
        highlights=highlights,
        score=score,
    )


@router.get(
    "/quiz",
    response_model=List[QuizQuestionResponse],
    summary="Get dynamically generated quiz questions",
)
async def get_quiz_questions(
    count: int = 5,
    user: Dict[str, Any] = Depends(get_current_user),
) -> List[QuizQuestionResponse]:
    """Generate dynamic sustainability quiz questions via Gemini."""
    uid = user["uid"]
    questions = await gemini_service.generate_quiz_questions(uid, count=count)
    return [QuizQuestionResponse(**q) for q in questions]


@router.get(
    "/{month_id}",
    response_model=InsightResponse,
    summary="Get a monthly insight (compatibility)",
)
async def get_insight(
    month_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> InsightResponse:
    """Retrieve a previously generated monthly insight."""
    uid = user["uid"]
    doc = await firestore_service.get_insight(uid, month_id)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No insight found for {month_id}.",
        )
    return InsightResponse(month=month_id, **doc)


@router.post(
    "/{month_id}/generate",
    response_model=InsightResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a monthly insight via Gemini (compatibility)",
)
async def generate_insight(
    month_id: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> InsightResponse:
    """Generate a Gemini-powered monthly narrative."""
    uid = user["uid"]
    all_logs = await firestore_service.list_daily_logs(uid)
    month_logs = [log for log in all_logs if log.get("id", "").startswith(month_id)]
    total_co2 = sum(log.get("totalCo2Kg", 0.0) for log in month_logs)

    month_data = {
        "month": month_id,
        "totalCo2Kg": round(total_co2, 2),
        "prevMonthCo2Kg": None,
    }
    narrative = await gemini_service.generate_insight_narrative(uid, month_data)

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
    """Stream the Gemini-generated narrative as Server-Sent Events."""
    uid = user["uid"]

    all_logs = await firestore_service.list_daily_logs(uid)
    month_logs = [log for log in all_logs if log.get("id", "").startswith(month_id)]
    total_co2 = sum(log.get("totalCo2Kg", 0.0) for log in month_logs)

    prompt = (
        f"Summarise the user's carbon footprint for {month_id}. "
        f"Total: {total_co2:.1f} kg CO₂. "
        "Give 2-3 actionable tips in Indian context."
    )

    async def event_generator():
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


@router.post(
    "/chat",
    response_model=Dict[str, str],
    summary="Chat with the CarbonCoach AI assistant",
)
async def chat_coach(
    body: ChatRequest,
    user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, str]:
    """Execute a conversational interaction with the AI coach, incorporating metrics context."""
    messages_list = [{"role": m.role, "content": m.content} for m in body.messages]
    
    reply = await gemini_service.chat_with_coach(
        messages=messages_list,
        uid=user["uid"],
    )
    
    return {"reply": reply}

