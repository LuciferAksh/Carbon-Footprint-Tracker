# Community 4: embedding_service.py, vector_search.py, test_embedding_service.py

> 28 nodes · cohesion 0.10

## Key Concepts

- **embed_text()** (8 connections) — `backend\app\services\embedding_service.py`
- **vector_search.py** (6 connections) — `backend\app\services\vector_search.py`
- **embed_texts()** (6 connections) — `backend\app\services\embedding_service.py`
- **search()** (6 connections) — `backend\app\services\vector_search.py`
- **embedding_service.py** (5 connections) — `backend\app\services\embedding_service.py`
- **upsert()** (5 connections) — `backend\app\services\vector_search.py`
- **_get_embedding_model()** (4 connections) — `backend\app\services\embedding_service.py`
- **_mock_embedding()** (4 connections) — `backend\app\services\embedding_service.py`
- **test_upsert_and_search()** (3 connections) — `backend\tests\test_vector_search.py`
- **clear_index()** (3 connections) — `backend\app\services\vector_search.py`
- **_cosine_similarity()** (3 connections) — `backend\app\services\vector_search.py`
- **VectorRecord** (3 connections) — `backend\app\services\vector_search.py`
- **test_embedding_service.py** (2 connections) — `backend\tests\test_embedding_service.py`
- **test_vector_search.py** (2 connections) — `backend\tests\test_vector_search.py`
- **Embedding service – generates text embeddings via Vertex AI or mock.  Used by th** (2 connections) — `backend\app\services\embedding_service.py`
- **Lazily initialise the Vertex AI text-embedding model.** (2 connections) — `backend\app\services\embedding_service.py`
- **Deterministic mock embedding based on a hash of the input text.      Returns a l** (2 connections) — `backend\app\services\embedding_service.py`
- **Return the embedding vector for *text*.      Args:         text: Input string.** (2 connections) — `backend\app\services\embedding_service.py`
- **Batch-embed multiple strings.      Args:         texts: List of input strings.** (2 connections) — `backend\app\services\embedding_service.py`
- **test_embed_text()** (2 connections) — `backend\tests\test_embedding_service.py`
- **test_embed_texts()** (2 connections) — `backend\tests\test_embedding_service.py`
- **_clean_index()** (2 connections) — `backend\tests\test_vector_search.py`
- **Lightweight in-memory vector search.  Stores embeddings alongside metadata and s** (1 connections) — `backend\app\services\vector_search.py`
- **Remove all records from the in-memory index (test helper).** (1 connections) — `backend\app\services\vector_search.py`
- **A single record in the vector store.      Attributes:         id: Unique identif** (1 connections) — `backend\app\services\vector_search.py`
- *... and 3 more nodes in this community*

## Relationships

- No strong cross-community connections detected

## Source Files

- `backend\app\services\embedding_service.py`
- `backend\app\services\vector_search.py`
- `backend\tests\test_embedding_service.py`
- `backend\tests\test_vector_search.py`

## Audit Trail

- EXTRACTED: 60 (73%)
- INFERRED: 22 (27%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*