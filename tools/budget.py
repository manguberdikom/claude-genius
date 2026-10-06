#!/usr/bin/env python3
"""Aktyor chaqiruv budjeti: bitta vazifada ko'pi bilan ikki marta.

    python3 tools/budget.py --yangi-vazifa "<nom>"   # hisoblagich nolga
    python3 tools/budget.py dasturchi               # +1, uchinchida xato
    python3 tools/budget.py --holat                  # jadval
    python3 tools/budget.py --tiklash dasturchi     # bitta qadamni qaytarish
    python3 tools/budget.py --tiklash dasturchi --guruh orders

`PreToolUse` hook sifatida ham ishlaydi: stdin ga JSON kelsa, `Task`
yoki `Agent` chaqiruvidagi aktyorni o'zi oladi va uchinchisini to'sadi.
`SendMessage` da `to` aktyor nomi bo'lsa, tugagan aktyorni qayta
yurgizish ham o'sha aktyorning chaqiruvi: yangi Agent chaqiruvisiz
ishlaydi va aks holda budjetdan o'tib ketardi. Boshqa manzil (asosiy
sessiya, agentId, jamoa) sanalmaydi. Bu faqat hook matcher'i
`SendMessage` ni ushlaganda ishlaydi.
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

Parallel guruhlar: aktyor promptidagi `guruh: <id>` qatori hisobni
guruhga ajratadi. Ikki guruh bir sessiyada parallel ishlasa, ularning
dasturchi chaqiruvlari bitta hisobga tushib, birinchi guruhning ikkinchi
aylanasi ikkinchi guruhning birinchi chaqiruvi tufayli to'silardi.
Qatorsiz chaqiruv eski xulqda: bitta umumiy hisob. Id faqat `guruh.py`
holat faylida (`<git-common-dir>/genius-guruh.json`) bo'lsa qabul
qilinadi: aks holda har chaqiruvga yangi `guruh: xN` yozib chegara
aylanib o'tilardi.

Zanjirdagi to'rtta aktyor sanaladi. `qidiruv`, `tahlil` va `Explore`
sanalmaydi: ular zanjir qadami emas, o'qish asbobi, va ularni cheklash
arzon yo'lni qimmat qiladi. Qolgan har qanday subagent (general-purpose,
boshqa plaginning agenti) `boshqa` hisobiga tushadi. Chegara unga faqat
shu so'rovda zanjir aktyori chaqirilgan bo'lsa qo'llanadi: aks holda
aktyor ishi nomsiz agent orqali cheksiz yurardi. Zanjirsiz oddiy ishda
general-purpose agent sanaladi, lekin to'silmaydi.
Nomdan faqat `manguberdi:` prefiksi kesiladi; `boshqa-plugin:review`
bu loyihaning `review` budjetini yemaydi.
"""

import contextlib
import json
import os
import re
import subprocess
import sys
import time

import geniuslib
import hookio

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = geniuslib.state_dir(ROOT)
LOG = os.path.join(STATE_DIR, "budget.json")

# Zanjir aktyorlari. Tartib chiqishdagi jadval tartibi.
ACTORS = ("rejalashtiruvchi", "dasturchi", "test-muhandis", "review")
LIMIT = 2

# O'qish asboblari: sanalmaydi.
FREE = ("qidiruv", "tahlil", "Explore")
# Qolgan subagentlar shu bitta hisobga tushadi.
OTHER = "boshqa"
# Plagin sifatida o'rnatilganda nom shu prefiks bilan keladi.
PREFIX = "manguberdi:"
GROUP_STATE = "genius-guruh.json"

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

# Bitta so'rovdagi jami agent (guruh va aktyordan qat'i nazar). Shundan
# keyin har AGENT_MAX-chi chaqiruvda foydalanuvchidan tasdiq so'raladi:
# aktyor chegarasi guruh bo'yicha bo'linadi va yolg'iz o'zi jami sonni
# to'xtatmaydi (2026-10-05/06: 18 review va 7 rejalashtiruvchi, ~$470).
try:
    AGENT_MAX = max(1, int(os.environ.get("GENIUS_AGENT_MAX", "5")))
except ValueError:
    AGENT_MAX = 5

# Bitta agentning o'lchangan o'rtacha narxi, dollar (usage.py, 2026-10-05/06:
# 18 sonnet review $263, 7 opus rejalashtiruvchi $199). Taxmin, hisob emas.
AGENT_COST = {"haiku": 2, "sonnet": 15, "opus": 28}

