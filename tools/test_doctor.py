#!/usr/bin/env python3
"""doctor.py uchun sinovlar.

    python3 tools/test_doctor.py

Asosiy holat: repodagi .claude/settings.json dagi har hook
tools/testdata/hooks namunasi bilan shartnomadan o'tadi. `python3` nomi
sinov Python yo'liga almashtiriladi: Windows CI da python3 Store stub'i
bo'lishi mumkin, sinalayotgan narsa esa asbob shartnomasi. Qolgan
holatlar soxta hook skriptlari va soxta CLAUDE_CONFIG_DIR bilan: haqiqiy
~/.claude va .claude/.state ga tegilmaydi.
"""

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import doctor as D  # noqa: E402

PY = sys.executable.replace("\\", "/")


class Env:
    """os.environ ni vaqtincha almashtiradi (None: o'chiriladi)."""

    def __init__(self, **values):
        self.values = values
        self.saved = {}

    def __enter__(self):
        for key, value in self.values.items():
            self.saved[key] = os.environ.get(key)
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        return self

    def __exit__(self, *exc):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def script(tmp, name, body):
    """Hook o'rnidagi soxta skript: stdin JSON -> `payload`."""
    return write(os.path.join(tmp, name),
                 "import json, sys\npayload = json.load(sys.stdin)\n" + body)


def command(path, suffix=" || exit 0"):
    return '"%s" "%s"%s' % (PY, path.replace("\\", "/"), suffix)


def settings_with(hooks):
    """{event: [(matcher, buyruq), ...]} -> settings.json shakli."""
    out = {}
    for event, items in hooks.items():
        out[event] = [dict({"hooks": [{"type": "command", "command": cmd,
                                       "timeout": 20}]},
                           **({"matcher": matcher} if matcher else {}))
                      for matcher, cmd in items]
    return {"hooks": out}


def statuses(results):
    return [status for status, _ in results]


def case_versiya():
    same = D.check_version("2.1.289 (Claude Code)", "2.1.289")
    newer = D.check_version("2.2.0 (Claude Code)", "2.1.289")
    older = D.check_version("2.1.10", "2.1.289")
    return (same[0] == D.OK and newer[0] == D.WARN and "yangi" in newer[1]
            and older[0] == D.WARN and "eski" in older[1]
            and D.check_version(None)[0] == D.SKIP
            and D.check_version("noma'lum")[0] == D.WARN
            and D.SINALGAN_CLAUDE_CODE == "2.1.289")


def proc(code=0, out="", err=""):
    return subprocess.CompletedProcess([], code, out, err)


def case_hukm():
    good = json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                              "permissionDecision": "deny"}})
    return (D.judge("PreToolUse", proc())[0] == D.OK
            and D.judge("PreToolUse", proc(out=good))[0] == D.OK
            and D.judge("PostToolUse", proc(out=good))[0] == D.FAIL
            and D.judge("PostToolUse", proc(
                out='{"decision": "block", "reason": "x"}'))[0] == D.OK
            and D.judge("Stop", proc(out="oddiy matn"))[0] == D.FAIL
            and D.judge("Stop", proc(out='{"boshqa": 1}'))[0] == D.FAIL
            and D.judge("Stop", proc(err="Traceback"))[0] == D.FAIL
            and D.judge("Stop", proc(code=2, err="yo'q"))[0] == D.FAIL)


def case_repo_hooklari_shartnomada():
    """Repodagi har hook namuna payload bilan exit 0, bo'sh stderr, to'g'ri JSON."""
    with io.open(os.path.join(ROOT, ".claude", "settings.json"),
                 encoding="utf-8") as handle:
        settings = json.load(handle)
    for groups in settings["hooks"].values():
        for group in groups:
            for hook in group["hooks"]:
                if hook["command"].startswith("python3 "):
                    hook["command"] = '"%s" %s' % (PY, hook["command"][len("python3 "):])
    results = D.check_hooks(settings, ROOT)
    bad = [text for status, text in results if status != D.OK]
    if bad:
        raise AssertionError("; ".join(bad))
    return len(results) == 8


