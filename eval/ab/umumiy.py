#!/usr/bin/env python3
"""A/B sinovining umumiy qismi: vazifa fayllari, natijalar.tsv, transkript.

yurgiz.py, baho.py va tahlil.py shu modulni import qiladi. O'zi ishga
tushirilmaydi. Bu fayl `tools/` da emas: u faqat A/B sinoviga tegishli
va genius asboblari qatoriga qo'shilmaydi.
"""

import csv
import json
import os
import re
from pathlib import Path

AB = Path(__file__).resolve().parent
GENIUS = AB.parents[1]
VAZIFALAR = AB / "vazifalar"
OLTIN = AB / "oltin"
NATIJALAR = AB / "natijalar.tsv"

PETCLINIC_URL = "https://github.com/spring-projects/spring-petclinic"
PETCLINIC_COMMIT = "500158f732419217507c7656904b8e6aa1bcc0d6"

# Testcontainers talab qiladigan uchta sinf hamma joyda chiqariladi.
TOLIQ_TOPLAM = "!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests"

# B holatining aktyorlari. A transkriptida ulardan biri subagent_type
# bo'lib kelsa, yurish ifloslangan (README, "Ifloslanish").
AKTYORLAR = ("rejalashtiruvchi", "dasturchi", "test-muhandis", "review",
             "qidiruv", "tahlil")

# Natijalar ustunlari. Tartib o'zgarsa tahlil.py eski qatorlarni ham
# nom bo'yicha o'qiydi, shuning uchun faqat oxiriga qo'shiladi.
USTUNLAR = [
    "vazifa", "holat", "takror", "sessiya_id", "genius_commit", "model",
    "muvaffaqiyat", "xato_topildi", "yolgon_topilma", "usd", "token",
    "daqiqa", "aralashuv", "kor_baho", "ifloslangan", "memory_toza", "izoh",
]


class Vazifa:
    """Bitta vazifa fayli: raqam, tur, prompt va tayyorlov diffi."""

    def __init__(self, raqam, fayl, tur, prompt, diff, birinchi):
        self.raqam = raqam
        self.fayl = fayl
        self.tur = tur
        self.prompt = prompt
        self.diff = diff
        self.birinchi = birinchi

    @property
    def tartib(self):
        return ("A", "B") if self.birinchi == "A" else ("B", "A")

    def __repr__(self):
        return f"Vazifa({self.raqam}, {self.tur})"


def _bolim(matn, sarlavha):
    """`## <sarlavha>` dan keyingi `## ` gacha bo'lgan matn."""
    m = re.search(rf"^## {re.escape(sarlavha)}[^\n]*\n(.*?)(?=^## |\Z)",
                  matn, re.S | re.M)
    return m.group(1) if m else ""


def vazifa_oqi(fayl):
    """Vazifa faylidan prompt va tayyorlovni oladi.

    Prompt `## Prompt` bo'limidagi birinchi ```text blokidan aynan olinadi:
    ikkala holat bir xil matnni oladi va u faqat shu faylda yashaydi.
    """
    fayl = Path(fayl)
    matn = fayl.read_text(encoding="utf-8")
    raqam = int(fayl.name.split("-", 1)[0])
    tur_m = re.search(r"\*\*Tur:\*\*\s*([^.(]+)", matn)
    tur = tur_m.group(1).strip() if tur_m else ""
    if tur.startswith("bug"):
        tur = "bug"
    elif tur.startswith("refaktoring"):
        tur = "refaktoring"
    elif tur.startswith("test"):
        tur = "test"
    elif tur.startswith("review"):
        tur = "review"
    elif tur.startswith("reja"):
        tur = "reja"
    prompt_m = re.search(r"```text\n(.*?)\n```", _bolim(matn, "Prompt"), re.S)
    if not prompt_m:
        raise ValueError(f"{fayl.name}: ## Prompt da ```text bloki yo'q")
    diff_m = re.search(r"git apply \S*eval/ab/vazifalar/diff/(\S+\.diff)",
                       _bolim(matn, "Tayyorlash"))
    tartib_m = re.search(r"\*\*Tartib:\*\*\s*([AB]) birinchi", matn)
    birinchi = tartib_m.group(1) if tartib_m else ("A" if raqam % 2 else "B")
    return Vazifa(raqam, fayl, tur, prompt_m.group(1),
                  diff_m.group(1) if diff_m else None, birinchi)


