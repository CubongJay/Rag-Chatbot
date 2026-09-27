import os
import uuid
from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.document import DocumentRecord, DocumentStatus
from app.domain.interfaces.document_repository import DocumentRepository

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


@dataclass
class UploadDocumentResponse:
    document_id: UUID
    file_path: str
    status: str


class UploadDocumentUseCase:
    """Saves the file and creates a PENDING document record."""

    def __init__(self, document_repo: DocumentRepository):
        self.document_repo = document_repo

    async def execute(
        self, file_content: bytes, file_name: str, session_id: UUID
    ) -> UploadDocumentResponse:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        document_id = uuid.uuid4()
        safe_name = f"{document_id}_{file_name}"
        file_path = os.path.join(UPLOAD_DIR, safe_name)

        with open(file_path, "wb", ) as f:
            f.write(file_content)

        document = DocumentRecord(
            id=document_id,
            session_id=session_id,
            file_name=file_name,
            file_path=file_path,
            status=DocumentStatus.PENDING,
            chunk_count=0,
            error_message=None,
        )

        saved = await self.document_repo.save(document)

        return UploadDocumentResponse(
            document_id=saved.id,
            file_path=saved.file_path,
            status=saved.status.value,
        )