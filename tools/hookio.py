"""Hook kirishi: Claude Code stdin ga UTF-8 JSON beradi.

Matnli `sys.stdin` Windows da ANSI kod sahifasi (cp1252) bilan o'qiydi,
o'zbekcha `ʻ` yoki ruscha harfli prompt buzilib keladi. Windows
PowerShell 5.1 esa native buyruqqa pipe qilganda boshiga BOM qo'yishi
mumkin: `json.load` undan yiqiladi va hook jim qoladi. Shuning uchun
baytlar o'qiladi va `utf-8-sig` bilan ochiladi.
"""

import json
import sys


def read_text(stream=None):
    """stdin matni. Terminal, yopiq yoki o'qilmaydigan oqimda ""."""
    stream = sys.stdin if stream is None else stream
    try:
        if stream is None or stream.isatty():
            return ""
        raw = getattr(stream, "buffer", None)
        data = raw.read() if raw is not None else stream.read()
    except (OSError, ValueError):
        return ""
    if isinstance(data, bytes):
        return data.decode("utf-8-sig", errors="replace")
    return data.lstrip("\ufeff")


def read_payload(stream=None, blank=None):
    """JSON obyekt. Bo'sh kirishda `blank`, buzuq yoki obyekt emasda None.

    Terminal ham None: hook qo'lda yurgizilganda EOF kutib qotmaydi.
    """
    stream = sys.stdin if stream is None else stream
    try:
        if stream is None or stream.isatty():
            return None
    except (OSError, ValueError):
        return None
    text = read_text(stream)
    if not text.strip():
        return blank
    try:
        payload = json.loads(text)
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None
