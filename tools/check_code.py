#!/usr/bin/env python3
"""PostToolUse hook: yozilgan Java faylni qo'llanma qoidalariga solishtiradi.

    echo '<hook json>' | python3 tools/check_code.py
    python3 tools/check_code.py <fayl.java>     # qo'lda tekshirish
    find src -name '*.java' -print0 | xargs -0 python3 tools/check_code.py

Bir nechta fayl bitta chaqiruvda: 800 faylda Python 800 marta emas, bir
marta ishga tushadi. Faqat buzilishi bor fayllar chiqadi, oxirida yig'ma
qator `check_code: N fayl, M buzilish`, shuning uchun grep kerak emas.
Chiqish kodi: 0 toza, 1 buzilish bor, 3 .java bo'lmagan fayl tekshirilmadi.

NOSONAR izohli satr va `@SuppressWarnings("java:Sxxxx")` bilan o'ralgan
e'lon o'tkaziladi: Sonar ham ularni o'tkazadi. Hook rejimida Edit dan
oldingi mazmun (`originalFile`) bilan solishtiriladi va faqat yangi
topilma aytiladi.

Nega hook: qoidani CLAUDE.md da yozib qo'yish maslahat beradi, tekshirish
esa majburlaydi. Fayl yozilgandan keyin bu hook uni o'qiydi va qoidaga zid
joyni bo'lim raqami bilan qaytaradi, ya'ni xato keyingi review ga emas,
o'sha zahoti ko'rinadi.

Bu yerda FAQAT yolg'on ishga tushishi deyarli nol bo'lgan tekshiruvlar
bor. Har yozuvda shubhali ogohlantirish chiqarsa, hook o'chiriladi va
hech qanday qoida qolmaydi. Chuqurroq tahlil `review` agentida va
SonarQube da.

Sonar qoidalari (`check_sonar`: S1128, S8694, S6213, S5778, S8692, S1612,
S5838, S3415, S8696, S1135, S1068, S1144, S5853, S1488, S1845, S6126,
S3457, S2093, S4087, S5976; space-hrm dan 2026-10-09: S125, S2245, S2133,
S6068, S5841, S4144, S6878, S1640; lokal Sonar dan 2026-10-10: S6353, S6035,
S1123, S6355, S1192 bor konstanta, S3415 manfiy va char literal) va qo'llanmadagi ikki test qoidasi
(JVM system property ga yozish, static ArchUnit grafi; kalitsiz) tur ma'lumotisiz, regex va qavs sanash bilan. Ular haqiqiy loyihaning Sonar
ro'yxatiga solishtirib sozlangan. Tur kerak bo'lgan qoidalar (S1130,
S1874, S2184, S6809) ataylab yo'q: ular qo'llanmada qoida sifatida yoziladi
(sonarqube 28.17 va 30.15). S6878 va S1640 recordlar va enumlarni shu
fayldan va loyiha `src` papkasidan oladi; S5841 faqat kolleksiya ekaniga
dalil bor o'zgaruvchida (e'lon qilingan tur, `var x = ...collect(..)`). Daraja: `yuqori` hookni
to'sadi (S8694, S6213, S8696 value-based tur), qolganlari `o'rta`:
yozuvchiga eslatma.
"""

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hookio  # noqa: E402

# in_clone, quote, tool_cmd va hint docref da: rules_for va budget ularni
# shu moduldan oladi, shuning uchun qayta eksport qilinadi. docref va state
# kech yuklanadi: hook har yozuvda (.md, .py ham) ishga tushadi va .java
# bo'lmagan yo'lda ular kerak emas, importi esa ~10 ms.
_DOCREF_NAMES = ("hint", "in_clone", "quote", "tool_cmd")


def __getattr__(name):
    if name in _DOCREF_NAMES:
        import docref
        return getattr(docref, name)
    raise AttributeError("module %r has no attribute %r" % (__name__, name))


MAX_SHOWN = 6

# Izoh va literallar bitta o'tishda: qaysi biri matnda oldin boshlansa,
# o'sha yutadi. Avval uch regex ketma-ket yurardi va `"http://x"` ichidagi
# `//` izoh deb, `"image/*"` ichidagi `/*` blok izoh deb olinardi: satr
# qolgan qismi kod bo'lib qolar va toza kod to'silardi.
NOISE_RE = re.compile(
    r'"""(?:\\.|[^\\])*?"""'        # text block
    r'|"(?:\\.|[^"\\\n])*"'          # satr
    r"|'(?:\\.|[^'\\\n])+'"          # char
    r"|//[^\n]*"
    r"|/\*.*?\*/", re.S)

# Faqat chaqiruv shakli `nom.metod(` olinadi: tur nomi (`HttpClient.Version`,
# `WebClient.Builder builder`) va argument sifatida uzatilgan klient
# chaqiruv emas. Sinf darajasida registr muhim: maydon initsializatoridagi
# statik fabrika (`RestClient.create()`) tranzaksiya ichida yurmaydi.
# Metod tanasida esa `RestClient.create().get()` ham tarmoq chaqiruvi,
# shuning uchun u yerda registrsiz variant.
_CLIENT_CALL = (r"\b(restTemplate|webClient|restClient|httpClient|feignClient)"
                r"\s*\.\s*\w+\s*\(")
CLIENT_CALL_RE = re.compile(_CLIENT_CALL)
CLIENT_CALL_ANY_CASE_RE = re.compile(_CLIENT_CALL, re.I)
# Commit dan keyin yuradigan joy: TransactionSynchronization callbacklari va
# registerSynchronization argumenti. Qo'llanma tashqi chaqiruvni aynan shu
# yerga ko'chirishni tavsiya qiladi (patterns, code-review, architect).
AFTER_TX_RE = re.compile(r"\b(?:afterCommit|afterCompletion)\s*(?=\()")
REGISTER_SYNC_RE = re.compile(r"\bregisterSynchronization\s*(?=\()")
# Sinf darajasidagi @Transactional da listener metodi publisher tranzaksiyasi
# commit bo'lgandan keyin yuradi (default AFTER_COMMIT). BEFORE_COMMIT esa
# hali tranzaksiya ichida.
TX_LISTENER_RE = re.compile(r"@TransactionalEventListener\b")
TX_RE = re.compile(r"@Transactional\b")
# Tranzaksiyani o'chiradigan propagation: tanasidagi chaqiruv bu qoidaga
# tushmaydi.
NO_TX_RE = re.compile(
    r"propagation\s*=\s*(?:Propagation\s*\.\s*)?(?:NOT_SUPPORTED|NEVER)\b")
# Annotatsiyadan keyin sinf e'lon qilinadimi. `.class` (rollbackFor) va
# `record` nomli parametr e'lon emas.
TYPE_DECL_RE = re.compile(
    r"(?<![.\w])(?:class|interface|enum)\b|\brecord\s+\w+\s*[(<]")


def strip_noise(text):
    """Izoh, satr, char va text block literallarini bo'sh joyga almashtiradi.

    Satr raqami va pozitsiya saqlanishi kerak, shuning uchun o'chirilmaydi,
    balki bir xil uzunlikdagi probel bilan almashtiriladi.
    """
    return NOISE_RE.sub(
        lambda m: "".join("\n" if c == "\n" else " " for c in m.group(0)), text)


class Finding:
    def __init__(self, level, line, message, topic, rule="", ref="", term=""):
        self.level = level
        self.line = line
        self.message = message
        self.topic = topic
        self.rule = rule
        # Aniq bo'lim: kalit ham, taxallus ham mavzuga tushmasa. Indeksda
        # yo'q bo'lsa docref keyingisiga (kalit, taxallus) o'tadi.
        self.ref = ref
        # Kalit bir nechta bo'limda bo'lsa, tanasida shu so'z ko'p
        # uchragani olinadi (docref.by_rule). Usiz ulush kalitni
        # yo'l-yo'lakay eslatgan bo'limni tanlaydi.
        self.term = term


def strip_comments(text):
    """Faqat izohlar bo'sh joyga: literallar saqlanadi (argument bo'shligi,
    `@MethodSource("nom")` kabi satrdagi nom ko'rinishi uchun)."""
    return NOISE_RE.sub(
        lambda m: (re.sub(r"[^\n]", " ", m.group(0))
                   if m.group(0).startswith(("//", "/*")) else m.group(0)), text)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def check_text(text, path):
    """Faylning mexanik qoidalarga mosligi."""
    code = strip_noise(text)
    is_test = ("/test/" in path.replace("\\", "/")
               or os.path.basename(path).endswith(("Test.java", "Tests.java", "IT.java")))
    out = []

    for match in re.finditer(r"catch\s*\([^)]*\)\s*(\{\s*\})", code):
        # Izohli blok Sonar uchun bo'sh emas (java:S108 istisnosi). Izoh
        # strip_noise da o'chgan, shuning uchun asl matndan qaraladi:
        # pozitsiyalar bir xil.
        if re.search(r"//|/\*", text[match.start(1):match.end(1)]):
            continue
        out.append(Finding(
            "yuqori", line_of(code, match.start()),
            "Bo'sh catch: xato yutiladi va hech qayerda ko'rinmaydi.",
            "Error Handling", "java:S108"))

    # Keng tur: xato qayta otilishi ham mumkin, shuning uchun "yutadi"
    # deyilmaydi (yutish S108 ning ishi). Throwable Sonar da alohida kalit.
    for match in re.finditer(r"catch\s*\(\s*(?:final\s+)?(Exception|Throwable)\s", code):
        if match.group(1) == "Exception":
            out.append(Finding(
                "o'rta", line_of(code, match.start()),
                "`catch (Exception)` keng tur: kutilmagan xatolar ham tutiladi; "
                "aniq tur ko'rsatilsin.",
                "Error Handling", "java:S2221", term="catch"))
        else:
            out.append(Finding(
                "o'rta", line_of(code, match.start()),
                "`catch (Throwable)`: Error lar ham (OutOfMemoryError, "
                "StackOverflowError) tutiladi; aniq tur ko'rsatilsin.",
                "Error Handling", "java:S1181", term="catch"))

    # Sonar S106 ni test manbasiga qo'llamaydi.
    for match in ([] if is_test else re.finditer(r"\bSystem\.(?:out|err)\.print", code)):
        out.append(Finding(
            "o'rta", line_of(code, match.start()),
            "`System.out` o'rniga logger ishlatilsin: chiqish darajasi, "
            "formati va yo'nalishi boshqarilmaydi.",
            "Logging", "java:S106"))

    for match in re.finditer(r"\.printStackTrace\s*\(", code):
        out.append(Finding(
            "yuqori", line_of(code, match.start()),
            "`printStackTrace()` xatoni stderr ga tashlaydi va log tizimidan "
            "chetda qoladi.",
            "Logging", "java:S1148", term="printStackTrace"))

    # new BigDecimal(0.1) ikkilik kasrni aynan saqlamaydi; satr yoki valueOf kerak.
    # "Money" taxallusi Money value object patterniga olib boradi, konstruktor
    # tuzog'i esa clean-code dagi pul bo'limida.
    for match in re.finditer(r"new\s+BigDecimal\s*\(\s*[-+]?\d+\.\d+", code):
        out.append(Finding(
            "yuqori", line_of(code, match.start()),
            "`new BigDecimal(double)` aniq qiymat bermaydi: "
            "`new BigDecimal(\"0.1\")` yoki `BigDecimal.valueOf(0.1)` ishlatilsin.",
            "Money", "java:S2111", ref="clean-code 20.1"))

    if is_test:
        for match in re.finditer(r"\bThread\.sleep\s*\(", code):
            out.append(Finding(
                "yuqori", line_of(code, match.start()),
                "Testda `Thread.sleep`: flaky test va sekin pipeline. "
                "Awaitility yoki deterministik kutish ishlatilsin.",
                "Flaky Test", "java:S2925"))

    out.extend(check_transactions(code))
    out.extend(check_sonar(text, code, is_test, path))
    return suppress(out, text, code)


# ---------------------------------------------------------------------------
# Sonar qoidalari, aktyor yozgan koddagi eng ko'p uchraganlari.
#
# Hammasi regex va qavs sanash bilan, tur ma'lumotisiz. Tur kerak bo'lgan
# qoida (S1130, S2184, S6809, S1874) bu yerda yo'q: ular
# qo'llanmada qoida sifatida yoziladi (sonarqube 28.17, 30.15). Har
# tekshiruv noaniq joyda jim qoladi: yolg'on musbatdan ko'ra o'tkazib
# yuborilgan topilma yaxshi, chunki Sonar baribir ushlaydi.
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[\w$]+")
KEYWORDS = frozenset((
    "if", "for", "while", "switch", "catch", "synchronized", "return", "throw",
    "new", "else", "case", "assert", "do", "try", "yield", "instanceof",
    "super", "this", "default", "finally", "import", "package"))

IMPORT_RE = re.compile(r"^[ \t]*import\s+(static\s+)?([\w.]+?)(\.\*)?\s*;", re.M)
DOC_NAME_RE = re.compile(
    r"@(?:see|throws|exception)\s+([^\n*]*)|\{@(?:link|linkplain|value)\s+([^}]*)\}")

MONTH_NAMES = ("JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY",
               "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER")
# (tur, oy argumentining o'rni)
MONTH_FACTORIES = (("LocalDate", 1), ("LocalDateTime", 1), ("ZonedDateTime", 1),
                   ("OffsetDateTime", 1), ("YearMonth", 1), ("MonthDay", 0))
MONTH_OF_RE = re.compile(
    r"(?<![\w.$])(%s)\s*\.\s*of\s*(?=\()" % "|".join(t for t, _ in MONTH_FACTORIES))

RESTRICTED = "record|var|yield"
NOT_A_TYPE = KEYWORDS | {"var", "record"}
RESTRICTED_DECL_RE = re.compile(
    r"(?<![\w.$])([\w$]+(?:<[^;(){}=]*>)?(?:\[\])*)\s+(%s)\s*(?==|;|:|,|\)|\()" % RESTRICTED)
