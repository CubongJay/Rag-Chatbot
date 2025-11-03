import logging

from app.domain.entities.session import Session
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class CreateSessionUseCase:
    def __init__(self, session_repo: SessionRepository) -> None:
        self.session_repo = session_repo

    async def execute(
        self,
        title: str,
        is_favorite: bool = False,
    ) -> Session:

        new_session = Session(title="", is_favorite=False)
        new_session.set_title(title)
        new_session.set_favorite(is_favorite)

        saved_session = await self.session_repo.save(new_session)
        logger.info(
            f"Session created successfully: ID={saved_session.id}, title='{saved_session.title}'"
        )
        return saved_session
