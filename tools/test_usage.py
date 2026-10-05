#!/usr/bin/env python3
"""usage.py uchun sinovlar.

    python3 tools/test_usage.py

Aktyorga bo'lish soxta transkript bilan, Claude Code yozadigan shaklda
sinaladi: subagent `<sessiya>/subagents/**/agent-<id>.jsonl` da, nomi
yonidagi `.meta.json` da. Meta bo'lmagan eski shakl uchun ikkala zaxira
yo'l ham qo'lda yasalgan qatorlar bilan tekshiriladi: parentUuid zanjiri
va tartib.

Narx hisobida eng ko'p uchraydigan xato keshni kirish narxida sanash.
Keshdan o'qish modelga qarab 10-20 barobar arzon; keshga yozish 5
daqiqalik keshda chorak barobar, 1 soatlikda 2 barobar qimmat: shuning
uchun har bir maydon alohida tekshiriladi.
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

import usage as U  # noqa: E402

DAY = "2026-10-04"


def row(total_read=0, out=0, inp=0, write=0, model="claude-opus-5",
        side=False, uuid=None, parent=None, day=DAY, mid=None, write_1h=None):
    item = {
        "timestamp": "%sT10:00:00.000Z" % day,
        "message": {"model": model, "usage": {
            "input_tokens": inp,
            "cache_creation_input_tokens": write,
            "cache_read_input_tokens": total_read,
            "output_tokens": out}},
    }
    if write_1h is not None:
        item["message"]["usage"]["cache_creation"] = {
            "ephemeral_1h_input_tokens": write_1h,
            "ephemeral_5m_input_tokens": write - write_1h}
    if mid:
        item["message"]["id"] = mid
    if side:
        item["isSidechain"] = True
    if uuid:
        item["uuid"] = uuid
    if parent:
        item["parentUuid"] = parent
    return item


def task_row(actor, uuid):
    return {"timestamp": "%sT10:00:00.000Z" % DAY, "uuid": uuid,
            "message": {"model": "claude-opus-5", "content": [
                {"type": "tool_use", "name": "Task",
                 "input": {"subagent_type": actor}}]}}


def write_jsonl(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as handle:
        for item in rows:
            handle.write(json.dumps(item) + "\n")


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle)


def collect(tmp, rows, name="t.jsonl"):
    path = os.path.join(tmp, name)
    write_jsonl(path, rows)
    return U.collect([path])


def session(tmp, project, sid, main_rows, agents):
    """Haqiqiy shakl: `<p>/<sid>.jsonl` va `<p>/<sid>/subagents/<nisbiy>`.

    agents: {nisbiy yo'l: (qatorlar, meta yoki None)}.
    """
    base = os.path.join(tmp, project)
    main = os.path.join(base, sid + ".jsonl")
    write_jsonl(main, main_rows)
    for rel, (rows, meta) in agents.items():
        path = os.path.join(base, sid, "subagents", rel)
        write_jsonl(path, rows)
        if meta is not None:
            write_json(path[:-len(".jsonl")] + ".meta.json", meta)
    return base, main


def hermetic_env(tmp, **extra):
    """Bolalar jarayoni haqiqiy ~/.claude va repo STORE ga tegmasin."""
    env = dict(os.environ, HOME=tmp, USERPROFILE=tmp, **extra)
    for name in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR"):
        env.pop(name, None)
    return env


def case_narx_maydon_boyicha():
    """Har maydon o'z stavkasida: kirish, kesh yozish, kesh o'qish, chiqish."""
    counts = {"input_tokens": 1_000_000, "cache_creation_input_tokens": 0,
              "cache_read_input_tokens": 0, "output_tokens": 0}
    a = U.cost("claude-opus-5", counts)
    counts = {"input_tokens": 0, "cache_creation_input_tokens": 1_000_000,
              "cache_read_input_tokens": 0, "output_tokens": 0}
    b = U.cost("claude-opus-5", counts)
    counts = {"input_tokens": 0, "cache_creation_input_tokens": 0,
              "cache_read_input_tokens": 1_000_000, "output_tokens": 0}
    c = U.cost("claude-opus-5", counts)
    counts = {"input_tokens": 0, "cache_creation_input_tokens": 0,
              "cache_read_input_tokens": 0, "output_tokens": 1_000_000}
    d = U.cost("claude-opus-5", counts)
    return (abs(a - 5.0) < 1e-9 and abs(b - 6.25) < 1e-9
            and abs(c - 0.5) < 1e-9 and abs(d - 25.0) < 1e-9)


def case_kesh_oqish_modelga_xos():
    """Opus 5.5 da kesh o'qish $0.20, kirishning o'ndan biri ($0.40) emas."""
    counts = {"input_tokens": 0, "cache_creation_input_tokens": 0,
              "cache_read_input_tokens": 1_000_000, "output_tokens": 0}
    return abs(U.cost("claude-opus-5-5", counts) - 0.20) < 1e-9


def case_kesh_yozish_1_soat():
    """1 soatlik keshga yozish 2x, 5 daqiqalik 1.25x emas."""
    counts = {"input_tokens": 0, "cache_creation_input_tokens": 1_000_000,
              "cache_read_input_tokens": 0, "output_tokens": 0,
              "cache_write_1h": 1_000_000}
    return abs(U.cost("claude-opus-5", counts) - 10.0) < 1e-9


def case_sonnet_5_narxi():
    return U.price_for("claude-sonnet-5") == (2.0, 10.0, 0.20)


def case_kesh_1_soat_yigiladi(tmp):
    """`cache_creation` dagi 1 soatlik qism alohida sanaladi."""
    rows, _ = collect(tmp, [row(write=500, write_1h=500)], "w1h.jsonl")
    counts = next(iter(rows.values()))
    return (counts["cache_write_1h"] == 500
            and counts["cache_creation_input_tokens"] == 500)


def case_noma_lum_model_nol_emas():
    """Narxi yo'q model None qaytaradi, nol emas: nol yolg'on son."""
    counts = dict.fromkeys(U.FIELDS, 1000)
    return U.cost("claude-kelajak-9", counts) is None


def case_nol_token_narxsiz_emas():
    """`<synthetic>` javobining tokeni nol: narxi ham nol, belgi kerak emas."""
    return U.cost("<synthetic>", dict.fromkeys(U.FIELDS, 0)) == 0.0


def case_eng_uzun_kalit():
    """opus-5-5 opus-5 dan ustun: qisqa kalit uzunini yutib ketmasin."""
    return U.price_for("claude-opus-5-5") == (4.0, 20.0, 0.20) \
        and U.price_for("claude-opus-5") == (5.0, 25.0, 0.50)


def case_asosiy_sessiya(tmp):
    rows, guessed = collect(tmp, [row(total_read=100, out=10)], "a.jsonl")
    keys = list(rows)
    return (len(keys) == 1 and keys[0][1] == U.MAIN
            and keys[0][0] == DAY and not guessed)


def case_aktyor_parent_boyicha(tmp):
    """parentUuid zanjiri bo'lsa aktyor aniq, taxmin qilinmaydi."""
    rows, guessed = collect(tmp, [
        task_row("arxitektor", "t1"),
        row(total_read=500, out=50, side=True, uuid="s1", parent="t1"),
    ], "b.jsonl")
    actors = {k[1] for k in rows}
    return actors == {"arxitektor"} and not guessed


def case_zanjir_davomi(tmp):
    """Sidechain ichidagi keyingi javob ham shu aktyorga yoziladi."""
    rows, _ = collect(tmp, [
        task_row("review", "t1"),
        row(total_read=100, side=True, uuid="s1", parent="t1"),
        row(total_read=200, side=True, uuid="s2", parent="s1"),
    ], "c.jsonl")
    total = sum(c["cache_read_input_tokens"] for k, c in rows.items()
                if k[1] == "review")
    return total == 300


def case_tartib_boyicha_belgilanadi(tmp):
    """Havola bo'lmasa tartib ishlatiladi va bu AYTILADI."""
    rows, guessed = collect(tmp, [
        task_row("test-muhandis", "t1"),
        row(total_read=400, side=True),      # uuid va parent yo'q
    ], "d.jsonl")
    return {k[1] for k in rows} == {"test-muhandis"} and guessed


def case_ikki_aktyor_aralashmaydi(tmp):
    rows, _ = collect(tmp, [
        task_row("arxitektor", "t1"),
        row(total_read=100, side=True, uuid="s1", parent="t1"),
        task_row("review", "t2"),
        row(total_read=900, side=True, uuid="s2", parent="t2"),
    ], "e.jsonl")
    got = {k[1]: c["cache_read_input_tokens"] for k, c in rows.items()}
    return got.get("arxitektor") == 100 and got.get("review") == 900


def case_subagent_meta_dan(tmp):
    """Subagent alohida faylda, aktyor nomi meta dagi agentType dan."""
    _, main = session(tmp, "pa", "s1", [row(total_read=10)], {
        "agent-a.jsonl": ([row(total_read=500, side=True)],
                          {"agentType": "arxitektor"}),
    })
    rows, guessed = U.collect(U.session_files(main))
    got = {k[1]: c["cache_read_input_tokens"] for k, c in rows.items()}
    return got == {U.MAIN: 10, "arxitektor": 500} and not guessed


def case_workflow_bosqichi(tmp):
    """workflow-subagent bitta tur: bosqich description dan ajratiladi."""
    _, main = session(tmp, "pb", "s1", [], {
        "workflows/wf_1/agent-v.jsonl": (
            [row(total_read=70, side=True)],
            {"agentType": "workflow-subagent", "description": "verify:x:1"}),
    })
    rows, _ = U.collect(U.session_files(main))
    return {k[1] for k in rows} == {"workflow:verify"}


def case_meta_yoq_asosiyga_tushmaydi(tmp):
    """Meta yo'q subagent fayli asosiy sessiyaga yozilmaydi va bu aytiladi."""
    _, main = session(tmp, "pc", "s1", [
        task_row("arxitektor", "t1"), row(total_read=10)], {
        "agent-m.jsonl": ([row(total_read=300, side=True)], None),
    })
    rows, guessed = U.collect(U.session_files(main))
    got = {k[1]: c["cache_read_input_tokens"] for k, c in rows.items()}
    return got.get(U.MAIN) == 10 and got.get("aktyor (noma'lum)") == 300 \
        and guessed


def case_transcripts_ichma_ich(tmp):
    """transcripts(base) workflows ostidagi agentni oladi, journal ni emas."""
    base, _ = session(tmp, "pd", "s1", [row(total_read=1)], {
        "workflows/wf_1/agent-y.jsonl": ([row(total_read=20, side=True)],
                                         {"agentType": "review"}),
        "workflows/wf_1/journal.jsonl": ([row(total_read=4000)], None),
    })
    rows, _ = U.collect(U.transcripts(base))
    got = {k[1]: c["cache_read_input_tokens"] for k, c in rows.items()}
    return got == {U.MAIN: 1, "review": 20}


def case_takroriy_qator_bir_marta(tmp):
    """Bitta javob 3 qatorga bo'linadi: bir marta, oxirgi chiqish bilan."""
    rows, _ = collect(tmp, [
        row(total_read=1000, out=8, mid="msg_1"),
        row(total_read=1000, out=8, mid="msg_1"),
        row(total_read=1000, out=2631, mid="msg_1"),
    ], "dup.jsonl")
    counts = rows[(DAY, U.MAIN, "claude-opus-5")]
    return (counts["cache_read_input_tokens"] == 1000
            and counts["output_tokens"] == 2631)


def case_takrordagi_task_yoqolmaydi(tmp):
    """Task chaqiruvi guruhning uchinchi qatorida: aktyor baribir topiladi."""
    text = row(total_read=100, mid="msg_t", uuid="u1")
    text["message"]["content"] = [{"type": "text", "text": "x"}]
    task = row(total_read=100, mid="msg_t", uuid="u3")
    task["message"]["content"] = [{"type": "tool_use", "name": "Task",
                                   "input": {"subagent_type": "arxitektor"}}]
    rows, guessed = collect(tmp, [
        text, row(total_read=100, mid="msg_t", uuid="u2"), task,
        row(total_read=900, side=True, uuid="s1", parent="u3"),
    ], "duptask.jsonl")
    got = {k[1]: c["cache_read_input_tokens"] for k, c in rows.items()}
    return got == {U.MAIN: 100, "arxitektor": 900} and not guessed


def case_kun_boyicha_bolinadi(tmp):
    rows, _ = collect(tmp, [
        row(total_read=100, day="2026-10-03"),
        row(total_read=200, day="2026-10-04"),
    ], "f.jsonl")
    return {k[0] for k in rows} == {"2026-10-03", "2026-10-04"}


def case_kun_mahalliy_vaqtda():
    """UTC 20:00 qatori UTC+5 da ertangi mahalliy kunga tushadi."""
    if not hasattr(time, "tzset"):
        return True                          # Windows: TZ almashtirib bo'lmaydi
    old = os.environ.get("TZ")
    os.environ["TZ"] = "XYZ-5"
    time.tzset()
    try:
        return (U.day_of("2026-10-04T20:00:00.000Z") == "2026-10-05"
                and U.day_of("2026-10-04T10:00:00.000Z") == DAY)
    finally:
        if old is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old
        time.tzset()


def case_davr_filtri(tmp):
    rows, _ = collect(tmp, [
        row(total_read=100, day="2026-10-03"),
        row(total_read=200, day="2026-10-04"),
    ], "g.jsonl")
    summary = U.summarise(rows, {"2026-10-04"})
    return list(summary) == ["2026-10-04"]


def case_narxsiz_belgilanadi(tmp):
    rows, _ = collect(tmp, [row(total_read=100, model="claude-yoq-7")], "h.jsonl")
    summary = U.summarise(rows, None)
    slot = summary[DAY][U.MAIN]
    return slot[2] is True and slot[1] == 0.0


def case_buzuq_qator_otkaziladi(tmp):
    path = os.path.join(tmp, "i.jsonl")
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write("not json\n")
        handle.write(json.dumps(row(total_read=70)) + "\n")
    rows, _ = U.collect([path])
    return sum(c["cache_read_input_tokens"] for c in rows.values()) == 70


def case_slug_claude_code_bilan_bir_xil():
    """Windows yo'li ham: `C:\\src\\x` -> `C--src-x`, `_` va `.` ham `-`."""
    return (U.slug("C:\\src\\claude-genius") == "C--src-claude-genius"
            and U.slug("/home/a_b.c") == "-home-a-b-c")


def case_proyekt_papkasi_topiladi(tmp):
    """Klon emas, ish papkasi slugi; uzun slugga qo'shilgan hash ham."""
    cfg = os.path.join(tmp, "cfg")
    work = os.path.join(tmp, "my_proj.v2")
    short = os.path.join(cfg, "projects", U.slug(os.path.abspath(work)))
    long_dir = os.path.join(tmp, "x" * 230)
    hashed = os.path.join(cfg, "projects",
                          U.slug(os.path.abspath(long_dir))[:200] + "-abc123")
    os.makedirs(short)
    os.makedirs(hashed)
    old = {k: os.environ.get(k) for k in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR")}
    try:
        os.environ["CLAUDE_CONFIG_DIR"] = cfg
        os.environ["CLAUDE_PROJECT_DIR"] = work
        first = U.project_base()
        os.environ["CLAUDE_PROJECT_DIR"] = long_dir
        second = U.project_base()
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
    return first == short and second == hashed


def case_saqlash_fayl_yozadi(tmp):
    rows, _ = collect(tmp, [
        task_row("arxitektor", "t1"),
        row(total_read=1_000_000, out=1000, side=True, uuid="s1", parent="t1"),
        row(total_read=2_000_000, out=2000),
    ], "j.jsonl")
    saved = os.path.join(tmp, "usage")
    old_store, U.STORE = U.STORE, saved
    try:
        U.save(rows, "proj", "s1")
        path = os.path.join(saved, "2026-10", "proj", "s1.json")
        if not os.path.isfile(path):
            return False
        data = json.load(io.open(path, encoding="utf-8"))
        day = data.get(DAY, {})
        return ("arxitektor" in day and U.MAIN in day
                and day["arxitektor"]["tokens"]["cache_read_input_tokens"] == 1_000_000
                and day["arxitektor"]["usd"] > 0)
    finally:
        U.STORE = old_store


def case_saqlash_ikki_marta_qoshmaydi(tmp):
    """Qayta saqlash kunni BOSADI, ustiga qo'shmaydi."""
    rows, _ = collect(tmp, [row(total_read=1_000_000)], "k.jsonl")
    saved = os.path.join(tmp, "usage2")
    old_store, U.STORE = U.STORE, saved
    try:
        U.save(rows, "proj", "s1")
        U.save(rows, "proj", "s1")
        data = json.load(io.open(os.path.join(saved, "2026-10", "proj", "s1.json"),
                                 encoding="utf-8"))
        got = data[DAY][U.MAIN]["tokens"]["cache_read_input_tokens"]
        return got == 1_000_000
    finally:
        U.STORE = old_store


def case_ikki_sessiya_bosmaydi(tmp):
    """Bir kunda ikki sessiya: ikkala fayl ham qoladi."""
    saved = os.path.join(tmp, "usage3")
    old_store, U.STORE = U.STORE, saved
    try:
        for sid, read in (("s1", 100), ("s2", 200)):
            rows, _ = collect(tmp, [row(total_read=read)], sid + "_l.jsonl")
            U.save(rows, "proj", sid)
        folder = os.path.join(saved, "2026-10", "proj")
        got = {}
        for sid in ("s1", "s2"):
            data = json.load(io.open(os.path.join(folder, sid + ".json"),
                                     encoding="utf-8"))
            got[sid] = data[DAY][U.MAIN]["tokens"]["cache_read_input_tokens"]
        return got == {"s1": 100, "s2": 200}
    finally:
        U.STORE = old_store


def case_saqlash_hook_payload(tmp):
    """Stop hook payloadidagi sessiya subagentlari bilan yoziladi."""
    _, main = session(tmp, "p", "s1", [row(total_read=10)], {
        "agent-a.jsonl": ([row(total_read=500, side=True)],
                          {"agentType": "arxitektor"}),
    })
    store = os.path.join(tmp, "st_payload")
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "usage.py"), "--saqlash"],
        capture_output=True, text=True, cwd=tmp,
        input=json.dumps({"transcript_path": main, "session_id": "s1"}),
        env=hermetic_env(tmp, USAGE_STORE=store))
    path = os.path.join(store, "2026-10", "p", "s1.json")
    if proc.returncode != 0 or proc.stdout.strip() or not os.path.isfile(path):
        return False
    day = json.load(io.open(path, encoding="utf-8")).get(DAY, {})
    return set(day) == {U.MAIN, "arxitektor"}


