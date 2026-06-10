# ChallengeResponse

> God node · 18 connections · `backend\app\models\challenge.py`

## Connections by Relation

### calls
- [[get_current_challenge()]] `INFERRED`
- [[suggest_challenge()]] `INFERRED`
- [[create_challenge()]] `INFERRED`
- [[get_challenge()]] `INFERRED`
- [[complete_challenge()]] `INFERRED`
- [[list_challenges()]] `INFERRED`

### contains
- [[challenge.py]] `EXTRACTED`

### inherits
- [[BaseModel]] `EXTRACTED`

### rationale_for
- [[Response shape for a weekly challenge.]] `EXTRACTED`

### uses
- [[CategoryBreakdown]] `INFERRED`
- [[Pydantic v2 models for weekly challenges and monthly insights.]] `INFERRED`
- [[Return the current ISO week as ``YYYY-WNN``.]] `INFERRED`
- [[Create a new weekly challenge for the current ISO week.]] `INFERRED`
- [[Retrieve the current week's challenge, creating a default one if none exists.]] `INFERRED`
- [[Return every challenge for the authenticated user.]] `INFERRED`
- [[Retrieve a single challenge by its ID.]] `INFERRED`
- [[Mark a challenge as completed.]] `INFERRED`
- [[Ask Gemini to suggest a challenge for *category* and save it.]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*