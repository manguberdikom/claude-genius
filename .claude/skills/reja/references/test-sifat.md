# 5-bosqich: test strategiyasi va sifat darvozasi

Bu bosqichda reja test injener ko'zi bilan o'qiladi. Natija ikki artefakt:
**test matritsasi** (nima o'zgaradi -> qanday tekshiriladi) va **quality gate
talablari** (o'zgarish Sonar/CI dan o'tishi uchun nima kerak).

Qoida: **"test yozish" degan qadam yo'q.** Har test uchun to'rt narsa aytiladi:
daraja, joy, ma'lumot, oracle (kutilgan natija). Oracle yo'q test — yolg'on
xotirjamlik.

## 5.1 Test matritsasi formati

| O'zgarish | Daraja | Joy | Ma'lumot | Oracle |
|---|---|---|---|---|
| `PaymentHandler` strategiya registri | unit | `PaymentHandlerRegistryTest` | har turga bitta stub handler | noma'lum tur -> `IllegalArgumentException`; `CARD` -> `CardHandler` |
| Outbox yozuvi tranzaksiyada | integratsion (`@DataJpaTest`) | `OutboxRepositoryIT` | buyruq + rollback holati | commit -> 1 qator; rollback -> 0 qator |
| Publisher Kafka ga jo'natadi | integratsion (Testcontainers) | `OutboxPublisherIT` | 2 jo'natilmagan qator | ikkisi ham topic'da; `sent_at` to'ldirilgan |
| Takroriy xabar | integratsion | `OrderConsumerIT` | bir xil `request_id` bilan 2 xabar | DB da 1 buyruq; ikkinchisi e'tiborsiz |
| Tashqi servis timeout | unit + WireMock | `PaymentClientTest` | 5 s kechikadigan stub | 3 s da `TimeoutException`, retry 2 marta |
| Yangi endpoint kontrakti | slice (`@WebMvcTest`) | `OrderControllerTest` | noto'g'ri body | 400 + xato formati o'zgarmagan |
| Migratsiya | migratsiya testi | `MigrationIT` | bo'sh va to'liq baza | yuqoriga va orqaga qaytish ishlaydi |

## 5.2 Daraja tanlash

Piramida qoidasi (testlash 2-bob): past darajada mumkin bo'lsa, yuqorida
yozilmaydi. Spring kontekstini ko'tarish — test sekinligining asosiy manbasi
(patternlar 25.40).

| Nimani tekshiramiz | Daraja | Vosita | Qarash |
|---|---|---|---|
| Sof logika, shart, hisob, validatsiya qoidasi | unit, kontekstsiz | JUnit 5 + Mockito | testlash 5, 6-bob |
| Controller: marshrutlash, serializatsiya, status, validatsiya | slice | `@WebMvcTest` | testlash 7-bob |
| Repository: so'rov, mapping, indeks ishlashi | slice + real DB | `@DataJpaTest` + Testcontainers | testlash 7, 8-bob |
| Tranzaksiya chegarasi, rollback, lock | integratsion | `@SpringBootTest` + Testcontainers | testlash 11-bob |
| Broker bilan oqim (producer/consumer) | integratsion | Testcontainers Kafka | testlash 8-bob |
| Tashqi HTTP servis xulqi (timeout, 500, sekinlik) | unit/integratsion | WireMock | testlash 9-bob |
| Tashqi kontrakt buzilmasligi | contract test | Spring Cloud Contract / Pact | testlash 9-bob; patternlar 23.17 |
| Foydalanuvchi oqimi | E2E (kam sonda) | REST-assured / Playwright | testlash 12-bob |
| Yuklama, chidamlilik | nofunksional | k6/Gatling, chaos | testlash 13-bob |
| Arxitektura qoidasi (qatlam, tsikl, nomlash) | arxitektura testi | ArchUnit | testlash 14-bob |
| Coverage yolg'on emasligi | mutation | PIT | sonarqube 20-bob; patternlar 23.10 |

Qoida: **bitta xulq bitta darajada tekshiriladi.** Bir xil shartni unit va E2E da
ikki marta tekshirish — ikki marta saqlash xarajati.

## 5.3 Test ma'lumoti

- Qurilish takrorlanadigan bo'lsa — Test Data Builder (patternlar 23.5) yoki
  Object Mother (23.6). Rejada builder qayerda turishi aytiladi.
- Umumiy mutable fixture ishlatilmaydi: test tartibiga bog'liqlik paydo bo'ladi
  (testlash 16-bob).
- Real ma'lumot nusxasi ishlatilsa, shaxsiy ma'lumot maskalanadi (testlash 10-bob).
- Har test o'z ma'lumotini yaratadi va tozalaydi; `@Sql` yoki builder — tanlov
  rejada aytiladi.

## 5.4 Test qiyin joylar uchun reja

Kod o'zgarmasdan test yozilmaydigan holatlar (arxitektor 34-bob, sonarqube
11-bob) rejada **alohida qadam** bo'ladi:

