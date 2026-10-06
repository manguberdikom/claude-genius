#!/usr/bin/env python3
"""install/rewrite_paths.py uchun sinovlar.

    python3 tools/test_rewrite_paths.py

Nega bu asbobga sinov kerak: o'rnatuvchining PowerShell qismi sinalmaydi,
shuning uchun u iloji boricha ozroq ish qilishi va asosiy mantiq shu
yerda, sinaladigan joyda turishi kerak. Noto'g'ri almashtirish jim
o'tadi: skill o'rnatiladi, ko'rinishidan joyida, lekin har buyruq
"No such file or directory" beradi.
"""

import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "install"))

import rewrite_paths as R  # noqa: E402

GENIUS = "C:/src/claude-genius"


def one(text, root=GENIUS, bash="bash", python="python3"):
    return R.rewrite(text, root, bash, python)


def case_python_chaqiruvi():
    out, n = one("python3 tools/rules_for.py <fayllar>")
    return n == 1 and out == "python3 %s/tools/rules_for.py <fayllar>" % GENIUS


def case_backtick_ichida():
    """Markdown da buyruqlar backtick ichida yoziladi: ular ham almashadi."""
    out, n = one("`tools/doc.sh show patterns 17.2`")
    return n == 1 and out == "`bash %s/tools/doc.sh show patterns 17.2`" % GENIUS


def case_python3siz_py():
    out, n = one("chiqishni tools/parse_test_output.py ga bering")
    return n == 1 and "python3 %s/tools/parse_test_output.py" % GENIUS in out


def case_doc_sh_bash_bilan():
    out, _ = one("tools/doc.sh find saga")
    return out.startswith("bash %s/tools/doc.sh" % GENIUS)


def case_bash_nomi_beriladi():
    """Qo'lda qo'shtirnoq bilan berilgan bash ikki qavat o'ralmaydi."""
    out, _ = one("tools/doc.sh toc", bash='"C:/Git/bin/bash.exe"')
    return out == '"C:/Git/bin/bash.exe" %s/tools/doc.sh toc' % GENIUS


def case_bash_bosh_joyli_qoshtirnoqlanadi():
    """O'rnatuvchi bash yo'lini qo'shtirnoqsiz beradi. Git for Windows
    standart holda `Program Files` da: qo'shtirnoqsiz yo'lni shell
    `C:/Program` ga bo'lib yuboradi va har doc.sh buyrug'i yiqiladi."""
    out, _ = one("tools/doc.sh toc", bash="C:/Program Files/Git/bin/bash.exe")
    return out == '"C:/Program Files/Git/bin/bash.exe" %s/tools/doc.sh toc' % GENIUS


def case_bash_teskari_slash():
    out, _ = one("tools/doc.sh toc",
                 bash="C:\\Program Files\\Git\\bin\\bash.exe")
    return out == '"C:/Program Files/Git/bin/bash.exe" %s/tools/doc.sh toc' % GENIUS


def case_bash_bosh_joysiz_qoshtirnoqsiz():
    out, _ = one("tools/doc.sh toc", bash="C:/Git/bin/bash.exe")
    return out == "C:/Git/bin/bash.exe %s/tools/doc.sh toc" % GENIUS


def case_bash_prefiksi_ikkilanmaydi():
    out, n = one("`bash tools/doc.sh find saga`")
    return n == 1 and out == "`bash %s/tools/doc.sh find saga`" % GENIUS


def case_python_3siz_chaqiruv():
    out, n = one("python tools/check_code.py a")
    return n == 1 and out == "python3 %s/tools/check_code.py a" % GENIUS


def case_nuqta_slash():
    sh, n1 = one("./tools/doc.sh toc")
    py, n2 = one("python3 ./tools/rules_for.py x")
    return (n1 == 1 and sh == "bash %s/tools/doc.sh toc" % GENIUS
            and n2 == 1 and py == "python3 %s/tools/rules_for.py x" % GENIUS)