ASK = """Bu so'rovda %d-agent (%s, model %s). Chegara %d agent (GENIUS_AGENT_MAX).
Taxminiy narx: shu agent ~$%d, shu so'rovda hozirgacha ~$%d.
Har agent o'z kontekstini har chaqiruvda keshdan qayta o'qiydi: sarfning
asosiy qismi shu. Kamroq agent, arzonroq model yoki bitta umumiy review
yetmaydimi? Davom etish uchun tasdiqlang."""

BLOCKED = """%s uchun budjet tugadi: %d chaqiruv bo'ldi, chegara %d.

Uchinchi urinish o'rniga sabab aytiladi. Odatda u uchtadan biri:
  1. Aktyor birinchi martada qoidani ko'rmagan
     -> %s <fayllar> chiqishini tekshiring
  2. Reviewer boshqa mezon bilan tekshirgan
     -> ikkalasi bir xil ro'yxatni olishi kerak
  3. "Bajarildi" nimaligi aytilmagan
     -> qabul mezoni normalizatsiyada belgilanadi

Nima bajarildi, nima qolgan va nima yetishmayotganini yozib, aniq
savol bering. Foydalanuvchi javob bergach budjet o'zi yangilanadi.
Keyin memory bosqichi: qolgan kamchilik feedback nomzodi.
"""


GROUP_RE = re.compile(r"(?im)^\s*\[?guruh:\s*([\w.-]+)")


def strip_prefix(name):
    name = (name or "").strip()
    return name[len(PREFIX):] if name.startswith(PREFIX) else name


def actor_of(subagent_type):
    """subagent_type qaysi hisobga tushadi; '' sanalmaydi."""
    name = strip_prefix(subagent_type)
    if name in ACTORS:
        return name
    return "" if name in FREE else OTHER


def registered(group, cwd=""):
    """Id `guruh.py yarat` bilan ro'yxatga olinganmi.

    Holat fayli umumiy .git papkasida: guruh worktree sidan ham, asosiy
    daraxtdan ham bir xil fayl ko'rinadi. Tekshirib bo'lmasa (git yo'q,
    repo emas) id qabul qilinmaydi: umumiy hisob xavfsiz tomon.
    """
    try:
        from guruh import common_dir
        common = common_dir(cwd or os.getcwd())
        if not common:
            return False
        with open(os.path.join(common, GROUP_STATE), encoding="utf-8") as handle:
            data = json.load(handle)
    except (ImportError, OSError, ValueError, subprocess.SubprocessError):
        return False
    return isinstance(data, dict) and group in data


def group_of(prompt, cwd=""):
    """Promptdagi ro'yxatdan o'tgan `guruh: <id>`, aks holda ''."""
    match = GROUP_RE.search(prompt if isinstance(prompt, str) else "")
    if not match:
        return ""
    return match.group(1) if registered(match.group(1), cwd) else ""


def counter(actor, group=""):
    return "%s/%s" % (group, actor) if group else actor


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


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _count(value):
    return int(value) if _number(value) else 0


def _sound(slot):
    """Slot ishlatsa bo'ladigan shaklda bo'lsa o'zi (calls tuzatilgan), aks
    holda None. `seen: null` yoki `started: "x"` keyingi `now - ...` da
    TypeError berardi va budjet hooki HAMMA sessiyada jim o'chardi (KD-K2)."""
    if not isinstance(slot, dict):
        return None
    if any(key in slot and not _number(slot[key]) for key in ("started", "seen")):
        return None
    calls = slot.get("calls")
    slot["calls"] = ({k: v for k, v in calls.items() if _number(v)}
                     if isinstance(calls, dict) else {})
    if not isinstance(slot.get("ids", []), list):
        slot["ids"] = []
    return slot


