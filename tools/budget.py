#!/usr/bin/env python3
"""Aktyor chaqiruv budjeti: bitta vazifada ko'pi bilan ikki marta.

    python3 tools/budget.py --yangi-vazifa "<nom>"   # hisoblagich nolga
    python3 tools/budget.py arxitektor               # +1, uchinchida xato
    python3 tools/budget.py --holat                  # jadval
    python3 tools/budget.py --tiklash arxitektor     # bitta qadamni qaytarish

`PreToolUse` hook sifatida ham ishlaydi: stdin ga JSON kelsa, `Task`
yoki `Agent` chaqiruvidagi aktyorni o'zi oladi va uchinchisini to'sadi.
`UserPromptSubmit` payloadi kelsa shu sessiya hisobini jim nolga
tushiradi: yangi so'rov yangi vazifa.

Nega hisoblagich kerak: ikki chaqiruv chegarasi matnda yozilgan edi va
matn esdan chiqadi. Uchinchi urinish arzon ko'rinadi, aslida esa u
muammoni hal qilmaydi, sababini yashiradi: aktyor birinchi martada
qoidani ko'rmagan yoki reviewer boshqa mezon bilan tekshirgan. Chegara
to'silganda shu savol beriladi, uchinchi urinish o'rniga.

Hisob sessiya bo'yicha: hook payloaddagi `session_id` ni, CLI esa
`CLAUDE_CODE_SESSION_ID` ni oladi (u yo'q bo'lsa shu papkadagi oxirgi
faol sessiyani va buni aytadi). Parallel sessiyalar va global
o'rnatishdagi proyektlar bir-birini to'smaydi. Holat
`.claude/.state/budget.json` da (`GENIUS_STATE_DIR` bilan
almashtiriladi), bir vaqtdagi hooklar qulf bilan navbatlashadi.

Zanjirdagi to'rtta aktyor sanaladi. `qidiruv` va `tahlil` sanalmaydi:
ular zanjir qadami emas, o'qish asbobi, va ularni cheklash arzon
yo'lni qimmat qiladi.
"""

import contextlib
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = (os.environ.get("GENIUS_STATE_DIR")
             or os.path.join(ROOT, ".claude", ".state"))
LOG = os.path.join(STATE_DIR, "budget.json")

# Zanjir aktyorlari. Tartib chiqishdagi jadval tartibi.
ACTORS = ("rejalashtiruvchi", "arxitektor", "test-muhandis", "review")
LIMIT = 2

# Vazifa belgilanmagan bo'lsa hisoblagich shu muddatdan keyin o'zi
# nolga tushadi: uzun sessiyada ertalabki vazifa kechqurungisini
# to'sib qo'ymasligi kerak.
MAX_AGE = 6 * 3600

# Bir kundan beri ko'rinmagan sessiya fayldan tashlanadi.
KEEP = 24 * 3600

# Qulf shundan eski bo'lsa egasi o'lgan: tirik egasi uni millisekund ushlaydi.
STALE_LOCK = 5

# Bir chaqiruv ikki marta kelsa (repo va global hook birga) bir marta sanaladi.
SEEN_IDS = 20

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


@contextlib.contextmanager
def locked():
    """Parallel Agent chaqiruvlari bir-birining hisobini o'chirmasin.

    fcntl emas, O_EXCL: Windows ham maqsadli platforma.
    """
    lock = LOG + ".lock"
    fd = None
    with contextlib.suppress(OSError):
        os.makedirs(STATE_DIR, exist_ok=True)
    for _ in range(200):                 # ~4 s, hook timeout 10 s
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except OSError as exc:
            # Windows da o'chirilayotgan qulf PermissionError beradi.
            if not isinstance(exc, FileExistsError) and not os.path.exists(lock):
                break                    # papka yozilmaydi: qulfsiz davom
            with contextlib.suppress(OSError):   # qulf shu orada yechilgan
                if time.time() - os.path.getmtime(lock) > STALE_LOCK:
                    os.remove(lock)
            time.sleep(0.02)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
            with contextlib.suppress(OSError):
                os.remove(lock)


def norm(path):
    return os.path.normcase(os.path.realpath(path)) if path else ""


def here():
    try:
        return norm(os.getcwd())
    except OSError:
        return ""


def load():
    """{"sessions": {kalit: hisob}}. Eski tekis shakl bo'sh holat deb olinadi."""
    try:
        with open(LOG, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        data = None
    if not isinstance(data, dict) or not isinstance(data.get("sessions"), dict):
        data = {"sessions": {}}
    return data


def fresh(slot, now):
    return isinstance(slot, dict) and now - slot.get("started", 0) <= MAX_AGE


def slot_of(data, key, cwd=""):
    """Sessiya hisobi; yo'q yoki muddati o'tgan bo'lsa yangisi."""
    now = time.time()
    slot = data["sessions"].get(key)
    if not fresh(slot, now):
        slot = {"task": "", "started": now, "calls": {}}
        data["sessions"][key] = slot
    if not isinstance(slot.get("calls"), dict):
        slot["calls"] = {}
    slot["seen"] = now
    if cwd:
        slot.setdefault("cwd", cwd)
    return slot


def save(data):
    now = time.time()
    data["sessions"] = {
        key: slot for key, slot in data["sessions"].items()
        if isinstance(slot, dict)
        and now - slot.get("seen", slot.get("started", 0)) <= KEEP}
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        # Har jarayonning o'z tmp fayli: qulfsiz holatda ham JSON buzilmaydi.
        tmp = "%s.%d.tmp" % (LOG, os.getpid())
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle)
        os.replace(tmp, LOG)
    except OSError:
        pass   # hisoblagich ishni to'xtatmaydi


