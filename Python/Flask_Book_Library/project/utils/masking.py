"""Helpers for masking sensitive personal data (PESEL, address) before it is logged."""

MASK_CHAR = '*'


def mask(value):
    """Replace every character of the value with '*', e.g. '90010112345' -> '***********'.

    The length is kept so the log format stays unchanged; None stays None.
    """
    if value is None:
        return None
    return MASK_CHAR * len(str(value))


def redact(text, *sensitive_values):
    """Mask every occurrence of the given sensitive values inside free text
    (e.g. an exception message that echoes SQL parameters)."""
    text = str(text)
    # longest first, so a short value never breaks a longer one that contains it
    values = sorted({str(v) for v in sensitive_values if v not in (None, '')}, key=len, reverse=True)
    for value in values:
        # SQLAlchemy prints parameters as Python literals ('value'), mask those first
        text = text.replace(repr(value), repr(mask(value)))
        # bare occurrences too - only for longer values, so e.g. apartment no. '3'
        # does not wipe every digit 3 from the message
        if len(value) >= 4:
            text = text.replace(value, mask(value))
    return text
