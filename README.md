# Smart Campus Assistant

Smart Campus Assistant is a full-stack campus support system that combines:

- A student-facing AI Q&A assistant
- An admin panel for managing campus knowledge (FAQs, rooms, exams, reception hours, users)
- A FastAPI backend with JWT authentication and rate limiting
- A React + Vite frontend for admin and student workflows

The project is designed to answer student questions using trusted campus data stored in your own database, while giving administrators a controlled way to keep that data updated.

## Table Of Contents

- [What The System Does](#what-system-does)
- [Project Structure](#project-structure)
- [Architecture Summary](#architecture-summary)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Required Environment Variables](#required-env-vars)
- [Run The System](#run-system)
- [Database And Migrations](#database-migrations)
- [Authentication And Roles](#authentication-roles)
- [API Overview](#api-overview)
- [Testing](#testing)
- [Notes](#notes)
- [Additional Documentation](#additional-docs)

<a id="what-system-does"></a>
## 🎯 What The System Does

- Authenticated students can ask natural-language questions through the assistant endpoint.
- The backend retrieves relevant campus context from the database.
- The AI service generates an answer based only on that context.
- Admin users can log in and manage core campus knowledge entities.
- A root admin account is auto-bootstrapped on backend startup.

<a id="project-structure"></a>
## 🗂️ Project Structure

- backend: FastAPI application, database, business services, Alembic migrations, tests
- frontend: React + Vite client application
- docs: supplementary project documentation

For a deeper architecture breakdown, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

<a id="architecture-summary"></a>
## 🏗️ Architecture Summary

At a high level:

1. Frontend sends authenticated API requests (Bearer JWT).
2. FastAPI routes validate/authenticate requests.
3. Service layer fetches relevant data from SQLAlchemy models.
4. AI service calls OpenAI with strict context-bound prompting.
5. Structured response returns to the client.

More details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

<a id="prerequisites"></a>
## ✅ Prerequisites

- Python 3.11+ recommended
- Node.js 18+ recommended
- npm 9+ recommended

<a id="installation"></a>
## ⚙️ Installation

<details>
<summary>Show installation steps</summary>

### 1. Clone the repository

~~~bash
git clone https://github.com/YaliB/Smart-Campus-Assistant.git
cd Smart-Campus-Assistant
~~~

### 2. Backend setup

~~~bash
cd backend
python -m venv venv
~~~

Activate the virtual environment:

Windows (PowerShell):

~~~powershell
.\venv\Scripts\Activate.ps1
~~~

macOS/Linux (bash/zsh):

~~~bash
source venv/bin/activate
~~~

Install dependencies:

~~~bash
pip install -r requirements.txt
~~~

### 3. Frontend setup

Open a new terminal and run:

~~~bash
cd frontend
npm install
~~~

</details>

<a id="required-env-vars"></a>
## 🔐 Required Environment Variables

Create a .env file inside backend and configure the variables below.

See full explanations and production notes in [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md).

| Variable | Required | Example | Purpose |
|---|---|---|---|
| OPENAI_API_KEY | Yes (for AI answers) | sk-... | OpenAI key used by the AI service |
| DATABASE_URL | Optional (has default) | sqlite:///./database/campus_data.db | SQLAlchemy database connection |
| JWT_SECRET_KEY | Strongly recommended | change-this-secret | JWT signing secret |
| ALGORITHM | Optional | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | Optional | 30 | JWT lifetime in minutes |
| ROOT_ADMIN_EMAIL | Optional | root@campus.ac.il | Root admin email bootstrapped at startup |
| ROOT_ADMIN_PASSWORD | Optional | admin123 | Root admin password bootstrapped at startup |

<a id="run-system"></a>
## ▶️ Run The System

<details>
<summary>Show run commands (backend + frontend)</summary>

Run backend and frontend in separate terminals.

### Terminal A: Start backend

From backend directory with venv activated:

~~~bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
~~~

If running from inside backend, use:

~~~bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
~~~

Backend health check:

- http://localhost:8000/
- Swagger UI: http://localhost:8000/docs

### Terminal B: Start frontend

From frontend directory:

~~~bash
npm run dev
~~~

Typical dev URL:

- http://localhost:5173

</details>

<a id="database-migrations"></a>
## 🗄️ Database And Migrations

<details>
<summary>Show migration and seed commands</summary>

The backend uses SQLAlchemy + Alembic.

From backend directory (with venv activated):

~~~bash
alembic upgrade head
~~~

Create a new migration:

~~~bash
alembic revision --autogenerate -m "your message"
~~~

Optional: seed demo campus data:

~~~bash
python seed.py
~~~

</details>

<a id="authentication-roles"></a>
## 👤 Authentication And Roles

- JWT Bearer authentication is required for protected routes.
- Student assistant endpoint /api/ask requires a valid token.
- Admin routes under /api/admin/* are restricted to admin users.
- Root admin account is initialized/synchronized at startup from env variables.

<a id="api-overview"></a>
## 📡 API Overview

<details>
<summary>Show endpoints</summary>

- GET /: health check
- POST /api/ask: ask the assistant (authenticated)
- POST /api/admin/login: admin login
- CRUD under /api/admin/users
- CRUD under /api/admin/faq
- CRUD under /api/admin/rooms
- CRUD under /api/admin/exams
- CRUD under /api/admin/reception

</details>

<a id="testing"></a>
## 🧪 Testing

From backend directory (with venv activated):

~~~bash
pytest tests/
~~~

<a id="notes"></a>
## 📝 Notes

<details>
<summary>Show implementation notes</summary>

- Frontend API base URL is currently hardcoded to http://localhost:8000 in frontend/src/services/api.js.
- CORS allowlist is currently configured in backend/main.py for localhost ports used in development.
- For production deployment, lock down CORS, set a strong JWT secret, and configure a production-grade database.

</details>

<a id="additional-docs"></a>
## 📚 Additional Documentation

- Environment variables: [docs/ENVIRONMENT.md](docs/ENVIRONMENT.md)
- Architecture details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
