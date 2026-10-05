#!/usr/bin/env python3
"""schema_from_entities.py uchun sinovlar.

    python3 tools/test_schema.py

tools/testdata/entities/ dagi ikkita entity ataylab qarama-qarshi yozilgan:
Order.java da tipik xatolar bor, Customer.java esa toza. Shunda ikkala
yo'nalish ham sinaladi: muammoni ko'rish va toza kodni tinch qo'yish.

Qolgan papkalar avvalgi regex parserni sindirgan real idiomalar:
entities_inherit (meros, @EmbeddedId, package-private maydon),
entities_nested (ichma-ich annotatsiya, Javadoc, static va transient),
entities_types (izohsiz enum, UUID FK, @Embedded, mappedBy, unique) va
entities_migration (indeks migratsiyada yozilgan loyiha).
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "schema_from_entities.py")
DATA = os.path.join(HERE, "testdata")
SECTIONS = os.path.join(ROOT, "index", "sections.tsv")

ENT = "entities"
INH = "entities_inherit"
NEST = "entities_nested"
TYPES = "entities_types"
MIG = os.path.join("entities_migration", "src", "main", "java")
MIG_SQL = os.path.join(DATA, "entities_migration", "src", "main", "resources",
                       "db", "migration")
DIRS = [ENT, INH, NEST, TYPES, MIG]

# (papka, nom, matn): sxema matnida bo'lishi shart.
SCHEMA_EXPECT = [
    (ENT, "@ManyToOne -> _id ustuni", "customer_id"),
    (ENT, "length -> varchar(n)", "varchar(32)"),
    (ENT, "Instant -> timestamptz", "timestamptz"),
    (ENT, "ORDINAL enum -> integer", "integer"),
    (ENT, "STRING enum -> varchar", "varchar(20)"),
    (NEST, "@ManyToMany -> @JoinTable nomi", "jadval: purchase_order_supplier"),
    (NEST, "@ElementCollection -> @CollectionTable", "jadval: po_tag"),
]

# (papka, fayl, jadval): jadval nomi qayerdan olinishi.
TABLES = [
    (ENT, "Order.java", "orders"),                  # @Table dan
    (NEST, "PurchaseOrder.java", "purchase_order"), # name indexes dan keyin emas
    (NEST, "Supplier.java", "supplier"),            # Javadoc dagi "class" emas
    (INH, "Animal.java", "animals"),
]
NO_TABLES = [
    (INH, "dog"),               # SINGLE_TABLE voris ota jadvalda
    (NEST, "for"),
    (NEST, "without"),
    (NEST, "idx_po_customer"),
]

# (papka, jadval, ustun, tur yoki None): JSON ustunlarida bo'lishi shart.
COLUMNS = [
    (ENT, "orders", "total_amount", None),          # nom berilmasa snake_case
    (ENT, "customers", "registered_at", None),      # ikkinchi entity
    (INH, "products", "id", "uuid"),                # @MappedSuperclass dan
    (INH, "products", "version", "bigint"),
    (INH, "products", "created_at", "timestamptz"),
    (INH, "products", "title", "varchar(120)"),
    (INH, "car", "id", "bigint"),                   # JOINED: PK/FK ustuni
    (INH, "car", "seats", "integer"),
    (INH, "animals", "breed", "varchar(60)"),
    (INH, "animals", "dtype", "varchar(31)"),
    (INH, "order_lines", "order_id", "uuid"),       # @EmbeddedId yoyildi
    (INH, "order_lines", "line_no", "integer"),
    (INH, "order_lines", "product_id", "uuid"),     # FK turi nishon @Id dan
    (INH, "invoice", "id", "bigint"),               # package-private maydon
    (INH, "invoice", "title", "varchar(255)"),
    (INH, "vehicle", "fuel", "varchar(10)"),
    (NEST, "purchase_order", "id", "bigint"),
    (NEST, "purchase_order", "amt", "numeric(19,2)"),
    (NEST, "purchase_order", "homepage", "varchar(200)"),
    (NEST, "purchase_order", "externalid", "varchar(64)"),
    (NEST, "purchase_order", "customer_id", "bigint?"),
    (NEST, "purchase_order", "supplier_id", "uuid"),
    (NEST, "supplier", "id", "uuid"),
    (TYPES, "shipment", "status", "integer"),
    (TYPES, "shipment", "parcel_id", "uuid"),
    (TYPES, "shipment", "owner_id", "uuid"),
    (TYPES, "shipment", "wh_street", "varchar(120)"),
    (TYPES, "shipment", "wh_city", "varchar(60)"),
    (TYPES, "shipment", "street", "varchar(80)"),
    (TYPES, "shipment", "city", "varchar(255)"),
    (TYPES, "shipment", "created_at", "timestamp"),
    (TYPES, "shipment", "total", "numeric"),
    (TYPES, "shipment", "payload", "jsonb"),
    (TYPES, "label", "shipment_id", "bigint"),
]
NO_COLUMNS = [
    (INH, "vehicle", "code"),                  # ichki enum maydoni
    (INH, "order_lines", "id"),
    (INH, "order_lines", "purchase_id"),       # @MapsId ikkinchi ustun bermaydi
    (NEST, "purchase_order", "po_seq"),        # @SequenceGenerator nomi
    (NEST, "purchase_order", "serial_versionuid"),
    (NEST, "purchase_order", "serial_version_u_i_d"),
    (NEST, "purchase_order", "cache"),         # transient
    (NEST, "purchase_order", "ghost"),         # metod ichidagi satr
    (NEST, "purchase_order", "suppliers"),
    (NEST, "purchase_order", "tags"),
    (NEST, "purchase_order", "tag"),
    (NEST, "purchase_order", "external_i_d"),
    (TYPES, "shipment", "warehouse"),
    (TYPES, "shipment", "origin"),
    (TYPES, "shipment", "label_id"),           # mappedBy: ustun yo'q
]
PRIMARY = [
    (INH, "order_lines", "order_id"),
    (INH, "order_lines", "line_no"),
    (INH, "car", "id"),
    (INH, "products", "id"),
    (NEST, "purchase_order", "id"),
]

# (papka, jadval, ustun, matn bo'lagi): topilmalar ichida bo'lishi shart.
FINDING_EXPECT = [
    (ENT, "orders", "customer_id", "default EAGER"),
    (ENT, "orders", "customer_id", "indeks"),
    (ENT, "orders", "lines", "EAGER yuklanadi"),
    (ENT, "orders", "lines", "mappedBy"),
    (ENT, "orders", "status", "ORDINAL"),
    (ENT, "orders", "total_amount", "precision"),
    (ENT, "orders", "note", "varchar(255)"),
    (ENT, "orders", "-", "@Version yo'q"),
    (ENT, "customers", "registered_at", "Eski sana"),
    (INH, "invoice", "title", "varchar(255)"),
    (INH, "invoice", "amount", "precision"),
    (INH, "legacy", "-", "manbada yo'q"),
    (INH, "order_lines", "order_id", "kompozit PK"),
    (NEST, "purchase_order", "supplier_id", "indeks"),   # kompozitning 2-ustuni
    (TYPES, "shipment", "status", "ORDINAL"),            # @Enumerated yo'q
    (TYPES, "shipment", "total", "precision"),           # java.math.BigDecimal
    (TYPES, "shipment", "label", "default EAGER"),       # teskari @OneToOne
    (TYPES, "Address", "city", "varchar(255)"),          # @Embeddable bir marta
    (MIG, "delivery", "courier_id", "migratsiyada"),
]

# Toza yoki tuzatilgan holat uchun bular CHIQMASLIGI kerak.
FINDING_ABSENT = [
    (ENT, "customers", "email", "indeks"),
    (ENT, "customers", "tier", "ORDINAL"),
    (ENT, "customers", "-", "@Version yo'q"),
    (ENT, "customers", "orders", "EAGER"),
    (INH, "products", "-", "@Id topilmadi"),
    (INH, "products", "-", "@Version yo'q"),
    (INH, "purchases", "-", "@Id topilmadi"),
    (INH, "car", "-", "@Id topilmadi"),
    (INH, "car", "-", "@Version yo'q"),
    (INH, "invoice", "-", "@Id topilmadi"),
    (INH, "invoice", "-", "@Version yo'q"),
    (INH, "order_lines", "-", "@Id topilmadi"),
    (INH, "order_lines", "product_id", "indeks"),
    (INH, "legacy", "-", "@Id topilmadi"),
    (INH, "legacy", "-", "@Version yo'q"),
    (NEST, "purchase_order", "customer_id", "indeks"),
    (NEST, "purchase_order", "created_by", "indeks"),
    (NEST, "purchase_order", "amt", "precision"),
    (NEST, "purchase_order", "homepage", "varchar(255)"),
    (NEST, "purchase_order", "-", "@Id topilmadi"),
    (TYPES, "shipment", "legacy_status", "ORDINAL"),     # @Convert
    (TYPES, "shipment", "parcel_id", "indeks"),          # unique = true
    (TYPES, "shipment", "owner_id", "indeks"),           # @Index(... DESC)
    (TYPES, "shipment", "label", "indeks"),
    (TYPES, "label", "shipment_id", "indeks"),
    (TYPES, "shipment", "payload", "varchar(255)"),      # columnDefinition
    (TYPES, "shipment", "city", "varchar(255)"),
    (MIG, "delivery", "depot_id", "indeks"),             # CREATE INDEX
    (MIG, "delivery", "backup_id", "indeks"),            # UNIQUE (backup_id, id)
    (MIG, "delivery", "courier_id", "e'lon qilinmagan"),  # yuqori emas, o'rta
]

# Topilma matni -> qo'llanma bo'limi sarlavhasida bo'lishi kerak so'z.
# Alias bo'yicha "Index" Index Table ga, "Enum" Enum Singleton ga ketardi.
REF_KEYWORDS = [
    ("Tashqi kalit", "Tashqi kalit"),
    ("ORDINAL", "enum"),
    ("varchar(255)", "varchar"),
    ("Eski sana", "Date"),
]


def execute(folder, *args):
    return subprocess.run([sys.executable, TOOL, os.path.join(DATA, folder)]
                          + list(args), capture_output=True, text=True, cwd=ROOT)


def run(folder, *args):
    return execute(folder, *args).stdout


def mark(ok):
    return "OK" if ok else "XATO"


def section_titles():
    """Indeks bor bo'lsa {"<hujjat> <raqam>": sarlavha}. Sinov uni
    yasamaydi: yo'q bo'lsa havola tekshiruvi o'tkazib yuboriladi."""
    if not os.path.exists(SECTIONS):
        return None
    titles = {}
    with open(SECTIONS, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) > 3:
                titles["%s %s" % (parts[0], parts[1])] = parts[3]
    return titles


