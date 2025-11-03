import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies.message.handlers import (
    CreateMessageHandler,
    DeleteMessageHandler,
    GetMessageHandler,
    GetMessagesHandler,
)
from app.schemas.message.requests import MessageCreateRequest
from app.schemas.message.responses import MessagePairResponse, MessageResponse
from app.schemas.pagination import PaginatedResponse
from app.security.auth import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sessions", tags=["messages"])


@router.post(
    "/{session_id}/messages/",
    status_code=status.HTTP_201_CREATED,
    response_model=MessagePairResponse,
)
async def create_message(
    session_id: UUID,
    message_create: MessageCreateRequest,
    create_message_handler: CreateMessageHandler,
    api_key: str = Depends(verify_api_key),
):
    return await create_message_handler(session_id, message_create)


@router.get(
    "/{session_id}/messages/", response_model=PaginatedResponse[MessageResponse]
)
async def get_messages(
    session_id: UUID,
    get_messages_handler: GetMessagesHandler,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    api_key: str = Depends(verify_api_key),
):
    """Get all messages for a session with pagination."""
    return await get_messages_handler(session_id, page, size)


@router.get("/{session_id}/messages/{message_id}/", response_model=MessageResponse)
async def get_message(
    session_id: UUID,
    message_id: UUID,
    get_message_handler: GetMessageHandler,
    api_key: str = Depends(verify_api_key),
):
    """Get a specific message by ID."""
    return await get_message_handler(session_id, message_id)


@router.delete(
    "/{session_id}/messages/{message_id}/", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_message(
    session_id: UUID,
    message_id: UUID,
    delete_message_handler: DeleteMessageHandler,
    api_key: str = Depends(verify_api_key),
):
    """Delete a specific message by ID."""
    await delete_message_handler(session_id, message_id)
