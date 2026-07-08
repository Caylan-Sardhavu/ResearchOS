from app.models.research import ResearchPlan


class PlannerService:

    def create_plan(self, question: str) -> ResearchPlan:

        q = question.lower()

        search_queries = [question]

        subquestions = []

        if "amd" in q:
            search_queries.append("AMD GPU performance")

        if "rocm" in q:
            search_queries.append("ROCm optimization")

        if "transformer" in q:
            search_queries.append("Transformer inference")
            search_queries.append("LLM inference AMD GPU")

            subquestions.extend(
                [
                    "What transformer optimization methods exist?",
                    "Which AMD GPUs are evaluated?",
                    "Which benchmarks are commonly used?",
                    "What limitations are repeatedly mentioned?",
                    "What research gaps remain?",
                ]
            )

        return ResearchPlan(
            objective=f"Investigate: {question}",
            subquestions=subquestions,
            search_queries=list(dict.fromkeys(search_queries)),
        )