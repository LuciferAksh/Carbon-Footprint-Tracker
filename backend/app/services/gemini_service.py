"""
Gemini service – wraps Vertex AI Gemini calls with streaming + caching.

When ``MOCK_AI=true`` a deterministic mock response is returned so the
app can run without any GCP credentials.

Caching strategy:
    After generating a response the full text is written to Firestore
    (at the path chosen by the caller, typically under the user's
    ``insights`` sub-collection).  On the *next* identical request the
    cached result can be served directly.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, AsyncGenerator, Dict, Optional

from app.core.config import Settings, get_settings
from app.core.rate_limiter import check_rate_limit

logger = logging.getLogger(__name__)

# ── Lazy model handle ────────────────────────────────
_generative_model = None


def _get_model(settings: Settings):
    """Return (or create) the Vertex AI GenerativeModel.  Skipped in mock."""
    global _generative_model
    if settings.is_mock:
        return None
    if _generative_model is None:
        import vertexai  # noqa: WPS433
        from vertexai.generative_models import GenerativeModel  # noqa: WPS433

        vertexai.init(
            project=settings.GCP_PROJECT_ID,
            location=settings.GEMINI_LOCATION,
        )
        _generative_model = GenerativeModel(
            settings.GEMINI_MODEL,
            system_instruction=settings.CARBON_COACH_SYSTEM_PROMPT,
        )
    return _generative_model


# ──────────────────────────────────────────────────────
# Mock helpers
# ──────────────────────────────────────────────────────

_MOCK_NARRATIVE = (
    "Great job this month! 🎉 Your carbon footprint dropped by about 10 %. "
    "Switching two car trips to the metro saved roughly 3 kg CO₂. "
    "Try swapping one chicken meal for a vegetarian thali each week — "
    "that alone could save another 3 kg/month. Keep going, champ! 💪"
)

_MOCK_CHALLENGE = {
    "title": "Metro Week Challenge",
    "description": (
        "Use the metro instead of your car for at least 3 commutes "
        "this week.  Track each trip in CarbonCoach."
    ),
    "category": "transport",
    "targetMetric": "≥3 metro commutes",
    "co2SavingKg": 4.2,
}


# ──────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────


async def generate_text(
    prompt: str,
    uid: str,
    settings: Settings | None = None,
) -> str:
    """Send a prompt to Gemini and return the full text response.

    Rate-limiting is enforced **per user**.

    Args:
        prompt: The user-facing prompt (system prompt is prepended
            automatically by the model config).
        uid: Firebase UID of the caller (used for rate-limiting).
        settings: App settings.

    Returns:
        The generated text string.
    """
    settings = settings or get_settings()
    check_rate_limit(uid, settings)

    if settings.is_mock:
        logger.info("MOCK generate_text for uid=%s", uid)
        return _MOCK_NARRATIVE

    model = _get_model(settings)
    response = await asyncio.to_thread(
        model.generate_content, prompt
    )
    return response.text


async def generate_text_stream(
    prompt: str,
    uid: str,
    settings: Settings | None = None,
) -> AsyncGenerator[str, None]:
    """Stream Gemini output token-by-token.

    Yields:
        Successive text chunks as they arrive from the model.
    """
    settings = settings or get_settings()
    check_rate_limit(uid, settings)

    if settings.is_mock:
        logger.info("MOCK generate_text_stream for uid=%s", uid)
        # Simulate streaming by yielding words one at a time
        for word in _MOCK_NARRATIVE.split(" "):
            yield word + " "
            await asyncio.sleep(0.02)
        return

    model = _get_model(settings)
    response = await asyncio.to_thread(
        model.generate_content, prompt, stream=True
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text


async def generate_insight_narrative(
    uid: str,
    month_data: Dict[str, Any],
    settings: Settings | None = None,
) -> str:
    """Generate a monthly insight narrative and cache it in Firestore.

    If a cached insight already exists for the month, it is returned
    immediately without calling Gemini.

    Args:
        uid: Firebase UID.
        month_data: Dict containing ``totalCo2Kg``, ``prevMonthCo2Kg``,
            and ``month`` (``YYYY-MM``).
        settings: App settings.

    Returns:
        The generated (or cached) narrative text.
    """
    from app.services import firestore_service  # noqa: WPS433 – avoid cycle

    settings = settings or get_settings()
    month_id = month_data.get("month", "unknown")

    # ── Check cache ──
    cached = await firestore_service.get_insight(uid, month_id)
    if cached and cached.get("narrative"):
        logger.info("Returning cached insight for %s/%s", uid, month_id)
        return cached["narrative"]

    # ── Build prompt ──
    total = month_data.get("totalCo2Kg", 0)
    prev = month_data.get("prevMonthCo2Kg")
    comparison = ""
    if prev is not None:
        diff = total - prev
        direction = "increase" if diff > 0 else "decrease"
        comparison = (
            f" Compared to last month ({prev:.1f} kg), that is a "
            f"{abs(diff):.1f} kg {direction}."
        )

    prompt = (
        f"Summarise the user's carbon footprint for {month_id}. "
        f"Total: {total:.1f} kg CO₂.{comparison} "
        "Give 2-3 actionable tips in Indian context."
    )

    narrative = await generate_text(prompt, uid, settings)

    # ── Cache in Firestore ──
    from datetime import datetime, timezone  # noqa: WPS433

    await firestore_service.save_insight(
        uid,
        month_id,
        {
            "totalCo2Kg": total,
            "prevMonthCo2Kg": prev,
            "narrative": narrative,
            "generatedAt": datetime.now(timezone.utc).isoformat(),
        },
    )

    return narrative


async def generate_challenge_suggestion(
    uid: str,
    category: str,
    settings: Settings | None = None,
) -> Dict[str, Any]:
    """Ask Gemini to suggest a weekly challenge for a given category.

    Args:
        uid: Firebase UID.
        category: One of ``transport``, ``food``, ``energy``, ``shopping``.
        settings: App settings.

    Returns:
        Dict with ``title``, ``description``, ``category``,
        ``targetMetric``, ``co2SavingKg``.
    """
    settings = settings or get_settings()

    if settings.is_mock:
        return {**_MOCK_CHALLENGE, "category": category}

    prompt = (
        f"Suggest one specific, achievable weekly challenge to reduce "
        f"carbon emissions in the '{category}' category for an Indian user. "
        f"Return JSON with keys: title, description, category, "
        f"targetMetric, co2SavingKg."
    )
    raw = await generate_text(prompt, uid, settings)

    # Best-effort JSON extraction
    import json  # noqa: WPS433

    try:
        # Try to find JSON object in the response
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        logger.warning("Could not parse Gemini challenge JSON, using fallback")
        return {**_MOCK_CHALLENGE, "category": category}
