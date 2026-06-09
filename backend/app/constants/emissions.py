"""
Carbon-emission factor constants.

Every factor is expressed in **kg CO₂e per unit** (km, meal, kWh, or ₹1 000).
Sources: DEFRA 2023, CEA India 2023, academic meta-analyses.

Usage::

    from app.constants.emissions import TRANSPORT, FOOD

    co2 = distance_km * TRANSPORT["car_petrol"]
"""

from __future__ import annotations

from typing import Dict

# ---------- Transport (kg CO₂e per km) ----------
TRANSPORT: Dict[str, float] = {
    "car_petrol": 0.21,
    "car_ev": 0.05,
    "bus": 0.089,
    "train": 0.041,
    "motorbike": 0.114,
    "flight_short": 0.255,
    "flight_long": 0.195,
}

# ---------- Food (kg CO₂e per meal) ----------
FOOD: Dict[str, float] = {
    "beef_meal": 6.0,
    "chicken_meal": 1.5,
    "fish_meal": 1.2,
    "vegetarian_meal": 0.7,
    "vegan_meal": 0.4,
}

# ---------- Energy (kg CO₂e per kWh) ----------
ENERGY: Dict[str, float] = {
    "india_grid": 0.82,
    "renewable": 0.02,
}

# ---------- Shopping (kg CO₂e per ₹1 000 spent) ----------
SHOPPING: Dict[str, float] = {
    "clothing": 0.4,
    "electronics": 0.8,
    "groceries": 0.2,
    "other": 0.3,
}

# ---------- Aggregate lookup for dynamic access ----------
ALL_FACTORS: Dict[str, Dict[str, float]] = {
    "transport": TRANSPORT,
    "food": FOOD,
    "energy": ENERGY,
    "shopping": SHOPPING,
}
