import logging
from typing import Optional
from uuid import UUID

from app.domain.entities.session import Session
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class UpdateSessionUseCase:
    """Use case for updating session properties."""

    def __init__(self, session_repo: SessionRepository) -> None:
        self.session_repo = session_repo

    async def execute(
        self,
        session_id: UUID,
        title: Optional[str] = None,
        is_favorite: Optional[bool] = None,
    ) -> Optional[Session]:
        """
        Update session properties (title and/or favorite status)
        """

        session = await self.session_repo.get_by_id(session_id)
        if not session:
            logger.warning(f"Session with id {session_id} not found")
            return None

        if title is not None:
            session.set_title(title)

        if is_favorite is not None:
            session.set_favorite(is_favorite)

        updated_session = await self.session_repo.update(
            session_id=session_id, title=title, is_favorite=is_favorite
        )
        logger.info(f"Session updated successfully: ID={session_id}'")
        return updated_session
