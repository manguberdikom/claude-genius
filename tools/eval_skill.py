#!/usr/bin/env python3
"""manguberdi zanjirining determinik qismini o'lchaydi.

    python3 tools/eval_skill.py

Nima o'lchanadi: aktyor ishni boshlaganda unga TO'G'RI qoidalar
beriladimi va mashina TO'G'RI muammolarni topadimi. Bu ikkisi zanjirning
poydevori: noto'g'ri ro'yxat bergan holda yaxshi natija kutib bo'lmaydi,
va reviewer topadigan narsa yozuvchiga oldindan berilmasa, ikkinchi
chaqiruv muqarrar.

Nima o'lchanmaydi, ochiq aytilsin: arxitektor yozgan kodning sifati.
Buning uchun modelni yurgizish kerak, u esa har safar boshqacha natija
beradi va pul turadi. Shu sababli bu yerda faqat har safar bir xil
javob beradigan qism o'lchanadi.

Har holat uchun uch o'lchov:
  marshrut  - kutilgan bob chiqdimi (eslab qolish)
  topilma   - kutilgan mexanik muammo topildimi
  taqiqlangan bob chiqmadi - holatga qo'lda yozilgan ikki bob chiqmadimi.
            Bu aniqlik (precision) emas: kutilgan ro'yxat ataylab minimal,
            ALWAYS boblari esa loyiha qarori, shuning uchun foiz yolg'on
            qizil berardi. Suyulishdan himoya alohida: marshrut
            MAX_CHAPTERS + ALWAYS dan oshmaydi.
va teskari tekshiruvlar: toza faylda shovqin bo'lmasin, "Avval yo'l
qo'yilgan xatolar" bo'limidagi har tavsif bo'sh yoki `---` bo'lmasin.

Kutilgan natijalar implementatsiya bilan birga yozilgan, shuning uchun
bu avvalambor REGRESSIYA qo'riqchisi: bob ko'chsa, belgi buzilsa yoki
marshrut suyulsa, shu yerda ko'rinadi. Mutlaq sifat o'lchovi emas.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from rules_for import ALWAYS, MAX_CHAPTERS  # noqa: E402

# Bitta fayl uchun marshrutning yuqori chegarasi: undan ko'pi suyulish.
MAX_ROUTED = MAX_CHAPTERS + len(ALWAYS)
JAVA = os.path.join("tools", "testdata", "java")
ENT = os.path.join("tools", "testdata", "entities")

# (nom, fayl, kutilgan boblar, kutilgan topilmalar, CHIQMASLIGI kerak boblar)
# Oxirgi ustun taqiqlangan boblar: pul bilan ishlaydigan faylga
# injection review bobi chiqsa, bu marshrut suyulganini bildiradi.
CASES = [
    ("tranzaksiya ichida HTTP", os.path.join(JAVA, "Bad.java"),
     [("architect", "19"), ("code-review", "19"),
      ("patterns", "17"), ("code-review", "22")],
     ["Tranzaksiya ichida tashqi chaqiruv", "Bo'sh catch",
      "printStackTrace", "aniq qiymat bermaydi", "System.out"],
     [("code-review", "29"), ("testing", "8")]),

    ("SQL injection va sir", os.path.join(JAVA, "Insecure.java"),
     [("code-review", "29"), ("code-review", "32"), ("code-review", "31")],
     [],
     [("testing", "8"), ("architect", "29")]),

    ("entity", os.path.join(ENT, "Order.java"),
     [("patterns", "9"), ("architect", "18"), ("sonarqube", "29")],
     [],
     [("code-review", "32"), ("testing", "5")]),

    ("flaky test", os.path.join(JAVA, "FlakyTest.java"),
     [("testing", "7"), ("testing", "5"), ("sonarqube", "19")],
     ["Thread.sleep"],
     [("code-review", "29"), ("architect", "19")]),

    ("konkurentlik", os.path.join(JAVA, "Concurrent.java"),
     [("architect", "11"), ("architect", "12")],
     [],
     [("code-review", "29"), ("testing", "5")]),

    ("broker", os.path.join(JAVA, "Consumer.java"),
     [("architect", "29"), ("patterns", "16")],
     [],
     [("code-review", "32"), ("testing", "8")]),

    ("pul va sana", os.path.join(JAVA, "Money.java"),
     [("clean-code", "20"), ("clean-code", "22")],
     ["aniq qiymat bermaydi"],
     [("code-review", "29"), ("testing", "5")]),

    ("bog'liqlik", os.path.join(JAVA, "pom.xml"),
     [("code-review", "33"), ("sonarqube", "39")],
     [],
     [("clean-code", "2"), ("code-review", "29")]),
]

# Toza fayl: marshrut bo'lsin, lekin mexanik topilma bo'lmasin.
CLEAN = [os.path.join(JAVA, "Good.java"), os.path.join(ENT, "Customer.java")]


def rules_for(path):
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "rules_for.py"), path],
        capture_output=True, text=True, cwd=ROOT)
    return proc.stdout


def routed(output):
    """Chiqishdagi "# Tegishli boblar" ro'yxati."""
    out, inside = set(), False
    for line in output.split("\n"):
        if line.startswith("# Tegishli boblar"):
            inside = True
            continue
        if inside:
            if line.startswith("#"):
                break
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                out.add((parts[0], parts[1]))
    return out


