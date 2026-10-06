#!/usr/bin/env python3
"""Aktyor natijasini mexanik tekshirish: SubagentStop hooki.

`dasturchi` va `test-muhandis` ish oxirida `run_tests.py` ni yurgizishi
shart, javobida esa `run_tests exit=<kod>` qatori turadi
(`Testlar:` yoki `Natija:`). Bu matnda yozilgan edi va matn esdan
chiqadi: aktyor test yurgizmay "bajarildi" desa, xato partiya oxiridagi
to'liq suite gacha ko'rinmaydi. Hook ikki narsani tekshiradi:

1. javobda `run_tests exit=` qatori bor;
2. aktyorning oxirgi Edit/Write idan keyin `run_tests.py` jurnalida
   (`<holat>/run_tests.jsonl`) shu fayllar turgan ildiz uchun yozuv bor.
   Guruhda ildiz worktree papkasi: fayl o'sha yerda tahrirlanadi va
   `run_tests --ildiz <papka>` o'sha yo'lni yozadi.

Biri bajarilmasa `{"decision": "block", "reason": ...}`: aktyor
to'xtamaydi, shu chaqiruv ichida davom etadi. Yangi Agent chaqiruvi yo'q,
ya'ni budjetga tushmaydi.

Jim qoladigan holatlar (fail-open, hook o'z noaniqligi bilan ishni
to'smaydi):

- boshqa aktyor (`review`, `qidiruv`, general-purpose, ...);
- `hookio.active()` false: Java proyekti ham, klon ham emas;
- `stop_hook_active`: aktyor allaqachon shu hook tufayli davom etyapti.
  Ikkinchi to'xtashda u sababni yozgan bo'ladi (masalan rc 2, build
  topilmadi), cheksiz aylana bo'lmaydi;
- aktyor transkripti o'qilmadi yoki unda kod fayliga Edit/Write yo'q
  (faqat hujjat tegilgan, yoki aktyor ochiq savol bilan to'xtagan);
- `run_tests` "Ta'sirlangan test yo'q" degan: u holda jurnalga yozuv
  tushmaydi, lekin test yurgizish urinilgan.

Payload maydonlari rasmiy hujjatdan (hooks, SubagentStop): `agent_type`,
`agent_id`, `agent_transcript_path`, `last_assistant_message`,
`stop_hook_active`, `transcript_path`. `agent_type` bo'lmasa (eski
versiya) tur `agent-<id>.meta.json` dan, u ham bo'lmasa asosiy
transkriptdagi oxirgi Agent/Task chaqiruvidan olinadi.
"""

import contextlib
import datetime
import json
import os
import re
import sys

import hookio

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# run_tests.py bilan bir xil joy: jurnalni u yozadi.
STATE_DIR = (os.environ.get("GENIUS_STATE_DIR")
             or os.path.join(ROOT, ".claude", ".state"))
JOURNAL = os.path.join(STATE_DIR, "run_tests.jsonl")

CHECKED = ("dasturchi", "test-muhandis")
PREFIX = "manguberdi:"
EDIT_TOOLS = ("Edit", "Write", "MultiEdit", "NotebookEdit")
AGENT_TOOLS = ("Agent", "Task")
# Faqat shu kengaytmali fayl tegilgan bo'lsa test talab qilinmaydi:
# dasturchi.md ga ko'ra hujjat uchun "Testlar: yurgizilmadi va nega".
DOC_EXT = (".md", ".markdown", ".txt", ".rst", ".adoc")
LINE_RE = re.compile(r"run_tests\s+exit=\d+")
NO_TESTS = "Ta'sirlangan test yo'q"
# Isitish faqat kompilyatsiya qiladi, test yurmaydi.
NOT_A_RUN = ("isitish",)

REASON = """Aktyor javobi mexanik tekshiruvdan o'tmadi (tools/actor_check.py):
%s

Ish oxirida testni bir marta yurgizing: `python3 tools/run_tests.py --diff --yurgiz`
(guruhda kartadagi `test:` buyrug'i, `--ildiz <papka>` bilan), Bash timeout 600000.
Keyin javob shaklidagi qatorni yozing: dasturchi `Testlar: run_tests exit=<kod>, <N> sinf`,
test-muhandis `Natija: run_tests exit=<kod>: ...`. Yurgizib bo'lmasa (rc 2: --ildiz yoki
--asbob so'raldi, build topilmadi) shu qatorda sababini ayting; bu tekshiruv ikkinchi
marta to'xtatmaydi."""


def strip_prefix(name):
    name = (name or "").strip() if isinstance(name, str) else ""
    return name[len(PREFIX):] if name.startswith(PREFIX) else name


def entries(path):
    """JSONL transkript yozuvlari; o'qilmasa None."""
    if not isinstance(path, str) or not path:
        return None
    rows = []
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                with contextlib.suppress(ValueError):
                    row = json.loads(line)
                    if isinstance(row, dict):
                        rows.append(row)
    except OSError:
        return None
    return rows


def blocks(row):
    message = row.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    return content if isinstance(content, list) else []


def epoch(stamp):
    try:
        moment = datetime.datetime.fromisoformat(str(stamp or "").replace("Z", "+00:00"))
    except ValueError:
        return None
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=datetime.timezone.utc)
    return moment.timestamp()


