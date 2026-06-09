# CarbonCoach — Project Context for AI Continuation

> **Purpose:** This file contains everything a new AI model needs to understand the project
> and continue development from the current state. Read this FIRST before making any changes.

---

## 1. What Is CarbonCoach?

An AI-powered carbon footprint tracker built for **Google Prompt Wars**.
Users track daily transport, food, energy, and shopping activities,
get Gemini AI tips, participate in weekly challenges, and view monthly reports.

**Demo:** Run locally with `VITE_DEMO_MODE=true` (no Firebase project needed).

---

## 2. Tech Stack (All Google)

| Layer           | Technology                          | Location          |
|-----------------|-------------------------------------|-------------------|
| Frontend        | React 19, TypeScript 6, Vite 8      | `frontend/`       |
| Styling         | Tailwind CSS v4 (CSS-first config)  | `frontend/src/index.css` |
| Animations      | Framer Motion                       | Throughout screens |
| Charts          | Chart.js + react-chartjs-2          | `components/charts/` |
| Auth            | Firebase Auth (Google Sign-In)      | `features/auth/`  |
| Backend         | FastAPI, Python 3.11                | `backend/`        |
| Database        | Firestore                           | via backend       |
| AI              | Vertex AI Gemini (2.0 Flash/1.5 Pro)| `services/gemini_service.py` |
| Embeddings      | text-embedding-004                  | `services/embedding_service.py` |
| Cron            | Cloud Functions + Cloud Scheduler   | `functions/`      |
| IaC             | Terraform                           | `terraform/`      |
| CI              | GitHub Actions                      | `.github/workflows/ci.yml` |

---

## 3. Project Structure

```
Prompt wars 2/
├── backend/                    # FastAPI backend (Python 3.11)
│   ├── app/
│   │   ├── api/                # Route handlers
│   │   │   ├── health.py       # GET /health
│   │   │   ├── profile.py      # /api/v1/users/*
│   │   │   ├── activity.py     # /api/v1/activity/*
│   │   │   ├── challenge.py    # /api/v1/challenge/*
│   │   │   └── insights.py     # /api/v1/insights/*
│   │   ├── core/
│   │   │   ├── config.py       # pydantic-settings, env vars, MOCK_AI
│   │   │   ├── security.py     # Firebase ID token verification middleware
│   │   │   └── rate_limiter.py # Per-user Gemini call rate limit (5s)
│   │   ├── models/             # Pydantic request/response models
│   │   ├── services/
│   │   │   ├── carbon_calculator.py  # Pure CO2 math functions
│   │   │   ├── gemini_service.py     # Gemini AI (streaming + mock mode)
│   │   │   ├── firestore_service.py  # Firestore CRUD
│   │   │   ├── embedding_service.py  # text-embedding-004
│   │   │   └── vector_search.py      # Vertex AI Vector Search
│   │   ├── constants/emissions.py    # Emission factor data
│   │   └── main.py             # FastAPI app, CORS, router registration
│   ├── tests/                  # pytest tests (mock Firebase + Gemini)
│   ├── Dockerfile              # Multi-stage Python 3.11-slim
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # React + Vite + Tailwind v4
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/             # Button, Card, Badge, Input, Select, ProgressBar, Skeleton, Toast
│   │   │   ├── charts/         # BarChart, DonutChart (Chart.js dark theme)
│   │   │   ├── layout/         # AppShell (with Outlet), BottomNav (4 tabs)
│   │   │   └── feedback/       # ErrorBoundary, LoadingSpinner
│   │   ├── features/
│   │   │   ├── auth/           # AuthProvider (demo mode support), LoginScreen, ProtectedRoute
│   │   │   ├── onboarding/     # OnboardingQuiz (6-step, Framer Motion), ProfileResult
│   │   │   ├── dashboard/      # DashboardScreen (CO2 counter, charts, benchmark)
│   │   │   ├── activity-log/   # LogScreen (4 category tiles, CO2 preview, AI tip)
│   │   │   ├── challenges/     # ChallengesScreen, ChallengeDetail
│   │   │   ├── reports/        # MonthlyReport (Gemini narrative, share)
│   │   │   └── profile/        # ProfileScreen (avatar, badges, settings)
│   │   ├── lib/
│   │   │   ├── firebase.ts     # Firebase config from VITE_FIREBASE_* env vars
│   │   │   ├── api.ts          # API client with auto Firebase ID token injection
│   │   │   └── carbon-constants.ts # Emission factors, types, calculateEmissions()
│   │   ├── types/index.ts      # All TypeScript interfaces
│   │   ├── App.tsx             # Routes with React.lazy + ErrorBoundary on every route
│   │   ├── main.tsx            # Entry: StrictMode > BrowserRouter > AuthProvider > ToastProvider > App
│   │   └── index.css           # Tailwind v4 @theme tokens, glassmorphism, animations
│   ├── vite.config.ts          # React plugin, Tailwind plugin, proxy /api -> :8000, vendor chunks
│   ├── tsconfig.json           # strict: true, @/* path alias
│   ├── index.html              # SEO meta, skip-to-content, React entry
│   └── .env.local              # VITE_DEMO_MODE=true + placeholder Firebase config
│
├── functions/                  # Cloud Functions (Gen2, Python 3.11)
│   ├── main.py                 # Pub/Sub trigger entry point
│   ├── challenge_generator.py  # Weekly challenge generation logic
│   └── tests/
│
├── terraform/                  # Infrastructure as Code
│   ├── main.tf                 # Provider, project config
│   ├── variables.tf            # Input variables
│   ├── cloud_run.tf            # Cloud Run service
│   ├── scheduler.tf            # Cloud Scheduler + Pub/Sub topic
│   ├── bigquery.tf             # Analytics dataset + tables
│   ├── secrets.tf              # Secret Manager
│   └── outputs.tf              # Output values
│
├── firebase.json               # Firebase Hosting config
├── firestore.rules             # Firestore security rules (user isolation)
├── firestore.indexes.json      # Composite indexes
├── .github/workflows/ci.yml    # CI: lint → typecheck → test (80% cov) → build
└── README.md
```

