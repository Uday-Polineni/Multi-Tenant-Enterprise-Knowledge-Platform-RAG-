# Enterprise Knowledge Assistant

Multi-tenant enterprise knowledge platform for semantic document search and citation-backed Q&A.

Built with FastAPI, PostgreSQL, ChromaDB, Redis, and OpenAI.

## Features

**Implemented (Day 1–2)**

- Multi-tenant organizations with JWT auth (register + login)
- Admin-only PDF upload with PyMuPDF text extraction
- Semantic chunking stored in PostgreSQL (`documents` + `chunks`)
- React UI for auth and manual upload testing

**Planned**

- Vector embeddings (ChromaDB) and RAG Q&A with citations
- RBAC enforcement, invites, document listing
- Query analytics, caching, and rate limiting (Redis)

## Quick start

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
# Edit .env with your DATABASE_URL
.\.venv\Scripts\alembic upgrade head
.\.venv\Scripts\uvicorn app.main:app --reload
```

### Frontend (React)

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

Open http://localhost:5173 — register or login, then upload a PDF (admin only).

| Service | URL |
|---------|-----|
| UI | http://localhost:5173 |
| API docs | http://127.0.0.1:8000/docs |
| Health | http://127.0.0.1:8000/health |

**Requirements:** Python 3.11+, PostgreSQL, Node.js 18+ (frontend)

### API (Day 1–2)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | — | Liveness check |
| POST | `/api/v1/auth/register` | — | Create org + admin user |
| POST | `/api/v1/auth/login` | — | Issue JWT |
| POST | `/api/v1/documents/upload` | Bearer (admin) | Upload PDF → extract → chunk |

Upload stores the PDF at `backend/data/uploads/{organization_id}/{document_id}.pdf` and writes metadata to PostgreSQL.

## Architecture

```
Client  →  FastAPI  →  Services  →  PostgreSQL (metadata, users, chunks)
                ↓
            ChromaDB (embeddings, per-org collections)
                ↓
            OpenAI (embeddings + answers)
                ↓
            Redis (cache, rate limits, background jobs)
```

| Layer | Role |
|-------|------|
| **FastAPI** | HTTP API, auth, routing |
| **PostgreSQL** | Source of truth — orgs, users, documents, chunks, query logs |
| **ChromaDB** | Vector search — one collection per organization |
| **OpenAI** | Embeddings + LLM (swappable for Ollama later) |
| **Redis** | Query/embedding cache, rate limiting, async jobs |

**Multi-tenant:** every row scoped by `organization_id`; JWT carries `user_id`, `organization_id`, `role`.

**RAG flow (target):** upload PDF → chunk in Postgres → embed → Chroma → query → retrieve → rerank → LLM → answer + citations.

**Ingestion flow (Day 2):** upload PDF → save to disk → extract text (PyMuPDF) → chunk → `documents` + `chunks` in Postgres.

Full decisions: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Design decisions |

## Project layout

```
backend/
  app/
    api/auth/         # register, login
    api/documents/    # PDF upload
    core/             # config, database, deps, security, storage
    models/           # organizations, users, documents, chunks
    repositories/     # DB access layer
    schemas/          # Pydantic request/response models
    services/         # auth, document ingest, pdf extract, chunking
    utils/            # text cleaning helpers
  alembic/            # database migrations
  data/uploads/       # PDF files (gitignored contents)
frontend/             # React (Vite) — auth + upload UI
docker/               # Docker Compose (optional local / deploy)
docs/                 # Architecture notes
```

## Status

| Day | Deliverable |
|-----|-------------|
| **Day 1** | JWT auth — register + login; React UI |
| **Day 2** | PDF upload pipeline — extract, chunk, store in Postgres; upload UI |

**Next (Day 3):** embeddings, ChromaDB collections per org, RAG query pipeline.

Optional polish: Docker API service, DB health check on `/health`.
