import logging
import re
import sys

_PESEL = re.compile(r'(?<!\d)\d{11}(?!\d)')
_ADDRESS = re.compile(r"""(\b(?:street|appNo|address)\b["']?\s*[:=]\s*["']?)([^,)}&"'\r\n]+)""", re.I)


def mask(text):
    text = _PESEL.sub(lambda m: '*' * len(m[0]), text)
    return _ADDRESS.sub(lambda m: m[1] + '*' * len(m[2]), text)


class _MaskingStream:
    def __init__(self, stream):
        self._stream = stream

    def write(self, text):
        return self._stream.write(mask(text))

    def __getattr__(self, name):
        return getattr(self._stream, name)


def install_masking():
    if isinstance(sys.stdout, _MaskingStream):
        return

    sys.stdout = _MaskingStream(sys.stdout)
    sys.stderr = _MaskingStream(sys.stderr)

    make_record = logging.getLogRecordFactory()

    def masked_record(*args, **kwargs):
        record = make_record(*args, **kwargs)
        record.msg, record.args = mask(record.getMessage()), None
        return record

    logging.setLogRecordFactory(masked_record)
