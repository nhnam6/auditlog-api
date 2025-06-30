# AuditLog API System

A comprehensive multi-tenant audit logging system built with FastAPI, designed to track user actions and system events with real-time indexing, export capabilities, and secure authentication.

## System Architecture

The AuditLog API system consists of three main components:

### 1. **Auth Service** (`auth_service/`)
- JWT-based authentication and authorization
- Multi-tenant user management
- Role-based access control (Admin/User)
- Tenant creation and management

### 2. **Log Service** (`log_service/`)
- Audit log creation and management
- Real-time indexing to OpenSearch
- Log search and filtering
- Export functionality with S3 storage
- Background processing with SQS

### 3. **Infrastructure Services**
- **PostgreSQL** - Primary data storage
- **OpenSearch** - Full-text search and analytics
- **AWS S3** - File storage for exports
- **AWS SQS** - Message queuing for background processing

## Quick Start

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- PostgreSQL
- OpenSearch/Elasticsearch
- AWS S3 (or compatible storage)
- AWS SQS (or compatible message queue)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auditlog-api
   ```

2. **Start infrastructure services**
   ```bash
   docker-compose up -d
   ```

3. **Set up Auth Service**
   ```bash
   cd auth_service
   poetry install
   cp .env.example .env
   # Edit .env with your configuration
   poetry run alembic upgrade head
   poetry run python api_run.py
   ```

4. **Set up Log Service**
   ```bash
   cd ../log_service
   poetry install
   cp .env.example .env
   # Edit .env with your configuration
   poetry run alembic upgrade head
   poetry run python api_run.py
   ```

5. **Start background consumers**
   ```bash
   # In log_service directory
   python consumer_log.py &
   python consumer_export.py &
   ```

## Documentation

### Service Documentation
- **[Auth Service Documentation](auth_service/README.md)** - Authentication, user management, and tenant operations
- **[Log Service Documentation](log_service/README.md)** - Audit logging, search, and export functionality
- **[Postman Collection Documentation](postman/README.md)** - API testing and examples
- **[Infrastructure Deployment Guide](cdk/auditlog_infra/DEPLOYMENT.md)**

### API Documentation
Once services are running, access the interactive API documentation:
- **Auth Service API**: http://localhost:8001/docs
- **Log Service API**: http://localhost:8000/docs

## Configuration

### Environment Variables

#### Auth Service
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `JWT_SECRET` | JWT signing secret | - | Yes |
| `JWT_ALGORITHM` | JWT algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 60 | No |

#### Log Service
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `JWT_SECRET` | JWT signing secret | - | Yes |
| `OPENSEARCH_HOST` | OpenSearch host | localhost:9200 | No |
| `AWS_ENDPOINT_URL` | AWS endpoint URL | http://localhost:4566 | No |
| `SQS_LOG_QUEUE_URL` | SQS log queue URL | - | Yes |
| `SQS_EXPORT_QUEUE_URL` | SQS export queue URL | - | Yes |
| `EXPORT_S3_BUCKET` | S3 bucket for exports | logs-export | No |

## Testing

### Running Tests

```bash
# Auth Service Tests
cd auth_service
poetry run pytest --cov=. --cov-report=html

# Log Service Tests
cd ../log_service
poetry run pytest --cov=. --cov-report=html
```

### Test Coverage
- **Auth Service**: 94% coverage
- **Log Service**: 97% coverage

## Monitoring

### Health Checks
- **Auth Service**: `GET http://localhost:8001/health`
- **Log Service**: `GET http://localhost:8000/health`

## Security Features

- **JWT Authentication** - Secure token-based authentication
- **Multi-tenant Isolation** - Complete data separation between tenants
- **Role-based Access Control** - Admin and user roles with different permissions
- **Password Hashing** - Bcrypt with salt for secure password storage
- **Input Validation** - Pydantic schema validation for all inputs
- **SQL Injection Protection** - SQLAlchemy ORM with parameterized queries

## Deployment

### Production Considerations

1. **Database**
   - Use connection pooling
   - Set up read replicas for heavy read loads
   - Implement proper backup strategy

2. **Message Queues**
   - Use AWS SQS or RabbitMQ in production
   - Set up dead letter queues
   - Monitor queue depth

3. **Search**
   - Use managed OpenSearch/Elasticsearch
   - Configure proper indexing strategy
   - Set up monitoring and alerting

4. **Storage**
   - Use S3 or compatible object storage
   - Implement lifecycle policies
   - Set up proper access controls

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.yml up -d

# Or build individual services
docker build -t auth-service auth_service/
docker build -t log-service log_service/
```

## Project Structure

```
auditlog-api/
├── auth_service/           # Authentication and user management
│   ├── alembic/           # Database migrations
│   ├── tests/             # Test files
│   ├── main.py            # FastAPI application
│   ├── api_run.py         # Development server
│   └── README.md          # Service documentation
├── log_service/           # Audit logging and search
│   ├── alembic/           # Database migrations
│   ├── api/               # API routes
│   ├── core/              # Core functionality
│   ├── services/          # Business logic
│   ├── tests/             # Test files
│   ├── consumer_log.py    # Log indexing consumer
│   ├── consumer_export.py # Export processing consumer
│   ├── main.py            # FastAPI application
│   └── README.md          # Service documentation
├── postman/               # API testing collection
│   ├── AuditLog.postman_collection.json
│   ├── Local.postman_environment.json
│   └── README.md          # Collection documentation
├── scripts/               # Utility scripts
├── docker-compose.yml     # Infrastructure services
└── README.md              # This file
```

**Note**: This is a development version. For production deployment, ensure proper security configurations and environment setup.

```sql
INSERT INTO users (uid, email, hashed_password, role, created_at)
VALUES (
    '95735f15-c28d-44df-8091-1b047670b02a',
    'admin@example.com',
    '$2b$12$08tYrXcgGrsdEgZ16l7yWeXvyRudgpL1gdVWmPkiElf7ao1Hxg9TC', --admin123
    'admin',
    now()
);
```
