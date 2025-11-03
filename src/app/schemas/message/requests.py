from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.domain.entities.message import MessageType


class MessageCreate(BaseModel):
    """Schema for creating a new message."""

    session_id: UUID
    sender: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=4000)
    message_type: MessageType = MessageType.USER

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()

    @field_validator("sender")
    @classmethod
    def validate_sender(cls, v):
        if not v or not v.strip():
            raise ValueError("Sender cannot be empty")
        return v.strip()


class MessageCreateRequest(BaseModel):
    """Schema for creating a message via API endpoint (session_id from URL)."""

    sender: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=4000)
    message_type: MessageType = MessageType.USER

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()

    @field_validator("sender")
    @classmethod
    def validate_sender(cls, v):
        if not v or not v.strip():
            raise ValueError("Sender cannot be empty")
        return v.strip()


class MessageUpdate(BaseModel):
    """Schema for updating an existing message."""

    content: str = Field(..., min_length=1, max_length=4000)

    @field_validator("content")
    @classmethod
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()
