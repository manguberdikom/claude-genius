#!/usr/bin/env python3
"""UserPromptSubmit hook: so'rovga mos bo'limlarni avtomatik taklif qiladi.

Muammo: model `doc.sh find` ni chaqirishga majbur emas. Chaqirmasa,
repodagi 3293 bo'lim o'rniga o'z umumiy bilimidan javob beradi va bu jim
sodir bo'ladi - javob ishonchli ko'rinadi, lekin qoidaga tayanmaydi.

Yechim: bilimni tortib olinadigan emas, itariladigan qilish. Bu hook har
bir so'rovda ishlaydi va mos bo'lim raqamlarini kontekstga qo'shadi, ya'ni
model hech narsa chaqirmasa ham kerakli joy ko'rsatilgan bo'ladi.

Baholash ikki signaldan iborat:
  1. Inglizcha taxallus so'rov ichida butun so'z bo'lib uchrasa - kuchli
     signal, uzunroq taxallus aniqroq.
  2. Sarlavha so'zlarining mosligi, IDF bilan tortilgan: korpusda kamyob
     so'z ("bulkhead") ko'p uchraydiganidan ("kod") ancha ko'proq ma'no
     beradi. Stop-so'z ro'yxati shuning uchun kerak emas, chastota o'zi
     hal qiladi.

Sonar kaliti (java:S2259) bo'lsa, index/rules.tsv dagi bo'limlar boshida
turadi: kalit foydalanuvchi bera oladigan eng aniq signal.

Hech narsa yetarlicha mos kelmasa, hook jim turadi: har so'rovga shovqin
qo'shish uni foydasiz qiladi. Indeks yo'q yoki bobdan eski bo'lsa, doc.sh
dagi kabi avval qayta yasaladi.
"""

import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX = os.path.join(ROOT, "index")
# build_index va docref shu papkadan yuklanadi, skript qayerdan
# chaqirilmasin.
if HERE not in sys.path:
    sys.path.insert(0, HERE)

MAX_SUGGESTIONS = 4
# Ikki shart birgalikda ishlaydi. MIN_SCORE umumiy moslikni, MIN_RARE_IDF
# esa mosliklardan kamida bittasi haqiqatan aniq atama ekanini talab
# qiladi. Qiymatlar tools/test_suggest.py dagi so'rovlarda sozlangan.
MIN_SCORE = 3.0
MIN_RARE_IDF = 2.9
# Yagona dalil bo'ladigan so'z shuncha belgidan qisqa bo'lmasin.
MIN_SPECIFIC_LEN = 4
# Yolg'iz so'z yetarli emas, agar u atama lug'atida bo'lmasa.
MIN_EVIDENCE = 2
# O'zbekcha qo'shimchalar. Kesish faqat o'zak korpus lug'atida bo'lsa
# bajariladi, shuning uchun "tezlik" ga tegilmaydi, "funksiyani" esa
# "funksiya" ga keladi. Uzundan qisqaga qarab sinaladi.
SUFFIXES = ("larini", "lariga", "larida", "lardan", "ningiz", "larni", "larga",
            "larda", "lari", "ning", "dagi", "gacha", "siz", "dan", "lar",
            "ini", "iga", "ida", "ni", "ga", "da", "ta", "si", "i")
SYNONYMS_FILE = os.path.join(HERE, "synonyms.tsv")
# Dalil bo'lish uchun so'z shunchaki uzun emas, kamyob ham bo'lsin:
# `bilan` besh harfli, lekin 2480 bo'limda uchraydi.
EVIDENCE_MIN_IDF = 2.0
ALIAS_WEIGHT = 1.2
ALIAS_BASE = 2.2
PAREN_SUFFIX_RE = re.compile(r'\s*\([^()]*\)\s*$')
# build_index.py dagi WORD_RE bilan bir xil bo'lishi shart. tokens() esa
# ustiga `@` ni kesadi: "DataJpaTest" va "@DataJpaTest" bitta so'z.
TOKEN_RE = re.compile(r"[a-z0-9_.@#]+(?:\+\+|\+\d+)?(?:'[a-z0-9]+)*")

# GLOSSARY.md dagi atama, lekin "tech stack" ma'nosida shovqin beradi.
GLOSSARY_SKIP = {"stack"}
# Domen oti yolg'iz dalil emas: "customer null" mavzu emas, "Account
# Lockout" kabi ko'p so'zli taxallus esa score_aliases orqali topiladi.
DOMAIN_NOUNS = {"customer", "account", "notification"}