RESTRICTED_LAMBDA_RE = re.compile(r"(?<![\w.$])(%s)\s*->" % RESTRICTED)
LAMBDA_PARAMS_RE = re.compile(r"\(([^()]*)\)\s*->")

THROW_ASSERTS = ("assertThrows", "assertThrowsExactly", "assertThatThrownBy",
                 "isThrownBy")
CALL_RE = re.compile(r"(?<![\w$])([A-Za-z_$][\w$]*)\s*(?=\()")

SYSTEM_CLOCK_RE = re.compile(
    r"(?<![\w.$])(Instant|LocalDate|LocalDateTime|LocalTime|ZonedDateTime|"
    r"OffsetDateTime|OffsetTime|Year|YearMonth|MonthDay)\s*\.\s*now\s*(?=\()")
CLOCK_FACTORY_RE = re.compile(
    r"(?<![\w$])Clock\s*\.\s*(systemUTC|systemDefaultZone|system|tickSeconds|"
    r"tickMillis|tickMinutes|tick)\s*(?=\()")
ZONE_ARG_RE = re.compile(r"\b(?:ZoneId|ZoneOffset|[Zz]one\w*|ZONE\w*)\b")

LAMBDA_NULL_RE = re.compile(
    r"(?<![\w.$])([A-Za-z_$][\w$]*)\s*->\s*(?:\1\s*([!=])=\s*null|null\s*([!=])=\s*\1)"
    r"\s*(?=[,)])")
LAMBDA_CALL_RE = re.compile(
    r"(?<![\w.$])([A-Za-z_$][\w$]*)\s*->\s*\1\s*\.\s*([A-Za-z_$][\w$]*)\s*\(\s*\)"
    r"\s*(?=[,)])")
LAMBDA_STATIC_RE = re.compile(
    r"(?<![\w.$])([A-Za-z_$][\w$]*)\s*->\s*([A-Z][\w$.]*)\s*\.\s*([A-Za-z_$][\w$]*)"
    r"\s*\(\s*\1\s*\)\s*(?=[,)])")
LAMBDA_NEW_RE = re.compile(
    r"(?<![\w.$])([A-Za-z_$][\w$]*)\s*->\s*new\s+([A-Z][\w$.]*)\s*\(\s*\1\s*\)"
    r"\s*(?=[,)])")
LAMBDA_THIS_RE = re.compile(
    r"\(\s*\)\s*->\s*([a-z_$][\w$]*)\s*\.\s*([A-Za-z_$][\w$]*)\s*\(\s*\)\s*(?=[,)])")

MAP_DECL_RE = re.compile(
    r"(?<![\w$])\w*Map\s*<[^;=(){}]*>\s+([A-Za-z_$][\w$]*)\s*(?==|;|,|\)|\()")
CHAIN_RE = re.compile(r"\s*\.\s*([A-Za-z_$][\w$]*)\s*(?=\()")
ASSERT_THAT_RE = re.compile(r"(?<![\w.$])assertThat\s*(?=\()")
CONSTANT_RE = re.compile(r"(?:[\w$]+\s*\.\s*)*[A-Z][A-Z0-9_]*\Z")
# Manfiy son, o'n oltilik son va char ham literal: `assertEquals(count, -1)`
# va `assertEquals(c, 'a')` da kutilgan qiymat actual o'rnida (java:S3415).
LITERAL_RE = re.compile(
    r'(?:"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])+\'|-?0[xX][0-9a-fA-F_]+[Ll]?'
    r'|-?\d[\d_.]*[LlFfDd]?|true|false|null)\Z')
EQ_ASSERTS = ("assertEquals", "assertSame", "assertNotEquals", "assertNotSame")
AG_ORDERED = ("isEqualTo", "isNotEqualTo", "isSameAs", "isNotSameAs", "contains")
# Kutilgan qiymatni argument qilib oladigan boshqa AssertJ metodlari: ularda
# argument ko'pincha literal, shuning uchun faqat actual ning konstantaligi
# tekshiriladi (Sonar `assertThat(Type.EMPTY).hasToString("...")` ni ham tutadi).
AG_EXPECTED_ARG = ("hasToString", "hasSameHashCodeAs", "hasSameClassAs",
                   "isEqualToIgnoringCase", "isEqualToIgnoringWhitespace",
                   "isEqualByComparingTo", "isNotEqualByComparingTo")
SIZE_COMPARISONS = {
    "isGreaterThan": "hasSizeGreaterThan(n)",
    "isGreaterThanOrEqualTo": "hasSizeGreaterThanOrEqualTo(n)",
    "isLessThan": "hasSizeLessThan(n)",
    "isLessThanOrEqualTo": "hasSizeLessThanOrEqualTo(n)",
}
ARRAY_DECL_RE = re.compile(
    r"[\w$>]\s*\[\]\s+([A-Za-z_$][\w$]*)\s*(?==|;|,|\)|:)")
CONTAINS_CALL_RE = re.compile(
    r"\.\s*contains\s*\((?:[^()]|\((?:[^()]|\([^()]*\))*\))*\)\Z")

VALUE_TYPES = ("LocalDate", "LocalDateTime", "LocalTime", "Instant", "Duration",
               "Period", "YearMonth", "MonthDay", "Year", "ZonedDateTime",
               "OffsetDateTime", "OffsetTime", "Optional", "OptionalInt",
               "OptionalLong", "OptionalDouble")
VALUE_DECL_RE = re.compile(
    r"(?<![\w.$])(?:%s)(?:<[^;=(){}]*>)?\s+([A-Za-z_$][\w$]*)\s*(?==|;|,|\)|:)"
    % "|".join(VALUE_TYPES))
VALUE_CONST_RE = re.compile(r"(?:%s)\.(?:[A-Z][A-Z_0-9]*|now\(\)|of\w*\(.*\))\Z"
                            % "|".join(VALUE_TYPES))
JAVA_TIME_ENUM_RE = re.compile(r"(?:DayOfWeek|Month)\.[A-Z]+\Z")
EQ_OP_RE = re.compile(
    r"(?<![\w.$])([\w$]+(?:\s*\.\s*[\w$]+)*(?:\([^()]*\))?)\s*([!=]=)\s*"
    r"([\w$]+(?:\s*\.\s*[\w$]+)*(?:\([^()]*\))?)(?![\w$])")

FIELD_RE = re.compile(
    r"^[ \t]*((?:(?:public|protected|private|static|final|volatile|transient)\s+)+)"
    r"[\w<>\[\],.?& ]+?\s+([A-Za-z_$][\w$]*)\s*(?==|;)", re.M)
METHOD_RE = re.compile(
    r"^[ \t]*private\s+((?:static\s+|final\s+|synchronized\s+)*)"
    r"(?:<[^>]+>\s+)?[\w<>\[\],.?& ]+?\s+([A-Za-z_$][\w$]*)\s*\(", re.M)
SERIAL_METHODS = frozenset((
    "readObject", "writeObject", "readResolve", "writeReplace", "readObjectNoData"))

RETURN_NAME_RE = re.compile(r"(?<![\w$.])return\s+([A-Za-z_$][\w$]*)\s*;")
TEMP_DECL_RE = re.compile(
    r"\s*(?:final\s+)?[\w<>\[\],.?&]+(?:\s*<[^;=]*>)?(?:\[\])*\s+([A-Za-z_$][\w$]*)\s*=\s*[^;]+\Z")