| To'siq | Reja qadami |
|---|---|
| `static` chaqiruv (`LocalDate.now()`, util sinflar) | `Clock` bean inject qilinadi; test `Clock.fixed` beradi |
| `new` konstruktor ichida | fabrika yoki konstruktor injection |
| `private` metod murakkab | xulq public API orqali tekshiriladi yoki metod alohida sinfga chiqariladi |
| Tashqi tizim qattiq bog'langan | port interfeysi + adapter (patternlar 12.2) |
| Random / UUID | generator interfeysi yoki seed |
| Thread va vaqt | `Awaitility`, deterministik executor (testlash 11-bob) |

## 5.5 Quality gate talablari

Chegaralar **taxmin qilinmaydi** — loyihadan o'qiladi (1-bosqich jadvalidan).
Rejaga aynan shu qiymatlar yoziladi:

| Shart | Loyihadagi qiymat | Manba | Reja uchun ma'nosi |
|---|---|---|---|
| New code coverage | 100% | `sonar-project.properties:12` | yangi/o'zgargan har qator qamralishi kerak |
| Duplication (new code) | 3% | quality gate | ko'chirib-qo'yish o'rniga umumiy metod |
| Cognitive complexity | metodga 15 | quality profile | yangi `switch` ni handler'larga bo'lish |
| Blocker/Critical issue | 0 | gate | yangi `catch(Exception)` yo'q |
| Security hotspot | hammasi ko'rib chiqilgan | gate | yangi tashqi kiritish uchun validatsiya |
| Test muvaffaqiyati | 100% | CI | `@Disabled` qo'shilmaydi |

Agar gate topilmasa: rejada `TAXMIN:` deb yoziladi va birinchi qadamlardan biri —
gate shartlarini aniqlash.

### Exclusion halolligi

Coverage ni `sonar.coverage.exclusions` bilan "yopish" — faqat haqiqatan
mantiqsiz kod uchun (generatsiya qilingan, DTO/record, konfiguratsiya sinflari);
mantiq bor kodni chiqarish aldov (sonarqube 12-bob). Reja exclusion qo'shsa,
sababi va qaysi fayl ekani aniq yoziladi.

## 5.6 O'zgarish turi -> ehtimoliy Sonar qoidalari

Reja qanday kod yozishni aytadi, demak qaysi qoidani buzish xavfi borligini ham
aytadi (sonarqube 14, 25–30-boblar):

| Reja nima qo'shadi | Xavfdagi qoidalar |
|---|---|
| Yangi `switch` / shartlar | cognitive complexity, takrorlanish (15-bob) |
| Yangi tashqi chaqiruv | resurs yopilmasligi, timeout yo'qligi, `InterruptedException` yutilishi (25-bob) |
| SQL yoki filtr | SQL injection, taint oqimi (26, 37-bob) |
| Yangi DTO/record | Lombok/record va coverage (41-bob) |
| Yangi `@Transactional` | `private`/`self-invocation` xatolari (29-bob) |
| Yangi test | assertion yo'qligi, `@Disabled`, test ichida mantiq (19, 30-bob) |
| Yangi log | foydalanuvchi ma'lumotini log qilish, formatlash (26, 28-bob) |

## 5.7 CI dagi o'rni

Rejada yangi test turi paydo bo'lsa, u pipeline ga qanday tushishi aytiladi
(testlash 15-bob):

- unit testlar — har push da, PR ni blokirovka qiladi
- integratsion/Testcontainers — PR da, alohida job, timeout bilan
- contract test — provider va consumer tomonida
- E2E / yuklama — kechasi yoki reliz oldidan, PR ni blokirovka qilmaydi
- mutation testing — nightly, o'zgargan modulga

Vaqt budjeti yoziladi: "integratsion job ~4 daqiqa qo'shadi" — pipeline sekinligi
ham narx.

## 5.8 Definition of Done qatorlar

Reja oxiridagi DoD ga shular kiradi (testlash 18-bob shabloni bilan mos):

- [ ] Kod o'zgarishlari rejadagi qadamlarga mos, qo'shimchasiz
- [ ] Har yangi xulq uchun test bor va u o'zgarishsiz kodda qulaydi (test avval
      qizil bo'lganini ko'rsatish)
- [ ] `mvn verify` (yoki loyiha buyrug'i) lokalda yashil
- [ ] Quality gate o'tdi (new code coverage, duplication, complexity)
- [ ] Migratsiya yuqoriga va orqaga sinab ko'rilgan
- [ ] Yangi konfiguratsiya kalitlari hamma muhitga qo'shilgan
- [ ] Log/metrika qo'shilgan va dashboard/alert yangilangan
- [ ] ADR yozilgan va reja fayliga havola qilingan

## Bosqich tugaganini qanday bilamiz

- Har xulq o'zgarishi matritsada bitta qator
- Har qatorda daraja, joy, ma'lumot, oracle bor
- Gate qiymatlari loyihadan olingan, taxmin emas
- Test qiyin joylar uchun alohida qadam bor
- Pipeline ga ta'siri (vaqt, job) aytilgan
