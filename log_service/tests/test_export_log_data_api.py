"""Test export log data API"""

from unittest.mock import MagicMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from core.db import get_session
from main import app
from models.export_pipeline import ExportPipeline

client = TestClient(app)


def override_get_session():
    """Override get_session"""
    return MagicMock()


@patch("api.logs.send_to_export_queue")
@patch("api.logs.create_export_pipeline")
@patch("api.logs.get_tenant_id")
def test_export_log_data_api_success(
    mock_get_tenant_id, mock_create_export_pipeline, mock_send_to_export_queue
):
    """Test export log data API success"""
    # Arrange
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db

    # Mock get_tenant_id to return the expected tenant_id
    mock_get_tenant_id.return_value = "1"

    # Create a mock export pipeline
    pipeline_id = str(uuid4())
    mock_pipeline = MagicMock(spec=ExportPipeline)
    mock_pipeline.id = pipeline_id
    mock_pipeline.tenant_id = "1"
    mock_pipeline.status = "PENDING"
    mock_pipeline.file_url = None

    mock_create_export_pipeline.return_value = mock_pipeline

    # Act
    response = client.post("/api/v1/logs/export")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == pipeline_id
    assert data["data"]["tenant_id"] == "1"
    assert data["data"]["status"] == "PENDING"
    assert data["data"]["file_url"] is None

    # Verify function calls
    mock_get_tenant_id.assert_called_once()
    mock_create_export_pipeline.assert_called_once_with("1", mock_db)
    mock_send_to_export_queue.assert_called_once_with(pipeline_id, "1")

    # Cleanup
    app.dependency_overrides = {}


@patch("api.logs.send_to_export_queue")
@patch("api.logs.create_export_pipeline")
@patch("api.logs.get_tenant_id")
def test_export_log_data_api_with_different_tenant(
    mock_get_tenant_id, mock_create_export_pipeline, mock_send_to_export_queue
):
    """Test export log data API with different tenant"""
    # Arrange
    mock_db = MagicMock()
    app.dependency_overrides[get_session] = lambda: mock_db

    # Mock get_tenant_id to return a different tenant_id
    mock_get_tenant_id.return_value = "tenant-123"

    # Create a mock export pipeline
    pipeline_id = str(uuid4())
    mock_pipeline = MagicMock(spec=ExportPipeline)
    mock_pipeline.id = pipeline_id
    mock_pipeline.tenant_id = "tenant-123"
    mock_pipeline.status = "PENDING"
    mock_pipeline.file_url = None

    mock_create_export_pipeline.return_value = mock_pipeline

    # Act
    response = client.post("/api/v1/logs/export")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["tenant_id"] == "tenant-123"

    # Verify function calls
    mock_create_export_pipeline.assert_called_once_with("tenant-123", mock_db)
    mock_send_to_export_queue.assert_called_once_with(
        pipeline_id,
        "tenant-123",
    )

    # Cleanup
    app.dependency_overrides = {}
