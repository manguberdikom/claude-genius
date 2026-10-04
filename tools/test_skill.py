#!/usr/bin/env python3
"""Skill va agent fayllarining tuzilishini tekshiradi.

    python3 tools/test_skill.py

check_docs.py havolalarni tekshiradi: fayl bormi, anchor bormi, asbob
bormi. Bu yerda boshqa narsa tekshiriladi: fayl o'zi to'g'ri yozilganmi.
Buzilgan frontmatter yoki noma'lum model nomi jim ishlamaydi - skill
yuklanmaydi yoki agent boshqa modelda ishlaydi va hech kim bilmaydi.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, ".claude", "skills")
AGENTS = os.path.join(ROOT, ".claude", "agents")

FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
FIELD_RE = re.compile(r"^(\w+):\s*(.*)$", re.M)

VALID_MODELS = {"haiku", "sonnet", "opus", "fable"}
VALID_TOOLS = {"Bash", "Read", "Grep", "Glob", "Edit", "Write",
               "WebFetch", "WebSearch", "NotebookEdit"}
# Umumiy narxni cost_report.py o'lchaydi, bu yerda faqat chetga chiqish
# tutiladi. Mavjud tavsiflar 420-860 bayt oralig'ida; chegarani ularning
# o'rtasiga qo'yish har bir faylni belgilagan bo'lardi va bunday test
# e'tiborsiz qoldiriladi.
MAX_DESC = 900
MAX_SKILL_LINES = 500   # tana shundan uzun bo'lsa, references ga bo'linadi

errors = []


def err(where, msg):
    errors.append("%s: %s" % (where, msg))


def front_matter(path):
    text = open(path, encoding="utf-8").read()
    match = FRONT_RE.match(text)
    if not match:
        return None, text
    return dict(FIELD_RE.findall(match.group(1))), text


def check(path, kind):
    rel = os.path.relpath(path, ROOT)
    front, text = front_matter(path)
    if front is None:
        err(rel, "frontmatter yo'q yoki fayl boshida emas")
        return

    name = front.get("name", "")
    if not name:
        err(rel, "name yo'q")
    else:
        expected = (os.path.basename(os.path.dirname(path)) if kind == "skill"
                    else os.path.splitext(os.path.basename(path))[0])
        if name != expected:
            err(rel, "name '%s' fayl nomi '%s' bilan mos emas" % (name, expected))

    desc = front.get("description", "")
    if not desc:
        err(rel, "description yo'q: usiz skill hech qachon ishga tushmaydi")
    elif len(desc) > MAX_DESC:
        err(rel, "description %d bayt, chegara %d" % (len(desc), MAX_DESC))

    if kind == "agent":
        model = front.get("model", "")
        if not model:
            err(rel, "model yo'q: aktyor qaysi modelda ishlashi aniqlanmagan")
        elif model.split("-")[0] not in VALID_MODELS:
            err(rel, "noma'lum model: %s" % model)
        tools = [t.strip() for t in front.get("tools", "").split(",") if t.strip()]
        if not tools:
            err(rel, "tools yo'q")
        for tool in tools:
            if tool not in VALID_TOOLS:
                err(rel, "noma'lum asbob: %s" % tool)

    lines = text.count("\n")
    if kind == "skill" and lines > MAX_SKILL_LINES:
        err(rel, "%d satr, chegara %d: tafsilot references ga chiqarilsin"
            % (lines, MAX_SKILL_LINES))

    # references/ ga havola qilingan fayl mavjudmi
    base = os.path.dirname(path)
    for ref in set(re.findall(r"`?references/([\w-]+\.md)`?", text)):
        if not os.path.exists(os.path.join(base, "references", ref)):
            err(rel, "references/%s yo'q" % ref)


def main():
    skills = sorted(
        os.path.join(SKILLS, d, "SKILL.md") for d in os.listdir(SKILLS)
        if os.path.exists(os.path.join(SKILLS, d, "SKILL.md"))
    ) if os.path.isdir(SKILLS) else []
    agents = sorted(
        os.path.join(AGENTS, f) for f in os.listdir(AGENTS)
        if f.endswith(".md")
    ) if os.path.isdir(AGENTS) else []

    for path in skills:
        check(path, "skill")
    for path in agents:
        check(path, "agent")

    print("%d skill, %d agent tekshirildi" % (len(skills), len(agents)))

    # Orkestrator aktyorlarni nom bilan chaqiradi: nom yo'q bo'lsa,
    # marshrut jadvali mavjud bo'lmagan aktyorga yo'naltiradi.
    orchestrator = os.path.join(SKILLS, "manguberdi", "SKILL.md")
    if os.path.exists(orchestrator):
        text = open(orchestrator, encoding="utf-8").read()
        have = {os.path.splitext(os.path.basename(p))[0] for p in agents}
        for actor in re.findall(r"`([a-z-]+)`", text):
            if actor.endswith((".md", ".py", ".sh")) or "/" in actor:
                continue
            if actor in {"docs", "memory"} or actor in have:
                continue
            if actor in {"rejalashtiruvchi", "arxitektor", "test-muhandis",
                         "review", "qidiruv", "tahlil"}:
                err("manguberdi/SKILL.md", "aktyor yo'q: %s" % actor)

    if errors:
        print("\n%d XATO:" % len(errors))
        for e in errors:
            print("  - %s" % e)
        return 1
    print("Hammasi joyida.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
