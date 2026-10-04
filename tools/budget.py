#!/usr/bin/env python3
"""Aktyor chaqiruv budjeti: bitta vazifada ko'pi bilan ikki marta.

    python3 tools/budget.py --yangi-vazifa "<nom>"   # hisoblagich nolga
    python3 tools/budget.py arxitektor               # +1, uchinchida xato
    python3 tools/budget.py --holat                  # jadval
    python3 tools/budget.py --tiklash arxitektor     # bitta qadamni qaytarish

`PreToolUse` hook sifatida ham ishlaydi: stdin ga JSON kelsa, `Task`
yoki `Agent` chaqiruvidagi aktyorni o'zi oladi va uchinchisini to'sadi.

Nega hisoblagich kerak: ikki chaqiruv chegarasi matnda yozilgan edi va
matn esdan chiqadi. Uchinchi urinish arzon ko'rinadi, aslida esa u
muammoni hal qilmaydi, sababini yashiradi: aktyor birinchi martada
qoidani ko'rmagan yoki reviewer boshqa mezon bilan tekshirgan. Chegara
to'silganda shu savol beriladi, uchinchi urinish o'rniga.

Zanjirdagi to'rtta aktyor sanaladi. `qidiruv` va `tahlil` sanalmaydi:
ular zanjir qadami emas, o'qish asbobi, va ularni cheklash arzon
yo'lni qimmat qiladi.
"""

import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(ROOT, ".claude", ".state")
LOG = os.path.join(STATE_DIR, "budget.json")

# Zanjir aktyorlari. Tartib chiqishdagi jadval tartibi.
ACTORS = ("rejalashtiruvchi", "arxitektor", "test-muhandis", "review")
LIMIT = 2

# Vazifa belgilanmagan bo'lsa hisoblagich shu muddatdan keyin o'zi
# nolga tushadi: uzun sessiyada ertalabki vazifa kechqurungisini
# to'sib qo'ymasligi kerak.
MAX_AGE = 6 * 3600

BLOCKED = """%s uchun budjet tugadi: %d chaqiruv bo'ldi, chegara %d.

Uchinchi urinish o'rniga sabab aytiladi. Odatda u uchtadan biri:
  1. Aktyor birinchi martada qoidani ko'rmagan
     -> python3 tools/rules_for.py <fayllar> chiqishini tekshiring
  2. Reviewer boshqa mezon bilan tekshirgan
     -> ikkalasi bir xil ro'yxatni olishi kerak
  3. "Bajarildi" nimaligi aytilmagan
     -> qabul mezoni normalizatsiyada belgilanadi

Nima bajarildi, nima qolgan va nima yetishmayotganini yozib, aniq
savol bering. Yangi vazifa boshlansa:
  python3 tools/budget.py --yangi-vazifa "<nom>"
"""


def load():
    try:
        with open(LOG, encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ValueError
    except (OSError, ValueError):
        return {"task": "", "started": time.time(), "calls": {}}
    if time.time() - data.get("started", 0) > MAX_AGE:
        return {"task": "", "started": time.time(), "calls": {}}
    data.setdefault("calls", {})
    return data


def save(data):
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        tmp = LOG + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp, LOG)
    except OSError:
        pass   # hisoblagich ishni to'xtatmaydi


def new_task(name):
    save({"task": name, "started": time.time(), "calls": {}})
    print("Vazifa: %s. Budjet nolga tushdi (har aktyor %d marta)."
          % (name or "nomsiz", LIMIT))
    return 0


def status():
    data = load()
    print("Vazifa: %s" % (data.get("task") or "nomsiz"))
    print("\n%-18s %-10s %s" % ("aktyor", "chaqiruv", "holat"))
    for actor in ACTORS:
        used = data["calls"].get(actor, 0)
        state = "-" if not used else ("tugadi" if used >= LIMIT else "qoldi 1")
        print("%-18s %-10s %s" % (actor, "%d/%d" % (used, LIMIT), state))
    return 0


def restore(actor):
    data = load()
    used = data["calls"].get(actor, 0)
    if used:
        data["calls"][actor] = used - 1
        save(data)
    print("%s: %d/%d" % (actor, data["calls"].get(actor, 0), LIMIT))
    return 0


def take(actor):
    """Bitta chaqiruvni hisobga oladi. Chegara oshsa (xabar, False)."""
    if actor not in ACTORS:
        return "", True            # sanalmaydigan aktyor erkin
    data = load()
    used = data["calls"].get(actor, 0)
    if used >= LIMIT:
        return BLOCKED % (actor, used, LIMIT), False
    data["calls"][actor] = used + 1
    save(data)
    return "%s: %d/%d chaqiruv" % (actor, used + 1, LIMIT), True


def hook(payload):
    """PreToolUse: Task yoki Agent chaqiruvidagi aktyorni tekshiradi."""
    if payload.get("tool_name") not in ("Task", "Agent"):
        return 0
    actor = (payload.get("tool_input") or {}).get("subagent_type") or ""
    message, allowed = take(actor)
    if not allowed:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": message,
        }}, sys.stdout)
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        if sys.stdin.isatty():
            print(__doc__.strip().split("\n\n")[1].strip())
            return 2
        try:
            payload = json.load(sys.stdin)
        except (OSError, ValueError):
            return 0           # hook o'z xatosi bilan ishni to'xtatmaydi
        return hook(payload)
    if args[0] == "--holat":
        return status()
    if args[0] == "--yangi-vazifa":
        return new_task(args[1] if len(args) > 1 else "")
    if args[0] == "--tiklash":
        if len(args) < 2:
            print("foydalanish: budget.py --tiklash <aktyor>", file=sys.stderr)
            return 2
        return restore(args[1])
    message, allowed = take(args[0])
    print(message or "%s sanalmaydi (zanjir aktyori emas)" % args[0])
    return 0 if allowed else 1


if __name__ == "__main__":
    sys.exit(main())
