from fastapi import APIRouter

from app.agents.director import ResearchDirector
from app.models.research import ResearchRequest
from app.services.fireworks import FireworksService

router = APIRouter()

director = ResearchDirector()
fireworks = FireworksService()


@router.post("/research")
def research(request: ResearchRequest):
    return director.create_plan(request.question)


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "researchos-backend"
    }

@router.get("/ai/status")
def ai_status():
    return {
        "fireworks_configured": fireworks.available()
    }