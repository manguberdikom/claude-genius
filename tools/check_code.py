#!/usr/bin/env python3
"""PostToolUse hook: yozilgan Java faylni qo'llanma qoidalariga solishtiradi.

    echo '<hook json>' | python3 tools/check_code.py
    python3 tools/check_code.py <fayl.java>     # qo'lda tekshirish
    find src -name '*.java' -print0 | xargs -0 python3 tools/check_code.py

Bir nechta fayl bitta chaqiruvda: 800 faylda Python 800 marta emas, bir
marta ishga tushadi. Faqat buzilishi bor fayllar chiqadi, oxirida yig'ma
qator `check_code: N fayl, M buzilish`, shuning uchun grep kerak emas.

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

# in_clone, quote va tool_cmd docref da: rules_for ularni shu moduldan
# oladi, shuning uchun bu yerda qayta eksport qilinadi.
import hookio  # noqa: E402
from docref import hint, in_clone, quote, tool_cmd  # noqa: E402,F401
from state import marked_labels, was_marked  # noqa: E402

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

HTTP_CLIENT_RE = re.compile(
    r"\b(restTemplate|webClient|restClient|httpClient|feignClient)\b", re.I)
# Sinf darajasida faqat chaqiruv shakli olinadi: maydon e'loni
# (`RestTemplate restTemplate;`) va statik fabrika (`RestClient.create()`)
# tranzaksiya ichidagi tarmoq chaqiruvi emas.
CLIENT_CALL_RE = re.compile(
    r"\b(restTemplate|webClient|restClient|httpClient|feignClient)"
    r"\s*\.\s*\w+\s*\(")
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

    for match in re.finditer(r"catch\s*\(\s*(?:final\s+)?(Exception|Throwable)\s", code):
        out.append(Finding(
            "o'rta", line_of(code, match.start()),
            "`catch (%s)` kutilmagan xatolarni ham yutadi; aniq tur tutilsin."
            % match.group(1),
            "Error Handling", "java:S2221", term="catch"))

    for match in re.finditer(r"\bSystem\.(?:out|err)\.print", code):
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
    return out


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


def check_transactions(code):
    """@Transactional ichida tashqi HTTP chaqiruvi bormi.

    Metod chegarasi jingalak qavslarni sanash bilan topiladi. Bu to'liq
    parser emas, lekin annotatsiyadan keyingi birinchi blok uchun yetarli
    va noto'g'ri ishga tushishi kam: qavslar soni teng bo'lmasa, tekshiruv
    jim o'tadi. Tanasiz metod (interfeys, abstract) o'tkaziladi. Sinf
    darajasidagi annotatsiyada butun sinf tanasi ko'riladi, lekin faqat
    chaqiruv shakli va NOT_SUPPORTED/NEVER metodlaridan tashqarida.
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

    excluded = [(s, e) for s, e, no_tx, _ in blocks if no_tx]
    out, lines = [], set()
    for start, end, no_tx, is_type in blocks:
        if no_tx:
            continue
        if is_type:
            call = next((m for m in CLIENT_CALL_RE.finditer(code, start, end)
                         if not any(s <= m.start() < e for s, e in excluded)),
                        None)
        else:
            call = HTTP_CLIENT_RE.search(code, start, end)
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
    lines = ["%s: %d ta qoida buzilishi" % (path, len(findings))]
    for f in findings[:MAX_SHOWN]:
        lines.append("[%s] %s:%d  %s" % (f.level, os.path.basename(path),
                                         f.line, f.message))
        lines.append("    %s%s" % (hint(f.topic, f.rule, f.ref, f.term),
                                   "  (%s)" % f.rule if f.rule else ""))
    if len(findings) > MAX_SHOWN:
        lines.append("... yana %d ta" % (len(findings) - MAX_SHOWN))
    return "\n".join(lines)


def analyse(path):
    if not path.endswith(".java") or not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    except OSError:
        return []
    return check_text(text, path)


def new_signals(path):
    """rules_for chaqirilganda bo'lmagan, yozilgandan keyin chiqqan belgilar.

    Yozuvchi rules_for ni fayl hali yo'q yoki boshqacha paytda chaqiradi,
    reviewer esa yozilgan mazmundan oladi. Farq shu yerda aytiladi, aks
    holda reviewer ko'radigan bob yozuvchiga hech qachon yetmaydi.
    """
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
    """
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
    return 1 if total else 0


def main():
    if len(sys.argv) > 1:
        return check_paths(sys.argv[1:])

    payload = hookio.read_payload()
    if payload is None:
        return 0
    tool_input = payload.get("tool_input") or {}
    response = payload.get("tool_response") or {}
    path = (response.get("filePath") or tool_input.get("file_path") or "")
    findings = analyse(path)
    written = path.endswith(".java") and os.path.isfile(path)

    # Zanjir qoidasi: .java yozilishidan oldin rules_for chaqirilgan
    # bo'lishi kerak. Bu ko'rsatma emas, shart: aks holda u unutiladi.
    if written and not was_marked(path):
        reason = SKIPPED % (tool_cmd("rules_for.py"), quote(path))
        if findings:
            reason = render(path, findings) + "\n\n" + reason
        json.dump({"decision": "block", "reason": reason}, sys.stdout)
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
