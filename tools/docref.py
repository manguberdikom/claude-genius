#!/usr/bin/env python3
"""Mavzu yoki Sonar kalitini qo'llanmadagi bo'limga bog'laydi.

Ikkita asbob buni talab qiladi (schema_from_entities.py va check_code.py),
shuning uchun mantiq shu yerda: nusxa ko'chirilsa, biri tuzatilganda
ikkinchisi eskirib qolardi.

Topilma faqat "shunday qilma" desa, uni tekshirib bo'lmaydi. Bo'lim
raqami bilan kelsa, o'qib solishtirish mumkin. Shuning uchun har bir
topilma shu funksiyadan o'tadi. Bo'lim topilmasligi topilma noto'g'ri
degani emas: qo'llanma ma'lumotnoma, hamma holatni qamramaydi.
"""

import os
import re
import subprocess
import sys

import geniuslib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX = os.path.join(ROOT, "index")
BUILD = os.path.join(HERE, "build_index.py")

_cache = {}
_files = {}
_checked = False


def ensure_index(name=""):
    """Indeks yo'q, chala yoki eskirgan bo'lsa bir marta yasaydi.

    Indeks hosila va git ga kirmaydi. U yo'q bo'lganda bu modul avval
    jim turib bo'sh ro'yxat qaytarardi: topilmalar chiqar, lekin bo'lim
    raqami yo'q, va nega yo'qligini hech kim aytmasdi. Bob tahrirlangandan
    keyin esa eski bo'lim raqamini berardi. Fayllar birga yasaladi,
    shuning uchun tekshiruv butun indeks bo'yicha; `name` chaqiruvchi qaysi
    faylga tayanishini bildiradi xolos.

    build_index.py to'g'ridan-to'g'ri chaqiriladi, bash shart emas: doc.sh
    orqali chaqirilganda Windows da indeks hech qachon yasalmasdi. Alohida
    jarayonda, chunki build() chiqishi check_code hookining JSON iga
    aralashmasin.
    """
    global _checked
    if _checked:
        return
    _checked = True   # yasash yiqilsa ham ikkinchi marta urinilmaydi
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        import build_index   # faqat kerak bo'lganda yuklanadi
        if build_index.is_fresh():
            return
    except (ImportError, SyntaxError):
        return   # yasovchining o'zi buzuq: bor indeks bilan davom etiladi
    try:
        subprocess.run([sys.executable or "python3", BUILD],
                       stdin=subprocess.DEVNULL, capture_output=True,
                       timeout=120, check=False)
    except (OSError, subprocess.SubprocessError):
        pass


def _rows(name):
    if name in _cache:
        return _cache[name]
    ensure_index(name)
    path = os.path.join(INDEX, name)
    rows = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            handle.readline()
            for line in handle:
                rows.append(line.rstrip("\n").split("\t"))
    _cache[name] = rows
    return rows


def _body(doc, section):
    """Bo'lim tanasi, sections.tsv dagi satr oralig'i bo'yicha."""
    for parts in _rows("sections.tsv"):
        if len(parts) >= 7 and parts[0] == doc and parts[1] == section:
            rel, start, end = parts[4], int(parts[5]), int(parts[6])
            if rel not in _files:
                try:
                    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
                        _files[rel] = f.read().split("\n")
                except OSError:
                    _files[rel] = []
            return "\n".join(_files[rel][start - 1:end])
    return ""


def by_ref(ref):
    """Aniq havola ("code-review 19.2") indeksda bo'lsa o'zi, bo'lmasa "".

    Raqam satr sifatida solishtiriladi: 24.10 va 24.1 boshqa bo'limlar.
    """
    doc, _, num = ref.partition(" ")
    name = "sections.tsv" if "." in num else "chapters.tsv"
    for parts in _rows(name):
        if len(parts) >= 2 and parts[0] == doc and parts[1] == num:
            return ref
    return ""


