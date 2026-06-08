# Enterprise Knowledge Assistant

Multi-tenant enterprise knowledge platform for semantic document search and citation-backed Q&A.

Built with FastAPI, PostgreSQL, ChromaDB, Redis, and OpenAI.

## Features

**Implemented (Day 1–6)**

- Multi-tenant organizations with JWT auth (register + login)
- Admin invites — join existing org with `employee` / `manager` / `admin` role
- Document `access_level` enum — role-based retrieval filters in Chroma
- Admin-only PDF upload with PyMuPDF text extraction and chunking (PostgreSQL)
- OpenAI embeddings + ChromaDB vector index (one collection per organization)
- RAG: Chroma top-15 → **bge-reranker-base** (optional) → top-10 → LLM + citations
- **Query logs** in PostgreSQL; manager/admin analytics API
- **Redis** — answer + embedding cache, per-user rate limits, ARQ async embed jobs
- React UI — auth home, chat, admin tools, recent queries

**Latency (Phase A — implemented)**
- SSE streaming (`POST /api/v1/query/stream`) — sources appear first, answer streams token-by-token
- Trimmed LLM context (3 chunks × 800 chars) — faster prefill without changing retrieval top-k
- Per-stage timing in `query_logs.token_usage.stage_timings_ms` + structured logs

**Planned**
- Production deploy (Day 7)
- Latency Phase B1 — org cache version + semantic answer cache + async query logs
- Latency Phase B2 — Postgres FTS + Chroma hybrid retrieval (RRF merge)

## Quick start

### Backend

```powershell
cd backend
python -m venv .venv
copy .env.example .env
# Edit .env: DATABASE_URL, OPENAI_API_KEY, JWT_SECRET
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\alembic upgrade head
```

**Redis (local)** — required for cache, rate limits, and async upload indexing:

```powershell
# Option A — Docker
cd docker
docker compose up -d redis

# Option B — Redis on Windows (Memurai, etc.) — use 127.0.0.1 not localhost (ARQ/async)
```

**Terminal 1 — API:**

```powershell
cd backend
.\.venv\Scripts\uvicorn app.main:app --reload
```

**Terminal 2 — ARQ worker** (when `EMBED_ASYNC=true`):

```powershell
cd backend
.\.venv\Scripts\arq app.worker.settings.WorkerSettings
```

**Note:** First query downloads `BAAI/bge-reranker-base` (~400MB). Repeat identical questions are served from Redis cache (much faster).

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
| POST | `/api/v1/auth/register` | — | Create org + admin, or join via `invite_token` |
| POST | `/api/v1/auth/login` | — | Issue JWT |
| POST | `/api/v1/auth/invite` | Bearer (admin) | Create invite token for email + role |
| POST | `/api/v1/documents/upload` | Bearer (admin) | Upload PDF + `access_level` → ingest → Chroma |
| POST | `/api/v1/query` | Bearer | RAG → rerank → answer + citations (blocking JSON) |
| POST | `/api/v1/query/stream` | Bearer | Same pipeline via SSE: `citations` → `token`* → `done` |
| GET | `/api/v1/analytics/queries` | Bearer (admin/manager) | Recent query logs for org |

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
            Redis (cache, rate limits, ARQ job queue)
