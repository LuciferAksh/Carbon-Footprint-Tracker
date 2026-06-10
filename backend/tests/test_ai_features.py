"""
Tests for advanced AI features: Conversational Logging Parser and CarbonCoach Chat.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_parse_text_log(client: AsyncClient):
    """Verify that the NLP conversational activity parser processes text logs correctly."""
    response = await client.post(
        "/api/v1/activity/parse-text",
        json={"text": "I drove my electric car for 25 km and ate a vegan lunch"}
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify structured fields exist
    assert "transport" in data
    assert "food" in data
    assert "energy" in data
    assert "shopping" in data
    
    # In mock mode, EV keyword triggers car_ev and distance matching
    assert len(data["transport"]) > 0
    assert data["transport"][0]["mode"] == "car_ev"
    assert data["transport"][0]["distanceKm"] == 25.0
    
    # vegan keyword triggers vegan_meal
    assert len(data["food"]) > 0
    assert data["food"][0]["mealType"] == "vegan_meal"


@pytest.mark.anyio
async def test_chat_coach(client: AsyncClient):
    """Verify that the conversational chat endpoint accepts messages and returns a reply."""
    response = await client.post(
        "/api/v1/insights/chat",
        json={
            "messages": [
                {"role": "user", "content": "How do I lower my transport carbon score?"}
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    assert "reply" in data
    assert len(data["reply"]) > 0
    # In mock mode, should contain advice about transport
    assert "transport" in data["reply"].lower() or "metro" in data["reply"].lower()
