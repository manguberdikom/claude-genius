---
name: reja
description: Build one complete, grounded implementation plan (REJA.md) before any code is written - architecture decisions, per-location design-pattern assignment, test strategy and quality gate in a single document. Use when the user asks for a reja, plan, "reja tuz", "plan ber", "qanday qilaman", "qaysi pattern", a design or refactoring plan, a migration or performance plan, an architecture review before implementation, or hands over a spec as PDF, HTML, DOCX, image or URL. Harvests project configs, CLAUDE.md memories and prompt-design material, analyses the real code structure, then assigns every change a pattern, a test and an acceptance check, citing by topic name the five Java/Spring/PostgreSQL handbooks in this repository.
---

# Reja - aqlli implementatsiya rejasi

Bu skill kod yozishdan oldin bitta hujjat tayyorlaydi: **`REJA.md`**. Reja -
bajariladigan ishlar ro'yxati emas, **qarorlar to'plami**: qaysi faylning qaysi
joyi o'zgaradi, nega shu dizayn tanlandi, o'sha joyda qaysi pattern qo'llanadi,
qanday test yoziladi va natija qanday tekshiriladi.

Reja ikki kishiga yoziladi: qaror sababini bilmoqchi bo'lgan odamga va rejani
bajaradigan agentga. Shu sababli u ham izohlovchi, ham buyruq beruvchi bo'ladi.

## Qachon ishlatiladi

- "reja tuz", "plan ber", "qanday qilaman", "qaysi pattern mos" so'rovlari
- yangi funksiya, refaktoring, migratsiya, performance, integratsiya ishlari
- spetsifikatsiya PDF / HTML / DOCX / rasm / URL ko'rinishida berilganda
- katta o'zgarishdan oldin arxitektura va test strategiyasini kelishish kerak

**Ishlatilmaydi:** bir qatorli tuzatish, typo, versiya ko'tarish, formatlash -
bular darhol bajariladi. Reja yozish bajarishdan qimmatga tushmasligi kerak.

## Qattiq qoidalar

1. **Asossiz qator yo'q.** Har bir da'vo manbaga bog'lanadi: `fayl:qator`, config
   kaliti, qo'llanmadagi mavzu yoki PDF sahifasi. Manba bo'lmasa - `TAXMIN:` deb
   belgilanadi, yashirilmaydi.
2. **Variant emas, qaror.** "A yoki B bo'lishi mumkin" - bu reja emas. Bitta
   variant tanlanadi; qolganlari ADR ichida "ko'rib chiqilgan variantlar" bo'lib
   qoladi, asosiy matnda emas.
3. **Avval kodni o'qish, keyin pattern nomlash.** Kod tahlili (2-bosqich)
   tugamaguncha rejada bitta ham pattern nomi yozilmaydi.
4. **Pattern muammodan keladi, chiroylikdan emas.** Pattern nomlanishidan oldin
   `references/pattern-tanlash.md` dagi to'rt savol o'tkaziladi.
5. **Har bir qadam yashil qoldiradi.** Qadam tugaganda loyiha kompilyatsiya
   bo'ladi va testlar o'tadi. Yarim holatda qoldiradigan qadam ikkiga bo'linadi.
6. **Har bir xulq o'zgarishiga test.** Test darajasi, joyi, ma'lumoti va kutilgan
   natijasi (oracle) ko'rsatiladi. "Test yozish" degan qadam - bo'sh qator.
7. **Config haqiqati qo'llanmadan ustun.** classpathda yo'q kutubxona rejada
   ishlatilmaydi; kerak bo'lsa, uni qo'shish alohida qadam bo'ladi. Java va Spring
   versiyasi, DB, coverage chegarasi - hammasi loyiha faylidan o'qiladi.
8. **Hajm vazifaga mos.** S / M / L o'lchov `references/shablon.md` da; kichik
   ishga 15 bo'limli hujjat yozish - zarar.
9. **Reja o'zini bajarmaydi.** Bu skill faqat rejani yozadi va foydalanuvchiga
   beradi. Kod o'zgartirish - alohida, aniq ruxsatdan keyin.

## Bosqichlar

Har bosqich o'z artefaktini chiqaradi; artefakt tayyor bo'lmasa, keyingi
bosqichga o'tilmaydi.

