#!/usr/bin/env python3
"""budget.py uchun sinovlar.

    python3 tools/test_budget.py

Eng muhimi oxirgi ikkitasi. Hisoblagich ishlashi yetarli emas: u
sanamasligi kerak bo'lgan narsani sanab qo'ysa (o'qish asbobini yoki
boshqa hook chaqiruvini), zanjir o'rtasida to'xtaydi va hisoblagich
o'chiriladi. Shuning uchun qidiruv, tahlil va Task bo'lmagan asbob
erkin o'tishi tekshiriladi.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "budget.py")


def run(*args):
    proc = subprocess.run([sys.executable, TOOL] + list(args),
                          capture_output=True, text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


def hook(tool_name, actor):
    payload = json.dumps({"tool_name": tool_name,
                          "tool_input": {"subagent_type": actor}})
    proc = subprocess.run([sys.executable, TOOL], input=payload,
                          capture_output=True, text=True, cwd=ROOT)
    out = proc.stdout.strip()
    if not out:
        return "allow"
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"]


def fresh(name="sinov"):
    run("--yangi-vazifa", name)


def case_ikki_marta(_):
    fresh()
    first, _ = run("arxitektor")
    second, _ = run("arxitektor")
    return first == 0 and second == 0


def case_uchinchi_tosiladi(_):
    fresh()
    run("arxitektor")
    run("arxitektor")
    code, out = run("arxitektor")
    return code == 1 and "budjet tugadi" in out


def case_sabab_aytiladi(_):
    fresh()
    run("review")
    run("review")
    _, out = run("review")
    # To'siq sababni so'rashi kerak, shunchaki "yo'q" demasligi.
    return "rules_for.py" in out and "qabul mezoni" in out


def case_aktyorlar_mustaqil(_):
    fresh()
    run("arxitektor")
    run("arxitektor")
    code, _ = run("test-muhandis")
    return code == 0


def case_yangi_vazifa_nolga(_):
    fresh()
    run("arxitektor")
    run("arxitektor")
    fresh("boshqa vazifa")
    code, _ = run("arxitektor")
    return code == 0


def case_tiklash(_):
    fresh()
    run("arxitektor")
    run("arxitektor")
    run("--tiklash", "arxitektor")
    code, _ = run("arxitektor")
    return code == 0


def case_holat_jadvali(_):
    fresh()
    run("arxitektor")
    _, out = run("--holat")
    return "arxitektor" in out and "1/2" in out and "rejalashtiruvchi" in out


def case_hook_tosadi(_):
    fresh()
    return (hook("Task", "arxitektor") == "allow"
            and hook("Task", "arxitektor") == "allow"
            and hook("Task", "arxitektor") == "deny")


def case_hook_agent_nomi(_):
    """Harness Task deb ham, Agent deb ham ataydi: ikkisi bir hisob."""
    fresh()
    return (hook("Agent", "review") == "allow"
            and hook("Task", "review") == "allow"
            and hook("Agent", "review") == "deny")


def case_oqish_asbobi_erkin(_):
    """qidiruv va tahlil zanjir qadami emas, cheklanmaydi."""
    fresh()
    return all(hook("Task", "qidiruv") == "allow" for _ in range(4)) and \
        all(hook("Task", "tahlil") == "allow" for _ in range(4))


def case_boshqa_asbob_tegilmaydi(_):
    fresh()
    run("arxitektor")
    run("arxitektor")
    # Read chaqiruvi hisobga olinmaydi va to'silmaydi.
    before = run("--holat")[1]
    ok = hook("Read", "") == "allow"
    return ok and run("--holat")[1] == before


def case_notanish_aktyor(_):
    fresh()
    code, out = run("yoq-aktyor")
    return code == 0 and "sanalmaydi" in out


def case_buzuq_json(_):
    proc = subprocess.run([sys.executable, TOOL], input="not json",
                          capture_output=True, text=True, cwd=ROOT)
    return proc.returncode == 0 and proc.stdout.strip() == ""


CASES = [
    ("ikki chaqiruv o'tadi", case_ikki_marta),
    ("uchinchisi to'siladi", case_uchinchi_tosiladi),
    ("to'siq sababni so'raydi", case_sabab_aytiladi),
    ("aktyorlar alohida sanaladi", case_aktyorlar_mustaqil),
    ("yangi vazifa nolga tushiradi", case_yangi_vazifa_nolga),
    ("--tiklash bitta qadam qaytaradi", case_tiklash),
    ("--holat jadval beradi", case_holat_jadvali),
    ("hook uchinchisini to'sadi", case_hook_tosadi),
    ("Task va Agent bir hisob", case_hook_agent_nomi),
    ("qidiruv va tahlil erkin", case_oqish_asbobi_erkin),
    ("boshqa asbob tegilmaydi", case_boshqa_asbob_tegilmaydi),
    ("notanish aktyor erkin", case_notanish_aktyor),
    ("buzuq JSON to'smaydi", case_buzuq_json),
]


def main():
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn(None))
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    run("--yangi-vazifa", "")      # sinovdan keyin toza holat
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
