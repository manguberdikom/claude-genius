#!/usr/bin/env python3
"""Global o'rnatishni yangilaydi: o'zgarish ro'yxati, tasdiq, yangi snapshot.

    python3 tools/yangilash.py                 # ro'yxat, so'rov [y/N], keyin yangilaydi
    python3 tools/yangilash.py --faqat-korsat  # faqat ro'yxat: hech narsa o'zgarmaydi
    python3 tools/yangilash.py --ha            # so'rovsiz ha (ro'yxat baribir chiqadi)
    python3 tools/yangilash.py --klon <yo'l> --branch main

Yurgizish joyi: o'rnatilgan SNAPSHOTDAGI nusxa
(`~/.claude/genius/<sha12>/tools/yangilash.py`, o'rnatuvchi yo'lini chiqaradi),
klondagi emas: `git pull` dan keyin klonda ko'rilmagan yangi yangilash.py va
geniuslib.py bo'lishi mumkin va ular tasdiqdan OLDIN yurardi. Global o'rnatish
bor bo'lsa klondan yurgizilgan nusxa to'xtaydi (`--klondan` bilan ataylab
yurgiziladi). Klon manifestdagi `clone` dan olinadi; env yoki skript joyi undan
farq qilsa xato (aniq `--klon` ruxsat).

Nega kerak (R7.8, XV-Y1): global o'rnatishda hooklar klonning ishchi
daraxtidan emas, aniq commit dagi snapshotdan (`~/.claude/genius/<sha12>/`,
install/snapshot.py) yuradi. `git pull` ularni O'ZGARTIRMAYDI: yangi kod
foydalanuvchi ko'rib, tasdiqlagandan keyingina hookka o'tadi. Bu skript
shu tasdiqni beradi.

Tartib:
1. Klon tekshiriladi: git repo, branch da (detached HEAD emas), tracked
   fayllari toza. Iflos klon yoki detached HEAD da to'xtaydi.
2. `git fetch origin`.
3. Ko'rsatiladi: `git log --oneline <asos>..origin/<branch>` va
   `git diff --stat <asos>..origin/<branch> -- tools install .claude .github`
   (hookka tegadigan yo'llar). `<asos>` hozir ishlayotgan snapshot commiti;
   manifest yo'q yoki commit klonda topilmasa klon HEAD. Snapshot klon
   HEAD dan orqada bo'lsa (qo'lda `git pull` qilingan), HEAD gacha bo'lgan
   ko'rilmagan commitlar ham ro'yxatga kiradi.
4. So'rov. `--faqat-korsat` shu yerda tugaydi, `--ha` so'ramaydi. Javob
   bo'sh yoki stdin yo'q (CI, agent) bo'lsa "yo'q".
5. Tasdiqdan keyin `git merge --ff-only`: ff bo'lmasa (klon va origin
   ajralgan) to'xtaydi, rebase va merge commit yo'q.
6. Yangi snapshot va settings.json dagi hook yo'llari o'rnatuvchining
   mavjud yo'li bilan yangilanadi (`install/install.py --apply`, Windows da
   `manguberdi.ps1 -Apply`): takrorlanmaydi.
7. Eski snapshot BITTA qaytarish uchun qoladi, qolgani `git worktree
   remove` bilan tozalanadi (faqat shu klonniki, `~/.claude/genius` ostida).

Qaytarish: settings.json zaxirasi o'rnatuvchi chiqargan papkada
(install/README.md, "Orqaga qaytarish"), eski snapshot esa joyida.

Chiqish kodi: 0 yangilandi, yangilanish yo'q, yoki rad etildi/ko'rsatildi;
1 xato (sabab matnda, hech narsa yarim qolmaganini matn aytadi).
"""

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INSTALL = os.path.join(ROOT, "install")
for _path in (HERE, INSTALL):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import geniuslib  # noqa: E402
import snapshot  # noqa: E402

