#!/usr/bin/env python3
"""Hujjatlar sog'ligini tekshiradi. CI da ham, lokal ham bir xil ishlaydi.

    python3 tools/check_docs.py

Tekshiradi:
  1. Fayl hajmi   - GitHub 1 MB dan katta markdown ni render qilmaydi.
  2. Havolalar    - har bir nisbiy havola va anchor haqiqatan mavjudmi.
  3. Kirill       - hujjat o'zbek lotin yozuvida, kirill harf bo'lmasin.
                    Ildizdagi DECISIONS.md ham shu tekshiruvdan o'tadi:
                    u har .md fayl kabi md_files() ga tushadi.
  3b. Em-dash     - loyiha qoidasi: em-dash va en-dash ishlatilmaydi.
  3c. Kod fence   - ``` soni juft bo'lishi kerak, aks holda render buziladi;
                    docs/ da ochiluvchi fence til belgisiz bo'lmasin.
  4. Manifest     - docs/manifest.json diskdagi fayllar bilan mos.
  5. Skilllar     - .claude/ ichidagi docs/ havolalari haqiqiy; tools/
                    yo'llari (kod bloki ichida ham) skill, agent, CLAUDE.md,
                    README.md, CONTRIBUTING.md va install/README.md da
                    mavjud, doc.sh subkomandasi doc.sh da bor; har bob
                    kamida bitta skill yoki agent jadvalida turadi.
  6. Struktura    - har bob faylida metadata manifest bilan mos, breadcrumb
                    (3-qator), H1 manifest sarlavhasi (5-qator), bo'lim soni
                    manifest, README va <summary> bilan mos, footer qo'shni
                    boblarga ishora qiladi va oxirida turadi.
  7. Konvensiya   - har bobning oxirgi `##` bo'limi `Amalda qo'llash` yoki
                    `Arxitektor nazorat ro'yxati`.
  8. Regressiya   - tools/known_errors.tsv dagi naqsh qaytib kelmaganmi.
                    Tuzatilgan mazmun xatosi keyingi tahrirda jim
                    qaytib kelishi mumkin, shuning uchun u naqsh bo'lib
                    yoziladi va shu yerda qo'riqlanadi.
  9. Sonlar       - README.md, CLAUDE.md va install/README.md da qo'lda
                    yozilgan "N bob" va "N bo'lim" manifestdan
                    hisoblangan songa mos. Qator hujjat nomini aytsa
                    aynan o'shasi, aytmasa hech bo'lmaganda biror
                    hujjatning yoki jamining soni bo'lishi kerak.
"""
import json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE_LIMIT = 900_000          # GitHub chegarasi 1 048 576; zahira bilan
RE_REMOVE = re.compile(r"[^\w\- ]", re.UNICODE)
SKIP_DIRS = {'.git', 'dist', 'node_modules'}
# Hech qaysi skill yoki agent jadvalida turmasligi ataylab bo'lgan boblar:
# kalit (hujjat, bob raqami), qiymat sabab. Hozir bo'sh, ya'ni har bobga
# marshrut bor; yangi bob yo'lsiz qolsa tekshiruv xato beradi.
UNROUTED_OK = {}

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def gh_slug(text):
    t = text.replace('`', '')
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'\*\*([^*]*)\*\*', r'\1', t)
    t = t.strip().lower().replace("'", "").replace("’", "")
    return RE_REMOVE.sub('', t).replace(' ', '-')


def md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            if fn.endswith('.md'):
                yield os.path.relpath(os.path.join(dirpath, fn), ROOT)


def strip_fences(text):
    """Kod bloklari ichidagi satrlarni bo'sh qiladi, qolganini saqlaydi."""
    out, fence = [], False
    for l in text.split('\n'):
        if l.startswith('```'):
            fence = not fence
            out.append('')
            continue
        out.append('' if fence else l)
    return '\n'.join(out)


def strip_inline_code(text):
    """`...` ichidagi matn markdown da havola emas - havola tekshiruvida o'tkazib yuboriladi."""
    return re.sub(r'`[^`\n]*`', lambda m: ' ' * len(m.group(0)), text)


def heading_anchors(text):
    seen, anchors = {}, set()
    for l in strip_fences(text).split('\n'):
        if re.match(r'^#{1,6} ', l):
            base = gh_slug(re.sub(r'^#+ ', '', l))
            n = seen.get(base, 0)
            seen[base] = n + 1
            anchors.add(base if n == 0 else f"{base}-{n}")
    return anchors


