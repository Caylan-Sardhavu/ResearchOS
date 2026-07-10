from app.models.analysis import PaperAnalysis


class GapDetectorService:
    """
    Identifies research gaps from analyzed papers.

    MVP version:
    Uses rule-based aggregation over paper analyses.

    Future version:
    Fireworks AI will synthesize deeper cross-paper gaps.
    """

    def detect_gaps(
        self,
        analyses: list[PaperAnalysis],
    ) -> list[str]:
        """
        Combines research gaps and limitations across papers,
        then removes duplicates while preserving order.
        """

        gaps = []

        for analysis in analyses:
            for gap in analysis.research_gaps:
                gaps.append(gap)

            for limitation in analysis.limitations:
                gaps.append(f"Repeated limitation: {limitation}")

        if not gaps:
            gaps.append(
                "No strong research gaps were detected from the available abstracts."
            )

        # Remove duplicate gaps while keeping the original order.
        return list(dict.fromkeys(gaps))