# AuditLog Infrastructure Deployment Guide

This document provides comprehensive instructions for deploying and managing the AuditLog infrastructure using AWS CDK.

## Prerequisites

- AWS CLI configured with appropriate credentials
- AWS CDK CLI installed (`npm install -g aws-cdk`)
- Python 3.8+ and pip
- Docker (for building container images)
- Appropriate AWS permissions for the services being deployed

## Environment Configuration

### AWS Profile Setup

Ensure you have an AWS profile configured:

```bash
aws configure --profile test
```

### Account and Region

- **Account ID**: 598540919918
- **Region**: ap-northeast-1
- **Profile**: test

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Step

- nvm use 20

```bash
Now using node v20.19.2 (npm v10.8.2)
```

- source .venv/bin/activate

- cdk bootstrap aws://598540919918/ap-northeast-1 --profile test --toolkit-stack-name AuditLogToolkit

```bash

⏳ Bootstrapping environment aws://598540919918/ap-northeast-1...
Trusted accounts for deployment: (none)
Trusted accounts for lookup: (none)
Using default execution policy of 'arn:aws:iam::aws:policy/AdministratorAccess'. Pass '--cloudformation-execution-policies' to customize.
AuditLogToolkit: creating CloudFormation changeset...
✅ Environment aws://598540919918/ap-northeast-1 bootstrapped.

```

- cdk bootstrap aws://598540919918/ap-northeast-1 --profile test --toolkit-stack-name AuditLogToolkit

```bash
Trusted accounts for deployment: (none)
Trusted accounts for lookup: (none)
Using default execution policy of 'arn:aws:iam::aws:policy/AdministratorAccess'. Pass '--cloudformation-execution-policies' to customize.
AuditLogToolkit: creating CloudFormation changeset...
 ✅  Environment aws://598540919918/ap-northeast-1 bootstrapped.
(.venv) 21:02:31 ~/workspace/labs/auditlog-api/cdk/auditlog_infra main $ cdk --profile test deploy AuditLogAuthDBStack

✨  Synthesis time: 12.97s

AuditLogAuthDBStack: start: Building AuditLogAuthDBStack/Custom::VpcRestrictDefaultSGCustomResourceProvider Code
AuditLogAuthDBStack: success: Built AuditLogAuthDBStack/Custom::VpcRestrictDefaultSGCustomResourceProvider Code
AuditLogAuthDBStack: start: Building AuditLogAuthDBStack Template
AuditLogAuthDBStack: success: Built AuditLogAuthDBStack Template
AuditLogAuthDBStack: start: Publishing AuditLogAuthDBStack/Custom::VpcRestrictDefaultSGCustomResourceProvider Code (598540919918-ap-northeast-1)
AuditLogAuthDBStack: start: Publishing AuditLogAuthDBStack Template (598540919918-ap-northeast-1)
AuditLogAuthDBStack: success: Published AuditLogAuthDBStack/Custom::VpcRestrictDefaultSGCustomResourceProvider Code (598540919918-ap-northeast-1)
AuditLogAuthDBStack: success: Published AuditLogAuthDBStack Template (598540919918-ap-northeast-1)
Stack AuditLogAuthDBStack
IAM Statement Changes
┌───┬────────────────────────────────────────────────────────────────────────────────────────┬────────┬───────────────────────────────────┬────────────────────────────────────────────────────────────────┬───────────┐
│   │ Resource                                                                               │ Effect │ Action                            │ Principal                                                      │ Condition │
├───┼────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role.Arn}                         │ Allow  │ sts:AssumeRole                    │ Service:lambda.amazonaws.com                                   │           │
├───┼────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ec2:ap-northeast-1:598540919918:security-group/${MainVpc.DefaultSecurityGroup} │ Allow  │ ec2:AuthorizeSecurityGroupEgress  │ AWS:${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │           │
│   │                                                                                        │        │ ec2:AuthorizeSecurityGroupIngress │                                                                │           │
│   │                                                                                        │        │ ec2:RevokeSecurityGroupEgress     │                                                                │           │
│   │                                                                                        │        │ ec2:RevokeSecurityGroupIngress    │                                                                │           │
└───┴────────────────────────────────────────────────────────────────────────────────────────┴────────┴───────────────────────────────────┴────────────────────────────────────────────────────────────────┴───────────┘
IAM Policy Changes
┌───┬────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                   │ Managed Policy ARN                                                                           │
├───┼────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"} │
└───┴────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬─────────────────────────────────────────┬─────┬────────────┬─────────────────┐
│   │ Group                                   │ Dir │ Protocol   │ Peer            │
├───┼─────────────────────────────────────────┼─────┼────────────┼─────────────────┤
│ + │ ${AuditLogAuthDB/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4) │
└───┴─────────────────────────────────────────┴─────┴────────────┴─────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)


Do you wish to deploy these changes (y/n)? y
AuditLogAuthDBStack: deploying... [1/1]
AuditLogAuthDBStack: creating CloudFormation changeset...
[███████████████████████████████████████████▉··············] (25/33)

 ✅  AuditLogAuthDBStack

✨  Deployment time: 294.49s

Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogAuthDBStack/d4e00b90-5684-11f0-8854-0647a29c7809

✨  Total time: 307.45s
```

