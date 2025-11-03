from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

from app.config.settings import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify API key for endpoint protection.

    Args:
        api_key: API key from X-API-Key header

    Returns:
        str: The verified API key

    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")

    settings = get_settings()
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key


__all__ = ["verify_api_key", "api_key_header"]
