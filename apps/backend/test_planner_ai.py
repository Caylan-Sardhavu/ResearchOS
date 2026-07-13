import asyncio

from app.services.planner import PlannerService


async def main() -> None:
    """
    Tests Fireworks-powered research planning.
    """

    planner = PlannerService()

    plan = await planner.create_plan(
        "Identify recent research gaps in transformer inference "
        "optimization for AMD GPUs using benchmarks and academic papers."
    )

    print(plan.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())