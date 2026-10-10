from abc import ABC, abstractmethod
from typing import List


class LLMService(ABC):
    """Abstract interface for LLM service."""

    @abstractmethod
    async def generate_response(self, message: str, conversation_history: list = None) -> str:
        """
        Generate a response from the LLM based on user input.

        Args:
            message: The user's message
            conversation_history: Optional list of previous messages for context

        Returns:
            The generated response from the LLM

        Raises:
            ExternalServiceError: If the LLM service fails
        """
        pass

    @abstractmethod
    async def embed_query(self, text: str) -> List[float]:
            """Generate an embedding for a single query (async)."""
            pass

    @abstractmethod
    async def classify_query(self, user_message: str) -> str:
         """ Classify the user's message.

             Returns:
                "document" — the message asks about facts, topics, or content that may be in an uploaded document.
                "conversational" — the message is a greeting, acknowledgment, meta-question, or doesn't need retrieval. """
         pass

    @abstractmethod
    async def summarize_document(self, content: str) -> str:
         """
            Gets a brief summary of the entire document being uploaded.
         """
         pass
    