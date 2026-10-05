#!/usr/bin/env python3
"""parse_test_output.py uchun sinovlar.

    python3 tools/test_parse_test_output.py

Ikki format sinaladi (Maven va Gradle), chunki stack qatorlari va
xulosa satri ularda boshqacha yoziladi. Gradle modul prefiksi qo'yadi
("at app//shop.Foo.bar"), Maven qo'ymaydi.

maven_fail.txt va gradle_fail.txt sun'iy, regexga yaqin shaklda. Real
chiqish shakllari testdata/test_output/ da: Surefire 3 (batafsil blok va
Results ro'yxati bitta yiqilishni ikki marta aytadi), parametrli test,
Gradle JUnit 5 standart (SHORT) va to'liq formati, Maven va Gradle
kompilyatsiya xatosi, Spring context yiqilishi, AssertJ va Hamcrest.
Ularsiz asbob real chiqishda yiqilib, sinovda o'tib turardi.

CI jurnali (`gh run view --log` va GitHub Actions xom logi) har qator
boshiga vaqt qo'yadi. Uning uchun alohida fayl yo'q: real fixture har
qatoriga prefiks qo'shib olinadi, natija prefikssiz bilan bir xil bo'lishi
kerak.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "parse_test_output.py")
DATA = os.path.join(HERE, "testdata")

CLEAN = "[INFO] Tests run: 12, Failures: 0, Errors: 0, Skipped: 0\n[INFO] BUILD SUCCESS\n"
SF3 = os.path.join("test_output", "surefire3_fail.txt")
SPRING = os.path.join("test_output", "surefire3_spring.txt")
G5_SHORT = os.path.join("test_output", "gradle_junit5_short.txt")
G5_FULL = os.path.join("test_output", "gradle_junit5_full.txt")
G5_LIB = os.path.join("test_output", "gradle_junit5_library.txt")
MVN_COMPILE = os.path.join("test_output", "maven_compile.txt")
GRADLE_COMPILE = os.path.join("test_output", "gradle_compile.txt")
ASSERTJ = os.path.join("test_output", "assertj_hamcrest.txt")
RESULTS = os.path.join("test_output", "results_only.txt")

CASES = [
    ("maven: xulosa", "maven_fail.txt", "Tests: 24, yiqildi: 3"),
    ("maven: kutilgan qiymat", "maven_fail.txt", "kutilgan: 201"),
    ("maven: olingan qiymat", "maven_fail.txt", "olingan : 500"),
    ("maven: loyiha qatori", "maven_fail.txt",
     "OrderControllerTest.createsOrder(OrderControllerTest.java:58)"),
    ("maven: NPE xabari", "maven_fail.txt", "Cannot invoke"),
    ("gradle: xulosa", "gradle_fail.txt", "Tests: 2, yiqildi: 2"),
    ("gradle: modul prefiksi tashlandi", "gradle_fail.txt",
     "MoneyTest.addsAmounts(MoneyTest.java:24)"),
    ("gradle: ishlab chiqarish kodi", "gradle_fail.txt",
     "Money.<init>(Money.java:17)"),
    ("gradle: istisno turi", "gradle_fail.txt", "IllegalArgumentException"),
    ("surefire 3: xulosa", SF3, "Tests: 11, yiqildi: 2, xato: 1"),
    ("surefire 3: Results ikki marta sanalmaydi", SF3,
     "Noyob sabab: 3 ta (jami 3 ta yiqilish)"),
    ("surefire 3: parametrli 2-chaqiriq alohida", SF3, "Price.of(Price.java:40)"),
    ("spring: asl sabab", SPRING, "asl sabab: NoSuchBeanDefinitionException"),
    ("spring: loyiha qatori Hibernate emas", SPRING,
     "kod     : OrderController.lines(OrderController.java:41)"),
    ("spring: ikki yiqilish", SPRING, "Noyob sabab: 2 ta (jami 2 ta yiqilish)"),
    ("gradle 5 short: xulosa", G5_SHORT, "Tests: 12, yiqildi: 4"),
    ("gradle 5 short: hammasi tanildi", G5_SHORT, "jami 4 ta yiqilish"),
    ("gradle 5 short: () li nom", G5_SHORT, "MoneyTest.addsAmounts"),
    ("gradle 5 short: test qatori", G5_SHORT, "kod     : MoneyTest.java:24"),
    ("gradle 5 short: Mockito istisnosi", G5_SHORT, "WantedButNotInvoked"),
    ("gradle 5 short: asl sabab", G5_SHORT, "asl sabab: ConnectException"),
    ("gradle 5 full: kutilgan qiymat", G5_FULL, "kutilgan: 10.00"),
    ("gradle 5 full: loyiha qatori", G5_FULL, "MoneyTest.addsAmounts(MoneyTest.java:24)"),
    # Paketsiz Gradle sarlavhasi: prefiks test sinfi kadridan, Guava emas.
    ("gradle 5 full: kutubxona qatori kod emas", G5_LIB,
     "kod     : OrderService.place(OrderService.java:42)"),
    ("maven compile: soni takrorsiz", MVN_COMPILE, "Kompilyatsiya xatosi: 2 ta"),
    ("maven compile: xabar", MVN_COMPILE, "cannot find symbol"),
    ("maven compile: symbol", MVN_COMPILE, "symbol  : method lines()"),
    ("maven compile: fayl va qator", MVN_COMPILE, "kod     : OrderController.java:41"),
    ("gradle compile: soni", GRADLE_COMPILE, "Kompilyatsiya xatosi: 1 ta"),
    ("gradle compile: fayl va qator", GRADLE_COMPILE, "kod     : OrderController.java:41"),
    ("assertj: kutilgan", ASSERTJ, 'kutilgan: "Alice"'),
    ("assertj: olingan", ASSERTJ, 'olingan : "Bob"'),
    ("hamcrest: kutilgan", ASSERTJ, "kutilgan: is <90>"),
    ("hamcrest: olingan", ASSERTJ, "olingan : was <100>"),
    ("assertj Expecting: kutilgan", ASSERTJ, 'kutilgan: to contain ["ADMIN"]'),
    ("assertj Expecting: olingan", ASSERTJ, 'olingan : ["USER"]'),
    ("faqat Results: sabablar qo'shilmaydi", RESULTS,
     "Noyob sabab: 3 ta (jami 3 ta yiqilish)"),
    ("faqat Results: qavssiz son", RESULTS, "olingan : 100"),
]

# Chiqishda bo'lmasligi kerak: framework stack qatorlari va soxta natija.
ABSENT = [
    ("maven_fail.txt", "org.junit"),
    ("maven_fail.txt", "jdk.internal"),
    ("maven_fail.txt", "AssertionFailureBuilder"),
    ("gradle_fail.txt", "org.junit"),
    ("gradle_fail.txt", "app//"),
    (SF3, "yana"),
    (SPRING, "AbstractPersistentCollection"),
    (SPRING, "CollectionSerializer"),
    (G5_SHORT, "Yiqilgan test topilmadi"),
    (G5_FULL, "Yiqilgan test topilmadi"),
    (MVN_COMPILE, "Yiqilgan test topilmadi"),
    (GRADLE_COMPILE, "Legacy.java"),        # ogohlantirish xato emas
]

# (nom, fayl yoki None, matn yoki None, kutilgan kod, chiqishda bo'lishi kerak)
EXIT_CODES = [
    ("yiqilish bo'lsa 1", "maven_fail.txt", None, 1, ""),
    ("toza bo'lsa 0", None, CLEAN, 0, "Yiqilgan test topilmadi"),
    ("surefire 3", SF3, None, 1, ""),
    ("gradle JUnit 5 short", G5_SHORT, None, 1, ""),
    ("gradle JUnit 5 full", G5_FULL, None, 1, ""),
    ("maven kompilyatsiya", MVN_COMPILE, None, 1, ""),
    ("gradle kompilyatsiya", GRADLE_COMPILE, None, 1, ""),
    ("xulosada yiqilish, nom yo'q", None, "3 tests completed, 1 failed\n", 1,
     "format tanilmadi"),
    ("BUILD FAILURE, test yo'q", None,
     "[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0\n[INFO] BUILD FAILURE\n"
     "[ERROR] Failed to execute goal org.jacoco:jacoco-maven-plugin:0.8.11:check "
     "(check) on project shop: Coverage checks have not been met.\n", 1,
     "Build yiqilgan"),
    ("ogohlantirishli yashil build", None,
     "Foo.java:14: warning: [deprecation] Date(int,int,int) has been deprecated\n"
     "BUILD SUCCESSFUL in 3s\n", 0, "Yiqilgan test topilmadi"),
    ("bo'sh kirish", None, "", 0, "Yiqilgan test topilmadi"),
]

# (nom, fayl yoki None, matn, qator prefiksi, kutilgan kod, chiqishda bo'lishi kerak).
# Xom log (job va step ustunlarisiz) birinchi qatori BOM bilan boshlanadi.
STAMP = "2026-10-05T10:11:12.1234567Z "
CI_LOGS = [
    ("gh run view --log: surefire 3", SF3, None, "build\tRun tests\t" + STAMP, 1,
     "Noyob sabab: 3 ta (jami 3 ta yiqilish)"),
    ("xom log: gradle 5 short", G5_SHORT, None, STAMP, 1,
     "Noyob sabab: 4 ta (jami 4 ta yiqilish)"),
    ("xom log: toza build", None, CLEAN, STAMP, 0, "Yiqilgan test topilmadi"),
]


def ci_log(fixture, text, prefix):
    """Har qatoriga CI prefiksi qo'yilgan nusxa."""
    if fixture:
        with open(os.path.join(DATA, fixture), encoding="utf-8") as handle:
            text = handle.read()
    bom = "" if "\t" in prefix else "\ufeff"
    return bom + "\n".join(prefix + line for line in text.split("\n"))


