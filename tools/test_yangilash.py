#!/usr/bin/env python3
"""tools/yangilash.py va snapshot (install/snapshot.py) uchun sinovlar (R7.8, XV-Y1).

    python3 tools/test_yangilash.py
    python3 tools/test_yangilash.py -k tasdiq

Haqiqiy ~/.claude ga va ishchi daraxtning o'ziga (uning .git/worktrees iga)
tegilmaydi: har sahna vaqtinchalik HOME, bare origin va ikki klon (o'rnatiladigan
`klon` va origin ga yangi commit push qiladigan `dev`) bilan yuradi. Klonlar
ishchi daraxt nusxasidan yasaladi (testkit.repo_nusxa), shuning uchun hali
commit qilinmagan o'zgarishlar ham sinaladi.

Sahnalar qimmat (har o'rnatish indeks yasaydi), shuning uchun har biri bir
marta yuradi va holatlar uning natijasini tekshiradi:

- pin:   o'rnatish snapshot yasaydi; klonda yangi commit va `git pull` dan keyin
         hook ishlatayotgan fayl SHA-256 o'zgarmaydi (XV-Y1 o'lchovi);
         --faqat-korsat va rad etish hech narsa o'zgartirmaydi; --ha yangi snapshot;
- ff:    so'rovga `y`: ff-merge, yangi snapshot, settings yangilangan, eski bittasi
         qoladi; keyingi yangilashda eng eskisi `git worktree remove` bilan ketadi;
- stop:  iflos klon, detached HEAD va ajralgan tarix da to'xtaydi, hech narsa o'zgarmaydi;
- yozish: memory va holat klonga tushadi, snapshotga emas.
"""

import atexit
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "install"))

import testkit  # noqa: E402
import test_install as TI  # noqa: E402
import snapshot as SNAP  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "yangilash_py", os.path.join(HERE, "yangilash.py"))
Y = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(Y)

POSIX = os.name != "nt"
SKIP = [("o'tkazildi: Windows da install.py yo'q (ps1 ishlaydi)", True)]

_TMP = []
_TEMPLATE = []
_SAHNA = {}


def tmpdir(prefix="yang_"):
    path = tempfile.mkdtemp(prefix=prefix)
    _TMP.append(path)
    return path


@atexit.register
def _cleanup():
    for path in _TMP:
        shutil.rmtree(path, ignore_errors=True)


def template():
    """Bare shablon repo (bir marta): har sahna undan o'z origin ini klonlaydi."""
    if not _TEMPLATE:
        base = tmpdir("shablon_")
        seed = testkit.repo_nusxa(ROOT, os.path.join(base, "seed"))
        bare = os.path.join(base, "shablon.git")
        testkit.git(base, "clone", "-q", "--bare", seed, bare)
        _TEMPLATE.append(bare)
    return _TEMPLATE[0]


class Sahna(object):
    """Bare origin, o'rnatilgan klon, dev klon va o'rnatilgan HOME."""

    def __init__(self):
        self.base = tmpdir()
        self.origin, self.klon, self.dev = testkit.origin_va_klonlar(template(), self.base)
        self.home = os.path.join(self.base, "uy")
        self.claude = os.path.join(self.home, ".claude")
        os.makedirs(self.home)
        self.count = 0
        self.install = TI.run_install(
            self.home, "--apply", "--genius-path", self.klon,
            "--backup-to", os.path.join(self.home, "zaxira-0"))
        self.head0 = testkit.git(self.klon, "rev-parse", "HEAD")
        self.snap0 = os.path.join(self.claude, "genius", self.head0[:12])

    def settings_path(self):
        return os.path.join(self.claude, "settings.json")

    def settings_bytes(self):
        with open(self.settings_path(), "rb") as handle:
            return handle.read()

    def manifest(self):
        return TI.jget(os.path.join(self.claude, "skills", "manguberdi", ".genius.json"))

    def commands(self):
        return TI.commands_of(TI.jget(self.settings_path()))

    def snapshots(self):
        base = os.path.join(self.claude, "genius")
        return sorted(os.listdir(base)) if os.path.isdir(base) else []

    def worktrees(self):
        return testkit.git(self.klon, "worktree", "list").splitlines()

    def state(self):
        """Hech narsa o'zgarmaganini ko'rsatadigan to'liq holat."""
        manifest = os.path.join(self.claude, "skills", "manguberdi", ".genius.json")
        with open(manifest, "rb") as handle:
            manifest_bytes = handle.read()
        return (testkit.git(self.klon, "rev-parse", "HEAD"),
                testkit.git(self.klon, "status", "--porcelain"),
                self.settings_bytes(), manifest_bytes, self.snapshots(),
                self.worktrees(), sorted(os.listdir(self.home)))

    def dev_commit(self, rel="tools/guard.py"):
        """dev da bitta tools/ fayliga qator qo'shib origin ga push qiladi."""
        self.count += 1
        path = os.path.join(self.dev, *rel.split("/"))
        with io.open(path, "a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n# yangilash sinovi %d\n" % self.count)
        testkit.git(self.dev, "commit", "-q", "-am", "yangi %d: %s" % (self.count, rel))
        testkit.git(self.dev, "push", "-q", "origin", "main")
        return testkit.git(self.dev, "rev-parse", "HEAD")

    def run(self, *args, **kwargs):
        """yangilash.main() ni shu HOME bilan jarayon ichida yurgizadi.

        Skript ishchi daraxtdan (klondan) yurgani uchun `--klondan` beriladi;
        snapshotdan yurish va uning rad etilishi alohida holatlarda."""
        extra = [] if kwargs.get("klondan") is False else ["--klondan"]
        return testkit.call_main(
            Y.main, argv=["yangilash.py", "--klon", self.klon] + extra + list(args),
            stdin=kwargs.get("stdin", ""),
            env={"HOME": self.home, "CLAUDE_CONFIG_DIR": None})


