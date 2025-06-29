"""
Main module for the FastAPI application
"""

from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from api import logs
from core.auth import AuthMiddleware
from core.logging import setup_logging

setup_logging()

app = FastAPI(title="Log Service")

app.add_middleware(AuthMiddleware)

# Register the audit log router
app.include_router(logs.router, prefix="/api/v1")


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str
    message: str = "Service is healthy"


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Check if the API service is running and healthy",
    response_description="Health status of the service",
)
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint
    """
    return {"status": "ok", "message": "Service is healthy"}
