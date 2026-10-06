#!/usr/bin/env python3
"""Kunlik token sarfi va uni qaysi aktyor sarflagani.

    python3 tools/usage.py                 # bugun (mahalliy sana)
    python3 tools/usage.py --kun 2026-10-04
    python3 tools/usage.py --davr 7        # oxirgi 7 kun
    python3 tools/usage.py --hammasi       # butun tarix
    python3 tools/usage.py --hafta [--json]                 # mediana $/sessiya
    python3 tools/usage.py --sessiya <id|yo'l> [--json]     # bitta sessiya
    python3 tools/usage.py --saqlash       # jim: kunlik yig'mani yozadi
    python3 tools/usage.py --jadval        # narx jadvali

Raqam transkriptdan olinadi, taxmin qilinmaydi: har javobning `usage`
yozuvida to'rtta son turadi va ularning narxi boshqacha. Keshdan o'qish
modelga qarab 10-20 barobar arzon; keshga yozish 5 daqiqalik keshda
chorak barobar, 1 soatlikda 2 barobar qimmat, shuning uchun "token" deb
bitta songa qo'shib yuborish narxni yashiradi. Bitta javob har content
block uchun alohida qatorda bir xil `message.id` bilan takrorlanadi:
har id bir marta, oxirgi qatoridan sanaladi.

Aktyorga bo'lish: subagent `<sessiya>/subagents/**/agent-<id>.jsonl`
da yoziladi, aktyor nomi yonidagi `agent-<id>.meta.json` ning
`agentType` maydonidan olinadi. Meta bo'lmasa eski yo'l: `isSidechain`
qatori oldingi `Task`/`Agent` chaqiruviga `parentUuid` zanjiri bilan,
bo'lmasa tartib bo'yicha bog'lanadi va chiqishda shu aytiladi.

Stop hook faqat joriy sessiyani subagentlari bilan o'qiydi va
`.claude/usage/<oy>/<proyekt-slug>/<sessiya>.json` ga yozadi. Hisobot shu
yig'mani ham o'qiydi: transkript `cleanupPeriodDays` (sukut 30 kun)
dan keyin o'chadi, yig'ma esa qoladi. Transkriptda yo'q (kun, sessiya)
jufti yig'madan olinadi, ikkalasida bor bo'lsa transkript ustun. Stop
hook `async` qilinmaydi: `-p` rejimida va sessiyadan chiqishda fon hooki
o'ldiriladi va oxirgi navbat yozilmay qoladi, 0.1-0.2 s esa sezilmaydi.

Sessiya bloki (`--sessiya`) monitoring, natija o'lchovi emas. Unda faqat
bir ma'noli maydonlar: USD, faol daqiqa (5 daqiqadan qisqa oraliqlar
yig'indisi), tool soni nom bo'yicha, aktyor chaqiruvi soni, guard va
check_code to'siqlari soni. Foydalanuvchi aralashuvi sanalmaydi: yangi
vazifa xabarini aralashuvdan ajratib bo'lmaydi.

Narx jadvali o'zgaradi. U shu faylda ochiq turadi: eskirsa tahrirlanadi,
va noma'lum model jim nolga aylanmaydi, alohida belgilanadi. Model faqat
ANIQ kalit bilan narxlanadi: `claude-opus-5-6` `opus-5` narxini olmaydi,
chunki narx bir oila ichida ham o'zgaradi (Opus 5.5 Opus 5 dan arzon).
Provayder prefiksli id (`us.anthropic.`, `global.`) ham narxsiz: Bedrock
va Vertex narxi mintaqaviy. Narx sahifasi o'zgarsa PRICES, PRICES_AS_OF
va test_usage dagi narx holatlari bitta commitda yangilanadi. Natija
Claude Code `/cost` dan 5-10% kam chiqishi mumkin: fon chaqiruvlari
transkriptga yozilmaydi.

Transkript formati rasmiy shartnoma emas. U o'zgarsa jim nol o'rniga
"FORMAT O'ZGARGAN: <sabab>" chiqadi va kod 3 qaytadi. Hook rejimida sabab
`.claude/.state/format.json` ga yoziladi: hookda stderr hech kimga
ko'rinmaydi.
"""

import argparse
import collections
import datetime
import glob
import json
import os
import re
import statistics
import sys

import geniuslib
import hookio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.environ.get("USAGE_STORE") or os.path.join(
    geniuslib.clone_root(ROOT), ".claude", "usage")