def run_script(s, script, *args, **env):
    """Skriptni alohida jarayonda yurgizadi: hook jarayoni muhiti (GENIUS_CLONE) bilan."""
    environ = dict(os.environ, HOME=s.home, GENIUS_CLONE=s.klon, PYTHONIOENCODING="utf-8")
    environ.pop("CLAUDE_CONFIG_DIR", None)
    environ.update(env)
    return subprocess.run([sys.executable, script] + list(args), cwd=s.home, env=environ,
                          stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")


def sahna(name):
    if name not in _SAHNA:
        _SAHNA[name] = Sahna()
    return _SAHNA[name]


def tools_hashes(folder):
    """{fayl: sha256} papkadagi *.py (XV-Y1: sha256sum snapshot/tools/*.py)."""
    out = {}
    tools = os.path.join(folder, "tools")
    for name in sorted(os.listdir(tools)):
        if name.endswith(".py"):
            with open(os.path.join(tools, name), "rb") as handle:
                out[name] = hashlib.sha256(handle.read()).hexdigest()
    return out


def hooks_point_to(cmds, snap):
    own = [c for c in cmds if "begona" not in c]
    return len(own) >= 8 and all((snap + "/tools/") in c for c in own)


# --- pin: o'rnatish snapshot yasaydi, pull hook faylini o'zgartirmaydi ----------

def pin():
    """Sahna `pin` ketma-ketligi (bir marta)."""
    if "pin_natija" in _SAHNA:
        return _SAHNA["pin_natija"]
    s = sahna("pin")
    r = {"s": s, "install_ok": s.install.returncode == 0}
    r["hashes_before"] = tools_hashes(s.snap0)
    r["cmds_before"] = s.commands()
    r["new_sha"] = s.dev_commit("tools/guard.py")
    testkit.git(s.klon, "pull", "-q", "--ff-only")          # XV-Y1: "git pull"
    r["hashes_after"] = tools_hashes(s.snap0)
    r["clone_guard_differs"] = tools_hashes(s.klon)["guard.py"] != r["hashes_before"]["guard.py"]
    r["cmds_after_pull"] = s.commands()
    r["state_pull"] = s.state()

    r["korsat"] = s.run("--faqat-korsat")
    r["korsat_same"] = r["state_pull"] == s.state()
    r["rad_bosh"] = s.run(stdin="")
    r["rad_bosh_same"] = r["state_pull"] == s.state()
    r["rad_n"] = s.run(stdin="n\n")
    r["rad_n_same"] = r["state_pull"] == s.state()

    r["ha"] = s.run("--ha")
    r["manifest"] = s.manifest()
    r["cmds_ha"] = s.commands()
    r["snapshots_ha"] = s.snapshots()
    r["worktrees_ha"] = s.worktrees()
    r["head_ha"] = testkit.git(s.klon, "rev-parse", "HEAD")
    r["new_hashes"] = tools_hashes(os.path.join(s.claude, "genius", r["head_ha"][:12]))
    r["old_hashes_ha"] = tools_hashes(s.snap0)
    _SAHNA["pin_natija"] = r
    return r


def case_ornatish_snapshot_yasaydi():
    if not POSIX:
        return SKIP
    r = pin()
    s = r["s"]
    return [
        ("o'rnatish: rc 0 va snapshot detached worktree",
         r["install_ok"] and any(line.startswith(s.snap0) and "detached HEAD" in line
                                 for line in r["state_pull"][5])),
        ("o'rnatish: hook buyruqlari snapshotga ishora qiladi, klonga emas",
         hooks_point_to(r["cmds_before"], s.snap0)
         and not any((s.klon + "/tools/") in c for c in r["cmds_before"])),
        ("o'rnatish: snapshotda indeks va klonda yo'q",
         os.path.isfile(os.path.join(s.snap0, "index", "sections.tsv"))
         and not os.path.exists(os.path.join(s.klon, "index"))),
    ]


def case_pull_hook_faylini_ozgartirmaydi():
    """XV-Y1 o'lchovi: klonda yangi commit va `git pull` dan keyin
    `sha256sum <snapshot>/tools/*.py` bir xil, klonning o'zida esa fayl o'zgargan."""
    if not POSIX:
        return SKIP
    r = pin()
    return [
        ("pull: snapshot tools/*.py SHA-256 o'zgarmadi",
         r["hashes_before"] == r["hashes_after"] and len(r["hashes_before"]) > 20),
        ("pull: klonning guard.py i o'zgargan (pull ishladi)", r["clone_guard_differs"]),
        ("pull: settings.json hooklari hamon eski snapshotda",
         r["cmds_before"] == r["cmds_after_pull"]),
    ]


def case_faqat_korsat_hech_narsa_ozgartirmaydi():
    if not POSIX:
        return SKIP
    r = pin()
    out = r["korsat"].stdout
    return [
        ("--faqat-korsat: rc 0, hech narsa o'zgarmadi (HEAD, status, settings, manifest, "
         "snapshotlar, worktree, uy)", r["korsat"].returncode == 0 and r["korsat_same"]),
        ("--faqat-korsat: yangi commit va tools/guard.py diff ko'rsatildi",
         "yangi 1: tools/guard.py" in out and "tools/guard.py" in out
         and "O'rnatilgan snapshot: %s" % r["s"].head0[:12] in out),
        ("--faqat-korsat: snapshot klon HEAD dan farq qilishi aytildi",
         "farq qiladi" in out and "--faqat-korsat: hech narsa o'zgarmadi" in out),
    ]


def case_rad_etishda_ozgarmaydi():
    if not POSIX:
        return SKIP
    r = pin()
    return [
        ("rad: bo'sh stdin (CI, agent) 'yo'q' deb olinadi, o'zgarmadi",
         r["rad_bosh"].returncode == 0 and r["rad_bosh_same"]
         and "Rad etildi" in r["rad_bosh"].stdout + "Rad etildi"),
        ("rad: `n` javobi, rc 0, o'zgarmadi, 'Rad etildi' aytildi",
         r["rad_n"].returncode == 0 and r["rad_n_same"] and "Rad etildi" in r["rad_n"].stdout),
    ]


def case_ha_yangi_snapshot_eski_qoladi():
    """--ha: klon allaqachon origin da (qo'lda pull), lekin snapshot eski: yangi
    snapshot, settings yangilanadi, eski bittasi qoladi."""
    if not POSIX:
        return SKIP
    r = pin()
    s = r["s"]
    new_snap = os.path.join(s.claude, "genius", r["head_ha"][:12])
    return [
        ("--ha: rc 0, yangi snapshot klon HEAD da", r["ha"].returncode == 0
         and r["head_ha"] == r["new_sha"] and os.path.isdir(new_snap)),
        ("--ha: manifest yangi snapshotga o'tdi (root, commit), clone o'sha",
         r["manifest"]["root"] == new_snap and r["manifest"]["commit"] == r["new_sha"]
         and r["manifest"]["clone"] == s.klon),
        ("--ha: settings.json hooklari yangi snapshotga, eskisiga yo'q",
         hooks_point_to(r["cmds_ha"], new_snap)
         and not any(s.snap0 in c for c in r["cmds_ha"])),
        ("--ha: eski snapshot qaytarish uchun qoldi, o'zgarmagan",
         os.path.isdir(s.snap0) and r["old_hashes_ha"] == r["hashes_before"]
         and sorted(r["snapshots_ha"]) == sorted([s.head0[:12], r["head_ha"][:12]])),
        ("--ha: yangi snapshotda yangi kod (guard.py farq qiladi)",
         r["new_hashes"]["guard.py"] != r["hashes_before"]["guard.py"]),
        ("--ha: so'ralmadi va ro'yxat chiqdi",
         "--ha berilgan" in r["ha"].stdout and "Yangi commitlar" in r["ha"].stdout),
    ]


# --- ff: tasdiq bilan merge --ff-only, tozalash --------------------------------

def ff():
    if "ff_natija" in _SAHNA:
        return _SAHNA["ff_natija"]
    s = sahna("ff")
    r = {"s": s, "install_ok": s.install.returncode == 0}
    r["snap_a"] = s.snap0
    r["b"] = s.dev_commit("tools/budget.py")
    r["head_before"] = testkit.git(s.klon, "rev-parse", "HEAD")
    r["yes"] = s.run(stdin="y\n")
    r["head_b"] = testkit.git(s.klon, "rev-parse", "HEAD")
    r["manifest_b"] = s.manifest()
    r["cmds_b"] = s.commands()
    r["snaps_b"] = s.snapshots()
    r["worktrees_b"] = s.worktrees()
    r["snap_b"] = os.path.join(s.claude, "genius", r["head_b"][:12])
    r["a_exists_b"] = os.path.isdir(r["snap_a"])
    r["backups"] = sorted(n for n in os.listdir(s.home) if n.startswith(".claude-backup"))

    r["c"] = s.dev_commit("tools/usage.py")
    r["ha"] = s.run("--ha")
    r["head_c"] = testkit.git(s.klon, "rev-parse", "HEAD")
    r["snap_c"] = os.path.join(s.claude, "genius", r["head_c"][:12])
    r["manifest_c"] = s.manifest()
    r["cmds_c"] = s.commands()
    r["snaps_c"] = s.snapshots()
    r["worktrees_c"] = s.worktrees()

    before = s.state()
    r["yangi_yoq"] = s.run("--ha")
    r["yangi_yoq_same"] = before == s.state()
    _SAHNA["ff_natija"] = r
    return r


def case_tasdiq_ff_merge_va_yangi_snapshot():
    if not POSIX:
        return SKIP
    r = ff()
    out = r["yes"].stdout
    return [
        ("tasdiq: rc 0, klon origin ga ff-merge qilindi",
         r["yes"].returncode == 0 and r["head_before"] != r["b"] and r["head_b"] == r["b"]
         and "git merge --ff-only origin/main" in out),
        ("tasdiq: ro'yxat tasdiqdan oldin chiqdi (commit va hook fayli diff)",
         out.index("Yangi commitlar") < out.index("git merge --ff-only")
         and "tools/budget.py" in out),
        ("tasdiq: yangi snapshot, manifest va settings.json yangilandi",
         os.path.isdir(r["snap_b"]) and r["manifest_b"]["root"] == r["snap_b"]
         and r["manifest_b"]["commit"] == r["b"] and hooks_point_to(r["cmds_b"], r["snap_b"])
         and not any(r["snap_a"] in c for c in r["cmds_b"])),
        ("tasdiq: eski snapshot bittasi qaytarish uchun qoldi",
         r["a_exists_b"] and len(r["snaps_b"]) == 2
         and len(r["worktrees_b"]) == 3
         and "Qaytarish uchun eski snapshot qoldi" in out),
        ("tasdiq: o'rnatuvchi zaxira oldi", len(r["backups"]) >= 1),
    ]


def case_keyingi_yangilashda_eng_eskisi_tozalanadi():
    if not POSIX:
        return SKIP
    r = ff()
    s = r["s"]
    return [
        ("tozalash: --ha rc 0, snapshot C yaratildi, B qaytarish uchun qoldi",
         r["ha"].returncode == 0 and os.path.isdir(r["snap_c"]) and os.path.isdir(r["snap_b"])
         and r["manifest_c"]["root"] == r["snap_c"]),
        ("tozalash: eng eski A `git worktree remove` bilan ketdi (papka va reestr)",
         not os.path.exists(r["snap_a"]) and len(r["snaps_c"]) == 2
         and len(r["worktrees_c"]) == 3
         and not any(r["snap_a"] in line for line in r["worktrees_c"])
         and "Tozalandi (git worktree remove)" in r["ha"].stdout),
        ("tozalash: hooklar C da, A va B ga yo'q",
         hooks_point_to(r["cmds_c"], r["snap_c"])
         and not any(r["snap_a"] in c or r["snap_b"] in c for c in r["cmds_c"])),
        ("yangilanish yo'q: rc 0 va hech narsa o'zgarmadi",
         r["yangi_yoq"].returncode == 0 and r["yangi_yoq_same"]
         and "Yangilanish yo'q" in r["yangi_yoq"].stdout),
        ("klon ishchi daraxti toza qoldi", testkit.git(s.klon, "status", "--porcelain") == ""),
    ]


# --- stop: iflos klon, detached HEAD, ajralgan tarix ---------------------------

def stop():
    if "stop_natija" in _SAHNA:
        return _SAHNA["stop_natija"]
    s = sahna("stop")
    r = {"s": s}
    s.dev_commit("tools/budget.py")
    base = s.state()

    # Kirish nuqtasi: klondan yurgizilgan nusxa to'xtaydi (pull dan keyin
    # ko'rilmagan kod tasdiqdan oldin yurmasin), snapshotdagi nusxa ishlaydi.
    r["klondan_rad"] = testkit.call_main(
        Y.main, argv=["yangilash.py", "--klon", s.klon, "--faqat-korsat"],
        env={"HOME": s.home, "CLAUDE_CONFIG_DIR": None})
    r["klondan_rad_same"] = base == s.state()
    tool = os.path.join(s.snap0, "tools", "yangilash.py")
    r["snap_tool"] = tool
    r["snap_run"] = run_script(s, tool, "--faqat-korsat")
    r["snap_run_same"] = base == s.state()
    r["snap_run_boshqa_klon"] = run_script(s, tool, "--faqat-korsat", GENIUS_CLONE=s.dev)
    r["snap_run_boshqa_same"] = base == s.state()
    r["snap_run_aniq_klon"] = run_script(s, tool, "--faqat-korsat", "--klon", s.dev)
    r["snap_run_aniq_same"] = base == s.state()

    path = os.path.join(s.klon, "tools", "guard.py")
    with io.open(path, "a", encoding="utf-8", newline="\n") as handle:
        handle.write("\n# iflos\n")
    r["dirty"] = s.run("--ha")
    r["dirty_dry"] = s.run("--faqat-korsat")
    testkit.git(s.klon, "checkout", "-q", "--", "tools/guard.py")
    r["dirty_same"] = base == s.state()

    testkit.git(s.klon, "checkout", "-q", "--detach")
    r["detached"] = s.run("--ha")
    # worktree ro'yxatining birinchi qatori (klonning o'zi) detached holatini ko'rsatadi
    r["detached_same"] = (s.state()[:5] == base[:5] and s.state()[5][1:] == base[5][1:]
                          and s.state()[6:] == base[6:])
    testkit.git(s.klon, "checkout", "-q", "main")

    with io.open(os.path.join(s.klon, "tools", "usage.py"), "a", encoding="utf-8",
                 newline="\n") as handle:
        handle.write("\n# lokal commit\n")
    testkit.git(s.klon, "commit", "-q", "-am", "lokal")
    r["local_head"] = testkit.git(s.klon, "rev-parse", "HEAD")
    r["ajralgan"] = s.run("--ha")
    after = s.state()
    r["ajralgan_same"] = (after[0] == r["local_head"] and after[2:5] == base[2:5]
                          and after[5][1:] == base[5][1:] and after[6:] == base[6:]
                          and after[1] == "" and "Merge" not in testkit.git(
                              s.klon, "log", "-1", "--format=%s"))
    _SAHNA["stop_natija"] = r
    return r


def case_kirish_nuqtasi_snapshotdan():
    """Yangilash kirish nuqtasi snapshotdagi nusxa: klondagi nusxa manifest bor
    bo'lsa to'xtaydi va snapshot yo'lini aytadi; snapshotdan yurgan nusxa klonni
    manifestdan topadi; env yoki `--klon` manifestdan farq qilsa xato (aniq
    `--klon` ruxsat)."""
    if not POSIX:
        return SKIP
    r = stop()
    s = r["s"]
    out = r["klondan_rad"].stdout
    return [
        ("klondan yurgizilgan nusxa: rc 1, snapshotdagi yo'l aytildi, hech narsa o'zgarmadi",
         r["klondan_rad"].returncode == 1 and r["snap_tool"].replace("\\", "/") in out
         and "--klondan" in out and r["klondan_rad_same"]),
        ("snapshotdan yurgan nusxa: klon manifestdan, ro'yxat chiqdi, hech narsa o'zgarmadi",
         r["snap_run"].returncode == 0 and "Klon  : %s" % s.klon in r["snap_run"].stdout
         and "Yangi commitlar" in r["snap_run"].stdout and r["snap_run_same"]),
        ("snapshotdan yurish: GENIUS_CLONE manifestdagidan farq qilsa xato",
         r["snap_run_boshqa_klon"].returncode == 1
         and "manifestdagi klon" in r["snap_run_boshqa_klon"].stdout
         and r["snap_run_boshqa_same"]),
        ("snapshotdan yurish: aniq --klon ruxsat (iflos emas dev klon fetch qiladi)",
         "manifestdagi klon" not in r["snap_run_aniq_klon"].stdout
         and r["snap_run_aniq_same"]),
    ]


def case_iflos_klonda_toxtaydi():
    if not POSIX:
        return SKIP
    r = stop()
    return [
        ("iflos klon: --ha rc 1, sabab aytildi", r["dirty"].returncode == 1
         and "iflos" in r["dirty"].stdout and "Hech narsa o'zgarmadi" in r["dirty"].stdout),
        ("iflos klon: --faqat-korsat ham to'xtaydi", r["dirty_dry"].returncode == 1
         and "iflos" in r["dirty_dry"].stdout),
        ("iflos klon: HEAD, settings, manifest, snapshot va worktree o'zgarmadi",
         r["dirty_same"]),
    ]


def case_detached_headda_toxtaydi():
    if not POSIX:
        return SKIP
    r = stop()
    return [
        ("detached HEAD: rc 1, sabab aytildi", r["detached"].returncode == 1
         and "detached HEAD" in r["detached"].stdout),
        ("detached HEAD: hech narsa o'zgarmadi", r["detached_same"]),
    ]


def case_ff_bolmasa_toxtaydi():
    """Klon va origin ajralgan: rebase va merge commit yo'q, hech narsa o'zgarmaydi."""
    if not POSIX:
        return SKIP
    r = stop()
    out = r["ajralgan"].stdout
    return [
        ("ff bo'lmasa: rc 1, 'fast-forward mumkin emas' va rebase qilinmasligi aytildi",
         r["ajralgan"].returncode == 1 and "fast-forward mumkin emas" in out
         and "Rebase" in out),
        ("ff bo'lmasa: klon HEAD i lokal commitda qoldi, settings, snapshot va worktree "
         "o'zgarmadi, merge commit yo'q", r["ajralgan_same"]),
    ]


# --- yozish: memory va holat klonga tushadi -----------------------------------

def tool_env(s, **extra):
    """Hook jarayoni muhiti: settings.json env (GENIUS_CLONE, GENIUS_PYTHON)."""
    env = dict(os.environ, HOME=s.home, GENIUS_CLONE=s.klon,
               GENIUS_PYTHON=sys.executable, CLAUDE_PROJECT_DIR=s.klon,
               PYTHONIOENCODING="utf-8")
    for key in ("GENIUS_STATE_DIR", "GENIUS_MEMORY_DIR", "CLAUDE_CODE_REMOTE",
                "CLAUDE_CONFIG_DIR"):
        env.pop(key, None)
    env.update(extra)
    return env


def run_tool(s, snap, script, *args, **extra):
    return subprocess.run(
        [sys.executable, os.path.join(snap, "tools", script)] + list(args),
        cwd=s.klon, env=tool_env(s, **extra), stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8",
        errors="replace")


def case_memory_va_holat_klonga_tushadi():
    """Asbob snapshotdan yuradi, lekin yozadigani klonda: holat `.claude/.state`
    va memory (bulut sessiyasida handoff) klonga, snapshotga hech narsa."""
    if not POSIX:
        return SKIP
    s = sahna("yozish")
    snap = s.snap0
    probe = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, %r); import docref, geniuslib, hookio; "
         "print(hookio.state_dir()); print(docref.memory_dir('umumiy')); "
         "print(docref.memory_dir('claude-genius')); print(docref.is_clone_project()); "
         "print(docref.in_clone()); print(docref.ROOT)" % os.path.join(snap, "tools")],
        cwd=s.klon, env=tool_env(s), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        encoding="utf-8", errors="replace")
    lines = probe.stdout.strip().splitlines()

    budget = run_tool(s, snap, "budget.py", "--yangi-vazifa", "sinov")
    local = run_tool(s, snap, "handoff.py", "--prompt", "--vazifa", "lokal-sinov")
    remote = run_tool(s, snap, "handoff.py", "--prompt", "--vazifa", "bulut-sinov",
                      CLAUDE_CODE_REMOTE="true")

    klon_state = os.path.join(s.klon, ".claude", ".state")
    memory_files = []
    for dirpath, _, files in os.walk(os.path.join(s.klon, "memory")):
        memory_files += [os.path.join(dirpath, n) for n in files if "bulut-sinov" in n]
    snap_memory_new = [p for p in memory_files if p.startswith(snap)]
    return [
        ("yozish: ROOT snapshot, lekin holat va memory yo'llari klonda",
         probe.returncode == 0 and len(lines) == 6 and lines[0] == klon_state
         and lines[1] == os.path.join(s.klon, "memory", "umumiy")
         and lines[2] == os.path.join(s.klon, "memory", "claude-genius")
         and lines[3] == "True" and lines[5] == snap),
        ("yozish: budget.py holatni klonning .claude/.state ga yozdi",
         budget.returncode == 0
         and os.path.isfile(os.path.join(klon_state, "budget.json"))),
        ("yozish: lokal handoff topshirig'i klonning holat papkasiga",
         local.returncode == 0 and os.path.isfile(
             os.path.join(klon_state, "handoff", "lokal-sinov.md"))),
        ("yozish: bulut handoff memory ga, klonning memory/ ostiga",
         remote.returncode == 0 and len(memory_files) == 1
         and memory_files[0].startswith(os.path.join(s.klon, "memory") + os.sep)),
        ("yozish: snapshotga holat ham, memory ham tushmadi",
         not snap_memory_new
         and not os.path.exists(os.path.join(snap, ".claude", ".state"))
         and not os.path.exists(os.path.join(snap, ".claude", "usage"))
         and testkit.git(snap, "status", "--porcelain", "--untracked-files=no") == ""),
    ]


