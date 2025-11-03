import logging
from typing import List, Optional
from uuid import UUID

from app.domain.entities.message import Message
from app.domain.interfaces.message_repository import MessageRepository
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class GetMessagesUseCase:
    """Use case for retrieving messages from a chat session."""

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
        return self.message_repo.get_by_id(message_id)

    async def execute_by_session_id(
        self, session_id: UUID, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Message]:
        """
        Retrieve all messages for a specific session with optional pagination.

        Args:
            session_id: The ID of the session to retrieve messages from
            page: Optional page number for pagination
            size: Optional page size for pagination

        Returns:
            List of message entities for the session

        """

        session = await self.session_repo.get_by_id(str(session_id))
        if not session:
            logger.warning(f"Session with id {session_id} not found")
            return None
        return await self.message_repo.get_by_session_id(
            session_id, page=page, size=size
        )

    async def execute_count_by_session_id(self, session_id: UUID) -> int:
        """
        Count the number of messages in a session.

        Args:
            session_id: The ID of the session to count messages for

        Returns:
            Number of messages in the session

        Raises:
            ValueError: If the session doesn't exist
        """

        session = await self.session_repo.get_by_id(str(session_id))
        if not session:
            logger.warning(f"Session with id {session_id} not found")
            return 0

        return await self.message_repo.count_by_session_id(session_id)