# ROOT_FILES hozir bo'sh (memory qoidasi memory/README.md ga ko'chdi va
# uni MEM_PATH almashtiradi), lekin mexanizm qoladi: ildizga yana shunday
# fayl qo'shilishi mumkin. Shuning uchun quyidagi holatlar soxta nom
# qo'yib mexanizmning o'zini sinaydi.


@contextlib.contextmanager
def root_files(*names):
    saved_names, saved_re = R.ROOT_FILES, R.ROOT_FILE
    R.ROOT_FILES = names
    R.ROOT_FILE = R.root_file_re(names)
    try:
        yield
    finally:
        R.ROOT_FILES, R.ROOT_FILE = saved_names, saved_re


def case_root_file_bosh_royxat():
    """Bo'sh ROOT_FILES hech narsani tutmaydi.

    Avval naqsh `(%s)` bilan yasalardi: bo'sh ro'yxatda u bo'sh guruhga
    aylanib matnning har joyida mos kelardi va rewrite() butun faylni
    buzardi.
    """
    assert R.ROOT_FILES == ()
    text = "qoida.md va memory-protocol.md va oddiy matn"
    out, n = one(text)
    return out == text and n == 0 and R.relative_left(text) == []


def case_root_file():
    """Ildizdagi qoida fayli mutlaq bo'ladi va qayta tutilmaydi."""
    with root_files("qoida.md"):
        out, n = one("Qoida manbai `qoida.md`.")
        second, n2 = one(out)
        return (n == 1 and out == "Qoida manbai `%s/qoida.md`." % GENIUS
                and n2 == 0 and second == out
                and R.relative_left("`qoida.md`") == ["qoida.md"])


def case_root_file_bosh_joyli():
    """Fayl `awk '...' <fayl>` argumenti ham bo'ladi: bo'sh joyda qo'shtirnoq."""
    with root_files("qoida.md"):
        out, _ = one("`awk '/x/' qoida.md`", root="C:/Program Files/genius")
        return out == "`awk '/x/' \"C:/Program Files/genius/qoida.md\"`"


def case_root_file_chegarasi():
    """Yalang nom almashadi; boshqa papkadagi yoki boshqa nomli fayl emas."""
    with root_files("qoida.md"):
        out, n = one("`qoida.md` dagi")
        other = "`../qoida.md` va `my-qoida.md`"
        kept, n2 = one(other)
        return (n == 1 and out == "`%s/qoida.md` dagi" % GENIUS
                and n2 == 0 and kept == other
                and R.relative_left(other) == [])


def case_memory_yoli():
    out, n = one("`memory/<proyekt-slug>/MEMORY.md` indeksini o'qing")
    return n == 1 and "%s/memory/<proyekt-slug>/" % GENIUS in out


def case_mutlaq_yol_tegilmaydi():
    """Allaqachon mutlaq yo'l ikkinchi marta almashmaydi."""
    text = "python3 /opt/genius/tools/rules_for.py x"
    out, n = one(text)
    return n == 0 and out == text


def case_idempotent():
    """Ikki marta yurgizish bir marta bilan bir xil natija beradi."""
    text = ("python3 tools/rules_for.py x va tools/doc.sh find y, "
            "`memory/umumiy/` va `memory/README.md`")
    first, _ = one(text)
    second, n = one(first)
    spaced = dict(root="C:/Program Files/genius",
                  bash="C:/Program Files/Git/bin/bash.exe")
    first_sp, _ = one(text, **spaced)
    second_sp, n_sp = one(first_sp, **spaced)
    return n == 0 and second == first and n_sp == 0 and second_sp == first_sp


def case_teskari_slash_tozalanadi():
    out, _ = one("tools/doc.sh toc", root="C:\\src\\claude-genius\\")
    return out == "bash C:/src/claude-genius/tools/doc.sh toc"


