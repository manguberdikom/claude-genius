<!-- doc: code-review | chapter: 37 | part: VIII. Kesishgan sifat -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 37. API moslik va breaking change review (API Compatibility)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [37.1 Breaking change katalogi](#371-breaking-change-katalogi)
- [37.2 Kim ishlatayotganini aniqlash](#372-kim-ishlatayotganini-aniqlash)
- [37.3 Versiyalash strategiyalari](#373-versiyalash-strategiyalari)
- [37.4 Deserializatsiya qattiqligi](#374-deserializatsiya-qattiqligi)
- [37.5 Ichki API: modullar orasidagi shartnoma](#375-ichki-api-modullar-orasidagi-shartnoma)
- [37.6 Event va xabar sxemasi](#376-event-va-xabar-sxemasi)
- [37.7 Deprecation jarayoni](#377-deprecation-jarayoni)
- [37.8 Review checklisti: API moslik](#378-review-checklisti-api-moslik)
- [37.9 Amalda qo'llash](#379-amalda-qollash)

</details>


API o'zgarishi diffda oddiy ko'rinadi: maydon nomi tuzatildi, tur aniqlashtirildi, ortiqcha maydon olib tashlandi. Lekin API ning narxi tashqarida: mobil ilovaning eski versiyasi, hamkor integratsiyasi, boshqa jamoaning servisi. Shu sababli API ga tegadigan PR da reviewer bitta narsani aniqlashi kerak - kim sinadi va qachon.

## 37.1 Breaking change katalogi

| O'zgarish | Breaking mi | Izoh |
| --- | --- | --- |
| Yangi ixtiyoriy maydon javobda | Yo'q | Qattiq deserializatsiya ishlatadigan mijoz sinishi mumkin |
| Yangi majburiy maydon so'rovda | Ha | Eski mijoz yubormaydi |
| Yangi ixtiyoriy maydon so'rovda | Yo'q | - |
| Maydon olib tashlash javobdan | Ha | Mijoz o'qiyotgan bo'lishi mumkin |
| Maydon nomini o'zgartirish | Ha | Ikkisi ham (olib tashlash + qo'shish) |
| Maydon turini o'zgartirish | Ha | `"1000"` va `1000` farqi |
| Maydonni nullable qilish | Ha | Mijoz null ni kutmaydi |
| Maydonni majburiy qilish | Ha | Eski so'rovlar rad etiladi |
| Enum ga yangi qiymat (javobda) | Ehtimol | Mijoz `switch` da `default` siz bo'lsa |
| `sealed` iyerarxiyaga yangi subklass | Ha | Chaqiruvchining `switch` i to'liq qamramaydi |
| Enum dan qiymat olib tashlash | Ha | - |
| Status kodini o'zgartirish | Ha | Mijoz mantiqi unga tayanadi |
| Xato javob shaklini o'zgartirish | Ha | Xato ishlash kodi sinadi |
| Validatsiyani qattiqlashtirish | Ha | Avval o'tgan so'rovlar rad etiladi |
| Validatsiyani yumshatish | Yo'q | - |
| Standart qiymatni o'zgartirish | Ha | Jim xulq o'zgarishi - eng xavfli |
| Tartiblashni o'zgartirish | Ehtimol | Mijoz tartibga tayanishi mumkin |
| Pagination standartini o'zgartirish | Ha | `size=20` dan `size=10` ga |
| Endpoint URL ini o'zgartirish | Ha | - |
| Rate limit qo'shish | Ehtimol | Yuqori yukli mijoz sinadi |
| Autentifikatsiya talabini qo'shish | Ha | - |

Eng xavfli qator - standart qiymatni o'zgartirish, chunki u hech qanday xato bermaydi: mijoz ishlaydi, lekin boshqa natija oladi.

Oxirgi ikki qatorning farqi muhim. Enum yoki `sealed` iyerarxiyaga
qiymat qo'shilganda buzilish jim bo'lmaydi: switch-expression hamma
qiymatni qamramasa, javac "the switch expression does not cover all
possible input values" degan XATO beradi, ogohlantirish emas. Ya'ni
chaqiruvchi kodi umuman kompilyatsiya qilinmaydi. Bu yaxshi xabar,
chunki muammo ishlab chiqarishda emas, build da chiqadi; lekin
chaqiruvchini qayta build qilmasdan kutubxonani ko'tarib qo'ysa,
eski bayt-kod `IncompatibleClassChangeError` yoki
`MatchException` bilan ish vaqtida yiqilishi mumkin.

## 37.2 Kim ishlatayotganini aniqlash

Review izohida "bu breaking change" deyish yetarli emas - kim sinishini bilish kerak.

```bash
# Endpoint dan kim foydalanayotganini aniqlash: dalil to'plash.
# 1) Access loglardan: User-Agent va versiya bo'yicha.
#    (ELK, Loki yoki CloudWatch da)
#    sum by (user_agent) (rate(http_requests_total{uri="/api/orders"}[7d]))

# 2) Mijoz versiyalari bo'yicha: agar header yuborilsa.
#    sum by (client_version) (rate(http_requests_total{uri=~"/api/orders.*"}[30d]))

# 3) Kod bazasida: boshqa servislar shu endpointni chaqiradimi.
#    (monorepo bo'lsa)
grep -rn '/api/orders' --include='*.java' --include='*.ts' --include='*.kt' .. | grep -v test

# 4) API gateway yoki service mesh statistikasi.
```

Review izohining shakli: "`total` maydonini satrdan raqamga o'zgartirish - breaking change. Oxirgi 30 kunda bu endpointni uch mijoz ishlatgan: mobil ilova 2.x (so'rovlarning 40 foizi), mobil 3.x (55 foizi) va hamkor integratsiyasi (5 foizi). Mobil 2.x yangilanmaydi - ya'ni foydalanuvchilarning 40 foizida buyurtma ekrani sinadi."

## 37.3 Versiyalash strategiyalari

| Strategiya | Qachon mos | Narxi |
| --- | --- | --- |
| Hech qanday versiyalash (faqat mos o'zgarishlar) | Ichki API, nazoratdagi mijozlar | Qattiq disiplina |
| URL versiyasi (`/v1/`, `/v2/`) | Ommaviy API | Ikki kod yo'li |
| Header versiyasi (`Accept: ...v2+json`) | Nozik versiyalash | Keshlash murakkabligi |
| Maydon darajasida evolyutsiya | Barcha holatlar | Eski maydonlarni saqlash |
| Yangi endpoint | Shakl tubdan o'zgarganda | Ikki endpoint |

```java
// Eng amaliy yondashuv: maydon darajasida evolyutsiya (expand and contract).
public record OrderResponse(
        UUID id,
        String number,
        @Deprecated(since = "2026-10", forRemoval = true)
        String total,                            // eski: satr
        BigDecimal totalAmount,                  // yangi: raqam
        String currency) {

    // Ikkisi ham to'ldiriladi: eski mijoz `total` ni, yangi
    // `totalAmount` ni o'qiydi. Olib tashlash sanasi e'lon qilinadi.
    public static OrderResponse from(Order o) {
        return new OrderResponse(o.id().value(), o.number().value(),
                                 o.total().amount().toPlainString(),
                                 o.total().amount(), o.total().currency().getCurrencyCode());
    }
}
// Review talabi: deprecation uchun sana, e'lon qilish yo'li va
// o'chirish shartlari (masalan "mobil 2.x foydalanuvchilari 1 foizdan
// kam bo'lganda") yozilishi kerak.
```

## 37.4 Deserializatsiya qattiqligi

```java
// Mijoz tomonda: qattiq deserializatsiya yangi maydonga sindiradi.
ObjectMapper mapper = new ObjectMapper();
// Jackson 2 (`com.fasterxml`) da bu feature standart YOQILGAN, ya'ni
// `new ObjectMapper()` noma'lum maydonga darhol sinadi. Jackson 3
// (`tools.jackson`) da esa standart O'CHIQ. Spring boshqaradigan
// mapper da ham o'chiq: Spring Framework uni ataylab o'chirib qo'yadi.
// Demak xavf asosan Spring tashqarisidagi, Jackson 2 dagi mijozda.
mapper.enable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
// Agar sizning servisingiz javobga yangi maydon qo'shsa, shunday
// sozlangan mijoz sinadi - ya'ni "mos" o'zgarish ham breaking bo'ladi.

// Review tavsiyasi ikki tomonga:
// 1) Iste'molchi sifatida: noma'lum maydonlarga chidamli bo'lish
//    (Spring Boot da spring.jackson.deserialization.fail-on-unknown-properties=false).
//    Spring boshqaradigan mapper da bu allaqachon shunday, shuning
//    uchun qatorni yozish faqat niyatni qayd qiladi.
// 2) Provayder sifatida: mijozlarning qattiqligini bilish va
//    yangi maydon qo'shishni ham e'lon qilish.
// 3) Mijoz qaysi Jackson da ekanini aniqlash: ikki versiyada standart
//    teskari, shuning uchun "bizda sinamaydi" degan dalil mijoz
//    versiyasini bilmasdan hech narsa isbotlamaydi.
```

## 37.5 Ichki API: modullar orasidagi shartnoma

```java
// Ichki modullar orasidagi shartnoma ham API: uning o'zgarishi
// boshqa jamoaning ishini to'xtatadi.
// Review savoli: bu metodni kim chaqiradi va u xabardor qilinganmi?

// Yordam: deprecation va kompilyatsiya ogohlantirishi.
@Deprecated(since = "2026-10", forRemoval = true)
public Money calculateTotal(Order order) {
    return calculateTotal(order, TaxContext.domestic());    // yangi shakl
}
// Foydasi: chaqiruvchilar kompilyatsiya paytida ogohlantirish oladi va
// migratsiya uchun vaqt bo'ladi.

// Katta loyihada: API moslikni avtomatik tekshirish.
// japicmp yoki revapi plugini mos kelmaydigan o'zgarishni build da tutadi.
```

```xml
<!-- japicmp: public API da breaking change ni build da tutish. -->
<plugin>
  <groupId>com.github.siom79.japicmp</groupId>
  <artifactId>japicmp-maven-plugin</artifactId>
  <version>0.26.3</version>
  <executions>
    <!-- Goal ni aniq bog'lash kerak: `cmp` ning default fazasi
         `verify` bo'lsa ham, execution yozilmasa Maven uni
         lifecycle ga qo'shmaydi va plugin jimgina ishlamaydi. -->
    <execution>
      <phase>verify</phase>
      <goals><goal>cmp</goal></goals>
    </execution>
  </executions>
  <configuration>
    <oldVersion>
      <dependency>
        <groupId>${project.groupId}</groupId>
        <artifactId>${project.artifactId}</artifactId>
        <!-- japicmp bu qiymatni o'zi talqin qilmaydi, to'g'ridan-to'g'ri
             Maven ga beradi. Maven esa faqat `RELEASE` va `LATEST`
             meta-versiyalarini taniydi, `LATEST_RELEASE` degan qiymat
             yo'q. Eng ishonchli yo'l aniq versiya: oldingi reliz
             raqamini property da saqlash. -->
        <version>${api.baseline.version}</version>
      </dependency>
    </oldVersion>
    <parameter>
      <onlyModified>true</onlyModified>
      <breakBuildOnBinaryIncompatibleModifications>true</breakBuildOnBinaryIncompatibleModifications>
      <!-- Binary moslik yetarli emas: overload qo'shilishi chaqiruvni
           noaniq qilishi mumkin, bu binary da emas, source da buzadi.
           Kutubxona chiqarayotgan bo'lsangiz ikkinchisini ham yoqing. -->
      <breakBuildOnSourceIncompatibleModifications>true</breakBuildOnSourceIncompatibleModifications>
      <includes><include>com.acme.api</include></includes>   <!-- faqat public API -->
    </parameter>
  </configuration>
</plugin>
```

## 37.6 Event va xabar sxemasi

Xabar sxemasi API dan ham qattiqroq: iste'molchilar mustaqil deploy qilinadi va eski xabarlar navbatda turgan bo'lishi mumkin.

Atamalarda bitta tuzoq bor va u jamoani soatlab chalg'itadi. Schema
registry da `BACKWARD` so'zi "eski iste'molchi yangi xabarni o'qiydi"
degani EMAS. Confluent ning ta'rifi teskari tomondan qaraydi: `BACKWARD`
yangi sxema oldingi sxema yozgan ma'lumotni o'qiy oladimi (ya'ni yangi
iste'molchi, eski xabar), `FORWARD` esa yangi sxema yozgan ma'lumotni
oldingi sxema o'qiy oladimi (eski iste'molchi, yangi xabar). Shuning
uchun jadvalda yo'nalish so'z bilan yoziladi, `backward` va `forward`
yorliqlari esa registry sozlamasi bo'lgani uchun alohida ustunda.

| O'zgarish | Yangi iste'molchi eski xabarni o'qiydi (registry: `BACKWARD`) | Eski iste'molchi yangi xabarni o'qiydi (registry: `FORWARD`) |
| --- | --- | --- |
| Standart qiymatli maydon qo'shish | Ha (o'quvchi default bilan to'ldiradi) | Ha (eski o'quvchi maydonni e'tiborsiz qoldiradi) |
| Majburiy maydon qo'shish | Yo'q | Ha |
| Ixtiyoriy maydon olib tashlash | Ha | Yo'q (agar o'qilsa) |
| Maydon nomini o'zgartirish | Faqat alias bilan | Faqat eski sxemada ham alias bo'lsa |
| `int` dan `long` ga kengaytirish | Ha (`int` `long` ga promotsiya qilinadi) | Yo'q (`long` ni `int` o'quvchi qabul qilmaydi) |
| Enum qiymat qo'shish | Ha | Iste'molchiga bog'liq |

Oxirgi ikki qator alohida izoh talab qiladi. Avro da tur promotsiyasi
bir tomonlama: `int` ni `long`, `float` yoki `double` sifatida o'qish
mumkin, `long` ni `int` sifatida esa yo'q. Shuning uchun maydonni
`int` dan `long` ga kengaytirish yangi o'quvchi uchun xavfsiz, eski
o'quvchi uchun esa buzadi, va ko'p jamoa buni teskari eslab qoladi.

Maydon nomini o'zgartirish ham "umuman mumkin emas" emas: Avro da
nomlangan turlar va maydonlar `aliases` olishi mumkin, va o'quvchi
sxemasidagi alias yozuvchi sxemasidagi eski nomga moslanadi. Ya'ni
yangi o'quvchi `aliases: ["oldName"]` bilan eski ma'lumotni o'qiy
oladi. Teskari yo'nalish uchun esa eski sxemaning o'zida ham alias
bo'lishi kerak edi, shuning uchun nomni "keyinchalik" o'zgartirish
amalda yangi maydon qo'shib eskisini deprecate qilishga teng.

```java
// Event sxemasini versiyalash: eng oddiy ishlaydigan shakl.
public record OrderPlacedV2(
        UUID orderId,
        Money total,
        @Nullable PromoCode promoCode,           // yangi, ixtiyoriy
        int schemaVersion) {                     // aniq versiya raqami

    public static final int VERSION = 2;
}
// Iste'molchi tomonda:
if (event.schemaVersion() > SUPPORTED_VERSION) {
    // Noma'lum versiya: DLQ ga yuborish yoki ogohlantirish bilan
    // mavjud maydonlar bo'yicha ishlash. Jim tashlab yuborish - xato.
    log.warn("qo'llab-quvvatlanmaydigan sxema versiyasi: {}", event.schemaVersion());
    meter.counter("event.unsupported.version").increment();
}
```

## 37.7 Deprecation jarayoni

```markdown
<!-- API o'zgarishi uchun PR shabloni bo'limi -->
## API o'zgarishi

- O'zgarish turi: [ ] mos  [ ] breaking  [ ] deprecation
- Ta'sirlangan endpointlar:
- Oxirgi 30 kundagi chaqiruvlar soni va mijozlar:
- Breaking bo'lsa:
  - [ ] Mijozlar xabardor qilingan (qayerda, qachon)
  - [ ] O'tish davri muddati:
  - [ ] Eski shakl saqlanadi (qancha vaqt):
  - [ ] Monitoring: eski shakl ishlatilishi o'lchanadi
- [ ] API hujjati (OpenAPI) yangilangan
- [ ] CHANGELOG ga yozilgan
```

```java
// Eski maydon ishlatilishini o'lchash: o'chirish qarori uchun dalil.
// Agar mijoz eski maydonni o'qiyotganini bilib bo'lmasa, uning
// ishlatilishini so'rov darajasida o'lchash mumkin:
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id,
                         @RequestHeader(value = "X-Client-Version", required = false) String clientVersion) {
    meter.counter("api.orders.get", "client", clientVersion == null ? "unknown" : clientVersion)
         .increment();
    return ...;
}
// Yoki eski endpoint uchun alohida hisoblagich: o'chirish vaqtini
// raqam bilan asoslash imkonini beradi.
```

## 37.8 Review checklisti: API moslik

| Savol | Nega |
| --- | --- |
| Bu o'zgarish breaking katalogida bormi | Jim sinish |
| Kim ishlatadi va qancha trafik | Ta'sir hajmi |
| Standart qiymat o'zgardimi | Xatosiz xulq o'zgarishi |
| Validatsiya qattiqlashdimi | Avval o'tgan so'rovlar |
| Enum ga yangi qiymat qo'shildimi | Mijoz `switch` i |
| `sealed` iyerarxiyaga subklass qo'shildimi | Chaqiruvchining `switch` i, kompilyatsiya xatosi |
| Xato javob shakli o'zgardimi | Mijoz xato ishlash kodi |
| Deprecation sanasi va rejasi bormi | Abadiy ikki shakl |
| OpenAPI hujjati yangilandimi | Mijoz noto'g'ri ma'lumot oladi |
| Event sxemasi ikki tomonga mosmi | Iste'molchi sinishi |
| Eski shakl ishlatilishi o'lchanadimi | O'chirish qarori |
| Mijozlar xabardor qilindimi | Kutilmagan uzilish |

## 37.9 Amalda qo'llash

- [ ] Breaking change katalogini `REVIEW.md` ga qo'shib, API ga tegadigan PR larda uni tekshirishni majburiy qiling.
- [ ] PR shablonida API o'zgarishi bo'limini qo'shing (o'zgarish turi, mijozlar, o'tish davri).
- [ ] Asosiy endpointlar uchun mijoz versiyasi bo'yicha trafik metrikasini qo'shing.
- [ ] `spring.jackson.deserialization.fail-on-unknown-properties=false` ni iste'molchi tomonda tekshiring.
- [ ] Public API modullari uchun japicmp yoki revapi ni build ga qo'shing.
- [ ] Event sxemalariga aniq versiya maydonini kiritib, iste'molchida noma'lum versiya uchun xulq belgilang.
- [ ] Deprecated maydon va endpointlar ro'yxatini o'chirish sanasi bilan yuritib boring.
- [ ] API javob shakllari uchun snapshot testlarini qo'shib (36.5), tasodifiy o'zgarishlarni tuting.

## Manbalar

- Apache Avro, *Specification* (Schema Resolution va Aliases)
  ([https://github.com/apache/avro/blob/release-1.12.2/doc/content/en/docs/++version++/Specification/_index.md](https://github.com/apache/avro/blob/release-1.12.2/doc/content/en/docs/++version++/Specification/_index.md),
  tag `release-1.12.2`, Apache-2.0) - 37.6 dagi tur promotsiyasi
  (`int` dan `long` ga, teskarisi emas), default bilan to'ldirish va
  `aliases` orqali nom o'zgartirish.
- Confluent Schema Registry, `CompatibilityChecker`
  ([https://github.com/confluentinc/schema-registry/blob/v8.5.0-335/client/src/main/java/io/confluent/kafka/schemaregistry/CompatibilityChecker.java](https://github.com/confluentinc/schema-registry/blob/v8.5.0-335/client/src/main/java/io/confluent/kafka/schemaregistry/CompatibilityChecker.java),
  tag `v8.5.0-335`, fayl Apache-2.0) - 37.6 dagi `BACKWARD` va
  `FORWARD` yorliqlarining aniq ma'nosi.
- japicmp, `ConfigParameters`, `JApiCmpMojo` va README
  ([https://github.com/siom79/japicmp/tree/japicmp-base-0.26.3/japicmp-maven-plugin](https://github.com/siom79/japicmp/tree/japicmp-base-0.26.3/japicmp-maven-plugin),
  tag `japicmp-base-0.26.3`, Apache-2.0) - 37.5 dagi plugin
  parametrlari, `executions` zarurati va source moslik bayrog'i.
- Maven Resolver, `VersionResolver`
  ([https://github.com/apache/maven-resolver/blob/maven-resolver-2.0.24/maven-resolver-impl/src/main/java/org/eclipse/aether/impl/VersionResolver.java](https://github.com/apache/maven-resolver/blob/maven-resolver-2.0.24/maven-resolver-impl/src/main/java/org/eclipse/aether/impl/VersionResolver.java),
  tag `maven-resolver-2.0.24`, Apache-2.0) - 37.5 dagi meta-versiyalar
  ro'yxati: faqat `RELEASE` va `LATEST`.
- Jackson Databind, `DeserializationFeature`
  ([https://github.com/FasterXML/jackson-databind/blob/jackson-databind-2.22.3/src/main/java/com/fasterxml/jackson/databind/DeserializationFeature.java](https://github.com/FasterXML/jackson-databind/blob/jackson-databind-2.22.3/src/main/java/com/fasterxml/jackson/databind/DeserializationFeature.java),
  tag `jackson-databind-2.22.3` va
  [3.2.3 dagi `tools.jackson` varianti](https://github.com/FasterXML/jackson-databind/blob/jackson-databind-3.2.3/src/main/java/tools/jackson/databind/DeserializationFeature.java),
  Apache-2.0) - 37.4 dagi `FAIL_ON_UNKNOWN_PROPERTIES` standart
  qiymatining Jackson 2 va 3 da teskari bo'lishi.
- Spring Framework, `Jackson2ObjectMapperBuilder`
  ([https://github.com/spring-projects/spring-framework/blob/v7.0.9/spring-web/src/main/java/org/springframework/http/converter/json/Jackson2ObjectMapperBuilder.java](https://github.com/spring-projects/spring-framework/blob/v7.0.9/spring-web/src/main/java/org/springframework/http/converter/json/Jackson2ObjectMapperBuilder.java),
  tag `v7.0.9`, Apache-2.0) - 37.4 dagi Spring boshqaradigan mapper da
  feature ning ataylab o'chirilishi.
- OpenJDK, `Deprecated`, `Lint` va `Flow`
  ([https://github.com/openjdk/jdk/blob/jdk-28+9/src/jdk.compiler/share/classes/com/sun/tools/javac/comp/Flow.java](https://github.com/openjdk/jdk/blob/jdk-28+9/src/jdk.compiler/share/classes/com/sun/tools/javac/comp/Flow.java),
  tag `jdk-28+9`, GPLv2 + Classpath istisnosi) - 37.1 va 37.8 dagi
  to'liq qamramagan `switch` uchun kompilyatsiya xatosi, va 37.5 dagi
  `forRemoval = true` ogohlantirishining standart yoqilganligi.

---

[&larr; 36. Test turi va integratsion test review](36-test-turi-va-integratsion-test-review.md) · [Mundarija](README.md) · [38. Performance review diffdan &rarr;](38-performance-review-diffdan.md)
