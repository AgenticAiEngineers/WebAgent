from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

class LLMClient:

    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_response(self, prompt: str):

        try:
            completion = self.client.chat.completions.create(
                model="qwen/qwen3-32b",
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            return completion.choices[0].message.content

        except Exception as e:
            print("LLM ERROR:", e)
            return "LLM error occurred"
