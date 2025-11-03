from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1 import context, messages, sessions
from app.config.logger import get_logger
from app.config.settings import get_settings
from app.middleware.error_handler import global_exception_handler
from app.middleware.rate_limiter import RateLimiter

settings = get_settings()

app_logger = get_logger("RAG-Chatbot")

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "sessions",
            "description": "Session management operations",
        },
        {
            "name": "messages",
            "description": "Message operations",
        },
    ],
    openapi_extra={
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                    "description": "API Key for authentication. Get your key from environment variables.",
                }
            }
        },
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(RateLimiter())


app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, global_exception_handler)
app.add_exception_handler(SQLAlchemyError, global_exception_handler)

app.include_router(messages.router)
app.include_router(sessions.router)
app.include_router(context.router)


@app.get("/healthcheck")
def healthcheck():
    """Health check endpoint to verify the service is running."""

    return {
        "status_code": status.HTTP_200_OK,
        "status": "Healthy",
        "app_name": settings.app_name,
        "environment": settings.environment,
    }
