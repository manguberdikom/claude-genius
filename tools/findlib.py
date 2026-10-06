#!/usr/bin/env python3
"""doc.sh find ning ko'p so'zli zaxira yo'li.

    python3 tools/findlib.py <so'rov>

doc.sh find butun so'rovni ibora sifatida qidiradi. "optimistic locking"
yoki "transaction propagation" kabi so'rovda ibora hech bir sarlavhada
aynan uchramaydi va natija bo'sh chiqadi, model esa "topilmadi" deb o'z
bilimidan javob beradi. Shuning uchun natija bo'sh va so'rovda kamida
ikki so'z bo'lsa, doc.sh shu skriptni chaqiradi: so'rov so'zlarga
bo'linadi va har so'z alohida qidiriladi.

Leksik qism suggest_sections dan olinadi (tokens, roots, sinonimlar):
ikki dvigatel bir-biridan uzoqlashmasin. Ustiga uchta qo'shimcha:

  - transliteratsiya: optimistic -> optimistik, propagation ->
    propagatsiya (doc.sh dagi qoida bilan bir xil);
  - synonyms.tsv dagi inglizcha-o'zbekcha blok: transaction -> tranzaksiya;
  - so'z boshi bo'yicha moslik: locking -> lock, testlar -> test.

Saralash: avval hamma so'zi topilgan yozuvlar (AND). Bunday yozuv yo'q
bo'lsa, eng ko'p so'zi topilganlar. Ichida IDF yig'indisi bo'yicha: kamyob
so'z ko'p uchraydiganidan og'irroq. Sarlavhada topilgan so'z to'liq, faqat
bob sarlavhasida topilgani yarim og'irlik oladi. Chiqish doc.sh find
qatori bilan bir xil: hujjat, raqam, sarlavha (tab bilan).
"""

import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import suggest_sections as S  # noqa: E402

# Prefiks moslik shundan qisqa so'zda qilinmaydi: "pin" "pinning" ga,
# "log" "login" ga yopishib qolardi.
MIN_PREFIX = 4
CHAPTER_WEIGHT = 0.5
ASCII_WORD = re.compile(r"^[a-z]+$")
BLOCK_START = "# [inglizcha]"
BLOCK_END = "# [/inglizcha]"


def translit(word):
    """Inglizcha atamaning o'zbekcha yozilishi (doc.sh name_hits bilan bir xil).

    Faqat sof harfli so'zga. Natija so'zning o'zi bo'lsa, None.
    """
    if not ASCII_WORD.match(word):
        return None
    out = word.replace("ction", "ksiya").replace("tion", "tsiya").replace("sion", "siya")
    if out.endswith("ic"):
        out = out[:-2] + "ik"
    out = out.replace("c", "k")
    return out if out != word else None


def english_table(path=S.SYNONYMS_FILE):
    """synonyms.tsv dagi [inglizcha] bloki: so'z -> o'zbekcha yozilishlari."""
    table, inside = {}, False
    try:
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                line = line.rstrip("\n")
                if line.startswith(BLOCK_START):
                    inside = True
                elif line.startswith(BLOCK_END):
                    inside = False
                elif inside and line and not line.startswith("#"):
                    parts = line.split("\t")
                    if len(parts) == 2:
                        table[parts[0]] = parts[1].split()
    except OSError:
        pass
    return table


def word_forms(word, vocab, synonyms, table):
    """So'zning qidiriladigan shakllari: o'zagi, sinonimi, o'zbekcha yozilishi."""
    forms = set(S.roots(word, vocab))
    for form in list(forms):
        forms.update(synonyms.get(form, ()))
    variant = translit(word)
    if variant:
        forms.add(variant)
    forms.update(table.get(word, ()))
    return forms


def matches(forms, title_tokens):
    """Shakllardan biri sarlavha so'ziga teng yoki so'z boshi sifatida mos."""
    for form in forms:
        if form in title_tokens:
            return form
        if len(form) >= MIN_PREFIX:
            for token in title_tokens:
                if len(token) >= MIN_PREFIX and (
                        token.startswith(form) or form.startswith(token)):
                    return token
    return None


def word_weight(word, forms, idf, top_idf):
    """So'zning IDF si; korpusda yo'q bo'lsa shakllaridan eng kamyobi."""
    if word in idf:
        return idf[word]
    known = [idf[f] for f in forms if f in idf]
    return max(known) if known else top_idf


def entries():
    """(hujjat, raqam, sarlavha, sarlavha so'zlari, bob so'zlari) ro'yxati.

    Bo'lim sarlavhasiga uning taxalluslari qo'shiladi, bob sarlavhasi esa
    ikkinchi darajali kontekst: "transaction propagation" da
    "tranzaksiya" 19-bob nomida, "propagation" 19.2 sarlavhasida.
    """
    chapters = {(r["doc"], r["chapter"]): r["title"] for r in S.read_tsv("chapters.tsv")}
    aliases = {}
    for row in S.read_tsv("aliases.tsv"):
        if row["kind"] == "section":
            aliases.setdefault((row["doc"], row["ref"]), []).append(row["alias"])
    out = []
    for row in S.read_tsv("sections.tsv"):
        if not row["section"]:
            continue
        key = (row["doc"], row["section"])
        text = " ".join([row["title"]] + aliases.get(key, []))
        title = row["title"]
        if row.get("ishora"):
            title += " [ishora: %s]" % row["ishora"]
        chapter = chapters.get((row["doc"], row["chapter"]), "")
        out.append((row["doc"], row["section"], title,
                    set(S.tokens(text)), set(S.tokens(chapter))))
    for (doc, number), title in chapters.items():
        out.append((doc, number, title, set(S.tokens(title)), set()))
    return out


def search(query):
    """[(hujjat, raqam, sarlavha, topilgan, jami)] eng yaxshisi birinchi."""
    sections = S.read_tsv("sections.tsv")
    if not sections:
        return []
    idf = S.load_idf(len(sections))
    top_idf = math.log(max(len(sections), 1))
    words = []
    for token in S.tokens(S.clean_prompt(query)):
        if token not in words:
            words.append(token)
    if not words:
        return []
    synonyms, table = S.load_synonyms(), english_table()
    forms = [word_forms(w, idf, synonyms, table) for w in words]
    # So'z og'irligi so'rovdagi so'zning o'zidan: "god class" da `god`
    # `class` dan kamyob. Sarlavhadagi mos so'zdan olinsa, "klasslarini"
    # kabi uzun shakl kamyob bo'lib, umumiy so'zni oldinga chiqarardi.
    weights = [word_weight(w, f, idf, top_idf) for w, f in zip(words, forms)]

    scored = []
    for order, (doc, number, title, own, chapter) in enumerate(entries()):
        score, found = 0.0, 0
        for word_set, weight in zip(forms, weights):
            if matches(word_set, own) is None:
                if matches(word_set, chapter) is None:
                    continue
                weight *= CHAPTER_WEIGHT
            found += 1
            score += weight
        if found:
            scored.append((found, score, order, doc, number, title))
    if not scored:
        return []
    best = max(item[0] for item in scored)
    keep = [item for item in scored if item[0] == best]
    keep.sort(key=lambda item: (-item[1], item[2]))
    return [(doc, number, title, found, len(words))
            for found, _, _, doc, number, title in keep]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    query = " ".join(sys.argv[1:])
    for doc, number, title, found, total in search(query):
        sys.stdout.write("%s\t%s\t%s [so'zlar: %d/%d]\n" % (doc, number, title, found, total))
    return 0


if __name__ == "__main__":
    sys.exit(main())
