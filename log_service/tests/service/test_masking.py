"""Test masking service"""

from services.masking import mask_sensitive_data, mask_value


def test_mask_value_basic():
    """Test mask value basic"""
    assert mask_value("john.doe@example.com") == "joh*****************"


def test_mask_value_custom_min_visible():
    """Test mask value with custom min visible"""
    assert mask_value("sensitivevalue", min_visible=5) == "sensi*********"
    assert mask_value("123", min_visible=5) == "***"


def test_mask_sensitive_data_flat():
    """Test mask sensitive data with flat"""
    input_data = {
        "email": "user@example.com",
        "phone": "1234567890",
        "name": "Alice",
    }
    masked = mask_sensitive_data(input_data)

    assert masked["email"].startswith("use")
    assert "*" in masked["email"]
    assert masked["phone"].startswith("123")
    assert "*" in masked["phone"]
    assert masked["name"] == "Alice"


def test_mask_sensitive_data_nested():
    """Test mask sensitive data with nested"""
    input_data = {
        "profile": {
            "email": "user@example.com",
            "phone": "0987654321",
            "address": "123 Main St",
        },
        "activity": {"last_login": "today"},
    }

    masked = mask_sensitive_data(input_data)

    assert masked["profile"]["email"].startswith("use")
    assert masked["profile"]["phone"].startswith("098")
    assert "*" in masked["profile"]["email"]
    assert "*" in masked["profile"]["phone"]
    assert masked["profile"]["address"] == "123 Main St"
    assert masked["activity"]["last_login"] == "today"


def test_mask_sensitive_data_with_list():
    """Test mask sensitive data with list"""
    input_data = {
        "users": [
            {"email": "user1@example.com", "phone": "1112223333"},
            {"email": "user2@example.com", "phone": "4445556666"},
        ],
        "non_sensitive": ["a", "b"],
    }

    masked = mask_sensitive_data(input_data)

    for user in masked["users"]:
        assert user["email"].startswith("use")
        assert "*" in user["email"]
        assert user["phone"].startswith("111") or user["phone"].startswith("444")
        assert "*" in user["phone"]

    assert masked["non_sensitive"] == ["a", "b"]
