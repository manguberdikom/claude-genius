#!/usr/bin/env python3
"""actor_check.py (SubagentStop hooki) uchun sinovlar.

    python3 tools/test_actor_check.py

Va'da: dasturchi yoki test-muhandis kod faylini o'zgartirib, test
yurgizmay yoki javobda `run_tests exit=` qatorisiz to'xtasa, hook
`decision: block` beradi. Qolgan hamma holatda jim: boshqa aktyor,
nofaol proyekt, ikkinchi to'xtash (`stop_hook_active`), faqat hujjat
tegilgan, tahrir yo'q, transkript o'qilmaydi. Jurnal yozuvi faqat
oxirgi tahrirdan keyingi va shu fayl turgan ildizniki bo'lsa sanaladi:
guruh worktree sidagi fayl uchun asosiy ildizdagi yurish yetmaydi.
"""

import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TEMP = tempfile.mkdtemp(prefix="actor_check_")
STATE = os.path.join(TEMP, "state")
os.environ["GENIUS_STATE_DIR"] = STATE   # import dan OLDIN: modul uni importda oladi
sys.path.insert(0, HERE)
import actor_check  # noqa: E402
import testkit  # noqa: E402

actor_check.STATE_DIR = STATE
actor_check.JOURNAL = os.path.join(STATE, "run_tests.jsonl")

PROJECT = os.path.join(TEMP, "app")
JAVA = os.path.join(PROJECT, "src", "main", "java", "A.java")
WORKTREE = os.path.join(PROJECT, ".claude", "worktrees", "genius-orders")
WT_JAVA = os.path.join(WORKTREE, "src", "main", "java", "B.java")
LINE = "O'zgarish: x\nTestlar: run_tests exit=0, 3 sinf\nBajarilmagan: yo'q"
COUNTER = [0]


def stamp(seconds):
    return datetime.datetime.fromtimestamp(seconds, datetime.timezone.utc) \
        .isoformat().replace("+00:00", "Z")


def tool_use(name, **tool_input):
    return {"type": "tool_use", "id": "t%d" % time.perf_counter_ns(),
            "name": name, "input": tool_input}


def row(kind, at, *content):
    return {"type": kind, "timestamp": stamp(at),
            "message": {"role": kind, "content": list(content)}}


def transcript(rows, name=None):
    COUNTER[0] += 1
    path = os.path.join(TEMP, name or "agent-%d.jsonl" % COUNTER[0])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        for item in rows:
            handle.write(json.dumps(item) + "\n")
    return path


def edited(path=JAVA, at=None, text=LINE, tool="Edit"):
    """Aktyor transkripti: tahrir, keyin yakuniy javob."""
    at = time.time() - 60 if at is None else at
    return transcript([
        row("user", at - 5, {"type": "text", "text": "vazifa"}),
        row("assistant", at, tool_use(tool, file_path=path)),
        row("assistant", at + 30, {"type": "text", "text": text}),
    ])


def journal(*rows):
    os.makedirs(STATE, exist_ok=True)
    with open(actor_check.JOURNAL, "w", encoding="utf-8") as handle:
        for item in rows:
            handle.write(json.dumps(item) + "\n")


def run_entry(root=PROJECT, ts=None, mode="maqsadli"):
    return {"ts": int(time.time() if ts is None else ts), "root": root,
            "mode": mode, "exit": 0}


def payload(agent="dasturchi", path=None, message=LINE, **extra):
    data = {"session_id": "s", "hook_event_name": "SubagentStop",
            "cwd": PROJECT, "stop_hook_active": False, "agent_id": "a1",
            "agent_type": agent, "agent_transcript_path": path,
            "last_assistant_message": message,
            "transcript_path": os.path.join(TEMP, "main.jsonl")}
    for key, value in extra.items():
        if value is None:
            data.pop(key, None)
        else:
            data[key] = value
    return data


def call(data, project=ROOT):
    res = testkit.call_main(actor_check.main, json.dumps(data), argv=["actor_check.py"],
                            env={"CLAUDE_PROJECT_DIR": project, "GENIUS_HOOKS": None})
    return res


def blocked(data, project=ROOT):
    res = call(data, project)
    if res.returncode != 0 or res.stderr:
        raise AssertionError("rc=%d stderr=%s" % (res.returncode, res.stderr))
    if not res.stdout.strip():
        return None
    out = json.loads(res.stdout)
    assert out.get("decision") == "block", out
    return out["reason"]


def case_testsiz_block():
    journal()
    reason = blocked(payload(path=edited(), message="O'zgarish: x\nBajarilmagan: yo'q"))
    return bool(reason) and "run_tests exit=" in reason and "jurnal" in reason


