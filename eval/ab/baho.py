#!/usr/bin/env python3
"""A/B mexanik baholovchi va ifloslanish filtri.

    python3 eval/ab/baho.py <yurish-papkasi>        # pc/, asl/, config/, javob.md
    python3 eval/ab/baho.py --kalibr [--pc <repo>]  # oltin -> 1, bo'sh -> 0, haqiqiy Maven
    python3 eval/ab/baho.py --sinov                 # Maven siz o'z-o'zini sinash

Mexanik qism vazifa faylidagi qabul mezonini kod bilan tekshiradi:
testlar (surefire XML), diff (`asl/` bilan fayl darajasida, model git
bilan nima qilgani muhim emas), maqsadli fayldagi qator va 7-vazifada
JaCoCo shoxlari. Arzon tekshiruvlar avval yuradi: biri yiqilsa Maven
yurmaydi va izohda birinchi yiqilgan mezon turadi.

Review (8, 9) va reja (10) vazifalarida mexanik qism kalit so'z
bo'yicha sanaydi. Bu taxminiy: `xato_topildi` ni ko'r hakam tasdiqlaydi,
`yolgon_topilma` ni faqat hakam beradi (README, "Baholash").

Ifloslanish (README, "Ifloslanish qoidasi"): transkriptda
- A holatida Skill(manguberdi), /manguberdi yoki aktyor subagent_type;
- har holatda `eval/ab` yo'li (javob kaliti);
- B holatida manguberdi yuklangani izi yo'q;
- transkript umuman yo'q.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import umumiy  # noqa: E402
from umumiy import AKTYORLAR, TOLIQ_TOPLAM  # noqa: E402

BAZAVIY_TEST = 76
OWNER = "src/main/java/org/springframework/samples/petclinic/owner/"
OWNER_TEST = "src/test/java/org/springframework/samples/petclinic/owner/"
YOQ = {".git", "target", ".idea", ".vscode", "node_modules", ".claude", ".mvn"}


# ---------------------------------------------------------------- ifloslanish

def ifloslanish(config_dir, holat):
    """Yurishni yaroqsiz qiladigan sabablar ro'yxati (bo'sh = toza)."""
    fayllar = umumiy.transkriptlar(config_dir)
    if not fayllar:
        return ["transkript yo'q"]
    yozuvlar = list(umumiy.transkript_yozuvlari(fayllar))
    sabab = []
    manguberdi = False
    for nom, inp in umumiy.tool_uselar(yozuvlar):
        matn = json.dumps(inp, ensure_ascii=False).replace("\\\\", "/")
        if "eval/ab" in matn:
            sabab.append("eval/ab yo'li: %s" % nom)
        if nom == "Skill" and str(inp.get("skill", "")).split(":")[-1] == "manguberdi":
            manguberdi = True
            if holat == "A":
                sabab.append("A: Skill(manguberdi)")
        if nom in ("Task", "Agent") and inp.get("subagent_type") in AKTYORLAR and holat == "A":
            sabab.append("A: aktyor %s" % inp.get("subagent_type"))
    for matn in umumiy.foydalanuvchi_matnlari(yozuvlar):
        if re.search(r"<command-name>/?manguberdi</command-name>|skills/manguberdi", matn):
            manguberdi = True
            if holat == "A":
                sabab.append("A: /manguberdi")
    if holat == "B" and not manguberdi:
        sabab.append("B: manguberdi yuklanmadi")
    return sorted(set(sabab))


# ---------------------------------------------------------------- yordamchi

def matn(yol):
    yol = Path(yol)
    return yol.read_text(encoding="utf-8", errors="replace") if yol.is_file() else ""


def daraxt(ildiz):
    ildiz = Path(ildiz)
    natija = {}
    for f in ildiz.rglob("*"):
        rel = f.relative_to(ildiz)
        if rel.parts and rel.parts[0] in YOQ:
            continue
        if f.is_file():
            natija[rel.as_posix()] = f.read_bytes()
    return natija


def farq(asl, pc):
    """{yo'l: 'qo'shilgan' | 'o'chirilgan' | 'o'zgargan'}."""
    a, b = daraxt(asl), daraxt(pc)
    natija = {}
    for k in set(a) | set(b):
        if k not in a:
            natija[k] = "qo'shilgan"
        elif k not in b:
            natija[k] = "o'chirilgan"
        elif a[k] != b[k]:
            natija[k] = "o'zgargan"
    return natija


TEST_RE = re.compile(r"@(?:Test|ParameterizedTest)\b[^\n]*\n(?:[ \t]*@[^\n]*\n)*[ \t]*"
                     r"(?:(?:public|protected|private|static|final)\s+)*void\s+(\w+)\s*\(")


def test_metodlari(java):
    """{metod nomi: tanasi}: @Test va @ParameterizedTest."""
    natija = {}
    for m in TEST_RE.finditer(java):
        i = java.find("{", m.end())
        if i < 0:
            continue
        chuq, j = 0, i
        while j < len(java):
            if java[j] == "{":
                chuq += 1
            elif java[j] == "}":
                chuq -= 1
                if chuq == 0:
                    break
            j += 1
        natija[m.group(1)] = java[i + 1:j]
    return natija


def yangi_testlar(asl_dir, pc_dir, fayl_filtri):
    """(yangi {nom: tana}, dublikat nomlar, fayl->sinf) filtrga mos test fayllarida."""
    yangi, dublikat, sinflar = {}, [], set()
    for rel, tur in farq(asl_dir, pc_dir).items():
        if not rel.startswith("src/test/") or not rel.endswith(".java") or tur == "o'chirilgan":
            continue
        if not fayl_filtri(Path(rel).name):
            continue
        eski = test_metodlari(matn(Path(asl_dir) / rel))
        hozir = test_metodlari(matn(Path(pc_dir) / rel))
        eski_tana = {re.sub(r"\s+", "", t) for t in eski.values()}
        for nom, tana in hozir.items():
            if nom in eski:
                continue
            yangi[nom] = tana
            sinflar.add(Path(rel).stem)
            if re.sub(r"\s+", "", tana) in eski_tana:
                dublikat.append(nom)
    return yangi, dublikat, sorted(sinflar)


def yashil(n, kamida=1):
    return n["rc"] == 0 and n["jami"] >= kamida and not n["yiqilgan"]


def mvn_yurgiz(pc, test, jacoco=False):
    """./mvnw test, natija surefire XML dan."""
    pc = Path(pc)
    hisobot = pc / "target" / "surefire-reports"
    if hisobot.exists():
        shutil.rmtree(hisobot)
    cmd = ["./mvnw", "-B", "test", "-Dtest=" + test, "-DfailIfNoSpecifiedTests=false"]
    if jacoco:
        cmd.append("jacoco:report")
    try:
        r = subprocess.run(cmd, cwd=pc, capture_output=True, timeout=1800)
        rc = r.returncode
    except subprocess.TimeoutExpired:
        rc = -1
    jami, yiqilgan, otgan = 0, [], []
    for x in sorted(hisobot.glob("TEST-*.xml")) if hisobot.exists() else []:
        try:
            ildiz = ET.parse(x).getroot()
        except ET.ParseError:
            continue
        for tc in ildiz.iter("testcase"):
            nom = "%s.%s" % (tc.get("classname", "").rsplit(".", 1)[-1], tc.get("name", ""))
            if tc.find("skipped") is not None:
                continue
            jami += 1
            if tc.find("failure") is not None or tc.find("error") is not None:
                yiqilgan.append(nom)
            else:
                otgan.append(nom)
    return {"rc": rc, "jami": jami, "yiqilgan": yiqilgan, "otgan": otgan}


def jacoco_qatorlar(pc, fayl="Owner.java"):
    """{qator raqami: (mb, cb)} JaCoCo XML dan."""
    x = Path(pc) / "target" / "site" / "jacoco" / "jacoco.xml"
    if not x.exists():
        return {}
    natija = {}
    for sf in ET.parse(x).getroot().iter("sourcefile"):
        if sf.get("name") != fayl:
            continue
        for ln in sf.iter("line"):
            natija[int(ln.get("nr"))] = (int(ln.get("mb", 0)), int(ln.get("cb", 0)))
    return natija


def metod_qatorlari(java, sarlavha):
    """Metod tanasidagi qatorlar: [(raqam, matn)]."""
    qatorlar = java.splitlines()
    for i, q in enumerate(qatorlar):
        if sarlavha in q:
            chuq, boshladi = 0, False
            for j in range(i, len(qatorlar)):
                chuq += qatorlar[j].count("{") - qatorlar[j].count("}")
                boshladi = boshladi or "{" in qatorlar[j]
                if boshladi and chuq <= 0:
                    return [(n + 1, qatorlar[n]) for n in range(i, j + 1)]
    return []


def normal(t):
    return re.sub(r"[\u2018\u2019\u02bb\u02bc`]", "'", t).lower()


# ---------------------------------------------------------------- kalit so'zlar

REVIEW = {
    8: [
        ("R1-1", [r"thread[- ]?safe", r"concurrenthashmap", r"race condition", r"poyga",
                  r"parallel\s+so'rov", r"konkuren", r"concurren", r"synchroniz", r"sinxronla"]),
        ("R1-2", [r"cheklanmagan", r"chegarasiz", r"unbounded", r"chiqarish\s+siyosat",
                  r"eviction\s+polic", r"\bttl\b", r"memory\s+leak", r"xotira\s+(o'sadi|sizib|to'l)",
                  r"\boom\b", r"outofmemory", r"maximumsize", r"cheksiz\s+o's"]),
        ("R1-3", [r"printstacktrace", r"yutib\s+yubor|yutiladi|yutadi", r"swallow", r"page\.empty",
                  r"bo'sh\s+sahifa", r"xato(ni)?\s+yashir"]),
        ("R1-4", [r"invalidat", r"\bstale\b", r"eskirgan\s+(ma'lumot|natija|sahifa)",
                  r"eski\s+(sahifa|natija|ma'lumot)", r"@cacheevict"]),
    ],
    9: [
        ("R2-1", [r"\bdouble\b.{0,120}(pul|money|aniq|precision|yaxlit|round|kasr)",
                  r"(pul|money).{0,120}\bdouble\b", r"floating[- ]point", r"suzuvchi\s+nuqta",
                  r"ikkilik\s+kasr"]),
        ("R2-2", [r"new\s+(java\.math\.)?bigdecimal\s*\(\s*(double|amount)", r"bigdecimal\.valueof",
                  r"bigdecimal\s*\(\s*double\s*\)", r"satrli\s+konstruktor", r"string\s+constructor"]),
        ("R2-3", [r"simpledateformat.{0,200}(thread|parallel|konkuren|concurren|bo'lishil|shared)",
                  r"(thread|parallel|konkuren|concurren).{0,200}simpledateformat",
                  r"datetimeformatter"]),
        ("R2-4", [r"private.{0,150}(transactional|proxy|tranzaksiya)",
                  r"(transactional|proxy).{0,150}private", r"self[- ]invocation"]),
    ],
}

# 10-vazifa: har band uchun kerakli guruhlar (har guruhdan kamida bittasi).
REJA = [
    ("pul turi", [[r"bigdecimal", r"tiyin", r"\bcents?\b", r"minor\s+unit",
                   r"(numeric|decimal)\s*\(\s*\d+\s*,\s*2\s*\)"]]),
    ("sxema va qaytarish", [[r"migratsiya", r"migration", r"flyway", r"liquibase",
                             r"alter\s+table", r"schema\.sql", r"db/"],
                            [r"orqaga\s+qaytar", r"rollback", r"revert", r"\bdown\b",
                             r"drop\s+column", r"qaytarish\s+yo'li"]]),
    ("mavjud ma'lumot", [[r"\bnull\b", r"default", r"eski\s+tashrif",
                          r"mavjud\s+(yozuv|ma'lumot|tashrif)", r"backfill"]]),
    ("validatsiya", [[r"manfiy", r"negative", r"@positive", r"@decimalmin", r"@min\b", r"musbat"],
                     [r"juda\s+katta", r"maksimal", r"maximum", r"@max\b", r"@decimalmax",
                      r"@digits", r"yuqori\s+chegara", r"overflow"]]),
    ("test rejasi", [[r"@webmvctest", r"@datajpatest", r"@springboottest", r"testcontainers",
                      r"slice", r"unit\s+test", r"integratsion", r"integration\s+test"]]),
    ("qadam va buyruq", [[r"\./mvnw", r"\bmvn\s"]]),
    ("qamrovdan tashqari", [[r"qamrov(dan)?\s+tashqari", r"out\s+of\s+scope", r"non[- ]goals?",
                             r"kirmaydi", r"qilinmaydi", r"keyingi\s+bosqich"]]),
]


def review_hisob(raqam, javob):
    t = normal(javob)
    return [k for k, naqsh in REVIEW[raqam] if any(re.search(n, t, re.S) for n in naqsh)]


def reja_hisob(javob):
    t = normal(javob)
    bor = []
    for nom, guruhlar in REJA:
        if not all(any(re.search(n, t, re.S) for n in g) for g in guruhlar):
            continue
        if nom == "test rejasi":
            if sum(1 for n in guruhlar[0] if re.search(n, t)) < 2:
                continue
        if nom == "qadam va buyruq":
            qadam = re.findall(r"(?m)^\s*(?:#+\s*)?(?:\d+[.)]\s|qadam\s*\d+|step\s*\d+)", t)
            if len(qadam) < 3:
                continue
        bor.append(nom)
    return bor


# ---------------------------------------------------------------- vazifalar

class Baho:
    def __init__(self):
        self.izoh = []
        self.ok = True

    def tek(self, shart, nom):
        if not shart:
            self.ok = False
            self.izoh.append("YO'Q: " + nom)
        return shart


def _src_ozgarish(f, prefiks):
    return sorted(k for k in f if k.startswith(prefiks))


def baho_mexanik(raqam, pc, asl, javob="", mvn=mvn_yurgiz):
    """(muvaffaqiyat, xato_topildi, izoh). Arzon mezon avval, Maven keyin."""
    pc, asl = Path(pc), Path(asl)
    f = farq(asl, pc)
    main_oz = _src_ozgarish(f, "src/main/")
    test_oz = _src_ozgarish(f, "src/test/")
    b = Baho()
    xato_topildi = ""
    mavn = []  # (nom, test, kamida) Maven tekshiruvlari, arzonlar o'tsa

    if raqam == 1:
        pv = matn(pc / OWNER / "PetValidator.java")
        b.tek(re.search(r"name\.length\(\)\s*>\s*MAX_NAME_LENGTH\s*\)", pv)
              and not re.search(r"MAX_NAME_LENGTH\s*\+\s*1", pv), "chegara MAX_NAME_LENGTH ga teng")
        decl = re.compile(r".*MAX_NAME_LENGTH\s*=.*")
        b.tek(decl.findall(pv) == decl.findall(matn(asl / OWNER / "PetValidator.java")),
              "MAX_NAME_LENGTH qiymati o'zgarmagan")
        b.tek(not test_oz, "test o'zgartirilmagan")
        b.tek(main_oz == [OWNER + "PetValidator.java"], "faqat PetValidator.java o'zgargan")
        mavn = [("PetValidatorTests yashil", "PetValidatorTests", 1)]
    elif raqam == 2:
        pv = matn(pc / OWNER / "PetValidator.java")
        b.tek(re.search(r"StringUtils\.hasText\(\s*name\s*\)|name\.isBlank\(\)|"
                        r"name\.(strip|trim)\(\)\.isEmpty\(\)", pv)
              and not re.search(r"if\s*\(\s*name\s*==\s*null\s*\)", pv),
              "bo'sh va bo'sh joyli ism rad etiladi")
        b.tek(not test_oz, "test o'zgartirilmagan")
        b.tek(main_oz == [OWNER + "PetValidator.java"], "tuzatish PetValidator da")
        mavn = [("PetControllerTests yashil", "PetControllerTests", 1)]
    elif raqam == 3:
        oc = matn(pc / OWNER / "OwnerController.java")
        b.tek(re.search(r"PageRequest\.of\(\s*\w+\s*-\s*1\s*,", oc), "PageRequest nol asosli")
        yangi, _, sinflar = yangi_testlar(asl, pc, lambda n: n.endswith(".java"))
        b.tek(yangi, "yangi regressiya testi")
    elif raqam in (4, 5):
        b.tek(not test_oz, "test o'zgartirilmagan")
        b.tek(main_oz and all(k.startswith(OWNER) for k in main_oz),
              "diff faqat owner paketidagi ishlab chiqarish kodida")
        if raqam == 4:
            b.tek(OWNER + "OwnerController.java" in main_oz, "OwnerController o'zgargan")
            b.tek("processFindForm(" in matn(pc / OWNER / "OwnerController.java"),
                  "processFindForm saqlangan")
        else:
            ow = matn(pc / OWNER / "Owner.java")
            b.tek(OWNER + "Owner.java" in main_oz, "Owner o'zgargan")
            b.tek(len(re.findall(r"for\s*\(\s*Pet\b", ow))
                  < len(re.findall(r"for\s*\(\s*Pet\b", matn(asl / OWNER / "Owner.java"))),
                  "getPet sikli takrori kamaygan")
            optional_yomon = re.compile(
                r"(?:private|protected|public)\s+(?:static\s+)?(?:final\s+)?Optional<[^>]*>\s+\w+\s*[;=]"
                r"|[(,]\s*(?:final\s+)?Optional<[^>]*>\s+\w+\s*[,)]")
            b.tek(not any(optional_yomon.search(matn(pc / k)) for k in main_oz),
                  "Optional maydon yoki parametr emas")
    elif raqam == 6:
        b.tek(not main_oz, "ishlab chiqarish kodi o'zgarmagan")
        yangi, dub, _ = yangi_testlar(asl, pc, lambda n: "PetTypeFormatter" in n)
        b.tek(len(yangi) >= 2, "kamida 2 yangi test (%d)" % len(yangi))
        b.tek(not dub, "mavjud test takrorlanmagan")
        tana = "\n".join(yangi.values())
        turlar = set()
        for lit in re.findall(r"\.parse\(\s*\"([^\"]*)\"", tana):
            if lit.strip() == "":
                turlar.add("bo'sh satr")
            elif lit.lower() in ("dog", "bird") and lit not in ("Dog", "Bird"):
                turlar.add("registr")
        if re.search(r"\.parse\(\s*null", tana):
            turlar.add("null")
        if re.search(r"willReturn\(\s*(List\.of\(\)|Collections\.emptyList\(\)|new ArrayList<>\(\))", tana):
            turlar.add("bo'sh ro'yxat")
        b.tek(len(turlar) >= 2, "kamida 2 yangi chegara holati (%s)" % ", ".join(sorted(turlar)))
        mavn = [("PetTypeFormatterTests yashil", "PetTypeFormatterTests", 1)]
    elif raqam == 7:
        b.tek(not main_oz, "ishlab chiqarish kodi o'zgarmagan")
        yangi, dub, _ = yangi_testlar(asl, pc, lambda n: n == "OwnerTests.java")
        b.tek(len(yangi) >= 3, "OwnerTests da kamida 3 yangi test (%d)" % len(yangi))
        mavn = [("OwnerTests yashil", "OwnerTests", 1)]
    elif raqam in (8, 9):
        b.tek(not main_oz and not test_oz, "kod o'zgartirilmagan")
        topildi = review_hisob(raqam, javob)
        xato_topildi = len(topildi)
        b.izoh.append("kalit so'z: " + (",".join(topildi) or "-"))
        b.tek(len(topildi) >= 3, "kamida 3/4 nuqson (%d)" % len(topildi))
    elif raqam == 10:
        b.tek(not main_oz and not test_oz, "kod yozilmagan")
        bandlar = reja_hisob(javob)
        b.izoh.append("reja bandlari %d/7" % len(bandlar))
        b.tek(len(bandlar) >= 5, "kamida 5/7 band")
    else:
        raise ValueError("noma'lum vazifa %s" % raqam)

    if not b.ok:
        return 0, xato_topildi, b.izoh

    for nom, test, kamida in mavn:
        if not b.tek(yashil(mvn(pc, test), kamida), nom):
            return 0, xato_topildi, b.izoh
    if raqam <= 7:
        toliq = mvn(pc, TOLIQ_TOPLAM)
        if not b.tek(yashil(toliq, BAZAVIY_TEST), "butun to'plam yashil (%d test, %d yiqilgan)"
                     % (toliq["jami"], len(toliq["yiqilgan"]))):
            return 0, xato_topildi, b.izoh
    if raqam == 3:
        b.tek(qoriqlaydimi(pc, asl, sinflar, set(yangi), mvn),
              "yangi test bug qaytganda yiqiladi")
    if raqam == 7:
        b.tek(addpet_shoxlari(pc, mvn, b.izoh), "addPet shoxlari qoplangan (JaCoCo)")
    return (1 if b.ok else 0), xato_topildi, b.izoh


def qoriqlaydimi(pc, asl, sinflar, nomlar, mvn):
    """Testlar qoladi, src/main asl (bugli) holatga qaytadi: yangi test yiqilishi shart."""
    with tempfile.TemporaryDirectory(prefix="ab-qoriq-") as t:
        nusxa = Path(t) / "pc"
        shutil.copytree(pc, nusxa, symlinks=True,
                        ignore=shutil.ignore_patterns(".git", "target"))
        shutil.rmtree(nusxa / "src" / "main")
        shutil.copytree(Path(asl) / "src" / "main", nusxa / "src" / "main")
        n = mvn(nusxa, ",".join(sinflar))
        yiqilgan = {y.split(".", 1)[-1] for y in n["yiqilgan"]}
        return bool(yiqilgan & nomlar)


def addpet_shoxlari(pc, mvn, izoh):
    """null va contains shoxlari to'liq, id sharti kamida 4 shox (bir xil id, yangi hayvon)."""
    n = mvn(pc, "OwnerTests", jacoco=True)
    if not yashil(n):
        return False
    qatorlar = metod_qatorlari(matn(Path(pc) / OWNER / "Owner.java"), "void addPet(")
    jac = jacoco_qatorlar(pc)
    if not jac:
        izoh.append("jacoco.xml yo'q")
        return False

    def qator(naqsh):
        for nr, q in qatorlar:
            if re.search(naqsh, q):
                return jac.get(nr, (1, 0))
        return (1, 0)

    null_ = qator(r"pet\s*==\s*null")
    cont = qator(r"contains\(\s*pet\s*\)")
    teng = qator(r"Objects\.equals\(")
    jami_mb = sum(jac.get(nr, (0, 0))[0] for nr, _ in qatorlar)
    jami_cb = sum(jac.get(nr, (0, 0))[1] for nr, _ in qatorlar)
    izoh.append("addPet shox %d/%d" % (jami_cb, jami_cb + jami_mb))
    return null_[0] == 0 and cont[0] == 0 and teng[1] >= 4


def javob_matni(papka):
    """Sessiyaning yakuniy javobi va u yozgan yangi .md fayllar (src dan tashqari)."""
    papka = Path(papka)
    qism = [matn(papka / "javob.md")]
    if (papka / "asl").is_dir() and (papka / "pc").is_dir():
        for rel, tur in sorted(farq(papka / "asl", papka / "pc").items()):
            if tur != "o'chirilgan" and rel.endswith(".md") and not rel.startswith("src/"):
                qism.append(matn(papka / "pc" / rel))
    return "\n\n".join(q for q in qism if q)


def baholash(vazifa, papka, holat, mvn=mvn_yurgiz):
    papka = Path(papka)
    muv, xato, izoh = baho_mexanik(vazifa.raqam, papka / "pc", papka / "asl",
                                   javob_matni(papka), mvn)
    return {"muvaffaqiyat": muv, "xato_topildi": xato, "izoh": izoh,
            "ifloslanish": ifloslanish(papka / "config", holat)}


# ---------------------------------------------------------------- kalibrlash

def kalibr(pc_manba, faqat=None):
    """Haqiqiy petclinic va Maven: oltin yechim 1, bo'sh yechim 0 olishi shart."""
    import yurgiz
    oltin_ok = bosh_ok = jami = 0
    for v in umumiy.vazifalar():
        if faqat and v.raqam not in faqat:
            continue
        jami += 1
        with tempfile.TemporaryDirectory(prefix="ab-kalibr-") as t:
            t = Path(t)
            yurgiz.tayyorla(v, pc_manba, t / "bosh")
            m0, _, iz0 = baho_mexanik(v.raqam, t / "bosh" / "pc", t / "bosh" / "asl", "")
            yurgiz.tayyorla(v, pc_manba, t / "oltin")
            diff = umumiy.OLTIN / ("%02d.diff" % v.raqam)
            if diff.exists():
                yurgiz.git("apply", str(diff), cwd=t / "oltin" / "pc")
            jav = matn(umumiy.OLTIN / ("%02d.md" % v.raqam))
            m1, x1, iz1 = baho_mexanik(v.raqam, t / "oltin" / "pc", t / "oltin" / "asl", jav)
        oltin_ok += m1 == 1
        bosh_ok += m0 == 0
        print("%02d oltin=%d bo'sh=%d  | oltin: %s | bo'sh: %s"
              % (v.raqam, m1, m0, "; ".join(iz1) or "-", "; ".join(iz0[:2]) or "-"))
    print("kalibr: oltin %d/%d, bo'sh 0 olgani %d/%d" % (oltin_ok, jami, bosh_ok, jami))
    return 0 if oltin_ok == jami and bosh_ok == jami else 1


