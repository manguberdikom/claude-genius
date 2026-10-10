#!/usr/bin/env python3
"""sonar_local.py uchun sinovlar: tarmoq va docker mock qilinadi.

    python3 tools/test_sonar_local.py [-k bo'lim]
"""

import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sonar_local as sl  # noqa: E402
import testkit  # noqa: E402

TMP = tempfile.mkdtemp(prefix="sonar-local-")
SECRET = "sinov-parol-qiymati"


def case_kalit():
    return [
        ("https remote + branch", sl.project_key("https://git.example.org/acme/shop/orders.git", "dev")
         == "acme-shop-orders-dev"),
        ("ssh (scp) remote", sl.project_key("git@git.example.org:grp/sub/repo.git", "main") == "grp-sub-repo-main"),
        ("ssh:// remote portli, .git siz", sl.remote_slug("ssh://git@h.example:2222/grp/repo") == "grp-repo"),
        ("oxiridagi / va .git", sl.remote_slug("https://h.example/a/b.git/") == "a-b"),
        ("branch dagi / tozalanadi", sl.project_key("https://h/a/b.git", "feature/x y") == "a-b-feature-x-y"),
        ("detached HEAD: kalit yo'q", sl.project_key("https://h/a/b.git", "HEAD") == ""),
        ("remote yo'q: kalit yo'q", sl.project_key("", "dev") == ""),
    ]


def case_report_task():
    text = ("projectKey=k\nserverUrl=http://localhost:9000\n"
            "ceTaskUrl=http://localhost:9000/api/ce/task?id=AX1\ndashboardUrl=http://x/dashboard?id=k\n")
    got = sl.read_report_task(text)
    return [
        ("ceTaskUrl o'qildi (= ichida = bor qiymat ham)", got["ceTaskUrl"].endswith("task?id=AX1")),
        ("projectKey o'qildi", got["projectKey"] == "k"),
        ("bo'sh matn: bo'sh dict", sl.read_report_task("") == {}),
    ]


def case_hotspot():
    def spot(key, rule, comp, line, resolution=None):
        out = {"key": key, "ruleKey": rule, "component": "p:" + comp, "line": line}
        if resolution:
            out["resolution"] = resolution
        return out
    reviewed = [spot("r1", "java:S5122", "src/A.java", 7, "SAFE"),
                spot("r2", "java:S2245", "src/B.java", 3, "ACKNOWLEDGED")]
    pending = [spot("l1", "java:S5122", "src/A.java", 7),
               spot("l2", "java:S2245", "src/B.java", 4),      # qator siljigan
               spot("l3", "java:S4423", "src/C.java", 1)]      # serverda ko'rilmagan
    moves = sl.match_hotspots(reviewed, pending)
    return [
        ("qoida+fayl+qator mos: ko'chadi", moves == [("l1", "SAFE")]),
        ("qator siljigan va yangisi TO_REVIEW qoladi", len(moves) == 1),
        ("resolution saqlanadi", sl.match_hotspots(reviewed[1:], [spot("x", "java:S2245", "src/B.java", 3)])
         == [("x", "ACKNOWLEDGED")]),
        ("resolution yo'q: SAFE", sl.match_hotspots([spot("r", "a", "f", 1)], [spot("l", "a", "f", 1)])
         == [("l", "SAFE")]),
    ]


def case_chiqish_kodi():
    return [
        ("gate OK, topilma yo'q: 0", sl.verdict("OK", 0, 0) == 0),
        ("gate ERROR: 1", sl.verdict("ERROR", 0, 0) == 1),
        ("ochiq issue: 1", sl.verdict("OK", 2, 0) == 1),
        ("TO_REVIEW hotspot: 1", sl.verdict("OK", 0, 1) == 1),
        ("solishtir: farq yo'q 0", sl.compare_verdict("abc", "abc", []) == 0),
        ("solishtir: bir xil commit va farq 1", sl.compare_verdict("abc", "abc", ["x"]) == 1),
        ("solishtir: commit boshqa va farq 3", sl.compare_verdict("abc", "def", ["x"]) == 3),
        ("solishtir: commit noma'lum va farq 3", sl.compare_verdict("", "def", ["x"]) == 3),
    ]


