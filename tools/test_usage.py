#!/usr/bin/env python3
"""usage.py uchun sinovlar.

    python3 tools/test_usage.py

Aktyorga bo'lish soxta transkript bilan sinaladi. Sabab ochiq: bu
sessiyada bitta ham subagent chaqirilmagan, ya'ni haqiqiy sidechain
ma'lumoti yo'q. Shuning uchun ikkala atributsiya yo'li ham qo'lda
yasalgan qatorlar bilan tekshiriladi: parentUuid zanjiri va tartib.

Narx hisobida eng ko'p uchraydigan xato keshni kirish narxida sanash.
Keshdan o'qish o'n barobar arzon, yozish chorak barobar qimmat: shuning
uchun har bir maydon alohida tekshiriladi.
"""

import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import usage as U  # noqa: E402

DAY = "2026-10-04"


def row(total_read=0, out=0, inp=0, write=0, model="claude-opus-5",
        side=False, uuid=None, parent=None, day=DAY):
    item = {
        "timestamp": "%sT10:00:00.000Z" % day,
        "message": {"model": model, "usage": {
            "input_tokens": inp,
            "cache_creation_input_tokens": write,
            "cache_read_input_tokens": total_read,
            "output_tokens": out}},
    }
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
    with io.open(path, "w", encoding="utf-8") as handle:
        for item in rows:
            handle.write(json.dumps(item) + "\n")


def collect(tmp, rows, name="t.jsonl"):
    path = os.path.join(tmp, name)
    write_jsonl(path, rows)
    return U.collect([path])


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


def case_noma_lum_model_nol_emas():
    """Narxi yo'q model None qaytaradi, nol emas: nol yolg'on son."""
    counts = dict.fromkeys(U.FIELDS, 1000)
    return U.cost("claude-kelajak-9", counts) is None


def case_eng_uzun_kalit():
    """opus-5-5 opus-5 dan ustun: qisqa kalit uzunini yutib ketmasin."""
    return U.price_for("claude-opus-5-5") == (4.0, 20.0) \
        and U.price_for("claude-opus-5") == (5.0, 25.0)


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


def case_kun_boyicha_bolinadi(tmp):
    rows, _ = collect(tmp, [
        row(total_read=100, day="2026-10-03"),
        row(total_read=200, day="2026-10-04"),
    ], "f.jsonl")
    return {k[0] for k in rows} == {"2026-10-03", "2026-10-04"}


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


def case_saqlash_fayl_yozadi(tmp):
    rows, _ = collect(tmp, [
        task_row("arxitektor", "t1"),
        row(total_read=1_000_000, out=1000, side=True, uuid="s1", parent="t1"),
        row(total_read=2_000_000, out=2000),
    ], "j.jsonl")
    saved = os.path.join(tmp, "usage")
    old_store, U.STORE = U.STORE, saved
    try:
        U.save(rows)
        path = os.path.join(saved, "2026-10.json")
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
        U.save(rows)
        U.save(rows)
        data = json.load(io.open(os.path.join(saved, "2026-10.json"),
                                 encoding="utf-8"))
        got = data[DAY][U.MAIN]["tokens"]["cache_read_input_tokens"]
        return got == 1_000_000
    finally:
        U.STORE = old_store


def case_saqlash_hook_jim(tmp):
    """--saqlash hech narsa chiqarmaydi va 0 qaytaradi: Stop hook uchun."""
    proc = __import__("subprocess").run(
        [sys.executable, os.path.join(HERE, "usage.py"), "--saqlash"],
        capture_output=True, text=True, cwd=ROOT)
    return proc.returncode == 0 and proc.stdout.strip() == ""


CASES = [
    ("narx har maydon uchun alohida", case_narx_maydon_boyicha),
    ("noma'lum model nol emas", case_noma_lum_model_nol_emas),
    ("eng uzun model kaliti tanlanadi", case_eng_uzun_kalit),
    ("asosiy sessiya alohida", case_asosiy_sessiya),
    ("aktyor parentUuid bo'yicha", case_aktyor_parent_boyicha),
    ("zanjir davomi shu aktyorga", case_zanjir_davomi),
    ("tartib bo'yicha aniqlanishi aytiladi", case_tartib_boyicha_belgilanadi),
    ("ikki aktyor aralashmaydi", case_ikki_aktyor_aralashmaydi),
    ("kun bo'yicha bo'linadi", case_kun_boyicha_bolinadi),
    ("davr filtri", case_davr_filtri),
    ("narxsiz model belgilanadi", case_narxsiz_belgilanadi),
    ("buzuq qator o'tkaziladi", case_buzuq_qator_otkaziladi),
    ("--saqlash fayl yozadi", case_saqlash_fayl_yozadi),
    ("qayta saqlash ikki marta qo'shmaydi", case_saqlash_ikki_marta_qoshmaydi),
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
