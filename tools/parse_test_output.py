#!/usr/bin/env python3
"""Maven yoki Gradle test chiqishidan faqat muhimini ajratadi.

    mvn test | python3 tools/parse_test_output.py
    python3 tools/parse_test_output.py target/surefire-reports/out.txt

Nega: yiqilgan test 200-2000 qator chiqish beradi, undan kerakli uchta
qator: qaysi test, nima kutilgan edi, loyiha kodining qaysi qatorida.
Qolgani framework ichidagi stack va takrorlangan oqibatlar.

Testni qayta ishga tushirish sababni ko'rsatmaydi, chiqishni o'qish
ko'rsatadi. Shuning uchun bu asbob bor.
"""

import os
import re
import sys
from collections import OrderedDict

# Stack qatoridagi shu prefikslar framework, loyiha kodi emas.
FRAMEWORK = (
    "java.", "javax.", "jakarta.", "jdk.", "sun.", "com.sun.",
    "org.junit", "junit.", "org.opentest4j", "org.hamcrest", "org.assertj",
    "org.mockito", "net.bytebuddy", "org.objenesis",
    "org.springframework", "org.apache.maven", "org.apache.tools",
    "org.gradle", "worker.org.gradle", "org.testcontainers",
    "com.intellij", "jdk.internal",
)

# Modul prefiksi bo'lishi mumkin: "at app//shop.Foo.bar(...)" yoki
# "at java.base/jdk.internal...". U tashlanadi, sinf nomi qoladi.
FRAME_RE = re.compile(
    r"^\s*at (?:[\w$.]+/{1,2})?([\w$.]+)\.([\w$<>]+)\(([^)]*)\)")
# JUnit 5 va 4: "ClassName.method:123 message" yoki "[ERROR] Class.method"
MAVEN_FAIL_RE = re.compile(r"^\[ERROR\]\s+([\w$.]+)\.([\w$]+)(?::(\d+))?\s*(.*)$")
GRADLE_FAIL_RE = re.compile(r"^([\w$.]+)\s*>\s*([\w$ ]+?)\s+FAILED\s*$")
EXCEPTION_RE = re.compile(r"^\s*(?:Caused by:\s*)?([\w$.]*(?:Exception|Error))(?::\s*(.*))?$")
EXPECTED_RE = re.compile(
    r"expect(?:ed)?[:\s]*[<\[](.*?)[>\]].*?but was[:\s]*[<\[](.*?)[>\]]",
    re.I | re.S)
SUMMARY_RE = re.compile(
    r"Tests run:\s*(\d+),\s*Failures:\s*(\d+),\s*Errors:\s*(\d+)(?:,\s*Skipped:\s*(\d+))?")
# Gradle: "12 tests completed, 2 failed, 1 skipped"
GRADLE_SUMMARY_RE = re.compile(
    r"(\d+) tests? completed(?:,\s*(\d+) failed)?(?:,\s*(\d+) skipped)?")

MAX_SHOWN = 3


def is_project_frame(cls):
    return not cls.startswith(FRAMEWORK)


class Failure:
    def __init__(self, test):
        self.test = test
        self.exception = ""
        self.message = ""
        self.expected = None
        self.actual = None
        self.frame = ""

    def key(self):
        """Bir xil sabab bir marta ko'rsatiladi."""
        return (self.exception, self.message[:120], self.frame)

    def render(self):
        out = ["%s" % self.test]
        if self.exception or self.message:
            head = self.exception or ""
            if self.message:
                head = ("%s: %s" % (head, self.message)).strip(": ")
            out.append("    %s" % head[:300])
        if self.expected is not None:
            out.append("    kutilgan: %s" % self.expected[:120])
            out.append("    olingan : %s" % self.actual[:120])
        if self.frame:
            out.append("    kod     : %s" % self.frame)
        return "\n".join(out)


def split_blocks(lines):
    """Chiqishni yiqilish bloklariga bo'ladi.

    Blok yiqilgan test nomidan boshlanib, keyingi test nomigacha davom
    etadi. Shu tufayli stack qatorlari o'z testiga tegishli bo'ladi.
    """
    blocks = OrderedDict()
    current = None
    for line in lines:
        maven = MAVEN_FAIL_RE.match(line)
        gradle = GRADLE_FAIL_RE.match(line)
        if gradle:
            current = "%s.%s" % (gradle.group(1), gradle.group(2).strip())
            blocks.setdefault(current, [])
            continue
        if maven and not line.startswith("[ERROR] Tests run"):
            current = "%s.%s" % (maven.group(1), maven.group(2))
            blocks.setdefault(current, [])
            if maven.group(4):
                blocks[current].append(maven.group(4))
            continue
        if current is not None:
            blocks[current].append(line)
    return blocks


def parse_block(test, body):
    failure = Failure(test)
    text = "\n".join(body)

    match = EXPECTED_RE.search(text)
    if match:
        failure.expected = " ".join(match.group(1).split())
        failure.actual = " ".join(match.group(2).split())

    for line in body:
        if not failure.exception:
            exc = EXCEPTION_RE.match(line)
            if exc and exc.group(1):
                failure.exception = exc.group(1).rsplit(".", 1)[-1]
                failure.message = " ".join((exc.group(2) or "").split())
        frame = FRAME_RE.match(line)
        if frame and not failure.frame and is_project_frame(frame.group(1)):
            failure.frame = "%s.%s(%s)" % (
                frame.group(1).rsplit(".", 1)[-1], frame.group(2), frame.group(3))

    if not failure.exception and not failure.expected:
        first = next((l.strip() for l in body if l.strip()), "")
        failure.message = " ".join(first.split())[:200]
    return failure


def summarize(lines):
    totals = None
    for line in lines:
        gradle = GRADLE_SUMMARY_RE.search(line)
        if gradle:
            run, fail, skip = (int(g or 0) for g in gradle.groups())
            totals = [run, fail, 0, skip]
            continue
        match = SUMMARY_RE.search(line)
        if match:
            run, fail, err, skip = (int(g or 0) for g in match.groups())
            if totals is None:
                totals = [0, 0, 0, 0]
            # Maven har modul uchun va oxirida umumiy qator chiqaradi;
            # eng kattasi umumiy natija.
            totals = [max(a, b) for a, b in zip(totals, (run, fail, err, skip))]
    return totals


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.exists(path):
            print("fayl yo'q: %s" % path, file=sys.stderr)
            return 2
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.read().split("\n")
    else:
        lines = sys.stdin.read().split("\n")

    totals = summarize(lines)
    blocks = split_blocks(lines)
    failures = [parse_block(t, b) for t, b in blocks.items()]

    unique = OrderedDict()
    for failure in failures:
        unique.setdefault(failure.key(), failure)
    unique = list(unique.values())

    if totals:
        print("Tests: %d, yiqildi: %d, xato: %d, o'tkazildi: %d"
              % tuple(totals))
    if not unique:
        print("Yiqilgan test topilmadi.")
        return 0

    print("Noyob sabab: %d ta (jami %d ta yiqilish)\n"
          % (len(unique), len(failures)))
    for failure in unique[:MAX_SHOWN]:
        print(failure.render())
        print()
    if len(unique) > MAX_SHOWN:
        print("... yana %d ta sabab" % (len(unique) - MAX_SHOWN))
    print("Birinchisidan boshlang: keyingilari ko'pincha shuning oqibati.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
