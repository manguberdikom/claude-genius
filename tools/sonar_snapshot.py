#!/usr/bin/env python3
"""Sonar rule metadata snapshotini yangilaydi (java, xml, docker, kubernetes).

    python3 tools/sonar_snapshot.py                 # korpusdagi kalitlar
    python3 tools/sonar_snapshot.py java:S109 xml:S3822  # faqat shular
    python3 tools/sonar_snapshot.py --tekshir       # yozmaydi, farqni aytadi

Nega snapshot: korpusda 600 dan ko'p qoida kaliti bor va ularning turi,
darajasi hamda default profilga kirgani jadvallarda yozilgan. Metadata
tarmoqda turadi, CI esa har yurishda tarmoqqa chiqmasligi kerak.
Shuning uchun metadata bir marta olinadi, `tools/sonar_rules.tsv` ga
yoziladi va `check_docs.py` shu faylga solishtiradi.

Kalit to'liq shaklda yoziladi: `java:S1192`, `xml:S3822`,
`docker:S6596`, `kubernetes:S6864`. Faqat Java ni bilgan eski snapshot
(kalit ustunida yalang `S1192`) o'qilganda avtomatik `java:` prefiksi
qo'yiladi, shuning uchun migratsiya uchun alohida qadam kerak emas.

Nega bir nechta til: 2026-10 da sonarqube 38-bobni tekshirganda to'rtta
xato aynan shundan chiqdi. Bobda `pom.xml` dagi `LATEST` versiya uchun
XML qoidasi bor deb yozilgan edi (yo'q), Kubernetes da probe qoidasi bor
deb yozilgan edi (yo'q), `apt-get` versiyasi uchun Docker qoidasi bor deb
yozilgan edi (yo'q), va CPU limit qoidasi default profilda deb
hisoblangan edi (emas). Faqat `java:` kalitlarini tekshiradigan snapshot
bu to'rttasini ko'rmaydi. Shuning uchun `profil` ustuni ham bor: qoida
`Sonar way` da yoqilganmi yoki qo'lda yoqish kerakmi.

Metadata ochiq repolarda turadi, hammasi `REPOS` da:

    java        SonarSource/sonar-java (+ sonar-java-symbolic-execution)
    xml         SonarSource/sonar-xml
    docker      SonarSource/sonar-iac, iac-extensions/docker
    kubernetes  SonarSource/sonar-iac, iac-extensions/kubernetes

Symbolic execution repo si alohida muhim: S2095, S2189, S2583, S2589,
S2755 kabi qoidalar 2024 da ko'chirilgan va yo'lida `rules/java` emas,
`rules/javase` turadi. Faqat birinchi repoga qaragan snapshot ularni
topa olmaydi.

Shunga qaramay ba'zi qoidalar ochiq metadata da hamon YO'Q (yopiq
analizator: taint analysis va bir qism SE qoidalari). Ular
`tekshirilmadi` deb belgilanadi va check_docs ularni ogohlantirish
bilan o'tkazadi, xato bermaydi.
"""

import argparse
import datetime
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SNAPSHOT = os.path.join(HERE, "sonar_rules.tsv")

# Manba branch emas, tag ga mixlanadi. Ikki sabab: loyiha qoidasi
# (branch ko'chadi, havola bir yildan keyin ham ayni matnni ochishi
# kerak) va amaliy sabab, 2026-10 da sonar-iac ning `master` i
# qayta tuzilish holatida edi va `S6587`, `S6497`, `S6437` kabi
# mavjud qoidalarning fayllari o'sha branchda 404 qaytardi.
# Yangilashda shu to'rtta tagni ko'tarib, snapshotni qayta yozish
# kerak; `--tekshir` farqni ko'rsatadi.
TAGS = {
    "sonar-java": "8.44.0.48651",
    "sonar-java-symbolic-execution": "8.24.0.2319",
    "sonar-xml": "2.19.0.8138",
    "sonar-iac": "1.42.0.14460",
}


def raw(repo, path):
    return ("https://raw.githubusercontent.com/SonarSource/%s/%s/%s"
            % (repo, TAGS[repo], path))

