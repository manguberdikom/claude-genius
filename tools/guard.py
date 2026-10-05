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

Chegaralangan o'qish o'tadi: kichik bo'lakli Read, sed oralig'i, grep, head,
`Get-Content -TotalCount`. Tashxis buyruqlari ham o'tadi: docker ps,
docker logs, docker images, psql --version.

Bash va PowerShell asboblari bir xil tekshiriladi: Windows da Git Bash
bo'lmasa PowerShell asbobi yoqiladi, va faqat Bash tekshirilsa docker,
baza va katta fayl to'siqlari jim o'chib qolardi.
"""

import glob
import json
import os
import re
import sys

import hookio

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
# bo'lishi mumkin. Prefiks bayrog'i qiymat olishi mumkin: `sudo -u postgres
# psql` dagi "postgres" buyruq emas. Yangi satr ham ajratgich, shuning
# uchun heredoc tanasi tekshiruvdan oldin olib tashlanadi (strip_heredoc).
CMD = (r"(?:^|[|;&\n(]\s*|\$\(\s*|`\s*)"
       r"(?:(?:sudo|time|env|nohup|nice|exec)(?:\s+-\S+(?:\s+[^\s|;&-][^\s|;&]*)??)*\s+"
       r"|[A-Za-z_]\w*=\S*\s+)*")

# Faylni boshdan oxirigacha oqizadigan buyruqlar. Argumentlar oralig'ida
# '>' bo'lishi mumkin emas: shunda `cat > fayl <<EOF ...` kabi YOZISH
# buyrug'i noto'g'ri to'silmaydi.
SLURP_RE = re.compile(CMD + r"(?:cat|bat|less|more|most|view|tac|nl)\s+([^|;&\n>]*)")
# PowerShell da o'qish fe'li registrga befarq; `cat` va `type` ham
# Get-Content taxallusi. Bash da `type` faylni o'qimaydi, shuning uchun bu
# naqsh faqat PowerShell asbobiga qo'llanadi.
PS_SLURP_RE = re.compile(CMD + r"(?:get-content|gc|type|cat)\s+([^|;&\n>]*)", re.I)
# Get-Content ning satr chegarasi (First va Head TotalCount taxallusi,
# Last esa Tail taxallusi): bo'lak cheklangan, o'qish o'tadi.
PS_BOUNDED_RE = re.compile(r"(?:^|\s)-(?:TotalCount|Head|Tail|First|Last)\b", re.I)

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
# Konteyner yoki pod ichida buyruq yurgizish: `docker compose -f x.yml exec`,
# `kubectl -n prod exec`.
EXEC = (r"(?:(?:docker|podman)(?:-compose|\s+compose)?|kubectl)(?:" + DOCKER_FLAG
        + r")*\s+exec\b")

# Pul va vaqt sarflaydigan amallar. Tashxis fe'llari (ps, logs, images,
# inspect, version) ataylab yo'q: ular arzon va ko'pincha aynan kerak.
EXPENSIVE = (
    (re.compile(CMD + r"(?:docker|podman)(?:-compose|\s+compose)?(?:" + DOCKER_FLAG
                + r")*\s+(?:container\s+|image\s+)?" + VERB),
     "Konteyner ko'tarish yoki yig'ish",
     "Avval arzon yo'lni sinang: test chiqishidagi xato odatda sababni "
     "aytadi, baza tuzilishini esa entity sinflari ko'rsatadi:\n"
     "  {schema} <src>\n"
     "Konteyner haqiqatan kerak bo'lsa: COST_OK=1 <buyruq>"),
    # Skript nomi buyruq o'rnida turishi shart. Aks holda uni shunchaki
    # ATAGAN buyruq ham to'siladi: `wc -l install/x.ps1`, `git add x.ps1`.
    # Bu amalda uchradi, o'rnatuvchi faylni yozayotganda.
    # Papkali yo'l ham: `.\\install\\x.ps1`, `C:/a/x.ps1`. PowerShell
    # asbobida ham to'siladi: proyekt qoidasi skript yurgizishni taqiqlaydi,
    # oddiy PowerShell buyrug'i (Get-ChildItem) esa o'tadi.
    (re.compile(CMD + r"(?:pwsh|powershell(?:\.exe)?)\b"
                r"|" + CMD + r"(?:[.]{1,2}[/\\])?(?:[\w.:~-]+[/\\])*[\w.-]*\.ps1\b"),
     "PowerShell skripti",
     "PowerShell skripti yurgizilmaydi: u boshqa mashinada tekshirilmagan\n"
     "bo'ladi. Shu ishni python3 (yoki bash) bilan bajaring, ular shu yerda\n"
     "sinaladi."),
    # Har qanday ulanish, lokal ham: hostsiz `psql shop` ham jonli bazani
    # ochadi. Faqat versiya va yordam o'tadi. Konteyner yoki pod ichidagi
    # klient ham ulanish. Naqsh qo'shtirnoq olib tashlangandan keyin
    # qo'llanadi (strip_quoted): `grep 'psql' .` to'silmaydi, qo'shtirnoqli
    # URI bilan `psql` esa to'siladi. Tekshiruv keyingi buyruqqa o'tmaydi.
    (re.compile(CMD + DB_CLIENT + r"(?!\s+(?:--version|--help|-V)\b)"
                r"|" + CMD + EXEC + r"[^|;&\n]*?\s" + DB_CLIENT),
     "Bazaga ulanish",
     "Sxemani bilish uchun ulanish shart emas, entity sinflari uni "
     "to'liq tasvirlaydi:\n"
     "  {schema} <src>\n"
     "Jonli ma'lumot haqiqatan kerak bo'lsa: COST_OK=1 <buyruq>"),
)

# Maslahat matnlari shablon: yo'llar to'siq paytida qo'yiladi (commands).
HINT = (
    "Butun faylni o'qish o'rniga indeksdan foydalaning:\n"
    "  {doc} find [-f] <so'rov>      - bo'limni topish\n"
    "  {doc} show <hujjat> <raqam>   - faqat o'sha bo'limni o'qish\n"
    "  {doc} outline <hujjat> [bob]  - ichidagi bo'limlar\n"
    "Batafsil: {claude_md}"
)


def commands():
    """Maslahatdagi yo'llar: klon ichida nisbiy, boshqa proyektda mutlaq.

    Global o'rnatishda hook boshqa proyektda yuradi, u yerda
    `tools/doc.sh` va `CLAUDE.md` yo'q: maslahat "No such file" ga olib
    borardi. Shuning uchun matn modul darajasida emas, to'siq paytida
    yasaladi. Yordamchi ham faqat shu paytda yuklanadi: hook har Read va
    Bash chaqiruvida ishlaydi, ruxsat holatida import kerak emas.
    """
    from docref import in_clone, tool_cmd
    claude_md = "CLAUDE.md"
    if not in_clone():
        claude_md = os.path.join(ROOT, claude_md).replace("\\", "/")
    return {"doc": tool_cmd("doc.sh"),
            "schema": tool_cmd("schema_from_entities.py"),
            "claude_md": claude_md}


def deny(reason):
    deny_with(reason, HINT)


def deny_with(reason, hint):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason + "\n" + hint.format(**commands()),
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


def check_bash(tool_input, powershell=False):
    command = tool_input.get("command") or ""
    check_cost(command)
    regex = PS_SLURP_RE if powershell else SLURP_RE
    for match in regex.finditer(strip_heredoc(command)):
        args = match.group(1)
        if powershell:
            if PS_BOUNDED_RE.search(args):
                continue
            # `docs\patterns\x.md` va vergul bilan bir nechta yo'l.
            args = args.replace("\\", "/").replace(",", " ")
        files = sorted({f for arg in args.split() for f in slurped(arg)})
        size = sum(os.path.getsize(f) for f in files)
        if size > MAX_BYTES:
            deny("Bu buyruq %d KB ni butunligicha oqizadi: %s"
                 % (size // 1000, ", ".join(os.path.relpath(f, ROOT) for f in files[:3])))


def main():
    payload = hookio.read_payload()
    if payload is None:
        return  # hook hech qachon chaqiruvni o'z xatosi tufayli to'smaydi
    tool_input = payload.get("tool_input") or {}
    name = payload.get("tool_name")
    if name == "Read":
        check_read(tool_input)
    elif name in ("Bash", "PowerShell"):
        check_bash(tool_input, powershell=name == "PowerShell")


if __name__ == "__main__":
    main()