# Stack trace: frame va exception xabari mavzu emas, sinf nomlari shovqin.
FRAME = re.compile(r"^\s*at\s+[\w.$<>]+\(", re.M)
DROP = re.compile(r"^\s*(at\s+[\w.$<>]+\(|\.\.\.\s*\d+\s+more|(Detail|Hint|Where|Position):)")
HEAD = re.compile(r"^\s*(?:Caused by:\s*)?([\w.$]+(?:Exception|Error))\b:?.*$")
# Asbobning o'ziga buyruq ("memory ga yoz"), qo'llanma mavzusi emas.
META = re.compile(r"\bmemory\s*(?:ga|ni|dan|da|dagi)?\s+"
                  r"(?:yoz|saqla|tozala|o'qi|eslab|qo'sh)\w*", re.I)

# Sarlavhadagi texnik nom: backtick ichida identifikator, tashqarida
# CamelCase yoki kamida 4 harfli qisqartma. O'zbekcha mavhum ot hech
# qachon shunday yozilmaydi, shuning uchun u lug'atga kirmaydi.
BACKTICK_RE = re.compile(r"`([^`]+)`")
PROPER_RE = re.compile(r"\b(?:[A-Z][a-z0-9]*[A-Z][A-Za-z0-9]*|[A-Z]{4,}[0-9]*)\b")
CODEY_RE = re.compile(r"[a-z][A-Z]|[_.@#0-9]")

RULE_RE = re.compile(r"\b(?:java|squid):s(\d+)\b", re.I)
# Bitta kalit uchun shuncha bo'lim, qolgani `doc.sh rule` da.
RULE_PER_KEY = 2
# Indeks yasash shundan uzoq cho'zilsa, bor indeks bilan davom etiladi.
REBUILD_TIMEOUT = 8


def tokens(text):
    out = (t.strip(".").lstrip("@") for t in TOKEN_RE.findall(text.lower()))
    return [t for t in out if len(t) > 1 or (t and not t.isalpha())]


def read_tsv(name):
    path = os.path.join(INDEX, name)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        header = handle.readline().rstrip("\n").split("\t")
        out = []
        for line in handle:
            parts = line.rstrip("\n").split("\t")
            if len(parts) == len(header):
                out.append(dict(zip(header, parts)))
        return out


def ensure_fresh():
    """Indeks yo'q yoki biror bobdan eski bo'lsa qayta yasaladi.

    Indeks hosila va git ga kirmaydi. Usiz hook jim turardi, eskirganida
    esa yo'q bo'lim raqamini berardi va model aynan shuni `show` qilardi.
    Yangilik mezoni docref bilan bitta (build_index.is_fresh), bash siz
    ham ishlashi uchun build_index.py to'g'ridan chaqiriladi.
    """
    try:
        import build_index
        if build_index.is_fresh():
            return
    except Exception:
        return  # yasovchi yuklanmasa, yasash ham yiqilardi
    try:
        subprocess.run([sys.executable, os.path.join(HERE, "build_index.py")],
                       stdin=subprocess.DEVNULL, capture_output=True,
                       timeout=REBUILD_TIMEOUT, check=False)
    except (OSError, subprocess.SubprocessError):
        pass  # bor indeks bilan davom etiladi


def load_synonyms():
    """So'rov so'zi -> korpusda turgan so'zlar."""
    table = {}
    if not os.path.exists(SYNONYMS_FILE):
        return table
    with open(SYNONYMS_FILE, encoding="utf-8") as handle:
        handle.readline()
        for line in handle:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) == 2 and parts[0] and parts[1]:
                table[parts[0]] = parts[1].split()
    return table


def clean_prompt(prompt):
    """So'rovdan mavzu bo'lmagan qismlarni olib tashlaydi.

    Stack trace da frame qatorlari paket va sinf nomlariga to'la, ular
    sarlavha so'zlariga tasodifan mos keladi. Frame bor bo'lsa, ular va
    `... 42 more`, `Detail:` qatorlari tashlanadi, exception qatoridan esa
    faqat sinf nomi qoladi. Bir qatorlik "XxxException chiqyapti" ga
    tegilmaydi: unda nom mavzuning o'zi.
    """
    if FRAME.search(prompt):
        kept = []
        for line in prompt.splitlines():
            if DROP.match(line):
                continue
            head = HEAD.match(line)
            kept.append(head.group(1).rsplit(".", 1)[-1] if head else line)
        prompt = "\n".join(kept)
    return META.sub(" ", prompt)