def case_bosh_joyli_yol_qoshtirnoqda():
    out, _ = one("python3 tools/budget.py --holat",
                 root="C:/Program Files/genius")
    return '"C:/Program Files/genius/tools/budget.py"' in out


def case_quvur_ichida():
    out, n = one("mvn -q test | python3 tools/parse_test_output.py")
    return n == 1 and out.endswith("%s/tools/parse_test_output.py" % GENIUS)


def case_qolgani_sanaladi():
    left = R.relative_left("tools/doc.sh va python3 tools/x.py va memory/umumiy/")
    more = R.relative_left("./tools/doc.sh, `memory/umumiy/` va "
                           "$CLAUDE_PROJECT_DIR/tools/guard.py")
    return len(left) == 3 and len(more) == 3


def case_almashtirilgandan_keyin_qolmaydi():
    out, _ = one("tools/doc.sh va python3 tools/x.py va memory/umumiy/")
    return R.relative_left(out) == []


def case_prefikssiz_doc_sh_sanaladi():
    """`doc.sh checklist testing` rewrite() ga tushmaydi va boshqa proyektda
    "command not found" beradi: --tekshir uni sanashi shart. Argumentsiz
    eslatma (`doc.sh show`) buyruq emas, test_skill.py dagi qoida bilan bir
    xil tutilmaydi. Mutlaq qilingan buyruq ikkinchi marta sanalmaydi."""
    return (R.relative_left("va `doc.sh checklist testing`") != []
            and R.relative_left("`bash doc.sh toc`") != []
            and R.relative_left("bo'lim o'qiladi (`doc.sh show`).") == []
            and R.relative_left(R.rewrite("tools/doc.sh show x 1", "/opt/g")[0]) == [])


PY_SPACED = "C:/Program Files/Python312/python.exe"
BASH_SPACED = "C:/Program Files/Git/bin/bash.exe"


def case_python_yoli_beriladi():
    """O'rnatuvchi sys.executable ni beradi: bo'sh joyli bo'lsa qo'shtirnoqda,
    teskari slash to'g'rilanadi, ikkinchi yurgizish tegmaydi."""
    out, n = one("python3 tools/rules_for.py x", python=PY_SPACED)
    back, _ = one("tools/budget.py --holat", python=PY_SPACED.replace("/", "\\"))
    second, n2 = one(out, python=PY_SPACED)
    return (n == 1 and out == '"%s" %s/tools/rules_for.py x' % (PY_SPACED, GENIUS)
            and back == '"%s" %s/tools/budget.py --holat' % (PY_SPACED, GENIUS)
            and n2 == 0 and second == out)


