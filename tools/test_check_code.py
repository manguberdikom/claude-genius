#!/usr/bin/env python3
"""check_code.py uchun sinovlar.

    python3 tools/test_check_code.py

Ikki tomon ham sinaladi va ikkinchisi muhimroq. Hook har Java fayl
yozilganda ishlaydi: agar u toza kodga ogohlantirish bersa yoki izohdagi
matnni kod deb o'qisa, shovqin har yozuvda takrorlanadi va hook
o'chiriladi. Shuning uchun Good.java dan hech narsa chiqmasligi va
izoh/satr ichidagi yolg'on nusxalar sanalmasligi shart.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "check_code.py")
BAD = os.path.join(HERE, "testdata", "java", "Bad.java")
GOOD = os.path.join(HERE, "testdata", "java", "Good.java")

# (nom, daraja, satr, matn bo'lagi)
EXPECT = [
    ("bo'sh catch", "yuqori", 31, "Bo'sh catch"),
    ("keng catch", "o'rta", 23, "catch (Exception)"),
    ("System.out", "o'rta", 36, "System.out"),
    ("printStackTrace", "yuqori", 24, "printStackTrace"),
    ("BigDecimal(double)", "yuqori", 17, "aniq qiymat bermaydi"),
    ("tranzaksiyada HTTP", "yuqori", 12, "Tranzaksiya ichida tashqi chaqiruv"),
]


def run_file(path):
    proc = subprocess.run([sys.executable, TOOL, path],
                          capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


def run_hook(path, tool_name="Write"):
    payload = json.dumps({"tool_name": tool_name,
                          "tool_input": {"file_path": path}})
    proc = subprocess.run([sys.executable, TOOL], input=payload,
                          capture_output=True, text=True, cwd=ROOT)
    return proc.stdout.strip()


def main():
    for path in (BAD, GOOD):
        if not os.path.exists(path):
            print("sinov fayli yo'q: %s" % path)
            return 1

    failures = 0
    code_bad, out_bad = run_file(BAD)

    print("== Topilishi kerak ==")
    for name, level, line, needle in EXPECT:
        marker = "[%s] Bad.java:%d" % (level, line)
        ok = marker in out_bad and needle in out_bad
        failures += not ok
        print("%-4s %-22s %s" % ("OK" if ok else "XATO", name, marker))

    print("\n== Qo'llanmaga ulanish ==")
    refs = [l for l in out_bad.split("\n") if "doc.sh show" in l]
    ok = len(refs) >= 5
    failures += not ok
    print("%-4s %d ta topilma bo'lim raqamiga ulandi" % ("OK" if ok else "XATO",
                                                         len(refs)))

    print("\n== Yolg'on ishga tushish bo'lmasligi kerak ==")
    # Bad.java da izoh ichida System.out.println va catch (Exception e) {},
    # satr literalida esa printStackTrace() bor. Ular sanalmasligi kerak:
    # har biri aynan bir marta topilishi lozim.
    for name, needle, want in (("izohdagi System.out", "System.out", 1),
                               ("satrdagi printStackTrace", "printStackTrace", 1),
                               ("izohdagi bo'sh catch", "Bo'sh catch", 1)):
        got = out_bad.count(needle)
        ok = got == want
        failures += not ok
        print("%-4s %-26s %d marta (kutilgan %d)"
              % ("OK" if ok else "XATO", name, got, want))

    print("\n== Toza fayl ==")
    code_good, out_good = run_file(GOOD)
    for label, ok in (("chiqish kodi 0", code_good == 0),
                      ("topilma yo'q", "topilmadi" in out_good)):
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", label))

    print("\n== Hook javobi ==")
    raw_bad = run_hook(BAD)
    raw_good = run_hook(GOOD)
    checks = [
        ("yuqori daraja block qaytaradi",
         bool(raw_bad) and json.loads(raw_bad).get("decision") == "block"),
        ("block sababida bo'lim raqami bor",
         bool(raw_bad) and "doc.sh show" in json.loads(raw_bad).get("reason", "")),
        ("toza faylda jim", raw_good == ""),
        ("java bo'lmagan faylda jim", run_hook(os.path.join(ROOT, "README.md")) == ""),
        ("mavjud bo'lmagan faylda jim", run_hook("/yoq/Fayl.java") == ""),
    ]
    for label, ok in checks:
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", label))

    total = len(EXPECT) + 1 + 3 + 2 + len(checks)
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
