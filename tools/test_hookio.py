#!/usr/bin/env python3
"""hookio.py uchun sinovlar.

    python3 tools/test_hookio.py

Windows holati oqim bilan taqlid qilinadi: cp1252 li TextIOWrapper
(matnli sys.stdin aynan shunday) va PowerShell 5.1 qo'yadigan BOM.
"""

import contextlib
import io
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hookio  # noqa: E402

ROOT = os.path.dirname(HERE)
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


@contextlib.contextmanager
def folder(*files):
    """Vaqtinchalik papka; har `files` yo'li bo'sh fayl bo'lib yaratiladi.

    `(yo'l, matn)` juftligi berilsa fayl o'sha matn bilan yoziladi.
    """
    tmp = tempfile.mkdtemp(prefix="hookio_")
    try:
        for item in files:
            rel, text = item if isinstance(item, tuple) else (item, "")
            path = os.path.join(tmp, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with io.open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@contextlib.contextmanager
def env(**values):
    """Muhit o'zgaruvchilari; None bo'lsa o'chiriladi, oxirida tiklanadi."""
    saved = {key: os.environ.get(key) for key in values}
    try:
        for key, value in values.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        yield
    finally:
        for key, value in saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def gating_cases():
    """active(): hook qaysi proyektda ishlaydi.

    Har holat CLAUDE_PROJECT_DIR ni ataylab qo'yadi, chunki sinov
    jarayonining o'zida u klonga ishora qilib turishi mumkin.
    """
    rows = []

    def check(name, want, root, payload=None, hooks=None):
        with env(CLAUDE_PROJECT_DIR=root, GENIUS_HOOKS=hooks):
            rows.append((name, hookio.active(payload), want))

    with folder("pom.xml") as maven:
        check("Maven ildizi: faol", True, maven)
        check("GENIUS_HOOKS=off: nofaol", False, maven, hooks="off")
        check("GENIUS_HOOKS=OFF (katta harf): nofaol", False, maven, hooks="OFF")
        check("GENIUS_HOOKS=on: faolga ta'sir qilmaydi", True, maven, hooks="on")
    with folder("backend/pom.xml") as multi:
        check("kichik papkadagi pom.xml: faol", True, multi)
    with folder("app/build.gradle.kts") as gradle:
        check("kichik papkadagi build.gradle.kts: faol", True, gradle)
    with folder("settings.gradle") as settings:
        check("settings.gradle ildizda: faol", True, settings)
    with folder("src/main/java/A.java", "package.json") as js:
        check("Java emas (JS): nofaol", False, js)
        # Ikkinchi daraja sanalmaydi: aks holda har monorepo faol bo'lardi.
    with folder("a/b/pom.xml") as deep:
        check("ikkinchi darajadagi pom.xml: nofaol", False, deep)
        # Chuqur monorepo uchun qo'lda yoqish: skan o'rniga shu.
        check("GENIUS_HOOKS=on: chuqur modul faol", True, deep, hooks="on")
        check("GENIUS_HOOKS=true ham yoqadi", True, deep, hooks="true")
    with folder("main.py") as plain:
        check("GENIUS_HOOKS=on: Java emas ham faol", True, plain, hooks="on")
    check("GENIUS_HOOKS=on: ildiz yo'q ham faol", True, "", hooks="on")

    # Mobil va Android: android/build.gradle Java proyekti belgisi emas.
    with folder("package.json", "android/build.gradle",
                "android/app/build.gradle") as rn:
        check("React Native: nofaol", False, rn)
        check("React Native, GENIUS_HOOKS=on: faol", True, rn, hooks="on")
    with folder("pubspec.yaml", "android/build.gradle.kts") as flutter:
        check("Flutter: nofaol", False, flutter)
    with folder("app.json", "android/settings.gradle") as expo:
        check("Expo (app.json): nofaol", False, expo)
    with folder("package.json", "backend/pom.xml", "frontend/index.js") as mono:
        check("backend/pom.xml + ildizda package.json: faol", True, mono)
    with folder("package.json", "pom.xml") as rootjs:
        check("ildizda pom.xml + package.json: faol", True, rootjs)
    with folder("build.gradle", "settings.gradle",
                "app/build.gradle", "app/src/main/AndroidManifest.xml") as android:
        check("Android (AndroidManifest.xml): nofaol", False, android)
    with folder("build.gradle.kts", "settings.gradle.kts", "app/build.gradle.kts",
                ("gradle/libs.versions.toml",
                 '[plugins]\nandroid-application = { id = "com.android.application",'
                 ' version.ref = "agp" }\n')) as catalog:
        check("Android (version catalog): nofaol", False, catalog)
    with folder("build.gradle.kts",
                ("gradle/libs.versions.toml",
                 '[plugins]\nspring-boot = { id = "org.springframework.boot",'
                 ' version = "3.3.4" }\n')) as spring_catalog:
        check("Spring (version catalog): faol", True, spring_catalog)

    check("klonning o'zi: faol", True, ROOT)
    check("ildiz yo'q (bo'sh): nofaol", False, "")
    check("ildiz mavjud emas: nofaol", False,
          os.path.join(HERE, "yoq-papka-12345"))

    # Ildiz env da yo'q: payload dagi cwd ishlatiladi.
    with folder("pom.xml") as maven, folder("main.py") as plain:
        with env(CLAUDE_PROJECT_DIR=None, GENIUS_HOOKS=None):
            rows.append(("env yo'q, payload cwd: faol",
                         hookio.active({"cwd": maven}), True))
            rows.append(("env yo'q, payload cwd Java emas: nofaol",
                         hookio.active({"cwd": plain}), False))
            rows.append(("env ham, payload ham yo'q: nofaol",
                         hookio.active(None), False))
            rows.append(("payload cwd satr emas: nofaol",
                         hookio.active({"cwd": 5}), False))
    return rows


def main():
    failures = 0
    rows = cases() + gating_cases()
    for name, got, want in rows:
        ok = got == want
        failures += not ok
        print("%-4s %-44s %s" % ("OK" if ok else "XATO", name,
                                 "" if ok else "%r != %r" % (got, want)))
    print("\n%d/%d o'tdi" % (len(rows) - failures, len(rows)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
