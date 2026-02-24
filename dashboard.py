import streamlit as st
from app.orchestrator import Orchestrator
from app.services.domain_crawler import DomainCrawler
from app.services.vector_store import VectorStore

st.set_page_config(page_title="AI Website Chatbot")

st.title("🌐 Website AI Chatbot")

url = st.text_input("Enter Website URL")

if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()

if st.button("Ingest Website"):
    crawler = DomainCrawler()
    texts = crawler.crawl(url)
    st.session_state.vector_store.ingest_texts(texts)
    st.success("Website ingested successfully!")

query = st.text_input("Ask a question")

if st.button("Ask") and query:
    orchestrator = Orchestrator()
    result = orchestrator.handle_query(query)

    st.subheader("Answer")
    st.write(result["final_answer"])

    st.subheader("Score")
    st.write(result["score"])

    st.subheader("Feedback")
    st.write(result["feedback"])
