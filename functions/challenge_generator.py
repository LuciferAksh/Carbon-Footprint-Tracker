"""
CarbonCoach — Challenge Generator Logic

Pure business logic for generating weekly carbon challenges.
Separated from the Cloud Function entry point for testability.
"""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

# Category display names
CATEGORY_LABELS = {
    "transport": "🚗 Transport",
    "food": "🍽 Food",
    "energy": "⚡ Energy",
    "shopping": "🛍 Shopping",
}


def generate_challenge_prompt(profile: dict[str, Any], logs: list[dict[str, Any]]) -> str:
    """
    Generate the Gemini prompt for weekly challenge creation.

    Summarizes the user's profile and last 7 days of activity logs into
    a structured prompt that Gemini 1.5 Pro can use to generate a
    personalized, achievable weekly challenge.

    Args:
        profile: User's carbon profile from Firestore.
        logs: List of daily activity log dicts from the last 7 days.

    Returns:
        Formatted prompt string for Gemini.
    """
    # Summarize weekly emissions by category
    category_totals: dict[str, float] = {
        "transport": 0.0,
        "food": 0.0,
        "energy": 0.0,
        "shopping": 0.0,
    }

    for log in logs:
        for category in category_totals:
            if category in log and isinstance(log[category], dict):
                category_totals[category] += log[category].get("co2Kg", 0.0)

    total_weekly = sum(category_totals.values())

    # Find the highest-emission category
    highest_category = max(category_totals, key=lambda k: category_totals[k])

    # Build log summary
    log_summary_lines = []
    for category, total in sorted(category_totals.items(), key=lambda x: -x[1]):
        label = CATEGORY_LABELS.get(category, category)
        percentage = (total / total_weekly * 100) if total_weekly > 0 else 0
        log_summary_lines.append(f"  - {label}: {total:.1f} kg CO₂ ({percentage:.0f}%)")

    log_summary = "\n".join(log_summary_lines)

    profile_name = profile.get("carbonProfileType", "Unknown Profile")
    estimated_annual = profile.get("estimatedAnnualKg", "Unknown")
    top_categories = ", ".join(profile.get("topCategories", []))

    prompt = f"""You are a carbon coach. This user's profile:
- Carbon Profile: {profile_name}
- Estimated Annual CO₂: {estimated_annual} kg
- Top emission categories: {top_categories}

Last 7 days of activities (total: {total_weekly:.1f} kg CO₂):
{log_summary}

Highest emission category this week: {CATEGORY_LABELS.get(highest_category, highest_category)} ({category_totals[highest_category]:.1f} kg CO₂)

Generate ONE specific weekly carbon challenge that:
- Targets their highest-emission category ({highest_category})
- Is achievable in 7 days
- Has a clear success metric (e.g. 'Take public transport 3 times this week')
- Includes a CO₂ saving estimate if completed
- Uses Indian context where relevant (₹, km, Indian cities)

Respond in JSON only with this exact schema:
{{
  "title": "string - short catchy title",
  "description": "string - 2-3 sentence description of the challenge",
  "category": "string - one of: transport, food, energy, shopping",
  "targetMetric": "string - specific measurable goal",
  "co2SavingKg": number
}}"""

    return prompt


def parse_challenge_response(response_text: str) -> dict[str, Any] | None:
    """
    Parse and validate the Gemini response into a challenge dict.

    Handles both clean JSON and JSON wrapped in markdown code blocks.

    Args:
        response_text: Raw text response from Gemini.

    Returns:
        Validated challenge dictionary, or None if parsing fails.
    """
    try:
        # Strip markdown code blocks if present
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        data = json.loads(cleaned)

        # Validate required fields
        required_fields = ["title", "description", "category", "targetMetric", "co2SavingKg"]
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field in challenge response: {field}")
                return None

        # Validate category
        valid_categories = {"transport", "food", "energy", "shopping"}
        if data["category"] not in valid_categories:
            logger.warning(f"Invalid category '{data['category']}', defaulting to 'transport'")
            data["category"] = "transport"

        # Ensure co2SavingKg is a number
        try:
            data["co2SavingKg"] = float(data["co2SavingKg"])
        except (ValueError, TypeError):
            data["co2SavingKg"] = 0.0

        return data

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
        logger.debug(f"Raw response: {response_text}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error parsing challenge response: {str(e)}")
        return None
