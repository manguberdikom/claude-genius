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


def flatten_links(text, files):
    """`NN-slug.md#anchor` -> `#anchor`; hujjatlararo havolalar o'z holida qoladi."""
    def repl(m):
        tgt = m.group(1)
        path, _, anc = tgt.partition('#')
        if path in files and anc:
            return f"](#{anc})"
        if path in files and not anc:
            return "](#mundarija)"
        return m.group(0)
    return re.sub(r'\]\(([^)\s]+)\)', repl, text)


def build(key):
    man = json.load(open(os.path.join(ROOT, 'docs', 'manifest.json'), encoding='utf-8'))[key]
    d = os.path.join(ROOT, 'docs', key)
    files = {c['file'] for c in man['chapters']}
    readme = open(os.path.join(d, 'README.md'), encoding='utf-8').read()
    title = re.match(r'# ([^\n]*)', readme).group(1)
    preamble = readme.split('\n## Mundarija', 1)[0].split('\n', 1)[1].strip()
    preamble = flatten_links(preamble, files)

    body, toc = [], []
    last_part = object()
    for c in man['chapters']:
        raw = open(os.path.join(d, c['file']), encoding='utf-8').read()
        text = deepen(flatten_links(unwrap_chapter(raw), files))
        if c['part'] != last_part:
            last_part = c['part']
            if c['part']:
                body += ['', f"# {c['part']}", '']
                toc += ['', f"**{c['part']}**", '']
        body += [f"## {c['title']}", '', text, '', '---', '']
        toc.append(f"- [{c['title']}](#{gh_slug(c['title'])})")
        for l in text.split('\n'):
            if re.match(r'^### ', l):
                h = l[4:]
                toc.append(f"  - [{h}](#{gh_slug(h)})")

    doc = [f"# {title}", '', preamble, '', '## Mundarija', ''] + toc + [''] + body
    os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
    path = os.path.join(ROOT, 'dist', OUT[key])
    open(path, 'w', encoding='utf-8').write('\n'.join(doc).rstrip('\n') + '\n')
    return path


if __name__ == '__main__':
    keys = sys.argv[1:] or list(OUT)
    for k in keys:
        p = build(k)
        print(f"{os.path.relpath(p, ROOT)}  {os.path.getsize(p) / 1024:.0f} KB")
