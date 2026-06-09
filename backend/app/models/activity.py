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
