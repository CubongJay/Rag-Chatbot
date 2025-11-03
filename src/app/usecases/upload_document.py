from langchain_openai import OpenAIEmbeddings

from app.config.settings import get_settings
from app.domain.interfaces.vector_repository import VectorRepository
from app.infrastructure.utils import text_splitter

settings = get_settings()


class UploadDocumentUseCase:
    def __init__(self, vector_repo: VectorRepository):
        self.vector_repo = vector_repo

    async def execute(self, file_content: str, file_name: str):
        """Splits the uploaded files and saves chunks"""
        chunks = text_splitter.split_text_into_documents(file_content)

        documents = [
            {
                "id": f"{file_name}_{i}",
                "text": chunk.content,
                "metadata": {"source": file_name, "chunk_index": i},
            }
            for i, chunk in enumerate(chunks)
        ]
        print(documents)
        texts = [doc["text"] for doc in documents]
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.openai_api_key,
        )
        embeddings = embeddings.embed_documents(texts)
        self.vector_repo.add_documents(documents, embeddings=embeddings)
        return {
            "message": f"Uploaded {len(documents)} chunks from {file_name}."
        }
