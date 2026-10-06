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

Asos joriy holat: untracked REJA.md va oldingi partiyaning indeksdagi
natijasi guruhga tushadi, asosiy branch va indeks o'zgarmaydi. Worktree
`<root>/.claude/worktrees/genius-<id>` da, `info/exclude` orqali
yashiriladi va ikkinchi guruh ham ochiladi. `royxat --fayllar` har
guruhning fayllarini beradi.
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
sys.path.insert(0, HERE)
import testkit  # noqa: E402


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
    return os.path.join(root, ".claude", "worktrees", "genius-%s" % gid)


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


def read(root, name):
    with open(os.path.join(root, name), encoding="utf-8") as handle:
        return handle.read()


def case_reja_untracked(_):
    # Rejalashtiruvchi REJA.md ni commit qilmaydi; asosiy daraxtda yana
    # commit qilinmagan tahrir bor. Ikkalasi guruhga tushadi, asosiy
    # branch, indeks va daraxt esa o'zgarmaydi.
    root = repo("reja")
    write(root, "REJA.md", "1. orders\n")
    write(root, "a.txt", "commit qilinmagan\n")
    head = git(root, "rev-parse", "HEAD").stdout
    before = git(root, "status", "--porcelain").stdout
    code, out = run(root, "yarat", "g1")
    path = wt(root, "g1")
    ok_tree = (os.path.isfile(os.path.join(path, "REJA.md"))
               and read(path, "a.txt") == "commit qilinmagan\n")
    write(path, "b.txt", "b1\n")
    merged, _ = run(root, "birlashtir", "g1")
    status = git(root, "status", "--porcelain").stdout
    return [("yarat rc=0", code == 0 and "Asos:" in out),
            ("worktree da REJA.md va commit qilinmagan tahrir", ok_tree),
            ("asosiy HEAD va holat o'zgarmadi",
             git(root, "rev-parse", "HEAD").stdout == head
             and before == git(root, "status", "--porcelain").stdout.replace(
                 "M  b.txt\n", "")),
            ("birlashtir faqat guruh o'zgarishini qo'llaydi",
             merged == 0 and "M  b.txt" in status and "REJA.md" not in status.replace(
                 "?? REJA.md", "") and read(root, "a.txt") == "commit qilinmagan\n")]


def case_ikkinchi_partiya(_):
    # 1-partiya birlashtirilib tozalangan, natijasi indeksda, commit yo'q.
    # 2-partiya shu natija ustidan boshlanadi va faqat o'zinikini qo'llaydi.
    root = repo("partiya")
    run(root, "yarat", "p1")
    write(wt(root, "p1"), "a.txt", "p1\n")
    write(wt(root, "p1"), "yangi.txt", "p1\n")
    run(root, "birlashtir", "p1")
    cleaned, _ = run(root, "tozala", "p1")
    code, _ = run(root, "yarat", "p2")
    path = wt(root, "p2")
    sees = read(path, "a.txt") == "p1\n" and os.path.isfile(os.path.join(path, "yangi.txt"))
    write(path, "b.txt", "p2\n")
    files_before = run(root, "royxat", "--fayllar")[1]
    merged, out = run(root, "birlashtir", "p2")
    status = git(root, "status", "--porcelain").stdout
    return [("1-partiya tozalandi, 2-partiya yarat rc=0", cleaned == 0 and code == 0),
            ("2-partiya 1-partiya natijasini ko'radi", sees),
            ("2-partiya diffi faqat b.txt", "b.txt" in files_before
             and "a.txt" not in files_before and "yangi.txt" not in files_before),
            ("birlashtir: uchala fayl indeksda", merged == 0 and "1 fayl" in out
             and "M  a.txt" in status and "A  yangi.txt" in status
             and "M  b.txt" in status)]


def case_ichki_papka_exclude(_):
    root = repo("ichki")
    c1, _ = run(root, "yarat", "g1")
    c2, _ = run(root, "yarat", "g2")
    run(root, "yarat", "g3", GENIUS_GURUH_MAX="9")
    exclude = read(os.path.join(root, ".git", "info"), "exclude")
    status = git(root, "status", "--porcelain", "--untracked-files=all").stdout
    # Ikkinchi guruh asosiga birinchisining papkasi tushmagan.
    nested = git(wt(root, "g2"), "ls-files", ".claude").stdout
    return [("ikki guruh ichki papkada ochildi", c1 == 0 and c2 == 0
             and os.path.isdir(wt(root, "g1")) and os.path.isdir(wt(root, "g2"))),
            ("info/exclude da bir marta", exclude.count(".claude/worktrees/") == 1),
            (".gitignore yaratilmadi", not os.path.exists(os.path.join(root, ".gitignore"))),
            ("asosiy daraxt toza", status == ""),
            ("guruh asosida boshqa worktree yo'q", nested == "")]


def case_royxat_fayllar(_):
    root = repo("royxat")
    run(root, "yarat", "g1")
    run(root, "yarat", "g2")
    write(wt(root, "g1"), "a.txt", "a1\n")
    write(wt(root, "g1"), "OrderTest.java", "class OrderTest {}\n")
    write(wt(root, "g2"), "b.txt", "b2\n")
    run(root, "birlashtir", "g1")
    state = json.load(open(os.path.join(root, ".git", "genius-guruh.json"), encoding="utf-8"))
    # Birlashgan guruh fayllari holat faylidan: worktree o'zgarsa ham shu.
    write(wt(root, "g1"), "keyin.txt", "x\n")
    code, out = run(root, "royxat", "--fayllar")
    plain = run(root, "royxat")[1]
    blocks = out.split("\ng2")
    return [("birlashtir holatga files yozdi",
             sorted(state["g1"].get("files", [])) == ["OrderTest.java", "a.txt"]),
            ("--fayllar har guruh ostida", code == 0 and len(blocks) == 2
             and "    OrderTest.java" in blocks[0] and "    a.txt" in blocks[0]
             and "keyin.txt" not in out and "    b.txt" in blocks[1]),
            ("--fayllar siz nomlar yo'q", "OrderTest.java" not in plain)]


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
    ("untracked REJA.md va commit qilinmagan tahrir bilan yarat", case_reja_untracked),
    ("birlashtirilgan partiyadan keyingi ikkinchi partiya", case_ikkinchi_partiya),
    ("ikki guruh ichki papkada, info/exclude", case_ichki_papka_exclude),
    ("royxat --fayllar", case_royxat_fayllar),
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


def main(argv=()):
    try:
        return testkit.run_cases([(name, lambda fn=fn: fn(None)) for name, fn in CASES],
                                 argv)
    finally:
        shutil.rmtree(TEMP, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
