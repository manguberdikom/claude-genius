# O'zgarishlar

Har versiya `VERSION` faylida, o'rnatilgani `python3 tools/versiya.py`
da ko'rinadi. Yangi versiya chiqqanda shu ro'yxatning boshiga yoziladi.

## 0.5.3 (2026-10-21)

- `guruh.py birlashtir` fayl yo'qotmaydi: asos `dev` tarixida va daraxt
  toza bo'lsa guruh commitlari `cherry-pick` bilan (har qadam commiti
  alohida qoladi), aks holda patch. Ikkala yo'lda har fayl guruh nusxasi
  bilan solishtiriladi (`tekshiruv: N/N`), bittasi tushmasa guruh
  birlashgan hisoblanmaydi. `--3way` patch umuman qo'llanmasa buni
  aytadi (avval "ziddiyat" deb `tozala --majburiy` ga yo'naltirardi).
  Kesishish asosdan beri commit qilingan o'zgarishni ham ko'radi.
- `tozala --majburiy` commit qilinmagan ishni avval `genius/<id>` ga
  commit qiladi, branch qoladi.

## 0.5.2 (2026-10-21)

- `run_tests.py --qadam [<test>...]`: refaktoring harakati va bug qizili
  uchun tor tanlov: berilgan testlar va commit qilinmagan o'zgarishning
  bevosita testlari. Entity, bean, sozlama, migratsiya ta'siri, bir qadam
  narisi va modulga kengayish guruh oxiridagi `--asos`/`--diff` ga
  qoladi. Avval har harakat entity yoki servisga tegsa modulning hamma
  baza va Spring testlarini, guruhda esa guruh boshidan yig'ilgan diffni
  yurgizardi.

## 0.5.1 (2026-10-20)

O'lchovdan keyin (7 vazifa, keyin 4 qayta yurish):
- Mavjud `String` holat turi vazifa so'ramasa o'zgarmaydi; refaktoringda
  public setter qabul qiladigan qiymatlar ham xulq (clean-code 38.11).
- O'zgartiruvchi metod invariantni o'zi tekshiradi (patterns 13.15); xato
  istisno bilan, `false` qaytarib emas (clean-code 18.1); pul yaxlitlash
  bitta metodda (clean-code 37.8).

## 0.5.0 (2026-10-20)

Qatorma-qator audit (10 yo'nalish, 169 tasdiqlangan topilma) natijasi.

- Qamrov: rules_for ga kartasiz belgilar `unumdorlik`, `JVM xotira`,
  `sonar`, `API moslik`, `yangi proyekt`; deadlock va izolyatsiya
  tranzaksiyaga, flaky test asinxron testga. Boblar vazifa mavzusidan
  navbatma-navbat tanlanadi (bitta belgi 8 o'rinni egallamaydi).
- Tez yo'l fayl yo'lidan ham yopiladi (migratsiya, application.yml,
  build fayli); bog'liqlik, API moslik, pul, unumdorlik, yangi proyekt
  ham yopadi.
- Mexanik darvozalar: check_code Lombok `@Setter`/`@Data` va oddiy
  sinfdagi ikki yozuvchini ushlaydi, `@Deprecated` setter o'tadi;
  run_tests testga tegmaydigan o'zgarishda exit 5; sonar_local darvozasi
  faqat yangi kod bo'yicha.
- Bug fix har yo'lda avval qizil regressiya testi; refaktoringda
  xarakterizatsiya testlari `sha1sum` bilan qotiriladi.
- Diffsiz va eski proyekt review: `metod_bormi --audit`, code-review 12,
  38, Sonar ma'lumoti, ko'p bobli `doc.sh checklist`.
- 42 kartadagi xato misol va ziddiyatlar tuzatildi, takrorlar olib
  tashlandi; aktyor va skill fayllari kichraydi (jami ~6 KB).
- 8 bobdagi misol kartaga moslandi; ular `tekshirilmoqda` ga qaytdi.

## 0.4.1 (2026-10-19)

- `metod_bormi.py --audit` bir teshik buzilishini aniq sanaydi: boshqa
  sinfdan yozish (`a.setX(..)`, `a.x = ..`) va ochiq public setter alohida;
  test fayllari hisobga olinmaydi (`--ozgartiradi` da ham).
- Refaktoringda feature envy (clean-code 33.18): servisdagi qoida va
  o'zgarish egasining metodiga ko'chadi; saqlanishi shart public setter
  `@Deprecated`, o'chirish Ochiq qaror (36.12). Reja, dasturchi, review
  va retsept kartasida.

## 0.4.0 (2026-10-19)

- Eski kod refaktoringi alohida zanjirda (Feathers tartibi, architect
  34.1): opus ijro rejasi `metod_bormi.py --audit` ro'yxati bilan,
  `test-muhandis` xarakterizatsiya testi (eski kodda yashil), `dasturchi`
  bir harakat va test, `review` testlar o'zgarmaganini va audit sonlari
  kamayganini tekshiradi. Tez yo'l refaktoringda yopiq.
- `metod_bormi.py --audit`: ko'p yozuvchili maydon, takror blok, uzun
  metod; `refaktoring` belgisi va retsept kartasi.

## 0.3.1 (2026-10-19)

- `tools/metod_bormi.py`: metod yozishdan oldin shu ish bormi; muhim
  maydonni qaysi metodlar o'zgartiradi (`--ozgartiradi`).
- Holat bir teshikdan o'zgaradi (clean-code 16.6, patterns 26.16, 13.15):
  umumiy qoida, ijro rejasi va review mezoni; pul, balans, holat uchun
  majburiy; `check_code` entity dagi pul yoki
  holat maydonining public setterini ushlaydi (code-review 9.7).

## 0.3.0 (2026-10-19)

- Qaror opus da, ijro sonnet da: `rejalashtiruvchi` opus, har kod
  vazifasiga (Tez yo'ldan tashqari) 25 qatorgacha ijro rejasi beradi;
  `dasturchi`, `test-muhandis`, `review` sonnet da reja bilan ishlaydi.
  O'lchov: opus reja + sonnet kod minimal 9.2, takror 0 (opus yolg'iz
  8.5, sonnet yolg'iz 7.5).
- Review rejaning "yozilmaydi" ro'yxatini ham tekshiradi.
- Tez yo'l `rules_for --belgilar` dagi `tez_yol:` qarori bilan.
- DRY: "bir ish bitta metod" umumiy qoidada va kartalarda.
- Global o'rnatishda agentlardagi skill reference yo'li mutlaq.
- `usage.py`: katta sessiya fonda saqlanadi.

## 0.2.0 (2026-10-19)

- `dasturchi` opus da (0.3.0 da o'zgardi).
- Retsept kartalari (`tools/retsept/`): har belgiga eng kichik to'g'ri
  shakl, "allaqachon bor, yozmang" ro'yxati va tuzoqlar, bo'lim raqami bilan.
- Umumiy yozish qoidalari (`umumiy-kod.md`, `umumiy-test.md`): to'rt
  aktyor bir xil bilimni `rules_for` dan oladi; shartli bandlar faqat mos
  kodda chiqadi.
- `rules_for --vazifa`: fayl hali o'z ichiga olmagan mavzuning kartasi;
  vazifa kartasi birinchi. `--belgilar`: Tez yo'l qarori uchun qisqa chiqish.
- `qidiruv` va `tahlil` aktyorlari olib tashlandi.
- SKILL.md qisqardi (16 KB dan 12 KB); partiya ta'rifi; Tez yo'l vazifa
  belgilari bo'yicha; kod vazifasida nomzod bo'lim o'qilmaydi.
- Memory va hujjatlar `<workspace>/docs-local/` da, `.git/info/exclude`
  orqali git dan tashqarida; zaxira nusxa (`.bak`) yaratilmaydi.
- O'rnatuvchi: o'z skill va aktyor fayllarini zaxiralamaydi, eski
  zaxiralarni o'chiradi; `versiya.py` o'rnatilgan versiyani aytadi.
- `check_code`: takroriy import (`java:S1128`); yangi belgi xabari bir marta.
- Korpus: 222 bob odam tasdiqlagan (226 dan); kitob iqtiboslari betiga solishtirilgan.

## 0.1.0

- Birinchi versiya: olti hujjat, `manguberdi` orkestratori, hooklar.