def case_exit_0_yutmaydi(tmp):
    """`|| exit 0` olib tashlanadi: yiqilgan, stderr li yoki noto'g'ri
    hookEventName li hook XATO bo'ladi, to'g'risi OK."""
    good = script(tmp, "good.py", (
        "assert payload['hook_event_name'] == 'Stop'\n"
        "assert payload['transcript_path'].endswith('/transcript.jsonl')\n"
        "print(json.dumps({'decision': 'block', 'reason': 'x'}))\n"))
    crash = script(tmp, "crash.py", "sys.exit(2)\n")
    noisy = script(tmp, "noisy.py", "sys.stderr.write('ogoh\\n')\n")
    wrong = script(tmp, "wrong.py", (
        "print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse'}}))\n"))
    missing = os.path.join(tmp, "yoq", "guard.py")
    settings = settings_with({"Stop": [
        ("", command(good)), ("", command(crash)), ("", command(noisy)),
        ("", command(wrong)), ("", command(missing))]})
    return statuses(D.check_hooks(settings, ROOT)) == [
        D.OK, D.FAIL, D.FAIL, D.FAIL, D.FAIL]


def case_matcher_mos_namuna(tmp):
    """Task|Agent hooki Bash namunasini emas, PreToolUse-Agent.json ni oladi."""
    check = script(tmp, "agent.py", "sys.exit(0 if payload['tool_name'] == 'Agent' else 1)\n")
    bash = script(tmp, "bash.py", "sys.exit(0 if payload['tool_name'] == 'Bash' else 1)\n")
    settings = settings_with({
        "PreToolUse": [("Task|Agent", command(check)),
                       ("Read|Bash|PowerShell", command(bash))],
        "SessionStart": [("", command(bash))],
    })
    results = D.check_hooks(settings, ROOT)
    return (statuses(results) == [D.OK, D.OK, D.WARN]
            and "namunaviy payload yo'q" in results[2][1])


def case_hook_holatga_tegmaydi(tmp):
    """Hook GENIUS_STATE_DIR va USAGE_STORE ni vaqtinchalik papkada oladi."""
    probe = script(tmp, "env.py", (
        "import os\n"
        "ok = all(os.environ.get(k, '').find('doctor_') >= 0\n"
        "         for k in ('GENIUS_STATE_DIR', 'USAGE_STORE'))\n"
        "sys.exit(0 if ok and os.environ.get('CLAUDE_PROJECT_DIR') else 1)\n"))
    return statuses(D.check_hooks(settings_with({"Stop": [("", command(probe))]}),
                                  ROOT)) == [D.OK]


def case_python(tmp):
    with Env(GENIUS_PYTHON=sys.executable):
        good = D.check_python({})
    with Env(GENIUS_PYTHON=os.path.join(tmp, "yoq-python"), PATH=tmp):
        bad = D.check_python({})
    with Env(GENIUS_PYTHON=None, PATH=tmp):
        from_settings = D.check_python({"env": {"GENIUS_PYTHON": sys.executable}})
    return (good[0] == D.OK and bad[0] == D.FAIL and "GENIUS_PYTHON" in bad[1]
            and from_settings[0] == D.OK and "settings" in from_settings[1])


def case_klon(tmp):
    return (D.check_clone(None)[0] == D.OK
            and D.check_clone({"root": ROOT})[0] == D.OK
            and D.check_clone({"root": os.path.join(tmp, "ko'chgan")})[0] == D.FAIL)


def case_ornatilgan(tmp):
    head = D.git_head(ROOT)
    same = D.check_installed({"commit": head, "root": ROOT})
    other = D.check_installed({"commit": "0" * 40, "root": ROOT})
    return (D.check_installed(None)[0] == D.SKIP
            and D.check_installed([1])[0] == D.WARN
            and (not head or (same[0] == D.OK and other[0] == D.WARN
                              and "o'rnatilgan: 000000000000" in other[1])))


