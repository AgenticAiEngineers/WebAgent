from llm.llm_client import LLMClient
from orchestrator.router import Router
from memory.sqlite_memory import save_message, load_history, init_db
from memory.memory_classifier import MemoryClassifier
from memory.retriever import MemoryRetriever
from tools.calculator_tool import CalculatorTool
from agent.planner_agent import PlannerAgent
from agent.research_agent import ResearchAgent
from agent.writer_agent import WriterAgent
from agent.validator_agent import ValidatorAgent
from tools.web_tool import web_search


class Executor:

    def __init__(self):
        self.llm = LLMClient()
        self.router = Router(self.llm)
        self.memory_classifier = MemoryClassifier(self.llm)
        self.retriever = MemoryRetriever(self.llm)
        self.calculator = CalculatorTool()
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.writer = WriterAgent()
        self.validator = ValidatorAgent()

        init_db()

    def handle(self, user_input: str):

        decision = self.router.route(user_input)

        # ---------- CALCULATOR ----------
        if decision == "calculator":
            import re
            expression = re.findall(r"[0-9\.\+\-\*\/\(\)]+", user_input)
            if expression:
                expression = "".join(expression)
                return self.calculator.run(expression)
            return "I couldn't find a math expression."

        # ---------- MEMORY STORE ----------
        elif decision == "memory":
            save_message("memory", user_input)
            return "Got it. I will remember that."

        # ---------- WEB TOOL ----------
        elif decision == "web_tool":

            raw = web_search(user_input)

            filter_prompt = f"""
Extract ONLY information relevant to the user question.

Ignore:
- ads
- unrelated topics
- extra information
- SEO text

User question:
{user_input}

Search results:
{raw}

Relevant answer only:
"""

            filtered = self.llm.generate(filter_prompt)
            return filtered

        # ---------- PLANNER PIPELINE ----------
        elif decision == "planner":

            plan = self.planner.create_plan(user_input)
            research = self.researcher.research(user_input)
            draft = self.writer.write_content(plan, research)
            final = self.validator.validate(draft)

            save_message("assistant", final)
            return final

        # ---------- AUTO MEMORY STORE ----------
        if self.memory_classifier.should_store(user_input):
            save_message("memory", user_input)

        # ---------- SAVE USER MESSAGE ----------
        save_message("user", user_input)

        # ---------- LOAD MEMORY ----------
        history = load_history()

        memories = [
            item["content"]
            for item in history
            if item["role"] == "memory"
        ]

        memory_context = self.retriever.get_relevant(user_input, memories)

        # ---------- PROMPT WITH MEMORY ----------
        prompt = f"""
You are a helpful AI assistant.

Relevant known facts about user:
{memory_context}

Current user message:
{user_input}

Instructions:
- Use memory only if relevant
- If memory not relevant ignore it
- Respond naturally

Answer:
"""

        response = self.llm.generate(prompt)

        # ---------- SELF REVIEW ----------
        review_prompt = f"""
You are an AI reviewer.

Check the answer below.

If it is clear, correct, and complete → return EXACT SAME answer.
If it has mistakes or can be improved → return improved version.

Answer:
{response}
"""

        if len(response) > 150:
            improved = self.llm.generate(review_prompt)
        else:
            improved = response

        final_response = improved if improved else response

        save_message("assistant", final_response)

        return final_response
