from abc import ABC, abstractmethod
from typing import List


class VectorRepository(ABC):
    @abstractmethod
    def add_documents(self, documents: List[dict], embeddings: list) -> None:
        """Add documents to the vector store."""
        pass

    @abstractmethod
    def query_relevant_chunks(self, txt: str, top_k: int = 3):
        """Retrieve most relevant documents for a given query."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all documents from the vector store."""
        pass