def case_qator_va_jurnal_otadi():
    journal(run_entry())
    return blocked(payload(path=edited())) is None


def case_qatorsiz_jurnal_bor_block():
    journal(run_entry())
    reason = blocked(payload(path=edited(), message="O'zgarish: x"))
    return bool(reason) and "qatori yo'q" in reason and "jurnalida" not in reason


def case_jurnal_tahrirdan_oldin_block():
    journal(run_entry(ts=time.time() - 3600))
    reason = blocked(payload(path=edited()))
    return bool(reason) and "jurnalida" in reason and "qatori yo'q" not in reason


def case_begona_ildiz_block():
    journal(run_entry(root=os.path.join(TEMP, "boshqa")))
    return bool(blocked(payload(path=edited())))


def case_isitish_sanalmaydi():
    journal(run_entry(mode="isitish"))
    return bool(blocked(payload(path=edited())))


def case_guruh_worktree():
    # Worktree asosiy daraxt ichida: asosiy ildizdagi yurish guruh faylini
    # sinamaydi, worktree ildizidagi yurish esa sanaladi.
    path = edited(WT_JAVA)
    journal(run_entry(root=PROJECT))
    main_only = blocked(payload(path=path))
    journal(run_entry(root=WORKTREE))
    return [("asosiy ildizdagi yurish yetmaydi", bool(main_only)),
            ("worktree ildizidagi yurish sanaladi", blocked(payload(path=path)) is None)]


def case_test_muhandis():
    journal()
    text = "Qoplandi: x\nNatija: run_tests exit=0: 4 test o'tdi"
    path = edited(os.path.join(PROJECT, "src", "test", "java", "AT.java"), text=text,
                  tool="Write")
    missing = blocked(payload("test-muhandis", path, message=text))
    journal(run_entry())
    return [("test-muhandis jurnalsiz block", bool(missing)),
            ("test-muhandis Natija qatori va jurnal bilan o'tadi",
             blocked(payload("test-muhandis", path, message=text)) is None)]


def case_boshqa_aktyor_jim():
    journal()
    path = edited(text="hech narsa")
    return [(name + " jim", blocked(payload(name, path, message="x")) is None)
            for name in ("review", "rejalashtiruvchi", "qidiruv", "general-purpose",
                         "boshqa-plugin:dasturchi")]


def case_prefiks():
    journal()
    return bool(blocked(payload("manguberdi:dasturchi", edited(), message="x")))


def case_stop_hook_active_jim():
    journal()
    return blocked(payload(path=edited(), message="x", stop_hook_active=True)) is None


def case_nofaol_jim():
    journal()
    other = os.path.join(TEMP, "python-loyiha")
    os.makedirs(other, exist_ok=True)
    return blocked(payload(path=edited(), message="x"), project=other) is None


def case_faqat_hujjat_jim():
    journal()
    path = edited(os.path.join(PROJECT, "README.md"),
                  text="Testlar: yurgizilmadi, faqat hujjat")
    return blocked(payload(path=path, message="Testlar: yurgizilmadi")) is None


def case_tahrirsiz_jim():
    journal()
    at = time.time() - 30
    path = transcript([row("assistant", at, tool_use("Read", file_path=JAVA)),
                       row("assistant", at + 1, {"type": "text", "text": "Ochiq qaror: ?"})])
    return blocked(payload(path=path, message="Ochiq qaror: ?")) is None


def case_transkript_yoq_jim():
    journal()
    missing = os.path.join(TEMP, "yoq.jsonl")
    return [("yo'q fayl", blocked(payload(path=missing, message="x")) is None),
            ("buzuq payload", call({"x": 1}).stdout == "" and call({"x": 1}).returncode == 0),
            ("JSON emas", testkit.call_main(actor_check.main, "{buzuq",
                                            env={"CLAUDE_PROJECT_DIR": ROOT}).stdout == "")]


def case_tasirlangan_test_yoq():
    journal()
    at = time.time() - 60
    path = transcript([
        row("assistant", at, tool_use("Edit", file_path=JAVA)),
        row("user", at + 10, {"type": "tool_result", "tool_use_id": "x",
                              "content": "Ta'sirlangan test yo'q: o'zgargan fayllar testga tegmaydi"}),
        row("assistant", at + 20, {"type": "text", "text": LINE}),
    ])
    return blocked(payload(path=path)) is None


def case_oxirgi_xabar_transkriptdan():
    journal(run_entry())
    good = blocked(payload(path=edited(), last_assistant_message=None)) is None
    bad = blocked(payload(path=edited(text="Bajarildi."), last_assistant_message=None))
    return [("maydon yo'q: transkriptdagi qator o'qiladi", good),
            ("maydon yo'q: qatorsiz transkript block", bool(bad))]


