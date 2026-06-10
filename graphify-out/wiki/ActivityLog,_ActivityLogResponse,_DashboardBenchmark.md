# ActivityLog, ActivityLogResponse, DashboardBenchmark

> 22 nodes · cohesion 0.28

## Key Concepts

- **ActivityLogResponse** (12 connections) — `backend\app\models\activity.py`
- **activity.py** (12 connections) — `backend\app\models\activity.py`
- **ActivityLog** (10 connections) — `backend\app\models\activity.py`
- **DashboardBenchmark** (9 connections) — `backend\app\models\activity.py`
- **DashboardData** (9 connections) — `backend\app\models\activity.py`
- **Pydantic v2 models for daily activity logging.  Covers all four emission categor** (9 connections) — `backend\app\models\activity.py`
- **A single shopping entry.      Attributes:         category: Key matching ``const** (9 connections) — `backend\app\models\activity.py`
- **WeeklyDataPoint** (9 connections) — `backend\app\models\activity.py`
- **get_summary()** (8 connections) — `backend\app\api\activity.py`
- **ParseTextRequest** (8 connections) — `backend\app\models\activity.py`
- **Retrieve an existing daily log by date.** (8 connections) — `backend\app\api\activity.py`
- **Return every daily activity log for the authenticated user.** (8 connections) — `backend\app\api\activity.py`
- **Parse conversational input using Gemini and return structured log entries.** (8 connections) — `backend\app\api\activity.py`
- **Calculate emissions for the submitted activities and save them.** (8 connections) — `backend\app\api\activity.py`
- **activity.py** (7 connections) — `backend\app\api\activity.py`
- **log_activity()** (6 connections) — `backend\app\api\activity.py`
- **get_activity()** (4 connections) — `backend\app\api\activity.py`
- **list_activities()** (4 connections) — `backend\app\api\activity.py`
- **parse_text_log()** (4 connections) — `backend\app\api\activity.py`
- **log_activity_new()** (2 connections) — `backend\app\api\activity.py`
- **Request body for logging a day's carbon activities.      All four categories are** (1 connections) — `backend\app\models\activity.py`
- **Response after successfully recording a daily activity log.      Attributes:** (1 connections) — `backend\app\models\activity.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\api\activity.py`
- `backend\app\models\activity.py`

## Audit Trail

- EXTRACTED: 56 (36%)
- INFERRED: 100 (64%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*