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
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX = os.path.join(ROOT, "index")
BUILD = os.path.join(HERE, "build_index.py")

_cache = {}
_files = {}
_checked = False


def ensure_index(name=""):
    """Indeks yo'q, chala yoki eskirgan bo'lsa bir marta yasaydi.

    Indeks hosila va git ga kirmaydi. U yo'q bo'lganda bu modul avval
    jim turib bo'sh ro'yxat qaytarardi: topilmalar chiqar, lekin bo'lim
    raqami yo'q, va nega yo'qligini hech kim aytmasdi. Bob tahrirlangandan
    keyin esa eski bo'lim raqamini berardi. Fayllar birga yasaladi,
    shuning uchun tekshiruv butun indeks bo'yicha; `name` chaqiruvchi qaysi
    faylga tayanishini bildiradi xolos.

    build_index.py to'g'ridan-to'g'ri chaqiriladi, bash shart emas: doc.sh
    orqali chaqirilganda Windows da indeks hech qachon yasalmasdi. Alohida
    jarayonda, chunki build() chiqishi check_code hookining JSON iga
    aralashmasin.
    """
    global _checked
    if _checked:
        return
    _checked = True   # yasash yiqilsa ham ikkinchi marta urinilmaydi
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        import build_index   # faqat kerak bo'lganda yuklanadi
        if build_index.is_fresh():
            return
    except (ImportError, SyntaxError):
        return   # yasovchining o'zi buzuq: bor indeks bilan davom etiladi
    try:
        subprocess.run([sys.executable or "python3", BUILD],
                       stdin=subprocess.DEVNULL, capture_output=True,
                       timeout=120, check=False)
    except (OSError, subprocess.SubprocessError):
        pass


def _rows(name):
    if name in _cache:
        return _cache[name]
    ensure_index(name)
    path = os.path.join(INDEX, name)
    rows = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            handle.readline()
            for line in handle:
                rows.append(line.rstrip("\n").split("\t"))
    _cache[name] = rows
    return rows


def _body(doc, section):
    """Bo'lim tanasi, sections.tsv dagi satr oralig'i bo'yicha."""
    for parts in _rows("sections.tsv"):
        if len(parts) >= 7 and parts[0] == doc and parts[1] == section:
            rel, start, end = parts[4], int(parts[5]), int(parts[6])
            if rel not in _files:
                try:
                    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
                        _files[rel] = f.read().split("\n")
                except OSError:
                    _files[rel] = []
            return "\n".join(_files[rel][start - 1:end])
    return ""


def by_ref(ref):
    """Aniq havola ("code-review 19.2") indeksda bo'lsa o'zi, bo'lmasa "".

    Raqam satr sifatida solishtiriladi: 24.10 va 24.1 boshqa bo'limlar.
    """
    doc, _, num = ref.partition(" ")
    name = "sections.tsv" if "." in num else "chapters.tsv"
    for parts in _rows(name):
        if len(parts) >= 2 and parts[0] == doc and parts[1] == num:
            return ref
    return ""


def by_rule(rule, term=""):
    """Sonar kaliti -> "<hujjat> <raqam>".

    rules.tsv ko'zga tashlanish bo'yicha saralangan, shuning uchun `term`
    berilmasa birinchi mos qator olinadi. Ulush ba'zan kalitni
    yo'l-yo'lakay eslatgan kichik bo'limni uni tushuntirgan bo'limdan
    yuqori qo'yadi. `term` (topilmaning o'zidagi so'z, masalan
    `printStackTrace`) berilsa, bo'lim qatorlaridan tanasida shu so'z ko'p
    uchragani olinadi, tenglikni ulush hal qiladi.
    """
    rows = [p for p in _rows("rules.tsv") if len(p) >= 6 and p[0] == rule]
    if not rows:
        return ""
    best = rows[0]
    sections = [p for p in rows if p[3]]
    if term and sections:
        best = max(sections, key=lambda p: (_body(p[1], p[3]).count(term),
                                            float(p[5])))
    return "%s %s" % (best[1], best[3] or best[2])


def by_topic(topic):
    """Inglizcha atama -> "<hujjat> <raqam>".

    Avval aynan moslik, keyin qavsli bezak bilan turgan nom: jadvalda
    "Money (Value Object specialization)", so'rovda esa "Money". Oddiy
    prefiks olinmaydi: u "Enum" ni "Enum Singleton" ga, "Index" ni
    "Index Table" ga olib borardi.
    """
    low = topic.lower()
    prefix = None
    for parts in _rows("aliases.tsv"):
        if len(parts) != 4 or parts[2] != "section":
            continue
        name = parts[0].lower()
        if name == low:
            return "%s %s" % (parts[1], parts[3])
        if prefix is None and name.startswith(low + " ("):
            prefix = "%s %s" % (parts[1], parts[3])
    return prefix or ""


def resolve(topic, rule="", ref="", term=""):
    """Bo'lim havolasi yoki bo'sh satr.

    Tartib aniqlik bo'yicha: topilma bilgan bo'lim, keyin Sonar kaliti,
    oxirida taxallus. Indeksda yo'q havola keyingisiga o'tadi.
    """
    return ((by_ref(ref) if ref else "")
            or (by_rule(rule, term) if rule else "")
            or by_topic(topic))


def hint(topic, rule="", ref="", term=""):
    """Foydalanuvchiga ko'rsatiladigan bir qatorlik yo'l-yo'riq."""
    found = resolve(topic, rule, ref, term)
    if found:
        return "qo'llanma: tools/doc.sh show %s" % found
    return "qo'llanma: tools/doc.sh find \"%s\"" % topic
