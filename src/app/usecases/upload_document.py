# from langchain_openai import OpenAIEmbeddings

# from app.config.settings import get_settings
# from app.domain.interfaces.vector_repository import VectorRepository
# from app.infrastructure.utils import text_splitter

# settings = get_settings()


# class UploadDocumentUseCase:
#     def __init__(self, vector_repo: VectorRepository):
#         self.vector_repo = vector_repo

#     async def execute(self, file_content: str, file_name: str):
#         """Splits the uploaded files and saves chunks"""
#         chunks = text_splitter.split_text_into_documents(file_content)

#         documents = [
#             {
#                 "id": f"{file_name}_{i}",
#                 "text": chunk.content,
#                 "metadata": {"source": file_name, "chunk_index": i},
#             }
#             for i, chunk in enumerate(chunks)
#         ]
#         print(documents)
#         texts = [doc["text"] for doc in documents]
#         embeddings = OpenAIEmbeddings(
#             model="text-embedding-3-small",
#             openai_api_key=settings.openai_api_key,
#         )
#         embeddings = embeddings.embed_documents(texts)
#         self.vector_repo.add_documents(documents, embeddings=embeddings)
#         return {
#             "message": f"Uploaded {len(documents)} chunks from {file_name}."
#         }
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
        self, file_content: str, file_name: str, session_id: UUID
    ) -> UploadDocumentResponse:
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        document_id = uuid.uuid4()
        safe_name = f"{document_id}_{file_name}"
        file_path = os.path.join(UPLOAD_DIR, safe_name)

        with open(file_path, "w", encoding="utf-8") as f:
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