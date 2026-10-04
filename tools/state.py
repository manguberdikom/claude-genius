#!/usr/bin/env python3
"""Zanjir qadamlarining bajarilganini belgilaydi.

`rules_for.py` chaqirilishi ko'rsatma bo'lsa, u unutiladi va hech kim
sezmaydi: aktyor qoidani ko'rmay yozadi, reviewer topadi, ish ikkinchi
aylanaga tushadi. Shuning uchun chaqiruv belgilanadi va `check_code.py`
yozuvdan oldin shu belgini talab qiladi.

Holat `.claude/.state/` da, git ga kirmaydi: u sessiyaga tegishli,
jamoaga emas.
"""

import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT, ".claude", ".state")
RULES_LOG = os.path.join(STATE_DIR, "rules_for.json")

# Belgining yaroqlilik muddati. Uzoq sessiyada bir marta chaqirilgan
# narsa kun bo'yi amal qilmasligi kerak: kod o'zgaradi, qoida ham.
MAX_AGE = 6 * 3600


def _key(path):
    full = path if os.path.isabs(path) else os.path.join(ROOT, path)
    return os.path.normpath(full)


def _load():
    try:
        with open(RULES_LOG, encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def mark(paths):
    """Shu fayllar uchun rules_for chaqirilganini yozadi."""
    data = _load()
    now = time.time()
    for path in paths:
        data[_key(path)] = now
    # Eskirganlarini tashlab ketamiz, aks holda fayl cheksiz o'sadi.
    data = {k: v for k, v in data.items() if now - v < MAX_AGE}
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        tmp = RULES_LOG + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp, RULES_LOG)
    except OSError:
        pass  # belgilash ishni to'xtatmaydi


def was_marked(path):
    """Shu fayl uchun rules_for yaqinda chaqirilganmi."""
    stamp = _load().get(_key(path))
    return stamp is not None and (time.time() - stamp) < MAX_AGE


def clear():
    """Sinovlar uchun: holatni tozalaydi."""
    try:
        os.remove(RULES_LOG)
    except OSError:
        pass
