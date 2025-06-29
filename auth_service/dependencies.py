"""Authentication dependencies"""

from fastapi import Depends, HTTPException, Request, status


def get_current_user(request: Request) -> dict:
    """Get current user from request"""
    if hasattr(request, "state") and hasattr(request.state, "user"):
        return request.state.user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
    )


def require_admin_role(current_user: dict = Depends(get_current_user)) -> dict:
    """Require admin role for access"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return current_user
