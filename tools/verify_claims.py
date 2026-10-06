#!/usr/bin/env python3
"""Korpusdagi texnik da'volarni mashina bilan tekshiradi (oflayn).

    python3 tools/verify_claims.py               # kalit, api, bom, yaml, xml
    python3 tools/verify_claims.py --java        # + ```java bloklar javac parserida
    python3 tools/verify_claims.py --diff        # faqat HEAD dan beri o'zgargan boblar
    python3 tools/verify_claims.py --diff origin/main --java
    python3 tools/verify_claims.py --faqat kalit,api docs/testing/08-*.md
    python3 tools/verify_claims.py --izohli      # izoh bilan o'tkazilganlar ham
    python3 tools/verify_claims.py --yangila     # claims_data ni Maven Central dan

Tekshiruvlar (ma'lumot `tools/claims_data/` da, tarmoq kerak emas):

  kalit  ```properties va ```yaml bloklaridagi Spring kalitlari
         boot_deprecated.tsv bilan solishtiriladi: Boot 3.5 yoki 4.1
         metadata sida deprecated yoki 4.1 da yo'q kalit.
  api    removed_api.tsv dagi nom (Hibernate 6.6 -> 7, Testcontainers
         1.21 -> 2, Boot 3.5 -> 4 da olib tashlangan yoki ko'chgan
         annotatsiya, klass, artifactId) matnda yoki kodda.
  bom    pom va gradle bloklaridagi versiyasiz groupId:artifactId Boot
         boshqaradigan guruhdan, lekin Boot 4.1 BOM da yo'q
         (boot_managed.tsv).
  yaml   '//' bilan boshlangan qator (YAML da izoh emas, kalit bo'ladi);
         PyYAML o'rnatilgan bo'lsa blok parse ham qilinadi.
  xml    ```xml blok xml.etree da parse bo'lmaydi (izohdan keyin
         `<?xml ...?>` kabi).
  java   (faqat --java) ```java blok javac parserida uch o'ramda
         (compilation unit, class body, method body) ham o'tmaydi; butun
         blok o'tmasa bo'sh qator bo'yicha bo'laklarga bo'linib har bo'lak
         alohida sinaladi. `...` o'rinbosarli blok (varargs emas) va
         java_allow.tsv dagi (fayl + blok sha1) o'tkaziladi. javac yo'q
         bo'lsa tekshiruv o'tkazib yuboriladi va shu aytiladi.

Versiya izohi qoidasi (KR-T-K1): topilma yonida, ya'ni shu qator yoki kod
blokidagi shu paragrafdan 3 satr ichida yopiq versiya belgisi bo'lsa
("Boot 4 da", "Boot 3.4-3.5", "Hibernate 6.6 da", "4.0 gacha")
ogohlantirish chiqmaydi. Ochiq belgi ("Boot 3.4+", "3.2 dan") yetmaydi:
u keyingi major versiyani ham qamraydi. api uchun "olib tashlangan",
"deprecated", "eski", "ilgari", "undan oldin" va almashtiruvchi nomning
o'zi (masalan `@MockBean`/`@MockitoBean`) ham izoh hisoblanadi.

Chiqish kodi: topilma bo'lsa 1 (CI uchun). check_docs collect() ni
chaqiradi va natijani OGOHLANTIRISH qiladi; java qismi u yerda yurmaydi.
Faqat standart kutubxona, PyYAML ixtiyoriy.
"""

import argparse
import bisect
import collections
import errno
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(HERE, "claims_data")
KINDS = ("kalit", "api", "bom", "yaml", "xml", "java")
DEFAULT_KINDS = ("kalit", "api", "bom", "yaml", "xml")
WINDOW = 3

Finding = collections.namedtuple("Finding", "path line tur xabar")


def fmt(f):
    return "%s:%d: [%s] %s" % (f.path, f.line, f.tur, f.xabar)


# --- ma'lumot fayllari -------------------------------------------------

def read_tsv(name, data_dir=None):
    """Izoh (#) va bo'sh qatorsiz satrlar; birinchi satr sarlavha."""
    path = os.path.join(data_dir or DATA, name)
    rows, header = [], None
    if not os.path.exists(path):
        return rows
    with io.open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\t")
            if header is None:
                header = parts
                continue
            rows.append(dict(zip(header, parts + [""] * (len(header) - len(parts)))))
    return rows


def norm_key(key):
    """Relaxed binding: `connectTimeout`, `connect-timeout`, `[0]` bir xil."""
    key = re.sub(r"\[[^\]]*\]", "", key)
    return key.lower().replace("-", "").replace("_", "")


class Data(object):
    """claims_data dagi to'rt fayl, bir marta o'qiladi."""

    def __init__(self, data_dir=None):
        self.deprecated, self.dep_maps = {}, []
        for row in read_tsv("boot_deprecated.tsv", data_dir):
            self.deprecated[norm_key(row["kalit"])] = row
            if row.get("tur") == "map":
                self.dep_maps.append((norm_key(row["kalit"]) + ".", row))
        self.managed = {"4.1": {}, "3.5": {}}
        for row in read_tsv("boot_managed.tsv", data_dir):
            self.managed.setdefault(row["boot"], {}).setdefault(
                row["groupId"], set()).update(row["artifactId"].split())
        # Har naqshning literal o'zagi str.find bilan qidiriladi, regex faqat
        # topilgan joyda chegarani tekshiradi: qator x naqsh regex 6 MB da sekin.
        self.api = []
        for row in read_tsv("removed_api.tsv", data_dir):
            pattern = api_pattern(row)
            if pattern is not None:
                self.api.append((api_literal(row), re.compile(pattern), row))
        self.java_allow = {(r["fayl"], r["sha1"]) for r in
                           read_tsv("java_allow.tsv", data_dir)}


