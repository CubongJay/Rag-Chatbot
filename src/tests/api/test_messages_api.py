import os
import sys
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

# Add the src directory to Python path
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

    from app.domain.entities.message import Message, MessageType
    from app.main import app
    from app.schemas.message.responses import (MessagePairResponse,
                                               MessageResponse)
    from app.schemas.pagination import PaginatedResponse


class TestMessagesAPISimple:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_create_message_success(self, client):
        session_id = uuid4()
        message_id = uuid4()

        mock_user_message = Mock(spec=Message)
        mock_user_message.id = message_id
        mock_user_message.session_id = session_id
        mock_user_message.sender = "user"
        mock_user_message.content = "Hello"
        mock_user_message.message_type = MessageType.USER
        mock_user_message.timestamp = int(datetime.now().timestamp())
        mock_user_message.created_at = datetime.now()
        mock_user_message.updated_at = datetime.now()

        mock_ai_message = Mock(spec=Message)
        mock_ai_message.id = uuid4()
        mock_ai_message.session_id = session_id
        mock_ai_message.sender = "assistant"
        mock_ai_message.content = "Hi there!"
        mock_ai_message.message_type = MessageType.ASSISTANT
        mock_ai_message.timestamp = int(datetime.now().timestamp())
        mock_ai_message.created_at = datetime.now()
        mock_ai_message.updated_at = datetime.now()

        with (
            patch(
                "app.usecases.create_message.CreateMessageUseCase.execute",
                new_callable=AsyncMock,
            ) as mock_create,
            patch(
                "app.usecases.generate_ai_response.GenerateAIResponseUseCase.execute",
                new_callable=AsyncMock,
            ) as mock_ai,
        ):

            mock_create.return_value = mock_user_message
            mock_ai.return_value = mock_ai_message

            response = client.post(
                f"/sessions/{session_id}/messages/",
                json={"content": "Hello", "sender": "user", "message_type": "user"},
                headers={"X-API-Key": "test-key"},
            )

            assert response.status_code == 201
            data = response.json()
            assert "user_message" in data
            assert "assistant_message" in data
            assert data["user_message"]["content"] == "Hello"
            assert data["assistant_message"]["content"] == "Hi there!"

    def test_get_messages_success(self, client):
        session_id = uuid4()
        message_id = uuid4()

        mock_message = Mock(spec=Message)
        mock_message.id = message_id
        mock_message.session_id = session_id
        mock_message.sender = "user"
        mock_message.content = "Hello"
        mock_message.message_type = MessageType.USER
        mock_message.timestamp = int(datetime.now().timestamp())
        mock_message.created_at = datetime.now()
        mock_message.updated_at = datetime.now()

        with (
            patch(
                "app.usecases.get_messages.GetMessagesUseCase.execute_by_session_id",
                new_callable=AsyncMock,
            ) as mock_get,
            patch(
                "app.usecases.get_messages.GetMessagesUseCase.execute_count_by_session_id",
                new_callable=AsyncMock,
            ) as mock_count,
        ):

            mock_get.return_value = [mock_message]
            mock_count.return_value = 1

            response = client.get(
                f"/sessions/{session_id}/messages/?page=1&size=10",
                headers={"X-API-Key": "test-key"},
            )

            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert "pagination" in data
            assert len(data["items"]) == 1
            assert data["items"][0]["id"] == str(message_id)

    def test_get_message_success(self, client):
        session_id = uuid4()
        message_id = uuid4()

        mock_message = Mock(spec=Message)
        mock_message.id = message_id
        mock_message.session_id = session_id
        mock_message.sender = "user"
        mock_message.content = "Hello"
        mock_message.message_type = MessageType.USER
        mock_message.timestamp = int(datetime.now().timestamp())
        mock_message.created_at = datetime.now()
        mock_message.updated_at = datetime.now()

        with patch(
            "app.usecases.get_message.GetMessageUseCase.execute_by_id",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = mock_message

            response = client.get(
                f"/sessions/{session_id}/messages/{message_id}/",
                headers={"X-API-Key": "test-key"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == str(message_id)
            assert data["content"] == "Hello"

    def test_get_message_not_found(self, client):
        session_id = uuid4()
        message_id = uuid4()

        with patch(
            "app.usecases.get_message.GetMessageUseCase.execute_by_id",
            new_callable=AsyncMock,
        ) as mock_get:
            mock_get.return_value = None

            response = client.get(
                f"/sessions/{session_id}/messages/{message_id}/",
                headers={"X-API-Key": "test-key"},
            )

            assert response.status_code == 404

    def test_delete_message_success(self, client):
        session_id = uuid4()
        message_id = uuid4()

        with patch(
            "app.usecases.delete_message.DeleteMessageUseCase.execute_by_id",
            new_callable=AsyncMock,
        ) as mock_delete:
            mock_delete.return_value = True

            response = client.delete(
                f"/sessions/{session_id}/messages/{message_id}/",
                headers={"X-API-Key": "test-key"},
            )

            assert response.status_code == 204

    def test_delete_message_not_found(self, client):
        session_id = uuid4()
        message_id = uuid4()

        with patch(
            "app.usecases.delete_message.DeleteMessageUseCase.execute_by_id",
            new_callable=AsyncMock,
        ) as mock_delete:
            mock_delete.return_value = False

            response = client.delete(
                f"/sessions/{session_id}/messages/{message_id}/",
                headers={"X-API-Key": "test-key"},
            )

            assert response.status_code == 204
