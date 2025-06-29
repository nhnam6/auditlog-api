"""Audit log API"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from core.db import get_session
from core.response import create_detail_response, create_paginated_response
from infra.sqs import send_to_export_queue, send_to_log_queue
from schemas.schemas import (
    AuditLogBulkCreate,
    AuditLogBulkCreateResponse,
    AuditLogCleanupResponse,
    AuditLogCreate,
    AuditLogDetailResponse,
    AuditLogPaginatedResponse,
    AuditLogResponse,
    AuditLogStatsResponse,
    ExportPipelineDetailResponse,
)
from services.export import create_export_pipeline, get_export_pipeline
from services.logs import (
    cleanup_old_logs,
    create_bulk_logs,
    create_log_entry,
    get_log_entry,
)
from services.search import (
    delete_old_logs_in_opensearch,
    get_log_stats_opensearch,
    search_logs,
)
from utils.strutils import validate_uuid
from utils.tenant import get_tenant_id

router = APIRouter(prefix="/logs", tags=["Audit Logs"])


@router.delete(
    "/cleanup",
    status_code=200,
    response_model=AuditLogCleanupResponse,
    summary="Cleanup Audit Logs",
    description="Cleanup audit logs",
)
def cleanup_logs_api(request: Request, db: Session = Depends(get_session)):
    """Cleanup logs"""
    tenant_id = get_tenant_id(request)
    result = cleanup_old_logs(db, tenant_id)
    delete_old_logs_in_opensearch(tenant_id)
    return create_detail_response(result)


@router.post(
    "/export",
    status_code=200,
    response_model=ExportPipelineDetailResponse,
    summary="Export Log Data",
    description="Export log data",
)
def export_log_data_api(request: Request, db: Session = Depends(get_session)):
    """Export log data"""
    tenant_id = get_tenant_id(request)
    pipeline = create_export_pipeline(tenant_id, db)
    send_to_export_queue(pipeline.id, tenant_id)
    return create_detail_response(pipeline)


@router.get(
    "/export/{pipeline_id}",
    status_code=200,
    response_model=ExportPipelineDetailResponse,
    summary="Get Export Pipeline",
    description="Get an export pipeline by ID",
)
def export_result_api(
    pipeline_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    """Get export pipeline"""
    tenant_id = get_tenant_id(request)
    pipeline_id, error = validate_uuid(pipeline_id)
    if error:
        return HTTPException(status_code=400, detail="Invalid pipeline ID")
    pipeline = get_export_pipeline(db, tenant_id, pipeline_id)
    if not pipeline:
        return HTTPException(status_code=404, detail="Pipeline not found")
    return create_detail_response(pipeline)


@router.get(
    "/stats",
    status_code=200,
    response_model=AuditLogStatsResponse,
    summary="Get Audit Log Stats",
    description="Get audit log stats",
)
def get_log_stats_api(request: Request):
    """Get log stats"""
    tenant_id = get_tenant_id(request)
    stats = get_log_stats_opensearch(tenant_id)
    return create_detail_response(stats)


@router.post(
    "/bulk",
    status_code=200,
    response_model=AuditLogBulkCreateResponse,
    summary="Bulk Create Audit Log Entries",
    description="Bulk create audit log entries",
)
def bulk_create_logs_api(
    payload: AuditLogBulkCreate,
    request: Request,
    db: Session = Depends(get_session),
):
    """Bulk create logs"""
    tenant_id = get_tenant_id(request)
    if len(payload.logs) > 100:
        return HTTPException(
            status_code=400, detail="Bulk create logs is limited to 100 logs"
        )
    result = create_bulk_logs(db, tenant_id, payload.logs)
    for log_id in result["log_ids"]:
        send_to_log_queue(log_id, tenant_id)
    return create_detail_response(result)


@router.post(
    "",
    response_model=AuditLogResponse,
    status_code=201,
    summary="Create Audit Log Entry",
    description="Create a new audit log entry to track user actions",
    response_description="Successfully created audit log entry",
)
def create_log_api(
    log: AuditLogCreate, request: Request, db: Session = Depends(get_session)
):
    """
    Create a new audit log entry.
    """
    tenant_id = get_tenant_id(request)
    log = create_log_entry(db, tenant_id, log)
    send_to_log_queue(log.alid, tenant_id)
    return create_detail_response(log)


@router.get(
    "/{log_id}",
    status_code=200,
    response_model=AuditLogDetailResponse,
    summary="Get Audit Log Entry",
    description="Get an audit log entry by ID",
    response_description="Successfully retrieved audit log entry",
)
def get_log_api(
    log_id: str,
    request: Request,
    db: Session = Depends(get_session),
):
    """Get a log by ID"""
    log_id, error = validate_uuid(log_id)
    if error:
        return HTTPException(status_code=400, detail="Invalid log ID")
    tenant_id = get_tenant_id(request)
    log = get_log_entry(db, tenant_id, log_id)
    if not log:
        return HTTPException(status_code=404, detail="Log not found")
    return create_detail_response(log)


@router.get(
    "/",
    status_code=200,
    response_model=AuditLogPaginatedResponse,
    summary="List Audit Log Entries",
    description="List audit log entries with optional filters",
)
def list_logs_api(
    request: Request,
    action: str = Query(None),
    severity: str = Query(None),
    user_id: str = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
):
    """List logs"""
    tenant_id = get_tenant_id(request)
    filters = {
        "action": action,
        "severity": severity,
        "user_id": user_id,
        "search": search,
        "page": page,
        "page_size": page_size,
    }
    results = search_logs(tenant_id, filters)
    return create_paginated_response(
        results["logs"],
        results["total"],
        page,
        page_size,
    )
