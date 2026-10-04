#!/usr/bin/env python3
"""docs/ dan qidiruv indeksini yasaydi.

    python3 tools/build_index.py

Manba - docs/manifest.json va undagi bob fayllari. Chiqish - index/ dagi
to'rtta TSV. Hujjatlarga tegilmaydi, indeks butunlay hosila.

Nega kerak: manifest har bob uchun faqat bo'lim SONINI saqlaydi, nomini emas.
Bo'limni nomi yoki inglizcha atamasi bo'yicha topish uchun alohida indeks
kerak. Bitta bo'lim ~700 token, eng katta bob esa ~68k, shuning uchun
qidiruv bob emas, bo'lim darajasida bo'lishi kerak.
"""

import json
import os
import re
import sys

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

# `n+1`, `c++` kabi atamalar bitta token bo'lib qolishi kerak.
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


def index_chapter(doc_key, chapter, rel_path, rows):
    """Bitta bob faylini o'qib, bob va bo'lim qatorlarini to'playdi."""
    lines = read_lines(os.path.join(ROOT, rel_path))
    headings = parse_headings(lines)
    ends = assign_ends(headings, len(lines))
    num = str(chapter["num"]) if chapter.get("num") is not None else ""

    for (level, lineno, title), end in zip(headings, ends):
        if level == 1:
            rows["chapters"].append(
                (doc_key, num, clean(title), rel_path, lineno, end, gh_slug(title))
            )
            alias = english_alias(title)
            if num and alias:
                rows["aliases"].append((clean(alias), doc_key, "chapter", num))
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


def build():
    manifest = json.load(open(os.path.join(DOCS_DIR, "manifest.json"), encoding="utf-8"))
    rows = {"chapters": [], "sections": [], "aliases": [], "known": set()}
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

    df = build_df(rows["sections"])
    write("df.tsv", ["token", "sections"],
          sorted(df.items(), key=lambda kv: (-kv[1], kv[0])))


    print("index: %d hujjat, %d bob, %d bo'lim, %d taxallus, %d so'z chastotasi"
          % (len(doc_rows), len(rows["chapters"]), len(rows["sections"]),
             len(aliases), len(df)))


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


def write(name, header, data):
    with open(os.path.join(INDEX_DIR, name), "w", encoding="utf-8") as handle:
        handle.write("\t".join(header) + "\n")
        for row in data:
            handle.write("\t".join(str(cell) for cell in row) + "\n")


if __name__ == "__main__":
    build()
