import logging
import re
import sys

MASK_CHAR = '*'

# nazwy wrażliwych pól
SENSITIVE_FIELDS = ('pesel', 'street', 'city')

_SENSITIVE_RE = re.compile(
    r"""(?P<prefix>['"]?\b(?:%s)\b['"]?\s*[:=]\s*['"]?)
        (?P<value>.+?)
        (?=['"]?\s*(?:,\s*['"]?[A-Za-z_]+['"]?\s*[:=]|[)}\]&]|\s+HTTP/|$))
    """ % '|'.join(SENSITIVE_FIELDS),
    re.IGNORECASE | re.VERBOSE,
)


def mask_value(value):
    if value is None:
        return None
    return MASK_CHAR * len(str(value))


def mask_text(text):
    if not isinstance(text, str) or not text:
        return text
    return _SENSITIVE_RE.sub(
        lambda m: m.group('prefix') + mask_value(m.group('value')), text
    )


class RedactingStream:

    def __init__(self, stream):
        self._stream = stream

    def write(self, data):
        return self._stream.write(mask_text(data))

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def __getattr__(self, name):
        return getattr(self._stream, name)


_installed = False


def install_log_masking():
    global _installed
    if _installed:
        return
    _installed = True

    if not isinstance(sys.stdout, RedactingStream):
        sys.stdout = RedactingStream(sys.stdout)
    if not isinstance(sys.stderr, RedactingStream):
        sys.stderr = RedactingStream(sys.stderr)

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        try:
            record.msg = mask_text(record.getMessage())
            record.args = ()
        except Exception:
            pass
        return record

    logging.setLogRecordFactory(record_factory)