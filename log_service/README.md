# Audit Log Service

A comprehensive audit logging service built with FastAPI, designed to track user actions and system events with multi-tenant support, real-time indexing, and export capabilities.

## Architecture

The service consists of three main components:

1. **API Service** (`main.py` / `api_run.py`) - FastAPI REST API for log management
2. **Log Consumer** (`consumer_log.py`) - Background service for indexing logs to OpenSearch
3. **Export Consumer** (`consumer_export.py`) - Background service for processing log exports

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL
- Redis (for caching)
- OpenSearch/Elasticsearch
- AWS S3 (or compatible storage)
- AWS SQS (or compatible message queue)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd log_service
   ```

2. **Install dependencies**

   ```bash
   # Using Poetry (recommended)
   poetry install

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

### Running the Services

#### 1. API Service

```bash
# Development mode
poetry run dev

# Or directly
python api_run.py

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### 2. Log Consumer

```bash
python consumer_log.py
```

#### 3. Export Consumer

```bash
python consumer_export.py
```

### Docker Deployment

```bash
# Build the image
docker build -t audit-log-service .

# Run the container
docker run -p 8000:8000 audit-log-service
```

## API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

All API endpoints require JWT authentication via Bearer token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### Health Check

```http
GET /health
```

Returns service health status.

#### Create Audit Log

```http
POST /logs
```

Create a single audit log entry.

**Request Body:**

```json
{
  "user_id": "user-123",
  "action": "LOGIN",
  "resource_type": "user",
  "resource_id": "user-456",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0",
  "metadata": { "source": "web" },
  "before_state": {},
  "after_state": { "status": "logged_in" },
  "severity": "INFO"
}
```

#### Bulk Create Audit Logs

```http
POST /logs/bulk
```

Create multiple audit log entries (max 100 per request).

**Request Body:**

```json
{
  "logs": [
    {
      "action": "CREATE",
      "resource_type": "document",
      "resource_id": "doc-123",
      "severity": "INFO"
    }
  ]
}
```

#### Get Audit Log

```http
GET /logs/{log_id}
```

Retrieve a specific audit log entry by ID.

#### List Audit Logs

```http
GET /logs?action=LOGIN&severity=INFO&page=1&page_size=10
```

List audit logs with filtering and pagination.

**Query Parameters:**

- `action` - Filter by action type
- `severity` - Filter by severity level
- `user_id` - Filter by user ID
- `search` - Full-text search
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 10, max: 100)

#### Get Audit Log Statistics

```http
GET /logs/stats
```

Get aggregated statistics about audit logs.

#### Export Logs

```http
POST /logs/export
```

Initiate a log export process.

#### Get Export Status

```http
GET /logs/export/{pipeline_id}
```

Check the status of an export pipeline.

#### Cleanup Old Logs

```http
DELETE /logs/cleanup
```

Remove old audit logs based on retention policy.

## Configuration

### Environment Variables

| Variable                | Description                  | Default                 |
| ----------------------- | ---------------------------- | ----------------------- |
| `DEBUG`                 | Enable debug mode            | `False`                 |
| `LOG_LEVEL`             | Logging level                | `INFO`                  |
| `TENANT_ID`             | Default tenant ID            | `1`                     |
| `DATABASE_URL`          | PostgreSQL connection string | Required                |
| `JWT_SECRET`            | JWT signing secret           | Required                |
| `JWT_ALGORITHM`         | JWT algorithm                | `HS256`                 |
| `AWS_ENDPOINT_URL`      | AWS endpoint URL             | `http://localhost:4566` |
| `AWS_ACCESS_KEY_ID`     | AWS access key               | `fake`                  |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key               | `fake`                  |
| `AWS_REGION`            | AWS region                   | `ap-southeast-1`        |
| `SQS_ENDPOINT`          | SQS endpoint URL             | `http://localhost:4566` |
| `SQS_LOG_QUEUE_URL`     | SQS log queue URL            | Required                |
| `SQS_EXPORT_QUEUE_URL`  | SQS export queue URL         | Required                |
| `EXPORT_S3_BUCKET`      | S3 bucket for exports        | `logs-export`           |
| `OPENSEARCH_HOST`       | OpenSearch host              | `http://localhost:9200` |
| `OPENSEARCH_PORT`       | OpenSearch port              | `9200`                  |
| `OPENSEARCH_USER`       | OpenSearch username          | `admin`                 |
| `OPENSEARCH_PASS`       | OpenSearch password          | `admin`                 |

