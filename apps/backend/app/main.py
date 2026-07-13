from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

# -----------------------------------------------------------------------------
# Create the FastAPI application
# -----------------------------------------------------------------------------
app = FastAPI(
    title="ResearchOS API",
    description="Autonomous AI research laboratory backend",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Allow the Next.js frontend to communicate with this backend.
#
# During development the frontend runs on localhost:3000 while the backend runs
# on localhost:8000, so browsers require CORS to be enabled.
#
# When deploying later we'll replace "*" with the actual frontend domain.
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://research-ptkq0a6d8-limarco48.vercel.app/",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routes
app.include_router(router)


@app.get("/")
def root():
    """
    Simple health check endpoint.
    """
    return {
        "name": "ResearchOS",
        "status": "running",
        "message": "ResearchOS backend is alive.",
    }