- export DATABASE_URL=
- export JWT_SECRET=

- cdk --profile test deploy AuditLogAuthStack

```bash

```

- cdk --profile test deploy AuditLogAuthStack-v4

```
Including dependency stacks: AuditLogAuthDBStack
[Warning at /AuditLogAuthStack-v4/AuthService-v4/Service] minHealthyPercent has not been configured so the default value of 50% is used. The number of running tasks will decrease below the desired count during deployments etc. See https://github.com/aws/aws-cdk/issues/31705 [ack: @aws-cdk/aws-ecs:minHealthyPercent]

✨  Synthesis time: 15.53s

AuditLogAuthDBStack
AuditLogAuthStack-v4: start: Building AuditLogAuthStack-v4 Template
AuditLogAuthStack-v4: success: Built AuditLogAuthStack-v4 Template
AuditLogAuthDBStack: deploying... [1/2]

 ✅  AuditLogAuthDBStack (no changes)

✨  Deployment time: 1.49s

Outputs:
AuditLogAuthDBStack.ExportsOutputRefMainVpc919A5E7E852FB707 = vpc-0706f65a9ee748672
AuditLogAuthDBStack.ExportsOutputRefMainVpcPrivateSubnet1SubnetA8D0757B15568C8D = subnet-0c26d41d7bfa2404c
AuditLogAuthDBStack.ExportsOutputRefMainVpcPrivateSubnet2SubnetFC4F66C434910780 = subnet-05ac0154eaf25c860
AuditLogAuthDBStack.ExportsOutputRefMainVpcPublicSubnet1Subnet269349B144A4FA94 = subnet-0267c542f82f79133
AuditLogAuthDBStack.ExportsOutputRefMainVpcPublicSubnet2Subnet287D062B1BDD0C32 = subnet-0bef95dd67f1cfcc1
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogAuthDBStack/d4e00b90-5684-11f0-8854-0647a29c7809

✨  Total time: 17.02s

AuditLogAuthStack-v4: start: Publishing AuditLogAuthStack-v4 Template (598540919918-ap-northeast-1)
AuditLogAuthStack-v4: success: Published AuditLogAuthStack-v4 Template (598540919918-ap-northeast-1)
AuditLogAuthStack-v4
Stack AuditLogAuthStack-v4
IAM Statement Changes
┌───┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────┬─────────────────────────────────┬─────────────────────────────────────────────┬───────────┐
│   │ Resource                                                                                                      │ Effect │ Action                          │ Principal                                   │ Condition │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼─────────────────────────────────────────────┼───────────┤
│ + │ ${AuthService-v4/TaskDef/ExecutionRole.Arn}                                                                   │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com             │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼─────────────────────────────────────────────┼───────────┤
│ + │ ${AuthService-v4/TaskDef/TaskRole.Arn}                                                                        │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com             │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼─────────────────────────────────────────────┼───────────┤
│ + │ ${AuthService-v4/TaskDef/web/LogGroup.Arn}                                                                    │ Allow  │ logs:CreateLogStream            │ AWS:${AuthService-v4/TaskDef/ExecutionRole} │           │
│   │                                                                                                               │        │ logs:PutLogEvents               │                                             │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼─────────────────────────────────────────────┼───────────┤
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken       │ AWS:${AuthService-v4/TaskDef/ExecutionRole} │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼─────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability │ AWS:${AuthService-v4/TaskDef/ExecutionRole} │           │
│   │                                                                                                               │        │ ecr:BatchGetImage               │                                             │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer      │                                             │           │
└───┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴─────────────────────────────────┴─────────────────────────────────────────────┴───────────┘
Security Group Changes
┌───┬─────────────────────────────────────────────────┬─────┬────────────┬─────────────────────────────────────────────────┐
│   │ Group                                           │ Dir │ Protocol   │ Peer                                            │
├───┼─────────────────────────────────────────────────┼─────┼────────────┼─────────────────────────────────────────────────┤
│ + │ ${AuthService-v4/LB/SecurityGroup.GroupId}      │ In  │ TCP 80     │ Everyone (IPv4)                                 │
│ + │ ${AuthService-v4/LB/SecurityGroup.GroupId}      │ Out │ TCP 8001   │ ${AuthService-v4/Service/SecurityGroup.GroupId} │
├───┼─────────────────────────────────────────────────┼─────┼────────────┼─────────────────────────────────────────────────┤
│ + │ ${AuthService-v4/Service/SecurityGroup.GroupId} │ In  │ TCP 8001   │ ${AuthService-v4/LB/SecurityGroup.GroupId}      │
│ + │ ${AuthService-v4/Service/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4)                                 │
└───┴─────────────────────────────────────────────────┴─────┴────────────┴─────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)


Do you wish to deploy these changes (y/n)? y
AuditLogAuthStack-v4: deploying... [2/2]
AuditLogAuthStack-v4: creating CloudFormation changeset...
[███▋······················································] (1/16)

 ✅  AuditLogAuthStack-v4

✨  Deployment time: 278.79s

Outputs:
AuditLogAuthStack-v4.AuthServicev4LoadBalancerDNS2FF5A9F4 = AuthService-v4-alb-1416314438.ap-northeast-1.elb.amazonaws.com
AuditLogAuthStack-v4.AuthServicev4ServiceURL6F650B96 = http://AuthService-v4-alb-1416314438.ap-northeast-1.elb.amazonaws.com
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogAuthStack-v4/1b8ec9a0-568f-11f0-914e-0eb7ce20d777

✨  Total time: 294.32s
```

