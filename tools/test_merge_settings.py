#!/usr/bin/env python3
"""install/merge_settings.py uchun sinovlar.

    python3 tools/test_merge_settings.py

Nega bu asbobga sinov kerak: `manguberdi.ps1 -Update` foydalanuvchining
~/.claude/settings.json iga yozadi, PowerShell qismi esa agent sessiyasida
sinalmaydi. Noto'g'ri birlashtirish jim o'tadi: begona hook yoki ruxsat
yo'qoladi, o'z hooki esa ikki marta qoladi va har navbatda ikki marta
ishlaydi.
"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "install"))

import merge_settings as M  # noqa: E402

GENIUS = "C:/src/claude-genius"
WIN_PY = "C:\\Python312\\python.exe"


def own_cmd(script, root=GENIUS, python=WIN_PY):
    """ps1 dagi HookCmd ko'rinishi: teskari slash va qo'shtirnoq bilan."""
    return '"%s" "%s\\tools\\%s"' % (python, root.replace("/", "\\"), script)


def hook(command, **extra):
    entry = {"type": "command", "command": command}
    entry.update(extra)
    return entry


def fresh(root=GENIUS):
    """Toza o'rnatishning settings.json i (ps1 yasaydigan shakl)."""
    return {
        "$schema": "https://json.schemastore.org/claude-code-settings.json",
        "env": {"GENIUS_PYTHON": WIN_PY.replace("\\", "/")},
        "permissions": {
            "additionalDirectories": [root + "/docs", root + "/memory"],
            "allow": ['Bash("%s" "%s/tools/budget.py":*)'
                      % (WIN_PY.replace("\\", "/"), root),
                      "Bash(bash %s/tools/doc.sh:*)" % root],
        },
        "hooks": {
            "UserPromptSubmit": [{"hooks": [
                hook(own_cmd("suggest_sections.py", root), timeout=10),
                hook(own_cmd("budget.py", root), timeout=10)]}],
            "PreToolUse": [{"matcher": "Read|Bash|PowerShell", "hooks": [
                hook(own_cmd("guard.py", root), timeout=10)]}],
        },
    }


