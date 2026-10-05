#!/usr/bin/env python3
"""Bo'lingan boblardan bitta fayllik versiyani qayta yig'adi.

docs/ - yagona haqiqat manbasi. Bu skript undan offline o'qish, PDF va
LLM ga uzatish uchun monolit fayl yasaydi.

    python3 tools/build_single.py            # hammasi -> dist/
    python3 tools/build_single.py patterns   # faqat bittasi
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = {
    'patterns':  'java-spring-design-patterns.md',
    'testing':   'java-spring-testing-handbook.md',
    'architect': 'java-spring-architect-mindset.md',
    'sonarqube': 'java-spring-sonarqube.md',
    'clean-code': 'java-spring-clean-coder.md',
    'code-review': 'java-spring-code-review.md',
}
RE_REMOVE = re.compile(r"[^\w\- ]", re.UNICODE)


def gh_slug(text):
    t = text.replace('`', '')
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'\*\*([^*]*)\*\*', r'\1', t)
    t = t.strip().lower().replace("'", "").replace("’", "")
    return RE_REMOVE.sub('', t).replace(' ', '-')


def unwrap_chapter(text):
    """Bob faylidan sarlavha, breadcrumb, <details> va nav footer ni olib tashlaydi."""
    t = re.sub(r'\A<!-- doc:[^\n]*-->\n\n', '', text)
    t = re.sub(r'\A\[[^\n]*\]\(README\.md\)\n\n', '', t)
    t = re.sub(r'\A# [^\n]*\n\n', '', t)
    t = re.sub(r'\A<details>\n<summary>[^\n]*</summary>\n\n(?:- \[[^\n]*\n)+\n</details>\n\n', '', t)
    t = re.sub(r'\n\n---\n\n\[[^\n]*\n\Z', '\n', t)
    return t.rstrip('\n')


def deepen(text):
    """## -> ###: bob fayllari H1/H2, monolitda H2/H3."""
    out, fence = [], False
    for l in text.split('\n'):
        if l.startswith('```'):
            fence = not fence
            out.append(l)
            continue
        out.append('#' + l if not fence and re.match(r'^#{2,5} ', l) else l)
    return '\n'.join(out)


CROSS_RE = re.compile(r'^\.\./([\w-]+)/([^/#]+\.md)$')


def flatten_links(text, files, key=None, others=None):
    """`NN-slug.md#anchor` -> `#anchor`, `NN-slug.md` -> bob sarlavhasi anchori.

    `files` - bob fayli nomi -> o'sha bobning sarlavha anchori. Hujjatlararo
    havolalar dist/ dagi qo'shni monolitga yo'naltiriladi: `../<hujjat>/
    README.md` -> `<monolit>`, `../<hujjat>/<bob>.md` -> `<monolit>#<bob>`
    (`others` - hujjat -> {bob fayli: anchor}). Qolgan nisbiy yo'l
    docs/<key>/ dan dist/ ga ko'chiriladi. Kod bloki ichiga tegilmaydi:
    u yerdagi havola namuna. `build_single.py patterns` bitta faylni
    yig'sa, qo'shni monolit dist/ da bo'lmaguncha havola ochilmaydi.
    """
    def repl(m):
        path, _, anc = m.group(1).partition('#')
        if path in files:
            return f"](#{anc or files[path]})"
        if not path or re.match(r'^[a-z]+:', path) or path.startswith('/'):
            return m.group(0)
        cross = CROSS_RE.match(path)
        if cross and cross.group(1) in OUT:
            other, name = cross.groups()
            if name != 'README.md' and not anc:
                anc = (others or {}).get(other, {}).get(name, '')
            return f"]({OUT[other]}{'#' + anc if anc else ''})"
        if key is None:
            return m.group(0)
        moved = os.path.relpath(os.path.normpath(os.path.join('docs', key, path)), 'dist')
        return f"]({moved.replace(os.sep, '/')}{'#' + anc if anc else ''})"

    out, fence = [], False
    for l in text.split('\n'):
        if l.startswith('```'):
            fence = not fence
        out.append(l if fence or l.startswith('```')
                   else re.sub(r'\]\(([^)\s]+)\)', repl, l))
    return '\n'.join(out)


def build(key, out_dir=None):
    manifest = json.load(open(os.path.join(ROOT, 'docs', 'manifest.json'), encoding='utf-8'))
    man = manifest[key]
    others = {k: {c['file']: gh_slug(c['title']) for c in v['chapters']}
              for k, v in manifest.items() if k in OUT}
    d = os.path.join(ROOT, 'docs', key)
    files = others[key]
    readme = open(os.path.join(d, 'README.md'), encoding='utf-8').read()
    title = re.match(r'# ([^\n]*)', readme).group(1)
    preamble = readme.split('\n## Mundarija', 1)[0].split('\n', 1)[1].strip()
    preamble = flatten_links(preamble, files, key, others)

    body, toc = [], []
    last_part = object()
    for c in man['chapters']:
        raw = open(os.path.join(d, c['file']), encoding='utf-8').read()
        text = deepen(flatten_links(unwrap_chapter(raw), files, key, others))
        if c['part'] != last_part:
            last_part = c['part']
            if c['part']:
                body += ['', f"# {c['part']}", '']
                toc += ['', f"**{c['part']}**", '']
        body += [f"## {c['title']}", '', text, '', '---', '']
        toc.append(f"- [{c['title']}](#{gh_slug(c['title'])})")
        fence = False
        for l in text.split('\n'):
            if l.startswith('```'):
                fence = not fence   # deepen() kabi: ```markdown ichidagi ### sarlavha emas
            elif not fence and re.match(r'^### ', l):
                h = l[4:]
                toc.append(f"  - [{h}](#{gh_slug(h)})")

    doc = [f"# {title}", '', preamble, '', '## Mundarija', ''] + toc + [''] + body
    out_dir = out_dir or os.path.join(ROOT, 'dist')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUT[key])
    open(path, 'w', encoding='utf-8').write('\n'.join(doc).rstrip('\n') + '\n')
    return path


if __name__ == '__main__':
    keys = sys.argv[1:] or list(OUT)
    for k in keys:
        p = build(k)
        print(f"{os.path.relpath(p, ROOT)}  {os.path.getsize(p) / 1024:.0f} KB")
