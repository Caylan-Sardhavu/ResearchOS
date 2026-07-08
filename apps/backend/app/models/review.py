from pydantic import BaseModel


class LiteratureReview(BaseModel):
    """
    Cross-paper synthesis produced from multiple paper analyses.

    This represents what ResearchOS learns by comparing papers,
    not just summarizing them individually.
    """

    common_findings: list[str]
    common_limitations: list[str]
    emerging_topics: list[str]
    possible_research_gaps: list[str]
    confidence: str