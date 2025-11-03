import os
import sys
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from app.usecases.create_session import CreateSessionUseCase


class TestCreateSession:
    @pytest.mark.asyncio
    async def test_creates_session_successfully(self):
        session_repo = AsyncMock()
        mock_session = Mock(id=uuid4(), title="New Chat", is_favorite=False)
        session_repo.save.return_value = mock_session

        use_case = CreateSessionUseCase(session_repo)

        result = await use_case.execute(title="New Chat", is_favorite=False)

        session_repo.save.assert_called_once()
        assert result.title == "New Chat"
        assert result.is_favorite is False

    @pytest.mark.asyncio
    async def test_creates_favorite_session(self):
        session_repo = AsyncMock()
        mock_session = Mock(id=uuid4(), title="Important Chat", is_favorite=True)
        session_repo.save.return_value = mock_session

        use_case = CreateSessionUseCase(session_repo)

        result = await use_case.execute(title="Important Chat", is_favorite=True)

        session_repo.save.assert_called_once()
        assert result.title == "Important Chat"
        assert result.is_favorite is True

    @pytest.mark.asyncio
    async def test_creates_session_with_default_values(self):
        session_repo = AsyncMock()
        mock_session = Mock(id=uuid4(), title="Default Chat", is_favorite=False)
        session_repo.save.return_value = mock_session

        use_case = CreateSessionUseCase(session_repo)

        result = await use_case.execute(title="Default Chat")

        session_repo.save.assert_called_once()
        assert result.title == "Default Chat"
        assert result.is_favorite is False
