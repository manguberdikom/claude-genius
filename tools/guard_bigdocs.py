#!/usr/bin/env python3
"""PreToolUse hook: juda katta hujjat faylini butunligicha o'qishni to'sadi.

docs/ dagi eng katta bob ~68k token, dist/ dagi yig'ma fayl esa bundan ham
kattaroq. Bitta bo'lim o'rtacha ~700 token, ya'ni javob deyarli har doim
kichik bo'lakda. Bu hook butun faylni oqizadigan chaqiruvni to'xtatib,
o'rniga tools/doc.sh ni ko'rsatadi.

Fayllar ro'yxati qattiq yozilmagan: har chaqiruvda haqiqiy satr soni
sanaladi, shuning uchun yangi bob qo'shilganda hech narsa yangilanmaydi.

Chegaralangan o'qish o'tadi: limit berilgan Read, sed oralig'i, grep, head.
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

HINT = (
    "Butun faylni o'qish o'rniga indeksdan foydalaning:\n"
    "  tools/doc.sh find [-f] <so'rov>      - bo'limni topish\n"
    "  tools/doc.sh show <hujjat> <raqam>   - faqat o'sha bo'limni o'qish\n"
    "  tools/doc.sh outline <hujjat> [bob]  - ichidagi bo'limlar\n"
    "Batafsil: CLAUDE.md"
)


def deny(reason):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason + "\n" + HINT,
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


def check_bash(tool_input):
    command = tool_input.get("command") or ""
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
