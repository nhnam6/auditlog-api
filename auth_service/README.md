# Auth Service

A FastAPI-based authentication service for multi-tenant applications with JWT token authentication and role-based access control.

## Features

- 🔐 JWT-based authentication
- 🏢 Multi-tenant support
- 👥 Role-based access control (Admin/User)
- 🔒 Secure password hashing with bcrypt
- 📄 Pagination support
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 📝 Comprehensive API documentation
- 🧪 Unit tests with pytest
- 📈 Code coverage reporting

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: bcrypt
- **Package Management**: Poetry
- **Testing**: pytest
- **Code Quality**: Black, isort, flake8
- **Database Migrations**: Alembic

## Prerequisites

- Python 3.12+
- PostgreSQL
- Poetry

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd auth_service
   ```

2. **Install dependencies**

   ```bash
   poetry install
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:

   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/auth_service
   JWT_SECRET=your-super-secret-jwt-key-here
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   DEBUG=False
   ```

4. **Generate JWT secret**

   ```bash
   python -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(32))"
   ```

5. **Set up the database**
   ```bash
   # Run database migrations
   poetry run alembic upgrade head
   ```

## Running the Application

### Development

```bash
# Start the development server
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production

```bash
# Start the production server
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication

#### POST `/api/v1/login`

Login to get an access token.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**

```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tenant_id": "tenant-uuid",
    "token_type": "bearer"
  }
}
```

### Tenants (Admin Only)

#### GET `/api/v1/tenants`

Get all tenants with pagination.

**Query Parameters:**

- `page` (int): Page number (default: 1)
- `page_size` (int): Items per page (default: 10, max: 100)

**Headers:**

```
Authorization: Bearer <admin-token>
```

#### POST `/api/v1/tenants`

Create a new tenant (Admin only).

**Request:**

```json
{
  "name": "new-tenant",
  "email": "admin@newtenant.com",
  "password": "securepassword123"
}
```

**Headers:**

```
Authorization: Bearer <admin-token>
```

### Health Check

#### GET `/health`

Check service health status.

**Response:**

```json
{
  "status": "ok",
  "message": "Service is healthy"
}
```

## Database Schema

### Users Table

- `uid` (UUID): Primary key
- `email` (String): Unique email address
- `hashed_password` (String): Bcrypt hashed password
- `tenant_id` (UUID): Foreign key to tenants
- `role` (String): User role (admin/user)
- `created_at` (DateTime): Creation timestamp

### Tenants Table

- `tid` (UUID): Primary key
- `name` (String): Unique tenant name
- `created_at` (DateTime): Creation timestamp

## Testing

### Test Coverage

Current test coverage: **94%** (219 statements, 13 missed)

| Module              | Statements | Missed | Coverage |
| ------------------- | ---------- | ------ | -------- |
| `api_run.py`        | 2          | 2      | 0%       |
| `auth.py`           | 18         | 3      | 83%      |
| `config.py`         | 14         | 0      | 100%     |
| `db.py`             | 11         | 4      | 64%      |
| `dependencies.py`   | 9          | 0      | 100%     |
| `logger.py`         | 15         | 0      | 100%     |
| `main.py`           | 39         | 4      | 90%      |
| `models.py`         | 22         | 0      | 100%     |
| `response.py`       | 7          | 0      | 100%     |
| `schemas.py`        | 31         | 0      | 100%     |
| `tenant_service.py` | 22         | 0      | 100%     |
| `user_service.py`   | 4          | 0      | 100%     |
| `utils.py`          | 25         | 0      | 100%     |

### Test Categories

#### 1. API Tests (`tests/test_*.py`)

- **Health API Tests** (`test_health_api.py`)

  - Health check endpoint functionality
  - Response structure validation
  - Content type verification

- **Login API Tests** (`test_login_api.py`)

  - Authentication success/failure scenarios
  - Invalid credentials handling
  - Response format validation

- **Tenant API Tests** (`test_tenant_api.py`)
  - Tenant CRUD operations
  - Authorization (admin vs user roles)
  - Pagination functionality
  - Input validation
  - Error handling

#### 2. Utility Tests (`tests/test_utils.py`)

- **Password Functions** (`TestPasswordFunctions`)

  - Password hashing and verification
  - Salt generation and uniqueness
  - Special characters and unicode support
  - Edge cases (empty strings, very long passwords)

- **Token Functions** (`TestTokenFunctions`)

  - JWT token creation and verification
  - Token expiration handling
  - Complex data structures in tokens
  - Error scenarios (invalid tokens, wrong secrets)

- **Integration Tests** (`TestIntegration`)

  - Complete authentication flow
  - Password hash consistency
  - Token expiry behavior

- **Edge Cases** (`TestEdgeCases`)
  - None inputs handling
  - Malformed tokens
  - Error conditions

### Running Tests

#### Basic Test Commands

```bash
# Run all tests
poetry run pytest

# Run with verbose output
poetry run pytest -v

# Run with coverage report
poetry run pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
poetry run pytest --cov=. --cov-report=html

# Generate XML coverage report (for CI/CD)
poetry run pytest --cov=. --cov-report=xml
```

#### Running Specific Tests

```bash
# Run specific test file
poetry run pytest tests/test_login_api.py

# Run specific test class
poetry run pytest tests/test_utils.py::TestPasswordFunctions

# Run specific test method
poetry run pytest tests/test_utils.py::TestPasswordFunctions::test_hash_password_returns_string

# Run tests matching a pattern
poetry run pytest -k "password"

