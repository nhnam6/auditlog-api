"""Search service"""

from datetime import datetime, timedelta, timezone

from infra.opensearch import get_opensearch_client
from models import AuditLog


def index_log_to_opensearch(log: AuditLog):
    """Index log to opensearch"""
    client = get_opensearch_client()
    index_name = f"logs-{log.tenant_id}"

    doc = {
        "id": str(log.alid),
        "tenant_id": log.tenant_id,
        "user_id": log.user_id,
        "action": log.action,
        "resource_type": log.resource_type,
        "resource_id": log.resource_id,
        "ip_address": log.ip_address,
        "user_agent": log.user_agent,
        "log_metadata": log.log_metadata,
        "before_state": log.before_state,
        "after_state": log.after_state,
        "severity": log.severity,
        "created_at": log.created_at.isoformat(),
    }

    client.index(index=index_name, id=doc["id"], body=doc)


def search_logs(tenant_id: str, filters: dict) -> dict:
    """Search logs in opensearch"""
    client = get_opensearch_client()
    index_name = f"logs-{tenant_id}"

    must_clauses = []

    if filters.get("action"):
        must_clauses.append({"term": {"action": filters["action"]}})
    if filters.get("severity"):
        must_clauses.append({"term": {"severity": filters["severity"]}})
    if filters.get("user_id"):
        must_clauses.append({"term": {"user_id": filters["user_id"]}})
    if filters.get("search"):
        must_clauses.append(
            {
                "match": {
                    "user_agent": {
                        "query": filters["search"],
                        "operator": "or",
                    }
                },
            }
        )

    body = {
        "query": {"bool": {"must": must_clauses}},
        "from": (filters.get("page", 1) - 1) * filters.get("page_size", 10),
        "size": filters.get("page_size", 10),
        "sort": [{"timestamp": {"order": "desc"}}],
    }

    result = client.search(index=index_name, body=body)
    return {
        "total": result["hits"]["total"]["value"],
        "logs": [hit["_source"] for hit in result["hits"]["hits"]],
    }


def get_log_stats_opensearch(tenant_id: str):
    """Get log stats from opensearch"""
    client = get_opensearch_client()
    index = f"logs-{tenant_id}"

    body = {
        "size": 0,
        "aggs": {
            "by_action": {"terms": {"field": "action"}},
            "by_severity": {"terms": {"field": "severity"}},
        },
    }

    try:
        response = client.search(index=index, body=body)
        aggregations = response["aggregations"]
        return {
            "action_counts": aggregations["by_action"]["buckets"],
            "severity_counts": aggregations["by_severity"]["buckets"],
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get stats from OpenSearch: {e}") from e


def delete_old_logs_in_opensearch(tenant_id: str, days: int = 90):
    """Delete old logs in opensearch"""
    client = get_opensearch_client()
    index_name = f"logs-{tenant_id}"
    threshold_date = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"tenant_id": tenant_id}},
                    {"range": {"timestamp": {"lt": threshold_date}}},
                ]
            }
        }
    }

    response = client.delete_by_query(index=index_name, body=query)
    return response
