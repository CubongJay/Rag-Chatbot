import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class APIKeyAuth:
    def __init__(self):
        self.settings = get_settings()

    async def __call__(self, request: Request, call_next):

        public_paths = ["/healthcheck", "/docs", "/redoc", "/openapi.json"]

        if request.url.path in public_paths:
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")

        if not api_key:
            logger.warning(f"Missing API key for {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={
                    "error": {"code": "UNAUTHORIZED", "message": "API key required"}
                },
            )

        if api_key != self.settings.api_key:
            logger.warning(f"Invalid API key for {request.url.path}")
            return JSONResponse(
                status_code=401,
                content={
                    "error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}
                },
            )

        return await call_next(request)
