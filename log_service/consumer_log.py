"""Log consumer"""

import json
import time

import boto3

from core.config import settings
from core.db import get_session
from core.logging import consumer_log_consumer_logger, setup_logging
from models import AuditLog
from services.search import index_log_to_opensearch

setup_logging()

sqs = boto3.client(
    "sqs",
    endpoint_url=settings.SQS_ENDPOINT,
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

logger = consumer_log_consumer_logger


def handle_message(msg: dict):
    """Handle message"""
    log_id = msg["log_id"]
    tenant_id = msg["tenant_id"]

    db = next(get_session())
    log = (
        db.query(AuditLog)
        .filter_by(
            alid=log_id,
            tenant_id=tenant_id,
        )
        .first()
    )
    if log:
        logger.info("Indexing log: log_id:%s", log_id)
        index_log_to_opensearch(log)
    else:
        logger.error("Log not found: log_id:%s", log_id)


def run_consumer():
    """Run SQS log consumer"""
    logger.info("Starting SQS log consumer...")
    while True:
        response = sqs.receive_message(
            QueueUrl=settings.SQS_LOG_QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=10,
        )

        messages = response.get("Messages", [])
        for message in messages:
            try:
                body = json.loads(message["Body"])
                logger.info("Processing message: body:%s", body)
                handle_message(body)

                # Delete after success
                sqs.delete_message(
                    QueueUrl=settings.SQS_LOG_QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"],
                )
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("Error: %s", e)
        time.sleep(1)


if __name__ == "__main__":
    run_consumer()
