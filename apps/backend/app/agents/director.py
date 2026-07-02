from app.agents.base import AgentProfile
from app.knowledge.notebook import ResearchNotebook
from app.models.research import ResearchPlan


class ResearchDirector:
    def __init__(self):
        self.notebook = ResearchNotebook()

    def create_plan(self, question: str) -> ResearchPlan:
        matches = self.notebook.search(question)
        selected_agents = self._select_agents(question)
        complexity = self._estimate_complexity(question)

        return ResearchPlan(
            question=question,
            complexity=complexity,
            notebook_matches=matches,
            selected_agents=selected_agents,
            director_notes=[
                "Checked the Research Notebook for similar previous work.",
                "Selected specialist agents based on the question type.",
                "Prepared an initial research team for this investigation.",
            ],
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
        word_count = len(question.split())

        if word_count > 18:
            return "high"

        if any(word in question.lower() for word in ["compare", "gap", "benchmark", "systematic", "literature review"]):
            return "medium"

        return "low"