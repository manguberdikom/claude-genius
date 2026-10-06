#!/usr/bin/env python3
"""Sessiya kontekstini o'lchaydi va yangi sessiya uchun prompt beradi.

    python3 tools/handoff.py              # o'lchov va tavsiya
    python3 tools/handoff.py --prompt     # yangi sessiya uchun tayyor matn
    python3 tools/handoff.py --prompt --vazifa <nom>   # topshiriq faylga
    python3 tools/handoff.py --memory     # ikki MEMORY.md indeksi, ish boshida
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
CLAUDE_AUTOCOMPACT_PCT_OVERRIDE oynaning shu foizida siqadi, shuning
uchun chegara o'sha nuqtaga tushiriladi (PL-CC8).

Transkript klondan emas, sessiyadan topiladi: global o'rnatishda asbob
bitta papkada turadi, ish esa boshqa proyektda yuradi. Avval
CLAUDE_CODE_SESSION_ID, keyin proyekt papkasi (CLAUDE_PROJECT_DIR, joriy
papka va uning otalari, oxirida klon).

Topshiriqning fakt qismi (branch, commitlar, `git diff --stat HEAD`,
kuzatilmagan fayllar, REJA.md dagi `[x]` va `[ ]` qadamlar) mashinadan
olinadi; model faqat Maqsad, Qarorlar va Keyingi qadamni yozadi
(OK-O17). `--vazifa` bilan topshiriq faylga yoziladi: lokal sessiyada
holat papkasining `handoff/` iga, git siz; bulut sessiyasida
(CLAUDE_CODE_REMOTE) proyekt memorysiga, chunki konteyner qaytarib
olinadi. Proyekt memorysi joyi docref.memory_dir da (R0.5).
"""

import glob
import json
import os
import re
import subprocess
import sys
import time

import hookio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# Claude Code o'zi oynaning shu foizida siqadi (1M modelda ~967K).
# CLAUDE_AUTOCOMPACT_PCT_OVERRIDE faqat undan kichik bo'lsa chegarani
# o'zgartiradi: kattasi baribir shu nuqtada siqiladi.
DEFAULT_COMPACT_PCT = 96.7

# Hook bir sessiyaga bir pog'onani bir marta aytadi, yozuv shuncha saqlanadi.
STATE_MAX_AGE = 7 * 24 * 3600

# Topshiriqdagi fakt ro'yxatlari shuncha qatorda kesiladi: uzun
# topshiriq yangi sessiyani ham to'ldiradi.
FACT_LINES = 15


def env_int(name):
    """Musbat butun son yoki 0. Har chaqiruvda o'qiladi, import paytida emas."""
    value = os.environ.get(name, "").strip()
    return int(value) if value.isdigit() else 0


def state_dir():
    """Holat papkasi: GENIUS_STATE_DIR (budget.py, state.py bilan bir xil),
    aks holda klondagi `.claude/.state`. Har chaqiruvda o'qiladi."""
    return (os.environ.get("GENIUS_STATE_DIR")
            or os.path.join(ROOT, ".claude", ".state"))


def state_path():
    return os.path.join(state_dir(), "handoff.json")


def remote_session():
    """Bulut sessiyasi: konteyner qaytarib olinadi, lokal fayl yo'qoladi."""
    return os.environ.get("CLAUDE_CODE_REMOTE", "").strip().lower() == "true"


def compact_pct():
    """CLAUDE_AUTOCOMPACT_PCT_OVERRIDE (1-100), sukutdan kichik bo'lsa, aks
    holda 0. Kasr ham qabul qilinadi."""
    try:
        value = float(os.environ.get("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE", "").strip())
    except ValueError:
        return 0
    return value if 0 < value < DEFAULT_COMPACT_PCT else 0


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


def window_for(before_auto, model, override):
    """(chegara, manbasi, oynami). Aniq berilgani o'lchangandan, u
    jadvaldan ustun. `oynami` False bo'lsa qiymat allaqachon siqish
    nuqtasi yoki foydalanuvchi bergan chegara: foiz unga qo'llanmaydi."""
    if override:
        return override, "berilgan (--limit)", False
    value = env_int("CONTEXT_LIMIT")
    if value:
        return value, "CONTEXT_LIMIT", False
    value = env_int("CLAUDE_CODE_AUTO_COMPACT_WINDOW")
    if value:
        return value, "CLAUDE_CODE_AUTO_COMPACT_WINDOW", True
    value = settings_window()
    if value:
        return value, "autoCompactWindow sozlamasi", True
    if before_auto:
        return before_auto, "o'lchangan (auto siqish nuqtasi)", False
    window = SMALL_WINDOW if "haiku" in (model or "") else LARGE_WINDOW
    return window, "model jadvali (%s)" % (model or "noma'lum"), True