def by_rule(rule, term=""):
    """Sonar kaliti -> "<hujjat> <raqam>".

    rules.tsv ko'zga tashlanish bo'yicha saralangan, shuning uchun `term`
    berilmasa birinchi mos qator olinadi. Ulush ba'zan kalitni
    yo'l-yo'lakay eslatgan kichik bo'limni uni tushuntirgan bo'limdan
    yuqori qo'yadi. `term` (topilmaning o'zidagi so'z, masalan
    `printStackTrace`) berilsa, bo'lim qatorlaridan tanasida shu so'z ko'p
    uchragani olinadi, tenglikni ulush hal qiladi.
    """
    rows = [p for p in _rows("rules.tsv") if len(p) >= 6 and p[0] == rule]
    if not rows:
        return ""
    best = rows[0]
    sections = [p for p in rows if p[3]]
    if term and sections:
        best = max(sections, key=lambda p: (_body(p[1], p[3]).count(term),
                                            float(p[5])))
    return "%s %s" % (best[1], best[3] or best[2])


def by_topic(topic):
    """Inglizcha atama -> "<hujjat> <raqam>".

    Avval aynan moslik, keyin qavsli bezak bilan turgan nom: jadvalda
    "Money (Value Object specialization)", so'rovda esa "Money". Oddiy
    prefiks olinmaydi: u "Enum" ni "Enum Singleton" ga, "Index" ni
    "Index Table" ga olib borardi.
    """
    low = topic.lower()
    prefix = None
    for parts in _rows("aliases.tsv"):
        if len(parts) != 4 or parts[2] != "section":
            continue
        name = parts[0].lower()
        if name == low:
            return "%s %s" % (parts[1], parts[3])
        if prefix is None and name.startswith(low + " ("):
            prefix = "%s %s" % (parts[1], parts[3])
    return prefix or ""


def resolve(topic, rule="", ref="", term=""):
    """Bo'lim havolasi yoki bo'sh satr.

    Tartib aniqlik bo'yicha: topilma bilgan bo'lim, keyin Sonar kaliti,
    oxirida taxallus. Indeksda yo'q havola keyingisiga o'tadi.
    """
    return ((by_ref(ref) if ref else "")
            or (by_rule(rule, term) if rule else "")
            or by_topic(topic))


def quote(path):
    """Bo'sh joy bo'lsa qo'shtirnoq (rewrite_paths.quote bilan bir xil)."""
    return '"%s"' % path if " " in path else path


def _git(args, cwd):
    proc = geniuslib.run_git(args, cwd=cwd)
    return proc.stdout if proc and proc.returncode == 0 else ""


# Klonda turadigan memory papkalari. Klon ochiq repo, shuning uchun unga
# faqat hammaga tegishli bilim (`umumiy`) va klonning o'z proyekti
# (`claude-genius`) yoziladi. guard.SHARED_MEMORY shu ro'yxat bilan bir xil.
SHARED_MEMORY = ("umumiy", "claude-genius")


def _top(here):
    """Proyekt ildizi: git daraxtining tepasi, git bo'lmasa papkaning o'zi."""
    return _git(["rev-parse", "--show-toplevel"], here).strip() or here


def memory_home(cwd=None):
    """Klondan tashqari proyektlar memorysi: GENIUS_MEMORY_DIR, sukut
    `<workspace>/docs-local/memory` (docs_base). Har chaqiruvda o'qiladi.

    Global o'rnatishda boshqa proyektning vazifa, qaror va fayl nomlari
    ochiq klon reposiga tushmasligi uchun (R0.5). Memory proyekt
    hujjatlari yonida turadi, git ga kirmaydi va push qilinmaydi
    (ensure_local); uy papkasiga yozilmaydi.
    """
    given = os.environ.get("GENIUS_MEMORY_DIR", "").strip()
    if given:
        return os.path.abspath(os.path.expanduser(given))
    return os.path.join(docs_base(cwd), "memory")


def clone():
    """Klon: yoziladigan memory shu yerda. Global o'rnatishda ROOT pin
    qilingan snapshot, klon esa `GENIUS_CLONE` (geniuslib.clone_root,
    R7.8 XV-Y1); o'rnatilmagan holatda ikkalasi bir xil."""
    return geniuslib.clone_root(ROOT)


def is_clone_project(cwd=None):
    """Joriy proyekt qo'llanma klonining o'zimi (pastki papkasi ham)."""
    top = _top(cwd or os.getcwd())
    return (os.path.normcase(os.path.realpath(top))
            == os.path.normcase(os.path.realpath(clone())))


