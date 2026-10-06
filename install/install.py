#!/usr/bin/env python3
"""manguberdi skillini Linux va macOS da o'rnatadi (POSIX, faqat stdlib, Python 3.8+).

    python3 install/install.py                      # quruq yurish: ro'yxat, hech narsa yozilmaydi
    python3 install/install.py --apply              # o'rnatadi (qo'shuvchi)
    python3 install/install.py --update --apply     # xuddi shu: qayta o'rnatadi, begonasi qoladi
    python3 install/install.py --uninstall --apply  # faqat o'zi qo'shganini olib tashlaydi
    python3 install/install.py --reset --apply --confirm-reset   # to'liq tozalash

Windows da `install/manguberdi.ps1` ishlatiladi: bu skript `nt` da to'xtaydi.
Mantiq ps1 bilan bir xil: sukut QO'SHUVCHI, faqat `skills/manguberdi`, olti
aktyor fayli va settings.json dagi shu klonga ishora qilgan hook va
ruxsatlar almashadi. Boshqa skill, agent, CLAUDE.md, commands/, plugins/,
hooks/, rules/, output-styles/ va settings.json dagi begona yozuvlar
joyida qoladi. `--update` eski nom: sukut xulq bilan bir xil, buyruqlar
va hujjatlar buzilmasin deb qabul qilinadi.

Quruq yurish ham Python yordamchilarini haqiqatan chaqiradi va skillni
vaqtinchalik papkada yig'ib sinaydi, keyin o'chiradi: nosozlik hech narsa
o'chmasidan oldin chiqadi. Faqat shu vaqtinchalik papkaga yoziladi,
`~/.claude`, klon va indeksga tegilmaydi.

Hooklar klonning ishchi daraxtidan EMAS, aniq commit dagi snapshotdan
yuradi: `git worktree add --detach ~/.claude/genius/<sha12>` (R7.8, XV-Y1).
Aks holda `git pull` dan keyingi birinchi promptdayoq tekshirilmagan kod
bajarilardi. Skill, hook buyruqlari, ruxsat qoidalari va `<snapshot>/docs`
snapshotga ishora qiladi; memory va holat (`.claude/.state`) klonda qoladi:
settings.json `env.GENIUS_CLONE` ni yozadi. Yangi commit snapshotga faqat
`tools/yangilash.py` (ro'yxatni ko'rsatadi, tasdiq so'raydi) yoki shu
skriptni qayta yurgizish bilan o'tadi. Snapshot HEAD commitdan olinadi:
klondagi commit qilinmagan o'zgarish unga kirmaydi.

Yordamchilar qayta ishlatiladi, takrorlanmaydi: `rewrite_paths.py` (yo'l
almashtirish, ruxsat ro'yxati, opt-in bo'lagi), `merge_settings.py`
(settings.json ni birlashtirish), `uninstall_settings.py` (olib tashlash),
`snapshot.py` (snapshot joyi, yaratish, tozalash: ps1 ham shuni chaqiradi).
`restore_backup.py` o'rnatishda chaqirilmaydi: u zaxirani qaytaradi
(install/README.md, "Orqaga qaytarish").

manguberdi.ps1 qadamlari va ularning shu yerdagi o'rni:

    ps1 qadami                                  install.py
    ------------------------------------------  ---------------------------------
    -Reset/-Project/-IncludeAuth/-ConfirmReset  tekshir_argumentlar (--reset, ...)
    CLAUDE_CONFIG_DIR rad etish                 tekshir_argumentlar
    Test-SafePath ($, backtick, ")              xavfsiz_yol (R7.8 XV-P2)
    $Required fayllari                          REQUIRED, klon_tekshir
    -Project himoyasi (klon, uy papkasi)        project_tekshir
    zaxira papkasi bo'sh emas                   zaxira_tekshir
    Find-Python (py -3, Store stub'i)           POSIX da kerak emas: sys.executable
    Invoke-Native (stderr, BOM, kodirovka)      POSIX da kerak emas: subprocess,
                                                UTF-8 BOM siz
    Set-ExecutionPolicy                         POSIX da kerak emas
    Git Bash izlash (System32/WSL)              POSIX da PATH dagi bash yetadi
    managed-settings.json ogohlantirishi        managed_ogohlantirish (POSIX yo'llari)
    CRLF li doc.sh rad etish                    klon_tekshir
    user MCP serverlar ro'yxati                 user_mcp
    0. sinov yig'imi, --tekshir, --allow,       sinov_yigimi
       --opt-in
    hook jadvali, settings.json                 sozlama_yasa, HOOKS
    -Update: merge_settings (quruq)             ornatish
    1. zaxira                                   zaxira_ol
    snapshot (worktree) va indeks               ornatish, snapshot.yarat
    2. almashtirish yoki tozalash               ornatish
    3. skill, aktyorlar, .genius.json           ornatish, manifest_yoz
    4. sozlama (--yoz yoki toza yozuv)          ornatish
    5. tekshirish                               tekshirish
    -Uninstall                                  olib_tashlash
    Get-StaleActors                             eski_aktyorlar

Chiqish kodi: 0 muvaffaqiyat, 1 xato (hech narsa o'chmaganini matn aytadi).
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CLONE = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import snapshot  # noqa: E402  (snapshot joyi va git mantig'i: ps1 bilan bitta)

# O'rnatiladigan aktyorlar. Skill shu nomlar bilan chaqiradi.
ACTORS = ("qidiruv", "tahlil", "review", "dasturchi", "test-muhandis",
          "rejalashtiruvchi")

# Olib tashlangan yoki qayta nomlangan aktyorlar: yangilash va --uninstall
# ularni zaxira bilan oladi (dab9314: arxitektor dasturchi bo'ldi).
RETIRED = ("arxitektor",)

# --reset o'chiradigan sozlama birliklari. Tarix, todo va kirish bu yerda
# yo'q: ular sozlama emas.
CONFIG_ITEMS = ("settings.json", "settings.local.json", "CLAUDE.md",
                "skills", "agents", "commands", "plugins", "hooks", "rules",
                "output-styles")

# Klon to'liqligi (ps1 dagi $Required bilan bir xil, `/` ajratgich bilan).
# install/merge_settings.py (--reset siz) va install/uninstall_settings.py
# ni kod o'zi qo'shadi, xuddi ps1 kabi.
REQUIRED = (
    "tools/doc.sh", "tools/guard.py", "tools/check_code.py", "tools/rules_for.py",
    "tools/budget.py", "tools/suggest_sections.py", "tools/usage.py", "tools/actor_check.py",
    "tools/handoff.py", "tools/state.py", "tools/docref.py", "tools/hookio.py", "tools/geniuslib.py",
    "tools/build_index.py", "tools/check_docs.py",
    "tools/review_status.py", "tools/sonar_snapshot.py",
    "tools/run_tests.py", "tools/parse_test_output.py", "tools/guruh.py",
    "install/rewrite_paths.py", "install/snapshot.py",
    "docs/manifest.json", ".claude/skills/manguberdi/SKILL.md",
)

UNSAFE_CHARS = ("$", "`", '"')

SCHEMA = "https://json.schemastore.org/claude-code-settings.json"

# Hook jadvali: (hodisa, matcher, [(skript, argument, timeout, statusMessage)]).
# Repodagi .claude/settings.json va manguberdi.ps1 bilan bir xil bo'lishi
# shart: tools/test_install.py (hook jadvali ps1 ga mos) nomuvofiqlikda CI
# ni yiqitadi. Har buyruq oxirida `|| exit 1` (sababi manguberdi.ps1 dagi
# izohda: o'chgan klon hookdan 2 qaytarib Claude Code ni hamma proyektda
# to'sib qo'ymasligi uchun). `||` argumentdan keyin turadi, shuning uchun
# handoff va usage argumenti buyruqqa shu yerda biriktiriladi.
HOOKS = (
    ("UserPromptSubmit", "", (
        ("suggest_sections.py", "", 10, "Mos bo'limlar qidirilmoqda"),
        ("budget.py", "", 10, ""),
        ("handoff.py", "--hook", 10, "Kontekst o'lchanmoqda"))),
    ("PreToolUse", "Read|Bash|PowerShell", (
        ("guard.py", "", 10, "Qimmat amal tekshirilmoqda"),)),
    ("PreToolUse", "Task|Agent|SendMessage", (
        ("budget.py", "", 10, "Aktyor budjeti tekshirilmoqda"),)),
    ("SubagentStop", "", (
        ("actor_check.py", "", 10, "Aktyor natijasi tekshirilmoqda"),)),
    ("PostToolUse", "Write|Edit", (
        ("check_code.py", "", 15, "Java qoidalari tekshirilmoqda"),)),
    ("Stop", "", (
        ("usage.py", "--saqlash", 20, "Token sarfi yozilmoqda"),)),
)


class Xato(Exception):
    """O'rnatish to'xtaydi: sabab matnda."""


def say(text=""):
    print(text)


def step(text):
    print("  " + text)


def run_py(args, input_text=None, env=None):
    """Python yordamchisini chaqiradi: (kod, chiqish). stderr stdout ga qo'shiladi."""
    merged = dict(os.environ)
    merged["PYTHONIOENCODING"] = "utf-8"
    merged.update(env or {})
    try:
        proc = subprocess.run([sys.executable] + list(args), input=input_text,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              env=merged, encoding="utf-8", errors="replace")
    except OSError as exc:
        return 1, str(exc)
    return proc.returncode, proc.stdout.strip()


