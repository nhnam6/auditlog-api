"""Auth service"""

from typing import Any, Dict

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from auth import AuthMiddleware
from db import get_session
from dependencies import require_admin_role
from logger import auth_logger, setup_logging
from response import create_detail_response, create_paginated_response
from schemas import (
    HealthResponse,
    LoginRequest,
    TenantListResponse,
    TenantRequest,
    TenantResponse,
    TokenResponse,
)
from tenant_service import create_tenant, get_tenant_by_name, get_tenants
from user_service import get_user_by_email
from utils import create_access_token, verify_password

setup_logging()


app = FastAPI(title="Auth Service")
app.add_middleware(AuthMiddleware)

logger = auth_logger


@app.get(
    "/api/v1/tenants",
    status_code=200,
    tags=["tenants"],
    summary="Get all tenants",
    description="Get all tenants",
    response_description="All tenants",
    response_model=TenantListResponse,
)
def get_tenants_api(
    page: int = Query(1, ge=1, description="Page number (minimum 1)"),
    page_size: int = Query(
        10, ge=1, le=100, description="Number of items per page (1-100)"
    ),
    db: Session = Depends(get_session),
    current_user: dict = Depends(require_admin_role),
):
    """Get all tenants"""
    logger.info("Getting tenants for current_user:%s", current_user)
    tenants, total = get_tenants(db, page, page_size)
    return create_paginated_response(
        tenants,
        total=total,
        page=page,
        page_size=page_size,
    )


@app.post(
    "/api/v1/tenants",
    status_code=201,
    tags=["tenants"],
    summary="Create a tenant",
    description="Create a tenant",
    response_description="Tenant created",
    response_model=TenantResponse,
)
def create_tenant_api(
    data: TenantRequest,
    db: Session = Depends(get_session),
    current_user: dict = Depends(require_admin_role),
):
    """Create a tenant"""
    logger.info("Creating tenant for current_user:%s", current_user)
    if get_tenant_by_name(db, data.name):
        raise HTTPException(
            status_code=400,
            detail="Tenant name already exists",
        )

    tenant = create_tenant(db, data)
    return create_detail_response(tenant)


@app.post(
    "/api/v1/login",
    response_model=TokenResponse,
    tags=["auth"],
    summary="Login",
    description="Login to the service",
    response_description="Access token",
)
def login_api(data: LoginRequest, db: Session = Depends(get_session)):
    """Login endpoint"""
    user = get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_data = {
        "sub": user.email,
        "tenant_id": str(user.tenant_id or ""),
        "role": user.role,
    }
    token = create_access_token(token_data)
    return create_detail_response(
        {"access_token": token, "tenant_id": str(user.tenant_id or "")}
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Check if the API service is running and healthy",
    response_description="Health status of the service",
)
def health_check_api() -> Dict[str, Any]:
    """
    Health check endpoint
    """
    return {"status": "ok", "message": "Service is healthy"}
