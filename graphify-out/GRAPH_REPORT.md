# Graph Report - C:\Prompt wars 2  (2026-06-11)

## Corpus Check
- 108 files · ~322,007 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 718 nodes · 1520 edges · 88 communities detected
- Extraction: 44% EXTRACTED · 56% INFERRED · 0% AMBIGUOUS · INFERRED: 848 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]

## God Nodes (most connected - your core abstractions)
1. `Settings` - 117 edges
2. `TransportEntry` - 54 edges
3. `FoodEntry` - 50 edges
4. `ShoppingEntry` - 49 edges
5. `EnergyEntry` - 48 edges
6. `CategoryBreakdown` - 48 edges
7. `ChallengeResponse` - 25 edges
8. `InsightResponse` - 23 edges
9. `WeeklyTrendPoint` - 21 edges
10. `MonthlyReportResponse` - 21 edges

## Surprising Connections (you probably didn't know these)
- `Settings` --uses--> `Firestore service – all database operations in one place.  When ``MOCK_AI=true```  [INFERRED]
  C:\Prompt wars 2\backend\app\core\config.py → backend\app\services\firestore_service.py
- `Settings` --uses--> `Join Firestore-style path segments into a flat key.`  [INFERRED]
  C:\Prompt wars 2\backend\app\core\config.py → C:\Prompt wars 2\backend\app\services\firestore_service.py
- `Settings` --uses--> `Return (or create) a Firestore client.  Skipped in mock mode.`  [INFERRED]
  C:\Prompt wars 2\backend\app\core\config.py → C:\Prompt wars 2\backend\app\services\firestore_service.py
- `Settings` --uses--> `Create or update a Firestore document.      Args:         collection_path: Slash`  [INFERRED]
  C:\Prompt wars 2\backend\app\core\config.py → C:\Prompt wars 2\backend\app\services\firestore_service.py
