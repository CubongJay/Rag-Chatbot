from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.document import DocumentRecord, DocumentStatus
from app.domain.interfaces.document_repository import DocumentRepository
from app.infrastructure.db.models import Document as DocumentModel


class DbDocumentRepository(DocumentRepository):
    """SQLAlchemy implementation of DocumentRepository."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(self, document: DocumentRecord) -> DocumentRecord:
        db_document = DocumentModel(
            id=document.id,
            session_id=document.session_id,
            file_name=document.file_name,
            file_path=document.file_path,
            status=document.status,
            chunk_count=document.chunk_count,
            error_message=document.error_message,
        )
        self.db_session.add(db_document)
        await self.db_session.commit()
        await self.db_session.refresh(db_document)
        return self._to_domain_entity(db_document)

    async def update_status(
        self,
        document_id: UUID,
        status: DocumentStatus,
        error_message: Optional[str] = None,
        chunk_count: Optional[int] = None,
    ) -> DocumentRecord:
        document = await self.db_session.get(DocumentModel, document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found")

        document.status = status
        if error_message is not None:
            document.error_message = error_message
        if chunk_count is not None:
            document.chunk_count = chunk_count

        await self.db_session.commit()
        await self.db_session.refresh(document)
        return self._to_domain_entity(document)

    async def get_by_id(self, document_id: UUID) -> Optional[DocumentRecord]:
        document = await self.db_session.get(DocumentModel, document_id)
        if not document:
            return None
        return self._to_domain_entity(document)

    def _to_domain_entity(self, db_document: DocumentModel) -> DocumentRecord:
        return DocumentRecord(
            id=db_document.id,
            session_id=db_document.session_id,
            file_name=db_document.file_name,
            file_path=db_document.file_path,
            status=db_document.status,
            chunk_count=db_document.chunk_count,
            error_message=db_document.error_message,
            created_at=db_document.created_at,
            updated_at=db_document.updated_at,
        )