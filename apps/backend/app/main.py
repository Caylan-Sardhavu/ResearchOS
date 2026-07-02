from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="ResearchOS API",
    description="Autonomous AI research laboratory backend",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "ResearchOS",
        "status": "running",
        "message": "ResearchOS backend is alive.",
    }