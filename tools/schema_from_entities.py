#!/usr/bin/env python3
"""JPA entity sinflaridan baza sxemasini va ehtimoliy muammolarni chiqaradi.

    python3 tools/schema_from_entities.py <manba_papka> [--json] [--only-findings]

Nega: baza tuzilishini bilish uchun konteyner ko'tarish, ulanish ochish va
`\\d+` yurgizish shart emas. Entity sinflari sxemani allaqachon to'liq
tasvirlaydi, ularni o'qish esa bir necha millisekund va nol pul turadi.
Topilgan muammolar ham xuddi shunday: `@ManyToOne` ning default fetch
turi EAGER ekanini ko'rish uchun so'rov yurgizish kerak emas, buni kod
aytib turibdi.

Chiqish ikki qism: jadval tuzilishi va ogohlantirishlar. Har bir
ogohlantirish qo'llanmadagi tegishli mavzuga ulanadi, shuning uchun
"nega yomon" degan savolga javob bir buyruq narida turadi.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from docref import hint  # noqa: E402

ENTITY_RE = re.compile(r"@Entity\b")
CLASS_RE = re.compile(r"\b(?:public\s+)?(?:final\s+)?class\s+(\w+)")
TABLE_RE = re.compile(r'@Table\s*\(([^)]*)\)', re.S)
NAME_ARG_RE = re.compile(r'name\s*=\s*"([^"]+)"')
COLUMN_LIST_RE = re.compile(r'columnList\s*=\s*"([^"]+)"')
# Maydon: oldidagi annotatsiyalar bloki + tur + nom
FIELD_RE = re.compile(
    r"((?:@\w+(?:\s*\([^)]*\))?\s*)*)"
    r"(?:private|protected|public)\s+"
    r"([\w<>,.\[\]\s]+?)\s+(\w+)\s*(?:=[^;]*)?;",
    re.S,
)

JAVA_TO_SQL = {
    "String": "varchar",
    "UUID": "uuid",
    "Long": "bigint", "long": "bigint",
    "Integer": "integer", "int": "integer",
    "Short": "smallint", "short": "smallint",
    "Boolean": "boolean", "boolean": "boolean",
    "BigDecimal": "numeric",
    "Double": "double precision", "double": "double precision",
    "Float": "real", "float": "real",
    "Instant": "timestamptz",
    "OffsetDateTime": "timestamptz",
    "ZonedDateTime": "timestamptz",
    "LocalDateTime": "timestamp",
    "LocalDate": "date",
    "LocalTime": "time",
    "Duration": "interval",
    "byte[]": "bytea",
    # Eski turlar: xaritalanadi, lekin check() ogohlantiradi.
    "Date": "timestamp",
    "Calendar": "timestamp",
}

COLLECTION_RE = re.compile(r"^(List|Set|Collection|Map)\s*<")


def snake(name):
    out = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    return re.sub(r"_+", "_", out)


def arg(block, pattern):
    match = pattern.search(block)
    return match.group(1) if match else None


def has(block, annotation):
    return re.search(r"@%s\b" % annotation, block) is not None


class Finding:
    def __init__(self, level, table, column, message, topic):
        self.level = level
        self.table = table
        self.column = column
        self.message = message
        self.topic = topic

    def as_dict(self):
        return {"level": self.level, "table": self.table,
                "column": self.column, "message": self.message,
                "topic": self.topic}


def parse_entity(text, path):
    """Bitta fayldagi entity: jadval nomi, ustunlar, bog'lanishlar."""
    if not ENTITY_RE.search(text):
        return None
    class_match = CLASS_RE.search(text)
    if not class_match:
        return None
    class_name = class_match.group(1)

    table_block = TABLE_RE.search(text)
    table_args = table_block.group(1) if table_block else ""
    table = arg(table_args, NAME_ARG_RE) or snake(class_name)
    declared_indexes = [c.replace(" ", "")
                        for c in COLUMN_LIST_RE.findall(table_args)]

    columns, relations = [], []
    body = text[class_match.end():]
    for ann, java_type, field in FIELD_RE.findall(body):
        java_type = " ".join(java_type.split())
        if has(ann, "Transient") or "static" in ann:
            continue
        entry = {
            "field": field, "java": java_type, "ann": ann,
            "name": arg(ann, NAME_ARG_RE) or snake(field),
        }
        if has(ann, "ManyToOne") or has(ann, "OneToOne"):
            entry["name"] = arg(ann, NAME_ARG_RE) or snake(field) + "_id"
            entry["kind"] = "fk"
            relations.append(entry)
            columns.append(entry)
        elif has(ann, "OneToMany") or has(ann, "ManyToMany"):
            entry["kind"] = "collection"
            relations.append(entry)
        else:
            entry["kind"] = "column"
            columns.append(entry)

    return {"class": class_name, "table": table, "file": path,
            "columns": columns, "relations": relations,
            "indexes": declared_indexes}


