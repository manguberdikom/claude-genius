#!/usr/bin/env python3
"""install/rewrite_paths.py uchun sinovlar.

    python3 tools/test_rewrite_paths.py

Nega bu asbobga sinov kerak: o'rnatuvchining PowerShell qismi sinalmaydi,
shuning uchun u iloji boricha ozroq ish qilishi va asosiy mantiq shu
yerda, sinaladigan joyda turishi kerak. Noto'g'ri almashtirish jim
o'tadi: skill o'rnatiladi, ko'rinishidan joyida, lekin har buyruq
"No such file or directory" beradi.
"""

import io
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "install"))

import rewrite_paths as R  # noqa: E402

GENIUS = "C:/src/claude-genius"


def one(text, root=GENIUS, bash="bash"):
    return R.rewrite(text, root, bash)


def case_python_chaqiruvi():
    out, n = one("python3 tools/rules_for.py <fayllar>")
    return n == 1 and out == "python3 %s/tools/rules_for.py <fayllar>" % GENIUS


def case_backtick_ichida():
    """Markdown da buyruqlar backtick ichida yoziladi: ular ham almashadi."""
    out, n = one("`tools/doc.sh show patterns 17.2`")
    return n == 1 and out == "`bash %s/tools/doc.sh show patterns 17.2`" % GENIUS


def case_python3siz_py():
    out, n = one("chiqishni tools/parse_test_output.py ga bering")
    return n == 1 and "python3 %s/tools/parse_test_output.py" % GENIUS in out


def case_doc_sh_bash_bilan():
    out, _ = one("tools/doc.sh find saga")
    return out.startswith("bash %s/tools/doc.sh" % GENIUS)


def case_bash_nomi_beriladi():
    """Qo'lda qo'shtirnoq bilan berilgan bash ikki qavat o'ralmaydi."""
    out, _ = one("tools/doc.sh toc", bash='"C:/Git/bin/bash.exe"')
    return out == '"C:/Git/bin/bash.exe" %s/tools/doc.sh toc' % GENIUS


def case_bash_bosh_joyli_qoshtirnoqlanadi():
    """O'rnatuvchi bash yo'lini qo'shtirnoqsiz beradi. Git for Windows
    standart holda `Program Files` da: qo'shtirnoqsiz yo'lni shell
    `C:/Program` ga bo'lib yuboradi va har doc.sh buyrug'i yiqiladi."""
    out, _ = one("tools/doc.sh toc", bash="C:/Program Files/Git/bin/bash.exe")
    return out == '"C:/Program Files/Git/bin/bash.exe" %s/tools/doc.sh toc' % GENIUS


def case_bash_teskari_slash():
    out, _ = one("tools/doc.sh toc",
                 bash="C:\\Program Files\\Git\\bin\\bash.exe")
    return out == '"C:/Program Files/Git/bin/bash.exe" %s/tools/doc.sh toc' % GENIUS


def case_bash_bosh_joysiz_qoshtirnoqsiz():
    out, _ = one("tools/doc.sh toc", bash="C:/Git/bin/bash.exe")
    return out == "C:/Git/bin/bash.exe %s/tools/doc.sh toc" % GENIUS


def case_bash_prefiksi_ikkilanmaydi():
    out, n = one("`bash tools/doc.sh find saga`")
    return n == 1 and out == "`bash %s/tools/doc.sh find saga`" % GENIUS


def case_python_3siz_chaqiruv():
    out, n = one("python tools/check_code.py a")
    return n == 1 and out == "python3 %s/tools/check_code.py a" % GENIUS


def case_nuqta_slash():
    sh, n1 = one("./tools/doc.sh toc")
    py, n2 = one("python3 ./tools/rules_for.py x")
    return (n1 == 1 and sh == "bash %s/tools/doc.sh toc" % GENIUS
            and n2 == 1 and py == "python3 %s/tools/rules_for.py x" % GENIUS)


