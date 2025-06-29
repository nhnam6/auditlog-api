"""Test list logs API"""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@patch("api.logs.search_logs")
@patch("api.logs.get_tenant_id")
def test_list_logs_api_success(mock_get_tenant_id, mock_search_logs):
    """Test list logs API success"""
    # Arrange
    tenant_id = "tenant-abc"
    mock_get_tenant_id.return_value = tenant_id

    expected_filters = {
        "action": "LOGIN",
        "severity": "INFO",
        "user_id": None,
        "search": None,
        "page": 2,
        "page_size": 1,
    }

    mock_search_logs.return_value = {
        "total": 5,
        "logs": [
            {
                "id": "log-001",
                "action": "LOGIN",
                "resource_type": "user",
                "resource_id": "user_123",
                "severity": "INFO",
                "user_id": "user-abc",
                "tenant_id": tenant_id,
                "created_at": "2024-01-01T00:00:00Z",
            }
        ],
    }

    # Act
    response = client.get("/api/v1/logs/?action=LOGIN&severity=INFO&page=2&page_size=1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["total"] == 5
    assert len(data["items"]) == 1
    assert data["page"] == 2
    assert data["page_size"] == 1

    mock_get_tenant_id.assert_called_once()
    mock_search_logs.assert_called_once_with(tenant_id, expected_filters)
