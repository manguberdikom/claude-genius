#!/usr/bin/env python3
"""run_tests.py uchun sinovlar.

    python3 tools/test_run_tests.py

Asbobning ikki va'dasi bor va ikkalasi ham sinaladi. Birinchisi: ko'p
modulli loyihada buyruq modulga bog'langan bo'ladi, chunki modulsiz
`--tests X` (Gradle) va `-Dtest=X` (Maven) X yo'q modulda yiqiladi va
aktyor shundan keyin to'liq suite ga qaytardi. Ikkinchisi: tanlash
o'zgarishga ta'sir qilgan testni o'tkazib yubormaydi, shu jumladan
o'zgargan sinfni tilga olmaydigan, lekin uni ishlatgan sinfning testini.

Haqiqiy Gradle va Maven yurmaydi: CI da ular bo'lmasligi mumkin va
sinov daqiqalar emas, soniyalar olishi kerak. Yurgizish yo'li soxta
runner bilan sinaladi (GENIUS_TEST_RUNNER), u Gradle chiqishiga
o'xshash log yozadi.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "run_tests.py")
sys.path.insert(0, HERE)
import run_tests  # noqa: E402

TEMP = tempfile.mkdtemp(prefix="run_tests_")

TEST = """package %(pkg)s;
import org.junit.jupiter.api.Test;
%(ann)sclass %(name)s%(ext)s {
    %(body)s
    @Test void works() { }
}
"""


def java(pkg, name, body="", ann="", ext=""):
    return TEST % {"pkg": pkg, "name": name, "body": body, "ann": ann, "ext": ext}


def main_class(pkg, name, body=""):
    return "package %s;\npublic class %s { %s }\n" % (pkg, name, body)


def tree(name, files):
    root = os.path.join(TEMP, name)
    shutil.rmtree(root, ignore_errors=True)
    for path, text in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as handle:
            handle.write(text)
    return root


def git(root, *args):
    subprocess.run(["git", "-C", root] + list(args), capture_output=True, check=True)


def commit(root):
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")


def gradle_shop():
    """orders va billing; billing orders ni ishlatadi."""
    return {
        "settings.gradle": "rootProject.name = 'shop'\ninclude 'orders',\n        'billing'\n",
        "build.gradle": "subprojects { apply plugin: 'java' }\n",
        "orders/src/main/java/shop/orders/OrderService.java":
            main_class("shop.orders", "OrderService", "public int one() { return 1; }"),
        "orders/src/test/java/shop/orders/OrderServiceTest.java":
            java("shop.orders", "OrderServiceTest"),
        "orders/src/test/java/shop/orders/OrderRepositoryIT.java":
            java("shop.orders", "OrderRepositoryIT", ann="@DataJpaTest\n"),
        "orders/src/test/java/shop/orders/OrderApiTest.java":
            java("shop.orders", "OrderApiTest", ann="@SpringBootTest\n"),
        "billing/src/main/java/shop/billing/Invoice.java":
            main_class("shop.billing", "Invoice",
                       "int total() { return new shop.orders.OrderService().one(); }"),
        "billing/src/test/java/shop/billing/InvoiceTest.java":
            java("shop.billing", "InvoiceTest"),
        "billing/src/test/java/shop/billing/UnrelatedTest.java":
            java("shop.billing", "UnrelatedTest"),
    }


def plan_for(root, changed, deleted=()):
    project = run_tests.Project(root, runner=["./gradlew"])
    return project, run_tests.select(project, changed, deleted)


def chosen(plan):
    return {fqn for bucket in plan.targets.values() for fqn in bucket}


# -- sozlama va modul ----------------------------------------------------------

def case_settings_groovy_va_kotlin(_):
    groovy = run_tests.parse_settings(
        "include 'a', 'b:c'\ninclude(\n  ':d',\n  ':e'\n)\n// include 'x'\n"
        "project(':e').projectDir = file('modules/e')\n")
    kotlin = run_tests.parse_settings('include(":api", ":core:domain")\n')
    return (groovy == {":a": "a", ":b:c": "b/c", ":d": "d", ":e": "modules/e"}
            and kotlin == {":api": "api", ":core:domain": "core/domain"})


def case_modul_yoli_gradle(_):
    root = tree("modul", gradle_shop())
    project = run_tests.Project(root, runner=["./gradlew"])
    return (project.module_of("orders/src/main/java/shop/orders/OrderService.java") == "orders"
            and project.module_of("README.md") == ""
            and project.gradle_path("orders") == ":orders"
            and project.gradle_path("") == "")


# -- tanlash -------------------------------------------------------------------

def case_nomi_mos_va_bir_qadam(_):
    root = tree("bir_qadam", gradle_shop())
    _, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    picked = chosen(plan)
    # InvoiceTest OrderService ni tilga olmaydi: u Invoice orqali (bir qadam).
    return ("shop.orders.OrderServiceTest" in picked
            and "shop.billing.InvoiceTest" in picked
            and "shop.billing.UnrelatedTest" not in picked
            and plan.targets[("billing", "test")]["shop.billing.InvoiceTest"][0] == "hop")


def case_buyruq_modulga_bogliq(_):
    root = tree("buyruq", gradle_shop())
    project, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    argv = run_tests.commands(project, plan)[0][0]
    text = " ".join(argv)
    return (":orders:test --tests shop.orders.OrderServiceTest" in text
            and ":billing:test --tests shop.billing.InvoiceTest" in text
            and "--continue" in argv
            and not {"clean", "--rerun-tasks", "--no-daemon", "test"} & set(argv))


def case_ozgargan_test_yolgiz(_):
    root = tree("faqat_test", gradle_shop())
    _, plan = plan_for(root, ["billing/src/test/java/shop/billing/UnrelatedTest.java"])
    return chosen(plan) == {"shop.billing.UnrelatedTest"}


def case_ochirilgan_sinf(_):
    files = gradle_shop()
    files["orders/src/test/java/shop/orders/LegacyTest.java"] = java(
        "shop.orders", "LegacyTest", body="Object x = new LegacyPricing();")
    root = tree("ochirilgan", files)
    _, plan = plan_for(root, [], ["orders/src/main/java/shop/orders/LegacyPricing.java"])
    return "shop.orders.LegacyTest" in chosen(plan)


def case_sozlama_spring_testlari(_):
    root = tree("sozlama", gradle_shop())
    _, plan = plan_for(root, ["orders/src/main/resources/application.yml"])
    return chosen(plan) == {"shop.orders.OrderApiTest", "shop.orders.OrderRepositoryIT"}


def case_migratsiya_baza_testlari(_):
    root = tree("migratsiya", gradle_shop())
    _, plan = plan_for(root, ["orders/src/main/resources/db/migration/V2__x.sql"])
    picked = chosen(plan)
    return "shop.orders.OrderRepositoryIT" in picked and "shop.orders.OrderServiceTest" not in picked


def case_build_fayli(_):
    root = tree("build_fayli", gradle_shop())
    project, whole_root = plan_for(root, ["build.gradle"])
    _, module = plan_for(root, ["billing/build.gradle"])
    argv = run_tests.commands(project, module)[0][0]
    return (whole_root.everything is not None
            and ("billing", "test") in module.whole
            and ":billing:test" in argv and "--tests" not in argv)


def case_keng_murojaat_butun_vazifa(_):
    files = gradle_shop()
    for i in range(run_tests.WIDE + 1):
        files["orders/src/test/java/shop/orders/Uses%dTest.java" % i] = java(
            "shop.orders", "Uses%dTest" % i, body="Money m;")
    files["orders/src/main/java/shop/orders/Money.java"] = main_class("shop.orders", "Money")
    root = tree("keng", files)
    _, plan = plan_for(root, ["orders/src/main/java/shop/orders/Money.java"])
    return ("orders", "test") in plan.whole and ("orders", "test") not in plan.targets


def case_testga_tegmaydigan_ozgarish(_):
    root = tree("hujjat", gradle_shop())
    _, plan = plan_for(root, ["README.md", "docs/arch.md"])
    return plan.empty()


def case_yordamchi_sinf(_):
    files = gradle_shop()
    files["orders/src/test/java/shop/orders/AbstractIT.java"] = (
        "package shop.orders;\npublic abstract class AbstractIT { }\n")
    files["orders/src/test/java/shop/orders/CartIT.java"] = java(
        "shop.orders", "CartIT", ext=" extends AbstractIT")
    root = tree("yordamchi", files)
    _, plan = plan_for(root, ["orders/src/test/java/shop/orders/AbstractIT.java"])
    return chosen(plan) == {"shop.orders.CartIT"}


def case_build_chiqishi_ozgarish_emas(_):
    out = run_tests.is_output
    return (out("orders/build/reports/x.html") and out(".gradle/8/file.bin")
            and out("target/surefire-reports/x.xml")
            and not out("orders/src/main/java/shop/bin/Tool.java")
            and not out("README.md"))


# -- Maven ---------------------------------------------------------------------

POM = """<project><modelVersion>4.0.0</modelVersion><artifactId>%s</artifactId>
%s</project>"""


def maven_shop(extra_plugins=""):
    return {
        "pom.xml": POM % ("shop", "<modules><module>orders</module></modules>"
                          "<build><plugins><plugin><artifactId>maven-failsafe-plugin"
                          "</artifactId></plugin>%s</plugins></build>" % extra_plugins),
        "orders/pom.xml": POM % ("orders", ""),
        "orders/src/main/java/shop/orders/OrderService.java":
            main_class("shop.orders", "OrderService"),
        "orders/src/test/java/shop/orders/OrderServiceTest.java":
            java("shop.orders", "OrderServiceTest"),
        "orders/src/test/java/shop/orders/OrderServiceIT.java":
            java("shop.orders", "OrderServiceIT"),
    }


def case_maven_it_failsafe_ga(_):
    root = tree("maven", maven_shop())
    project = run_tests.Project(root, runner=["mvn"])
    plan = run_tests.select(project, ["orders/src/main/java/shop/orders/OrderService.java"])
    argv = run_tests.commands(project, plan)[-1][0]
    return (project.tool == "maven"
            and argv[:5] == ["mvn", "-B", "-fae", "-pl", "orders"]
            and "-am" in argv and "verify" in argv
            and "-Dtest=shop.orders.OrderServiceTest" in argv
            and "-Dit.test=shop.orders.OrderServiceIT" in argv
            and "-Dsurefire.failIfNoSpecifiedTests=false" in argv
            and "-Dfailsafe.failIfNoSpecifiedTests=false" in argv)


def case_maven_faqat_it(_):
    root = tree("maven_it", maven_shop())
    project = run_tests.Project(root, runner=["mvn"])
    plan = run_tests.select(project, ["orders/src/test/java/shop/orders/OrderServiceIT.java"])
    argv = run_tests.commands(project, plan)[-1][0]
    # Unit test tanlanmagan: -Dtest bo'sh qolsa surefire HAMMASINI yurgizardi.
    return "-Dtest=%s" % run_tests.SENTINEL in argv


def case_maven_spring_javaformat(_):
    plugin = "<plugin><artifactId>spring-javaformat-maven-plugin</artifactId></plugin>"
    root = tree("maven_format", maven_shop(plugin))
    project = run_tests.Project(root, runner=["mvn"])
    plan = run_tests.select(project, ["orders/src/main/java/shop/orders/OrderService.java"])
    cmds = run_tests.commands(project, plan)
    return cmds[0][0][-1] == "spring-javaformat:apply" and cmds[-1][1] == "maqsadli"


# -- git va yurgizish ------------------------------------------------------------

FAKE = r'''
import sys, time
args = sys.argv[1:]
mode = open(%r).read().strip()
if mode == "sekin":
    time.sleep(30)
print("$ " + " ".join(args))
if mode == "yiqil":
    print("> Task :orders:test FAILED")
    print("")
    print("OrderServiceTest > works() FAILED")
    print("    org.opentest4j.AssertionFailedError at OrderServiceTest.java:5")
    print("")
    print("2 tests completed, 1 failed")
    print("BUILD FAILED in 3s")
    sys.exit(1)
print("BUILD SUCCESSFUL in 2s")
'''


def fake_runner(mode):
    flag = os.path.join(TEMP, "fake_mode.txt")
    with open(flag, "w") as handle:
        handle.write(mode)
    script = os.path.join(TEMP, "fake_gradle.py")
    with open(script, "w") as handle:
        handle.write(FAKE % flag)
    return json.dumps([sys.executable, script])


def run_cli(root, *args, mode="yashil"):
    env = dict(os.environ, GENIUS_TEST_RUNNER=fake_runner(mode))
    proc = subprocess.run([sys.executable, TOOL] + list(args), cwd=root,
                          capture_output=True, text=True, encoding="utf-8", env=env)
    return proc.returncode, proc.stdout + proc.stderr


def git_shop(name):
    root = tree(name, gradle_shop())
    commit(root)
    path = os.path.join(root, "orders/src/main/java/shop/orders/OrderService.java")
    with open(path, "a") as handle:
        handle.write("// o'zgarish\n")
    return root


def case_diff_git_dan(_):
    root = git_shop("diff")
    code, out = run_cli(root, "--diff")
    return code == 0 and "shop.orders.OrderServiceTest" in out and "--yurgiz" in out


def case_yurgiz_yashil(_):
    root = git_shop("yashil")
    log = os.path.join(TEMP, "yashil.log")
    code, out = run_cli(root, "--diff", "--yurgiz", "--log", log)
    with open(log, encoding="utf-8") as handle:
        written = handle.read()
    return code == 0 and "yashil" in out and ":orders:test" in written


def case_yurgiz_yiqildi(_):
    root = git_shop("yiqildi")
    code, out = run_cli(root, "--diff", "--yurgiz", "--log", os.path.join(TEMP, "y.log"),
                        mode="yiqil")
    return code == 1 and "yiqildi" in out and "OrderServiceTest" in out


def case_vaqt_tugadi(_):
    root = git_shop("vaqt")
    code, out = run_cli(root, "--diff", "--yurgiz", "--vaqt", "2",
                        "--log", os.path.join(TEMP, "v.log"), mode="sekin")
    return code == 3 and "vaqt tugadi" in out


def case_tasir_yoq(_):
    root = tree("tasir_yoq", gradle_shop())
    commit(root)
    with open(os.path.join(root, "README.md"), "w") as handle:
        handle.write("x\n")
    code, out = run_cli(root, "--diff", "--yurgiz")
    return code == 0 and "Ta'sirlangan test yo'q" in out


def case_hammasi(_):
    root = tree("hammasi", gradle_shop())
    commit(root)
    code, out = run_cli(root, "--hammasi")
    return code == 0 and "to'liq suite" in out and "--tests" not in out


def case_modul(_):
    root = tree("modul_rejim", gradle_shop())
    commit(root)
    code, out = run_cli(root, "--modul", "billing")
    bad, _ = run_cli(root, "--modul", "yoq")
    return (code == 0 and ":billing:test" in out and "--tests" not in out
            and ":orders:test" not in out and bad == 2)


def case_symlink_orqali_yol(_):
    """Ildizga boshqa nom bilan yetib kelgan yo'l (POSIX da symlink,
    Windows da qisqa 8.3 nom) modulini yo'qotmasin."""
    root = tree("symlink", gradle_shop())
    commit(root)
    link = os.path.join(TEMP, "symlink_havola")
    try:
        os.symlink(root, link, target_is_directory=True)
    except (OSError, NotImplementedError, AttributeError):
        return True        # symlink yo'q (Windows): case_modul shu yo'lni sinaydi
    code, out = run_cli(root, "--modul", os.path.join(link, "billing"))
    fcode, fout = run_cli(root, os.path.join(
        link, "orders", "src", "main", "java", "shop", "orders", "OrderService.java"))
    return (code == 0 and ":billing:test" in out
            and fcode == 0 and "shop.orders.OrderServiceTest" in fout)


