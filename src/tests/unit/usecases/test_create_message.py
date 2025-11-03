import os
import sys
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from app.domain.entities.message import MessageType
from app.usecases.create_message import CreateMessageUseCase


class TestCreateMessage:
    @pytest.mark.asyncio
    async def test_creates_user_message_successfully(self):
        message_repo = AsyncMock()
        session_repo = AsyncMock()
        session_id = uuid4()

        session_repo.get_by_id.return_value = Mock(id=session_id)
        mock_saved_message = Mock()
        mock_saved_message.session_id = session_id
        mock_saved_message.sender = "user"
        mock_saved_message.content = "What's the weather like?"
        mock_saved_message.message_type = MessageType.USER
        message_repo.save.return_value = mock_saved_message

        use_case = CreateMessageUseCase(message_repo, session_repo)

        result = await use_case.execute(
            session_id=session_id,
            content="What's the weather like?",
            sender="user",
            message_type=MessageType.USER,
        )

        session_repo.get_by_id.assert_called_once_with(session_id)
        message_repo.save.assert_called_once()
        assert result.session_id == session_id
        assert result.sender == "user"
        assert result.content == "What's the weather like?"

    @pytest.mark.asyncio
    async def test_returns_none_when_session_not_found(self):
        message_repo = AsyncMock()
        session_repo = AsyncMock()
        session_repo.get_by_id.return_value = None

        use_case = CreateMessageUseCase(message_repo, session_repo)

        result = await use_case.execute(
            session_id=uuid4(),
            content="Hello",
            sender="user",
            message_type=MessageType.USER,
        )

        session_repo.get_by_id.assert_called_once()
        message_repo.save.assert_not_called()
        assert result is None

    @pytest.mark.asyncio
    async def test_creates_assistant_message_successfully(self):
        message_repo = AsyncMock()
        session_repo = AsyncMock()
        session_id = uuid4()

        session_repo.get_by_id.return_value = Mock(id=session_id)
        mock_saved_message = Mock()
        mock_saved_message.session_id = session_id
        mock_saved_message.sender = "assistant"
        mock_saved_message.content = "Hello! How can I help you?"
        mock_saved_message.message_type = MessageType.ASSISTANT
        message_repo.save.return_value = mock_saved_message

        use_case = CreateMessageUseCase(message_repo, session_repo)

        result = await use_case.execute(
            session_id=session_id,
            content="Hello! How can I help you?",
            sender="assistant",
            message_type=MessageType.ASSISTANT,
        )

        session_repo.get_by_id.assert_called_once_with(session_id)
        message_repo.save.assert_called_once()
        assert result.session_id == session_id
        assert result.sender == "assistant"
        assert result.message_type == MessageType.ASSISTANT
