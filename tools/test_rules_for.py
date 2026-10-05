#!/usr/bin/env python3
"""rules_for.py uchun sinovlar.

    python3 tools/test_rules_for.py

Eng muhim sinov birinchisi: SIGNALS jadvalidagi har bir bob indeksda
haqiqatan bormi. Jadval qo'lda yozilgan, boblar esa ko'chishi mumkin.
Mos kelmagan bob jim yo'qoladi va aktyor qoidani ko'rmay qoladi, keyin
reviewer uni topadi va ish ikkinchi aylanaga tushadi. Aynan shuning
oldini olish uchun bu asbob yozilgan.

Sinov umumiy narsaga tegmaydi: holat vaqtinchalik papkada
(GENIUS_STATE_DIR), indekssiz holat esa repo nusxasida sinaladi. Avval
haqiqiy index/ vaqtincha ko'chirilardi va shu oraliqda parallel sessiya,
hook va boshqa agent indekssiz qolardi.
"""

import contextlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# rules_for (u orqali state) import qilinishidan OLDIN: subprocesslar ham
# shu papkani meros oladi.
STATE = tempfile.mkdtemp(prefix="genius-state-")
os.environ["GENIUS_STATE_DIR"] = STATE
sys.path.insert(0, HERE)

import rules_for as R  # noqa: E402
import state  # noqa: E402

# Mutlaq yo'l: R.detect jarayon ichida chaqiriladi va nisbiy yo'lni joriy
# papkaga nisbatan hal qiladi.
DATA = os.path.join(ROOT, "tools", "testdata")
BAD = os.path.join(DATA, "java", "Bad.java")
GOOD = os.path.join(DATA, "java", "Good.java")
ENTITY = os.path.join(DATA, "entities", "Order.java")
INSECURE = os.path.join(DATA, "java", "Insecure.java")
POM = os.path.join(DATA, "java", "pom.xml")
SIG = os.path.join(DATA, "rules_for")


def run(*args, cwd=ROOT):
    proc = subprocess.run([sys.executable, os.path.join(HERE, "rules_for.py")]
                          + list(args), capture_output=True, text=True, cwd=cwd)
    return proc.returncode, proc.stdout, proc.stderr


def routed(out):
    """"# Tegishli boblar" ostidagi qatorlar, keyingi sarlavhagacha.

    Keyingi sarlavhada to'xtash SHART: belgi qatorida ham bob raqami bor
    (`-> code-review 29`) va pastdagi "# Mashina topgani" ham, shuning
    uchun butun chiqishdan qidirish buzuq holatda ham yashil berardi.
    """
    body = out.split("# Tegishli boblar", 1)[-1].split("\n#", 1)[0]
    return [l for l in body.split("\n") if l.startswith("  ") and len(l.split()) >= 4]


def has_chapter(out, doc, num):
    return any(l.split()[:2] == [doc, num] for l in routed(out))


def labels(paths):
    return [l for l, _, _ in R.detect(paths)]


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=sinov", "-c", "user.email=s@s",
                    "-c", "init.defaultBranch=main"] + list(args),
                   capture_output=True, text=True, cwd=cwd, check=True)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def report(rows):
    bad = 0
    for label, ok in rows:
        bad += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", label))
    return bad


