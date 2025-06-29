"""Audit log services"""

from datetime import datetime, timedelta, timezone
from typing import List
from uuid import uuid4

from sqlalchemy.orm import Session

from models.audit_logs import AuditLog
from schemas.schemas import AuditLogCreate
from services.masking import mask_sensitive_data


def create_log_entry(
    db: Session,
    tenant_id: str,
    log: AuditLogCreate,
) -> AuditLog:
    """Create a log entry"""
    log_data = mask_sensitive_data(log.model_dump())
    log_entry = AuditLog(**log_data, tenant_id=tenant_id, alid=uuid4())
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry


def get_log_entry(db: Session, tenant_id: str, log_id: str) -> AuditLog:
    """Get a log entry"""

    return (
        db.query(AuditLog)
        .filter_by(
            alid=log_id,
            tenant_id=tenant_id,
        )
        .first()
    )


def create_bulk_logs(
    db: Session,
    tenant_id: str,
    logs: List[AuditLogCreate],
) -> dict:
    """Create bulk logs"""
    log_ids = []
    for log in logs:
        log_data = mask_sensitive_data(log.model_dump())
        log_entry = AuditLog(**log_data, tenant_id=tenant_id, alid=uuid4())
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        log_ids.append(log_entry.alid)

    return {"affected_rows": len(log_ids), "log_ids": log_ids}


def get_logs_for_export(db: Session, tenant_id: str) -> List[AuditLog]:
    """Get logs for export"""
    return (
        db.query(AuditLog)
        .filter(AuditLog.tenant_id == tenant_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )


def cleanup_old_logs(
    db: Session,
    tenant_id: str,
    retention_days: int = 90,
):
    """Cleanup old logs"""
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    deleted = (
        db.query(AuditLog)
        .filter(AuditLog.tenant_id == tenant_id)
        .filter(AuditLog.created_at < cutoff)
        .delete(synchronize_session=False)
    )
    db.commit()
    return {"deleted": deleted, "cutoff": cutoff.isoformat()}
