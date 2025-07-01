"""
This stack creates an SQS queue.
"""

import os

import aws_cdk as cdk
from aws_cdk import CfnOutput, RemovalPolicy, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_opensearchservice as opensearch
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sqs as sqs
from constructs import Construct


class SQSStack(Stack):
    """
    This stack creates an SQS queue.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        queue_name: str,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Main queue
        self.queue = sqs.Queue(
            self,
            queue_name,
            visibility_timeout=cdk.Duration.seconds(60),
            retention_period=cdk.Duration.days(4),
            removal_policy=cdk.RemovalPolicy.DESTROY,  # safe for dev/test
        )

        # Export ARN for other stacks
        CfnOutput(
            self,
            "QueueArn",
            value=self.queue.queue_arn,
            export_name=f"{queue_name}QueueArn",
        )
        CfnOutput(
            self,
            "QueueName",
            value=self.queue.queue_name,
            export_name=f"{queue_name}QueueName",
        )
