#!/usr/bin/env python3
"""parse_test_output.py uchun sinovlar.

    python3 tools/test_parse_test_output.py

Ikki format sinaladi (Maven va Gradle), chunki stack qatorlari va
xulosa satri ularda boshqacha yoziladi. Gradle modul prefiksi qo'yadi
("at app//shop.Foo.bar"), Maven qo'ymaydi.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "parse_test_output.py")
DATA = os.path.join(HERE, "testdata")

CLEAN = "[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0\n[INFO] BUILD SUCCESS\n"

CASES = [
    ("maven: xulosa", "maven_fail.txt", "Tests: 24, yiqildi: 3"),
    ("maven: kutilgan qiymat", "maven_fail.txt", "kutilgan: 201"),
    ("maven: olingan qiymat", "maven_fail.txt", "olingan : 500"),
    ("maven: loyiha qatori", "maven_fail.txt",
     "OrderControllerTest.createsOrder(OrderControllerTest.java:58)"),
    ("maven: NPE xabari", "maven_fail.txt", "Cannot invoke"),
    ("gradle: xulosa", "gradle_fail.txt", "Tests: 2, yiqildi: 2"),
    ("gradle: modul prefiksi tashlandi", "gradle_fail.txt",
     "MoneyTest.addsAmounts(MoneyTest.java:24)"),
    ("gradle: ishlab chiqarish kodi", "gradle_fail.txt",
     "Money.<init>(Money.java:17)"),
    ("gradle: istisno turi", "gradle_fail.txt", "IllegalArgumentException"),
]

# Chiqishda bo'lmasligi kerak: framework stack qatorlari.
ABSENT = [
    ("maven_fail.txt", "org.junit"),
    ("maven_fail.txt", "jdk.internal"),
    ("maven_fail.txt", "AssertionFailureBuilder"),
    ("gradle_fail.txt", "org.junit"),
    ("gradle_fail.txt", "app//"),
]


def run(path=None, text=None):
    args = [sys.executable, TOOL] + ([path] if path else [])
    proc = subprocess.run(args, input=text, capture_output=True,
                          text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


def main():
    missing = [f for _, f, _ in CASES
               if not os.path.exists(os.path.join(DATA, f))]
    if missing:
        print("sinov ma'lumoti yo'q: %s" % ", ".join(sorted(set(missing))))
        return 1

    failures = 0
    cache = {}

    print("== Chiqishda bo'lishi kerak ==")
    for name, fixture, needle in CASES:
        if fixture not in cache:
            cache[fixture] = run(os.path.join(DATA, fixture))[1]
        ok = needle in cache[fixture]
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))

    print("\n== Chiqishda bo'lmasligi kerak (framework shovqini) ==")
    for fixture, needle in ABSENT:
        if fixture not in cache:
            cache[fixture] = run(os.path.join(DATA, fixture))[1]
        ok = needle not in cache[fixture]
        failures += not ok
        print("%-4s %-18s %s" % ("OK" if ok else "XATO", fixture, needle))

    print("\n== Chiqish kodi ==")
    code_fail, _ = run(os.path.join(DATA, "maven_fail.txt"))
    code_clean, out_clean = run(text=CLEAN)
    for label, got, want in (("yiqilish bo'lsa 1", code_fail, 1),
                             ("toza bo'lsa 0", code_clean, 0)):
        ok = got == want
        failures += not ok
        print("%-4s %-20s kutilgan=%d olingan=%d"
              % ("OK" if ok else "XATO", label, want, got))

    ok = "Yiqilgan test topilmadi" in out_clean
    failures += not ok
    print("%-4s toza chiqishda aniq xabar" % ("OK" if ok else "XATO"))

    total = len(CASES) + len(ABSENT) + 3
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
