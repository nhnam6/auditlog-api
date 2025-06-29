"""Export consumer"""

import json
import time

import boto3

from core.config import settings
from core.db import get_session
from core.logging import consumer_log_consumer_logger, setup_logging
from infra.s3 import upload_to_s3
from models import ExportPipeline
from services.csv import write_logs_to_csv
from services.logs import get_logs_for_export

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
    export_id = msg["export_id"]
    tenant_id = msg["tenant_id"]

    db = next(get_session())
    export_pipeline = (
        db.query(ExportPipeline)
        .filter_by(
            id=export_id,
            tenant_id=tenant_id,
        )
        .first()
    )
    if export_pipeline:
        try:
            logger.info("Export pipeline found: export_id:%s", export_id)
            export_pipeline.status = "IN_PROGRESS"
            db.commit()
            db.refresh(export_pipeline)

            # Get logs and write to CSV
            logger.info("Getting logs for export: export_id:%s", export_id)
            logs = get_logs_for_export(db, tenant_id)
            logger.info("Writing logs to CSV: export_id:%s", export_id)
            file_path = write_logs_to_csv(logs, tenant_id)

            # Upload to S3
            logger.info("Uploading to S3: export_id:%s", export_id)
            s3_url = upload_to_s3(file_path, settings.EXPORT_S3_BUCKET)

            # Update export pipeline
            export_pipeline.status = "DONE"
            export_pipeline.file_url = s3_url
            logger.info("Export pipeline updated: export_id:%s", export_id)
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Error: %s", e)
            export_pipeline.status = "FAILED"
        finally:
            db.commit()
            db.refresh(export_pipeline)
    else:
        logger.error("Export pipeline not found: export_id:%s", export_id)


def run_consumer():
    """Run SQS export consumer"""
    logger.info("Starting SQS export consumer...")
    while True:
        response = sqs.receive_message(
            QueueUrl=settings.SQS_EXPORT_QUEUE_URL,
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
                    QueueUrl=settings.SQS_EXPORT_QUEUE_URL,
                    ReceiptHandle=message["ReceiptHandle"],
                )
            except Exception as e:  # pylint: disable=broad-exception-caught
                logger.error("Error: %s", e)
        time.sleep(1)


if __name__ == "__main__":
    run_consumer()