def load():
    """{"sessions": {kalit: hisob}}. Eski tekis shakl bo'sh holat deb olinadi.

    Buzuq slot shu yerda bir marta tashlanadi: save, fresh, cli_key va
    slot_of undan keyin faqat son va dict ko'radi."""
    try:
        with open(LOG, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        data = None
    if not isinstance(data, dict) or not isinstance(data.get("sessions"), dict):
        data = {"sessions": {}}
    sessions = {}
    for key, slot in data["sessions"].items():
        slot = _sound(slot)
        if slot is not None:
            sessions[key] = slot
    data["sessions"] = sessions
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
        geniuslib.atomic_write_text(LOG, json.dumps(data))
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
        slot_of(data, key, cwd).update(task="", started=time.time(), calls={},
                                       total=0, spent=0)
        save(data)


def installed_line():
    """`o'rnatilgan: <sha>, klon: <sha>` yoki None (global o'rnatish yo'q).

    O'rnatuvchi `~/.claude/skills/manguberdi/.genius.json` ga snapshot
    commitini yozadi. Skill, aktyorlar va hooklar shu snapshotdan (R7.8
    XV-Y1), klon esa undan oldinga ketishi mumkin (`git pull`): farqni shu
    qator aytadi va yangilashni `tools/yangilash.py` bajaradi. Eski
    o'rnatishda (manifestda `clone` yo'q) asboblar klondan jonli edi.
    """
    config = (os.environ.get("CLAUDE_CONFIG_DIR")
              or os.path.join(os.path.expanduser("~"), ".claude"))
    try:
        with open(os.path.join(config, "skills", "manguberdi", ".genius.json"),
                  encoding="utf-8-sig") as handle:
            manifest = json.load(handle)
        installed = str(manifest.get("commit") or "")
    except (OSError, ValueError, AttributeError):
        return None
    pinned = bool(manifest.get("clone"))
    root = manifest.get("clone") or manifest.get("root") or ROOT
    proc = geniuslib.run_git(["-C", root, "rev-parse", "HEAD"], timeout=5)
    clone = proc.stdout.strip() if proc else ""
    line = "o'rnatilgan: %s, klon: %s" % (installed[:12] or "?", clone[:12] or "?")
    if installed and clone and installed != clone:
        if pinned:
            tool = os.path.join(str(manifest.get("root") or ""), "tools",
                                "yangilash.py").replace("\\", "/")
            line += (" (hooklar o'rnatilgan commitdan yuradi: ro'yxatni ko'rish va "
                     "yangilash uchun `python3 %s` (snapshotdagi nusxa), install/README.md "
                     "'Yangilash')" % tool)
        else:
            line += (" (farq bor: o'rnatuvchini qayta yurgizing, install/README.md "
                     "'Yangilash')")
    return line


def status():
    data = load()
    key, note = cli_key(data)
    slot = slot_of(data, key)
    version = installed_line()
    if version:
        print(version)
    if note:
        print(note)
    print("Vazifa: %s" % (slot.get("task") or "nomsiz"))
    groups = sorted({key.split("/", 1)[0] for key in slot["calls"] if "/" in key})
    for group in [""] + groups:
        if group:
            print("\nGuruh: %s" % group)
        print("\n%-18s %-10s %s" % ("aktyor", "chaqiruv", "holat"))
        rows = ACTORS + ((OTHER,) if slot["calls"].get(counter(OTHER, group)) else ())
        for actor in rows:
            used = slot["calls"].get(counter(actor, group), 0)
            state = "-" if not used else ("tugadi" if used >= LIMIT else "qoldi 1")
            print("%-18s %-10s %s" % (actor, "%d/%d" % (used, LIMIT), state))
    return 0


def restore(actor, group=""):
    name = counter(actor, group)
    with locked():
        data = load()
        key, note = cli_key(data)
        slot = slot_of(data, key, here())
        used = slot["calls"].get(name, 0)
        if used:
            slot["calls"][name] = used - 1
            save(data)
    if note:
        print(note)
    print("%s: %d/%d" % (name, slot["calls"].get(name, 0), LIMIT))
    return 0


def blocked(actor, used, group=""):
    """To'siq matni. Buyruq klon ichida nisbiy, boshqa proyektda mutlaq.

    Import xatosi to'siqni buzmasin: hook yiqilsa chaqiruv o'tib ketadi.
    """
    try:
        from check_code import tool_cmd
        rules = tool_cmd("rules_for.py")
    except (ImportError, OSError):
        rules = "python3 tools/rules_for.py"
    return BLOCKED % (counter(actor, group) if group else actor, used, LIMIT, rules)


def model_of(actor):
    """Aktyor faylidagi `model:`; topilmasa sonnet (subagent sukuti)."""
    path = os.path.join(ROOT, ".claude", "agents", actor + ".md")
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle.read(2000).splitlines():
                if line.startswith("model:"):
                    return line.split(":", 1)[1].strip() or "sonnet"
    except OSError:
        pass
    return "sonnet"


def ask_text(actor, total, spent):
    model = model_of(actor)
    cost = AGENT_COST.get(model, AGENT_COST["sonnet"])
    return ASK % (total, actor, model, AGENT_MAX, cost, spent + cost)


def chain_active(slot, group=""):
    """Shu so'rovda zanjir aktyori chaqirilganmi (manguberdi faol)."""
    return any(slot["calls"].get(counter(a, group)) for a in ACTORS)


def take(actor, key=None, cwd="", call_id=None, group=""):
    """Bitta chaqiruvni hisobga oladi: (xabar, ruxsat, tasdiq matni).

    Aktyor chegarasi oshsa ruxsat False. Jami agent AGENT_MAX dan oshib,
    har AGENT_MAX-chi chaqiruvga yetsa tasdiq matni bo'sh emas.

    key None bo'lsa CLI chaqiruvi: sessiya cli_key bilan tanlanadi.
    group bo'lsa hisob shu guruhniki: parallel guruhlar bir-birini to'smaydi.
    """
    raw = strip_prefix(actor)
    actor = actor_of(actor)
    if not actor:
        return "", True, ""        # o'qish asbobi erkin
    name = counter(actor, group)
    ask = ""
    with locked():
        data = load()
        if key is None:
            key, cwd = cli_key(data)[0], here()
        slot = slot_of(data, key, cwd)
        used = slot["calls"].get(name, 0)
        ids = slot.setdefault("ids", [])
        if call_id and call_id in ids:
            return "%s: %d/%d chaqiruv" % (name, used, LIMIT), True, ""
        over = used >= LIMIT and (actor != OTHER or chain_active(slot, group))
        if not over:
            slot["calls"][name] = used + 1
            total = _count(slot.get("total")) + 1
            spent = _count(slot.get("spent"))
            if total > AGENT_MAX and (total - AGENT_MAX - 1) % AGENT_MAX == 0:
                ask = ask_text(raw or actor, total, spent)
            model = model_of(raw) if raw else "sonnet"
            slot["total"] = total
            slot["spent"] = spent + AGENT_COST.get(model, AGENT_COST["sonnet"])
            if call_id:
                slot["ids"] = (ids + [call_id])[-SEEN_IDS:]
            save(data)
    if over:                       # matn qulfdan tashqarida yasaladi
        return blocked(actor, used, group), False, ""
    return "%s: %d/%d chaqiruv" % (name, used + 1, LIMIT), True, ask


def hook(payload):
    """PreToolUse: Task, Agent yoki SendMessage dagi aktyorni tekshiradi."""
    key = (payload.get("session_id")
           or os.environ.get("CLAUDE_CODE_SESSION_ID") or "")
    cwd = norm(payload.get("cwd"))
    if payload.get("hook_event_name") == "UserPromptSubmit":
        reset(key, cwd)            # jim: bu hook chiqishi kontekstga tushadi
        return 0
    tool = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return 0
    if tool in ("Task", "Agent"):
        actor = tool_input.get("subagent_type") or ""
        text = tool_input.get("prompt")
    elif tool == "SendMessage":
        actor = strip_prefix(tool_input.get("to"))
        if actor not in ACTORS:
            return 0               # asosiy sessiya, agentId yoki jamoa
        text = tool_input.get("message")
    else:
        return 0
    message, allowed, ask = take(actor, key, cwd, payload.get("tool_use_id"),
                                 group_of(text, cwd))
    if not allowed or ask:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny" if not allowed else "ask",
            "permissionDecisionReason": message if not allowed else ask,
        }}, sys.stdout)
    return 0


