#!/usr/bin/env python3
"""budget.py uchun sinovlar.

    python3 tools/test_budget.py [-k matn] [--vaqt [ms]]

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

# Hook faqat Java proyektida yoki klonning o'zida ishlaydi
# (hookio.active). Sinovlar vaqtinchalik papkada yuradi, shu yerda esa
# tekshirilayotgan narsa gating emas: ildiz klonga qo'yiladi. Gating ning
# o'z sinovlari tools/test_hookio.py da.
ROOT = os.path.dirname(HERE)
os.environ["CLAUDE_PROJECT_DIR"] = ROOT
# budget import qilinishidan OLDIN: modul holat papkasini importda oladi,
# parallel holatdagi jarayonlar ham shu papkani meros oladi.
os.environ["GENIUS_STATE_DIR"] = STATE
sys.path.insert(0, HERE)
import budget  # noqa: E402
import testkit  # noqa: E402

budget.STATE_DIR, budget.LOG = STATE, LOG

# Parallel holatdagi jarayon: import tugagach "R" qatorini chiqaradi, keyin
# stdin ni kutadi. Ota jarayon hamma "R" ni o'qigach payloadlarni beradi.
READY = ("import sys; sys.path.insert(0, %r); import budget; "
         "print('R', flush=True); sys.exit(budget.main())" % HERE)


def env_for(session=SESSION):
    env = dict(os.environ, GENIUS_STATE_DIR=STATE)
    env.pop("CLAUDE_CODE_SESSION_ID", None)
    if session is not None:
        env["CLAUDE_CODE_SESSION_ID"] = session
    return env


def call(args=(), stdin="", session=SESSION, cwd=None):
    """budget.main() jarayon ichida. session None bo'lsa muhitda sessiya yo'q."""
    return testkit.call_main(budget.main, stdin, argv=["budget.py"] + list(args),
                             cwd=cwd or STATE,
                             env={"CLAUDE_CODE_SESSION_ID": session})


def run(*args, session=SESSION, cwd=None):
    res = call(args, session=session, cwd=cwd)
    return res.returncode, res.stdout


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
    return decision(call(stdin=payload(tool_name, actor, session, cwd, call_id)).stdout)


def parallel(payloads):
    """Hamma jarayon stdin ni kutib turganda payload bir vaqtda beriladi.

    Kutishsiz jarayonlar ishga tushish vaqti bilan navbatlashib qoladi va
    qulfsiz kod ham sinovdan o'tib ketadi. Tayyorlik qat'iy kutish bilan
    emas, har jarayonning "R" qatori bilan aniqlanadi: sekin runnerda ham
    payload hamma jarayon importni tugatgandan keyin beriladi.
    """
    procs = [subprocess.Popen([sys.executable, "-c", READY], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                              text=True, cwd=STATE, env=env_for())
             for _ in payloads]
    for proc in procs:
        if proc.stdout.readline().strip() != "R":
            raise RuntimeError("budget jarayoni tayyor emas")
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


def hook_group(actor, group, call_id=None):
    """Aktyor prompti `guruh: <id>` qatori bilan, orkestrator yozgandek."""
    data = {"hook_event_name": "PreToolUse", "tool_name": "Agent",
            "tool_input": {"subagent_type": actor,
                           "prompt": "guruh: %s\nVazifa: ..." % group},
            "session_id": SESSION}
    if call_id:
        data["tool_use_id"] = call_id
    return decision(call(stdin=json.dumps(data)).stdout)


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
    first, _ = run("dasturchi")
    second, _ = run("dasturchi")
    return first == 0 and second == 0


def case_uchinchi_tosiladi(_):
    fresh()
    run("dasturchi")
    run("dasturchi")
    code, out = run("dasturchi")
    return code == 1 and "budjet tugadi" in out


def case_sabab_aytiladi(_):
    fresh()
    run("review")
    run("review")
    _, out = run("review")
    # To'siq sababni so'rashi kerak, shunchaki "yo'q" demasligi. Budjetni
    # o'zi nolga tushirish yo'li aytilmaydi: aks holda to'siq aylanib o'tiladi.
    return ("rules_for.py" in out and "qabul mezoni" in out
            and "--yangi-vazifa" not in out)


def case_tosiq_buyrugi_klonga_mos(_):
    """Klon ichida buyruq nisbiy, boshqa proyektda mutlaq yo'l bilan."""
    fresh()
    for _ in range(3):
        _, inside = run("review", cwd=os.path.dirname(HERE))
    fresh()
    for _ in range(3):
        _, outside = run("review")
    full = os.path.join(HERE, "rules_for.py").replace("\\", "/")
    return ("-> python3 tools/rules_for.py" in inside
            and full in outside and "-> python3 tools/" not in outside)


