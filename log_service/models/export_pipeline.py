"""Export pipeline model"""

from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class ExportPipeline(Base):
    """Export pipeline model"""

    __tablename__ = "export_pipelines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
