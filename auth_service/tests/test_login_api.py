"""Test login API"""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from db import get_session
from main import app
from models import Base, Tenant, User
from utils import hash_password

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create all tables
Base.metadata.create_all(bind=engine)


# Override the database dependency for testing
def override_get_session():
    """Override the database session for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


@pytest.fixture()
def test_db_session() -> Any:
    """Test database session"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# pylint: disable=redefined-outer-name
@pytest.fixture()
def seed_user(test_db_session: Session):
    """Seed user"""
    tenant = Tenant(
        tid=uuid4(),
        name="test-tenant",
        created_at=datetime.now(timezone.utc),
    )
    test_db_session.add(tenant)
    test_db_session.commit()

    user = User(
        uid=uuid4(),
        email="tenant1@example.com",
        hashed_password=hash_password("tenant123"),
        tenant_id=tenant.tid,
        role="user",
        created_at=datetime.now(timezone.utc),
    )
    test_db_session.add(user)
    test_db_session.commit()
    return user


def test_login_failure():
    """Test login failure"""
    response = client.post(
        "/api/v1/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpass",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
