"""
This stack creates an OpenSearch domain.
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


class OpenSearchStack(Stack):
    """
    This stack creates an OpenSearch domain.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        domain_name: str,
        **kwargs,
    ):
        super().__init__(scope, id, **kwargs)

        # Public Access Policy: allow access from IP or all (for test only)
        access_policies = [
            iam.PolicyStatement(
                actions=["es:*"],
                effect=iam.Effect.ALLOW,
                principals=[iam.ArnPrincipal("*")],
                resources=["*"],
                conditions={
                    "IpAddress": {
                        "aws:SourceIp": "0.0.0.0/0",
                    }
                },
            )
        ]
        user = os.environ.get("OPENSEARCH_USER")
        password = os.environ.get("OPENSEARCH_PASS")
        domain = opensearch.Domain(
            self,
            domain_name,
            version=opensearch.EngineVersion.OPENSEARCH_2_11,
            enforce_https=True,
            node_to_node_encryption=True,
            encryption_at_rest=opensearch.EncryptionAtRestOptions(enabled=True),
            fine_grained_access_control=opensearch.AdvancedSecurityOptions(
                master_user_name=user,
                master_user_password=cdk.SecretValue.unsafe_plain_text(password),
            ),
            access_policies=access_policies,
            removal_policy=RemovalPolicy.DESTROY,
            capacity=opensearch.CapacityConfig(
                data_nodes=1, data_node_instance_type="t3.small.search"
            ),
            zone_awareness=opensearch.ZoneAwarenessConfig(enabled=False),
        )

        # Output
        CfnOutput(self, "OpenSearchEndpoint", value=domain.domain_endpoint)
