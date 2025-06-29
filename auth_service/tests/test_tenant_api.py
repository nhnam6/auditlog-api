"""Test tenant API"""

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
from utils import create_access_token, hash_password

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
def seed_admin_user(test_db_session: Session):
    """Seed admin user"""
    tenant = Tenant(
        tid=uuid4(),
        name="admin-tenant",
        created_at=datetime.now(timezone.utc),
    )
    test_db_session.add(tenant)
    test_db_session.commit()

    user = User(
        uid=uuid4(),
        email="admin@example.com",
        hashed_password=hash_password("admin123"),
        tenant_id=tenant.tid,
        role="admin",
        created_at=datetime.now(timezone.utc),
    )
    test_db_session.add(user)
    test_db_session.commit()
    return user


# pylint: disable=redefined-outer-name
@pytest.fixture()
def seed_regular_user(test_db_session: Session):
    """Seed regular user"""
    tenant = Tenant(
        tid=uuid4(),
        name="regular-tenant",
        created_at=datetime.now(timezone.utc),
    )
    test_db_session.add(tenant)
    test_db_session.commit()

    user = User(
        uid=uuid4(),
        email="user@example.com",
        hashed_password=hash_password("user123"),
        tenant_id=tenant.tid,
        role="user",
        created_at=datetime.now(timezone.utc),
    )
    test_db_session.add(user)
    test_db_session.commit()
    return user


@pytest.fixture()
def seed_admin_user_token(seed_admin_user: User):
    """Seed admin user token"""
    token_data = {
        "sub": seed_admin_user.email,
        "tenant_id": str(seed_admin_user.tenant_id or ""),
        "role": seed_admin_user.role,
    }
    token = create_access_token(token_data)
    return token


@pytest.fixture()
def seed_regular_user_token(seed_regular_user: User):
    """Seed regular user token"""
    token_data = {
        "sub": seed_regular_user.email,
        "tenant_id": str(seed_regular_user.tenant_id or ""),
        "role": seed_regular_user.role,
    }
    token = create_access_token(token_data)
    return token


def get_auth_headers(token: str) -> dict:
    """Get authorization headers"""
    return {"Authorization": f"Bearer {token}"}


# pylint: disable=redefined-outer-name
def test_get_tenants_success(
    test_db_session: Session,
    seed_admin_user_token: str,
):
    """Test get tenants success"""
    # Create some test tenants
    tenant1 = Tenant(
        tid=uuid4(),
        name="tenant-1",
        created_at=datetime.now(timezone.utc),
    )
    tenant2 = Tenant(
        tid=uuid4(),
        name="tenant-2",
        created_at=datetime.now(timezone.utc),
    )
    test_db_session.add(tenant1)
    test_db_session.add(tenant2)
    test_db_session.commit()

    response = client.get(
        "/api/v1/tenants", headers=get_auth_headers(seed_admin_user_token)
    )

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert data["total"] >= 2


def test_get_tenants_pagination(seed_admin_user_token: str):
    """Test get tenants with pagination"""
    response = client.get(
        "/api/v1/tenants?page=1&page_size=5",
        headers=get_auth_headers(seed_admin_user_token),
    )

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5


def test_get_tenants_invalid_pagination(seed_admin_user_token: str):
    """Test get tenants with invalid pagination"""
    response = client.get(
        "/api/v1/tenants?page=0&page_size=5",
        headers=get_auth_headers(seed_admin_user_token),
    )
    assert response.status_code == 422  # Validation error

    response = client.get(
        "/api/v1/tenants?page=1&page_size=0",
        headers=get_auth_headers(seed_admin_user_token),
    )
    assert response.status_code == 422  # Validation error


def test_create_tenant_success(seed_admin_user_token: str):
    """Test create tenant success with admin user"""
    tenant_data = {
        "name": f"new-tenant-{uuid4()}",
        "email": "newuser@newtenant.com",
        "password": "password123",
    }

    response = client.post(
        "/api/v1/tenants",
        json=tenant_data,
        headers=get_auth_headers(seed_admin_user_token),
    )

    assert response.status_code == 201
    data = response.json()
    assert "data" in data
    assert data["data"]["name"] == tenant_data["name"]


def test_create_tenant_unauthorized():
    """Test create tenant without authentication"""
    tenant_data = {
        "name": "new-tenant",
        "email": "newuser@newtenant.com",
        "password": "password123",
    }

    response = client.post("/api/v1/tenants", json=tenant_data)
    assert response.status_code == 401


def test_create_tenant_forbidden(seed_regular_user_token: str):
    """Test create tenant with non-admin user"""
    tenant_data = {
        "name": "new-tenant",
        "email": "newuser@newtenant.com",
        "password": "password123",
    }

    response = client.post(
        "/api/v1/tenants",
        json=tenant_data,
        headers=get_auth_headers(seed_regular_user_token),
    )
    assert response.status_code == 403
