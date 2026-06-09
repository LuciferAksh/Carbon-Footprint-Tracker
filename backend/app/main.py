"""
CarbonCoach FastAPI application entry-point.

Creates the ``FastAPI`` app instance, registers middleware (CORS),
and includes all API routers.

Run locally::

    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import activity, challenge, health, insights, profile
from app.core.config import get_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler – runs on startup and shutdown.

    Logs the current configuration and mock-mode status.
    """
    settings = get_settings()
    logging.basicConfig(level=settings.LOG_LEVEL)
    logger.info(
        "🌱 CarbonCoach starting – env=%s  mock=%s  model=%s",
        settings.APP_ENV,
        settings.is_mock,
        settings.GEMINI_MODEL,
    )
    yield
    logger.info("🛑 CarbonCoach shutting down.")


app = FastAPI(
    title="CarbonCoach API",
    description=(
        "AI-powered carbon footprint tracker backend. "
        "Track transport, food, energy & shopping emissions. "
        "Get personalised insights and weekly challenges from Gemini."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS middleware ──────────────────────────────────
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ────────────────────────────────
app.include_router(health.router)
app.include_router(profile.router, prefix="/api/v1")
app.include_router(activity.router, prefix="/api/v1")
app.include_router(challenge.router, prefix="/api/v1")
app.include_router(insights.router, prefix="/api/v1")
