#!/usr/bin/env python3
"""Hujjatlar sog'ligini tekshiradi. CI da ham, lokal ham bir xil ishlaydi.

    python3 tools/check_docs.py

Tekshiradi:
  1. Fayl hajmi   - GitHub 1 MB dan katta markdown ni render qilmaydi.
  2. Havolalar    - har bir nisbiy havola va anchor haqiqatan mavjudmi.
  3. Kirill       - hujjat o'zbek lotin yozuvida, kirill harf bo'lmasin.
  3b. Em-dash     - loyiha qoidasi: em-dash va en-dash ishlatilmaydi.
  3c. Kod fence   - ``` soni juft bo'lishi kerak, aks holda render buziladi.
  4. Manifest     - docs/manifest.json diskdagi fayllar bilan mos.
  5. Skilllar     - .claude/skills/ ichidagi docs/ havolalari haqiqiy.
  6. Struktura    - har bob faylida metadata va navigatsiya bor.
"""
import json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZE_LIMIT = 900_000          # GitHub chegarasi 1 048 576; zahira bilan
RE_REMOVE = re.compile(r"[^\w\- ]", re.UNICODE)
SKIP_DIRS = {'.git', 'dist', 'node_modules'}

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

        # 3c. kod fence juftligi
        fences = sum(1 for l in text.split('\n') if l.startswith('```'))
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

    # 3b. skill havolalari
    for sk in sorted(__import__('glob').glob(os.path.join(ROOT, '.claude/skills/*/SKILL.md'))):
        rel_sk = os.path.relpath(sk, ROOT)
        body = open(sk, encoding='utf-8').read()
        for m in re.finditer(r'`(docs/[^`\s<>]+?\.md)(#[-\w]+)?`', body):
            p_, a_ = m.group(1), (m.group(2) or '')[1:]
            if not os.path.exists(os.path.join(ROOT, p_)):
                err(f"{rel_sk}: skill havolasi fayli yo'q -> {p_}")
            elif a_ and a_ not in anchors.get(p_, set()):
                err(f"{rel_sk}: skill havolasi anchori yo'q -> {p_}#{a_}")
        for m in re.finditer(r'`(docs/[^`\s<>]+/)`', body):
            if not os.path.isdir(os.path.join(ROOT, m.group(1))):
                err(f"{rel_sk}: skill havolasi papkasi yo'q -> {m.group(1)}")

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
            for c in doc['chapters']:
                p = os.path.join(d, c['file'])
                if not os.path.exists(p):
                    continue
                t = open(p, encoding='utf-8').read()
                if not t.startswith('<!-- doc: '):
                    err(f"docs/{key}/{c['file']}: metadata izohi yo'q")
                if '[Mundarija](README.md)' not in t:
                    err(f"docs/{key}/{c['file']}: navigatsiya havolasi yo'q")

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
