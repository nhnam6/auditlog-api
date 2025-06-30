from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from constructs import Construct

"""
This stack is responsible for creating the infrastructure for the Auditlog application.
"""


class AuditlogInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "AuditlogInfraQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
