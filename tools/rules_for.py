#!/usr/bin/env python3
"""Tegilayotgan fayllarga qaysi qoidalar tegishli ekanini bir chaqiruvda beradi.

    python3 tools/rules_for.py src/main/java/shop/OrderService.java
    python3 tools/rules_for.py --diff          # git diff dagi fayllar
    python3 tools/rules_for.py --diff --cached

Nega: aktyor ikkinchi marta chaqirilsa, sababi deyarli har doim bitta -
qoidani oldindan bilmagan. Qidirib topish esa har aktyorda boshqacha
chiqadi, shuning uchun arxitektor yozgan narsani reviewer boshqa
mezon bilan tekshiradi va ish ikkinchi aylanaga tushadi.

Bu asbob shu ikkisini bitta manbaga bog'laydi. Arxitektor YOZISHDAN
OLDIN, reviewer esa TEKSHIRISHDA shu buyruqni chaqiradi: kirish bir xil,
chiqish bir xil, kelishmovchilik qolmaydi.

Chiqish uch qism: tegishli boblar, ularning tekshiruv punktlari va
mashina allaqachon topgan muammolar.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CHAPTERS = os.path.join(ROOT, "index", "chapters.tsv")
CHECKLIST = os.path.join(ROOT, "index", "checklist.tsv")
MEMORY = os.path.join(ROOT, "memory")

# Punktlar audit uchun yozilgan: ularning ko'pi butun proyektga tegishli
# ("ro'yxatla", "bir hafta kuzat"). Bitta o'zgarish uchun o'ttiztasi
# shovqin bo'ladi va o'qilmay o'tiladi. Shuning uchun kam olinadi va
# boblar bo'ylab navbatma-navbat: har mavzudan birinchi punktlar.
MAX_ITEMS = 12

# Kod ichidagi belgi -> tegishli boblar. Jadval qo'lda tuzilgan, lekin
# har bob ishga tushishdan oldin indeksda borligi tekshiriladi, shuning
# uchun bob ko'chsa yoki o'chsa, jim xato bo'lmaydi.
# Tartib muhim: aniqroq belgi oldinda, punktlar shu tartibda olinadi.
SIGNALS = [
    ("entity va ORM", r"@Entity\b|@Table\b|@ManyToOne\b|@OneToMany\b|@Column\b",
     [("patterns", "9"), ("architect", "18"), ("sonarqube", "29"),
      ("code-review", "23")]),
    ("tranzaksiya", r"@Transactional\b",
     [("architect", "19"), ("code-review", "19")]),
    ("tashqi chaqiruv", r"\b(?:RestTemplate|WebClient|RestClient|FeignClient)\b",
     [("patterns", "17"), ("code-review", "22")]),
    ("web qatlami", r"@RestController\b|@Controller\b|@(?:Get|Post|Put|Delete|Request)Mapping\b",
     [("patterns", "7"), ("architect", "17"), ("code-review", "20")]),
    ("test", r"@Test\b|@ParameterizedTest\b|\bassertThat\b|\bAssertions\.",
     [("testing", "5"), ("sonarqube", "19"), ("code-review", "35"),
      ("code-review", "34"), ("code-review", "36")]),
    ("xavfsizlik: ruxsat", r"@PreAuthorize\b|SecurityFilterChain|@Secured\b|@RolesAllowed\b",
     [("patterns", "18"), ("code-review", "30"), ("code-review", "28"),
      ("sonarqube", "26")]),
    ("xavfsizlik: SQL", r"createNativeQuery|createQuery|\bStatement\b|@Query\b|jdbcTemplate",
     [("code-review", "29"), ("sonarqube", "26")]),
    ("xavfsizlik: sir va kripto",
     r"\bCipher\.|MessageDigest\.|KeyStore\b|SecretKey|getPassword\(|apiKey|secretKey",
     [("code-review", "32")]),
    ("xavfsizlik: tashqi kirish",
     r"MultipartFile|ObjectInputStream|readObject\(|new\s+URL\(|URI\.create\(",
     [("code-review", "31")]),
    ("keshlash", r"@Cacheable\b|@CacheEvict\b|CacheManager",
     [("patterns", "11"), ("architect", "28")]),
    ("rejalashtirilgan ish", r"@Scheduled\b|JobBuilder|StepBuilder",
     [("patterns", "20")]),
    ("loglash", r"\bLogger\b|@Slf4j\b|\blog\.(?:info|warn|error|debug)\b",
     [("clean-code", "29")]),
    ("servis qatlami", r"@Service\b|@Component\b",
     [("patterns", "8")]),
    # Build fayli: bog'liqlik qo'shish ham kod o'zgarishi, lekin uning
    # qoidalari boshqa bobda va .java faylidan ko'rinmaydi.
    ("bog'liqlik", r"<dependency>|<artifactId>|implementation\s|api\s*[(']|plugins\s*\{",
     [("code-review", "33"), ("sonarqube", "39")]),
]

# Qaysi fayllar ko'riladi. Build fayllari ham: ular kod kabi tekshiruvga
# muhtoj, lekin .java emas.
WATCHED = (".java", "pom.xml", "build.gradle", "build.gradle.kts",
           "settings.gradle", "settings.gradle.kts")

# Har Java fayl uchun, belgisidan qat'i nazar.
ALWAYS = [("clean-code", "2"), ("clean-code", "4"), ("code-review", "8")]


def chapter_titles():
    titles = {}
    if not os.path.exists(CHAPTERS):
        return titles
    with open(CHAPTERS, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 3 and parts[1]:
                titles[(parts[0], parts[1])] = parts[2]
    return titles


def changed_files(args):
    if "--diff" in args:
        cmd = ["git", "diff", "--name-only"]
        if "--cached" in args:
            cmd.append("--cached")
        out = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT).stdout
        candidates = out.split("\n")
    else:
        candidates = [a for a in args if not a.startswith("--")]
    # Faqat kuzatiladigan turlar. Boshqa faylni jim qabul qilish
    # chalg'itadi: javob beriladi, lekin u o'sha faylga tegishli emas.
    return [f.strip() for f in candidates if f.strip().endswith(WATCHED)]


def detect(paths):
    """Fayllardan belgilarni topadi: (belgi, fayl) juftliklari."""
    found = []
    seen = set()
    for path in paths:
        full = path if os.path.isabs(path) else os.path.join(ROOT, path)
        if not os.path.isfile(full):
            continue
        try:
            with open(full, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
        except OSError:
            continue
        for label, pattern, chapters in SIGNALS:
            if re.search(pattern, text) and label not in seen:
                seen.add(label)
                found.append((label, chapters, os.path.basename(path)))
    return found


def checklist_for(wanted):
    """Berilgan boblarning tekshiruv punktlari, bob tartibida."""
    items = {}
    if not os.path.exists(CHECKLIST):
        return items
    with open(CHECKLIST, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 4 and (parts[0], parts[1]) in wanted:
                items.setdefault((parts[0], parts[1]), []).append(parts[3])
    return items


def past_mistakes():
    """Memorydagi feedback yozuvlari: avval nima noto'g'ri ketgan."""
    out = []
    if not os.path.isdir(MEMORY):
        return out
    for dirpath, _, filenames in os.walk(MEMORY):
        for name in sorted(filenames):
            if name.startswith("feedback_") and name.endswith(".md"):
                rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
                first = ""
                with open(os.path.join(dirpath, name), encoding="utf-8") as handle:
                    for line in handle:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            first = line
                            break
                out.append((rel, first[:110]))
    return out


def mechanical(paths):
    """check_code allaqachon topa oladigan muammolar."""
    tool = os.path.join(HERE, "check_code.py")
    out = []
    for path in paths:
        full = path if os.path.isabs(path) else os.path.join(ROOT, path)
        if not os.path.isfile(full) or not full.endswith(".java"):
            continue
        proc = subprocess.run([sys.executable, tool, full],
                              capture_output=True, text=True, cwd=ROOT)
        if proc.returncode == 1:
            out.extend(l for l in proc.stdout.split("\n") if l.startswith("["))
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__.strip().split("\n\n")[1].strip())
        return 2

    paths = changed_files(args)
    if not paths:
        print("Tekshiriladigan fayl berilmadi (.java yoki build fayli).",
              file=sys.stderr)
        return 2

    titles = chapter_titles()
    signals = detect(paths)
    wanted, order = set(), []
    for _, chapters, _ in signals:
        for ch in chapters:
            if ch not in wanted:
                wanted.add(ch)
                order.append(ch)
    if any(p.endswith(".java") for p in paths):
        for ch in ALWAYS:
            if ch not in wanted:
                wanted.add(ch)
                order.append(ch)

    missing = [ch for ch in order if ch not in titles]
    if missing:
        print("OGOHLANTIRISH: jadvaldagi bob indeksda yo'q: %s"
              % ", ".join("%s %s" % c for c in missing), file=sys.stderr)
        order = [ch for ch in order if ch in titles]

    print("# %d fayl, %d belgi\n" % (len(paths), len(signals)))
    for label, chapters, where in signals:
        print("%-22s %-14s -> %s" % (label, where,
                                     ", ".join("%s %s" % c for c in chapters)))
    print()

    print("# Tegishli boblar\n")
    for ch in order:
        print("  %-11s %-4s %s" % (ch[0], ch[1], titles[ch]))

    items = checklist_for(set(order))
    total = sum(len(v) for v in items.values())
    print("\n# Tekshiruv punktlari (%d tadan %d tasi)\n"
          % (total, min(total, MAX_ITEMS)))
    shown = 0
    for round_no in range(MAX_ITEMS):
        progressed = False
        for ch in order:
            bucket = items.get(ch, [])
            if round_no < len(bucket) and shown < MAX_ITEMS:
                print("  - [ ] (%s %s) %s" % (ch[0], ch[1], bucket[round_no]))
                shown += 1
                progressed = True
        if shown >= MAX_ITEMS or not progressed:
            break
    if total > shown:
        print("\n  qolgani: tools/doc.sh checklist <hujjat> <bob>")

    found = mechanical(paths)
    print("\n# Mashina topgani (%d)\n" % len(found))
    for line in found[:MAX_ITEMS]:
        print("  " + line.strip())
    if not found:
        print("  yo'q")

    mistakes = past_mistakes()
    if mistakes:
        print("\n# Avval yo'l qo'yilgan xatolar\n")
        for rel, note in mistakes:
            print("  %s\n      %s" % (rel, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())
