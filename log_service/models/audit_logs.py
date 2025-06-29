"""Audit log model"""

from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import JSON, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class AuditLog(Base):
    """Audit log model"""

    __tablename__ = "audit_logs"

    alid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    user_id = Column(String, nullable=True)
    email = Column(String, nullable=True)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    log_metadata = Column(JSON, nullable=True)
    before_state = Column(JSON, nullable=True)
    after_state = Column(JSON, nullable=True)
    severity = Column(String, default="INFO")
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