- cdk --profile test deploy AuditLogLogDBStack

```bash
✨  Synthesis time: 15.28s

AuditLogLogDBStack: start: Building AuditLogLogDBStack Template
AuditLogLogDBStack: success: Built AuditLogLogDBStack Template
AuditLogLogDBStack: start: Publishing AuditLogLogDBStack Template (598540919918-ap-northeast-1)
AuditLogLogDBStack: success: Published AuditLogLogDBStack Template (598540919918-ap-northeast-1)
Stack AuditLogLogDBStack
IAM Statement Changes
┌───┬────────────────────────────────────────────────────────────────────────────────────────┬────────┬───────────────────────────────────┬────────────────────────────────────────────────────────────────┬───────────┐
│   │ Resource                                                                               │ Effect │ Action                            │ Principal                                                      │ Condition │
├───┼────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role.Arn}                         │ Allow  │ sts:AssumeRole                    │ Service:lambda.amazonaws.com                                   │           │
├───┼────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ec2:ap-northeast-1:598540919918:security-group/${MainVpc.DefaultSecurityGroup} │ Allow  │ ec2:AuthorizeSecurityGroupEgress  │ AWS:${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │           │
│   │                                                                                        │        │ ec2:AuthorizeSecurityGroupIngress │                                                                │           │
│   │                                                                                        │        │ ec2:RevokeSecurityGroupEgress     │                                                                │           │
│   │                                                                                        │        │ ec2:RevokeSecurityGroupIngress    │                                                                │           │
└───┴────────────────────────────────────────────────────────────────────────────────────────┴────────┴───────────────────────────────────┴────────────────────────────────────────────────────────────────┴───────────┘
IAM Policy Changes
┌───┬────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                   │ Managed Policy ARN                                                                           │
├───┼────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"} │
└───┴────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬────────────────────────────────────────┬─────┬────────────┬─────────────────┐
│   │ Group                                  │ Dir │ Protocol   │ Peer            │
├───┼────────────────────────────────────────┼─────┼────────────┼─────────────────┤
│ + │ ${AuditLogLogDB/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4) │
└───┴────────────────────────────────────────┴─────┴────────────┴─────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)


Do you wish to deploy these changes (y/n)? y
AuditLogLogDBStack: deploying... [1/1]
AuditLogLogDBStack: creating CloudFormation changeset...

 ✅  AuditLogLogDBStack

✨  Deployment time: 295.32s

Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogLogDBStack/9b6b1be0-5691-11f0-9d2d-0e17bc43fb77

✨  Total time: 310.6s
```

