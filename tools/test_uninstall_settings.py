#!/usr/bin/env python3
"""install/uninstall_settings.py uchun sinovlar.

    python3 tools/test_uninstall_settings.py

Olib tashlash o'rnatishning teskarisi: shuning uchun asosiy holat
o'rnatuvchi yozgan settings.json ni olib, undan hamma o'z yozuvi
ketganini va begona yozuvlarning hammasi qolganini tekshiradi.
"""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INSTALL = os.path.join(ROOT, "install")
TOOL = os.path.join(INSTALL, "uninstall_settings.py")

GENIUS = "C:/src/claude-genius"
PY = "C:/Python312/python.exe"


def own_cmd(name):
    return '"%s" "%s/tools/%s"' % (PY, GENIUS, name)


def installed():
    """O'rnatuvchi yozadigan shakl, ichida begona yozuvlar ham bor."""
    return {
        "$schema": "https://json.schemastore.org/claude-code-settings.json",
        "env": {"GENIUS_PYTHON": PY, "MENING": "1"},
        "permissions": {
            "additionalDirectories": [GENIUS + "/docs", GENIUS + "/memory",
                                      "D:/mening"],
            "allow": ["Bash(%s:*)" % own_cmd("budget.py"),
                      "Bash(bash %s/tools/doc.sh:*)" % GENIUS,
                      "Bash(npm test:*)", "Read"],
            "deny": ["Bash(rm:*)"],
        },
        "model": "opus",
        "hooks": {
            "UserPromptSubmit": [{"hooks": [
                {"type": "command", "command": own_cmd("suggest_sections.py")},
                {"type": "command", "command": "python3 mening-hookim.py"},
            ]}],
            "PreToolUse": [
                {"matcher": "Read|Bash", "hooks": [
                    {"type": "command", "command": own_cmd("guard.py")}]},
                {"matcher": "Edit", "hooks": [
                    {"type": "command", "command": "mening.py"}]},
            ],
            "Stop": [{"hooks": [
                {"type": "command", "command": own_cmd("usage.py") + " --saqlash"}]}],
        },
    }


@contextlib.contextmanager
def workdir():
    tmp = tempfile.mkdtemp(prefix="uninst_")
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def write_json(path, data, bom=False):
    raw = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
    with open(path, "wb") as handle:
        handle.write((b"\xef\xbb\xbf" if bom else b"") + raw)


def run(tmp, data, root=GENIUS, write=True, bom=False):
    path = os.path.join(tmp, "settings.json")
    if data is not None:
        write_json(path, data, bom=bom)
    args = [sys.executable, TOOL, path, "--root", root]
    if write:
        args.append("--yoz")
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), path


def load(path):
    with open(path, encoding="utf-8-sig") as handle:
        return json.load(handle)


def case_oz_yozuvlari_ketadi():
    """Hamma o'z yozuvi ketadi, begonalari qoladi."""
    with workdir() as tmp:
        code, out, path = run(tmp, installed())
        got = load(path)
        commands = [h["command"] for groups in got["hooks"].values()
                    for g in groups for h in g.get("hooks", [])]
        return (code == 0
                and not any(GENIUS in c for c in commands)
                and sorted(commands) == ["mening.py", "python3 mening-hookim.py"]
                and got["permissions"]["allow"] == ["Bash(npm test:*)", "Read"]
                and got["permissions"]["additionalDirectories"] == ["D:/mening"]
                and got["permissions"]["deny"] == ["Bash(rm:*)"]
                and got["env"] == {"MENING": "1"}
                and got["model"] == "opus"
                and got["$schema"].endswith("claude-code-settings.json")
                and "olib tashlandi" in out)


def case_bosh_guruh_va_hodisa_tushadi():
    """Faqat o'z hooki bo'lgan guruh, va shundan bo'shagan hodisa tushadi."""
    data = {"hooks": {"Stop": [{"hooks": [{"command": own_cmd("usage.py")}]}],
                      "PreToolUse": [{"hooks": [{"command": "begona.py"}]}]}}
    with workdir() as tmp:
        code, _, path = run(tmp, data)
        got = load(path)
        return (code == 0 and "Stop" not in got.get("hooks", {})
                and len(got["hooks"]["PreToolUse"]) == 1)


def case_env_bosh_qolsa_tushadi():
    with workdir() as tmp:
        code, _, path = run(tmp, {"env": {"GENIUS_PYTHON": PY}, "model": "x"})
        got = load(path)
        return code == 0 and "env" not in got and got["model"] == "x"


def case_boshqa_klon_tegilmaydi():
    """`<root>-eski` boshqa klon: uning yozuvlari o'zniki emas."""
    other = GENIUS + "-eski"
    data = {"hooks": {"Stop": [{"hooks": [
                {"command": '"%s" "%s/tools/usage.py"' % (PY, other)}]}]},
            "permissions": {"allow": ["Bash(bash %s/tools/doc.sh:*)" % other]}}
    with workdir() as tmp:
        code, out, path = run(tmp, data)
        got = load(path)
        return (code == 0 and len(got["hooks"]["Stop"]) == 1
                and len(got["permissions"]["allow"]) == 1
                and "topilmadi" in out)


def case_teskari_slash_va_registr():
    """Windows da ildiz teskari slash va boshqa registrda berilishi mumkin."""
    with workdir() as tmp:
        code, _, path = run(tmp, installed(), root="C:\\SRC\\Claude-Genius")
        got = load(path)
        commands = [h["command"] for groups in got["hooks"].values()
                    for g in groups for h in g.get("hooks", [])]
        return code == 0 and not any("claude-genius" in c for c in commands)


def case_ask_deny_va_ichki_papkalar_ketadi():
    """ask va deny dagi o'z qoidalari, butun klon yozuvi va `<root>/`
    ostidagi papkalar ham olinadi. Avval faqat allow va ildizning o'zi
    olinardi, `<root>/docs` qolib ketardi (XV-T-M1). Boshqa klon qoladi."""
    data = {"permissions": {
        "additionalDirectories": [GENIUS, GENIUS + "/docs", "C:\\SRC\\Claude-Genius\\memory",
                                  GENIUS + "-eski/docs", "D:/mening"],
        "ask": ["Bash(%s tozala:*)" % own_cmd("guruh.py"), "Bash(git push:*)"],
        "deny": ["Edit(%s/tools/**)" % GENIUS, "Read(~/.ssh/**)"]}}
    with workdir() as tmp:
        code, out, path = run(tmp, data)
        perm = load(path)["permissions"]
        under = [d for d in perm["additionalDirectories"]
                 if d.replace("\\", "/").lower().startswith(GENIUS.lower() + "/")
                 or d == GENIUS]
        return (code == 0 and under == []
                and perm["additionalDirectories"] == [GENIUS + "-eski/docs", "D:/mening"]
                and perm["ask"] == ["Bash(git push:*)"]
                and perm["deny"] == ["Read(~/.ssh/**)"]
                and "2 ruxsat" in out and "3 additionalDirectories" in out)


def case_mavjud_bolmagan_ildiz():
    """Klon o'chirilgan bo'lsa ham yozuvlar olinadi: yo'l tekshirilmaydi."""
    missing = "C:/yoq/papka/claude-genius"
    data = {"hooks": {"Stop": [{"hooks": [
        {"command": '"%s" "%s/tools/usage.py"' % (PY, missing)}]}]}}
    with workdir() as tmp:
        code, _, path = run(tmp, data, root=missing)
        return code == 0 and "hooks" not in load(path)


def case_quruq_yurish_yozmaydi():
    with workdir() as tmp:
        path = os.path.join(tmp, "settings.json")
        write_json(path, installed())
        with open(path, "rb") as handle:
            before = handle.read()
        code, out, _ = run(tmp, None, write=False)
        with open(path, "rb") as handle:
            after = handle.read()
        return code == 0 and before == after and "quruq" in out


def case_bom_oqiladi_bomsiz_yoziladi():
    with workdir() as tmp:
        code, _, path = run(tmp, installed(), bom=True)
        with open(path, "rb") as handle:
            raw = handle.read()
        return code == 0 and not raw.startswith(b"\xef\xbb\xbf")


