import re
import logging
from concurrent.futures import ThreadPoolExecutor

from agent.reflection_agent import ReflectionAgent
from agent.tools import calculator_tool, search_tool, smart_query_rewrite
from tools.time_tool import time_tool

from llm.llm_client import LLMClient
from memory.sqlite_memory import save_message, load_history
from memory.chromadb_memory import VectorMemory
from agent.planner_agent import PlannerAgent
try:
    from logs.logger import logger
except Exception:
    logger = logging.getLogger("webagent")


# =====================================================
# DEBUG MODE
# =====================================================
DEBUG = True


def log(msg):
    if DEBUG:
        print(msg)


# =====================================================
# SAFE TOOL EXECUTION
# =====================================================
def safe_execute(tool_function, argument, retries=2):
    for attempt in range(retries):
        try:
            result = tool_function(argument)

            if result is None or result == "":
                raise ValueError("Empty result")

            return result

        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Tool failed: {str(e)}")
                return f"[Tool failed: {str(e)}]"


# =====================================================
# MAIN AGENT
# =====================================================
class SimpleAgent:

    def __init__(self):
        self.llm = LLMClient()
        self.memory = load_history()
        self.vector_memory = VectorMemory()
        self.planner = PlannerAgent()
        self.reflector = ReflectionAgent()

    # =================================================
    # BUILD CONVERSATION CONTEXT (FIX FOR MEMORY)
    # =================================================
    def build_context(self, user_input):

        # last 8 turns memory
        recent_memory = self.memory[-8:]

        convo = ""
        for msg in recent_memory:
            convo += f"{msg['role']}: {msg['content']}\n"

        # vector memory
        relevant = self.vector_memory.search_memory(user_input)
        relevant_block = "\n".join(relevant)

        return f"""
Conversation History:
{convo}

Relevant Memories:
{relevant_block}

User: {user_input}
"""

    # =================================================
    # MAIN RUN LOOP
    # =================================================
    def run(self, user_input: str):

        log("\n==============================")
        log(f"USER INPUT: {user_input}")
        logger.info(f"USER INPUT: {user_input}")
        log("==============================")

        # store user message
        self.memory.append({"role": "user", "content": user_input})
        save_message("user", user_input)
        self.vector_memory.store_memory(user_input, id=str(len(self.memory)))

        user_lower = user_input.lower()

        # =================================================
        # DIRECT MATH FAST PATH  ⚡ (NO LLM)
        # =================================================
        if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", user_input):
            log("Math detected → calculator")
            result = calculator_tool(user_input)

            self.memory.append({"role": "assistant", "content": result})
            save_message("assistant", result)
            return result

        # =================================================
        # WRITING TASK
        # =================================================
        writing_words = ["write", "blog", "essay", "article", "story", "paragraph"]

        if any(w in user_lower for w in writing_words):
            log("Creative task → LLM")

            context_prompt = self.build_context(user_input)
            result = self.llm.generate(context_prompt)

            self.memory.append({"role": "assistant", "content": result})
            save_message("assistant", result)
            self.vector_memory.store_memory(result, id=str(len(self.memory)))

            return result

        # =================================================
        # TIME TOOL
        # =================================================
        time_words = ["time", "date", "clock", "current time", "current date"]

        if any(w in user_lower for w in time_words):
            log("Time query → tool")

            result = time_tool(user_input)

            self.memory.append({"role": "assistant", "content": result})
            save_message("assistant", result)
            return result

        # =================================================
        # PLANNER
        # =================================================
        log("Generating plan...")
        steps = self.planner.create_task_plan(user_input)

        # =================================================
        # PARALLEL EXECUTION
        # =================================================
        def execute_step(step):
            log(f"Running step: {step}")
            step_lower = step.lower()

            math_words = ["sum", "add", "plus", "minus", "multiply", "divide"]

            if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", step_lower) or any(
                w in step_lower for w in math_words
            ):
                return safe_execute(calculator_tool, step)

            query = smart_query_rewrite(step)
            return safe_execute(search_tool, query)

        collected = []

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(execute_step, step) for step in steps]
            for f in futures:
                collected.append(f.result())

        collected_info = "\n".join(collected)

        # =================================================
        # FINAL ANSWER PROMPT  (WITH MEMORY)
        # =================================================
        context_block = self.build_context(user_input)

        summary_prompt = f"""
You are a helpful AI assistant.

Use conversation context if relevant.
Answer clearly and naturally.

{context_block}

External Information:
{collected_info}

Answer:
"""

        draft = self.llm.generate(summary_prompt)

        # =================================================
        # REFLECTION CONTROL
        # =================================================
        simple = draft.strip()

        if (
            simple.replace(".", "", 1).isdigit()
            or len(simple) < 25
        ):
            response = simple
        else:
            response = self.reflector.reflect(user_input, draft)

        # =================================================
        # STORE RESPONSE
        # =================================================
        self.memory.append({"role": "assistant", "content": response})
        save_message("assistant", response)
        self.vector_memory.store_memory(response, id=str(len(self.memory)))

        logger.info("Response generated successfully")
        return response
