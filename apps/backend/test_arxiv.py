import asyncio
import json

from app.services.arxiv import ArxivService


async def main():
    arxiv = ArxivService()

    papers = await arxiv.search(
        "transformer inference AMD GPU",
        max_results=3,
    )

    print(json.dumps(papers, indent=2))


asyncio.run(main())