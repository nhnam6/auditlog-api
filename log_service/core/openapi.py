"""Openapi"""

from fastapi.openapi.utils import get_openapi


def custom_openapi(app):
    """Custom openapi"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Audit Log API",
        version="1.0.0",
        description="Audit Log API with multi-tenant support",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema
