"""Sinov fayllari uchun umumiy runner va jarayon ichidagi chaqiruv.

    python3 tools/test_guard.py -k docker       # faqat nomida "docker" bor holatlar
    python3 tools/test_guard.py --vaqt          # 200 ms dan uzun holatlar
    python3 tools/test_budget.py --vaqt 50      # chegara ms da

Har suite o'z `CASES` ro'yxatini `run_cases(CASES, sys.argv[1:])` ga
beradi. Holat `(nom, funksiya)` juftligi, funksiya argumentsiz chaqiriladi
va quyidagilardan birini qaytaradi:

- `bool`: bitta qator, matni holat nomi;
- `[(matn, ok), ...]`: bir nechta qator, har biri alohida sanaladi.

Holat istisno bersa u bitta XATO qator bo'ladi: qolgan holatlar yuradi.

`call_main` hook yoki CLI ning `main()` funksiyasini jarayon ichida
yurgizadi. Python jarayonini ishga tushirish bitta chaqiruvdan 20-40
barobar qimmat, shuning uchun holatlarning asosiy qismi shu yo'l bilan
yuradi, subprocess faqat jarayon chegarasini sinaydigan E2E holatlarda.
Faqat standart kutubxona: Windows CI ham shu faylni ishlatadi.
"""

import argparse
import collections
import contextlib
import io
import os
import shutil
import subprocess
import sys
import time

SLOW_MS = 200

# Sinov jonli sessiyaning global sozlamasidan (settings.json env) xoli:
# GENIUS_CLONE tashqaridan kirsa memory va holat yo'llari klonga qarab
# ketardi (tools/geniuslib.py clone_root). Kerak bo'lgan sinov uni o'zi beradi.
os.environ.pop("GENIUS_CLONE", None)

Result = collections.namedtuple("Result", "returncode stdout stderr")


def call_main(main, stdin=b"", argv=None, cwd=None, env=None):
    """`main()` ni jarayon ichida yurgizadi: Result(returncode, stdout, stderr).

    stdin baytlar (yoki UTF-8 ga o'giriladigan matn): hookio.read_text
    avval `.buffer` ni o'qiydi, shuning uchun StringIO emas, TextIOWrapper.
    `env` qiymati None bo'lsa o'zgaruvchi o'chiriladi. argv, cwd, muhit va
    oqimlar `finally` da tiklanadi; SystemExit chiqish kodiga aylanadi.
    """
    raw = stdin.encode("utf-8") if isinstance(stdin, str) else stdin
    env = env or {}
    saved_env = {key: os.environ.get(key) for key in env}
    saved = (sys.stdin, sys.argv, os.getcwd())
    out, err = io.StringIO(), io.StringIO()
    try:
        sys.stdin = io.TextIOWrapper(io.BytesIO(raw), encoding="utf-8")
        if argv is not None:
            sys.argv = list(argv)
        if cwd:
            os.chdir(cwd)
        for key, value in env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = main()
            except SystemExit as exc:
                code = exc.code
    finally:
        sys.stdin, sys.argv = saved[0], saved[1]
        os.chdir(saved[2])
        for key, value in saved_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    if code is None:
        code = 0
    elif not isinstance(code, int):
        err.write("%s\n" % code)   # sys.exit("matn") kabi
        code = 1
    return Result(code, out.getvalue(), err.getvalue())


def _options(argv):
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0] or "test"),
        description="Sinov holatlarini yurgizadi.")
    parser.add_argument("-k", dest="keys", action="append", default=[],
                        metavar="MATN",
                        help="faqat nomida shu matn bor holatlar (registrsiz, "
                             "bir necha marta berilsa istalgani)")
    parser.add_argument("--vaqt", nargs="?", type=float, const=SLOW_MS,
                        metavar="MS",
                        help="oxirida shundan uzun holatlar (standart %d ms)"
                             % SLOW_MS)
    return parser.parse_args(argv)


def _rows(result, name):
    if isinstance(result, bool):
        return [(result, name)]
    if isinstance(result, list):
        return [(bool(ok), label) for label, ok in result]
    raise TypeError("holat bool yoki [(matn, ok)] qaytarishi kerak: %r"
                    % (result,))


