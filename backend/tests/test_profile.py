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
