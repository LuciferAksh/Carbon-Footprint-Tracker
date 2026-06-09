"""
Health-check endpoint.

Returns basic service status and configuration info.  This route is
**unauthenticated** so load-balancers and uptime monitors can hit it.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Service health check",
    response_description="Service status and configuration snapshot",
)
async def health_check(
    settings: Settings = Depends(get_settings),
) -> dict:
    """Return a lightweight health payload.

    Includes:
    * ``status`` – always ``"ok"`` if the server is up.
    * ``mock_mode`` – whether mock mode is active.
    * ``environment`` – current ``APP_ENV``.
    * ``gemini_model`` – configured Gemini model name.
    """
    return {
        "status": "ok",
        "mock_mode": settings.is_mock,
        "environment": settings.APP_ENV,
        "gemini_model": settings.GEMINI_MODEL,
    }
