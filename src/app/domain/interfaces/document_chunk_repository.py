from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.domain.entities.document import DocumentChunk


class DocumentChunkRepository(ABC):
    """Abstract repository interface for DocumentChunk entities."""

    @abstractmethod
    async def add_chunks(
        self,
        document_id: UUID,
        session_id: UUID,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
    ) -> int:
        """Store chunks with their embeddings. Returns count stored."""
        pass

    @abstractmethod
    async def delete_by_document_id(self, document_id: UUID) -> None:
        """Delete all chunks for a document."""
        pass

    @abstractmethod
    async def get_chunks_by_document_id(self, document_id: UUID) -> List[DocumentChunk]:
        """Retrieve all chunks for a document."""
        pass