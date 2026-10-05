<!-- doc: code-review | chapter: 37 | part: VIII. Kesishgan sifat -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

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
mapper.enable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);   // standart yoqilgan!
// Agar sizning servisingiz javobga yangi maydon qo'shsa, shunday
// sozlangan mijoz sinadi - ya'ni "mos" o'zgarish ham breaking bo'ladi.

// Review tavsiyasi ikki tomonga:
// 1) Iste'molchi sifatida: noma'lum maydonlarga chidamli bo'lish.
spring.jackson.deserialization.fail-on-unknown-properties=false
// 2) Provayder sifatida: mijozlarning qattiqligini bilish va
//    yangi maydon qo'shishni ham e'lon qilish.
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
  <configuration>
    <oldVersion>
      <dependency>
        <groupId>${project.groupId}</groupId>
        <artifactId>${project.artifactId}</artifactId>
        <version>LATEST_RELEASE</version>
      </dependency>
    </oldVersion>
    <parameter>
      <onlyModified>true</onlyModified>
      <breakBuildOnBinaryIncompatibleModifications>true</breakBuildOnBinaryIncompatibleModifications>
      <includes><include>com.acme.api</include></includes>   <!-- faqat public API -->
    </parameter>
  </configuration>
</plugin>
```

## 37.6 Event va xabar sxemasi

Xabar sxemasi API dan ham qattiqroq: iste'molchilar mustaqil deploy qilinadi va eski xabarlar navbatda turgan bo'lishi mumkin.

| O'zgarish | Orqaga mos (eski iste'molchi yangi xabarni o'qiydi) | Oldinga mos (yangi iste'molchi eski xabarni o'qiydi) |
| --- | --- | --- |
| Standart qiymatli maydon qo'shish | Ha | Ha |
| Majburiy maydon qo'shish | Ha | Yo'q |
| Ixtiyoriy maydon olib tashlash | Yo'q (agar o'qilsa) | Ha |
| Maydon nomini o'zgartirish | Yo'q | Yo'q |
| Turni kengaytirish (`int` -> `long`) | Ehtimol | Yo'q |
| Enum qiymat qo'shish | Iste'molchiga bog'liq | Ha |

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

---

[&larr; 36. Test turi va integratsion test review](36-test-turi-va-integratsion-test-review.md) · [Mundarija](README.md) · [38. Performance review diffdan &rarr;](38-performance-review-diffdan.md)
