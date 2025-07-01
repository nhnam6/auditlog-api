"""
This is the main entry point for the Auditlog application.
"""

import aws_cdk as cdk

from db_stack import DatabaseStack
from main_stack import AuthStack
from s3_stack import S3PublicBucketStack
from sqs_stack import SQSStack
from tenant_stack import LogStack

app = cdk.App()

db_stack = DatabaseStack(
    app,
    "AuditLogAuthDBStack",
    db_id="AuditLogAuthDB",
    db_name="master_db",
    db_secret_name="masteruser",
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

auth_stack = AuthStack(
    app,
    "AuditLogAuthStack-v4",
    service_id="AuthService-v4",
    vpc=db_stack.vpc,
    image_path="../../auth_service",
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

log_db_stack = DatabaseStack(
    app,
    "AuditLogLogDBStack",
    db_id="AuditLogLogDB",
    db_name="log_db",
    db_secret_name="masteruser",
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

log_queue_stack = SQSStack(
    app,
    "AuditLogLogQueueStack",
    queue_name="log-queue",
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

export_queue_stack = SQSStack(
    app,
    "AuditLogExportQueueStack",
    queue_name="export-queue",
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

s3_bucket_stack = S3PublicBucketStack(
    app,
    "AuditLogS3BucketStack",
    bucket_name="logs-export",
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

log_stack = LogStack(
    app,
    "AuditLogLogStack-v2",
    service_id="LogService-v2",
    tenant_id="4ccf062b-20eb-4f94-85b2-908f12aef6ca",
    image_path="../../log_service",
    vpc=log_db_stack.vpc,
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

app.synth()
