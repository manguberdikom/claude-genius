#!/usr/bin/env python3
"""Bob tekshiruvi navbatini yasaydi: agentlar eng ko'p tayangani oldinda.

    python3 tools/review_queue.py              # quruq: navbatni chiqaradi
    python3 tools/review_queue.py --yoz        # docs/review-queue.tsv ga yozadi

Nega navbat kerak: 224 bob bor, hammasini birdan tekshirib bo'lmaydi.
Noto'g'ri bob qanchalik qimmat ekanini uning NIMAGA ishlatilishi
belgilaydi. Agent `rules_for` orqali ko'rsatgan bob xato bo'lsa, xato
yozilayotgan kodga darhol o'tadi; hech kim ochmagan bob esa kutishi
mumkin.

Vazn uchta dalildan yig'iladi, hammasi mashina o'qiydigan manbadan:

  rules_for   - tools/rules_for.py dagi SIGNALS jadvalida bob necha
                marta ko'rsatilgan. Eng og'ir dalil (vazni 5), chunki
                bu bob Java yozishdan OLDIN majburiy chiqadi.
  sonar       - index/rules.tsv da bobga nechta Sonar kaliti bog'langan
                (vazni 2): kalit bo'yicha so'rov to'g'ridan shu bobga
                boradi.
  eval        - tools/eval_skill.py va tools/eval_find.py kutilgan
                qiymatlarida bob necha marta uchraydi (vazni 3): bu
                bob marshrut sinovida qoplangan, ya'ni u yo'lning
                asosiy qismi.
  bo'lim      - bobdagi bo'lim soni (vazni 1 ta 10 bo'limga): katta
                bobda xato ko'p bo'lishi ehtimoli yuqori.

Holat `docs/review.tsv` dan olinadi: `tekshirilgan` boblar navbat
oxiriga tushadi, chunki ularni qayta tekshirish kutib turishi mumkin.
"""

import argparse
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import review_status  # noqa: E402

QUEUE = os.path.join(ROOT, "docs", "review-queue.tsv")
MANIFEST = os.path.join(ROOT, "docs", "manifest.json")
RULES_TSV = os.path.join(ROOT, "index", "rules.tsv")

# Vaznlar. Har dalil AVVAL o'z maksimumiga bo'linadi (0..1), keyin
# ko'paytiriladi: aks holda Sonar kaliti soni (eng kattasi 61) qolgan
# hamma dalilni bosib ketadi va navbat faqat sonarqube bo'lib chiqadi.
W_RULES_FOR, W_EVAL, W_SONAR, W_SECTIONS = 5.0, 3.0, 2.0, 1.0
# `("hujjat", "raqam")` juftligi: rules_for SIGNALS jadvalidagi shakl.
PAIR_RE = re.compile(r"\(\"([a-z-]+)\",\s*\"(\d+)\"\)")
# eval fayllaridagi `"hujjat", {"12.3"}` va `patterns 7.10` shakllari.
EVAL_REFS = (re.compile(r'"([a-z-]+)",\s*\{([^}]*)\}'),
             re.compile(r'"([a-z-]+)\s+(\d+(?:\.\d+)?)"'))


def rules_for_hits():
    """{(hujjat, bob): necha marta} rules_for.py SIGNALS jadvalidan."""
    hits = {}
    text = io.open(os.path.join(HERE, "rules_for.py"), encoding="utf-8").read()
    start = text.find("SIGNALS = [")
    block = text[start:text.find("\n]", start)] if start >= 0 else ""
    for doc, num in PAIR_RE.findall(block):
        hits[(doc, num)] = hits.get((doc, num), 0) + 1
    return hits


