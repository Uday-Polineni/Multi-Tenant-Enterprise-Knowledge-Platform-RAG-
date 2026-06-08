# Context handoff — Enterprise Knowledge Assistant

**Use this file** when starting a new Cursor chat. Paste the block at the bottom into the new conversation.

**Repo:** https://github.com/Uday-Polineni/Multi-Tenant-Enterprise-Knowledge-Platform-RAG-  
**Local path:** `d:\Projects\Enterprise Knowledge Assistant`  
**Architecture (frozen):** `docs/ARCHITECTURE.md`  
**Step-by-step log (local, gitignored):** `docs/development.md`  
**Last updated:** 2026-06-08 — **Days 1–4 complete**, Day 5 next

---

## User preferences (follow in new chat)

- Go **step by step** — one small step at a time, minimal code per step
- Say **`Day N Step M`** to continue (each day has its own step numbering)
- Update **`docs/development.md`** after each step (gitignored — local only)
- Update **`README.md`** on day milestones
- User pushes to GitHub themselves unless they ask for guidance only
- **Never commit** `backend/.env`, API keys, or `docs/development.md`
- Debug: use **FastAPI (backend)** launch config + `backend/.venv`; breakpoints on **executable lines** (not signature lines)
- OpenAI dev cost so far: negligible (<$0.01 for a few embed + query calls)

---

## Stack

| Layer | Tech |
|-------|------|
| API | FastAPI, `/api/v1` prefix |
| DB | PostgreSQL `eka`, SQLAlchemy, Alembic |
| Vectors | ChromaDB persistent `backend/data/chroma/` |
| AI | OpenAI `text-embedding-3-small` + `gpt-4o-mini` |
| PDF | PyMuPDF |
| Frontend | React + Vite `localhost:5173` |
| Planned | Redis, ARQ worker (Day 6), Nginx/EC2 (Day 7) |

---

## Multi-tenancy (ADR)

- Shared Postgres; **`organization_id`** on tenant tables
- JWT claims: `sub` (user_id), `organization_id`, `role`
- Chroma: **one collection per org** → `org_{uuid}`
- Tenant id from JWT only — never trust client-supplied org id
- Upsert Chroma by **`chunk_id`**; new upload = new ids (re-upload stale vectors → Day 8)

---

## API (implemented)

| Method | Path | Auth | Notes |
|--------|------|------|-------|
| GET | `/health` | — | `{"status":"ok"}` |
| POST | `/api/v1/auth/register` | — | New org + admin, or `invite_token` join |
| POST | `/api/v1/auth/login` | — | JWT |
| POST | `/api/v1/auth/invite` | Bearer, **admin** | `{ "email", "role" }` → invite token |
| POST | `/api/v1/documents/upload` | Bearer, **admin** | PDF + `access_level` form field |
| POST | `/api/v1/query` | Bearer, any role | RAG — filtered by role's allowed levels |

---

## Key backend paths

```
backend/app/
  api/auth/router.py
  api/documents/router.py
  api/query/router.py
  core/config.py          # DATABASE_URL, JWT, OPENAI_API_KEY, ALLOW_PUBLIC_REGISTRATION
  core/access.py          # role → allowed access_level map
  core/deps.py            # get_current_user, require_admin, require_role
  core/ai/base.py         # EmbeddingProvider, LLMProvider protocols
  core/ai/openai_embedding.py
  core/ai/openai_llm.py
  core/storage.py         # PDF save/read
  models/                 # organization, user, document, chunk
  repositories/
  services/
    auth.py
    document.py           # ingest_document()
    embedding.py          # embed_document_chunks()
    rag.py                # answer_question()
    vector_store.py       # get_org_collection, upsert_chunks, search
    pdf_extract.py, chunking.py
  schemas/auth.py, document.py, query.py
backend/data/uploads/     # PDFs (gitignored contents)
backend/data/chroma/      # Chroma index (gitignored contents)
```

## Key frontend paths

```
frontend/src/
  App.jsx                 # register, login, upload, query UI
  api/auth.js, documents.js, query.js
```

---

## Ingestion flow (Day 2–3)

```
POST upload (admin)
  → document pending
  → save PDF to disk
  → processing
  → extract (PyMuPDF) → chunk → bulk_create_chunks (Postgres)
  → embed_document_chunks → Chroma upsert
  → ready (or failed; on embed fail: delete PG chunks, status failed)
```

## Query flow (Day 3)

```
POST query (JWT)
  → embed question
  → Chroma search top_k=5 (org collection)
  → LLM context-only prompt
  → answer + citations (from hits, not parsed from LLM text)
```

---

## Env vars (`backend/.env` — not in repo)

Copy from `backend/.env.example`:

- `DATABASE_URL` — local Postgres `eka`
- `JWT_SECRET`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`
- `UPLOAD_DIR=data/uploads`
- `OPENAI_API_KEY` — **required Day 3+**
- `CHROMA_PERSIST_DIR=data/chroma`
- `EMBEDDING_MODEL=text-embedding-3-small`
- `LLM_MODEL=gpt-4o-mini`

---

## Run locally

```powershell
# Terminal 1 — API
cd backend
.\.venv\Scripts\alembic upgrade head
.\.venv\Scripts\uvicorn app.main:app --reload

