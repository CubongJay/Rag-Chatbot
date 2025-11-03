from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.session import Session


class SessionRepository(ABC):
    @abstractmethod
    async def save(self, session: Session) -> Session:
        """Save a session entity to the repository."""
        pass

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> Optional[Session]:
        """Retrieve a session entity by its ID."""
        pass

    @abstractmethod
    async def get_all(
        self, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Session]:
        """Retrieve all session entities."""
        pass

    @abstractmethod
    async def get_by_favorite(
        self, is_favorite: bool, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Session]:
        """Retrieve sessions filtered by favorite status."""
        pass

    @abstractmethod
    async def update(
        self,
        session_id: UUID,
        title: Optional[str] = None,
        is_favorite: Optional[bool] = None,
    ) -> Session:
        """Update an existing session entity."""
        pass

    @abstractmethod
    async def delete(self, session_id: UUID) -> None:
        """Delete a session entity by its ID."""
        pass
