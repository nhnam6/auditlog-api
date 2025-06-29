"""Tenant utils"""

from fastapi import HTTPException, Request

from core.config import settings


def get_tenant_id(request: Request) -> str:
    """Get tenant ID from request"""
    user = getattr(request.state, "user", None)
    if not user or "tenant_id" not in user:
        raise HTTPException(
            status_code=403,
            detail="Missing or invalid tenant_id",
        )
    if user["tenant_id"] != settings.TENANT_ID:
        raise HTTPException(
            status_code=403,
            detail="Invalid tenant_id",
        )
    return user["tenant_id"]