| # | Bosqich | O'qiladi | Artefakt | O'tish sharti |
|---|---|---|---|---|
| 0 | Vazifani aniqlash | - | vazifa turi + hajm (S/M/L) | bitta jumlada maqsad yozildi |
| 1 | Manba yig'ish | `references/manbalar.md` | "Aniqlangan haqiqatlar" jadvali | config, memory va berilgan hujjatlar o'qildi |
| 2 | Kod analizi | `references/kod-analizi.md` | inventar + bog'liqlik eskizi + simptomlar | har bir simptom `fayl:qator` ga bog'landi |
| 3 | Arxitektura qarori | `references/arxitektura.md` | NFR budjeti + ADR(lar) + risk ro'yxati | qaytarib bo'lmaydigan har qarorga ADR bor |
| 4 | Pattern tayinlash | `references/pattern-tanlash.md` | joy -> pattern -> sabab -> mavzu jadvali | har pattern to'rt savoldan o'tdi |
| 5 | Test va sifat | `references/test-sifat.md` | test matritsasi + quality gate talablari | har o'zgarishga daraja va oracle bor |
| 6 | Rejani yozish | `references/prompt-dizayn.md`, `references/shablon.md` | `REJA.md` | shablon bo'limlari to'ldirildi |
| 7 | O'z-o'zini tekshirish | pastdagi checklist | tuzatilgan `REJA.md` | 13 banddan hammasi "ha" |

0-bosqichda vazifa turi aniqlanadi, chunki keyingi bosqichlar shunga qarab
og'irlashadi: `yangi funksiya`, `refaktoring`, `bug`, `migratsiya`,
`performance`, `integratsiya`, `xavfsizlik`, `test qarzi`.

