#!/usr/bin/env python3
"""geniuslib.py uchun sinovlar.

    python3 tools/test_geniuslib.py
    python3 tools/test_geniuslib.py -k atomik

Ikki yordamchi: `run_git` (muvaffaqiyat, git xatosi, git yo'q, timeout,
bytes, stdin, muhit) va `atomic_write_text` (oraliq holatda eski fayl
butun, tmp qolmaydi, encoding, fsync, mtime). Hammasi vaqtinchalik
papkada: jonli repo va holatga tegilmaydi. "git yo'q" PATH ni bo'sh
papkaga ko'rsatib taqlid qilinadi, timeout esa soxta `git` skripti bilan
(faqat POSIX, Windows da o'tkazib yuboriladi).
"""

import contextlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import geniuslib  # noqa: E402
import testkit  # noqa: E402

HAS_GIT = shutil.which("git") is not None


@contextlib.contextmanager
def temp_dir():
    folder = tempfile.mkdtemp(prefix="geniuslib-")
    try:
        yield folder
    finally:
        shutil.rmtree(folder, ignore_errors=True)


@contextlib.contextmanager
def patched(owner, name, value):
    old = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, old)


@contextlib.contextmanager
def path_env(folder):
    """PATH faqat `folder`: git topilmasa OSError chiqadi."""
    old = os.environ.get("PATH")
    os.environ["PATH"] = folder
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = old


def fake_git(folder, body):
    """folder ichida `git` nomli POSIX skript yasaydi."""
    script = os.path.join(folder, "git")
    with open(script, "w") as handle:
        handle.write("#!/bin/sh\n" + body + "\n")
    os.chmod(script, 0o755)


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def leftovers(folder):
    return [name for name in os.listdir(folder) if name.endswith(".tmp")]


# ---- run_git ----

def git_success():
    if not HAS_GIT:
        return [("git o'rnatilmagan: o'tkazib yuborildi", True)]
    with temp_dir() as folder:
        subprocess.run(["git", "init", "-q", folder], check=True,
                       capture_output=True)
        proc = geniuslib.run_git(["rev-parse", "--show-toplevel"], cwd=folder)
        top = proc.stdout.strip() if proc else ""
        by_c = geniuslib.run_git(["-C", folder, "rev-parse", "--git-dir"])
        return [
            ("CompletedProcess, returncode 0", bool(proc) and proc.returncode == 0),
            ("cwd: git shu papkada yuradi",
             os.path.realpath(top) == os.path.realpath(folder)),
            ("sukut text=True: stdout str", isinstance(proc.stdout, str)),
            ("-C args da ham ishlaydi", bool(by_c) and by_c.stdout.strip() == ".git"),
        ]


def git_bytes_input_env():
    if not HAS_GIT:
        return [("git o'rnatilmagan: o'tkazib yuborildi", True)]
    blob = geniuslib.run_git(["hash-object", "--stdin"], text=False,
                             input=b"salom\n")
    ident = geniuslib.run_git(["var", "GIT_AUTHOR_IDENT"],
                              env={"GIT_AUTHOR_NAME": "Muallif",
                                   "GIT_AUTHOR_EMAIL": "m@x.uz"})
    return [
        ("text=False: stdout bytes", bool(blob) and isinstance(blob.stdout, bytes)),
        ("input stdin ga beriladi: 40 belgili hash",
         bool(blob) and len(blob.stdout.strip()) in (40, 64)),
        ("env os.environ ustiga qo'shiladi",
         bool(ident) and ident.stdout.startswith("Muallif <m@x.uz>")),
    ]


def git_failure():
    if not HAS_GIT:
        return [("git o'rnatilmagan: o'tkazib yuborildi", True)]
    with temp_dir() as folder:
        # Bo'sh papka repo emas: git 128 bilan tugaydi, istisno emas.
        old = os.environ.get("GIT_CEILING_DIRECTORIES")
        os.environ["GIT_CEILING_DIRECTORIES"] = os.path.dirname(folder)
        try:
            proc = geniuslib.run_git(["rev-parse", "--show-toplevel"], cwd=folder)
        finally:
            if old is None:
                os.environ.pop("GIT_CEILING_DIRECTORIES", None)
            else:
                os.environ["GIT_CEILING_DIRECTORIES"] = old
        bad_cwd = geniuslib.run_git(["status"], cwd=os.path.join(folder, "yoq"))
        return [
            ("git xatosi: None emas, returncode != 0",
             proc is not None and proc.returncode != 0),
            ("xato matni stderr da", proc is not None and bool(proc.stderr.strip())),
            ("cwd yo'q papka: OSError yutiladi, None", bad_cwd is None),
        ]


