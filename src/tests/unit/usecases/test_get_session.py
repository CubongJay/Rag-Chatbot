import os
import sys
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from app.usecases.get_session import GetSessionUseCase


class TestGetSession:
    @pytest.mark.asyncio
    async def test_retrieves_session_by_id_successfully(self):
        session_repo = AsyncMock()
        session_id = uuid4()
        mock_session = Mock(id=session_id, title="Test Chat", is_favorite=False)
        session_repo.get_by_id.return_value = mock_session

        use_case = GetSessionUseCase(session_repo)

        result = await use_case.execute_by_id(session_id)

        session_repo.get_by_id.assert_called_once_with(session_id)
        assert result.id == session_id
        assert result.title == "Test Chat"

    @pytest.mark.asyncio
    async def test_returns_none_when_session_not_found(self):
        session_repo = AsyncMock()
        session_id = uuid4()
        session_repo.get_by_id.return_value = None

        use_case = GetSessionUseCase(session_repo)

        result = await use_case.execute_by_id(session_id)

        session_repo.get_by_id.assert_called_once_with(session_id)
        assert result is None

    @pytest.mark.asyncio
    async def test_handles_repository_error_gracefully(self):
        session_repo = AsyncMock()
        session_id = uuid4()
        session_repo.get_by_id.side_effect = Exception("Database error")

        use_case = GetSessionUseCase(session_repo)

        result = await use_case.execute_by_id(session_id)

        session_repo.get_by_id.assert_called_once_with(session_id)
        assert result is None
