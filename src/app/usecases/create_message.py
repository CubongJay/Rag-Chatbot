import logging
from uuid import UUID

from app.domain.entities.message import Message, MessageType
from app.domain.interfaces.message_repository import MessageRepository
from app.domain.interfaces.session_repository import SessionRepository

logger = logging.getLogger(__name__)


class CreateMessageUseCase:
    """Use case for creating a new message in a chat session."""

    def __init__(
        self, message_repo: MessageRepository, session_repo: SessionRepository
    ) -> None:
        self.message_repo = message_repo
        self.session_repo = session_repo

    async def execute(
        self,
        session_id: UUID,
        content: str,
        sender: str = "user",
        message_type: MessageType = MessageType.USER,
    ) -> Message:
        """
        Create a new message in the specified session.

        Args:
            session_id: The ID of the session to add the message to
            content: The content of the message
            sender: The sender of the message (default: "user")
            message_type: The type of message (default: USER)

        Returns:
            The created message entity


        """

        session = await self.session_repo.get_by_id(session_id)
        if not session:
            logger.warning(f"Session with id {session_id} not found")
            return None

        message = Message(session_id=session_id)
        message.set_content(content.strip())
        message.set_sender(sender)
        message.set_message_type(message_type)

        saved_message = await self.message_repo.save(message)
        logger.info(
            f"Message created successfully: ID={saved_message.id}, session_id={saved_message.session_id}, sender={saved_message.sender}, content='{saved_message.content}'"
        )
        return saved_message
