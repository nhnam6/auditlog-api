"""Test export service"""

from unittest.mock import MagicMock

from models.export_pipeline import ExportPipeline
from services.export import create_export_pipeline, get_export_pipeline


def test_create_export_pipeline():
    """Test create export pipeline"""
    # Arrange
    mock_db = MagicMock()
    mock_session_add = mock_db.add
    mock_session_commit = mock_db.commit

    tenant_id = "tenant-abc"

    # Act
    pipeline = create_export_pipeline(tenant_id, mock_db)

    # Assert
    assert isinstance(pipeline, ExportPipeline)
    assert pipeline.tenant_id == tenant_id
    assert pipeline.status == "PENDING"
    assert pipeline.created_at is not None

    mock_session_add.assert_called_once_with(pipeline)
    mock_session_commit.assert_called_once()


def test_get_export_pipeline():
    """Test get export pipeline"""
    # Arrange
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter_by.return_value

    pipeline_id = "pipeline-123"
    tenant_id = "tenant-abc"

    expected_pipeline = ExportPipeline(
        id=pipeline_id,
        tenant_id=tenant_id,
        status="COMPLETED",
        created_at=None,
    )

    mock_filter.first.return_value = expected_pipeline

    # Act
    result = get_export_pipeline(mock_db, tenant_id, pipeline_id)

    # Assert
    assert result == expected_pipeline
    mock_db.query.assert_called_once_with(ExportPipeline)
    mock_query.filter_by.assert_called_once_with(
        id=pipeline_id,
        tenant_id=tenant_id,
    )
    mock_filter.first.assert_called_once()
