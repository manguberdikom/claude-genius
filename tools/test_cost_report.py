#!/usr/bin/env python3
"""cost_report.py uchun sinovlar.

    python3 tools/test_cost_report.py

Eng muhimi til aniqlash. Nisbat tilga qarab tanlanadi: o'zbekcha matn
inglizcha nisbat bilan sanalsa ~1.5 baravar kam chiqadi va byudjet jim
oshib ketadi. Shuning uchun haqiqiy fayllarning tili tekshiriladi.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "cost_report.py")
sys.path.insert(0, HERE)

import cost_report  # noqa: E402
import suggest_sections  # noqa: E402

SKILLS = os.path.join(ROOT, ".claude", "skills")
AGENTS = os.path.join(ROOT, ".claude", "agents")


def run(*args):
    proc = subprocess.run([sys.executable, TOOL] + list(args),
                          capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


def description(path):
    match = cost_report.FRONT_RE.match(cost_report.read(path))
    return dict(cost_report.FIELD_RE.findall(match.group(1)))["description"]


def case_skill_tavsiflari_inglizcha(_):
    """Marshrut skilllari tavsifi inglizcha: trigger inglizcha promptga ham
    tushsin. Soni faqat bo'sh ro'yxatdan yolg'on yashil chiqmasligi uchun."""
    names = [d for d in sorted(os.listdir(SKILLS))
             if os.path.exists(os.path.join(SKILLS, d, "SKILL.md"))
             and d != "manguberdi"]
    return len(names) >= 7 and all(
        cost_report.lang_of(description(os.path.join(SKILLS, d, "SKILL.md")))
        == "en" for d in names)


def case_ozbekcha_matnlar(_):
    paths = [os.path.join(SKILLS, "manguberdi", "SKILL.md")]
    paths += [os.path.join(AGENTS, f) for f in sorted(os.listdir(AGENTS))
              if f.endswith(".md")]
    if len(paths) < 7:
        return False
    texts = [description(p) for p in paths]
    texts.append(cost_report.read(os.path.join(ROOT, "CLAUDE.md")))
    return all(cost_report.lang_of(t) == "uz" for t in texts)


def case_royxat_qatori(tmp):
    """Skill `- nom: tavsif`, agent tools bilan; model sanalmaydi."""
    root = os.path.join(tmp, "qator")
    os.makedirs(os.path.join(root, ".claude", "skills", "sinov"))
    os.makedirs(os.path.join(root, ".claude", "agents"))
    with open(os.path.join(root, ".claude", "skills", "sinov", "SKILL.md"),
              "w", encoding="utf-8") as handle:
        handle.write("---\nname: sinov\ndescription: Use it when testing.\n"
                     "---\n\n# Tana sanalmaydi\n")
    with open(os.path.join(root, ".claude", "agents", "yordamchi.md"),
              "w", encoding="utf-8") as handle:
        handle.write("---\nname: yordamchi\ndescription: Kodni o'qiydi.\n"
                     "tools: Bash, Read\nmodel: haiku\n---\n\nTana.\n")
    with open(os.path.join(root, ".claude", "agents", "toolsiz.md"),
              "w", encoding="utf-8") as handle:
        handle.write("---\ndescription: Hammasini qiladi.\nmodel: opus\n---\n")
    old = cost_report.ROOT
    cost_report.ROOT = root
    try:
        rows = {r[0]: r for r in cost_report.collect()}
    finally:
        cost_report.ROOT = old
    skill = "- sinov: Use it when testing.\n"
    agents = ("- toolsiz: Hammasini qiladi. (Tools: *)\n"
              "- yordamchi: Kodni o'qiydi. (Tools: Bash, Read)\n")
    return (rows["1 skill qatori"][1] == len(skill)
            and rows["2 agent qatori"][1] == len(agents)
            and "CLAUDE.md" not in rows)