STATE_DIR = geniuslib.state_dir(ROOT)
FORMAT_FILE = "format.json"

# Million token uchun dollar: (kirish, chiqish, keshdan o'qish).
PRICES_AS_OF = "2026-10-05"
PRICES_SOURCE = "https://platform.claude.com/docs/en/about-claude/pricing"
PRICES = {
    "opus-5-5": (4.0, 20.0, 0.20),
    "opus-5": (5.0, 25.0, 0.50),
    "sonnet-5-5": (2.0, 10.0, 0.20),
    "sonnet-5": (2.0, 10.0, 0.20),
    "haiku-4-5": (1.0, 5.0, 0.10),
}
# Keshga yozish kirish narxidan qimmat: 5 daqiqalik va 1 soatlik kesh.
CACHE_WRITE_5M = 1.25
CACHE_WRITE_1H = 2.0

MAIN = "asosiy sessiya"
UNKNOWN = "noma'lum model"

FIELDS = ("input_tokens", "cache_creation_input_tokens",
          "cache_read_input_tokens", "output_tokens")
# cache_creation_input_tokens ichidagi 1 soatlik qism: narxi boshqa.
WRITE_1H = "cache_write_1h"

# Faol vaqt: bundan uzun tanaffusda foydalanuvchi yo'q deb olinadi.
IDLE_GAP = 300
# Sessiya bloki yig'ma faylida shu kalit ostida; kun kalitlari bilan
# aralashmasligi uchun `_` bilan boshlanadi.
BLOCK_KEY = "_sessiya"
# guard.py matcher i (settings.json): shu tool larda PreToolUse to'sig'i
# guard niki. Task/Agent dagi to'siq budget.py niki va sanalmaydi.
GUARD_TOOLS = ("Read", "Bash", "PowerShell")
GUARD_ERROR = re.compile(r"PreToolUse:(%s) hook error" % "|".join(GUARD_TOOLS))


def price_key(model):
    """`claude-opus-5-5-20260101[1m]` -> `opus-5-5`. Boshqa shakl None."""
    text = str(model or "").strip()
    if text.endswith("[1m]"):
        text = text[:-len("[1m]")]
    if not text.startswith("claude-"):
        return None
    return re.sub(r"[-@]\d{8}$", "", text[len("claude-"):]) or None


def price_for(model):
    """(kirish, chiqish, kesh o'qish) narxi yoki None. Faqat aniq kalit."""
    key = price_key(model)
    return PRICES.get(key) if key else None


def cost(model, counts):
    """Dollar. Narxi yo'q model uchun None: nol deb ko'rsatish yolg'on."""
    price = price_for(model)
    if price is None:
        # Nol token har qanday narxda nol (`<synthetic>` javoblari).
        return 0.0 if not any(counts.get(f, 0) for f in FIELDS) else None
    rate_in, rate_out, rate_read = price
    write_1h = counts.get(WRITE_1H, 0)
    write_5m = max(0, counts["cache_creation_input_tokens"] - write_1h)
    return (counts["input_tokens"] * rate_in
            + write_5m * rate_in * CACHE_WRITE_5M
            + write_1h * rate_in * CACHE_WRITE_1H
            + counts["cache_read_input_tokens"] * rate_read
            + counts["output_tokens"] * rate_out) / 1_000_000


def config_dir():
    return (os.environ.get("CLAUDE_CONFIG_DIR")
            or os.path.join(os.path.expanduser("~"), ".claude"))


def slug(path):
    """Claude Code papka nomi: harf va raqamdan boshqa har belgi `-`."""
    return re.sub(r"[^A-Za-z0-9]", "-", path)


def candidates():
    """Proyekt ildizi bo'lishi mumkin bo'lgan papkalar, ustunlik tartibida."""
    out = [os.environ.get("CLAUDE_PROJECT_DIR")]
    try:
        here = os.getcwd()
    except OSError:
        here = ROOT
    while True:
        out.append(here)
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    out.append(ROOT)
    out.append(geniuslib.clone_root(ROOT))
    return [c for c in out if c]


