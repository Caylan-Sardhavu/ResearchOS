from pydantic import BaseModel


class Paper(BaseModel):
    """
    Standard internal representation of a research paper.

    Every research source should return papers in this format.
    This allows the rest of ResearchOS to work with a single,
    consistent object regardless of where the paper came from.
    """

    title: str
    authors: list[str]
    summary: str
    published: str | None = None
    url: str
    pdf_url: str | None = None
    source: str

    # Calculated later by the ranking engine.
    relevance_score: float = 0.0