def run_main(argv):
    """main() ni chaqiradi: (qaytish kodi, stdout)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = M.main(argv)
    return code, out.getvalue() + err.getvalue()


@contextlib.contextmanager
def workdir():
    tmp = tempfile.mkdtemp(prefix="merge_")
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def write_json(path, data, bom=False):
    raw = json.dumps(data, indent=4, ensure_ascii=False).encode("utf-8")
    with open(path, "wb") as handle:
        handle.write((b"\xef\xbb\xbf" if bom else b"") + raw)


def read_bytes(path):
    with open(path, "rb") as handle:
        return handle.read()


def merge_files(tmp, existing, bom=False, yoz=True, root=GENIUS):
    """existing ni faylga yozib main() ni yurgizadi: (kod, chiqish, yo'l)."""
    old = os.path.join(tmp, "settings.json")
    new = os.path.join(tmp, "yangi.json")
    if existing is not None:
        write_json(old, existing, bom=bom)
    write_json(new, fresh(root))
    argv = [old, new, "--root", root] + (["--yoz"] if yoz else [])
    code, out = run_main(argv)
    return code, out, old


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def commands(data, event):
    return [h["command"] for g in data["hooks"].get(event, [])
            for h in g.get("hooks", [])]


def case_mavjud_fayl_yoq():
    """Fayl yo'q bo'lsa {} sanaladi: natija toza o'rnatishning o'zi."""
    with workdir() as tmp:
        code, out, path = merge_files(tmp, None)
        got = load(path)
        return code == 0 and got == fresh() and "yo'q edi" in out


def case_ota_papka_yaratiladi():
    with workdir() as tmp:
        new = os.path.join(tmp, "yangi.json")
        write_json(new, fresh())
        old = os.path.join(tmp, "uy", ".claude", "settings.json")
        code, _ = run_main([old, new, "--root", GENIUS, "--yoz"])
        return code == 0 and load(old) == fresh()


def case_bom_oqiladi():
    """PowerShell 5.1 dagi eski o'rnatuvchi BOM yozgan: fayl baribir o'qiladi."""
    with workdir() as tmp:
        code, _, path = merge_files(tmp, {"model": "opus"}, bom=True)
        got = load(path)
        return code == 0 and got["model"] == "opus" and "hooks" in got


def case_begona_hook_bir_guruhda_qoladi():
    """Bir guruhdagi begona hook qoladi, o'z hooki yangisiga almashadi."""
    foreign = hook("node C:/mening/hook.js")
    existing = {"hooks": {"UserPromptSubmit": [{"hooks": [
        foreign, hook(own_cmd("suggest_sections.py"), timeout=5)]}]}}
    with workdir() as tmp:
        code, _, path = merge_files(tmp, existing)
        got = load(path)
        groups = got["hooks"]["UserPromptSubmit"]
        cmds = commands(got, "UserPromptSubmit")
        return (code == 0 and groups[0]["hooks"] == [foreign]
                and groups[1:] == fresh()["hooks"]["UserPromptSubmit"]
                and sum("suggest_sections.py" in c for c in cmds) == 1)


def case_windows_buyruq_katta_harf_bilan_oziniki():
    """Teskari slash va boshqa harf registri bilan yozilgan buyruq ham o'zniki."""
    upper = '"C:\\PYTHON312\\python.exe" "C:\\SRC\\Claude-Genius\\tools\\guard.py"'
    existing = {"hooks": {"PreToolUse": [
        {"matcher": "Read|Bash", "hooks": [hook(upper)]}]}}
    with workdir() as tmp:
        code, _, path = merge_files(tmp, existing, root="c:\\src\\claude-genius\\")
        got = load(path)
        cmds = commands(got, "PreToolUse")
        return (code == 0 and upper not in cmds
                and sum("guard.py" in c for c in cmds) == 1)


def case_bosh_qolgan_guruh_tushadi():
    """Faqat o'z hooki bor guruh bo'shaydi va tushadi; begona guruh qoladi."""
    foreign = {"matcher": "Write", "hooks": [hook("C:/boshqa/tools/lint.sh")]}
    existing = {"hooks": {
        "PreToolUse": [
            {"matcher": "Read|Bash", "hooks": [hook(own_cmd("guard.py"))]},
            foreign],
        "Stop": [{"hooks": [hook(own_cmd("usage.py") + " --saqlash")]}]}}
    with workdir() as tmp:
        code, out, path = merge_files(tmp, existing)
        got = load(path)
        pre = got["hooks"]["PreToolUse"]
        return (code == 0 and pre[0] == foreign
                and pre[1:] == fresh()["hooks"]["PreToolUse"]
                and "Stop" not in got["hooks"]
                and "2 hook almashdi, 1 qo'shildi" in out)


def case_ruxsat_birlashadi():
    """Begona ruxsat qoladi, o'ziniki almashadi, takror yo'q."""
    foreign = "Bash(git status:*)"
    other_clone = "Bash(bash %s-eski/tools/doc.sh:*)" % GENIUS
    stale = "Bash(C:\\Python311\\python.exe C:\\SRC\\claude-genius\\tools\\old.py:*)"
    existing = {"permissions": {
        "allow": [foreign, stale, fresh()["permissions"]["allow"][1], other_clone],
        "deny": ["Read(.env)"],
        "additionalDirectories": ["D:/boshqa", GENIUS]}}
    with workdir() as tmp:
        code, _, path = merge_files(tmp, existing)
        perm = load(path)["permissions"]
        allow = perm["allow"]
        return (code == 0
                and allow == [foreign, other_clone] + fresh()["permissions"]["allow"]
                and len(allow) == len(set(allow))
                and perm["deny"] == ["Read(.env)"]
                and perm["additionalDirectories"]
                == ["D:/boshqa"] + fresh()["permissions"]["additionalDirectories"])


def case_butun_klon_papkasi_toraydi():
    """Eski butun klon yozuvi va `<root>/` ostidagilar o'ziniki: ular
    tushadi va faqat docs bilan memory qoladi. Begona papka va boshqa klon
    (`<root>-eski`) qoladi. Avval birlashma edi va -Update dan keyin butun
    klon yozuvi joyida qolardi (XV-T-M1)."""
    existing = {"permissions": {"additionalDirectories": [
        "D:/boshqa", GENIUS, "C:\\SRC\\Claude-Genius\\tools",
        GENIUS + "-eski"]}}
    with workdir() as tmp:
        code, _, path = merge_files(tmp, existing)
        dirs = load(path)["permissions"]["additionalDirectories"]
        return (code == 0
                and dirs == ["D:/boshqa", GENIUS + "-eski",
                             GENIUS + "/docs", GENIUS + "/memory"])


def case_foydalanuvchi_deny_va_ask_saqlanadi():
    """Foydalanuvchining deny va ask qoidasi qoladi, o'rnatuvchinikisi
    qo'shiladi. Avval foydalanuvchida shu nomli ro'yxat bo'lsa yangisi jim
    tushib qolardi."""
    existing = {"permissions": {"deny": ["Read(~/.foo)"], "ask": ["Bash(git push:*)"]}}
    new = fresh()
    new["permissions"]["deny"] = ["Read(~/.ssh/**)"]
    new["permissions"]["ask"] = ["Bash(git push:*)", "Bash(rm:*)"]
    with workdir() as tmp:
        old = os.path.join(tmp, "settings.json")
        yangi = os.path.join(tmp, "yangi.json")
        write_json(old, existing)
        write_json(yangi, new)
        code, _ = run_main([old, yangi, "--root", GENIUS, "--yoz"])
        perm = load(old)["permissions"]
        return (code == 0
                and perm["deny"] == ["Read(~/.foo)", "Read(~/.ssh/**)"]
                and perm["ask"] == ["Bash(git push:*)", "Bash(rm:*)"])


def case_oz_ask_deny_qoidasi_almashadi():
    """Root bor ask va deny qoidasi o'ziniki: eskisi tushadi, yangisi
    keladi. Begona qoida joyida qoladi."""
    py = WIN_PY.replace("\\", "/")
    stale = "Bash(%s %s/tools/guruh.py tozala:*)" % (py, GENIUS)
    fresh_rule = "Bash(%s %s/tools/budget.py --tiklash:*)" % (py, GENIUS)
    existing = {"permissions": {"ask": ["Bash(rm:*)", stale],
                                "deny": ["Edit(%s/tools/**)" % GENIUS]}}
    new = fresh()
    new["permissions"]["ask"] = [fresh_rule]
    with workdir() as tmp:
        old = os.path.join(tmp, "settings.json")
        yangi = os.path.join(tmp, "yangi.json")
        write_json(old, existing)
        write_json(yangi, new)
        code, out = run_main([old, yangi, "--root", GENIUS, "--yoz"])
        perm = load(old)["permissions"]
        return (code == 0 and perm["ask"] == ["Bash(rm:*)", fresh_rule]
                and perm["deny"] == []
                and "ruxsat olib tashlandi" not in out)


def case_env_birlashadi():
    existing = {"env": {"GENIUS_PYTHON": "python3", "MENING": "1"},
                "model": "opus", "hooks": {}}
    with workdir() as tmp:
        code, _, path = merge_files(tmp, existing)
        got = load(path)
        return (code == 0
                and got["env"] == {"GENIUS_PYTHON": WIN_PY.replace("\\", "/"),
                                   "MENING": "1"}
                and got["model"] == "opus"
                and list(got)[:3] == ["env", "model", "hooks"]
                and "bashOutputMaxChars" not in got)


def case_eskirgan_kalit_olinadi():
    """O'rnatuvchi yozgan bashOutputMaxChars=12000 olib tashlanadi.

    Kalit Claude Code sozlama sxemasida yo'q (142 kalit ichida yo'q,
    additionalProperties true, ya'ni jim e'tiborsiz qoladi).
    """
    existing = {"bashOutputMaxChars": 12000, "model": "opus", "hooks": {}}
    with workdir() as tmp:
        code, out, path = merge_files(tmp, existing)
        got = load(path)
        return (code == 0 and "bashOutputMaxChars" not in got
                and got["model"] == "opus"
                and "bashOutputMaxChars olib tashlandi" in out)


def case_foydalanuvchi_qiymati_qoladi():
    """Boshqa qiymat foydalanuvchiniki: tegilmaydi."""
    existing = {"bashOutputMaxChars": 8000, "hooks": {}}
    with workdir() as tmp:
        code, out, path = merge_files(tmp, existing)
        got = load(path)
        return (code == 0 and got.get("bashOutputMaxChars") == 8000
                and "bashOutputMaxChars olib tashlandi" not in out)


def case_quruq_yurish_yozmaydi():
    """--yoz siz fayl bayt-bayt o'zgarmaydi, chiqishda xulosa bor."""
    existing = {"hooks": {"Stop": [{"hooks": [hook(own_cmd("usage.py"))]}]}}
    with workdir() as tmp:
        old = os.path.join(tmp, "settings.json")
        write_json(old, existing, bom=True)
        before = read_bytes(old)
        code, out, _ = merge_files(tmp, existing, bom=True, yoz=False)
        return (code == 0 and read_bytes(old) == before
                and "yozilmadi" in out and "hook almashdi" in out
                and len(os.listdir(tmp)) == 2)


def case_buzuq_json_1():
    """Buzuq JSON yoki obyekt emas: 1 qaytadi, fayl tegilmaydi."""
    with workdir() as tmp:
        old = os.path.join(tmp, "settings.json")
        new = os.path.join(tmp, "yangi.json")
        write_json(new, fresh())
        results = []
        for raw in (b'{"hooks": {', b'[1, 2]'):
            with open(old, "wb") as handle:
                handle.write(raw)
            code, out = run_main([old, new, "--root", GENIUS, "--yoz"])
            results.append(code == 1 and read_bytes(old) == raw and out.strip())
        return all(results) and sorted(os.listdir(tmp)) == ["settings.json", "yangi.json"]


def case_bomsiz_yoziladi_va_ikkinchi_yurish_ozgartirmaydi():
    foreign = hook("node C:/mening/hook.js")
    existing = {"hooks": {"UserPromptSubmit": [{"hooks": [
        foreign, hook(own_cmd("budget.py"))]}]},
        "permissions": {"allow": ["Bash(git status:*)"]}}
    with workdir() as tmp:
        code1, _, path = merge_files(tmp, existing, bom=True)
        first = read_bytes(path)
        new = os.path.join(tmp, "yangi.json")
        code2, out2 = run_main([path, new, "--root", GENIUS, "--yoz"])
        second = read_bytes(path)
        return (code1 == 0 and code2 == 0 and not first.startswith(b"\xef\xbb\xbf")
                and first == second
                and json.loads(first.decode("utf-8")) is not None
                and "0 qo'shildi" in out2
                and sorted(os.listdir(tmp)) == ["settings.json", "yangi.json"])


def case_haqiqiy_ps1_yangi_hooklari_oziniki():
    """ps1 yasaydigan har hook buyrug'i o'zniki deb taniladi: aks holda
    -Update har safar hookni ikkilantiradi."""
    data = fresh()
    root = M.norm_root(GENIUS)
    hooks = [h for groups in data["hooks"].values() for g in groups
             for h in g["hooks"]]
    rules = data["permissions"]["allow"]
    return (all(M.is_own_hook(h, root) for h in hooks)
            and all(M.is_own_rule(r, root) for r in rules)
            and not M.is_own_rule("Bash(git status:*)", root))


CASES = [
    ("mavjud fayl yo'q: yangi sozlamaning o'zi", case_mavjud_fayl_yoq),
    ("ota papka yo'q bo'lsa yaratiladi", case_ota_papka_yaratiladi),
    ("BOM li fayl o'qiladi", case_bom_oqiladi),
    ("bir guruhdagi begona hook qoladi", case_begona_hook_bir_guruhda_qoladi),
    ("teskari slash va katta harfli buyruq o'zniki",
     case_windows_buyruq_katta_harf_bilan_oziniki),
    ("bo'shab qolgan guruh tushadi", case_bosh_qolgan_guruh_tushadi),
    ("ruxsatlar takrorsiz birlashadi", case_ruxsat_birlashadi),
    ("butun klon papkasi docs va memory ga almashadi",
     case_butun_klon_papkasi_toraydi),
    ("foydalanuvchi deny va ask qoidasi saqlanadi, yangisi qo'shiladi",
     case_foydalanuvchi_deny_va_ask_saqlanadi),
    ("o'z ask va deny qoidasi almashadi", case_oz_ask_deny_qoidasi_almashadi),
    ("env kalitlari birlashadi", case_env_birlashadi),
    ("eskirgan bashOutputMaxChars=12000 olinadi", case_eskirgan_kalit_olinadi),
    ("foydalanuvchining 8000 qiymati qoladi", case_foydalanuvchi_qiymati_qoladi),
    ("quruq yurish faylga tegmaydi", case_quruq_yurish_yozmaydi),
    ("buzuq JSON 1 qaytaradi, fayl tegilmaydi", case_buzuq_json_1),
    ("BOM siz yoziladi, ikkinchi yurish o'zgartirmaydi",
     case_bomsiz_yoziladi_va_ikkinchi_yurish_ozgartirmaydi),
    ("ps1 hook va ruxsatlari o'zniki deb taniladi",
     case_haqiqiy_ps1_yangi_hooklari_oziniki),
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
