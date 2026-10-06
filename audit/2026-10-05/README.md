# claude-genius: o'z-o'zini tanqidiy baholash va takomil rejasi

**Natija.** Tizimning mexanizm qismi kuchli: hooklar tez va xavfsiz yiqiladi, asboblar faqat stdlib bilan yozilgan, coverage 88-96%. Lekin tizim beradigan ikki asosiy qiymat hali isbotlanmagan:

- **Korpus to'g'riligi isbotlanmagan.** 224 bobdan birortasini ham odam tekshirmagan. Xavfli da'voli 25 bo'limdan 6 tasida aniq faktik xato topildi.
- **Orkestrator foydasi o'lchanmagan.** A/B sinovi bir marta ham yurilmagan, tayyorlovida esa kritik nuqson bor. Hisob bo'yicha kichik bug zanjiri oddiy sessiyadan 2.5-4 baravar ko'p token sarflaydi (taxmin).

Bundan tashqari xavfsizlik chegarasi umuman chizilmagan:

- Global ruxsat ro'yxati begona repo yoki fork PR ning build kodini so'rovsiz yurgizadi.
- Threat model yo'q.
- Subagent ichida guard `ask` qaytarsa, zanjir cheksiz kutadi. Shu auditning o'zida bitta agent 6 soat 20 daqiqa qotib qoldi.

Tezlik muammosi hooklarda emas: ular sessiyaga ~0.4% vaqt qo'shadi. Vaqt zanjir uzunligiga, Maven yurishlari soniga, ketma-ket yuradigan test suitega (48 s) va CI ga (158 s) ketadi.

Reja 8 bosqichdan iborat:

1. Avval xavf va qizil CI yopiladi.
2. Keyin o'lchov to'g'rilanadi. Asosiy qoida: o'lchamasdan optimallashtirilmaydi.
3. So'ng tezlik, qidiruv, korpus va orkestrator ishlari o'lchov bilan qilinadi.

Sana: 2026-10-05. Baholangan commit: `8f47f42`, branch `ccr-bbd7652b-066u0n`. To'liq dalillar [topilmalar](#ilova-topilmalar-yonalish-boyicha) ilovasida.

## Mundarija

