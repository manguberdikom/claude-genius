#!/usr/bin/env python3
"""schema_from_entities.py uchun sinovlar.

    python3 tools/test_schema.py

tools/testdata/entities/ dagi ikkita entity ataylab qarama-qarshi yozilgan:
Order.java da tipik xatolar bor, Customer.java esa toza. Shunda ikkala
yo'nalish ham sinaladi: muammoni ko'rish va toza kodni tinch qo'yish.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "schema_from_entities.py")
DATA = os.path.join(HERE, "testdata", "entities")

# Sxema chiqishida bo'lishi shart bo'lgan satrlar.
SCHEMA_EXPECT = [
    ("jadval nomi @Table dan olinadi", "orders"),
    ("nom berilmasa snake_case", "order_no"),
    ("@ManyToOne -> _id ustuni", "customer_id"),
    ("length -> varchar(n)", "varchar(32)"),
    ("Instant -> timestamptz", "timestamptz"),
    ("ORDINAL enum -> integer", "integer"),
    ("STRING enum -> varchar", "varchar(20)"),
]

# (jadval, ustun, matn bo'lagi) uchligi topilmalar ichida bo'lishi shart.
FINDING_EXPECT = [
    ("orders", "customer_id", "default EAGER"),
    ("orders", "customer_id", "indeks"),
    ("orders", "lines", "EAGER yuklanadi"),
    ("orders", "lines", "mappedBy"),
    ("orders", "status", "ORDINAL"),
    ("orders", "total_amount", "precision"),
    ("orders", "note", "varchar(255)"),
    ("customers", "registered_at", "Eski sana"),
]

# Toza entity uchun bular CHIQMASLIGI kerak.
FINDING_ABSENT = [
    ("customers", "email", "indeks"),
    ("customers", "tier", "ORDINAL"),
    ("customers", "-", "@Version yo'q"),
    ("customers", "orders", "EAGER"),
]


def run(*args):
    proc = subprocess.run([sys.executable, TOOL, DATA] + list(args),
                          capture_output=True, text=True, cwd=ROOT)
    return proc.stdout


def findings(payload):
    return [(f["table"], f["column"], f["message"]) for f in payload["findings"]]


def main():
    import json

    if not os.path.isdir(DATA):
        print("sinov ma'lumoti yo'q: %s" % DATA)
        return 1

    failures = 0
    text = run()

    print("== Sxema ==")
    for label, needle in SCHEMA_EXPECT:
        ok = needle in text
        failures += not ok
        print("%-4s %-34s %s" % ("OK" if ok else "XATO", label, needle))

    payload = json.loads(run("--json"))
    found = findings(payload)

    print("\n== Topilishi kerak ==")
    for table, column, needle in FINDING_EXPECT:
        ok = any(t == table and c == column and needle in m for t, c, m in found)
        failures += not ok
        print("%-4s %s.%s  %s" % ("OK" if ok else "XATO", table, column, needle))

    print("\n== Chiqmasligi kerak (toza entity) ==")
    for table, column, needle in FINDING_ABSENT:
        ok = not any(t == table and c == column and needle in m
                     for t, c, m in found)
        failures += not ok
        print("%-4s %s.%s  %s" % ("OK" if ok else "XATO", table, column, needle))

    print("\n== Takrorlanish yo'q ==")
    duplicated = len(found) != len(set(found))
    failures += duplicated
    print("%-4s %d ta topilma, %d tasi noyob"
          % ("XATO" if duplicated else "OK", len(found), len(set(found))))

    total = len(SCHEMA_EXPECT) + len(FINDING_EXPECT) + len(FINDING_ABSENT) + 1
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
