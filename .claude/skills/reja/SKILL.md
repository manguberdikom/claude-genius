---
name: reja
description: Build one complete, grounded implementation plan (REJA.md) before any code is written - architecture decisions, per-location design-pattern assignment, test strategy and quality gate in a single document. Use when the user asks for a reja, plan, "reja tuz", "plan ber", "qanday qilaman", "qaysi pattern", a design or refactoring plan, a migration or performance plan, an architecture review before implementation, or hands over a spec as PDF, HTML, DOCX, image or URL. Harvests project configs, CLAUDE.md memories and prompt-design material, analyses the real code structure, then assigns every change a pattern, a test and an acceptance check, citing the four Java/Spring/PostgreSQL handbooks in this repository.
---

# Reja - aqlli implementatsiya rejasi

Bu skill kod yozishdan oldin bitta hujjat tayyorlaydi: **`REJA.md`**. Reja —
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

**Ishlatilmaydi:** bir qatorli tuzatish, typo, versiya ko'tarish, formatlash —
bular darhol bajariladi. Reja yozish bajarishdan qimmatga tushmasligi kerak.

## Qattiq qoidalar

1. **Asossiz qator yo'q.** Har bir da'vo manbaga bog'lanadi: `fayl:qator`, config
   kaliti, qo'llanma bo'limi yoki PDF sahifasi. Manba bo'lmasa — `TAXMIN:` deb
   belgilanadi, yashirilmaydi.
2. **Variant emas, qaror.** "A yoki B bo'lishi mumkin" — bu reja emas. Bitta
   variant tanlanadi; qolganlari ADR ichida "ko'rib chiqilgan variantlar" bo'lib
   qoladi, asosiy matnda emas.
3. **Avval kodni o'qish, keyin pattern nomlash.** Kod tahlili (2-bosqich)
   tugamaguncha rejada bitta ham pattern nomi yozilmaydi.
4. **Pattern muammodan keladi, chiroylikdan emas.** Pattern nomlanishidan oldin
   `references/pattern-tanlash.md` dagi to'rt savol o'tkaziladi.
5. **Har bir qadam yashil qoldiradi.** Qadam tugaganda loyiha kompilyatsiya
   bo'ladi va testlar o'tadi. Yarim holatda qoldiradigan qadam ikkiga bo'linadi.
6. **Har bir xulq o'zgarishiga test.** Test darajasi, joyi, ma'lumoti va kutilgan
   natijasi (oracle) ko'rsatiladi. "Test yozish" degan qadam — bo'sh qator.
7. **Config haqiqati qo'llanmadan ustun.** classpathda yo'q kutubxona rejada
   ishlatilmaydi; kerak bo'lsa, uni qo'shish alohida qadam bo'ladi. Java va Spring
   versiyasi, DB, coverage chegarasi — hammasi loyiha faylidan o'qiladi.
8. **Hajm vazifaga mos.** S / M / L o'lchov `references/shablon.md` da; kichik
   ishga 15 bo'limli hujjat yozish — zarar.
9. **Reja o'zini bajarmaydi.** Bu skill faqat rejani yozadi va foydalanuvchiga
   beradi. Kod o'zgartirish — alohida, aniq ruxsatdan keyin.

## Bosqichlar

Har bosqich o'z artefaktini chiqaradi; artefakt tayyor bo'lmasa, keyingi
bosqichga o'tilmaydi.

| # | Bosqich | O'qiladi | Artefakt | O'tish sharti |
|---|---|---|---|---|
| 0 | Vazifani aniqlash | — | vazifa turi + hajm (S/M/L) | bitta jumlada maqsad yozildi |
| 1 | Manba yig'ish | `references/manbalar.md` | "Aniqlangan haqiqatlar" jadvali | config, memory va berilgan hujjatlar o'qildi |
| 2 | Kod analizi | `references/kod-analizi.md` | inventar + bog'liqlik eskizi + simptomlar | har bir simptom `fayl:qator` ga bog'landi |
| 3 | Arxitektura qarori | `references/arxitektura.md` | NFR budjeti + ADR(lar) + risk ro'yxati | qaytarib bo'lmaydigan har qarorga ADR bor |
| 4 | Pattern tayinlash | `references/pattern-tanlash.md` | joy -> pattern -> sabab -> qo'llanma § jadvali | har pattern to'rt savoldan o'tdi |
| 5 | Test va sifat | `references/test-sifat.md` | test matritsasi + quality gate talablari | har o'zgarishga daraja va oracle bor |
| 6 | Rejani yozish | `references/prompt-dizayn.md`, `references/shablon.md` | `REJA.md` | shablon bo'limlari to'ldirildi |
| 7 | O'z-o'zini tekshirish | pastdagi checklist | tuzatilgan `REJA.md` | 12 banddan hammasi "ha" |