def api_literal(row):
    kind, name = row["tur"], row["naqsh"]
    if kind == "annotatsiya":
        return "@" + name
    if kind == "artifact":
        return name.partition(":")[0] + ":"
    return name


def find_all(text, literal, rx):
    """literal uchragan har joyda rx.match: [(pos, match)]."""
    out, pos = [], text.find(literal)
    while pos >= 0:
        m = rx.match(text, pos)
        if m:
            out.append(m)
        pos = text.find(literal, pos + 1)
    return out


def api_pattern(row):
    kind, name = row["tur"], row["naqsh"]
    if kind == "annotatsiya":
        return r"@" + re.escape(name) + r"\b"
    if kind == "klass":
        return r"(?<!\w)" + re.escape(name) + r"\b"
    if kind == "fqn":
        return r"\b" + re.escape(name) + r"\b"
    if kind == "artifact":
        group, _, arts = name.partition(":")
        return (r"(?<![\w.-])" + re.escape(group) + r":(" + arts
                + r")(?![\w.-])")
    return None


class Sink(object):
    """Topilmalar va (so'ralsa) versiya izohi bilan o'tkazilganlari."""

    def __init__(self):
        self.found, self.excused = [], []

    def add(self, finding, excused=False):
        (self.excused if excused else self.found).append(finding)


# --- korpus ------------------------------------------------------------

TOC_RE = re.compile(r"^\s*[-*] \[[^\]]*\]\([^)]*\)( - [\d.]+)?\s*$")


class Block(object):
    __slots__ = ("lang", "open", "close", "first", "last")

    def __init__(self, lang, open_line, close_line):
        self.lang, self.open, self.close = lang, open_line, close_line
        self.first, self.last = open_line + 1, close_line - 1


class Doc(object):
    """Bitta markdown fayl: satrlar (1 dan) va kod bloklari."""

    def __init__(self, rel, text):
        self.rel = rel.replace(os.sep, "/")
        self.text = text
        self.lines = [""] + text.split("\n")
        self.starts = [m.end() for m in re.finditer("\n", text)]
        self.blocks, self.in_block = [], {}
        start, lang = None, ""
        for n in range(1, len(self.lines)):
            l = self.lines[n]
            if not l.startswith("```"):
                continue
            if start is None:
                start = n
                info = l[3:].strip().split()
                lang = info[0].lower() if info else ""
            else:
                block = Block(lang, start, n)
                self.blocks.append(block)
                for k in range(block.first, n):
                    self.in_block[k] = block
                start = None

    def body(self, block):
        return self.lines[block.first:block.close]

    def line_of(self, pos):
        return bisect.bisect_right(self.starts, pos) + 1

    def is_title(self, line):
        """Sarlavha yoki mundarija qatori: da'vo emas, faqat nom."""
        if line in self.in_block:
            return False
        l = self.lines[line]
        return l.startswith("#") or bool(TOC_RE.match(l))

    def window(self, line):
        """Topilma konteksti: qator +-3, kod blokida esa paragraf +-3.

        Paragraf blok chegarasiga tegsa oyna fence dan tashqariga chiqadi:
        blok oldidagi "Spring Boot 3.5 (Testcontainers 1.21):" kabi
        sarlavha shu blokdagi har qatorga tegishli.
        """
        block = self.in_block.get(line)
        lo = hi = line
        if block is not None:
            while lo > block.first and self.lines[lo - 1].strip():
                lo -= 1
            while hi < block.last and self.lines[hi + 1].strip():
                hi += 1
            if lo == block.first:
                lo = block.open
            if hi == block.last:
                hi = block.close
        lo, hi = max(1, lo - WINDOW), min(len(self.lines) - 1, hi + WINDOW)
        return "\n".join(self.lines[lo:hi + 1])


def doc_files(root, files=None):
    if files:
        return sorted({os.path.relpath(os.path.abspath(f), root)
                       if os.path.isabs(f) else f for f in files})
    found = glob.glob(os.path.join(root, "docs", "*", "*.md"))
    return sorted(os.path.relpath(p, root) for p in found)


def load_docs(root, files):
    docs = []
    for rel in files:
        path = os.path.join(root, rel)
        if os.path.exists(path):
            with io.open(path, encoding="utf-8") as handle:
                docs.append(Doc(rel, handle.read()))
    return docs


# --- versiya izohi -----------------------------------------------------

# Mahsulot va versiya. Keyingi major (Boot 4, Hibernate 7, TC 2, Spring
# Framework 7) qanday shaklda bo'lsa ham izoh. Undan kichik versiya faqat
# yopiq bo'lsa: "3.4+", "3.2 dan", "3.x+" ochiq. Izoh topilma mahsulotiga
# tegishli bo'lishi kerak: "JUnit 5" @MockBean ni oqlamaydi.
VERSION_RE = re.compile(
    r"\b(Spring Boot|Boot|Hibernate|Testcontainers|TC|Spring Framework|"
    r"Framework|Spring)\s*(\d+)((?:\.(?:\d+|x))*)(\s*\+|\s+dan\b|\s+va yuqori)?")
