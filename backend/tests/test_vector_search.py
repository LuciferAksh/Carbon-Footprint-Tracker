import pytest
from app.services import vector_search

@pytest.fixture(autouse=True)
def _clean_index():
    vector_search.clear_index()
    yield
    vector_search.clear_index()

@pytest.mark.asyncio
async def test_upsert_and_search():
    await vector_search.upsert("rec1", "electric vehicle carbon footprint", {"category": "transport"})
    await vector_search.upsert("rec2", "plant-based diet beef substitution", {"category": "food"})

    results = await vector_search.search("climate impact of eating meat", top_k=2)
    assert len(results) == 2
    ids = [r["id"] for r in results]
    assert "rec1" in ids
    assert "rec2" in ids
    assert -1.0 <= results[0]["score"] <= 1.0

@pytest.mark.asyncio
async def test_search_empty_index():
    results = await vector_search.search("some query")
    assert results == []

def test_cosine_similarity_zero_vector():
    from app.services.vector_search import _cosine_similarity
    assert _cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


