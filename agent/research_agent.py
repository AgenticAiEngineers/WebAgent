from llm.llm_client import LLMClient
from dotenv import load_dotenv
from tools.web_tool import web_search

load_dotenv()

class ResearchAgent:
    def __init__(self):
        self.llm = LLMClient()

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
{self.system_prompt}

TASK:
{task}

WEB DATA:
{search_results}

Return summarized research findings.
"""

        response = self.llm.generate(prompt)

        return response