# ---------------------------------------------------------------- sinov

def _soxta_mvn(pc, test, jacoco=False):
    """Maven o'rnida: qoida fayl matnidan. Faqat --sinov uchun."""
    pc = Path(pc)
    pv = matn(pc / OWNER / "PetValidator.java")
    oc = matn(pc / OWNER / "OwnerController.java")
    testlar = {}
    for f in (pc / OWNER_TEST).glob("*.java"):
        for nom in test_metodlari(matn(f)):
            testlar["%s.%s" % (f.stem, nom)] = True
    if test == TOLIQ_TOPLAM:
        tanlangan = list(testlar)
    else:
        sinflar = set(test.split(","))
        tanlangan = [k for k in testlar if k.split(".")[0] in sinflar]
    yiqilgan = []
    for k in tanlangan:
        if "MAX_NAME_LENGTH + 1" in pv and k == "PetValidatorTests.validateWithLongPetName":
            yiqilgan.append(k)
        if "if (name == null)" in pv and k.startswith("PetControllerTests.processCreationFormWithBlank"):
            yiqilgan.append(k)
        if "PageRequest.of(validatedPage, " in oc and "Sahifa" in k:
            yiqilgan.append(k)
    jami = len(tanlangan) + (BAZAVIY_TEST - 6 if test == TOLIQ_TOPLAM else 0)
    if jacoco:
        ow = matn(pc / OWNER / "Owner.java")
        ot = matn(pc / OWNER_TEST / "OwnerTests.java")
        jd = pc / "target" / "site" / "jacoco"
        jd.mkdir(parents=True, exist_ok=True)
        qq = []
        for nr, q in metod_qatorlari(ow, "void addPet("):
            if "pet == null" in q:
                mb = 0 if "addPet(null)" in ot else 1
                qq.append('<line nr="%d" mi="0" ci="2" mb="%d" cb="%d"/>' % (nr, mb, 2 - mb))
            elif "Objects.equals(" in q:
                cb = 4 if ("bir xil id" in ot and "yangi hayvon" in ot) else 2
                qq.append('<line nr="%d" mi="0" ci="9" mb="%d" cb="%d"/>' % (nr, 6 - cb, cb))
            elif "contains(pet)" in q:
                qq.append('<line nr="%d" mi="0" ci="3" mb="0" cb="2"/>' % nr)
        (jd / "jacoco.xml").write_text(
            '<report name="x"><package name="o"><sourcefile name="Owner.java">%s'
            '</sourcefile></package></report>' % "".join(qq), encoding="utf-8")
    return {"rc": 1 if yiqilgan else 0, "jami": jami, "yiqilgan": yiqilgan, "otgan": []}