PRODUCT = {"spring boot": "boot", "boot": "boot", "hibernate": "hibernate",
           "testcontainers": "tc", "tc": "tc", "spring framework": "spring",
           "framework": "spring", "spring": "spring"}
NEXT_MAJOR = {"boot": 4, "hibernate": 7, "tc": 2, "spring": 7}
# Mahsulot nomisiz "4.0 gacha", "3.3 gacha".
UNTIL_RE = re.compile(r"\b\d+\.\d+(?:\.x)?\s+gacha\b")
# "o'rniga" kabi umumiy so'z emas: "X o'rniga slice test" versiya izohi emas.
API_NOTE_RE = re.compile(r"olib tashlangan|deprecat|\beski\b|ilgari|undan oldin|"
                         r"removed", re.I)


def version_note(text, products=("boot", "tc")):
    for m in VERSION_RE.finditer(text):
        product = PRODUCT[m.group(1).lower()]
        if product not in products:
            continue
        if int(m.group(2)) >= NEXT_MAJOR[product] or not m.group(4):
            return True
    return bool(UNTIL_RE.search(text))


def row_products(row):
    """removed_api qatori qaysi mahsulotga tegishli: `nima` ning boshidan."""
    head = row.get("nima", "").split(" ")[0].lower()
    return (PRODUCT.get(head, "boot"),)


# --- 1. kalit ----------------------------------------------------------

PROP_LINE_RE = re.compile(r"^\s*([A-Za-z][\w.\-\[\]]*)\s*[=:]")
YAML_KEY_RE = re.compile(r"""^(["']?)([^\s"'#{\[][^:#]*?)\1\s*:(?:\s|$)(.*)$""")
BLOCK_SCALAR_RE = re.compile(r"^[|>][-+0-9]*\s*(#.*)?$")


def yaml_keys(lines, first):
    """Oddiy YAML ni yassilaydi: [(yo'l, satr)], '//' qatorlari alohida.

    PyYAML siz ishlaydi: chekinish steki, ro'yxat elementi (`- k: v`)
    ichkariroq hisoblanadi, blok skalyar (`|`, `>`) tanasi o'tkaziladi.
    Har oraliq yo'l ham qaytadi: map turidagi kalit (`a.b.tags`) uchun.
    """
    keys, slashes, stack, scalar = [], [], [], None
    for i, raw in enumerate(lines):
        n = first + i
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        if scalar is not None:
            if indent > scalar:
                continue
            scalar = None
        body = raw.strip()
        if body.startswith("#"):
            continue
        if body.startswith("//"):
            slashes.append(n)
            continue
        if body in ("---", "..."):
            stack = []
            continue
        while body.startswith("- "):
            body = body[2:].lstrip()
            indent = len(raw) - len(body)
        m = YAML_KEY_RE.match(body)
        if not m:
            continue
        key, rest = m.group(2).strip(), m.group(3).strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        path = ".".join([k for _, k in stack] + [key])
        keys.append((path, n))
        if BLOCK_SCALAR_RE.match(rest):
            scalar = indent
        elif not rest or rest.startswith("#") or rest.startswith("&"):
            stack.append((indent, key))
    return keys, slashes


def property_keys(doc, block):
    lines = doc.body(block)
    if block.lang == "properties":
        out = []
        for i, l in enumerate(lines):
            if l.lstrip().startswith(("#", "!")):
                continue
            m = PROP_LINE_RE.match(l)
            if m:
                out.append((m.group(1), block.first + i))
        return out
    return yaml_keys(lines, block.first)[0]


def describe_dep(row):
    level = row.get("daraja") or "warning"
    since = (", %s dan" % row["since"]) if row.get("since") else ""
    if level == "removed":
        what = "Boot 4.1 metadata sida yo'q"
        if row.get("boot") == "3.5":
            what += " (3.5 da deprecated%s)" % since
    elif row.get("boot") == "3.5":
        what = "Boot 3.5 da ham deprecated (%s%s)" % (level, since)
    else:
        what = "Boot 4.1 da deprecated (%s%s)" % (level, since)
    if row.get("almashtirish"):
        what += ", o'rniga %s" % row["almashtirish"]
    return what


def check_keys(doc, data, sink):
    seen = set()
    for block in doc.blocks:
        if block.lang not in ("properties", "yaml", "yml"):
            continue
        for key, line in property_keys(doc, block):
            nk = norm_key(key)
            row = data.deprecated.get(nk)
            if row is None:
                row = next((r for p, r in data.dep_maps if nk.startswith(p)), None)
            if row is None or (line, nk) in seen:
                continue
            seen.add((line, nk))
            ctx = doc.window(line)
            excused = version_note(ctx) or bool(re.search(r"deprecat", ctx, re.I))
            sink.add(Finding(doc.rel, line, "kalit", "%s: %s; yonida 'Boot 4 da' "
                             "yoki yopiq versiya izohi yo'q" % (key, describe_dep(row))),
                     excused)


