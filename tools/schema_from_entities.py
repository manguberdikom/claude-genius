#!/usr/bin/env python3
"""JPA entity sinflaridan baza sxemasini va ehtimoliy muammolarni chiqaradi.

    python3 tools/schema_from_entities.py <manba_papka> [--json] [--only-findings] [--migrations <papka>]

Nega: baza tuzilishini bilish uchun konteyner ko'tarish, ulanish ochish va
`\\d+` yurgizish shart emas. Jadval, ustun va tashqi kalitni entity
sinflari tasvirlaydi, ularni o'qish esa bir necha millisekund va nol pul
turadi. Indeks esa ko'pincha migratsiyada yoziladi: loyihada
`db/migration` yoki `db/changelog` bo'lsa, u ham o'qiladi, boshqa joyda
bo'lsa `--migrations` beriladi. Topilgan muammolar ham xuddi shunday:
`@ManyToOne` ning default fetch turi EAGER ekanini ko'rish uchun so'rov
yurgizish kerak emas, buni kod aytib turibdi.

Chiqish ikki qism: jadval tuzilishi va ogohlantirishlar. Har bir
ogohlantirish qo'llanmadagi tegishli bo'limga ulanadi, shuning uchun
"nega yomon" degan savolga javob bir buyruq narida turadi.

Bu Java parser emas, lekin regex ning odatiy tuzoqlari chetlab o'tiladi:
izoh avval olib tashlanadi, satr literali maskalanadi, qavslar sanab
yopiladi. Shu tufayli Javadoc dagi "class" so'zi, `@Table(indexes = {...})`
kabi ichma-ich annotatsiya va metod tanasi natijani buzmaydi. O'tish
ikkita: avval hamma sinf o'qiladi, keyin entity quriladi, chunki
`@MappedSuperclass`, `@Inheritance`, `@Embeddable` va FK nishonining
`@Id` turi boshqa faylda turadi.
"""

import json
import os
import re
import signal
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from docref import hint  # noqa: E402

# Satr, matn bloki va belgi literali. Izoh tozalanganda ular joyida
# qoladi: aks holda "https://..." ichidagi `//` qatorning qolganini yeb
# qo'yardi.
LITERAL = r'"""[\s\S]*?"""|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])+\''
LITERAL_RE = re.compile(LITERAL)
COMMENT_RE = re.compile(r"(%s)|/\*[\s\S]*?\*/|//[^\n]*" % LITERAL)
# @jakarta.persistence.Id -> @Id
QUALIFIER_RE = re.compile(r"@(?:[a-z_]\w*\.)+(?=[A-Z])")
TYPE_HEAD_RE = re.compile(r"\b(class|record|enum|interface)\s+([\w$]+)")
ANN_NAME_RE = re.compile(r"@([\w$.]+)")
WORD_RE = re.compile(r"[\w$-]+")
DECL_RE = re.compile(r"^([\w$<>,.?@\[\]\s]+?)\s+([\w$]+)\s*((?:\[\s*\]\s*)*)$")
COLLECTION_RE = re.compile(r"^(?:List|Set|SortedSet|Collection|Map|SortedMap)\s*<")

MODIFIERS = {"public", "protected", "private", "static", "final", "transient",
             "volatile", "abstract", "synchronized", "native", "default",
             "strictfp", "sealed", "non-sealed"}
NOT_A_TYPE = {"class", "enum", "interface", "record", "return", "package",
              "import", "throw", "new"}
# Bular bor bo'lsa ustun turini konvertor yoki Hibernate turi belgilaydi.
CONVERTERS = ("Convert", "JdbcType", "JdbcTypeCode", "Type")
SKIP_DIRS = {".git", "target", "build", "node_modules", ".gradle", ".idea"}
BUILD_FILES = ("pom.xml", "build.gradle", "build.gradle.kts",
               "settings.gradle", "settings.gradle.kts")
MIGRATION_EXT = (".sql", ".xml", ".yaml", ".yml", ".json")

JAVA_TO_SQL = {
    "String": "varchar",
    "UUID": "uuid",
    "Long": "bigint", "long": "bigint",
    "Integer": "integer", "int": "integer",
    "Short": "smallint", "short": "smallint",
    "Byte": "smallint", "byte": "smallint",
    "Character": "char(1)", "char": "char(1)",
    "Boolean": "boolean", "boolean": "boolean",
    "BigDecimal": "numeric",
    "BigInteger": "numeric",
    "Double": "double precision", "double": "double precision",
    "Float": "real", "float": "real",
    "Instant": "timestamptz",
    "OffsetDateTime": "timestamptz",
    "ZonedDateTime": "timestamptz",
    "LocalDateTime": "timestamp",
    "LocalDate": "date",
    "LocalTime": "time",
    "Duration": "interval",
    "byte[]": "bytea", "Byte[]": "bytea",
    # Eski turlar: xaritalanadi, lekin check() ogohlantiradi.
    "Date": "timestamp",
    "Calendar": "timestamp",
}

# Alias bilan topilmaydigan mavzular uchun aniq bo'lim. Raqam eskirsa
# (bo'lim indeksda yo'q), sarlavha matni bo'yicha `find` ga qaytiladi.
FK_REF = ("code-review 26.6", "Tashqi kalitlar va o'chirish qoidalari")
ENUM_REF = ("code-review 14.8", "switch, enum va sealed")
VARCHAR_REF = ("architect 25.1", "Turni to'g'ri tanlash")
DATE_REF = ("clean-code 22.1", "Calendar")