---

## 4. How to Run Locally

### Frontend (port 5173)
```bash
cd frontend
npm install              # already done
npm run dev              # Vite dev server at http://localhost:5173
```

### Backend (port 8000)
```bash
cd backend
python -m venv venv                     # already done
.\venv\Scripts\activate                 # Windows
pip install -r requirements.txt         # already done
uvicorn app.main:app --reload --port 8000
```

### Environment
- `frontend/.env.local` has `VITE_DEMO_MODE=true` — bypasses Firebase Auth entirely
- `backend/.env` has `MOCK_AI=true` — all Gemini/Firestore calls return mock data
- Vite proxy forwards `/api` requests to `http://localhost:8000`

---

## 5. Current State (as of June 8, 2026)

### ✅ DONE
- [x] Full backend API (5 route modules, 5 services, 3 model modules, tests)
- [x] Full frontend (9 screens, 12 UI components, routing, lazy loading)
- [x] Demo mode auth (bypass Firebase for local dev)
- [x] Cloud Functions (weekly challenge cron)
- [x] Terraform IaC (Cloud Run, Scheduler, BigQuery, Secrets)
- [x] CI pipeline (GitHub Actions)
- [x] TypeScript compiles with ZERO errors
- [x] Vite build succeeds (305ms, optimized vendor chunks)

### ❌ NOT DONE (next tasks)
- [ ] **Frontend unit tests** — Add Vitest + tests for hooks and components
- [ ] **E2E test stubs** — Set up Cypress for the core demo loop
- [ ] **Deploy** — `terraform apply`, `firebase deploy`, `gcloud run deploy`
- [ ] **Real Firebase project** — Create project, enable Google Sign-In, set real env vars
- [ ] **Google Maps integration** — Route-based carbon visualization (planned feature)
- [ ] **Community benchmarking** — BigQuery aggregate queries (backend exists, UI placeholder)

### ⚠️ KNOWN ISSUES
- Backend API routes use `/api/v1/` prefix but frontend API client calls `/api/` without `v1` — 
  the Vite proxy sends to `:8000` which doesn't have `/api/` routes at root level. 
  **Fix needed:** Either update `api.ts` to use `/api/v1` or add a route prefix in FastAPI.
