"""
Pure-function carbon emission calculator.

Every public function in this module is **pure** (no side-effects, no I/O)
and computes CO₂e in **kg** for a given activity category.  This makes
unit-testing trivial.
"""

from __future__ import annotations

import logging
from typing import List

from app.constants.emissions import ENERGY, FOOD, SHOPPING, TRANSPORT
from app.models.activity import (
    EnergyEntry,
    FoodEntry,
    ShoppingEntry,
    TransportEntry,
)

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────
# Transport
# ──────────────────────────────────────────────────────


def calc_transport(entries: List[TransportEntry]) -> float:
    """Calculate total CO₂ for a list of transport entries.

    Args:
        entries: List of ``TransportEntry`` with ``mode`` and ``distanceKm``.

    Returns:
        Total kg CO₂e.  Unknown modes are logged and skipped.

    Examples:
        >>> calc_transport([TransportEntry(mode="car_petrol", distanceKm=10)])
        2.1
    """
    total = 0.0
    for e in entries:
        factor = TRANSPORT.get(e.mode)
        if factor is None:
            logger.warning("Unknown transport mode '%s' – skipped.", e.mode)
            continue
        total += e.distanceKm * factor
    return round(total, 4)


# ──────────────────────────────────────────────────────
# Food
# ──────────────────────────────────────────────────────


def calc_food(entries: List[FoodEntry]) -> float:
    """Calculate total CO₂ for a list of food entries.

    Args:
        entries: List of ``FoodEntry`` with ``mealType`` and ``quantity``.

    Returns:
        Total kg CO₂e.

    Examples:
        >>> calc_food([FoodEntry(mealType="vegan_meal", quantity=3)])
        1.2
    """
    total = 0.0
    for e in entries:
        factor = FOOD.get(e.mealType)
        if factor is None:
            logger.warning("Unknown meal type '%s' – skipped.", e.mealType)
            continue
        total += e.quantity * factor
    return round(total, 4)


# ──────────────────────────────────────────────────────
# Energy
# ──────────────────────────────────────────────────────


def calc_energy(entries: List[EnergyEntry]) -> float:
    """Calculate total CO₂ for energy-usage entries.

    Args:
        entries: List of ``EnergyEntry`` with ``source`` and ``kWh``.

    Returns:
        Total kg CO₂e.

    Examples:
        >>> calc_energy([EnergyEntry(source="india_grid", kWh=10)])
        8.2
    """
    total = 0.0
    for e in entries:
        factor = ENERGY.get(e.source)
        if factor is None:
            logger.warning("Unknown energy source '%s' – skipped.", e.source)
            continue
        total += e.kWh * factor
    return round(total, 4)


# ──────────────────────────────────────────────────────
# Shopping
# ──────────────────────────────────────────────────────


def calc_shopping(entries: List[ShoppingEntry]) -> float:
    """Calculate total CO₂ for shopping entries.

    The emission factor is per ₹1 000, so we divide ``amountInr`` by 1 000
    before multiplying.

    Args:
        entries: List of ``ShoppingEntry`` with ``category`` and ``amountInr``.

    Returns:
        Total kg CO₂e.

    Examples:
        >>> calc_shopping([ShoppingEntry(category="electronics", amountInr=5000)])
        4.0
    """
    total = 0.0
    for e in entries:
        factor = SHOPPING.get(e.category)
        if factor is None:
            logger.warning(
                "Unknown shopping category '%s' – skipped.", e.category
            )
            continue
        total += (e.amountInr / 1000.0) * factor
    return round(total, 4)


# ──────────────────────────────────────────────────────
# Grand total convenience helper
# ──────────────────────────────────────────────────────


def calc_daily_total(
    transport: List[TransportEntry],
    food: List[FoodEntry],
    energy: List[EnergyEntry],
    shopping: List[ShoppingEntry],
) -> dict:
    """Calculate per-category and total CO₂ for a full day.

    Args:
        transport: Transport entries for the day.
        food: Food entries for the day.
        energy: Energy entries for the day.
        shopping: Shopping entries for the day.

    Returns:
        Dict with keys ``transportCo2Kg``, ``foodCo2Kg``, ``energyCo2Kg``,
        ``shoppingCo2Kg``, and ``totalCo2Kg``.
    """
    t = calc_transport(transport)
    f = calc_food(food)
    e = calc_energy(energy)
    s = calc_shopping(shopping)
    return {
        "transportCo2Kg": t,
        "foodCo2Kg": f,
        "energyCo2Kg": e,
        "shoppingCo2Kg": s,
        "totalCo2Kg": round(t + f + e + s, 4),
    }
