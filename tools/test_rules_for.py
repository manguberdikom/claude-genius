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


def run(*args, cwd=ROOT, env=None):
    proc = subprocess.run([sys.executable, os.path.join(HERE, "rules_for.py")]
                          + list(args), capture_output=True, text=True, cwd=cwd,
                          env=env)
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
    # eski topilma yangi bo'lib ko'rinib, dasturchi tegilmagan qatorni
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
    # belgilasa, dasturchi rules_for ni chaqirmay yozsa ham check_code
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
        # tmp ning o'zi git ichida bo'lishi mumkin (uy papkasi repo bo'lsa):
        # git tmp dan yuqoriga qaramasin.
        code_n, _, err_n = run("--diff", cwd=nogit,
                               env=dict(os.environ, GIT_CEILING_DIRECTORIES=tmp))
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
    # Klondan tashqari proyekt memorysi (R0.5): GENIUS_MEMORY_DIR.
    ext = tempfile.mkdtemp(prefix="genius_memory_")
    proj_tmp = tempfile.mkdtemp(prefix="proyekt_")
    saved_env = os.environ.get("GENIUS_MEMORY_DIR")
    os.environ["GENIUS_MEMORY_DIR"] = ext
    here = os.getcwd()
    try:
        os.chdir(ROOT)   # klonning o'zi: proyekt memorysi R.MEMORY da
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

        # Boshqa proyekt: `<egasi>__<repo>` papkasi ham, feedback ham
        # GENIUS_MEMORY_DIR da qidiriladi, klondagi shu nomli papka o'qilmaydi.
        slug_repo = os.path.join(proj_tmp, "Shop-Api")
        os.makedirs(os.path.join(ext, "acme__shop-api"))
        os.makedirs(os.path.join(mem, "acme__shop-api"), exist_ok=True)
        os.makedirs(slug_repo)
        git(slug_repo, "init", "-q")
        os.chdir(slug_repo)
        slug_bare = R.project_slug()
        git(slug_repo, "remote", "add", "origin", "git@github.com:acme/Shop-Api.git")
        slug_owner = R.project_slug()
        os.rmdir(os.path.join(ext, "acme__shop-api"))
        slug_remote = R.project_slug()
        write(os.path.join(ext, "shop-api", "feedback_tashqi.md"),
              "# Tashqi\n\nGENIUS_MEMORY_DIR dagi gap.\n")
        write(os.path.join(mem, "shop-api", "feedback_klonda.md"),
              "# Klonda\n\nKlondagi eski gap.\n")
        outside = [os.path.basename(rel) for rel, _ in R.past_mistakes()]
    finally:
        os.chdir(here)
        R.MEMORY = saved
        if saved_env is None:
            os.environ.pop("GENIUS_MEMORY_DIR", None)
        else:
            os.environ["GENIUS_MEMORY_DIR"] = saved_env
        shutil.rmtree(mem, ignore_errors=True)
        shutil.rmtree(ext, ignore_errors=True)
        shutil.rmtree(proj_tmp, ignore_errors=True)
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
        ("boshqa proyekt: memory GENIUS_MEMORY_DIR dan, klondan emas",
         outside == ["feedback_tashqi.md", "feedback_umumiy.md"]),
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

    print("\n== SIGNALS bo'shliqlari (held-out petclinic) ==")
    # Petclinic da topilgan bo'shliqlar: `extends Repository<Vet, Integer>`,
    # @MappedSuperclass li BaseEntity, FQN annotatsiya va static kesh
    # hech qanday belgi bermasdi.
    tmp = tempfile.mkdtemp()
    try:
        def sig(name, body):
            path = os.path.join(tmp, name)
            write(path, body)
            return set(labels([path]))
        gaps = [
            ("Repository<", "ma'lumotga kirish", sig(
                "VetRepository.java",
                "interface VetRepository extends Repository<Vet, Integer> {}\n")),
            ("@RepositoryDefinition", "ma'lumotga kirish", sig(
                "Vets.java", "@RepositoryDefinition(domainClass = Vet.class)\n"
                             "interface Vets {}\n")),
            ("@MappedSuperclass", "entity va ORM", sig(
                "BaseEntity.java", "@MappedSuperclass\nclass BaseEntity {}\n")),
            ("@Embeddable", "entity va ORM", sig(
                "Address.java", "@Embeddable\nclass Address { String city; }\n")),
            ("@Id", "entity va ORM", sig(
                "Plain.java", "class Plain { @Id Long id; }\n")),
            ("FQN @Transactional", "tranzaksiya", sig(
                "Fqn.java", "class Fqn {\n  @org.springframework.transaction."
                            "annotation.Transactional\n  void x() {}\n}\n")),
            ("FQN @Entity", "entity va ORM", sig(
                "FqnEntity.java", "@jakarta.persistence.Entity class FqnEntity {}\n")),
            ("static HashMap", "konkurentlik", sig(
                "Cache.java", "class Cache {\n  private static final Map<String, Long> "
                              "SEEN = new HashMap<>();\n}\n")),
            ("static SimpleDateFormat", "konkurentlik", sig(
                "Fmt.java", "class Fmt {\n  static SimpleDateFormat F = "
                            "new SimpleDateFormat(\"yyyy\");\n}\n")),
            ("static ArrayList", "konkurentlik", sig(
                "Reg.java", "class Reg { static List<String> ALL = new ArrayList<>(); }\n")),
        ]
        local_map = sig("Local.java", "class Local {\n  static int f() {\n"
                                      "    Map<String, Long> m = new HashMap<>();\n"
                                      "    return m.size();\n  }\n}\n")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rows = [("%s -> %s" % (name, want), want in got) for name, want, got in gaps]
    rows.append(("metod ichidagi HashMap konkurentlik emas",
                 "konkurentlik" not in local_map))
    failures += report(rows)
    total += len(rows)

    print("\n== Kotlin va version catalog ==")
    tmp = tempfile.mkdtemp()
    try:
        repo = os.path.join(tmp, "repo")
        kt = os.path.join(repo, "src", "main", "kotlin", "shop", "OrderService.kt")
        write(kt, "package shop\n\n@Service\nclass OrderService {\n"
                  "  @Transactional\n  fun place() {}\n}\n")
        catalog = os.path.join(repo, "gradle", "libs.versions.toml")
        write(catalog, '[versions]\nspring-boot = "3.3.4"\n\n[libraries]\n'
                       'jackson = { module = "com.fasterxml.jackson.core:jackson-databind",'
                       ' version = "2.17.0" }\n')
        git(repo, "init", "-q")
        git(repo, "add", "-A")
        git(repo, "commit", "-qm", "boshlang'ich")
        code_kt, out_kt, _ = run("--no-mark", kt)
        write(kt, "package shop\n\n@Service\nclass OrderService {\n"
                  "  @Transactional(readOnly = true)\n  fun find() {}\n}\n")
        code_ktd, out_ktd, _ = run("--no-mark", "--diff", cwd=repo)
        git(repo, "checkout", "-q", "--", ".")
        write(catalog, '[versions]\nspring-boot = "3.3.4"\n\n[libraries]\n'
                       'jackson = { module = "com.fasterxml.jackson.core:jackson-databind",'
                       ' version = "2.9.0" }\n')
        code_cat, out_cat, _ = run("--no-mark", "--diff", cwd=repo)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rows = [
        (".kt: rc 0", code_kt == 0),
        (".kt: Kotlin ogohlantirishi", R.KOTLIN_NOTE in out_kt),
        (".kt: @Transactional -> architect 19", has_chapter(out_kt, "architect", "19")),
        (".kt: ALWAYS boblari", has_chapter(out_kt, "clean-code", "2")),
        (".kt diff: rc 0 (2 emas)", code_ktd == 0 and "OrderService.kt" in out_ktd),
        ("nomdan belgi .kt da ham",
         "web qatlami" in labels(["/yoq/web/XController.kt"])),
        ("faqat libs.versions.toml diff: rc 0", code_cat == 0),
        ("catalog: bog'liqlik va code-review 33",
         "bog'liqlik" in out_cat and has_chapter(out_cat, "code-review", "33")),
        ("catalog: Kotlin ogohlantirishi yo'q", R.KOTLIN_NOTE not in out_cat),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Proyekt versiyasi va framework ==")
    tmp = tempfile.mkdtemp()
    try:
        def project(name, files):
            base = os.path.join(tmp, name)
            os.makedirs(os.path.join(base, ".git"))
            for rel, text in files.items():
                write(os.path.join(base, rel), text)
            src = os.path.join(base, "src", "main", "java", "shop", "A.java")
            write(src, "class A { @Autowired Repo r; @Transactional void x() {} }\n")
            return src
        boot27 = project("boot27", {"pom.xml": (
            "<project><parent><groupId>org.springframework.boot</groupId>"
            "<artifactId>spring-boot-starter-parent</artifactId>"
            "<version>2.7.18</version></parent>"
            "<properties><java.version>11</java.version></properties></project>")})
        boot33 = project("boot33", {"pom.xml": (
            "<project><parent><groupId>org.springframework.boot</groupId>"
            "<artifactId>spring-boot-starter-parent</artifactId>"
            "<version>3.3.4</version></parent>"
            "<properties><java.version>21</java.version></properties></project>")})
        prop = project("prop", {"pom.xml": (
            "<project><properties><spring-boot.version>2.6.1</spring-boot.version>"
            "</properties><dependencyManagement><dependencies><dependency>"
            "<artifactId>spring-boot-dependencies</artifactId>"
            "<version>${spring-boot.version}</version></dependency></dependencies>"
            "</dependencyManagement></project>")})
        gradle = project("gradle", {"build.gradle": (
            "plugins {\n  id 'org.springframework.boot' version '2.7.0'\n}\n"
            "java { sourceCompatibility = JavaVersion.VERSION_1_8 }\n")})
        kts = project("kts", {"build.gradle.kts": (
            'plugins {\n  id("org.springframework.boot") version "3.4.1"\n}\n'
            "java { toolchain { languageVersion = JavaLanguageVersion.of(17) } }\n")})
        cat = project("cat", {
            "build.gradle.kts": "plugins { alias(libs.plugins.spring.boot) }\n",
            "gradle/libs.versions.toml": (
                '[versions]\nboot = "3.1.5"\njava = "17"\n\n[plugins]\n'
                'spring-boot = { id = "org.springframework.boot", version.ref = "boot" }\n')})
        modul = project("modul", {
            "pom.xml": ("<project><parent><groupId>org.springframework.boot</groupId>"
                        "<version>2.7.18</version></parent></project>")})
        # Ko'p modulli Maven: versiya ildizdagi ota pom da, modul pom ida yo'q.
        sub = os.path.join(tmp, "modul", "orders", "src", "main", "java", "B.java")
        write(os.path.join(tmp, "modul", "orders", "pom.xml"), "<project/>")
        write(sub, "class B {}\n")
        quarkus = project("quarkus", {"pom.xml": (
            "<project><dependencyManagement><dependencies><dependency>"
            "<groupId>io.quarkus.platform</groupId><artifactId>quarkus-bom</artifactId>"
            "</dependency></dependencies></dependencyManagement></project>")})
        code_old, out_old, _ = run("--no-mark", boot27)
        _, out_new, _ = run("--no-mark", boot33)
        code_q, out_q, _ = run("--no-mark", quarkus)
        prof = {name: R.project_profile([path]) for name, path in (
            ("boot27", boot27), ("boot33", boot33), ("prop", prop), ("gradle", gradle),
            ("kts", kts), ("cat", cat), ("sub", sub), ("quarkus", quarkus))}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    rows = [
        ("Maven parent: 2.7.18, Java 11", prof["boot27"][:2] == ("2.7.18", "11")),
        ("Maven xossa va ${...}: 2.6.1", prof["prop"][0] == "2.6.1"),
        ("Gradle plagin va VERSION_1_8", prof["gradle"][:2] == ("2.7.0", "8")),
        ("kts plagin va toolchain", prof["kts"][:2] == ("3.4.1", "17")),
        ("version catalog: version.ref", prof["cat"][:2] == ("3.1.5", "17")),
        ("modul ota pom dan oladi", prof["sub"][0] == "2.7.18"),
        ("boot27: banner, versiya va architect 16.11",
         code_old == 0 and "ESKI VERSIYA" in out_old and "2.7.18" in out_old
         and "Java 11" in out_old and R.MIGRATION_REF in out_old),
        ("Boot 3.3: banner yo'q", "ESKI VERSIYA" not in out_new),
        ("Quarkus: 'Spring emas' qatori", prof["quarkus"][2] == "Quarkus"
         and "Spring emas (Quarkus)" in out_q and code_q == 0),
        ("Quarkus: spring. va @Autowired punktlari yo'q",
         not any(re.search(R.SPRING_ONLY_RE, l) for l in out_q.split("\n")
                 if l.startswith("  - [ ] ("))),
        ("Spring: profil None", prof["boot33"][2] is None),
    ]
    failures += report(rows)
    total += len(rows)

    print("\n== Punkt doirasi va memory filtri ==")
    import build_index  # noqa: E402
    wanted = {("architect", "19"), ("code-review", "19"), ("clean-code", "2"),
              ("clean-code", "4"), ("code-review", "8"), ("code-review", "22")}
    kept, dropped = R.checklist_for(wanted)
    flat = [i for bucket in kept.values() for i in bucket]
    _, out_bad, _ = run("--no-mark", BAD)
    shown = [l for l in out_bad.split("\n") if l.startswith("  - [ ] (")]
    saved, mem = R.MEMORY, tempfile.mkdtemp()
    try:
        write(os.path.join(mem, "demo", "feedback_hujjat.md"),
              "# Hujjat yig'ish\n\nParallel agentlar kirill harf qo'yadi.\n")
        write(os.path.join(mem, "demo", "feedback_tx.md"),
              "# Tranzaksiya\n\n`@Transactional` ichida HTTP chaqirilmaydi.\n")
        write(os.path.join(mem, "demo", "feedback_fayl.md"),
              "# OrderService\n\nOrderService da narx keshlanmaydi.\n")
        R.MEMORY = mem
        all_notes = [os.path.basename(r) for r, _ in R.past_mistakes(slug="demo")]
        tx_notes = [os.path.basename(r) for r, _ in R.past_mistakes(
            slug="demo", labels={"tranzaksiya"}, names=["Bad.java"])]
        file_notes = [os.path.basename(r) for r, _ in R.past_mistakes(
            slug="demo", labels={"loglash"}, names=["OrderService.java"])]
    finally:
        R.MEMORY = saved
        shutil.rmtree(mem, ignore_errors=True)
    rows = [
        ("checklist.tsv da doira ustuni: loyiha punktlari sanaldi", dropped > 0),
        ("rules_for loyiha punktini olmaydi",
         flat and not any(build_index.SCOPE_RE.search(i) for i in flat)),
        ("chiqishda loyiha punkti yo'q",
         shown and not any(build_index.SCOPE_RE.search(l) for l in shown)),
        ("punkt chegarasi MAX_POINTS", len(shown) <= R.MAX_POINTS),
        ("loyiha punktlari doc.sh ga yo'naltiriladi", "loyiha auditi punktlari" in out_bad),
        ("filtrsiz: hamma feedback", len(all_notes) == 3),
        ("belgi bo'yicha: faqat tranzaksiya yozuvi", tx_notes == ["feedback_tx.md"]),
        ("fayl nomi bo'yicha", file_notes == ["feedback_fayl.md"]),
    ]
    failures += report(rows)
    total += len(rows)

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
