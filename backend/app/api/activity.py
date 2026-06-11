"""
Activity API – log daily emissions and retrieve history.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import Settings, get_settings
from app.core.security import get_current_user
from app.models.activity import (
    ActivityLog,
    ActivityLogResponse,
    DashboardData,
    WeeklyDataPoint,
    CategoryBreakdown,
    DashboardBenchmark,
    ParseTextRequest,
    CommunityAnalyticsPoint,
    CommunityAnalyticsResponse,
)
from app.services import carbon_calculator, firestore_service, gemini_service

router = APIRouter(prefix="/activity", tags=["activity"])


@router.post(
    "",
    response_model=ActivityLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a day's carbon activities (compatibility)",
)
async def log_activity(
    body: ActivityLog,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ActivityLogResponse:
    """Calculate emissions for the submitted activities and save them."""
    uid = user["uid"]
    date_str = body.date or date.today().isoformat()

    # Calculate emissions
    result = carbon_calculator.calc_daily_total(
        transport=body.transport,
        food=body.food,
        energy=body.energy,
        shopping=body.shopping,
    )

    # Persist
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


@router.post(
    "/log",
    response_model=ActivityLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log a day's carbon activities",
)
async def log_activity_new(
    body: ActivityLog,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ActivityLogResponse:
    """Forward to ``log_activity`` for compatibility with the ``/log`` endpoint."""
    return await log_activity(body, user)


@router.get(
    "/summary",
    response_model=DashboardData,
    summary="Get weekly/monthly emissions summary",
)
async def get_summary(
    period: str = "week",
    user: Dict[str, Any] = Depends(get_current_user),
) -> DashboardData:
    """Return dashboard summary data including today/weekly/monthly stats."""
    uid = user["uid"]
    logs = await firestore_service.list_daily_logs(uid)

    # Convert logs list to dict for fast lookup by date_str
    logs_dict = {log.get("id"): log for log in logs if log.get("id")}

    today_str = date.today().isoformat()
    today_log = logs_dict.get(today_str, {})
    total_today = today_log.get("totalCo2Kg", 0.0)

    # Calculate weekly and monthly totals
    total_week = 0.0
    total_month = 0.0
    
    # Category totals for breakdown (past 30 days)
    cat_totals = {"transport": 0.0, "food": 0.0, "energy": 0.0, "shopping": 0.0}

    for i in range(30):
        check_date = (date.today() - timedelta(days=i)).isoformat()
        log = logs_dict.get(check_date, {})
        tot = log.get("totalCo2Kg", 0.0)
        if i < 7:
            total_week += tot
        total_month += tot
        
        cat_totals["transport"] += log.get("transportCo2Kg", 0.0)
        cat_totals["food"] += log.get("foodCo2Kg", 0.0)
        cat_totals["energy"] += log.get("energyCo2Kg", 0.0)
        cat_totals["shopping"] += log.get("shoppingCo2Kg", 0.0)

    # Calculate weekly comparison (this week vs last week daily trend)
    weekly_comp = []
    days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # We want to return the last 7 days of comparison
    for i in range(6, -1, -1):
        dt = date.today() - timedelta(days=i)
        day_name = days_of_week[dt.weekday()]
        
        this_week_date = dt.isoformat()
        last_week_date = (dt - timedelta(days=7)).isoformat()
        
        this_week_val = logs_dict.get(this_week_date, {}).get("totalCo2Kg", 0.0)
        last_week_val = logs_dict.get(last_week_date, {}).get("totalCo2Kg", 0.0)
        
        weekly_comp.append(
            WeeklyDataPoint(
                day=day_name,
                thisWeek=round(this_week_val, 2),
                lastWeek=round(last_week_val, 2),
            )
        )

    # Calculate category breakdown
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

    # Calculate streak (consecutive days of logging)
    streak = 0
    check_day = date.today()
    
    # If today hasn't been logged, start checking from yesterday
    if today_str not in logs_dict:
        check_day = date.today() - timedelta(days=1)
        
    while check_day.isoformat() in logs_dict:
        streak += 1
        check_day -= timedelta(days=1)

    # Get carbon score from user profile or calculate fallback
    profile = await firestore_service.get_profile(uid)
    carbon_score = 75
    if profile and profile.get("carbonProfile"):
        carbon_score = profile["carbonProfile"].get("carbonScore", 75)
    else:
        # Fallback dynamic calculation
        carbon_score = max(10, min(99, 100 - int(total_week * 1.5)))

    # Set up benchmarks
    annual_user = (total_week / 7.0) * 365.0 if total_week > 0 else 2100.0
    benchmark = DashboardBenchmark(
        user=round(annual_user, 1),
        national=2500.0,
        target=1500.0,
    )

    return DashboardData(
        totalCO2Today=round(total_today, 2),
        totalCO2Week=round(total_week, 2),
        totalCO2Month=round(total_month, 2),
        weeklyComparison=weekly_comp,
        categoryBreakdown=cat_breakdown,
        streak=streak,
        carbonScore=carbon_score,
        benchmark=benchmark,
    )


@router.get(
    "/analytics",
    response_model=CommunityAnalyticsResponse,
    summary="Get paginated community analytics from BigQuery",
)
async def get_community_analytics(
    page: int = 1,
    size: int = 10,
    category: str | None = None,
    user: Dict[str, Any] = Depends(get_current_user),
    settings: Settings = Depends(get_settings),
) -> CommunityAnalyticsResponse:
    """Query paginated community carbon aggregates from BigQuery (or return mock data)."""
    offset = (page - 1) * size
    
    # 1. Mock mode fallback
    if settings.is_mock:
        categories = ["transport", "food", "energy", "shopping"]
        mock_data = []
        for i in range(20):
            wk = f"2026-W{24-i:02d}"
            for cat in categories:
                if category and cat != category:
                    continue
                mock_data.append(
                    CommunityAnalyticsPoint(
                        category=cat,
                        avg_co2_kg=round(10.5 - (i * 0.1), 2),
                        median_co2_kg=round(9.8 - (i * 0.12), 2),
                        p20_co2_kg=round(5.4 - (i * 0.05), 2),
                        p80_co2_kg=round(15.2 - (i * 0.2), 2),
                        total_users=142 + (i * 3),
                        week=wk,
                    )
                )
        
        total = len(mock_data)
        paginated_results = mock_data[offset : offset + size]
        return CommunityAnalyticsResponse(
            page=page,
            size=size,
            total=total,
            results=paginated_results,
        )

    # 2. Production BigQuery query
    from google.cloud import bigquery
    client = bigquery.Client(project=settings.GCP_PROJECT_ID)
    
    query = f"""
        SELECT category, avg_co2_kg, median_co2_kg, p20_co2_kg, p80_co2_kg, total_users, CAST(week AS STRING) as week
        FROM `{settings.GCP_PROJECT_ID}.carboncoach_analytics.community_aggregates_view`
    """
    
    where_clauses = []
    params = []
    
    if category:
        where_clauses.append("category = @category")
        params.append(bigquery.ScalarQueryParameter("category", "STRING", category))
        
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
        
    query += " ORDER BY week DESC, category LIMIT @limit OFFSET @offset"
    params.append(bigquery.ScalarQueryParameter("limit", "INT64", size))
    params.append(bigquery.ScalarQueryParameter("offset", "INT64", offset))
    
    job_config = bigquery.QueryJobConfig(query_parameters=params)
    query_job = client.query(query, job_config=job_config)
    rows = query_job.result()
    
    results = []
    for row in rows:
        results.append(
            CommunityAnalyticsPoint(
                category=row.category,
                avg_co2_kg=round(row.avg_co2_kg, 2),
                median_co2_kg=round(row.median_co2_kg, 2),
                p20_co2_kg=round(row.p20_co2_kg, 2),
                p80_co2_kg=round(row.p80_co2_kg, 2),
                total_users=row.total_users,
                week=row.week,
            )
        )
        
    count_query = f"SELECT COUNT(*) as cnt FROM `{settings.GCP_PROJECT_ID}.carboncoach_analytics.community_aggregates_view`"
    if where_clauses:
        count_query += " WHERE " + " AND ".join(where_clauses)
        
    count_job_config = bigquery.QueryJobConfig(query_parameters=[p for p in params if p.name == "category"])
    count_job = client.query(count_query, job_config=count_job_config)
    count_result = list(count_job.result())
    total = count_result[0].cnt if count_result else 0
    
    return CommunityAnalyticsResponse(
        page=page,
        size=size,
        total=total,
        results=results,
    )


@router.get(
    "/{date_str}",
    response_model=ActivityLogResponse,
    summary="Get a single day's activity log",
)
async def get_activity(
    date_str: str,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ActivityLogResponse:
    """Retrieve an existing daily log by date."""
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
    """Return every daily activity log for the authenticated user."""
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


@router.post(
    "/parse-text",
    response_model=ActivityLog,
    summary="Parse plain text into structured daily activities",
)
async def parse_text_log(
    body: ParseTextRequest,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ActivityLog:
    """Parse conversational input using Gemini and return structured log entries."""
    parsed = await gemini_service.parse_conversational_log(
        text=body.text,
        uid=user["uid"],
    )
    return ActivityLog(**parsed)


