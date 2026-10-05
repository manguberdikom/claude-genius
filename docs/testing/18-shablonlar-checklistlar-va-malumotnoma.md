<!-- doc: testing | chapter: 18 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

# 18. Shablonlar, checklistlar va ma'lumotnoma (Templates, Checklists & Reference)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

- [18.1 Test strategiyasi hujjati shabloni](#181-test-strategiyasi-hujjati-shabloni)
- [18.2 Test rejasi (test plan) shabloni](#182-test-rejasi-test-plan-shabloni)
- [18.3 Definition of Done namunasi](#183-definition-of-done-namunasi)
- [18.4 Pull request'da test uchun review checklisti](#184-pull-requestda-test-uchun-review-checklisti)
- [18.5 Bug report shabloni](#185-bug-report-shabloni)
- [18.6 Test case va checklist shabloni](#186-test-case-va-checklist-shabloni)
- [18.7 Exploratory testing charter va sessiya hisoboti](#187-exploratory-testing-charter-va-sessiya-hisoboti)
- [18.8 Yangi mikroservis uchun test setup checklisti](#188-yangi-mikroservis-uchun-test-setup-checklisti)
- [18.9 Yangi jamoa a'zosi uchun onboarding checklisti](#189-yangi-jamoa-azosi-uchun-onboarding-checklisti)
- [18.10 Release sign-off checklisti](#1810-release-sign-off-checklisti)
- [18.11 Incident'dan keyin test yozish (postmortem) checklisti](#1811-incidentdan-keyin-test-yozish-postmortem-checklisti)
- [18.12 Tavsiya etilgan kutubxonalar ma'lumotnomasi](#1812-tavsiya-etilgan-kutubxonalar-malumotnomasi)
- [18.13 Nomlash va joylashtirish konvensiyalari](#1813-nomlash-va-joylashtirish-konvensiyalari)
- [18.14 Keng tarqalgan xatolar va tezkor yechimlar](#1814-keng-tarqalgan-xatolar-va-tezkor-yechimlar)
- [18.15 Keyingi o'qish uchun manbalar](#1815-keyingi-oqish-uchun-manbalar)
- [18.16 Arxitektor nazorat ro'yxati](#1816-arxitektor-nazorat-royxati)

</details>



Oldingi boblarda testlash strategiyasining mantiqi, darajalari va arxitekturaga ta'siri muhokama qilindi. Bu bobda esa nazariya emas, balki bevosita ishlatishga tayyor materiallar jamlangan: hujjat shablonlari, checklistlar, kutubxonalar ma'lumotnomasi va eng ko'p uchraydigan muammolar jadvali. Har bir shablonni nusxa olib, loyihangiz nomlari bilan to'ldirib, repozitoriyning `docs/testing/` papkasiga joylashtirish mumkin. Maqsad - jamoada "qanday yozamiz?" savolini muhokamadan chiqarib, kelishilgan standartga aylantirish.

## 18.1 Test strategiyasi hujjati shabloni

Test strategiyasi - bu bitta release uchun emas, butun tizim (yoki domen) uchun yoziladigan uzoq muddatli hujjat. U "nimani qanday darajada tekshiramiz va nega" degan savolga javob beradi. Uni arxitektor QA lead bilan birgalikda yozadi, har chorakda qayta ko'rib chiqadi va versiyalaydi (git tarixida saqlanishi shart).

```markdown
# Test strategiyasi - <tizim/domen nomi>
Versiya: 1.3 | Muallif: <ism> | Oxirgi ko'rib chiqilgan: 2026-10-04
Keyingi ko'rib chiqish: 2027-01-15

## 1. Maqsad va kontekst
- Bu hujjat kimga: <auditoriya>
- Qaysi tizimlarni qamraydi: <servislar ro'yxati>
- Biznes risk profili: <masalan, to'lov oqimi - yuqori, admin panel - o'rta>
- Strategik prinsiplar (3-5 ta jumla): masalan "tez qaytish aloqasi
  qamrov foizidan muhimroq", "har bir incident regression testga aylanadi".

## 2. Qamrov (scope) va qamrovdan tashqari
- Qamrovda: <modullar, integratsiyalar, NFR turlari>
- Qamrovdan tashqari va nega: <masalan, uchinchi tomon SaaS UI'si>

## 3. Test darajalari va mas'uliyat taqsimoti
| Daraja | Nimani tekshiradi | Kim yozadi | Qayerda ishlaydi | Maqsadli vaqt |
|---|---|---|---|---|
| Unit | domen mantiqi, qoidalar | developer | har commit | < 2 min |
| Slice (@WebMvcTest, @DataJpaTest) | adapter qatlami | developer | har commit | < 4 min |
| Integration (Testcontainers) | real DB/broker bilan oqim | developer | har PR | < 12 min |
| Contract | servislar o'rtasidagi kelishuv | ikki jamoa | har PR | < 5 min |
| E2E | kritik biznes yo'llari | QA | nightly + release | < 30 min |
| NFR (yuklama, xavfsizlik) | SLO va zaifliklar | QA + platforma | haftalik | reja bo'yicha |

## 4. Muhitlar
| Muhit | Maqsad | Ma'lumot manbasi | Kim boshqaradi | Qayta tiklash |
|---|---|---|---|---|
| local | developer | Testcontainers | developer | istalgan vaqt |
| ci | PR tekshiruvi | ephemeral | platforma | har run |
| staging | E2E, UAT | anonimlashtirilgan | platforma | kunlik |
| prod | smoke, synthetic | real | platforma | - |

## 5. Test ma'lumotlari
- Yaratish usuli: <fixture builder / Datafaker / Instancio>
- Izolyatsiya qoidasi: <har test o'z tenant/ID'si bilan>
- Shaxsiy ma'lumotlar: prod dump ishlatish TAQIQLANADI; maskalash qoidalari <havola>
- Migratsiyalar: Flyway/Liquibase testda ham ishlaydi, `ddl-auto=none`

## 6. Vositalar va versiya boshqaruvi
- Asosiy stek: <JUnit 5, AssertJ, Mockito, Testcontainers ...>
- Versiyalar Spring Boot BOM tomonidan boshqariladi; BOM tashqarisidagilar
  `<properties>`da markazlashtiriladi.
- Yangi vosita qo'shish tartibi: ADR yozish + arxitektura kengashi roziligi

## 7. Sifat darvozalari (quality gates)
- PR bloklanadi agar: build yiqilsa, yangi kod qamrovi < 80%, yangi
  Sonar blocker/critical, ArchUnit qoidasi buzilsa, flaky test aniqlansa.
- Release bloklanadi agar: E2E smoke yiqilsa, kritik contract buzilsa,
  ochiq Sev-1/Sev-2 bo'lsa, yuklama testi SLO'dan chiqsa.

## 8. Metrikalar
| Metrika | Maqsad | Manba | Ko'rib chiqish |
|---|---|---|---|
| CI yashil build ulushi | > 90% | CI | haftalik |
| PR pipeline davomiyligi (p95) | < 15 min | CI | haftalik |
| Flaky test soni | 0 ochiq | test reporter | haftalik |
| Yangi kod qamrovi | > 80% | JaCoCo | har PR |
| Mutation score (domen) | > 60% | PIT | chorakda |
| Prodga chiqqan defektlar | kamayish trendi | incident tracker | oylik |

## 9. Rollar va mas'uliyat
- Developer: unit/slice/integration testlar, o'z PR'ining yashilligi
- QA engineer: E2E, exploratory, test ma'lumotlari, release sign-off
- QA lead: strategiya, metrikalar, flaky backlog
- Arxitektor: darajalar chegarasi, vositalar, darvozalar, ADR'lar
- SRE/platforma: muhitlar, CI infratuzilmasi, synthetic monitoring

## 10. Risklar va yumshatish choralari
| Risk | Ta'sir | Ehtimollik | Chora |
|---|---|---|---|
| E2E suite sekinlashuvi | release kechikadi | o'rta | nightly'ga ko'chirish, parallel run |
| Legacy modulda test yo'q | regressiya | yuqori | har o'zgarishda "test qarzi" to'lash qoidasi |

## 11. Kelishilmagan/ochiq masalalar
- <masalan: UI testlar uchun Playwright yoki Selenide - qaror kutilmoqda,
  mas'ul: <ism>, muddat: <sana>>
```

## 18.2 Test rejasi (test plan) shabloni

Strategiya uzoq muddatli bo'lsa, test rejasi bitta release yoki epic uchun yoziladi va bir sahifadan oshmasligi kerak. Agar reja ikki sahifaga chiqsa, demak epic juda katta bo'lgan.

```markdown
# Test rejasi - <epic/release nomi>
Jira: <EPIC-123> | QA mas'ul: <ism> | Sana: <...>

## Nima o'zgaradi
<2-3 jumla: funksional o'zgarish va unga tegadigan modullar>

## Ta'sir doirasi (impact)
- O'zgargan servislar: <...>
- Ta'sirlanadigan integratsiyalar: <...>
- DB migratsiyalari: <bor/yo'q, orqaga qaytarish strategiyasi>

## Test yondashuvi
| Daraja | Nimani qoplaydi | Kim | Holat |
|---|---|---|---|
| Unit | <...> | dev | reja |
| Integration | <...> | dev | reja |
| Contract | <...> | dev | reja |
| E2E | <kritik 3 ta yo'l> | QA | reja |
| Exploratory | <charter havolasi> | QA | reja |
| NFR | <yuklama/xavfsizlik> | QA | reja |

## Test ma'lumotlari va muhit
<kerakli hisoblar, feature flag holati, tashqi stublar>

## Riskka asoslangan ustuvorlik
- P1: <to'lov hisob-kitobi> - maksimal qamrov
- P2: <bildirishnoma yuborish> - happy path + 1 xato holati
- P3: <UI matnlari> - faqat exploratory

## Chiqish mezonlari (exit criteria)
- [ ] Barcha P1 ssenariylari o'tdi
- [ ] Ochiq Sev-1/Sev-2 yo'q
- [ ] Yangi kod qamrovi darvozasi o'tdi
- [ ] Feature flag o'chirilgan holatda ham regressiya yo'q

## Rollback rejasi
<flag o'chirish / oldingi versiyaga qaytish / migratsiya orqaga>
```

## 18.3 Definition of Done namunasi

DoD - jamoa kelishuvi, uni PR shablonida takrorlash foydali. Quyidagi namuna Spring xizmatlari uchun minimal va real ishlaydigan variant.

```markdown
## Definition of Done

Kod
- [ ] Qabul mezonlari bajarildi, feature flag bilan himoyalangan
- [ ] Kod review o'tdi (kamida 1 ta approve), sharhlar yopildi
- [ ] Statik analiz yangi blocker/critical keltirmadi
- [ ] Public API orqaga moslik buzilmadi yoki versiyalandi

Test
- [ ] Domen mantiqi unit testlar bilan qoplangan (xato holatlari ham)
- [ ] Yangi adapter uchun slice yoki integration test bor
- [ ] Tashqi servis chaqiruvi contract yoki WireMock stub bilan tekshirildi
- [ ] Yangi kod qamrovi >= 80%, mutation score domenda tushmadi
- [ ] Hech bir test `@Disabled` yoki `Thread.sleep` bilan qoldirilmadi

Hujjat
- [ ] README/OpenAPI yangilandi
- [ ] Arxitektura qaroriga ta'sir qilsa - ADR yozildi
- [ ] Runbook'da yangi failure mode tasvirlandi

Kuzatuvchanlik (observability)
- [ ] Muhim oqim uchun metrika va structured log qo'shildi
- [ ] Trace span'lar uzilmagan (tashqi chaqiruvlar instrumentlangan)
- [ ] Alert yoki SLO ta'siri ko'rib chiqildi

Xavfsizlik
- [ ] Avtorizatsiya qoidalari testda tekshirildi (401/403 holatlari)
- [ ] Input validatsiyasi va xato javoblari sir oshkor qilmaydi
- [ ] Yangi bog'liqlik CVE skaneridan o'tdi, maxfiy ma'lumot kodda yo'q
```

## 18.4 Pull request'da test uchun review checklisti

Bu checklist review paytida "test bor" degan yuzaki tekshiruvdan "test foydali" degan baholashga o'tish uchun. Uni PR shabloniga joylashtirish yoki reviewer uchun alohida hujjat qilib saqlash mumkin.

- [ ] Test to'g'ri darajada yozilgan: domen qoidasi uchun unit, HTTP marshrutlash uchun slice, SQL uchun Testcontainers
- [ ] Butun Spring kontekstini ko'tarmasdan hal qilinadigan narsa uchun `@SpringBootTest` ishlatilmagan
- [ ] Test nomi "nima qilinganda nima bo'ladi" ni aytadi, `test1` yoki `shouldWork` emas
- [ ] Assertion mazmunli: `assertThat(result.status()).isEqualTo(REJECTED)` ko'rinishida, `assertNotNull` bilan cheklanmagan
- [ ] Bitta testda bitta xulosa tekshirilgan, 20 qatorlik assertion to'dasi yo'q
- [ ] Mock faqat chegaradagi bog'liqliklar uchun; domen obyektlari mock qilinmagan
- [ ] `verify(...)` chaqiruvlari natijani emas, faqat haqiqatan muhim yon ta'sirni tekshiradi
- [ ] Test o'z ma'lumotini o'zi yaratadi; boshqa test qoldirgan holatga tayanmaydi
- [ ] Ma'lumot izolyatsiyasi ta'minlangan (tranzaksiya rollback, unikal kalit yoki tozalash)
- [ ] Testlar istalgan tartibda ishlaydi; `@Order` yoki `@TestMethodOrder` asossiz ishlatilmagan
- [ ] Vaqtga bog'liqlik `Clock` orqali boshqariladi, `LocalDateTime.now()` to'g'ridan-to'g'ri ishlatilmagan
- [ ] Asinxron kutish `Awaitility` bilan, `Thread.sleep` bilan emas
- [ ] Tashqi tarmoqqa real chaqiruv yo'q (WireMock/Testcontainers orqali izolyatsiya)
- [ ] Random ma'lumot ishlatilsa, seed fiksirlangan yoki natija randomga bog'liq emas
- [ ] Test taxminan 1 sekunddan oshsa, sababi tushunarli va tegishli tag bilan belgilangan
- [ ] Xato va chegara holatlari qoplangan: bo'sh ro'yxat, null, limitdan oshish, duplikat
- [ ] Exception tekshiruvi turi va xabari bilan, `assertThatThrownBy` orqali
- [ ] Takrorlanuvchi setup fixture builder yoki `@TestConfiguration` ichida jamlangan
- [ ] Testda biznes mantiqining nusxasi yo'q (kutilgan natija qo'lda yozilgan)
- [ ] O'chirilgan yoki kommentga olingan test qolmagan
- [ ] Yangi testlar mavjud tag/konvensiyaga mos (`@Tag("integration")` va h.k.)
- [ ] Testcontainers konteynerlari qayta ishlatiladi (statik yoki shared), har metodda qayta ko'tarilmaydi
- [ ] Test xabarlari yiqilganda diagnostika beradi (AssertJ `as("...")` yoki soft assertions)
- [ ] CI'da flaky bo'lish ehtimoli baholangan (tarmoq, vaqt, tartib, parallel)
- [ ] Agar bu bugfix bo'lsa - avval yiqiladigan regression test qo'shilgan

## 18.5 Bug report shabloni

```text
Sarlavha: [Sev-2][Payments] Takroriy webhook ikkinchi to'lovni yaratadi

Muhit: staging, build 2026.10.3-rc2, PostgreSQL 16, feature flag: payments.v2=on
Qurilma/klient: curl / Postman
Topilgan vaqt: 2026-10-03 14:22 (UTC+5)
Topuvchi: <ism> | Mas'ul jamoa: payments

Oldingi shartlar:
  1. CONFIRMED holatidagi buyurtma mavjud (orderId=1042)
  2. Provider webhook secret konfiguratsiya qilingan

Takrorlash qadamlari:
  1. POST /webhooks/psp (payload A, eventId=evt_77) -> 200
  2. Xuddi shu payloadni qayta yuborish (eventId=evt_77) -> 200

Kutilgan natija:
  Ikkinchi chaqiruv idempotent: yangi Payment yozuvi yaratilmaydi,
  javob 200, log'da "duplicate event ignored".

Haqiqiy natija:
  payments jadvalida 2 yozuv (id=551, 552), balans ikki baravar yechilgan.

Ta'sir: moliyaviy xatolik, mijozdan ortiqcha pul yechilishi mumkin.
Chastota: 3/3 (har safar takrorlanadi)
Loglar/trace: trace_id=9f1c..., havola <...>
Qo'shimcha: eventId uchun unique constraint yo'q (V12 migratsiyada qo'shilmagan)
Regression test talab qilinadi: HA (PaymentWebhookIdempotencyIT)
```

## 18.6 Test case va checklist shabloni

Batafsil test case'lar faqat yuqori riskli oqimlar uchun yoziladi; qolgan joyda yengil checklist yetarli.

```text
TC-PAY-014 | Idempotent webhook qayta ishlash
Daraja: integration | Ustuvorlik: P1 | Avtomatlashtirilgan: HA
Oldingi shart: CONFIRMED buyurtma, PSP stub WireMock'da
Qadamlar:
  1. Webhook eventId=evt_77 bilan yuboriladi
  2. Xuddi shu event qayta yuboriladi
Kutilgan natija:
  - HTTP 200 ikki marta
  - payments jadvalida aynan 1 yozuv
  - outbox'da 1 ta PaymentCaptured event
Tozalash: tranzaksiya rollback (test o'z schema'sida)
```

```text
CHECKLIST: yangi REST endpoint
- [ ] Happy path 2xx va javob sxemasi
- [ ] Validatsiya xatolari 400 va xato formati (RFC 7807)
- [ ] Autentifikatsiyasiz 401, ruxsatsiz rol bilan 403
- [ ] Mavjud bo'lmagan resurs 404
- [ ] Idempotentlik (PUT/POST retry)
- [ ] Sahifalash chegaralari: 0, 1, maksimal limit
- [ ] Katta payload va noto'g'ri Content-Type
- [ ] OpenAPI hujjati haqiqatga mos
```

## 18.7 Exploratory testing charter va sessiya hisoboti

Exploratory testing tartibsiz "o'ynash" emas - u vaqt bilan cheklangan, maqsadi yozilgan va natijasi hisobot bo'lgan ish usuli.

```text
CHARTER
Maqsad: To'lovni qaytarish (refund) oqimini chegara holatlarida o'rganish
Qamrov: POST /refunds, admin UI "Refund" tugmasi
Vositalar: Postman, DB konsoli, Toxiproxy (kechikish simulyatsiyasi)
Vaqt: 90 daqiqa
Riskka gipoteza: qisman qaytarishlar yig'indisi asl summadan oshishi mumkin

SESSIYA HISOBOTI
Sana/tester: 2026-10-03 / <ism>   Sarflangan vaqt: 85 daqiqa
Taqsimot: test dizayni 60% | bug tekshirish 25% | setup 15%
Qamrab olindi: qisman qaytarish, to'liq qaytarish, takroriy qaytarish,
  PSP kechikishi 5s, valyuta farqi
Topilganlar:
  - BUG-884 (Sev-2): 3 ta qisman qaytarish asl summadan oshdi
  - BUG-885 (Sev-4): xato xabari texnik stack trace ko'rsatadi
Savollar/risklar: PSP timeout'dan keyin holat noaniq qoladi - runbook yo'q
Keyingi charter taklifi: refund + chargeback kombinatsiyasi
```

## 18.8 Yangi mikroservis uchun test setup checklisti

Yangi servis birinchi kundan to'g'ri sozlanmasa, keyin tuzatish bir necha hafta oladi. Quyidagilar repozitoriy yaratilgan kunning o'zida bajarilishi kerak.

- [ ] `spring-boot-starter-test` qo'shilgan, `spring-security-test` xavfsizlik bo'lsa
- [ ] `org.testcontainers:junit-jupiter` va kerakli modullar (`postgresql`, `kafka`) qo'shilgan
- [ ] `spring-boot-testcontainers` orqali `@ServiceConnection` ishlatilgan (manual property yo'q)
- [ ] ArchUnit (`com.tngtech.archunit:archunit-junit5`) va kamida 3 ta qoida: qatlam yo'nalishi, paket bog'liqligi, test nomlash
- [ ] Bazaviy sinflar yaratilgan: `AbstractIntegrationTest` (konteynerlar, shared context), `AbstractWebMvcTest`, `AbstractRepositoryTest`
- [ ] Fixture builder/`Instancio` konvensiyasi kelishilgan, `TestDataFactory` bor
- [ ] `application-test.yml`: `ddl-auto=none`, Flyway yoqilgan, tashqi URL'lar stubga qaratilgan
- [ ] WireMock yoki contract stub runner tashqi bog'liqlik uchun sozlangan
- [ ] CI job'lari: `build-and-unit` (har push), `integration` (har PR), `contract` (har PR), `nightly-e2e`, `weekly-load`, `mutation` (chorakda yoki nightly)
- [ ] JaCoCo report + `check` goal, yangi kod qamrovi darvozasi yoqilgan
- [ ] Darvozalar birinchi kundan: build yashil, qamrov minimumi, statik analiz, ArchUnit, bog'liqlik CVE skaneri
- [ ] Test tag'lari va Maven profillari (`-Pintegration`) ishlaydi, lokalda hujjatlashtirilgan
- [ ] Flaky test reporter yoki retry faqat belgilangan tag uchun yoqilgan (yashirish uchun emas)
- [ ] `README` ichida "testlarni qanday ishga tushirish" bo'limi bor

## 18.9 Yangi jamoa a'zosi uchun onboarding checklisti

- [ ] Test strategiyasi hujjatini o'qidi va savollarini yozdi
- [ ] Lokalda butun test suite'ni ishga tushirdi (Docker ishlashini tekshirdi)
- [ ] Har bir test darajasidan bittasini ochib, nima uchun shu daraja tanlangani tushuntirdi
- [ ] Fixture builder va `TestDataFactory` bilan bitta yangi test yozdi
- [ ] Bitta mavjud testni ataylab buzib, xato xabarining o'qilishini ko'rdi
- [ ] PR test review checklistidan foydalanib birinchi review qildi
- [ ] Flaky test backlog'ini ko'rib chiqdi va bittasini tuzatdi
- [ ] CI pipeline bosqichlarini va darvozalarni tushuntirib bera oladi
- [ ] Incident -> regression test jarayonini bilib oldi
- [ ] Mentor bilan birinchi exploratory sessiyada qatnashdi

## 18.10 Release sign-off checklisti

- [ ] Barcha reja qilingan P1/P2 test ssenariylari o'tdi
- [ ] Ochiq Sev-1/Sev-2 defekt yo'q; Sev-3 lar ro'yxati kelishilgan
- [ ] Nightly E2E va smoke suite oxirgi build'da yashil
- [ ] Contract testlar barcha iste'molchilar uchun o'tdi
- [ ] DB migratsiyalari staging'da ishladi va rollback sinovdan o'tdi
- [ ] Yuklama testi SLO chegaralarida (p95 latency, error rate)
- [ ] Xavfsizlik skaneri yangi critical topmadi
- [ ] Feature flag holatlari hujjatlashtirilgan (kim, qachon yoqadi)
- [ ] Monitoring/alert dashboardlari yangi metrikalarni ko'rsatadi
- [ ] Rollback rejasi yozilgan va mas'ul tayinlangan
- [ ] Release notes va ma'lum cheklovlar ro'yxati tayyor
- [ ] Sign-off: QA lead, arxitektor, product owner imzolari

## 18.11 Incident'dan keyin test yozish (postmortem) checklisti

Qoida oddiy: har bir prodga chiqqan incident kamida bitta avtomatlashtirilgan regression test qoldiradi. Test yozilmagan postmortem yopilmaydi.

- [ ] Incident'ning aniq texnik sababi bir jumlada yozilgan
- [ ] Nega mavjud testlar ushlab qolmadi - javob yozilgan (qamrov bo'shlig'i, noto'g'ri daraja, mock haqiqatni yashirgan)
- [ ] Muammoni takrorlaydigan test yozildi va u tuzatishdan OLDIN yiqildi
- [ ] Test eng past mumkin bo'lgan darajada (agar unit yetsa, E2E yozilmadi)
- [ ] Test nomida incident ID bor (masalan `shouldNotDoubleCharge_INC_412`)
- [ ] Agar sabab integratsiya chegarasida bo'lsa - contract test yangilandi
- [ ] Agar sabab konfiguratsiyada bo'lsa - konfiguratsiya validatsiya testi qo'shildi
- [ ] Agar sabab yuklama ostida yuzaga kelgan bo'lsa - yuklama ssenariysi qo'shildi
- [ ] Monitoring/alert qo'shildi, test uni ham qoplaydi (metrika chiqishini tekshirish)
- [ ] Shu sinf xatolar uchun ArchUnit yoki statik qoida qo'shish mumkinmi - baholandi
- [ ] Postmortem'da test havolasi ko'rsatilgan, PR merge qilindi
- [ ] Yangi test flaky emasligi 20 marta ketma-ket run bilan tekshirildi

## 18.12 Tavsiya etilgan kutubxonalar ma'lumotnomasi

Muhim ogohlantirish: aksariyat kutubxonalar versiyasini Spring Boot BOM (`spring-boot-dependencies`) boshqaradi - `pom.xml`da `<version>` yozish kerak EMAS va zararli. Pastdagi jadvalda "BOM" degani shu. BOM tashqarisidagilar uchun faqat taxminiy major versiya ko'rsatilgan; aniq versiyani Maven Central'dan tekshiring.

| Maqsad | Kutubxona | Maven coordinate | Izoh |
|---|---|---|---|
| Test engine | JUnit 5 | `org.junit.jupiter:junit-jupiter` | BOM; starter-test ichida keladi |
| Assertion | AssertJ | `org.assertj:assertj-core` | BOM; fluent, o'qiladigan xabarlar |
| Mock | Mockito | `org.mockito:mockito-core`, `mockito-junit-jupiter` | BOM; faqat chegaralar uchun |
| Umumiy to'plam | Spring Boot test starter | `org.springframework.boot:spring-boot-starter-test` | JUnit 5, AssertJ, Mockito, Hamcrest, JSONassert, JsonPath, XMLUnit, spring-test, Awaitility |
| Xavfsizlik testi | Spring Security Test | `org.springframework.security:spring-security-test` | BOM; `@WithMockUser`, SecurityMockMvc |
| Real bog'liqliklar | Testcontainers | `org.testcontainers:junit-jupiter`, `:postgresql`, `:kafka`, `:mongodb`, `:localstack` | BOM; Docker talab qiladi |
| Boot integratsiyasi | Spring Boot Testcontainers | `org.springframework.boot:spring-boot-testcontainers` | BOM; `@ServiceConnection` |
| HTTP stub | WireMock | `org.wiremock:wiremock-standalone` | BOM tashqarisida, 3.x |
| Contract (Spring) | Spring Cloud Contract | `org.springframework.cloud:spring-cloud-starter-contract-verifier`, `...-stub-runner` | Spring Cloud BOM boshqaradi |
| Contract (til-neytral) | Pact JVM | `au.com.dius.pact.consumer:junit5`, `au.com.dius.pact.provider:junit5spring` | 4.x; broker bilan |
| REST API testi | RestAssured | `io.rest-assured:rest-assured` | BOM; E2E/API darajasi |
| Brauzer (modern) | Playwright | `com.microsoft.playwright:playwright` | 1.x; tez, auto-wait |
| Brauzer (Selenium ustida) | Selenide | `com.codeborne:selenide` | 7.x; qisqa API |
| Asinxron kutish | Awaitility | `org.awaitility:awaitility` | BOM; `Thread.sleep` o'rniga |
| Soxta ma'lumot | Datafaker | `net.datafaker:datafaker` | 2.x; ism, manzil, IBAN |
| Obyekt generatsiyasi | Instancio | `org.instancio:instancio-junit` | 5.x; to'ldirilgan POJO |
| Arxitektura qoidalari | ArchUnit | `com.tngtech.archunit:archunit-junit5` | 1.x; qatlam va paket qoidalari |
| Modullar | Spring Modulith test | `org.springframework.modulith:spring-modulith-starter-test` | Modulith BOM; `@ApplicationModuleTest` |
| Qamrov | JaCoCo | `org.jacoco:jacoco-maven-plugin` | 0.8.x; plugin |
| Mutation testing | PIT | `org.pitest:pitest-maven` + `org.pitest:pitest-junit5-plugin` | plugin; testlar sifatini o'lchaydi |
| Yuklama (JVM) | Gatling | `io.gatling:gatling-maven-plugin` (+ gatling-charts-highcharts) | 4.x atrofida |
| Yuklama (skript) | k6 | Maven artefakti yo'q (Grafana k6 binary) | JS skript, CI'da konteyner |
| Hisobot | Allure | `io.qameta.allure:allure-junit5` (+ `allure-maven`) | 2.x |
| Tarmoq nosozligi | Toxiproxy | `org.testcontainers:toxiproxy` | BOM; kechikish, uzilish |
| Resilience sinovi | Chaos Monkey for Spring Boot | `de.codecentric:chaos-monkey-spring-boot` | 3.x; faqat non-prod profil |

## 18.13 Nomlash va joylashtirish konvensiyalari

| Element | Konvensiya | Namuna |
|---|---|---|
| Unit test sinfi | `<Sinf>Test` | `OrderPricingServiceTest` |
| Integration test sinfi | `<Mavzu>IT` | `OrderRepositoryIT` |
| Slice (web) test | `<Controller>Test` + `@WebMvcTest` | `OrderControllerTest` |
| Contract (provider) | `<Consumer>ContractTest` | `MobileAppContractTest` |
| E2E test | `<Oqim>E2ETest` | `CheckoutFlowE2ETest` |
| Arxitektura testi | `ArchitectureTest` / `<Qoida>ArchTest` | `LayerDependencyArchTest` |
| Test metodi | `should<Natija>_when<Shart>` | `shouldRejectOrder_whenStockIsEmpty()` |
| Muqobil metod uslubi | `given...when...then...` (bitta uslub tanlang) | `givenEmptyStock_whenOrder_thenRejected()` |
| Paket | Production bilan bir xil paket | `com.acme.orders.pricing` |
| Fayl joyi | `src/test/java/...` | - |
| Resurslar | `src/test/resources/` | `__files/psp/capture-200.json` |
| Fixture/builder | `<Entity>TestDataBuilder` yoki `<Entity>Fixtures` | `OrderTestDataBuilder` |
| Bazaviy sinflar | `support/` yoki `testsupport/` subpaketi | `com.acme.support.AbstractIntegrationTest` |
| Tag'lar | `unit` (default, tagsiz), `integration`, `contract`, `e2e`, `slow`, `flaky-quarantine` | `@Tag("integration")` |
| Maven profil | tag bilan bir xil nom | `mvn verify -Pintegration` |

## 18.14 Keng tarqalgan xatolar va tezkor yechimlar

| Simptom | Ehtimoliy sabab | Yechim |
|---|---|---|
| Kontekst ko'tarilmayapti (`ApplicationContextFailure`) | Yetishmayotgan bean, noto'g'ri property, bir nechta nomos `@MockBean` kombinatsiyasi | Xato stack'ining ENG CHUQUR `Caused by`ni o'qing; `@SpringBootTest` o'rniga slice test; `--debug` bilan auto-configuration reportini ko'ring |
| `LazyInitializationException` testda | Tranzaksiya tashqarisida lazy kolleksiyaga murojaat | Testda `@Transactional`, yoki `JOIN FETCH`/entity graph, yoki DTO proyeksiyasi bilan tekshirish |
| Test lokalda o'tadi, CI'da yiqiladi | Vaqt zonasi, locale, fayl tartibi, sekinlik, parallel run, Docker resurslari | CI va lokalni bir xil `-Duser.timezone=UTC -Duser.language=en` bilan ishga tushirish; vaqtni `Clock` orqali; tartibga tayanchni olib tashlash |
| `Could not find a valid Docker environment` | Docker demon ishlamaydi yoki socket boshqa yo'lda (Colima/Podman/Rancher) | Docker'ni yoqish; `DOCKER_HOST` yoki `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` sozlash; CI'da privileged runner yoki DinD |
| MockMvc 403 qaytaradi | CSRF yoqilgan yoki foydalanuvchi yo'q | POST uchun `with(csrf())`; `@WithMockUser(roles=...)`; `SecurityMockMvcRequestPostProcessors` ishlatish |
| `@MockBean` deprecated ogohlantirishi | Spring Framework 6.2 / Boot 3.4'dan keyin yangi API | `@MockitoBean` va `@MockitoSpyBean`ga o'tish (`org.springframework.test.context.bean.override.mockito`) |
| Testlar bir-biriga xalaqit beradi | Umumiy DB holati, static field, cache, yoqilgan scheduler | Har test o'z ma'lumotini yaratadi; `@Transactional` rollback; `@DirtiesContext` faqat chora sifatida; cache va scheduler'ni test profilida o'chirish |
| H2'da ishlagan SQL PostgreSQL'da yiqildi | Dialekt farqi: `ON CONFLICT`, `jsonb`, window funksiyalar, `LIMIT` sintaksisi, type casting | H2'dan voz kechish; Testcontainers PostgreSQL ishlatish; migratsiyalarni real DB'da tekshirish |
| Har test konteyner ko'taradi, suite sekin | Konteyner lifecycle noto'g'ri | `static` container + `@Testcontainers`, yoki singleton container pattern; `@ServiceConnection` bilan bitta shared context |
| `Port already in use` | `@SpringBootTest(webEnvironment = DEFINED_PORT)` yoki qotib qolgan port | `RANDOM_PORT` + `@LocalServerPort`; WireMock uchun `0` porti va dinamik property |
| Asinxron natija "hali kelmagan" | Event/listener alohida thread'da | `Awaitility.await().atMost(...).untilAsserted(...)`; `@TransactionalEventListener` bo'lsa commit'ni kutish |
| Jackson testda boshqa natija beradi | Test `ObjectMapper`ni qo'lda yaratgan, Boot konfiguratsiyasi qo'llanmagan | `@JsonTest` yoki kontekstdan `ObjectMapper` inject qilish |
| Flyway testda migratsiyani topmaydi yoki checksum xatosi | Test uchun qo'shimcha migratsiyalar, o'zgargan fayl | Test migratsiyalarini alohida `locations`ga ajratish; mavjud migratsiyani tahrirlamaslik, yangisini qo'shish |
| Qamrov hisoboti bo'sh | JaCoCo agent `argLine` bilan to'qnashgan (Surefire, Lombok, agentlar) | Surefire `argLine`ga `@{argLine}` qo'shish; `prepare-agent` fazasi tartibini tekshirish |
| Parallel run'da random yiqilishlar | Shared mutable holat, bir xil DB nomi, port to'qnashuvi | Parallelizmni sinf darajasida cheklash; har thread uchun alohida schema/tenant; `@ResourceLock` |

## 18.15 Keyingi o'qish uchun manbalar

| Manba | Turi | Nega foydali |
|---|---|---|
| Gerard Meszaros, *xUnit Test Patterns* | Kitob | Test smells va fixture pattern'larining eng to'liq katalogi; nomlash va tozalash muammolarida ma'lumotnoma |
| Michael Feathers, *Working Effectively with Legacy Code* | Kitob | Testsiz legacy kodga seam yaratib test kiritish texnikalari - Spring monolitlarini bo'lishda bevosita qo'llanadi |
| Freeman & Pryce, *Growing Object-Oriented Software, Guided by Tests* | Kitob | Testlar dizaynni qanday boshqarishi va mock'ning o'rni haqida eng aniq tushuntirish |
| Vladimir Khorikov, *Unit Testing: Principles, Practices, and Patterns* | Kitob | Yaxshi testning to'rt ustuni va "nimani mock qilmaslik" bo'yicha amaliy mezonlar |
| Ham Vocke, "The Practical Test Pyramid" (martinfowler.com) | Maqola | Piramidani Spring kontekstida bosqichma-bosqich tushuntiradi; jamoaga o'qitish uchun qisqa material |
| Spring Framework va Spring Boot rasmiy testing hujjati | Hujjat | Kontekst keshi, slice annotatsiyalari va bean override semantikasi bo'yicha yagona ishonchli manba |
| Testcontainers rasmiy hujjati | Hujjat | Modullar ro'yxati, singleton container pattern, CI sozlamalari va `@ServiceConnection` integratsiyasi |

## 18.16 Arxitektor nazorat ro'yxati

- [ ] Test strategiyasi hujjati repozitoriyda, versiyalangan va oxirgi 3 oy ichida ko'rib chiqilgan
- [ ] PR test review checklisti amalda ishlatiladi (faqat qog'ozda emas) va PR shablonida mavjud
- [ ] Definition of Done'da test, kuzatuvchanlik va xavfsizlik bandlari bor hamda darvozalar bilan bog'langan
- [ ] Yangi servis uchun test setup checklisti shablon repozitoriyda avtomatlashtirilgan
- [ ] Har bir Sev-1/Sev-2 incident regression test bilan yopilgan - bu metrika sifatida kuzatiladi
- [ ] Kutubxona versiyalari Spring Boot BOM orqali boshqariladi, BOM tashqarisidagilar markazlashtirilgan
- [ ] Nomlash va tag konvensiyalari ArchUnit qoidasi bilan majburlanadi
- [ ] Flaky testlar uchun ko'rinadigan backlog va mas'ul shaxs tayinlangan

---

[&larr; 17. Metrikalar va test yetukligi modeli](17-metrikalar-va-test-yetukligi-modeli.md) · [Mundarija](README.md)