# --- 2-3. api va bom ---------------------------------------------------

DEP_RE = re.compile(r"<dependency>(.*?)</dependency>", re.S)
GRADLE_RE = re.compile(r"""["']([\w.\-]+\.[\w\-]+):([\w.\-]+)(?::([^"'\s]+))?["']""")
GRADLE_LANGS = ("groovy", "gradle", "kotlin", "kts")


def tag(chunk, name):
    m = re.search(r"<%s>\s*([^<]+?)\s*</%s>" % (name, name), chunk)
    return m.group(1) if m else None


def coordinates(doc):
    """Kod bloklaridagi bog'liqliklar: [(group, artifact, versiyali, satr)]."""
    out = []
    for block in doc.blocks:
        if block.lang == "xml":
            text = "\n".join(doc.body(block))
            for m in DEP_RE.finditer(text):
                chunk = m.group(1)
                group, art = tag(chunk, "groupId"), tag(chunk, "artifactId")
                if not group or not art:
                    continue
                off = m.start(1) + chunk.find("<artifactId>")
                line = block.first + text.count("\n", 0, off)
                out.append((group, art, tag(chunk, "version") is not None, line))
        elif block.lang in GRADLE_LANGS:
            for i, l in enumerate(doc.body(block)):
                for m in GRADLE_RE.finditer(l):
                    out.append((m.group(1), m.group(2), bool(m.group(3)),
                                block.first + i))
    return out


def api_excused(doc, line, row):
    ctx = doc.window(line)
    if version_note(ctx, row_products(row)) or API_NOTE_RE.search(ctx):
        return True
    repl = row.get("almashtirish", "")
    if row["tur"] == "artifact":
        return "testcontainers-" in doc.lines[line]
    return bool(repl) and any(r.strip() and r.strip() in ctx
                              for r in repl.split(","))


def check_api(doc, data, sink, flagged):
    hits = {}
    for literal, rx, row in data.api:
        if row["tur"] == "artifact":
            continue
        for m in find_all(doc.text, literal, rx):
            line = doc.line_of(m.start())
            if doc.is_title(line) or (line, literal) in hits:
                continue
            hits[(line, literal)] = True
            sink.add(Finding(doc.rel, line, "api", "%s: %s%s" % (
                m.group(0), row["nima"],
                ("; o'rniga " + row["almashtirish"]) if row["almashtirish"] else "")),
                api_excused(doc, line, row))
    # artifactId: kod blokidagi koordinata va matndagi `g:a`.
    arts = [(literal, rx, row) for literal, rx, row in data.api
            if row["tur"] == "artifact"]
    found = {}
    for group, art, _, line in coordinates(doc):
        for _, rx, row in arts:
            if rx.fullmatch("%s:%s" % (group, art)):
                found.setdefault((line, art), row)
    for literal, rx, row in arts:
        for m in find_all(doc.text, literal, rx):
            found.setdefault((doc.line_of(m.start()), m.group(1)), row)
    for (line, art), row in sorted(found.items()):
        flagged.add((line, art))
        sink.add(Finding(doc.rel, line, "api", "%s:%s: %s" % (
            row["naqsh"].split(":")[0], art, row["nima"])),
            api_excused(doc, line, row))


def check_bom(doc, data, sink, flagged):
    new, old = data.managed.get("4.1", {}), data.managed.get("3.5", {})
    for group, art, versioned, line in coordinates(doc):
        if versioned or group not in new or art in new[group]:
            continue
        if (line, art) in flagged:
            continue
        legacy = art in old.get(group, ())
        where = " (Boot 3.5 BOM da bor)" if legacy else ""
        sink.add(Finding(doc.rel, line, "bom", "%s:%s versiyasiz, Boot 4.1 BOM "
                         "uni boshqarmaydi%s" % (group, art, where)),
                 legacy and version_note(doc.window(line)))


# --- 5. yaml va xml ----------------------------------------------------

def yaml_loader():
    try:
        import yaml
    except ImportError:
        return None

    class Loader(yaml.SafeLoader):
        pass

    # `!Ref`, `!!binary` kabi teglar: tuzilma tekshiriladi, qiymat emas.
    Loader.add_multi_constructor("", lambda loader, suffix, node: None)
    return yaml, Loader


def check_yaml(doc, sink, loader):
    for block in doc.blocks:
        if block.lang not in ("yaml", "yml"):
            continue
        lines = doc.body(block)
        for line in yaml_keys(lines, block.first)[1]:
            sink.add(Finding(doc.rel, line, "yaml", "'//' YAML da izoh emas, "
                             "kalit yoki qiymat bo'lib qoladi; '#' yozing"))
        text = "\n".join(lines)
        if loader is None or "..." in text or "{{" in text:
            continue
        yaml, Loader = loader
        try:
            for _ in yaml.load_all(text, Loader=Loader):
                pass
        except yaml.YAMLError as exc:
            mark = getattr(exc, "problem_mark", None)
            line = block.first + (mark.line if mark else 0)
            problem = getattr(exc, "problem", None) or str(exc).split("\n")[0]
            sink.add(Finding(doc.rel, line, "yaml", "parse bo'lmaydi: %s" % problem))


