"""Test tenant utils"""

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from core.config import settings
from utils.tenant import get_tenant_id


def make_request_with_user(user_dict):
    """Make a request with a user"""
    req = SimpleNamespace()
    req.state = SimpleNamespace(user=user_dict)
    return req


def test_get_tenant_id_valid():
    """Test get tenant ID valid"""
    req = make_request_with_user({"tenant_id": settings.TENANT_ID})
    tenant_id = get_tenant_id(req)
    assert tenant_id == settings.TENANT_ID


def test_get_tenant_id_missing_user():
    """Test get tenant ID missing user"""
    req = SimpleNamespace()
    req.state = SimpleNamespace()  # no user attribute
    with pytest.raises(HTTPException) as exc:
        get_tenant_id(req)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Missing or invalid tenant_id"


def test_get_tenant_id_missing_tenant_id():
    """Test get tenant ID missing tenant ID"""
    req = make_request_with_user({"email": "user@example.com"})  # no tenant_id
    with pytest.raises(HTTPException) as exc:
        get_tenant_id(req)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Missing or invalid tenant_id"


def test_get_tenant_id_invalid_value(monkeypatch):
    """Test get tenant ID invalid value"""
    req = make_request_with_user({"tenant_id": "wrong-id"})
    monkeypatch.setattr(settings, "TENANT_ID", "correct-id")
    with pytest.raises(HTTPException) as exc:
        get_tenant_id(req)
    assert exc.value.status_code == 403
    assert exc.value.detail == "Invalid tenant_id"