def vazifalar():
    """Hamma vazifa, raqam tartibida."""
    return [vazifa_oqi(f) for f in sorted(VAZIFALAR.glob("[0-9][0-9]-*.md"))]


def natija_oqi(yol=NATIJALAR):
    yol = Path(yol)
    if not yol.exists():
        return []
    with yol.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def natija_yoz(qator, yol=NATIJALAR):
    """Bitta qatorni qo'shadi. Sarlavha yo'q yoki eski bo'lsa to'xtaydi."""
    yol = Path(yol)
    if yol.exists() and yol.stat().st_size:
        sarlavha = yol.read_text(encoding="utf-8").split("\n", 1)[0].split("\t")
        if sarlavha != USTUNLAR:
            raise SystemExit(f"{yol}: sarlavha USTUNLAR ga mos emas, qo'lda tekshiring")
    else:
        yol.write_text("\t".join(USTUNLAR) + "\n", encoding="utf-8")
    qiymat = []
    for k in USTUNLAR:
        v = qator.get(k, "")
        v = "" if v is None else str(v)
        qiymat.append(v.replace("\t", " ").replace("\n", " "))
    with yol.open("a", encoding="utf-8") as f:
        f.write("\t".join(qiymat) + "\n")


def transkriptlar(config_dir):
    """CLAUDE_CONFIG_DIR ichidagi hamma transkript (subagentlar ham).

    Har yurishning o'z config papkasi bor, shuning uchun bu yerdagi har
    fayl aynan shu yurishga tegishli.
    """
    papka = Path(config_dir) / "projects"
    if not papka.is_dir():
        return []
    return sorted(papka.rglob("*.jsonl"))


def transkript_yozuvlari(fayllar):
    """JSONL yozuvlarini ketma-ket beradi, buzuq qatorni o'tkazadi."""
    for fayl in fayllar:
        with open(fayl, encoding="utf-8", errors="replace") as f:
            for qator in f:
                qator = qator.strip()
                if not qator:
                    continue
                try:
                    yield json.loads(qator)
                except ValueError:
                    continue


def tool_uselar(yozuvlar):
    """Assistant xabarlaridagi tool_use bloklari: (nom, input)."""
    for y in yozuvlar:
        xabar = y.get("message") if isinstance(y, dict) else None
        if not isinstance(xabar, dict):
            continue
        kontent = xabar.get("content")
        if not isinstance(kontent, list):
            continue
        for blok in kontent:
            if isinstance(blok, dict) and blok.get("type") == "tool_use":
                yield blok.get("name", ""), blok.get("input") or {}


def foydalanuvchi_matnlari(yozuvlar):
    """User xabarlaridagi matn (slash buyruq izi shu yerda)."""
    for y in yozuvlar:
        if not isinstance(y, dict) or y.get("type") != "user":
            continue
        xabar = y.get("message")
        if not isinstance(xabar, dict):
            continue
        kontent = xabar.get("content")
        if isinstance(kontent, str):
            yield kontent
        elif isinstance(kontent, list):
            for blok in kontent:
                if isinstance(blok, dict) and blok.get("type") == "text":
                    yield blok.get("text", "")


def git_blob_sha(data):
    """`git hash-object` bilan bir xil SHA-1: memory tozaligini git siz tekshirish uchun."""
    import hashlib
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def papka_manifest(papka):
    """Papkadagi fayllar: nisbiy yo'l -> git blob sha."""
    papka = Path(papka)
    natija = {}
    if not papka.is_dir():
        return natija
    for f in sorted(papka.rglob("*")):
        if f.is_file():
            natija[f.relative_to(papka).as_posix()] = git_blob_sha(f.read_bytes())
    return natija


def env_toza(asos=None):
    """Bola `claude -p` uchun muhit: ota sessiya izlari olib tashlanadi.

    CLAUDE_CODE_SESSION_ID meros bo'lsa bola sessiya ota id sini oladi,
    budjet va usage aralashadi (PL-CC10). `env -u CLAUDE_CODE_SESSION_ID`
    ning Python dagi teng'i.
    """
    env = dict(os.environ if asos is None else asos)
    for k in ("CLAUDE_CODE_SESSION_ID", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT",
              "CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR"):
        env.pop(k, None)
    return env
