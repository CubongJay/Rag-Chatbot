import os
import sys
from datetime import datetime
from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

src_path = os.path.join(os.path.dirname(__file__), "../../")
if os.path.exists(src_path):
    sys.path.insert(0, os.path.abspath(src_path))
else:
    sys.path.insert(0, os.getcwd())

with patch.dict(
    os.environ,
    {
        "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
        "SECRET_KEY": "test-secret",
        "API_KEY": "test-key",
        "ENCRYPTION_KEY": "tLKcezNbbYKFOZdB_yt1GBwiVLJqz2jQ6JxIURtGSnI=",
        "OPENAI_API_KEY": "test-openai-key",
    },
):
    sys.modules["langchain_core"] = Mock()
    sys.modules["langchain_core.messages"] = Mock()
    sys.modules["langchain_openai"] = Mock()
    sys.modules["langchain_openai.chat_models"] = Mock()

    from app.main import app
    from app.schemas.pagination import PaginatedResponse, PaginationMeta
    from app.schemas.session.responses import (SessionCreateResponse,
                                               SessionResponse)


class TestSessionsAPISimple:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_create_session_success(self, client):
        """Test creating a session with mocked use case."""
        session_id = uuid4()

        mock_session = Mock()
        mock_session.id = session_id
        mock_session.title = "New Chat"
        mock_session.is_favorite = False
        mock_session.created_at = datetime.now()

        with patch(
            "app.usecases.create_session.CreateSessionUseCase.execute"
        ) as mock_execute:
            mock_execute.return_value = mock_session

            response = client.post(
                "/sessions/",
                json={"title": "New Chat", "is_favorite": False},
                headers={"X-API-Key": "test-key"},
            )

            assert response.status_code == 201
            data = response.json()
            assert data["title"] == "New Chat"
            assert "session_id" in data

    def test_get_sessions_success(self, client):
        """Test getting sessions with mocked use case."""
        session_id = uuid4()

        mock_session = Mock()
        mock_session.id = session_id
        mock_session.title = "Chat 1"
        mock_session.is_favorite = False
        mock_session.created_at = datetime.now()
        mock_session.updated_at = datetime.now()

        with (
            patch(
                "app.usecases.get_sessions.GetSessionsUseCase.execute_all"
            ) as mock_execute_all,
            patch(
                "app.usecases.get_sessions.GetSessionsUseCase.execute_count"
            ) as mock_execute_count,
        ):

            mock_execute_all.return_value = [mock_session]
            mock_execute_count.return_value = 1

            response = client.get(
                "/sessions/?page=1&size=10", headers={"X-API-Key": "test-key"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert "pagination" in data

    def test_get_session_success(self, client):
        """Test getting a single session with mocked use case."""
        session_id = uuid4()

        mock_session = SessionResponse(
            id=session_id,
            title="Chat 1",
            is_favorite=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        with patch(
            "app.usecases.get_session.GetSessionUseCase.execute_by_id"
        ) as mock_execute:
            mock_execute.return_value = mock_session

            response = client.get(
                f"/sessions/{session_id}", headers={"X-API-Key": "test-key"}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == str(session_id)

    def test_delete_session_success(self, client):
        """Test deleting a session with mocked use case."""
        session_id = uuid4()

        with patch(
            "app.usecases.delete_session.DeleteSessionUseCase.execute"
        ) as mock_execute:
            mock_execute.return_value = True

            response = client.delete(
                f"/sessions/{session_id}", headers={"X-API-Key": "test-key"}
            )

            assert response.status_code == 204
