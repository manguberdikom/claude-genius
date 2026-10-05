#!/usr/bin/env python3
"""handoff.py uchun sinovlar.

    python3 tools/test_handoff.py

Sinovlar soxta transkript bilan ishlaydi, haqiqiysi bilan emas: CI da
transkript yo'q, mahalliy sessiyada esa u har safar boshqacha. Shuning
uchun o'lchov mantig'i shu yerda tekshiriladi, raqam esa emas. Uy papkasi
va muhit har sinovda soxta: haqiqiy sozlama va transkript aralashmaydi.
"""

import contextlib
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

import handoff  # noqa: E402

# Natijaga ta'sir qiladigan muhit. Sinov ichida tozalanadi va tiklanadi.
ENV_KEYS = ("CONTEXT_LIMIT", "CLAUDE_CODE_AUTO_COMPACT_WINDOW", "CONTEXT_WARN",
            "CLAUDE_PROJECT_DIR", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CONFIG_DIR",
            "HOME", "USERPROFILE")


def write_transcript(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def usage_row(total, extra=None, model=None, msg_id=None):
    message = {"usage": {"input_tokens": 0,
                         "cache_creation_input_tokens": 0,
                         "cache_read_input_tokens": total}}
    if model:
        message["model"] = model
    if msg_id:
        message["id"] = msg_id
    row = {"message": message}
    if extra:
        row.update(extra)
    return row


def boundary(trigger, pre=None):
    """Haqiqiy siqishning birinchi qatori."""
    meta = {"trigger": trigger}
    if pre is not None:
        meta["preTokens"] = pre
    return {"type": "system", "subtype": "compact_boundary", "uuid": "b",
            "compactMetadata": meta}


SUMMARY = {"type": "user", "parentUuid": "b", "isCompactSummary": True}


@contextlib.contextmanager
def isolated(tmp, name, **env):
    """Soxta uy va proyekt papkasi; muhit va joriy papka oxirida tiklanadi."""
    home = os.path.join(tmp, name, "uy")
    project = os.path.join(tmp, name, "my_proj.v2")
    os.makedirs(home, exist_ok=True)
    os.makedirs(project, exist_ok=True)
    saved = {key: os.environ.get(key) for key in ENV_KEYS + tuple(env)}
    cwd = os.getcwd()
    for key in ENV_KEYS:
        os.environ.pop(key, None)
    os.environ["HOME"] = os.environ["USERPROFILE"] = home
    os.environ.update(env)
    os.chdir(project)
    try:
        yield home, project
    finally:
        os.chdir(cwd)
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def projects_dir(home, project):
    return os.path.join(home, ".claude", "projects",
                        handoff.project_slug(project))


def case_olchov(tmp):
    """current oxirgi javobdan, peak eng kattasidan olinadi."""
    path = os.path.join(tmp, "a.jsonl")
    write_transcript(path, [usage_row(100), usage_row(900),
                            usage_row(300, model="claude-opus-5")])
    return handoff.measure(path) == (300, 900, 0, 0, 3, "claude-opus-5")


def case_siqish_sanaladi(tmp):
    """Haqiqiy siqish ikki qator, lekin bitta siqish."""
    path = os.path.join(tmp, "b.jsonl")
    write_transcript(path, [
        usage_row(500), usage_row(800),
        boundary("auto", 850), SUMMARY,
        usage_row(120),
    ])
    current, peak, before, compacts, _, _ = handoff.measure(path)
    # Siqishdan keyingi kichik kontekst peak ni pasaytirmaydi, oyna esa
    # siqish yozgan preTokens dan olinadi.
    return current == 120 and peak == 800 and before == 850 and compacts == 1


def case_eski_format_xulosa_sanaladi(tmp):
    """Chegarasiz yolg'iz xulosa ham siqish, lekin oyna hajmini aytmaydi."""
    path = os.path.join(tmp, "b2.jsonl")
    write_transcript(path, [usage_row(500), {"isCompactSummary": True},
                            usage_row(120)])
    _, _, before, compacts, _, _ = handoff.measure(path)
    return compacts == 1 and before == 0


def case_siqishdan_keyingi_peak_hisobga_kirmaydi(tmp):
    """preTokens yo'q bo'lsa siqish nuqtasigacha bo'lgan peak olinadi."""
    path = os.path.join(tmp, "c.jsonl")
    write_transcript(path, [
        usage_row(400),
        {"compactMetadata": {"trigger": "auto"}},
        usage_row(950),
    ])
    _, peak, before, compacts, _, _ = handoff.measure(path)
    return peak == 950 and before == 400 and compacts == 1


def case_manual_siqish_chegara_bermaydi(tmp):
    path = os.path.join(tmp, "c2.jsonl")
    write_transcript(path, [usage_row(700), boundary("manual", 700), SUMMARY,
                            usage_row(90, model="claude-opus-5")])
    _, _, before, compacts, _, model = handoff.measure(path)
    with isolated(tmp, "manual"):
        limit, source = handoff.limit_for(before, model, 0)
    return (before == 0 and compacts == 1 and limit == 1000000
            and "model jadvali" in source)


def case_bir_javob_bir_marta(tmp):
    """Bir xil message.id li qatorlar bitta javob; id siz qator alohida."""
    path = os.path.join(tmp, "f.jsonl")
    write_transcript(path, [usage_row(100, msg_id="m1"),
                            usage_row(100, msg_id="m1"),
                            usage_row(200, msg_id="m2"),
                            usage_row(300)])
    return handoff.measure(path)[4] == 3


def case_subagent_qatori_aralashmaydi(tmp):
    path = os.path.join(tmp, "g.jsonl")
    write_transcript(path, [
        usage_row(500, model="claude-opus-5"),
        usage_row(30, {"isSidechain": True}, model="claude-haiku-4-5"),
    ])
    current, _, _, _, turns, model = handoff.measure(path)
    return current == 500 and turns == 1 and model == "claude-opus-5"


def case_chegara_olchangan(tmp):
    with isolated(tmp, "olchangan"):
        limit, source = handoff.limit_for(800, "claude-opus-5", 0)
    return limit == 800 and "o'lchangan" in source


def case_chegara_model_jadvali(tmp):
    with isolated(tmp, "jadval"):
        opus = handoff.limit_for(0, "claude-opus-5", 0)
        haiku = handoff.limit_for(0, "claude-haiku-4-5", 0)
    return (opus[0] == 1000000 and haiku[0] == 200000
            and "claude-opus-5" in opus[1])


def case_chegara_berilgan(tmp):
    with isolated(tmp, "berilgan", CONTEXT_LIMIT="300000"):
        limit, source = handoff.limit_for(800, "claude-opus-5", 5000)
    return limit == 5000 and "berilgan" in source


def case_env_oyna_ustun(tmp):
    with isolated(tmp, "env", CLAUDE_CODE_AUTO_COMPACT_WINDOW="300000"):
        limit, source = handoff.limit_for(800, "claude-opus-5", 0)
    return limit == 300000 and "AUTO_COMPACT" in source


def case_sozlama_oynasi(tmp):
    """Global va proyekt sozlamasidan eng kichigi; "auto" hisoblanmaydi."""
    with isolated(tmp, "sozlama") as (home, project):
        for path, value in ((os.path.join(home, ".claude", "settings.json"),
                             500000),
                            (os.path.join(project, ".claude",
                                          "settings.local.json"), 300000),
                            (os.path.join(project, ".claude", "settings.json"),
                             "auto")):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with io.open(path, "w", encoding="utf-8") as handle:
                json.dump({"autoCompactWindow": value}, handle)
        limit, source = handoff.limit_for(800, "claude-opus-5", 0)
    return limit == 300000 and "autoCompactWindow" in source


def case_slug(_):
    """Claude Code qoidasi: harf-raqamdan boshqa har belgi `-`."""
    return (handoff.project_slug(r"C:\Users\Ali\my_proj") == "C--Users-Ali-my-proj"
            and handoff.project_slug("/home/a/x.y") == "-home-a-x-y")


def case_sessiya_id_boyicha(tmp):
    """ID berilsa eng yangi fayl emas, aynan shu sessiya olinadi."""
    with isolated(tmp, "sid", CLAUDE_CODE_SESSION_ID="eski") as (home, project):
        base = projects_dir(home, project)
        old = os.path.join(base, "eski.jsonl")
        new = os.path.join(base, "yangi.jsonl")
        write_transcript(old, [usage_row(10)])
        write_transcript(new, [usage_row(20)])
        past = time.time() - 3600
        os.utime(old, (past, past))
        own = handoff.transcript()
        # Boshqa proyekt papkasidagi sessiya ham ID bo'yicha topiladi.
        other = os.path.join(home, ".claude", "projects", "-boshqa", "uzoq.jsonl")
        write_transcript(other, [usage_row(30)])
        os.environ["CLAUDE_CODE_SESSION_ID"] = "uzoq"
        far = handoff.transcript()
        del os.environ["CLAUDE_CODE_SESSION_ID"]
        newest = handoff.transcript()
    return own == old and far == other and newest == new


def case_pastki_papkadan_ota_topiladi(tmp):
    with isolated(tmp, "ota") as (home, project):
        path = os.path.join(projects_dir(home, project), "s.jsonl")
        write_transcript(path, [usage_row(10)])
        sub = os.path.join(project, "src", "main")
        os.makedirs(sub)
        os.chdir(sub)
        found = handoff.transcript()
        where = handoff.project_dir()
    return found == path and where == project


def case_config_dir_hisobga_olinadi(tmp):
    """CLAUDE_CONFIG_DIR berilsa transkript ~/.claude dan emas, shu yerdan."""
    config = os.path.join(tmp, "konfig", "boshqa")
    with isolated(tmp, "konfig", CLAUDE_CONFIG_DIR=config) as (_, project):
        path = os.path.join(config, "projects",
                            handoff.project_slug(project), "k.jsonl")
        write_transcript(path, [usage_row(10)])
        found = handoff.transcript()
    return found == path


def case_hisobot_proyekt_papkasidan(tmp):
    """Klondan tashqaridagi proyektda ham transkript topiladi."""
    home = os.path.join(tmp, "hisobot", "uy")
    project = os.path.join(tmp, "hisobot", "my_proj.v2")
    os.makedirs(project)
    write_transcript(os.path.join(projects_dir(home, project), "a.jsonl"),
                     [usage_row(1500, model="claude-opus-5")])
    env = {k: v for k, v in os.environ.items() if k not in ENV_KEYS}
    env.update(HOME=home, USERPROFILE=home)
    proc = subprocess.run([sys.executable, os.path.join(HERE, "handoff.py")],
                          capture_output=True, text=True, cwd=project, env=env)
    return proc.returncode == 0 and "Kontekst:" in proc.stdout


def case_hisobot_tejamkorlik_tavsiyasi(tmp):
    """Oyna to'lmagan, lekin kontekst katta: yangi sessiya arzonroq."""
    path = os.path.join(tmp, "h.jsonl")
    write_transcript(path, [usage_row(450000, model="claude-opus-5")])
    saved = handoff.transcript
    handoff.transcript = lambda: path
    out = io.StringIO()
    try:
        with isolated(tmp, "tejam"), contextlib.redirect_stdout(out):
            code = handoff.report(0)
    finally:
        handoff.transcript = saved
    return code == 0 and "keshdan qayta o'qiydi" in out.getvalue()


def case_prompt_transkriptsiz_ishlaydi(_):
    """Transkript topilmasa ham prompt beriladi: git holati baribir bor."""
    saved = handoff.transcript
    handoff.transcript = lambda: None
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            code = handoff.prompt(0)
    finally:
        handoff.transcript = saved
    text = out.getvalue()
    return (code == 0 and "/manguberdi" in text and "branch:" in text
            and "\"Kontekst to'lsa\"" in text)


def case_hisobot_transkriptsiz_tavsiya_bermaydi(tmp):
    """O'lchov yo'q bo'lsa tavsiya ham yo'q: taxmin qilinmaydi."""
    home = os.path.join(tmp, "bosh_uy")
    os.makedirs(home)
    env = {k: v for k, v in os.environ.items() if k not in ENV_KEYS}
    env.update(HOME=home, USERPROFILE=home)
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "handoff.py")],
        capture_output=True, text=True, cwd=ROOT, env=env)
    return proc.returncode == 2 and "topilmadi" in proc.stdout


