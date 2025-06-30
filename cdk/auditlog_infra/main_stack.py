"""
Main stack for the auditlog project.
"""

import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_rds as rds
from constructs import Construct
from aws_cdk import aws_secretsmanager as secretsmanager


class MainStack(Stack):
    """
    Main stack for the auditlog project.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "MainVpc", max_azs=2)
        print(f"Main VPC created: {vpc}")

        db = rds.DatabaseInstance(
            self,
            "MasterDB",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15
            ),
            vpc=vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            allocated_storage=20,
            credentials=rds.Credentials.from_generated_secret("masteruser"),
            database_name="masterdb",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            backup_retention=cdk.Duration.seconds(0),
        )
        print(f"Master DB created: {db}")

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        jwt_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "JWTSecret", "auth/jwt-secret"
        )
        db_secret = secretsmanager.Secret.from_secret_name_v2(
            self, "DBSecret", "auth/database-url"
        )
        auth_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "AuthService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../../auth_service"),
                environment={
                    "JWT_ALGORITHM": "HS256",
                    "ACCESS_TOKEN_EXPIRE_MINUTES": "60",
                },
                secrets={
                    "JWT_SECRET": ecs.Secret.from_secrets_manager(jwt_secret, "secret"),
                    "DATABASE_URL": ecs.Secret.from_secrets_manager(
                        db_secret, "secret"
                    ),
                },
            ),
            public_load_balancer=True,
        )
        print(f"Auth service created: {auth_service}")
