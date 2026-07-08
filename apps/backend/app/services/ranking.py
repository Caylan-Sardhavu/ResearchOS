from datetime import datetime

from app.models.paper import Paper


class RankingService:
    """
    Scores research papers according to how relevant they are
    to the user's research query.

    This allows ResearchOS to prioritize the strongest evidence
    before passing it to downstream AI agents.
    """

    def rank(
        self,
        papers: list[Paper],
        query: str,
    ) -> list[Paper]:
        """
        Calculates a relevance score for every paper and returns
        the papers sorted from most relevant to least relevant.
        """

        keywords = query.lower().split()

        for paper in papers:
            score = self._calculate_score(
                paper,
                keywords,
            )

            paper.relevance_score = score

        return sorted(
            papers,
            key=lambda p: p.relevance_score,
            reverse=True,
        )

    def _calculate_score(
        self,
        paper: Paper,
        keywords: list[str],
    ) -> float:
        """
        Very simple scoring algorithm.

        Later we can replace this with embeddings or
        semantic similarity.
        """

        score = 0.0

        title = paper.title.lower()
        summary = paper.summary.lower()

        # -------------------------
        # Title matches
        # -------------------------
        for word in keywords:
            if word in title:
                score += 8

        # -------------------------
        # Abstract matches
        # -------------------------
        for word in keywords:
            if word in summary:
                score += 2

        # -------------------------
        # Publication recency
        # -------------------------
        if paper.published:

            try:
                year = datetime.fromisoformat(
                    paper.published.replace("Z", "")
                ).year

                current_year = datetime.now().year

                score += max(
                    0,
                    10 - (current_year - year),
                )

            except Exception:
                pass

        return score