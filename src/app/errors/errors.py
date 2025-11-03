import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException
from starlette import status

logger = logging.getLogger(__name__)


class BaseAPIException(HTTPException):
    """Base exception for API errors with enhanced details."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.context = context or {}

        logger.error(
            f"API Error {error_code}: {detail}",
            extra={
                "status_code": status_code,
                "error_code": error_code,
                "context": context,
            },
        )


class ValidationError(BaseAPIException):
    """Validation error with detailed field information."""

    def __init__(self, detail: str, field_errors: Optional[Dict[str, str]] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR",
            context={"field_errors": field_errors or {}},
        )


class SessionNotFoundError(BaseAPIException):
    """Session not found error."""

    def __init__(self, session_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found",
            error_code="SESSION_NOT_FOUND",
            context={"session_id": session_id},
        )


class MessageNotFoundError(BaseAPIException):
    """Message not found error."""

    def __init__(self, message_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Message with ID {message_id} not found",
            error_code="MESSAGE_NOT_FOUND",
            context={"message_id": message_id},
        )


class ExternalServiceError(BaseAPIException):
    """External service error (e.g., OpenAI API)."""

    def __init__(self, service: str, detail: str):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"External service error ({service}): {detail}",
            error_code="EXTERNAL_SERVICE_ERROR",
            context={"service": service},
        )


class RateLimitError(BaseAPIException):
    """Rate limit exceeded error."""

    def __init__(self, limit: int, window: int):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {limit} requests per {window} seconds",
            error_code="RATE_LIMIT_EXCEEDED",
            context={"limit": limit, "window": window},
        )


class SessionNotFoundException(SessionNotFoundError):
    """Backward compatibility alias."""

    pass