def case_snapshot_manifesti(tmp):
    """R7.8 XV-Y1: manifestda `clone` bor: root snapshot (tools shu yerda),
    klon alohida. Snapshot to'liq emas yoki klon yo'q bo'lsa aytiladi, commit
    farqi `yangilash.py` ga yo'naltiradi (eski o'rnatishdagi 'qayta yurgizing' emas)."""
    head = D.git_head(ROOT)
    pinned = {"root": ROOT, "clone": ROOT, "commit": "0" * 40}
    ok = D.check_clone(pinned)
    gone = D.check_clone({"root": ROOT, "clone": os.path.join(tmp, "yoq-klon")})
    broken = D.check_clone({"root": os.path.join(tmp, "yoq-snapshot"), "clone": ROOT})
    diff = D.check_installed(pinned)
    old = D.check_installed({"root": ROOT, "commit": "0" * 40})
    return (ok[0] == D.OK and "snapshot" in ok[1]
            and gone[0] == D.WARN and "memory va holat" in gone[1]
            and broken[0] == D.FAIL and "snapshot" in broken[1]
            and (not head or (diff[0] == D.WARN and "yangilash.py" in diff[1]
                              and "yangilash.py" not in old[1])))


def subagent(cfg, sid, name, actor, model, age_days=0):
    folder = os.path.join(cfg, "projects", "p", sid, "subagents")
    path = write(os.path.join(folder, name + ".jsonl"), json.dumps(
        {"type": "assistant", "message": {"model": model, "role": "assistant"}}) + "\n")
    meta = write(os.path.join(folder, name + ".meta.json"),
                 json.dumps({"agentType": actor}))
    if age_days:
        old = time.time() - age_days * 86400
        os.utime(meta, (old, old))
    return path


def case_aktyor_modeli(tmp):
    """review sonnet da OK; dasturchi opus da OGOH va pin yo'li; 40 kunlik
    fayl va repo aktyori bo'lmagan tur hisobga kirmaydi."""
    cfg = os.path.join(tmp, "cfg")
    with Env(CLAUDE_CONFIG_DIR=cfg):
        empty = D.check_models(30)
        subagent(cfg, "s1", "agent-a", "review", "claude-sonnet-5-5")
        subagent(cfg, "s1", "agent-b", "dasturchi", "claude-opus-5-5")
        subagent(cfg, "s1", "agent-c", "dasturchi", "claude-opus-5-5", age_days=40)
        subagent(cfg, "s1", "agent-d", "general-purpose", "claude-opus-5-5")
        results = D.check_models(30)
    texts = dict((text.split(":")[0], (status, text)) for status, text in results)
    review = texts.get("OK   model review")
    coder = texts.get("OGOH model dasturchi")
    return (statuses(empty) == [D.SKIP] and len(results) == 2
            and review is not None and coder is not None
            and "x1" in coder[1] and "ANTHROPIC_DEFAULT_SONNET_MODEL" in coder[1])


def case_cli_bir_qator_va_kod(tmp):
    """Har band bir qator; XATO bo'lsa 1, bo'lmasa 0."""
    good = script(tmp, "cli_good.py", "")
    crash = script(tmp, "cli_crash.py", "sys.exit(3)\n")
    ok_path = write(os.path.join(tmp, "ok.json"), json.dumps(
        settings_with({"Stop": [("", command(good))]})))
    bad_path = write(os.path.join(tmp, "bad.json"), json.dumps(
        settings_with({"Stop": [("", command(crash))]})))
    env = dict(os.environ, CLAUDE_CONFIG_DIR=os.path.join(tmp, "bo'sh"),
               GENIUS_PYTHON=sys.executable,
               GENIUS_STATE_DIR=os.path.join(tmp, "cli-holat"))
    runs = [subprocess.run([sys.executable, os.path.join(HERE, "doctor.py"),
                            "--settings", path], capture_output=True, text=True,
                           env=env, cwd=tmp)
            for path in (ok_path, bad_path)]
    bands = [ln for ln in runs[0].stdout.splitlines()
             if ln and not ln.startswith("doctor:")]
    write(os.path.join(tmp, "cli-log", "hook_errors.log"),
          "%s\thandoff\tValueError: \u0416 xabar\n2020-01-01T00:00:00\tx\tOSError: eski\n"
          % time.strftime("%Y-%m-%dT%H:%M:%S"))
    logged = subprocess.run(
        [sys.executable, os.path.join(HERE, "doctor.py"), "--settings", ok_path],
        capture_output=True, text=True, cwd=tmp,
        env=dict(env, GENIUS_STATE_DIR=os.path.join(tmp, "cli-log"),
                 PYTHONIOENCODING="ascii"))
    logged_bands = [ln for ln in logged.stdout.splitlines()
                    if ln and not ln.startswith("doctor:")]
    return (runs[0].returncode == 0 and runs[1].returncode == 1
            and all(ln[:4].rstrip() in (D.OK, D.WARN, D.FAIL, D.SKIP) for ln in bands)
            and logged.returncode == 0
            and all(ln[:4].rstrip() in (D.OK, D.WARN, D.FAIL, D.SKIP)
                    for ln in logged_bands)
            and any(ln.startswith("OGOH hook xatolari") and "jami 2" in ln
                    for ln in logged_bands)
            and any(ln.startswith("OK   hook xatolari") and "toza" in ln for ln in bands)
            and any("hook Stop cli_crash.py" in ln and ln.startswith("XATO")
                    for ln in runs[1].stdout.splitlines()))


