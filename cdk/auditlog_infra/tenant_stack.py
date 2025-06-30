"""
Tenant stack for the auditlog project.
"""

import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_opensearchservice as opensearch
from aws_cdk import aws_rds as rds
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class TenantStack(Stack):
    """
    Tenant stack for the auditlog project.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        tenant_id: str,
        tags: dict = None,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        if tags:
            for k, v in tags.items():
                cdk.Tags.of(self).add(k, v)

        vpc = ec2.Vpc(self, "TenantVpc", max_azs=2)

        db = rds.DatabaseInstance(
            self,
            "TenantDB",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15
            ),
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            allocated_storage=20,
            credentials=rds.Credentials.from_generated_secret("tenantuser"),
            database_name="logs_db",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            backup_retention=cdk.Duration.seconds(0),
        )
        print(f"Tenant DB created: {db}")

        cluster = ecs.Cluster(self, "TenantCluster", vpc=vpc)

        sqs_queue = sqs.Queue(self, "LogQueue")
        print(f"Log queue created: {sqs_queue}")
        export_queue = sqs.Queue(self, "ExportQueue")
        print(f"Export queue created: {export_queue}")
        s3_bucket = s3.Bucket(self, "ExportBucket")
        print(f"Export bucket created: {s3_bucket}")

        jwt_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "JWTSecret", "log/jwt-secret"
        )
        db_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "DBSecret", "log/database-url"
        )
        ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "LogService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../../log_service"),
                environment={
                    "DEBUG": "False",
                    "TENANT_ID": tenant_id,
                    "JWT_ALGORITHM": "HS256",
                   
                    "SQS_LOG_QUEUE_URL": sqs_queue.queue_url,
                    "SQS_EXPORT_QUEUE_URL": export_queue.queue_url,
                    "LOG_QUEUE_NAME": "log-queue",
                    "EXPORT_QUEUE_NAME": "export-queue",
                    "EXPORT_S3_BUCKET": s3_bucket.bucket_name,
                    "OPENSEARCH_HOST": "localhost",
                    "OPENSEARCH_PORT": "9200",
                   
                },
                secrets={
                    "JWT_SECRET": ecs.Secret.from_secrets_manager(jwt_secret, "secret",),
                    "DATABASE_URL": ecs.Secret.from_secrets_manager(
                        db_secret, "secret"
                    ),
                },
            ),
            public_load_balancer=True,
        )

        # Create log consumer task definition
        log_consumer = ecs.FargateTaskDefinition(self, "LogConsumerTask")
        log_consumer.add_container(
            "LogConsumerContainer",
            image=ecs.ContainerImage.from_asset("../../log_service"),
            command=["python", "consumer_log.py"],
            environment={
                "DEBUG": "True",
                "TENANT_ID": tenant_id,
                "JWT_ALGORITHM": "HS256",
                "AWS_ENDPOINT_URL": "http://localhost:4566",
                "AWS_ACCESS_KEY_ID": "fake",
                "AWS_SECRET_ACCESS_KEY": "fake",
                "AWS_REGION": "ap-southeast-1",
                "SQS_ENDPOINT": "http://localhost:4566",
                "SQS_LOG_QUEUE_URL": sqs_queue.queue_url,
                "SQS_EXPORT_QUEUE_URL": export_queue.queue_url,
                "LOG_QUEUE_NAME": "log-queue",
                "EXPORT_QUEUE_NAME": "export-queue",
                "EXPORT_S3_BUCKET": "logs-export",
                "OPENSEARCH_HOST": "localhost",
                "OPENSEARCH_PORT": "9200",
                "OPENSEARCH_USER": "admin",
                "OPENSEARCH_PASS": "admin",
            },
            secrets={
                "JWT_SECRET": ecs.Secret.from_secrets_manager(jwt_secret),
                "DATABASE_URL": ecs.Secret.from_secrets_manager(db_secret),
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="log-consumer"),
        )

        ecs.FargateService(
            self,
            "LogConsumerService",
            cluster=cluster,
            task_definition=log_consumer,
            desired_count=1,
        )

        # Create export consumer task definition
        export_consumer = ecs.FargateTaskDefinition(self, "ExportConsumerTask")
        export_consumer.add_container(
            "ExportConsumerContainer",
            image=ecs.ContainerImage.from_asset("../../log_service"),
            command=["python", "consumer_export.py"],
            environment={
                "DEBUG": "True",
                "TENANT_ID": tenant_id,
                "JWT_ALGORITHM": "HS256",
                "AWS_ENDPOINT_URL": "http://localhost:4566",
                "AWS_ACCESS_KEY_ID": "fake",
                "AWS_SECRET_ACCESS_KEY": "fake",
                "AWS_REGION": "ap-southeast-1",
                "SQS_ENDPOINT": "http://localhost:4566",
                "SQS_LOG_QUEUE_URL": sqs_queue.queue_url,
                "SQS_EXPORT_QUEUE_URL": export_queue.queue_url,
                "LOG_QUEUE_NAME": "log-queue",
                "EXPORT_QUEUE_NAME": "export-queue",
                "EXPORT_S3_BUCKET": "logs-export",
                "OPENSEARCH_HOST": "localhost",
                "OPENSEARCH_PORT": "9200",
                "OPENSEARCH_USER": "admin",
                "OPENSEARCH_PASS": "admin",
            },
            secrets={
                "JWT_SECRET": ecs.Secret.from_secrets_manager(jwt_secret),
                "DATABASE_URL": ecs.Secret.from_secrets_manager(db_secret),
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="export-consumer"),
        )

        ecs.FargateService(
            self,
            "ExportConsumerService",
            cluster=cluster,
            task_definition=export_consumer,
            desired_count=1,
        )
