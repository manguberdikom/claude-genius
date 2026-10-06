#!/usr/bin/env python3
"""doc.sh find ning aniqligini o'lchaydi.

    python3 tools/eval_find.py [namuna_soni] [--oltin]

--oltin: faqat E sinovi (oltin to'plam), bir necha soniya.

Nega kerak: qidiruv ishlayotgani "topdi" degani emas. Kerakli bo'lim
yuzinchi qatorda chiqsa, u amalda topilmagan bilan barobar. Shuning uchun
topilish emas, O'RIN o'lchanadi. Hujjat o'zgarganda yoki find mantig'i
tahrirlanganda qayta ishga tushiriladi: pasayish shu yerda ko'rinadi.

Besh sinov:
  A. Taxallus bo'yicha - inglizcha nomni so'raydi. Oson yo'l, aliases.tsv
     ni tekshiradi: taxallus yo'lining smoke testi (aylanma: so'rov ham,
     javob ham shu jadvaldan).
  B. Matn ichidagi atama bo'yicha - bo'lim TANASIDAN kamyob atama olinadi
     va `find -f` bilan so'raladi. Namuna xesh bilan olinadi (sha1
     sarlavhadan, mod B_MOD), ya'ni bo'lim qo'shilsa yoki o'chsa faqat
     o'sha bo'lim namunaga kiradi yoki chiqadi, qolgani joyida qoladi.
     Chegara: bazaviy natija minus 3 so'rov. 1-o'rin va top-3 faqat
     ma'lumot uchun: yorliq bitta bo'lim, atama esa ko'pincha 2-3
     bo'limda turadi, ya'ni 1-o'rin reytingni emas, yorliq shovqinini
     o'lchaydi.
  C. Reyting - belgilangan so'rovlarda `find -f` chiqishidagi "(N marta)"
     sonlari kamayib borishi kerak. Determinik: saralash olib tashlansa
     yoki buzilsa A va B yashil qolardi, bu sinov esa yiqiladi.
  D. `doc.sh rule` reytingi (pastda).
  E. Oltin to'plam - realistik so'rovlar (tools/testdata/find_golden.tsv
     va prompts_golden.tsv). find kalit so'rov bilan, hook
     (suggest_sections) foydalanuvchi prompti bilan o'lchanadi. dev va
     holdout alohida chiqadi. Sozlash faqat dev ga qarab qilinadi,
     holdout esa o'zgarish yomonlashtirmaganini ko'rsatadi: holdout
     pasaysa o'zgarish qaytariladi. Holdout topilmalari shuning uchun
     chop etilmaydi.

B uchun so'rov tanlash muhim: `kerak` yoki `spring` kabi korpusda mingdan
ortiq uchraydigan so'z real so'rov emas va natijani buzadi, shuning uchun
atama korpusda 20 martadan kam uchrashi shart.
"""

import collections
import hashlib
import math
import os
import random
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = os.path.join(ROOT, "tools", "doc.sh")
# Windows .sh ni o'zi yurgiza olmaydi: bash PATH tartibida (test_doc.py kabi).
SHELL = [shutil.which("bash") or "bash"] if os.name == "nt" else []
SECTIONS = os.path.join(ROOT, "index", "sections.tsv")
ALIASES = os.path.join(ROOT, "index", "aliases.tsv")
TESTDATA = os.path.join(ROOT, "tools", "testdata")
GOLDEN_FIND = os.path.join(TESTDATA, "find_golden.tsv")
GOLDEN_PROMPTS = os.path.join(TESTDATA, "prompts_golden.tsv")

DEFAULT_SAMPLE = 120
TOP_N = 60                 # find dan shuncha natija so'raladi
MAX_CORPUS_FREQ = 20       # bundan ko'p uchraydigan atama so'rov sifatida yaroqsiz
IDENT_RE = re.compile(r"`([A-Za-z_][A-Za-z0-9_.]{4,40})`")
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*")

# A ning pastki chegarasi, foizda. Nega 100 emas: so'rovlar korpusdan
# TASODIFIY olinadi, shuning uchun ba'zida `author` kabi umumiy so'z
# tushadi va u o'nlab bo'limda uchraydi. Bitta shunday so'rov tufayli har
# safar "yiqildi" deb chiqadigan o'lchov e'tibordan qoladi, ya'ni umuman
# o'lchamagan bilan barobar.
# 1-o'rin: aniq moslik darajasidan oldin 116/120 edi, chegara shu (97%).
FLOORS_A = {"topildi": 99, "1-o'rin": 97, "top-3": 98}
# Namuna o'zining generatori bilan: avval global random.seed(7) edi va
# aliases.tsv dagi o'zgarish B namunasini ham almashtirardi.
A_SEED = 7