def error_lines(state, rows):
    write(os.path.join(state, "hook_errors.log"), "".join(rows))


def stamp(now, ago):
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now - ago))


def case_hook_xatolari_toza(tmp):
    """Log yo'q yoki bo'sh: bitta OK 'toza' qatori, davomsiz."""
    state = os.path.join(tmp, "xato-toza")
    with Env(GENIUS_STATE_DIR=state):
        missing = D.check_hook_errors()
        error_lines(state, [])
        empty = D.check_hook_errors()
        error_lines(state, ["\n", "  \n"])
        blank = D.check_hook_errors()
    return all(len(r) == 1 and r[0][0] == D.OK and "toza" in r[0][1]
               and "handoff" in r[0][1] for r in (missing, empty, blank))


def case_hook_xatolari_oxirgilar_va_son(tmp):
    """8 qator, yoshi 250, 222, 194, 55.6, 30.6 soat, 1 soat, 1 daqiqa va
    kelajakdagi (1 soat keyingi): oxirgi 5 ko'rinadi (h3..h7), 24 soatlik son 2 (1 soat va 1 daqiqa; kelajakdagi kirmaydi), OGOH,
    hammasi bitta qatorda."""
    state = os.path.join(tmp, "xato-bir-nechta")
    now = time.time()
    ages = (900000, 800000, 700000, 200000, 110000, 3600, 60, -3600)
    rows = ["%s\th%d\tValueError: xabar %d\n" % (stamp(now, ago), i, i)
            for i, ago in enumerate(ages)]
    error_lines(state, rows)
    with Env(GENIUS_STATE_DIR=state):
        results = D.check_hook_errors(now)
    (status, text), = results
    return (status == D.WARN and "\n" not in text
            and "oxirgi 24 soatda 2, jami 8" in text
            and all(("h%d " % i) in text for i in (3, 4, 5, 6, 7))
            and "h2 " not in text and "o'qilmagan" not in text)


def case_hook_xatolari_eski_qizil_emas(tmp):
    """Faqat eski xato: OK (qizil emas), lekin oxirgisi ko'rinadi; XATO hech qachon."""
    state = os.path.join(tmp, "xato-eski")
    now = time.time()
    error_lines(state, ["%s\tguard\tOSError: eski\n" % stamp(now, 5 * 86400)])
    with Env(GENIUS_STATE_DIR=state):
        results = D.check_hook_errors(now)
    return (results[0][0] == D.OK and "oxirgi 24 soatda 0, jami 1" in results[0][1]
            and "OSError: eski" in results[0][1] and len(results) == 1
            and D.FAIL not in statuses(results))