SOXTA = {
    "PetValidator.java": "class PetValidator {\n\tprivate static final int MAX_NAME_LENGTH = 30;\n"
                         "\tvoid validate(String name) {\n\t\tif (!StringUtils.hasText(name)) {\n\t\t}\n"
                         "\t\telse if (name.length() > MAX_NAME_LENGTH) {\n\t\t}\n\t}\n}\n",
    "OwnerController.java": "class OwnerController {\n\tString processFindForm(int page) {\n"
                            "\t\treturn find(page);\n\t}\n\tPage find(int page) {\n"
                            "\t\tint validatedPage = Math.max(page, 1);\n"
                            "\t\treturn PageRequest.of(validatedPage - 1, 5);\n\t}\n}\n",
    "Owner.java": "class Owner {\n\tpublic void addPet(Pet pet) {\n\t\tif (pet == null) {\n\t\t\treturn;\n\t\t}\n"
                  "\t\tif (getPets().contains(pet)) {\n\t\t\treturn;\n\t\t}\n"
                  "\t\tfor (Pet existingPet : getPets()) {\n"
                  "\t\t\tif (!existingPet.isNew() && Objects.equals(existingPet.getId(), pet.getId())) {\n"
                  "\t\t\t\treturn;\n\t\t\t}\n\t\t}\n\t\tgetPets().add(pet);\n\t}\n"
                  "\tpublic Pet getPet(Integer id) {\n\t\tfor (Pet pet : getPets()) {\n"
                  "\t\t\tif (Objects.equals(pet.getId(), id)) {\n\t\t\t\treturn pet;\n\t\t\t}\n\t\t}\n"
                  "\t\treturn null;\n\t}\n"
                  "\tpublic Pet getPet(String name) {\n\t\tfor (Pet pet : getPets()) {\n"
                  "\t\t\tif (name.equals(pet.getName())) {\n\t\t\t\treturn pet;\n\t\t\t}\n\t\t}\n"
                  "\t\treturn null;\n\t}\n}\n",
    "VisitController.java": "class VisitController {\n}\n",
}
SOXTA_TEST = {
    "PetValidatorTests.java": "class PetValidatorTests {\n\t@Test\n\tvoid validateWithLongPetName() {\n"
                              "\t\tassertFalse(ok(\"x\".repeat(31)));\n\t}\n}\n",
    "PetControllerTests.java": "class PetControllerTests {\n\t@Test\n\tvoid processCreationFormWithBlankName() {\n"
                               "\t}\n\t@Test\n\tvoid processCreationFormWithBlankNameSpaces() {\n\t}\n}\n",
    "OwnerControllerTests.java": "class OwnerControllerTests {\n\t@Test\n\tvoid processFindFormSuccess() {\n\t}\n}\n",
    "PetTypeFormatterTests.java": "class PetTypeFormatterTests {\n\t@Test\n\tvoid shouldParse() {\n"
                                  "\t\tpetTypeFormatter.parse(\"Bird\", Locale.ENGLISH);\n\t}\n}\n",
    "OwnerTests.java": "class OwnerTests {\n\t@Test\n\tvoid addPetAddsPersistedPet() {\n\t\towner.addPet(pet);\n\t}\n}\n",
}


