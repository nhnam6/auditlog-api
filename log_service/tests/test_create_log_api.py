"""Test create log API"""

from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from core.db import get_session
from main import app

client = TestClient(app)


def override_get_session():
    """Override get_session"""
    return MagicMock()


@patch("api.logs.send_to_log_queue")
@patch("api.logs.create_log_entry")
@patch("api.logs.get_tenant_id")
def test_create_log_api_success(
    mock_get_tenant_id, mock_create_log, mock_send_to_queue
):
    """Test create log API success"""
    # Arrange
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db
    tenant_id = str(uuid4())
    mock_get_tenant_id.return_value = tenant_id

    payload = {
        "user_id": "user-abc",
        "email": "nhnam6@gmail.com",
        "action": "LOGIN",
        "resource_type": "user",
        "resource_id": "user_12345",
        "ip_address": "192.168.1.100",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "metadata": {"login_method": "password"},
        "before_state": {},
        "after_state": {"login_time": "2024-01-15T10:30:00Z"},
        "severity": "INFO",
    }

    alid = str(uuid4())
    mock_log = MagicMock()
    mock_log.alid = alid
    mock_log.user_id = "user-abc"
    mock_log.email = "nhnam6@gmail.com"
    mock_log.action = "LOGIN"
    mock_log.resource_type = "user"
    mock_log.resource_id = "user_12345"
    mock_log.ip_address = "192.168.1.100"
    mock_log.user_agent = "Mozilla/5.0"
    mock_log.log_metadata = {"login_method": "password"}
    mock_log.before_state = {}
    mock_log.after_state = {"login_time": "2024-01-15T10:30:00Z"}
    mock_log.severity = "INFO"
    mock_log.tenant_id = tenant_id
    mock_log.created_at = "2024-01-01T00:00:00Z"

    # This is only needed if your view uses .dict() anywhere explicitly
    mock_log.dict.return_value = {
        "alid": mock_log.alid,
        "user_id": mock_log.user_id,
        "email": mock_log.email,
        "action": mock_log.action,
        "resource_type": mock_log.resource_type,
        "resource_id": mock_log.resource_id,
        "ip_address": mock_log.ip_address,
        "user_agent": mock_log.user_agent,
        "metadata": mock_log.log_metadata,
        "before_state": mock_log.before_state,
        "after_state": mock_log.after_state,
        "severity": mock_log.severity,
        "tenant_id": mock_log.tenant_id,
        "created_at": mock_log.created_at,
    }

    mock_create_log.return_value = mock_log

    # Act
    response = client.post("/api/v1/logs", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["alid"] == alid
    assert data["tenant_id"] == tenant_id

    mock_get_tenant_id.assert_called_once()
    mock_create_log.assert_called_once()
    mock_send_to_queue.assert_called_once_with(alid, tenant_id)

    # Cleanup
    app.dependency_overrides = {}
