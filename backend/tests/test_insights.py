import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
class TestInsightsAPI:
    async def test_get_monthly_report(self, client: AsyncClient):
        resp = await client.get("/api/v1/insights/monthly?month=2026-06")
        assert resp.status_code == 200
        data = resp.json()
        assert data["month"] == "2026-06"
        assert "totalCO2" in data
        assert "geminiNarrative" in data
        assert "weeklyTrend" in data
        assert "categoryBreakdown" in data

    async def test_get_insight_compatibility(self, client: AsyncClient):
        await client.post("/api/v1/insights/2026-06/generate")
        resp = await client.get("/api/v1/insights/2026-06")
        assert resp.status_code == 200
        assert resp.json()["month"] == "2026-06"

    async def test_stream_insight(self, client: AsyncClient):
        # We need to make a request and inspect the response
        resp = await client.get("/api/v1/insights/2026-06/stream")
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers["content-type"]

    async def test_get_quiz_question(self, client: AsyncClient):
        resp = await client.get("/api/v1/insights/quiz?count=5")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0
        first_q = data[0]
        assert "question" in first_q
        assert "options" in first_q
        assert len(first_q["options"]) == 4
        assert "correctAnswer" in first_q
        assert "explanation" in first_q

    async def test_get_monthly_report_invalid_format(self, client: AsyncClient):
        resp = await client.get("/api/v1/insights/monthly?month=invalid-date")
        assert resp.status_code == 400

    async def test_get_monthly_report_january(self, client: AsyncClient):
        resp = await client.get("/api/v1/insights/monthly?month=2026-01")
        assert resp.status_code == 200

    async def test_get_monthly_report_with_comparison(self, client: AsyncClient):
        # Log this month (June)
        await client.post(
            "/api/v1/activity",
            json={"date": "2026-06-15", "transport": [{"mode": "bus", "distanceKm": 10}]}
        )
        # Log previous month (May)
        await client.post(
            "/api/v1/activity",
            json={"date": "2026-05-15", "transport": [{"mode": "bus", "distanceKm": 5}]}
        )
        resp = await client.get("/api/v1/insights/monthly?month=2026-06")
        assert resp.status_code == 200
        data = resp.json()
        assert data["previousMonthCO2"] > 0
        assert data["changePercent"] != 0.0
        # Weekly trends should reflect W3 (since 15th is W3)
        assert any(item["week"] == "W3" and item["amount"] > 0 for item in data["weeklyTrend"])

    async def test_get_insight_not_found(self, client: AsyncClient):
        resp = await client.get("/api/v1/insights/non-existent-month")
        assert resp.status_code == 404

    async def test_generate_insight_empty_cache(self, client: AsyncClient):
        # POST to generate first time
        resp1 = await client.post("/api/v1/insights/2026-07/generate")
        assert resp1.status_code == 201
        
        # POST again to check cached return path
        resp2 = await client.post("/api/v1/insights/2026-07/generate")
        assert resp2.status_code == 201