def git_missing():
    with temp_dir() as empty:
        with path_env(empty):
            soft = geniuslib.run_git(["--version"])
            try:
                geniuslib.run_git(["--version"], strict=True)
                raised = None
            except OSError as exc:
                raised = exc
    return [
        ("git yo'q: None", soft is None),
        ("git yo'q, strict: OSError ko'tariladi", raised is not None),
    ]


def git_timeout():
    if os.name == "nt":
        return [("Windows: soxta git skripti yo'q, o'tkazib yuborildi", True)]
    with temp_dir() as folder:
        fake_git(folder, "sleep 5")
        with path_env(folder + os.pathsep + "/bin:/usr/bin"):
            soft = geniuslib.run_git(["status"], timeout=0.2)
            try:
                geniuslib.run_git(["status"], timeout=0.2, strict=True)
                raised = None
            except subprocess.TimeoutExpired as exc:
                raised = exc
    return [
        ("timeout: None", soft is None),
        ("timeout, strict: TimeoutExpired ko'tariladi", raised is not None),
    ]


def git_no_timeout_value():
    if os.name == "nt":
        return [("Windows: o'tkazib yuborildi", True)]
    seen = {}

    def fake_run(cmd, **kwargs):
        seen.update(kwargs)
        seen["cmd"] = cmd
        return subprocess.CompletedProcess(cmd, 0, "", "")

    with patched(geniuslib.subprocess, "run", fake_run):
        geniuslib.run_git(["status"], timeout=None)
        none_timeout = seen.get("timeout", "yo'q")
        geniuslib.run_git(["status"])
        default_timeout = seen.get("timeout")
    return [
        ("timeout=None cheksiz o'tadi", none_timeout is None),
        ("sukut timeout 20 s", default_timeout == 20),
        ("buyruq `git` + args", seen["cmd"] == ["git", "status"]),
    ]


# ---- atomic_write_text ----

def atomic_basic():
    with temp_dir() as folder:
        path = os.path.join(folder, "a.json")
        geniuslib.atomic_write_text(path, "bir")
        first = read_bytes(path)
        geniuslib.atomic_write_text(path, "ikki")
        return [
            ("yangi fayl yoziladi", first == b"bir"),
            ("mavjud fayl almashtiriladi", read_bytes(path) == b"ikki"),
            ("tmp qolmaydi", leftovers(folder) == []),
        ]


def atomic_intermediate():
    """os.replace paytida: eski fayl hali butun, yangi matn tmp da."""
    with temp_dir() as folder:
        path = os.path.join(folder, "a.txt")
        with open(path, "w") as handle:
            handle.write("ESKI")
        seen = {}
        real = os.replace

        def spy(src, dst):
            seen["old"] = read_bytes(dst)
            seen["tmp"] = read_bytes(src)
            seen["src"] = src
            real(src, dst)

        with patched(os, "replace", spy):
            geniuslib.atomic_write_text(path, "YANGI")
        return [
            ("almashtirishdan oldin eski fayl butun", seen.get("old") == b"ESKI"),
            ("yangi matn tmp da to'liq", seen.get("tmp") == b"YANGI"),
            ("tmp nomida pid", seen.get("src") == "%s.%d.tmp" % (path, os.getpid())),
            ("keyin yangi matn", read_bytes(path) == b"YANGI"),
            ("tmp qolmaydi", leftovers(folder) == []),
        ]


