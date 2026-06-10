"""
Integration tests for the Profile API.

Uses the async HTTP client fixture from conftest – all calls go through
the full FastAPI stack with mocked auth and in-memory Firestore.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestProfileAPI:
    """Tests for ``/api/v1/profile``."""

    async def test_create_profile(self, client: AsyncClient):
        """POST creates a profile and returns 201."""
        payload = {
            "name": "Priya Patel",
            "carbonProfileType": "eco-conscious",
            "estimatedAnnualKg": 1800.0,
            "topCategories": ["food", "energy"],
        }
        resp = await client.post("/api/v1/profile", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Priya Patel"
        assert data["carbonProfileType"] == "eco-conscious"
        assert data["uid"] == "test-user-001"
        assert data["createdAt"] is not None

    async def test_get_profile_not_found(self, client: AsyncClient):
        """GET before creating returns 404."""
        resp = await client.get("/api/v1/profile")
        assert resp.status_code == 404

    async def test_get_profile_after_create(self, client: AsyncClient):
        """GET after creating returns the profile."""
        payload = {
            "name": "Rahul Kumar",
            "carbonProfileType": "urban-commuter",
            "estimatedAnnualKg": 2400.0,
            "topCategories": ["transport"],
        }
        await client.post("/api/v1/profile", json=payload)
        resp = await client.get("/api/v1/profile")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Rahul Kumar"

    async def test_update_profile_merges(self, client: AsyncClient):
        """A second POST merges fields into the existing profile."""
        await client.post(
            "/api/v1/profile",
            json={
                "name": "Anita Singh",
                "carbonProfileType": "general",
                "estimatedAnnualKg": 2000.0,
                "topCategories": ["transport"],
            },
        )
        resp = await client.post(
            "/api/v1/profile",
            json={
                "name": "Anita Singh",
                "carbonProfileType": "eco-warrior",
                "estimatedAnnualKg": 1500.0,
                "topCategories": ["food"],
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["carbonProfileType"] == "eco-warrior"
        assert data["estimatedAnnualKg"] == 1500.0

    async def test_onboarding_calculation(self, client: AsyncClient):
        """POST /api/v1/onboarding calculates and returns carbon profile."""
        payload = {
            "location": "india",
            "householdSize": 4,
            "primaryTransport": "car_petrol",
            "dietType": "chicken_meal",
            "energySource": "india_grid",
            "shoppingFrequency": "medium",
        }
        resp = await client.post("/api/v1/onboarding", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert "weeklyEstimate" in data
        assert "monthlyEstimate" in data
        assert "yearlyEstimate" in data
        assert "carbonScore" in data
        assert data["topCategory"] in ["transport", "food", "energy", "shopping"]

    async def test_profile_badges_and_streaks(self, client: AsyncClient):
        from datetime import date, timedelta

        # 1. Onboard with eco-friendly options to get score >= 80 (carbon-a)
        onboard_payload = {
            "location": "india",
            "householdSize": 4,
            "primaryTransport": "train",
            "dietType": "vegan_meal",
            "energySource": "renewable",
            "shoppingFrequency": "low",
        }
        await client.post("/api/v1/onboarding", json=onboard_payload)

        # 2. Check profile when no logs (should have 0 streak, no badges)
        resp = await client.get("/api/v1/profile")
        assert resp.status_code == 200
        data = resp.json()
        assert data["streak"] == 0
        assert "first-log" not in data["badges"]
        # Since score is high (eco options), it should get "carbon-a"
        assert "carbon-a" in data["badges"]

        # 3. Log a daily activity to unlock "first-log" badge
        await client.post(
            "/api/v1/activity",
            json={"date": date.today().isoformat(), "transport": [{"mode": "bus", "distanceKm": 5}]},
        )
        resp = await client.get("/api/v1/profile")
        assert "first-log" in resp.json()["badges"]

        # 4. Log 7 consecutive days to get "week-streak"
        for i in range(1, 8):
            d = date.today() - timedelta(days=i)
            await client.post(
                "/api/v1/activity",
                json={"date": d.isoformat(), "transport": []},
            )
        resp = await client.get("/api/v1/profile")
        assert resp.json()["streak"] >= 7
        assert "week-streak" in resp.json()["badges"]

        # 5. Complete a challenge to get "challenge-1"
        curr = await client.get("/api/v1/challenge/current")
        cid = curr.json()["id"]
        await client.patch(f"/api/v1/challenge/{cid}/complete")
        resp = await client.get("/api/v1/profile")
        assert "challenge-1" in resp.json()["badges"]

        # 6. Log 10 public transport entries to get "green-commute"
        for i in range(10):
            d = date.today() - timedelta(days=15 + i)
            await client.post(
                "/api/v1/activity",
                json={"date": d.isoformat(), "transport": [{"mode": "metro", "distanceKm": 5}]},
            )
        resp = await client.get("/api/v1/profile")
        assert "green-commute" in resp.json()["badges"]

        # 7. Log 7 vegan meals to get "vegan-week"
        for i in range(7):
            d = date.today() - timedelta(days=30 + i)
            await client.post(
                "/api/v1/activity",
                json={"date": d.isoformat(), "food": [{"mealType": "vegan_meal", "quantity": 1}]},
            )
        resp = await client.get("/api/v1/profile")
        assert "vegan-week" in resp.json()["badges"]


