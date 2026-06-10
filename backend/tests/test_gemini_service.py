"""
Tests for the Gemini service (mock mode).

Verifies that mock-mode responses are returned correctly and that
rate limiting is enforced.
"""

from __future__ import annotations

import os

import pytest
import pytest_asyncio

# Ensure mock mode
os.environ["MOCK_AI"] = "true"
os.environ["RATE_LIMIT_SECONDS"] = "5"

from app.core.config import get_settings
get_settings.cache_clear()

from app.core.rate_limiter import (  # noqa: E402

    check_rate_limit,
    clear_all_rate_limits,
    reset_rate_limit,
)
from app.services import gemini_service  # noqa: E402
from fastapi import HTTPException  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_rate_limits():
    """Clear rate limits before and after each test."""
    clear_all_rate_limits()
    yield
    clear_all_rate_limits()


class TestGeminiServiceMock:
    """Tests for Gemini service in mock mode."""

    @pytest.mark.asyncio
    async def test_generate_text_returns_mock(self):
        """``generate_text`` returns the mock narrative in mock mode."""
        result = await gemini_service.generate_text(
            "test prompt", uid="test-gemini-user"
        )
        assert isinstance(result, str)
        assert len(result) > 0
        assert "footprint" in result.lower() or "carbon" in result.lower() or "co₂" in result.lower()

    @pytest.mark.asyncio
    async def test_generate_text_stream_returns_chunks(self):
        """``generate_text_stream`` yields multiple chunks."""
        chunks = []
        async for chunk in gemini_service.generate_text_stream(
            "test prompt", uid="test-stream-user"
        ):
            chunks.append(chunk)
        assert len(chunks) > 1
        full_text = "".join(chunks)
        assert len(full_text) > 0

    @pytest.mark.asyncio
    async def test_generate_insight_narrative(self):
        """``generate_insight_narrative`` returns a narrative and caches it."""
        month_data = {
            "month": "2026-06",
            "totalCo2Kg": 142.5,
            "prevMonthCo2Kg": 158.0,
        }
        narrative = await gemini_service.generate_insight_narrative(
            uid="test-insight-user", month_data=month_data
        )
        assert isinstance(narrative, str)
        assert len(narrative) > 0

    @pytest.mark.asyncio
    async def test_generate_challenge_suggestion(self):
        """``generate_challenge_suggestion`` returns a valid challenge dict."""
        result = await gemini_service.generate_challenge_suggestion(
            uid="test-challenge-user", category="transport"
        )
        assert isinstance(result, dict)
        assert "title" in result
        assert "description" in result
        assert result["category"] == "transport"


class TestRateLimiter:
    """Tests for the per-user rate limiter."""

    def test_first_call_passes(self):
        """First call should not raise."""
        check_rate_limit("rate-test-user-1")

    def test_rapid_second_call_raises_429(self):
        """Second call within RATE_LIMIT_SECONDS raises 429."""
        check_rate_limit("rate-test-user-2")
        with pytest.raises(HTTPException) as exc_info:
            check_rate_limit("rate-test-user-2")
        assert exc_info.value.status_code == 429

    def test_different_users_independent(self):
        """Different users have independent rate limits."""
        check_rate_limit("user-a")
        # user-b should not be affected
        check_rate_limit("user-b")

    def test_reset_clears_limit(self):
        """``reset_rate_limit`` allows immediate re-call."""
        check_rate_limit("rate-reset-user")
        reset_rate_limit("rate-reset-user")
        # Should not raise now
        check_rate_limit("rate-reset-user")