def memory_root(cwd=None):
    """Proyekt memorysi ildizi: klonda `memory/`, boshqa proyektda
    memory_home()."""
    if is_clone_project(cwd):
        return os.path.join(clone(), "memory")
    return memory_home(cwd)


def memory_dir(slug, cwd=None):
    """Bitta slug papkasi. `umumiy` va `claude-genius` har doim klonda."""
    if slug in SHARED_MEMORY:
        return os.path.join(clone(), "memory", slug)
    return os.path.join(memory_root(cwd), slug)


def ensure_local(path):
    """Papkani yaratadi va uning `docs-local` ildizini git dan chiqaradi.

    `docs-local` git daraxti ichida bo'lsa (workspace o'zi repo), u shu
    reponing `.git/info/exclude` iga qo'shiladi: commit ham, push ham
    bo'lmaydi, repo `.gitignore` iga tegilmaydi. Yo'lni qaytaradi.
    """
    try:
        os.makedirs(path, exist_ok=True)
        _exclude_docs_local(path)
    except (OSError, ValueError) as exc:
        # Papka yozilmasa (read-only mount, `docs-local` fayl) yo'l baribir
        # qaytadi: chaqiruvchi yiqilmasin, sabab bir qatorda.
        print("docs-local: %s (%s)" % (path, exc), file=sys.stderr)
    return path


def _exclude_docs_local(path):
    """`docs-local` ildizini o'z reposining `.git/info/exclude` iga qo'shadi."""
    base = os.path.realpath(path)
    while os.path.basename(base) != "docs-local":
        parent = os.path.dirname(base)
        if parent == base:
            return
        base = parent
    parent = os.path.dirname(base)
    top = _git(["rev-parse", "--show-toplevel"], parent).strip()
    git_dir = _git(["rev-parse", "--git-common-dir"], parent).strip()
    if not top or not git_dir:
        return
    rel = os.path.relpath(base, os.path.realpath(top))
    if rel.startswith(".."):
        return
    # --path-format=absolute git 2.31+ da: eski gitda ham ishlashi uchun
    # nisbiy natija chaqiruv papkasiga qo'shiladi.
    exclude = os.path.join(parent, git_dir, "info", "exclude")
    line = "/" + rel.replace(os.sep, "/") + "/"
    text = ""
    if os.path.exists(exclude):
        with open(exclude, encoding="utf-8") as handle:
            text = handle.read()
    if line in {l.strip() for l in text.split("\n")}:
        return
    os.makedirs(os.path.dirname(exclude), exist_ok=True)
    with open(exclude, "a", encoding="utf-8", newline="\n") as handle:
        handle.write(("\n" if text and not text.endswith("\n") else "") + line + "\n")


def project_slug(cwd=None, memory=None):
    """memory/README.md qoidasi: repo nomi kichik harfda, ikki egada bir
    xil nom bo'lsa `<egasi>__<repo>`, repo yo'q bo'lsa ildiz papka nomi.

    rules_for va handoff shu bitta funksiyani ishlatadi: avval handoff
    `<egasi>__<repo>` ni bilmas, proyekt indeksini topshiriqdan tushirardi.
    `<egasi>__<repo>` papkasi proyekt memorysi turgan joyda qidiriladi
    (memory_root), `memory` berilsa o'sha yerda.
    """
    here = cwd or os.getcwd()
    # Klonning memorysi har doim `claude-genius` da (memory/README.md),
    # fork yoki remote nomidan qat'i nazar.
    if is_clone_project(here):
        return SHARED_MEMORY[1]
    top = _top(here)
    url = _git(["remote", "get-url", "origin"], top).strip().rstrip("/")
    parts = [p for p in re.split(r"[/:]", url) if p]
    if not parts:
        return os.path.basename(os.path.normpath(top)).lower()
    repo = parts[-1].lower()
    repo = repo[:-4] if repo.endswith(".git") else repo
    if len(parts) > 1:
        both = "%s__%s" % (parts[-2].lower(), repo)
        if os.path.isdir(os.path.join(memory or memory_root(top), both)):
            return both
    return repo


def in_clone():
    """Joriy papka qo'llanma klonining o'zimi."""
    try:
        here = os.path.realpath(os.getcwd())
    except OSError:
        return False
    return os.path.normcase(here) == os.path.normcase(os.path.realpath(clone()))


