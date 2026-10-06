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
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check_docs  # noqa: E402
import review_status  # noqa: E402

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
        "<details>",
        "<summary>Bu bobdagi 2 bo'lim</summary>",
        "",
        "- [%d.1 Mavzu](#%d1-mavzu)" % (n, n),
        "</details>",
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


def status(total, done, doing, link):
    return review_status.readme_line(total, done, doing, link)


FILES = {
    "README.md": ("# Kitob\n\nJami 2 bob, 4 bo'lim.\n\n"
                  "| [Sinov](docs/sinov/README.md) | 2 bob, 4 bo'lim |\n\n"
                  + status(2, 0, 0, "docs/review.tsv") + "\n"),
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
        "**Versiya bazasi:** Java 21.\n\n"
        + status(2, 0, 0, "../review.tsv") + "\n\n"
        "- **1.** [Birinchi bob](01-birinchi.md) - 2 bo'lim\n"
        "- **2.** [Ikkinchi bob](02-ikkinchi.md) - 2 bo'lim\n"),
    "docs/OWNERS.tsv": ("mavzu\tuy_bob\tdalil\n"
                        "ikkinchi mavzu\tsinov 2.1\tsinov uchun\n"),
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
        "java:S9999[^\\n]{0,80}public bo'lmagan\tkontekstli naqsh\tdocs\n"
        "nasrxato\tfaqat nasrda qidiriladi\tnasr\n"),
}


def write(root, change=None):
    """Toza nusxa yozadi va o'zgartiradi. change: (fayl, eski, yangi) yoki ro'yxat."""
    for rel, text in FILES.items():
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
    edit(root, change)


def edit(root, change):
    changes = change if isinstance(change, list) else ([change] if change else [])
    for rel, old, new in changes:
        path = os.path.join(root, rel)
        text = open(path, encoding="utf-8").read()
        assert old in text, "%s da '%s' yo'q" % (rel, old)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text.replace(old, new, 1))


def run(tmp, name, change=None):
    """Toza nusxa yasaydi, o'zgartiradi va check_docs xatolarini qaytaradi."""
    return run_full(tmp, name, change)[0]


def run_full(tmp, name, change=None, root=None):
    """(xatolar, ogohlantirishlar). root berilsa nusxa yozilmaydi."""
    if root is None:
        root = os.path.join(tmp, name)
        write(root, change)
    saved = check_docs.ROOT
    check_docs.ROOT = root
    del check_docs.errors[:]
    del check_docs.warnings[:]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            check_docs.main()
    finally:
        check_docs.ROOT = saved
    return list(check_docs.errors), list(check_docs.warnings)


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


def ratchet(tmp):
    saved = check_docs.README_LINK_BASE
    check_docs.README_LINK_BASE = 0
    try:
        errs = run(tmp, "ratchet", (CH1, "Matn.", "Qarang [sinov](../sinov/README.md)."))
    finally:
        check_docs.README_LINK_BASE = saved
    return any("README siga 1 havola, chegara 0" in e for e in errs)


def expect(change, needle):
    def case(tmp):
        # Papka nomi: needle dagi `:` va `/` Windows da nomga sig'maydi.
        errs = run(tmp, re.sub(r"\W", "_", needle[:20]), change)
        return any(needle in e for e in errs)
    return case


CH1 = "docs/sinov/01-birinchi.md"
CH2 = "docs/sinov/02-ikkinchi.md"
SKILL = ".claude/skills/sinov/SKILL.md"
TSV = "docs/review.tsv"
SOURCES = "- Band.\n\n## Manbalar\n\n- [Manba](https://example.org/a) - izoh\n"


