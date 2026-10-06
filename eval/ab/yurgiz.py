#!/usr/bin/env python3
"""A/B runner: har (vazifa, holat, takror) uchun alohida klon, config va sessiya.

    python3 eval/ab/yurgiz.py                       # quruq yurish: reja va buyruqlar
    python3 eval/ab/yurgiz.py --smoke               # smoke rejasi (3 x 2 x 1)
    env -u CLAUDE_CODE_SESSION_ID \\
      python3 eval/ab/yurgiz.py --takror 3 --yurgiz # haqiqiy yurish
    python3 eval/ab/yurgiz.py --sinov               # o'z-o'zini sinash, tarmoqsiz

Sukut rejim QURUQ: hech narsa yaratilmaydi, `claude` chaqirilmaydi, faqat
reja, papkalar, buyruqlar va jami chek chiqadi. Pul faqat `--yurgiz` bilan
sarflanadi.

Har yurish (README, "Avtomatik yurish"):
1. petclinic klonlanadi, vazifa tayyorlovi bajariladi, keyin `.git` qayta
   yaratiladi: bitta "boshlang'ich" commit. Bug vazifasida diff shu commit
   ichida, ya'ni `git diff` va `git status` javobni ko'rsatmaydi (OL-O6).
   Review vazifasida diff commitdan KEYIN qo'llanadi, u ataylab ko'rinadi.
   Tayyor holat `asl/` ga nusxalanadi: baholovchi shu bilan solishtiradi.
2. Alohida CLAUDE_CONFIG_DIR. A: bo'sh config, genius yo'q (OL-O8, KT-K3).
   B: `eval/` va `audit/` papkasiz genius nusxasi (OL-T-M2), uning ichidagi
   manguberdi skilli, olti aktyor va hooklar. Nusxa har yurish uchun
   yangidan olinadi, ya'ni memory git dagi holatda (OL-T-M1).
3. `claude -p --output-format json --max-budget-usd <chek>`. Ruxsat ikki
   holatda bir xil (`--allowedTools` ro'yxati yoki izolyatsiyada
   `bypassPermissions`). `acceptEdits` ishlatilmaydi: print rejimida u
   Bash so'rovlarini rad etadi va `./mvnw` yurmaydi. B da avval
   `/manguberdi`, keyin `--resume` bilan aynan o'sha vazifa prompti.
4. Muhitdan CLAUDE_CODE_SESSION_ID olib tashlanadi (PL-CC10). Runner
   Claude Code sessiyasi ichidan yurgizilsa `--yurgiz` to'xtaydi.
5. baho.py mexanik baho va ifloslanish filtrini beradi, qator
   natijalar.tsv ga yoziladi. Ifloslangan yurish qatori qoladi (iz uchun),
   lekin tahlil.py uni tashlaydi va runner shu katakni qayta yurgizadi.
"""

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import umumiy  # noqa: E402
from umumiy import AKTYORLAR, GENIUS, PETCLINIC_COMMIT, PETCLINIC_URL  # noqa: E402

SMOKE = (1, 3, 8)
# Sessiya ko'radigan genius nusxasidan chiqariladigan papkalar: javob
# kaliti (eval/) va audit topilmalari (unda bug qatorlari aynan yozilgan).
CHIQARILADI = ("eval", "audit")

# Ikkala holatga bir xil ro'yxat. B ning genius asboblari uchun qo'shimcha
# ruxsati o'rnatishning o'zida (settings.json), ya'ni u sinalayotgan
# qatlamning bir qismi.
RUXSAT_ROYXATI = [
    "Read", "Grep", "Glob", "Edit", "Write", "TodoWrite", "Skill", "Task", "Agent",
    "Bash(./mvnw:*)", "Bash(git:*)", "Bash(ls:*)", "Bash(cat:*)", "Bash(grep:*)",
    "Bash(find:*)", "Bash(head:*)", "Bash(tail:*)", "Bash(wc:*)", "Bash(mkdir:*)",
    "Bash(sed -n:*)", "Bash(diff:*)",
]

GIT_ID = ["-c", "user.name=ab-sinov", "-c", "user.email=ab-sinov@localhost",
          "-c", "init.defaultBranch=main", "-c", "commit.gpgsign=false"]


def sh(cmd, cwd=None, env=None, input=None, check=True, timeout=None):
    r = subprocess.run(cmd, cwd=cwd, env=env, input=input, capture_output=True,
                       timeout=timeout)
    if check and r.returncode != 0:
        raise RuntimeError("%s -> %d\n%s" % (shlex.join(map(str, cmd)), r.returncode,
                                            (r.stderr or r.stdout).decode("utf-8", "replace")))
    return r


def git(*args, cwd=None, check=True, input=None):
    return sh(["git", *GIT_ID, *args], cwd=cwd, check=check, input=input)


# ---------------------------------------------------------------- tayyorlov

