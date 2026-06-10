# CategoryBreakdown, challenge.py, insights.py

> 45 nodes · cohesion 0.14

## Key Concepts

- **CategoryBreakdown** (29 connections) — `backend\app\models\activity.py`
- **BaseModel** (23 connections)
- **ChallengeResponse** (18 connections) — `backend\app\models\challenge.py`
- **ChallengeCreate** (12 connections) — `backend\app\models\challenge.py`
- **ChallengeStatusUpdate** (12 connections) — `backend\app\models\challenge.py`
- **InsightResponse** (12 connections) — `backend\app\models\challenge.py`
- **MonthlyReportResponse** (10 connections) — `backend\app\models\challenge.py`
- **WeeklyTrendPoint** (10 connections) — `backend\app\models\challenge.py`
- **challenge.py** (9 connections) — `backend\app\models\challenge.py`
- **ChatRequest** (9 connections) — `backend\app\models\challenge.py`
- **list_daily_logs()** (9 connections) — `backend\app\services\firestore_service.py`
- **challenge.py** (8 connections) — `backend\app\api\challenge.py`
- **get_monthly_report()** (7 connections) — `backend\app\api\insights.py`
- **insights.py** (6 connections) — `backend\app\api\insights.py`
- **get_current_challenge()** (6 connections) — `backend\app\api\challenge.py`
- **Pydantic v2 models for weekly challenges and monthly insights.** (6 connections) — `backend\app\models\challenge.py`
- **suggest_challenge()** (6 connections) — `backend\app\api\challenge.py`
- **save_challenge()** (6 connections) — `backend\app\services\firestore_service.py`
- **generate_insight()** (6 connections) — `backend\app\api\insights.py`
- **Insights API – generate and retrieve monthly carbon-footprint insights.** (6 connections) — `backend\app\api\insights.py`
- **Retrieve a previously generated monthly insight.** (6 connections) — `backend\app\api\insights.py`
- **Generate a Gemini-powered monthly narrative.** (6 connections) — `backend\app\api\insights.py`
- **Stream the Gemini-generated narrative as Server-Sent Events.** (6 connections) — `backend\app\api\insights.py`
- **Execute a conversational interaction with the AI coach, incorporating metrics co** (6 connections) — `backend\app\api\insights.py`
- **Retrieve or generate the monthly carbon report including AI narrative.** (6 connections) — `backend\app\api\insights.py`
- *... and 20 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\api\challenge.py`
- `backend\app\api\insights.py`
- `backend\app\models\activity.py`
- `backend\app\models\challenge.py`
- `backend\app\services\firestore_service.py`

## Audit Trail

- EXTRACTED: 128 (41%)
- INFERRED: 183 (59%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*