def agent_path(payload):
    """Aktyor transkripti: maydon, bo'lmasa asosiy transkript yonidagi
    `<sessiya>/subagents/agent-<id>.jsonl`."""
    path = payload.get("agent_transcript_path")
    if isinstance(path, str) and os.path.isfile(path):
        return path
    main, agent = payload.get("transcript_path"), payload.get("agent_id")
    if not (isinstance(main, str) and main.endswith(".jsonl")
            and isinstance(agent, str) and agent):
        return None
    folder = os.path.join(main[:-len(".jsonl")], "subagents")
    for name in (agent, "agent-" + agent):
        candidate = os.path.join(folder, name + ".jsonl")
        if os.path.isfile(candidate):
            return candidate
    return None


def last_agent_call(path):
    """Asosiy transkriptdagi oxirgi Agent/Task chaqiruvining subagent_type i."""
    found = ""
    for row in entries(path) or []:
        for block in blocks(row):
            if (isinstance(block, dict) and block.get("type") == "tool_use"
                    and block.get("name") in AGENT_TOOLS):
                tool_input = block.get("input")
                if isinstance(tool_input, dict) and tool_input.get("subagent_type"):
                    found = str(tool_input["subagent_type"])
    return found


def agent_type(payload, transcript):
    for key in ("agent_type", "subagent_type"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    if transcript:
        with contextlib.suppress(OSError, ValueError):
            with open(transcript[:-len(".jsonl")] + ".meta.json", encoding="utf-8") as handle:
                meta = json.load(handle)
            if isinstance(meta, dict) and isinstance(meta.get("agentType"), str):
                return meta["agentType"]
    return last_agent_call(payload.get("transcript_path"))


def scan(rows, cwd):
    """(kod fayliga tahrirlar [(vaqt, yo'l)], oxirgi matn, natijalar [(vaqt, matn)])."""
    edits, results, last_text = [], [], ""
    for row in rows:
        moment = epoch(row.get("timestamp"))
        for block in blocks(row):
            if not isinstance(block, dict):
                continue
            kind = block.get("type")
            if kind == "tool_use" and block.get("name") in EDIT_TOOLS:
                tool_input = block.get("input") if isinstance(block.get("input"), dict) else {}
                path = tool_input.get("file_path") or tool_input.get("notebook_path")
                if isinstance(path, str) and path and moment is not None \
                        and not path.lower().endswith(DOC_EXT):
                    edits.append((moment, os.path.join(cwd, path)))
            elif kind == "tool_result" and moment is not None:
                results.append((moment, json.dumps(block.get("content"), ensure_ascii=False)))
            elif kind == "text" and row.get("type") == "assistant":
                last_text = str(block.get("text") or "")
    return edits, last_text, results


def inside(path, root):
    """Fayl shu ildizning o'z daraxtidami. Guruh worktree si sukut bo'yicha
    asosiy daraxt ichida (`.claude/worktrees/`): asosiy ildizdagi yurish
    guruh faylini sinamaydi, shuning uchun bunday yo'l mos emas."""
    try:
        path = os.path.normcase(os.path.realpath(path))
        root = os.path.normcase(os.path.realpath(root))
        if os.path.commonpath([path, root]) != root:
            return False
    except (OSError, ValueError):
        return False
    parts = os.path.relpath(path, root).replace("\\", "/").split("/")
    return not any(a == ".claude" and b == "worktrees" for a, b in zip(parts, parts[1:]))


def journal_has(files, since):
    """Jurnalda `since` dan keyin, fayllardan biri turgan ildiz uchun yurish bormi."""
    with contextlib.suppress(OSError):
        with open(JOURNAL, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                with contextlib.suppress(ValueError, TypeError):
                    row = json.loads(line)
                    root = row.get("root")
                    if (isinstance(root, str) and row.get("ts", 0) >= int(since)
                            and row.get("mode") not in NOT_A_RUN
                            and any(inside(f, root) for f in files)):
                        return True
    return False


def problems(payload):
    """To'xtashni to'sish sabablari; bo'sh ro'yxat - jim."""
    if payload.get("stop_hook_active"):
        return []
    transcript = agent_path(payload)
    if strip_prefix(agent_type(payload, transcript)) not in CHECKED:
        return []
    rows = entries(transcript)
    if not rows:
        return []
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else ""
    edits, last_text, results = scan(rows, cwd)
    if not edits:
        return []
    message = payload.get("last_assistant_message")
    if not isinstance(message, str) or not message.strip():
        message = last_text
    since = max(moment for moment, _ in edits)
    found = []
    if not LINE_RE.search(message):
        found.append("- javobda `run_tests exit=<kod>` qatori yo'q")
    no_tests = any(moment >= since and NO_TESTS in text for moment, text in results)
    if not no_tests and not journal_has([path for _, path in edits], since):
        last = sorted({path for _, path in edits})[:3]
        found.append("- oxirgi Edit/Write dan keyin run_tests jurnalida shu ildiz uchun "
                     "yurish yo'q (fayllar: %s)" % ", ".join(last))
    return found


def main():
    payload = hookio.read_payload()
    if payload is None or not hookio.active(payload):
        return 0   # hook o'z xatosi yoki o'rinsizligi bilan ishni to'xtatmaydi
    found = problems(payload)
    if found:
        # ASCII JSON: Windows konsol kod sahifasidan qat'i nazar o'qiladi.
        json.dump({"decision": "block", "reason": REASON % "\n".join(found)},
                  sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
