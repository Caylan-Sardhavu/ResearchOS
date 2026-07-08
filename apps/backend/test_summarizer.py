import asyncio

from app.services.evidence import EvidenceService
from app.services.ranking import RankingService
from app.services.summarizer import PaperSummarizerService


async def main():
    """
    Tests the paper summarizer using real arXiv papers.
    """

    evidence = EvidenceService()
    ranking = RankingService()
    summarizer = PaperSummarizerService()

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

    top_paper = ranked_papers[0]

    analysis = summarizer.analyze_paper(top_paper)

    print(analysis.model_dump_json(indent=2))


asyncio.run(main())