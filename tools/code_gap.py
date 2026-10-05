#!/usr/bin/env python3
"""Kod misoli yo'q patternlarni ro'yxatlaydi.

    python3 tools/code_gap.py                 # hujjat bo'yicha yig'indi
    python3 tools/code_gap.py patterns 3      # 3-bo'limdagi bo'sh patternlar
    python3 tools/code_gap.py patterns 3 -v   # Spring qatori bilan
    python3 tools/code_gap.py patterns 17.2   # faqat shu yozuv, kodsiz bo'lsa

Maxraj yopish bo'limlarisiz sanaladi (`Amalda qo'llash`, `Arxitektor
nazorat ro'yxati`): ular pattern emas va surat ham ularni tashlaydi.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLOSING = ("Amalda qo'llash", 'Arxitektor nazorat')


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
    """(kodsiz bo'limlar, jami bo'lim). Surat va maxraj bitta filtrdan.

    Maxraj manifestdagi `sections` dan emas, fayldan sanaladi: unda
    yopish bo'limi ham bor va u eskirishi mumkin.
    """
    man = json.load(open(os.path.join(ROOT, 'docs/manifest.json'), encoding='utf-8'))[key]
    res, total = [], 0
    for ch in man['chapters']:
        if not ch['num'] or (num and ch['num'] != num):
            continue
        path = os.path.join(ROOT, 'docs', key, ch['file'])
        for h, body in sections(path):
            if any(c in h for c in CLOSING):
                continue
            total += 1
            if '```' in body:
                continue
            spring = ''
            m = re.search(r"\*\*Spring'da qayerda uchraydi:\*\*\s*(.+)", body)
            if m:
                spring = m.group(1)
            res.append((ch['num'], ch['file'], h, spring))
    return res, total


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '-v']
    verbose = '-v' in sys.argv
    if not args:
        man = json.load(open(os.path.join(ROOT, 'docs/manifest.json'), encoding='utf-8'))
        for key in man:
            g, total = gaps(key)
            print(f"{key:12} kodsiz bo'lim: {len(g):4} / {total}")
        sys.exit()
    key = args[0]
    arg = args[1] if len(args) > 1 else None
    if arg and not re.fullmatch(r'\d+(\.\d+)?', arg):
        sys.exit(f"bob yoki bo'lim raqami kerak, masalan: code_gap.py {key} 17 "
                 f"yoki {key} 17.2 (berildi: {arg})")
    num = int(arg.split('.')[0]) if arg else None
    g, _ = gaps(key, num)
    if arg and '.' in arg:
        # Bo'lim so'ralsa butun bobga kengaytirilmaydi, faqat o'sha yozuv.
        g = [row for row in g if row[2].startswith(arg + ' ')]
    for n, f, h, spring in g:
        print(f"{h}")
        if verbose and spring:
            print(f"    SPRING: {spring[:240]}")
    print(f"\n--- {len(g)} ta kodsiz bo'lim", file=sys.stderr)
