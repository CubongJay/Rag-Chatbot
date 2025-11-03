from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_async_database_session

AsyncSessionLocal = get_async_database_session()


async def get_async_db() -> AsyncSession:
    """Dependency to get database session."""

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
