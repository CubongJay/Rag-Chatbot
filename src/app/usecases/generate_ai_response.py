import logging
from uuid import UUID

from langchain_openai import OpenAIEmbeddings

from app.config.settings import get_settings
from app.domain.entities.message import Message, MessageType
from app.domain.interfaces.llm_service import LLMService
from app.domain.interfaces.message_repository import MessageRepository
from app.domain.interfaces.session_repository import SessionRepository
from app.domain.interfaces.vector_repository import VectorRepository

logger = logging.getLogger(__name__)

settings = get_settings()


class GenerateAIResponseUseCase:
    """Use case for generating AI responses to user messages."""

    def __init__(
        self,
        message_repo: MessageRepository,
        session_repo: SessionRepository,
        llm_service: LLMService,
        vector_repo: VectorRepository,
    ) -> None:
        self.message_repo = message_repo
        self.session_repo = session_repo
        self.llm_service = llm_service
        self.vector_repo = vector_repo

    async def execute(
        self, session_id: UUID, user_message_content: str
    ) -> Message:
        """
        Generate an AI response to a user message.

        Args:
            session_id: The session ID
            user_message_content: The user's message content

        Returns:
            The AI assistant's response message (or fallback message if LLM fails)
        """
        session = await self.session_repo.get_by_id(session_id)
        if not session:
            logger.warning(f"Session with id {session_id} not found")
            return None

        try:

            history_messages = await self.message_repo.get_by_session_id(
                session_id
            )
            conversation_history = [
                {
                    "role": (
                        "assistant"
                        if msg.message_type == MessageType.ASSISTANT
                        else "user"
                    ),
                    "content": msg.content,
                }
                for msg in history_messages[-10:]
            ]
            open_ai_embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=settings.openai_api_key,
            )

            embedded_message = open_ai_embeddings.embed_query(
                user_message_content
            )

            retrieved_docs = self.vector_repo.query_relevant_chunks(
                embedded_text=embedded_message,
                top_k=3,
            )
            # retrieved_docs could return e.g. ["doc1 content...", "doc2 content..."]
            combined_context = "\n\n".join(retrieved_docs)
            ai_response_content = self.llm_service.generate_response(
                user_message_content,
                conversation_history,
                context=combined_context,
            )

            ai_message = Message(session_id=session_id)
            ai_message.set_sender("assistant")
            ai_message.set_content(ai_response_content)
            ai_message.set_message_type(MessageType.ASSISTANT)

        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}", exc_info=True)

            # ai_message = Message(session_id=session_id)
            # ai_message.set_sender("assistant")
            # ai_message.set_content(
            #     "I apologize, but I'm having trouble generating a response right now. Please try again."
            # )
            # ai_message.set_message_type(MessageType.ASSISTANT)
            return None

        saved_ai_message = await self.message_repo.save(ai_message)
        return saved_ai_message
