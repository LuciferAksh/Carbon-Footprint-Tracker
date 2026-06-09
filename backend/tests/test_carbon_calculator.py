"""
Unit tests for the pure-function carbon calculator.

These tests do not require any network access, mock mode, or fixtures
beyond the standard pytest runner.
"""

from __future__ import annotations

import pytest

from app.models.activity import (
    EnergyEntry,
    FoodEntry,
    ShoppingEntry,
    TransportEntry,
)
from app.services.carbon_calculator import (
    calc_daily_total,
    calc_energy,
    calc_food,
    calc_shopping,
    calc_transport,
)


# ──────────────────────────────────────────────────────
# Transport
# ──────────────────────────────────────────────────────


class TestCalcTransport:
    """Tests for ``calc_transport``."""

    def test_car_petrol(self):
        """10 km by petrol car → 10 × 0.21 = 2.1 kg."""
        entries = [TransportEntry(mode="car_petrol", distanceKm=10)]
        assert calc_transport(entries) == pytest.approx(2.1)

    def test_car_ev(self):
        """50 km by EV → 50 × 0.05 = 2.5 kg."""
        entries = [TransportEntry(mode="car_ev", distanceKm=50)]
        assert calc_transport(entries) == pytest.approx(2.5)

    def test_bus(self):
        """20 km by bus → 20 × 0.089 = 1.78 kg."""
        entries = [TransportEntry(mode="bus", distanceKm=20)]
        assert calc_transport(entries) == pytest.approx(1.78)

    def test_train(self):
        """100 km by train → 100 × 0.041 = 4.1 kg."""
        entries = [TransportEntry(mode="train", distanceKm=100)]
        assert calc_transport(entries) == pytest.approx(4.1)

    def test_motorbike(self):
        """30 km by motorbike → 30 × 0.114 = 3.42 kg."""
        entries = [TransportEntry(mode="motorbike", distanceKm=30)]
        assert calc_transport(entries) == pytest.approx(3.42)

    def test_flight_short(self):
        """500 km short flight → 500 × 0.255 = 127.5 kg."""
        entries = [TransportEntry(mode="flight_short", distanceKm=500)]
        assert calc_transport(entries) == pytest.approx(127.5)

    def test_flight_long(self):
        """2000 km long flight → 2000 × 0.195 = 390 kg."""
        entries = [TransportEntry(mode="flight_long", distanceKm=2000)]
        assert calc_transport(entries) == pytest.approx(390.0)

    def test_multiple_entries(self):
        """Combination of modes sums correctly."""
        entries = [
            TransportEntry(mode="car_petrol", distanceKm=10),  # 2.1
            TransportEntry(mode="bus", distanceKm=20),  # 1.78
        ]
        assert calc_transport(entries) == pytest.approx(3.88)

    def test_empty_list(self):
        """No entries → 0."""
        assert calc_transport([]) == 0.0

    def test_unknown_mode_skipped(self):
        """Unknown mode is skipped gracefully."""
        entries = [TransportEntry(mode="hovercraft", distanceKm=100)]
        assert calc_transport(entries) == 0.0


# ──────────────────────────────────────────────────────
# Food
# ──────────────────────────────────────────────────────


class TestCalcFood:
    """Tests for ``calc_food``."""

    def test_single_vegan_meal(self):
        """1 vegan meal → 0.4 kg."""
        entries = [FoodEntry(mealType="vegan_meal", quantity=1)]
        assert calc_food(entries) == pytest.approx(0.4)

    def test_multiple_chicken_meals(self):
        """3 chicken meals → 3 × 1.5 = 4.5 kg."""
        entries = [FoodEntry(mealType="chicken_meal", quantity=3)]
        assert calc_food(entries) == pytest.approx(4.5)

    def test_beef_meal(self):
        """1 beef meal → 6.0 kg."""
        entries = [FoodEntry(mealType="beef_meal", quantity=1)]
        assert calc_food(entries) == pytest.approx(6.0)

    def test_mixed_meals(self):
        """Mixed meal types."""
        entries = [
            FoodEntry(mealType="chicken_meal", quantity=2),  # 3.0
            FoodEntry(mealType="vegan_meal", quantity=1),  # 0.4
        ]
        assert calc_food(entries) == pytest.approx(3.4)

    def test_empty(self):
        assert calc_food([]) == 0.0

    def test_unknown_meal_skipped(self):
        entries = [FoodEntry(mealType="alien_food", quantity=1)]
        assert calc_food(entries) == 0.0


# ──────────────────────────────────────────────────────
# Energy
# ──────────────────────────────────────────────────────


class TestCalcEnergy:
    """Tests for ``calc_energy``."""

    def test_india_grid(self):
        """10 kWh × 0.82 = 8.2 kg."""
        entries = [EnergyEntry(source="india_grid", kWh=10)]
        assert calc_energy(entries) == pytest.approx(8.2)

    def test_renewable(self):
        """100 kWh × 0.02 = 2.0 kg."""
        entries = [EnergyEntry(source="renewable", kWh=100)]
        assert calc_energy(entries) == pytest.approx(2.0)

    def test_empty(self):
        assert calc_energy([]) == 0.0


# ──────────────────────────────────────────────────────
# Shopping
# ──────────────────────────────────────────────────────


class TestCalcShopping:
    """Tests for ``calc_shopping``."""

    def test_electronics(self):
        """₹5000 electronics → (5000/1000) × 0.8 = 4.0 kg."""
        entries = [ShoppingEntry(category="electronics", amountInr=5000)]
        assert calc_shopping(entries) == pytest.approx(4.0)

    def test_clothing(self):
        """₹2000 clothing → (2000/1000) × 0.4 = 0.8 kg."""
        entries = [ShoppingEntry(category="clothing", amountInr=2000)]
        assert calc_shopping(entries) == pytest.approx(0.8)

    def test_groceries(self):
        """₹3000 groceries → (3000/1000) × 0.2 = 0.6 kg."""
        entries = [ShoppingEntry(category="groceries", amountInr=3000)]
        assert calc_shopping(entries) == pytest.approx(0.6)

    def test_empty(self):
        assert calc_shopping([]) == 0.0


# ──────────────────────────────────────────────────────
# Daily total
# ──────────────────────────────────────────────────────


class TestCalcDailyTotal:
    """Tests for ``calc_daily_total``."""

    def test_full_day(self):
        """A realistic full-day log."""
        result = calc_daily_total(
            transport=[TransportEntry(mode="car_petrol", distanceKm=25)],
            food=[
                FoodEntry(mealType="chicken_meal", quantity=2),
                FoodEntry(mealType="vegan_meal", quantity=1),
            ],
            energy=[EnergyEntry(source="india_grid", kWh=8.5)],
            shopping=[ShoppingEntry(category="electronics", amountInr=5000)],
        )
        assert result["transportCo2Kg"] == pytest.approx(5.25)
        assert result["foodCo2Kg"] == pytest.approx(3.4)
        assert result["energyCo2Kg"] == pytest.approx(6.97)
        assert result["shoppingCo2Kg"] == pytest.approx(4.0)
        assert result["totalCo2Kg"] == pytest.approx(19.62)

    def test_empty_day(self):
        """No activities → all zeros."""
        result = calc_daily_total([], [], [], [])
        assert result["totalCo2Kg"] == 0.0
