"""Export service"""

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models.export_pipeline import ExportPipeline


def create_export_pipeline(tenant_id: str, db: Session):
    """Create export pipeline"""
    pipeline_id = str(uuid.uuid4())
    pipeline = ExportPipeline(
        id=pipeline_id,
        tenant_id=tenant_id,
        status="PENDING",
        created_at=datetime.now(timezone.utc),
    )
    db.add(pipeline)
    db.commit()
    return pipeline


def get_export_pipeline(db: Session, tenant_id: str, pipeline_id: str):
    """Get export pipeline"""
    return (
        db.query(ExportPipeline)
        .filter_by(
            id=pipeline_id,
            tenant_id=tenant_id,
        )
        .first()
    )