def _split_args(code, open_idx, text=None):
    """`open_idx` dagi `(` ning argumentlari: ([(boshi, oxiri)...], yopuvchi pozitsiya).

    Faqat eng tashqi darajadagi vergullar bo'luvchi. Qavslar teng bo'lmasa
    (None, -1). Bo'sh argumentni `text` (literali bor matn) ajratadi:
    `code` da `""` bo'sh joy bo'lib qoladi.
    """
    source = code if text is None else text
    depth = 0
    start = open_idx + 1
    spans = []
    for i in range(open_idx, len(code)):
        c = code[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                if source[start:i].strip():
                    spans.append((start, i))
                return spans, i
        elif c == "," and depth == 1:
            spans.append((start, i))
            start = i + 1
    return None, -1


def _arg_texts(code, text, open_idx):
    """Argumentlar asl matndan (literal qiymati bilan), qirqilgan."""
    spans, close = _split_args(code, open_idx, text)
    if spans is None:
        return None, -1
    return [text[s:e].strip() for s, e in spans], close


def _find(rule, level, code, pos, message, topic, ref="", term=""):
    return Finding(level, line_of(code, pos), message, topic, rule, ref, term)


def check_unused_imports(text, code):
    """java:S1128. Ishlatilmagan import, statik import ham."""
    comments = " ".join(
        m.group(0) for m in NOISE_RE.finditer(text)
        if m.group(0).startswith("/*"))
    doc_names = set()
    for m in DOC_NAME_RE.finditer(comments):
        doc_names.update(WORD_RE.findall(m.group(1) or m.group(2)))
    body = IMPORT_RE.sub(lambda m: " " * len(m.group(0)), code)
    out = []
    for m in IMPORT_RE.finditer(code):
        if m.group(3):
            continue   # wildcard: qaysi nom ishlatilgani noma'lum
        static = bool(m.group(1))
        name = m.group(2).rsplit(".", 1)[-1]
        pattern = r"(?<![.\w$:])%s\b" % re.escape(name)
        if re.search(pattern, body) or (not static and name in doc_names):
            continue
        out.append(_find(
            "java:S1128", "o'rta", code, m.start(2),
            "Ishlatilmagan %simport `%s`: o'quvchiga yolg'on bog'liqlik "
            "ko'rsatadi; o'chirilsin." % ("statik " if static else "", m.group(2)),
            "Unused Code", ref="sonarqube 28.3"))
    return out


def check_month_literals(code):
    """java:S8694. LocalDate.of(2026, 10, 7): oy int literal, Month kerak."""
    out = []
    index = dict(MONTH_FACTORIES)
    for m in MONTH_OF_RE.finditer(code):
        args, _ = _split_args(code, m.end())
        pos = index[m.group(1)]
        if not args or len(args) <= pos:
            continue
        s, e = args[pos]
        arg = code[s:e].strip()
        if not re.match(r"\d{1,2}\Z", arg) or not 1 <= int(arg) <= 12:
            continue
        out.append(_find(
            "java:S8694", "yuqori", code, s,
            "`%s.of(...)` da oy int literal (%s): `Month.%s` ishlatilsin, "
            "int tartibi o'qilmaydi va oy/kun almashib ketadi."
            % (m.group(1), arg, MONTH_NAMES[int(arg) - 1]),
            "Date and Time", ref="sonarqube 30.15"))
    return out


def check_restricted_identifiers(code):
    """java:S6213. record, var, yield, sealed, permits, when nomli identifikator."""
    hits = {}
    for m in RESTRICTED_DECL_RE.finditer(code):
        if m.group(1) in NOT_A_TYPE:
            continue
        # `return record(x)` emas, `Type record(` e'lon: tur so'zi shart.
        hits.setdefault(m.start(2), m.group(2))
    for m in RESTRICTED_LAMBDA_RE.finditer(code):
        hits.setdefault(m.start(1), m.group(1))
    for m in LAMBDA_PARAMS_RE.finditer(code):
        offset = m.start(1)
        for part in m.group(1).split(","):
            tokens = part.split()
            if tokens and re.match(r"(?:%s)\Z" % RESTRICTED, tokens[-1]):
                hits.setdefault(offset + part.rindex(tokens[-1]), tokens[-1])
            offset += len(part) + 1
    return [_find(
        "java:S6213", "yuqori", code, pos,
        "`%s` cheklangan identifikator (Java kalit so'zi bo'lib qolishi mumkin): "
        "boshqa nom bering (`record` o'rniga `event`, `inputRecord`, `row`)." % name,
        "Naming", ref="sonarqube 28.17")
        for pos, name in sorted(hits.items())]


# Sonar S5778 shu zanjirlarda ishlaydi (isInstanceOfSatisfying, isSameAs va
# hasMessage da 0/37 ta topilma bergan: sinov kodi bazasida o'lchangan).
THROW_CHAINS = ("isInstanceOf", "isExactlyInstanceOf", "isNotInstanceOf",
                "isNotExactlyInstanceOf")
# Qiymat fabrikalari istisno tashlamaydi, ular chaqiruv hisobiga kirmaydi.
FACTORY_CALL_RE = re.compile(
    r"(?<![\w$.])(?:List|Set|Map|Arrays|Optional|UUID|Duration|Instant|"
    r"LocalDate|LocalDateTime|Collections)\s*\.\s*[A-Za-z_$][\w$]*\s*(?=\()")


def _blank_nested_lambdas(body):
    """Ichki lambda tanasini bo'sh joyga: `run(() -> "x")` dagi `run` tashqi
    chaqiruv, lambda ichi esa alohida hisoblanadi (tashqi lambdaning ikkinchi
    chaqiruvi emas)."""
    out = list(body)
    pos = 0
    while True:
        arrow = body.find("->", pos)
        if arrow == -1:
            return "".join(out)
        depth = 0
        end = len(body)
        for i in range(arrow + 2, len(body)):
            c = body[i]
            if c in "([{":
                depth += 1
            elif c in ")]}":
                if depth == 0:
                    end = i
                    break
                depth -= 1
            elif c == "," and depth == 0:
                end = i
                break
        for i in range(arrow + 2, end):
            if out[i] != "\n":
                out[i] = " "
        pos = end


def _count_calls(body):
    body = FACTORY_CALL_RE.sub(lambda m: " " * len(m.group(0)), body)
    return sum(1 for m in CALL_RE.finditer(body) if m.group(1) not in KEYWORDS)


def check_throwing_lambda(code):
    """java:S5778. assertThrows lambdasida bir nechta chaqiruv (heuristik).

    Faqat ifodali lambda (`() -> a.b(c.d())`) va `isInstanceOf` kabi zanjir
    yoki JUnit `assertThrows`: Sonar boshqa shaklni bayroqlamaydi, shuning
    uchun biz ham.
    """
    out = []
    for name in THROW_ASSERTS:
        for m in re.finditer(r"(?<![\w$])%s\s*(?=\()" % name, code):
            args, close = _split_args(code, m.end())
            if not args:
                continue
            arrow = next((code.find("->", s, e) for s, e in args
                          if "->" in code[s:e]), -1)
            if arrow == -1:
                continue
            lam = next((s, e) for s, e in args if s <= arrow < e)
            body = code[arrow + 2:lam[1]]
            if body.lstrip().startswith("{"):
                continue
            body = _blank_nested_lambdas(body)
            if name == "assertThatThrownBy":
                chain = re.match(r"\s*\.\s*(\w+)", code[close + 1:])
                if not chain or chain.group(1) not in THROW_CHAINS:
                    continue
            calls = _count_calls(body)
            if calls < 2:
                continue
            out.append(_find(
                "java:S5778", "o'rta", code, arrow,
                "`%s` lambdasida %d ta chaqiruv: qaysi biri istisno tashlagani "
                "noma'lum. Tayyorlashni lambdadan tashqariga chiqaring, "
                "ichida bitta chaqiruv qolsin." % (name, calls),
                "Test Quality", ref="sonarqube 30.3"))
    return out


def check_system_clock(code):
    """java:S8692. Testda tizim soati."""
    out = []
    for m in SYSTEM_CLOCK_RE.finditer(code):
        args, _ = _split_args(code, m.end())
        if args and not ZONE_ARG_RE.search(code[args[0][0]:args[0][1]]):
            continue   # `now(clock)`: soat berilgan
        out.append(_find(
            "java:S8692", "o'rta", code, m.start(),
            "Testda tizim soati (`%s.now(...)`): natija ishga tushgan vaqtga "
            "bog'liq. `Clock.fixed(...)` bering va kodga `Clock` inyeksiya qiling."
            % m.group(1), "Flaky Test", ref="clean-code 22.3"))
    for m in CLOCK_FACTORY_RE.finditer(code):
        out.append(_find(
            "java:S8692", "o'rta", code, m.start(),
            "Testda tizim soati (`Clock.%s(...)`): `Clock.fixed(Instant, ZoneId)` "
            "yoki `Clock.offset(fixed, ...)` ishlatilsin." % m.group(1),
            "Flaky Test", ref="clean-code 22.3"))
    return out


def _outside_strings(matches, lit, code):
    """`lit` da topilgan, lekin satr literali ichida boshlanmagan moslashuvlar."""
    return [m for m in matches if not (code[m.start()] == " " and lit[m.start()] != " ")]


def check_method_reference(lit, code):
    """java:S1612. `x -> x.foo()` va `x -> x == null` metod havolasi bo'la oladi."""
    out = []
    for m in _outside_strings(LAMBDA_NULL_RE.finditer(lit), lit, code):
        is_null = (m.group(2) or m.group(3)) == "="
        out.append(_find(
            "java:S1612", "o'rta", code, m.start(),
            "`%s -> %s %s= null` o'rniga `Objects::%s`."
            % (m.group(1), m.group(1), "=" if is_null else "!",
               "isNull" if is_null else "nonNull"),
            "Lambda", ref="clean-code 24.2"))
    for m in _outside_strings(LAMBDA_CALL_RE.finditer(lit), lit, code):
        out.append(_find(
            "java:S1612", "o'rta", code, m.start(),
            "`%s -> %s.%s()` o'rniga metod havolasi `Tur::%s`."
            % (m.group(1), m.group(1), m.group(2), m.group(2)),
            "Lambda", ref="clean-code 24.2"))
    for m in _outside_strings(LAMBDA_STATIC_RE.finditer(lit), lit, code):
        out.append(_find(
            "java:S1612", "o'rta", code, m.start(),
            "`%s -> %s.%s(%s)` o'rniga `%s::%s`."
            % (m.group(1), m.group(2), m.group(3), m.group(1), m.group(2), m.group(3)),
            "Lambda", ref="clean-code 24.2"))
    for m in _outside_strings(LAMBDA_NEW_RE.finditer(lit), lit, code):
        out.append(_find(
            "java:S1612", "o'rta", code, m.start(),
            "`%s -> new %s(%s)` o'rniga `%s::new`."
            % (m.group(1), m.group(2), m.group(1), m.group(2)),
            "Lambda", ref="clean-code 24.2"))
    for m in _outside_strings(LAMBDA_THIS_RE.finditer(lit), lit, code):
        out.append(_find(
            "java:S1612", "o'rta", code, m.start(),
            "`() -> %s.%s()` o'rniga `%s::%s`."
            % (m.group(1), m.group(2), m.group(1), m.group(2)),
            "Lambda", ref="clean-code 24.2"))
    return out


def _chain_after(code, close):
    """`assertThat(...)` dan keyingi birinchi mazmunli chaqiruv: (nom, qavs).

    `.as(...)`, `.describedAs(...)`, `.withFailMessage(...)` o'tkaziladi.
    Uchinchi qiymat: metod nomining pozitsiyasi (Sonar shu qatorni bayroqlaydi).
    """
    pos = close + 1
    while True:
        m = CHAIN_RE.match(code, pos)
        if not m:
            return None, -1, -1
        if m.group(1) in ("as", "describedAs", "withFailMessage", "overridingErrorMessage"):
            _, end = _split_args(code, m.end())
            if end == -1:
                return None, -1, -1
            pos = end + 1
            continue
        return m.group(1), m.end(), m.start(1)


def _is_constant(arg):
    return bool(CONSTANT_RE.match(arg) or LITERAL_RE.match(arg))


def _map_names(code):
    """Faylda `Map<...> nom` deb e'lon qilingan nomlar."""
    if "Map" not in code:
        return set()
    return set(m.group(1) for m in MAP_DECL_RE.finditer(code))


def _short(arg):
    arg = " ".join(arg.split())
    return arg if len(arg) <= 40 else arg[:37] + "..."


MAP_GET_RE = re.compile(
    r"(?:^|[.\s)])([A-Za-z_$][\w$]*)\s*(?:\((?:[^()]|\([^()]*\))*\))?\s*\.get\(([^()]+)\)\Z")


def _array_names(code):
    """Faylda `T[] nom` deb e'lon qilingan nomlar."""
    return set(m.group(1) for m in ARRAY_DECL_RE.finditer(code)) if "[]" in code else set()


def _better_assertion(actual, method, expected, maps, arrays=frozenset()):
    """AssertJ da aniqroq assertion bor bo'lsa uning tavsifi, aks holda "".

    Faqat tur ma'lumotisiz aniq holatlar: `toString()`, `size()`, bo'sh satr
    va e'lon qilingan `Map` dan `get`. `contains`, `isEmpty` kabilar maxsus
    sinfda ham bo'ladi (Sonar ularni bayroqlamadi), shuning uchun yo'q.
    """
    flat = " ".join(actual.split())
    sized = re.search(r"\.\s*size\(\)\Z", flat)
    length = re.search(r"([\w$]*)\s*(\)?)\s*\.\s*length\Z", flat)
    if length and (length.group(2) or length.group(1) in arrays):
        if method == "isEqualTo":
            return "massiv uzunligi uchun `hasSize(n)` ishlatilsin"
        if method in SIZE_COMPARISONS:
            return "massiv uzunligi uchun `%s` ishlatilsin" % SIZE_COMPARISONS[method]
    if sized and method in SIZE_COMPARISONS:
        return "`%s` ishlatilsin" % SIZE_COMPARISONS[method]
    if method in ("isTrue", "isFalse") and not expected and CONTAINS_CALL_RE.search(flat):
        if method == "isTrue":
            return "`contains(x)` ishlatilsin"
        return ("`doesNotContain(x)` ishlatilsin; u bo'sh kolleksiyada ham o'tadi "
                "(java:S5841), shuning uchun kirishni to'liq to'g'ri qilib "
                "`isEmpty()` bilan tekshiring yoki avval `isNotEmpty()` yozing")
    if method != "isEqualTo":
        return ""
    if expected == ['""']:
        return "`isEmpty()` ishlatilsin"
    if re.search(r"\.size\(\)\Z", flat):
        return "`hasSize(n)` (yoki `isEmpty()`) ishlatilsin"
    if re.search(r"\.toString\(\)\Z", flat):
        return "`hasToString(...)` ishlatilsin"
    mget = MAP_GET_RE.search(flat)
    if mget and mget.group(1) in maps and not re.match(r"\d+\Z", mget.group(2).strip()):
        return "`containsEntry(kalit, qiymat)` ishlatilsin"
    return ""


def check_assertions(code, text):
    """java:S5838 (maxsus assertion) va java:S3415 (argument tartibi)."""
    out = []
    maps = _map_names(code)
    arrays = _array_names(code)
    for m in ASSERT_THAT_RE.finditer(code):
        actual_args, close = _arg_texts(code, text, m.end())
        if not actual_args or len(actual_args) != 1:
            continue
        actual = actual_args[0]
        method, paren, at = _chain_after(code, close)
        if not method:
            continue
        expected_args, end = _arg_texts(code, text, paren)
        if expected_args is None:
            continue
        terminal = code[end + 1:].lstrip().startswith(";")
        better = _better_assertion(actual, method, expected_args, maps, arrays) if terminal else ""
        if better:
            out.append(_find(
                "java:S5838", "o'rta", code, at,
                "`assertThat(%s).%s(...)`: %s. Maxsus assertion xato xabarini "
                "ham aniq qiladi." % (_short(actual), method, better),
                "Test Quality", ref="sonarqube 30.15"))
        if (method in AG_ORDERED and len(expected_args) == 1
                and _is_constant(actual) and not _is_constant(expected_args[0])):
            out.append(_find(
                "java:S3415", "o'rta", code, m.start(),
                "`assertThat(%s)` da kutilgan qiymat actual o'rnida: "
                "argumentlarni almashtiring, `assertThat(haqiqiy).%s(%s)`."
                % (_short(actual), method, _short(actual)),
                "Test Quality", ref="sonarqube 30.15"))
        if (method in AG_EXPECTED_ARG and len(expected_args) == 1
                and CONSTANT_RE.match(actual) and not CONSTANT_RE.match(expected_args[0])):
            out.append(_find(
                "java:S3415", "o'rta", code, m.start(),
                "`assertThat(%s).%s(...)`: Sonar konstantani kutilgan qiymat deb "
                "biladi, actual o'rnida turibdi. Konstantani lokal o'zgaruvchiga "
                "oling (`var actual = %s;`) yoki haqiqiy qiymatni hisoblang."
                % (_short(actual), method, _short(actual)),
                "Test Quality", ref="sonarqube 30.15"))
    for name in EQ_ASSERTS:
        for m in re.finditer(r"(?<![\w$.])%s\s*(?=\()" % name, code):
            args, _ = _arg_texts(code, text, m.end())
            if not args or len(args) not in (2, 3):
                continue
            if len(args) == 3 and not args[2].startswith('"'):
                continue   # delta yoki JUnit 4 xabari: tartib noaniq
            if _is_constant(args[1]) and not _is_constant(args[0]):
                out.append(_find(
                    "java:S3415", "o'rta", code, m.start(),
                    "`%s(%s, %s)`: JUnit da avval kutilgan, keyin haqiqiy qiymat. "
                    "Literal birinchi argument bo'lsin." % (name, _short(args[0]),
                                                           _short(args[1])),
                    "Test Quality", ref="sonarqube 30.15"))
    return out


def _statement_end(code, start):
    """`start` dan boshlangan ifodaning `;` pozitsiyasi (qavs va blokdan tashqarida)."""
    depth = 0
    for i in range(start, len(code)):
        c = code[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth < 0:
                return -1
        elif c == ";" and depth == 0:
            return i
    return -1


# Zanjir shu metodlardan birini chaqirsa, keyingi tekshiruv boshqa obyektga
# o'tadi va birlashtirib bo'lmaydi.
NAVIGATION_RE = re.compile(
    r"\.\s*(?:extracting|flatExtracting|filteredOn|first|last|element|singleElement|"
    r"asInstanceOf|asList|asString|usingRecursive\w*|usingElementComparator|"
    r"usingComparator|extractingResultOf|map|isInstanceOfSatisfying)\s*\(")


def check_joined_assertions(code):
    """java:S5853. Ketma-ket assertThat(bir xil_nom) ... bitta zanjir bo'lsin."""
    stmts = []
    for m in ASSERT_THAT_RE.finditer(code):
        before = code[:m.start()].rstrip()
        if before and before[-1] not in ";{}":
            continue
        spans, _ = _split_args(code, m.end())
        end = _statement_end(code, m.start())
        if not spans or len(spans) != 1 or end == -1:
            continue
        subject = code[spans[0][0]:spans[0][1]].strip()
        if (re.match(r"[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*\Z", subject)
                and not NAVIGATION_RE.search(code[m.start():end])):
            stmts.append((m.start(), end, subject))
    out, i = [], 0
    while i < len(stmts):
        j = i
        while (j + 1 < len(stmts) and stmts[j + 1][2] == stmts[i][2]
               and not code[stmts[j][1] + 1:stmts[j + 1][0]].strip()):
            j += 1
        if j > i:
            out.append(_find(
                "java:S5853", "o'rta", code, stmts[i][0],
                "`assertThat(%s)` ketma-ket %d marta: bitta zanjirga "
                "birlashtiring (`assertThat(%s).a().b()`)."
                % (stmts[i][2], j - i + 1, stmts[i][2]),
                "Test Quality", ref="sonarqube 30.15"))
        i = j + 1
    return out


def _flat(token):
    return "".join(token.split())


def _value_based_expr(token, names):
    flat = _flat(token)
    return flat in names or bool(VALUE_CONST_RE.match(flat))


def check_value_based_equality(code):
    """java:S8696. LocalDate, Instant, Optional va boshqa value-based turni ==/!= bilan."""
    names = set(m.group(1) for m in VALUE_DECL_RE.finditer(code))
    out = []
    for m in EQ_OP_RE.finditer(code):
        left, right = m.group(1), m.group(3)
        if "null" in (left, right):
            continue
        if _value_based_expr(left, names) or _value_based_expr(right, names):
            out.append(_find(
                "java:S8696", "yuqori", code, m.start(),
                "Value-based tur `%s` da `%s`: identity solishtiriladi, qiymat "
                "emas. `.equals(...)` (yoki `isBefore`/`isAfter`) ishlatilsin."
                % (_short(left if _value_based_expr(left, names) else right), m.group(2)),
                "Equality", ref="sonarqube 28.17"))
        elif JAVA_TIME_ENUM_RE.match(_flat(right)) or JAVA_TIME_ENUM_RE.match(_flat(left)):
            out.append(_find(
                "java:S8696", "o'rta", code, m.start(),
                "`%s %s %s`: Sonar java.time enum (`DayOfWeek`, `Month`) ni ham "
                "value-based deb `==` da bayroqlaydi. `.equals(...)` yoki "
                "`switch` ishlatilsin." % (_short(left), m.group(2), _short(right)),
                "Equality", ref="sonarqube 28.17"))
    return out


def check_todo(text, code):
    """java:S1135. Izohdagi TODO."""
    out = []
    for m in NOISE_RE.finditer(text):
        chunk = m.group(0)
        if not chunk.startswith(("//", "/*")):
            continue
        for t in re.finditer(r"(?i)(?<![^\W\d_])todo(?![^\W\d_])", chunk):
            out.append(_find(
                "java:S1135", "o'rta", code, m.start() + t.start(),
                "`TODO` izohi Sonar issue (info) ochadi va gate dagi New Issues "
                "soniga kiradi. Ishni ticketga yozing, izohda esa cheklovni "
                "`Cheklov:` yoki `Known limitation:` deb bayon qiling.",
                "Technical Debt", ref="sonarqube 28.6"))
    seen, uniq = set(), []
    for f in out:
        if f.line not in seen:
            seen.add(f.line)
            uniq.append(f)
    return uniq


def _unannotated(code, pos):
    """E'lon oldidan annotatsiya yo'qmi: oldingi mazmunli belgi `;`, `{` yoki `}`."""
    before = code[:pos].rstrip()
    return not before or before[-1] in ";{}"


def check_unused_private(code, lit):
    """java:S1068 va java:S1144. Faylda nomi bir marta uchraydigan private maydon/metod."""
    if "lombok" in code:
        return []   # Lombok maydonni o'zi ishlatadi, kod ko'rinmaydi
    out = []
    # Satr literallari ham sanaladi: `@MethodSource("nom")` metodni ishlatadi.
    counts = collections.Counter(WORD_RE.findall(lit))

    def used(name):
        return counts[name] > 1

    for m in FIELD_RE.finditer(code):
        mods, name = m.group(1).split(), m.group(2)
        if "private" not in mods or name == "serialVersionUID" or used(name):
            continue
        if not _unannotated(code, m.start()):
            continue
        out.append(_find(
            "java:S1068", "o'rta", code, m.start(2),
            "`private` maydon `%s` hech qayerda ishlatilmaydi: o'chiring "
            "(testda ham)." % name, "Unused Code", ref="sonarqube 28.3"))
    for m in METHOD_RE.finditer(code):
        name = m.group(2)
        if name in SERIAL_METHODS or used(name) or not _unannotated(code, m.start()):
            continue
        out.append(_find(
            "java:S1144", "o'rta", code, m.start(2),
            "`private` metod `%s` hech qayerdan chaqirilmaydi: o'chiring." % name,
            "Dead Code", ref="sonarqube 28.4"))
    return out


def check_field_case(code):
    """java:S1845. Faqat harf registri bilan farqlanadigan ikki final maydon.

    Sonar `DOORS` (final) va `doors` (final emas) juftini bayroqlamadi, shuning
    uchun ikkalasi ham `final` bo'lishi shart. Kichik harfli nom bayroqlanadi.
    """
    by_lower = {}
    for m in FIELD_RE.finditer(code):
        mods, name = m.group(1).split(), m.group(2)
        if "final" in mods:
            by_lower.setdefault(name.lower(), {}).setdefault(name, m.start(2))
    out = []
    for names in by_lower.values():
        if len(names) < 2:
            continue
        for name, pos in names.items():
            if not name.isupper():
                other = next(n for n in names if n != name)
                out.append(_find(
                    "java:S1845", "o'rta", code, pos,
                    "Maydonlar `%s` va `%s` faqat registr bilan farqlanadi: "
                    "chalkashlik, `%s` nomini o'zgartiring." % (other, name, name),
                    "Naming", ref="sonarqube 28.17"))
    return sorted(out, key=lambda f: f.line)


def check_temp_return(code):
    """java:S1488. `T x = ...; return x;`."""
    out = []
    for m in RETURN_NAME_RE.finditer(code):
        before = code[:m.start()].rstrip()
        if not before.endswith(";"):
            continue
        stmt = before[:-1]
        cut = max(stmt.rfind(";"), stmt.rfind("{"), stmt.rfind("}"))
        decl = TEMP_DECL_RE.match(stmt[cut + 1:])
        if not decl or decl.group(1) != m.group(1):
            continue
        out.append(_find(
            "java:S1488", "o'rta", code, cut + 1 + decl.start(1),
            "`%s` vaqtinchalik o'zgaruvchi: ifodani to'g'ridan-to'g'ri `return` "
            "qiling." % m.group(1), "Clean Code", ref="sonarqube 28.17"))
    return out


STRING_LITERAL_RE = re.compile(r'"(?:\\.|[^"\\\n])*"')
NEWLINE_ESCAPE_RE = re.compile(r"(?<!\\)(?:\\\\)*\\n")
PLUS_RE = re.compile(r"\s*\+\s*")
PRINTF_RE = re.compile(
    r"(?<![\w$])(?:String\s*\.\s*format|[\w$.]*\bprintf)\s*(?=\()")
FORMATTED_RE = re.compile(r'("(?:\\.|[^"\\\n])*")\s*\.\s*formatted\s*(?=\()')
LOCALE_ARG_RE = re.compile(r"(?:[\w$.]*[Ll]ocale\w*|Locale\s*\.\s*\w+)\Z")


def _literals_only(text):
    """Faqat bir qatorli satr literallari qoladi: izoh, char va text block
    bo'sh joyga, pozitsiya saqlanadi."""
    def keep(m):
        s = m.group(0)
        if s.startswith('"') and not s.startswith('"""'):
            return s
        return re.sub(r"[^\n]", " ", s)
    return NOISE_RE.sub(keep, text)


def check_newline_concat(text):
    """java:S6126. `"a\\n" + "b"`: ichida \\n bor satr literallari `+` bilan qo'shilgan.

    Faqat ifodaning boshidagi literal zanjiri: `"a\\n" + "b" + x` da literallar
    chap-assotsiativ daraxtda alohida qism ifoda hosil qiladi, `x + "a\\n" +
    "b"` da esa yo'q. O'zgaruvchi oraga kirgan qismni text block ga
    o'tkazib bo'lmaydi, shuning uchun bunday zanjir bayroqlanmaydi.
    """
    lit = _literals_only(text)
    parts = list(STRING_LITERAL_RE.finditer(lit))
    out = []
    i = 0
    while i < len(parts):
        j = i
        while (j + 1 < len(parts)
               and PLUS_RE.fullmatch(lit[parts[j].end():parts[j + 1].start()])):
            j += 1
        starts_expression = not lit[:parts[i].start()].rstrip().endswith("+")
        if (j > i and starts_expression
                and any(NEWLINE_ESCAPE_RE.search(p.group(0)) for p in parts[i:j + 1])):
            out.append(_find(
                "java:S6126", "o'rta", lit, parts[i].start(),
                "Ichida `\\n` bor satr literallari `+` bilan qo'shilgan: "
                "text block (`\"\"\"`) ishlatilsin. Baytlar muhim bo'lsa (CRLF, "
                "PDF yoki binar format) `\\n` ni text blockda escape bilan saqlang.",
                "Strings", ref="sonarqube 30.15"))
        i = j + 1
    return out


def check_format_newline(code, text):
    """java:S3457. `String.format("..\\n", x)`: format satrida \\n, `%n` kerak."""
    out = []
    for m in PRINTF_RE.finditer(code):
        args, _ = _arg_texts(code, text, m.end())
        if not args:
            continue
        rest = [a for a in args if not LOCALE_ARG_RE.match(a)]
        fmt = rest[0] if rest else ""
        if not any(NEWLINE_ESCAPE_RE.search(lit)
                   for lit in STRING_LITERAL_RE.findall(fmt)):
            continue
        out.append(_find(
            "java:S3457", "o'rta", code, m.start(),
            "Format satrida `\\n`: platformaga bog'liq qator oxiri. `%n` "
            "yozilsin; baytlar muhim bo'lsa (`\\n` aynan kerak) formatdan "
            "tashqarida `append('\\n')` qiling.",
            "Strings", ref="sonarqube 30.15"))
    for m in FORMATTED_RE.finditer(_literals_only(text)):
        if NEWLINE_ESCAPE_RE.search(m.group(1)):
            out.append(_find(
                "java:S3457", "o'rta", code, m.start(1),
                "`formatted(...)` satrida `\\n`: `%n` yozilsin, baytlar muhim "
                "bo'lsa formatdan tashqarida qo'shing.",
                "Strings", ref="sonarqube 30.15"))
    return out


TRY_FINALLY_RE = re.compile(
    r"(?<![\w$.])([A-Za-z_$][\w$]*)\s*=\s*([^;{}]*);\s*try\s*(?=\{)")
CATCH_RE = re.compile(r"\s*catch\s*\(")
FINALLY_RE = re.compile(r"\s*finally\s*(?=\{)")


def _finally_block(code, try_open):
    """`try {` ning `{` idan boshlab `catch` lardan o'tib, `finally {` ning
    (`{` pozitsiyasi, `}` pozitsiyasi); `finally` yo'q bo'lsa None."""
    end = _block_end(code, try_open)
    while end != -1:
        m = CATCH_RE.match(code, end + 1)
        if not m:
            break
        close = _paren_end(code, m.end() - 1)
        brace = code.find("{", close) if close != -1 else -1
        if brace == -1:
            return None
        end = _block_end(code, brace)
    if end == -1:
        return None
    m = FINALLY_RE.match(code, end + 1)
    if not m:
        return None
    fin_end = _block_end(code, m.end())
    return (m.end(), fin_end) if fin_end != -1 else None


def _top_level(body):
    """Ichki `{...}` bloklari bo'sh joyga: shartli `if (r != null) { r.close(); }`
    qoidaga tushmaydi."""
    depth = 0
    out = []
    for c in body:
        if c == "{":
            depth += 1
        out.append(c if depth == 0 or c == "\n" else " ")
        if c == "}":
            depth -= 1
    return "".join(out)


def check_manual_close(code):
    """java:S2093. `T r = open(); try { .. } finally { r.close(); }`."""
    out = []
    for m in TRY_FINALLY_RE.finditer(code):
        if m.group(2).strip() == "null":
            continue
        fin = _finally_block(code, m.end())
        if not fin:
            continue
        body = _top_level(code[fin[0] + 1:fin[1]])
        close = re.search(
            r"(?:^|[;{}])\s*%s\s*\.\s*close\s*\(\s*\)\s*;" % re.escape(m.group(1)), body)
        if not close:
            continue
        out.append(_find(
            "java:S2093", "o'rta", code, m.start(1),
            "`%s` `finally` da qo'lda yopilmoqda: `try (T %s = ...) { ... }` "
            "(try-with-resources) ishlatilsin. `close()` tekshiriladigan "
            "istisno tashlasa: `interface X extends AutoCloseable { void "
            "close() throws SQLException; }` e'lon qiling va lambda bering."
            % (m.group(1), m.group(1)),
            "Resource Leak", ref="sonarqube 13.6"))
    return out


TRY_RES_RE = re.compile(r"(?<![\w$.])try\s*(?=\()")
RESOURCE_DECL_RE = re.compile(
    r"\s*(?:final\s+)?[\w$.<>?,\[\]\s]+?\s([\w$]+)\s*=")


def _resource_names(code, start, end):
    """`try (` ichidagi resurs nomlari: `T a = ..; U b = ..` yoki mavjud `a`."""
    names = []
    depth = 0
    seg = start
    for i in range(start, end + 1):
        c = ";" if i == end else code[i]
        if c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == ";" and depth <= 0:
            part = code[seg:i]
            seg = i + 1
            decl = RESOURCE_DECL_RE.match(part)
            if decl:
                names.append(decl.group(1))
            elif re.fullmatch(r"\s*[\w$]+\s*", part):
                names.append(part.strip())
    return names


def check_close_in_twr(code):
    """java:S4087. try-with-resources resursi tanada qo'lda yopilgan."""
    out = []
    for m in TRY_RES_RE.finditer(code):
        close = _paren_end(code, m.end())
        if close == -1:
            continue
        brace = re.compile(r"\s*(?=\{)").match(code, close + 1)
        if not brace:
            continue
        body_end = _block_end(code, brace.end())
        if body_end == -1:
            continue
        body = code[brace.end():body_end]
        for name in _resource_names(code, m.end() + 1, close):
            hit = re.search(r"(?<![\w$.])%s\s*\.\s*close\s*\(\s*\)" % re.escape(name), body)
            if hit:
                out.append(_find(
                    "java:S4087", "o'rta", code, brace.end() + hit.start(),
                    "`%s` try-with-resources resursi, tanada `close()` ortiqcha: "
                    "blok oxirida o'zi yopiladi. Yopilgandan keyingi holat "
                    "kerak bo'lsa, `try` dan chiqib tekshiring." % name,
                    "Resource Leak", ref="sonarqube 13.6"))
    return out


TEST_METHOD_RE = re.compile(
    r"@Test\b(?:\s*@[\w.]+(?:\s*\((?:[^()]|\([^()]*\))*\))?)*"
    r"\s*(?:public\s+|protected\s+|private\s+)?void\s+([\w$]+)\s*\(\s*\)"
    r"\s*(?:throws\s+[\w$.,\s]+)?(?=\{)")
NUMBER_RE = re.compile(r"(?<![\w$.])\d[\w.]*")


def check_similar_tests(text, code):
    """java:S5976. Bir xil shakldagi 3+ test, faqat literal farq qiladi."""
    lit = strip_comments(text)
    groups = collections.defaultdict(list)
    for m in TEST_METHOD_RE.finditer(code):
        end = _block_end(code, m.end())
        if end == -1:
            continue
        raw = re.sub(r"\s+", " ", lit[m.end() + 1:end]).strip()
        shape = NUMBER_RE.sub("N", STRING_LITERAL_RE.sub('"S"', raw))
        if len(shape) < 40 or shape == raw:
            continue
        groups[shape].append((m.start(), raw))
    out = []
    for items in groups.values():
        if len(items) >= 3 and len({raw for _, raw in items}) >= 2:
            out.append(_find(
                "java:S5976", "o'rta", code, items[0][0],
                "%d ta test bir xil shaklda, faqat kirish ma'lumoti farq qiladi: "
                "`@ParameterizedTest(name = \"{0}\")` + `@MethodSource` bilan "
                "bitta testga yig'ing (nomlar `Arguments.of(\"nom\", ...)` da "
                "saqlanadi)." % len(items),
                "Test Quality", ref="sonarqube 30.15"))
    return out


ENV_WRITE_RE = re.compile(
    r"\b(getSystemProperties|getSystemEnvironment)\s*\(\s*\)\s*\.\s*"
    r"(?:put|putAll|remove|clear)\s*(?=\()")
SET_PROPERTY_RE = re.compile(r"\bSystem\s*\.\s*setProperty\s*(?=\()")
PROPERTY_RESTORE_RE = re.compile(r"\bSystem\s*\.\s*(?:clearProperty|setProperties)\s*\(")
STATIC_GRAPH_RE = re.compile(
    r"\bstatic\s+(?:(?:final|volatile)\s+)*JavaClasses\s+([\w$]+)\s*([=;])")


def check_test_env_leak(code):
    """Testda JVM system property yoki environment ga yozish: fork ga sizadi."""
    out = []
    for m in ENV_WRITE_RE.finditer(code):
        out.append(_find(
            "", "o'rta", code, m.start(),
            "Testda `%s().put(..)`: `StandardEnvironment.getSystemProperties()` "
            "haqiqiy JVM `System.getProperties()` ni qaytaradi, yozilgan qiymat shu "
            "fork dagi keyingi testlarga sizadi va testlar tartibga bog'liq "
            "yiqiladi. `environment.getPropertySources().addFirst(new "
            "MapPropertySource(..))` ishlating." % m.group(1),
            "Flaky Test", ref="testing 15.14"))
    if not PROPERTY_RESTORE_RE.search(code):
        for m in SET_PROPERTY_RE.finditer(code):
            out.append(_find(
                "", "o'rta", code, m.start(),
                "Testda `System.setProperty(..)` va shu sinfda `clearProperty` yoki "
                "tiklash yo'q: qiymat fork dagi keyingi testlarga sizadi. Tiklang "
                "yoki `MapPropertySource` ni `addFirst` bilan qo'shing.",
                "Flaky Test", ref="testing 15.14"))
    return out


def check_static_archunit_graph(code):
    """Testda static `JavaClasses` maydoniga ClassFileImporter importi."""
    out = []
    for m in STATIC_GRAPH_RE.finditer(code):
        if m.group(2) == "=":
            end = _statement_end(code, m.end())
            loaded = end != -1 and "ClassFileImporter" in code[m.end():end]
        else:
            loaded = re.search(r"(?<![\w$.])%s\s*=\s*[^;]*ClassFileImporter"
                               % re.escape(m.group(1)), code) is not None
        if loaded:
            out.append(_find(
                "", "o'rta", code, m.start(),
                "Static `JavaClasses` maydoni: har import yuzlab MB lik graf, static "
                "maydon uni fork oxirigacha ushlaydi. Bir necha arxitektura testi bitta "
                "forkka tushsa test JVM `OutOfMemoryError` bilan o'ladi. Umumiy, "
                "`SoftReference` bilan keshlangan yordamchi yoki `@AnalyzeClasses` "
                "keshini ishlating.",
                "Flaky Test", ref="testing 15.14"))
    return out


# ---------------------------------------------------------------------------
# space-hrm Sonar ida chiqqan, lekin yuqoridagilar ushlamagan holatlar
# (2026-10-09): S125, S2245, S2133, S6068, S5841, S4144, S6878, S1640.
# ---------------------------------------------------------------------------

ENTITY_END_RE = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|\w+);\Z")


def _code_like_line(line):
    """sonar-java JavaFootprint EndWithDetector: qator `;`, `{` yoki `}` bilan tugaydi.

    `{@link X}` kabi juft figurali qavs va HTML entity (`&lt;`) kod emas.
    """
    if not line:
        return False
    if line.endswith(";"):
        return not ENTITY_END_RE.search(line)
    if line[-1] in "{}":
        return line.count("{") != line.count("}")
    return False


def _comment_lines(chunk):
    """Izohning mazmunli qatorlari: [(chunk ichidagi siljish, qator matni)]."""
    out, offset = [], 0
    for raw in chunk.split("\n"):
        s = raw.strip()
        if s.startswith("/*"):
            s = s.lstrip("/*").strip()
        elif s.startswith("//"):
            s = s.lstrip("/").strip()
        elif s.startswith("*") and not s.startswith("*/"):
            s = s.lstrip("*").strip()
        if s.endswith("*/"):
            s = s[:-2].rstrip()
        out.append((offset, s))
        offset += len(raw) + 1
    return out


def check_commented_code(text, code):
    """java:S125. Izoh qatori `;`, `{` yoki `}` bilan tugasa Sonar uni kodga o'xshatadi."""
    first_code = len(code) - len(code.lstrip())
    out = []
    for m in NOISE_RE.finditer(text):
        chunk = m.group(0)
        if m.start() < first_code or not chunk.startswith(("//", "/*")):
            continue   # fayl boshidagi sarlavha izohi Sonar da ham o'tadi
        if chunk.startswith("/**"):
            continue   # Javadoc: space-hrm da `;` bilan tugagan Javadoc qatorlari Sonar da toza
        for offset, line in _comment_lines(chunk):
            if _code_like_line(line):
                out.append(_find(
                    "java:S125", "o'rta", code, m.start() + offset,
                    "Izoh qatori `%s` bilan tugaydi: Sonar uni kommentga olingan "
                    "kod deb biladi. Haqiqiy kod bo'lsa o'chiring, gap bo'lsa "
                    "nuqta bilan tugating." % line[-1],
                    "Unused Code", ref="sonarqube 28.5"))
                break   # Sonar bitta izohga bitta topilma beradi
    return out


RANDOM_RE = re.compile(
    r"(?<![\w$])(?:ThreadLocalRandom\s*\.\s*current|Math\s*\.\s*random"
    r"|new\s+(?:java\s*\.\s*util\s*\.\s*)?Random)\s*(?=\()")


def check_insecure_random(code):
    """java:S2245 (hotspot, faqat main kod). SecureRandom bu yerga tushmaydi."""
    return [_find(
        "java:S2245", "o'rta", code, m.start(),
        "`%s` bashorat qilinadigan generator (Sonar hotspot): xavfsizlikka "
        "daxldor qiymat uchun `SecureRandom`. Faqat vaqtga yoyish (jitter) "
        "bo'lsa ham hotspot ko'rib chiqiladi: `SecureRandom` arzon."
        % " ".join(m.group(0).split()),
        "Security", ref="sonarqube 26.5") for m in RANDOM_RE.finditer(code)]


NEW_RE = re.compile(
    r"(?<![\w$.])new\s+[A-Za-z_$][\w$.]*\s*(?:<[^()<>]*(?:<[^()<>]*>[^()<>]*)*>)?\s*(?=\()")
GET_CLASS_RE = re.compile(r"\s*\.\s*getClass\s*\(\s*\)")


def check_new_get_class(code):
    """java:S2133. `new X(...).getClass()`: obyekt faqat sinfi uchun yaratiladi."""
    out = []
    for m in NEW_RE.finditer(code):
        _, close = _split_args(code, m.end())
        if close != -1 and GET_CLASS_RE.match(code, close + 1):
            out.append(_find(
                "java:S2133", "o'rta", code, m.start(),
                "`%s(...).getClass()`: obyekt faqat sinfi uchun yaratiladi; "
                "`X.class` yozing." % " ".join(m.group(0).split()),
                "Clean Code", ref="sonarqube 28.17"))
    return out


MOCK_WHEN_RE = re.compile(
    r"(?:(?<![\w$.])|(?<=Mockito\.)|(?<=BDDMockito\.))(?:when|given)\s*(?=\()")
MOCK_DO_WHEN_RE = re.compile(r"\)\s*\.\s*when\s*(?=\()")
MOCK_VERIFY_RE = re.compile(r"(?:(?<![\w$.])|(?<=Mockito\.))verify\s*(?=\()")
EQ_CALL_RE = re.compile(r"(?:[\w$]+\s*\.\s*)*eq\s*(?=\()")


def _all_eq(code, open_idx):
    """`(` dagi argumentlarning hammasi `eq(...)` mi (kamida bitta argument)."""
    spans, _ = _split_args(code, open_idx)
    if not spans:
        return False
    for s, e in spans:
        chunk = code[s:e]
        first = s + len(chunk) - len(chunk.lstrip())
        last = s + len(chunk.rstrip()) - 1
        m = EQ_CALL_RE.match(code, first)
        if not m:
            return False
        _, close = _split_args(code, m.end())
        if close != last:
            return False
    return True


def _last_call_open(code, s, e):
    """`code[s:e]` ifodasining oxirgi chaqiruvi `(` pozitsiyasi, aks holda -1."""
    end = s + len(code[s:e].rstrip()) - 1
    if end < s or code[end] != ")":
        return -1
    depth = 0
    for i in range(end, s - 1, -1):
        if code[i] == ")":
            depth += 1
        elif code[i] == "(":
            depth -= 1
            if depth == 0:
                return i
    return -1


def check_mockito_eq(code):
    """java:S6068. when/verify chaqiruvida hamma argument `eq(...)`: matcher ortiqcha."""
    if "eq" not in code:
        return []
    opens = []
    for m in MOCK_WHEN_RE.finditer(code):
        spans, _ = _split_args(code, m.end())
        if spans and len(spans) == 1:
            opens.append((m.start(), _last_call_open(code, *spans[0])))
    for rx in (MOCK_DO_WHEN_RE, MOCK_VERIFY_RE):
        for m in rx.finditer(code):
            _, close = _split_args(code, m.end())
            chain = CHAIN_RE.match(code, close + 1) if close != -1 else None
            if chain:
                opens.append((m.start(), chain.end()))
    return [_find(
        "java:S6068", "o'rta", code, at,
        "Mockito chaqiruvida hamma argument `eq(...)`: matcher ortiqcha, "
        "xom qiymatlarni yozing (`eq(null)` o'rniga `null`).",
        "Test Quality", ref="sonarqube 30.15")
        for at, op in opens if op != -1 and _all_eq(code, op)]


VACUOUS_ASSERTS = frozenset((
    "doesNotContain", "doesNotContainAnyElementsOf", "doesNotContainNull",
    "allMatch", "allSatisfy", "noneMatch", "noneSatisfy"))
NONEMPTY_ASSERTS = frozenset((
    "isNotEmpty", "hasSize", "hasSizeGreaterThan", "hasSizeGreaterThanOrEqualTo",
    "hasSizeBetween", "contains", "containsExactly", "containsExactlyInAnyOrder",
    "containsExactlyElementsOf", "containsOnly", "containsOnlyOnce", "containsAnyOf",
    "containsAnyElementsOf", "containsSequence", "containsSubsequence", "anyMatch",
    "anySatisfy", "satisfiesExactly", "satisfiesExactlyInAnyOrder",
    "hasAtLeastOneElementOfType", "hasOnlyOneElementSatisfying",
    "containsKey", "containsEntry", "containsKeys", "containsValue"))
# Shu metoddan keyin subyekt boshqa narsa (element, satr): bo'shlik masalasi yo'q.
SUBJECT_CHANGERS = frozenset((
    "first", "last", "element", "singleElement", "asString", "asInstanceOf",
    "extracting", "flatExtracting", "map", "filteredOn"))
COLLECTION_TYPES = ("List", "Set", "Collection", "Iterable", "Queue", "Deque",
                    "SortedSet", "NavigableSet", "Stream", "ArrayList", "LinkedList",
                    "HashSet", "LinkedHashSet", "TreeSet")
COLLECTION_RESULT_RE = re.compile(
    r"\.\s*(?:toList|toSet|toArray)\s*\(\s*\)\Z|\.\s*collect\s*\(|"
    r"new\s+(?:Array|Linked|Hash|Tree)(?:List|Set)|\.\s*stream\s*\(\s*\)")
# Bo'sh bo'lishi mumkin emas deb qabul qilinadigan manbalar.
LITERAL_COLLECTION_RE = re.compile(
    r"(?:List|Set|Stream)\s*\.\s*of\s*\(\s*[^\s)]|Arrays\s*\.\s*asList\s*\(\s*[^\s)]|"
    r"EnumSet\s*\.\s*(?:allOf|of)\s*\(")


def _collection_evidence(actual, code):
    """Tur ma'lumotisiz: actual kolleksiya ekaniga dalil bormi (aks holda S5841 jim).

    Dalil: e'lon qilingan tur (`List<..> x`, `T[] x`), `var x = ...collect(..)`
    yoki ifodaning o'zi `.stream()`/`.toList()` bilan tugashi. Satr (`String`, `CapturedOutput`)
    va noma'lum tur dalil emas: `doesNotContain` satrga ham yoziladi.
    """
    flat = " ".join(actual.split())
    if COLLECTION_RESULT_RE.search(flat):
        return True
    plain = re.match(r"(?:this\s*\.\s*)?([A-Za-z_$][\w$]*)\Z", flat)
    if not plain:
        return False   # metod chaqiruvi: space-hrm Sonar i `assertThat(columns())` ni bayroqlamaydi
    ident = re.escape(plain.group(1))
    decl = (r"(?<![\w$.])(?:(?:%s)(?:<[^;=(){}]*>)?|[\w$.]+(?:<[^;=(){}]*>)?\[\])\s+%s\s*(?==|;|,|\)|:)" %
            ("|".join(COLLECTION_TYPES), ident))
    if re.search(decl, code):
        return True
    for m in re.finditer(r"(?<![\w$.])var\s+%s\s*=\s*([^;]+);" % ident, code):
        if COLLECTION_RESULT_RE.search(" ".join(m.group(1).split())):
            return True
    return False


def _method_span(code, pos):
    """`pos` turgan metod tanasi (boshi, oxiri); topilmasa (0, len(code))."""
    best = (0, len(code))
    for m in METHOD_HEAD_RE.finditer(code, 0, pos):
        if m.group(1) in NOT_RETURN_TYPE:
            continue
        prev = PREV_TOKEN_RE.search(code[max(0, m.start() - 200):m.start()])
        if not prev or prev.group(1) in NOT_RETURN_TYPE:
            continue
        end = _block_end(code, m.end() - 1)
        if end >= pos:
            best = (m.end(), end)
    return best


def _asserted_nonempty_before(code, text, actual, pos):
    """Shu metodda oldin `assertThat(shu_actual)` zanjirida bo'sh emasligi tekshirilganmi."""
    start, _ = _method_span(code, pos)
    want = "".join(actual.split())
    for m in ASSERT_THAT_RE.finditer(code, start, pos):
        args, close = _arg_texts(code, text, m.end())
        if not args or len(args) != 1 or "".join(args[0].split()) != want:
            continue
        cursor = close + 1
        while True:
            call = CHAIN_RE.match(code, cursor)
            if not call:
                break
            cargs, end = _arg_texts(code, text, call.end())
            if cargs is None:
                break
            if _is_nonempty_check(call.group(1), cargs):
                return True
            cursor = end + 1
    return False


def _is_nonempty_check(name, args):
    if name == "hasSize":
        return args != ["0"]
    return name in NONEMPTY_ASSERTS or (
        name.startswith("hasSize") and not name.startswith("hasSizeLessThan"))


def check_vacuous_assertions(code, text):
    """java:S5841. doesNotContain/allMatch/... bo'sh kolleksiyada ham o'tadi."""
    out = []
    for m in ASSERT_THAT_RE.finditer(code):
        actual_args, close = _arg_texts(code, text, m.end())
        if not actual_args or len(actual_args) != 1:
            continue
        actual = actual_args[0]
        if (LITERAL_COLLECTION_RE.match(" ".join(actual.split()))
                or not _collection_evidence(actual, code)):
            continue
        nonempty, pos = False, close + 1
        while True:
            call = CHAIN_RE.match(code, pos)
            if not call:
                break
            name = call.group(1)
            args, end = _arg_texts(code, text, call.end())
            if args is None or name in SUBJECT_CHANGERS:
                break
            if _is_nonempty_check(name, args):
                nonempty = True
            elif name in VACUOUS_ASSERTS and not nonempty:
                if not _asserted_nonempty_before(code, text, actual, m.start()):
                    out.append(_find(
                        "java:S5841", "o'rta", code, call.start(1),
                        "`assertThat(%s).%s(...)` bo'sh kolleksiyada ham o'tadi: test "
                        "hech narsani tekshirmay yashil bo'lishi mumkin. Kirishni to'liq "
                        "to'g'ri qilib `isEmpty()` bilan tekshiring, yoki zanjirga "
                        "oldin `isNotEmpty()`/`hasSize(n)` qo'ying."
                        % (_short(actual), name),
                        "Test Quality", ref="sonarqube 30.15"))
                break
            pos = end + 1
    return out


def _brace_parents(code):
    """Har `{` ning o'rab turgan `{` i: {pozitsiya: ota pozitsiya yoki -1}."""
    parents, stack = {}, []
    for i, c in enumerate(code):
        if c == "{":
            parents[i] = stack[-1] if stack else -1
            stack.append(i)
        elif c == "}" and stack:
            stack.pop()
    return parents


METHOD_HEAD_RE = re.compile(
    r"(?<![\w$.])([A-Za-z_$][\w$]*)\s*\(([^()]*)\)\s*(?:throws\s+[\w$.,\s<>]+?)?\s*\{")
PREV_TOKEN_RE = re.compile(r"([\w$>\]]+)\s*\Z")
NOT_RETURN_TYPE = KEYWORDS | {
    "try", "record", "public", "protected", "private", "static", "final",
    "abstract", "synchronized", "native", "strictfp", "class", "enum", "interface"}


def _top_level_statements(code, start, end):
    """Tanadagi eng tashqi darajadagi `;` soni."""
    brace = paren = count = 0
    for c in code[start:end]:
        if c == "{":
            brace += 1
        elif c == "}":
            brace -= 1
        elif c == "(":
            paren += 1
        elif c == ")":
            paren -= 1
        elif c == ";" and brace == 0 and paren == 0:
            count += 1
    return count


def check_identical_methods(text, code):
    """java:S4144. Bitta sinfda tanasi bir xil, kamida 2 statementli ikki metod."""
    methods = []
    for m in METHOD_HEAD_RE.finditer(code):
        if m.group(1) in NOT_RETURN_TYPE:
            continue
        prev = PREV_TOKEN_RE.search(code[max(0, m.start() - 200):m.start()])
        if not prev or prev.group(1) in NOT_RETURN_TYPE:
            continue   # konstruktor, anonim sinf yoki chaqiruv
        open_idx = m.end() - 1
        close = _block_end(code, open_idx)
        if close == -1 or _top_level_statements(code, open_idx + 1, close) < 2:
            continue
        # Parametr turlari ham bir xil bo'lsin (nomlarsiz): Sonar
        # `normalizeCreate(CreateDto)` va `normalizeUpdate(UpdateDto)` ni bayroqlamaydi.
        params = re.sub(r"\s+[\w$]+\s*(?=,|\Z)", "", " ".join(m.group(2).split()))
        methods.append((m.group(1), m.start(1), open_idx,
                        (params, " ".join(text[open_idx + 1:close].split()))))
    if len(methods) < 2:
        return []
    parents = _brace_parents(code)
    seen, out = {}, []
    for name, at, open_idx, body in methods:
        key = (parents.get(open_idx), body)
        first = seen.setdefault(key, (name, at))
        if first[0] != name:
            out.append(_find(
                "java:S4144", "o'rta", code, at,
                "`%s` tanasi `%s` (%d-qator) bilan bir xil: bittasi ikkinchisini "
                "chaqirsin yoki umumiy metodga chiqarilsin."
                % (name, first[0], line_of(code, first[1])),
                "Clean Code", ref="sonarqube 28.14"))
    return out


RECORD_DECL_RE = re.compile(
    r"(?<![\w$.])record\s+([A-Z][\w$]*)\s*(?:<[^>(){}]*>)?\s*(?=\()")
ENUM_DECL_RE = re.compile(r"(?<![\w$.])enum\s+([A-Z][\w$]*)\b")
TYPE_FILE_LIMIT = 20000
_TYPE_CACHE = {}


def _declared_types(code):
    """Faylda e'lon qilingan recordlar ({nom: [komponentlar...]}) va enumlar."""
    records = {}
    for m in RECORD_DECL_RE.finditer(code):
        spans, _ = _split_args(code, m.end())
        if spans is None:
            continue
        comps = [WORD_RE.findall(code[s:e])[-1] for s, e in spans
                 if WORD_RE.findall(code[s:e])]
        records.setdefault(m.group(1), []).append(comps)
    return records, set(m.group(1) for m in ENUM_DECL_RE.finditer(code))


def _src_root(path):
    """Loyihaning `src` papkasi (ichida main yoki test bor); fayl diskda bo'lmasa None."""
    if not os.path.isfile(path):
        return None
    d = os.path.dirname(os.path.abspath(path))
    while True:
        if (os.path.basename(d) == "src"
                and any(os.path.isdir(os.path.join(d, x)) for x in ("main", "test"))):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def _project_types(code, path):
    """Shu fayl va loyiha `src` idagi recordlar va enumlar (tur ma'lumoti kerak bo'lganda)."""
    records, enums = _declared_types(code)
    root = _src_root(path)
    if root is None:
        return records, enums
    if root not in _TYPE_CACHE:
        found, found_enums, count = {}, set(), 0
        for base, _, names in os.walk(root):
            for name in names:
                count += 1
                if not name.endswith(".java") or count > TYPE_FILE_LIMIT:
                    continue
                try:
                    with open(os.path.join(base, name), encoding="utf-8",
                              errors="replace") as handle:
                        body = handle.read()
                except OSError:
                    continue
                if "record " not in body and "enum " not in body:
                    continue
                recs, ens = _declared_types(strip_noise(body))
                for key, lists in recs.items():
                    found.setdefault(key, []).extend(lists)
                found_enums |= ens
        _TYPE_CACHE[root] = (found, found_enums)
    cached_records, cached_enums = _TYPE_CACHE[root]
    merged = dict(cached_records)
    merged.update(records)   # fayldagi yangi matn diskdagidan ustun
    return merged, enums | cached_enums


TYPE_PATH = r"([A-Z][\w$]*(?:\s*\.\s*[A-Z][\w$]*)*)"
CASE_BIND_RE = re.compile(
    r"(?<![\w$.])case\s+(?:final\s+)?%s\s+([a-z_][\w$]*)\s*(?=->|when\b)" % TYPE_PATH)
INSTANCEOF_BIND_RE = re.compile(
    r"(?<![\w$.])instanceof\s+(?:final\s+)?%s\s+([a-z_][\w$]*)\b(?!\s*\()" % TYPE_PATH)


def _enclosing_end(code, pos):
    """`pos` turgan blokning yopuvchi `}` i; topilmasa -1."""
    depth = 0
    for i in range(pos, len(code)):
        if code[i] == "{":
            depth += 1
        elif code[i] == "}":
            depth -= 1
            if depth < 0:
                return i
    return -1


def _binding_scopes(code):
    """(tur, nom, boshi, oxiri, pozitsiya): pattern o'zgaruvchilari va ko'rinish sohasi."""
    out = []
    for m in CASE_BIND_RE.finditer(code):
        arrow = code.find("->", m.end())
        if arrow == -1:
            continue
        j = arrow + 2
        while j < len(code) and code[j].isspace():
            j += 1
        end = _block_end(code, j) if code[j:j + 1] == "{" else _statement_end(code, j)
        out.append((m.group(1), m.group(2), m.end(), end, m.start()))
    for m in INSTANCEOF_BIND_RE.finditer(code):
        out.append((m.group(1), m.group(2), m.end(),
                    _enclosing_end(code, m.end()), m.start()))
    return out


def check_record_pattern(code, path):
    """java:S6878. `case Rec r ->` / `instanceof Rec r` da r faqat accessor sifatida."""
    scopes = _binding_scopes(code)
    if not scopes:
        return []
    records, _ = _project_types(code, path)
    out = []
    for type_path, name, start, end, at in scopes:
        short = re.split(r"\s*\.\s*", type_path)[-1]
        if end == -1 or short not in records:
            continue
        used = []
        for u in re.finditer(r"(?<![\w$.])%s(?![\w$])" % re.escape(name), code[start:end]):
            acc = re.match(r"\s*\.\s*([A-Za-z_$][\w$]*)\s*\(\s*\)", code[start + u.end():end])
            if not acc or any(acc.group(1) not in comps for comps in records[short]):
                used = []
                break
            if acc.group(1) not in used:
                used.append(acc.group(1))
        # Sonar faqat record ning HAMMA komponenti o'qilganda bayroqlaydi
        # (space-hrm: 2 komponentdan bittasi o'qilgan joylar toza).
        if not used or any(set(comps) - set(used) for comps in records[short]):
            continue
        out.append(_find(
            "java:S6878", "o'rta", code, at,
            "`%s %s` faqat accessor (`%s.%s()`) uchun ishlatilgan: record pattern "
            "yozing, `%s(%s)`." % (short, name, name, used[0], short,
                                   ", ".join("var " + c for c in records[short][0])),
            "Clean Code", ref="sonarqube 28.17"))
    return out


HASHMAP_NEW_RE = re.compile(
    r"(?<![\w$])new\s+(?:java\s*\.\s*util\s*\.\s*)?HashMap\s*<\s*([\w$.]+)\s*,")
HASHMAP_DECL_RE = re.compile(
    r"(?<![\w$])(?:java\s*\.\s*util\s*\.\s*)?Map\s*<\s*([\w$.]+)\s*,[^;=(){}]*>\s*[A-Za-z_$][\w$]*\s*=\s*"
    r"new\s+(?:java\s*\.\s*util\s*\.\s*)?HashMap\s*<\s*>")


def check_enum_hashmap(code, path):
    """java:S1640. Kaliti enum bo'lgan HashMap: EnumMap ishlatilsin."""
    if "HashMap" not in code:
        return []
    candidates = [(m.group(1), m.start()) for rx in (HASHMAP_NEW_RE, HASHMAP_DECL_RE)
                  for m in rx.finditer(code)]
    if not candidates:
        return []
    _, enums = _project_types(code, path)
    return [_find(
        "java:S1640", "o'rta", code, at,
        "Kaliti enum (`%s`) bo'lgan `HashMap`: `new EnumMap<>(%s.class)` tezroq va "
        "kam xotira oladi. Null kalit kerak bo'lsa (EnumMap uni rad etadi) "
        "metodga sababli @SuppressWarnings(\"java:S1640\") qo'ying."
        % (key.rsplit(".", 1)[-1], key.rsplit(".", 1)[-1]),
        "Clean Code", ref="sonarqube 28.17")
        for key, at in candidates if key.rsplit(".", 1)[-1] in enums]


# ---------------------------------------------------------------------------
# Lokal Sonar ida chiqqan, lekin yuqoridagilar ushlamagan holatlar:
# S6353, S6035 (regex), S1123, S6355 (@Deprecated), S1192 (bor konstanta).
# ---------------------------------------------------------------------------

REGEX_CALL_RE = re.compile(
    r"(?:(?<![\w$])Pattern\s*\.\s*(?:compile|matches)"
    r"|\.\s*(?:matches|replaceAll|replaceFirst|split))\s*(?=\()")
PATTERN_ANNOTATION_RE = re.compile(r"(?<![\w$.])@Pattern\s*(?=\()")
REGEXP_ARG_RE = re.compile(r'regexp\s*=\s*("(?:\\.|[^"\\\n])*")\Z')
SINGLE_LITERAL_RE = re.compile(r'"(?:\\.|[^"\\\n])*"\Z')
WORD_CLASS_PARTS = frozenset(("A-Z", "a-z", "0-9", "_"))
WORD_CLASS_BODY_RE = re.compile(r"(?:A-Z|a-z|0-9|_)+\Z")
SINGLE_CHAR = r"[A-Za-z0-9_ ,;:/@#%&=~]"
SINGLE_CHAR_ALT_RE = re.compile(
    r"\((?:\?:)?(%s(?:\|%s)+)\)" % (SINGLE_CHAR, SINGLE_CHAR))


def _java_regex(literal):
    """Java satr literali (qo'shtirnoqli) ichidagi regex: `\\\\` va `\\"` ochiladi."""
    return re.sub(r'\\([\\"])', r"\1", literal[1:-1])


def _regex_classes(rx):
    """Regexdagi oddiy belgi sinflari va tuzilma bo'lmagan pozitsiyalar.

    Qaytaradi: ([(boshi, oxiri, tanasi, inkor)], pozitsiyalar). Pozitsiyalar:
    escape qilingan belgilar va sinf ichi, ya'ni guruh qavsi bo'la olmaydigan
    joylar. Ichma-ich sinf (`[a-z&&[^aeiou]]`) va kesishma o'tkaziladi.
    """
    classes, skip = [], set()
    n, i = len(rx), 0
    while i < n:
        c = rx[i]
        if c == "\\":
            skip.update((i, i + 1))
            i += 2
            continue
        if c != "[":
            i += 1
            continue
        j = i + 1
        negated = j < n and rx[j] == "^"
        if negated:
            j += 1
        k, nested = j, False
        while k < n:
            if rx[k] == "\\":
                k += 2
                continue
            if rx[k] == "[":
                nested = True
            elif rx[k] == "]" and k > j:
                break
            k += 1
        if k >= n:
            break
        skip.update(range(i, k + 1))
        body = rx[j:k]
        if not nested and "&&" not in body:
            classes.append((i, k + 1, body, negated))
        i = k + 1
    return classes, skip


def _concise_class(body, negated):
    """Belgi sinfining qisqa shakli (`\\d`, `\\w`) yoki ""."""
    if body == "0-9":
        return "\\D" if negated else "\\d"
    if WORD_CLASS_BODY_RE.match(body):
        parts = re.findall(r"A-Z|a-z|0-9|_", body)
        if len(parts) == 4 and set(parts) == WORD_CLASS_PARTS:
            return "\\W" if negated else "\\w"
    return ""


def _check_regex(literal, code, pos):
    """Bitta regex literalidagi S6353 va S6035."""
    rx = _java_regex(literal)
    if "[" not in rx and "|" not in rx:
        return []
    out = []
    classes, skip = _regex_classes(rx)
    for start, end, body, negated in classes:
        short = _concise_class(body, negated)
        if short:
            out.append(_find(
                "java:S6353", "o'rta", code, pos,
                "Regexda `%s` o'rniga `%s` yozilsin (Java literalida `%s`): "
                "qisqa belgi sinfi o'qishga oson." % (
                    rx[start:end], short, short.replace("\\", "\\\\")),
                "Strings", ref="clean-code 21.6"))
    for m in SINGLE_CHAR_ALT_RE.finditer(rx):
        if m.start() in skip:
            continue
        chars = m.group(1).split("|")
        out.append(_find(
            "java:S6035", "o'rta", code, pos,
            "Regexda bir belgili alternatsiya `%s` o'rniga belgi sinfi `[%s]` "
            "yozilsin." % (m.group(0), "".join(chars)),
            "Strings", ref="clean-code 21.6"))
    return out


def check_regex_literals(code, text):
    """java:S6353 va java:S6035. Regex kontekstidagi satr literali.

    Faqat bitta literaldan iborat birinchi argument: `Pattern.compile`,
    `Pattern.matches`, `matches`, `replaceAll`, `replaceFirst`, `split` va
    `@Pattern(regexp = ...)`. O'zgaruvchi yoki birlashtirilgan regex
    o'tkaziladi.
    """
    out = []
    for m in REGEX_CALL_RE.finditer(code):
        args, _ = _arg_texts(code, text, m.end())
        if args and SINGLE_LITERAL_RE.match(args[0]):
            out.extend(_check_regex(args[0], code, m.start()))
    for m in PATTERN_ANNOTATION_RE.finditer(code):
        args, _ = _arg_texts(code, text, m.end())
        for arg in args or ():
            found = REGEXP_ARG_RE.match(arg)
            if found:
                out.extend(_check_regex(found.group(1), code, m.start()))
    return out


ANNOTATION_RE = re.compile(r"@(?!interface\b)([A-Za-z_$][\w$.]*)")
DECL_MODIFIERS = frozenset((
    "public", "protected", "private", "static", "final", "abstract", "default",
    "synchronized", "native", "strictfp", "sealed", "transient", "volatile"))
DEPRECATED_NAMES = ("Deprecated", "java.lang.Deprecated")
JAVADOC_DEPRECATED_RE = re.compile(r"(?<![\w{])@deprecated\b")
OVERRIDE_BEFORE_RE = re.compile(
    r"@Override\s*(?:@[\w.]+\s*(?:\([^()]*\))?\s*)*\Z")


def _annotation_chain(code, pos):
    """`pos` dan boshlangan annotatsiyalar va modifikatorlar zanjiri.

    Qaytaradi: [(nom, boshi, argumentlar matni yoki None)].
    """
    chain, i, n = [], pos, len(code)
    while i < n:
        while i < n and code[i].isspace():
            i += 1
        m = ANNOTATION_RE.match(code, i)
        if m:
            j = m.end()
            k = j
            while k < n and code[k].isspace():
                k += 1
            args = None
            if k < n and code[k] == "(":
                close = _paren_end(code, k)
                if close == -1:
                    break
                args = code[k + 1:close]
                j = close + 1
            chain.append((m.group(1), m.start(), args))
            i = j
            continue
        word = WORD_RE.match(code, i)
        if word and word.group(0) in DECL_MODIFIERS:
            i = word.end()
            continue
        break
    return chain


def check_deprecated(code, text):
    """java:S1123 (Javadoc da `@deprecated` yo'q) va java:S6355 (argumentsiz).

    Javadoc `@Deprecated` dan oldin turgan blok: undan keyin annotatsiyalar
    zanjiri keladi. `@Override` li metod o'tkaziladi (Sonar ham).
    """
    javadoc = {}
    for m in NOISE_RE.finditer(text):
        chunk = m.group(0)
        if chunk.startswith("/**") and len(chunk) > 4:
            for name, start, _ in _annotation_chain(code, m.end()):
                if name in DEPRECATED_NAMES:
                    javadoc[start] = chunk
    out = []
    for m in ANNOTATION_RE.finditer(code):
        if m.group(1) not in DEPRECATED_NAMES:
            continue
        chain = _annotation_chain(code, m.start())
        overriding = (any(name == "Override" for name, _, _ in chain)
                      or OVERRIDE_BEFORE_RE.search(code[max(0, m.start() - 300):m.start()]))
        doc = javadoc.get(m.start())
        if not overriding and (doc is None or not JAVADOC_DEPRECATED_RE.search(doc)):
            out.append(_find(
                "java:S1123", "o'rta", code, m.start(),
                "`@Deprecated` bor, lekin Javadoc da `@deprecated` tegi yo'q: "
                "`@deprecated Use {@link X} instead.` deb sababni va almashtirishni yozing.",
                "Clean Code", ref="sonarqube 28.7"))
        args = chain[0][2] if chain else None
        if args is None or not args.strip():
            out.append(_find(
                "java:S6355", "o'rta", code, m.start(),
                "`@Deprecated` argumentsiz: `since` va `forRemoval` qo'shing, "
                "masalan `@Deprecated(since = \"2.0\", forRemoval = true)`.",
                "Clean Code", ref="sonarqube 28.7"))
    return out


CONSTANT_DECL_RE = re.compile(
    r"(?<![\w$.])(?:(?:public|protected|private)\s+)?"
    r"(?:static\s+final|final\s+static)\s+String\s+([A-Za-z_$][\w$]*)\s*=")
ANNOTATION_ARGS_RE = re.compile(r"(?<![\w$.])@(?!interface\b)[A-Za-z_$][\w$.]*\s*(?=\()")
MIN_LITERAL_LENGTH = 5


def _string_literals(text):
    """Bir qatorli satr literallari: [(boshi, oxiri, qiymat)]. Text block emas."""
    return [(m.start(), m.end(), m.group(0)[1:-1]) for m in NOISE_RE.finditer(text)
            if m.group(0).startswith('"') and not m.group(0).startswith('"""')]


def _enclosing_block(code, pos):
    """`pos` ni o'raydigan eng ichki `{...}`: (boshi, oxiri) yoki (0, len)."""
    stack, best = [], (0, len(code))
    for i, c in enumerate(code):
        if c == "{":
            stack.append(i)
        elif c == "}" and stack:
            start = stack.pop()
            if start < pos < i and i - start < best[1] - best[0]:
                best = (start, i)
    return best


def check_known_constant(code, text):
    """java:S1192 (tor holat). `static final String X = "abc"` bor, boshqa joyda `"abc"`.

    Takror soni sanalmaydi: Sonar e'lon qilingan konstantaning qiymatini
    nusxalagan har literalni ("Use already-defined constant") bayroqlaydi.
    Annotatsiya argumenti, boshqa konstantaning initsializatori va o'sha
    konstanta ko'rinmaydigan boshqa sinf tanasi o'tkaziladi.
    """
    if "static" not in code or "final" not in code:
        return []
    literals = _string_literals(text)
    if not literals:
        return []
    constants, declared = [], set()
    for m in CONSTANT_DECL_RE.finditer(code):
        first = next((lit for lit in literals if lit[0] >= m.end()), None)
        if (first and not text[m.end():first[0]].strip()
                and text[first[1]:].lstrip().startswith(";")):
            declared.add(first[0])
            if len(first[2]) >= MIN_LITERAL_LENGTH:
                constants.append((m.group(1), first[2], m.start()))
    if not constants:
        return []
    ranges = []
    for m in ANNOTATION_ARGS_RE.finditer(code):
        close = _paren_end(code, m.end())
        if close != -1:
            ranges.append((m.end(), close))
    out = []
    for name, value, at in constants:
        lo, hi = _enclosing_block(code, at)
        for start, _, other in literals:
            if (other != value or start in declared or not lo < start < hi
                    or any(a < start < b for a, b in ranges)):
                continue
            out.append(_find(
                "java:S1192", "o'rta", code, start,
                "Literal `\"%s\"` allaqachon `%s` konstantasi sifatida e'lon "
                "qilingan: shu konstantani ishlating." % (_short(value), name),
                "Clean Code", ref="sonarqube 27.8"))
    return out


def check_sonar(text, code, is_test, path=""):
    """Sonar qoidalari: tur ma'lumotisiz aniqlanadiganlari."""
    out = []
    out.extend(check_unused_imports(text, code))
    out.extend(check_month_literals(code))
    out.extend(check_restricted_identifiers(code))
    lit = strip_comments(text)
    out.extend(check_method_reference(lit, code))
    out.extend(check_value_based_equality(code))
    out.extend(check_todo(text, code))
    out.extend(check_unused_private(code, lit))
    out.extend(check_field_case(code))
    out.extend(check_temp_return(code))
    out.extend(check_newline_concat(text))
    out.extend(check_format_newline(code, text))
    out.extend(check_manual_close(code))
    out.extend(check_close_in_twr(code))
    out.extend(check_commented_code(text, code))
    out.extend(check_new_get_class(code))
    out.extend(check_identical_methods(lit, code))
    out.extend(check_record_pattern(code, path))
    out.extend(check_enum_hashmap(code, path))
    out.extend(check_regex_literals(code, text))
    out.extend(check_deprecated(code, text))
    out.extend(check_known_constant(code, text))
    if not is_test:
        out.extend(check_insecure_random(code))
    if is_test:
        out.extend(check_mockito_eq(code))
        out.extend(check_vacuous_assertions(code, text))
        out.extend(check_similar_tests(text, code))
        out.extend(check_throwing_lambda(code))
        out.extend(check_system_clock(code))
        out.extend(check_assertions(code, text))
        out.extend(check_joined_assertions(code))
        out.extend(check_test_env_leak(code))
        out.extend(check_static_archunit_graph(code))
    return out


def nosonar_lines(text):
    """Izohida NOSONAR bor satrlar. Satr literalidagi so'z hisoblanmaydi."""
    lines = set()
    for match in NOISE_RE.finditer(text):
        chunk = match.group(0)
        if chunk.startswith(("//", "/*")) and "NOSONAR" in chunk:
            lines.add(line_of(text, match.start() + chunk.index("NOSONAR")))
    return lines


def suppressed_ranges(text, code):
    """@SuppressWarnings bilan o'ralgan e'lonlar: (kalitlar, 1-satr, oxirgi satr).

    Annotatsiya `code` da qidiriladi (izohdagisi sanalmaydi), kalitlar esa
    asl matndan olinadi: strip_noise satr literalini o'chirgan, pozitsiya
    bir xil. Tanasiz e'lon (maydon) o'tkaziladi.
    """
    out = []
    for match in re.finditer(r"@SuppressWarnings\s*\(", code):
        close = _paren_end(code, match.end() - 1)
        if close == -1:
            continue
        keys = set(re.findall(r'"([^"]*)"', text[match.end():close]))
        start = _body_start(code, close + 1)
        end = _block_end(code, start) if start != -1 else -1
        if keys and end != -1:
            out.append((keys, line_of(code, match.start()), line_of(code, end)))
    return out


def suppress(findings, text, code):
    """Sonar o'tkazadigan joy: NOSONAR satri va @SuppressWarnings kaliti.

    Ongli istisnoga ogohlantirish shovqin: u har yozuvda takrorlanadi.
    """
    if "NOSONAR" not in text and "@SuppressWarnings" not in code:
        return findings
    quiet = nosonar_lines(text)
    ranges = suppressed_ranges(text, code)
    kept = []
    for f in findings:
        if f.line in quiet:
            continue
        names = {f.rule, f.rule.replace("java:", "squid:")} if f.rule else set()
        if any(names & keys and first <= f.line <= last
               for keys, first, last in ranges):
            continue
        kept.append(f)
    return kept


def _body_start(code, pos):
    """Annotatsiyadan keyingi e'lon tanasining `{` i; tanasiz bo'lsa -1.

    Qavs ichidagi `{` (masalan `rollbackFor = {IOException.class}`) tana
    emas, shuning uchun qavs chuqurligi sanaladi.
    """
    depth = 0
    for i in range(pos, len(code)):
        c = code[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif depth <= 0 and c in "{;":
            return i if c == "{" else -1
    return -1


def _paren_end(code, start):
    """`start` dagi `(` ning jufti; qavslar teng bo'lmasa -1."""
    depth = 0
    for i in range(start, len(code)):
        if code[i] == "(":
            depth += 1
        elif code[i] == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _block_end(code, start):
    """`start` dagi `{` ning jufti; qavslar teng bo'lmasa -1."""
    depth = 0
    for i in range(start, len(code)):
        if code[i] == "{":
            depth += 1
        elif code[i] == "}":
            depth -= 1
            if depth == 0:
                return i
    return -1


def _after_tx_ranges(code):
    """Commit dan keyin yuradigan bloklar: (boshi, oxiri) pozitsiyalari.

    `afterCommit()`/`afterCompletion(int)` metod tanasi va
    `registerSynchronization(...)` argumenti (anonim sinf yoki lambda).
    Chaqiruv (`sync.afterCommit();`) tanasiz, o'tkaziladi.
    """
    out = []
    for match in AFTER_TX_RE.finditer(code):
        start = _body_start(code, match.end())
        end = _block_end(code, start) if start != -1 else -1
        if end != -1:
            out.append((start, end))
    for match in REGISTER_SYNC_RE.finditer(code):
        end = _paren_end(code, match.end())
        if end != -1:
            out.append((match.end(), end))
    return out


def _listener_ranges(code):
    """@TransactionalEventListener metod tanalari, BEFORE_COMMIT dan tashqari."""
    out = []
    for match in TX_LISTENER_RE.finditer(code):
        start = _body_start(code, match.end())
        end = _block_end(code, start) if start != -1 else -1
        if end != -1 and "BEFORE_COMMIT" not in code[match.end():start]:
            out.append((start, end))
    return out


def check_transactions(code):
    """@Transactional ichida tashqi HTTP chaqiruvi bormi.

    Metod chegarasi jingalak qavslarni sanash bilan topiladi. Bu to'liq
    parser emas, lekin annotatsiyadan keyingi birinchi blok uchun yetarli
    va noto'g'ri ishga tushishi kam: qavslar soni teng bo'lmasa, tekshiruv
    jim o'tadi. Tanasiz metod (interfeys, abstract) o'tkaziladi. Sinf
    darajasidagi annotatsiyada butun sinf tanasi ko'riladi, lekin faqat
    chaqiruv shakli va NOT_SUPPORTED/NEVER metodlaridan tashqarida.

    Commit dan keyingi bloklar (afterCommit, registerSynchronization
    argumenti) ikkala darajada o'tkaziladi: qo'llanma tashqi chaqiruvni
    aynan shu yerga ko'chirishni tavsiya qiladi va hook o'z maslahatini
    to'smasligi kerak. Listener metodi faqat sinf darajasida o'tkaziladi:
    metodning o'z @Transactional i (REQUIRES_NEW) yangi tranzaksiya ochadi.
    """
    blocks = []
    for match in TX_RE.finditer(code):
        start = _body_start(code, match.end())
        if start == -1:
            continue
        end = _block_end(code, start)
        if end == -1:
            continue
        head = code[match.end():start]
        blocks.append((start, end, bool(NO_TX_RE.search(head)),
                       bool(TYPE_DECL_RE.search(head))))
    if not blocks:
        return []

    excluded = [(s, e) for s, e, no_tx, _ in blocks if no_tx]
    excluded += _after_tx_ranges(code)
    in_type = excluded + _listener_ranges(code)
    out, lines = [], set()
    for start, end, no_tx, is_type in blocks:
        if no_tx:
            continue
        pattern, skip = ((CLIENT_CALL_RE, in_type) if is_type
                         else (CLIENT_CALL_ANY_CASE_RE, excluded))
        call = next((m for m in pattern.finditer(code, start, end)
                     if not any(s <= m.start() < e for s, e in skip)), None)
        if not call or line_of(code, call.start()) in lines:
            continue
        lines.add(line_of(code, call.start()))
        out.append(Finding(
            "yuqori", line_of(code, call.start()),
            "Tranzaksiya ichida tashqi chaqiruv (`%s`): ulanish tashqi "
            "servis javobini kutib band turadi va pool tugaydi."
            % call.group(1),
            "Transaction Spanning Remote Calls"))
    return out


def render(path, findings):
    from docref import hint
    lines = ["%s: %d ta qoida buzilishi" % (path, len(findings))]
    for f in findings[:MAX_SHOWN]:
        lines.append("[%s] %s:%d  %s" % (f.level, os.path.basename(path),
                                         f.line, f.message))
        lines.append("    %s%s" % (hint(f.topic, f.rule, f.ref, f.term),
                                   "  (%s)" % f.rule if f.rule else ""))
    if len(findings) > MAX_SHOWN:
        lines.append("... yana %d ta" % (len(findings) - MAX_SHOWN))
    return "\n".join(lines)


def read_java(path):
    """.java fayl matni; .java emas, yo'q yoki o'qilmasa None."""
    if not path.endswith(".java") or not os.path.isfile(path):
        return None
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return None


def analyse(path):
    text = read_java(path)
    return [] if text is None else check_text(text, path)


def _source_line(text, line):
    lines = text.split("\n")
    return lines[line - 1].strip() if 0 < line <= len(lines) else ""


def _finding_key(f, text):
    # Satr raqami emas, mazmuni: Edit yuqorida satr qo'shsa ham eski
    # topilma eski bo'lib qoladi. Kaliti yo'q topilma mavzusi bilan.
    return (f.rule or f.topic, _source_line(text, f.line))


def only_new(findings, text, original, path):
    """Edit dan oldin ham bor bo'lgan topilmalar olib tashlanadi.

    Solishtirish multiset bo'yicha: (kalit, strip qilingan satr). Eski
    faylda bitta printStackTrace bo'lib, yangisida ikkita bo'lsa, bittasi
    yangi. Tegilgan satrdagi topilma (matni o'zgargan) ham yangi sanaladi.
    """
    old = {}
    for f in check_text(original, path):
        key = _finding_key(f, original)
        old[key] = old.get(key, 0) + 1
    fresh = []
    for f in findings:
        key = _finding_key(f, text)
        if old.get(key):
            old[key] -= 1
        else:
            fresh.append(f)
    return fresh


def new_signals(path):
    """rules_for chaqirilganda bo'lmagan, yozilgandan keyin chiqqan belgilar.

    Yozuvchi rules_for ni fayl hali yo'q yoki boshqacha paytda chaqiradi,
    reviewer esa yozilgan mazmundan oladi. Farq shu yerda aytiladi, aks
    holda reviewer ko'radigan bob yozuvchiga hech qachon yetmaydi.
    """
    from docref import quote, tool_cmd
    from state import marked_labels
    known = marked_labels(path)
    if known is None:
        return ""
    import rules_for   # kech: rules_for o'zi check_code ni import qiladi
    fresh = [(label, chapters) for label, chapters, _ in rules_for.detect([path])
             if label not in known]
    if not fresh:
        return ""
    lines = ["Yozilgandan keyin yangi belgi chiqdi, uning boblari "
             "yozuvchiga berilmagan:"]
    for label, chapters in fresh:
        lines.append("  %s -> %s" % (label, ", ".join("%s %s" % c for c in chapters)))
    lines.append("Punktlar: %s %s" % (tool_cmd("rules_for.py"), quote(path)))
    return "\n".join(lines)


# Klondagi sinov fixture lari: ular qoidani buzish uchun yoziladi va
# rules_for ro'yxati ularga hech narsa bermaydi (HK-H5).
FIXTURES = os.path.join(HERE, "testdata")


def is_fixture(path):
    """Yo'l klonning tools/testdata/ papkasi ichidami."""
    try:
        full = os.path.normcase(os.path.realpath(path))
        base = os.path.normcase(os.path.realpath(FIXTURES))
    except (OSError, ValueError):
        return False
    return full.startswith(base.rstrip(os.sep) + os.sep)


SKIPPED = (
    "Yozishdan oldin qoidalar olinmagan:\n"
    "    %s %s\n"
    "U tegishli boblarni, tekshiruv punktlarini va avvalgi xatolarni\n"
    "beradi. Reviewer aynan shu ro'yxat bilan tekshiradi, shuning uchun\n"
    "uni o'tkazib yuborish ikkinchi aylanani keltiradi."
)


def check_paths(paths):
    """CLI: har fayl tekshiriladi, buzilish bo'lsa 1.

    Avval faqat argv[1] olinardi: qolganlari jim tashlanar va rc 0 chiqardi.
    Bitta fayl uchun eski javob qoladi (toza fayl ham aytiladi). Ko'p
    faylda toza fayl qatori shovqin, o'rniga yig'ma qator bor: undagi
    fayl soni tekshiruv oxirigacha borganini ko'rsatadi.

    .java bo'lmagan fayl (Kotlin, Groovy) uchun "topilmadi" yolg'on: u
    tekshirilmagan. Shuning uchun alohida qator va rc 3 (buzilish bo'lsa
    baribir 1). Hook rejimi bunday yozuvda jim qoladi.
    """
    skipped = [p for p in paths if not p.endswith(".java")]
    for path in skipped:
        print("%s: tekshirilmadi (faqat .java)" % path)
    if len(paths) == 1 and skipped:
        return 3
    if len(paths) == 1:
        findings = analyse(paths[0])
        if not findings:
            print("%s: qoida buzilishi topilmadi." % paths[0])
            return 0
        print(render(paths[0], findings))
        return 1
    files = total = 0
    for path in paths:
        if not path.endswith(".java") or not os.path.isfile(path):
            continue
        files += 1
        findings = analyse(path)
        if findings:
            total += len(findings)
            print(render(path, findings))
    print("check_code: %d fayl, %d buzilish" % (files, total))
    return 1 if total else 3 if skipped else 0


def main():
    if len(sys.argv) > 1:
        return check_paths(sys.argv[1:])

    payload = hookio.read_payload()
    if payload is None:
        return 0
    tool_input = payload.get("tool_input") or {}
    response = payload.get("tool_response")
    response = response if isinstance(response, dict) else {}
    path = (response.get("filePath") or tool_input.get("file_path") or "")
    # .md, .py yozuvlari ko'pchilik: docref, state va proyekt ildizini
    # qidirmasdan chiqiladi.
    if not path.endswith(".java"):
        return 0
    if not hookio.active(payload):
        return 0   # CLI rejimi (argv) bu tekshiruvdan o'tmaydi
    text = read_java(path)
    written = text is not None
    findings = check_text(text, path) if written else []
    # Edit dan oldingi mazmun bo'lsa faqat shu yozuv keltirgan topilma
    # aytiladi: eski kodga har Edit da block modelni tegilmagan kodni
    # tuzatishga undaydi (diff kengayadi). Yangi faylda originalFile null.
    original = response.get("originalFile")
    if findings and isinstance(original, str):
        findings = only_new(findings, text, original, path)

    from docref import in_clone, quote, tool_cmd
    from state import was_marked

    # Zanjir qoidasi: .java yozilishidan oldin rules_for chaqirilgan
    # bo'lishi kerak. Bu ko'rsatma emas, shart: aks holda u unutiladi.
    #
    # Lekin shart faqat KLON ichida: u shu proyektning o'z konvensiyasi,
    # boshqa repoda esa hech kim unga rozi bo'lmagan. Global o'rnatishda
    # bu hook har Java proyektida yuradi va u yerda har birinchi .java
    # yozuvini to'sardi. Shuning uchun klondan tashqarida bu eslatma:
    # chaqiruv to'xtamaydi, ro'yxat esa taklif qilinadi.
    #
    # tools/testdata/ dagi fixture shartdan tashqarida: u ataylab buzuq
    # kod, unga qoidalar ro'yxati kerak emas. Mexanik tekshiruv qoladi.
    if written and not was_marked(path) and not is_fixture(path):
        reason = SKIPPED % (tool_cmd("rules_for.py"), quote(path))
        if findings:
            reason = render(path, findings) + "\n\n" + reason
        if in_clone():
            json.dump({"decision": "block", "reason": reason}, sys.stdout)
        else:
            json.dump({"hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": reason,
            }}, sys.stdout)
        return 0

    drift = new_signals(path) if written else ""
    if not findings and not drift:
        return 0

    text = "\n\n".join(x for x in (render(path, findings) if findings else "",
                                   drift) if x)
    high = [f for f in findings if f.level == "yuqori"]
    if high:
        # block: sabab modelga qaytariladi va navbat davom etadi, ya'ni
        # xato keyingi review ga qolmay, shu yerda tuzatiladi.
        json.dump({"decision": "block", "reason": text}, sys.stdout)
    else:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": text,
        }}, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