def run(path=None, text=None):
    args = [sys.executable, TOOL] + ([path] if path else [])
    proc = subprocess.run(args, input=text, capture_output=True,
                          text=True, cwd=ROOT)
    return proc.returncode, proc.stdout


def main():
    fixtures = ({f for _, f, _ in CASES} | {f for f, _ in ABSENT}
                | {c[1] for c in EXIT_CODES if c[1]} | {c[1] for c in CI_LOGS if c[1]})
    missing = [f for f in fixtures if not os.path.exists(os.path.join(DATA, f))]
    if missing:
        print("sinov ma'lumoti yo'q: %s" % ", ".join(sorted(missing)))
        return 1

    failures = 0
    cache = {}

    def output(fixture):
        if fixture not in cache:
            cache[fixture] = run(os.path.join(DATA, fixture))
        return cache[fixture]

    print("== Chiqishda bo'lishi kerak ==")
    for name, fixture, needle in CASES:
        ok = needle in output(fixture)[1]
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))

    print("\n== Chiqishda bo'lmasligi kerak ==")
    for fixture, needle in ABSENT:
        ok = needle not in output(fixture)[1]
        failures += not ok
        print("%-4s %-36s %s" % ("OK" if ok else "XATO", fixture, needle))

    print("\n== mvn -q (INFO qatorlarisiz) ==")
    with open(os.path.join(DATA, SF3), encoding="utf-8") as handle:
        quiet = "".join(l for l in handle if not l.startswith("[INFO]"))
    ok = "jami 3 ta yiqilish" in run(text=quiet)[1]
    failures += not ok
    print("%-4s surefire 3 -q: jami 3 ta yiqilish" % ("OK" if ok else "XATO"))

    print("\n== Chiqish kodi ==")
    for label, fixture, text, want, needle in EXIT_CODES:
        got, out = output(fixture) if fixture else run(text=text)
        ok = got == want and needle in out
        failures += not ok
        print("%-4s %-30s kutilgan=%d olingan=%d" % ("OK" if ok else "XATO", label, want, got))

    print("\n== CI vaqt prefiksi ==")
    for label, fixture, text, prefix, want, needle in CI_LOGS:
        got, out = run(text=ci_log(fixture, text, prefix))
        ok = got == want and needle in out and STAMP.strip() not in out
        failures += not ok
        print("%-4s %-30s kutilgan=%d olingan=%d" % ("OK" if ok else "XATO", label, want, got))

    total = len(CASES) + len(ABSENT) + 1 + len(EXIT_CODES) + len(CI_LOGS)
    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
