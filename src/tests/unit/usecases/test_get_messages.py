import os
import sys
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from app.domain.entities.message import MessageType
from app.usecases.get_messages import GetMessagesUseCase


class TestGetMessages:
    @pytest.mark.asyncio
    async def test_retrieves_messages_by_session_with_pagination(self):
        message_repo = AsyncMock()
        session_repo = AsyncMock()
        session_id = uuid4()

        mock_messages = [
            Mock(id=uuid4(), session_id=session_id, sender="user", content="Hello"),
            Mock(
                id=uuid4(),
                session_id=session_id,
                sender="assistant",
                content="Hi there!",
            ),
        ]
        message_repo.get_by_session_id.return_value = mock_messages
        message_repo.count_by_session_id.return_value = 2
        session_repo.get_by_id.return_value = Mock(id=session_id)

        use_case = GetMessagesUseCase(message_repo, session_repo)

        messages = await use_case.execute_by_session_id(session_id, page=1, size=10)
        total_count = await use_case.execute_count_by_session_id(session_id)

        assert session_repo.get_by_id.call_count == 2
        message_repo.get_by_session_id.assert_called_once_with(
            session_id, page=1, size=10
        )
        message_repo.count_by_session_id.assert_called_once_with(session_id)
        assert len(messages) == 2
        assert total_count == 2

    @pytest.mark.asyncio
    async def test_returns_none_when_session_not_found(self):
        message_repo = AsyncMock()
        session_repo = AsyncMock()
        session_id = uuid4()
        session_repo.get_by_id.return_value = None

        use_case = GetMessagesUseCase(message_repo, session_repo)

        result = await use_case.execute_by_session_id(session_id)

        session_repo.get_by_id.assert_called_once_with(str(session_id))
        message_repo.get_by_session_id.assert_not_called()
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_messages_when_session_exists(self):
        message_repo = AsyncMock()
        session_repo = AsyncMock()
        session_id = uuid4()

        message_repo.get_by_session_id.return_value = []
        message_repo.count_by_session_id.return_value = 0
        session_repo.get_by_id.return_value = Mock(id=session_id)

        use_case = GetMessagesUseCase(message_repo, session_repo)

        messages = await use_case.execute_by_session_id(session_id)
        total_count = await use_case.execute_count_by_session_id(session_id)

        assert session_repo.get_by_id.call_count == 2
        message_repo.get_by_session_id.assert_called_once_with(
            session_id, page=None, size=None
        )
        message_repo.count_by_session_id.assert_called_once_with(session_id)
        assert messages == []
        assert total_count == 0

    @pytest.mark.asyncio
    async def test_raises_error_when_session_not_found_for_count(self):
        message_repo = AsyncMock()
        session_repo = AsyncMock()
        session_id = uuid4()
        session_repo.get_by_id.return_value = None

        use_case = GetMessagesUseCase(message_repo, session_repo)

        with pytest.raises(ValueError, match="Session with id .* not found"):
            await use_case.execute_count_by_session_id(session_id)

        session_repo.get_by_id.assert_called_once_with(str(session_id))
        message_repo.count_by_session_id.assert_not_called()
