import logging
from typing import Optional
from uuid import UUID

from app.domain.entities.message import Message
from app.domain.interfaces.message_repository import MessageRepository
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class GetMessageUseCase:
    """Use case for retrieving a single message by ID."""

    def __init__(
        self, message_repo: MessageRepository, session_repo: SessionRepository
    ) -> None:
        self.message_repo = message_repo
        self.session_repo = session_repo

    async def execute_by_id(self, message_id: UUID) -> Optional[Message]:
        """
        Retrieve a specific message by its ID.

        Args:
            message_id: The ID of the message to retrieve

        Returns:
            The message entity if found, None otherwise
        """
        return await self.message_repo.get_by_id(message_id)
