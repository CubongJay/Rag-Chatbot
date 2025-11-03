from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.session import Session
from app.domain.interfaces.session_repository import SessionRepository
from app.infrastructure.db.models import ChatSession


class DbSessionRepository(SessionRepository):
    """A SQLAlchemy implementation of the SessionRepository interface."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(self, session: Session) -> Session:
        """Save a chat session to the database."""
        db_session = ChatSession(
            title=session.title,
            is_favorite=session.is_favorite,
        )
        self.db_session.add(db_session)
        await self.db_session.commit()
        await self.db_session.refresh(db_session)

        session.id = db_session.id
        return session

    async def get_by_id(self, session_id: UUID) -> Optional[Session]:
        """Retrieve a chat session by its ID."""

        result = await self.db_session.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        db_session = result.scalar_one_or_none()
        if not db_session:
            return None
        return self._to_domain_entity(db_session)

    async def get_all(
        self, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Session]:
        """Retrieve all chat sessions with optional pagination."""
        query = select(ChatSession).order_by(ChatSession.created_at.desc())

        if page and size:
            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

        result = await self.db_session.execute(query)
        db_sessions = result.scalars().all()

        return [self._to_domain_entity(session) for session in db_sessions]

    async def get_by_favorite(
        self, is_favorite: bool, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Session]:
        """Retrieve sessions filtered by favorite status."""

        query = (
            select(ChatSession)
            .where(ChatSession.is_favorite == is_favorite)
            .order_by(ChatSession.created_at.desc())
        )
        if page is not None and size is not None:
            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

        result = await self.db_session.execute(query)
        db_sessions = result.scalars().all()

        return [self._to_domain_entity(session) for session in db_sessions]

    async def update(
        self,
        session_id: UUID,
        title: Optional[str] = None,
        is_favorite: Optional[bool] = None,
    ) -> Optional[Session]:
        """Update an existing session entity."""
        result = await self.db_session.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        db_session = result.scalar_one_or_none()
        if not db_session:
            return None
        if title is not None:
            db_session.title = title
        if is_favorite is not None:
            db_session.is_favorite = is_favorite
        db_session.updated_at = datetime.utcnow()
        await self.db_session.commit()
        await self.db_session.refresh(db_session)

        return self._to_domain_entity(db_session)

    async def delete(self, session_id: UUID) -> None:
        """Delete a chat session by its ID."""
        result = await self.db_session.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        db_session = result.scalar_one_or_none()

        if db_session:
            await self.db_session.delete(db_session)
            await self.db_session.commit()

    async def get_sessions_count(self, is_favorite: Optional[bool] = None) -> int:
        """Get total count of sessions."""
        query = select(ChatSession)
        if is_favorite:
            query = query.where(ChatSession.is_favorite == is_favorite)

        result = await self.db_session.execute(query)
        return len(result.scalars().all())

    def _to_domain_entity(self, db_session: ChatSession) -> Session:
        """Convert database model to domain entity."""
        return Session(
            id=db_session.id,
            title=db_session.title,
            is_favorite=db_session.is_favorite,
        )
