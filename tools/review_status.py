#!/usr/bin/env python3
"""Bob fayllariga `docs/review.tsv` dagi holat qatorini yozadi.

    python3 tools/review_status.py            # quruq: nima o'zgaradi
    python3 tools/review_status.py --yoz      # yozadi (boblar va README lar)
    python3 tools/review_status.py --imzo 68 --yoz   # navbat boshidagi 68 bob: tekshirilgan

`--imzo N` ni faqat ODAM yurgizadi va natijani o'z nomidan commit qiladi:
`check_docs` `tekshirilgan` qatorini Claude commit qilganini xato deydi
(CONTRIBUTING.md, Tekshiruv tartibi, 4-qoida). Bob `docs/review-queue.tsv`
tartibida olinadi, ya'ni agentlar eng ko'p tayanadiganlari.

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

Kirish sahifalari ham bitta holat qatorini oladi (TZ-T8): ildiz
`README.md` da hujjatlar jadvali ostida, har `docs/<hujjat>/README.md`
da `**Versiya bazasi:**` qatoridan keyin. Mundarijadan to'g'ridan
bo'limga kirgan o'quvchi bob boshini ko'rmaydi, shuning uchun holat
kirish sahifasida ham aytiladi. Qator `- N bo'lim` shaklida emas va
"N bobdan" deb yoziladi: `check_docs` dagi mundarija va son regexlari
uni ushlamaydi.
"""

import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REVIEW = os.path.join(ROOT, "docs", "review.tsv")
QUEUE = os.path.join(ROOT, "docs", "review-queue.tsv")
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


def tally(review, keys):
    """(jami, tekshirilgan, tekshirilmoqda) berilgan (hujjat, bob) lar uchun."""
    states = [(review.get(k) or {}).get("holat", "ai-draft") for k in keys]
    return (len(states), states.count("tekshirilgan"),
            states.count("tekshirilmoqda"))


def readme_line(total, done, doing, tsv_link):
    """Kirish sahifasidagi bitta holat qatori."""
    rest = total - done - doing
    return ("%s %d bobdan %d tasi odam tekshirgan, %d tasi tekshirilmoqda, "
            "qolgan %d tasi AI yozgan va inson tekshirmagan. Har bob holati: "
            "[docs/review.tsv](%s)." % (MARKER, total, done, doing, rest, tsv_link))


def readme_targets(review, root=None):
    """[(fayl_yo'li, kutilgan_qator, langar_regex)]: ildiz README va hujjat README lari.

    Langar - qator yo'q bo'lganda u qaysi qatordan keyin qo'yilishi.
    """
    root = root or ROOT
    with io.open(os.path.join(root, "docs", "manifest.json"), encoding="utf-8") as handle:
        man = json.load(handle)
    out, every = [], []
    for key in sorted(man):
        keys = [(key, str(c["num"] or "")) for c in man[key]["chapters"]]
        every += keys
        out.append((os.path.join(root, "docs", key, "README.md"),
                    readme_line(*tally(review, keys), tsv_link="../review.tsv"),
                    r"^\*\*Versiya bazasi:\*\*"))
    out.insert(0, (os.path.join(root, "README.md"),
                   readme_line(*tally(review, every), tsv_link="docs/review.tsv"),
                   r"^\| \[.*\]\(docs/[a-z-]+/README\.md\) \|"))
    return out


def apply_readme(text, line, anchor):
    """Holat qatorini README ga qo'yadi. (yangi matn, o'zgardimi).

    Bor bo'lsa almashtiriladi. Yo'q bo'lsa langarga mos OXIRGI qatordan
    keyin bo'sh qator bilan qo'shiladi (jadval bo'lsa uning ostiga).
    Langar topilmasa matn o'zgarmaydi: check_docs buni aytadi.
    """
    lines = text.split("\n")
    for i, cur in enumerate(lines):
        if cur.startswith(MARKER):
            if cur == line:
                return text, False
            lines[i] = line
            return "\n".join(lines), True
    hits = [i for i, cur in enumerate(lines) if re.match(anchor, cur)]
    if not hits:
        return text, False
    at = hits[-1] + 1
    lines[at:at] = ["", line]
    return "\n".join(lines), True


def queue_head(count, path=QUEUE):
    """Navbatning birinchi `count` bobi: [(hujjat, bob)]."""
    out = []
    for row in read_review(path).values():
        if row.get("tartib", "").isdigit() and int(row["tartib"]) <= count:
            out.append((int(row["tartib"]), (row["hujjat"], row["bob"])))
    return [key for _, key in sorted(out)]


def sign(keys, day, path=REVIEW):
    """`keys` qatorlarini `tekshirilgan`, `odam` qiladi; boshqa qatorga tegmaydi."""
    lines = io.open(path, encoding="utf-8").read().split("\n")
    header = next(l for l in lines if l and not l.startswith("#")).split("\t")
    col = {name: i for i, name in enumerate(header)}
    for i, line in enumerate(lines):
        parts = line.split("\t")
        if len(parts) == len(header) and (parts[col["hujjat"]], parts[col["bob"]]) in keys:
            parts[col["holat"]], parts[col["sana"]] = "tekshirilgan", day
            parts[col["tekshiruvchi"]] = "odam"
            lines[i] = "\t".join(parts)
    with io.open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--yoz", action="store_true")
    parser.add_argument("--imzo", type=int, metavar="N",
                        help="navbat boshidagi N bob: tekshirilgan (faqat odam)")
    parser.add_argument("--sana", default=None, help="YYYY-MM-DD, sukut bugun")
    args = parser.parse_args(argv)

    if args.imzo:
        import datetime
        keys = queue_head(args.imzo)
        print("tekshirilgan%s: %d bob (%s)" % ("" if args.yoz else " (quruq, --yoz bilan yoziladi)",
                                               len(keys), ", ".join("%s %s" % k for k in keys)))
        if not args.yoz:
            return 0
        sign(set(keys), args.sana or datetime.date.today().isoformat())

    review = read_review()
    changed = missing = 0
    for path, line, anchor in readme_targets(review):
        if not os.path.exists(path):
            continue
        text = io.open(path, encoding="utf-8").read()
        new, did = apply_readme(text, line, anchor)
        if not did and MARKER not in text:
            print("holat qatori uchun joy topilmadi: %s" % os.path.relpath(path, ROOT))
            missing += 1
        if did:
            changed += 1
            if args.yoz:
                io.open(path, "w", encoding="utf-8").write(new)
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
        print("%d faylda holat qatori yangilandi" % changed)
    else:
        print("%d faylda holat qatori o'zgaradi (--yoz bilan yoziladi)" % changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
