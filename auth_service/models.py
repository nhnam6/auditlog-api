"""Models for the authentication service"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model"""

    __tablename__ = "users"

    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tenant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tenants.tid"),
        nullable=True,
    )
    tenant = relationship("Tenant", back_populates="users", lazy="joined")


class Tenant(Base):
    """Tenant model"""

    __tablename__ = "tenants"
    tid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="tenant")
