from typing import List

from app.domain.entities.document import Document
from app.domain.interfaces.vector_repository import VectorRepository
from app.infrastructure.utils.text_splitter import split_text_into_documents


class CreateContextUsecase:

    def __init__(self, vector_repo: VectorRepository):
        self.vector_repo = vector_repo

    def execute(self, text: str, metadata: dict = None):
        """Add a document to the vector store."""

        documents: List[Document] = self._split_text(
            text=text, metadata=metadata
        )
        self.vector_repo.add_documents(documents)

    def _split_text(self, text: str, metadata: dict = None):
        """Splits text into smaller chunks."""
        chunks = split_text_into_documents(
            text=text, chunk_size=500, overlap=50
        )
        return [Document(content=chunk, metadata=metadata) for chunk in chunks]
