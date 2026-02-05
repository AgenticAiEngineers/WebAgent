from langchain_groq import ChatGroq
from dotenv import load_dotenv
from tools.web_tool import web_search

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.3
        )

        self.system_prompt = (
            "You are a research agent.\n"
            "Your job is to gather accurate information related to the given task.\n"
            "Use web search results to create short, factual summaries.\n"
            "Rules:\n"
            "- Do not write final articles.\n"
            "- Only summarize important facts.\n"
            "- Keep responses concise and informative."
        )

    def research(self, task: str):

        # Step 1: Perform web search
        search_results = web_search(task)

        # Step 2: Summarize using LLM
        prompt = f"""
SYSTEM:
{self.system_prompt}

TASK:
{task}

WEB DATA:
{search_results}

Return summarized research findings.
"""

        response = self.llm.invoke(prompt)

        return response.content