def xavfsiz_yol(what, value):
    """Hook buyrug'i bash da qo'sh qo'shtirnoq ichida yuradi: `$`, backtick
    kengayadi, `"` qo'shtirnoqni yopadi (R7.8 XV-P2)."""
    for char in UNSAFE_CHARS:
        if char in value:
            raise Xato("%s yo'lida $, backtick yoki qo'sh qo'shtirnoq bor: %s. "
                       "Hook buyrug'i bash da qo'sh qo'shtirnoq ichida yuradi va "
                       "bu belgi u yerda kengayadi yoki bajariladi. Boshqa papka "
                       "tanlang." % (what, value))


def tekshir_argumentlar(opts):
    # --project va --include-auth to'liq tozalashning qismi.
    if not opts.reset and (opts.project or opts.include_auth):
        raise Xato("--project va --include-auth faqat --reset bilan beriladi: ular "
                   "to'liq tozalashning qismi. Sukut rejim esa faqat manguberdi "
                   "birliklarini almashtiradi va boshqa hech narsaga tegmaydi.")
    # Interaktiv so'rov emas: CI va agent sessiyasi interaktiv emas.
    if opts.reset and opts.apply and not opts.confirm_reset:
        raise Xato("--reset --apply ~/.claude dagi settings.json, settings.local.json, "
                   "CLAUDE.md, skills/, agents/, commands/, plugins/, hooks/, rules/ "
                   "va output-styles/ ni o'chiradi (zaxira bilan). Rozi bo'lsangiz "
                   "--confirm-reset ham qo'shing. Faqat manguberdi kerak bo'lsa "
                   "--reset bermang: sukut rejim qo'shuvchi.")
    if opts.uninstall and (opts.project or opts.include_auth or opts.reset):
        raise Xato("--uninstall bilan --reset, --project yoki --include-auth berilmaydi.")
    # ps1 da -Reset -Update jim o'tadi (reset ustun). Bu yerda ikki ma'noli
    # buyruq rad etiladi: --update qo'shuvchi, --reset esa hammasini tozalaydi.
    if opts.update and (opts.reset or opts.uninstall):
        raise Xato("--update bilan --reset yoki --uninstall berilmaydi: "
                   "--update qo'shuvchi qayta o'rnatish.")
    if opts.confirm_reset and not opts.reset:
        raise Xato("--confirm-reset faqat --reset bilan beriladi.")
    if os.environ.get("CLAUDE_CONFIG_DIR"):
        raise Xato("CLAUDE_CONFIG_DIR o'rnatilgan (%s): Claude Code sozlamani o'sha "
                   "yerdan o'qiydi, skript esa ~/.claude ni o'zgartiradi. O'zgaruvchini "
                   "olib tashlab qayta yurgizing." % os.environ["CLAUDE_CONFIG_DIR"])


def klon_tekshir(root, reset, nom="klon"):
    for rel in REQUIRED + (() if reset else ("install/merge_settings.py",)) \
            + ("install/uninstall_settings.py",):
        if not os.path.exists(os.path.join(root, rel)):
            raise Xato("%s to'liq emas, yo'q: %s" % (nom, rel))
    # Git for Windows dan ko'chirilgan klonda doc.sh CRLF bilan bo'lishi
    # mumkin: bash uni birinchi qatordayoq to'xtatadi va qidiruv jim qoladi.
    with open(os.path.join(root, "tools", "doc.sh"), "rb") as handle:
        if b"\r\n" in handle.read():
            raise Xato("tools/doc.sh CRLF bilan olingan, bash uni yurgizmaydi. Yechim: "
                       "git -C '%s' -c core.autocrlf=false checkout -- tools/doc.sh "
                       "(avval faylni o'chiring). Hech narsa o'chmadi." % root)


def project_tekshir(project, claude_dir, root):
    """--project ning .claude/ papkasi o'chiriladi: uy papkasi va klon rad etiladi."""
    if not os.path.isdir(project):
        raise Xato("Project topilmadi: %s" % project)
    project = os.path.abspath(project).rstrip("/") or "/"
    proj_claude = os.path.join(project, ".claude")
    for guarded in (claude_dir, os.path.join(root, ".claude")):
        if os.path.normcase(os.path.realpath(guarded)) == \
                os.path.normcase(os.path.realpath(proj_claude)):
            raise Xato("--project klon yoki uy papkasi bo'la olmaydi: %s" % project)
    return project, proj_claude


