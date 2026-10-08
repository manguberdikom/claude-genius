#!/usr/bin/env python3
"""sonar_fetch.py uchun sinovlar: tarmoq mock qilinadi, token faylda.

    python3 tools/test_sonar_fetch.py [-k bo'lim]
"""

import base64
import os
import sys
import tempfile
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sonar_fetch as sf  # noqa: E402
import testkit  # noqa: E402

TOKEN = "squ_sinov_qiymati"
TMP = tempfile.mkdtemp(prefix="sonar-fetch-")
TOKEN_FILE = os.path.join(TMP, "token.txt")
with open(TOKEN_FILE, "w", encoding="utf-8") as handle:
    handle.write(TOKEN + "\n")

CALLS = []


def fake_get(url, token):
    CALLS.append((url, token))
    path = urllib.parse.urlparse(url).path
    page = int(urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("p", ["1"])[0])
    if path == "/api/issues/search":
        items = [
            {"rule": "java:S1128", "severity": "MINOR", "type": "CODE_SMELL",
             "component": "k:src/A.java", "line": 3, "message": "Remove\nthis  import"},
            {"rule": "java:S1068", "severity": "MAJOR", "type": "CODE_SMELL",
             "component": "k:src/B.java", "message": "x"},
        ]
        return {"issues": items if page == 1 else [], "paging": {"total": 2}}
    if path == "/api/qualitygates/project_status":
        return {"projectStatus": {"status": "ERROR", "conditions": [
            {"metricKey": "new_violations", "comparator": "GT", "errorThreshold": "30",
             "actualValue": "41", "status": "ERROR"}]}}
    if path == "/api/measures/component_tree":
        def comp(p, a, b):
            return {"path": p, "key": "k:" + p, "measures": [
                {"metric": "uncovered_lines", "value": str(a)},
                {"metric": "uncovered_conditions", "value": str(b)}]}
        return {"components": [comp("src/A.java", 2, 1), comp("src/B.java", 9, 0),
                               comp("src/C.java", 0, 0)], "paging": {"total": 3}}
    if path == "/api/hotspots/search":
        return {"hotspots": [{"ruleKey": "java:S5122", "vulnerabilityProbability": "MEDIUM",
                              "component": "k:src/A.java", "line": 7, "message": "CORS"}],
                "paging": {"total": 1}}
    return {}


sf.http_get = fake_get


def run(*argv, env=None):
    CALLS.clear()
    base = {"GENIUS_SONAR_TOKEN_FILE": TOKEN_FILE, "GENIUS_SONAR_PROJECT": "k",
            "GENIUS_SONAR_URL": None}
    base.update(env or {})
    res = testkit.call_main(sf.main, argv=["sonar_fetch.py"] + list(argv), env=base)
    return res.returncode, res.stdout, res.stderr


def case_buyruqlar():
    rc_i, out_i, _ = run("issues")
    rc_g, out_g, _ = run("gate")
    rc_c, out_c, _ = run("coverage")
    rc_h, out_h, _ = run("hotspots")
    cov = out_c.strip().split("\n")
    return [
        ("issues: sarlavha va rule bo'yicha tartib",
         rc_i == 0 and out_i.split("\n")[0].startswith("kalit\t")
         and out_i.split("\n")[1].startswith("java:S1068\t")),
        ("issues: xabar bir qatorga keltirildi, fayl prefiksi olib tashlandi",
         "java:S1128\tMINOR\tCODE_SMELL\tsrc/A.java\t3\tRemove this import" in out_i),
        ("gate: holat va shart", rc_g == 0 and "holat\tERROR" in out_g
         and "new_violations\tGT\t30\t41\tERROR" in out_g),
        ("coverage: eng ko'pi birinchi, qoplanganlari yo'q",
         rc_c == 0 and cov[1].startswith("src/B.java\t9\t0") and len(cov) == 3
         and "C.java" not in out_c),
        ("hotspots: TO_REVIEW qatori", rc_h == 0 and "java:S5122\tMEDIUM\tsrc/A.java\t7\tCORS" in out_h),
    ]


def case_token():
    run("gate")
    url, sent = CALLS[0]
    _, out, err = run("issues")
    out_file = os.path.join(TMP, "out.tsv")
    _, out_f, err_f = run("issues", "--chiqish", out_file)
    return [
        ("token fayldan o'qilib yuboriladi", sent == TOKEN),
        ("birinchi so'rov sukut serverga", url.startswith("https://sonar.mbabm.uz/")),
        ("token chiqishga tushmaydi", TOKEN not in out + err + out_f + err_f),
        ("--chiqish faylga yozadi", os.path.exists(out_file)
         and "java:S1128" in open(out_file, encoding="utf-8").read()),
        ("token URL da emas", all(TOKEN not in u for u, _ in CALLS)),
    ]


def case_sozlama():
    rc_url, _, _ = run("gate", env={"GENIUS_SONAR_URL": "https://boshqa.example/"})
    boshqa = CALLS[0][0]
    rc_np, _, err_np = run("gate", env={"GENIUS_SONAR_PROJECT": None})
    rc_nt, _, err_nt = run("gate", env={"GENIUS_SONAR_TOKEN_FILE": os.path.join(TMP, "yoq")})
    rc_arg, _, _ = run("gate", "--loyiha", "boshqa-kalit", env={"GENIUS_SONAR_PROJECT": None})
    return [
        ("GENIUS_SONAR_URL ishlatiladi", rc_url == 0 and boshqa.startswith("https://boshqa.example/api/")),
        ("loyiha yo'q: rc 2", rc_np == 2 and "project key" in err_np),
        ("token fayli yo'q: rc 2, qiymatsiz xabar", rc_nt == 2 and "token fayli" in err_nt
         and TOKEN not in err_nt),
        ("--loyiha muhitsiz ishlaydi", rc_arg == 0 and "projectKey=boshqa-kalit" in CALLS[0][0]),
    ]


def case_tarmoq():
    def broken(url, token):
        raise sf.Network("URLError: %s" % url.split("?")[0])
    saved = sf.http_get
    sf.http_get = broken
    try:
        rc, out, err = run("issues")
    finally:
        sf.http_get = saved
    headers = base64.b64encode((TOKEN + ":").encode()).decode()
    return [("tarmoq xatosi: rc 3 va qiymatsiz xabar",
             rc == 3 and "tarmoq" in err and TOKEN not in err and headers not in err)]


SECTIONS = [
    ("Buyruqlar", case_buyruqlar),
    ("Token", case_token),
    ("Sozlama", case_sozlama),
    ("Tarmoq xatosi", case_tarmoq),
]


def main(argv=()):
    return testkit.run_cases(SECTIONS, argv, headers=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