def _yangi_test(fayl, nom, tana):
    s = fayl.read_text(encoding="utf-8").rstrip()
    assert s.endswith("}")
    s = s[:-1] + "\t@Test\n\tvoid %s() {\n\t\t%s\n\t}\n}\n" % (nom, tana)
    fayl.write_text(s, encoding="utf-8")


def _almashtir(fayl, eski, yangi):
    s = fayl.read_text(encoding="utf-8")
    assert eski in s, (fayl, eski)
    fayl.write_text(s.replace(eski, yangi), encoding="utf-8")


# Har vazifa: (tayyorlov, oltin yechim). Ikkalasi soxta daraxtga funksiya.
def _sinov_holatlari(oltin_matn):
    m, t = OWNER, OWNER_TEST

    def bug1(p):
        _almashtir(p / m / "PetValidator.java", "> MAX_NAME_LENGTH)", "> MAX_NAME_LENGTH + 1)")

    def bug2(p):
        _almashtir(p / m / "PetValidator.java", "if (!StringUtils.hasText(name))", "if (name == null)")

    def bug3(p):
        _almashtir(p / m / "OwnerController.java", "of(validatedPage - 1, 5)", "of(validatedPage, 5)")

    def oltin1(p):
        _almashtir(p / m / "PetValidator.java", "MAX_NAME_LENGTH + 1)", "MAX_NAME_LENGTH)")

    def oltin2(p):
        _almashtir(p / m / "PetValidator.java", "if (name == null)", "if (!StringUtils.hasText(name))")

    def oltin3(p):
        _almashtir(p / m / "OwnerController.java", "of(validatedPage, 5)", "of(validatedPage - 1, 5)")
        _yangi_test(p / t / "OwnerControllerTests.java", "birinchiSahifaNoldan",
                    "verify(owners).find(argThat(p -> p.getPageNumber() == 0));")

    def oltin4(p):
        _almashtir(p / m / "OwnerController.java", "\t\treturn find(page);",
                   "\t\treturn natija(find(page));")

    def oltin5(p):
        s = SOXTA["Owner.java"]
        bosh = s.index("\tpublic Pet getPet(Integer id)")
        yangi = (s[:bosh] + "\tpublic Pet getPet(Integer id) {\n\t\treturn findPet(p -> Objects.equals(p.getId(), id)).orElse(null);\n\t}\n"
                 "\tpublic Pet getPet(String name) {\n\t\treturn findPet(p -> name.equals(p.getName())).orElse(null);\n\t}\n"
                 "\tprivate Optional<Pet> findPet(Predicate<Pet> shart) {\n"
                 "\t\treturn getPets().stream().filter(shart).findFirst();\n\t}\n}\n")
        (p / m / "Owner.java").write_text(yangi, encoding="utf-8")

    def oltin6(p):
        f = p / t / "PetTypeFormatterTests.java"
        _yangi_test(f, "kichikHarf", "assertThrows(() -> petTypeFormatter.parse(\"bird\", Locale.ENGLISH));")
        _yangi_test(f, "nullMatn", "assertThrows(() -> petTypeFormatter.parse(null, Locale.ENGLISH));")
        _yangi_test(f, "boshSatr", "assertThrows(() -> petTypeFormatter.parse(\"\", Locale.ENGLISH));")

    def oltin7(p):
        f = p / t / "OwnerTests.java"
        _yangi_test(f, "nullQoshilmaydi", "owner.addPet(null);")
        _yangi_test(f, "birXilIdQoshilmaydi", "// bir xil id li ikkinchi obyekt\n\t\towner.addPet(b);")
        _yangi_test(f, "yangiHayvonQoshiladi", "// yangi hayvon id siz\n\t\towner.addPet(c);")

    def dublikat6(p):
        f = p / t / "PetTypeFormatterTests.java"
        _yangi_test(f, "shouldParse2", "petTypeFormatter.parse(\"Bird\", Locale.ENGLISH);")
        _yangi_test(f, "kichikHarf", "assertThrows(() -> petTypeFormatter.parse(\"bird\", Locale.ENGLISH));")

    def test_tuzatish1(p):
        oltin1(p)
        _almashtir(p / t / "PetValidatorTests.java", "repeat(31)", "repeat(32)")

    def optional_param5(p):
        oltin5(p)
        _almashtir(p / m / "Owner.java", "private Optional<Pet> findPet(Predicate<Pet> shart)",
                   "private Optional<Pet> findPet(Predicate<Pet> shart, Optional<String> nom)")

    def kod8(p):
        _almashtir(p / m / "OwnerController.java", "5);", "10);")

    def bug3_testsiz(p):
        _almashtir(p / m / "OwnerController.java", "of(validatedPage, 5)", "of(validatedPage - 1, 5)")

    def bug3_qoriqlamaydi(p):
        bug3_testsiz(p)
        _yangi_test(p / t / "OwnerControllerTests.java", "boshqaTest", "assertTrue(true);")

    return {
        # raqam: (tayyorlov, oltin, [(nom, buzuq yechim)], javob oltin)
        1: (bug1, oltin1, [("test tahrirlangan", test_tuzatish1)], ""),
        2: (bug2, oltin2, [], ""),
        3: (bug3, oltin3, [("test yo'q", bug3_testsiz), ("test qo'riqlamaydi", bug3_qoriqlamaydi)], ""),
        4: (None, oltin4, [], ""),
        5: (None, oltin5, [("Optional parametr", optional_param5)], ""),
        6: (None, oltin6, [("dublikat + bitta holat", dublikat6)], ""),
        7: (None, oltin7, [], ""),
        8: (None, None, [("kod o'zgargan", kod8)], oltin_matn(8)),
        9: (None, None, [], oltin_matn(9)),
        10: (None, None, [], oltin_matn(10)),
    }


