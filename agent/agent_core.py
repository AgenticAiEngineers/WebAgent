from agent.tools import calculator_tool, search_tool
from llm.llm_client import LLMClient


class SimpleAgent:

    def __init__(self):
        self.llm = LLMClient()

    def run(self, user_input: str):

        text = user_input.lower()

        if "calculate" in text:
            expression = text.replace("calculate", "")
            return calculator_tool(expression)

        elif "search" in text:
            query = text.replace("search", "")
            return search_tool(query)

        else:
            return self.llm.generate_response(user_input)
