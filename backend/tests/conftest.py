"""
Pytest configuration and shared fixtures for the CarbonCoach test suite.

All tests run with ``MOCK_AI=true`` so no GCP credentials are needed.
The Firestore mock store and rate-limiter state are cleared between tests.
"""

from __future__ import annotations

import os
from typing import AsyncGenerator, Dict, Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# Force mock mode before any app imports
os.environ["MOCK_AI"] = "true"
os.environ["RATE_LIMIT_SECONDS"] = "0"  # Disable rate limiting in tests

from app.core.rate_limiter import clear_all_rate_limits  # noqa: E402
from app.core.security import get_current_user  # noqa: E402
from app.main import app  # noqa: E402
from app.services.firestore_service import clear_mock_store  # noqa: E402


# ── Mock user for dependency override ───────────────

MOCK_USER: Dict[str, Any] = {
    "uid": "test-user-001",
    "email": "test@carboncoach.local",
    "name": "Test User",
    "email_verified": True,
}


async def _override_get_current_user() -> Dict[str, Any]:
    """Override the auth dependency to always return the test user."""
    return MOCK_USER


# Apply the override globally
app.dependency_overrides[get_current_user] = _override_get_current_user


# ── Fixtures ─────────────────────────────────────────


@pytest.fixture(autouse=True)
def _clean_state():
    """Reset all in-memory stores before each test."""
    clear_mock_store()
    clear_all_rate_limits()
    yield
    clear_mock_store()
    clear_all_rate_limits()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP client bound to the FastAPI app.

    Usage in tests::

        async def test_health(client: AsyncClient):
            resp = await client.get("/health")
            assert resp.status_code == 200
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
