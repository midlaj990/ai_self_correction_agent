from fastapi import FastAPI
from app.orchestrator import Orchestrator
from app.services.vector_store import VectorStore
from config import DEFAULT_SITE_URL

app = FastAPI(title="Self-Correcting AI Agent")

orchestrator = Orchestrator()
vector_store = VectorStore()
vector_store.ingest_documents("data/documents")
vector_store.ingest_website(DEFAULT_SITE_URL)


@app.get("/")
def index():
    return {"status": "running"}


@app.post("/query")
def query_agent(query: str):
    docs = vector_store.retrieve(query)
    context = "\n\n".join(docs) if docs else ""

    result = orchestrator.handle_query(
        query=query,
        context=context
    )

    result["final_answer"] = result["final_answer"].strip()
    return result