def zaxira_tekshir(path):
    """Zaxira hech qachon avvalgisi ustidan yozilmaydi."""
    if os.path.exists(path) and (not os.path.isdir(path) or os.listdir(path)):
        raise Xato("zaxira papkasi bo'sh emas: %s. Avvalgi zaxira ustidan yozilmaydi: "
                   "yangi yo'l bering yoki --backup-to ni olib tashlang." % path)


def managed_ogohlantirish():
    """Managed sozlama hammadan ustun: unga tegilmaydi, lekin hooklarni o'chirishi mumkin."""
    for path in ("/etc/claude-code/managed-settings.json",
                 "/Library/Application Support/ClaudeCode/managed-settings.json"):
        if os.path.exists(path):
            say()
            say("DIQQAT: %s topildi. U eng ustun sozlama, skript unga tegmaydi; "
                "disableAllHooks yoki allowManagedHooksOnly bo'lsa hooklar "
                "ishlamaydi." % path)


def user_mcp(auth_file):
    """~/.claude.json dagi user scope MCP serverlar nomi (faqat o'qiladi)."""
    try:
        with open(auth_file, encoding="utf-8-sig") as handle:
            servers = json.load(handle).get("mcpServers")
    except (OSError, ValueError, AttributeError):
        return []
    return sorted(servers) if isinstance(servers, dict) else []


def manifest_aktyorlar(manifest_path):
    """Manifestdagi `actors` (fayl nomiga yaraydigan nomlar) yoki None, agar
    manifest yo'q, o'qilmaydi yoki `actors` ro'yxat emas."""
    try:
        with open(manifest_path, encoding="utf-8-sig") as handle:
            listed = json.load(handle).get("actors")
    except (OSError, ValueError, AttributeError):
        return None
    if not isinstance(listed, list):
        return None
    return [n for n in (str(item) for item in listed) if re.match(r"^[\w-]+\Z", n)]


def eski_aktyorlar(manifest_path):
    """RETIRED va avvalgi manifestdagi, ACTORS da yo'q nomlar.

    Manifestdagi nom fayl yo'liga qo'shiladi, shuning uchun faqat harf, raqam,
    `_` va `-`.
    """
    names = list(RETIRED)
    if os.path.isfile(manifest_path):
        try:
            with open(manifest_path, encoding="utf-8-sig") as handle:
                prev = json.load(handle).get("actors")
            if isinstance(prev, list):
                names += [str(item) for item in prev]
        except (OSError, ValueError, AttributeError):
            step("OGOHLANTIRISH: %s o'qilmadi, faqat RETIRED olinadi" % manifest_path)
    out = []
    for name in names:
        if re.match(r"^[\w-]+\Z", name) and name not in ACTORS and name not in out:
            out.append(name)
    return out


def hook_buyruq(python, tools_dir, script, suffix=""):
    return '"%s" "%s/%s"%s || exit 1' % (python, tools_dir, script,
                                         " " + suffix if suffix else "")


def sozlama_yasa(python, root, allow, clone):
    """Global settings.json. Hook yo'llari MUTLAQ: global o'rnatishda asboblar
    boshqa papkada turadi. `root` pin qilingan snapshot (`~/.claude/genius/
    <sha12>`), `clone` esa klon: hook va docs snapshotdan, memory klondan
    (R7.8 XV-Y1).

    additionalDirectories da butun klon EMAS, faqat `<snapshot>/docs` va
    `<klon>/memory` (XV-Y4): butun daraxt berilsa aktyor hook skriptini
    so'rovsiz tahrirlay olardi. GENIUS_PYTHON: doc.sh indeksni qayta
    yasaganda aynan sinalgan Python ni oladi. GENIUS_CLONE: snapshotdan
    yuradigan asbob memory va holatni klonga yozadi (geniuslib.clone_root).
    """
    hooks = {}
    tools_dir = root + "/tools"
    for event, matcher, items in HOOKS:
        group = {"hooks": []}
        if matcher:
            group = {"matcher": matcher, "hooks": []}
        for script, arg, timeout, status in items:
            hook = {"type": "command",
                    "command": hook_buyruq(python, tools_dir, script, arg),
                    "timeout": timeout}
            if status:
                hook["statusMessage"] = status
            group["hooks"].append(hook)
        hooks.setdefault(event, []).append(group)
    return {
        "$schema": SCHEMA,
        "env": {"GENIUS_PYTHON": python, "GENIUS_CLONE": clone},
        "permissions": {
            "additionalDirectories": [root + "/docs", clone + "/memory"],
            "allow": allow,
        },
        "hooks": hooks,
    }


def json_matn(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def yoz_atomik(path, text):
    """BOM siz UTF-8, shu papkadagi vaqtinchalik fayl va os.replace orqali."""
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    handle, tmp = tempfile.mkstemp(prefix=".tmp-", dir=folder)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as out:
            out.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def olib_tashla(path):
    if os.path.islink(path) or os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)


def nusxa(src, dst):
    """Symlink symlink sifatida zaxiralanadi (singani ham): nishon nusxalanmaydi
    va o'chirishda faqat havola ketadi, nishon joyida qoladi."""
    if os.path.islink(src):
        os.symlink(os.readlink(src), dst)
    elif os.path.isdir(src):
        shutil.copytree(src, dst, symlinks=True)
    else:
        shutil.copy2(src, dst)


def haqiqiy_birlik(path):
    """Birlikning haqiqiy joyi: ota papka symlink bo'lsa ochiladi, birlikning
    o'zi (havola bo'lishi mumkin) ochilmaydi: o'chadigani havolaning o'zi."""
    parent, leaf = os.path.split(os.path.abspath(path))
    return os.path.join(os.path.realpath(parent), leaf)


def ichida(path, folder):
    """`path` papka `folder` ning o'zi yoki ichida (ikkalasi ham haqiqiy yo'l)."""
    path, folder = os.path.normcase(path), os.path.normcase(folder)
    return path == folder or path.startswith(folder.rstrip(os.sep) + os.sep)


