# General imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Database and initialization imports
from .database.db import SessionLocal
from .database.init_admin import init_root_admin
# Router imports
from .routers.students_router import router as students_router
from .routers.admin_router import router as admin_router
# Services imports
from .services.api_rate_limit import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to initialize resources when the application starts and clean up when it shuts down."""
    db = SessionLocal()
    try:
        init_root_admin(db) # Ensure the root admin user is created or updated at startup
    finally:
        db.close()
    yield # Syntax required for async context manager, allows the application to run until shutdown


# Initialize the FastAPI application
app = FastAPI(
    title="Smart Campus Assistant API",
    description="Backend service for the Smart Campus Assistant application.",
    version="1.0.0",
    lifespan=lifespan
)

# Register the rate limiter and its exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS for React frontend integration
# React development servers typically run on port 3000 or 5173 (Vite)
# TODO: Make this more flexible by using environment variables or configuration files for allowed origins
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Configure routers for API endpoints
app.include_router(students_router, prefix="/api", tags=["Student Assistant"]) # All routes in this router will be prefixed with /api =(e.g., /api/ask)
app.include_router(admin_router, prefix="/api/admin", tags=["Admin Management"])


# Health check endpoint to verify the server is running successfully
@app.get("/")
async def root():
    return {"status": "ok", "message": "Smart Campus Assistant API is running"}


if __name__ == "__main__":
    # Run the server using uvicorn when executing this file directly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)