# til -> (qoida yo'li naqshlari, profil JSON i yoki None,
#          profil marker naqshlari yoki None).
# Yo'l naqshida `%s` kalit bilan almashadi. Naqshlar tartib bilan
# sinaladi, birinchi topilgani olinadi.
#
# Profil ikki shaklda saqlanadi va ikkisi ham kerak. sonar-xml va
# sonar-iac bitta `Sonar_way_profile.json` beradi, uning ichida
# `ruleKeys` ro'yxati bor. sonar-java esa `profiles/Sonar_way/`
# katalogida kalit nomli BO'SH fayllar qo'yadi, ya'ni a'zolik
# faylning mavjudligi bilan bildiriladi. Marker yo'li uchun JSON
# parse qilinmaydi, faqat HTTP 200 tekshiriladi.
REPOS = {
    "java": (
        (raw("sonar-java",
             "sonar-java-plugin/src/main/resources/org/sonar/l10n/java/"
             "rules/java/%s.json"),
         raw("sonar-java-symbolic-execution",
             "java-symbolic-execution/java-symbolic-execution-plugin/"
             "src/main/resources/org/sonar/l10n/java/rules/javase/"
             "%s.json")),
        None,
        # Marker: kalit nomli bo'sh fayl bor bo'lsa, qoida Sonar way da.
        raw("sonar-java",
            "sonar-java-plugin/src/main/resources/profiles/Sonar_way/%s"),
    ),
    "xml": (
        (raw("sonar-xml",
             "sonar-xml-plugin/src/main/resources/org/sonar/l10n/xml/"
             "rules/xml/%s.json"),),
        raw("sonar-xml",
            "sonar-xml-plugin/src/main/resources/org/sonar/l10n/xml/"
            "rules/xml/Sonar_way_profile.json"),
        None,
    ),
    "docker": (
        (raw("sonar-iac",
             "iac-extensions/docker/src/main/resources/org/sonar/l10n/"
             "docker/rules/docker/%s.json"),),
        raw("sonar-iac",
            "iac-extensions/docker/src/main/resources/org/sonar/l10n/"
            "docker/rules/docker/Sonar_way_profile.json"),
        None,
    ),
    "kubernetes": (
        (raw("sonar-iac",
             "iac-extensions/kubernetes/src/main/resources/org/sonar/"
             "l10n/kubernetes/rules/kubernetes/%s.json"),),
        raw("sonar-iac",
            "iac-extensions/kubernetes/src/main/resources/org/sonar/"
            "l10n/kubernetes/rules/kubernetes/Sonar_way_profile.json"),
        None,
    ),
}
LANGS = tuple(sorted(REPOS))
RULE_RE = re.compile(r"\b(%s):(S\d+)\b" % "|".join(LANGS))
DEFAULT_LANG = "java"

# Qoida sarlavhasi (`title`) olinmaydi: u analizatorlarning SSALv1
# ostidagi matni, bu fayl esa MIT ostida. Uni hech bir asbob o'qimaydi,
# check_docs faqat tur, daraja va profilga qaraydi.
HEADER = ("kalit", "tur", "daraja", "scope", "profil")
MISSING = "tekshirilmadi"
IN_PROFILE = "ha"
NOT_IN_PROFILE = "yo'q"
SCAN_DIRS = ("docs", ".claude")
SCAN_EXT = (".md", ".tsv")


def sort_key(key):
    """`xml:S3822` -> ("xml", 3822). Yalang `S3822` ham ishlaydi."""
    lang, _, num = key.rpartition(":")
    return (lang or DEFAULT_LANG, int(num[1:]) if num[1:].isdigit() else 0)


def normalize(key):
    """Prefiksi yo'q kalitga `java:` qo'yadi (eski snapshot uchun)."""
    return key if ":" in key else "%s:%s" % (DEFAULT_LANG, key)


def corpus_keys():
    """Korpusda uchraydigan to'liq qoida kalitlari."""
    keys = set()
    for base in SCAN_DIRS:
        for dirpath, dirs, files in os.walk(os.path.join(ROOT, base)):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for name in files:
                if not name.endswith(SCAN_EXT):
                    continue
                try:
                    text = io.open(os.path.join(dirpath, name),
                                   encoding="utf-8").read()
                except (OSError, UnicodeDecodeError):
                    continue
                keys.update("%s:%s" % pair for pair in RULE_RE.findall(text))
    return keys


def read_snapshot(path=SNAPSHOT):
    """{kalit: {tur, daraja, scope, profil}} va sana.

    Ustunlar sarlavha qatori bo'yicha olinadi, shuning uchun eski
    4 ustunli (profilsiz) va 5 ustunli fayl ham o'qiladi. Kalitga
    prefiks qo'yilmagan bo'lsa `java:` deb o'qiladi."""
    rows, date, header = {}, "", None
    if not os.path.exists(path):
        return rows, date
    with io.open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith("# sana:"):
                date = line.split(":", 1)[1].strip()
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if header is None:
                header = parts
                continue
            row = dict(zip(header, parts))
            row.setdefault("profil", MISSING)
            rows[normalize(row.get("kalit", ""))] = row
    return rows, date


def get(url):
    """URL dan JSON yoki None."""
    try:
        proc = subprocess.run(["curl", "-sS", "-f", "--max-time", "30", url],
                              capture_output=True, timeout=45)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout.decode("utf-8"))
    except ValueError:
        return None


def fetch(key):
    """Bitta to'liq kalitning metadata si yoki None.

    Til naqshlari tartib bilan sinaladi, birinchi topilgani qaytadi."""
    lang, _, num = normalize(key).rpartition(":")
    templates = REPOS.get(lang, ((), None, None))[0]
    for template in templates:
        data = get(template % num)
        if data is not None:
            return data
    return None


