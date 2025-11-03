from abc import ABC, abstractmethod


class LLMService(ABC):
    """Abstract interface for LLM service."""

    @abstractmethod
    def generate_response(self, message: str, conversation_history: list = None) -> str:
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
