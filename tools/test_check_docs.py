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
import re
import shutil
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
        "> Holat: AI yozgan, inson tekshirmagan.",
        "",
        "# %s" % CHAPTERS[n - 1]["title"],
        "",
        "## %d.1 Mavzu" % n,
        "",
        "Matn.",
        "",
        "| Holat | Qoida | Toifa | Jiddiylik |",
        "| --- | --- | --- | --- |",
        "| Magic number | `java:S109` | maintainability (code smell) | Major |",
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
    "README.md": ("# Kitob\n\nJami 2 bob, 4 bo'lim.\n\n"
                  "| [Sinov](docs/sinov/README.md) | 2 bob, 4 bo'lim |\n"),
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
    # 8. Regressiya naqshlari. Fixture da ataylab ikki qator: biri oddiy
    # so'z, biri kontekstli (naqsh to'g'ri matnni tutmasligi sinaladi).
    "tools/sonar_rules.tsv": ("# sana: 2026-01-01\n"
                              "kalit\ttur\tdaraja\tscope\n"
                              "S109\tCODE_SMELL\tMajor\tMain\n"
                              "S2259\ttekshirilmadi\ttekshirilmadi"
                              "\ttekshirilmadi\n"
                              "S9999\ttekshirilmadi\ttekshirilmadi"
                              "\ttekshirilmadi\n"),
    "docs/review.tsv": ("hujjat\tbob\tholat\tsana\ttekshiruvchi"
                        "\tmanbalar\txatolar\tizoh\n"
                        "sinov\t1\tai-draft\t\t\t0\t0\t\n"
                        "sinov\t2\tai-draft\t\t\t0\t0\t\n"),
    "tools/known_errors.tsv": (
        "naqsh\tizoh\tqamrov\n"
        "xatoso'z\tsinov uchun naqsh\tdocs\n"
        "java:S9999[^\\n]{0,80}public bo'lmagan\tkontekstli naqsh\tdocs\n"),
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
        # Papka nomi: needle dagi `:` va `/` Windows da nomga sig'maydi.
        errs = run(tmp, re.sub(r"\W", "_", needle[:20]), change)
        return any(needle in e for e in errs)
    return case


CH1 = "docs/sinov/01-birinchi.md"
CH2 = "docs/sinov/02-ikkinchi.md"
SKILL = ".claude/skills/sinov/SKILL.md"

CASES = [
    ("toza nusxada xato yo'q", lambda tmp: run(tmp, "toza") == []),
    ("H1 manifestdan farq qiladi",
     expect((CH1, "# 1. Birinchi bob", "# 1. Boshqa sarlavha"), "H1 manifest")),
    # 10. Tekshiruv holati.
    ("holat qatori yo'q",
     expect((CH1, "> Holat: AI yozgan, inson tekshirmagan.\n\n", ""),
            "holat qatori yo'q")),
    ("holat qatori review.tsv ga mos emas",
     expect(("docs/review.tsv", "sinov\t1\tai-draft", "sinov\t1\ttekshirilgan"),
            "holat qatori review.tsv ga mos emas")),
    ("review.tsv da bob yo'q",
     expect(("docs/review.tsv", "sinov\t2\tai-draft\t\t\t0\t0\t\n", ""),
            "2-bob yo'q")),
    ("review.tsv da noma'lum holat",
     expect(("docs/review.tsv", "sinov\t1\tai-draft", "sinov\t1\tqoralama"),
            "holati noma'lum")),
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
     expect((CH1, "```markdown", "```"), "01-birinchi.md:17: kod blokida til belgisi")),
    ("docs/ dan tashqarida belgisiz blok xato emas",
     lambda tmp: run(tmp, "tashqari", ("CLAUDE.md", "```bash", "```")) == []),
    ("bob hech qaysi skill jadvalida yo'q",
     expect((SKILL, "`docs/sinov/02-ikkinchi.md`", "`docs/sinov/`"),
            "docs/sinov: 2-bob hech qaysi skill")),
    ("UNROUTED_OK dagi bob kechiriladi", excused),
    # 8. Regressiya.
    ("tuzatilgan xato qaytsa xato beradi",
     expect((CH1, "Matn.", "Matn xatoso'z bilan."), "tuzatilgan xato qaytdi")),
    ("naqsh qator raqamini beradi",
     expect((CH1, "Matn.", "Matn xatoso'z bilan."), "01-birinchi.md:11")),
    ("kontekstli naqsh mos kelsa tutadi",
     expect((CH1, "Matn.", "`java:S9999` public bo'lmagan metod."),
            "tuzatilgan xato qaytdi")),
    ("kontekstli naqsh uzoq matnni tutmaydi",
     lambda tmp: run(tmp, "uzoq_kontekst",
                     (CH1, "Matn.", "`java:S9999` kaliti. " + "to'ldiruvchi " * 12
                      + "public bo'lmagan metod.")) == []),
    ("qamrovdan tashqari fayl tekshirilmaydi",
     lambda tmp: run(tmp, "qamrov_tashqari",
                     ("CLAUDE.md", "# Ko'rsatma", "# Ko'rsatma xatoso'z")) == []),
    ("buzuq naqsh aytiladi",
     expect(("tools/known_errors.tsv", "xatoso'z\t", "[buzuq(\t"),
            "naqsh buzuq")),
    # 9. Qo'lda yozilgan sonlar.
    ("hujjat nomli qatorda bob soni eskirgan",
     expect(("README.md", "| [Sinov](docs/sinov/README.md) | 2 bob",
             "| [Sinov](docs/sinov/README.md) | 7 bob"),
            "7 bob yozilgan, sinov da 2 ta")),
    ("hujjat nomli qatorda bo'lim soni eskirgan",
     expect(("README.md", "2 bob, 4 bo'lim |", "2 bob, 9 bo'lim |"),
            "9 bo'lim yozilgan, sinov da 4 ta")),
    ("jami bob soni hech narsaga mos emas",
     expect(("README.md", "Jami 2 bob", "Jami 5 bob"),
            "5 bob hech bir hujjatga va jamiga (2) mos emas")),
    # 11. Sonar snapshot.
    ("jadvaldagi tur metadata ga mos emas",
     expect((CH1, "| maintainability (code smell) | Major |",
             "| reliability (bug) | Major |"),
            "java:S109 turi BUG, metadata da CODE_SMELL")),
    ("jadvaldagi daraja metadata ga mos emas",
     expect((CH1, "(code smell) | Major |", "(code smell) | Blocker |"),
            "java:S109 darajasi Blocker, metadata da Major")),
    ("snapshotda yo'q kalit xato beradi",
     expect((CH1, "`java:S109`", "`java:S9998`"), "java:S9998 snapshotda yo'q")),
    ("ochiq metadata da yo'q kalit xato emas",
     lambda tmp: run(tmp, "tekshirilmadi_kaliti",
                     (CH1, "`java:S109`", "`java:S2259`")) == []),
    ("kod bloki ichidagi son tekshirilmaydi",
     lambda tmp: run(tmp, "fence_ichida",
                     ("README.md", "Jami 2 bob, 4 bo'lim.",
                      "```text\nJami 99 bob\n```")) == []),
]


def main():
    tmp = tempfile.mkdtemp(prefix="check_docs_")
    failures = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(tmp))
            except Exception as exc:
                ok, name = False, "%s (%s)" % (name, exc)
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", name))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
