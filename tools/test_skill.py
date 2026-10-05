#!/usr/bin/env python3
"""Skill va agent fayllarining tuzilishini tekshiradi.

    python3 tools/test_skill.py

check_docs.py havolalarni tekshiradi: fayl bormi, anchor bormi, asbob
bormi. Bu yerda boshqa narsa tekshiriladi: fayl o'zi to'g'ri yozilganmi.
Buzilgan frontmatter yoki noma'lum model nomi jim ishlamaydi - skill
yuklanmaydi yoki agent boshqa modelda ishlaydi va hech kim bilmaydi.
Matndagi doc.sh raqami indeksda borligi va `tools/` prefiksi, agent
modeli manguberdi/SKILL.md dagi taqsimotga mosligi, `## Asboblar`
bo'limlari va settings.json dagi hook ulanishi ham tekshiriladi.
"""

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILLS = os.path.join(ROOT, ".claude", "skills")
AGENTS = os.path.join(ROOT, ".claude", "agents")
INDEX = os.path.join(ROOT, "index")
SETTINGS = os.path.join(ROOT, ".claude", "settings.json")
sys.path.insert(0, HERE)

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

# doc.sh buyrug'i aniq raqam bilan. show bob yoki bo'lim oladi, path
# faqat bo'lim, outline va checklist faqat bob. `2.*` kabi wildcard
# qo'llanmaydi: buyruq "topilmadi" beradi, tekshiruv esa jim o'tardi.
DOC_REF_RE = re.compile(
    r"doc\.sh (show|path|outline|checklist)(?: --force)? ([a-z-]+) ([0-9][^\s`'\"),]*)")
# tools/ prefiksisiz doc.sh: rewrite_paths uni mutlaq qilmaydi va global
# o'rnatishda buyruq ishlamaydi. Argumentsiz eslatma tutilmaydi.
BARE_DOC_RE = re.compile(
    r"(?<![\w/])doc\.sh (?:show|find|outline|checklist|rule|path|toc)\s+[-\w]")
# Sonar qo'llanmasiga ishlaydigan yo'l: rule yoki sonarqube bobi.
SONAR_RE = re.compile(r"doc\.sh (?:rule java:|(?:show|outline|checklist) sonarqube\b)")

# references/ havolasi: nisbiy (o'z skilli) va to'liq (istalgan skill).
LOCAL_REF_RE = re.compile(r"(?<![\w/.-])references/([\w-]+\.md)")
FULL_REF_RE = re.compile(r"\.claude/skills/([\w-]+)/references/([\w-]+\.md)")

MODEL_RE = re.compile(r"\b(haiku|sonnet|opus|fable)\b")
# Hook matcher qismlari shu nomlardan bo'lsin: "Taskk" kabi xato jim
# o'tsa, hook hech qachon ishga tushmaydi.
HOOK_TOOLS = {"Read", "Bash", "PowerShell", "Task", "Agent", "Write", "Edit",
              "MultiEdit", "NotebookEdit", "Grep", "Glob", "WebFetch",
              "WebSearch"}
# Hook skripti o'z asboblarini ushlashi shart: kengaytirish mumkin,
# tushirib qoldirish yo'q. Matcher faqat asbob hodisalarida bor:
# UserPromptSubmit va Stop uni o'qimaydi, budget.py u yerda hisobni
# nolga tushirish uchun ulangan.
HOOK_MUST_MATCH = {"guard": {"Read", "Bash"}, "budget": {"Task", "Agent"},
                   "check_code": {"Write", "Edit"}}
TOOL_EVENTS = {"PreToolUse", "PostToolUse"}

errors = []


def err(where, msg):
    errors.append("%s: %s" % (where, msg))


