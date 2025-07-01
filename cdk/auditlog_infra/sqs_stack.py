"""
This stack creates an SQS queue.
"""

import aws_cdk as cdk
from aws_cdk import CfnOutput, Stack
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
