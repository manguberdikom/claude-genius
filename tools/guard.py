#!/usr/bin/env python3
"""PreToolUse hook: qimmat amallarni to'xtatib, arzon yo'lni ko'rsatadi.

Ikki xil qimmatlik bor va ikkalasi ham shu yerda tekshiriladi, chunki
alohida hook har Bash chaqiruvida ikkinchi marta Python ishga tushirardi.

1. Kontekst qimmatligi. docs/ dagi bob o'n minglab token, bitta bo'lim
   esa ~700. Butun faylni o'qish kontekstni yoqadi, holbuki javob kichik
   bo'lakda turadi. Fayllar ro'yxati yozilmagan: har chaqiruvda o'qiladigan
   bo'lakning bayti sanaladi, shuning uchun yangi bob qo'shilsa ham ishlaydi.

2. Pul va vaqt qimmatligi. Konteyner ko'tarish yoki bazaga ulanish bir
   necha daqiqa va katta chiqish beradi, holbuki kerakli javob ko'pincha
   kodning o'zida: entity sinflari sxemani to'liq tasvirlaydi, test
   chiqishi esa xatoni aytib turadi. Bu amallar to'siladi, lekin yo'l
   yopiq emas: buyruq oldiga COST_OK=1 qo'yilsa o'tadi.

Chegaralangan o'qish o'tadi: kichik bo'lakli Read, sed oralig'i, grep, head.
Tashxis buyruqlari ham o'tadi: docker ps, docker logs, docker images.
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Shu papkalardagi markdown fayllar kuzatiladi.
WATCHED_DIRS = ("docs", "dist")

# Bir o'qishda bundan ko'p bayt qaytsa to'siladi. Bo'lim o'rtacha 1.7 KB,
# eng kattasi 5.6 KB, ya'ni chegara bir necha bo'limga yetadi. Satr soni
# o'lchov emas: 1100 satrlik bob 138 KB (Read uni 70k token deb sanadi),
# zich bobda 300 satr esa 40 KB. doc.sh show bilan bitta o'zgaruvchi va
# bitta standart qiymat.
MAX_BYTES = int(os.environ.get("DOC_MAX_BYTES", "16000"))
# Read limit berilmasa shuncha satr qaytaradi.
READ_DEFAULT_LINES = 2000

# Buyruq boshi: ajratgichdan keyin, oldida sudo/time/env yoki VAR=qiymat
# bo'lishi mumkin. Yangi satr ham ajratgich, shuning uchun heredoc tanasi
# tekshiruvdan oldin olib tashlanadi (strip_heredoc).
CMD = (r"(?:^|[|;&\n(]\s*|\$\(\s*|`\s*)"
       r"(?:(?:sudo|time|env|nohup|nice|exec)(?:\s+-\S+)*\s+|[A-Za-z_]\w*=\S*\s+)*")

# Faylni boshdan oxirigacha oqizadigan buyruqlar. Argumentlar oralig'ida
# '>' bo'lishi mumkin emas: shunda `cat > fayl <<EOF ...` kabi YOZISH
# buyrug'i noto'g'ri to'silmaydi.
SLURP_RE = re.compile(CMD + r"(?:cat|bat|less|more|most|view|tac|nl)\s+([^|;&\n>]*)")

HEREDOC_RE = re.compile(
    r"<<-?\s*(['\"]?)(\w+)\1[^\n]*(?:\n.*?)??(?:\n[ \t]*\2[ \t]*(?=\n|$)|\Z)", re.S)

# Buyruq oldiga qo'yilsa, qimmat amal baribir bajariladi.
ESCAPE = "COST_OK=1"

# docker fe'li. Fe'ldan keyin yo'l yoki fayl nomi belgisi kelmasin:
# `-f build/compose.yml ps` dagi "build" fe'l emas.
VERB = r"(?:up|run|build|pull|start|create)(?![\w./-])"
# Bayroq qiymat bilan yoki qiymatsiz: `-f x.yml`, `--profile dev`, `-d`.
# `--?\w` bir ma'noli, shuning uchun regex qaytish (backtracking) qilib
# osilib qolmaydi.
DOCKER_FLAG = r"\s+--?\w[\w-]*(?:[ =](?!" + VERB + r")[^\s|;&-][^\s|;&]*)?"
DB_CLIENT = r"(?:psql|mysql|mariadb|mongosh|mongo|redis-cli)\b"

# Pul va vaqt sarflaydigan amallar. Tashxis fe'llari (ps, logs, images,
# inspect, version) ataylab yo'q: ular arzon va ko'pincha aynan kerak.
EXPENSIVE = (
    (re.compile(CMD + r"(?:docker|podman)(?:-compose|\s+compose)?(?:" + DOCKER_FLAG
                + r")*\s+(?:container\s+|image\s+)?" + VERB),
     "Konteyner ko'tarish yoki yig'ish",
     "Avval arzon yo'lni sinang: test chiqishidagi xato odatda sababni "
     "aytadi, baza tuzilishini esa entity sinflari ko'rsatadi:\n"
     "  python3 tools/schema_from_entities.py <src>\n"
     "Konteyner haqiqatan kerak bo'lsa: COST_OK=1 <buyruq>"),
    # Skript nomi buyruq o'rnida turishi shart. Aks holda uni shunchaki
    # ATAGAN buyruq ham to'siladi: `wc -l install/x.ps1`, `git add x.ps1`.
    # Bu amalda uchradi, o'rnatuvchi faylni yozayotganda.
    (re.compile(CMD + r"(?:pwsh|powershell(?:\.exe)?)\b"
                r"|" + CMD + r"(?:[.]{1,2}[/\\])?[\w.-]*\.ps1\b"),
     "PowerShell skripti",
     "Bu muhitda PowerShell ishlatilmaydi va u yozilgan skript boshqa\n"
     "mashinada tekshirilmagan bo'ladi. Shu ishni bash yoki python3 bilan\n"
     "bajaring; ikkalasi ham shu yerda sinaladi."),
    # Host yoki URL bilan ulanish, yoki konteyner ichidagi klient. `\s-h`
    # `--help` ni ushlamaydi. Tekshiruv keyingi buyruqqa o'tib ketmaydi.
    (re.compile(CMD + DB_CLIENT + r"(?=[^|;&\n]*(?:\s-h|--host|://))"
                r"|" + CMD + r"(?:docker|podman)(?:-compose|\s+compose)?\s+exec\b"
                r"[^|;&\n]*\b" + DB_CLIENT),
     "Bazaga ulanish",
     "Sxemani bilish uchun ulanish shart emas, entity sinflari uni "
     "to'liq tasvirlaydi:\n"
     "  python3 tools/schema_from_entities.py <src>\n"
     "Jonli ma'lumot haqiqatan kerak bo'lsa: COST_OK=1 <buyruq>"),
)

HINT = (
    "Butun faylni o'qish o'rniga indeksdan foydalaning:\n"
    "  tools/doc.sh find [-f] <so'rov>      - bo'limni topish\n"
    "  tools/doc.sh show <hujjat> <raqam>   - faqat o'sha bo'limni o'qish\n"
    "  tools/doc.sh outline <hujjat> [bob]  - ichidagi bo'limlar\n"
    "Batafsil: CLAUDE.md"
)


def deny(reason):
    deny_with(reason, HINT)


def deny_with(reason, hint):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason + "\n" + hint,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


def watched_path(candidate):
    """Kuzatiladigan papkadagi markdown faylning to'liq yo'li, aks holda None."""
    if not candidate.endswith(".md"):
        return None
    for base in (os.getcwd(), ROOT):
        full = os.path.normpath(os.path.join(base, candidate))
        try:
            rel = os.path.relpath(full, ROOT)
        except ValueError:
            continue
        head = rel.split(os.sep)[0]
        if head in WATCHED_DIRS and os.path.isfile(full):
            return full
    return None


def slice_bytes(path, offset=None, limit=None):
    """Read qaytaradigan bo'lakning bayt hajmi: offset dan limit satr."""
    start = max(offset if isinstance(offset, int) else 1, 1) - 1
    stop = start + (limit if isinstance(limit, int) and limit > 0 else READ_DEFAULT_LINES)
    total = 0
    try:
        with open(path, "rb") as handle:
            for number, line in enumerate(handle):
                if number >= stop:
                    break
                if number >= start:
                    total += len(line)
    except OSError:
        return 0
    return total


