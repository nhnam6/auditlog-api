# AuditLog API

## Project Structure

```
auditlog-api/
├── app/
│   ├── api/                # Routers
│   ├── core/               # Config, tenant DB manager
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic (logging, export)
│   ├── workers/            # Background worker (SQS consumer)
│   └── main.py             # FastAPI app entrypoint
├── scripts/
│   └── init_tenant.py      # CLI for onboarding new tenants
├── tests/
│   └── test_log_api.py     # Pytest tests
├── Dockerfile
├── requirements.txt
└── README.md

```

```sql
INSERT INTO users (uid, email, hashed_password, role, created_at)
VALUES (
    '95735f15-c28d-44df-8091-1b047670b02a',
    'admin@example.com',
    '$2b$12$S9h/mGislH0PemmiNZ7Hau5xHpQE5b3lX5V1VhTtQDCBWs1vsyx5G', --admin123
    'admin',
    now()
);
```
