#!/usr/bin/env python3
"""rules_for.py uchun sinovlar.

    python3 tools/test_rules_for.py

Eng muhim sinov birinchisi: SIGNALS jadvalidagi har bir bob indeksda
haqiqatan bormi. Jadval qo'lda yozilgan, boblar esa ko'chishi mumkin.
Mos kelmagan bob jim yo'qoladi va aktyor qoidani ko'rmay qoladi, keyin
reviewer uni topadi va ish ikkinchi aylanaga tushadi. Aynan shuning
oldini olish uchun bu asbob yozilgan.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import rules_for as R  # noqa: E402

BAD = os.path.join("tools", "testdata", "java", "Bad.java")
GOOD = os.path.join("tools", "testdata", "java", "Good.java")
ENTITY = os.path.join("tools", "testdata", "entities", "Order.java")
INSECURE = os.path.join("tools", "testdata", "java", "Insecure.java")
POM = os.path.join("tools", "testdata", "java", "pom.xml")


def run(*args):
    proc = subprocess.run([sys.executable, os.path.join(HERE, "rules_for.py")]
                          + list(args), capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout, proc.stderr


def main():
    failures = 0
    titles = R.chapter_titles()

    print("== Jadvaldagi boblar indeksda bormi ==")
    referenced = [ch for _, _, chapters in R.SIGNALS for ch in chapters] + R.ALWAYS
    missing = sorted({ch for ch in referenced if ch not in titles})
    ok = not missing
    failures += not ok
    print("%-4s %d ta bob tekshirildi%s"
          % ("OK" if ok else "XATO", len(set(referenced)),
             "" if ok else ", yo'q: " + ", ".join("%s %s" % c for c in missing)))

    print("\n== Belgi aniqlash ==")
    cases = [
        ("tranzaksiya", BAD, "tranzaksiya"),
        ("tashqi chaqiruv", BAD, "tashqi chaqiruv"),
        ("entity", ENTITY, "entity va ORM"),
        ("loglash", GOOD, "loglash"),
        # Xavfsizlik: avval faqat @PreAuthorize belgisi bor edi, shuning
        # uchun SQL injection, sir va fayl yuklash hech qayerga
        # yo'naltirilmasdi. Qamrov o'lchangandan keyin topilgan kamchilik.
        ("SQL injection", INSECURE, "xavfsizlik: SQL"),
        ("sir va kripto", INSECURE, "xavfsizlik: sir va kripto"),
        ("tashqi kirish", INSECURE, "xavfsizlik: tashqi kirish"),
        # Build fayli ham ko'riladi: bog'liqlik qo'shish .java da
        # ko'rinmaydi, lekin uning o'z review bobi bor.
        ("build fayli", POM, "bog'liqlik"),
    ]
    for name, path, label in cases:
        found = {l for l, _, _ in R.detect([path])}
        ok = label in found
        failures += not ok
        print("%-4s %-18s %s" % ("OK" if ok else "XATO", name, path.split("/")[-1]))

    print("\n== Chiqish tarkibi ==")
    code, out, _ = run(BAD)
    checks = [
        ("tegishli boblar bor", "# Tegishli boblar" in out),
        ("punktlar bor", "- [ ] (" in out),
        ("mashina topilmasi bor", "[yuqori] Bad.java" in out),
        ("punkt chegarasi hurmat qilindi",
         out.count("  - [ ] (") <= R.MAX_ITEMS),
        ("navbatma-navbat: bir nechta bobdan",
         len({l.split("(")[1].split(")")[0] for l in out.split("\n")
              if l.startswith("  - [ ] (")}) >= 3),
        ("chiqish kodi 0", code == 0),
    ]
    for label, ok in checks:
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", label))

    print("\n== Toza fayl ==")
    code_good, out_good, _ = run(GOOD)
    for label, ok in (("chiqish kodi 0", code_good == 0),
                      ("mashina topilmasi yo'q", "# Mashina topgani (0)" in out_good),
                      ("baribir boblar beriladi", "# Tegishli boblar" in out_good)):
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", label))

    print("\n== Xato yo'llar ==")
    for label, args, want in (("fayl berilmadi", [], 2),
                              ("ko'rilmaydigan fayl", ["README.md"], 2),
                              ("mavjud bo'lmagan fayl", ["/yoq/A.java"], 0)):
        code_e, _, _ = run(*args)
        ok = code_e == want
        failures += not ok
        print("%-4s %-22s kutilgan=%d olingan=%d"
              % ("OK" if ok else "XATO", label, want, code_e))

    total = 1 + len(cases) + len(checks) + 3 + 3
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
