"""
Profile API – onboarding and user profile management.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.profile import ProfileCreate, ProfileResponse, OnboardingAnswers, CarbonProfile
from app.services import firestore_service

router = APIRouter(tags=["profile"])


@router.get(
    "/users/me",
    response_model=ProfileResponse,
    summary="Get current user's profile",
)
async def get_profile(
    user: Dict[str, Any] = Depends(get_current_user),
) -> ProfileResponse:
    """Retrieve the authenticated user's profile."""
    uid = user["uid"]
    doc = await firestore_service.get_profile(uid)
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please onboarding first.",
        )

    # ── Calculate dynamic streak and badges ──
    logs = await firestore_service.list_daily_logs(uid)
    logs_dict = {log.get("id"): log for log in logs if log.get("id")}
    
    streak = 0
    today_str = date.today().isoformat()
    check_day = date.today()
    
    if today_str not in logs_dict:
        check_day = date.today() - timedelta(days=1)
        
    while check_day.isoformat() in logs_dict:
        streak += 1
        check_day -= timedelta(days=1)
        
    badges = []
    challenges = await firestore_service.list_challenges(uid)
    
    # 1. first-log: at least 1 log exists
    if len(logs) >= 1:
        badges.append("first-log")
        
    # 2. week-streak: streak >= 7
    if streak >= 7:
        badges.append("week-streak")
        
    # 3. challenge-1: at least 1 completed challenge
    if any(c.get("status") == "completed" for c in challenges):
        badges.append("challenge-1")
        
    # 4. green-commute: Took public transport 10 times (bus, train, or metro)
    public_transport_count = 0
    for log in logs:
        for entry in log.get("transport", []):
            if entry.get("mode") in {"bus", "train", "metro"}:
                public_transport_count += 1
    if public_transport_count >= 10:
        badges.append("green-commute")
        
    # 5. vegan-week: Logged at least 7 vegan meals in total
    vegan_meal_count = 0
    for log in logs:
        for entry in log.get("food", []):
            if entry.get("mealType") == "vegan_meal":
                vegan_meal_count += entry.get("quantity", 1)
    if vegan_meal_count >= 7:
        badges.append("vegan-week")
        
    # 6. carbon-a: Carbon Score is A or A+ (>= 80)
    carbon_score = 75
    if doc.get("carbonProfile"):
        carbon_score = doc["carbonProfile"].get("carbonScore", 75)
    else:
        total_week_co2 = sum(log.get("totalCo2Kg", 0.0) for log in logs[:7])
        carbon_score = max(10, min(99, 100 - int(total_week_co2 * 1.5)))
        
    if carbon_score >= 80:
        badges.append("carbon-a")

    # Ensure defaults exist so ProfileResponse validates correctly
    return ProfileResponse(
        uid=uid,
        name=doc.get("name") or doc.get("displayName") or user.get("name") or "User",
        displayName=doc.get("displayName") or user.get("name") or "User",
        email=doc.get("email") or user.get("email"),
        photoURL=doc.get("photoURL") or user.get("picture"),
        onboardingComplete=doc.get("onboardingComplete", False),
        carbonProfileType=doc.get("carbonProfileType", "general"),
        estimatedAnnualKg=doc.get("estimatedAnnualKg", 0.0),
        topCategories=doc.get("topCategories", []),
        createdAt=doc.get("createdAt"),
        onboardingAnswers=doc.get("onboardingAnswers"),
        carbonProfile=doc.get("carbonProfile"),
        streak=streak,
        badges=badges,
    )