def case_snapshot_va_klon_ildizlari():
    """R7.8 XV-Y1: klon va snapshot yo'llari `--root` takroran beriladi: hooklar,
    ruxsat, docs (snapshot) va memory (klon) yozuvlari, env.GENIUS_CLONE ketadi;
    boshqa klonning snapshoti va begona yozuv qoladi."""
    snap = "C:/Users/a/.claude/genius/0123456789ab"
    boshqa = "C:/Users/a/.claude/genius/ffffffffffff"
    data = installed()
    data["env"]["GENIUS_CLONE"] = GENIUS
    data["hooks"]["UserPromptSubmit"][0]["hooks"] = [
        {"type": "command", "command": '"%s" "%s/tools/suggest_sections.py"' % (PY, snap)},
        {"type": "command", "command": '"%s" "%s/tools/budget.py"' % (PY, boshqa)}]
    data["permissions"]["additionalDirectories"] = [
        snap + "/docs", GENIUS + "/memory", boshqa + "/docs", "D:/mening"]
    with workdir() as tmp:
        path = os.path.join(tmp, "settings.json")
        write_json(path, data)
        proc = subprocess.run([sys.executable, TOOL, path, "--root", GENIUS,
                               "--root", snap, "--yoz"], capture_output=True, text=True)
        got = load(path)
        cmds = [h["command"] for gs in got["hooks"].values() for g in gs for h in g["hooks"]]
        return (proc.returncode == 0
                and not any(snap in c or GENIUS in c for c in cmds)
                and any(boshqa in c for c in cmds)
                and got["permissions"]["additionalDirectories"] == [boshqa + "/docs", "D:/mening"]
                and got["env"] == {"MENING": "1"})


def case_fayl_yoq():
    with workdir() as tmp:
        code, out, _ = run(tmp, None)
        return code == 0 and "yo'q" in out


def case_buzuq_json():
    with workdir() as tmp:
        path = os.path.join(tmp, "settings.json")
        io.open(path, "w", encoding="utf-8").write("{buzuq")
        proc = subprocess.run([sys.executable, TOOL, path, "--root", GENIUS,
                               "--yoz"], capture_output=True, text=True)
        return (proc.returncode == 1
                and io.open(path, encoding="utf-8").read() == "{buzuq")


def case_bosh_ildiz_rad_etiladi():
    """Bo'sh ildiz hamma yozuvni o'zniki deb o'qib yuborishi mumkin edi."""
    with workdir() as tmp:
        code, out, _ = run(tmp, installed(), root="  /  ")
        return code == 1 and "bo'sh" in out


def case_ikkinchi_yurish_ozgartirmaydi():
    with workdir() as tmp:
        run(tmp, installed())
        path = os.path.join(tmp, "settings.json")
        with open(path, "rb") as handle:
            first = handle.read()
        subprocess.run([sys.executable, TOOL, path, "--root", GENIUS, "--yoz"],
                       capture_output=True, text=True)
        with open(path, "rb") as handle:
            return first == handle.read()


CASES = [
    ("snapshot va klon ildizlari (--root takroran)", case_snapshot_va_klon_ildizlari),
    ("o'z yozuvlari ketadi, begonalari qoladi", case_oz_yozuvlari_ketadi),
    ("bo'shab qolgan guruh va hodisa tushadi", case_bosh_guruh_va_hodisa_tushadi),
    ("env bo'sh qolsa env ham tushadi", case_env_bosh_qolsa_tushadi),
    ("`<root>-eski` boshqa klon, tegilmaydi", case_boshqa_klon_tegilmaydi),
    ("teskari slash va katta harfli ildiz", case_teskari_slash_va_registr),
    ("ask, deny va ildiz ostidagi papkalar ham olinadi",
     case_ask_deny_va_ichki_papkalar_ketadi),
    ("mavjud bo'lmagan ildiz ham ishlaydi", case_mavjud_bolmagan_ildiz),
    ("quruq yurish faylga tegmaydi", case_quruq_yurish_yozmaydi),
    ("BOM o'qiladi, BOM siz yoziladi", case_bom_oqiladi_bomsiz_yoziladi),
    ("fayl yo'q: 0 va xabar", case_fayl_yoq),
    ("buzuq JSON: 1, fayl tegilmaydi", case_buzuq_json),
    ("bo'sh ildiz rad etiladi", case_bosh_ildiz_rad_etiladi),
    ("ikkinchi yurish o'zgartirmaydi", case_ikkinchi_yurish_ozgartirmaydi),
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
