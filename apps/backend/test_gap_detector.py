import asyncio

from app.services.evidence import EvidenceService
from app.services.ranking import RankingService
from app.services.summarizer import PaperSummarizerService
from app.services.gap_detector import GapDetectorService


async def main():
    """
    Tests the research gap detector using real arXiv papers.
    """

    evidence = EvidenceService()
    ranking = RankingService()
    summarizer = PaperSummarizerService()
    gap_detector = GapDetectorService()

    papers = await evidence.collect_evidence(
        search_queries=[
            "transformer inference AMD GPU",
            "LLM inference ROCm",
        ]
    )

    ranked_papers = ranking.rank(
        papers,
        "transformer inference AMD GPU",
    )

    top_papers = ranked_papers[:3]

    analyses = [
        summarizer.analyze_paper(paper)
        for paper in top_papers
    ]

    gaps = gap_detector.detect_gaps(analyses)

    print("========== Research Gaps ==========")

    for gap in gaps:
        print(f"- {gap}")


asyncio.run(main())