# Environment Variables

This project reads environment variables mainly from a .env file in backend.

## Where To Put .env

Create this file:

- backend/.env

## Required For Core Assistant

### OPENAI_API_KEY

- Required: Yes (if you use /api/ask)
- Example: OPENAI_API_KEY=sk-...
- Used by: backend/services/ai_service.py
- Impact if missing: AI responses fail and fallback error handling is triggered.

## Database

### DATABASE_URL

- Required: No (default exists)
- Default: sqlite:///./database/campus_data.db
- Example (PostgreSQL): DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/campus
- Used by: backend/database/db.py

## Authentication

### JWT_SECRET_KEY

- Required: Not technically required (has fallback), but required for any secure environment
- Example: JWT_SECRET_KEY=replace-with-long-random-secret
- Used by: backend/services/auth_service.py

### ALGORITHM

- Required: No
- Default: HS256
- Example: ALGORITHM=HS256
- Used by: backend/services/auth_service.py

### ACCESS_TOKEN_EXPIRE_MINUTES

- Required: No
- Default: 30
- Example: ACCESS_TOKEN_EXPIRE_MINUTES=60
- Used by: backend/services/auth_service.py

## Root Admin Bootstrap

The backend startup lifecycle creates or synchronizes a fixed root admin user.

### ROOT_ADMIN_EMAIL

- Required: No
- Default: root@campus.ac.il
- Example: ROOT_ADMIN_EMAIL=admin@your-campus.edu
- Used by: backend/database/init_admin.py

### ROOT_ADMIN_PASSWORD

- Required: No
- Default: admin123
- Example: ROOT_ADMIN_PASSWORD=change-me-now
- Used by: backend/database/init_admin.py

## Recommended .env Example

~~~dotenv
# AI
OPENAI_API_KEY=sk-...

# Database
DATABASE_URL=sqlite:///./database/campus_data.db

# JWT
JWT_SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Root Admin
ROOT_ADMIN_EMAIL=root@campus.ac.il
ROOT_ADMIN_PASSWORD=change-this-password
~~~

## Production Guidance

- Never use the default JWT or admin password values in production.
- Keep secrets out of source control.
- Use a managed production database instead of local SQLite.
- Rotate credentials periodically.