def xavfsiz_joylashuv(ctx, removable):
    """Hech narsa o'zgarmasdan oldin (quruq yurishda ham): o'rnatuvchi klonning
    manba fayllarini bosmasligi, zaxira o'chiriladigan birlik ichiga tushmasligi.

    - ~/.claude, skills, agents va skills/manguberdi ning haqiqiy joyi klon
      ichida bo'lsa (symlink), o'rnatish `.claude/agents/*.md` kabi manba
      fayllarini ustidan yozardi yoki o'chirardi;
    - `~/.claude/genius` (snapshotlar) klon ichiga symlink bo'lsa, worktree klon
      ichida yaratilardi;
    - klonning o'zi o'chiriladigan birlik ichida bo'lsa, o'chirish klonni olib ketadi;
    - --backup-to o'chiriladigan birlik ichida bo'lsa, zaxira o'zini nusxalardi
      va o'chirish bilan birga ketardi.
    """
    clone = os.path.realpath(ctx.clone)
    for path in (ctx.claude, os.path.join(ctx.claude, "skills"), ctx.agents_dst,
                 ctx.skill_dst, snapshot.genius_dir(ctx.claude)):
        # To'liq realpath: papkaning o'zi symlink bo'lsa, ichiga yoziladigan va
        # ichidan o'chiriladigan narsa nishondagi fayllar.
        if ichida(os.path.realpath(path), clone):
            raise Xato("%s haqiqiy joyi klon ichida (symlink?): %s. O'rnatuvchi klonning "
                       "manba fayllarini bosardi yoki o'chirardi. Symlinkni olib tashlang "
                       "yoki boshqa papkaga yo'naltiring. Hech narsa o'zgarmadi."
                       % (path, os.path.realpath(path)))
    backup = os.path.realpath(ctx.backup_to)
    for path in removable:
        real = haqiqiy_birlik(path)
        if ichida(clone, real):
            raise Xato("klon o'chiriladigan birlik ichida: %s. Hech narsa o'zgarmadi." % path)
        if ichida(backup, real):
            raise Xato("--backup-to o'chiriladigan birlik ichida: %s (%s). Zaxira o'zini "
                       "nusxalardi va o'chirish bilan ketardi. Boshqa papka bering. Hech "
                       "narsa o'zgarmadi." % (ctx.backup_to, path))


def zaxira_ol(paths, backup_to):
    """Har birlik `<ota>--<nom>` nomi bilan: restore_backup.py shuni kutadi."""
    os.makedirs(backup_to, exist_ok=True)
    for path in paths:
        leaf = os.path.basename(path)
        parent = os.path.basename(os.path.dirname(path))
        nusxa(path, os.path.join(backup_to, "%s--%s" % (parent, leaf)))


class Ctx(object):
    """Bir yurish uchun yo'llar va tanlangan rejim."""

    def __init__(self, opts):
        home = os.path.expanduser("~")
        # HOME="" yoki "/" bo'lsa expanduser "/" beradi va ~/.claude o'rniga
        # /.claude ga tegilardi.
        if not home or home == "~" or not os.path.isabs(home) or not home.strip("/"):
            raise Xato("uy papkasi aniqlanmadi yoki ildiz papka (HOME=%r)." % home)
        self.opts = opts
        self.apply = opts.apply
        self.reset = opts.reset
        self.update = not opts.reset      # sukut qo'shuvchi (ps1: $Update = -not $Reset)
        self.home = home
        self.claude = os.path.join(home, ".claude")
        self.auth = os.path.join(home, ".claude.json")
        self.settings_path = os.path.join(self.claude, "settings.json")
        self.skill_dst = os.path.join(self.claude, "skills", "manguberdi")
        self.agents_dst = os.path.join(self.claude, "agents")
        self.manifest_path = os.path.join(self.skill_dst, ".genius.json")
        self.stage = None
        self.src = None                   # commit tarkibi (git archive), vaqtinchalik
        self.changed = False              # birinchi o'chirish boshlandimi
        self.stage_skill = None
        self.stage_agents = None
        self.root = None                  # asboblar turadigan joy: snapshot
        self.clone = None                 # klon: memory, holat va o'rnatuvchi manbasi
        self.sha = ""                     # snapshot olingan commit (to'liq)
        self.python = sys.executable
        self.proj_claude = None
        self.backup_to = None

    def rejim(self):
        return "BAJARILADI" if self.apply else "quruq yurish (--apply bermadingiz)"


def sinov_yigimi(ctx):
    """Skill avval vaqtinchalik papkada yig'iladi va sinaladi, keyin o'rniga
    ko'chadi. Yo'l almashtirish yoki indeks yiqilsa, hali hech narsa o'chmagan.

    Manba klonning ishchi daraxti emas, snapshot olinadigan commit tarkibi
    (`git archive`, git ga yozmaydi): quruq yurish ham, --apply ham aynan
    snapshotga tushadigan matnni sinaydi. Snapshot hali yo'q, shuning uchun
    `--root-keyin`: yo'l almashtirish kelajakdagi snapshot yo'li bilan yuradi.

    Qaytaradi: (allow ro'yxati, opt-in bo'lagi matni).
    """
    root = ctx.root
    rewriter = os.path.join(ctx.clone, "install", "rewrite_paths.py")
    ctx.stage = tempfile.mkdtemp(prefix="manguberdi-")
    stage_skill = os.path.join(ctx.stage, "skills", "manguberdi")
    stage_agents = os.path.join(ctx.stage, "agents")
    ctx.stage_skill, ctx.stage_agents = stage_skill, stage_agents

    say()
    say("0. Sinov yig'imi -> %s" % ctx.stage)
    step("python: %s" % ctx.python)
    step("bash  : bash (skill matnida shu nom)")
    step("manba : commit %s (klonning ishchi daraxti emas)" % ctx.sha[:snapshot.SHA_UZUNLIK])

    # Alohida papka: `--allow` va `--opt-in` ctx.stage dagi hamma .md ni
    # o'qiydi, commit tarkibidagi hujjatlar (bobda `tools/x.py` eslatmasi
    # bor) ruxsat ro'yxatiga kirib qolmasin.
    ctx.src = tempfile.mkdtemp(prefix="manguberdi-src-")
    commit_src = os.path.join(ctx.src, "commit")
    try:
        snapshot.arxiv(ctx.clone, ctx.sha, commit_src)
    except snapshot.SnapshotXato as exc:
        raise Xato("commit tarkibi olinmadi, hech narsa o'chmadi: %s" % exc) from exc
    klon_tekshir(commit_src, ctx.reset, "commit %s" % ctx.sha[:snapshot.SHA_UZUNLIK])

    os.makedirs(os.path.dirname(stage_skill))
    os.makedirs(stage_agents)
    shutil.copytree(os.path.join(commit_src, ".claude", "skills", "manguberdi"), stage_skill)
    for actor in ACTORS:
        src = os.path.join(commit_src, ".claude", "agents", actor + ".md")
        if not os.path.exists(src):
            say("  OGOHLANTIRISH: aktyor fayli yo'q: %s.md" % actor)
            continue
        shutil.copy2(src, stage_agents)

    common = ["--root", root, "--clone", ctx.clone, "--root-keyin",
              "--python", ctx.python, "--bash", "bash"]
    for target in (stage_skill, stage_agents):
        code, out = run_py([rewriter, target] + common)
        if code:
            raise Xato("yo'llarni almashtirish yiqildi, hech narsa o'chmadi: %s" % out)
        step(out)
        code, out = run_py([rewriter, target, "--root", root, "--clone", ctx.clone,
                            "--root-keyin", "--tekshir"])
        if code:
            raise Xato("nisbiy yo'l qoldi, hech narsa o'chmadi: %s" % out)

    # Qoida buyruq matnining aynan boshlanishi bo'lishi shart: ro'yxatni
    # yo'llarni yozgan asbob o'zi beradi.
    code, out = run_py([rewriter, ctx.stage] + common + ["--allow"])
    if code:
        raise Xato("ruxsat ro'yxati yasalmadi, hech narsa o'chmadi: %s" % out)
    try:
        allow = [str(rule) for rule in json.loads(out)]
    except ValueError:
        raise Xato("ruxsat ro'yxati o'qilmadi: %s" % out) from None
    step("ruxsat qoidasi: %d ta" % len(allow))

    # run_tests.py global ruxsatga kirmaydi: u proyektning build kodini
    # bajaradi. Tayyor settings.local.json bo'lagini rewrite_paths beradi.
    code, out = run_py([rewriter, ctx.stage] + common + ["--opt-in"])
    if code:
        raise Xato("opt-in ruxsat bo'lagi yasalmadi, hech narsa o'chmadi: %s" % out)
    return allow, out


