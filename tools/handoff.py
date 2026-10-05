#!/usr/bin/env python3
"""Sessiya kontekstini o'lchaydi va yangi sessiya uchun prompt beradi.

    python3 tools/handoff.py              # o'lchov va tavsiya
    python3 tools/handoff.py --prompt     # yangi sessiya uchun tayyor matn
    python3 tools/handoff.py --limit 400000
    python3 tools/handoff.py --hook       # UserPromptSubmit hooki

Nega o'lchov kerak: kontekst to'lganini hech kim sezmaydi. Javoblar
sekinlashadi, eski tafsilot yangisini siqib chiqaradi, va buni faqat
natija yomonlashgandan keyin bilib olinadi. Shuning uchun bu yerda
taxmin emas, transkriptdagi haqiqiy raqam o'qiladi: har javobning
`usage` yozuvida kontekst hajmi turadi.

Oyna hajmi CONTEXT_LIMIT, autoCompactWindow sozlamasi yoki model
jadvalidan olinadi; auto siqish bo'lgan bo'lsa o'sha nuqtadan. Manual
/compact chegara bermaydi: u foydalanuvchi tanlagan payt, oyna emas.

Transkript klondan emas, sessiyadan topiladi: global o'rnatishda asbob
bitta papkada turadi, ish esa boshqa proyektda yuradi. Avval
CLAUDE_CODE_SESSION_ID, keyin proyekt papkasi (CLAUDE_PROJECT_DIR, joriy
papka va uning otalari, oxirida klon).
"""

import glob
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, ".claude", ".state", "handoff.json")

# Shu nisbatdan keyin yangi sessiya tavsiya qilinadi. 0.75 tanlangan:
# qolgan chorak ishni yakunlab, topshiriqni yozishga yetadi.
WARN_RATIO = 0.75

# Hook ikkinchi marta shu nisbatda aytadi: auto siqish yaqin qoldi.
CRITICAL_RATIO = 0.9

# Shu hajmdan keyin har navbat shuncha tokenni keshdan qayta o'qiydi:
# oyna to'lmagan bo'lsa ham ish tugagan joyda yangi sessiya arzonroq.
# CONTEXT_WARN bilan o'zgartiriladi.
ECONOMY_TOKENS = 400000

# Model oynasi. Haiku 200K, qolganlari 1M.
SMALL_WINDOW = 200000
LARGE_WINDOW = 1000000

# Hook bir sessiyaga bir pog'onani bir marta aytadi, yozuv shuncha saqlanadi.
STATE_MAX_AGE = 7 * 24 * 3600


def env_int(name):
    """Musbat butun son yoki 0. Har chaqiruvda o'qiladi, import paytida emas."""
    value = os.environ.get(name, "").strip()
    return int(value) if value.isdigit() else 0


def economy_tokens():
    return env_int("CONTEXT_WARN") or ECONOMY_TOKENS


