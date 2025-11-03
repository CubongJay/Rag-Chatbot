from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class SessionResponse(BaseModel):
    """Schema for session response."""

    id: UUID
    title: str
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionCreateResponse(BaseModel):
    """Schema for session creation response."""

    session_id: UUID
    title: str
    is_favorite: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SessionListResponse(BaseModel):
    """Schema for listing sessions."""

    sessions: List[SessionResponse]
    total_count: int
