import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class SelfCorrectionAgent:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-20b"

    def improve(self, query, previous_answer, feedback):

        prompt = f"""
Improve this answer based on feedback.

Question:
{query}

Previous Answer:
{previous_answer}

Feedback:
{feedback}

Improved Answer:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content.strip()