def case_clone_env_faqat_snapshotda():
    """GENIUS_CLONE faqat ROOT `<claude>/genius/<12hex>` (snapshot) bo'lsa olinadi.
    Global o'rnatilgan mashinada u hamma sessiyada turadi: klonning o'zi va uning
    `.claude/worktrees/genius-x` worktree si holat va memoryni asosiy klonga
    yozmasligi shart. Buzuq qiymat (yo'q papka, nisbiy) ham e'tiborsiz."""
    sys.path.insert(0, HERE)
    import geniuslib
    tmp = tmpdir("clone_env_")
    asosiy = os.path.join(tmp, "asosiy")
    os.makedirs(asosiy)
    snap = os.path.join(tmp, "uy", ".claude", "genius", "0123456789ab")
    klon = os.path.join(tmp, "boshqa-klon")
    worktree = os.path.join(klon, ".claude", "worktrees", "genius-x")
    yomon_nom = os.path.join(tmp, "uy", ".claude", "genius", "begona")
    for path in (snap, klon, worktree, yomon_nom):
        os.makedirs(path)
    saved = os.environ.get("GENIUS_CLONE"), os.environ.get("GENIUS_STATE_DIR")
    try:
        os.environ.pop("GENIUS_STATE_DIR", None)
        os.environ["GENIUS_CLONE"] = asosiy
        rows = []
        for root, want in ((snap, os.path.normpath(asosiy)), (klon, klon), (worktree, worktree),
                           (yomon_nom, yomon_nom), (ROOT, ROOT)):
            rows.append((geniuslib.clone_root(root) == want,
                         geniuslib.state_dir(root) == os.path.join(want, ".claude", ".state")))
        for given in ("", "   ", "nisbiy/yo'l", os.path.join(tmp, "yoq")):
            os.environ["GENIUS_CLONE"] = given
            rows.append((geniuslib.clone_root(snap) == snap, True))
        os.environ["GENIUS_CLONE"] = asosiy
        os.environ["GENIUS_STATE_DIR"] = os.path.join(tmp, "holat")
        rows.append((geniuslib.state_dir(snap) == os.path.join(tmp, "holat"), True))
        rows.append((geniuslib.is_snapshot(snap) and not geniuslib.is_snapshot(klon)
                     and not geniuslib.is_snapshot(worktree), True))
        return all(a and b for a, b in rows) and len(rows) == 11
    finally:
        for key, value in zip(("GENIUS_CLONE", "GENIUS_STATE_DIR"), saved):
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def case_klon_va_worktree_hooki_asosiy_klonga_yozmaydi():
    """Regressiya (haqiqiy jarayon): global o'rnatilgan muhitda (GENIUS_CLONE asosiy
    klonda) klonning o'zidagi tools/ va uning worktree sidagi tools/ holatni va
    memoryni O'Z daraxtiga yozadi, asosiy klonga emas."""
    if not POSIX:
        return SKIP
    s = sahna("yozish")
    boshqa = testkit.repo_nusxa(ROOT, os.path.join(tmpdir("worktree_"), "klon2"))
    wt = os.path.join(boshqa, ".claude", "worktrees", "genius-x")
    testkit.git(boshqa, "worktree", "add", "-q", "--detach", wt, "HEAD")
    probe = ("import sys; sys.path.insert(0, %r); import hookio, docref; "
             "print(hookio.state_dir()); print(docref.memory_dir('umumiy'))")
    rows = []
    for tree in (boshqa, wt):
        res = subprocess.run(
            [sys.executable, "-c", probe % os.path.join(tree, "tools")], cwd=tree,
            env=tool_env(s), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            encoding="utf-8", errors="replace")
        lines = res.stdout.strip().splitlines()
        rows.append(("%s: holat va memory o'z daraxtida" % os.path.basename(tree),
                     res.returncode == 0 and len(lines) == 2
                     and lines[0] == os.path.join(tree, ".claude", ".state")
                     and lines[1] == os.path.join(tree, "memory", "umumiy")))
    rows.append(("asosiy klon (GENIUS_CLONE) ga hech narsa yozilmadi",
                 not os.path.exists(os.path.join(s.klon, ".claude", ".state", "rules_for"))))
    return rows