# Run tests excluding certain patterns
poetry run pytest -k "not slow"
```

#### Test Configuration

The project uses `pytest.ini` for test configuration:

```ini
[tool:pytest]
addopts =
    --cov=.
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=80
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### Test Best Practices

1. **Test Isolation**: Each test should be independent
2. **Descriptive Names**: Use clear, descriptive test names
3. **Arrange-Act-Assert**: Structure tests in three phases
4. **Mock External Dependencies**: Use mocks for external services
5. **Test Edge Cases**: Include boundary conditions and error scenarios
6. **Coverage Goals**: Maintain at least 80% code coverage

### Continuous Integration

Tests are configured to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    poetry install
    poetry run pytest --cov=. --cov-report=xml
    poetry run coverage report --fail-under=80
```

### Debugging Tests

#### Verbose Output

```bash
poetry run pytest -v -s
```

#### Debug Specific Test

```bash
poetry run pytest tests/test_login_api.py::test_login_success -v -s --pdb
```

#### Show Local Variables

```bash
poetry run pytest --tb=short
```

### Performance Testing

For performance testing, you can add:

```python
import time

def test_api_response_time():
    """Test API response time"""
    start_time = time.time()
    response = client.get("/health")
    end_time = time.time()

    assert response.status_code == 200
    assert (end_time - start_time) < 0.1  # Response time < 100ms
```

### Test Data Management

Use factories for test data:

```python
from factory import Factory, Faker
from models import User, Tenant

class UserFactory(Factory):
    class Meta:
        model = User

    email = Faker('email')
    hashed_password = hash_password('password123')
    role = 'user'

# Usage in tests
user = UserFactory()
```

### Coverage Reports

After running tests with coverage, you can:

1. **View HTML Report**: Open `htmlcov/index.html` in browser
2. **Check Missing Lines**: Look at `--cov-report=term-missing` output
3. **Set Coverage Thresholds**: Configure minimum coverage requirements

### Test Maintenance

Regular test maintenance tasks:

1. **Update Tests**: When API changes, update corresponding tests
2. **Remove Obsolete Tests**: Delete tests for removed functionality
3. **Refactor Common Code**: Extract shared test utilities
4. **Monitor Coverage**: Track coverage trends over time

## Code Quality

### Format code

```bash
poetry run black .
poetry run isort .
```

### Lint code

```bash
poetry run flake8
```

## Database Migrations

### Create a new migration

```bash
poetry run alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
poetry run alembic upgrade head
```

### Rollback migration

```bash
poetry run alembic downgrade -1
```

## Environment Variables

| Variable                      | Description                  | Default | Required |
| ----------------------------- | ---------------------------- | ------- | -------- |
| `DATABASE_URL`                | PostgreSQL connection string | -       | Yes      |
| `JWT_SECRET`                  | Secret key for JWT tokens    | -       | Yes      |
| `JWT_ALGORITHM`               | JWT algorithm                | HS256   | No       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time        | 60      | No       |
| `DEBUG`                       | Debug mode                   | False   | No       |
| `LOG_LEVEL`                   | Logging level                | INFO    | No       |

## Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: Admin and user roles
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Protection**: Configurable CORS middleware

## Project Structure

```
auth_service/
├── alembic/                 # Database migrations
├── tests/                   # Test files
│   ├── test_login_api.py
│   ├── test_health_api.py
│   └── test_utils.py
├── auth.py                  # Authentication middleware
├── config.py               # Configuration settings
├── db.py                   # Database connection
├── dependencies.py         # FastAPI dependencies
├── logger.py               # Logging configuration
├── main.py                 # FastAPI application
├── models.py               # SQLAlchemy models
├── response.py             # Response utilities
├── schemas.py              # Pydantic schemas
├── tenant_service.py       # Tenant business logic
├── user_service.py         # User business logic
├── utils.py                # Utility functions
├── pyproject.toml          # Poetry configuration
└── README.md               # This file
```

## Usage Examples

### Creating an Admin User

1. **Create a tenant with admin user**

   ```bash
   curl -X POST "http://localhost:8000/api/v1/tenants" \
     -H "Authorization: Bearer <admin-token>" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "my-company",
       "email": "admin@mycompany.com",
       "password": "SecurePass123"
     }'
   ```

2. **Login as admin**

   ```bash
   curl -X POST "http://localhost:8000/api/v1/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@mycompany.com",
       "password": "SecurePass123"
     }'
   ```

3. **Use the token for authenticated requests**
   ```bash
   curl -X GET "http://localhost:8000/api/v1/tenants" \
     -H "Authorization: Bearer <your-token>"
   ```

### Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid credentials)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `422`: Validation Error (invalid input)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Workflow

1. **Set up development environment**

   ```bash
   poetry install
   ```

2. **Create feature branch**

   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes and test**

   ```bash
   poetry run pytest
   poetry run black .
   poetry run isort .
   poetry run flake8
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

## Troubleshooting

### Common Issues

1. **Database connection error**

   - Check `DATABASE_URL` in `.env`
   - Ensure PostgreSQL is running
   - Verify database exists

2. **JWT token errors**

   - Check `JWT_SECRET` is set
   - Ensure token is not expired
   - Verify token format

3. **Import errors**
   - Ensure you're in the virtual environment: `poetry shell`
   - Check Python path: `poetry run python -c "import sys; print(sys.path)"`

### Logs

Check application logs for detailed error information:

```bash
tail -f logs/auth_service.log
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/docs`

---

**Note**: This is a development version. For production deployment, ensure proper security configurations and environment setup.
