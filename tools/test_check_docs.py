#!/usr/bin/env python3
"""check_docs.py uchun sinovlar.

    python3 tools/test_check_docs.py

check_docs CI da faqat haqiqiy korpusda yuradi, korpus esa toza. Demak
uning salbiy yo'llari hech qachon ishlamaydi: tekshiruv olib tashlansa
yoki buzilsa ham CI yashil qoladi. Bu yerda vaqtinchalik papkada kichik
hujjat yasaladi va har buzilish alohida xato berishi tekshiriladi.
"""

import contextlib
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_docs  # noqa: E402

CHAPTERS = [
    {"num": 1, "title": "1. Birinchi bob", "file": "01-birinchi.md",
     "part": None, "sections": 2},
    {"num": 2, "title": "2. Ikkinchi bob", "file": "02-ikkinchi.md",
     "part": None, "sections": 2},
]

FOOTERS = {
    1: "[Mundarija](README.md) · [2. Ikkinchi bob &rarr;](02-ikkinchi.md)",
    2: "[&larr; 1. Birinchi bob](01-birinchi.md) · [Mundarija](README.md)",
}


def chapter(n):
    return "\n".join([
        "<!-- doc: sinov | chapter: %d | part:  -->" % n,
        "",
        "[Sinov hujjati](../../README.md) / [Sinov](README.md)",
        "",
        "# %s" % CHAPTERS[n - 1]["title"],
        "",
        "## %d.1 Mavzu" % n,
        "",
        "Matn.",
        "",
        "```markdown",
        "## Namuna sarlavha, bob bo'limi emas",
        "```",
        "",
        "## %d.2 Amalda qo'llash" % n,
        "",
        "- Band.",
        "",
        "---",
        "",
        FOOTERS[n],
        "",
    ])


FILES = {
    "README.md": "# Kitob\n\n[Sinov](docs/sinov/README.md)\n",
    "CLAUDE.md": ("# Ko'rsatma\n\n`tools/doc.sh show sinov 1.1`\n\n"
                  "```bash\npython3 tools/asbob.py\n```\n"),
    "tools/doc.sh": "case \"$1\" in\n  show) cmd_show ;;\n  find) cmd_find ;;\nesac\n",
    "tools/asbob.py": "",
    ".claude/skills/sinov/SKILL.md": (
        "| Mavzu | Bo'lim |\n|---|---|\n"
        "| Birinchi | `docs/sinov/01-birinchi.md#11-mavzu` |\n"
        "| Ikkinchi | `docs/sinov/02-ikkinchi.md` |\n"),
    "docs/manifest.json": json.dumps({"sinov": {
        "title": "Sinov hujjati", "label": "Sinov", "chapters": CHAPTERS}}),
    "docs/sinov/README.md": (
        "# Sinov\n\n"
        "- **1.** [Birinchi bob](01-birinchi.md) - 2 bo'lim\n"
        "- **2.** [Ikkinchi bob](02-ikkinchi.md) - 2 bo'lim\n"),
    "docs/sinov/01-birinchi.md": chapter(1),
    "docs/sinov/02-ikkinchi.md": chapter(2),
}


def run(tmp, name, change=None):
    """Toza nusxa yasaydi, o'zgartiradi va check_docs xatolarini qaytaradi."""
    root = os.path.join(tmp, name)
    for rel, text in FILES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    if change:
        rel, old, new = change
        path = os.path.join(root, rel)
        text = open(path, encoding="utf-8").read()
        assert old in text, "%s da '%s' yo'q" % (rel, old)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text.replace(old, new, 1))
    saved = check_docs.ROOT
    check_docs.ROOT = root
    del check_docs.errors[:]
    del check_docs.warnings[:]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            check_docs.main()
    finally:
        check_docs.ROOT = saved
    return list(check_docs.errors)


def excused(tmp):
    """UNROUTED_OK dagi bob marshrutsiz bo'lsa ham xato bermaydi."""
    saved = dict(check_docs.UNROUTED_OK)
    check_docs.UNROUTED_OK[("sinov", 2)] = "sinov uchun"
    try:
        errs = run(tmp, "uzrli", (SKILL, "| Ikkinchi | `docs/sinov/02-ikkinchi.md` |\n", ""))
    finally:
        check_docs.UNROUTED_OK.clear()
        check_docs.UNROUTED_OK.update(saved)
    return errs == []


def expect(change, needle):
    def case(tmp):
        errs = run(tmp, needle[:20].replace(" ", "_").replace("'", ""), change)
        return any(needle in e for e in errs)
    return case


CH1 = "docs/sinov/01-birinchi.md"
CH2 = "docs/sinov/02-ikkinchi.md"
SKILL = ".claude/skills/sinov/SKILL.md"

CASES = [
    ("toza nusxada xato yo'q", lambda tmp: run(tmp, "toza") == []),
    ("H1 manifestdan farq qiladi",
     expect((CH1, "# 1. Birinchi bob", "# 1. Boshqa sarlavha"), "H1 manifest")),
    ("metadata manifestdan farq qiladi",
     expect((CH1, "chapter: 1 |", "chapter: 7 |"), "metadata manifest")),
    ("breadcrumb yo'q",
     expect((CH1, "[Sinov hujjati](../../README.md) / [Sinov](README.md)", ""),
            "breadcrumb")),
    ("yopish bo'limidan keyin bo'lim",
     expect((CH1, "- Band.\n", "- Band.\n\n## 1.3 Qo'shimcha\n"),
            "oxirgi bo'lim yopish bo'limi emas")),
    ("footer noto'g'ri qo'shniga",
     expect((CH2, "(01-birinchi.md)", "(02-ikkinchi.md)"), "footer qo'shni")),
    ("manifestdagi bo'lim soni eskirgan",
     expect(("docs/manifest.json", '"sections": 2', '"sections": 3'),
            "2 bo'lim, manifestda 3")),
    ("README dagi bo'lim soni eskirgan",
     expect(("docs/sinov/README.md", "- 2 bo'lim", "- 5 bo'lim"),
            "01-birinchi.md 5 bo'lim")),
    ("kod blokidagi asbob yo'li",
     expect(("CLAUDE.md", "tools/asbob.py", "tools/asbobXX.py"), "asbob yo'q")),
    ("doc.sh da yo'q subkomanda",
     expect(("CLAUDE.md", "doc.sh show", "doc.sh shw"), "subkomandasi yo'q")),
    ("docs/ da til belgisiz kod bloki",
     expect((CH1, "```markdown", "```"), "01-birinchi.md:11: kod blokida til belgisi")),
    ("docs/ dan tashqarida belgisiz blok xato emas",
     lambda tmp: run(tmp, "tashqari", ("CLAUDE.md", "```bash", "```")) == []),
    ("bob hech qaysi skill jadvalida yo'q",
     expect((SKILL, "`docs/sinov/02-ikkinchi.md`", "`docs/sinov/`"),
            "docs/sinov: 2-bob hech qaysi skill")),
    ("UNROUTED_OK dagi bob kechiriladi", excused),
]


def main():
    tmp = tempfile.mkdtemp(prefix="check_docs_")
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn(tmp))
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
