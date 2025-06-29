"""Schemas for audit logs"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from schemas.base import DetailResponse, PaginatedResponse


class AuditLogCreate(BaseModel):
    """Audit log create schema"""

    user_id: Optional[str]
    email: Optional[str]
    action: str
    resource_type: str
    resource_id: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    before_state: Optional[Dict[str, Any]] = Field(default_factory=dict)
    after_state: Optional[Dict[str, Any]] = Field(default_factory=dict)
    severity: Optional[str] = "INFO"


class AuditLog(BaseModel):
    """Audit log out schema"""

    alid: UUID
    tenant_id: str
    created_at: datetime


class AuditLogResponse(DetailResponse[AuditLog]):
    """Audit log out schema"""


class AuditLogDetail(BaseModel):
    """Audit log detail response schema"""

    alid: UUID = Field(..., description="Unique log entry ID")
    tenant_id: str = Field(..., description="Tenant ID")
    user_id: Optional[str] = Field(
        None,
        description="User ID who performed the action",
    )
    action: str = Field(..., description="Action performed")
    resource_type: str = Field(..., description="Type of resource")
    resource_id: str = Field(..., description="ID of the resource")
    ip_address: Optional[str] = Field(
        None,
        description="IP address of the user",
    )
    user_agent: Optional[str] = Field(
        None,
        description="User agent string",
    )
    log_metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional metadata"
    )
    before_state: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="State before the action"
    )
    after_state: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="State after the action"
    )
    severity: Optional[str] = Field("INFO", description="Severity level")
    created_at: datetime = Field(
        ...,
        description="Timestamp when log was created",
    )


class AuditLogDetailResponse(DetailResponse[AuditLogDetail]):
    """Audit log detail response schema"""


class AuditLogSearchResult(BaseModel):
    """Individual audit log search result"""

    id: str = Field(..., description="Unique log entry ID")
    tenant_id: str = Field(..., description="Tenant ID")
    user_id: Optional[str] = Field(
        None,
        description="User ID who performed the action",
    )
    action: str = Field(..., description="Action performed")
    resource_type: str = Field(..., description="Type of resource")
    resource_id: str = Field(..., description="ID of the resource")
    ip_address: Optional[str] = Field(
        None,
        description="IP address of the user",
    )
    user_agent: Optional[str] = Field(None, description="User agent string")
    log_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata"
    )
    before_state: Optional[Dict[str, Any]] = Field(
        None, description="State before the action"
    )
    after_state: Optional[Dict[str, Any]] = Field(
        None, description="State after the action"
    )
    severity: str = Field(..., description="Severity level")
    created_at: datetime = Field(
        ...,
        description="Timestamp when log was created",
    )


class AuditLogPaginatedResponse(PaginatedResponse[AuditLogSearchResult]):
    """Paginated response specifically for audit logs"""


class AuditLogStatsBucket(BaseModel):
    """Audit log stats bucket response schema"""

    key: str
    doc_count: int


class AuditLogStats(BaseModel):
    """Audit log stats response schema"""

    action_counts: List[AuditLogStatsBucket]
    severity_counts: List[AuditLogStatsBucket]


class AuditLogStatsResponse(DetailResponse[AuditLogStats]):
    """Audit log stats response schema"""


class AuditLogBulkCreate(BaseModel):
    """Audit log bulk create schema"""

    logs: List[AuditLogCreate]


class AuditLogBulkCreateResult(BaseModel):
    """Audit log bulk create result schema"""

    affected_rows: int


class AuditLogBulkCreateResponse(DetailResponse[AuditLogBulkCreateResult]):
    """Audit log bulk create response schema"""


class ExportPipeline(BaseModel):
    """Export pipeline schema"""

    id: UUID
    tenant_id: str
    status: str
    created_at: datetime
    file_url: Optional[str] = None


class ExportPipelineDetailResponse(DetailResponse[ExportPipeline]):
    """Export pipeline detail response schema"""


class AuditLogCleanup(BaseModel):
    """Audit log cleanup response schema"""

    deleted: int
    cutoff: datetime


class AuditLogCleanupResponse(DetailResponse[AuditLogCleanup]):
    """Audit log cleanup response schema"""
