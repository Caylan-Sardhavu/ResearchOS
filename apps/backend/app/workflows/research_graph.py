from app.agents.director import ResearchDirector
from app.services.evidence import EvidenceService
from app.services.gap_detector import GapDetectorService
from app.services.literature_review import LiteratureReviewService
from app.services.planner import PlannerService
from app.services.ranking import RankingService
from app.services.report_writer import ReportWriterService
from app.services.summarizer import PaperSummarizerService
from app.knowledge.notebook import ResearchNotebook


class ResearchWorkflow:
    """
    End-to-end ResearchOS pipeline.

    The Research Director acts as the orchestrator. It prepares the initial
    plan and team selection, while the workflow executes the research stages.
    """

    def __init__(self):
        self.director = ResearchDirector()
        self.planner = PlannerService()
        self.evidence = EvidenceService()
        self.ranking = RankingService()
        self.summarizer = PaperSummarizerService()
        self.literature_review = LiteratureReviewService()
        self.gap_detector = GapDetectorService()
        self.report_writer = ReportWriterService()
        self.notebook = ResearchNotebook()

    async def run(self, question: str) -> dict:
        """
        Executes the full research pipeline for one user question.
        """

        # 1. Ask the Director to inspect the question, check notebook memory,
        # and assemble the specialist research team.
        director_plan = await self.director.create_plan(question)

        # 2. Create the structured investigation plan.
        plan = await self.planner.create_plan(question)

        # 3. Retrieve evidence using the planner's search queries.
        papers = await self.evidence.collect_evidence(
            search_queries=plan.search_queries,
            max_results_per_query=3,
        )

        # 4. Rank papers by relevance.
        ranked_papers = self.ranking.rank(
            papers=papers,
            query=question,
        )

        # 5. Analyze the strongest papers.
        top_papers = ranked_papers[:5]

        analyses = [
            self.summarizer.analyze_paper(paper)
            for paper in top_papers
        ]

        # 6. Compare findings across papers.
        review = await self.literature_review.create_review(analyses)

        # 7. Detect possible research gaps.
        research_gaps = self.gap_detector.detect_gaps(analyses)

        # 8. Generate the final markdown report.
        report = await self.report_writer.create_report(
            question=question,
            plan=plan,
            review=review,
            ranked_papers=ranked_papers,
            research_gaps=research_gaps,
        )

        self.notebook.save_investigation(
            question=question,
            summary=report[:300],
            research_gaps=research_gaps,
            selected_agents=[
                agent.name for agent in director_plan.selected_agents
            ],
            paper_titles=[
                paper.title for paper in papers
            ],
            report=report,
        )

        return {
            "question": question,
            "director": {
                "complexity": director_plan.complexity,
                "notebook_matches": director_plan.notebook_matches,
                "selected_agents": director_plan.selected_agents,
                "notes": director_plan.director_notes,
                "ai_used": director_plan.ai_used,
            },
            "research_plan": plan,
            "papers_found": len(papers),
            "top_papers": top_papers,
            "paper_analyses": analyses,
            "literature_review": review,
            "research_gaps": research_gaps,
            "report": report,
        }