from llm.llm_client import LLMClient


class PlannerAgent:

    def __init__(self):
        self.llm = LLMClient()

    # -----------------------------
    # SEARCH PLANNER
    # -----------------------------
    def create_plan(self, user_query: str):

        prompt = f"""
You are a research planner.

Break the user request into 1–3 specific search queries.

IMPORTANT:
If the question asks for latest or current information,
include words like:
latest, today, current, headlines, update

User request:
{user_query}
"""



        response = self.llm.generate_response(prompt)

        queries = []
        for line in response.split("\n"):
            if line.strip():
                cleaned = line.split(".", 1)[-1].strip()
                queries.append(cleaned)

        return queries[:3]


    # -----------------------------
    # TASK PLANNER (MULTI-STEP)
    # -----------------------------
    def create_task_plan(self, user_query: str):

        prompt = f"""
You are an intelligent task planner.

Break the user's request into logical steps needed to solve it.

If the question is simple, return only one step.
If complex, return multiple steps.

Return ONLY numbered steps.

User request:
{user_query}
"""

        response = self.llm.generate_response(prompt)

        steps = []
        for line in response.split("\n"):
            if line.strip():
                cleaned = line.split(".", 1)[-1].strip()
                steps.append(cleaned)

        return steps
