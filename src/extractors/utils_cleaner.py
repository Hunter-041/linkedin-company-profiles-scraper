import logging
import re
from typing import Any, Optional

logger = logging.getLogger(__name__)

_whitespace_re = re.compile(r"\s+", re.UNICODE)

def clean_text(value: Optional[str]) -> Optional[str]:
    """
    Normalize whitespace in text and strip it.
    Returns None if the input is falsy after cleaning.
    """
    if value is None:
        return None

    if not isinstance(value, str):
        value = str(value)

    cleaned = _whitespace_re.sub(" ", value).strip()
    return cleaned or None

def safe_int(value: Any) -> Optional[int]:
    """
    Convert a value to int where possible.
    Returns None if conversion fails.
    """
    if value is None:
        return None

    if isinstance(value, int):
        return value

    try:
        # Remove obvious formatting from numbers like "1,234"
        text = str(value)
        text = text.replace(",", "").strip()
        if not text:
            return None
        return int(text)
    except (ValueError, TypeError) as exc:
        logger.debug("safe_int: failed to parse %r: %s", value, exc)
        return None

def safe_str(value: Any) -> str:
    """
    Always return a safe string representation.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)

def extract_year(text: Optional[str]) -> Optional[int]:
    """
    Extract a 4-digit year from a text.
    """
    if not text:
        return None
    match = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    if not match:
        return None
    return safe_int(match.group(1))