# B: sarlavha xeshi shu songa bo'linsa bo'lim namunaga kiradi (~120 ta).
B_MOD = 13
# Bazaviy natija (2026-10-06, 121 so'rov) va chegara = bazaviy - 3 so'rov.
# Chegara qiymatga teng bo'lsa korpus tahriri tasodifan qizil berardi.
B_BASE = {"topildi": 121, "top-10": 117}
B_SLACK = 3

# E: oltin to'plam chegaralari, sanoqda: (to'plam, o'lchov) -> kamida.
# Qiymat oxirgi o'lchovdan bitta so'rov past (1 so'rov tolerantlik).
# Bazaviy raqamlar (find va hook o'zgarishidan oldin, 2026-10-06):
#   find  dev     topildi 18/32, 1-o'rin 14, top-3 18
#   find  holdout topildi 20/35, 1-o'rin 13, top-3 19
#   hook  dev     1-o'rin 10/34, top-3 15, topildi 16, aniqlik 34/82, jim 7/9
#   hook  holdout 1-o'rin 11/27, top-3 16, topildi 16, aniqlik 34/75, jim 5/6
# find ning daraja, transliteratsiya va so'zlar bo'yicha zaxirasi hamda
# hook kirishini tozalashdan keyin (shu chegaralar shundan):
#   find  dev     topildi 28/32, 1-o'rin 26, top-3 27
#   find  holdout topildi 30/35, 1-o'rin 22, top-3 28
#   hook  dev     1-o'rin 15/34, top-3 18, topildi 19, aniqlik 38/87, jim 7/9
#   hook  holdout 1-o'rin 11/27, top-3 17, topildi 17, aniqlik 34/75, jim 5/6
# exceptions.tsv ni find ishlatgandan va erkin gap iboralari (R3.3, R3.5)
# dan keyin (dev ga 3 ta uz-erkin qator qo'shildi: 37 ta):
#   find  dev     topildi 30/32, 1-o'rin 28, top-3 29
#   find  holdout topildi 32/35, 1-o'rin 27, top-3 31
#   hook  dev     1-o'rin 24/37, top-3 29, topildi 30, aniqlik 61/110, jim 7/9
#   hook  holdout 1-o'rin 14/27, top-3 18, topildi 18, aniqlik 37/75, jim 5/6
FLOORS_E = {
    ("find", "dev"): {"topildi": 29, "1-o'rin": 27, "top-3": 28},
    ("find", "holdout"): {"topildi": 31, "1-o'rin": 26, "top-3": 30},
    ("hook", "dev"): {"1-o'rin": 23, "top-3": 28, "jim": 6},
    ("hook", "holdout"): {"1-o'rin": 10, "top-3": 16, "jim": 4},
}

# C uchun so'rovlar: korpusda har xil sonda uchraydi, shuning uchun tartib
# buzilsa ko'rinadi. Hammasi bir martadan uchrasa sinov bo'sh o'tardi.
RANK_QUERIES = ("pg_stat_statements", "HikariCP", "outbox")
COUNT_RE = re.compile(r"\((\d+) marta\)$")