def project_base():
    """Shu proyekt transkriptlari papkasi yoki None.

    Asbob klonining emas, ish papkasining slugi olinadi: global
    o'rnatishda klon bitta, proyekt esa ko'p.
    """
    projects = os.path.join(config_dir(), "projects")
    for candidate in candidates():
        name = slug(os.path.abspath(candidate))
        path = os.path.join(projects, name)
        if os.path.isdir(path):
            return path
        if len(name) > 200 and os.path.isdir(projects):
            # Uzun nomni Claude Code kesadi: `<200 belgi>-<hash>`.
            for entry in sorted(os.listdir(projects)):
                if entry.startswith(name[:200] + "-"):
                    return os.path.join(projects, entry)
    return None


def project_name(base):
    """Yig'madagi proyekt papkasi nomi. Transkript papkasi o'chgan bo'lsa
    yig'mada bor slug izlanadi."""
    if base:
        return os.path.basename(base)
    for candidate in candidates():
        name = slug(os.path.abspath(candidate))
        if glob.glob(os.path.join(glob.escape(STORE), "*", glob.escape(name))):
            return name
    return None


def session_files(main):
    """Sessiya fayli va uning subagentlari (`journal.jsonl` kirmaydi)."""
    pattern = os.path.join(glob.escape(main[:-len(".jsonl")]), "subagents",
                           "**", "agent-*.jsonl")
    return [main] + sorted(glob.glob(pattern, recursive=True))


def mains(base):
    return sorted(glob.glob(os.path.join(glob.escape(base), "*.jsonl")))


def transcripts(base):
    """Proyektdagi barcha sessiyalar, subagentlari bilan."""
    out = []
    for main in mains(base):
        out.extend(session_files(main))
    return out


def meta_actor(path):
    """Subagent aktyori `agent-<id>.meta.json` dan; yo'q yoki buzuq bo'lsa None."""
    try:
        with open(path[:-len(".jsonl")] + ".meta.json", encoding="utf-8") as handle:
            meta = json.load(handle)
    except (OSError, ValueError):
        return None
    if not isinstance(meta, dict):
        return None
    actor = meta.get("agentType")
    if actor == "workflow-subagent":
        # Workflow agentlarining turi bitta, bosqichni description ajratadi.
        phase = str(meta.get("description") or "").split(":")[0]
        return "workflow:" + phase if phase else "workflow"
    return actor or None


def parse_time(stamp):
    try:
        return datetime.datetime.fromisoformat(
            str(stamp or "").replace("Z", "+00:00"))
    except ValueError:
        return None


def day_of(stamp):
    """Mahalliy sana: "bugun" va --davr ham mahalliy sanadan hisoblanadi."""
    moment = parse_time(stamp)
    if moment is None:
        return str(stamp or "")[:10]
    return moment.astimezone().date().isoformat()


def blocks(message):
    content = message.get("content")
    return content if isinstance(content, list) else []


def add(counts, usage):
    for field in FIELDS:
        counts[field] += usage.get(field, 0) or 0
    created = usage.get("cache_creation")
    if isinstance(created, dict):
        counts[WRITE_1H] += created.get("ephemeral_1h_input_tokens", 0) or 0


class Scan:
    """Transkriptni bir o'qishda yig'iladigan sessiya belgilari.

    Format sentineli ham shu yerda: platforma maydon nomini o'zgartirsa
    narx jim nolga yoki 30-60% kamga tushadi, sentinel esa buni aytadi.
    """

    def __init__(self):
        self.assistant = 0      # haqiqiy (synthetic emas) assistant qatorlari
        self.usage = 0          # usage li qatorlar
        self.read_key = 0       # usage da cache_read_input_tokens kaliti bor
        self.stamps = set()
        self.tools = {}         # tool_use id -> nom
        self.actors = {}        # Task/Agent tool_use id -> aktyor
        self.blocked = {"guard": set(), "check_code": set()}

    def problem(self):
        """Format o'zgargan bo'lsa sababi, aks holda None."""
        if self.assistant and not self.usage:
            return ("assistant qatorlari bor (%d), lekin hech birida "
                    "message.usage yo'q" % self.assistant)
        if self.usage and not self.read_key:
            return ("usage bor (%d qator), lekin cache_read_input_tokens "
                    "kaliti hech qayerda yo'q" % self.usage)
        return None

    def active_minutes(self):
        moments = sorted(m for m in (parse_time(s) for s in self.stamps)
                         if m is not None and m.tzinfo is not None)
        total = 0.0
        for left, right in zip(moments, moments[1:]):
            gap = (right - left).total_seconds()
            if gap < IDLE_GAP:
                total += gap
        return round(total / 60, 1)


