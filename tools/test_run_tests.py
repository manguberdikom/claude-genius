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

Gradle init skriptining haqiqiy xulqi alohida, qo'lda sinaladi (tarmoq
kerak: JUnit va jacoco Maven Central dan):

    python3 tools/test_run_tests.py --gradle [gradle-binar]

U jacoco va coverage tekshiruvi `test` ga bog'langan loyihada maqsadli
yurish yolg'on yiqilmasligini, to'liq suite da coverage saqlanishini,
yangi worktree kompilyatsiyani keshdan olib testni keshdan olmasligini,
yiqilgan test qayta yurishini va remote keshga murojaat yo'qligini
tekshiradi. Gradle versiyasi o'zgarganda shu yurgiziladi.
"""

import json
import os
import _thread
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "run_tests.py")
sys.path.insert(0, HERE)
import run_tests  # noqa: E402

TEMP = tempfile.mkdtemp(prefix="run_tests_")
# Mashinadagi ~/.gradle/gradle.properties (masalan org.gradle.caching) buyruqni
# o'zgartirmasin: sinov har joyda bir xil natija bersin.
os.environ["GRADLE_USER_HOME"] = os.path.join(TEMP, "gradle-home")
for _name in ("GENIUS_GRADLE_INIT", "GENIUS_TEST_FLAGS", "GRADLE_OPTS", "JAVA_OPTS"):
    os.environ.pop(_name, None)

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


_GIT_TEMPLATE = []


def shop_repo(name):
    """gradle_shop() + commit. Repo bir marta yasaladi (init, add, commit
    ~140 ms), keyingilari nusxa (~15 ms). symlinks=True: .git ichidagi
    havola fayl bo'lib ko'chmasin."""
    if not _GIT_TEMPLATE:
        template = tree("_git_shablon", gradle_shop())
        commit(template)
        _GIT_TEMPLATE.append(template)
    root = os.path.join(TEMP, name)
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(_GIT_TEMPLATE[0], root, symlinks=True)
    return root


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


def case_claude_worktree_modul_emas(_):
    files = gradle_shop()
    files.update({".claude/worktrees/genius-x/" + path: text for path, text in gradle_shop().items()})
    root = tree("claude_worktree", files)
    project, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    return (all(not src.rel.startswith(".claude/") for src in project.sources)
            and all(not module.startswith(".claude") for module, _ in plan.targets))


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


def case_migratsiya_papkasini_oqiydigan_unit_test(_):
    files = gradle_shop()
    files["orders/src/test/java/shop/orders/ChangelogLintTest.java"] = java(
        "shop.orders", "ChangelogLintTest",
        body='java.nio.file.Path root = java.nio.file.Path.of("src/main/resources").resolve("db/shop");')
    root = tree("migratsiya_papkasi", files)
    _, plan = plan_for(root, ["orders/src/main/resources/db/shop/2026/V3__y.yaml"])
    picked = chosen(plan)
    return ("shop.orders.ChangelogLintTest" in picked and "shop.orders.OrderRepositoryIT" in picked
            and "shop.orders.OrderServiceTest" not in picked)


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


def both_tools(name, *extra):
    """pom.xml va build.gradle birga, `extra` wrapper fayllari."""
    files = maven_shop()
    files["settings.gradle"] = "rootProject.name = 'shop'\ninclude 'orders'\n"
    files["build.gradle"] = "subprojects { apply plugin: 'java' }\n"
    for wrapper in extra:
        files[wrapper] = "#!/bin/sh\n"
    return tree(name, files)


def case_asbob_wrapper_ustun(_):
    maven = run_tests.Project(both_tools("ikki_mvnw", "mvnw"), runner=["mvn"])
    gradle = run_tests.Project(both_tools("ikki_gradlew", "gradlew"), runner=["gradle"])
    return (maven.tool == "maven" and "wrapper mvnw" in maven.tool_note
            and not maven.tool_error
            and gradle.tool == "gradle" and "wrapper gradlew" in gradle.tool_note)


def case_asbob_noaniq(_):
    both = run_tests.Project(both_tools("ikki_wrapper", "mvnw", "gradlew"), runner=["x"])
    none = run_tests.Project(both_tools("wrappersiz"), runner=["x"])
    return (both.tool is None and "ikkalasida bor" in both.tool_error
            and "--asbob maven|gradle" in both.tool_error
            and none.tool is None and "hech birida yo'q" in none.tool_error)


def case_asbob_tanlov(_):
    root = both_tools("ikki_tanlov")
    with Env(GENIUS_BUILD_TOOL="gradle"):
        env = run_tests.Project(root, runner=["x"])
        flag = run_tests.Project(root, runner=["x"], tool="maven")
    only_gradle = run_tests.Project(tree("faqat_gradle", gradle_shop()), runner=["x"],
                                    tool="maven")
    with Env(GENIUS_BUILD_TOOL="ant"):
        bad = run_tests.Project(root, runner=["x"])
    return (env.tool == "gradle" and "GENIUS_BUILD_TOOL=gradle" in env.tool_note
            and "ikkalasi bor" in env.tool_note
            and flag.tool == "maven" and "--asbob maven" in flag.tool_note
            and only_gradle.tool is None and "pom.xml" in only_gradle.tool_error
            and bad.tool is None and "maven yoki gradle" in bad.tool_error)


def case_asbob_cli(_):
    """Reja qatorida tanlov va sababi; noaniq bo'lsa rc 2."""
    root = both_tools("ikki_cli")
    changed = "orders/src/main/java/shop/orders/OrderService.java"
    bad, bad_out = run_cli(root, changed)
    code, out = run_cli(root, changed, "--asbob", "maven")
    return (bad == 2 and "--asbob" in bad_out
            and code == 0 and "Asbob: maven (--asbob maven; Maven va Gradle ikkalasi bor)" in out
            and "-Dtest=shop.orders.OrderServiceTest" in out)


def case_quarkus_micronaut_sozlama(_):
    """Spring siz JVM: sozlama o'zgarsa ilova testlari, migratsiyada baza testi."""
    files = gradle_shop()
    files["orders/src/test/java/shop/orders/QuarkusApiTest.java"] = java(
        "shop.orders", "QuarkusApiTest", ann="@QuarkusTest\n")
    files["orders/src/test/java/shop/orders/QuarkusFlowIT.java"] = java(
        "shop.orders", "QuarkusFlowIT", ann="@QuarkusIntegrationTest\n")
    files["orders/src/test/java/shop/orders/MicronautApiTest.java"] = java(
        "shop.orders", "MicronautApiTest", ann="@MicronautTest\n")
    root = tree("quarkus", files)
    _, config = plan_for(root, ["orders/src/main/resources/application.properties"])
    _, migration = plan_for(root, ["orders/src/main/resources/db/migration/V2__x.sql"])
    picked = chosen(config)
    return ({"shop.orders.QuarkusApiTest", "shop.orders.QuarkusFlowIT",
             "shop.orders.MicronautApiTest"} <= picked
            and "shop.orders.OrderServiceTest" not in picked
            and "shop.orders.QuarkusApiTest" in chosen(migration))


def case_qayta_yurish_jami(_):
    """Qayta yurish logi faqat yiqilgan sinf: xulosa soni birinchi yurishdan."""
    log = os.path.join(TEMP, "jami.log")
    with open(log, "w", encoding="utf-8") as handle:
        handle.write("[INFO] Tests run: 21, Failures: 1, Errors: 0, Skipped: 0\n")
    summary = "Tests: 7, yiqildi: 1, xato: 0, o'tkazildi: 0\nNoyob sabab: 1 ta"
    merged = run_tests.first_run_totals(log, summary)
    return (merged.startswith("Tests: 21, yiqildi: 1") and "birinchi yurish" in merged
            and merged.endswith("Noyob sabab: 1 ta")
            and run_tests.first_run_totals(os.path.join(TEMP, "yoq.log"), summary) == summary)


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
import os, sys, time
args = sys.argv[1:]
mode = open(%r).read().strip()
calls = %r
with open(calls, "a") as handle:
    handle.write(" ".join(args) + "\n")
count = sum(1 for _ in open(calls))
if mode == "sekin":
    time.sleep(30)
if mode == "nevara":
    # O'zi uxlaydigan nevara ochadi (Windows da `cmd /c gradlew.bat` ostidagi java kabi).
    import subprocess
    grandchild = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    pidfile = os.path.join(os.path.dirname(calls), "nevara.pid")
    with open(pidfile + ".tmp", "w") as handle:
        handle.write(str(grandchild.pid))
    os.replace(pidfile + ".tmp", pidfile)
    time.sleep(30)
print("$ " + " ".join(args))

def report(failures):
    folder = os.path.join("orders", "build", "test-results", "test")
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "TEST-shop.orders.OrderServiceTest.xml"), "w") as handle:
        handle.write('<testsuite name="shop.orders.OrderServiceTest" tests="1" '
                     'failures="%%d" errors="0" time="0.1"/>' %% failures)

if mode == "kompil":
    # Bir modulda test yiqilgan, boshqasida kompilyatsiya xatosi: XML bor,
    # lekin qayta yurish kompilyatsiya xatosini "beqaror" deb yashirardi.
    report(1)
    print("OrderService.java:3: error: cannot find symbol")
    print("BUILD FAILED in 1s")
    sys.exit(1)