def check_read(tool_input):
    full = watched_path(tool_input.get("file_path") or "")
    if full is None:
        return
    limit = tool_input.get("limit")
    limit = limit if isinstance(limit, int) and limit > 0 else None
    size = slice_bytes(full, tool_input.get("offset"), limit)
    if size <= MAX_BYTES:
        return
    what = "chegarasiz o'qilmoqda" if limit is None else "limit=%d" % limit
    deny("%s - %s, %d KB qaytadi (chegara %d KB)."
         % (os.path.relpath(full, ROOT), what, size // 1000, MAX_BYTES // 1000))


QUOTED_RE = re.compile(r"'[^']*'|\"[^\"]*\"")


def strip_quoted(command):
    """Qo'shtirnoq ichidagi matnni bo'sh joyga almashtiradi.

    `grep -n 'docker run' .` buyrug'i konteyner ko'tarmaydi, u shu haqda
    QIDIRADI. Naqsh ichidagi so'zni chaqiruv deb o'qish qidiruvning
    o'zini to'sib qo'yadi. Bu amalda uchradi: qo'riqchi shu repoda
    o'z sozlamalarini qidirgan buyruqni to'xtatdi.
    """
    return QUOTED_RE.sub(lambda m: " " * len(m.group(0)), command)


def strip_heredoc(command):
    """Heredoc tanasini olib tashlaydi, `<<EOF` qatori qoladi.

    Tana buyruq emas, matn: `cat > notes <<EOF` ichidagi "docker run"
    yoki fayl nomi chaqiruv deb o'qilmasligi kerak.
    """
    return HEREDOC_RE.sub(lambda m: m.group(0).split("\n", 1)[0], command)


def check_cost(command):
    """Konteyner va baza chaqiruvlari: arzon yo'l bor ekan, to'xtatiladi.

    Bu odatga qarshi to'siq, xavfsizlik chegarasi emas: `bash -c` ichiga
    yashirilgan buyruqni u ko'rmaydi va ko'rishga urinmaydi ham.
    """
    if ESCAPE in command:
        return
    command = strip_quoted(strip_heredoc(command))
    for pattern, what, hint in EXPENSIVE:
        match = pattern.search(command)
        if match:
            found = match.group(0).lstrip(" \t\n|;&(`$").strip()
            deny_with("%s qimmat amal: %s" % (what, found), hint)


def slurped(arg):
    """Argument ko'rsatgan kuzatiladigan fayllar: qo'shtirnoq va glob bilan."""
    arg = arg.strip("'\"")
    if not any(ch in arg for ch in "*?["):
        full = watched_path(arg)
        return {full} if full else set()
    found = set()
    for base in (os.getcwd(), ROOT):
        for path in glob.glob(os.path.join(base, arg)):
            full = watched_path(path)
            if full:
                found.add(full)
    return found


def check_bash(tool_input):
    command = tool_input.get("command") or ""
    check_cost(command)
    for match in SLURP_RE.finditer(strip_heredoc(command)):
        files = sorted({f for arg in match.group(1).split() for f in slurped(arg)})
        size = sum(os.path.getsize(f) for f in files)
        if size > MAX_BYTES:
            deny("Bu buyruq %d KB ni butunligicha oqizadi: %s"
                 % (size // 1000, ", ".join(os.path.relpath(f, ROOT) for f in files[:3])))


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return  # hook hech qachon chaqiruvni o'z xatosi tufayli to'smaydi
    if not isinstance(payload, dict):
        return
    tool_input = payload.get("tool_input") or {}
    name = payload.get("tool_name")
    if name == "Read":
        check_read(tool_input)
    elif name == "Bash":
        check_bash(tool_input)


if __name__ == "__main__":
    main()
