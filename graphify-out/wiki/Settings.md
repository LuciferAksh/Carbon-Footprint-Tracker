# Settings

> God node · 46 connections · `backend\app\core\config.py`

## Connections by Relation

### calls
- [[get_settings()]] `EXTRACTED`

### contains
- [[config.py]] `EXTRACTED`

### inherits
- [[BaseSettings]] `EXTRACTED`

### rationale_for
- [[Centralised, validated application settings.      Attributes:         GCP_PROJEC]] `EXTRACTED`

### uses
- [[Health-check endpoint.  Returns basic service status and configuration info.  Th]] `INFERRED`
- [[Return a lightweight health payload.      Includes:     * ``status`` – always ``]] `INFERRED`
- [[Per-user rate limiter for Gemini API calls.  Enforces a minimum interval of ``RA]] `INFERRED`
- [[Raise ``429 Too Many Requests`` if the user is calling too fast.      Args:]] `INFERRED`
- [[Remove the rate-limit record for *uid* (useful in tests).      Args:         uid]] `INFERRED`
- [[Wipe every rate-limit record (test-only helper).]] `INFERRED`
- [[Firebase ID-token verification middleware.  Provides a FastAPI dependency ``get_]] `INFERRED`
- [[Initialise the Firebase Admin SDK exactly once.      Skipped entirely when mock]] `INFERRED`
- [[Verify a Firebase ID token and return the decoded claims.      Args:         tok]] `INFERRED`
- [[FastAPI dependency that returns the authenticated user's claims.      In **mock]] `INFERRED`
- [[Embedding service – generates text embeddings via Vertex AI or mock.  Used by th]] `INFERRED`
- [[Lazily initialise the Vertex AI text-embedding model.]] `INFERRED`
- [[Deterministic mock embedding based on a hash of the input text.      Returns a l]] `INFERRED`
- [[Return the embedding vector for *text*.      Args:         text: Input string.]] `INFERRED`
- [[Batch-embed multiple strings.      Args:         texts: List of input strings.]] `INFERRED`
- [[Firestore service – all database operations in one place.  When ``MOCK_AI=true``]] `INFERRED`
- [[Join Firestore-style path segments into a flat key.]] `INFERRED`
- [[Return (or create) a Firestore client.  Skipped in mock mode.]] `INFERRED`
- [[Create or update a Firestore document.      Args:         collection_path: Slash]] `INFERRED`
- [[Fetch a single Firestore document.      Args:         collection_path: Collectio]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*