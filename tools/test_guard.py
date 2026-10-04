#!/usr/bin/env python3
"""guard_bigdocs.py uchun sinovlar.

    python3 tools/test_guard.py

Sinov matnlari shu faylda turadi, Bash buyrug'ida emas: aks holda guard
o'z sinovini haqiqiy chaqiruv deb to'sib qo'yadi.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GUARD = os.path.join(HERE, "guard_bigdocs.py")

# 1414 satr - chegaradan katta.
BIG = "docs/patterns/25-anti-patternlar.md"
# ~200 satr - chegaradan kichik.
SMALL = "docs/clean-code/43-professional-masuliyat.md"

DENY, ALLOW = "deny", "allow"

CASES = [
    ("katta bob, chegarasiz Read", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": BIG}}),
    ("katta bob, limit=60", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "limit": 60}}),
    ("katta bob, limit=9000", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "limit": 9000}}),
    ("kichik bob, chegarasiz Read", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": SMALL}}),
    ("docs tashqarisidagi fayl", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": "README.md"}}),
    ("mavjud bo'lmagan fayl", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": "docs/yoq.md"}}),
    ("katta bobni cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat " + BIG}}),
    ("kichik bobni cat", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "cat " + SMALL}}),
    ("less", DENY, {"tool_name": "Bash", "tool_input": {"command": "less " + BIG}}),
    ("quvur ichidagi cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "x; cat " + BIG + " | tail -3"}}),
    ("sed oralig'i", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "sed -n 100,160p " + BIG}}),
    ("grep", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "grep -n God " + BIG}}),
    ("head -n", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "head -n 40 " + BIG}}),
    # Asosiy noto'g'ri-ijobiy holat: heredoc bilan YOZISH, matn ichida
    # tasodifan fayl nomi uchraydi.
    ("heredoc yozish, nom matnda", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > CLAUDE.md <<EOF\nqoida: " + BIG + " to'liq o'qilmaydi\nEOF"}}),
    ("cat > boshqa faylga", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > notes.md <<EOF\n" + BIG + "\nEOF"}}),
    ("boshqa faylni cat", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "cat README.md"}}),
    ("Bash bo'lmagan asbob", ALLOW,
     {"tool_name": "Grep", "tool_input": {"pattern": "x", "path": BIG}}),
    ("buzuq JSON", ALLOW, None),
]


def verdict(payload):
    raw = "not json" if payload is None else json.dumps(payload)
    out = subprocess.run(
        [sys.executable, GUARD], input=raw, capture_output=True, text=True, cwd=ROOT
    ).stdout.strip()
    if not out:
        return ALLOW
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"]


def main():
    missing = [p for p in (BIG, SMALL) if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        print("sinov fayllari yo'q: %s" % ", ".join(missing))
        return 1

    failures = 0
    for name, want, payload in CASES:
        got = verdict(payload)
        ok = got == want
        failures += not ok
        print("%-4s %-30s kutilgan=%-5s olingan=%s"
              % ("OK" if ok else "XATO", name, want, got))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
