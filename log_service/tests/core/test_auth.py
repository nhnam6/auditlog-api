"""Test auth middleware"""

import jwt
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from core.auth import AuthMiddleware
from core.config import settings


def create_test_app():
    """Create a test app"""
    app = FastAPI()

    @app.get("/abcxyz")
    async def abcxyz(request: Request):
        return JSONResponse(content={"user": request.state.user})

    app.add_middleware(AuthMiddleware)
    return app


def test_auth_middleware_valid_token():
    """Test auth middleware with valid token"""
    # Arrange
    payload = {
        "user_id": "123",
        "tenant_id": "tenant-abc",
        "email": "me@example.com",
    }
    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
    app = create_test_app()

    # Act
    client = TestClient(app)
    response = client.get(
        "/abcxyz",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == 200
    user = response.json()["user"]
    assert user["user_id"] == "123"
    assert user["tenant_id"] == "tenant-abc"
    assert user["email"] == "me@example.com"


def test_auth_middleware_invalid_token():
    """Test auth middleware with invalid token"""
    # Arrange
    invalid_token = "Bearer this.is.invalid.token"
    app = create_test_app()

    # Act
    client = TestClient(app)
    response = client.get("/abcxyz", headers={"Authorization": invalid_token})

    # Assert
    assert response.status_code == 200
    user = response.json()["user"]
    assert user == {}  # fallback if JWT decoding fails