def petclinic_manba(ish, pc=None, quruq=False):
    """Klon manbasi: berilgan mahalliy repo yoki bir martalik mirror."""
    if pc:
        return Path(pc).resolve()
    kesh = Path(ish) / "kesh" / "spring-petclinic.git"
    if not quruq and not kesh.exists():
        kesh.parent.mkdir(parents=True, exist_ok=True)
        git("clone", "-q", "--mirror", PETCLINIC_URL, str(kesh))
    return kesh


def tayyorla(vazifa, manba, papka, commit=PETCLINIC_COMMIT, diff_papka=None):
    """papka/pc va papka/asl ni yaratadi. Natija: tekshiruv lug'ati.

    `.git` hamma vazifada qayta yaratiladi (bitta commit), shunda tarix
    ham, bug qatori ham `git log`/`git diff` da ko'rinmaydi.
    """
    papka = Path(papka)
    pc = papka / "pc"
    git("clone", "-q", "--no-checkout", str(manba), str(pc))
    git("checkout", "-q", commit, cwd=pc)
    diff = None
    if vazifa.diff:
        diff = Path(diff_papka or umumiy.VAZIFALAR / "diff") / vazifa.diff
    if diff and vazifa.tur != "review":
        git("apply", str(diff), cwd=pc)
    shutil.rmtree(pc / ".git")
    git("init", "-q", cwd=pc)
    git("add", "-A", cwd=pc)
    git("commit", "-qm", "boshlang'ich", cwd=pc)
    git("config", "user.name", "ab-sinov", cwd=pc)
    git("config", "user.email", "ab-sinov@localhost", cwd=pc)
    if diff and vazifa.tur == "review":
        git("apply", str(diff), cwd=pc)
    holat = git("status", "--porcelain", cwd=pc).stdout.decode().splitlines()
    commitlar = git("rev-list", "--count", "HEAD", cwd=pc).stdout.decode().strip()
    tekshiruv = {"status": holat, "commitlar": int(commitlar)}
    if tekshiruv["commitlar"] != 1:
        raise RuntimeError("tayyorlov: commit soni 1 emas: %s" % commitlar)
    if vazifa.tur == "review":
        if not holat:
            raise RuntimeError("tayyorlov: review diffi ko'rinmayapti")
    elif holat:
        raise RuntimeError("tayyorlov: git status bo'sh emas: %s" % holat)
    shutil.copytree(pc, papka / "asl", ignore=shutil.ignore_patterns(".git"),
                    symlinks=True)
    return tekshiruv


def genius_commit(commit="HEAD"):
    return git("rev-parse", commit, cwd=GENIUS).stdout.decode().strip()


def genius_sablon(ish, commit, indeks=True):
    """`eval/` va `audit/` siz genius nusxasi, commit bo'yicha bir marta."""
    sablon = Path(ish) / "genius" / commit[:12]
    belgi = sablon / ".ab-tayyor"
    if belgi.exists():
        return sablon
    if sablon.exists():
        shutil.rmtree(sablon)
    sablon.mkdir(parents=True)
    tar_bytes = git("archive", "--format=tar", commit, cwd=GENIUS).stdout
    with tempfile.TemporaryFile() as tmp:
        tmp.write(tar_bytes)
        tmp.seek(0)
        with tarfile.open(fileobj=tmp) as tar:
            azolar = [m for m in tar.getmembers()
                      if m.name.split("/", 1)[0] not in CHIQARILADI]
            tar.extractall(sablon, members=azolar)
    if indeks:
        sh([sys.executable, "tools/build_index.py"], cwd=sablon)
    belgi.write_text(commit + "\n", encoding="utf-8")
    return sablon


def memory_toza(nusxa, commit):
    """Nusxadagi memory/ aynan commitdagi memory/ mi (git blob sha bo'yicha)."""
    r = git("ls-tree", "-r", commit, "memory", cwd=GENIUS)
    kutilgan = {}
    for qator in r.stdout.decode().splitlines():
        meta, yol = qator.split("\t", 1)
        kutilgan[yol[len("memory/"):]] = meta.split()[2]
    return umumiy.papka_manifest(Path(nusxa) / "memory") == kutilgan


def a_config(config):
    """A: oddiy Claude Code. Skill, aktyor va hook yo'q."""
    config = Path(config)
    config.mkdir(parents=True, exist_ok=True)
    (config / "settings.json").write_text(json.dumps(
        {"env": {"GENIUS_HOOKS": "off"}}, indent=2) + "\n", encoding="utf-8")


