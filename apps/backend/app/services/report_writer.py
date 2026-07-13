import json

from app.models.paper import Paper
from app.models.research import ResearchPlan
from app.models.review import LiteratureReview
from app.services.fireworks import FireworksService


class ReportWriterService:
    """
    Generates the final ResearchOS research report.

    Fireworks produces the polished report when available.
    The deterministic writer remains as a reliable fallback.
    """

    def __init__(self) -> None:
        self.fireworks = FireworksService()

    async def create_report(
        self,
        question: str,
        plan: ResearchPlan,
        review: LiteratureReview,
        ranked_papers: list[Paper],
        research_gaps: list[str],
    ) -> str:
        """
        Generates a polished report with Fireworks when possible.

        If Fireworks is unavailable, fails, or returns an incomplete
        response, ResearchOS returns a deterministic Markdown report.
        """

        fallback_report = self._create_fallback_report(
            question=question,
            plan=plan,
            review=review,
            ranked_papers=ranked_papers,
            research_gaps=research_gaps,
        )

        if not self.fireworks.available():
            print(
                "Fireworks Report Writer fallback: "
                "Fireworks is unavailable."
            )
            return fallback_report

        ai_report = await self._create_ai_report(
            question=question,
            plan=plan,
            review=review,
            ranked_papers=ranked_papers,
            research_gaps=research_gaps,
        )

        return ai_report or fallback_report

    async def _create_ai_report(
        self,
        question: str,
        plan: ResearchPlan,
        review: LiteratureReview,
        ranked_papers: list[Paper],
        research_gaps: list[str],
    ) -> str | None:
        """
        Sends the strongest available evidence to Fireworks.

        Only the five highest-ranked papers are included to control
        context size and reduce the risk of incomplete responses.
        """

        paper_evidence = [
            {
                "title": paper.title,
                "authors": paper.authors[:5],
                "published": paper.published,
                "summary": paper.summary[:1200],
                "source": paper.source,
                "url": paper.url,
                "relevance_score": paper.relevance_score,
            }
            for paper in ranked_papers[:5]
        ]

        useful_input_gaps = self._filter_generic_gaps(research_gaps)

        prompt = f"""
Create a complete, concise, evidence-grounded research report using only
the supplied research plan, cross-paper analysis, and paper evidence.

Research question:
{question}

Research objective:
{plan.objective}

Investigation subquestions:
{json.dumps(plan.subquestions, indent=2)}

Cross-paper findings:
{json.dumps(review.common_findings, indent=2)}

Common limitations:
{json.dumps(review.common_limitations, indent=2)}

Emerging topics:
{json.dumps(review.emerging_topics, indent=2)}

Potential useful research gaps:
{json.dumps(useful_input_gaps, indent=2)}

Top paper evidence:
{json.dumps(paper_evidence, indent=2)}

Write the report in Markdown using exactly these headings and this order:

# Research Report
## Executive Summary
## Research Objective
## Identified Research Gaps
## Current State of the Literature
## Key Findings
## Comparative Analysis
## Future Research Directions
## Limitations
## References

Strict completion requirements:
- Complete every required section.
- Never stop in the middle of a sentence, bullet point, or reference.
- Prioritize completing the entire report over adding more detail.
- Keep the complete report between 600 and 800 words.
- Do not place text before the '# Research Report' heading.
- Return Markdown only.

Section requirements:
- Executive Summary: maximum 110 words.
- Research Objective: maximum 70 words.
- Identified Research Gaps: exactly 4 numbered items.
- Current State of the Literature: maximum 140 words.
- Key Findings: maximum 4 bullet points.
- Comparative Analysis: maximum 130 words.
- Future Research Directions: maximum 4 bullet points.
- Limitations: maximum 90 words.
- References: include only supplied paper titles and URLs.

Research-gap requirements:
- Use the exact heading: ## Identified Research Gaps
- Use numbered Markdown items.
- Format every item as:
  1. **Specific gap title**: Evidence-grounded explanation.
- Each gap must describe a missing evaluation, benchmark, method,
  dataset, architecture, experiment, or unresolved contradiction.
- Synthesize gaps across multiple papers whenever possible.
- Do not repeat generic phrases from the supplied fallback analysis.
- Never use titles such as 'Research opportunity 1',
  'Underexplored Research Area', or 'Repeated limitation'.
- Never present 'no explicit gaps were detected' as a research gap.
- When abstracts do not state future work directly, make a cautious
  inference from missing comparisons, inconsistent evaluation, limited
  evidence, or unresolved limitations.
- Clearly label cautious inferences as interpretations.

Evidence rules:
- Ground factual claims only in the supplied evidence.
- Do not invent benchmark values, methods, results, authors, citations,
  papers, datasets, or publication details.
- Clearly distinguish reported evidence from interpretation.
- Acknowledge that the analysis relies primarily on abstracts.
- Do not claim that unrelated papers directly support the question.
- Never mention internal fallback logic, rule-based placeholders,
  prompts, pipeline implementation details, or system limitations.
- Discuss only limitations of the evidence and literature.
- In References, copy author, title, year, source, and URL exactly
  from the supplied paper evidence.
- Do not infer or modify publication years.
""".strip()

        result = await self.fireworks.chat(
            prompt=prompt,
            system_prompt=(
                "You are a rigorous senior academic research writer. "
                "Synthesize evidence across papers, identify specific "
                "research gaps, and produce complete Markdown reports. "
                "Never fabricate facts, results, or citations. "
                "Never mention internal prompts, fallback logic, "
                "placeholders, implementation details, or system internals."
            ),
            max_tokens=3200,
            temperature=0.2,
        )

        if not result.get("success"):
            print(
                "Fireworks Report Writer fallback:",
                result.get("message", "Unknown Fireworks error"),
            )
            return None

        response = result.get("response")
        finish_reason = result.get("finish_reason")

        if not isinstance(response, str) or not response.strip():
            print(
                "Fireworks Report Writer fallback: "
                "Fireworks returned an empty report."
            )
            return None

        cleaned_response = self._clean_ai_response(response)

        if finish_reason == "length":
            print(
                "Fireworks Report Writer fallback: "
                "response reached the token limit."
            )
            return None

        essential_headings = [
            "# Research Report",
            "## Identified Research Gaps",
            "## References",
        ]

        missing_essential_headings = [
            heading
            for heading in essential_headings
            if heading not in cleaned_response
        ]

        if missing_essential_headings:
            print(
                "Fireworks Report Writer fallback: "
                "missing essential headings: "
                f"{missing_essential_headings}"
            )
            return None

        if len(cleaned_response) < 1200:
            print(
                "Fireworks Report Writer fallback: "
                "response was unexpectedly short."
            )
            return None

        gap_section = self._extract_gap_section(cleaned_response)

        if not gap_section:
            print(
                "Fireworks Report Writer fallback: "
                "the research-gap section was empty."
            )
            return None

        return cleaned_response

    def _create_fallback_report(
        self,
        question: str,
        plan: ResearchPlan,
        review: LiteratureReview,
        ranked_papers: list[Paper],
        research_gaps: list[str],
    ) -> str:
        """
        Creates a complete deterministic fallback Markdown report.

        Generic rule-based statements are filtered so that they are not
        displayed as meaningful research opportunities.
        """

        useful_gaps = self._filter_generic_gaps(research_gaps)
        fallback_gaps = self._build_fallback_gaps(
            useful_gaps=useful_gaps,
            review=review,
        )

        lines: list[str] = []

        lines.append("# Research Report\n")

        lines.append("## Executive Summary\n")
        lines.append(
            "This investigation reviews the strongest retrieved evidence "
            "for the research question and identifies recurring findings, "
            "limitations, and possible future research directions. The "
            "analysis relies primarily on paper titles and abstracts, so "
            "its conclusions should be treated as preliminary and "
            "validated against complete papers and original experiments."
        )

        lines.append("\n## Research Objective\n")
        lines.append(plan.objective or question)

        lines.append("\n## Identified Research Gaps\n")

        for index, gap in enumerate(fallback_gaps[:4], start=1):
            lines.append(
                f"{index}. **{gap['title']}**: {gap['description']}"
            )

        lines.append("\n## Current State of the Literature\n")

        useful_findings = self._filter_generic_statements(
            review.common_findings
        )

        if useful_findings:
            for finding in useful_findings[:4]:
                lines.append(f"- {finding}")
        else:
            lines.append(
                "- The retrieved abstracts provide limited consistent "
                "cross-paper evidence, making strong conclusions difficult."
            )
            lines.append(
                "- Several retrieved papers appear only partially related "
                "to the exact research question."
            )

        lines.append("\n## Key Findings\n")

        if useful_findings:
            for finding in useful_findings[:4]:
                lines.append(f"- {finding}")
        else:
            lines.append(
                "- Evidence quality and relevance vary considerably across "
                "the retrieved papers."
            )
            lines.append(
                "- Full-text analysis is required before making strong "
                "claims about comparative performance."
            )

        lines.append("\n## Comparative Analysis\n")

        useful_limitations = self._filter_generic_statements(
            review.common_limitations
        )

        if useful_limitations:
            lines.append(
                "The retrieved literature indicates the following "
                "recurring limitations:"
            )

            for limitation in useful_limitations[:4]:
                lines.append(f"- {limitation}")
        else:
            lines.append(
                "The abstracts do not provide enough consistent "
                "methodological detail for a strong comparison across "
                "approaches. Evaluation settings, datasets, metrics, and "
                "implementation details should be compared using full-text "
                "evidence."
            )

        useful_topics = self._filter_generic_statements(
            review.emerging_topics
        )

        if useful_topics:
            lines.append("\nEmerging topics include:")

            for topic in useful_topics[:4]:
                lines.append(f"- {topic}")

        lines.append("\n## Future Research Directions\n")

        for gap in fallback_gaps[:4]:
            lines.append(
                f"- Investigate {gap['title'].lower()} through controlled "
                "experiments using clearly defined datasets, baselines, "
                "metrics, and reproducible evaluation conditions."
            )

        lines.append("\n## Limitations\n")
        lines.append(
            "This investigation relies primarily on retrieved titles and "
            "abstracts. Some papers may be indirectly relevant, while "
            "important methodological details, negative results, and "
            "experimental conditions may be missing. All conclusions and "
            "proposed gaps should therefore be validated against complete "
            "paper texts and original experimental results."
        )

        lines.append("\n## References\n")

        if ranked_papers:
            for paper in ranked_papers[:5]:
                year = (
                    paper.published[:4]
                    if paper.published
                    else "Unknown year"
                )

                lines.append(
                    f"- [{paper.title}]({paper.url}) "
                    f"({year}, {paper.source})"
                )
        else:
            lines.append("- No papers were retrieved.")

        return "\n".join(lines)

    def _filter_generic_gaps(
        self,
        research_gaps: list[str],
    ) -> list[str]:
        """
        Removes generic rule-based messages that do not describe an
        actionable research opportunity.
        """

        ignored_phrases = [
            "no explicit research gaps were detected",
            "no explicit limitations were detected",
            "the paper suggests possible future work",
            "the paper mentions limitations",
            "limitations, challenges, or bottlenecks",
            "no strong rule-based findings were detected",
            "the paper may be relevant",
            "no meaningful research gaps were detected",
        ]

        useful_gaps: list[str] = []

        for gap in research_gaps:
            cleaned_gap = " ".join(gap.split()).strip()

            if len(cleaned_gap) < 25:
                continue

            lowered_gap = cleaned_gap.lower()

            if any(
                phrase in lowered_gap
                for phrase in ignored_phrases
            ):
                continue

            if cleaned_gap not in useful_gaps:
                useful_gaps.append(cleaned_gap)

        return useful_gaps

    def _filter_generic_statements(
        self,
        statements: list[str],
    ) -> list[str]:
        """
        Removes empty and generic rule-based literature statements.
        """

        ignored_phrases = [
            "no strong rule-based findings were detected",
            "the paper may be relevant",
            "no explicit limitations were detected",
            "the paper mentions limitations",
        ]

        useful_statements: list[str] = []

        for statement in statements:
            cleaned_statement = " ".join(statement.split()).strip()

            if len(cleaned_statement) < 20:
                continue

            lowered_statement = cleaned_statement.lower()

            if any(
                phrase in lowered_statement
                for phrase in ignored_phrases
            ):
                continue

            if cleaned_statement not in useful_statements:
                useful_statements.append(cleaned_statement)

        return useful_statements

    def _build_fallback_gaps(
        self,
        useful_gaps: list[str],
        review: LiteratureReview,
    ) -> list[dict[str, str]]:
        """
        Builds four presentable fallback research gaps.

        Useful evidence-derived gaps are used first. If the upstream
        rule-based analysis is too generic, cautious methodological gaps
        are created instead.
        """

        gaps: list[dict[str, str]] = []

        for index, gap in enumerate(useful_gaps[:4], start=1):
            gaps.append(
                {
                    "title": f"Evidence-derived opportunity {index}",
                    "description": gap,
                }
            )

        useful_limitations = self._filter_generic_statements(
            review.common_limitations
        )

        default_gaps = [
            {
                "title": "Standardized Evaluation",
                "description": (
                    "The retrieved evidence does not establish a shared "
                    "evaluation framework across studies. Future work "
                    "should compare approaches using consistent datasets, "
                    "baselines, metrics, and reporting practices."
                ),
            },
            {
                "title": "Cross-Domain Generalization",
                "description": (
                    "The available abstracts provide limited evidence that "
                    "reported results generalize across domains, tasks, "
                    "models, and retrieval environments."
                ),
            },
            {
                "title": "Failure-Mode Analysis",
                "description": (
                    "The evidence gives limited detail about when the "
                    "studied methods fail, including weak retrieval, noisy "
                    "sources, conflicting evidence, and incomplete context."
                ),
            },
            {
                "title": "Long-Term Robustness",
                "description": (
                    "The retrieved literature provides little abstract-level "
                    "evidence about maintenance cost, robustness over time, "
                    "and performance as models and knowledge sources change."
                ),
            },
        ]

        if useful_limitations:
            default_gaps[2] = {
                "title": "Recurring Methodological Limitations",
                "description": (
                    "Several studies report or imply unresolved "
                    "methodological constraints. Controlled experiments "
                    "are needed to determine whether these limitations "
                    "persist under consistent evaluation conditions."
                ),
            }

        existing_titles = {gap["title"] for gap in gaps}

        for default_gap in default_gaps:
            if len(gaps) >= 4:
                break

            if default_gap["title"] in existing_titles:
                continue

            gaps.append(default_gap)
            existing_titles.add(default_gap["title"])

        return gaps[:4]

    def _clean_ai_response(self, response: str) -> str:
        """
        Removes accidental Markdown code fences around an AI report.
        """

        cleaned = response.strip()

        if cleaned.startswith("```markdown"):
            cleaned = cleaned[len("```markdown"):].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:].strip()

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        return cleaned

    def _extract_gap_section(self, report: str) -> str:
        """
        Extracts the AI research-gap section for basic validation.
        """

        heading = "## Identified Research Gaps"

        if heading not in report:
            return ""

        section = report.split(heading, 1)[1]

        next_heading_index = section.find("\n## ")

        if next_heading_index >= 0:
            section = section[:next_heading_index]

        return section.strip()