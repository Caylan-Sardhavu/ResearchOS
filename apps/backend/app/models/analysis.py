from pydantic import BaseModel


class PaperAnalysis(BaseModel):
    """
    Structured analysis extracted from a research paper.

    For now, this is produced using simple rule-based logic.
    Later, Fireworks AI will generate much richer analysis.
    """

    paper_title: str
    key_findings: list[str]
    limitations: list[str]
    research_gaps: list[str]
    confidence: str