def known_errors():
    """known_errors.tsv dagi qatorlar: [(naqsh, regex, izoh, qamrov)]."""
    path = os.path.join(ROOT, 'tools', 'known_errors.tsv')
    if not os.path.exists(path):
        return []
    rows, header = [], None
    with open(path, encoding='utf-8') as handle:
        for line in handle:
            line = line.rstrip('\n')
            if not line.strip() or line.startswith('#'):
                continue
            parts = line.split('\t')
            if header is None:
                header = parts
                continue
            pattern = parts[0].strip()
            note = parts[1].strip() if len(parts) > 1 else ''
            scope = parts[2].strip() if len(parts) > 2 else ''
            scopes = {s.strip() for s in scope.split(',') if s.strip()}
            try:
                rx = re.compile(pattern, re.I)
            except re.error as exc:
                err(f"tools/known_errors.tsv: naqsh buzuq -> {pattern} ({exc})")
                continue
            rows.append((pattern, rx, note, scopes or {'docs', 'claude', 'root'}))
    return rows


def scope_of(rel):
    """Fayl qaysi qamrovga tegishli: docs, claude yoki root."""
    head = rel.replace('\\', '/').split('/')[0]
    if head == 'docs':
        return 'docs'
    if head == '.claude':
        return 'claude'
    return 'root'


# Regressiya tekshiruvi o'z naqshlarini o'zi ham ushlab qolmasin.
REGRESSION_SKIP = {'tools/known_errors.tsv'}


def check_regression(files):
    """8. known_errors.tsv dagi naqsh docs/, .claude/ yoki ildizda topilmasin."""
    rows = known_errors()
    if not rows:
        return
    # Ildizda faqat qoida matni o'qiladigan fayllar; butun repo emas.
    root_docs = ('README.md', 'CONTRIBUTING.md', 'CLAUDE.md', 'DECISIONS.md',
                 'GLOSSARY.md', 'install/README.md')
    targets = [f for f in files if scope_of(f) in ('docs', 'claude')]
    targets += [f for f in root_docs if os.path.exists(os.path.join(ROOT, f))]
    for rel in sorted(set(targets)):
        if rel in REGRESSION_SKIP:
            continue
        where = scope_of(rel)
        try:
            text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        except OSError:
            continue
        for pattern, rx, note, scopes in rows:
            if where not in scopes:
                continue
            match = rx.search(text)
            if match:
                line = text[:match.start()].count('\n') + 1
                err(f"{rel}:{line}: tuzatilgan xato qaytdi -> {pattern} "
                    f"({note})")


# 9. Qo'lda yozilgan sonlar shu fayllarda tekshiriladi. docs/*/README.md
# bu yerda yo'q: undagi bob bo'yicha sonlarni 6-tekshiruv solishtiradi.
COUNT_DOCS = ('README.md', 'CLAUDE.md', 'install/README.md')
COUNT_RE = re.compile(r"(\d+)\s+(bob|bo'lim)\b")


def check_counts(manifest):
    """9. "N bob" va "N bo'lim" manifestdan hisoblangan songa mos."""
    chapters = {key: len(doc.get('chapters', [])) for key, doc in manifest.items()}
    sections = {key: sum(c.get('sections', 0) for c in doc.get('chapters', []))
                for key, doc in manifest.items()}
    totals = {'bob': sum(chapters.values()), "bo'lim": sum(sections.values())}
    allowed = {'bob': set(chapters.values()) | {totals['bob']},
               "bo'lim": set(sections.values()) | {totals["bo'lim"]}}
    per_doc = {'bob': chapters, "bo'lim": sections}

    for rel in COUNT_DOCS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        text = strip_fences(open(path, encoding='utf-8').read())
        for number, line in enumerate(text.split('\n'), 1):
            # Qator qaysi hujjat haqida: `docs/<kalit>/` yoki `<kalit>`.
            named = [k for k in manifest
                     if 'docs/%s/' % k in line or '`%s`' % k in line]
            for match in COUNT_RE.finditer(line):
                value, unit = int(match.group(1)), match.group(2)
                if len(named) == 1:
                    want = per_doc[unit][named[0]]
                    if value != want:
                        err(f"{rel}:{number}: {value} {unit} yozilgan, "
                            f"{named[0]} da {want} ta (manifestdan)")
                elif value not in allowed[unit]:
                    err(f"{rel}:{number}: {value} {unit} hech bir hujjatga "
                        f"va jamiga ({totals[unit]}) mos emas")


