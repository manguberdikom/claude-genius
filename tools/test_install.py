#!/usr/bin/env python3
"""install/install.py uchun sinovlar (Linux va macOS o'rnatuvchisi).

    python3 tools/test_install.py
    python3 tools/test_install.py -k paritet

Haqiqiy ~/.claude ga tegilmaydi: har holat vaqtinchalik HOME (`HOME` env,
tmp papka) bilan yuradi. Quruq yurish, --apply, --update, --uninstall bitta
ketma-ketlikda (`stsenariy`) bir marta yuradi va holatlar uning natijasini
tekshiradi: har --apply indeksni qayta yasaydi va asboblarni chaqiradi.

Paritet: manguberdi.ps1 sinalmaydi, shuning uchun uning matni
tools/test_rewrite_paths.py dagi usul bilan o'qiladi (hook jadvali,
aktyorlar, eski aktyorlar, klon fayllari, manifest kalitlari) va install.py
bilan solishtiriladi. Windows da install.py ishlamaydi (u yerda ps1), shuning
uchun ish yuradigan holatlar o'tkazib yuboriladi, matnga oid paritet esa
yuradi.
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
import test_rewrite_paths as T  # noqa: E402  (ps1 matnini o'qish usuli)

INSTALL_PY = os.path.join(ROOT, "install", "install.py")
spec = importlib.util.spec_from_file_location("install_py", INSTALL_PY)
I = importlib.util.module_from_spec(spec)
spec.loader.exec_module(I)

POSIX = os.name != "nt"
SKIP = [("o'tkazildi: Windows da install.py yo'q (ps1 ishlaydi)", True)]

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


def run_install(home, *args):
    """install.main() ni vaqtinchalik HOME bilan yurgizadi: Result(rc, out, err)."""
    return testkit.call_main(
        I.main, argv=["install.py"] + list(args),
        env={"HOME": home, "CLAUDE_CONFIG_DIR": None})


def hooks_of(settings):
    return [h for groups in settings.get("hooks", {}).values()
            for g in groups for h in g.get("hooks", [])]


def commands_of(settings):
    return [h.get("command", "") for h in hooks_of(settings)]


# --- stsenariy: foydalanuvchi sozlamasi, dry, apply, update, uninstall ----

_STATE = {}
_CLONE = []

FOREIGN_SETTINGS = {
    "model": "opus",
    "hooks": {"SessionStart": [{"hooks": [
        {"type": "command", "command": "echo begona-hook"}]}]},
    "permissions": {"allow": ["Bash(git status:*)"]},
}


def stsenariy():
    if _STATE:
        return _STATE
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

    st = _STATE
    st["home"], st["claude"] = home, claude
    index = os.path.join(ROOT, "index")

    st["stages_before"] = temp_stages()
    before = snapshot(home), snapshot(index), temp_stages()
    st["dry"] = run_install(home)
    st["dry_same"] = before == (snapshot(home), snapshot(index), temp_stages())

    st["apply"] = run_install(home, "--apply", "--backup-to",
                              os.path.join(home, "zaxira-1"))
    path = os.path.join(claude, "settings.json")
    st["stages_after"] = temp_stages()
    st["after_apply_raw"] = open(path, "rb").read()
    st["after_apply"] = jget(path)
    st["apply_agents"] = sorted(os.listdir(os.path.join(claude, "agents")))
    st["fs_apply"] = set(snapshot(claude))
    st["claude_md"] = get(os.path.join(claude, "CLAUDE.md"))
    st["manifest"] = jget(os.path.join(claude, "skills", "manguberdi", ".genius.json"))
    st["opt_in_cli"] = I.run_py(
        [os.path.join(ROOT, "install", "rewrite_paths.py"), claude, "--root", ROOT,
         "--python", sys.executable, "--bash", "bash", "--opt-in"])
    # ps1 ham, install.py ham ruxsatni shu asbobdan oladi: shu holatdagi chiqishi.
    st["allow_cli"] = I.run_py(
        [os.path.join(ROOT, "install", "rewrite_paths.py"), claude, "--root", ROOT,
         "--python", sys.executable, "--bash", "bash", "--allow"])

    # Yangilash: begona skill, begona hook (o'z hooklari bilan bir guruhda),
    # begona ruxsat va ikkinchi marta o'rnatish.
    put(os.path.join(claude, "skills", "begona", "SKILL.md"), "begona")
    data = jget(path)
    data["hooks"]["UserPromptSubmit"][0]["hooks"].append(
        {"type": "command", "command": "echo begona-hook-2"})
    data["permissions"]["allow"].append("Bash(ls:*)")
    put(path, json.dumps(data))
    st["update"] = run_install(home, "--update", "--apply", "--backup-to",
                               os.path.join(home, "zaxira-2"))
    st["after_update"] = jget(path)
    st["update_agents"] = sorted(os.listdir(os.path.join(claude, "agents")))
    st["fs_update"] = set(snapshot(claude))

    before = snapshot(home)
    st["uninstall_dry"] = run_install(home, "--uninstall")
    st["uninstall_dry_same"] = before == snapshot(home)
    st["uninstall"] = run_install(home, "--uninstall", "--apply", "--backup-to",
                                  os.path.join(home, "zaxira-3"))
    st["fs_uninstall"] = set(snapshot(claude))
    st["after_uninstall"] = jget(path)
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
        ("quruq: uy, indeks va vaqtinchalik papka o'zgarmadi", st["dry_same"]),
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
        ("apply: manifest", manifest["root"] == ROOT and manifest["actors"] == list(I.ACTORS)
         and manifest["python"] == sys.executable and "commit" in manifest),
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
    root = ROOT.lower()
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
        dst = os.path.join(tmpdir("klon_"), "klon")
        shutil.copytree(ROOT, dst, symlinks=True, ignore=shutil.ignore_patterns(
            ".git", "index", "dist", "worktrees", "__pycache__", ".state", "usage"))
        _CLONE.append(dst)
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


# --- paritet: manguberdi.ps1 bilan --------------------------------------

def ps1_text():
    return T.ps1_text()


def ps1_list(name):
    """`$Name = @( 'a', 'b' )` ro'yxati (ko'p qatorli ham)."""
    m = re.search(r"\$%s = @\((.*?)\)\s*\n" % name, ps1_text(), re.S)
    if not m:
        raise AssertionError("ps1 da $%s topilmadi" % name)
    return re.findall(r"'([^']+)'", m.group(1))


def case_paritet_hook_jadvali():
    """install.py yozgan hook jadvali ps1 yasaydiganiga teng (hodisa, matcher,
    skript, argument, timeout, statusMessage) va buyruq shakli bir xil."""
    if not POSIX:
        return SKIP
    settings = I.sozlama_yasa(sys.executable, ROOT, [])
    got = []
    shape_ok = True
    for event, groups in settings["hooks"].items():
        for group in groups:
            for hook in group["hooks"]:
                m = T.SETTINGS_CMD.search(hook["command"])
                script, arg = (m.group(1), m.group(2).strip()) if m else (hook["command"], "")
                got.append((event, group.get("matcher", ""), script, arg,
                            hook.get("timeout"), hook.get("statusMessage", "")))
                shape_ok = shape_ok and re.match(
                    r'^"%s" "%s/tools/%s"( [^|]+)? \|\| exit 1$' % (
                        re.escape(sys.executable), re.escape(ROOT), re.escape(script)),
                    hook["command"]) is not None
    got.sort()
    want = T.ps1_hooks()
    if len(got) < 5 or len(want) < 5:
        raise AssertionError("hook kam o'qildi: install %d, ps1 %d" % (len(got), len(want)))
    return [
        ("paritet: hook jadvali ps1 bilan bir xil (faqat install: %s; faqat ps1: %s)"
         % ([h for h in got if h not in want], [h for h in want if h not in got]),
         got == want),
        ("paritet: buyruq shakli `\"python\" \"<klon>/tools/x.py\" [arg] || exit 1`", shape_ok),
        ("paritet: env, papkalar, schema (ps1 matnida ham shunday)",
         settings["env"] == {"GENIUS_PYTHON": sys.executable}
         and settings["permissions"]["additionalDirectories"]
         == [ROOT + "/docs", ROOT + "/memory"]
         and "schemastore" in settings["$schema"]
         and '"$g/docs", "$g/memory"' in ps1_text()
         and "GENIUS_PYTHON = $pyArg" in ps1_text()),
    ]


def case_paritet_ruxsat_royxati():
    """Ruxsat ro'yxatini ikkala o'rnatuvchi ham rewrite_paths.py --allow dan
    oladi: install.py ning ro'yxati shu asbobning ko'chirilgan skill va
    aktyorlardagi chiqishiga teng, qo'lda yig'ilmagan."""
    if not POSIX:
        return SKIP
    st = stsenariy()
    code, out = st["allow_cli"]
    want = json.loads(out)
    allow = st["after_apply"]["permissions"]["allow"]
    own = [r for r in allow if r != "Bash(git status:*)"]
    text = ps1_text()
    return [
        ("paritet: --allow chiqishi o'qildi", code == 0 and len(want) >= 5),
        ("paritet: install.py ruxsati rewrite_paths --allow ga teng", sorted(own) == sorted(want)),
        ("paritet: run_tests global ruxsatda yo'q",
         not any("run_tests.py" in r for r in allow)),
        ("paritet: opt-in bo'lagi (run_tests) --opt-in chiqishi bilan bir xil va oxirida ko'rsatildi",
         st["opt_in_cli"][0] == 0 and "run_tests.py" in st["opt_in_cli"][1]
         and st["opt_in_cli"][1] in st["apply"].stdout),
        ("paritet: ps1 ham ruxsat va opt-in ni shu asbobdan oladi",
         "'--allow'" in text and "'--opt-in'" in text),
    ]


def case_paritet_ps1_doimiylari():
    ps1 = {
        "aktyorlar": ps1_list("Actors"),
        "eski aktyorlar": ps1_list("Retired"),
        "tozalash birliklari": ps1_list("ConfigItems"),
        "klon fayllari": [r.replace("\\", "/") for r in ps1_list("Required")],
    }
    mine = {
        "aktyorlar": list(I.ACTORS),
        "eski aktyorlar": list(I.RETIRED),
        "tozalash birliklari": list(I.CONFIG_ITEMS),
        "klon fayllari": list(I.REQUIRED),
    }
    rows = [("paritet: %s ps1 bilan bir xil (%d)" % (key, len(ps1[key])),
             ps1[key] == mine[key] and len(ps1[key]) > 0) for key in ps1]
    keys = re.search(r"\$manifest = \[ordered\]@\{(.*?)\n  \}", ps1_text(), re.S)
    ps1_keys = re.findall(r"^\s*(\w+)\s*=", keys.group(1), re.M) if keys else []
    if POSIX:
        st = stsenariy()
        manifest = st["manifest"]
        rows.append(("paritet: manifest kalitlari ps1 bilan bir xil %s" % ps1_keys,
                     bool(ps1_keys) and sorted(manifest) == sorted(ps1_keys)))
    return rows


def case_paritet_ps1_xavfsiz_belgilar():
    """ps1 va install.py bir xil belgilarni rad etadi (R7.8 XV-P2)."""
    text = ps1_text()
    m = re.search(r"\$UnsafeChars = \[char\[\]\]@\((.*?)\)", text)
    ps1_chars = re.findall(r"'([^']+)'", m.group(1)) if m else []
    return sorted(ps1_chars) == sorted(I.UNSAFE_CHARS) and len(ps1_chars) == 3


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
    ("xavfli yo'l o'rnatishni to'xtatadi (XV-P2)", case_xavfli_yol_toxtatadi),
    ("rad etiladigan birikmalar", case_rad_etiladigan_birikmalar),
    ("--reset faqat tasdiq bilan", case_reset_tasdiq_bilan),
    ("symlink: zaxirada havola, nishon joyida", case_symlink_zaxirasi),
    ("klon ichiga symlink rad etiladi", case_klon_ichiga_symlink_rad),
    ("--backup-to o'chiriladigan birlik ichida rad", case_backup_ornatiladigan_ichida_rad),
    ("--uninstall manifest bo'yicha", case_uninstall_manifest_boyicha),
    ("HOME bo'sh yoki / rad etiladi", case_uy_papka_rad),
    ("--reset --include-auth --project --apply", case_reset_include_auth_va_project_apply),
    ("paritet: hook jadvali ps1 ga teng", case_paritet_hook_jadvali),
    ("paritet: ruxsat ro'yxati", case_paritet_ruxsat_royxati),
    ("paritet: ps1 doimiylari", case_paritet_ps1_doimiylari),
    ("paritet: xavfsiz belgilar", case_paritet_ps1_xavfsiz_belgilar),
    ("run_all_tests yangi suiteni topadi", case_run_all_tests_topadi),
]


if __name__ == "__main__":
    sys.exit(testkit.run_cases(CASES, sys.argv[1:]))