def b_config(config, nusxa, python=None):
    """B: manguberdi.ps1 qiladigan o'rnatishning Python dagi teng'i.

    Skill va olti aktyor nusxadan olinadi, yo'llar install/rewrite_paths.py
    bilan mutlaq qilinadi, hook jadvali nusxadagi .claude/settings.json dan
    (o'rnatuvchidagi bilan bir xil jadval, tools/test_rewrite_paths.py
    buni qo'riqlaydi), yo'li esa shu nusxaga bog'lanadi.
    """
    config, nusxa = Path(config), Path(nusxa)
    python = (python or sys.executable).replace("\\", "/")
    root = str(nusxa).replace("\\", "/")
    skill = config / "skills" / "manguberdi"
    agents = config / "agents"
    shutil.copytree(nusxa / ".claude" / "skills" / "manguberdi", skill)
    agents.mkdir(parents=True)
    for aktyor in AKTYORLAR:
        shutil.copy2(nusxa / ".claude" / "agents" / (aktyor + ".md"), agents)
    yozuvchi = [sys.executable, str(nusxa / "install" / "rewrite_paths.py")]
    for papka in (skill, agents):
        sh(yozuvchi + [str(papka), "--root", root, "--python", python, "--bash", "bash"])
        sh(yozuvchi + [str(papka), "--root", root, "--tekshir"])
    allow = json.loads(sh(yozuvchi + [str(config), "--root", root, "--python", python,
                                      "--bash", "bash", "--allow"]).stdout or b"[]")
    # Sinov proyekti ishonchli va izolyatsiyalangan: run_tests opt-in
    # ruxsati ham beriladi, aks holda B aktyorlari print rejimida yiqiladi.
    opt = sh(yozuvchi + [str(config), "--root", root, "--python", python,
                         "--bash", "bash", "--opt-in"]).stdout.decode().strip()
    if opt:
        allow += json.loads(opt)["permissions"]["allow"]
    repo = json.loads((nusxa / ".claude" / "settings.json").read_text(encoding="utf-8"))
    eski = 'python3 "${CLAUDE_PROJECT_DIR}/tools/'
    yangi = '"%s" "%s/tools/' % (python, root)
    hooks = json.loads(json.dumps(repo["hooks"]).replace(
        json.dumps(eski)[1:-1], json.dumps(yangi)[1:-1]))
    if "CLAUDE_PROJECT_DIR" in json.dumps(hooks):
        raise RuntimeError("B hook jadvalida nisbiy yo'l qoldi")
    settings = {
        "env": {"GENIUS_PYTHON": python},
        "permissions": {
            "additionalDirectories": [root + "/docs", root + "/memory"],
            "allow": sorted(set(allow)),
        },
        "hooks": hooks,
    }
    (config / "settings.json").write_text(json.dumps(settings, indent=2, ensure_ascii=False)
                                          + "\n", encoding="utf-8")
    return settings


# ---------------------------------------------------------------- sessiya

def claude_buyruq(prompt, chek, ruxsat="royxat", model=None, resume=None, claude="claude"):
    cmd = [claude, "-p", prompt, "--output-format", "json",
           "--max-budget-usd", "%.2f" % chek]
    if resume:
        cmd += ["--resume", resume]
    if model:
        cmd += ["--model", model]
    if ruxsat == "bypass":
        cmd += ["--permission-mode", "bypassPermissions"]
    else:
        cmd += ["--permission-mode", "default", "--allowedTools", *RUXSAT_ROYXATI]
    return cmd


def qadamlar(vazifa, holat):
    """Sessiyaga beriladigan promptlar ketma-ketligi."""
    if holat == "B":
        return ["/manguberdi", vazifa.prompt]
    return [vazifa.prompt]


def json_oqi(matn):
    """claude -p chiqishi: oxirgi JSON obyekt (oldida ogohlantirish bo'lishi mumkin)."""
    matn = matn.strip()
    try:
        return json.loads(matn)
    except ValueError:
        for qator in reversed(matn.splitlines()):
            qator = qator.strip()
            if qator.startswith("{"):
                try:
                    return json.loads(qator)
                except ValueError:
                    continue
    return {}


def token_soni(natija):
    jami = 0
    mu = natija.get("modelUsage")
    if isinstance(mu, dict) and mu:
        for v in mu.values():
            for k in ("inputTokens", "outputTokens", "cacheReadInputTokens",
                      "cacheCreationInputTokens"):
                jami += int(v.get(k) or 0)
        return jami
    u = natija.get("usage") or {}
    for k in ("input_tokens", "output_tokens", "cache_read_input_tokens",
              "cache_creation_input_tokens"):
        jami += int(u.get(k) or 0)
    return jami