def result_text(block):
    content = block.get("content")
    if isinstance(content, list):
        return " ".join(str(x.get("text", "")) for x in content
                        if isinstance(x, dict))
    return str(content or "")


def hook_json(text):
    try:
        data = json.loads(text or "")
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def scan_row(scan, row, message, where):
    """Sessiya blokiga kerak belgilar: tool, aktyor, to'siq, vaqt."""
    if row.get("timestamp"):
        scan.stamps.add(row["timestamp"])
    kind = row.get("type")
    if ((kind == "assistant" or message.get("role") == "assistant")
            and message.get("model") != "<synthetic>"):
        scan.assistant += 1
    usage = message.get("usage")
    if usage:
        scan.usage += 1
        if isinstance(usage, dict) and "cache_read_input_tokens" in usage:
            scan.read_key += 1
    for index, block in enumerate(blocks(message)):
        if not isinstance(block, dict):
            continue
        if block.get("type") == "tool_use" and block.get("name"):
            ident = block.get("id") or "%s:%d" % (where, index)
            scan.tools[ident] = block["name"]
            actor = (block.get("input") or {}).get("subagent_type")
            if block["name"] in ("Task", "Agent") and actor:
                scan.actors[ident] = actor
        elif (block.get("type") == "tool_result" and block.get("is_error")
              and GUARD_ERROR.match(result_text(block))):
            scan.blocked["guard"].add(block.get("tool_use_id") or where)
    attachment = row.get("attachment")
    if kind != "attachment" or not isinstance(attachment, dict):
        return
    name = str(attachment.get("hookName") or "")
    event, _, tool = name.partition(":")
    event = attachment.get("hookEvent") or event
    ident = attachment.get("toolUseID") or where
    output = hook_json(attachment.get("stdout"))
    if event == "PreToolUse" and tool in GUARD_TOOLS:
        decision = (output.get("hookSpecificOutput") or {}).get("permissionDecision")
        if decision == "deny":
            scan.blocked["guard"].add(ident)
    elif event == "PostToolUse" and re.search(r"Write|Edit", tool):
        if (output.get("decision") == "block"
                or "block" in str(attachment.get("type") or "")):
            scan.blocked["check_code"].add(ident)


# Hook belgisi qator boshida turadi (attachment.hookName, tool_result
# matni, real transkriptda 251-belgigacha). Butun qatorni uch marta
# qidirish katta tool natijasida Stop hookni sezilarli sekinlashtiradi.
HEAD = 2000
ASSISTANT = re.compile(r'"role":\s*"assistant"')


def worth_parsing(line):
    """Na usage, na tool, na hook belgisi bo'lgan qatorni ochish behuda."""
    if '"usage"' in line or '"tool_use"' in line:
        return True
    head = line[:HEAD]
    return ("hook error" in head or "PostToolUse" in head
            or "permissionDecision" in head)


def collect(paths, scan=None):
    """{(kun, aktyor, model): {maydon: son}} va atributsiya usuli.

    `scan` berilsa sessiya belgilari va format sentineli ham yig'iladi.
    """
    scan = scan if scan is not None else Scan()
    rows = collections.defaultdict(lambda: collections.Counter())
    by_uuid = {}            # Task chiqargan javob uuid -> aktyor
    guessed = False
    last = {}               # message.id -> (kalit, usage)
    for path in paths:
        file_actor = meta_actor(path)
        agent_file = os.path.basename(path).startswith("agent-")
        ordered = None      # fayl ichida tartib bo'yicha oxirgi aktyor
        with open(path, encoding="utf-8", errors="replace") as handle:
            for number, line in enumerate(handle):
                if not worth_parsing(line):
                    # usage siz assistant qatori faqat sentinel uchun sanaladi.
                    head = line[:HEAD]
                    if ASSISTANT.search(head) and '"<synthetic>"' not in head:
                        scan.assistant += 1
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(row, dict):
                    continue
                message = row.get("message")
                message = message if isinstance(message, dict) else {}
                scan_row(scan, row, message, "%s:%d" % (path, number))
                for block in blocks(message):
                    if (isinstance(block, dict)
                            and block.get("type") == "tool_use"
                            and block.get("name") in ("Task", "Agent")):
                        actor = (block.get("input") or {}).get("subagent_type")
                        if actor:
                            ordered = actor
                            if row.get("uuid"):
                                by_uuid[row["uuid"]] = actor
                usage = message.get("usage")
                if not usage or not isinstance(usage, dict):
                    continue
                if file_actor:
                    actor = file_actor
                elif row.get("isSidechain") or agent_file:
                    parent = row.get("parentUuid")
                    if parent in by_uuid:
                        actor = by_uuid[parent]
                    else:
                        actor = ordered or "aktyor (noma'lum)"
                        guessed = True
                    # Zanjir ichidagi keyingi javoblar ham shu aktyorga.
                    if row.get("uuid"):
                        by_uuid[row["uuid"]] = actor
                else:
                    actor = MAIN
                key = (day_of(row.get("timestamp")), actor,
                       message.get("model") or UNKNOWN)
                mid = message.get("id")
                if mid:
                    # Bitta javob har content block uchun qayta yoziladi;
                    # oqim o'rtasidagi qatorda chiqish hali to'liq emas.
                    last[mid] = (key, usage)
                else:
                    add(rows[key], usage)
    for key, usage in last.values():
        add(rows[key], usage)
    return rows, guessed


