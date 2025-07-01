"""
This stack creates an ECS cluster and a service for the auth service.
"""

import os

import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from constructs import Construct


class AuthStack(Stack):
    """
    This stack creates an ECS cluster and a service for the auth service.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        service_id: str,
        vpc: ec2.IVpc,
        image_path: str,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        jwt_secret = os.environ.get("JWT_SECRET")
        db_secret = os.environ.get("DATABASE_URL")

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
                environment={
                    "ACCESS_TOKEN_EXPIRE_MINUTES": "60",
                    "JWT_ALGORITHM": "HS256",
                    "JWT_SECRET": jwt_secret,
                    "DATABASE_URL": db_secret,
                },
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