def sessiya(vazifa, holat, papka, chek, ruxsat, model, claude="claude", timeout=3600):
    """Bitta sessiyani yurgizadi. Natija: usd, token, daqiqa, sessiya_id, model."""
    papka = Path(papka)
    env = umumiy.env_toza()
    env["CLAUDE_CONFIG_DIR"] = str(papka / "config")
    if holat == "A":
        env["GENIUS_HOOKS"] = "off"
    else:
        env.pop("GENIUS_HOOKS", None)
    usd = 0.0
    token = 0
    ms = 0
    sid = None
    modellar = set()
    izoh = []
    javob = ""
    boshi = time.time()
    for i, prompt in enumerate(qadamlar(vazifa, holat), 1):
        qoldi = chek - usd
        if qoldi <= 0.05:
            izoh.append("chek tugadi %d-qadamdan oldin" % i)
            break
        cmd = claude_buyruq(prompt, qoldi, ruxsat, model, resume=sid, claude=claude)
        try:
            r = sh(cmd, cwd=papka / "pc", env=env, check=False, timeout=timeout)
            chiqish = r.stdout.decode("utf-8", "replace")
            (papka / ("claude-%d.json" % i)).write_text(chiqish, encoding="utf-8")
            (papka / ("claude-%d.err" % i)).write_bytes(r.stderr)
        except subprocess.TimeoutExpired:
            izoh.append("%d-qadam vaqt chegarasi" % i)
            break
        n = json_oqi(chiqish)
        usd += float(n.get("total_cost_usd") or 0)
        token += token_soni(n)
        ms += int(n.get("duration_ms") or 0)
        modellar.update((n.get("modelUsage") or {}).keys())
        yangi_sid = n.get("session_id")
        if sid and yangi_sid and yangi_sid != sid:
            izoh.append("resume yangi sessiya berdi")
        sid = yangi_sid or sid
        if n.get("is_error") or n.get("subtype", "success") != "success":
            izoh.append("%d-qadam: %s" % (i, n.get("subtype") or "xato rc=%d" % r.returncode))
        javob = n.get("result") or ""
        if not sid:
            izoh.append("%d-qadam: session_id yo'q" % i)
            break
    (papka / "javob.md").write_text(javob, encoding="utf-8")
    daqiqa = (ms / 60000.0) if ms else (time.time() - boshi) / 60.0
    return {
        "sessiya_id": sid or "",
        "usd": round(usd, 4),
        "token": token,
        "daqiqa": round(daqiqa, 1),
        "model": model or "+".join(sorted(modellar)),
        "izoh": izoh,
    }


# ---------------------------------------------------------------- reja

def reja(vazifalar, holatlar, takror):
    """(vazifa, holat, takror) ketma-ketligi. Holat tartibi vazifa faylidan."""
    for k in range(1, takror + 1):
        for v in vazifalar:
            for h in v.tartib:
                if h in holatlar:
                    yield v, h, k


def tayyor_qatorlar(natijalar, commit, model):
    """Ifloslanmagan qatori bor kataklar: ular qayta yurgizilmaydi."""
    bor = set()
    for q in natijalar:
        if q.get("genius_commit") != commit[:12]:
            continue
        if model and q.get("model") != model:
            continue
        if q.get("ifloslangan") == "0":
            bor.add((q.get("vazifa"), q.get("holat"), q.get("takror")))
    return bor


def yurish_papkasi(ish, commit, v, h, k):
    asos = Path(ish) / "yurish" / commit[:12]
    n = 1
    while True:
        p = asos / ("%02d-%s-%d-u%d" % (v.raqam, h, k, n))
        if not p.exists():
            return p
        n += 1


def bitta_yurish(v, h, k, args, manba, sablon, commit, baholovchi=None):
    import baho
    papka = yurish_papkasi(args.ish, commit, v, h, k)
    papka.mkdir(parents=True)
    tayyorla(v, manba, papka, commit=getattr(args, "pc_commit", PETCLINIC_COMMIT),
             diff_papka=getattr(args, "diff_papka", None))
    toza = True
    if h == "B":
        nusxa = papka / "genius"
        shutil.copytree(sablon, nusxa, symlinks=True)
        toza = memory_toza(nusxa, commit)
        if not toza:
            raise RuntimeError("genius nusxasida memory toza emas: %s" % nusxa)
        b_config(papka / "config", nusxa)
        oldin = umumiy.papka_manifest(nusxa / "memory")
    else:
        a_config(papka / "config")
    s = sessiya(v, h, papka, args.chek, args.ruxsat, args.model, claude=args.claude)
    if h == "B":
        keyin = umumiy.papka_manifest(papka / "genius" / "memory")
        ozgargan = sorted(k2 for k2 in set(oldin) | set(keyin) if oldin.get(k2) != keyin.get(k2))
        (papka / "memory-keyin.txt").write_text("\n".join(ozgargan) + "\n", encoding="utf-8")
    b = (baholovchi or baho.baholash)(v, papka, h)
    izoh = s["izoh"] + b["izoh"]
    qator = {
        "vazifa": v.raqam, "holat": h, "takror": k, "sessiya_id": s["sessiya_id"],
        "genius_commit": commit[:12], "model": s["model"],
        "muvaffaqiyat": b["muvaffaqiyat"], "xato_topildi": b.get("xato_topildi", ""),
        "yolgon_topilma": "", "usd": s["usd"], "token": s["token"],
        "daqiqa": s["daqiqa"], "aralashuv": 0, "kor_baho": "",
        "ifloslangan": 1 if b["ifloslanish"] else 0,
        "memory_toza": 1 if toza else 0,
        "izoh": "; ".join(izoh + b["ifloslanish"]),
    }
    (papka / "qator.json").write_text(json.dumps(qator, indent=2, ensure_ascii=False),
                                      encoding="utf-8")
    return qator


