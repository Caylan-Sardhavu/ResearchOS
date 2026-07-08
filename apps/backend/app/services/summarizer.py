from app.models.analysis import PaperAnalysis
from app.models.paper import Paper


class PaperSummarizerService:
    """
    Extracts structured insights from research papers.

    MVP version:
    Uses simple rule-based analysis from the paper title and abstract.

    Future version:
    Uses Fireworks AI to extract richer findings, limitations,
    benchmarks, methods, and research gaps.
    """

    def analyze_paper(self, paper: Paper) -> PaperAnalysis:
        """
        Creates a basic structured analysis for one paper.
        """

        text = f"{paper.title} {paper.summary}".lower()

        key_findings = []
        limitations = []
        research_gaps = []

        if "performance" in text or "benchmark" in text:
            key_findings.append(
                "The paper discusses performance or benchmarking results."
            )

        if "gpu" in text:
            key_findings.append(
                "The paper is relevant to GPU-based computing."
            )

        if "amd" in text or "rocm" in text:
            key_findings.append(
                "The paper contains AMD or ROCm-related content."
            )

        if "limitation" in text or "challenge" in text or "bottleneck" in text:
            limitations.append(
                "The paper mentions limitations, challenges, or bottlenecks."
            )

        if "future work" in text or "gap" in text or "open" in text:
            research_gaps.append(
                "The paper suggests possible future work or open research questions."
            )

        if not key_findings:
            key_findings.append(
                "The paper may be relevant, but no strong rule-based findings were detected."
            )

        if not limitations:
            limitations.append(
                "No explicit limitations were detected from the abstract."
            )

        if not research_gaps:
            research_gaps.append(
                "No explicit research gaps were detected from the abstract."
            )

        return PaperAnalysis(
            paper_title=paper.title,
            key_findings=key_findings,
            limitations=limitations,
            research_gaps=research_gaps,
            confidence="medium",
        )