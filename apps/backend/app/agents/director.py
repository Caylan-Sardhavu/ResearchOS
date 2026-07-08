from app.agents.base import AgentProfile
from app.knowledge.notebook import ResearchNotebook
from app.models.research import ResearchResponse
from app.services.planner import PlannerService


class ResearchDirector:
    def __init__(self):
        self.notebook = ResearchNotebook()
        self.planner = PlannerService()

    def create_plan(self, question: str) -> ResearchResponse:
        matches = self.notebook.search(question)
        research_plan = self.planner.create_plan(question)
        selected_agents = self._select_agents(question)
        complexity = self._estimate_complexity(question)

        return ResearchResponse(
            question=question,
            complexity=complexity,
            notebook_matches=matches,
            research_plan=research_plan,
            selected_agents=selected_agents,
            director_notes=[
                "Checked the Research Notebook for similar previous work.",
                "Created a structured research plan.",
                "Selected specialist agents using fallback rule-based planning.",
                "Prepared an initial research team for this investigation.",
            ],
            ai_used=False,
        )

    def _select_agents(self, question: str) -> list[AgentProfile]:
        q = question.lower()

        agents = [
            AgentProfile(
                name="Research Planner",
                department="Strategy",
                role="Planner",
                description="Breaks the research question into investigation steps.",
            ),
            AgentProfile(
                name="Evidence Synthesizer",
                department="Knowledge",
                role="Synthesizer",
                description="Combines findings into coherent evidence-backed insights.",
            ),
        ]

        if any(word in q for word in ["paper", "literature", "study", "research", "journal"]):
            agents.append(
                AgentProfile(
                    name="Literature Specialist",
                    department="Literature",
                    role="Retriever",
                    description="Finds relevant academic papers and open-access sources.",
                )
            )

        if any(word in q for word in ["benchmark", "gpu", "amd", "nvidia", "rocm", "cuda", "inference"]):
            agents.append(
                AgentProfile(
                    name="Benchmark Analyst",
                    department="Engineering",
                    role="Benchmark Analyst",
                    description="Analyzes technical benchmarks, hardware comparisons, and performance claims.",
                )
            )

        if any(word in q for word in ["gap", "unexplored", "opportunity", "future work", "novel"]):
            agents.append(
                AgentProfile(
                    name="Research Gap Detector",
                    department="Discovery",
                    role="Gap Detector",
                    description="Identifies missing, weak, or underexplored areas in the research landscape.",
                )
            )

        if any(word in q for word in ["contradiction", "bias", "reliable", "validate", "evidence"]):
            agents.append(
                AgentProfile(
                    name="Skeptic Reviewer",
                    department="Validation",
                    role="Reviewer",
                    description="Challenges claims, checks reliability, and looks for contradictions.",
                )
            )

        agents.append(
            AgentProfile(
                name="Research Writer",
                department="Publication",
                role="Writer",
                description="Produces the final structured research report.",
            )
        )

        return agents

    def _estimate_complexity(self, question: str) -> str:
        q = question.lower()
        word_count = len(question.split())

        if word_count > 18:
            return "high"

        if any(word in q for word in ["compare", "gap", "benchmark", "systematic", "literature review"]):
            return "medium"

        return "low"