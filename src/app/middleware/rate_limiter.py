import logging
import time
from collections import defaultdict, deque
from fastapi import Request

from app.config.settings import get_settings
from app.errors.errors import RateLimitError

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self):
        self.settings = get_settings()

        self.requests = defaultdict(lambda: deque())
        self.cleanup_interval = 300
        self.last_cleanup = time.time()

    def _cleanup_old_requests(self, current_time: float):
        """Clean up old request timestamps to prevent memory leaks."""
        if current_time - self.last_cleanup < self.cleanup_interval:
            return

        cutoff_time = current_time - self.settings.rate_limit_window
        for api_key in list(self.requests.keys()):

            while self.requests[api_key] and self.requests[api_key][0] < cutoff_time:
                self.requests[api_key].popleft()

            if not self.requests[api_key]:
                del self.requests[api_key]

        self.last_cleanup = current_time

    def _is_rate_limited(self, api_key: str, current_time: float) -> bool:
        """Check if API key has exceeded rate limit."""
        cutoff_time = current_time - self.settings.rate_limit_window

        while self.requests[api_key] and self.requests[api_key][0] < cutoff_time:
            self.requests[api_key].popleft()

        return len(self.requests[api_key]) >= self.settings.rate_limit_requests

    async def __call__(self, request: Request, call_next):

        public_paths = ["/healthcheck", "/docs", "/redoc", "/openapi.json"]

        if request.url.path in public_paths:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if not api_key:

            return await call_next(request)

        current_time = time.time()

        self._cleanup_old_requests(current_time)

        if self._is_rate_limited(api_key, current_time):
            logger.warning(f"Rate limit exceeded for API key: {api_key[:8]}...")
            raise RateLimitError(
                self.settings.rate_limit_requests, self.settings.rate_limit_window
            )

        self.requests[api_key].append(current_time)

        response = await call_next(request)
        return response
