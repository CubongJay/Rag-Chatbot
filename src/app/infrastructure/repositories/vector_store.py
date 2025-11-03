from typing import List

from app.config.chroma_client import get_chroma_client
from app.domain.interfaces.vector_repository import VectorRepository


class DbVectorStoreRepository(VectorRepository):
    """Wrapper around a vectore database."""

    def __init__(self, collection_name: str = "documents"):
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add_documents(self, documents: List[dict], embeddings: list) -> None:
        """Add documents to the vector store."""

        ids = [doc["id"] for doc in documents]
        # print(ids)
        texts = [doc["text"] for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas or [{} for _ in texts],
        )

    # def query(self, txt: str, top_k: int = 3):
    #     """Retrieve most relevant documents for a given query."""
    #     results = self.collection.query(
    #         query_texts=[txt],
    #         n_results=top_k,
    #     )
    #     documents = results["documents"][0]
    #     return documents

    def clear(self) -> None:
        """Clear all documents from the vector store."""
        self.collection.delete(where={})

    def query_relevant_chunks(self, embedded_text, top_k: int = 3):
        results = self.collection.query(
            query_embeddings=[embedded_text], n_results=top_k
        )
        docs = (
            results["documents"][0]
            if results and "documents" in results
            else []
        )
        return docs