def case_navbat_qulfi(_):
    root = tree("navbat", gradle_shop())
    with run_tests.queue_lock(root):
        inside = True
    with run_tests.queue_lock(root):      # qayta olinadi: oldingisi yechilgan
        again = True
    return inside and again


# -- tashxis -------------------------------------------------------------------

def case_tashxis(_):
    files = gradle_shop()
    files["gradle.properties"] = "org.gradle.daemon=false\n"
    files["build.gradle"] += "test { forkEvery = 1 }\n"
    files["orders/src/test/java/shop/orders/SlowIT.java"] = java(
        "shop.orders", "SlowIT", ann="@DirtiesContext\n",
        body="@org.testcontainers.junit.jupiter.Container\n"
             "    PostgreSQLContainer<?> db = new PostgreSQLContainer<>(\"pg\");\n"
             "    void w() throws Exception { Thread.sleep(5); }")
    files["orders/build/test-results/test/TEST-shop.orders.SlowIT.xml"] = (
        '<testsuite name="shop.orders.SlowIT" tests="1" time="41.5"/>')
    root = tree("tashxis", files)
    project = run_tests.Project(root, runner=["./gradlew"])
    titles = " | ".join("%s %s" % (f[0], f[1]) for f in run_tests.diagnose(project))
    slow = run_tests.slowest_reports(root)
    return ("yuqori Gradle daemon" in titles and "yuqori forkEvery" in titles
            and "@DirtiesContext" in titles and "yuqori @Container instance" in titles
            and "Thread.sleep" in titles
            and slow and slow[0] == ("shop.orders.SlowIT", 41.5))


