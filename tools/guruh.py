#!/usr/bin/env python3
"""Parallel guruhlar uchun git worktree: yaratish, holat, birlashtirish.

    python3 tools/guruh.py yarat orders [--nusxa .env]   # worktree va branch
    python3 tools/guruh.py royxat                        # faol guruhlar
    python3 tools/guruh.py birlashtir orders [--3way]    # o'zgarishni asosiy daraxtga
    python3 tools/guruh.py tozala orders [--majburiy]    # worktree va branch ni o'chirish
    python3 tools/guruh.py tozala --hammasi              # birlashgan va bo'sh guruhlar

Nega: ishchi papka bitta bo'lsa, ikki Gradle yoki Maven bir vaqtda
`build/` va `target/` ni bir-biriga yozadi, shuning uchun guruhlar
ketma-ket yurardi. Har guruhning o'z worktree si bor: o'z build papkasi,
o'z test yurishi. `~/.gradle` va `~/.m2` keshlari umumiy va bir vaqtda
o'qishga chidaydi.

Guruh asosiy daraxtning HEAD idan boshlanadi. Asosiy daraxtda commit
qilinmagan o'zgarish bo'lsa guruh uni ko'rmaydi, shuning uchun `yarat`
rad etadi: bunday holatda guruhlar ketma-ket ishlaydi, savol berilmaydi.

Birlashtirish commit qilmaydi: guruhning butun o'zgarishi (yangi
fayllar bilan) patch bo'lib asosiy daraxtga qo'llanadi va indeksga
tushadi, xuddi ish o'sha yerda bajarilgandek. Guruhlar fayl bo'yicha
ajratilgan bo'lishi kerak; kesishsa `birlashtir` asosiy daraxtga tegmay
kesishgan fayllarni aytadi, `--3way` esa ziddiyat belgilari bilan
qo'llaydi va egasi ularni asosiy daraxtda hal qiladi.

Tozalash ish yo'qotmaydi va begona narsaga tegmaydi. Birlashtirilmagan
va o'zgarishi bor guruhni `tozala` rc=1 bilan rad etadi va fayllarni
aytadi, `--majburiy` bilan o'chiradi; `--hammasi` faqat birlashgan yoki
o'zgarishsiz guruhlarni oladi. `--3way` ziddiyat bilan tugasa guruh
birlashgan hisoblanmaydi. Holat faylidagi yo'l guruhning o'z worktree
si bo'lmasa yoki branch `genius/<id>` bo'lmasa rc=2: hech narsa o'chmaydi.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time

ID_RE = re.compile(r"^[A-Za-z0-9][\w.-]{0,39}$")
BRANCH_RE = re.compile(r"^genius/[\w.-]{1,40}$")


def git(cwd, *args, check=False, data=None):
    proc = subprocess.run(["git", "-C", cwd] + list(args), capture_output=True,
                          input=data, timeout=120)
    if check and proc.returncode:
        raise RuntimeError((proc.stderr or proc.stdout).decode("utf-8", "replace").strip())
    return proc


def out(cwd, *args):
    proc = git(cwd, *args)
    return proc.stdout.decode("utf-8", "replace").strip() if proc.returncode == 0 else ""


def common_dir(start):
    """Umumiy .git papkasi, mutlaq. --path-format git 2.31 dan: eski git
    nisbiy yo'l beradi, u chaqiruv papkasiga nisbatan."""
    path = out(start, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if path and os.path.isabs(path):
        return path
    path = out(start, "rev-parse", "--git-common-dir")
    return os.path.normpath(os.path.join(start, path)) if path else ""


def main_root(start):
    """Asosiy worktree ildizi, guruh ichidan chaqirilsa ham."""
    common = common_dir(start)
    if not common:
        return None
    if os.path.basename(common) == ".git":
        return os.path.dirname(common)
    return out(start, "rev-parse", "--show-toplevel") or None


def state_file(root):
    return os.path.join(common_dir(root), "genius-guruh.json")


def load(root):
    try:
        with open(state_file(root), encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save(root, data):
    path = state_file(root)
    tmp = path + ".%d.tmp" % os.getpid()
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=1)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def limit():
    """Bir vaqtdagi guruh soni. Har guruh o'z Gradle daemon i va test JVM ini
    ko'taradi: mashina chegarasidan oshsa hamma guruh birga sekinlashadi."""
    try:
        return max(1, int(os.environ["GENIUS_GURUH_MAX"]))
    except (KeyError, ValueError):
        return max(2, min(4, (os.cpu_count() or 4) // 4))


def worktree_path(root, gid):
    base = os.environ.get("GENIUS_GURUH_DIR") or os.path.dirname(root)
    return os.path.join(base, "%s.guruh-%s" % (os.path.basename(root), gid))


def dirty(root):
    return out(root, "status", "--porcelain", "--untracked-files=normal")


def same(a, b):
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def bad_copy(item):
    """--nusxa faqat ildiz ichidagi nisbiy yo'l: mutlaq yo'l yoki `..`
    faylni worktree dan tashqariga yozadi yoki o'zini o'ziga ko'chiradi."""
    parts = item.replace("\\", "/").split("/")
    return os.path.isabs(item) or bool(os.path.splitdrive(item)[0]) or ".." in parts


def create(root, gid, copies):
    wrong = [item for item in copies if bad_copy(item)]
    if wrong:
        print("--nusxa faqat ildizga nisbiy yo'l, mutlaq yo'l va '..' yo'q: %s"
              % ", ".join(wrong))
        return 2
    data = load(root)
    if gid in data:
        print("Guruh bor: %s -> %s" % (gid, data[gid]["path"]))
        return 0
    active = [g for g, v in data.items() if not v.get("merged")]
    if len(active) >= limit():
        print("Faol guruh %d ta, chegara %d (GENIUS_GURUH_MAX). Avval birini "
              "birlashtiring yoki ketma-ket ishlang." % (len(active), limit()))
        return 1
    if dirty(root):
        print("Asosiy daraxtda commit qilinmagan o'zgarish bor: guruh HEAD dan "
              "boshlanadi va uni ko'rmaydi. Parallel rejim yo'q, ketma-ket ishlang.")
        return 1
    base = out(root, "rev-parse", "HEAD")
    path = worktree_path(root, gid)
    branch = "genius/%s" % gid
    try:
        git(root, "worktree", "add", "-q", "-b", branch, path, base, check=True)
    except RuntimeError as exc:
        print("worktree yaratilmadi: %s" % exc)
        return 1
    try:
        for item in copies:
            src = os.path.join(root, item)
            if os.path.isfile(src):
                dst = os.path.join(path, item)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            else:
                print("nusxa topilmadi: %s" % item)
        data[gid] = {"path": path, "branch": branch, "base": base,
                     "created": int(time.time())}
        save(root, data)
    except Exception as exc:  # har qanday xato: worktree yetim qolmasin
        # Holat fayliga tushmagan worktree ni royxat va tozala ko'rmaydi:
        # yetim qolmasin, endigina yaratilgan branch bilan qaytariladi.
        git(root, "worktree", "remove", "--force", path)
        git(root, "worktree", "prune")
        git(root, "branch", "-D", branch)
        print("Guruh yaratilmadi, worktree va branch qaytarildi: %s" % exc)
        return 1
    print("Guruh: %s\nPapka: %s\nBranch: %s\nAsos: %s" % (gid, path, branch, base[:12]))
    print("Aktyor promptida: `guruh: %s` va `papka: %s`. Testlar: "
          "run_tests.py --ildiz %s --asos %s --yurgiz" % (gid, path, path, base[:12]))
    return 0


def changed(path, base):
    git(path, "add", "-A")
    names = out(path, "diff", "--cached", "--name-only", base)
    return [n for n in names.splitlines() if n]


def merge(root, gid, three_way):
    data = load(root)
    group = data.get(gid)
    if not group:
        print("Guruh yo'q: %s" % gid)
        return 1
    path, base = group["path"], group["base"]
    files = changed(path, base)
    if not files:
        print("Guruh %s da o'zgarish yo'q." % gid)
        return 0
    patch = git(path, "diff", "--cached", "--binary", base).stdout
    check = git(root, "apply", "--check", "--index", data=patch)
    if check.returncode == 0:
        git(root, "apply", "--index", data=patch, check=True)
        group["merged"] = True
        save(root, data)
        print("Birlashtirildi: %s, %d fayl (indeksda, commit qilinmagan)" % (gid, len(files)))
        for name in files[:15]:
            print("  " + name)
        return 0
    touched = set(out(root, "diff", "--name-only", "HEAD").splitlines()) | set(
        out(root, "diff", "--cached", "--name-only").splitlines())
    overlap = sorted(touched & set(files))
    if not three_way:
        print("Qo'llanmadi, asosiy daraxtga tegilmadi: %s" % gid)
        if overlap:
            print("Kesishgan fayllar (boshqa guruh yoki asosiy daraxt o'zgartirgan):")
            for name in overlap[:15]:
                print("  " + name)
        print("Yo'l: --3way bilan qo'llab, ziddiyatni egasi asosiy daraxtda hal "
              "qiladi; yoki shu guruhni boshqalaridan keyin ketma-ket bajarish.")
        return 1
    applied = git(root, "apply", "--3way", data=patch)
    conflicts = out(root, "diff", "--name-only", "--diff-filter=U").splitlines()
    if applied.returncode or conflicts:
        # Birlashgan deb belgilanmaydi: aks holda tozala guruh ishini
        # ziddiyat hal qilinmasdan o'chirib yuborardi.
        print("Ziddiyat bilan qo'llandi: %s. Hal qilinadigan fayllar:" % gid)
        for name in conflicts or overlap:
            print("  " + name)
        print("Guruh birlashgan hisoblanmaydi. Ziddiyat asosiy daraxtda hal "
              "qilingach: guruh.py tozala %s --majburiy" % gid)
        return 1
    group["merged"] = True
    save(root, data)
    print("Birlashtirildi (3way): %s, %d fayl" % (gid, len(files)))
    return 0


def worktrees(root):
    text = out(root, "worktree", "list", "--porcelain")
    return [line[len("worktree "):] for line in text.splitlines()
            if line.startswith("worktree ")]


def broken(root, gid, group):
    """Holat faylidagi yozuv shu guruhning o'zinikimi. Fayl qo'lda yoki
    boshqa vosita bilan buzilgan bo'lsa o'chirish begona papka yoki
    branch ga tegardi. Sabab qaytadi, hammasi joyida bo'lsa None."""
    if not isinstance(group, dict):
        return "yozuv lug'at emas"
    path, branch = group.get("path"), group.get("branch")
    expected = worktree_path(root, gid)
    if not isinstance(path, str) or not path or not same(path, expected):
        return "yo'l guruhniki emas: %r (kutilgan %s)" % (path, expected)
    if same(path, root):
        return "yo'l repo ildizi: %s" % path
    if not any(same(path, item) for item in worktrees(root)):
        return "yo'l git worktree list da yo'q: %s" % path
    if not isinstance(branch, str) or not BRANCH_RE.match(branch) \
            or branch != "genius/%s" % gid:
        return "branch guruhniki emas: %r" % (branch,)
    if not isinstance(group.get("base"), str):
        return "asos commit yo'q"
    return None


def pending(group):
    """Birlashtirilmagan guruhning o'zgargan fayllari: o'chsa yo'qoladigan ish."""
    if group.get("merged") or not os.path.isdir(group["path"]):
        return []
    return changed(group["path"], group["base"])


def refuse_broken(root, bad):
    print("Holat fayli buzilgan, hech narsa o'chirilmadi (%s):" % state_file(root))
    for gid, reason in bad:
        print("  %s: %s" % (gid, reason))
    return 2


def remove(root, gid, force=False):
    data = load(root)
    group = data.get(gid)
    if not group:
        print("Guruh yo'q: %s" % gid)
        return 1
    reason = broken(root, gid, group)
    if reason:
        return refuse_broken(root, [(gid, reason)])
    path, branch, merged = group["path"], group["branch"], bool(group.get("merged"))
    files = pending(group)
    if files and not force:
        print("Rad etildi: %s birlashtirilmagan, %d fayl o'zgargan:" % (gid, len(files)))
        for name in files[:15]:
            print("  " + name)
        print("Avval birlashtiring; ish kerak bo'lmasa: guruh.py tozala %s --majburiy" % gid)
        return 1
    git(root, "worktree", "remove", "--force", path)
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    git(root, "worktree", "prune")
    # Birlashgan guruhning ishi asosiy daraxtda, branch kerak emas. Aks
    # holda faqat -d: branch da birlashmagan commit bo'lsa u qoladi.
    git(root, "branch", "-D" if merged else "-d", branch)
    data.pop(gid, None)
    save(root, data)
    print("O'chirildi: %s" % gid)
    if out(root, "rev-parse", "--verify", "-q", "refs/heads/" + branch):
        print("Branch qoldi, unda birlashmagan commit bor: %s" % branch)
    return 0


def remove_all(root):
    """Faqat birlashgan yoki o'zgarishsiz guruhlar. Birorta yozuv buzilgan
    bo'lsa hech biri o'chmaydi: holat faylining o'ziga ishonib bo'lmaydi."""
    data = load(root)
    bad = [(gid, broken(root, gid, group)) for gid, group in data.items()]
    bad = [(gid, reason) for gid, reason in bad if reason]
    if bad:
        return refuse_broken(root, bad)
    kept = []
    for gid, group in data.items():
        files = pending(group)
        if files:
            kept.append((gid, len(files)))
        else:
            remove(root, gid)
    if not kept:
        return 0
    print("Qoldirildi, birlashtirilmagan ish bor:")
    for gid, count in kept:
        print("  %s: %d fayl" % (gid, count))
    print("Har birini birlashtiring yoki egasi qarori bilan: guruh.py tozala <id> --majburiy")
    return 1


def listing(root):
    data = load(root)
    if not data:
        print("Faol guruh yo'q. Chegara: %d" % limit())
        return 0
    print("%-14s %-8s %-6s %s" % ("guruh", "holat", "fayl", "papka"))
    for gid, group in data.items():
        exists = os.path.isdir(group["path"])
        count = len(changed(group["path"], group["base"])) if exists else 0
        state = "birlashgan" if group.get("merged") else ("ishda" if exists else "yo'q")
        print("%-14s %-8s %-6d %s" % (gid, state, count, group["path"]))
    print("Chegara: %d" % limit())
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="guruh.py", description=__doc__.split("\n\n")[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("buyruq", choices=["yarat", "royxat", "birlashtir", "tozala"])
    parser.add_argument("id", nargs="?")
    parser.add_argument("--nusxa", action="append", default=[], metavar="FAYL",
                        help="git da yo'q, lekin test uchun kerak fayl (yarat)")
    parser.add_argument("--3way", dest="three_way", action="store_true",
                        help="kesishsa ziddiyat belgilari bilan qo'llash (birlashtir)")
    parser.add_argument("--hammasi", action="store_true",
                        help="birlashgan va o'zgarishsiz hamma guruh (tozala)")
    parser.add_argument("--majburiy", action="store_true",
                        help="birlashtirilmagan ishi bilan o'chirish (tozala <id>)")
    args = parser.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    root = main_root(os.getcwd())
    if root is None:
        print("git repo emas: %s" % os.getcwd())
        return 2
    if args.buyruq == "royxat":
        return listing(root)
    if args.buyruq == "tozala" and args.hammasi:
        if args.majburiy:
            print("--majburiy faqat bitta guruh uchun: guruh.py tozala <id> --majburiy")
            return 2
        return remove_all(root)
    if not args.id or not ID_RE.match(args.id):
        print("guruh nomi kerak: harf yoki raqam bilan boshlanadi, keyin harf, "
              "raqam, nuqta, chiziq (40 gacha)")
        return 2
    if args.buyruq == "yarat":
        return create(root, args.id, args.nusxa)
    if args.buyruq == "birlashtir":
        return merge(root, args.id, args.three_way)
    return remove(root, args.id, args.majburiy)


if __name__ == "__main__":
    sys.exit(main())