def run_hook(tmp, payload):
    """hook() ni jarayon ichida chaqiradi: (qaytgan kod, stdout)."""
    saved_state, saved_stdin = handoff.STATE, sys.stdin
    handoff.STATE = os.path.join(tmp, "holat", "handoff.json")
    sys.stdin = io.StringIO(payload if isinstance(payload, str)
                            else json.dumps(payload))
    out = io.StringIO()
    try:
        with isolated(tmp, "hook"), contextlib.redirect_stdout(out):
            code = handoff.hook()
    finally:
        handoff.STATE, sys.stdin = saved_state, saved_stdin
    return code, out.getvalue()


def hook_transcript(tmp, name, total, model):
    path = os.path.join(tmp, "hook_tr", name + ".jsonl")
    write_transcript(path, [usage_row(1000, model=model),
                            usage_row(total, model=model)])
    return path


def case_hook(tmp):
    """Pog'ona bir marta aytiladi; kichik kontekst va buzuq kirish jim."""
    small = hook_transcript(tmp, "kichik", 150000, "claude-opus-5")
    big = hook_transcript(tmp, "katta", 450000, "claude-opus-5")
    haiku = hook_transcript(tmp, "haiku", 160000, "claude-haiku-4-5")
    code_a, out_a = run_hook(tmp, {"transcript_path": small, "session_id": "a"})
    code_b, out_b = run_hook(tmp, {"transcript_path": big, "session_id": "b"})
    code_c, out_c = run_hook(tmp, {"transcript_path": big, "session_id": "b"})
    code_d, out_d = run_hook(tmp, {"transcript_path": haiku, "session_id": "d"})
    code_e, out_e = run_hook(tmp, "not json")
    context = ""
    if out_b:
        context = json.loads(out_b)["hookSpecificOutput"]["additionalContext"]
    return (out_a == "" and "--prompt" in context and out_c == ""
            and out_d != "" and out_e == ""
            and {code_a, code_b, code_c, code_d, code_e} == {0})


