import json
import re
from typing import Any

from app.models.analysis import PaperAnalysis
from app.models.review import LiteratureReview
from app.services.fireworks import FireworksService


class LiteratureReviewService:
    """
    Synthesizes insights across multiple analyzed papers.

    Fireworks compares evidence across the papers and identifies:
    - areas of consensus,
    - strong and weak evidence,
    - contradictions,
    - emerging trends,
    - cross-paper research gaps.

    The deterministic implementation remains available as a fallback.
    """

    def __init__(self) -> None:
        self.fireworks = FireworksService()

    async def create_review(
        self,
        analyses: list[PaperAnalysis],
    ) -> LiteratureReview:
        """
        Creates a cross-paper literature review.

        Fireworks is used when configured. If the API is unavailable,
        returns malformed output, or fails validation, ResearchOS uses
        the original deterministic review logic.
        """

        fallback_review = self._create_fallback_review(analyses)

        if not analyses:
            return fallback_review

        if not self.fireworks.available():
            return fallback_review

        ai_review = await self._create_ai_review(analyses)

        if ai_review is None:
            return fallback_review

        return ai_review

    async def _create_ai_review(
        self,
        analyses: list[PaperAnalysis],
    ) -> LiteratureReview | None:
        """
        Sends normalized paper analyses to Fireworks for synthesis.
        """

        evidence_payload = []

        for index, analysis in enumerate(analyses[:6], start=1):
            evidence_payload.append(
                {
                    "paper_number": index,
                    "key_findings": analysis.key_findings[:8],
                    "limitations": analysis.limitations[:6],
                    "research_gaps": analysis.research_gaps[:6],
                }
            )

        prompt = f"""
Compare the following analyzed research papers and produce a rigorous
cross-paper literature synthesis.

Paper analyses:
{json.dumps(evidence_payload, indent=2)}

Return only valid JSON with exactly this structure:

{{
  "consensus": [
    "finding supported across multiple papers"
  ],
  "strong_evidence": [
    "finding with the strongest support"
  ],
  "contradictions": [
    "meaningful disagreement or methodological inconsistency"
  ],
  "weak_evidence": [
    "claim or topic with insufficient evidence"
  ],
  "emerging_trends": [
    "important recurring or developing topic"
  ],
  "research_gaps": [
    "specific gap inferred across the papers"
  ],
  "confidence": "low, medium, or high"
}}

Requirements:
- Base every statement only on the supplied analyses.
- Do not invent benchmark results, paper names, or citations.
- Separate consensus from contradiction.
- Treat missing evidence as weak evidence, not as a confirmed fact.
- Return between 2 and 5 items per populated category.
- Keep every item concise and specific.
- Return no Markdown and no text outside the JSON object.
""".strip()

        result = await self.fireworks.chat(
            prompt=prompt,
            system_prompt=(
                "You are an evidence-synthesis specialist conducting a "
                "cross-paper literature review. Compare claims carefully, "
                "identify consensus and disagreement, and return strict JSON."
            ),
            max_tokens=900,
            temperature=0.1,
        )

        if not result.get("success"):
            print(
                "Fireworks Literature Review fallback:",
                result.get("message", "Unknown Fireworks error"),
            )
            return None

        response_text = result.get("response")

        if not isinstance(response_text, str):
            return None

        parsed = self._parse_json_object(response_text)

        if parsed is None:
            print(
                "Fireworks Literature Review fallback: "
                "invalid JSON response."
            )
            return None

        return self._validate_ai_review(parsed)

    def _validate_ai_review(
        self,
        data: dict[str, Any],
    ) -> LiteratureReview | None:
        """
        Validates and maps the richer AI response into the existing
        LiteratureReview model.
        """

        consensus = self._clean_string_list(
            data.get("consensus"),
            limit=5,
        )
        strong_evidence = self._clean_string_list(
            data.get("strong_evidence"),
            limit=5,
        )
        contradictions = self._clean_string_list(
            data.get("contradictions"),
            limit=5,
        )
        weak_evidence = self._clean_string_list(
            data.get("weak_evidence"),
            limit=5,
        )
        emerging_trends = self._clean_string_list(
            data.get("emerging_trends"),
            limit=5,
        )
        research_gaps = self._clean_string_list(
            data.get("research_gaps"),
            limit=6,
        )

        confidence = str(
            data.get("confidence", "medium")
        ).lower().strip()

        if confidence not in {"low", "medium", "high"}:
            confidence = "medium"

        common_findings = self._combine_labeled_items(
            [
                ("Consensus", consensus),
                ("Strong evidence", strong_evidence),
            ],
            limit=8,
        )

        common_limitations = self._combine_labeled_items(
            [
                ("Contradiction", contradictions),
                ("Weak evidence", weak_evidence),
            ],
            limit=8,
        )

        if (
            not common_findings
            and not common_limitations
            and not emerging_trends
            and not research_gaps
        ):
            return None

        return LiteratureReview(
            common_findings=common_findings,
            common_limitations=common_limitations,
            emerging_topics=emerging_trends,
            possible_research_gaps=research_gaps,
            confidence=confidence,
        )

    def _clean_string_list(
        self,
        value: Any,
        *,
        limit: int,
    ) -> list[str]:
        """
        Converts an unknown model value into a clean unique string list.
        """

        if not isinstance(value, list):
            return []

        cleaned_items: list[str] = []

        for item in value:
            if not isinstance(item, str):
                continue

            cleaned = " ".join(item.split()).strip()

            if len(cleaned) < 10:
                continue

            if cleaned not in cleaned_items:
                cleaned_items.append(cleaned)

        return cleaned_items[:limit]

    def _combine_labeled_items(
        self,
        groups: list[tuple[str, list[str]]],
        *,
        limit: int,
    ) -> list[str]:
        """
        Adds useful labels while preserving the existing model structure.
        """

        combined: list[str] = []

        for label, items in groups:
            for item in items:
                formatted = f"{label}: {item}"

                if formatted not in combined:
                    combined.append(formatted)

        return combined[:limit]

    def _parse_json_object(
        self,
        response_text: str,
    ) -> dict[str, Any] | None:
        """
        Parses a JSON object and tolerates accidental Markdown fences.
        """

        cleaned = response_text.strip()

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

    def _create_fallback_review(
        self,
        analyses: list[PaperAnalysis],
    ) -> LiteratureReview:
        """
        Original deterministic review implementation.
        """

        common_findings: list[str] = []
        common_limitations: list[str] = []
        possible_research_gaps: list[str] = []
        emerging_topics: list[str] = []

        for analysis in analyses:
            self._add_unique_items(
                common_findings,
                analysis.key_findings,
            )
            self._add_unique_items(
                common_limitations,
                analysis.limitations,
            )
            self._add_unique_items(
                possible_research_gaps,
                analysis.research_gaps,
            )

            text = " ".join(
                analysis.key_findings
            ).lower()

            if "gpu" in text:
                self._add_unique_items(
                    emerging_topics,
                    ["GPU computing"],
                )

            if "amd" in text or "rocm" in text:
                self._add_unique_items(
                    emerging_topics,
                    ["AMD / ROCm ecosystem"],
                )

            if "performance" in text or "benchmark" in text:
                self._add_unique_items(
                    emerging_topics,
                    ["Performance benchmarking"],
                )

        return LiteratureReview(
            common_findings=common_findings,
            common_limitations=common_limitations,
            emerging_topics=emerging_topics,
            possible_research_gaps=possible_research_gaps,
            confidence="medium",
        )

    def _add_unique_items(
        self,
        target: list[str],
        items: list[str],
    ) -> None:
        """
        Adds non-empty unique items to a list.
        """

        for item in items:
            cleaned = item.strip()

            if cleaned and cleaned not in target:
                target.append(cleaned)