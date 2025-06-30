# AuditLog API - Postman Collection

This Postman collection provides a comprehensive set of API requests for testing and interacting with the AuditLog API system, which includes both the Log Service and Auth Service.

## Overview

The collection is organized into three main sections:
- **Opensearch** - Direct OpenSearch operations for data management
- **LogService** - Audit log API endpoints for log management
- **AuthService** - Authentication and tenant management endpoints

## Setup Instructions

### Import the Collection

1. Open Postman
2. Click "Import" button
3. Select the `AuditLog.postman_collection.json` file
4. The collection will be imported with all pre-configured requests

### 2. Import the Environment

1. In Postman, go to "Environments" tab
2. Click "Import" button
3. Select the `Local.postman_environment.json` file
4. Select the "Local" environment from the dropdown in the top-right corner

### 3. Configure Environment Variables

The environment includes the following variables that you may need to update:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `LOG_SERVICE_API_URL` | Log Service API base URL | `http://localhost:8000` |
| `AUTH_SERVICE_API_URL` | Auth Service API base URL | `http://localhost:8001` |
| `OPENSEARCH_URL` | OpenSearch instance URL | `http://localhost:9200` |
| `TENANT_ACCESS_TOKEN` | JWT token for tenant operations | (empty - set after login) |
| `ADMIN_ACCESS_TOKEN` | JWT token for admin operations | (empty - set after login) |
| `TENANT_ID` | Current tenant ID | (empty - set after login) |
| `INDEX_PREFIX` | OpenSearch index prefix | `logs` |
| `INDEX_NAME` | Computed index name | `{{INDEX_PREFIX}}-{{TENANT_ID}}` |

## Authentication

### Getting Access Tokens

1. **Login as Admin** (AuthService > Login):
   ```json
   {
     "email": "admin@example.com",
     "password": "adminpassword"
   }
   ```
   Copy the `access_token` from the response to `ADMIN_ACCESS_TOKEN`

2. **Login as Tenant User** (AuthService > Login):
   ```json
   {
     "email": "user@tenant.com",
     "password": "userpassword"
   }
   ```
   Copy the `access_token` from the response to `TENANT_ACCESS_TOKEN`
   Copy the `tenant_id` from the response to `TENANT_ID`

## API Endpoints

### Opensearch Operations

#### Health Check
- **GET** `{{OPENSEARCH_URL}}/_cluster/health`
- Check OpenSearch cluster health status

#### Index Management
- **PUT** `{{OPENSEARCH_URL}}/_index_template/audit-logs-template` - Create index template
- **GET** `{{OPENSEARCH_URL}}/_index_template/audit-logs-template` - Get index template
- **DELETE** `{{OPENSEARCH_URL}}/_index_template/audit-logs-template` - Delete index template
- **PUT** `{{OPENSEARCH_URL}}/{{INDEX_NAME}}` - Create index
- **GET** `{{OPENSEARCH_URL}}/{{INDEX_NAME}}` - Get index info
- **DELETE** `{{OPENSEARCH_URL}}/{{INDEX_NAME}}` - Delete index

#### Search Operations
- **GET** `{{OPENSEARCH_URL}}/{{INDEX_NAME}}/_search` - Search logs with query

### Log Service API

#### Health Check
- **GET** `{{LOG_SERVICE_API_URL}}/health`
- Check Log Service health status

#### Audit Log Management
- **POST** `{{LOG_SERVICE_API_URL}}/api/v1/logs` - Create single log entry
- **POST** `{{LOG_SERVICE_API_URL}}/api/v1/logs/bulk` - Create multiple log entries
- **GET** `{{LOG_SERVICE_API_URL}}/api/v1/logs/{log_id}` - Retrieve specific log
- **GET** `{{LOG_SERVICE_API_URL}}/api/v1/logs/` - List logs with filters
- **GET** `{{LOG_SERVICE_API_URL}}/api/v1/logs/stats` - Get log statistics
- **DELETE** `{{LOG_SERVICE_API_URL}}/api/v1/logs/cleanup` - Cleanup old logs

