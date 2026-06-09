"""
Pydantic v2 models for user profiles.

These models handle both the request body when creating/updating a profile
and the response shape returned by the API.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    """Request body for creating or updating a user profile.

    Attributes:
        name: Display name of the user.
        carbonProfileType: High-level lifestyle category such as
            ``'urban-commuter'`` or ``'eco-conscious'``.
        estimatedAnnualKg: Rough estimate of the user's annual carbon
            footprint in kg CO₂e.
        topCategories: Up to 3 categories where the user emits the most.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Display name",
        json_schema_extra={"examples": ["Aarav Sharma"]},
    )
    carbonProfileType: str = Field(
        default="general",
        description="Lifestyle archetype for personalised tips",
        json_schema_extra={"examples": ["urban-commuter"]},
    )
    estimatedAnnualKg: float = Field(
        default=0.0,
        ge=0,
        description="Estimated annual CO₂ in kg",
        json_schema_extra={"examples": [2400.0]},
    )
    topCategories: List[str] = Field(
        default_factory=list,
        max_length=5,
        description="Top emission categories",
        json_schema_extra={"examples": [["transport", "food"]]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Aarav Sharma",
                    "carbonProfileType": "urban-commuter",
                    "estimatedAnnualKg": 2400.0,
                    "topCategories": ["transport", "food"],
                }
            ]
        }
    }


class ProfileResponse(BaseModel):
    """Response body for a user profile.

    Attributes:
        uid: Firebase UID.
        name: Display name.
        carbonProfileType: Lifestyle archetype.
        estimatedAnnualKg: Estimated annual CO₂.
        topCategories: Top emission categories.
        createdAt: ISO-8601 timestamp of profile creation.
    """

    uid: str = Field(..., description="Firebase user ID")
    name: str = Field(..., description="Display name")
    carbonProfileType: str = Field(
        default="general", description="Lifestyle archetype"
    )
    estimatedAnnualKg: float = Field(
        default=0.0, description="Estimated annual CO₂ in kg"
    )
    topCategories: List[str] = Field(
        default_factory=list, description="Top emission categories"
    )
    createdAt: Optional[str] = Field(
        default=None, description="ISO-8601 creation timestamp"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uid": "abc123",
                    "name": "Aarav Sharma",
                    "carbonProfileType": "urban-commuter",
                    "estimatedAnnualKg": 2400.0,
                    "topCategories": ["transport", "food"],
                    "createdAt": "2026-01-15T10:30:00Z",
                }
            ]
        }
    }