def snake(name):
    """Spring/Hibernate CamelCaseToUnderscoresNamingStrategy bilan bir xil:
    `totalAmount` -> total_amount, `serialVersionUID` -> serial_versionuid."""
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z][a-z0-9])", "_",
                  name.replace(".", "_")).lower()


def has(block, annotation):
    return re.search(r"@%s\b" % annotation, block) is not None


def strip_comments(text):
    return COMMENT_RE.sub(lambda m: m.group(1) or " ", text)


def mask(text):
    """Literal ichini bo'sh joy bilan to'ldiradi. Uzunlik o'zgarmaydi,
    shuning uchun maskadagi indeks asl matnda ham o'sha joy, literal
    ichidagi qavs, `;` va `@` esa tuzilishni buzmaydi."""
    return LITERAL_RE.sub(
        lambda m: m.group()[0] + " " * (len(m.group()) - 2) + m.group()[-1],
        text)


def match_close(masked, i):
    """masked[i] dagi `(` yoki `{` ga mos yopuvchidan keyingi indeks."""
    opener = masked[i]
    closer = ")" if opener == "(" else "}"
    depth = 0
    for j in range(i, len(masked)):
        if masked[j] == opener:
            depth += 1
        elif masked[j] == closer:
            depth -= 1
            if depth == 0:
                return j + 1
    return len(masked)


def split_top(masked, lo, hi, opens="(<{[", closes=")>}]"):
    """masked[lo:hi] ni yuqori darajadagi vergul bo'yicha bo'ladi."""
    parts, depth, start = [], 0, lo
    for i in range(lo, hi):
        if masked[i] in opens:
            depth += 1
        elif masked[i] in closes:
            depth -= 1
        elif masked[i] == "," and depth == 0:
            parts.append((start, i))
            start = i + 1
    parts.append((start, hi))
    return parts


def top_arg(args, key):
    """`(key = "qiymat")` ning yuqori darajadagi qiymati, massiv bo'lsa
    birinchi elementi. `@Table(indexes = @Index(name = ...))` dagi ichki
    `name` hisobga olinmaydi, argumentlar tartibi ahamiyatsiz."""
    if not args:
        return None
    masked = mask(args)
    pattern = re.compile(r'\b%s\s*=\s*(?:\{\s*)?"' % key)
    depth = 0
    for i, ch in enumerate(masked):
        if ch in "({":
            depth += 1
        elif ch in ")}":
            depth -= 1
        elif depth == 1:
            match = pattern.match(masked, i)
            if match:
                return args[match.end():masked.find('"', match.end())]
    return None


def bare_value(args):
    """`@MapsId("orderId")` -> orderId."""
    match = re.match(r'\(\s*"([^"]*)"\s*\)$', (args or "").strip())
    return match.group(1) if match else top_arg(args, "value")


def find_annotations(text, name):
    """`@name(...)` ning har uchrashidagi argumentlari, ichma-ichlari ham.
    Qavssiz annotatsiya uchun bo'sh satr."""
    masked = mask(text)
    out = []
    for match in re.finditer(r"@%s\b" % name, masked):
        k = match.end()
        while k < len(masked) and masked[k].isspace():
            k += 1
        if k < len(masked) and masked[k] == "(":
            out.append(text[k:match_close(masked, k)])
        else:
            out.append("")
    return out


def first(items):
    return items[0] if items else ""


def leading(columns):
    """"created_by, owner_id DESC" -> created_by. FK so'rovini indeksning
    faqat bosh ustuni qamraydi."""
    head = (columns or "").split(",")[0].split()
    return head[0].strip('"`').lower() if head else ""


class Finding:
    def __init__(self, level, table, column, message, topic, ref=""):
        self.level = level
        self.table = table
        self.column = column
        self.message = message
        self.topic = topic
        self.ref = ref

    def as_dict(self):
        return {"level": self.level, "table": self.table,
                "column": self.column, "message": self.message,
                "topic": self.topic, "ref": self.ref}


# ---------------------------------------------------------------- o'qish

def members(masked, lo, hi):
    """Tana a'zolarining chegarasi: ("field", bosh, oxir) yoki
    ("type", bosh, `{` indeksi, tana oxiri).

    `;` bayonotni tugatadi. Qavs darajasi 0 dagi `{` blok ochadi: oldida
    `=` bo'lsa bu massiv yoki lambda initsializatori va bayonot davom
    etadi, aks holda metod, konstruktor, initsializator yoki ichki tur.
    """
    out = []
    start, paren, eq, i = lo, 0, False, lo
    while i < hi:
        ch = masked[i]
        if ch == "(":
            paren += 1
        elif ch == ")":
            paren -= 1
        elif paren == 0 and ch == "=":
            eq = True
        elif paren == 0 and ch == ";":
            out.append(("field", start, i))
            start, eq = i + 1, False
        elif paren == 0 and ch == "{":
            close = match_close(masked, i)
            if not eq:
                if type_head(masked, start, i):
                    out.append(("type", start, i, close))
                start = close
            i = close
            continue
        i += 1
    return out


