import logging
import os
import re

SENSITIVE_PATTERNS = [
    re.compile(r'(?i)token=\\S+'),
    re.compile(r'(?i)password=\\S+'),
    re.compile(r'(?i)apikey=\\S+'),
    re.compile(r'(?i)gemini_api_key=\\S+'),
]


def mask_message(msg: str) -> str:
    out = msg
    for pat in SENSITIVE_PATTERNS:
        out = pat.sub('[REDACTED]', out)
    # Mask common secret-looking substrings
    out = re.sub(r'([A-Za-z0-9_-]{20,})', '[REDACTED]', out)
    return out


class MaskingFormatter(logging.Formatter):
    def format(self, record):
        try:
            record.msg = mask_message(str(record.getMessage()))
        except Exception:
            record.msg = '[LOG-MASK-ERROR]'
        return super().format(record)


def configure_logging(level: str = None):
    if level is None:
        level = os.getenv("LOG_LEVEL", "INFO")
    level = getattr(logging, level.upper(), logging.INFO)

    handler = logging.StreamHandler()
    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    handler.setFormatter(MaskingFormatter(fmt))
    root = logging.getLogger()
    root.setLevel(level)
    # remove existing handlers to avoid duplicate logs in some environments
    for h in list(root.handlers):
        root.removeHandler(h)
    root.addHandler(handler)