def main():
    files = list(md_files())
    anchors = {}
    for rel in files:
        text = open(os.path.join(ROOT, rel), encoding='utf-8').read()
        anchors[rel] = heading_anchors(text)

        # 1. hajm
        size = os.path.getsize(os.path.join(ROOT, rel))
        if size > SIZE_LIMIT:
            err(f"{rel}: {size} bayt > {SIZE_LIMIT} - GitHub bu faylni render qilmaydi, bo'lish kerak")

        # 3. kirill
        cyr = sorted({c for c in text if 'CYRILLIC' in unicodedata.name(c, '')})
        if cyr:
            err(f"{rel}: kirill harflar topildi: {''.join(cyr)}")

        # 3c. kod fence juftligi. docs/ da ochiluvchi fence til belgisiz
        # bo'lmasin: belgisiz blokni GitHub rangsiz chiqaradi va o'quvchi
        # u kodmi yoki matnmi bilmaydi.
        fences, fence = 0, False
        in_docs = rel.replace(os.sep, '/').startswith('docs/')
        for n, l in enumerate(text.split('\n'), 1):
            if not l.startswith('```'):
                continue
            fences += 1
            if in_docs and not fence and l.rstrip() == '```':
                err(f"{rel}:{n}: kod blokida til belgisi yo'q (text, java, sql, ...)")
            fence = not fence
        if fences % 2:
            err(f"{rel}: kod fence soni juft emas ({fences} ta ```), render buziladi")

        # 3b. em-dash / en-dash
        dashes = text.count('\u2014') + text.count('\u2013')
        if dashes:
            err(f"{rel}: {dashes} ta em-dash/en-dash topildi, oddiy tire (-) ishlatilsin")

    # 2. havolalar
    total = 0
    for rel in files:
        text = strip_inline_code(strip_fences(open(os.path.join(ROOT, rel), encoding='utf-8').read()))
        base = os.path.dirname(rel)
        for m in re.finditer(r'\]\(([^)\s]+)\)', text):
            tgt = m.group(1)
            if tgt.startswith(('http://', 'https://', 'mailto:')):
                continue
            total += 1
            path, _, anc = tgt.partition('#')
            key = rel if path == '' else os.path.normpath(os.path.join(base, path))
            if path and not os.path.exists(os.path.join(ROOT, key)):
                err(f"{rel}: havola fayli yo'q -> {tgt}")
                continue
            if anc and key in anchors and anc not in anchors[key]:
                err(f"{rel}: anchor topilmadi -> {tgt}")

    # 3b. skill va agent havolalari.
    # Agentlar ham skilllar kabi docs/ ga va tools/ ga yo'naltiradi, lekin
    # avval tekshirilmasdi. Asbob nomi o'zgarsa yoki fayl ko'chirilsa,
    # ko'rsatma jim buziladi: chaqiruv ishlamaydi, hech kim xabar bermaydi.
    glob = __import__('glob')
    routed = (glob.glob(os.path.join(ROOT, '.claude/skills/*/SKILL.md'))
              + glob.glob(os.path.join(ROOT, '.claude/skills/*/references/*.md'))
              + glob.glob(os.path.join(ROOT, '.claude/agents/*.md')))
    # Faqat shu repoga tegishli yo'llar tekshiriladi. Ko'rsatmalarda
    # tahlil qilinadigan LOYIHA yo'llari ham uchraydi (`docs/adr/` kabi);
    # ular bu yerda bo'lmasligi xato emas. Manifest kalitlari chegara.
    try:
        manifest = json.load(open(os.path.join(ROOT, 'docs', 'manifest.json'),
                                  encoding='utf-8'))
    except (OSError, ValueError):
        manifest = {}
    own = set(manifest)

    def is_ours(path):
        parts = path.split('/')
        return len(parts) > 1 and parts[1] in own

    seen = set()
    for sk in sorted(routed):
        rel_sk = os.path.relpath(sk, ROOT)
        body = open(sk, encoding='utf-8').read()
        for m in re.finditer(r'`(docs/[^`\s<>]+?\.md)(#[-\w]+)?`', body):
            p_, a_ = m.group(1), (m.group(2) or '')[1:]
            if not is_ours(p_):
                continue
            if not os.path.exists(os.path.join(ROOT, p_)):
                err(f"{rel_sk}: havola fayli yo'q -> {p_}")
            # anchors kaliti relpath: Windows da `\` bilan, p_ esa `/` bilan.
            elif a_ and a_ not in anchors.get(os.path.normpath(p_), set()):
                err(f"{rel_sk}: havola anchori yo'q -> {p_}#{a_}")
        for m in re.finditer(r'`(docs/[^`\s<>]+/)`', body):
            if is_ours(m.group(1)) and not os.path.isdir(
                    os.path.join(ROOT, m.group(1))):
                err(f"{rel_sk}: havola papkasi yo'q -> {m.group(1)}")
        seen.update((d_, int(n_)) for d_, n_ in
                    re.findall(r"docs/([a-z-]+)/(\d\d)-", body))

    # Bob marshruti: har bob kamida bitta skill yoki agent jadvalida.
    # Yo'lsiz bob faqat doc.sh find tasodifan topsa o'qiladi, skill uni
    # hech qachon tavsiya qilmaydi. Raqamsiz bob (patterns indeksi) emas.
    for key, doc in manifest.items():
        for c in doc.get('chapters', []):
            num = c.get('num')
            if num and (key, num) not in seen and (key, num) not in UNROUTED_OK:
                err(f"docs/{key}: {num}-bob hech qaysi skill jadvalida yo'q")

    # tools/ ga ishora: faqat fayl nomi, argumentlarsiz. Backtick talab
    # qilinmaydi, shuning uchun kod bloki ichidagi chaqiruv ham
    # (`mvn test | python3 tools/parse_test_output.py`) tekshiriladi.
    # Har navbatda o'qiladigan CLAUDE.md va o'rnatish hujjati ham kiradi.
    tool_docs = sorted(routed) + [os.path.join(ROOT, f) for f in (
        'CLAUDE.md', 'README.md', 'CONTRIBUTING.md', 'install/README.md',
        'DECISIONS.md')
        if os.path.exists(os.path.join(ROOT, f))]
    doc_sh = os.path.join(ROOT, 'tools', 'doc.sh')
    subcommands = (set(re.findall(r'^\s+([a-z]+)\)', open(doc_sh, encoding='utf-8').read(), re.M))
                   if os.path.exists(doc_sh) else set())
    for path in tool_docs:
        rel_t = os.path.relpath(path, ROOT)
        body = open(path, encoding='utf-8').read()
        for m in re.finditer(r'(?<![\w/])(tools/[\w./-]+\.(?:py|sh))', body):
            if not os.path.exists(os.path.join(ROOT, m.group(1))):
                err(f"{rel_t}: asbob yo'q -> {m.group(1)}")
        # doc.sh subkomandasi: faqat kod ichida (inline yoki fence), nasrdagi
        # "doc.sh bilan" kabi gap tutilmasin. Ro'yxat doc.sh ning case
        # blokidan olinadi, qo'lda yozilgan ro'yxat eskirardi.
        code = re.findall(r'`[^`\n]*`', body) + [
            l for l, f in zip(body.split('\n'), strip_fences(body).split('\n'))
            if l != f]
        for span in code if subcommands else ():
            for m in re.finditer(r'doc\.sh ([a-z][\w-]*)', span):
                if m.group(1) not in subcommands:
                    err(f"{rel_t}: doc.sh da '{m.group(1)}' subkomandasi yo'q")

    # 4. manifest
    mpath = os.path.join(ROOT, 'docs', 'manifest.json')
    if not os.path.exists(mpath):
        err("docs/manifest.json yo'q")
    else:
        man = json.load(open(mpath, encoding='utf-8'))
        for key, doc in man.items():
            d = os.path.join(ROOT, 'docs', key)
            listed = {c['file'] for c in doc['chapters']}
            on_disk = {f for f in os.listdir(d) if f.endswith('.md') and f != 'README.md'}
            for f in sorted(listed - on_disk):
                err(f"docs/{key}: manifest da bor, diskda yo'q -> {f}")
            for f in sorted(on_disk - listed):
                err(f"docs/{key}: diskda bor, manifest da yo'q -> {f}")

            # 5. struktura
            readme_path = os.path.join(d, 'README.md')
            readme = (open(readme_path, encoding='utf-8').read()
                      if os.path.exists(readme_path) else '')
            crumb = re.compile(r'^\[[^\]]+\]\(\.\./\.\./README\.md\) / \[%s\]\(README\.md\)$'
                               % re.escape(doc.get('label', '')))
            chapters = doc['chapters']
            for i, c in enumerate(chapters):
                p = os.path.join(d, c['file'])
                if not os.path.exists(p):
                    continue
                where = f"docs/{key}/{c['file']}"
                t = open(p, encoding='utf-8').read()
                lines = t.split('\n')
                if not t.startswith('<!-- doc: '):
                    err(f"{where}: metadata izohi yo'q")
                elif lines[0].rstrip() != (f"<!-- doc: {key} | chapter: {c['num'] or ''}"
                                           f" | part: {c['part'] or ''} -->"):
                    err(f"{where}: metadata manifest bilan mos emas -> {lines[0][:60]}")
                if len(lines) < 5 or not crumb.match(lines[2]):
                    err(f"{where}: breadcrumb yo'q yoki noto'g'ri (3-qator)")
                if len(lines) < 5 or lines[4] != '# ' + c['title']:
                    err(f"{where}: H1 manifest sarlavhasi bilan mos emas (5-qator)")

                # Sarlavhalar fence tashqarisidan sanaladi: ```markdown
                # namunasidagi `## Hotfix` bob bo'limi emas.
                plain = strip_fences(t).split('\n')
                h1 = [l for l in plain if l.startswith('# ')]
                h2 = [l[3:] for l in plain if l.startswith('## ')]
                if len(h1) > 1:
                    err(f"{where}: {len(h1)} ta H1, bitta bo'lsin")
                if c.get('sections') is not None and len(h2) != c['sections']:
                    err(f"{where}: {len(h2)} bo'lim, manifestda {c['sections']}")
                summary = re.search(r"<summary>Bu bobdagi (\d+) bo'lim</summary>", t)
                if summary and int(summary.group(1)) != len(h2):
                    err(f"{where}: <summary> da {summary.group(1)} bo'lim, "
                        f"haqiqatda {len(h2)}")
                if c['num'] and readme:
                    # patterns README da yopish bo'limisiz "N pattern" yoziladi.
                    unit, want = (('pattern', len(h2) - 1) if key == 'patterns'
                                  else ("bo'lim", len(h2)))
                    m = re.search(r'\]\(%s\) - (\d+) %s' % (re.escape(c['file']), unit),
                                  readme)
                    if not m:
                        err(f"docs/{key}/README.md: {c['file']} uchun `- N {unit}` yo'q")
                    elif int(m.group(1)) != want:
                        err(f"docs/{key}/README.md: {c['file']} {m.group(1)} {unit}, "
                            f"haqiqatda {want}")
                if '[Mundarija](README.md)' not in t:
                    err(f"docs/{key}/{c['file']}: navigatsiya havolasi yo'q")
                # Footer oxirida turishi kerak, shunchaki mavjud bo'lishi
                # emas: add_code.py kabi yozuvchi asbob kod blokini uning
                # ORQASIGA qo'yib yuborishi mumkin va bob shakli buziladi.
                body = [l for l in lines if l.strip()]
                if body and '[Mundarija](README.md)' not in body[-1]:
                    err(f"{where}: navigatsiya footeridan keyin "
                        f"matn bor -> {body[-1][:50]}")
                elif body:
                    want = (([chapters[i - 1]['file']] if i else []) + ['README.md']
                            + ([chapters[i + 1]['file']] if i + 1 < len(chapters) else []))
                    if re.findall(r'\]\(([^)]+)\)', body[-1]) != want:
                        err(f"{where}: footer qo'shni boblarga ishora qilmaydi "
                            f"(kutilgan: {' · '.join(want)})")

                # 7. bob-yopish konvensiyasi: yopuvchi bo'lim bor VA oxirgi.
                closing = r"[\d.]+ (Amalda qo'llash|Arxitektor nazorat ro'yxati)\s*$"
                if c['num'] and not re.search(r"^## " + closing, t, re.M):
                    err(f"{where}: bob `Amalda qo'llash` yoki "
                        f"`Arxitektor nazorat ro'yxati` bilan tugamaydi")
                elif c['num'] and h2 and not re.match(closing, h2[-1]):
                    err(f"{where}: oxirgi bo'lim yopish bo'limi emas -> {h2[-1][:50]}")

    # 8. Regressiya: tuzatilgan xato naqshi qaytib kelmaganmi.
    check_regression(files)

    # 9. Qo'lda yozilgan bob va bo'lim sonlari.
    try:
        check_counts(json.load(open(os.path.join(ROOT, 'docs', 'manifest.json'),
                                    encoding='utf-8')))
    except (OSError, ValueError):
        pass          # manifest muammosini 4-tekshiruv aytadi

    print(f"{len(files)} markdown fayl, {total} nisbiy havola tekshirildi")
    for w in warnings:
        print(f"OGOHLANTIRISH: {w}")
    if errors:
        print(f"\n{len(errors)} XATO:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Hammasi joyida.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
