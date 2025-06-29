"""Test get log API"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from core.db import get_session
from main import app

client = TestClient(app)


@patch("api.logs.get_log_entry")
@patch("api.logs.get_tenant_id")
def test_get_log_api_success(mock_get_tenant_id, mock_get_log_entry):
    """Test get log API success"""
    # Arrange
    log_id = str(uuid4())
    tenant_id = "tenant-abc"

    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db
    mock_get_tenant_id.return_value = tenant_id

    # Create a mock log with real data (not MagicMock fields)
    mock_log = MagicMock()
    mock_log.alid = log_id
    mock_log.tenant_id = tenant_id
    mock_log.user_id = "user-123"
    mock_log.email = "user@example.com"
    mock_log.action = "LOGIN"
    mock_log.resource_type = "user"
    mock_log.resource_id = "user_12345"
    mock_log.ip_address = "192.168.0.1"
    mock_log.user_agent = "Mozilla/5.0"
    mock_log.log_metadata = {"login_method": "oauth"}
    mock_log.before_state = {}
    mock_log.after_state = {"login_time": "2024-01-01T00:00:00Z"}
    mock_log.severity = "INFO"
    mock_log.created_at = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    mock_log.dict.return_value = {
        "alid": mock_log.alid,
        "tenant_id": mock_log.tenant_id,
        "user_id": mock_log.user_id,
        "email": mock_log.email,
        "action": mock_log.action,
        "resource_type": mock_log.resource_type,
        "resource_id": mock_log.resource_id,
        "ip_address": mock_log.ip_address,
        "user_agent": mock_log.user_agent,
        "log_metadata": mock_log.log_metadata,
        "before_state": mock_log.before_state,
        "after_state": mock_log.after_state,
        "severity": mock_log.severity,
        "created_at": mock_log.created_at.isoformat(),
    }

    mock_get_log_entry.return_value = mock_log

    # Act
    response = client.get(f"/api/v1/logs/{log_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["alid"] == log_id
    assert data["action"] == "LOGIN"
    assert data["resource_type"] == "user"
    assert data["tenant_id"] == tenant_id
    assert data["log_metadata"]["login_method"] == "oauth"

    mock_get_tenant_id.assert_called_once()
    mock_get_log_entry.assert_called_once_with(mock_db, tenant_id, log_id)

    # Cleanup
    app.dependency_overrides = {}