def run_main(argv):
    """main() ni chaqiradi: (qaytish kodi, stdout)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = R.main(argv)
    return code, out.getvalue()


def case_allow_qoidasi_buyruq_boshlanishi():
    """Ruxsat qoidasi buyruq matnining aynan boshlanishi bo'lmasa, mos
    kelmaydi va har buyruq so'rov beradi. Bo'sh joyli root, python va bash
    bilan --allow chiqishi rewrite() yozgan buyruqlarga solishtiriladi."""
    tmp = tempfile.mkdtemp(prefix="rw_allow_")
    try:
        root = os.path.join(tmp, "Program Files", "genius")
        folder = os.path.join(tmp, "stage")
        os.makedirs(root)
        os.makedirs(folder)
        commands = ["tools/doc.sh show patterns 17.2",
                    "python3 tools/budget.py --holat"]
        written = [R.rewrite(c, root, BASH_SPACED, PY_SPACED)[0] for c in commands]
        io.open(os.path.join(folder, "SKILL.md"), "w", encoding="utf-8").write(
            "\n".join(written) + "\nnisbiy qoldiq: python3 tools/x.py\n")
        code, out = run_main([folder, "--root", root, "--python", PY_SPACED,
                              "--bash", BASH_SPACED, "--allow"])
        rules = json.loads(out)
        prefixes = [r[len("Bash("):-len(":*)")] for r in rules
                    if r.startswith("Bash(") and r.endswith(":*)")]
        covered = all(any(cmd.startswith(p + " ") for p in prefixes)
                      for cmd in written)
        return (code == 0 and len(rules) == len(prefixes) == 2 and covered
                and any(p.startswith('"%s" "' % BASH_SPACED) for p in prefixes)
                and any(p.startswith('"%s" "' % PY_SPACED) for p in prefixes)
                and io.open(os.path.join(folder, "SKILL.md"),
                            encoding="utf-8").read().startswith(written[0]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def case_root_yoq_bolsa_2():
    """Mavjud bo'lmagan klonga yo'l yozilsa, har buyruq "No such file"
    beradi: o'rnatuvchi hech narsa o'chmasidan oldin to'xtashi kerak."""
    tmp = tempfile.mkdtemp(prefix="rw_root_")
    try:
        io.open(os.path.join(tmp, "SKILL.md"), "w", encoding="utf-8").write(
            "tools/doc.sh toc")
        code, _ = run_main([tmp, "--root", os.path.join(tmp, "yoq")])
        untouched = io.open(os.path.join(tmp, "SKILL.md"),
                            encoding="utf-8").read() == "tools/doc.sh toc"
        return code == 2 and untouched
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def real_stage(tmp, root, python="python3"):
    """Haqiqiy skill va aktyorlar nusxasi, yo'llari mutlaq qilingan."""
    stage = os.path.join(tmp, "stage")
    shutil.copytree(os.path.join(ROOT, ".claude", "skills", "manguberdi"),
                    os.path.join(stage, "manguberdi"))
    agents = os.path.join(stage, "agents")
    os.makedirs(agents)
    src = os.path.join(ROOT, ".claude", "agents")
    for name in os.listdir(src):
        if name.endswith(".md"):
            shutil.copy(os.path.join(src, name), agents)
    code, _ = run_main([stage, "--root", root, "--python", python])
    if code != 0:
        raise AssertionError("rewrite yiqildi: %d" % code)
    return stage


def case_allow_run_tests_va_guruh_cheklangan():
    """Haqiqiy skillning --allow chiqishida run_tests.py yo'q (fork PR da
    build kodi so'rovsiz bajarilardi, XV-K1). guruh.py uchun faqat yarat va
    royxat: birlashtir va tozala so'raladi (XV-T1). Yon ta'sirsiz asboblar
    joyida qoladi."""
    tmp = tempfile.mkdtemp(prefix="rw_allow_real_")
    try:
        root = os.path.join(tmp, "genius")
        os.makedirs(root)
        stage = real_stage(tmp, root)
        code, out = run_main([stage, "--root", root, "--allow"])
        rules = json.loads(out)
        guruh = sorted(r for r in rules if "/tools/guruh.py" in r)
        prefix = R.tool_cmd(R.clean_root(root), "python3", "guruh.py")
        return (code == 0 and len(rules) >= 8
                and not any("run_tests.py" in r for r in rules)
                and guruh == ["Bash(%s royxat:*)" % prefix,
                              "Bash(%s yarat:*)" % prefix]
                and "Bash(%s:*)" % R.tool_cmd(R.clean_root(root), "python3",
                                               "rules_for.py") in rules
                and any("/tools/doc.sh:*)" in r for r in rules))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def case_allow_aniq_royxat():
    """Sintetik matnda --allow aniq ro'yxat beradi: run_tests tushadi,
    guruh ikki subbuyruqqa bo'linadi, qolgani bitta qoidadan."""
    text = "\n".join(R.rewrite(c, GENIUS)[0] for c in (
        "python3 tools/run_tests.py --diff --yurgiz",
        "python3 tools/guruh.py tozala --hammasi",
        "python3 tools/budget.py --holat",
        "tools/doc.sh find saga"))
    py = "python3 %s/tools/" % GENIUS
    return R.allow_rules(text, GENIUS) == sorted([
        "Bash(bash %s/tools/doc.sh:*)" % GENIUS,
        "Bash(%sbudget.py:*)" % py,
        "Bash(%sguruh.py royxat:*)" % py,
        "Bash(%sguruh.py yarat:*)" % py,
    ]) and R.opt_in_rules(text, GENIUS) == ["Bash(%srun_tests.py:*)" % py]


