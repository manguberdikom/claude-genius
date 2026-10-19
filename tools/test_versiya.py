#!/usr/bin/env python3
"""versiya.py: o'rnatilgan manifest va klon holatida versiya, commit va
CHANGELOG bo'limi chiqadi.

    python3 tools/test_versiya.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def run(config):
    env = dict(os.environ, CLAUDE_CONFIG_DIR=config)
    return subprocess.run([sys.executable, os.path.join(HERE, "versiya.py")],
                          capture_output=True, text=True, env=env).stdout


def main():
    tmp = tempfile.mkdtemp(prefix="versiya-")
    try:
        version = open(os.path.join(ROOT, "VERSION"), encoding="utf-8").read().strip()
        bare = run(tmp)
        skill = os.path.join(tmp, "skills", "manguberdi")
        os.makedirs(skill)
        head = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD~1"],
                              capture_output=True, text=True).stdout.strip()
        with open(os.path.join(skill, ".genius.json"), "w", encoding="utf-8") as handle:
            json.dump({"versiya": version, "commit": head, "sana": "2026-10-19T10:00:00",
                       "root": ROOT, "clone": ROOT}, handle)
        installed = run(tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    checks = [
        ("manifestsiz: klon versiyasi", ("manguberdi %s: o'rnatilmagan" % version) in bare),
        ("CHANGELOG bo'limi chiqadi", "Shu versiyada:" in bare),
        ("manifest: versiya, sana va commit", ("manguberdi %s: o'rnatilgan 2026-10-19" % version)
         in installed and head[:12] in installed),
        ("manifest: klonda yangi commit aytiladi", "o'rnatilgandan keyin 1 commit" in installed),
    ]
    failures = 0
    for name, ok in checks:
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(checks) - failures, len(checks)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
