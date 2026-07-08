from app.services.arxiv import ArxivService
from app.models.paper import Paper


class EvidenceService:
    """
    Coordinates research evidence retrieval.

    This service sits between the Planner and individual data sources.
    For now, it only uses arXiv. Later, we can add Semantic Scholar,
    OpenAlex, AMD docs, GitHub, PubMed, and more without changing the Director.
    """

    def __init__(self):
        self.arxiv = ArxivService()

    async def collect_evidence(
            self,
            search_queries: list[str],
            max_results_per_query: int = 3,
    ) -> list[Paper]:
        """
        Runs multiple search queries against research sources
        and returns a deduplicated list of papers.
        """

        all_papers = []

        for query in search_queries:
            papers = await self.arxiv.search(
                query=query,
                max_results=max_results_per_query,
            )

            all_papers.extend(papers)

        return self._deduplicate_papers(all_papers)

    def _deduplicate_papers(self, papers: list[Paper],) -> list[Paper]:
        """
        Removes duplicate papers based on their URL.

        Since multiple search queries can return the same paper,
        we keep only the first occurrence.
        """

        seen_urls = set()
        unique_papers = []

        for paper in papers:

            if paper.url in seen_urls:
                continue

            seen_urls.add(paper.url)
            unique_papers.append(paper)

        return unique_papers
    