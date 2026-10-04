#!/usr/bin/env python3
"""Hujjatlardan qidiruv indeksini yasaydi.

Manba - to'rtta monolit .md fayl. Chiqish - index/ katalogidagi TSV fayllar:
docs.tsv, chapters.tsv, sections.tsv, aliases.tsv. Hujjatlar o'zgarmaydi.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_DIR = os.path.join(ROOT, "index")

# qisqa kalit -> fayl nomi
DOCS = {
    "patterns": "java-spring-design-patterns.md",
    "mindset": "java-spring-architect-mindset.md",
    "sonar": "java-spring-sonarqube.md",
    "testing": "java-spring-testing-handbook.md",
}

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*?)\s*$")
CHAPTER_NUM_RE = re.compile(r"^(\d+)\.\s")
SECTION_NUM_RE = re.compile(r"^(\d+\.\d+)\s")
# "- [Abstract Factory](#18-...) — 1.8"
ALIAS_RE = re.compile(r"^- \[(.+?)\]\(#[^)]*\)\s*[—-]\s*(\d+\.\d+)\s*$")
# sarlavha oxiridagi inglizcha nom: "Zanjirni uzgich (Circuit Breaker)"
PAREN_RE = re.compile(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)\s*$")

TAB_SUB = " "


def clean(text):
    """TSV ni buzmaydigan bir satrli matn."""
    return text.replace("\t", TAB_SUB).replace("\n", " ").strip()


def parse_headings(path):
    """Fayldan (daraja, satr_raqami, sarlavha) ro'yxatini oladi.

    Kod bloklari ichidagi '#' belgilari sarlavha emas, shuning uchun
    ``` va ~~~ chegaralari kuzatiladi.
    """
    headings = []
    in_fence = False
    with open(path, encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = HEADING_RE.match(line)
            if match:
                headings.append((len(match.group(1)), lineno, match.group(2)))
    return headings


def line_count(path):
    with open(path, encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def assign_ends(headings, total_lines):
    """Har bir sarlavhaning oxirgi satrini belgilaydi.

    Bo'lim keyingi teng yoki yuqori darajadagi sarlavhagacha davom etadi,
    shuning uchun 3-daraja bo'lim keyingi 2-daraja bobga o'tib ketmaydi.
    """
    ends = []
    for i, (level, lineno, _) in enumerate(headings):
        end = total_lines
        for next_level, next_lineno, _ in headings[i + 1:]:
            if next_level <= level:
                end = next_lineno - 1
                break
        ends.append(end)
    return ends


def english_alias(title):
    """Sarlavha oxiridagi qavs ichidagi inglizcha nomni qaytaradi."""
    match = PAREN_RE.search(title)
    if not match:
        return None
    candidate = match.group(1).strip()
    if not candidate or len(candidate) > 120:
        return None
    # kamida bitta lotin harfi bo'lsin, sof raqam yoki belgi emas
    if not re.search(r"[A-Za-z]", candidate):
        return None
    return candidate


def parse_aliases(path, doc_key, section_nums):
    """Patternlar hujjati oxiridagi alifbo indeksidan inglizcha nomlarni oladi."""
    aliases = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            match = ALIAS_RE.match(line.rstrip("\n"))
            if not match:
                continue
            name, num = match.group(1), match.group(2)
            if num in section_nums:
                aliases.append((clean(name), doc_key, "section", num))
    return aliases


def build():
    docs_rows = []
    chapter_rows = []
    section_rows = []
    alias_rows = []

    for doc_key, filename in DOCS.items():
        path = os.path.join(ROOT, filename)
        if not os.path.exists(path):
            sys.stderr.write("yo'q: %s\n" % filename)
            continue

        total = line_count(path)
        headings = parse_headings(path)
        ends = assign_ends(headings, total)

        current_chapter = ""
        n_chapters = 0
        n_sections = 0
        section_nums = set()

        for (level, lineno, title), end in zip(headings, ends):
            if level == 2:
                match = CHAPTER_NUM_RE.match(title)
                current_chapter = match.group(1) if match else ""
                chapter_rows.append(
                    (doc_key, current_chapter, clean(title), filename, lineno, end)
                )
                n_chapters += 1
                if current_chapter:
                    alias = english_alias(title)
                    if alias:
                        alias_rows.append(
                            (clean(alias), doc_key, "chapter", current_chapter)
                        )
            elif level == 3:
                match = SECTION_NUM_RE.match(title)
                num = match.group(1) if match else ""
                section_rows.append(
                    (doc_key, num, current_chapter, clean(title), filename, lineno, end)
                )
                n_sections += 1
                if num:
                    section_nums.add(num)
                    alias = english_alias(title)
                    if alias:
                        alias_rows.append((clean(alias), doc_key, "section", num))

        docs_rows.append(
            (doc_key, filename, os.path.getsize(path), total, n_chapters, n_sections)
        )

        if doc_key == "patterns":
            alias_rows.extend(parse_aliases(path, doc_key, section_nums))

    # bir xil (nom, hujjat, raqam) uchligini bir marta yozamiz
    alias_rows = sorted(
        set(alias_rows), key=lambda row: (row[0].lower(), row[1], row[2], row[3])
    )

    os.makedirs(INDEX_DIR, exist_ok=True)
    write(
        "docs.tsv",
        ["doc", "file", "bytes", "lines", "chapters", "sections"],
        sorted(docs_rows),
    )
    write(
        "chapters.tsv",
        ["doc", "chapter", "title", "file", "start", "end"],
        chapter_rows,
    )
    write(
        "sections.tsv",
        ["doc", "section", "chapter", "title", "file", "start", "end"],
        section_rows,
    )
    write("aliases.tsv", ["alias", "doc", "kind", "ref"], alias_rows)

    print(
        "index: %d hujjat, %d bob, %d bo'lim, %d taxallus"
        % (len(docs_rows), len(chapter_rows), len(section_rows), len(alias_rows))
    )


def write(name, header, rows):
    path = os.path.join(INDEX_DIR, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\t".join(header) + "\n")
        for row in rows:
            handle.write("\t".join(str(cell) for cell in row) + "\n")


if __name__ == "__main__":
    build()
