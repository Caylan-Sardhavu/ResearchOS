from pydantic import BaseModel

from app.agents.base import AgentProfile


class ResearchRequest(BaseModel):
    question: str


class ResearchPlan(BaseModel):
    question: str
    complexity: str
    notebook_matches: list[str]
    selected_agents: list[AgentProfile]
    director_notes: list[str]