def session_block(rows, scan, session, source="transkript"):
    """Sessiya bloki: faqat bir ma'noli maydonlar."""
    usd, unpriced = 0.0, set()
    for (_, _, model), counts in rows.items():
        value = cost(model, counts)
        if value is None:
            unpriced.add(model)
        else:
            usd += value
    return {
        "sessiya": session,
        "turi": "monitoring",
        "manba": source,
        "usd": round(usd, 4),
        "narxsiz": sorted(unpriced),
        "faol_daqiqa": scan.active_minutes(),
        "tools": dict(sorted(collections.Counter(scan.tools.values()).items())),
        "aktyorlar": dict(sorted(
            collections.Counter(scan.actors.values()).items())),
        "tosiqlar": {name: len(ids) for name, ids in sorted(scan.blocked.items())},
    }


def summarise(rows, days):
    """Kun bo'yicha: {kun: {aktyor: (sonlar, narx, narxsiz_modelmi)}}."""
    out = collections.defaultdict(lambda: collections.defaultdict(
        lambda: [collections.Counter(), 0.0, False]))
    for (day, actor, model), counts in rows.items():
        if days and day not in days:
            continue
        slot = out[day][actor]
        slot[0].update(counts)
        value = cost(model, counts)
        if value is None:
            slot[2] = True
        else:
            slot[1] += value
    return out


def fmt(n):
    return f"{n:,}"


def show(summary, guessed):
    if not summary:
        print("Bu kunlar uchun yozuv topilmadi.")
        return 0
    grand = 0.0
    for day in sorted(summary):
        actors = summary[day]
        total = sum(slot[1] for slot in actors.values())
        grand += total
        print("\n== %s == $%.2f" % (day, total))
        print("%-22s %10s %12s %12s %10s %9s"
              % ("aktyor", "kirish", "kesh yoz", "kesh o'qi",
                 "chiqish", "narx"))
        for actor in sorted(actors, key=lambda a: -actors[a][1]):
            counts, value, unpriced = actors[actor]
            print("%-22s %10s %12s %12s %10s %9s%s"
                  % (actor,
                     fmt(counts["input_tokens"]),
                     fmt(counts["cache_creation_input_tokens"]),
                     fmt(counts["cache_read_input_tokens"]),
                     fmt(counts["output_tokens"]),
                     "$%.2f" % value,
                     "  (narxsiz model bor)" if unpriced else ""))
    if len(summary) > 1:
        print("\nJAMI: $%.2f" % grand)
    if guessed:
        print("\nAktyor nomi qismi tartib bo'yicha aniqlandi, zanjir "
              "havolasi bo'lmagan joyda.")
    return 0


