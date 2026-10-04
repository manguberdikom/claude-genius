#!/usr/bin/env python3
"""PostToolUse hook: yozilgan Java faylni qo'llanma qoidalariga solishtiradi.

    echo '<hook json>' | python3 tools/check_code.py
    python3 tools/check_code.py <fayl.java>     # qo'lda tekshirish

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
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from docref import hint  # noqa: E402
from state import was_marked  # noqa: E402

MAX_SHOWN = 6

STRING_RE = re.compile(r'"(?:\\.|[^"\\])*"')
LINE_COMMENT_RE = re.compile(r"//[^\n]*")
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)

HTTP_CLIENT_RE = re.compile(
    r"\b(restTemplate|webClient|restClient|httpClient|feignClient)\b", re.I)


def strip_noise(text):
    """Izoh va satr literallarini bo'sh joyga almashtiradi.

    Satr raqami saqlanishi kerak, shuning uchun o'chirilmaydi, balki
    bir xil uzunlikdagi probel bilan almashtiriladi.
    """
    def blank(match):
        return "".join("\n" if c == "\n" else " " for c in match.group(0))
    text = BLOCK_COMMENT_RE.sub(blank, text)
    text = LINE_COMMENT_RE.sub(blank, text)
    return STRING_RE.sub(blank, text)


class Finding:
    def __init__(self, level, line, message, topic, rule=""):
        self.level = level
        self.line = line
        self.message = message
        self.topic = topic
        self.rule = rule


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def check_text(text, path):
    """Faylning mexanik qoidalarga mosligi."""
    code = strip_noise(text)
    is_test = ("/test/" in path.replace("\\", "/")
               or os.path.basename(path).endswith(("Test.java", "Tests.java", "IT.java")))
    out = []

    for match in re.finditer(r"catch\s*\([^)]*\)\s*\{\s*\}", code):
        out.append(Finding(
            "yuqori", line_of(code, match.start()),
            "Bo'sh catch: xato yutiladi va hech qayerda ko'rinmaydi.",
            "Error Handling", "java:S108"))

    for match in re.finditer(r"catch\s*\(\s*(?:final\s+)?(Exception|Throwable)\s", code):
        out.append(Finding(
            "o'rta", line_of(code, match.start()),
            "`catch (%s)` kutilmagan xatolarni ham yutadi; aniq tur tutilsin."
            % match.group(1),
            "Error Handling", "java:S2221"))

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
            "Logging", "java:S1148"))

    # new BigDecimal(0.1) ikkilik kasrni aynan saqlamaydi; satr yoki valueOf kerak.
    for match in re.finditer(r"new\s+BigDecimal\s*\(\s*[-+]?\d+\.\d+", code):
        out.append(Finding(
            "yuqori", line_of(code, match.start()),
            "`new BigDecimal(double)` aniq qiymat bermaydi: "
            "`new BigDecimal(\"0.1\")` yoki `BigDecimal.valueOf(0.1)` ishlatilsin.",
            "Money", "java:S2111"))

    if is_test:
        for match in re.finditer(r"\bThread\.sleep\s*\(", code):
            out.append(Finding(
                "yuqori", line_of(code, match.start()),
                "Testda `Thread.sleep`: flaky test va sekin pipeline. "
                "Awaitility yoki deterministik kutish ishlatilsin.",
                "Flaky Test", "java:S2925"))

    out.extend(check_transactions(code))
    return out


def check_transactions(code):
    """@Transactional metod ichida tashqi HTTP chaqiruvi bormi.

    Metod chegarasi jingalak qavslarni sanash bilan topiladi. Bu to'liq
    parser emas, lekin annotatsiyadan keyingi birinchi blok uchun yetarli
    va noto'g'ri ishga tushishi kam: qavslar soni teng bo'lmasa, tekshiruv
    jim o'tadi.
    """
    out = []
    for match in re.finditer(r"@Transactional\b", code):
        start = code.find("{", match.end())
        if start == -1:
            continue
        depth, end = 0, -1
        for i in range(start, len(code)):
            if code[i] == "{":
                depth += 1
            elif code[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end == -1:
            continue
        body = code[start:end]
        call = HTTP_CLIENT_RE.search(body)
        if call:
            out.append(Finding(
                "yuqori", line_of(code, start + call.start()),
                "Tranzaksiya ichida tashqi chaqiruv (`%s`): ulanish tashqi "
                "servis javobini kutib band turadi va pool tugaydi."
                % call.group(0),
                "Transaction Script"))
    return out


def render(path, findings):
    lines = ["%s: %d ta qoida buzilishi" % (path, len(findings))]
    for f in findings[:MAX_SHOWN]:
        lines.append("[%s] %s:%d  %s" % (f.level, os.path.basename(path),
                                         f.line, f.message))
        lines.append("    %s%s" % (hint(f.topic, f.rule),
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


SKIPPED = (
    "Yozishdan oldin qoidalar olinmagan:\n"
    "    python3 tools/rules_for.py %s\n"
    "U tegishli boblarni, tekshiruv punktlarini va avvalgi xatolarni\n"
    "beradi. Reviewer aynan shu ro'yxat bilan tekshiradi, shuning uchun\n"
    "uni o'tkazib yuborish ikkinchi aylanani keltiradi."
)


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        findings = analyse(path)
        if not findings:
            print("%s: qoida buzilishi topilmadi." % path)
            return 0
        print(render(path, findings))
        return 1

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    tool_input = payload.get("tool_input") or {}
    response = payload.get("tool_response") or {}
    path = (response.get("filePath") or tool_input.get("file_path") or "")
    findings = analyse(path)

    # Zanjir qoidasi: .java yozilishidan oldin rules_for chaqirilgan
    # bo'lishi kerak. Bu ko'rsatma emas, shart: aks holda u unutiladi.
    if path.endswith(".java") and os.path.isfile(path) and not was_marked(path):
        reason = SKIPPED % path
        if findings:
            reason = render(path, findings) + "\n\n" + reason
        json.dump({"decision": "block", "reason": reason}, sys.stdout)
        return 0

    if not findings:
        return 0

    text = render(path, findings)
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
