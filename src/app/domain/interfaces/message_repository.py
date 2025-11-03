from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.message import Message


class MessageRepository(ABC):
    """Abstract repository interface for Message entities."""

    @abstractmethod
    async def save(self, message: Message) -> Message:
        """Save a message entity to the repository."""
        pass

    @abstractmethod
    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Retrieve a message entity by its ID."""
        pass

    @abstractmethod
    async def get_by_session_id(self, session_id: UUID) -> List[Message]:
        """Retrieve all messages for a specific session."""
        pass

    @abstractmethod
    async def delete(self, message_id: UUID) -> None:
        """Delete a message entity by its ID."""
        pass

    @abstractmethod
    async def delete_by_session_id(self, session_id: UUID) -> None:
        """Delete all messages for a specific session."""
        pass

    @abstractmethod
    async def count_by_session_id(self, session_id: UUID) -> int:
        """Count the number of messages in a session."""
        pass