def save(rows, project, session, block=None):
    """Sessiya yig'masini `<oy>/<proyekt>/<sessiya>.json` ga yozadi. Jim, hook uchun.

    Sessiya har safar transkriptdan to'liq qayta hisoblanadi va fayl
    butunligicha almashtiriladi: ikki marta qo'shilish yo'q, boshqa
    sessiya va proyekt fayllariga tegilmaydi, qulf kerak emas. Sessiya
    bloki oxirgi kunning oyi fayliga yoziladi.
    """
    months = collections.defaultdict(dict)
    for (day, actor, model), counts in rows.items():
        if not day:
            continue
        entry = months[day[:7]].setdefault(day, {})
        slot = entry.setdefault(actor, {
            "tokens": dict.fromkeys(FIELDS + (WRITE_1H,), 0),
            "usd": 0.0, "models": []})
        for field in slot["tokens"]:
            slot["tokens"][field] += counts.get(field, 0)
        value = cost(model, counts)
        if value is None:
            slot.setdefault("narxsiz", []).append(model)
        else:
            slot["usd"] = round(slot["usd"] + value, 4)
        if model not in slot["models"]:
            slot["models"].append(model)
    if block and months:
        months[max(months)][BLOCK_KEY] = block
    try:
        for month, data in months.items():
            folder = os.path.join(STORE, month, project)
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, session + ".json")
            geniuslib.atomic_write_text(
                path, json.dumps(data, indent=1, sort_keys=True))
    except OSError:
        return 0           # hook o'z xatosi bilan ishni to'xtatmaydi
    return 0


def note_format(problem, source):
    """Hook rejimidagi sentinel: sabab faylga, toza bo'lsa fayl olinadi."""
    target = os.path.join(STATE_DIR, FORMAT_FILE)
    try:
        if not problem:
            if os.path.exists(target):
                os.remove(target)
            return
        os.makedirs(STATE_DIR, exist_ok=True)
        geniuslib.atomic_write_text(target, json.dumps(
            {"sabab": problem, "transkript": source,
             "vaqt": datetime.datetime.now().isoformat(timespec="seconds")},
            ensure_ascii=False))
    except OSError:
        pass


def read_payload():
    """Hook stdin dagi JSON. Terminal, bo'sh yoki buzuq bo'lsa {}."""
    return hookio.read_payload() or {}


def save_session(main, project, session):
    scan = Scan()
    rows, _ = collect(session_files(main), scan)
    note_format(scan.problem(), main)
    return save(rows, project, session, session_block(rows, scan, session))


def save_hook():
    """--saqlash: hookda payloaddagi sessiya, qo'lda proyektning har sessiyasi."""
    payload = read_payload()
    if not hookio.active(payload):
        return 0
    path = payload.get("transcript_path")
    if path and path.endswith(".jsonl") and os.path.isfile(path):
        session = (payload.get("session_id")
                   or os.path.basename(path)[:-len(".jsonl")])
        return save_session(path, os.path.basename(os.path.dirname(path)), session)
    base = None if path else project_base()
    if base is None:
        print("usage.py: transkript topilmadi, sarf yozilmadi.", file=sys.stderr)
        return 0
    for main in mains(base):
        save_session(main, os.path.basename(base),
                     os.path.basename(main)[:-len(".jsonl")])
    return 0


# --- Hisobot: transkript va saqlangan yig'ma birga -------------------------

def stored(project, session="*"):
    """{sessiya: {"days": {kun: {aktyor: slot}}, "block": blok yoki None}}."""
    out = {}
    if not project:
        return out
    name = "*.json" if session == "*" else glob.escape(session) + ".json"
    pattern = os.path.join(glob.escape(STORE), "*", glob.escape(project), name)
    for path in sorted(glob.glob(pattern)):
        try:
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict):
            continue
        entry = out.setdefault(os.path.basename(path)[:-len(".json")],
                               {"days": {}, "block": None})
        for day, actors in data.items():
            if day == BLOCK_KEY and isinstance(actors, dict):
                entry["block"] = actors
            elif not day.startswith("_") and isinstance(actors, dict):
                entry["days"][day] = actors
    return out


def new_slot():
    return [collections.Counter(), 0.0, False]


def ledger(base, project, scan):
    """{sessiya: {kun: {aktyor: [sonlar, usd, narxsiz]}}}, guessed va manba
    kunlari {"transkript": kunlar, "yigma": kunlar}.

    Transkriptda yo'q (kun, sessiya) juftlari yig'madan olinadi.
    """
    book = collections.defaultdict(lambda: collections.defaultdict(
        lambda: collections.defaultdict(new_slot)))
    guessed = False
    sources = {"transkript": set(), "yigma": set()}
    for main in (mains(base) if base else []):
        session = os.path.basename(main)[:-len(".jsonl")]
        rows, flag = collect(session_files(main), scan)
        guessed = guessed or flag
        for (day, actor, model), counts in rows.items():
            sources["transkript"].add(day)
            slot = book[session][day][actor]
            slot[0].update(counts)
            value = cost(model, counts)
            if value is None:
                slot[2] = True
            else:
                slot[1] += value
    for session, entry in stored(project).items():
        known = book.get(session, {})
        for day, actors in entry["days"].items():
            if day in known:
                continue
            for actor, data in actors.items():
                if not isinstance(data, dict):
                    continue
                slot = book[session][day][actor]
                tokens = data.get("tokens") or {}
                slot[0].update({k: v for k, v in tokens.items()
                                if isinstance(v, int)})
                slot[1] += float(data.get("usd") or 0.0)
                slot[2] = slot[2] or bool(data.get("narxsiz"))
                sources["yigma"].add(day)
    return book, guessed, sources


