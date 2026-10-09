#!/usr/bin/env python3
"""Ish tugagach qoldiqlarni tozalaydi: yetim worktree, branch va tugagan hujjat.

    python3 tools/tozala.py            # tozalaydi
    python3 tools/tozala.py --quruq    # hech narsa o'chirmay ro'yxat beradi
    python3 tools/tozala.py --ildiz <papka>

Nima o'chadi:

1. `<repo>/.claude/worktrees/` dagi, `git worktree list` da RO'YXATDA YO'Q
   papkalar. Ro'yxatdagi worktree faol guruh: unga tegilmaydi. Windows da
   uzun yo'l uchun `\\\\?\\` prefiksi, read-only fayl uchun chmod. Papka
   bo'shasa `worktrees` o'zi ham o'chadi.
2. Worktree si yo'q lokal `genius/*` branchlar (`git branch -D`), boshqa
   branchga tegilmaydi.
3. Hujjatlar papkasidagi (`docref.docs_dir`) tugagan hujjatlar: faylning
   birinchi 10 qatorida `holat: tugadi` (yoki `status: done`) bo'lsa.
   Tugamagan hujjatga tegilmaydi; papka bo'shab qolsa u ham o'chadi.

Nima O'CHMAYDI, faqat aytiladi: repoda git ga qo'shilgan hujjat yoki
asbob fayllari (`*.md`, `.claude/`, `.idea/`, `*.http`, `adr/`, `docs/`).
Ularni olib tashlash commit talab qiladi, buni foydalanuvchi hal qiladi.
Genius klonining o'zida (hujjat uning mahsuloti) bu ro'yxat chiqmaydi.

Git ro'yxati olinmasa (git yo'q yoki worktree list yiqildi) worktree va
branch tozalanmaydi: faol guruhni noto'g'ri o'chirishdan ko'ra qoldirish
yaxshi. Chiqish kodi har doim 0, xato bo'lsa sabab matnda.
"""

import argparse
import os
import re
import shutil
import stat
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import docref  # noqa: E402
import geniuslib  # noqa: E402

BRANCH_PREFIX = "genius/"
HEAD_LINES = 10
DONE_RE = re.compile(
    r"^[\s>*#_-]*(?:holat|status)[\s*_]*:[\s*_]*(?:tugadi|done)\b", re.IGNORECASE)
# Repoda bo'lmasligi kerak bo'lgan hujjat va asbob fayllari (git ls-files yo'li).
EXTRA_RE = re.compile(
    r"(?:^|/)(?:\.claude|\.idea|adr|docs)/|\.md$|\.http$", re.IGNORECASE)
# Kodga tegishli resurs: test yoki ilova resursi ichidagi .md/.http hujjat emas.
RESOURCE_RE = re.compile(r"(?:^|/)src/(?:main|test)/resources/")
SHOW = 6


def git(root, *args):
    """git chiqishi (str) yoki None: git yo'q yoki chiqish kodi 0 emas."""
    proc = geniuslib.run_git(list(args), cwd=root)
    return proc.stdout if proc is not None and proc.returncode == 0 else None


