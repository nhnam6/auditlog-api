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

## Deployment Process

### Step 1: Create Required Secrets

Before deploying the stacks, create the necessary secrets in AWS Secrets Manager:

#### Authentication Secrets
```bash
# Create JWT secret for authentication
aws --profile test secretsmanager create-secret \
    --name auth/jwt-secret \
    --secret-string "your-secure-jwt-secret-here"

# Create database URL secret for auth service
aws --profile test secretsmanager create-secret \
    --name auth/database-url \
    --secret-string "postgresql://username:password@host:port/database"
```

#### Log Service Secrets
```bash
# Create JWT secret for log
aws --profile test secretsmanager create-secret \
    --name log/jwt-secret \
    --secret-string "your-secure-jwt-secret-here"

# Create database URL secret for log service
aws --profile test secretsmanager create-secret \
    --name log/database-url \
    --secret-string "postgresql://username:password@host:port/database"

# Create AWS access key secret
aws --profile test secretsmanager create-secret \
    --name log/aws-access-key-id \
    --secret-string "your-actual-access-key-id"

# Create AWS secret access key secret
aws --profile test secretsmanager create-secret \
    --name log/aws-secret-access-key \
    --secret-string "your-actual-secret-access-key"

# Create OpenSearch username secret
aws --profile test secretsmanager create-secret \
    --name log/opensearch-user \
    --secret-string "your-opensearch-username"

# Create OpenSearch password secret
aws --profile test secretsmanager create-secret \
    --name log/opensearch-pass \
    --secret-string "your-secure-opensearch-password"
```

### Step 2: Deploy Main Stack

The main stack contains the authentication service and shared infrastructure:

```bash
cdk deploy AuditlogMainStack --profile test
```

**What gets deployed:**
- VPC with public and private subnets
- RDS PostgreSQL instance (MasterDB)
- ECS Cluster
- Application Load Balancer
- Auth Service (Fargate)
- Security Groups and IAM roles


Result:
```bash

✨  Synthesis time: 11.25s

AuditlogMainStack: start: Building AuditlogMainStack Template
AuditlogMainStack: success: Built AuditlogMainStack Template
AuditlogMainStack: start: Publishing AuditlogMainStack Template (598540919918-ap-northeast-1)
AuditlogMainStack: success: Published AuditlogMainStack Template (598540919918-ap-northeast-1)
Stack AuditlogMainStack
IAM Statement Changes
┌───┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────┬───────────────────────────────────┬────────────────────────────────────────────────────────────────┬───────────┐
│   │ Resource                                                                                                      │ Effect │ Action                            │ Principal                                                      │ Condition │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${AuthService/TaskDef/ExecutionRole.Arn}                                                                      │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${AuthService/TaskDef/TaskRole.Arn}                                                                           │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${AuthService/TaskDef/web/LogGroup.Arn}                                                                       │ Allow  │ logs:CreateLogStream              │ AWS:${AuthService/TaskDef/ExecutionRole}                       │           │
│   │                                                                                                               │        │ logs:PutLogEvents                 │                                                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role.Arn}                                                │ Allow  │ sts:AssumeRole                    │ Service:lambda.amazonaws.com                                   │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken         │ AWS:${AuthService/TaskDef/ExecutionRole}                       │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ec2:ap-northeast-1:598540919918:security-group/${MainVpc.DefaultSecurityGroup}                        │ Allow  │ ec2:AuthorizeSecurityGroupEgress  │ AWS:${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │           │
│   │                                                                                                               │        │ ec2:AuthorizeSecurityGroupIngress │                                                                │           │
│   │                                                                                                               │        │ ec2:RevokeSecurityGroupEgress     │                                                                │           │
│   │                                                                                                               │        │ ec2:RevokeSecurityGroupIngress    │                                                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability   │ AWS:${AuthService/TaskDef/ExecutionRole}                       │           │
│   │                                                                                                               │        │ ecr:BatchGetImage                 │                                                                │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer        │                                                                │           │
└───┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴───────────────────────────────────┴────────────────────────────────────────────────────────────────┴───────────┘
IAM Policy Changes
┌───┬────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                   │ Managed Policy ARN                                                                           │
├───┼────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"} │
└───┴────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬──────────────────────────────────────────────┬─────┬────────────┬──────────────────────────────────────────────┐
│   │ Group                                        │ Dir │ Protocol   │ Peer                                         │
├───┼──────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────┤
│ + │ ${AuthService/LB/SecurityGroup.GroupId}      │ In  │ TCP 80     │ Everyone (IPv4)                              │
│ + │ ${AuthService/LB/SecurityGroup.GroupId}      │ Out │ TCP 80     │ ${AuthService/Service/SecurityGroup.GroupId} │
├───┼──────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────┤
│ + │ ${AuthService/Service/SecurityGroup.GroupId} │ In  │ TCP 80     │ ${AuthService/LB/SecurityGroup.GroupId}      │
│ + │ ${AuthService/Service/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4)                              │
├───┼──────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────┤
│ + │ ${MasterDB/SecurityGroup.GroupId}            │ Out │ Everything │ Everyone (IPv4)                              │
└───┴──────────────────────────────────────────────┴─────┴────────────┴──────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)
```


