# Database Setup Guide

This guide explains how to set up the databases and create the initial admin user for the AuditLog API system.

## Overview

The AuditLog API system uses PostgreSQL with the following databases:
- **master_db**: Main database for system management
- **auth_service**: Database for authentication and user management
- **log_service**: Database for audit log storage

## Database Architecture

```
PostgreSQL Instance
├── master_db (system management)
├── auth_service (authentication)
│   ├── users (user accounts)
│   ├── tenants (tenant management)
│   └── alembic_version (migrations)
└── log_service (audit logs)
    ├── audit_logs (log entries)
    ├── export_pipelines (export jobs)
    └── alembic_version (migrations)
```

## 👤 Admin User Creation

If you need to create the admin user manually:

#### Step 1: Connect to the auth_service database

```bash
psql -h localhost -U admin -d auth_service
```

#### Step 2: Create the admin user

```sql
-- Create admin user with bcrypt hashed password
INSERT INTO users (uid, email, hashed_password, role, created_at)
VALUES (
    '95735f15-c28d-44df-8091-1b047670b02a',
    'admin@example.com',
    '$2b$12$08tYrXcgGrsdEgZ16l7yWeXvyRudgpL1gdVWmPkiElf7ao1Hxg9TC', --admin123
    'admin',
    now()
);
```

#### Step 3: Verify the user was created

```sql
-- Check if admin user exists
SELECT uid, email, role, created_at FROM users WHERE email = 'admin@example.com';
```

## Password Information

### Admin User Credentials
- **Email**: `admin@example.com`
- **Password**: `admin123`
- **Role**: `admin`

### Password Hash Details
The password `admin123` is hashed using bcrypt with:
- **Algorithm**: bcrypt
- **Cost Factor**: 12
- **Salt**: Automatically generated
- **Hash**: `$2b$12$S9h/mGislH0PemmiNZ7Hau5xHpQE5b3lX5V1VhTtQDCBWs1vsyx5G`

### Generate New Password Hash

To create a new password hash:

```bash
# Using Python
python3 -c "
import bcrypt
password = 'your_new_password'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
print(hashed.decode('utf-8'))
"

# Using the utility function in the project
cd auth_service
poetry run python -c "
from utils import hash_password
print(hash_password('your_new_password'))
"
```

## Database Schema

### Auth Service Database

#### Users Table
```sql
CREATE TABLE users (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    tenant_id UUID REFERENCES tenants(tid),
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Tenants Table
```sql
CREATE TABLE tenants (
    tid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Log Service Database

#### Audit Logs Table
```sql
CREATE TABLE audit_logs (
    alid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    user_id VARCHAR(255),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    ip_address INET,
    user_agent TEXT,
    metadata JSONB,
    before_state JSONB,
    after_state JSONB,
    severity VARCHAR(20) DEFAULT 'INFO',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Export Pipelines Table
```sql
CREATE TABLE export_pipelines (
    epid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    filters JSONB,
    file_path VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Database Migrations

### Running Migrations

```bash
# Auth Service migrations
cd auth_service
poetry run alembic upgrade head

# Log Service migrations
cd ../log_service
poetry run alembic upgrade head
```

### Creating New Migrations

```bash
# Auth Service
cd auth_service
poetry run alembic revision --autogenerate -m "Description of changes"
poetry run alembic upgrade head

# Log Service
cd ../log_service
poetry run alembic revision --autogenerate -m "Description of changes"
poetry run alembic upgrade head
```

## Environment Variables

### Required Database Variables

```bash
# PostgreSQL Configuration
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin123
POSTGRES_DB=master_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Service Database URLs
AUTH_SERVICE_DATABASE_URL=postgresql://admin:admin123@localhost:5432/auth_service
LOG_SERVICE_DATABASE_URL=postgresql://admin:admin123@localhost:5432/log_service
```