cdk --profile test deploy AuditLogLogQueueStack

```bash
✨  Synthesis time: 17.88s

AuditLogLogQueueStack: start: Building AuditLogLogQueueStack Template
AuditLogLogQueueStack: success: Built AuditLogLogQueueStack Template
AuditLogLogQueueStack: start: Publishing AuditLogLogQueueStack Template (598540919918-ap-northeast-1)
AuditLogLogQueueStack: success: Published AuditLogLogQueueStack Template (598540919918-ap-northeast-1)
AuditLogLogQueueStack: deploying... [1/1]
AuditLogLogQueueStack: creating CloudFormation changeset...

 ✅  AuditLogLogQueueStack

✨  Deployment time: 48.23s

Outputs:
AuditLogLogQueueStack.QueueArn = arn:aws:sqs:ap-northeast-1:598540919918:AuditLogLogQueueStack-logqueueCDD10A25-P1JiaXtj1NBR
AuditLogLogQueueStack.QueueName = AuditLogLogQueueStack-logqueueCDD10A25-P1JiaXtj1NBR
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogLogQueueStack/5d5d4420-5693-11f0-92af-0a11dcbc6b15

✨  Total time: 66.1s
```

cdk --profile test deploy AuditLogExportQueueStack

```bash
✨  Synthesis time: 14.24s

AuditLogExportQueueStack: start: Building AuditLogExportQueueStack Template
AuditLogExportQueueStack: success: Built AuditLogExportQueueStack Template
AuditLogExportQueueStack: start: Publishing AuditLogExportQueueStack Template (598540919918-ap-northeast-1)
AuditLogExportQueueStack: success: Published AuditLogExportQueueStack Template (598540919918-ap-northeast-1)
AuditLogExportQueueStack: deploying... [1/1]
AuditLogExportQueueStack: creating CloudFormation changeset...

 ✅  AuditLogExportQueueStack

✨  Deployment time: 48.3s

Outputs:
AuditLogExportQueueStack.QueueArn = arn:aws:sqs:ap-northeast-1:598540919918:AuditLogExportQueueStack-exportqueueB723D8B3-YYjgtYq0FYGD
AuditLogExportQueueStack.QueueName = AuditLogExportQueueStack-exportqueueB723D8B3-YYjgtYq0FYGD
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogExportQueueStack/9db7b910-5693-11f0-8511-0efaa35bdf21

✨  Total time: 62.54s
```

- cdk --profile test deploy AuditLogS3BucketStack

