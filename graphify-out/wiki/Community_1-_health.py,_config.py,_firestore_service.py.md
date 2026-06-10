# Community 1: health.py, config.py, firestore_service.py

> 73 nodes · cohesion 0.05

## Key Concepts

- **Settings** (46 connections) — `backend\app\core\config.py`
- **firestore_service.py** (19 connections) — `backend\app\services\firestore_service.py`
- **get_settings()** (17 connections) — `backend\app\core\config.py`
- **get_document()** (10 connections) — `backend\app\services\firestore_service.py`
- **set_document()** (10 connections) — `backend\app\services\firestore_service.py`
- **generate_text()** (10 connections) — `backend\app\services\gemini_service.py`
- **generate_insight_narrative()** (9 connections) — `backend\app\services\gemini_service.py`
- **gemini_service.py** (8 connections) — `backend\app\services\gemini_service.py`
- **test_gemini_service.py** (8 connections) — `backend\tests\test_gemini_service.py`
- **_get_client()** (7 connections) — `backend\app\services\firestore_service.py`
- **chat_with_coach()** (7 connections) — `backend\app\services\gemini_service.py`
- **list_documents()** (6 connections) — `backend\app\services\firestore_service.py`
- **generate_challenge_suggestion()** (6 connections) — `backend\app\services\gemini_service.py`
- **generate_text_stream()** (6 connections) — `backend\app\services\gemini_service.py`
- **parse_conversational_log()** (6 connections) — `backend\app\services\gemini_service.py`
- **config.py** (5 connections) — `backend\app\core\config.py`
- **delete_document()** (5 connections) — `backend\app\services\firestore_service.py`
- **get_profile()** (5 connections) — `backend\app\services\firestore_service.py`
- **_mock_path()** (5 connections) — `backend\app\services\firestore_service.py`
- **get_daily_log()** (4 connections) — `backend\app\services\firestore_service.py`
- **get_insight()** (4 connections) — `backend\app\services\firestore_service.py`
- **save_daily_log()** (4 connections) — `backend\app\services\firestore_service.py`
- **save_insight()** (4 connections) — `backend\app\services\firestore_service.py`
- **update_challenge_status()** (4 connections) — `backend\app\services\firestore_service.py`
- **upsert_profile()** (4 connections) — `backend\app\services\firestore_service.py`
- *... and 48 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\api\health.py`
- `backend\app\api\insights.py`
- `backend\app\core\config.py`
- `backend\app\services\firestore_service.py`
- `backend\app\services\gemini_service.py`
- `backend\tests\test_gemini_service.py`

## Audit Trail

- EXTRACTED: 189 (60%)
- INFERRED: 124 (40%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*