from pydantic import BaseModel

from app.agents.base import AgentProfile


class ResearchRequest(BaseModel):
    question: str


class ResearchPlan(BaseModel):
    objective: str
    subquestions: list[str]
    search_queries: list[str]


class ResearchResponse(BaseModel):
    question: str
    complexity: str
    notebook_matches: list[str]
    research_plan: ResearchPlan
    selected_agents: list[AgentProfile]
    director_notes: list[str]
    ai_used: bool