0-bosqichda vazifa turi aniqlanadi, chunki keyingi bosqichlar shunga qarab
og'irlashadi: `yangi funksiya`, `refaktoring`, `bug`, `migratsiya`,
`performance`, `integratsiya`, `xavfsizlik`, `test qarzi`.

Blokirovchi savol faqat bitta holatda beriladi: javobsiz har qanday taxmin
rejani bekor qiladi (masalan, "yangi servis mikroservis bo'ladimi yoki
monolitda qoladimi" ma'lum bo'lmasa). Qolgan noaniqliklar `TAXMIN:` qatori
bilan yozib ketiladi va rejaning oxirida "Ochiq savollar" ga qo'yiladi.

## Qo'llanmaga yo'naltirish

Bu repozitoriyda to'rtta qo'llanma bor; reja ularga **bo'lim raqami bilan**
havola qiladi, mazmunini ko'chirmaydi.

| Savol | Hujjat | Kirish nuqtasi |
|---|---|---|
| Qaysi pattern? Qanday ko'rinishda? | `java-spring-design-patterns.md` | "Alifbo bo'yicha indeks" (oxirida), keyin 1–30-bo'lim |
| Bu anti-pattern emasmi? | `java-spring-design-patterns.md` | 25-bo'lim (Anti-patternlar) |
| SOLID / GRASP buzilyaptimi? | `java-spring-design-patterns.md` | 26-bo'lim |
| Nima ishlamay qolishi mumkin? Qancha tez bo'ladi? | `java-spring-architect-mindset.md` | 7-bob (nosozlik), 8-bob (napkin math) |
| Spring / JPA / tranzaksiya ichida nima bo'ladi? | `java-spring-architect-mindset.md` | 15–20-boblar |
| PostgreSQL: indeks, lock, plan, migratsiya | `java-spring-architect-mindset.md` | 21–27, 33-boblar |
| Qarorni qanday hujjatlashtirish (ADR)? | `java-spring-architect-mindset.md` | 3-bob |
| Legacy kodni qanday bosqichma-bosqich o'zgartirish? | `java-spring-architect-mindset.md` | 34-bob |
| Qaysi daraja test, qayerda? | `java-spring-testing-handbook.md` | 2-bob (piramida), 5–9-boblar |
| Test ma'lumoti, muhit, Testcontainers | `java-spring-testing-handbook.md` | 8, 10-boblar |
| Arxitektura testi, DoD, test plan shabloni | `java-spring-testing-handbook.md` | 14, 18-boblar |
| Quality gate, new code, coverage mexanikasi | `java-spring-sonarqube.md` | 6–10-boblar |
| Qamralmaydigan kod, exclusion halolligi | `java-spring-sonarqube.md` | 11, 12-boblar |
| Bu o'zgarish qaysi Sonar qoidasini buzadi? | `java-spring-sonarqube.md` | 14, 25–30-boblar (xato katalogi) |

Pattern qidirishning eng tez yo'li — indeksdan grep:

```bash
grep -n "^- \[Strategy" java-spring-design-patterns.md     # -> 3.9, 8.21, 24.11
grep -n "^### 3\.9 " java-spring-design-patterns.md        # bo'limni ochish
```

## Chiqish shartnomasi

- Bitta fayl: loyiha ildizida `REJA.md` (bir nechta reja bo'lsa:
  `reja/<slug>-reja.md`). Foydalanuvchi ochib o'qiy oladigan joyda bo'lishi shart.
- Til: o'zbek lotin yozuvi, texnik atamalar inglizcha (bean, proxy, quality gate,
  coverage) — repozitoriyaning uslubi.
- Tuzilishi va majburiy bo'limlari: `references/shablon.md`.
- Oxirida ikki narsa bo'ladi: **Definition of Done** va **Manbalar** (o'qilgan
  config, qo'llanma bo'limlari, PDF sahifalari).
- Chatga reja ko'chirilmaydi: 5–10 qatorlik xulosa + fayl yo'li + eng muhim
  qaror va eng katta risk aytiladi.

## Yakuniy tekshiruv (7-bosqich)

Rejani berishdan oldin har bir bandga "ha" deb javob berilishi kerak. Bitta
"yo'q" bo'lsa — reja tuzatiladi, keyin beriladi.

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

## Yomon reja belgilari

- "optimallashtiramiz", "yaxshilaymiz", "refaktor qilamiz" — fe'l aniq emas
- 20 qadam, lekin birinchi qadamdan keyin loyiha kompilyatsiya bo'lmaydi
- pattern nomlari ko'p, lekin birortasi `fayl:qator` ga bog'lanmagan
- "coverage 80% bo'lsin" — lekin loyihada gate 100% yoki umuman yo'q
- `TAXMIN:` yo'q, lekin reja o'qilmagan fayl haqida gapiradi
- o'qiydigan odamga "qolganini o'zingiz hal qiling" degan bo'limlar
- o'zgarishlar sonini kamaytirish uchun bitta qadamga 12 fayl tiqilgan
