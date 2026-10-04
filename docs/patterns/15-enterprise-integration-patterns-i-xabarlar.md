<!-- doc: patterns | chapter: 15 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 15. Enterprise Integration Patterns I: xabarlar, kanallar, marshrutlash (EIP I: Messaging Systems, Channels, Construction, Routing)

<details>
<summary>Bu bo'limdagi 36 bo'lim</summary>

- [15.1 Xabar kanali (Message Channel)](#151-xabar-kanali-message-channel)
- [15.2 Xabar (Message)](#152-xabar-message)
- [15.3 Quvurlar va filtrlar (Pipes and Filters)](#153-quvurlar-va-filtrlar-pipes-and-filters)
- [15.4 Xabar marshrutlagich (Message Router)](#154-xabar-marshrutlagich-message-router)
- [15.5 Xabar tarjimoni (Message Translator)](#155-xabar-tarjimoni-message-translator)
- [15.6 Xabar endpoint'i (Message Endpoint)](#156-xabar-endpointi-message-endpoint)
- [15.7 Nuqta-nuqta kanali (Point-to-Point Channel)](#157-nuqta-nuqta-kanali-point-to-point-channel)
- [15.8 E'lon-obuna kanali (Publish-Subscribe Channel)](#158-elon-obuna-kanali-publish-subscribe-channel)
- [15.9 Ma'lumot turi kanali (Datatype Channel)](#159-malumot-turi-kanali-datatype-channel)
- [15.10 Noto'g'ri xabar kanali (Invalid Message Channel)](#1510-notogri-xabar-kanali-invalid-message-channel)
- [15.11 O'lik xat kanali (Dead Letter Channel)](#1511-olik-xat-kanali-dead-letter-channel)
- [15.12 Kafolatlangan yetkazib berish (Guaranteed Delivery)](#1512-kafolatlangan-yetkazib-berish-guaranteed-delivery)
- [15.13 Kanal adapteri (Channel Adapter)](#1513-kanal-adapteri-channel-adapter)
- [15.14 Xabar ko'prigi (Messaging Bridge)](#1514-xabar-koprigi-messaging-bridge)
- [15.15 Xabar sahnasi / Message Bus (Message Bus)](#1515-xabar-sahnasi--message-bus-message-bus)
- [15.16 Buyruq xabari (Command Message)](#1516-buyruq-xabari-command-message)
- [15.17 Hujjat xabari (Document Message)](#1517-hujjat-xabari-document-message)
- [15.18 Hodisa xabari (Event Message)](#1518-hodisa-xabari-event-message)
- [15.19 So'rov-javob (Request-Reply)](#1519-sorov-javob-request-reply)
- [15.20 Qaytish manzili (Return Address)](#1520-qaytish-manzili-return-address)
- [15.21 Korrelyatsiya identifikatori (Correlation Identifier)](#1521-korrelyatsiya-identifikatori-correlation-identifier)
- [15.22 Xabarlar ketma-ketligi (Message Sequence)](#1522-xabarlar-ketma-ketligi-message-sequence)
- [15.23 Xabar amal qilish muddati (Message Expiration)](#1523-xabar-amal-qilish-muddati-message-expiration)
- [15.24 Format ko'rsatkichi (Format Indicator)](#1524-format-korsatkichi-format-indicator)
- [15.25 Kontent asosidagi marshrutizator (Content-Based Router)](#1525-kontent-asosidagi-marshrutizator-content-based-router)
- [15.26 Xabar filtri (Message Filter)](#1526-xabar-filtri-message-filter)
- [15.27 Dinamik marshrutizator (Dynamic Router)](#1527-dinamik-marshrutizator-dynamic-router)
- [15.28 Qabul qiluvchilar ro'yxati (Recipient List)](#1528-qabul-qiluvchilar-royxati-recipient-list)
- [15.29 Ajratuvchi (Splitter)](#1529-ajratuvchi-splitter)
- [15.30 Agregator (Aggregator)](#1530-agregator-aggregator)
- [15.31 Qayta tartiblovchi (Resequencer)](#1531-qayta-tartiblovchi-resequencer)
- [15.32 Birlashtirilgan xabar protsessori (Composed Message Processor)](#1532-birlashtirilgan-xabar-protsessori-composed-message-processor)
- [15.33 Sochish-yig'ish (Scatter-Gather)](#1533-sochish-yigish-scatter-gather)
- [15.34 Marshrut varaqasi (Routing Slip)](#1534-marshrut-varaqasi-routing-slip)
- [15.35 Jarayon menejeri (Process Manager)](#1535-jarayon-menejeri-process-manager)
- [15.36 Xabar brokeri (Message Broker)](#1536-xabar-brokeri-message-broker)

</details>



Enterprise Integration Patterns (EIP) - Gregor Hohpe va Bobby Woolf tomonidan kodlashtirilgan, asinxron xabar almashinuvga asoslangan tizimlar integratsiyasining umumiy lug'ati. Bu patternlar alohida deploy qilinadigan servislar bir-biriga to'g'ridan-to'g'ri RPC bilan bog'lanmasdan, kanal (channel) va xabar (message) abstraksiyalari orqali vaqt bo'yicha ajralgan (temporally decoupled) holda muloqot qilish usulini tasvirlaydi. Arxitektor uchun bu muhim, chunki Spring Integration, Spring Cloud Stream, Apache Camel va hatto Kafka/RabbitMQ bilan ishlashning zamonaviy API'lari aynan shu terminologiya ustiga qurilgan - pattern nomini bilish jamoa bilan bir tilda gaplashish va tayyor komponentni noldan yozib o'tirmaslik imkonini beradi. Quyidagi entry'lar messaging tizimining poydevorini, kanal turlarini va marshrutlash (routing) asoslarini qamrab oladi.

## 15.1 Xabar kanali (Message Channel)

**Tavsif:** Ikki ilova yoki komponent to'g'ridan-to'g'ri bir-birini chaqirmasligi uchun ular orasiga qo'yiladigan mantiqiy "quvur" (conduit). Jo'natuvchi (producer) xabarni kanalga yozadi, qabul qiluvchi (consumer) esa undan o'qiydi - natijada ikki tomon bir-birining manzilini, mavjudligini va ishlash tezligini bilishi shart emas. Kanal buffer vazifasini ham bajaradi: iste'molchi sekin bo'lsa, xabarlar navbatda turadi. Kanal - barcha boshqa EIP patternlarining asosiy qurilish bloki.

**Spring'da qayerda uchraydi:** Spring Integration'da `org.springframework.messaging.MessageChannel` interfeysi va uning amalga oshirishlari: `DirectChannel` (default, chaqiruvchi thread'da sinxron), `QueueChannel` (in-memory buffer, pollerga muhtoj), `ExecutorChannel`, `PublishSubscribeChannel`, `FluxMessageChannel` (reactive). Java DSL'da `IntegrationFlow` ichida `.channel("orders")` yoki `MessageChannels.queue(100)` orqali e'lon qilinadi, `@ServiceActivator(inputChannel = "orders")` orqali iste'mol qilinadi. Spring Cloud Stream 4.x'da kanal roli `java.util.function.Function`/`Supplier`/`Consumer` bean'lari va binder (Kafka, RabbitMQ) destination'lari bilan almashtirilgan.

**Qo'llanish keyslari:**
- Buyurtma qabul qilish REST controller'i va og'ir hisob-kitob qiluvchi worker'ni ajratish.
- Fayl yuklash modulidan parsing modulini bufer bilan ajratib, trafik cho'qqilarini yumshatish.
- Monolitdan ajratilgan servislar orasida vaqt bo'yicha decoupling (biri o'chganda ham xabar yo'qolmaydi).
- Bir xil hodisani bir nechta iste'molchiga yetkazish uchun nomli kanal yaratish.
- Test muhitida real broker o'rniga in-memory kanal bilan oqimni tekshirish.

**Ehtiyot bo'ling:** `DirectChannel` nomi "kanal" bo'lsa ham asinxron emas - u chaqiruvchi thread'da ishlaydi, shuning uchun uni ishlatib "asinxron qildim" deb o'ylash eng keng tarqalgan xato. `QueueChannel` esa in-memory bo'lgani uchun JVM o'chsa xabarlar yo'qoladi - durability kerak bo'lsa broker-backed kanal (Kafka, Rabbit, JMS) ishlating.

## 15.2 Xabar (Message)

**Tavsif:** Kanal orqali uzatiladigan atomar ma'lumot birligi: foydali yuk (payload) va meta-ma'lumot (header'lar) dan iborat konvert. Header'lar texnik kontekstni (ID, correlation ID, timestamp, reply address, content type) tashiydi, payload esa biznes ma'lumotini. Bu ajratish tufayli infrastruktura payload'ni ochib ko'rmasdan marshrutlash, filtrlash va kuzatish (tracing) ishlarini bajara oladi.

**Spring'da qayerda uchraydi:** `org.springframework.messaging.Message<T>` interfeysi (`getPayload()`, `getHeaders()`), `GenericMessage`, `ErrorMessage` va `MessageBuilder.withPayload(...).setHeader(...).build()`. Header kalitlari uchun `MessageHeaders` (`ID`, `TIMESTAMP`, `REPLY_CHANNEL`, `ERROR_CHANNEL`, `CONTENT_TYPE`) va `IntegrationMessageHeaderAccessor` (`CORRELATION_ID`, `SEQUENCE_NUMBER`). Handler metodlarida `@Payload`, `@Header`, `@Headers` annotatsiyalari; Kafka'da `KafkaHeaders`, JMS'da `javax.jms.Message`/`jakarta.jms.Message` ga mapping `DefaultJmsHeaderMapper` orqali.

```java
Message<Order> msg = MessageBuilder.withPayload(order)
        .setHeader("tenantId", tenantId)
        .setHeader(MessageHeaders.CONTENT_TYPE, "application/json")
        .build();
```

**Qo'llanish keyslari:**
- Multi-tenant tizimda `tenantId` ni header'da tashib, payload sxemasini o'zgartirmaslik.
- Distributed tracing uchun `traceparent` header'ini oqim bo'ylab uzatish.
- Idempotentlik uchun `messageId` ni header'dan olib dedup store bilan solishtirish.
- Routing qarori uchun `eventType` header'idan foydalanish (payload'ni deserialize qilmasdan).
- Retry hisobini `x-retry-count` header'ida saqlab, limitdan oshganda DLQ'ga yuborish.

**Ehtiyot bo'ling:** `MessageHeaders` immutable - mavjud xabarni o'zgartirmoqchi bo'lsangiz `MessageBuilder.fromMessage(...)` bilan yangi nusxa yarating. Header'ga katta obyekt yoki maxfiy ma'lumot (token, parol) solish - broker log'lariga chiqib ketish va limitdan oshish xavfi; payload kattaligini header'ga ko'chirib hal qilmang, Claim Check patternidan foydalaning.

## 15.3 Quvurlar va filtrlar (Pipes and Filters)

**Tavsif:** Katta ishlov berish vazifasini mustaqil bosqichlarga (filter) bo'lib, ularni kanallar (pipe) bilan ketma-ket ulash. Har bir bosqich faqat bitta ishni bajaradi va natijani keyingi kanalga beradi, shuning uchun bosqichlarni qayta tartiblash, almashtirish yoki alohida masshtablash mumkin. Kirish va chiqish interfeysi bir xil (Message) bo'lgani uchun bosqichlar bir-biri haqida hech narsa bilmaydi.

**Spring'da qayerda uchraydi:** Spring Integration Java DSL'ning butun modeli shu patternga asoslangan: `IntegrationFlow.from(...).filter(...).transform(...).handle(...).get()`. Har bir `.transform()`/`.filter()`/`.handle()` bosqichi orasida avtomatik kanal yaratiladi; `.channel(MessageChannels.executor(...))` qo'yib bosqichni alohida thread pool'ga chiqarish mumkin. Spring Cloud Stream'da `Function` bean'larini `spring.cloud.function.definition=enrich|validate|persist` orqali kompozitsiya qilish; Spring Batch'da `Step` zanjiri va `CompositeItemProcessor` ham xuddi shu g'oya.

**Qo'llanish keyslari:**
- XML/EDI faylni dekodlash → validatsiya → boyitish → DB'ga yozish bosqichlariga bo'lish.
- Faqat sekin bosqichni (masalan tashqi API chaqiruvi) alohida concurrency bilan masshtablash.
- Yangi biznes talabi uchun oqimga yangi bosqich qo'shish (eski kodga tegmasdan).
- Har bir bosqichni alohida unit test qilish va metrikalarini alohida o'lchash.
- Log boyitish pipeline'i: parse → mask PII → enrich geo → sink.

**Ehtiyot bo'ling:** Juda ko'p mayda bosqich serialize/deserialize va kanal hop xarajatini oshiradi - latency sezgir oqimda bosqichlarni birlashtirish yaxshiroq. Bosqichlar orasida yashirin umumiy mutable state (static map, shared bean field) paydo bo'lsa, pattern afzalligi yo'qoladi va parallel ishlaganda race condition chiqadi.

## 15.4 Xabar marshrutlagich (Message Router)

**Tavsif:** Bitta kirish kanalidan xabarni olib, uning mazmuni yoki header'iga qarab bir nechta chiqish kanalidan birini tanlaydi. Router xabarni o'zgartirmaydi - faqat "qayerga ketishi" qarorini qabul qiladi, shu bilan jo'natuvchini qabul qiluvchilar topologiyasidan ajratadi. Qoida o'zgarganda faqat router sozlamasi o'zgaradi, producer kodiga tegilmaydi.

**Spring'da qayerda uchraydi:** `AbstractMessageRouter` va uning amalga oshirishlari: `HeaderValueRouter`, `PayloadTypeRouter`, `RecipientListRouter`, `ErrorMessageExceptionTypeRouter`, `ExpressionEvaluatingRouter`. Annotatsiya: `@Router`; Java DSL: `.route("headers['eventType']")` yoki `.<Order, Boolean>route(o -> o.getTotal() > 1000, m -> m.channelMapping(true, "manualReview").channelMapping(false, "autoApprove"))`. Apache Camel'da `choice().when(...).to(...)`; Kafka Streams'da `KStream.split().branch(...)`.

**Qo'llanish keyslari:**
- `eventType` header'iga qarab buyurtma, to'lov va qaytarish hodisalarini turli handler'larga yuborish.
- Premium va oddiy mijoz so'rovlarini alohida SLA'li navbatlarga ajratish.
- Payload turi (`CreditCardPayment` vs `BankTransfer`) bo'yicha to'lov provayderini tanlash.
- Versiyalangan xabarlarni (`schemaVersion=1|2`) mos parserga yo'naltirish.
- Xato turiga qarab retry kanali yoki DLQ orasida tanlov qilish.

**Ehtiyot bo'ling:** Router tizimda markaziy "bilimli" nuqtaga aylanib ketishi mumkin - barcha biznes qoidalari unga yig'ilsa, bu yashirin monolit bo'ladi; qoidalar ko'paysa Publish-Subscribe + filter yoki Content-Based Router'ni servislarga tarqatishni ko'rib chiqing. `defaultOutputChannel` berilmasa, mos kanal topilmagan xabar exception bilan tushadi.

## 15.5 Xabar tarjimoni (Message Translator)

**Tavsif:** Ikki tizim turli ma'lumot formatlari yoki sxemalaridan foydalanganda, ular orasida format o'girishni amalga oshiruvchi komponent. Xabarning payload'ini (ba'zan header'larini) bir ko'rinishdan boshqasiga o'zgartiradi, lekin marshrutlash qarori qabul qilmaydi. Shu tufayli har bir tizim o'z ichki modelini saqlab qoladi va integratsiya "adapter" kodi bir joyda to'planadi.

**Spring'da qayerda uchraydi:** `@Transformer` annotatsiyasi, `GenericTransformer`/`AbstractTransformer`, tayyorlar: `ObjectToJsonTransformer`, `JsonToObjectTransformer`, `MarshallingTransformer` (JAXB), `ObjectToStringTransformer`, `MapToObjectTransformer`, `FileToByteArrayTransformer`. Java DSL'da `.transform(Order.class, this::toOrderDto)` yoki `.transform(Transformers.fromJson(OrderDto.class))`. Kengroq ekotizimda MapStruct (`@Mapper`), Jackson `ObjectMapper`, Spring Cloud Stream'da `spring.cloud.stream.bindings.*.content-type` bilan avtomatik konvertatsiya (`MessageConverter`).

**Qo'llanish keyslari:**
- Legacy SOAP/XML so'rovini ichki JSON domen modeliga o'girish.
- Domen event'ini tashqi partner talab qilgan CSV yoki fixed-width formatga aylantirish.
- Kafka'dagi Avro record'ni ichki DTO'ga map qilish.
- Maydon nomlari va o'lchov birliklarini normalizatsiya qilish (sent → dollar, epoch → ISO-8601).
- Chiqish xabaridan maxfiy maydonlarni (PII) olib tashlab, auditga mos ko'rinish berish.

**Ehtiyot bo'ling:** Transformer ichida I/O (DB yoki REST chaqiruvi) qilish - bu allaqachon Content Enricher vazifasi; ularni aralashtirsangiz test qilish qiyinlashadi va oqim latency'si ko'rinmas bo'lib qoladi. Qo'lda yozilgan mapping kodi sxema o'zgarganda sekin buziladi - MapStruct yoki sxema reestri (schema registry) bilan compile-time/contract tekshiruvini qo'shing.

## 15.6 Xabar endpoint'i (Message Endpoint)

**Tavsif:** Ilova kodi bilan messaging infrastrukturasi orasidagi ulanish nuqtasi: ilova messaging API'sini bilmaydi, endpoint uning o'rniga xabarni oladi/jo'natadi va metod chaqiruviga aylantiradi. Bu ikki yo'nalishda ishlaydi - kiruvchi xabarni POJO metodiga uzatadi (consumer endpoint) yoki metod chaqiruvini xabarga o'rab kanalga yozadi (producer/gateway). Natijada biznes logikasi broker turiga bog'lanmagan va alohida test qilinadigan bo'lib qoladi.

**Spring'da qayerda uchraydi:** `@ServiceActivator`, `@MessagingGateway`, `@InboundChannelAdapter`, `@MessageEndpoint` annotatsiyalari; `MessageHandler`, `MessageProducer`, `SourcePollingChannelAdapter`, `EventDrivenConsumer`, `PollingConsumer`. Broker-maxsus endpoint'lar: `@KafkaListener` + `KafkaTemplate`, `@RabbitListener` + `RabbitTemplate`, `@JmsListener` + `JmsTemplate`, `@SqsListener` (Spring Cloud AWS). Spring Cloud Stream'da endpoint roli `Consumer<Message<T>>`/`Supplier<T>` funksional bean'lari bilan bajariladi.

**Qo'llanish keyslari:**
- `@MessagingGateway` interfeysi orqali servis kodidan sinxron ko'rinishdagi, lekin ichida asinxron chaqiruv qilish.
- `@KafkaListener` bilan topic'dan o'qib, POJO handler metodiga uzatish.
- Polling adapter bilan katalog papkasidan yoki DB jadvalidan yangi yozuvlarni oqimga tortish.
- Tashqi SFTP/HTTP manbadan inbound adapter orqali xabar yaratish.
- Biznes servisni messaging'dan mustaqil unit test qilish (endpoint'ni mocklab).

**Ehtiyot bo'ling:** Biznes logikasini bevosita listener metodining ichiga yozish - endpoint'ni biznes qatlamiga aylantirib, uni brokersiz test qilishni imkonsiz qiladi; handler faqat delegatsiya qilsin. Listener metodida exception'ni jimgina yutib yuborish ack semantikasini buzadi: Kafka'da offset commit bo'lib xabar yo'qoladi.

## 15.7 Nuqta-nuqta kanali (Point-to-Point Channel)

**Tavsif:** Kanalga yozilgan har bir xabarni faqat BITTA iste'molchi oladi - bir nechta consumer ulansa ham, xabar ular orasida taqsimlanadi, nusxalanmaydi. Bu competing consumers orqali gorizontal masshtablash va ishni taqsimlashning asosiy mexanizmi. Semantikasi "ish buyrug'i" (command) uchun to'g'ri keladi: bir ishni ikki marta bajarish kerak emas.

**Spring'da qayerda uchraydi:** Spring Integration'da `DirectChannel` (round-robin `LoadBalancingStrategy` bilan), `QueueChannel`, `ExecutorChannel`. Broker darajasida: JMS `Queue` (`JmsTemplate`, `@JmsListener`), RabbitMQ'da bitta queue'ga bir nechta consumer (`SimpleMessageListenerContainer`, `concurrency`), Kafka'da bir xil `group.id` dagi consumer'lar (`@KafkaListener(groupId = "...")`) - partition'lar ular orasida bo'linadi. Spring Cloud Stream'da `spring.cloud.stream.bindings.<name>-in-0.group` berilishi aynan shu semantikani beradi.

**Qo'llanish keyslari:**
- Buyurtmani ishlovchi worker'larni 10 ta instance'ga ko'paytirib throughput oshirish.
- PDF/hisobot generatsiyasi kabi og'ir vazifalarni ish navbatiga qo'yish.
- Email/SMS yuborish command'larini bitta marta bajarilishini kafolatlash.
- Kafka'da consumer group bilan partition'larni avtomatik rebalance qilish.
- Fon vazifalarini (image resize) navbat uzunligi bo'yicha autoscale qilish.

**Ehtiyot bo'ling:** Point-to-point "bir marta yetkazish" degani emas - retry va rebalance paytida takroriy yetkazish bo'lishi mumkin, shuning uchun handler idempotent bo'lishi shart. Kafka'da parallelizm partition soni bilan cheklangan: consumer'ni partition'dan ko'p qilsangiz, ortiqchasi bo'sh turadi.

## 15.8 E'lon-obuna kanali (Publish-Subscribe Channel)

**Tavsif:** Kanalga yozilgan xabarning nusxasi barcha obunachilarga (subscriber) yetkaziladi, ya'ni bir hodisaga bir nechta mustaqil reaksiya bo'lishi mumkin. Producer obunachilar kimligini va sonini bilmaydi - yangi obunachi qo'shilsa, jo'natuvchi kodi o'zgarmaydi. Bu "hodisa yuz berdi" (event) semantikasi uchun to'g'ri model.

**Spring'da qayerda uchraydi:** `PublishSubscribeChannel` (ixtiyoriy `TaskExecutor` bilan asinxron), Java DSL'da `.publishSubscribeChannel(s -> s.subscribe(f -> ...).subscribe(f -> ...))`. JVM ichida `ApplicationEventPublisher` + `@EventListener`/`@TransactionalEventListener`. Broker darajasida: JMS `Topic`, RabbitMQ `fanout`/`topic` exchange (`TopicExchange`, `FanoutExchange`, `Binding`), Kafka'da har bir iste'molchiga alohida `group.id`. Spring Cloud Stream'da bir destination'ga turli `group` qiymatlari bilan bir nechta app obuna bo'ladi.

**Qo'llanish keyslari:**
- `OrderPlaced` hodisasiga ombor, billing va analytics servislarining mustaqil reaksiyasi.
- Audit log'ni asosiy oqimga tegmasdan yon tarmoq sifatida yozish.
- Cache invalidation signalini barcha node'larga tarqatish.
- Notification (email + push + webhook) kanallarini bir-biridan mustaqil qo'shish.
- Yangi analitik servisni ishlab chiqishda mavjud oqimga "tinglovchi" sifatida ulash.

**Ehtiyot bo'ling:** Default `PublishSubscribeChannel` sinxron ishlaydi - bitta obunachi sekin yoki exception tashlasa, u butun chain'ni bloklaydi yoki buzadi; `TaskExecutor` va `ErrorHandler` sozlang. Pub-sub'ni command uchun ishlatish (masalan to'lovni olish) ikki marta bajarilish xatosiga olib keladi - command uchun point-to-point ishlating.

## 15.9 Ma'lumot turi kanali (Datatype Channel)

**Tavsif:** Har bir kanal faqat bitta aniq turdagi xabarni tashiydi, shunda iste'molchi payload turini tekshirish yoki `instanceof` zanjiri yozish zaruratidan xalos bo'ladi. Bu kanal nomining o'zini kontrakt (contract) ga aylantiradi: "`orders` kanalida faqat `Order` keladi". Turli turlar bir kanalda aralashsa, Message Router bilan ularni alohida datatype kanallarga ajratish kerak.

**Spring'da qayerda uchraydi:** Spring Integration'da `AbstractMessageChannel.setDatatypes(Class<?>...)` (XML'da `datatype="com.acme.Order"`), kerak bo'lsa `MessageConverter` bilan birga - tur mos kelmasa `MessageDeliveryException` tashlanadi. Shuningdek `PayloadTypeRouter` va `PayloadTypeSelector` bilan ajratish; handler darajasida generic signature (`GenericTransformer<Order, OrderDto>`) va `@ServiceActivator` metod parametri turi ham de-fakto datatype kontraktini bildiradi. Kafka'da bu rol topic + schema registry (Avro/Protobuf) juftligi bilan bajariladi.

**Qo'llanish keyslari:**
- `payments` va `refunds` uchun alohida kanal ochib, handler'lardan tur tekshiruvini olib tashlash.
- Kafka'da har bir event turi uchun alohida topic va sxema belgilash.
- Oqimga xato turdagi payload kirib ketishini deploy paytida emas, erta aniqlash.
- Compile-time type safety uchun generic transformer zanjiri qurish.
- Versiyalangan sxemalar uchun `orders.v1` / `orders.v2` kanallarini ajratish.

**Ehtiyot bo'ling:** Har bir mayda tur uchun alohida kanal ochish topologiyani portlatib yuboradi - tur yaqin bo'lsa umumiy bazaviy tur yoki canonical data model bilan bitta kanalda qolish arzonroq. `setDatatypes` bilan qattiq cheklash evolyutsiyani qiyinlashtiradi: sxema o'zgarganda eski producer'lar birdan `MessageDeliveryException` ola boshlaydi.

## 15.10 Noto'g'ri xabar kanali (Invalid Message Channel)

**Tavsif:** Formati, turi yoki mazmuni kutilganiga mos kelmagan xabarlarni asosiy oqimdan chiqarib, alohida kanalga yuborish uchun ishlatiladi. Bu "poison message" bitta sekund ichida minglab marta qayta ishlanib oqimni to'xtatib qo'yishining oldini oladi va texnik jamoaga tahlil uchun material beradi. Muhim farqi: bu yetkazib berish muammosi emas - xabar keldi, lekin uni tushunib bo'lmadi.

**Spring'da qayerda uchraydi:** Spring Integration'da global `errorChannel` (default `PublishSubscribeChannel`) va endpoint darajasidagi `@ServiceActivator(inputChannel="...", ...)` bilan birga `MessageHeaders.ERROR_CHANNEL` header'i; xabar `ErrorMessage` ichida `MessagingException` (`getFailedMessage()`) bo'lib keladi. `ErrorMessageExceptionTypeRouter` bilan validatsiya xatolarini (`MessageConversionException`, `MessageHandlingException`) alohida kanalga ajratish mumkin. Kafka'da `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`, `ErrorHandlingDeserializer` (deserialize xatosini listener'ga yetib bormasdan ushlaydi); Rabbit'da `RepublishMessageRecoverer`.

**Qo'llanish keyslari:**
- Deserialize qilinmaydigan buzuq JSON/Avro xabarni oqimdan chiqarib, consumer'ni to'xtatib qo'ymaslik.
- Majburiy maydoni yo'q buyurtmalarni alohida kanalda yig'ib, biznes jamoaga ro'yxat berish.
- Noto'g'ri sxema versiyasi bilan kelgan xabarlarni karantinga olish.
- Invalid xabarlar ratesini metrikaga chiqarib, upstream producer regressiyasini aniqlash.
- Tahlil qilingan xabarlarni tuzatib, qayta oqimga qo'yish (replay) uchun saqlash.

**Ehtiyot bo'ling:** Invalid message kanalini hech kim o'qimasa - u ko'rinmas ma'lumot qabristoniga aylanadi; alert, retention va replay protsedurasi bo'lishi shart. Bu kanalni infrastruktura xatolari (broker uzilishi, timeout) uchun ishlatmang - ular retry va Dead Letter Channel hududiga tegishli.

## 15.11 O'lik xat kanali (Dead Letter Channel)

**Tavsif:** Xabarni belgilangan iste'molchiga yetkazib bo'lmaganda (bir necha marta retry'dan keyin ham, TTL tugaganda, queue to'lganda yoki handler doimiy xato berganda) broker uni yo'q qilmasdan maxsus kanalga ko'chiradi. Shu tufayli xabar yo'qolmaydi, asosiy navbat bloklanmaydi va operatsion jamoa muammoni keyin tahlil qilib, xabarni qayta jo'natishi mumkin. Odatda bu broker tomonidan taqdim etiladigan infrastruktura imkoniyati.

**Spring'da qayerda uchraydi:** Spring Kafka'da `DefaultErrorHandler` + `DeadLetterPublishingRecoverer` (default `<topic>.DLT`), `@RetryableTopic(attempts = "4", dltTopicSuffix = ".dlt")` va `@DltHandler`; `FixedBackOff`/`ExponentialBackOffWithMaxRetries` bilan retry policy. Spring AMQP'da `x-dead-letter-exchange` / `x-dead-letter-routing-key` argumentlari (`QueueBuilder.durable("orders").deadLetterExchange("dlx").build()`), `RepublishMessageRecoverer`. Spring Cloud Stream'da `spring.cloud.stream.rabbit.bindings.*.consumer.auto-bind-dlq=true` yoki `spring.cloud.stream.kafka.bindings.*.consumer.enable-dlq=true`. JMS'da brokerning o'zidagi `ActiveMQ.DLQ`.

```java
@Bean
DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> template) {
    return new DefaultErrorHandler(
            new DeadLetterPublishingRecoverer(template),
            new ExponentialBackOffWithMaxRetries(3));
}
```

**Qo'llanish keyslari:**
- Tashqi API uzoq vaqt javob bermaganda xabarlarni DLQ'ga chiqarib, asosiy oqimni tirik saqlash.
- `@DltHandler` da xabarni audit jadvaliga yozib, support ticket yaratish.
- Bug tuzatilgandan keyin DLQ'dan asosiy topic'ga replay qilish.
- DLQ hajmini SRE dashboard'ida SLO sifatida kuzatish va alert qo'yish.
- TTL tugagan, eskirgan buyurtmalarni tahlil uchun saqlab qolish.

**Ehtiyot bo'ling:** DLQ'ni "keyin ko'ramiz" qutisi sifatida qoldirish eng ko'p uchraydigan operatsion qarz - monitoring va retention siyosati bo'lmasa, ma'lumot jimgina yo'qoladi. Retry'ni cheksiz yoki juda tez (backoff'siz) qilib qo'ysangiz, poison message broker va downstream'ni DoS qiladi; shuningdek DLQ'ga qayta-qayta tushayotgan xabarlar uchun ikkinchi darajali tsikl (DLQ → retry → DLQ) hosil qilmang.

## 15.12 Kafolatlangan yetkazib berish (Guaranteed Delivery)

**Tavsif:** Xabar jo'natuvchi va qabul qiluvchi JVM'lari yoki broker qayta ishga tushsa ham yo'qolmasligini ta'minlash uchun xabarni doimiy saqlash joyiga (disk, replikatsiya qilingan log) yozish. Producer tomonida xabar broker tomonidan qabul qilinganini tasdiqlash (ack/publisher confirm), consumer tomonida esa muvaffaqiyatli ishlov berilgandan keyingina ack berish kerak. Bu kafolat latency va throughput hisobiga keladi - har bir yozuv `fsync`/replikatsiya kutadi.

**Spring'da qayerda uchraydi:** Kafka'da `acks=all`, `enable.idempotence=true`, `min.insync.replicas`, consumer tomonida `enable.auto.commit=false` + `AckMode.MANUAL_IMMEDIATE` (`ContainerProperties`), `KafkaTransactionManager`. RabbitMQ'da durable queue + `MessageDeliveryMode.PERSISTENT`, `CachingConnectionFactory.setPublisherConfirmType(CORRELATED)` va `RabbitTemplate#setConfirmCallback`/`setReturnsCallback`, consumer'da `AcknowledgeMode.MANUAL`. JMS'da `DeliveryMode.PERSISTENT` va `CLIENT_ACKNOWLEDGE`. DB-ga asoslangan yondashuv: Spring Integration `JdbcChannelMessageStore` bilan persistent `QueueChannel`, yoki transactional outbox jadvali (`@Transactional` + alohida publisher).

**Qo'llanish keyslari:**
- To'lov va buyurtma hodisalarini broker restart'idan keyin ham yo'qotmaslik.
- Transactional outbox bilan DB commit va event publikatsiyasini atomar qilish.
- Moliyaviy hisobot uchun audit event'larini durable topic'da saqlash.
- Consumer deploy/rollout paytida in-flight xabarlarni saqlab qolish.
- Multi-AZ replikatsiya bilan butun data center yo'qolishiga chidamlilik.

**Ehtiyot bo'ling:** Persistence o'z-o'zidan "exactly-once" bermaydi - failover va retry paytida duplicate bo'ladi, shuning oqibatida iste'molchi idempotent bo'lishi yoki dedup store ishlatishi kerak. `acks=all` va `fsync` har bir xabar uchun latency'ni bir necha barobar oshiradi; past qiymatli telemetriya yoki metrika oqimida bu kafolatni talab qilish ortiqcha xarajat. Shuningdek DB va broker'ni bitta XA tranzaksiyaga bog'lashga urinmang - outbox pattern soddaroq va ishonchliroq.

## 15.13 Kanal adapteri (Channel Adapter)

**Tavsif:** Messaging tizimidan tashqarida turgan tizimni (fayl tizimi, baza, HTTP endpoint, SMTP, legacy API) messaging kanaliga ulaydigan ko'prikdir. Adapter bir tomonda domen/transport protokolini "gaplashadi", ikkinchi tomonda esa `Message<?>` bilan ishlaydi, shu bilan ilova kodi integratsiya mexanikasidan ajraladi. Inbound adapter tashqi tizimdan ma'lumot olib kanalga qo'yadi, outbound adapter kanaldan olib tashqi tizimga uzatadi. Natijada tashqi tizimni almashtirsangiz, faqat adapter o'zgaradi - oqimning qolgan qismi tegmaydi.

**Spring'da qayerda uchraydi:** Spring Integration'ning asosiy qurilish bloki: polling inbound uchun `@InboundChannelAdapter` + `MessageSource` implementatsiyalari (`FileReadingMessageSource`, `JdbcPollingChannelAdapter`, `MailReceivingMessageSource`) `SourcePollingChannelAdapter` ichida ishlaydi; event-driven inbound uchun `MessageProducerSupport` merosxo'rlari (`JmsMessageDrivenEndpoint`, `KafkaMessageDrivenChannelAdapter`, `AmqpInboundChannelAdapter`). Outbound tomonda `@ServiceActivator` bilan ro'yxatga olingan `JmsSendingMessageHandler`, `KafkaProducerMessageHandler`, `FileWritingMessageHandler`. Java DSL'da `IntegrationFlow.from(Files.inboundAdapter(dir))`, `Kafka.messageDrivenChannelAdapter(cf, "topic")`, `.handle(Jms.outboundAdapter(jmsTemplate))`. Spring Cloud Stream 4.x/5.x da `Supplier<T>` va `Consumer<T>` bean'lari binder orqali aynan shu rolni bajaradi, Debezium esa baza uchun CDC inbound adapter sifatida ishlatiladi.

**Qo'llanish keyslari:**
- Legacy tizim tashlab ketgan CSV fayllarni katalogdan o'qib Kafka topic'ga yuborish.
- SFTP'dan kelgan bank to'lov fayllarini `Sftp.inboundAdapter` bilan oqimga tortish.
- Baza jadvalidagi `status = NEW` qatorlarni JDBC polling adapter bilan yig'ib qayta ishlash.
- IMAP pochta qutisidan kelgan murojaatlarni ticket tizimiga aylantirish.
- Mikroservis chiqaradigan event'larni outbound adapter orqali RabbitMQ exchange'iga uzatish.

**Ehtiyot bo'ling:** Polling adapter'da `poller` fixed-delay va `maxMessagesPerPoll` noto'g'ri sozlansa, baza yoki fayl tizimini "o'ldirib" qo'yadi; inbound adapter ichida biznes logika yozmang - adapter faqat tarjimon bo'lishi kerak. Shuningdek polling adapter bir nechta instance'da ishlasa, taqsimlangan lock (`JdbcLockRegistry`, `RedisLockRegistry`) yoki leader election bo'lmasa, bitta yozuv bir necha marta qayta ishlanadi.

## 15.14 Xabar ko'prigi (Messaging Bridge)

**Tavsif:** Ikkita alohida messaging tizimi yoki ikkita kanal o'rtasida xabarlarni oddiy nusxalab o'tkazadigan minimal ulanishdir. Ko'prik xabarni o'zgartirmaydi: bir kanaldan oladi, boshqasiga qo'yadi, lekin yo'l-yo'lakay transport, transaksiya chegarasi yoki kanal turini (pollable ↔ subscribable) almashtiradi. Bu migratsiya davrida eski va yangi broker'ni parallel ishlatish uchun eng arzon usul. Shu bilan ikkita infratuzilma bir-birini bilmasdan "gaplashadi".

**Spring'da qayerda uchraydi:** Spring Integration'da `BridgeHandler`, deklarativ `@BridgeFrom` va `@BridgeTo` annotatsiyalari, XML'da `<int:bridge/>`, Java DSL'da `IntegrationFlow.from("inChannel").bridge().channel("outChannel")`. `QueueChannel` (pollable) ni `DirectChannel` ga ulashda ko'prik `poller` bilan birga ishlatiladi. Kross-broker holatda inbound adapter + ko'prik + outbound adapter kombinatsiyasi qo'llanadi (masalan `AmqpInboundChannelAdapter` → `bridge()` → `KafkaProducerMessageHandler`). Spring Cloud Stream'da bir nechta binder'ni (`spring.cloud.stream.binders.*`) bitta ilovada sozlab, kiruvchi binding'ni chiquvchi binding'ga `Function<Message<?>, Message<?>>` bilan ulash ham amalda ko'prikdir.

**Qo'llanish keyslari:**
- ActiveMQ'dan Kafka'ga bosqichma-bosqich migratsiyada ikkala brokerda bir xil xabar oqimini saqlash.
- On-prem RabbitMQ va cloud'dagi Amazon SQS o'rtasida hybrid oqim qurish.
- `QueueChannel` dagi buffer'langan xabarlarni belgilangan tezlikda `DirectChannel` consumer'lariga uzatish.
- Hamkor tashkilotning brokeridan kelgan xabarlarni ichki korporativ kanalga o'tkazish.
- Test kontur bilan prod kontur o'rtasida read-only trafik replikatsiyasi qilish.

**Ehtiyot bo'ling:** Ko'prik ikki transportni bog'laganda yagona atomar transaksiya bo'lmaydi - ikki fazali commit o'rniga idempotentlik va duplikat bardoshligini loyihalash kerak, aks holda xabar yo'qoladi yoki ikkilanadi. Ko'prikni "vaqtinchalik" deb kiritib, keyin arxitekturada abadiy qoldirish ham tipik xato: migratsiya tugash muddatini boshidan belgilang.

## 15.15 Xabar sahnasi / Message Bus (Message Bus)

**Tavsif:** Ko'plab ilovalarni bitta umumiy messaging infratuzilmasi, kelishilgan kanal nomlari va yagona kanonik ma'lumot modeli orqali birlashtiruvchi arxitektura uslubidir. Yangi ilova bus'ga "ulanadi" - qolgan tizimlar haqida hech narsa bilmaydi, faqat umumiy xabar formatini va adapter konvensiyasini biladi. Bu Message Channel, Message Router, Message Translator va Channel Adapter patternlarining birlashgan, tashkilot miqyosidagi ko'rinishi. Natijada integratsiya point-to-point ulanishlar o'rniga markazlashgan "orqa miya" ko'rinishini oladi.

**Spring'da qayerda uchraydi:** Spring Cloud Stream (binder abstraksiyasi + `spring.cloud.stream.bindings.*` destinatsiyalari) zamonaviy, yengil bus sifatida eng ko'p ishlatiladi; Spring Cloud Bus (`spring-cloud-bus`, `RemoteApplicationEvent`, `RefreshRemoteApplicationEvent`) esa konfiguratsiya va boshqaruv event'lari uchun maxsus bus. Yagona ilova doirasida Spring Integration kanallari + `PublishSubscribeChannel` "ichki bus" vazifasini bajaradi, Spring Framework'ning `ApplicationEventMulticaster`'i ham JVM ichidagi bus hisoblanadi. Kanonik model uchun odatda Avro/Protobuf sxemalari Confluent Schema Registry bilan yoki CloudEvents formati (`spring-cloud-function` ichidagi `CloudEventMessageUtils`) tanlanadi.

**Qo'llanish keyslari:**
- Bank ichidagi 40 ta tizim uchun yagona "customer updated" kanonik event oqimini qurish.
- Spring Cloud Bus bilan barcha instance'larda `/actuator/refresh` ni bir vaqtda ishga tushirish.
- Yangi analytics servisini mavjud bus'ga consumer sifatida ulab, manba tizimlarga tegmaslik.
- Retail platformada buyurtma hodisalarini warehouse, billing va CRM'ga bir topic'dan tarqatish.
- Monolitdan ajratilgan mikroservislarni umumiy event bus orqali bosqichma-bosqich ko'chirish.

**Ehtiyot bo'ling:** Bus tez orada taqsimlangan monolitga aylanishi mumkin: kanonik model har bir yangi talabda o'sib, barcha consumer'larni bir vaqtda deploy qilishga majbur qiladi - shuning uchun sxema evolyutsiyasini (backward/forward compatibility) kun birinchi talabi qiling. Bus'ga biznes logika va marshrutlash qoidalarini yig'ish (klassik ESB anti-patterni) uni yagona nosozlik nuqtasi va tashkiliy "tirbandlik" ga aylantiradi.

## 15.16 Buyruq xabari (Command Message)

**Tavsif:** Qabul qiluvchidan muayyan amalni bajarishni so'rovchi xabar turidir: payload'da bajarilishi kerak bo'lgan operatsiya nomi va parametrlar bo'ladi. Bu messaging orqali amalga oshirilgan asinxron RPC - jo'natuvchi kimga va nima qilish kerakligini biladi, shuning uchun bog'liqlik (coupling) event xabarga nisbatan yuqori. Odatda bitta aniq qabul qiluvchiga, point-to-point kanal orqali yuboriladi. Nomlash ham buyruq mayliga mos bo'ladi: `CreateInvoice`, `ReserveStock`.

**Spring'da qayerda uchraydi:** Spring Integration'da buyruq oddiy POJO payload bo'lib `Message<ReserveStockCommand>` ko'rinishida ketadi va `@ServiceActivator` yoki `@MessagingGateway` metodi uni qabul qiladi; `GenericMessage` va `MessageBuilder.withPayload(cmd).setHeader("commandType", ...)` bilan quriladi. `@KafkaListener`, `@RabbitListener`, `@JmsListener` metodlari buyruq handler'i sifatida eng ko'p uchraydigan shakl. Spring Integration'ning `ControlBus` (`Integration.controlBus()` / `ExpressionControlBusFactoryBean`) infratuzilma buyruqlari uchun maxsus misoldir. CQRS'ni to'liq qurmoqchi bo'lsangiz, Spring bilan ko'p ishlatiladigan Axon Framework'ning `CommandGateway`/`@CommandHandler` yoki Spring Modulith'ning event/komanda ajratish yondashuvi qo'llanadi.

**Qo'llanish keyslari:**
- Buyurtma servisidan omborga `ReserveStock` buyrug'ini navbat orqali yuborish.
- PDF hisobot generatsiyasini uzoq ishlovchi worker'ga buyruq xabari bilan topshirish.
- SMS/push yuborish topshiriqlarini notification servisining command queue'siga qo'yish.
- Control bus orqali ishlab turgan adapter'ni runtime'da `@adapterName.stop()` bilan to'xtatish.
- Batch qayta hisoblashni admin paneldan buyruq xabari sifatida ishga tushirish.

**Ehtiyot bo'ling:** Buyruq xabarini event bilan aralashtirmang - buyruqni `PublishSubscribeChannel` ga qo'ysangiz, bitta amal necha marta bajariladi; har doim point-to-point kanaldan foydalaning. Qayta yetkazish (at-least-once) tufayli har bir buyruq handler'i idempotent bo'lishi va buyruq `messageId` bo'yicha deduplikatsiya (`IdempotentReceiverInterceptor`, `MetadataStore`) qilinishi kerak.

## 15.17 Hujjat xabari (Document Message)

**Tavsif:** Qabul qiluvchiga ma'lumotning o'zini - biznes hujjat yoki data strukturasini - uzatish uchun ishlatiladigan xabar turidir. Jo'natuvchi qabul qiluvchi bu ma'lumot bilan nima qilishini belgilamaydi va natijani kutmaydi; muhim bo'lgani - hujjatning yetib borishi. Buyruqdan farqi: niyat emas, mazmun uzatiladi; event'dan farqi: vaqt sezgirligi past va payload odatda to'liq va katta bo'ladi. Shuning uchun u ko'pincha "data transfer" integratsiyalarida asosiy shakl bo'ladi.

**Spring'da qayerda uchraydi:** `Message<OrderDto>` yoki `Message<byte[]>` payload'i, `MessageBuilder` bilan quriladi va `MessageConverter` (`MappingJackson2MessageConverter`, Spring AMQP'ning `Jackson2JsonMessageConverter`, Spring AMQP 4.x/Boot 4 liniyasida Jackson 3 asosidagi `JacksonJsonMessageConverter`) orqali serializatsiya qilinadi. Spring Integration'da `ObjectToJsonTransformer`, `JsonToObjectTransformer`, fayl hujjatlari uchun `FileToByteArrayTransformer` ishlatiladi. Katta hujjatlar uchun `ClaimCheckInTransformer`/`ClaimCheckOutTransformer` + `MessageStore` (yoki S3) kombinatsiyasi standart yechim; `@Payload` va `@Headers` annotatsiyalari listener metodlarida hujjatni ajratib olishga xizmat qiladi.

**Qo'llanish keyslari:**
- Kunlik to'lov registrini (ming qatorli hujjat) to'lov provayderiga uzatish.
- Mahsulot katalogi snapshot'ini e-commerce frontend servisiga yuborish.
- Hisob-faktura XML hujjatini soliq integratsiya moduliga topshirish.
- ETL oqimida normalizatsiya qilingan mijoz yozuvlarini data warehouse'ga yuborish.
- Mikroservislar o'rtasida hisobot natijalarini JSON payload sifatida almashish.

**Ehtiyot bo'ling:** Katta hujjatni to'g'ridan-to'g'ri payload qilib yuborish broker limitlarini (Kafka `max.message.bytes`, Rabbit frame o'lchami) va heap'ni buzadi - bunday holatda Claim Check yoki obyekt saqlovga havola ishlating. Shuningdek hujjat sxemasini versiyalamasdan o'zgartirish barcha consumer'larni sindiradi: yangi maydonlarni ixtiyoriy qilib qo'shing, mavjudlarini olib tashlamang.

## 15.18 Hodisa xabari (Event Message)

**Tavsif:** Tizimda yuz bergan o'zgarish haqida xabar beruvchi, o'tgan zamonda nomlanadigan xabar turidir: `OrderPlaced`, `PaymentFailed`. Jo'natuvchi kim tinglashini bilmaydi va javob kutmaydi, shuning uchun bu eng kam bog'liqlikka ega shakl va publish-subscribe kanallari bilan birga ishlatiladi. Event odatda kichik, immutable va vaqt belgisiga ega bo'ladi; consumer'lar o'z reaksiyasini mustaqil tanlaydi. Shu sababli yangi consumer qo'shish producer kodini o'zgartirishni talab qilmaydi.

**Spring'da qayerda uchraydi:** JVM ichida `ApplicationEventPublisher.publishEvent`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)`; Spring Data JDBC/JPA'da `AbstractAggregateRoot` va `@DomainEvents`/`@AfterDomainEventPublication` orqali domen event'lari. Spring Integration'da `PublishSubscribeChannel` va `ApplicationEventPublishingMessageHandler` (DSL: `.handle(new ApplicationEventPublishingMessageHandler())`), teskari yo'nalishda `ApplicationEventListeningMessageProducer`. Tashqi event'lar uchun `KafkaTemplate`, `RabbitTemplate` (fanout exchange), Spring Cloud Stream `Supplier`, Spring Modulith'ning `@ApplicationModuleListener` va event publication registry (`spring-modulith-events-*`) transactional outbox'ni beradi; CDC yondashuvida Debezium outbox jadvalini kuzatadi.

**Qo'llanish keyslari:**
- `OrderPlaced` event'iga billing, ombor va notifikatsiya servislari mustaqil reaksiya qilishi.
- Audit log'ni domen event'laridan to'ldirish, biznes kodga tegmasdan.
- Cache invalidatsiyasini `EntityUpdated` event'i bilan klaster bo'ylab tarqatish.
- Foydalanuvchi ro'yxatdan o'tgach analytics va onboarding oqimlarini ishga tushirish.
- Event sourcing uchun audit qilinadigan o'zgarishlar jurnalini yuritish.

**Ehtiyot bo'ling:** Event ichida javob yoki ko'rsatma kutish (aslida buyruq bo'lgan "event") arxitekturani yashirin bog'liqlik bilan to'ldiradi; event faqat fakt haqida xabar berishi kerak. Tranzaksiya commit bo'lmasdan event chiqarish esa consumer'ning mavjud bo'lmagan ma'lumotni o'qishiga olib keladi - `@TransactionalEventListener(AFTER_COMMIT)` yoki transactional outbox ishlating.

## 15.19 So'rov-javob (Request-Reply)

**Tavsif:** Jo'natuvchi so'rov xabarini yuborib, qabul qiluvchidan alohida kanal orqali javob xabarini oladigan ikki yo'nalishli almashish patterni. U ikki kanaldan iboratdir: request channel (odatda doimiy, umumiy) va reply channel (ko'pincha har bir so'rov uchun vaqtinchalik). Chaqiruvchi kutib turishi (sinxron, blocking) yoki javobni keyinroq callback bilan olishi (asinxron) mumkin. Bu messaging ustida RPC semantikasini qurish usuli bo'lib, javobni so'rov bilan bog'lash uchun Return Address va Correlation Identifier bilan birga ishlaydi.

**Spring'da qayerda uchraydi:** `@MessagingGateway` interfeysi (`MessagingGatewaySupport`, `GatewayProxyFactoryBean`) qaytish tipi `void` bo'lmasa avtomatik request-reply qiladi; past darajada `MessagingTemplate.sendAndReceive`. Transport darajasida `JmsTemplate.sendAndReceive` (`TemporaryQueue`), `RabbitTemplate.convertSendAndReceive` va `AsyncRabbitTemplate` (direct reply-to), Kafka uchun `ReplyingKafkaTemplate` va `@SendTo` bilan javob qaytaruvchi `@KafkaListener`. `Jms.outboundGateway(...)`, `Amqp.outboundGateway(...)`, `Http.outboundGateway(...)` DSL komponentlari ham shu patternni ifodalaydi; reaktiv oqimda `Mono<T>` qaytaruvchi gateway metodi ishlatiladi.

```java
@MessagingGateway(defaultRequestChannel = "priceRequests")
public interface PricingGateway {
    @Gateway(replyTimeout = 2000)
    Mono<Price> quote(QuoteRequest request);
}
```

**Qo'llanish keyslari:**
- Fraud-scoring servisidan to'lovni tasdiqlashdan oldin baho olish.
- Legacy mainframe'dan JMS gateway orqali mijoz balansini so'rash.
- Narx kalkulyatsiyasini alohida compute servisiga topshirib natijani kutish.
- Kafka asosidagi "enrichment" servisidan ma'lumot to'ldirish so'rovi.
- Hamkor API'sidan hujjat statusini so'rab, javobni REST controller'ga qaytarish.

**Ehtiyot bo'ling:** `replyTimeout` ni cheksiz yoki juda uzun qoldirish thread pool'ni band qilib ilovani muzlatadi; messaging ustida sinxron so'rov-javob qurishdan oldin oddiy HTTP yetarli emasligiga ishonch hosil qiling. Shuningdek har bir so'rov uchun yangi `TemporaryQueue` yaratish broker'da katta yuk tug'diradi - Rabbit'da direct reply-to, JMS'da esa correlation ID bilan umumiy reply queue'ni afzal ko'ring.

## 15.20 Qaytish manzili (Return Address)

**Tavsif:** So'rov xabari ichida javob qaysi kanalga yuborilishi kerakligini ko'rsatuvchi header'dir. Shu bilan qabul qiluvchi javob manzilini hard-code qilmaydi va bitta servis turli chaqiruvchilarga xizmat qila oladi. Manzil odatda header'da bo'ladi, payload'da emas - chunki u marshrutlash metama'lumoti. Natijada request-reply dinamik, ko'p-chaqiruvchili muhitda ham ishlaydi.

**Spring'da qayerda uchraydi:** Spring Integration'da `MessageHeaders.REPLY_CHANNEL` (ko'pincha `TemporaryReplyChannel` obyekti sifatida) va unga juft bo'lgan `MessageHeaders.ERROR_CHANNEL`; gateway javobni shu header asosida topadi. JMS'da `Message.setJMSReplyTo(Destination)` va `JmsHeaders.REPLY_TO`, AMQP'da `MessageProperties.setReplyTo` / `amqp_replyTo` header'i hamda `amq.rabbitmq.reply-to` pseudo-queue; Kafka'da `KafkaHeaders.REPLY_TOPIC` va `KafkaHeaders.REPLY_PARTITION`, ularni `ReplyingKafkaTemplate` to'ldiradi, `@SendTo` esa statik alternativa beradi. `HeaderEnricher` (`.enrichHeaders(h -> h.replyChannel(...))`) bilan qaytish manzilini oqim ichida o'rnatish mumkin.

**Qo'llanish keyslari:**
- Bitta umumiy "pricing" servisi turli consumer'larga o'z reply topic'iga javob qaytarishi.
- Mobil va web gateway'lar bir xil backend oqimidan turli kanallarga javob olishi.
- Xatolarni asosiy javob kanalidan ajratib `errorChannel` ga yo'naltirish.
- Saga qadamida javobni keyingi bosqich kanaliga to'g'ridan-to'g'ri yuborish.
- Test muhitida javobni mock `QueueChannel` ga qaytarib tekshirish.

**Ehtiyot bo'ling:** Qaytish manzilini tashqi, ishonchsiz chaqiruvchidan olingan header'dan ko'r-ko'rona ishlatish xavfli - zararli manzil bilan tizimingiz begona topic'ga yozishi mumkin, shuning uchun whitelist bilan validatsiya qiling. Splitter/aggregator orqali o'tganda `replyChannel` header'i yo'qolib qolishi mumkin: `HeaderEnricher` yoki `@Gateway` orqali uni ataylab saqlab o'tkazing.

## 15.21 Korrelyatsiya identifikatori (Correlation Identifier)

**Tavsif:** Javob xabarini uni keltirib chiqargan so'rov bilan (yoki bir guruhga tegishli xabarlarni bir-biri bilan) bog'lash uchun ishlatiladigan unikal qiymatdir. Qabul qiluvchi javobga shu identifikatorni ko'chirib qo'yadi, chaqiruvchi esa javoblarni to'g'ri so'rovga moslaydi - bu asinxron, ko'p so'rov parallel ketayotgan muhitda majburiy. Xuddi shu mexanizm aggregator'ning xabarlarni guruhlashi va taqsimlangan tracing uchun ham asos bo'ladi. Identifikator har doim header'da yuritiladi.

**Spring'da qayerda uchraydi:** Spring Integration'da `IntegrationMessageHeaderAccessor.CORRELATION_ID` ("correlationId") header'i, `CorrelationStrategy` interfeysi va uning implementatsiyalari `HeaderAttributeCorrelationStrategy`, `ExpressionEvaluatingCorrelationStrategy`; `AbstractCorrelatingMessageHandler` (aggregator/resequencer) shu asosda `MessageGroupStore` ichida guruh yig'adi. Transportda: JMS `JMSCorrelationID` (`JmsHeaders.CORRELATION_ID`), AMQP `MessageProperties.correlationId` / `amqp_correlationId`, Kafka `KafkaHeaders.CORRELATION_ID`. Kuzatuv tomonida Micrometer Tracing (Boot 3.x/4.x) `traceId`/`spanId` ni MDC'ga qo'yadi va bu log korrelyatsiyasining standart usulidir.

```java
@Bean
public IntegrationFlow aggregateFlow() {
    return f -> f.aggregate(a -> a
        .correlationStrategy(new HeaderAttributeCorrelationStrategy("orderId"))
        .releaseStrategy(g -> g.size() == 3)
        .expireGroupsUponCompletion(true));
}
```

**Qo'llanish keyslari:**
- Umumiy reply queue'dan kelgan javoblarni to'g'ri chaqiruvchi thread'iga moslash.
- Bir buyurtmaga tegishli uch xil servis javobini aggregator bilan birlashtirish.
- Taqsimlangan tizimda bitta biznes operatsiyaning loglarini `traceId` bo'yicha yig'ish.
- Saga/process manager'da uzun ishlovchi tranzaksiya holatini kuzatish.
- Support so'rovida mijoz operatsiyasini uchidan uchiga qayta tiklash.

**Ehtiyot bo'ling:** Correlation ID ni biznes kaliti (masalan buyurtma raqami) bilan almashtirib yuborish takroriy va bir-biriga qo'shilib ketgan guruhlarga olib keladi - biznes kalit kerak bo'lsa alohida header'da yuboring. Aggregator'da `expireGroupsUponCompletion` va `MessageGroupStoreReaper` sozlanmasa, tugallanmagan guruhlar `MessageStore` da abadiy qolib memory leak yaratadi.

## 15.22 Xabarlar ketma-ketligi (Message Sequence)

**Tavsif:** Katta ma'lumotni bir nechta xabarga bo'lib yuborishda har bir bo'lakka ketma-ketlik metama'lumotini qo'shish patterni: guruh identifikatori, tartib raqami va umumiy soni (yoki oxirgi bo'lak belgisi). Qabul qiluvchi shu ma'lumot bilan bo'laklarni to'g'ri tartibda yig'adi va hech biri yo'qolmaganini tekshiradi. Bu splitter-aggregator juftligining asosiy ishlash mexanizmi. Noto'g'ri tartibda kelgan xabarlarni qayta tartiblash ham shu metama'lumotga tayanadi.

**Spring'da qayerda uchraydi:** Spring Integration `IntegrationMessageHeaderAccessor` ning `SEQUENCE_NUMBER`, `SEQUENCE_SIZE`, `SEQUENCE_DETAILS` va `CORRELATION_ID` header'larini `AbstractMessageSplitter` avtomatik qo'yadi (`applySequence` default `true`), `DefaultAggregatingMessageHandler` esa `SequenceSizeReleaseStrategy` bilan guruhni yopadi. Tartiblash uchun `ResequencingMessageHandler` va DSL'dagi `.resequence()`, `.split()`, `.aggregate()` operatorlari mavjud. Kafka'da tartib faqat bitta partition ichida kafolatlanadi, shuning uchun bir xil key bilan yozish (`KafkaHeaders.KEY`, `Partitioner`) amaliy yechim; `MessageGroupStore` (`JdbcMessageStore`, `RedisMessageStore`) bo'laklarni holat sifatida saqlaydi.

**Qo'llanish keyslari:**
- 1 GB CSV faylni qatorlar bo'yicha bo'lib yuborib, natijalarni yana bitta hisobotga yig'ish.
- Bank kunlik fayl paketini bo'laklab yuborishda hech bir bo'lak yo'qolmaganini tekshirish.
- Tartibi buzilgan IoT telemetriya paketlarini resequencer bilan vaqt bo'yicha tiklash.
- Ko'p sahifali API natijasini bo'laklab qayta ishlab, oxirida yagona javob qaytarish.
- Hujjat imzolash oqimida sahifalarni to'g'ri tartibda qayta birlashtirish.

**Ehtiyot bo'ling:** Resequencer va aggregator holat saqlaydi - in-memory `SimpleMessageStore` bilan ilova restart bo'lsa yarim yig'ilgan guruhlar yo'qoladi, shuning uchun persistent store va `MessageGroupStoreReaper` timeout'ini sozlang. Agar oqim bir nechta instance'da parallel ishlasa, bitta guruh bo'laklari turli node'larga tushib hech qachon yopilmaydi: umumiy `JdbcMessageStore` + `LockRegistry` yoki partition-affinity (Kafka key) kerak.

## 15.23 Xabar amal qilish muddati (Message Expiration)

**Tavsif:** Xabarga "shu vaqtdan keyin qiymatsiz" degan muddat belgilash patterni: muddat o'tgach xabar iste'mol qilinmaydi, balki o'chiriladi yoki dead letter kanaliga yo'naltiriladi. Bu eskirgan ma'lumot bilan ish bajarilishini oldini oladi va navbatlarning cheksiz o'sishini cheklaydi. Muddat odatda header'da absolyut vaqt yoki TTL sifatida yuritiladi. Qabul qiluvchi yoki broker muddatni tekshirish mas'uliyatini oladi.

**Spring'da qayerda uchraydi:** Spring Integration'da `MessageHeaders.EXPIRATION_DATE` header'i va uni filtrlash uchun `UnexpiredMessageSelector` (`QueueChannel.setMessageSelector` yoki `MessageFilter` bilan), guruh muddatlari uchun `MessageGroupStoreReaper` + aggregator `groupTimeout`. Transportda: JMS `JmsTemplate.setTimeToLive`/`MessageProducer.setTimeToLive`, AMQP `MessageProperties.setExpiration` (per-message) va queue argumenti `x-message-ttl` + `x-dead-letter-exchange` (Spring AMQP'da `QueueBuilder.ttl(...).deadLetterExchange(...)`), Kafka'da topic darajasidagi `retention.ms`. Request-reply tomonida `@Gateway(replyTimeout = ...)`, `RabbitTemplate.setReplyTimeout`, `ReplyingKafkaTemplate` ning reply timeout'i xuddi shu maqsadga xizmat qiladi; kechiktirish uchun esa `DelayHandler`/`.delay()` ishlatiladi.

**Qo'llanish keyslari:**
- Birja narx kotirovkalarini 2 sekunddan keyin eskirgan deb tashlab yuborish.
- OTP/SMS yuborish buyruqlarini 60 sekundlik TTL bilan navbatga qo'yish.
- Real-time dashboard uchun telemetriya xabarlarini TTL bilan cheklab backlog o'sishini to'xtatish.
- Muddati o'tgan to'lov so'rovlarini DLQ'ga yo'naltirib qo'lda tekshirishga berish.
- Consumer uzilganda eskirgan buyruqlarning qayta yetkazilishini oldini olish.

**Ehtiyot bo'ling:** Muddat o'tgan xabarni jimgina tashlab yuborish ma'lumot yo'qolishiga teng - har doim dead letter kanalini va monitoring/alert'ni yoqib qo'ying. Rabbit'da klassik queue'da TTL faqat navbat boshidagi xabarga qo'llanishi (head-of-line effekti) va tarqoq server/klient soatlari (clock skew) absolyut `expirationDate` ni ishonchsiz qilishini hisobga oling.

## 15.24 Format ko'rsatkichi (Format Indicator)

**Tavsif:** Xabar payload'ining formatini yoki sxema versiyasini xabarning o'zida e'lon qilish patterni, shunda qabul qiluvchi uni qanday parse qilishni aniq biladi. Ko'rsatkich uchta shaklda bo'ladi: versiya raqami, format/kontent turi yoki tashqi sxemaga havola (schema registry ID). Bu producer va consumer'larni mustaqil rivojlantirishga, bitta kanalda bir necha versiyani birga yashashiga imkon beradi. Metama'lumot payload emas - u header'da turishi kerak.

**Spring'da qayerda uchraydi:** `MessageHeaders.CONTENT_TYPE` ("contentType") Spring Messaging'da standart ko'rsatkich, `MessageConverter` implementatsiyalari shu asosda tanlanadi. Spring AMQP'da `MessageProperties.contentType` va `__TypeId__` header'i (`DefaultJackson2JavaTypeMapper`, `Jackson2JsonMessageConverter`; Spring AMQP 4.x da Jackson 3 asosidagi `JacksonJsonMessageConverter`), `setTypePrecedence`/trusted packages bilan sozlanadi. Spring for Apache Kafka'da `JsonSerializer.ADD_TYPE_INFO_HEADERS`, `JsonDeserializer` ning `spring.json.type.mapping` va `spring.json.trusted.packages` xususiyatlari; Avro/Protobuf holatida Confluent `KafkaAvroSerializer` schema ID ni payload prefiksida yuboradi. Spring Cloud Stream'da `spring.cloud.stream.bindings.<name>.content-type`, CloudEvents uchun `ce-specversion`/`ce-type` header'lari va `CloudEventMessageUtils` mavjud.

**Qo'llanish keyslari:**
- Bitta topic'da `OrderCreated` event'ining v1 va v2 sxemalarini birga yashashiga ruxsat berish.
- JSON va Avro payload'larni bir kanalda qabul qilib, converter'ni contentType bo'yicha tanlash.
- Legacy fixed-length va yangi XML formatdagi fayllarni bitta oqimda ajratib qayta ishlash.
- Hamkor integratsiyasida kelgan hujjat versiyasini header orqali aniqlab mos transformer'ga yo'naltirish.
- Schema registry bilan consumer'ni producer deploy'iga bog'liq bo'lmagan holda rivojlantirish.

**Ehtiyot bo'ling:** Java sinf nomini (`__TypeId__`, type info headers) format ko'rsatkichi sifatida ishlatish producer va consumer'ni bir xil paket strukturasiga bog'lab qo'yadi va ishonchsiz manbadan kelganda deserializatsiya zaifligiga yo'l ochadi - trusted packages/type mapping ni albatta cheklang. Versiyani faqat payload ichida yashirish esa marshrutlashni payload'ni to'liq parse qilishga majbur qiladi: ko'rsatkichni header'da saqlang.

## 15.25 Kontent asosidagi marshrutizator (Content-Based Router)

**Tavsif:** Xabarni uning mazmuni - payload turi, header qiymati yoki payload ichidagi maydon - asosida bir nechta mumkin bo'lgan kanaldan bittasiga yo'naltiradi. Jo'natuvchi qabul qiluvchini bilmaydi: u faqat routerning input kanaliga yozadi, qaror esa markazlashgan bir joyda qabul qilinadi. Bu `if/else` zanjirini biznes logikasidan ajratib, marshrutlash qoidalarini deklarativ qiladi. Router xabarni o'zgartirmaydi - faqat uni qayerga borishini hal qiladi.

**Spring'da qayerda uchraydi:** Spring Integration'da `AbstractMessageRouter` ierarxiyasi: `PayloadTypeRouter`, `HeaderValueRouter`, `ExpressionEvaluatingRouter` (SpEL), `MethodInvokingRouter`. POJO metodiga `@Router` annotatsiyasini qo'yib, kanal nomi yoki `MessageChannel` qaytarish mumkin. Java DSL'da `.route(...)` operatori `RouterSpec` orqali `channelMapping(...)` va `subFlowMapping(...)` beradi. Apache Camel'da bu `choice().when(...).otherwise(...)`, Spring Cloud Stream'da esa `RoutingFunction` va `spring.cloud.stream.function.routing.enabled` bilan amalga oshiriladi.

**Qo'llanish keyslari:**
- To'lov xabarini `paymentMethod` header qiymatiga ko'ra card, bank transfer yoki wallet oqimiga yuborish.
- Yagona webhook endpoint'iga kelgan event'larni `eventType` bo'yicha tegishli handler flow'ga tarqatish.
- Buyurtmani summasiga qarab avtomatik tasdiqlash yoki manual review navbatiga yo'naltirish.
- Hujjatni MIME turiga ko'ra PDF, XML va CSV parserlariga ajratish.
- Mijoz segmentiga (VIP / standart) qarab turli SLA'li ishlov berish oqimini tanlash.

**Ehtiyot bo'ling:** Routerning `channelMapping` xaritasi vaqt o'tib o'nlab tarmoqqa aylansa, u yashirin "god object"ga aylanadi - bunday holda mas'uliyatni bir nechta kichik routerga yoki qabul qiluvchining o'zidagi filterga bo'lish yaxshiroq. `defaultOutputChannel` berilmagan bo'lsa, mos kelmagan xabar `MessageDeliveryException` bilan yiqiladi, shuning uchun har doim default yoki `resolutionRequired=false` strategiyasini ongli tanlang.

## 15.26 Xabar filtri (Message Filter)

**Tavsif:** Kanaldagi xabarlar oqimidan faqat berilgan shartga javob beradiganlarini o'tkazib, qolganlarini chetlab o'tadi. Routerdan farqi: filter bitta output kanalga ega va "o'tsin yoki o'tmasin" degan binar qarorni qabul qiladi. Bu qabul qiluvchini o'ziga aloqasi yo'q xabarlarni tekshirish yukidan xalos qiladi. Rad etilgan xabarni jimgina tashlash, alohida kanalga yuborish yoki exception bilan qaytarish mumkin.

**Spring'da qayerda uchraydi:** Spring Integration'da `MessageFilter` handler'i `MessageSelector` strategiyasi bilan ishlaydi (`ExpressionEvaluatingMessageSelector`, `PayloadTypeSelector`, `UnexpiredMessageSelector`, `MetadataStoreSelector`). POJO metodiga `@Filter` qo'yib `boolean` qaytarish, Java DSL'da `.filter(...)` yoki `.filter(Order.class, o -> o.getTotal() > 0)` ishlatiladi. Muhim sozlamalar: `discardChannel`, `throwExceptionOnRejection`, `discardWithinAdvice`. Kafka/AMQP darajasida bu `RecordFilterStrategy` (`FilteringMessageListenerAdapter`) va `@KafkaListener(filter = "...")` orqali, Camel'da `filter()` orqali bajariladi.

**Qo'llanish keyslari:**
- Kafka topic'idagi barcha event'lardan faqat `tenantId` ushbu instansiyaga tegishli bo'lganlarini qayta ishlash.
- Takroriy (duplicate) xabarlarni `MetadataStoreSelector` bilan idempotent receiver sifatida bloklash.
- Test yoki shadow trafik deb belgilangan xabarlarni production handler'ga o'tkazmaslik.
- Fayl kataloglaridan faqat `.csv` kengaytmali va minimal hajmdan katta fayllarni olish.
- Muddati o'tgan (TTL tugagan) xabarlarni `UnexpiredMessageSelector` bilan tashlab, downstream'ni bekor ishdan saqlash.

**Ehtiyot bo'ling:** Default holatda rad etilgan xabar hech qanday iz qoldirmasdan yo'qoladi - bu production'da "xabar yo'qolgan" degan eng og'riqli debug keysini tug'diradi, shuning uchun `discardChannel`ni log yoki audit oqimiga ulang. Filterni biznes qoidasi uchun ishlatganda, "nega o'tmadi" savoliga javob beradigan sababni header'da saqlamasa, keyinchalik qoidani isbotlash imkonsiz bo'ladi.

## 15.27 Dinamik marshrutizator (Dynamic Router)

**Tavsif:** Marshrutlash qoidalari kod ichida qotib qolmaydi, balki runtime'da - qabul qiluvchilarning o'zlari tomonidan ro'yxatdan o'tish yoki tashqi konfiguratsiya orqali - o'zgaradi. Router "control channel" yoki tashqi manba orqali yangi kanal xaritasini oladi va keyingi xabarlarni unga ko'ra yuboradi. Bu yangi qabul qiluvchi qo'shilganda tizimni qayta deploy qilish zaruratini yo'q qiladi. Haqiqiy dinamikada har bir xabar uchun keyingi qadam alohida hisoblanadi.

**Spring'da qayerda uchraydi:** `AbstractMappingMessageRouter` runtime'da `setChannelMapping(key, channelName)` va `removeChannelMapping(key)` metodlarini beradi; bu metodlar `@ManagedOperation` sifatida JMX'ga ham chiqariladi va Control Bus (`.controlBus()`) orqali xabar bilan chaqirilishi mumkin. Dinamik qarorni `@Router` qo'yilgan metodda `MessageChannel` yoki kanal nomini DB/`Environment`/Redis'dan o'qib qaytarish bilan yozish eng keng tarqalgan yo'l; kanal nomini `BeanFactoryChannelResolver` hal qiladi. Java DSL'da `.route(m -> resolver.next(m))` va `DynamicPeriodicTrigger`, Camel'da esa bevosita `dynamicRouter()` EIP mavjud.

**Qo'llanish keyslari:**
- Multi-tenant platformada yangi tenant qo'shilganda uning ishlov berish kanalini deploy'siz ro'yxatga olish.
- Feature flag (LaunchDarkly, Unleash) qiymatiga qarab trafikni eski va yangi implementatsiya orasida ko'chirish.
- A/B test yoki canary uchun xabarlarning foizli ulushini yangi consumer'ga yuborish.
- Admin UI'dan boshqariladigan biznes qoidalarini DB'da saqlab, marshrutni ular bo'yicha hisoblash.
- Qabul qiluvchi servis sog'lig'i (health) yo'qolganda uni marshrut xaritasidan vaqtincha chiqarib tashlash.

**Ehtiyot bo'ling:** Runtime'da o'zgaradigan marshrut - kuzatuvi eng qiyin holat: qaysi xabar qayerga ketgani hech qayerda yozilmasa, incident paytida tiklash imkonsiz, shuning uchun tanlangan marshrutni header va trace span attribute'iga yozing. Xarita mutable bo'lgani uchun uni bir nechta thread o'qiydi va yozadi - `ConcurrentHashMap` yoki `AbstractMappingMessageRouter`ning o'z API'sidan foydalaning, oddiy `HashMap`ni tashqaridan o'zgartirmang.

## 15.28 Qabul qiluvchilar ro'yxati (Recipient List)

**Tavsif:** Bitta xabarning nusxasini bir vaqtda bir nechta, dinamik hisoblangan qabul qiluvchiga yuboradi. Content-Based Routerdan farqi: bu "bittasini tanlash" emas, "bir nechtasini tanlash"; publish-subscribe kanaldan farqi esa - ro'yxat statik obuna emas, har bir xabar uchun hisoblanadi va shart bilan filtrlanishi mumkin. Shu tariqa jo'natuvchi obunachilar ro'yxatini bilmagan holda selektiv broadcast qiladi.

**Spring'da qayerda uchraydi:** Spring Integration'da `RecipientListRouter` (va `RecipientListRouterManagement` interfeysi orqali JMX/Control Bus'dan `addRecipient`/`removeRecipient`) aynan shu patternni beradi. Har bir recipient'ga SpEL selektor berish mumkin, ya'ni shartli ro'yxat hosil bo'ladi. Java DSL'da `.routeToRecipients(r -> r.recipient("audit").recipientFlow("payload.vip", sf -> ...))` ishlatiladi; XML'da `<int:recipient-list-router>`. Oddiy statik broadcast uchun esa `PublishSubscribeChannel` (yoki `.publishSubscribeChannel(...)`) yetarli, Camel'da bu `recipientList()`.

**Qo'llanish keyslari:**
- Yangi buyurtma event'ini bir yo'la ombor, billing va analytics servislariga jo'natish.
- Narx so'rovini bir nechta yetkazib beruvchiga yuborib, keyin javoblarni Aggregator bilan to'plash.
- Mijoz sozlamalariga ko'ra bildirishnomani email, SMS va push kanallaridan faqat tanlanganlariga yuborish.
- Barcha moliyaviy xabarlarning nusxasini asosiy oqim bilan birga audit/compliance oqimiga yuborish.
- Migratsiya davrida xabarni eski va yangi tizimga parallel yozib, natijalarni taqqoslash (dual-write shadow).

**Ehtiyot bo'ling:** Default holatda `RecipientListRouter` barcha recipient'larga bir xil thread'da ketma-ket yuboradi - bitta sekin yoki yiqilgan qabul qiluvchi butun yuborishni bloklaydi yoki yarim yo'lda to'xtatadi, shuning uchun kritik bo'lmagan tarmoqlarni `ExecutorChannel` yoki broker orqasiga oling. Payload mutable obyekt bo'lsa, barcha recipient'lar ayni bir instansiyani oladi va biri uni o'zgartirsa boshqalari buziladi - immutable payload ishlating.

## 15.29 Ajratuvchi (Splitter)

**Tavsif:** Bir nechta element saqlagan kompozit xabarni mustaqil ishlov berilishi mumkin bo'lgan alohida xabarlarga bo'ladi. Har bir chiqish xabariga korrelyatsiya identifikatori, tartib raqami va umumiy soni (sequence details) qo'yiladi, shunda keyinchalik Aggregator yoki Resequencer ularni qayta yig'ishi mumkin. Bu katta batch'ni parallel va oqim (streaming) tarzda qayta ishlashga yo'l ochadi. Splitter - Composed Message Processor va Scatter-Gather'ning asosiy qurilish bloki.

**Spring'da qayerda uchraydi:** Spring Integration'da `AbstractMessageSplitter` va uning `DefaultMessageSplitter`, `ExpressionEvaluatingSplitter`, `MethodInvokingSplitter` implementatsiyalari; POJO uchun `@Splitter`, Java DSL'da `.split()`. Maxsus splitterlar: `FileSplitter` (fayl qatorlari bo'yicha, `markers` opsiyasi bilan), `XPathMessageSplitter`, `JsonToObjectTransformer` bilan birga ishlatiladigan SpEL `#jsonPath`. Splitter default holatda `applySequence=true` bo'lib `correlationId`, `sequenceNumber`, `sequenceSize` header'larini qo'yadi; `Iterator` yoki `Flux` qaytarish esa barcha elementni xotiraga yuklamaslikka imkon beradi. Camel'da bu `split().streaming()`.

**Qo'llanish keyslari:**
- 500 ming qatorli CSV faylni `FileSplitter` bilan qatorlarga bo'lib, oqim tarzida yuklash.
- Bitta buyurtma xabaridagi har bir pozitsiyani (order line) alohida ombor so'roviga aylantirish.
- Bulk API chaqiruvidagi massivni alohida domain event'larga ajratib Kafka'ga yozish.
- Ko'p sahifali hisobotni sahifalarga bo'lib parallel render qilish.
- Katta XML batch hujjatini `XPathMessageSplitter` orqali tranzaksiyalarga ajratish.

**Ehtiyot bo'ling:** Collection'ni to'liq xotiraga yuklab bo'lib tashlash katta fayllarda darhol `OutOfMemoryError` keltiradi - splitter metodidan `Iterator`/`Stream` qaytarib streaming rejimida ishlang va downstream'da backpressure yoki `QueueChannel` sig'imini hisobga oling. Tranzaksiya chegarasi ham o'zgaradi: bo'lingan xabarlar bir xil thread'da ketmasa, ularning muvaffaqiyati endi atomik emas, shuning uchun qisman muvaffaqiyat (partial failure) stsenariysini ongli loyihalash kerak.

## 15.30 Agregator (Aggregator)

**Tavsif:** Bir-biriga bog'liq bir nechta xabarni to'plab, ular to'liq bo'lganda yagona natija xabari hosil qiladi - Splitter'ning teskarisi va Scatter-Gather'ning yig'ish qismi. Uchta qarorga tayanadi: xabarlarni qanday guruhlash (correlation), guruh qachon tugallangan deb hisoblash (release) va natijani qanday birlashtirish (aggregation). Guruhlar hali to'lmagan paytda saqlanishi kerak, shuning uchun agregator - stateful komponent. Timeout mexanizmi hech qachon to'lmaydigan guruhlar tizimda abadiy qolib ketishini oldini oladi.

**Spring'da qayerda uchraydi:** Spring Integration'da `AggregatingMessageHandler` + `CorrelationStrategy` (`HeaderAttributeCorrelationStrategy`), `ReleaseStrategy` (`SequenceSizeReleaseStrategy`, `SimpleSequenceSizeReleaseStrategy`, `MessageCountReleaseStrategy`), `MessageGroupProcessor`. POJO uchun `@Aggregator`, `@CorrelationStrategy`, `@ReleaseStrategy` annotatsiyalari; Java DSL'da `.aggregate(a -> a.correlationStrategy(...).releaseStrategy(...).groupTimeout(5000))`. State uchun `MessageGroupStore`: `SimpleMessageStore` (xotira), `JdbcMessageStore`, `RedisMessageStore`, `MongoDbMessageStore`, `JpaMessageStore`. Muhim sozlamalar: `groupTimeout`, `sendPartialResultOnExpiry`, `expireGroupsUponCompletion`, `MessageGroupStoreReaper`.

```java
@Bean
IntegrationFlow aggregateOrderLines(JdbcMessageStore store) {
    return IntegrationFlow.from("orderLines")
        .aggregate(a -> a.messageStore(store)
            .correlationExpression("headers['orderId']")
            .releaseStrategy(g -> g.size() == g.getSequenceSize())
            .groupTimeout(10_000)
            .sendPartialResultOnExpiry(true)
            .expireGroupsUponCompletion(true))
        .channel("completedOrders")
        .get();
}
```

**Qo'llanish keyslari:**
- Splitter bilan bo'lingan buyurtma pozitsiyalarining natijalarini bitta javobga qayta yig'ish.
- Bir nechta microservisdan kelgan javoblardan yagona API response qurish (API composition).
- Sensor o'lchovlarini 1 daqiqalik oynalarga to'plab o'rtacha qiymat hisoblash.
- Mijozga bir nechta alohida bildirishnoma yuborish o'rniga ularni bitta digest email'ga birlashtirish.
- Kafka'ga yozishdan oldin yozuvlarni 500 talik batch'larga yig'ib, I/O sonini kamaytirish.

**Ehtiyot bo'ling:** Xotiradagi `SimpleMessageStore` bilan ishlagan agregator - instansiya restart bo'lganda yarim guruhlarni, ya'ni to'lovlarni va buyurtmalarni yo'qotadi; cluster'da esa bir xil correlation key'li xabarlar turli pod'larga tushib guruh hech qachon to'lmaydi, shuning uchun persistent `MessageGroupStore` va partitioning/ sticky routing shart. `groupTimeout` yoki reaper sozlanmagan bo'lsa, to'lmagan guruhlar sekin-asta store'ni to'ldirib, klassik xotira oqishiga (memory leak) aylanadi.

## 15.31 Qayta tartiblovchi (Resequencer)

**Tavsif:** Tartibi buzilib kelgan xabarlarni ularning tartib raqami bo'yicha qayta to'g'ri ketma-ketlikka keltirib chiqaradi. Agregatordan farqi: xabarlarni birlashtirmaydi - ularni bittalab, lekin to'g'ri tartibda chiqaradi. Buning uchun kutilayotgan raqam kelmaguncha keyingi xabarlarni buferda ushlab turadi. Parallel ishlov berish yoki bir nechta transport yo'li tartibni buzgan joylarda ketma-ketlikni tiklash uchun kerak.

**Spring'da qayerda uchraydi:** Spring Integration'da `ResequencingMessageHandler` va uning `ResequencingMessageGroupProcessor`'i; POJO darajasida `@Resequencer`, Java DSL'da `.resequence(r -> r.releasePartialSequences(true).messageStore(store))`, XML'da `<int:resequencer>`. U Splitter qo'ygan `correlationId`, `sequenceNumber`, `sequenceSize` header'laridan (`IntegrationMessageHeaderAccessor` konstantalari) foydalanadi va agregator bilan bir xil `MessageGroupStore` infratuzilmasiga tayanadi. Camel'da bu `resequence()` (batch yoki stream rejimi), Kafka'da esa tartib asosan partition kaliti bilan ta'minlanadi.

**Qo'llanish keyslari:**
- Parallel consumer'lar qayta ishlagan hodisalarni DB'ga yozishdan oldin asl tartibiga keltirish.
- Chunk'larga bo'lib yuborilgan fayl bo'laklarini to'g'ri tartibda qayta birlashtirishga tayyorlash.
- Buyurtma holati o'zgarishlarini (created → paid → shipped) ketma-ketligi buzilmasidan state machine'ga berish.
- Bir nechta yo'l (multi-route) orqali kelgan bank tranzaksiyalarini vaqt tamg'asi bo'yicha tiklash.
- Replikatsiya oqimida CDC event'larini LSN raqami bo'yicha tartiblash.

**Ehtiyot bo'ling:** Agar bitta xabar butunlay yo'qolsa, resequencer kutilayotgan raqamni abadiy kutib oqimni to'xtatib qo'yadi - `releasePartialSequences`, timeout va reaper'ni albatta sozlang. Shuningdek bu pattern tabiatan buferlaydi va ketma-ketlikni talab qiladi, ya'ni parallelizmni yo'q qiladi: kerakli tartibni transport darajasida (bir xil partition kaliti) ta'minlash ko'pincha arzonroq yechim.

## 15.32 Birlashtirilgan xabar protsessori (Composed Message Processor)

**Tavsif:** Splitter, marshrutlash/ishlov berish va Aggregator'ni yagona mantiqiy komponentga birlashtiradi: kompozit xabar bo'laklarga bo'linadi, har bir bo'lak o'z yo'li bilan qayta ishlanadi, so'ng natijalar bitta javobga yig'iladi. Tashqaridan bu oddiy "so'rov → javob" protsessori kabi ko'rinadi, ichidagi murakkablik yashiriladi. Shu bilan har xil turdagi elementlarni o'z mutaxassis handler'lariga yuborib, keyin yaxlit natija qaytarish mumkin bo'ladi.

**Spring'da qayerda uchraydi:** Spring Integration'da bu alohida sinf emas, balki kompozitsiya: `IntegrationFlow` ichida `.split()` → `.route(...)`/`.handle(...)` → `.aggregate(...)` zanjiri, ko'pincha `.channel(c -> c.executor(taskExecutor))` bilan parallel qilinadi. Bo'laklarni ichki oqimlarda ishlash uchun `RouterSpec.subFlowMapping(...)` va `IntegrationFlows`ning sub-flow (`IntegrationFlowDefinition`) imkoniyatlari ishlatiladi; butun kompozitsiyani `@Bean` sifatida bitta nom ostida e'lon qilib, tashqi dunyoga `MessagingGateway` (`@MessagingGateway`) orqali bitta metod ko'rinishida beriladi. Apache Camel'da bu `split(...).aggregationStrategy(...)` yoki `multicast().aggregationStrategy(...)` bilan to'g'ridan-to'g'ri qo'llanadi.

**Qo'llanish keyslari:**
- Savatchadagi har bir mahsulotni o'z yetkazib beruvchi servisiga yuborib, yakuniy narx va muddatni bitta javobga yig'ish.
- Aralash turdagi hujjat paketini (PDF, XML, rasm) turli parserlarga bo'lib, keyin yagona metadata obyekti qurish.
- Ko'p valyutali to'lov fayli pozitsiyalarini valyuta bo'yicha turli clearing oqimlariga yuborib, umumiy hisobot qaytarish.
- Buyurtma validatsiyasini bir nechta mustaxassis qoidalar servisiga bo'lib, natijalardan yagona validatsiya hisobotini yig'ish.
- Bir nechta tashqi API'dan olingan bo'laklardan mijozning 360-daraja profilini qurish.

**Ehtiyot bo'ling:** Bu pattern asosan Splitter va Aggregator xatolarini meros qilib oladi: bitta bo'lak yiqilsa yoki kechiksa, butun kompozit javob osilib qoladi - har bir sub-flow uchun timeout, retry va `sendPartialResultOnExpiry` siyosatini oldindan belgilang. Ichida bir nechta EIP yashirinishi kuzatuvni qiyinlashtiradi, shuning uchun correlation id'ni uchidan uchiga olib o'tib, Micrometer Tracing bilan span'larni bog'lang.

## 15.33 Sochish-yig'ish (Scatter-Gather)

**Tavsif:** So'rovni bir vaqtda bir nechta qabul qiluvchiga tarqatadi (scatter), ularning javoblarini kutadi va bitta natijaga yig'adi (gather). Scatter qismi publish-subscribe kanal yoki Recipient List bilan, gather qismi esa Aggregator bilan amalga oshiriladi. Asosiy qiymati - parallellik: eng sekin javob qancha bo'lsa, umumiy kechikish shunga teng, ketma-ket chaqiruvlar yig'indisiga emas. Javoblarning hammasini yoki eng yaxshisini, yoki timeout ichida kelganlarini olish strategiyasini tanlash mumkin.

**Spring'da qayerda uchraydi:** Spring Integration'da to'g'ridan-to'g'ri `ScatterGatherHandler` mavjud: Java DSL'da `.scatterGather(scatterer, gatherer, spec -> spec.gatherTimeout(3000))`, XML'da `<int:scatter-gather>`. Scatterer sifatida `RecipientListRouterSpec` yoki `PublishSubscribeChannel`, gatherer sifatida `AggregatorSpec` beriladi; `errorChannel` va `requiresReply` xatolarni boshqaradi. Reaktiv muhitda xuddi shu g'oya `Mono.zip(...)` / `Flux.merge(...)` bilan (Spring WebFlux `WebClient`), imperativ kodda esa `CompletableFuture.allOf(...)` yoki Java 21+ `StructuredTaskScope` bilan yozilishi mumkin; Resilience4j `TimeLimiter` esa timeout qismini qo'shadi.

```java
@Bean
IntegrationFlow quoteFlow() {
    return IntegrationFlow.from("quoteRequests")
        .scatterGather(
            r -> r.applySequence(true)
                  .recipient("bankA").recipient("bankB").recipient("bankC"),
            a -> a.releaseStrategy(g -> g.size() == 3),
            s -> s.gatherTimeout(2_000).errorChannel("quoteErrors"))
        .channel("bestQuote")
        .get();
}
```

**Qo'llanish keyslari:**
- Bir nechta bank yoki sug'urta kompaniyasidan narx taklifi so'rab, eng arzonini tanlash (auktsion stsenariysi).
- Aviachipta qidiruvini bir vaqtda bir nechta GDS provayderiga yuborib, natijalarni birlashtirish.
- Dashboard uchun 5 ta turli microservisdan ma'lumot olib, bitta javob qurish.
- Fraud skoringni bir nechta mustaqil model/servisga parallel yuborib, ularning ovozini yig'ish (ensemble).
- Mahsulot qoldig'ini bir nechta ombor tizimidan parallel so'rab, umumiy mavjudlikni hisoblash.

**Ehtiyot bo'ling:** `gatherTimeout` berilmasa, bitta javob bermagan qabul qiluvchi chaqiruv thread'ini cheksiz ushlab, thread pool'ni tugatadi va kaskad nosozlikka olib keladi - timeout, circuit breaker va fallback majburiy. Shuningdek bu pattern yukni N barobar oshiradi: har bir so'rov barcha provayderni urgani uchun downstream rate limit va xarajatni hisoblab, kerak bo'lsa keshlash yoki qisman scatter qiling.

## 15.34 Marshrut varaqasi (Routing Slip)

**Tavsif:** Xabarning o'ziga bosib o'tishi kerak bo'lgan qadamlar ro'yxatini (marshrut varaqasini) ilova qiladi; har bir qadam o'z ishini bajarib, ro'yxatdagi keyingi manzilga uzatadi. Shu bilan markazlashgan orkestrator ham, qadamlar orasidagi qattiq bog'lanish ham kerak bo'lmaydi - marshrut ma'lumot sifatida ko'chib yuradi. Ketma-ketlik har bir xabar uchun boshida (yoki yo'lda) dinamik hisoblanishi mumkin. Bu Process Manager'ga nisbatan yengilroq, lekin faqat chiziqli oqimlar uchun mos muqobil.

**Spring'da qayerda uchraydi:** Spring Integration patternni `IntegrationMessageHeaderAccessor.ROUTING_SLIP` header'i orqali qo'llab-quvvatlaydi: `HeaderEnricher`ning `<int:routing-slip>` sub-elementi yoki Java DSL'da `.enrichHeaders(h -> h.headerExpression(...))`/`.routingSlip(...)` bilan kanal nomlari va `RoutingSlipRouteStrategy` implementatsiyalari ro'yxati beriladi. `AbstractMessageProducingHandler` o'zining `outputChannel`i bo'lmaganda avval `routingSlip` header'ini, keyin `replyChannel`ni ko'radi, shuning uchun qadamlar bir-birini bilmasligi mumkin. Apache Camel'da bu bevosita `routingSlip(header("slip"))` EIP ko'rinishida mavjud.

**Qo'llanish keyslari:**
- Hujjat tasdiqlash yo'lini (bo'lim boshlig'i → moliya → yuridik) hujjat turiga qarab boshida belgilash.
- Mijozga ko'rsatiladigan onboarding qadamlarini tarif rejasiga qarab dinamik tuzish.
- Mahsulot turiga bog'liq ravishda qayta ishlash bosqichlarini (validatsiya → boyitish → narxlash) tanlash.
- Bir martalik migratsiya yoki tuzatish oqimida qadamlar ketma-ketligini konfiguratsiyadan boshqarish.
- Compliance talabiga ko'ra ma'lum mamlakat xabarlariga qo'shimcha tekshiruv qadamini kiritish.

**Ehtiyot bo'ling:** Routing slip faqat chiziqli ketma-ketlik uchun: shartli tarmoqlanish, parallel qadamlar yoki compensation kerak bo'lsa, u tezda o'qib bo'lmas holatga keladi - bunday holda Process Manager yoki haqiqiy workflow engine tanlang. Marshrut xabar header'ida yurgani uchun uni tashqi manbadan (masalan foydalanuvchi so'rovidan) to'g'ridan-to'g'ri olish xavfli: ro'yxatni faqat ichki, oq ro'yxatdagi kanal nomlaridan yasang.

## 15.35 Jarayon menejeri (Process Manager)

**Tavsif:** Ko'p qadamli, uzoq davom etadigan jarayonni markazlashgan holda boshqaradigan stateful komponent: har bir qadam yakunlanganda kelgan xabarga qarab keyingi qadamni hal qiladi va jarayon holatini saqlaydi. Routing Slip'dan farqi - marshrut xabarda emas, menejerda; u shartli tarmoqlanish, parallel qadamlar, timeout va compensation (teskari amal) ni ham boshqaradi. Distributed tranzaksiyalarda bu orchestration-based Saga sifatida tanilgan. Jarayon holati davomli saqlangani uchun restart va qayta tiklash mumkin bo'ladi.

**Spring'da qayerda uchraydi:** Spring Integration'da bu stateful router yoki `MessageStore`ga tayangan maxsus handler bilan yoziladi - tayyor `ProcessManager` sinfi yo'q. Odatda Spring Statemachine ishlatiladi (`@EnableStateMachine`, `StateMachineFactory`, `StateMachinePersister`, `StateMachineRuntimePersister` bilan JPA/Redis persistence) yoki Axon Framework'ning saga'si (`@Saga`, `@StartSaga`, `@SagaEventHandler`, `@EndSaga`, `DeadlineManager`). Og'irroq keyslarda BPMN engine'lar - Camunda 8 (Zeebe `spring-boot-starter-camunda-sdk`, `@JobWorker`), Flowable yoki Temporal'ning Java SDK'si Spring Boot bilan integratsiya qilinadi. Qadamlar orasidagi transport sifatida Kafka/AMQP va `@KafkaListener`/`@RabbitListener` qoladi.

**Qo'llanish keyslari:**
- Buyurtma sagasi: to'lovni ushlash → omborni rezervlash → yetkazib berishni rejalashtirish, har bir qadam yiqilsa compensation bajarish.
- Mijoz onboardingi: KYC tekshiruvi, hujjat yuklash va hisob ochishni kunlar davomida kuzatish.
- Kredit arizasi jarayonini skoring, manual review va tasdiqlash bosqichlari bilan boshqarish.
- Abonementni bekor qilish oqimida qaytarish, resurslarni o'chirish va bildirishnomalarni muvofiqlashtirish.
- Uzoq ETL pipeline'ida qadamlarni kuzatib, xatolikdan keyin aynan to'xtagan joydan davom etish.

**Ehtiyot bo'ling:** Process Manager - tizimning markaziy nuqtasi: unga juda ko'p biznes qoida yuklansa, u taqsimlangan arxitekturadagi yangi monolitga va yagona nosozlik nuqtasiga aylanadi, shuning uchun unda faqat koordinatsiya qolsin, domen logikasi servislarda. Jarayon holatini davomli saqlamasdan va qadamlarni idempotent qilmasdan qurish - restart'dan keyin takroriy to'lov yoki yarim qolgan saga degani; shuningdek har bir uzoq qadam uchun timeout/deadline belgilash shart.

## 15.36 Xabar brokeri (Message Broker)

**Tavsif:** Ko'plab jo'natuvchi va qabul qiluvchi o'rtasida nuqta-nuqta ulanishlar o'rniga markaziy hub joylashtiradi: barcha xabarlar brokerga boradi, broker esa ularni obuna va marshrut qoidalariga ko'ra tarqatadi. Natijada N×M integratsiya bog'lanishlari N+M ga tushadi, jo'natuvchi qabul qiluvchining joylashuvi va hatto mavjudligini bilmaydi. Broker, shu bilan birga, xabarlarni davomli saqlash, qayta urinish, dead-letter va yukni tekislash (buffering) mas'uliyatini ham oladi. Bu EIP'ning "hub-and-spoke" asosiy infratuzilma patterni.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x starter'lari brokerlar bilan ishlashni avtomatlashtiradi: `spring-boot-starter-amqp` (RabbitMQ - `RabbitTemplate`, `@RabbitListener`, `RabbitListenerContainerFactory`), `spring-kafka` (`KafkaTemplate`, `@KafkaListener`, `DefaultErrorHandler` + `DeadLetterPublishingRecoverer`), `spring-boot-starter-artemis`/`spring-jms` (`JmsTemplate`, `@JmsListener`), `spring-pulsar`. Spring Integration ularga adapter beradi: `Amqp.inboundAdapter(...)`, `Kafka.messageDrivenChannelAdapter(...)`, `Jms.inboundGateway(...)`; yuqori darajadagi abstraksiya - Spring Cloud Stream binder'lari. WebSocket/STOMP dunyosida esa `@EnableWebSocketMessageBroker` bilan `enableSimpleBroker()` (ichki broker) yoki `enableStompBrokerRelay()` (tashqi broker) ishlatiladi.

**Qo'llanish keyslari:**
- O'nlab microservis o'rtasidagi event almashinuvini Kafka topic'lari orqali markazlashtirish.
- Pik yuklamada so'rovlarni navbatga qo'yib, consumer'larni o'z tezligida ishlashga qo'yish (load leveling).
- Qabul qiluvchi vaqtincha o'chganda xabarlarni durable queue'da saqlab, keyin yetkazib berish.
- Bitta domen event'ini bir nechta mustaqil obunachiga fan-out qilish (topic exchange yoki consumer group).
- Legacy JMS tizimini yangi servislar bilan broker orqali, kodini o'zgartirmasdan bog'lash.

**Ehtiyot bo'ling:** Broker kuchli bo'lgani uchun unga marshrutlash va transformatsiya logikasini ko'chirishga kuchli vasvasa bo'ladi - bu "aqlli broker, ahmoq servislar" anti-patternini va yagona nosozlik nuqtasini tug'diradi; biznes logikasi servislarda qolsin, broker esa transport bo'lib qolsin. Shuningdek broker avtomatik ravishda "exactly-once" yoki global tartib bermaydi: idempotent consumer, partition kaliti, dead-letter topic va retry siyosatini o'zingiz loyihalashingiz kerak, aks holda yo'qotilgan yoki takrorlangan xabarlar production'da chiqadi.

---

[&larr; 14. Microservices patternlari](14-microservices-patternlari.md) · [Mundarija](README.md) · [16. Enterprise Integration Patterns II: transformatsiya, endpointlar, boshqaruv, event patternlar &rarr;](16-enterprise-integration-patterns-ii.md)
