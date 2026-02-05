from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class PlannerAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.2
        )

        self.system_prompt = (
            "You are a task planning agent.\n"
            "Your job is to break a user goal into clear, ordered, actionable steps.\n"
            "Rules:\n"
            "- Do not execute tasks.\n"
            "- Only return a numbered step-by-step plan.\n"
            "- Keep steps simple and logical."
        )

    def create_plan(self, user_goal: str):

        prompt = f"""
SYSTEM:
{self.system_prompt}

USER GOAL:
{user_goal}

Return only the plan.
"""

        response = self.llm.invoke(prompt)
        return response.content
