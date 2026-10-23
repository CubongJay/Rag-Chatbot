from typing import List, Optional

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langfuse.langchain import CallbackHandler

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
        self.langfuse_handler = CallbackHandler()

        try:

            self.llm = AzureAIChatCompletionsModel(
                endpoint=settings.azure_inference_url,
                credential=settings.azure_inference_credential,
                model="gpt-4.1-mini",
            )
        except Exception as e:
            raise ExternalServiceError(
                "OpenAI", f"Failed to initialize: {str(e)}"
            )

        try:
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=settings.openai_api_key,
            )

        except Exception as e:
            raise ExternalServiceError(
                "OpenAI", f"Failed to initialize: {str(e)}"
            )

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts (async)."""
        return await self.embeddings.aembed_documents(texts)

    async def embed_query(self, text: str) -> List[float]:
        """Generate an embedding for a single query (async)."""
        return await self.embeddings.aembed_query(text)

    async def generate_response(
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
                    SystemMessage(
                        content=(
                            "Answer the user's question using ONLY the following context. "
                            "If the answer is not in the context, say you don't know.\n\n"
                            f"Context:\n{context}"
                        )
                    )
                )

            else:
                messages.append(
                    SystemMessage(
                        content=(
                            "You are a helpful assistant. Respond to the user's message "
                            "using the conversation history for context. Do not claim to have "
                            "information from documents you have not been given."
                        )
                    )
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

            response = await self.llm.ainvoke(
                messages, config={"callbacks": [self.langfuse_handler]}
            )
            return response.content.strip()

        except Exception as e:
            raise ExternalServiceError(
                "OpenAI", f"Failed to generate response: {str(e)}"
            )

    async def classify_query(self, user_message: str) -> str:
        try:
            messages = [
                SystemMessage(
                    content=(
                        "You are a classifier. Categorize the user's message into one of two categories:\n\n"
                        "- 'document': the message asks about facts, topics, or content that might be in an uploaded document. "
                        "Examples: 'What is X?', 'How many Y?', 'Explain Z.'\n"
                        "- 'conversational': greetings, thanks, meta-questions about the conversation, or anything that doesn't need document lookup. "
                        "Examples: 'Hello', 'Thanks', 'What did you just say?'\n\n"
                        "Respond with exactly one word: 'document' or 'conversational'."
                    )
                ),
                HumanMessage(content=user_message),
            ]

            response = await self.llm.ainvoke(
                messages,
                config={"callbacks": [self.langfuse_handler]},
            )

            result = response.content.strip().lower()
            if "document" in result:
                return "document"
            return "conversational"

        except Exception as e:
            raise ExternalServiceError(
                "OpenAI", f"Failed to classify query: {str(e)}"
            )

    async def summarize_document(self, document_content: str) -> str:
        try:
            messages = [
                SystemMessage(
                    content=(
                        "You are a helpful assistant. "
                        "Summarize the document content into 2-4 sentences "
                        "that accurately describe what the document is about. "
                        "Include key entities such as names, dates, amounts, "
                        "and topics covered."
                    )
                ),
                HumanMessage(content=document_content),
            ]

            response = await self.llm.ainvoke(
                messages,
                config={"callbacks": [self.langfuse_handler]},
            )
            return response.content.strip()

        except Exception as e:
            raise ExternalServiceError(
                "OpenAI", f"Failed to summarize the document: {str(e)}"
            )