def tool_cmd(name):
    """Xabardagi buyruq. Klon ichida nisbiy, ya'ni allow ro'yxatiga mos;
    boshqa proyektda mutlaq, aks holda u yerda "No such file" beradi.

    Klondan tashqarida Python o'rnatuvchi settings.json env ga yozgan
    GENIUS_PYTHON bilan: Windows da `python3` Store stub'i bo'lishi mumkin,
    allow qoidasi ham aynan shu yo'l bilan yozilgan (rewrite_paths.tool_cmd).
    """
    if in_clone():
        return ("" if name.endswith(".sh") else "python3 ") + "tools/" + name
    full = quote(os.path.join(ROOT, "tools", name).replace("\\", "/"))
    if name.endswith(".sh"):
        return "bash " + full
    runner = os.environ.get("GENIUS_PYTHON") or "python3"
    return quote(runner.replace("\\", "/")) + " " + full


def hint(topic, rule="", ref="", term=""):
    """Foydalanuvchiga ko'rsatiladigan bir qatorlik yo'l-yo'riq.

    Klon ichida chiqish o'zgarmaydi (`tools/doc.sh ...`), boshqa proyektda
    esa mutlaq yo'l beriladi: nisbiy buyruq u yerda ishlamasdi.
    """
    found = resolve(topic, rule, ref, term)
    cmd = tool_cmd("doc.sh")
    if found:
        return "qo'llanma: %s show %s" % (cmd, found)
    return "qo'llanma: %s find \"%s\"" % (cmd, topic)


def docs_dir(cwd=None):
    """Proyekt hujjatlari (reja, review hisoboti, talab, handover, ADR)
    turadigan papka. Hujjat proyekt git reposiga YOZILMAYDI.

    `GENIUS_DOCS_DIR/<repo-nomi>/`; berilmasa proyekt git ildizining OTA
    papkasidagi `docs-local/<repo-nomi>/`, ya'ni `<workspace>/docs-local/<repo>/`.
    Workspace git repo bo'lmasa u git ga tushmaydi; bo'lsa `docs-local/`
    ni foydalanuvchi o'zi `.git/info/exclude` ga qo'shadi (asbob repo
    `.gitignore` iga tegmaydi).

    Guruh worktree si (`.claude/worktrees/genius-<id>`) asosiy repoga
    ulangan: `--git-common-dir` orqali asosiy repo nomi olinadi, shuning
    uchun guruh va asosiy sessiya bitta papkani o'qiydi. Papka yaratilmaydi:
    yozuvchi `os.makedirs` qiladi. Har chaqiruvda o'qiladi.
    """
    here = cwd or os.getcwd()
    top = _repo_top(here)
    if not top:
        # Git bo'lmagan workspace (bir nechta repo turgan papka): hujjatlar uning o'zida, repo nomisiz.
        return docs_base(here)
    return os.path.join(docs_base(here), os.path.basename(os.path.normpath(top)))


def _repo_top(here):
    """Asosiy repo ildizi (guruh worktree si ham asosiy repoga); git yo'q bo'lsa ''."""
    if not _git(["rev-parse", "--show-toplevel"], here).strip():
        return ""
    top = _top(here)
    common = _git(["rev-parse", "--path-format=absolute", "--git-common-dir"],
                  here).strip()
    if common and os.path.basename(os.path.normpath(common)) == ".git":
        top = os.path.dirname(os.path.normpath(common))
    return top


def docs_base(cwd=None):
    """`docs-local` ildizi: GENIUS_DOCS_DIR, aks holda repo ildizining ota
    papkasidagi (git bo'lmasa joriy papkadagi) `docs-local`."""
    given = os.environ.get("GENIUS_DOCS_DIR", "").strip()
    if given:
        return os.path.abspath(os.path.expanduser(given))
    here = cwd or os.getcwd()
    top = _repo_top(here)
    if not top and not cwd and os.environ.get("CLAUDE_PROJECT_DIR"):
        # Git bo'lmagan workspace ning pastki papkasidan chaqirilsa ham
        # docs-local workspace ildizida bitta bo'lsin.
        here = os.environ["CLAUDE_PROJECT_DIR"]
        top = _repo_top(here)
    if not top:
        return os.path.join(here, "docs-local")
    return os.path.join(os.path.dirname(os.path.normpath(top)), "docs-local")
