import logging
from uuid import UUID

from app.domain.interfaces.message_repository import MessageRepository
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class DeleteMessageUseCase:
    """Use case for deleting messages from a chat session."""

    def __init__(
        self, message_repo: MessageRepository, session_repo: SessionRepository
    ) -> None:
        self.message_repo = message_repo
        self.session_repo = session_repo

    async def execute_by_id(self, message_id: UUID) -> bool:
        """
        Delete a specific message by its ID.

        Args:
            message_id: The ID of the message to delete

        Returns:
            True if the message was deleted, False if it didn't exist
        """
        message = await self.message_repo.get_by_id(message_id)
        if not message:
            logger.warning(f"Message with id {message_id} not found")
            return False

        await self.message_repo.delete(message_id)
        logger.info(f"Message deleted successfully: ID={message_id}")
        return True

    async def execute_by_session_id(self, session_id: UUID) -> int:
        """
        Delete all messages for a specific session.

        Args:
            session_id: The ID of the session to delete messages from

        Returns:
            Number of messages that were deleted
        """
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            logger.warning(f"Session with id {session_id} not found")
            return 0

        message_count = await self.message_repo.count_by_session_id(session_id)
        await self.message_repo.delete_by_session_id(session_id)

        logger.info(f"Deleted {message_count} messages from session: ID={session_id}")
        return message_count
