"""Tenant service"""

import uuid
from typing import List, Tuple

from sqlalchemy.orm import Session

from models import Tenant, User
from schemas import TenantRequest
from utils import hash_password


def create_tenant(db: Session, payload: TenantRequest):
    """Create a tenant"""
    tenant = Tenant(name=payload.name, tid=uuid.uuid4())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)

    user = User(
        uid=uuid.uuid4(),
        email=payload.email,
        hashed_password=hash_password(payload.password),
        tenant_id=tenant.tid,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return tenant


def get_tenant_by_name(db: Session, name: str):
    """Get a tenant by name"""
    return db.query(Tenant).filter(Tenant.name == name).first()


def get_tenants(
    db: Session,
    page: int,
    page_size: int,
) -> Tuple[List[Tenant], int]:
    """Get all tenants"""
    tenants = (
        db.query(Tenant)
        .order_by(Tenant.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    total = db.query(Tenant).count()
    return tenants, total
