#!/usr/bin/env python3
"""hookio.py uchun sinovlar.

    python3 tools/test_hookio.py

Windows holati oqim bilan taqlid qilinadi: cp1252 li TextIOWrapper
(matnli sys.stdin aynan shunday) va PowerShell 5.1 qo'yadigan BOM.
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hookio  # noqa: E402

BOM = b"\xef\xbb\xbf"
PROMPT = "o\u02bbzbekcha \u0441\u0445\u0435\u043c\u0430"   # o'zbekcha va ruscha harf


def windows_stdin(data):
    """Windows dagi pipe: baytlar ustida cp1252 li matnli oqim."""
    return io.TextIOWrapper(io.BytesIO(data), encoding="cp1252")


class Tty(io.StringIO):
    def isatty(self):
        return True


class Broken(io.StringIO):
    def read(self, *args):
        raise OSError("yopiq")


def cases():
    utf8 = ('{"prompt": "%s"}' % PROMPT).encode("utf-8")
    return [
        ("cp1252 oqimda UTF-8 to'g'ri",
         hookio.read_payload(windows_stdin(utf8)), {"prompt": PROMPT}),
        ("BOM va CRLF tashlanadi",
         hookio.read_payload(windows_stdin(BOM + b'{"a": 1}\r\n')), {"a": 1}),
        ("StringIO (bufersiz) ham o'qiladi",
         hookio.read_payload(io.StringIO('\ufeff{"a": 2}')), {"a": 2}),
        ("bo'sh: blank qiymati", hookio.read_payload(io.StringIO("  \n")), None),
        ("bo'sh: blank={}", hookio.read_payload(io.StringIO(""), blank={}), {}),
        ("buzuq JSON: None", hookio.read_payload(io.StringIO("{a")), None),
        ("buzuq JSON blank bilan ham None",
         hookio.read_payload(io.StringIO("{a"), blank={}), None),
        ("obyekt emas: None", hookio.read_payload(io.StringIO("[1, 2]")), None),
        ("terminal: o'qilmaydi", hookio.read_payload(Tty('{"a": 1}'), blank={}), None),
        ("o'qish xatosi: bo'sh deb", hookio.read_payload(Broken(""), blank={}), {}),
        ("read_text: BOM siz matn",
         hookio.read_text(windows_stdin(BOM + "\u02bb".encode("utf-8"))), "\u02bb"),
        ("read_text: noto'g'ri bayt yiqitmaydi",
         hookio.read_text(windows_stdin(b"\xff{")), "\ufffd{"),
    ]


def main():
    failures = 0
    rows = cases()
    for name, got, want in rows:
        ok = got == want
        failures += not ok
        print("%-4s %-40s %s" % ("OK" if ok else "XATO", name,
                                 "" if ok else "%r != %r" % (got, want)))
    print("\n%d/%d o'tdi" % (len(rows) - failures, len(rows)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
