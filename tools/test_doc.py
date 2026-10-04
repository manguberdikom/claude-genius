#!/usr/bin/env python3
"""doc.sh buyruqlari uchun sinovlar.

    python3 tools/test_doc.py

Qidiruv sifatini eval_find.py o'lchaydi; bu yerda buyruqlarning o'zi
tekshiriladi: to'g'ri javob, to'g'ri xato, to'g'ri chiqish kodi.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "tools", "doc.sh")


def run(*args):
    proc = subprocess.run([DOC] + list(args), capture_output=True,
                          text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


# (nom, argumentlar, kutilgan chiqish kodi, chiqishda bo'lishi shart matn)
CASES = [
    # Sonar kaliti: uchala yozilish shakli ham bir xil javob berishi kerak.
    ("rule to'liq shakl", ["rule", "java:S2095"], 0, "try-with-resources"),
    ("rule S bilan", ["rule", "S2095"], 0, "try-with-resources"),
    ("rule faqat raqam", ["rule", "2095"], 0, "try-with-resources"),
    ("rule kichik harf", ["rule", "java:s2095"], 0, "try-with-resources"),
    # Reyting: tushuntirgan bo'lim yuqorida turishi kerak, shunchaki
    # tilga olgan katalog qatori emas.
    ("rule S106 loglash", ["rule", "java:S106"], 0, "loglash"),
    ("rule S3776 murakkablik", ["rule", "java:S3776"], 0, "complexity"),
    ("rule yo'q kalit", ["rule", "S99999"], 1, ""),
    ("rule raqamsiz", ["rule", "abc"], 1, ""),

    # Tekshiruv punktlari.
    ("checklist bo'lim", ["checklist", "patterns", "17.43"], 0, "timeout"),
    ("checklist bob", ["checklist", "sonarqube", "13"], 0, "- [ ]"),
    ("checklist butun hujjat", ["checklist", "clean-code"], 0, "- [ ]"),
    ("checklist yo'q bo'lim", ["checklist", "patterns", "99.99"], 1, ""),
    ("checklist yo'q hujjat", ["checklist", "yoq"], 1, ""),

    # Avvaldan bor buyruqlar buzilmaganini tekshirish.
    ("find taxallus", ["find", "circuit breaker"], 0, "17.2"),
    ("find topilmadi", ["find", "zzqwertyuiop"], 1, ""),
    ("show bo'lim", ["show", "patterns", "17.2"], 0, "Circuit Breaker"),
    ("show katta bob to'siladi", ["show", "patterns", "25"], 1, ""),
    ("path anchor", ["path", "patterns", "17.2"], 0, "#172-"),
    ("toc", ["toc"], 0, "patterns"),
    ("outline", ["outline", "testing", "8"], 0, "8.1"),
]


def main():
    failures = 0
    for name, args, want_code, needle in CASES:
        code, out = run(*args)
        ok = code == want_code and (not needle or needle in out)
        failures += not ok
        detail = ""
        if not ok:
            detail = "  (kod=%d, kutilgan=%d%s)" % (
                code, want_code,
                ", matn topilmadi" if needle and needle not in out else "")
        print("%-4s %-28s %s%s" % ("OK" if ok else "XATO", name,
                                   " ".join(args)[:34], detail))

    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
