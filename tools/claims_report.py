#!/usr/bin/env python3
"""Manbasiz raqamli da'volarni hujjat va bob bo'yicha sanaydi.

    python3 tools/claims_report.py              # hamma hujjat
    python3 tools/claims_report.py architect    # bitta hujjat
    python3 tools/claims_report.py --bob architect 27
    python3 tools/claims_report.py --batafsil   # har da'voning qatori
    python3 tools/claims_report.py --empirik    # faqat empirik taqqoslash

Nega kerak: "2-5 foiz CPU", "3 barobar tez", "~200 ms" kabi raqamlar
hujjatga ishonch beradi, lekin manbasi bo'lmasa ularni tekshirib
bo'lmaydi. Bu asbob ularni TOPADI, hukm chiqarmaydi: hisobot
CI ni yiqitmaydi. Qaror odamda, chunki ba'zi raqam o'lchangan,
ba'zisi esa taxmin va shunday belgilanishi kerak.

Raqam MANBALI hisoblanadi, agar:
  - shu qatorda yoki undan oldingi uch qatorda havola bo'lsa
    (`http`, `[...](...)`, `docs.spring.io` kabi), yoki
  - shu qatorda `o'lchanmagan taxmin` belgisi bo'lsa, yoki
  - bob oxiridagi `## Manbalar` bo'limida bo'lsa, yoki
  - kod bloki, jadval ajratgichi yoki bo'lim raqami bo'lsa.

Empirik taqqoslash (KR-Q13) alohida sinf: "2-4 barobar tez", "15 foiz
yo'qotish", "G1 ga nisbatan 5 foiz". Bunday raqamni faqat o'lchov beradi,
misol yoki sozlama tanlovi emas, shuning uchun agent to'lqini aynan shu
sinfni manba yoki `o'lchanmagan taxmin` bilan yopadi. Qolgan raqamlarning
ko'pi misol arifmetikasi (budjet taqsimoti, timeout tanlovi) va ularni
qatorma-qator manbalash shart emas. Empirik moslik ichidagi raqam
ikkinchi marta (foiz yoki barobar sifatida) sanalmaydi.

Qoida CONTRIBUTING.md dagi "Raqamlar" bo'limida.
"""

import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MANIFEST = os.path.join(ROOT, "docs", "manifest.json")

NUM = r"\d+(?:[.,]\d+)?(?:\s*-\s*\d+(?:[.,]\d+)?)?"
# Empirik taqqoslash: ikki narsa o'lchov bilan solishtirilgan. Birinchi
# tekshiriladi; uning ichidagi raqam boshqa sinfga qayta tushmaydi.
EMPIRIC_RE = re.compile(
    NUM + r"\s*(?:barobar|marta|x)\s+(?:tez|sekin|ko'p|kam|katta|kichik|yaxshi"
    r"|yomon|arzon|qimmat)\w*"
    # "10 foizdan kam" chegara, taqqoslash emas: `dan` bu yerga tushmaydi.
    r"|" + NUM + r"\s*(?:foiz|%)(?:ga|gacha)?\s+(?:yo'qotish|yutuq|tez|sekin"
    r"|tejaydi|tejash|oshadi|oshiradi|kamayadi|kamaytiradi|pasayadi|tushadi"
    r"|yaxshi|yomon|ko'proq|kamroq)\w*"
    r"|\w[\w'-]*\s+ga\s+nisbatan\b[^.\n]{0,60}?" + NUM + r"\s*(?:foiz|%|barobar|marta)",
    re.I)
# Tekshiriladigan raqamli da'volar. Bo'lim raqami (`25.31`) va ro'yxat
# raqami emas: ular tuzilma.
CLAIM_RES = (
    ("foiz", re.compile(r"\d+(?:[.,]\d+)?\s*(?:foiz|%)")),
    ("vaqt", re.compile(r"\d+(?:[.,]\d+)?\s*(?:ms|mks|sekund|sek|daqiqa|soat)\b")),
    ("hajm", re.compile(r"\d+(?:[.,]\d+)?\s*(?:KB|MB|GB|TB|bayt)\b")),
    ("barobar", re.compile(r"\d+(?:[.,]\d+)?\s*(?:barobar|marta tez|x tez)")),
    ("token", re.compile(r"\d+(?:[.,]\d+)?\s*k?\s*token\b")),
)
# Manba belgisi.
SOURCE_RE = re.compile(r"https?://|\]\([^)]+\)|docs\.spring\.io|postgresql\.org"
                       r"|openjdk\.org|docs\.oracle\.com|sonarsource")
