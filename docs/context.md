# Context handoff — Enterprise Knowledge Assistant

**Use this file** when starting a new Cursor chat. Paste the block at the bottom into the new conversation.

**Repo:** https://github.com/Uday-Polineni/Multi-Tenant-Enterprise-Knowledge-Platform-RAG-  
**Local path:** `d:\Projects\Enterprise Knowledge Assistant`  
**Architecture (frozen):** `docs/ARCHITECTURE.md`  
**Step-by-step log (local, gitignored):** `docs/development.md`  
**Last updated:** 2026-06-08 — **Days 1–6 complete**, Day 7 next

---

## User preferences (follow in new chat)

- Go **step by step** — one small step at a time, minimal code per step
- Say **`Day N Step M`** to continue (each day has its own step numbering)
- Update **`docs/development.md`** after each step (gitignored — local only)
- Update **`README.md`** on day milestones
- User pushes to GitHub themselves unless they ask for guidance only
- **Never commit** `backend/.env`, API keys, or `docs/development.md`
- Debug: use **FastAPI (backend)** launch config + `backend/.venv`; breakpoints on **executable lines** (not signature lines)

---

## Stack

| Layer | Tech |
|-------|------|
| API | FastAPI, `/api/v1` prefix |
| DB | PostgreSQL `eka`, SQLAlchemy, Alembic |
| Vectors | ChromaDB persistent `backend/data/chroma/` |
| Cache / queue | **Redis** (`127.0.0.1:6379` on Windows — not `localhost`) |
| Jobs | **ARQ worker** — async PDF embedding after upload |
| AI | OpenAI `text-embedding-3-small` + `gpt-4o-mini` |
| Reranker | `BAAI/bge-reranker-base` — **optional** (`RERANKER_ENABLED=false` in dev) |
| PDF | PyMuPDF |
| Frontend | React + Vite — auth home + ChatGPT-style chat |
| Next | Nginx / EC2 (Day 7) |

---

## Multi-tenancy (ADR)

- Shared Postgres; **`organization_id`** on tenant tables
- JWT claims: `sub` (user_id), `organization_id`, `role`
- Chroma: **one collection per org** → `org_{uuid}`
- Tenant id from JWT only — never trust client-supplied org id
- Upsert Chroma by **`chunk_id`**; new upload = new ids (re-upload stale vectors → Day 8)
- **`access_level`** on documents + Chroma metadata; role-filtered search (Day 4)

---

## API (implemented)

| Method | Path | Auth | Notes |
|--------|------|------|-------|
| GET | `/health` | — | `{"status":"ok"}` |
| POST | `/api/v1/auth/register` | — | New org + admin, or `invite_token` join |
| POST | `/api/v1/auth/login` | — | JWT |
| POST | `/api/v1/auth/invite` | Bearer, **admin** | `{ "email", "role" }` → invite token |
| POST | `/api/v1/documents/upload` | Bearer, **admin** | PDF + `access_level`; async → `processing` then `ready` |
| GET | `/api/v1/documents/{id}` | Bearer, **admin** | Poll upload status (UI auto-updates green popup) |
| POST | `/api/v1/query` | Bearer, any role | Cache? → RAG → `query_logs`; rate limit 429 |
| GET | `/api/v1/analytics/queries` | Bearer, admin/manager | Recent query logs (latency ms, chunks) |

---

## Key backend paths

```
backend/app/
  api/auth/, documents/, query/, analytics/
  core/access.py              # role → access_level map
  core/redis_client.py        # Redis + graceful degrade
  core/rate_limit.py
  core/deps.py                # require_admin, require_role
  core/ai/bge_reranker.py     # optional reranker
  models/                     # org, user, document, chunk, invite, query_log
  services/
    auth.py, document.py, document_embed.py
    cache.py, cache_keys.py, job_queue.py
    rag.py, rerank.py, embedding.py, vector_store.py
  worker/tasks.py, worker/settings.py   # ARQ embed_document_task
```

## Key frontend paths

```
frontend/src/
  App.jsx                     # auth vs chat routing
  components/AuthPage.jsx     # sign in / sign up only
  components/ChatPage.jsx     # chat + admin panel + upload status poll
  api/auth.js, documents.js, query.js, analytics.js
  utils/jwt.js                # role from JWT (UI only)
```

---

## Ingestion flow (Day 6 async)

```
POST upload (admin) + access_level
  → save PDF → extract → chunk → Postgres (processing)
  → if EMBED_ASYNC + Redis: enqueue ARQ job → API returns fast
  → worker: embed → Chroma → status ready
  → UI polls GET /documents/{id} → green "Your document is ready"
  → fallback: sync embed in API if Redis/worker down
```