def check_xml(doc, sink):
    import xml.etree.ElementTree as ET
    for block in doc.blocks:
        if block.lang != "xml":
            continue
        raw = "\n".join(doc.body(block))
        text = raw.lstrip()
        skipped = raw[:len(raw) - len(text)].count("\n")
        text = text.rstrip()
        if not text.startswith("<") or "..." in text or "\u2026" in text:
            continue
        error = xml_error(ET, text)
        if error is None:
            continue
        msg, line = error
        sink.add(Finding(doc.rel, block.first + skipped + max(line - 1, 0), "xml",
                         "parse bo'lmaydi: %s" % msg))


def xml_error(ET, text):
    """(xabar, blok ichidagi satr) yoki None. Fragment ildiz bilan o'raladi."""
    try:
        ET.fromstring(text)
        return None
    except ET.ParseError as exc:
        first = exc
    msg = str(first)
    if "undefined entity" in msg:
        return None     # &xxe; va HTML entity: tuzilma to'g'ri
    if "junk after document element" in msg and not text.startswith("<?xml"):
        try:
            ET.fromstring("<r_>" + text + "</r_>")
            return None
        except ET.ParseError as exc:
            if "undefined entity" in str(exc):
                return None
            return str(exc).split(":")[0], exc.position[0]
    return msg.split(":")[0], first.position[0]


# --- 4. java -----------------------------------------------------------

JAVA_PARSER = r"""
import com.sun.source.util.JavacTask;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;
import java.util.stream.IntStream;
import javax.tools.*;

// Har blok: avval butunligicha uch o'ramda, o'tmasa bo'sh qator (qavs
// chuqurligi 0) bo'yicha bo'laklarga bo'lib har bo'lak uch o'ramda.
// Chiqish: "yo'l\tOK" yoki "yo'l\tsatr\txabar".
public class ClaimsParse {
    static final String[][] WRAP = {{"", ""}, {"class W_ {\n", "\n}"},
        {"class W_ { void m_() throws Throwable {\n", "\n}}"}};
    static final JavaCompiler JAVAC = ToolProvider.getSystemJavaCompiler();
    static final List<String> OPTS = List.of("--enable-preview", "--release",
        String.valueOf(Runtime.version().feature()), "-proc:none");

    // null: o'tdi; aks holda {satr, xabar} (satr 1 dan, kod ichida).
    static Object[] parse(String src) {
        Object[] best = null;
        for (int i = 0; i < WRAP.length; i++) {
            final String code = WRAP[i][0] + src + WRAP[i][1];
            DiagnosticCollector<JavaFileObject> diags = new DiagnosticCollector<>();
            JavaFileObject file = new SimpleJavaFileObject(
                    URI.create("string:///W_.java"), JavaFileObject.Kind.SOURCE) {
                public CharSequence getCharContent(boolean ignore) { return code; }
            };
            try {
                ((JavacTask) JAVAC.getTask(null, null, diags, OPTS, null, List.of(file))).parse();
            } catch (java.io.IOException | RuntimeException e) {
                return new Object[] {1L, "parser: " + e};
            }
            Diagnostic<? extends JavaFileObject> err = null;
            for (Diagnostic<? extends JavaFileObject> d : diags.getDiagnostics()) {
                if (d.getKind() == Diagnostic.Kind.ERROR) { err = d; break; }
            }
            if (err == null) return null;
            long line = err.getLineNumber() - (i == 0 ? 0 : 1);
            if (best == null || line > (Long) best[0]) {
                best = new Object[] {line, err.getMessage(Locale.ROOT).split("\n")[0]};
            }
        }
        return best;
    }

    static int depthDelta(String line) {
        int d = 0;
        boolean str = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (!str && c == '/' && i + 1 < line.length() && line.charAt(i + 1) == '/') break;
            if (c == '"' && (i == 0 || line.charAt(i - 1) != '\\')) str = !str;
            if (str) continue;
            if (c == '{') d++;
            if (c == '}') d--;
        }
        return d;
    }

    static String check(String src) {
        Object[] whole = parse(src);
        if (whole == null) return "OK";
        String[] lines = src.split("\n", -1);
        int depth = 0, start = 0;
        List<int[]> segs = new ArrayList<>();
        for (int i = 0; i < lines.length; i++) {
            if (lines[i].trim().isEmpty() && depth == 0) {
                if (i > start) segs.add(new int[] {start, i});
                start = i + 1;
            } else {
                depth += depthDelta(lines[i]);
            }
        }
        if (start < lines.length) segs.add(new int[] {start, lines.length});
        if (segs.size() < 2) return whole[0] + "\t" + whole[1];
        for (int[] s : segs) {
            String part = String.join("\n", Arrays.asList(lines).subList(s[0], s[1]));
            Object[] err = parse(part);
            if (err != null) return (s[0] + (Long) err[0]) + "\t" + err[1];
        }
        return "OK";
    }

    public static void main(String[] args) throws Exception {
        List<String> paths = Files.readAllLines(Paths.get(args[0]), StandardCharsets.UTF_8);
        String[] out = new String[paths.size()];
        IntStream.range(0, paths.size()).parallel().forEach(k -> {
            try {
                String src = new String(Files.readAllBytes(Paths.get(paths.get(k))),
                                        StandardCharsets.UTF_8);
                out[k] = paths.get(k) + "\t" + check(src);
            } catch (java.io.IOException | RuntimeException e) {
                out[k] = paths.get(k) + "\t1\tparser: " + e;
            }
        });
        for (String line : out) System.out.println(line);
    }
}
"""