def taklif_row(root):
    old = cost_report.ROOT
    cost_report.ROOT = root
    try:
        rows = {r[0]: r for r in cost_report.collect()}
    finally:
        cost_report.ROOT = old
    return rows["taklif hooki (eng ko'pi)"]


def write_tsv(path, header, rows):
    with open(path, "w", encoding="utf-8") as handle:
        for row in [header] + rows:
            handle.write("\t".join(row) + "\n")


def case_taklif_indekssiz(tmp):
    """Indeks yo'q: sarlavha 55 + har qator 150 belgi."""
    root = os.path.join(tmp, "taklif_bosh")
    os.makedirs(os.path.join(root, "tools"))
    with open(os.path.join(root, "tools", "suggest_sections.py"), "w",
              encoding="utf-8") as handle:
        handle.write("MAX_SUGGESTIONS = 3\n")
    return taklif_row(root)[1] == 55 + 3 * 150


def case_taklif_eng_uzun(tmp):
    """Indeks bor: hookning render() i eng uzun sarlavhalar bilan, bob ham."""
    root = os.path.join(tmp, "taklif_indeks")
    os.makedirs(os.path.join(root, "tools"))
    os.makedirs(os.path.join(root, "index"))
    shutil.copy(os.path.join(HERE, "suggest_sections.py"),
                os.path.join(root, "tools"))
    sections = [("patterns", "1.%d" % n, "1.%d %s" % (n, "x" * n * 10))
                for n in range(1, 7)]
    write_tsv(os.path.join(root, "index", "sections.tsv"),
              ("doc", "section", "chapter", "title"),
              [(d, s, "1", t) for d, s, t in sections])
    chapter = ("testing", "2", "2. " + "y" * 200)
    write_tsv(os.path.join(root, "index", "chapters.tsv"),
              ("doc", "chapter", "title"), [chapter])
    count = suggest_sections.MAX_SUGGESTIONS
    longest = [chapter] + sections[::-1][:count - 1]
    expected = suggest_sections.render([h + (0,) for h in longest])
    return taklif_row(root)[1] == len(expected)


def case_budget_qiymatsiz(_):
    code, _ = run("--budget")
    return code == 2


def case_budget_oshdi(_):
    code, out = run("--budget", "1")
    return code == 1 and "OSHIB KETDI" in out


def case_argumentsiz(_):
    code, out = run()
    return code == 0 and "Joyida" in out


def case_memory_papka_nomiga_bogliq_emas(tmp):
    """Klon boshqa nomli papkada (ZIP dan claude-genius-main): ikki indeks.

    Slug avval papka nomidan olinardi va proyekt indeksi sanalmasdi.
    """
    root = os.path.join(tmp, "claude-genius-main")
    for slug in ("umumiy", "claude-genius"):
        os.makedirs(os.path.join(root, "memory", slug))
        with open(os.path.join(root, "memory", slug, "MEMORY.md"), "w",
                  encoding="utf-8") as handle:
            handle.write("# %s\n" % slug)
    old = cost_report.ROOT
    cost_report.ROOT = root
    try:
        return len(cost_report.memory_indexes()) == 2
    finally:
        cost_report.ROOT = old


CASES = [
    ("marshrut skilllari tavsifi inglizcha", case_skill_tavsiflari_inglizcha),
    ("manguberdi, agentlar va CLAUDE.md o'zbekcha", case_ozbekcha_matnlar),
    ("ro'yxat qatori nom va tools bilan", case_royxat_qatori),
    ("taklif hooki indekssiz taxmin", case_taklif_indekssiz),
    ("taklif hooki eng uzun sarlavhalar bilan", case_taklif_eng_uzun),
    ("--budget qiymatsiz rc 2", case_budget_qiymatsiz),
    ("--budget 1 oshib ketadi", case_budget_oshdi),
    ("argumentsiz byudjet ichida", case_argumentsiz),
    ("memory indeksi papka nomiga bog'liq emas", case_memory_papka_nomiga_bogliq_emas),
]


def main():
    tmp = tempfile.mkdtemp(prefix="cost_report_")
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
