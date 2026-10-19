#!/usr/bin/env python3
"""Yangi metod yozishdan oldin: shu ish allaqachon bormi, muhim maydonni kim o'zgartiradi.

    python3 tools/metod_bormi.py <papka> refund charge      # o'xshash metodlar
    python3 tools/metod_bormi.py <papka> --ozgartiradi amount   # maydonni o'zgartiradigan metodlar
    python3 tools/metod_bormi.py <papka> --audit   # eski kod rentgeni: refaktoring ro'yxati va sonlar

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


def is_test(path):
    return "/test/" in path.replace("\\", "/") or path.endswith(("Test.java", "Tests.java"))


def writers(root, field):
    """{(fayl, metod)}: maydonga yozadigan metodlar (`this.f =`, `f =`, `setF(`), testsiz."""
    write = re.compile(r"(?:\bthis\.%s|(?<![.\w])%s)\s*(?:[-+*/]?=)(?!=)" % (field, field))
    # Setter chaqiruvi (`a.setX(`), e'loni (`void setX(`) emas.
    setter = re.compile(r"(?<![\w\s])\s*\bset%s\s*\(|\.set%s\s*\("
                        % ((re.escape(field[:1].upper() + field[1:]),) * 2))
    out = []
    for path in java_files(root):
        if is_test(path):
            continue
        text = read(path)
        spans = sorted([(pos, name) for pos, name, _ in methods(text)]
                       + [(c.start(1), c.group(1)) for c in CTOR_RE.finditer(text)])
        for m in list(write.finditer(text)) + list(setter.finditer(text)):
            owner = [name for pos, name in spans if pos < m.start()]
            if not owner:
                continue   # maydon e'loni yoki initsializator
            out.append((os.path.relpath(path, root), owner[-1], line_of(text, m.start())))
    return out


FIELD_RE = re.compile(r"^[ \t]*(?:private|protected|public)\s+(?:static\s+)?"
                      r"(?!final\b)[\w<>\[\],.? ]+\s+(\w+)\s*(?:=[^;]*)?;", re.M)
LONG_METHOD = 30


def bodies(text):
    """[(nom, qator, tana)]: qavs balansi bilan metod tanalari."""
    out = []
    for pos, name, _ in methods(text):
        start = text.find("{", pos)
        semi = text.find(";", pos)
        if start < 0 or (0 <= semi < start):
            continue
        depth, i = 0, start
        while i < len(text):
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            if depth == 0:
                break
            i += 1
        out.append((name, line_of(text, pos), text[start + 1:i]))
    return out


def audit(root):
    """Eski kod rentgeni: bir teshik buzilishi, takror tana, uzun metod.

    Bir teshik: maydon o'z sinfidagi domen metodlari orqali o'zgarsa to'g'ri
    (`registerOverdraft`, `close`); buzilish - boshqa sinfdan yozish
    (`a.setBalance(..)`, `a.balance = ..`) va ochiq `public` setter
    (clean-code 16.6, 36.12). Test fayllari hisobga olinmaydi. Sonlar
    refaktoringdan oldin va keyin solishtiriladi (architect 34.10).
    """
    outside, open_setters, dup, long_ = [], [], [], []
    seen = {}
    files = [p for p in java_files(root) if not is_test(p)]
    texts = {p: read(p) for p in files}
    for path in files:
        text, rel = texts[path], os.path.relpath(path, root)
        for field in sorted(set(FIELD_RE.findall(text))):
            cap = field[:1].upper() + field[1:]
            if re.search(r"\bpublic\s+\w+\s+set%s\s*\(" % re.escape(cap), text):
                open_setters.append("%s: `set%s` ochiq" % (rel, cap))
            call = re.compile(r"\.set%s\s*\(|\.%s\s*(?:[-+*/]?=)(?!=)" % (re.escape(cap), re.escape(field)))
            where = []
            for other in files:
                if other == path:
                    continue
                spans = methods(texts[other])
                for m in call.finditer(texts[other]):
                    owner = [n for pos, n, _ in spans if pos < m.start()]
                    where.append("%s.%s" % (os.path.basename(other)[:-5], owner[-1] if owner else "?"))
            if where:
                outside.append("%s: `%s` tashqaridan %d joyda yoziladi (%s)"
                               % (rel, field, len(where), ", ".join(sorted(set(where)))))
        for name, line, body in bodies(text):
            lines = [l.strip() for l in body.split("\n") if l.strip()]
            if len(lines) > LONG_METHOD:
                long_.append("%s:%d `%s` %d qator" % (rel, line, name, len(lines)))
            for i in range(len(lines) - 2):
                key = re.sub(r"\s+", "", "".join(lines[i:i + 3]))
                if len(key) < 60:
                    continue
                spot = "%s:%d `%s`" % (rel, line, name)
                if key in seen and seen[key] != spot:
                    dup.append("%s va %s" % (seen[key], spot))
                else:
                    seen.setdefault(key, spot)
    return outside, open_setters, sorted(set(dup)), long_


def main(argv):
    if len(argv) < 2 or (argv[1] == "--ozgartiradi" and len(argv) != 3):
        print(__doc__.strip().split("\n\n")[1])
        return 2
    root = argv[0]
    if argv[1] == "--audit":
        outside, open_setters, dup, long_ = audit(root)
        for title, rows in (("Tashqaridan yoziladigan maydon (clean-code 16.6, 33.18)", outside),
                            ("Ochiq setter (clean-code 36.12)", open_setters),
                            ("Takror blok (clean-code 32.2)", dup),
                            ("Uzun metod > %d qator (clean-code 32.3)" % LONG_METHOD, long_)):
            print("# %s: %d" % (title, len(rows)))
            for row in rows[:MAX_SHOWN]:
                print("  " + row)
        print("\naudit: %d tashqi yozuvchi, %d ochiq setter, %d takror, %d uzun metod"
              % (len(outside), len(open_setters), len(dup), len(long_)))
        return 0
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