# Hook va asboblarga tegadigan yo'llar: diff shularni ko'rsatadi.
HOOK_PATHS = ("tools", "install", ".claude", ".github")
FETCH_TIMEOUT = 180
MAX_LOG = 40
YES = ("y", "yes", "ha", "h")


class Xato(Exception):
    """Yangilash to'xtaydi: sabab matnda."""


def say(text=""):
    print(text)


def git(clone, args, timeout=60):
    proc = geniuslib.run_git(["-C", clone] + list(args), timeout=timeout)
    if proc is None:
        raise Xato("git yurmadi (o'rnatilmagan yoki vaqt tugadi): git %s" % " ".join(args))
    return proc


def git_out(clone, args, timeout=60):
    """stdout (bo'sh joysiz) yoki None, agar git xato bergan bo'lsa."""
    proc = git(clone, args, timeout)
    return proc.stdout.strip() if proc.returncode == 0 else None


def claude_dir():
    home = os.path.expanduser("~")
    if not home or home == "~" or not home.strip("/"):
        raise Xato("uy papkasi aniqlanmadi (HOME=%r)" % home)
    return os.path.join(home, ".claude")


def read_manifest(claude):
    path = os.path.join(claude, "skills", "manguberdi", ".genius.json")
    try:
        with open(path, encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def inside(path, folder):
    path = os.path.normcase(os.path.realpath(path))
    folder = os.path.normcase(os.path.realpath(folder))
    return path == folder or path.startswith(folder.rstrip(os.sep) + os.sep)


def same(left, right):
    return (os.path.normcase(os.path.realpath(left))
            == os.path.normcase(os.path.realpath(right)))


def from_snapshot(claude):
    """Skript pin qilingan snapshotdan (`~/.claude/genius/<sha12>`) yurayaptimi."""
    return geniuslib.is_snapshot(ROOT) and inside(ROOT, snapshot.genius_dir(claude))


def find_clone(opts, manifest, claude):
    """Qaysi klon yangilanadi.

    Aniq `--klon` ustun. Aks holda manifestdagi `clone` (o'rnatuvchi yozgan):
    skript turgan klon (klondan yurgizilsa) yoki `GENIUS_CLONE` (snapshotdan
    yurgizilsa) undan farq qilsa xato: noto'g'ri klonni jim yangilamaslik uchun.
    Manifest yo'q bo'lsa (global o'rnatish yo'q) klondan yurgan skriptning
    klonining o'zi."""
    if opts.klon:
        return os.path.abspath(opts.klon)
    pinned = from_snapshot(claude)
    here = geniuslib.clone_root(ROOT) if pinned else ROOT
    if pinned and here == ROOT:
        here = ""   # GENIUS_CLONE yo'q yoki yaroqsiz
    recorded = str((manifest or {}).get("clone") or "")
    if recorded:
        if here and not same(here, recorded):
            raise Xato("manifestdagi klon %s, lekin siz %s dan yurgizdingiz. Boshqa klonni "
                       "yangilamoqchi bo'lsangiz `--klon <yo'l>` bering. Hech narsa "
                       "o'zgarmadi." % (recorded, here))
        return recorded
    if here:
        return here
    raise Xato("klon topilmadi (manifestda clone yo'q, GENIUS_CLONE yo'q). `--klon <yo'l>` bering.")


def require_snapshot_copy(opts, manifest, claude):
    """Klondan yurgizilgan yangilash.py ni to'xtatadi (manifest bor bo'lsa).

    Aks holda `git pull` dan keyin ko'rilmagan yangi yangilash.py va geniuslib.py
    tasdiqdan OLDIN yurardi: aynan shu zanjirni yopish kerak. Yechim: o'rnatilgan
    snapshotdagi nusxa (manifest `root`). `--klondan` bilan rozilik berilsa
    (klonning o'zida yangilash.py ni ishlab chiqayotgan dasturchi) ogohlantirib
    davom etadi."""
    if from_snapshot(claude) or not manifest:
        return
    root = str(manifest.get("root") or "")
    tool = os.path.join(root, "tools", "yangilash.py").replace("\\", "/")
    if opts.klondan:
        say("OGOHLANTIRISH: --klondan: klondagi yangilash.py yuryapti (pull dan keyin "
            "ko'rilmagan kod bo'lishi mumkin). Odatdagi yo'l: python3 %s" % tool)
        return
    raise Xato("bu nusxa klondan yuryapti (%s): `git pull` dan keyin unda ko'rilmagan kod "
               "tasdiqdan oldin yurardi. O'rnatilgan snapshotdagi nusxani ishlating:\n"
               "  python3 %s\nKlondagi nusxani ataylab yurgizish uchun `--klondan`. "
               "Hech narsa o'zgarmadi." % (ROOT, tool))


def preflight(clone, branch_opt):
    """(branch). Klon tayyor emas bo'lsa Xato: hech narsa o'zgarmaydi."""
    if not os.path.isdir(clone):
        raise Xato("klon topilmadi: %s" % clone)
    if git_out(clone, ["rev-parse", "--git-dir"], 10) is None:
        raise Xato("%s git repo emas" % clone)
    branch = git_out(clone, ["symbolic-ref", "--short", "-q", "HEAD"], 10)
    if not branch:
        raise Xato("klon detached HEAD da (%s): branch ga o'ting va qayta yurgizing. "
                   "Hech narsa o'zgarmadi." % clone)
    dirty = git_out(clone, ["status", "--porcelain", "--untracked-files=no"], 60)
    if dirty:
        first = dirty.splitlines()
        raise Xato("klon iflos, commit qilinmagan o'zgarish bor (%d ta, masalan: %s). "
                   "Avval commit yoki stash qiling. Hech narsa o'zgarmadi."
                   % (len(first), first[0].strip()))
    branch = branch_opt or branch
    if not re.match(r"^[\w][\w./-]{0,100}\Z", branch) or ".." in branch:
        raise Xato("branch nomi yaroqsiz: %s" % branch)
    return branch


def short(sha):
    return (sha or "?")[:snapshot.SHA_UZUNLIK]


def commit_bor(clone, sha):
    return bool(sha) and bool(snapshot.SHA_RE.match(sha)) and git(
        clone, ["cat-file", "-e", sha + "^{commit}"], 10).returncode == 0


def royxat_korsat(clone, base, final):
    """base..final: commitlar va hookka tegadigan fayllar. Qaytaradi: commitlar soni."""
    log = git_out(clone, ["log", "--oneline", "%s..%s" % (base, final)]) or ""
    lines = log.splitlines()
    say()
    say("Yangi commitlar (%s..%s): %d ta" % (short(base), short(final), len(lines)))
    for text in lines[:MAX_LOG]:
        say("  " + text)
    if len(lines) > MAX_LOG:
        say("  ... va yana %d ta (to'liq: git -C %s log --oneline %s..%s)"
            % (len(lines) - MAX_LOG, clone, short(base), short(final)))
    stat = git_out(clone, ["diff", "--stat", "%s..%s" % (base, final), "--"]
                   + list(HOOK_PATHS)) or ""
    say()
    say("Hook va asboblarga tegadigan o'zgarish (%s):" % ", ".join(HOOK_PATHS))
    if stat:
        for text in stat.splitlines():
            say("  " + text)
    else:
        say("  yo'q: tools, install, .claude va .github o'zgarmagan")
    total = git_out(clone, ["diff", "--shortstat", "%s..%s" % (base, final)]) or ""
    if total:
        say("Hammasi: %s" % total)
    say("To'liq diff (ko'rib chiqing): git -C %s diff %s..%s -- %s"
        % (clone, short(base), short(final), " ".join(HOOK_PATHS)))
    return len(lines)


def tasdiq(opts):
    if opts.ha:
        say("--ha berilgan: so'ralmaydi.")
        return True
    say()
    try:
        answer = input("Yangilansinmi? [y/N] ")
    except (EOFError, OSError):
        say("(javob yo'q: stdin yopiq, 'yo'q' deb olindi)")
        return False
    return answer.strip().lower() in YES


def installer(clone):
    """O'rnatuvchining mavjud yo'li: Linux va macOS da install.py, Windows da ps1."""
    if os.name == "nt":
        ps1 = os.path.join(clone, "install", "manguberdi.ps1")
        return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1,
                "-GeniusPath", clone, "-Apply"]
    return [sys.executable, os.path.join(clone, "install", "install.py"),
            "--genius-path", clone, "--apply"]


