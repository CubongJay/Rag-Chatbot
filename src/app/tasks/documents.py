import os
from uuid import UUID

from app.config.database import get_async_database_session
from app.domain.entities.document import DocumentStatus, DocumentChunk
from app.infrastructure.repositories.document_repository_sqlalchemy import (
    DbDocumentRepository,
)
from app.infrastructure.repositories.document_chunk_repository_sqlalchemy import (
    DbDocumentChunkRepository,
)
from app.infrastructure.llm.openai_service import OpenAIService
from app.infrastructure.utils import text_splitter


async def process_document_task(document_id: UUID, file_path: str, session_id: UUID):
    """Reads file, chunks, embeds, stores in pgvector, updates status."""

    async_session = get_async_database_session()

    async with async_session() as db:
        repo = DbDocumentRepository(db)
        chunk_repo = DbDocumentChunkRepository(db)
        llm = OpenAIService()

        try:
           
            await repo.update_status(document_id, DocumentStatus.PROCESSING)

          
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == ".pdf":
                import pypdf
                reader = pypdf.PdfReader(file_path)
                raw_text = "".join(page.extract_text() or "" for page in reader.pages)
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_text = f.read()

          
            chunks = text_splitter.split_text_into_documents(raw_text)
            if not chunks:
                raise ValueError("No text extracted from file")

          
            chunk_entities = [
                DocumentChunk(
                    content=c.content,
                    metadata={
                        "document_id": str(document_id),
                        "session_id": str(session_id),
                        "chunk_index": i,
                    },
                )
                for i, c in enumerate(chunks)
            ]

          
            embeddings = await llm.embed_documents(
                [c.content for c in chunk_entities]
            )

            
            await chunk_repo.add_chunks(
                document_id=document_id,
                session_id=session_id,
                chunks=chunk_entities,
                embeddings=embeddings,
            )

          
            if os.path.exists(file_path):
                os.remove(file_path)

            
            await repo.update_status(
                document_id,
                DocumentStatus.SUCCESS,
                chunk_count=len(chunks),
            )

        except Exception as e:
            await repo.update_status(
                document_id,
                DocumentStatus.FAILED,
                error_message=str(e),
            )
            raise