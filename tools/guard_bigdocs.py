#!/usr/bin/env python3
"""PreToolUse hook: monolit hujjatni to'liq o'qishni to'sadi.

Eng katta hujjat ~837k token, kontekst oynasi esa 200k. To'liq o'qish
imkonsiz, lekin urinish sessiyani buzadi. Bu hook shunday chaqiruvni
to'xtatib, o'rniga tools/doc.sh ni ko'rsatadi.

Chegaralangan o'qish (Read limit bilan, sed/grep/head oralig'i) o'tadi.
"""

import json
import os
import re
import sys

BIG_DOCS = (
    "java-spring-design-patterns.md",
    "java-spring-architect-mindset.md",
    "java-spring-sonarqube.md",
    "java-spring-testing-handbook.md",
)

# Read uchun: shu satrdan ko'p bo'lmagan o'qish ruxsat etiladi.
MAX_READ_LINES = 1200

# Faylni boshdan oxirigacha oqizadigan buyruqlar.
# Argumentlar oralig'ida na yangi satr, na '>' bo'lishi mumkin. Shu tufayli
# `cat > fayl <<EOF ...` kabi YOZISH buyrug'i va heredoc matni ichida
# tasodifan uchragan hujjat nomi noto'g'ri to'silmaydi.
SLURP_RE = re.compile(
    r"(?:^|[|;&]\s*|\$\(\s*)(?:cat|bat|less|more|most|view)\s+[^|;&\n>]*"
    r"(?:" + "|".join(re.escape(name) for name in BIG_DOCS) + r")"
)

HINT = (
    "Bu hujjatlar juda katta (eng kattasi ~837k token, kontekst oynasi 200k). "
    "To'liq o'qish o'rniga indeksdan foydalaning:\n"
    "  tools/doc.sh find [-f] <so'rov>      - bo'limni topish\n"
    "  tools/doc.sh show <hujjat> <raqam>   - faqat o'sha bo'limni o'qish\n"
    "  tools/doc.sh toc | outline <hujjat>  - tuzilishni ko'rish\n"
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


def check_read(tool_input):
    path = tool_input.get("file_path") or ""
    if os.path.basename(path) not in BIG_DOCS:
        return
    limit = tool_input.get("limit")
    if isinstance(limit, int) and 0 < limit <= MAX_READ_LINES:
        return
    deny(
        "%s chegarasiz o'qilmoqda." % os.path.basename(path)
        if limit is None
        else "%s uchun limit=%s juda katta (maksimum %d)."
        % (os.path.basename(path), limit, MAX_READ_LINES)
    )


def check_bash(tool_input):
    command = tool_input.get("command") or ""
    match = SLURP_RE.search(command)
    if match:
        deny("Bu buyruq hujjatni to'liq oqizadi: %s" % match.group(0).strip())


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # hook hech qachon chaqiruvni xato tufayli to'smaydi
    tool_input = payload.get("tool_input") or {}
    if payload.get("tool_name") == "Read":
        check_read(tool_input)
    elif payload.get("tool_name") == "Bash":
        check_bash(tool_input)


if __name__ == "__main__":
    main()
