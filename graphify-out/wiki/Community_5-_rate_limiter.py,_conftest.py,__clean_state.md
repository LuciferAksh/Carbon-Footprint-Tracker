# Community 5: rate_limiter.py, conftest.py, _clean_state

> 28 nodes · cohesion 0.08

## Key Concepts

- **check_rate_limit()** (9 connections) — `backend\app\core\rate_limiter.py`
- **TestRateLimiter** (6 connections) — `backend\tests\test_gemini_service.py`
- **rate_limiter.py** (4 connections) — `backend\app\core\rate_limiter.py`
- **conftest.py** (4 connections) — `backend\tests\conftest.py`
- **_clean_state()** (4 connections) — `backend\tests\conftest.py`
- **clear_all_rate_limits()** (4 connections) — `backend\app\core\rate_limiter.py`
- **.test_reset_clears_limit()** (4 connections) — `backend\tests\test_gemini_service.py`
- **client()** (3 connections) — `backend\tests\conftest.py`
- **reset_rate_limit()** (3 connections) — `backend\app\core\rate_limiter.py`
- **_reset_rate_limits()** (3 connections) — `backend\tests\test_gemini_service.py`
- **.test_different_users_independent()** (3 connections) — `backend\tests\test_gemini_service.py`
- **.test_first_call_passes()** (3 connections) — `backend\tests\test_gemini_service.py`
- **.test_rapid_second_call_raises_429()** (3 connections) — `backend\tests\test_gemini_service.py`
- **_override_get_current_user()** (2 connections) — `backend\tests\conftest.py`
- **Per-user rate limiter for Gemini API calls.  Enforces a minimum interval of ``RA** (2 connections) — `backend\app\core\rate_limiter.py`
- **Raise ``429 Too Many Requests`` if the user is calling too fast.      Args:** (2 connections) — `backend\app\core\rate_limiter.py`
- **Remove the rate-limit record for *uid* (useful in tests).      Args:         uid** (2 connections) — `backend\app\core\rate_limiter.py`
- **Wipe every rate-limit record (test-only helper).** (2 connections) — `backend\app\core\rate_limiter.py`
- **Pytest configuration and shared fixtures for the CarbonCoach test suite.  All te** (1 connections) — `backend\tests\conftest.py`
- **Override the auth dependency to always return the test user.** (1 connections) — `backend\tests\conftest.py`
- **Reset all in-memory stores before each test.** (1 connections) — `backend\tests\conftest.py`
- **Provide an async HTTP client bound to the FastAPI app.      Usage in tests::** (1 connections) — `backend\tests\conftest.py`
- **Different users have independent rate limits.** (1 connections) — `backend\tests\test_gemini_service.py`
- **``reset_rate_limit`` allows immediate re-call.** (1 connections) — `backend\tests\test_gemini_service.py`
- **Clear rate limits before and after each test.** (1 connections) — `backend\tests\test_gemini_service.py`
- *... and 3 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\core\rate_limiter.py`
- `backend\tests\conftest.py`
- `backend\tests\test_gemini_service.py`

## Audit Trail

- EXTRACTED: 50 (68%)
- INFERRED: 23 (32%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*