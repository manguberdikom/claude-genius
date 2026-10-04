#!/usr/bin/env python3
"""PreToolUse hook: qimmat amallarni to'xtatib, arzon yo'lni ko'rsatadi.

Ikki xil qimmatlik bor va ikkalasi ham shu yerda tekshiriladi, chunki
alohida hook har Bash chaqiruvida ikkinchi marta Python ishga tushirardi.

1. Kontekst qimmatligi. docs/ dagi eng katta bob ~68k token, bitta bo'lim
   esa ~700. Butun faylni o'qish kontekstni yoqadi, holbuki javob kichik
   bo'lakda turadi. Fayllar ro'yxati yozilmagan: har chaqiruvda haqiqiy
   satr soni sanaladi, shuning uchun yangi bob qo'shilsa ham ishlaydi.

2. Pul va vaqt qimmatligi. Konteyner ko'tarish yoki bazaga ulanish bir
   necha daqiqa va katta chiqish beradi, holbuki kerakli javob ko'pincha
   kodning o'zida: entity sinflari sxemani to'liq tasvirlaydi, test
   chiqishi esa xatoni aytib turadi. Bu amallar to'siladi, lekin yo'l
   yopiq emas: buyruq oldiga COST_OK=1 qo'yilsa o'tadi.

Chegaralangan o'qish o'tadi: limit berilgan Read, sed oralig'i, grep, head.
Tashxis buyruqlari ham o'tadi: docker ps, docker logs, docker images.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Shu papkalardagi markdown fayllar kuzatiladi.
WATCHED_DIRS = ("docs", "dist")

# Bundan uzun faylni butunligicha o'qish to'siladi.
MAX_LINES = int(os.environ.get("DOC_MAX_LINES", "1200"))

# Faylni boshdan oxirigacha oqizadigan buyruqlar. Argumentlar oralig'ida na
# yangi satr, na '>' bo'lishi mumkin: shunda `cat > fayl <<EOF ...` kabi
# YOZISH buyrug'i va heredoc matnidagi fayl nomi noto'g'ri to'silmaydi.
SLURP_RE = re.compile(
    r"(?:^|[|;&]\s*|\$\(\s*)(?:cat|bat|less|more|most|view)\s+([^|;&\n>]*)"
)

# Buyruq oldiga qo'yilsa, qimmat amal baribir bajariladi.
ESCAPE = "COST_OK=1"

# Pul va vaqt sarflaydigan amallar. Tashxis fe'llari (ps, logs, images,
# inspect, version) ataylab yo'q: ular arzon va ko'pincha aynan kerak.
EXPENSIVE = (
    (re.compile(r"\bdocker(?:\s+compose)?\s+(?:up|run|build|pull|start)\b"),
     "Konteyner ko'tarish yoki yig'ish",
     "Avval arzon yo'lni sinang: test chiqishidagi xato odatda sababni "
     "aytadi, baza tuzilishini esa entity sinflari ko'rsatadi:\n"
     "  python3 tools/schema_from_entities.py <src>\n"
     "Konteyner haqiqatan kerak bo'lsa: COST_OK=1 <buyruq>"),
    (re.compile(r"\bdocker-compose\s+(?:up|build|pull|start)\b"),
     "Konteyner ko'tarish yoki yig'ish",
     "Avval test chiqishini va entity sinflarini o'qing:\n"
     "  python3 tools/schema_from_entities.py <src>\n"
     "Konteyner haqiqatan kerak bo'lsa: COST_OK=1 <buyruq>"),
    (re.compile(r"\b(?:psql|mysql|mariadb|mongosh|mongo|redis-cli)\b"
                r"(?=.*(?:-h|--host|://))"),
     "Bazaga ulanish",
     "Sxemani bilish uchun ulanish shart emas, entity sinflari uni "
     "to'liq tasvirlaydi:\n"
     "  python3 tools/schema_from_entities.py <src>\n"
     "Jonli ma'lumot haqiqatan kerak bo'lsa: COST_OK=1 <buyruq>"),
)

HINT = (
    "Butun faylni o'qish o'rniga indeksdan foydalaning:\n"
    "  tools/doc.sh find [-f] <so'rov>      - bo'limni topish\n"
    "  tools/doc.sh show <hujjat> <raqam>   - faqat o'sha bo'limni o'qish\n"
    "  tools/doc.sh outline <hujjat> [bob]  - ichidagi bo'limlar\n"
    "Batafsil: CLAUDE.md"
)


def deny(reason):
    deny_with(reason, HINT)


def deny_with(reason, hint):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason + "\n" + hint,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


def watched_path(candidate):
    """Kuzatiladigan papkadagi markdown faylning to'liq yo'li, aks holda None."""
    if not candidate.endswith(".md"):
        return None
    for base in (os.getcwd(), ROOT):
        full = os.path.normpath(os.path.join(base, candidate))
        try:
            rel = os.path.relpath(full, ROOT)
        except ValueError:
            continue
        head = rel.split(os.sep)[0]
        if head in WATCHED_DIRS and os.path.isfile(full):
            return full
    return None


def line_count(path):
    try:
        with open(path, "rb") as handle:
            return sum(1 for _ in handle)
    except OSError:
        return 0


def check_read(tool_input):
    path = tool_input.get("file_path") or ""
    full = watched_path(path)
    if full is None:
        return
    limit = tool_input.get("limit")
    if isinstance(limit, int) and 0 < limit <= MAX_LINES:
        return
    lines = line_count(full)
    if lines <= MAX_LINES:
        return
    name = os.path.relpath(full, ROOT)
    if limit is None:
        deny("%s - %d satr, chegarasiz o'qilmoqda (chegara %d)."
             % (name, lines, MAX_LINES))
    deny("%s - limit=%s juda katta (chegara %d)." % (name, limit, MAX_LINES))


def check_cost(command):
    """Konteyner va baza chaqiruvlari: arzon yo'l bor ekan, to'xtatiladi."""
    if ESCAPE in command:
        return
    for pattern, what, hint in EXPENSIVE:
        match = pattern.search(command)
        if match:
            deny_with("%s qimmat amal: %s" % (what, match.group(0)), hint)


def check_bash(tool_input):
    command = tool_input.get("command") or ""
    check_cost(command)
    for match in SLURP_RE.finditer(command):
        for arg in match.group(1).split():
            full = watched_path(arg)
            if full is None:
                continue
            lines = line_count(full)
            if lines > MAX_LINES:
                deny("Bu buyruq %d satrli faylni butunligicha oqizadi: %s"
                     % (lines, os.path.relpath(full, ROOT)))


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # hook hech qachon chaqiruvni o'z xatosi tufayli to'smaydi
    tool_input = payload.get("tool_input") or {}
    name = payload.get("tool_name")
    if name == "Read":
        check_read(tool_input)
    elif name == "Bash":
        check_bash(tool_input)


if __name__ == "__main__":
    main()
