from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Session:
    title: str
    is_favorite: bool
    id: Optional[UUID] = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)

    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if self.id is None:
            self.id = uuid4()
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc)

    @property
    def session_id(self) -> UUID:
        """Get the session ID."""
        return self.id

    def set_title(self, title: str) -> None:
        """Set the session title and update timestamp."""
        self.title = title
        self.updated_at = datetime.now(timezone.utc)

    def set_favorite(self, is_favorite: bool) -> None:
        """Set the favorite status and update timestamp."""
        self.is_favorite = is_favorite
        self.updated_at = datetime.now(timezone.utc)
