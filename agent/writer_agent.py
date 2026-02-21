from llm.llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()

class WriterAgent:

    def __init__(self):
        self.llm = LLMClient()

        self.system_prompt = (
            "You are a professional technical content writer.\n"
            "Your job is to write clear, structured, and easy-to-understand content\n"
            "based on the provided plan and research data.\n\n"
            "Rules:\n"
            "- Do not invent facts.\n"
            "- Use only the given research data.\n"
            "- Write in a beginner-friendly but professional tone.\n"
            "- Use headings and bullet points where appropriate."
        )

    def write_content(self, plan: str, research_data: str):

        prompt = f"""
{self.system_prompt}

PLAN:
{plan}

RESEARCH DATA:
{research_data}

Write the final content now.
"""

        try:
            response = self.llm.generate(prompt)
            return response if response else "No content generated"
        except Exception as e:
            print("WRITER AGENT ERROR:", e)
            return "Writer agent failed to generate content"