def case_state_usage_run_tests_actor_check_klonda():
    """DECISIONS da'vosi: state.py, usage.py, run_tests jurnali va actor_check holati
    snapshotdan yurganda klonga yo'naltiriladi (modul yo'llari va haqiqiy yozuv)."""
    if not POSIX:
        return SKIP
    s = sahna("yozish")
    snap = s.snap0
    tools = os.path.join(snap, "tools")
    klon_state = os.path.join(s.klon, ".claude", ".state")
    code = ("import sys, os; sys.path.insert(0, %r); "
            "import state, usage, run_tests, actor_check, budget; "
            "print(state.MARKS); print(usage.STATE_DIR); print(usage.STORE); "
            "print(run_tests.JOURNAL); print(actor_check.JOURNAL); print(budget.LOG); "
            "state.mark([os.path.join(%r, 'Sinov.java')], ['sinov'])" % (tools, s.klon))
    res = subprocess.run([sys.executable, "-c", code], cwd=s.klon, env=tool_env(s),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         encoding="utf-8", errors="replace")
    lines = res.stdout.strip().splitlines()
    want = [os.path.join(klon_state, "rules_for"), klon_state,
            os.path.join(s.klon, ".claude", "usage"),
            os.path.join(klon_state, "run_tests.jsonl"),
            os.path.join(klon_state, "run_tests.jsonl"),
            os.path.join(klon_state, "budget.json")]
    marks = os.path.join(klon_state, "rules_for")
    return [
        ("yozuvchi modullar yo'llari klonda (MARKS, STATE_DIR, STORE, JOURNAL, LOG)",
         res.returncode == 0 and lines == want),
        ("state.mark() belgisi klonga tushdi", os.path.isdir(marks) and os.listdir(marks)),
        ("snapshotda .claude/.state va usage yo'q",
         not os.path.exists(os.path.join(snap, ".claude", ".state"))
         and not os.path.exists(os.path.join(snap, ".claude", "usage"))),
    ]