warmup = "testClasses" in args or "geniusIsit" in args
if mode in ("beqaror", "beqaror_gate") or (mode == "yiqil" and not warmup):
    failing = mode == "yiqil" or count == 1
    report(1 if failing else 0)
    if not failing:
        print("BUILD SUCCESSFUL in 1s")
        sys.exit(0)
if mode in ("yiqil", "beqaror", "beqaror_gate"):
    print("> Task :orders:test FAILED")
    if mode == "beqaror_gate":
        print("> Task :common:jacocoTestCoverageVerification FAILED")
        print("Execution failed for task ':common:jacocoTestCoverageVerification'.")
    print("Execution failed for task ':orders:test'.")
    print("")
    print("OrderServiceTest > works() FAILED")
    print("    org.opentest4j.AssertionFailedError at OrderServiceTest.java:5")
    print("")
    print("2 tests completed, 1 failed")
    print("BUILD FAILED in 3s")
    sys.exit(1)
print("BUILD SUCCESSFUL in 2s")
'''


CALLS = os.path.join(TEMP, "fake_calls.txt")


def fake_runner(mode):
    flag = os.path.join(TEMP, "fake_mode.txt")
    with open(flag, "w") as handle:
        handle.write(mode)
    if os.path.exists(CALLS):
        os.remove(CALLS)
    script = os.path.join(TEMP, "fake_gradle.py")
    with open(script, "w") as handle:
        handle.write(FAKE % (flag, CALLS))
    return json.dumps([sys.executable, script])


def calls():
    with open(CALLS) as handle:
        return [line.split() for line in handle]


STATE = os.path.join(TEMP, "state")


def run_cli(root, *args, mode="yashil"):
    env = dict(os.environ, GENIUS_TEST_RUNNER=fake_runner(mode), GENIUS_STATE_DIR=STATE)
    proc = subprocess.run([sys.executable, TOOL] + list(args), cwd=root,
                          capture_output=True, text=True, encoding="utf-8", env=env)
    return proc.returncode, proc.stdout + proc.stderr


def git_shop(name):
    root = shop_repo(name)
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
    code, out = run_cli(root, "--diff", "--yurgiz", "--vaqt", "0.3",
                        "--log", os.path.join(TEMP, "v.log"), mode="sekin")
    return code == 3 and "vaqt tugadi" in out


NEVARA = os.path.join(TEMP, "nevara.pid")


class Skip(Exception):
    pass


def skip_on_windows():
    """POSIX avlod yo'li: Windows da taskkill /T yo'li bu yerda sinalmaydi."""
    if os.name == "nt":
        raise Skip("nt")


def read_pid(wait=5.0):
    deadline = time.time() + wait
    while time.time() < deadline:
        if os.path.exists(NEVARA):
            with open(NEVARA) as handle:
                text = handle.read().strip()
            if text:
                return int(text)
        time.sleep(0.05)
    return 0


def gone(pid, wait=2.0):
    """pid 2 s ichida yo'q bo'ladimi (zombi ham yo'q hisoblanadi)."""
    deadline = time.time() + wait
    while time.time() < deadline:
        if not run_tests.pid_alive(pid):
            return True
        time.sleep(0.05)
    return False


def reap(pid):
    if pid:
        try:
            os.kill(pid, 9)
        except OSError:
            pass


def case_vaqt_tugadi_nevara(_):
    # Timeout da faqat bola emas, nevara ham to'xtaydi; chiqish kodi 3 va log saqlanadi.
    skip_on_windows()
    root = git_shop("vaqt_nevara")
    log = os.path.join(TEMP, "vn.log")
    if os.path.exists(NEVARA):
        os.remove(NEVARA)
    code, out = run_cli(root, "--diff", "--yurgiz", "--vaqt", "6", "--log", log, mode="nevara")
    pid = read_pid(1)
    try:
        with open(log, encoding="utf-8") as handle:
            written = handle.read()
        return (code == 3 and "vaqt tugadi" in out and "vaqt tugadi" in written
                and pid > 0 and gone(pid))
    finally:
        reap(pid)


def case_keyboard_interrupt_nevara(_):
    # KeyboardInterrupt da ham daraxt to'xtaydi va istisno yutilmaydi.
    skip_on_windows()
    if os.path.exists(NEVARA):
        os.remove(NEVARA)
    script = ("import os, subprocess, sys, time\n"
              "g = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
              "open(%r, 'w').write(str(g.pid))\n"
              "time.sleep(30)\n" % NEVARA)
    interrupted = False

    def interrupt_when_ready():
        # Qat'iy kutish emas: nevara pid fayli paydo bo'lguncha kutiladi.
        if read_pid(15):
            _thread.interrupt_main()

    timer = threading.Thread(target=interrupt_when_ready, daemon=True)
    timer.start()
    try:
        with open(os.path.join(TEMP, "ki.log"), "w") as out:
            run_tests.run_command([sys.executable, "-c", script], TEMP, out, 60)
    except KeyboardInterrupt:
        interrupted = True
    timer.join(5)
    pid = read_pid(1)
    try:
        return interrupted and pid > 0 and gone(pid)
    finally:
        reap(pid)


def case_sigterm_nevara(_):
    # Asbobning o'ziga SIGTERM: nevara yetim qolmaydi va root_lock bo'shaydi.
    skip_on_windows()
    root = git_shop("sigterm_nevara")
    if os.path.exists(NEVARA):
        os.remove(NEVARA)
    env = dict(os.environ, GENIUS_TEST_RUNNER=fake_runner("nevara"), GENIUS_STATE_DIR=STATE)
    proc = subprocess.Popen([sys.executable, TOOL, "--diff", "--yurgiz",
                             "--log", os.path.join(TEMP, "st.log")], cwd=root, env=env,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pid = read_pid()
    try:
        if not pid:
            return False
        os.kill(proc.pid, signal.SIGTERM)
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            return False
        with open(os.path.join(TEMP, "st.log"), encoding="utf-8") as handle:
            stopped = "[run_tests] to'xtatildi" in handle.read()
        return gone(pid) and stopped and proc.returncode == 128 + signal.SIGTERM
    finally:
        reap(pid)
        if proc.poll() is None:
            proc.kill()


def case_tasir_yoq(_):
    root = shop_repo("tasir_yoq")
    with open(os.path.join(root, "README.md"), "w") as handle:
        handle.write("x\n")
    code, out = run_cli(root, "--diff", "--yurgiz")
    return code == 0 and "Ta'sirlangan test yo'q" in out


def case_hammasi(_):
    root = shop_repo("hammasi")
    code, out = run_cli(root, "--hammasi")
    return code == 0 and "to'liq suite" in out and "--tests" not in out


def case_modul(_):
    root = shop_repo("modul_rejim")
    code, out = run_cli(root, "--modul", "billing")
    bad, _ = run_cli(root, "--modul", "yoq")
    return (code == 0 and ":billing:test" in out and "--tests" not in out
            and ":orders:test" not in out and bad == 2)


def case_symlink_orqali_yol(_):
    """Ildizga boshqa nom bilan yetib kelgan yo'l (POSIX da symlink,
    Windows da qisqa 8.3 nom) modulini yo'qotmasin."""
    root = shop_repo("symlink")
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


def case_symlink_ildiz_log(_):
    """Git siz loyihaga symlink orqali kirilsa ham ildiz va log nomi bitta.

    Windows da TEMP qisqa 8.3 nom bilan keladi (`RUNNER~1`) va shu sinf
    xatosi faqat windows-latest CI da chiqardi. Linux da symlink xuddi
    shu holat: realpath siz project_root havola yo'lini, log_path esa
    boshqa hash berib, --tashxis yozilgan logni topmasdi.
    """
    root = tree("kontekst_havola", gradle_shop())
    link = os.path.join(TEMP, "kontekst_havola_link")
    try:
        os.symlink(root, link, target_is_directory=True)
    except (OSError, NotImplementedError, AttributeError):
        return True        # symlink yo'q (Windows): CI da qisqa nom shuni sinaydi
    real = os.path.realpath(root)
    same_root = (run_tests.project_root(link) == real
                 and run_tests.project_root(os.path.join(link, "orders")) == real)
    same_log = run_tests.log_path(link, True) == run_tests.log_path(real, True)
    log = run_tests.log_path(link, True)
    with open(log, "w", encoding="utf-8") as handle:
        handle.write("Started OrderApiTest in 4.2 seconds (process running for 9.1)\n"
                     "Started CartIT in 3.0 seconds (process running for 12.0)\n")
    try:
        code, out = run_cli(root, "--ildiz", link, "--tashxis")
    finally:
        os.remove(log)
    return same_root and same_log and code == 0 and "2 marta" in out


# U+02BB (o'zbek lotin "ʻ"): git -z siz uni qo'shtirnoq va oktal bilan beradi.
OKINA = "ʻ"


def case_diff_non_ascii_migratsiya(_):
    files = gradle_shop()
    sql = "orders/src/main/resources/db/migration/V2__qo%sshimcha_ustun.sql" % OKINA
    files[sql] = "alter table orders add column x int;\n"
    root = tree("non_ascii_migratsiya", files)
    commit(root)
    with open(os.path.join(root, sql), "a", encoding="utf-8") as handle:
        handle.write("alter table orders add column y int;\n")
    code, out = run_cli(root, "--diff")
    return (code == 0 and "shop.orders.OrderRepositoryIT" in out
            and "shop.orders.OrderServiceTest" not in out)


def case_diff_non_ascii_untracked(_):
    root = shop_repo("non_ascii_untracked")
    name = "Yangi%sTest" % OKINA
    path = os.path.join(root, "orders/src/test/java/shop/orders/%s.java" % name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(java("shop.orders", name))
    code, out = run_cli(root, "--diff")
    return code == 0 and "shop.orders." + name in out and "o'zgargan test" in out


def monorepo(name):
    """Git ildizi tepada, build `backend/` da, yonida `frontend/`."""
    files = {"backend/" + path: text for path, text in gradle_shop().items()}
    files["backend/orders/build.gradle"] = "dependencies { }\n"
    files["frontend/app.js"] = "console.log(1);\n"
    root = tree(name, files)
    commit(root)
    return root


SERVICE = "backend/orders/src/main/java/shop/orders/OrderService.java"


def case_monorepo_diff(_):
    root = monorepo("monorepo_diff")
    with open(os.path.join(root, SERVICE), "a") as handle:
        handle.write("// o'zgarish\n")
    code, out = run_cli(root, "--ildiz", "backend", "--diff")
    git(root, "checkout", "--", SERVICE)
    with open(os.path.join(root, "frontend/app.js"), "a") as handle:
        handle.write("console.log(2);\n")
    fcode, fout = run_cli(root, "--ildiz", "backend", "--diff")
    return (code == 0 and "shop.orders.OrderServiceTest" in out
            and "--ildiz dan tashqarida" not in out
            and fcode == 0 and "Ta'sirlangan test yo'q" in fout
            and "1 fayl --ildiz dan tashqarida, hisobga olinmadi" in fout)


def case_monorepo_ildizsiz(_):
    """--ildiz siz: git ildizida build yo'q, birinchi darajada yagona
    backend/. Submoduldan (o'z build.gradle i bor) ham ildiz backend."""
    root = monorepo("monorepo_ildizsiz")
    with open(os.path.join(root, SERVICE), "a") as handle:
        handle.write("// o'zgarish\n")
    top, tcode = run_cli(root, "--diff")
    sub_code, sub_out = run_cli(os.path.join(root, "backend", "orders"), "--diff")
    return (top == 0 and "shop.orders.OrderServiceTest" in tcode
            and ":orders:test" in tcode
            and sub_code == 0 and ":orders:test" in sub_out
            and "shop.orders.OrderServiceTest" in sub_out)


def case_ildiz_tanlash(_):
    """locate_root: eng yuqori marker, yagona birinchi daraja, noaniqlik."""
    files = {"backend/" + path: text for path, text in gradle_shop().items()}
    files["backend/orders/build.gradle"] = "dependencies { }\n"
    files["frontend/app.js"] = "x\n"
    files["build/pom.xml"] = "<project/>\n"         # chiqish papkasi nomzod emas
    root = os.path.realpath(tree("ildiz_tanlash", files))
    git(root, "init", "-q")
    backend = os.path.join(root, "backend")
    results = [
        run_tests.locate_root(root) == (backend, []),
        run_tests.locate_root(os.path.join(backend, "orders", "src", "main")) == (backend, []),
        run_tests.locate_root(os.path.join(root, "frontend")) == (backend, []),
    ]
    os.makedirs(os.path.join(root, "tools"))
    with open(os.path.join(root, "tools", "pom.xml"), "w") as handle:
        handle.write("<project/>\n")
    results.append(run_tests.locate_root(root) == (root, ["backend", "tools"]))
    # Submodul ichida noaniqlik yo'q: yo'ldagi eng yuqori marker hal qiladi.
    results.append(run_tests.locate_root(os.path.join(backend, "orders")) == (backend, []))
    code, out = run_cli(root, "--diff")
    results.append(code == 2 and "Build ildizlari: backend, tools; --ildiz <papka>" in out)
    # Git ildizida marker bo'lsa avvalgi xulq: ildizning o'zi.
    with open(os.path.join(root, "pom.xml"), "w") as handle:
        handle.write("<project/>\n")
    results.append(run_tests.locate_root(os.path.join(backend, "orders")) == (root, []))
    return all(results)


def case_monorepo_asos(_):
    root = monorepo("monorepo_asos")
    git(root, "branch", "asos")
    with open(os.path.join(root, SERVICE), "a") as handle:
        handle.write("// o'zgarish\n")
    git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qam", "ish")
    code, out = run_cli(root, "--ildiz", "backend", "--asos", "asos")
    return code == 0 and "shop.orders.OrderServiceTest" in out


def case_log_faqat_temp_yoki_loyiha(_):
    """--log ixtiyoriy faylni build chiqishi bilan qayta yozmasin."""
    root = git_shop("log_chegara")
    outside = os.path.join(HERE, "genius-log-sinovi-%d.log" % os.getpid())
    if run_tests.inside(outside, tempfile.gettempdir()):
        return True        # repo temp ichida: tashqi yo'l yo'q
    try:
        code, out = run_cli(root, "--diff", "--yurgiz", "--log", outside)
        written = os.path.exists(outside)
    finally:
        if os.path.exists(outside):
            os.remove(outside)
    inner = os.path.join(root, "ichki.log")
    icode, _ = run_cli(root, "--diff", "--yurgiz", "--log", inner)
    return code == 2 and "--log" in out and not written and icode == 0 and os.path.exists(inner)


def case_asos_bayroq_emas(_):
    """--asos git ga bayroq bo'lib o'tmasin va commit bo'lmasa rc 2."""
    root = git_shop("asos_bayroq")
    target = os.path.join(TEMP, "injected")
    code, out = run_cli(root, "--asos=--output=%s" % target)
    created = [n for n in os.listdir(TEMP) if n.startswith("injected")]
    bad, _ = run_cli(root, "--asos", "yoq-ref")
    good, gout = run_cli(root, "--asos", "HEAD")
    return (code == 2 and not created and bad == 2
            and good == 0 and "shop.orders.OrderServiceTest" in gout)


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


# -- Spring orqali ta'sir -------------------------------------------------------

def spring_shop():
    files = gradle_shop()
    files["orders/src/main/java/shop/orders/SecurityConfig.java"] = (
        "package shop.orders;\n@Configuration\npublic class SecurityConfig { }\n")
    files["orders/src/main/java/shop/orders/Order.java"] = (
        "package shop.orders;\n@Entity\npublic class Order { }\n")
    files["orders/src/test/java/shop/orders/AbstractIT.java"] = (
        "package shop.orders;\n@SpringBootTest\npublic abstract class AbstractIT { }\n")
    files["orders/src/test/java/shop/orders/CartIT.java"] = java(
        "shop.orders", "CartIT", ext=" extends AbstractIT")
    files["billing/src/main/java/shop/billing/BillingConfig.java"] = (
        "package shop.billing;\n@Configuration\npublic class BillingConfig { }\n")
    return files


def case_spring_sozlamasi(_):
    # SecurityConfig hech qaysi testda nomi bilan yo'q, lekin har Spring
    # testining kontekstiga kiradi.
    root = tree("wiring", spring_shop())
    _, plan = plan_for(root, ["orders/src/main/java/shop/orders/SecurityConfig.java"])
    picked = chosen(plan)
    return ({"shop.orders.OrderApiTest", "shop.orders.OrderRepositoryIT",
             "shop.orders.CartIT"} <= picked
            and "shop.orders.OrderServiceTest" not in picked
            and "shop.billing.InvoiceTest" not in picked)


def case_kutubxona_sozlamasi(_):
    # billing da Spring testi yo'q: uning sozlamasi ishlatuvchi modulda.
    root = tree("kutubxona", spring_shop())
    _, plan = plan_for(root, ["billing/src/main/java/shop/billing/BillingConfig.java"])
    return "shop.orders.OrderApiTest" in chosen(plan)


def case_entity_baza_testlari(_):
    root = tree("entity", spring_shop())
    _, plan = plan_for(root, ["orders/src/main/java/shop/orders/Order.java"])
    picked = chosen(plan)
    return ("shop.orders.OrderRepositoryIT" in picked and "shop.orders.CartIT" in picked
            and "shop.orders.OrderServiceTest" not in picked)


def case_sozlama_ota_sinf_orqali(_):
    root = tree("ota_sinf", spring_shop())
    _, plan = plan_for(root, ["orders/src/main/resources/application.yml"])
    return "shop.orders.CartIT" in chosen(plan)


# -- yiqilgan sinf, qayta yurish -------------------------------------------------

def case_xml_dan_yiqilgan(_):
    files = gradle_shop()
    files["orders/build/test-results/test/TEST-shop.orders.OrderServiceTest.xml"] = (
        '<testsuite name="shop.orders.OrderServiceTest" failures="1" errors="0"/>')
    files["orders/build/test-results/test/TEST-shop.orders.OrderApiTest.xml"] = (
        '<testsuite name="shop.orders.OrderApiTest" failures="0" errors="0"/>')
    files["billing/target/surefire-reports/TEST-shop.billing.InvoiceTest.xml"] = (
        '<testsuite name="shop.billing.InvoiceTest" failures="0" errors="2"/>')
    root = tree("xml", files)
    project = run_tests.Project(root, runner=["./gradlew"])
    return run_tests.failed_classes(project, 0) == {
        ("orders", "test"): ["shop.orders.OrderServiceTest"],
        ("billing", "test"): ["shop.billing.InvoiceTest"]}


def case_beqaror_exit_4(_):
    root = git_shop("beqaror")
    code, out = run_cli(root, "--diff", "--yurgiz", "--log", os.path.join(TEMP, "b.log"),
                        mode="beqaror")
    second = calls()[-1]
    return (code == 4 and "beqaror" in out and len(calls()) == 2
            and "shop.orders.OrderServiceTest" in second
            and "shop.billing.InvoiceTest" not in second)


def case_doimiy_yiqilish(_):
    root = git_shop("doimiy")
    code, out = run_cli(root, "--diff", "--yurgiz", "--log", os.path.join(TEMP, "d.log"),
                        mode="yiqil")
    return code == 1 and "qayta yurish:" in out and len(calls()) == 2


def case_kompilyatsiya_qayta_yoq(_):
    root = git_shop("kompil")
    code, out = run_cli(root, "--diff", "--yurgiz", "--log", os.path.join(TEMP, "k.log"),
                        mode="kompil")
    return code == 1 and len(calls()) == 1 and "Kompilyatsiya" in out


def case_qayta_ochiq(_):
    root = git_shop("qayta0")
    code, _ = run_cli(root, "--diff", "--yurgiz", "--qayta", "0",
                      "--log", os.path.join(TEMP, "q.log"), mode="beqaror")
    return code == 1 and len(calls()) == 1


# -- isitish, jurnal, kontekst, bayroqlar ------------------------------------------

def case_isit(_):
    root = git_shop("isit")
    code, out = run_cli(root, "--isit")
    return code == 0 and "Isitish" in out and "geniusIsit" in calls()[0]


def case_jurnal_hisobot(_):
    root = git_shop("jurnal")
    run_cli(root, "--diff", "--yurgiz", "--log", os.path.join(TEMP, "j.log"))
    code, out = run_cli(root, "--hisobot")
    return code == 0 and "maqsadli" in out and "Test yurishlari" in out


def case_kontekst_ishga_tushishi(_):
    root = tree("kontekst", gradle_shop())
    log = run_tests.log_path(os.path.realpath(root), True)
    with open(log, "w", encoding="utf-8") as handle:
        handle.write("Started OrderApiTest in 4.2 seconds (process running for 9.1)\n"
                     "x\nStarted CartIT in 3.0 seconds (process running for 12.0)\n")
    try:
        path, starts = run_tests.context_starts([log])
        code, out = run_cli(root, "--tashxis")
    finally:
        os.remove(log)
    return (starts == [("OrderApiTest", 4.2), ("CartIT", 3.0)]
            and "Spring kontekst ishga tushishi" in out and "2 marta" in out)


def case_maven_jacoco_maqsadlida(_):
    root = tree("maven_jacoco", maven_shop())
    project = run_tests.Project(root, runner=["mvn"])
    plan = run_tests.select(project, ["orders/src/main/java/shop/orders/OrderService.java"])
    target = run_tests.commands(project, plan)[-1][0]
    full = run_tests.commands(project, run_tests.Plan(), everything=True)[-1][0]
    return "-Djacoco.skip=true" in target and "-Djacoco.skip=true" not in full


def case_maven_coverage(_):
    """--coverage: Maven maqsadli yurishda jacoco.skip yo'q, jacoco:report bor."""
    root = tree("maven_coverage", maven_shop())
    project = run_tests.Project(root, runner=["mvn"])
    plan = run_tests.select(project, ["orders/src/main/java/shop/orders/OrderService.java"])
    plain = run_tests.commands(project, plan)[-1][0]
    cov = run_tests.commands(project, plan, coverage=True)[-1][0]
    return ("-Djacoco.skip=true" in plain and "jacoco:report" not in plain
            and "-Djacoco.skip=true" not in cov and "jacoco:report" in cov
            and "-Djacoco.haltOnFailure=false" in cov)


def case_qoshimcha_bayroqlar(_):
    root = tree("bayroq", gradle_shop())
    project, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    old = os.environ.get("GENIUS_TEST_FLAGS")
    os.environ["GENIUS_TEST_FLAGS"] = "--build-cache --offline"
    try:
        argv = run_tests.commands(project, plan)[0][0]
    finally:
        if old is None:
            os.environ.pop("GENIUS_TEST_FLAGS", None)
        else:
            os.environ["GENIUS_TEST_FLAGS"] = old
    return argv[-2:] == ["--build-cache", "--offline"]


class Env:
    """Muhit o'zgaruvchisini vaqtincha qo'yish va qaytarish."""

    def __init__(self, **values):
        self.values, self.old = values, {}

    def __enter__(self):
        for key, value in self.values.items():
            self.old[key] = os.environ.get(key)
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def __exit__(self, *exc):
        for key, value in self.old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


WRAPPER = ("# eski: distributionUrl=https\\://services.gradle.org/distributions/gradle-4.6-all.zip\n"
           "distributionUrl=https\\://services.gradle.org/distributions/gradle-%s-bin.zip\n")


def init_of(argv, root=None):
    """Buyruqdagi init skript matni, yo'q bo'lsa ''. Yo'l loyiha ildiziga nisbiy."""
    if "-I" not in argv:
        return ""
    path = os.path.join(root or os.path.join(TEMP, "gradle_init"), argv[argv.index("-I") + 1])
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def gradle_argv(files, everything=False, version="8.14.3", coverage=False):
    files = dict(files)
    if version:
        files.setdefault("gradle/wrapper/gradle-wrapper.properties", WRAPPER % version)
    root = tree("gradle_init", files)
    project, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    if everything:
        plan = run_tests.Plan()
    return run_tests.commands(project, plan, everything=everything,
                              coverage=coverage)[-1][0]


def case_gradle_init(_):
    # tree() papkani qayta yaratadi: skript matni har chaqiruvdan keyin darhol o'qiladi.
    target = gradle_argv(gradle_shop())
    text = init_of(target)
    full = gradle_argv(gradle_shop(), everything=True)
    full_text = init_of(full)
    path = target[target.index("-I") + 1]
    return ("geniusMaqsadli = true" in text and "geniusKesh = true" in text
            and "--build-cache" in target and target.count("--build-cache") == 1
            and "geniusMaqsadli = false" in full_text and "geniusKesh = true" in full_text
            and "JacocoReportBase" in text and "doNotCacheIf" in text
            and "beforeSettings" in text and "geniusIsit" in text
            # Loyihaning .gradle/ ida, nisbiy: umumiy /tmp da emas.
            and not os.path.isabs(path) and path.startswith(".gradle")
            and init_of(gradle_argv(gradle_shop())) == text)


def case_gradle_coverage(_):
    """--coverage: init da jacoco agenti va hisobot qoladi, chegara tekshiruvi
    o'chadi; qolgan init (cache, XML) o'zgarmaydi. Bayroqsiz eski xulq."""
    files = gradle_shop()
    plain = gradle_argv(files)
    plain_text = init_of(plain)
    cov = gradle_argv(files, coverage=True)
    cov_text = init_of(cov)
    full = gradle_argv(files, everything=True, coverage=True)
    return ("geniusCoverage = false" in plain_text and "geniusCoverage = true" in cov_text
            and "geniusMaqsadli = true" in cov_text and "geniusKesh = true" in cov_text
            and "jacoco != null && !geniusCoverage" in cov_text
            and "JacocoCoverageVerification" in cov_text
            and "jacocoTestReport" in cov_text
            and "--build-cache" in cov and cov[cov.index("-I") + 1] != plain[plain.index("-I") + 1]
            # to'liq suite da jacoco avvaldan qoladi: bayroq init ni o'zgartirmaydi
            and "geniusCoverage = false" in init_of(full))


def case_coverage_hisobot_yoli(_):
    """Hisobot yo'li faqat shu yurishda yozilgan XML dan topiladi."""
    root = tree("coverage_yol", gradle_shop())
    project = run_tests.Project(root, runner=["./gradlew"])
    old = os.path.join(root, "orders", "build", "reports", "jacoco", "test", "jacocoTestReport.xml")
    os.makedirs(os.path.dirname(old), exist_ok=True)
    with open(old, "w", encoding="utf-8") as handle:
        handle.write("<report/>")
    stamp = time.time() - 3600
    os.utime(old, (stamp, stamp))
    before = run_tests.coverage_reports(project, time.time() - 60)
    os.utime(old, None)
    after = run_tests.coverage_reports(project, time.time() - 60)
    return before == [] and after == ["orders/build/reports/jacoco/test/jacocoTestReport.xml"]


def case_describe_coverage(_):
    files = gradle_shop()
    files["gradle/wrapper/gradle-wrapper.properties"] = WRAPPER % "8.14.3"
    root = tree("describe_coverage", files)
    project, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    text = run_tests.describe(project, plan, run_tests.commands(project, plan, coverage=True), False)
    return "Gradle init: jacoco qoladi (--coverage)" in text


def case_gradle_kesh_qarori(_):
    """Loyiha yoki foydalanuvchi cache ni o'zi tanlagan bo'lsa asbob unga tegmaydi."""
    results = []
    for value in ("false", "true", "TRUE"):
        files = gradle_shop()
        files["gradle.properties"] = "org.gradle.caching : %s\n" % value
        argv = gradle_argv(files)
        results.append("--build-cache" not in argv and "geniusKesh = false" in init_of(argv)
                       and "geniusMaqsadli = true" in init_of(argv))
    home = os.environ["GRADLE_USER_HOME"]
    os.makedirs(home, exist_ok=True)
    with open(os.path.join(home, "gradle.properties"), "w") as handle:
        handle.write("org.gradle.caching=false\n")
    try:
        results.append("--build-cache" not in gradle_argv(gradle_shop()))
        # GRADLE_USER_HOME dagi qiymat loyihanikidan ustun (Gradle ham shunday o'qiydi).
        files = gradle_shop()
        files["gradle.properties"] = "org.gradle.caching=true\n"
        results.append(run_tests.gradle_props(tree("ustun", files))["org.gradle.caching"]
                       == "false")
    finally:
        os.remove(os.path.join(home, "gradle.properties"))
    for env in ({"GENIUS_TEST_FLAGS": "--no-build-cache"},
                {"GENIUS_TEST_FLAGS": "-Dorg.gradle.caching=false"},
                {"GRADLE_OPTS": "-Xmx1g -Dorg.gradle.caching=true"},
                {"JAVA_OPTS": "-Dorg.gradle.caching=false"}):
        with Env(**env):
            argv = gradle_argv(gradle_shop())
            results.append("--build-cache" not in argv and "geniusKesh = false" in init_of(argv))
    with Env(GENIUS_TEST_FLAGS="--build-cache"):
        argv = gradle_argv(gradle_shop())
        results.append(argv.count("--build-cache") == 1
                       and "geniusKesh = false" in init_of(argv))
    return all(results)


def case_gradle_init_ochirish(_):
    with Env(GENIUS_GRADLE_INIT="0"):
        off = gradle_argv(gradle_shop())
    old = gradle_argv(gradle_shop(), version="6.0")
    new = gradle_argv(gradle_shop(), version="8.14.3")
    # Versiya noma'lum (wrapper yo'q): init bor, cache esa yo'q.
    unknown = gradle_argv(gradle_shop(), version=None)
    unknown_text = init_of(unknown)
    unknown_version = run_tests.gradle_version(os.path.join(TEMP, "gradle_init"))
    files = gradle_shop()
    files["gradle.properties"] = "org.gradle.unsafe.isolated-projects=true\n"
    isolated = gradle_argv(files)
    with Env(GRADLE_OPTS="-Dorg.gradle.isolated-projects=true"):
        isolated_opts = gradle_argv(gradle_shop())
    return ("-I" not in off and "--build-cache" not in off and "-I" not in old
            and "-I" in new and "-I" in unknown and "--build-cache" not in unknown
            and "geniusKesh = false" in unknown_text
            and "-I" not in isolated and "-I" not in isolated_opts
            and unknown_version is None
            and run_tests.gradle_version(tree("v", {"gradle/wrapper/gradle-wrapper.properties":
                                                    WRAPPER % "8.14.3"})) == (8, 14))


def case_properties_sintaksisi(_):
    props = run_tests.properties(
        "# izoh\n! izoh\na=1\nb : 2\nc 3\nd\\:x=4\n"
        "distributionUrl=https\\://h/gradle-9.8.0-bin.zip\n")
    return (props.get("a") == "1" and props.get("b") == "2" and props.get("c") == "3"
            and props.get("distributionUrl") == "https://h/gradle-9.8.0-bin.zip")


def case_isit_hamma_toplam(_):
    files = gradle_shop()
    files["orders/src/integration-test/java/shop/orders/OrderFlowIT.java"] = java(
        "shop.orders", "OrderFlowIT")
    root = tree("isit_toplam", files)
    project = run_tests.Project(root, runner=["./gradlew"])
    argv = run_tests.warmup_commands(project)[0][0]
    with Env(GENIUS_GRADLE_INIT="0"):
        off = run_tests.warmup_commands(project)[0][0]
    # Papka nomidan vazifa taxmin qilinmaydi: geniusIsit Gradle source set laridan.
    return (argv[1] == "geniusIsit" and "integration-testClasses" not in argv
            and "geniusMaqsadli = false" in init_of(argv, root)
            and off[1] == "testClasses" and "-I" not in off)


def case_describe_init(_):
    files = gradle_shop()
    files["gradle/wrapper/gradle-wrapper.properties"] = WRAPPER % "8.14.3"
    root = tree("describe_init", files)
    project, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    text = run_tests.describe(project, plan, run_tests.commands(project, plan), False)
    files["gradle.properties"] = "org.gradle.caching=true\n"
    root = tree("describe_init_loyiha", files)
    project, plan = plan_for(root, ["orders/src/main/java/shop/orders/OrderService.java"])
    own = run_tests.describe(project, plan, run_tests.commands(project, plan), False)
    return ("Gradle init: jacoco va HTML hisobot o'chiq, build cache faqat kompilyatsiya"
            in text and "build cache loyihaniki" in own)


def case_composite_build(_):
    files = gradle_shop()
    files["settings.gradle"] = ("pluginManagement { includeBuild('build-logic') }\n"
                                + files["settings.gradle"] + "includeBuild 'libs/money'\n")
    files["libs/money/settings.gradle"] = "rootProject.name = 'money'\ninclude 'core'\n"
    files["libs/money/core/src/main/java/money/Money.java"] = main_class("money", "Money")
    files["libs/money/core/src/test/java/money/MoneyTest.java"] = java("money", "MoneyTest")
    files["build-logic/src/functionalTest/java/bl/PluginTest.java"] = java("bl", "PluginTest")
    root = tree("composite", files)
    project, plan = plan_for(root, ["libs/money/core/src/main/java/money/Money.java"])
    argv = run_tests.commands(project, plan)[-1][0]
    full = run_tests.commands(project, run_tests.Plan(), everything=True)[-1][0]
    rerun = run_tests.commands(project, run_tests.rerun_plan(
        {("libs/money/core", "test"): ["money.MoneyTest"]}))[-1][0]
    return (argv[1:4] == [":money:core:test", "--tests", "money.MoneyTest"]
            and ":test" not in argv
            and ":build-logic:functionalTest" in full and ":money:core:test" in full
            and "functionalTest" not in full and rerun[1] == ":money:core:test")


def case_boshqa_yiqilish(_):
    """Coverage tekshiruvi ham yiqilgan, yiqilgan test esa qayta o'tdi:
    natija beqaror (4) emas, yiqildi (1)."""
    root = git_shop("boshqa_yiqilish")
    code, out = run_cli(root, "--diff", "--yurgiz", mode="beqaror_gate")
    pom = "<project><parent><artifactId>shop</artifactId></parent><artifactId>%s</artifactId></project>"
    maven_root = tree("boshqa_maven", {"pom.xml": pom % "shop", "a/pom.xml": pom % "a",
                                       "b/pom.xml": pom % "b", "c/pom.xml": pom % "c"})
    project = run_tests.Project(maven_root, runner=["mvn"])
    log = os.path.join(TEMP, "maven.log")
    with open(log, "w") as handle:
        handle.write(
            "[INFO] a .................................................. FAILURE [  2.1 s]\n"
            "[INFO] b .................................................. FAILURE [  1.0 s]\n"
            "[INFO] c .................................................. SKIPPED\n"
            "[ERROR] Failed to execute goal io.spring.javaformat:spring-javaformat-maven-plugin:"
            "0.0.43:apply (default-cli) on project a: x\n"
            "[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:"
            "3.2.5:test (default-test) on project a: There are test failures.\n"
            "[ERROR] Failed to execute goal org.apache.maven.plugins:maven-surefire-plugin:"
            "3.2.5:test (default-test) on project b: The forked VM terminated\n"
            "[ERROR] Failed to execute goal org.jacoco:jacoco-maven-plugin:"
            "0.8.11:check (check) on project a: Coverage checks have not been met.\n")
    maven = run_tests.other_failures(project, log, {("a", "test"): ["a.FlakyTest"]})
    # a dagi surefire yiqilishini yiqilgan sinf izohlaydi; b dagi qulash,
    # a dagi coverage va SKIPPED c izohlanmaydi; formatlash kechiriladi.
    return (code == 1 and "Beqaror" in out and "Boshqa yiqilish" in out
            and ":common:jacocoTestCoverageVerification" in out
            and maven == ["c: SKIPPED",
                          "org.apache.maven.plugins:maven-surefire-plugin (b)",
                          "org.jacoco:jacoco-maven-plugin (a)"])


def case_composite_nomi_va_dinamik(_):
    """Gradle included build ni papka nomi bilan chaqiradi; ildiz include lari
    dinamik bo'lsa modul build fayli bo'yicha topiladi."""
    files = gradle_shop()
    files["settings.gradle.kts"] = (
        "pluginManagement { includeBuild(\"build-logic\") }\n"
        "listOf(\"orders\", \"billing\").forEach { include(it) }\n"
        "includeBuild(\"libs/money\")\n"
        "includeBuild(\"libs/legacy\") { name = \"old\" }\n")
    del files["settings.gradle"]
    files["orders/build.gradle.kts"] = "plugins { java }\n"
    files["billing/build.gradle.kts"] = "plugins { java }\n"
    files["libs/money/settings.gradle"] = ("// rootProject.name = 'eski'\n"
                                           "rootProject.name = 'cash'\nincludeBuild '../nested'\n")
    files["libs/money/src/test/java/money/MoneyTest.java"] = java("money", "MoneyTest")
    files["libs/legacy/src/test/java/legacy/LegacyTest.java"] = java("legacy", "LegacyTest")
    files["libs/nested/src/test/java/nested/NTest.java"] = java("nested", "NTest")
    root = tree("composite_nom", files)
    project = run_tests.Project(root, runner=["./gradlew"])
    plan = run_tests.select(project, ["orders/src/main/java/shop/orders/OrderService.java"])
    argv = run_tests.commands(project, plan)[-1][0]
    money = run_tests.commands(project, run_tests.select(
        project, ["libs/money/src/test/java/money/MoneyTest.java"]))[-1][0]
    nested = run_tests.commands(project, run_tests.select(
        project, ["libs/nested/src/test/java/nested/NTest.java"]))[-1][0]
    legacy = run_tests.commands(project, run_tests.select(
        project, ["libs/legacy/src/test/java/legacy/LegacyTest.java"]))[-1][0]
    settings = run_tests.select(project, ["libs/money/settings.gradle"])
    old = gradle_argv(files, version="6.7")
    return (":orders:test" in argv and ":test" not in argv
            and money[1] == ":money:test" and nested[1] == ":nested:test"
            and legacy[1] == ":old:test" and bool(settings.everything)
            and "libs/money" not in run_tests.Project(
                os.path.join(TEMP, "gradle_init"), runner=["./gradlew"]).included
            and old is not None)


def case_soyabon_composite(_):
    """Ildizda o'z testi yo'q, faqat includeBuild: `test` va `geniusIsit`
    selektorlari ildizda yo'q, faqat `:<nom>:...` vazifalari."""
    files = {"settings.gradle": "rootProject.name = 'umbrella'\nincludeBuild 'money'\n",
             "gradle/wrapper/gradle-wrapper.properties": WRAPPER % "8.14.3",
             "money/build.gradle": "apply plugin: 'java'\n",
             "money/src/main/java/money/Money.java": main_class("money", "Money"),
             "money/src/test/java/money/MoneyTest.java": java("money", "MoneyTest")}
    root = tree("soyabon", files)
    project = run_tests.Project(root, runner=["./gradlew"])
    full = run_tests.commands(project, run_tests.Plan(), everything=True)[-1][0]
    warm = run_tests.warmup_commands(project)[0][0]
    return ("test" not in full and ":money:test" in full
            and "geniusIsit" not in warm and ":money:geniusIsit" in warm)


def case_source_set_nomi(_):
    groovy = "sourceSets { integrationTest { java.srcDir 'src/integration-test/java' } }\n"
    nested = ("sourceSets {\n  it {\n    java {\n      srcDirs = ['src/it-tests/java']\n"
              "    }\n  }\n}\n")
    kts = 'val functional by sourceSets.creating { java.srcDir("src/func-test/java") }\n'
    suite = ('testing { suites { register<JvmTestSuite>("e2e") { sources { java {\n'
             '  setSrcDirs(listOf("src/end-to-end/java")) } } } } }\n')
    names = run_tests.source_set_names(groovy + nested + kts + suite)
    files = gradle_shop()
    files["orders/build.gradle"] = groovy
    files["orders/src/integration-test/java/shop/orders/FlowIT.java"] = java("shop.orders", "FlowIT")
    files["billing/src/contract-test/java/shop/billing/PactTest.java"] = java(
        "shop.billing", "PactTest")
    root = tree("sset_nomi", files)
    project = run_tests.Project(root, runner=["./gradlew"])
    flow = run_tests.commands(project, run_tests.select(
        project, ["orders/src/integration-test/java/shop/orders/FlowIT.java"]))[-1][0]
    pact = run_tests.commands(project, run_tests.select(
        project, ["billing/src/contract-test/java/shop/billing/PactTest.java"]))[-1][0]
    full = run_tests.commands(project, run_tests.Plan(), everything=True)[-1][0]
    return (names == {"integration-test": "integrationTest", "it-tests": "it",
                      "func-test": "functional", "end-to-end": "e2e"}
            and flow[1] == ":orders:integrationTest" and pact[1] == ":billing:contractTest"
            and "integrationTest" in full and "contractTest" in full
            and "integration-test" not in full)


def case_tashxis_gradle(_):
    files = gradle_shop()
    files["gradle.properties"] = ("org.gradle.caching=false\n"
                                  "org.gradle.unsafe.isolated-projects=true\n")
    files["build.gradle"] += ("test { testLogging { showStandardStreams = true }\n"
                              "       outputs.upToDateWhen { false } }\n")
    files["settings.gradle"] = "plugins { id 'com.gradle.develocity' version '3.18' }\n" + \
        files["settings.gradle"]
    project = run_tests.Project(tree("tashxis_gradle", files), runner=["./gradlew"])
    titles = " | ".join(f[1] for f in run_tests.diagnose(project))
    clean = run_tests.Project(tree("tashxis_gradle_toza", gradle_shop()), runner=["./gradlew"])
    clean_titles = " | ".join(f[1] for f in run_tests.diagnose(clean))
    single = {"settings.gradle": "pluginManagement { includeBuild 'build-logic' }\n"
                                 "rootProject.name = 'one'\n",
              "build.gradle": "apply plugin: 'java'\n",
              "src/test/java/one/OneTest.java": java("one", "OneTest")}
    single_titles = " | ".join(f[1] for f in run_tests.diagnose(run_tests.Project(
        tree("tashxis_bitta", single), runner=["./gradlew"])))

    def scan(settings):
        files = gradle_shop()
        files["settings.gradle"] = settings + files["settings.gradle"]
        project = run_tests.Project(tree("tashxis_scan", files), runner=["./gradlew"])
        return any("Build scan" in f[1] for f in run_tests.diagnose(project))

    return ("build cache o'chirilgan" in titles and "showStandardStreams" in titles
            and "UP-TO-DATE" in titles and "Build scan" in titles
            and "Isolated projects" in titles
            and "build cache" not in clean_titles and "Build scan" not in clean_titles
            and "ketma-ket" not in single_titles
            and not scan("plugins { id 'com.gradle.enterprise' version '3.16' }\n")
            and scan("plugins { id 'com.gradle.enterprise' version '3.16' }\n"
                     "gradleEnterprise { buildScan { publishAlways() } }\n")
            and not scan("plugins { id 'com.gradle.develocity' version '3.18' }\n"
                         "develocity { buildScan { publishing.onlyIf { false } } }\n"))


def case_ildiz_qulfi(_):
    root = tree("ildiz_qulfi", gradle_shop())
    with run_tests.root_lock(root):
        first = True
    with run_tests.root_lock(root):
        second = True
    return first and second


CASES = [
    ("settings.gradle: groovy, kotlin, projectDir", case_settings_groovy_va_kotlin),
    ("Gradle modul yo'li", case_modul_yoli_gradle),
    ("migratsiya papkasini o'qiydigan bazasiz test ham tanlanadi", case_migratsiya_papkasini_oqiydigan_unit_test),
    (".claude/worktrees ichidagi nusxa modul emas", case_claude_worktree_modul_emas),
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
    ("vaqt tugasa nevara ham to'xtaydi", case_vaqt_tugadi_nevara),
    ("KeyboardInterrupt da nevara to'xtaydi", case_keyboard_interrupt_nevara),
    ("SIGTERM da nevara to'xtaydi", case_sigterm_nevara),
    ("ta'sir yo'q: yurmaydi", case_tasir_yoq),
    ("--hammasi filtrsiz", case_hammasi),
    ("--modul: butun modul, boshqasi yo'q", case_modul),
    ("symlink yoki qisqa nom orqali yo'l", case_symlink_orqali_yol),
    ("symlink orqali ildiz: bitta ildiz va log nomi", case_symlink_ildiz_log),
    ("--diff: non-ASCII nomli migratsiya", case_diff_non_ascii_migratsiya),
    ("--diff: non-ASCII nomli untracked test", case_diff_non_ascii_untracked),
    ("monorepo: --ildiz backend --diff, frontend eslatma", case_monorepo_diff),
    ("monorepo: --ildiz backend --asos", case_monorepo_asos),
    ("monorepo: --ildiz siz, ildizdan va submoduldan", case_monorepo_ildizsiz),
    ("ildiz: eng yuqori marker, yagona papka, noaniq rc 2", case_ildiz_tanlash),
    ("asbob: wrapperi bor ustun", case_asbob_wrapper_ustun),
    ("asbob: wrapper ikkalasida yoki yo'q", case_asbob_noaniq),
    ("asbob: --asbob va GENIUS_BUILD_TOOL", case_asbob_tanlov),
    ("asbob: reja qatori va rc 2", case_asbob_cli),
    ("Quarkus va Micronaut testlari", case_quarkus_micronaut_sozlama),
    ("qayta yurish: test soni birinchi yurishdan", case_qayta_yurish_jami),
    ("--log faqat temp yoki loyiha ichida", case_log_faqat_temp_yoki_loyiha),
    ("--asos bayroq emas, commit bo'lmasa 2", case_asos_bayroq_emas),
    ("navbat qulfi yechiladi", case_navbat_qulfi),
    ("tashxis: daemon, forkEvery, konteyner, sleep, hisobot", case_tashxis),
    ("tashxis: static konteyner toza", case_tashxis_static_konteyner_toza),
    ("Spring sozlamasi: barcha Spring testlari", case_spring_sozlamasi),
    ("kutubxona modul sozlamasi", case_kutubxona_sozlamasi),
    ("entity: baza testlari", case_entity_baza_testlari),
    ("sozlama: ota sinf orqali Spring testi", case_sozlama_ota_sinf_orqali),
    ("XML dan yiqilgan sinflar", case_xml_dan_yiqilgan),
    ("beqaror: exit 4, faqat yiqilgani qayta", case_beqaror_exit_4),
    ("doimiy yiqilish: exit 1", case_doimiy_yiqilish),
    ("kompilyatsiya xatosida qayta yurish yo'q", case_kompilyatsiya_qayta_yoq),
    ("--qayta 0: qayta yurish yo'q", case_qayta_ochiq),
    ("--isit: testClasses", case_isit),
    ("jurnal va --hisobot", case_jurnal_hisobot),
    ("tashxis: kontekst ishga tushishi logdan", case_kontekst_ishga_tushishi),
    ("Maven: jacoco faqat maqsadlida o'chadi", case_maven_jacoco_maqsadlida),
    ("Maven --coverage: jacoco qoladi, jacoco:report", case_maven_coverage),
    ("GENIUS_TEST_FLAGS", case_qoshimcha_bayroqlar),
    ("ildiz qulfi yechiladi", case_ildiz_qulfi),
    ("Gradle init: maqsadlida jacoco o'chadi, cache faqat kompilyatsiya", case_gradle_init),
    ("Gradle --coverage: jacoco agenti va hisobot qoladi", case_gradle_coverage),
    ("--coverage: hisobot yo'li yangi XML dan", case_coverage_hisobot_yoli),
    ("describe: --coverage init satri", case_describe_coverage),
    ("Gradle cache: loyiha, foydalanuvchi va -D qarori ustun", case_gradle_kesh_qarori),
    ("Gradle init: o'chirish, Gradle 6.0, noma'lum versiya, isolated", case_gradle_init_ochirish),
    ("isitish: Gradle source set lari, papka nomidan emas", case_isit_hamma_toplam),
    ("properties: =, : va bo'shliq ajratgich", case_properties_sintaksisi),
    ("describe: Gradle init satri", case_describe_init),
    ("composite build: :money:core:test, :test emas", case_composite_build),
    ("coverage ham yiqilgan bo'lsa beqaror emas, exit 1", case_boshqa_yiqilish),
    ("composite: papka nomi, name=, nested, dinamik include", case_composite_nomi_va_dinamik),
    ("soyabon composite: faqat :<nom>: vazifalari", case_soyabon_composite),
    ("source set nomi: srcDir va camelCase", case_source_set_nomi),
    ("tashxis: Gradle cache, log, UP-TO-DATE, build scan, isolated", case_tashxis_gradle),
]


# -- haqiqiy Gradle (qo'lda: --gradle) ---------------------------------------

E2E_BUILD = """
subprojects {
    apply plugin: 'java'
    apply plugin: 'jacoco'
    repositories { mavenCentral() }
    dependencies {
        testImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'
        testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
    }
    test {
        useJUnitPlatform()
        finalizedBy jacocoTestReport, jacocoTestCoverageVerification
        // Build XML ni o'chirgan: qayta yurish init skript majburlagan XML ga tayanadi.
        reports.junitXml.required = false
    }
    jacocoTestCoverageVerification {
        violationRules { rule { limit { minimum = 0.9 } } }
    }
}
project(':orders') { dependencies { implementation project(':common') } }
"""

E2E_TEST = """package shop.orders;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
class OrderServiceTest { @Test void total() { assertEquals(%d, new OrderService().total(2)); } }
"""

E2E_JAVA_BUILD = """apply plugin: 'java'
repositories { mavenCentral() }
dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}
test { useJUnitPlatform() }
"""


def write_files(root, files):
    for path, text in files.items():
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as handle:
            handle.write(text)


def e2e_project(root, version):
    files = {
        "settings.gradle": "rootProject.name = 'shop'\ninclude 'common', 'orders'\n",
        "build.gradle": E2E_BUILD,
        "gradle/wrapper/gradle-wrapper.properties": WRAPPER % version,
        "common/src/test/java/shop/common/Gen0Test.java":
            "package shop.common;\nimport org.junit.jupiter.api.Test;\n"
            "class Gen0Test { @Test void works() { new Gen0().m0(1); } }\n",
        "orders/src/main/java/shop/orders/OrderService.java":
            "package shop.orders;\npublic class OrderService {\n"
            "    public int total(int x) { return new shop.common.Gen1().m0(x); }\n}\n",
        "orders/src/test/java/shop/orders/OrderServiceTest.java": E2E_TEST % 2,
        # Refund ni faqat OtherTest qoplaydi: OrderServiceTest yolg'iz
        # yursa modul coverage 0.9 dan past.
        "orders/src/main/java/shop/orders/Refund.java":
            "package shop.orders;\npublic class Refund {\n" + "".join(
                "    public int r%d(int x) { if (x > %d) { return x - %d; } return x + %d; }\n"
                % (j, j, j, j) for j in range(30)) + "}\n",
        "orders/src/test/java/shop/orders/OtherTest.java":
            "package shop.orders;\nimport org.junit.jupiter.api.Test;\n"
            "class OtherTest { @Test void other() { Refund r = new Refund();\n" + "".join(
                "  r.r%d(100); r.r%d(-100);\n" % (j, j) for j in range(30)) + "} }\n",
    }
    for i in range(40):
        files["common/src/main/java/shop/common/Gen%d.java" % i] = (
            "package shop.common;\npublic class Gen%d {\n" % i + "".join(
                "    public int m%d(int x) { return x * %d + %d; }\n" % (j, i, j)
                for j in range(10)) + "}\n")
    shutil.rmtree(root, ignore_errors=True)
    write_files(root, files)
    with open(os.path.join(root, ".gitignore"), "w") as handle:
        handle.write(".gradle/\nbuild/\n")
    commit(root)


class CacheServer:
    """Remote build cache o'rnida: murojaatlarni sanaydi, hammasiga 404."""

    def __init__(self):
        import http.server
        import threading
        hits = self.hits = []

        class Handler(http.server.BaseHTTPRequestHandler):
            def answer(self):
                hits.append(self.command)
                length = int(self.headers.get("Content-Length") or 0)
                if length:
                    self.rfile.read(length)
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()

            do_GET = do_PUT = do_HEAD = answer

            def log_message(self, *args):
                pass

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = "http://127.0.0.1:%d/cache/" % self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def settings(self):
        return ("buildCache { remote(HttpBuildCache) { url = '%s'\n"
                "    push = true; allowInsecureProtocol = true } }\n" % self.url)


def gradle_e2e(gradle):
    env = dict(os.environ, GENIUS_TEST_RUNNER=json.dumps([gradle]), GENIUS_STATE_DIR=STATE)
    version = re.search(r"Gradle (\d+\.\d+(?:\.\d+)?)", subprocess.run(
        [gradle, "--version"], capture_output=True, text=True, env=env).stdout).group(1)
    print("Gradle %s" % version)
    root = os.path.join(TEMP, "e2e")
    e2e_project(root, version)
    results = []

    def cli(cwd, *args, **extra):
        # Tarmoq xatosi (Maven Central 429, uzilish) sinov natijasi emas: qayta urinish.
        log = os.path.join(TEMP, "e2e-%d.log" % len(results))
        for attempt in range(3):
            proc = subprocess.run([sys.executable, TOOL] + list(args) + ["--log", log],
                                  cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                                  env=dict(env, **extra), timeout=900)
            with open(log, encoding="utf-8", errors="replace") as handle:
                text = handle.read()
            if not re.search(r"Could not (?:GET|HEAD|download|resolve)", text):
                break
            time.sleep(5 * (attempt + 1))
        return proc.returncode, text, proc.stdout

    def check(name, ok, detail=""):
        results.append(bool(ok))
        print("%-4s %s%s" % ("OK" if ok else "XATO", name, "" if ok else "  :: " + detail))

    def edit(path, text, append=False):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a" if append else "w", encoding="utf-8") as handle:
            handle.write(text)

    def tail(log):
        return " | ".join(l for l in log.splitlines()[-40:] if "wrong" in l or "FAIL" in l
                          or "Could not" in l or "Rule" in l)[:600]

    exec_file = os.path.join(root, "orders", "build", "jacoco", "test.exec")
    html = os.path.join(root, "orders", "build", "reports", "tests", "test")
    code, log, _ = cli(root, "--hammasi", "--yurgiz")
    check("to'liq suite: coverage tekshiruvi saqlanadi",
          code == 1 and "Rule violated" in log and os.path.exists(exec_file),
          "exit=%d exec=%s %s" % (code, os.path.exists(exec_file), tail(log)))

    edit(os.path.join(root, "orders/src/main/java/shop/orders/OrderService.java"),
         "// o'zgarish\n", append=True)
    code, log, _ = cli(root, "--diff", "--yurgiz", GENIUS_GRADLE_INIT="0")
    check("init siz: maqsadli yurish coverage tufayli yiqiladi (nazorat)",
          code == 1 and "Rule violated" in log, "exit=%d" % code)
    # Eski exec qoladi: hisobot va coverage vazifasi o'chiqligi shu holatda sinaladi.
    before = os.stat(exec_file)
    shutil.rmtree(html, ignore_errors=True)
    code, log, out = cli(root, "--diff", "--yurgiz")
    after = os.stat(exec_file)
    xml = os.path.join(root, "orders/build/test-results/test/TEST-shop.orders.OrderServiceTest.xml")
    check("init bilan: eski exec bo'lsa ham yashil, agent va HTML hisobot yo'q, XML bor",
          code == 0 and (after.st_mtime_ns, after.st_size) == (before.st_mtime_ns, before.st_size)
          and not os.path.exists(html) and os.path.exists(xml), "exit=%d %s" % (code, out[-300:]))

    worktrees = []
    for name in ("wa", "wb", "wc"):
        path = os.path.join(TEMP, "e2e-" + name)
        git(root, "worktree", "add", "-q", path, "HEAD")
        worktrees.append(path)
    wa, wb, wc = worktrees
    target = "orders/src/test/java/shop/orders/OrderServiceTest.java"
    cli(wa, target, "--yurgiz")
    code, log, _ = cli(wb, target, "--yurgiz")
    check("yangi worktree: kompilyatsiya cache dan, test cache dan emas",
          code == 0 and ":common:compileJava FROM-CACHE" in log
          and "> Task :orders:test\n" in log and ":orders:test FROM-CACHE" not in log,
          "exit=%d" % code)

    edit(os.path.join(wb, target), E2E_TEST % 3)
    code, log, out = cli(wb, target, "--yurgiz")
    check("yiqilgan test: exit 1, XML (build o'chirgan, init majburlagan) dan qayta yurish",
          code == 1 and "OrderServiceTest" in out and "qayta yurish:" in out, "exit=%d" % code)
    edit(os.path.join(wb, target), E2E_TEST % 2)

    server = CacheServer()
    service = os.path.join(wb, "orders/src/main/java/shop/orders/OrderService.java")
    edit(os.path.join(wb, "settings.gradle"), server.settings(), append=True)
    edit(service, "class Miss1 { }\n", append=True)
    code, log, _ = cli(wb, target, "--yurgiz")
    ours = len(server.hits)
    edit(service, "class Miss2 { }\n", append=True)
    cli(wb, target, "--yurgiz", GENIUS_GRADLE_INIT="0", GENIUS_TEST_FLAGS="--build-cache")
    check("remote: asbob yoqqan cache da murojaat yo'q (nazoratda bor)",
          code == 0 and ours == 0 and len(server.hits) > ours,
          "exit=%d ours=%d nazorat=%d" % (code, ours, len(server.hits) - ours))

    home = os.environ["GRADLE_USER_HOME"]
    os.makedirs(os.path.join(home, "init.d"), exist_ok=True)
    initd = os.path.join(home, "init.d", "genius-e2e-remote.gradle")
    edit(initd, "settingsEvaluated { s -> s.%s }\n" % server.settings().strip())
    hits = len(server.hits)
    edit(os.path.join(wa, "orders/src/main/java/shop/orders/OrderService.java"),
         "class Miss3 { }\n", append=True)
    code, log, _ = cli(wa, target, "--yurgiz")
    os.remove(initd)
    check("remote: GRADLE_USER_HOME/init.d dagi remote ham o'chadi",
          code == 0 and len(server.hits) == hits, "exit=%d murojaat=%d" % (
              code, len(server.hits) - hits))

    edit(os.path.join(wc, "gradle.properties"), "org.gradle.caching=true\n")
    edit(os.path.join(wc, "settings.gradle"), server.settings(), append=True)
    edit(os.path.join(wc, "orders/src/main/java/shop/orders/OrderService.java"),
         "class Miss5 { }\n", append=True)
    hits = len(server.hits)
    code, log, out = cli(wc, target, "--yurgiz")
    command = next((l for l in out.splitlines() if l.startswith("Buyruq")), "")
    check("loyiha cache i (org.gradle.caching=true): asbob tegmaydi, remote ishlaydi",
          code == 0 and "--build-cache" not in command and len(server.hits) > hits,
          "exit=%d murojaat=%d" % (code, len(server.hits) - hits))

    edit(os.path.join(wc, "orders/build.gradle"), """
sourceSets { integrationTest { java.srcDir 'src/integration-test/java' } }
dependencies {
    integrationTestImplementation 'org.junit.jupiter:junit-jupiter:5.10.2'
    integrationTestRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}
tasks.register('integrationTest', Test) {
    testClassesDirs = sourceSets.integrationTest.output.classesDirs
    classpath = sourceSets.integrationTest.runtimeClasspath
    useJUnitPlatform()
}
""")
    flow = "orders/src/integration-test/java/shop/orders/FlowIT.java"
    edit(os.path.join(wc, flow), "package shop.orders;\nimport org.junit.jupiter.api.Test;\n"
                                 "class FlowIT { @Test void flow() { } }\n")
    code, log, _ = cli(wc, "--isit")
    check("--isit: papka nomi source set nomidan farq qilsa ham test sinflari quriladi",
          code == 0 and os.path.isdir(os.path.join(
              wc, "orders/build/classes/java/integrationTest")), "exit=%d" % code)
    code, log, _ = cli(wc, flow, "--yurgiz")
    check("src/integration-test dagi test :orders:integrationTest bilan yuradi",
          code == 0 and os.path.exists(os.path.join(
              wc, "orders/build/test-results/integrationTest/TEST-shop.orders.FlowIT.xml")),
          "exit=%d %s" % (code, tail(log)))

    comp = os.path.join(TEMP, "e2e-composite")
    shutil.rmtree(comp, ignore_errors=True)
    write_files(comp, {
        "settings.gradle": "rootProject.name = 'shop'\ninclude 'app'\nincludeBuild 'libs/money'\n",
        "gradle/wrapper/gradle-wrapper.properties": WRAPPER % version,
        "app/build.gradle": E2E_JAVA_BUILD + "dependencies { implementation 'shop:money' }\n",
        "app/src/main/java/app/App.java":
            "package app;\npublic class App { int x() { return new money.Money().v(); } }\n",
        "libs/money/settings.gradle": "rootProject.name = 'money'\n",
        "libs/money/build.gradle": E2E_JAVA_BUILD + "group = 'shop'\n",
        "libs/money/src/main/java/money/Money.java":
            "package money;\npublic class Money { public int v() { return 1; } }\n",
        "libs/money/src/test/java/money/MoneyTest.java":
            "package money;\nimport org.junit.jupiter.api.Test;\n"
            "class MoneyTest { @Test void v() { new Money().v(); } }\n",
        ".gitignore": ".gradle/\nbuild/\n",
    })
    commit(comp)
    edit(os.path.join(comp, "libs/money/src/main/java/money/Money.java"), "// o'zgarish\n",
         append=True)
    code, log, _ = cli(comp, "--diff", "--yurgiz")
    check("composite build: included build testi :money:test bilan yuradi",
          code == 0 and os.path.exists(os.path.join(
              comp, "libs/money/build/test-results/test/TEST-money.MoneyTest.xml")),
          "exit=%d" % code)
    isit, _, _ = cli(comp, "--isit")
    code, log, _ = cli(comp, "--hammasi", "--yurgiz")
    check("composite: ildizda testsiz --isit va --hammasi :money: vazifalari bilan",
          isit == 0 and code == 0 and "> Task :money:test" in log,
          "isit=%d hammasi=%d %s" % (isit, code, tail(log)))

    server.server.shutdown()
    subprocess.run([gradle, "--stop"], capture_output=True, env=env)
    print("\n%d/%d o'tdi (Gradle %s e2e)" % (sum(results), len(results), version))
    return 0 if all(results) else 1


def main():
    if "--gradle" in sys.argv:
        rest = sys.argv[sys.argv.index("--gradle") + 1:]
        gradle = rest[0] if rest else shutil.which("gradle")
        if not gradle:
            print("gradle topilmadi: yo'lini bering, `--gradle /yo'l/gradle`")
            return 2
        try:
            return gradle_e2e(gradle)
        finally:
            shutil.rmtree(TEMP, ignore_errors=True)
    failures = skipped = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(None))
            except Skip as exc:
                skipped += 1
                print("%-4s %s" % ("SKIP", "%s (%s)" % (name, exc)))
                continue
            except Exception as exc:
                ok, name = False, "%s (%s: %s)" % (name, type(exc).__name__, exc)
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", name))
    finally:
        shutil.rmtree(TEMP, ignore_errors=True)
    print("\n%d/%d o'tdi%s" % (len(CASES) - failures - skipped, len(CASES) - skipped,
                              ", %d o'tkazildi" % skipped if skipped else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
