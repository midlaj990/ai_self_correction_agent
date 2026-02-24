from app.agents.generation_agent import GenerationAgent
from app.agents.evaluation_agent import EvaluationAgent
from app.agents.self_correction_agent import SelfCorrectionAgent
from app.services.vector_store import VectorStore


class Orchestrator:

    def __init__(self):
        self.generator = GenerationAgent()
        self.evaluator = EvaluationAgent()
        self.corrector = SelfCorrectionAgent()
        self.vector_store = VectorStore()

    def handle_query(self, query):

        docs = self.vector_store.retrieve(query)

        if not docs:
            context = ""
        else:
            context = "\n\n".join(docs)

        if not context or len(context.strip()) < 30:
            return {
                "final_answer": "The information is not available on the website.",
                "score": 100,
                "feedback": "No relevant context found.",
                "attempts": 0
            }

        # Only generate if context exists
        response = self.generator.generate(query, context)
        score, feedback = self.evaluator.evaluate(query, response)

        attempts = 0
        while score < 80 and attempts < 2:
            response = self.corrector.improve(query, response, feedback)
            score, feedback = self.evaluator.evaluate(query, response)
            attempts += 1

        return {
            "final_answer": response,
            "score": score,
            "feedback": feedback,
            "attempts": attempts
        }
