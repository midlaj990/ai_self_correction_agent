import chromadb
from chromadb.utils import embedding_functions
from app.services.semantic_chunker import SemanticChunker


class VectorStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(path="chroma_db")

        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-large-en-v1.5"
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            embedding_function=self.embedding_function
        )

        self.chunker = SemanticChunker()

    def ingest_texts(self, texts):

        for idx, text in enumerate(texts):

            chunks = self.chunker.chunk(text)

            for i, chunk in enumerate(chunks):
                self.collection.add(
                    documents=[chunk],
                    ids=[f"{idx}_{i}"]
                )

    def retrieve(self, query, top_k=4):

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )

        return results["documents"][0] if results["documents"] else []