def main():
    failures = total = 0
    titles = R.chapter_titles()

    print("== Jadvaldagi boblar indeksda bormi ==")
    referenced = [ch for _, _, chapters in R.SIGNALS for ch in chapters] + R.ALWAYS
    missing = sorted({ch for ch in referenced if ch not in titles})
    unknown = sorted((set(R.NAME_SIGNALS) | set(R.PATH_SIGNALS) | R.BUILD_ONLY)
                     - {l for l, _, _ in R.SIGNALS})
    rows = [
        ("%d ta bob tekshirildi%s" % (len(set(referenced)), "" if not missing
                                      else ", yo'q: " + ", ".join("%s %s" % c for c in missing)),
         not missing),
        # Yo'l jadvallari SIGNALS dagi belgiga tayanadi: noma'lum belgi jim
        # ishlamay qolardi.
        ("yo'l jadvallaridagi belgilar SIGNALS da bor%s"
         % ("" if not unknown else ": " + ", ".join(unknown)), not unknown),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Belgi aniqlash ==")
    # (nom, fayl, bo'lishi kerak belgi, bo'lmasligi kerak belgi)
    cases = [
        ("tranzaksiya", BAD, "tranzaksiya", None),
        ("tashqi chaqiruv", BAD, "tashqi chaqiruv", None),
        ("entity", ENTITY, "entity va ORM", None),
        ("loglash", GOOD, "loglash", None),
        # Xavfsizlik: avval faqat @PreAuthorize belgisi bor edi, shuning
        # uchun SQL injection, sir va fayl yuklash hech qayerga
        # yo'naltirilmasdi. Qamrov o'lchangandan keyin topilgan kamchilik.
        ("SQL injection", INSECURE, "xavfsizlik: SQL", None),
        ("sir va kripto", INSECURE, "xavfsizlik: sir va kripto", None),
        ("tashqi kirish", INSECURE, "xavfsizlik: tashqi kirish", None),
        # Build fayli ham ko'riladi: bog'liqlik qo'shish .java da
        # ko'rinmaydi, lekin uning o'z review bobi bor.
        ("build fayli", POM, "bog'liqlik", None),
        # Oddiy Spring kodi: avval belgisiz yoki noto'g'ri belgi bilan qolardi.
        ("repository", os.path.join(SIG, "OrderRepository.java"),
         "ma'lumotga kirish", "vorislik"),
        ("MapStruct", os.path.join(SIG, "OrderMapper.java"), "mapper", None),
        ("@Value sozlama", os.path.join(SIG, "AppConfig.java"),
         "konfiguratsiya", "Lombok"),
        ("Spring Security", os.path.join(SIG, "WebSecurity.java"),
         "xavfsizlik: ruxsat", None),
        ("hodisa", os.path.join(SIG, "OrderEvents.java"), "hodisa", None),
        ("retry", os.path.join(SIG, "OrderEvents.java"), "chidamlilik", None),
        # Izoh va satr literali belgi emas, ularning orasidagi kod esa belgi.
        ("izohdan keyingi kod", os.path.join(SIG, "Noise.java"), "tranzaksiya", "broker"),
        ("izohdagi SQL", os.path.join(SIG, "Noise.java"), None, "xavfsizlik: SQL"),
        # Migratsiya va sozlama fayllari: matni kichik harfli, ichma-ich.
        ("Flyway sql", os.path.join(SIG, "db", "migration", "V2__add_status.sql"),
         "sxema migratsiyasi", None),
        ("application.yml", os.path.join(SIG, "application.yml"), "sozlama", None),
        ("yml dagi kafka", os.path.join(SIG, "application.yml"), "broker", None),
    ]
    for name, path, want, forbid in cases:
        found = set(labels([path]))
        ok = (want is None or want in found) and (forbid is None or forbid not in found)
        failures += not ok
        total += 1
        print("%-4s %-20s %s" % ("OK" if ok else "XATO", name, os.path.basename(path)))

    print("\n== Chiqish tarkibi ==")
    code, out, _ = run(BAD)
    punkt = re.search(r"# Tekshiruv punktlari \((\d+) tadan (\d+) tasi\)", out)
    rows = [
        ("tegishli boblar bor", "# Tegishli boblar" in out),
        ("punktlar bor", "- [ ] (" in out),
        # Sarlavha regex bilan o'qiladi (eval_skill ham), shakli o'zgarmaydi.
        ("punkt sarlavhasi shakli", bool(punkt)),
        ("mashina topilmasi bor", "[yuqori] Bad.java" in out),
        # Topilma yonida Sonar kaliti va bo'lim turishi shart. Avval
        # bu yerda faqat "[" bilan boshlangan qatorlar olinardi va
        # havola tashlanardi: aktyor muammoni ko'rib, qoidani
        # ko'rmasdi. Skillning birinchi qoidasi aynan buni talab
        # qiladi, shuning uchun sinov ham shu yerda.
        ("topilma Sonar kaliti bilan keladi", "java:S108" in out),
        ("kalit bo'limga ulangan", "java:S108 -> sonarqube" in out),
        ("punkt chegarasi hurmat qilindi",
         out.count("  - [ ] (") <= R.MAX_ITEMS),
        ("navbatma-navbat: bir nechta bobdan",
         len({l.split("(")[1].split(")")[0] for l in out.split("\n")
              if l.startswith("  - [ ] (")}) >= 3),
        ("chiqish kodi 0", code == 0),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Mashina topilmasi to'liq ==")
    # check_code jarayon ichida chaqiriladi: MAX_SHOWN (6) dan ortig'i ham
    # olinadi. Bad.java dagi 6 tasiga Tx.java dagi 3 tasi qo'shiladi.
    tx = os.path.join(DATA, "check_code", "Tx.java")
    found = R.mechanical([BAD, tx])
    rows = [
        ("ikki fayldan 9 ta topilma", len(found) == 9),
        ("har topilma havolasi bilan", all(tail for _, tail, _, _ in found)),
        ("BigDecimal pul bo'limiga", any("java:S2111 -> clean-code 20.1" in t
                                         for _, t, _, _ in found)),
    ]
    # MAX_ITEMS dan ortig'i ham qator va kalit bilan: kesilgan ro'yxatda
    # eski topilma yangi bo'lib ko'rinib, arxitektor tegilmagan qatorni
    # tuzatishga majbur bo'lardi.
    tmp = tempfile.mkdtemp()
    try:
        legacy = os.path.join(tmp, "Legacy.java")
        body = "".join("    void m%d() { try { x(); } catch (Exception e) { } }\n" % i
                       for i in range(15))
        write(legacy, "class Legacy {\n%s}\n" % body)
        _, out_many, _ = run("--no-mark", legacy)
        many = len(R.mechanical([legacy]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rest = out_many.split("qolgani %d ta" % (many - R.MAX_ITEMS), 1)[-1]
    rows += [
        ("%d topilma: qolgani ham ko'rinadi" % many,
         many > R.MAX_ITEMS and "qolgani %d ta" % (many - R.MAX_ITEMS) in out_many),
        ("qolganida fayl, qator va kalit",
         "Legacy.java: " in rest and re.search(r"Legacy\.java: \d+ \S+", rest) is not None),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Test fayli va oddiy Java ==")
    # Test fayli berilsa testing boblari chegaradan tashqarida: avval
    # entity, tranzaksiya va HTTP belgilari MAX_CHAPTERS ni to'ldirib,
    # test-muhandis birorta test bobini olmasdi.
    new_test = os.path.join("src", "test", "java", "x", "OrderTest.java")
    _, out_mix, _ = run("--no-mark", new_test, BAD, ENTITY, INSECURE)
    _, out_mix2, _ = run("--no-mark", BAD, ENTITY, INSECURE, new_test)
    _, out_prod, _ = run("--no-mark", BAD, ENTITY, INSECURE)
    tmp = tempfile.mkdtemp()
    try:
        calc = os.path.join(tmp, "Calc.java")
        write(calc, "class Calc { int f(int[] a) { int s = 0;\n"
                    "  for (int x : a) { while (x > 0) { if (x > 5) { s++; }"
                    " else if (x > 2) { s--; } x--; } }\n  return s; } }\n")
        _, out_calc, _ = run("--no-mark", calc)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rows = [
        ("test fayli bilan testing 5 saqlanadi", has_chapter(out_mix, "testing", "5")),
        ("test fayli oxirida ham", routed(out_mix) == routed(out_mix2)),
        ("test faylisiz chegara o'zgarmaydi",
         len(routed(out_prod)) <= R.MAX_CHAPTERS + len(R.ALWAYS)
         and not has_chapter(out_prod, "testing", "5")),
        ("sikl va shart: Sonar cognitive complexity",
         has_chapter(out_calc, "sonarqube", "15")),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Ko'p fayl: tartibga bog'liq emas ==")
    # Belgilar fayl tartibida yig'ilsa, birinchi faylning umumiy belgilari
    # MAX_CHAPTERS ni egallab, keyingisining xavfsizlik bobini siqib chiqarardi.
    _, out_ab, _ = run(BAD, INSECURE)
    _, out_ba, _ = run(INSECURE, BAD)
    _, out_pom, _ = run(BAD, POM)
    rows = [
        ("detect fayl tartibiga bog'liq emas",
         labels([BAD, INSECURE]) == labels([INSECURE, BAD])),
        ("boblar fayl tartibiga bog'liq emas", routed(out_ab) == routed(out_ba)),
        ("xavfsizlik boblari saqlanadi",
         all(has_chapter(out_ab, d, n) for d, n in (("code-review", "29"),
                                                    ("code-review", "31"),
                                                    ("code-review", "32"),
                                                    ("sonarqube", "26")))),
        ("Java dan keyin build fayli ham", has_chapter(out_pom, "code-review", "33")),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Toza fayl ==")
    code_good, out_good, _ = run(GOOD)
    rows = [("chiqish kodi 0", code_good == 0),
            ("mashina topilmasi yo'q", "# Mashina topgani (0)" in out_good),
            ("baribir boblar beriladi", "# Tegishli boblar" in out_good)]
    failures += report(rows)
    total += len(rows)

    print("\n== --no-mark ==")
    # Belgini faqat yozuvchi qo'yadi. Rejalashtiruvchi yoki reviewer
    # belgilasa, arxitektor rules_for ni chaqirmay yozsa ham check_code
    # uni to'smasdi: darvoza jim o'chardi.
    state.clear()
    code_nm, _, _ = run("--no-mark", GOOD)
    unmarked = not state.was_marked(GOOD)
    run(GOOD)
    rows = [("--no-mark: rc 0", code_nm == 0),
            ("--no-mark belgilamaydi", unmarked),
            ("--no-mark siz belgilaydi", state.was_marked(GOOD))]
    failures += report(rows)
    total += len(rows)

    print("\n== Indeks yo'q: bitta ogohlantirish ==")
    # Indeks yasalmasa har bob "jadvaldagi bob indeksda yo'q" bo'lib
    # chiqardi: jadval aybdordek ko'rinar, haqiqiy sabab yashirinardi.
    saved_titles, saved_argv = R.chapter_titles, sys.argv
    out_buf, err_buf = io.StringIO(), io.StringIO()
    try:
        R.chapter_titles = lambda: {}
        sys.argv = ["rules_for.py", "--no-mark", BAD]
        with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
            code_ni = R.main()
    finally:
        R.chapter_titles, sys.argv = saved_titles, saved_argv
    err_ni = err_buf.getvalue()
    rows = [("rc 0", code_ni == 0),
            ("bitta sabab aytildi", err_ni.count("indeks yo'q va yasab bo'lmadi") == 1),
            ("jadval aybdor qilinmadi", "jadvaldagi bob indeksda yo'q" not in err_ni),
            ("bob ro'yxati bo'sh", routed(out_buf.getvalue()) == [])]
    failures += report(rows)
    total += len(rows)

    print("\n== Boshqa papkadan va --diff ==")
    # Global o'rnatishda skript klonda, ish boshqa proyektda: nisbiy yo'l
    # va git joriy papkadan olinadi. Avval ikkalasi klonga bog'lanardi:
    # 0 belgi, noto'g'ri belgi kaliti va klonning diffi.
    tmp = tempfile.mkdtemp()
    try:
        shutil.copy(BAD, os.path.join(tmp, "A.java"))
        code_rel, out_rel, _ = run("A.java", cwd=tmp)
        new_test = os.path.join("src", "test", "java", "x", "NewThingTest.java")
        _, out_new, _ = run(new_test, cwd=tmp)
        marked = state.was_marked(os.path.join(tmp, "A.java"))
        clone_key = state.was_marked(os.path.join(ROOT, "A.java"))

        repo = os.path.join(tmp, "repo")
        main_dir = os.path.join(repo, "src", "main", "java", "shop")
        # Har faylda boshqa belgi: chiqishdagi belgi qatori qaysi fayl
        # olinganini ko'rsatadi.
        write(os.path.join(main_dir, "Kept.java"), "class Kept {}\n")
        write(os.path.join(main_dir, "Gone.java"), "@Scheduled class Gone {}\n")
        git(repo, "init", "-q")
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", "boshlang'ich")
        write(os.path.join(main_dir, "Kept.java"),
              "class Kept { @Transactional void x() {} }\n")
        os.remove(os.path.join(main_dir, "Gone.java"))
        write(os.path.join(main_dir, "Staged.java"), "@Entity class Staged {}\n")
        git(repo, "add", os.path.join(main_dir, "Staged.java"))
        write(os.path.join(repo, "src", "test", "java", "shop", "ATest.java"),
              "class ATest { @Test void t() {} }\n")
        code_d, out_d, _ = run("--diff", cwd=repo)
        _, out_sub, _ = run("--diff", cwd=os.path.join(repo, "src"))
        _, out_c, _ = run("--diff", "--cached", cwd=repo)

        nogit = os.path.join(tmp, "nogit")
        os.makedirs(nogit)
        code_n, _, err_n = run("--diff", cwd=nogit)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rows = [
        ("nisbiy yo'l: rc 0 va belgi topildi",
         code_rel == 0 and "tranzaksiya" in out_rel),
        ("nisbiy yo'l: mashina topgani to'liq", "# Mashina topgani (6)" in out_rel),
        ("belgi joriy papkadagi faylga qo'yildi", marked and not clone_key),
        # Hali yozilmagan test: belgi yo'ldan olinadi.
        ("yozilmagan test test boblarini oladi",
         has_chapter(out_new, "testing", "5") and "hali yo'q" in out_new),
        ("nomdan belgi: Controller", "web qatlami" in labels(["/yoq/web/XController.java"])),
        ("nomsiz yo'q fayl belgisiz", labels(["/yoq/A.java"]) == []),
        ("--diff: rc 0", code_d == 0),
        ("--diff: commit qilingan va o'zgargan", "Kept.java" in out_d),
        ("--diff: staged yangi fayl", "Staged.java" in out_d),
        ("--diff: untracked yangi fayl", "ATest.java" in out_d),
        ("--diff: o'chirilgan fayl kirmaydi", "Gone.java" not in out_d
         and "# 3 fayl" in out_d),
        ("--diff ichki papkadan ham butun repo", "# 3 fayl" in out_sub),
        ("--diff --cached: faqat staged",
         "Staged.java" in out_c and "ATest.java" not in out_c
         and "Kept.java" not in out_c),
        ("git bo'lmagan papkada --diff: rc 2, traceback yo'q",
         code_n == 2 and "Traceback" not in err_n),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Avval yo'l qo'yilgan xatolar ==")
    # Topic fayl frontmatter bilan boshlanadi: avval har yozuv `---` bo'lib
    # chiqardi. Boshqa proyektning yozuvi esa bu yerda shovqin.
    saved, mem = R.MEMORY, tempfile.mkdtemp()
    try:
        write(os.path.join(mem, "demo", "feedback_sinov.md"),
              "---\ntype: feedback\nmodified: 2026-01-01T00:00:00Z\n---\n\n"
              "# Sinov sarlavhasi\n\nBirinchi gap.\n\n- punkt\n")
        write(os.path.join(mem, "demo", "feedback_yangi.md"),
              "---\ntype: feedback\nmodified: 2026-02-01T00:00:00Z\n---\n\n"
              "# Yangi sarlavha\n\n- **Punkt matni.** Davomi\n  ikkinchi qatorda.\n"
              "- Ikkinchi punkt.\n")
        write(os.path.join(mem, "demo", "MEMORY.md"),
              "# demo\n\n- `feedback_yangi.md` - indeksdagi tavsif\n"
              "  ikki qatorga o'ralgan\n")
        write(os.path.join(mem, "boshqa", "feedback_begona.md"), "# Begona\n\nBegona gap.\n")
        write(os.path.join(mem, "umumiy", "feedback_umumiy.md"), "# Umumiy\n\nUmumiy gap.\n")
        R.MEMORY = mem
        notes = R.past_mistakes(slug="demo")
        _, note_of = zip(*notes) if notes else ((), ())
        files = [os.path.basename(rel) for rel, _ in notes]

        slug_repo = os.path.join(mem, "Shop-Api")
        os.makedirs(os.path.join(mem, "acme__shop-api"))
        os.makedirs(slug_repo)
        git(slug_repo, "init", "-q")
        here = os.getcwd()
        try:
            os.chdir(slug_repo)
            slug_bare = R.project_slug()
            git(slug_repo, "remote", "add", "origin", "git@github.com:acme/Shop-Api.git")
            slug_owner = R.project_slug()
            os.rmdir(os.path.join(mem, "acme__shop-api"))
            slug_remote = R.project_slug()
        finally:
            os.chdir(here)
    finally:
        R.MEMORY = saved
        shutil.rmtree(mem, ignore_errors=True)
    rows = [
        ("frontmatter chiqmaydi", bool(notes)
         and not any(n.startswith("---") or "type:" in n for n in note_of)),
        ("indeks yo'q: sarlavha va birinchi gap",
         "Sinov sarlavhasi: Birinchi gap." in note_of),
        ("indeks bor: sarlavha va o'ralgan tavsif",
         "Yangi sarlavha: indeksdagi tavsif ikki qatorga o'ralgan" in note_of),
        ("boshqa proyekt yozuvi chiqmaydi", "feedback_begona.md" not in files),
        ("proyekt oldin, eng yangisi oldin, keyin umumiy",
         files == ["feedback_yangi.md", "feedback_sinov.md", "feedback_umumiy.md"]),
        ("slug: remote yo'q, papka nomi", slug_bare == "shop-api"),
        ("slug: ikki ega bo'lsa egasi__repo", slug_owner == "acme__shop-api"),
        ("slug: remote dagi repo nomi", slug_remote == "shop-api"),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Indekssiz ishlaydimi ==")
    # Indeks hosila va git ga kirmaydi, ya'ni toza klonda yo'q. Avval
    # rules_for jim turib bob raqamisiz chiqish berardi: topilma bor,
    # havola yo'q, sabab aytilmagan. Endi o'zi yasaydi. Bu sinov shuni
    # qo'riqlaydi, chunki xato ko'rinmaydigan turdan: hech narsa
    # yiqilmaydi, faqat javob kambag'allashadi. Repo nusxasida yuradi:
    # ROOT skript faylidan olinadi, shuning uchun nusxa faqat o'z
    # index/ iga tegadi.
    sandbox = tempfile.mkdtemp(prefix="rules_for_sinov_")
    index_checks = []
    try:
        for name in ("tools", "docs", "memory"):
            shutil.copytree(os.path.join(ROOT, name), os.path.join(sandbox, name),
                            ignore=shutil.ignore_patterns("__pycache__"))
        proc = subprocess.run(
            [sys.executable, os.path.join(sandbox, "tools", "rules_for.py"), BAD],
            capture_output=True, text=True, cwd=sandbox)
        out_i, err_i = proc.stdout, proc.stderr
        # Indekssiz chiqish shakli saqlanadi, faqat ichi bo'shaydi:
        # "# Tegishli boblar" sarlavhasi baribir chiqadi, ostida esa hech
        # narsa bo'lmaydi. Shuning uchun sarlavhani sanash yetarli emas,
        # uning OSTIDAGI qatorlar sanaladi.
        punkt = re.search(r"# Tekshiruv punktlari \((\d+) tadan", out_i)
        index_checks = [
            ("indeks o'zi yasaladi", os.path.isdir(os.path.join(sandbox, "index"))),
            ("boblar sarlavhasi bilan chiqdi", len(routed(out_i)) >= 5),
            ("tekshiruv punktlari topildi",
             bool(punkt) and int(punkt.group(1)) > 0),
            # Ogohlantirish stderr ga chiqadi, shuning uchun aynan
            # stderr tekshiriladi.
            ("ogohlantirish chiqmadi", "indeksda yo'q" not in err_i),
            ("chiqish kodi 0", proc.returncode == 0),
        ]
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)
    failures += report(index_checks)
    total += len(index_checks)

    print("\n== Xato yo'llar ==")
    for label, args, want in (("fayl berilmadi", [], 2),
                              ("ko'rilmaydigan fayl", ["README.md"], 2),
                              ("mavjud bo'lmagan fayl", ["/yoq/A.java"], 0)):
        code_e, _, _ = run(*args)
        ok = code_e == want
        failures += not ok
        total += 1
        print("%-4s %-22s kutilgan=%d olingan=%d"
              % ("OK" if ok else "XATO", label, want, code_e))

    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(STATE, ignore_errors=True)
