"""
Unit tests for the real-API (non-mock) code paths in CarbonCoach services.

All Google Cloud, Firebase Admin, and external HTTP calls are fully mocked.
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch
import pytest
from fastapi import HTTPException, Request
from httpx import AsyncClient

from app.core.config import Settings
import app.core.security as security
import app.services.embedding_service as embedding_service
import app.services.firestore_service as firestore_service
import app.services.gemini_service as gemini_service

# ── Mock Classes for Google Cloud / Firebase ──

class MockDocumentReference:
    def __init__(self, path):
        self.path = path
    def set(self, data, merge=True):
        pass
    def get(self):
        return MockDocumentSnapshot(self.path, {"title": "Test Challenge", "co2SavingKg": 5.0})
    def delete(self):
        pass

class MockDocumentSnapshot:
    def __init__(self, path, data, doc_id="doc-id"):
        self.path = path
        self._data = data
        self.exists = True
        self.id = doc_id
    def to_dict(self):
        return self._data

class MockCollectionReference:
    def __init__(self, path):
        self.path = path
    def stream(self):
        return [MockDocumentSnapshot(self.path + "/doc1", {"title": "C1"}, doc_id="doc1")]

class MockFirestoreClient:
    def __init__(self, project=None):
        self.project = project
    def document(self, path):
        return MockDocumentReference(path)
    def collection(self, path):
        return MockCollectionReference(path)

class MockEmbeddingValue:
    def __init__(self, values):
        self.values = values

class MockTextEmbeddingModel:
    @classmethod
    def from_pretrained(cls, name):
        return cls()
    def get_embeddings(self, texts):
        return [MockEmbeddingValue([0.1, 0.2, 0.3]) for _ in texts]

class MockGenerativeModel:
    def __init__(self, model_name, system_instruction=None):
        self.model_name = model_name
        self.system_instruction = system_instruction
    def generate_content(self, prompt, stream=False):
        if stream:
            return [MockGenerateContentResponse("Word1 "), MockGenerateContentResponse("Word2")]
        return MockGenerateContentResponse("Response Text")

class MockGenerateContentResponse:
    def __init__(self, text):
        self.text = text

# Mock Response for HTTPX
class MockHttpxResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")
    def json(self):
        return self._json_data

class MockHttpxClient:
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    async def post(self, url, json=None, headers=None, timeout=None):
        return MockHttpxResponse(200, {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "Gemini API Response"}]
                    }
                }
            ]
        })

# ── Tests for app/core/security.py ──

@pytest.fixture(autouse=True)
def reset_security_globals():
    security._firebase_app_initialized = False
    yield
    security._firebase_app_initialized = False

def test_ensure_firebase_initialized_with_creds():
    settings = Settings(MOCK_AI=False, GOOGLE_APPLICATION_CREDENTIALS="fake_path.json")
    
    mock_firebase = MagicMock()
    mock_firebase._apps = []
    
    with patch.dict(sys.modules, {"firebase_admin": mock_firebase, "firebase_admin.credentials": mock_firebase}):
        security._ensure_firebase_initialized(settings)
        assert mock_firebase.initialize_app.called
        assert security._firebase_app_initialized

def test_ensure_firebase_initialized_with_project_id():
    settings = Settings(MOCK_AI=False, GOOGLE_APPLICATION_CREDENTIALS="", GCP_PROJECT_ID="test-project")
    
    mock_firebase = MagicMock()
    mock_firebase._apps = []
    
    with patch.dict(sys.modules, {"firebase_admin": mock_firebase, "firebase_admin.credentials": mock_firebase}):
        security._ensure_firebase_initialized(settings)
        assert mock_firebase.initialize_app.called
        assert security._firebase_app_initialized

def test_ensure_firebase_initialized_failure():
    settings = Settings(MOCK_AI=False)
    
    mock_firebase = MagicMock()
    mock_firebase._apps = []
    mock_firebase.initialize_app.side_effect = Exception("Failed init")
    
    with patch.dict(sys.modules, {"firebase_admin": mock_firebase, "firebase_admin.credentials": mock_firebase}):
        with pytest.raises(HTTPException) as exc:
            security._ensure_firebase_initialized(settings)
        assert exc.value.status_code == 500

def test_verify_firebase_token_success():
    settings = Settings(MOCK_AI=False)
    
    mock_firebase = MagicMock()
    mock_firebase._apps = [MagicMock()]
    mock_auth = MagicMock()
    mock_auth.verify_id_token.return_value = {"uid": "user123", "email": "user@test.com"}
    mock_firebase.auth = mock_auth
    
    with patch.dict(sys.modules, {
        "firebase_admin": mock_firebase, 
        "firebase_admin.credentials": mock_firebase,
        "firebase_admin.auth": mock_auth
    }):
        claims = security._verify_firebase_token("valid_token", settings)
        assert claims["uid"] == "user123"

def test_verify_firebase_token_failure():
    settings = Settings(MOCK_AI=False)
    
    mock_firebase = MagicMock()
    mock_firebase._apps = [MagicMock()]
    mock_auth = MagicMock()
    mock_auth.verify_id_token.side_effect = Exception("Invalid token")
    mock_firebase.auth = mock_auth
    
    with patch.dict(sys.modules, {
        "firebase_admin": mock_firebase, 
        "firebase_admin.credentials": mock_firebase,
        "firebase_admin.auth": mock_auth
    }):
        with pytest.raises(HTTPException) as exc:
            security._verify_firebase_token("invalid_token", settings)
        assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_no_credentials():
    settings = Settings(MOCK_AI=False)
    request_mock = MagicMock(spec=Request)
    
    with pytest.raises(HTTPException) as exc:
        await security.get_current_user(request_mock, credentials=None, settings=settings)
    assert exc.value.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_with_token():
    settings = Settings(MOCK_AI=False)
    request_mock = MagicMock(spec=Request)
    credentials_mock = MagicMock()
    credentials_mock.credentials = "jwt_token"
    
    mock_firebase = MagicMock()
    mock_firebase._apps = [MagicMock()]
    mock_auth = MagicMock()
    mock_auth.verify_id_token.return_value = {"uid": "user123"}
    mock_firebase.auth = mock_auth
    
    with patch.dict(sys.modules, {
        "firebase_admin": mock_firebase, 
        "firebase_admin.credentials": mock_firebase,
        "firebase_admin.auth": mock_auth
    }):
        user = await security.get_current_user(request_mock, credentials=credentials_mock, settings=settings)
        assert user["uid"] == "user123"


# ── Tests for app/services/embedding_service.py ──

@pytest.mark.asyncio
async def test_embedding_service_real_methods():
    settings = Settings(MOCK_AI=False, GCP_PROJECT_ID="test-proj")
    
    mock_vertexai = MagicMock()
    mock_lang = MagicMock()
    mock_lang.TextEmbeddingModel = MockTextEmbeddingModel
    
    with patch.dict(sys.modules, {
        "vertexai": mock_vertexai,
        "vertexai.language_models": mock_lang
    }):
        # Clean cached model
        embedding_service._embedding_model = None
        
        vec = await embedding_service.embed_text("hello", settings=settings)
        assert vec == [0.1, 0.2, 0.3]
        
        vecs = await embedding_service.embed_texts(["hello", "world"], settings=settings)
        assert vecs == [[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]]


# ── Tests for app/services/firestore_service.py ──

@pytest.mark.asyncio
async def test_firestore_service_real_methods():
    settings = Settings(MOCK_AI=False, GCP_PROJECT_ID="test-proj")
    
    mock_google_cloud = MagicMock()
    mock_google_cloud.firestore.Client = MockFirestoreClient
    
    with patch.dict(sys.modules, {
        "google.cloud": mock_google_cloud,
        "google.cloud.firestore": mock_google_cloud
    }):
        # Clean client
        firestore_service._firestore_client = None
        
        # Test set
        await firestore_service.set_document("col", "doc", {"a": 1}, settings=settings)
        
        # Test get
        doc = await firestore_service.get_document("col", "doc", settings=settings)
        assert doc["title"] == "Test Challenge"
        
        # Test list
        docs = await firestore_service.list_documents("col", settings=settings)
        assert len(docs) == 1
        assert docs[0]["id"] == "doc1"
        
        # Test delete
        await firestore_service.delete_document("col", "doc", settings=settings)


# ── Tests for app/services/gemini_service.py ──

@pytest.mark.asyncio
async def test_gemini_service_real_methods():
    settings = Settings(MOCK_AI=False, GCP_PROJECT_ID="test-proj", GEMINI_API_KEY="fake-api-key", RATE_LIMIT_SECONDS=0)
    
    # 1. Test generate_text with Gemini API Key direct call
    with patch("httpx.AsyncClient", return_value=MockHttpxClient()):
        res = await gemini_service.generate_text("prompt", uid="user123", settings=settings)
        assert res == "Gemini API Response"

        # 2. Test generate_text_stream with Gemini API Key direct call
        chunks = []
        async for chunk in gemini_service.generate_text_stream("prompt", uid="user123", settings=settings):
            chunks.append(chunk)
        assert "".join(chunks).strip() == "Gemini API Response"

    # 3. Test fallback to Vertex AI when API key not present (or failing)
    settings_no_key = Settings(MOCK_AI=False, GCP_PROJECT_ID="test-proj", GEMINI_API_KEY="", RATE_LIMIT_SECONDS=0)
    mock_vertexai = MagicMock()
    mock_gen = MagicMock()
    mock_gen.GenerativeModel = MockGenerativeModel
    
    with patch.dict(sys.modules, {
        "vertexai": mock_vertexai,
        "vertexai.generative_models": mock_gen
    }):
        # Clean cached model
        gemini_service._generative_model = None
        
        res = await gemini_service.generate_text("prompt", uid="user123", settings=settings_no_key)
        assert res == "Response Text"

        # Caching Narrative
        month_data = {
            "month": "2026-06",
            "totalCo2Kg": 150.0,
            "prevMonthCo2Kg": 140.0
        }
        # Mock Firestore get_insight and save_insight
        with patch("app.services.firestore_service.get_insight", return_value=None), \
             patch("app.services.firestore_service.save_insight") as mock_save:
            narrative = await gemini_service.generate_insight_narrative("user123", month_data, settings=settings_no_key)
            assert narrative == "Response Text"
            assert mock_save.called

        # Challenge Suggestion
        with patch("app.services.firestore_service.get_insight", return_value=None):
            # Vertex AI prompt response will return mock JSON if we mock it, or custom mock responses.
            # Let's mock generate_text to return valid JSON
            with patch("app.services.gemini_service.generate_text", return_value='{"title": "Eco Challenge", "co2SavingKg": 4.5}'):
                sugg = await gemini_service.generate_challenge_suggestion("user123", "transport", settings=settings_no_key)
                assert sugg["title"] == "Eco Challenge"
                assert sugg["co2SavingKg"] == 4.5

        # Conversational Log Parsing
        with patch("app.services.gemini_service.generate_text", return_value='{"transport": [{"mode": "bus", "distanceKm": 15.0}], "food": [], "energy": [], "shopping": []}'):
            parsed = await gemini_service.parse_conversational_log("Rode bus for 15km", "user123", settings=settings_no_key)
            assert len(parsed["transport"]) == 1
            assert parsed["transport"][0]["mode"] == "bus"

        # Conversational Chat Coach
        with patch("app.services.gemini_service.generate_text", return_value="Coach response"):
            with patch("app.services.firestore_service.get_profile", return_value={"name": "Alice"}), \
                 patch("app.services.firestore_service.list_daily_logs", return_value=[]):
                chat_reply = await gemini_service.chat_with_coach([{"role": "user", "content": "hi"}], "user123", settings=settings_no_key)
                assert chat_reply == "Coach response"

        # Quiz generation
        with patch("app.services.gemini_service.generate_text", return_value='[{"question": "Q1", "options": ["A", "B", "C", "D"], "correctAnswer": 0, "explanation": "Exp"}]'):
            quiz = await gemini_service.generate_quiz_questions("user123", count=1, settings=settings_no_key)
            assert len(quiz) == 1
            assert quiz[0]["question"] == "Q1"

        # Single quiz question compatibility helper
        with patch("app.services.gemini_service.generate_quiz_questions", return_value=[{"question": "Q1"}]):
            single_q = await gemini_service.generate_quiz_question("user123", settings=settings_no_key)
            assert single_q["question"] == "Q1"

        # Insight Narrative Cache Hit
        with patch("app.services.firestore_service.get_insight", return_value={"narrative": "Cached narrative"}):
            narrative_cached = await gemini_service.generate_insight_narrative("user123", month_data, settings=settings_no_key)
            assert narrative_cached == "Cached narrative"

        # Direct API call exception fallback to Vertex AI
        with patch("httpx.AsyncClient", side_effect=Exception("API Key Network Error")):
            res = await gemini_service.generate_text("prompt", uid="user123", settings=settings)
            assert res == "Response Text"

        # Direct API call HTTP response candidate parse error fallback
        class MockBadHttpxClient:
            async def __aenter__(self): return self
            async def __aexit__(self, exc_type, exc_val, exc_tb): pass
            async def post(self, url, json=None, headers=None, timeout=None):
                return MockHttpxResponse(200, {"candidates": []})
        with patch("httpx.AsyncClient", return_value=MockBadHttpxClient()):
            res = await gemini_service.generate_text("prompt", uid="user123", settings=settings)
            assert res == "Response Text"

        # Offline fallback generation when direct API and Vertex AI fail
        with patch("httpx.AsyncClient", side_effect=Exception("Key Error")), \
             patch("app.services.gemini_service._get_model", side_effect=Exception("Vertex Error")):
            res = await gemini_service.generate_text("prompt", uid="user123", settings=settings)
            assert "progress" in res or "carbon" in res or "sustainability" in res or "work" in res or "CO₂" in res
            
            # Streaming offline fallback
            chunks = []
            async for chunk in gemini_service.generate_text_stream("prompt", uid="user123", settings=settings):
                chunks.append(chunk)
            assert len(chunks) > 0

        # Offline fallback for conversational logs
        parsed_ev = await gemini_service.parse_conversational_log("I drove my EV car for 20 km", "user123", settings=Settings(MOCK_AI=True))
        assert parsed_ev["transport"][0]["mode"] == "car_ev"
        
        parsed_electricity = await gemini_service.parse_conversational_log("We consumed 10 kwh of electricity", "user123", settings=Settings(MOCK_AI=True))
        assert parsed_electricity["energy"][0]["kWh"] == 5.0
        
        parsed_shopping = await gemini_service.parse_conversational_log("Bought some clothes", "user123", settings=Settings(MOCK_AI=True))
        assert parsed_shopping["shopping"][0]["category"] == "clothing"

        # Challenge suggestion invalid JSON fallback
        with patch("app.services.gemini_service.generate_text", return_value="Not a JSON string"):
            sugg_fb = await gemini_service.generate_challenge_suggestion("user123", "energy", settings=settings_no_key)
            assert sugg_fb["category"] == "energy"

        # Conversational chat coach mock mode custom keywords
        settings_mock = Settings(MOCK_AI=True)
        chat_meat = await gemini_service.chat_with_coach([{"role": "user", "content": "I love meat"}], "user123", settings=settings_mock)
        assert "diet" in chat_meat.lower() or "meal" in chat_meat.lower()
        
        chat_default = await gemini_service.chat_with_coach([{"role": "user", "content": "random question"}], "user123", settings=settings_mock)
        assert "coach" in chat_default.lower() or "sustainability" in chat_default.lower() or "carbon" in chat_default.lower()

        # Conversational chat coach real mode chat history formatting
        with patch("app.services.gemini_service.generate_text", return_value="Coach response text"):
            with patch("app.services.firestore_service.get_profile", return_value={"name": "Bob"}), \
                 patch("app.services.firestore_service.list_daily_logs", return_value=[]):
                chat_hist = await gemini_service.chat_with_coach([
                    {"role": "user", "content": "hello"},
                    {"role": "assistant", "content": "hi"},
                    {"role": "user", "content": "tell me more"}
                ], "user123", settings=settings_no_key)
                assert chat_hist == "Coach response text"

        # Parse conversational log real mode invalid JSON fallback
        with patch("app.services.gemini_service.generate_text", return_value="Invalid response"):
            parsed_err = await gemini_service.parse_conversational_log("Log text", "user123", settings=settings_no_key)
            assert parsed_err == {"transport": [], "food": [], "energy": [], "shopping": []}

        # Quiz generation parse error fallback
        with patch("app.services.gemini_service.generate_text", return_value="No list here"):
            quiz_err = await gemini_service.generate_quiz_questions("user123", count=2, settings=settings_no_key)
            assert len(quiz_err) == 2

        # Firestore service mock delete document
        await firestore_service.delete_document("col", "doc", settings=settings_mock)


def test_firestore_mock_client_branch():
    settings = Settings(MOCK_AI=True)
    # _get_client should return None in mock mode
    assert firestore_service._get_client(settings) is None


@pytest.mark.asyncio
async def test_main_lifespan():
    from app.main import lifespan, app
    # Directly exercise lifespan startup and shutdown
    async with lifespan(app):
        pass


@pytest.mark.asyncio
async def test_main_body_size_value_error():
    # Use client fixture to send request with invalid content-length header
    from app.main import app
    from httpx import ASGITransport, AsyncClient
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Pass content-length that is not an integer to trigger ValueError
        headers = {"content-length": "not-a-number"}
        resp = await client.post("/api/v1/onboarding", content="{}", headers=headers)
        # Even with bad content-length, it shouldn't raise 413, but might return 401/422/etc.
        assert resp.status_code != 413


@pytest.mark.asyncio
async def test_insights_monthly_trend_days_branches(client: AsyncClient):
    # Log days in different weeks of the month to hit W1, W2, and W4
    # W1: day <= 7
    await client.post(
        "/api/v1/activity",
        json={"date": "2026-06-05", "transport": [{"mode": "bus", "distanceKm": 1.0}]}
    )
    # W2: day <= 14
    await client.post(
        "/api/v1/activity",
        json={"date": "2026-06-12", "transport": [{"mode": "bus", "distanceKm": 1.0}]}
    )
    # W4: day > 21
    await client.post(
        "/api/v1/activity",
        json={"date": "2026-06-25", "transport": [{"mode": "bus", "distanceKm": 1.0}]}
    )
    # Invalid date day format (raises ValueError in splitting/parsing)
    # We will save it directly via firestore mock since API checks date format
    await firestore_service.save_daily_log(
        uid="test-user-001",
        date_str="2026-06-invalid",
        data={"totalCo2Kg": 5.0}
    )

    resp = await client.get("/api/v1/insights/monthly?month=2026-06")
    assert resp.status_code == 200
    data = resp.json()
    weeks = {item["week"]: item["amount"] for item in data["weeklyTrend"]}
    assert weeks["W1"] > 0
    assert weeks["W2"] > 0
    assert weeks["W4"] > 0


