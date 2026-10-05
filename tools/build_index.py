#!/usr/bin/env python3
"""docs/ dan qidiruv indeksini yasaydi.

    python3 tools/build_index.py

Manba - docs/manifest.json va undagi bob fayllari. Chiqish - index/ dagi
TSV fayllar va oxirida yoziladigan `.stamp` belgisi. Hujjatlarga
tegilmaydi, indeks butunlay hosila.

Nega kerak: manifest har bob uchun faqat bo'lim SONINI saqlaydi, nomini emas.
Bo'limni nomi yoki inglizcha atamasi bo'yicha topish uchun alohida indeks
kerak. Bitta bo'lim ~700 token, eng katta bob esa ~68k, shuning uchun
qidiruv bob emas, bo'lim darajasida bo'lishi kerak.
"""

import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX_DIR = os.path.join(ROOT, "index")
DOCS_DIR = os.path.join(ROOT, "docs")

# Anchor hisoblash mantig'i check_docs.py da. Nusxa ko'chirilsa ikkisi
# vaqt o'tib bir-biridan uzoqlashadi, shuning uchun import qilinadi.
sys.path.insert(0, HERE)
from check_docs import gh_slug  # noqa: E402

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*?)\s*$")
SECTION_NUM_RE = re.compile(r"^(\d+\.\d+)\s")
# "- [Abstract Factory](01-....md#18-abstrakt-fabrika) - 1.8"
ALIAS_RE = re.compile(r"^- \[(.+?)\]\([^)]*\)\s*-\s*(\d+\.\d+)\s*$")
# Sarlavha oxiridagi qavs ichidagi inglizcha nom, ichki qavslarga chidamli.
PAREN_RE = re.compile(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*$")

ALIAS_FILE = "99-alifbo-boyicha-indeks.md"

# build() yozadigan fayllar: is_fresh() hammasi borligini talab qiladi.
OUTPUTS = ("docs.tsv", "chapters.tsv", "sections.tsv", "aliases.tsv",
           "rules.tsv", "checklist.tsv", "df.tsv")
# Hamma fayldan keyin yoziladi: u bor bo'lsa indeks to'liq. Vaqti build
# BOSHLANGAN payt, shuning uchun build paytida tahrirlangan bob keyingi
# chaqiruvda baribir qayta yasaladi. doc.sh ensure_index ham shunga qaraydi.
STAMP = ".stamp"

# `n+1`, `c++` kabi atamalar bitta token bo'lib qolishi kerak.
RULE_RE = re.compile(r"\bjava:S\d+\b")
CHECKBOX_RE = re.compile(r"^\s*- \[ \]\s+(.*?)\s*$")

WORD_RE = re.compile(r"[a-z0-9_.@#]+(?:\+\+|\+\d+)?(?:'[a-z0-9]+)*")


def clean(text):
    """TSV ni buzmaydigan bir satrli matn."""
    return text.replace("\t", " ").replace("\n", " ").strip()


def read_lines(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().split("\n")


def parse_headings(lines):
    """(daraja, satr_raqami, sarlavha) ro'yxati, kod bloklaridan tashqari."""
    headings = []
    in_fence = False
    for lineno, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((len(match.group(1)), lineno, match.group(2)))
    return headings


def assign_ends(headings, total_lines):
    """Har bir sarlavha keyingi teng yoki yuqori darajadagisigacha davom etadi."""
    ends = []
    for i, (level, _, _) in enumerate(headings):
        end = total_lines
        for next_level, next_lineno, _ in headings[i + 1:]:
            if next_level <= level:
                end = next_lineno - 1
                break
        ends.append(end)
    return ends


def english_alias(title):
    """Sarlavha oxiridagi qavs ichidagi inglizcha nom, bo'lmasa None."""
    match = PAREN_RE.search(title)
    if not match:
        return None
    candidate = match.group(1).strip()
    if not candidate or len(candidate) > 120:
        return None
    if not re.search(r"[A-Za-z]", candidate):
        return None
    return candidate


def parse_alias_file(path, doc_key, known_sections):
    """Alifbo indeksidagi inglizcha nomlarni bo'lim raqamiga bog'laydi."""
    aliases = []
    for line in read_lines(path):
        match = ALIAS_RE.match(line)
        if match and match.group(2) in known_sections:
            aliases.append((clean(match.group(1)), doc_key, "section", match.group(2)))
    return aliases


def scan_body(doc_key, chapter, section, body, rows):
    """Bo'lim tanasidan Sonar qoida kalitlari va tekshiruv punktlarini oladi.

    Ikkalasi ham korpusda allaqachon mashina o'qiydigan shaklda yotibdi:
    98 ta `java:Sxxxx` kaliti va 2000 dan ortiq `- [ ]` punkti. Indekssiz
    ularni faqat odam ko'radi.
    """
    if not section and not chapter:
        return
    text = "\n".join(body)
    for rule in set(RULE_RE.findall(text)):
        rows["rules"].append(
            (rule, doc_key, chapter, section, text.count(rule))
        )
    for line in body:
        match = CHECKBOX_RE.match(line)
        if match:
            rows["checklist"].append(
                (doc_key, chapter, section, clean(match.group(1)))
            )


def index_chapter(doc_key, chapter, rel_path, rows):
    """Bitta bob faylini o'qib, bob va bo'lim qatorlarini to'playdi."""
    lines = read_lines(os.path.join(ROOT, rel_path))
    headings = parse_headings(lines)
    ends = assign_ends(headings, len(lines))
    num = str(chapter["num"]) if chapter.get("num") is not None else ""

    # Bobning muqaddimasi: H1 dan birinchi bo'limgacha. Katalog jadvallari
    # aynan shu yerda turadi, shuning uchun u ham skanlanadi. H1 ning o'z
    # oralig'i butun bobni qamraydi, undan foydalanilsa hammasi ikki marta
    # sanalardi.
    first_section = next((ln for lvl, ln, _ in headings if lvl == 2), len(lines) + 1)

    for (level, lineno, title), end in zip(headings, ends):
        if level == 1:
            rows["chapters"].append(
                (doc_key, num, clean(title), rel_path, lineno, end, gh_slug(title))
            )
            alias = english_alias(title)
            if num and alias:
                rows["aliases"].append((clean(alias), doc_key, "chapter", num))
            scan_body(doc_key, num, "", lines[lineno:first_section - 1], rows)
        elif level == 2:
            match = SECTION_NUM_RE.match(title)
            section = match.group(1) if match else ""
            rows["sections"].append(
                (doc_key, section, num, clean(title), rel_path,
                 lineno, end, gh_slug(title))
            )
            if section:
                rows["known"].add((doc_key, section))
                alias = english_alias(title)
                if alias:
                    rows["aliases"].append(
                        (clean(alias), doc_key, "section", section)
                    )
            # Tana shu yerda qo'lda, chunki satrlar allaqachon o'qilgan:
            # alohida yurish fayllarni ikkinchi marta ochishni talab qilardi.
            scan_body(doc_key, num, section, lines[lineno:end], rows)


def build():
    started = time.time()
    manifest = json.load(open(os.path.join(DOCS_DIR, "manifest.json"), encoding="utf-8"))
    rows = {"chapters": [], "sections": [], "aliases": [], "known": set(),
            "rules": [], "checklist": []}
    doc_rows = []

    for doc_key, doc in manifest.items():
        doc_dir = os.path.join("docs", doc_key)
        total_bytes = 0
        before = len(rows["sections"])

        for chapter in doc["chapters"]:
            rel_path = os.path.join(doc_dir, chapter["file"])
            full = os.path.join(ROOT, rel_path)
            if not os.path.exists(full):
                sys.stderr.write("yo'q: %s\n" % rel_path)
                continue
            total_bytes += os.path.getsize(full)
            index_chapter(doc_key, chapter, rel_path, rows)

        doc_rows.append((
            doc_key,
            doc.get("label", doc_key),
            clean(doc.get("title", "")),
            doc_dir,
            len(doc["chapters"]),
            len(rows["sections"]) - before,
            total_bytes,
        ))

        alias_path = os.path.join(ROOT, doc_dir, ALIAS_FILE)
        if os.path.exists(alias_path):
            known = {s for d, s in rows["known"] if d == doc_key}
            rows["aliases"].extend(parse_alias_file(alias_path, doc_key, known))

    aliases = sorted(
        set(rows["aliases"]), key=lambda r: (r[0].lower(), r[1], r[2], r[3])
    )

    os.makedirs(INDEX_DIR, exist_ok=True)
    write("docs.tsv",
          ["doc", "label", "title", "dir", "chapters", "sections", "bytes"],
          sorted(doc_rows))
    write("chapters.tsv",
          ["doc", "chapter", "title", "file", "start", "end", "anchor"],
          rows["chapters"])
    write("sections.tsv",
          ["doc", "section", "chapter", "title", "file", "start", "end", "anchor"],
          rows["sections"])
    write("aliases.tsv", ["alias", "doc", "kind", "ref"], aliases)

    # Bir kalit bir necha bo'limda uchraydi. Ko'p uchragani odatda uni
    # tushuntirgan bo'lim, bir marta uchragani esa ro'yxatda eslatilgan.
    # Reyting: sanoqning o'zi aldaydi. Yigirmata kalit sanab o'tgan
    # katalog qatori ham, bitta kalitni tushuntirgan bo'lim ham kalitni
    # bir necha marta tilga oladi. Shuning uchun ulush = sanoq / bo'limdagi
    # turli kalitlar soni. Bu nisbat emas, 1 dan oshishi mumkin (S2925 19.4
    # da 3.0). Kalitni yo'l-yo'lakay eslatgan kichik bo'lim ham yuqori
    # chiqishi mumkin: docref.by_rule buni topilma so'zi bilan aniqlaydi.
    per_section = {}
    for rule, doc, chapter, section, _ in set(rows["rules"]):
        per_section.setdefault((doc, chapter, section), set()).add(rule)
    rules = []
    for rule, doc, chapter, section, count in set(rows["rules"]):
        distinct = len(per_section[(doc, chapter, section)])
        rules.append((rule, doc, chapter, section, count,
                      round(count / distinct, 3)))
    rules.sort(key=lambda r: (r[0], -r[5], -r[4], r[1], r[2], r[3]))
    write("rules.tsv",
          ["rule", "doc", "chapter", "section", "marta", "ulush"], rules)
    write("checklist.tsv", ["doc", "chapter", "section", "item"],
          rows["checklist"])

    df = build_df(rows["sections"])
    write("df.tsv", ["token", "sections"],
          sorted(df.items(), key=lambda kv: (-kv[1], kv[0])))

    summary = ("index: %d hujjat, %d bob, %d bo'lim, %d taxallus, %d so'z, "
               "%d qoida kaliti, %d tekshiruv punkti"
               % (len(doc_rows), len(rows["chapters"]), len(rows["sections"]),
                  len(aliases), len(df), len({r[0] for r in rules}),
                  len(rows["checklist"])))
    write(STAMP, [], [(summary,)], mtime=started)
    return summary


def word_tokens(text):
    return {t for t in (x.strip(".") for x in WORD_RE.findall(text.lower()))
            if len(t) > 1 or not t.isalpha()}


def build_df(section_rows):
    """Sarlavha so'zlari nechta bo'lim TANASIDA uchrashini sanaydi.

    Nega tana bo'yicha: sarlavhalar qisqa, shuning uchun u yerda `yaxshi`
    ham, `deadlock` ham bir necha marta uchraydi va ikkalasi teng kamyob
    ko'rinadi. Tana bo'yicha sanalganda `yaxshi` yuzlab bo'limda chiqadi,
    `deadlock` esa o'nlarida: taklif qilish uchun farq shu yerda.
    """
    wanted = set()
    for row in section_rows:
        wanted |= word_tokens(row[3])

    cache = {}
    df = dict.fromkeys(wanted, 0)
    for row in section_rows:
        path = row[4]
        if path not in cache:
            cache[path] = read_lines(os.path.join(ROOT, path))
        body = "\n".join(cache[path][row[5] - 1:row[6]])
        for token in word_tokens(body) & wanted:
            df[token] += 1
    return df


def write(name, header, data, mtime=None):
    """Faylni atomik almashtiradi: avval vaqtinchalik nusxa, keyin os.replace.

    Joyida qayta yozilganda rebuild paytida parallel o'quvchi (boshqa
    doc.sh yoki hook) bo'sh yoki yarim faylni ko'rardi.
    """
    path = os.path.join(INDEX_DIR, name)
    tmp = "%s.%d.tmp" % (path, os.getpid())
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            if header:
                handle.write("\t".join(header) + "\n")
            for row in data:
                handle.write("\t".join(str(cell) for cell in row) + "\n")
        if mtime is not None:
            os.utime(tmp, (mtime, mtime))
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def sources():
    """Indeks tayanadigan fayllar: bob matnlari, manifest va shu skript."""
    yield os.path.abspath(__file__)
    for folder, _, names in os.walk(DOCS_DIR):
        for name in names:
            if name.endswith(".md") or name == "manifest.json":
                yield os.path.join(folder, name)


def is_fresh():
    """Indeks to'liq va hech bir manbadan eski emas.

    Faqat fayl borligiga qarash yetmaydi: eski klonda keyin qo'shilgan
    rules.tsv yoki df.tsv yo'q, bob tahrirlangandan keyin esa satr
    raqamlari jimgina noto'g'ri bo'ladi.
    """
    try:
        built = os.path.getmtime(os.path.join(INDEX_DIR, STAMP))
    except OSError:
        return False
    if not all(os.path.exists(os.path.join(INDEX_DIR, n)) for n in OUTPUTS):
        return False
    return all(os.path.getmtime(path) <= built for path in sources())


if __name__ == "__main__":
    print(build())
