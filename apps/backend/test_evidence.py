import asyncio
import json

from app.services.evidence import EvidenceService


async def main():
    """
    Quick manual test for the EvidenceService.

    This proves that ResearchOS can take multiple search queries,
    search arXiv, merge results, and remove duplicate papers.
    """

    evidence = EvidenceService()

    papers = await evidence.collect_evidence(
        search_queries=[
            "transformer inference AMD GPU",
            "LLM inference ROCm",
            "AMD GPU performance",
        ],
        max_results_per_query=2,
    )

    print(f"Collected {len(papers)} unique papers.")
    for paper in papers:
        print(paper.model_dump_json(indent=2))


asyncio.run(main())