def case_ikki_klon_bir_sha_snapshot_ulashilmaydi():
    """Qaror: boshqa klon bir xil sha da yasagan snapshotni `yarat` ulashmaydi
    (uning `--uninstall` i bu klonning hookini ostidan olib tashlardi): xato."""
    if not POSIX:
        return SKIP
    s = sahna("yozish")
    base = tmpdir("ikkinchi_")
    ikkinchi = os.path.join(base, "klon")
    testkit.git(base, "clone", "-q", s.klon, ikkinchi)
    sha = testkit.git(ikkinchi, "rev-parse", "HEAD")
    rows = []
    if sha[:12] != s.head0[:12]:
        return [("ikkinchi klon bir xil sha da emas", False)]
    try:
        SNAP.yarat(ikkinchi, s.claude, sha)
        rows.append(("ikki klon bir sha: xato berdi", False))
    except SNAP.SnapshotXato as exc:
        rows.append(("ikki klon bir sha: xato 'boshqa klonga tegishli' berdi",
                     "boshqa klonga" in str(exc)))
    rows.append(("ikki klon bir sha: asl snapshot va klon reestri joyida",
                 os.path.isdir(s.snap0) and len(s.worktrees()) >= 2
                 and SNAP.royxat(ikkinchi, s.claude) == []))
    return rows