def tanlash(args):
    hammasi = umumiy.vazifalar()
    if args.smoke:
        raqamlar = set(SMOKE)
    elif args.vazifa:
        raqamlar = {int(x) for x in args.vazifa.split(",")}
    else:
        raqamlar = {v.raqam for v in hammasi}
    return [v for v in hammasi if v.raqam in raqamlar]


def asosiy(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--vazifa", help="vergul bilan raqamlar, masalan 1,3,8")
    p.add_argument("--smoke", action="store_true", help="vazifa %s, takror 1" % (SMOKE,))
    p.add_argument("--holat", default="A,B")
    p.add_argument("--takror", type=int, default=1)
    p.add_argument("--chek", type=float, default=5.0, help="bitta sessiya uchun USD chek")
    p.add_argument("--jami-chek", type=float, help="butun yurish uchun USD (sukut: chek x yurish)")
    p.add_argument("--model", help="ikkala holatga bir xil --model")
    p.add_argument("--ruxsat", choices=("royxat", "bypass"), default="royxat")
    p.add_argument("--ish", default=os.path.join(os.path.expanduser("~"), "genius-ab"),
                   help="klonlar, config va transkriptlar papkasi (repodan tashqarida)")
    p.add_argument("--pc", help="petclinic manbasi (mahalliy repo), sukut: GitHub mirror")
    p.add_argument("--genius-commit", default="HEAD")
    p.add_argument("--natijalar", default=str(umumiy.NATIJALAR))
    p.add_argument("--claude", default="claude")
    p.add_argument("--yurgiz", action="store_true", help="haqiqiy yurish (pul sarflanadi)")
    p.add_argument("--sinov", action="store_true", help="o'z-o'zini sinash")
    args = p.parse_args(argv)
    if args.sinov:
        return sinov()
    if args.smoke:
        args.takror = 1
    holatlar = [h.strip() for h in args.holat.split(",") if h.strip()]
    vaz = tanlash(args)
    commit = genius_commit(args.genius_commit)
    natijalar = umumiy.natija_oqi(args.natijalar)
    bor = tayyor_qatorlar(natijalar, commit, args.model)
    rejalar = [(v, h, k) for v, h, k in reja(vaz, holatlar, args.takror)
               if (str(v.raqam), h, str(k)) not in bor]
    jami_chek = args.jami_chek if args.jami_chek is not None else args.chek * len(rejalar)

    print("genius commit : %s (B shu commitdan, eval/ va audit/ siz)" % commit[:12])
    print("petclinic     : %s @ %s" % (args.pc or PETCLINIC_URL, PETCLINIC_COMMIT[:12]))
    print("ish papkasi   : %s" % args.ish)
    print("ruxsat        : %s (ikkala holatda bir xil)%s" % (
        args.ruxsat, ": " + " ".join(RUXSAT_ROYXATI) if args.ruxsat == "royxat" else ""))
    print("yurishlar     : %d (tayyori %d), chek %.2f USD/sessiya, jami chek %.2f USD"
          % (len(rejalar), len(bor), args.chek, jami_chek))
    for v, h, k in rejalar:
        print("  %02d %s k=%d  %s" % (v.raqam, h, k, v.fayl.name))
        if not args.yurgiz:
            for i, prompt in enumerate(qadamlar(v, h)):
                cmd = claude_buyruq(prompt if len(prompt) < 40 else "<%s prompti>" % v.fayl.name,
                                    args.chek, args.ruxsat, args.model,
                                    resume="<sessiya_id>" if i else None, claude=args.claude)
                if args.ruxsat == "royxat":
                    cmd = cmd[:cmd.index("--allowedTools") + 1] + ["<RUXSAT>"]
                print("      " + shlex.join(cmd))
    sessiya_ichida = "CLAUDE_CODE_SESSION_ID" in os.environ
    kalit = any(os.environ.get(k) for k in ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN"))
    if not args.yurgiz:
        print("\nQURUQ YURISH: hech narsa yaratilmadi va claude chaqirilmadi.")
        if sessiya_ichida:
            print("Diqqat: CLAUDE_CODE_SESSION_ID bor. Haqiqiy yurish terminaldan: "
                  "env -u CLAUDE_CODE_SESSION_ID python3 eval/ab/yurgiz.py ... --yurgiz")
        if not kalit:
            print("Diqqat: alohida CLAUDE_CONFIG_DIR da login yo'q, ANTHROPIC_API_KEY "
                  "yoki CLAUDE_CODE_OAUTH_TOKEN kerak bo'ladi.")
        return 0

    if sessiya_ichida:
        print("to'xtadi: CLAUDE_CODE_SESSION_ID bor. Runner Claude Code sessiyasi ichidan "
              "emas, terminaldan yurgiziladi: env -u CLAUDE_CODE_SESSION_ID ...", file=sys.stderr)
        return 2
    if not kalit:
        print("to'xtadi: ANTHROPIC_API_KEY yoki CLAUDE_CODE_OAUTH_TOKEN yo'q", file=sys.stderr)
        return 2
    if not shutil.which(args.claude):
        print("to'xtadi: %s topilmadi" % args.claude, file=sys.stderr)
        return 2
    manba = petclinic_manba(args.ish, args.pc)
    sablon = genius_sablon(args.ish, commit)
    sarf = 0.0
    for v, h, k in rejalar:
        if sarf + args.chek > jami_chek + 1e-9:
            print("jami chek: %.2f USD sarflandi, keyingisi chekdan oshadi, to'xtadi" % sarf)
            break
        for urinish in (1, 2):
            qator = bitta_yurish(v, h, k, args, manba, sablon, commit)
            umumiy.natija_yoz(qator, args.natijalar)
            sarf += float(qator["usd"] or 0)
            print("  %02d %s k=%d -> muvaffaqiyat %s, %.2f USD, %s daqiqa%s"
                  % (v.raqam, h, k, qator["muvaffaqiyat"], float(qator["usd"]),
                     qator["daqiqa"], ", IFLOSLANGAN" if qator["ifloslangan"] else ""))
            if not qator["ifloslangan"] or sarf + args.chek > jami_chek + 1e-9:
                break
    print("jami sarf: %.2f USD" % sarf)
    return 0


# ---------------------------------------------------------------- sinov

SOXTA_CLAUDE = r'''#!/usr/bin/env python3
import json, os, sys, uuid, pathlib
assert "CLAUDE_CODE_SESSION_ID" not in os.environ, "ota sessiya id si meros qoldi"
cfg = pathlib.Path(os.environ["CLAUDE_CONFIG_DIR"])
args = sys.argv[1:]
prompt = args[args.index("-p") + 1]
assert "acceptEdits" not in args
sid = args[args.index("--resume") + 1] if "--resume" in args else str(uuid.uuid4())
proj = cfg / "projects" / "-soxta"
proj.mkdir(parents=True, exist_ok=True)
yozuv = []
if prompt == "/manguberdi":
    yozuv.append({"type": "user", "message": {"role": "user",
                  "content": "<command-name>/manguberdi</command-name>"}})
else:
    yozuv.append({"type": "user", "message": {"role": "user", "content": prompt}})
    xulq = os.environ.get("SOXTA_XULQ", "")
    if xulq == "skill":
        yozuv.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": "manguberdi"}}]}})
    if xulq == "kalit":
        yozuv.append({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Read",
             "input": {"file_path": "/x/eval/ab/vazifalar/08-review-kesh.md"}}]}})
with open(proj / (sid + ".jsonl"), "a") as f:
    for y in yozuv:
        f.write(json.dumps(y) + "\n")
javob = os.environ.get("SOXTA_JAVOB", "")
print(json.dumps({"type": "result", "subtype": "success", "is_error": False,
                  "duration_ms": 60000, "num_turns": 3, "result": javob,
                  "session_id": sid, "total_cost_usd": 0.5,
                  "modelUsage": {"claude-sonnet-x": {"inputTokens": 10, "outputTokens": 5,
                                                     "cacheReadInputTokens": 100,
                                                     "cacheCreationInputTokens": 0}}}))
'''


def _soxta_repo(papka):
    """Bitta fayl va bitta diffli kichik git repo: petclinic o'rnida."""
    repo = Path(papka) / "soxta-pc"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "A.java").write_text("class A {\n\tint x = 1;\n}\n", encoding="utf-8")
    git("init", "-q", str(repo))
    git("add", "-A", cwd=repo)
    git("commit", "-qm", "asl", cwd=repo)
    commit = git("rev-parse", "HEAD", cwd=repo).stdout.decode().strip()
    (repo / "src" / "A.java").write_text("class A {\n\tint x = 2;\n}\n", encoding="utf-8")
    diff = git("diff", cwd=repo).stdout
    git("checkout", "-q", "--", ".", cwd=repo)
    dpapka = Path(papka) / "diff"
    dpapka.mkdir()
    (dpapka / "soxta.diff").write_bytes(diff)
    return repo, commit, dpapka


def sinov():
    """Tarmoqsiz va pulsiz: tayyorlov, nusxa, config, buyruq, to'liq zanjir."""
    xato = []

    def tek(shart, nom):
        print(("  ok   " if shart else "  XATO ") + nom)
        if not shart:
            xato.append(nom)

    with tempfile.TemporaryDirectory(prefix="ab-sinov-") as t:
        t = Path(t)
        repo, commit, dpapka = _soxta_repo(t)
        bug = umumiy.Vazifa(1, Path("01-x.md"), "bug", "tuzat", "soxta.diff", "A")
        rev = umumiy.Vazifa(8, Path("08-x.md"), "review", "review qil", "soxta.diff", "B")
        oddiy = umumiy.Vazifa(4, Path("04-x.md"), "refaktoring", "qayta yoz", None, "B")

        # 1. Tayyorlov (OL-O6)
        tk = tayyorla(bug, repo, t / "bug", commit, dpapka)
        pc = t / "bug" / "pc"
        tek(tk["status"] == [] and tk["commitlar"] == 1, "bug: git status bo'sh, 1 commit")
        tek("x = 2" in (pc / "src" / "A.java").read_text(), "bug: diff ishchi daraxtda")
        tek(git("diff", "HEAD", cwd=pc).stdout == b"", "bug: git diff HEAD javobni ko'rsatmaydi")
        tek("x = 2" in git("show", "HEAD:src/A.java", cwd=pc).stdout.decode(),
            "bug: diff boshlang'ich commit ichida")
        tek((t / "bug" / "asl" / "src" / "A.java").read_text() == (pc / "src" / "A.java").read_text()
            and not (t / "bug" / "asl" / ".git").exists(), "bug: asl/ nusxasi, .git siz")
        tk = tayyorla(rev, repo, t / "rev", commit, dpapka)
        tek(tk["commitlar"] == 1 and tk["status"] == [" M src/A.java"],
            "review: diff commitdan keyin, git status da ko'rinadi")
        tk = tayyorla(oddiy, repo, t / "oddiy", commit, dpapka)
        tek(tk["status"] == [] and tk["commitlar"] == 1, "diffsiz vazifa: toza, 1 commit")

        # 2. Genius nusxasi (OL-T-M2, OL-T-M1)
        gc = genius_commit("HEAD")
        sablon = genius_sablon(t / "ish", gc, indeks=False)
        tek(not (sablon / "eval").exists() and not (sablon / "audit").exists(),
            "genius nusxasida eval/ va audit/ yo'q")
        tek((sablon / "tools" / "doc.sh").exists() and (sablon / "docs").is_dir(),
            "genius nusxasida tools/ va docs/ bor")
        tek(memory_toza(sablon, gc), "memory commitdagi holatda (memory_toza=1)")
        nusxa = t / "nusxa"
        shutil.copytree(sablon, nusxa, symlinks=True)
        (nusxa / "memory" / "claude-genius" / "soxta_yozuv.md").write_text("x", encoding="utf-8")
        tek(not memory_toza(nusxa, gc), "memoryga yozilgan fayl memory_toza=0 beradi")

        # 3. Config (OL-O8)
        a_config(t / "cfgA")
        tek(not (t / "cfgA" / "skills").exists() and not (t / "cfgA" / "agents").exists(),
            "A config: skill va aktyor yo'q")
        s = b_config(t / "cfgB", sablon, python="/usr/bin/python3")
        tek((t / "cfgB" / "skills" / "manguberdi" / "SKILL.md").exists(), "B config: manguberdi skilli")
        tek(sorted(p.stem for p in (t / "cfgB" / "agents").glob("*.md")) == sorted(AKTYORLAR),
            "B config: olti aktyor")
        hj = json.dumps(s["hooks"])
        tek("CLAUDE_PROJECT_DIR" not in hj and str(sablon).replace("\\", "/") + "/tools/" in hj,
            "B hooklari nusxaga mutlaq bog'langan")
        tek(any("rules_for.py" in r for r in s["permissions"]["allow"])
            and any("run_tests.py" in r for r in s["permissions"]["allow"]),
            "B ruxsati: rules_for va run_tests (opt-in)")
        skill_matn = (t / "cfgB" / "skills" / "manguberdi" / "SKILL.md").read_text(encoding="utf-8")
        tek("python3 tools/" not in skill_matn, "B skill matnida nisbiy yo'l qolmagan")

        # 4. Buyruq
        a = claude_buyruq("p", 5, "royxat")
        b = claude_buyruq("p", 5, "royxat", resume="s1")
        tek("--output-format" in a and a[a.index("--output-format") + 1] == "json"
            and "--max-budget-usd" in a, "buyruq: json va --max-budget-usd")
        tek(a[a.index("--allowedTools"):] == b[b.index("--allowedTools"):],
            "ruxsat ro'yxati A va B da bir xil")
        tek("acceptEdits" not in a + b + claude_buyruq("p", 5, "bypass"), "acceptEdits yo'q")
        tek(qadamlar(rev, "B") == ["/manguberdi", "review qil"] and qadamlar(rev, "A") == ["review qil"],
            "B: avval /manguberdi, keyin aynan o'sha prompt")
        e = umumiy.env_toza({"CLAUDE_CODE_SESSION_ID": "x", "PATH": "/bin", "CLAUDECODE": "1"})
        tek("CLAUDE_CODE_SESSION_ID" not in e and "CLAUDECODE" not in e and e["PATH"] == "/bin",
            "muhit: CLAUDE_CODE_SESSION_ID olib tashlanadi (PL-CC10)")
        tek(list(reja([bug, rev], ["A", "B"], 2))[:4] ==
            [(bug, "A", 1), (bug, "B", 1), (rev, "B", 1), (rev, "A", 1)],
            "reja: holat tartibi vazifa faylidan")
        hammasi = umumiy.vazifalar()
        tek(len(hammasi) == 10 and all(v.prompt for v in hammasi), "10 vazifa va prompt o'qildi")
        tek([v.diff for v in hammasi if v.diff] ==
            ["bug-1.diff", "bug-2.diff", "bug-3.diff", "review-1.diff", "review-2.diff"],
            "diffli vazifalar: 1, 2, 3, 8, 9")

        # 5. To'liq zanjir soxta claude bilan
        claude = t / "soxta-claude"
        claude.write_text(SOXTA_CLAUDE, encoding="utf-8")
        claude.chmod(0o755)
        rev8 = umumiy.Vazifa(8, Path("08-x.md"), "review", "review qil", "soxta.diff", "B")
        tsv = t / "natijalar.tsv"
        args = argparse.Namespace(ish=str(t / "ish"), chek=2.0, ruxsat="royxat", model=None,
                                  claude=str(claude), diff_papka=str(dpapka),
                                  pc_commit=commit)
        oz = os.environ.copy()
        os.environ["CLAUDE_CODE_SESSION_ID"] = "ota-sessiya"
        try:
            os.environ["SOXTA_JAVOB"] = ""
            os.environ["SOXTA_XULQ"] = ""
            qA = bitta_yurish(rev8, "A", 1, args, repo, sablon, gc,
                              baholovchi=_soxta_baholovchi)
            os.environ["SOXTA_XULQ"] = "skill"
            qA2 = bitta_yurish(rev8, "A", 1, args, repo, sablon, gc,
                               baholovchi=_soxta_baholovchi)
            os.environ["SOXTA_XULQ"] = ""
            qB = bitta_yurish(rev8, "B", 1, args, repo, sablon, gc,
                              baholovchi=_soxta_baholovchi)
            os.environ["SOXTA_XULQ"] = "kalit"
            qB2 = bitta_yurish(rev8, "B", 2, args, repo, sablon, gc,
                               baholovchi=_soxta_baholovchi)
        finally:
            os.environ.clear()
            os.environ.update(oz)
        tek(qA["ifloslangan"] == 0 and qA["usd"] == 0.5 and qA["daqiqa"] == 1.0,
            "A toza: usd va daqiqa JSON dan")
        tek(qA2["ifloslangan"] == 1 and "manguberdi" in qA2["izoh"],
            "A da Skill(manguberdi) -> ifloslangan")
        tek(qB["ifloslangan"] == 0 and qB["usd"] == 1.0 and qB["memory_toza"] == 1,
            "B: ikki qadam (/manguberdi + --resume), usd yig'ildi, memory toza")
        tek(qB2["ifloslangan"] == 1 and "eval/ab" in qB2["izoh"], "eval/ab yo'li -> ifloslangan")
        for q in (qA, qA2, qB, qB2):
            umumiy.natija_yoz(q, tsv)
        qatorlar = umumiy.natija_oqi(tsv)
        tek(len(qatorlar) == 4 and list(qatorlar[0].keys()) == umumiy.USTUNLAR,
            "natijalar.tsv: sarlavha va 4 qator")
        tek(tayyor_qatorlar(qatorlar, gc, None) == {("8", "A", "1"), ("8", "B", "1")},
            "faqat ifloslanmagan katak tayyor hisoblanadi (B k=2 qayta yuradi)")
        tek(yurish_papkasi(t / "ish", gc, rev8, "A", 1).name == "08-A-1-u3",
            "qayta urinish yangi papkada")

    print("yurgiz --sinov: %s" % ("hammasi o'tdi" if not xato else "%d XATO" % len(xato)))
    return 1 if xato else 0


def _soxta_baholovchi(v, papka, holat):
    """Sinov uchun: Maven siz, faqat ifloslanish filtri haqiqiy."""
    import baho
    return {"muvaffaqiyat": 0, "xato_topildi": "", "izoh": [],
            "ifloslanish": baho.ifloslanish(papka / "config", holat)}


if __name__ == "__main__":
    sys.exit(asosiy())
