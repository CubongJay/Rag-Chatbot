# from fastapi import Depends

# from app.config.chroma_client import get_chroma_client
# from app.infrastructure.repositories.vector_store import (
#     DbVectorStoreRepository,
# )
# from app.usecases.create_context import CreateContextUsecase
# from app.usecases.upload_document import UploadDocumentUseCase


# async def get_vector_repository(
#     client=Depends(get_chroma_client),
# ) -> DbVectorStoreRepository:
#     return DbVectorStoreRepository()


# async def upload_document_usecase(
#     vector_repo: DbVectorStoreRepository = Depends(get_vector_repository),
# ):

#     return UploadDocumentUseCase(vector_repo)


# async def create_context_usecase(
#     vector_repo: DbVectorStoreRepository = Depends(get_vector_repository),
# ):
#     return CreateContextUsecase(vector_repo)
from fastapi import Depends

from app.infrastructure.db.session import get_async_db
        
from app.infrastructure.repositories.document_repository_sqlalchemy import (
    DbDocumentRepository,
)
from app.usecases.get_document_status import GetDocumentStatusUseCase
from app.usecases.upload_document import UploadDocumentUseCase



async def upload_document_usecase(
    db=Depends(get_async_db),
) -> UploadDocumentUseCase:
    """Dependency provider for UploadDocumentUseCase."""
    document_repo = DbDocumentRepository(db)
    return UploadDocumentUseCase(document_repo)


async def get_document_status_usecase(
    db=Depends(get_async_db),
) -> GetDocumentStatusUseCase:
    """Dependency provider for GetDocumentStatusUseCase."""
    document_repo = DbDocumentRepository(db)
    return GetDocumentStatusUseCase(document_repo)