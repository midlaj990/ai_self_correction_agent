import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class EvaluationAgent:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-20b"

    def evaluate(self, query, answer):

        prompt = f"""
Score this answer from 0 to 100.

Question:
{query}

Answer:
{answer}

Return format:
Score: <number>
Feedback: <short explanation>
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content

        try:
            score = int(output.split("Score:")[1].split("\n")[0].strip())
        except:
            score = 0

        feedback = output.split("Feedback:")[-1].strip()

        return score, feedback