def findings(output):
    return [l for l in output.split("\n") if l.strip().startswith("[")]


def bad_feedback(output):
    """"# Avval yo'l qo'yilgan xatolar" dagi bo'sh yoki frontmatter tavsif.

    Har yozuv ikki qator: yo'l (2 bo'shliq) va tavsif (6 bo'shliq).
    Tavsif `---` bo'lsa, o'quvchi frontmatter chizig'ini oladi va aktyor
    xato o'rniga bezakni ko'radi.
    """
    lines, inside = [], False
    for line in output.split("\n"):
        if line.startswith("# Avval yo'l qo'yilgan xatolar"):
            inside = True
            continue
        if inside:
            if line.startswith("#"):
                break
            if line.strip():
                lines.append(line)
    bad = []
    for i, line in enumerate(lines):
        if line.startswith("  ") and not line.startswith("      "):
            note = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if not note or note.startswith("---") or not lines[i + 1].startswith("      "):
                bad.append(line.strip())
    return bad


def main():
    missing = [c[1] for c in CASES if not os.path.exists(os.path.join(ROOT, c[1]))]
    if missing:
        print("sinov fayllari yo'q: %s" % ", ".join(missing))
        return 1

    route_hit = route_total = find_hit = find_total = 0
    prec_ok = prec_total = 0
    rows, wide, feedback = [], [], set()

    for name, path, want_ch, want_find, forbid_ch in CASES:
        out = rules_for(path)
        got_ch = routed(out)
        found = "\n".join(findings(out))
        feedback.update(bad_feedback(out))
        if len(got_ch) > MAX_ROUTED:
            wide.append((name, len(got_ch)))

        ch_ok = [c for c in want_ch if c in got_ch]
        f_ok = [f for f in want_find if f in found]
        route_hit += len(ch_ok)
        route_total += len(want_ch)
        find_hit += len(f_ok)
        find_total += len(want_find)

        leaked = [c for c in forbid_ch if c in got_ch]
        prec_ok += len(forbid_ch) - len(leaked)
        prec_total += len(forbid_ch)

        rows.append((name, len(ch_ok), len(want_ch), len(f_ok), len(want_find),
                     [c for c in want_ch if c not in got_ch],
                     [f for f in want_find if f not in found], leaked))

    print("== Holatlar ==\n")
    print("%-26s %-9s %-9s %s" % ("holat", "marshrut", "topilma", "yetishmagani"))
    for name, ch, cht, fh, ft, miss_ch, miss_f, leaked in rows:
        gap = ", ".join("%s %s" % c for c in miss_ch) + \
              (" | " + ", ".join(m[:20] for m in miss_f) if miss_f else "") + \
              (" | ortiqcha: " + ", ".join("%s %s" % c for c in leaked)
               if leaked else "")
        print("%-26s %d/%-7d %d/%-7d %s"
              % (name, ch, cht, fh, ft, gap.strip(" |") or "-"))

    print("\n== Toza fayl: shovqin bo'lmasin ==\n")
    noise = 0
    for path in CLEAN:
        out = rules_for(path)
        found = findings(out)
        feedback.update(bad_feedback(out))
        ok = not found
        noise += not ok
        print("%-4s %-34s %d topilma" % ("OK" if ok else "XATO", path, len(found)))

    print("\n== Avvalgi xatolar: tavsif bo'sh yoki frontmatter emas ==\n")
    for rel in sorted(feedback):
        print("XATO %s" % rel)
    noise += len(feedback)
    if not feedback:
        print("OK")
    for name, count in wide:
        print("XATO %s: %d bob, chegara %d (marshrut suyulgan)"
              % (name, count, MAX_ROUTED))

    print("\n== Natija ==\n")
    r = 100 * route_hit / route_total if route_total else 0
    f = 100 * find_hit / find_total if find_total else 0
    print("  marshrut eslab qolish   : %3d/%-3d  (%.0f%%)" % (route_hit, route_total, r))
    print("  topilma eslab qolish    : %3d/%-3d  (%.0f%%)" % (find_hit, find_total, f))
    pr = 100 * prec_ok / prec_total if prec_total else 0
    print("  taqiqlangan bob chiqmadi: %3d/%-3d  (%.0f%%)" % (prec_ok, prec_total, pr))
    print("  marshrut chegarasida    : %3d/%-3d  (<= %d bob)"
          % (len(CASES) - len(wide), len(CASES), MAX_ROUTED))
    print("  shovqin                 : %d" % noise)

    failed = (route_hit < route_total or find_hit < find_total
              or prec_ok < prec_total or noise or wide)
    print("\n%s" % ("Hammasi joyida." if not failed
                    else "Yetishmovchilik bor, yuqoriga qarang."))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