def limit_for(before_auto, model, override):
    """(chegara, manbasi). Oynaga CLAUDE_AUTOCOMPACT_PCT_OVERRIDE
    qo'llanadi: siqish oyna oxirida emas, shu foizda bo'ladi."""
    value, source, is_window = window_for(before_auto, model, override)
    pct = compact_pct() if is_window else 0
    if pct:
        value = int(value * pct / 100)
        source += ", CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=%g%%" % pct
    return value, source


def git(*args):
    try:
        out = subprocess.run(["git"] + list(args), capture_output=True,
                             text=True, cwd=project_dir(), timeout=20)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def in_git(path):
    """Papka git ishchi daraxti ichidami."""
    try:
        out = subprocess.run(["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
                             capture_output=True, text=True, timeout=20)
        return out.returncode == 0 and out.stdout.strip() == "true"
    except (OSError, subprocess.SubprocessError):
        return False


def memory_slug():
    """memory/README.md qoidasi (docref.project_slug, rules_for bilan bitta):
    repo nomi, ikki egada bir xil nom bo'lsa `<egasi>__<repo>`."""
    try:
        from docref import project_slug
        return project_slug(cwd=project_dir())
    except (ImportError, SyntaxError, OSError):
        url = git("remote", "get-url", "origin")
        name = re.split(r"[/:]", url.rstrip("/"))[-1] if url else ""
        name = name[:-4] if name.endswith(".git") else name
        if not name:
            top = git("rev-parse", "--show-toplevel") or project_dir()
            name = os.path.basename(top.rstrip("/\\"))
        return name.lower()


def same_path(a, b):
    return (os.path.normcase(os.path.realpath(a))
            == os.path.normcase(os.path.realpath(b)))


def show_path(path):
    """Klon ichida ishlaganda klondagi fayl nisbiy, qolgani to'liq, `/` bilan."""
    if same_path(project_dir(), ROOT):
        try:
            rel = os.path.relpath(path, ROOT)
        except ValueError:
            rel = ".."   # Windows: boshqa disk
        if not rel.startswith(".."):
            return rel.replace(os.sep, "/")
    return path.replace(os.sep, "/")


def memory_paths():
    """[(slug, MEMORY.md yo'li)]: proyektniki va `umumiy`. Proyekt papkasi
    klonda faqat klonning o'zi uchun, boshqa proyektda GENIUS_MEMORY_DIR
    (docref.memory_dir, R0.5). docref yuklanmasa bo'sh ro'yxat."""
    try:
        from docref import memory_dir
    except (ImportError, SyntaxError):
        return []
    here = project_dir()
    return [(slug, os.path.join(memory_dir(slug, cwd=here), "MEMORY.md"))
            for slug in dict.fromkeys((memory_slug(), "umumiy"))]


def memory_lines():
    """Mavjud MEMORY.md indekslari, ko'rsatiladigan shaklda."""
    return [show_path(path) for _, path in memory_paths() if os.path.isfile(path)]


def memory_report():
    """--memory: ish boshida o'qiladigan ikki indeks bitta chaqiruvda.

    Ikki Read o'rniga bitta buyruq, va klondan tashqaridagi papka uchun
    ruxsat so'rovi yo'q. Yo'q indeks to'siq emas: memory hali yozilmagan.
    """
    paths = memory_paths()
    if not paths:
        print("docref.py yuklanmadi: memory joyi aniqlanmadi.")
        return 2
    for slug, path in paths:
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = handle.read().rstrip("\n")
        except OSError:
            print("## %s\n(yo'q: `%s` uchun memory hali yozilmagan)\n"
                  % (show_path(path), slug))
            continue
        print("## %s\n\n%s\n" % (show_path(path), text))
    print("Topic fayl indeksdagi tavsifga qarab, faqat keragi o'qiladi. "
          "Yozish qoidasi: %s" % show_path(os.path.join(ROOT, "memory", "README.md")))
    return 0


# REJA.md dagi qadam: `### [x] 1-qadam. ...` sarlavha yoki `- [x] ...` band.
PLAN_HEAD_RE = re.compile(r"^#{2,6}\s+(?:\[([ xX])\]\s+)?(\d+-qadam\..*)$")
PLAN_ITEM_RE = re.compile(r"^\s*[-*+]\s+\[([ xX])\]\s+(.+)$")


def plan_steps():
    """(bajarilgan, qolgan) qadamlar. rejalashtiruvchi rejani proyekt
    ildizidagi REJA.md ga yozadi, bir nechta bo'lsa `reja/<slug>-reja.md`
    ga; bajarilgan qadam oldiga `[x]` qo'yiladi."""
    top = git("rev-parse", "--show-toplevel") or project_dir()
    files = [os.path.join(top, "REJA.md")]
    files += sorted(glob.glob(os.path.join(glob.escape(top), "reja", "*-reja.md")))
    done, left = [], []
    for path in files:
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                lines = handle.read().split("\n")
        except OSError:
            continue
        mark = "" if path == files[0] else " (%s)" % os.path.relpath(path, top)
        for line in lines:
            match = PLAN_HEAD_RE.match(line) or PLAN_ITEM_RE.match(line)
            if match:
                text = match.group(2).strip() + mark
                (done if (match.group(1) or " ") in "xX" else left).append(text)
    return done, left


def short_list(items, limit=FACT_LINES):
    if len(items) <= limit:
        return items
    return items[:limit] + ["... yana %d ta" % (len(items) - limit)]


def facts():
    """Topshiriqning mashina biladigan qismi: model uni qo'lda yozmaydi."""
    stat = git("diff", "--stat", "HEAD")
    untracked = git("ls-files", "--others", "--exclude-standard")
    done, left = plan_steps()
    return {
        "branch": git("rev-parse", "--abbrev-ref", "HEAD") or "?",
        "commits": [l for l in git("log", "--oneline", "-5").split("\n") if l],
        "stat": [l.strip() for l in stat.split("\n") if l.strip()],
        "untracked": [l for l in untracked.split("\n") if l],
        "done": done,
        "left": left,
    }


def task_name(raw):
    """Fayl nomi uchun: kichik harf, harf-raqam va `-`, 60 belgigacha."""
    name = re.sub(r"[^a-z0-9_-]+", "-", (raw or "").lower()).strip("-_")[:60]
    return name or "vazifa"


def handoff_file(name):
    """(topshiriq fayli, memory ildizi yoki None).

    Lokal sessiyada holat papkasining `handoff/` ida, git siz: fayl shu
    mashinada qoladi va hech qayerga push qilinmaydi. Bulut sessiyasida
    konteyner qaytarib olinadi, shuning uchun proyekt memorysiga
    `project_<vazifa>.md` bo'lib yoziladi; ildizi git ga yozish uchun
    qaytariladi (memory/README.md, `git -C <memory ildizi>`).
    """
    if not remote_session():
        return os.path.join(state_dir(), "handoff", name + ".md"), None
    from docref import memory_dir
    folder = memory_dir(memory_slug(), cwd=project_dir())
    return os.path.join(folder, "project_%s.md" % name), os.path.dirname(folder)


def task_text(fact, measured, name):
    """Topshiriq matni: `<...>` ni model to'ldiradi, qolgani mashinadan."""
    out = ["# Topshiriq: %s" % name, "",
           "Oldingi sessiya kontekstga sig'may uzatildi%s." % measured, "",
           "Maqsad: <bir jumla, tekshirib bo'ladigan>", ""]
    if fact["done"]:
        out.append("Bajarildi (REJA.md dagi [x]):")
        out += ["  %s" % s for s in short_list(fact["done"])]
    else:
        out += ["Bajarildi:", "  <qadam>   <- har biri bir qator"]
    out.append("")
    if fact["left"]:
        out.append("Qolgan (REJA.md):")
        out += ["  %s" % s for s in short_list(fact["left"])]
    else:
        out += ["Qolgan:", "  <qadam>"]
    out += ["", "Qarorlar: <qaror> (<hujjat> <raqam>), nega shunday tanlangan", "",
            "Keyingi qadam: <aniq birinchi harakat>", "",
            "Mashina bergan holat, to'ldirish shart emas:",
            "  branch: %s" % fact["branch"]]
    if fact["commits"]:
        out.append("  oxirgi commitlar:")
        out += ["    %s" % l for l in fact["commits"]]
    if fact["stat"]:
        out.append("  o'zgargan fayllar (git diff --stat HEAD):")
        out += ["    %s" % l for l in short_list(fact["stat"][:-1]) + fact["stat"][-1:]]
    if fact["untracked"]:
        out.append("  yangi fayllar (git da yo'q):")
        out += ["    %s" % l for l in short_list(fact["untracked"])]
    if not fact["stat"] and not fact["untracked"]:
        out.append("  ishchi daraxt: toza")
    for rel in memory_lines():
        out.append("  memory indeksi: %s" % rel)
    return "\n".join(out)


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


def prompt(override, vazifa=None):
    path = transcript()
    measured = ""
    if path:
        current, _, before, _, _, model = measure(path)
        limit, source = limit_for(before, model, override)
        if current:
            measured = " (%s / %s token, %s)" % (f"{current:,}", f"{limit:,}", source)
    name = task_name(vazifa) if vazifa is not None else "<vazifa nomi>"
    text = task_text(facts(), measured, name)

    if vazifa is None:
        print("# Yangi sessiya uchun prompt: pastdagini nusxalab yuboring\n")
        print("```")
        print("/manguberdi\n")
        print(text)
        print("```")
        print("\n`<...>` ichidagi joylarni to'ldiring: faqat siz bilasiz. "
              "Qolganini mashina yozdi.")
        print("Topshiriqni saqlash: manguberdi skillining "
              "`references/kontekst.md`, \"Kontekst to'lsa\" bo'limi.")
        return 0

    target, memory_root = handoff_file(name)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(text + "\n")
    shown = show_path(target)
    print("Topshiriq yozildi: %s" % shown)
    print("Endi faqat `<...>` joylarini to'ldiring (Maqsad, Qarorlar, "
          "Keyingi qadam; reja bo'lmasa Bajarildi va Qolgan), bitta Edit bilan.")
    if memory_root and in_git(memory_root):
        root = memory_root.replace(os.sep, "/")
        print("Bulut sessiyasi: konteyner qaytarib olinadi. Saqlash "
              "memory/README.md, \"Ketma-ketlik\" bo'yicha:")
        print("  git -C \"%s\" add -- \"%s\" && git -C \"%s\" commit -m \"handoff: %s\""
              % (root, target.replace(os.sep, "/"), root, name))
    elif memory_root:
        print("Bulut sessiyasi, lekin %s git da emas: konteyner qaytarilsa "
              "fayl yo'qoladi." % memory_root.replace(os.sep, "/"))
        print("Saqlash kerak bo'lsa GENIUS_MEMORY_DIR ni xususiy git repoga "
              "qo'ying (ochiq klonga emas).")
    else:
        print("Lokal sessiya: fayl git ga kirmaydi va push qilinmaydi.")
    print("\nYangi sessiya uchun prompt:\n")
    print("```")
    print("/manguberdi\n")
    print("Topshiriq: %s faylida. Avval uni o'qing." % shown)
    print("```")
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
        with open(state_path(), encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(data):
    """Atomar yozuv. tmp nomida pid: parallel sessiyalar bir tmp faylga
    yozmaydi (budget.py va usage.py bilan bir xil)."""
    path = state_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = "%s.%d.tmp" % (path, os.getpid())
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle)
    os.replace(tmp, path)


def hook():
    """UserPromptSubmit: chegaradan oshganda modelga bir qator aytadi.

    Hook navbatni hech qachon buzmaydi: har qanday xatoda jim 0. Bir
    pog'ona bir sessiyaga bir marta aytiladi, har navbatda takrorlanib
    tarixda to'planmaydi.
    """
    try:
        return _hook()
    except Exception as exc:  # noqa: BLE001 - hook yiqilsa navbat to'xtamasin
        hookio.fail_open("handoff", exc)   # o'zi hech qachon yiqilmaydi
        return 0


def own_cmd():
    """Shu asbob buyrug'i: klon ichida nisbiy, boshqa proyektda mutlaq va
    GENIUS_PYTHON bilan (docref.tool_cmd). docref yuklanmasa mutlaq yo'l."""
    try:
        from docref import tool_cmd
        return tool_cmd("handoff.py")
    except (ImportError, SyntaxError, OSError):
        script = os.path.join(ROOT, "tools", "handoff.py").replace(os.sep, "/")
        return 'python3 "%s"' % script


def _hook():
    if sys.stdin.isatty():
        return 0
    payload = hookio.read_payload(blank={})
    if payload is None:
        return 0
    if not hookio.active(payload):
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

    text = ("Kontekst %dK / %dK token (%d%%). Ishni yakunlab, %s --prompt "
            "bilan yangi sessiyaga uzating."
            % (current // 1000, limit // 1000, 100 * current // limit, own_cmd()))
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
    if "--memory" in args:
        return memory_report()
    if "--prompt" in args or "--vazifa" in args:
        vazifa = None
        if "--vazifa" in args:
            index = args.index("--vazifa")
            vazifa = args[index + 1] if index + 1 < len(args) else ""
        return prompt(override, vazifa)
    return report(override)


if __name__ == "__main__":
    sys.exit(main())
