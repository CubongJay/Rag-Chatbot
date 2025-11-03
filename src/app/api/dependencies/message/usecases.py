from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_async_db
from app.infrastructure.llm.openai_service import OpenAIService
from app.infrastructure.repositories.message_repository_sqlalchemy import (
    DbMessageRepository,
)
from app.infrastructure.repositories.session_repository_sqlalchemy import (
    DbSessionRepository,
)
from app.infrastructure.repositories.vector_store import (
    DbVectorStoreRepository,
)
from app.usecases.create_message import CreateMessageUseCase
from app.usecases.delete_message import DeleteMessageUseCase
from app.usecases.generate_ai_response import GenerateAIResponseUseCase
from app.usecases.get_message import GetMessageUseCase
from app.usecases.get_messages import GetMessagesUseCase


async def get_message_repository(
    db: AsyncSession = Depends(get_async_db),
) -> DbMessageRepository:
    """Shared dependency provider for DbMessageRepository."""
    return DbMessageRepository(db)


async def get_session_repository(
    db: AsyncSession = Depends(get_async_db),
) -> DbSessionRepository:
    """Shared dependency provider for DbSessionRepository."""
    return DbSessionRepository(db)


async def get_vector_repository() -> DbVectorStoreRepository:
    """Shared dependency provider for DbVectorStoreRepository."""
    return DbVectorStoreRepository()


async def create_message_usecase(
    message_repo: DbMessageRepository = Depends(get_message_repository),
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> CreateMessageUseCase:
    """Dependency provider for CreateMessageUseCase."""
    return CreateMessageUseCase(message_repo, session_repo)


async def generate_ai_response_usecase(
    message_repo: DbMessageRepository = Depends(get_message_repository),
    session_repo: DbSessionRepository = Depends(get_session_repository),
    vector_repo: DbVectorStoreRepository = Depends(get_vector_repository),
) -> GenerateAIResponseUseCase:
    """Dependency provider for GenerateAIResponseUseCase."""
    llm_service = OpenAIService()
    return GenerateAIResponseUseCase(
        message_repo, session_repo, llm_service, vector_repo
    )


async def get_message_usecase(
    message_repo: DbMessageRepository = Depends(get_message_repository),
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> GetMessageUseCase:
    """Dependency provider for GetMessageUseCase."""
    return GetMessageUseCase(message_repo, session_repo)


async def get_messages_usecase(
    message_repo: DbMessageRepository = Depends(get_message_repository),
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> GetMessagesUseCase:
    """Dependency provider for GetMessagesUseCase."""
    return GetMessagesUseCase(message_repo, session_repo)


async def delete_message_usecase(
    message_repo: DbMessageRepository = Depends(get_message_repository),
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> DeleteMessageUseCase:
    """Dependency provider for DeleteMessageUseCase."""
    return DeleteMessageUseCase(message_repo, session_repo)
