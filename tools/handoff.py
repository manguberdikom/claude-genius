#!/usr/bin/env python3
"""Sessiya kontekstini o'lchaydi va yangi sessiya uchun prompt beradi.

    python3 tools/handoff.py              # o'lchov va tavsiya
    python3 tools/handoff.py --prompt     # yangi sessiya uchun tayyor matn
    python3 tools/handoff.py --limit 400000

Nega o'lchov kerak: kontekst to'lganini hech kim sezmaydi. Javoblar
sekinlashadi, eski tafsilot yangisini siqib chiqaradi, va buni faqat
natija yomonlashgandan keyin bilib olinadi. Shuning uchun bu yerda
taxmin emas, transkriptdagi haqiqiy raqam o'qiladi: har javobning
`usage` yozuvida kontekst hajmi turadi.

Chegara taxmin qilinmaydi. Sessiyada siqish (compact) bo'lgan bo'lsa,
undan oldingi eng katta kontekst - oynaning haqiqiy hajmi, shuning
uchun chegara aynan shundan olinadi. Siqish bo'lmagan bo'lsa --limit
yoki CONTEXT_LIMIT ishlatiladi va bu ochiq aytiladi.
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Siqish bo'lmagan sessiyada tayanch yo'q, shuning uchun e'lon qilingan
# qiymat ishlatiladi va javobda "taxminiy" deb belgilanadi.
DEFAULT_LIMIT = int(os.environ.get("CONTEXT_LIMIT", "200000"))

# Shu nisbatdan keyin yangi sessiya tavsiya qilinadi. 0.75 tanlangan:
# qolgan chorak ishni yakunlab, topshiriqni yozishga yetadi.
WARN_RATIO = 0.75


def transcript():
    """Shu proyektning eng yangi transkript fayli, yo'q bo'lsa None."""
    slug = ROOT.replace(os.sep, "-")
    base = os.path.expanduser(os.path.join("~", ".claude", "projects", slug))
    if not os.path.isdir(base):
        return None
    files = [os.path.join(base, f) for f in os.listdir(base)
             if f.endswith(".jsonl")]
    return max(files, key=os.path.getmtime) if files else None


def context_size(usage):
    return (usage.get("input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0))


def measure(path):
    """current, peak, siqishgacha bo'lgan peak, siqish soni, navbat soni."""
    current = peak = before_compact = compacts = turns = 0
    seen_compact = False
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if row.get("isCompactSummary") or row.get("compactMetadata"):
                compacts += 1
                seen_compact = True
            usage = (row.get("message") or {}).get("usage")
            if not usage:
                continue
            turns += 1
            size = context_size(usage)
            current = size or current
            peak = max(peak, size)
            if not seen_compact:
                before_compact = max(before_compact, size)
    return current, peak, before_compact, compacts, turns


def limit_for(before_compact, compacts, override):
    """(chegara, manbasi). Siqish bo'lgan bo'lsa o'lchangan, aks holda e'lon."""
    if override:
        return override, "berilgan (--limit)"
    if compacts and before_compact:
        return before_compact, "o'lchangan (siqishdan oldingi eng katta)"
    return DEFAULT_LIMIT, "taxminiy (o'lchanmagan, CONTEXT_LIMIT)"


def git(*args):
    try:
        out = subprocess.run(["git"] + list(args), capture_output=True,
                             text=True, cwd=ROOT, timeout=20)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def memory_lines():
    out = []
    for rel in ("memory/claude-genius/MEMORY.md", "memory/umumiy/MEMORY.md"):
        path = os.path.join(ROOT, rel)
        if os.path.isfile(path):
            out.append(rel)
    return out


def report(override):
    path = transcript()
    if not path:
        print("Transkript topilmadi, kontekst o'lchanmadi.")
        print("Tavsiya faqat o'lchovga tayanadi, shuning uchun berilmaydi.")
        return 2
    current, peak, before, compacts, turns = measure(path)
    limit, source = limit_for(before, compacts, override)
    ratio = current / limit if limit else 0

    print("Kontekst: %s / %s token (%.0f%%)"
          % (f"{current:,}", f"{limit:,}", 100 * ratio))
    print("  chegara manbasi : %s" % source)
    print("  eng katta       : %s" % f"{peak:,}")
    print("  siqish (compact): %d" % compacts)
    print("  javob soni      : %d" % turns)

    print()
    if compacts:
        print("TAVSIYA: yangi sessiya. Bu sessiya allaqachon %d marta "
              "siqilgan," % compacts)
        print("ya'ni tafsilot yo'qolgan. Yangi sessiya topshiriq bilan "
              "aniqroq boshlaydi.")
    elif ratio >= WARN_RATIO:
        print("TAVSIYA: yangi sessiya. Kontekst %.0f%% to'lgan, qolgani "
              "ishni" % (100 * ratio))
        print("yakunlab topshiriq yozishga yetadi, yangi katta ishga emas.")
    else:
        print("TAVSIYA: davom etish. Kontekstda joy bor.")
    print("\nTayyor prompt: python3 tools/handoff.py --prompt")
    return 0


def prompt(override):
    path = transcript()
    current = limit = 0
    source = "o'lchanmagan"
    if path:
        current, _, before, compacts, _ = measure(path)
        limit, source = limit_for(before, compacts, override)

    branch = git("rev-parse", "--abbrev-ref", "HEAD") or "?"
    commits = git("log", "--oneline", "-5")
    dirty = git("status", "--short")

    print("# Yangi sessiya uchun prompt: pastdagini nusxalab yuboring\n")
    print("```")
    print("/manguberdi")
    print()
    print("Oldingi sessiya kontekstga sig'may uzatildi"
          + (" (%s / %s token, %s)" % (f"{current:,}", f"{limit:,}", source)
             if current else "") + ".")
    print()
    print("Maqsad: <bir jumla, tekshirib bo'ladigan>")
    print()
    print("Bajarildi:")
    print("  <qadam>   <- har biri bir qator")
    print()
    print("Qolgan:")
    print("  <qadam>")
    print()
    print("Qarorlar: <qaror> (<hujjat> <raqam>), nega shunday tanlangan")
    print()
    print("Keyingi qadam: <aniq birinchi harakat>")
    print()
    print("Mashina bergan holat, to'ldirish shart emas:")
    print("  branch: %s" % branch)
    if commits:
        print("  oxirgi commitlar:")
        for line in commits.split("\n"):
            print("    %s" % line)
    print("  ishchi daraxt: %s"
          % ("toza" if not dirty else "%d fayl o'zgargan" % len(dirty.split("\n"))))
    for rel in memory_lines():
        print("  memory indeksi: %s" % rel)
    print("```")
    print("\nUch burchakli joylarni to'ldiring: faqat siz bilasiz. "
          "Qolganini mashina yozdi.")
    print("Topshiriqni saqlash kerak bo'lsa `references/kontekst.md` "
          "marshrutiga qarang.")
    return 0


def main():
    args = sys.argv[1:]
    override = 0
    if "--limit" in args:
        index = args.index("--limit")
        if index + 1 < len(args) and args[index + 1].isdigit():
            override = int(args[index + 1])
    if "--prompt" in args:
        return prompt(override)
    return report(override)


if __name__ == "__main__":
    sys.exit(main())
