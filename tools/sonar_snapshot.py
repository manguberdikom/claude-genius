#!/usr/bin/env python3
"""sonar-java rule metadata snapshotini yangilaydi.

    python3 tools/sonar_snapshot.py            # korpusdagi kalitlar bo'yicha
    python3 tools/sonar_snapshot.py S109 S2230 # faqat shu kalitlar qo'shiladi
    python3 tools/sonar_snapshot.py --tekshir   # yozmaydi, farqni aytadi

Nega snapshot: korpusda 100 ga yaqin `java:S` kaliti bor va ularning
turi hamda darajasi jadvallarda yozilgan. Metadata tarmoqda turadi,
CI esa har yurishda tarmoqqa chiqmasligi kerak. Shuning uchun
metadata bir marta olinadi, `tools/sonar_rules.tsv` ga yoziladi va
`check_docs.py` shu faylga solishtiradi.

Metadata manbasi (SonarSource/sonar-java, master):

    sonar-java-plugin/src/main/resources/org/sonar/l10n/java/rules/java/<kalit>.json

Ba'zi qoidalar ochiq metadata da YO'Q: symbolic execution va shunga
o'xshash yopiq qoidalar (S2259, S2095, S1148 va boshqalar). Ular
`tekshirilmadi` deb belgilanadi va check_docs ularni ogohlantirish
bilan o'tkazadi, xato bermaydi.
"""

import argparse
import datetime
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAPSHOT = os.path.join(HERE, "sonar_rules.tsv")
URL = ("https://raw.githubusercontent.com/SonarSource/sonar-java/master/"
       "sonar-java-plugin/src/main/resources/org/sonar/l10n/java/rules/java/"
       "%s.json")
RULE_RE = re.compile(r"\bjava:(S\d+)\b")
# Qoida sarlavhasi (`title`) olinmaydi: u sonar-java ning SSALv1 ostidagi
# matni, bu fayl esa MIT ostida. Uni hech bir asbob o'qimaydi, check_docs
# faqat tur va darajaga qaraydi.
HEADER = ("kalit", "tur", "daraja", "scope")
MISSING = "tekshirilmadi"
SCAN_DIRS = ("docs", ".claude")
SCAN_EXT = (".md", ".tsv")


def corpus_keys():
    """Korpusda uchraydigan `java:S` kalitlari."""
    keys = set()
    for base in SCAN_DIRS:
        for dirpath, dirs, files in os.walk(os.path.join(ROOT, base)):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for name in files:
                if not name.endswith(SCAN_EXT):
                    continue
                try:
                    text = io.open(os.path.join(dirpath, name),
                                   encoding="utf-8").read()
                except (OSError, UnicodeDecodeError):
                    continue
                keys.update(RULE_RE.findall(text))
    return keys


def read_snapshot(path=SNAPSHOT):
    """{kalit: {tur, daraja, scope}} va sana.

    Ustunlar sarlavha qatori bo'yicha olinadi, shuning uchun eski
    5 ustunli fayl ham o'qiladi: ortiqcha ustun e'tiborsiz qoladi."""
    rows, date, header = {}, "", None
    if not os.path.exists(path):
        return rows, date
    with io.open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith("# sana:"):
                date = line.split(":", 1)[1].strip()
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if header is None:
                header = parts
                continue
            row = dict(zip(header, parts))
            rows[row.get("kalit", "")] = row
    return rows, date


def fetch(key):
    """Bitta kalitning metadata si yoki None (ochiq metadata da yo'q)."""
    try:
        proc = subprocess.run(["curl", "-sS", "-f", "--max-time", "30",
                               URL % key], capture_output=True, timeout=45)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout.decode("utf-8"))
    except ValueError:
        return None


def write_snapshot(rows, path=SNAPSHOT):
    today = datetime.date.today().isoformat()
    lines = [
        "# sonar-java rule metadata snapshoti.",
        "# sana: %s" % today,
        "# manba: %s" % (URL % "<kalit>"),
        "#",
        "# tur    - CODE_SMELL | BUG | VULNERABILITY | SECURITY_HOTSPOT",
        "# daraja - defaultSeverity (legacy severity)",
        "# scope  - Main | Tests | All",
        "#",
        "# `%s` = qoida ochiq metadata da yo'q (symbolic execution va" % MISSING,
        "# shunga o'xshash yopiq qoidalar). check_docs ularni ogohlantirish",
        "# bilan o'tkazadi. Yangilash: python3 tools/sonar_snapshot.py",
        "\t".join(HEADER),
    ]
    for key in sorted(rows, key=lambda k: int(k[1:])):
        row = rows[key]
        lines.append("\t".join([key, row.get("tur", MISSING),
                                row.get("daraja", MISSING),
                                row.get("scope", MISSING)]))
    io.open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return today


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("kalitlar", nargs="*",
                        help="faqat shu kalitlar; bermasa korpus bo'yicha")
    parser.add_argument("--tekshir", action="store_true",
                        help="yozmaydi, snapshotda yo'q kalitlarni aytadi")
    args = parser.parse_args(argv)

    want = set(args.kalitlar) or corpus_keys()
    have, date = read_snapshot()
    missing = sorted(want - set(have), key=lambda k: int(k[1:]))

    if args.tekshir:
        print("snapshot: %d kalit, sana %s" % (len(have), date or "yo'q"))
        print("korpusda: %d kalit" % len(want))
        if missing:
            print("snapshotda yo'q (%d): %s" % (len(missing), " ".join(missing)))
            return 1
        extra = sorted(set(have) - want, key=lambda k: int(k[1:]))
        if extra:
            print("korpusda ishlatilmaydi (%d): %s" % (len(extra), " ".join(extra)))
        print("snapshot korpusni qoplaydi.")
        return 0

    rows = dict(have)
    added = unchecked = 0
    for key in sorted(want, key=lambda k: int(k[1:])):
        if key in rows and rows[key].get("tur") != MISSING:
            continue
        data = fetch(key)
        if data is None:
            rows[key] = {"tur": MISSING, "daraja": MISSING,
                         "scope": MISSING}
            unchecked += 1
            continue
        rows[key] = {"tur": data.get("type", MISSING),
                     "daraja": data.get("defaultSeverity", MISSING),
                     "scope": data.get("scope", MISSING)}
        added += 1
    today = write_snapshot(rows)
    print("snapshot yozildi: %d kalit, %d yangi olindi, %d tekshirilmadi, "
          "sana %s" % (len(rows), added, unchecked, today))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