def _transkript(config, yozuvlar):
    d = Path(config) / "projects" / "-x"
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "s.jsonl", "w", encoding="utf-8") as f:
        for y in yozuvlar:
            f.write(json.dumps(y) + "\n")


def _tool(nom, inp):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": nom, "input": inp}]}}


def _user(t):
    return {"type": "user", "message": {"role": "user", "content": t}}


def sinov():
    xato = []

    def tek(shart, nom):
        print(("  ok   " if shart else "  XATO ") + nom)
        if not shart:
            xato.append(nom)

    def oltin_matn(n):
        return matn(umumiy.OLTIN / ("%02d.md" % n))

    with tempfile.TemporaryDirectory(prefix="ab-baho-") as t:
        t = Path(t)

        def daraxt_yarat(nom, tayyorlov):
            p = t / nom / "pc"
            (p / OWNER).mkdir(parents=True)
            (p / OWNER_TEST).mkdir(parents=True)
            for k, v in SOXTA.items():
                (p / OWNER / k).write_text(v, encoding="utf-8")
            for k, v in SOXTA_TEST.items():
                (p / OWNER_TEST / k).write_text(v, encoding="utf-8")
            if tayyorlov:
                tayyorlov(p)
            shutil.copytree(p, t / nom / "asl")
            return p, t / nom / "asl"

        oltin_soni = bosh_soni = 0
        for raqam, (tay, olt, buzuq, jav) in _sinov_holatlari(oltin_matn).items():
            pc, asl = daraxt_yarat("b%d" % raqam, tay)
            m0, _, _ = baho_mexanik(raqam, pc, asl, "", _soxta_mvn)
            bosh_soni += m0 == 0
            pc, asl = daraxt_yarat("o%d" % raqam, tay)
            if olt:
                olt(pc)
            m1, x1, iz1 = baho_mexanik(raqam, pc, asl, jav, _soxta_mvn)
            oltin_soni += m1 == 1
            if m1 != 1:
                print("       %d oltin: %s" % (raqam, "; ".join(iz1)))
            if raqam in (8, 9):
                tek(x1 == 4, "%d-vazifa oltin review: 4/4 nuqson kalit so'zda" % raqam)
            for nom, f in buzuq:
                pc, asl = daraxt_yarat("x%d%s" % (raqam, nom.replace(" ", "")), tay)
                f(pc)
                m, _, iz = baho_mexanik(raqam, pc, asl, jav, _soxta_mvn)
                tek(m == 0, "%d-vazifa buzuq yechim 0 oladi: %s" % (raqam, nom))
        tek(oltin_soni == 10, "oltin yechim %d/10" % oltin_soni)
        tek(bosh_soni == 10, "bo'sh yechim 0 olgani %d/10" % bosh_soni)
        tek(review_hisob(9, "BigDecimal ishlating, double pul uchun aniq emas") == ["R2-1"],
            "faqat 'BigDecimal ishlat' R2-1, R2-2 emas")
        tek(len(reja_hisob("Kod yozmang dedingiz, reja:\n1. BigDecimal")) < 5, "qisqa reja 5/7 olmaydi")

        # Ifloslanish
        def ifl(holat, yozuvlar):
            c = t / ("cfg%d" % len(list(t.glob("cfg*"))))
            if yozuvlar is not None:
                _transkript(c, yozuvlar)
            return ifloslanish(c, holat)

        tek(ifl("A", [_user("tuzat"), _tool("Read", {"file_path": "/pc/src/A.java"})]) == [],
            "A toza transkript")
        tek(ifl("A", [_tool("Skill", {"skill": "manguberdi"})]) == ["A: Skill(manguberdi)"],
            "A: Skill(manguberdi) ifloslaydi")
        tek(ifl("A", [_tool("Task", {"subagent_type": "review", "prompt": "x"})]) == ["A: aktyor review"],
            "A: Task(subagent_type=review) ifloslaydi")
        tek(ifl("A", [_tool("Agent", {"subagent_type": "general-purpose"})]) == [],
            "A: boshqa subagent ifloslamaydi")
        tek(ifl("A", [_user("<command-name>/manguberdi</command-name>")]) == ["A: /manguberdi"],
            "A: /manguberdi slash ifloslaydi")
        tek(ifl("B", [_user("<command-name>/manguberdi</command-name>"),
                      _tool("Task", {"subagent_type": "review"})]) == [],
            "B: manguberdi va aktyor - toza")
        tek(ifl("B", [_user("tuzat")]) == ["B: manguberdi yuklanmadi"], "B: manguberdi yo'q - yaroqsiz")
        tek(ifl("B", [_user("<command-name>/manguberdi</command-name>"),
                      _tool("Grep", {"pattern": "x", "path": "C:\\g\\eval\\ab\\vazifalar"})])
            == ["eval/ab yo'li: Grep"], "Windows yo'lidagi eval\\ab ham ushlanadi")
        tek(ifl("A", None) == ["transkript yo'q"], "transkript yo'q - yaroqsiz")

    print("baho --sinov: %s" % ("hammasi o'tdi" if not xato else "%d XATO" % len(xato)))
    return 1 if xato else 0


