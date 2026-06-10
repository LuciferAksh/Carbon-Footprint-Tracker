# test_activity.py, Integration tests for the Activity API.  Exercises the POST (log activities) and, Tests for ``/api/v1/activity``.

> 18 nodes · cohesion 0.11

## Key Concepts

- **TestActivityAPI** (9 connections) — `backend\tests\test_activity.py`
- **test_activity.py** (2 connections) — `backend\tests\test_activity.py`
- **.test_activity_summary()** (2 connections) — `backend\tests\test_activity.py`
- **.test_get_activity_by_date()** (2 connections) — `backend\tests\test_activity.py`
- **.test_get_activity_not_found()** (2 connections) — `backend\tests\test_activity.py`
- **.test_list_activities()** (2 connections) — `backend\tests\test_activity.py`
- **.test_log_activity()** (2 connections) — `backend\tests\test_activity.py`
- **.test_log_activity_defaults_date()** (2 connections) — `backend\tests\test_activity.py`
- **.test_transport_only()** (2 connections) — `backend\tests\test_activity.py`
- **Integration tests for the Activity API.  Exercises the POST (log activities) and** (1 connections) — `backend\tests\test_activity.py`
- **Tests for ``/api/v1/activity``.** (1 connections) — `backend\tests\test_activity.py`
- **POST a full day's log and verify calculated emissions.** (1 connections) — `backend\tests\test_activity.py`
- **GET returns a previously logged day.** (1 connections) — `backend\tests\test_activity.py`
- **GET for a date with no log returns 404.** (1 connections) — `backend\tests\test_activity.py`
- **GET /activity returns all logged days.** (1 connections) — `backend\tests\test_activity.py`
- **Omitting date uses today's date.** (1 connections) — `backend\tests\test_activity.py`
- **Log with only transport entries.** (1 connections) — `backend\tests\test_activity.py`
- **GET /api/v1/activity/summary returns aggregated dashboard data.** (1 connections) — `backend\tests\test_activity.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\tests\test_activity.py`

## Audit Trail

- EXTRACTED: 34 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*