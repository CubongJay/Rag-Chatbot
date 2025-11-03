from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4


class MessageType(Enum):
    """Enum representing the type of message."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """Domain entity representing a chat message."""

    session_id: UUID = field()
    sender: str = field(default="user")
    content: str = field(default="")
    id: Optional[UUID] = field(default=None)
    message_type: MessageType = field(default=MessageType.USER)
    timestamp: Optional[int] = field(default=None)
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)

    def __post_init__(self):
        """Initialize default values after dataclass creation."""
        if self.id is None:
            self.id = uuid4()
        if self.timestamp is None:
            self.timestamp = int(datetime.now(timezone.utc).timestamp())
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        if self.updated_at is None:
            self.updated_at = datetime.now(timezone.utc)

    def set_content(self, content: str) -> None:
        """Update the message content and timestamp."""
        self.content = content
        self.updated_at = datetime.now(timezone.utc)
        self.timestamp = int(datetime.now(timezone.utc).timestamp())

    def set_sender(self, sender: str) -> None:
        """Set the message sender."""
        self.sender = sender

    def set_message_type(self, message_type: MessageType) -> None:
        """Set the message type."""
        self.message_type = message_type

    def is_user_message(self) -> bool:
        """Check if this is a user message."""
        return self.message_type == MessageType.USER

    def is_assistant_message(self) -> bool:
        """Check if this is an assistant message."""
        return self.message_type == MessageType.ASSISTANT