def case_snapshotsiz_ornatishdan_yangilashda_eski_snapshot_xabari():
    """Eski (snapshotsiz) o'rnatishda manifest `root` klonning o'zi edi: yangilash
    uni 'eski snapshot qoldi' deb ko'rsatmaydi va tozalashga ham bermaydi."""
    if not POSIX:
        return SKIP
    s = Sahna()
    path = os.path.join(s.claude, "skills", "manguberdi", ".genius.json")
    manifest = TI.jget(path)
    manifest["root"] = s.klon
    del manifest["clone"]
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(manifest))
    s.dev_commit("tools/budget.py")
    res = s.run("--ha")
    return [
        ("snapshotsiz o'rnatishdan yangilash: rc 0, yangi snapshot",
         res.returncode == 0 and len(s.snapshots()) == 1),
        ("snapshotsiz o'rnatishdan yangilash: klon 'eski snapshot' deb aytilmadi",
         "Qaytarish uchun eski snapshot qoldi" not in res.stdout
         and os.path.isdir(s.klon) and "Yangilandi" in res.stdout),
    ]


def case_ornatuvchi_ozgargan_commitni_korsatadi():
    """install.py --apply manifestdagi commitdan farqli sha ga o'tayotganda
    `log --oneline <eski>..<yangi>` ro'yxatini ko'rsatadi (to'smaydi)."""
    if not POSIX:
        return SKIP
    s = Sahna()
    s.dev_commit("tools/guard.py")
    testkit.git(s.klon, "pull", "-q", "--ff-only")
    res = TI.run_install(s.home, "--apply", "--genius-path", s.klon,
                         "--backup-to", os.path.join(s.home, "zaxira-1"))
    again = TI.run_install(s.home, "--apply", "--genius-path", s.klon,
                           "--backup-to", os.path.join(s.home, "zaxira-2"))
    return [
        ("o'rnatuvchi: farq ro'yxati chiqdi, rc 0",
         res.returncode == 0 and "yangi 1: tools/guard.py" in res.stdout
         and "tools/guard.py" in res.stdout and "tools/yangilash.py" in res.stdout),
        ("o'rnatuvchi: klon aytiladi, yangilash yo'li snapshotdagi nusxa",
         "Klon  : %s" % s.klon in res.stdout
         and ("%s/tools/yangilash.py" % os.path.join(s.claude, "genius",
                                                    testkit.git(s.klon, "rev-parse", "HEAD")[:12]))
         in res.stdout),
        ("o'rnatuvchi: bir xil commit da ro'yxat yo'q",
         again.returncode == 0 and "Yangi commitlar" not in again.stdout),
    ]


