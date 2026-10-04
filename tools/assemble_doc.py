#!/usr/bin/env python3
"""mindset/NN.md bob fayllarini bitta hujjatga yig'adi va tekshiradi."""
import json, os, re, sys, unicodedata

S = os.path.dirname(os.path.abspath(__file__))
PLAN = json.load(open(sys.argv[1], encoding='utf-8'))
SRC = sys.argv[2]
OUT = sys.argv[3]

TITLE = PLAN["title"]
INTRO = PLAN["intro"]

CYR = re.compile(r'[Ѐ-ӿ]')

def slug(text):
    t = text.strip().lower()
    t = t.replace('’', '').replace('ʻ', '').replace('ʼ', '').replace("'", '')
    out = []
    for ch in t:
        if ch.isalnum() or ch == '-' or ch == '_':
            out.append(ch)
        elif ch.isspace():
            out.append('-')
    return ''.join(out)

class Slugger:
    def __init__(self):
        self.seen = {}
    def __call__(self, text):
        s = slug(text)
        n = self.seen.get(s, 0)
        self.seen[s] = n + 1
        return s if n == 0 else '%s-%d' % (s, n)

def split_fences(lines):
    """Har bir qator uchun (qator, kod_bloki_ichidami) juftligini qaytaradi."""
    infence = False
    out = []
    for ln in lines:
        if ln.lstrip().startswith('```'):
            out.append((ln, True))
            infence = not infence
            continue
        out.append((ln, infence))
    return out

def process_chapter(n, meta, slugger, problems):
    path = os.path.join(SRC, '%02d.md' % n)
    if not os.path.exists(path):
        problems.append('%02d.md mavjud emas' % n)
        return None, []
    raw = open(path, encoding='utf-8').read().strip('\n')
    if len(raw) < 500:
        problems.append('%02d.md juda kichik (%d bayt)' % (n, len(raw)))
    pairs = split_fences(raw.split('\n'))

    body = []
    sections = []
    k = 0
    for ln, infence in pairs:
        if infence:
            body.append(ln)
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if not m:
            body.append(ln)
            continue
        level, text = len(m.group(1)), m.group(2).strip()
        if level <= 2:
            problems.append('%02d.md: ruxsatsiz H%d sarlavha: %s' % (n, level, text[:60]))
            continue
        text = re.sub(r'^\d+(\.\d+)*\.?\s+', '', text)
        k += 1
        label = '%d.%d %s' % (n, k, text)
        sections.append((label, slugger(label), text))
        body.append('### ' + label)

    if not sections:
        problems.append('%02d.md: ### bo\'lim topilmadi' % n)
    elif not sections[-1][2].strip().lower().startswith('amalda qo'):
        problems.append('%02d.md: oxirgi bo\'lim "Amalda qo\'llash" emas: %s' % (n, sections[-1][2][:50]))

    text_all = '\n'.join(body)
    if text_all.count('```') % 2 != 0:
        problems.append('%02d.md: kod fence soni toq (%d)' % (n, text_all.count('```')))
    code_blocks = text_all.count('```') // 2
    if code_blocks < 4:
        problems.append('%02d.md: kod bloki kam (%d)' % (n, code_blocks))
    tables = len(re.findall(r'^\|.*\|\s*$', text_all, re.M))
    if tables < 6:
        problems.append('%02d.md: jadval qatori kam (%d)' % (n, tables))
    if CYR.search(text_all):
        found = set(CYR.findall(text_all))
        problems.append('%02d.md: kirill harf bor: %s' % (n, ''.join(sorted(found))[:30]))
    checks = len(re.findall(r'^\s*- \[ \]', text_all, re.M))
    if checks < 4:
        problems.append('%02d.md: "- [ ]" bandi kam (%d)' % (n, checks))

    words = len(text_all.split())
    return {'n': n, 'meta': meta, 'body': text_all, 'sections': sections,
            'words': words, 'code': code_blocks, 'tables': tables}, sections

def main():
    problems = []
    slugger = Slugger()
    slugger(TITLE)
    slugger('Mundarija')
    parts = PLAN['parts']
    order = PLAN['order']
    chapters = {c['n']: c for c in PLAN['chapters']}

    part_anchor = {}
    done = []
    seen_parts = []
    for c in PLAN['chapters']:
        n = c['n']
        if c['part'] not in seen_parts:
            seen_parts.append(c['part'])
            part_anchor[c['part']] = slugger(parts[c['part']])
        head = '%d. %s (%s)' % (n, c['title'], c['en'])
        c['anchor'] = slugger(head)
        c['head'] = head
        ch, _ = process_chapter(n, c, slugger, problems)
        if ch:
            done.append(ch)

    # Mundarija
    toc = ['## Mundarija', '']
    cur = None
    for ch in done:
        c = ch['meta']
        if c['part'] != cur:
            cur = c['part']
            toc.append('')
            toc.append('**[%s](#%s)**' % (parts[cur], part_anchor[cur]))
            toc.append('')
        toc.append('- [%s](#%s)' % (ch['meta']['head'], c['anchor']))
        for label, anc, _t in ch['sections']:
            toc.append('  - [%s](#%s)' % (label, anc))

    doc = ['# ' + TITLE, '', INTRO, '', '\n'.join(toc), '']
    cur = None
    for ch in done:
        c = ch['meta']
        if c['part'] != cur:
            cur = c['part']
            doc.append('')
            doc.append('# ' + parts[cur])
            doc.append('')
        doc.append('## ' + c['head'])
        doc.append('')
        doc.append(ch['body'].strip('\n'))
        doc.append('')

    text = '\n'.join(doc).rstrip('\n') + '\n'
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # havolalarni tekshirish
    anchors = set()
    infence = False
    for ln in text.split('\n'):
        if ln.lstrip().startswith('```'):
            infence = not infence
            continue
        if infence:
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', ln)
        if m:
            anchors.add(slug(m.group(2).strip()))
    # takroriy sarlavhalar uchun -N variantlari
    extra = set()
    for a in list(anchors):
        for i in range(1, 6):
            extra.add('%s-%d' % (a, i))
    anchors |= extra
    broken = [l for l in re.findall(r'\]\(#([^)]+)\)', text) if l not in anchors]
    if broken:
        problems.append('ishlamaydigan havola: %d ta, masalan %s' % (len(broken), broken[:3]))
    if text.count('```') % 2 != 0:
        problems.append('yakuniy hujjatda kod fence soni toq')
    if CYR.search(text):
        problems.append('yakuniy hujjatda kirill harf bor')

    open(OUT, 'w', encoding='utf-8').write(text)

    print('Yakuniy fayl: %s' % OUT)
    print('Boblar: %d / %d' % (len(done), len(PLAN['chapters'])))
    print('Bo\'limlar: %d' % sum(len(c['sections']) for c in done))
    print('So\'z: %d, kod bloki: %d, jadval qatori: %d' % (
        sum(c['words'] for c in done), sum(c['code'] for c in done), sum(c['tables'] for c in done)))
    print('Hajm: %.2f MB' % (len(text.encode('utf-8')) / 1048576.0))
    print('Havola: %d, ishlamaydigan: %d' % (len(re.findall(r'\]\(#', text)), len(broken)))
    if problems:
        print('\nMUAMMOLAR (%d):' % len(problems))
        for p in problems:
            print('  - ' + p)
        return 1
    print('\nTekshiruv toza.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
