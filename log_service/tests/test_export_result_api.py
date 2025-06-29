"""Test get export pipeline result API"""

from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from core.db import get_session
from main import app

client = TestClient(app)


def override_get_session():
    """Override get_session"""
    return MagicMock()


@patch("api.logs.get_export_pipeline")
@patch("api.logs.get_tenant_id")
def test_export_result_api_success(
    mock_get_tenant_id,
    mock_get_export_pipeline,
):
    """Test export result API success"""
    # Arrange
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db
    mock_get_tenant_id.return_value = "test-tenant-id"

    pipeline_id = str(uuid4())
    mock_pipeline = MagicMock()
    mock_pipeline.id = pipeline_id
    mock_pipeline.status = "DONE"
    mock_pipeline.tenant_id = "test-tenant-id"
    mock_pipeline.file_url = "https://example.com/file.csv"
    mock_pipeline.created_at = "2024-01-01T00:00:00Z"

    mock_get_export_pipeline.return_value = mock_pipeline

    # Act
    response = client.get(f"/api/v1/logs/export/{pipeline_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == pipeline_id
    assert data["status"] == "DONE"
    assert data["tenant_id"] == "test-tenant-id"
    assert data["created_at"] == "2024-01-01T00:00:00Z"
    assert data["file_url"] == "https://example.com/file.csv"

    mock_get_export_pipeline.assert_called_once_with(
        mock_db, "test-tenant-id", pipeline_id
    )

    # Cleanup
    app.dependency_overrides = {}
