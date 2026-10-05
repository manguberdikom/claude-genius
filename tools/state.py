#!/usr/bin/env python3
"""Zanjir qadamlarining bajarilganini belgilaydi.

`rules_for.py` chaqirilishi ko'rsatma bo'lsa, u unutiladi va hech kim
sezmaydi: aktyor qoidani ko'rmay yozadi, reviewer topadi, ish ikkinchi
aylanaga tushadi. Shuning uchun chaqiruv belgilanadi va `check_code.py`
har Java yozuvidan keyin (`PostToolUse`) shu belgini tekshiradi.

Holat `.claude/.state/` da, git ga kirmaydi: u sessiyaga tegishli,
jamoaga emas. `GENIUS_STATE_DIR` berilsa, holat o'sha papkada turadi:
sinovlar jonli sessiyaning belgilarini o'chirmasligi uchun.

Har fayl uchun alohida belgi fayli. Avval hammasi bitta JSON da edi va
har chaqiruv uni o'qib, o'zgartirib, qayta yozardi: parallel ikki
rules_for bir-birining belgisini o'chirar, check_code esa keyin yolg'on
to'sardi. Alohida faylda o'qish-yozish poygasi yo'q, qulf ham kerak emas.
"""

import hashlib
import json
import os
import shutil
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = (os.environ.get("GENIUS_STATE_DIR")
             or os.path.join(ROOT, ".claude", ".state"))
MARKS = os.path.join(STATE_DIR, "rules_for")
# Eski shakl: clear() uni ham tozalaydi, aks holda yetim qoladi.
LEGACY_LOG = os.path.join(STATE_DIR, "rules_for.json")

# Belgining yaroqlilik muddati. Uzoq sessiyada bir marta chaqirilgan
# narsa kun bo'yi amal qilmasligi kerak: kod o'zgaradi, qoida ham.
MAX_AGE = 6 * 3600


def resolve(path):
    """Belgi kaliti: mutlaq, symlinksiz va registrga befarq yo'l.

    Nisbiy yo'l chaqiruvchining joriy papkasiga nisbatan hal qilinadi:
    global o'rnatishda rules_for boshqa proyektdan nisbiy yo'l bilan
    chaqiriladi, hook esa mutlaq yo'l beradi. normcase Windows dagi
    `c:`/`C:` va slash farqini yopadi.
    """
    return os.path.normcase(os.path.realpath(path))


def _marker(path):
    digest = hashlib.sha1(resolve(path).encode("utf-8")).hexdigest()
    return os.path.join(MARKS, digest)


def _prune(now):
    """Eskirgan belgilar o'chiriladi, aks holda papka cheksiz o'sadi."""
    for name in os.listdir(MARKS):
        full = os.path.join(MARKS, name)
        try:
            if now - os.path.getmtime(full) > MAX_AGE:
                os.remove(full)
        except OSError:
            pass  # boshqa jarayon allaqachon o'chirgan


def mark(paths, labels=()):
    """Shu fayllar uchun rules_for chaqirilganini va bergan belgilarini yozadi.

    Belgilar check_code uchun: yozilgan fayldan yangi belgi chiqsa, u
    yozuvchiga berilmagan boblarni aytadi.
    """
    body = json.dumps({"labels": sorted(set(labels))}, ensure_ascii=False)
    try:
        os.makedirs(MARKS, exist_ok=True)
        for path in paths:
            target = _marker(path)
            tmp = "%s.%d.tmp" % (target, os.getpid())
            with open(tmp, "w", encoding="utf-8") as handle:
                handle.write(body)
            os.replace(tmp, target)
        _prune(time.time())
    except OSError:
        pass  # belgilash ishni to'xtatmaydi


def was_marked(path):
    """Shu fayl uchun rules_for yaqinda chaqirilganmi."""
    try:
        age = time.time() - os.path.getmtime(_marker(path))
    except OSError:
        return False
    return age < MAX_AGE


def marked_labels(path):
    """rules_for shu fayl uchun bergan belgilar; belgi bo'lmasa None."""
    if not was_marked(path):
        return None
    try:
        with open(_marker(path), encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return None
    labels = data.get("labels") if isinstance(data, dict) else None
    return set(labels) if isinstance(labels, list) else None


def clear():
    """Sinovlar uchun: holatni tozalaydi."""
    shutil.rmtree(MARKS, ignore_errors=True)
    try:
        os.remove(LEGACY_LOG)
    except OSError:
        pass
