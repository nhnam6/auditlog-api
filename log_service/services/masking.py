"""Masking service"""

SENSITIVE_KEYS = {"email", "phone"}


def mask_value(value: str, min_visible: int = 3) -> str:
    """
    Mask a value while keeping at least min_visible characters visible.

    Args:
        value: The string value to mask
        min_visible: Minimum number of characters to keep visible (default: 3)

    Returns:
        Masked string with format like "abc***" or "***" for very short values
    """
    if not isinstance(value, str):
        return value

    value = str(value).strip()
    length = len(value)

    if length <= min_visible:
        # For very short values, just return asterisks
        return "*" * min(length, 3)

    # Keep first min_visible characters, mask the rest
    visible_part = value[:min_visible]
    masked_part = "*" * (length - min_visible)

    return f"{visible_part}{masked_part}"


def mask_sensitive_data(data: dict) -> dict:
    """
    Mask sensitive data in a dictionary.

    Args:
        data: Dictionary containing potentially sensitive data

    Returns:
        Dictionary with sensitive data masked
    """
    masked = {}
    for k, v in data.items():
        key_lower = k.lower()

        if key_lower in SENSITIVE_KEYS:
            # Mask sensitive values
            masked[k] = mask_value(v)
        elif isinstance(v, dict):
            # Recursively mask nested dictionaries
            masked[k] = mask_sensitive_data(v)
        elif isinstance(v, list):
            # Handle lists (mask each item if it's a dict)
            masked[k] = [
                mask_sensitive_data(item) if isinstance(item, dict) else item
                for item in v
            ]
        else:
            # Keep non-sensitive values as-is
            masked[k] = v

    return masked