# `...` o'rinbosar: varargs (`String... args`) emas.
PLACEHOLDER_RE = re.compile(r"(?<![\w>\]])\.\.\.|\u2026")


def block_sha1(lines):
    return hashlib.sha1("\n".join(lines).encode("utf-8")).hexdigest()


def java_tools():
    javac = shutil.which("javac")
    if not javac:
        return None
    java = os.path.join(os.path.dirname(os.path.realpath(javac)),
                        "java.exe" if os.name == "nt" else "java")
    return java if os.path.exists(java) else shutil.which("java")


def check_java(docs, data, sink, notes):
    java = java_tools()
    if java is None:
        notes.append("java: javac topilmadi, ```java bloklar tekshirilmadi")
        return
    tmp = tempfile.mkdtemp(prefix="verify_claims_")
    try:
        where, paths, skipped = {}, [], collections.Counter()
        for doc in docs:
            for block in doc.blocks:
                if block.lang != "java":
                    continue
                lines = doc.body(block)
                text = "\n".join(lines)
                if PLACEHOLDER_RE.search(text):
                    skipped["..."] += 1
                    continue
                if (doc.rel, block_sha1(lines)) in data.java_allow:
                    skipped["allowlist"] += 1
                    continue
                path = os.path.join(tmp, "b%05d.java" % len(paths))
                with io.open(path, "w", encoding="utf-8") as handle:
                    handle.write(text)
                where[path] = (doc, block)
                paths.append(path)
        summary = "%d tasi `...` li, %d tasi allowlistda" % (
            skipped["..."], skipped["allowlist"])
        if not paths:
            notes.append("java: tekshiriladigan blok yo'q (%s)" % summary)
            return
        src = os.path.join(tmp, "ClaimsParse.java")
        with io.open(src, "w", encoding="utf-8") as handle:
            handle.write(JAVA_PARSER)
        listing = os.path.join(tmp, "list.txt")
        with io.open(listing, "w", encoding="utf-8") as handle:
            handle.write("\n".join(paths) + "\n")
        proc = subprocess.run([java, src, listing], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=600)
        if proc.returncode != 0:
            lines = [l for l in proc.stderr.decode("utf-8", "replace").splitlines()
                     if l.strip() and not l.startswith("Picked up")]
            notes.append("java: parser yiqildi: %s" % " | ".join(lines[:3]))
            return
        for row in proc.stdout.decode("utf-8", "replace").splitlines():
            parts = row.split("\t", 2)
            if len(parts) < 3 or parts[0] not in where:
                continue
            doc, block = where[parts[0]]
            line = block.first + max(int(parts[1]) - 1, 0)
            sink.add(Finding(doc.rel, line, "java", "javac parse: %s (blok sha1 %s)"
                             % (parts[2], block_sha1(doc.body(block)))))
        notes.append("java: %d blok parse qilindi, %s" % (len(paths), summary))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- yig'uvchi ---------------------------------------------------------

def collect(root=None, files=None, kinds=DEFAULT_KINDS, notes=None, data_dir=None,
            excused=None):
    """Topilmalar ro'yxati. check_docs shu funksiyani chaqiradi.

    `excused` ro'yxat bo'lsa versiya izohi tufayli o'tkazilganlar shunga
    yoziladi (CLI --izohli, sinov va qo'lda ko'rib chiqish uchun).
    """
    root = root or ROOT
    notes = notes if notes is not None else []
    data = Data(data_dir)
    docs = load_docs(root, doc_files(root, files))
    sink = Sink()
    loader = yaml_loader() if "yaml" in kinds else None
    if "yaml" in kinds and loader is None:
        notes.append("yaml: PyYAML yo'q, faqat '//' tekshirildi")
    for doc in docs:
        flagged = set()
        if "kalit" in kinds:
            check_keys(doc, data, sink)
        if "api" in kinds:
            check_api(doc, data, sink, flagged)
        if "bom" in kinds:
            check_bom(doc, data, sink, flagged)
        if "yaml" in kinds:
            check_yaml(doc, sink, loader)
        if "xml" in kinds:
            check_xml(doc, sink)
    if "java" in kinds:
        check_java(docs, data, sink, notes)

    def order(items):
        return sorted(set(items), key=lambda f: (f.path, f.line, f.tur, f.xabar))

    if excused is not None:
        excused.extend(order(sink.excused))
    return order(sink.found)


def changed_files(root, ref):
    """ref dan beri o'zgargan va kuzatilmagan docs/ boblari."""
    names = set()
    for cmd in (["git", "-C", root, "diff", "--name-only", ref, "--", "docs"],
                ["git", "-C", root, "ls-files", "--others", "--exclude-standard",
                 "--", "docs"]):
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise SystemExit("git: %s" % proc.stderr.decode("utf-8", "replace").strip())
        names.update(proc.stdout.decode("utf-8").split())
    return sorted(n for n in names if re.match(r"docs/[^/]+/[^/]+\.md$", n))


# --- --yangila: claims_data ni qayta yasash -----------------------------