def case_opt_in_bolagi():
    """--opt-in settings.local.json bo'lagini beradi: ichida faqat
    run_tests qoidasi, u esa skill yozgan buyruqning aynan boshlanishi."""
    tmp = tempfile.mkdtemp(prefix="rw_optin_")
    try:
        root = os.path.join(tmp, "Program Files", "genius")
        os.makedirs(root)
        stage = real_stage(tmp, root, python=PY_SPACED)
        code, out = run_main([stage, "--root", root, "--python", PY_SPACED,
                              "--opt-in"])
        data = json.loads(out)
        rules = data["permissions"]["allow"]
        prefix = R.tool_cmd(R.clean_root(root), PY_SPACED, "run_tests.py")
        texts = [io.open(p, encoding="utf-8").read() for p in R.walk(stage)]
        return (code == 0 and list(data) == ["permissions"]
                and rules == ["Bash(%s:*)" % prefix]
                and any(prefix + " " in t for t in texts))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def case_xavfli_belgili_yol_2():
    """`$`, backtick yoki qo'sh qo'shtirnoq bor --root yoki --python: hook
    buyrug'i bash da "..." ichida yuradi va bu belgi u yerda kengayadi
    (XV-P2). 2 qaytadi va fayl tegilmaydi."""
    tmp = tempfile.mkdtemp(prefix="rw_unsafe_")
    try:
        skill = os.path.join(tmp, "SKILL.md")
        io.open(skill, "w", encoding="utf-8").write("tools/doc.sh toc")
        results = []
        for char in ("$", "`", '"'):
            bad = os.path.join(tmp, "g%sx" % char)
            try:
                os.makedirs(bad)
            except OSError:
                pass  # Windows da " papka nomida bo'lmaydi: matn baribir sinaladi
            for argv in ([tmp, "--root", bad],
                         [tmp, "--root", tmp, "--python", "C:/py%s/python.exe" % char],
                         [tmp, "--root", bad, "--allow"]):
                code, out = run_main(argv)
                results.append(code == 2 and out == "")
        untouched = io.open(skill, encoding="utf-8").read() == "tools/doc.sh toc"
        return all(results) and len(results) == 9 and untouched
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def ps1_text():
    return io.open(os.path.join(ROOT, "install", "manguberdi.ps1"),
                   encoding="utf-8").read()


def case_ps1_papkalar_va_opt_in():
    """ps1 sinalmaydi, matni tekshiriladi: additionalDirectories da butun
    klon emas, faqat docs va memory (XV-Y4); opt-in bo'lagi rewrite_paths
    dan olinadi va ko'rsatiladi; GeniusPath va Python yo'li xavfli belgida
    to'xtatiladi (XV-P2)."""
    text = ps1_text()
    dirs = re.search(r"additionalDirectories = @\(([^)]*)\)", text)
    if not dirs:
        raise AssertionError("ps1 da additionalDirectories topilmadi")
    entries = re.findall(r'"([^"]*)"', dirs.group(1))
    unsafe = re.search(r"\$UnsafeChars = \[char\[\]\]@\(([^)]*)\)", text)
    return (entries == ["$g/docs", "$g/memory"]
            and "'--opt-in')" in text
            and text.count("Show-OptIn") >= 3
            and unsafe is not None
            and sorted(re.findall(r"'(.)'", unsafe.group(1))) == sorted(R.UNSAFE_CHARS)
            and "Test-SafePath 'GeniusPath' $GeniusPath" in text
            and "Test-SafePath 'Python' $PythonExe" in text)


