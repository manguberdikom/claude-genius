#!/usr/bin/env python3
"""code_gap.py uchun sinovlar.

    python3 tools/test_code_gap.py

Maxraj avval manifestdagi `sections` dan olinardi: unda yopish bo'limi
ham bor, shuning uchun "479 / 1037" chiqardi, CLAUDE.md esa 1007 deydi.
Bu yerda maxraj bob fayllaridan mustaqil sanaladi va bo'lim raqami
berilganda asbob traceback bilan yiqilmasligi tekshiriladi.
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "code_gap.py")
sys.path.insert(0, HERE)

import code_gap  # noqa: E402

MANIFEST = json.load(open(os.path.join(ROOT, "docs", "manifest.json"),
                          encoding="utf-8"))


def run(*args):
    proc = subprocess.run([sys.executable, TOOL] + list(args),
                          capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout, proc.stderr


def plain_sections(key):
    """Fence tashqarisidagi `## ` sarlavhalar, yopish bo'limisiz."""
    count = 0
    for ch in MANIFEST[key]["chapters"]:
        if not ch["num"]:
            continue
        fence = False
        path = os.path.join(ROOT, "docs", key, ch["file"])
        for line in open(path, encoding="utf-8"):
            if line.startswith("```"):
                fence = not fence
            elif not fence and line.startswith("## ") and not re.search(
                    r"Amalda qo'llash|Arxitektor nazorat", line):
                count += 1
    return count


def case_maxraj_yopishsiz(_):
    return all(code_gap.gaps(key)[1] == plain_sections(key) for key in MANIFEST)


def case_surat_maxrajdan_oshmaydi(_):
    return all(len(g) <= total for g, total in map(code_gap.gaps, MANIFEST))


def case_yigindi_chiqishi(_):
    code, out, _ = run()
    _, total = code_gap.gaps("patterns")
    return code == 0 and re.search(r"patterns .* / %d$" % total, out, re.M)


def case_bob_rejimi(_):
    code, _, err = run("patterns", "17")
    return code == 0 and "kodsiz bo'lim" in err


def case_bolim_raqami(_):
    """`17.2` butun bobga kengaymaydi va traceback bermaydi."""
    code, out, err = run("patterns", "17.2")
    lines = [l for l in out.splitlines() if l.strip()]
    return (code == 0 and "Traceback" not in err
            and all(l.startswith("17.2 ") for l in lines))


def case_notogri_argument(_):
    code, _, err = run("patterns", "abc")
    return code != 0 and "Traceback" not in err and "raqami kerak" in err


CASES = [
    ("maxraj yopish bo'limlarisiz", case_maxraj_yopishsiz),
    ("surat maxrajdan oshmaydi", case_surat_maxrajdan_oshmaydi),
    ("yig'indi o'sha maxrajni chiqaradi", case_yigindi_chiqishi),
    ("bob rejimi ishlaydi", case_bob_rejimi),
    ("bo'lim raqami faqat o'sha yozuv", case_bolim_raqami),
    ("noto'g'ri argument xabar beradi", case_notogri_argument),
]


def main():
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn(None))
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