def signed(holat="tekshirilgan", sources=1):
    """sinov 1 ni berilgan holatga izchil o'tkazadigan o'zgarishlar ro'yxati."""
    done, doing = (1, 0) if holat == "tekshirilgan" else (0, 1)
    line = review_status.status_line({"holat": holat, "sana": "2026-10-06"})
    return [
        (TSV, "sinov\t1\tai-draft\t\t\t0\t0\t",
         "sinov\t1\t%s\t2026-10-06\todam\t%d\t0\t" % (holat, sources)),
        (CH1, "> Holat: AI yozgan, inson tekshirmagan.", line),
        (CH1, "- Band.\n", SOURCES),
        ("README.md", status(2, 0, 0, "docs/review.tsv"),
         status(2, done, doing, "docs/review.tsv")),
        ("docs/sinov/README.md", status(2, 0, 0, "../review.tsv"),
         status(2, done, doing, "../review.tsv")),
    ]


def warned(change, needle):
    def case(tmp):
        _, warns = run_full(tmp, re.sub(r"\W", "_", "w_" + needle[:18]), change)
        return any(needle in w for w in warns)
    return case


def silent(change, needle):
    """Xato ham, `needle` li ogohlantirish ham yo'q."""
    def case(tmp):
        errs, warns = run_full(tmp, re.sub(r"\W", "_", "s_" + needle[:18]), change)
        return errs == [] and not any(needle in w for w in warns)
    return case


def no_owner_error(change, name):
    """Sarlavha o'zgarishi anchorni sindirishi mumkin: faqat uy-bob xatosi yo'qligi tekshiriladi."""
    def case(tmp):
        errs, _ = run_full(tmp, re.sub(r"\W", "_", "o_" + name[:18]), change)
        return not any("sarlavhasi" in e or "OWNERS.tsv" in e for e in errs)
    return case


def topic_heading(topic, pattern, heading, flagged):
    """OWNERS dagi mavzu `topic`, CH1 sarlavhasi `heading`: uy-bob xatosi bormi."""
    row = "%s\tsinov 2.1\tsinov uchun\t%s\n" % (topic, pattern)
    change = [("docs/OWNERS.tsv", "ikkinchi mavzu\tsinov 2.1\tsinov uchun\n", row),
              (CH1, "## 1.1 Mavzu", "## 1.1 " + heading)]
    if flagged:
        return expect(change, "'%s' sarlavhasi sinov 1.1" % topic)
    return no_owner_error(change, "%s %s" % (topic, heading))


def git(root, *args, author="Odam <odam@example.org>", body="sinov"):
    env = dict(os.environ, GIT_AUTHOR_NAME=author.split(" <")[0],
               GIT_AUTHOR_EMAIL=author.split("<")[1].rstrip(">"),
               GIT_COMMITTER_NAME="Sinov", GIT_COMMITTER_EMAIL="sinov@example.org")
    base = ["git", "-C", root, "-c", "commit.gpgsign=false"]
    if args == ("commit",):
        subprocess.run(base + ["add", "-A"], check=True, capture_output=True, env=env)
        args = ("commit", "-q", "-m", body)
    subprocess.run(base + list(args), check=True, capture_output=True, env=env)


def signoff(author, body="sinov"):
    """Odam ai-draft ni commit qiladi, keyin `author` tekshirilgan ga o'tkazadi."""
    def case(tmp):
        root = os.path.join(tmp, re.sub(r"\W", "_", "git_" + author[:12] + body[-8:]))
        write(root)
        git(root, "init", "-q")
        git(root, "commit")
        edit(root, signed())
        git(root, "commit", author=author, body=body)
        errs, _ = run_full(tmp, "", root=root)
        return [e for e in errs if "Claude muallifligida" in e]
    return case

BAD_CHAPTER = "Bu \u2014 em-dash va \u0416 kirill.\n"


def extra_file(tmp, name, rel, git_marker=None):
    """Toza nusxa yasaydi, `rel` ga buzuq md yozadi va (xatolar, ogohlantirishlar) qaytaradi."""
    root = os.path.join(tmp, name)
    write(root)
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(BAD_CHAPTER)
    if git_marker:
        with open(os.path.join(root, git_marker), "w", encoding="utf-8") as handle:
            handle.write("gitdir: /yo'q\n")
    return run_full(tmp, "", root=root)


