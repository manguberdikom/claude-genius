#!/usr/bin/env python3
"""install/install.py uchun sinovlar (Linux, macOS va Windows o'rnatuvchisi).

    python3 tools/test_install.py
    python3 tools/test_install.py -k paritet
    python3 tools/test_install.py -k windows

Haqiqiy ~/.claude ga tegilmaydi: har holat vaqtinchalik HOME (`HOME` env,
tmp papka) bilan yuradi. Quruq yurish, --apply, --update, --uninstall bitta
ketma-ketlikda (`stsenariy`) bir marta yuradi va holatlar uning natijasini
tekshiradi: har --apply indeksni qayta yasaydi va asboblarni chaqiradi.

Windows (R7.2): manguberdi.ps1 yupqa o'ram, o'rnatish mantig'i install.py da
va PowerShell bu muhitda yurmaydi. Windows shakli `--platforma nt` bilan Linux
da ham yuradi (USERPROFILE, teskari slashli Python, managed yo'llari, bash
tashqaridan): ikkinchi stsenariy (`stsenariy(nt=True)`) shu rejimda dry,
apply, update va uninstall ni yurgizadi. Paritet ps1 matnini emas, install.py
ning ikki platforma uchun chiqishini solishtiradi; Windows shaklining ilgari
ps1 bergan natijaga tengligi OLTIN qiymat bilan tekshiriladi (asos commit
89133b10982c dagi manguberdi.ps1 matnidan bir marta chiqarilgan). ps1 ning
o'zi uchun faqat "yupqa o'ram" matn tekshiruvi: haqiqiy sinov CI Windows
ishida (powershell va pwsh). Ish yuradigan holatlar POSIX da; Windows da
install.py ni ps1 CI qadamlari sinaydi.
"""

import atexit
import ast
import importlib.util
import io
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "install"))

import testkit  # noqa: E402
import test_rewrite_paths as T  # noqa: E402  (settings.json hook jadvalini o'qish usuli)

INSTALL_PY = os.path.join(ROOT, "install", "install.py")
spec = importlib.util.spec_from_file_location("install_py", INSTALL_PY)
I = importlib.util.module_from_spec(spec)
spec.loader.exec_module(I)

POSIX = os.name != "nt"
SKIP = [("o'tkazildi: Windows da ish yuradigan holatlar yo'q (ps1 CI qadamlari sinaydi)", True)]

# Windows shakli (`--platforma nt`): hook buyrug'ida teskari slashli Python, env
# va manifestda `/` bilan.
WIN_PY = "C:\\Python312\\python.exe"
WIN_PY_FWD = "C:/Python312/python.exe"

_TMP = []


def tmpdir(prefix="inst_"):
    path = tempfile.mkdtemp(prefix=prefix)
    _TMP.append(path)
    return path


@atexit.register
def _cleanup():
    for path in _TMP:
        shutil.rmtree(path, ignore_errors=True)


