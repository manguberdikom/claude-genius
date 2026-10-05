#!/usr/bin/env python3
"""doc.sh find ning aniqligini o'lchaydi.

    python3 tools/eval_find.py [namuna_soni]

Nega kerak: qidiruv ishlayotgani "topdi" degani emas. Kerakli bo'lim
yuzinchi qatorda chiqsa, u amalda topilmagan bilan barobar. Shuning uchun
topilish emas, O'RIN o'lchanadi. Hujjat o'zgarganda yoki find mantig'i
tahrirlanganda qayta ishga tushiriladi: pasayish shu yerda ko'rinadi.

Uch sinov:
  A. Taxallus bo'yicha - inglizcha nomni so'raydi. Oson yo'l, aliases.tsv
     ni tekshiradi: taxallus yo'lining smoke testi.
  B. Matn ichidagi atama bo'yicha - bo'lim TANASIDAN kamyob atama olinadi
     va `find -f` bilan so'raladi. Real foydalanuvchi sarlavhani emas,
     atamani yozadi, shuning uchun asosiy o'lchov shu. 1-o'rin va top-3
     faqat ma'lumot uchun: namuna shovqini (seed'lar orasida 1-o'rin
     47-61%) reyting ta'siridan katta, ularga chegara qo'yilsa kod
     o'zgarmasa ham qizil berardi.
  C. Reyting - belgilangan so'rovlarda `find -f` chiqishidagi "(N marta)"
     sonlari kamayib borishi kerak. Determinik: saralash olib tashlansa
     yoki buzilsa A va B yashil qolardi, bu sinov esa yiqiladi.

B uchun so'rov tanlash muhim: `kerak` yoki `spring` kabi korpusda mingdan
ortiq uchraydigan so'z real so'rov emas va natijani buzadi, shuning uchun
atama korpusda 20 martadan kam uchrashi shart.
"""

import collections
import os
import random
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(ROOT, "tools", "doc.sh")
SECTIONS = os.path.join(ROOT, "index", "sections.tsv")
ALIASES = os.path.join(ROOT, "index", "aliases.tsv")

DEFAULT_SAMPLE = 120
TOP_N = 60                 # find dan shuncha natija so'raladi
MAX_CORPUS_FREQ = 20       # bundan ko'p uchraydigan atama so'rov sifatida yaroqsiz
IDENT_RE = re.compile(r"`([A-Za-z_][A-Za-z0-9_.]{4,40})`")
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.]*")

# Pastki chegaralar, foizda. Nega 100 emas: so'rovlar korpusdan TASODIFIY
# olinadi, shuning uchun ba'zida `author` kabi umumiy so'z tushadi va u
# o'nlab bo'limda uchraydi. Bitta shunday so'rov tufayli har safar
# "yiqildi" deb chiqadigan o'lchov e'tibordan qoladi, ya'ni umuman
# o'lchamagan bilan barobar. Chegaralar bugungi o'lchovdan sal pastda
# turadi: haqiqiy pasayish ilinadi, bitta qaysar so'rov esa yo'q.
FLOORS = {
    "A": {"topildi": 99, "top-3 ": 98},
    "B": {"topildi": 97, "top-10": 95},
}

random.seed(7)

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
    args = [DOC, "find", "-n", str(TOP_N)] + (["-f"] if full else []) + [query]
    start = time.perf_counter()
    proc = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
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
    found = [r for r in ranks if r is not None]
    times = sorted(times)
    failed = []
    print("\n== %s (%d ta so'rov) ==" % (name, total))
    for label, count in (
        ("topildi", len(found)),
        ("1-o'rin", sum(1 for r in found if r == 1)),
        ("top-3 ", sum(1 for r in found if r <= 3)),
        ("top-10", sum(1 for r in found if r <= 10)),
    ):
        pct = 100 * count / total if total else 0
        floor = floors.get(label)
        mark = ""
        if floor is not None:
            if pct + 0.5 < floor:
                mark = "  CHEGARADAN PAST (kamida %d%%)" % floor
                failed.append(label.strip())
            else:
                mark = "  chegara %d%%" % floor
        print("  %-8s %3d/%d  (%3.0f%%)%s" % (label, count, total, pct, mark))
    if times:
        print("  vaqt     median %.0f ms, p95 %.0f ms, max %.0f ms"
              % (1000 * times[len(times) // 2],
                 1000 * times[int(0.95 * (len(times) - 1))],
                 1000 * times[-1]))
    return not failed


def section_bodies():
    """Har bo'lim uchun tanasidagi backtick ichidagi atamalar."""
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
            out.append((row["doc"], row["section"], idents))
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


def test_aliases(sample_size):
    pool = [r for r in rows(ALIASES) if r["kind"] == "section"]
    sample = random.sample(pool, min(sample_size, len(pool)))
    ranks, times, misses = [], [], []
    for row in sample:
        hits, elapsed = run_find(row["alias"], full=False)
        rank = rank_of(hits, (row["doc"], row["ref"]))
        ranks.append(rank)
        times.append(elapsed)
        if rank is None:
            misses.append((row["alias"], row["doc"], row["ref"]))
    return report("A. Taxallus bo'yicha", ranks, times, len(sample),
                  FLOORS["A"]), misses


def test_identifiers(sample_size):
    sections = section_bodies()
    corpus = corpus_token_freq()
    per_section = collections.Counter()
    for _, _, idents in sections:
        for ident in idents:
            per_section[ident] += 1

    usable = []
    for doc, section, idents in sections:
        good = sorted(i for i in idents
                      if 1 <= per_section[i] <= 3
                      and corpus[i.lower()] <= MAX_CORPUS_FREQ)
        if good:
            usable.append((doc, section, good))

    sample = random.sample(usable, min(sample_size, len(usable)))
    ranks, times, misses = [], [], []
    for doc, section, idents in sample:
        query = random.choice(idents)
        hits, elapsed = run_find(query, full=True)
        rank = rank_of(hits, (doc, section))
        ranks.append(rank)
        times.append(elapsed)
        if rank is None:
            misses.append((query, doc, section))
    print("\n  %d bo'limdan %d tasida yaroqli atama bor"
          % (len(sections), len(usable)))
    return report("B. Matn ichidagi atama bo'yicha", ranks, times,
                  len(sample), FLOORS["B"]), misses


def test_ranking():
    """find -f: ko'p uchragan bo'lim yuqorida turadimi."""
    print("\n== C. find -f reytingi (%d ta so'rov) ==" % len(RANK_QUERIES))
    ok, varied = True, False
    for query in RANK_QUERIES:
        proc = subprocess.run([DOC, "find", "-f", "-n", str(TOP_N), query],
                              capture_output=True, text=True, cwd=ROOT)
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


def main():
    sample_size = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SAMPLE
    if not os.path.exists(SECTIONS):
        build = os.path.join(ROOT, "tools", "build_index.py")
        subprocess.run([sys.executable, build], cwd=ROOT, check=True)

    ok_a, miss_a = test_aliases(sample_size)
    ok_b, miss_b = test_identifiers(sample_size)
    ok_c = test_ranking()

    for label, misses in (("A", miss_a), ("B", miss_b)):
        if misses:
            print("\n  %s da topilmagan (%d ta), birinchi 5:" % (label, len(misses)))
            for item in misses[:5]:
                print("    %s -> %s %s" % item)

    if ok_a and ok_b and ok_c:
        print("\nUchala sinov ham joyida.")
        return 0
    print("\nChegaradan pastga tushdi, yuqoriga qarang.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