def worktree_hidden(tmp):
    # Nazorat: shu fayl worktrees dan tashqarida xato beradi, ya'ni sinov
    # tekshiruvning o'zini ko'radi.
    seen, _ = extra_file(tmp, "wt_nazorat", "boshqa/x.md")
    hidden, _ = extra_file(tmp, "wt_yashirin", ".claude/worktrees/x/docs/sinov/01-birinchi.md")
    return any("em-dash" in e for e in seen) and hidden == []


def nested_repo_hidden(tmp):
    seen, _ = extra_file(tmp, "ir_nazorat", "ichki/x.md")
    hidden, _ = extra_file(tmp, "ir_yashirin", "ichki/x.md", git_marker="ichki/.git")
    return any("em-dash" in e for e in seen) and hidden == []


def skill_scan_hidden(tmp):
    import test_skill
    root = os.path.join(tmp, "skill_scan")
    for rel in (".claude/skills/a/SKILL.md", ".claude/worktrees/x/.claude/agents/b.md",
                ".claude/ichki/y.md"):
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write("x\n")
    os.makedirs(os.path.join(root, ".claude", "ichki", "repo"))
    open(os.path.join(root, ".claude", "ichki", "repo", ".git"), "w").write("gitdir: /yo'q\n")
    open(os.path.join(root, ".claude", "ichki", "repo", "z.md"), "w").write("x\n")
    saved = test_skill.ROOT
    test_skill.ROOT = root
    try:
        got = [os.path.relpath(p, root).replace(os.sep, "/") for p in test_skill.claude_md_files()]
    finally:
        test_skill.ROOT = saved
    return got == [".claude/ichki/y.md", ".claude/skills/a/SKILL.md"]


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
     expect((CH1, "```markdown", "```"), "01-birinchi.md:23: kod blokida til belgisi")),
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
     expect((CH1, "Matn.", "Matn xatoso'z bilan."), "01-birinchi.md:17")),
    # 8. `nasr` qamrovi: kod, inline kod, sarlavha va ichki havola emas.
    ("nasr naqshi nasrda tutiladi",
     expect((CH1, "Matn.", "Matn nasrxato bilan."), "01-birinchi.md:17: tuzatilgan")),
    ("nasr naqshi sarlavhada tutilmaydi",
     lambda tmp: run(tmp, "nasr_sarlavha", [
         (CH1, "## 1.1 Mavzu", "## 1.1 Mavzu nasrxato"),
         (CH1, "- [1.1 Mavzu](#11-mavzu)", "- [1.1 Mavzu nasrxato](#11-mavzu-nasrxato)"),
         (SKILL, "#11-mavzu", "#11-mavzu-nasrxato")]) == []),
    ("nasr naqshi inline kod va blokda tutilmaydi",
     lambda tmp: run(tmp, "nasr_kod", [
         (CH1, "Matn.", "Matn `nasrxato` bilan."),
         (CH1, "## Namuna sarlavha", "nasrxato\n## Namuna sarlavha")]) == []),
    ("nasr naqshi havola manzilida tutilmaydi",
     lambda tmp: run(tmp, "nasr_url",
                     (CH1, "Matn.", "Matn [manba](https://x.org/nasrxato).")) == []),
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
    # 10. Tekshiruv qat'iyligi.
    ("tekshirilmoqda bobi izchil bo'lsa xato yo'q",
     lambda tmp: run(tmp, "izchil", signed("tekshirilmoqda")) == []),
    ("tekshirilmoqda da sana bo'sh",
     expect(signed("tekshirilmoqda") + [(TSV, "2026-10-06\todam", "\todam")],
            "`sana` bo'sh")),
    ("tekshirilmoqda da tekshiruvchi bo'sh",
     expect(signed("tekshirilmoqda") + [(TSV, "2026-10-06\todam", "2026-10-06\t")],
            "`tekshiruvchi` bo'sh")),
    ("manbalar soni bobdagiga teng emas",
     expect(signed("tekshirilmoqda", sources=3),
            "manbalar=3, bobning `## Manbalar` ro'yxatida 1 ta")),
    ("tekshirilgan bobda Manbalar yo'q",
     expect(signed("tekshirilgan", sources=0)[:2] + signed()[3:],
            "kamida bitta birlamchi manba")),
    ("ai-draft da sana talab qilinmaydi",
     lambda tmp: run(tmp, "draft_bosh") == []),
    ("Manbalar da main ga bog'langan havola ogohlantiradi",
     warned(signed("tekshirilmoqda") + [
         (CH1, "https://example.org/a",
          "https://raw.githubusercontent.com/o/r/main/src/main/A.java")],
         "ko'chib yuradigan branchga")),
    ("Manbalar da tagga qadalgan havola jim",
     silent(signed("tekshirilmoqda") + [
         (CH1, "https://example.org/a",
          "https://raw.githubusercontent.com/o/r/v1.2.0/src/main/A.java")],
         "ko'chib yuradigan branchga")),
    ("tekshirilgan ni Claude commiti qo'ysa xato",
     lambda tmp: signoff("Claude <noreply@anthropic.com>")(tmp) != []),
    ("Co-Authored-By: Claude ham xato",
     lambda tmp: signoff("Odam <odam@example.org>",
                         "imzo\n\nCo-Authored-By: Claude Opus <noreply@anthropic.com>")(tmp) != []),
    ("tekshirilgan ni odam qo'ysa xato yo'q",
     lambda tmp: signoff("Odam <odam@example.org>")(tmp) == []),
    ("git yo'q joyda imzo tekshiruvi o'tkaziladi",
     lambda tmp: run(tmp, "gitsiz", signed()) == []),
    # README holat qatori.
    ("README da holat qatori yo'q",
     expect(("README.md", status(2, 0, 0, "docs/review.tsv"), ""), "README.md: holat qatori yo'q")),
    ("hujjat README sidagi holat review.tsv ga mos emas",
     expect(("docs/sinov/README.md", "2 bobdan 0 tasi", "2 bobdan 1 tasi"),
            "docs/sinov/README.md: holat qatori review.tsv ga mos emas")),
    # 12. Uy-bob: havola bo'lsa ogohlantirish yo'q.
    ("uy bo'limdan tashqari sarlavha xato beradi",
     expect((CH1, "## 1.1 Mavzu", "## 1.1 Ikkinchi mavzu"), "uy-bob sinov 2.1")),
    ("uy bo'limga havola bo'lsa jim",
     silent([(CH1, "## 1.1 Mavzu", "## 1.1 Ikkinchi mavzu"),
             (CH1, "- [1.1 Mavzu](#11-mavzu)", "- [1.1 Ikkinchi mavzu](#11-ikkinchi-mavzu)"),
             (SKILL, "#11-mavzu", "#11-ikkinchi-mavzu"),
             (CH1, "Matn.", "To'liq yozuv [ikkinchi mavzu](02-ikkinchi.md#21-mavzu) da.")],
            "uy-bob sinov 2.1")),
    ("boshqa bo'limga havola yetmaydi",
     expect([(CH1, "## 1.1 Mavzu", "## 1.1 Ikkinchi mavzu"),
             (CH1, "Matn.", "Qarang: [ikkinchi bob](02-ikkinchi.md#22-amalda-qollash).")],
            "uy-bob sinov 2.1")),
    ("shu bobdagi uy bo'limga `](#anchor)` havolasi ham yetadi",
     lambda tmp: not any("sinov 2.2 da" in w for w in run_full(tmp, "ozbob", [
         ("docs/OWNERS.tsv", "ikkinchi mavzu\tsinov 2.1", "amalda\tsinov 2.1"),
         (CH2, "- Band.\n", "- Band. To'liq yozuv [mavzu](#21-mavzu) da.\n")])[0])),
    ("naqsh ustuni sarlavhadagi o'zbekcha shaklni tutadi",
     expect([("docs/OWNERS.tsv", "sinov uchun\n", "sinov uchun\tqiziq mavzu[a-z']*\n"),
             (CH1, "## 1.1 Mavzu", "## 1.1 Qiziq mavzularga kirish")],
            "'ikkinchi mavzu' sarlavhasi sinov 1.1")),
    ("naqshsiz o'zbekcha shakl mavzu nomiga mos kelmaydi",
     no_owner_error((CH1, "## 1.1 Mavzu", "## 1.1 Qiziq mavzularga kirish"), "naqshsiz")),
    ("sozlama kaliti (nuqtadan keyingi bo'lak) mavzu emas",
     no_owner_error([("docs/OWNERS.tsv", "sinov uchun\n", "sinov uchun\tqiziq\n"),
                     (CH1, "## 1.1 Mavzu", "## 1.1 Kalit app.qiziq sozlamasi")], "nuqta")),
    ("uy bo'limning o'zida mavzu sarlavhasi xato bermaydi",
     no_owner_error((CH2, "## 2.1 Mavzu", "## 2.1 Ikkinchi mavzu"), "uyning ozi")),
    ("imlo naqshi `claude` qamrovi bilan .claude matnini ham tutadi",
     expect([("tools/known_errors.tsv", "sinov uchun naqsh\tdocs", "sinov uchun naqsh\tdocs,claude,nasr"),
             (SKILL, "| Mavzu | Bo'lim |", "xatoso'z\n\n| Mavzu | Bo'lim |")],
            "tuzatilgan xato qaytdi -> xatoso'z")),
    ("sozlama kaliti `a.b.c` mavzu emas",
     topic_heading("testcontainers", "testcontainers?",
                   "`testcontainers.reuse.enable` sozlamasi", False)),
    ("defisli artifact nomi mavzu emas",
     topic_heading("testcontainers", "testcontainers?", "spring-boot-testcontainers", False)),
    ("nuqtadan keyingi bo'lak mavzu emas",
     topic_heading("idempotency", "idempoten[a-z']*", "idempotency.key sozlamasi", False)),
    ("naqshdagi defisli shakl mavzuning o'zi",
     topic_heading("circuit breaker", "circuit[ -]?breaker",
                   "Resilience4j circuit-breaker sozlamasi", True)),
    ("`@Testcontainers` annotatsiyasi mavzuning API si",
     topic_heading("testcontainers", "testcontainers?", "@Testcontainers annotatsiyasi", True)),
    ("umumiy `Sahifa n + 1` n+1 naqshini tutmaydi",
     topic_heading("n+1", "n\\+1|n ?\\+ ?1 (so'rov|muammo|problem|query)[a-z']*",
                   "Sahifa n + 1", False)),
    ("`N+1 muammosi` n+1 naqshini tutadi",
     topic_heading("n+1", "n\\+1|n ?\\+ ?1 (so'rov|muammo|problem|query)[a-z']*",
                   "N+1 muammosi", True)),
    ("`.claude/worktrees` ichidagi nusxa skanerlanmaydi", worktree_hidden),
    ("ichki repo (o'z .git i bor papka) skanerlanmaydi", nested_repo_hidden),
    ("test_skill `.claude/worktrees` ni o'tkazib yuboradi", skill_scan_hidden),
    # 13. README havola ratchet.
    ("README havolasi bazaviydan oshsa xato", ratchet),
    # 14. Summary.
    ("summary yo'q bo'lsa xato",
     expect((CH1, "<summary>Bu bobdagi 2 bo'lim</summary>", "<summary>Bu bo'limdagi 2 bo'lim</summary>"),
            "01-birinchi.md: `<summary>Bu bobdagi N bo'lim</summary>` yo'q")),
    ("summary soni noto'g'ri",
     expect((CH1, "Bu bobdagi 2 bo'lim", "Bu bobdagi 5 bo'lim"), "<summary> da 5 bo'lim")),
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