def project_slug(path):
    """Claude Code transkript papkasining nomi: harf-raqamdan boshqasi `-`."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def config_dir():
    """Claude Code sozlama papkasi: CLAUDE_CONFIG_DIR yoki ~/.claude."""
    return (os.environ.get("CLAUDE_CONFIG_DIR")
            or os.path.join(os.path.expanduser("~"), ".claude"))


def projects_root():
    return os.path.join(config_dir(), "projects")


def candidates():
    """Proyekt papkasiga nomzodlar: sessiya bergan, joriy va otalari, klon."""
    out = []
    given = os.environ.get("CLAUDE_PROJECT_DIR")
    if given:
        out.append(os.path.abspath(given))
    try:
        path = os.path.abspath(os.getcwd())
    except OSError:
        path = ROOT
    while True:
        out.append(path)
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    out.append(ROOT)
    return out


def slug_dir(path):
    """Shu proyektning transkript papkasi, yo'q bo'lsa None."""
    root = projects_root()
    slug = project_slug(path)
    exact = os.path.join(root, slug)
    if os.path.isdir(exact):
        return exact
    if len(slug) > 200:
        # Uzun nomni Claude Code kesadi: `<200 belgi>-<hash>`.
        found = sorted(f for f in glob.glob(
            os.path.join(root, glob.escape(slug[:200]) + "-*"))
            if os.path.isdir(f))
        if found:
            return found[0]
    return None


def locate():
    """(proyekt papkasi, transkript papkasi yoki None)."""
    options = candidates()
    for path in options:
        base = slug_dir(path)
        if base:
            return path, base
    return options[0], None


def project_dir():
    return locate()[0]


def project_base():
    return locate()[1]


def top_level(base):
    return [os.path.join(base, f) for f in os.listdir(base)
            if f.endswith(".jsonl")]


def transcript():
    """Joriy sessiya transkripti, aniqlanmasa proyektning eng yangisi."""
    base = project_base()
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID", "").strip()
    if sid and os.path.basename(sid) == sid:
        if base and os.path.isfile(os.path.join(base, sid + ".jsonl")):
            return os.path.join(base, sid + ".jsonl")
        found = glob.glob(os.path.join(projects_root(), "*",
                                       glob.escape(sid) + ".jsonl"))
        if found:
            return found[0]
    if not base:
        return None
    files = top_level(base)
    return max(files, key=os.path.getmtime) if files else None


def context_size(usage):
    return (usage.get("input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0))


def main_message(row):
    """Asosiy sessiya javobining message qismi, aks holda None.

    Subagent qatorlari (`isSidechain`) boshqa kontekst va boshqa model:
    ular asosiy sessiya o'lchoviga aralashmaydi.
    """
    if not isinstance(row, dict) or row.get("isSidechain"):
        return None
    message = row.get("message")
    if not isinstance(message, dict) or not message.get("usage"):
        return None
    return message


def measure(path):
    """current, peak, auto siqish nuqtasi, siqish, javob soni, model.

    Bitta siqish transkriptda ikki qator: `compact_boundary` (bunda
    `compactMetadata`) va undan keyin `isCompactSummary`. Chegara sanaladi,
    unga ergashgan xulosa sanalmaydi; chegarasiz yolg'iz xulosa (eski
    format) baribir bitta siqish. Bitta javob bir nechta qatorga bo'linadi
    (har content block alohida), shuning uchun javob `message.id` bo'yicha.
    """
    current = peak = before_auto = compacts = turns = 0
    model = ""
    seen_ids = set()
    boundary = False
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if not isinstance(row, dict):
                continue
            meta = row.get("compactMetadata")
            if meta or row.get("subtype") == "compact_boundary":
                compacts += 1
                boundary = True
                meta = meta if isinstance(meta, dict) else {}
                if meta.get("trigger") == "auto":
                    pre = meta.get("preTokens")
                    before_auto = pre if isinstance(pre, int) and pre > 0 else peak
                continue
            if row.get("isCompactSummary"):
                if not boundary:
                    compacts += 1
                boundary = False
                continue
            message = main_message(row)
            if not message:
                continue
            msg_id = message.get("id")
            if not msg_id or msg_id not in seen_ids:
                turns += 1
                if msg_id:
                    seen_ids.add(msg_id)
            size = context_size(message["usage"])
            current = size or current
            peak = max(peak, size)
            if size and not str(message.get("model", "")).startswith("<"):
                model = message.get("model") or model
    return current, peak, before_auto, compacts, turns, model


def settings_window():
    """autoCompactWindow: global va proyekt sozlamasidagi eng kichigi, 0."""
    project = project_dir()
    paths = (os.path.join(config_dir(), "settings.json"),
             os.path.join(project, ".claude", "settings.json"),
             os.path.join(project, ".claude", "settings.local.json"))
    values = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            continue
        value = data.get("autoCompactWindow") if isinstance(data, dict) else None
        # "auto" va obyekt shakli oyna hajmini aytmaydi.
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            values.append(value)
    return min(values) if values else 0


def limit_for(before_auto, model, override):
    """(chegara, manbasi). Aniq berilgani o'lchangandan, u jadvaldan ustun."""
    if override:
        return override, "berilgan (--limit)"
    for name in ("CONTEXT_LIMIT", "CLAUDE_CODE_AUTO_COMPACT_WINDOW"):
        value = env_int(name)
        if value:
            return value, name
    value = settings_window()
    if value:
        return value, "autoCompactWindow sozlamasi"
    if before_auto:
        return before_auto, "o'lchangan (auto siqish nuqtasi)"
    window = SMALL_WINDOW if "haiku" in (model or "") else LARGE_WINDOW
    return window, "model jadvali (%s)" % (model or "noma'lum")


