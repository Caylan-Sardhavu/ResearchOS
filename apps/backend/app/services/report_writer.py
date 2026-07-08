from app.models.paper import Paper
from app.models.research import ResearchPlan
from app.models.review import LiteratureReview


class ReportWriterService:
    """
    Creates the final markdown research report from the full ResearchOS pipeline.
    """

    def create_report(
        self,
        question: str,
        plan: ResearchPlan,
        review: LiteratureReview,
        ranked_papers: list[Paper],
        research_gaps: list[str],
    ) -> str:
        """
        Combines planning, evidence, literature review, and gap detection
        into one readable research report.
        """

        lines = []

        lines.append("# Research Report\n")

        lines.append("## Research Question\n")
        lines.append(question + "\n")

        lines.append("## Investigation Plan\n")
        for subquestion in plan.subquestions:
            lines.append(f"- {subquestion}")

        lines.append("\n## Literature Review\n")

        lines.append("### Common Findings")
        for finding in review.common_findings:
            lines.append(f"- {finding}")

        lines.append("\n### Common Limitations")
        for limitation in review.common_limitations:
            lines.append(f"- {limitation}")

        lines.append("\n### Emerging Topics")
        for topic in review.emerging_topics:
            lines.append(f"- {topic}")

        lines.append("\n## Top Papers")
        for paper in ranked_papers[:5]:
            year = paper.published[:4] if paper.published else "Unknown year"
            lines.append(f"- **{paper.title}** ({year}) — {paper.url}")

        lines.append("\n## Research Gaps")
        for gap in research_gaps:
            lines.append(f"- {gap}")

        return "\n".join(lines)