- [1. Qanday baholandi](#1-qanday-baholandi)
- [2. Umumiy baho](#2-umumiy-baho)
- [3. Asosiy xulosalar](#3-asosiy-xulosalar)
- [4. O'z-o'zimni tanqid: men qayerda xato qildim](#4-oz-ozimni-tanqid-men-qayerda-xato-qildim)
- [5. Saqlanadigan kuchli tomonlar](#5-saqlanadigan-kuchli-tomonlar)
- [6. Tekshiruvda rad etilgan yoki yumshatilgan da'volar](#6-tekshiruvda-rad-etilgan-yoki-yumshatilgan-davolar)
- [7. Reja](#7-reja)
- [8. Nima qilinmaydi](#8-nima-qilinmaydi)
- [9. Egasining qarori kerak bo'lgan joylar](#9-egasining-qarori-kerak-bolgan-joylar)
- [10. Muvaffaqiyat ko'rsatkichlari](#10-muvaffaqiyat-korsatkichlari)
- [11. Qamrov tanqidchisi topgan bo'shliqlar](#11-qamrov-tanqidchisi-topgan-boshliqlar)
- [Ilova: topilmalar yo'nalish bo'yicha](#ilova-topilmalar-yonalish-boyicha)

## 1. Qanday baholandi

Baholash 10 yo'nalishda olib borildi. Har yo'nalishda bitta auditor agent dalil yig'di: faylni o'qidi, buyruq yurgizdi, o'lchadi. Keyin alohida skeptik tekshiruvchi agent har topilmani rad etishga urindi. Dalilni takrorlay olmasa topilma rad etildi, mubolag'a bo'lsa og'irlik va tavsiya tuzatildi. Oxirida qamrov tanqidchisi nima o'tkazib yuborilganini qidirdi va bo'shliqlar bo'yicha qo'shimcha audit o'tkazildi ([11-bo'lim](#11-qamrov-tanqidchisi-topgan-boshliqlar)).

| Ko'rsatkich | Qiymat |
|---|---|
| Yo'nalish | 10 asosiy + 4 qamrov tanqidchisi topgan |
| Agent | 29: 10 auditor, 10 tekshiruvchi, 1 qamrov tanqidchisi, 4 + 4 bo'shliq auditor va tekshiruvchisi |
| Tasdiqlangan topilma | 240: kritik 1, yuqori 40, o'rta 106, past 93 |
| Asosiy 10 yo'nalishda tekshiruv natijasi | 34 o'zgarishsiz tasdiqlandi, 115 tuzatish bilan tasdiqlandi, 29 tasini tekshiruvchi o'zi qo'shdi |
| Rad etilgan | 4 (HK-H13, QD-Q13, PL-CC1, TL-TL13) |
| Subagent tokeni | ~6.0 mln |

O'lchov muhiti: Linux, 4 CPU, Python 3.11. Repo fayllari o'zgartirilmagan, hamma sinov scratchpad nusxasida qilingan. Haqiqiy Java proyekt sifatida A/B sinovidagi `spring-petclinic` (`500158f`) ishlatilgan.

Cheklovlar:

- Korpus faktlari tanlab tekshirildi: 25 ta xavfli da'voli bo'lim qo'lda ko'rildi. Mashina bilan esa 1477 java blok, 975 Spring kaliti, 2391 annotatsiya va 291 GUC ishlatilishi tekshirildi.
- Orkestrator narxi jonli sessiyada emas, fayllar va transkript o'lchovlaridan hisoblandi. Shuning uchun u "taxmin" deb belgilangan.

## 2. Umumiy baho

Baho 10 ballik va sub'ektiv, lekin har biri ilovadagi dalilga tayanadi.

| Yo'nalish | Baho | Bir qatorda nega |
|---|---|---|
| Korpus faktik sifati | 4 | Tuzilma va sintaksis yaxshi (88% java blok parserdan o'tadi), lekin 0 bob tekshirilgan, versiya bazasi Boot 3.x, xavfli bo'limlarning 24% ida xato |
| O'lchov va eval | 3 | Ichki eval 100%, lekin u tautologik. Held-out da rules_for 4/8, check_code 1/8. A/B kritik nuqsonli va yurilmagan |
| Orkestrator | 4 | Budjet, qulf va state puxta yozilgan. Lekin marshrut noaniq, `guruh.py` ish yo'qotadi, parallel rejim amalda ishga tushmaydi, foydasi o'lchanmagan |
| Qidiruv va taklif | 6 | Taxallus bo'yicha 97%. Realistik so'rovda hook 1-o'rinni 44% holatda topadi, ko'p so'zli `find` 0 qator beradi |
| Ish jarayoni | 4 | Commit xabarlari va DECISIONS namunali. Lekin commitlarning 46-59% i tuzatuvchi, CI kutilmaydi, kuch korpusdan asbobga ko'chgan |
| O'rnatish va CI | 4 | O'rnatuvchi qo'shuvchi va CI da sinalgan. Lekin sukut branch eski destruktiv o'rnatuvchini beradi, main qizil, himoya yo'q, Linux va macOS uchun yo'l yo'q |
| Asbob kodi | 7 | Stdlib, `shell=True` 0, ruff toza, coverage 88-96%. Non-ASCII yo'l xatosi bor, Windows qizil, yordamchi kod takrorlangan, testlar sekin |
| Hooklar va guard | 7 | 31-108 ms, fail-open, regex chidamli. Aylanib o'tish yo'llari va yolg'on to'siqlar bor, check_code qo'llanmaning o'z patternini block qiladi |
| Kontekst va ko'rsatmalar | 6 | Qat'iy kontekst o'lchanadi va CI da qo'riqlanadi. S/M/L uch xil ta'riflangan, qoidalar 3-5 joyda takrorlanadi, zahira 154 token |
| Hujjat tuzilmasi | 6 | Bo'lim darajasida o'qish to'liq ishlaydi, 6171 havola to'g'ri. 32 o'xshash juft o'zaro havolasiz, korpus holati kirish sahifalarida aytilmaydi |
| Xavfsizlik va ishonch chegarasi | 3 | `shell=True` va injection yo'q. Lekin global ruxsat begona build kodini yurgizadi, guard 21 halokatli yoki sir payloadidan 1 tasini ushlaydi (u narx to'sig'i, xavfsizlik emas), threat model yo'q |
| Platforma bilan shartnoma | 6 | Hook chiqishlari rasmiy maydonlarda va jonli sinalgan, narx jadvali rasmiyga mos. Minimal versiya yo'q, format o'zgarsa jim nol beradi, SendMessage budjetni aylanib o'tadi |
| Qo'llanish chegarasi | 4 | React Native va Flutter Java deb faollashadi. Ichki modulli monorepo jim qoladi, Kotlin tekshirilmaydi, Boot 2.7 proyektga Boot 3.4+ API tavsiya qilinadi |
| O'quvchi va til sifati | 5 | Bitta so'zning 3-4 yozilishi bor, Fowler va Martin kataloglarida manba ko'rsatilmagan, litsenziya fayli kanonik emas, fikr kanali yo'q |

**Umumiy baho: 5/10.** Poydevor yaxshi, qiymat isbotlanmagan, xavfsizlik chegarasi chizilmagan. Ish tartibi esa qiymatdan ko'ra asbob soniga xizmat qilgan.

## 3. Asosiy xulosalar

### 3.1 Qiymat o'lchanmagan, ichki o'lchov esa 100% ko'rsatadi

- `eval_skill.py` 31/31, 7/7, 19/19 beradi. Lekin kutilgan natijalar `rules_for.SIGNALS` jadvalining aynan nusxasi va ular bir commitda yozilgan (OL-O1).
- Held-out petclinic fayllarida esa natija past. rules_for kiritilgan 8 nuqsondan 4 tasiga mos bob beradi, check_code 8 tadan 1 tasini topadi (OL-O1, OL-O2).
- `eval_find` taxallus bo'yicha 97% ko'rsatadi. 45 ta realistik so'rovda esa hook 1-o'rinni 44%, top-3 ni 60% holatda topadi, aniqlik 41% (QD-Q1, OL-O3).
- A/B sinovi yurilmagan (OL-O10, OK-O15). Uning tayyorlovida bug javobi `git diff` da ochiq turadi (OL-O6, kritik). A holatini `manguberdi` o'zi ifloslantira oladi (KT-K3, OL-O8). Qaror qoidasining statistik kuchi esa tanga tashlashga yaqin (OL-O9).

### 3.2 Kuch mahsulotdan asbobga ko'chgan

- 26 soatda asbob soni 2 dan 27 ga, qoida bandlari ~172 ga yetdi (JR-J10).
- 112 commitdan 77 tasi `docs/` ga tegmagan. 0 bob tekshirilgan, kod misollari 1-kunda to'xtagan (JR-J11).
- Commitlarning 46% i o'z avvalgi asbob ishini tuzatgan, docs tuzatishlari bilan birga 59% (JR-J3).
- Bir agent bir vaqtda yozgan yashil testlar noto'g'ri javobni tutmagan: eski `parse_test_output` kompilyatsiya xatosida "test topilmadi, exit=0" bergan (JR-J3).

### 3.3 Korpusda haqiqiy xatolar bor va versiya bazasi eskirgan

Tasdiqlangan xatolar:

- Hibernate 7 da yo'q `@Where` va `@LazyCollection` (KR-Q4).
- Boot 4 BOM da yo'q Testcontainers artifactId lari, build yiqiladi (KR-Q5).
- Kompilyatsiya bo'lmaydigan ikki misol (KR-Q6).
- PostgreSQL 17 da yo'q SPLIT/MERGE PARTITION (KR-Q9).
- "Haqiqiy himoya" deb atalgan `read-only=false` (KR-Q10).
- Actuator haqidagi noto'g'ri tushuntirish (KR-Q8).
- JDK 16+ da ishlamaydigan Error Prone konfiguratsiyasi (KR-Q11).
- Payload noto'g'ri yozilgan XXE misoli (KR-T-K2).
- O'zi tuzatmoqchi bo'lgan xatoni qayta kiritgan entity (TZ-T-K3).

Bularning ostida tizimli sabab bor: korpus Boot 3.2-3.5 ga tayanadi. "Spring Boot 3" 256 marta uchraydi, "Hibernate 7" va "JUnit 6" esa 0 marta. "Boot 3.x+" ko'rinishidagi ochiq oraliq 76 joyda turibdi (KR-Q1, KR-T-K1).

1-to'lqin tekshiruvi 15 xato / 130 bo'lim berdi. Shu ulush bilan qolgan 3163 bo'limda ~290-365 xato kutiladi (taxmin, KR-Q3).

### 3.4 Ma'lumot yo'qotish va maxfiylik xavflari

- `guruh.py tozala --hammasi` birlashtirilmagan guruh ishini o'chiradi (OK-O1, repro ikki marta takrorlangan).
- Global o'rnatishda boshqa proyektlarning memory va handoff yozuvlari ommaviy repoga commit va push qilinadi (JR-J6, OC-K4, OK-T-K3).
- GitHub sukut branchi main dan 54 commit orqada va eski destruktiv o'rnatuvchini beradi (OC-K1).

### 3.5 main sog'lom emas

- main ga push qilingan runlarning 36% i qizil, ketma-ket 16 qizil run bo'lgan (JR-J5, OC-K2).
- HEAD da Windows tools job haqiqiy regressiya bilan qizil: `log_path` realpath ishlatmaydi (KD-T-M1, OC-T-Q1).
- Oxirgi 2 run runner topilmay bekor bo'lgan (OC-T-Q3).
- Branch protection yo'q.

### 3.6 Tezlik qayerda yo'qoladi

| Joy | O'lchov | Manba |
|---|---|---|
| Hooklar | 31-108 ms median, sessiyaga ~15 s (~0.4%) | HK-H15 |
| S zanjiri (bitta bug) | Oddiy sessiyadan ~2.5-4x token, ~2-3x vaqt (taxmin) | OK-O2 |
| M zanjiri | 3-5 aktyor chaqiruvi, rules_for 3 marta, Maven 3-5 marta | OK-O3 |
| Test suite | 48 s ketma-ket. test_doc 12 s, test_guard 6 s (144 Python jarayon) | KD-T1, KD-T2 |
| CI | 158 s, kritik yo'l Windows tools 154 s. Concurrency va paths filter yo'q | OC-K8, KD-T6 |
| Korpus tekshiruvi | ~11 daqiqa/bob, 219 bob uchun 18-40 soat agent va 28-44 soat odam vaqti | KR-Q3 |
| Subagentda guard `ask` | Javob beradigan odam yo'q, zanjir cheksiz kutadi: 6 soat 20 daqiqa kuzatildi | PL-T-M1 |

Xulosa: hooklarni optimallash sezilmaydi. Haqiqiy yutuq zanjir, test, CI va mashina tekshiruvida. Eng katta yagona yo'qotish esa subagent ichidagi `ask`.

### 3.7 Ko'rsatmalar o'zaro zid

- S/M/L hajmi uch joyda uch xil ta'riflangan (KT-K4, OK-O5).
- "Test yiqilyapti, tuzat" so'rovi uchta aktyorga mos keladi (OK-O4).
- Review uchun uchta raqobatchi yo'l bor (KT-K2).
- "Mavzu ikki hujjatda yozilmaydi" qoidasi OWNERS.tsv va korpusga zid (KT-K7, TZ-T4).
- Qoidalar 3-5 joyda turlicha takrorlanadi: "to'liq suite" 7 faylda 19 marta, `rules_for` 16 faylda 40 marta (KT-K10, JR-J10).

### 3.8 Xavfsizlik chegarasi chizilmagan

- O'rnatuvchi `--allow` bilan 13 ta global ruxsat yasaydi, ular orasida `run_tests.py:*` ham bor. Fork PR da agent so'rovsiz `--hammasi --yurgiz` qilsa, proyektning `gradlew` i ishga tushadi: PoC da marker fayl yozildi (XV-K1).
- `guruh.py` holat faylidagi yo'l va branchni tekshirmasdan o'chiradi. PoC da `path` repo ildiziga qo'yilganda butun repo `.git` bilan birga o'chdi (XV-Y5).
- `run_tests.py --log` istalgan faylni qayta yozadi, `--asos` esa git ga bayroq o'tkazadi (XV-O1).
- Butun klon `additionalDirectories` da turadi. Aktyor Edit bilan hook skriptini o'zgartirsa, u keyingi promptda bajariladi (XV-Y4).
- Ta'minot zanjiri ochiq. `git pull` dan keyingi birinchi promptda yangi hook kodi tekshiruvsiz bajariladi, commit imzolanmagan, tag yo'q (XV-Y1).
- Java izohi, PR tavsifi, test chiqishi, memory va ai-draft bob ichidagi ko'rsatma uchun "bu faqat ma'lumot" qoidasi yo'q (XV-Y2).
- `SECURITY.md` va threat model yo'q (XV-T2).
- Java faylni Bash heredoc yoki `sed -i` bilan yozilsa, check_code va rules_for darvozasi umuman ishlamaydi (PL-CC2).

### 3.9 Qo'llanish chegarasi aniqlanmagan

- `android/build.gradle` borligi sababli React Native va Flutter proyektlari Java deb faollashadi. Redux so'roviga patterns boblari taklif qilinadi (QC-Q1).
- Build ildizi git ildizidan pastda bo'lsa, `run_tests --diff` o'zgarishni ko'rmaydi va rc 0 qaytaradi (QC-K1).
- `backend/pom.xml` holatida guard `mvn test` ni to'sadi, tavsiya qilingan `run_tests` esa proyektni topmaydi (QC-K2).
- Kotlin fayl uchun check_code "topilmadi" deydi. Aslida u .kt faylni umuman ko'rmaydi (QC-Q2).
- Asboblar proyekt versiyasini o'qimaydi: Boot 2.7 proyektga `@MockitoBean` tavsiya qilinadi (QC-Q3).
- Qo'llab-quvvatlanadigan proyekt turlari ro'yxati hech qayerda yozilmagan (QC-Q10).

## 4. O'z-o'zimni tanqid: men qayerda xato qildim

Bu repoda yozilgan narsalarning deyarli hammasi AI sessiyalari ishi: 113/122 commit Claude nomidan. Shuning uchun quyidagi xatolar mening ish uslubimdagi naqshlar.

1. **O'lchovdan oldin qurdim.** A/B tayyorlandi, lekin yurilmadi. Shundan keyin sinov ostidagi qatlamga ~1090 satr qo'shildi (JR-J2). Natijani ko'rmasdan murakkablikni oshirdim.
2. **O'z kodimni o'z testim bilan tasdiqladim.** Eval kutilmalari implementatsiya bilan birga yozildi va 100% chiqdi (OL-O1). Yashil testlar haqiqiy formatdagi xatoni tutmadi (JR-J3).
3. **CI ni kutmadim.** main ga to'g'ridan-to'g'ri push qildim, 16 ketma-ket qizil run checkpoint commitlardan bo'ldi (JR-J5).
4. **Oson ishni tanladim.** Asbob yozish o'lchanadigan va tez ko'rinadi. Korpus tekshiruvi esa sekin va zerikarli. Natijada 0 bob tekshirildi (JR-J11).
5. **Qoida ustiga qoida qo'ydim.** Har muammoga yangi qoida yoki asbob yozdim, eskisini olib tashlamadim. Natijada bir qoida 3-5 joyda turlicha yashaydi (JR-J10, KT-K10).
6. **Xavfli sukut qiymatlarni ko'rmadim.** Ommaviy repoga xususiy memory push qilinishi, birlashmagan ishni o'chiradigan `tozala --hammasi` va sukut branchdagi destruktiv o'rnatuvchi shunday chiqdi (JR-J6, OK-O1, OC-K1).
7. **Shu sessiyaning o'zida ham xato qildim.** Uchta holat bo'ldi:
   - Workflow hali ishlayotganida uning tugaganligi haqidagi bildirishnomani o'zim yozib qo'ydim, keyin tekshirib tuzatdim. Bu "natijani tekshirmasdan da'vo qilish" naqshining aynan o'zi.
   - Birinchi workflowni konteynerdagi CPU sonini tekshirmasdan ishga tushirdim. Bir vaqtda faqat 2 agent yurar ekan, shuning uchun ishni to'xtatib, to'rtta workflowga bo'lib qayta yurgizdim.
   - Audit agentlariga `ask` beradigan buyruq (psql, docker) yurgizmaslikni aytmadim. Bitta agent 6 soat 20 daqiqa javobsiz kutib qoldi.

   Saboq: har da'vo fayl yoki chiqish bilan tasdiqlanadi. Ishga tushirishdan oldin muhit cheklovi o'lchanadi.

Tuzatish yo'li har birida bitta: avval o'lchov va mustaqil tekshiruv, keyin o'zgarish. Bu [8-bosqich](#bosqich-8-ish-tartibi-qoidalari-hamma-bosqichga) qoidalarida mexanizm sifatida yozilgan.

## 5. Saqlanadigan kuchli tomonlar

Reja bularni buzmasligi kerak.

- **Hook mexanikasi.** `hookio.py` BOM, cp1252 va buzuq JSON ni to'g'ri ushlaydi va toza fail-open beradi. `GENIUS_HOOKS=off` ishlaydi. Hooklar faqat klon va Java proyektida faol (HK kuchli tomonlari).
- **guard regexlari.** Catastrophic backtracking ga chidamli, qo'shtirnoq va heredoc ichidagi matnni to'g'ri chiqarib tashlaydi. Read da baytni sanaydi.
- **budget.py.** `tool_use_id` dedupe, O_EXCL qulf, atomik yozuv. Parallel 6 chaqiruvda aniq 2 tasini o'tkazadi.
- **Asbob kodi.** Faqat stdlib, `shell=True` 0, ruff default 41 topilma (30 tasi E741). Coverage: guard 96%, rules_for 95%, run_tests 88%, install 89%.
- **Bo'lim darajasida o'qish.** 3293 bo'limdan birortasi 16 KB dan katta emas (max 5.6 KB). 6171 nisbiy havola va anchor tekshiriladi. 224 bobning hammasi kamida bitta skillga marshrutlangan.
- **Halollik mexanizmlari.** Har bobda holat qatori bor, `doc.sh show` va `rules_for` `[tekshirilmagan]` belgisini chiqaradi. `known_errors.tsv` dagi 22 naqsh tuzatilgan xatoni qaytarmaydi. Sonar kalitlari rasmiy metadata bilan solishtiriladi.
- **Mashina tekshiruvi uchun tayyor poydevor.** GUC nomlarida 0 xato (291 ishlatish). Java bloklarining 88% i parserdan o'tadi. Annotatsiyalarning 204/253 tasi Boot 4.1 jarlarida bor.
- **O'rnatuvchi.** Sukut bo'yicha qo'shuvchi, sinov yig'imi, zaxira, PowerShell 5.1 va 7 da CI. Python mantiqi Linux da ham ishlaydi.
- **Qaror yozuvlari.** DECISIONS.md rad etilgan variantlar va orqaga qaytarish yo'lini yozadi, commit xabarlari "nega" va raqam bilan.
- **Qisqartira olish.** Memory qoidasi 43 KB dan 2.8 KB ga, 80 KB lik reja skilli olib tashlandi, o'zini o'zi ochadigan to'siq olib tashlandi.

## 6. Tekshiruvda rad etilgan yoki yumshatilgan da'volar

Skeptik tekshiruvchi auditorning ba'zi da'volarini rad etdi yoki yumshatdi. Rejaga faqat tuzatilgan shakli kirdi.

- **HK-H13 rad etildi.** "Matcher langarsiz regex bo'lsa ortiqcha toollarda ham hook yuradi" degan da'vo noto'g'ri. Claude Code `A|B` shaklidagi matcherni aniq tenglik bilan solishtiradi.
- **QD-Q13 rad etildi.** DECISIONS.md dagi qidiruv raqamlari bugungi o'lchov bilan mos keldi.
- **PL-CC1 rad etildi.** Auditor "auto rejimda guard `ask` odamsiz o'tib ketadi" degan edi. Transkript buning teskarisini ko'rsatdi: `ask` 6 soat 20 daqiqa javob kutdi. Bu kuzatuv yangi topilma bo'ldi (PL-T-M1).
- **TL-TL13 rad etildi.** U TZ-T10 ning to'liq takrori.
- **Stop hookka `async: true` zararli (PL-CC12).** `-p` rejimida async hook sessiya yopilganda o'ldiriladi va oxirgi navbat sarfi yozilmaydi. Shuning uchun HK-H6 dagi bu tavsiya rejaga kirmadi.
- **`|| exit 0` uchun oddiyroq yechim (PL-CC11).** Rasmiy hujjatga ko'ra 2 dan boshqa nol bo'lmagan kod to'smaydi, faqat "hook error" ko'rsatadi. Demak `|| exit 1` yetadi, HK-H2 dagi chiqish kodini almashtirish va log zanjiri shart emas.
- **"Aktyor bazasi ~51k token" oshirilgan.** Bu raqam MCP asboblari to'liq bo'lgan workflow subagentidan olingan. Cheklangan asbobli aktyorda baza ~17-20k token (OK-O2 tekshiruvi). Xulosa, ya'ni S zanjiri 1.5x shartidan o'tmasligi, saqlanadi.
- **Hook latency muammo emas.** Hook keshi va birlashtirish bo'yicha topilmalar "past" ga tushirildi. 40 ms model navbati oldida sezilmaydi (QD-Q8, HK-H15).
- **"Tekshiruv to'xtagan" degan xulosa asossiz.** Repo 2 kunlik va tekshiruv jarayoni 16:48 da yaratilgan (KR-Q3). O'tkazuvchanlik muammosi esa haqiqiy.
- **Bir nechta tavsiya zararli deb topildi va tuzatildi:**
  - `clean` ni umumiy `ask` qilish. Bunda `mvn clean install` ham ochilib qoladi (HK-H12).
  - `start_new_session=True`. Bu yetim build qoldiradi (KD-Q10).
  - Refaktoringda test-muhandisni dasturchidan oldinga qo'yish. Bu A/B mezonini buzadi (OK-O6).
  - Worktree ni `.gitignore` orqali yashirish. Buning o'rniga `.git/info/exclude` ishlatiladi (OK-O13).
  - `/` li tokenlarni tashlash. Bu to'g'ri javoblarni o'chiradi (QD-Q12).
  - Umumiy o'zbekcha stemming. Bu holdout natijasini yomonlashtiradi (QD-Q10).

## 7. Reja

### Tartib va bog'liqlik

```text
Bosqich 0 (xavf, xavfsizlik, qizil CI)  ->  Bosqich 1 (o'lchov)  ->  Bosqich 2 (tezlik)
                                         |              ->  Bosqich 3 (qidiruv)
                                         |              ->  Bosqich 5 (orkestrator, A/B natijasiga qarab)
                                         |              ->  Bosqich 6 (hook aniqligi, qo'llanish chegarasi)
Bosqich 4 (korpus) 0-bosqichdan keyin boshlanadi va uzoq davom etadi
Bosqich 7 (tarqatish, platforma, SECURITY.md) 0-bosqichdan keyin, mustaqil
Bosqich 8 (ish tartibi qoidalari) darhol va hamma bosqichga
```

Muddatlar agent sessiyasi kunida va taxminiy. Har vazifa uchun:

- "Qabul" - tugaganini qanday tekshirish.
- "Asos" - ilovadagi topilma ID si.
- Mehnat: S (bir necha soat), M (1-2 kun), L (bir necha kun yoki davomiy).

### Bosqich 0. Xavf, xavfsizlik va qizil CI (2-3 kun)

Maqsad: ma'lumot yo'qotish, maxfiylik, xavfli ruxsatlar, cheksiz kutish va buzuq main ni yopish. Bu bosqichda yangi imkoniyat qo'shilmaydi.

**R0.1 main ni yashilga qaytarish (S).**
- Nima o'zgaradi: `tools/run_tests.py` dagi `log_path()` va `project_root()` fallbacki `os.path.realpath` ishlatadi. `test_run_tests.py` ga symlink orqali ochilgan root holati qo'shiladi, u Windows 8.3 taxallus regressiyasini Linux da ushlaydi.
- Runner muammosi uchun: `docs.yml` ga `workflow_dispatch:` qo'shiladi. Egasi Actions billing va limitni tekshiradi.
- Qabul: main HEAD da 5 job yashil.
- Asos: KD-T-M1, OC-T-Q1, OC-T-Q3, KD-Q1.

**R0.2 Sukut branch main ga (S, egasi).**
- Nima o'zgaradi: GitHub sozlamasida default branch `main` qilinadi. `install/README.md` boshiga bitta qator: eski o'rnatuvchi ishlatilgan bo'lsa `install/restore_backup.py`. Eski branch egasi tasdiqlasa o'chiriladi.
- Qabul: `default_branch = main`. Yangi klonda `install/restore_backup.py` bor. Repo sahifasidagi README "224 bob" deydi va bob fayllarining 5-qatorida "Holat:" turadi.
- Asos: OC-K1, TL-TL1.

**R0.3 `guruh.py` ish yo'qotmasin va begona narsani o'chirmasin (S).**
- Nima o'zgaradi:
  - `remove()` birlashtirilmagan va o'zgarishi bor guruhni rad etadi (rc=1, fayllar ro'yxati, `--majburiy` talab qilinadi).
  - `tozala --hammasi` faqat birlashgan yoki bo'sh guruhlarni oladi.
  - `--3way` yiqilsa `merged=True` qo'yilmaydi.
  - O'chirishdan oldin yo'l va branch tekshiriladi, biri buzilsa rc=2 qaytadi va hech narsa o'chmaydi:
    - `path == worktree_path(root, gid)`;
    - yo'l `git worktree list` da bor;
    - yo'l repo ildizi emas;
    - branch `^genius/[\w.-]{1,40}$` ga mos.
  - `create()` yiqilsa worktree va branch qaytariladi. `--nusxa` da mutlaq yo'l va `..` rad etiladi.
  - `parallel.md` da tozalash faqat `birlashtir` 0 qaytargandan va to'liq suite natijasidan keyin.
  - `test_guruh.py` ga uch holat: kesishgan guruh, budjeti tugagan guruh, buzilgan holat fayli.
- Qabul: repro skriptida `tozala --hammasi` dan keyin billing ishi saqlanadi va rc != 0. Holat faylida `path` repo ildiziga qo'yilsa ham hech narsa o'chmaydi.
- Asos: OK-O1, OK-T-K1, XV-K2, XV-Y5, XV-O6.

**R0.4 `run_tests --diff` non-ASCII yo'lni ko'rsin (S).**
- Nima o'zgaradi:
  - `changed_files()` da `git diff --name-status -z --relative` va `ls-files -z`. `--relative` build ildizi git ildizidan pastda bo'lgan holatni yopadi.
  - `run_git` ga `encoding='utf-8', errors='surrogateescape'`.
  - Diffda fayl bor, lekin `--ildiz` dan tashqarida bo'lsa, "N fayl hisobga olinmadi" eslatmasi chiqadi.
- Qabul: `V2__qoʻshimcha_ustun.sql` o'zgarganda migratsiya testi tanlanadi. `--ildiz backend --diff` monorepoda `OrderServiceTest` ni tanlaydi. Yangi holatlar yashil.
- Asos: KD-K1, KD-Q3, QC-K1.

**R0.5 Xususiy memory ommaviy repoga tushmasin (M).**
- Nima o'zgaradi:
  - Global o'rnatishda proyekt memorysi va handoff klondan tashqarida turadi. Joy `GENIUS_MEMORY_DIR`, sukut bo'yicha `~/.claude/genius-memory/<slug>/`, push siz.
  - Klonga faqat `memory/umumiy/` va `memory/claude-genius/` yoziladi.
  - Memory git buyruqlari `git -C <memory ildizi>` bilan yuradi.
  - `guard.py` begona slug ni `git add` yoki `git commit` qilishda `ask` beradi.
  - Yangi qoida DECISIONS.md ga yoziladi.
- Qabul: o'rnatilgan skill matnida `<klon>/memory/<proyekt-slug>` 0 marta. `test_guard` da begona slug commiti `ask`.
- Asos: JR-J6, OC-K4, OK-T-K3, OC-T-Q2, XV-Y3.

**R0.6 check_code yolg'on block bermasin (M).**
- Nima o'zgaradi:
  - Tranzaksiya tekshiruvi `afterCommit`/`afterCompletion` bloklarini va `@TransactionalEventListener` ni istisno qiladi.
  - `HttpClient.Version` kabi tur nomi chaqiruv deb sanalmaydi.
  - Edit da `originalFile` dagi eski topilmalar block bermaydi, faqat yangi topilma block beradi.
  - Uchta yangi fixture qo'shiladi.
- Qabul: `TxAfterCommit.java` 0 topilma. Eski topilmali faylga aloqasiz Edit da block yo'q. `test_check_code` yashil.
- Asos: HK-H1, HK-T-M1.

**R0.7 Korpusdagi tasdiqlangan xatolarni tuzatish (M).**
- Nima o'zgaradi: quyidagi bo'limlar tuzatiladi va har xato `tools/known_errors.tsv` ga naqsh bo'lib tushadi.
  - code-review 23.8 va 23.10 (`@SQLRestriction`, `@SoftDelete`).
  - testing 8.2 va 8.6 (TC 2 artifactId lari ikki variantda).
  - architect 13.2, code-review 36.4 (kompilyatsiya).
  - code-review 21.7, 21.8 (actuator `show-values`).
  - architect 26.5 (PG 17).
  - architect 19.5 (read-only).
  - clean-code 25.10 (Error Prone `--add-exports`).
  - architect 12.7, 12.8, 10.4 (aniqlik).
  - sonarqube 26 (XXE), 10.6 (JaCoCo goal), 41.5 (entity).
  - patterns 23 (FQN), patterns 6.2 va architect 32.2 (eskirgan kalitlar).
  - architect 17.8 (RFC 9457).
  - patterns 25.31 (Kotlin va Lombok final metod: `kotlin("plugin.spring")`).
  - code-review 14.3: "`BigDecimal.valueOf(0.1)` ham xavfli" degan noto'g'ri ogohlantirish (clean-code 20 ga zid) va int overflow misoli (`100_000 * 50_000` manfiy emas).
  - code-review 13.7: `grep -c ... | wc -l` so'z sonini emas, fayl sonini sanaydi.
  - testing 7.13 (`@MockitoBean` uchun "Boot 3.4+" belgisi).
- Qabul: `check_docs.py` yashil. Har tuzatishda manba URL tag ga qadalgan.
- Asos: KR-Q4..Q11, KR-Q15, KR-Q16, KR-T-K2, KR-T-K3, TZ-T-K1, TZ-T-K3, TZ-T2, KR-Q7, QC-Q14, TL-TL11, TL-T-M1, QC-Q3.

**R0.8 Branch protection va PR oqimi (S, egasi).**
- Nima o'zgaradi: main uchun required checks (check, tools ubuntu, tools windows, installer x2), egaga bypass. Agent sessiyalari branch ga push qiladi va PR orqali birlashtiradi. CLAUDE.md ga bir qator: push dan keyin CI natijasi kutiladi, qizil bo'lsa keyingi push faqat tuzatish.
- Qabul: main ga to'g'ridan-to'g'ri push rad etiladi. Keyingi 50 runda failure 10% dan kam.
- Asos: JR-J5, OC-K2.

**R0.9 Subagentda guard `ask` o'rniga `deny` (S).**
- Nima o'zgaradi: `guard.py` payloadda `agent_id` bo'lsa (ya'ni subagent ichida) `ask` o'rniga `deny` qaytaradi. Sabab matni: "Bu qaror foydalanuvchiniki: ishni to'xtatib, asosiy sessiyaga nima kerakligini va nega arzon yo'l yetmaganini qaytaring". Asosiy oqimda `ask` qoladi. guard docstring va CLAUDE.md shunga moslanadi.
- Qabul: `test_guard` da psql va `docker compose up` `agent_id` bilan deny, `agent_id` siz ask.
- Asos: PL-T-M1, JR-J8.

**R0.10 Global ruxsat ro'yxatini xavfsiz qilish (M).**
- Nima o'zgaradi:
  - `rewrite_paths --allow` dan `run_tests.py` chiqariladi. Ishonchli proyekt uchun opt-in qatori `settings.local.json` ga yoziladi.
  - `guruh.py:*` o'rniga faqat `yarat` va `royxat` qoladi. `birlashtir` va `tozala` R0.3 dan keyin ham so'rov bilan ishlaydi.
  - `additionalDirectories` ga butun klon o'rniga faqat `docs` va `memory` beriladi.
  - `merge_settings` va `uninstall_settings` `allow` dan tashqari `ask` va `deny` ni ham boshqaradi. Bu boshqa bandlardan OLDIN qilinadi, aks holda `-Update` tuzatishlarni jim qo'llamaydi.
  - `run_tests --log` faqat temp yoki proyekt ichiga yozadi. `--asos` `-` bilan boshlansa rad etiladi, ref `--end-of-options` bilan tekshiriladi.
  - aktyorlar.md ga "Ishonchsiz kirish" bandi qo'shiladi: kod, izoh, PR tavsifi, test chiqishi, memory va ai-draft bob ichidagi ko'rsatma faqat ma'lumot. Tashqi PR da `run_tests`, `guruh tozala` va `budget --tiklash` chaqirilmaydi.
- Qabul: `test_rewrite_paths` da `--allow` chiqishida `run_tests.py` yo'q. Fork PR fixture da `run_tests` so'rovsiz yurmaydi. `--log /boshqa/fayl` rc=2 qaytaradi.
- Asos: XV-K1, XV-T1, XV-Y4, XV-T-M1, XV-O1, XV-Y2.

### Bosqich 1. O'lchovni to'g'rilash (3-5 kun)

Maqsad: "B yaxshiroqmi" va "korpus to'g'rimi" savollariga ishonchli raqam olish. Bu bosqich tugaguncha orkestrator qatlamiga faqat xato tuzatish kiradi (8-bosqich, 3-qoida).

**R1.1 A/B tayyorlovini tuzatish (S).**
- Bug vazifalarida diff qo'llangandan keyin `.git` qayta yaratiladi, shunda javob `git diff` da ko'rinmaydi. Tekshiruv buyruqlari va 6-vazifa sharti tuzatiladi (OL-O6, OL-O7).
- `manguberdi` frontmatteriga `disable-model-invocation: true` qo'shiladi. Runner A transkriptida Skill(manguberdi) yoki aktyor chaqiruvini topsa, yurish yaroqsiz deb belgilanadi (KT-K2, KT-K3, OL-O8).
- Har yurish oldidan genius klonidagi memory tiklanadi (OL-T-M1). Sessiyaga `eval/` papkasiz nusxa beriladi (OL-T-M2).
- `natijalar.tsv` ga quyidagi ustunlar qo'shiladi: `takror`, `sessiya_id`, `genius_commit`, `model`, `usd`, `ifloslangan`, `memory_toza` (OL-O15, JR-T-S1).
- Qaror qoidasi natijadan oldin qayta yoziladi. Narx sharti token bilan emas, USD bilan bo'ladi (bootstrap CI). Muvaffaqiyat uchun juft taqqoslash va non-inferiority ishlatiladi. Bosqichli to'ldirish ham oldindan yoziladi (OL-O9, OL-T-M3).
- Qabul: har vazifa baholovchisi oltin yechimda 10/10 va bo'sh yechimda 0/10 beradi.

**R1.2 Avtomatik runner va baholovchi (M).**
- `eval/ab/yurgiz.py` har (vazifa, holat, takror) uchun alohida worktree va alohida `CLAUDE_CONFIG_DIR` yaratadi. Ishga tushirish: `claude -p --output-format json --max-budget-usd <chek>`.
- Ruxsat ikki holatda bir xil bo'ladi: izolyatsiyalangan nusxada `bypassPermissions` yoki bir xil `--allowedTools` ro'yxati. `acceptEdits` print rejimida so'rovlarni rad etadi, shuning uchun u ishlatilmaydi.
- `eval/ab/baho.py` mexanik tekshiruvni (testlar, diff, maqsadli fayllar) va ko'r LLM hakamni birlashtiradi.
- Ketma-ketlik: avval smoke (3 vazifa x 2 holat x 1), keyin 10 x 2 x 3.
- Runner Claude Code sessiyasi ichidan emas, foydalanuvchi terminalidan `env -u CLAUDE_CODE_SESSION_ID` bilan yuradi. Aks holda sessiya id si meros bo'lib, budjet va usage aralashadi (PL-CC10).
- Qabul: smoke natijasi `natijalar.tsv` da. To'liq yurish narxi oldindan chek bilan cheklangan.
- Asos: OL-O10, OK-O15, OL-O11.

**R1.3 Held-out to'plamlar (M).**
- `tools/testdata/heldout/`: petclinic dan 30 main va 20 test fayl (Apache-2.0) va `labels.tsv`. `labels.tsv` ni SIGNALS ni ko'rmagan sessiya yozadi. SIGNALS dagi arzon tuzatishlar: `Repository<`, `@MappedSuperclass`, FQN `@Transactional` (OL-O1).
- check_code uchun nol-FP qoidalar: `private` metoddagi `@Transactional`, static `SimpleDateFormat`. Held-out mexanik recall maxraji faqat mexanik aniqlanadigan nuqsonlar (OL-O2).
- `tools/testdata/find_golden.tsv` va `prompts_golden.tsv`: kamida 100 qator, 40 dan ortig'i holdout. Kategoriyalar: o'zbekcha erkin gap, inglizcha, aralash, xato yozilgan, Sonar, stack trace, kod parchasi. Holdout ga qarab hech narsa sozlanmaydi (QD-Q1, OL-O3, OL-O5).
- `eval_find` B namunasi xesh asosida olinadi, chegara "bazaviy minus 3 so'rov" (OL-O4, QD-Q9).
- Qabul: har eval ikki raqam chiqaradi, dev va holdout. CI dagi eval qismi 30 s dan oshmaydi.

**R1.4 Review va skill tanlash evali (M, haftada ko'pi bilan bir marta, qo'lda).**
- `eval/review/`: 12 diff, shundan 4 tasi toza refaktoring. `claude -p --agent review` k=3 marta yuradi. Recall va toza difflardagi yolg'on topilma sanaladi (OL-O13).
- `eval/trigger.tsv`: 30 prompt. Birinchi Skill tool_use nomi va birinchi aktyor sanaladi (KT-K5, OK-O4).
- Qabul: bazaviy qiymat yozilgan. Marshrut 30 tadan kamida 27 tasida to'g'ri.

**R1.5 Haqiqiy proyektda dogfood (M).**
- `schema_from_entities.py`: `@OneToMany` + `@JoinColumn` bo'lsa FK maqsad jadvalga yoziladi va soxta "mappedBy yo'q" topilmasi chiqmaydi.
- `run_tests.py`: `--asbob maven|gradle` va `GENIUS_BUILD_TOOL`. Gradle "What went wrong" blokidan sabab olinadi. Maven xulosasidagi test soni oxirgi `Tests run:` qatoridan olinadi.
- Haqiqiy loglar `tools/testdata/real/` ga manbasi bilan qo'yiladi.
- Qabul: petclinic da sxema `schema.sql` ustunlariga mos. bug-1 da run_tests birinchi sababi to'g'ri.
- Asos: JR-J1, JR-J13, JR-J3.

**R1.6 Sessiya monitoringi va narx to'g'riligi (S).**
- `usage.py --sessiya <id> --json` qo'shiladi. Sessiya blokida faqat bir ma'noli maydonlar bo'ladi: USD, faol daqiqa, tool soni nom bo'yicha, aktyor soni, guard va check_code to'siqlari soni.
- Stop hook yozgan `.claude/usage` yig'masi hisobotda o'qiladi. Hozir uni hech kim o'qimaydi, transkript esa 30 kunda o'chadi (PL-CC9).
- `price_for` faqat aniq model kalitini qabul qiladi. Noma'lum versiya jimgina eski narxda hisoblanmaydi, "narxsiz" deb belgilanadi (PL-CC5). Jadvalda `PRICES_AS_OF` va manba saqlanadi (PL-CC6).
- Transkript formati o'zgarsa, jim nol o'rniga "FORMAT O'ZGARGAN" ogohlantirishi chiqadi (PL-CC3).
- Stop hook `async` qilinmaydi (PL-CC12). Hozirgi 0.1-0.2 s sezilmaydi.
- Qabul: `usage.py --hafta` mediana $/sessiya ni beradi. `price_for('claude-opus-5-6')` None qaytaradi. Transkript o'chirilgandan keyin ham `--hammasi` jami o'zgarmaydi.
- Asos: OL-O11, OL-O12, OL-O14, PL-CC3, PL-CC5, PL-CC6, PL-CC9, PL-CC12.

### Bosqich 2. Tezlik (3-4 kun, 1-bosqich bilan parallel)

**R2.1 Test suite 48 s dan 15 s gacha (M).**
- `test_guard` va `test_check_code` jarayon ichida yuradi, faqat 6-8 E2E holat subprocess bilan qoladi (KD-T1, HK-H7).
- `test_doc` mini korpusda yuradi, `check_exact_refs` parallel bo'ladi (KD-T2).
- `--vaqt` float bo'ladi, git repo shabloni bitta (KD-T4).
- `test_budget` da `sleep(0.3)` o'rniga stdout handshake. Parallel takror kamaytirilmaydi (KD-T5).
- `tools/testkit.py`: `-k` filtr va sekin holat vaqti (KD-Q11).
- Qabul: lokal ketma-ket yurish 25 s dan, parallel yurish 15 s dan oshmaydi. Holatlar soni kamaymaydi.

**R2.2 CI 158 s dan 90 s gacha (S).**
- `concurrency: cancel-in-progress` qo'shiladi.
- Paths filter: faqat docs o'zgarsa installer va Windows tools job qisqa yo'ldan o'tadi. Required check nomlari saqlanadi.
- Windows da `eval_find` faqat qidiruv fayllari o'zgarganda yuradi.
- Indeks bir marta yasaladi, testlar `-P 4` bilan yuradi.
- `permissions: contents: read` qo'shiladi, actions yangi majorga o'tadi.
- Qabul: oddiy commitda run 90 s dan, faqat docs commitida 45 s dan oshmaydi. Bir SHA uchun takroriy run yo'q.
- Asos: OC-K8, KD-T6, OC-K10, OC-K12.

**R2.3 `check_docs` 2.8 s dan 2.1 s gacha (S).**
- Kirill tekshiruvi `for c in set(text)` bo'ladi.
- Qabul: natija bir xil.
- Asos: KD-Q6.

**R2.4 Qat'iy kontekst 6346 tokendan ~4800 tokenga (S).**
- Ketma-ketlik:
  1. CLAUDE.md dan takror olib tashlanadi: "Boshqa asboblar" katalogi references ga ko'chadi, model taqsimoti va docker ro'yxati bir qatorga qisqaradi.
  2. `manguberdi` listing dan chiqadi (`disable-model-invocation`).
  3. `cost_report` byudjeti "yangi JAMI + 300" ga tushadi.
  4. Faqat shundan keyin skill tavsiflariga o'zbekcha triggerlar qo'shiladi.
- Qabul: `cost_report` JAMI 5000 tokendan oshmaydi, zahira 200-400.
- Asos: KT-K1, KT-K2, KT-T-Q3, KT-K12.

**R2.5 Zanjirni qisqartirish (M, R1.2 smoke dan keyin, tajriba sifatida).**
- Tez yo'l: hajm S va rules_for belgilarida tranzaksiya, xavfsizlik, migratsiya, sozlama va parallel yo'q bo'lsa, asosiy sessiya o'zi bajaradi: rules_for -> Edit -> `run_tests --diff --yurgiz`. Review faqat xavf belgisi bo'lsa yoki diff 40 qatordan katta bo'lsa chaqiriladi (OK-O2).
- M zanjirida Maven yurishlari 3 tagacha kamaytiriladi: oxirgi yurish to'liq bo'lsa va keyin kod o'zgarmagan bo'lsa, alohida `--hammasi` yurmaydi (OK-O3).
- Cheklov test o'zgarishini taqiqlasa, test-muhandis chaqirilmaydi va S da regressiya testi yozilmaydi (OK-T-K2, OK-O11).
- Qabul: smoke da S vazifa uchun token_B/token_A 1.5 dan, asbob chaqiruvi 7 tadan oshmaydi, muvaffaqiyat A dan past emas.

**R2.6 rules_for shovqinini kamaytirish (M).**
- `checklist.tsv` ga `doira` ustuni qo'shiladi (kod | loyiha). `rules_for` faqat kod punktlarini chiqaradi, loyiha punktlari `doc.sh checklist` da qoladi. Memory feedback lari belgi bo'yicha filtrlanadi.
- Qabul: 5 testdata faylida loyiha punkti 2 tadan oshmaydi, `Bad.java` chiqishi 2.6 KB dan oshmaydi, eval_skill yashil.
- Asos: JR-J14, KT-T-Q2, OK-O8.

**R2.7 Hook mikro-optimallash (S, ixtiyoriy, eng oxirida).**
- `suggest_sections` korpus qismini oldindan yasalgan keshdan o'qiydi. Tejash ~37 ms.
- Global o'rnatishda Java bo'lmagan proyekt uchun shell prefiltr qo'shiladi. Tejash ~35 ms.
- `check_code` .java bo'lmagan yozuvda importdan oldin chiqadi.
- Qabul: `bench_all` qayta yurgiziladi, natija o'zgarmaydi.
- Asos: HK-H8, QD-Q8, KD-T3, HK-H9, HK-H11.

### Bosqich 3. Qidiruv sifati (3-5 kun, R1.3 dan keyin)

Har o'zgarish R1.3 dagi holdout to'plamda o'lchanadi. Holdout yomonlashsa o'zgarish qaytariladi.

**R3.1 `doc.sh find` ko'p so'zli so'rov (M).**
- Natija bo'sh va so'rovda kamida 2 so'z bo'lsa, so'zlar bo'yicha AND/IDF fallback ishlaydi. Fallback Python yordamchida, `suggest_sections` tokenizatori bilan yoziladi.
- Aniq moslik so'z chegarasidan, so'z chegarasi esa substringdan yuqori turadi. Transliteratsiya qo'shiladi: `tion->tsiya`, `ic->ik`, `c->k` va kichik inglizcha-o'zbekcha jadval.
- Qabul: "optimistic locking", "transaction propagation", "thread safety" topiladi. "kesh" so'rovida "Bikeshedding" 1-o'rinda chiqmaydi. A 1-o'rin 116 dan kam emas.
- Asos: QD-Q4, OL-O3, QD-T-M1, QD-Q11.

**R3.2 Hook kirishini tozalash (S).**
- `ʻ` va `’` belgilari `'` ga keltiriladi.
- FQCN oddiy nomga aylantiriladi.
- Yopishtirilgan Java kodda zaxira so'zlar tashlanadi.
- Prefikssiz Sonar kaliti (`S1192`) taniladi.
- Teng balda alifbo o'rniga max-idf hal qiladi.
- Qabul: `yoʻqolgan yangilanish muammosi` -> architect 22.5. Kod parchasi uchun begona bo'lim chiqmaydi. `test_suggest` yashil.
- Asos: QD-Q7, QD-Q2, QD-T-M2, QD-Q3, QD-Q6.

**R3.3 Exception va Sonar indeksi (M).**
- `index/exceptions.tsv`: nomlar faqat kod blokidan tashqarida va sarlavhada olinadi, umumiy istisnolar chiqariladi.
- Sonar katalog bo'limlarining birinchi qatoriga kalit yoziladi. `check_docs` katalogdagi har kalitning bo'limda borligini tekshiradi.
- Qabul: stack trace kategoriyasida topildi 1/5 dan kamida 4/5 ga chiqadi. `doc.sh rule S1192` 27.8 ni beradi.
- Asos: QD-Q2, QD-Q3.

**R3.4 Uy-bob va taxalluslar (M).**
- OWNERS.tsv qatorlari `aliases.tsv` ga `kind=uy` bilan yoziladi va `find` uy-bobni birinchi qo'yadi.
- OWNERS ga naqsh ustuni (o'zbekcha shakllar bilan) qo'shiladi.
- Magic number uyi tuzatiladi.
- Boshqa hujjatlar uchun inglizcha taxalluslar `docs/<hujjat>/aliases.tsv` da yoziladi.
- Qabul: 12 OWNERS mavzusining 12 tasida uy-bob top-3 da. "topilmadi" 3 dan 0 ga tushadi.
- Asos: TZ-T3, TZ-T-K2, TZ-T9, QD-Q11.

**R3.5 Sinonimlar (S, bittalab).**
- `synonyms.tsv` ga yozuvlar faqat ibora darajasida qo'shiladi. Har biri uchun musbat va manfiy test bo'ladi. Umumiy stemming qilinmaydi.
- Qabul: o'zbekcha erkin gapda topilganlar 3/8 dan kamida 5/8 ga chiqadi, mavzusiz shovqin 3/25 dan oshmaydi.
- Asos: QD-Q10, TZ-T6.

**R3.6 Taklif hookiga to'g'ri ishonch (S).**
- CLAUDE.md da taklif "nomzod" deb ataladi va hook sarlavhasi "Nomzod bo'limlar" bo'ladi. Javob takliflarga emas, `show` bilan o'qilgan matnga tayanadi.
- Asos: KT-K8.

### Bosqich 4. Korpus sifati (davomiy, 8-12 hafta)

Bu eng katta va eng qimmatli ish. Hisob: agentga ~40 soat, odamga ~28-44 soat (taxmin). Mashina qatlami agent vaqtini kamaytiradi.

**R4.1 Versiya bazasi qarori (S, egasi).**
- DECISIONS.md ga yoziladi: yangi misollar Boot 4.x, Spring 7, Hibernate 7, TC 2, JUnit 6 bo'yicha. Boot 3.5 farqi bor joyda "Boot 3.5 da: ..." eslatmasi qoladi. Java bazasi 21, Java 25 eslatma bo'ladi.
- Korpus butunlay qayta yozilmaydi, faqat mashina topgan farq nuqtalari tuzatiladi.
- CONTRIBUTING ga yopiq oraliq qoidasi qo'shiladi.
- Oltita README dagi "Versiya bazasi" qatori yangilanadi.
- Asos: KR-Q1, KR-T-K1.

**R4.2 Mashina tekshiruvi `verify_claims` (M).**
- Avval ogohlantirish, keyin xato sifatida `check_docs` ga ulanadi. Tekshiruvlar:
  - Boot property deprecation (`spring-configuration-metadata` dan).
  - Versiyalar orasidagi olib tashlangan API ro'yxati: Hibernate 6.6 va 7, TC 1.21 va 2, Boot 3.5 va 4.
  - Maven koordinata BOM da boshqariladimi.
  - Java blok parse (allowlist fayl va blok xeshi bo'yicha).
  - YAML/XML parse.
- Qabul: 2026-10-05 da qo'lda topilgan xatolarni u ham topadi. Yolg'on ishga tushish 5% dan kam. Qo'shimcha vaqt 1 s dan oshmaydi.
- Asos: KR-Q2, KR-Q6, KR-Q7, KR-T-K1.

**R4.3 Uch qatlamli tekshiruv jarayoni (S).**
- Qatlamlar: mashina (R4.2), agent (faqat mashina hal qilmagan da'volar), odam (har 10 bobdan 3 tasi, tasodifiy).
- CONTRIBUTING da da'vo turi bo'yicha jadval bo'ladi.
- `review_queue.py --holat` filtri: agent ro'yxati `ai-draft`, odam ro'yxati `tekshirilmoqda`.
- `check_review` qat'iylashadi: sana, tekshiruvchi va manba soni majburiy. "tekshirilgan" holatini Claude muallifligidagi commit qo'ya olmaydi.
- Manbalar tag yoki commit SHA ga qadaladi, mavjud 31 URL almashtiriladi.
- `claims_report` ga empirik taqqoslash sinfi qo'shiladi.
- Asos: KR-Q3, KR-Q17, KR-Q12, KR-Q14, KR-T-K4, KR-Q13.

**R4.4 O'tkazuvchanlik maqsadi (L).**
- Haftasiga 15-20 bob agent tekshiruvidan (`tekshirilmoqda`), 5 bob odam imzosidan (`tekshirilgan`) o'tadi. Har xato `known_errors.tsv` ga naqsh bo'ladi.
- Navbat `review-queue.tsv` tartibida: agentlar eng ko'p o'qiydigan boblar oldin.
- Qabul: 12 haftada barcha boblar kamida `tekshirilmoqda`, 60 tadan ko'pi `tekshirilgan`.
- Asos: JR-J11, KR-Q3.

**R4.5 Holatni ochiq aytish (S).**
- README va oltita hujjat README sida bitta holat qatori bo'ladi, uni `review_status.py --yoz` yozadi va `check_docs` solishtiradi.
- Asos: TZ-T8.

**R4.6 Takror va izchillik (M, bob tekshiruvi bilan birga).**
- Takror qoidasi CONTRIBUTING, CLAUDE.md, README va OWNERS da bitta matnga keltiriladi.
- OWNERS dagi 25 ogohlantirish uy-bobga havola qo'shish bilan yopiladi, keyin `warn` `err` ga o'tadi.
- `dup_report.py` faqat hisobot bo'ladi, `check_docs` ga qo'shilmaydi.
- Havolalar aniq bo'lim anchoriga beriladi (ratchet bilan).
- `testrovshik` tuzatiladi.
- Patterns summary tekshiruvi qo'shiladi.
- Ishora bo'limlarga havola beriladi va taxallus nishonga ko'chadi.
- Asos: TZ-T1, TZ-T4, KT-K7, TZ-T5, TZ-T7, TZ-T11, TZ-T12.

**R4.7 Til sifati va o'quvchi tajribasi (M, bob tekshiruvi bilan birga).**
- Faqat aniq imlo variantlari nasrda bitta shaklga keltiriladi va `known_errors.tsv` ga yoziladi: `stsenariy|scenariy|senariy` -> `ssenariy`, `in'ektsiya|injeksiya` -> `inyeksiya`, `ob'ekt` -> `obyekt`. Sarlavhalar anchor bilan birga bitta commitda o'zgartiriladi (TL-TL4).
- Inglizcha atamaga qo'shimcha qo'shish uslubi egasi tomonidan tanlanadi va CONTRIBUTING "Til" bo'limiga yoziladi (TL-TL9).
- "Bo'lim ichida bitta tushuncha bitta nom bilan" qoidasi qo'shiladi. Yangi asbob yozilmaydi (TL-TL10).
- Kalka va rus so'zlari bob tekshiruvida tuzatiladi (TL-TL12). Faqat koddan iborat bo'limlarga 1-2 gap nasr qo'shiladi (TL-TL8).
- README "Qayerdan boshlash" ga anchor bilan 6-8 tipik savol qo'shiladi (N+1, S3776 va boshqalar) (TL-TL7).
- `.github/ISSUE_TEMPLATE/bob-xatosi.yml` va README larda xabar havolasi qo'shiladi (TL-TL2).

### Bosqich 5. Orkestrator to'g'riligi va soddaligi (3-5 kun, A/B smoke dan keyin)

**R5.1 Marshrut va hajm bitta joyda (S).**
- S/M/L jadvali faqat `marshrut.md` da bo'ladi: 1-3 fayl S, 4 va undan ko'p fayl yoki bir necha qatlam M, qaytarib bo'lmaydigan qaror L.
- "tuzat + yiqildi" so'rovi dasturchiga boradi. test-muhandis faqat qoplash so'ralganda chaqiriladi.
- `manguberdi` faol bo'lsa marshrut skilllari faqat bob jadvali vazifasini bajaradi.
- spring-testing `run_tests.py` ni tavsiya qiladi.
- `test_skill.py` S/M/L ta'rifi faqat bir joyda ekanini tekshiradi.
- Qabul: R1.4 marshrut evali 27/30.
- Asos: KT-K4, OK-O5, OK-O4, KT-K13, KT-K6.

**R5.2 Yozuvchi va reviewer bir xil mezon (S).**
- Kartaga `fayllar:` qatori qo'shiladi. Review rules_for ni shu fayllar bilan chaqiradi.
- M da test fayllari review doirasidan chiqariladi (ko'p modulli pathspec bilan). Hisobotda "Testlar: mexanik tekshirildi" yoziladi.
- Asos: OK-O9, OK-O10.

**R5.3 Aktyor natijasini mexanik tekshirish (M).**
- SubagentStop hooki dasturchi va test-muhandis javobida `run_tests exit=` qatorini va jurnal yozuvini tekshiradi, bo'lmasa block qiladi.
- Review dagi "yuqori" og'irlik faqat aniq buzilish stsenariysi bilan beriladi.
- Asos: OK-O14.

**R5.4 Budjet aylanib o'tishlari (S).**
- `guruh:` id faqat ro'yxatdan o'tgan guruh bo'lsa qabul qilinadi.
- Noma'lum `subagent_type` "boshqa" hisobiga tushadi.
- `--tiklash` uchun `ask` beriladi.
- UserPromptSubmit dagi reset saqlanadi.
- Asos: OK-O7.

**R5.5 Parallel rejim ishlasin (M).**
- Asos sifatida joriy holatdan `commit-tree` bilan vaqtinchalik commit olinadi (branch va indeks o'zgarmaydi).
- Worktree `<root>/.claude/worktrees/<id>` da yaratiladi va `.git/info/exclude` ga yoziladi.
- `royxat --fayllar` qo'shiladi.
- Qabul: REJA.md bor daraxtda va ikkinchi partiyada `yarat` ishlaydi. Jonli yurishda ruxsat so'rovi 0.
- Asos: OK-T-K4, OK-O13, OK-T-K1.

**R5.6 Handoff va memory (S).**
- Handoff fakt qismini avtomatik yig'adi. Lokal sessiyada u git siz `.claude/.state/handoff/` ga yoziladi.
- B yo'lida `manguberdi` ish boshida memory indekslarini o'qiydi.
- Memory o'qish va yozish qoidasi bitta qilinadi.
- Asos: OK-O17, KT-T-Q1, KT-K9.

**R5.7 A/B qarori (S).**
- To'liq A/B natijasiga ko'ra uch yo'ldan biri tanlanadi:
  - Orkestrator qoladi.
  - Faqat tez yo'l bilan qoladi.
  - Olib tashlanadi (`eval/ab/README.md` dagi ro'yxat bo'yicha).
- Review modelini opus ga ko'tarish faqat A/B 8 va 9-vazifada foyda ko'rinsa.
- Asos: OK-O15, OK-O12, JR-J2.

### Bosqich 6. Hook, guard va qo'llanish chegarasi (4-6 kun)

**R6.1 Chegaralangan o'qish o'lchansin (M).**
- `sed -n 'A,Bp'`, `head -n N`, `head -c N`, `tail -n +K` haqiqiy bayt bilan o'lchanadi.
- `grep ''`, `awk '1'`, `sed ''` butun fayl o'qish deb sanaladi.
- Quvurda oxirgi bosqich chegarani beradi, shunda `cat BIG | wc -l` o'tadi.
- `index/` ham kuzatuvga olinadi.
- Qabul: 14 yangi holat. Read va Bash bir xil baytga bir xil qaror beradi.
- Asos: HK-H3, HK-T-M2.

**R6.2 Tabiiy prefikslar (S).**
- `timeout`, `command`, `sh/bash gradlew` va `(subshell)` aylanib o'tishi yopiladi.
- Asos: HK-H4.

**R6.3 Hook xatolari ko'rinsin (S).**
- `settings.json` va o'rnatuvchidagi 7 hook buyrug'ida `|| exit 0` o'rniga `|| exit 1` yoziladi. 2 dan boshqa kod to'smaydi, lekin Claude Code "hook error" ni ko'rsatadi. Izoh matni yangilanadi va DECISIONS.md ga yozuv qo'shiladi.
- Hook ichidagi kutilmagan istisno ham 1 bilan chiqadi. To'siq faqat JSON orqali beriladi.
- Ixtiyoriy: `hookio.fail_open()` holat papkasidagi `hook_errors.log` ga bitta qator yozadi.
- Qabul: `CLAUDE_PROJECT_DIR=/yoq` bilan har buyruq rc=1 va stdout bo'sh. Ataylab buzilgan skript hook error sifatida ko'rinadi.
- Asos: PL-CC11, HK-H2, KD-Q5, OC-K6.

**R6.4 Mayda tuzatishlar (S).**
- NOSONAR va `@SuppressWarnings` hurmat qilinadi. Test kodidagi `System.out` belgilanmaydi (HK-H10).
- Yagona vazifa sifatidagi `clean` uchun `ask` beriladi, `clean test` esa `deny` bo'lib qoladi (HK-H12).
- `budget.json` dagi buzuq slot tozalanadi (KD-K2).
- handoff `GENIUS_STATE_DIR` ni hurmat qiladi (HK-H14).
- `tools/testdata/` rules_for shartidan chiqariladi (HK-H5).
- check_code xabarlari tuzatiladi: qayta otiladigan catch "yutadi" deb atalmaydi, `catch (Throwable)` uchun `java:S1181` beriladi (QC-Q12, QC-T-M2).
- guard paketlash buyrug'ida (`package`, `install`) to'g'ri yo'lni aytadi: testlar o'tgan bo'lsa `-DskipTests` bilan package (QC-Q13).

**R6.5 Darvozalarni aylanib o'tish yo'llari (S).**
- `.java` faylga Bash orqali yozish (`>`, `tee`, `sed -i`) deny bo'ladi va xabari "Edit yoki Write bilan yozing". Faylni o'qish va heredoc ichidagi Java matni ruxsat etiladi (PL-CC2).
- `flyway:clean`, `flywayClean` va `liquibase:dropAll` to'g'ri sabab bilan `ask` oladi. Hozir tasodifan va noto'g'ri sabab bilan to'siladi (XV-O5).
- budget faqat `manguberdi:` prefiksini kesadi. `SendMessage` aktyor nomiga yuborilsa, u ham hisobga tushadi (PL-CC7).
- Qabul: `test_guard` va `test_budget` da har band uchun ijobiy va salbiy holat.

**R6.6 Qo'llanish chegarasi (M).**
- `hookio.active()` ildizda `package.json`, `pubspec.yaml` yoki `app.json` bo'lsa `android/` dagi markerni hisobga olmaydi. `AndroidManifest.xml` yoki `com.android` bo'lsa ham nofaol (QC-Q1, QC-Q6).
- `GENIUS_HOOKS=on` chuqur monorepo uchun majburan yoqadi. Chuqur skan qo'shilmaydi (QC-Q7).
- `run_tests.project_root` cwd dan git ildizigacha eng yuqori markerni oladi. Bir nechta bo'lsa ro'yxat bilan rc=2 qaytadi. guard maslahatida `--ildiz` ko'rsatiladi (QC-K2).
- Wrapperi bor asbob ustun bo'ladi (QC-Q5).
- Kotlin uchun ochiq aytiladi:
  - check_code .kt uchun "tekshirilmadi" va rc=3 qaytaradi.
  - rules_for .kt ni ko'radi va "Kotlin: mexanik tekshiruv yo'q" deydi (QC-Q2).
- Quarkus va Micronaut profili: Spring-only punktlar filtrlanadi, `@QuarkusTest` taniladi (QC-Q4).
- rules_for proyekt Boot va Java versiyasini o'qiydi va eski versiyada banner chiqaradi (QC-Q3).
- rules_for Gradle version catalog ni ko'radi (QC-T-M1).
- install/README da uch qismli jadval: to'liq, qisman, qo'llab-quvvatlanmaydi (QC-Q10).
- Qabul: RN, Flutter va Android fixture larida hook nofaol. Monorepo va Kotlin holatlari tegishli `test_<nom>.py` da yashil.

### Bosqich 7. Tarqatish, platforma va xavfsizlik hujjati (6-9 kun, mustaqil)

**R7.1 Versiya (M).**
- `VERSION` va `v0.1.0` tag qo'yiladi.
- `~/.claude/skills/manguberdi/.genius.json` yoziladi: commit, sana, aktyorlar.
- Retired aktyorlar (`arxitektor`) yangilashda olib tashlanadi.
- `budget.py --holat` o'rnatilgan va klon commitini solishtiradi.
- Asos: OC-K5, JR-J9.

**R7.2 Linux va macOS o'rnatuvchisi (L).**
- `install/install.py` (POSIX) yoziladi: quruq, `--apply`, `--update`, `--uninstall`.
- CI installer matritsasiga ubuntu va macos qo'shiladi.
- Shundan keyin ps1 Python o'ramiga qisqaradi.
- Asos: OC-K3.

**R7.3 `doctor` buyrug'i va `GENIUS_PYTHON` (S).**
- O'rnatishdan keyin har band bir qatorda tekshiriladi. Hook buyrug'i `${GENIUS_PYTHON:-python3}` ni ishlatadi.
- Asos: OC-K6, OC-K7.

**R7.4 Statik darvoza (S).**
- `ruff --select E9,F` CI da ishlaydi, 4 topilma tuzatiladi.
- Python 3.8 va'dasi eng past versiyada sinaladi yoki va'da ko'tariladi.
- mypy darvoza bo'lmaydi.
- Asos: KD-Q2, OC-K9, KD-T-M2.

**R7.5 Umumiy yordamchi (M, faqat tegilganda).**
- `geniuslib.run_git` va `atomic_write_text` 1-qadamda R0.4 bilan birga qo'shiladi. Qolgan yordamchilar fayl tegilganda ko'chadi.
- Asos: KD-Q4, KD-Q9.

**R7.6 Release (S).**
- Tag `v*` da `check_docs`, `build_single`, zip va release yuradi. CHANGELOG release commitida qo'lda yoziladi.
- Asos: OC-K11.

**R7.7 Platforma bilan shartnoma (M).**
- `tools/doctor.py` quyidagilarni tekshiradi:
  - `claude --version` sinalgan versiyadan farq qilsa ogohlantiradi;
  - har hook buyrug'i namunaviy payload bilan exit 0, bo'sh stderr va to'g'ri `hookEventName` beradi;
  - aktyorlar qaysi modelda yurganini oxirgi transkriptdan chiqaradi.
- install/README ga sinalgan minimal Claude Code versiyasi yoziladi.
- Jonli kanareyka faqat foydalanuvchi terminalidan yuradi, `env -u CLAUDE_CODE_SESSION_ID` bilan (PL-CC10).
- `handoff.py` `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` ni o'qiydi (PL-CC8).
- Model aliasini pinlash yo'li hujjatlanadi (PL-CC13).
- Asos: PL-CC4, PL-CC8, PL-CC10, PL-CC13, OC-K6.

**R7.8 Xavfsizlik hujjati va ta'minot zanjiri (M).**
- Qisqa `SECURITY.md` yoziladi. Unda quyidagilar bo'ladi:
  - qatlamlar: guard narx uchun, permissions xavfsizlik uchun, hooklar fail-open va nega;
  - har ruxsat qoidasining yon ta'siri;
  - fork PR bilan ishlash;
  - memory ga nima yozilmasligi;
  - zaiflik xabar qilish kanali (XV-T2).
- Hooklar klondagi ishchi daraxtdan emas, aniq commit dagi `git worktree --detach` dan yuradi. `tools/yangilash.py` o'zgarish ro'yxatini ko'rsatadi va faqat tasdiqdan keyin `merge --ff-only` qiladi (XV-Y1).
- CI da `permissions: contents: read` qo'yiladi va actions SHA ga pin qilinadi. `.github/`, `tools/` va `install/` uchun CODEOWNERS yoziladi (XV-P1).
- O'rnatish yo'lida `$`, backtick yoki qo'shtirnoq bo'lsa o'rnatish to'xtaydi (XV-P2).
- Sir fayllar uchun global `deny` va `ask` qo'shiladi (`~/.ssh`, `~/.aws`, `.env`). Repo sozlamasidagi specifiersiz `Read` olib tashlanadi (XV-O4).
- Asos: XV-T2, XV-Y1, XV-P1, XV-P2, XV-O4, XV-O3.

**R7.9 Litsenziya va manba ko'rsatish (S).**
- `tools/sonar_rules.tsv` dan inglizcha sarlavha ustuni olib tashlanadi: u SSALv1 ostidagi matn va uni hech kim o'qimaydi (TL-TL5).
- `LICENSE` ga CC BY 4.0 legalcode, `LICENSE-CODE` ga toza MIT matni qo'yiladi. Qamrov izohi README ga ko'chadi (TL-TL6).
- clean-code 32-37 kataloglariga Fowler (Refactoring, 2-nashr) va Martin (Clean Code, 17-bob) manbasi yoziladi. Fowler misollari o'z domenidagi misolga almashtiriladi (TL-TL3).
- Asos: TL-TL5, TL-TL6, TL-TL3.

### Bosqich 8. Ish tartibi qoidalari (hamma bosqichga)

Bu qoidalar CONTRIBUTING.md ga bitta qisqa bo'lim bo'lib yoziladi va iloji boricha mexanizm bilan qo'llab-quvvatlanadi.

1. **Sof asbob soni o'smaydi.** Yangi asbob faqat mavjudini almashtirsa yoki uning subbuyrug'i bo'lsa qo'shiladi (JR-J10, JR-T-S2).
2. **Branch, PR va yashil CI.** main ga to'g'ridan-to'g'ri push yo'q (R0.8). Push dan keyin CI natijasi kutiladi (JR-J5).
3. **A/B tugaguncha muzlatish.** `manguberdi`, `budget.py`, `guruh.py` va check_code zanjir shartiga faqat xato tuzatish kiradi (JR-J2).
4. **Mustaqil tekshiruv.** 200 satrdan katta asbob o'zgarishi `review` aktyoridan o'tadi. Tashqi chiqishni o'qiydigan asbob haqiqiy fixture bilan sinaladi (JR-J3, JR-J4).
5. **Commit bitta asbob yoki qaror.** Kod, uning testi va hujjati birga, `docs/` mazmuni alohida (JR-J12).
6. **Korpus ulushi.** Har ish kunida korpus tekshiruviga vaqtning kamida yarmi beriladi, toki R4.4 maqsadiga yetilmaguncha (JR-J11).
7. **Memory saboqlari yo'qolmasin.** Windows saboqlari CONTRIBUTING ga qisqa ro'yxat bo'lib yoziladi. Muhit haqidagi bilim `memory/umumiy/` ga tushadi (JR-J7).
8. **Olib tashlash nomzodlari.**
   - `restore_backup.py`: 2 haftalik deprecation dan keyin.
   - `guruh.py` va budjetning guruh mantiqi: A/B natijasiga bog'liq.
   - `review_*` va `usage`/`cost_report` ni birlashtirish: keyinroq.

### Birinchi 17 vazifa (ta'sir / mehnat bo'yicha)

| # | Vazifa | Mehnat | Nega birinchi |
|---|---|---|---|
| 1 | R0.1 main ni yashilga qaytarish | S | Hamma keyingi ish CI signaliga tayanadi |
| 2 | R0.9 subagentda `ask` o'rniga `deny` | S | Zanjir 6 soat 20 daqiqa qotib qolgani kuzatilgan |
| 3 | R0.3 `guruh.py` himoyasi | S | Ma'lumot yo'qotish, holat faylidan butun repo o'chishi mumkin |
| 4 | R0.10 global ruxsat ro'yxati | M | Fork PR build kodi so'rovsiz bajariladi |
| 5 | R0.5 memory maxfiyligi | M | Xususiy ma'lumot ommaviy repoga |
| 6 | R0.2 va R0.8 sukut branch va protection | S | Foydalanuvchi destruktiv o'rnatuvchini va tuzatilmagan korpusni oladi |
| 7 | R0.4 non-ASCII va monorepo yo'li | S | O'zgarish ko'rinmaydi, "test yo'q" deb rc 0 qaytadi |
| 8 | R0.6 check_code yolg'on block | M | Qo'llanma o'z tavsiyasini to'sadi |
| 9 | R0.7 tasdiqlangan korpus xatolari | M | Foydalanuvchi buzilgan build yoki noto'g'ri ogohlantirish oladi |
| 10 | R1.1 A/B tayyorlovini tuzatish | S | Usiz A/B natijasi ma'nosiz |
| 11 | R1.2 runner va smoke | M | Orkestrator taqdiri shu raqamga bog'liq |
| 12 | R2.1 test suite tezligi | M | Har iteratsiya 48 s dan 15 s ga |
| 13 | R2.2 CI tezligi | S | 158 s dan 90 s ga, docs commitida 45 s |
| 14 | R4.1 va R4.2 versiya qarori va mashina tekshiruvi | M | Korpus tekshiruvini 2-3 baravar arzonlashtiradi (taxmin) |
| 15 | R1.3 held-out to'plamlar | M | Qidiruv va eval ishlari shunga tayanadi |
| 16 | R6.6 qo'llanish chegarasi (RN, Flutter, Android) | S | Begona proyektda yolg'on maslahat va to'siq |
| 17 | R3.1 va R3.2 qidiruv tuzatishlari | M | Realistik so'rovda eng katta bo'shliq |

## 8. Nima qilinmaydi

Bular o'lchov yoki tekshiruv bilan rad etilgan, yoki narxi foydasidan katta.

- **Hooklarni bitta jarayonga yoki daemonga birlashtirish.** Yutuq deyarli nol, izolyatsiya esa yo'qoladi (HK-H15).
- **Qidiruv dvigatelini SQLite/FTS ga ko'chirish.** Hamma yaxshilanish mavjud TSV ustida qo'shimcha sifatida qilinadi (DECISIONS.md, QD kuchli tomonlari).
- **224 bobni qayta yozish.** Faqat mashina topgan farq nuqtalari tuzatiladi (KR-Q1).
- **patterns boblarini bo'lish.** Bo'lim darajasida o'qish ishlaydi, bo'lish kosmetik (TZ-T10).
- **Umumiy o'zbekcha stemming va fuzzy.** Holdout yomonlashdi va shovqin oshdi (QD-Q10).
- **`/` li tokenlarni va build iboralarini ko'r-ko'rona tashlash.** Bu to'g'ri javoblarni o'chiradi (QD-Q12).
- **`clean` ni umumiy `ask` qilish.** `mvn clean install` ochilib qoladi (HK-H12).
- **`start_new_session=True`.** Yetim build qoladi (KD-Q10).
- **Refaktoringda test-muhandisni oldinga qo'yish.** Bu A/B mezonini buzadi va parallellikni yo'qotadi (OK-O6).
- **Budjetni "davom et" da reset qilmaslik.** Bunda odam tasdiqlagan davom ham to'silib qoladi (OK-O7).
- **mypy darvozasi, coverage foiz maqsadi, karantin ro'yxati.** Bular haqiqiy nuqson topmadi, faqat shovqin beradi (KD-Q2, KD-Q8, KD-Q1).
- **Har orkestrator o'zgarishida to'liq A/B.** 2 kunda 42 shunday commit bo'lgan, bu juda qimmat. To'liq yurish oyiga ko'pi bilan bir marta yoki qaror oldidan bo'ladi, oraliqda faqat smoke (OL-O16).
- **CI da LLM eval.** Faqat qo'lda va kamdan-kam (OL-O16).
- **Stop hookni `async` qilish.** `-p` rejimida oxirgi navbat sarfi yo'qoladi (PL-CC12).
- **Chuqur monorepo skani har Read va Bash da.** Har chaqiruvga fayl o'qish qo'shiladi. O'rniga `GENIUS_HOOKS=on` beriladi (QC-Q7).
- **`qotib` sinonimini zaiflashtirish.** U Java ichidagi so'rovlarda to'g'ri ishlaydi (QC-Q8).
- **Qo'llanish uchun alohida `test_scope.py` va atama uchun alohida `terms_report.py`.** Ular mavjud testlarni takrorlaydi va asbob sonini oshiradi (QC-Q9, TL-TL10).
- **guard ni xavfsizlik chegarasiga aylantirish.** U narx to'sig'i bo'lib qoladi. Xavfsizlik ruxsat qoidalari va `SECURITY.md` orqali hal qilinadi (XV-T2, XV-O5).

## 9. Egasining qarori kerak bo'lgan joylar

Bularni agent o'zi hal qila olmaydi yoki hal qilmasligi kerak.

1. **Sukut branch.** `main` qilish va eski branchni o'chirish (R0.2).
2. **Branch protection.** Required checks, egaga bypass, agent PR oqimi va auto-merge ruxsati (R0.8).
3. **Actions runner.** Oxirgi 2 run runnersiz bekor bo'ldi: billing yoki limitni tekshirish (R0.1).
4. **Versiya bazasi.** Boot 4 asosiy va Boot 3.5 eslatma, yoki aksincha (R4.1).
5. **Memory siyosati.** Global o'rnatishda proyekt memorysi qayerda turadi va push qilinadimi (R0.5).
6. **A/B byudjeti.** Smoke ~6 sessiya, to'liq 10 x 2 x 3 = 60 sessiya. Narxi sessiyaga ~$1-4 deb olinsa ~$60-240 (taxmin, R1.2).
7. **Odam tekshiruvi vaqti.** ~66 bob, bobiga 25-40 daqiqa, jami 28-44 soat (taxmin, R4.4).
8. **Python minimal versiyasi.** 3.8 va'dasi sinaladimi yoki ko'tariladimi (R7.4).
9. **Global ruxsatlar.** `run_tests.py` faqat opt-in bo'lishiga va `guruh.py` ruxsatini toraytirishga rozilik (R0.10).
10. **Qo'llab-quvvatlanadigan proyekt turlari.** Kotlin, Quarkus va Android "qisman" bo'ladimi yoki "qo'llab-quvvatlanmaydi" mi (R6.6).
11. **Litsenziya va uslub.** Kanonik litsenziya matnlari va inglizcha atamaga qo'shimcha yozish uslubi (R7.9, R4.7).
12. **Hook yangilanish siyosati.** Hooklar `git pull` dan keyin darhol yangilanadimi yoki faqat tasdiq bilan (R7.8).

## 10. Muvaffaqiyat ko'rsatkichlari

| Ko'rsatkich | Hozir (2026-10-05) | 2 hafta | 6 hafta | 12 hafta |
|---|---|---|---|---|
| main CI yashil ulushi | 64%, HEAD qizil | 90%+, HEAD yashil | 90%+ | 95%+ |
| Odam imzolagan bob | 0 / 224 | 5 | 30 | 60+ |
| Agent tekshirgan bob (`tekshirilmoqda`) | 5 | 30 | 120 | 224 |
| R0.7 dagi tasdiqlangan korpus xatolari ochiq | 20+ | 0 | 0 | 0 |
| Mashina tekshiruvi (verify_claims) | yo'q | ogohlantirish | xato | xato |
| A/B | yurilmagan | smoke | 10 x 2 x 3 va qaror | qaror bajarilgan |
| S zanjiri token B/A | ~2.5-4 (taxmin) | o'lchangan | 1.5 dan kam | 1.5 dan kam |
| Hook realistik 1-o'rin / top-3 | 44% / 60% | o'lchangan (holdout) | 55% / 70% | 60% / 75% |
| `find` kalit so'z topildi | 20/30 | - | 27/30 | 28/30 |
| Held-out rules_for / check_code recall | 4/8, 1/8 | o'lchangan | 6/8, 4/4 mexanik | 7/8, 4/4 |
| Test suite (lokal) | 48 s | 25 s | 15 s | 15 s |
| CI run | 158 s | 90 s | 90 s | 90 s |
| check_docs | 2.8 s | 2.1 s | 2.5 s gacha (verify_claims bilan) | 2.5 s |
| Qat'iy kontekst | 6346 token | ~4800 | ~4800 | 5000 dan kam |
| Asbob soni (test emas) | 27 | 27 | 27 dan ko'p emas | 27 dan ko'p emas |
| Global ruxsatda yon ta'sirli asbob | 2 (`run_tests`, `guruh` to'liq) | 0 | 0 | 0 |
| Subagentda `ask` kutishi | 6 soat 20 daqiqa kuzatilgan | 0 (deny) | 0 | 0 |
| RN, Flutter, Android da yolg'on faollashuv | faol | nofaol | nofaol | nofaol |
| `SECURITY.md` va minimal Claude Code versiyasi | yo'q | - | bor | bor |
| Ochiq yuqori va kritik topilma | 41 | 22 | 8 | 0 |

## 11. Qamrov tanqidchisi topgan bo'shliqlar

10 yo'nalishli auditdan keyin alohida agent repo tuzilmasini qayta ko'rib chiqdi. U 4 ta umuman qamralmagan maydonni topdi. Har biri asosiy yo'nalishlar bilan bir xil tartibda tekshirildi: auditor va skeptik tekshiruvchi.

| Bo'shliq | Nega qamralmagan edi | Natija | Rejadagi joyi |
|---|---|---|---|
| Xavfsizlik modeli va ishonch chegarasi (XV) | Audit guard ni faqat narx to'sig'i, memory ni faqat maxfiylik deb ko'rgan | 18 topilma, 3 yuqori: fork PR build kodi, `guruh.py` holat fayli, ochiq memory | R0.3, R0.5, R0.10, R6.5, R7.8 |
| Claude Code bilan shartnoma (PL) | Asboblar rasmiy bo'lmagan transkript tuzilishiga va narx jadvaliga tayanadi | 13 topilma, 1 rad etildi. Eng muhimi: subagentda `ask` 6 soat 20 daqiqa kutdi | R0.9, R1.6, R6.3, R6.5, R7.7 |
| Qo'llanish chegarasi (QC) | Faqat Boot 4 va ikki build faylli holat ko'rilgan | 18 topilma, 2 yuqori: RN va Flutter faollashuvi, monorepo da `--diff` ko'r | R0.4, R0.7, R6.4, R6.6 |
| O'zbek tili, o'quvchi va kelib chiqish (TL) | Korpus faqat texnik fakt va mashina qidiruvi tomonidan ko'rilgan | 13 topilma, 1 rad etildi: imlo variantlari, manba ko'rsatilmagan kataloglar, litsenziya, ikki adashtiruvchi xato | R0.2, R0.7, R4.7, R7.9 |

Qamrov tanqidchisi boshqa bo'shliq bermadi.

## Ilova: topilmalar yo'nalish bo'yicha

Har faylda kuchli tomonlar, o'lchovlar, har topilmaning dalili, ta'siri, tavsiyasi, o'lchovi va tekshiruvchi izohi bor. ID shakli `PREFIKS-ID`, masalan `OK-O1`.

| Prefiks | Yo'nalish | Fayl |
|---|---|---|
| KR | Korpus faktik sifati va tekshiruv tezligi | [korpus.md](topilmalar/korpus.md) |
| OL | O'lchov va eval tizimi | [olchov.md](topilmalar/olchov.md) |
| OK | manguberdi orkestratori va aktyorlar | [orkestrator.md](topilmalar/orkestrator.md) |
| QD | Qidiruv va bo'lim taklifi | [qidiruv.md](topilmalar/qidiruv.md) |
| JR | Ish jarayoni va o'z-o'zini tanqid | [jarayon.md](topilmalar/jarayon.md) |
| OC | O'rnatish, CI va platforma | [ornatish.md](topilmalar/ornatish.md) |
| KD | Asbob kodi sifati va test tezligi | [kod.md](topilmalar/kod.md) |
| HK | Hooklar va guard | [hooklar.md](topilmalar/hooklar.md) |
| KT | Kontekst, token va ko'rsatmalar sifati | [kontekst.md](topilmalar/kontekst.md) |
| TZ | Hujjat tuzilmasi va izchillik | [tuzilma.md](topilmalar/tuzilma.md) |
| XV | Xavfsizlik modeli va ishonch chegarasi | [xavfsizlik.md](topilmalar/xavfsizlik.md) |
| PL | Claude Code ichki tuzilishi va narxlarga bog'liqlik | [platforma.md](topilmalar/platforma.md) |
| QC | Qo'llanish chegarasi: Spring bo'lmagan va nostandart JVM proyektlar | [qollanish.md](topilmalar/qollanish.md) |
| TL | O'zbek tili sifati, o'quvchi tajribasi va kontent kelib chiqishi | [oquvchi.md](topilmalar/oquvchi.md) |
