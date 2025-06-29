"""OpenSearch client"""

from opensearchpy import OpenSearch

from core.config import settings


def get_opensearch_client():
    """Get OpenSearch client"""
    return OpenSearch(
        hosts=[
            {
                "host": settings.OPENSEARCH_HOST,
                "port": settings.OPENSEARCH_PORT,
            },
        ],
        http_auth=(settings.OPENSEARCH_USER, settings.OPENSEARCH_PASS),
        use_ssl=False,
        verify_certs=False,
        timeout=30,
        max_retries=3,
        retry_on_timeout=True,
        retry_on_status=[502, 503, 504],
        sniff_on_start=False,
        sniff_on_connection_fail=False,
        sniffer_timeout=None,
    )
