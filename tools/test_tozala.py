#!/usr/bin/env python3
"""tozala.py uchun sinovlar.

    python3 tools/test_tozala.py [-k matn]

Hammasi vaqtinchalik repoda: jonli repo, branch va hujjatlar papkasiga
tegilmaydi. Hujjatlar papkasi `GENIUS_DOCS_DIR` bilan temp ichiga qo'yiladi.
Sinaladi: yetim worktree papkasi o'chadi, ro'yxatdagi (faol) qoladi, read-only
fayl to'siq emas; worktree siz `genius/*` branch o'chadi, boshqa branch va
worktree li `genius/*` qoladi; tugagan hujjat o'chadi, tugamagani va 10
qatordan keyingi belgi qoladi; git ga qo'shilgan hujjat faqat aytiladi;
`--quruq` hech narsa o'chirmaydi.
"""

import contextlib
import os
import shutil
import stat
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "tozala.py")
sys.path.insert(0, HERE)
import testkit  # noqa: E402

IDENT = ["-c", "user.email=t@t", "-c", "user.name=t", "-c", "commit.gpgsign=false"]


def git(cwd, *args):
    return subprocess.run(["git"] + IDENT + ["-C", cwd] + list(args),
                          capture_output=True, text=True)


def write(path, text="x\n"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


@contextlib.contextmanager
def project(tracked=("src/Main.java",)):
    """(root, docs): git repo `<tmp>/ws/app`, hujjatlar `<tmp>/docs/app`."""
    tmp = tempfile.mkdtemp(prefix="tozala_")
    root = os.path.join(tmp, "ws", "app")
    os.makedirs(root)
    git(root, "init", "-q", "-b", "dev")
    for rel in tracked:
        write(os.path.join(root, rel))
    git(root, "add", "-A")
    git(root, "commit", "-qm", "init")
    docs = os.path.join(tmp, "docs", "app")
    try:
        yield root, docs
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def tozala(root, docs, *args):
    """CLI ni yurgizadi; hujjatlar papkasi `docs` (GENIUS_DOCS_DIR/app)."""
    env = dict(os.environ, GENIUS_DOCS_DIR=os.path.dirname(docs))
    env.pop("GENIUS_CLONE", None)
    proc = subprocess.run([sys.executable, TOOL, "--ildiz", root] + list(args),
                          capture_output=True, text=True, encoding="utf-8", env=env)
    return proc.returncode, proc.stdout + proc.stderr


def worktree(root, name):
    path = os.path.join(root, ".claude", "worktrees", name)
    git(root, "worktree", "add", "-q", "-b", "genius/" + name, path)
    return path


def branches(root):
    return git(root, "branch", "--format=%(refname:short)").stdout.split()


def orphan(root, name, readonly=False):
    path = os.path.join(root, ".claude", "worktrees", name)
    write(os.path.join(path, "deep", "f.txt"))
    if readonly:
        os.chmod(os.path.join(path, "deep", "f.txt"), stat.S_IREAD)
    return path


def case_orphan_worktree():
    with project() as (root, docs):
        live = worktree(root, "live")
        dead = orphan(root, "dead", readonly=True)
        code, out = tozala(root, docs)
        return [("yetim papka o'chdi, read-only to'siq emas", not os.path.exists(dead)),
                ("ro'yxatdagi worktree qoldi", os.path.isdir(live)),
                ("worktrees papkasi qoldi (bo'sh emas)",
                 os.path.isdir(os.path.dirname(live))),
                ("chiqish dead ni aytadi", code == 0 and "dead" in out)]


def case_empty_worktrees_removed():
    with project() as (root, docs):
        orphan(root, "dead")
        tozala(root, docs)
        return [("bo'shagan worktrees o'zi ham o'chdi",
                 not os.path.exists(os.path.join(root, ".claude", "worktrees")))]


def case_branches():
    with project() as (root, docs):
        worktree(root, "live")
        git(root, "branch", "genius/stale")
        git(root, "branch", "feature/x")
        tozala(root, docs)
        have = branches(root)
        return [("worktree siz genius/* o'chdi", "genius/stale" not in have),
                ("worktree li genius/* qoldi", "genius/live" in have),
                ("boshqa prefiksli branch qoldi", "feature/x" in have and "dev" in have)]


def case_docs():
    with project() as (root, docs):
        write(os.path.join(docs, "REJA.md"), "# Reja: a\n\nHolat: tugadi\n")
        write(os.path.join(docs, "reja", "b-reja.md"), "# Reja: b\nstatus: done\n")
        write(os.path.join(docs, "reja", "c-reja.md"), "# Reja: c\nHolat: ishda\n")
        write(os.path.join(docs, "late.md"), "\n" * 12 + "Holat: tugadi\n")
        write(os.path.join(docs, "old", "d.md"), "Holat: tugadi\n")
        code, out = tozala(root, docs)
        return [("tugagan REJA.md o'chdi", not os.path.exists(os.path.join(docs, "REJA.md"))),
                ("status: done o'chdi",
                 not os.path.exists(os.path.join(docs, "reja", "b-reja.md"))),
                ("ishda hujjat qoldi", os.path.isfile(os.path.join(docs, "reja", "c-reja.md"))),
                ("10 qatordan keyingi belgi hisobga olinmaydi",
                 os.path.isfile(os.path.join(docs, "late.md"))),
                ("bo'shagan papka o'chdi", not os.path.exists(os.path.join(docs, "old"))),
                ("chiqish hujjat sonini aytadi", code == 0 and "hujjat 3" in out)]


def case_docs_all_done_folder_removed():
    with project() as (root, docs):
        write(os.path.join(docs, "REJA.md"), "Holat: tugadi\n")
        tozala(root, docs)
        return [("hammasi tugagan: repo papkasi o'chdi", not os.path.exists(docs))]


def case_git_extra_only_listed():
    tracked = ("src/Main.java", "REJA.md", "docs/a.md", ".claude/x.json", "api.http",
               "src/test/resources/note.md")
    with project(tracked) as (root, docs):
        code, out = tozala(root, docs)
        kept = all(os.path.isfile(os.path.join(root, rel)) for rel in tracked)
        return [("git dagi fayllar o'chmadi", kept),
                ("ro'yxat chiqdi", "git da ortiqcha" in out and "REJA.md" in out
                 and "docs/a.md" in out and ".claude/x.json" in out and "api.http" in out),
                ("test resursi ro'yxatda emas", "note.md" not in out),
                ("kod fayli ro'yxatda emas", "Main.java" not in out)]


def case_dry_run():
    with project() as (root, docs):
        dead = orphan(root, "dead")
        git(root, "branch", "genius/stale")
        write(os.path.join(docs, "REJA.md"), "Holat: tugadi\n")
        code, out = tozala(root, docs, "--quruq")
        return [("--quruq: papka joyida", os.path.isdir(dead)),
                ("--quruq: branch joyida", "genius/stale" in branches(root)),
                ("--quruq: hujjat joyida", os.path.isfile(os.path.join(docs, "REJA.md"))),
                ("--quruq: ro'yxat va yig'ma qator",
                 code == 0 and "dead" in out and "genius/stale" in out
                 and "tozala (quruq)" in out)]


def case_summary_line():
    with project() as (root, docs):
        orphan(root, "dead")
        git(root, "branch", "genius/stale")
        write(os.path.join(docs, "REJA.md"), "Holat: tugadi\n")
        _, out = tozala(root, docs)
        last = out.strip().splitlines()[-1]
        return [("yig'ma qator oxirida", last.startswith("tozala:")
                 and "worktree 1" in last and "branch 1" in last and "hujjat 1" in last)]


def case_not_git():
    tmp = tempfile.mkdtemp(prefix="tozala_nogit_")
    try:
        code, out = tozala(tmp, os.path.join(tmp, "d", "app"))
        return [("git emas: rc=0 va sabab", code == 0 and "git repo emas" in out)]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


CASES = [
    ("yetim worktree papkasi", case_orphan_worktree),
    ("bo'shagan worktrees o'chadi", case_empty_worktrees_removed),
    ("genius/* branchlar", case_branches),
    ("tugagan hujjatlar", case_docs),
    ("hammasi tugagan: papka o'chadi", case_docs_all_done_folder_removed),
    ("git dagi ortiqcha faqat aytiladi", case_git_extra_only_listed),
    ("--quruq", case_dry_run),
    ("yig'ma qator", case_summary_line),
    ("git repo emas", case_not_git),
]


def main():
    return testkit.run_cases(CASES, sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
