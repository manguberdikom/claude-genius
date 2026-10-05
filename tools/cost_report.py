#!/usr/bin/env python3
"""Har navbatda qat'iy ketadigan kontekstni sanaydi.

    python3 tools/cost_report.py [--budget N]

Nega: sessiya boshlanishida yuklanadigan matn har bir navbatda qayta
hisoblanadi. CLAUDE.md ga qo'shilgan o'n qator bir marta emas, yuz marta
to'lanadi. Bu o'sish sezilmay boradi, shuning uchun o'lchanadi.

Token soni tilga qarab o'lchangan nisbatdan (o'zbekcha 1.8, inglizcha 2.7
belgi/token). Aniq son kerak bo'lsa Anthropic API ning count_tokens
chaqiruvi ishlatiladi; bu yerda maqsad o'sishni ko'rish, hisob-kitob
qilish emas.
"""

import argparse
import importlib.util
import os
import re
import signal
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2026-10-05 da Opus 5.5 sessiyasida transkriptdagi kontekst farqidan
# o'lchangan: o'zbekcha matn ~1.8, inglizcha ~2.7 belgi/token. Model yoki
# tokenizer almashsa qayta o'lchanadi (kalit bo'lsa count_tokens bilan).
CHARS_PER_TOKEN = {"uz": 1.8, "en": 2.7}
EN_WORDS = re.compile(r"\b(the|and|or|of|to|when|a|an|is|for|with|use|in)\b", re.I)
EN_SHARE = 0.08
# Byudjet joriy JAMI ustiga ~300 token zahira, taxminan bitta skill
# tavsifi. Teng qilib qo'yilmaydi, aks holda har kichik tahrir yolg'on
# signal beradi. Shundan oshsa, yangi narsa qo'shishdan oldin eskisi
# qisqartiriladi yoki birlashtiriladi. 2026-10-05 da o'lchangan JAMI 6106.
DEFAULT_BUDGET = 6500

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FIELD_RE = re.compile(r"^(\w+):\s*(.*)$", re.M)
# Read natijasi har qatorga raqam prefiksi qo'shadi (`     1<TAB>`).
READ_PREFIX = 7


def lang_of(text):
    """Inglizcha xizmat so'zlari ulushi bo'yicha: "en" yoki "uz"."""
    words = len(text.split()) or 1
    return "en" if len(EN_WORDS.findall(text)) / words >= EN_SHARE else "uz"


def tokens(text, lang=None):
    return int(len(text) / CHARS_PER_TOKEN[lang or lang_of(text)])


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def listing_text(path, kind):
    """Claude Code ro'yxatiga kiradigan qator va uning tili.

    Skill `- nom: tavsif`, agent `- nom: tavsif (Tools: ...)` bo'lib
    kiradi. model qatori ro'yxatda chiqmaydi, shuning uchun sanalmaydi.
    """
    match = FRONT_RE.match(read(path))
    if not match:
        return "", "uz"
    front = dict(FIELD_RE.findall(match.group(1)))
    default = (os.path.basename(os.path.dirname(path)) if kind == "skill"
               else os.path.splitext(os.path.basename(path))[0])
    name = front.get("name") or default
    desc = front.get("description", "")
    if kind == "agent":
        line = "- %s: %s (Tools: %s)\n" % (name, desc, front.get("tools") or "*")
    else:
        line = "- %s: %s\n" % (name, desc)
    return line, lang_of(desc)


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


def listing_row(label, paths, kind, note):
    """Har fayl o'z tilida sanaladi, keyin yig'iladi."""
    lines = [listing_text(p, kind) for p in paths]
    return (label % len(paths), sum(len(t) for t, _ in lines),
            sum(tokens(t, lang) for t, lang in lines), note)


def memory_indexes():
    """CLAUDE.md talabi bilan sessiya boshida o'qiladigan ikki indeks."""
    out = []
    for slug in ("umumiy", os.path.basename(ROOT).lower()):
        path = os.path.join(ROOT, "memory", slug, "MEMORY.md")
        if os.path.exists(path):
            out.append(read(path))
    return out


def suggest_worst(path, count):
    """Taklif hooki matnining eng uzun holati, belgida.

    Indeks bo'lsa hookning o'z render() i eng uzun `count` sarlavha bilan
    chaqiriladi: nomzodlar hook ishlatadigan titles_by_key dan, bob
    sarlavhasi ham (ko'p so'zli bob taxallusi bob raqamini beradi). Modul
    ROOT dagi fayldan yuklanadi, shunda u indeksni ham o'sha ROOT dan
    o'qiydi. Indekssiz: sarlavha ~55, qator ~150 belgi.
    """
    if not os.path.exists(os.path.join(ROOT, "index", "sections.tsv")):
        return 55 + count * 150
    spec = importlib.util.spec_from_file_location("suggest_sections", path)
    S = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(S)
    titles = S.titles_by_key(S.read_tsv("sections.tsv"))
    hits = [(doc, num, title, 0) for (doc, num), title in titles.items()]
    hits.sort(key=lambda hit: len(S.render([hit])), reverse=True)
    return len(S.render(hits[:count]))