def sql_type(entry):
    java = entry["java"]
    ann = entry["ann"]
    if entry.get("kind") == "fk":
        return "bigint"
    if has(ann, "Lob"):
        return "text"
    if has(ann, "Enumerated") and "STRING" not in ann:
        return "integer"
    # STRING enum ham, oddiy String ham varchar: ikkalasida @Column(length)
    # hisobga olinadi, aks holda e'lon qilingan uzunlik yo'qolib ketardi.
    base = "varchar" if has(ann, "Enumerated") else JAVA_TO_SQL.get(java)
    if base == "varchar":
        length = re.search(r"length\s*=\s*(\d+)", ann)
        return "varchar(%s)" % (length.group(1) if length else "255")
    if base == "numeric":
        precision = re.search(r"precision\s*=\s*(\d+)", ann)
        scale = re.search(r"scale\s*=\s*(\d+)", ann)
        if precision and scale:
            return "numeric(%s,%s)" % (precision.group(1), scale.group(1))
        return "numeric"
    return base or java.lower()


def check(entity):
    """Kodni o'qib aytish mumkin bo'lgan muammolar. Hech narsa ishga tushmaydi."""
    out = []
    table = entity["table"]
    indexed = set()
    for group in entity["indexes"]:
        indexed.update(group.split(","))

    # FK yozuvi ikkala ro'yxatda ham turadi (ustun sifatida ham, bog'lanish
    # sifatida ham), shuning uchun id bo'yicha bir marta ko'riladi.
    seen = set()
    entries = []
    for entry in entity["columns"] + entity["relations"]:
        if id(entry) not in seen:
            seen.add(id(entry))
            entries.append(entry)

    for entry in entries:
        ann, name, java = entry["ann"], entry["name"], entry["java"]

        if entry.get("kind") == "fk":
            if "fetch" not in ann:
                out.append(Finding(
                    "yuqori", table, name,
                    "@ManyToOne/@OneToOne da fetch ko'rsatilmagan, default EAGER. "
                    "Har o'qishda qo'shimcha JOIN yoki alohida so'rov keladi.",
                    "N+1 Problem Solutions"))
            if name not in indexed:
                out.append(Finding(
                    "yuqori", table, name,
                    "Tashqi kalit ustunida indeks e'lon qilinmagan. PostgreSQL "
                    "FK uchun indeksni avtomatik yasamaydi: JOIN va ota qator "
                    "o'chirilishi sekinlashadi.",
                    "Index"))

        if has(ann, "OneToMany") or has(ann, "ManyToMany"):
            if "FetchType.EAGER" in ann:
                out.append(Finding(
                    "yuqori", table, entry["field"],
                    "Kolleksiya EAGER yuklanadi. Ikkita EAGER kolleksiya "
                    "MultipleBagFetchException yoki dekart ko'paytmasini beradi.",
                    "N+1 Queries"))
            if has(ann, "OneToMany") and "mappedBy" not in ann:
                out.append(Finding(
                    "o'rta", table, entry["field"],
                    "@OneToMany da mappedBy yo'q: Hibernate kutilmaganda "
                    "qo'shimcha bog'lovchi jadval yasaydi.",
                    "Association Table Mapping"))

        if has(ann, "Enumerated") and "STRING" not in ann:
            out.append(Finding(
                "yuqori", table, name,
                "@Enumerated default ORDINAL: enum tartibi o'zgarsa bazadagi "
                "eski qatorlar boshqa qiymatga aylanadi.",
                "Enum"))

        if java == "BigDecimal" and "precision" not in ann:
            out.append(Finding(
                "yuqori", table, name,
                "Pul maydonida precision/scale yo'q: yaxlitlash xatosi va "
                "bazada kutilmagan aniqlik.",
                "Money"))

        if java == "String" and "length" not in ann and not has(ann, "Lob"):
            out.append(Finding(
                "past", table, name,
                "Uzunlik ko'rsatilmagan, varchar(255) qabul qilinadi.",
                "Validation"))

        if java in ("Date", "Calendar", "java.util.Date"):
            out.append(Finding(
                "o'rta", table, name,
                "Eski sana turi. java.time (Instant yoki LocalDate) "
                "mintaqa xatolarini oldini oladi.",
                "Date"))

    if not any(has(c["ann"], "Id") for c in entity["columns"]):
        out.append(Finding(
            "yuqori", table, "-", "@Id topilmadi.", "Identity Field"))
    if not any(has(c["ann"], "Version") for c in entity["columns"]):
        out.append(Finding(
            "past", table, "-",
            "@Version yo'q: bir vaqtda yangilash jim yo'qotishga olib keladi.",
            "Optimistic Offline Lock"))
    return out


