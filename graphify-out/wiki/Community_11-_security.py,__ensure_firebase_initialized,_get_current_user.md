# Community 11: security.py, _ensure_firebase_initialized, get_current_user

> 8 nodes · cohesion 0.32

## Key Concepts

- **security.py** (4 connections) — `backend\app\core\security.py`
- **_verify_firebase_token()** (4 connections) — `backend\app\core\security.py`
- **_ensure_firebase_initialized()** (3 connections) — `backend\app\core\security.py`
- **get_current_user()** (3 connections) — `backend\app\core\security.py`
- **Firebase ID-token verification middleware.  Provides a FastAPI dependency ``get_** (2 connections) — `backend\app\core\security.py`
- **FastAPI dependency that returns the authenticated user's claims.      In **mock** (2 connections) — `backend\app\core\security.py`
- **Initialise the Firebase Admin SDK exactly once.      Skipped entirely when mock** (2 connections) — `backend\app\core\security.py`
- **Verify a Firebase ID token and return the decoded claims.      Args:         tok** (2 connections) — `backend\app\core\security.py`

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\core\security.py`

## Audit Trail

- EXTRACTED: 18 (82%)
- INFERRED: 4 (18%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*