```bash
✨  Synthesis time: 15.78s

AuditLogS3BucketStack: start: Building AuditLogS3BucketStack/Custom::S3AutoDeleteObjectsCustomResourceProvider Code
AuditLogS3BucketStack: success: Built AuditLogS3BucketStack/Custom::S3AutoDeleteObjectsCustomResourceProvider Code
AuditLogS3BucketStack: start: Building AuditLogS3BucketStack Template
AuditLogS3BucketStack: success: Built AuditLogS3BucketStack Template
AuditLogS3BucketStack: start: Publishing AuditLogS3BucketStack/Custom::S3AutoDeleteObjectsCustomResourceProvider Code (598540919918-ap-northeast-1)
AuditLogS3BucketStack: start: Publishing AuditLogS3BucketStack Template (598540919918-ap-northeast-1)
AuditLogS3BucketStack: success: Published AuditLogS3BucketStack/Custom::S3AutoDeleteObjectsCustomResourceProvider Code (598540919918-ap-northeast-1)
AuditLogS3BucketStack: success: Published AuditLogS3BucketStack Template (598540919918-ap-northeast-1)
Stack AuditLogS3BucketStack
IAM Statement Changes
┌───┬───────────────────────────────────────────────────────────────┬────────┬────────────────────┬───────────────────────────────────────────────────────────────────┬───────────┐
│   │ Resource                                                      │ Effect │ Action             │ Principal                                                         │ Condition │
├───┼───────────────────────────────────────────────────────────────┼────────┼────────────────────┼───────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${Custom::S3AutoDeleteObjectsCustomResourceProvider/Role.Arn} │ Allow  │ sts:AssumeRole     │ Service:lambda.amazonaws.com                                      │           │
├───┼───────────────────────────────────────────────────────────────┼────────┼────────────────────┼───────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${logs-export.Arn}                                            │ Allow  │ s3:DeleteObject*   │ AWS:${Custom::S3AutoDeleteObjectsCustomResourceProvider/Role.Arn} │           │
│   │ ${logs-export.Arn}/*                                          │        │ s3:GetBucket*      │                                                                   │           │
│   │                                                               │        │ s3:List*           │                                                                   │           │
│   │                                                               │        │ s3:PutBucketPolicy │                                                                   │           │
├───┼───────────────────────────────────────────────────────────────┼────────┼────────────────────┼───────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${logs-export.Arn}/*                                          │ Allow  │ s3:GetObject       │ AWS:*                                                             │           │
└───┴───────────────────────────────────────────────────────────────┴────────┴────────────────────┴───────────────────────────────────────────────────────────────────┴───────────┘
IAM Policy Changes
┌───┬───────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                  │ Managed Policy ARN                                                                           │
├───┼───────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${Custom::S3AutoDeleteObjectsCustomResourceProvider/Role} │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"} │
└───┴───────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)


Do you wish to deploy these changes (y/n)?
Do you wish to deploy these changes (y/n)? y
AuditLogS3BucketStack: deploying... [1/1]
AuditLogS3BucketStack: creating CloudFormation changeset...

 ✅  AuditLogS3BucketStack

✨  Deployment time: 48.66s

Outputs:
AuditLogS3BucketStack.BucketName = auditlogs3bucketstack-logsexportfd736235-calkvu7a5h6l
AuditLogS3BucketStack.BucketURL = https://auditlogs3bucketstack-logsexportfd736235-calkvu7a5h6l.s3.amazonaws.com/
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogS3BucketStack/d0f0dcc0-5694-11f0-ab94-06ac317e8351

✨  Total time: 64.43s
```

- cdk --profile test deploy AuditLogLogStack-v6

