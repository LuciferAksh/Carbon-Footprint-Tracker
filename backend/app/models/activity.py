"""
Pydantic v2 models for daily activity logging.

Covers all four emission categories: transport, food, energy, shopping.
Each sub-model maps directly to one section of the daily log document
stored in Firestore at ``users/{uid}/logs/{YYYY-MM-DD}``.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────
# Sub-models (one per category)
# ──────────────────────────────────────────────────────


class TransportEntry(BaseModel):
    """A single transport activity.

    Attributes:
        mode: Key matching ``constants.emissions.TRANSPORT``.
        distanceKm: Distance travelled in kilometres.
    """

    mode: str = Field(
        ...,
        description="Transport mode key (e.g. car_petrol, bus, train)",
        json_schema_extra={"examples": ["car_petrol"]},
    )
    distanceKm: float = Field(
        ...,
        gt=0,
        description="Distance in km",
        json_schema_extra={"examples": [25.0]},
    )


class FoodEntry(BaseModel):
    """A single meal entry.

    Attributes:
        mealType: Key matching ``constants.emissions.FOOD``.
        quantity: Number of meals of this type.
    """

    mealType: str = Field(
        ...,
        description="Meal type key (e.g. chicken_meal, vegan_meal)",
        json_schema_extra={"examples": ["chicken_meal"]},
    )
    quantity: int = Field(
        default=1,
        ge=1,
        description="Number of meals",
        json_schema_extra={"examples": [2]},
    )


class EnergyEntry(BaseModel):
    """A single energy-usage entry.

    Attributes:
        source: Key matching ``constants.emissions.ENERGY``.
        kWh: Energy consumed in kilowatt-hours.
    """

    source: str = Field(
        ...,
        description="Energy source key (india_grid or renewable)",
        json_schema_extra={"examples": ["india_grid"]},
    )
    kWh: float = Field(
        ...,
        gt=0,
        description="Energy consumed in kWh",
        json_schema_extra={"examples": [8.5]},
    )


class ShoppingEntry(BaseModel):
    """A single shopping entry.

    Attributes:
        category: Key matching ``constants.emissions.SHOPPING``.
        amountInr: Amount spent in Indian Rupees (₹).
    """

    category: str = Field(
        ...,
        description="Shopping category key (clothing, electronics, …)",
        json_schema_extra={"examples": ["electronics"]},
    )
    amountInr: float = Field(
        ...,
        gt=0,
        description="Amount spent in ₹",
        json_schema_extra={"examples": [5000.0]},
    )


# ──────────────────────────────────────────────────────
# Top-level request / response models
# ──────────────────────────────────────────────────────


class ActivityLog(BaseModel):
    """Request body for logging a day's carbon activities.

    All four categories are optional — the user can submit whichever
    categories they tracked today.

    Attributes:
        date: ISO date string ``YYYY-MM-DD`` (auto-filled to today on
            the server if omitted).
        transport: List of transport activities.
        food: List of meals.
        energy: List of energy usage entries.
        shopping: List of shopping entries.
    """

    date: Optional[str] = Field(
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Date in YYYY-MM-DD format (defaults to today)",
        json_schema_extra={"examples": ["2026-06-08"]},
    )
    transport: List[TransportEntry] = Field(default_factory=list)
    food: List[FoodEntry] = Field(default_factory=list)
    energy: List[EnergyEntry] = Field(default_factory=list)
    shopping: List[ShoppingEntry] = Field(default_factory=list)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "date": "2026-06-08",
                    "transport": [
                        {"mode": "car_petrol", "distanceKm": 25.0}
                    ],
                    "food": [
                        {"mealType": "chicken_meal", "quantity": 2},
                        {"mealType": "vegan_meal", "quantity": 1},
                    ],
                    "energy": [{"source": "india_grid", "kWh": 8.5}],
                    "shopping": [
                        {"category": "electronics", "amountInr": 5000.0}
                    ],
                }
            ]
        }
    }


class ActivityLogResponse(BaseModel):
    """Response after successfully recording a daily activity log.

    Attributes:
        date: The date the log was recorded for.
        transportCo2Kg: Total transport emissions for the day.
        foodCo2Kg: Total food emissions.
        energyCo2Kg: Total energy emissions.
        shoppingCo2Kg: Total shopping emissions.
        totalCo2Kg: Grand total for the day.
    """

    date: str = Field(..., description="Log date (YYYY-MM-DD)")
    transportCo2Kg: float = Field(default=0.0)
    foodCo2Kg: float = Field(default=0.0)
    energyCo2Kg: float = Field(default=0.0)
    shoppingCo2Kg: float = Field(default=0.0)
    totalCo2Kg: float = Field(default=0.0)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "date": "2026-06-08",
                    "transportCo2Kg": 5.25,
                    "foodCo2Kg": 3.4,
                    "energyCo2Kg": 6.97,
                    "shoppingCo2Kg": 4.0,
                    "totalCo2Kg": 19.62,
                }
            ]
        }
    }


class WeeklyDataPoint(BaseModel):
    """A single data point comparing emissions between two weeks.

    Attributes:
        day: Abbreviated day name (e.g. ``Mon``, ``Tue``).
        thisWeek: CO\u2082 emissions for the day in the current week (kg).
        lastWeek: CO\u2082 emissions for the same day in the previous week (kg).
    """

    day: str = Field(..., description="Abbreviated day name")
    thisWeek: float = Field(..., description="Current week CO\u2082 (kg)")
    lastWeek: float = Field(..., description="Previous week CO\u2082 (kg)")


class CategoryBreakdown(BaseModel):
    """Emission breakdown for a single activity category.

    Attributes:
        category: Category key (``transport``, ``food``, ``energy``, ``shopping``).
        amount: Total CO\u2082 for this category (kg).
        percentage: Share of total emissions (0\u2013100).
        color: Hex colour code for chart rendering.
    """

    category: str = Field(..., description="Category key")
    amount: float = Field(..., description="Total CO\u2082 in kg")
    percentage: float = Field(..., description="Percentage of total")
    color: str = Field(..., description="Chart hex colour")


class DashboardBenchmark(BaseModel):
    """Annualised CO\u2082 benchmarks for the dashboard comparison chart.

    Attributes:
        user: User's projected annual emissions (kg).
        national: Indian national average annual emissions (kg).
        target: Recommended sustainability target (kg).
    """

    user: float = Field(..., description="User annual CO\u2082 (kg)")
    national: float = Field(..., description="National average annual CO\u2082 (kg)")
    target: float = Field(..., description="Sustainability target (kg)")


class DashboardData(BaseModel):
    """Aggregate dashboard payload returned by ``GET /activity/summary``.

    Attributes:
        totalCO2Today: Emissions for today (kg).
        totalCO2Week: Emissions for the last 7 days (kg).
        totalCO2Month: Emissions for the last 30 days (kg).
        weeklyComparison: Daily this-week vs last-week data points.
        categoryBreakdown: Per-category totals and percentages.
        streak: Consecutive days with logged activities.
        carbonScore: User's overall carbon score (0\u2013100).
        benchmark: Annualised benchmark comparison.
    """

    totalCO2Today: float = Field(..., description="Today's CO\u2082 (kg)")
    totalCO2Week: float = Field(..., description="Last 7 days CO\u2082 (kg)")
    totalCO2Month: float = Field(..., description="Last 30 days CO\u2082 (kg)")
    weeklyComparison: List[WeeklyDataPoint] = Field(..., description="Daily comparison data")
    categoryBreakdown: List[CategoryBreakdown] = Field(..., description="Per-category breakdown")
    streak: int = Field(..., description="Consecutive logging days")
    carbonScore: int = Field(..., description="Carbon score 0\u2013100")
    benchmark: DashboardBenchmark = Field(..., description="Annualised benchmarks")


class ParseTextRequest(BaseModel):
    """Request body for natural-language activity parsing via Gemini.

    Attributes:
        text: Free-form description of daily carbon activities.
    """

    text: str = Field(..., description="Free-form activity description")

    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "I drove my petrol car for 12 km and ate a chicken sandwich"}]
        }
    }


class CommunityAnalyticsPoint(BaseModel):
    """A single aggregated community analytics row from BigQuery.

    Attributes:
        category: Emission category (transport, food, energy, shopping).
        avg_co2_kg: Average weekly CO\u2082 across all users (kg).
        median_co2_kg: Median weekly CO\u2082 (kg).
        p20_co2_kg: 20th-percentile weekly CO\u2082 (kg).
        p80_co2_kg: 80th-percentile weekly CO\u2082 (kg).
        total_users: Number of users contributing to this data point.
        week: ISO week identifier (e.g. ``2026-W24``).
    """

    category: str = Field(..., description="Emission category")
    avg_co2_kg: float = Field(..., description="Average CO\u2082 (kg)")
    median_co2_kg: float = Field(..., description="Median CO\u2082 (kg)")
    p20_co2_kg: float = Field(..., description="20th percentile CO\u2082 (kg)")
    p80_co2_kg: float = Field(..., description="80th percentile CO\u2082 (kg)")
    total_users: int = Field(..., description="Number of contributing users")
    week: str = Field(..., description="ISO week identifier")


class CommunityAnalyticsResponse(BaseModel):
    """Paginated response for community analytics queries.

    Attributes:
        page: Current page number (1-indexed).
        size: Number of results per page.
        total: Total number of matching records.
        results: List of analytics data points for this page.
    """

    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Results per page")
    total: int = Field(..., description="Total record count")
    results: List[CommunityAnalyticsPoint] = Field(..., description="Analytics data points")