#### Export Operations
- **POST** `{{LOG_SERVICE_API_URL}}/api/v1/logs/export` - Initiate log export
- **GET** `{{LOG_SERVICE_API_URL}}/api/v1/logs/export/{pipeline_id}` - Get export status

### Auth Service API

#### Health Check
- **GET** `{{AUTH_SERVICE_API_URL}}/health`
- Check Auth Service health status

#### Authentication
- **POST** `{{AUTH_SERVICE_API_URL}}/api/v1/login` - Login to get access token

#### Tenant Management (Admin Only)
- **GET** `{{AUTH_SERVICE_API_URL}}/api/v1/tenants` - List all tenants
- **POST** `{{AUTH_SERVICE_API_URL}}/api/v1/tenants` - Create new tenant

## Usage Examples

### 1. Complete Setup Flow

1. **Start Services**: Ensure Log Service (port 8000) and Auth Service (port 8001) are running
2. **Login as Admin**: Use AuthService > Login with admin credentials
3. **Set Admin Token**: Copy the access token to `ADMIN_ACCESS_TOKEN` environment variable
4. **Create Tenant**: Use AuthService > Create Tenant to create a new tenant
5. **Login as Tenant User**: Use AuthService > Login with tenant user credentials
6. **Set Tenant Token**: Copy the access token to `TENANT_ACCESS_TOKEN` and tenant_id to `TENANT_ID`
7. **Setup OpenSearch**: Use Opensearch > Create index template and Create index
8. **Create Logs**: Use LogService > Create Log to add audit log entries

### 2. Creating Audit Logs

**Single Log Entry:**
```json
{
  "user_id": "{{$guid}}",
  "email": "nhnam6@gmail.com",
  "action": "LOGIN",
  "resource_type": "user",
  "resource_id": "user_12345",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "metadata": {
      "login_method": "password"
  },
  "before_state": {},
  "after_state": {
      "login_time": "2024-01-15T10:30:00Z"
  },
  "severity": "INFO"
}
```

**Bulk Log Entries:**
```json
{
  "logs": [
    {
      "user_id": "{{$guid}}",
      "email": "nhnam6@gmail.com",
      "action": "LOGIN",
      "resource_type": "user",
      "resource_id": "user_12345",
      "ip_address": "192.168.1.100",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
      "metadata": {
          "login_method": "password"
      },
      "before_state": {},
      "after_state": {
          "login_time": "2024-01-15T10:30:00Z"
      },
      "severity": "INFO"
    }
  ]
}
```

### 3. Searching Logs

**Basic Search:**
```
GET {{LOG_SERVICE_API_URL}}/api/v1/logs/?action=LOGIN&severity=INFO&page=1&page_size=10
```

**Advanced Search with Filters:**
```
GET {{LOG_SERVICE_API_URL}}/api/v1/logs/?action=CREATE&user_id=user-123&search=document&page=1&page_size=20
```

### 4. Exporting Logs

1. **Initiate Export:**
   ```json
   POST {{LOG_SERVICE_API_URL}}/api/v1/logs/export
   ```

2. **Check Export Status:**
   ```
   GET {{LOG_SERVICE_API_URL}}/api/v1/logs/export/{pipeline_id}
   ```

## Headers

Most API requests require the following headers:

```
Content-Type: application/json
Authorization: Bearer {{TENANT_ACCESS_TOKEN}}
```

For admin operations, use:
```
Authorization: Bearer {{ADMIN_ACCESS_TOKEN}}
```

## Error Handling

The API returns standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

Error responses include detailed error messages:
```json
{
  "detail": "Invalid credentials"
}
```

## Testing Workflows

### 1. Basic CRUD Operations
1. Create a log entry
2. Retrieve the created log
3. List logs with filters
4. Get log statistics

### 2. Bulk Operations
1. Create multiple logs in bulk
2. Search and filter bulk logs
3. Export bulk logs

### 3. Admin Operations
1. Login as admin
2. Create new tenant
3. List all tenants
4. Manage tenant users

### 4. OpenSearch Integration
1. Create index template
2. Create index
3. Index logs via API
4. Search logs in OpenSearch
5. Verify data consistency
