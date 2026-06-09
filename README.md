# 🌿 CarbonCoach

**AI-powered carbon footprint tracker** — Helping individuals understand, track, and reduce their carbon footprint through personalized Gemini AI coaching.

Built entirely on the Google Cloud ecosystem for **Google Prompt Wars**.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + Tailwind CSS v4 + Vite |
| Auth | Firebase Authentication (Google Sign-In) |
| Database | Cloud Firestore |
| Backend | FastAPI on Cloud Run (Python 3.11) |
| AI | Vertex AI — Gemini 2.0 Flash & 1.5 Pro |
| Embeddings | Vertex AI text-embedding-004 |
| Vector Search | Vertex AI Vector Search |
| Cron | Cloud Functions + Cloud Scheduler |
| Analytics | BigQuery |
| Storage | Cloud Storage |
| Secrets | Secret Manager |
| Hosting | Firebase Hosting |
| IaC | Terraform |

## Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Set `MOCK_AI=true` in backend `.env` to run without GCP credentials.

### Environment Variables
Copy `backend/.env.example` to `backend/.env` and fill in your values.

## Project Structure

```
carboncoach/
├── frontend/          # React + Vite + Tailwind v4
├── backend/           # FastAPI + Python 3.11
├── functions/         # Cloud Functions (weekly cron)
├── terraform/         # Infrastructure as Code
├── firestore.rules    # Firestore security rules
├── firebase.json      # Firebase Hosting config
└── README.md
```

## Demo Script
1. Sign in with Google → Take the Carbon Profile Quiz → See your AI-generated profile
2. Log today's commute → See an AI tip appear instantly
3. Dashboard shows CO2 breakdown + community benchmark
4. View this week's AI-generated challenge
5. View monthly report with Gemini narrative

**Everything runs on Google** — Firebase, Vertex AI, Cloud Run, BigQuery.
