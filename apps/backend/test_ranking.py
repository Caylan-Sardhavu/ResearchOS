import asyncio

from app.services.evidence import EvidenceService
from app.services.ranking import RankingService


async def main():
    evidence = EvidenceService()

    papers = await evidence.collect_evidence(
        search_queries=[
            "transformer inference AMD GPU",
            "LLM inference ROCm",
        ]
    )

    ranking = RankingService()

    ranked = ranking.rank(
        papers,
        "transformer inference AMD GPU",
    )

    print()
    print("========== Ranked Papers ==========")

    for paper in ranked:
        print()
        print(f"Score : {paper.relevance_score:.1f}")
        print(f"Title : {paper.title}")
        print(f"Year  : {paper.published}")


asyncio.run(main())