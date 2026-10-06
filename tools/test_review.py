#!/usr/bin/env python3
"""review_status.py va review_queue.py uchun sinovlar.

    python3 tools/test_review.py

Ikkisi bitta faylda, chunki ikkisi ham `docs/review.tsv` ni o'qiydi va
sinovlari o'sha fixture ni bo'lishadi.
"""

import io
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import review_queue as Q  # noqa: E402
import review_status as S  # noqa: E402

TSV = ("# izoh qatori tashlanadi\n"
       "hujjat\tbob\tholat\tsana\ttekshiruvchi\tmanbalar\txatolar\tizoh\n"
       "architect\t1\tai-draft\t\t\t0\t0\t\n"
       "architect\t2\ttekshirilgan\t2026-10-05\todam\t4\t3\tizoh\n"
       "architect\t3\ttekshirilmoqda\t\tsessiya\t2\t0\t\n"
       "patterns\t\tai-draft\t\t\t0\t0\t\n")


def with_tsv(text=TSV):
    tmp = tempfile.mkdtemp(prefix="review_")
    path = os.path.join(tmp, "review.tsv")
    io.open(path, "w", encoding="utf-8").write(text)
    return tmp, path


def case_oqish():
    tmp, path = with_tsv()
    try:
        rows = S.read_review(path)
        return (len(rows) == 4
                and rows[("architect", "1")]["holat"] == "ai-draft"
                and rows[("architect", "2")]["sana"] == "2026-10-05"
                and ("patterns", "") in rows)      # raqamsiz bob
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def case_fayl_yoq():
    return S.read_review("/yoq/papka/review.tsv") == {}


def case_holat_matni():
    draft = S.status_line({"holat": "ai-draft"})
    done = S.status_line({"holat": "tekshirilgan", "sana": "2026-10-05"})
    doing = S.status_line({"holat": "tekshirilmoqda"})
    none = S.status_line(None)
    return (draft.startswith(S.MARKER) and "inson tekshirmagan" in draft
            and "2026-10-05" in done and "Manbalar" in done
            and "tekshirilmoqda" in doing
            and none == draft)             # qator yo'q bo'lsa ai-draft


def case_qator_qoshiladi():
    text = "\n".join(["<!-- doc: x | chapter: 1 | part:  -->", "",
                      "[Barcha](../../README.md) / [X](README.md)", "",
                      "# 1. Sarlavha", "", "Matn."])
    new, did = S.apply_to(text, "> Holat: sinov.")
    lines = new.split("\n")
    return (did and lines[4] == "> Holat: sinov." and lines[5] == ""
            and lines[6] == "# 1. Sarlavha")


def case_qator_almashadi():
    text = "\n".join(["<!-- doc: x | chapter: 1 | part:  -->", "",
                      "[Barcha](../../README.md) / [X](README.md)", "",
                      "> Holat: eski.", "", "# 1. Sarlavha"])
    new, did = S.apply_to(text, "> Holat: yangi.")
    return did and new.split("\n")[4] == "> Holat: yangi." and new.count("Holat") == 1


def case_qator_ikki_marta_qoshilmaydi():
    text = "\n".join(["<!-- doc: x | chapter: 1 | part:  -->", "",
                      "[Barcha](../../README.md) / [X](README.md)", "",
                      "> Holat: bir xil.", "", "# 1. Sarlavha"])
    new, did = S.apply_to(text, "> Holat: bir xil.")
    return not did and new == text


def case_qisqa_fayl_buzilmaydi():
    text = "faqat bitta qator"
    new, did = S.apply_to(text, "> Holat: sinov.")
    return not did and new == text


def case_navbat_normallashadi():
    """Katta shkalali dalil qolganini bosib ketmaydi."""
    rows = Q.build()
    if not rows:
        return False
    top = rows[0]
    # Birinchi o'rin faqat Sonar kaliti ko'p bo'lgani uchun bo'lmasin:
    # rules_for yoki eval dalili ham bo'lishi kerak.
    return (top[4] > 0 or top[5] > 0) and len(rows) > 200


def case_navbat_tekshirilganni_oxirga_qoyadi():
    rows = Q.build()
    done = [r for r in rows if r[3] == "tekshirilgan"]
    return all(r[0] == -1.0 for r in done)


def case_navbat_dalillari_bor():
    """Uch dalil ham haqiqatan topiladi, aks holda vazn ma'nosiz."""
    return (sum(Q.rules_for_hits().values()) > 0
            and sum(Q.sonar_hits().values()) > 0
            and sum(Q.eval_hits().values()) > 0)