# Ataylab belgilangan taxmin.
GUESS_RE = re.compile(r"o'lchanmagan taxmin", re.I)
# "taxminan", "~", "qariyb": aniqlik da'vo qilmaydigan raqam.
HEDGE_RE = re.compile(r"taxminan|qariyb|~\s*\d|deyarli", re.I)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
TABLE_SEP_RE = re.compile(r"^\s*\|[\s|:-]+\|\s*$")
SOURCES_HEADING = re.compile(r"^##\s+Manbalar\s*$")


def chapters(only=None):
    with io.open(MANIFEST, encoding="utf-8") as handle:
        man = json.load(handle)
    out = []
    for key in sorted(man):
        if only and key != only:
            continue
        for c in man[key]["chapters"]:
            out.append((key, str(c["num"] or ""),
                        os.path.join(ROOT, "docs", key, c["file"])))
    return out


def scan(path):
    """[(qator_raqami, tur, matn, manbali, taxmin)]. Tur `empirik` ham bo'ladi."""
    found = []
    fence = in_sources = False
    lines = io.open(path, encoding="utf-8").read().split("\n")
    for number, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            fence = not fence
            continue
        if fence or TABLE_SEP_RE.match(line):
            continue
        if line.startswith("## "):
            in_sources = bool(SOURCES_HEADING.match(line))
        if in_sources or line.startswith("#"):
            continue
        near = "\n".join(lines[max(0, number - 4):number])
        sourced = bool(SOURCE_RE.search(near))
        guess = bool(GUESS_RE.search(line) or HEDGE_RE.search(line))
        taken = []
        for match in EMPIRIC_RE.finditer(line):
            taken.append(match.span())
            found.append((number, "empirik", match.group(0).strip(), sourced, guess))
        for kind, regex in CLAIM_RES:
            for match in regex.finditer(line):
                if any(a <= match.start() and match.end() <= b for a, b in taken):
                    continue
                found.append((number, kind, match.group(0).strip(), sourced, guess))
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("hujjat", nargs="?", default=None)
    parser.add_argument("--bob", nargs=2, metavar=("HUJJAT", "RAQAM"))
    parser.add_argument("--batafsil", action="store_true")
    parser.add_argument("--empirik", action="store_true",
                        help="faqat empirik taqqoslash sinfi (barobar tez, "
                             "foiz yo'qotish, X ga nisbatan)")
    args = parser.parse_args(argv)

    only_doc, only_num = (args.bob if args.bob else (args.hujjat, None))
    rows = []
    for doc, num, path in chapters(only_doc):
        if only_num is not None and num != str(only_num):
            continue
        if not os.path.exists(path):
            continue
        hits = scan(path)
        if args.empirik:
            hits = [h for h in hits if h[1] == "empirik"]
        manbasiz = [h for h in hits if not h[3] and not h[4]]
        taxmin = [h for h in hits if h[4]]
        empirik = [h for h in manbasiz if h[1] == "empirik"]
        rows.append((doc, num, len(hits), len(manbasiz), len(taxmin),
                     len(empirik), os.path.relpath(path, ROOT), manbasiz))

    print("%-12s %-5s %7s %9s %8s %8s"
          % ("hujjat", "bob", "da'vo", "manbasiz", "taxmin", "empirik"))
    total = [0, 0, 0, 0]
    for doc, num, all_n, bad_n, guess_n, emp_n, rel, manbasiz in rows:
        total = [total[0] + all_n, total[1] + bad_n, total[2] + guess_n,
                 total[3] + emp_n]
        if all_n:
            print("%-12s %-5s %7d %9d %8d %8d"
                  % (doc, num, all_n, bad_n, guess_n, emp_n))
        if args.batafsil and manbasiz:
            for number, kind, text, _, _ in manbasiz:
                print("    %s:%d  %-8s %s" % (rel, number, kind, text))
    print("\n%-12s %-5s %7d %9d %8d %8d"
          % ("JAMI", "", total[0], total[1], total[2], total[3]))
    print("\nempirik: manbasiz empirik taqqoslash (barobar tez, foiz yo'qotish, "
          "X ga nisbatan).\nAgent to'lqini avval shularni manba yoki "
          "\"o'lchanmagan taxmin\" bilan yopadi.")
    print("\nBu hisobot: CI ni yiqitmaydi. Manbasiz raqam o'chiriladi, "
          "manba bilan beriladi\nyoki \"o'lchanmagan taxmin\" deb belgilanadi "
          "(CONTRIBUTING.md, Raqamlar).")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
