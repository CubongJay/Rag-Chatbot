from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.config.settings import get_settings

Base = declarative_base()


def get_database_engine():
    """Create database engine with settings."""
    settings = get_settings()

    engine = create_async_engine(
        settings.database_url,
        echo=False,
    )
    return engine


def get_async_database_session():
    """Create async database session factory."""
    engine = get_database_engine()
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def get_base():
    """Get the declarative base for models."""
    return Base