## Query flow (current)

```
POST query (JWT + role)
  → rate limit (Redis)
  → answer cache hit? → return (0ms in analytics)
  → embed question (embedding cache?)
  → Chroma search top_k=10 + access_level filter
  → if RERANKER_ENABLED: bge-rerank → top 5; else vector top 5
  → LLM → answer + citations → cache answer → query_logs
```

---

## Env vars (`backend/.env` — not in repo)

See `backend/.env.example`. Important:

| Var | Notes |
|-----|-------|
| `DATABASE_URL`, `JWT_*`, `OPENAI_API_KEY` | Required |
| `REDIS_URL` | **`redis://127.0.0.1:6379/0`** on Windows (ARQ async fails on `localhost`) |
| `CACHE_TTL_SECONDS` | Default 3600 |
| `RATE_LIMIT_PER_HOUR` | Default 100 |
| `EMBED_ASYNC` | `true` = worker; `false` = sync upload (no worker) |
| `RAG_SEARCH_TOP_K` | **10** (was 20) |
| `RAG_RERANK_TOP_N` | 5 |
| `RERANKER_ENABLED` | **`false`** in dev (CPU ~17s); `true` for quality |
| `ALLOW_PUBLIC_REGISTRATION` | Day 4 |

---

## Run locally

```powershell
# Redis — local on 127.0.0.1:6379 OR: cd docker; docker compose up -d redis

# Terminal 1 — API
cd backend
.\.venv\Scripts\alembic upgrade head
.\.venv\Scripts\uvicorn app.main:app --reload

# Terminal 2 — Worker (only if EMBED_ASYNC=true)
cd backend
.\.venv\Scripts\arq app.worker.settings.WorkerSettings

# Terminal 3 — UI
cd frontend
npm run dev
```

UI: http://localhost:5173 · Docs: http://127.0.0.1:8000/docs

---

## Completed (Days 1–6)

| Day | Deliverable |
|-----|-------------|
| **1** | FastAPI, Postgres, Alembic, JWT, React auth |
| **2** | PDF upload, extract, chunk, Postgres |
| **3** | OpenAI embed, Chroma, RAG + citations, query UI |
| **4** | RBAC, `access_level`, invites; role-filtered search; chat UI redesign |
| **5** | Reranker (optional), `query_logs`, analytics API + Recent queries UI |
| **6** | Redis cache, rate limit, ARQ async embed, upload ready polling, Redis fallback |

**Manual testing done:** cache hit ~0ms; upload processing→ready popup; analytics latency panel; reranker off for speed.

---

## UX (business-facing)

- **Home:** sign in / sign up only (no token shown)
- **Chat:** ChatGPT-style Q&A for all roles
- **Admin only:** invite + upload; managers see Analytics (query logs)
- **Upload:** green status — "preparing…" → auto-updates to "ready"
- **Analytics:** question + latency ms + chunks (manager/admin)

---

## Known issues → Day 8 backlog

1. Document re-upload / stale Chroma vectors  
2. Citation dedupe, cap citations, LLM markdown in UI  
3. Chunk section names, bullet normalization  
4. Infra polish: cache invalidation on delete, `/health` + DB  
5. **First-query latency** (~10–17s uncached) — tune before company rollout  
6. **Search paraphrases** — "portfolio policy" vs "prompt guide"; query rewrite / hybrid search  

---

## Debugging notes learned

- `flush()` ≠ `commit()` — pgAdmin needs commit at end of ingest  
- Chroma `upsert` same `chunk_id` only; new upload = new ids  
- **Windows Redis:** use `127.0.0.1` not `localhost` for ARQ worker  
- **Reranker:** ~5–10s CPU per query; disable with `RERANKER_ENABLED=false`  
- **Redis down:** API degrades — no cache/rate limit; sync embed fallback  
- **ARQ ≠ Kafka:** job queue for embed jobs; Kafka overkill for MVP  
- PowerShell: use `;` not `&&`  
- Run `arq` from **`backend/`** folder  

---

## Day 7 — next

EC2, Docker full compose (api, worker, postgres, redis, nginx), HTTPS, demo data, architecture diagram, production README.

---

## Paste this into a new chat

```
Continue the Enterprise Knowledge Assistant project.

Read docs/context.md and docs/ARCHITECTURE.md first.

Status: Days 1–6 complete. Day 7 next (deploy + demo).

Work step-by-step: say "Day 7 Step 1" when I want to implement.
Update docs/development.md after each step (local, gitignored).
Do not commit secrets. User pushes to GitHub themselves.

Start by giving me Day 7 objectives and a step breakdown, then wait for "Day 7 Step 1".
```

Optional: attach or `@` reference `docs/context.md` in the new chat.