def case_ps1_manifest_va_eski_aktyor():
    """ps1 matni (OC-K5): .genius.json budget.py o'qiydigan joyga va
    kalitlar bilan yoziladi; $Retired dagi nom hozirgi aktyor emas va
    yangilash hamda -Uninstall ikkalasida olinadi."""
    text = ps1_text()
    budget = io.open(os.path.join(ROOT, "tools", "budget.py"),
                     encoding="utf-8").read()
    actors = re.search(r"\$Actors = @\(([^)]*)\)", text)
    retired = re.search(r"\$Retired = @\(([^)]*)\)", text)
    manifest = re.search(r"\$manifest = \[ordered\]@\{(.*?)\n  \}", text, re.S)
    if not (actors and retired and manifest):
        raise AssertionError("ps1 da $Actors, $Retired yoki $manifest topilmadi")
    current = re.findall(r"'([\w-]+)'", actors.group(1))
    old = re.findall(r"'([\w-]+)'", retired.group(1))
    keys = re.findall(r"^\s*(\w+)\s*=", manifest.group(1), re.M)
    agents = {name[:-3] for name in os.listdir(os.path.join(ROOT, ".claude", "agents"))}
    return ("arxitektor" in old and not set(old) & set(current)
            and not set(old) & agents and set(current) <= agents
            and keys == ["versiya", "commit", "sana", "root", "python", "actors"]
            and "skills\\manguberdi\\.genius.json" in text
            and '"manguberdi", ".genius.json"' in budget
            and 'manifest.get("commit")' in budget
            and 'manifest.get("root")' in budget
            # ta'rif, -Uninstall va yangilash
            and text.count("Get-StaleActors") >= 3)


# PowerShell sinalmaydi, lekin u yasaydigan hook jadvali matndan o'qiladi
# va repodagi .claude/settings.json ga solishtiriladi: biri o'zgarib
# ikkinchisi unutilsa, global o'rnatish jim boshqacha ishlaydi.
PS_HOOK_TOKEN = re.compile(
    r"^\s*(?P<event>\w+) = @\("
    r"|(?P<group>\[ordered\]@\{ (?:matcher = '(?P<matcher>[^']*)'; )?hooks = @\()"
    r"|HookCmd '(?P<script>[^']+)'\)(?: \+ '(?P<arg>[^']*)')?"
    r"|timeout = (?P<timeout>\d+)"
    r"|statusMessage = (?:\"(?P<dq>[^\"]*)\"|'(?P<sq>[^']*)')", re.M)
SETTINGS_CMD = re.compile(r'tools/(\w+\.py)"?\s*(.*)')


def ps1_hooks():
    """manguberdi.ps1 dagi `hooks = [ordered]@{` dan `$settingsPath` gacha."""
    text = io.open(os.path.join(ROOT, "install", "manguberdi.ps1"),
                   encoding="utf-8").read()
    start = text.index("hooks = [ordered]@{")
    block = text[start:text.index("$settingsPath", start)]
    hooks, event, matcher = [], "", ""
    for m in PS_HOOK_TOKEN.finditer(block):
        if m.group("event"):
            event, matcher = m.group("event"), ""
        elif m.group("group"):
            matcher = m.group("matcher") or ""
        elif m.group("script"):
            hooks.append([event, matcher, m.group("script"),
                          (m.group("arg") or "").strip(), None, ""])
        elif m.group("timeout") and hooks:
            hooks[-1][4] = int(m.group("timeout"))
        elif hooks:
            hooks[-1][5] = m.group("dq") if m.group("dq") is not None else m.group("sq")
    return sorted(tuple(h) for h in hooks)


def settings_hooks():
    data = json.load(io.open(os.path.join(ROOT, ".claude", "settings.json"),
                             encoding="utf-8"))
    hooks = []
    for event, groups in data.get("hooks", {}).items():
        for group in groups:
            for hook in group.get("hooks", []):
                m = SETTINGS_CMD.search(hook.get("command", ""))
                script, arg = (m.group(1), m.group(2).strip()) if m else (
                    hook.get("command", ""), "")
                hooks.append((event, group.get("matcher", ""), script, arg,
                              hook.get("timeout"), hook.get("statusMessage", "")))
    return sorted(hooks)


