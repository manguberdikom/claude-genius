#!/usr/bin/env python3
"""Lokal SonarQube da push dan oldin bir marta tez tahlil (asosiy server bilan bir xil natija).

    python3 tools/sonar_local.py ishga [--yangila]
    python3 tools/sonar_local.py sozla [--loyiha KEY]
    python3 tools/sonar_local.py tahlil [--loyiha KEY] [--testlar]
    python3 tools/sonar_local.py moslik [--loyiha KEY]
    python3 tools/sonar_local.py solishtir [--loyiha KEY]

ishga      konteyner `sonar-local` bor va ishlayaptimi: yo'q bo'lsa asosiy
           server versiyasi bilan yaratadi, to'xtagan bo'lsa `docker start`,
           `UP` gacha kutadi (180 s). Versiya mos kelmasa ogohlantiradi;
           `--yangila` konteynerni yangi image bilan qayta yaratadi (volume
           saqlanadi). Docker faqat konteyner YO'Q, to'xtagan yoki `--yangila`
           bo'lsa chaqiriladi va bu oldindan bir qator bilan aytiladi:
           `guard.py` subprocess ichidagi docker ni ko'rmaydi, shuning uchun
           birinchi marta foydalanuvchi roziligi bilan ishga tushiriladi.
sozla      parol, GLOBAL_ANALYSIS_TOKEN (holat ~/.sonar-local.json, 0600),
           asosiy serverdagi maxsus profillar (backup/restore) va gate shartlari.
           Idempotent: o'zgarmagan narsaga tegmaydi.
tahlil     ishga + sozla, keyin Gradle (`sonar`) yoki Maven (`sonar:sonar`),
           CE vazifasini kutish, hotspot statusini asosiy serverdan ko'chirish
           va natija: ochiq issue, TO_REVIEW hotspot, gate, coverage.
           Chiqish kodi: 0 gate OK va topilma yo'q, 1 topilma bor, 2 sozlama
           yoki konteyner xatosi.
           Coverage to'liq bo'lishi uchun avval unit va integration testlar
           jacoco bilan yurgan bo'lishi kerak (build/jacoco/*.exec). Exec
           manbadan eski bo'lsa asbob aytadi; `--testlar` testlarni ham yurgizadi.
moslik     konfiguratsiya farqini topib tuzatadi (server versiyasi, plugin, profil
           qoidalari hash i, gate, loyiha sozlamalari, new code davri, qo'lda
           qo'yilgan hotspot va issue statuslari) va nimani tuzatganini bir
           qatorda aytadi; ko'rinmaydigan narsa "tekshirib bo'lmadi" deyiladi.
           `tahlil` boshida avtomatik yuradi.
solishtir  asosiy server va lokal: issue, hotspot, metrikalar. Chiqish kodi:
           0 bir xil, 1 bir xil commit da farq bor, 3 commit mos emas (farq
           kutilgan, ishonchli xulosa yo'q).

Loyiha kaliti: `--loyiha`, `GENIUS_SONAR_PROJECT`, bo'lmasa `origin` remote dan
slug (`group/sub/repo` -> `group-sub-repo`) + `-` + joriy branch.

Sozlama (qiymat kodda yo'q, muhitdan):

    GENIUS_SONAR_URL         asosiy server (sonar_fetch.py bilan umumiy)
    GENIUS_SONAR_TOKEN_FILE  asosiy server tokeni fayli (sonar_fetch.py bilan umumiy)
    GENIUS_SONAR_LOCAL_URL   lokal server, sukut http://localhost:9000
    GENIUS_SONAR_LOCAL_STATE holat fayli, sukut ~/.sonar-local.json

Token va parol hech qayerga chop etilmaydi.
"""

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sonar_fetch  # noqa: E402

CONTAINER = "sonar-local"
DEFAULT_LOCAL = "http://localhost:9000"
PLUGIN_VERSION = "7.5.0.8588"
UP_TIMEOUT = 180
CE_TIMEOUT = 600
SCAN_TIMEOUT = 1500
TEST_SCAN_TIMEOUT = 2400
SKIP_DIRS = {".git", ".gradle", "build", "target", "out", "bin", "node_modules",
             ".idea", ".vscode", ".mvn", ".claude"}
SOURCE_EXT = (".java", ".kt", ".groovy", ".xml", ".yml", ".yaml", ".properties", ".sql")
METRICS = ("ncloc,lines,files,classes,functions,statements,coverage,line_coverage,"
           "branch_coverage,lines_to_cover,uncovered_lines,conditions_to_cover,"
           "uncovered_conditions,duplicated_blocks,duplicated_lines,violations,"
           "code_smells,bugs,vulnerabilities,security_hotspots,cognitive_complexity,"
           "alert_status")
INIT_SCRIPT = """initscript {
    repositories { gradlePluginPortal() }
    dependencies { classpath "org.sonarsource.scanner.gradle:sonarqube-gradle-plugin:%s" }
}
rootProject {
    apply plugin: org.sonarqube.gradle.SonarQubePlugin
}
""" % PLUGIN_VERSION


class Fail(Exception):
    """Sozlama, konteyner yoki tarmoq xatosi: chiqish kodi 2."""


def say(text):
    print(text, flush=True)


# -- sozlama -----------------------------------------------------------------

def local_url():
    return os.environ.get("GENIUS_SONAR_LOCAL_URL", "").strip().rstrip("/") or DEFAULT_LOCAL


def state_path():
    given = os.environ.get("GENIUS_SONAR_LOCAL_STATE", "").strip()
    return os.path.expanduser(given or "~/.sonar-local.json")


