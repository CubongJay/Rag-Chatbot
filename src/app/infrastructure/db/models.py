import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import get_base

Base = get_base()


class ChatSession(Base):
    __tablename__ = "sessions"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    title = Column(String, index=True)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {"extend_existing": True}
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    session_id = Column(UUID, ForeignKey("sessions.id"))
    sender = Column(String, default="user")
    content = Column(Text)
    message_type = Column(String, default="user")
    timestamp = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    session = relationship("ChatSession", back_populates="messages")
