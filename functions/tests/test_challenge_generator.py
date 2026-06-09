"""
Tests for the CarbonCoach challenge generator logic.
"""

import json
import pytest
from challenge_generator import generate_challenge_prompt, parse_challenge_response


class TestGenerateChallengePrompt:
    """Tests for the generate_challenge_prompt function."""

    def _sample_profile(self) -> dict:
        """Return a sample user profile for testing."""
        return {
            "carbonProfileType": "The Urban Commuter",
            "estimatedAnnualKg": 4500,
            "topCategories": ["transport", "food", "energy"],
        }

    def _sample_logs(self) -> list[dict]:
        """Return sample weekly activity logs for testing."""
        return [
            {
                "date": "2026-06-01",
                "transport": {"mode": "car_petrol", "km": 30, "co2Kg": 6.3},
                "food": {"meals": ["chicken_meal", "vegan_meal"], "co2Kg": 1.9},
                "energy": {"kwh": 8, "co2Kg": 6.56},
                "shopping": {"items": [], "co2Kg": 0.0},
                "totalCo2Kg": 14.76,
            },
            {
                "date": "2026-06-02",
                "transport": {"mode": "bus", "km": 20, "co2Kg": 1.78},
                "food": {"meals": ["vegetarian_meal", "vegan_meal"], "co2Kg": 1.1},
                "energy": {"kwh": 6, "co2Kg": 4.92},
                "shopping": {"items": ["clothing"], "co2Kg": 0.8},
                "totalCo2Kg": 8.6,
            },
        ]

    def test_prompt_contains_profile_info(self) -> None:
        """Prompt should include the user's carbon profile type."""
        prompt = generate_challenge_prompt(self._sample_profile(), self._sample_logs())
        assert "The Urban Commuter" in prompt
        assert "4500" in prompt

    def test_prompt_contains_log_summary(self) -> None:
        """Prompt should contain emission totals by category."""
        prompt = generate_challenge_prompt(self._sample_profile(), self._sample_logs())
        assert "Transport" in prompt
        assert "Food" in prompt
        assert "Energy" in prompt

    def test_prompt_identifies_highest_category(self) -> None:
        """Prompt should identify the highest-emission category."""
        prompt = generate_challenge_prompt(self._sample_profile(), self._sample_logs())
        # Energy should be highest (6.56 + 4.92 = 11.48)
        assert "energy" in prompt.lower()

    def test_prompt_handles_empty_logs(self) -> None:
        """Prompt should handle empty logs gracefully."""
        prompt = generate_challenge_prompt(self._sample_profile(), [])
        assert "0.0 kg CO" in prompt

    def test_prompt_handles_missing_profile_fields(self) -> None:
        """Prompt should handle missing profile fields gracefully."""
        prompt = generate_challenge_prompt({}, [])
        assert "Unknown Profile" in prompt


class TestParseChallengeResponse:
    """Tests for the parse_challenge_response function."""

    def _valid_response(self) -> str:
        """Return a valid JSON challenge response."""
        return json.dumps({
            "title": "Green Commute Week",
            "description": "Take public transport or cycle at least 3 days this week.",
            "category": "transport",
            "targetMetric": "Use public transport 3 times",
            "co2SavingKg": 4.2,
        })

    def test_parses_valid_json(self) -> None:
        """Should correctly parse a valid JSON response."""
        result = parse_challenge_response(self._valid_response())
        assert result is not None
        assert result["title"] == "Green Commute Week"
        assert result["co2SavingKg"] == 4.2

    def test_parses_json_in_code_block(self) -> None:
        """Should handle JSON wrapped in markdown code blocks."""
        wrapped = f"```json\n{self._valid_response()}\n```"
        result = parse_challenge_response(wrapped)
        assert result is not None
        assert result["title"] == "Green Commute Week"

    def test_rejects_missing_fields(self) -> None:
        """Should return None when required fields are missing."""
        incomplete = json.dumps({"title": "Test", "description": "Test"})
        result = parse_challenge_response(incomplete)
        assert result is None

    def test_handles_invalid_json(self) -> None:
        """Should return None for unparseable responses."""
        result = parse_challenge_response("not json at all")
        assert result is None

    def test_handles_invalid_category(self) -> None:
        """Should default invalid categories to 'transport'."""
        response = json.dumps({
            "title": "Test",
            "description": "Test",
            "category": "invalid_category",
            "targetMetric": "Test",
            "co2SavingKg": 1.0,
        })
        result = parse_challenge_response(response)
        assert result is not None
        assert result["category"] == "transport"

    def test_coerces_co2_saving_to_float(self) -> None:
        """Should coerce co2SavingKg to float."""
        response = json.dumps({
            "title": "Test",
            "description": "Test",
            "category": "food",
            "targetMetric": "Test",
            "co2SavingKg": "3.5",
        })
        result = parse_challenge_response(response)
        assert result is not None
        assert result["co2SavingKg"] == 3.5
        assert isinstance(result["co2SavingKg"], float)
