from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.entities.message import MessageType


class MessageQueryParams(BaseModel):
    """Schema for message query parameters."""

    session_id: UUID
    message_type: Optional[MessageType] = None
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    offset: Optional[int] = Field(default=0, ge=0)