def case_exec():
    now = time.time()
    src = os.path.join(TMP, "proj", "mod", "src", "main", "java")
    jac = os.path.join(TMP, "proj", "mod", "build", "jacoco")
    os.makedirs(src)
    os.makedirs(jac)
    java = os.path.join(src, "A.java")
    for path in (java, os.path.join(jac, "test.exec"), os.path.join(jac, "integrationTest.exec")):
        with open(path, "w") as handle:
            handle.write("x")
    os.utime(java, (now - 100, now - 100))
    for name in ("test.exec", "integrationTest.exec"):
        os.utime(os.path.join(jac, name), (now, now))
    root = os.path.join(TMP, "proj")
    found = sl.find_exec(root)
    fresh = sl.exec_state([os.path.getmtime(p) for p in found], sl.newest_mtime(root))
    os.utime(java, (now + 50, now + 50))
    stale = sl.exec_state([os.path.getmtime(p) for p in found], sl.newest_mtime(root))
    return [
        ("2 exec topildi", len(found) == 2),
        ("exec manbadan yangi: yangi", fresh == "yangi"),
        ("manba exec dan yangi: eskirgan", stale == "eskirgan"),
        ("exec yo'q: yo'q", sl.exec_state([], 1.0) == "yo'q"),
        ("eng eski exec hisoblanadi", sl.exec_state([10.0, 99.0], 50.0) == "eskirgan"),
    ]


def case_versiya():
    return [
        ("image dan versiya", sl.image_version("sonarqube:26.6.0.123539-community") == "26.6.0.123539"),
        ("registry prefiksi bilan", sl.image_version("docker.io/library/sonarqube:26.6.0.1-community") == "26.6.0.1"),
        ("tag yo'q: bo'sh", sl.image_version("sonarqube") == ""),
        ("image nomi", sl.image_name("26.6.0.1") == "sonarqube:26.6.0.1-community"),
        ("bir xil versiya mos", sl.versions_match("26.6", "26.6")),
        ("farqli versiya mos emas", not sl.versions_match("26.5", "26.6")),
        ("noma'lum versiya to'sqinlik qilmaydi", sl.versions_match("", "26.6")),
    ]


def case_docker_ps():
    up = "sonar-local\tUp 14 minutes\tsonarqube:26.6.0.1-community\n"
    down = "other\tUp 1 hour\tpostgres:16\nsonar-local\tExited (0) 2 hours ago\tsonarqube:26.5.0.1-community\n"
    got_up, got_down = sl.parse_docker_ps(up), sl.parse_docker_ps(down)
    return [
        ("ishlayotgan konteyner", got_up["running"] and got_up["image"].endswith("-community")),
        ("to'xtagan konteyner", got_down is not None and not got_down["running"]),
        ("boshqa nom e'tiborga olinmaydi", sl.parse_docker_ps("sonar-local2\tUp\tx\n") is None),
        ("bo'sh chiqish: yo'q", sl.parse_docker_ps("") is None),
        ("run argumentlari: mmap, volume, versiya",
         "SONAR_SEARCH_JAVAADDITIONALOPTS=-Dnode.store.allow_mmap=false" in sl.run_args("26.6.0.1")
         and "sonar_local_data:/opt/sonarqube/data" in sl.run_args("26.6.0.1")
         and sl.run_args("26.6.0.1")[-1] == "sonarqube:26.6.0.1-community"),
    ]


class FakeDocker:
    def __init__(self, ps_out):
        self.ps_out = ps_out
        self.calls = []

    def __call__(self, *args):
        self.calls.append(args)
        if args[0] == "ps":
            return 0, self.ps_out
        return 0, "id"


def with_mocks(ps_out, status="", local_ver="", remote_ver="26.6.0.1"):
    fake = FakeDocker(ps_out)
    saved = (sl.docker, sl.local_status, sl.local_version, sl.remote_version, sl.wait_up)
    state = {"status": status}
    sl.docker = fake
    sl.local_status = lambda: state["status"]
    sl.local_version = lambda: local_ver
    sl.remote_version = lambda: remote_ver
    sl.wait_up = lambda timeout=0: 1
    return fake, saved


def restore(saved):
    sl.docker, sl.local_status, sl.local_version, sl.remote_version, sl.wait_up = saved