def type_head(masked, lo, hi):
    """Qavsdan tashqaridagi birinchi `class|record|enum|interface Nom`."""
    for match in TYPE_HEAD_RE.finditer(masked, lo, hi):
        before = masked[lo:match.start()]
        if before.count("(") == before.count(")"):
            return match
    return None


def parse_field(orig, masked):
    """Bitta bayonot maydon e'loni bo'lsa uning yozuvi, aks holda None.

    Annotatsiya va modifikator istalgan tartibda keladi, modifikator
    ixtiyoriy: Lombok `@FieldDefaults` bilan package-private maydon ham
    maydon. static va transient maydon ustun emas.
    """
    i, n = 0, len(masked)
    anns, raw, mods = {}, [], set()
    while i < n:
        if masked[i].isspace():
            i += 1
            continue
        if masked[i] == "@":
            match = ANN_NAME_RE.match(masked, i)
            if not match or match.group(1) == "interface":
                return None
            j = k = match.end()
            while k < n and masked[k].isspace():
                k += 1
            args = ""
            if k < n and masked[k] == "(":
                j = match_close(masked, k)
                args = orig[k:j]
            anns.setdefault(match.group(1).rsplit(".", 1)[-1], args)
            raw.append(orig[i:j])
            i = j
            continue
        word = WORD_RE.match(masked, i)
        if word and word.group() in MODIFIERS:
            mods.add(word.group())
            i = word.end()
            continue
        break
    if mods & {"static", "transient"}:
        return None
    paren, end = 0, n
    for j in range(i, n):
        if masked[j] == "(":
            paren += 1
        elif masked[j] == ")":
            paren -= 1
        elif masked[j] == "=" and paren == 0:
            end = j
            break
    decl = " ".join(orig[i:end].split())
    if "(" in decl:             # metod yoki konstruktor
        return None
    match = DECL_RE.match(decl)
    if not match or match.group(1).split()[0].split("<")[0] in NOT_A_TYPE:
        return None
    java = " ".join(match.group(1).split()) + "[]" * match.group(3).count("[")
    if "<" not in java:
        java = java.rsplit(".", 1)[-1]   # java.math.BigDecimal -> BigDecimal
    return {"field": match.group(2), "java": java, "anns": anns,
            "ann": QUALIFIER_RE.sub("@", " ".join(raw))}


def parse_body(orig, masked, path, lo, hi, out, enums):
    """Tana: maydonlar qaytariladi, ichki turlar `out` ga yoziladi."""
    fields = []
    for item in members(masked, lo, hi):
        if item[0] == "field":
            entry = parse_field(orig[item[1]:item[2]], masked[item[1]:item[2]])
            if entry:
                fields.append(entry)
        else:
            parse_type(orig, masked, path, item[1:], out, enums)
    return fields


def parse_type(orig, masked, path, span, out, enums):
    start, brace, close = span
    head = type_head(masked, start, brace)
    keyword, name = head.group(1), head.group(2)
    if keyword in ("enum", "interface"):
        if keyword == "enum":
            enums.add(name)
        parse_body(orig, masked, path, brace + 1, close - 1, out, enums)
        return
    annotations = QUALIFIER_RE.sub("@", orig[start:head.start()])
    info = {"name": name, "file": path, "head": annotations,
            "kind": kind_of(annotations),
            "extends": extends_of(masked[head.end():brace]), "fields": []}
    if keyword == "record":
        p = masked.find("(", head.end(), brace)
        if p >= 0:
            for s, e in split_top(masked, p + 1, match_close(masked, p) - 1):
                entry = parse_field(orig[s:e], masked[s:e])
                if entry:
                    info["fields"].append(entry)
    info["fields"] += parse_body(orig, masked, path, brace + 1, close - 1,
                                 out, enums)
    out.append(info)


def kind_of(head):
    for annotation, kind in (("Entity", "entity"), ("MappedSuperclass", "mapped"),
                             ("Embeddable", "embeddable")):
        if has(head, annotation):
            return kind
    return "other"


def extends_of(tail):
    """`Product<T> extends BaseEntity<Long> implements X` -> BaseEntity."""
    flat = re.sub(r"<[^<>]*>", "", tail)
    while flat != tail:
        tail, flat = flat, re.sub(r"<[^<>]*>", "", flat)
    match = re.search(r"\bextends\s+([\w$.]+)", tail)
    return match.group(1).rsplit(".", 1)[-1] if match else None