def case_aktyorlar_mustaqil(_):
    fresh()
    run("dasturchi")
    run("dasturchi")
    code, _ = run("test-muhandis")
    return code == 0


def case_yangi_vazifa_nolga(_):
    fresh()
    run("dasturchi")
    run("dasturchi")
    fresh("boshqa vazifa")
    code, _ = run("dasturchi")
    return code == 0


def case_tiklash(_):
    fresh()
    run("dasturchi")
    run("dasturchi")
    run("--tiklash", "dasturchi")
    code, _ = run("dasturchi")
    return code == 0


def case_holat_jadvali(_):
    fresh()
    run("dasturchi")
    _, out = run("--holat")
    return "dasturchi" in out and "1/2" in out and "rejalashtiruvchi" in out


def case_hook_tosadi(_):
    fresh()
    return (hook("Task", "dasturchi") == "allow"
            and hook("Task", "dasturchi") == "allow"
            and hook("Task", "dasturchi") == "deny")


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
    run("dasturchi")
    run("dasturchi")
    # Read chaqiruvi hisobga olinmaydi va to'silmaydi.
    before = run("--holat")[1]
    ok = hook("Read", "") == "allow"
    return ok and run("--holat")[1] == before


def case_notanish_aktyor(_):
    fresh()
    code, out = run("yoq-aktyor")
    return code == 0 and "sanalmaydi" in out


def case_buzuq_json(_):
    """E2E: alohida jarayon, chiqish kodi haqiqiy sys.exit dan."""
    proc = subprocess.run([sys.executable, TOOL], input="not json",
                          capture_output=True, text=True, cwd=STATE,
                          env=env_for())
    return proc.returncode == 0 and proc.stdout.strip() == ""


def case_eskirgan_nolga(_):
    """Vazifa belgilanmasa hisob MAX_AGE dan keyin o'zi nolga tushadi."""
    old = time.time() - 7 * 3600
    write_state({"sessions": {SESSION: {
        "task": "eski", "started": old, "seen": old,
        "calls": {"dasturchi": 2}}}})
    return run("dasturchi")[0] == 0


def case_eski_shakl_toza(_):
    """Sessiyasiz eski tekis fayl yangi sessiyani to'smaydi."""
    write_state({"task": "x", "started": time.time(),
                 "calls": {"dasturchi": 2}})
    return run("dasturchi")[0] == 0


def case_ikki_sessiya_tosmaydi(_):
    """Parallel sessiya yoki boshqa proyekt hisobi aralashmaydi."""
    clean()
    return (hook("Agent", "dasturchi", "s-a") == "allow"
            and hook("Agent", "dasturchi", "s-a") == "allow"
            and hook("Agent", "dasturchi", "s-b") == "allow"
            and hook("Agent", "dasturchi", "s-a") == "deny")


def case_yangi_vazifa_boshqasiga_tegmaydi(_):
    clean()
    hook("Agent", "dasturchi", "s-a")
    hook("Agent", "dasturchi", "s-a")
    run("--yangi-vazifa", "B", session="s-b")
    return hook("Agent", "dasturchi", "s-a") == "deny"


def case_envsiz_cli_oz_proyektini_oladi(_):
    """CLAUDE_CODE_SESSION_ID yo'q CLI shu papkadagi sessiyani tanlaydi."""
    clean()
    proj_a = os.path.join(STATE, "projA")
    proj_b = os.path.join(STATE, "projB")
    os.makedirs(os.path.join(proj_a, "src"), exist_ok=True)
    os.makedirs(proj_b, exist_ok=True)
    hook("Agent", "dasturchi", "s-p", cwd=proj_a)
    hook("Agent", "dasturchi", "s-q", cwd=proj_b)
    hook("Agent", "dasturchi", "s-q", cwd=proj_b)
    _, in_a = run("--holat", session=None, cwd=os.path.join(proj_a, "src"))
    _, elsewhere = run("--holat", session=None, cwd=STATE)
    return ("Sessiya: s-p" in in_a and "1/2" in in_a
            and "Sessiya: s-q" in elsewhere and "2/2" in elsewhere)


