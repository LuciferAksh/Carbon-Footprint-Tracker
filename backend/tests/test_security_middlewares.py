"""
Tests for security headers, payload size limiting, and request ID tracking middlewares.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_security_headers_are_present(client: AsyncClient):
    """Verify that all standard security headers are injected into the response."""
    response = await client.get("/health")
    assert response.status_code == 200
    
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("Strict-Transport-Security") == "max-age=63072000; includeSubDomains; preload"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert response.headers.get("Referrer-Policy") == "no-referrer-when-downgrade"


@pytest.mark.anyio
async def test_request_id_header(client: AsyncClient):
    """Verify that X-Request-ID is generated and returned, or propagated if sent by client."""
    # Test generation
    response1 = await client.get("/health")
    assert "X-Request-ID" in response1.headers
    id1 = response1.headers["X-Request-ID"]
    assert len(id1) > 0

    # Test propagation
    custom_id = "test-request-uuid-12345"
    response2 = await client.get("/health", headers={"X-Request-ID": custom_id})
    assert response2.headers.get("X-Request-ID") == custom_id


@pytest.mark.anyio
async def test_payload_size_limit(client: AsyncClient):
    """Verify that payloads larger than 1MB are rejected with 413 Payload Too Large."""
    # Under 1MB should be processed normally (or get the router's normal response)
    small_data = "a" * 1024  # 1 KB
    response_small = await client.post(
        "/api/v1/onboarding", 
        content=small_data,
        headers={"Content-Type": "application/json"}
    )
    # Even if it's bad JSON format, it shouldn't be 413
    assert response_small.status_code != 413

    # Over 1MB should be blocked by middleware with 413
    large_data = "a" * (1024 * 1024 + 100)  # > 1 MB
    response_large = await client.post(
        "/api/v1/onboarding", 
        content=large_data,
        headers={"Content-Type": "application/json"}
    )
    assert response_large.status_code == 413
    assert response_large.json() == {
        "detail": "Payload Too Large. Maximum allowed size is 1MB."
    }
