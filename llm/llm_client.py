import os
from dotenv import load_dotenv

try:
    from google import genai as google_genai
except Exception:
    google_genai = None

try:
    import google.generativeai as google_generativeai
except Exception:
    google_generativeai = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


class LLMClient:

    def __init__(self):
        api_key = (
            os.getenv("GOOGLE_API_KEY")
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("OPENAI_API_KEY")
        )

        if not api_key:
            raise RuntimeError(
                "No API key found in .env. Set one of: GOOGLE_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY"
            )

        if google_genai is not None:
            self._provider = "google-genai"
            self.client = google_genai.Client(api_key=api_key)
            return

        if google_generativeai is not None:
            self._provider = "google-generativeai"
            google_generativeai.configure(api_key=api_key)
            self.client = None
            return

        raise RuntimeError(
            "No Gemini SDK found. Install one of: `pip install google-genai` "
            "or `pip install google-generativeai`"
        )

    def generate(self, prompt: str):
        if self._provider == "google-genai":
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text

        response = google_generativeai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
        return response.text

    def generate_response(self, prompt):
        return self.generate(prompt)

   
