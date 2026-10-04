<!-- doc: clean-code | chapter: 29 | part: VIII. Spring va ma'lumot qatlamida toza kod -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 29. Log kodining tozaligi (Clean Logging Code)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [29.1 SLF4J parametrlangan xabar va satr birlashtirmaslik](#291-slf4j-parametrlangan-xabar-va-satr-birlashtirmaslik)
- [29.2 Daraja tanlash qoidalari](#292-daraja-tanlash-qoidalari)
- [29.3 Istisnoni oxirgi argument sifatida berish](#293-istisnoni-oxirgi-argument-sifatida-berish)
- [29.4 `e.getMessage()` bilan stack trace ni yo'qotish](#294-egetmessage-bilan-stack-trace-ni-yoqotish)
- [29.5 Bir hodisa, bitta log](#295-bir-hodisa-bitta-log)
- [29.6 Strukturali log va kalit nomlari](#296-strukturali-log-va-kalit-nomlari)
- [29.7 Korrelyatsiya identifikatori va MDC tozalash](#297-korrelyatsiya-identifikatori-va-mdc-tozalash)
- [29.8 Sezgir ma'lumot va maskalash](#298-sezgir-malumot-va-maskalash)
- [29.9 Log ni test bilan mahkamlash](#299-log-ni-test-bilan-mahkamlash)
- [29.10 Amalda qo'llash](#2910-amalda-qollash)

</details>


Kuzatuvchanlik amaliyoti va log narxi [arxitektor hujjatidagi](../architect/README.md) kuzatuvchanlik amaliyoti bo'limida, observability patternlari [patternlar hujjatidagi](../patterns/README.md) observability patternlari bo'limida. Bu bobda log **kodining** o'zi: xabar yozish shakli, daraja tanlash, istisno uzatish, takrorlanish va MDC.

## 29.1 SLF4J parametrlangan xabar va satr birlashtirmaslik

SLF4J da `{}` placeholder ikki foyda beradi: daraja o'chirilgan bo'lsa satr umuman qurilmaydi, va xabar shabloni log agregatorida guruhlanadi.

```java
// yomon: satr har doim qurilib keyin tashlanadi
log.debug("to'lov " + paymentId + " yopildi, summa: " + amount);

// yomon: toString() har doim chaqiriladi
log.debug("to'lov {}", expensiveObject.toString());

// yaxshi
log.debug("to'lov {} yopildi, summa: {}", paymentId, amount);

// yaxshi: qimmat hisob lazy supplier bilan (SLF4J 2.x fluent API)
log.atDebug().setMessage("holat: {}").addArgument(() -> expensiveSnapshot()).log();
```

`isDebugEnabled()` tekshiruvi parametrlangan xabar bilan **kerak emas** - u faqat argument hisoblash qimmat bo'lganda haqli.

## 29.2 Daraja tanlash qoidalari

Daraja noto'g'ri tanlansa, ikki muammo paydo bo'ladi: `ERROR` shovqinga aylanadi va hech kim ogohlantirishga qaramaydi, yoki haqiqiy xato `DEBUG` da yo'qoladi.

| Daraja | Qachon | Kim ko'radi |
|---|---|---|
| `ERROR` | odam aralashuvi kerak, SLO buzildi | alert, on-call |
| `WARN` | kutilmagan holat, lekin tizim ishlayapti | kundalik ko'rib chiqish |
| `INFO` | muhim biznes hodisasi, holat o'zgarishi | audit, tahlil |
| `DEBUG` | diagnostika uchun tafsilot | ishlab chiqish, incident |
| `TRACE` | juda batafsil, odatda o'chirilgan | chuqur diagnostika |

Amaliy sinov: `ERROR` yozilganda kimdir uyg'onishi kerakmi? Javob "yo'q" bo'lsa, u `WARN`. Validatsiya xatosi, topilmadi (404), biznes qoidasi buzildi - bular `ERROR` emas (27.3).

## 29.3 Istisnoni oxirgi argument sifatida berish

SLF4J istisnoni oxirgi argument sifatida qabul qiladi va stack trace ni to'liq yozadi. Istisnoni placeholder bilan uzatish stack trace ni yo'qotadi.

```java
// yomon: stack trace yo'q, faqat xabar
log.error("hisob-kitob xatosi: {}", e.getMessage());

// yomon: istisno placeholder ga tushdi, trace yo'qoldi
log.error("hisob-kitob xatosi: {}", e);

// yaxshi: kontekst placeholder da, istisno oxirgi argument
log.error("to'lov {} uchun hisob-kitob muvaffaqiyatsiz", paymentId, e);
```

## 29.4 `e.getMessage()` bilan stack trace ni yo'qotish

`e.getMessage()` eng ko'p uchraydigan diagnostika xatosi: `NullPointerException` uchun u ko'pincha `null` qaytaradi, va stack trace bo'lmasa xato qayerda bo'lganini aniqlash imkonsiz.

Qoida: log da istisno **obyekti** uzatiladi, xabari emas. Xabarni esa faqat foydalanuvchiga ko'rsatiladigan javobda ishlatish mumkin (19.10).

## 29.5 Bir hodisa, bitta log

Log takrorlanishi 19.7 da ko'rilgan muammoning amaliy natijasi: bitta xato har bir qatlamda log qilinsa, incident vaqtida bir xato uch-to'rt yozuv beradi va haqiqiy sabab shovqin ichida qoladi.

```java
// yomon: uch qatlam, uch log
// repository: log.error("SQL xatosi", e); throw ...
// service:    log.error("hisob-kitob xatosi", e); throw ...
// controller: log.error("so'rov xatosi", e); return 500

// yaxshi: kontekst har qatlamda qo'shiladi, log bir joyda
// repository: throw new SettlementStorageException("yozib bo'lmadi: " + id, e);
// service:    throw new SettlementFailedException(paymentId, e);
// controller advice: log.error("hisob-kitob muvaffaqiyatsiz: {}", paymentId, e);
```

## 29.6 Strukturali log va kalit nomlari

Agregatorda qidirish uchun log maydonlari strukturali bo'lishi kerak: matn ichidagi qiymatni qidirish emas, maydon bo'yicha filtrlash. Kalit nomlari esa izchil bo'lishi lozim (3.13).

```java
// yaxshi: strukturali maydonlar, matn ichida yashirin emas
log.atInfo()
        .addKeyValue("orderId", order.id())
        .addKeyValue("customerId", order.customerId())
        .addKeyValue("amount", order.total().amount())
        .addKeyValue("currency", order.total().currency())
        .setMessage("buyurtma tasdiqlandi")
        .log();
```

```xml
<!-- logback-spring.xml: production da JSON, mahalliy ishda o'qiladigan matn -->
<springProfile name="!local">
  <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
      <includeMdcKeyName>traceId</includeMdcKeyName>
      <includeMdcKeyName>spanId</includeMdcKeyName>
    </encoder>
  </appender>
</springProfile>
```

## 29.7 Korrelyatsiya identifikatori va MDC tozalash

Korrelyatsiya identifikatori (trace id) bo'lmasa, taqsimlangan tizimda bitta so'rovning yo'lini kuzatib bo'lmaydi. MDC uni har bir log yozuviga avtomatik qo'shadi, lekin uni **tozalash majburiy**: thread pool da thread qayta ishlatiladi va eski qiymat keyingi so'rovga o'tadi (16.9).

```java
// yaxshi: try/finally bilan kafolatlangan tozalash
@Component
class TraceIdFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        String traceId = Optional.ofNullable(request.getHeader("X-Trace-Id"))
                .orElseGet(() -> UUID.randomUUID().toString());
        MDC.put("traceId", traceId);
        try {
            response.setHeader("X-Trace-Id", traceId);
            chain.doFilter(request, response);
        } finally {
            MDC.clear();        // majburiy: thread qayta ishlatiladi
        }
    }
}
```

Asinxron kodda MDC avtomatik ko'chmaydi: `@Async` va `CompletableFuture` uchun kontekstni oshkor uzatish kerak (`MDC.getCopyOfContextMap()`).

## 29.8 Sezgir ma'lumot va maskalash

Sezgir ma'lumotni log ga yozish [patternlar hujjatida](../patterns/README.md) anti-pattern (25.47) va u ko'pincha `toString` orqali tasodifan sodir bo'ladi (15.7). Himoya ikki qatlamli bo'lishi kerak: turda maskalash va log konfiguratsiyasida filtr.

```java
// yaxshi: tur o'zi maskalaydi - tasodifan oqib ketmaydi
public record CardNumber(String value) {

    public CardNumber {
        if (!value.matches("\\d{13,19}")) throw new IllegalArgumentException("karta raqami");
    }

    public String last4() { return value.substring(value.length() - 4); }

    @Override
    public String toString() { return "****" + last4(); }     // log xavfsiz
}
```

Log ga hech qachon chiqmasligi kerak bo'lgan ma'lumotlar ro'yxati: parol, token, `Authorization` sarlavhasi, karta raqami va CVV, shaxsiy identifikator (JSHSHIR), tibbiy ma'lumot, to'liq so'rov tanasi (ichida yuqoridagilar bo'lishi mumkin).

## 29.9 Log ni test bilan mahkamlash

Muhim log yozuvlari (audit, xavfsizlik hodisasi) shartnomaning qismi bo'lsa, ular test bilan qotirilishi kerak - aks holda refaktoring paytida jim yo'qoladi.

```java
@Test
void logsAuditEventOnRefund() {
    ListAppender<ILoggingEvent> appender = attachAppender(RefundService.class);

    refunds.create(command, idempotencyKey);

    assertThat(appender.list)
            .anySatisfy(event -> {
                assertThat(event.getLevel()).isEqualTo(Level.INFO);
                assertThat(event.getKeyValuePairs())
                        .anySatisfy(kv -> assertThat(kv.key).isEqualTo("refundId"));
            });
}
```

Bu testni har bir log uchun yozish kerak emas - faqat audit va xavfsizlik yozuvlari uchun.

## 29.10 Amalda qo'llash

- [ ] Log xabarlarida satr birlashtirish (`+`) ishlatilgan joylarni `{}` placeholder ga o'tkazing.
- [ ] `log.error("...", e.getMessage())` namunalarini istisno obyektini uzatadigan shaklga tuzating.
- [ ] `ERROR` darajasidagi yozuvlarni ko'rib, odam aralashuvi kerak bo'lmaganlarini `WARN` ga tushiring.
- [ ] Bir xatoni bir necha qatlamda log qiladigan joylarni topib, log ni faqat chegarada qoldiring.
- [ ] Strukturali log ga o'tib, kalit nomlarini (`orderId`, `traceId`) izchil qiling.
- [ ] MDC ishlatilgan filtrlarda `finally` da `MDC.clear()` borligini tekshiring.
- [ ] Karta, parol va token turlariga maskalangan `toString` qo'shib, log filtrini sozlang.
- [ ] Audit va xavfsizlik log yozuvlarini test bilan mahkamlang.

---

[&larr; 28. JPA va SQL kodining tozaligi](28-jpa-va-sql-kodining-tozaligi.md) · [Mundarija](README.md) · [30. Test kodi ham ishlab chiqarish kodi &rarr;](30-test-kodi-ham-ishlab-chiqarish-kodi.md)
