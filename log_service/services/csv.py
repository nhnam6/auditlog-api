"""CSV service"""

import csv
import os
from datetime import datetime, timezone
from typing import List

from models import AuditLog

EXPORT_DIR = "/tmp/exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


def write_logs_to_csv(logs: List[AuditLog], tenant_id: str) -> str:
    """Write logs to CSV"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    filename = f"{tenant_id}_logs_{timestamp}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "alid",
                "tenant_id",
                "user_id",
                "action",
                "resource_type",
                "resource_id",
                "ip_address",
                "user_agent",
                "log_metadata",
                "severity",
                "created_at",
            ]
        )
        for log in logs:
            writer.writerow(
                [
                    log.alid,
                    log.tenant_id,
                    log.user_id,
                    log.action,
                    log.resource_type,
                    log.resource_id,
                    log.ip_address,
                    log.user_agent,
                    log.log_metadata,
                    log.severity,
                    log.created_at,
                ]
            )
    return filepath
