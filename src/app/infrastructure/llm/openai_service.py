from typing import List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config.settings import get_settings
from app.domain.interfaces.llm_service import LLMService
from app.errors.errors import ExternalServiceError


class OpenAIService(LLMService):
    """OpenAI implementation of LLM service using LangChain."""

    def __init__(self):
        """Initialize the OpenAI service with settings."""
        settings = get_settings()

        if not settings.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set in environment variables"
            )

        try:
            self.llm = ChatOpenAI(
                api_key=settings.openai_api_key,
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
            )
        except Exception as e:
            raise ExternalServiceError(
                "OpenAI", f"Failed to initialize: {str(e)}"
            )

    def generate_response(
        self,
        message: str,
        conversation_history: Optional[List] = None,
        context: Optional[str] = None,
    ) -> str:
        """
        Generate a response from OpenAI based on user input.

        Args:
            message: The user's message
            conversation_history: Optional list of previous messages

        Returns:
            The generated response from OpenAI

        Raises:
            ExternalServiceError: If OpenAI API fails
        """
        try:
            messages = [
                SystemMessage(content="You are a helpful AI assistant.")
            ]

            if context:
                messages.append(
                    SystemMessage(content=f"Use this context: {context}")
                )

            if conversation_history:
                for msg in conversation_history:
                    if msg.get("role") == "user":
                        messages.append(
                            HumanMessage(content=msg.get("content", ""))
                        )
                    elif msg.get("role") == "assistant":
                        messages.append(
                            AIMessage(content=msg.get("content", ""))
                        )

            messages.append(HumanMessage(content=message))

            response = self.llm.invoke(messages)
            return response.content.strip()

        except Exception as e:
            raise ExternalServiceError(
                "OpenAI", f"Failed to generate response: {str(e)}"
            )
