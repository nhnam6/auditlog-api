from utils.strutils import validate_uuid


def test_validate_uuid_success():
    """Test validate UUID success"""
    valid_uuid = "3cf0513f-c56d-4141-a90e-6ae02eb89cad"
    result, error = validate_uuid(valid_uuid)
    assert result == valid_uuid
    assert error is None


def test_validate_uuid_failure():
    """Test validate UUID failure"""
    invalid_uuid = "not-a-uuid"
    result, error = validate_uuid(invalid_uuid)
    assert result is None
    assert error == "Invalid UUID format"
