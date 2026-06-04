# Enterprise Knowledge Assistant

Multi-tenant enterprise knowledge platform for semantic document search and citation-backed Q&A.

Built with FastAPI, PostgreSQL, ChromaDB, Redis, and OpenAI.

## Features (planned)

- Multi-tenant organizations with JWT auth and RBAC
- PDF ingestion, semantic chunking, and vector retrieval
- RAG answers with source citations
- Query analytics, caching, and rate limiting

## Quick start

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
# Edit .env with your DATABASE_URL
.\.venv\Scripts\uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

**Requirements:** Python 3.11+, PostgreSQL

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

**RAG flow:** upload PDF → chunk in Postgres → embed → Chroma → query → retrieve → rerank → LLM → answer + citations.

Full decisions: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Design decisions |

## Project layout

```
backend/          # FastAPI application
docker/           # Docker Compose (optional local / deploy)
docs/             # Architecture notes
```

## Status

**Day 1 in progress** — auth foundation (register / login).

**API versioning:** routes are unversioned until after the first GitHub push; then prefix `/api/v1`.