def asosiy(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("papka", nargs="?", help="yurish papkasi (yurgiz.py yaratgan)")
    p.add_argument("--holat", help="A yoki B (sukut: papka nomidan)")
    p.add_argument("--kalibr", action="store_true", help="oltin va bo'sh yechim, haqiqiy Maven")
    p.add_argument("--pc", help="--kalibr uchun petclinic repo (sukut: GitHub)")
    p.add_argument("--vazifa", help="--kalibr uchun vergul bilan raqamlar")
    p.add_argument("--sinov", action="store_true")
    a = p.parse_args(argv)
    if a.sinov:
        return sinov()
    if a.kalibr:
        faqat = {int(x) for x in a.vazifa.split(",")} if a.vazifa else None
        return kalibr(a.pc or umumiy.PETCLINIC_URL, faqat)
    if not a.papka:
        p.error("papka yoki --sinov/--kalibr kerak")
    papka = Path(a.papka)
    m = re.match(r"(\d+)-([AB])-", papka.name)
    if not m:
        p.error("papka nomi NN-H-k-uN shaklida emas")
    v = next(x for x in umumiy.vazifalar() if x.raqam == int(m.group(1)))
    natija = baholash(v, papka, a.holat or m.group(2))
    print(json.dumps(natija, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(asosiy())