def load_state():
    try:
        with open(state_path(), encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(state):
    path = state_path()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(state, handle)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


# -- loyiha kaliti -----------------------------------------------------------

def remote_slug(url):
    """`https://h/g/s/r.git`, `git@h:g/s/r.git`, `ssh://git@h:22/g/s/r` -> `g-s-r`."""
    text = (url or "").strip().rstrip("/")
    if text.endswith(".git"):
        text = text[:-4]
    if "://" in text:
        path = urllib.parse.urlparse(text).path
    elif ":" in text:
        path = text.split(":", 1)[1]
    else:
        path = text
    parts = [p for p in path.split("/") if p]
    return "-".join(parts)


def clean_key(text):
    return re.sub(r"[^A-Za-z0-9_.:-]+", "-", text).strip("-")


def project_key(origin_url, branch):
    slug = remote_slug(origin_url)
    if not slug or not branch or branch == "HEAD":
        return ""
    return clean_key("%s-%s" % (slug, branch))


def git_out(root, *args):
    try:
        done = subprocess.run(["git", "-C", root] + list(args), capture_output=True,
                              text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return ""
    return done.stdout.strip() if done.returncode == 0 else ""


def resolve_key(given, root):
    key = (given or os.environ.get("GENIUS_SONAR_PROJECT", "")).strip()
    if key:
        return key
    key = project_key(git_out(root, "remote", "get-url", "origin"),
                      git_out(root, "rev-parse", "--abbrev-ref", "HEAD"))
    if not key:
        raise Fail("loyiha kaliti topilmadi: --loyiha yoki GENIUS_SONAR_PROJECT "
                   "(origin remote yoki branch yo'q)")
    return key


# -- HTTP --------------------------------------------------------------------

def api(base, path, auth, data=None, raw=False, ctype=None):
    """Sonar API. `auth` = 'login:parol' yoki 'token:'. HTTP/tarmoq xatosi Fail."""
    body = urllib.parse.urlencode(data, doseq=True).encode() if isinstance(data, dict) else data
    request = urllib.request.Request(base + path, data=body,
                                     method="POST" if data is not None else "GET")
    if auth:
        request.add_header("Authorization",
                           "Basic " + base64.b64encode(auth.encode()).decode())
    if ctype:
        request.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
    except urllib.error.HTTPError as err:
        raise Fail("HTTP %d: %s%s" % (err.code, base.split("//")[-1], path.split("?")[0]))
    except (urllib.error.URLError, OSError, ValueError) as err:
        raise Fail("%s: %s%s" % (type(err).__name__, base.split("//")[-1], path.split("?")[0]))
    if raw:
        return payload
    return json.loads(payload) if payload else {}


def multipart(file_field, filename, content):
    boundary = "----genius" + secrets.token_hex(8)
    head = ("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n"
            "Content-Type: application/xml\r\n\r\n" % (boundary, file_field, filename)).encode()
    tail = ("\r\n--%s--\r\n" % boundary).encode()
    return head + content + tail, "multipart/form-data; boundary=" + boundary


class Remote:
    """Asosiy server: faqat o'qish."""

    def __init__(self):
        self.base = sonar_fetch.base_url()
        self.auth = sonar_fetch.read_token() + ":"

    def get(self, path, raw=False):
        return api(self.base, path, self.auth, raw=raw)


def remote_version():
    """Asosiy server versiyasi (`/api/system/status` ochiq, token kerak emas)."""
    return api(sonar_fetch.base_url(), "/api/system/status", None).get("version", "")


def local_status():
    """Lokal server holati (`UP`, `STARTING`, ...) yoki '' agar javob yo'q."""
    try:
        return api(local_url(), "/api/system/status", None).get("status", "")
    except Fail:
        return ""


def local_version():
    try:
        return api(local_url(), "/api/system/status", None).get("version", "")
    except Fail:
        return ""


# -- docker (ishga) ----------------------------------------------------------

def docker(*args):
    """(kod, chiqish). Docker yo'q bo'lsa Fail."""
    try:
        done = subprocess.run(["docker"] + list(args), capture_output=True, text=True,
                              timeout=900)
    except FileNotFoundError:
        raise Fail("docker topilmadi: lokal SonarQube uchun Docker kerak")
    except (OSError, subprocess.SubprocessError) as err:
        raise Fail("docker ishlamadi (%s)" % type(err).__name__)
    return done.returncode, (done.stdout or "") + (done.stderr or "")


def parse_docker_ps(text):
    """`docker ps -a --format '{{.Names}}\\t{{.Status}}\\t{{.Image}}'` -> {'running', 'image', 'status'} yoki None."""
    for line in text.splitlines():
        cols = line.split("\t")
        if len(cols) >= 3 and cols[0].strip() == CONTAINER:
            return {"running": cols[1].strip().startswith("Up"),
                    "status": cols[1].strip(), "image": cols[2].strip()}
    return None


def image_version(image):
    match = re.search(r":(\d[\w.]*?)(?:-community)?$", image or "")
    return match.group(1) if match else ""


def image_name(version):
    return "sonarqube:%s-community" % version


def run_args(version):
    port = urllib.parse.urlparse(local_url()).port or 9000
    return ["run", "-d", "--name", CONTAINER, "--restart", "unless-stopped",
            "-p", "%d:9000" % port,
            "-e", "SONAR_SEARCH_JAVAADDITIONALOPTS=-Dnode.store.allow_mmap=false",
            "-e", "SONAR_TELEMETRY_ENABLE=false",
            "-v", "sonar_local_data:/opt/sonarqube/data",
            "-v", "sonar_local_ext:/opt/sonarqube/extensions",
            "-v", "sonar_local_logs:/opt/sonarqube/logs",
            image_name(version)]


def wait_up(timeout=UP_TIMEOUT):
    started = time.time()
    while time.time() - started < timeout:
        if local_status() == "UP":
            return int(time.time() - started)
        time.sleep(3)
    raise Fail("lokal SonarQube %d s ichida UP bo'lmadi (docker logs %s)" % (timeout, CONTAINER))


def ensure_running(update=False):
    """Konteynerni tayyorlaydi. (xulosa, ogohlantirishlar) qaytaradi."""
    notes = []
    try:
        wanted = remote_version()
    except Fail as err:
        wanted = ""
        notes.append("asosiy server versiyasi olinmadi (%s)" % err)
    if local_status() == "UP" and not update:
        have = local_version()
        if wanted and have and have != wanted:
            notes.append("versiya mos emas: lokal %s, server %s (--yangila)" % (have, wanted))
        return "tayyor (UP, %s)" % (have or "?"), notes
    code, out = docker("ps", "-a", "--format", "{{.Names}}\t{{.Status}}\t{{.Image}}")
    if code != 0:
        raise Fail("docker javob bermadi (Docker Desktop ishlayaptimi?): %s" % out.strip()[:120])
    found = parse_docker_ps(out)
    if update and not wanted:
        raise Fail("--yangila uchun asosiy server versiyasi kerak")
    if found is None or update:
        if not wanted:
            raise Fail("konteyner yo'q va asosiy server versiyasi noma'lum")
        if found is not None:
            say("ishga: docker rm -f %s va qayta yaratish (volume saqlanadi)" % CONTAINER)
            docker("rm", "-f", CONTAINER)
        else:
            say("ishga: docker run %s (yangi konteyner, image yuklanishi mumkin)" % image_name(wanted))
        code, out = docker(*run_args(wanted))
        if code != 0:
            raise Fail("docker run yiqildi: %s" % out.strip()[:200])
        action = "yaratildi"
    else:
        have = image_version(found["image"])
        if wanted and have and have != wanted:
            notes.append("versiya mos emas: konteyner %s, server %s (--yangila)" % (have, wanted))
        if found["running"]:
            action = "ishlayapti"
        else:
            say("ishga: docker start %s (to'xtagan konteyner)" % CONTAINER)
            code, out = docker("start", CONTAINER)
            if code != 0:
                raise Fail("docker start yiqildi: %s" % out.strip()[:200])
            action = "ishga tushirildi"
    waited = wait_up()
    return "%s, UP (%d s)" % (action, waited), notes


def cmd_ishga(args):
    summary, notes = ensure_running(update=args.yangila)
    for note in notes:
        say("ishga: ogohlantirish: " + note)
    say("sonar_local: ishga: " + summary)
    return 0


# -- sozla -------------------------------------------------------------------

def conditions_of(gate):
    return sorted((c["metric"], c["op"], str(c.get("error", ""))) for c in gate.get("conditions", []))


def ensure_password_and_token(state):
    """Parol va GLOBAL_ANALYSIS_TOKEN. `state` yangilanadi, o'zgarsa True."""
    base, changed = local_url(), False
    if "password" in state:
        try:
            api(base, "/api/user_tokens/search", "admin:" + state["password"])
        except Fail as err:
            if "HTTP 401" not in str(err):
                raise
            state.clear()   # hajm tozalangan: holat eskirgan
    if "password" not in state:
        password = "G" + secrets.token_urlsafe(18) + "9!"
        api(base, "/api/users/change_password", "admin:admin",
            {"login": "admin", "previousPassword": "admin", "password": password})
        state["password"] = password
        changed = True
    admin = "admin:" + state["password"]
    names = {t.get("name") for t in api(base, "/api/user_tokens/search", admin).get("userTokens", [])}
    if "token" not in state or state.get("token_name") not in names:
        name = "genius-%d" % int(time.time())
        state["token"] = api(base, "/api/user_tokens/generate", admin,
                             {"name": name, "type": "GLOBAL_ANALYSIS_TOKEN"})["token"]
        state["token_name"] = name
        changed = True
    return admin, changed


def sync_profiles(remote, admin, key, state):
    """Asosiy serverdagi maxsus profillarni lokalga ko'chiradi. Ko'chirilganlar soni."""
    base = local_url()
    try:
        listing = remote.get("/api/qualityprofiles/search?project=" + urllib.parse.quote(key))
    except Fail:
        listing = remote.get("/api/qualityprofiles/search?defaults=true")
    seen, moved = state.setdefault("profiles", {}), 0
    for prof in listing.get("profiles", []):
        if prof.get("isBuiltIn"):
            continue
        xml = remote.get("/api/qualityprofiles/backup?language=%s&qualityProfile=%s" % (
            prof["language"], urllib.parse.quote(prof["name"])), raw=True)
        digest = hashlib.sha256(xml).hexdigest()
        tag = "%s:%s" % (prof["language"], prof["name"])
        if seen.get(tag) == digest:
            continue
        body, ctype = multipart("backup", "profile.xml", xml)
        api(base, "/api/qualityprofiles/restore", admin, body, ctype=ctype)
        api(base, "/api/qualityprofiles/set_default", admin,
            {"language": prof["language"], "qualityProfile": prof["name"]})
        seen[tag] = digest
        moved += 1
    return moved


def sync_gate(remote, admin, key):
    """Asosiy serverdagi gate shartlari lokalga. Yangilanganmi (bool) va nomi."""
    base = local_url()
    try:
        name = remote.get("/api/qualitygates/get_by_project?project=" + urllib.parse.quote(key))["qualityGate"]["name"]
    except Fail:
        gates = remote.get("/api/qualitygates/list")["qualitygates"]
        name = next(g["name"] for g in gates if g.get("isDefault"))
    source = remote.get("/api/qualitygates/show?name=" + urllib.parse.quote(name))
    local_names = {g["name"] for g in api(base, "/api/qualitygates/list", admin)["qualitygates"]}
    if name not in local_names:
        api(base, "/api/qualitygates/create", admin, {"name": name})
    existing = api(base, "/api/qualitygates/show?name=" + urllib.parse.quote(name), admin)
    updated = False
    if not source.get("isBuiltIn") and conditions_of(existing) != conditions_of(source):
        for cond in existing.get("conditions", []):
            api(base, "/api/qualitygates/delete_condition", admin, {"id": cond["id"]})
        for cond in source.get("conditions", []):
            api(base, "/api/qualitygates/create_condition", admin,
                {"gateName": name, "metric": cond["metric"], "op": cond["op"],
                 "error": cond["error"]})
        updated = True
    api(base, "/api/qualitygates/set_as_default", admin, {"name": name})
    return updated, name, len(source.get("conditions", []))


def do_sozla(key):
    try:
        remote = Remote()
    except sonar_fetch.Config as err:
        raise Fail(str(err))
    state = load_state()
    admin, changed = ensure_password_and_token(state)
    moved = sync_profiles(remote, admin, key, state)
    updated, gate_name, count = sync_gate(remote, admin, key)
    save_state(state)
    parts = ["parol/token " + ("yangilandi" if changed else "bor"),
             "profil ko'chirildi %d" % moved,
             "gate %s (%d shart%s)" % (gate_name, count, ", yangilandi" if updated else "")]
    return ", ".join(parts)


def cmd_sozla(args):
    key = resolve_key(args.loyiha, os.getcwd())
    say("sonar_local: sozla: " + do_sozla(key))
    return 0


# -- moslik: server va lokal konfiguratsiyasi bir xil ---------------------------

BLOCKED_SETTINGS = ("sonar.auth.", "sonar.forceAuthentication", "email.", "sonar.core.",
                    "sonar.server.", "sonar.plugins.", "sonar.dbcleaner.")
NEW_CODE_TYPES = ("PREVIOUS_VERSION", "NUMBER_OF_DAYS")


def rules_signature(actives, profile_key):
    """Profildagi faol qoidalar: (qoida, severity, params) ro'yxati hash i va soni.
    `actives` = /api/rules/search javobidagi {qoida: [{qProfile, severity, params}]}."""
    rows = []
    for rule, items in actives.items():
        for item in items:
            if item.get("qProfile") == profile_key:
                params = sorted((p["key"], str(p.get("value", ""))) for p in item.get("params", []))
                rows.append((rule, item.get("severity", ""), params))
    return hashlib.sha256(repr(sorted(rows)).encode()).hexdigest()[:16], len(rows)


def profile_signature(base, auth, profile_key):
    actives, page = {}, 1
    while True:
        data = api(base, "/api/rules/search?qprofile=%s&activation=true&ps=500&p=%d" % (
            urllib.parse.quote(profile_key), page), auth)
        actives.update(data.get("actives", {}))
        if page * 500 >= data.get("total", 0):
            return rules_signature(actives, profile_key)
        page += 1


def plugins_diff(remote_plugins, local_plugins):
    remote = {p["key"]: p.get("version", "") for p in remote_plugins}
    local = {p["key"]: p.get("version", "") for p in local_plugins}
    return ["%s: server %s, lokal %s" % (k, remote[k], local.get(k, "yo'q"))
            for k in sorted(remote) if remote[k] != local.get(k)]


def normalise_setting(item):
    if "fieldValues" in item:
        return json.dumps(item["fieldValues"], sort_keys=True)
    if "values" in item:
        return json.dumps(item["values"])
    return str(item.get("value", ""))


def own_settings(listing):
    """Loyihaning o'z (meros emas) ko'rinadigan sozlamalari: {kalit: element}."""
    return {s["key"]: s for s in listing
            if not s.get("inherited", False) and not s["key"].startswith(BLOCKED_SETTINGS)}


def settings_plan(remote_listing, local_listing):
    """(qo'yiladiganlar [element], tiklanadigan kalitlar [kalit])."""
    remote, local = own_settings(remote_listing), own_settings(local_listing)
    to_set = [remote[k] for k in sorted(remote)
              if k not in local or normalise_setting(remote[k]) != normalise_setting(local[k])]
    to_reset = sorted(k for k in local if k not in remote)
    return to_set, to_reset


def setting_payload(project, item):
    data = {"key": item["key"], "component": project}
    if "fieldValues" in item:
        data["fieldValues"] = [json.dumps(v) for v in item["fieldValues"]]
    elif "values" in item:
        data["values"] = list(item["values"])
    else:
        data["value"] = item.get("value", "")
    return data


def new_code_action(remote, local):
    """None (teng), ('set', tur, qiymat) yoki ('note', matn)."""
    if (remote.get("type"), remote.get("value")) == (local.get("type"), local.get("value")):
        return None
    if remote.get("type") not in NEW_CODE_TYPES:
        return ("note", "new code davri turi %s lokalga qo'yilmaydi" % remote.get("type"))
    return ("set", remote["type"], remote.get("value", ""))


def match_issues(remote_issues, local_open):
    """Asosiy serverda qo'lda ACCEPTED/FALSE_POSITIVE qilingan issue lar:
    [(lokal kalit, o'tish)]. Moslik: qoida + fayl + qator."""
    transitions = {"ACCEPTED": "accept", "FALSE_POSITIVE": "falsepositive"}
    by_ident = {}
    for i in remote_issues:
        status = i.get("issueStatus") or i.get("status")
        if status in transitions:
            by_ident[(i["rule"], i["component"].split(":", 1)[1], i.get("line"))] = transitions[status]
    out = []
    for i in local_open:
        move = by_ident.get((i["rule"], i["component"].split(":", 1)[1], i.get("line")))
        if move:
            out.append((i["key"], move))
    return out


def ensure_project(admin, key):
    base = local_url()
    if not api(base, "/api/projects/search?projects=" + urllib.parse.quote(key), admin).get("components"):
        api(base, "/api/projects/create", admin, {"project": key, "name": key})
        return True
    return False


def restore_profile(remote, admin, prof, state):
    xml = remote.get("/api/qualityprofiles/backup?language=%s&qualityProfile=%s" % (
        prof["language"], urllib.parse.quote(prof["name"])), raw=True)
    body, ctype = multipart("backup", "profile.xml", xml)
    api(local_url(), "/api/qualityprofiles/restore", admin, body, ctype=ctype)
    api(local_url(), "/api/qualityprofiles/set_default", admin,
        {"language": prof["language"], "qualityProfile": prof["name"]})
    state.setdefault("profiles", {})["%s:%s" % (prof["language"], prof["name"])] = hashlib.sha256(xml).hexdigest()


def local_profile(admin, prof):
    listing = api(local_url(), "/api/qualityprofiles/search?language=" + prof["language"], admin)["profiles"]
    return next((p for p in listing if p["name"] == prof["name"]), None)


def check_profiles(remote, admin, key, state, fixed, unchecked):
    """Qoida darajasida tekshiruv: server va lokal profil hash i teng bo'lishi shart."""
    base = local_url()
    try:
        listing = remote.get("/api/qualityprofiles/search?project=" + urllib.parse.quote(key))
    except Fail:
        listing = remote.get("/api/qualityprofiles/search?defaults=true")
    for prof in listing.get("profiles", []):
        mine = local_profile(admin, prof)
        label = "%s/%s" % (prof["language"], prof["name"])
        if mine is None:
            unchecked.append("profil %s lokalda yo'q" % label)
            continue
        want = profile_signature(remote.base, remote.auth, prof["key"])
        have = profile_signature(base, admin, mine["key"])
        if want == have:
            continue
        if not prof.get("isBuiltIn"):
            restore_profile(remote, admin, prof, state)
            mine = local_profile(admin, prof) or mine
            have = profile_signature(base, admin, mine["key"])
            if want == have:
                fixed.append("profil %s qayta tiklandi" % label)
                continue
        unchecked.append("profil %s qoidalari farq (server %d, lokal %d qoida)%s" % (
            label, want[1], have[1], " [built-in: versiya farqi]" if prof.get("isBuiltIn") else ""))


def do_moslik(key):
    """Konfiguratsiyani tenglashtiradi. (tuzatilgan, tekshirib_bo'lmagan)."""
    fixed, unchecked = [], []
    try:
        remote = Remote()
    except sonar_fetch.Config as err:
        raise Fail(str(err))
    try:
        want, have = remote_version(), local_version()
    except Fail as err:
        want = have = ""
        unchecked.append("server versiyasi (%s)" % err)
    if want and have and want != have:
        say("moslik: versiya %s -> %s: konteyner qayta yaratiladi" % (have, want))
        ensure_running(update=True)
        fixed.append("server versiyasi %s -> %s" % (have, want))
    state = load_state()
    admin, changed = ensure_password_and_token(state)
    if changed:
        fixed.append("parol/token")
    moved = sync_profiles(remote, admin, key, state)
    if moved:
        fixed.append("profil ko'chirildi %d" % moved)
    updated, _, _ = sync_gate(remote, admin, key)
    if updated:
        fixed.append("gate shartlari")
    check_profiles(remote, admin, key, state, fixed, unchecked)
    try:
        diff = plugins_diff(remote.get("/api/plugins/installed").get("plugins", []),
                            api(local_url(), "/api/plugins/installed", admin).get("plugins", []))
        if diff:
            unchecked.append("plugin farqi (qo'lda o'rnatiladi): " + "; ".join(diff[:3]))
    except Fail as err:
        unchecked.append("plugin versiyalari (%s)" % err)
    if ensure_project(admin, key):
        fixed.append("loyiha lokalda yaratildi")
    try:
        r_set = remote.get("/api/settings/values?component=" + urllib.parse.quote(key)).get("settings", [])
        l_set = api(local_url(), "/api/settings/values?component=" + urllib.parse.quote(key),
                    admin).get("settings", [])
        to_set, to_reset = settings_plan(r_set, l_set)
        for item in to_set:
            api(local_url(), "/api/settings/set", admin, setting_payload(key, item))
        if to_reset:
            api(local_url(), "/api/settings/reset", admin, {"keys": ",".join(to_reset), "component": key})
        if to_set or to_reset:
            fixed.append("loyiha sozlamasi %d qo'yildi, %d tiklandi" % (len(to_set), len(to_reset)))
    except Fail as err:
        unchecked.append("loyiha sozlamalari (%s)" % err)
    try:
        r_nc = remote.get("/api/new_code_periods/show?project=" + urllib.parse.quote(key))
        l_nc = api(local_url(), "/api/new_code_periods/show?project=" + urllib.parse.quote(key), admin)
        act = new_code_action(r_nc, l_nc)
        if act and act[0] == "set":
            data = {"project": key, "type": act[1]}
            if act[2]:
                data["value"] = act[2]
            api(local_url(), "/api/new_code_periods/set", admin, data)
            fixed.append("new code davri %s" % act[1])
        elif act:
            unchecked.append(act[1])
    except Fail as err:
        unchecked.append("new code davri (%s)" % err)
    unchecked.append("scanner konteksti (JDK, env) ko'rinmaydi")
    state["moslik"] = {"vaqt": time.strftime("%Y-%m-%dT%H:%M:%S"), "server": want or have}
    save_state(state)
    return fixed, unchecked


def sync_statuses(remote, admin, key):
    """Qo'lda qo'yilgan issue (ACCEPTED/FALSE_POSITIVE) va hotspot statuslari. (issue, hotspot, izoh)."""
    moved_hot, _, note = sync_hotspots(remote, admin, key)
    r_issues, page = [], 1
    try:
        while True:
            data = remote.get("/api/issues/search?componentKeys=%s&issueStatuses=ACCEPTED,FALSE_POSITIVE"
                              "&ps=500&p=%d" % (urllib.parse.quote(key), page))
            r_issues += data.get("issues", [])
            if page * 500 >= data.get("paging", {}).get("total", 0):
                break
            page += 1
    except Fail as err:
        return 0, moved_hot, note or "issue statuslari olinmadi (%s)" % err
    moves = match_issues(r_issues, open_issues(local_url(), admin, key))
    for issue, transition in moves:
        api(local_url(), "/api/issues/do_transition", admin, {"issue": issue, "transition": transition})
    return len(moves), moved_hot, note


def moslik_line(fixed, unchecked):
    parts = ["tuzatildi: " + ", ".join(fixed) if fixed else "farq yo'q"]
    if unchecked:
        parts.append("tekshirib bo'lmadi: " + "; ".join(unchecked))
    return "moslik: " + ". ".join(parts)


def cmd_moslik(args):
    key = resolve_key(args.loyiha, os.getcwd())
    summary, notes = ensure_running()
    fixed, unchecked = do_moslik(key)
    state = load_state()
    try:
        n_issue, n_hot, note = sync_statuses(Remote(), "admin:" + state["password"], key)
        if n_issue or n_hot:
            fixed.append("status: issue %d, hotspot %d" % (n_issue, n_hot))
        if note:
            unchecked.append(note)
    except (Fail, sonar_fetch.Config) as err:
        unchecked.append("statuslar (%s)" % err)
    say("sonar_local: " + moslik_line(fixed, unchecked))
    return 0


# -- tahlil ------------------------------------------------------------------

def read_report_task(text):
    """`report-task.txt` (key=value) -> dict."""
    out = {}
    for line in text.splitlines():
        if "=" in line:
            name, value = line.split("=", 1)
            out[name.strip()] = value.strip()
    return out


def wrapper_command(root, tool):
    """Wrapper bo'lsa u, bo'lmasa PATH dagi asbob (run_tests.Tests._runner bilan bir xil qoida)."""
    wrapper, fallback = ("gradlew", "gradle") if tool == "gradle" else ("mvnw", "mvn")
    if os.name == "nt":
        script = wrapper + (".bat" if tool == "gradle" else ".cmd")
        if os.path.exists(os.path.join(root, script)):
            return ["cmd", "/c", script]
        return ["cmd", "/c", fallback]
    path = os.path.join(root, wrapper)
    if os.path.exists(path):
        return ["./" + wrapper] if os.access(path, os.X_OK) else ["sh", wrapper]
    return [fallback]


def scan_env(token):
    """Gradle/Maven uchun muhit: token faqat env da, Windows wrapper yechimi."""
    # Windows da kalit katta harfga o'tadi: nomi kichik-katta farqsiz olib tashlanadi,
    # aks holda `cmd /c gradlew.bat` joriy papkadan topilmaydi.
    env = {k: v for k, v in os.environ.items() if k.lower() != "nodefaultcurrentdirectoryinexepath"}
    env["SONAR_TOKEN"] = token
    return env


def mentions_task(root, task):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in ("build.gradle", "build.gradle.kts") or current.endswith("buildSrc"):
                try:
                    with open(os.path.join(current, name), encoding="utf-8", errors="ignore") as h:
                        if task in h.read():
                            return True
                except OSError:
                    pass
    return False


def build_command(root, tool, key, name, with_tests, init_path):
    runner = wrapper_command(root, tool)
    host = "-Dsonar.host.url=" + local_url()
    ident = ["-Dsonar.projectKey=" + key, "-Dsonar.projectName=" + name]
    if tool == "gradle":
        has_it = mentions_task(root, "integrationTest")
        if with_tests:
            tasks = ["test"] + (["integrationTest"] if has_it else []) + ["jacocoTestReport", "sonar"]
        else:
            tasks = ["sonar", "-x", "test"] + (["-x", "integrationTest"] if has_it else [])
        return runner + tasks + ["-I", init_path, host] + ident + ["--console=plain"]
    goals = ["verify"] if with_tests else []
    flags = [] if with_tests else ["-DskipTests"]
    return (runner + ["-B"] + flags + goals
            + ["org.sonarsource.scanner.maven:sonar-maven-plugin:sonar", host] + ident)


def report_task_path(root, tool):
    return os.path.join(root, "build" if tool == "gradle" else "target", "sonar", "report-task.txt")


def newest_mtime(root, exts=SOURCE_EXT):
    newest = 0.0
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if "/src/" not in current.replace(os.sep, "/") + "/":
            continue
        for name in files:
            if name.endswith(exts):
                try:
                    newest = max(newest, os.path.getmtime(os.path.join(current, name)))
                except OSError:
                    pass
    return newest


def find_exec(root):
    found = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS - {"build"}]
        if os.path.basename(current) == "build":
            dirs[:] = [d for d in dirs if d == "jacoco"]
        if current.replace(os.sep, "/").endswith("build/jacoco"):
            found += [os.path.join(current, f) for f in files if f.endswith(".exec")]
            dirs[:] = []
    return found


def exec_state(exec_mtimes, source_mtime):
    """'yo'q' | 'eskirgan' | 'yangi'. Eng eski exec eng yangi manbadan eski bo'lsa eskirgan."""
    if not exec_mtimes:
        return "yo'q"
    return "eskirgan" if min(exec_mtimes) < source_mtime else "yangi"


def versions_match(have, wanted):
    return not have or not wanted or have == wanted


def run_scan(cmd, root, token, log_path, timeout):
    with open(log_path, "w", encoding="utf-8") as log:
        try:
            done = subprocess.run(cmd, cwd=root, env=scan_env(token), stdout=log,
                                  stderr=subprocess.STDOUT, timeout=timeout)
        except FileNotFoundError:
            raise Fail("build buyrug'i topilmadi: %s" % cmd[0])
        except subprocess.TimeoutExpired:
            raise Fail("tahlil %d s ichida tugamadi (log: %s)" % (timeout, log_path))
    if done.returncode != 0:
        with open(log_path, encoding="utf-8", errors="replace") as log:
            tail = log.read().splitlines()[-12:]
        raise Fail("build yiqildi (rc %d), log %s:\n  %s" % (
            done.returncode, log_path, "\n  ".join(tail)))


def wait_ce(task_url, admin, timeout=CE_TIMEOUT):
    base = local_url()
    parsed = urllib.parse.urlparse(task_url)
    path = parsed.path + ("?" + parsed.query if parsed.query else "")
    started = time.time()
    while time.time() - started < timeout:
        status = api(base, path, admin).get("task", {}).get("status", "")
        if status == "SUCCESS":
            return
        if status in ("FAILED", "CANCELED"):
            raise Fail("Sonar hisoblash vazifasi %s" % status)
        time.sleep(2)
    raise Fail("Sonar hisoblash vazifasi %d s ichida tugamadi" % timeout)


def hotspot_ident(h):
    return h.get("ruleKey"), h["component"].split(":", 1)[1], h.get("line")


def match_hotspots(reviewed, to_review):
    """Asosiy serverdagi REVIEWED ro'yxati bo'yicha lokal TO_REVIEW hotspotlar:
    [(lokal kalit, resolution)]. Moslik: qoida + fayl + qator."""
    by_ident = {hotspot_ident(h): h for h in reviewed}
    out = []
    for h in to_review:
        src = by_ident.get(hotspot_ident(h))
        if src is not None:
            out.append((h["key"], src.get("resolution") or "SAFE"))
    return out


def hotspots_of(base, auth, key, status):
    out, page = [], 1
    while True:
        data = api(base, "/api/hotspots/search?projectKey=%s&status=%s&ps=500&p=%d" % (
            urllib.parse.quote(key), status, page), auth)
        out += data.get("hotspots", [])
        if page * 500 >= data.get("paging", {}).get("total", 0):
            return out
        page += 1


def sync_hotspots(remote, admin, key):
    """(ko'chirilgan, serverda REVIEWED, izoh)."""
    try:
        reviewed = hotspots_of(remote.base, remote.auth, key, "REVIEWED")
    except Fail as err:
        return 0, 0, "asosiy serverdan olinmadi (%s)" % err
    pending = hotspots_of(local_url(), admin, key, "TO_REVIEW")
    moves = match_hotspots(reviewed, pending)
    for hotspot, resolution in moves:
        api(local_url(), "/api/hotspots/change_status", admin,
            {"hotspot": hotspot, "status": "REVIEWED", "resolution": resolution,
             "comment": "asosiy serverdagi ko'rib chiqish statusi"})
    return len(moves), len(reviewed), ""


def open_issues(base, admin, key):
    out, page = [], 1
    while True:
        data = api(base, "/api/issues/search?componentKeys=%s&resolved=false&ps=500&p=%d" % (
            urllib.parse.quote(key), page), admin)
        out += data.get("issues", [])
        if page * 500 >= data.get("paging", {}).get("total", 0):
            return out
        page += 1


def verdict(gate_status, issue_count, hotspot_count):
    """Chiqish kodi: 0 gate OK va topilma yo'q, aks holda 1."""
    return 0 if gate_status == "OK" and issue_count == 0 and hotspot_count == 0 else 1


def short(text, limit=110):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


def cmd_tahlil(args):
    started = time.time()
    try:
        from run_tests import choose_tool, project_root
    except ImportError as err:
        raise Fail("run_tests.py import bo'lmadi: %s" % err)
    root = project_root(os.getcwd())
    tool, _, error = choose_tool(root)
    if error or tool is None:
        raise Fail(error or "build fayli yo'q (Gradle yoki Maven): %s" % root)
    key = resolve_key(args.loyiha, root)
    name = os.path.basename(root.rstrip("/\\")) or key
    say("tahlil: loyiha %s, build %s" % (key, tool))

    summary, notes = ensure_running()
    for note in notes:
        say("tahlil: ogohlantirish: " + note)
    say("tahlil: konteyner " + summary)
    fixed, unchecked = do_moslik(key)
    say("tahlil: " + moslik_line(fixed, unchecked))
    state = load_state()
    admin, token = "admin:" + state["password"], state["token"]
    remote = Remote()

    states = exec_state([os.path.getmtime(p) for p in find_exec(root)], newest_mtime(root))
    if states != "yangi" and not args.testlar:
        say("tahlil: ogohlantirish: jacoco exec %s: coverage to'liq emas. "
            "Avval `run_tests.py --hammasi --yurgiz`, yoki `--testlar` (~7.5 daqiqa)" % states)
    elif args.testlar:
        say("tahlil: --testlar: unit + integration testlar jacoco bilan yurgiziladi")

    folder = os.path.join(os.path.expanduser("~"), ".sonar-local")
    os.makedirs(folder, exist_ok=True)
    init_path = os.path.join(folder, "sonar-init.gradle")
    with open(init_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(INIT_SCRIPT)
    cmd = build_command(root, tool, key, name, args.testlar, init_path.replace(os.sep, "/"))
    report = report_task_path(root, tool)
    before = os.path.getmtime(report) if os.path.exists(report) else 0
    run_scan(cmd, root, token, os.path.join(folder, "last-scan.log"),
             TEST_SCAN_TIMEOUT if args.testlar else SCAN_TIMEOUT)
    if not os.path.exists(report) or os.path.getmtime(report) <= before:
        raise Fail("scanner %s ni yangilamadi" % report)
    with open(report, encoding="utf-8") as handle:
        info = read_report_task(handle.read())
    if not info.get("ceTaskUrl"):
        raise Fail("report-task.txt da ceTaskUrl yo'q")
    wait_ce(info["ceTaskUrl"], admin)

    moved_issue, moved, note = sync_statuses(remote, admin, key)
    if note:
        say("tahlil: status: " + note)

    base = local_url()
    gate = api(base, "/api/qualitygates/project_status?projectKey=" + urllib.parse.quote(key), admin)
    gate_status = gate.get("projectStatus", {}).get("status", "?")
    issues = open_issues(base, admin, key)
    todo = hotspots_of(base, admin, key, "TO_REVIEW")
    done = hotspots_of(base, admin, key, "REVIEWED")
    cov = {m["metric"]: m.get("value") for m in api(
        base, "/api/measures/component?component=%s&metricKeys=coverage,line_coverage,branch_coverage" %
        urllib.parse.quote(key), admin)["component"].get("measures", [])}

    for item in sorted(issues, key=lambda i: (i.get("rule", ""), i.get("component", ""), i.get("line") or 0)):
        say("issue %s %s:%s %s" % (item.get("rule", ""), sonar_fetch.file_of(item.get("component", "")),
                                    item.get("line") or "-", short(item.get("message", ""))))
    for item in sorted(todo, key=lambda h: (h.get("component", ""), h.get("line") or 0)):
        say("hotspot %s %s:%s %s" % (item.get("ruleKey", ""), sonar_fetch.file_of(item.get("component", "")),
                                      item.get("line") or "-", short(item.get("message", ""))))
    for cond in gate.get("projectStatus", {}).get("conditions", []):
        if cond.get("status") == "ERROR":
            say("gate sharti buzildi: %s %s %s (qiymat %s)" % (
                cond.get("metricKey"), cond.get("comparator"), cond.get("errorThreshold"),
                cond.get("actualValue")))
    code = verdict(gate_status, len(issues), len(todo))
    say("sonar_local: tahlil: gate %s, issue %d, hotspot TO_REVIEW %d (reviewed %d, serverdan ko'chirildi %d, issue status %d), "
        "coverage %s%% (qator %s%%, shart %s%%), %d s" % (
            gate_status, len(issues), len(todo), len(done), moved, moved_issue,
            cov.get("coverage", "?"), cov.get("line_coverage", "?"), cov.get("branch_coverage", "?"),
            int(time.time() - started)) + ("" if code == 0 else " -> TOPILMA, push tavsiya qilinmaydi"))
    return code


# -- solishtir ---------------------------------------------------------------

def revision_of(base, auth, key):
    try:
        data = api(base, "/api/project_analyses/search?project=%s&ps=1" % urllib.parse.quote(key), auth)
    except Fail:
        return ""
    items = data.get("analyses", [])
    return (items[0].get("revision") or "") if items else ""


def compare_verdict(remote_rev, local_rev, differences):
    """0 bir xil, 1 bir xil commit da farq, 3 commit mos emas va farq bor."""
    if not differences:
        return 0
    same = remote_rev and local_rev and remote_rev == local_rev
    return 1 if same else 3


def all_issues(base, auth, key):
    out, page = set(), 1
    while True:
        data = api(base, "/api/issues/search?componentKeys=%s&issueStatuses=OPEN,CONFIRMED,ACCEPTED,"
                         "FALSE_POSITIVE&ps=500&p=%d" % (urllib.parse.quote(key), page), auth)
        for i in data["issues"]:
            out.add((i["rule"], i["component"].split(":", 1)[1], i.get("line"),
                     i.get("issueStatus", i.get("status"))))
        if page * 500 >= data["paging"]["total"]:
            return out
        page += 1


def all_hotspots(base, auth, key):
    data = api(base, "/api/hotspots/search?projectKey=%s&ps=500" % urllib.parse.quote(key), auth)
    return {(h.get("ruleKey", h.get("securityCategory")), h["component"].split(":", 1)[1],
             h.get("line"), h["status"]) for h in data["hotspots"]}


def measures_of(base, auth, key):
    data = api(base, "/api/measures/component?component=%s&metricKeys=%s" % (
        urllib.parse.quote(key), METRICS), auth)
    return {m["metric"]: m.get("value") for m in data["component"]["measures"]}


def cmd_solishtir(args):
    key = resolve_key(args.loyiha, os.getcwd())
    try:
        remote = Remote()
    except sonar_fetch.Config as err:
        raise Fail(str(err))
    state = load_state()
    if "password" not in state:
        raise Fail("lokal holat yo'q: avval `sonar_local.py sozla`")
    admin, base = "admin:" + state["password"], local_url()
    diffs = []
    r_i, l_i = all_issues(remote.base, remote.auth, key), all_issues(base, admin, key)
    diffs += ["issue faqat serverda: %s" % (x,) for x in sorted(r_i - l_i, key=str)]
    diffs += ["issue faqat lokalda: %s" % (x,) for x in sorted(l_i - r_i, key=str)]
    r_h, l_h = all_hotspots(remote.base, remote.auth, key), all_hotspots(base, admin, key)
    first = lambda s: {x[:3] for x in s}
    diffs += ["hotspot faqat serverda: %s" % (x,) for x in sorted(first(r_h) - first(l_h), key=str)]
    diffs += ["hotspot faqat lokalda: %s" % (x,) for x in sorted(first(l_h) - first(r_h), key=str)]
    r_m, l_m = measures_of(remote.base, remote.auth, key), measures_of(base, admin, key)
    names = sorted(set(r_m) | set(l_m))
    bad = [k for k in names if r_m.get(k) != l_m.get(k)]
    diffs += ["metrika %s: server %s, lokal %s" % (k, r_m.get(k), l_m.get(k)) for k in bad]
    r_rev, l_rev = revision_of(remote.base, remote.auth, key), revision_of(base, admin, key)
    for line in diffs[:40]:
        say(line)
    code = compare_verdict(r_rev, l_rev, diffs)
    trust = ("bir xil commit %s" % r_rev[:8] if r_rev and r_rev == l_rev
             else "commit mos emas (server %s, lokal %s)" % (r_rev[:8] or "?", l_rev[:8] or "?"))
    say("sonar_local: solishtir: issue %d/%d, hotspot %d/%d, metrika %d tadan %d farq, %s%s" % (
        len(r_i), len(l_i), len(r_h), len(l_h), len(names), len(bad), trust,
        "" if code == 0 else (" -> FARQ" if code == 1 else " -> ishonchli xulosa yo'q")))
    return code


COMMANDS = {"ishga": cmd_ishga, "sozla": cmd_sozla, "moslik": cmd_moslik, "tahlil": cmd_tahlil, "solishtir": cmd_solishtir}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("buyruq", choices=sorted(COMMANDS))
    parser.add_argument("--loyiha", help="project key (sukut GENIUS_SONAR_PROJECT yoki remote+branch)")
    parser.add_argument("--yangila", action="store_true", help="ishga: konteynerni yangi image bilan qayta yarat")
    parser.add_argument("--testlar", action="store_true", help="tahlil: testlarni ham jacoco bilan yurgiz")
    args = parser.parse_args(argv)
    try:
        return COMMANDS[args.buyruq](args)
    except Fail as err:
        print("sonar_local: %s" % err, file=sys.stderr)
        return 2
    except sonar_fetch.Config as err:
        print("sonar_local: %s" % err, file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
