"""Test SQS"""

import json
from unittest.mock import MagicMock, patch

from infra.sqs import send_to_export_queue, send_to_log_queue


@patch("infra.sqs.get_sqs_client")
def test_send_to_log_queue(mock_get_client):
    """Test send to log queue"""
    # Arrange
    mock_sqs = MagicMock()
    mock_get_client.return_value = mock_sqs

    log_id = "log-123"
    tenant_id = "tenant-abc"

    # Act
    send_to_log_queue(log_id, tenant_id)

    # Assert
    mock_get_client.assert_called_once()
    mock_sqs.send_message.assert_called_once_with(
        QueueUrl=mock_get_client.return_value.send_message.call_args[1]["QueueUrl"],
        MessageBody=json.dumps({"log_id": log_id, "tenant_id": tenant_id}),
    )


@patch("infra.sqs.get_sqs_client")
def test_send_to_export_queue(mock_get_client):
    """Test send to export queue"""
    # Arrange
    mock_sqs = MagicMock()
    mock_get_client.return_value = mock_sqs

    export_id = "export-456"
    tenant_id = "tenant-xyz"

    # Act
    send_to_export_queue(export_id, tenant_id)

    # Assert
    mock_get_client.assert_called_once()
    mock_sqs.send_message.assert_called_once_with(
        QueueUrl=mock_get_client.return_value.send_message.call_args[1]["QueueUrl"],
        MessageBody=json.dumps({"export_id": export_id, "tenant_id": tenant_id}),
    )