def section(text, title):
    """`## <title>` bo'limi matni, keyingi `## ` gacha."""
    match = re.search(r"^## %s[^\n]*\n(.*?)(?=^## |\Z)" % re.escape(title),
                      text, re.M | re.S)
    return match.group(1) if match else None


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

    # references/ ga havola qilingan fayl mavjudmi. Nisbiy yo'l o'z
    # skilliga, `.claude/skills/<skill>/references/...` esa o'sha skillga.
    base = os.path.dirname(path)
    own = os.path.basename(base)
    linked = set(LOCAL_REF_RE.findall(text))
    for ref in linked:
        if not os.path.exists(os.path.join(base, "references", ref)):
            err(rel, "references/%s yo'q" % ref)
    for skill, ref in set(FULL_REF_RE.findall(text)):
        if not os.path.exists(os.path.join(SKILLS, skill, "references", ref)):
            err(rel, "skills/%s/references/%s yo'q" % (skill, ref))
        elif kind == "skill" and skill == own:
            linked.add(ref)

    # Teskari yo'nalish: SKILL.md tilga olmagan reference faylni model
    # hech qachon ochmaydi. U jim eskiradi va qoidasi ikki joyda yashaydi.
    refdir = os.path.join(base, "references")
    if kind == "skill" and os.path.isdir(refdir):
        for ref in sorted(os.listdir(refdir)):
            if ref.endswith(".md") and ref not in linked:
                err(rel, "references/%s hech qayerdan havola qilinmagan" % ref)


def known_refs():
    """Indeksdagi (hujjat, raqam): bo'limlar va boblar alohida."""
    from docref import ensure_index
    out = {}
    for name in ("sections.tsv", "chapters.tsv"):
        ensure_index(name)
        rows = set()
        path = os.path.join(INDEX, name)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as handle:
                handle.readline()
                for line in handle:
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) > 1 and parts[1]:
                        rows.add((parts[0], parts[1]))
        out[name] = rows
    return out["sections.tsv"], out["chapters.tsv"]


def check_doc_refs(path, secs, chs, bare=True):
    """bare=False: proyektning o'z CLAUDE.md si, u yerda nisbiy yo'l to'g'ri."""
    rel = os.path.relpath(path, ROOT)
    text = open(path, encoding="utf-8").read()
    for m in DOC_REF_RE.finditer(text):
        cmd, doc, ref = m.group(1), m.group(2), m.group(3).rstrip(".")
        if re.search(r"[A-Z]", ref):
            continue    # `25.N` kabi o'rinbosar, o'quvchi raqam qo'yadi
        if cmd in ("outline", "checklist"):
            ok = (doc, ref) in chs
        elif cmd == "path":
            ok = (doc, ref) in secs
        else:
            ok = (doc, ref) in secs or (doc, ref) in chs
        if not ok:
            err(rel, "doc.sh %s %s %s indeksda yo'q" % (cmd, doc, ref))
    for m in (BARE_DOC_RE.finditer(text) if bare else ()):
        err(rel, "tools/ prefiksisiz doc.sh: %s" % m.group(0).strip())


def check_models(agents):
    """Agent modeli manguberdi/SKILL.md dagi `## Model tanlash` ga mos.

    Taqsimot testga qattiq yozilmaydi: yagona manba hujjatdagi bo'lim,
    test esa frontmatter undan chetga chiqmaganini ko'radi. haiku dan
    opus ga jim o'tish narxni ~4 baravar oshiradi.
    """
    path = os.path.join(SKILLS, "manguberdi", "SKILL.md")
    if not os.path.exists(path):
        return
    sec = section(open(path, encoding="utf-8").read(), "Model tanlash")
    if sec is None:
        err("manguberdi/SKILL.md", "`## Model tanlash` bo'limi yo'q")
        return
    planned = {}
    for m in re.finditer(r"`([a-z-]+)`", sec):
        model = MODEL_RE.search(sec, m.end())
        if model:
            planned.setdefault(m.group(1), model.group(1))
    for agent in agents:
        name = os.path.splitext(os.path.basename(agent))[0]
        front, _ = front_matter(agent)
        model = (front or {}).get("model", "").split("-")[0]
        rel = os.path.relpath(agent, ROOT)
        if name not in planned:
            err(rel, "manguberdi/SKILL.md `## Model tanlash` da yo'q")
        elif model and model != planned[name]:
            err(rel, "model %s, manguberdi/SKILL.md da %s"
                % (model, planned[name]))