def case_saqlash_hook_jim(tmp):
    """--saqlash hech narsa chiqarmaydi va 0 qaytaradi: Stop hook uchun.

    HOME vaqtinchalik: transkript yo'q, repo dagi .claude/usage ga yozilmaydi.
    """
    store = os.path.join(tmp, "st_jim")
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "usage.py"), "--saqlash"],
        capture_output=True, text=True, cwd=tmp, input="",
        env=hermetic_env(tmp, USAGE_STORE=store))
    return (proc.returncode == 0 and proc.stdout.strip() == ""
            and not os.path.exists(store))


CASES = [
    ("narx har maydon uchun alohida", case_narx_maydon_boyicha),
    ("kesh o'qish narxi modelga xos", case_kesh_oqish_modelga_xos),
    ("1 soatlik keshga yozish 2x", case_kesh_yozish_1_soat),
    ("sonnet-5 narxi", case_sonnet_5_narxi),
    ("1 soatlik kesh yozuvi yig'iladi", case_kesh_1_soat_yigiladi),
    ("noma'lum model nol emas", case_noma_lum_model_nol_emas),
    ("nol tokenli model narxsiz emas", case_nol_token_narxsiz_emas),
    ("eng uzun model kaliti tanlanadi", case_eng_uzun_kalit),
    ("asosiy sessiya alohida", case_asosiy_sessiya),
    ("aktyor parentUuid bo'yicha", case_aktyor_parent_boyicha),
    ("zanjir davomi shu aktyorga", case_zanjir_davomi),
    ("tartib bo'yicha aniqlanishi aytiladi", case_tartib_boyicha_belgilanadi),
    ("ikki aktyor aralashmaydi", case_ikki_aktyor_aralashmaydi),
    ("subagent aktyori meta dan", case_subagent_meta_dan),
    ("workflow bosqichi ajratiladi", case_workflow_bosqichi),
    ("meta yo'q subagent asosiyga tushmaydi", case_meta_yoq_asosiyga_tushmaydi),
    ("ichma-ich agent olinadi, journal emas", case_transcripts_ichma_ich),
    ("takroriy qator bir marta sanaladi", case_takroriy_qator_bir_marta),
    ("takrordagi Task yo'qolmaydi", case_takrordagi_task_yoqolmaydi),
    ("kun bo'yicha bo'linadi", case_kun_boyicha_bolinadi),
    ("kun mahalliy vaqtda", case_kun_mahalliy_vaqtda),
    ("davr filtri", case_davr_filtri),
    ("narxsiz model belgilanadi", case_narxsiz_belgilanadi),
    ("buzuq qator o'tkaziladi", case_buzuq_qator_otkaziladi),
    ("slug Claude Code bilan bir xil", case_slug_claude_code_bilan_bir_xil),
    ("proyekt papkasi ish papkasidan", case_proyekt_papkasi_topiladi),
    ("--saqlash fayl yozadi", case_saqlash_fayl_yozadi),
    ("qayta saqlash ikki marta qo'shmaydi", case_saqlash_ikki_marta_qoshmaydi),
    ("ikki sessiya bir-birini bosmaydi", case_ikki_sessiya_bosmaydi),
    ("hook payloaddagi sessiyani yozadi", case_saqlash_hook_payload),
    ("--saqlash jim va 0 qaytaradi", case_saqlash_hook_jim),
]


def main():
    tmp = tempfile.mkdtemp(prefix="usage_")
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
