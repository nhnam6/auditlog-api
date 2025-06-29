"""Auth middleware"""

import jwt
from starlette.middleware.base import BaseHTTPMiddleware

from core.config import settings
from core.logging import log_service_logger

logger = log_service_logger


class AuthMiddleware(BaseHTTPMiddleware):
    """Auth middleware"""

    TOKEN_PREFIX = "Bearer "

    async def dispatch(self, request, call_next):
        """Dispatch request"""
        token = request.headers.get("Authorization")
        if token and token.startswith(self.TOKEN_PREFIX):
            token = token.removeprefix(self.TOKEN_PREFIX)
            try:
                token_data = jwt.decode(
                    token,
                    settings.JWT_SECRET,
                    algorithms=settings.JWT_ALGORITHM,
                )
                request.state.user = token_data
            except jwt.PyJWTError as e:
                logger.error("JWT error: %s", e)
                request.state.user = {}
        return await call_next(request)
