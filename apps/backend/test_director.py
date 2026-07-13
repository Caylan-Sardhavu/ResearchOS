import asyncio
import json

from app.agents.director import ResearchDirector


async def main() -> None:
    """
    Tests Fireworks-powered Director planning.
    """

    director = ResearchDirector()

    result = await director.create_plan(
        "Identify recent research gaps in transformer inference "
        "optimization for AMD GPUs using benchmarks and academic papers."
    )

    print(
        json.dumps(
            result.model_dump(),
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())