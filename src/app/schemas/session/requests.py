from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SessionCreate(BaseModel):
    """Schema for creating a new session."""

    title: str = Field(..., min_length=1, max_length=200)
    is_favorite: Optional[bool] = Field(default=False)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()


class SessionUpdate(BaseModel):
    """Schema for updating a session."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    is_favorite: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v
