"""
Application configuration loaded from environment variables.

Uses pydantic-settings to validate and type-check every env var at startup.
When ``MOCK_AI=true`` the app runs entirely without GCP credentials.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised, validated application settings.

    Attributes:
        GCP_PROJECT_ID: Google Cloud project identifier.
        GOOGLE_APPLICATION_CREDENTIALS: Path to the GCP service-account key.
        FIREBASE_WEB_API_KEY: Firebase web API key (used by frontend SDKs).
        MOCK_AI: When ``"true"`` every Gemini / Firestore call returns
            deterministic mock data so the app can run locally without
            any cloud credentials.
        GEMINI_MODEL: Vertex AI model name for Gemini calls.
        GEMINI_LOCATION: GCP region for Vertex AI.
        RATE_LIMIT_SECONDS: Minimum seconds between consecutive Gemini
            calls for the same user.
        APP_ENV: ``development`` | ``staging`` | ``production``.
        LOG_LEVEL: Python logging level name.
        CORS_ORIGINS: JSON-encoded list of allowed CORS origins.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---- GCP / Firebase ----
    GCP_PROJECT_ID: str = "carbon-coach-dev"
    GOOGLE_APPLICATION_CREDENTIALS: str = ""
    FIREBASE_WEB_API_KEY: str = ""

    # ---- Mock mode ----
    MOCK_AI: bool = True

    # ---- Gemini ----
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_LOCATION: str = "us-central1"
    GEMINI_API_KEY: str = ""

    # ---- Rate limiter ----
    RATE_LIMIT_SECONDS: int = 5

    # ---- App ----
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = '["http://localhost:3000","http://localhost:5173"]'

    # ---- Derived helpers ----
    @property
    def is_mock(self) -> bool:
        """Return ``True`` when mock mode is active."""
        return self.MOCK_AI

    @property
    def cors_origin_list(self) -> List[str]:
        """Parse the JSON-encoded CORS_ORIGINS string into a Python list."""
        try:
            return json.loads(self.CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:3000"]

    # ---- System prompt for all Gemini calls ----
    CARBON_COACH_SYSTEM_PROMPT: str = (
        "You are CarbonCoach, a friendly and knowledgeable carbon footprint "
        "advisor. You speak like a supportive coach, not a scientist. Keep "
        "responses concise. Use Indian context where relevant (₹, km, Indian "
        "cities)."
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the singleton *Settings* instance (cached after first call)."""
    return Settings()
