from llm.llm_client import LLMClient


class ValidatorAgent:

    def __init__(self):
        self.llm = LLMClient()

    def validate(self, answer: str):

        prompt = f"""
You are a safety validator.

Check the response below.

RULES:
- If the response is safe and correct → RETURN IT EXACTLY AS IT IS.
- Only modify if it contains harmful, unsafe, illegal, or dangerous content.
- Do NOT analyze the answer.
- Do NOT explain anything.
- Do NOT add comments.
- Return ONLY the final answer text.

Response:
{answer}
"""

        validated_answer = self.llm.generate_response(prompt)

        return validated_answer.strip()
