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
"""

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
    return suppress(out, text, code)


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
    if written and not was_marked(path):
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
