from fastapi import APIRouter

from app.agents.director import ResearchDirector
from app.models.research import ResearchRequest
from app.services.fireworks import FireworksService
from app.workflows.research_graph import ResearchWorkflow
from app.knowledge.notebook import ResearchNotebook

router = APIRouter()

director = ResearchDirector()
fireworks = FireworksService()
workflow = ResearchWorkflow()
notebook = ResearchNotebook()


@router.post("/research")
async def research(request: ResearchRequest):
    """
    Runs the full ResearchOS research workflow.

    This endpoint now does more than planning:
    it plans, retrieves evidence, ranks papers, analyzes them,
    detects gaps, and generates a markdown report.
    """

    return await workflow.run(request.question)


@router.post("/research/plan")
def research_plan(request: ResearchRequest):
    """
    Returns only the Director's planning output.

    Useful for debugging team assembly and notebook memory.
    """

    return director.create_plan(request.question)

@router.get("/notebook")
def list_notebook_entries():
    """
    Returns all saved research investigations, newest first.
    """

    return {
        "entries": notebook.list_entries()
    }


@router.get("/notebook/{entry_id}")
def get_notebook_entry(entry_id: str):
    """
    Returns one saved investigation by ID.
    """

    entry = notebook.get_entry(entry_id)

    if entry is None:
        return {
            "error": "Notebook entry not found."
        }

    return entry

@router.get("/ai/status")
def ai_status():
    """
    Shows whether Fireworks AI is configured.
    """

    return {
        "fireworks_configured": fireworks.available()
    }


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "researchos-backend"
    }