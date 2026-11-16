# Helpers for hiding personal data in logs.


def mask(value):
    """Replace every character with '*', keeping the length (None stays None)."""
    if value is None:
        return None
    return '*' * len(str(value))
