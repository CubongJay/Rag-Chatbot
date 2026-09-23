from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.domain.entities.document import DocumentRecord, DocumentStatus


class DocumentRepository(ABC):
    """Abstract repository interface for DocumentRecord entities."""

    @abstractmethod
    async def save(self, document: DocumentRecord) -> DocumentRecord:
        """Save a document record."""
        pass

    @abstractmethod
    async def update_status(
        self,
        document_id: UUID,
        status: DocumentStatus,
        error_message: Optional[str] = None,
        chunk_count: Optional[int] = None,
    ) -> DocumentRecord:
        """Update the status of a document record."""
        pass

    @abstractmethod
    async def get_by_id(self, document_id: UUID) -> Optional[DocumentRecord]:
        """Retrieve a document record by ID."""
        pass