def case_parallel_hisob_yoqolmaydi(_):
    """Bir xabardagi 6 ta Agent: har turda aynan 2 o'tadi, 4 to'siladi."""
    for _ in range(5):
        fresh()
        got = parallel([payload("Agent", "dasturchi")] * 6)
        if got.count("deny") != 4:
            return False
    return True


def case_parallel_aktyorlar_saqlanadi(_):
    """4 xil aktyor parallel: fayl buzilmaydi, har biri 1 ga teng."""
    fresh()
    parallel([payload("Agent", actor) for actor in
              ("rejalashtiruvchi", "dasturchi", "test-muhandis", "review")])
    calls = state()["sessions"][SESSION]["calls"]
    return calls == {"rejalashtiruvchi": 1, "dasturchi": 1,
                     "test-muhandis": 1, "review": 1}


def case_bir_chaqiruv_bir_marta(_):
    """Repo va global hook birga yursa ham bitta tool_use_id bir marta."""
    fresh()
    first = hook("Agent", "dasturchi", call_id="toolu_1")
    again = hook("Agent", "dasturchi", call_id="toolu_1")
    second = hook("Agent", "dasturchi", call_id="toolu_2")
    third = hook("Agent", "dasturchi", call_id="toolu_3")
    return (first, again, second, third) == ("allow", "allow", "allow", "deny")


def case_yangi_sorov_nolga(_):
    """UserPromptSubmit payloadi shu sessiyani jim nolga tushiradi."""
    fresh()
    hook("Agent", "dasturchi")
    hook("Agent", "dasturchi")
    hook("Agent", "dasturchi", "boshqa")
    proc = call(stdin=json.dumps({"hook_event_name": "UserPromptSubmit",
                                  "session_id": SESSION, "prompt": "x"}))
    calls = state()["sessions"]
    return (proc.returncode == 0 and proc.stdout == ""
            and calls[SESSION]["calls"] == {}
            and calls["boshqa"]["calls"] == {"dasturchi": 1}
            and hook("Agent", "dasturchi") == "allow")


def case_guruhlar_bir_birini_tosmaydi(_):
    """Ikki guruh parallel: har biri o'z ikki chaqiruvini oladi."""
    run("--yangi-vazifa", "partiya")
    got = [hook_group("dasturchi", "orders"), hook_group("dasturchi", "billing"),
           hook_group("dasturchi", "orders"), hook_group("dasturchi", "billing")]
    third = hook_group("dasturchi", "orders")
    other = hook_group("test-muhandis", "orders")
    return got == ["allow"] * 4 and third == "deny" and other == "allow"


def case_guruhsiz_eski_xulq(_):
    run("--yangi-vazifa", "bitta")
    first = [hook("Agent", "review"), hook("Agent", "review")]
    return first == ["allow", "allow"] and hook("Agent", "review") == "deny"


def case_guruh_holat_va_tiklash(_):
    run("--yangi-vazifa", "holat")
    hook_group("dasturchi", "orders")
    hook_group("dasturchi", "orders")
    _, before = run("--holat")
    code, out = run("--tiklash", "dasturchi", "--guruh", "orders")
    after = hook_group("dasturchi", "orders")
    return ("Guruh: orders" in before and code == 0
            and "orders/dasturchi: 1/2" in out and after == "allow")


CASES = [
    ("ikki chaqiruv o'tadi", case_ikki_marta),
    ("uchinchisi to'siladi", case_uchinchi_tosiladi),
    ("to'siq sababni so'raydi", case_sabab_aytiladi),
    ("to'siq buyrug'i klonga mos", case_tosiq_buyrugi_klonga_mos),
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
    ("guruhlar bir-birini to'smaydi", case_guruhlar_bir_birini_tosmaydi),
    ("guruhsiz chaqiruv eski xulqda", case_guruhsiz_eski_xulq),
    ("guruh holati va tiklash", case_guruh_holat_va_tiklash),
]


def main(argv=()):
    try:
        return testkit.run_cases(
            [(name, lambda fn=fn: bool(fn(None))) for name, fn in CASES], argv)
    finally:
        shutil.rmtree(STATE, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