def case_memory_protocol():
    """Klon ildizidagi qoida fayli ham mutlaq bo'ladi va qayta tutilmaydi."""
    out, n = one("Qoida manbai `memory-protocol.md`.")
    second, n2 = one(out)
    return (n == 1 and out == "Qoida manbai `%s/memory-protocol.md`." % GENIUS
            and n2 == 0 and second == out
            and R.relative_left("`memory-protocol.md`") == ["memory-protocol.md"])


def case_memory_protocol_bosh_joyli():
    """Fayl `awk '...' <fayl>` argumenti ham bo'ladi: bo'sh joyda qo'shtirnoq."""
    out, _ = one("`awk '/x/' memory-protocol.md`", root="C:/Program Files/genius")
    return out == "`awk '/x/' \"C:/Program Files/genius/memory-protocol.md\"`"


def case_memory_yoli():
    out, n = one("`memory/<proyekt-slug>/MEMORY.md` indeksini o'qing")
    return n == 1 and "%s/memory/<proyekt-slug>/" % GENIUS in out


def case_mutlaq_yol_tegilmaydi():
    """Allaqachon mutlaq yo'l ikkinchi marta almashmaydi."""
    text = "python3 /opt/genius/tools/rules_for.py x"
    out, n = one(text)
    return n == 0 and out == text


def case_idempotent():
    """Ikki marta yurgizish bir marta bilan bir xil natija beradi."""
    text = ("python3 tools/rules_for.py x va tools/doc.sh find y, "
            "`memory/umumiy/` va `memory-protocol.md`")
    first, _ = one(text)
    second, n = one(first)
    spaced = dict(root="C:/Program Files/genius",
                  bash="C:/Program Files/Git/bin/bash.exe")
    first_sp, _ = one(text, **spaced)
    second_sp, n_sp = one(first_sp, **spaced)
    return n == 0 and second == first and n_sp == 0 and second_sp == first_sp


def case_teskari_slash_tozalanadi():
    out, _ = one("tools/doc.sh toc", root="C:\\src\\claude-genius\\")
    return out == "bash C:/src/claude-genius/tools/doc.sh toc"


def case_bosh_joyli_yol_qoshtirnoqda():
    out, _ = one("python3 tools/budget.py --holat",
                 root="C:/Program Files/genius")
    return '"C:/Program Files/genius/tools/budget.py"' in out


def case_quvur_ichida():
    out, n = one("mvn -q test | python3 tools/parse_test_output.py")
    return n == 1 and out.endswith("%s/tools/parse_test_output.py" % GENIUS)


def case_qolgani_sanaladi():
    left = R.relative_left("tools/doc.sh va python3 tools/x.py va memory/umumiy/")
    more = R.relative_left("./tools/doc.sh, `memory-protocol.md` va "
                           "$CLAUDE_PROJECT_DIR/tools/guard.py")
    return len(left) == 3 and len(more) == 3


def case_almashtirilgandan_keyin_qolmaydi():
    out, _ = one("tools/doc.sh va python3 tools/x.py va memory/umumiy/")
    return R.relative_left(out) == []


