class MemoryRetriever:

    def __init__(self, llm):
        self.llm = llm

    def get_relevant(self, question, memories):

        if not memories:
            return ""

        memory_text = "\n".join(memories)

        prompt = f"""
You are a memory filtering system.

User question:
{question}

Memories:
{memory_text}

Return only the memories relevant to answering the question.
If none are relevant, return NONE.
"""

        result = self.llm.generate(prompt)

        if "none" in result.lower():
            return ""

        return result.strip()
