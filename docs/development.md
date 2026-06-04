# Development log

Step-by-step implementation notes. Updated after each step.

**Secrets:** `backend/.env` is gitignored. Use `backend/.env.example` as the template.

---

## Day 1 checklist

- [x] Step 1 — FastAPI skeleton + `/health`
- [x] Step 2 — `docker/docker-compose.yml` (Postgres; optional — using local Postgres)
- [x] Step 3 — `.env.example` + local `.env`
- [x] Step 4 — Verify Postgres + database `eka`
- [x] Step 5 — `app/core/config.py`
- [x] Step 6 — SQLAlchemy deps in `requirements.txt`
- [x] Step 7 — `app/core/database.py`
- [x] Step 8 — `app/models/base.py`
- [x] Step 9 — `app/models/organization.py`
- [x] Step 10 — `app/models/user.py`
- [x] Step 11 — `app/models/__init__.py`
- [x] Step 12 — Alembic init
- [x] Step 13 — First migration
- [x] Step 14 — Run migration
- [x] Step 15 — Password hash/verify
- [x] Step 16 — JWT create/decode
- [ ] Step 17 — Auth schemas
- [ ] Step 18 — `UserRole` enum
- [ ] Step 19 — Organization repository
- [ ] Step 20 — User repository
- [ ] Step 21 — Register service
- [ ] Step 22 — Login service
- [ ] Step 23 — `POST /auth/register`
- [ ] Step 24 — `POST /auth/login`
- [ ] Step 25 — Wire router in `main.py`
- [ ] Step 26–28 — Docker API service + smoke test (optional)
- [ ] Step 29–30 — DB health check + polish (optional)

---

## Completed steps

### Step 1 — FastAPI skeleton

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\uvicorn app.main:app --reload
```

Verify: http://127.0.0.1:8000/health → `{"status":"ok"}`

### Step 2 — Docker Compose (optional)

`docker/docker-compose.yml` — Postgres for Docker users. Skipped locally; using local Postgres instead.

### Step 3 — Environment variables

```powershell
cd backend
copy .env.example .env
```

Local setup:

| Variable | Value |
|----------|--------|
| `DATABASE_URL` | `postgresql://postgres:superuser123@localhost:5432/eka` |

JWT vars in `.env` are placeholders until auth steps.

### Step 4 — Verify Postgres

Database `eka` exists on local server (pgAdmin / `psql`).

### Step 5 — App config

`app/core/config.py` — `get_settings()` loads from `backend/.env`.

Verify:

```powershell
cd backend
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -c "from app.core.config import get_settings; print(get_settings().database_url)"
```

### Step 6 — SQLAlchemy dependencies

Added to `requirements.txt`:

| Package | Purpose |
|---------|---------|
| `sqlalchemy` | Python ORM — maps classes to SQL tables |
| `psycopg2-binary` | PostgreSQL driver — connects Python to Postgres |

Verify:

```powershell
cd backend
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -c "import sqlalchemy; import psycopg2; print('sqlalchemy', sqlalchemy.__version__)"
```

### Step 7 — Database engine + session

`app/core/database.py`:

| Piece | Role |
|-------|------|
| `engine` | Connection pool to Postgres (uses `DATABASE_URL`) |
| `SessionLocal` | Factory for DB sessions |
| `get_db()` | FastAPI dependency — opens/closes a session per request |

Verify connection:

```powershell
cd backend
.\.venv\Scripts\python -c "from sqlalchemy import text; from app.core.database import engine; engine.connect().execute(text('SELECT 1')); print('db ok')"
```

### Step 8 — Model base class

`app/models/base.py` — shared `Base` for all SQLAlchemy table models (Steps 9–10).

All models will inherit from `Base` so Alembic can discover and migrate them.

Verify:

```powershell
cd backend
.\.venv\Scripts\python -c "from app.models.base import Base; print('Base', Base)"
```

### Step 9 — Organization model

`app/models/organization.py` → table `organizations`

| Column | Type |
|--------|------|
| `id` | UUID (primary key) |
| `name` | string |
| `created_at` | timestamp (auto) |

Verify:

```powershell
cd backend
.\.venv\Scripts\python -c "from app.models.organization import Organization; print(Organization.__tablename__)"
```

### Step 10 — User model

`app/models/user.py` → table `users`

| Column | Type |
|--------|------|
| `id` | UUID (primary key) |
| `organization_id` | UUID → `organizations.id` |
| `email` | string |
| `password_hash` | string |
| `role` | `admin` / `manager` / `employee` |
| `created_at` | timestamp (auto) |

Unique per org: `(organization_id, email)`.

`UserRole` enum included here (covers planned Step 18).

Verify:

```powershell
cd backend
.\.venv\Scripts\python -c "from app.models.user import User, UserRole; print(User.__tablename__, UserRole.ADMIN.value)"
```

### Step 11 — Model exports

`app/models/__init__.py` re-exports `Base`, `Organization`, `User`, `UserRole` so Alembic and the app can import from `app.models`.

Verify:

```powershell
cd backend
.\.venv\Scripts\python -c "from app.models import Base, Organization, User, UserRole; print(list(Base.metadata.tables))"
```

Should list `organizations` and `users`.

### Step 12 — Alembic init

Database migrations tool — reads models from `Base.metadata` and applies schema changes.

Added `alembic` to `requirements.txt` and:

```
backend/
  alembic.ini
  alembic/
    env.py          # wired to .env DATABASE_URL + app.models.Base
    versions/       # migration scripts (Step 13)
```

Verify (no migrations yet — empty history is OK):

```powershell
cd backend
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\alembic history
```

### Step 13 — First migration

Autogenerated migration creating `organizations` and `users`:

```
backend/alembic/versions/35af7ef40689_create_organizations_and_users.py
```

Review the file, then apply in Step 14:

```powershell
cd backend
.\.venv\Scripts\alembic history
```

Should show one revision: `create organizations and users`.

### Step 14 — Run migration

Applies the migration to Postgres (`eka`):

```powershell
cd backend
.\.venv\Scripts\alembic upgrade head
```

Verify:

```powershell
.\.venv\Scripts\alembic current
# 35af7ef40689 (head)

.\.venv\Scripts\python -c "from sqlalchemy import inspect; from app.core.database import engine; print(inspect(engine).get_table_names())"
# alembic_version, organizations, users
```

Or in pgAdmin: refresh `eka` → see `organizations`, `users`, `alembic_version`.

### Step 15 — Password hash / verify

**Why:** Never store plain passwords. Store a **one-way hash** in `users.password_hash`.

| Function | Use |
|----------|-----|
| `hash_password(plain)` | On **register** — save hash to DB |
| `verify_password(plain, hash)` | On **login** — check password matches |

Uses **bcrypt** via `passlib` (slow by design → harder to brute-force).

Flow:

```
Register:  "superuser123"  →  hash  →  "$2b$12$..."  →  DB
Login:     "superuser123"  +  hash from DB  →  verify  →  True/False
```

Verify:

```powershell
cd backend
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -c "from app.core.security import hash_password, verify_password; h=hash_password('test'); print(verify_password('test', h), verify_password('wrong', h))"
```

Should print: `True False`

### Step 16 — JWT create / decode

**Why:** After login, the client sends a **JWT** (JSON Web Token) instead of email/password on every request.

Token = signed string containing claims:

| Claim | Meaning |
|-------|---------|
| `sub` | `user_id` |
| `organization_id` | tenant |
| `role` | `admin` / `manager` / `employee` |
| `exp` | expiry time |

| Function | Use |
|----------|-----|
| `create_access_token(...)` | **Login** — build token after password OK |
| `decode_access_token(token)` | **Protected routes** — read claims (Step 22+) |

Uses `JWT_SECRET` and `JWT_EXPIRE_MINUTES` from `.env`.

Verify:

```powershell
cd backend
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -c "from app.core.security import create_access_token, decode_access_token; t=create_access_token(user_id='u1', organization_id='o1', role='admin'); print(decode_access_token(t)['role'])"
```

Should print: `admin`

---

## Next

**Step 17** — `app/schemas/auth.py` (register/login request + token response)