def main():
    args = sys.argv[1:]
    if not args:
        if sys.stdin.isatty():
            print(__doc__.strip().split("\n\n")[1].strip())
            return 2
        payload = hookio.read_payload()
        if payload is None or not hookio.active(payload):
            return 0   # hook o'z xatosi yoki o'rinsizligi bilan ishni to'xtatmaydi
        return hook(payload)
    if args[0] == "--holat":
        return status()
    if args[0] == "--yangi-vazifa":
        return new_task(args[1] if len(args) > 1 else "")
    group = ""
    if "--guruh" in args:
        at = args.index("--guruh")
        group = args[at + 1] if at + 1 < len(args) else ""
        args = args[:at] + args[at + 2:]
    if args[0] == "--tiklash":
        if len(args) < 2:
            print("foydalanish: budget.py --tiklash <aktyor> [--guruh <id>]",
                  file=sys.stderr)
            return 2
        return restore(args[1], group)
    if group and not registered(group, here()):
        print("guruh %s ro'yxatda yo'q (guruh.py yarat): umumiy hisob" % group)
        group = ""
    message, allowed, _ = take(args[0], group=group)
    print(message or "%s sanalmaydi (o'qish asbobi)" % args[0])
    return 0 if allowed else 1


if __name__ == "__main__":
    sys.exit(main())
