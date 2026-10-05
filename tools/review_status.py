#!/usr/bin/env python3
"""Bob fayllariga `docs/review.tsv` dagi holat qatorini yozadi.

    python3 tools/review_status.py            # quruq: nima o'zgaradi
    python3 tools/review_status.py --yoz      # yozadi

Nega skript: holat 224 bobda turadi va `review.tsv` o'zgarganda
hammasi birga yangilanishi kerak. Qo'lda yozilsa ikkisi darhol
ajralib ketadi, `check_docs.py` esa aynan shu mosliqni talab qiladi.

Qator joyi qat'iy: breadcrumb (3-qator) ostida, H1 dan oldin.
Shuning uchun bob boshi shunday bo'ladi:

    1  <!-- doc: ... -->
    2
    3  [Barcha hujjatlar](../../README.md) / [Hujjat](README.md)
    4
    5  > Holat: ...
    6
    7  # 1. Sarlavha

Matn qisqa: u har `doc.sh show` chiqishiga emas, bob faylining boshiga
tushadi, lekin `build_single.py` yig'masida 224 marta takrorlanadi.
"""

import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REVIEW = os.path.join(ROOT, "docs", "review.tsv")
MANIFEST = os.path.join(ROOT, "docs", "manifest.json")

MARKER = "> Holat:"
HOLATLAR = ("ai-draft", "tekshirilmoqda", "tekshirilgan")


def read_review(path=REVIEW):
    """{(hujjat, bob): {maydon: qiymat}}. Izoh qatorlari tashlanadi."""
    rows, header = {}, None
    if not os.path.exists(path):
        return rows
    with io.open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if header is None:
                header = parts
                continue
            row = dict(zip(header, parts))
            rows[(row.get("hujjat", ""), row.get("bob", ""))] = row
    return rows


def status_line(row):
    """Bob boshida turadigan bitta qator."""
    holat = (row or {}).get("holat", "ai-draft")
    if holat == "tekshirilgan":
        sana = row.get("sana", "")
        return ("%s tekshirilgan%s. Manbalar bob oxirida."
                % (MARKER, " (%s)" % sana if sana else ""))
    if holat == "tekshirilmoqda":
        return "%s tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda." % MARKER
    return "%s AI yozgan, inson tekshirmagan." % MARKER


def chapters():
    """[(hujjat, bob_raqami, fayl_yo'li)] manifest bo'yicha."""
    with io.open(MANIFEST, encoding="utf-8") as handle:
        man = json.load(handle)
    out = []
    for key in sorted(man):
        for c in man[key]["chapters"]:
            # Raqamsiz bob bor (patterns dagi alifbo indeksi): kalit
            # bo'sh satr bo'ladi, check_docs dagi qoida bilan bir xil.
            out.append((key, str(c["num"] or ""),
                        os.path.join(ROOT, "docs", key, c["file"])))
    return out


def apply_to(text, line):
    """Holat qatorini breadcrumb ostiga qo'yadi. (yangi matn, o'zgardimi)."""
    lines = text.split("\n")
    if len(lines) < 5:
        return text, False
    # Bor bo'lsa almashtiriladi, yo'q bo'lsa 5-qator bo'lib qo'shiladi.
    if lines[4].startswith(MARKER):
        if lines[4] == line:
            return text, False
        lines[4] = line
        return "\n".join(lines), True
    lines[4:4] = [line, ""]
    return "\n".join(lines), True


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--yoz", action="store_true")
    args = parser.parse_args(argv)

    review = read_review()
    changed = missing = 0
    for doc, num, path in chapters():
        if not os.path.exists(path):
            print("bob fayli yo'q: %s" % os.path.relpath(path, ROOT))
            missing += 1
            continue
        row = review.get((doc, num))
        if row is None:
            print("review.tsv da yo'q: %s %s" % (doc, num))
            missing += 1
            continue
        if row.get("holat") not in HOLATLAR:
            print("noma'lum holat: %s %s -> %s" % (doc, num, row.get("holat")))
            missing += 1
            continue
        text = io.open(path, encoding="utf-8").read()
        new, did = apply_to(text, status_line(row))
        if did:
            changed += 1
            if args.yoz:
                io.open(path, "w", encoding="utf-8").write(new)
    if missing:
        print("%d muammo: holat qatori to'liq yozilmadi" % missing)
        return 1
    if args.yoz:
        print("%d bobda holat qatori yangilandi" % changed)
    else:
        print("%d bobda holat qatori o'zgaradi (--yoz bilan yoziladi)" % changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