def atomic_replace_fails():
    with temp_dir() as folder:
        path = os.path.join(folder, "a.txt")
        with open(path, "w") as handle:
            handle.write("ESKI")

        def broken(src, dst):
            raise OSError("almashtirib bo'lmadi")

        with patched(os, "replace", broken):
            try:
                geniuslib.atomic_write_text(path, "YANGI")
                raised = False
            except OSError:
                raised = True
        return [
            ("os.replace xatosi OSError bo'lib ko'tariladi", raised),
            ("eski fayl butun", read_bytes(path) == b"ESKI"),
            ("tmp o'chiriladi", leftovers(folder) == []),
        ]


def atomic_write_fails():
    """Yozish o'rtasida yiqilsa (kodlab bo'lmaydigan belgi): eski fayl butun."""
    with temp_dir() as folder:
        path = os.path.join(folder, "a.txt")
        with open(path, "w") as handle:
            handle.write("ESKI")
        try:
            geniuslib.atomic_write_text(path, "oʻzbek", encoding="ascii")
            raised = False
        except UnicodeEncodeError:
            raised = True
        return [
            ("kodlash xatosi ko'tariladi", raised),
            ("eski fayl butun", read_bytes(path) == b"ESKI"),
            ("tmp o'chiriladi", leftovers(folder) == []),
        ]


def atomic_missing_folder():
    with temp_dir() as folder:
        path = os.path.join(folder, "yoq", "a.txt")
        try:
            geniuslib.atomic_write_text(path, "x")
            raised = False
        except OSError:
            raised = True
        return [
            ("papka yaratilmaydi: OSError", raised),
            ("papka paydo bo'lmaydi", not os.path.exists(os.path.dirname(path))),
        ]


def atomic_encoding():
    with temp_dir() as folder:
        path = os.path.join(folder, "a.txt")
        text = "oʻzbek é\n"
        geniuslib.atomic_write_text(path, text)
        utf8 = read_bytes(path)
        geniuslib.atomic_write_text(path, text, encoding="utf-16")
        utf16 = read_bytes(path)
        geniuslib.atomic_write_text(path, "a\nb\n", newline="\n")
        lf = read_bytes(path)
        geniuslib.atomic_write_text(path, "a\nb\n", newline="\r\n")
        crlf = read_bytes(path)
        return [
            ("sukut UTF-8", utf8 == text.encode("utf-8")),
            ("encoding parametri", utf16 == text.encode("utf-16")),
            ("newline='\\n': CR yo'q", lf == b"a\nb\n"),
            ("newline='\\r\\n': CRLF", crlf == b"a\r\nb\r\n"),
        ]


def atomic_fsync_mtime():
    with temp_dir() as folder:
        path = os.path.join(folder, "a.txt")
        calls = []
        real = os.fsync

        def spy(fd):
            calls.append(fd)
            real(fd)

        with patched(os, "fsync", spy):
            geniuslib.atomic_write_text(path, "x")
            plain = len(calls)
            geniuslib.atomic_write_text(path, "y", fsync=True)
            synced = len(calls)
            body = read_bytes(path)
        geniuslib.atomic_write_text(path, "z", mtime=1_000_000_000)
        return [
            ("fsync sukutda yo'q", plain == 0),
            ("fsync=True: diskka yoziladi", synced == 1 and body == b"y"),
            ("mtime almashtirishdan oldin qo'yiladi",
             int(os.path.getmtime(path)) == 1_000_000_000),
            ("tmp qolmaydi", leftovers(folder) == []),
        ]


CASES = [
    ("run_git: muvaffaqiyat", git_success),
    ("run_git: bytes, stdin, muhit", git_bytes_input_env),
    ("run_git: git xatosi", git_failure),
    ("run_git: git yo'q", git_missing),
    ("run_git: timeout", git_timeout),
    ("run_git: timeout qiymatlari", git_no_timeout_value),
    ("atomik: oddiy yozuv", atomic_basic),
    ("atomik: oraliq holat", atomic_intermediate),
    ("atomik: almashtirish yiqiladi", atomic_replace_fails),
    ("atomik: yozish yiqiladi", atomic_write_fails),
    ("atomik: papka yo'q", atomic_missing_folder),
    ("atomik: encoding va newline", atomic_encoding),
    ("atomik: fsync va mtime", atomic_fsync_mtime),
]


def main():
    return testkit.run_cases(CASES, sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