def case_ishga():
    rows = []
    fake, saved = with_mocks("", status="UP", local_ver="26.6.0.1")
    try:
        text, notes = sl.ensure_running()
        rows.append(("UP va mos: docker ga tegilmaydi", fake.calls == [] and notes == []))
    finally:
        restore(saved)
    fake, saved = with_mocks("", status="UP", local_ver="26.5.0.1")
    try:
        text, notes = sl.ensure_running()
        rows.append(("UP, versiya mos emas: ogohlantirish, docker yo'q", fake.calls == [] and "--yangila" in notes[0]))
    finally:
        restore(saved)
    fake, saved = with_mocks("")
    try:
        text, _ = sl.ensure_running()
        rows.append(("konteyner yo'q: docker run server versiyasi bilan",
                     fake.calls[-1][0] == "run" and fake.calls[-1][-1] == "sonarqube:26.6.0.1-community"
                     and "yaratildi" in text))
    finally:
        restore(saved)
    fake, saved = with_mocks("sonar-local\tExited (0) 1 hour ago\tsonarqube:26.6.0.1-community\n")
    try:
        text, notes = sl.ensure_running()
        rows.append(("to'xtagan: docker start", fake.calls[-1] == ("start", "sonar-local") and notes == []))
    finally:
        restore(saved)
    fake, saved = with_mocks("sonar-local\tUp 3 hours\tsonarqube:26.5.0.1-community\n", status="")
    try:
        text, notes = sl.ensure_running()
        rows.append(("ishlayapti, eski image: ogohlantirish, qayta yaratilmaydi",
                     [c[0] for c in fake.calls] == ["ps"] and "26.5.0.1" in notes[0]))
    finally:
        restore(saved)
    fake, saved = with_mocks("sonar-local\tUp 3 hours\tsonarqube:26.5.0.1-community\n", status="UP", local_ver="26.5.0.1")
    try:
        text, _ = sl.ensure_running(update=True)
        names = [c[0] for c in fake.calls]
        rows.append(("--yangila: rm -f keyin run, volume o'chmaydi",
                     names == ["ps", "rm", "run"] and fake.calls[1] == ("rm", "-f", "sonar-local")
                     and "-v" in fake.calls[2]))
    finally:
        restore(saved)
    return rows


def case_docker_yoq():
    saved = (sl.docker, sl.local_status, sl.remote_version)

    def no_docker(*args):
        raise sl.Fail("docker topilmadi: lokal SonarQube uchun Docker kerak")
    sl.docker = no_docker
    sl.local_status = lambda: ""
    sl.remote_version = lambda: "26.6.0.1"
    try:
        res = testkit.call_main(sl.main, argv=["sonar_local.py", "ishga"])
    finally:
        sl.docker, sl.local_status, sl.remote_version = saved
    return [("docker yo'q: rc 2 va tushunarli xabar", res.returncode == 2 and "docker topilmadi" in res.stderr)]


def case_buyruq_va_holat():
    old = os.environ.get("GENIUS_SONAR_LOCAL_STATE")
    os.environ["GENIUS_SONAR_LOCAL_STATE"] = os.path.join(TMP, "state.json")
    try:
        sl.save_state({"password": SECRET, "token": "squ_x"})
        mode = os.stat(sl.state_path()).st_mode & 0o777
        loaded = sl.load_state()
    finally:
        if old is None:
            os.environ.pop("GENIUS_SONAR_LOCAL_STATE", None)
        else:
            os.environ["GENIUS_SONAR_LOCAL_STATE"] = old
    cmd = sl.build_command(TMP, "maven", "k", "n", False, "x.gradle")
    gradle = sl.build_command(os.path.join(TMP, "proj"), "gradle", "k", "n", False, "i.gradle")
    gradle_t = sl.build_command(os.path.join(TMP, "proj"), "gradle", "k", "n", True, "i.gradle")
    outer = os.path.join(TMP, "outer")
    for folder, text in ((os.path.join(outer, "nested"), 'tasks.register("integrationTest")'),
                         (os.path.join(outer, "module"), 'tasks.register("moduleCheck")')):
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "build.gradle.kts"), "w", encoding="utf-8") as h:
            h.write(text)
    with open(os.path.join(outer, "nested", "settings.gradle.kts"), "w", encoding="utf-8") as h:
        h.write('rootProject.name = "nested"')
    nested_cmd = sl.build_command(outer, "gradle", "k", "n", False, "i.gradle")
    os.environ["NODEFAULTCURRENTDIRECTORYINEXEPATH"] = "1"
    try:
        env = sl.scan_env("squ_tokenqiymati")
    finally:
        os.environ.pop("NODEFAULTCURRENTDIRECTORYINEXEPATH", None)
    return [
        ("holat o'qiladi", loaded.get("password") == SECRET),
        ("holat 0600 (POSIX)", os.name == "nt" or mode == 0o600),
        ("gradle: testlarsiz, init va kalit", "-x" in gradle and "test" in gradle and "sonar" in gradle
         and "-Dsonar.projectKey=k" in gradle and "i.gradle" in gradle),
        ("gradle --testlar: test va jacocoTestReport", "jacocoTestReport" in gradle_t and "-x" not in gradle_t),
        ("gradle: ichki mustaqil build vazifasi tashqi ildizga -x bo'lib tushmaydi",
         "integrationTest" not in nested_cmd and sl.mentions_task(outer, "moduleCheck")
         and sl.mentions_task(os.path.join(outer, "nested"), "integrationTest")),
        ("maven: -DskipTests", "-DskipTests" in cmd and any("sonar-maven-plugin" in c for c in cmd)),
        ("token faqat muhitda, buyruqda emas", env["SONAR_TOKEN"] == "squ_tokenqiymati"
         and not any("squ_" in c for c in gradle + gradle_t + cmd)),
        ("NoDefaultCurrentDirectoryInExePath olib tashlanadi", not any(k.lower() == "nodefaultcurrentdirectoryinexepath" for k in env)),
        ("muhit kaliti asl yozilishida: Gradle xossa nomi kichik-katta farqli",
         sl.original_case_env({"ORG_GRADLE_PROJECT_REPOURL": "yangi", "PATH": "p", "QOSHIMCHA": "q"},
                              {"ORG_GRADLE_PROJECT_repoUrl": "eski", "Path": "p"})
         == {"ORG_GRADLE_PROJECT_repoUrl": "yangi", "Path": "p", "QOSHIMCHA": "q"}),
    ]


