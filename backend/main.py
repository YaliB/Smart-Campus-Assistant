# General imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import Routers for API endpoints
from backend.routers.api_router import api_router
# from api.admin_routes import admin_router

# Initialize the FastAPI application
app = FastAPI(
    title="Smart Campus Assistant API",
    description="Backend service for the Smart Campus Assistant application.",
    version="1.0.0"
)

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
app.include_router(api_router, prefix="/api", tags=["Student Assistant"]) # All routes in this router will be prefixed with /api =(e.g., /api/ask)
# TODO for future implementation: Include the Admin router
# app.include_router(admin_router, prefix="/admin", tags=["Admin Management"])


# Health check endpoint to verify the server is running successfully
@app.get("/")
async def root():
    return {"status": "ok", "message": "Smart Campus Assistant API is running"}


if __name__ == "__main__":
    # Run the server using uvicorn when executing this file directly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)