"""
Pydantic v2 models for user profiles and onboarding.
"""

from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class ProfileCreate(BaseModel):
    """Request body for creating or updating a user profile."""
    name: str = Field(..., min_length=1, max_length=100)
    carbonProfileType: str = "general"
    estimatedAnnualKg: float = 0.0
    topCategories: List[str] = Field(default_factory=list)


class OnboardingAnswers(BaseModel):
    """Onboarding quiz answers submitted by the user."""
    location: str
    householdSize: int
    primaryTransport: str
    dietType: str
    energySource: str
    shoppingFrequency: str


class CarbonProfile(BaseModel):
    """Calculated carbon profile result."""
    weeklyEstimate: float
    monthlyEstimate: float
    yearlyEstimate: float
    nationalAverage: float
    percentile: float
    topCategory: str
    recommendations: List[str]
    carbonScore: int


class ProfileResponse(BaseModel):
    """Response body representing user profile and auth state."""
    uid: str
    name: Optional[str] = None
    displayName: Optional[str] = None
    email: Optional[str] = None
    photoURL: Optional[str] = None
    onboardingComplete: bool = False
    carbonProfileType: str = "general"
    estimatedAnnualKg: float = 0.0
    topCategories: List[str] = Field(default_factory=list)
    createdAt: Optional[str] = None
    onboardingAnswers: Optional[OnboardingAnswers] = None
    carbonProfile: Optional[CarbonProfile] = None
    streak: int = 0
    badges: List[str] = Field(default_factory=list)
