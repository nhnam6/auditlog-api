"""Test health API"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check_success():
    """Test health check endpoint success"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "Service is healthy"


def test_health_check_response_structure():
    """Test health check response structure"""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()

    # Check all required fields are present
    required_fields = ["status", "message"]
    for field in required_fields:
        assert field in data
        assert isinstance(data[field], str)


def test_health_check_content_type():
    """Test health check content type"""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
