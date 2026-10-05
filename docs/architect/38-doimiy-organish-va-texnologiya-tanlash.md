<!-- doc: architect | chapter: 38 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 38. Doimiy o'rganish va texnologiya tanlash (Continuous Learning and Technology Choice)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

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
- [38.13 Amalda qo'llash](#3813-amalda-qollash)

</details>



Arxitektorning bilimi ikki xil eskiradi. Birinchisi tezda chiriydi: kutubxona versiyasi, konfiguratsiya kaliti, bulut panelining joylashuvi. Ikkinchisi o'n yil yashaydi: tranzaksiya izolyatsiyasi, xotira modeli, indeks tanlash mexanikasi. Bu bob shu ikki qatlamni ajratish, yangi texnologiyani sovuq boshda baholash va o'rganishni chorakka bo'lingan o'lchovli rejaga aylantirish haqida.

## 38.1 Nimani chuqur o'rganish kerak va nimani yuzaki bilish yetarli

Chuqurlik darajasini ehtimollik bilan tanlang. Agar mexanika buzilganda production incident bo'lsa va uni siz tuzatishingiz kerak bo'lsa, u chuqur bilim. Agar hujjatni ochib 20 daqiqada javob topsa bo'lsa, u yuzaki bilim.

To'lov servisi uchun ro'yxat shunday. Chuqur: JDBC tranzaksiya chegarasi, Hibernate flush tartibi, PostgreSQL row lock va deadlock, HikariCP pool o'lchami, JVM GC pauzalari, `ExecutorService` va virtual thread semantikasi. Yuzaki: Flyway migratsiya sintaksisi, Jackson annotatsiyalari, Testcontainers moduli nomi, OpenAPI generator sozlamasi.

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

## 38.2 Uzoq yashaydigan bilim va tez eskiradigan bilim farqi

Standart va protokol darajasidagi bilim eng uzoq yashaydi. SQL'ning `SERIALIZABLE` semantikasi 1992 yildan beri o'zgarmagan, HTTP keshlash sarlavhalari 1999 yildan beri o'z kuchida.

Keyingi qatlam: implementatsiya mexanikasi. PostgreSQL MVCC va vacuum, Hibernate dirty checking, JVM escape analysis. Bu bilim 5 yildan 10 yilgacha yashaydi.

Eng tez eskiradigani: API sirti va konfiguratsiya nomi. `WebSecurityConfigurerAdapter` Spring Security 5.7 da deprecated bo'ldi va 6.0 da olib tashlandi. Konfiguratsiya nomini yodlash eng past daromadli investitsiya.

Amaliy qoida: o'qish vaqtingizning 60 foizini mexanikaga, 30 foizini joriy stack'ning reliz o'zgarishlariga, 10 foizini yangi texnologiyalarni kuzatishga ajrating.

## 38.3 Birlamchi manbalar: spetsifikatsiya, hujjat, manba kod, reliz eslatmasi

Blog postidan javob izlash odati arxitektorni sekin zaharlaydi. Blog ikkinchi qo'l, bitta versiyaga bog'langan va ko'pincha noto'g'ri. Birlamchi manbalar ketma-ketligini odat qiling.

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

Kutubxona tanlashni yozma mezon bilan qiling. Men yetti mezondan foydalanaman va har biriga raqam yoki aniq javob talab qilaman.

Birinchi: tiriklik. Oxirgi 12 oyda kamida 4 ta reliz bo'ldimi, loyihani bitta odam ushlab turadimi.

Ikkinchi: bog'liqlik og'irligi. Bitta JSON yordamchisi 14 ta tranzitiv jar olib kelsa, bu yomon signal.

Uchinchi: stack bilan to'qnashuv. Kutubxona Jackson yoki Netty ning boshqa major versiyasini talab qilsa, siz versiya urushiga kirasiz.

To'rtinchi: chiqish yo'li. Bir yildan keyin voz kechsangiz, qancha fayl o'zgaradi. Javob "beshdan kam" bo'lishi uchun interface ortiga yashiring.

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

## 38.5 Bog'liqlik qo'shishning yashirin narxi va uni yangilash majburiyati

Bog'liqlik qo'shganda siz kod emas, majburiyat olasiz. Har bir jar CVE yuzangizni, build vaqtini, startup vaqtini va yangilash ishini oshiradi.

Raqamlar bilan tushunarli bo'ladi. Oddiy Spring Boot web ilovasi taxminan 50 dan 70 ta jar bilan keladi, har bir yangi starter yana 5 dan 15 ta qo'shadi. 200 jar'dan oshgan ilovada yiliga taxminan 15 dan 30 ta CVE e'tiboringizni so'raydi, va ularning ko'pi sizga tegishli bo'lmasa ham, har birini ko'rib chiqish kerak. Startup ham sekinlashadi: har 50 ta qo'shimcha jar classpath skanerlashga taxminan 100 dan 300 millisekund qo'shadi.

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

## 38.6 Moda texnologiyani baholash: qaysi muammoni hal qiladi, sizda u bormi

Har bir moda texnologiya haqiqiy muammoni hal qiladi, lekin odatda sizning muammoyingizni emas. Ikki savoldan boshlang: bu texnologiya qaysi og'riqni yo'q qiladi, va shu og'riq sizning metrikangizda ko'rinadimi.

Kafka'ning haqiqiy kuchi yuqori o'tkazuvchanlik va qayta o'qiladigan log. Agar sizda kuniga 50 ming hodisa bo'lsa, PostgreSQL jadvali va `SELECT ... FOR UPDATE SKIP LOCKED` buni osongina ko'taradi.

```sql
-- PostgreSQL navbat taxminan 2000 msg/s ko'taradi, SKIP LOCKED consumer'larni to'qnashtirmaydi.
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

Reactive stack uchun ham shu mantiq. WebFlux ko'p ming parallel ulanishda thread tejaydi, lekin Java 21 dan keyin virtual thread shu muammoning katta qismini oddiy blokirovka qiluvchi kod bilan hal qiladi. Agar servisingiz 500 ta parallel so'rovdan oshmasa, reactive sizga faqat debug qiyinchiligini beradi.

Baholashni yozma shaklga soling: muammo, joriy metrika, da'vo, o'lchov rejasi, voz kechish sharti. Agar "joriy metrika" qatori bo'sh bo'lsa, bu moda, muammo emas.

## 38.7 Qurish yoki sotib olish qarori va mezonlari

Bu qarorni "qiziqarli" mezoni bilan emas, uch yillik egalik narxi bilan qiling: boshlang'ich ishlab chiqish, yillik saqlash, navbatchilik yuki, integratsiya va o'rganish vaqti.

Agar komponent sizning raqobat ustunligingiz bo'lsa, o'zingiz quring. To'lov marshrutlash mantig'i, narx hisoblash, ombor rezervatsiya qoidalari shu toifada.

Agar komponent hamma uchun bir xil bo'lsa, tayyorini oling. Autentifikatsiya, email yuborish, PDF generatsiya, log agregatsiya, feature flag. Bu yerda o'zingiz qurish deyarli har doim yo'qotish.

Chegara holat: komponent standart, lekin talablaringiz g'alati. Tayyorini oling, interface ortiga yashiring, g'alati qismni o'zingiz yozing.

| Mezon | Qurish foydasiga | Sotib olish foydasiga |
|---|---|---|
| Biznes farqlovchisi | Ha, mantiq bizga xos | Yo'q, hamma bir xil qiladi |
| Talablarning barqarorligi | Tez o'zgaradi, nazorat kerak | Yillar davomida o'zgarmaydi |
| Jamoa ekspertizasi | Bizda shu sohada chuqur bilim bor | Bilim yo'q, o'rganish 6 oy |
| Ishga tushirish muddati | 3 oy bor | 2 hafta bor |
| Uch yillik narx | Saqlash yillik 0.2 FTE dan kam | Litsenziya ishlab chiqishdan arzon |
| Muvofiqlik talabi | Audit izini o'zimiz nazorat qilamiz | Vendor sertifikatlangan |
| Chiqish narxi | Kod bizda, chiqish shart emas | Adapter ortida, ko'chish mumkin |

## 38.8 Tajriba uchun vaqt ajratish: spike, ichki loyiha, o'lchovli tajriba

Tajribani kayfiyatga qoldirmang, uni sprintga element qilib kiriting. Uch format ishlaydi.

Spike: vaqt chegarasi qat'iy, odatda 2 kundan 3 kungacha. Savol bitta va yozma. Natija kod emas, balki qaror va o'lchov. Spike kodi production'ga kirmasligini oldindan aytib qo'ying.

Ichki loyiha: past xatarli haqiqiy servisda sinash, masalan ichki hisobot generatori. U buzilsa mijoz ko'rmaydi, lekin siz real yuk va real deploy jarayonini ko'rasiz.

O'lchovli tajriba: production'da, lekin trafikning kichik qismida. Yangi kesh strategiyasini 5 foiz so'rovga yoqib, latency taqsimotini solishtirish.

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

Bir kishining boshidagi bilim arxitektura xatari. Uni tarqatishning uchta formati ishlaydi.

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

Namunani CI da test qilib turing: testlanmagan namuna olti oyda eskirib, noto'g'ri bilim tarqatadi.

## 38.10 Xatolardan o'rganishni odat qilish va o'z qarorlarini qayta ko'rish

Incident'dan keyin "kim aybdor" savoli o'rniga "qaysi signal yetishmadi" savolini bering. Birinchi savol odamni yashirishga o'rgatadi, ikkinchisi tizimni yaxshilaydi.

Har bir incident'dan uchta natija chiqsin: muammoni oldin ko'rsatadigan metrika, shu holatni qaytaradigan test, va qaror xato bo'lgan bo'lsa qaror yozuvining yangilangan versiyasi.

Qarorlarni rejali qayta ko'rish odati kam uchraydi, lekin eng qimmatlisi. Har chorakda qaror papkasini oching va har biriga bitta savol bering: bugungi bilim bilan shu qarorni yana qabul qilarmidim.

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

JDK tomoni. Har yarim yilda feature reliz chiqadi, LTS esa ikki yilda: Java 17, 21 va 25. Har reliz uchun faqat JEP ro'yxatini o'qing, bu 15 daqiqa. Sizga tegadigan JEP bo'lsa, to'liq matnini o'qing.

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

Chorak uchun uchta maqsaddan oshmang. Haftada 3 soat real vaqt chorakda taxminan 36 soat beradi, har maqsadga 12 soat tushadi.

Yaxshi yozilgan maqsad shunday ko'rinadi. "Ombor harakatlari jadvalini oylik partition'ga bo'lish bo'yicha spike qilaman. Isbot: 50 million qatorli test ma'lumotida oylik hisobot so'rovining latency farqini o'lchagan hujjat va qaror yozuvi." Natija ham o'lchanadi, ham ishga tegishli.

Har bir maqsadni joriy og'riqqa bog'lang. Agar eng og'ir incident'laringiz pool to'lishidan bo'lsa, chorak maqsadi connection pool bo'lsin, vector database emas.

Chorak oxirida ikki savol bering: uchta maqsaddan qanchasi isbotlangan natija bilan tugadi, va qaysi biri ishga ta'sir qildi. Birortasi ham tugamagan bo'lsa, muammo rejada emas, vaqt ajratishda.

## 38.13 Amalda qo'llash

- [ ] O'z stack'ingiz uchun "chuqur" va "yuzaki" ro'yxatini yozing: chuqur ro'yxatda 7 dan ko'p element bo'lmasin, va har biri uchun isbotlovchi test bor-yo'qligini belgilang.
- [ ] `mvn dependency:tree` va `mvn help:effective-pom` ni ishga tushirib, 50 dan ortiq jar keltirayotgan starter yoki kutubxonani toping, uning kerakligini PR muhokamasiga qo'ying.
- [ ] `.github/dependabot.yml` faylini guruhlar bilan sozlang, major yangilanishlarni `ignore` ga kiritib, haftada bir marta 30 daqiqalik "yangilash oynasi" ni kalendarga qo'ying.
- [ ] Eng ko'p ishlatiladigan uchta tashqi kutubxona uchun chiqish yo'lini tekshiring: vendor sinfi nechta faylda import qilinganini `grep` bilan sanab, 5 dan ko'p bo'lsa adapter kiritishni rejaga qo'ying.
- [ ] Keyingi spike'ni 3 kunlik vaqt chegarasi va bitta yozma savol bilan sprintga element qilib kiritib, natijani JMH yoki `pg_stat_statements` raqami bilan hujjatlashtiring.
- [ ] `docs/decisions/` papkasini yarating yoki tartibga soling, olti oydan oshgan qarorlarni skript bilan ro'yxat qilib, ulardan uchtasini bu chorakda qayta ko'rishga belgilang.
- [ ] Joriy LTS'dan keyingi JDK ni SDKMAN bilan o'rnatib, loyihani shu versiyada kompilyatsiya qiling, deprecated va native access ogohlantirishlarini issue sifatida yozib qo'ying.
- [ ] Chorak uchun uchta o'rganish maqsadini yozing, har biriga o'lchanadigan isbot va 12 soatlik budjet qo'yib, ularni joriy incident ro'yxatidagi og'riq bilan bog'lang.

---

[&larr; 37. Xarajat, SLO va biznes bilan muloqot](37-xarajat-slo-va-biznes-bilan-muloqot.md) · [Mundarija](README.md) · [39. Birinchi 90 kun va o'z-o'zini baholash &rarr;](39-birinchi-90-kun-va-oz-ozini-baholash.md)
