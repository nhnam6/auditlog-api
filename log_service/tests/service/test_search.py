"""Test search service"""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from models import AuditLog
from services.search import (
    delete_old_logs_in_opensearch,
    get_log_stats_opensearch,
    index_log_to_opensearch,
    search_logs,
)


@patch("services.search.get_opensearch_client")
def test_index_log_to_opensearch(mock_get_client):
    """Test index log to opensearch"""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    log = AuditLog(
        alid="log-123",
        tenant_id="tenant-abc",
        user_id="user-123",
        email="test@example.com",
        action="LOGIN",
        resource_type="user",
        resource_id="user_001",
        ip_address="127.0.0.1",
        user_agent="test-agent",
        log_metadata={"key": "value"},
        before_state={},
        after_state={"logged_in": True},
        severity="INFO",
        created_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )

    index_log_to_opensearch(log)

    mock_client.index.assert_called_once()
    _, kwargs = mock_client.index.call_args
    assert kwargs["index"] == "logs-tenant-abc"
    assert kwargs["id"] == "log-123"
    assert kwargs["body"]["action"] == "LOGIN"


@patch("services.search.get_opensearch_client")
def test_search_logs(mock_get_client):
    """Test search logs"""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_client.search.return_value = {
        "hits": {
            "total": {"value": 1},
            "hits": [{"_source": {"action": "LOGIN"}}],
        }
    }

    filters = {"action": "LOGIN", "page": 1, "page_size": 10}
    result = search_logs("tenant-abc", filters)

    assert result["total"] == 1
    assert result["logs"][0]["action"] == "LOGIN"
    mock_client.search.assert_called_once()


@patch("services.search.get_opensearch_client")
def test_get_log_stats_opensearch(mock_get_client):
    """Test get log stats in opensearch"""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_client.search.return_value = {
        "aggregations": {
            "by_action": {
                "buckets": [{"key": "LOGIN", "doc_count": 5}],
            },
            "by_severity": {
                "buckets": [{"key": "INFO", "doc_count": 10}],
            },
        }
    }

    stats = get_log_stats_opensearch("tenant-abc")
    assert stats["action_counts"][0]["key"] == "LOGIN"
    assert stats["severity_counts"][0]["key"] == "INFO"


@patch("services.search.get_opensearch_client")
def test_delete_old_logs_in_opensearch(mock_get_client):
    """Test delete old logs in opensearch"""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_client.delete_by_query.return_value = {"deleted": 123}

    response = delete_old_logs_in_opensearch("tenant-abc", days=30)
    assert response["deleted"] == 123
    mock_client.delete_by_query.assert_called_once()