CASES = [
    ("current, peak, navbat va model", case_olchov),
    ("siqish ikki qator, bitta sanaladi", case_siqish_sanaladi),
    ("eski formatdagi xulosa sanaladi", case_eski_format_xulosa_sanaladi),
    ("siqishdan keyingi peak oyna emas",
     case_siqishdan_keyingi_peak_hisobga_kirmaydi),
    ("manual siqish chegara bermaydi", case_manual_siqish_chegara_bermaydi),
    ("bir javob bir marta sanaladi", case_bir_javob_bir_marta),
    ("subagent qatori aralashmaydi", case_subagent_qatori_aralashmaydi),
    ("chegara o'lchangan", case_chegara_olchangan),
    ("chegara model jadvalidan", case_chegara_model_jadvali),
    ("--limit ustun turadi", case_chegara_berilgan),
    ("CLAUDE_CODE_AUTO_COMPACT_WINDOW ustun", case_env_oyna_ustun),
    ("autoCompactWindow sozlamasi", case_sozlama_oynasi),
    ("proyekt slugi Claude Code qoidasida", case_slug),
    ("sessiya ID bo'yicha tanlanadi", case_sessiya_id_boyicha),
    ("pastki papkadan ota proyekt topiladi",
     case_pastki_papkadan_ota_topiladi),
    ("CLAUDE_CONFIG_DIR hisobga olinadi", case_config_dir_hisobga_olinadi),
    ("klondan tashqari proyektda o'lchaydi", case_hisobot_proyekt_papkasidan),
    ("katta kontekstda tejamkorlik tavsiyasi",
     case_hisobot_tejamkorlik_tavsiyasi),
    ("transkriptsiz prompt beriladi", case_prompt_transkriptsiz_ishlaydi),
    ("transkriptsiz tavsiya berilmaydi",
     case_hisobot_transkriptsiz_tavsiya_bermaydi),
    ("hook: chegara, takror va buzuq kirish", case_hook),
]


def main():
    # realpath: macOS da /tmp havola, os.getcwd() esa haqiqiy yo'l beradi.
    tmp = os.path.realpath(tempfile.mkdtemp(prefix="handoff_"))
    failures = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(tmp))
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
