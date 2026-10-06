#!/usr/bin/env python3
"""install/restore_backup.py uchun sinovlar.

    python3 tools/test_restore_backup.py

Asosiy shart: HOZIR turgan narsa ustidan yozilmaydi. Yangi o'rnatish
qo'shuvchi, shuning uchun ~/.claude dagi har fayl foydalanuvchining joriy
holati; zaxira esa faqat eski o'rnatuvchi o'chirgan bo'shliqni to'ldiradi.
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
TOOL = os.path.join(INSTALL, "restore_backup.py")
sys.path.insert(0, INSTALL)
import restore_backup as R  # noqa: E402


@contextlib.contextmanager
def workdir():
    tmp = tempfile.mkdtemp(prefix="restore_")
    try:
        yield (os.path.join(tmp, "zaxira"), os.path.join(tmp, "claude"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def write(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    io.open(path, "w", encoding="utf-8").write(text)


def write_json(path, data):
    write(path, json.dumps(data, indent=2, ensure_ascii=False))


def unit(backup, name):
    """Zaxiradagi birlik yo'li: `.claude--<nom>`."""
    return os.path.join(backup, ".claude%s%s" % (R.SEP, name))


def run(backup, claude, write_mode=True):
    args = [sys.executable, TOOL, backup, "--claude", claude]
    if write_mode:
        args.append("--yoz")
    proc = subprocess.run(args, capture_output=True, text=True)
    return proc.returncode, proc.stdout


def load(path):
    with io.open(path, encoding="utf-8-sig") as handle:
        return json.load(handle)


def case_yoq_birliklar_qaytadi():
    with workdir() as (backup, claude):
        write(unit(backup, "CLAUDE.md"), "eski qoidalar")
        write(os.path.join(unit(backup, "commands"), "a.md"), "buyruq")
        write(os.path.join(unit(backup, "rules"), "r.md"), "qoida")
        os.makedirs(claude)
        code, out = run(backup, claude)
        return (code == 0
                and io.open(os.path.join(claude, "CLAUDE.md"),
                            encoding="utf-8").read() == "eski qoidalar"
                and os.path.isfile(os.path.join(claude, "commands", "a.md"))
                and os.path.isfile(os.path.join(claude, "rules", "r.md"))
                and "3 birlik qaytarildi" in out)


def case_hozirgi_ustidan_yozilmaydi():
    with workdir() as (backup, claude):
        write(unit(backup, "CLAUDE.md"), "eski")
        write(os.path.join(claude, "CLAUDE.md"), "yangi")
        code, out = run(backup, claude)
        return (code == 0
                and io.open(os.path.join(claude, "CLAUDE.md"),
                            encoding="utf-8").read() == "yangi"
                and "hozir bor" in out)


def case_skills_ichida_faqat_yoq_bolalar():
    with workdir() as (backup, claude):
        src = unit(backup, "skills")
        write(os.path.join(src, "eski-skill", "SKILL.md"), "eski")
        write(os.path.join(src, "bor-skill", "SKILL.md"), "zaxiradagi")
        write(os.path.join(src, "manguberdi", "SKILL.md"), "eski manguberdi")
        write(os.path.join(claude, "skills", "bor-skill", "SKILL.md"), "hozirgi")
        write(os.path.join(claude, "skills", "manguberdi", "SKILL.md"), "yangi")
        code, _ = run(backup, claude)
        read = lambda *p: io.open(os.path.join(claude, "skills", *p),
                                  encoding="utf-8").read()
        return (code == 0
                and read("eski-skill", "SKILL.md") == "eski"
                and read("bor-skill", "SKILL.md") == "hozirgi"
                and read("manguberdi", "SKILL.md") == "yangi")


def case_agents_oz_aktyorlari_tashlanadi():
    with workdir() as (backup, claude):
        src = unit(backup, "agents")
        write(os.path.join(src, "review.md"), "eski review")
        write(os.path.join(src, "mening.md"), "mening aktyorim")
        os.makedirs(os.path.join(claude, "agents"))
        code, _ = run(backup, claude)
        agents = os.path.join(claude, "agents")
        return (code == 0
                and os.path.isfile(os.path.join(agents, "mening.md"))
                and not os.path.exists(os.path.join(agents, "review.md")))