### Step 3: Deploy Tenant Stack

The tenant stack contains tenant-specific infrastructure:

```bash
cdk deploy AuditlogTenantStack --profile test
```

Result:

```bash
✨  Synthesis time: 19.07s

AuditlogTenantStack: start: Building AuditlogTenantStack Template
AuditlogTenantStack: success: Built AuditlogTenantStack Template
AuditlogTenantStack: start: Building LogService/TaskDef/web/AssetImage
AuditlogTenantStack: start: Publishing AuditlogTenantStack Template (598540919918-ap-northeast-1)
AuditlogTenantStack: success: Published AuditlogTenantStack Template (598540919918-ap-northeast-1)
#0 building with "desktop-linux" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 268B 0.0s done
#1 DONE 0.1s

#2 [internal] load metadata for docker.io/library/python:3.12-slim
#2 DONE 2.3s

#3 [internal] load .dockerignore
#3 transferring context: 321B done
#3 DONE 0.0s

#4 [1/5] FROM docker.io/library/python:3.12-slim@sha256:e55523f127124e5edc03ba201e3dbbc85172a2ec40d8651ac752364b23dfd733
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 89.89MB 3.8s done
#5 DONE 3.9s

#6 [2/5] WORKDIR /app
#6 CACHED

#7 [3/5] COPY ./requirements.txt .
#7 CACHED

#8 [4/5] RUN pip install --no-cache-dir -r requirements.txt
#8 CACHED

#9 [5/5] COPY . .
#9 DONE 2.2s

#10 exporting to image
#10 exporting layers
#10 exporting layers 0.9s done
#10 writing image sha256:9b58e17144fb8246a32d78b15bd4c2a5997ff2117bc36aa7b62adf7c614f3481 done
#10 naming to docker.io/library/cdkasset-99737137e750a28963633708357a11bf8176e8f1f444b38396dde2494c47979d done
#10 DONE 1.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/u7lw7igvtrh0p9yw8phgfis4b
AuditlogTenantStack: success: Built LogService/TaskDef/web/AssetImage
AuditlogTenantStack: start: Publishing LogService/TaskDef/web/AssetImage (598540919918-ap-northeast-1)
The push refers to repository [598540919918.dkr.ecr.ap-northeast-1.amazonaws.com/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1]
cc9dbe093b19: Preparing
7768f5d05722: Preparing
e289f5ec9b95: Preparing
b9ad8f249f22: Preparing
e7fd3ca5b4d3: Preparing
5eaadadb6079: Preparing
7b35846aeec0: Preparing
7fb72a7d1a8e: Preparing
5eaadadb6079: Waiting
7b35846aeec0: Waiting
7fb72a7d1a8e: Waiting
b9ad8f249f22: Layer already exists
e7fd3ca5b4d3: Layer already exists
5eaadadb6079: Layer already exists
7b35846aeec0: Layer already exists
7fb72a7d1a8e: Layer already exists
e289f5ec9b95: Pushed
cc9dbe093b19: Pushed
7768f5d05722: Pushed
99737137e750a28963633708357a11bf8176e8f1f444b38396dde2494c47979d: digest: sha256:0bbd3da343570471dbcd1fe07168f4d6b0ad3321ef41ac5c0f0d6f69f0075b79 size: 1996
AuditlogTenantStack: success: Published LogService/TaskDef/web/AssetImage (598540919918-ap-northeast-1)
Stack AuditlogTenantStack
IAM Statement Changes
┌───┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────┬────────┬───────────────────────────────────┬────────────────────────────────────────────────────────────────┬───────────┐
│   │ Resource                                                                                                      │ Effect │ Action                            │ Principal                                                      │ Condition │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role.Arn}                                                │ Allow  │ sts:AssumeRole                    │ Service:lambda.amazonaws.com                                   │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${ExportConsumerTask/ExecutionRole.Arn}                                                                       │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${ExportConsumerTask/ExportConsumerContainer/LogGroup.Arn}                                                    │ Allow  │ logs:CreateLogStream              │ AWS:${ExportConsumerTask/ExecutionRole}                        │           │
│   │                                                                                                               │        │ logs:PutLogEvents                 │                                                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${ExportConsumerTask/TaskRole.Arn}                                                                            │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${LogConsumerTask/ExecutionRole.Arn}                                                                          │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${LogConsumerTask/LogConsumerContainer/LogGroup.Arn}                                                          │ Allow  │ logs:CreateLogStream              │ AWS:${LogConsumerTask/ExecutionRole}                           │           │
│   │                                                                                                               │        │ logs:PutLogEvents                 │                                                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${LogConsumerTask/TaskRole.Arn}                                                                               │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${LogService/TaskDef/ExecutionRole.Arn}                                                                       │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${LogService/TaskDef/TaskRole.Arn}                                                                            │ Allow  │ sts:AssumeRole                    │ Service:ecs-tasks.amazonaws.com                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ ${LogService/TaskDef/web/LogGroup.Arn}                                                                        │ Allow  │ logs:CreateLogStream              │ AWS:${LogService/TaskDef/ExecutionRole}                        │           │
│   │                                                                                                               │        │ logs:PutLogEvents                 │                                                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken         │ AWS:${LogService/TaskDef/ExecutionRole}                        │           │
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken         │ AWS:${LogConsumerTask/ExecutionRole}                           │           │
│ + │ *                                                                                                             │ Allow  │ ecr:GetAuthorizationToken         │ AWS:${ExportConsumerTask/ExecutionRole}                        │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ec2:ap-northeast-1:598540919918:security-group/${TenantVpc.DefaultSecurityGroup}                      │ Allow  │ ec2:AuthorizeSecurityGroupEgress  │ AWS:${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │           │
│   │                                                                                                               │        │ ec2:AuthorizeSecurityGroupIngress │                                                                │           │
│   │                                                                                                               │        │ ec2:RevokeSecurityGroupEgress     │                                                                │           │
│   │                                                                                                               │        │ ec2:RevokeSecurityGroupIngress    │                                                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability   │ AWS:${LogService/TaskDef/ExecutionRole}                        │           │
│   │                                                                                                               │        │ ecr:BatchGetImage                 │                                                                │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer        │                                                                │           │
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability   │ AWS:${LogConsumerTask/ExecutionRole}                           │           │
│   │                                                                                                               │        │ ecr:BatchGetImage                 │                                                                │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer        │                                                                │           │
│ + │ arn:aws:ecr:ap-northeast-1:598540919918:repository/cdk-hnb659fds-container-assets-598540919918-ap-northeast-1 │ Allow  │ ecr:BatchCheckLayerAvailability   │ AWS:${ExportConsumerTask/ExecutionRole}                        │           │
│   │                                                                                                               │        │ ecr:BatchGetImage                 │                                                                │           │
│   │                                                                                                               │        │ ecr:GetDownloadUrlForLayer        │                                                                │           │
├───┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────┼───────────────────────────────────┼────────────────────────────────────────────────────────────────┼───────────┤
│ + │ arn:aws:secretsmanager:ap-northeast-1:598540919918:secret:auth/database-url-??????                            │ Allow  │ secretsmanager:DescribeSecret     │ AWS:${LogService/TaskDef/ExecutionRole}                        │           │
│   │ arn:aws:secretsmanager:ap-northeast-1:598540919918:secret:auth/jwt-secret-??????                              │        │ secretsmanager:GetSecretValue     │                                                                │           │
│ + │ arn:aws:secretsmanager:ap-northeast-1:598540919918:secret:auth/database-url-??????                            │ Allow  │ secretsmanager:DescribeSecret     │ AWS:${LogConsumerTask/ExecutionRole}                           │           │
│   │ arn:aws:secretsmanager:ap-northeast-1:598540919918:secret:auth/jwt-secret-??????                              │        │ secretsmanager:GetSecretValue     │                                                                │           │
│ + │ arn:aws:secretsmanager:ap-northeast-1:598540919918:secret:auth/database-url-??????                            │ Allow  │ secretsmanager:DescribeSecret     │ AWS:${ExportConsumerTask/ExecutionRole}                        │           │
│   │ arn:aws:secretsmanager:ap-northeast-1:598540919918:secret:auth/jwt-secret-??????                              │        │ secretsmanager:GetSecretValue     │                                                                │           │
└───┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────┴────────┴───────────────────────────────────┴────────────────────────────────────────────────────────────────┴───────────┘
IAM Policy Changes
┌───┬────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                   │ Managed Policy ARN                                                                           │
├───┼────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────┤
│ + │ ${Custom::VpcRestrictDefaultSGCustomResourceProvider/Role} │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"} │
└───┴────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬────────────────────────────────────────────────┬─────┬────────────┬─────────────────────────────────────────────┐
│   │ Group                                          │ Dir │ Protocol   │ Peer                                        │
├───┼────────────────────────────────────────────────┼─────┼────────────┼─────────────────────────────────────────────┤
│ + │ ${ExportConsumerService/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4)                             │
├───┼────────────────────────────────────────────────┼─────┼────────────┼─────────────────────────────────────────────┤
│ + │ ${LogConsumerService/SecurityGroup.GroupId}    │ Out │ Everything │ Everyone (IPv4)                             │
├───┼────────────────────────────────────────────────┼─────┼────────────┼─────────────────────────────────────────────┤
│ + │ ${LogService/LB/SecurityGroup.GroupId}         │ In  │ TCP 80     │ Everyone (IPv4)                             │
│ + │ ${LogService/LB/SecurityGroup.GroupId}         │ Out │ TCP 80     │ ${LogService/Service/SecurityGroup.GroupId} │
├───┼────────────────────────────────────────────────┼─────┼────────────┼─────────────────────────────────────────────┤
│ + │ ${LogService/Service/SecurityGroup.GroupId}    │ In  │ TCP 80     │ ${LogService/LB/SecurityGroup.GroupId}      │
│ + │ ${LogService/Service/SecurityGroup.GroupId}    │ Out │ Everything │ Everyone (IPv4)                             │
├───┼────────────────────────────────────────────────┼─────┼────────────┼─────────────────────────────────────────────┤
│ + │ ${TenantDB/SecurityGroup.GroupId}              │ Out │ Everything │ Everyone (IPv4)                             │
└───┴────────────────────────────────────────────────┴─────┴────────────┴─────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)
```
