# test_profile.py, Integration tests for the Profile API.  Uses the async HTTP client fixture from, Tests for ``/api/v1/profile``.

> 14 nodes · cohesion 0.14

## Key Concepts

- **TestProfileAPI** (7 connections) — `backend\tests\test_profile.py`
- **test_profile.py** (2 connections) — `backend\tests\test_profile.py`
- **.test_create_profile()** (2 connections) — `backend\tests\test_profile.py`
- **.test_get_profile_after_create()** (2 connections) — `backend\tests\test_profile.py`
- **.test_get_profile_not_found()** (2 connections) — `backend\tests\test_profile.py`
- **.test_onboarding_calculation()** (2 connections) — `backend\tests\test_profile.py`
- **.test_update_profile_merges()** (2 connections) — `backend\tests\test_profile.py`
- **Integration tests for the Profile API.  Uses the async HTTP client fixture from** (1 connections) — `backend\tests\test_profile.py`
- **Tests for ``/api/v1/profile``.** (1 connections) — `backend\tests\test_profile.py`
- **POST creates a profile and returns 201.** (1 connections) — `backend\tests\test_profile.py`
- **GET before creating returns 404.** (1 connections) — `backend\tests\test_profile.py`
- **GET after creating returns the profile.** (1 connections) — `backend\tests\test_profile.py`
- **A second POST merges fields into the existing profile.** (1 connections) — `backend\tests\test_profile.py`
- **POST /api/v1/onboarding calculates and returns carbon profile.** (1 connections) — `backend\tests\test_profile.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\tests\test_profile.py`

## Audit Trail

- EXTRACTED: 26 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*