BOOT_OLD, BOOT_NEW = "3.5.16", "4.1.0"
MIRRORS = ("https://repo1.maven.org/maven2",
           "https://maven-central.storage-download.googleapis.com/maven2")
# Metadata yoki BOM bermaydigan modullar.
NO_METADATA = ("spring-boot-dependencies", "spring-boot-maven-plugin",
               "spring-boot-loader", "spring-boot-loader-classic",
               "spring-boot-loader-tools", "spring-boot-buildpack-platform",
               "spring-boot-jarmode-tools", "spring-boot-autoconfigure-processor",
               "spring-boot-configuration-processor",
               "spring-boot-configuration-metadata",
               "spring-boot-properties-migrator",
               "spring-boot-autoconfigure-classic-modules",
               "spring-boot-test-classic-modules")


def fetch(group, art, version, ext):
    """Avval ~/.m2, keyin Maven Central oynalari. (baytlar, manba)."""
    rel = "%s/%s/%s/%s-%s.%s" % (group.replace(".", "/"), art, version, art,
                                 version, ext)
    local = os.path.join(os.path.expanduser("~"), ".m2", "repository", rel)
    if os.path.exists(local):
        with open(local, "rb") as handle:
            return handle.read(), "~/.m2"
    import urllib.request
    last = None
    for base in MIRRORS:
        try:
            with urllib.request.urlopen("%s/%s" % (base, rel), timeout=60) as resp:
                return resp.read(), base
        except Exception as exc:  # noqa: BLE001 - keyingi oyna sinaladi
            last = exc
    raise RuntimeError("%s:%s:%s yuklanmadi (%s)" % (group, art, version, last))


def pom_props(text):
    props = {}
    m = re.search(r"<properties>(.*?)</properties>", text, re.S)
    if m:
        props.update(re.findall(r"<([\w.\-]+)>([^<]*)</\1>", m.group(1)))
    v = re.search(r"<artifactId>[^<]+</artifactId>\s*<version>([^<]+)</version>", text)
    if v:
        props["project.version"] = v.group(1)
    parent = re.search(r"<parent>.*?<version>([^<]+)</version>.*?</parent>", text, re.S)
    if parent:
        props.setdefault("project.parent.version", parent.group(1))
        props.setdefault("project.version", parent.group(1))
    return props


def resolve(value, props):
    for _ in range(5):
        new = re.sub(r"\$\{([^}]+)\}", lambda m: props.get(m.group(1), m.group(0)), value)
        if new == value:
            break
        value = new
    return value


def bom_managed(group, art, version, seen, notes):
    """BOM va u import qilgan BOMlar boshqaradigan {groupId: {artifactId}}."""
    out = collections.defaultdict(set)
    if (group, art) in seen:
        return out
    seen.add((group, art))
    try:
        text = fetch(group, art, version, "pom")[0].decode("utf-8")
    except RuntimeError as exc:
        notes.append(str(exc))
        return out
    props = pom_props(text)
    dm = re.search(r"<dependencyManagement>(.*?)</dependencyManagement>", text, re.S)
    for chunk in DEP_RE.findall(dm.group(1) if dm else ""):
        g, a = resolve(tag(chunk, "groupId") or "", props), tag(chunk, "artifactId") or ""
        a = resolve(a, props)
        if tag(chunk, "scope") == "import":
            v = resolve(tag(chunk, "version") or "", props)
            if "${" in v:
                notes.append("%s:%s versiyasi aniqlanmadi (%s)" % (g, a, v))
                continue
            for k, vals in bom_managed(g, a, v, seen, notes).items():
                out[k] |= vals
        elif "${" not in g + a:
            out[g].add(a)
    return out


def boot_metadata(version, notes):
    text = fetch("org.springframework.boot", "spring-boot-dependencies", version,
                 "pom")[0].decode("utf-8")
    arts = sorted(set(a for a in re.findall(
        r"<groupId>org\.springframework\.boot</groupId>\s*<artifactId>([^<]+)</artifactId>",
        text) if "starter" not in a and a not in NO_METADATA))
    props = {}
    for art in arts:
        try:
            data = fetch("org.springframework.boot", art, version, "jar")[0]
        except RuntimeError as exc:
            notes.append(str(exc))
            continue
        with zipfile.ZipFile(io.BytesIO(data)) as jar:
            try:
                meta = json.loads(jar.read("META-INF/spring-configuration-metadata.json"))
            except KeyError:
                continue
        for p in meta.get("properties", []):
            props[p["name"]] = p
    return props, len(arts)