def case_navbat_holat_filtri():
    """--holat: agent ai-draft ni, odam tekshirilmoqda ni oladi; tartib saqlanadi."""
    rows = [(5.0, "a", "1", "tekshirilmoqda"), (4.0, "a", "2", "ai-draft"),
            (3.0, "a", "3", "ai-draft"), (-1.0, "a", "4", "tekshirilgan")]
    agent = Q.filter_rows(rows, "ai-draft")
    odam = Q.filter_rows(rows, "tekshirilmoqda")
    return ([r[2] for r in agent] == ["2", "3"]
            and [r[2] for r in odam] == ["1"]
            and Q.filter_rows(rows, None) == rows)


def case_navbat_holat_yoz_bilan_rad():
    """--holat va --yoz birga: navbat fayli qisman yozilmaydi."""
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        code = Q.main(["--yoz", "--holat", "ai-draft"])
    return code == 2


def case_readme_qatori():
    line = S.readme_line(224, 0, 5, "docs/review.tsv")
    return (line.startswith(S.MARKER) and "224 bobdan 0 tasi odam tekshirgan" in line
            and "5 tasi tekshirilmoqda" in line and "qolgan 219 tasi AI yozgan" in line
            and "](docs/review.tsv)" in line
            # check_docs dagi regexlar: `N bob\b` va `- N bo'lim` ushlamasin.
            and not __import__("re").search(r"\d+\s+bob\b", line)
            and "bo'lim" not in line)


def case_readme_jadval_ostiga():
    text = ("# Kitob\n\n| Hujjat | Hajm |\n|---|---|\n"
            "| [A](docs/a/README.md) | 1 bob |\n| [B](docs/b/README.md) | 2 bob |\n"
            "\nKeyingi matn.\n")
    new, did = S.apply_readme(text, "> Holat: x.", r"^\| \[.*\]\(docs/[a-z-]+/README\.md\) \|")
    lines = new.split("\n")
    at = lines.index("> Holat: x.")
    again, did2 = S.apply_readme(new, "> Holat: x.", r"^\| \[")
    swapped, did3 = S.apply_readme(new, "> Holat: y.", r"^\| \[")
    return (did and lines[at - 1] == "" and lines[at - 2].startswith("| [B]")
            and not did2 and again == new
            and did3 and swapped.count("> Holat:") == 1 and "> Holat: y." in swapped)


def case_readme_langarsiz_ozgarmaydi():
    new, did = S.apply_readme("# Faqat sarlavha\n", "> Holat: x.", r"^\*\*Versiya")
    return not did and new == "# Faqat sarlavha\n"


def case_readme_sanoq():
    review = {("a", "1"): {"holat": "tekshirilgan"}, ("a", "2"): {"holat": "tekshirilmoqda"}}
    return (S.tally(review, [("a", "1"), ("a", "2"), ("a", "3")]) == (3, 1, 1)
            and S.tally({}, [("a", "1")]) == (1, 0, 0))


CASES = [
    ("review.tsv o'qiladi, izoh tashlanadi", case_oqish),
    ("fayl yo'q bo'lsa bo'sh", case_fayl_yoq),
    ("holat matni uch holat uchun", case_holat_matni),
    ("holat qatori breadcrumb ostiga qo'shiladi", case_qator_qoshiladi),
    ("bor holat qatori almashadi", case_qator_almashadi),
    ("bir xil qator ikkinchi marta yozilmaydi", case_qator_ikki_marta_qoshilmaydi),
    ("qisqa fayl buzilmaydi", case_qisqa_fayl_buzilmaydi),
    ("navbat: dalillar normallashadi", case_navbat_normallashadi),
    ("navbat: tekshirilgan bob oxirda", case_navbat_tekshirilganni_oxirga_qoyadi),
    ("navbat: uch dalil ham topiladi", case_navbat_dalillari_bor),
    ("navbat: --holat filtri", case_navbat_holat_filtri),
    ("navbat: --holat --yoz bilan rad etiladi", case_navbat_holat_yoz_bilan_rad),
    ("README holat qatori matni", case_readme_qatori),
    ("README holat qatori jadval ostiga, bir marta", case_readme_jadval_ostiga),
    ("README langarsiz bo'lsa o'zgarmaydi", case_readme_langarsiz_ozgarmaydi),
    ("README sanog'i holat bo'yicha", case_readme_sanoq),
]


def main():
    failures = 0
    for name, fn in CASES:
        try:
            ok = bool(fn())
        except Exception as exc:
            ok, name = False, "%s (%s)" % (name, exc)
        failures += not ok
        print("%-4s %s" % ("OK" if ok else "XATO", name))
    print("\n%d/%d o'tdi" % (len(CASES) - failures, len(CASES)))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
