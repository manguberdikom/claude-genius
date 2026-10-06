#!/usr/bin/env python3
"""A/B tahlili: natijalar.tsv dan juft bootstrap va oldindan yozilgan qaror.

    python3 eval/ab/tahlil.py                    # natijalar.tsv, bitta seriya
    python3 eval/ab/tahlil.py --commit <sha12>   # bir nechta seriya bo'lsa
    python3 eval/ab/tahlil.py --quvvat           # qaror qoidasining quvvati, simulyatsiya
    python3 eval/ab/tahlil.py --sinov            # soxta natijalar bilan o'z-o'zini sinash

Qoida README dagi "Qaror qoidasi" bilan aynan bir xil va natijadan oldin
yozilgan. Bu yerda faqat hisob: qoidani o'zgartirish README ni ham,
shu faylni ham bitta commitda o'zgartiradi va yangi seriya boshlaydi.

Hisob:
- Birlik vazifa. Har vazifada holat bo'yicha o'rtacha muvaffaqiyat va
  o'rtacha USD olinadi (takrorlar bo'yicha).
- Farq d = o'rtacha_v (pB_v - pA_v), juft: har vazifa o'zi bilan.
- Narx nisbati r = sum_v usdB_v / sum_v usdA_v.
- Bootstrap: vazifalar qaytarib olinadi, har vazifa ichida har holatning
  takrorlari ham qaytarib olinadi. 10000 marta, urug' qotirilgan.
- Chegara bir tomonli 90%: quyi = 10-persentil, yuqori = 90-persentil.
- Ifloslangan qator (ifloslangan=1) hisobga kirmaydi.
"""

import argparse
import random
import statistics
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import umumiy  # noqa: E402

URUG = 20261005
BOOT = 10000
USTUNLIK_NARX = 1.5      # B yaxshiroq bo'lsa narx nisbatining yuqori chegarasi
NON_INF_FARQ = -0.05     # B "yomon emas" deyish uchun farqning quyi chegarasi
NON_INF_NARX = 1.0       # ... va u holda B arzonroq yoki teng bo'lishi shart
TOLIQ_VAZIFA = 10
TOLIQ_TAKROR = 3
IKKINCHI_BOSQICH = 20


def seriyalar(qatorlar):
    s = {}
    for q in qatorlar:
        s.setdefault((q.get("genius_commit", ""), q.get("model", "")), []).append(q)
    return s


