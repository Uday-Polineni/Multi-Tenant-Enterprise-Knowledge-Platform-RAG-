# Enterprise Knowledge Assistant — Architecture Decision Record

Status: **Frozen** (pre-implementation)  
Last updated: 2026-06-03

---

## Summary

Multi-tenant enterprise RAG platform: FastAPI, PostgreSQL (source of truth), ChromaDB (per-org collections), Redis (cache + rate limits + ARQ), OpenAI with provider abstraction for future Ollama. API-first; frontend deferred. Hybrid registration and hybrid document access (enum now, tags later).

---

## 1. Multi-tenancy

| Decision | Choice |
|----------|--------|
| Database model | **Shared PostgreSQL** with `organization_id` on all tenant-scoped tables |
| Isolation enforcement | Repository/service layer always scopes by `organization_id` from JWT — never from client-supplied tenant id alone |
| ChromaDB | **One collection per organization** (e.g. `org_{uuid}`) |

**Rationale:** Matches 7-day MVP ops on single EC2; hard tenant boundary in vector store; Postgres remains authoritative for metadata and chunks.

---

## 2. PostgreSQL ↔ Chroma consistency

| Decision | Choice |
|----------|--------|
| Source of truth | **PostgreSQL** (documents, chunks) |
| Chroma | Derived embedding index |
| Document lifecycle | `status`: `pending` → `processing` → `ready` \| `failed` |
| Ingestion timing | **Sync** chunk persist (Day 2); **async** embedding via ARQ (Day 6) |
| Retries | Idempotent embed jobs keyed by `chunk_id`; re-embed from PG on failure |

---

## 3. Registration & authentication (Hybrid — Option C)

### Phase 1 (Day 1)

- `POST /auth/register`: `email`, `password`, `organization_name` → creates **new org** + **Admin** user.
- `POST /auth/login`: returns JWT access token.
- JWT claims: `user_id`, `organization_id`, `role`.
- Password hashing: bcrypt (`passlib`).

### Phase 2 (Day 4)

- `POST /auth/invite` (Admin): create invite with `email`, `role`, expiry.
- Register-with-invite: `invite_token` → user joins **existing** org with invited role.
- Env: `ALLOW_PUBLIC_REGISTRATION=false` to disable open signup in production.

### Tables (incremental)

- Day 1: `organizations`, `users`
- Day 4: `invites` (`organization_id`, `email`, `role`, `token`, `expires_at`, `used_at`)

---

## 4. RBAC & document access (Hybrid)

### API roles (enum on `users.role`)

| Role | Capabilities |
|------|----------------|
| **Admin** | Upload/delete documents, manage users, invites |
| **Manager** | Query, analytics |
| **Employee** | Query only |

### Document scope — Phase 1 (Day 4)

- `documents.access_level` enum (e.g. `public`, `hr`, `engineering`, `finance`, `admin_only`).
- Set on upload by Admin.
- **Role → allowed `access_level` list** (config or code map); enforced at retrieval via Chroma metadata filter + app-side validation on top-20 hits if needed.

### Document scope — Phase 2 (later)

- Optional `documents.tags` (JSON array) for analytics and labeling **without** changing retrieval filter in MVP.
- Per-user grants (`user_document_grants`) — **out of scope** for 7-day plan unless explicitly added.

### Chunk / Chroma metadata (minimum)

- `organization_id`, `document_id`, `chunk_id`, `access_level`
- `page_number`, `section_name`, `filename`

---

## 5. File storage

| Decision | Choice |
|----------|--------|
| MVP | **Local volume** `/data/uploads/{organization_id}/` |
| Abstraction | `StorageBackend` interface for future S3 |

---

## 6. Background processing

| Decision | Choice |
|----------|--------|
| Queue | **ARQ** + Redis (Day 6) |
| Jobs | Embedding generation after upload, re-index, optional analytics |
| Worker | Separate Docker Compose service, same image as API |

---

## 7. AI providers

| Concern | Implementation |
|---------|----------------|
| Embeddings | `EmbeddingProvider.embed()` — default OpenAI `text-embedding-3-small` |
| Generation | `LLMProvider.complete()` — default `gpt-4o-mini` |
| Reranking | `RerankerProvider.rerank()` — BAAI `bge-reranker-base` (Day 5), local |
| Config | `AI_PROVIDER=openai` (future: `ollama`) |

