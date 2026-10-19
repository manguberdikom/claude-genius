#!/usr/bin/env python3
"""Qaysi manguberdi versiyasi o'rnatilgan va unda nima o'zgargan.

    python3 tools/versiya.py

O'rnatilgan nusxa (`~/.claude/skills/manguberdi/.genius.json`) bo'lsa
uning versiyasi, commiti va sanasi; klonda undan yangi commit bo'lsa
ularning soni. Manifest yo'q bo'lsa (klon ichida ishlash) klonning
o'zi. Oxirida shu versiyaning `CHANGELOG.md` bo'limi.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import geniuslib  # noqa: E402


def config_dir():
    return (os.environ.get("CLAUDE_CONFIG_DIR")
            or os.path.join(os.path.expanduser("~"), ".claude"))


def manifest():
    path = os.path.join(config_dir(), "skills", "manguberdi", ".genius.json")
    try:
        with open(path, encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def read(path):
    try:
        with open(path, encoding="utf-8-sig") as handle:
            return handle.read().strip()
    except OSError:
        return ""


def git(root, *args):
    proc = geniuslib.run_git(["-C", root] + list(args), timeout=10)
    return proc.stdout.strip() if proc and proc.returncode == 0 else ""


def changes(root, version):
    """CHANGELOG.md dagi `## <versiya>` bo'limi."""
    text = read(os.path.join(root, "CHANGELOG.md"))
    match = re.search(r"^## %s(?=\s|$)[^\n]*\n(.*?)(?=^## |\Z)" % re.escape(version),
                      text, re.M | re.S)
    return match.group(1).strip() if match else ""


def main():
    data = manifest()
    root = (data or {}).get("root") or ROOT
    version = (data or {}).get("versiya") or read(os.path.join(root, "VERSION")) or "?"
    if data:
        commit = str(data.get("commit") or "")
        print("manguberdi %s: o'rnatilgan %s, commit %s" % (
            version, data.get("sana", "?"), commit[:12] or "?"))
        print("snapshot: %s" % root)
        clone = data.get("clone") or ""
        if clone and commit:
            head = git(clone, "rev-parse", "HEAD")
            ahead = git(clone, "rev-list", "--count", "%s..HEAD" % commit)
            if head == commit:
                print("klon: %s, o'rnatilgan commit bilan bir xil" % clone)
            elif ahead and ahead != "0":
                print("klon: %s, HEAD %s, o'rnatilgandan keyin %s commit: "
                      "yangilash `python3 %s`" % (clone, head[:12], ahead,
                      os.path.join(root, "tools", "yangilash.py").replace("\\", "/")))
            else:
                print("klon: %s, HEAD %s: o'rnatilgan commit bilan solishtirib "
                      "bo'lmadi (klon orqada, tarix qayta yozilgan yoki git yo'q)"
                      % (clone, head[:12] or "?"))
    else:
        print("manguberdi %s: o'rnatilmagan, klon %s, commit %s" % (
            version, ROOT, git(ROOT, "rev-parse", "--short=12", "HEAD") or "?"))
    notes = changes(root, version)
    if notes:
        print("\nShu versiyada:\n" + notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