def regenerate(data_dir=None):
    data_dir = data_dir or DATA
    notes = []
    old, n_old = boot_metadata(BOOT_OLD, notes)
    new, n_new = boot_metadata(BOOT_NEW, notes)
    rows = []

    def deprecated(p):
        return p.get("deprecated") or p.get("deprecation")

    for name in sorted(set(old) | set(new)):
        p_old, p_new = old.get(name), new.get(name)
        if p_new is not None and not deprecated(p_new):
            continue
        if p_new is None and p_old is None:
            continue
        src = p_new if p_new is not None else p_old
        dep = (src.get("deprecation") or {}) if deprecated(src) else {}
        boot = "3.5" if p_old is not None and deprecated(p_old) else "4.1"
        level = "removed" if p_new is None else dep.get("level", "warning")
        kind = "map" if str(src.get("type", "")).startswith("java.util.Map") else ""
        rows.append("\t".join([name, boot, level, dep.get("replacement", ""),
                               dep.get("since", ""), kind]))
    with io.open(os.path.join(data_dir, "boot_deprecated.tsv"), "w",
                 encoding="utf-8", newline="\n") as handle:
        handle.write(
            "# Spring Boot sozlama kalitlarining deprecation ro'yxati. Yasovchi:\n"
            "# `python3 tools/verify_claims.py --yangila`, qo'lda tahrir qilinmaydi.\n"
            "# Manba: org.springframework.boot:*:%s (%d modul) va *:%s (%d modul)\n"
            "# jarlaridagi META-INF/spring-configuration-metadata.json, Maven Central\n"
            "# (https://repo1.maven.org/maven2/org/springframework/boot/).\n"
            "# boot: kalit qaysi versiyada deprecated bo'lgan (3.5 = bazada ham).\n"
            "# daraja: %s metadata sidagi level; removed = %s da kalit yo'q.\n"
            "kalit\tboot\tdaraja\talmashtirish\tsince\ttur\n"
            % (BOOT_OLD, n_old, BOOT_NEW, n_new, BOOT_NEW, BOOT_NEW))
        handle.write("\n".join(rows) + "\n")
    managed_new = bom_managed("org.springframework.boot", "spring-boot-dependencies",
                              BOOT_NEW, set(), notes)
    managed_old = bom_managed("org.springframework.boot", "spring-boot-dependencies",
                              BOOT_OLD, set(), notes)
    lines = []
    for group in sorted(managed_new):
        lines.append("4.1\t%s\t%s" % (group, " ".join(sorted(managed_new[group]))))
    for group in sorted(managed_old):
        gone = managed_old[group] - managed_new.get(group, set())
        if gone:
            lines.append("3.5\t%s\t%s" % (group, " ".join(sorted(gone))))
    with io.open(os.path.join(data_dir, "boot_managed.tsv"), "w",
                 encoding="utf-8", newline="\n") as handle:
        handle.write(
            "# Spring Boot BOM boshqaradigan groupId:artifactId (import qilingan BOMlar\n"
            "# bilan). Yasovchi: `python3 tools/verify_claims.py --yangila`.\n"
            "# Manba: org.springframework.boot:spring-boot-dependencies:%s va :%s pom,\n"
            "# Maven Central. 4.1 qatorlari to'liq ro'yxat, 3.5 qatorlari faqat 4.1 da\n"
            "# yo'qlari.\n"
            "boot\tgroupId\tartifactId\n" % (BOOT_NEW, BOOT_OLD))
        handle.write("\n".join(lines) + "\n")
    print("boot_deprecated.tsv: %d kalit; boot_managed.tsv: %d guruh (4.1)"
          % (len(rows), len(managed_new)))
    for note in notes:
        print("eslatma: %s" % note)
    return 0


# --- CLI ---------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("files", nargs="*", help="faqat shu boblar (docs/... yo'li)")
    parser.add_argument("--java", action="store_true",
                        help="```java bloklarni javac parserida tekshirish")
    parser.add_argument("--diff", nargs="?", const="HEAD", metavar="REF",
                        help="faqat REF (standart HEAD) dan beri o'zgargan boblar")
    parser.add_argument("--faqat", metavar="TUR,..",
                        help="tekshiruv turlari: %s" % ",".join(KINDS))
    parser.add_argument("--izohli", action="store_true",
                        help="versiya izohi tufayli o'tkazilganlarni ham ko'rsatish")
    parser.add_argument("--yangila", action="store_true",
                        help="claims_data dagi Boot ro'yxatlarini qayta yasash (tarmoq)")
    args = parser.parse_args(argv)
    if args.yangila:
        return regenerate()
    kinds = list(DEFAULT_KINDS) + (["java"] if args.java else [])
    if args.faqat:
        kinds = [k.strip() for k in args.faqat.split(",") if k.strip()]
        bad = [k for k in kinds if k not in KINDS]
        if bad:
            parser.error("noma'lum tur: %s" % ", ".join(bad))
    files = args.files or None
    if args.diff:
        files = changed_files(ROOT, args.diff)
        if not files:
            print("o'zgargan bob yo'q (%s)" % args.diff)
            return 0
    notes, excused = [], ([] if args.izohli else None)
    found = collect(ROOT, files, kinds, notes, excused=excused)
    for f in found:
        print(fmt(f))
    for f in excused or ():
        print("izohli  " + fmt(f))
    for note in notes:
        print("eslatma: %s" % note)
    by_kind = collections.Counter(f.tur for f in found)
    print("\n%d topilma%s" % (len(found), (" (" + ", ".join(
        "%s %d" % kv for kv in sorted(by_kind.items())) + ")") if found else ""))
    return 1 if found else 0


if __name__ == "__main__":
    # `| head` yopgan quvur: Linux da BrokenPipeError, Windows da OSError
    # (EINVAL). Traceback chiqmasin.
    try:
        code = main()
        sys.stdout.flush()
    except OSError as exc:
        if not isinstance(exc, BrokenPipeError) and exc.errno != errno.EINVAL:
            raise
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        code = 1
    sys.exit(code)
