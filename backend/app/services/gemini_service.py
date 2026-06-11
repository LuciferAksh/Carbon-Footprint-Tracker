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
import json
import logging
from typing import Any, AsyncGenerator, Dict, List

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


async def _generate_text_gemini_api(
    prompt: str,
    settings: Settings,
) -> str:
    """Call the Gemini REST API directly using an API key.

    This is the preferred path when ``GEMINI_API_KEY`` is configured
    because it avoids the heavier Vertex AI SDK initialisation.

    Args:
        prompt: The user-facing prompt text.
        settings: App settings (provides API key and model name).

    Returns:
        The generated text from Gemini.

    Raises:
        ValueError: If the response format is unexpected.
    """
    import httpx
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": settings.CARBON_COACH_SYSTEM_PROMPT}]
        }
    }
    headers = {"Content-Type": "application/json"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers, timeout=30.0)
        response.raise_for_status()
        data = response.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as err:
            logger.error("Failed to parse Gemini response: %s", data)
            raise ValueError("Invalid Gemini response format") from err


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

    if settings.GEMINI_API_KEY:
        try:
            logger.info("Calling Gemini API directly via API key...")
            return await _generate_text_gemini_api(prompt, settings)
        except Exception as exc:
            logger.warning("Gemini API call failed, trying Vertex AI fallback: %s", exc)

    try:
        model = _get_model(settings)
        response = await asyncio.to_thread(
            model.generate_content, prompt
        )
        return response.text
    except Exception as exc:
        logger.warning("Gemini generation failed, falling back to mock: %s", exc)
        # Check if it expects a JSON challenge response
        if "co2SavingKg" in prompt or "co2SavedTarget" in prompt or "JSON" in prompt:
            if "Extract daily carbon footprint" in prompt:
                # Return parsed JSON structure
                return '{"transport": [{"mode": "car_petrol", "distanceKm": 10.0}], "food": [], "energy": [], "shopping": []}'
            # Return standard challenge JSON
            return json.dumps(_MOCK_CHALLENGE)
        
        # Else, return a helpful coach message
        if "CHAT HISTORY" in prompt:
            # Check last message to customise fallback
            last_line = prompt.strip().split("\n")[-2] if "\n" in prompt else ""
            last_message = last_line.lower()
            if "transport" in last_message or "car" in last_message or "drive" in last_message or "travel" in last_message or "km" in last_message:
                return "Your transport emissions are a key area! Switching just 2 commutes per week from a petrol car to public transport or a metro can save up to 15 kg of CO₂ monthly."
            if "food" in last_message or "meat" in last_message or "eat" in last_message or "diet" in last_message or "meal" in last_message or "veg" in last_message:
                return "Your diet has a huge impact! Swapping one meat meal for a vegetarian option (like a dal or paneer dish) saves around 0.8 kg CO₂. A meatless Monday habit can save up to 40 kg CO₂ annually!"
            if "energy" in last_message or "electricity" in last_message or "ac" in last_message or "power" in last_message or "solar" in last_message or "light" in last_message:
                return "Energy is a great category to optimize. Try raising your AC temperature to 24°C, unplugging idle chargers to avoid standby drain, and upgrading to LED bulbs. It saves both carbon and your utility bill!"
            if "shopping" in last_message or "buy" in last_message or "clothes" in last_message or "habit" in last_message:
                return "For shopping, try buying only what you need. Buy pre-owned items when possible, adopt a 'one-in, one-out' rule for clothes, and prioritize experiences over physical goods."
            if "hello" in last_message or "hi" in last_message or "hey" in last_message:
                return "Hello! I am your CarbonCoach. I can help you understand your carbon footprint and guide you on reducing it. What category (Transport, Food, Energy, or Shopping) should we discuss today?"
            if "thanks" in last_message or "thank you" in last_message:
                return "You're very welcome! Keep logging your daily activities and playing the quiz. Together we can make a difference! 🌍"
            if "quiz" in last_message or "game" in last_message:
                return "You can play the Eco-Quiz by clicking the 'Play Eco-Quiz' tab right at the top of this screen. Give it a shot!"
            return (
                "Hello! I am your CarbonCoach (running in resilient offline mode). "
                "Try asking me about travel tips, lowering food footprint, saving household energy, "
                "or click the tab at the top to play our Eco-Quiz!"
            )
        
        return (
            "Great progress! To reduce your carbon footprint further, consider: "
            "1. Replacing short car drives with walking or cycling. "
            "2. Shifting to energy-efficient LED bulbs. "
            "3. Adopting one meat-free day per week. "
            "Keep up the great work! 🌱"
        )


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

    if settings.GEMINI_API_KEY:
        try:
            logger.info("Streaming via Gemini API key...")
            full_text = await _generate_text_gemini_api(prompt, settings)
            for word in full_text.split(" "):
                yield word + " "
                await asyncio.sleep(0.02)
            return
        except Exception as exc:
            logger.warning("Gemini API stream fallback failed: %s", exc)

    try:
        model = _get_model(settings)
        response = await asyncio.to_thread(
            model.generate_content, prompt, stream=True
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as exc:
        logger.warning("Gemini streaming failed, falling back: %s", exc)
        for word in _MOCK_NARRATIVE.split(" "):
            yield word + " "
            await asyncio.sleep(0.02)


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


async def parse_conversational_log(
    text: str,
    uid: str,
    settings: Settings | None = None,
) -> Dict[str, Any]:
    """Parse raw text description of daily carbon activities into structured parameters."""
    settings = settings or get_settings()

    if settings.is_mock:
        # Mock parsing: scan for keywords to return a realistic mock response
        lower_text = text.lower()
        res: Dict[str, List[Any]] = {
            "transport": [],
            "food": [],
            "energy": [],
            "shopping": []
        }
        if "car" in lower_text or "drive" in lower_text or "commute" in lower_text or "rode" in lower_text:
            # check distance
            import re
            dist = 10.0
            match = re.search(r"(\d+(?:\.\d+)?)\s*km", lower_text)
            if match:
                dist = float(match.group(1))
            mode = "car_petrol"
            if "ev" in lower_text or "electric" in lower_text:
                mode = "car_ev"
            res["transport"].append({"mode": mode, "distanceKm": dist})
        if "meal" in lower_text or "eat" in lower_text or "ate" in lower_text or "food" in lower_text or "lunch" in lower_text or "dinner" in lower_text or "sandwich" in lower_text:
            meal = "chicken_meal"
            if "vegan" in lower_text or "plant" in lower_text:
                meal = "vegan_meal"
            elif "veg" in lower_text or "vegetarian" in lower_text:
                meal = "vegetarian_meal"
            res["food"].append({"mealType": meal, "quantity": 1})
        if "electricity" in lower_text or "ac" in lower_text or "power" in lower_text or "kwh" in lower_text:
            res["energy"].append({"source": "india_grid", "kWh": 5.0})
        if "shop" in lower_text or "buy" in lower_text or "bought" in lower_text or "cloth" in lower_text:
            res["shopping"].append({"category": "clothing", "amountInr": 1500.0})
        return res

    # Real Gemini model call
    prompt = (
        "Extract daily carbon footprint activities from the following user description. "
        "User description: \"" + text + "\"\n\n"
        "Return ONLY a JSON object with keys: transport, food, energy, shopping.\n"
        "- 'transport': list of objects with keys: mode (car_petrol, car_ev, bus, train, motorbike), distanceKm (float)\n"
        "- 'food': list of objects with keys: mealType (beef_meal, chicken_meal, fish_meal, vegetarian_meal, vegan_meal), quantity (int)\n"
        "- 'energy': list of objects with keys: source (india_grid, renewable), kWh (float)\n"
        "- 'shopping': list of objects with keys: category (clothing, electronics, furniture, other), amountInr (float)\n\n"
        "If a category is not mentioned, return an empty list for it. Return raw JSON only, no markdown."
    )
    raw = await generate_text(prompt, uid, settings)

    import json
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError) as err:
        logger.warning("Could not parse Gemini log parsing JSON: %s", err)
        return {"transport": [], "food": [], "energy": [], "shopping": []}


