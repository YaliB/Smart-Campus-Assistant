# Architecture

## Short Description

Smart Campus Assistant uses a layered architecture:

- Frontend (React + Vite) for user/admin interactions
- Backend API (FastAPI) for routing, authentication, and orchestration
- Service layer for business logic and integrations
- Data layer (SQLAlchemy + Alembic) for persistence and schema evolution
- OpenAI integration for context-aware answer generation

## Component Overview

### Frontend

Main responsibilities:

- Admin authentication flow
- Data management screens (users, FAQ, rooms, exams, reception)
- Chat-like student interaction flow
- Sending JWT in Authorization headers via Axios interceptor

Key location:

- frontend/src/services/api.js

### Backend API (FastAPI)

Main responsibilities:

- Request validation through Pydantic schemas
- Route protection using OAuth2 bearer tokens
- Admin-only authorization checks
- Rate limiting sensitive endpoints

Routing layout:

- /api/ask for student assistant questions
- /api/admin/login for authentication
- /api/admin/* for protected admin CRUD

Key locations:

- backend/main.py
- backend/routers/students_router.py
- backend/routers/admin_router.py
- backend/routers/admin/

### Service Layer

Main responsibilities:

- auth_service.py: password hashing, JWT creation/validation, auth dependencies
- db_service.py: extracting relevant local context from campus data
- ai_service.py: calling OpenAI and enforcing context-bound prompting strategy
- api_rate_limit.py: deriving keys for request throttling

Key location:

- backend/services/

### Data Layer

Main responsibilities:

- SQLAlchemy models for users and campus entities
- Session/engine initialization from DATABASE_URL
- Alembic migrations and versioning
- Root admin bootstrap logic at startup

Key locations:

- backend/database/db_models.py
- backend/database/db.py
- backend/database/init_admin.py
- backend/alembic/

## Runtime Flow (Student Question)

1. Client sends POST /api/ask with JWT and question payload.
2. FastAPI validates token and request body.
3. Backend fetches relevant context from local DB.
4. AI service sends question + local context to OpenAI.
5. Model returns strict JSON with answer and category.
6. API returns AskResponse to frontend.

## Security Boundaries

- Authentication: JWT bearer tokens
- Authorization: admin-only dependencies for management routes
- Passwords: bcrypt hashing via passlib
- Rate limiting: request caps on login and /api/ask

## Development Assumptions

- Frontend calls backend at http://localhost:8000 by default.
- CORS allowlist currently includes common local Vite/React ports.
- SQLite default is used when DATABASE_URL is not provided.

## Future Improvements

- Move frontend baseURL to a Vite environment variable.
- Move backend CORS origins to environment configuration.
- Add structured logging and observability.
- Add integration tests for auth + assistant flows.