def collect(src):
    entities = []
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = [d for d in dirnames
                       if d not in {".git", "target", "build", "node_modules"}]
        for name in sorted(filenames):
            if not name.endswith(".java"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8", errors="replace") as handle:
                parsed = parse_entity(handle.read(), os.path.relpath(path, src))
            if parsed:
                entities.append(parsed)
    return entities


LEVEL_ORDER = {"yuqori": 0, "o'rta": 1, "past": 2}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if not args:
        print(__doc__.strip().split("\n\n")[1].strip())
        return 2
    src = args[0]
    if not os.path.isdir(src):
        print("papka yo'q: %s" % src, file=sys.stderr)
        return 2

    entities = collect(src)
    if not entities:
        print("entity topilmadi: %s" % src, file=sys.stderr)
        return 1

    findings = []
    for entity in entities:
        findings.extend(check(entity))
    findings.sort(key=lambda f: (LEVEL_ORDER.get(f.level, 9), f.table, f.column))

    if "--json" in flags:
        json.dump({
            "entities": [{
                "class": e["class"], "table": e["table"], "file": e["file"],
                "columns": [{"name": c["name"], "type": sql_type(c),
                             "kind": c.get("kind")} for c in e["columns"]],
            } for e in entities],
            "findings": [f.as_dict() for f in findings],
        }, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0

    if "--only-findings" not in flags:
        print("# Sxema (%d entity, bazaga ulanmasdan)\n" % len(entities))
        for entity in sorted(entities, key=lambda e: e["table"]):
            print("%s  <- %s" % (entity["table"], entity["file"]))
            for col in entity["columns"]:
                mark = "PK" if has(col["ann"], "Id") else (
                    "FK" if col.get("kind") == "fk" else "  ")
                print("    %-2s %-26s %s" % (mark, col["name"], sql_type(col)))
            for rel in entity["relations"]:
                if rel.get("kind") == "collection":
                    print("    ..  %-26s %s" % (rel["field"], rel["java"]))
            print()

    print("# Ehtimoliy muammolar (%d ta, hech narsa ishga tushirilmadi)\n"
          % len(findings))
    for f in findings:
        print("[%s] %s.%s" % (f.level, f.table, f.column))
        print("    %s" % f.message)
        print("    %s" % hint(f.topic))
    return 0


if __name__ == "__main__":
    sys.exit(main())