def case_sozlama_birlashadi_hozirgisi_ustun():
    """Zaxiradagi foydalanuvchi yozuvlari qaytadi, klon yozuvlari ustun."""
    with workdir() as (backup, claude):
        write_json(unit(backup, "settings.json"), {
            "model": "eski-model",
            "mening": "qiymat",
            "env": {"MENING": "1", "GENIUS_PYTHON": "eski-py"},
            "permissions": {"allow": ["Bash(npm test:*)"],
                            "deny": ["Bash(rm:*)"]},
            "hooks": {"SessionStart": [{"hooks": [{"command": "mening.py"}]}],
                      "Stop": [{"hooks": [{"command": "eski-usage.py"}]}]},
        })
        write_json(os.path.join(claude, "settings.json"), {
            "model": "yangi-model",
            "env": {"GENIUS_PYTHON": "yangi-py"},
            "permissions": {"allow": ["Bash(py budget.py:*)"]},
            "hooks": {"Stop": [{"hooks": [{"command": "yangi-usage.py"}]}]},
        })
        code, out = run(backup, claude)
        got = load(os.path.join(claude, "settings.json"))
        stop = got["hooks"]["Stop"][0]["hooks"][0]["command"]
        return (code == 0
                and got["model"] == "yangi-model"            # hozirgisi ustun
                and got["mening"] == "qiymat"                # zaxiradan qaytdi
                and got["env"] == {"MENING": "1", "GENIUS_PYTHON": "yangi-py"}
                and stop == "yangi-usage.py"                 # klon hooki ustun
                and "SessionStart" in got["hooks"]           # begona hodisa qaytdi
                and got["permissions"]["allow"] == ["Bash(py budget.py:*)",
                                                    "Bash(npm test:*)"]
                and got["permissions"]["deny"] == ["Bash(rm:*)"]
                and "birlashtiriladi: settings.json" in out)


def case_sozlama_hozir_yoq():
    with workdir() as (backup, claude):
        write_json(unit(backup, "settings.json"), {"model": "eski"})
        os.makedirs(claude)
        code, _ = run(backup, claude)
        return code == 0 and load(os.path.join(claude, "settings.json"))["model"] == "eski"


def case_quruq_yurish_yozmaydi():
    with workdir() as (backup, claude):
        write(unit(backup, "CLAUDE.md"), "eski")
        os.makedirs(claude)
        code, out = run(backup, claude, write_mode=False)
        return (code == 0 and not os.path.exists(os.path.join(claude, "CLAUDE.md"))
                and "quruq yurish" in out)


def case_zaxira_yoq():
    with workdir() as (backup, claude):
        code, out = run(backup, claude)
        return code == 1 and "topilmadi" in out


def case_qaytariladigan_narsa_yoq():
    with workdir() as (backup, claude):
        os.makedirs(backup)
        os.makedirs(claude)
        code, out = run(backup, claude)
        return code == 0 and "narsa yo'q" in out


def case_ajratgichsiz_nom_tashlanadi():
    """Zaxirada `--` siz fayl bo'lsa (qo'lda qo'yilgan) e'tiborsiz qoladi."""
    with workdir() as (backup, claude):
        write(os.path.join(backup, "izoh.txt"), "qo'lda")
        write(unit(backup, "CLAUDE.md"), "eski")
        os.makedirs(claude)
        code, _ = run(backup, claude)
        return (code == 0 and not os.path.exists(os.path.join(claude, "izoh.txt"))
                and os.path.isfile(os.path.join(claude, "CLAUDE.md")))


def case_ota_nomida_ajratgich():
    """`my--repo--skills`: oxirgi ajratgich olinadi."""
    with workdir() as (backup, claude):
        src = os.path.join(backup, "my--repo--skills")
        write(os.path.join(src, "x", "SKILL.md"), "x")
        os.makedirs(claude)
        code, _ = run(backup, claude)
        return code == 0 and os.path.isfile(
            os.path.join(claude, "skills", "x", "SKILL.md"))


def case_buzuq_sozlama_1_qaytaradi():
    with workdir() as (backup, claude):
        write(unit(backup, "settings.json"), "{buzuq")
        os.makedirs(claude)
        code, out = run(backup, claude)
        return code == 1 and "buzuq" in out.lower()


CASES = [
    ("yo'q birliklar qaytadi", case_yoq_birliklar_qaytadi),
    ("hozirgi fayl ustidan yozilmaydi", case_hozirgi_ustidan_yozilmaydi),
    ("skills: faqat yo'q bolalar, manguberdi tashlanadi",
     case_skills_ichida_faqat_yoq_bolalar),
    ("agents: olti aktyor tashlanadi", case_agents_oz_aktyorlari_tashlanadi),
    ("settings.json birlashadi, hozirgisi ustun",
     case_sozlama_birlashadi_hozirgisi_ustun),
    ("settings.json hozir yo'q bo'lsa qaytadi", case_sozlama_hozir_yoq),
    ("quruq yurish yozmaydi", case_quruq_yurish_yozmaydi),
    ("zaxira papkasi yo'q: 1", case_zaxira_yoq),
    ("qaytariladigan narsa yo'q: 0", case_qaytariladigan_narsa_yoq),
    ("ajratgichsiz nom e'tiborsiz", case_ajratgichsiz_nom_tashlanadi),
    ("ota nomida ajratgich bo'lsa ham", case_ota_nomida_ajratgich),
    ("buzuq settings.json: 1", case_buzuq_sozlama_1_qaytaradi),
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
