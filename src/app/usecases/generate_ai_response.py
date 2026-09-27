import logging
from uuid import UUID

from langfuse import get_client
from langfuse.langchain import CallbackHandler

from app.config.settings import get_settings
from app.domain.entities.message import Message, MessageType
from app.domain.interfaces.llm_service import LLMService
from app.domain.interfaces.message_repository import MessageRepository
from app.domain.interfaces.session_repository import SessionRepository
from app.domain.interfaces.document_chunk_repository import DocumentChunkRepository

logger = logging.getLogger(__name__)

settings = get_settings()


class GenerateAIResponseUseCase:
    """Use case for generating AI responses to user messages."""

    def __init__(
        self,
        message_repo: MessageRepository,
        session_repo: SessionRepository,
        llm_service: LLMService,
        document_repo: DocumentChunkRepository,
   

    ) -> None:
        self.message_repo = message_repo
        self.session_repo = session_repo
        self.llm_service = llm_service
   
        self.document_repo = document_repo
        self.langfuse = get_client()
        self.langfuse_handler = CallbackHandler()

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
        
            embedded_message = await self.llm_service.embed_query(
                user_message_content
            )


            with self.langfuse.start_as_current_observation(
                name="retrieve_chunks",
                input=user_message_content,
                as_type="retriever",
            ) as span:
                retrieved_docs = await self.document_repo.retrieve_similar_chunks(
                    session_id=session_id,
                    query_embedding=embedded_message,
                    k=3,
                )
                span.update(
                    output=[c.content for c in retrieved_docs],
                    metadata={"chunks_found": len(retrieved_docs)},
                )

            combined_context =  "\n\n".join(c.content for c in retrieved_docs)
            ai_response_content = await self.llm_service.generate_response(
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

            return None

        saved_ai_message = await self.message_repo.save(ai_message)
        return saved_ai_message
