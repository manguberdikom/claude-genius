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

## Har vazifadagi qoidalar

1. **Qoidasiz qaror yo'q.** Har o'zgarish, har topilma, har reja qadami
   yonida `<hujjat> <raqam>` turadi. Topilmasa, "qoidada yo'q, mening
   asosim" deb belgilanadi.
2. **Arzon yo'l oldin.** Javob kodda yoki chiqishda bo'lsa, u o'qiladi.
   Konteyner, baza ulanishi va PowerShell **taqiqlangan** va `guard.py`
   tomonidan to'siladi. Batafsil: `references/taqiq.md`.
3. **Og'ir o'qish asosiy sessiyada emas.** Ko'p o'qib oz qaytaradigan ish
   aktyorga uzatiladi, uzun chiqish ularning kontekstida qoladi.
4. **Mezon bitta.** Arxitektor, test muhandisi va reviewer ishni
   boshlashdan oldin `python3 tools/rules_for.py <fayllar>` chaqiradi
   (reviewer `--no-mark` bilan: belgini faqat yozuvchi qo'yadi).
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
| "qayerda yozilgan", "qoida nima deydi" (bir-uch bo'lim) | aktyor yo'q: taklif hookidagi raqam yoki `tools/doc.sh find`, keyin `tools/doc.sh show` |
| ko'p bo'limni o'qib taqqoslash (uchtadan ko'p) | `qidiruv` |
| "nega yiqildi", "sxema qanday" (chiqish uzun) | `tahlil` |

Qisqa chiqishni asosiy sessiya o'zi o'qiydi: test uchun birinchi xato,
sxema uchun `python3 tools/schema_from_entities.py <src>`.

Review doirasi modul yoki butun proyekt bo'lsa yoki diff bo'sh bo'lsa,
`review` ga doira va modul ro'yxati beriladi: u agent faylidagi
`Diff yo'q bo'lsa` tartibida ishlaydi. Doira bitta chaqiruvga sig'masa,
ish boshida modullarga bo'linadi (`references/aktyorlar.md`).

Manguberdi faol bo'lsa `code-review`, `clean-code`, `design-patterns` va
`architect-review` skilllari alohida tartib sifatida yurgizilmaydi: vazifa
yuqoridagi jadval bo'yicha aktyorga beriladi, skill faqat bob jadvali
bo'lib xizmat qiladi. Topilma darajasi `review` aktyori shkalasida
(`yuqori`, `o'rta`, `past`) yoziladi; PR izohiga o'tkazilganda `yuqori` =
`blocker`, `o'rta` = `suggest`, `past` = `nit` (`code-review 4.9`).

Reja faqat `references/marshrut.md` dagi `Hajm: reja kerakmi` shartlaridan
birida (uch fayldan ko'proq yoki bir necha qatlam, qaytarib bo'lmaydigan
qaror, talab hujjatdan) yoki foydalanuvchi ochiq so'raganda tuziladi.
Kichik bug va toza kod o'zgarishini `arxitektor` rejasiz bajaradi.

Reja so'rovi har doim `rejalashtiruvchi` ga beriladi. Repoda reja
tuzadigan skill bo'lsa ham (masalan `reja`), zanjirda u chaqirilmaydi: u
asosiy sessiyada ~25k token o'qiydi va `budget.py` uni sanamaydi.

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
      v (toza yoki to'xtadi)
   memory
```

`review` kamchilik topsa, u **egasiga** qaytadi: kod muammosi
`arxitektor` ga, test muammosi `test-muhandis` ga, reja muammosi
`rejalashtiruvchi` ga. Har aktyor bitta
vazifada ko'pi bilan **ikki marta** chaqiriladi. Ikkinchidan keyin ham
hal bo'lmasa, zanjir to'xtaydi va nima yetishmayotgani aytiladi. Buni
hook sanaydi va har yangi so'rovda o'zi nolga tushiradi. Bitta so'rov
ichida ikkinchi vazifa boshlansa:
`python3 tools/budget.py --yangi-vazifa "<nom>"`.

## Model tanlash

Aktyorlar o'z modelini olib yuradi va u vazifaga qarab tanlangan:
`qidiruv` va `tahlil` haiku (ko'p o'qiydi, oz qaytaradi), `arxitektor`
va `test-muhandis` sonnet (amalga oshirish), `review` sonnet (diffni
qoidaga solishtiradi), `rejalashtiruvchi` opus (qaytarib bo'lmaydigan
qarorlar). Bu taqsimot `.claude/agents/` da yozilgan, har vazifada
qayta o'ylanmaydi.

## Memory

Memory bosqichi har zanjir oxirida bajariladi: toza tugaganda ham,
budjet tugab to'xtaganda ham. Nima yoziladi va nima **yozilmaydi** -
`references/memory.md`. Qoida bitta: `memory-protocol.md` dagi yetti
savol darvozasidan o'tmagan narsa yozilmaydi.

## Kontekst

Uzun ishda kontekstni toza saqlash va ishni yangi sessiyaga uzatish:
`references/kontekst.md`.

## Tekshiruvlar

Ish yakunida shular toza bo'lishi kerak:

```bash
# o'zgargan va yangi .java fayllar, bitta chaqiruvda, oxirida yig'ma qator
{ git diff --name-only --diff-filter=d HEAD; git ls-files --others --exclude-standard; } \
  | grep '\.java$' | xargs python3 tools/check_code.py
python3 tools/check_docs.py          # hujjat tegilgan bo'lsa
```

`xargs` 123 qaytarsa, kamida bitta faylda topilma bor.

`check_code.py` dagi eski topilma (ishdan oldin bor bo'lgan, `rules_for`
ning "Mashina topgani" ro'yxatida chiqqan) arxitektorga qaytarilmaydi:
u `Tegilmagan` qatorida aytiladi. Toza bo'lishi kerak bo'lgani yangi
yoki tegilgan qatordagi topilma.

## Chegaralar, ochiq aytilgan

Skill Claude Code ning sozlamalarini, hooklarini yoki ruxsatlarini
o'chira olmaydi: ular harness darajasida ishlaydi. Amalda bu to'siq
emas, chunki hooklar aynan shu qoidalarni majburlaydi (`guard.py`
qimmat amalni, `check_code.py` kod qoidasini). Skill ishning tartibini
belgilaydi, muhitni emas.

Skill yangi sessiya ocha olmaydi. Buning o'rniga kontekst o'lchanadi
va tayyor topshiriq beriladi: `python3 tools/handoff.py --prompt`.
Batafsil: `references/kontekst.md`.
