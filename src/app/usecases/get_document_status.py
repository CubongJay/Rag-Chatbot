from uuid import UUID

from app.domain.interfaces.document_repository import DocumentRepository


class GetDocumentStatusUseCase:
    """Returns the status of a document by ID."""

    def __init__(self, document_repo: DocumentRepository):
        self.document_repo = document_repo

    async def execute(self, document_id: UUID):
        return await self.document_repo.get_by_id(document_id)