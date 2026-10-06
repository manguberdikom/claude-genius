<!-- doc: patterns | chapter: 16 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 16. Enterprise Integration Patterns II: transformatsiya, endpointlar, boshqaruv, event patternlar (EIP II: Transformation, Endpoints, System Management, Event Patterns)

<details>
<summary>Bu bobdagi 45 bo'lim</summary>

- [16.1 Konvert O'ramchisi (Envelope Wrapper)](#161-konvert-oramchisi-envelope-wrapper)
- [16.2 Mazmun Boyituvchi (Content Enricher)](#162-mazmun-boyituvchi-content-enricher)
- [16.3 Mazmun Filtri (Content Filter)](#163-mazmun-filtri-content-filter)
- [16.4 Yuk Kvitansiyasi (Claim Check)](#164-yuk-kvitansiyasi-claim-check)
- [16.5 Normalizator (Normalizer)](#165-normalizator-normalizer)
- [16.6 Kanonik Ma'lumot Modeli (Canonical Data Model)](#166-kanonik-malumot-modeli-canonical-data-model)
- [16.7 Messaging Shlyuzi (Messaging Gateway)](#167-messaging-shlyuzi-messaging-gateway)
- [16.8 Messaging Mapperi (Messaging Mapper)](#168-messaging-mapperi-messaging-mapper)
- [16.9 Tranzaksion Mijoz (Transactional Client)](#169-tranzaksion-mijoz-transactional-client)
- [16.10 So'rovchi Iste'molchi (Polling Consumer)](#1610-sorovchi-istemolchi-polling-consumer)
- [16.11 Hodisaga Asoslangan Iste'molchi (Event-Driven Consumer)](#1611-hodisaga-asoslangan-istemolchi-event-driven-consumer)
- [16.12 Raqobatlashuvchi Iste'molchilar (Competing Consumers)](#1612-raqobatlashuvchi-istemolchilar-competing-consumers)
- [16.13 Xabar Dispetcheri (Message Dispatcher)](#1613-xabar-dispetcheri-message-dispatcher)
- [16.14 Tanlab qabul qiluvchi (Selective Consumer)](#1614-tanlab-qabul-qiluvchi-selective-consumer)
- [16.15 Ishonchli obunachi (Durable Subscriber)](#1615-ishonchli-obunachi-durable-subscriber)
- [16.16 Idempotent qabul qiluvchi (Idempotent Receiver)](#1616-idempotent-qabul-qiluvchi-idempotent-receiver)
- [16.17 Service Activator (Service Activator)](#1617-service-activator-service-activator)
- [16.18 Boshqaruv shinasi (Control Bus)](#1618-boshqaruv-shinasi-control-bus)
- [16.19 Chetlab o'tish yo'li (Detour)](#1619-chetlab-otish-yoli-detour)
- [16.20 Sim ulanishi (Wire Tap)](#1620-sim-ulanishi-wire-tap)
- [16.21 Xabar tarixi (Message History)](#1621-xabar-tarixi-message-history)
- [16.22 Xabar ombori (Message Store)](#1622-xabar-ombori-message-store)
- [16.23 Aqlli proxy (Smart Proxy)](#1623-aqlli-proxy-smart-proxy)
- [16.24 Test xabari (Test Message)](#1624-test-xabari-test-message)
- [16.25 Kanal tozalovchi (Channel Purger)](#1625-kanal-tozalovchi-channel-purger)
- [16.26 Hodisa xabarnomasi (Event Notification)](#1626-hodisa-xabarnomasi-event-notification)
- [16.27 Holat ko'chiruvchi event (Event-Carried State Transfer)](#1627-holat-kochiruvchi-event-event-carried-state-transfer)
- [16.28 Event Sourcing (messaging nuqtai nazaridan) (Event Sourcing (messaging view))](#1628-event-sourcing-messaging-nuqtai-nazaridan-event-sourcing-messaging-view)
- [16.29 CloudEvents (CloudEvents)](#1629-cloudevents-cloudevents)
- [16.30 Kafka Consumer Group (Kafka: Consumer Group)](#1630-kafka-consumer-group-kafka-consumer-group)
- [16.31 Partition kaliti bo'yicha tartib (Kafka: Partition key ordering)](#1631-partition-kaliti-boyicha-tartib-kafka-partition-key-ordering)
- [16.32 Compacted topic (Kafka: Compacted topic)](#1632-compacted-topic-kafka-compacted-topic)
- [16.33 Exactly-once va tranzaksion producer (Kafka: Exactly-once / transactional producer)](#1633-exactly-once-va-tranzaksion-producer-kafka-exactly-once--transactional-producer)
- [16.34 Schema Registry va schema evolyutsiyasi (Schema Registry & schema evolution)](#1634-schema-registry-va-schema-evolyutsiyasi-schema-registry--schema-evolution)
- [16.35 Retry topic va Dead Letter Topic (Retry topic / Dead Letter Topic (Spring Kafka))](#1635-retry-topic-va-dead-letter-topic-retry-topic--dead-letter-topic-spring-kafka)
- [16.36 Spring Integration DSL moslashuvi (Spring Integration DSL mapping)](#1636-spring-integration-dsl-moslashuvi-spring-integration-dsl-mapping)
- [16.37 Spring Cloud Stream binder abstraksiyasi (Spring Cloud Stream binder abstraction)](#1637-spring-cloud-stream-binder-abstraksiyasi-spring-cloud-stream-binder-abstraction)
- [16.38 JMS va AMQP moslashuvi (JMS / AMQP mapping (Spring JMS, Spring AMQP))](#1638-jms-va-amqp-moslashuvi-jms--amqp-mapping-spring-jms-spring-amqp)
- [16.39 Log siqilishi (Log Compaction)](#1639-log-siqilishi-log-compaction)
- [16.40 Aynan-bir-marta semantikasi (Exactly-Once Semantics)](#1640-aynan-bir-marta-semantikasi-exactly-once-semantics)
- [16.41 Stream-jadval birlashtirish (Stream-Table Join)](#1641-stream-jadval-birlashtirish-stream-table-join)
- [16.42 Oynalash (Windowing)](#1642-oynalash-windowing)
- [16.43 Event vaqti va ishlov vaqti (Event Time vs Processing Time)](#1643-event-vaqti-va-ishlov-vaqti-event-time-vs-processing-time)
- [16.44 Watermark (Watermark)](#1644-watermark-watermark)
- [16.45 Amalda qo'llash](#1645-amalda-qollash)

</details>



Enterprise Integration Patterns'ning ikkinchi katta guruhi xabarni *yo'naltirish*dan ko'ra uning *mazmuni* va *chegaralari* bilan ishlaydi: payload'ni bir modeldan boshqasiga o'tkazish (transformatsiya), ilovani messaging infratuzilmasiga ulovchi endpointlarni qurish, tranzaksiya va iste'mol rejimini boshqarish hamda hodisalarni ko'p iste'molchi o'rtasida taqsimlash. Arxitektor uchun bu patternlar aynan o'sha joyda yashaydi, qaerda integratsiya loyihalari ko'pincha qulaydi - sxema versiyalanishi, katta payloadlar, "exactly-once" illyuziyasi, iste'molchi parallelligi va xabar tartibi. Spring ekotizimida bu patternlarning deyarli har biri tayyor abstraksiya sifatida mavjud (Spring Integration, Spring Messaging, Spring for Apache Kafka, Spring AMQP, Spring JMS), shuning uchun asosiy ish - ularni noldan yozish emas, balki to'g'ri tanlash va to'g'ri sozlash. Quyida har bir pattern uchun Spring'dagi aniq joylashuvi, real keyslari va amaliy tuzoqlari keltirilgan.

## 16.1 Konvert O'ramchisi (Envelope Wrapper)

**Tavsif:** Domen payload'ini metama'lumot (marshrut, korrelyatsiya ID, versiya, xavfsizlik konteksti) bilan birga "konvert" ichiga o'rab yuboradi, shunda infratuzilma payload'ni ochmasdan qaror qabul qila oladi. Qabul qiluvchi tomonda konvert ochiladi (unwrap) va faqat sof domen obyekti biznes logikaga uzatiladi. Bu transport talablari bilan domen modelini bir-biridan ajratadi. Natijada bir xil payload turli kanallar orqali turli metama'lumot bilan harakatlana oladi.

**Spring'da qayerda uchraydi:** Spring Messaging'ning `org.springframework.messaging.Message<T>` abstraksiyasi aynan shu pattern: `getPayload()` + `MessageHeaders`. Konvert `MessageBuilder.withPayload(x).setHeader(...).setCorrelationId(...)` bilan quriladi; transport darajasida `JmsHeaderMapper`/`DefaultJmsHeaderMapper`, `AmqpHeaderMapper`, Kafka `KafkaHeaderMapper`/`DefaultKafkaHeaderMapper` headerlarni mahalliy protokol headerlariga map qiladi. Iste'molchida `@Payload`, `@Header`, `@Headers` argument resolverlari konvertni avtomatik ochadi. Standartlashtirilgan konvert kerak bo'lsa CloudEvents (`io.cloudevents:cloudevents-spring`) Spring Integration va WebFlux bilan integratsiyalashadi; Spring Cloud Stream esa `spring.cloud.stream` binderlari orqali o'z headerlarini qo'shadi.

**Qo'llanish keyslari:**
- Distributed tracing uchun `traceparent`/`b3` headerlarini xabar bilan birga tashish (Micrometer Tracing).
- Sxema versiyasini (`contentType`, `schemaVersion`) headerga qo'yib, iste'molchini to'g'ri deserializerga yo'naltirish.
- Multi-tenant tizimda `tenantId`ni konvertda tashib, biznes payload'ini o'zgartirmaslik.
- Retry/DLQ metama'lumotlarini (`x-death`, `retryCount`) payload'ga tegmasdan saqlash.
- Idempotentlik uchun `messageId` va `correlationId`ni konvert darajasida majburiy qilish.

**Ehtiyot bo'ling:** Headerlarga katta yoki maxfiy ma'lumot solish - headerlar ko'pincha loglanadi, broker chegarasi bor (Kafka header hajmi, AMQP frame limiti) va serializatsiyada yo'qolishi mumkin. Shuningdek konvertni biznes logika ichida ochib ishlatish domen kodini transportga bog'lab qo'yadi.

## 16.2 Mazmun Boyituvchi (Content Enricher)

**Tavsif:** Kelgan xabarda qabul qiluvchi uchun yetarli ma'lumot bo'lmaganda, pattern tashqi manbaga (DB, REST servis, boshqa kanal) murojaat qilib payload'ni qo'shimcha maydonlar bilan to'ldiradi. Shu bilan yuboruvchi minimal, barqaror xabar yuboradi, kontekst esa integratsiya qatlamida qo'shiladi. Boyitish sinxron (request-reply) yoki lokal lookup orqali bo'lishi mumkin.

**Spring'da qayerda uchraydi:** Spring Integration'da `org.springframework.integration.transformer.ContentEnricher` (XML'da `<int:enricher>`, DSL'da `.enrich(e -> e.requestChannel("lookupChannel").propertyExpression("customer", "payload"))`) va header darajasida `HeaderEnricher` / `.enrichHeaders(h -> h.header("region", "EU"))`. Lookup uchun odatda `RestClient`/`WebClient` yoki `JdbcTemplate` chaqiriladi, natija `SpEL` expression bilan payload'ga joylanadi. Kafka Streams bilan ishlaganda boyitish `KStream.join(KTable, ...)` (`spring-kafka` + `KafkaStreamsConfiguration`) orqali amalga oshiriladi; mikroservislarda esa `@ServiceActivator` metodida oddiy mapper + repository chaqirig'i ham shu patternning sodda shakli.

**Qo'llanish keyslari:**
- Buyurtma xabariga mijozning hozirgi manzili va chegirma darajasini DB'dan qo'shib yuborish.
- IoT sensor hodisasiga qurilma metama'lumotlarini (model, joylashuv) boyitish.
- To'lov hodisasiga valyuta kursini tashqi servisdan olib qo'shish.
- Audit xabariga foydalanuvchi roli va bo'limini identity servisdan boyitish.
- Kafka Streams'da yengil hodisani `KTable` bilan join qilib to'liq view yasash.

**Ehtiyot bo'ling:** Boyitish sinxron tashqi chaqiriqqa aylansa, butun oqim o'sha servisning latency va availability'siga bog'lanib qoladi - timeout, circuit breaker (Resilience4j) va cache shart. Juda ko'p boyitish esa "distributed join" ga olib keladi; bunda ma'lumotni iste'molchi tomoni o'zi egallashi (local projection) ko'pincha to'g'riroq.

## 16.3 Mazmun Filtri (Content Filter)

**Tavsif:** Xabardan keraksiz yoki ruxsat etilmagan maydonlarni olib tashlab, payload'ni soddalashtiradi yoki kichraytiradi. Content Enricher'ning teskarisi: bu yerda maqsad - iste'molchiga faqat kerakli minimal ma'lumotni berish. Bu ham xavfsizlik (PII), ham hajm/performance vositasi.

**Spring'da qayerda uchraydi:** Spring Integration'da `.transform()` bilan DTO proyeksiyasi yoki `HeaderFilter` (`.headerFilter("internalToken", "debugInfo")`). REST qatlamida Jackson'ning `@JsonIgnore`, `@JsonView` + `@JsonView` controller metodida, hamda `MappingJacksonValue` + `@JsonFilter`/`SimpleFilterProvider` dinamik filtrlash beradi. Spring Data REST'da `@Projection` interfeyslari, Spring GraphQL'da (`spring-boot-starter-graphql`) mijoz so'ragan maydonlar tanlanishi aynan shu pattern. Loglardan maxfiy maydonni chiqarib tashlash uchun Actuator `Sanitizer` va `@JsonIgnore` kombinatsiyasi ishlatiladi.

**Qo'llanish keyslari:**
- Tashqi hamkorga yuborilayotgan xabardan PII (pasport, karta raqami) maydonlarini olib tashlash.
- Mobil mijozga og'ir obyektning faqat 5 maydonli yengil proyeksiyasini qaytarish.
- Ichki xizmat headerlari (`internal-trace`, `debug`) tashqi chegaradan o'tmasligini kafolatlash.
- Analytics topicga faqat agregatsiya uchun kerakli maydonlarni yuborish.
- Bitta canonical hodisadan rolga qarab turli "ko'rinish"lar yasash.

**Ehtiyot bo'ling:** Filtrlashni faqat serializatsiya annotatsiyalariga tayanib qilish xatarli - bitta yangi maydon qo'shilsa, u avtomatik "oqib" ketishi mumkin; shuning uchun tashqi chegara uchun alohida explicit DTO afzal. Shuningdek filtrlangan maydonni keyin kimdir talab qilsa, sxema evolyutsiyasi og'irlashadi.

## 16.4 Yuk Kvitansiyasi (Claim Check)

**Tavsif:** Katta payload broker orqali tashilmaydi; u tashqi omborga (DB, S3, fayl tizimi) saqlanadi va xabarda faqat kalit ("kvitansiya") yuboriladi. Kerakli joyda kvitansiya bo'yicha payload qaytarib olinadi. Bu broker yukini, latency va xotira sarfini keskin kamaytiradi, bir vaqtda maxfiy ma'lumotni kanaldan olib tashlaydi.

**Spring'da qayerda uchraydi:** Spring Integration'da to'g'ridan-to'g'ri `ClaimCheckInTransformer` va `ClaimCheckOutTransformer`, `MessageStore` implementatsiyalari bilan: `SimpleMessageStore`, `JdbcMessageStore`, `RedisMessageStore`, `MongoDbMessageStore`. Java DSL: `.claimCheckIn(messageStore)` / `.claimCheckOut(messageStore)`. Kafka'da ko'pincha qo'lda variant ishlatiladi: fayl S3'ga `S3Template`/AWS SDK bilan yoziladi, topicga esa `objectKey` yuboriladi (Spring Cloud AWS). Fayl integratsiyasida `FileReadingMessageSource` + `FileToByteArrayTransformer`ni almashtirib, faqat `File` referensini uzatish ham shu yondashuv.

```java
@Bean
IntegrationFlow bigPayloadFlow(MessageStore store) {
    return IntegrationFlow.from("inbound")
            .claimCheckIn(store)
            .channel("kafkaOut")
            .get();
}
```

**Qo'llanish keyslari:**
- Skanerlangan hujjat yoki video faylni S3'ga qo'yib, topicga faqat kalitini yuborish.
- 50 MB'li XML to'lov faylini DB'ga saqlab, oqimda faqat `batchId` tashish.
- Maxfiy payload'ni shifrlangan omborda saqlab, brokerda faqat referens qoldirish.
- Uzoq muddatli saga oqimida og'ir kontekstni har qadamda qayta uzatmaslik.
- Kafka'ning 1 MB `max.request.size` chegarasini oshirmasdan katta hujjatlar bilan ishlash.

**Ehtiyot bo'ling:** Endi xabar va ombor o'rtasida izchillik muammosi paydo bo'ladi - iste'molchi xabarni olib, obyektni topmasligi (yoki TTL tugab ketishi) mumkin; shuning uchun omborga yozish xabar yuborishdan oldin bo'lishi va tozalash (retention) siyosati aniq bo'lishi kerak. Kichik payloadlar uchun bu pattern ortiqcha murakkablik.

## 16.5 Normalizator (Normalizer)

**Tavsif:** Semantik jihatdan bir xil, lekin formati turlicha bo'lgan xabarlarni (XML, CSV, turli JSON sxemalar) bitta umumiy ichki formatga keltiradi. Odatda avval xabar turi aniqlanadi, so'ng har bir tur uchun maxsus transformator ishlaydi va natija bitta kanalga tushadi. Shu bilan ichki logika manba xilma-xilligidan xabardor bo'lmaydi.

**Spring'da qayerda uchraydi:** Spring Integration'da `PayloadTypeRouter` yoki `HeaderValueRouter` xabarni tur bo'yicha ajratadi, har bir tarmoqda o'z `@Transformer`/`.transform()` bo'ladi va hammasi umumiy canonical kanalga yig'iladi. Format-maxsus parserlar uchun `spring-integration-xml` (`UnmarshallingTransformer`, `XsltPayloadTransformer`), Jackson converterlari, `spring-batch`'ning `DelimitedLineTokenizer`/`FlatFileItemReader` ishlatiladi. Obyekt-obyekt map qilishda `ConversionService` + `Converter<S, T>` bean'lari yoki MapStruct generatsiyasi standart yechim; Kafka'da `ErrorHandlingDeserializer` bilan birga `DelegatingByTopicDeserializer`/`DelegatingDeserializer` turli topiclar uchun turli deserializerni tanlaydi.

**Qo'llanish keyslari:**
- Uch xil bank formatidagi (SWIFT MT, ISO 20022 XML, CSV) to'lov faylini bitta `PaymentEvent`ga keltirish.
- Hamkor API'larining turli JSON sxemalarini bitta ichki `Order` modeliga map qilish.
- Legacy fixed-width fayl va yangi JSON API'ni bir xil pipeline'da qayta ishlash.
- Turli IoT vendorlarining telemetriyasini bitta o'lchov modeliga normalizatsiya qilish.
- Migratsiya davrida v1 va v2 hodisalarni bitta iste'molchiga yetkazish.

**Ehtiyot bo'ling:** Har bir yangi manba uchun yangi tarmoq qo'shilishi normalizator ichida "if-else do'zaxi"ga aylanib ketishi mumkin - turni aniqlash qoidalari deklarativ va testlangan bo'lishi kerak. Yana bir xato: normalizatsiya paytida ma'lumotni "o'rtalashtirib", manbaga xos muhim maydonlarni yo'qotib qo'yish.

## 16.6 Kanonik Ma'lumot Modeli (Canonical Data Model)

**Tavsif:** Tizimlar bir-biriga to'g'ridan-to'g'ri o'z ichki modeli bilan bog'lanmasligi uchun integratsiya chegarasida umumiy, neytral model belgilanadi. Har bir ilova faqat o'zining modeli bilan canonical model orasidagi map'ni saqlaydi, natijada N×N o'rniga N ta map paydo bo'ladi. Bu integratsiya bog'liqliklarini keskin kamaytiradi.

**Spring'da qayerda uchraydi:** Amalda bu alohida versiyalangan "contract" moduli bo'ladi: Maven/Gradle'da `order-events-api` artifacti, ichida DTO/record'lar yoki Avro/Protobuf sxemalari. Sxema boshqaruvi uchun `spring-cloud-schema-registry-client` va Confluent `KafkaAvroSerializer`/`spring-kafka` konfiguratsiyasi, REST uchun OpenAPI spetsifikatsiyasi va `springdoc-openapi` ishlatiladi. Kontraktni test bilan muhrlash uchun Spring Cloud Contract (`spring-cloud-starter-contract-verifier`) mavjud; Spring Cloud Stream'da esa `spring.cloud.stream.bindings.*.content-type` va `MessageConverter`lar canonical formatni majburlaydi.

**Qo'llanish keyslari:**
- Bir nechta mikroservis o'qiydigan `CustomerChanged` hodisasi uchun umumiy Avro sxemasini e'lon qilish.
- Legacy ERP va yangi platformani canonical `Invoice` modeli orqali ulash.
- Hamkorlar bilan ISO/sanoat standartidagi (ISO 20022, FHIR) modelni qabul qilish.
- Bir nechta jamoada DTO moduli orqali backward-compatible sxema evolyutsiyasini boshqarish.
- Yangi iste'molchi qo'shilganda faqat bitta mapper yozish bilan cheklanish.

**Ehtiyot bo'ling:** Canonical model "hamma narsani qamrab oluvchi" gigant modelga aylansa, u har bir o'zgarishda barcha jamoani bloklaydigan taqsimlangan monolitga aylanadi - uni domen chegaralari bo'yicha bir nechta kichik kontraktga bo'lish afzal. Shuningdek canonical modelni ichki domen modeli sifatida qayta ishlatish (DDD'dagi shared kernel) ko'pincha xato.

## 16.7 Messaging Shlyuzi (Messaging Gateway)

**Tavsif:** Ilova kodini messaging API'sidan to'liq ajratadi: biznes kod oddiy Java interfeysini chaqiradi, pattern uni xabarga aylantirib kanalga yuboradi va kerak bo'lsa javobni qaytaradi. Shu tufayli domen qatlamida `Message`, `Channel`, `JmsTemplate` kabi tushunchalar ko'rinmaydi. Natijada transportni almashtirish biznes kodga tegmasdan amalga oshadi.

**Spring'da qayerda uchraydi:** `@MessagingGateway` annotatsiyasi (`org.springframework.integration.annotation.MessagingGateway`) va uning ostidagi `GatewayProxyFactoryBean` interfeys uchun proxy yaratadi; `@Gateway(requestChannel = "...", replyTimeout = ...)` metod darajasida sozlanadi. Java DSL'da `IntegrationFlow.from(MyGateway.class)` yoki `.gateway("someChannel")` ishlatiladi. Quyi darajada `MessagingTemplate`, `MessagingGatewaySupport`, hamda transport-maxsus template'lar: `JmsTemplate`, `RabbitTemplate`, `KafkaTemplate`. Interfeys metodi `CompletableFuture`, `Mono` yoki `void` qaytarishi mumkin.

```java
@MessagingGateway(defaultRequestChannel = "orders.in")
public interface OrderGateway {
    @Gateway(replyTimeout = 2000)
    OrderAck submit(@Payload OrderDto order, @Header("tenant") String tenant);
}
```

**Qo'llanish keyslari:**
- Domen servisidan Kafka'ga hodisa yuborishni interfeys chaqirig'iga aylantirish.
- Testlarda gateway interfeysini mock qilib, broker'ni ko'tarmasdan unit test yozish.
- JMS'dan Kafka'ga migratsiyada biznes kodni o'zgartirmaslik.
- Sinxron request-reply integratsiyani (`replyChannel`) oddiy metod sifatida ko'rsatish.
- Legacy koddan messaging oqimiga kirish nuqtasini bitta joyga markazlashtirish.

**Ehtiyot bo'ling:** Sinxron gateway metodi `replyTimeout` bilan bloklanadi - javob kelmasa thread pool tez to'lib qoladi, shuning uchun timeout va asinxron qaytarish turlarini ongli tanlash kerak. Gateway interfeysini juda "chatty" qilib, har bir maydon uchun alohida metod yasash esa messaging afzalligini yo'qotadi.

## 16.8 Messaging Mapperi (Messaging Mapper)

**Tavsif:** Domen obyektlari va xabar formati o'rtasidagi konvertatsiyani alohida komponentga chiqaradi, shunda na domen model messaging haqida biladi, na xabar sxemasi domen ichki tuzilishiga bog'lanadi. Mapper ikki yo'nalishda ishlaydi: domen → xabar va xabar → domen. Bu sxema evolyutsiyasini bitta joyda boshqarish imkonini beradi.

**Spring'da qayerda uchraydi:** `org.springframework.messaging.converter.MessageConverter` ierarxiyasi: `SimpleMessageConverter`, `MappingJackson2MessageConverter`, `StringMessageConverter`, `ProtobufMessageConverter`, hamda `SmartMessageConverter`. Spring Framework 7 / Boot 4 da Jackson 3 uchun `JacksonJson*` nomli converterlar qo'shildi, Jackson 2 variantlari esa `Jackson2` prefiksi bilan qoldi. Transport darajasida Spring AMQP `Jackson2JsonMessageConverter`, Spring for Apache Kafka `JsonSerializer`/`JsonDeserializer` va `JsonMessageConverter`, JMS uchun `MappingJackson2MessageConverter`. Domen↔DTO map'i uchun `Converter<S, T>` + `ConversionService` yoki MapStruct generatsiyasi ishlatiladi; `@Payload` argument resolver mapperni avtomatik qo'llaydi.

**Qo'llanish keyslari:**
- JPA entity'ni to'g'ridan-to'g'ri topicga yubormasdan, event DTO'ga map qilish.
- Avro `SpecificRecord` va domen record o'rtasida ikki tomonlama mapper yozish.
- Bir xil domen obyektini ikki xil tashqi sxemaga (v1, v2) map qilib, migratsiyani bosqichli qilish.
- `type` headerini `JsonDeserializer` trusted packages bilan birga xavfsiz boshqarish.
- Legacy fixed-width xabarni domen obyektiga mapper orqali keltirish.

**Ehtiyot bo'ling:** Entity'ni to'g'ridan-to'g'ri serializatsiya qilish (lazy proxy, `@JsonIgnore` yetishmasligi, ichki maydonlar oqib ketishi) eng ko'p uchraydigan xato - har doim alohida wire-model saqlang. Yana: deserializatsiyada `type` headeriga ishonib, ixtiyoriy sinfni yuklash (polymorphic deserialization) xavfsizlik teshigi, shuning uchun trusted package ro'yxati majburiy.

## 16.9 Tranzaksion Mijoz (Transactional Client)

**Tavsif:** Mijoz broker bilan tranzaksiya doirasida ishlaydi: xabar o'qish, DB o'zgarishi va xabar yuborish bitta atomar birlik sifatida commit yoki rollback bo'ladi. Bu dublikat va yo'qolgan xabarlar muammosini kamaytiradi, lekin tranzaksiya chegarasi faqat bitta resurs doirasida ishonchli bo'ladi. Ko'p resursda XA yoki alternativ naqshlar kerak bo'ladi.

**Spring'da qayerda uchraydi:** `@Transactional` + `PlatformTransactionManager`; transport uchun `JmsTransactionManager`, `RabbitTransactionManager`, `KafkaTransactionManager` (`spring-kafka`). `JmsTemplate.setSessionTransacted(true)`, `DefaultMessageListenerContainer.setSessionTransacted(true)`, `SimpleRabbitListenerContainerFactory.setChannelTransacted(true)` konteyner darajasida tranzaksiyani yoqadi. Kafka'da `KafkaTemplate.executeInTransaction(...)`, `spring.kafka.producer.transaction-id-prefix` va `isolation.level=read_committed` kombinatsiyasi "read-process-write" atomarligini beradi. `ChainedTransactionManager` eskirgan; haqiqiy XA uchun `JtaTransactionManager` (Atomikos/Narayana) yoki - tavsiya etilgan yo'l - transactional outbox (DB jadvaliga yozib, keyin Debezium/poller bilan yuborish).

**Qo'llanish keyslari:**
- Buyurtmani DB'ga yozish va `OrderCreated` hodisasini outbox jadvali orqali atomar yuborish.
- Kafka'da `read-process-write` oqimini `transaction-id-prefix` bilan exactly-once (EOS) qilish.
- JMS listenerda xabarni faqat DB commit muvaffaqiyatli bo'lgandan keyin acknowledge qilish.
- Rollback holatida xabarni broker qayta yetkazishiga tayanib retry qurish.
- Spring Batch step'ida chunk tranzaksiyasi bilan reader/writer izchilligini saqlash.

**Ehtiyot bo'ling:** DB va broker ustida "tranzaksiya" deganda ko'pincha sinxronlashtirilgan ikki alohida commit tushuniladi - ular orasida nosozlik bo'lsa dual-write muammosi qoladi, shuning uchun XA'ga tayanmasdan outbox + idempotent iste'molchi tanlang. Shuningdek uzun tranzaksiya ichida tashqi HTTP chaqirish lock ushlab turadi va throughput'ni yo'q qiladi.

## 16.10 So'rovchi Iste'molchi (Polling Consumer)

**Tavsif:** Iste'molchi o'zi tashabbus bilan kanaldan xabarni ma'lum interval yoki jadval bo'yicha olib keladi. Bu yondashuv iste'mol tezligini to'liq nazorat qilish (back-pressure) imkonini beradi va event-driven push imkoni yo'q manbalar (fayl papkasi, DB jadvali, FTP, mail) uchun yagona yo'l. Evaziga latency oshadi va bo'sh pollinglar resurs sarflaydi.

**Spring'da qayerda uchraydi:** Spring Integration'ning `PollingConsumer` endpointi, `PollerMetadata`, `@Poller` (`@InboundChannelAdapter(poller = @Poller(fixedDelay = "5000"))`) va DSL'da `.poller(Pollers.fixedDelay(Duration.ofSeconds(5)).maxMessagesPerPoll(10))`. Manba adapterlar: `FileReadingMessageSource`, `JdbcPollingChannelAdapter`, `MailReceivingMessageSource`, `SftpInboundFileSynchronizingMessageSource`, `KafkaMessageSource`. Sof Spring'da `@Scheduled` + `JmsTemplate.receive()`/`receiveAndConvert()` yoki `@Scheduled` + repository so'rovi. Kafka'ning `KafkaConsumer`i ham ichdan poll qiladi, ammo `ConcurrentMessageListenerContainer` uni ilovaga event-driven ko'rinishida beradi. Ko'p instansda takrorlanishni to'xtatish uchun ShedLock yoki `JdbcLockRegistry` (`LockRegistryLeaderInitiator`) ishlatiladi.

**Qo'llanish keyslari:**
- SFTP papkasidagi kunlik hisobot fayllarini har 5 daqiqada olib kelish.
- Outbox jadvalini poller bilan skanerlab, yuborilmagan hodisalarni jo'natish.
- Legacy tizim faqat REST so'rov qabul qilganda, o'zgarishlarni interval bilan tortib olish.
- Batch oynasi uchun xabarlarni `maxMessagesPerPoll` bilan boshqariladigan tezlikda iste'mol qilish.
- Pochta qutisidagi hujjatlarni IMAP orqali davriy o'qish.

**Ehtiyot bo'ling:** Bir nechta instansda bir xil poller ishlaganda bir xil yozuv ikki marta qayta ishlanadi - distributed lock yoki `SELECT ... FOR UPDATE SKIP LOCKED` majburiy. Juda qisqa interval DB/FTP'ni ortiqcha yuklaydi, juda uzun interval esa SLA'ni buzadi; `maxMessagesPerPoll` va tranzaksion poller sozlamalarini e'tibordan chetda qoldirmang.

## 16.11 Hodisaga Asoslangan Iste'molchi (Event-Driven Consumer)

**Tavsif:** Iste'molchi xabarni o'zi so'ramaydi - messaging infratuzilmasi xabar kelganda iste'molchi metodini chaqiradi (push model). Bu minimal latency va bo'sh polling yo'qligini ta'minlaydi, lekin iste'mol tezligi broker nazoratida bo'lgani uchun back-pressure'ni alohida sozlash kerak. Zamonaviy Spring ilovalarida bu asosiy iste'mol modeli.

**Spring'da qayerda uchraydi:** `@JmsListener`, `@RabbitListener`, `@KafkaListener` annotatsiyalari va ularning ostidagi `MessageListenerContainer` implementatsiyalari (`DefaultMessageListenerContainer`, `SimpleMessageListenerContainer`/`DirectMessageListenerContainer`, `ConcurrentMessageListenerContainer`). Spring Integration'da `EventDrivenConsumer` endpointi `SubscribableChannel` (`DirectChannel`, `PublishSubscribeChannel`, `ExecutorChannel`) ga `MessageHandler` sifatida obuna bo'ladi; `@ServiceActivator` shu endpointni yaratadi. Ilova ichidagi hodisalar uchun `ApplicationEventPublisher` + `@EventListener`/`@TransactionalEventListener`, reaktiv oqimlar uchun Spring Cloud Stream `Consumer<Flux<T>>` funksiyalari ishlatiladi. Xatolik boshqaruvi `DefaultErrorHandler`, `@RetryableTopic`, `RetryTemplate` bilan sozlanadi.

**Qo'llanish keyslari:**
- `@KafkaListener` bilan to'lov hodisalarini real vaqtda qayta ishlash.
- `@RabbitListener` orqali xabar kelishi bilan bildirishnoma yuborish.
- `@TransactionalEventListener(phase = AFTER_COMMIT)` bilan DB commit'dan keyin integratsiya hodisasini chiqarish.
- WebSocket/SSE orqali mijozga push qilish uchun ichki hodisalarni tinglash.
- Spring Integration flow'ida `DirectChannel` + `@ServiceActivator` bilan past latencyli ichki pipeline qurish.

**Ehtiyot bo'ling:** Listener metodida og'ir yoki uzoq ish bajarish broker rebalance/`max.poll.interval.ms` muammosiga olib keladi va butun partition iste'molini to'xtatadi - uzoq ishni alohida pool yoki keyingi topicga uzatish kerak. `DirectChannel` push modelida handler chaqiruvchi thread'da ishlaydi, shuning uchun u yerdagi bloklanish yuboruvchini ham bloklaydi.

## 16.12 Raqobatlashuvchi Iste'molchilar (Competing Consumers)

**Tavsif:** Bir kanalga bir nechta iste'molchi obuna bo'ladi va har bir xabarni ulardan faqat bittasi oladi, shu bilan ish yuk ular orasida taqsimlanadi va throughput chiziqli oshadi. Bu bir vaqtda gorizontal masshtablash va nosozlikka chidamlilik beradi. Evaziga xabarlar o'rtasida global tartib yo'qoladi.

**Spring'da qayerda uchraydi:** `@JmsListener(concurrency = "3-10")` va `DefaultMessageListenerContainer.setConcurrentConsumers/setMaxConcurrentConsumers`; `@RabbitListener(concurrency = "5")`, `SimpleRabbitListenerContainerFactory.setConcurrentConsumers(...)` + `setPrefetchCount(...)`, `DirectMessageListenerContainer.setConsumersPerQueue(...)`. Kafka'da `ConcurrentKafkaListenerContainerFactory.setConcurrency(n)` yoki `@KafkaListener(concurrency = "4")` - bu yerdagi parallellik partition soni bilan cheklanadi, haqiqiy taqsimlash esa consumer group orqali bo'ladi. Spring Integration'da `ExecutorChannel` + `TaskExecutor` yoki `QueueChannel` ustida bir nechta `PollingConsumer` shu patternni ichki kanalda beradi.

**Qo'llanish keyslari:**
- PDF generatsiya navbatini 10 ta worker instans bilan parallel qayta ishlash.
- Kafka consumer group'ga pod qo'shib, trafik o'sganda avtomatik masshtablash (KEDA).
- Rabbit work queue'da `prefetch=1` bilan uzoq ishlarni adolatli taqsimlash.
- Bitta instans ichida `concurrency` oshirib, I/O-bound xabarlarni tezroq iste'mol qilish.
- Nosoz pod o'chganda xabarlar qolgan iste'molchilarga o'tib ketishini ta'minlash.

**Ehtiyot bo'ling:** Tartib talab qiladigan oqimlarda (bir hisob bo'yicha ketma-ket operatsiyalar) raqobatlashuvchi iste'molchilar tartibni buzadi - Kafka'da kalit bo'yicha partitionlash yoki Rabbit'da "single active consumer" kerak. Shuningdek concurrency'ni DB connection pool hajmidan oshirib qo'yish bottleneck'ni brokerdan DB'ga ko'chiradi.

## 16.13 Xabar Dispetcheri (Message Dispatcher)

**Tavsif:** Kanaldan xabarni bitta komponent - dispetcher - oladi va uni ro'yxatdagi performerlardan biriga (yoki hammasiga) uzatadi. Shu bilan iste'molchilarning parallelligi, tanlash strategiyasi va xatolik boshqaruvi markazlashtiriladi, performerlar esa oddiy handler bo'lib qoladi. Competing Consumers'dan farqi: taqsimlash mantig'i broker emas, dispetcher qo'lida.

**Spring'da qayerda uchraydi:** Spring Integration yadrosida `MessageDispatcher` interfeysi va ikki implementatsiyasi: `UnicastingDispatcher` (`DirectChannel`, `ExecutorChannel` ichida - bitta subscriber tanlanadi) va `BroadcastingDispatcher` (`PublishSubscribeChannel` - barcha subscriberlarga). Tanlash strategiyasi `LoadBalancingStrategy`, standart implementatsiya `RoundRobinLoadBalancingStrategy`; `DirectChannel.setFailover(true)` bilan birinchi handler xato bersa keyingisiga o'tiladi. Spring MVC'dagi `DispatcherServlet` + `HandlerMapping` ham shu g'oyaning HTTP varianti, Kafka'da esa `ConcurrentMessageListenerContainer` partitionlarni ichki `KafkaMessageListenerContainer`larga taqsimlab shu rolni bajaradi.

**Qo'llanish keyslari:**
- `DirectChannel`ga ikki handler obuna qilib, round-robin bilan yukni ichkarida taqsimlash.
- `failover` bilan asosiy handler ishlamay qolganda zaxira handlerga o'tish.
- `PublishSubscribeChannel` orqali bitta hodisani audit, notification va analytics handlerlariga bir vaqtda yuborish.
- `ExecutorChannel` + `ThreadPoolTaskExecutor` bilan handler chaqiriqlarini asinxron qilish.
- Kafka konteynerida partitionlarni thread'lar bo'yicha boshqariladigan tarzda bo'lish.

**Ehtiyot bo'ling:** `DirectChannel`da dispetcher xabarni yuboruvchi thread'ida tarqatadi, shuning uchun bitta sekin handler butun oqimni bloklaydi; asinxronlik kerak bo'lsa `ExecutorChannel`/`QueueChannel` tanlang - lekin u bilan tranzaksiya va thread-bound konteks (Security, MDC) yo'qolishini hisobga oling. `failover`ni idempotent bo'lmagan handlerlar bilan yoqish xabarning qisman ikki marta bajarilishiga olib keladi.

## 16.14 Tanlab qabul qiluvchi (Selective Consumer)

**Tavsif:** Bitta kanalda turli xil xabarlar aralash kelganda, consumer faqat o'ziga tegishli xabarlarni oladi, qolganlarini broker boshqa consumerga qoldiradi. Tanlash mezoni xabar header'lari yoki property'lari ustidagi predicate bo'ladi, payload'ni deserializatsiya qilmasdan. Bu Message Filter'dan farq qiladi: filter xabarni olib keyin tashlaydi, selective consumer esa umuman olmaydi. Natijada tarmoq trafigi va keraksiz ishlov kamayadi, lekin tanlanmagan xabarlar navbatda qolib ketish riski paydo bo'ladi.

**Spring'da qayerda uchraydi:** JMS'da bu to'g'ridan-to'g'ri broker darajasida ishlaydi: `@JmsListener(destination = "orders", selector = "region = 'EU' AND priority > 5")` yoki `DefaultMessageListenerContainer.setMessageSelector(...)`. Spring Integration'da `MessageSelector` interfeysi, `MessageSelectingInterceptor` va `UnexpiredMessageSelector` mavjud; `QueueChannel.purge(MessageSelector)` ham shu interfeysdan foydalanadi. RabbitMQ'da JMS selector yo'q - uning o'rniga `headers` exchange va `x-match` argumenti, yoki routing key bo'yicha ajratish ishlatiladi (`@RabbitListener(bindings = @QueueBinding(...))`). Kafka'da ham broker-side selector yo'q: tanlash yo partition/topic darajasida, yoki `RecordFilterStrategy` bilan `FilteringMessageListenerAdapter` orqali client tomonda (`ConcurrentKafkaListenerContainerFactory.setRecordFilterStrategy(...)`) bajariladi.

**Qo'llanish keyslari:**
- Bitta `payments` navbatidan valyuta header'i bo'yicha turli region service'lariga xabar taqsimlash.
- Priority yuqori buyurtmalarni alohida consumer pool'i bilan ishlash (`priority > 8` selector).
- Multi-tenant tizimda har bir tenant uchun alohida listener, `tenantId` header selector bilan.
- Kafka'da `RecordFilterStrategy` orqali `schemaVersion` eski bo'lgan record'larni commit qilib o'tkazib yuborish.
- Saga yoki long-running process'da faqat kutilgan `correlationId` bilan kelgan javobni qabul qilish.

**Ehtiyot bo'ling:** Agar hech bir consumer selector'iga tushmagan xabarlar bo'lsa, ular navbatda abadiy qolib, queue depth monitoring'ni buzadi va oxir-oqibat broker xotirasini to'ldiradi - doim "catch-all" consumer yoki TTL + DLQ qo'ying. Selector'lar broker tomonda indekslanmagan skanerlash bo'lgani uchun navbat uzun bo'lsa throughput keskin tushadi; bunday holda bitta kanalni bo'lib yuborish (Content-Based Router yoki alohida topic) deyarli har doim yaxshiroq.

## 16.15 Ishonchli obunachi (Durable Subscriber)

**Tavsif:** Publish-Subscribe kanalda obunachi offline bo'lgan paytda yuborilgan xabarlar yo'qolmasligi uchun broker ularni obunachi nomidan saqlab turadi va u qaytganda yetkazib beradi. Buning uchun obunachi barqaror identifikatorga (client ID + subscription name yoki consumer group) ega bo'lishi kerak. Non-durable obunachi uchun uzilish davridagi xabarlar oddiygina yo'qoladi. Narxi - brokerda state va disk o'sishi, hamda "o'lik" obunalarni tozalash majburiyati.

**Spring'da qayerda uchraydi:** JMS'da `DefaultJmsListenerContainerFactory` ustida `setSubscriptionDurable(true)`, `setSubscriptionShared(true)` (JMS 2.0 shared durable) va `setClientId(...)`, listener tomonda `@JmsListener(destination = "events", subscription = "billing-sub", containerFactory = "topicFactory")`. Spring Integration JMS modulida `Jms.messageDrivenChannelAdapter(...).subscriptionDurable(true).durableSubscriptionName("...")`. Kafka'da bu pattern tabiiy ravishda `group.id` + committed offset va `auto.offset.reset=earliest` orqali ishlaydi (`@KafkaListener(groupId = "billing")`). MQTT uchun `MqttPahoMessageDrivenChannelAdapter` bilan `cleanSession=false` va barqaror `clientId`. RabbitMQ'da esa durable queue + persistent message kombinatsiyasi shu rolni bajaradi: `@RabbitListener` o'qiydigan navbat `durable=true` bo'lsa, consumer uzilganda ham xabarlar navbatda qoladi.

**Qo'llanish keyslari:**
- Billing service deploy/restart paytida `order-events` topic'dagi hech bir event yo'qolmasligi kerak bo'lgan hol.
- Audit yoki compliance consumer'i - hamma eventni, kechikish bilan bo'lsa ham, albatta ko'rishi shart.
- Analytics pipeline'ni bir kecha to'xtatib, ertalab backlog'ni qayta o'qish (Kafka consumer group).
- IoT qurilma qisqa vaqt tarmoqdan uzilganda MQTT buyruqlarini keyin olishi.
- Blue-green deploy'da yangi versiya eski subscription nomini davom ettirib, oraliq eventlarni yutib olishi.

**Ehtiyot bo'ling:** Tashlab ketilgan durable subscription brokerni sekin o'ldiradi - xabarlar to'planib disk va memory limitga uriladi, shuning uchun obuna nomlari rejali boshqarilishi va ishlatilmaganlari o'chirilishi kerak. `clientId` ikki instansiyada bir xil bo'lsa klassik (shared bo'lmagan) durable subscription'da ikkinchi instansiya `InvalidClientIDException` bilan yiqiladi - horizontal scaling uchun JMS 2.0 shared durable yoki Kafka consumer group ishlatiladigan dizaynni tanlang.

## 16.16 Idempotent qabul qiluvchi (Idempotent Receiver)

**Tavsif:** At-least-once yetkazib berishda bir xil xabar bir necha marta kelishi muqarrar, shuning uchun receiver takroriy xabarni aniqlab, biznes effektini ikkinchi marta bajarmasligi kerak. Amalda xabarning biznes kaliti (yoki `messageId`) persistent store'da saqlanadi va har kelganda tekshiriladi; yoki operatsiyaning o'zi tabiiy idempotent qilib yoziladi (`UPSERT`, absolute qiymat o'rnatish). Bu pattern Exactly-Once illyuziyasini qurishning eng arzon va amaliy yo'li.

**Spring'da qayerda uchraydi:** Spring Integration'da to'g'ridan-to'g'ri qo'llab-quvvatlanadi: `IdempotentReceiverInterceptor` + `MetadataStoreSelector` + `ConcurrentMetadataStore` implementatsiyalari (`JdbcMetadataStore`, `RedisMetadataStore`, `MongoDbMetadataStore`, `ZookeeperMetadataStore`, `PropertiesPersistingMetadataStore`), hamda `@IdempotentReceiver("interceptorBeanName")` annotatsiyasi endpoint ustida. Oddiy Spring Boot 3.x ilovasida bu ko'pincha `processed_messages` jadvaliga unique constraint bilan `INSERT` qilib, `DataIntegrityViolationException` tutish, yoki JPA `@Version` / `ON CONFLICT DO NOTHING` orqali amalga oshiriladi. Kafka tomonida `@KafkaListener` + `enable.idempotence=true` producer sozlamasi va transactional `KafkaTemplate` yordam beradi, lekin consumer tomondagi dublikat himoyasini o'zi hal qilmaydi.

```java
@Bean
IdempotentReceiverInterceptor idempotentInterceptor(ConcurrentMetadataStore store) {
    MetadataStoreSelector selector = new MetadataStoreSelector(
            msg -> msg.getHeaders().get("orderId", String.class), store);
    var interceptor = new IdempotentReceiverInterceptor(selector);
    interceptor.setDiscardChannelName("duplicateChannel");
    return interceptor;
}
```

**Qo'llanish keyslari:**
- Payment gateway webhook'i bir xil `transactionId` bilan uch marta kelganda bitta marta hisobdan yechish.
- Kafka consumer rebalance'dan keyin commit qilinmagan offset'lar qayta o'qilganda stock ikki marta kamaymasligi.
- Email/SMS yuborish handler'ida bir xil notification ID uchun takroriy xabar yubormaslik.
- Saga qadamining retry'dan keyin qayta ishga tushishi (compensation ham idempotent bo'lishi kerak).
- Outbox poller'ning ikki instansiyasi bir xil eventni publish qilganda consumer tomonda dublikatni yutish.

**Ehtiyot bo'ling:** Dublikat kalitini yozish va biznes operatsiyasini bajarish bitta atomar chegarada (bir xil DB tranzaksiyasida) bo'lmasa, crash paytida yo "yozildi lekin bajarilmadi", yo teskarisi yuz beradi - in-memory `SimpleMetadataStore` esa restart'dan keyin butun himoyani yo'qotadi. Kalitlarni abadiy saqlash store'ni cheksiz o'stiradi, shuning uchun biznes uchun mantiqiy TTL (masalan 7-30 kun) va retention ishini oldindan rejalashtiring.

Mavzuning to'liq yozuvi [idempotency](07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 16.17 Service Activator (Service Activator)

**Tavsif:** Messaging infratuzilmasi bilan oddiy biznes POJO o'rtasida ko'prik bo'lib, kanaldan kelgan xabarni metod chaqiruviga aylantiradi va natijani (agar bo'lsa) reply kanaliga qaytaradi. Shu tufayli domain kodi `Message`, kanal yoki broker API'sini bilmaydi va xuddi oddiy service kabi unit-test qilinadi. Payload argumentga, header'lar esa alohida parametrlarga bind qilinadi.

**Spring'da qayerda uchraydi:** Spring Integration'da `@ServiceActivator(inputChannel = "orders", outputChannel = "results")` annotatsiyasi, uning ichki implementatsiyasi `ServiceActivatingHandler` va `MessageHandler`/`GenericHandler` interfeyslari; Java DSL'da `.handle(OrderService.class, "process")` yoki `.handle((payload, headers) -> ...)`. Bind qilish `@Payload`, `@Header`, `@Headers`, `@MessageMapping` orqali bo'ladi. Kengroq Spring ekotizimida bir xil g'oyani `@KafkaListener`, `@RabbitListener`, `@JmsListener` va `@SqsListener` metodlari, hamda Spring Cloud Stream'ning `Function<T, R>` / `Consumer<T>` bean'lari bajaradi - ular ham xabarni POJO metodiga ulaydi.

**Qo'llanish keyslari:**
- `OrderValidator.validate(Order)` metodini `validation` kanaliga ulash va natijani keyingi qadamga uzatish.
- Legacy service'ni o'zgartirmasdan messaging pipeline'ga qo'shish (wrapper kod yozmasdan).
- Request-reply integration flow'ida javobni `replyChannel` header'i bo'yicha avtomatik qaytarish.
- Aggregator'dan chiqqan to'plangan natijani bitta report generator metodiga berish.
- Spring Cloud Stream'da `Function<OrderEvent, InvoiceCommand>` bean'ini binding orqali Kafka'ga ulash.

**Ehtiyot bo'ling:** Service activator metodi `void` qaytarsa flow shu joyda tugaydi - `outputChannel` berilgan bo'lsa ham reply bo'lmaydi, bu esa request-reply'da timeout sifatida namoyon bo'ladi. Metod ichida uzoq blocking ish qilish consumer thread'ini egallab broker'da backpressure yaratadi; bunday hollarda `ExecutorChannel`, `TaskExecutor` yoki virtual thread'lar bilan ajratish va alohida error channel belgilash kerak.

## 16.18 Boshqaruv shinasi (Control Bus)

**Tavsif:** Ilovaning integration komponentlarini boshqarish buyruqlarini (start, stop, poller interval o'zgartirish, metrika o'qish) oddiy biznes xabarlari bilan bir xil messaging mexanizmi orqali yuborish imkonini beradi. Boshqaruv trafigi alohida kanalda yuradi, shuning uchun ma'lumot oqimidan ajratilgan bo'ladi. Bu runtime'da deploy qilmasdan tizim xatti-harakatini o'zgartirishga yo'l ochadi.

**Spring'da qayerda uchraydi:** Spring Integration'da Java DSL'dagi `.controlBus()` (`IntegrationFlow.from("controlChannel").controlBus()`) va `ControlBusFactoryBean`; boshqariladigan komponentlar `Lifecycle`/`SmartLifecycle` va `@ManagedResource`/`@ManagedOperation` orqali ochiladi, masalan `@EndpointId("poller")` bilan nomlangan endpoint'ga `"poller.stop()"` buyrug'i yuboriladi. Spring Integration 6.4+ da klassik SpEL baholashdan ko'proq nazorat qilingan `ControlBusCommandRegistry` yondashuvi kiritilgan, shuning uchun migratsiyada versiyaga qarab tekshirish kerak. Boshqaruv uchun qo'shimcha kanal - Spring Boot Actuator: `/actuator/integrationgraph` (`@EnableIntegrationManagement` bilan), `/actuator/loggers`, `/actuator/env` va `@RefreshScope` bilan Spring Cloud Config.

**Qo'llanish keyslari:**
- Bazani maintenance'ga olishdan oldin barcha inbound poller'ni to'xtatib, keyin qayta ishga tushirish.
- Yuklama cho'qqisida file poller'ning `fixedDelay` qiymatini runtime'da kattalashtirish.
- Incident paytida muayyan channel adapter'ni o'chirib, qolgan flow'ni ishlayotgan holda qoldirish.
- Operator panelidan JMS navbatiga buyruq yuborib, kluster bo'ylab barcha node'larda bir vaqtda komponentni to'xtatish.
- Smoke test'dan oldin flow'ni `start()` qilib, test tugagach `stop()` qilish.

**Ehtiyot bo'ling:** Control bus kanali - bu masofadan kod bajarish vektori: SpEL asosidagi klassik implementatsiyada tashqi/ishonchsiz manbadan kelgan buyruq jiddiy xavf, shuning uchun kanal autentifikatsiya va tarmoq darajasida yopiq bo'lishi, buyruqlar esa oq ro'yxat bilan cheklanishi shart. Ikkinchi tuzoq - kluster: bitta node'da `stop()` qilish qolgan node'larga ta'sir qilmaydi, natijada topologiya "yarim o'chgan" holatga tushadi va buni faqat markazlashgan monitoring ko'rsatadi.

## 16.19 Chetlab o'tish yo'li (Detour)

**Tavsif:** Xabarni asosiy yo'l o'rniga, boshqariladigan kalit asosida qo'shimcha oraliq qadamlar (validatsiya, loglash, autentifikatsiya, enrichment) orqali o'tkazib, so'ngra asosiy yo'lga qaytaradi. Kalit yoqilmaganda xabar to'g'ridan-to'g'ri ketadi, ya'ni diagnostika narxi faqat kerak bo'lganda to'lanadi. Wire Tap'dan farqi - Detour'da xabar haqiqatan ham boshqa yo'ldan yuradi, nusxa olinmaydi, shuning uchun kechikish va natijaga ta'sir qiladi.

**Spring'da qayerda uchraydi:** Spring Integration'da bu router bilan quriladi: `@Router` yoki DSL'dagi `.route(m -> detourEnabled ? "detourChannel" : "mainChannel")`, ko'pincha `AbstractMessageRouter` yoki `RecipientListRouter` ning selector'li `recipient(channel, "headers.debug == true")` ko'rinishi; kalitni runtime'da Control Bus yoki `@ManagedAttribute` bilan o'zgartiriladi. Boot ilovasida kalit `@ConfigurationProperties` + `@RefreshScope`, feature flag kutubxonasi (Togglz, FF4J, Unleash) yoki oddiy `Environment` property bo'ladi. HTTP chegarasida xuddi shu pattern Spring Cloud Gateway predicate/filter'lari, `OncePerRequestFilter` yoki `HandlerInterceptor` orqali, servis chaqiruvlarida esa `@Conditional`/`ObjectProvider` bilan almashtiriladigan `ChannelInterceptor` ko'rinishida uchraydi.

**Qo'llanish keyslari:**
- Production'da shubhali tenant uchun vaqtincha batafsil validatsiya va payload loglashni yoqish.
- Yangi transformer'ni shadow rejimda sinab ko'rish: faqat 1% trafikni qo'shimcha qadamdan o'tkazish.
- Compliance talabi paydo bo'lganda muayyan davlat xabarlarini qo'shimcha maskalash qadamiga burish.
- Debug paytida xabarni schema validator va `Message History` boyituvchisi orqali o'tkazish.
- Migratsiya davrida xabarlarni eski yoki yangi protsessorga kalit bilan yo'naltirish.

**Ehtiyot bo'ling:** Detour yoqilganda qo'shimcha qadam kechikish, xatolik manbasi va tranzaksiya chegarasini o'zgartiradi - shuning uchun u "shunchaki log" deb qaralmasligi, balki asosiy yo'l kabi test qilinishi kerak. Kalitlar vaqt o'tib unutiladi va kodni tarmoqqa aylantiradi: har bir detour uchun o'chirish muddati va egasi belgilanishi, uzoq yashaydigan diagnostika uchun esa Wire Tap yoki tracing afzal.

## 16.20 Sim ulanishi (Wire Tap)

**Tavsif:** Kanal orqali o'tayotgan xabarning nusxasini asosiy oqimga aralashmasdan ikkinchi kanalga yuboradi, shunda monitoring, audit yoki debug uchun ma'lumot olinadi. Asl xabar o'z yo'lida davom etadi va kechikish deyarli o'zgarmaydi. Odatda nusxa olish shartli (selector) va interceptor sifatida amalga oshiriladi, ya'ni biznes kodga tegmaydi.

**Spring'da qayerda uchraydi:** Spring Integration'da `org.springframework.integration.channel.interceptor.WireTap` sinfi `ChannelInterceptor` sifatida ishlaydi; DSL'da `.wireTap("auditChannel")` yoki `.wireTap(flow -> flow.handle(...))`, va `.log(LoggingHandler.Level.DEBUG, "flow")` ham ichki wire tap ustiga qurilgan. Barcha kanallarga bir vaqtda ulash uchun `@GlobalChannelInterceptor(patterns = "*.input")` ishlatiladi, shartli nusxalash uchun `WireTap.setSelector(MessageSelector)` va `setTimeout(...)`. Keng ekotizimda analoglar: `ClientHttpRequestInterceptor` / `ExchangeFilterFunction` (`RestClient`, `WebClient`), Kafka'da `ProducerInterceptor`/`ConsumerInterceptor`, hamda Micrometer `ObservationRegistry` bilan avtomatik tracing.

**Qo'llanish keyslari:**
- Barcha inbound to'lov xabarlarining nusxasini audit log'iga yozib qo'yish.
- Production trafikning nusxasini yangi service versiyasiga shadow traffic sifatida yuborish.
- Fraud detection pipeline'iga asosiy oqimni sekinlashtirmasdan ma'lumot berish.
- Integration test'da flow o'rtasidagi xabarlarni `QueueChannel`ga ulab, assert qilish.
- Incident davrida muayyan `correlationId` bo'yicha xabarlarni debug kanaliga ko'chirish (selector bilan).

**Ehtiyot bo'ling:** Wire Tap maqsad kanali `QueueChannel` bo'lib to'lib qolsa yoki `DirectChannel` orqali sekin handler'ga ulansa, u asosiy oqimni bloklaydi - `timeout` qo'yish va audit tomonida async/queue ishlatish majburiy. Ikkinchi xavf - maxfiylik: nusxaga PII, token va karta ma'lumotlari tushadi, shuning uchun loglashdan oldin maskalash va log retention siyosati bo'lishi kerak.

## 16.21 Xabar tarixi (Message History)

**Tavsif:** Xabar o'tgan barcha komponentlar ro'yxatini xabarning o'zida (header sifatida) olib yuradi, shunda murakkab, ko'p tarmoqli oqimda "bu xabar qayerdan keldi" savoliga javob topish mumkin bo'ladi. Har bir endpoint o'z nomi, turi va timestamp'ini qo'shib qo'yadi. Bu debugging va audit uchun kuchli vosita, lekin xabar hajmini va ishlov narxini oshiradi.

**Spring'da qayerda uchraydi:** Spring Integration'da `@EnableMessageHistory` (yoki `<int:message-history/>`) yoqilganda `org.springframework.integration.history.MessageHistory` to'planadi va `MessageHistory.HEADER_NAME` (`"history"`) header'idan o'qiladi; pattern bilan cheklash mumkin, masalan `@EnableMessageHistory("*Channel", "orderGateway")`. Kuzatuvning zamonaviy va distributed muqobili - Micrometer Tracing (Brave/OpenTelemetry) bilan trace/span propagation, Spring Integration tomonida `@EnableIntegrationManagement(observationPatterns = "*")`, hamda `MessageHeaderAccessor` orqali `traceparent` kabi header'larni broker chegarasidan o'tkazish. Spring Boot 3.x da `/actuator/integrationgraph` oqim topologiyasini ko'rsatadi va tarix bilan birgalikda o'qiladi.

**Qo'llanish keyslari:**
- Ko'p router va filterli oqimda xabar nimaga kutilmagan kanalga tushganini aniqlash.
- Qo'llab-quvvatlash so'rovida muayyan buyurtmaning qaysi komponentlardan o'tganini ko'rsatish.
- Loop yoki takroriy ishlov (xabar bir xil endpoint'ga ikki marta tushishi) hodisasini fosh qilish.
- Integration test'da xabar kutilgan qadamlar ketma-ketligidan o'tganini assert qilish.
- Legacy oqimni reverse-engineer qilib, haqiqiy topologiyani hujjatlashtirish.

**Ehtiyot bo'ling:** `MessageHistory` faqat bitta JVM ichidagi Spring Integration komponentlarini qamraydi - broker yoki HTTP chegarasidan o'tganda yo'qoladi, shuning uchun uni distributed tracing o'rnini bosuvchi deb hisoblash xato. Uni global `"*"` pattern bilan doimiy yoqib qo'yish har bir xabarga header va allocation qo'shadi; yuqori throughput'li oqimlarda faqat diagnostika davrida yoki tor pattern bilan yoqish to'g'ri.

## 16.22 Xabar ombori (Message Store)

**Tavsif:** Xabarlarni (yoki xabar guruhlarini) ishlov vaqtida persistent joyda saqlab, restart va crash'dan keyin tiklanish imkonini beradi. Aggregator, resequencer, delayer va queue kanallari uchun bu state'ni yo'qotmaslikning asosiy mexanizmi. Shuningdek keyinroq tahlil, qayta yuborish (replay) va claim-check uchun xabar ma'lumotini saqlash joyi bo'lib xizmat qiladi.

**Spring'da qayerda uchraydi:** Spring Integration'da `MessageStore` va `MessageGroupStore` interfeyslari, implementatsiyalari: `SimpleMessageStore` (in-memory, default), `JdbcMessageStore`, `JdbcChannelMessageStore` (persistent `QueueChannel` uchun), `MongoDbMessageStore`, `RedisMessageStore`, `JpaMessageStore`. Ular `.aggregate(a -> a.messageStore(store))`, `.delay("d", d -> d.messageStore(store))` yoki `new QueueChannel(channelMessageStore, "groupKey")` ko'rinishida ulanadi; JDBC uchun `schema-*.sql` skriptlari (`INT_MESSAGE`, `INT_GROUP_TO_MESSAGE` jadvallari) Spring Integration JDBC modulida keladi. Yaqin tushunchalar: `ConcurrentMetadataStore` (offset/idempotency uchun), Spring Modulith'ning `event_publication` jadvali (`@ApplicationModuleListener` uchun completion tracking) va o'z qo'lingiz bilan quriladigan Transactional Outbox jadvali.

**Qo'llanish keyslari:**
- Aggregator 10 ming yarim to'plangan guruhni ushlab turganda deploy qilish va state'ni yo'qotmaslik.
- `QueueChannel`ni `JdbcChannelMessageStore` bilan persistent qilib, crash paytida xabarlar yo'qolmasligi.
- Delayer bilan "24 soatdan keyin eslatma" rejalashtirish va shu davrda restart bo'lishiga tayyor bo'lish.
- Claim Check pattern'ida katta payload'ni store'ga qo'yib, kanalda faqat kalitni uzatish.
- Failed message'larni saqlab, operator panelidan tanlab qayta yuborish (replay).

**Ehtiyot bo'ling:** Default `SimpleMessageStore` in-memory bo'lgani uchun "aggregator ishlayapti" degan ishonch restart'da yolg'onga aylanadi - production'da persistent store ongli ravishda tanlanishi va DB tranzaksiyasi bilan moslashtirilishi kerak. Persistent store tanlangach, u tez o'sadigan "hot" jadvalga aylanadi: tugallangan guruhlarni tozalash (`MessageGroupStoreReaper`, expiry), indekslar va kluster muhitida bir xil `region`/`groupId` to'qnashuvi oldindan hal qilinishi lozim.

## 16.23 Aqlli proxy (Smart Proxy)

**Tavsif:** Request-reply servisi oldiga qo'yiladigan proxy bo'lib, so'rovni o'tkazishdan oldin asl `reply-to` manzili va metadata'ni saqlab qo'yadi, javob kelganda esa uni asl so'rovchiga qaytaradi va shu bilan birga javobni ham kuzatadi. Bu oddiy Wire Tap bilan hal bo'lmaydi, chunki har bir mijoz o'z reply kanalini ko'rsatadi va javob nusxasini olish uchun korrelyatsiya kerak. Natijada servis latency, xatolik foizi va javob mazmuni markazdan kuzatiladi, servis kodiga tegmasdan.

**Spring'da qayerda uchraydi:** Spring Integration'da bu `HeaderEnricher`/`@Transformer` bilan asl `replyChannel`/`errorChannel` header'ini `MessageStore` yoki metadata store'ga yozib, servisga sun'iy reply kanalini berish, javob kelganda esa saqlangan header'ni qayta tiklash orqali quriladi; `HeaderChannelRegistry` (`.enrichHeaders(h -> h.headerChannelsToString())`) aynan reply kanalini stringga aylantirib broker orqali uzatish uchun mavjud. Kuzatish qismi `WireTap`, `MessageHandler` metrikalar va Micrometer `Timer`/`ObservationRegistry` bilan bajariladi. HTTP dunyosida xuddi shu rolni Spring Cloud Gateway `GlobalFilter`/`GatewayFilter` (so'rov va javobni birga ko'radi), `ExchangeFilterFunction` va service mesh sidecar'lari o'ynaydi.

**Qo'llanish keyslari:**
- Tashqi provayder servisining real javob vaqtini SLA hisobot uchun markazdan o'lchash.
- Har bir mijoz o'z `replyTo` navbatini ko'rsatadigan JMS request-reply'da javoblarni audit qilish.
- Javobdagi xato kodlarini yig'ib, circuit breaker va alert qoidalarini shunga qurish.
- Legacy servisga tegmasdan request/response juftligini compliance uchun arxivlash.
- Migratsiyada eski va yangi servis javoblarini yonma-yon solishtirish (shadow comparison).

**Ehtiyot bo'ling:** Proxy saqlagan korrelyatsiya state'i restart'da yo'qolsa javoblar "yetim" bo'lib qoladi, shuning uchun store persistent va TTL bilan bo'lishi, timeout'da esa asl so'rovchiga aniq xatolik qaytarilishi kerak. Har bir so'rov-javob juftligini to'liq saqlash tez orada eng katta xarajat manbasiga aylanadi va PII yig'adi - sampling, maskalash va retention'ni boshidan belgilang.

## 16.24 Test xabari (Test Message)

**Tavsif:** Tizimga maxsus belgilangan sintetik xabar yuborilib, uning oqimdan to'g'ri o'tgani va kutilgan natija bergani tekshiriladi; shu yo'l bilan komponent "ishlayapti" emas, balki "to'g'ri ishlayapti" degan ishonch olinadi. Test xabari odatda alohida header bilan belgilanadi va natija verifikator tomonidan solishtiriladi, real ma'lumotga esa aralashmaydi. Bu passiv health check'dan kuchliroq: "silent failure" (xabar yutilib ketishi, noto'g'ri transformatsiya) ni ham aniqlaydi.

**Spring'da qayerda uchraydi:** Boot 3.x da sintetik tekshiruvni `HealthIndicator`/`AbstractHealthIndicator` bean'i sifatida yozib, `/actuator/health`ga ulash odatiy yo'l; davriy yuborish uchun `@Scheduled` yoki Spring Integration inbound poller (`.fixedRate(...)`), yuborish uchun `JmsTemplate`, `RabbitTemplate`, `KafkaTemplate` yoki `MessagingGateway`. Test xabarini real oqimdan ajratish `@Header("x-synthetic")` + router/filter, natijani tekshirish esa `.wireTap("verifyChannel")` va alohida handler orqali qilinadi. Pre-prod va CI darajasida bu `spring-integration-test` moduli (`@SpringIntegrationTest`, `MockIntegration`, `MessageVerifier`), Testcontainers (`KafkaContainer`, `RabbitMQContainer`) va `@EmbeddedKafka` bilan avtomatlashtiriladi.

**Qo'llanish keyslari:**
- Har 60 soniyada sintetik buyurtma yuborib, to'liq order pipeline'ning end-to-end sog'lig'ini kuzatish.
- Deploy'dan keyin smoke test: bitta test xabari o'tmasa, avtomatik rollback trigger qilish.
- Tungi vaqtda trafik yo'q bo'lganda ham integration uzilishini ertalabdan oldin aniqlash.
- Tashqi provayder sandbox'iga test chaqiruvi yuborib, sertifikat yoki token amal qilishini tekshirish.
- Transformatsiya qoidasi o'zgargach, kutilgan natijani sintetik xabar bilan canary tarzda tasdiqlash.

**Ehtiyot bo'ling:** Test xabari real hisob-kitobga, reporting'ga yoki tashqi hamkorga chiqib ketsa, bu haqiqiy moliyaviy xatoga aylanadi - belgilovchi header, alohida tenant/test account va chegaradagi filter majburiy, "unutilgan" sintetik yozuvlarni tozalash ishi ham bo'lishi kerak. Yana bir tuzoq - test xabari asosiy yo'ldan boshqacha yurishi: u haqiqiy oqimni emas, faqat o'zining maxsus yo'lini tekshirsa, ishonch yolg'on bo'ladi.

## 16.25 Kanal tozalovchi (Channel Purger)

**Tavsif:** Kanal yoki navbatda qolib ketgan, endi keraksiz yoki eskirgan xabarlarni ongli ravishda olib tashlash vositasi. Test muhitini tiklash, incident'dan keyin "zaharli" backlog'ni tozalash yoki noto'g'ri formatda yuborilgan ming xabarni olib tashlash uchun kerak bo'ladi. Tanlab tozalash (selector bilan) to'liq tozalashdan ancha xavfsiz.

**Spring'da qayerda uchraydi:** Spring Integration'da `QueueChannel.purge(MessageSelector)` to'g'ridan-to'g'ri shu maqsadga xizmat qiladi va `null` selector bilan hammasini tozalaydi; persistent kanal uchun `MessageGroupStore.removeMessageGroup(...)`, eskirgan guruhlar uchun `MessageGroupStoreReaper` (`setTimeout`, `expireGroupsUponTimeout`) ishlatiladi. AMQP'da `AmqpAdmin`/`RabbitAdmin.purgeQueue(queueName, noWait)` navbatni brokerda tozalaydi. JMS'da standart purge API yo'q - amalda `JmsTemplate` bilan selector qo'yib consume qilib tashlash yoki broker admin vositasi (ActiveMQ/Artemis konsoli, JMX) ishlatiladi. Kafka'da xabar o'chirilmaydi: `KafkaAdmin`/`AdminClient` bilan `deleteRecords(...)`, topic retention o'zgartirish, yoki consumer tomonda `ConsumerSeekAware` / `seekToEnd` bilan backlog'ni o'tkazib yuborish qo'llaniladi.

**Qo'llanish keyslari:**
- Integration test'lar orasida `QueueChannel`ni tozalab, testlarning bir-biriga ta'sirini yo'qotish.
- Buzilgan deploy ming marta noto'g'ri formatdagi xabar yuborgandan keyin DLQ'ni tozalash.
- Muddati o'tgan buyruqlarni (`UnexpiredMessageSelector`) navbatdan olib tashlash.
- Staging muhitida prod'dan ko'chirilgan eski backlog'ni tozalab, toza holatdan boshlash.
- Kafka consumer'ni incident'dan keyin `seekToEnd` bilan "hozirgi vaqtdan" ishga tushirish.

**Ehtiyot bo'ling:** Purge - qaytarilmas ma'lumot yo'qotish: avval xabarlarni arxivga (Message Store, S3, fayl) ko'chirib, keyin tozalash va amalni audit qilish kerak; prod'da bu operatsiya hech qachon ilova kodida avtomatik ishlamasligi, faqat nazorat ostidagi admin amal bo'lishi lozim. Shuningdek "navbat to'lib qolgani" ko'pincha simptom - purge bilan uni yashirish o'rniga consumer throughput, poison message va DLQ sabablari tuzatilishi shart.

## 16.26 Hodisa xabarnomasi (Event Notification)

**Tavsif:** Publisher holat o'zgargani haqida minimal, "yupqa" event yuboradi - odatda faqat agregat ID'si, turi va vaqti - qabul qiluvchi esa kerak bo'lsa detallarni manbadan alohida so'rab oladi. Bu publisher va consumer o'rtasidagi contract'ni juda kichik qiladi va schema evolyutsiyasini osonlashtiradi, lekin har bir consumer uchun qo'shimcha so'rov (chatty tizim) narxini keltiradi. Qarama-qarshi variant - Event-Carried State Transfer, bunda event o'z ichida to'liq ma'lumotni olib yuradi.

**Spring'da qayerda uchraydi:** Monolit ichida `ApplicationEventPublisher.publishEvent(...)`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)` va `@Async` bilan; Spring Data'da domain eventlarni agregatdan chiqarish uchun `AbstractAggregateRoot.registerEvent(...)`, `@DomainEvents` va `@AfterDomainEventPublication`. Modulli monolitda Spring Modulith `@ApplicationModuleListener` (tranzaksion + async + persistent `event_publication` jadvali bilan qayta urinish) va `@Externalized` orqali eventni brokerga chiqarish. Servislar orasida `KafkaTemplate`/`RabbitTemplate` bilan yupqa event yuborilib, detallar `RestClient`, `WebClient` yoki gRPC chaqiruvi bilan olinadi; CloudEvents formati `spring-cloud-function`/Spring for Apache Kafka bilan ishlatiladi.

```java
@Transactional
public void confirm(Order order) {
    order.confirm();
    events.publishEvent(new OrderConfirmed(order.getId())); // faqat ID
}

@ApplicationModuleListener
void on(OrderConfirmed event) {
    OrderView fresh = orderClient.fetch(event.orderId()); // detallar uchun so'rov
    invoicing.create(fresh);
}
```

**Qo'llanish keyslari:**
- `OrderConfirmed(orderId)` eventidan keyin invoicing service buyurtma detallarini REST bilan o'qishi.
- Katta payload'li agregatlar uchun eventni kichik ushlab, broker trafigini kamaytirish.
- Maxfiy ma'lumot (PII, karta) brokerdan o'tmasligi talab qilinganda faqat ID uzatish.
- Consumer'lar turli xil ma'lumot kesimiga muhtoj bo'lganda, har biri o'ziga kerakli projection'ni so'rab olishi.
- Cache invalidation: "bu ID o'zgardi" signali bilan local cache entry'ni bo'shatish.

**Ehtiyot bo'ling:** Asosiy tuzoq - race condition va vaqt mosligi: consumer callback qilganda manba allaqachon yangi holatga o'tgan bo'lishi mumkin, shuning uchun event ichida versiya/timestamp bo'lishi va consumer "kutilganidan yangi" ma'lumotni to'g'ri qabul qilishi kerak. Ikkinchi xavf - availability bog'liqligi: har bir event endi sinxron callback'ni talab qiladi, shuning uchun publisher o'chsa consumer ham ishlamay qoladi; yuqori throughput yoki temporal decoupling muhim bo'lsa, Event-Carried State Transfer tanlanadi.

## 16.27 Holat ko'chiruvchi event (Event-Carried State Transfer)

**Tavsif:** Consumer har safar producer'ning API'siga sinxron so'rov yubormasligi uchun event ichiga o'zgargan domen obyektining holatini (yoki uning muhim qismini) solib yuboriladi. Consumer bu holatni o'zining local read model'ida saqlaydi va so'rovlarga mustaqil javob beradi - bu temporal coupling'ni yo'q qiladi va producer o'chganda ham consumer ishlashda davom etadi. Buning narxi - ma'lumot dublikatsiyasi va eventual consistency. Odatda "Notification event" (faqat ID) bilan solishtirib tanlanadi: notification kichik, lekin callback so'rovlar to'lqinini keltiradi.

**Spring'da qayerda uchraydi:** Event payload'i `record CustomerUpdated(UUID id, String name, String tier, long version)` ko'rinishidagi Java 17+ record sifatida modellashtiriladi va `KafkaTemplate<String, CustomerUpdated>` orqali `JsonSerializer` yoki `KafkaAvroSerializer` bilan yuboriladi. Consumer tomonda `@KafkaListener` holatni Spring Data JPA/Redis repository'siga `save()` qiladi (upsert). Spring Modulith'ning `@ApplicationModuleListener` va `spring-modulith-events-kafka` moduli domen event'ini tashqi event'ga externalize qilish uchun `@Externalized("customer.updated::#{#this.id()}")` annotatsiyasini beradi. Local replica uchun ko'pincha `@Version` (optimistic locking) yoki event'dagi `version` maydoni bilan stale update'lar filtrlanadi.

**Qo'llanish keyslari:**
- Order service mijozning nomi va manzilini Customer service'ga REST so'rov yubormasdan local keshida saqlaydi.
- Katalog narxlari va mahsulot nomlari e-commerce frontend BFF'ida replica sifatida turadi, chunki katalog servisi tez-tez deploy bo'ladi.
- Pricing service valyuta kurslarini event sifatida qabul qilib, hisob-kitobni tashqi chaqiruvsiz bajaradi.
- Reporting/analytics servisi operatsion bazaga join qilmasdan, event'lardan yig'ilgan denormalizatsiyalangan jadval ustida ishlaydi.
- Mobil push servisi foydalanuvchi til va timezone sozlamalarini local nusxada ushlaydi, chunki profile servisi SLA'si pastroq.

**Ehtiyot bo'ling:** Payload kattalashib ketsa (butun aggregate har o'zgarishda) topic throughput va retention xarajati keskin oshadi, shuningdek PII'ni keraksiz servislarga tarqatib yuborish xavfi paydo bo'ladi (GDPR). Agar consumer doim eng so'nggi, qat'iy aktual holatni talab qilsa (masalan balans tekshiruvi to'lov oldidan), bu pattern mos emas - stale replica bilan noto'g'ri qaror qabul qiladi.

## 16.28 Event Sourcing (messaging nuqtai nazaridan) (Event Sourcing (messaging view))

**Tavsif:** Aggregate'ning hozirgi holati jadvalda emas, balki o'zgarishlar ketma-ketligi - immutable event'lar log'i sifatida saqlanadi; holat esa event'larni qayta o'ynatib (replay) tiklanadi. Messaging kontekstida event store ham yozuv manbai, ham integratsiya kanali bo'lib xizmat qiladi: bir xil event'lar projection'larni (CQRS read model) qurish uchun ham, boshqa servislarga tarqatish uchun ham ishlatiladi. Bu to'liq audit tarixi, vaqt bo'yicha "orqaga qaytish" va yangi projection'ni noldan qurish imkonini beradi.

**Spring'da qayerda uchraydi:** Spring Framework'da standart event store yo'q, shuning uchun Axon Framework (`axon-spring-boot-starter`, `@Aggregate`, `@CommandHandler`, `@EventSourcingHandler`, `@EventHandler`, `AggregateLifecycle.apply()`) yoki EventStoreDB'ning Java client'i bilan ishlatiladi. Oddiy variantda event'lar PostgreSQL'dagi `events` jadvaliga `@Entity` sifatida append-only yoziladi, optimistic concurrency `(aggregate_id, sequence_number)` unique constraint bilan ta'minlanadi, so'ng Transactional Outbox (Debezium yoki Spring Modulith event publication registry) orqali Kafka'ga chiqariladi. Projection'lar `@KafkaListener` yoki Axon'ning `@EventHandler` + `TrackingEventProcessor` orqali quriladi; replay uchun `EventProcessor.resetTokens()` ishlatiladi.

**Qo'llanish keyslari:**
- Bank hisobidagi har bir debet/kredit operatsiyasi event sifatida saqlanib, balans replay bilan hisoblanadi va regulyator uchun to'liq audit trail bo'ladi.
- Buyurtma holati tarixini ("qachon kim bekor qildi") biznes talabi sifatida saqlash zarur bo'lgan order management tizimi.
- Insurance polislarida har bir endorsement/o'zgartirish tarixi saqlanib, istalgan sanadagi polis holati tiklanadi.
- Yangi analitik projection (masalan "mijoz yo'qotish voronkasi") mavjud event log'dan noldan qayta qurildi.
- Murakkab biznes bug'idan keyin event'larni qayta o'ynatib, tuzatilgan logika bilan to'g'ri holat tiklanadi.

**Ehtiyot bo'ling:** Event schema migratsiyasi eng og'ir muammo - 5 yil oldingi event'lar ham o'qilishi kerak, shuning uchun upcasting qatlami va event versiyalash majburiy; "oddiy CRUD"ga Event Sourcing qo'yish loyihani asossiz murakkablashtiradi. GDPR "o'chirish huquqi" immutable log bilan ziddiyatga kiradi, buni crypto-shredding (kalitni yo'q qilish) kabi maxsus yechimlar bilan hal qilish kerak.

**Tavsiya:** Event Sourcing'ni faqat tarix o'zi biznes qiymatiga ega bo'lgan bounded context'larga qo'llang, butun tizimga emas.

## 16.29 CloudEvents (CloudEvents)

**Tavsif:** CloudEvents - CNCF'ning event metadata'sini standartlashtiruvchi spetsifikatsiyasi: `id`, `source`, `type`, `specversion`, `subject`, `time`, `datacontenttype`, `data` kabi umumiy atributlar to'plamini belgilaydi. Bu turli broker'lar (Kafka, RabbitMQ, HTTP webhook, cloud pub/sub) va turli tillardagi servislar o'rtasida event'ni bir xil tushunish, routing va tracing qilish imkonini beradi. Binary mode'da atributlar transport header'lariga (`ce_type`, `ce_source`), structured mode'da esa butun event JSON sifatida body'ga joylanadi.

**Spring'da qayerda uchraydi:** Rasmiy `io.cloudevents:cloudevents-core` va binding'lar: `cloudevents-kafka` (`CloudEventSerializer`/`CloudEventDeserializer`, `KafkaMessageFactory`), `cloudevents-http-basic`, `cloudevents-spring` (`CloudEventHttpMessageConverter`, Spring WebFlux/MVC uchun `CloudEventMessageConverter`). Spring Cloud Function va Spring Cloud Stream CloudEvents'ni first-class qo'llab-quvvatlaydi - funksiya `Message<T>` qabul qilganda header'lar `ce-` prefiksi bilan keladi. Knative Eventing va Azure Event Grid integratsiyalarida Spring Boot 3.x ilovasi uchun de-fakto standart format shu.

**Qo'llanish keyslari:**
- Polyglot muhitda (Java, Go, Python servislari) bitta Kafka topic'ni bir xil envelope bilan o'qish.
- Knative Eventing yoki Azure Event Grid'ga Spring Boot servisidan event yuborish.
- `ce_type` header'i bo'yicha broker darajasida routing va content-based filtering qilish.
- `traceparent` extension atributi orqali event'lar bo'ylab distributed tracing uzilmasligini ta'minlash.
- Tashqi SaaS hamkorlarga webhook chiqarishda bir xil, hujjatlashtirilgan event formatini kafolatlash.

**Ehtiyot bo'ling:** CloudEvents faqat envelope'ni standartlashtiradi - `data` ichidagi payload schema'si va uning evolyutsiyasi hamon sizning javobingizda, shuning uchun uni Schema Registry bilan birga ishlatish kerak. Structured mode'da header'lardan filtrlash mumkin bo'lmaydi, shuning uchun Kafka'da odatda binary mode afzal.

## 16.30 Kafka Consumer Group (Kafka: Consumer Group)

**Tavsif:** Consumer Group - bitta `group.id` bilan birlashgan consumer'lar to'plami bo'lib, topic partition'lari ular orasida taqsimlanadi: har bir partition bir vaqtda faqat bitta group a'zosiga tegishli bo'ladi. Bu Competing Consumers patterni'ni gorizontal masshtablash bilan amalga oshiradi va offset'lar group darajasida `__consumer_offsets` topic'ida saqlanadi, shuning uchun qayta ishga tushganda ish joyidan davom etadi. A'zo qo'shilsa yoki yo'qolsa rebalance bo'ladi; turli `group.id` esa Publish-Subscribe semantikasini beradi - har bir group barcha xabarlarning nusxasini oladi.

**Spring'da qayerda uchraydi:** `spring.kafka.consumer.group-id` property yoki `@KafkaListener(topics = "orders", groupId = "order-processor", concurrency = "3")`. `concurrency` har biri alohida thread'da ishlaydigan `KafkaMessageListenerContainer`lar sonini belgilaydi (partition sonidan oshirish befoyda). `ConcurrentKafkaListenerContainerFactory`, `ContainerProperties.AckMode.RECORD`/`BATCH`/`MANUAL_IMMEDIATE` offset commit strategiyasini boshqaradi; `KafkaAdmin` va `AdminClient` orqali group lag monitoring qilinadi. Kafka 3.x'dagi cooperative-sticky assignor (`partition.assignment.strategy`) stop-the-world rebalance'ni kamaytiradi.

**Qo'llanish keyslari:**
- Buyurtma ishlovchi servisni 6 pod'ga masshtablab, 12 partition'ni ular orasida avtomatik taqsimlash.
- Bir xil `orders` topic'ini alohida `group.id` bilan analytics, notification va fraud servislariga mustaqil o'qitish.
- Blue-green deploy'da yangi versiya eski group'dan offset meros qilib olib, ishni to'xtatmasdan davom ettirish.
- Consumer lag metrikasi bo'yicha KEDA/HPA orqali avtomatik scale qilish.
- Batch rejimida ishlaydigan ETL consumer'ini kechasi ko'proq instance bilan ishga tushirib lag'ni yopish.

**Ehtiyot bo'ling:** Partition soni consumer parallelizmining qat'iy yuqori chegarasi - partition'dan ko'p consumer ishga tushirsa, qolganlari bo'sh (idle) turadi. `max.poll.interval.ms` ichida `poll()` qaytmasa, broker consumer'ni o'lgan deb hisoblab rebalance qiladi va xabar qayta ishlanadi, shuning uchun uzoq davom etadigan ishni listener thread'ida bajarmang.

## 16.31 Partition kaliti bo'yicha tartib (Kafka: Partition key ordering)

**Tavsif:** Kafka xabarlarning tartibini faqat bitta partition ichida kafolatlaydi, global emas. Producer xabarga key berganda, `murmur2(key) % numPartitions` formulasi bo'yicha partition tanlanadi, shuning uchun bir xil key'li barcha xabarlar bir partition'ga tushadi va yozilgan tartibda o'qiladi. Shu tufayli biznes aggregate ID'sini (orderId, accountId, customerId) key sifatida tanlash - bir aggregate ichida qat'iy tartib, aggregate'lar orasida esa to'liq parallelizm beradi.

**Spring'da qayerda uchraydi:** `kafkaTemplate.send("orders", order.id().toString(), event)` yoki `ProducerRecord` bilan aniq partition/key berish; custom logika uchun `partitioner.class` (`org.apache.kafka.clients.producer.Partitioner`) implementatsiyasi. Spring Cloud Stream'da `spring.cloud.stream.bindings.output.producer.partition-key-expression=payload.customerId` yoki `partitionKeyExtractorName` bean'i ishlatiladi. Idempotent producer (`enable.idempotence=true`, Kafka 3.x'da default) `max.in.flight.requests.per.connection<=5` bilan retry paytida ham partition ichida tartibni saqlaydi.

**Qo'llanish keyslari:**
- Bitta buyurtma uchun `CREATED → PAID → SHIPPED` event'lari consumer'ga to'g'ri ketma-ketlikda yetib boradi.
- CDC (Debezium) oqimida bir qatorning `UPDATE` tarixi primary key bo'yicha tartibda qoladi.
- Hisob balansi o'zgarishlari `accountId` key bilan bir partition'da ketma-ket qayta ishlanadi.
- IoT qurilma telemetriyasi `deviceId` bo'yicha tartiblanib, oldingi o'lchov keyingisini bosib ketmaydi.
- Kafka Streams'da `groupByKey().aggregate()` uchun co-partitioning talabi bajariladi.

**Ehtiyot bo'ling:** Key taqsimoti nomutanosib bo'lsa (masalan 90% trafik bitta yirik mijozga tegishli) "hot partition" paydo bo'ladi va bitta consumer thread butun oqimni ushlab qoladi. Partition sonini keyinchalik oshirish mavjud key→partition moslashuvini buzadi, ya'ni eski va yangi xabarlar turli partition'larga tushib tartib kafolati yo'qoladi - shuning uchun partition sonini boshidan yetarli qilib rejalashtiring.

## 16.32 Compacted topic (Kafka: Compacted topic)

**Tavsif:** `cleanup.policy=compact` bo'lgan topic'da Kafka har bir key uchun kamida eng so'nggi qiymatni saqlab, undan oldingi nusxalarni fonda tozalab yuboradi. Natijada topic cheksiz o'sadigan log'dan "key→so'nggi holat" ko'rinishidagi, qayta o'ynatiladigan snapshot'ga aylanadi - bu changelog va konfiguratsiya tarqatish uchun ideal. `null` qiymatli xabar (tombstone) key'ni o'chirilgan deb belgilaydi va `delete.retention.ms` o'tgach butunlay yo'qotiladi.

**Spring'da qayerda uchraydi:** Topic'ni `@Bean NewTopic` + `TopicBuilder.name("customer-state").partitions(6).replicas(3).config(TopicConfig.CLEANUP_POLICY_CONFIG, TopicConfig.CLEANUP_POLICY_COMPACT).build()` bilan yaratish (`KafkaAdmin` avtomatik qo'llaydi). Kafka Streams'ning `KTable` va state store'lari ichki changelog topic'larini aynan compacted qilib yaratadi; `spring-kafka`da `StreamsBuilderFactoryBean` va `@EnableKafkaStreams` orqali `builder.table("customer-state", Consumed.with(...))` ishlatiladi. GlobalKTable esa barcha instance'larda to'liq nusxani ushlab, local lookup beradi.

**Qo'llanish keyslari:**
- Mijoz profillarining so'nggi holatini saqlab, yangi servis instance'i ishga tushganda local keshni to'liq to'ldirish.
- Feature flag yoki tariff konfiguratsiyasini barcha pod'larga `GlobalKTable` sifatida tarqatish.
- Kafka Streams aggregation state store'ining fault-tolerant changelog'i.
- Valyuta kurslari/narx jadvalining oxirgi qiymatlarini lookup topic sifatida ushlash.
- Debezium CDC snapshot + stream natijasini jadval ko'rinishida saqlash.

**Ehtiyot bo'ling:** Compaction event tarixini yo'q qiladi - audit yoki Event Sourcing log'i uchun uni ishlatmang (yoki `compact,delete` emas, alohida retention topic qo'ying). Key `null` bo'lgan xabarlar compacted topic'da mantiqsiz, tombstone'larni esa consumer kodi aniq ravishda `payload == null` holati sifatida ishlashi kerak - aks holda keshda o'chirilgan yozuvlar abadiy qoladi.

## 16.33 Exactly-once va tranzaksion producer (Kafka: Exactly-once / transactional producer)

**Tavsif:** Kafka tranzaksiyalari bir nechta topic/partition'ga yozishni va consumer offset commit'ini bitta atomik blokka birlashtiradi, shu bilan "read-process-write" oqimida exactly-once semantikasini (EOS) beradi. Producer `transactional.id` bilan ro'yxatdan o'tadi, broker epoch orqali zombie instance'larni to'sadi; consumer `isolation.level=read_committed` bo'lsa, abort qilingan tranzaksiya xabarlarini ko'rmaydi. Muhimi: bu kafolat faqat Kafka ichida amal qiladi, tashqi tizim (DB, HTTP) bilan birgalikda emas.

**Spring'da qayerda uchraydi:** `spring.kafka.producer.transaction-id-prefix=tx-` berilsa, Spring Boot `KafkaTransactionManager` bean'ini yaratadi va `KafkaTemplate` tranzaksion bo'ladi; `kafkaTemplate.executeInTransaction(...)` yoki `@Transactional` metod ichida `send()` ishlatiladi. Listener container'da `ContainerProperties.setKafkaAwareTransactionManager(...)` offset'ni producer tranzaksiyasiga qo'shadi. DB bilan birga ishlatilsa `ChainedKafkaTransactionManager` o'rniga (u deprecated) Transactional Outbox pattern tavsiya etiladi; Kafka Streams'da esa `processing.guarantee=exactly_once_v2` yetarli.

```java
@Transactional("kafkaTransactionManager")
@KafkaListener(topics = "payments")
public void onPayment(PaymentEvent e) {
    kafkaTemplate.send("ledger", e.accountId(), toLedgerEntry(e));
    kafkaTemplate.send("audit", e.id(), toAudit(e));
}
```

**Qo'llanish keyslari:**
- Bir event'dan ikki topic'ga (ledger va audit) atomik yozish, qismiy natija qolmasligi uchun.
- Kafka Streams'da to'lov summalarini agregatlashda dublikat hisoblashni butunlay yo'qotish.
- Fan-out router bir kiruvchi xabardan N chiquvchi xabar yaratganda hammasi yoki hech biri yozilishi.
- Reprocessing/backfill job'ida qayta ishga tushirish dublikat yaratmasligini kafolatlash.
- Moliyaviy hisob-kitob pipeline'ida `read_committed` consumer'lar bilan toza, yarim tayyor ma'lumotsiz oqim.

**Ehtiyot bo'ling:** Tranzaksiyalar throughput'ni pasaytiradi va latency'ni oshiradi (ayniqsa kichik tranzaksiyalarda commit overhead'i katta), shuningdek `read_committed` consumer'lar LSO (last stable offset) tufayli qo'shimcha kechikish ko'radi. Eng keng tarqalgan xato - EOS'ni "DB + Kafka atomik" deb tushunish: ikki fazali kafolat yo'q, shuning uchun idempotent consumer va Outbox patterni'ni baribir qurish kerak.

## 16.34 Schema Registry va schema evolyutsiyasi (Schema Registry & schema evolution)

**Tavsif:** Schema Registry - Avro/Protobuf/JSON Schema'larni markazlashgan saqlash va versiyalash servisi: producer schema'ni ro'yxatdan o'tkazadi, xabar payload'iga faqat kichik schema ID qo'shiladi, consumer esa ID bo'yicha schema'ni olib deserializatsiya qiladi. Registry moslik qoidalarini (`BACKWARD`, `FORWARD`, `FULL`, `*_TRANSITIVE`) majburlaydi, shuning uchun buzuvchi o'zgarish CI/CD yoki publish bosqichida darhol rad etiladi. Bu event'larni servislar orasidagi rasmiy kontraktga aylantiradi va "men maydonni o'chirdim, 6 ta consumer sindi" muammosini oldini oladi.

**Spring'da qayerda uchraydi:** Confluent Schema Registry bilan `io.confluent:kafka-avro-serializer` (`KafkaAvroSerializer`/`KafkaAvroDeserializer`, `specific.avro.reader=true`) yoki `KafkaProtobufSerializer`; `spring.kafka.properties.schema.registry.url` orqali konfiguratsiya qilinadi. Avro sinflari `avro-maven-plugin`/`gradle-avro-plugin` bilan `.avsc` fayldan generatsiya qilinadi, moslik tekshiruvi esa `kafka-schema-registry-maven-plugin`ning `test-compatibility` goal'i bilan build'da bajariladi. Apicurio Registry ham shu rolni bajaradi (`apicurio-registry-serdes-avro-serde`); Spring Cloud Stream'da `spring-cloud-stream-schema-registry-client` mavjud, lekin yangi loyihalarda to'g'ridan-to'g'ri Confluent/Apicurio serde'lari afzal.

**Qo'llanish keyslari:**
- Yangi ixtiyoriy maydon qo'shishni `BACKWARD` moslik bilan xavfsiz deploy qilish, consumer'larni oldin yangilamasdan.
- CI pipeline'da schema o'zgarishini merge'dan oldin avtomatik tekshirib, buzuvchi PR'ni blokirovka qilish.
- Polyglot consumer'lar (Java, Python, .NET) uchun bitta rasmiy event kontraktini e'lon qilish.
- Avro binary format bilan JSON'ga nisbatan topic hajmi va tarmoq trafigini sezilarli kamaytirish.
- Event Sourcing log'ida eski versiyali event'larni upcasting bilan o'qish uchun schema tarixini saqlash.

**Ehtiyot bo'ling:** Registry yagona nuqtali nosozlikka (SPOF) aylanishi mumkin - uni HA qilib, client'larda schema keshini (`max.schemas.per.subject`) hisobga olish kerak. `BACKWARD` moslik faqat ixtiyoriy, default qiymatli maydonlarni qo'shishga ruxsat beradi; majburiy maydon qo'shish yoki maydon turini o'zgartirish esa yangi topic yoki `v2` event turini talab qiladi.

## 16.35 Retry topic va Dead Letter Topic (Retry topic / Dead Letter Topic (Spring Kafka))

**Tavsif:** Vaqtinchalik xato (network timeout, downstream 503) bo'lganda xabarni darhol tashlab yubormasdan, uni kechikish bilan qayta urinish uchun alohida retry topic'ga yuboriladi; urinishlar tugagach xabar Dead Letter Topic'ga (DLT) ko'chiriladi va asosiy oqim bloklanmaydi. Non-blocking retry'da kutish consumer thread'ida emas, alohida topic'da sodir bo'ladi, shuning uchun partition'dagi keyingi xabarlar to'xtab qolmaydi. Doimiy xatolar (validation, deserialization) esa umuman retry qilinmasligi kerak - ular to'g'ridan-to'g'ri DLT'ga ketadi.

**Spring'da qayerda uchraydi:** `@RetryableTopic(attempts = "4", backoff = @Backoff(delay = 1000, multiplier = 2.0), dltStrategy = DltStrategy.FAIL_ON_ERROR, exclude = ValidationException.class)` annotatsiyasi `@KafkaListener` ustiga qo'yiladi va `orders-retry-0`, `orders-retry-1`, `orders-dlt` topic'larini avtomatik yaratadi; `@DltHandler` metodi DLT xabarlarini qabul qiladi. Blocking variant uchun `DefaultErrorHandler` + `FixedBackOff`/`ExponentialBackOffWithMaxRetries` va `DeadLetterPublishingRecoverer` ishlatiladi; `addNotRetryableExceptions(...)` bilan doimiy xatolar ajratiladi. Deserialization xatolari uchun `ErrorHandlingDeserializer` (`DeserializationException` header'ga joylanadi) majburiy, aks holda poison pill cheksiz loop keltiradi.

**Qo'llanish keyslari:**
- Downstream REST API vaqtincha 503 qaytarganda exponential backoff bilan qayta urinish.
- Buzilgan (non-deserializable) poison pill xabarni DLT'ga olib chiqib, consumer loop'ini to'xtab qolishdan saqlash.
- DLT hajmi bo'yicha alert qo'yib, SRE jamoasini integratsiya nosozligidan xabardor qilish.
- DLT'dagi xabarlarni tuzatilgandan keyin asosiy topic'ga qayta yuborish (replay) operatorlik vositasi.
- Partner API'ning rate limit'iga tushib qolgan xabarlarni kechiktirib, asosiy oqimni bloklamasdan qayta ishlash.

**Ehtiyot bo'ling:** Non-blocking retry xabar tartibini buzadi - bir aggregate uchun qat'iy ketma-ketlik talab qilinsa (`orderId` bo'yicha tartib), retry topic'lar o'rniga blocking retry yoki partition'ni pauza qilish kerak. DLT'ni monitoring va qayta ishlash protsedurasi bo'lmasa, u shunchaki yo'qolgan ma'lumotlar qabristoniga aylanadi.

## 16.36 Spring Integration DSL moslashuvi (Spring Integration DSL mapping)

**Tavsif:** Spring Integration - EIP kitobidagi patternlarning to'g'ridan-to'g'ri Java implementatsiyasi: `MessageChannel`, `MessageHandler`, `Transformer`, `Router`, `Filter`, `Splitter`, `Aggregator` komponentlari o'zaro xabar almashuv orqali oqim quradi. Java DSL (`IntegrationFlow`) bu oqimni fluent, tipli va kompilyatsiya vaqtida tekshiriladigan ko'rinishda yozishga imkon beradi, XML konfiguratsiyasiga ehtiyoj qolmaydi. Natija - pattern nomlari kod ichida ko'rinib turadigan, deklarativ integratsiya qatlami.

**Spring'da qayerda uchraydi:** `spring-boot-starter-integration`, `@EnableIntegration`, `IntegrationFlow`/`IntegrationFlows` (6.x'da `IntegrationFlow.from(...)` statik factory), `@Bean IntegrationFlow` deklaratsiyasi. Kanal turlari: `MessageChannels.direct()`, `.queue()`, `.publishSubscribe()`, `.executor()`, `.flux()`. Adapter'lar alohida modullarda: `spring-integration-file` (`Files.inboundAdapter`), `spring-integration-kafka`, `spring-integration-amqp`, `spring-integration-jdbc`, `spring-integration-http`, `spring-integration-mail`. `@ServiceActivator`, `@Transformer`, `@Router`, `@Splitter`, `@Aggregator`, `@MessagingGateway` annotatsiyalari ham mavjud; `.handle(...)` va `.wireTap(...)` bilan monitoring qo'shiladi.

```java
@Bean
IntegrationFlow orderFlow(OrderService svc) {
    return IntegrationFlow.from(Kafka.messageDrivenChannelAdapter(cf, "orders"))
        .transform(Transformers.fromJson(OrderEvent.class))
        .filter((OrderEvent e) -> e.amount() > 0)
        .route(OrderEvent::region, m -> m.subFlowMapping("EU", f -> f.handle(svc::handleEu)))
        .get();
}
```

**Qo'llanish keyslari:**
- Legacy tizim bilan fayl almashinuvi: SFTP'dan fayl olish, parse qilish, split qilib Kafka'ga yuborish.
- Bir nechta manbadan kelgan xabarlarni normalize qilib, yagona canonical formatga transformatsiya qilish.
- Content-based router bilan hujjat turiga qarab turli handler'larga yo'naltirish.
- `@MessagingGateway` orqali oddiy Java interfeysi ortida butun integratsiya oqimini yashirish.
- Aggregator bilan bitta buyurtmaga tegishli N ta qismni yig'ib, to'liq bo'lgach keyingi bosqichga uzatish.

**Ehtiyot bo'ling:** Spring Integration murakkab oqimlarda debug qilish va kuzatish qiyin bo'lishi mumkin - oddiy "Kafka'dan o'qib, DB'ga yoz" vazifasi uchun `@KafkaListener` yetarli, DSL'ni asossiz tortish ortiqcha abstraksiya qo'shadi. `DirectChannel` chaqiruvchi thread'da sinxron ishlaydi, shuning uchun uni haqiqiy asinxronlik deb hisoblash xato - buning uchun `ExecutorChannel` yoki `QueueChannel` kerak.

## 16.37 Spring Cloud Stream binder abstraksiyasi (Spring Cloud Stream binder abstraction)

**Tavsif:** Spring Cloud Stream biznes logikani broker'dan ajratadi: siz `java.util.function.Function`, `Consumer` yoki `Supplier` bean'ini yozasiz, framework esa uni binder orqali Kafka, RabbitMQ, Kinesis yoki Pub/Sub'ga ulaydi. Binding konfiguratsiya bilan boshqarilganidan, broker'ni almashtirish (yoki test uchun in-memory'ga o'tish) kodga tegmasdan amalga oshadi. Shu bilan birga framework serializatsiya, partitioning, consumer group, DLQ va retry'ni yagona, broker-neutral property modeli ostida beradi.

**Spring'da qayerda uchraydi:** `spring-cloud-stream` + binder: `spring-cloud-stream-binder-kafka`, `-binder-rabbit`, `-binder-kafka-streams`. Funksional model: `@Bean Function<OrderEvent, ShipmentEvent> process()` va `spring.cloud.function.definition=process`, binding nomlari `process-in-0` / `process-out-0`. Muhim property'lar: `spring.cloud.stream.bindings.process-in-0.group`, `...consumer.max-attempts`, `...consumer.dlq-name` (Rabbit) yoki `spring.cloud.stream.kafka.bindings.process-in-0.consumer.enableDlq`, `...producer.partition-count`. Imperativ yuborish uchun `StreamBridge.send("orders-out-0", payload)`; test uchun `spring-cloud-stream-test-binder` (`InputDestination`, `OutputDestination`).

**Qo'llanish keyslari:**
- Bir xil ishlov logikasini dev muhitda RabbitMQ, prod'da Kafka bilan ishga tushirish.
- Event-driven mikroservislarni `Function` bean'lari sifatida yozib, broker boilerplate'ini butunlay yo'q qilish.
- `spring-cloud-stream-test-binder` bilan broker ko'tarmasdan integratsiya testlari yozish.
- Kafka Streams binder orqali `KStream`/`KTable` topologiyasini Boot konfiguratsiyasi bilan boshqarish.
- Funksiya kompozitsiyasi (`validate|enrich|publish`) bilan bir nechta qadamni bitta binding'da birlashtirish.

**Ehtiyot bo'ling:** Abstraksiya "leaky" - broker'ning o'ziga xos imkoniyatlari (Kafka tranzaksiyalari, aniq offset boshqaruvi, Rabbit'ning quorum queue sozlamalari) kerak bo'lganda baribir `spring.cloud.stream.kafka.*` yoki native API'ga tushishga to'g'ri keladi, shuning uchun "broker'ni oson almashtiramiz" va'dasiga haddan tashqari ishonmang. Agar loyiha bir umr Kafka'da qolsa, to'g'ridan-to'g'ri `spring-kafka` sodda va shaffofroq bo'ladi.

## 16.38 JMS va AMQP moslashuvi (JMS / AMQP mapping (Spring JMS, Spring AMQP))

**Tavsif:** JMS (ActiveMQ Artemis, IBM MQ) va AMQP (RabbitMQ) broker'lari queue/topic modeli bilan Point-to-Point va Publish-Subscribe patternlarini, shuningdek transactional consume, message priority, TTL va server-side DLQ'ni beradi - bu Kafka'dagi log modelidan jiddiy farq qiladi. AMQP'da routing broker ichida exchange (`direct`, `topic`, `fanout`, `headers`) va binding key orqali amalga oshadi, ya'ni Message Router pattern infratuzilma darajasida konfiguratsiya qilinadi. Spring bu ikki transportni bir xil uslubdagi template + listener container abstraksiyasi bilan yopadi.

**Spring'da qayerda uchraydi:** JMS: `spring-boot-starter-artemis`/`spring-jms`, `JmsTemplate`, `@JmsListener`, `@EnableJms`, `DefaultJmsListenerContainerFactory`, `JmsMessageConverter` (`MappingJackson2MessageConverter`), `JmsTransactionManager`, `spring.jms.listener.session.acknowledge-mode`. AMQP: `spring-boot-starter-amqp`, `RabbitTemplate`, `@RabbitListener`, `@EnableRabbit`, `RabbitAdmin` va `@Bean Queue/TopicExchange/Binding` deklaratsiyalari, `SimpleRabbitListenerContainerFactory` yoki `DirectRabbitListenerContainerFactory`, `Jackson2JsonMessageConverter`, `RabbitTransactionManager`, publisher confirms (`spring.rabbitmq.publisher-confirm-type=correlated`) va `spring.rabbitmq.listener.simple.default-requeue-rejected=false` + DLX konfiguratsiyasi. `RabbitTemplate.convertSendAndReceive(...)` Request-Reply'ni to'g'ridan-to'g'ri qo'llab-quvvatlaydi.

**Qo'llanish keyslari:**
- Legacy IBM MQ yoki Artemis bilan integratsiya qilingan korporativ tizimlarga Spring Boot servisini ulash.
- Har bir xabarga alohida ack/nack va per-message retry kerak bo'lgan task queue (hisobot generatsiyasi, email yuborish).
- Priority queue bilan shoshilinch buyurtmalarni oddiylaridan oldin ishlash.
- RabbitMQ topic exchange bilan `order.*.created` kabi pattern bo'yicha fan-out routing.
- Delayed message plugin yoki TTL + DLX kombinatsiyasi bilan kechiktirilgan retry mexanizmini qurish.

**Ehtiyot bo'ling:** Bu broker'larda xabar iste'mol qilingach o'chadi - Kafka'dagidek replay yoki yangi consumer group bilan tarixni qayta o'qish imkoniyati yo'q, shuning uchun Event Sourcing yoki analytics backfill uchun ularni tanlamang. `default-requeue-rejected=true` (default) bo'lsa, xato bergan xabar cheksiz requeue loop'iga tushib CPU'ni yeb qo'yadi - DLX'ni albatta sozlang; shuningdek `JmsTemplate`ning har `send()`da connection/session yaratish xususiyati tufayli `CachingConnectionFactory` ishlatish majburiy.

## 16.39 Log siqilishi (Log Compaction)

**Tavsif:** Log Compaction - bu append-only logda har bir kalit uchun faqat eng oxirgi qiymatni saqlab, undan avvalgi yozuvlarni fonda olib tashlash strategiyasi. Natijada log cheksiz o'smaydi, lekin unda har doim butun holatning to'liq "oxirgi tasviri" (snapshot) qoladi, ya'ni log ham event oqimi, ham jadval (table) bo'lib xizmat qiladi. Kalitni o'chirish uchun qiymati `null` bo'lgan tombstone yozuv yuboriladi. Bu retention vaqt yoki hajm bo'yicha emas, kalit bo'yicha ishlaydi, shuning uchun yangi consumer nolda boshlab to'liq holatni tiklay oladi.

**Spring'da qayerda uchraydi:** Bu pattern Apache Kafka broker darajasida amalga oshiriladi - topic konfiguratsiyasidagi `cleanup.policy=compact`, `min.cleanable.dirty.ratio`, `delete.retention.ms` va `segment.ms` parametrlari orqali; Spring'ning o'zida bunday mexanizm yo'q. Spring Boot 3.x ilovasi bunga `spring-kafka` va `KafkaAdmin` bean'i orqali `TopicBuilder.name("customer-state").partitions(6).replicas(3).config(TopicConfig.CLEANUP_POLICY_CONFIG, TopicConfig.CLEANUP_POLICY_COMPACT).build()` ko'rinishida topic'ni deklarativ yaratib tayanadi. Iste'mol tomonida Spring for Apache Kafka'ning `@KafkaListener`'i yoki Spring Cloud Stream Kafka Streams binder'i ichida `StreamsBuilder.globalTable(...)` / `KTable` ishlatiladi - Kafka Streams'ning `KTable` va `GlobalKTable` abstraksiyalari aynan compacted topic ustiga qurilgan va RocksDB'dagi state store'ni to'ldiradi. Tombstone'ni Spring'da yuborish uchun `KafkaTemplate.send(topic, key, null)` chaqiriladi, `ConsumerRecord.value()` esa `null` bo'lib keladi (shu sababli listener metodida `@Payload(required = false)` yoki `ConsumerRecord` parametri kerak bo'ladi).

**Qo'llanish keyslari:**
- Mijoz profili yoki narx jadvalining oxirgi holatini saqlovchi `customer-profile` topic'i, undan yangi mikroservislar to'liq cache'ni tiklaydi.
- Kafka Streams/KSQL'da reference data'ni `GlobalKTable` sifatida har bir instance xotirasiga yuklash va stream'ga join qilish.
- Kafka Connect va Debezium'ning CDC snapshot topic'lari, bunda har bir primary key uchun qatorning oxirgi versiyasi qoladi.
- Event sourcing tizimida "latest snapshot per aggregate" topic'i: hodisalar logi alohida, siqilgan holat topic'i alohida.
- Feature flag yoki konfiguratsiya tarqatish kanali: yangi pod ko'tarilganda nolinchi offsetdan o'qib barcha flaglarni oladi.

**Ehtiyot bo'ling:** Compaction faqat kalitlar soni cheklangan bo'lsa ma'noli - kalit sifatida UUID yoki timestamp ishlatsangiz, log hech qachon siqilmaydi va disk to'lib ketadi. Shuni ham unutmang: compaction kechikib ishlaydi va faqat passiv segmentlarga tegadi, ya'ni consumer bir kalit uchun bir nechta eski versiyani ham ko'rishi mumkin, demak bu "faqat bitta yozuv keladi" degan kafolat emas; tombstone'lar esa `delete.retention.ms` o'tgach butunlay yo'q bo'ladi, shuning uchun uzoq offline bo'lgan consumer o'chirilgan kalitni sezmay qolishi mumkin.

## 16.40 Aynan-bir-marta semantikasi (Exactly-Once Semantics)

**Tavsif:** Exactly-Once Semantics (EOS) - xabar qayta yuborilsa ham yoki ishlov beruvchi qulasa ham, uning effekti tizimda aynan bir marta kuzatilishini ta'minlash. Amalda bu "fizik jihatdan bir marta yetkazish" emas, balki idempotent producer (sequence number + producer ID), transactional read-process-write va `read_committed` isolation level kombinatsiyasidir: consumer offset va chiqish xabarlari bitta atomar transaksiyada commit qilinadi. Tashqi tizimlarga yozishda esa bu idempotency key yoki transactional outbox bilan ta'minlanadi.

**Spring'da qayerda uchraydi:** Spring for Apache Kafka'da `spring.kafka.producer.transaction-id-prefix` berilsa `KafkaTemplate` transactional bo'ladi va `KafkaTransactionManager` bean'i avtomatik yaratiladi; `@Transactional` bilan belgilangan `@KafkaListener` metodi ichidagi `kafkaTemplate.send(...)` chaqiruvlari offset bilan birga atomar commit qilinadi (`sendOffsetsToTransaction` ichda `KafkaResourceHolder` orqali bajariladi). Consumer tomonida `spring.kafka.consumer.isolation-level=read_committed` kerak. Kafka Streams'da bu `processing.guarantee=exactly_once_v2` (Spring Cloud Stream Kafka Streams binder yoki `KafkaStreamsConfiguration` orqali) bilan yoqiladi. DB + Kafka kombinatsiyasida haqiqiy XA yo'q, shuning uchun `ChainedTransactionManager` o'rniga (u Spring Data 2021.2'dan deprecated) Transactional Outbox yoki `JdbcTemplate` bilan idempotency jadvali tavsiya etiladi. RabbitMQ tomonida `RabbitTemplate` publisher confirms (`spring.rabbitmq.publisher-confirm-type=correlated`) va manual ack (`AcknowledgeMode.MANUAL`) bilan at-least-once + idempotent consumer yondashuvi qo'llanadi. Spring Integration'da takrorlarni filtrlash uchun `IdempotentReceiverInterceptor` va `MetadataStoreSelector` mavjud.

**Qo'llanish keyslari:**
- To'lov yoki hisob-kitob oqimi: bitta `PaymentAuthorized` eventi hisobdan ikki marta pul yechmasligi kerak.
- Kafka Streams bilan aggregatsiya: `count()`/`sum()` natijasi rebalance yoki qulashdan keyin ikki hisoblanmasligi uchun `exactly_once_v2`.
- Buyurtma holatini o'zgartiruvchi command handler: `Idempotency-Key` bo'yicha unique index va natijani qaytarish.
- ETL/CDC pipeline'da `read-process-write` zanjiri: kirish topic'dan o'qib, boyitib, chiqish topic'ga transaksiya ichida yozish.
- Email yoki SMS yuborish: takroriy delivery'ni oldini olish uchun yuborilgan xabar ID'si saqlanadigan dedup store.

**Ehtiyot bo'ling:** EOS faqat Kafka ichida (Kafka'dan Kafka'ga va offsetga) kafolat beradi - HTTP chaqiruvi, email yuborish yoki tashqi DB yozuvi transaksiyaga kirmaydi, shuning uchun u yerda idempotentlikni o'zingiz ta'minlashingiz kerak. Transactional producer throughput'ni pasaytiradi va latency'ni oshiradi (`transaction.timeout.ms`, `max.in.flight.requests`), noto'g'ri `transaction-id-prefix` (masalan, bir nechta instance'da bir xil prefiks) esa `ProducerFencedException`ga olib keladi; agar biznes allaqachon idempotent bo'lsa, oddiy at-least-once + dedup ko'pincha arzonroq va barqarorroq yechim.

## 16.41 Stream-jadval birlashtirish (Stream-Table Join)

**Tavsif:** Stream-Table Join cheksiz event oqimidagi har bir yozuvni o'zgarib turuvchi ma'lumotnoma holati (changelog'dan qurilgan jadval) bilan kalit bo'yicha boyitadi. Stream yozuvi kelganda joinni faqat stream tomoni "qo'zg'atadi" (trigger qiladi), jadval tomoni esa o'sha paytdagi eng oxirgi qiymatni beradi - bu klassik "ma'lumotni boyitish" (Content Enricher) pattern'ining oqim versiyasi. Shu sabab har bir event uchun tashqi servisga RPC qilish o'rniga lokal state store'dan o'qiladi, bu latency va tashqi yuklamani keskin kamaytiradi.

**Spring'da qayerda uchraydi:** Kafka Streams DSL'da `KStream.join(KTable, ValueJoiner)` (co-partitioning talab qiladi) yoki `KStream.join(GlobalKTable, KeyValueMapper, ValueJoiner)` (co-partitioning talab qilmaydi) orqali; Spring tomonida bu Spring Cloud Stream Kafka Streams binder'ida `java.util.function.BiFunction<KStream<K,V>, KTable<K,R>, KStream<K,O>>` bean'i sifatida yoziladi va `spring.cloud.stream.bindings.process-in-0/-in-1` bilan topic'larga bog'lanadi. Alternativ sifatida `StreamsBuilderFactoryBean` (spring-kafka) bilan `StreamsBuilder`ni to'g'ridan-to'g'ri ishlatish mumkin. Jadval tomoni odatda compacted topic ustiga qurilgan `KTable` bo'ladi, state store esa RocksDB'da yashaydi va `InteractiveQueryService` orqali so'rov qilinishi mumkin. Spring Integration yoki oddiy `@KafkaListener` ishlatilsa, "jadval" rolini Caffeine/Redis cache (`@Cacheable`, `RedisTemplate`) o'ynaydi - bu Kafka Streams bermaydigan vaqt semantikasini qo'lda boshqarishni talab qiladi.

```java
@Bean
public BiFunction<KStream<String, Order>, KTable<String, Customer>, KStream<String, EnrichedOrder>> enrich() {
    return (orders, customers) -> orders
        .join(customers, (order, customer) -> new EnrichedOrder(order, customer.tier()));
}
```

**Qo'llanish keyslari:**
- Buyurtma oqimini mijoz profili jadvali bilan boyitib, VIP mijozlarni real vaqtda ajratish.
- Klik/telemetriya eventlariga qurilma yoki tarif ma'lumotini qo'shish (`GlobalKTable` reference data).
- To'lov tranzaksiyalarini `fraud-rules` jadvali bilan solishtirib, qoidaga mos keladiganlarini belgilash.
- IoT sensor o'qishlarini sensor metadata (joylashuv, kalibrovka koeffitsienti) bilan birlashtirish.
- Narx oqimini valyuta kursi jadvaliga join qilib, normallashtirilgan summani chiqarish.

**Ehtiyot bo'ling:** `KTable` bilan join qilish qat'iy co-partitioning talab qiladi - ikki topic bir xil partition soni va bir xil partitioning strategiyasiga ega bo'lishi shart, aks holda jim tarzda ma'lumot yo'qoladi; `GlobalKTable` bu talabni olib tashlaydi, lekin to'liq nusxani har bir instance xotirasiga yuklaydi va faqat katta bo'lmagan reference data uchun mos. Ikkinchi tuzoq - vaqt: jadval yangilanishi stream eventidan kechikib kelsa join eski qiymat bilan bajariladi (`max.task.idle.ms` buni yumshatadi, lekin yo'q qilmaydi), shuning uchun tarixiy aniqlik muhim bo'lsa versiyalangan jadval yoki stream-stream join haqida o'ylash kerak.

## 16.42 Oynalash (Windowing)

**Tavsif:** Windowing cheksiz oqimni vaqt yoki sessiya bo'yicha chekli bo'laklarga ajratib, aggregatsiya (count, sum, avg) va join'ni umuman mumkin qiladi - aks holda "jami qancha" savoli hech qachon yakuniy javobga ega bo'lmaydi. Asosiy turlari: tumbling (ustma-ust tushmaydigan teng oynalar), hopping (ustma-ust tushadigan), sliding (har bir yozuv atrofida) va session (faollik pauzasi bilan ajraladigan). Har bir oyna o'z state store'ida natijani saqlaydi va retention muddati o'tgach tozalanadi.

**Spring'da qayerda uchraydi:** Kafka Streams DSL'da `groupByKey().windowedBy(TimeWindows.ofSizeAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1)))`, `SlidingWindows.ofTimeDifferenceAndGrace(...)` yoki `SessionWindows.ofInactivityGapAndGrace(...)` orqali, natija `KTable<Windowed<K>, V>` bo'ladi; Spring Cloud Stream Kafka Streams binder'ida bu `Function<KStream<...>, KStream<...>>` bean ichida yoziladi, `StreamsBuilderFactoryBean` esa topologiyani boshqaradi. Oyna natijalarini `InteractiveQueryService.getQueryableStore(name, QueryableStoreTypes.windowStore())` bilan HTTP endpoint'dan so'rash mumkin. Kafka Streams'dan tashqari: Spring Integration'da `AggregatingMessageHandler` + `MessageGroupStoreReaper` va `GroupTimeoutExpression` vaqt bo'yicha to'plashni beradi, Project Reactor'da `Flux.window(Duration)`, `buffer(Duration)`, `windowTimeout(n, duration)` operatorlari mavjud (reactive Spring WebFlux oqimlari uchun), Spring Batch esa chunk-oriented ishlov bilan analogik bo'laklashni amalga oshiradi.

**Qo'llanish keyslari:**
- Har 1 daqiqalik tumbling oynada API xatolar sonini hisoblab, alert chiqarish.
- 5 daqiqalik hopping oyna bilan "oxirgi 5 daqiqadagi o'rtacha javob vaqti" dashboard metrikasi.
- Session window bilan foydalanuvchining veb-sayt sessiyasi davomiyligini va ichidagi sahifalar sonini aniqlash.
- Fraud detection: 10 daqiqada bir kartadan 5 dan ko'p tranzaksiya bo'lsa bloklash.
- IoT'da 30 sekundlik oynalarda sensor o'qishlarini o'rtachalashtirib, shovqinni kamaytirish.

**Ehtiyot bo'ling:** Oyna soni va retention (`Materialized.withRetention`) state store hajmini belgilaydi - kichik hopping oynalar va uzun retention RocksDB'ni va changelog topic'ni portlatib yuboradi, session window esa kalitlar soni ko'p bo'lsa xotirani tez to'ldiradi. Shuni ham bilib qo'ying: default holda oyna har yangi yozuvda oraliq natija chiqaradi (downstream ko'p marta yangilanish ko'radi), yakuniy natijani faqat `suppress(Suppressed.untilWindowCloses(...))` beradi, lekin u latency qo'shadi va grace period bilan birga sozlanishi shart.

## 16.43 Event vaqti va ishlov vaqti (Event Time vs Processing Time)

**Tavsif:** Event time - hodisa manbada haqiqatan sodir bo'lgan payt (payload yoki record timestamp ichida keladi), processing time - xabar oqim protsessoriga yetib kelgan va qayta ishlangan payt. Tarmoq kechikishi, mobil qurilmaning offline bo'lishi yoki consumer'ning orqada qolishi bu ikkisini soatlar, hatto kunlarga ajratishi mumkin, shuning uchun aggregatsiya qaysi vaqt bo'yicha bo'lishi natijani tubdan o'zgartiradi. Event time takrorlanuvchi (deterministic) va qayta ishlashda bir xil natija beradi; processing time oddiy va past latency'li, lekin qayta o'qishda boshqa javob chiqadi.

**Spring'da qayerda uchraydi:** Kafka'da har bir `ConsumerRecord` o'z `timestamp()` va `TimestampType` (`CREATE_TIME` = event time, `LOG_APPEND_TIME` = broker qabul qilgan vaqt) atributiga ega; topic darajasida `message.timestamp.type` buni belgilaydi. Kafka Streams'da vaqt manbasini `TimestampExtractor` interfeysi tanlaydi: default `FailOnInvalidTimestamp` record timestamp'ni oladi, `WallclockTimestampExtractor` esa processing time'ga o'tadi; payload ichidagi maydonni ishlatish uchun o'zingizning extractor'ingizni yozib `default.timestamp.extractor` yoki `Consumed.with(..., extractor)` bilan ulaysiz (Spring Cloud Stream'da `spring.cloud.stream.kafka.streams.binder.configuration.default.timestamp.extractor`). Spring for Apache Kafka'da `@Header(KafkaHeaders.RECEIVED_TIMESTAMP)` orqali listener'da record vaqtini olish mumkin, `@Payload` ichidagi `OffsetDateTime` maydoni esa domen event time'i bo'ladi. Umumiy qoida: Java 17+ da event time uchun `Instant`/`OffsetDateTime` (UTC) ishlatiladi, `LocalDateTime` emas.

```java
public class OrderTimeExtractor implements TimestampExtractor {
    @Override
    public long extract(ConsumerRecord<Object, Object> record, long partitionTime) {
        if (record.value() instanceof Order o && o.placedAt() != null) {
            return o.placedAt().toEpochMilli();
        }
        return partitionTime; // fallback: oqimning joriy vaqti
    }
}
```

**Qo'llanish keyslari:**
- Mobil ilovadan offline rejimda to'plangan eventlar ulanish tiklangach kelganda, ularni haqiqiy sodir bo'lish kuniga hisoblash.
- Kunlik moliyaviy yopilish hisoboti: tranzaksiya kechqurun 23:59'da bo'lib, ertalab kelsa ham o'sha kunga tushishi kerak.
- Replay/backfill: tarixiy topic'ni qayta o'qiganda event time bilan avvalgi natijalar aynan takrorlanishi.
- Monitoring va alerting uchun processing time (hozir nima bo'layotgani muhim, tarixiy aniqlik emas).
- Lag o'lchash: `processingTime - eventTime` ni metrika sifatida (Micrometer `Timer`/`Gauge`) chiqarib, pipeline kechikishini kuzatish.

**Ehtiyot bo'ling:** Event time manbadagi soatga tayanadi - mijoz qurilmasi yoki boshqa serverning soati noto'g'ri bo'lsa, "kelajakdan" kelgan timestamp oyna va watermark hisobini buzadi, shuning uchun kelgan vaqtni sanity-check qilish (kelajakka chegara qo'yish) kerak. Ikkita vaqtni bitta pipeline'da aralashtirib yubormang: masalan filtrlashni processing time, aggregatsiyani event time bo'yicha qilsangiz, natija tushuntirib bo'lmas holga keladi; past latency'li va aniqlikka sezgir bo'lmagan ishlar uchun processing time'ni ongli ravishda tanlash to'g'ri yechim.

## 16.44 Watermark (Watermark)

**Tavsif:** Watermark - oqim protsessorining "event time bo'yicha hozir shu paytgacha yetib keldim, bundan avvalgi hodisalar deyarli to'liq keldi deb hisoblayman" degan harakatlanuvchi chegarasi. U kechikkan ma'lumot kutish bilan natijani chiqarish o'rtasidagi muvozanatni boshqaradi: watermark oyna oxiridan o'tib ketganda oyna yopiladi va natija yakunlanadi. Watermarkdan keyin kelgan yozuvlar "late" hisoblanib, grace period ichida bo'lsa qabul qilinadi, aks holda tashlab yuboriladi yoki alohida kanalga yo'naltiriladi.

**Spring'da qayerda uchraydi:** Kafka Streams'da alohida `Watermark` API yo'q - uning ekvivalenti "stream time" (har bir task ko'rgan eng katta event timestamp) va `ofSizeAndGrace(windowSize, gracePeriod)` / `SessionWindows.ofInactivityGapAndGrace(...)` dagi grace period; oyna faqat `windowEnd + grace < streamTime` bo'lganda yopiladi. Spring Cloud Stream Kafka Streams binder bu konfiguratsiyani topologiya ichida yozilgan oyna ta'rifi orqali meros qilib oladi, `suppress(Suppressed.untilWindowCloses(BufferConfig.unbounded()))` esa yakuniy natijani faqat watermark o'tgandan keyin chiqaradi. Kechikkan yozuvlarni kuzatish uchun `kafka_stream_task_dropped_records` metrikasi Micrometer orqali Spring Boot Actuator'ning `/actuator/prometheus` endpoint'iga chiqadi (`KafkaStreamsMicrometerListener`). Haqiqiy watermark modeli Apache Flink'da (`WatermarkStrategy.forBoundedOutOfOrderness`) va Apache Beam'da mavjud - Spring ilovasi odatda bu engine'larga `spring-boot-starter`'siz, alohida job sifatida murojaat qiladi yoki Kafka Streams'ning stream time modeli bilan cheklanadi.

**Qo'llanish keyslari:**
- Kunlik savdo aggregatsiyasida kechikkan buyurtmalarni 2 soat kutib, keyin hisobotni yakunlash (`ofSizeAndGrace(1 kun, 2 soat)`).
- Yakuniy natijani bir marta downstream'ga yuborish: `suppress(untilWindowCloses)` bilan oraliq yangilanishlarni bosish.
- Juda kechikkan eventlarni tashlab yubormasdan alohida "late-events" topic'iga yo'naltirib, keyinroq batch bilan qayta hisoblash.
- SLA monitoringi: `streamTime - windowEnd` va dropped-records metrikalari orqali pipeline qanchalik orqada qolganini kuzatish.
- Stream-stream join'da ikki oqimdan birining kechikishini `JoinWindows.ofTimeDifferenceAndGrace(...)` bilan toleratsiya qilish.

**Ehtiyot bo'ling:** Kafka Streams'ning stream time faqat kelgan ma'lumot bilan oldinga suriladi - oqim to'xtab qolsa (partition bo'sh bo'lsa) watermark qotib qoladi va oynalar hech qachon yopilmaydi, shuning uchun "nega natija chiqmayapti" muammosi ko'pincha shundan; past trafikli topic'larda `suppress(untilWindowCloses)` ni ehtiyotkorlik bilan ishlating. Grace period'ni haddan ziyod uzun qilsangiz latency va state store hajmi oshadi, juda qisqa qilsangiz esa haqiqiy biznes ma'lumoti jimgina yo'qoladi - shuning uchun uni real kechikish taqsimotini (p99) o'lchab tanlang va tashlangan yozuvlar uchun albatta alert qo'ying.

## 16.45 Amalda qo'llash

- [ ] Xabar transformatsiyasi bajariladigan joylarni sanab chiqing va har biri idempotent ekanini tasdiqlang.
- [ ] Content enricher ishlatiladigan joylarni toping va boyitish uchun tashqi chaqiruv borligini, uning timeout'i borligini tekshiring.
- [ ] Har bir iste'molchi uchun idempotent receiver mexanizmini yozib qo'ying: qanday kalit bo'yicha takrorlanish aniqlanadi.
- [ ] Xabar tartibi muhim bo'lgan oqimlarni belgilab, ularning partition kaliti to'g'ri tanlanganini tasdiqlang.
- [ ] Hodisa turlarini ajratib yozing: hodisa xabarnomasimi, holat uzatuvchimi yoki event sourcing uchunmi.
- [ ] Control bus yoki boshqaruv kanali orqali bajariladigan operatsiyalarni ro'yxatga olib, ularning huquqlari cheklanganini tekshiring.
- [ ] Xabar oqimlarida kuzatuvchanlik borligini tasdiqlang: correlation ID uzatiladimi, lag o'lchanadimi.
- [ ] Har bir sxema o'zgarishi uchun orqaga va oldinga moslik testini CI ga qo'shing.

---

[&larr; 15. Enterprise Integration Patterns I: xabarlar, kanallar, marshrutlash](15-enterprise-integration-patterns-i-xabarlar.md) · [Mundarija](README.md) · [17. Resilience va cloud dizayn patternlari &rarr;](17-resilience-va-cloud-dizayn-patternlari.md)