def case_sir():
    """Parol va token chop etilmaydi: sozla xatosi qiymatsiz."""
    saved = sl.Remote
    sl.Remote = lambda: (_ for _ in ()).throw(sl.sonar_fetch.Config("token fayli o'qilmadi: x"))
    try:
        res = testkit.call_main(sl.main, argv=["sonar_local.py", "sozla", "--loyiha", "k"])
    finally:
        sl.Remote = saved
    return [("token fayli yo'q: rc 2, qiymatsiz", res.returncode == 2 and SECRET not in res.stderr + res.stdout
             and "token fayli" in res.stderr)]


def case_moslik():
    def act(rule, sev, params=()):
        return {rule: [{"qProfile": "P", "severity": sev,
                        "params": [{"key": k, "value": v} for k, v in params]}]}
    a = {}
    a.update(act("java:S1", "MAJOR"))
    a.update(act("java:S2", "MINOR", [("max", "15")]))
    b = {}
    b.update(act("java:S2", "MINOR", [("max", "15")]))
    b.update(act("java:S1", "MAJOR"))
    changed_sev = dict(b, **act("java:S1", "CRITICAL"))
    changed_param = dict(b, **act("java:S2", "MINOR", [("max", "20")]))
    other_profile = {"java:S1": [{"qProfile": "Q", "severity": "MAJOR", "params": []}]}
    sig = lambda x: sl.rules_signature(x, "P")
    plugins_r = [{"key": "java", "version": "8.1"}, {"key": "x", "version": "1"}]
    plugins_l = [{"key": "java", "version": "8.0"}]
    rs = [{"key": "sonar.exclusions", "values": ["a/**", "b/**"], "inherited": False},
          {"key": "sonar.cpd.exclusions", "value": "c/**", "inherited": False},
          {"key": "sonar.core.id", "value": "1", "inherited": False},
          {"key": "sonar.inherited", "value": "z", "inherited": True},
          {"key": "sonar.rows", "fieldValues": [{"a": "1"}], "inherited": False}]
    ls = [{"key": "sonar.exclusions", "values": ["a/**", "b/**"], "inherited": False},
          {"key": "sonar.cpd.exclusions", "value": "old", "inherited": False},
          {"key": "sonar.stale", "value": "q", "inherited": False}]
    to_set, to_reset = sl.settings_plan(rs, ls)
    remote_issues = [
        {"rule": "java:S1", "component": "p:src/A.java", "line": 3, "issueStatus": "ACCEPTED"},
        {"rule": "java:S2", "component": "p:src/B.java", "line": 5, "issueStatus": "FALSE_POSITIVE"},
        {"rule": "java:S3", "component": "p:src/C.java", "line": 1, "issueStatus": "OPEN"}]
    local_open = [
        {"key": "L1", "rule": "java:S1", "component": "p:src/A.java", "line": 3},
        {"key": "L2", "rule": "java:S2", "component": "p:src/B.java", "line": 6},
        {"key": "L3", "rule": "java:S3", "component": "p:src/C.java", "line": 1}]
    gate_a = {"conditions": [{"metric": "a", "op": "GT", "error": "1"}, {"metric": "b", "op": "LT", "error": "2"}]}
    gate_b = {"conditions": [{"metric": "b", "op": "LT", "error": "2"}, {"metric": "a", "op": "GT", "error": "1"}]}
    gate_c = {"conditions": [{"metric": "a", "op": "GT", "error": "5"}, {"metric": "b", "op": "LT", "error": "2"}]}
    return [
        ("qoida hash: tartibga bog'liq emas", sig(a) == sig(b) and sig(a)[1] == 2),
        ("qoida hash: severity farqi ushlanadi", sig(b) != sig(changed_sev)),
        ("qoida hash: param farqi ushlanadi", sig(b) != sig(changed_param)),
        ("qoida hash: boshqa profil sanalmaydi", sig(other_profile)[1] == 0),
        ("plugin farqi: versiya va yo'q plugin", len(sl.plugins_diff(plugins_r, plugins_l)) == 2
         and sl.plugins_diff(plugins_l, plugins_l) == []),
        ("gate shartlari: tartib farqsiz teng", sl.conditions_of(gate_a) == sl.conditions_of(gate_b)),
        ("gate shartlari: chegara farqi ushlanadi", sl.conditions_of(gate_a) != sl.conditions_of(gate_c)),
        ("sozlama: o'zgargan va yangi qo'yiladi, meros va bloklanganlar yo'q",
         [i["key"] for i in to_set] == ["sonar.cpd.exclusions", "sonar.rows"]),
        ("sozlama: lokalda ortiqcha tiklanadi", to_reset == ["sonar.stale"]),
        ("sozlama: teng bo'lsa reja bo'sh", sl.settings_plan(rs[:1], ls[:1]) == ([], [])),
        ("sozlama payload: values/fieldValues/value",
         sl.setting_payload("k", rs[0])["values"] == ["a/**", "b/**"]
         and sl.setting_payload("k", rs[4])["fieldValues"] == ['{"a": "1"}']
         and sl.setting_payload("k", rs[1])["value"] == "c/**"),
        ("issue status: qoida+fayl+qator mos, qator siljigani va OPEN yo'q",
         sl.match_issues(remote_issues, local_open) == [("L1", "accept")]),
        ("issue status: false positive", sl.match_issues(remote_issues, [dict(local_open[1], line=5)])
         == [("L2", "falsepositive")]),
        ("new code: teng", sl.new_code_action({"type": "PREVIOUS_VERSION"}, {"type": "PREVIOUS_VERSION"}) is None),
        ("new code: kunlar qo'yiladi", sl.new_code_action({"type": "NUMBER_OF_DAYS", "value": "30"},
                                                         {"type": "PREVIOUS_VERSION"}) == ("set", "NUMBER_OF_DAYS", "30")),
        ("new code: qo'llanmaydigan tur izoh", sl.new_code_action({"type": "REFERENCE_BRANCH", "value": "m"},
                                                                 {"type": "PREVIOUS_VERSION"})[0] == "note"),
        ("moslik qatori: tuzatilgan va tekshirib bo'lmagan",
         sl.moslik_line(["gate shartlari"], ["x"]) == "moslik: tuzatildi: gate shartlari. tekshirib bo'lmadi: x"
         and sl.moslik_line([], []) == "moslik: farq yo'q"),
    ]


SECTIONS = [
    ("Loyiha kaliti", case_kalit),
    ("report-task.txt", case_report_task),
    ("Hotspot moslash", case_hotspot),
    ("Chiqish kodi", case_chiqish_kodi),
    ("Exec eskirishi", case_exec),
    ("Versiya", case_versiya),
    ("docker ps", case_docker_ps),
    ("ishga (docker mock)", case_ishga),
    ("Docker yo'q", case_docker_yoq),
    ("Buyruq, muhit, holat", case_buyruq_va_holat),
    ("Sir chiqmaydi", case_sir),
    ("Moslik (tarmoqsiz)", case_moslik),
]


def main(argv=()):
    return testkit.run_cases(SECTIONS, argv, headers=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
