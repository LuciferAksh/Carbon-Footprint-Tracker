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

import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import activity, challenge, health, insights, profile
from app.core.config import get_settings

logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler – runs on startup and shutdown.

    Logs the current configuration and mock-mode status.
    """
    import os
    settings = get_settings()
    logging.basicConfig(level=settings.LOG_LEVEL)
    
    if settings.GOOGLE_APPLICATION_CREDENTIALS:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.GOOGLE_APPLICATION_CREDENTIALS
        logger.info("🔑 Set GOOGLE_APPLICATION_CREDENTIALS = %s", settings.GOOGLE_APPLICATION_CREDENTIALS)

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

# ── Custom Middlewares ───────────────────────────────

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def limit_body_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > 1024 * 1024:  # 1MB
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Payload Too Large. Maximum allowed size is 1MB."}
                )
        except ValueError:
            pass
    return await call_next(request)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    return response


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
app.include_router(health.router, prefix="/api")
app.include_router(health.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")
app.include_router(activity.router, prefix="/api/v1")
app.include_router(challenge.router, prefix="/api/v1")
app.include_router(insights.router, prefix="/api/v1")
