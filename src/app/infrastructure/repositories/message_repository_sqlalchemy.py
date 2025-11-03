from typing import List, Optional
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.message import Message, MessageType
from app.domain.interfaces.message_repository import MessageRepository
from app.infrastructure.db.models import Message as MessageModel
from app.infrastructure.encryption.encryption_service import EncryptionService


class DbMessageRepository(MessageRepository):
    """SQLAlchemy implementation of MessageRepository."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.encryption_service = EncryptionService()

    async def save(self, message: Message) -> Message:
        """Save a message entity to the database."""
        encrypted_content = self.encryption_service.encrypt(message.content)
        db_message = MessageModel(
            session_id=message.session_id,
            sender=message.sender,
            content=encrypted_content,
            message_type=message.message_type.value,
            timestamp=message.timestamp,
        )

        self.db_session.add(db_message)
        await self.db_session.commit()
        await self.db_session.refresh(db_message)

        return self._to_domain_entity(db_message)

    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Retrieve a message entity by its ID."""
        result = await self.db_session.execute(
            select(MessageModel).where(MessageModel.id == message_id)
        )
        db_message = result.scalar_one_or_none()

        if not db_message:
            return None

        return self._to_domain_entity(db_message)

    async def get_by_session_id(
        self, session_id: UUID, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Message]:
        """Retrieve all messages for a specific session with optional pagination."""

        query = (
            select(MessageModel)
            .where(MessageModel.session_id == session_id)
            .order_by(MessageModel.timestamp.asc())
        )

        if page and size:
            offset = (page - 1) * size
            query = query.offset(offset).limit(size)

        result = await self.db_session.execute(query)
        db_messages = result.scalars().all()

        return [self._to_domain_entity(msg) for msg in db_messages]

    async def delete(self, message_id: UUID) -> None:
        """Delete a message entity by its ID."""
        result = await self.db_session.execute(
            select(MessageModel).where(MessageModel.id == message_id)
        )
        db_message = result.scalar_one_or_none()

        if db_message:
            await self.db_session.delete(db_message)
            await self.db_session.commit()

    async def delete_by_session_id(self, session_id: UUID) -> None:
        """Delete all messages for a specific session."""
        await self.db_session.execute(
            delete(MessageModel).where(MessageModel.session_id == session_id)
        )
        await self.db_session.commit()

    async def count_by_session_id(self, session_id: UUID) -> int:
        """Count the number of messages in a session."""
        result = await self.db_session.execute(
            select(MessageModel).where(MessageModel.session_id == session_id)
        )
        return len(result.scalars().all())

    def _to_domain_entity(self, db_message: MessageModel) -> Message:
        """Convert database model to domain entity."""
        decrypted_content = self.encryption_service.decrypt(db_message.content)
        return Message(
            session_id=db_message.session_id,
            sender=db_message.sender,
            content=decrypted_content,
            id=db_message.id,
            message_type=MessageType(db_message.message_type),
            timestamp=db_message.timestamp,
            created_at=db_message.created_at,
            updated_at=db_message.updated_at,
        )
