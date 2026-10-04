#!/usr/bin/env python3
"""guard_bigdocs.py uchun sinovlar.

Sinov matnlari shu faylda turadi, Bash buyrug'ida emas: aks holda guard
o'z sinovini haqiqiy chaqiruv deb to'sib qo'yadi.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "guard_bigdocs.py")

BIG = "java-spring-design-patterns.md"
SONAR = "java-spring-sonarqube.md"
MIND = "java-spring-architect-mindset.md"

DENY, ALLOW = "deny", "allow"

CASES = [
    ("chegarasiz Read", DENY, {"tool_name": "Read", "tool_input": {"file_path": BIG}}),
    ("limitli Read (60)", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "limit": 60}}),
    ("haddan katta limit", DENY,
     {"tool_name": "Read", "tool_input": {"file_path": BIG, "limit": 9000}}),
    ("boshqa faylni Read", ALLOW,
     {"tool_name": "Read", "tool_input": {"file_path": "README.md"}}),
    ("cat monolit", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat " + SONAR}}),
    ("absolut yo'l bilan cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "cat /home/u/" + MIND}}),
    ("quvur ichidagi cat", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "x; cat " + MIND + " | head -5"}}),
    ("less", DENY, {"tool_name": "Bash", "tool_input": {"command": "less " + BIG}}),
    ("sed oralig'i", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "sed -n 100,160p " + SONAR}}),
    ("grep", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "grep -n Circuit " + BIG}}),
    ("head -n", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "head -n 40 " + SONAR}}),
    # Asosiy noto'g'ri-ijobiy holat: heredoc bilan YOZISH, matn ichida
    # tasodifan hujjat nomi uchraydi.
    ("heredoc yozish, nom matnda", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > CLAUDE.md <<EOF\nqoida: " + BIG + " to'liq o'qilmaydi\nEOF"}}),
    ("cat > boshqa faylga", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "cat > notes.md <<EOF\n" + SONAR + "\nEOF"}}),
    ("boshqa faylni cat", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "cat README.md"}}),
    ("buzuq JSON", ALLOW, None),
]


def verdict(payload):
    raw = "not json" if payload is None else json.dumps(payload)
    out = subprocess.run(
        [sys.executable, GUARD], input=raw, capture_output=True, text=True
    ).stdout.strip()
    if not out:
        return ALLOW
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"]


def main():
    failures = 0
    for name, want, payload in CASES:
        got = verdict(payload)
        ok = got == want
        failures += not ok
        print("%-4s %-28s kutilgan=%-5s olingan=%s"
              % ("OK" if ok else "XATO", name, want, got))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