def case_hook_xatolari_buzuq_qator(tmp):
    """Buzuq qator (tabsiz, noto'g'ri vaqt, bo'sh maydon) yiqitmaydi: jami va
    'o'qilmagan' ga kiradi, 24 soatga kirmaydi."""
    state = os.path.join(tmp, "xato-buzuq")
    now = time.time()
    error_lines(state, ["faqat matn\n", "kecha\tguard\tX: y\n",
                        "%s\tguard\n" % stamp(now, 10),
                        "%s\tbudget\tKeyError: 'k'\n" % stamp(now, 10)])
    with Env(GENIUS_STATE_DIR=state):
        results = D.check_hook_errors(now)
    (status, text), = results
    return (status == D.WARN and "oxirgi 24 soatda 1, jami 4, o'qilmagan 3" in text
            and "o'qilmadi: faqat matn" in text and "KeyError" in text)


def case_hook_xatolari_holat_yoli(tmp):
    """Haqiqiy kutilgan yo'l: GENIUS_STATE_DIR berilsa o'sha papka; berilmasa
    klon ichidagi .claude/.state; hook snapshotdan yurganda (ROOT
    `<...>/.claude/genius/<12 hex>`) va GENIUS_CLONE bo'lsa klonniki."""
    import hookio
    clone = os.path.join(tmp, "klon")
    snapshot = os.path.join(tmp, "home", ".claude", "genius", "0123456789ab")
    os.makedirs(clone)
    os.makedirs(snapshot)
    saved = hookio.ROOT
    try:
        with Env(GENIUS_STATE_DIR=os.path.join(tmp, "boshqa"), GENIUS_CLONE=clone):
            given = D.check_hook_errors()[0][1]
        hookio.ROOT = clone
        with Env(GENIUS_STATE_DIR=None, GENIUS_CLONE=None):
            in_clone = D.check_hook_errors()[0][1]
        hookio.ROOT = snapshot
        with Env(GENIUS_STATE_DIR=None, GENIUS_CLONE=clone):
            from_snapshot = D.check_hook_errors()[0][1]
    finally:
        hookio.ROOT = saved
    log = os.path.join(".claude", ".state", "hook_errors.log")
    return (os.path.join(tmp, "boshqa", "hook_errors.log") in given
            and os.path.join(clone, log) in in_clone
            and os.path.join(clone, log) in from_snapshot
            and snapshot not in from_snapshot)


CASES = [
    ("claude versiyasi sinalgan bilan solishtiriladi", case_versiya),
    ("hook chiqishi hukmi: exit, stderr, hookEventName", case_hukm),
    ("repo hooklari namuna payload bilan shartnomada", case_repo_hooklari_shartnomada),
    ("|| exit 0 xatoni yutmaydi", case_exit_0_yutmaydi),
    ("matcher ga mos namuna, namuna yo'q bo'lsa OGOH", case_matcher_mos_namuna),
    ("hook vaqtinchalik holat papkasida yuradi", case_hook_holatga_tegmaydi),
    ("GENIUS_PYTHON, settings env va python3", case_python),
    ("klon yo'li bor-yo'qligi", case_klon),
    ("o'rnatilgan commit klon bilan", case_ornatilgan),
    ("snapshot manifesti: root snapshot, clone klon", case_snapshot_manifesti),
    ("aktyor -> model jadvali va alias ogohlantirishi", case_aktyor_modeli),
    ("hook xatolari: log yo'q yoki bo'sh bo'lsa toza", case_hook_xatolari_toza),
    ("hook xatolari: oxirgi qatorlar va 24 soatlik son", case_hook_xatolari_oxirgilar_va_son),
    ("hook xatolari: eski xato qizil emas", case_hook_xatolari_eski_qizil_emas),
    ("hook xatolari: buzuq qator yiqitmaydi", case_hook_xatolari_buzuq_qator),
    ("hook xatolari: holat papkasi hookio bilan bir", case_hook_xatolari_holat_yoli),
    ("CLI: har band bir qator, kod 0/1", case_cli_bir_qator_va_kod),
]


def main():
    tmp = tempfile.mkdtemp(prefix="doctor_test_")
    failures = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(tmp) if fn.__code__.co_argcount else fn())
            except Exception as exc:
                ok, name = False, "%s (%s)" % (name, exc)
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", name))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