def run_cases(cases, argv=(), headers=False):
    """Holatlarni yurgizadi, natijani chop etadi va chiqish kodini qaytaradi.

    `headers` bo'lsa har holat oldidan `== nom ==` sarlavhasi: bir holat
    bir nechta qatorli bo'lim bo'lganda.
    """
    opts = _options(list(argv))
    keys = [k.lower() for k in opts.keys]
    chosen = [(name, fn) for name, fn in cases
              if not keys or any(k in name.lower() for k in keys)]
    if not chosen:
        print("mos holat yo'q: -k %s" % " ".join(opts.keys))
        return 1

    total = failures = 0
    timings = []
    for index, (name, fn) in enumerate(chosen):
        if headers:
            print("%s== %s ==" % ("\n" if index else "", name))
        start = time.perf_counter()
        try:
            rows = _rows(fn(), name)
        except Exception as exc:  # noqa: BLE001 - bitta holat suiteni to'xtatmaydi
            rows = [(False, "%s (%s: %s)" % (name, type(exc).__name__, exc))]
        timings.append(((time.perf_counter() - start) * 1000, name))
        for ok, label in rows:
            total += 1
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", label))

    if opts.vaqt is not None:
        slow = sorted((t for t in timings if t[0] >= opts.vaqt), reverse=True)
        print("\n%d ms dan uzun holatlar: %d" % (opts.vaqt, len(slow)))
        for ms, name in slow:
            print("%8.0f ms  %s" % (ms, name))
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


# --- git fixture: vaqtinchalik repo, bare origin va klonlar ----------------
#
# Global o'rnatish snapshotni `git worktree add` bilan yasaydi (R7.8 XV-Y1),
# shuning uchun uni sinash uchun haqiqiy git repo kerak. Sinov reponing o'ziga
# (uning .git/worktrees iga) tegmaydi: ishchi daraxtning nusxasi vaqtinchalik
# papkada alohida repo bo'ladi.

REPO_IGNORE = shutil.ignore_patterns(
    ".git", "index", "dist", "worktrees", "__pycache__", ".state", "usage", "audit")


def git(cwd, *args):
    """`git <args>` ni cwd da yurgizadi: stdout (bo'sh joysiz). Xatoda RuntimeError.

    Shaxsiy sozlama (imzo, hook) ta'sir qilmasligi uchun o'zgaruvchilar va -c
    bayroqlari aniq beriladi."""
    env = dict(os.environ, GIT_AUTHOR_NAME="sinov", GIT_AUTHOR_EMAIL="sinov@example.com",
               GIT_COMMITTER_NAME="sinov", GIT_COMMITTER_EMAIL="sinov@example.com",
               GIT_TERMINAL_PROMPT="0")
    proc = subprocess.run(
        ["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=" + os.devnull,
         "-c", "protocol.file.allow=always"] + list(args),
        cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), proc.stdout.strip()))
    return proc.stdout.strip()


def repo_nusxa(src_root, dst):
    """src_root ishchi daraxtining nusxasi dst da, bitta commit li `main` repo."""
    shutil.copytree(src_root, dst, symlinks=True, ignore=REPO_IGNORE)
    git(dst, "init", "-q")
    git(dst, "symbolic-ref", "HEAD", "refs/heads/main")
    git(dst, "add", "-A")
    git(dst, "commit", "-q", "-m", "boshlang'ich")
    return dst


def origin_va_klonlar(template_bare, base):
    """(origin.git, klon, dev): bare origin shablondan, undan ikki klon.

    `klon` o'rnatiladigan klon, `dev` esa origin ga yangi commit push qiladigan
    ikkinchi ishchi daraxt (boshqa dasturchi)."""
    origin = os.path.join(base, "origin.git")
    git(base, "clone", "-q", "--bare", template_bare, origin)
    klon, dev = os.path.join(base, "klon"), os.path.join(base, "dev")
    git(base, "clone", "-q", origin, klon)
    git(base, "clone", "-q", origin, dev)
    return origin, klon, dev
