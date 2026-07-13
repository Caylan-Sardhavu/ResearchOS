import json
import re
from typing import Any

from app.models.research import ResearchPlan
from app.services.fireworks import FireworksService


class PlannerService:
    """
    Creates a structured investigation plan for a research question.

    Fireworks generates the objective, subquestions, and search queries.
    If Fireworks is unavailable or returns invalid data, ResearchOS uses
    the deterministic fallback planner.
    """

    def __init__(self) -> None:
        self.fireworks = FireworksService()

    async def create_plan(self, question: str) -> ResearchPlan:
        """
        Creates a research plan using Fireworks when available.

        The fallback planner ensures the investigation can continue even
        when the external AI service is unavailable.
        """

        fallback_plan = self._create_fallback_plan(question)

        if not self.fireworks.available():
            return fallback_plan

        ai_plan = await self._create_ai_plan(question)

        if ai_plan is None:
            return fallback_plan

        return ai_plan

    async def _create_ai_plan(
        self,
        question: str,
    ) -> ResearchPlan | None:
        """
        Asks Fireworks to generate a focused research strategy.
        """

        prompt = f"""
Create a structured research investigation plan for this question:

{question}

Return only valid JSON using exactly this structure:

{{
  "objective": "one concise research objective",
  "subquestions": [
    "subquestion 1",
    "subquestion 2"
  ],
  "search_queries": [
    "search query 1",
    "search query 2"
  ]
}}

Requirements:
- Return exactly 5 subquestions.
- Return between 4 and 6 search queries.
- Search queries must be concise and suitable for academic databases.
- Include the original question as the first search query.
- Cover methods, evidence, limitations, comparisons, and research gaps.
- Do not include Markdown.
- Do not include text outside the JSON object.
""".strip()

        result = await self.fireworks.chat(
            prompt=prompt,
            system_prompt=(
                "You are a senior academic research planner. "
                "You decompose research questions into precise investigation "
                "steps and academic search queries. Return strict JSON."
            ),
            max_tokens=650,
            temperature=0.1,
        )

        if not result.get("success"):
            print(
                "Fireworks Planner fallback:",
                result.get("message", "Unknown Fireworks error"),
            )
            return None

        response_text = result.get("response")

        if not isinstance(response_text, str):
            return None

        parsed = self._parse_json_object(response_text)

        if parsed is None:
            print("Fireworks Planner fallback: invalid JSON response.")
            return None

        return self._validate_ai_plan(
            data=parsed,
            original_question=question,
        )

    def _validate_ai_plan(
        self,
        data: dict[str, Any],
        original_question: str,
    ) -> ResearchPlan | None:
        """
        Validates and normalizes the Fireworks-generated plan.
        """

        objective = data.get("objective")
        subquestions = data.get("subquestions")
        search_queries = data.get("search_queries")

        if not isinstance(objective, str) or not objective.strip():
            return None

        if not isinstance(subquestions, list):
            return None

        if not isinstance(search_queries, list):
            return None

        clean_subquestions = [
            item.strip()
            for item in subquestions
            if isinstance(item, str) and item.strip()
        ]

        clean_search_queries = [
            item.strip()
            for item in search_queries
            if isinstance(item, str) and item.strip()
        ]

        # Ensure the original question is always searched.
        if original_question not in clean_search_queries:
            clean_search_queries.insert(0, original_question)

        # Remove duplicates while preserving order.
        clean_subquestions = list(dict.fromkeys(clean_subquestions))
        clean_search_queries = list(dict.fromkeys(clean_search_queries))

        if not clean_subquestions or not clean_search_queries:
            return None

        return ResearchPlan(
            objective=objective.strip(),
            subquestions=clean_subquestions[:5],
            search_queries=clean_search_queries[:6],
        )

    def _parse_json_object(
        self,
        response_text: str,
    ) -> dict[str, Any] | None:
        """
        Extracts a JSON object from a Fireworks response.
        """

        cleaned = response_text.strip()

        # Remove accidental Markdown code fences.
        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            parsed = json.loads(cleaned)

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError:
            pass

        # Recover an object if the model included surrounding text.
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1 or end <= start:
            return None

        try:
            parsed = json.loads(cleaned[start : end + 1])

            if isinstance(parsed, dict):
                return parsed

        except json.JSONDecodeError:
            return None

        return None

    def _create_fallback_plan(
        self,
        question: str,
    ) -> ResearchPlan:
        """
        Existing deterministic research planner.

        This keeps ResearchOS operational without Fireworks.
        """

        q = question.lower()

        search_queries = [question]
        subquestions: list[str] = []

        if "amd" in q:
            search_queries.append("AMD GPU performance")

        if "rocm" in q:
            search_queries.append("ROCm optimization")

        if "transformer" in q:
            search_queries.extend(
                [
                    "Transformer inference",
                    "LLM inference AMD GPU",
                ]
            )

            subquestions.extend(
                [
                    "What transformer optimization methods exist?",
                    "Which AMD GPUs are evaluated?",
                    "Which benchmarks are commonly used?",
                    "What limitations are repeatedly mentioned?",
                    "What research gaps remain?",
                ]
            )

        # Generic fallback questions keep the planner useful for any field.
        if not subquestions:
            subquestions = [
                "What are the major approaches in the current literature?",
                "What evidence supports the main claims?",
                "Which methods and datasets are commonly used?",
                "What limitations or disagreements appear across studies?",
                "What important research gaps remain?",
            ]

        return ResearchPlan(
            objective=f"Investigate: {question}",
            subquestions=subquestions,
            search_queries=list(dict.fromkeys(search_queries)),
        )