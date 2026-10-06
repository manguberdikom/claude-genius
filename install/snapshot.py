#!/usr/bin/env python3
"""Global o'rnatish uchun pin qilingan snapshot: `~/.claude/genius/<sha12>/`.

    python3 install/snapshot.py yol    --clone <klon> --claude-dir <~/.claude>
    python3 install/snapshot.py yarat  --clone <klon> --claude-dir <~/.claude> [--sha <sha>]
    python3 install/snapshot.py arxiv  --clone <klon> --sha <sha> --to <papka>
    python3 install/snapshot.py royxat --clone <klon> --claude-dir <~/.claude> [--yetim]
    python3 install/snapshot.py tozala --clone <klon> --claude-dir <~/.claude> \
        [--saqla <snapshot>]... [--yetim]
    python3 install/snapshot.py farq   --clone <klon> --claude-dir <~/.claude> --sha <yangi>

Nega kerak (R7.8, XV-Y1): hook buyrug'i avval klonning ishchi daraxtidagi
`tools/` ga bog'langan edi, shuning uchun `git pull` dan keyingi birinchi
promptdayoq yangi kod hech kim ko'rmasdan bajarilardi. Endi hooklar aniq
commit dagi `git worktree add --detach` snapshotidan yuradi. Butun daraxt
olinadi, faqat `tools/` emas: asboblar `ROOT` ni `tools/` ning ota
papkasidan oladi va `index/`, `docs/`, `GLOSSARY.md` ni shu yerdan o'qiydi.

Yoziladigan narsa (memory, holat) snapshotga emas, klonga tushadi: o'rnatuvchi
settings.json `env` ga `GENIUS_CLONE` yozadi (tools/geniuslib.py clone_root).

Bu mantiq install.py va manguberdi.ps1 uchun BITTA: ikkalasi snapshot joyini
va git buyrug'ini shu yerdan oladi, shuning uchun paritet tasodif emas va
PowerShell qismi sinalmaydigan git mantig'ini o'zida tutmaydi.

Xavfsizlik: o'chirish faqat `<claude-dir>/genius/<12 ta hex>` papkalarini
oladi (symlink emas, haqiqiy yo'li shu papka ichida), boshqa hech narsani.
Chiqish kodi: 0 muvaffaqiyat, 1 xato (sabab stdout da).
"""