def collect():
    """(nom, belgi, token, izoh) to'rtliklari: har navbatda ketadigan narsalar."""
    rows = []

    claude_md = os.path.join(ROOT, "CLAUDE.md")
    if os.path.exists(claude_md):
        text = read(claude_md)
        rows.append(("CLAUDE.md", len(text), tokens(text),
                     "to'liq, har sessiyada"))

    skills = glob_sorted(os.path.join(ROOT, ".claude", "skills"), "SKILL.md")
    if skills:
        rows.append(listing_row("%d skill qatori", skills, "skill",
                                "nom+tavsif; tanasi trigger bo'lganda"))

    agents = glob_sorted(os.path.join(ROOT, ".claude", "agents"), "")
    if agents:
        rows.append(listing_row("%d agent qatori", agents, "agent",
                                "nom+tavsif+tools; tanasi chaqirilganda"))

    memory = memory_indexes()
    if memory:
        size = sum(len(t) + READ_PREFIX * t.count("\n") for t in memory)
        rows.append(("%d MEMORY.md indeksi" % len(memory), size,
                     int(size / CHARS_PER_TOKEN["uz"]),
                     "CLAUDE.md talabi: ish boshida o'qiladi"))

    suggest = os.path.join(ROOT, "tools", "suggest_sections.py")
    if os.path.exists(suggest):
        # Taklif hooki: eng uzun MAX_SUGGESTIONS sarlavha bilan render()
        # natijasi (suggest_worst). Promptda Sonar kaliti bo'lsa har kalitga
        # yana bitta ~45 belgilik qator qo'shiladi ("To'liq ro'yxat: ...
        # rule java:Sxxxx"); u kamdan-kam, shuning uchun bu yerda sanalmaydi.
        match = re.search(r"^MAX_SUGGESTIONS = (\d+)", read(suggest), re.M)
        count = int(match.group(1)) if match else 4
        size = suggest_worst(suggest, count)
        rows.append(("taklif hooki (eng ko'pi)", size,
                     int(size / CHARS_PER_TOKEN["uz"]),
                     "eng uzun %d qator; Sonar kaliti +45, mavzusiz 0" % count))

    handoff = os.path.join(ROOT, "tools", "handoff.py")
    if os.path.exists(handoff) and '"--hook"' in read(handoff):
        rows.append(("kontekst hooki (eng ko'pi)", 170,
                     int(170 / CHARS_PER_TOKEN["uz"]),
                     "chegaradan past bo'lsa 0"))

    return rows


def on_demand():
    """Navbatga kirmaydigan, lekin hajmi kuzatiladigan narsalar."""
    for label, path in (("docs/ korpusi", "docs"), ("index/", "index")):
        full = os.path.join(ROOT, path)
        if not os.path.isdir(full):
            continue
        size = sum(os.path.getsize(os.path.join(dp, f))
                   for dp, _, fs in os.walk(full) for f in fs)
        how = ("doc.sh show bilan bo'lim-bo'lim" if path == "docs"
               else "grep qilinadi, kontekstga olinmaydi")
        print("%-26s %8.1f MB            %s" % (label, size / 1048576, how))

    body = os.path.join(ROOT, ".claude", "skills", "manguberdi", "SKILL.md")
    if os.path.exists(body):
        text = read(body)
        print("%-26s %8d %9d   %s" % ("manguberdi tanasi", len(text),
                                     tokens(text, "uz"),
                                     "manguberdi sessiyasida doimiy"))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Har navbatda qat'iy ketadigan kontekstni sanaydi.")
    parser.add_argument("--budget", type=int, default=DEFAULT_BUDGET,
                        help="token chegarasi (standart: %(default)s)")
    budget = parser.parse_args(argv).budget

    rows = collect()
    print("# Har navbatdagi qat'iy kontekst\n")
    print("%-26s %8s %9s   %s" % ("manba", "belgi", "~token", "izoh"))
    chars = estimate = 0
    for name, size, count, note in rows:
        chars += size
        estimate += count
        print("%-26s %8d %9d   %s" % (name, size, count, note))
    print("%-26s %8d %9d" % ("JAMI", chars, estimate))

    print("\n# Talab bo'yicha o'qiladigan (navbatda emas)\n")
    on_demand()

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
