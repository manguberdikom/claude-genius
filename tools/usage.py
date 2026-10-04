#!/usr/bin/env python3
"""Kunlik token sarfi va uni qaysi aktyor sarflagani.

    python3 tools/usage.py                 # bugun
    python3 tools/usage.py --kun 2026-10-04
    python3 tools/usage.py --davr 7        # oxirgi 7 kun
    python3 tools/usage.py --saqlash       # jim: kunlik yig'mani yozadi
    python3 tools/usage.py --jadval        # narx jadvali

Raqam transkriptdan olinadi, taxmin qilinmaydi: har javobning `usage`
yozuvida to'rtta son turadi va ularning narxi boshqacha. Keshdan o'qish
kirishdan o'n barobar arzon, keshga yozish esa chorak barobar qimmat,
shuning uchun "token" deb bitta songa qo'shib yuborish narxni yashiradi.

Aktyorga bo'lish: subagent javoblari transkriptda `isSidechain` bilan
belgilanadi, lekin ularning o'zida aktyor nomi yo'q. Nom oldingi
`Task`/`Agent` chaqiruvidan olinadi: `parentUuid` zanjiri bo'lsa shundan,
bo'lmasa tartib bo'yicha. Tartib bo'yicha bo'lsa chiqishda shu aytiladi.

Narx jadvali o'zgaradi. U shu faylda ochiq turadi: eskirsa tahrirlanadi,
va noma'lum model jim nolga aylanmaydi, alohida belgilanadi.
"""

import argparse
import collections
import datetime
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, ".claude", "usage")

# Million token uchun dollar: (kirish, chiqish). 2026-10 holati.
PRICES = {
    "opus-5-5": (4.0, 20.0),
    "opus-5": (5.0, 25.0),
    "sonnet-5-5": (2.0, 10.0),
    "sonnet-5": (3.0, 15.0),
    "haiku-4-5": (1.0, 5.0),
}
# Keshga yozish kirishdan qimmat, keshdan o'qish ancha arzon.
CACHE_WRITE = 1.25
CACHE_READ = 0.10

MAIN = "asosiy sessiya"
UNKNOWN = "noma'lum model"

FIELDS = ("input_tokens", "cache_creation_input_tokens",
          "cache_read_input_tokens", "output_tokens")


def price_for(model):
    """(kirish, chiqish) narxi yoki None. Eng uzun mos kalit tanlanadi."""
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
        return None
    rate_in, rate_out = price
    return (counts["input_tokens"] * rate_in
            + counts["cache_creation_input_tokens"] * rate_in * CACHE_WRITE
            + counts["cache_read_input_tokens"] * rate_in * CACHE_READ
            + counts["output_tokens"] * rate_out) / 1_000_000


def transcripts():
    """Shu proyektning barcha transkript fayllari."""
    slug = ROOT.replace(os.sep, "-")
    base = os.path.expanduser(os.path.join("~", ".claude", "projects", slug))
    if not os.path.isdir(base):
        return []
    return sorted(os.path.join(base, f) for f in os.listdir(base)
                  if f.endswith(".jsonl"))


def day_of(stamp):
    return (stamp or "")[:10]


def blocks(message):
    content = message.get("content")
    return content if isinstance(content, list) else []


def collect(paths):
    """{(kun, aktyor, model): {maydon: son}} va atributsiya usuli."""
    rows = collections.defaultdict(lambda: collections.Counter())
    by_uuid = {}            # Task chiqargan javob uuid -> aktyor
    ordered = None          # tartib bo'yicha oxirgi aktyor
    guessed = False
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
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
                if row.get("isSidechain"):
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
                for field in FIELDS:
                    rows[key][field] += usage.get(field, 0)
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


def save(rows):
    """Kunlik yig'mani oy fayliga yozadi. Jim ishlaydi, hook uchun."""
    months = collections.defaultdict(dict)
    for (day, actor, model), counts in rows.items():
        if not day:
            continue
        entry = months[day[:7]].setdefault(day, {})
        slot = entry.setdefault(actor, {"tokens": dict.fromkeys(FIELDS, 0),
                                        "usd": 0.0, "models": []})
        for field in FIELDS:
            slot["tokens"][field] += counts[field]
        value = cost(model, counts)
        if value is None:
            slot.setdefault("narxsiz", []).append(model)
        else:
            slot["usd"] = round(slot["usd"] + value, 4)
        if model not in slot["models"]:
            slot["models"].append(model)
    try:
        os.makedirs(STORE, exist_ok=True)
        for month, data in months.items():
            path = os.path.join(STORE, "%s.json" % month)
            old = {}
            if os.path.isfile(path):
                try:
                    with open(path, encoding="utf-8") as handle:
                        old = json.load(handle)
                except ValueError:
                    old = {}
            # Qayta hisoblangan kun eskisini bosadi: transkript haqiqat
            # manbasi, fayl esa uning nusxasi.
            old.update(data)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as handle:
                json.dump(old, handle, indent=1, sort_keys=True)
            os.replace(tmp, path)
    except OSError:
        return 0           # hook o'z xatosi bilan ishni to'xtatmaydi
    return 0


def table():
    print("Million token uchun dollar (%s dagi PRICES):" % os.path.basename(__file__))
    print("\n%-14s %8s %8s %10s %10s" % ("model", "kirish", "chiqish",
                                         "kesh yoz", "kesh o'qi"))
    for key in sorted(PRICES):
        rate_in, rate_out = PRICES[key]
        print("%-14s %8.2f %8.2f %10.2f %10.2f"
              % (key, rate_in, rate_out,
                 rate_in * CACHE_WRITE, rate_in * CACHE_READ))
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

    paths = transcripts()
    if not paths:
        if args.saqlash:
            return 0
        print("Transkript topilmadi, sarf o'lchanmadi.")
        return 2

    rows, guessed = collect(paths)

    if args.saqlash:
        return save(rows)

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
