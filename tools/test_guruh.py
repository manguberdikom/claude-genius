#!/usr/bin/env python3
"""guruh.py uchun sinovlar.

    python3 tools/test_guruh.py

Uch va'da sinaladi. Ajratilgan guruhlar asosiy daraxtga yo'qotishsiz
tushadi, yangi fayllar bilan. Kesishgan guruh asosiy daraxtga TEGMAYDI,
`--3way` siz: aks holda yarim qo'llangan patch qolardi. Va chegara:
mashina ko'tara olmaydigan sonda guruh ochilmaydi, chunki shunda hamma
guruh birga sekinlashadi.

Tozalash ish yo'qotmaydi: birlashtirilmagan, kesishgan yoki ziddiyatda
qolgan guruh `tozala --hammasi` dan keyin joyida turadi. Buzilgan holat
fayli (yo'l repo ildizi, begona papka yoki branch) hech narsani
o'chirmaydi. `--nusxa` worktree dan tashqariga chiqmaydi, `yarat` yarim
yo'lda yiqilsa yetim worktree va branch qolmaydi.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "guruh.py")
TEMP = tempfile.mkdtemp(prefix="guruh_")


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd] + list(args), capture_output=True,
                          text=True)


def repo(name):
    root = os.path.join(TEMP, name, "app")
    os.makedirs(root)
    for f in ("a.txt", "b.txt"):
        with open(os.path.join(root, f), "w") as handle:
            handle.write(f + "\n")
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    return root


def run(root, *args, **env):
    environ = dict(os.environ, **env)
    proc = subprocess.run([sys.executable, TOOL] + list(args), cwd=root,
                          capture_output=True, text=True, encoding="utf-8", env=environ)
    return proc.returncode, proc.stdout + proc.stderr


def write(root, name, text):
    with open(os.path.join(root, name), "w") as handle:
        handle.write(text)


def wt(root, gid):
    return os.path.join(os.path.dirname(root), "app.guruh-%s" % gid)


def case_ajratilgan_guruhlar(_):
    root = repo("ajratilgan")
    run(root, "yarat", "g1")
    run(root, "yarat", "g2")
    write(wt(root, "g1"), "a.txt", "a1\n")
    write(wt(root, "g1"), "yangi.txt", "yangi\n")
    write(wt(root, "g2"), "b.txt", "b2\n")
    c1, _ = run(root, "birlashtir", "g1")
    c2, _ = run(root, "birlashtir", "g2")
    status = git(root, "status", "--porcelain").stdout
    return (c1 == 0 and c2 == 0 and "M  a.txt" in status and "M  b.txt" in status
            and "A  yangi.txt" in status)


def case_kesishgan_tegmaydi(_):
    root = repo("kesishgan")
    run(root, "yarat", "g1")
    run(root, "yarat", "g2")
    write(wt(root, "g1"), "a.txt", "a1\n")
    write(wt(root, "g2"), "a.txt", "a2\n")
    run(root, "birlashtir", "g1")
    before = open(os.path.join(root, "a.txt")).read()
    code, out = run(root, "birlashtir", "g2")
    after = open(os.path.join(root, "a.txt")).read()
    return code == 1 and before == after == "a1\n" and "a.txt" in out


def case_3way_ziddiyat(_):
    root = repo("uchyol")
    run(root, "yarat", "g1")
    run(root, "yarat", "g2")
    write(wt(root, "g1"), "a.txt", "a1\n")
    write(wt(root, "g2"), "a.txt", "a2\n")
    run(root, "birlashtir", "g1")
    code, out = run(root, "birlashtir", "g2", "--3way")
    text = open(os.path.join(root, "a.txt")).read()
    # Ziddiyatli guruh birlashgan hisoblanmaydi: tozala uni olmaydi.
    cleaned, _ = run(root, "tozala", "g2")
    return (code == 1 and "<<<<<<<" in text and "a.txt" in out and cleaned == 1
            and os.path.exists(wt(root, "g2")))


def case_iflos_daraxt_rad(_):
    root = repo("iflos")
    write(root, "a.txt", "commit qilinmagan\n")
    code, out = run(root, "yarat", "g1")
    return code == 1 and "ketma-ket" in out and not os.path.exists(wt(root, "g1"))


def case_chegara(_):
    root = repo("chegara")
    first, _ = run(root, "yarat", "g1", GENIUS_GURUH_MAX="1")
    second, out = run(root, "yarat", "g2", GENIUS_GURUH_MAX="1")
    return first == 0 and second == 1 and "chegara 1" in out


def case_guruh_ichidan_chaqiruv(_):
    root = repo("ichidan")
    run(root, "yarat", "g1")
    code, out = run(wt(root, "g1"), "royxat")
    return code == 0 and "g1" in out


def case_tozala(_):
    root = repo("tozala")
    run(root, "yarat", "g1")
    code, _ = run(root, "tozala", "g1")
    branches = git(root, "branch", "--list", "genius/*").stdout
    return code == 0 and not os.path.exists(wt(root, "g1")) and not branches.strip()


def branches(root):
    return git(root, "branch", "--list", "--format=%(refname:short)", "genius/*").stdout.split()


def worktree_count(root):
    return git(root, "worktree", "list", "--porcelain").stdout.count("worktree ")


def case_kesishgan_tozalanmaydi(_):
    root = repo("kesishgan_tozala")
    run(root, "yarat", "g1")
    run(root, "yarat", "g2")
    write(wt(root, "g1"), "a.txt", "a1\n")
    write(wt(root, "g2"), "a.txt", "a2\n")
    write(wt(root, "g2"), "New.java", "class New {}\n")
    c1, _ = run(root, "birlashtir", "g1")
    c2, _ = run(root, "birlashtir", "g2")
    code, out = run(root, "tozala", "--hammasi")
    kept = os.path.join(wt(root, "g2"), "New.java")
    return (c1 == 0 and c2 == 1 and code == 1 and "g2" in out
            and not os.path.exists(wt(root, "g1")) and os.path.exists(kept)
            and open(os.path.join(wt(root, "g2"), "a.txt")).read() == "a2\n"
            and branches(root) == ["genius/g2"])


def case_birlashmagan_saqlanadi(_):
    # Budjeti tugab to'xtagan guruh: birlashtir umuman chaqirilmagan.
    root = repo("birlashmagan")
    run(root, "yarat", "g1")
    write(wt(root, "g1"), "yangi.txt", "ish\n")
    all_code, _ = run(root, "tozala", "--hammasi")
    one_code, out = run(root, "tozala", "g1")
    kept = os.path.exists(os.path.join(wt(root, "g1"), "yangi.txt"))
    forced, _ = run(root, "tozala", "g1", "--majburiy")
    return (all_code == 1 and one_code == 1 and "yangi.txt" in out and kept
            and forced == 0 and not os.path.exists(wt(root, "g1")))


def set_state(root, gid, **fields):
    path = os.path.join(root, ".git", "genius-guruh.json")
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    data[gid].update(fields)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle)


def case_buzilgan_holat(_):
    root = repo("buzilgan")
    git(root, "checkout", "-q", "-b", "ish")
    git(root, "branch", "main")  # checkout qilinmagan main: -D uni o'chira olardi
    victim = os.path.join(os.path.dirname(root), "qurbon")
    os.makedirs(victim)
    write(victim, "muhim.txt", "x\n")
    run(root, "yarat", "g1")
    path = wt(root, "g1")
    codes = []
    set_state(root, "g1", path=root)
    codes.append(run(root, "tozala", "g1")[0])
    set_state(root, "g1", path=victim)
    codes.append(run(root, "tozala", "--hammasi")[0])
    set_state(root, "g1", path=path, branch="main")
    codes.append(run(root, "tozala", "g1")[0])
    codes.append(run(root, "tozala", "--hammasi")[0])
    has_main = git(root, "rev-parse", "--verify", "-q", "refs/heads/main").returncode == 0
    return (codes == [2, 2, 2, 2] and os.path.exists(os.path.join(root, ".git"))
            and os.path.exists(os.path.join(root, "a.txt"))
            and os.path.exists(os.path.join(victim, "muhim.txt"))
            and os.path.exists(path) and has_main and branches(root) == ["genius/g1"])


def case_nusxa_tashqari_rad(_):
    root = repo("nusxa_rad")
    write(os.path.dirname(root), "x", "maxfiy\n")
    rel, _ = run(root, "yarat", "g1", "--nusxa", "../x")
    absolute, _ = run(root, "yarat", "g2", "--nusxa", os.path.join(os.path.dirname(root), "x"))
    dash, _ = run(root, "yarat", "--", "-x")
    return (rel == 2 and absolute == 2 and dash == 2 and worktree_count(root) == 1
            and not branches(root) and not os.path.exists(wt(root, "g1")))


def case_yarat_qaytariladi(_):
    root = repo("qaytar")
    os.makedirs(os.path.join(root, ".git", "genius-guruh.json"))  # save() yiqiladi
    code, out = run(root, "yarat", "g1")
    return (code == 1 and "qaytarildi" in out and worktree_count(root) == 1
            and not branches(root) and not os.path.exists(wt(root, "g1")))


def case_nusxa(_):
    root = repo("nusxa")
    write(root, ".env", "SECRET=x\n")
    with open(os.path.join(root, ".gitignore"), "w") as handle:
        handle.write(".env\n")
    git(root, "add", ".gitignore")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "ignore")
    code, _ = run(root, "yarat", "g1", "--nusxa", ".env")
    return code == 0 and os.path.exists(os.path.join(wt(root, "g1"), ".env"))


def case_ozgarishsiz(_):
    root = repo("bosh")
    run(root, "yarat", "g1")
    code, out = run(root, "birlashtir", "g1")
    return code == 0 and "o'zgarish yo'q" in out


CASES = [
    ("ajratilgan guruhlar yangi fayl bilan tushadi", case_ajratilgan_guruhlar),
    ("kesishgan guruh asosiy daraxtga tegmaydi", case_kesishgan_tegmaydi),
    ("--3way ziddiyat belgisi bilan", case_3way_ziddiyat),
    ("iflos daraxtda guruh ochilmaydi", case_iflos_daraxt_rad),
    ("chegara: GENIUS_GURUH_MAX", case_chegara),
    ("guruh ichidan chaqirilsa ham asosiy daraxt", case_guruh_ichidan_chaqiruv),
    ("tozala: worktree va branch yo'qoladi", case_tozala),
    ("--nusxa git dagi yo'q faylni ko'chiradi", case_nusxa),
    ("o'zgarishsiz guruh", case_ozgarishsiz),
    ("kesishgan ikkinchi guruh tozala --hammasi dan keyin joyida",
     case_kesishgan_tozalanmaydi),
    ("birlashtirilmagan guruh rad, --majburiy bilan o'chadi", case_birlashmagan_saqlanadi),
    ("buzilgan holat fayli: rc=2, hech narsa o'chmaydi", case_buzilgan_holat),
    ("--nusxa ../x va mutlaq yo'l rad, '-' bilan nom rad", case_nusxa_tashqari_rad),
    ("yarat yiqilsa worktree va branch qaytariladi", case_yarat_qaytariladi),
]


def main():
    failures = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(None))
            except Exception as exc:
                ok, name = False, "%s (%s: %s)" % (name, type(exc).__name__, exc)
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", name))
    finally:
        shutil.rmtree(TEMP, ignore_errors=True)
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
