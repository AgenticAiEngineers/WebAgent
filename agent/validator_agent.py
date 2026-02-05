from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


class ValidatorAgent:

    def __init__(self):
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant",
            temperature=0.1
        )

        self.system_prompt = """
You are a validation and quality control agent.

Your job is to review AI-generated content and improve quality.

Rules:
- Fix grammar and clarity issues.
- Remove hallucinated or incorrect claims.
- Ensure professional tone.
- Preserve original meaning.
- Output the corrected final version only.
"""

    def validate_content(self, content: str):

        prompt = f"""
SYSTEM:
{self.system_prompt}

CONTENT TO VALIDATE:
{content}

Return only the improved final content.
"""

        response = self.llm.invoke(prompt)

        return response.content
