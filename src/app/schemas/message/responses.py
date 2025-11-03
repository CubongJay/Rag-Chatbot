from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.domain.entities.message import MessageType


class MessageResponse(BaseModel):
    """Schema for message response."""

    id: UUID
    session_id: UUID
    sender: str
    content: str
    message_type: MessageType
    timestamp: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class MessageListResponse(BaseModel):
    """Schema for listing messages in a session."""

    messages: list[MessageResponse]
    total_count: int
    session_id: UUID


class MessagePairResponse(BaseModel):
    """Schema for conversation pair (user message + AI response)."""

    user_message: MessageResponse
    assistant_message: MessageResponse