def son(x, sukut=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return sukut


def jadval(qatorlar):
    """{vazifa: {"A": [(muv, usd)], "B": [...]}} faqat ikkala holati bor vazifalar."""
    j = {}
    for q in qatorlar:
        if q.get("ifloslangan") == "1" or q.get("holat") not in ("A", "B"):
            continue
        if q.get("muvaffaqiyat", "") == "":
            continue
        j.setdefault(q["vazifa"], {"A": [], "B": []})[q["holat"]].append(
            (son(q["muvaffaqiyat"]), son(q.get("usd"))))
    return {v: x for v, x in j.items() if x["A"] and x["B"]}


def _orta(xs):
    return sum(xs) / len(xs)


def hisob(j, boot=BOOT, urug=URUG):
    """Nuqta bahosi va bir tomonli 90% chegaralar."""
    vaz = sorted(j)

    def statistika(tanlov, olish):
        farq, ua, ub = [], 0.0, 0.0
        for v in tanlov:
            a, b = olish(j[v]["A"]), olish(j[v]["B"])
            farq.append(_orta([m for m, _ in b]) - _orta([m for m, _ in a]))
            ua += _orta([u for _, u in a])
            ub += _orta([u for _, u in b])
        return _orta(farq), (ub / ua if ua > 0 else float("inf"))

    d, r = statistika(vaz, lambda xs: xs)
    rng = random.Random(urug)
    ds, rs = [], []
    for _ in range(boot):
        tanlov = [rng.choice(vaz) for _ in vaz]
        bd, br = statistika(tanlov, lambda xs: [rng.choice(xs) for _ in xs])
        ds.append(bd)
        rs.append(br)
    ds.sort()
    rs.sort()

    def pers(xs, p):
        return xs[min(len(xs) - 1, max(0, int(p * len(xs))))]

    return {"d": d, "d_quyi": pers(ds, 0.10), "d_yuqori": pers(ds, 0.90),
            "r": r, "r_quyi": pers(rs, 0.10), "r_yuqori": pers(rs, 0.90)}


def qaror(h, bosqich):
    """README dagi qoida. Natija: (qaror, sabab)."""
    if h["d_quyi"] > 0 and h["r_yuqori"] <= USTUNLIK_NARX:
        return "B QOLADI", "ustunlik: farq quyi chegarasi > 0 va narx nisbati yuqori chegarasi <= %.1f" % USTUNLIK_NARX
    if h["d_quyi"] >= NON_INF_FARQ and h["r_yuqori"] <= NON_INF_NARX:
        return "B QOLADI", "non-inferiority: farq quyi chegarasi >= %.2f va B arzonroq" % NON_INF_FARQ
    if h["d_yuqori"] < 0:
        return "B OLIB TASHLANADI", "B aniq yomonroq: farq yuqori chegarasi < 0"
    if h["r_quyi"] > USTUNLIK_NARX:
        return "B OLIB TASHLANADI", "B aniq qimmat: narx nisbati quyi chegarasi > %.1f" % USTUNLIK_NARX
    if bosqich >= 2:
        return "B OLIB TASHLANADI", "2-bosqichda ham B qolish shartini bajarmadi"
    return "NOANIQ", "2-bosqich: 10 yangi vazifa qo'shilib %d x 2 x %d gacha to'ldiriladi" % (
        IKKINCHI_BOSQICH, TOLIQ_TAKROR)


def tahlil(qatorlar, commit=None, chiqar=print, boot=BOOT):
    """Natija lug'ati; xato bo'lsa {'xato': ...}."""
    seriya = seriyalar(qatorlar)
    if commit:
        seriya = {k: v for k, v in seriya.items() if k[0].startswith(commit[:12])}
    if not seriya:
        return {"xato": "natijalar.tsv da natija qatori yo'q"}
    if len(seriya) > 1:
        return {"xato": "bir nechta seriya (genius_commit, model): %s; --commit bilan tanlang"
                % ", ".join("%s/%s" % k for k in sorted(seriya))}
    (gc, model), qq = next(iter(seriya.items()))
    ifl = {h: sum(1 for q in qq if q.get("holat") == h and q.get("ifloslangan") == "1") for h in "AB"}
    j = jadval(qq)
    takror = min((len(x["A"]) for x in j.values()), default=0)
    takror = min([takror] + [len(x["B"]) for x in j.values()]) if j else 0
    chiqar("seriya: genius %s, model %s" % (gc or "-", model or "-"))
    chiqar("vazifa: %d (ikkala holati bor), eng kam takror: %d, ifloslangan: A %d, B %d"
           % (len(j), takror, ifl["A"], ifl["B"]))
    natija = {"vazifa": len(j), "takror": takror, "ifloslangan": ifl}
    if not j:
        natija["qaror"] = "QAROR YO'Q"
        chiqar("qaror: QAROR YO'Q (ifloslanmagan juft yo'q)")
        return natija
    for v in sorted(j, key=lambda x: int(x)):
        a, b = j[v]["A"], j[v]["B"]
        chiqar("  %2s  A %.2f (%d)  B %.2f (%d)  usd A %.2f  B %.2f"
               % (v, _orta([m for m, _ in a]), len(a), _orta([m for m, _ in b]), len(b),
                  _orta([u for _, u in a]), _orta([u for _, u in b])))
    h = hisob(j, boot=boot)
    natija.update(h)
    chiqar("farq (B-A): %+.3f  [90%% quyi %+.3f, yuqori %+.3f]" % (h["d"], h["d_quyi"], h["d_yuqori"]))
    chiqar("USD nisbati (B/A): %.2f  [90%% quyi %.2f, yuqori %.2f]" % (h["r"], h["r_quyi"], h["r_yuqori"]))
    for nom in ("daqiqa", "token"):
        for hl in "AB":
            xs = [son(q.get(nom)) for q in qq if q.get("holat") == hl and q.get("ifloslangan") != "1"
                  and q.get(nom, "") != ""]
            if xs:
                chiqar("  %s %s mediana: %.1f" % (nom, hl, statistics.median(xs)))
    for v in ("8", "9"):
        for hl in "AB":
            xs = [son(q.get("xato_topildi")) for q in qq if q.get("vazifa") == v and q.get("holat") == hl
                  and q.get("ifloslangan") != "1" and q.get("xato_topildi", "") != ""]
            ys = [son(q.get("yolgon_topilma")) for q in qq if q.get("vazifa") == v and q.get("holat") == hl
                  and q.get("ifloslangan") != "1" and q.get("yolgon_topilma", "") != ""]
            if xs or ys:
                chiqar("  review %s %s: xato_topildi %s, yolgon_topilma %s"
                       % (v, hl, "%.1f" % _orta(xs) if xs else "-", "%.1f" % _orta(ys) if ys else "-"))
    if len(j) < TOLIQ_VAZIFA or takror < TOLIQ_TAKROR:
        natija["qaror"] = "QAROR YO'Q"
        chiqar("qaror: QAROR YO'Q (smoke yoki to'liq emas: kamida %d vazifa x %d takror kerak)"
               % (TOLIQ_VAZIFA, TOLIQ_TAKROR))
        return natija
    bosqich = 2 if len(j) >= IKKINCHI_BOSQICH else 1
    q, sabab = qaror(h, bosqich)
    natija.update({"qaror": q, "sabab": sabab, "bosqich": bosqich})
    chiqar("qaror (%d-bosqich): %s, chunki %s" % (bosqich, q, sabab))
    return natija


# ---------------------------------------------------------------- quvvat

def simulyatsiya(n_vazifa, takror, effekt, narx, rng):
    qatorlar = []
    for v in range(1, n_vazifa + 1):
        pa = rng.betavariate(1.5, 1.0)
        pb = min(1.0, max(0.0, pa + effekt))
        asos = rng.lognormvariate(0.7, 0.4)
        for k in range(1, takror + 1):
            for h, p, ko in (("A", pa, 1.0), ("B", pb, narx)):
                qatorlar.append({"vazifa": str(v), "holat": h, "takror": str(k),
                                 "muvaffaqiyat": "1" if rng.random() < p else "0",
                                 "usd": "%.3f" % (asos * ko * rng.lognormvariate(0, 0.25)),
                                 "ifloslangan": "0", "genius_commit": "sim", "model": "sim"})
    return qatorlar


def quvvat(n_vazifa=TOLIQ_VAZIFA, takror=TOLIQ_TAKROR, sim=200, boot=400):
    rng = random.Random(URUG)
    print("Qaror qoidasi quvvati (%d vazifa x %d takror, %d simulyatsiya, bootstrap %d)"
          % (n_vazifa, takror, sim, boot))
    for effekt, narx in ((0.2, 1.2), (0.0, 1.2), (0.0, 0.8), (0.0, 2.0), (-0.1, 1.0)):
        sanoq = {}
        for _ in range(sim):
            n = tahlil(simulyatsiya(n_vazifa, takror, effekt, narx, rng), chiqar=lambda *_: None, boot=boot)
            sanoq[n["qaror"]] = sanoq.get(n["qaror"], 0) + 1
        print("  effekt %+.2f, narx x%.1f: %s" % (effekt, narx, ", ".join(
            "%s %d%%" % (k, round(100 * v / sim)) for k, v in sorted(sanoq.items()))))
    return 0


# ---------------------------------------------------------------- sinov

def _qatorlar(spek, commit="abc123def456", model="m"):
    """spek: [(vazifa, holat, [muv...], usd, ifloslangan)]."""
    qq = []
    for v, h, muvlar, usd, ifl in spek:
        for k, m in enumerate(muvlar, 1):
            qq.append({"vazifa": str(v), "holat": h, "takror": str(k), "sessiya_id": "s",
                       "genius_commit": commit, "model": model, "muvaffaqiyat": str(m),
                       "usd": str(usd), "ifloslangan": "1" if ifl else "0", "memory_toza": "1"})
    return qq


def sinov():
    xato = []

    def tek(shart, nom):
        print(("  ok   " if shart else "  XATO ") + nom)
        if not shart:
            xato.append(nom)

    jim = lambda *_: None  # noqa: E731
    A = [0, 1, 0]

    def toplam(fa, fb, ua, ub, n=10):
        s = []
        for v in range(1, n + 1):
            s.append((v, "A", fa(v), ua, False))
            s.append((v, "B", fb(v), ub, False))
        return _qatorlar(s)

    kuchli = toplam(lambda v: A, lambda v: [1, 1, 1], 2.0, 2.4)
    n = tahlil(kuchli, chiqar=jim, boot=2000)
    tek(n["qaror"] == "B QOLADI" and "ustunlik" in n["sabab"], "katta effekt, narx x1.2 -> B QOLADI")
    tek(abs(n["d"] - 2 / 3) < 1e-9 and abs(n["r"] - 1.2) < 1e-9, "nuqta bahosi: d=0.667, r=1.2")

    qimmat = toplam(lambda v: [1, 1, 1], lambda v: [1, 1, 1], 1.0, 3.0)
    n = tahlil(qimmat, chiqar=jim, boot=2000)
    tek(n["qaror"] == "B OLIB TASHLANADI" and "qimmat" in n["sabab"], "effekt yo'q, narx x3 -> OLIB TASHLANADI")

    kuchli_qimmat = toplam(lambda v: A, lambda v: [1, 1, 1], 1.0, 3.0)
    n = tahlil(kuchli_qimmat, chiqar=jim, boot=2000)
    tek(n["qaror"] == "B OLIB TASHLANADI", "B yaxshi, lekin narx x3 -> OLIB TASHLANADI (narx sharti ikkala yo'lda)")

    arzon = toplam(lambda v: [1, 1, 1], lambda v: [1, 1, 1], 2.0, 1.5)
    n = tahlil(arzon, chiqar=jim, boot=2000)
    tek(n["qaror"] == "B QOLADI" and "non-inferiority" in n["sabab"], "teng va arzon -> non-inferiority bilan QOLADI")

    yomon = toplam(lambda v: [1, 1, 1], lambda v: [0, 0, 1], 1.0, 1.0)
    n = tahlil(yomon, chiqar=jim, boot=2000)
    tek(n["qaror"] == "B OLIB TASHLANADI" and "yomonroq" in n["sabab"], "B yomonroq -> OLIB TASHLANADI")

    def fa(v):
        return [1, 0, 1] if v % 2 else [0, 1, 0]

    def fb(v):
        return [0, 1, 0] if v % 2 else [1, 0, 1]

    shovqin = toplam(fa, fb, 2.0, 2.2)
    n = tahlil(shovqin, chiqar=jim, boot=2000)
    tek(n["qaror"] == "NOANIQ", "effekt yo'q, B sal qimmat, 1-bosqich -> NOANIQ")
    n = tahlil(toplam(fa, fb, 2.0, 2.2, n=20), chiqar=jim, boot=2000)
    tek(n["qaror"] == "B OLIB TASHLANADI" and n["bosqich"] == 2, "20 vazifada ham noaniq -> OLIB TASHLANADI")
    n = tahlil(toplam(fa, lambda v: [1, 1, 0] if v % 2 else [1, 0, 1], 2.0, 2.2, n=20), chiqar=jim, boot=2000)
    tek(n["qaror"] == "B QOLADI" and n["bosqich"] == 2, "2-bosqichda effekt ko'rinsa -> B QOLADI")

    ifl = _qatorlar([(v, "B", [1, 1, 1], 1.0, True) for v in range(1, 11)])
    n = tahlil(qimmat + ifl, chiqar=jim, boot=2000)
    tek(n["ifloslangan"]["B"] == 30 and n["qaror"] == "B OLIB TASHLANADI",
        "ifloslangan qatorlar hisobga kirmaydi")

    smoke = _qatorlar([(v, h, [1], 1.0, False) for v in (1, 3, 8) for h in "AB"])
    n = tahlil(smoke, chiqar=jim, boot=200)
    tek(n["qaror"] == "QAROR YO'Q", "smoke (3 x 2 x 1) qaror bermaydi")

    aralash = kuchli + _qatorlar([(1, "A", [1], 1.0, False)], commit="boshqa000000")
    n = tahlil(aralash, chiqar=jim, boot=200)
    tek("xato" in n and "seriya" in n["xato"], "ikki genius_commit aralashsa xato")
    n = tahlil(aralash, commit="abc123def456", chiqar=jim, boot=200)
    tek(n.get("qaror") == "B QOLADI", "--commit bilan seriya tanlanadi")

    tek(hisob(jadval(shovqin), boot=500) == hisob(jadval(shovqin), boot=500), "bootstrap urug' bilan takrorlanadi")

    with tempfile.TemporaryDirectory() as t:
        tsv = Path(t) / "n.tsv"
        for q in kuchli:
            umumiy.natija_yoz(q, tsv)
        n = tahlil(umumiy.natija_oqi(tsv), chiqar=jim, boot=2000)
        tek(n["qaror"] == "B QOLADI" and n["vazifa"] == 10 and n["takror"] == 3,
            "natijalar.tsv orqali aylanib keladi")

    print("tahlil --sinov: %s" % ("hammasi o'tdi" if not xato else "%d XATO" % len(xato)))
    return 1 if xato else 0


def asosiy(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--natijalar", default=str(umumiy.NATIJALAR))
    p.add_argument("--commit", help="genius_commit (seriya)")
    p.add_argument("--quvvat", action="store_true")
    p.add_argument("--vazifa-soni", type=int, default=TOLIQ_VAZIFA)
    p.add_argument("--takror", type=int, default=TOLIQ_TAKROR)
    p.add_argument("--sinov", action="store_true")
    a = p.parse_args(argv)
    if a.sinov:
        return sinov()
    if a.quvvat:
        return quvvat(a.vazifa_soni, a.takror)
    n = tahlil(umumiy.natija_oqi(a.natijalar), a.commit)
    if "xato" in n:
        print(n["xato"], file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(asosiy())
