#!/usr/bin/env python3
"""Ko'chirilgan skill va aktyor fayllaridagi nisbiy yo'llarni mutlaq qiladi.

    python3 install/rewrite_paths.py <papka> --root <klon-yo'li> \
        [--python python3] [--bash bash]
    python3 install/rewrite_paths.py <papka> --root <klon> --tekshir
    python3 install/rewrite_paths.py <papka> --root <klon> \
        [--python P] [--bash B] --allow

Nega kerak: skill matni `python3 tools/rules_for.py` deb yozilgan va bu
yo'l JORIY papkaga nisbatan hal qilinadi. Klon ichida ishlaganda to'g'ri,
lekin skill global o'rnatilib boshqa proyektda ishlatilganda shu
buyruqlarning hammasi "No such file or directory" beradi. Klon ildizidagi
qoida fayli (`memory-protocol.md`) ham shunday: u ham mutlaq qilinadi.

Bu skript faqat ko'chirilgan `.md` matnini almashtiradi. Asboblar ROOT ni
o'z faylidan oladi, foydalanuvchi bergan nisbiy yo'lni va git ni esa
joriy papkadan hal qiladi; faqat matndagi yo'l almashtiriladi. Hook
chiqishidagi buyruqlar (suggest_sections, check_code, guard, budget)
asboblarning o'zida yasaladi va bu yerda tegilmaydi.

`--python` interpreterning to'liq yo'li (o'rnatuvchi `sys.executable` ni
beradi): Windows da `python3` nomi Store stub'iga tushadi. Sukut `python3`,
shuning uchun klon ichidagi xulq o'zgarmaydi. `--allow` faylga yozmaydi:
allaqachon almashtirilgan matnda uchragan har asbob uchun ruxsat qoidasini
JSON qilib chiqaradi. Qoida buyruq matnining aynan boshlanishi bo'lishi
shart, shuning uchun uni yo'lni yozgan funksiyaning o'zi yasaydi.

`doc.sh` bash skripti. Windows da bash har doim bo'lmaydi, shuning uchun
u ochiq chaqiriladi: `bash "<klon>/tools/doc.sh"`. `--bash` bilan berilgan
yo'lda bo'sh joy bo'lsa u ham qo'shtirnoqqa olinadi
(`"C:/Program Files/Git/bin/bash.exe"`), aks holda shell uni bo'lib
yuboradi. Bash topilmasa o'rnatuvchi buni aytadi, chunki qidiruv qatlami
usiz ishlamaydi.

Bu almashtirish aynan shu yerda, Python da turadi: PowerShell qismi
sinalmaydi, bu esa sinaladi.
"""

import argparse
import json
import os
import re
import sys

# Almashtiriladigan ko'rinishlar. Tartib muhim: uzunrog'i oldin, aks holda
# `python3 tools/x.py` ning `tools/x.py` qismi alohida tutilib qoladi.
# Interpreter va `bash` prefiksi naqshga kiradi, aks holda `python tools/x.py`
# dan `python python3 <klon>/...` chiqadi. Lookbehind harf, `/` va `.` ni
# rad etadi: shunda allaqachon mutlaq bo'lgan yo'l ikkinchi marta
# almashmaydi, `../tools/` dan esa `./tools/` qismi tutilmaydi. Backtick
# RAD ETILMAYDI, chunki markdown da buyruqlar aynan backtick ichida
# yoziladi va o'girilishi kerak bo'lgan yo'llarning ko'pi shu shaklda turadi.
PY_CALL = re.compile(r"(?<![\w/.])(?:python3?|py -3) (?:\./)?tools/([a-z_]+\.py)\b")
PY_BARE = re.compile(r"(?<![\w/.])(?:\./)?tools/([a-z_]+\.py)\b")
SH_CALL = re.compile(r"(?<![\w/.])(?:(?:bash|sh) )?(?:\./)?tools/(doc\.sh)\b")
MEM_PATH = re.compile(r"(?<![\w/])memory/(?=[\w<])")
# Klon ildizidagi, skill matni nomi bilan tilga oladigan fayllar. Ular
# Read bilan ham, shell argumenti sifatida ham (`awk '...' <fayl>`)
# o'qiladi, shuning uchun tools/ yo'li kabi qo'shtirnoqqa olinadi.
ROOT_FILES = ("memory-protocol.md",)
ROOT_FILE = re.compile(r"(?<![\w/.-])(%s)\b"
                       % "|".join(re.escape(name) for name in ROOT_FILES))
# Global o'rnatishda $CLAUDE_PROJECT_DIR foydalanuvchi proyekti, klon emas:
# undagi tools/ yo'li ham noto'g'ri. Almashtirilmaydi, faqat sanaladi.
PROJECT_TOOLS = re.compile(r"\$\{?CLAUDE_PROJECT_DIR\}?\"?/tools/")
# Qolganini sanash rewrite() naqshlaridan kengroq: tools/ dagi har .py va
# .sh, almashtirilmaydigani ham. Almashmagan yo'l jim o'tmasin, sanalsin.
LEFT_TOOLS = re.compile(r"(?<![\w/.])(?:\./)?tools/[a-z_]+\.(?:py|sh)\b")
# tools/ prefiksisiz doc.sh buyrug'i: rewrite() uni tanimaydi va global
# o'rnatishda u "command not found" beradi. Argumentsiz eslatma
# (`doc.sh show` deb nomini aytish) tutilmaydi, tools/test_skill.py dagi
# BARE_DOC_RE bilan bir xil qoida; toc argumentsiz ham to'liq buyruq.
BARE_DOC = re.compile(r"(?<![\w/.])doc\.sh (?:toc\b|(?:find|show|outline|path"
                      r"|rule|checklist)(?=\s+[-\w]))")