def opt_in_korsat(opt_in):
    if not opt_in:
        return
    say()
    say("Ixtiyoriy: run_tests.py global ruxsatda yo'q, chunki u proyektning "
        "build kodini bajaradi. Faqat O'ZINGIZ ishonadigan proyektda u "
        "so'rovsiz yursin desangiz, shu bo'lakni <proyekt>/.claude/settings.local.json "
        "ga qo'shing. Fork PR, namuna repo yoki begona klonda qo'shmang.")
    say(opt_in)


def manifest_yoz(ctx):
    """Manifest skill nusxasi bilan birga: qaysi commit o'rnatilgani saqlanadi.

    `commit` va `root` snapshotniki (hooklar yuradigan joy), `clone` klonniki:
    budget.py va doctor.py o'rnatilgan commitni klon HEAD bilan solishtiradi,
    tools/yangilash.py klonni shu yerdan topadi."""
    commit = ctx.sha
    version = ""
    version_file = os.path.join(ctx.root, "VERSION")
    if os.path.isfile(version_file):
        with open(version_file, encoding="utf-8") as handle:
            version = handle.read().strip()
    manifest = {
        "versiya": version,
        "commit": commit,
        "sana": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "root": ctx.root,
        "clone": ctx.clone,
        "python": ctx.python,
        "actors": list(ACTORS),
    }
    yoz_atomik(ctx.manifest_path, json_matn(manifest))


def own_roots(ctx):
    """Settings.json da o'zimniki sanaladigan ildizlar: klon, uning mavjud
    snapshotlari (klon o'chgan yoki ko'chgan bo'lsa yetim ham) va yangi snapshot.

    Yangilashda eski snapshotga ishora qilgan hook shu yo'l bilan almashadi,
    aks holda eski va yangi hook birga yurardi. Boshqa klonning snapshoti
    begona: u `snapshot.royxat` ga kirmaydi."""
    roots = [ctx.clone] + snapshot.royxat(ctx.clone, ctx.claude, yetim=True) + [ctx.root]
    out = []
    for item in roots:
        if item not in out:
            out.append(item)
    return out


def root_args(roots):
    args = []
    for item in roots:
        args += ["--root", item]
    return args


def snapshot_yarat(ctx):
    """--apply: snapshot (git worktree --detach) va undagi indeks.

    Hech narsa almashtirilmasdan oldin, zaxiradan keyin: yiqilsa eski
    o'rnatish joyida qoladi. Mavjud snapshot qayta ishlatiladi, lekin
    tekshiriladi (boshqa commit yoki o'zgartirilgan bo'lsa xato).
    Indeks hosila: snapshotda bir marta yasaladi (build_index.py snapshotning
    o'zidan), keyin hooklar uni faqat o'qiydi."""
    index_dir = os.path.join(ctx.root, "index")
    if not ctx.apply:
        step("snapshot: %s (--apply bilan git worktree add --detach)" % ctx.root)
        step("indeks: %s (--apply bilan yasaladi)" % index_dir)
        return
    try:
        path, created = snapshot.yarat(ctx.clone, ctx.claude, ctx.sha)
    except snapshot.SnapshotXato as exc:
        raise Xato("snapshot yaratilmadi, hech narsa o'chmadi: %s" % exc) from exc
    step("snapshot %s: %s" % ("yaratildi" if created else "mavjud, qayta ishlatildi", path))
    code, out = run_py([os.path.join(path, "tools", "build_index.py")],
                       env={"GENIUS_CLONE": ctx.clone})
    if code or not os.path.isfile(os.path.join(index_dir, "sections.tsv")):
        raise Xato("indeks yasalmadi, hech narsa o'chmadi: %s" % out)
    step("indeks yasaldi: %s" % index_dir)


