import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestChallengeAPI:
    async def test_get_current_challenge(self, client: AsyncClient):
        resp = await client.get("/api/v1/challenge/current")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Green Commuter Week"

    async def test_list_challenges(self, client: AsyncClient):
        resp = await client.get("/api/v1/challenge/list")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_complete_challenge(self, client: AsyncClient):
        curr = await client.get("/api/v1/challenge/current")
        challenge_id = curr.json()["id"]
        resp = await client.patch(f"/api/v1/challenge/{challenge_id}/complete")
        assert resp.status_code == 200
        assert resp.json()["status"] == "completed"

    async def test_suggest_challenge(self, client: AsyncClient):
        resp = await client.post("/api/v1/challenge/suggest/transport")
        assert resp.status_code == 201
        assert "title" in resp.json()

    async def test_create_challenge(self, client: AsyncClient):
        payload = {
            "title": "Energy Saver",
            "description": "Lower AC usage",
            "category": "energy",
            "targetMetric": "AC <= 24C",
            "co2SavingKg": 4.5,
        }
        resp = await client.post("/api/v1/challenge", json=payload)
        assert resp.status_code == 201
        assert resp.json()["title"] == "Energy Saver"

    async def test_get_challenge_by_id(self, client: AsyncClient):
        # Create one first
        curr = await client.get("/api/v1/challenge/current")
        challenge_id = curr.json()["id"]
        
        resp = await client.get(f"/api/v1/challenge/{challenge_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == challenge_id

    async def test_get_challenge_by_id_not_found(self, client: AsyncClient):
        resp = await client.get("/api/v1/challenge/non-existent-challenge-id")
        assert resp.status_code == 404

    async def test_complete_challenge_not_found(self, client: AsyncClient):
        resp = await client.patch("/api/v1/challenge/non-existent-id/complete")
        assert resp.status_code == 404

    async def test_suggest_challenge_invalid_category(self, client: AsyncClient):
        resp = await client.post("/api/v1/challenge/suggest/invalid-cat")
        assert resp.status_code == 400

