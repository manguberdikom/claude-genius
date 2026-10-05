#!/usr/bin/env python3
"""add_code.py uchun sinovlar.

    python3 tools/test_add_code.py

Nega aynan bu asbobga sinov kerak: u korpusga YOZADI. Qolgan asboblar
xato qilsa noto'g'ri javob beradi, bu esa 268 faylning birini buzadi va
natija git tarixiga tushadi. Sinovlar vaqtinchalik faylda ishlaydi,
docs/ ga tegmaydi.
"""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import add_code  # noqa: E402

CHAPTER = """<!-- doc: sinov -->

[Mundarija](README.md)

# 17. Sinov bobi

## 17.1 Birinchi

Birinchi bo'lim matni.

## 17.2 Kodi bor

Matn.

```java
int bor = 1;
```

## 17.3 Oxirgi

Oxirgi bo'lim matni.

---

[&larr; 16. Oldingi](16-x.md) - [Mundarija](README.md) - [18. Keyingi &rarr;](18-x.md)
"""


def write(tmp, text=CHAPTER):
    path = os.path.join(tmp, "17-sinov.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def lines_of(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().split("\n")


def run_main(tmp, data):
    """main() ni soxta omborda yurgizadi: ROOT vaqtincha shu yerga buriladi.

    (chiqish kodi, stderr, bob yo'li) qaytaradi. Haqiqiy docs/ ga tegmaydi.
    """
    root = os.path.join(tmp, "root")
    os.makedirs(os.path.join(root, "docs", "sinov"), exist_ok=True)
    with open(os.path.join(root, "docs", "manifest.json"), "w", encoding="utf-8") as handle:
        json.dump({"sinov": {"chapters": [{"num": 17, "file": "17-sinov.md"}]}}, handle)
    path = write(os.path.join(root, "docs", "sinov"))
    spec = os.path.join(tmp, "snippets.json")
    with open(spec, "w", encoding="utf-8") as handle:
        json.dump(data, handle)
    old, add_code.ROOT = add_code.ROOT, root
    err = io.StringIO()
    try:
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            code = add_code.main([spec])
    finally:
        add_code.ROOT = old
    return code, err.getvalue(), path


def case_oddiy_boshqa(tmp):
    """O'rtadagi bo'limga kod qo'shiladi va keyingi sarlavhadan oldin turadi."""
    path = write(tmp)
    added = add_code.insert(path, {"17.1": "int x = 1;"})
    lines = lines_of(path)
    start = lines.index("## 17.1 Birinchi")
    nxt = lines.index("## 17.2 Kodi bor")
    block = lines[start:nxt]
    return added == {"17.1"} and "```java" in block and "int x = 1;" in block


def case_footerdan_oldin(tmp):
    """Oxirgi bo'limga qo'shilgan kod navigatsiya footeridan OLDIN turadi."""
    path = write(tmp)
    add_code.insert(path, {"17.3": "int y = 2;"})
    body = [l for l in lines_of(path) if l.strip()]
    return "[Mundarija](README.md)" in body[-1] and "int y = 2;" in body


def case_kodi_bori_otkaziladi(tmp):
    """Allaqachon kod bloki bor bo'lim o'tkazib yuboriladi."""
    path = write(tmp)
    added = add_code.insert(path, {"17.2": "int z = 3;"})
    return added == set() and "int z = 3;" not in lines_of(path)


def case_yoq_bolim(tmp):
    """Mavjud bo'lmagan raqam fayl ichini o'zgartirmaydi."""
    path = write(tmp)
    before = lines_of(path)
    added = add_code.insert(path, {"17.9": "int q = 4;"})
    return added == set() and lines_of(path) == before


def case_boshqa_til(tmp):
    """lang berilsa fence shu til bilan ochiladi."""
    path = write(tmp)
    add_code.insert(path, {"17.1": {"lang": "yaml", "code": "spring:\n  main: x"}})
    return "```yaml" in lines_of(path)


def case_fence_ichidagi_sarlavha(tmp):
    """Kod bloki ichidagi `## ` qator bo'lim chegarasi deb sanalmaydi."""
    text = CHAPTER.replace("Birinchi bo'lim matni.",
                           "```md\n## 17.99 soxta sarlavha\n```")
    path = write(tmp, text)
    added = add_code.insert(path, {"17.99": "int w = 5;"})
    return added == set()


def case_footersiz_fayl(tmp):
    """Footeri yo'q faylda ham kod oxirgi bo'lim ichiga tushadi."""
    text = CHAPTER.split("---")[0]
    path = write(tmp, text)
    added = add_code.insert(path, {"17.3": "int v = 6;"})
    return added == {"17.3"} and "int v = 6;" in lines_of(path)


def case_skipped_toplami(tmp):
    """Kodi bor bo'lim skipped ga tushadi, yo'q raqam tushmaydi."""
    path = write(tmp)
    skipped = set()
    added = add_code.insert(path, {"17.2": "int z = 3;", "17.9": "int q = 4;"}, skipped)
    return added == set() and skipped == {"17.2"}


def case_main_ogohlantirishlar(tmp):
    """Kodi bor va mavjud bo'lmagan bo'lim alohida xabar oladi."""
    code, err, path = run_main(tmp, {"sinov": {
        "17.1": "int x = 1;", "17.2": "int z = 3;", "17.9": "int q = 4;"}})
    return (code == 0 and "int x = 1;" in lines_of(path)
            and "kod allaqachon bor -> ['17.2']" in err
            and "bunday bo'lim yo'q -> ['17.9']" in err)


def case_nomalum_hujjat(tmp):
    """Noma'lum hujjat kaliti: 2 bilan chiqadi, to'g'ri kalit ham yozilmaydi."""
    code, err, path = run_main(tmp, {"sinov": {"17.1": "int x = 1;"},
                                     "sinovv": {"1.1": "int y = 2;"}})
    return code == 2 and "sinovv" in err and "int x = 1;" not in lines_of(path)


CASES = [
    ("o'rtadagi bo'limga qo'shadi", case_oddiy_boshqa),
    ("oxirgi bo'lim: footerdan oldin", case_footerdan_oldin),
    ("kodi bor bo'lim o'tkaziladi", case_kodi_bori_otkaziladi),
    ("yo'q bo'lim faylga tegmaydi", case_yoq_bolim),
    ("boshqa til fence'i", case_boshqa_til),
    ("fence ichidagi sarlavha sanalmaydi", case_fence_ichidagi_sarlavha),
    ("footersiz fayl", case_footersiz_fayl),
    ("kodi bor bo'lim skipped ga tushadi", case_skipped_toplami),
    ("main: ikki ogohlantirish alohida", case_main_ogohlantirishlar),
    ("noma'lum hujjat: 2, hech narsa yozilmaydi", case_nomalum_hujjat),
]


def main():
    tmp = tempfile.mkdtemp(prefix="add_code_")
    failures = 0
    try:
        for name, fn in CASES:
            try:
                ok = bool(fn(tmp))
            except Exception as exc:  # sinov xatosi ham yiqilish
                ok = False
                name = "%s (%s)" % (name, exc)
            failures += not ok
            print("%-4s %s" % ("OK" if ok else "XATO", name))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