def roots(token, vocab):
    """So'zning o'zi va qo'shimchasi kesilgan shakli.

    Qo'shimcha kesish ALMASHTIRISH emas, QO'SHISH: "keshni" ning o'zi ham
    biror sarlavhada uchraydi, shuning uchun uni tashlab yuborib bo'lmaydi,
    lekin "kesh" ni ham qo'shish kerak. Kesish faqat o'zak korpus lug'atida
    bo'lsa bajariladi: shartsiz kesish "tezlik" ni "tez" ga aylantirib,
    mavjud bo'lmagan so'z yasaydi.
    """
    out = {token}
    for suffix in SUFFIXES:
        if len(token) - len(suffix) >= 4 and token.endswith(suffix):
            root = token[: -len(suffix)]
            if root in vocab:
                out.add(root)
                break
    return out


def expand(prompt, vocab, synonyms):
    """So'rov so'zlari: o'zagi va sinonimlari bilan birga."""
    out = set()
    for token in tokens(prompt):
        forms = roots(token, vocab)
        out |= forms
        for form in forms:
            out.update(synonyms.get(form, ()))
    return out


def load_idf(total_sections):
    """So'z og'irligi, bo'lim TANASIDAGI chastotadan (index/df.tsv).

    Sarlavhalar qisqa, shuning uchun ular bo'yicha hisoblangan IDF `yaxshi`
    bilan `deadlock` ni teng kamyob deb ko'rsatadi. Tana bo'yicha sanalganda
    farq ochiladi: yaxshi 362 bo'limda, deadlock 40 tasida.
    """
    total = max(total_sections, 1)
    idf = {}
    for row in read_tsv("df.tsv"):
        count = int(row["sections"]) or 1
        idf[row["token"]] = math.log(total / count)
    # df.tsv `@` ni saqlaydi, tokens() esa kesadi.
    for token in [t for t in idf if t.startswith("@")]:
        idf.setdefault(token.lstrip("@"), idf[token])
    return idf


def score_sections(wanted, sections, idf, term_vocab, direct=frozenset()):
    """Har bir bo'lim uchun uchta son: ball, kamyoblik, dalil kuchi.

    Uchinchisi kerak bo'lib qoldi, chunki chastota atamani mavhum so'zdan
    ajrata olmaydi: bu korpusda `aniqlik` ning IDF si 5.1, `deadlock` niki
    4.4, `coverage` niki esa atigi 2.7. Chegarani ko'tarish mavhum so'zdan
    oldin haqiqiy atamalarni o'ldiradi.

    Shuning uchun yolg'iz so'zga ishonilmaydi. Bitta mos so'z faqat u
    atamalar lug'atida bo'lsa (ya'ni biror inglizcha texnik nomning qismi)
    dalil hisoblanadi. Aks holda kamida ikkita aniq so'z mos kelishi
    kerak: "tezlik" yolg'iz o'zi hech narsani ko'rsatmaydi, "funksiya
    nomi" esa ko'rsatadi. Sinonim orqali kelgan atama yolg'iz o'zi dalil
    bo'lmaydi, u faqat boshqa dalilni kuchaytiradi: `direct` so'rovda
    to'g'ridan yozilgan shakllar (o'zagi bilan).
    """
    if not wanted:
        return {}
    scores = {}
    for row in sections:
        if not row["section"]:
            continue
        shared = wanted & set(tokens(row["title"]))
        if not shared:
            continue
        specific = [t for t in shared if is_specific(t)]
        carrying = [t for t in specific if idf.get(t, 0.0) >= EVIDENCE_MIN_IDF]
        evidence = len(carrying)
        if evidence == 1 and carrying[0] in term_vocab and carrying[0] in direct:
            evidence = 2
        scores[(row["doc"], row["section"])] = [
            sum(idf.get(t, 0.0) for t in shared),
            max((idf.get(t, 0.0) for t in specific), default=0.0),
            evidence,
        ]
    return scores


