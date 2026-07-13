import json
import re
from typing import Any

from app.agents.base import AgentProfile
from app.knowledge.notebook import ResearchNotebook
from app.models.research import ResearchResponse
from app.services.fireworks import FireworksService
from app.services.planner import PlannerService


class ResearchDirector:
    """
    Orchestrates the beginning of a ResearchOS investigation.

    Fireworks is used to estimate complexity and dynamically select
    specialist agents. If Fireworks is unavailable or returns invalid
    data, the existing deterministic logic is used automatically.
    """

    def __init__(self) -> None:
        self.notebook = ResearchNotebook()
        self.planner = PlannerService()
        self.fireworks = FireworksService()

    async def create_plan(self, question: str) -> ResearchResponse:
        """
        Creates the initial research plan and specialist team.

        The structured research plan still comes from PlannerService.
        Fireworks currently improves the Director's complexity estimate,
        agent selection, and notes.
        """

        matches = self.notebook.search(question)
        research_plan = await self.planner.create_plan(question)

        # Start with the reliable fallback values.
        selected_agents = self._select_agents_fallback(question)
        complexity = self._estimate_complexity_fallback(question)
        director_notes = [
            "Checked the Research Notebook for similar previous work.",
            "Created a structured research plan.",
            "Selected specialist agents using fallback rule-based planning.",
            "Prepared an initial research team for this investigation.",
        ]
        ai_used = False

        # Try Fireworks only when it is configured and enabled.
        if self.fireworks.available():
            ai_result = await self._create_ai_direction(
                question=question,
                notebook_matches=matches,
            )

            if ai_result is not None:
                complexity = ai_result["complexity"]
                selected_agents = ai_result["selected_agents"]
                director_notes = ai_result["notes"]
                ai_used = True

        return ResearchResponse(
            question=question,
            complexity=complexity,
            notebook_matches=matches,
            research_plan=research_plan,
            selected_agents=selected_agents,
            director_notes=director_notes,
            ai_used=ai_used,
        )

    async def _create_ai_direction(
        self,
        question: str,
        notebook_matches: list[str],
    ) -> dict[str, Any] | None:
        """
        Asks Fireworks to classify the investigation and choose agents.

        Returns None when Fireworks fails or its response cannot be
        validated, which causes the caller to keep fallback results.
        """

        available_agent_names = list(self._agent_catalog().keys())

        prompt = f"""
Analyze the following research question and assemble an appropriate
specialist research team.

Research question:
{question}

Related previous notebook work:
{json.dumps(notebook_matches)}

Available agents:
{json.dumps(available_agent_names)}

Return only valid JSON with exactly this structure:

{{
  "complexity": "low, medium, or high",
  "selected_agents": [
    "agent name from the available agents list"
  ],
  "notes": [
    "short explanation of a Director decision"
  ]
}}

Requirements:
- Always include Research Planner.
- Always include Evidence Synthesizer.
- Always include Research Writer.
- Select only agents from the available agents list.
- Select specialists that are relevant to the question.
- Use between 3 and 7 agents.
- Return exactly 3 concise notes.
- Each note must contain fewer than 15 words.
- Do not include Markdown or text outside the JSON object.
""".strip()

        result = await self.fireworks.chat(
            prompt=prompt,
            system_prompt=(
                "You are the Research Director of an autonomous AI "
                "research laboratory. You classify investigations and "
                "assemble specialist research teams. Return strict JSON."
            ),
            max_tokens=500,
            temperature=0.1,
        )

        if not result.get("success"):
            print(
                "Fireworks Director fallback:",
                result.get("message", "Unknown Fireworks error"),
            )
            return None

        response_text = result.get("response")

        if not isinstance(response_text, str):
            return None

        parsed = self._parse_json_object(response_text)

        if parsed is None:
            print("Fireworks Director fallback: invalid JSON response.")
            return None

        return self._validate_ai_direction(parsed)

    def _validate_ai_direction(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Validates the model response and converts agent names into
        AgentProfile objects used by the rest of ResearchOS.
        """

        complexity = str(data.get("complexity", "")).lower().strip()

        if complexity not in {"low", "medium", "high"}:
            return None

        raw_agent_names = data.get("selected_agents")
        raw_notes = data.get("notes")

        if not isinstance(raw_agent_names, list):
            return None

        if not isinstance(raw_notes, list):
            return None

        catalog = self._agent_catalog()

        # Remove unknown and duplicate agent names.
        valid_agent_names: list[str] = []

        for name in raw_agent_names:
            if not isinstance(name, str):
                continue

            cleaned_name = name.strip()

            if (
                cleaned_name in catalog
                and cleaned_name not in valid_agent_names
            ):
                valid_agent_names.append(cleaned_name)

        # These agents are required for every investigation.
        required_agents = [
            "Research Planner",
            "Evidence Synthesizer",
            "Research Writer",
        ]

        for required_name in required_agents:
            if required_name not in valid_agent_names:
                valid_agent_names.append(required_name)

        # Limit the team to prevent unnecessarily large outputs.
        valid_agent_names = valid_agent_names[:7]

        selected_agents = [
            catalog[name]
            for name in valid_agent_names
        ]

        notes = [
            note.strip()
            for note in raw_notes
            if isinstance(note, str) and note.strip()
        ][:4]

        if not notes:
            notes = [
                "Checked the Research Notebook for related previous work.",
                "Created a structured investigation plan.",
                "Used Fireworks AI to assess complexity and team composition.",
                "Assembled specialist agents for the research question.",
            ]

        return {
            "complexity": complexity,
            "selected_agents": selected_agents,
            "notes": notes,
        }

    def _parse_json_object(
        self,
        response_text: str,
    ) -> dict[str, Any] | None:
        """
        Parses a JSON object from a model response.

        This also handles accidental Markdown code fences without
        allowing malformed responses into the research workflow.
        """

        cleaned = response_text.strip()

        # Remove common Markdown JSON fences.
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

        # As a final recovery step, extract the outer JSON object.
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

    def _agent_catalog(self) -> dict[str, AgentProfile]:
        """
        Defines every specialist the AI Director may select.
        """

        return {
            "Research Planner": AgentProfile(
                name="Research Planner",
                department="Strategy",
                role="Planner",
                description=(
                    "Breaks the research question into investigation steps."
                ),
            ),
            "Evidence Synthesizer": AgentProfile(
                name="Evidence Synthesizer",
                department="Knowledge",
                role="Synthesizer",
                description=(
                    "Combines findings into coherent evidence-backed insights."
                ),
            ),
            "Literature Specialist": AgentProfile(
                name="Literature Specialist",
                department="Literature",
                role="Retriever",
                description=(
                    "Finds relevant academic papers and open-access sources."
                ),
            ),
            "Benchmark Analyst": AgentProfile(
                name="Benchmark Analyst",
                department="Engineering",
                role="Benchmark Analyst",
                description=(
                    "Analyzes technical benchmarks, hardware comparisons, "
                    "and performance claims."
                ),
            ),
            "Research Gap Detector": AgentProfile(
                name="Research Gap Detector",
                department="Discovery",
                role="Gap Detector",
                description=(
                    "Identifies missing, weak, or underexplored areas in "
                    "the research landscape."
                ),
            ),
            "Skeptic Reviewer": AgentProfile(
                name="Skeptic Reviewer",
                department="Validation",
                role="Reviewer",
                description=(
                    "Challenges claims, checks reliability, and looks for "
                    "contradictions."
                ),
            ),
            "Research Writer": AgentProfile(
                name="Research Writer",
                department="Publication",
                role="Writer",
                description=(
                    "Produces the final structured research report."
                ),
            ),
        }

    def _select_agents_fallback(
        self,
        question: str,
    ) -> list[AgentProfile]:
        """
        Existing deterministic agent-selection logic.

        This runs whenever Fireworks is unavailable or invalid.
        """

        q = question.lower()
        catalog = self._agent_catalog()

        selected_names = [
            "Research Planner",
            "Evidence Synthesizer",
        ]

        if any(
            word in q
            for word in [
                "paper",
                "literature",
                "study",
                "research",
                "journal",
            ]
        ):
            selected_names.append("Literature Specialist")

        if any(
            word in q
            for word in [
                "benchmark",
                "gpu",
                "amd",
                "nvidia",
                "rocm",
                "cuda",
                "inference",
            ]
        ):
            selected_names.append("Benchmark Analyst")

        if any(
            word in q
            for word in [
                "gap",
                "unexplored",
                "opportunity",
                "future work",
                "novel",
            ]
        ):
            selected_names.append("Research Gap Detector")

        if any(
            word in q
            for word in [
                "contradiction",
                "bias",
                "reliable",
                "validate",
                "evidence",
            ]
        ):
            selected_names.append("Skeptic Reviewer")

        selected_names.append("Research Writer")

        return [
            catalog[name]
            for name in selected_names
        ]

    def _estimate_complexity_fallback(
        self,
        question: str,
    ) -> str:
        """
        Existing deterministic complexity estimation.
        """

        q = question.lower()
        word_count = len(question.split())

        if word_count > 18:
            return "high"

        if any(
            phrase in q
            for phrase in [
                "compare",
                "gap",
                "benchmark",
                "systematic",
                "literature review",
            ]
        ):
            return "medium"

        return "low"