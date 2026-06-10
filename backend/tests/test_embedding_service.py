import pytest
from app.services import embedding_service

@pytest.mark.asyncio
async def test_embed_text():
    vec = await embedding_service.embed_text("test")
    assert isinstance(vec, list)
    assert len(vec) == 256
    assert all(isinstance(x, float) for x in vec)

@pytest.mark.asyncio
async def test_embed_texts():
    vecs = await embedding_service.embed_texts(["hello", "world"])
    assert len(vecs) == 2
    assert len(vecs[0]) == 256
