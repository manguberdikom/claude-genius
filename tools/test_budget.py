#!/usr/bin/env python3
"""budget.py uchun sinovlar.

    python3 tools/test_budget.py

Hisoblagich ishlashi yetarli emas: u sanamasligi kerak bo'lgan narsani
sanab qo'ysa (o'qish asbobini yoki boshqa hook chaqiruvini), zanjir
o'rtasida to'xtaydi va hisoblagich o'chiriladi. Shuning uchun qidiruv,
tahlil va Task bo'lmagan asbob erkin o'tishi tekshiriladi. Parallel
Agent chaqiruvlari va bir nechta sessiya ham alohida sinaladi: hisob
yo'qolsa chegara jim aylanib o'tiladi.

Sinov jonli budjetga tegmaydi: holat vaqtinchalik papkada
(`GENIUS_STATE_DIR`), sessiya nomi soxta.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "budget.py")
STATE = tempfile.mkdtemp(prefix="budget_")
LOG = os.path.join(STATE, "budget.json")
SESSION = "sinov"


def env_for(session=SESSION):
    env = dict(os.environ, GENIUS_STATE_DIR=STATE)
    env.pop("CLAUDE_CODE_SESSION_ID", None)
    if session is not None:
        env["CLAUDE_CODE_SESSION_ID"] = session
    return env


def run(*args, session=SESSION, cwd=None):
    proc = subprocess.run([sys.executable, TOOL] + list(args),
                          capture_output=True, text=True,
                          cwd=cwd or STATE, env=env_for(session))
    return proc.returncode, proc.stdout


def payload(tool_name, actor, session=SESSION, cwd=None, call_id=None):
    data = {"hook_event_name": "PreToolUse", "tool_name": tool_name,
            "tool_input": {"subagent_type": actor}, "session_id": session}
    if cwd:
        data["cwd"] = cwd
    if call_id:
        data["tool_use_id"] = call_id
    return json.dumps(data)


def decision(out):
    out = out.strip()
    if not out:
        return "allow"
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"]


def hook(tool_name, actor, session=SESSION, cwd=None, call_id=None):
    proc = subprocess.run([sys.executable, TOOL],
                          input=payload(tool_name, actor, session, cwd, call_id),
                          capture_output=True, text=True, cwd=STATE,
                          env=env_for())
    return decision(proc.stdout)


def parallel(payloads):
    """Hamma jarayon stdin ni kutib turganda payload bir vaqtda beriladi.

    Kutishsiz jarayonlar ishga tushish vaqti bilan navbatlashib qoladi va
    qulfsiz kod ham sinovdan o'tib ketadi.
    """
    procs = [subprocess.Popen([sys.executable, TOOL], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                              text=True, cwd=STATE, env=env_for())
             for _ in payloads]
    time.sleep(0.3)
    for proc, data in zip(procs, payloads):
        proc.stdin.write(data)
        proc.stdin.close()
    out = []
    for proc in procs:
        text = proc.stdout.read()
        proc.stdout.close()
        proc.wait()
        out.append(decision(text))
    return out


def state():
    with open(LOG, encoding="utf-8") as handle:
        return json.load(handle)


def write_state(data):
    with open(LOG, "w", encoding="utf-8") as handle:
        json.dump(data, handle)


def clean():
    if os.path.exists(LOG):
        os.remove(LOG)


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
                          capture_output=True, text=True, cwd=STATE,
                          env=env_for())
    return proc.returncode == 0 and proc.stdout.strip() == ""


def case_eskirgan_nolga(_):
    """Vazifa belgilanmasa hisob MAX_AGE dan keyin o'zi nolga tushadi."""
    old = time.time() - 7 * 3600
    write_state({"sessions": {SESSION: {
        "task": "eski", "started": old, "seen": old,
        "calls": {"arxitektor": 2}}}})
    return run("arxitektor")[0] == 0


def case_eski_shakl_toza(_):
    """Sessiyasiz eski tekis fayl yangi sessiyani to'smaydi."""
    write_state({"task": "x", "started": time.time(),
                 "calls": {"arxitektor": 2}})
    return run("arxitektor")[0] == 0


def case_ikki_sessiya_tosmaydi(_):
    """Parallel sessiya yoki boshqa proyekt hisobi aralashmaydi."""
    clean()
    return (hook("Agent", "arxitektor", "s-a") == "allow"
            and hook("Agent", "arxitektor", "s-a") == "allow"
            and hook("Agent", "arxitektor", "s-b") == "allow"
            and hook("Agent", "arxitektor", "s-a") == "deny")