def case_tashxis_static_konteyner_toza(_):
    files = gradle_shop()
    files["orders/src/test/java/shop/orders/GoodIT.java"] = java(
        "shop.orders", "GoodIT",
        body="@Container\n    static PostgreSQLContainer<?> db = new PostgreSQLContainer<>(\"pg\");")
    root = tree("static", files)
    project = run_tests.Project(root, runner=["./gradlew"])
    return not any("instance" in f[1] for f in run_tests.diagnose(project))


CASES = [
    ("settings.gradle: groovy, kotlin, projectDir", case_settings_groovy_va_kotlin),
    ("Gradle modul yo'li", case_modul_yoli_gradle),
    ("nomi mos va bir qadam narida", case_nomi_mos_va_bir_qadam),
    ("buyruq modulga bog'langan, clean yo'q", case_buyruq_modulga_bogliq),
    ("o'zgargan test yolg'iz yuradi", case_ozgargan_test_yolgiz),
    ("o'chirilgan sinfga murojaat", case_ochirilgan_sinf),
    ("sozlama: Spring testlari", case_sozlama_spring_testlari),
    ("migratsiya: baza testlari", case_migratsiya_baza_testlari),
    ("build fayli: ildiz va modul", case_build_fayli),
    ("keng murojaat butun vazifaga", case_keng_murojaat_butun_vazifa),
    ("testga tegmaydigan o'zgarish", case_testga_tegmaydigan_ozgarish),
    ("abstrakt yordamchi sinf", case_yordamchi_sinf),
    ("build chiqishi o'zgarish emas", case_build_chiqishi_ozgarish_emas),
    ("Maven: IT failsafe ga, -pl -am", case_maven_it_failsafe_ga),
    ("Maven: faqat IT, -Dtest bo'sh emas", case_maven_faqat_it),
    ("Maven: spring-javaformat oldin", case_maven_spring_javaformat),
    ("--diff git dan oladi", case_diff_git_dan),
    ("--yurgiz yashil, log yoziladi", case_yurgiz_yashil),
    ("--yurgiz yiqildi, sabab chiqadi", case_yurgiz_yiqildi),
    ("vaqt tugasa 3", case_vaqt_tugadi),
    ("ta'sir yo'q: yurmaydi", case_tasir_yoq),
    ("--hammasi filtrsiz", case_hammasi),
    ("--modul: butun modul, boshqasi yo'q", case_modul),
    ("symlink yoki qisqa nom orqali yo'l", case_symlink_orqali_yol),
    ("navbat qulfi yechiladi", case_navbat_qulfi),
    ("tashxis: daemon, forkEvery, konteyner, sleep, hisobot", case_tashxis),
    ("tashxis: static konteyner toza", case_tashxis_static_konteyner_toza),
]


def main():
    failures = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(None))
            except Exception as exc:
                ok, name = False, "%s (%s: %s)" % (name, type(exc).__name__, exc)
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", name))
    finally:
        shutil.rmtree(TEMP, ignore_errors=True)
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
