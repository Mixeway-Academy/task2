import sys
import re
import logging

PESEL_REGEX = re.compile(r'\b\d{11}\b')

class SensitiveDataMasker:
    @staticmethod
    def mask_text(text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        
        text = PESEL_REGEX.sub(lambda m: '*' * len(m.group(0)), text)
        
        return text

class StreamRedirector:
    def __init__(self, original_stream):
        self.original_stream = original_stream

    def write(self, message):
        masked_message = SensitiveDataMasker.mask_text(message)
        self.original_stream.write(masked_message)

    def flush(self):
        self.original_stream.flush()

class LoggingMaskingFilter(logging.Filter):
    def filter(self, record):
        if record.msg and isinstance(record.msg, str):
            record.msg = SensitiveDataMasker.mask_text(record.msg)
        if record.args:
            if isinstance(record.args, tuple):
                record.args = tuple(SensitiveDataMasker.mask_text(arg) if isinstance(arg, str) else arg for arg in record.args)
            elif isinstance(record.args, dict):
                record.args = {k: (SensitiveDataMasker.mask_text(v) if isinstance(v, str) else v) for k, v in record.args.items()}
        return True

def init_log_masking():
    sys.stdout = StreamRedirector(sys.stdout)
    sys.stderr = StreamRedirector(sys.stderr)
    
    root_logger = logging.getLogger()
    root_logger.addFilter(LoggingMaskingFilter())
    for handler in root_logger.handlers:
        handler.addFilter(LoggingMaskingFilter())