"""Test get log stats API"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@patch("api.logs.get_log_stats_opensearch")
@patch("api.logs.get_tenant_id")
def test_get_log_stats_api(mock_get_tenant_id, mock_get_log_stats):
    """Test get log stats API"""
    # Arrange
    mock_get_tenant_id.return_value = "test-tenant-id"
    mock_get_log_stats.return_value = {
        "action_counts": [
            {"key": "login", "doc_count": 100},
            {"key": "logout", "doc_count": 50},
        ],
        "severity_counts": [
            {"key": "info", "doc_count": 120},
            {"key": "error", "doc_count": 30},
        ],
    }

    # Act
    response = client.get("/api/v1/logs/stats")

    # Assert
    assert response.status_code == 200
    data = response.json()["data"]

    assert "action_counts" in data
    assert data["action_counts"][0]["key"] == "login"
    assert data["action_counts"][0]["doc_count"] == 100

    assert "severity_counts" in data
    assert data["severity_counts"][1]["key"] == "error"
    assert data["severity_counts"][1]["doc_count"] == 30

    mock_get_tenant_id.assert_called_once()
    mock_get_log_stats.assert_called_once_with("test-tenant-id")