def case_ps1_hooklari_repoga_mos():
    ps, repo = ps1_hooks(), settings_hooks()
    # Naqsh hech narsani tutmasa ikki bo'sh ro'yxat teng chiqadi: yolg'on
    # yashil bo'lmasin.
    if len(ps) < 5 or len(repo) < 5:
        raise AssertionError("hook kam o'qildi: ps1 %d, settings.json %d"
                             % (len(ps), len(repo)))
    if ps != repo:
        only_ps = [h for h in ps if h not in repo]
        only_repo = [h for h in repo if h not in ps]
        raise AssertionError("faqat ps1 da: %s; faqat settings.json da: %s"
                             % (only_ps, only_repo))
    return True


def case_papkani_yuradi():
    """Papkadagi har .md fayl almashadi, boshqa tur tegilmaydi."""
    tmp = tempfile.mkdtemp(prefix="rw_")
    try:
        sub = os.path.join(tmp, "references")
        os.makedirs(sub)
        io.open(os.path.join(tmp, "SKILL.md"), "w", encoding="utf-8").write(
            "python3 tools/budget.py --holat")
        io.open(os.path.join(sub, "a.md"), "w", encoding="utf-8").write(
            "tools/doc.sh toc")
        io.open(os.path.join(tmp, "b.txt"), "w", encoding="utf-8").write(
            "tools/doc.sh toc")
        files = list(R.walk(tmp))
        if len(files) != 2:
            return False
        for path in files:
            text = io.open(path, encoding="utf-8").read()
            new, _ = R.rewrite(text, GENIUS)
            io.open(path, "w", encoding="utf-8").write(new)
        skill = io.open(os.path.join(tmp, "SKILL.md"), encoding="utf-8").read()
        nested = io.open(os.path.join(sub, "a.md"), encoding="utf-8").read()
        plain = io.open(os.path.join(tmp, "b.txt"), encoding="utf-8").read()
        return (GENIUS in skill and GENIUS in nested
                and plain == "tools/doc.sh toc")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def case_haqiqiy_skill_toza_qoladi():
    """Haqiqiy skill nusxasida bitta ham nisbiy yo'l qolmaydi."""
    tmp = tempfile.mkdtemp(prefix="rw_real_")
    try:
        shutil.copytree(os.path.join(ROOT, ".claude", "skills", "manguberdi"),
                        os.path.join(tmp, "manguberdi"))
        agents = os.path.join(tmp, "agents")
        os.makedirs(agents)
        src = os.path.join(ROOT, ".claude", "agents")
        for name in os.listdir(src):
            if name.endswith(".md"):
                shutil.copy(os.path.join(src, name), agents)
        changed = 0
        for path in R.walk(tmp):
            text = io.open(path, encoding="utf-8").read()
            new, count = R.rewrite(text, GENIUS)
            changed += count
            io.open(path, "w", encoding="utf-8").write(new)
        texts = [io.open(p, encoding="utf-8").read() for p in R.walk(tmp)]
        left = sum(len(R.relative_left(t)) for t in texts)
        # relative_left faqat ma'lum naqshlarni sanaydi. Klon ildizidagi
        # yangi faylga havola qo'shilsa, u naqshda yo'q va sinov yolg'on
        # yashil beradi (memory-protocol.md aynan shunday topildi). Shuning
        # uchun ildizdagi har .md nomi alohida qidiriladi. CLAUDE.md va
        # README.md maqsadli proyektning o'z fayli, ular nisbiy qoladi.
        names = [n for n in os.listdir(ROOT) if n.endswith(".md")
                 and n not in ("CLAUDE.md", "README.md")]
        stray = [n for n in names for t in texts
                 if re.search(r"(?<![\w/.-])%s\b" % re.escape(n), t)]
        # Almashtirish bo'lishi SHART: nol bo'lsa, naqsh hech narsani
        # tutmagan va sinov yolg'on yashil beradi.
        return changed > 30 and left == 0 and not stray
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