def check_tool_sections(skills):
    """manguberdi dan boshqa skill `## Asboblar` da doc.sh ni biladi.

    Bob jadvali bor skill bo'limni o'qish yo'lini ham beradi: jadval
    faqat bob nomini aytadi, `doc.sh show` siz model butun bobni ochadi.
    """
    for path in skills:
        if os.path.basename(os.path.dirname(path)) == "manguberdi":
            continue
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8").read()
        sec = section(text, "Asboblar")
        if sec is None:
            err(rel, "`## Asboblar` bo'limi yo'q: skill asboblarni bilmaydi")
        elif "doc.sh" not in sec:
            err(rel, "`## Asboblar` da doc.sh yo'q")
        elif (re.search(r"^## [^\n]*bob jadvali", text, re.M | re.I)
              and "doc.sh show" not in sec):
            err(rel, "bob jadvali bor, lekin `## Asboblar` da doc.sh show yo'q")


def check_hooks():
    """settings.json dagi har hook skripti bor va matcher to'g'ri."""
    if not os.path.exists(SETTINGS):
        return
    rel = os.path.relpath(SETTINGS, ROOT)
    try:
        hooks = json.load(open(SETTINGS, encoding="utf-8")).get("hooks", {})
    except ValueError as exc:
        err(rel, "JSON buzuq: %s" % exc)
        return
    wired = set()
    for event, groups in hooks.items():
        for group in groups:
            matcher = group.get("matcher", "")
            parts = set(matcher.split("|")) if matcher else set()
            for part in parts - HOOK_TOOLS:
                err(rel, "%s: noma'lum matcher qismi '%s'" % (event, part))
            for hook in group.get("hooks", []):
                for script in re.findall(r"tools/(\w+)\.py",
                                         hook.get("command", "")):
                    if not os.path.exists(os.path.join(HERE, script + ".py")):
                        err(rel, "%s: tools/%s.py yo'q" % (event, script))
                    if event not in TOOL_EVENTS:
                        continue
                    wired.add(script)
                    missing = HOOK_MUST_MATCH.get(script, set()) - parts
                    if missing:
                        err(rel, "%s: %s matcher'ida %s yo'q"
                            % (event, script, ", ".join(sorted(missing))))
    for script in sorted(set(HOOK_MUST_MATCH) - wired):
        err(rel, "tools/%s.py hech bir asbob hodisasiga ulanmagan" % script)


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

    check_models(agents)
    check_tool_sections(skills)
    check_hooks()

    secs, chs = known_refs()
    if not secs or not chs:
        err("index", "indeks yasalmadi: doc.sh havolalari tekshirilmadi")
    else:
        for path in sorted(glob.glob(os.path.join(ROOT, ".claude", "**", "*.md"),
                                     recursive=True)):
            check_doc_refs(path, secs, chs)
        claude_md = os.path.join(ROOT, "CLAUDE.md")
        if os.path.exists(claude_md):
            check_doc_refs(claude_md, secs, chs, bare=False)

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

    # Talab shunday: Sonar qo'llanmasini TO'RTTALASI ishlatadi. Bu
    # o'z-o'zidan ko'rinmaydi, chunki hech narsa yiqilmaydi: aktyor
    # shunchaki sifat darvozasini bilmay ishlaydi va kamchilik keyin
    # chiqadi. Ikkitasi aynan shu holatda topildi.
    sonar_actors = ("arxitektor", "test-muhandis", "rejalashtiruvchi", "review")
    for name in sonar_actors:
        path = os.path.join(AGENTS, name + ".md")
        if not os.path.exists(path):
            continue
        body = open(path, encoding="utf-8").read().lower()
        if not SONAR_RE.search(body):
            err("agents/%s.md" % name, "Sonar qo'llanmasiga ishlaydigan yo'l "
                "yo'q (doc.sh rule yoki sonarqube bobi)")

    if errors:
        print("\n%d XATO:" % len(errors))
        for e in errors:
            print("  - %s" % e)
        return 1
    print("Hammasi joyida.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
