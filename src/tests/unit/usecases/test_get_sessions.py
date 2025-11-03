import os
import sys
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from app.usecases.get_sessions import GetSessionsUseCase


class TestGetSessions:
    @pytest.mark.asyncio
    async def test_retrieves_all_sessions_with_pagination(self):
        session_repo = AsyncMock()
        mock_sessions = [
            Mock(id=uuid4(), title="Chat 1"),
            Mock(id=uuid4(), title="Chat 2"),
        ]
        session_repo.get_all.return_value = mock_sessions
        session_repo.get_sessions_count.return_value = 2

        use_case = GetSessionsUseCase(session_repo)

        sessions = await use_case.execute_all(page=1, size=10)
        total_count = await use_case.execute_count()

        session_repo.get_all.assert_called_once_with(page=1, size=10)
        session_repo.get_sessions_count.assert_called_once_with(is_favorite=None)
        assert len(sessions) == 2
        assert total_count == 2

    @pytest.mark.asyncio
    async def test_filters_favorite_sessions(self):
        session_repo = AsyncMock()
        favorite_sessions = [Mock(id=uuid4(), title="Favorite Chat")]
        session_repo.get_by_favorite.return_value = favorite_sessions
        session_repo.get_sessions_count.return_value = 1

        use_case = GetSessionsUseCase(session_repo)

        sessions = await use_case.execute_by_favorite(True, page=1, size=5)
        total_count = await use_case.execute_count(is_favorite=True)

        session_repo.get_by_favorite.assert_called_once_with(
            is_favorite=True, page=1, size=5
        )
        session_repo.get_sessions_count.assert_called_once_with(is_favorite=True)
        assert len(sessions) == 1
        assert total_count == 1

    @pytest.mark.asyncio
    async def test_retrieves_sessions_with_default_pagination(self):
        session_repo = AsyncMock()
        mock_sessions = [Mock(id=uuid4(), title="Chat 1")]
        session_repo.get_all.return_value = mock_sessions
        session_repo.get_sessions_count.return_value = 1

        use_case = GetSessionsUseCase(session_repo)

        sessions = await use_case.execute_all()
        total_count = await use_case.execute_count()

        session_repo.get_all.assert_called_once_with(page=None, size=None)
        session_repo.get_sessions_count.assert_called_once_with(is_favorite=None)
        assert len(sessions) == 1
        assert total_count == 1
