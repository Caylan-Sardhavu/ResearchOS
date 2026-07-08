from app.services.planner import PlannerService


planner = PlannerService()

plan = planner.create_plan(
    "Find research gaps in transformer inference optimization for AMD GPUs."
)

print(plan.model_dump_json(indent=2))