#!/usr/bin/env python3
"""Kod misoli yo'q patternlarni ro'yxatlaydi.

    python3 tools/code_gap.py                 # hujjat bo'yicha yig'indi
    python3 tools/code_gap.py patterns 3      # 3-bo'limdagi bo'sh patternlar
    python3 tools/code_gap.py patterns 3 -v   # Spring qatori bilan
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sections(path):
    """[(sarlavha, tanasi)] - kod fence holatini hisobga olib."""
    lines = open(path, encoding='utf-8').read().split('\n')
    out, cur, fence = [], None, False
    for l in lines:
        if l.startswith('```'):
            fence = not fence
            if cur:
                cur[1].append(l)
            continue
        m = None if fence else re.match(r'^## (.+)$', l)
        if m:
            cur = (m.group(1), [])
            out.append(cur)
        elif cur:
            cur[1].append(l)
    return [(h, '\n'.join(b)) for h, b in out]


def gaps(key, num=None):
    man = json.load(open(os.path.join(ROOT, 'docs/manifest.json'), encoding='utf-8'))[key]
    res = []
    for ch in man['chapters']:
        if not ch['num'] or (num and ch['num'] != num):
            continue
        path = os.path.join(ROOT, 'docs', key, ch['file'])
        for h, body in sections(path):
            if "Amalda qo'llash" in h or 'Arxitektor nazorat' in h:
                continue
            if '```' in body:
                continue
            spring = ''
            m = re.search(r"\*\*Spring'da qayerda uchraydi:\*\*\s*(.+)", body)
            if m:
                spring = m.group(1)
            res.append((ch['num'], ch['file'], h, spring))
    return res


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '-v']
    verbose = '-v' in sys.argv
    if not args:
        man = json.load(open(os.path.join(ROOT, 'docs/manifest.json'), encoding='utf-8'))
        for key in man:
            g = gaps(key)
            tot = sum(1 for ch in man[key]['chapters'] for _ in [0] if ch['num'])
            allsec = sum(ch['sections'] for ch in man[key]['chapters'])
            print(f"{key:12} kodsiz bo'lim: {len(g):4} / {allsec}")
        sys.exit()
    key = args[0]
    num = int(args[1]) if len(args) > 1 else None
    g = gaps(key, num)
    for n, f, h, spring in g:
        print(f"{h}")
        if verbose and spring:
            print(f"    SPRING: {spring[:240]}")
    print(f"\n--- {len(g)} ta kodsiz bo'lim", file=sys.stderr)