```

| Layer | Role |
|-------|------|
| **FastAPI** | HTTP API, auth, routing |
| **PostgreSQL** | Source of truth — orgs, users, documents, chunks |
| **ChromaDB** | Vector search — one collection per organization |
| **OpenAI** | Embeddings (`text-embedding-3-small`) + LLM (`gpt-4o-mini`) |
| **Redis** | Answer/embedding cache, rate limiting, ARQ embed queue |

**Multi-tenant:** every row scoped by `organization_id`; JWT carries `user_id`, `organization_id`, `role`.

**RAG flow:** query → Redis cache? → embed (cached?) → Chroma → rerank → LLM → answer → `query_logs`. Upload with async worker: chunk in PG → `processing` → worker embeds → `ready`.

**Roles (Day 4):** Admin — all access levels + upload/invite. Manager — `public`, `hr`, `engineering`, `finance`. Employee — `public` only.

Full decisions: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Latency & tradeoffs

Uncached queries without the reranker often take **8–12 seconds** end-to-end because the pipeline runs two serial OpenAI API calls (embed + generate) and waits for the full answer before responding.

| Stage | Typical cost | Notes |
|-------|--------------|-------|
| Redis exact cache hit | ~0 ms | Same normalized question only |
| OpenAI embedding | 300–1500 ms | One network round trip per novel question |
| Chroma vector search | 50–500 ms | Local; can spike on cold start |
| bge-reranker (if enabled) | 5–10 s CPU | Keep `RERANKER_ENABLED=false` on dev/small VMs |
| LLM `gpt-4o-mini` | 2–6 s | Dominated by context size + answer length |

### How enterprise search (e.g. Glean) differs

| Approach | Glean-scale | This MVP |
|----------|-------------|----------|
| **Search vs chat** | Instant indexed search; AI summary is optional | Every question hits full RAG |
| **Indexing** | Pre-crawled HNSW + BM25 hybrid, ms retrieval | Chroma at query time |
| **Query-time models** | Small planner (Waldo ~250 ms) + frontier LLM only for synthesis | Embed + LLM every time |
| **Perceived speed** | Streaming, sources-first UI, aggressive caching | Phase A adds streaming + sources-first |
| **Context size** | Focused snippets to LLM | ~700-char ingest chunks; up to 10 sent whole to LLM |

We cannot replicate Glean's full stack on a 7-day MVP. The phased plan:

| Phase | Focus | Expected effect |
|-------|--------|-----------------|
| **A (done)** | SSE streaming, sources before LLM, trim context, stage timings | Feels ~2× faster; total time similar |
| **B1 (done)** | Org cache version + semantic cache + chunk validation | Paraphrase hits ~50 ms; safe after re-upload |
| **B2 (done)** | Postgres FTS + Chroma hybrid + RRF | Better keyword / exact-term recall |
| **B3** | ~~Local embeddings~~ **deferred** | Staying on OpenAI — better multilingual demo uploads |
| **C** | Search-only endpoint, query router, optional AI summarize button | Matches “search first, chat second” UX |

### Chunking + LLM context (pre–Phase B)

PDFs are chunked at **~700 characters** on upload (was 2000). Retrieval returns focused passages so the LLM can receive **full chunks** without head truncation.

```env
INGEST_CHUNK_MAX_CHARS=700
INGEST_CHUNK_OVERLAP_CHARS=80
RAG_SEARCH_TOP_K=15
RAG_RERANK_TOP_N=10
RAG_LLM_CONTEXT_CHUNKS=10   # matches RAG_RERANK_TOP_N — send reranked chunks whole
RAG_CHUNK_MAX_CHARS=700     # safety cap; equals ingest size → no truncation
RERANKER_ENABLED=false      # required for fast dev/demo on CPU
```

**Re-upload existing PDFs** after changing ingest settings (old 2000-char vectors stay in Chroma until replace/delete).

### Phase A (streaming)

SSE: `POST /api/v1/query/stream` — sources first, then streamed answer. Stage timings in `query_logs.token_usage.stage_timings_ms`.

Stage timings are stored in `query_logs.token_usage.stage_timings_ms` (`embed_ms`, `chroma_ms`, `rerank_ms`, `llm_ttft_ms`, `llm_total_ms`, `total_ms`) and logged as `rag_query_timings` in API stdout.

### Phase B1 — semantic cache + org version (done)

```env
SEMANTIC_CACHE_ENABLED=true
SEMANTIC_CACHE_SIMILARITY_THRESHOLD=0.92
SEMANTIC_CACHE_MAX_ENTRIES=200
```

```text
Query → exact cache (org version in key)?
      → embed question
      → semantic cache (cosine ≥ threshold, same org version)?
          → verify cached chunk_ids still in Postgres
      → full RAG → store exact + semantic entry

Upload / delete / replace → INCR cache:org_version:{org_id}  (instant invalidation)
```

Cache hits are logged as `token_usage.cache_hit`: `"exact"` or `"semantic"`.

### Phase B2 — hybrid search (done)

```env
HYBRID_SEARCH_ENABLED=true
HYBRID_RRF_K=60
```

```text
Question → embed → Chroma vector top-15  ─┐
         → Postgres FTS (ts_rank_cd) top-15 ┴→ RRF merge → rerank top-10 → LLM
```

`chunks.search_vector` (GIN index) is built from `section_name + content` on ingest.  
Run `alembic upgrade head` after pull; re-upload PDFs if migration backfill missed rows.

## Documentation

| Doc | Purpose |
|-----|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Design decisions |

## Project layout

```
backend/
  app/
    api/auth/         # register, login, invite
    core/access.py    # role → access_level map
    api/documents/    # PDF upload
    api/query/        # RAG query
    api/analytics/    # query logs (manager/admin)
    core/ai/          # embedding, LLM, bge reranker
    core/             # config, database, deps, security, storage
    models/           # organizations, users, documents, chunks, invites, query_logs
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
| **Day 4** | RBAC, `access_level`, invites, role-filtered retrieval; UI updates |
| **Day 5** | bge-reranker, top-10→5 RAG, query_logs, analytics API |
| **Day 6** | Redis cache, rate limits, ARQ async embeddings |

**Day 8 (partial):** Document replace/delete, citation PDF links, markdown UI, latency Phase A.

**Next (Day 7):** EC2 deploy, Nginx, demo data.

**Embeddings:** OpenAI `text-embedding-3-small` (kept for multilingual demo PDFs; local `bge-base` deferred).

**Next:** Day 7 deploy + demo, or further latency polish (warm-up, query router).
