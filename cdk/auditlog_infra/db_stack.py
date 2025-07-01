"""
This stack creates a database instance and a secret for the database.
"""

import os

import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_rds as rds
from constructs import Construct


class DatabaseStack(Stack):
    """
    This stack creates a database instance and a secret for the database.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        db_id: str,
        db_name: str,
        db_secret_name: str,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, "MainVpc", max_azs=2)

        self.db = rds.DatabaseInstance(
            self,
            db_id,
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_15
            ),
            vpc=self.vpc,
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO
            ),
            allocated_storage=20,
            credentials=rds.Credentials.from_generated_secret(db_secret_name),
            database_name=db_name,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            backup_retention=cdk.Duration.days(0),
        )
