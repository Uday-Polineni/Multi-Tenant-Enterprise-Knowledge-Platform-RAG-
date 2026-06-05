# Enterprise Knowledge Assistant

Multi-tenant enterprise knowledge platform for semantic document search and citation-backed Q&A.

Built with FastAPI, PostgreSQL, ChromaDB, Redis, and OpenAI.

## Features

**Implemented (Day 1–3)**

- Multi-tenant organizations with JWT auth (register + login)
- Admin-only PDF upload with PyMuPDF text extraction and chunking (PostgreSQL)
- OpenAI embeddings + ChromaDB vector index (one collection per organization)
- RAG query API with context-only answers and citations
- React UI — register, login, upload PDF, ask questions

**Planned**

- RBAC enforcement, `access_level` filters, invites (Day 4)
- Reranker + query logging (Day 5)
- Redis cache, rate limits, async embedding jobs (Day 6)
- Production deploy (Day 7)
- Text/citation polish (Day 8 misc)

## Quick start

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
# Edit .env: DATABASE_URL, OPENAI_API_KEY, JWT_SECRET
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

Open http://localhost:5173 — register, upload a PDF (admin), then ask a question.

| Service | URL |
|---------|-----|
| UI | http://localhost:5173 |
| API docs | http://127.0.0.1:8000/docs |
| Health | http://127.0.0.1:8000/health |

**Requirements:** Python 3.11+, PostgreSQL, Node.js 18+, OpenAI API key

### API

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | — | Liveness check |
| POST | `/api/v1/auth/register` | — | Create org + admin user |
| POST | `/api/v1/auth/login` | — | Issue JWT |
| POST | `/api/v1/documents/upload` | Bearer (admin) | Upload PDF → extract → chunk → embed → Chroma |
| POST | `/api/v1/query` | Bearer | RAG question → answer + citations |

Upload stores PDFs at `backend/data/uploads/{organization_id}/{document_id}.pdf`.  
Vectors persist at `backend/data/chroma/` (local dev).

## Architecture

```
Client  →  FastAPI  →  Services  →  PostgreSQL (metadata, users, chunks)
                ↓
            ChromaDB (embeddings, per-org collections)
                ↓
            OpenAI (embeddings + answers)
                ↓
            Redis (cache, rate limits, background jobs) — planned Day 6
```

| Layer | Role |
|-------|------|
| **FastAPI** | HTTP API, auth, routing |
| **PostgreSQL** | Source of truth — orgs, users, documents, chunks |
| **ChromaDB** | Vector search — one collection per organization |
| **OpenAI** | Embeddings (`text-embedding-3-small`) + LLM (`gpt-4o-mini`) |
| **Redis** | Query/embedding cache, rate limiting, async jobs (planned) |

**Multi-tenant:** every row scoped by `organization_id`; JWT carries `user_id`, `organization_id`, `role`.

**RAG flow (Day 3):** upload PDF → chunk in Postgres → embed → Chroma → query → retrieve → LLM → answer + citations.

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
    api/query/        # RAG query
    core/ai/          # OpenAI embedding + LLM providers
    core/             # config, database, deps, security, storage
    models/           # organizations, users, documents, chunks
    repositories/     # DB access layer
    schemas/          # Pydantic request/response models
    services/         # auth, ingest, embedding, rag, vector_store, chunking
    utils/            # text cleaning helpers
  alembic/            # database migrations
  data/uploads/       # PDF files (gitignored contents)
  data/chroma/        # Chroma persist dir (gitignored contents)
frontend/             # React (Vite) — auth, upload, query UI
docker/               # Docker Compose (optional local / deploy)
docs/                 # Architecture notes
```

## Status

| Day | Deliverable |
|-----|-------------|
| **Day 1** | JWT auth — register + login; React UI |
| **Day 2** | PDF upload pipeline — extract, chunk, Postgres; upload UI |
| **Day 3** | Embeddings, Chroma, RAG query API + citations; query UI |

**Next (Day 4):** RBAC, `access_level`, invites, retrieval filters.

Optional polish: Day 8 misc (citation dedupe, document replace, markdown UI).
