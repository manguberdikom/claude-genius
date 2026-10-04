---
name: manguberdi
description: Java/Spring/PostgreSQL ishini boshidan oxirigacha olib boradigan orkestrator. Sessiyada bir marta chaqiriladi va keyingi vazifalarda o'zi ishlaydi. Prompt bo'yicha aktyor tanlaydi (rejalashtiruvchi, arxitektor, test muhandisi, reviewer), ularni ketma-ket yurgizadi, har qadamni qo'llanma bo'limi bilan asoslaydi va oxirida memoryga yozadi. Review, reja tuzish va yangilash, bug tuzatish, refaktoring, test qoplash uchun.
---

# manguberdi

Bu skill sessiyada **bir marta** chaqiriladi. Shundan keyin har bir
vazifa shu yerdagi tartib bo'yicha bajariladi, qayta chaqirish shart
emas: vazifa kelganda avval `## Marshrut` ko'riladi.

Skill ishning **qanday** bajarilishini belgilaydi. Qoidalar manbai bitta:
`docs/` dagi oltita qo'llanma. Boshqa odat, boshqa did yoki boshqa
yondashuv ularning o'rnini bosmaydi.

## Har vazifada uch qoida

1. **Qoidasiz qaror yo'q.** Har o'zgarish, har topilma, har reja qadami
   yonida `<hujjat> <raqam>` turadi. Topilmasa, "qoidada yo'q, mening
   asosim" deb belgilanadi.
2. **Arzon yo'l oldin.** Javob kodda yoki chiqishda bo'lsa, u o'qiladi.
   Konteyner, baza ulanishi va PowerShell **taqiqlangan** va `guard.py`
   tomonidan to'siladi. Batafsil: `references/taqiq.md`.
3. **Og'ir o'qish asosiy sessiyada emas.** Ko'p o'qib oz qaytaradigan ish
   aktyorga uzatiladi, uzun chiqish ularning kontekstida qoladi.
4. **Mezon bitta.** Arxitektor, test muhandisi va reviewer ishni
   boshlashdan oldin `python3 tools/rules_for.py <fayllar>` chaqiradi.
   Kirish bir xil, chiqish bir xil: yozuvchi reviewer tekshiradigan
   aynan o'sha ro'yxat bilan ishlaydi. Ikkinchi aylana shundan
   kamayadi.

## Marshrut

Avval prompt normallashtiriladi (`references/marshrut.md`), keyin aktyor
tanlanadi:

| Prompt nimani so'rayapti | Boshlang'ich aktyor |
|---|---|
| "review qil", "tekshir", "nima kamchilik bor" | `review` |
| "reja tuz", "reja yangila", spetsifikatsiya yoki hujjat berildi | `rejalashtiruvchi` |
| "tuzat", "qo'sh", "refaktoring qil", bug, kichik vazifa | `arxitektor` |
| "test yoz", "qoplash", test yiqildi | `test-muhandis` |
| "qayerda yozilgan", "qoida nima deydi" | `qidiruv` |
| "nega yiqildi", "sxema qanday" | `tahlil` |

Reja **faqat zarur bo'lganda** tuziladi: bir necha fayl, bir necha qatlam
yoki qaytarib bo'lmaydigan qaror. Kichik bug va toza kod o'zgarishini
`arxitektor` rejasiz bajaradi.

## Ketma-ketlik

Ish zanjiri va har aktyorning ikki chaqiruv chegarasi:
`references/aktyorlar.md`. Qisqacha:

```
rejalashtiruvchi (zarur bo'lsa)
      v
  arxitektor  --kod muammosi--.
      v                        |
 test-muhandis --test muammosi-+
      v                        |
    review  ---kamchilik-------'
      v (toza)
   memory
```

`review` kamchilik topsa, u **egasiga** qaytadi: kod muammosi
`arxitektor` ga, test muammosi `test-muhandis` ga. Har aktyor bitta
vazifada ko'pi bilan **ikki marta** chaqiriladi. Ikkinchidan keyin ham
hal bo'lmasa, zanjir to'xtaydi va nima yetishmayotgani aytiladi.

## Model tanlash

Aktyorlar o'z modelini olib yuradi va u vazifaga qarab tanlangan:
`qidiruv` va `tahlil` haiku (ko'p o'qiydi, oz qaytaradi), `arxitektor`
va `test-muhandis` sonnet (amalga oshirish), `rejalashtiruvchi` opus
(qaytarib bo'lmaydigan qarorlar). Bu taqsimot `.claude/agents/` da
yozilgan, har vazifada qayta o'ylanmaydi.

## Memory

Ish toza tugagandan keyin memory bosqichi bajariladi. Nima yoziladi va
nima **yozilmaydi** - `references/memory.md`. Qoida bitta: `memory-protocol.md`
dagi yetti savol darvozasidan o'tmagan narsa yozilmaydi.

## Kontekst

Uzun ishda kontekstni toza saqlash va ishni yangi sessiyaga uzatish:
`references/kontekst.md`.

## Tekshiruvlar

Ish yakunida shular toza bo'lishi kerak:

```bash
python3 tools/check_code.py <o'zgargan-java-fayl>
python3 tools/check_docs.py          # hujjat tegilgan bo'lsa
```

## Chegaralar, ochiq aytilgan

Skill Claude Code ning sozlamalarini, hooklarini yoki ruxsatlarini
o'chira olmaydi: ular harness darajasida ishlaydi. Amalda bu to'siq
emas, chunki hooklar aynan shu qoidalarni majburlaydi (`guard.py`
qimmat amalni, `check_code.py` kod qoidasini). Skill ishning tartibini
belgilaydi, muhitni emas.

Skill yangi sessiya ocha olmaydi. Kontekst to'lganda ish uzatiladi:
qanday - `references/kontekst.md`.
