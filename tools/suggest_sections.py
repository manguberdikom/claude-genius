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

Hech narsa yetarlicha mos kelmasa, hook jim turadi: har so'rovga shovqin
qo'shish uni foydasiz qiladi.
"""

import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index")

MAX_SUGGESTIONS = 4
# Ikki shart birgalikda ishlaydi. MIN_SCORE umumiy moslikni, MIN_RARE_IDF
# esa mosliklardan kamida bittasi haqiqatan aniq atama ekanini talab
# qiladi. Qiymatlar tools/test_suggest.py dagi so'rovlarda sozlangan.
MIN_SCORE = 3.0
MIN_RARE_IDF = 2.9
# Yagona dalil bo'ladigan so'z shuncha belgidan qisqa bo'lmasin.
MIN_SPECIFIC_LEN = 5
ALIAS_WEIGHT = 1.2
ALIAS_BASE = 2.2
PAREN_SUFFIX_RE = __import__('re').compile(r'\s*\([^()]*\)\s*$')
# build_index.py dagi WORD_RE bilan bir xil bo'lishi shart.
TOKEN_RE = re.compile(r"[a-z0-9_.@#]+(?:\+\+|\+\d+)?(?:'[a-z0-9]+)*")


def tokens(text):
    out = (t.strip(".") for t in TOKEN_RE.findall(text.lower()))
    return [t for t in out if len(t) > 1 or not t.isalpha()]


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
    return idf


def score_sections(prompt, sections, idf):
    """Har bir bo'lim uchun ball va eng kamyob mos so'zning og'irligi.

    Ikkinchisi kerak, chunki yig'indining o'zi aldaydi: uchta umumiy so'z
    ("qilib", "va", "kerak") bitta aniq atama bilan teng ball to'playdi.
    Shuning uchun kamida bitta haqiqatan kamyob so'z talab qilinadi.

    Kamyoblikka faqat aniq so'z hisobga olinadi (is_specific). Chastota
    o'zi yetarli emas: `ber` kabi qisqa o'zbek fe'li ham kam bo'limda
    uchraydi va "tushuntirib ber" so'rovini "Qulashiga yo'l ber" bo'limiga
    ulab yuboradi.
    """
    wanted = set(tokens(prompt))
    if not wanted:
        return {}
    scores = {}
    for row in sections:
        if not row["section"]:
            continue
        shared = wanted & set(tokens(row["title"]))
        if not shared:
            continue
        total = sum(idf.get(t, 0.0) for t in shared)
        specific = [idf.get(t, 0.0) for t in shared if is_specific(t)]
        scores[(row["doc"], row["section"])] = [total, max(specific, default=0.0)]
    return scores


def is_specific(token):
    """Yagona dalil bo'la oladigan so'zmi.

    Texnik atama odatda uzun (`testcontainers`, `deadlock`) yoki harfdan
    boshqa belgi tutadi (`n+1`, `c++`, `@transactional`). Qisqa sof
    harfli so'z ko'pincha o'zbek yordamchi fe'li, shuning uchun u yolg'iz
    o'zi taklif uchun asos bo'lmaydi. Qisqa texnik atamalar (`jpa`, `gc`)
    taxalluslar jadvali orqali baribir topiladi.
    """
    return len(token) >= MIN_SPECIFIC_LEN or not token.isalpha()


def score_aliases(prompt, aliases, scores):
    """Taxallus so'rovda butun so'z bo'lib uchrasa, ballni oshiradi.

    Taxallus moslig'i o'z-o'zidan yetarli dalil, shuning uchun u kamyoblik
    shartini ham qondirilgan deb belgilaydi.
    """
    low = " " + " ".join(tokens(prompt)) + " "
    for row in aliases:
        if row["kind"] != "section":
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
        entry = scores.setdefault(key, [0.0, 0.0])
        entry[0] += ALIAS_WEIGHT * best + ALIAS_BASE
        entry[1] = max(entry[1], MIN_RARE_IDF)
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
    return {(r["doc"], r["section"]): r["title"] for r in sections if r["section"]}


def suggest(prompt):
    sections = read_tsv("sections.tsv")
    if not sections:
        return []
    idf = load_idf(len(sections))
    scores = score_sections(prompt, sections, idf)
    scores = score_aliases(prompt, read_tsv("aliases.tsv"), scores)

    keep = {k: v for k, v in scores.items()
            if v[0] >= MIN_SCORE and v[1] >= MIN_RARE_IDF}
    ranked = sorted(keep.items(), key=lambda kv: (-kv[1][0], kv[0]))
    titles = titles_by_key(sections)
    return [(doc, sec, titles.get((doc, sec), ""), total)
            for (doc, sec), (total, _) in ranked[:MAX_SUGGESTIONS]]


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return
    prompt = payload.get("prompt") or ""
    if not prompt.strip():
        return

    try:
        hits = suggest(prompt)
    except Exception:
        return  # hook hech qachon navbatni o'z xatosi tufayli buzmaydi
    if not hits:
        return

    lines = ["Shu so'rovga mos bo'limlar (indeksdan, avtomatik):"]
    for doc, section, title, _ in hits:
        lines.append("  %-11s %-7s %s" % (doc, section, title))
    lines.append("")
    lines.append("Matnini olish: tools/doc.sh show <hujjat> <raqam>")
    lines.append("Bular taklif, majburiyat emas. Mavzu boshqa bo'lsa, "
                 "tools/doc.sh find bilan qidiring.")

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n".join(lines),
            }
        },
        sys.stdout,
    )


if __name__ == "__main__":
    main()
