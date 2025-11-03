import logging
from typing import Optional
from uuid import UUID

from app.domain.entities.session import Session
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class GetSessionUseCase:
    """Use case for retrieving a single session."""

    def __init__(self, session_repo: SessionRepository) -> None:
        self.session_repo = session_repo

    async def execute_by_id(self, session_id: UUID) -> Optional[Session]:
        """
        Retrieve a specific session by its ID.

        Args:
            session_id: The ID of the session to retrieve

        Returns:
            The session entity if found, None otherwise
        """

        try:
            session = await self.session_repo.get_by_id(session_id)
            if not session:
                logger.warning(f"Session with id {session_id} not found")
            return session
        except Exception as e:
            logger.error(f"Error retrieving session {session_id}: {e}")
            return None
