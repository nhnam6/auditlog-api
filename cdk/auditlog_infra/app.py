import aws_cdk as cdk

from main_stack import MainStack
from tenant_stack import TenantStack

app = cdk.App()

MainStack(
    app,
    "AuditlogMainStack",
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)
TenantStack(
    app,
    "AuditlogTenantStack",
    tenant_id="tenant-a",
    tags={"tenant_id": "tenant-a"},
    env=cdk.Environment(account="598540919918", region="ap-northeast-1"),
)

app.synth()