def main_root(path):
    """Asosiy repo ildizi: guruh worktree sidan ham asosiy repoga chiqadi."""
    top = git(path, "rev-parse", "--show-toplevel")
    if top is None:
        return None
    common = git(path, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if common and os.path.basename(os.path.normpath(common.strip())) == ".git":
        return os.path.dirname(os.path.normpath(common.strip()))
    return os.path.normpath(top.strip())


def norm(path):
    """Taqqoslash uchun yo'l: realpath, kichik harf (Windows), `\\\\?\\`siz."""
    path = os.path.realpath(path)
    if path.startswith("\\\\?\\"):
        path = path[4:]
    return os.path.normcase(path)


def listed_worktrees(root):
    """(yo'llar to'plami, ularda checkout qilingan branchlar) yoki None."""
    out = git(root, "worktree", "list", "--porcelain")
    if out is None:
        return None
    paths, branches = set(), set()
    for line in out.splitlines():
        if line.startswith("worktree "):
            paths.add(norm(line[9:].strip()))
        elif line.startswith("branch "):
            branches.add(line[7:].strip().replace("refs/heads/", "", 1))
    return paths, branches


def long_path(path):
    """Windows da 260 belgidan uzun yo'l uchun `\\\\?\\` prefiksi."""
    path = os.path.abspath(path)
    if os.name == "nt" and not path.startswith("\\\\?\\"):
        return "\\\\" + "?" + "\\" + path
    return path


def writable_retry(func, path, _error):
    """rmtree xatosi: read-only faylni yoziladigan qilib qayta urinadi."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path):
    target = long_path(path)
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(target)
    elif sys.version_info >= (3, 12):
        shutil.rmtree(target, onexc=writable_retry)
    else:
        shutil.rmtree(target, onerror=writable_retry)


def orphan_worktrees(root, listed):
    """`.claude/worktrees/` ostidagi, git ro'yxatida yo'q papkalar."""
    base = os.path.join(root, ".claude", "worktrees")
    try:
        names = sorted(os.listdir(base))
    except OSError:
        return base, []
    return base, [n for n in names if norm(os.path.join(base, n)) not in listed]


def clean_worktrees(root, listed, dry):
    base, orphans = orphan_worktrees(root, listed[0])
    failed = []
    if not dry:
        for name in orphans:
            try:
                remove_tree(os.path.join(base, name))
            except OSError as exc:
                failed.append("%s (%s)" % (name, exc.__class__.__name__))
        if os.path.isdir(base) and not os.listdir(base):
            os.rmdir(base)
        git(root, "worktree", "prune")
    return [n for n in orphans if not any(f.startswith(n + " ") for f in failed)], failed


def clean_branches(root, listed, dry):
    out = git(root, "for-each-ref", "--format=%(refname:short)", "refs/heads/" + BRANCH_PREFIX)
    names = [n.strip() for n in (out or "").splitlines() if n.strip()]
    stale = [n for n in names if n.startswith(BRANCH_PREFIX) and n not in listed[1]]
    done = []
    for name in stale:
        if dry or git(root, "branch", "-D", name) is not None:
            done.append(name)
    return done


def is_done(path):
    """Birinchi 10 qatorda `holat: tugadi` yoki `status: done`."""
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for _, line in zip(range(HEAD_LINES), handle):
                if DONE_RE.match(line):
                    return True
    except OSError:
        pass
    return False


def clean_docs(docs, dry):
    """(o'chgan fayllar, o'chgan papkalar). Tugamagan hujjat joyida qoladi."""
    files, folders = [], []
    if not os.path.isdir(docs):
        return files, folders
    for here, _dirs, names in os.walk(docs):
        for name in sorted(names):
            path = os.path.join(here, name)
            if is_done(path):
                files.append(os.path.relpath(path, docs).replace(os.sep, "/"))
                if not dry:
                    os.chmod(path, stat.S_IWRITE)
                    os.remove(path)
    if dry:
        return files, folders
    for here, _dirs, _names in os.walk(docs, topdown=False):
        if not os.listdir(here):
            os.rmdir(here)
            folders.append(os.path.relpath(here, docs).replace(os.sep, "/"))
    return files, folders


def extra_in_git(root):
    """Git ga qo'shilgan hujjat va asbob fayllari; genius klonida bo'sh."""
    if docref.is_clone_project(root):
        return []
    out = git(root, "ls-files") or ""
    return [p for p in out.splitlines()
            if EXTRA_RE.search(p) and not RESOURCE_RE.search(p)]


def brief(items):
    """Qisqa ro'yxat: birinchi SHOW tasi, qolgani soni bilan."""
    text = ", ".join(items[:SHOW])
    return text + (" ... +%d" % (len(items) - SHOW) if len(items) > SHOW else "")


def run(root, dry):
    """Tozalaydi va chiqish qatorlarini qaytaradi."""
    lines, counts = [], {}
    verb = "o'chadi" if dry else "o'chdi"
    listed = listed_worktrees(root)
    if listed is None:
        lines.append("git worktree ro'yxati olinmadi: worktree va branch tegilmadi")
    else:
        gone, failed = clean_worktrees(root, listed, dry)
        counts["worktree"] = len(gone)
        if gone:
            lines.append("worktree %s: %s" % (verb, brief(gone)))
        if failed:
            lines.append("worktree o'chmadi: %s" % brief(failed))
        branches = clean_branches(root, listed, dry)
        counts["branch"] = len(branches)
        if branches:
            lines.append("branch %s: %s" % (verb, brief(branches)))
    docs = docref.docs_dir(root)
    files, folders = clean_docs(docs, dry)
    counts["hujjat"] = len(files)
    if files:
        lines.append("hujjat %s (%s): %s" % (verb, docs.replace(os.sep, "/"), brief(files)))
    if folders:
        lines.append("bo'sh papka %s: %d ta" % (verb, len(folders)))
    extra = extra_in_git(root)
    counts["git da ortiqcha"] = len(extra)
    if extra:
        lines.append("git da ortiqcha: %s" % brief(extra))
        lines.append("  (o'chirilmadi: commit talab qiladi, foydalanuvchi hal qiladi)")
    total = ", ".join("%s %d" % (k, v) for k, v in counts.items())
    lines.append("tozala%s: %s" % (" (quruq)" if dry else "", total or "git yo'q"))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description="Yetim worktree, branch va tugagan hujjat.")
    parser.add_argument("--quruq", action="store_true", help="hech narsa o'chirmay ro'yxat")
    parser.add_argument("--ildiz", default=os.getcwd(), help="repo papkasi (sukut joriy)")
    args = parser.parse_args(argv)
    root = main_root(args.ildiz)
    if root is None:
        print("tozala: git repo emas: %s" % args.ildiz)
        return 0
    print("\n".join(run(root, args.quruq)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