def collect(src):
    """Birinchi o'tish: har .java dagi sinflar va enum nomlari."""
    types, enums = {}, set()
    for dirpath, dirnames, filenames in os.walk(src):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if not name.endswith(".java"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8", errors="replace") as handle:
                text = strip_comments(handle.read())
            found = []
            parse_body(text, mask(text), os.path.relpath(path, src),
                       0, len(text), found, enums)
            for info in found:
                old = types.get(info["name"])
                if old is None or old["kind"] == "other":
                    types[info["name"]] = info
    return types, enums


# ------------------------------------------------------------ migratsiya

CREATE_INDEX_RE = re.compile(
    r'create\s+(?:unique\s+)?index\s+(?:concurrently\s+)?(?:if\s+not\s+exists\s+)?'
    r'(?:[\w"]+\s+)?on\s+(?:only\s+)?([\w."]+)\s*(?:using\s+\w+\s*)?\(([^)]*)\)',
    re.I)
ALTER_KEY_RE = re.compile(
    r'alter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?([\w."]+)\s+add\s+'
    r'(?:constraint\s+[\w"]+\s+)?(?:unique|primary\s+key)\s*\(([^)]*)\)', re.I)
CREATE_TABLE_RE = re.compile(
    r'create\s+table\s+(?:if\s+not\s+exists\s+)?([\w."]+)\s*\(', re.I)
TABLE_KEY_RE = re.compile(
    r'^(?:constraint\s+[\w"]+\s+)?(?:primary\s+key|unique)\s*\(([^)]*)\)', re.I)
INLINE_KEY_RE = re.compile(r"\b(?:primary\s+key|unique)\b", re.I)
LB_INDEX_RE = re.compile(r"<createIndex\b([^>]*)>(.*?)</createIndex>", re.S)
LB_KEY_RE = re.compile(r"<(?:addUniqueConstraint|addPrimaryKey)\b([^>]*?)/?>", re.S)
LB_COLUMN_RE = re.compile(r'<column\b[^>]*\bname="([^"]+)"')
ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


def project_root(src):
    """src dan yuqoriga qarab build fayli bor papka. Git ildizidan
    tashqariga chiqilmaydi."""
    path = os.path.abspath(src)
    while True:
        if any(os.path.isfile(os.path.join(path, f)) for f in BUILD_FILES):
            return path
        parent = os.path.dirname(path)
        if os.path.exists(os.path.join(path, ".git")) or parent == path:
            return None
        path = parent


def migration_files(src, explicit=None):
    """`--migrations` papkasi yoki loyiha ildizidagi db/migration va
    db/changelog ichidagi fayllar."""
    tops = [explicit] if explicit else []
    root = None if explicit else project_root(src)
    if root:
        for dirpath, dirnames, _ in os.walk(root):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            if (os.path.basename(dirpath) in ("migration", "changelog")
                    and os.path.basename(os.path.dirname(dirpath)) == "db"):
                tops.append(dirpath)
                dirnames[:] = []
    files = []
    for top in tops:
        for dirpath, dirnames, filenames in os.walk(top):
            dirnames.sort()
            files += [os.path.join(dirpath, f) for f in sorted(filenames)
                      if f.endswith(MIGRATION_EXT)]
    return files


def read_migrations(files):
    """(migratsiya bormi, {jadval: {indeks bosh ustunlari}}).

    SQL dan CREATE INDEX, PRIMARY KEY va UNIQUE, Liquibase XML dan
    createIndex va addUniqueConstraint/addPrimaryKey olinadi. YAML
    o'qilmaydi, lekin uning borligi ham "migratsiya bor" degani.
    """
    indexes = {}

    def add(table, columns):
        column = leading(columns)
        if column:
            key = table.replace('"', "").split(".")[-1].lower()
            indexes.setdefault(key, set()).add(column)

    for path in files:
        with open(path, encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        if path.endswith(".sql"):
            text = re.sub(r"--[^\n]*|/\*[\s\S]*?\*/", " ", text)
            for table, columns in CREATE_INDEX_RE.findall(text) + ALTER_KEY_RE.findall(text):
                add(table, columns)
            for match in CREATE_TABLE_RE.finditer(text):
                body_end = match_close(text, match.end() - 1) - 1
                for s, e in split_top(text, match.end(), body_end, "(", ")"):
                    item = text[s:e].strip()
                    key = TABLE_KEY_RE.match(item)
                    if key:
                        add(match.group(1), key.group(1))
                    elif INLINE_KEY_RE.search(item) and not re.match(
                            r"(?:constraint|foreign|check|exclude)\b", item, re.I):
                        add(match.group(1), item)
        elif path.endswith(".xml"):
            for attrs, body in LB_INDEX_RE.findall(text):
                column = LB_COLUMN_RE.search(body)
                table = dict(ATTR_RE.findall(attrs)).get("tableName")
                if table and column:
                    add(table, column.group(1))
            for attrs in LB_KEY_RE.findall(text):
                values = dict(ATTR_RE.findall(attrs))
                if values.get("tableName"):
                    add(values["tableName"], values.get("columnNames"))
    return bool(files), indexes


# --------------------------------------------------------------- qurish

class Context:
    def __init__(self, types, enums, migrations):
        self.types = types
        self.enums = enums
        self.migrations = migrations   # (topildimi, {jadval: {bosh ustun}})
        self.built = {}


def column_name(anns):
    return (top_arg(anns.get("Column"), "name")
            or top_arg(anns.get("JoinColumn"), "name"))


def attribute_overrides(ann):
    """@AttributeOverride(name = "maydon", column = @Column(...)) ->
    {maydon: @Column argumentlari}."""
    out = {}
    for args in find_annotations(ann, "AttributeOverride"):
        field, column = top_arg(args, "name"), find_annotations(args, "Column")
        if field and column:
            out[field] = column[0]
    return out


def classify(field, ctx, origin, stack=()):
    """Maydon -> sxema yozuvlari. @Embedded bir nechta ustunga yoyiladi.

    `origin` - maydon kelgan @MappedSuperclass yoki @Embeddable nomi.
    Bunday maydonning ta'rif topilmalari o'sha sinf nomi ostida bir marta
    chiqadi, jadvalga bog'liq FK indeks tekshiruvi esa har jadvalda.
    """
    entry = dict(field, origin=origin)
    ann, anns, java = entry["ann"], entry["anns"], entry["java"]
    if has(ann, "Transient"):
        return []
    entry["pk"] = has(ann, "Id")
    if has(ann, "ManyToOne") or has(ann, "OneToOne"):
        relation = anns.get("ManyToOne") or anns.get("OneToOne") or ""
        if top_arg(relation, "mappedBy"):
            entry.update(kind="inverse", name=entry["field"])
            return [entry]
        target = re.search(r"targetEntity\s*=\s*([\w$.]+)\.class", relation)
        entry.update(kind="fk",
                     name=column_name(anns) or snake(entry["field"]) + "_id",
                     target=target.group(1).rsplit(".", 1)[-1] if target else java)
        if "MapsId" in anns:
            entry["mapsid"] = bare_value(anns["MapsId"]) or ""
        return [entry]
    if (has(ann, "OneToMany") or has(ann, "ManyToMany") or has(ann, "ElementCollection")
            or (COLLECTION_RE.match(java) and not entry["pk"]
                and not any(a in anns for a in ("Column", "Lob") + CONVERTERS))):
        table = anns.get("JoinTable") or anns.get("CollectionTable")
        entry.update(kind="collection", name=entry["field"],
                     join_table=top_arg(table, "name"))
        return [entry]
    embeddable = ctx.types.get(java)
    is_embeddable = embeddable is not None and embeddable["kind"] == "embeddable"
    if has(ann, "Embedded") or has(ann, "EmbeddedId") or is_embeddable:
        if is_embeddable and java not in stack:
            overrides = attribute_overrides(ann)
            out = []
            for sub in embeddable["fields"]:
                for part in classify(sub, ctx, java, stack + (java,)):
                    column = overrides.get(part["field"])
                    if column and part["kind"] in ("column", "fk"):
                        # Override @Column ni to'liq almashtiradi: eski
                        # length/precision qolib ketmasin.
                        old = part["anns"].get("Column")
                        if old:
                            part["ann"] = part["ann"].replace(old, "", 1)
                        part["name"] = top_arg(column, "name") or part["name"]
                        part["anns"] = dict(part["anns"], Column=column)
                        part["ann"] += " @Column" + column
                    part["pk"] = part["pk"] or has(ann, "EmbeddedId")
                    out.append(part)
            return out
        entry["pk"] = entry["pk"] or has(ann, "EmbeddedId")
    entry.update(kind="column", name=column_name(anns) or snake(entry["field"]),
                 enum=java in ctx.enums)
    return [entry]


def ancestry(info, types):
    """extends zanjiri: (@MappedSuperclass ajdodlar, eng yaqin @Entity
    ajdod, manbada topilmagan ota nomi)."""
    mapped, seen, current = [], {info["name"]}, info
    while current.get("extends"):
        name = current["extends"]
        if name in seen:
            break
        seen.add(name)
        current = types.get(name)
        if current is None:
            return mapped, None, name
        if current["kind"] == "entity":
            return mapped, current, None
        if current["kind"] == "mapped":
            mapped.append(current)
    return mapped, None, None


def inheritance(head):
    args = first(find_annotations(head, "Inheritance"))
    for strategy in ("JOINED", "TABLE_PER_CLASS"):
        if strategy in args:
            return strategy
    return "SINGLE_TABLE"


def declared_indexes(head):
    """@Index va @UniqueConstraint bosh ustunlari, @Table ichida yoki
    tashqarisida, tartibidan qat'i nazar."""
    out = {leading(top_arg(a, "columnList")) for a in find_annotations(head, "Index")}
    out |= {leading(top_arg(a, "columnNames"))
            for a in find_annotations(head, "UniqueConstraint")}
    out.discard("")
    return out


def build(name, ctx):
    """Ikkinchi o'tish: entity meros va yoyilgan ustunlari bilan.

    SINGLE_TABLE (default) vorisning ustunlari ildiz jadvalga qo'shiladi,
    alohida jadval chiqmaydi. JOINED voris o'z jadvalini va PK/FK
    ustunini oladi. TABLE_PER_CLASS voris ota ustunlarini nusxalaydi.
    """
    if name in ctx.built:
        return ctx.built[name]
    ctx.built[name] = None       # sikldan himoya
    info = ctx.types[name]
    mapped, parent, missing = ancestry(info, ctx.types)
    entries = []
    for ancestor in reversed(mapped):
        for field in ancestor["fields"]:
            entries.extend(classify(field, ctx, ancestor["name"]))
    for field in info["fields"]:
        entries.extend(classify(field, ctx, None))
    head = info["head"]
    entity = {
        "class": name, "file": info["file"], "head": head,
        "table": (top_arg(first(find_annotations(head, "Table")), "name")
                  or snake(top_arg(first(find_annotations(head, "Entity")), "name")
                           or name)),
        "entries": entries, "indexed": declared_indexes(head),
        "missing": missing, "merged": False, "subclasses": [],
        "inherits_id": False, "inherits_version": False,
    }
    entity["root"] = entity
    base = build(parent["name"], ctx) if parent else None
    if parent and base is None:
        entity["missing"] = parent["name"]
    elif base:
        root = entity["root"] = base["root"]
        entity["inherits_id"] = True
        entity["inherits_version"] = has_version(base)
        strategy = inheritance(root["head"])
        if strategy == "SINGLE_TABLE":
            entity["merged"] = True
            for entry in entries:
                entry["owner"] = name
            root["entries"].extend(entries)
            root["subclasses"].append(name)
        elif strategy == "JOINED":
            pk = [e["name"] for e in root["entries"] if e.get("pk")]
            join = first(find_annotations(head, "PrimaryKeyJoinColumn"))
            entries.insert(0, {
                "field": "-", "java": "", "ann": "", "anns": {}, "origin": None,
                "kind": "pkjoin", "pk": True, "target": root["class"],
                "name": top_arg(join, "name") or (pk[0] if len(pk) == 1 else "id")})
        else:
            entity["entries"] = [dict(e, origin=e["origin"] or base["class"])
                                 for e in base["entries"]] + entries
    ctx.built[name] = entity
    return entity


def has_version(entity):
    return entity["inherits_version"] or any(
        has(e["ann"], "Version") for e in entity["entries"])


def add_discriminator(entity):
    """SINGLE_TABLE ildizida vorislarni ajratuvchi ustun (default dtype)."""
    args = first(find_annotations(entity["head"], "DiscriminatorColumn"))
    if not (args or has(entity["head"], "DiscriminatorColumn")
            or (entity["subclasses"] and inheritance(entity["head"]) == "SINGLE_TABLE")):
        return
    length = re.search(r"length\s*=\s*(\d+)", args)
    sql = ("integer" if "INTEGER" in args else "char(1)" if "CHAR" in args
           else "varchar(%s)" % (length.group(1) if length else "31"))
    entity["entries"].insert(0, {
        "field": "-", "java": "", "ann": "", "anns": {}, "origin": None,
        "kind": "discriminator", "pk": False, "sql": sql,
        "name": top_arg(args, "name") or "dtype"})


def resolve_fk(entry, ctx, depth=0):
    """FK ustuni turi nishon entity @Id turi bilan bir xil. Nishon
    manbada bo'lmasa taxmin `bigint?` deb belgilanadi."""
    if "fk_type" not in entry:
        target = ctx.built.get(entry.get("target"))
        pk = [e for e in target["root"]["entries"] if e.get("pk")] if target else []
        if len(pk) > 1:
            entry["fk_type"] = "kompozit"
        elif pk and depth < 5:
            if pk[0]["kind"] in ("fk", "pkjoin"):
                resolve_fk(pk[0], ctx, depth + 1)
            entry["fk_type"] = sql_type(pk[0])
        else:
            entry["fk_type"] = "bigint?"
    return entry["fk_type"]


def columns_of(entity):
    return [e for e in entity["entries"]
            if e["kind"] in ("column", "fk", "pkjoin", "discriminator")
            and "mapsid" not in e]


def relations_of(entity):
    return [e for e in entity["entries"]
            if e["kind"] in ("fk", "collection", "inverse")]


def converted(entry):
    return any(a in entry["anns"] for a in CONVERTERS)


def is_enum(entry):
    return has(entry["ann"], "Enumerated") or entry.get("enum", False)


def is_ordinal(entry):
    return is_enum(entry) and "STRING" not in entry["ann"] and not converted(entry)


def sql_type(entry):
    kind, java, ann, anns = entry["kind"], entry["java"], entry["ann"], entry["anns"]
    if kind in ("fk", "pkjoin"):
        return entry.get("fk_type") or "bigint?"
    if kind == "discriminator":
        return entry["sql"]
    definition = top_arg(anns.get("Column"), "columnDefinition")
    if definition:
        return definition
    if has(ann, "Lob"):
        return "text"
    if "JSON" in (anns.get("JdbcTypeCode") or ""):
        return "jsonb"
    if is_enum(entry) and converted(entry):
        return "? (%s)" % java
    if is_ordinal(entry):
        return "integer"
    # STRING enum ham, oddiy String ham varchar: ikkalasida @Column(length)
    # hisobga olinadi, aks holda e'lon qilingan uzunlik yo'qolib ketardi.
    base = "varchar" if is_enum(entry) else JAVA_TO_SQL.get(java)
    if base == "varchar":
        length = re.search(r"length\s*=\s*(\d+)", ann)
        return "varchar(%s)" % (length.group(1) if length else "255")
    if base == "numeric":
        precision = re.search(r"precision\s*=\s*(\d+)", ann)
        scale = re.search(r"scale\s*=\s*(\d+)", ann)
        if precision and scale:
            return "numeric(%s,%s)" % (precision.group(1), scale.group(1))
        return "numeric"
    return base or "? (%s)" % java


# ------------------------------------------------------------ tekshirish

def column_findings(table, entry):
    """Maydon ta'rifiga bog'liq muammolar: tuzatish joyi maydonning o'zi."""
    out = []
    ann, name, java, kind = entry["ann"], entry["name"], entry["java"], entry["kind"]
    definition = top_arg(entry["anns"].get("Column"), "columnDefinition")

    if kind in ("fk", "inverse") and "fetch" not in ann:
        out.append(Finding(
            "yuqori", table, name,
            "@ManyToOne/@OneToOne da fetch ko'rsatilmagan, default EAGER. "
            "Har o'qishda qo'shimcha JOIN yoki alohida so'rov keladi.",
            "N+1 Problem Solutions"))

    if kind == "collection" and (has(ann, "OneToMany") or has(ann, "ManyToMany")):
        if "FetchType.EAGER" in ann:
            out.append(Finding(
                "yuqori", table, entry["field"],
                "Kolleksiya EAGER yuklanadi. Ikkita EAGER kolleksiya "
                "MultipleBagFetchException yoki dekart ko'paytmasini beradi.",
                "N+1 Queries"))
        if has(ann, "OneToMany") and "mappedBy" not in ann:
            out.append(Finding(
                "o'rta", table, entry["field"],
                "@OneToMany da mappedBy yo'q: Hibernate kutilmaganda "
                "qo'shimcha bog'lovchi jadval yasaydi.",
                "Association Table Mapping"))

    if kind in ("column", "collection") and is_ordinal(entry):
        out.append(Finding(
            "yuqori", table, name,
            ("@Enumerated default ORDINAL" if has(ann, "Enumerated") else
             "@Enumerated yo'q, enum default ORDINAL saqlanadi")
            + ": enum tartibi o'zgarsa bazadagi eski qatorlar boshqa "
            "qiymatga aylanadi.",
            ENUM_REF[1], ENUM_REF[0]))

    if kind != "column":
        return out
    if java == "BigDecimal" and "precision" not in ann and not definition:
        out.append(Finding(
            "yuqori", table, name,
            "Pul maydonida precision/scale yo'q: yaxlitlash xatosi va "
            "bazada kutilmagan aniqlik.",
            "Money"))
    if (java == "String" and "length" not in ann and not has(ann, "Lob")
            and not definition and not converted(entry)):
        out.append(Finding(
            "past", table, name,
            "Uzunlik ko'rsatilmagan, varchar(255) qabul qilinadi.",
            VARCHAR_REF[1], VARCHAR_REF[0]))
    if java in ("Date", "Calendar"):
        out.append(Finding(
            "o'rta", table, name,
            "Eski sana turi. java.time (Instant yoki LocalDate) "
            "mintaqa xatolarini oldini oladi.",
            DATE_REF[1], DATE_REF[0]))
    return out


def index_finding(entity, entry, ctx):
    """FK ustuni indekssiz bo'lsa topilma. Indeks deb hisoblanadi: @Index
    yoki @UniqueConstraint bosh ustuni, `unique = true`, bitta ustunli PK
    va migratsiyadagi indeks."""
    table, name = entity["table"], entry["name"]
    low = name.lower()
    pk = [e["name"].lower() for e in entity["entries"] if e.get("pk")]
    if "mapsid" in entry and not entry["mapsid"]:
        return None              # umumiy PK: ustun PK ning o'zi
    if low in pk or entry.get("mapsid"):
        if pk == [low]:
            return None
        return Finding(
            "o'rta", table, name,
            "Tashqi kalit kompozit PK tarkibida. PK indeksi uni faqat bosh "
            "ustun bo'lsa qamraydi: ustunlar tartibini tekshiring.",
            FK_REF[1], FK_REF[0])
    unique = any(re.search(r"\bunique\s*=\s*true", entry["anns"].get(a) or "")
                 for a in ("Column", "JoinColumn"))
    found, indexes = ctx.migrations
    if (unique or low in entity["indexed"]
            or low in indexes.get(table.lower(), ())):
        return None
    if found:
        return Finding(
            "o'rta", table, name,
            "Tashqi kalit ustunida indeks entity da ham, migratsiyada ham "
            "topilmadi. PostgreSQL FK uchun indeksni avtomatik yasamaydi: "
            "boshqa migratsiya yoki DROP INDEX bor-yo'qligini tekshiring.",
            FK_REF[1], FK_REF[0])
    return Finding(
        "yuqori", table, name,
        "Tashqi kalit ustunida indeks e'lon qilinmagan. PostgreSQL "
        "FK uchun indeksni avtomatik yasamaydi: JOIN va ota qator "
        "o'chirilishi sekinlashadi.",
        FK_REF[1], FK_REF[0])


def check(entity, ctx):
    """Kodni o'qib aytish mumkin bo'lgan muammolar. Hech narsa ishga tushmaydi."""
    out = []
    table = entity["table"]
    for entry in entity["entries"]:
        if entry["kind"] == "fk":
            finding = index_finding(entity, entry, ctx)
            if finding:
                out.append(finding)
        if entry.get("origin") is None and entry["kind"] not in ("pkjoin", "discriminator"):
            out.extend(column_findings(table, entry))

    pk = entity["inherits_id"] or any(e.get("pk") for e in entity["entries"])
    version = has_version(entity)
    if entity["missing"] and not (pk and version):
        lacking = " va ".join(n for n, ok in (("@Id", pk), ("@Version", version)) if not ok)
        out.append(Finding(
            "past", table, "-",
            "Ota sinf %s manbada yo'q: %s tekshirilmadi."
            % (entity["missing"], lacking),
            "Identity Field"))
        return out
    if not pk:
        out.append(Finding(
            "yuqori", table, "-", "@Id topilmadi.", "Identity Field"))
    if not version:
        out.append(Finding(
            "past", table, "-",
            "@Version yo'q: bir vaqtda yangilash jim yo'qotishga olib keladi.",
            "Optimistic Offline Lock"))
    return out


def definition_findings(ctx):
    """@MappedSuperclass va @Embeddable maydonlari bir marta, sinf nomi
    ostida tekshiriladi: ular o'nta jadvalga tushsa ham tuzatish joyi bitta."""
    out = []
    for name in sorted(ctx.types):
        info = ctx.types[name]
        if info["kind"] not in ("mapped", "embeddable"):
            continue
        for field in info["fields"]:
            for entry in classify(field, ctx, None, (name,)):
                if entry.get("origin") is None:
                    out.extend(column_findings(name, entry))
    return out


def guide(finding):
    """Aniq bo'lim indeksda bo'lsa o'sha, aks holda mavzu bo'yicha.
    Tekshiruv va buyruq yo'li docref da: yagona yo'l."""
    return hint(finding.topic, ref=finding.ref)


# ------------------------------------------------------------------ main

LEVEL_ORDER = {"yuqori": 0, "o'rta": 1, "past": 2}


def parse_args(argv):
    args, flags, migrations = [], set(), None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--migrations" and i + 1 < len(argv):
            migrations = argv[i + 1]
            i += 2
            continue
        if a.startswith("--migrations="):
            migrations = a.split("=", 1)[1]
        elif a.startswith("--"):
            flags.add(a)
        else:
            args.append(a)
        i += 1
    return args, flags, migrations


def analyse(src, migrations=None):
    """(entity'lar, topilmalar) - main va sinovlar uchun bitta yo'l."""
    types, enums = collect(src)
    ctx = Context(types, enums, read_migrations(migration_files(src, migrations)))
    for name in sorted(types):
        if types[name]["kind"] == "entity":
            build(name, ctx)
    entities = [e for e in ctx.built.values() if e and not e["merged"]]
    for entity in entities:
        add_discriminator(entity)
        for entry in entity["entries"]:
            if entry["kind"] in ("fk", "pkjoin"):
                resolve_fk(entry, ctx)
    findings = []
    for entity in entities:
        findings.extend(check(entity, ctx))
    findings.extend(definition_findings(ctx))
    findings.sort(key=lambda f: (LEVEL_ORDER.get(f.level, 9), f.table, f.column))
    return entities, findings


def main():
    args, flags, migrations = parse_args(sys.argv[1:])
    if not args:
        print(__doc__.strip().split("\n\n")[1].strip())
        return 2
    src = args[0]
    for path in (src, migrations):
        if path and not os.path.isdir(path):
            print("papka yo'q: %s" % path, file=sys.stderr)
            return 2

    entities, findings = analyse(src, migrations)
    if not entities:
        print("entity topilmadi: %s" % src, file=sys.stderr)
        return 1

    if "--json" in flags:
        json.dump({
            "entities": [{
                "class": e["class"], "table": e["table"], "file": e["file"],
                "subclasses": e["subclasses"],
                "columns": [{"name": c["name"], "type": sql_type(c),
                             "kind": c["kind"], "pk": bool(c.get("pk"))}
                            for c in columns_of(e)],
                "relations": [{"field": r["field"], "kind": r["kind"],
                               "java": r["java"], "table": r.get("join_table")}
                              for r in relations_of(e)],
            } for e in entities],
            "findings": [f.as_dict() for f in findings],
        }, sys.stdout, ensure_ascii=False, indent=1)
        print()
        return 0

    if "--only-findings" not in flags:
        print("# Sxema (%d entity, bazaga ulanmasdan)\n" % len(entities))
        for entity in sorted(entities, key=lambda e: e["table"]):
            extra = " (+ %s)" % ", ".join(entity["subclasses"]) if entity["subclasses"] else ""
            print("%s  <- %s%s" % (entity["table"], entity["file"], extra))
            for col in columns_of(entity):
                mark = "PK" if col.get("pk") else ("FK" if col["kind"] == "fk" else "  ")
                owner = "  [%s]" % col["owner"] if col.get("owner") else ""
                print("    %-2s %-26s %s%s" % (mark, col["name"], sql_type(col), owner))
            for rel in relations_of(entity):
                if rel["kind"] == "collection":
                    joined = "  (jadval: %s)" % rel["join_table"] if rel.get("join_table") else ""
                    print("    ..  %-26s %s%s" % (rel["field"], rel["java"], joined))
                elif rel["kind"] == "inverse":
                    print("    ..  %-26s %s (mappedBy)" % (rel["field"], rel["java"]))
            print()

    print("# Ehtimoliy muammolar (%d ta, hech narsa ishga tushirilmadi)\n"
          % len(findings))
    for f in findings:
        print("[%s] %s.%s" % (f.level, f.table, f.column))
        print("    %s" % f.message)
        print("    %s" % guide(f))
    return 0


if __name__ == "__main__":
    # `| head` quvurni yopsa traceback emas, jim chiqish (cost_report bilan bir xil).
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
