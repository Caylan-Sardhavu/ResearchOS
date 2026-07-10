from app.models.paper import Paper
from app.services.arxiv import ArxivService


class EvidenceService:
    """
    Coordinates research evidence retrieval from external sources.
    """

    def __init__(self):
        self.arxiv = ArxivService()

    async def collect_evidence(
        self,
        search_queries: list[str],
        max_results_per_query: int = 3,
    ) -> list[Paper]:
        """
        Runs multiple search queries and safely skips failed searches.
        """

        all_papers = []

        for query in search_queries:
            try:
                papers = await self.arxiv.search(
                    query=query,
                    max_results=max_results_per_query,
                )
                all_papers.extend(papers)

            except Exception as error:
                print(f"Evidence retrieval failed for query '{query}': {error}")

        return self._deduplicate_papers(all_papers)

    def _deduplicate_papers(self, papers: list[Paper]) -> list[Paper]:
        """
        Removes duplicate papers based on URL.
        """

        seen_urls = set()
        unique_papers = []

        for paper in papers:
            if paper.url in seen_urls:
                continue

            seen_urls.add(paper.url)
            unique_papers.append(paper)

        return unique_papers