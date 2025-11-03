from typing import Annotated, Callable, Optional
from uuid import UUID

from fastapi import Depends

from app.errors.errors import SessionNotFoundError
from app.schemas.pagination import PaginatedResponse, PaginationMeta
from app.schemas.session.requests import SessionUpdate
from app.schemas.session.responses import SessionCreateResponse, SessionResponse
from app.usecases.create_session import CreateSessionUseCase
from app.usecases.delete_session import DeleteSessionUseCase
from app.usecases.get_session import GetSessionUseCase
from app.usecases.get_sessions import GetSessionsUseCase
from app.usecases.update_session import UpdateSessionUseCase

from .usecases import (
    create_session_usecase,
    delete_session_usecase,
    get_session_usecase,
    get_sessions_usecase,
    update_session_usecase,
)


async def create_session_handler(
    use_case: CreateSessionUseCase = Depends(create_session_usecase),
) -> Callable[[str, bool], SessionCreateResponse]:
    """Dependency provider that returns a handler function."""

    async def handler(title: str, is_favorite: bool = False) -> SessionCreateResponse:
        new_session = await use_case.execute(title=title, is_favorite=is_favorite)

        return SessionCreateResponse(
            session_id=new_session.id,
            title=new_session.title,
            is_favorite=new_session.is_favorite,
            created_at=new_session.created_at,
        )

    return handler


async def get_sessions_handler(
    use_case: GetSessionsUseCase = Depends(get_sessions_usecase),
) -> Callable[[int, int, Optional[bool]], PaginatedResponse[SessionResponse]]:
    """Dependency provider that returns a handler function."""

    async def handler(
        page: int = 1, size: int = 10, is_favorite: Optional[bool] = None
    ) -> PaginatedResponse[SessionResponse]:
        if is_favorite is not None:
            sessions = await use_case.execute_by_favorite(
                is_favorite=is_favorite, page=page, size=size
            )
        else:
            sessions = await use_case.execute_all(page=page, size=size)

        total_sessions = await use_case.execute_count(is_favorite=is_favorite)
        total_pages = (total_sessions + size - 1) // size
        session_responses = [
            SessionResponse(
                id=session.id,
                title=session.title,
                is_favorite=session.is_favorite,
                created_at=session.created_at,
                updated_at=session.updated_at,
            )
            for session in sessions
        ]

        return PaginatedResponse(
            items=session_responses,
            pagination=PaginationMeta(
                page=page, size=size, total=total_sessions, pages=total_pages
            ),
        )

    return handler


async def get_session_handler(
    use_case: GetSessionUseCase = Depends(get_session_usecase),
) -> Callable[[UUID], SessionResponse]:
    """Dependency provider that returns a handler function."""

    async def handler(session_id: UUID) -> SessionResponse:
        session = await use_case.execute_by_id(session_id)
        if not session:
            raise SessionNotFoundError(session_id)
        return SessionResponse(
            id=session.id,
            title=session.title,
            is_favorite=session.is_favorite,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    return handler


async def delete_session_handler(
    use_case: DeleteSessionUseCase = Depends(delete_session_usecase),
) -> Callable[[UUID], None]:
    """Dependency provider that returns a handler function."""

    async def handler(session_id: UUID) -> bool:
        success = await use_case.execute(session_id)
        if not success:
            raise SessionNotFoundError(session_id)
        return success

    return handler


async def update_session_handler(
    use_case: UpdateSessionUseCase = Depends(update_session_usecase),
) -> Callable[[UUID, SessionUpdate], SessionResponse]:
    """Dependency provider that returns a handler function."""

    async def handler(
        session_id: UUID, session_update: SessionUpdate
    ) -> SessionResponse:
        updated_session = await use_case.execute(
            session_id=session_id,
            title=session_update.title,
            is_favorite=session_update.is_favorite,
        )
        if not updated_session:
            raise SessionNotFoundError(session_id)

        return SessionResponse(
            id=updated_session.id,
            title=updated_session.title,
            is_favorite=updated_session.is_favorite,
            created_at=updated_session.created_at,
            updated_at=updated_session.updated_at,
        )

    return handler


CreateSessionHandler = Annotated[
    Callable[[str, bool], SessionCreateResponse], Depends(create_session_handler)
]
GetSessionsHandler = Annotated[
    Callable[[int, int, Optional[bool]], PaginatedResponse[SessionResponse]],
    Depends(get_sessions_handler),
]
GetSessionHandler = Annotated[
    Callable[[UUID], SessionResponse], Depends(get_session_handler)
]
DeleteSessionHandler = Annotated[
    Callable[[UUID], None], Depends(delete_session_handler)
]
UpdateSessionHandler = Annotated[
    Callable[[UUID, SessionUpdate], SessionResponse], Depends(update_session_handler)
]