async def chat_with_coach(
    messages: List[Dict[str, str]],
    uid: str,
    settings: Settings | None = None,
) -> str:
    """Conversational chat with CarbonCoach. Injects user profile and log stats as context."""
    from app.services import firestore_service  # noqa: WPS433

    settings = settings or get_settings()

    # 1. Fetch user context
    profile = await firestore_service.get_profile(uid)
    logs = await firestore_service.list_daily_logs(uid)

    # 2. Compile metrics summary
    profile_info = {}
    if profile:
        profile_info = {
            "location": profile.get("location"),
            "householdSize": profile.get("householdSize"),
            "primaryTransport": profile.get("primaryTransport"),
            "dietType": profile.get("dietType"),
            "energySource": profile.get("energySource"),
            "shoppingFrequency": profile.get("shoppingFrequency"),
        }

    # Sum total carbon
    total_co2 = sum(log.get("totalCo2Kg", 0.0) for log in logs)
    recent_logs = []
    # Get last 5 logs
    sorted_logs = sorted(logs, key=lambda x: x.get("id", ""), reverse=True)
    for log_entry in sorted_logs[:5]:
        recent_logs.append({
            "date": log_entry.get("id"),
            "totalCo2Kg": log_entry.get("totalCo2Kg"),
            "categories": {
                "transport": log_entry.get("transportCo2Kg"),
                "food": log_entry.get("foodCo2Kg"),
                "energy": log_entry.get("energyCo2Kg"),
                "shopping": log_entry.get("shoppingCo2Kg"),
            }
        })

    # 3. Create context prompt
    context = (
        "USER CONTEXT INFORMATION:\n"
        f"- Profile: {json.dumps(profile_info)}\n"
        f"- Total Tracked Emissions: {total_co2:.1f} kg CO₂\n"
        f"- Recent 5 Logs: {json.dumps(recent_logs)}\n\n"
        "You are CarbonCoach. Answer the user's latest question directly. "
        "Keep responses brief, supportive, and action-oriented. Refer to their actual numbers if relevant."
    )

    if settings.is_mock:
        # Return a friendly mock response based on the last user message
        last_message = messages[-1]["content"] if messages else ""
        lower_msg = last_message.lower()
        if "transport" in lower_msg or "car" in lower_msg:
            return "Based on your logs, transport is a key area. Try walking or taking the metro to save about 3-5 kg CO₂!"
        if "food" in lower_msg or "meat" in lower_msg or "eat" in lower_msg:
            return "Your diet is a great place to start! Swapping one chicken meal for a vegetarian option saves 0.8 kg CO₂ per meal."
        return "I am here to coach you on your carbon reductions! Try tracking your daily commute or asking how to optimize your diet."

    # Using Vertex AI GenerativeModel
    # Construct a structured history prompt for conversational memory
    chat_prompt = context + "\n\nCHAT HISTORY:\n"
    for msg in messages[:-1]:
        sender = "User" if msg["role"] == "user" else "Coach"
        chat_prompt += f"{sender}: {msg['content']}\n"
    
    chat_prompt += f"User: {messages[-1]['content']}\n"
    chat_prompt += "Coach: "

    reply = await generate_text(chat_prompt, uid, settings)
    return reply


