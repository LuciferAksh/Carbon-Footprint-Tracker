"""
Pydantic v2 models for weekly challenges and monthly insights.
"""

from __future__ import annotations

from typing import List, Optional


from pydantic import BaseModel, Field
from app.models.activity import CategoryBreakdown



# ──────────────────────────────────────────────────────
# Challenges
# ──────────────────────────────────────────────────────


class ChallengeCreate(BaseModel):
    """Request body for creating a weekly challenge.

    Attributes:
        title: Short title for the challenge.
        description: Longer description with instructions.
        category: Emission category the challenge targets.
        targetMetric: Quantitative goal description.
        co2SavingKg: Estimated CO₂ saving if the challenge is met.
    """

    title: str = Field(
        ...,
        min_length=3,
        max_length=120,
        description="Challenge title",
        json_schema_extra={"examples": ["Meatless Monday Week"]},
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=500,
        description="Challenge instructions",
        json_schema_extra={
            "examples": [
                "Skip all meat meals on Monday for the whole week."
            ]
        },
    )
    category: str = Field(
        ...,
        description="Emission category (transport, food, energy, shopping)",
        json_schema_extra={"examples": ["food"]},
    )
    targetMetric: str = Field(
        ...,
        description="Quantitative goal description",
        json_schema_extra={"examples": ["0 meat meals on Mondays"]},
    )
    co2SavingKg: float = Field(
        ...,
        ge=0,
        description="Estimated weekly CO₂ saving in kg",
        json_schema_extra={"examples": [4.5]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Meatless Monday Week",
                    "description": "Skip all meat meals on Monday for the whole week.",
                    "category": "food",
                    "targetMetric": "0 meat meals on Mondays",
                    "co2SavingKg": 4.5,
                }
            ]
        }
    }


class ChallengeResponse(BaseModel):
    """Response shape for a weekly challenge.

    Attributes:
        id: Challenge identifier in ``YYYY-WNN`` format.
        title: Short display title.
        description: Detailed challenge instructions.
        category: Emission category (transport, food, energy, shopping).
        targetMetric: Quantitative goal description.
        co2SavingKg: Estimated CO₂ saving if completed (kg).
        status: Current status (active, completed, failed).
        difficulty: Difficulty level (easy, medium, hard).
        durationDays: Challenge duration in days.
        co2SavedTarget: Target CO₂ saving (kg).
        co2SavedActual: Actual CO₂ saved so far (kg).
        progress: Completion progress (0–100).
        participants: Number of participants.
        tips: List of helpful tips for completing the challenge.
    """

    id: str = Field(..., description="Challenge ID (YYYY-WW)")
    title: str = Field(..., description="Challenge title")
    description: str = Field(..., description="Challenge instructions")
    category: str = Field(..., description="Emission category")
    targetMetric: str = Field(..., description="Quantitative goal")
    co2SavingKg: float = Field(..., description="Estimated CO₂ saving (kg)")
    status: str = Field(default="active", description="Challenge status")
    difficulty: str = Field(default="medium", description="Difficulty level")
    durationDays: int = Field(default=7, description="Duration in days")
    co2SavedTarget: float = Field(default=5.0, description="Target CO₂ saving (kg)")
    co2SavedActual: float = Field(default=0.0, description="Actual CO₂ saved (kg)")
    progress: float = Field(default=0.0, description="Completion progress 0–100")
    participants: int = Field(default=124, description="Number of participants")
    tips: List[str] = Field(default_factory=list, description="Helpful tips")


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "2026-W24",
                    "title": "Meatless Monday Week",
                    "description": "Skip all meat meals on Monday for the whole week.",
                    "category": "food",
                    "targetMetric": "0 meat meals on Mondays",
                    "co2SavingKg": 4.5,
                    "status": "active",
                }
            ]
        }
    }


class ChallengeStatusUpdate(BaseModel):
    """Request body for updating a challenge's status.

    Attributes:
        status: New status value.
    """

    status: str = Field(
        ...,
        description="New status (active | completed | failed)",
        json_schema_extra={"examples": ["completed"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"status": "completed"}]
        }
    }


# ──────────────────────────────────────────────────────
# Insights
# ──────────────────────────────────────────────────────


