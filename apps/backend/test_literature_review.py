import asyncio

from app.services.evidence import EvidenceService
from app.services.ranking import RankingService
from app.services.summarizer import PaperSummarizerService
from app.services.literature_review import LiteratureReviewService


async def main():
    """
    Tests cross-paper literature review generation.
    """

    evidence = EvidenceService()
    ranking = RankingService()
    summarizer = PaperSummarizerService()
    reviewer = LiteratureReviewService()

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

    review = reviewer.create_review(analyses)

    print(review.model_dump_json(indent=2))


asyncio.run(main())