def by_day(book, days):
    out = collections.defaultdict(lambda: collections.defaultdict(new_slot))
    for sessions in book.values():
        for day, actors in sessions.items():
            if days and day not in days:
                continue
            for actor, (counts, value, unpriced) in actors.items():
                slot = out[day][actor]
                slot[0].update(counts)
                slot[1] += value
                slot[2] = slot[2] or unpriced
    return out


def week(book, today):
    """Oxirgi 7 kun: sessiya soni, mediana $/sessiya, aktyor ulushi."""
    days = {str(today - datetime.timedelta(days=i)) for i in range(7)}
    per_session, per_actor, unpriced = [], collections.Counter(), 0
    for sessions in book.values():
        usd, seen, flag = 0.0, False, False
        for day, actors in sessions.items():
            if day not in days:
                continue
            for actor, (_, value, narxsiz) in actors.items():
                seen = True
                usd += value
                per_actor[actor] += value
                flag = flag or narxsiz
        if seen:
            per_session.append(usd)
            unpriced += flag
    total = sum(per_actor.values())
    return {
        "davr": {"dan": min(days), "gacha": max(days)},
        "sessiyalar": len(per_session),
        "mediana_usd": round(statistics.median(per_session), 4)
        if per_session else 0.0,
        "jami_usd": round(total, 4),
        "aktyor_ulushi": {actor: round(value / total, 3)
                          for actor, value in per_actor.most_common()}
        if total else {},
        "narxsiz_sessiyalar": unpriced,
    }


def show_week(data):
    print("Hafta %s .. %s: %d sessiya, jami $%.2f"
          % (data["davr"]["dan"], data["davr"]["gacha"], data["sessiyalar"],
             data["jami_usd"]))
    print("mediana $/sessiya: $%.2f" % data["mediana_usd"])
    if data["aktyor_ulushi"]:
        print("aktyor ulushi:")
        for actor, share in data["aktyor_ulushi"].items():
            print("  %-22s %5.1f%%" % (actor, share * 100))
    if data["narxsiz_sessiyalar"]:
        print("narxsiz model bor sessiya: %d (dollar kam ko'rsatilgan)"
              % data["narxsiz_sessiyalar"])
    return 0


def find_session(arg):
    """`--sessiya` qiymati: .jsonl yo'li yoki sessiya id si."""
    if arg.endswith(".jsonl") and os.path.isfile(arg):
        return os.path.abspath(arg)
    base = project_base()
    places = [os.path.join(base, arg + ".jsonl")] if base else []
    places += sorted(glob.glob(os.path.join(
        glob.escape(config_dir()), "projects", "*", glob.escape(arg) + ".jsonl")))
    for place in places:
        if os.path.isfile(place):
            return place
    return None


def stored_block(session):
    """Transkripti o'chgan sessiya bloki yig'madan."""
    for path in sorted(glob.glob(os.path.join(
            glob.escape(STORE), "*", "*", glob.escape(session) + ".json"))):
        entry = stored(os.path.basename(os.path.dirname(path)), session).get(session)
        if not entry:
            continue
        if entry["block"]:
            return dict(entry["block"], manba="saqlangan yig'ma")
        usd, unpriced = 0.0, set()
        for actors in entry["days"].values():
            for data in actors.values():
                if isinstance(data, dict):
                    usd += float(data.get("usd") or 0.0)
                    unpriced.update(data.get("narxsiz") or [])
        return {"sessiya": session, "turi": "monitoring",
                "manba": "saqlangan yig'ma", "usd": round(usd, 4),
                "narxsiz": sorted(unpriced), "faol_daqiqa": None,
                "tools": None, "aktyorlar": None, "tosiqlar": None}
    return None