def case_tur_zaxira():
    journal()
    # agent_type yo'q: avval agent-<id>.meta.json, keyin asosiy transkript.
    meta_path = edited()
    with open(meta_path[:-len(".jsonl")] + ".meta.json", "w", encoding="utf-8") as handle:
        json.dump({"agentType": "dasturchi"}, handle)
    by_meta = blocked(payload(path=meta_path, message="x", agent_type=None))
    at = time.time() - 120
    main = transcript([row("assistant", at, tool_use("Agent", subagent_type="dasturchi",
                                                     prompt="p"))])
    by_main = blocked(payload(path=edited(), message="x", agent_type=None,
                              transcript_path=main))
    main_review = transcript([
        row("assistant", at, tool_use("Agent", subagent_type="dasturchi", prompt="p")),
        row("assistant", at + 1, tool_use("Task", subagent_type="review", prompt="p"))])
    by_review = blocked(payload(path=edited(), message="x", agent_type=None,
                                transcript_path=main_review))
    return [("meta.json dan dasturchi", bool(by_meta)),
            ("asosiy transkriptdagi oxirgi Agent dan", bool(by_main)),
            ("oxirgi chaqiruv review: jim", by_review is None)]


def case_yol_zaxira():
    # agent_transcript_path yo'q: <sessiya>/subagents/agent-<id>.jsonl
    journal()
    main = os.path.join(TEMP, "sess.jsonl")
    open(main, "w").close()
    at = time.time() - 60
    transcript([row("assistant", at, tool_use("Edit", file_path=JAVA))],
               name=os.path.join("sess", "subagents", "agent-a9.jsonl"))
    return bool(blocked(payload(message="x", agent_transcript_path=None,
                                transcript_path=main, agent_id="a9")))


def case_jarayon_chegarasi():
    """E2E: haqiqiy jarayon, stdin baytlar, stdout JSON."""
    journal()
    data = payload(path=edited(), message="x")
    env = dict(os.environ, CLAUDE_PROJECT_DIR=ROOT, GENIUS_STATE_DIR=STATE)
    env.pop("GENIUS_HOOKS", None)
    proc = subprocess.run([sys.executable, os.path.join(HERE, "actor_check.py")],
                          input=json.dumps(data).encode("utf-8"), capture_output=True,
                          env=env, timeout=30)
    out = json.loads(proc.stdout.decode("utf-8"))
    return proc.returncode == 0 and out.get("decision") == "block" and not proc.stderr


CASES = [
    ("testsiz va qatorsiz: block", case_testsiz_block),
    ("qator va jurnal yozuvi bor: o'tadi", case_qator_va_jurnal_otadi),
    ("jurnal bor, qator yo'q: block", case_qatorsiz_jurnal_bor_block),
    ("jurnal yozuvi tahrirdan oldin: block", case_jurnal_tahrirdan_oldin_block),
    ("begona ildiz yozuvi sanalmaydi", case_begona_ildiz_block),
    ("isitish yozuvi sanalmaydi", case_isitish_sanalmaydi),
    ("guruh worktree ildizi", case_guruh_worktree),
    ("test-muhandis", case_test_muhandis),
    ("boshqa aktyor", case_boshqa_aktyor_jim),
    ("manguberdi: prefiksi kesiladi", case_prefiks),
    ("stop_hook_active: ikkinchi to'xtash jim", case_stop_hook_active_jim),
    ("hookio.active false: jim", case_nofaol_jim),
    ("faqat hujjat tegilgan: jim", case_faqat_hujjat_jim),
    ("tahrir yo'q: jim", case_tahrirsiz_jim),
    ("fail-open", case_transkript_yoq_jim),
    ("run_tests 'Ta'sirlangan test yo'q': jim", case_tasirlangan_test_yoq),
    ("last_assistant_message yo'q", case_oxirgi_xabar_transkriptdan),
    ("agent_type zaxirasi", case_tur_zaxira),
    ("agent_transcript_path zaxirasi", case_yol_zaxira),
    ("jarayon chegarasi", case_jarayon_chegarasi),
]


def main(argv=()):
    try:
        os.makedirs(os.path.dirname(JAVA), exist_ok=True)
        os.makedirs(os.path.dirname(WT_JAVA), exist_ok=True)
        for path in (JAVA, WT_JAVA):
            open(path, "w").close()
        return testkit.run_cases(CASES, argv)
    finally:
        shutil.rmtree(TEMP, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