def rows(path):
    with open(path, encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == len(header):
                yield dict(zip(header, parts))


def run_find(query, full):
    args = SHELL + [DOC, "find", "-n", str(TOP_N)] + (["-f"] if full else []) + [query]
    start = time.perf_counter()
    proc = subprocess.run(args, capture_output=True, encoding="utf-8", cwd=ROOT)
    elapsed = time.perf_counter() - start
    hits = []
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            hits.append((parts[0], parts[1]))
    return hits, elapsed


def rank_of(hits, target):
    for position, hit in enumerate(hits, 1):
        if hit == target:
            return position
    return None


def report(name, ranks, times, total, floors):
    """floors: o'lchov -> kamida nechta so'rov (sanoqda)."""
    found = [r for r in ranks if r is not None]
    times = sorted(times)
    failed = []
    print("\n== %s (%d ta so'rov) ==" % (name, total))
    for label, count in (
        ("topildi", len(found)),
        ("1-o'rin", sum(1 for r in found if r == 1)),
        ("top-3", sum(1 for r in found if r <= 3)),
        ("top-10", sum(1 for r in found if r <= 10)),
    ):
        pct = 100 * count / total if total else 0
        floor = floors.get(label)
        mark = ""
        if floor is not None:
            if count < floor:
                mark = "  CHEGARADAN PAST (kamida %d)" % floor
                failed.append(label)
            else:
                mark = "  chegara %d" % floor
        print("  %-8s %3d/%d  (%3.0f%%)%s" % (label, count, total, pct, mark))
    if times:
        print("  vaqt     median %.0f ms, p95 %.0f ms, max %.0f ms"
              % (1000 * times[len(times) // 2],
                 1000 * times[int(0.95 * (len(times) - 1))],
                 1000 * times[-1]))
    return not failed


def sha1_int(text):
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest(), 16)


def section_bodies():
    """Har bo'lim uchun sarlavhasi va tanasidagi backtick atamalar."""
    cache, out = {}, []
    for row in rows(SECTIONS):
        if not row["section"]:
            continue
        path = os.path.join(ROOT, row["file"])
        if path not in cache:
            with open(path, encoding="utf-8") as handle:
                cache[path] = handle.read().split("\n")
        body = "\n".join(cache[path][int(row["start"]):int(row["end"])])
        idents = set(IDENT_RE.findall(body))
        if idents:
            out.append((row["doc"], row["section"], row["title"], idents))
    return out


def corpus_token_freq():
    """Butun korpusdagi so'z chastotasi, kichik harfda."""
    freq = collections.Counter()
    for dirpath, _, filenames in os.walk(os.path.join(ROOT, "docs")):
        for name in filenames:
            if name.endswith(".md"):
                with open(os.path.join(dirpath, name), encoding="utf-8") as handle:
                    for token in WORD_RE.findall(handle.read()):
                        freq[token.lower()] += 1
    return freq


def percent_floor(percent, total):
    """Foizli chegara sanoqqa: avvalgi `pct + 0.5 < floor` bilan bir xil."""
    return math.ceil((percent - 0.5) * total / 100 - 1e-9)


def test_aliases(sample_size):
    pool = [r for r in rows(ALIASES) if r["kind"] == "section"]
    sample = random.Random(A_SEED).sample(pool, min(sample_size, len(pool)))
    ranks, times, misses = [], [], []
    for row in sample:
        hits, elapsed = run_find(row["alias"], full=False)
        rank = rank_of(hits, (row["doc"], row["ref"]))
        ranks.append(rank)
        times.append(elapsed)
        if rank is None:
            misses.append((row["alias"], row["doc"], row["ref"]))
    floors = {k: percent_floor(v, len(sample)) for k, v in FLOORS_A.items()}
    return report("A. Taxallus bo'yicha", ranks, times, len(sample),
                  floors), misses


def test_identifiers(sample_size):
    sections = section_bodies()
    corpus = corpus_token_freq()
    per_section = collections.Counter()
    for _, _, _, idents in sections:
        for ident in idents:
            per_section[ident] += 1

    usable = []
    for doc, section, title, idents in sections:
        good = sorted(i for i in idents
                      if 1 <= per_section[i] <= 3
                      and corpus[i.lower()] <= MAX_CORPUS_FREQ)
        if good:
            usable.append((doc, section, title, good))

    # Raqam emas, sarlavha: bob ichida bo'lim ko'chsa namuna o'zgarmaydi.
    default = sample_size == DEFAULT_SAMPLE
    mod = B_MOD if default else max(1, round(len(usable) / sample_size))
    sample = [u for u in usable if sha1_int(u[0] + "\t" + u[2]) % mod == 0]
    ranks, times, misses = [], [], []
    for doc, section, title, idents in sample:
        query = min(idents, key=lambda i: sha1_int(doc + "\t" + title + "\t" + i))
        hits, elapsed = run_find(query, full=True)
        rank = rank_of(hits, (doc, section))
        ranks.append(rank)
        times.append(elapsed)
        if rank is None:
            misses.append((query, doc, section))
    print("\n  %d bo'limdan %d tasida yaroqli atama bor, namuna: sha1 mod %d"
          % (len(sections), len(usable), mod))
    floors = {k: v - B_SLACK for k, v in B_BASE.items()} if default else {}
    return report("B. Matn ichidagi atama bo'yicha", ranks, times,
                  len(sample), floors), misses


def test_ranking():
    """find -f: ko'p uchragan bo'lim yuqorida turadimi."""
    print("\n== C. find -f reytingi (%d ta so'rov) ==" % len(RANK_QUERIES))
    ok, varied = True, False
    for query in RANK_QUERIES:
        proc = subprocess.run(SHELL + [DOC, "find", "-f", "-n", str(TOP_N), query],
                              capture_output=True, encoding="utf-8", cwd=ROOT)
        counts = [int(m.group(1)) for m in
                  (COUNT_RE.search(l) for l in proc.stdout.splitlines()) if m]
        good = bool(counts) and counts == sorted(counts, reverse=True)
        varied = varied or len(set(counts)) > 1
        ok = ok and good
        print("  %-4s %-20s %s" % ("OK" if good else "XATO", query,
                                   " ".join(map(str, counts[:12])) or "-"))
    if not varied:
        print("  XATO: hech bir so'rovda son farq qilmadi, tartib sinalmadi")
    return ok and varied


# `doc.sh rule <kalit>`: kalitni faqat o'tib ketgan eslatma sifatida
# tilga olgan bo'lim (glossariy, kirish, kod izohi) birinchi javob
# bo'lmasligi kerak. (kalit, pastda turishi kerak bo'lgan bo'limlar).
RULE_QUERIES = (
    ("java:S2259", ("sonarqube 43.14", "sonarqube 24.1", "sonarqube 1.4")),
)


def test_rule_ranking():
    """doc.sh rule: illustrativ eslatma yuqoriga chiqmaydi."""
    print("\n== D. doc.sh rule reytingi (%d ta kalit) ==" % len(RULE_QUERIES))
    ok = True
    for rule, demoted in RULE_QUERIES:
        proc = subprocess.run(SHELL + [DOC, "rule", rule],
                              capture_output=True, encoding="utf-8", cwd=ROOT)
        order = []
        for line in proc.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 3 and parts[0].isalpha() and not line.startswith(">"):
                order.append("%s %s" % (parts[0], parts[1]))
        if not order:
            print("  XATO %-14s chiqish bo'sh" % rule)
            ok = False
            continue
        half = len(order) // 2
        bad = [ref for ref in demoted
               if ref in order and order.index(ref) < half]
        good = not bad and order[0] not in demoted
        ok = ok and good
        print("  %-4s %-14s birinchi: %-16s pastda kutilgani: %s"
              % ("OK" if good else "XATO", rule, order[0],
                 ", ".join(bad) and "YUQORIDA: " + ", ".join(bad) or "joyida"))
    return ok


def golden(path):
    """Oltin to'plam qatorlari: `#` izoh, birinchi qolgan qator sarlavha.

    qabul: {(hujjat, raqam)} yoki None (`-`: hook jim qolishi kerak).
    Matndagi `\n` va `\t` yangi qator va tab bo'ladi.
    """
    out, header = [], None
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if header is None:
                header = parts
                continue
            row = dict(zip(header, parts))
            text = row.get("sorov") or row.get("prompt") or ""
            row["text"] = text.replace("\\n", "\n").replace("\\t", "\t")
            acc = row["qabul"].strip()
            row["accept"] = None if acc == "-" else {
                tuple(ref.split(":", 1)) for ref in acc.split()}
            out.append(row)
    return out


def first_rank(hits, accept):
    for position, hit in enumerate(hits, 1):
        if hit in accept:
            return position
    return None


def check_floors(kind, part, counts):
    floors = FLOORS_E.get((kind, part), {})
    return [label for label, floor in floors.items() if counts.get(label, 0) < floor]


def print_table(title, labels, results):
    """results: to'plam -> (o'lchov -> (son, maxraj)); chegaradan pastini belgilaydi."""
    print("\n== %s ==" % title)
    print("  %-10s %-14s %-14s" % ("", "dev", "holdout"))
    for label in labels:
        cells = []
        for part in ("dev", "holdout"):
            count, total = results[part][label]
            cells.append("%d/%d" % (count, total))
        print("  %-10s %-14s %-14s" % (label, cells[0], cells[1]))


def test_golden_find():
    """find kalit so'rovi: topildi, 1-o'rin, top-3 (dev va holdout)."""
    results, misses, failed = {}, [], []
    for part in ("dev", "holdout"):
        rows_ = [r for r in golden(GOLDEN_FIND) if r["toplam"] == part]
        ranks = []
        for row in rows_:
            hits, _ = run_find(row["text"], full=False)
            rank = first_rank(hits, row["accept"])
            ranks.append(rank)
            if part == "dev" and rank != 1:
                misses.append((row["id"], row["text"], rank or "-"))
        n = len(rows_)
        counts = {"topildi": sum(r is not None for r in ranks),
                  "1-o'rin": sum(r == 1 for r in ranks),
                  "top-3": sum(r is not None and r <= 3 for r in ranks)}
        results[part] = {k: (v, n) for k, v in counts.items()}
        failed += ["find %s %s" % (part, f) for f in check_floors("find", part, counts)]
    print_table("E1. Oltin to'plam: find kalit so'rovi",
                ("topildi", "1-o'rin", "top-3"), results)
    return failed, misses


def test_golden_hook():
    """suggest_sections: 1-o'rin, top-3, topildi, aniqlik, jim."""
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import suggest_sections
    results, misses, failed = {}, [], []
    for part in ("dev", "holdout"):
        rows_ = [r for r in golden(GOLDEN_PROMPTS) if r["toplam"] == part]
        topical = [r for r in rows_ if r["accept"] is not None]
        silent = [r for r in rows_ if r["accept"] is None]
        counts = collections.Counter()
        given = 0
        for row in rows_:
            hits = [(h[0], h[1]) for h in suggest_sections.suggest(row["text"])]
            if row["accept"] is None:
                counts["jim"] += not hits
                if part == "dev" and hits:
                    misses.append((row["id"], row["text"][:50], "shovqin %d" % len(hits)))
                continue
            rank = first_rank(hits, row["accept"])
            counts["1-o'rin"] += rank == 1
            counts["top-3"] += rank is not None and rank <= 3
            counts["topildi"] += rank is not None
            counts["aniqlik"] += sum(h in row["accept"] for h in hits)
            given += len(hits)
            if part == "dev" and rank != 1:
                misses.append((row["id"], row["text"][:50].replace("\n", " | "),
                               rank or ("jim" if not hits else "-")))
        n = len(topical)
        results[part] = {"1-o'rin": (counts["1-o'rin"], n),
                         "top-3": (counts["top-3"], n),
                         "topildi": (counts["topildi"], n),
                         "aniqlik": (counts["aniqlik"], given),
                         "jim": (counts["jim"], len(silent))}
        failed += ["hook %s %s" % (part, f) for f in check_floors("hook", part, counts)]
    print_table("E2. Oltin to'plam: hook (suggest_sections)",
                ("1-o'rin", "top-3", "topildi", "aniqlik", "jim"), results)
    print("  aniqlik: to'g'ri taklif / jami taklif (mavzuli promptlarda)")
    return failed, misses


def test_golden():
    failed_f, miss_f = test_golden_find()
    failed_h, miss_h = test_golden_hook()
    for label, misses in (("E1 dev", miss_f), ("E2 dev", miss_h)):
        if misses:
            print("\n  %s da 1-o'rinda emas (%d ta):" % (label, len(misses)))
            for rid, text, rank in misses:
                print("    %-5s %-52s %s" % (rid, text, rank))
    for item in failed_f + failed_h:
        print("  CHEGARADAN PAST: %s" % item)
    return not (failed_f + failed_h)


def main():
    # Topilmagan atama ro'yxati Windows quvuridagi kod sahifasida yo'q belgi
    # bilan yiqilmasin.
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    only_golden = "--oltin" in args
    args = [a for a in args if a != "--oltin"]
    sample_size = int(args[0]) if args else DEFAULT_SAMPLE
    if not os.path.exists(SECTIONS):
        build = os.path.join(ROOT, "tools", "build_index.py")
        subprocess.run([sys.executable, build], cwd=ROOT, check=True)

    if only_golden:
        return 0 if test_golden() else 1

    ok_a, miss_a = test_aliases(sample_size)
    ok_b, miss_b = test_identifiers(sample_size)
    ok_c = test_ranking()
    ok_d = test_rule_ranking()
    ok_e = test_golden()

    for label, misses in (("A", miss_a), ("B", miss_b)):
        if misses:
            print("\n  %s da topilmagan (%d ta), birinchi 5:" % (label, len(misses)))
            for item in misses[:5]:
                print("    %s -> %s %s" % item)

    if ok_a and ok_b and ok_c and ok_d and ok_e:
        print("\nBeshala sinov ham joyida.")
        return 0
    print("\nChegaradan pastga tushdi, yuqoriga qarang.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