Blokirovchi savol faqat bitta holatda beriladi: javobsiz har qanday taxmin
rejani bekor qiladi (masalan, "yangi servis mikroservis bo'ladimi yoki
monolitda qoladimi" ma'lum bo'lmasa). Qolgan noaniqliklar `TAXMIN:` qatori
bilan yozib ketiladi va rejaning oxirida "Ochiq savollar" ga qo'yiladi.

## Qo'llanmaga yo'naltirish

Bu repozitoriyda beshta qo'llanma bor. Reja ularga **mavzu nomi bilan** havola
qiladi, bob raqami bilan emas (raqam hujjat o'sganda siljiydi) va mazmunini
ko'chirmaydi.

| Savol | Hujjat | Mavzu |
|---|---|---|
| Qaysi pattern? Qanday ko'rinishda? | patternlar | hujjat oxiridagi `Alifbo bo'yicha indeks` orqali pattern nomi |
| Bu anti-pattern emasmi? | patternlar | `Anti-patternlar` |
| SOLID yoki GRASP buzilyaptimi? | patternlar | `Dizayn printsiplari` |
| Nima ishlamay qolishi mumkin? | arxitektor | `Nosozlik haqida fikrlash` |
| Qancha tez bo'ladi, qancha resurs yeydi? | arxitektor | `Ishlash va resurs hissi` |
| Spring, JPA va tranzaksiya ichida nima bo'ladi? | arxitektor | `Spring Core mexanikasi`, `Spring Data JPA va Hibernate chuqur`, `Spring tranzaksiyalari va ularning chegaralari` |
| PostgreSQL: indeks, lock, so'rov rejasi | arxitektor | `Indekslar`, `MVCC, izolyatsiya darajalari, lock va deadlock`, `Planner, statistika va EXPLAIN ANALYZE o'qish` |
| Qarorni qanday hujjatlashtirish (ADR)? | arxitektor | `Qaror qabul qilish va uni hujjatlashtirish` |
| Legacy kodni qanday bosqichma-bosqich o'zgartirish? | arxitektor | `Legacy kod va bosqichma-bosqich refaktoring` |
| Qaysi daraja test, qayerda? | testlash | `Test piramidasi va test turlari xaritasi`, `Integratsion test` |
| Test ma'lumoti va real infratuzilma | testlash | `Test ma'lumotlarini boshqarish`, `Testcontainers bilan real infratuzilmada test` |
| Arxitektura testi, test plan va DoD shabloni | testlash | `Arxitektura testlari va kod sifati darvozalari`, `Shablonlar, checklistlar va ma'lumotnoma` |
| Quality gate, new code, coverage mexanikasi | sonarqube | `Quality gate mexanikasi va shartlari`, `Yangi kod (new code) va "clean as you code" tamoyili`, `Coverage qanday o'lchanadi` |
| Qamralmaydigan kod, exclusion halolligi | sonarqube | `Qamralmay qoladigan kod va unga test yozish`, `Exclusion` |
| Bu o'zgarish qaysi Sonar qoidasini buzadi? | sonarqube | `Java va Spring da eng ko'p uchraydigan issue va ularning yechimi`, `Xato katalogi` boblari |
| Diffda nimaga qaraladi, niyat qanday tekshiriladi? | review | `Diffni o'qish mexanikasi`, `Reviewer ning tahlil apparati` |
| Pattern yetishmaydimi yoki ortiqchami? | review | `Dizayn pattern review I: yo'q patternni ko'rish`, `Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern` |
| Migratsiya, integratsiya va API o'zgarishi nimadan yiqiladi? | review | `Migratsiya review`, `Tashqi integratsiya review`, `API moslik va breaking change review` |
| Test to'liqmi? | review | `Test to'liqligini review qilish` |
| Reja review stolidan o'tadimi? | review | `Shablonlar, checklistlar va reviewer yetukligi` |

Mavzu nomidan bobni topish:

```bash
grep -n "^## " java-spring-architect-mindset.md | grep -i "tranzaksiya"
grep -n "^- \[Strategy" java-spring-design-patterns.md   # indeks: nom -> bo'lim
grep -n "^### " java-spring-design-patterns.md | grep -i "outbox"
```

Pattern nomi indeksda inglizcha turadi, shuning uchun reja patternni **inglizcha
nomi bilan** ataydi: `Transactional Outbox`, `Keyset / Cursor Pagination`.

## Chiqish shartnomasi

- Bitta fayl: loyiha ildizida `REJA.md` (bir nechta reja bo'lsa:
  `reja/<slug>-reja.md`). Foydalanuvchi ochib o'qiy oladigan joyda bo'lishi shart.
- Til: o'zbek lotin yozuvi, texnik atamalar inglizcha (bean, proxy, quality gate,
  coverage) - repozitoriyaning uslubi.
- Tuzilishi va majburiy bo'limlari: `references/shablon.md`.
- Oxirida ikki narsa bo'ladi: **Definition of Done** va **Manbalar** (o'qilgan
  config, qo'llanma bo'limlari, PDF sahifalari).
- Chatga reja ko'chirilmaydi. Javobning birinchi qatorida natija turadi (reja
  tayyor va fayl yo'li), keyin 5-10 qator tafsilot: eng muhim qaror, eng katta
  risk, ochiq savollar.

## Yakuniy tekshiruv (7-bosqich)

Rejani berishdan oldin 13 banddan har biriga "ha" deb javob berilishi kerak.
Bitta "yo'q" bo'lsa, reja tuzatiladi, keyin beriladi.

1. Maqsad bitta jumlada yozilganmi va o'lchanadiganmi?
2. Qamrovdan tashqari (non-goals) ro'yxati bormi?
3. Har bir "hozirgi holat" da'vosi `fayl:qator` ga bog'langanmi?
4. Har bir versiya/chegara/kalit config faylidan olinganmi (taxmin emas)?
5. Qaytarib bo'lmaydigan har qarorga ADR bormi (kontekst, qaror, variantlar, oqibat)?
6. Har bir pattern uchun: joyi, hal qiladigan muammosi, qo'llanma bo'limi va
   narxi (indirection) yozilganmi?
7. Tanlangan patternlar 25-bo'limdagi anti-patternlarga tushmaydimi?
8. Har bir qadam mustaqil tekshiriladimi (buyruq + kutilgan natija)?
9. Har bir xulq o'zgarishiga test darajasi, joyi, ma'lumoti va oracle bormi?
10. Quality gate talablari loyiha konfiguratsiyasidan olinganmi (new code
    coverage, duplication, complexity)?
11. Risklar ro'yxatida har risk uchun yumshatish choralari va "qanday bilib
    olamiz" bormi?
12. Rollback yo'li bormi (migratsiya, flag, reliz tartibi)?
13. Reja review ko'zi bilan o'qilganmi: yetishmayotgan pattern bormi, ortiqcha
    pattern bormi (review: `Dizayn pattern review I: yo'q patternni ko'rish`,
    `Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern`)?

## Yomon reja belgilari

- "optimallashtiramiz", "yaxshilaymiz", "refaktor qilamiz" - fe'l aniq emas
- 20 qadam, lekin birinchi qadamdan keyin loyiha kompilyatsiya bo'lmaydi
- pattern nomlari ko'p, lekin birortasi `fayl:qator` ga bog'lanmagan
- "coverage 80% bo'lsin" - lekin loyihada gate 100% yoki umuman yo'q
- `TAXMIN:` yo'q, lekin reja o'qilmagan fayl haqida gapiradi
- o'qiydigan odamga "qolganini o'zingiz hal qiling" degan bo'limlar
- o'zgarishlar sonini kamaytirish uchun bitta qadamga 12 fayl tiqilgan

## Memory

Bu faylda memory qoidalari takrorlanmaydi. Ish boshida proyekt va umumiy
`MEMORY.md` indekslari o'qiladi; yozishdan oldin `memory-protocol.md`:

- darvoza (yetti savol) - nimani yozmaslik kerak
- marshrut jadvali - qaysi joyga yozish kerak
- ketma-ketlik - qanday tartibda o'qish va yozish

Rejadan keyin memoryga faqat qaytariladigan bilim tushadi: shu proyektda
takrorlangan tuzoq, qabul qilingan qaror va uning sababi. Rejaning o'zi
memoryga ko'chirilmaydi, u `REJA.md` da va git tarixida qoladi.
