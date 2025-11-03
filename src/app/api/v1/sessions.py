from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.session.handlers import (
    CreateSessionHandler,
    DeleteSessionHandler,
    GetSessionHandler,
    GetSessionsHandler,
    UpdateSessionHandler,
)
from app.schemas.pagination import PaginatedResponse
from app.schemas.session.requests import SessionCreate, SessionUpdate
from app.schemas.session.responses import SessionCreateResponse, SessionResponse
from app.security.auth import verify_api_key

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=SessionCreateResponse
)
async def create_session(
    session_in: SessionCreate,
    create_handler: CreateSessionHandler,
    api_key: str = Depends(verify_api_key),
):

    return await create_handler(
        title=session_in.title.strip(),
        is_favorite=session_in.is_favorite,
    )


@router.get("/", response_model=PaginatedResponse[SessionResponse])
async def get_sessions(
    sessions_handler: GetSessionsHandler,
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    is_favorite: Optional[bool] = Query(None, description="Filter by favorite status"),
    api_key: str = Depends(verify_api_key),
):
    return await sessions_handler(page=page, size=size, is_favorite=is_favorite)


@router.get("/{session_id}/", response_model=SessionResponse)
async def get_session(
    session_id: UUID,
    get_session_handler: GetSessionHandler,
    api_key: str = Depends(verify_api_key),
):

    return await get_session_handler(session_id)


@router.put("/{session_id}/", response_model=SessionResponse)
async def update_session(
    session_id: UUID,
    session_update: SessionUpdate,
    update_session_handler: UpdateSessionHandler,
    api_key: str = Depends(verify_api_key),
):
    return await update_session_handler(session_id, session_update)


@router.delete("/{session_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: UUID,
    delete_session_handler: DeleteSessionHandler,
    api_key: str = Depends(verify_api_key),
):
    await delete_session_handler(session_id)
    return None
