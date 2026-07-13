import asyncio
import json

from app.models.analysis import PaperAnalysis
from app.services.literature_review import LiteratureReviewService


async def main() -> None:
    """
    Tests the Fireworks-powered cross-paper literature review.
    """

    analyses = [
        PaperAnalysis(
            paper_title="AMD MI300X Performance for LLM Inference",
            key_findings=[
                "Memory bandwidth is a major LLM inference bottleneck.",
                "MI300X provides high memory bandwidth for large models.",
            ],
            limitations=[
                "Only one AMD GPU generation was evaluated.",
                "The study does not test transformer-specific kernels.",
            ],
            research_gaps=[
                "Cross-generation AMD benchmarking remains limited.",
            ],
            confidence="high",
        ),
        PaperAnalysis(
            paper_title="ROCm Profiling for GPU Workloads",
            key_findings=[
                "Profiling tools help identify GPU memory bottlenecks.",
                "ROCm supports performance analysis on AMD GPUs.",
            ],
            limitations=[
                "Profiling support is less mature for transformer workloads.",
                "The evaluation predates MI300 hardware.",
            ],
            research_gaps=[
                "Modern ROCm profiling requires transformer-specific studies.",
            ],
            confidence="medium",
        ),
        PaperAnalysis(
            paper_title="Quantized Transformer Inference Across GPU Platforms",
            key_findings=[
                "Quantization can reduce inference memory requirements.",
                "Most quantization benchmarks target NVIDIA GPUs.",
            ],
            limitations=[
                "AMD-specific quantization results are not reported.",
            ],
            research_gaps=[
                "Quantization performance on AMD GPUs remains underexplored.",
            ],
            confidence="medium",
        ),
    ]

    service = LiteratureReviewService()

    review = await service.create_review(analyses)

    print(
        json.dumps(
            review.model_dump(),
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())