CASES = [
    ("python3 tools/x.py", case_python_chaqiruvi),
    ("backtick ichidagi buyruq", case_backtick_ichida),
    ("python3 siz .py yo'li", case_python3siz_py),
    ("doc.sh bash bilan chaqiriladi", case_doc_sh_bash_bilan),
    ("bash yo'li berilsa ishlatiladi", case_bash_nomi_beriladi),
    ("bo'sh joyli bash yo'li qo'shtirnoqda", case_bash_bosh_joyli_qoshtirnoqlanadi),
    ("bash yo'lidagi teskari slash", case_bash_teskari_slash),
    ("bo'sh joysiz bash qo'shtirnoqsiz", case_bash_bosh_joysiz_qoshtirnoqsiz),
    ("bash prefiksi ikkilanmaydi", case_bash_prefiksi_ikkilanmaydi),
    ("python (3 siz) chaqiruvi", case_python_3siz_chaqiruv),
    ("./tools/ yo'li", case_nuqta_slash),
    ("bo'sh ROOT_FILES hech narsa tutmaydi", case_root_file_bosh_royxat),
    ("ildizdagi qoida fayli", case_root_file),
    ("bo'sh joyli ildiz fayli qo'shtirnoqda", case_root_file_bosh_joyli),
    ("../ va boshqa nomli ildiz fayli tegilmaydi", case_root_file_chegarasi),
    ("memory yo'li", case_memory_yoli),
    ("mutlaq yo'l tegilmaydi", case_mutlaq_yol_tegilmaydi),
    ("ikki marta yurgizish xavfsiz", case_idempotent),
    ("teskari slash to'g'rilanadi", case_teskari_slash_tozalanadi),
    ("bo'sh joyli yo'l qo'shtirnoqda", case_bosh_joyli_yol_qoshtirnoqda),
    ("quvur ichidagi chaqiruv", case_quvur_ichida),
    ("qolgan nisbiy yo'l sanaladi", case_qolgani_sanaladi),
    ("almashtirgandan keyin qolmaydi", case_almashtirilgandan_keyin_qolmaydi),
    ("prefikssiz doc.sh buyrug'i sanaladi", case_prefikssiz_doc_sh_sanaladi),
    ("python yo'li berilsa ishlatiladi", case_python_yoli_beriladi),
    ("--allow qoidasi buyruqning aynan boshlanishi", case_allow_qoidasi_buyruq_boshlanishi),
    ("mavjud bo'lmagan --root 2 qaytaradi", case_root_yoq_bolsa_2),
    ("--allow da run_tests yo'q, guruh faqat yarat va royxat",
     case_allow_run_tests_va_guruh_cheklangan),
    ("--allow aniq ro'yxat, run_tests opt-in da", case_allow_aniq_royxat),
    ("--opt-in settings.local.json bo'lagi", case_opt_in_bolagi),
    ("$, backtick yoki qo'shtirnoqli yo'l 2 qaytaradi", case_xavfli_belgili_yol_2),
    ("ps1: docs va memory papkasi, opt-in, xavfli belgi", case_ps1_papkalar_va_opt_in),
    ("ps1 hook jadvali settings.json ga mos", case_ps1_hooklari_repoga_mos),
    ("ps1: .genius.json manifesti va eski aktyor", case_ps1_manifest_va_eski_aktyor),
    ("papka bo'ylab yuradi, .md dan boshqasi tegilmaydi", case_papkani_yuradi),
    ("haqiqiy skillda nol nisbiy yo'l", case_haqiqiy_skill_toza_qoladi),
]


def main():
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn())
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
