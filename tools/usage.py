#!/usr/bin/env python3
"""Kunlik token sarfi va uni qaysi aktyor sarflagani.

    python3 tools/usage.py                 # bugun (mahalliy sana)
    python3 tools/usage.py --kun 2026-10-04
    python3 tools/usage.py --davr 7        # oxirgi 7 kun
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
`.claude/usage/<oy>/<proyekt-slug>/<sessiya>.json` ga yozadi.

Narx jadvali o'zgaradi. U shu faylda ochiq turadi: eskirsa tahrirlanadi,
va noma'lum model jim nolga aylanmaydi, alohida belgilanadi.
"""

import argparse
import collections
import datetime
import glob
import json
import os
import re
import sys

import hookio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.environ.get("USAGE_STORE") or os.path.join(ROOT, ".claude", "usage")

# Million token uchun dollar: (kirish, chiqish, keshdan o'qish). 2026-10 holati.
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


def price_for(model):
    """(kirish, chiqish, kesh o'qish) narxi yoki None. Eng uzun mos kalit tanlanadi."""
    if not model:
        return None
    best = None
    for key, value in PRICES.items():
        if key in model and (best is None or len(key) > len(best[0])):
            best = (key, value)
    return best[1] if best else None


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


def project_base():
    """Shu proyekt transkriptlari papkasi yoki None.

    Asbob klonining emas, ish papkasining slugi olinadi: global
    o'rnatishda klon bitta, proyekt esa ko'p.
    """
    projects = os.path.join(config_dir(), "projects")
    candidates = [os.environ.get("CLAUDE_PROJECT_DIR")]
    try:
        here = os.getcwd()
    except OSError:
        here = ROOT
    while True:
        candidates.append(here)
        parent = os.path.dirname(here)
        if parent == here:
            break
        here = parent
    candidates.append(ROOT)
    for candidate in candidates:
        if not candidate:
            continue
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


def session_files(main):
    """Sessiya fayli va uning subagentlari (`journal.jsonl` kirmaydi)."""
    pattern = os.path.join(glob.escape(main[:-len(".jsonl")]), "subagents",
                           "**", "agent-*.jsonl")
    return [main] + sorted(glob.glob(pattern, recursive=True))


def transcripts(base):
    """Proyektdagi barcha sessiyalar, subagentlari bilan."""
    out = []
    for main in sorted(glob.glob(os.path.join(glob.escape(base), "*.jsonl"))):
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


def day_of(stamp):
    """Mahalliy sana: "bugun" va --davr ham mahalliy sanadan hisoblanadi."""
    text = str(stamp or "")
    try:
        moment = datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return text[:10]
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


def collect(paths):
    """{(kun, aktyor, model): {maydon: son}} va atributsiya usuli."""
    rows = collections.defaultdict(lambda: collections.Counter())
    by_uuid = {}            # Task chiqargan javob uuid -> aktyor
    guessed = False
    last = {}               # message.id -> (kalit, usage)
    for path in paths:
        file_actor = meta_actor(path)
        agent_file = os.path.basename(path).startswith("agent-")
        ordered = None      # fayl ichida tartib bo'yicha oxirgi aktyor
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                # Na usage, na tool_use bo'lgan qatorni ochish behuda.
                if '"usage"' not in line and '"tool_use"' not in line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                message = row.get("message") or {}
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
                if not usage:
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


def save(rows, project, session):
    """Sessiya yig'masini `<oy>/<proyekt>/<sessiya>.json` ga yozadi. Jim, hook uchun.

    Sessiya har safar transkriptdan to'liq qayta hisoblanadi va fayl
    butunligicha almashtiriladi: ikki marta qo'shilish yo'q, boshqa
    sessiya va proyekt fayllariga tegilmaydi, qulf kerak emas.
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
    try:
        for month, data in months.items():
            folder = os.path.join(STORE, month, project)
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, session + ".json")
            tmp = "%s.%d.tmp" % (path, os.getpid())
            with open(tmp, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=1, sort_keys=True)
            os.replace(tmp, path)
    except OSError:
        return 0           # hook o'z xatosi bilan ishni to'xtatmaydi
    return 0


def read_payload():
    """Hook stdin dagi JSON. Terminal, bo'sh yoki buzuq bo'lsa {}."""
    return hookio.read_payload() or {}


def save_hook():
    """--saqlash: hookda payloaddagi sessiya, qo'lda proyektning har sessiyasi."""
    payload = read_payload()
    path = payload.get("transcript_path")
    if path and path.endswith(".jsonl") and os.path.isfile(path):
        rows, _ = collect(session_files(path))
        session = (payload.get("session_id")
                   or os.path.basename(path)[:-len(".jsonl")])
        return save(rows, os.path.basename(os.path.dirname(path)), session)
    base = None if path else project_base()
    if base is None:
        print("usage.py: transkript topilmadi, sarf yozilmadi.", file=sys.stderr)
        return 0
    for main in sorted(glob.glob(os.path.join(glob.escape(base), "*.jsonl"))):
        rows, _ = collect(session_files(main))
        save(rows, os.path.basename(base),
             os.path.basename(main)[:-len(".jsonl")])
    return 0


def table():
    print("Million token uchun dollar (%s dagi PRICES):" % os.path.basename(__file__))
    print("\n%-14s %8s %8s %12s %12s %10s"
          % ("model", "kirish", "chiqish", "kesh yoz 5m", "kesh yoz 1h",
             "kesh o'qi"))
    for key in sorted(PRICES):
        rate_in, rate_out, rate_read = PRICES[key]
        print("%-14s %8.2f %8.2f %12.2f %12.2f %10.2f"
              % (key, rate_in, rate_out, rate_in * CACHE_WRITE_5M,
                 rate_in * CACHE_WRITE_1H, rate_read))
    print("\nNarx o'zgaradi. Eskirsa shu jadval tahrirlanadi; noma'lum "
          "model nolga aylanmaydi, belgilanadi.")
    return 0


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--kun")
    parser.add_argument("--davr", type=int)
    parser.add_argument("--saqlash", action="store_true")
    parser.add_argument("--jadval", action="store_true")
    parser.add_argument("--hammasi", action="store_true")
    args = parser.parse_args()

    if args.jadval:
        return table()
    if args.saqlash:
        return save_hook()

    base = project_base()
    paths = transcripts(base) if base else []
    if not paths:
        print("Transkript topilmadi, sarf o'lchanmadi.")
        return 2

    rows, guessed = collect(paths)

    days = None
    if args.kun:
        days = {args.kun}
    elif args.davr:
        today = datetime.date.today()
        days = {str(today - datetime.timedelta(days=i))
                for i in range(args.davr)}
    elif not args.hammasi:
        days = {str(datetime.date.today())}

    return show(summarise(rows, days), guessed)


if __name__ == "__main__":
    sys.exit(main())
