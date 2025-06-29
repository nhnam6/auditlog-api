"""Test cleanup logs API"""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from core.db import get_session
from main import app

client = TestClient(app)


def override_get_session():
    """Override get_session"""
    return MagicMock()


@patch("api.logs.cleanup_old_logs")
@patch("api.logs.delete_old_logs_in_opensearch")
@patch("api.logs.get_tenant_id")
def test_cleanup_logs_api(
    mock_get_tenant_id, mock_delete_opensearch, mock_cleanup_logs
):
    """Test cleanup logs API"""
    # Arrange
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db

    # Mock get_tenant_id to return the expected tenant_id
    mock_get_tenant_id.return_value = "1"

    mock_cleanup_logs.return_value = {
        "deleted": 123,
        "cutoff": "2024-01-01T00:00:00Z",
    }

    # Act
    response = client.delete("/api/v1/logs/cleanup")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["deleted"] == 123

    mock_cleanup_logs.assert_called_once_with(mock_db, "1")
    mock_delete_opensearch.assert_called_once_with("1")

    # Cleanup
    app.dependency_overrides = {}
