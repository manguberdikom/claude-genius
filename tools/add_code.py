#!/usr/bin/env python3
"""Pattern bo'limlarining oxiriga `java` kod bloki qo'shadi.

Kirish - JSON fayl: {"<hujjat>": {"<bo'lim raqami>": "<kod>", ...}, ...}
Kod satr bo'lsa til `java` deb olinadi; boshqa til kerak bo'lsa
{"lang": "yaml", "code": "..."} ko'rinishida beriladi.

    python3 tools/add_code.py snippets.json

Kod bo'limning eng oxiriga, keyingi `## ` sarlavhasidan oldin qo'yiladi.
Bo'limda allaqachon kod bo'lsa, o'tkazib yuboriladi. Kodi bor va umuman
topilmagan raqam alohida ogohlantirish oladi: raqamdagi xato "allaqachon
tayyor" holati bilan adashmasin. Hujjat kaliti manifestda bo'lmasa hech
narsa yozilmaydi va asbob 2 bilan chiqadi.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_manifest():
    return json.load(open(os.path.join(ROOT, 'docs/manifest.json'), encoding='utf-8'))


def chapter_paths(key, manifest=None):
    man = (manifest or load_manifest())[key]
    return [os.path.join(ROOT, 'docs', key, c['file']) for c in man['chapters'] if c['num']]


NAV = '[Mundarija](README.md)'


def content_end(lines, first_section):
    """Navigatsiya footeri boshlanadigan qator raqami.

    Oxirgi bo'limning tanasi fayl oxirigacha emas, footergacha davom
    etadi: aks holda kod bloki navigatsiya havolasidan KEYIN tushadi va
    bob shakli buziladi (CONTRIBUTING.md, "Bob fayli shakli"). check_docs
    buni fayl yozilgandan keyin ushlaydi, asbobning o'zi esa faylni
    buzmasligi kerak.
    """
    for i in range(len(lines) - 1, first_section, -1):
        if NAV in lines[i]:
            end = i
            while end > first_section and lines[end - 1].strip() in ('', '---'):
                end -= 1
            return end
    return len(lines)


def insert(path, wanted, skipped=None):
    """wanted: {'1.2': kod}. Qo'shilgan raqamlar to'plamini qaytaradi.

    skipped berilsa, topilgan, lekin kodi allaqachon bor bo'limlar
    raqami unga qo'shiladi.
    """
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    # bo'lim chegaralarini topish (fence tashqarisidagi `## ` lar)
    marks, fence = [], False
    for i, l in enumerate(lines):
        if l.startswith('```'):
            fence = not fence
            continue
        if not fence and re.match(r'^## ', l):
            marks.append(i)
    added = set()
    for n, start in reversed(list(enumerate(marks))):
        head = lines[start][3:]
        m = re.match(r'^(\d+\.\d+) ', head)
        if not m or m.group(1) not in wanted:
            continue
        num = m.group(1)
        end = marks[n + 1] if n + 1 < len(marks) else content_end(lines, start)
        body = lines[start + 1:end]
        if any(l.startswith('```') for l in body):
            if skipped is not None:
                skipped.add(num)
            continue
        # tanadan oxirgi bo'sh qatorlarni hisobga olib joy topish
        j = end
        while j > start + 1 and lines[j - 1].strip() == '':
            j -= 1
        spec = wanted[num]
        lang = 'java'
        if isinstance(spec, dict):
            lang, spec = spec.get('lang', 'java'), spec['code']
        code = spec.strip('\n')
        lines[j:j] = ['', f'```{lang}', *code.split('\n'), '```']
        added.add(num)
    if added:
        open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    return added


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    data = json.load(open(argv[0], encoding='utf-8'))
    manifest = load_manifest()
    # Kalit yozishdan OLDIN tekshiriladi: aks holda birinchi hujjat yozilib
    # bo'lgach yiqilib, qisman yozuv qolardi.
    bad = sorted(k for k in data if k not in manifest)
    if bad:
        print(f"XATO hujjat topilmadi: {bad}; mavjud: {sorted(manifest)}", file=sys.stderr)
        return 2
    total = 0
    for key, wanted in data.items():
        left, skipped = dict(wanted), set()
        for path in chapter_paths(key, manifest):
            if not left:
                break
            got = insert(path, left, skipped)
            for g in got | skipped:
                left.pop(g, None)
            total += len(got)
        if skipped:
            print(f"OGOHLANTIRISH {key}: kod allaqachon bor -> {sorted(skipped)}", file=sys.stderr)
        if left:
            print(f"OGOHLANTIRISH {key}: bunday bo'lim yo'q -> {sorted(left)}", file=sys.stderr)
    print(f"{total} kod bloki qo'shildi")
    return 0


if __name__ == '__main__':
    sys.exit(main())