# --allow uchun: almashtirilgan matndagi asbob nomlari.
ABS_TOOL = re.compile(r"/tools/([a-z_]+\.(?:py|sh))\b")

TEXT_EXT = (".md",)


def quote(path):
    """Bo'sh joy bo'lsa qo'shtirnoq. Windows yo'lida bo'sh joy odatiy.

    Allaqachon qo'shtirnoqli qiymatga tegilmaydi: `--bash` ni qo'lda
    qo'shtirnoq bilan bergan foydalanuvchida ikki qavat chiqmasin."""
    if path.startswith('"') or " " not in path:
        return path
    return '"%s"' % path


def clean_root(root):
    return root.replace("\\", "/").rstrip("/")


def tool_cmd(root, runner, name):
    """rewrite() yozadigan buyruq boshlanishi: `<runner> <root>/tools/<name>`.

    rewrite() ham, allow_rules() ham shu yerdan oladi: ruxsat qoidasi
    buyruq matnining aynan boshlanishi bo'lmasa, mos kelmaydi."""
    return "%s %s" % (quote(runner.replace("\\", "/")),
                      quote("%s/tools/%s" % (root, name)))


def rewrite(text, root, bash="bash", python="python3"):
    """Matndagi nisbiy yo'llarni mutlaq qiladi. (yangi matn, almashtirish soni)."""
    root = clean_root(root)
    count = [0]

    def py(match):
        count[0] += 1
        return tool_cmd(root, python, match.group(1))

    def sh(match):
        count[0] += 1
        return tool_cmd(root, bash, match.group(1))

    def mem(_):
        count[0] += 1
        return "%s/memory/" % root

    def root_file(match):
        count[0] += 1
        return quote("%s/%s" % (root, match.group(1)))

    text = PY_CALL.sub(py, text)
    text = PY_BARE.sub(py, text)
    text = SH_CALL.sub(sh, text)
    text = MEM_PATH.sub(mem, text)
    text = ROOT_FILE.sub(root_file, text)
    return text, count[0]


def relative_left(text):
    """Almashtirilmagan nisbiy yo'llar. Bo'sh bo'lishi kerak."""
    out = []
    for pattern in (LEFT_TOOLS, BARE_DOC, MEM_PATH, ROOT_FILE, PROJECT_TOOLS):
        out.extend(match.group(0) for match in pattern.finditer(text))
    return out


def allow_rules(text, root, bash="bash", python="python3"):
    """Almashtirilgan matnda uchragan har asbob buyrug'i uchun ruxsat qoidasi."""
    root = clean_root(root)
    rules = set()
    for name in set(ABS_TOOL.findall(text)):
        prefix = tool_cmd(root, bash if name.endswith(".sh") else python, name)
        if re.search(re.escape(prefix) + r"(?![\w.])", text):
            rules.add("Bash(%s:*)" % prefix)
    return sorted(rules)


def walk(folder):
    for dirpath, _, names in os.walk(folder):
        for name in sorted(names):
            if name.endswith(TEXT_EXT):
                yield os.path.join(dirpath, name)


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("folder")
    parser.add_argument("--root", required=True)
    parser.add_argument("--bash", default="bash")
    parser.add_argument("--python", default="python3",
                        help="interpreter yo'li, skill buyruqlari shu bilan yoziladi")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--tekshir", action="store_true",
                      help="yozmaydi, faqat qolgan nisbiy yo'llarni sanaydi")
    mode.add_argument("--allow", action="store_true",
                      help="yozmaydi, ruxsat qoidalarini JSON qilib chiqaradi")
    args = parser.parse_args(argv)

    # Mavjud bo'lmagan klonga yo'l yozilsa, skill o'rnatiladi va har
    # buyruq "No such file" beradi: shu yerda to'xtaladi.
    if not os.path.isdir(args.root):
        print("root papka emas: %s" % args.root, file=sys.stderr)
        return 2

    if not os.path.isdir(args.folder):
        print("papka yo'q: %s" % args.folder, file=sys.stderr)
        return 2

    files = list(walk(args.folder))
    if not files:
        print("almashtiriladigan .md fayl topilmadi: %s" % args.folder,
              file=sys.stderr)
        return 1

    total = left = 0
    rules = set()
    for path in files:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
        if args.allow:
            rules.update(allow_rules(text, args.root, args.bash, args.python))
            continue
        if args.tekshir:
            remaining = relative_left(text)
            left += len(remaining)
            if remaining:
                print("%s: %d nisbiy yo'l qoldi (%s)"
                      % (os.path.basename(path), len(remaining),
                         ", ".join(sorted(set(remaining))[:3])))
            continue
        new, count = rewrite(text, args.root, args.bash, args.python)
        total += count
        if new != text:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(new)

    if args.allow:
        # Faqat JSON: o'rnatuvchi chiqishni to'g'ridan-to'g'ri o'qiydi.
        print(json.dumps(sorted(rules)))
        return 0
    if args.tekshir:
        print("%d fayl tekshirildi, %d nisbiy yo'l qoldi" % (len(files), left))
        return 1 if left else 0
    print("%d fayl, %d yo'l mutlaq qilindi" % (len(files), total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
