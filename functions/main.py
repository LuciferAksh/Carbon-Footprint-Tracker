"""
CarbonCoach — Weekly Challenge Generator Cloud Function

Triggered by Cloud Scheduler every Monday at 8:00 AM IST.
Reads all active users, analyzes their last 7 days of activity logs,
and generates personalized weekly challenges using Gemini 1.5 Pro.

Google Cloud Function entry point.
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import functions_framework
from google.cloud import firestore
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, GenerationConfig

from challenge_generator import generate_challenge_prompt, parse_challenge_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firestore client
db = firestore.Client()

# IST timezone offset
IST = timezone(timedelta(hours=5, minutes=30))

# CarbonCoach system prompt
SYSTEM_PROMPT = (
    "You are CarbonCoach, a friendly and knowledgeable carbon footprint advisor. "
    "You speak like a supportive coach, not a scientist. Keep responses concise. "
    "Use Indian context where relevant (₹, km, Indian cities)."
)


@functions_framework.http
def generate_weekly_challenges(request: Any) -> tuple[str, int]:
    """
    HTTP Cloud Function entry point for weekly challenge generation.

    Triggered by Cloud Scheduler every Monday at 8:00 AM IST.
    Iterates through all active users, fetches their recent activity,
    and generates a personalized weekly challenge via Gemini 1.5 Pro.

    Args:
        request: The HTTP request object (unused, but required by framework).

    Returns:
        Tuple of (response_body, status_code).
    """
    try:
        now = datetime.now(IST)
        week_key = now.strftime("%Y-W%U")
        seven_days_ago = now - timedelta(days=7)

        logger.info(f"Starting weekly challenge generation for week {week_key}")

        # Get all active users
        users_ref = db.collection("users")
        users = users_ref.stream()

        generated_count = 0
        skipped_count = 0
        error_count = 0

        for user_doc in users:
            uid = user_doc.id
            user_data = user_doc.to_dict()

            if not user_data:
                continue

            try:
                # Check if challenge already exists for this week
                existing_challenge = (
                    db.collection("users")
                    .document(uid)
                    .collection("challenges")
                    .document(week_key)
                    .get()
                )

                if existing_challenge.exists:
                    logger.info(f"Challenge already exists for user {uid}, week {week_key}")
                    skipped_count += 1
                    continue

                # Fetch last 7 days of logs
                logs_ref = (
                    db.collection("users")
                    .document(uid)
                    .collection("logs")
                    .where("date", ">=", seven_days_ago.strftime("%Y-%m-%d"))
                    .order_by("date", direction=firestore.Query.DESCENDING)
                    .limit(7)
                )
                logs = [log.to_dict() for log in logs_ref.stream()]

                # Get user profile
                profile = user_data.get("profile", {})

                if not profile:
                    logger.warning(f"No profile found for user {uid}, skipping")
                    skipped_count += 1
                    continue

                # Generate challenge using Gemini 1.5 Pro
                prompt = generate_challenge_prompt(profile, logs)
                challenge_data = _call_gemini_for_challenge(prompt)

                if challenge_data:
                    # Write challenge to Firestore
                    challenge_doc = {
                        **challenge_data,
                        "status": "active",
                        "createdAt": firestore.SERVER_TIMESTAMP,
                        "weekKey": week_key,
                    }

                    db.collection("users").document(uid).collection(
                        "challenges"
                    ).document(week_key).set(challenge_doc)

                    generated_count += 1
                    logger.info(f"Generated challenge for user {uid}: {challenge_data.get('title', 'N/A')}")
                else:
                    error_count += 1
                    logger.error(f"Failed to generate challenge for user {uid}")

            except Exception as e:
                error_count += 1
                logger.error(f"Error processing user {uid}: {str(e)}")
                continue

        summary = {
            "week": week_key,
            "generated": generated_count,
            "skipped": skipped_count,
            "errors": error_count,
            "timestamp": now.isoformat(),
        }

        logger.info(f"Challenge generation complete: {json.dumps(summary)}")
        return json.dumps(summary), 200

    except Exception as e:
        logger.error(f"Fatal error in challenge generation: {str(e)}")
        return json.dumps({"error": str(e)}), 500


def _call_gemini_for_challenge(prompt: str) -> dict[str, Any] | None:
    """
    Call Gemini 1.5 Pro to generate a weekly challenge.

    Args:
        prompt: The formatted prompt with user profile and activity summary.

    Returns:
        Parsed challenge data dictionary, or None if generation fails.
    """
    try:
        model = GenerativeModel(
            "gemini-1.5-pro",
            system_instruction=SYSTEM_PROMPT,
        )

        generation_config = GenerationConfig(
            temperature=0.7,
            max_output_tokens=1024,
            response_mime_type="application/json",
        )

        response = model.generate_content(
            prompt,
            generation_config=generation_config,
        )

        return parse_challenge_response(response.text)

    except Exception as e:
        logger.error(f"Gemini API call failed: {str(e)}")
        return None
