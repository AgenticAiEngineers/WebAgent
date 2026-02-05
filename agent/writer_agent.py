from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class WriterAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.5
        )

        self.system_prompt = (
            "You are a professional technical content writer.\n"
            "Your job is to write clear, structured, and easy-to-understand content\n"
            "based on provided research and plan.\n"
            "Rules:\n"
            "- Do not invent facts.\n"
            "- Use the given research data.\n"
            "- Write in a beginner-friendly but professional tone.\n"
            "- Format content with headings and bullet points if needed."
        )

    def write_content(self, plan: str, research_data: str):

        prompt = f"""
SYSTEM:
{self.system_prompt}

PLAN:
{plan}

RESEARCH DATA:
{research_data}

Write the final content now.
"""

        response = self.llm.invoke(prompt)
        return response.content
