"""S3 service"""

import os
from uuid import uuid4

import boto3
from botocore.config import Config

from core.config import settings
from core.logging import s3_logger

S3_PREFIX = os.getenv("S3_PREFIX", "exports/")

logger = s3_logger


def get_s3_client():
    """Get S3 client"""
    config = Config(
        max_pool_connections=50,
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=60,
        connect_timeout=60,
        tcp_keepalive=True,
    )
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_ENDPOINT_URL,
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=config,
    )


def upload_to_s3(file_path: str, bucket: str) -> str:
    """Upload to S3"""
    logger.info("Uploading to S3: file_path:%s, bucket:%s", file_path, bucket)
    file_key = f"{S3_PREFIX}{uuid4()}_{os.path.basename(file_path)}"
    s3 = get_s3_client()
    s3.upload_file(
        file_path,
        bucket,
        file_key,
        ExtraArgs={"ACL": "public-read"},
    )

    url = f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{file_key}"
    return url