class InsightResponse(BaseModel):
    """Monthly insight summary generated by Gemini.

    Attributes:
        month: ``YYYY-MM`` identifier.
        totalCo2Kg: Total CO₂ for the month.
        prevMonthCo2Kg: Previous month's total for comparison.
        narrative: AI-generated narrative insight.
        generatedAt: ISO-8601 timestamp.
    """

    month: str = Field(
        ...,
        description="Month identifier (YYYY-MM)",
        json_schema_extra={"examples": ["2026-06"]},
    )
    totalCo2Kg: float = Field(
        default=0.0,
        description="Total CO₂ for the month in kg",
        json_schema_extra={"examples": [142.5]},
    )
    prevMonthCo2Kg: Optional[float] = Field(
        default=None,
        description="Previous month's CO₂ for comparison",
        json_schema_extra={"examples": [158.0]},
    )
    narrative: str = Field(
        default="",
        description="AI-generated narrative insight",
        json_schema_extra={
            "examples": [
                "Great progress! You cut your footprint by 10% this month."
            ]
        },
    )
    generatedAt: Optional[str] = Field(
        default=None,
        description="ISO-8601 generation timestamp",
        json_schema_extra={"examples": ["2026-06-08T12:00:00Z"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "month": "2026-06",
                    "totalCo2Kg": 142.5,
                    "prevMonthCo2Kg": 158.0,
                    "narrative": "Great progress! You cut your footprint by 10% this month.",
                    "generatedAt": "2026-06-08T12:00:00Z",
                }
            ]
        }
    }


class WeeklyTrendPoint(BaseModel):
    """A data point in the monthly weekly-trend chart.

    Attributes:
        week: Week label (e.g. ``W1``, ``W2``, ``W3``, ``W4``).
        amount: Total CO\u2082 for that week segment (kg).
    """

    week: str = Field(..., description="Week label")
    amount: float = Field(..., description="Total CO\u2082 for the week (kg)")


class MonthlyReportResponse(BaseModel):
    """Full monthly carbon-footprint report with AI narrative.

    Attributes:
        month: Month identifier (``YYYY-MM``).
        year: Calendar year.
        totalCO2: Total emissions for the month (kg).
        previousMonthCO2: Previous month's total emissions (kg).
        changePercent: Month-over-month change percentage.
        dailyAverage: Average daily emissions (kg).
        categoryBreakdown: Per-category emission breakdown.
        weeklyTrend: Weekly aggregated emission trend.
        geminiNarrative: AI-generated narrative insight.
        highlights: Key achievements or observations.
        score: Monthly carbon score (0\u2013100).
    """

    month: str = Field(..., description="Month identifier (YYYY-MM)")
    year: int = Field(..., description="Calendar year")
    totalCO2: float = Field(..., description="Total month emissions (kg)")
    previousMonthCO2: float = Field(..., description="Previous month emissions (kg)")
    changePercent: float = Field(..., description="Month-over-month change %")
    dailyAverage: float = Field(..., description="Average daily emissions (kg)")
    categoryBreakdown: List[CategoryBreakdown] = Field(..., description="Per-category breakdown")
    weeklyTrend: List[WeeklyTrendPoint] = Field(..., description="Weekly trend data")
    geminiNarrative: str = Field(..., description="AI-generated narrative")
    highlights: List[str] = Field(..., description="Key highlights")
    score: int = Field(..., description="Monthly carbon score 0\u2013100")


class ChatMessage(BaseModel):
    """A single message in a coach conversation.

    Attributes:
        role: Sender role (``user`` or ``assistant``).
        content: Message text content.
    """

    role: str = Field(..., description="Sender role (user | assistant)")
    content: str = Field(..., description="Message text")


class ChatRequest(BaseModel):
    """Request body for the AI coach chat endpoint.

    Attributes:
        messages: Ordered list of conversation messages.
    """

    messages: List[ChatMessage] = Field(..., description="Conversation history")


class QuizQuestionResponse(BaseModel):
    """Response model for a dynamically generated quiz question."""
    question: str = Field(..., description="The quiz question text")
    options: List[str] = Field(..., description="List of 4 options")
    correctAnswer: int = Field(..., description="Index of the correct option (0-3)")
    explanation: str = Field(..., description="Explanation of why the option is correct")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "question": "Which of the following diets has the lowest average carbon footprint?",
                    "options": [
                        "Vegetarian diet with dairy",
                        "Fully vegan diet",
                        "Poultry and fish-based diet",
                        "High-protein meat diet"
                    ],
                    "correctAnswer": 1,
                    "explanation": "A fully vegan diet has the lowest carbon footprint, saving up to 60-70% of food emissions."
                }
            ]
        }
    }


