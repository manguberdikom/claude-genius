#!/usr/bin/env python3
"""Har navbatda qat'iy ketadigan kontekstni sanaydi.

    python3 tools/cost_report.py [--budget 4500]

Nega: sessiya boshlanishida yuklanadigan matn har bir navbatda qayta
hisoblanadi. CLAUDE.md ga qo'shilgan o'n qator bir marta emas, yuz marta
to'lanadi. Bu o'sish sezilmay boradi, shuning uchun o'lchanadi.

Token soni taxminiy (belgi/3). Aniq son kerak bo'lsa Anthropic API ning
count_tokens chaqiruvi ishlatiladi; bu yerda maqsad o'sishni ko'rish,
hisob-kitob qilish emas.
"""

import os
import re
import signal
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Taxminiy: o'zbek lotin va inglizcha aralash matnda bitta token ~3 belgi.
CHARS_PER_TOKEN = 3
# Shift: orkestrator skill va olti aktyor qo'shilgandan keyin haqiqiy
# narx ~4460. Byudjet unga teng qilib qo'yilmaydi, aks holda har kichik
# tahrir yolg'on signal beradi; zahira taxminan bitta skill yoki ikkita
# agentga yetadi. Shundan oshsa, yangi narsa qo'shishdan oldin eskisi
# qisqartiriladi yoki birlashtiriladi.
DEFAULT_BUDGET = 5000

DESC_RE = re.compile(r"^description:\s*(.*?)(?=^\w+:|^---)", re.S | re.M)
FRONT_RE = re.compile(r"^---\n(.*?)\n---", re.S)


def tokens(n_chars):
    return n_chars // CHARS_PER_TOKEN


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def description_bytes(path):
    """SKILL.md yoki agent faylidagi description uzunligi."""
    front = FRONT_RE.search(read(path))
    if not front:
        return 0
    match = DESC_RE.search(front.group(1) + "\n---")
    return len(match.group(1).strip()) if match else 0


def glob_sorted(pattern_dir, name):
    if not os.path.isdir(pattern_dir):
        return []
    out = []
    for entry in sorted(os.listdir(pattern_dir)):
        path = os.path.join(pattern_dir, entry)
        if os.path.isfile(path) and entry.endswith(".md"):
            out.append(path)
        elif os.path.isdir(path) and os.path.exists(os.path.join(path, name)):
            out.append(os.path.join(path, name))
    return out


def collect():
    """(nom, bayt, izoh) uchliklari: har navbatda ketadigan narsalar."""
    rows = []

    claude_md = os.path.join(ROOT, "CLAUDE.md")
    if os.path.exists(claude_md):
        rows.append(("CLAUDE.md", len(read(claude_md)), "to'liq, har sessiyada"))

    skills = glob_sorted(os.path.join(ROOT, ".claude", "skills"), "SKILL.md")
    if skills:
        total = sum(description_bytes(p) for p in skills)
        rows.append(("%d skill tavsifi" % len(skills), total,
                     "faqat tavsif; tanasi trigger bo'lganda"))

    agents = glob_sorted(os.path.join(ROOT, ".claude", "agents"), "")
    if agents:
        total = sum(description_bytes(p) for p in agents)
        rows.append(("%d agent tavsifi" % len(agents), total,
                     "faqat tavsif; tanasi chaqirilganda"))

    suggest = os.path.join(ROOT, "tools", "suggest_sections.py")
    if os.path.exists(suggest):
        # Taklif hooki: sarlavha, MAX_SUGGESTIONS qator, ikki qator izoh.
        match = re.search(r"^MAX_SUGGESTIONS = (\d+)", read(suggest), re.M)
        count = int(match.group(1)) if match else 4
        rows.append(("taklif hooki (eng ko'pi)", 120 + count * 95 + 150,
                     "%d qatorgacha, mavzusiz so'rovda 0" % count))

    return rows


def main():
    budget = DEFAULT_BUDGET
    if "--budget" in sys.argv:
        budget = int(sys.argv[sys.argv.index("--budget") + 1])

    rows = collect()
    print("# Har navbatdagi qat'iy kontekst\n")
    print("%-26s %8s %9s   %s" % ("manba", "bayt", "~token", "izoh"))
    total = 0
    for name, size, note in rows:
        total += size
        print("%-26s %8d %9d   %s" % (name, size, tokens(size), note))
    print("%-26s %8d %9d" % ("JAMI", total, tokens(total)))

    print("\n# Talab bo'yicha o'qiladigan (navbatda emas)\n")
    for label, path in (("docs/ korpusi", "docs"), ("index/", "index")):
        full = os.path.join(ROOT, path)
        if not os.path.isdir(full):
            continue
        size = sum(os.path.getsize(os.path.join(dp, f))
                   for dp, _, fs in os.walk(full) for f in fs)
        how = ("doc.sh show bilan bo'lim-bo'lim" if path == "docs"
               else "grep qilinadi, kontekstga olinmaydi")
        print("%-26s %8.1f MB            %s" % (label, size / 1048576, how))

    estimate = tokens(total)
    print("\nByudjet: %d token." % budget)
    if estimate > budget:
        print("OSHIB KETDI: %d token, %d ortiqcha." % (estimate, estimate - budget))
        print("Eng katta ulush qaysi qatorda ekanini yuqoridan ko'ring.")
        return 1
    print("Joyida: %d token, %d zahira." % (estimate, budget - estimate))
    return 0


if __name__ == "__main__":
    # `| head` quvuri yopilganda Python BrokenPipeError beradi. Hisobot
    # asbobi buning uchun qulamasligi kerak: standart xatti-harakat
    # tiklanadi va jarayon jim tugaydi.
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