def run_installer(clone):
    try:
        proc = subprocess.run(installer(clone), stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, encoding="utf-8",
                              errors="replace", cwd=clone)
    except OSError as exc:
        return 1, str(exc)
    return proc.returncode, proc.stdout.strip()


def update(opts):
    claude = claude_dir()
    manifest = read_manifest(claude)
    require_snapshot_copy(opts, manifest, claude)
    clone = find_clone(opts, manifest, claude)
    branch = preflight(clone, opts.branch)
    target_ref = "origin/%s" % branch

    say("Klon  : %s (branch %s)" % (clone, branch))
    say("fetch : git fetch origin")
    proc = git(clone, ["fetch", "origin"], FETCH_TIMEOUT)
    if proc.returncode != 0:
        raise Xato("git fetch yiqildi: %s. Hech narsa o'zgarmadi."
                   % (proc.stderr.strip() or proc.stdout.strip())[:300])
    target = git_out(clone, ["rev-parse", "--verify", target_ref + "^{commit}"], 10)
    if not target:
        raise Xato("%s topilmadi: remote yoki branch nomini tekshiring. Hech narsa "
                   "o'zgarmadi." % target_ref)
    head = git_out(clone, ["rev-parse", "HEAD"], 10)
    installed = str((manifest or {}).get("commit") or "")
    installed = installed if commit_bor(clone, installed) else ""

    say("O'rnatilgan snapshot: %s%s" % (short(installed) if installed else "yo'q",
                                       "" if manifest else " (manifest topilmadi)"))
    say("Klon HEAD          : %s" % short(head))
    say("%-19s: %s" % (target_ref, short(target)))

    # Qaysi commit snapshot bo'ladi: ff bo'lsa origin, klon origindan ilgari
    # bo'lsa (yangi narsa yo'q) HEAD, ajralgan bo'lsa to'xtaymiz.
    merge_needed = head != target
    if merge_needed:
        if git(clone, ["merge-base", "--is-ancestor", head, target], 10).returncode == 0:
            final = target
        elif git(clone, ["merge-base", "--is-ancestor", target, head], 10).returncode == 0:
            final, merge_needed = head, False   # klon origindan oldinda: merge kerak emas
        else:
            raise Xato("fast-forward mumkin emas: klon (%s) va %s (%s) ajralgan. "
                       "Rebase va merge commit qilinmaydi: ajralishni qo'lda hal "
                       "qiling. Hech narsa o'zgarmadi." % (short(head), target_ref, short(target)))
    else:
        final = head

    if final == installed:
        say()
        say("Yangilanish yo'q: o'rnatilgan snapshot %s allaqachon eng yangi commit." % short(final))
        return 0
    if manifest is None:
        say()
        say("Global o'rnatish topilmadi (%s yo'q): snapshot yo'q." % os.path.join(
            claude, "skills", "manguberdi", ".genius.json"))
        if not merge_needed:
            say("O'rnatish: python3 %s --apply" % os.path.join(clone, "install", "install.py"))
            return 0

    base = installed or head
    count = royxat_korsat(clone, base, final)
    if installed and installed != head:
        say()
        say("Diqqat: o'rnatilgan snapshot (%s) klon HEAD (%s) dan farq qiladi: oradagi "
            "commitlar ham yangi snapshotga kiradi." % (short(installed), short(head)))
    if not count and base == final:
        say("  (commit farqi yo'q)")

    if opts.faqat_korsat:
        say()
        say("--faqat-korsat: hech narsa o'zgarmadi.")
        return 0
    if not tasdiq(opts):
        say()
        say("Rad etildi: klon, snapshot va settings.json o'zgarmadi.")
        return 0

    old_head = head
    if merge_needed:
        say()
        say("git merge --ff-only %s" % target_ref)
        proc = git(clone, ["merge", "--ff-only", target], 120)
        if proc.returncode != 0:
            raise Xato("merge --ff-only yiqildi: %s. Klon o'zgarmadi, snapshot ham."
                       % (proc.stderr.strip() or proc.stdout.strip())[:300])
        say("  klon: %s -> %s" % (short(old_head), short(final)))

    if manifest is None:
        say()
        say("Klon yangilandi. Global o'rnatish yo'q: python3 %s --apply"
            % os.path.join(clone, "install", "install.py"))
        return 0

    # Qaytarish uchun faqat haqiqiy snapshot: eski (snapshotsiz) o'rnatishda
    # manifestdagi root klonning o'zi edi, uni "eski snapshot" deb bo'lmaydi.
    previous = str((manifest or {}).get("root") or "")
    if not (geniuslib.is_snapshot(previous) and inside(previous, snapshot.genius_dir(claude))):
        previous = ""
    say()
    say("Klon  : %s (o'rnatuvchi shu klonning install/ idan yuradi)" % clone)
    say("Yangi snapshot va settings.json: %s" % " ".join(installer(clone)))
    code, out = run_installer(clone)
    if out:
        for text in out.splitlines():
            say("  " + text)
    if code != 0:
        say()
        say("XATO: o'rnatuvchi rc=%d. Klon %s ga o'tdi, settings.json va snapshot "
            "to'liq yangilanmagan bo'lishi mumkin: eski snapshot (%s) joyida." % (
                code, short(final), short(installed)))
        if merge_needed:
            say("Klonni qaytarish: git -C %s reset --hard %s (faqat o'zingiz xohlasangiz)."
                % (clone, old_head))
        return 1

    fresh = read_manifest(claude) or {}
    keep = [p for p in (fresh.get("root"), previous) if p and os.path.isdir(p)]
    try:
        removed = snapshot.tozala(clone, claude, keep)
    except snapshot.SnapshotXato as exc:
        say("OGOHLANTIRISH: eski snapshot tozalanmadi: %s" % exc)
        removed = []
    say()
    say("Yangilandi: snapshot %s." % short(fresh.get("commit") or final))
    if previous and previous != fresh.get("root") and os.path.isdir(previous):
        say("Qaytarish uchun eski snapshot qoldi: %s" % previous)
    for path in removed:
        say("Tozalandi (git worktree remove): %s" % path)
    say("Yangi sessiyada o'zgarish ko'rinadi.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Global o'rnatishni yangilaydi: o'zgarish ro'yxati, tasdiq, "
                    "yangi snapshot (R7.8 XV-Y1).")
    parser.add_argument("--klon", default="",
                        help="klon yo'li (sukut: skript turgan klon, snapshotdan "
                             "yurgan bo'lsa GENIUS_CLONE yoki manifestdagi)")
    parser.add_argument("--klondan", action="store_true",
                        help="klondagi yangilash.py ni ataylab yurgizish (odatda snapshotdagi "
                             "nusxa ishlatiladi: pull dan keyin ko'rilmagan kod yurmasin)")
    parser.add_argument("--branch", default="",
                        help="yangilanadigan branch (sukut: klonning joriy branch i)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--ha", action="store_true",
                       help="so'ramasdan ha (ro'yxat baribir chiqadi)")
    group.add_argument("--faqat-korsat", action="store_true",
                       help="faqat ro'yxat: hech narsa o'zgarmaydi")
    opts = parser.parse_args(argv)
    try:
        return update(opts)
    except (Xato, snapshot.SnapshotXato) as exc:
        print("XATO: %s" % exc)
        return 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
