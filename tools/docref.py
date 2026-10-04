#!/usr/bin/env python3
"""Mavzu yoki Sonar kalitini qo'llanmadagi bo'limga bog'laydi.

Ikkita asbob buni talab qiladi (schema_from_entities.py va check_code.py),
shuning uchun mantiq shu yerda: nusxa ko'chirilsa, biri tuzatilganda
ikkinchisi eskirib qolardi.

Topilma faqat "shunday qilma" desa, u shaxsiy did. Qo'llanmadagi bo'limni
ko'rsatsa, uni tekshirish mumkin. Shuning uchun har bir topilma shu
funksiyadan o'tadi.
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index")

_cache = {}


def _rows(name):
    if name in _cache:
        return _cache[name]
    path = os.path.join(INDEX, name)
    rows = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            handle.readline()
            for line in handle:
                rows.append(line.rstrip("\n").split("\t"))
    _cache[name] = rows
    return rows


def by_rule(rule):
    """Sonar kaliti -> "<hujjat> <raqam>". rules.tsv ko'zga tashlanish
    bo'yicha saralangan, shuning uchun birinchi mos qator eng yaxshisi."""
    for parts in _rows("rules.tsv"):
        if len(parts) >= 4 and parts[0] == rule:
            return "%s %s" % (parts[1], parts[3] or parts[2])
    return ""


def by_topic(topic):
    """Inglizcha atama -> "<hujjat> <raqam>".

    Avval aynan moslik, keyin atama bilan boshlanadigan taxallus:
    jadvalda nom bezak bilan turadi ("Money (Value Object specialization)"),
    so'rov esa sodda bo'ladi ("Money").
    """
    low = topic.lower()
    prefix = None
    for parts in _rows("aliases.tsv"):
        if len(parts) != 4 or parts[2] != "section":
            continue
        name = parts[0].lower()
        if name == low:
            return "%s %s" % (parts[1], parts[3])
        if prefix is None and name.startswith(low + " "):
            prefix = "%s %s" % (parts[1], parts[3])
    return prefix or ""


def resolve(topic, rule=""):
    """Bo'lim havolasi yoki bo'sh satr. Kalit aniqroq, shuning uchun oldin."""
    return (by_rule(rule) if rule else "") or by_topic(topic)


def hint(topic, rule=""):
    """Foydalanuvchiga ko'rsatiladigan bir qatorlik yo'l-yo'riq."""
    ref = resolve(topic, rule)
    if ref:
        return "qo'llanma: tools/doc.sh show %s" % ref
    return "qo'llanma: tools/doc.sh find \"%s\"" % topic