@router.post(
    "/onboarding",
    response_model=CarbonProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Submit onboarding quiz answers",
)
async def upsert_onboarding(
    body: OnboardingAnswers,
    user: Dict[str, Any] = Depends(get_current_user),
) -> CarbonProfile:
    """Submit onboarding answers and calculate carbon footprint profile."""
    uid = user["uid"]

    # ── Calculation Logic ──
    # 1. Transport emissions (weekly)
    transport_factors = {
        "car_petrol": 0.21,
        "car_ev": 0.05,
        "bus": 0.089,
        "train": 0.041,
        "motorbike": 0.114,
    }
    t_factor = transport_factors.get(body.primaryTransport, 0.11)
    transport_weekly = 150.0 * t_factor  # assume 150km / week average

    # 2. Food emissions (weekly)
    food_factors = {
        "beef_meal": 6.0,
        "chicken_meal": 1.5,
        "fish_meal": 1.2,
        "vegetarian_meal": 0.7,
        "vegan_meal": 0.4,
    }
    f_factor = food_factors.get(body.dietType, 0.7)
    food_weekly = 21.0 * f_factor  # 21 meals / week

    # 3. Energy emissions (weekly)
    energy_factors = {
        "india_grid": 0.82,
        "renewable": 0.02,
    }
    e_factor = energy_factors.get(body.energySource, 0.82)
    energy_weekly = (50.0 / max(1, body.householdSize)) * e_factor  # 50 kWh average

    # 4. Shopping emissions (weekly)
    shopping_factors = {
        "low": 0.4,
        "medium": 1.6,
        "high": 4.0,
    }
    shopping_weekly = shopping_factors.get(body.shoppingFrequency, 1.6)

    # 5. Grand Totals
    weekly_est = round(transport_weekly + food_weekly + energy_weekly + shopping_weekly, 2)
    monthly_est = round(weekly_est * 4.0, 2)
    yearly_est = round(weekly_est * 52.0, 2)
    national_avg = 2500.0

    percentile = max(5.0, min(95.0, round((yearly_est / 3000.0) * 100.0)))
    carbon_score = max(10, min(99, 100 - int(yearly_est / 60.0)))

    # Determine top category
    categories = {
        "transport": transport_weekly,
        "food": food_weekly,
        "energy": energy_weekly,
        "shopping": shopping_weekly,
    }
    top_cat = max(categories, key=lambda k: categories[k])

    recommendations_map = {
        "transport": [
            "Consider carpooling or using public transit (metro/bus) for commutes.",
            "Combine errands to reduce driving time.",
            "Maintain proper tire inflation to improve fuel efficiency.",
        ],
        "food": [
            "Adopt one meatless day per week (like Meatless Monday).",
            "Reduce food waste by planning meals and freezing leftovers.",
            "Source seasonal and locally grown produce where possible.",
        ],
        "energy": [
            "Unplug idle electronics to prevent standby power drain.",
            "Upgrade lighting to energy-efficient LED bulbs.",
            "Set air conditioning to 24°C or higher for optimal efficiency.",
        ],
        "shopping": [
            "Adopt a 'one-in, one-out' rule for buying new items.",
            "Consider renting or buying pre-owned for rare-use items.",
            "Focus budget on experiences rather than physical goods.",
        ],
    }
    recs = recommendations_map.get(top_cat, recommendations_map["transport"])

    carbon_profile = CarbonProfile(
        weeklyEstimate=weekly_est,
        monthlyEstimate=monthly_est,
        yearlyEstimate=yearly_est,
        nationalAverage=national_avg,
        percentile=percentile,
        topCategory=top_cat,
        recommendations=recs,
        carbonScore=carbon_score,
    )

    # 6. Save User Profile in Firestore
    profile_data = {
        "name": user.get("name") or "User",
        "displayName": user.get("name") or "User",
        "email": user.get("email"),
        "photoURL": user.get("picture"),
        "onboardingComplete": True,
        "carbonProfileType": "urban-commuter" if top_cat == "transport" else "general",
        "estimatedAnnualKg": yearly_est,
        "topCategories": [top_cat],
        "onboardingAnswers": body.model_dump(),
        "carbonProfile": carbon_profile.model_dump(),
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    await firestore_service.upsert_profile(uid, profile_data)

    return carbon_profile


# Compatibility endpoint for original tests
@router.post(
    "/profile",
    response_model=ProfileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Compatibility endpoint for creating/updating a profile",
)
async def upsert_profile(
    body: ProfileCreate,
    user: Dict[str, Any] = Depends(get_current_user),
) -> ProfileResponse:
    uid = user["uid"]
    data = body.model_dump()
    # Check if profile already has fields
    merged = await firestore_service.upsert_profile(uid, data)
    return ProfileResponse(
        uid=uid,
        name=merged.get("name") or user.get("name"),
        displayName=merged.get("displayName") or user.get("name"),
        email=merged.get("email") or user.get("email"),
        photoURL=merged.get("photoURL"),
        onboardingComplete=merged.get("onboardingComplete", False),
        carbonProfileType=merged.get("carbonProfileType", "general"),
        estimatedAnnualKg=merged.get("estimatedAnnualKg", 0.0),
        topCategories=merged.get("topCategories", []),
        createdAt=merged.get("createdAt"),
    )


@router.get(
    "/profile",
    response_model=ProfileResponse,
    summary="Compatibility endpoint for getting profile",
)
async def get_profile_compatibility(
    user: Dict[str, Any] = Depends(get_current_user),
) -> ProfileResponse:
    return await get_profile(user)