- LoginScreen `Icon` uses dynamic Tailwind classes like `w-[${size}px]` which won't work 
  with Tailwind's JIT compiler (needs safelist or fixed classes). Cosmetic only.

---

## 6. Key Architecture Decisions

1. **Monorepo** — Single repo with `frontend/`, `backend/`, `functions/`, `terraform/`
2. **Feature-based frontend** — Each screen is in `features/<name>/` with barrel exports
3. **Mock mode everywhere** — Both backend (`MOCK_AI=true`) and frontend (`VITE_DEMO_MODE=true`) 
   can run without any cloud services
4. **Tailwind v4 CSS-first** — Design tokens in `@theme` block in `index.css`, NOT `tailwind.config.js`
5. **Dark mode only** — No light mode toggle; dark theme with green primary (#16A34A)
6. **Component exports** — UI components use `export default` with barrel re-exports via `index.ts`
   (import from `@/components/ui` for named imports, or directly for default)
7. **Demo auth** — `AuthProvider` checks `VITE_DEMO_MODE` env var; when true, uses a fake 
   `DEMO_USER` object and `localStorage` for session persistence

---

## 7. API Routes (Backend)

| Method | Path                          | Purpose                        |
|--------|-------------------------------|--------------------------------|
| GET    | `/health`                     | Health check                   |
| GET    | `/api/v1/users/me`            | Get current user profile       |
| POST   | `/api/v1/users/onboarding`    | Submit onboarding answers      |
| POST   | `/api/v1/activity/log`        | Log an activity + get AI tip   |
| GET    | `/api/v1/activity/summary`    | Weekly/monthly summary         |
| GET    | `/api/v1/challenge/current`   | Get current week's challenge   |
| GET    | `/api/v1/challenge/list`      | List all challenges            |
| PATCH  | `/api/v1/challenge/:id/complete` | Mark challenge complete     |
| GET    | `/api/v1/insights/monthly`    | Monthly report with AI narrative |

---

## 8. Design System Quick Reference

### Colors (defined in `index.css` @theme)
- Primary: `primary-50` to `primary-950` (green scale, accent = `#16A34A`)
- Dark: `dark-50` to `dark-950` (slate scale, bg = `#020617`)
- Semantic: `success`, `warning`, `error`, `info`
- Category: `transport` (#3b82f6), `food` (#f59e0b), `energy` (#a855f7), `shopping` (#ec4899)

### CSS Utilities (custom classes in `index.css`)
- `.glass` — Dark glassmorphism with blur
- `.glass-light` — Lighter glass variant
- `.glass-primary` — Green-tinted glass
- `.gradient-primary` — Green gradient
- `.gradient-dark` — Dark vertical gradient
- `.gradient-radial` — Radial green glow from top

### Animations
- `animate-fade-in`, `animate-slide-up`, `animate-pulse-glow`, `animate-float`

---

## 9. Commands Reference

```bash
# Frontend
cd frontend
npm run dev              # Dev server on :5173
npm run build            # Production build (tsc + vite build)
npx tsc --noEmit         # Type check only
npx vite build           # Build only (skip tsc)

# Backend
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000   # Dev server
pytest -v                                    # Run tests
pytest --cov=app --cov-report=term           # Coverage

# Cloud Functions
cd functions
pytest tests/                                # Test challenge generator

# Infrastructure
cd terraform
terraform init
terraform plan
terraform apply
```

---

## 10. Tips for the Next AI Model

1. **Always run `npx tsc --noEmit` after making frontend changes** — catches type errors early.
2. **Import UI components from `@/components/ui`** (barrel), not individual files.
3. **The `ProgressBar` component uses `ariaLabel` prop**, not `label`.
4. **Zod v4 uses `.issues`** not `.errors` on the error object.
5. **Vite 8 uses Rolldown** — `manualChunks` must be a function, not an object.
6. **Tailwind v4 uses `@theme` in CSS** — no `tailwind.config.js` file exists.
7. **Demo mode persists** via `localStorage` key `carboncoach_demo_session`.
8. **The frontend `.env.local` must have `VITE_DEMO_MODE=true`** for local dev without Firebase.
9. **Backend `.env` must have `MOCK_AI=true`** for local dev without GCP credentials.
10. **All feature screens use mock/fallback data** when API calls fail — the app works standalone.
