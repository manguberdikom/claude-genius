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


def case_memory_protocol():
    """Klon ildizidagi qoida fayli ham mutlaq bo'ladi va qayta tutilmaydi."""
    out, n = one("Qoida manbai `memory-protocol.md`.")
    second, n2 = one(out)
    return (n == 1 and out == "Qoida manbai `%s/memory-protocol.md`." % GENIUS
            and n2 == 0 and second == out
            and R.relative_left("`memory-protocol.md`") == ["memory-protocol.md"])


def case_memory_protocol_bosh_joyli():
    """Fayl `awk '...' <fayl>` argumenti ham bo'ladi: bo'sh joyda qo'shtirnoq."""
    out, _ = one("`awk '/x/' memory-protocol.md`", root="C:/Program Files/genius")
    return out == "`awk '/x/' \"C:/Program Files/genius/memory-protocol.md\"`"


def case_memory_protocol_chegarasi():
    """Yalang nom almashadi; boshqa papkadagi yoki boshqa nomli fayl emas."""
    out, n = one("`memory-protocol.md` dagi")
    other = "`../memory-protocol.md` va `my-memory-protocol.md`"
    kept, n2 = one(other)
    return (n == 1 and out == "`%s/memory-protocol.md` dagi" % GENIUS
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
            "`memory/umumiy/` va `memory-protocol.md`")
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
    more = R.relative_left("./tools/doc.sh, `memory-protocol.md` va "
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
    ("memory-protocol.md", case_memory_protocol),
    ("bo'sh joyli memory-protocol.md qo'shtirnoqda", case_memory_protocol_bosh_joyli),
    ("../ va boshqa nomli memory-protocol.md tegilmaydi", case_memory_protocol_chegarasi),
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
    ("ps1 hook jadvali settings.json ga mos", case_ps1_hooklari_repoga_mos),
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