def ornatish(ctx, allow):
    root, apply = ctx.root, ctx.apply
    tools_dir = os.path.join(root, "tools")
    merger = os.path.join(ctx.clone, "install", "merge_settings.py")

    stage_settings = os.path.join(ctx.stage, "settings.json")
    text = json_matn(sozlama_yasa(ctx.python, root, allow, ctx.clone))
    with open(stage_settings, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    roots = root_args(own_roots(ctx))

    # Qo'shuvchi rejimda settings.json ga yozmasdan nima almashishini aytadi.
    if ctx.update:
        code, out = run_py([merger, ctx.settings_path, stage_settings] + roots)
        if code:
            raise Xato("settings.json birlashtirilmadi, hech narsa o'chmadi: %s" % out)
        step(out)

    # --- 1. Zaxira ---
    say()
    say("1. Zaxira -> %s" % ctx.backup_to)
    to_remove = []
    if ctx.update:
        own = [ctx.skill_dst] + [os.path.join(ctx.agents_dst, a + ".md") for a in ACTORS]
        # Eski aktyor zaxiralanib o'chiriladi va qaytib o'rnatilmaydi. Ro'yxat
        # manifest (skill papkasi ichida) o'chishidan OLDIN olinadi.
        for actor in eski_aktyorlar(ctx.manifest_path):
            stale = os.path.join(ctx.agents_dst, actor + ".md")
            if os.path.exists(stale):
                step("eski aktyor: %s (endi o'rnatilmaydi)" % actor)
                own.append(stale)
        to_remove = [p for p in own if os.path.lexists(p)]
        to_backup = list(to_remove)
        if os.path.exists(ctx.settings_path):
            to_backup.append(ctx.settings_path)
    else:
        for name in CONFIG_ITEMS:
            path = os.path.join(ctx.claude, name)
            if os.path.lexists(path):
                to_remove.append(path)
        if ctx.opts.include_auth and os.path.exists(ctx.auth):
            to_remove.append(ctx.auth)
        if ctx.proj_claude:
            if os.path.exists(ctx.proj_claude):
                to_remove.append(ctx.proj_claude)
            else:
                step("proyektda .claude yo'q: %s" % ctx.opts.project)
        to_backup = list(to_remove)

    xavfsiz_joylashuv(ctx, to_remove)
    if not to_backup:
        step("zaxiraga narsa yo'q, sozlama topilmadi")
    else:
        for path in to_backup:
            step(path)
        if apply:
            zaxira_ol(to_backup, ctx.backup_to)
            step("zaxira yozildi: %d birlik" % len(to_backup))

    # --- 1b. Snapshot ---
    say()
    say("1b. Snapshot (hooklar shu commitdan yuradi)")
    step("commit: %s, klon: %s" % (ctx.sha[:snapshot.SHA_UZUNLIK], ctx.clone))
    snapshot_yarat(ctx)

    # --- 2. Almashtirish yoki tozalash ---
    say()
    say("2. Almashtirish" if ctx.update else "2. Tozalash")
    for path in to_remove:
        step(("almashtiriladi: %s" if ctx.update else "o'chiriladi: %s") % path)
        if apply:
            ctx.changed = True
            olib_tashla(path)
    if ctx.update:
        step("qoladi: boshqa skill va agentlar, CLAUDE.md, plugins/, settings.json dagi "
             "boshqa yozuvlar")
    if not ctx.opts.include_auth:
        step("qoladi: %s (user MCP serverlar, proyekt trust, onboarding; "
             "--include-auth bilan o'chadi)" % ctx.auth)
        for name in user_mcp(ctx.auth):
            step("qoladi: user MCP server %s (olib tashlash: claude mcp remove %s -s user)"
                 % (name, name))
    step("qoladi: .credentials.json (kirish tokeni), projects/, todos/, history.jsonl "
         "(suhbat tarixi)")

    # --- 3. O'rnatish ---
    say()
    say("3. manguberdi o'rnatilmoqda")
    step("skill  -> %s" % ctx.skill_dst)
    step("aktyorlar -> %s" % ctx.agents_dst)
    staged = sorted(n for n in os.listdir(ctx.stage_agents) if n.endswith(".md"))
    for name in staged:
        step("  " + name[:-3])
    if apply:
        # copytree mavjud papkaga ko'chirmaydi: eski skill avval o'chiriladi.
        olib_tashla(ctx.skill_dst)
        os.makedirs(os.path.dirname(ctx.skill_dst), exist_ok=True)
        shutil.copytree(ctx.stage_skill, ctx.skill_dst)
        os.makedirs(ctx.agents_dst, exist_ok=True)
        for name in staged:
            shutil.copy2(os.path.join(ctx.stage_agents, name), ctx.agents_dst)
    step("manifest -> %s" % ctx.manifest_path)
    if apply:
        manifest_yoz(ctx)

    # --- 4. Sozlama ---
    say()
    say("4. Sozlama -> %s" % ctx.settings_path)
    step("yetti hook: bo'lim taklifi, budjetni nolga tushirish, kontekst o'lchovi, "
         "qo'riqchi, aktyor budjeti, kod tekshiruvi, sarf hisobi")
    step("yo'llar mutlaq, manba (snapshot): %s" % tools_dir)
    step("ruxsat: snapshotning docs va klonning memory papkalari "
         "additionalDirectories da, %d ta asbob buyrug'i oldindan ruxsatli" % len(allow))
    step("env.GENIUS_CLONE: memory va holat klonga yoziladi, snapshotga emas")
    step("so'raladi: run_tests.py, guruh.py birlashtir va tozala (yon ta'siri bor)")
    if ctx.update:
        step("birlashtiriladi: klonga ishora qilmagan hook, ruxsat (allow, ask, deny) "
             "va papkalar saqlanadi")
    if apply:
        os.makedirs(ctx.claude, exist_ok=True)
        if ctx.update:
            code, out = run_py([merger, ctx.settings_path, stage_settings]
                               + roots + ["--yoz"])
            if code:
                raise Xato("settings.json birlashtirilmadi va o'zgarmadi, skill va "
                           "aktyorlar esa yangilandi. Zaxira: %s. %s"
                           % (ctx.backup_to, out))
            step(out)
        else:
            yoz_atomik(ctx.settings_path, text)


def tekshirish(ctx):
    """Asboblarning o'zi ishlayaptimi: har qatlamdan bitta arzon chaqiruv."""
    root = ctx.root
    tools_dir = os.path.join(root, "tools")
    ok = True
    # Hooklar settings.json env ni oladi: yoziladigan narsa klonga tushsin,
    # sinov snapshotga `.claude/.state` yaratmasin.
    hook_env = {"GENIUS_CLONE": ctx.clone}

    if os.path.isfile(os.path.join(ctx.skill_dst, "SKILL.md")):
        step("skill joyida")
    else:
        step("XATO: skill ko'chmadi")
        ok = False

    try:
        count = len([n for n in os.listdir(ctx.agents_dst) if n.endswith(".md")])
    except OSError:
        count = 0
    step("aktyor fayli: %d" % count)
    if count < len(ACTORS):
        ok = False

    for actor in RETIRED:
        if os.path.exists(os.path.join(ctx.agents_dst, actor + ".md")):
            step("XATO: eski aktyor qoldi: %s.md" % actor)
            ok = False

    if os.path.isfile(ctx.manifest_path):
        step("manifest yozildi: %s" % ctx.manifest_path)
    else:
        step("XATO: manifest yozilmadi: %s" % ctx.manifest_path)
        ok = False

    try:
        with open(ctx.settings_path, encoding="utf-8") as handle:
            written = json.load(handle)
        step("settings.json o'qiladi")
        # Hook yo'li klonga emas, snapshotga ishora qilishi shart (XV-Y1).
        own = [h.get("command", "") for groups in (written.get("hooks") or {}).values()
               for g in groups for h in g.get("hooks", [])
               if (root + "/tools/") in h.get("command", "").replace("\\", "/")]
        if own:
            step("hook yo'li snapshotga ishora qiladi: %d ta" % len(own))
        else:
            step("XATO: hook yo'li snapshotga ishora qilmaydi (%d ta)" % len(own))
            ok = False
    except (OSError, ValueError, AttributeError, TypeError):
        step("XATO: settings.json buzuq")
        ok = False

    # Nisbiy yo'l qolmaganini tasdiqlash: qolsa skill boshqa proyektda jim
    # ishlamaydi.
    rewriter = os.path.join(ctx.clone, "install", "rewrite_paths.py")
    for target in (ctx.skill_dst, ctx.agents_dst):
        code, out = run_py([rewriter, target, "--root", root, "--clone", ctx.clone,
                            "--tekshir"])
        if code == 0:
            step("nisbiy yo'l qolmadi: %s" % os.path.basename(target))
        else:
            step("XATO: %s" % out)
            ok = False

    code, out = run_py([os.path.join(tools_dir, "budget.py"), "--holat"], env=hook_env)
    if code == 0:
        step("asboblar ishlayapti")
    else:
        step("XATO: budget.py yiqildi: %s" % out)
        ok = False

    # CLAUDE_PROJECT_DIR ni Claude Code har hook jarayoniga beradi va hook
    # faqat klonda yoki Java proyektida ishlaydi: shu yerda u klonga qo'yiladi.
    code, out = run_py([os.path.join(tools_dir, "suggest_sections.py")],
                       '{"prompt":"circuit breaker"}',
                       dict(hook_env, GENIUS_HOOK_DEBUG="1", CLAUDE_PROJECT_DIR=ctx.clone))
    if code == 0 and "patterns" in out:
        step("bo'lim taklifi ishlayapti")
    else:
        step("XATO: bo'lim taklifi bo'sh: %s" % out)
        ok = False

    bash = shutil.which("bash")
    if bash:
        env = dict(os.environ, GENIUS_PYTHON=ctx.python, PYTHONIOENCODING="utf-8",
                   **hook_env)
        proc = subprocess.run([bash, os.path.join(tools_dir, "doc.sh"), "find",
                               "circuit breaker"], stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, env=env,
                              encoding="utf-8", errors="replace")
        if proc.returncode == 0:
            step("doc.sh ishlayapti")
        else:
            step("XATO: doc.sh ishlamadi (bash ichida python3 yo'qmi?): %s"
                 % proc.stdout.strip())
            ok = False
    return ok


def olib_tashlash(ctx):
    """--uninstall: o'z birliklarini olib tashlash.

    Klon mavjud bo'lishi SHART EMAS: klon o'chirilgan yoki ko'chirilgan va
    settings.json da uning yo'li qolgan holat uchun. Yordamchi skript shu
    fayl yonidan olinadi (HERE), --genius-path dan EMAS.
    """
    uninstaller = os.path.join(HERE, "uninstall_settings.py")
    if not os.path.isfile(uninstaller):
        raise Xato("%s topilmadi. --uninstall shu fayl bilan birga ishlaydi: klonning "
                   "install/ papkasidan yurgizing, yoki settings.json ni qo'lda tahrir "
                   "qiling (install/README.md, 'Klon o'chsa yoki ko'chsa')."
                   % uninstaller)

    say()
    say("manguberdi olib tashlanmoqda")
    say("Ildiz : %s" % ctx.clone)
    say("Global: %s" % ctx.claude)
    say("Rejim : %s" % ctx.rejim())

    own = []
    if os.path.lexists(ctx.skill_dst):
        own.append(ctx.skill_dst)
    # Egalik: manifest (skill papkasi ichida, o'rnatuvchi yozgan) bo'lsa faqat
    # undagi `actors` olinadi. Manifest yo'q bo'lsa manguberdi o'rnatganini
    # tasdiqlab bo'lmaydi: ps1 kabi nom bo'yicha, lekin har fayl uchun
    # ogohlantirish. Ro'yxat o'chirishdan OLDIN olinadi: manifest skill
    # papkasi bilan birga o'chadi.
    listed = manifest_aktyorlar(ctx.manifest_path)
    if listed is not None:
        names, by_name = listed, False
    else:
        names, by_name = list(ACTORS) + eski_aktyorlar(ctx.manifest_path), True
    for actor in names:
        path = os.path.join(ctx.agents_dst, actor + ".md")
        if os.path.lexists(path):
            own.append(path)
            if by_name:
                step("OGOHLANTIRISH: manifest yo'q, %s nom bo'yicha olinadi: "
                     "manguberdi o'rnatganini tasdiqlab bo'lmaydi" % path)
    # Snapshotlar: shu klonniki (klon o'chgan bo'lsa yetimlari ham), faqat
    # ~/.claude/genius ostida. Ular zaxiralanmaydi: git dan qayta yasaladi.
    snaps = snapshot.royxat(ctx.clone, ctx.claude, yetim=True)
    xavfsiz_joylashuv(ctx, own + snaps)

    say()
    say("1. Zaxira -> %s" % ctx.backup_to)
    to_backup = list(own)
    if os.path.exists(ctx.settings_path):
        to_backup.append(ctx.settings_path)
    if not to_backup:
        step("zaxiraga narsa yo'q")
    else:
        for path in to_backup:
            step(path)
        if ctx.apply:
            zaxira_ol(to_backup, ctx.backup_to)
            step("zaxira yozildi: %d birlik" % len(to_backup))

    say()
    say("2. Skill va aktyorlar")
    if not own:
        step("manguberdi birliklari topilmadi")
    for path in own:
        step("o'chiriladi: %s" % path)
        if ctx.apply:
            ctx.changed = True
            olib_tashla(path)
    for path in snaps:
        step("snapshot o'chiriladi (git worktree remove): %s" % path)
        if ctx.apply:
            ctx.changed = True
            try:
                snapshot.olib_tashla(path, ctx.clone, ctx.claude)
            except snapshot.SnapshotXato as exc:
                raise Xato("snapshot o'chmadi: %s" % exc) from exc
    if not snaps:
        step("snapshot topilmadi: %s" % snapshot.genius_dir(ctx.claude))

    say()
    say("3. Sozlama -> %s" % ctx.settings_path)
    args = [uninstaller, ctx.settings_path] + root_args([ctx.clone] + snaps)
    if ctx.apply:
        args.append("--yoz")
    code, out = run_py(args)
    if code:
        raise Xato("settings.json o'zgarmadi: %s" % out)
    step(out)

    say()
    if ctx.apply:
        say("Tayyor. manguberdi olib tashlandi, begona yozuvlar joyida.")
        say("Zaxira: %s" % ctx.backup_to)
        say("Yangi sessiyada o'zgarish ko'rinadi.")
    else:
        say("Quruq yurish tugadi. Bajarish uchun --apply qo'shing.")
    return 0


def parser_yasa():
    parser = argparse.ArgumentParser(
        description="manguberdi skillini Linux va macOS da o'rnatadi. Sukut quruq "
                    "yurish: --apply bermaguncha ~/.claude ga tegilmaydi.")
    parser.add_argument("--genius-path", default=CLONE,
                        help="claude-genius klonining yo'li (sukut: shu fayl turgan klon)")
    parser.add_argument("--apply", action="store_true",
                        help="haqiqatan bajarish; bersiz faqat ro'yxat")
    parser.add_argument("--update", action="store_true",
                        help="eski nom, sukut xulq bilan bir xil (qo'shuvchi qayta o'rnatish)")
    parser.add_argument("--uninstall", action="store_true",
                        help="faqat manguberdi birliklarini olib tashlaydi")
    parser.add_argument("--reset", action="store_true",
                        help="to'liq tozalash (--apply bilan --confirm-reset ham kerak)")
    parser.add_argument("--confirm-reset", action="store_true",
                        help="--reset --apply uchun ikkinchi tasdiq")
    parser.add_argument("--include-auth", action="store_true",
                        help="--reset bilan ~/.claude.json ham zaxiralanib o'chadi")
    parser.add_argument("--project", default="",
                        help="--reset bilan shu proyektdagi .claude/ ham tozalanadi")
    parser.add_argument("--backup-to", default="",
                        help="zaxira papkasi (sukut ~/.claude-backup-<vaqt>), bo'sh bo'lmasa rad etiladi")
    return parser


def run(opts):
    if os.name == "nt":
        raise Xato("install.py faqat Linux va macOS uchun. Windows da "
                   "install/manguberdi.ps1 ishlatiladi.")
    if sys.version_info < (3, 8):
        raise Xato("Python 3.8+ kerak, hozir %d.%d: hooklar shu versiyaga yozilgan."
                   % sys.version_info[:2])
    tekshir_argumentlar(opts)
    ctx = Ctx(opts)
    try:
        return ish(ctx, opts)
    except (OSError, shutil.Error) as exc:
        # Kutilmagan fayl tizimi xatosi traceback bo'lib chiqmasin. "Hech
        # narsa o'chmadi" faqat birinchi o'chirishgacha rost.
        if ctx.changed:
            tail = ("O'rnatish yarim qoldi: ba'zi birliklar allaqachon almashtirilgan. "
                    "Zaxira: %s. Sababni tuzatib qayta yurgizing." % ctx.backup_to)
        else:
            tail = "Hech narsa o'chmadi."
        raise Xato("%s: %s. %s" % (type(exc).__name__, exc, tail)) from exc


def ish(ctx, opts):

    # --uninstall da klon mavjud bo'lishi shart emas: yo'l faqat settings.json
    # dagi yozuvlarni tanish uchun satr, shuning uchun faqat normallanadi.
    root = os.path.abspath(opts.genius_path).rstrip("/")
    ctx.clone = root
    if opts.uninstall:
        if not root.strip("/").strip():
            raise Xato("--genius-path bo'sh: olib tashlanadigan yozuvlarni tanib bo'lmaydi.")
    else:
        if not os.path.isdir(root):
            raise Xato("GeniusPath topilmadi: %s" % opts.genius_path)
        xavfsiz_yol("GeniusPath", root)
        klon_tekshir(root, opts.reset)
    ctx.root = root
    if not opts.uninstall:
        # Hooklar aniq commit dagi snapshotdan yuradi (XV-Y1): joyi HEAD
        # shasidan. Klon git repo bo'lmasa pin qilib bo'lmaydi.
        try:
            ctx.sha = snapshot.sha_ol(root)
        except snapshot.SnapshotXato as exc:
            raise Xato("%s Hech narsa o'zgarmadi." % exc) from exc
        ctx.root = snapshot.snapshot_yol(ctx.claude, ctx.sha).replace("\\", "/")
        xavfsiz_yol("Snapshot", ctx.root)

    if opts.project:
        project, ctx.proj_claude = project_tekshir(opts.project, ctx.claude, root)
        opts.project = project

    ctx.backup_to = opts.backup_to or os.path.join(
        ctx.home, ".claude-backup-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    zaxira_tekshir(ctx.backup_to)

    if not opts.uninstall:
        xavfsiz_yol("Python", ctx.python)
    else:
        return olib_tashlash(ctx)

    bash = shutil.which("bash")
    say()
    say("Manba : %s" % root)
    say("Snapshot: %s (commit %s)" % (ctx.root, ctx.sha[:snapshot.SHA_UZUNLIK]))
    say("Klon  : %s (hooklar shu klonning commitidan olinadi)" % root)
    # Ro'yxatsiz o'tishni yashirmaslik: hook kodi o'rnatilgan commitdan farq qilsa
    # nima kelayotgani ko'rsatiladi (to'smaydi; tasdiqli yo'l tools/yangilash.py).
    try:
        diff_text = snapshot.farq_matn(root, ctx.claude, ctx.sha)
    except snapshot.SnapshotXato:
        diff_text = ""
    if diff_text:
        say()
        say(diff_text)
        say()
    dirty = snapshot.git(["-C", root, "status", "--porcelain", "--untracked-files=no"],
                         timeout=30).stdout.strip()
    if dirty:
        say("OGOHLANTIRISH: klonda commit qilinmagan o'zgarish bor. U snapshotga "
            "KIRMAYDI: hooklar aniq commit %s dan yuradi." % ctx.sha[:snapshot.SHA_UZUNLIK])
    say("Python: %s" % ctx.python)
    say("Bash  : %s" % (bash or "TOPILMADI"))
    say("Global: %s" % ctx.claude)
    if opts.project:
        say("Proyekt: %s" % opts.project)
    say("Rejim : %s, %s" % (ctx.rejim(), "TO'LIQ TOZALASH (--reset)" if opts.reset
                            else "qo'shuvchi: faqat manguberdi birliklari"))
    managed_ogohlantirish()

    # tools/doc.sh bash skripti va qidiruv qatlamining hammasi unga tayanadi.
    if not bash:
        raise Xato("bash topilmadi, hech narsa o'zgarmadi. tools/doc.sh (find, show, "
                   "rule) usiz ishlamaydi: bash o'rnating va qayta yurgizing.")

    try:
        allow, opt_in = sinov_yigimi(ctx)
        ornatish(ctx, allow)
    finally:
        for temp in (ctx.stage, ctx.src):
            if temp and os.path.isdir(temp):
                shutil.rmtree(temp, ignore_errors=True)

    say()
    say("5. Tekshirish")
    if not ctx.apply:
        say()
        say("Sozlama o'zgarmadi. Bajarish uchun ayni buyruqqa --apply qo'shing.")
        opt_in_korsat(opt_in)
        return 0

    if tekshirish(ctx):
        say()
        say("Tayyor. Yangi sessiyada /manguberdi deb chaqiring.")
        say("Zaxira: %s" % ctx.backup_to)
        say()
        say("Hooklar va qo'llanma snapshotdan o'qiladi: %s" % ctx.root)
        say("(commit %s). Klondagi `git pull` ularni O'ZGARTIRMAYDI." % ctx.sha[:snapshot.SHA_UZUNLIK])
        say("Yangilash (snapshotdagi nusxa, klondagi emas): python3 %s/tools/yangilash.py "
            "(ro'yxatni ko'rsatadi, tasdiq so'raydi)." % ctx.root)
        say("Memory va holat klonda: %s. Klon ko'chirilsa skriptni yangi yo'l bilan qayta "
            "yurgizing." % ctx.clone)
        opt_in_korsat(opt_in)
        return 0
    say()
    say("O'rnatish to'liq emas, yuqoriga qarang. Zaxira: %s" % ctx.backup_to)
    return 1


def main(argv=None):
    opts = parser_yasa().parse_args(argv)
    try:
        return run(opts)
    except Xato as exc:
        print("XATO: %s" % exc)
        return 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
