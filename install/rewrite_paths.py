#!/usr/bin/env python3
"""Ko'chirilgan skill va aktyor fayllaridagi nisbiy yo'llarni mutlaq qiladi.

    python3 install/rewrite_paths.py <papka> --root <klon-yo'li> [--bash bash]
    python3 install/rewrite_paths.py <papka> --root <klon> --tekshir

Nega kerak: skill matni `python3 tools/rules_for.py` deb yozilgan va bu
yo'l JORIY papkaga nisbatan hal qilinadi. Klon ichida ishlaganda to'g'ri,
lekin skill global o'rnatilib boshqa proyektda ishlatilganda shu
buyruqlarning hammasi "No such file or directory" beradi. Asboblarning
o'zi joyga bog'liq emas (ROOT ni o'z faylidan hisoblaydi), faqat matndagi
yo'l almashtiriladi.

`doc.sh` bash skripti. Windows da bash har doim bo'lmaydi, shuning uchun
u ochiq chaqiriladi: `bash "<klon>/tools/doc.sh"`. Bash topilmasa
o'rnatuvchi buni aytadi, chunki qidiruv qatlami usiz ishlamaydi.

Bu almashtirish aynan shu yerda, Python da turadi: PowerShell qismi
sinalmaydi, bu esa sinaladi.
"""

import argparse
import os
import re
import sys

# Almashtiriladigan ko'rinishlar. Tartib muhim: uzunrog'i oldin, aks holda
# `python3 tools/x.py` ning `tools/x.py` qismi alohida tutilib qoladi.
# Lookbehind faqat harf va `/` ni rad etadi: shunda allaqachon mutlaq
# bo'lgan yo'l ikkinchi marta almashmaydi. Backtick RAD ETILMAYDI, chunki
# markdown da buyruqlar aynan backtick ichida yoziladi va o'girilishi
# kerak bo'lgan yo'llarning ko'pi shu shaklda turadi.
PY_CALL = re.compile(r"(?<![\w/])python3 tools/([a-z_]+\.py)\b")
PY_BARE = re.compile(r"(?<![\w/])tools/([a-z_]+\.py)\b")
SH_CALL = re.compile(r"(?<![\w/])tools/(doc\.sh)\b")
MEM_PATH = re.compile(r"(?<![\w/])memory/(?=[\w<])")

TEXT_EXT = (".md",)


def quote(path):
    """Bo'sh joy bo'lsa qo'shtirnoq. Windows yo'lida bo'sh joy odatiy."""
    return '"%s"' % path if " " in path else path


def rewrite(text, root, bash="bash"):
    """Matndagi nisbiy yo'llarni mutlaq qiladi. (yangi matn, almashtirish soni)."""
    root = root.replace("\\", "/").rstrip("/")
    count = [0]

    def py(match):
        count[0] += 1
        return "python3 %s" % quote("%s/tools/%s" % (root, match.group(1)))

    def sh(match):
        count[0] += 1
        return "%s %s" % (bash, quote("%s/tools/%s" % (root, match.group(1))))

    def mem(_):
        count[0] += 1
        return "%s/memory/" % root

    text = PY_CALL.sub(py, text)
    text = PY_BARE.sub(py, text)
    text = SH_CALL.sub(sh, text)
    text = MEM_PATH.sub(mem, text)
    return text, count[0]


def relative_left(text):
    """Almashtirilmagan nisbiy yo'llar. Bo'sh bo'lishi kerak."""
    out = []
    for match in re.finditer(r"(?<![\w/])tools/[a-z_]+\.(?:py|sh)\b", text):
        out.append(match.group(0))
    for match in re.finditer(r"(?<![\w/])memory/(?=[\w<])", text):
        out.append(match.group(0))
    return out


def walk(folder):
    for dirpath, _, names in os.walk(folder):
        for name in sorted(names):
            if name.endswith(TEXT_EXT):
                yield os.path.join(dirpath, name)


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("folder")
    parser.add_argument("--root", required=True)
    parser.add_argument("--bash", default="bash")
    parser.add_argument("--tekshir", action="store_true",
                        help="yozmaydi, faqat qolgan nisbiy yo'llarni sanaydi")
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print("papka yo'q: %s" % args.folder, file=sys.stderr)
        return 2

    files = list(walk(args.folder))
    if not files:
        print("almashtiriladigan .md fayl topilmadi: %s" % args.folder,
              file=sys.stderr)
        return 1

    total = left = 0
    for path in files:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        if args.tekshir:
            remaining = relative_left(text)
            left += len(remaining)
            if remaining:
                print("%s: %d nisbiy yo'l qoldi (%s)"
                      % (os.path.basename(path), len(remaining),
                         ", ".join(sorted(set(remaining))[:3])))
            continue
        new, count = rewrite(text, args.root, args.bash)
        total += count
        if new != text:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(new)

    if args.tekshir:
        print("%d fayl tekshirildi, %d nisbiy yo'l qoldi" % (len(files), left))
        return 1 if left else 0
    print("%d fayl, %d yo'l mutlaq qilindi" % (len(files), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
