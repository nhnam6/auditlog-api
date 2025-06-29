"""Auth middleware"""

import jwt
from starlette.middleware.base import BaseHTTPMiddleware

from logger import auth_logger
from utils import verify_token

logger = auth_logger


class AuthMiddleware(BaseHTTPMiddleware):
    """Auth middleware"""

    TOKEN_PREFIX = "Bearer "

    async def dispatch(self, request, call_next):
        """Dispatch request"""
        token = request.headers.get("Authorization")
        if token and token.startswith(self.TOKEN_PREFIX):
            token = token.removeprefix(self.TOKEN_PREFIX)

            try:
                token_data = verify_token(token)
                request.state.user = token_data
            except jwt.PyJWTError as e:
                logger.error("JWT error: %s", e)
                request.state.user = {}
        return await call_next(request)
