from typing import Optional

from pydantic import BaseModel, Field


class SessionQueryParams(BaseModel):
    """Schema for session query parameters."""

    is_favorite: Optional[bool] = None
    limit: Optional[int] = Field(default=50, ge=1, le=100)
    offset: Optional[int] = Field(default=0, ge=0)