## Project Structure

```
log_service/
├── alembic/                 # Database migrations
├── api/                     # API routes
│   └── logs.py             # Audit log endpoints
├── core/                    # Core functionality
│   ├── auth.py             # Authentication middleware
│   ├── config.py           # Configuration management
│   ├── db.py               # Database connection
│   ├── logging.py          # Logging setup
│   ├── openapi.py          # OpenAPI customization
│   └── response.py         # Response utilities
├── infra/                   # Infrastructure services
│   ├── opensearch.py       # OpenSearch client
│   ├── s3.py               # S3 operations
│   └── sqs.py              # SQS operations
├── models/                  # Database models
│   ├── audit_logs.py       # Audit log model
│   ├── export_pipeline.py  # Export pipeline model
│   └── base.py             # Base model
├── schemas/                 # Pydantic schemas
│   ├── schemas.py          # API schemas
│   └── base.py             # Base schemas
├── services/                # Business logic
│   ├── csv.py              # CSV export service
│   ├── export.py           # Export pipeline service
│   ├── logs.py             # Log management service
│   ├── masking.py          # Data masking service
│   └── search.py           # Search service
├── utils/                   # Utility functions
│   ├── strutils.py         # String utilities
│   ├── tenant.py           # Tenant utilities
│   └── token.py            # Token utilities
├── tests/                   # Test files
├── consumer_log.py          # Log consumer service
├── consumer_export.py       # Export consumer service
├── main.py                  # FastAPI application
├── api_run.py              # API runner
└── requirements.txt         # Python dependencies
```

## Data Flow

### 1. Log Creation Flow

```
Client Request → API → Database → SQS Queue → Consumer → OpenSearch
```

1. Client sends log creation request to API
2. API validates and stores log in PostgreSQL
3. API sends message to SQS log queue
4. Log consumer processes queue and indexes to OpenSearch

### 2. Export Flow

```
Client Request → API → Export Pipeline → SQS Queue → Consumer → CSV → S3
```

1. Client requests log export
2. API creates export pipeline record
3. API sends message to SQS export queue
4. Export consumer processes queue
5. Consumer generates CSV file
6. Consumer uploads file to S3
7. Consumer updates pipeline status

## Testing

### Test Coverage

The project maintains high test coverage with **97% overall coverage** across all modules:

```
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
api/logs.py                             70      5    93%
core/auth.py                            18      0   100%
core/config.py                          28      0   100%
core/db.py                              11      4    64%
core/logging.py                         18      0   100%
infra/opensearch.py                      4      1    75%
infra/sqs.py                            19      1    95%
services/logs.py                        33      9    73%
services/masking.py                     23      1    96%
services/search.py                      40      5    88%
utils/strutils.py                        6      0   100%
utils/tenant.py                          9      0   100%
--------------------------------------------------------
TOTAL                                  944     32    97%
```

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run with verbose output
pytest -v --cov

# Run specific test file
pytest tests/test_create_log_api.py

# Run tests in a specific directory
pytest tests/core/

# Run tests matching a pattern
pytest -k "test_create_log"

