<!-- doc: testing | chapter: 1 | part:  -->

[Java Spring loyihasida testlash](../../README.md) / [Testlash qo'llanmasi](README.md)

# 1. Sifat strategiyasi va arxitektorning roli (Quality Strategy & the Architect's Role)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [1.1 Testlash maqsadi: qaror uchun ishonch](#11-testlash-maqsadi-qaror-uchun-ishonch)
- [1.2 Shift-left va shift-right](#12-shift-left-va-shift-right)
- [1.3 Risk-ga asoslangan testlash](#13-risk-ga-asoslangan-testlash)
- [1.4 Test strategiyasi hujjati](#14-test-strategiyasi-hujjati)
- [1.5 Sifat darvozalari va Definition of Done](#15-sifat-darvozalari-va-definition-of-done)
- [1.6 Testability'ni arxitektura talabiga aylantirish](#16-testabilityni-arxitektura-talabiga-aylantirish)
- [1.7 Testlash xarajati va qiymati balansi](#17-testlash-xarajati-va-qiymati-balansi)
- [1.8 Arxitektorning aniq vazifalari](#18-arxitektorning-aniq-vazifalari)
- [1.9 Arxitektor nazorat ro'yxati](#19-arxitektor-nazorat-royxati)

</details>


Java va Spring ekotizimida testlash ko'pincha "qoplama foizini oshirish" vazifasi deb tushuniladi, lekin arxitektor uchun bu mutlaqo boshqa masala: testlar — bu tizim haqida qaror qabul qilish uchun kerak bo'ladigan ma'lumot manbai. Ushbu bobda biz sifat strategiyasini biznes riski bilan bog'lash, testability'ni arxitektura talabiga aylantirish va sifat darvozalarini o'rnatish masalalarini ko'rib chiqamiz. Maqsad — jamoaga "qancha test kerak?" degan savolga his-tuyg'u bilan emas, balki asoslangan tarzda javob berish imkonini beradigan ramka yaratish. Barcha misollar Spring Boot 3.x/4.x, Spring Framework 6.x/7.x, JUnit 5 va Java 17-25 kontekstida beriladi.

## 1.1 Testlash maqsadi: qaror uchun ishonch

Keng tarqalgan noto'g'ri tasavvur — testlash xatolarni topish uchun kerak. Haqiqatda xatoni topish bu yon mahsulot. Asosiy maqsad — **qaror qabul qilish uchun ishonch darajasini oshirish**. Har bir test aslida bitta savolga javob beradi: "Shu o'zgarishni production'ga chiqarsam bo'ladimi?"

Bu farq amaliy natijalarga olib keladi. Agar maqsad xato topish bo'lsa, jamoa topilgan xatolar sonini o'lchaydi va test yozishdan ko'ra bug tracker'ni to'ldirishga qiziqadi. Agar maqsad ishonch bo'lsa, savol o'zgaradi: "Qaysi test release haqidagi qo'rquvimni kamaytiradi?" Natijada test to'plami release jarayonining bir qismiga aylanadi, nafaqat developer'ning shaxsiy odatiga.

Ikkinchi muhim tamoyil — sifat butun jamoaning mas'uliyati. QA mustaqil "tekshiruvchi devor" emas; u sifat bo'yicha ekspert va jarayon dizayneri. Agar developer "men kod yozaman, QA sinaydi" deb o'ylasa, siz allaqachon arxitektura muammosiga egasiz: feedback loop uzun, mas'uliyat tarqoq, sifat esa oxirgi bosqichga surilgan. Arxitektor sifatida siz bu modelni buzishingiz kerak — kod yozgan odam o'z kodining testini ham yozadi, QA esa risk tahlili, test dizayni va avtomatlashtirish strategiyasiga javob beradi (batafsil taqsimot — [3-bobga](03-kim-nima-yozadi-rollar-va-masuliyat.md) qarang).

Shuni ham aytib o'tish kerak: testlar hech qachon xatolar yo'qligini isbotlay olmaydi. Ular faqat tekshirilgan stsenariylarda tizim kutilgandek ishlashini ko'rsatadi. Shuning uchun "100% coverage" maqsad emas — bu ko'rsatkichni maqsadga aylantirish (Goodhart qonuni) test sifatini pasaytiradi.

## 1.2 Shift-left va shift-right

**Shift-left** — sifat faoliyatini loyihaning boshlang'ich bosqichlariga surish. Bu faqat "testni erta yozish" degani emas. Bu quyidagilarni o'z ichiga oladi:

- Talablarni yozishda qabul kriteriylarini (acceptance criteria) misollar bilan aniqlash — "Given/When/Then" ko'rinishida.
- Arxitektura qarorini qabul qilayotganda "buni qanday sinaymiz?" savolini ADR (Architecture Decision Record) ning majburiy bo'limiga aylantirish.
- Design review'da testability'ni alohida kriteriya qilish: yangi komponent static bog'liqliklarga ega bo'lsa, review'dan o'tmaydi.
- Statik tahlil va kompilyatsiya vaqtidagi tekshiruvlarni (null-safety annotatsiyalari, Error Prone, SpotBugs) IDE darajasiga olib tushirish.

Xatoni dizayn bosqichida tuzatish arzon, production'da esa qimmat — bu eski, lekin hali ham amal qiladigan qoida. Muhimi, "arzon/qimmat" nisbatini o'z loyihangizda o'lchab ko'rish: production incident'ning o'rtacha narxi (MTTR x jalb qilingan odamlar soni + biznes yo'qotish) va bir test yozish narxini solishtiring.

**Shift-right** — production'da sifatni kuzatish va tekshirish. Testning barcha holatini staging'da takrorlash imkonsiz, shuning uchun:

- Health check va readiness probe'lar (`spring-boot-starter-actuator` orqali `/actuator/health`, `/actuator/metrics`).
- Micrometer orqali biznes metrikalari: muvaffaqiyatsiz to'lovlar foizi, retry soni, latency percentile'lari.
- Feature flag bilan canary release: yangi kod avval 1% trafikka ochiladi.
- Synthetic monitoring: production'da doimiy ishlab turadigan smoke stsenariylari.
- Chaos testing: tashqi servis javob bermaganida tizim qanday ishlashini real sharoitda tekshirish.

Shift-left va shift-right bir-birini almashtirmaydi, balki to'ldiradi. Shift-left xatoni oldini oladi, shift-right esa oldini olinmagan xatoni tez aniqlaydi.

## 1.3 Risk-ga asoslangan testlash

"Qaysi modulga qancha test yozamiz?" — arxitektor javob berishi kerak bo'lgan asosiy savol. Javob coverage maqsadidan kelib chiqmaydi, riskdan kelib chiqadi. Risk = ehtimollik x ta'sir.

**Ehtimollik** omillari: kodning o'zgarish tezligi (churn), siklomatik murakkablik, yangi texnologiya ishlatilishi, bog'liqliklar soni, jamoadagi tajriba.

**Ta'sir** omillari: pul yo'qotish, ma'lumot buzilishi, reglament/compliance buzilishi, foydalanuvchilar soni, tiklanish qiyinligi (reversible yoki yo'q).

| Modul | Ehtimollik | Ta'sir | Risk darajasi | Test chuqurligi |
|---|---|---|---|---|
| To'lov (payment) initsiatsiyasi | O'rta | Juda yuqori | Kritik | Unit + integration + contract + idempotency + konkurentlik + E2E smoke |
| To'lov holatini sinxronlash (webhook) | Yuqori | Juda yuqori | Kritik | Unit + Testcontainers + mutation testing + chaos (provider timeout) |
| Buyurtma narxini hisoblash | O'rta | Yuqori | Yuqori | Unit (property-based) + integration |
| Autentifikatsiya / authorization | Past | Juda yuqori | Yuqori | Unit + security slice test + arxitektura testlari |
| Hisobot eksporti (CSV) | O'rta | O'rta | O'rta | Unit + 1-2 integration |
| Admin paneli CRUD | Past | Past | Past | Slice test (`@WebMvcTest`) + happy path, E2E yo'q |
| Ichki feature flag paneli | Past | Past | Juda past | Smoke test, manual tekshiruv kifoya |

Misolni konkretlashtiramiz. **To'lov moduli** uchun: har bir summa hisoblash qoidasi unit test bilan qoplanadi, idempotency kaliti takroriy so'rovda ikki marta pul olinmasligini ta'minlaydi (test majburiy), tashqi provider bilan contract test, parallel so'rovlarda balans buzilmasligi uchun konkurentlik testi, va provider 500 qaytarganda retry/circuit breaker xatti-harakati tekshiriladi. Bu modulda line coverage 90%+ va mutation score kuzatiladi.

**Admin paneli** uchun: foydalanuvchilar — 12 ta ichki xodim, xato aniqlanishi bir necha daqiqada, tiklanish oson. Shuning uchun `@WebMvcTest` bilan controller validatsiyasi va ruxsat tekshiruvi sinaladi, E2E UI testi yozilmaydi (chunki saqlash narxi bergan ishonchdan yuqori). Coverage maqsadi 50-60%.

Qoida: **modul bo'yicha differensiallangan sifat talabi**. Bitta global coverage raqami butun loyiha uchun — bu strategiya emas, balki strategiya yo'qligining belgisi.

## 1.4 Test strategiyasi hujjati

Ko'p jamoalar "test strategiyasi" va "test rejasi" ni aralashtirib yuboradi. Farq quyidagicha:

| Mezon | Test strategiyasi | Test rejasi (test plan) |
|---|---|---|
| Qamrov | Butun mahsulot / tashkilot | Bitta release, epic yoki feature |
| Umr muddati | 6-12 oy, kamdan-kam o'zgaradi | Sprint yoki release davomida |
| Muallif | Arxitektor + QA lead | QA engineer / feature lead |
| Tasdiqlovchi | Engineering manager / CTO | Tech lead + product owner |
| Mazmuni | Tamoyillar, darajalar, vositalar, darvozalar | Konkret stsenariylar, muhitlar, jadval |

Strategiya hujjatiga kiritiladigan minimal bo'limlar:

1. Sifat maqsadlari va ularning biznes ko'rsatkichi bilan bog'lanishi (masalan: "to'lov oqimida production defect < 1 / chorak").
2. Test darajalari va har biri uchun mas'uliyat chegarasi ([2-bobga](02-test-piramidasi-va-test-turlari-xaritasi.md) qarang).
3. Risk klassifikatsiyasi va modul bo'yicha chuqurlik matritsasi (yuqoridagi jadval).
4. Vositalar to'plami: JUnit 5, AssertJ, Mockito, Testcontainers, WireMock, ArchUnit, JaCoCo — versiyalar BOM orqali boshqariladi.
5. Test muhitlari va ma'lumot strategiyasi.
6. Sifat darvozalari va Definition of Done.
7. Metrikalar va ularni kim, qanchalik tez-tez ko'rib chiqadi.
8. Istisnolar jarayoni: darvozani kim va qanday asos bilan chetlab o'tishi mumkin.

Hujjat kod repozitoriyasida (`docs/testing-strategy.md`) yashashi va PR orqali o'zgarishi kerak — shunda uning tarixi bo'ladi. Yangilanish triggerlari: yangi arxitektura uslubi joriy etilishi, jiddiy production incident, texnologiya stack'ining almashishi, yoki chorakda bir marta rejali qayta ko'rib chiqish.

## 1.5 Sifat darvozalari va Definition of Done

Darvoza — avtomatik, obyektiv va buzib o'tilishi qiyin shart. "Code review'da e'tibor bering" — bu darvoza emas, bu umid.

**PR darajasidagi darvoza** (har bir pull request uchun, 10 daqiqadan oshmasligi kerak):

| Tekshiruv | Shart | Buzilganda |
|---|---|---|
| Compile + unit testlar | 100% o'tadi | Merge bloklanadi |
| Yangi/o'zgargan kod coverage | >= 80% (JaCoCo diff coverage) | Merge bloklanadi |
| Statik tahlil (yangi issue) | Critical/Blocker = 0 | Merge bloklanadi |
| Arxitektura testlari (ArchUnit) | 100% o'tadi | Merge bloklanadi |
| Flaky test | Yangi flaky qo'shilmagan | Ogohlantirish + ticket |
| Code review | Kamida 1 approve | Merge bloklanadi |

**Release darajasidagi darvoza**:

| Tekshiruv | Shart |
|---|---|
| Integration + slice testlar | 100% o'tadi |
| Testcontainers bilan DB migratsiya testi | O'tadi (forward va rollback) |
| Contract testlar (provider + consumer) | 100% o'tadi |
| E2E smoke (kritik oqimlar) | 100% o'tadi |
| Performance baseline | p95 latency regressiya < 10% |
| Xavfsizlik skaneri (dependency CVE) | High/Critical = 0 yoki hujjatlashtirilgan istisno |
| Mutation score (kritik modullar) | >= 60% |

**Definition of Done** darvozadan kengroq — u insoniy bandlarni ham o'z ichiga oladi: qabul kriteriylari bajarilgan, log va metrika qo'shilgan, hujjat yangilangan, feature flag bilan o'raladigan joyi aniqlangan, rollback rejasi mavjud. Arxitektor DoD ni jamoa bilan birga yozadi va uni Jira/Linear shablonida ko'rinadigan qiladi — devordagi plakat emas, jarayonning qismi bo'lsin.

Maslahat: darvozani joriy qilishda avval "ogohlantirish" rejimida ishga tushirib, 2-3 sprint statistika yig'ing, keyin bloklashga o'tkazing. Birdan bloklash jamoaning qarshiligini keltiradi.

## 1.6 Testability'ni arxitektura talabiga aylantirish

Test yozish qiyinligi — bu test muammosi emas, dizayn muammosi. Agar sinovchi "buni sinash imkonsiz" desa, arxitektor javob berishi kerak bo'lgan savol: "Nega bu kod shunday qattiq bog'langan?"

**Dependency injection — construktor orqali.** Spring'da `@Autowired` field injection testda obyektni qo'lda yaratish imkonini yo'q qiladi. Constructor injection esa bean'ni Spring context'siz, oddiy `new` bilan yaratib sinash imkonini beradi. Final maydonlar bilan immutability ham bonus.

```java
@Service
public class PaymentService {
    private final PaymentGateway gateway;   // port (interfeys)
    private final Clock clock;              // vaqt tashqaridan
    private final IdGenerator idGenerator;  // tasodif tashqaridan

    public PaymentService(PaymentGateway gateway, Clock clock, IdGenerator idGenerator) {
        this.gateway = gateway;
        this.clock = clock;
        this.idGenerator = idGenerator;
    }
}
```

**Port va adapter (hexagonal).** Domain logikasi infratuzilmani bilmasligi kerak. `PaymentGateway` — port (domain paketidagi interfeys), `StripePaymentAdapter` — adapter (infrastructure paketida). Natijada domain testlari HTTP, DB yoki broker'siz, millisekundlarda ishlaydi. ArchUnit bilan bu qoidani majburlash mumkin ([14-bobga](14-arxitektura-testlari-va-kod-sifati.md) qarang).

**Vaqtni tashqaridan bering.** `LocalDateTime.now()` va `Instant.now()` to'g'ridan-to'g'ri chaqirilsa, "oyning oxirgi kuni" yoki "sertifikat muddati tugashi" stsenariysini sinash imkonsiz bo'ladi. Yechim — `java.time.Clock` bean:

```java
@Bean
public Clock clock() {
    return Clock.systemUTC();
}
// Testda: Clock.fixed(Instant.parse("2026-01-31T23:59:00Z"), ZoneOffset.UTC)
```

**Tasodifni tashqaridan bering.** UUID, random token, shuffle — barchasi interfeys ortida. Aks holda test natijasi takrorlanmaydi.

**Tashqi chaqiruvlarni interfeys ortiga yashiring.** `RestClient`, `WebClient`, Kafka producer, S3 client — hech qachon domain servisida to'g'ridan-to'g'ri ishlatilmasin. Bu nafaqat testability, balki retry, timeout va circuit breaker siyosatini bir joyda boshqarish imkonini beradi.

**Static va singleton'dan voz kechish.** Static metodlar, `new Date()`, global holat — bularning hammasi testda almashtirilmaydi. Agar legacy kodda bo'lsa, uni yupqa interfeys bilan o'rab chiqing.

**Kuzatiladigan (observable) qiling.** Test faqat qaytarilgan qiymatni tekshirmaydi — ba'zan "nima sodir bo'lganini" tekshirish kerak. Shuning uchun: muhim biznes hodisalar uchun Micrometer counter/timer, strukturalangan log (MDC bilan correlation ID), va domain event'lar. Spring'da `ApplicationEventPublisher` orqali chiqarilgan event testda osongina ushlanadi. Qoida: agar siz bir holatni log yoki metrika orqali tashqaridan ko'ra olmasangiz, uni production'da ham diagnostika qilolmaysiz.

Bu talablar ADR va design review checklist'ga kirishi kerak. "Testability — non-functional requirement" degan gapni hujjatda yozib qo'yish kifoya emas; uni review'da savol ko'rinishida so'rash kerak.

## 1.7 Testlash xarajati va qiymati balansi

Har bir test uch xil narxga ega: **yozish** (bir martalik), **ishga tushirish** (har CI run'da) va **saqlash** (kod o'zgarganda tuzatish). Uchinchisi eng ko'p e'tibordan chetda qoladi va aynan u eng qimmat.

| Daraja | Yozish narxi | Ishga tushish vaqti | Saqlash narxi | Bergan ishonch | Diagnostika aniqligi |
|---|---|---|---|---|---|
| Unit (Spring'siz) | Past | ms | Past | Logika to'g'riligi | Juda yuqori |
| Slice (`@WebMvcTest`, `@DataJpaTest`) | O'rta | 1-3 s | O'rta | Qatlam integratsiyasi | Yuqori |
| Integration (Testcontainers) | Yuqori | 5-30 s | O'rta-yuqori | Real DB/broker bilan ishlash | O'rta |
| Contract | O'rta | 1-5 s | O'rta | Servislar o'rtasidagi muvofiqlik | Yuqori |
| E2E / UI | Juda yuqori | daqiqalar | Juda yuqori | Foydalanuvchi oqimi | Past |

Amaliy qoidalar:

- Bir xil ishonchni arzonroq darajada olish mumkin bo'lsa, arzonroqni tanlang. Validatsiya qoidasini E2E testda sinash — resurs isrofi.
- Qiymat bermaydigan testni o'chirish — bu yo'qotish emas, tejamkorlik. Hech qachon buzilmagan va hech narsani ushlamagan test faqat saqlash narxini keltiradi.
- Ishga tushish vaqtini kuzatib boring. PR pipeline 10 daqiqadan oshsa, developer kutmay boshqa ishga o'tadi — feedback loop buziladi va testning qiymati tushadi.
- Spring context'ni qayta ishlatish (context caching) — eng arzon tezlashtirish usuli. Har bir test klassida har xil `@MockBean`/`@TestConfiguration` kombinatsiyasi yangi context yaratadi; bu sekinlikning asosiy manbai.
- Flaky test qiymati manfiy: u ishonchni yo'qotadi va jamoani "qayta ishga tushirish" odatiga o'rgatadi ([16-bobga](16-flaky-testlar-test-qarzi-va-test-kodini.md) qarang).

## 1.8 Arxitektorning aniq vazifalari

Sifat strategiyasida arxitektorning roli "maslahat berish" emas, balki konkret, tekshiriladigan ishlardan iborat:

1. **Strategiyani belgilash va hujjatlashtirish.** Risk matritsasini modul egalari bilan birga to'ldirish, modul bo'yicha chuqurlik talabini kelishish.
2. **Test infratuzilmasini tanlash.** JUnit 5 platformasi, mocking kutubxonasi, Testcontainers moduli, contract testing yondashuvi, coverage va mutation vositalari. Tanlov ADR bilan asoslanadi, versiyalar Spring Boot BOM va `dependencyManagement` orqali markazlashtiriladi.
3. **Standartlarni yozish.** Test nomlash konvensiyasi, test ma'lumotlari uchun builder/fixture uslubi, qaysi holatda mock va qaysi holatda real obyekt ishlatiladi, test paketlari tuzilishi. Shablonlar [18-bobda](18-shablonlar-checklistlar-va-malumotnoma.md).
4. **Test kodini review qilish.** Test kodi production kodi bilan bir xil standartga javob berishi kerak. Review'da e'tibor: assertion aniqligimi yoki `assertNotNull` bilan cheklanganmi, test nomi niyatni ifodalaydimi, mock haddan ortiq ishlatilmaganmi.
5. **Metrikalarni kuzatish.** Diff coverage, mutation score (kritik modullarda), pipeline davomiyligi, flaky test ro'yxati, production defect escape rate, MTTR. Chorakda bir marta trend tahlili ([17-bobga](17-metrikalar-va-test-yetukligi-modeli.md) qarang).
6. **Darvozalarni o'rnatish va himoya qilish.** Eng qiyin qismi — bosim ostida darvozani ochmaslik. Istisno jarayoni yozilgan va kim ruxsat berishi aniq bo'lishi kerak.
7. **Jamoani o'rgatish.** Pair testing sessiyalari, ichki workshop, misol bo'ladigan reference modul ("shunday yozamiz" namunasi). Yangi odamga onboarding'da test standartini ko'rsatish.
8. **Testability'ni dizayn review'ning majburiy kriteriyasiga aylantirish.** Har bir yangi komponent uchun: "bu qanday sinaladi?" savolini so'rash.

## 1.9 Arxitektor nazorat ro'yxati

- [ ] Loyihada `docs/testing-strategy.md` mavjud, oxirgi 6 oyda yangilangan va PR orqali boshqariladi.
- [ ] Modul bo'yicha risk matritsasi (ehtimollik x ta'sir) to'ldirilgan va har bir modul uchun test chuqurligi hamda coverage maqsadi alohida belgilangan.
- [ ] PR darajasidagi darvozalar CI'da avtomatik ishlaydi: unit testlar, diff coverage, statik tahlil, ArchUnit — qo'lda tekshiruvga tayanmaydi.
- [ ] Release darvozasi aniqlangan (integration, contract, migratsiya, smoke, CVE skaneri) va istisno berish jarayoni hujjatlashtirilgan.
- [ ] Definition of Done jamoa tomonidan tasdiqlangan va issue tracker shablonida ko'rinadi.
- [ ] Barcha yangi bean'lar constructor injection ishlatadi; `Clock`, ID/tasodif generatori va tashqi client'lar interfeys ortida va bean sifatida inject qilinadi.
- [ ] Domain qatlami infratuzilma paketlariga bog'liq emasligi arxitektura testi bilan majburlangan.
- [ ] PR pipeline davomiyligi 10 daqiqadan oshmaydi va u haftalik kuzatiladigan metrika.
- [ ] Flaky testlar ro'yxati mavjud, har biri uchun egasi va muddati belgilangan.

---

[Mundarija](README.md) · [2. Test piramidasi va test turlari xaritasi &rarr;](02-test-piramidasi-va-test-turlari-xaritasi.md)
