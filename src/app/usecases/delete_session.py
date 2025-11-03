import logging
from uuid import UUID

from app.domain.interfaces.message_repository import MessageRepository
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class DeleteSessionUseCase:
    """Use case for deleting sessions and their associated messages."""

    def __init__(
        self, session_repo: SessionRepository, message_repo: MessageRepository
    ) -> None:
        self.session_repo = session_repo
        self.message_repo = message_repo

    async def execute(self, session_id: UUID) -> None:
        """
        Delete a session and all its associated messages.

        Args:
            session_id: The ID of the session to delete

        Returns:
            True if the session was deleted successfully

        Raises:
            ValueError: If the session doesn't exist
        """

        session = await self.session_repo.get_by_id(session_id)
        if not session:
            logger.warning(f"Session with id {session_id} not found")
            return False

        try:
            logger.info(f"Deleting messages for session: ID={session_id}")
            await self.message_repo.delete_by_session_id(session_id)
            logger.info(f"Messages deleted for session: ID={session_id}")

            logger.info(f"Deleting session: ID={session_id}")
            await self.session_repo.delete(session_id)
            logger.info(f"Session deleted successfully: ID={session_id}")
            return True
        except Exception:
            logger.error(f"Error deleting session {session_id}")
            raise
