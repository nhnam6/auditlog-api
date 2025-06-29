"""Schemas for the authentication service"""

from typing import Generic, List, TypeVar
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema"""

    items: List[T]
    total: int
    page: int
    page_size: int


class DetailResponse(BaseModel, Generic[T]):
    """Detail response schema"""

    data: T


class LoginRequest(BaseModel):
    """Request schema for login"""

    email: str
    password: str


class Token(BaseModel):
    """Response schema for token"""

    tenant_id: str
    access_token: str
    token_type: str = "bearer"


class TokenResponse(DetailResponse[Token]):
    """Response schema for token"""


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    message: str = "Service is healthy"


class TenantRequest(BaseModel):
    """Request schema for tenant creation"""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr = Field(..., description="Admin user email for the tenant")
    password: str = Field(..., min_length=8)


class Tenant(BaseModel):
    """Tenant model"""

    tid: UUID
    name: str


class TenantResponse(DetailResponse[Tenant]):
    """Response schema for tenant creation"""


class TenantListResponse(PaginatedResponse[Tenant]):
    """Response schema for tenant list"""
