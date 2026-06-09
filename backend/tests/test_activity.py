"""
Integration tests for the Activity API.

Exercises the POST (log activities) and GET (retrieve / list) endpoints.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestActivityAPI:
    """Tests for ``/api/v1/activity``."""

    async def test_log_activity(self, client: AsyncClient):
        """POST a full day's log and verify calculated emissions."""
        payload = {
            "date": "2026-06-08",
            "transport": [{"mode": "car_petrol", "distanceKm": 25}],
            "food": [
                {"mealType": "chicken_meal", "quantity": 2},
                {"mealType": "vegan_meal", "quantity": 1},
            ],
            "energy": [{"source": "india_grid", "kWh": 8.5}],
            "shopping": [{"category": "electronics", "amountInr": 5000}],
        }
        resp = await client.post("/api/v1/activity", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["date"] == "2026-06-08"
        assert data["transportCo2Kg"] == pytest.approx(5.25)
        assert data["foodCo2Kg"] == pytest.approx(3.4)
        assert data["energyCo2Kg"] == pytest.approx(6.97)
        assert data["shoppingCo2Kg"] == pytest.approx(4.0)
        assert data["totalCo2Kg"] == pytest.approx(19.62)

    async def test_get_activity_by_date(self, client: AsyncClient):
        """GET returns a previously logged day."""
        payload = {
            "date": "2026-06-07",
            "transport": [{"mode": "bus", "distanceKm": 10}],
            "food": [],
            "energy": [],
            "shopping": [],
        }
        await client.post("/api/v1/activity", json=payload)
        resp = await client.get("/api/v1/activity/2026-06-07")
        assert resp.status_code == 200
        assert resp.json()["transportCo2Kg"] == pytest.approx(0.89)

    async def test_get_activity_not_found(self, client: AsyncClient):
        """GET for a date with no log returns 404."""
        resp = await client.get("/api/v1/activity/2000-01-01")
        assert resp.status_code == 404

    async def test_list_activities(self, client: AsyncClient):
        """GET /activity returns all logged days."""
        await client.post(
            "/api/v1/activity",
            json={"date": "2026-06-01", "transport": [], "food": [], "energy": [], "shopping": []},
        )
        await client.post(
            "/api/v1/activity",
            json={"date": "2026-06-02", "transport": [], "food": [], "energy": [], "shopping": []},
        )
        resp = await client.get("/api/v1/activity")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    async def test_log_activity_defaults_date(self, client: AsyncClient):
        """Omitting date uses today's date."""
        payload = {
            "transport": [{"mode": "train", "distanceKm": 50}],
            "food": [],
            "energy": [],
            "shopping": [],
        }
        resp = await client.post("/api/v1/activity", json=payload)
        assert resp.status_code == 201
        # date should be a valid YYYY-MM-DD
        assert len(resp.json()["date"]) == 10

    async def test_transport_only(self, client: AsyncClient):
        """Log with only transport entries."""
        payload = {
            "date": "2026-06-05",
            "transport": [{"mode": "motorbike", "distanceKm": 30}],
        }
        resp = await client.post("/api/v1/activity", json=payload)
        assert resp.status_code == 201
        assert resp.json()["transportCo2Kg"] == pytest.approx(3.42)
        assert resp.json()["foodCo2Kg"] == 0.0
