"""Test logs service"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from uuid import UUID

from models.audit_logs import AuditLog
from schemas.schemas import AuditLogCreate
from services.logs import (
    cleanup_old_logs,
    create_bulk_logs,
    create_log_entry,
    get_log_entry,
    get_logs_for_export,
)


@patch("services.logs.mask_sensitive_data")
def test_create_log_entry(mock_mask):
    """Test create log entry"""
    mock_db = MagicMock()
    tenant_id = "tenant-123"
    payload = AuditLogCreate(
        user_id="user-abc",
        email="email@example.com",
        action="LOGIN",
        resource_type="user",
        resource_id="res-001",
        ip_address="1.2.3.4",
        user_agent="agent",
        metadata={"m": 1},
        before_state={},
        after_state={"success": True},
        severity="INFO",
    )

    masked_data = payload.model_dump()
    mock_mask.return_value = masked_data

    log = create_log_entry(mock_db, tenant_id, payload)

    assert isinstance(log, AuditLog)
    assert log.tenant_id == tenant_id
    assert isinstance(log.alid, UUID)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_get_log_entry():
    """Test get log entry"""
    mock_db = MagicMock()
    tenant_id = "tenant-x"
    log_id = "log-123"
    expected_log = MagicMock()
    mock_db.query.return_value.filter_by.return_value.first.return_value = expected_log

    result = get_log_entry(mock_db, tenant_id, log_id)

    assert result == expected_log
    mock_db.query.assert_called_once_with(AuditLog)
    mock_db.query.return_value.filter_by.assert_called_once_with(
        alid=log_id, tenant_id=tenant_id
    )


def test_get_logs_for_export():
    """Test get logs for export"""
    mock_db = MagicMock()
    mock_logs = [MagicMock(), MagicMock()]
    mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = (
        mock_logs
    )

    result = get_logs_for_export(mock_db, "tenant-abc")

    assert result == mock_logs
    mock_db.query.assert_called_once_with(AuditLog)


def test_cleanup_old_logs():
    """Test cleanup old logs"""
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value.filter.return_value
    mock_filter.delete.return_value = 42

    result = cleanup_old_logs(mock_db, "tenant-x", retention_days=30)

    assert result["deleted"] == 42
    _ = datetime.now(timezone.utc) - timedelta(days=30)
    assert "cutoff" in result
    assert datetime.fromisoformat(result["cutoff"]) <= datetime.now(timezone.utc)
    mock_db.commit.assert_called_once()