# Run tests with coverage report
pytest --cov=. --cov-report=html
```

### Test Structure

The test suite is organized into logical groups:

#### API Tests

- `tests/test_create_log_api.py` - Single log creation API tests
- `tests/test_bulk_create_logs_api.py` - Bulk log creation API tests
- `tests/test_export_log_data_api.py` - Export pipeline API tests
- `tests/test_export_result_api.py` - Export status API tests
- `tests/test_get_log_api.py` - Get log by ID API tests
- `tests/test_get_log_stats_api.py` - Log statistics API tests
- `tests/test_list_logs_api.py` - List logs with filtering API tests
- `tests/test_cleanup_logs_api.py` - Log cleanup API tests

#### Core Tests

- `tests/core/test_auth.py` - Authentication middleware tests

#### Service Tests

- `tests/service/test_logs.py` - Log management service tests
- `tests/service/test_export.py` - Export pipeline service tests
- `tests/service/test_masking.py` - Data masking service tests
- `tests/service/test_search.py` - Search and indexing service tests

#### Infrastructure Tests

- `tests/infrra/test_sqs.py` - SQS message queue tests

#### Utility Tests

- `tests/utils/test_strutils.py` - String utility tests
- `tests/utils/test_tenant.py` - Tenant utility tests

### Test Configuration

The project uses `pytest.ini` for test configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --disable-warnings
    --tb=short
```

### Test Dependencies

Testing dependencies are defined in `pyproject.toml`:

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.4.1"
httpx = "^0.28.1"
pytest-cov = "^6.2.1"
coverage = "^7.9.1"
```

### Mocking Strategy

The tests use comprehensive mocking to isolate units:

1. **Database mocking** - Mock database sessions and queries
2. **External service mocking** - Mock SQS, S3, and OpenSearch calls
3. **Authentication mocking** - Mock JWT token validation
4. **Dependency injection** - Override FastAPI dependencies

### Test Data Management

- **Fixtures** - Reusable test data and objects
- **Factory patterns** - Create test objects with realistic data
- **Cleanup** - Proper cleanup of test data and mocks

### Continuous Integration

Tests are automatically run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    poetry install
    poetry run pytest --cov=. --cov-report=xml
```

### Coverage Reports

Generate detailed coverage reports:

```bash
# HTML coverage report
pytest --cov=. --cov-report=html
# Open coverage/index.html in browser

# XML coverage report (for CI)
pytest --cov=. --cov-report=xml

# Terminal coverage report
pytest --cov=. --cov-report=term-missing
```

### Best Practices

1. **Test naming** - Use descriptive test names that explain the scenario
2. **Arrange-Act-Assert** - Structure tests with clear sections
3. **Mock external dependencies** - Don't rely on external services in unit tests
4. **Test edge cases** - Include tests for error conditions and boundary values
5. **Keep tests fast** - Unit tests should run quickly
6. **Maintain test data** - Use realistic but minimal test data
7. **Clean up resources** - Ensure proper cleanup after each test

### Debugging Tests

```bash
# Run tests with debug output
pytest -v -s

# Run specific test with debugger
pytest tests/test_create_log_api.py::test_create_log_api_success -s

# Run tests with print statements
pytest -s

# Run tests and stop on first failure
pytest -x
```

### Test Results Summary

Current test suite includes **34 tests** with the following breakdown:

- **API Tests**: 8 test files covering all endpoints
- **Core Tests**: 1 test file for authentication
- **Service Tests**: 4 test files for business logic
- **Infrastructure Tests**: 1 test file for external services
- **Utility Tests**: 2 test files for helper functions

**Test Results**: ✅ All 34 tests passing
**Coverage**: 97% overall coverage
**Warnings**: 21 deprecation warnings (mostly Pydantic v2 migration)

## Monitoring

### Health Checks

- API health: `GET /health`
- Database connectivity
- OpenSearch connectivity
- SQS queue status

### Logging

The service uses structured logging with different loggers:

- `api_logger` - API request/response logs
- `consumer_log_consumer_logger` - Consumer service logs
- `s3_logger` - S3 operation logs

### Metrics

Consider integrating with:

- Prometheus for metrics collection
- Grafana for visualization
- AWS CloudWatch for AWS-specific metrics

## Security

### Authentication

- JWT-based authentication
- Tenant isolation
- Request validation

### Data Protection

- Sensitive data masking
- Input sanitization
- SQL injection prevention

### Access Control

- Tenant-based data isolation
- Role-based access control (can be extended)

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

### Scaling

- Horizontal scaling for API services
- Multiple consumer instances
- Load balancing
- Auto-scaling based on queue depth

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License
