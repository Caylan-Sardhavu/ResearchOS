from fastapi import APIRouter

from app.agents.director import ResearchDirector
from app.models.research import ResearchRequest

router = APIRouter()

director = ResearchDirector()


@router.post("/research")
def research(request: ResearchRequest):
    return director.create_plan(request.question)


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "researchos-backend"
    }