```bash
✨  Synthesis time: 20.79s

AuditLogLogDBStack
AuditLogLogStack-v6: start: Building AuditLogLogStack-v6 Template
AuditLogLogStack-v6: success: Built AuditLogLogStack-v6 Template
AuditLogLogDBStack: deploying... [1/2]

 ✅  AuditLogLogDBStack (no changes)

✨  Deployment time: 9.17s

Outputs:
AuditLogLogDBStack.ExportsOutputRefMainVpc919A5E7E852FB707 = vpc-0a6c2f962f0d928d0
AuditLogLogDBStack.ExportsOutputRefMainVpcPrivateSubnet1SubnetA8D0757B15568C8D = subnet-0551ca6170f32278f
AuditLogLogDBStack.ExportsOutputRefMainVpcPrivateSubnet2SubnetFC4F66C434910780 = subnet-061660f3a10602da8
AuditLogLogDBStack.ExportsOutputRefMainVpcPublicSubnet1Subnet269349B144A4FA94 = subnet-04c3eb3d2a8d9e8a3
AuditLogLogDBStack.ExportsOutputRefMainVpcPublicSubnet2Subnet287D062B1BDD0C32 = subnet-0328a7485bd72879e
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogLogDBStack/9b6b1be0-5691-11f0-9d2d-0e17bc43fb77

✨  Total time: 29.96s

AuditLogLogStack-v6: start: Publishing AuditLogLogStack-v6 Template (598540919918-ap-northeast-1)
AuditLogLogStack-v6: success: Published AuditLogLogStack-v6 Template (598540919918-ap-northeast-1)
AuditLogLogStack-v6
Stack AuditLogLogStack-v6
IAM Statement Changes
┌───┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────┬─────────────────────────────────┬────────────────────────────────────────────┬───────────┐
│   │ Resource                                                                                                      │ Effect │ Action                          │ Principal                                  │ Condition │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${ExportConsumerTask/ExecutionRole.Arn}                                                                       │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${ExportConsumerTask/ExportConsumerContainer/LogGroup.Arn}                                                    │ Allow  │ logs:CreateLogStream            │ AWS:${ExportConsumerTask/ExecutionRole}    │           │
│   │                                                                                                               │        │ logs:PutLogEvents               │                                            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${ExportConsumerTask/TaskRole.Arn}                                                                            │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${LogConsumerTask/ExecutionRole.Arn}                                                                          │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${LogConsumerTask/LogConsumerContainer/LogGroup.Arn}                                                          │ Allow  │ logs:CreateLogStream            │ AWS:${LogConsumerTask/ExecutionRole}       │           │
│   │                                                                                                               │        │ logs:PutLogEvents               │                                            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${LogConsumerTask/TaskRole.Arn}                                                                               │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${LogService-v6/TaskDef/ExecutionRole.Arn}                                                                    │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${LogService-v6/TaskDef/TaskRole.Arn}                                                                         │ Allow  │ sts:AssumeRole                  │ Service:ecs-tasks.amazonaws.com            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ ${LogService-v6/TaskDef/web/LogGroup.Arn}                                                                     │ Allow  │ logs:CreateLogStream            │ AWS:${LogService-v6/TaskDef/ExecutionRole} │           │
│   │                                                                                                               │        │ logs:PutLogEvents               │                                            │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken       │ AWS:${LogService-v6/TaskDef/ExecutionRole} │           │
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken       │ AWS:${LogConsumerTask/ExecutionRole}       │           │
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken       │ AWS:${ExportConsumerTask/ExecutionRole}    │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼─────────────────────────────────┼────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability │ AWS:${LogService-v6/TaskDef/ExecutionRole} │           │
│   │                                                                                                               │        │ ecr:BatchGetImage               │                                            │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer      │                                            │           │
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability │ AWS:${LogConsumerTask/ExecutionRole}       │           │
│   │                                                                                                               │        │ ecr:BatchGetImage               │                                            │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer      │                                            │           │
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability │ AWS:${ExportConsumerTask/ExecutionRole}    │           │
│   │                                                                                                               │        │ ecr:BatchGetImage               │                                            │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer      │                                            │           │
└───┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴─────────────────────────────────┴────────────────────────────────────────────┴───────────┘
Security Group Changes
┌───┬────────────────────────────────────────────────┬─────┬────────────┬────────────────────────────────────────────────┐
│   │ Group                                          │ Dir │ Protocol   │ Peer                                           │
├───┼────────────────────────────────────────────────┼─────┼────────────┼────────────────────────────────────────────────┤
│ + │ ${LogService-v6/LB/SecurityGroup.GroupId}      │ In  │ TCP 80     │ Everyone (IPv4)                                │
│ + │ ${LogService-v6/LB/SecurityGroup.GroupId}      │ Out │ TCP 8000   │ ${LogService-v6/Service/SecurityGroup.GroupId} │
├───┼────────────────────────────────────────────────┼─────┼────────────┼────────────────────────────────────────────────┤
│ + │ ${LogService-v6/Service/SecurityGroup.GroupId} │ In  │ TCP 8000   │ ${LogService-v6/LB/SecurityGroup.GroupId}      │
│ + │ ${LogService-v6/Service/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4)                                │
└───┴────────────────────────────────────────────────┴─────┴────────────┴────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)


Do you wish to deploy these changes (y/n)? y
AuditLogLogStack-v6: deploying... [2/2]
AuditLogLogStack-v6: creating CloudFormation changeset...

 ✅  AuditLogLogStack-v6

✨  Deployment time: 301.36s

Outputs:
AuditLogLogStack-v6.LogServicev6LoadBalancerDNS5F1305DC = LogService-v6-alb-1413408237.ap-northeast-1.elb.amazonaws.com
AuditLogLogStack-v6.LogServicev6ServiceURL3D43D34B = http://LogService-v6-alb-1413408237.ap-northeast-1.elb.amazonaws.com
Stack ARN:
arn:aws:cloudformation:ap-northeast-1:598540919918:stack/AuditLogLogStack-v6/880aa9f0-57b6-11f0-8647-0ecadcac3d45

✨  Total time: 322.15s
```
