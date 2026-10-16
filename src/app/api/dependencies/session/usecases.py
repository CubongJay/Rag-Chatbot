from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.session import get_async_db
from app.infrastructure.repositories.message_repository_sqlalchemy import (
    DbMessageRepository,
)
from app.infrastructure.repositories.session_repository_sqlalchemy import (
    DbSessionRepository,
)
from app.usecases.create_session import CreateSessionUseCase
from app.usecases.delete_session import DeleteSessionUseCase
from app.usecases.get_session import GetSessionUseCase
from app.usecases.get_sessions import GetSessionsUseCase
from app.usecases.update_session import UpdateSessionUseCase


async def get_session_repository(
    db: AsyncSession = Depends(get_async_db),
) -> DbSessionRepository:
    """Shared dependency provider for DbSessionRepository."""
    return DbSessionRepository(db)


async def get_message_repository(
    db: AsyncSession = Depends(get_async_db),
) -> DbMessageRepository:
    """Shared dependency provider for DbMessageRepository."""
    return DbMessageRepository(db)


async def create_session_usecase(
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> CreateSessionUseCase:
    """Dependency provider for CreateSessionUseCase."""
    return CreateSessionUseCase(session_repo)


async def get_sessions_usecase(
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> GetSessionsUseCase:
    """Dependency provider for GetSessionsUseCase."""
    return GetSessionsUseCase(session_repo)


async def get_session_usecase(
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> GetSessionUseCase:
    """Dependency provider for GetSessionUseCase."""
    return GetSessionUseCase(session_repo)


async def delete_session_usecase(
    session_repo: DbSessionRepository = Depends(get_session_repository),
    message_repo: DbMessageRepository = Depends(get_message_repository),
) -> DeleteSessionUseCase:
    """Dependency provider for DeleteSessionUseCase."""
    return DeleteSessionUseCase(session_repo, message_repo)


async def update_session_usecase(
    session_repo: DbSessionRepository = Depends(get_session_repository),
) -> UpdateSessionUseCase:
    """Dependency provider for UpdateSessionUseCase."""
    return UpdateSessionUseCase(session_repo)
