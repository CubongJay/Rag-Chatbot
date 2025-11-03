from fastapi import Depends

from app.config.chroma_client import get_chroma_client
from app.infrastructure.repositories.vector_store import (
    DbVectorStoreRepository,
)
from app.usecases.create_context import CreateContextUsecase
from app.usecases.upload_document import UploadDocumentUseCase


async def get_vector_repository(
    client=Depends(get_chroma_client),
) -> DbVectorStoreRepository:
    return DbVectorStoreRepository()


async def upload_document_usecase(
    vector_repo: DbVectorStoreRepository = Depends(get_vector_repository),
):

    return UploadDocumentUseCase(vector_repo)


async def create_context_usecase(
    vector_repo: DbVectorStoreRepository = Depends(get_vector_repository),
):
    return CreateContextUsecase(vector_repo)