def sonar_hits():
    """{(hujjat, bob): bog'langan Sonar kaliti soni} index/rules.tsv dan."""
    hits = {}
    if not os.path.exists(RULES_TSV):
        return hits
    with io.open(RULES_TSV, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3:
                hits[(parts[1], parts[2])] = hits.get((parts[1], parts[2]), 0) + 1
    return hits


def eval_hits():
    """{(hujjat, bob): necha marta} eval fayllarining kutilgan qiymatlaridan."""
    hits = {}
    for name in ("eval_skill.py", "eval_find.py"):
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        text = io.open(path, encoding="utf-8").read()
        for doc, blob in EVAL_REFS[0].findall(text):
            for ref in re.findall(r"\d+(?:\.\d+)?", blob):
                key = (doc, ref.split(".")[0])
                hits[key] = hits.get(key, 0) + 1
        for doc, ref in EVAL_REFS[1].findall(text):
            key = (doc, ref.split(".")[0])
            hits[key] = hits.get(key, 0) + 1
    return hits


def build():
    """[(vazn, hujjat, bob, holat, rules_for, eval, sonar, bo'lim, sarlavha)]."""
    with io.open(MANIFEST, encoding="utf-8") as handle:
        man = json.load(handle)
    rf, sn, ev = rules_for_hits(), sonar_hits(), eval_hits()
    review = review_status.read_review()
    secs = {(doc, str(c["num"] or "")): (c.get("sections") or 0)
            for doc in man for c in man[doc]["chapters"]}
    # Normallash: har dalil o'z maksimumiga bo'linadi, aks holda Sonar
    # kaliti soni (eng kattasi 61) qolgan dalillarni bosib ketadi.
    top = {"rf": max(list(rf.values()) or [1]),
           "ev": max(list(ev.values()) or [1]),
           "sn": max(list(sn.values()) or [1]),
           "sc": max(list(secs.values()) or [1])}
    rows = []
    for doc in sorted(man):
        for c in man[doc]["chapters"]:
            num = str(c["num"] or "")
            key = (doc, num)
            sections = secs[key]
            holat = (review.get(key) or {}).get("holat", "ai-draft")
            weight = (W_RULES_FOR * rf.get(key, 0) / top["rf"]
                      + W_EVAL * ev.get(key, 0) / top["ev"]
                      + W_SONAR * sn.get(key, 0) / top["sn"]
                      + W_SECTIONS * sections / top["sc"])
            if holat == "tekshirilgan":
                weight = -1.0          # navbat oxiriga
            rows.append((round(weight, 3), doc, num, holat, rf.get(key, 0),
                         ev.get(key, 0), sn.get(key, 0), sections, c["title"]))
    rows.sort(key=lambda r: (-r[0], r[1], int(r[2]) if r[2] else 999))
    return rows


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--yoz", action="store_true")
    parser.add_argument("-n", type=int, default=20,
                        help="quruq yurishda ko'rsatiladigan qator soni")
    args = parser.parse_args(argv)

    rows = build()
    if args.yoz:
        head = ("# Bob tekshiruvi navbati. Vazn: agentlar bobga qancha\n"
                "# tayanadi. Yasaladi: python3 tools/review_queue.py --yoz\n"
                "# Dalillar va vaznlari: rules_for %g, eval %g, sonar %g,\n"
                "# bo'lim soni %g. Har dalil avval o'z maksimumiga\n"
                "# bo'linadi (0..1), shuning uchun kattaroq shkala\n"
                "# qolganini bosib ketmaydi. `tekshirilgan` bob navbat\n"
                "# oxiriga tushadi (vazn -1).\n"
                % (W_RULES_FOR, W_EVAL, W_SONAR, W_SECTIONS))
        lines = [head + "\t".join(("tartib", "vazn", "hujjat", "bob", "holat",
                                   "rules_for", "eval", "sonar", "bolim",
                                   "sarlavha"))]
        for i, r in enumerate(rows, 1):
            lines.append("\t".join([str(i), str(r[0]), r[1], r[2], r[3],
                                    str(r[4]), str(r[5]), str(r[6]),
                                    str(r[7]), r[8].replace("\t", " ")]))
        io.open(QUEUE, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("docs/review-queue.tsv: %d bob" % len(rows))
        return 0

    print("%-4s %-6s %-12s %-5s %-15s %4s %4s %5s %6s"
          % ("#", "vazn", "hujjat", "bob", "holat", "r_f", "eval", "sonar", "bo'lim"))
    for i, r in enumerate(rows[:args.n], 1):
        print("%-4d %-6s %-12s %-5s %-15s %4d %4d %5d %6d"
              % (i, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]))
    print("\njami %d bob. --yoz bilan docs/review-queue.tsv ga yoziladi." % len(rows))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
