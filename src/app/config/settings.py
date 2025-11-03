from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    app_name: str = Field(default="RAG-Chatbot", json_schema_extra={"env": "APP_NAME"})
    debug: bool = Field(default=False, json_schema_extra={"env": "DEBUG"})
    environment: str = Field(
        default="development", json_schema_extra={"env": "ENVIRONMENT"}
    )

    database_url: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})

    api_host: str = Field(default="0.0.0.0", json_schema_extra={"env": "API_HOST"})
    api_port: int = Field(default=8000, json_schema_extra={"env": "API_PORT"})

    secret_key: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    api_key: str = Field(..., json_schema_extra={"env": "API_KEY"})
    encryption_key: str = Field(..., json_schema_extra={"env": "ENCRYPTION_KEY"})

    cors_origins: list[str] = Field(
        default=["*"], json_schema_extra={"env": "CORS_ORIGINS"}
    )
    cors_allow_credentials: bool = Field(
        default=True, json_schema_extra={"env": "CORS_ALLOW_CREDENTIALS"}
    )

    log_level: str = Field(default="INFO", json_schema_extra={"env": "LOG_LEVEL"})
    log_format: str = Field(default="json", json_schema_extra={"env": "LOG_FORMAT"})

    rate_limit_requests: int = Field(
        default=100, json_schema_extra={"env": "RATE_LIMIT_REQUESTS"}
    )
    rate_limit_window: int = Field(
        default=60, json_schema_extra={"env": "RATE_LIMIT_WINDOW"}
    )

    openai_api_key: Optional[str] = Field(
        default=None, json_schema_extra={"env": "OPENAI_API_KEY"}
    )

    llm_model: str = Field(default="gpt-4", json_schema_extra={"env": "LLM_MODEL"})
    llm_temperature: float = Field(
        default=0.7, json_schema_extra={"env": "LLM_TEMPERATURE"}
    )
    llm_max_tokens: int = Field(
        default=1000, json_schema_extra={"env": "LLM_MAX_TOKENS"}
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