def case_yangi_vazifa_boshqasiga_tegmaydi(_):
    clean()
    hook("Agent", "arxitektor", "s-a")
    hook("Agent", "arxitektor", "s-a")
    run("--yangi-vazifa", "B", session="s-b")
    return hook("Agent", "arxitektor", "s-a") == "deny"


def case_envsiz_cli_oz_proyektini_oladi(_):
    """CLAUDE_CODE_SESSION_ID yo'q CLI shu papkadagi sessiyani tanlaydi."""
    clean()
    proj_a = os.path.join(STATE, "projA")
    proj_b = os.path.join(STATE, "projB")
    os.makedirs(os.path.join(proj_a, "src"), exist_ok=True)
    os.makedirs(proj_b, exist_ok=True)
    hook("Agent", "arxitektor", "s-p", cwd=proj_a)
    hook("Agent", "arxitektor", "s-q", cwd=proj_b)
    hook("Agent", "arxitektor", "s-q", cwd=proj_b)
    _, in_a = run("--holat", session=None, cwd=os.path.join(proj_a, "src"))
    _, elsewhere = run("--holat", session=None, cwd=STATE)
    return ("Sessiya: s-p" in in_a and "1/2" in in_a
            and "Sessiya: s-q" in elsewhere and "2/2" in elsewhere)


def case_parallel_hisob_yoqolmaydi(_):
    """Bir xabardagi 6 ta Agent: har turda aynan 2 o'tadi, 4 to'siladi."""
    for _ in range(5):
        fresh()
        got = parallel([payload("Agent", "arxitektor")] * 6)
        if got.count("deny") != 4:
            return False
    return True


def case_parallel_aktyorlar_saqlanadi(_):
    """4 xil aktyor parallel: fayl buzilmaydi, har biri 1 ga teng."""
    fresh()
    parallel([payload("Agent", actor) for actor in
              ("rejalashtiruvchi", "arxitektor", "test-muhandis", "review")])
    calls = state()["sessions"][SESSION]["calls"]
    return calls == {"rejalashtiruvchi": 1, "arxitektor": 1,
                     "test-muhandis": 1, "review": 1}


def case_bir_chaqiruv_bir_marta(_):
    """Repo va global hook birga yursa ham bitta tool_use_id bir marta."""
    fresh()
    first = hook("Agent", "arxitektor", call_id="toolu_1")
    again = hook("Agent", "arxitektor", call_id="toolu_1")
    second = hook("Agent", "arxitektor", call_id="toolu_2")
    third = hook("Agent", "arxitektor", call_id="toolu_3")
    return (first, again, second, third) == ("allow", "allow", "allow", "deny")


def case_yangi_sorov_nolga(_):
    """UserPromptSubmit payloadi shu sessiyani jim nolga tushiradi."""
    fresh()
    hook("Agent", "arxitektor")
    hook("Agent", "arxitektor")
    hook("Agent", "arxitektor", "boshqa")
    proc = subprocess.run(
        [sys.executable, TOOL], capture_output=True, text=True, cwd=STATE,
        env=env_for(), input=json.dumps({"hook_event_name": "UserPromptSubmit",
                                         "session_id": SESSION, "prompt": "x"}))
    calls = state()["sessions"]
    return (proc.returncode == 0 and proc.stdout == ""
            and calls[SESSION]["calls"] == {}
            and calls["boshqa"]["calls"] == {"arxitektor": 1})


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
    ("eskirgan hisob nolga tushadi", case_eskirgan_nolga),
    ("eski tekis fayl to'smaydi", case_eski_shakl_toza),
    ("ikki sessiya bir-birini to'smaydi", case_ikki_sessiya_tosmaydi),
    ("--yangi-vazifa boshqa sessiyaga tegmaydi",
     case_yangi_vazifa_boshqasiga_tegmaydi),
    ("env siz CLI o'z proyektini oladi", case_envsiz_cli_oz_proyektini_oladi),
    ("parallel chaqiruvda hisob yo'qolmaydi", case_parallel_hisob_yoqolmaydi),
    ("parallel aktyorlar saqlanadi", case_parallel_aktyorlar_saqlanadi),
    ("bitta chaqiruv bir marta sanaladi", case_bir_chaqiruv_bir_marta),
    ("yangi so'rov hisobni nolga tushiradi", case_yangi_sorov_nolga),
]


def main():
    failures = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(None))
            except Exception as exc:
                ok, name = False, "%s (%s)" % (name, exc)
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", name))
    finally:
        shutil.rmtree(STATE, ignore_errors=True)
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
