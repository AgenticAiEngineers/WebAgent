from llm.llm_client import LLMClient


class ReflectionAgent:

    def __init__(self):
        self.llm = LLMClient()

    def reflect(self, question, draft):

        prompt = f"""
You are a reflection agent.

Check if the answer is correct and helpful.

If wrong:
- explain why
- give corrected answer
- state lesson learned

If correct:
- return the final corrected answer only

Question:
{question}

Answer:
{draft}
"""

        result = self.llm.generate(prompt)

        # -------- learning extraction --------
        if "lesson learned" in result.lower():
            with open("memory/learning_log.txt", "a", encoding="utf-8") as f:
                f.write("\n---\n")
                f.write(result)

        return result