# Terminal 2 — UI
cd frontend
npm run dev
```

UI: http://localhost:5173 · Docs: http://127.0.0.1:8000/docs

---

## Completed (Days 1–4)

| Day | Deliverable |
|-----|-------------|
| **1** | FastAPI, Postgres models, Alembic, JWT register/login, React auth UI |
| **2** | PDF upload, extract, chunk, Postgres; upload UI; pushed to GitHub |
| **3** | OpenAI embed, Chroma, ingest hook, RAG service, query API, query UI; manual test OK |
| **4** | `access_level`, role-filtered Chroma search, invites, RBAC deps, UI; smoke test OK |

**Day 4 Step 31:** Manual UI test (two users, two access levels) — user runs locally.

---

## Day 8 — Misc backlog (do NOT block Days 4–7)

1. **Document re-upload** — new `document_id` leaves old Chroma vectors; need delete/replace
2. **Citation dedupe** — by `(document, page, section)` not only `chunk_id`
3. **Cap citations** — e.g. top 3 unique sources
4. **LLM markdown** — `**bold**` in plain UI; plain-text prompt or react-markdown
5. **Chunk section names** — resume heading detection
6. **Bullet normalization** in `text_clean.py`
7. Hide upload until logged in; Docker API; DB health on `/health`; cache invalidation on delete

---

## Remaining plan — Days 4–7 (step outlines)

### Day 4 — RBAC, `access_level`, invites

**Objectives:** Enforce roles; document access enum; invite users to existing org.

| Step area | Tasks |
|-----------|--------|
| Model | `documents.access_level` enum; migration; `invites` table |
| Config | Role → allowed `access_level` map |
| Upload | Admin sets `access_level` on upload |
| Chroma | Store `access_level` in chunk metadata; filter on search |
| Auth | `POST /auth/invite` (admin); register-with-invite token |
| RBAC | Manager/employee query only; admin upload/delete |
| Env | `ALLOW_PUBLIC_REGISTRATION` |
| Test | Two users, different roles, filtered retrieval |
| Docs | README + development.md |

### Day 5 — Reranker + query logging

**Objectives:** top 20 → rerank → top 5; persist queries.

| Step area | Tasks |
|-----------|--------|
| Model | `query_logs` table + migration |
| Reranker | `RerankerProvider` + local `bge-reranker-base` |
| RAG | Search top_k=20 → rerank → top_n=5 → LLM |
| API | Optional analytics endpoint (manager) |
| Test | Better relevance vs raw vector top 5 |
| Docs | Wrap-up |

### Day 6 — Redis cache, rate limit, async embeddings

**Objectives:** Cache answers/embeddings; rate limit; ARQ worker for embed jobs.

| Step area | Tasks |
|-----------|--------|
| Infra | Redis in docker-compose; config |
| Cache | Hash question + org; TTL for answers/embeddings |
| Rate limit | Per user/org hourly cap |
| ARQ | Worker service; async embed after upload (optional sync fallback) |
| Upload | Return faster; status `processing` until embed done |
| Test | Cache hit; rate limit 429 |
| Docs | Wrap-up |

### Day  7 — Deploy + demo

**Objectives:** EC2, Nginx, HTTPS, demo data, final README/diagram.

| Step area | Tasks |
|-----------|--------|
| Docker | Full compose: api, worker, postgres, chroma, redis, nginx |
| Deploy | EC2 setup, env secrets, volumes |
| Nginx | Reverse proxy, TLS |
| Demo | Seed org, sample PDFs, demo script |
| Docs | Architecture diagram, production README |

---

## Roles (architecture — partial today)

| Role | Target (Day 4) | Today |
|------|----------------|-------|
| Admin | Upload, delete, invites, users | Upload + invite enforced; all access levels |
| Manager | Query, analytics | Query; public/hr/engineering/finance |
| Employee | Query only | Query; public only |

---

## Debugging notes learned

- `flush()` ≠ `commit()` — pgAdmin won't see rows until commit at end of `ingest_document()`
- Chroma `upsert` updates same `chunk_id` only; new upload = new ids
- Register fresh org for clean Chroma when testing RAG
- PowerShell: use `;` not `&&` between commands

---

## Paste this into a new chat

```
Continue the Enterprise Knowledge Assistant project.

Read docs/context.md and docs/ARCHITECTURE.md first.

Status: Days 1–3 complete. Day 4 next (RBAC, access_level, invites).

Work step-by-step like before: say "Day 4 Step 1" when I want to implement.
Update docs/development.md after each step (local, gitignored).
Do not commit secrets. User pushes to GitHub themselves.

Start by giving me Day 4 objectives and a step breakdown (like Days 1–3), then wait for "Day 4 Step 1".
```

Optional: attach or `@` reference `docs/context.md` in the new chat so the agent reads the full file.
