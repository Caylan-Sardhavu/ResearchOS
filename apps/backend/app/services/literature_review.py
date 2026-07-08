from app.models.analysis import PaperAnalysis
from app.models.review import LiteratureReview


class LiteratureReviewService:
    """
    Synthesizes insights across multiple analyzed papers.

    This service compares paper-level analyses and produces a higher-level
    literature review. It helps ResearchOS reason across papers instead of
    treating each paper in isolation.
    """

    def create_review(
        self,
        analyses: list[PaperAnalysis],
    ) -> LiteratureReview:
        """
        Builds a simple literature review from multiple paper analyses.
        """

        common_findings = []
        common_limitations = []
        possible_research_gaps = []
        emerging_topics = []

        for analysis in analyses:
            self._add_unique_items(common_findings, analysis.key_findings)
            self._add_unique_items(common_limitations, analysis.limitations)
            self._add_unique_items(possible_research_gaps, analysis.research_gaps)

            # Basic topic detection for MVP.
            text = " ".join(analysis.key_findings).lower()

            if "gpu" in text:
                self._add_unique_items(emerging_topics, ["GPU computing"])

            if "amd" in text or "rocm" in text:
                self._add_unique_items(emerging_topics, ["AMD / ROCm ecosystem"])

            if "performance" in text or "benchmark" in text:
                self._add_unique_items(emerging_topics, ["Performance benchmarking"])

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
        Adds items to a list while avoiding duplicates.
        """

        for item in items:
            if item not in target:
                target.append(item)