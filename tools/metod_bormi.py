#!/usr/bin/env python3
"""Yangi metod yozishdan oldin: shu ish allaqachon bormi, muhim maydonni kim o'zgartiradi.

    python3 tools/metod_bormi.py <papka> refund charge      # o'xshash metodlar
    python3 tools/metod_bormi.py <papka> --ozgartiradi amount   # maydonni o'zgartiradigan metodlar

Birinchi rejim: metod nomi (camelCase bo'laklari) so'zlardan biri bilan
boshlansa yoki uni o'z ichiga olsa chiqadi; bor metod qayta yozilmaydi,
chaqiriladi (clean-code 32.2). Ikkinchi rejim: maydonga yozadigan har
metod; bittadan ko'p bo'lsa qiymat "bir teshik"dan o'zgarmaydi
(code-review 9.7, 13.1). Qidiruv matn bo'yicha: tur ma'lumoti yo'q, shuning
uchun natija ro'yxat, hukm emas.
"""

import os
import re
import sys

MAX_SHOWN = 40
METHOD_RE = re.compile(
    r"^[ \t]*(?:@\w+(?:\([^)]*\))?\s+)*(?:(?:public|protected|private|static|final|"
    r"synchronized|default|abstract)\s+)*(?:<[^>]+>\s+)?([\w<>\[\],.? ]+?)\s+"
    r"([a-z]\w*)\s*\(([^)]*)\)", re.M)
CTOR_RE = re.compile(r"^[ \t]*(?:public|protected|private)\s+([A-Z]\w*)\s*\(", re.M)
KEYWORDS = {"if", "for", "while", "switch", "catch", "return", "new", "throw", "else"}
WORD_RE = re.compile(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])")


def java_files(root):
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "build", "target", "node_modules")]
        for name in files:
            if name.endswith((".java", ".kt")):
                yield os.path.join(folder, name)


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return ""


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def methods(text):
    """[(pos, nom, imzo)]: e'lon qilingan metodlar."""
    out = []
    for m in METHOD_RE.finditer(text):
        kind, name = m.group(1).strip(), m.group(2)
        if name in KEYWORDS or kind in KEYWORDS or kind.startswith(("return", "new ")):
            continue
        out.append((m.start(2), name, "%s %s(%s)" % (kind, name, " ".join(m.group(3).split()))))
    return out


def similar(root, words):
    words = [w.lower() for w in words]
    found = []
    for path in java_files(root):
        text = read(path)
        for pos, name, sig in methods(text):
            parts = [p.lower() for p in WORD_RE.findall(name)]
            low = name.lower()
            if any(w in low or any(p.startswith(w) for p in parts) for w in words):
                found.append("%s:%d  %s" % (os.path.relpath(path, root), line_of(text, pos), sig))
    return found


def writers(root, field):
    """{(fayl, metod)}: maydonga yozadigan metodlar (`this.f =`, `f =`, `setF(`)."""
    write = re.compile(r"(?:\bthis\.%s|(?<![.\w])%s)\s*(?:[-+*/]?=)(?!=)" % (field, field))
    setter = re.compile(r"\bset%s\s*\(" % re.escape(field[:1].upper() + field[1:]))
    out = []
    for path in java_files(root):
        text = read(path)
        spans = sorted([(pos, name) for pos, name, _ in methods(text)]
                       + [(c.start(1), c.group(1)) for c in CTOR_RE.finditer(text)])
        for m in list(write.finditer(text)) + list(setter.finditer(text)):
            owner = [name for pos, name in spans if pos < m.start()]
            if not owner:
                continue   # maydon e'loni yoki initsializator
            out.append((os.path.relpath(path, root), owner[-1], line_of(text, m.start())))
    return out


def main(argv):
    if len(argv) < 2 or (argv[1] == "--ozgartiradi" and len(argv) != 3):
        print(__doc__.strip().split("\n\n")[1])
        return 2
    root = argv[0]
    if argv[1] == "--ozgartiradi":
        rows = writers(root, argv[2])
        owners = sorted({(path, name) for path, name, _ in rows})
        for path, name, line in rows[:MAX_SHOWN]:
            print("%s:%d  %s()" % (path, line, name))
        if len(owners) > 1:
            print("\n%d metod `%s` ni o'zgartiradi: muhim qiymat bitta domen metodi "
                  "orqali o'zgarsin (code-review 9.7)" % (len(owners), argv[2]))
        elif not rows:
            print("`%s` ga yozadigan metod topilmadi" % argv[2])
        return 0
    rows = similar(root, argv[1:])
    for row in rows[:MAX_SHOWN]:
        print(row)
    if len(rows) > MAX_SHOWN:
        print("... yana %d ta: so'zni aniqlang" % (len(rows) - MAX_SHOWN))
    if not rows:
        print("o'xshash metod topilmadi: %s" % ", ".join(argv[1:]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
