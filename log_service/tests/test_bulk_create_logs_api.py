"""Test bulk create logs API"""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from core.db import get_session
from main import app

client = TestClient(app)


def override_get_session():
    """Override get_session"""
    return MagicMock()


@patch("api.logs.send_to_log_queue")
@patch("api.logs.create_bulk_logs")
@patch("api.logs.get_tenant_id")
def test_bulk_create_logs_api_success(
    mock_get_tenant_id, mock_create_bulk, mock_send_queue
):
    """Test bulk create logs API success"""
    # Arrange
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db
    mock_get_tenant_id.return_value = "tenant-1"

    logs_payload = {
        "logs": [
            {
                "user_id": "user-1",
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
        ]
    }

    mock_create_bulk.return_value = {
        "affected_rows": 2,
        "log_ids": ["log-1", "log-2"],
    }

    # Act
    response = client.post("/api/v1/logs/bulk", json=logs_payload)
    print(response.json())
    # Assert
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["affected_rows"] == 2

    mock_create_bulk.assert_called_once()
    mock_send_queue.assert_any_call("log-1", "tenant-1")
    mock_send_queue.assert_any_call("log-2", "tenant-1")

    # Cleanup
    app.dependency_overrides = {}