- `Settings` --uses--> `Fetch a single Firestore document.      Args:         collection_path: Collectio`  [INFERRED]
  C:\Prompt wars 2\backend\app\core\config.py → C:\Prompt wars 2\backend\app\services\firestore_service.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (114): BaseSettings, get_settings(), Application configuration loaded from environment variables.  Uses pydantic-sett, Centralised, validated application settings.      Attributes:         GCP_PROJEC, Return the singleton *Settings* instance (cached after first call)., Settings, List all documents in a collection.      Args:         collection_path: Collecti, List all documents in a collection.      Args:         collection_path: Collecti (+106 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (40): community_labels(), estimate_words(), filter_detection(), is_excluded(), main(), fetchDashboard(), Integration tests for the Activity API.  Exercises the POST (log activities) and, Tests for ``/api/v1/activity``. (+32 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (53): EnergyEntry, FoodEntry, A single transport activity.      Attributes:         mode: Key matching ``const, A single meal entry.      Attributes:         mealType: Key matching ``constants, A single energy-usage entry.      Attributes:         source: Key matching ``con, ShoppingEntry, TransportEntry, calc_daily_total() (+45 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (51): _clean_state(), client(), _override_get_current_user(), Pytest configuration and shared fixtures for the CarbonCoach test suite.  All te, Override the auth dependency to always return the test user., Reset all in-memory stores before each test., Provide an async HTTP client bound to the FastAPI app.      Usage in tests::, clear_mock_store() (+43 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (24): generate_challenge_prompt(), parse_challenge_response(), CarbonCoach — Challenge Generator Logic  Pure business logic for generating week, Generate the Gemini prompt for weekly challenge creation.      Summarizes the us, Parse and validate the Gemini response into a challenge dict.      Handles both, Tests for the CarbonCoach challenge generator logic., Should return None when required fields are missing., Should return None for unparseable responses. (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (34): CategoryBreakdown, ChatMessage, ChatRequest, InsightResponse, MonthlyReportResponse, QuizQuestionResponse, Monthly insight summary generated by Gemini.      Attributes:         month: ``Y, Response model for a dynamically generated quiz question. (+26 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (28): embed_text(), embed_texts(), _get_embedding_model(), _mock_embedding(), Embedding service – generates text embeddings via Vertex AI or mock.  Used by th, Lazily initialise the Vertex AI text-embedding model., Deterministic mock embedding based on a hash of the input text.      Returns a l, Return the embedding vector for *text*.      Args:         text: Input string. (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.26
Nodes (30): ActivityLog, ActivityLogResponse, CommunityAnalyticsPoint, CommunityAnalyticsResponse, DashboardBenchmark, DashboardData, get_activity(), get_community_analytics() (+22 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (30): ChallengeCreate, ChallengeResponse, ChallengeStatusUpdate, complete_challenge(), create_challenge(), _current_week_id(), get_challenge(), get_current_challenge() (+22 more)

### Community 9 - "Community 9"
Cohesion: 0.24
Nodes (16): CarbonProfile, get_profile(), get_profile_compatibility(), OnboardingAnswers, ProfileCreate, ProfileResponse, Pydantic v2 models for user profiles and onboarding., Request body for creating or updating a user profile. (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.27
Nodes (11): addSortIndicators(), enableUI(), getNthColumn(), getTable(), getTableBody(), getTableHeader(), loadColumns(), loadData() (+3 more)

### Community 11 - "Community 11"
Cohesion: 0.35
Nodes (8): a(), B(), D(), g(), i(), k(), Q(), y()

### Community 12 - "Community 12"
Cohesion: 0.22
Nodes (2): MockIntersectionObserver, MockResizeObserver

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (1): CarbonCoach test suite.

### Community 14 - "Community 14"
Cohesion: 0.29
Nodes (5): add_request_id(), lifespan(), limit_body_size(), Application lifespan handler – runs on startup and shutdown.      Logs the curre, test_main_lifespan()

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (1): ErrorBoundary

### Community 16 - "Community 16"
Cohesion: 0.4
Nodes (2): handleSendMessage(), handleSubmit()

### Community 17 - "Community 17"
Cohesion: 0.47
Nodes (4): ApiRequestError, buildHeaders(), getIdToken(), request()

### Community 18 - "Community 18"
Cohesion: 0.7
Nodes (4): goToNext(), goToPrevious(), makeCurrent(), toggleClass()

### Community 19 - "Community 19"
Cohesion: 0.4
Nodes (2): AuthConsumer(), useAuth()

### Community 20 - "Community 20"
Cohesion: 0.67
Nodes (0): 

### Community 21 - "Community 21"
Cohesion: 1.0
Nodes (1): Carbon-emission factor constants.  Every factor is expressed in **kg CO₂e per un

### Community 22 - "Community 22"
Cohesion: 1.0
Nodes (0): 

### Community 23 - "Community 23"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Community 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Community 25"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Community 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Community 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Community 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Community 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Community 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Community 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Community 32"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Community 33"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Community 34"
Cohesion: 1.0
Nodes (1): Return ``True`` when mock mode is active.

### Community 35 - "Community 35"
Cohesion: 1.0
Nodes (1): Parse the JSON-encoded CORS_ORIGINS string into a Python list.

### Community 36 - "Community 36"
Cohesion: 1.0
Nodes (1): ``generate_text`` returns the mock narrative in mock mode.

### Community 37 - "Community 37"
Cohesion: 1.0
Nodes (1): ``generate_text_stream`` yields multiple chunks.

### Community 38 - "Community 38"
Cohesion: 1.0
Nodes (1): ``generate_insight_narrative`` returns a narrative and caches it.

### Community 39 - "Community 39"
Cohesion: 1.0
Nodes (1): ``generate_challenge_suggestion`` returns a valid challenge dict.

### Community 40 - "Community 40"
Cohesion: 1.0
Nodes (0): 

### Community 41 - "Community 41"
Cohesion: 1.0
Nodes (0): 

### Community 42 - "Community 42"
Cohesion: 1.0
Nodes (0): 

### Community 43 - "Community 43"
Cohesion: 1.0
Nodes (0): 

### Community 44 - "Community 44"
Cohesion: 1.0
Nodes (0): 

### Community 45 - "Community 45"
Cohesion: 1.0
Nodes (0): 

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (0): 

### Community 47 - "Community 47"
Cohesion: 1.0
Nodes (0): 

### Community 48 - "Community 48"
Cohesion: 1.0
Nodes (0): 

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (0): 

### Community 50 - "Community 50"
Cohesion: 1.0
Nodes (0): 

### Community 51 - "Community 51"
Cohesion: 1.0
Nodes (0): 

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (0): 

### Community 53 - "Community 53"
Cohesion: 1.0
Nodes (0): 

### Community 54 - "Community 54"
Cohesion: 1.0
Nodes (0): 

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (0): 

### Community 56 - "Community 56"
Cohesion: 1.0
Nodes (0): 

### Community 57 - "Community 57"
Cohesion: 1.0
Nodes (0): 

### Community 58 - "Community 58"
Cohesion: 1.0
Nodes (0): 

### Community 59 - "Community 59"
Cohesion: 1.0
Nodes (0): 

### Community 60 - "Community 60"
Cohesion: 1.0
Nodes (0): 

### Community 61 - "Community 61"
Cohesion: 1.0
Nodes (0): 

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (0): 

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (0): 

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (0): 

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (0): 

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (0): 

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (0): 

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (0): 

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (0): 

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (0): 

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (0): 

### Community 72 - "Community 72"
Cohesion: 1.0
Nodes (0): 

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (0): 

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (0): 

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (0): 

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (0): 

### Community 77 - "Community 77"
Cohesion: 1.0
Nodes (0): 

### Community 78 - "Community 78"
Cohesion: 1.0
Nodes (0): 

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (0): 

### Community 80 - "Community 80"
Cohesion: 1.0
Nodes (0): 

### Community 81 - "Community 81"
Cohesion: 1.0
Nodes (0): 

### Community 82 - "Community 82"
Cohesion: 1.0
Nodes (0): 

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (0): 

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (0): 

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (1): Return ``True`` when mock mode is active.

### Community 86 - "Community 86"
Cohesion: 1.0
Nodes (1): Parse the JSON-encoded CORS_ORIGINS string into a Python list.

### Community 87 - "Community 87"
Cohesion: 1.0
Nodes (1): Return the singleton *Settings* instance (cached after first call).

## Knowledge Gaps
- **127 isolated node(s):** `Application lifespan handler – runs on startup and shutdown.      Logs the curre`, `Carbon-emission factor constants.  Every factor is expressed in **kg CO₂e per un`, `Application configuration loaded from environment variables.  Uses pydantic-sett`, `Centralised, validated application settings.      Attributes:         GCP_PROJEC`, `Return ``True`` when mock mode is active.` (+122 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 21`** (2 nodes): `emissions.py`, `Carbon-emission factor constants.  Every factor is expressed in **kg CO₂e per un`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 22`** (2 nodes): `vite.config.ts`, `manualChunks()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 23`** (2 nodes): `RouteFallback()`, `App.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 24`** (2 nodes): `LogScreen.tsx`, `handleParseText()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 25`** (2 nodes): `ChallengeDetail.tsx`, `fetchChallenge()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 26`** (2 nodes): `OnboardingQuiz.tsx`, `handleKeyDown()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 27`** (2 nodes): `ProfileResult.tsx`, `useCountUp()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 28`** (2 nodes): `ProfileScreen.tsx`, `getCarbonGrade()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 29`** (2 nodes): `MonthlyReport.tsx`, `fetchReport()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (2 nodes): `calculateEmissions()`, `carbon-constants.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (2 nodes): `useFocusOnRouteChange.ts`, `useFocusOnRouteChange()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (2 nodes): `Toast.test.tsx`, `TestComponent()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (1 nodes): `Return ``True`` when mock mode is active.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (1 nodes): `Parse the JSON-encoded CORS_ORIGINS string into a Python list.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (1 nodes): ```generate_text`` returns the mock narrative in mock mode.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 37`** (1 nodes): ```generate_text_stream`` yields multiple chunks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 38`** (1 nodes): ```generate_insight_narrative`` returns a narrative and caches it.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (1 nodes): ```generate_challenge_suggestion`` returns a valid challenge dict.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (1 nodes): `cypress.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (1 nodes): `eslint.config.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (1 nodes): `vitest.config.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (1 nodes): `smoke.cy.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (1 nodes): `sw.js`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (1 nodes): `main.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (1 nodes): `vite-env.d.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (1 nodes): `BarChart.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (1 nodes): `DonutChart.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 50`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (1 nodes): `LoadingSpinner.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (1 nodes): `AppShell.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (1 nodes): `BottomNav.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (1 nodes): `Badge.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (1 nodes): `Button.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `Card.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `Input.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (1 nodes): `ProgressBar.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (1 nodes): `Select.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (1 nodes): `Skeleton.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (1 nodes): `Toast.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `LoginScreen.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `ProtectedRoute.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `firebase.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `api.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (1 nodes): `Button.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (1 nodes): `carbon-constants.test.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 77`** (1 nodes): `Card.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 78`** (1 nodes): `ChallengesScreen.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (1 nodes): `CoachScreen.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 80`** (1 nodes): `LogScreen.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 81`** (1 nodes): `OnboardingQuiz.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 82`** (1 nodes): `ProgressBar.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (1 nodes): `ProtectedRoute.test.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (1 nodes): `index.ts`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (1 nodes): `Return ``True`` when mock mode is active.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 86`** (1 nodes): `Parse the JSON-encoded CORS_ORIGINS string into a Python list.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 87`** (1 nodes): `Return the singleton *Settings* instance (cached after first call).`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Settings` connect `Community 0` to `Community 3`, `Community 5`, `Community 6`, `Community 7`, `Community 8`?**
  _High betweenness centrality (0.234) - this node is a cross-community bridge._
- **Why does `generate_challenge_prompt()` connect `Community 4` to `Community 1`, `Community 3`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `CategoryBreakdown` connect `Community 5` to `Community 8`, `Community 7`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 113 inferred relationships involving `Settings` (e.g. with `Pydantic v2 models for daily activity logging.  Covers all four emission categor` and `Calculate emissions for the submitted activities and save them.`) actually correct?**
  _`Settings` has 113 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `TransportEntry` (e.g. with `TestCalcTransport` and `TestCalcFood`) actually correct?**
  _`TransportEntry` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 47 inferred relationships involving `FoodEntry` (e.g. with `TestCalcTransport` and `TestCalcFood`) actually correct?**
  _`FoodEntry` has 47 INFERRED edges - model-reasoned connections that need verification._
- **Are the 46 inferred relationships involving `ShoppingEntry` (e.g. with `TestCalcTransport` and `TestCalcFood`) actually correct?**
  _`ShoppingEntry` has 46 INFERRED edges - model-reasoned connections that need verification._