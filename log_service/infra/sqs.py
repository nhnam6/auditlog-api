"""SQS"""

import json

import boto3

from core.config import settings
from core.logging import sqs_logger

logger = sqs_logger


def get_sqs_client():
    """Get SQS client

    Returns:
        boto3.client: SQS client
    """
    return boto3.client(
        "sqs",
        endpoint_url=settings.SQS_ENDPOINT,
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def send_to_log_queue(log_id: str, tenant_id: str):
    """Send to log queue

    Args:
        log_id (str): Log ID
        tenant_id (str): Tenant ID
    """
    logger.info(
        "Sending to log queue: log_id:%s, tenant_id:%s, queue_url:%s",
        log_id,
        tenant_id,
        settings.SQS_LOG_QUEUE_URL,
    )
    sqs = get_sqs_client()
    message = {"log_id": str(log_id), "tenant_id": str(tenant_id)}
    sqs.send_message(
        QueueUrl=settings.SQS_LOG_QUEUE_URL,
        MessageBody=json.dumps(message),
    )
    logger.info(
        "Sent to log queue: tenant_id:%s, log_id:%s, queue_url:%s",
        tenant_id,
        log_id,
        settings.SQS_LOG_QUEUE_URL,
    )


def send_to_export_queue(export_id: str, tenant_id: str):
    """Send to export queue

    Args:
        export_id (str): Export ID
        tenant_id (str): Tenant ID
    """
    logger.info(
        "Sending to export queue: export_id:%s, tenant_id:%s, queue_url:%s",
        export_id,
        tenant_id,
        settings.SQS_EXPORT_QUEUE_URL,
    )
    sqs = get_sqs_client()
    message = {
        "export_id": str(export_id),
        "tenant_id": str(tenant_id),
    }
    sqs.send_message(
        QueueUrl=settings.SQS_EXPORT_QUEUE_URL,
        MessageBody=json.dumps(message),
    )
    logger.info(
        "Sent to export queue: tenant_id:%s, export_id:%s, queue_url:%s",
        tenant_id,
        export_id,
        settings.SQS_EXPORT_QUEUE_URL,
    )