### Retrieval constants (env-overridable)

- Vector search: **top_k = 20**
- After rerank: **top_n = 5**

---

## 8. Query pipeline

```
Question
  → Redis cache? (answer / embedding)
  → Query embedding
  → Chroma (org collection + access_level filter)
  → Top 20
  → Reranker → Top 5
  → LLM (context-only, no hallucination policy)
  → Response + citations
  → query_logs
```

### Response shape

```json
{
  "answer": "...",
  "citations": [
    {
      "document": "filename or title",
      "page": 12,
      "section": "PTO Policy",
      "chunk_id": "uuid"
    }
  ]
}
```

### Prompt policy

- Answer **only** from provided context.
- If not in context, state information is not available.
- Always include citations.

---

## 9. Caching & rate limiting (Day 6)

| Use | Notes |
|-----|--------|
| RAG answers | Key: hash(`organization_id` + normalized question); TTL-based MVP |
| Query embeddings | Key: hash(question) |
| Rate limit | e.g. 100 req/hour per user — `rl:{org_id}:{user_id}` |
| Invalidation | TTL-first; optional purge on document delete for org |

---

## 10. API conventions

| Topic | Choice |
|-------|--------|
| Paths (Day 1 → first GitHub push) | **Unversioned** (e.g. `/auth/register`, `/documents/upload`) |
| After first push | Prefix **`/api/v1`** |
| Structure | Monolith: `api/` routers, `services/`, `repositories/`, `core/` |

---

## 11. Chunking & ingestion

- PDF → PyMuPDF extract → clean → **structure-aware chunks** (headings/sections/paragraphs, max ~512–800 tokens, overlap ~50–100).
- Avoid naive fixed-character-only chunking.
- Postgres stores chunk text + metadata; Chroma stores embeddings + same metadata.

---

## 12. Frontend

- **Deferred** until RAG API is working.
- Demo via OpenAPI / curl / Postman; optional minimal UI later.

---

## 13. Docker Compose (target topology)

```
nginx → api (FastAPI)
          ├── postgres
          ├── chroma
          ├── redis
          └── worker (ARQ)
```

Named volumes for Postgres, Chroma, uploads.

---

## 14. Observability & security

- Structured JSON logs: `request_id`, `organization_id`, `user_id`, latency.
- Secrets via environment / Docker secrets — not in repo.
- JWT in `Authorization: Bearer` only.
- HTTPS at Nginx on EC2 (Day 7).
- `query_logs`: question, answer, latency_ms, token_usage, retrieved chunk ids (JSON, Day 5).

---

## 15. Implementation order (7-day plan)

| Day | Focus |
|-----|--------|
| 1 | FastAPI, Docker Compose, PG, Alembic, JWT, register (org+admin), login |
| 2 | PDF upload, extract, chunk, Postgres |
| 3 | Embeddings, Chroma, retrieval, LLM, citations |
| 4 | RBAC, tenant filters, `access_level`, invites |
| 5 | Reranker, query logging |
| 6 | Redis cache, rate limit, ARQ embeddings |
| 7 | EC2 deploy, Nginx, README, diagram, demo data |

---

## Decision log

| ID | Topic | Decision |
|----|--------|----------|
| ADR-001 | Tenancy | Shared PG + `organization_id` |
| ADR-002 | Chroma | Collection per org |
| ADR-003 | Registration | Hybrid C: public org signup Day 1; invites Day 4 |
| ADR-004 | Document access | Hybrid: `access_level` enum Day 4; tags later |
| ADR-005 | PDF storage | Local volume + abstraction |
| ADR-006 | Jobs | ARQ + Redis Day 6 |
| ADR-007 | API versioning | Unversioned until first GitHub push |
| ADR-008 | Citations | document, page, section, chunk_id |
| ADR-009 | Frontend | After RAG API |

---

## Open items (non-blocking)

- Exact `access_level` enum values and role→level matrix (define at Day 4).
- Cache invalidation strategy detail (TTL-only vs event-driven on delete).
- Email delivery for invites (manual token copy acceptable for demo).