# --- snapshot.py: xavfsizlik ---------------------------------------------------

def case_snapshot_faqat_genius_ostidagini_ochiradi():
    """olib_tashla: `<claude>/genius/<12 hex>` dan boshqasini rad etadi (symlink,
    nom, boshqa papka), hech narsa o'chmaydi."""
    tmp = tmpdir("snap_guard_")
    claude = os.path.join(tmp, ".claude")
    genius = os.path.join(claude, "genius")
    os.makedirs(genius)
    victim = os.path.join(tmp, "qurbon")
    os.makedirs(victim)
    with io.open(os.path.join(victim, "m.txt"), "w", encoding="utf-8") as handle:
        handle.write("muhim")
    link = os.path.join(genius, "0123456789ab")
    os.symlink(victim, link)
    bad_name = os.path.join(genius, "begona")
    os.makedirs(bad_name)
    outside = os.path.join(tmp, "0123456789ab")
    os.makedirs(outside)
    rows = []
    for path in (link, bad_name, outside, genius, victim):
        try:
            SNAP.olib_tashla(path, tmp, claude)
            rows.append(False)
        except SNAP.SnapshotXato:
            rows.append(True)
    rows.append(os.path.isfile(os.path.join(victim, "m.txt")) and os.path.isdir(bad_name)
                and os.path.isdir(outside) and os.path.islink(link))
    return all(rows) and len(rows) == 6