def pipe_closed_quietly():
    """`| head` quvurni yopsa traceback chiqmasligi kerak. O'qish uchi
    asbob yozishni boshlashidan oldin yopiladi, shuning uchun natija
    tasodifga bog'liq emas."""
    read_end, write_end = os.pipe()
    env = dict(os.environ, PYTHONUNBUFFERED="1")
    proc = subprocess.Popen([sys.executable, TOOL, os.path.join(DATA, ENT), "--json"],
                            stdout=write_end, stderr=subprocess.PIPE,
                            text=True, cwd=ROOT, env=env)
    os.close(write_end)
    os.close(read_end)
    _, err = proc.communicate(timeout=60)
    return "Traceback" not in err and "BrokenPipeError" not in err


def main():
    missing = [d for d in DIRS if not os.path.isdir(os.path.join(DATA, d))]
    if missing:
        print("sinov ma'lumoti yo'q: %s" % ", ".join(missing))
        return 1

    failures = total = 0

    def report(ok, text):
        nonlocal failures, total
        total += 1
        failures += not ok
        print("%-4s %s" % (mark(ok), text))

    procs = {d: execute(d) for d in DIRS}
    texts = {d: p.stdout for d, p in procs.items()}
    payloads = {d: json.loads(run(d, "--json")) for d in DIRS}
    found = {d: [(f["table"], f["column"], f["message"]) for f in p["findings"]]
             for d, p in payloads.items()}
    columns = {d: {(e["table"], c["name"]): c for e in p["entities"]
                   for c in e["columns"]} for d, p in payloads.items()}
    tables = {d: {e["file"]: e["table"] for e in p["entities"]}
              for d, p in payloads.items()}

    print("== Matn rejimi xatosiz tugaydi ==")
    for folder, proc in procs.items():
        report(proc.returncode == 0 and not proc.stderr,
               "%s (kod %d) %s" % (folder, proc.returncode, proc.stderr.strip()[-200:]))

    print("\n== Sxema matni ==")
    for folder, label, needle in SCHEMA_EXPECT:
        report(needle in texts[folder], "%-38s %s" % (label, needle))

    print("\n== Jadval nomi ==")
    for folder, path, table in TABLES:
        report(tables[folder].get(path) == table, "%s -> %s" % (path, table))
    for folder, table in NO_TABLES:
        report(table not in tables[folder].values(), "%s jadvali yo'q" % table)

    print("\n== Ustunlar ==")
    for folder, table, name, sql in COLUMNS:
        col = columns[folder].get((table, name))
        ok = col is not None and (sql is None or col["type"] == sql)
        got = col["type"] if col else "-"
        report(ok, "%s.%s %s (olingan: %s)" % (table, name, sql or "", got))
    for folder, table, name in NO_COLUMNS:
        report((table, name) not in columns[folder], "%s.%s yo'q" % (table, name))
    for folder, table, name in PRIMARY:
        col = columns[folder].get((table, name))
        report(bool(col and col.get("pk")), "%s.%s PK" % (table, name))

    print("\n== Topilishi kerak ==")
    for folder, table, column, needle in FINDING_EXPECT:
        ok = any(t == table and c == column and needle in m
                 for t, c, m in found[folder])
        report(ok, "%s.%s  %s" % (table, column, needle))

    print("\n== Chiqmasligi kerak ==")
    for folder, table, column, needle in FINDING_ABSENT:
        ok = not any(t == table and c == column and needle in m
                     for t, c, m in found[folder])
        report(ok, "%s.%s  %s" % (table, column, needle))

    print("\n== Takrorlanish yo'q ==")
    for folder in DIRS:
        items = found[folder]
        report(len(items) == len(set(items)),
               "%s: %d ta topilma, %d tasi noyob" % (folder, len(items), len(set(items))))

    print("\n== --migrations bayrog'i ==")
    out = run(ENT, "--json", "--migrations", MIG_SQL)
    flagged = [f for f in json.loads(out)["findings"]
               if f["column"] == "customer_id" and "indeks" in f["message"]]
    report(len(flagged) == 1 and flagged[0]["level"] == "o'rta",
           "migratsiya bor, indeks yo'q -> o'rta")

    print("\n== Qo'llanma havolasi ==")
    titles = section_titles()
    if titles is None:
        print("SKIP index/sections.tsv yo'q")
    else:
        everything = [f for p in payloads.values() for f in p["findings"]]
        for part, keyword in REF_KEYWORDS:
            hits = [f for f in everything if part in f["message"]]
            bad = [f.get("ref", "") for f in hits
                   if keyword.lower() not in titles.get(f.get("ref", ""), "").lower()]
            report(bool(hits) and not bad,
                   "%s -> sarlavhada \"%s\" %s" % (part, keyword, bad or ""))

    print("\n== Quvur yopilsa ==")
    report(pipe_closed_quietly(), "BrokenPipeError traceback yo'q")

    print("\n%d/%d o'tdi" % (total - failures, total))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
