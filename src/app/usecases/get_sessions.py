from typing import List, Optional
from uuid import UUID

from app.domain.entities.session import Session
from app.domain.interfaces.session_repository import SessionRepository


class GetSessionsUseCase:
    """Use case for retrieving sessions."""

    def __init__(self, session_repo: SessionRepository) -> None:
        self.session_repo = session_repo

    async def execute_all(
        self, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Session]:
        """
        Retrieve all sessions with optional pagination.

        Args:
            page: Optional page number for pagination
            size: Optional page size for pagination

        Returns:
            List of session entities
        """
        return await self.session_repo.get_all(page=page, size=size)

    async def execute_by_favorite(
        self, is_favorite: bool, page: Optional[int] = None, size: Optional[int] = None
    ) -> List[Session]:
        """
        Retrieve sessions filtered by favorite status with optional pagination.

        Args:
            is_favorite: Filter by favorite status
            page: Optional page number for pagination
            size: Optional page size for pagination

        Returns:
            List of session entities filtered by favorite status
        """
        return await self.session_repo.get_by_favorite(
            is_favorite=is_favorite, page=page, size=size
        )

    async def execute_with_pagination(
        self, limit: int = 50, offset: int = 0, is_favorite: Optional[bool] = None
    ) -> List[Session]:
        """
        Retrieve sessions with pagination support.

        Args:
            limit: Maximum number of sessions to retrieve (default: 50)
            offset: Number of sessions to skip (default: 0)
            is_favorite: Optional filter by favorite status

        Returns:
            List of session entities with pagination applied

        Raises:
            ValueError: If invalid pagination parameters
        """

        if limit <= 0:
            raise ValueError("Limit must be greater than 0")
        if offset < 0:
            raise ValueError("Offset must be non-negative")

        if is_favorite is not None:
            sessions = await self.session_repo.get_by_favorite(is_favorite)
        else:
            sessions = await self.session_repo.get_all()

        return sessions[offset : offset + limit]

    async def execute_count(self, is_favorite: Optional[bool] = None) -> int:
        """
        Count the number of sessions.

        Args:
            is_favorite: Optional filter by favorite status

        Returns:
            Number of sessions
        #"""
        # if is_favorite is not None:
        #     sessions = self.session_repo.get_by_favorite(is_favorite)
        # else:
        #     sessions = self.session_repo.get_all()

        # return len(sessions)
        return await self.session_repo.get_sessions_count(is_favorite=is_favorite)