def case_snapshot_ozgartirilgan_bolsa_rad():
    """Mavjud snapshotda tracked fayl o'zgartirilgan (hook kodi tahrirlangan) bo'lsa
    o'rnatuvchi uni jim qayta ishlatmaydi: xato, hech narsa almashmaydi."""
    if not POSIX:
        return SKIP
    s = Sahna()
    path = os.path.join(s.snap0, "tools", "guard.py")
    with io.open(path, "a", encoding="utf-8", newline="\n") as handle:
        handle.write("\nimport os  # kimdir tahrirladi\n")
    before = s.settings_bytes()
    res = TI.run_install(s.home, "--apply", "--genius-path", s.klon,
                         "--backup-to", os.path.join(s.home, "zaxira-1"))
    return [
        ("o'zgartirilgan snapshot: rc 1, sabab aytildi",
         res.returncode == 1 and "o'zgartirilgan fayl bor" in res.stdout),
        ("o'zgartirilgan snapshot: settings.json almashmadi", before == s.settings_bytes()),
    ]


def case_qolda_ochirilgan_snapshot_qayta_yasaladi():
    """Snapshot papkasi qo'lda o'chirilgan (`rm -rf`): git reestrida yozuv qoladi va
    `worktree add` rad etardi. O'rnatuvchi avval `worktree prune` qiladi va qayta yasaydi."""
    if not POSIX:
        return SKIP
    s = Sahna()
    shutil.rmtree(s.snap0)
    res = TI.run_install(s.home, "--apply", "--genius-path", s.klon,
                         "--backup-to", os.path.join(s.home, "zaxira-1"))
    return [
        ("qo'lda o'chirilgan snapshot: rc 0, qayta yasaldi",
         res.returncode == 0 and os.path.isdir(s.snap0) and "yaratildi" in res.stdout),
        ("qo'lda o'chirilgan snapshot: reestrda bitta yozuv, hooklar unga ishora qiladi",
         len(s.worktrees()) == 2 and hooks_point_to(s.commands(), s.snap0)),
    ]


def case_py38_sintaksis_va_emdash():
    import ast
    rows = []
    for name in (os.path.join(HERE, "yangilash.py"),
                 os.path.join(ROOT, "install", "snapshot.py")):
        with io.open(name, encoding="utf-8") as handle:
            text = handle.read()
        ast.parse(text, feature_version=(3, 8))
        rows.append(("—" not in text and "–" not in text, os.path.basename(name)))
    return [("py3.8 sintaksisi va em-dash yo'q: %s" % name, ok) for ok, name in rows]


CASES = [
    ("o'rnatish snapshot yasaydi, hook yo'li unga ishora qiladi", case_ornatish_snapshot_yasaydi),
    ("git pull hook faylini o'zgartirmaydi (XV-Y1, sha256)", case_pull_hook_faylini_ozgartirmaydi),
    ("--faqat-korsat hech narsa o'zgartirmaydi", case_faqat_korsat_hech_narsa_ozgartirmaydi),
    ("rad etishda hech narsa o'zgarmaydi", case_rad_etishda_ozgarmaydi),
    ("--ha: yangi snapshot, eski bittasi qoladi", case_ha_yangi_snapshot_eski_qoladi),
    ("tasdiq: ff-merge, yangi snapshot, settings yangilandi", case_tasdiq_ff_merge_va_yangi_snapshot),
    ("keyingi yangilashda eng eskisi tozalanadi", case_keyingi_yangilashda_eng_eskisi_tozalanadi),
    ("kirish nuqtasi snapshotdagi nusxa", case_kirish_nuqtasi_snapshotdan),
    ("iflos klonda to'xtaydi", case_iflos_klonda_toxtaydi),
    ("detached HEAD da to'xtaydi", case_detached_headda_toxtaydi),
    ("ff bo'lmasa to'xtaydi", case_ff_bolmasa_toxtaydi),
    ("memory va holat klonga tushadi, snapshotga emas", case_memory_va_holat_klonga_tushadi),
    ("GENIUS_CLONE faqat snapshotda olinadi (klon va worktree emas)", case_clone_env_faqat_snapshotda),
    ("klon va worktree hooki asosiy klonga yozmaydi", case_klon_va_worktree_hooki_asosiy_klonga_yozmaydi),
    ("state, usage, run_tests, actor_check yozuvi klonda", case_state_usage_run_tests_actor_check_klonda),
    ("ikki klon bir sha: snapshot ulashilmaydi", case_ikki_klon_bir_sha_snapshot_ulashilmaydi),
    ("snapshotsiz o'rnatishdan yangilash: eski snapshot xabari", case_snapshotsiz_ornatishdan_yangilashda_eski_snapshot_xabari),
    ("o'rnatuvchi o'zgargan commit ro'yxatini ko'rsatadi", case_ornatuvchi_ozgargan_commitni_korsatadi),
    ("snapshot: faqat ~/.claude/genius ostidagini o'chiradi", case_snapshot_faqat_genius_ostidagini_ochiradi),
    ("snapshot: o'zgartirilgan bo'lsa qayta ishlatilmaydi", case_snapshot_ozgartirilgan_bolsa_rad),
    ("snapshot: qo'lda o'chirilgan bo'lsa qayta yasaladi", case_qolda_ochirilgan_snapshot_qayta_yasaladi),
    ("yangilash.py va snapshot.py: py3.8, em-dash yo'q", case_py38_sintaksis_va_emdash),
]


if __name__ == "__main__":
    sys.exit(testkit.run_cases(CASES, sys.argv[1:]))