def cli_key(data):
    """CLI qaysi sessiya hisobini ko'radi: (kalit, izoh).

    CLAUDE_CODE_SESSION_ID bo'lsa shu. Bo'lmasa shu papka proyektidagi
    oxirgi faol sessiya, u ham bo'lmasa umuman oxirgisi. Tirik sessiya
    bir nechta bo'lsa tanlov aytiladi, xato jim qolmasin.
    """
    sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
    if sid:
        return sid, ""
    now = time.time()
    live = {k: s for k, s in data["sessions"].items() if fresh(s, now)}
    if not live:
        return "", ""
    cwd = here()
    near = {k: s for k, s in live.items()
            if s.get("cwd") and (cwd == s["cwd"]
                                 or cwd.startswith(s["cwd"].rstrip(os.sep) + os.sep))}
    pool = near or live
    key = max(pool, key=lambda k: pool[k].get("seen", 0))
    note = "Sessiya: %s (oxirgi faol)" % (key[:8] or "nomsiz") if len(live) > 1 else ""
    return key, note


def new_task(name):
    with locked():
        data = load()
        key, note = cli_key(data)
        slot_of(data, key, here()).update(task=name, started=time.time(), calls={})
        save(data)
    if note:
        print(note)
    print("Vazifa: %s. Budjet nolga tushdi (har aktyor %d marta)."
          % (name or "nomsiz", LIMIT))
    return 0


def reset(key, cwd=""):
    """Yangi so'rov: shu sessiya hisobi jim nolga tushadi."""
    with locked():
        data = load()
        slot_of(data, key, cwd).update(task="", started=time.time(), calls={})
        save(data)


def status():
    data = load()
    key, note = cli_key(data)
    slot = slot_of(data, key)
    if note:
        print(note)
    print("Vazifa: %s" % (slot.get("task") or "nomsiz"))
    print("\n%-18s %-10s %s" % ("aktyor", "chaqiruv", "holat"))
    for actor in ACTORS:
        used = slot["calls"].get(actor, 0)
        state = "-" if not used else ("tugadi" if used >= LIMIT else "qoldi 1")
        print("%-18s %-10s %s" % (actor, "%d/%d" % (used, LIMIT), state))
    return 0


def restore(actor):
    with locked():
        data = load()
        key, note = cli_key(data)
        slot = slot_of(data, key, here())
        used = slot["calls"].get(actor, 0)
        if used:
            slot["calls"][actor] = used - 1
            save(data)
    if note:
        print(note)
    print("%s: %d/%d" % (actor, slot["calls"].get(actor, 0), LIMIT))
    return 0


def take(actor, key=None, cwd="", call_id=None):
    """Bitta chaqiruvni hisobga oladi. Chegara oshsa (xabar, False).

    key None bo'lsa CLI chaqiruvi: sessiya cli_key bilan tanlanadi.
    """
    if actor not in ACTORS:
        return "", True            # sanalmaydigan aktyor erkin
    with locked():
        data = load()
        if key is None:
            key, cwd = cli_key(data)[0], here()
        slot = slot_of(data, key, cwd)
        used = slot["calls"].get(actor, 0)
        ids = slot.setdefault("ids", [])
        if call_id and call_id in ids:
            return "%s: %d/%d chaqiruv" % (actor, used, LIMIT), True
        if used >= LIMIT:
            return BLOCKED % (actor, used, LIMIT), False
        slot["calls"][actor] = used + 1
        if call_id:
            slot["ids"] = (ids + [call_id])[-SEEN_IDS:]
        save(data)
    return "%s: %d/%d chaqiruv" % (actor, used + 1, LIMIT), True


def hook(payload):
    """PreToolUse: Task yoki Agent chaqiruvidagi aktyorni tekshiradi."""
    key = (payload.get("session_id")
           or os.environ.get("CLAUDE_CODE_SESSION_ID") or "")
    cwd = norm(payload.get("cwd"))
    if payload.get("hook_event_name") == "UserPromptSubmit":
        reset(key, cwd)            # jim: bu hook chiqishi kontekstga tushadi
        return 0
    if payload.get("tool_name") not in ("Task", "Agent"):
        return 0
    actor = (payload.get("tool_input") or {}).get("subagent_type") or ""
    message, allowed = take(actor, key, cwd, payload.get("tool_use_id"))
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
        return hook(payload) if isinstance(payload, dict) else 0
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