def git(*args):
    try:
        out = subprocess.run(["git"] + list(args), capture_output=True,
                             text=True, cwd=project_dir(), timeout=20)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def memory_slug():
    """memory/README.md qoidasi: GitHub repo nomi, yo'q bo'lsa ildiz papka."""
    url = git("remote", "get-url", "origin")
    name = re.split(r"[/:]", url.rstrip("/"))[-1] if url else ""
    if name.endswith(".git"):
        name = name[:-4]
    if not name:
        top = git("rev-parse", "--show-toplevel") or project_dir()
        name = os.path.basename(top.rstrip("/\\"))
    return name.lower()


def memory_lines():
    """Memory klonda turadi; boshqa proyektdan chaqirilsa yo'l to'liq."""
    out = []
    here = os.path.normcase(project_dir()) == os.path.normcase(ROOT)
    for slug in dict.fromkeys((memory_slug(), "umumiy")):
        rel = "memory/%s/MEMORY.md" % slug
        path = os.path.join(ROOT, rel)
        if os.path.isfile(path):
            out.append(rel if here else path.replace(os.sep, "/"))
    return out


def report(override):
    path = transcript()
    if not path:
        print("Transkript topilmadi, kontekst o'lchanmadi.")
        print("Tavsiya faqat o'lchovga tayanadi, shuning uchun berilmaydi.")
        return 2
    current, peak, before, compacts, turns, model = measure(path)
    limit, source = limit_for(before, model, override)
    ratio = current / limit if limit else 0

    print("Kontekst: %s / %s token (%.0f%%)"
          % (f"{current:,}", f"{limit:,}", 100 * ratio))
    print("  chegara manbasi : %s" % source)
    print("  eng katta       : %s" % f"{peak:,}")
    print("  siqish (compact): %d" % compacts)
    print("  javob soni      : %d" % turns)

    print()
    if compacts:
        print("TAVSIYA: yangi sessiya. Bu sessiya allaqachon %d marta "
              "siqilgan," % compacts)
        print("ya'ni tafsilot yo'qolgan. Yangi sessiya topshiriq bilan "
              "aniqroq boshlaydi.")
    elif ratio >= WARN_RATIO:
        print("TAVSIYA: yangi sessiya. Kontekst %.0f%% to'lgan, qolgani "
              "ishni" % (100 * ratio))
        print("yakunlab topshiriq yozishga yetadi, yangi katta ishga emas.")
    elif current >= economy_tokens():
        print("TAVSIYA: yangi sessiya. Kontekst %dK token: har navbat shuni "
              "keshdan qayta o'qiydi," % (current // 1000))
        print("ish tugagan joyda yangi sessiya arzonroq.")
    else:
        print("TAVSIYA: davom etish. Kontekstda joy bor.")
    print("\nTayyor prompt: python3 tools/handoff.py --prompt")
    return 0


def prompt(override):
    path = transcript()
    current = limit = 0
    source = "o'lchanmagan"
    if path:
        current, _, before, _, _, model = measure(path)
        limit, source = limit_for(before, model, override)

    branch = git("rev-parse", "--abbrev-ref", "HEAD") or "?"
    commits = git("log", "--oneline", "-5")
    dirty = git("status", "--short")

    print("# Yangi sessiya uchun prompt: pastdagini nusxalab yuboring\n")
    print("```")
    print("/manguberdi")
    print()
    print("Oldingi sessiya kontekstga sig'may uzatildi"
          + (" (%s / %s token, %s)" % (f"{current:,}", f"{limit:,}", source)
             if current else "") + ".")
    print()
    print("Maqsad: <bir jumla, tekshirib bo'ladigan>")
    print()
    print("Bajarildi:")
    print("  <qadam>   <- har biri bir qator")
    print()
    print("Qolgan:")
    print("  <qadam>")
    print()
    print("Qarorlar: <qaror> (<hujjat> <raqam>), nega shunday tanlangan")
    print()
    print("Keyingi qadam: <aniq birinchi harakat>")
    print()
    print("Mashina bergan holat, to'ldirish shart emas:")
    print("  branch: %s" % branch)
    if commits:
        print("  oxirgi commitlar:")
        for line in commits.split("\n"):
            print("    %s" % line)
    print("  ishchi daraxt: %s"
          % ("toza" if not dirty else "%d fayl o'zgargan" % len(dirty.split("\n"))))
    for rel in memory_lines():
        print("  memory indeksi: %s" % rel)
    print("```")
    print("\n`<...>` ichidagi joylarni to'ldiring: faqat siz bilasiz. "
          "Qolganini mashina yozdi.")
    print("Topshiriqni saqlash: manguberdi skillining "
          "`references/kontekst.md`, \"Kontekst to'lsa\" bo'limi.")
    return 0


def tail_facts(path, nbytes=524288):
    """Oxirgi javobning (kontekst, model). Transkript o'nlab MB bo'ladi,
    hook esa har so'rovda ishlaydi, shuning uchun faqat fayl oxiri o'qiladi.
    """
    with open(path, "rb") as handle:
        handle.seek(0, os.SEEK_END)
        handle.seek(max(0, handle.tell() - nbytes))
        data = handle.read()
    for line in reversed(data.decode("utf-8", "replace").splitlines()):
        try:
            message = main_message(json.loads(line))
        except ValueError:
            continue
        size = context_size(message["usage"]) if message else 0
        if size:
            return size, message.get("model") or ""
    return 0, ""


def load_state():
    try:
        with open(STATE, encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(data):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle)
    os.replace(tmp, STATE)


def hook():
    """UserPromptSubmit: chegaradan oshganda modelga bir qator aytadi.

    Hook navbatni hech qachon buzmaydi: har qanday xatoda jim 0. Bir
    pog'ona bir sessiyaga bir marta aytiladi, har navbatda takrorlanib
    tarixda to'planmaydi.
    """
    try:
        return _hook()
    except Exception:  # noqa: BLE001 - hook yiqilsa navbat to'xtamasin
        return 0


def _hook():
    if sys.stdin.isatty():
        return 0
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return 0
    if not isinstance(payload, dict):
        return 0
    path = payload.get("transcript_path") or transcript()
    if not path or not os.path.isfile(path):
        return 0
    current, model = tail_facts(path)
    if not current:
        return 0
    limit, _ = limit_for(0, model, 0)
    if current >= CRITICAL_RATIO * limit:
        level = 2
    elif current >= min(WARN_RATIO * limit, economy_tokens()):
        level = 1
    else:
        return 0

    sid = str(payload.get("session_id") or os.path.basename(path))
    now = time.time()
    state = {key: value for key, value in load_state().items()
             if isinstance(value, list) and len(value) == 2
             and all(isinstance(v, (int, float)) for v in value)
             and now - value[1] < STATE_MAX_AGE}
    if sid in state and state[sid][0] >= level:
        return 0
    state[sid] = [level, now]
    save_state(state)

    script = os.path.join(ROOT, "tools", "handoff.py").replace(os.sep, "/")
    text = ("Kontekst %dK / %dK token (%d%%). Ishni yakunlab, python3 \"%s\" "
            "--prompt bilan yangi sessiyaga uzating."
            % (current // 1000, limit // 1000, 100 * current // limit, script))
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": text}}, ensure_ascii=False))
    return 0


def main():
    args = sys.argv[1:]
    if "--hook" in args:
        return hook()
    override = 0
    if "--limit" in args:
        index = args.index("--limit")
        if index + 1 < len(args) and args[index + 1].isdigit():
            override = int(args[index + 1])
    if "--prompt" in args:
        return prompt(override)
    return report(override)


if __name__ == "__main__":
    sys.exit(main())