def put(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def get(path):
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


def jget(path):
    return json.loads(get(path))


def snapshot(folder):
    """{yo'l: (hajm, mtime) yoki None papka uchun}: kengaytma fayllar ham."""
    out = {}
    for dirpath, dirs, files in os.walk(folder):
        for name in dirs:
            out[os.path.join(dirpath, name)] = None
        for name in files:
            path = os.path.join(dirpath, name)
            stat = os.stat(path)
            out[path] = (stat.st_size, stat.st_mtime_ns)
    return out


def temp_stages():
    return sorted(n for n in os.listdir(tempfile.gettempdir())
                  if n.startswith("manguberdi-"))


_GITKLON = []


def git_klon():
    """O'rnatiladigan klon: ishchi daraxt nusxasi, commit qilingan git repo.

    Snapshot `git worktree add` bilan yasaladi (R7.8 XV-Y1), shuning uchun klon
    git repo bo'lishi shart. Reponing o'zi (uning .git/worktrees i) tegilmaydi."""
    if not _GITKLON:
        _GITKLON.append(testkit.repo_nusxa(ROOT, os.path.join(tmpdir("gitklon_"), "klon")))
    return _GITKLON[0]


def head_of(klon):
    return testkit.git(klon, "rev-parse", "HEAD")


def snap_of(home, klon):
    """Kutilgan snapshot joyi: <uy>/.claude/genius/<sha12>."""
    return os.path.join(home, ".claude", "genius", head_of(klon)[:12])


_NT = {}


def nt_muhit(home):
    """Windows rejimi muhiti: uy USERPROFILE dan (HOME esa boshqa, bo'sh papka:
    unga tegilsa sinov ko'radi), managed yo'llari ProgramFiles va ProgramData dan."""
    if "decoy" not in _NT:
        _NT["decoy"] = tmpdir("decoy_home_")
        _NT["pf"] = tmpdir("programfiles_")
        _NT["pd"] = tmpdir("programdata_")
    return {"HOME": _NT["decoy"], "USERPROFILE": home, "CLAUDE_CONFIG_DIR": None,
            "ProgramFiles": _NT["pf"], "ProgramData": _NT["pd"]}


def nt_argv():
    """ps1 o'ramning chaqiruvi: --platforma nt, bash tashqaridan (Git Bash o'rnida
    shu mashinaning bashi), `--python` Windows shaklida."""
    return ["--platforma", "nt", "--ps1", "--python", WIN_PY, "--bash",
            shutil.which("bash") or "/bin/bash"]


def run_install(home, *args, **kw):
    """install.main() ni vaqtinchalik HOME bilan yurgizadi: Result(rc, out, err).

    `--genius-path` berilmasa git_klon(): ishchi daraxtning o'zi emas, uning
    commit qilingan nusxasi (snapshot reponing o'ziga tegmasin). `nt=True` bo'lsa
    Windows rejimi (nt_argv, USERPROFILE)."""
    args = list(args)
    if "--genius-path" not in args:
        args += ["--genius-path", git_klon()]
    env = {"HOME": home, "CLAUDE_CONFIG_DIR": None}
    if kw.get("nt"):
        args += nt_argv()
        env = nt_muhit(home)
    return testkit.call_main(I.main, argv=["install.py"] + args, env=env)


def hooks_of(settings):
    return [h for groups in settings.get("hooks", {}).values()
            for g in groups for h in g.get("hooks", [])]


def commands_of(settings):
    return [h.get("command", "") for h in hooks_of(settings)]


# --- stsenariy: foydalanuvchi sozlamasi, dry, apply, update, uninstall ----

_STATES = {}
_CLONE = []

FOREIGN_SETTINGS = {
    "model": "opus",
    "hooks": {"SessionStart": [{"hooks": [
        {"type": "command", "command": "echo begona-hook"}]}]},
    "permissions": {"allow": ["Bash(git status:*)"]},
}


def oz_tmp(func):
    """Stsenariy o'z vaqtinchalik papkasida yuradi: `manguberdi-*` papkalar soni
    ("qolmadi" tekshiruvi) umumiy /tmp dagi boshqa jarayonlarga (parallel
    worktree larning o'rnatuvchi sinovlariga) bog'liq bo'lmasin."""
    def wrapper(*args, **kw):
        private = tmpdir("tmp_")
        saved = tempfile.tempdir, os.environ.get("TMPDIR")
        # tempfile.tempdir: jarayon ichidagi mkdtemp (install.main), TMPDIR: uning
        # subprocess lari (run_py).
        tempfile.tempdir, os.environ["TMPDIR"] = private, private
        try:
            return func(*args, **kw)
        finally:
            tempfile.tempdir = saved[0]
            if saved[1] is None:
                os.environ.pop("TMPDIR", None)
            else:
                os.environ["TMPDIR"] = saved[1]
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


@oz_tmp
def stsenariy(nt=False):
    st = _STATES.setdefault(nt, {})
    if st:
        return st
    home = tmpdir("uy_")
    claude = os.path.join(home, ".claude")
    put(os.path.join(claude, "skills", "eski", "SKILL.md"), "eski")
    put(os.path.join(claude, "CLAUDE.md"), "eski")
    put(os.path.join(claude, "plugins", "p", "x.json"), "{}")
    put(os.path.join(claude, "rules", "r.md"), "qoida")
    put(os.path.join(claude, "settings.json"), json.dumps(FOREIGN_SETTINGS))
    # Eski nomli aktyor: yangilashda zaxira bilan olinishi kerak.
    put(os.path.join(claude, "agents", "arxitektor.md"), "eski aktyor")
    put(os.path.join(claude, "agents", "begona.md"), "begona aktyor")

    st["home"], st["claude"] = home, claude
    py = WIN_PY_FWD if nt else sys.executable
    if nt:
        # Managed sozlama: ogohlantirish Windows yo'llaridan chiqadi.
        nt_muhit(home)
        put(os.path.join(_NT["pf"], "ClaudeCode", "managed-settings.json"), "{}")
    klon = git_klon()
    st["klon"], st["snap"] = klon, snap_of(home, klon)
    st["head"] = head_of(klon)
    index = os.path.join(ROOT, "index")

    st["stages_before"] = temp_stages()
    git_before = (testkit.git(klon, "status", "--porcelain"),
                  testkit.git(klon, "worktree", "list"))
    before = snapshot(home), snapshot(index), temp_stages(), snapshot(os.path.join(klon, ".git"))
    st["dry"] = run_install(home, nt=nt)
    st["dry_same"] = before == (snapshot(home), snapshot(index), temp_stages(),
                                snapshot(os.path.join(klon, ".git")))
    st["dry_git_same"] = git_before == (testkit.git(klon, "status", "--porcelain"),
                                        testkit.git(klon, "worktree", "list"))
    st["dry_no_genius"] = not os.path.exists(os.path.join(claude, "genius"))

    st["apply"] = run_install(home, "--apply", "--backup-to",
                              os.path.join(home, "zaxira-1"), nt=nt)
    path = os.path.join(claude, "settings.json")
    st["stages_after"] = temp_stages()
    st["after_apply_raw"] = open(path, "rb").read()
    st["after_apply"] = jget(path)
    st["apply_agents"] = sorted(os.listdir(os.path.join(claude, "agents")))
    st["fs_apply"] = set(snapshot(claude))
    st["claude_md"] = get(os.path.join(claude, "CLAUDE.md"))
    st["manifest"] = jget(os.path.join(claude, "skills", "manguberdi", ".genius.json"))
    st["skill_text"] = get(os.path.join(claude, "skills", "manguberdi", "SKILL.md"))
    st["worktrees_apply"] = testkit.git(klon, "worktree", "list")
    st["snap_tools_apply"] = sorted(os.listdir(os.path.join(st["snap"], "tools")))
    st["snap_index_apply"] = os.path.isfile(os.path.join(st["snap"], "index", "sections.tsv"))
    st["opt_in_cli"] = I.run_py(
        [os.path.join(ROOT, "install", "rewrite_paths.py"), claude, "--root", st["snap"],
         "--clone", klon, "--python", py, "--bash", "bash", "--opt-in"])
    # ps1 ham, install.py ham ruxsatni shu asbobdan oladi: shu holatdagi chiqishi.
    st["allow_cli"] = I.run_py(
        [os.path.join(ROOT, "install", "rewrite_paths.py"), claude, "--root", st["snap"],
         "--clone", klon, "--python", py, "--bash", "bash", "--allow"])

    # Yangilash: begona skill, begona hook (o'z hooklari bilan bir guruhda),
    # begona ruxsat va ikkinchi marta o'rnatish.
    put(os.path.join(claude, "skills", "begona", "SKILL.md"), "begona")
    data = jget(path)
    data["hooks"]["UserPromptSubmit"][0]["hooks"].append(
        {"type": "command", "command": "echo begona-hook-2"})
    data["permissions"]["allow"].append("Bash(ls:*)")
    put(path, json.dumps(data))
    st["update"] = run_install(home, "--update", "--apply", "--backup-to",
                               os.path.join(home, "zaxira-2"), nt=nt)
    st["after_update"] = jget(path)
    st["update_agents"] = sorted(os.listdir(os.path.join(claude, "agents")))
    st["fs_update"] = set(snapshot(claude))

    before = snapshot(home)
    st["uninstall_dry"] = run_install(home, "--uninstall", nt=nt)
    st["uninstall_dry_same"] = before == snapshot(home)
    st["uninstall"] = run_install(home, "--uninstall", "--apply", "--backup-to",
                                  os.path.join(home, "zaxira-3"), nt=nt)
    st["fs_uninstall"] = set(snapshot(claude))
    st["after_uninstall"] = jget(path)
    st["worktrees_uninstall"] = testkit.git(klon, "worktree", "list")
    st["genius_after_uninstall"] = sorted(
        os.listdir(os.path.join(claude, "genius"))) if os.path.isdir(
            os.path.join(claude, "genius")) else []
    return st


def case_py38_sintaksis():
    text = get(INSTALL_PY)
    ast.parse(text, feature_version=(3, 8))
    bad = [c for c in ("—", "–") if c in text]
    return not bad


def case_quruq_yurish_hech_narsa_yozmaydi():
    if not POSIX:
        return SKIP
    st = stsenariy()
    out = st["dry"].stdout
    return [
        ("quruq: rc 0", st["dry"].returncode == 0),
        ("quruq: uy, indeks, vaqtinchalik papka va klonning .git i o'zgarmadi",
         st["dry_same"]),
        ("quruq: git status va worktree ro'yxati o'zgarmadi, snapshot yo'q",
         st["dry_git_same"] and st["dry_no_genius"]),
        ("quruq: ro'yxat chiqdi", "quruq yurish" in out and "o'rnatilmoqda" in out
         and "almashtiriladi:" in out),
        ("quruq: zaxira yozilmadi", not any(
            n.startswith(".claude-backup") for n in os.listdir(st["home"]))),
    ]


def case_apply_ornatadi():
    if not POSIX:
        return SKIP
    st = stsenariy()
    claude, after = st["claude"], st["after_apply"]
    cmds = commands_of(after)
    manifest, fs = st["manifest"], st["fs_apply"]
    backup = os.path.join(st["home"], "zaxira-1")
    return [
        ("apply: rc 0", st["apply"].returncode == 0),
        ("apply: skill va olti aktyor",
         os.path.join(claude, "skills", "manguberdi", "SKILL.md") in fs
         and all(a + ".md" in st["apply_agents"] for a in I.ACTORS)),
        ("apply: eski aktyor olindi, begonasi qoldi",
         "arxitektor.md" not in st["apply_agents"] and "begona.md" in st["apply_agents"]),
        ("apply: begona fayllar joyida",
         st["claude_md"] == "eski"
         and all(os.path.join(claude, *rel) in fs for rel in (
             ("skills", "eski", "SKILL.md"), ("plugins", "p", "x.json"),
             ("rules", "r.md")))),
        ("apply: begona hook, ruxsat va kalit joyida",
         "echo begona-hook" in cmds and after.get("model") == "opus"
         and "Bash(git status:*)" in after["permissions"]["allow"]),
        ("apply: o'z hooki bir marta",
         sum("suggest_sections.py" in c for c in cmds) == 1),
        ("apply: settings.json BOM siz", not st["after_apply_raw"].startswith(b"\xef\xbb\xbf")),
        ("apply: manifest (root snapshot, clone klon, commit HEAD)",
         manifest["root"] == st["snap"] and manifest["clone"] == st["klon"]
         and manifest["commit"] == st["head"] and manifest["actors"] == list(I.ACTORS)
         and manifest["python"] == sys.executable),
        ("apply: snapshot detached worktree, indeks bir marta yasalgan",
         any(line.startswith(st["snap"]) and "detached HEAD" in line
             for line in st["worktrees_apply"].splitlines())
         and st["snap_index_apply"] and "guard.py" in st["snap_tools_apply"]),
        ("apply: hook yo'li snapshotga ishora qiladi, klonning tools/ iga emas",
         len(cmds) >= 8
         and all((st["snap"] + "/tools/") in c for c in cmds if "begona" not in c)
         and not any((st["klon"] + "/tools/") in c for c in cmds)),
        ("apply: env.GENIUS_CLONE klon, additionalDirectories snapshot docs va klon memory",
         after["env"].get("GENIUS_CLONE") == st["klon"]
         and after["permissions"]["additionalDirectories"]
         == [st["snap"] + "/docs", st["klon"] + "/memory"]),
        ("apply: ruxsat qoidalari snapshotga ishora qiladi",
         all(st["klon"] not in r for r in after["permissions"]["allow"])
         and any(st["snap"] in r for r in after["permissions"]["allow"])),
        ("apply: skill matni tools/ ni snapshotga, memory/ ni klonga bog'laydi",
         ("%s/tools/rules_for.py" % st["snap"]) in st["skill_text"]
         and ("%s/memory/" % st["klon"]) in st["skill_text"]
         and ("%s/memory/" % st["snap"]) not in st["skill_text"]),
        ("apply: klon ishchi daraxti toza, indeks klonga yozilmadi",
         testkit.git(st["klon"], "status", "--porcelain") == ""
         and not os.path.exists(os.path.join(st["klon"], "index"))),
        ("apply: zaxira (settings, skill yo'q edi, eski aktyor)",
         os.path.isfile(os.path.join(backup, ".claude--settings.json"))
         and os.path.isfile(os.path.join(backup, "agents--arxitektor.md"))),
        ("apply: vaqtinchalik papka qolmadi", st["stages_after"] == st["stages_before"]),
    ]


def case_update_begonani_saqlaydi():
    if not POSIX:
        return SKIP
    st = stsenariy()
    claude, after = st["claude"], st["after_update"]
    cmds, fs = commands_of(after), st["fs_update"]
    backup = os.path.join(st["home"], "zaxira-2")
    return [
        ("update: rc 0", st["update"].returncode == 0),
        ("update: begona hooklar va ruxsat saqlandi",
         "echo begona-hook" in cmds and "echo begona-hook-2" in cmds
         and "Bash(ls:*)" in after["permissions"]["allow"]
         and "Bash(git status:*)" in after["permissions"]["allow"]),
        ("update: o'z hooki ikkilanmadi",
         sum("suggest_sections.py" in c for c in cmds) == 1
         and cmds.count("echo begona-hook-2") == 1),
        ("update: begona skill va ikkinchi manguberdi/ yo'q",
         os.path.join(claude, "skills", "begona", "SKILL.md") in fs
         and os.path.join(claude, "skills", "manguberdi", "SKILL.md") in fs
         and os.path.join(claude, "skills", "manguberdi", "manguberdi") not in fs),
        ("update: begona aktyor joyida", "begona.md" in st["update_agents"]),
        ("update: zaxirada skills--manguberdi va .claude--settings.json",
         os.path.isdir(os.path.join(backup, "skills--manguberdi"))
         and os.path.isfile(os.path.join(backup, ".claude--settings.json"))),
    ]


def case_uninstall_faqat_ozini_oladi():
    if not POSIX:
        return SKIP
    st = stsenariy()
    claude, after = st["claude"], st["after_uninstall"]
    cmds, fs = commands_of(after), st["fs_uninstall"]
    root = st["snap"].lower()
    return [
        ("uninstall quruq: rc 0, hech narsa o'chmadi",
         st["uninstall_dry"].returncode == 0 and st["uninstall_dry_same"]
         and "quruq yurish" in st["uninstall_dry"].stdout),
        ("uninstall: rc 0", st["uninstall"].returncode == 0),
        ("uninstall: skill va aktyorlar ketdi",
         os.path.join(claude, "skills", "manguberdi") not in fs and not any(
             os.path.join(claude, "agents", a + ".md") in fs for a in I.ACTORS)),
        ("uninstall: begona skill, aktyor, CLAUDE.md qoldi",
         os.path.join(claude, "skills", "begona", "SKILL.md") in fs
         and os.path.join(claude, "agents", "begona.md") in fs
         and os.path.join(claude, "CLAUDE.md") in fs),
        ("uninstall: o'z hooki, ruxsati, env ketdi", not any(
            root in c.lower() for c in cmds)
         and "GENIUS_PYTHON" not in after.get("env", {})
         and not any(root in str(r).lower() for r in after["permissions"]["allow"])),
        ("uninstall: begona hook, ruxsat, kalit qoldi",
         "echo begona-hook" in cmds and "echo begona-hook-2" in cmds
         and "Bash(ls:*)" in after["permissions"]["allow"]
         and after.get("model") == "opus"),
        ("uninstall: zaxira yozildi", os.path.isfile(
            os.path.join(st["home"], "zaxira-3", ".claude--settings.json"))),
        ("uninstall: snapshot worktree olib tashlandi, klon reestri toza",
         st["genius_after_uninstall"] == [] and not os.path.exists(st["snap"])
         and len(st["worktrees_uninstall"].splitlines()) == 1
         and not any(st["klon"] in c or st["snap"] in c for c in cmds)
         and "GENIUS_CLONE" not in after.get("env", {})
         and not after.get("permissions", {}).get("additionalDirectories")),
    ]


def case_uninstall_klon_yoq():
    """Klon o'chgan: --genius-path mavjud emas va yo'lda `$` bor, baribir ishlaydi."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    gone = os.path.join(tmpdir("yoq_"), "o'chgan $klon")
    claude = os.path.join(home, ".claude")
    put(os.path.join(claude, "settings.json"), json.dumps({
        "model": "opus",
        "env": {"GENIUS_PYTHON": "/usr/bin/python3"},
        "hooks": {"Stop": [{"hooks": [
            {"type": "command", "command": '"/usr/bin/python3" "%s/tools/usage.py" || exit 1' % gone},
            {"type": "command", "command": "echo begona"}]}]},
        "permissions": {"allow": ["Bash(/usr/bin/python3 %s/tools/budget.py:*)" % gone,
                                  "Bash(git status:*)"]}}))
    put(os.path.join(claude, "skills", "manguberdi", "SKILL.md"), "x")
    res = run_install(home, "--uninstall", "--apply", "--genius-path", gone,
                      "--backup-to", os.path.join(home, "z"))
    data = jget(os.path.join(claude, "settings.json"))
    cmds = commands_of(data)
    return [
        ("klon yo'q: rc 0", res.returncode == 0),
        ("klon yo'q: o'z yozuvi ketdi",
         not any(gone in c for c in cmds) and "GENIUS_PYTHON" not in data.get("env", {})
         and data["permissions"]["allow"] == ["Bash(git status:*)"]),
        ("klon yo'q: begona qoldi", cmds == ["echo begona"] and data["model"] == "opus"),
        ("klon yo'q: skill ketdi", not os.path.exists(
            os.path.join(claude, "skills", "manguberdi"))),
    ]


def case_uninstall_snapshotni_va_faqat_genius_ostidagini():
    """--uninstall `~/.claude/genius/<sha12>` worktree larni olib tashlaydi,
    lekin begona papka va nom mos kelmaydigan yozuvga tegmaydi."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    klon = git_klon()
    res = run_install(home, "--apply", "--backup-to", os.path.join(home, "z1"))
    snap = snap_of(home, klon)
    genius = os.path.join(home, ".claude", "genius")
    put(os.path.join(genius, "begona", "x.txt"), "begona")
    put(os.path.join(genius, "aaaaaaaaaaaa", "x.txt"), "worktree emas, 12 hex")
    put(os.path.join(home, ".claude", "genius-memory", "m.md"), "memory")
    res2 = run_install(home, "--uninstall", "--apply", "--backup-to", os.path.join(home, "z2"))
    return [
        ("snapshot: o'rnatildi", res.returncode == 0 and snap in res.stdout),
        ("snapshot: --uninstall rc 0, worktree olindi, reestr toza",
         res2.returncode == 0 and not os.path.exists(snap)
         and len(testkit.git(klon, "worktree", "list").splitlines()) == 1),
        ("snapshot: begona papka, worktree emas 12 hex va genius-memory joyida",
         os.path.isfile(os.path.join(genius, "begona", "x.txt"))
         and os.path.isfile(os.path.join(genius, "aaaaaaaaaaaa", "x.txt"))
         and os.path.isfile(os.path.join(home, ".claude", "genius-memory", "m.md"))),
    ]


def case_uninstall_klon_ochgan_yetim_snapshot():
    """Klon o'chgan: snapshot yetim (asosiy .git yo'q), --uninstall uni ham va
    settings.json dagi yozuvlarini ham olib tashlaydi."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    klon = testkit.repo_nusxa(ROOT, os.path.join(tmpdir("eski_"), "klon"))
    res = run_install(home, "--apply", "--genius-path", klon,
                      "--backup-to", os.path.join(home, "z1"))
    snap = snap_of(home, klon)
    shutil.rmtree(os.path.dirname(klon))
    res2 = run_install(home, "--uninstall", "--apply", "--genius-path", klon,
                       "--backup-to", os.path.join(home, "z2"))
    data = jget(os.path.join(home, ".claude", "settings.json"))
    return [
        ("yetim: o'rnatildi, klon o'chdi", res.returncode == 0 and not os.path.exists(klon)),
        ("yetim: --uninstall rc 0 va snapshot ketdi", res2.returncode == 0
         and not os.path.exists(snap)),
        ("yetim: settings.json da o'z yozuvi qolmadi",
         not any(snap in c for c in commands_of(data))
         and "GENIUS_CLONE" not in data.get("env", {})
         and not data.get("permissions", {}).get("additionalDirectories")),
    ]


def case_eski_ornatishdan_otish():
    """Snapshotdan oldingi o'rnatish: hook, ruxsat va papkalar klonning tools/ iga
    bog'langan. Qayta o'rnatish ularni snapshotga o'tkazadi (ikkilanmaydi), begona
    yozuv qoladi."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    klon = git_klon()
    py = sys.executable
    eski = {
        "model": "opus",
        "env": {"GENIUS_PYTHON": py},
        "permissions": {
            "additionalDirectories": [klon, "D:/begona"],
            "allow": ["Bash(%s %s/tools/budget.py:*)" % (py, klon), "Bash(ls:*)"]},
        "hooks": {"UserPromptSubmit": [{"hooks": [
            {"type": "command", "command": '"%s" "%s/tools/suggest_sections.py" || exit 1'
             % (py, klon)},
            {"type": "command", "command": "echo begona"}]}]}}
    put(os.path.join(home, ".claude", "settings.json"), json.dumps(eski))
    res = run_install(home, "--apply", "--backup-to", os.path.join(home, "z"))
    data = jget(os.path.join(home, ".claude", "settings.json"))
    snap = snap_of(home, klon)
    cmds = commands_of(data)
    return [
        ("eski o'rnatish: rc 0", res.returncode == 0),
        ("eski o'rnatish: klonning tools/ iga hook qolmadi, snapshotga o'tdi, begona qoldi",
         not any((klon + "/tools/") in c for c in cmds)
         and sum("suggest_sections.py" in c and (snap + "/tools/") in c for c in cmds) == 1
         and "echo begona" in cmds),
        ("eski o'rnatish: ruxsat va papkalar almashdi, begonasi qoldi",
         not any((klon + "/tools/") in r for r in data["permissions"]["allow"])
         and "Bash(ls:*)" in data["permissions"]["allow"]
         and data["permissions"]["additionalDirectories"]
         == ["D:/begona", snap + "/docs", klon + "/memory"]
         and data["env"]["GENIUS_CLONE"] == klon and data["model"] == "opus"),
    ]


def case_git_bolmagan_klon_rad():
    """Pin qilish uchun commit kerak: git repo bo'lmasa hech narsa yozilmaydi."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    klon = os.path.join(tmpdir("gitsiz_"), "klon")
    shutil.copytree(ROOT, klon, symlinks=True, ignore=testkit.REPO_IGNORE)
    rows = []
    for args in ((), ("--apply",)):
        res = run_install(home, "--genius-path", klon, *args)
        rows.append(("git siz klon %s: rc 1, sabab aytildi" % " ".join(args),
                     res.returncode == 1 and "git repo" in res.stdout
                     and "Hech narsa o'zgarmadi" in res.stdout))
    rows.append(("git siz klon: ~/.claude yozilmadi",
                 not os.path.exists(os.path.join(home, ".claude"))))
    return rows


def case_genius_klon_ichiga_symlink_rad():
    """`~/.claude/genius` klon ichiga symlink bo'lsa worktree klon ichida
    yaratilardi: o'rnatish snapshot yasamasdan to'xtaydi."""
    if not POSIX:
        return SKIP
    klon = clone_nusxa()
    home = tmpdir("uy_")
    inner = os.path.join(klon, "ichki-snapshotlar")
    os.makedirs(inner)
    os.makedirs(os.path.join(home, ".claude"))
    os.symlink(inner, os.path.join(home, ".claude", "genius"))
    res = run_install(home, "--apply", "--genius-path", klon)
    return [
        ("genius symlink klon ichiga: rc 1, sabab aytildi",
         res.returncode == 1 and "klon ichida" in res.stdout),
        ("genius symlink: klon ichida worktree yaratilmadi",
         os.listdir(inner) == [] and len(testkit.git(klon, "worktree", "list").splitlines()) == 1),
    ]


def case_xavfli_yol_toxtatadi():
    """R7.8 XV-P2: `$`, backtick yoki qo'shtirnoqli yo'lda hech narsa yozilmaydi."""
    if not POSIX:
        return SKIP
    rows = []
    for name in ("a$b", "a`b", 'a"b'):
        home = tmpdir("uy_")
        bad = os.path.join(tmpdir("klon_"), name)
        os.makedirs(bad)
        for args in ((), ("--apply",)):
            res = run_install(home, "--genius-path", bad, *args)
            rows.append(("xavfli yo'l %r %s: rc 1, sabab aytildi" % (name, " ".join(args)),
                         res.returncode == 1 and "$, backtick" in res.stdout))
        rows.append(("xavfli yo'l %r: ~/.claude yozilmadi" % name,
                     not os.path.exists(os.path.join(home, ".claude"))))
    return rows


def case_rad_etiladigan_birikmalar():
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    put(os.path.join(home, ".claude", "CLAUDE.md"), "eski")
    before = snapshot(home)
    cases = [
        (("--reset", "--apply"), "--confirm-reset"),
        (("--include-auth",), "faqat --reset bilan"),
        (("--project", home), "faqat --reset bilan"),
        (("--uninstall", "--reset"), "berilmaydi"),
        (("--update", "--reset"), "berilmaydi"),
        (("--confirm-reset",), "faqat --reset bilan"),
        (("--reset", "--project", home), "klon yoki uy papkasi"),
    ]
    rows = []
    for args, text in cases:
        res = run_install(home, *args)
        rows.append(("rad: %s" % " ".join(args), res.returncode == 1 and text in res.stdout))
    rows.append(("rad: uy papkasi o'zgarmadi", snapshot(home) == before))
    saved = os.environ.get("CLAUDE_CONFIG_DIR")
    res = testkit.call_main(I.main, argv=["install.py"],
                            env={"HOME": home, "CLAUDE_CONFIG_DIR": "/tmp/boshqa"})
    rows.append(("rad: CLAUDE_CONFIG_DIR", res.returncode == 1
                 and "CLAUDE_CONFIG_DIR" in res.stdout
                 and os.environ.get("CLAUDE_CONFIG_DIR") == saved))
    zaxira = os.path.join(home, "zaxira")
    put(os.path.join(zaxira, "eski.txt"), "avvalgi zaxira")
    res = run_install(home, "--backup-to", zaxira)
    rows.append(("rad: bo'sh bo'lmagan zaxira papkasi", res.returncode == 1
                 and "bo'sh emas" in res.stdout))
    return rows


def case_reset_tasdiq_bilan():
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    claude = os.path.join(home, ".claude")
    put(os.path.join(claude, "CLAUDE.md"), "reset-sinovi")
    put(os.path.join(claude, "skills", "begona2", "SKILL.md"), "begona")
    put(os.path.join(claude, "projects", "p", "tarix.jsonl"), "{}")
    put(os.path.join(claude, ".credentials.json"), "{}")
    put(os.path.join(home, ".claude.json"), '{"mcpServers": {"m": {}}}')
    project = tmpdir("proyekt_")
    put(os.path.join(project, ".claude", "x.md"), "x")

    dry = run_install(home, "--reset", "--include-auth", "--project", project)
    dry_ok = (dry.returncode == 0 and ".claude.json" in dry.stdout
              and os.path.join(project, ".claude") in dry.stdout
              and os.path.isfile(os.path.join(claude, "CLAUDE.md")))

    zaxira = os.path.join(home, "reset-zaxira")
    res = run_install(home, "--reset", "--apply", "--confirm-reset", "--backup-to", zaxira)
    return [
        ("reset quruq: ro'yxat, hech narsa o'chmadi", dry_ok),
        ("reset: rc 0", res.returncode == 0),
        ("reset: eski CLAUDE.md va begona skill ketdi",
         not os.path.exists(os.path.join(claude, "CLAUDE.md"))
         and not os.path.exists(os.path.join(claude, "skills", "begona2"))),
        ("reset: skill va aktyorlar o'rnatildi",
         os.path.isfile(os.path.join(claude, "skills", "manguberdi", "SKILL.md"))
         and os.path.isfile(os.path.join(claude, "agents", "review.md"))),
        ("reset: tarix, kirish tokeni, .claude.json qoldi",
         os.path.isfile(os.path.join(claude, "projects", "p", "tarix.jsonl"))
         and os.path.isfile(os.path.join(claude, ".credentials.json"))
         and os.path.isfile(os.path.join(home, ".claude.json"))),
        ("reset: proyekt .claude/ tegilmadi (--project berilmagan)",
         os.path.isfile(os.path.join(project, ".claude", "x.md"))),
        ("reset: zaxirada .claude--CLAUDE.md va .claude--skills",
         os.path.isfile(os.path.join(zaxira, ".claude--CLAUDE.md"))
         and os.path.isdir(os.path.join(zaxira, ".claude--skills"))),
    ]


def case_symlink_zaxirasi():
    """Katalogga va singan symlink: traceback yo'q, zaxirada symlink, nishon joyida."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    claude = os.path.join(home, ".claude")
    target = tmpdir("nishon_")
    put(os.path.join(target, "SKILL.md"), "begona skill nishoni")
    os.makedirs(os.path.join(claude, "skills"))
    os.makedirs(os.path.join(claude, "agents"))
    os.symlink(target, os.path.join(claude, "skills", "manguberdi"))
    os.symlink(os.path.join(target, "yoq.md"), os.path.join(claude, "agents", "qidiruv.md"))
    zaxira = os.path.join(home, "z")
    res = run_install(home, "--apply", "--backup-to", zaxira)
    link = os.path.join(zaxira, "skills--manguberdi")
    broken = os.path.join(zaxira, "agents--qidiruv.md")
    return [
        ("symlink: rc 0, traceback yo'q", res.returncode == 0 and "Traceback" not in res.stdout + res.stderr),
        ("symlink: zaxirada havola havola bo'lib turadi",
         os.path.islink(link) and os.readlink(link) == target
         and os.path.islink(broken) and os.readlink(broken) == os.path.join(target, "yoq.md")),
        ("symlink: nishon papka o'chmadi, skill haqiqiy papka bo'ldi",
         os.path.isfile(os.path.join(target, "SKILL.md"))
         and not os.path.islink(os.path.join(claude, "skills", "manguberdi"))
         and os.path.isfile(os.path.join(claude, "skills", "manguberdi", "SKILL.md"))),
        ("symlink: singan havola o'rniga aktyor fayli",
         not os.path.islink(os.path.join(claude, "agents", "qidiruv.md"))
         and os.path.isfile(os.path.join(claude, "agents", "qidiruv.md"))),
    ]


def clone_nusxa():
    """Klonning vaqtinchalik nusxasi: symlink rad etilmasa buzilishi mumkin bo'lgan
    manba fayllari reponing o'zida emas, shu nusxada bo'lsin."""
    if not _CLONE:
        # Git repo: snapshot (R7.8 XV-Y1) klon git repo bo'lishini talab qiladi.
        _CLONE.append(testkit.repo_nusxa(ROOT, os.path.join(tmpdir("klon_"), "klon")))
    return _CLONE[0]


def case_klon_ichiga_symlink_rad():
    if not POSIX:
        return SKIP
    rows = []
    klon = clone_nusxa()
    manba = os.path.join(klon, ".claude", "agents")
    before = {n: get(os.path.join(manba, n)) for n in os.listdir(manba)}
    for rel_name, target in (("agents", manba),
                             ("skills/manguberdi",
                              os.path.join(klon, ".claude", "skills", "manguberdi"))):
        home = tmpdir("uy_")
        link = os.path.join(home, ".claude", *rel_name.split("/"))
        os.makedirs(os.path.dirname(link))
        os.symlink(target, link)
        for args in ((), ("--apply",), ("--uninstall", "--apply")):
            res = run_install(home, "--genius-path", klon, *args)
            rows.append(("klon ichiga symlink (%s) %s: rc 1, sabab aytildi"
                         % (rel_name, " ".join(args)),
                         res.returncode == 1 and "klon ichida" in res.stdout))
    rows.append(("klon ichiga symlink: klonning aktyor fayllari o'zgarmadi",
                 before == {n: get(os.path.join(manba, n)) for n in os.listdir(manba)}))
    return rows


def case_backup_ornatiladigan_ichida_rad():
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    skill = os.path.join(home, ".claude", "skills", "manguberdi")
    put(os.path.join(skill, "SKILL.md"), "x")
    res = run_install(home, "--apply", "--backup-to", os.path.join(skill, "z"))
    res2 = run_install(home, "--uninstall", "--apply", "--backup-to", os.path.join(skill, "z"))
    return [
        ("--backup-to o'chiriladigan birlik ichida: rad", res.returncode == 1
         and "o'chiriladigan birlik ichida" in res.stdout),
        ("--backup-to o'chiriladigan birlik ichida (--uninstall): rad", res2.returncode == 1
         and "o'chiriladigan birlik ichida" in res2.stdout),
        ("--backup-to rad: skill joyida, zaxira yozilmadi",
         os.path.isfile(os.path.join(skill, "SKILL.md")) and not os.path.exists(os.path.join(skill, "z"))),
    ]


def case_uninstall_manifest_boyicha():
    """Manifest bo'lsa faqat undagi aktyorlar olinadi; yo'q bo'lsa nom bo'yicha va ogohlantirish."""
    if not POSIX:
        return SKIP
    rows = []
    home = tmpdir("uy_")
    claude = os.path.join(home, ".claude")
    put(os.path.join(claude, "skills", "manguberdi", "SKILL.md"), "x")
    put(os.path.join(claude, "skills", "manguberdi", ".genius.json"),
        json.dumps({"actors": ["qidiruv", "tahlil"]}))
    for name in ("qidiruv", "tahlil", "review"):
        put(os.path.join(claude, "agents", name + ".md"), name)
    res = run_install(home, "--uninstall", "--apply", "--backup-to", os.path.join(home, "z"))
    rows += [
        ("manifest: rc 0", res.returncode == 0),
        ("manifest: faqat manifestdagi aktyorlar va skill ketdi",
         not os.path.exists(os.path.join(claude, "agents", "qidiruv.md"))
         and not os.path.exists(os.path.join(claude, "agents", "tahlil.md"))
         and not os.path.exists(os.path.join(claude, "skills", "manguberdi"))),
        ("manifest: begona review.md qoldi, ogohlantirish yo'q",
         get(os.path.join(claude, "agents", "review.md")) == "review"
         and "OGOHLANTIRISH" not in res.stdout),
    ]
    home = tmpdir("uy_")
    claude = os.path.join(home, ".claude")
    put(os.path.join(claude, "skills", "manguberdi", "SKILL.md"), "x")
    put(os.path.join(claude, "agents", "review.md"), "review")
    put(os.path.join(claude, "agents", "begona.md"), "begona")
    res = run_install(home, "--uninstall", "--apply", "--backup-to", os.path.join(home, "z"))
    rows += [
        ("manifest yo'q: nom bo'yicha olindi, begonasi qoldi",
         res.returncode == 0 and not os.path.exists(os.path.join(claude, "agents", "review.md"))
         and os.path.isfile(os.path.join(claude, "agents", "begona.md"))),
        ("manifest yo'q: har fayl uchun ogohlantirish",
         "OGOHLANTIRISH: manifest yo'q" in res.stdout and "review.md" in res.stdout),
    ]
    return rows


def case_uy_papka_rad():
    if not POSIX:
        return SKIP
    rows = []
    for value in ("", "/", "//"):
        res = testkit.call_main(I.main, argv=["install.py", "--apply"],
                                env={"HOME": value, "CLAUDE_CONFIG_DIR": None})
        rows.append(("HOME=%r: rad etildi, traceback yo'q" % value,
                     res.returncode == 1 and "uy papkasi" in res.stdout))
    return rows


def case_reset_include_auth_va_project_apply():
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    claude = os.path.join(home, ".claude")
    put(os.path.join(claude, "CLAUDE.md"), "eski")
    put(os.path.join(claude, "projects", "p", "tarix.jsonl"), "{}")
    put(os.path.join(home, ".claude.json"), '{"mcpServers": {"m": {}}}')
    project = tmpdir("proyekt_")
    put(os.path.join(project, ".claude", "x.md"), "x")
    put(os.path.join(project, "CLAUDE.md"), "proyekt")
    zaxira = os.path.join(home, "z")
    res = run_install(home, "--reset", "--apply", "--confirm-reset", "--include-auth",
                      "--project", project, "--backup-to", zaxira)
    saved = sorted(os.listdir(zaxira)) if os.path.isdir(zaxira) else []
    return [
        ("reset --include-auth --project --apply: rc 0", res.returncode == 0),
        ("~/.claude.json va proyekt .claude/ o'chdi",
         not os.path.exists(os.path.join(home, ".claude.json"))
         and not os.path.exists(os.path.join(project, ".claude"))),
        ("proyektning CLAUDE.md va tarix qoldi",
         get(os.path.join(project, "CLAUDE.md")) == "proyekt"
         and os.path.isfile(os.path.join(claude, "projects", "p", "tarix.jsonl"))),
        ("zaxirada .claude.json va proyekt .claude/ bor",
         any(n.endswith("--.claude.json") for n in saved)
         and any(n.endswith("--.claude") and n != ".claude--.claude" for n in saved)
         and ".claude--CLAUDE.md" in saved),
        ("skill o'rnatildi", os.path.isfile(os.path.join(claude, "skills", "manguberdi", "SKILL.md"))),
    ]


# --- Windows rejimi (`--platforma nt`) -----------------------------------

# OLTIN qiymat: asos commit 89133b10982c dagi manguberdi.ps1 matnidan bir marta
# chiqarilgan. Kirish: Python `C:\Python312\python.exe`, snapshot
# `C:/Users/u/.claude/genius/0123456789ab`, klon `C:/src/claude-genius`. ps1
# HookCmd: `'"{0}" "{1}/{2}"' -f $PythonExe, $snapTools, $script` va oxirida
# ` || exit 1` (handoff va usage argumenti suffiksdan oldin). Hook buyrug'ida
# Python teskari slash bilan, env.GENIUS_PYTHON va manifestda `/` bilan.
GOLDEN_SNAP = "C:/Users/u/.claude/genius/0123456789ab"
GOLDEN_CLONE = "C:/src/claude-genius"
GOLDEN_TOP = ["$schema", "env", "permissions", "hooks"]
GOLDEN_ENV = {"GENIUS_PYTHON": "C:/Python312/python.exe", "GENIUS_CLONE": "C:/src/claude-genius"}
GOLDEN_DIRS = ["C:/Users/u/.claude/genius/0123456789ab/docs", "C:/src/claude-genius/memory"]
GOLDEN_HOOKS = [
    ('UserPromptSubmit', '',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/suggest_sections.py" || exit 1',
     10, "Mos bo'limlar qidirilmoqda"),
    ('UserPromptSubmit', '',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/budget.py" || exit 1',
     10, ''),
    ('UserPromptSubmit', '',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/handoff.py" --hook || exit 1',
     10, "Kontekst o'lchanmoqda"),
    ('PreToolUse', 'Read|Bash|PowerShell',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/guard.py" || exit 1',
     10, 'Qimmat amal tekshirilmoqda'),
    ('PreToolUse', 'Task|Agent|SendMessage',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/budget.py" || exit 1',
     10, 'Aktyor budjeti tekshirilmoqda'),
    ('SubagentStop', '',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/actor_check.py" || exit 1',
     10, 'Aktyor natijasi tekshirilmoqda'),
    ('PostToolUse', 'Write|Edit',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/check_code.py" || exit 1',
     15, 'Java qoidalari tekshirilmoqda'),
    ('Stop', '',
     '"C:\\Python312\\python.exe" "C:/Users/u/.claude/genius/0123456789ab/tools/usage.py" --saqlash || exit 1',
     20, 'Token sarfi yozilmoqda'),
]
GOLDEN_MANIFEST_KEYS = ["versiya", "commit", "sana", "root", "clone", "python", "actors"]


def flat_hooks(settings):
    return [(event, group.get("matcher", ""), hook["command"], hook.get("timeout"),
             hook.get("statusMessage", ""))
            for event, groups in settings["hooks"].items()
            for group in groups for hook in group["hooks"]]


def case_windows_oltin_qiymat():
    """Windows shakli (Python teskari slashli, env `/` bilan) ilgari ps1 bergan
    settings.json ga teng: hook buyruqlari, tartib, env, papkalar, kalit tartibi."""
    got = I.sozlama_yasa(WIN_PY, GOLDEN_SNAP, ["Bash(x)"], GOLDEN_CLONE, WIN_PY_FWD)
    hooks = flat_hooks(got)
    return [
        ("oltin: hook buyruqlari ps1 ning HookCmd shakli va tartibi bilan bir xil "
         "(farq: %s)" % [h for h in hooks if h not in GOLDEN_HOOKS],
         hooks == GOLDEN_HOOKS),
        ("oltin: env.GENIUS_PYTHON `/` bilan, GENIUS_CLONE klon", got["env"] == GOLDEN_ENV),
        ("oltin: additionalDirectories snapshot docs va klon memory",
         got["permissions"]["additionalDirectories"] == GOLDEN_DIRS
         and got["permissions"]["allow"] == ["Bash(x)"]),
        ("oltin: yuqori kalitlar tartibi", list(got) == GOLDEN_TOP
         and got["$schema"] == "https://json.schemastore.org/claude-code-settings.json"),
    ]


def case_windows_platforma_funksiyalari():
    """Platforma: ajratgich, uy papkasi, managed yo'llari, bash izlash."""
    nt, posix = I.Platforma("nt"), I.Platforma("posix")
    saved = {k: os.environ.get(k) for k in
             ("USERPROFILE", "HOMEDRIVE", "HOMEPATH", "ProgramFiles", "ProgramData")}
    try:
        os.environ["USERPROFILE"] = "C:\\Users\\u"
        home = nt.uy()
        os.environ.pop("USERPROFILE")
        os.environ["HOMEDRIVE"], os.environ["HOMEPATH"] = "D:", "\\h"
        home2 = nt.uy()
        os.environ["ProgramFiles"], os.environ["ProgramData"] = "C:\\PF", "C:\\PD"
        managed = [m.replace("\\", "/") for m in nt.managed_yollar()]
        os.environ.pop("ProgramFiles")
        managed2 = [m.replace("\\", "/") for m in nt.managed_yollar()]
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    return [
        ("platforma: fwd Windows da `\\` ni `/` ga, POSIX da tegmaydi",
         nt.fwd("C:\\a\\b") == "C:/a/b" and posix.fwd("/a\\b") == "/a\\b"),
        ("platforma: kes ildizni saqlaydi", nt.kes("C:\\a\\b\\") == "C:\\a\\b"
         and nt.kes("C:\\") == "C:\\" and nt.kes("C:/a//") == "C:/a"
         and posix.kes("/a/b/") == "/a/b" and posix.kes("/") == "/"),
        ("platforma: uy USERPROFILE, bo'lmasa HOMEDRIVE+HOMEPATH",
         home == "C:\\Users\\u" and home2 == "D:\\h"),
        ("platforma: uy ildiz papka rad", not nt.uy_yaroqli("") and not posix.uy_yaroqli("/")
         and not posix.uy_yaroqli("rel") and not nt.uy_yaroqli("/")
         and posix.uy_yaroqli("/home/u")),
        ("platforma: managed yo'llari ProgramFiles va ProgramData",
         managed == ["C:/PF/ClaudeCode/managed-settings.json",
                     "C:/PD/ClaudeCode/managed-settings.json"]
         and managed2 == ["C:/PD/ClaudeCode/managed-settings.json"]
         and all(m.startswith("/") for m in posix.managed_yollar())),
        ("platforma: bash tashqaridan berilsa o'sha", nt.bash_top("D:/Git/bin/bash.exe")
         == "D:/Git/bin/bash.exe"),
        ("platforma: Python nomi", nt.python_nomi() == "python" and posix.python_nomi() == "python3"),
    ]


def case_windows_bash_izlash():
    """Windows da PATH dagi bash: System32 va WindowsApps (WSL) rad, boshqasi olinadi."""
    if not POSIX:
        return SKIP
    nt = I.Platforma("nt")
    base = tmpdir("bash_")
    wsl = os.path.join(base, "Windows", "System32")
    store = os.path.join(base, "WindowsApps")
    git = os.path.join(base, "Git", "usr", "bin")
    for folder in (wsl, store, git):
        put(os.path.join(folder, "bash.exe"), "x")
    saved = os.environ.get("PATH")
    try:
        os.environ["PATH"] = os.pathsep.join([wsl, store])
        only_wsl = nt.bash_top()
        os.environ["PATH"] = os.pathsep.join([wsl, store, git])
        found = nt.bash_top()
    finally:
        os.environ["PATH"] = saved
    return [
        ("bash izlash: faqat System32 va WindowsApps bo'lsa topilmadi", only_wsl is None),
        ("bash izlash: WSL dan keyingi haqiqiy bash olinadi",
         found == os.path.join(git, "bash.exe")),
    ]


def case_windows_ps1_xabar_bayroqlari():
    """--ps1 bilan xabarlarda PowerShell bayroqlari; ps1 siz o'z shakli."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    rows = []
    for ps1, want, not_want in ((True, "-ConfirmReset", "--confirm-reset"),
                                (False, "--confirm-reset", "-ConfirmReset")):
        argv = ["--reset", "--apply", "--platforma", "nt"] + (["--ps1"] if ps1 else [])
        res = testkit.call_main(I.main, argv=["install.py"] + argv + ["--genius-path", git_klon()],
                                env=nt_muhit(home))
        rows.append(("xabar %s: rc 1, %s bor, %s yo'q" % ("ps1" if ps1 else "oddiy", want, not_want),
                     res.returncode == 1 and want in res.stdout
                     and not_want not in res.stdout.replace("-" + want.lstrip("-"), "")
                     if ps1 else res.returncode == 1 and want in res.stdout))
    rows.append(("xabar: uy papkasi yozilmadi", not os.path.exists(os.path.join(home, ".claude"))))
    return rows


def case_windows_rad_etiladigan_birikmalar():
    """ps1 dagi rad etishlar Windows rejimida ham: CI Windows qadamlari shunga tayanadi."""
    if not POSIX:
        return SKIP
    home = tmpdir("uy_")
    rows = []
    for args, text in (((["--reset", "--apply"]), "-ConfirmReset"),
                       ((["--include-auth"]), "faqat -Reset bilan"),
                       ((["--uninstall", "--reset"]), "berilmaydi")):
        res = run_install(home, *args, nt=True)
        rows.append(("windows rad: %s" % " ".join(args),
                     res.returncode == 1 and text in res.stdout))
    saved = os.environ.get("CLAUDE_CONFIG_DIR")
    env = nt_muhit(home)
    env["CLAUDE_CONFIG_DIR"] = "C:\\boshqa"
    res = testkit.call_main(I.main, argv=["install.py", "--genius-path", git_klon()] + nt_argv(),
                            env=env)
    rows.append(("windows rad: CLAUDE_CONFIG_DIR", res.returncode == 1
                 and "CLAUDE_CONFIG_DIR" in res.stdout
                 and os.environ.get("CLAUDE_CONFIG_DIR") == saved))
    for value in ("", "/", "\\"):
        env = nt_muhit(home)
        env["USERPROFILE"] = value
        env["HOME"] = value
        env.update({"HOMEPATH": None, "HOMEDRIVE": None})
        res = testkit.call_main(I.main, argv=["install.py", "--apply", "--genius-path", git_klon()]
                                + nt_argv(), env=env)
        rows.append(("windows uy=%r: rad, traceback yo'q" % value, res.returncode == 1
                     and "uy papkasi" in res.stdout and "USERPROFILE" in res.stdout))
    res = run_install(home, "--apply", nt=True, **{}) if False else None
    bad = os.path.join(tmpdir("klon_"), "a$b")
    os.makedirs(bad)
    res = run_install(home, "--genius-path", bad, nt=True)
    rows.append(("windows xavfli yo'l: rc 1", res.returncode == 1 and "$, backtick" in res.stdout))
    res = testkit.call_main(
        I.main, argv=["install.py", "--genius-path", git_klon(), "--platforma", "nt",
                      "--bash", os.path.join(home, "yoq-bash.exe")], env=nt_muhit(home))
    rows.append(("windows: berilgan --bash fayli yo'q: rad", res.returncode == 1
                 and "--bash fayli topilmadi" in res.stdout))
    rows.append(("windows rad: uy papkasi yozilmadi", not os.path.exists(os.path.join(home, ".claude"))))
    return rows


def case_windows_quruq_yurish():
    if not POSIX:
        return SKIP
    st = stsenariy(nt=True)
    out = st["dry"].stdout
    pf_managed = os.path.join(_NT["pf"], "ClaudeCode", "managed-settings.json")
    return [
        ("windows quruq: rc 0, ro'yxat chiqdi",
         st["dry"].returncode == 0 and "quruq yurish" in out and "o'rnatilmoqda" in out),
        ("windows quruq: bayroq PowerShell shaklida (-Apply)",
         "-Apply bermadingiz" in out and "--apply" not in out),
        ("windows quruq: uy, indeks, vaqtinchalik papka, klonning .git i o'zgarmadi",
         st["dry_same"] and st["dry_git_same"] and st["dry_no_genius"]),
        ("windows quruq: uy USERPROFILE dan (HOME dagi boshqa papkaga tegilmadi)",
         ("Global: %s" % st["claude"]) in out and os.listdir(_NT["decoy"]) == []),
        ("windows quruq: managed sozlama ogohlantirishi ProgramFiles dan",
         "DIQQAT: %s topildi" % pf_managed in out),
        ("windows quruq: python Windows shaklida, bash tashqaridan",
         ("Python: %s" % WIN_PY) in out and ("Bash  : %s" % nt_argv()[-1]) in out
         and ("python: %s" % WIN_PY_FWD) in out),
    ]


def case_windows_apply_ornatadi():
    if not POSIX:
        return SKIP
    st = stsenariy(nt=True)
    claude, after = st["claude"], st["after_apply"]
    cmds = commands_of(after)
    own = [c for c in cmds if "begona" not in c]
    manifest = st["manifest"]
    return [
        ("windows apply: rc 0", st["apply"].returncode == 0),
        ("windows apply: hook buyrug'i Python teskari slash bilan, yo'l snapshotga `/` bilan",
         len(own) >= 7 and all(c.startswith('"%s" "%s/tools/' % (WIN_PY, st["snap"]))
                               and c.endswith(" || exit 1") for c in own)),
        ("windows apply: env.GENIUS_PYTHON `/` bilan, GENIUS_CLONE klon",
         after["env"] == {"GENIUS_PYTHON": WIN_PY_FWD, "GENIUS_CLONE": st["klon"]}),
        ("windows apply: manifest kalitlari, root snapshot, python `/` bilan",
         list(manifest) == GOLDEN_MANIFEST_KEYS and manifest["root"] == st["snap"]
         and manifest["clone"] == st["klon"] and manifest["python"] == WIN_PY_FWD
         and manifest["commit"] == st["head"]),
        ("windows apply: skill matni Pythonni `/` bilan, tools/ snapshotga, memory/ klonga",
         ("%s %s/tools/rules_for.py" % (WIN_PY_FWD, st["snap"])) in st["skill_text"]
         and ("%s/memory/" % st["klon"]) in st["skill_text"]),
        ("windows apply: snapshot, indeks, begona yozuvlar, BOM yo'q",
         st["snap_index_apply"] and "guard.py" in st["snap_tools_apply"]
         and os.path.join(claude, "CLAUDE.md") in st["fs_apply"] and st["claude_md"] == "eski"
         and "echo begona-hook" in cmds and after.get("model") == "opus"
         and not st["after_apply_raw"].startswith(b"\xef\xbb\xbf")),
        ("windows apply: eski aktyor olindi, begonasi qoldi",
         "arxitektor.md" not in st["apply_agents"] and "begona.md" in st["apply_agents"]
         and all(a + ".md" in st["apply_agents"] for a in I.ACTORS)),
        ("windows apply: vaqtinchalik papka qolmadi, HOME dagi boshqa papkaga tegilmadi",
         st["stages_after"] == st["stages_before"] and os.listdir(_NT["decoy"]) == []),
        ("windows apply: oxirida PowerShell shaklidagi yangilash buyrug'i `python`",
         ("python %s/tools/yangilash.py" % st["snap"]) in st["apply"].stdout),
    ]


def case_windows_update_va_uninstall():
    if not POSIX:
        return SKIP
    st = stsenariy(nt=True)
    after, gone = st["after_update"], st["after_uninstall"]
    cmds, fs = commands_of(after), st["fs_uninstall"]
    claude = st["claude"]
    root = st["snap"].lower()
    return [
        ("windows update: rc 0, begona hooklar va ruxsat saqlandi, o'z hooki ikkilanmadi",
         st["update"].returncode == 0 and "echo begona-hook" in cmds
         and "echo begona-hook-2" in cmds and "Bash(ls:*)" in after["permissions"]["allow"]
         and sum("suggest_sections.py" in c for c in cmds) == 1),
        ("windows update: Windows shaklidagi hook qayta yozildi",
         all(c.startswith('"%s" "%s/tools/' % (WIN_PY, st["snap"]))
             for c in cmds if "begona" not in c and "tools/" in c)),
        ("windows uninstall: quruq yurish va haqiqiy rc 0",
         st["uninstall_dry"].returncode == 0 and st["uninstall_dry_same"]
         and st["uninstall"].returncode == 0),
        ("windows uninstall: skill, aktyorlar va snapshot ketdi, begona qoldi",
         os.path.join(claude, "skills", "manguberdi") not in fs
         and not any(os.path.join(claude, "agents", a + ".md") in fs for a in I.ACTORS)
         and os.path.join(claude, "skills", "begona", "SKILL.md") in fs
         and os.path.join(claude, "CLAUDE.md") in fs
         and st["genius_after_uninstall"] == [] and not os.path.exists(st["snap"])),
        ("windows uninstall: o'z hooki, env, papkalar ketdi, begonasi qoldi",
         not any(root in c.lower() for c in commands_of(gone))
         and "GENIUS_PYTHON" not in gone.get("env", {}) and "GENIUS_CLONE" not in gone.get("env", {})
         and not gone.get("permissions", {}).get("additionalDirectories")
         and "echo begona-hook" in commands_of(gone) and gone.get("model") == "opus"),
        ("windows: HOME dagi boshqa papkaga tegilmadi", os.listdir(_NT["decoy"]) == []),
    ]


def norm_settings(st, py_text):
    """Ikki stsenariyning farqli yo'llari (uy, Python) bir xil belgiga."""
    text = json.dumps(st["after_apply"], sort_keys=True)
    for value, mark in ((json.dumps(py_text)[1:-1], "<PY>"), (py_text, "<PY>"),
                        (st["home"], "<UY>")):
        text = text.replace(value, mark)
    return text


def case_paritet_ikki_platforma():
    """install.py ning ikki platforma uchun chiqishi: Python va uy yo'lini
    belgilab qo'ysak settings.json, manifest va skill matni bir xil; hook buyrug'idagi
    Python ham ikkala shaklda o'sha yo'l (POSIX da farq yo'q, Windows da faqat ajratgich)."""
    if not POSIX:
        return SKIP
    posix, nt = stsenariy(), stsenariy(nt=True)

    def mark(text, st, py):
        for value, label in ((json.dumps(py)[1:-1], "<PY>"), (py, "<PY>"),
                             (st["home"], "<UY>")):
            text = text.replace(value, label)
        return text

    nt_settings = json.dumps(nt["after_apply"], sort_keys=True).replace(
        json.dumps(WIN_PY)[1:-1], WIN_PY_FWD)
    same_settings = mark(json.dumps(posix["after_apply"], sort_keys=True), posix, sys.executable) \
        == mark(nt_settings, nt, WIN_PY_FWD)
    same_skill = mark(posix["skill_text"], posix, sys.executable) \
        == mark(nt["skill_text"], nt, WIN_PY_FWD)
    pm, nm = dict(posix["manifest"]), dict(nt["manifest"])
    for m in (pm, nm):
        m.pop("sana")
    same_manifest = mark(json.dumps(pm, sort_keys=True), posix, sys.executable) \
        == mark(json.dumps(nm, sort_keys=True), nt, WIN_PY_FWD)
    return [
        ("paritet: settings.json ikki platformada bir xil (Python, uy belgilanganda)", same_settings),
        ("paritet: skill matni bir xil", same_skill),
        ("paritet: manifest bir xil (sana bundan mustasno)", same_manifest),
        ("paritet: ruxsat qoidalari bir xil",
         mark(json.dumps(posix["after_apply"]["permissions"], sort_keys=True), posix,
              sys.executable)
         == mark(json.dumps(nt["after_apply"]["permissions"], sort_keys=True), nt, WIN_PY_FWD)),
        ("paritet: oldingi aktyorlar va fayl daraxti bir xil", posix["apply_agents"]
         == nt["apply_agents"] and len(posix["fs_apply"]) == len(nt["fs_apply"])),
    ]


def case_windows_rewrite_chaqiruvlari():
    """Yo'l almashtirish asbobiga Windows shaklida beriladigan argumentlar eski ps1
    bilan bir xil: `--root <snapshot> --clone <klon> --root-keyin --python <py `/`>
    --bash bash`; `--clone` klon o'z shaklida."""
    if not POSIX:
        return SKIP
    calls = []
    real = I.run_py

    def spy(args, input_text=None, env=None):
        calls.append(list(args))
        return real(args, input_text, env)

    home = tmpdir("uy_")
    I.run_py = spy
    try:
        res = run_install(home, nt=True)
    finally:
        I.run_py = real
    rewriter = [c for c in calls if os.path.basename(c[0]) == "rewrite_paths.py"]
    snap = snap_of(home, git_klon())
    want = ["--root", snap, "--clone", git_klon(), "--root-keyin",
            "--python", WIN_PY_FWD, "--bash", "bash"]
    return [
        ("rewrite: rc 0", res.returncode == 0),
        ("rewrite: beshta chaqiruv (2 papka x 2, --allow, --opt-in: jami 6)", len(rewriter) == 6),
        ("rewrite: --python `/` bilan, --bash nomi, --clone klon, --root snapshot",
         bool(rewriter) and all(c[2:2 + len(want)] == want for c in rewriter
                                if "--tekshir" not in c)),
        ("rewrite: --tekshir chaqiruvi ham --root va --clone bilan",
         any(c[2:7] == want[:5] and c[-1] == "--tekshir" for c in rewriter)),
        ("rewrite: --allow va --opt-in", any(c[-1] == "--allow" for c in rewriter)
         and any(c[-1] == "--opt-in" for c in rewriter)),
    ]


# --- ps1 yupqa o'ram: faqat matn ------------------------------------------

def ps1_text():
    return get(os.path.join(ROOT, "install", "manguberdi.ps1"))


def ps1_code():
    """Izoh bloki (`<# ... #>`) va `#` izohlarsiz kod qatorlari."""
    text = re.sub(r"<#.*?#>", "", ps1_text(), flags=re.S)
    return [ln for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]


def case_ps1_yupqa_oram():
    """R7.2: ps1 faqat Windows ga xos ish qiladi va install.py ni chaqiradi.
    O'rnatish mantig'i (hook jadvali, JSON, snapshot, birlashtirish, zaxira) unda yo'q."""
    text, lines = ps1_text(), ps1_code()
    code = "\n".join(lines)
    logic = ("ConvertTo-Json", "ConvertFrom-Json", "HookCmd", "merge_settings", "rewrite_paths",
             "snapshot.py", "uninstall_settings", "Remove-Item", "Copy-Item", "WriteAllText",
             "$ConfigItems", "$Actors", "$Retired", "$Required", "Test-SafePath", "git ")
    windows = ("'py', '-3'", "System32|WindowsApps", "\\Git\\bin\\bash.exe",
               "Find-Python", "Find-GitBash", "'--bash'", "'--ps1'", "$LASTEXITCODE",
               "$PSScriptRoot", "GetUnresolvedProviderPathFromPSPath", "Set-ExecutionPolicy")
    return [
        ("ps1 o'ram: o'rnatish mantig'i yo'q (%s)" % [w for w in logic if w in code],
         not any(w in code for w in logic)),
        ("ps1 o'ram: Windows ga xos qismlar qoldi (yo'q: %s)" % [w for w in windows if w not in text],
         all(w in text for w in windows)),
        ("ps1 o'ram: install.py ni chaqiradi va chiqish kodini qaytaradi",
         "& $PythonExe @pyArgs" in code and "exit $LASTEXITCODE" in code
         and "'install.py'" in code),
        ("ps1 o'ram: 300 qatordan oshmaydi (jami %d, kod %d)" % (len(text.splitlines()), len(lines)),
         len(text.splitlines()) < 300 and len(lines) < 150),
        ("ps1 o'ram: faqat ASCII (Windows PowerShell 5.1 BOM siz faylni ANSI deb o'qiydi)",
         all(ord(ch) < 128 for ch in text)),
    ]


def case_ps1_parametrlari_install_pyga_uzatiladi():
    """Har ps1 parametri install.py bayrog'iga uzatiladi (-Update bundan mustasno:
    u eski nom), uzatiladigan har bayroqni install.py taniydi."""
    text = ps1_text()
    block = re.search(r"\bparam\((.*?)\n\)", re.sub(r"<#.*?#>", "", text, flags=re.S), re.S)
    names = re.findall(r"\[(?:string|switch)\]\$(\w+)", block.group(1) if block else "")
    flags = {n: "--" + re.sub(r"(?<!^)(?=[A-Z])", "-", n).lower() for n in names}
    known = set(I.parser_yasa()._option_string_actions)
    used = set(re.findall(r"'(--[a-z0-9-]+)'", "\n".join(ps1_code())))
    missing = [n for n, f in flags.items() if n != "Update" and f not in used]
    unknown = sorted(used - known)
    return [
        ("ps1 parametrlari topildi: %s" % names, len(names) == 9 and "Update" in names),
        ("ps1 -> install.py: har parametr uzatiladi (yo'q: %s)" % missing, not missing),
        ("ps1 -> install.py: -Update uzatilmaydi (eski nom, hech narsa o'zgartirmaydi)",
         "'--update'" not in text),
        ("ps1 -> install.py: uzatiladigan bayroqlarni install.py taniydi (noma'lum: %s)" % unknown,
         not unknown and {"--bash", "--ps1", "--genius-path"} <= used),
        ("ps1 -> install.py: -ConfirmReset faqat -Reset bilan uzatiladi",
         "if ($Reset -and $ConfirmReset)" in text),
    ]


def case_paritet_hook_jadvali():
    """install.py hook jadvali ikkala platforma shaklida repodagi
    .claude/settings.json ga teng (tools/test_rewrite_paths.py ham shuni qo'riqlaydi)
    va buyruq shakli `"python" "<snapshot>/tools/x.py" [arg] || exit 1`."""
    snap = "/uy/.claude/genius/0123456789ab"
    rows = []
    for label, py in (("posix", sys.executable), ("windows", WIN_PY)):
        settings = I.sozlama_yasa(py, snap, [], ROOT, py.replace("\\", "/"))
        got, shape_ok = [], True
        for event, groups in settings["hooks"].items():
            for group in groups:
                for hook in group["hooks"]:
                    m = T.SETTINGS_CMD.search(hook["command"])
                    script, arg = (m.group(1), m.group(2).strip()) if m else (hook["command"], "")
                    got.append((event, group.get("matcher", ""), script, arg,
                                hook.get("timeout"), hook.get("statusMessage", "")))
                    shape_ok = shape_ok and re.match(
                        r'^"%s" "%s/tools/%s"( [^|]+)? \|\| exit 1$' % (
                            re.escape(py), re.escape(snap), re.escape(script)),
                        hook["command"]) is not None
        got.sort()
        want = T.settings_hooks()
        if len(got) < 5 or len(want) < 5:
            raise AssertionError("hook kam o'qildi: install %d, settings.json %d"
                                 % (len(got), len(want)))
        rows += [
            ("paritet (%s): hook jadvali repo settings.json bilan bir xil (faqat install: %s; "
             "faqat repo: %s)" % (label, [h for h in got if h not in want],
                                  [h for h in want if h not in got]), got == want),
            ("paritet (%s): buyruq shakli" % label, shape_ok),
            ("paritet (%s): env, papkalar, schema" % label,
             settings["env"] == {"GENIUS_PYTHON": py.replace("\\", "/"), "GENIUS_CLONE": ROOT}
             and settings["permissions"]["additionalDirectories"]
             == [snap + "/docs", ROOT + "/memory"]
             and "schemastore" in settings["$schema"]),
        ]
    return rows


def case_paritet_snapshot_joyi():
    """Snapshot joyi va git mantig'i bitta: install.py ham, ps1 o'rami ham
    install/snapshot.py dan oladi (ps1 unga umuman tegmaydi, git ni o'zi chaqirmaydi).
    CLI `yol` install.py yozgan manifestdagi root bilan bir xil joyni beradi."""
    if not POSIX:
        return SKIP
    st = stsenariy()
    code, out = I.run_py([os.path.join(ROOT, "install", "snapshot.py"), "yol",
                          "--clone", st["klon"], "--claude-dir", st["claude"]])
    info = json.loads(out) if code == 0 else {}
    snap_py = get(os.path.join(ROOT, "install", "snapshot.py"))
    inst = get(INSTALL_PY)
    return [
        ("paritet: snapshot.py yol == manifestdagi root",
         info.get("path") == st["manifest"]["root"] == st["snap"]
         and info.get("sha") == st["manifest"]["commit"]),
        ("paritet: joy `<claude>/genius/<sha12>`",
         st["snap"] == os.path.join(st["claude"], "genius", st["head"][:12])),
        ("paritet: install.py snapshot.py ning yarat, arxiv, royxat, olib_tashla, farq_matn, "
         "sha_ol amallarini chaqiradi",
         all(("snapshot.%s(" % fn) in inst for fn in (
             "yarat", "arxiv", "royxat", "olib_tashla", "farq_matn", "sha_ol"))),
        ("paritet: `-c core.autocrlf=false` snapshot.py da, ps1 da git yo'q",
         "core.autocrlf=false" in snap_py and "worktree" not in "\n".join(ps1_code())
         and "'git'" not in "\n".join(ps1_code())),
    ]


def case_paritet_ruxsat_royxati():
    """Ruxsat ro'yxatini install.py rewrite_paths.py --allow dan oladi: uning ro'yxati
    shu asbobning ko'chirilgan skill va aktyorlardagi chiqishiga teng, qo'lda
    yig'ilmagan (ikkala platforma shaklida)."""
    if not POSIX:
        return SKIP
    rows = []
    for label, nt in (("posix", False), ("windows", True)):
        st = stsenariy(nt=nt)
        code, out = st["allow_cli"]
        want = json.loads(out)
        allow = st["after_apply"]["permissions"]["allow"]
        own = [r for r in allow if r != "Bash(git status:*)"]
        rows += [
            ("paritet (%s): --allow chiqishi o'qildi" % label, code == 0 and len(want) >= 5),
            ("paritet (%s): install.py ruxsati rewrite_paths --allow ga teng" % label,
             sorted(own) == sorted(want)),
            ("paritet (%s): run_tests global ruxsatda yo'q" % label,
             not any("run_tests.py" in r for r in allow)),
            ("paritet (%s): opt-in bo'lagi (run_tests) --opt-in chiqishi bilan bir xil va "
             "oxirida ko'rsatildi" % label,
             st["opt_in_cli"][0] == 0 and "run_tests.py" in st["opt_in_cli"][1]
             and st["opt_in_cli"][1] in st["apply"].stdout),
        ]
    return rows


def case_paritet_doimiylar():
    """Doimiylar: aktyorlar skill va .claude/agents bilan, eski nom hozirgi emas,
    klon fayllari mavjud, xavfsiz belgilar rewrite_paths bilan bir xil (XV-P2)."""
    agents = {name[:-3] for name in os.listdir(os.path.join(ROOT, ".claude", "agents"))}
    return [
        ("doimiylar: aktyorlar .claude/agents da bor (%d)" % len(I.ACTORS),
         set(I.ACTORS) <= agents and len(I.ACTORS) == 6),
        ("doimiylar: eski aktyor hozirgi ro'yxatda va fayllarda yo'q",
         not set(I.RETIRED) & (set(I.ACTORS) | agents)),
        ("doimiylar: klon fayllari (%d) mavjud va `/` ajratgichli" % len(I.REQUIRED),
         all(os.path.exists(os.path.join(ROOT, rel)) for rel in I.REQUIRED)
         and not any("\\" in rel for rel in I.REQUIRED)),
        ("doimiylar: xavfsiz belgilar rewrite_paths bilan bir xil",
         sorted(I.UNSAFE_CHARS) == sorted(T.R.UNSAFE_CHARS) and len(I.UNSAFE_CHARS) == 3),
    ]


def case_run_all_tests_topadi():
    """Yangi suite ro'yxatga qo'lda qo'shilmaydi: glob topadi."""
    import glob
    found = [os.path.basename(p) for p in glob.glob(os.path.join(HERE, "test_*.py"))]
    src = get(os.path.join(HERE, "run_all_tests.py"))
    return "test_install.py" in found and 'glob.glob(os.path.join(HERE, "test_*.py"))' in src


CASES = [
    ("install.py: Python 3.8 sintaksisi, em-dash yo'q", case_py38_sintaksis),
    ("quruq yurish hech narsa yozmaydi", case_quruq_yurish_hech_narsa_yozmaydi),
    ("--apply o'rnatadi", case_apply_ornatadi),
    ("--update begonani saqlaydi", case_update_begonani_saqlaydi),
    ("--uninstall faqat o'zini oladi", case_uninstall_faqat_ozini_oladi),
    ("--uninstall klon yo'q bo'lsa ham ishlaydi", case_uninstall_klon_yoq),
    ("--uninstall snapshotni olib tashlaydi, begonasiga tegmaydi",
     case_uninstall_snapshotni_va_faqat_genius_ostidagini),
    ("--uninstall klon o'chgan: yetim snapshot", case_uninstall_klon_ochgan_yetim_snapshot),
    ("eski (snapshotsiz) o'rnatishdan o'tish", case_eski_ornatishdan_otish),
    ("git bo'lmagan klon rad etiladi", case_git_bolmagan_klon_rad),
    ("~/.claude/genius klon ichiga symlink rad etiladi", case_genius_klon_ichiga_symlink_rad),
    ("xavfli yo'l o'rnatishni to'xtatadi (XV-P2)", case_xavfli_yol_toxtatadi),
    ("rad etiladigan birikmalar", case_rad_etiladigan_birikmalar),
    ("--reset faqat tasdiq bilan", case_reset_tasdiq_bilan),
    ("symlink: zaxirada havola, nishon joyida", case_symlink_zaxirasi),
    ("klon ichiga symlink rad etiladi", case_klon_ichiga_symlink_rad),
    ("--backup-to o'chiriladigan birlik ichida rad", case_backup_ornatiladigan_ichida_rad),
    ("--uninstall manifest bo'yicha", case_uninstall_manifest_boyicha),
    ("HOME bo'sh yoki / rad etiladi", case_uy_papka_rad),
    ("--reset --include-auth --project --apply", case_reset_include_auth_va_project_apply),
    ("paritet: hook jadvali repo settings.json ga teng (ikki platforma)", case_paritet_hook_jadvali),
    ("paritet: snapshot joyi va git mantig'i bitta", case_paritet_snapshot_joyi),
    ("paritet: ruxsat ro'yxati (ikki platforma)", case_paritet_ruxsat_royxati),
    ("paritet: doimiylar", case_paritet_doimiylar),
    ("paritet: install.py chiqishi ikki platformada bir xil", case_paritet_ikki_platforma),
    ("windows: ps1 ilgari bergan natijaga teng (oltin qiymat)", case_windows_oltin_qiymat),
    ("windows: Platforma funksiyalari", case_windows_platforma_funksiyalari),
    ("windows: PATH dagi bash, WSL rad", case_windows_bash_izlash),
    ("windows: --ps1 xabarlarda PowerShell bayroqlari", case_windows_ps1_xabar_bayroqlari),
    ("windows: rad etiladigan birikmalar", case_windows_rad_etiladigan_birikmalar),
    ("windows: quruq yurish", case_windows_quruq_yurish),
    ("windows: --apply o'rnatadi", case_windows_apply_ornatadi),
    ("windows: --update va --uninstall", case_windows_update_va_uninstall),
    ("windows: yo'l almashtirish chaqiruvlari ps1 bilan bir xil", case_windows_rewrite_chaqiruvlari),
    ("ps1: yupqa o'ram", case_ps1_yupqa_oram),
    ("ps1: parametrlar install.py ga uzatiladi", case_ps1_parametrlari_install_pyga_uzatiladi),
    ("run_all_tests yangi suiteni topadi", case_run_all_tests_topadi),
]


if __name__ == "__main__":
    sys.exit(testkit.run_cases(CASES, sys.argv[1:]))
