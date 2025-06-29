"""String utilities"""

import uuid


def validate_uuid(id_str: str) -> tuple[str, str]:
    """
    Validates if the given string is a valid UUID.

    Returns:
        tuple[str, str]: The same string if it's a valid UUID,
            or None and error message if it's not.
    """
    try:
        return str(uuid.UUID(id_str)), None
    except ValueError:
        return None, "Invalid UUID format"