import argparse
import io
import json
import os
import re
import shutil
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(os.path.dirname(HERE), "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

import geniuslib  # noqa: E402

SHA_UZUNLIK = 12
SHA_RE = re.compile(r"^[0-9a-f]{40}\Z")
NOM_RE = re.compile(r"^[0-9a-f]{%d}\Z" % SHA_UZUNLIK)
GIT_TIMEOUT = 180
HOOK_PATHS = ("tools", "install", ".claude", ".github")
MAX_LOG = 40


class SnapshotXato(Exception):
    """Snapshotni yasab yoki o'chirib bo'lmaydi: sabab matnda."""


def genius_dir(claude_dir):
    return os.path.join(claude_dir, "genius")


def snapshot_yol(claude_dir, sha):
    """Snapshot joyi: `<claude-dir>/genius/<sha12>`."""
    return os.path.join(genius_dir(claude_dir), sha[:SHA_UZUNLIK])


def git(args, cwd=None, timeout=20, text=True):
    proc = geniuslib.run_git(args, cwd=cwd, timeout=timeout, text=text)
    if proc is None:
        raise SnapshotXato("git yurmadi (o'rnatilmagan yoki vaqt tugadi): git %s"
                           % " ".join(args))
    return proc


def sha_ol(clone, ref="HEAD"):
    """To'liq commit sha. Klon git repo emas yoki commit yo'q bo'lsa xato."""
    if ref != "HEAD" and not SHA_RE.match(ref):
        raise SnapshotXato("sha 40 ta kichik hex bo'lishi shart: %s" % ref)
    proc = git(["-C", clone, "rev-parse", "--verify", ref + "^{commit}"])
    out = proc.stdout.strip()
    if proc.returncode != 0 or not SHA_RE.match(out):
        raise SnapshotXato(
            "%s da commit topilmadi (git repo emasmi?): hooklarni aniq commitga "
            "pin qilish uchun klon git repo bo'lishi shart. %s"
            % (clone, proc.stderr.strip()[:200]))
    return out


def git_common_dir(clone):
    """Klonning `.git` papkasi (haqiqiy yo'l) yoki None."""
    if not os.path.isdir(clone):
        return None
    proc = geniuslib.run_git(["-C", clone, "rev-parse", "--git-common-dir"], timeout=10)
    if proc is None or proc.returncode != 0 or not proc.stdout.strip():
        return None
    path = proc.stdout.strip()
    if not os.path.isabs(path):
        path = os.path.join(clone, path)
    return os.path.normcase(os.path.realpath(path))


def worktree_common_dir(path):
    """Snapshotning `.git` fayli ko'rsatgan asosiy `.git` yoki None.

    `.git` fayli `gitdir: <klon>/.git/worktrees/<nom>` deb yozilgan. Git
    ishga tushmaydi: klon o'chgan bo'lsa ham o'qiladi."""
    try:
        with open(os.path.join(path, ".git"), encoding="utf-8") as handle:
            first = handle.readline().strip()
    except OSError:
        return None
    if not first.startswith("gitdir:"):
        return None
    gitdir = first[len("gitdir:"):].strip().replace("\\", "/")
    head, sep, _ = gitdir.rpartition("/worktrees/")
    return os.path.normcase(os.path.normpath(head)) if sep else None


def _same_dir(left, right):
    if not left or not right:
        return False
    return os.path.normcase(os.path.realpath(left)) == os.path.normcase(os.path.realpath(right))


def royxat(clone, claude_dir, yetim=False):
    """Shu klonga tegishli snapshotlar. `yetim` bo'lsa asosiy `.git` i endi
    yo'q (klon o'chgan) snapshotlar ham: ularni faqat o'chirish mumkin."""
    base = genius_dir(claude_dir)
    try:
        names = sorted(os.listdir(base))
    except OSError:
        return []
    mine = git_common_dir(clone)
    out = []
    for name in names:
        path = os.path.join(base, name)
        if not NOM_RE.match(name) or os.path.islink(path) or not os.path.isdir(path):
            continue
        common = worktree_common_dir(path)
        if common is None:
            continue
        if _same_dir(common, mine) or (yetim and not os.path.exists(common)):
            out.append(path)
    return out


def tekshir(path, sha):
    """Mavjud snapshot shu commit va o'zgartirilmagan bo'lsa True, aks holda xato."""
    proc = git(["-C", path, "rev-parse", "HEAD"], timeout=10)
    if proc.returncode != 0 or proc.stdout.strip() != sha:
        raise SnapshotXato(
            "%s mavjud, lekin commit %s emas. Qo'lda tekshiring va kerak bo'lmasa "
            "`git worktree remove --force` bilan olib tashlang." % (path, sha[:SHA_UZUNLIK]))
    proc = git(["-C", path, "status", "--porcelain", "--untracked-files=no"], timeout=30)
    if proc.stdout.strip():
        first = proc.stdout.strip().splitlines()[0]
        raise SnapshotXato(
            "%s da o'zgartirilgan fayl bor (%s): snapshot hook kodini aniq commit "
            "holida ushlashi shart. Sababini aniqlang va `git worktree remove "
            "--force` bilan olib tashlab qayta o'rnating." % (path, first))
    return True


def manifest_commit(claude_dir):
    """Hozir o'rnatilgan snapshot commiti (`.genius.json`) yoki ''."""
    path = os.path.join(claude_dir, "skills", "manguberdi", ".genius.json")
    try:
        with open(path, encoding="utf-8-sig") as handle:
            value = str(json.load(handle).get("commit") or "")
    except (OSError, ValueError, AttributeError):
        return ""
    return value if SHA_RE.match(value) else ""


def farq_matn(clone, claude_dir, sha):
    """O'rnatilgan commitdan `sha` gacha ro'yxat (to'smaydi, faqat ko'rsatadi).

    `git log --oneline <eski>..<yangi>` va hookka tegadigan yo'llar uchun
    `git diff --stat`. O'rnatilgan commit yo'q, bir xil yoki klonda topilmasa
    bo'sh satr. install.py va ps1 ro'yxatsiz o'tishni ko'rsatib o'tsin deb
    shu yerdan oladi (tasdiqli yo'l: tools/yangilash.py)."""
    old = manifest_commit(claude_dir)
    if not old or old == sha:
        return ""
    if git(["-C", clone, "cat-file", "-e", old + "^{commit}"], timeout=10).returncode:
        return "Oldingi snapshot commiti (%s) klonda topilmadi: ro'yxat yo'q." % old[:SHA_UZUNLIK]
    log = git(["-C", clone, "log", "--oneline", "%s..%s" % (old, sha)]).stdout.strip().splitlines()
    stat = git(["-C", clone, "diff", "--stat", "%s..%s" % (old, sha), "--"]
               + list(HOOK_PATHS)).stdout.strip()
    out = ["Hook kodi %s dan %s ga o'tadi (tasdiqli yo'l: tools/yangilash.py). "
           "Yangi commitlar: %d ta" % (old[:SHA_UZUNLIK], sha[:SHA_UZUNLIK], len(log))]
    out += ["  " + line for line in log[:MAX_LOG]]
    if len(log) > MAX_LOG:
        out.append("  ... va yana %d ta" % (len(log) - MAX_LOG))
    out.append("Hookka tegadigan o'zgarish (%s):" % ", ".join(HOOK_PATHS))
    out += ["  " + line for line in stat.splitlines()] or ["  yo'q"]
    return "\n".join(out)


def yarat(clone, claude_dir, sha=None):
    """(yo'l, yangi yasaldimi). Mavjud snapshot qayta ishlatiladi, lekin avval
    tekshiriladi: boshqa commit yoki o'zgartirilgan bo'lsa xato (jim bosilmaydi).

    `-c core.autocrlf=false`: Windows da doc.sh CRLF bilan chiqib, bash
    uni yurgizmay qo'ymasin."""
    sha = sha or sha_ol(clone)
    path = snapshot_yol(claude_dir, sha)
    if os.path.lexists(path):
        if os.path.islink(path):
            raise SnapshotXato("%s symlink: snapshot haqiqiy papka bo'lishi shart" % path)
        # Boshqa klon bir xil sha da yasagan snapshotni ulashmaymiz: uning
        # `--uninstall` i bu klonning hookini ostidan olib tashlardi. Qaror:
        # xato (yo'lga klon identifikatori qo'shilmaydi: joy `<sha12>` qoladi).
        if not _same_dir(worktree_common_dir(path), git_common_dir(clone)):
            raise SnapshotXato(
                "%s boshqa klonga (yoki endi yo'q klonga) tegishli snapshot. Ikki klon bir "
                "snapshotni ulashmaydi: avval o'sha klon bilan `--uninstall` qiling, yoki "
                "bu klonga boshqa commit oling." % path)
        tekshir(path, sha)
        return path, False
    try:
        os.makedirs(genius_dir(claude_dir), exist_ok=True)
    except OSError as exc:
        raise SnapshotXato("%s yaratilmadi: %s" % (genius_dir(claude_dir), exc)) from exc
    # Qo'lda o'chirilgan snapshotning reestr yozuvi `worktree add` ni to'sadi
    # ("missing but already registered"): faqat yo'q papkalar yozuvi tozalanadi.
    geniuslib.run_git(["-C", clone, "worktree", "prune"], timeout=30)
    proc = git(["-C", clone, "-c", "core.autocrlf=false", "worktree", "add",
                "--detach", path, sha], timeout=GIT_TIMEOUT)
    if proc.returncode != 0:
        raise SnapshotXato("git worktree add yiqildi: %s"
                           % (proc.stderr.strip() or proc.stdout.strip())[:300])
    tekshir(path, sha)
    return path, True


def arxiv(clone, sha, dest):
    """Commit tarkibini `dest` ga ochadi (git ga yozmaydi: quruq yurish uchun)."""
    if not SHA_RE.match(sha):
        raise SnapshotXato("sha 40 ta kichik hex bo'lishi shart: %s" % sha)
    proc = git(["-C", clone, "archive", "--format=tar", sha], timeout=GIT_TIMEOUT, text=False)
    if proc.returncode != 0:
        raise SnapshotXato("git archive yiqildi: %s"
                           % proc.stderr.decode("utf-8", "replace").strip()[:300])
    os.makedirs(dest, exist_ok=True)
    real = os.path.realpath(dest)
    with tarfile.open(fileobj=io.BytesIO(proc.stdout), mode="r:") as tar:
        for member in tar.getmembers():
            target = os.path.realpath(os.path.join(real, member.name))
            if target != real and not target.startswith(real + os.sep):
                raise SnapshotXato("arxivda papkadan tashqariga yo'l: %s" % member.name)
            if member.issym() or member.islnk():
                link = os.path.realpath(os.path.join(os.path.dirname(target), member.linkname))
                if member.islnk():
                    link = os.path.realpath(os.path.join(real, member.linkname))
                if link != real and not link.startswith(real + os.sep):
                    raise SnapshotXato("arxivda papkadan tashqariga havola: %s" % member.name)
        try:
            tar.extractall(real, filter="data")   # Python 3.12+: xavfsiz filtr
        except TypeError:
            tar.extractall(real)                  # filter parametri yo'q (3.8)
    return dest


def olib_tashla(path, clone, claude_dir):
    """Bitta snapshotni olib tashlaydi. Faqat `<claude-dir>/genius/<12 hex>`.

    Avval `git worktree remove --force` (klon `.git/worktrees` yozuvi bilan),
    keyin `prune`. Klon yo'q yoki git rad etsa papkaning o'zi o'chadi, chunki
    yetim snapshot boshqa yo'l bilan ketmaydi."""
    base = os.path.realpath(genius_dir(claude_dir))
    name = os.path.basename(os.path.normpath(path))
    if (not NOM_RE.match(name) or os.path.islink(path)
            or os.path.realpath(os.path.dirname(os.path.abspath(path))) != base):
        raise SnapshotXato("%s snapshot emas (faqat %s/<%d hex> o'chiriladi)"
                           % (path, genius_dir(claude_dir), SHA_UZUNLIK))
    if not os.path.lexists(path):
        return False
    main = worktree_common_dir(path)
    proc = None
    if os.path.isdir(clone) and main and _same_dir(main, git_common_dir(clone)):
        proc = geniuslib.run_git(["-C", clone, "worktree", "remove", "--force", path],
                                 timeout=60)
    if os.path.lexists(path):
        shutil.rmtree(path, ignore_errors=True)
    if os.path.lexists(path):
        raise SnapshotXato("%s o'chmadi%s" % (path, (": " + proc.stderr.strip()[:200])
                                              if proc and proc.returncode else ""))
    if os.path.isdir(clone):
        geniuslib.run_git(["-C", clone, "worktree", "prune"], timeout=30)
    return True


def tozala(clone, claude_dir, saqla=(), yetim=False):
    """Shu klonning `saqla` dagidan boshqa snapshotlarini olib tashlaydi.
    Qaytaradi: olib tashlanganlar yo'llari."""
    keep = {os.path.normcase(os.path.realpath(p)) for p in saqla}
    removed = []
    for path in royxat(clone, claude_dir, yetim=yetim):
        if os.path.normcase(os.path.realpath(path)) in keep:
            continue
        if olib_tashla(path, clone, claude_dir):
            removed.append(path)
    return removed


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("amal", choices=("yol", "yarat", "arxiv", "royxat", "tozala", "farq"))
    parser.add_argument("--clone", required=True)
    parser.add_argument("--claude-dir", default="")
    parser.add_argument("--sha", default="")
    parser.add_argument("--to", default="")
    parser.add_argument("--saqla", action="append", default=[])
    parser.add_argument("--yetim", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.amal != "arxiv" and not args.claude_dir:
            raise SnapshotXato("--claude-dir kerak")
        if args.amal in ("yol", "yarat"):
            sha = args.sha or sha_ol(args.clone)
            path = snapshot_yol(args.claude_dir, sha)
            created = False
            if args.amal == "yarat":
                path, created = yarat(args.clone, args.claude_dir, sha)
            print(json.dumps({"sha": sha, "path": path.replace("\\", "/"),
                              "yangi": created, "mavjud": os.path.isdir(path)}))
        elif args.amal == "arxiv":
            if not args.to or not args.sha:
                raise SnapshotXato("--sha va --to kerak")
            print(arxiv(args.clone, args.sha, args.to))
        elif args.amal == "farq":
            print(farq_matn(args.clone, args.claude_dir, args.sha or sha_ol(args.clone)))
        elif args.amal == "royxat":
            print(json.dumps([p.replace("\\", "/")
                              for p in royxat(args.clone, args.claude_dir, args.yetim)]))
        else:
            removed = tozala(args.clone, args.claude_dir, args.saqla, args.yetim)
            print(json.dumps([p.replace("\\", "/") for p in removed]))
    except SnapshotXato as exc:
        print("XATO: %s" % exc)
        return 1
    return 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
