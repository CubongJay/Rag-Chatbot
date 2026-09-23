from typing import List
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.document import DocumentChunk
from app.domain.interfaces.document_chunk_repository import DocumentChunkRepository
from app.infrastructure.db.models import DocumentChunk as DocumentChunkModel


class DbDocumentChunkRepository(DocumentChunkRepository):
    """SQLAlchemy implementation of DocumentChunkRepository."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_chunks(
        self,
        document_id: UUID,
        session_id: UUID,
        chunks: List[DocumentChunk],
        embeddings: List[List[float]],
    ) -> int:
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match")

        db_chunks = [
            DocumentChunkModel(
                document_id=document_id,
                session_id=session_id,
                content=chunk.content,
                embedding=embedding,
                chunk_index=chunk.metadata.get("chunk_index", i),
            )
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings))
        ]

        self.db_session.add_all(db_chunks)
        await self.db_session.commit()
        return len(db_chunks)

    async def delete_by_document_id(self, document_id: UUID) -> None:
        stmt = delete(DocumentChunkModel).where(
            DocumentChunkModel.document_id == document_id
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()

    async def get_chunks_by_document_id(self, document_id: UUID) -> List[DocumentChunk]:
        stmt = (
            select(DocumentChunkModel)
            .where(DocumentChunkModel.document_id == document_id)
            .order_by(DocumentChunkModel.chunk_index)
        )
        result = await self.db_session.execute(stmt)
        db_chunks = result.scalars().all()
        return [self._to_domain_entity(c) for c in db_chunks]

    def _to_domain_entity(self, db_chunk: DocumentChunkModel) -> DocumentChunk:
        return DocumentChunk(
            content=db_chunk.content,
            metadata={
                "document_id": str(db_chunk.document_id),
                "session_id": str(db_chunk.session_id),
                "chunk_index": db_chunk.chunk_index,
            },
        )