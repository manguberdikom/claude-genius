#!/usr/bin/env python3
"""guard.py uchun sinovlar.

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
GUARD = os.path.join(HERE, "guard.py")

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

    # Pul va vaqt sarflaydigan amallar.
    ("docker compose up", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "docker compose up -d"}}),
    ("docker run", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "docker run -it pg:16"}}),
    ("docker build", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "docker build -t app ."}}),
    ("docker-compose up (eski)", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "docker-compose up"}}),
    ("psql uzoq hostga", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "psql -h db.local -U u app"}}),
    ("mongosh URI bilan", DENY,
     {"tool_name": "Bash", "tool_input":
      {"command": "mongosh mongodb://localhost:27017/app"}}),
    # Tashxis arzon, to'silmaydi.
    ("docker ps", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "docker ps -a"}}),
    ("docker logs", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "docker logs app --tail 50"}}),
    ("psql --version", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "psql --version"}}),
    ("mvn test to'silmaydi", ALLOW,
     {"tool_name": "Bash", "tool_input": {"command": "mvn -q test -Dtest=OrderTest"}}),
    ("powershell", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "powershell -c ls"}}),
    ("pwsh", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "pwsh ./build.ps1"}}),
    (".ps1 skript", DENY,
     {"tool_name": "Bash", "tool_input": {"command": "./deploy.ps1 -Env prod"}}),
    # "powershell" so'zi matn ichida: to'silmasligi kerak.
    ("matndagi powershell", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "grep -rn powershell docs/"}}),
    # Qidiruv naqshi ichidagi so'z chaqiruv emas. Bu holat amalda
    # uchradi: qo'riqchi shu repoda o'z sozlamalarini qidirgan grep ni
    # to'xtatib qo'ydi.
    ("naqsh ichida taqiqlangan so'zlar", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "grep -rnoiE " + chr(39) + "(" + "docker (run|build)"
                  + "|powershell)" + chr(39) + " .claude/"}}),
    ("naqsh ichida konteyner buyrug'i", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "grep -rn " + chr(39) + "docker " + "run" + chr(39) + " docs/"}}),
    ("matnga yozilgan ulanish", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "echo " + chr(39) + "psql -h localhost" + chr(39)
                  + " >> notes.txt"}}),
    # Ataylab ruxsat berilgan holat.
    ("COST_OK bilan docker", ALLOW,
     {"tool_name": "Bash", "tool_input":
      {"command": "COST_OK=1 docker compose up -d"}}),
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
