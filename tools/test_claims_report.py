#!/usr/bin/env python3
"""claims_report.py uchun sinovlar.

    python3 tools/test_claims_report.py

Asbob haqiqiy korpusda yuradi va u yerda yuzlab topilma bor, ya'ni
chiqish borligi hech narsani isbotlamaydi. Bu yerda har qoida alohida
qisqa matnda sinaladi: manbali raqam sanalmaydi, manbasizi sanaladi.
"""

import io
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import claims_report as C  # noqa: E402


def scan_text(text):
    """Matnni vaqtinchalik faylga yozib skanerlaydi."""
    tmp = tempfile.mkdtemp(prefix="claims_")
    try:
        path = os.path.join(tmp, "bob.md")
        io.open(path, "w", encoding="utf-8").write(text)
        return C.scan(path)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def counts(text):
    """(jami, manbasiz, taxmin)."""
    hits = scan_text(text)
    return (len(hits),
            len([h for h in hits if not h[3] and not h[4]]),
            len([h for h in hits if h[4]]))


CASES = [
    ("manbasiz foiz sanaladi", "GC pauzasi 5 foiz CPU oladi.", (1, 1, 0)),
    ("manbasiz ms sanaladi", "So'rov 200 ms davom etadi.", (1, 1, 0)),
    ("manbasiz barobar sanaladi", "Keyset 3 barobar tez.", (1, 1, 0)),
    ("manbasiz MB sanaladi", "Korpus 6 MB.", (1, 1, 0)),
    ("manbasiz token sanaladi", "Bob 50k token turadi.", (1, 1, 0)),
    ("shu qatordagi havola manba",
     "GC pauzasi 5 foiz CPU oladi (https://openjdk.org/jeps/1).", (1, 0, 0)),
    ("markdown havola ham manba",
     "GC pauzasi 5 foiz ([manba](https://x.org/a)).", (1, 0, 0)),
    ("oldingi qatordagi havola ham manba",
     "Manba: https://postgresql.org/docs/current/x.html\n\nwork_mem 25 foiz.",
     (1, 0, 0)),
    ("uzoqdagi havola manba emas",
     "https://x.org/a\n\n\n\n\nGC pauzasi 5 foiz.", (1, 1, 0)),
    ("o'lchanmagan taxmin belgisi",
     "Bu 5 foiz atrofida (o'lchanmagan taxmin).", (1, 0, 1)),
    ("taxminan so'zi taxmin deb sanaladi",
     "Taxminan 200 ms davom etadi.", (1, 0, 1)),
    ("tilda bilan yozilgan raqam taxmin",
     "Bob ~200 KB.", (1, 0, 1)),
    ("kod bloki ichidagi raqam sanalmaydi",
     "```java\nint x = 5; // 200 ms\n```\n", (0, 0, 0)),
    ("sarlavhadagi raqam sanalmaydi", "## 27.3 work_mem va 25 foiz", (0, 0, 0)),
    ("jadval ajratgichi sanalmaydi", "| a | b |\n| --- | --- |\n", (0, 0, 0)),
    ("Manbalar bo'limidagi raqam sanalmaydi",
     "## Manbalar\n\n- https://x.org/a, 5 foiz haqida\n", (0, 0, 0)),
    ("Manbalar dan keyingi bo'lim yana sanaladi",
     "## Manbalar\n\n- https://x.org/a\n\n## 1.2 Yana\n\nBu 5 foiz.", (1, 1, 0)),
    ("bo'lim raqami da'vo emas", "Bo'lim 25.31 da aytilgan.", (0, 0, 0)),
]


def main():
    failures = 0
    for name, text, want in CASES:
        got = counts(text)
        ok = got == want
        failures += not ok
        print("%-4s %-44s %s" % ("OK" if ok else "XATO", name,
                                 "" if ok else "%s != %s" % (got, want)))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
