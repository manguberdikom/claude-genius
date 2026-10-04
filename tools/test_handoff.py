#!/usr/bin/env python3
"""handoff.py uchun sinovlar.

    python3 tools/test_handoff.py

Sinovlar soxta transkript bilan ishlaydi, haqiqiysi bilan emas: CI da
transkript yo'q, mahalliy sessiyada esa u har safar boshqacha. Shuning
uchun o'lchov mantig'i shu yerda tekshiriladi, raqam esa emas.
"""

import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import handoff  # noqa: E402


def write_transcript(path, rows):
    with io.open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def usage_row(total, extra=None):
    row = {"message": {"usage": {"input_tokens": 0,
                                 "cache_creation_input_tokens": 0,
                                 "cache_read_input_tokens": total}}}
    if extra:
        row.update(extra)
    return row


def case_olchov(tmp):
    """current oxirgi javobdan, peak eng kattasidan olinadi."""
    path = os.path.join(tmp, "a.jsonl")
    write_transcript(path, [usage_row(100), usage_row(900), usage_row(300)])
    current, peak, before, compacts, turns = handoff.measure(path)
    return (current, peak, before, compacts, turns) == (300, 900, 900, 0, 3)


def case_siqish_sanaladi(tmp):
    path = os.path.join(tmp, "b.jsonl")
    write_transcript(path, [
        usage_row(500), usage_row(800),
        {"isCompactSummary": True},
        usage_row(120),
    ])
    current, peak, before, compacts, _ = handoff.measure(path)
    # Siqishdan keyingi kichik kontekst peak ni pasaytirmaydi, va
    # siqishgacha bo'lgan eng katta alohida saqlanadi: oyna hajmi shu.
    return current == 120 and peak == 800 and before == 800 and compacts == 1


def case_siqishdan_keyingi_peak_hisobga_kirmaydi(tmp):
    path = os.path.join(tmp, "c.jsonl")
    write_transcript(path, [
        usage_row(400),
        {"compactMetadata": {"x": 1}},
        usage_row(950),
    ])
    _, peak, before, compacts, _ = handoff.measure(path)
    return peak == 950 and before == 400 and compacts == 1


def case_chegara_olchangan(_):
    limit, source = handoff.limit_for(800, 1, 0)
    return limit == 800 and "o'lchangan" in source


def case_chegara_taxminiy(_):
    limit, source = handoff.limit_for(0, 0, 0)
    return limit == handoff.DEFAULT_LIMIT and "taxminiy" in source


def case_chegara_berilgan(_):
    limit, source = handoff.limit_for(800, 1, 5000)
    return limit == 5000 and "berilgan" in source


def case_buzuq_qator_otkaziladi(tmp):
    path = os.path.join(tmp, "d.jsonl")
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write("not json\n")
        handle.write(json.dumps(usage_row(250)) + "\n")
    current, _, _, _, turns = handoff.measure(path)
    return current == 250 and turns == 1


def case_usagesiz_qator_sanalmaydi(tmp):
    path = os.path.join(tmp, "e.jsonl")
    write_transcript(path, [{"type": "user"}, usage_row(70), {"type": "x"}])
    _, _, _, _, turns = handoff.measure(path)
    return turns == 1


def case_prompt_transkriptsiz_ishlaydi(_):
    """Transkript topilmasa ham prompt beriladi: git holati baribir bor."""
    saved = handoff.transcript
    handoff.transcript = lambda: None
    try:
        out = io.StringIO()
        stdout, sys.stdout = sys.stdout, out
        try:
            code = handoff.prompt(0)
        finally:
            sys.stdout = stdout
    finally:
        handoff.transcript = saved
    text = out.getvalue()
    return code == 0 and "/manguberdi" in text and "branch:" in text


def case_hisobot_transkriptsiz_tavsiya_bermaydi(_):
    """O'lchov yo'q bo'lsa tavsiya ham yo'q: taxmin qilinmaydi."""
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "handoff.py")],
        capture_output=True, text=True, cwd=ROOT,
        env=dict(os.environ, HOME=tempfile.mkdtemp(prefix="bosh_uy_")))
    return proc.returncode == 2 and "topilmadi" in proc.stdout


CASES = [
    ("current, peak va navbat soni", case_olchov),
    ("siqish sanaladi", case_siqish_sanaladi),
    ("siqishdan keyingi peak oyna emas",
     case_siqishdan_keyingi_peak_hisobga_kirmaydi),
    ("chegara o'lchangan", case_chegara_olchangan),
    ("chegara taxminiy deb belgilanadi", case_chegara_taxminiy),
    ("--limit ustun turadi", case_chegara_berilgan),
    ("buzuq qator o'tkaziladi", case_buzuq_qator_otkaziladi),
    ("usage'siz qator sanalmaydi", case_usagesiz_qator_sanalmaydi),
    ("transkriptsiz prompt beriladi", case_prompt_transkriptsiz_ishlaydi),
    ("transkriptsiz tavsiya berilmaydi",
     case_hisobot_transkriptsiz_tavsiya_bermaydi),
]


def main():
    tmp = tempfile.mkdtemp(prefix="handoff_")
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn(tmp))
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