async def generate_quiz_questions(
    uid: str,
    count: int = 5,
    settings: Settings | None = None,
) -> List[Dict[str, Any]]:
    """Ask Gemini to generate a batch of multiple-choice questions about sustainability."""
    settings = settings or get_settings()

    # Predefined pool of fallback questions
    fallback_pool = [
        {
            "question": "Which of the following diets has the lowest average carbon footprint?",
            "options": [
                "Vegetarian diet with dairy",
                "Fully vegan diet",
                "Poultry and fish-based diet",
                "High-protein meat diet"
            ],
            "correctAnswer": 1,
            "explanation": "A fully vegan diet has the lowest carbon footprint, saving up to 60-70% of food emissions compared to a diet high in red meat."
        },
        {
            "question": "How much energy/CO₂ does a typical LED bulb save compared to an old incandescent bulb?",
            "options": [
                "About 10% to 20%",
                "About 30% to 50%",
                "About 75% to 80%",
                "Over 95%"
            ],
            "correctAnswer": 2,
            "explanation": "LED bulbs use up to 80% less electricity than traditional incandescent bulbs, drastically reducing grid power demand and carbon emissions."
        },
        {
            "question": "For a 10 km daily commute, which transport mode has the highest emissions per passenger-kilometer?",
            "options": [
                "Bus",
                "Electric Vehicle (EV)",
                "Single-occupant petrol car",
                "Metro/Subway train"
            ],
            "correctAnswer": 2,
            "explanation": "A single-occupant petrol car emits roughly 0.21 kg CO₂ per km, whereas a metro emits less than 0.04 kg per passenger-kilometer."
        },
        {
            "question": "What does the term 'Phantom energy drain' refer to?",
            "options": [
                "Energy used by electric vehicles while parked",
                "Electricity consumed by devices plugged in on standby mode",
                "Solar energy lost due to cloudy weather",
                "Heat leaking through poorly insulated windows"
            ],
            "correctAnswer": 1,
            "explanation": "Phantom energy (or standby load) is the power drawn by appliances like TVs, chargers, and microwaves while they are plugged in but turned off. It accounts for up to 10% of household bills."
        },
        {
            "question": "Which action has the highest single impact on reducing household carbon emissions?",
            "options": [
                "Recycling all household plastic bottles",
                "Switching to a 100% renewable energy tariff or solar panels",
                "Turning off lights when leaving a room",
                "Reusing grocery bags"
            ],
            "correctAnswer": 1,
            "explanation": "Switching your energy supply to renewable grid tariffs or installing home solar panels can reduce your annual household carbon footprint by 1 to 2 tonnes, far exceeding the impact of standard recycling."
        },
        {
            "question": "Which of the following transport modes is generally the most carbon-efficient for long-distance travel?",
            "options": [
                "Commercial airplane",
                "High-speed passenger train",
                "Single-occupancy SUV",
                "Diesel bus"
            ],
            "correctAnswer": 1,
            "explanation": "High-speed passenger trains are powered by electricity and carry hundreds of passengers, resulting in extremely low carbon emissions per passenger-mile compared to flying or driving."
        }
    ]

    import random
    if settings.is_mock:
        return random.sample(fallback_pool, min(count, len(fallback_pool)))

    prompt = (
        f"Generate exactly {count} distinct multiple-choice questions about carbon footprints, environmental science, "
        "or carbon emission reduction strategies.\n"
        "Return ONLY a JSON list of objects, where each object has keys:\n"
        "- 'question': string containing the question\n"
        "- 'options': list of exactly 4 strings for multiple-choice options\n"
        "- 'correctAnswer': integer index (0, 1, 2, or 3) of the correct option in the options list\n"
        "- 'explanation': string explaining why that option is correct\n\n"
        "Do not include any markdown, backticks, or comments. Return raw JSON list only."
    )

    try:
        raw = await generate_text(prompt, uid, settings)
        start = raw.index("[")
        end = raw.rindex("]") + 1
        parsed = json.loads(raw[start:end])
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed
        raise ValueError("Invalid format or empty list")
    except Exception as err:
        logger.warning("Failed to generate dynamic quiz questions, returning fallback: %s", err)
        return random.sample(fallback_pool, min(count, len(fallback_pool)))


async def generate_quiz_question(
    uid: str,
    settings: Settings | None = None,
) -> Dict[str, Any]:
    """Compatibility helper to return a single generated quiz question."""
    questions = await generate_quiz_questions(uid, count=1, settings=settings)
    return questions[0]