def fetch_profile(lang):
    """Tilning `Sonar way` profilidagi kalitlar to'plami yoki None.

    Faqat JSON shakli uchun. Marker shakli har kalit uchun alohida
    tekshiriladi (`in_profile_marker`), chunki ro'yxat fayli yo'q."""
    url = REPOS.get(lang, (None, None, None))[1]
    if url is None:
        return None
    data = get(url)
    if not isinstance(data, dict):
        return None
    return set(data.get("ruleKeys") or ())


def exists(url):
    """URL 200 qaytaradimi. JSON parse qilinmaydi."""
    try:
        proc = subprocess.run(["curl", "-sS", "-o", os.devnull, "-w", "%{http_code}",
                               "--max-time", "30", url],
                              capture_output=True, timeout=45)
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace").strip() == "200"


def in_profile_marker(lang, num):
    """Marker shaklidagi profil uchun: True, False yoki None (bilib
    bo'lmadi)."""
    template = REPOS.get(lang, (None, None, None))[2]
    if template is None:
        return None
    return exists(template % num)


def write_snapshot(rows, path=SNAPSHOT):
    today = datetime.date.today().isoformat()
    lines = [
        "# Sonar rule metadata snapshoti: java, xml, docker, kubernetes.",
        "# sana: %s" % today,
        "#",
        "# manba (hammasi SonarSource, tagga mixlangan):",
    ]
    for lang in LANGS:
        for template in REPOS[lang][0]:
            lines.append("#   %-10s %s" % (lang, template % "<kalit>"))
    lines += [
        "#",
        "# kalit  - to'liq kalit, masalan java:S1192 yoki docker:S6596",
        "# tur    - CODE_SMELL | BUG | VULNERABILITY | SECURITY_HOTSPOT",
        "# daraja - defaultSeverity (legacy severity)",
        "# scope  - Main | Tests | All",
        "# profil - qoida `Sonar way` da yoqilganmi: %s | %s | %s"
        % (IN_PROFILE, NOT_IN_PROFILE, MISSING),
        "#",
        "# `%s` = ma'lumot ochiq metadata da yo'q. Qoida uchun bu" % MISSING,
        "# yopiq analizator (taint analysis, bir qism SE qoidalari);",
        "# profil uchun esa til default profilini bermaydi. check_docs",
        "# ikkisini ham ogohlantirish bilan o'tkazadi, xato bermaydi.",
        "#",
        "# Yangilash: python3 tools/sonar_snapshot.py",
        "\t".join(HEADER),
    ]
    for key in sorted(rows, key=sort_key):
        row = rows[key]
        lines.append("\t".join([key] + [row.get(col, MISSING)
                                        for col in HEADER[1:]]))
    io.open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return today


def main(argv=None):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("kalitlar", nargs="*",
                        help="to'liq kalitlar (java:S109); bermasa korpus")
    parser.add_argument("--tekshir", action="store_true",
                        help="yozmaydi, snapshotda yo'q kalitlarni aytadi")
    args = parser.parse_args(argv)

    want = {normalize(k) for k in args.kalitlar} or corpus_keys()
    have, date = read_snapshot()
    missing = sorted(want - set(have), key=sort_key)

    if args.tekshir:
        print("snapshot: %d kalit, sana %s" % (len(have), date or "yo'q"))
        print("korpusda: %d kalit" % len(want))
        if missing:
            print("snapshotda yo'q (%d): %s" % (len(missing),
                                                " ".join(missing)))
            return 1
        extra = sorted(set(have) - want, key=sort_key)
        if extra:
            print("korpusda ishlatilmaydi (%d): %s"
                  % (len(extra), " ".join(extra)))
        print("snapshot korpusni qoplaydi.")
        return 0

    rows = dict(have)
    added = unchecked = 0
    for key in sorted(want, key=sort_key):
        if key in rows and rows[key].get("tur") != MISSING:
            continue
        data = fetch(key)
        if data is None:
            rows[key] = {"tur": MISSING, "daraja": MISSING,
                         "scope": MISSING, "profil": MISSING}
            unchecked += 1
            continue
        rows[key] = {"tur": data.get("type", MISSING),
                     "daraja": data.get("defaultSeverity", MISSING),
                     "scope": data.get("scope", MISSING),
                     "profil": MISSING}
        added += 1

    # Profil JSON i bir marta til bo'yicha olinadi: har kalit uchun
    # emas. Marker shakli esa har kalit uchun alohida tekshiriladi.
    langs = {sort_key(k)[0] for k in rows}
    for lang in sorted(langs):
        keys_in = fetch_profile(lang)
        for key in rows:
            lang_of, _, num = key.rpartition(":")
            if lang_of != lang:
                continue
            if keys_in is not None:
                rows[key]["profil"] = (IN_PROFILE if num in keys_in
                                       else NOT_IN_PROFILE)
                continue
            found = in_profile_marker(lang, num)
            if found is not None:
                rows[key]["profil"] = (IN_PROFILE if found
                                       else NOT_IN_PROFILE)

    today = write_snapshot(rows)
    print("snapshot yozildi: %d kalit, %d yangi olindi, %d tekshirilmadi, "
          "sana %s" % (len(rows), added, unchecked, today))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
