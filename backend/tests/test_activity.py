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

    async def test_activity_summary(self, client: AsyncClient):
        """GET /api/v1/activity/summary returns aggregated dashboard data."""
        await client.post(
            "/api/v1/activity",
            json={"date": "2026-06-01", "transport": [{"mode": "car_petrol", "distanceKm": 10}]},
        )
        resp = await client.get("/api/v1/activity/summary?period=week")
        assert resp.status_code == 200
        data = resp.json()
        assert "totalCO2Today" in data
        assert "totalCO2Week" in data
        assert "totalCO2Month" in data
        assert "weeklyComparison" in data
        assert "categoryBreakdown" in data
        assert "streak" in data
        assert "carbonScore" in data

    async def test_log_activity_new_compatibility(self, client: AsyncClient):
        payload = {
            "date": "2026-06-08",
            "transport": [{"mode": "car_petrol", "distanceKm": 10}],
            "food": [],
            "energy": [],
            "shopping": [],
        }
        resp = await client.post("/api/v1/activity/log", json=payload)
        assert resp.status_code == 201
        assert resp.json()["date"] == "2026-06-08"

    async def test_activity_summary_streak_and_score(self, client: AsyncClient):
        from datetime import date, timedelta
        
        # 1. Onboarding first to populate carbon score in profile
        onboarding_payload = {
            "location": "india",
            "householdSize": 4,
            "primaryTransport": "car_petrol",
            "dietType": "chicken_meal",
            "energySource": "india_grid",
            "shoppingFrequency": "medium",
        }
        await client.post("/api/v1/onboarding", json=onboarding_payload)

        # 2. Log consecutive days (today, yesterday, day before) to trigger streak loop
        today = date.today()
        yesterday = today - timedelta(days=1)
        day_before = today - timedelta(days=2)

        for d in [today, yesterday, day_before]:
            await client.post(
                "/api/v1/activity",
                json={"date": d.isoformat(), "transport": [{"mode": "bus", "distanceKm": 10}]},
            )

        resp = await client.get("/api/v1/activity/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["streak"] >= 3
        # Since we onboarded, it should fetch carbon score from profile which is around 60-95
        assert data["carbonScore"] > 0

    async def test_get_community_analytics(self, client: AsyncClient):
        """GET /api/v1/activity/analytics returns paginated community data."""
        resp = await client.get("/api/v1/activity/analytics?page=1&size=5")
        assert resp.status_code == 200
        data = resp.json()
        assert data["page"] == 1
        assert data["size"] == 5
        assert "total" in data
        assert "results" in data
        assert len(data["results"]) == 5
        
        # Test filtering by category
        resp_filtered = await client.get("/api/v1/activity/analytics?category=transport&size=2")
        assert resp_filtered.status_code == 200
        data_filtered = resp_filtered.json()
        for item in data_filtered["results"]:
            assert item["category"] == "transport"


