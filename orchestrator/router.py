class Router:

    def __init__(self, llm):
        self.llm = llm

    def route(self, user_input: str):

        prompt = f"""
You are an AI intent classifier.

Decide what action should be taken for this input.

Options:
- calculator → math expressions
- memory → user wants to store personal info
- web_tool → ONLY if user asks for latest news or real-time info
- planner → long tasks like writing blogs, reports, research
- llm → general questions or conversation

Reply ONLY one word:
calculator OR memory OR web_tool OR planner OR llm

Input:
{user_input}
"""



        decision = self.llm.generate(prompt).lower().strip()

        if "calculator" in decision:
            return "calculator"

        elif "memory" in decision:
            return "memory"

        elif "web" in decision:
            return "web_tool"
        elif "planner" in decision:
           return "planner"

        else:
            return "llm"
