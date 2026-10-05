#!/usr/bin/env python3
"""build_single.py uchun sinovlar.

    python3 tools/test_build_single.py

CI monolit bo'sh emasligini ko'radi, havolalarini emas. Shu sabab
monolitda 250 ta hujjatlararo havola (`../<hujjat>/README.md`, dist/ dan
qaraganda yo'q fayl) va ```markdown namunasidan mundarijaga tushgan 7 ta
anchor jim buzuq turgan. Bu yerda hammasi vaqtinchalik papkaga yig'iladi
va har nisbiy havola mavjud faylga hamda mavjud anchorga olib borishi
tekshiriladi (kod bloki va inline kod hisobga olinmaydi).
"""

import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import build_single  # noqa: E402
from check_docs import heading_anchors, strip_fences, strip_inline_code  # noqa: E402

LINK_RE = re.compile(r'\]\(([^)\s]+)\)')


def broken_links(out_dir):
    """(fayl, havola) ro'yxati: fayl yoki anchor topilmagan havolalar."""
    texts = {name: open(os.path.join(out_dir, name), encoding="utf-8").read()
             for name in build_single.OUT.values()}
    anchors = {name: heading_anchors(text) for name, text in texts.items()}
    bad = []
    for name, text in texts.items():
        for m in LINK_RE.finditer(strip_inline_code(strip_fences(text))):
            target = m.group(1)
            if re.match(r'^[a-z]+:', target):
                continue
            path, _, anc = target.partition('#')
            if not path:
                ok = anc in anchors[name]
            elif path in texts:
                ok = not anc or anc in anchors[path]
            else:
                # Monolit tashqarisi: kanonik joy dist/ dan hal qilinadi.
                full = os.path.normpath(os.path.join(ROOT, "dist", path))
                ok = os.path.exists(full)
            if not ok:
                bad.append((name, target))
    return bad


def case_havolalar_butun(tmp):
    for key in build_single.OUT:
        build_single.build(key, tmp)
    bad = broken_links(tmp)
    for name, target in bad[:10]:
        print("     %s -> %s" % (name, target))
    return not bad


def case_hujjatlararo_monolitga(_):
    files = {"01-a.md": "1-a"}
    others = {"testing": {"02-b.md": "2-b"}}
    text = ("[x](../patterns/README.md) [y](../testing/02-b.md) "
            "[z](../testing/02-b.md#25-q) [w](01-a.md) [g](../../GLOSSARY.md)")
    out = build_single.flatten_links(text, files, "patterns", others)
    return out == ("[x](java-spring-design-patterns.md) "
                   "[y](java-spring-testing-handbook.md#2-b) "
                   "[z](java-spring-testing-handbook.md#25-q) [w](#1-a) "
                   "[g](../GLOSSARY.md)")


def case_kod_blokiga_tegilmaydi(_):
    text = "```markdown\n[a](../patterns/README.md)\n```\n[b](../patterns/README.md)"
    out = build_single.flatten_links(text, {}, "testing", {})
    return out.split("\n")[1] == "[a](../patterns/README.md)" and \
        out.split("\n")[3] == "[b](java-spring-design-patterns.md)"


CASES = [
    ("hujjatlararo havola qo'shni monolitga", case_hujjatlararo_monolitga),
    ("kod bloki ichidagi havola namuna bo'lib qoladi", case_kod_blokiga_tegilmaydi),
    ("monolitdagi har havola va anchor butun", case_havolalar_butun),
]


def main():
    tmp = tempfile.mkdtemp(prefix="build_single_")
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn(tmp))
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
