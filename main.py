from agents.planner_agent import PlannerAgent
from agents.research_agent import ResearchAgent
from agents.writer_agent import WriterAgent
from agents.validator_agent import ValidatorAgent

# Initialize agents
planner = PlannerAgent()
researcher = ResearchAgent()
writer = WriterAgent()
validator = ValidatorAgent()

# User goal
goal = "Write a beginner friendly blog about Agentic AI"

# Step 1: Planning
plan = planner.create_plan(goal)
print("\n--- PLAN ---\n")
print(plan)

# Step 2: Research
research_task = "What is Agentic AI and its core concepts"
research_data = researcher.research(research_task)
print("\n--- RESEARCH DATA ---\n")
print(research_data)

# Step 3: Writing
draft_content = writer.write_content(plan, research_data)
print("\n--- DRAFT CONTENT ---\n")
print(draft_content)

# Step 4: Validation
final_content = validator.validate_content(draft_content)
print("\n--- FINAL VALIDATED OUTPUT ---\n")
print(final_content)
