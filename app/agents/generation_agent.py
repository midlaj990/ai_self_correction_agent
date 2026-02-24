import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GenerationAgent:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-20b"

    def generate(self, query, context):

        prompt = f"""
You are a website AI assistant.

STRICT RULES:
- Answer ONLY using the provided CONTEXT.
- If the answer is not clearly present in CONTEXT, say:
  "The information is not available on the website."
- Do NOT use outside knowledge.
- Do NOT guess.
- Do NOT hallucinate.

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You answer using only context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