def show_block(block):
    print("Sessiya %s (%s, %s)" % (block["sessiya"], block["turi"], block["manba"]))
    print("  usd        : $%.4f%s" % (block["usd"], "  (narxsiz: %s)"
                                      % ", ".join(block["narxsiz"])
                                      if block["narxsiz"] else ""))
    if block.get("faol_daqiqa") is None:
        print("  qolgan maydonlar: transkript o'chgan, yig'mada yo'q")
        return 0
    print("  faol daqiqa: %s" % block["faol_daqiqa"])
    print("  tools      : %s" % (", ".join("%s %d" % item for item
                                            in block["tools"].items()) or "-"))
    print("  aktyorlar  : %s" % (", ".join("%s %d" % item for item
                                            in block["aktyorlar"].items()) or "-"))
    print("  to'siqlar  : %s" % ", ".join("%s %d" % item for item
                                          in block["tosiqlar"].items()))
    return 0


def format_changed(problem):
    print("FORMAT O'ZGARGAN: %s" % problem)
    print("Transkript tuzilishi Claude Code yangilanishi bilan o'zgargan "
          "bo'lishi mumkin. Raqam jim noto'g'ri chiqmasligi uchun hisobot "
          "berilmadi: tools/usage.py ni yangi formatga moslang.")
    return 3


def table():
    print("Million token uchun dollar (%s dagi PRICES):" % os.path.basename(__file__))
    print("holati: %s, manba: %s" % (PRICES_AS_OF, PRICES_SOURCE))
    print("\n%-14s %8s %8s %12s %12s %10s"
          % ("model", "kirish", "chiqish", "kesh yoz 5m", "kesh yoz 1h",
             "kesh o'qi"))
    for key in sorted(PRICES):
        rate_in, rate_out, rate_read = PRICES[key]
        print("%-14s %8.2f %8.2f %12.2f %12.2f %10.2f"
              % (key, rate_in, rate_out, rate_in * CACHE_WRITE_5M,
                 rate_in * CACHE_WRITE_1H, rate_read))
    print("\nNarx o'zgaradi. Eskirsa shu jadval tahrirlanadi; model faqat "
          "aniq kalit bilan narxlanadi, noma'lum model nolga aylanmaydi, "
          "belgilanadi.")
    return 0


def session_main(arg, as_json):
    main = find_session(arg)
    if main is None:
        block = stored_block(arg)
        if block is None:
            print("Sessiya topilmadi: %s (transkriptda ham, yig'mada ham)" % arg)
            return 2
    else:
        scan = Scan()
        rows, _ = collect(session_files(main), scan)
        problem = scan.problem()
        if problem:
            return format_changed(problem)
        block = session_block(rows, scan, os.path.basename(main)[:-len(".jsonl")])
    if as_json:
        print(json.dumps(block, ensure_ascii=False, sort_keys=True))
        return 0
    return show_block(block)


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--kun")
    parser.add_argument("--davr", type=int)
    parser.add_argument("--saqlash", action="store_true")
    parser.add_argument("--jadval", action="store_true")
    parser.add_argument("--hammasi", action="store_true")
    parser.add_argument("--hafta", action="store_true")
    parser.add_argument("--sessiya")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.jadval:
        return table()
    if args.saqlash:
        return save_hook()
    if args.json and not (args.sessiya or args.hafta):
        parser.error("--json faqat --sessiya yoki --hafta bilan")
    if args.sessiya:
        return session_main(args.sessiya, args.json)

    base = project_base()
    project = project_name(base)
    if not base and not project:
        print("Transkript topilmadi, sarf o'lchanmadi.")
        return 2

    scan = Scan()
    book, guessed, sources = ledger(base, project, scan)
    problem = scan.problem()
    if problem:
        return format_changed(problem)
    if not book:
        print("Transkript topilmadi, sarf o'lchanmadi.")
        return 2

    today = datetime.date.today()
    if args.hafta:
        data = week(book, today)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, sort_keys=True))
            return 0
        return show_week(data)

    days = None
    if args.kun:
        days = {args.kun}
    elif args.davr:
        days = {str(today - datetime.timedelta(days=i))
                for i in range(args.davr)}
    elif not args.hammasi:
        days = {str(today)}

    summary = by_day(book, days)
    code = show(summary, guessed)
    if summary:
        print("\nmanba: transkript %d kun, saqlangan yig'ma %d kun"
              % (len(sources["transkript"] & set(summary)),
                 len(sources["yigma"] & set(summary))))
    return code


if __name__ == "__main__":
    sys.exit(main())
