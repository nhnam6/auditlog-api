"""
This stack creates a public S3 bucket.
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


class S3PublicBucketStack(Stack):
    """
    This stack creates a public S3 bucket.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        bucket_name: str,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Create the bucket
        self.bucket = s3.Bucket(
            self,
            bucket_name,
            public_read_access=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Output the bucket name and URL
        CfnOutput(self, "BucketName", value=self.bucket.bucket_name)
        CfnOutput(
            self,
            "BucketURL",
            value=f"https://{self.bucket.bucket_name}.s3.amazonaws.com/",
        )