def case_papkani_yuradi():
    """Papkadagi har .md fayl almashadi, boshqa tur tegilmaydi."""
    tmp = tempfile.mkdtemp(prefix="rw_")
    try:
        sub = os.path.join(tmp, "references")
        os.makedirs(sub)
        io.open(os.path.join(tmp, "SKILL.md"), "w", encoding="utf-8").write(
            "python3 tools/budget.py --holat")
        io.open(os.path.join(sub, "a.md"), "w", encoding="utf-8").write(
            "tools/doc.sh toc")
        io.open(os.path.join(tmp, "b.txt"), "w", encoding="utf-8").write(
            "tools/doc.sh toc")
        files = list(R.walk(tmp))
        if len(files) != 2:
            return False
        for path in files:
            text = io.open(path, encoding="utf-8").read()
            new, _ = R.rewrite(text, GENIUS)
            io.open(path, "w", encoding="utf-8").write(new)
        skill = io.open(os.path.join(tmp, "SKILL.md"), encoding="utf-8").read()
        nested = io.open(os.path.join(sub, "a.md"), encoding="utf-8").read()
        plain = io.open(os.path.join(tmp, "b.txt"), encoding="utf-8").read()
        return (GENIUS in skill and GENIUS in nested
                and plain == "tools/doc.sh toc")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def case_haqiqiy_skill_toza_qoladi():
    """Haqiqiy skill nusxasida bitta ham nisbiy yo'l qolmaydi."""
    tmp = tempfile.mkdtemp(prefix="rw_real_")
    try:
        shutil.copytree(os.path.join(ROOT, ".claude", "skills", "manguberdi"),
                        os.path.join(tmp, "manguberdi"))
        agents = os.path.join(tmp, "agents")
        os.makedirs(agents)
        src = os.path.join(ROOT, ".claude", "agents")
        for name in os.listdir(src):
            if name.endswith(".md"):
                shutil.copy(os.path.join(src, name), agents)
        changed = 0
        for path in R.walk(tmp):
            text = io.open(path, encoding="utf-8").read()
            new, count = R.rewrite(text, GENIUS)
            changed += count
            io.open(path, "w", encoding="utf-8").write(new)
        texts = [io.open(p, encoding="utf-8").read() for p in R.walk(tmp)]
        left = sum(len(R.relative_left(t)) for t in texts)
        # relative_left faqat ma'lum naqshlarni sanaydi. Klon ildizidagi
        # yangi faylga havola qo'shilsa, u naqshda yo'q va sinov yolg'on
        # yashil beradi (memory-protocol.md aynan shunday topildi). Shuning
        # uchun ildizdagi har .md nomi alohida qidiriladi. CLAUDE.md va
        # README.md maqsadli proyektning o'z fayli, ular nisbiy qoladi.
        names = [n for n in os.listdir(ROOT) if n.endswith(".md")
                 and n not in ("CLAUDE.md", "README.md")]
        stray = [n for n in names for t in texts
                 if re.search(r"(?<![\w/.-])%s\b" % re.escape(n), t)]
        # Almashtirish bo'lishi SHART: nol bo'lsa, naqsh hech narsani
        # tutmagan va sinov yolg'on yashil beradi.
        return changed > 30 and left == 0 and not stray
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


CASES = [
    ("python3 tools/x.py", case_python_chaqiruvi),
    ("backtick ichidagi buyruq", case_backtick_ichida),
    ("python3 siz .py yo'li", case_python3siz_py),
    ("doc.sh bash bilan chaqiriladi", case_doc_sh_bash_bilan),
    ("bash yo'li berilsa ishlatiladi", case_bash_nomi_beriladi),
    ("bo'sh joyli bash yo'li qo'shtirnoqda", case_bash_bosh_joyli_qoshtirnoqlanadi),
    ("bash yo'lidagi teskari slash", case_bash_teskari_slash),
    ("bo'sh joysiz bash qo'shtirnoqsiz", case_bash_bosh_joysiz_qoshtirnoqsiz),
    ("bash prefiksi ikkilanmaydi", case_bash_prefiksi_ikkilanmaydi),
    ("python (3 siz) chaqiruvi", case_python_3siz_chaqiruv),
    ("./tools/ yo'li", case_nuqta_slash),
    ("memory-protocol.md", case_memory_protocol),
    ("bo'sh joyli memory-protocol.md qo'shtirnoqda", case_memory_protocol_bosh_joyli),
    ("memory yo'li", case_memory_yoli),
    ("mutlaq yo'l tegilmaydi", case_mutlaq_yol_tegilmaydi),
    ("ikki marta yurgizish xavfsiz", case_idempotent),
    ("teskari slash to'g'rilanadi", case_teskari_slash_tozalanadi),
    ("bo'sh joyli yo'l qo'shtirnoqda", case_bosh_joyli_yol_qoshtirnoqda),
    ("quvur ichidagi chaqiruv", case_quvur_ichida),
    ("qolgan nisbiy yo'l sanaladi", case_qolgani_sanaladi),
    ("almashtirgandan keyin qolmaydi", case_almashtirilgandan_keyin_qolmaydi),
    ("papka bo'ylab yuradi, .md dan boshqasi tegilmaydi", case_papkani_yuradi),
    ("haqiqiy skillda nol nisbiy yo'l", case_haqiqiy_skill_toza_qoladi),
]


def main():
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn())
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
