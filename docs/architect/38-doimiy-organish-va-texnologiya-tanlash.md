<!-- doc: architect | chapter: 38 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 38. Doimiy o'rganish va texnologiya tanlash (Continuous Learning and Technology Choice)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [38.1 Nimani chuqur o'rganish kerak va nimani yuzaki bilish yetarli](#381-nimani-chuqur-organish-kerak-va-nimani-yuzaki-bilish-yetarli)
- [38.2 Uzoq yashaydigan bilim va tez eskiradigan bilim farqi](#382-uzoq-yashaydigan-bilim-va-tez-eskiradigan-bilim-farqi)
- [38.3 Birlamchi manbalar: spetsifikatsiya, hujjat, manba kod, reliz eslatmasi](#383-birlamchi-manbalar-spetsifikatsiya-hujjat-manba-kod-reliz-eslatmasi)
- [38.4 Yangi kutubxonani baholash mezonlari: qo'llab-quvvatlash, bog'liqlik, chiqish yo'li](#384-yangi-kutubxonani-baholash-mezonlari-qollab-quvvatlash-bogliqlik-chiqish-yoli)
- [38.5 Bog'liqlik qo'shishning yashirin narxi va uni yangilash majburiyati](#385-bogliqlik-qoshishning-yashirin-narxi-va-uni-yangilash-majburiyati)
- [38.6 Moda texnologiyani baholash: qaysi muammoni hal qiladi, sizda u bormi](#386-moda-texnologiyani-baholash-qaysi-muammoni-hal-qiladi-sizda-u-bormi)
- [38.7 Qurish yoki sotib olish qarori va mezonlari](#387-qurish-yoki-sotib-olish-qarori-va-mezonlari)
- [38.8 Tajriba uchun vaqt ajratish: spike, ichki loyiha, o'lchovli tajriba](#388-tajriba-uchun-vaqt-ajratish-spike-ichki-loyiha-olchovli-tajriba)
- [38.9 Bilimni jamoaga tarqatish: hujjat, suhbat, namuna kod](#389-bilimni-jamoaga-tarqatish-hujjat-suhbat-namuna-kod)
- [38.10 Xatolardan o'rganishni odat qilish va o'z qarorlarini qayta ko'rish](#3810-xatolardan-organishni-odat-qilish-va-oz-qarorlarini-qayta-korish)
- [38.11 Java va Spring ekotizimini kuzatib borish usullari](#3811-java-va-spring-ekotizimini-kuzatib-borish-usullari)
- [38.12 O'z o'rganish rejangizni tuzish: chorak uchun aniq maqsadlar](#3812-oz-organish-rejangizni-tuzish-chorak-uchun-aniq-maqsadlar)
- [38.13 Baza turini tanlash: yettita mezon va nega ular birga ishlaydi](#3813-baza-turini-tanlash-yettita-mezon-va-nega-ular-birga-ishlaydi)
- [38.14 Bog'liqlikni boshqarish: fork, ega va tashqariga chiqarish](#3814-bogliqlikni-boshqarish-fork-ega-va-tashqariga-chiqarish)
- [38.15 Amalda qo'llash](#3815-amalda-qollash)

</details>



Arxitektorning bilimi ikki xil eskiradi. Birinchisi tezda chiriydi: kutubxona versiyasi, konfiguratsiya kaliti, bulut panelining joylashuvi. Ikkinchisi o'n yil yashaydi: tranzaksiya izolyatsiyasi, xotira modeli, indeks tanlash mexanikasi. Bu bob shu ikki qatlamni ajratish, yangi texnologiyani sovuq boshda baholash va o'rganishni chorakka bo'lingan o'lchovli rejaga aylantirish haqida.

## 38.1 Nimani chuqur o'rganish kerak va nimani yuzaki bilish yetarli

Richards va Ford bilimni uch qatlamli piramida sifatida ko'rsatadi: bilganingiz, bilmasligingizni bilganingiz, va bilmasligingizni ham bilmaganingiz. Piramidaning yuqori qismi texnik chuqurlik (technical depth), o'rta qatlamning pastga qancha kirib borishi esa texnik kenglik (technical breadth). Ularning xulosasi aniq: developer uchun chuqurlik, arxitektor uchun kenglik muhimroq, chunki arxitektor imkoniyatni cheklovga moslashtirar ekan, bitta yechimni chuqur bilgandan ko'ra beshta yechim borligini bilishi foydaliroq. Shu almashuv ongli bo'lishi kerak, aks holda ikki disfunksiyadan biri chiqadi: hamma sohada ekspertlikni saqlashga urinib hech qayerda ulgurmaslik, yoki eskirgan bilimni hamon zamonaviy deb hisoblash (Fundamentals of Software Architecture, 2-bob).

Chuqurlik darajasini ehtimollik bilan tanlang. Agar mexanika buzilganda production incident bo'lsa va uni siz tuzatishingiz kerak bo'lsa, u chuqur bilim. Agar hujjatni ochib 20 daqiqada javob topsa bo'lsa, u yuzaki bilim.

To'lov servisi uchun ro'yxat shunday. Chuqur: JDBC tranzaksiya chegarasi, Hibernate flush tartibi, PostgreSQL row lock va deadlock, HikariCP pool o'lchami, JVM GC pauzalari, `ExecutorService` va virtual thread semantikasi. Yuzaki: Flyway migratsiya sintaksisi, Jackson annotatsiyalari, Testcontainers moduli nomi, OpenAPI generator sozlamasi.

Java tomonida ro'yxatning poydevori esa tanlovga qoldirilmaydi. Bloch minimal talabni aniq qo'yadi: har bir programmist `java.lang`, `java.util` va `java.io` ning asoslarini bilishi kerak, va asosiy asboblar to'plamiga to'plamlar frameworki, oqimlar kutubxonasi hamda `java.util.concurrent` ning yuqori darajali qismlari kiradi (Joshua Bloch, *Effective Java*, 3-nashr, Addison-Wesley, 2018, Item 59, 269-bet). Bu ro'yxat yuqoridagi "ehtimollik bilan tanlang" qoidasidan ustun turadi, chunki shu paketlar har kod yo'lida uchraydi: ularni bilmaslik narxi bitta incident emas, har kundalik qarorda bir oz noto'g'ri tanlov. Shu sababli piramidaning tanlanadigan qismi `java.lang`, `java.util` va `java.io` dan YUQORIDA boshlanadi.

Chuqur bilimning o'lchovi bitta: siz shu mexanikani kod bilan isbotlab bera olasizmi.

```java
// Chuqur bilimni tekshirish usuli: taxminni kod bilan isbotlash.
@Test
void flushTartibiInsertniUpdatedanOldinYuboradi() {
    var statistika = entityManagerFactory.unwrap(SessionFactory.class).getStatistics();
    statistika.setStatisticsEnabled(true);

    transactionTemplate.executeWithoutResult(status -> {
        var qoldiq = em.find(OmborQoldigi.class, 42L);
        qoldiq.kamaytir(5); // mavjud qoldiqni o'zgartiramiz
        em.persist(new OmborHarakati(42L, -5)); // yangi harakat yozuvi
        // Bu yerda hali hech qanday SQL ketmagan.
        assertThat(statistika.getPrepareStatementCount()).isZero();
    });

    // Flush insert'ni update'dan oldin yuboradi: unique constraint
    // kutilmagan tartibda ishga tushishi mumkin.
    assertThat(statistika.getEntityInsertCount()).isEqualTo(1);
    assertThat(statistika.getEntityUpdateCount()).isEqualTo(1);
}
```

Yuzaki bilim uchun boshqa strategiya: tafsilot o'rniga "qaerga qarash kerak" ni eslab qoling.

Oxirgi va eng ko'p e'tibordan qoladigan yo'l chuqurlikni individual masala deb qaramaslik. Brown arxitektordan har texnologiyada ekspert bo'lishni talab qilmaydi: bilmagan narsangizni tushunadigan odamni topib u bilan birga ishlash to'g'ri yo'l, ya'ni rolni bo'lishish mumkin, va o'z bilimidagi bo'shliqni tan olish birinchi qadam; uning formulasi esa qisqa, ya'ni pair programming foyda bersa, pair architecting ham beradi (Simon Brown, *Software Architecture for Developers*, Leanpub, 12-bob, 35-bet). Amaliy shakl ikkita. Birinchisi: chuqur bilim ro'yxatini jamoa bo'yicha to'ldirasiz, bitta odam bo'yicha emas, va natija [bilim xaritasi](36-code-review-va-jamoada-texnik-yetakchilik.md#3610-jamoaning-bilim-xaritasi-va-bitta-odamga-bogliqlikni-kamaytirish) ga tushadi. Ikkinchisi: sizda bo'shliq bo'lgan sohadagi qaror yolg'iz chiqarilmaydi, ya'ni ADR ni shu sohani biladigan odam bilan birga yozasiz. Bu qarorni sekinlashtirmaydi, aksincha, keyingi tuzatish ishini kamaytiradi.

## 38.2 Uzoq yashaydigan bilim va tez eskiradigan bilim farqi

Standart va protokol darajasidagi bilim eng uzoq yashaydi: SQL izolyatsiya darajalarining semantikasi, HTTP keshlash sarlavhalarining ma'nosi, Jakarta Persistence spetsifikatsiyasidagi `flush` qoidasi.

Keyingi qatlam: implementatsiya mexanikasi. PostgreSQL MVCC va vacuum, Hibernate dirty checking, JVM escape analysis. McConnell texnik muhitning aniq xususiyatlari besh yildan o'n yilgacha oraliqda o'zgarib turishini aytadi (Code Complete, 2-nashr, 33.3, 822-bet), ya'ni bu qatlam ham abadiy emas, faqat yuqorisidan sekin eskiradi.

Eng tez eskiradigani: API sirti va konfiguratsiya nomi. `WebSecurityConfigurerAdapter` Spring Security 5.7 da deprecated bo'ldi va 6.0 da olib tashlandi. Konfiguratsiya nomini yodlash eng past daromadli investitsiya.

Taqsimot uchun tasdiqlangan foiz yo'q, lekin ustuvorlik aniq. McConnell raqamni shunday qo'yadi: raqobatli bozorda bugun ishingiz uchun bilishingiz kerak bo'lgan narsaning yarmi uch yildan keyin eskiradi, va o'rganmay qolgan odam dinozavrga aylanadi (Code Complete, 2-nashr, 33.3, 822-bet). Ford va sheriklari esa ekotizim o'zini bo'lak-bo'lak almashtirib turishini ko'rsatib, shu sababli kitobni implementatsiya tafsilotiga emas, qaror qabul qilish va trade-off tahliliga qaratadi (The Hard Parts, 1-bob, 2-3-bet). Ikki manbadan chiqadigan xulosa: o'qish vaqtining kattasi mexanikaga va qaror usuliga ketadi, kichik qismi joriy stack relizlariga va kuzatuvga.

## 38.3 Birlamchi manbalar: spetsifikatsiya, hujjat, manba kod, reliz eslatmasi

Blog postidan javob izlash odati arxitektorni sekin zaharlaydi. Blog ikkinchi qo'l, bitta versiyaga bog'langan va ko'pincha noto'g'ri. Birlamchi manbalar ketma-ketligini odat qiling.

Ikki kitob bu nuqtada bir xil gapni aytadi, hatto bir xil jumla bilan: arxitektura - Google'dan javob topib bo'lmaydigan narsa, shuning uchun javob birlamchi manbadan va o'z o'lchovingizdan chiqadi (Fundamentals of Software Architecture, 2-bob; The Hard Parts, 2-bob, 26-bet).

Birinchi: rasmiy reference hujjat. Spring hujjatlari versiya bo'yicha ajratilgan, URL ichida versiya raqami bor. Har doim o'zingiz ishlatadigan versiyaning hujjatini oching, `current` ni emas.

Ikkinchi: reliz eslatmasi va migration guide. Spring Boot har bir minor reliz uchun migration guide chiqaradi, PostgreSQL har bir major reliz uchun "Migration to Version X" bo'limini beradi, OpenJDK esa JEP ro'yxatini beradi.

Uchinchi: spetsifikatsiya. Jakarta Persistence spetsifikatsiyasi `flush` semantikasini aytadi, Hibernate hujjati esa faqat o'z xulqini aytadi.

To'rtinchi: manba kod. Bu eng ishonchli manba va u bir buyruq bilan qo'lingizda bo'ladi.

```bash
# Barcha bog'liqliklarning manba kodini lokal repozitoriyga tushirish.
mvn dependency:sources dependency:resolve -Dclassifier=javadoc

# Spring Boot qaysi avtokonfiguratsiyani yoqdi va nega yoqmadi.
java -jar target/app.jar --debug 2>&1 | sed -n '/CONDITIONS EVALUATION/,/^$/p'

# BOM import qilingandan keyin aslida qaysi versiya tanlandi.
mvn help:effective-pom -Doutput=/tmp/effective-pom.xml

# Konkret kutubxonaning versiya konflikti qayerdan kelgan.
mvn dependency:tree -Dincludes=com.fasterxml.jackson.core:jackson-databind
```

Manba kodni o'qishni odat qiling. Spring'da annotatsiya ortidagi `BeanPostProcessor` ni topib o'qish 30 daqiqa oladi, va bu bilim 5 yil yashaydi.

## 38.4 Yangi kutubxonani baholash mezonlari: qo'llab-quvvatlash, bog'liqlik, chiqish yo'li

Birinchi savol kutubxona tanlashdan oldin keladi: bu ish platformaning o'zida bormi. JDK va Spring da bor narsani qayta yozish eng qimmat yo'l, chunki yozilgan kod sizning qarzingiz bo'ladi, platformadagisi esa mutaxassislar tomonidan ushlab turiladi va har relizda tezlashadi. Shu sababli standart kutubxonaning yangi qo'shilgan API larini kuzatib borish texnologiya tanlashning bir qismi: `Files`, `HttpClient`, `Random.ints`, `Objects`, `Collectors` va `java.time` da ko'p ehtiyoj allaqachon qoplangan (Joshua Bloch, Effective Java, 3-nashr, Item 59, 267-bet).

Bloch shu joyda kutubxonadan foydalanishning qolgan to'rt afzalligini ham sanaydi, va ular [bog'liqlik qo'shishning narxi](#385-bogliqlik-qoshishning-yashirin-narxi-va-uni-yangilash-majburiyati) bo'limini muvozanatlaydi: ad-hoc yechim yozishga vaqt ketmaydi; kutubxonaning ishlashi vaqt o'tishi bilan sizning ishtirokingizsiz yaxshilanadi; funksionalligi o'sadi; va kodingiz asosiy oqimda qoladi, ya'ni keyin kelgan odam uni tanish shaklda ko'radi (Item 59, 268-bet). Oxirgi afzallik eng kam gapiriladi va amalda eng ko'p vaqt tejaydi: o'z `RetryHelper` ingizni yangi odam o'qib chiqishi kerak, `@Retryable` ni esa hujjatdan tanib oladi. Shuning uchun qaror bir tomonlama emas: 38.5 narxni hisoblaydi, bu yerdagi to'rt band esa foydani, va tanlov ikkisining yig'indisidan chiqadi.

Kutubxona tanlashni yozma mezon bilan qiling. Quyidagi yetti mezon shu korpusning amaliy ro'yxati, kitobdagi taksonomiya emas; har biriga raqam yoki aniq javob talab qilinadi.

Birinchi: tiriklik. Oxirgi bir yilda relizlar muntazam chiqdimi, loyihani bitta odam ushlab turadimi.

Ikkinchi: bog'liqlik og'irligi. Bitta kichik JSON yordamchisi o'zi bilan uzun tranzitiv jar ro'yxatini olib kelsa, bu yomon signal.

Uchinchi: stack bilan to'qnashuv. Kutubxona Jackson yoki Netty ning boshqa major versiyasini talab qilsa, siz versiya urushiga kirasiz.

To'rtinchi: chiqish yo'li. Bir yildan keyin voz kechsangiz, qancha fayl o'zgaradi. Javob kichik son bo'lishi uchun kutubxonani interface ortiga yashiring.

```java
// Chiqish yo'li: tashqi kutubxona faqat bitta adapter ichida ko'rinadi.
// Domen kodi hech qachon vendor sinfini import qilmaydi.
public interface ToLovShlyuzi {
    ToLovNatijasi toLa(ToLovBuyrugi buyruq);
}

@Component
class StripeToLovShlyuzi implements ToLovShlyuzi {

    private final com.stripe.StripeClient mijoz; // vendor faqat shu yerda

    @Override
    public ToLovNatijasi toLa(ToLovBuyrugi buyruq) {
        try {
            var javob = mijoz.paymentIntents().create(mapQil(buyruq));
            return ToLovNatijasi.muvaffaqiyat(javob.getId());
        } catch (com.stripe.exception.StripeException e) {
            // Vendor exception'i domen xatosiga aylanadi, tashqariga chiqmaydi.
            throw new ToLovXatosi(buyruq.id(), e.getCode(), e);
        }
    }
}
```

Beshinchi: litsenziya, chunki AGPL kutubxonasi yopiq mahsulotga kirmaydi. Oltinchi: xavfsizlik tarixi, ya'ni CVE bo'lganda jamoa qancha kunda patch chiqargan. Yettinchi: kuzatuvchanlik, chunki Micrometer metrikasi bermaydigan kutubxona qora qutiga aylanadi.

Ro'yxatda yo'q, lekin tanlovni o'zgartiradigan sakkizinchi savol versiya yetukligi haqida: "oldinda buzuvchi o'zgarish bormi". Intuitiv javob "barqaror versiyani ol" bo'ladi, lekin Orosz teskari tanlovni ham oqlaydi: beqaror (hali barqaror deb belgilanmagan) framework yoki API versiyasini tanlash ba'zan to'g'ri bo'ladi, chunki eng yangi va yetarlicha barqaror versiyani olish keyinchalik migratsiya qilish majburiyatini yo'q qiladi; tez o'zgaradigan narsa uchun esa muqobil ham ko'rib chiqiladi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 16-bob, 235-bet). Ajratuvchi shart ikki narxni taqqoslashda: beqaror versiyaning xavfi (API o'zgarishi, hujjat yetishmasligi, kam ishlatilgani uchun kam topilgan xato) va keyingi migratsiyaning narxi (qancha fayl, qancha jamoa, qancha reliz oynasi).

| Holat | To'g'ri tanlov | Nega |
|---|---|---|
| Yangi loyiha, major versiya bir-ikki oyda chiqadi | yangi (hali beqaror) versiya | migratsiya ishi boshlanmasdan oldin yopiladi |
| Mavjud tizim, migratsiya bir necha jamoaga tegadi | hozirgi barqaror versiya | beqaror API o'zgarsa narx bir necha jamoaga ko'payadi |
| Kutubxona interfeys ortiga yashirilgan | yangi versiya xavfsizroq | chiqish yo'li qisqa, to'rtinchi mezon bajarilgan |
| Kutubxona domen kodi bo'ylab tarqalgan | barqaror versiya | API o'zgarishi hamma joyga tegadi |

## 38.5 Bog'liqlik qo'shishning yashirin narxi va uni yangilash majburiyati

Bog'liqlik qo'shganda siz kod emas, majburiyat olasiz. Har bir jar CVE yuzangizni, build vaqtini, startup vaqtini va yangilash ishini oshiradi.

Raqamni taxmin qilmang, o'zingizning build'ingizdan oling. `mvn dependency:list` jar sonini beradi, `mvn dependency:tree` qaysi starter qancha tranzitiv bog'liqlik keltirganini ko'rsatadi, startup ta'sirini esa bog'liqlik qo'shilishidan oldin va keyin bir xil mashinada o'lchab solishtirasiz. Shu uch o'lchov sizning kontekstingizda haqiqiy; boshqa loyihaning o'rtacha raqami emas.

Yangilashni avtomatlashtiring, aks holda u bo'lmaydi.

```yaml
# .github/dependabot.yml
# Maqsad: patch yangilanishlari avtomatik, minor haftalik, major qo'lda.
version: 2
updates:
  - package-ecosystem: maven
    directory: "/"
    schedule:
      interval: weekly
      day: tuesday
    open-pull-requests-limit: 5
    groups:
      # Spring ekotizimi bitta PR bo'lib keladi, aks holda versiya urushi bo'ladi.
      spring:
        patterns: ["org.springframework*", "org.springframework.boot*"]
      test-kutubxonalari:
        patterns: ["org.junit*", "org.mockito*", "org.testcontainers*"]
    ignore:
      # Major yangilanish ADR talab qiladi, bot o'zi ochmaydi.
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
```

Qoida: bog'liqlik qo'shish PR'ida uchta savolga yozma javob bo'lsin. Qanday muammoni hal qiladi, standart kutubxona bilan necha qatorda hal bo'ladi, kim yangilab turadi.

Uchinchi savolning narxi vaqt bilan o'sadi, shuning uchun yangilash ritmini ham qoidaga aylantirish kerak. *Software Engineering at Google* ning kuzatuvi aniq: til, kompilyator va freymvork yangilanishini muntazam qilish uni arzonlashtiradi, chunki eng qimmat yangilanish birinchisi bo'ladi. Kitobning misoli 2006 yildagi kompilyator yangilanishi: o'sha paytda kompaniya bir necha ming injener bilan ishlayotgan edi, kompilyator taxminan besh yil yangilanmagan, injenerlarning ko'pi kompilyator o'zgarishini boshdan kechirmagan va kodning ko'p qismi faqat bitta kompilyator versiyasini ko'rgan edi. Natija og'riqli bo'ldi: kod bazasiga katta va kichik Hyrum qonuni muammolari kirib, muayyan kompilyator versiyasiga bog'liqlikni chuqurlashtirgan, va bu yashirin bog'liqliklarni uzish qimmat tushgan. Ogohlantirishning umumiy shakli ham bor: kompilyator yangilanishi deyarli har doim xulqni ozgina o'zgartiradi, ya'ni noto'g'ri kompilyatsiyani tuzatadi, optimizatsiyani o'zgartiradi yoki avval aniqlanmagan narsalarning natijasini o'zgartirishi mumkin, demak "orqaga moslik bor" degan gap tekshiruvni almashtirmaydi. Teskari tomoni ham narxga ega: yangilanmaslik xavfsizlik va samaradorlik xarajatini jim yig'adi.

## 38.6 Moda texnologiyani baholash: qaysi muammoni hal qiladi, sizda u bormi

Har bir moda texnologiya haqiqiy muammoni hal qiladi, lekin odatda sizning muammoyingizni emas. Ikki savoldan boshlang: bu texnologiya qaysi og'riqni yo'q qiladi, va shu og'riq sizning metrikangizda ko'rinadimi.

Kafka'ning haqiqiy kuchi yuqori o'tkazuvchanlik va qayta o'qiladigan log. Agar hodisa oqimingiz past bo'lsa, PostgreSQL jadvali va `SELECT ... FOR UPDATE SKIP LOCKED` bilan yasalgan navbat yetishi mumkin. "Past" nimani bildirishini o'zingizning hodisa sonini va kechikish talabini o'lchab aytasiz: umumiy chegara yo'q.

```sql
-- SKIP LOCKED consumer'larni bir-biriga to'qnashtirmaydi; o'tkazuvchanlikni o'z muhitingizda o'lchang.
CREATE TABLE buyurtma_hodisasi (
    id          bigserial PRIMARY KEY,
    holat       text NOT NULL DEFAULT 'YANGI',
    yuklama     jsonb NOT NULL,
    urinish     int  NOT NULL DEFAULT 0,
    yaratilgan  timestamptz NOT NULL DEFAULT now()
);
-- Faqat ishlanmagan qatorlar indeksda: indeks kichik qoladi.
CREATE INDEX ON buyurtma_hodisasi (id) WHERE holat = 'YANGI';

-- Consumer'ning bitta tsikli.
WITH olingan AS (
    SELECT id FROM buyurtma_hodisasi
    WHERE holat = 'YANGI'
    ORDER BY id
    LIMIT 100
    FOR UPDATE SKIP LOCKED
)
UPDATE buyurtma_hodisasi b SET holat = 'ISHLANMOQDA'
FROM olingan o WHERE b.id = o.id
RETURNING b.id, b.yuklama;
```

Reactive stack uchun ham shu mantiq. WebFlux ko'p ming parallel ulanishda thread tejaydi, lekin Java 21 dan keyin virtual thread shu muammoning katta qismini oddiy blokirovka qiluvchi kod bilan hal qiladi. Parallel so'rov soningiz past bo'lsa, reactive sizga asosan debug qiyinchiligini beradi; chegarani metrikadan oling, taxmindan emas.

Baholashni yozma shaklga soling: muammo, joriy metrika, da'vo, o'lchov rejasi, voz kechish sharti. Agar "joriy metrika" qatori bo'sh bo'lsa, bu moda, muammo emas.

Bitta vaqt qoidasi ham bor va u texnologiyaning o'ziga emas, uni kiritish paytiga tegishli. Newman mikroservisga o'tishda yangi texnologiyani birga olib kirmaslikni qat'iy tavsiya qiladi: har qanday yangi texnologiya qabul qilish narx bilan keladi va tartibsizlik keltiradi, mikroservis arxitekturasini boshlaganda esa band bo'ladigan narsa allaqachon yetarli. Mantiq ham aytilgan: mikroservisni rivojlantirish va boshqarish taqsimlangan tizimlarning ko'p muammosini hal qilishni talab qiladi va ularning bir qismi siz uchun yangi; bu muammolarni tanish texnologiya steki bilan, ular paydo bo'lgan sayin o'zlashtirish ancha foydali, keyin esa mavjud texnologiyani almashtirish yordam berishini ko'rib chiqish mumkin. Kitobning umumiy formulasi: mikroservis texnologiyadan mustaqil, servislar tarmoq orqali gaplasha olsa qolgani ochiq, va PHP ni eng yaxshi bilsangiz servislarni PHP da qurishdan boshlang. Shundan amaliy xulosa chiqadi, platformani bir yil oldindan qurish xato; texnologiya aniq to'siqqa javoban qo'shiladi.

Shu yerda korpus ichida bitta nozik farq bor va uni aralashtirmaslik kerak: [patterns 25.72](../patterns/25-anti-patternlar.md#2572-rezyume-uchun-dasturlash-resume-driven-development) yangi texnologiyani umuman taqiqlashni ham antipattern deb ataydi. Ikki gap zid emas, ular turli vaqt haqida: yangi texnologiya taqiqlanmaydi, lekin u katta arxitektura o'tishi bilan bir vaqtda kiritilmaydi.

Ford va sheriklari shu yondashuvni ikki qoida bilan mustahkamlaydi. Birinchisi kitobning boshlanish nuqtasi: haqiqiy murakkab tizimlarga qo'llanadigan universal "best practice" yo'q, shuning uchun har qarorda trade-off o'z kontekstida tahlil qilinadi (The Hard Parts, 2-bob, 26-bet). Ikkinchisi "out-of-context" tuzog'i: umumiy mezonlar jadvalida g'olib chiqqan yechim kontekst qo'shilganda yutqazishi mumkin, shuning uchun qaror iterativ ravishda, aniq domen holatlarini modellashtirib tekshiriladi (The Hard Parts, 15-bob, 405-407-bet).

## 38.7 Qurish yoki sotib olish qarori va mezonlari

Bu qarorni "qiziqarli" mezoni bilan emas, uch yillik egalik narxi bilan qiling: boshlang'ich ishlab chiqish, yillik saqlash, navbatchilik yuki, integratsiya va o'rganish vaqti.

Agar komponent sizning raqobat ustunligingiz bo'lsa, o'zingiz quring. To'lov marshrutlash mantig'i, narx hisoblash, ombor rezervatsiya qoidalari shu toifada.

Agar komponent hamma uchun bir xil bo'lsa, tayyorini oling. Autentifikatsiya, email yuborish, PDF generatsiya, log agregatsiya, feature flag. Bu yerda o'zingiz qurish deyarli har doim yo'qotish.

Chegara holat: komponent standart, lekin talablaringiz g'alati. Tayyorini oling, interface ortiga yashiring, g'alati qismni o'zingiz yozing.

Qarorni biznes egasiga tushuntirganda butun jadvalni ko'rsatmaslik kerak. Ford va sheriklari buni alohida tavsiya qilib qo'yadi: yig'ilgan hamma dalilni yoyish o'rniga trade-off tahlilini bir nechta asosiy nuqtaga siqish kerak, chunki texnik tafsilot biznes tomoniga qaror qo'shmaydi, faqat diqqatni so'raydi (The Hard Parts, 15-bob, 409-410-bet).

| Mezon | Qurish foydasiga | Sotib olish foydasiga |
|---|---|---|
| Biznes farqlovchisi | Ha, mantiq bizga xos | Yo'q, hamma bir xil qiladi |
| Talablarning barqarorligi | Tez o'zgaradi, nazorat kerak | Yillar davomida o'zgarmaydi |
| Jamoa ekspertizasi | Bizda shu sohada chuqur bilim bor | Bilim yo'q, o'rganish uzoq cho'ziladi |
| Ishga tushirish muddati | Muddat yetarli | Muddat juda qisqa |
| Uch yillik narx | Saqlash yuki kichik va o'lchangan | Litsenziya ishlab chiqishdan arzon |
| Muvofiqlik talabi | Audit izini o'zimiz nazorat qilamiz | Vendor sertifikatlangan |
| Chiqish narxi | Kod bizda, chiqish shart emas | Adapter ortida, ko'chish mumkin |

## 38.8 Tajriba uchun vaqt ajratish: spike, ichki loyiha, o'lchovli tajriba

Tajribani kayfiyatga qoldirmang, uni sprintga element qilib kiriting. Uch format ishlaydi.

Spike: vaqt chegarasi qat'iy va oldindan yozilgan. Savol bitta va yozma. Natija kod emas, balki qaror va o'lchov.

Ichki loyiha: past xatarli haqiqiy servisda sinash, masalan ichki hisobot generatori. U buzilsa mijoz ko'rmaydi, lekin siz real yuk va real deploy jarayonini ko'rasiz.

O'lchovli tajriba: production'da, lekin trafikning kichik qismida. Yangi kesh strategiyasini so'rovlarning kichik ulushiga yoqib, latency taqsimotini solishtirish.

Bu uchlik ThoughtWorks radar halqalariga mos tushadi: `assess` halqasida texnologiya spike va tadqiqot loyihasi bilan baholanadi, `trial` halqasida esa past xatarli real loyihada sinaladi (Fundamentals of Software Architecture, 24-bob). Richards va Ford yana bir ogohlantirish beradi: tashlab yuborish uchun yozilgan proof-of-concept kodi ko'pincha repozitoriyga tushib, boshqalar uchun namuna bo'lib qoladi, shuning uchun POC kodini ham production sifatida yozish kerak (2-bob). Demak "spike kodi production'ga kirmaydi" degan og'zaki kelishuvga tayanmang: spike'ni alohida branch va modulda tuting.

```java
// Spike natijasi raqam bo'lishi kerak, taassurot emas.
// JMH bilan ikki kutubxonani bir xil sharoitda o'lchash.
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@Fork(value = 2, jvmArgs = {"-Xms1g", "-Xmx1g"})
@Warmup(iterations = 5, time = 2)       // JIT qizishi uchun
@Measurement(iterations = 10, time = 5) // o'lchov qismi
@State(Scope.Benchmark)
public class HisobotSerializatsiyaBenchmark {

    private List<HisobotQatori> qatorlar; // 10 000 qator, realga yaqin

    @Setup public void tayyorla() { qatorlar = TestMalumot.hisobot(10_000); }

    @Benchmark public byte[] jackson() throws Exception {
        return jacksonMapper.writeValueAsBytes(qatorlar);
    }

    @Benchmark public byte[] nomzodKutubxona() throws Exception {
        return nomzod.serialize(qatorlar);
    }
}
```

Spike hujjati bir sahifadan oshmasin: savol, usul, o'lchov jadvali, qaror, voz kechish sharti.

## 38.9 Bilimni jamoaga tarqatish: hujjat, suhbat, namuna kod

Bir kishining boshidagi bilim arxitektura xatari. Google'ning injenerlik amaliyoti bu xatarga nom beradi: kritik ma'lumot faqat bitta odamda bo'lsa, bu single point of failure, va u ko'pincha yaxshi niyatdan ("men o'zim qilib beraman") o'sadi. Natijasi all-or-nothing ekspertiza: bir tomonda "hammasini biladigan" bir necha odam, ikkinchi tomonda yangilar, o'rtada hech kim. Yozilgan bilim va odamdagi bilim bir-birini almashtirmaydi, to'ldiradi: hujjat butun tashkilot darajasiga ko'tariladi, odam esa javobni kontekstga moslab beradi va hujjat hali o'z kuchidami yoki yo'qligini aytadi (Software Engineering at Google, 3-bob).

Uni tarqatishning uchta formati ishlaydi.

Birinchi: qisqa qaror yozuvi, har bir muhim qaror uchun bir sahifa. Kontekst, variantlar, tanlangan yo'l, natijalar, voz kechish sharti. `docs/decisions/` papkasida, kod bilan birga versiyalanadi.

Ikkinchi: ichki ko'rsatuv. 30 daqiqa, slayd emas, ekranda tirik kod. Eng yaxshi mavzu "o'tgan haftadagi incident va asl sababi".

Uchinchi va eng kuchlisi: ishlaydigan namuna kod. Jamoa hujjat o'qimaydi, lekin namunani ko'chiradi.

```properties
# docs/namunalar/outbox/application.properties
# Jamoa shu fayldan ko'chiradi, shuning uchun har bir qiymat izohlangan.

# Pool o'lchami: CPU yadrosi * 2 + disk kutish. 4 yadro uchun taxminan 10.
spring.datasource.hikari.maximum-pool-size=10
# Ulanish olish uchun kutish: so'rov timeout'idan kichik bo'lishi shart.
spring.datasource.hikari.connection-timeout=3000
# Ochiq qolgan ulanishni aniqlash: leak bo'lsa log yoziladi.
spring.datasource.hikari.leak-detection-threshold=20000

# Batch insert: outbox yozuvlari to'plam bilan ketadi.
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true

# Statement darajasidagi timeout: uzoq so'rov pool'ni band qilmaydi.
spring.jpa.properties.hibernate.jakarta.persistence.query.timeout=5000
```

Namuna kodning teskari ta'siri ham bor. Google kitobi maqsadini tushunmasdan pattern yoki kodni ko'chirishni "parroting" anti-pattern deb ataydi: kod nima uchun kerakligi bilinmay ko'chiriladi (Software Engineering at Google, 3-bob). Shu sababli namunadagi har bir qiymat izohlanadi va namuna CI da test qilib turiladi: testlanmagan namuna tez eskirib, noto'g'ri bilim tarqatadi.

## 38.10 Xatolardan o'rganishni odat qilish va o'z qarorlarini qayta ko'rish

Incident'dan keyin "kim aybdor" savoli o'rniga "qaysi signal yetishmadi" savolini bering. Birinchi savol odamni yashirishga o'rgatadi, ikkinchisi tizimni yaxshilaydi.

McConnell buni bitta jumlaga siqadi: samarali programmalashning kalitlaridan biri xatoni tez qilish va har safar undan o'rganish; xato qilish gunoh emas, xatodan o'rganmaslik gunoh (Code Complete, 2-nashr, 33.3, 823-bet). U yana intellektual halollikni alohida xususiyat qilib ajratadi: xatoni darhol tan olish va bilmagan joyda ekspert bo'lib ko'rinmaslik (33.4, 826-bet). Shu odatning tashkiliy sharti psixologik xavfsizlik: bilmasligini yoki xato qilganini tan olish jazolanmasa, jamoa o'rganadi, aks holda qo'rquv madaniyati paydo bo'ladi (Software Engineering at Google, 3-bob).

Har bir incident'dan uchta natija chiqsin: muammoni oldin ko'rsatadigan metrika, shu holatni qaytaradigan test, va qaror xato bo'lgan bo'lsa qaror yozuvining yangilangan versiyasi.

Qarorlarni rejali qayta ko'rish odati kam uchraydi, lekin eng qimmatlisi. Har chorakda qaror papkasini oching va har biriga bitta savol bering: bugungi bilim bilan shu qarorni yana qabul qilarmidim.

Qayta ko'rishning teskari xatosi ham bor. Richards va Ford "frozen caveman" anti-pattern'ini shunday ta'riflaydi: bir marta kuyib chiqqan arxitektor har bir yangi arxitekturada o'sha shaxsiy qo'rquviga qaytadi va ehtimolligi juda past bo'lgan holatni markazga qo'yadi. Shu sababli qayta ko'rishda haqiqiy texnik xatarni o'ylab topilganidan ajratish kerak (Fundamentals of Software Architecture, 2-bob).

```bash
# Chorakda bir marta: olti oydan oshgan qarorlarni qayta ko'rishga chiqarish.
cd docs/decisions
for f in *.md; do
  # Fayl oxirgi marta qachon o'zgargan.
  oxirgi=$(git log -1 --format=%ad --date=short -- "$f")
  kun=$(( ( $(date +%s) - $(date -d "$oxirgi" +%s) ) / 86400 ))
  if [ "$kun" -gt 180 ]; then
    holat=$(grep -m1 '^Holat:' "$f" || echo 'Holat: yoq')
    printf '%-45s %4s kun  %s\n' "$f" "$kun" "$holat"
  fi
done | sort -k2 -n -r
```

Shu ro'yxatdan chorakda eng ko'pi bilan uchtasini tanlang. Hammasini qayta ko'rishga urinish rejani o'ldiradi.

## 38.11 Java va Spring ekotizimini kuzatib borish usullari

Maqsad hamma narsani o'qish emas, sizga tegadigan o'zgarishni vaqtida ko'rish.

Kuzatuvni kayfiyatga qoldirmaslik uchun Richards va Ford "20 daqiqa qoidasi" ni beradi: kuniga kamida 20 daqiqani notanish atamani o'rganishga yoki bitta mavzuni chuqurlashtirishga ajratish. Ularning aniq tavsiyasi shu 20 daqiqani tushlikka yoki kechqurunga qoldirmaslik, balki ertalab, qahvadan keyin va email'ni ochishdan OLDIN bajarish, chunki email ochilgach kun boshqa tomonga ketadi (Fundamentals of Software Architecture, 24-bob).

JDK tomoni. Har yarim yilda feature reliz chiqadi, LTS esa ikki yilda: Java 17, 21 va 25. Har reliz uchun avval faqat JEP ro'yxatini o'qing. Sizga tegadigan JEP bo'lsa, to'liq matnini o'qing.

Yangi JDK ni lokal mashinada sinash bir buyruq ishi.

```bash
# Yangi LTS ni lokal sinash: SDKMAN bilan yonma-yon o'rnatiladi.
sdk install java 25-tem
sdk use java 25-tem

# Deprecated va olib tashlangan API larni kompilyatsiyada ko'rish.
mvn -q clean compile -Dmaven.compiler.release=25 \
    -Dmaven.compiler.showDeprecation=true 2>&1 | grep -i 'deprecat\|removed'

# Reflection va native access ogohlantirishlari: kelgusi relizda xato bo'ladi.
java --illegal-native-access=warn -jar target/app.jar 2>&1 | head -40

# Startup va xotira farqini o'lchash.
/usr/bin/time -f "%e s, %M KB" java -jar target/app.jar --test-start
```

Spring tomoni. Minor relizlar taxminan har olti oyda chiqadi. Faqat migration guide va o'zingiz ishlatadigan modullar o'zgarishini o'qing. Eskirayotgan konfiguratsiyani qo'lda izlamang: `spring-boot-properties-migrator` ni vaqtincha bog'liqlik qilib qo'shsangiz, startup'da eski kalitlarni ro'yxat qilib beradi.

PostgreSQL tomoni. Har yil bitta major reliz. Faqat "Migration to Version X" va planner o'zgarishlarini o'qing. Planner o'zgarishi eng og'ir so'rovlaringizni sekinlashtirishi mumkin, shuning uchun yangilashdan oldin `pg_stat_statements` dan eng qimmat 20 so'rovni saqlab qo'ying va keyin solishtiring.

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| Blog postdan javob oladi | Reference hujjat va manba kodni o'qiydi |
| Yangi kutubxonani "qiziq" bo'lgani uchun qo'shadi | Yetti mezon bo'yicha yozma baho beradi |
| Bog'liqlikni qo'shib, unutadi | Yangilashni Dependabot guruhlari bilan avtomatlashtiradi |
| Reactive'ga o'tadi, chunki moda | Parallel so'rov sonini o'lchab, virtual thread bilan hal qiladi |
| Hammasini o'zi quradi, chunki shunday qiziqarli | Biznes farqlovchisini quradi, qolganini sotib oladi |
| Vendor sinfini butun kodga sochadi | Vendorni bitta adapter ortiga yashiradi |
| Spike'ni cheksiz davom ettiradi | Spike'ga 3 kun va bitta yozma savol beradi |
| LTS yangilashini oxirgi daqiqada boshlaydi | Yangi JDK ni chiqqan kuni lokal build'da sinaydi |
| Bilimni o'z boshida saqlaydi | Testlanadigan namuna kod va qaror yozuvi qoldiradi |
| Qarorni bir marta qabul qiladi | Har chorakda uchta qarorni qayta ko'rib chiqadi |

| Tuzoq | Yechim |
|---|---|
| Faqat `current` hujjatni o'qish, versiya mos kelmaydi | URL ichida aniq versiyani tanlash odatini qilish |
| Dependabot PR lari to'planib, hech kim ko'rmaydi | Guruhlash, limitni 5 ga qo'yish, haftada bir vaqt ajratish |
| Major yangilashni bot avtomatik ochadi va build sinadi | Major'ni `ignore` ga kiritib, qo'lda ADR bilan qilish |
| Spike kodi production'ga sirg'alib kiradi | Spike'ni alohida branch'da va `-spike` moduli ichida qilish |
| Benchmark JIT qizimasdan o'lchanadi, natija yolg'on | JMH va warmup iteratsiyalari, forklangan JVM |
| Yangi kutubxona Jackson major versiyasini tortadi | `dependency:tree` va enforcer bilan banned versiyani bloklash |
| PostgreSQL major yangilashdan keyin so'rov sekinlashadi | Yangilashdan oldin eng qimmat 20 so'rovni saqlab, solishtirish |
| Namuna kod eskiradi va noto'g'ri bilim tarqatadi | Namunani CI da test qilib turish |

## 38.12 O'z o'rganish rejangizni tuzish: chorak uchun aniq maqsadlar

"Kafka o'rganaman" maqsad emas, u istak. Maqsad uchta qismdan iborat: nima qilaman, qanday isbotlayman, qancha vaqt.

Chorak uchun uchta maqsaddan oshmaslik shu korpusning amaliy qoidasi, kitobdan olingan budjet emas. Kitoblar beradigan narsa boshqa va ikkita. Birinchisi kunlik oyna: 20 daqiqa qoidasi (38.11). Ikkinchisi shaxsiy radar, ya'ni texnologiyalarni `hold`, `assess`, `trial` va `adopt` halqalariga joylashtirib yozma holda saqlash; Richards va Ford radarning o'zidan ko'ra uni to'ldirish uchun ajratilgan vaqt muhimroq ekanini aytadi, chunki band arxitektor uchun vaqt ajratishning boshqa bahonasi bo'lmaydi (Fundamentals of Software Architecture, 24-bob).

Tuzilgan o'qish rejasiga tayyor namuna ham bor: McConnell darajalarga bo'lingan o'qish rejasini beradi, kirish, praktik va professional daraja uchun alohida kitob ro'yxati bilan (Code Complete, 2-nashr, 35.4, 860-862-bet). Ro'yxatning o'zi 2004 yilgi, lekin shakli hamon ishlaydi: daraja, ro'yxat va keyingi darajaga o'tish sharti. Shu shaklni o'z stack'ingiz uchun qayta to'ldirishingiz mumkin.

Yaxshi yozilgan maqsad shunday ko'rinadi. "Ombor harakatlari jadvalini oylik partition'ga bo'lish bo'yicha spike qilaman. Isbot: 50 million qatorli test ma'lumotida oylik hisobot so'rovining latency farqini o'lchagan hujjat va qaror yozuvi." Natija ham o'lchanadi, ham ishga tegishli.

Har bir maqsadni joriy og'riqqa bog'lang. Agar eng og'ir incident'laringiz pool to'lishidan bo'lsa, chorak maqsadi connection pool bo'lsin, vector database emas.

Chorak oxirida ikki savol bering: uchta maqsaddan qanchasi isbotlangan natija bilan tugadi, va qaysi biri ishga ta'sir qildi. Birortasi ham tugamagan bo'lsa, muammo rejada emas, vaqt ajratishda.

## 38.13 Baza turini tanlash: yettita mezon va nega ular birga ishlaydi

[Kutubxonani baholash](#384-yangi-kutubxonani-baholash-mezonlari-qollab-quvvatlash-bogliqlik-chiqish-yoli) mezonlari baza turiga yetmaydi, chunki bazadan voz kechish narxi kutubxonadan voz kechish narxiga o'xshamaydi. *The Hard Parts* bu qarorni alohida qo'yadi va sababini aytadi: 2005 yildan beri baza texnologiyalarida inqilob bo'ldi va mahsulotlar soni "tanlov paradoksi" ni yuzaga keltirdi, ya'ni har bir mahsulot ma'lum kelishuvlar uchun optimallashtirilgan, demak tanlash ishi dasturiy va ma'lumot arxitektorlariga tushadi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021, 6-bob, 161-bet). Bu qaror [bazani bo'lish sabablari](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md#518-bazani-bolish-sabablari-oltita-disintegrator-va-ikkita-integrator) dagi oltinchi disintegratorning davomi: monolit baza bo'lingandan keyingina ma'lumotning bir qismini boshqa turga ko'chirish mumkin bo'ladi.

Kitob har bir baza turini yetti mezon bo'yicha yulduz bilan baholaydi (6-bob, 161-162-betlar).

| Mezon | Savol |
| --- | --- |
| O'rganish osonligi | Yangi dasturchi, modelchi va DBA uni qancha vaqtda o'zlashtiradi? SQL ni ko'pchilik biladi, Gremlin kabi graf tili esa tor ko'nikma |
| Modellash osonligi | Domen shu modelda qanchalik tabiiy ifodalanadi va modellangandan keyin o'zgartirish osonmi |
| Masshtab va o'tkazuvchanlik | Baza gorizontal, vertikal yoki ikki yo'nalishda ham masshtablanadimi |
| Mavjudlik va partition ga chidamlilik | Yuqori mavjudlik konfiguratsiyasi bormi, tarmoq bo'linishini qanday boshqaradi |
| Izchillik | ACID tranzaksiya bormi, yoki eventual izchillik bilan BASE tomonga og'adimi; izchillikni sozlash mumkinmi |
| Til qo'llab-quvvatlashi, yetuklik, SQL va jamoa | Qancha til bilan ishlaydi, qanchalik yetuk, va shu bazani biladigan odamni ishga olish osonmi |
| O'qish va yozish ustuvorligi | Baza o'qishni, yozishni yoki ikkisini muvozanatda optimallashtiradimi; bu ikkilik tanlov emas, shkala |

Oxirgi mezon ko'pincha e'tibordan chetda qoladi, lekin aynan u xato tanlovni oldini oladi: kitob buni ikkilik tanlov emas, bazaning qaysi yo'nalishda optimallashtirilganini ko'rsatadigan shkala deb ta'riflaydi (6-bob, 162-bet).

PostgreSQL bilan ishlaydigan jamoa uchun amaliy foyda shu mezonlarni o'z bazasiga qo'llashdan chiqadi. Kitob relyatsion bazalar uchun quyidagi baholarni beradi (6-bob, 163-164-betlar): o'rganish oson, chunki ular o'n yillardan beri o'qitiladi va hujjati yetuk; modellash moslashuvchan, kalit-qiymat, hujjat va hatto grafga o'xshash tuzilmalarni ko'tara oladi va yangi indeks qo'shish bilan o'qish shakli o'zgaradi, lekin ixtiyoriy chuqurlikdagi graf tuzilmasi qiyin qoladi; masshtab odatda vertikal, replikatsiya va avtomatik almashtirishni sozlash esa ko'p muvofiqlashtirish talab qiladi; mavjudlik va partition ga chidamlilikdan ko'ra izchillik tanlanadi; ACID bir vaqtda ishlaydigan tizimdagi ko'p tashvishni hal qiladi; jamoa katta va yetuk, lekin reactive stream API lari kabi yangi tushunchalar relyatsion bazalarda kech paydo bo'ladi; o'qish va yozish ustuvorligi esa muvozanatda, ya'ni ma'lumot modelini o'qish yoki yozish foydasiga loyihalash mumkin.

Natijada tanlov qoidasi oddiy shaklga keladi: PostgreSQL ni almashtirish uchun yetti mezondan kamida bittasi keskin yutuq berishi va qolganlaridagi yo'qotish shu yutuqdan kichik bo'lishi kerak. Kitobning o'z misoli aynan shunday ko'rinadi: relyatsion bazada yashayotgan ma'lumotnoma kalit-qiymat shakliga mos kelgani uchun kalit-qiymat baza mosroq bo'ladi (6-bob, 146-bet). Qaror esa [ADR](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat) shaklida yoziladi, chunki uning oqibati yillarga cho'ziladi.

Tanlovdan oldin birinchi mezonni tekshirish arzon: mavjud baza so'ralgan shaklni allaqachon ko'tara oladimi. PostgreSQL da bu bitta so'rov bilan sinaladi.

```sql
-- Kalit-qiymat va hujjat shakli PostgreSQL ning o'zida ham bor: alohida
-- baza turiga o'tishdan oldin jsonb va GIN indeksini o'lchab ko'rish kerak.
CREATE TABLE reference_data (
    kind    text  NOT NULL,
    code    text  NOT NULL,
    payload jsonb NOT NULL,
    PRIMARY KEY (kind, code)
);

CREATE INDEX idx_reference_payload ON reference_data USING gin (payload jsonb_path_ops);

EXPLAIN (ANALYZE, BUFFERS)
SELECT code, payload
FROM reference_data
WHERE kind = 'warehouse' AND payload @> '{"region": "EU"}';
```

ESLATMA: yuqoridagi "kamida bitta keskin yutuq" qoidasi va `jsonb` misoli shu korpusning amaliy tavsiyasi. Kitob mezonlarni va yulduz baholarini beradi, qaror formulasini bermaydi.

## 38.14 Bog'liqlikni boshqarish: fork, ega va tashqariga chiqarish

[38.5](#385-bogliqlik-qoshishning-yashirin-narxi-va-uni-yangilash-majburiyati) bitta bog'liqlikni qo'shish qarorini beradi. Tashkilot darajasida esa savol boshqa: bitta bog'liqlikni emas, bog'liqliklar tarmog'ini va uning vaqt bo'yicha o'zgarishini boshqarish kerak bo'ladi. *Software Engineering at Google* bu farqni aniq qo'yadi: ko'p yarim tayyor yechim muammoni juda tor qo'yadi, "mahalliy kodimiz tayanadigan paketni qanday import qilamiz" degan savol zarur, lekin yetarli emas. Haqiqiy savollar boshqa: tarmoqdagi barcha node larning yangi versiyasi chiqqanda yangilanishlar kaskadini qanday boshqarish, o'zimiz nazorat qilmaydigan bog'liqliklarning o'zaro mos versiyalarini qanday topish, va doim o'sib boradigan grafni qanday tahlil qilish. Shu bobda to'rtta qaror yozuvi bor.

**Imkon bo'lsa bog'liqlik muammosini manba nazorati muammosiga aylantirish.** Google ning ichki bog'liqliklarining katta qismi ichki ishlab chiqilgan, demak ichki bog'liqlikni boshqarish aslida bog'liqlikni boshqarish emas, shunchaki manba nazorati, va bu ataylab shunday. Sabab nomlangan: provayder ham, iste'molchi ham bir tashkilotda bo'lsa va to'g'ri ko'rinish hamda CI mavjud bo'lsa, bog'liqlik qo'shishning murakkabligi va xavfini boshqarish ancha oson; bog'liqlikni boshqarishdagi ko'p muammo kodingiz qanday ishlatilayotganini aniq ko'rib, har qanday o'zgarishning ta'sirini aniq bilganda muammo bo'lishdan to'xtaydi. Kitobning qisqa formulasi: manba nazorati (loyihalarni o'zingiz nazorat qilganda) bog'liqlikni boshqarishdan (nazorat qilmaganda) ancha oson. Amalda bu "tashkilot" tushunchasini kengaytirishga undaydi: boshqa jamoaning kodi uchun ham imkon bo'lsa bitta repozitoriya yoki birga versiyalanadigan modullar afzal, va bu [patterns 22.43](../patterns/22-deployment-va-operatsion-patternlar.md#2243-har-mikroservisga-bitta-repozitoriya-one-repository-per-microservice-multirepo) dagi repozitoriya qarori bilan bir xil mantiq.

**Fork qarori umr va doira bilan o'lchanadi.** Kutubxonani fork qilish yoki qayta yozish nazorat beradi: tor muammo uchun moslashtirilgan yechim umumiy yechimdan tezroq ishlashi mumkin, yangi xususiyat qo'shish osonlashadi, va eng muhimi quyi bog'liqliklardagi o'zgarishlardan izolyatsiya qilinadi, ya'ni o'zgarishni boshqa jamoa yoki uchinchi tomon dikta qilmaydi. Narxi esa masshtabda chiqadi: agar har dasturchi mavjud narsani qayta ishlatmay fork qilsa, xavfsizlik muammosiga javob berish endi bitta bog'liqlikni va uning foydalanuvchilarini yangilash emas, o'sha bog'liqlikning har bir zaif fork ini va ularning foydalanuvchilarini topish ishiga aylanadi. Shundan mezon chiqadi: loyiha umri qisqa bo'lsa fork kamroq xavfli, fork doirasi isbotlanadigan darajada cheklangan bo'lsa ham yengillashadi, lekin vaqt va loyiha chegaralaridan o'tadigan interfeyslar uchun fork qilinmaydi, ya'ni ma'lumot tuzilmalari, serializatsiya formati va tarmoq protokoli.

**Har umumiy bog'liqlikning nomli egasi bo'ladi va egalik yangilanadi.** Kitobning hikoyasi bu qoidaning sababini beradi. Alice ta'tilga ketishdan oldin demoni tugatish uchun ochiq kodli paketni `third_party` ga qo'shadi; siyosat talablari sodda, build tizimi bilan yig'ilishi, shu paketning mavjud versiyasi yo'qligi va kamida ikki injener OWNERS sifatida yozilishi. Alice hamkasbi Bob dan "ha, yordam beraman" degan javob oladi. Ikkisi ham `third_party` paketini saqlash tajribasiga ega emas va paket implementatsiyasi haqida hech narsa tushunish zaruratidan qulay qochgan. Keyin paket boshqa jamoalarga ham ochiq bo'ladi va yangi bog'liqliklar qo'shilishi Alice va Bob uchun butunlay ko'rinmas qoladi: ular to'g'ridan to'g'ri ishlatishni kuzatsa ham, tranzitiv ishlatishning o'sishini sezmasligi mumkin. Charlie paketni Search infratuzilmasining ichiga qo'shadi va paket zararsizdan kritik infratuzilmaga o'tadi, lekin Charlie ga hech qanday signal bormaydi. Oxiri ma'lum: bir kun yangilanish kritik deb aytiladi, Bob menejmentga o'tgan va kod bazasiga ancha vaqt tegmagan, Alice boshqa jamoada va paketni qaytib ishlatmagan, OWNERS fayli esa o'zgarmagan; minglab loyiha unga bilvosita bog'langani uchun uni shunchaki o'chirib tashlab bo'lmaydi. Amaliy qoidalar shundan chiqadi: kamida ikki nomli ega, egalikni muntazam qayta tasdiqlash, tranzitiv ishlatish o'sishini kuzatish, va yangilashni muntazam hamda oson qilish.

**Kutubxonani tashqariga chiqarishdan oldin qo'llab-quvvatlash rejasi bo'ladi.** Kitob ikki xavfni ajratadi. Birinchisi obro': yomon amalga oshirilgan yoki to'g'ri saqlanmagan reliz tashkilot obro'siga zarar beradi, va Apache jamoasining qoidasi keltiriladi, "kod ustidan jamoa" ustuvor; ajoyib kod bersangiz ham jamoa a'zosi sifatida yomon bo'lsangiz, bu tashkilotga ham, kengroq jamoaga ham zarar. Ikkinchisi injenerlik samaradorligi: yaxshi niyatli reliz narsalarni sinxron ushlab turolmasangiz solig'a aylanadi, va kitobning keskin formulasi, vaqt o'tishi bilan hamma fork qimmat bo'ladi. Google ning 2006 yildagi C++ komanda satri flag kutubxonasini ochiq kodga chiqarishi aynan shunday tugadi: o'sha paytda katta ko'lamli refaktoring imkoni yo'q edi, shuning uchun ichkarida uni ishlatgan hamma narsa aynan o'z joyida qolishi kerak edi; repozitoriy "ichkarida ishlab chiqilgan kod" va "huquqiy yoki litsenziya masalasi bo'lishi mumkin kod" ga ajratilgan edi; va tashqi dasturchilardan kod qabul qilish huquqiy masala, chunki loyiha asoschisi o'sha hissani egallamaydi. Natijada loyiha yoki "devor ustidan tashlangan" reliz, yoki uzilgan fork bo'lishga mahkum edi. Qaror yozuvi uchun bu bitta savolga aylanadi: bu kutubxonani kim, qancha vaqt va qanday mandat bilan saqlaydi; javob bo'lmasa reliz qilinmaydi.

| Qaror | To'g'ri javob belgisi | Xato belgisi |
|---|---|---|
| Fork qilamizmi | qisqa umr, isbotlangan tor doira | fork ma'lumot tuzilmasi, serializatsiya yoki protokol ustida |
| Repo bitta bo'lsinmi | provayder va iste'molchi bir tashkilotda, CI bor | "import qilib qo'yamiz" degan yechim |
| Ega kim | OWNERS da ikki ism, oxirgi tasdiq sanasi bor | demo uchun qo'shilgan paket, egasi ketgan |
| Tashqariga chiqaramizmi | yozilgan qo'llab-quvvatlash mandati va muddati | "ochiq kod qilsak foydali bo'ladi" |

## 38.15 Amalda qo'llash

- [ ] O'z stack'ingiz uchun "chuqur" va "yuzaki" ro'yxatini yozing: chuqur ro'yxat qisqa bo'lsin, va har biri uchun isbotlovchi test bor-yo'qligini belgilang.
- [ ] `mvn dependency:tree` va `mvn help:effective-pom` ni ishga tushirib, eng ko'p tranzitiv bog'liqlik keltirayotgan starter yoki kutubxonani toping, uning kerakligini PR muhokamasiga qo'ying.
- [ ] `.github/dependabot.yml` faylini guruhlar bilan sozlang, major yangilanishlarni `ignore` ga kiritib, haftada bir marta 30 daqiqalik "yangilash oynasi" ni kalendarga qo'ying.
- [ ] Eng ko'p ishlatiladigan uchta tashqi kutubxona uchun chiqish yo'lini tekshiring: vendor sinfi nechta faylda import qilinganini `grep` bilan sanab, bir nechta faylda uchrasa adapter kiritishni rejaga qo'ying.
- [ ] Keyingi spike'ni yozma vaqt chegarasi va bitta yozma savol bilan sprintga element qilib kiritib, natijani JMH yoki `pg_stat_statements` raqami bilan hujjatlashtiring.
- [ ] `docs/decisions/` papkasini yarating yoki tartibga soling, olti oydan oshgan qarorlarni skript bilan ro'yxat qilib, ulardan uchtasini bu chorakda qayta ko'rishga belgilang.
- [ ] Joriy LTS'dan keyingi JDK ni SDKMAN bilan o'rnatib, loyihani shu versiyada kompilyatsiya qiling, deprecated va native access ogohlantirishlarini issue sifatida yozib qo'ying.
- [ ] Chorak uchun uchta o'rganish maqsadini yozing, har biriga o'lchanadigan isbot va kunlik 20 daqiqalik oyna qo'yib, ularni joriy incident ro'yxatidagi og'riq bilan bog'lang.

## Manbalar

- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020,
  1-bob - "keep current with latest trends" arxitektorning sakkizta asosiy kutilishidan biri
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*,
  O'Reilly, 2020, 1-bob ("Example: Compiler Upgrade" bo'limi) - yangilanishni muntazam
  qilish uni arzonlashtirishi, 2006 yildagi kompilyator yangilanishining besh yillik
  to'xtashdan keyin og'riqli bo'lishi, Hyrum qonuni muammolarining yashirin bog'liqlikni
  chuqurlashtirishi va kompilyator yangilanishining xulqni ozgina o'zgartirishi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*,
  O'Reilly, 2020, 1-bob ("Example: Deciding Between Time and Scale" bo'limi) - fork yoki
  bog'liqlik tanlovi, fork ning quyi o'zgarishlardan izolyatsiya qilishi, xavfsizlik
  muammosiga javobning har zaif fork ni topish ishiga aylanishi, hamda qisqa umr va tor
  doira mezoni bilan vaqt va loyiha chegaralaridan o'tadigan interfeyslar uchun taqiq
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*,
  O'Reilly, 2020, 21-bob ("Why Is Dependency Management So Difficult?",
  "How Google Handles Importing Dependencies", "Exporting Dependencies" bo'limlari) -
  bitta bog'liqlik emas tarmoqni boshqarish muammosi, manba nazoratining bog'liqlikni
  boshqarishdan osonligi, `third_party` siyosati va Alice hamda Bob hikoyasi orqali
  egasiz kritik bog'liqlik, tranzitiv ishlatishni kuzatish zarurati, kutubxonani
  tashqariga chiqarishdagi obro' va samaradorlik xavfi hamda gflags misoli
- Sam Newman, *Monolith to Microservices*, 1-nashr, O'Reilly, 2020, 1-bob (8-bet) -
  mikroservisga o'tishda yangi texnologiyani birga olib kirmaslik, tanish stek bilan
  boshlab muammolarni paydo bo'lgan sayin o'zlashtirish va keyin texnologiyani
  almashtirishni ko'rib chiqish
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020,
  2-bob - bilim piramidasi (bilganingiz, bilmasligingizni bilganingiz, bilmasligingizni
  bilmaganingiz), technical breadth va technical depth almashuvi, ikki disfunksiya,
  "frozen caveman" anti-pattern, "architecture is the stuff you can't Google",
  proof-of-concept kodini production sifatida yozish talabi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020,
  24-bob - 20 daqiqa qoidasi va uni ertalab email'dan oldin bajarish tavsiyasi, shaxsiy
  radar, ThoughtWorks Technology Radar halqalari (`hold`, `assess`, `trial`, `adopt`)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture:
  The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 1-bob (2-3-bet) - ekotizim o'zini bo'lak-bo'lak
  almashtiradi, shuning uchun diqqat implementatsiya tafsilotida emas, qaror va
  trade-off tahlilida
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture:
  The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 2-bob (26-bet) - murakkab tizimlar uchun universal
  "best practice" yo'q, javob Google'dan topilmaydi
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture:
  The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 15-bob (405-410-bet) - "out-of-context" tuzog'i va
  iterativ qaror tekshiruvi; dalil to'dasi o'rniga bir nechta asosiy nuqtani ko'rsatish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33.3 (822-823-bet) -
  texnik muhit xususiyatlari besh yildan o'n yilgacha oraliqda o'zgaradi, bilimning yarmi
  uch yilda eskiradi, xatoni tez qilib undan o'rganish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33.4 (826-bet) -
  intellektual halollik: xatoni tan olish va bilmagan joyda ekspert bo'lib ko'rinmaslik
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 35.4 (860-862-bet) -
  darajalarga bo'lingan o'qish rejasining shakli
- *Software Engineering at Google*, O'Reilly, 2020, 3-bob - single point of failure va
  all-or-nothing ekspertiza, yozilgan va odamdagi bilimning bir-birini to'ldirishi,
  "parroting" anti-pattern, psixologik xavfsizlik o'rganish sharti sifatida
- Joshua Bloch, *Effective Java*, 3-nashr, Addison-Wesley, 2018, Item 59 (267-bet) -
  platforma kutubxonasini bilish va ishlatish
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture:
  The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 6-bob (161-164-betlar) - 2005 yildan beri
  baza texnologiyalaridagi inqiroz va "tanlov paradoksi"; baza turini baholashning yetti
  mezoni (o'rganish osonligi, modellash osonligi, masshtab va o'tkazuvchanlik, mavjudlik va
  partition ga chidamlilik, izchillik, til qo'llab-quvvatlashi bilan yetuklik va jamoa,
  o'qish va yozish ustuvorligi) hamda relyatsion bazalar uchun shu mezonlar bo'yicha baho
- ESLATMA: 38.4 dagi yetti mezon ro'yxati, 38.7 dagi qurish/sotib olish jadvali, 38.8
  dagi uch format, 38.9 dagi uch format va 38.12 dagi "chorakda uchta maqsad" hamda 38.13 dagi "kamida bitta keskin yutuq" qoidasi shu
  korpusning amaliy tavsiyalari, kitobdan olingan taksonomiya emas
- ESLATMA: 38.3, 38.5, 38.11 va 38.14 dagi buyruqlar, `dependabot.yml` va namuna
  `application.properties` qiymatlari shu korpusning amaliy misollari; qiymatlar o'z
  muhitingizda o'lchanib tanlanadi
- Joshua Bloch, *Effective Java*, 3-nashr, Addison-Wesley, 2018, Item 59 (268-269-betlar) - kutubxonadan foydalanishning qolgan afzalliklari (ad-hoc yechimga vaqt ketmasligi, ishlashning sizning ishtirokingizsiz yaxshilanishi, funksionallikning o'sishi, kodning asosiy oqimda qolishi); har programmist `java.lang`, `java.util` va `java.io` asoslarini bilishi, asosiy asbob to'plamiga to'plamlar frameworki, oqimlar kutubxonasi va `java.util.concurrent` ning yuqori darajali qismlari kirishi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 16-bob (235-bet) - beqaror framework yoki API versiyasini tanlash ba'zan to'g'ri bo'lishi: eng yangi va yetarlicha barqaror versiya keyingi migratsiya majburiyatini yo'q qilishi, tez o'zgaradigan narsa uchun muqobilni ham ko'rib chiqish
- Simon Brown, *Software Architecture for Developers*, Leanpub, 12-bob (35-bet) - arxitektor har texnologiyada ekspert bo'lishi shart emasligi, bilmaganini tushunadigan odamni topib birga ishlash, rolni bo'lishish mumkinligi, o'z bilimidagi bo'shliqni tan olish birinchi qadam bo'lishi va pair architecting ning pair programming kabi foyda berishi

---

[&larr; 37. Xarajat, SLO va biznes bilan muloqot](37-xarajat-slo-va-biznes-bilan-muloqot.md) · [Mundarija](README.md) · [39. Birinchi 90 kun va o'z-o'zini baholash &rarr;](39-birinchi-90-kun-va-oz-ozini-baholash.md)
