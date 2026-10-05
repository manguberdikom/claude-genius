# 5-bosqich: test strategiyasi va sifat darvozasi

Bu bosqichda reja test injener ko'zi bilan o'qiladi. Natija ikki artefakt:
**test matritsasi** (nima o'zgaradi -> qanday tekshiriladi) va **quality gate
talablari** (o'zgarish Sonar/CI dan o'tishi uchun nima kerak).

Qoida: **"test yozish" degan qadam yo'q.** Har test uchun to'rt narsa aytiladi:
daraja, joy, ma'lumot, oracle (kutilgan natija). Oracle yo'q test - yolg'on
xotirjamlik.

## 5.1 Test matritsasi formati

| O'zgarish | Daraja | Joy | Ma'lumot | Oracle |
|---|---|---|---|---|
| `PaymentHandler` strategiya registri | unit | `PaymentHandlerRegistryTest` | har turga bitta stub handler | noma'lum tur -> `IllegalArgumentException`; `CARD` -> `CardHandler` |
| Outbox yozuvi tranzaksiyada | integratsion (`@SpringBootTest` + Testcontainers, test metodida `@Transactional` yo'q) | `OutboxWriteIT` | buyruq + outbox yozilgandan keyin majburiy xato | muvaffaqiyat -> `orders` va `outbox` da 1 tadan qator; xato -> ikkalasida 0 qator (`JdbcTemplate` bilan tashqaridan sanaladi) |
| Publisher Kafka ga jo'natadi | integratsion (Testcontainers) | `OutboxPublisherIT` | 2 jo'natilmagan qator | ikkisi ham topic'da; `sent_at` to'ldirilgan |
| Takroriy xabar | integratsion | `OrderConsumerIT` | bir xil `request_id` bilan 2 xabar | DB da 1 buyruq; ikkinchisi e'tiborsiz |
| Tashqi servis timeout | integratsion + WireMock | `PaymentClientIT` | read timeoutdan uzun `withFixedDelay` stub; test profilida timeout 200 ms, backoff 0 | `TimeoutException`; WireMock 3 so'rovni ko'rgan (1 + 2 retry) |
| Yangi endpoint kontrakti | slice (`@WebMvcTest`) | `OrderControllerTest` | noto'g'ri body | 400 + xato formati o'zgarmagan |
| Migratsiya | migratsiya testi | `MigrationIT` | bo'sh va to'liq baza | N-1 versiyagacha ko'tarilib ma'lumot qo'yilgan bazada yangi migratsiya o'tadi; N-1 kod yangi sxemada ishlaydi |

## 5.2 Daraja tanlash

Piramida qoidasi (testlash: `Test piramidasi va test turlari xaritasi`): past darajada mumkin bo'lsa, yuqorida
yozilmaydi. Spring kontekstini ko'tarish - test sekinligining asosiy manbasi
(patternlar: `@SpringBootTest for Everything`).

| Nimani tekshiramiz | Daraja | Vosita | Qarash |
|---|---|---|---|
| Sof logika, shart, hisob, validatsiya qoidasi | unit, kontekstsiz | JUnit 5 + Mockito | testlash: `Unit test`, `Unit test Spring loyihasida` |
| Controller: marshrutlash, serializatsiya, status, validatsiya | slice | `@WebMvcTest` | testlash: `Integratsion test` |
| Repository: so'rov, mapping, indeks ishlashi | slice + real DB | `@DataJpaTest` + Testcontainers | testlash: `Integratsion test`, `Testcontainers bilan real infratuzilmada test` |
| Tranzaksiya chegarasi, rollback, lock | integratsion | `@SpringBootTest` + Testcontainers | testlash: `Xavfsizlik, tranzaksiya, asinxron va konkurentlik testlari` |
| Broker bilan oqim (producer/consumer) | integratsion | Testcontainers Kafka | testlash: `Testcontainers bilan real infratuzilmada test` |
| Migratsiya: N-1 dan ko'tarilish, eski kod yangi sxemada | migratsiya testi | Flyway + Testcontainers | testlash: `Ma'lumotlar bazasi migratsiyasini testlash` |
| Tashqi HTTP servis xulqi (timeout, 500, sekinlik) | unit/integratsion | WireMock | testlash: `Tashqi servislarni taqlid qilish va contract testing` |
| Tashqi kontrakt buzilmasligi | contract test | Spring Cloud Contract / Pact | testlash: `Tashqi servislarni taqlid qilish va contract testing`; patternlar: `Contract Testing` |
| Foydalanuvchi oqimi | E2E (kam sonda) | REST-assured / Playwright | testlash: `End-to-end va UI testlar` |
| Yuklama, chidamlilik | nofunksional | k6/Gatling, chaos | testlash: `Nofunksional testlar` |
| Arxitektura qoidasi (qatlam, tsikl, nomlash) | arxitektura testi | ArchUnit | testlash: `Arxitektura testlari va kod sifati darvozalari` |
| Coverage yolg'on emasligi | mutation | PIT | sonarqube: `Mutation testing`; patternlar: `Mutation Testing` |

Qoida: **bitta xulq bitta darajada tekshiriladi.** Bir xil shartni unit va E2E da
ikki marta tekshirish - ikki marta saqlash xarajati.

Matritsa tugagandan keyin u to'liqlik ko'zi bilan qayta o'qiladi (review:
`Test to'liqligini review qilish`): chegara qiymatlari, bo'sh va bitta elementli
holat, xato yo'li, takroriy chaqiruv va ruxsat yetmagan foydalanuvchi
qoldirilmaganmi. Qoldirilgan holat bilib qoldirilsa, sababi matritsada bitta
qator bo'lib qoladi.

## 5.3 Test ma'lumoti

- Qurilish takrorlanadigan bo'lsa - Test Data Builder (patternlar: `Test Data Builder`) yoki
  Object Mother (patternlar: `Object Mother`). Rejada builder qayerda turishi aytiladi.
- Umumiy mutable fixture ishlatilmaydi: test tartibiga bog'liqlik paydo bo'ladi
  (testlash: `Flaky testlar, test qarzi va test kodini saqlash`).
- Real ma'lumot nusxasi ishlatilsa, shaxsiy ma'lumot maskalanadi (testlash: `Test ma'lumotlarini boshqarish`).
- Har test o'z ma'lumotini yaratadi va tozalaydi; `@Sql` yoki builder - tanlov
  rejada aytiladi.

## 5.4 Test qiyin joylar uchun reja

Kod o'zgarmasdan test yozilmaydigan holatlar rejada **alohida qadam** bo'ladi
(arxitektor: `Legacy kod va bosqichma-bosqich refaktoring`;
sonarqube: `Qamralmay qoladigan kod va unga test yozish`):

| To'siq | Reja qadami |
|---|---|
| `static` chaqiruv (`LocalDate.now()`, util sinflar) | `Clock` bean inject qilinadi; test `Clock.fixed` beradi |
| `new` konstruktor ichida | fabrika yoki konstruktor injection |
| `private` metod murakkab | xulq public API orqali tekshiriladi yoki metod alohida sinfga chiqariladi |
| Tashqi tizim qattiq bog'langan | port interfeysi + adapter (patternlar: `Hexagonal Architecture / Ports & Adapters`) |
| Random / UUID | generator interfeysi yoki seed |
| Thread va vaqt | `Awaitility`, deterministik executor (testlash: `Xavfsizlik, tranzaksiya, asinxron va konkurentlik testlari`) |

## 5.5 Quality gate talablari

Chegaralar **taxmin qilinmaydi** - loyihadan o'qiladi (1-bosqich jadvalidan).
Rejaga aynan shu qiymatlar yoziladi:

| Shart | Loyihadagi qiymat | Manba | Reja uchun ma'nosi |
|---|---|---|---|
| New code coverage | 100% | `sonar-project.properties:12` | yangi/o'zgargan har qator qamralishi kerak |
| Duplication (new code) | 3% | quality gate | ko'chirib-qo'yish o'rniga umumiy metod |
| Cognitive complexity | metodga 15 | quality profile | yangi `switch` ni handler'larga bo'lish |
| Blocker/Critical issue | 0 | gate | yangi `catch(Exception)` yo'q |
| Security hotspot | hammasi ko'rib chiqilgan | gate | yangi tashqi kiritish uchun validatsiya |
| Test muvaffaqiyati | 100% | CI | `@Disabled` qo'shilmaydi |

Agar gate topilmasa: rejada `TAXMIN:` deb yoziladi va birinchi qadamlardan biri -
gate shartlarini aniqlash.

### Exclusion halolligi

Coverage ni `sonar.coverage.exclusions` bilan "yopish" - faqat haqiqatan
mantiqsiz kod uchun (generatsiya qilingan, DTO/record, konfiguratsiya sinflari);
mantiq bor kodni chiqarish aldov (sonarqube: `Exclusion`). Reja exclusion qo'shsa,
sababi va qaysi fayl ekani aniq yoziladi.

## 5.6 O'zgarish turi -> ehtimoliy Sonar qoidalari

Reja qanday kod yozishni aytadi, demak qaysi qoidani buzish xavfi borligini ham
aytadi (sonarqube: `Java va Spring da eng ko'p uchraydigan issue va ularning yechimi`, `Xato katalogi: reliability (bug) toifasi`, `Xato katalogi: test kodidagi xatolar`):

| Reja nima qo'shadi | Xavfdagi qoidalar |
|---|---|
| Yangi `switch` / shartlar | cognitive complexity, takrorlanish (sonarqube: `Cognitive complexity va takrorlanishni kamaytirish`) |
| Yangi tashqi chaqiruv | resurs yopilmasligi, timeout yo'qligi, `InterruptedException` yutilishi (sonarqube: `Xato katalogi: reliability (bug) toifasi`) |
| SQL yoki filtr | SQL injection, taint oqimi (sonarqube: `Xato katalogi: security (vulnerability va hotspot)`, `Taint analysis mexanikasi`) |
| Yangi DTO/record | Lombok/record va coverage (sonarqube: `Lombok, record va generatsiya qilingan kod`) |
| Yangi `@Transactional` | `private`/`self-invocation` xatolari (sonarqube: `Xato katalogi: Spring, JPA va PostgreSQL ga xos xatolar`) |
| Yangi test | assertion yo'qligi, `@Disabled`, test ichida mantiq (sonarqube: `Testning o'zidagi Sonar qoidalari va test sifati`, `Xato katalogi: test kodidagi xatolar`) |
| Yangi log | foydalanuvchi ma'lumotini log qilish, formatlash (sonarqube: `Xato katalogi: security (vulnerability va hotspot)`, `Xato katalogi: maintainability, nomlash, o'lik kod va uslub`) |

## 5.7 CI dagi o'rni

Rejada yangi test turi paydo bo'lsa, u pipeline ga qanday tushishi aytiladi
(testlash: `CI/CD da test pipeline`):

- unit testlar - har push da, PR ni blokirovka qiladi
- integratsion/Testcontainers - PR da, alohida job, timeout bilan
- contract test - provider va consumer tomonida
- E2E / yuklama - kechasi yoki reliz oldidan, PR ni blokirovka qilmaydi
- mutation testing - nightly, o'zgargan modulga

Vaqt budjeti yoziladi: "integratsion job ~4 daqiqa qo'shadi" - pipeline sekinligi
ham narx.

## 5.8 Definition of Done qatorlar

Reja oxiridagi DoD ga shular kiradi (testlash: `Shablonlar, checklistlar va ma'lumotnoma` shabloni bilan mos):

- [ ] Kod o'zgarishlari rejadagi qadamlarga mos, qo'shimchasiz
- [ ] Har yangi xulq uchun test bor va u o'zgarishsiz kodda qulaydi (test avval
      qizil bo'lganini ko'rsatish)
- [ ] `mvn verify` (yoki loyiha buyrug'i) lokalda yashil
- [ ] Quality gate o'tdi (new code coverage, duplication, complexity)
- [ ] `MigrationIT` migratsiyani N-1 holatidagi to'liq bazada o'tkazadi;
      qaytarib bo'lmaydigan qadam (ustun yoki jadval o'chirish, tur
      o'zgartirish) alohida relizda va rejaning Rollback bandida forward fix
      bilan yozilgan (arxitektor:
      `Orqaga qaytish (rollback) rejasi: sxemani qaytarish nega qiyin`)
- [ ] Yangi konfiguratsiya kalitlari hamma muhitga qo'shilgan
- [ ] Log/metrika qo'shilgan va dashboard/alert yangilangan
- [ ] ADR yozilgan va reja fayliga havola qilingan

## Bosqich tugaganini qanday bilamiz

- Har xulq o'zgarishi matritsada bitta qator
- Har qatorda daraja, joy, ma'lumot, oracle bor
- Gate qiymatlari loyihadan olingan, taxmin emas
- Test qiyin joylar uchun alohida qadam bor
- Pipeline ga ta'siri (vaqt, job) aytilgan
