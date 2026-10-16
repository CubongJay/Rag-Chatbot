from typing import Annotated, Callable
from uuid import UUID

from fastapi import Depends, HTTPException

from app.schemas.message.requests import MessageCreateRequest
from app.schemas.message.responses import MessagePairResponse, MessageResponse
from app.schemas.pagination import PaginatedResponse, PaginationMeta
from app.usecases.create_message import CreateMessageUseCase
from app.usecases.delete_message import DeleteMessageUseCase
from app.usecases.generate_ai_response import GenerateAIResponseUseCase
from app.usecases.get_message import GetMessageUseCase
from app.usecases.get_messages import GetMessagesUseCase

from .usecases import (
    create_message_usecase,
    delete_message_usecase,
    generate_ai_response_usecase,
    get_message_usecase,
    get_messages_usecase,
)


async def create_message_handler(
    use_case: CreateMessageUseCase = Depends(create_message_usecase),
    ai_use_case: GenerateAIResponseUseCase = Depends(
        generate_ai_response_usecase
    ),
) -> Callable[[UUID, MessageCreateRequest], MessagePairResponse]:

    async def handler(
        session_id: UUID, message_create: MessageCreateRequest
    ) -> MessagePairResponse:
        user_message = await use_case.execute(
            session_id=session_id,
            content=message_create.content,
            sender=message_create.sender,
            message_type=message_create.message_type,
        )

        ai_message = await ai_use_case.execute(
            session_id=session_id, user_message_content=message_create.content
        )
        if not ai_message:
            raise HTTPException(
                status_code=400,
                detail="Failed to generate AI response message",
            )
        return MessagePairResponse(
            user_message=MessageResponse(
                id=user_message.id,
                session_id=user_message.session_id,
                sender=user_message.sender,
                content=user_message.content,
                message_type=user_message.message_type,
                timestamp=user_message.timestamp,
                created_at=user_message.created_at,
                updated_at=user_message.updated_at,
            ),
            assistant_message=MessageResponse(
                id=ai_message.id,
                session_id=ai_message.session_id,
                sender=ai_message.sender,
                content=ai_message.content,
                message_type=ai_message.message_type,
                timestamp=ai_message.timestamp,
                created_at=ai_message.created_at,
                updated_at=ai_message.updated_at,
            ),
        )

    return handler


async def get_messages_handler(
    use_case: GetMessagesUseCase = Depends(get_messages_usecase),
) -> Callable[[UUID, int, int], PaginatedResponse[MessageResponse]]:
    async def handler(
        session_id: UUID, page: int, size: int
    ) -> PaginatedResponse[MessageResponse]:
        messages = await use_case.execute_by_session_id(session_id, page, size)
        if not messages:
            raise HTTPException(
                status_code=404,
                detail=f"Messages with session id {session_id} not found",
            )

        total_count = await use_case.execute_count_by_session_id(session_id)
        total_pages = (total_count + size - 1) // size

        message_responses = [
            MessageResponse(
                id=msg.id,
                session_id=msg.session_id,
                sender=msg.sender,
                content=msg.content,
                message_type=msg.message_type,
                timestamp=msg.timestamp,
                created_at=msg.created_at,
                updated_at=msg.updated_at,
            )
            for msg in messages
        ]
        return PaginatedResponse(
            items=message_responses,
            pagination=PaginationMeta(
                page=page, size=size, total=total_count, pages=total_pages
            ),
        )

    return handler


async def get_message_handler(
    use_case: GetMessageUseCase = Depends(get_message_usecase),
) -> Callable[[UUID, UUID], MessageResponse]:
    """Dependency provider that returns a handler function for getting a single message."""

    async def handler(session_id: UUID, message_id: UUID) -> MessageResponse:
        message = await use_case.execute_by_id(message_id)
        if not message:
            raise HTTPException(
                status_code=404,
                detail=f"Message with id {message_id} not found",
            )

        return MessageResponse(
            id=message.id,
            session_id=message.session_id,
            sender=message.sender,
            content=message.content,
            message_type=message.message_type,
            timestamp=message.timestamp,
            created_at=message.created_at,
            updated_at=message.updated_at,
        )

    return handler


CreateMessageHandler = Annotated[
    Callable[[UUID, MessageCreateRequest], MessagePairResponse],
    Depends(create_message_handler),
]
GetMessagesHandler = Annotated[
    Callable[[UUID, int, int], PaginatedResponse[MessageResponse]],
    Depends(get_messages_handler),
]
GetMessageHandler = Annotated[
    Callable[[UUID, UUID], MessageResponse],
    Depends(get_message_handler),
]


async def delete_message_handler(
    use_case: DeleteMessageUseCase = Depends(delete_message_usecase),
) -> Callable[[UUID, UUID], bool]:
    """Dependency provider that returns a handler function for deleting a single message."""

    async def handler(session_id: UUID, message_id: UUID) -> bool:
        return await use_case.execute_by_id(message_id)

    return handler


DeleteMessageHandler = Annotated[
    Callable[[UUID, UUID], bool],
    Depends(delete_message_handler),
]