def glossary_terms():
    """GLOSSARY.md dagi 'Inglizcha qoladigan atamalar' ning bir so'zlilari.

    Ko'p so'zli atama olinmaydi: `code smell` dan `code`, `quality gate`
    dan `gate` yolg'iz dalilga aylanib qolardi. Ular taxallus orqali
    allaqachon topiladi.
    """
    try:
        with open(os.path.join(ROOT, "GLOSSARY.md"), encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return set()
    head = "## Inglizcha qoladigan atamalar"
    if head not in text:
        return set()
    block = text.split(head, 1)[1].split("\n## ", 1)[0]
    return {t for term in BACKTICK_RE.findall(block) if " " not in term
            for t in tokens(term) if is_specific(t) and t not in GLOSSARY_SKIP}


def term_vocabulary(aliases):
    """Korpusning atama lug'ati: taxalluslar va GLOSSARY.md dagi
    'Inglizcha qoladigan atamalar' ro'yxatining bir so'zli atamalari.

    `testcontainers`, `coverage` taxalluslarda, `deadlock`, `heap`,
    `latency` lug'atda bor, chunki ular inglizcha texnik nom. `tezlik`,
    `aniqlik`, `qoida` yo'q, chunki ular mavhum ot.
    """
    vocab = set()
    for row in aliases:
        for token in tokens(row["alias"]):
            if is_specific(token):
                vocab.add(token)
    return vocab | glossary_terms()


def title_terms(sections):
    """Sarlavhadagi texnik nomlar: `StampedLock`, OSIV, PECS, SonarLint.

    Ular taxallus jadvalida yo'q, shuning uchun bitta shunday nomli so'rov
    jim qolardi. Uch harfli qisqartma (JVM, DTO, ZGC) olinmaydi: "JVM nima"
    kabi umumiy savol ham taklif olib qolardi.
    """
    vocab = set()
    for row in sections:
        title = row["title"]
        found = [m for m in BACKTICK_RE.findall(title) if CODEY_RE.search(m)]
        found += PROPER_RE.findall(BACKTICK_RE.sub(" ", title))
        for name in found:
            vocab.update(t for t in tokens(name) if is_specific(t))
    return vocab


def is_specific(token):
    """Dalil sifatida sanaladigan so'zmi.

    Qisqa sof harfli so'z ko'pincha o'zbek yordamchi fe'li ("ber", "qil"),
    shuning uchun u sanalmaydi. Qisqa texnik atamalar (`jpa`, `gc`)
    taxalluslar jadvali orqali baribir topiladi. Sof raqam ham shunday:
    '90', '7' qator raqami, son yoki foiz bo'lib keladi, uzun raqam esa
    (RFC 9457) atama bo'lib qoladi.
    """
    if token.isdigit():
        return len(token) >= MIN_SPECIFIC_LEN
    return len(token) >= MIN_SPECIFIC_LEN or not token.isalpha()


def score_aliases(prompt, aliases, scores):
    """Taxallus so'rovda butun so'z bo'lib uchrasa, ballni oshiradi.

    Taxallus moslig'i o'z-o'zidan yetarli dalil, shuning uchun u kamyoblik
    shartini ham qondirilgan deb belgilaydi. Bob taxallusi bob raqamini
    beradi; bir so'zlisi ("Injection", "Configuration") olinmaydi, u boshqa
    ma'nodagi so'rovni egallab olardi.
    """
    low = " " + " ".join(tokens(prompt)) + " "
    for row in aliases:
        kind = row["kind"]
        if kind not in ("section", "chapter"):
            continue
        if kind == "chapter" and len(tokens(row["alias"])) < 2:
            continue
        best = 0
        for form in alias_forms(row["alias"]):
            needle = " " + " ".join(tokens(form)) + " "
            if len(needle.strip()) >= 4 and needle in low:
                best = max(best, len(needle.split()))
        if not best:
            continue
        key = (row["doc"], row["ref"])
        # Uzun taxallus aniqroq: "circuit breaker" > "retry".
        entry = scores.setdefault(key, [0.0, 0.0, 0])
        entry[0] += ALIAS_WEIGHT * best + ALIAS_BASE
        entry[1] = max(entry[1], MIN_RARE_IDF)
        entry[2] = max(entry[2], MIN_EVIDENCE)
    return scores


def alias_forms(alias):
    """Taxallusning izlanadigan shakllari.

    Jadvalda nom bezak bilan saqlanadi: "Saga (choreography)". Foydalanuvchi
    esa "saga" deb yozadi, shuning uchun qavsdagi qism olib tashlangan
    varianti ham tekshiriladi.
    """
    forms = [alias]
    core = PAREN_SUFFIX_RE.sub("", alias).strip()
    if core and core != alias:
        forms.append(core)
    return forms


def titles_by_key(sections):
    """(hujjat, raqam) -> sarlavha; bob taxallusi uchun bob raqami ham."""
    out = {(r["doc"], r["chapter"]): r["title"] for r in read_tsv("chapters.tsv")}
    out.update({(r["doc"], r["section"]): r["title"] for r in sections if r["section"]})
    return out


def rule_keys(prompt):
    """So'rovdagi Sonar kalitlari, rules.tsv dagi shaklda: java:S2259."""
    return sorted({"java:S" + digits for digits in RULE_RE.findall(prompt)})


def rule_hits(keys, titles):
    """Kalit izohlangan bo'limlar; rules.tsv kalit ichida ulush bo'yicha saralangan."""
    if not keys:
        return []
    out, seen = [], {}
    for row in read_tsv("rules.tsv"):
        rule = row["rule"]
        if rule in keys and row["section"] and seen.get(rule, 0) < RULE_PER_KEY:
            seen[rule] = seen.get(rule, 0) + 1
            out.append((row["doc"], row["section"],
                        titles.get((row["doc"], row["section"]), ""), 0.0))
    return out


def suggest(prompt):
    sections = read_tsv("sections.tsv")
    if not sections:
        return []
    prompt = clean_prompt(prompt)
    idf = load_idf(len(sections))
    aliases = read_tsv("aliases.tsv")
    term_vocab = (term_vocabulary(aliases) | title_terms(sections)) - DOMAIN_NOUNS
    wanted = expand(prompt, idf, load_synonyms())
    direct = set().union(*(roots(t, idf) for t in tokens(prompt)))
    scores = score_sections(wanted, sections, idf, term_vocab, direct)
    scores = score_aliases(prompt, aliases, scores)

    keep = {k: v for k, v in scores.items()
            if v[0] >= MIN_SCORE and v[1] >= MIN_RARE_IDF and v[2] >= MIN_EVIDENCE}
    ranked = sorted(keep.items(), key=lambda kv: (-kv[1][0], kv[0]))
    titles = titles_by_key(sections)
    hits = rule_hits(rule_keys(prompt), titles)
    have = {(h[0], h[1]) for h in hits}
    hits += [(doc, sec, titles.get((doc, sec), ""), total)
             for (doc, sec), (total, _, _) in ranked if (doc, sec) not in have]
    return hits[:MAX_SUGGESTIONS]


def doc_cmd():
    """`doc.sh` buyrug'i: klon ichida nisbiy (matn va narx o'zgarmaydi),
    boshqa proyektda mutlaq, aks holda u yerda "No such file" beradi.
    docref yuklanmasa, taklifni yo'qotgandan nisbiy buyruq afzal.
    """
    try:
        from docref import tool_cmd
    except (ImportError, SyntaxError):
        return "tools/doc.sh"
    return tool_cmd("doc.sh")


def render(hits, rules=(), cmd="tools/doc.sh"):
    """Hook matni. Sarlavha raqam bilan boshlanadi, raqam qayta yozilmaydi."""
    lines = ["Mos bo'limlar (%s show <hujjat> <raqam>):" % cmd]
    for doc, section, title, _ in hits:
        head = title.split(" ", 1)[0].rstrip(".")
        label = title if head == section else ("%s %s" % (section, title)).strip()
        lines.append("  %-11s %s" % (doc, label))
    for key in rules:
        lines.append("To'liq ro'yxat: %s rule %s" % (cmd, key))
    return "\n".join(lines)


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    prompt = (payload.get("prompt") if isinstance(payload, dict) else None) or ""
    if not isinstance(prompt, str) or not prompt.strip():
        return

    try:
        ensure_fresh()
        hits = suggest(prompt)
        rules = rule_keys(prompt)
        if rules:
            known = {row["rule"] for row in read_tsv("rules.tsv")}
            rules = [key for key in rules if key in known]
        text = render(hits, rules, doc_cmd()) if hits else ""
    except Exception:
        return  # hook hech qachon navbatni o'z xatosi tufayli buzmaydi
    if not hits:
        return

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": text,
            }
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
