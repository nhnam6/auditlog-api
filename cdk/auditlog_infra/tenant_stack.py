"""
This stack creates an ECS cluster and a service for the log service.
"""

import os

import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class LogStack(Stack):
    """
    This stack creates an ECS cluster and a service for the auth service.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        service_id: str,
        tenant_id: str,
        image_path: str,
        vpc: ec2.IVpc,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        sqs_log_queue_url = os.environ.get("SQS_LOG_QUEUE_URL")
        sqs_export_queue_url = os.environ.get("SQS_EXPORT_QUEUE_URL")
        log_queue_name = os.environ.get("LOG_QUEUE_NAME")
        export_queue_name = os.environ.get("EXPORT_QUEUE_NAME")
        export_s3_bucket = os.environ.get("EXPORT_S3_BUCKET")
        opensearch_host = os.environ.get("OPENSEARCH_HOST")
        opensearch_port = os.environ.get("OPENSEARCH_PORT")
        opensearch_user = os.environ.get("OPENSEARCH_USER")
        opensearch_pass = os.environ.get("OPENSEARCH_PASS")
        database_url = os.environ.get("DATABASE_URL")
        jwt_algorithm = os.environ.get("JWT_ALGORITHM")
        jwt_secret = os.environ.get("JWT_SECRET")

        environment = {
            "DEBUG": "True",
            "DATABASE_URL": database_url,
            "JWT_ALGORITHM": jwt_algorithm,
            "JWT_SECRET": jwt_secret,
            "TENANT_ID": tenant_id,
            "AWS_ENDPOINT_URL": "",
            "AWS_ACCESS_KEY_ID": aws_access_key_id,
            "AWS_SECRET_ACCESS_KEY": aws_secret_access_key,
            "AWS_REGION": "ap-southeast-1",
            "SQS_ENDPOINT": "",
            "SQS_LOG_QUEUE_URL": sqs_log_queue_url,
            "SQS_EXPORT_QUEUE_URL": sqs_export_queue_url,
            "LOG_QUEUE_NAME": log_queue_name,
            "EXPORT_QUEUE_NAME": export_queue_name,
            "EXPORT_S3_BUCKET": export_s3_bucket,
            "OPENSEARCH_HOST": opensearch_host,
            "OPENSEARCH_PORT": opensearch_port,
            "OPENSEARCH_USER": opensearch_user,
            "OPENSEARCH_PASS": opensearch_pass,
        }

        service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            service_id,
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset(image_path),
                container_port=8001,
                environment=environment,
            ),
            public_load_balancer=True,
            health_check_grace_period=cdk.Duration.seconds(60),
            load_balancer_name=f"{service_id}-alb",
        )
        service.target_group.configure_health_check(
            path="/health",
            port="8001",
            protocol=elbv2.Protocol.HTTP,
            healthy_threshold_count=2,
            unhealthy_threshold_count=3,
            timeout=cdk.Duration.seconds(10),
            interval=cdk.Duration.seconds(60),
            healthy_http_codes="200",
        )

        # Create log consumer task definition
        log_consumer = ecs.FargateTaskDefinition(self, "LogConsumerTask")
        log_consumer.add_container(
            "LogConsumerContainer",
            image=ecs.ContainerImage.from_asset("../../log_service"),
            command=["python", "consumer_log.py"],
            environment=environment,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="log-consumer"),
        )

        # Create export consumer task definition
        export_consumer = ecs.FargateTaskDefinition(self, "ExportConsumerTask")
        export_consumer.add_container(
            "ExportConsumerContainer",
            image=ecs.ContainerImage.from_asset("../../log_service"),
            command=["python", "consumer_export.py"],
            environment=environment,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="export-consumer"),
        )
