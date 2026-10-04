<!-- doc: architect | chapter: 29 | part: V. Atrof ekotizim: operatsion haqiqat -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 29. Kafka operatsion haqiqati: partition, lag, rebalance, idempotentlik (Kafka in Production)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [29.1 Kafka modeli: topic, partition, offset, consumer group](#291-kafka-modeli-topic-partition-offset-consumer-group)
- [29.2 Partition soni tanlash: parallellik chegarasi va keyin o'zgartirish qiyinligi](#292-partition-soni-tanlash-parallellik-chegarasi-va-keyin-ozgartirish-qiyinligi)
- [29.3 Kalit tanlash va tartib kafolati: tartib faqat partition ichida](#293-kalit-tanlash-va-tartib-kafolati-tartib-faqat-partition-ichida)
- [29.4 Producer sozlamalari: acks, enable.idempotence, linger.ms, batch.size](#294-producer-sozlamalari-acks-enableidempotence-lingerms-batchsize)
- [29.5 Consumer sozlamalari: max.poll.records, max.poll.interval.ms va rebalance sababi](#295-consumer-sozlamalari-maxpollrecords-maxpollintervalms-va-rebalance-sababi)
- [29.6 Offset commit strategiyasi va kamida bir marta yetkazish oqibati](#296-offset-commit-strategiyasi-va-kamida-bir-marta-yetkazish-oqibati)
- [29.7 Idempotent iste'molchi qurish: PostgreSQL da ishlov berilgan xabar jadvali](#297-idempotent-istemolchi-qurish-postgresql-da-ishlov-berilgan-xabar-jadvali)
- [29.8 Consumer lag ni o'lchash va ogohlantirish chegarasi qo'yish](#298-consumer-lag-ni-olchash-va-ogohlantirish-chegarasi-qoyish)
- [29.9 Xato xabar bilan nima qilish: qayta urinish topic va dead letter topic](#299-xato-xabar-bilan-nima-qilish-qayta-urinish-topic-va-dead-letter-topic)
- [29.10 Sxema o'zgarishi va orqaga moslik](#2910-sxema-ozgarishi-va-orqaga-moslik)
- [29.11 Tranzaksiya va xabar yuborish nomuvofiqligi: nega ikki fazali commit emas](#2911-tranzaksiya-va-xabar-yuborish-nomuvofiqligi-nega-ikki-fazali-commit-emas)
- [29.12 Spring Kafka da asosiy sozlamalar va xato ishlovchisi](#2912-spring-kafka-da-asosiy-sozlamalar-va-xato-ishlovchisi)
- [29.13 Qaror jadvali: oddiy yondashuv va arxitektor yondashuvi](#2913-qaror-jadvali-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [29.14 Amalda qo'llash](#2914-amalda-qollash)

</details>



Kafka ko'pchilik loyihada "xabar navbati" deb tushuniladi, lekin u aslida taqsimlangan, saqlanadigan va qayta o'qiladigan log. Shu farqni tushunmagan jamoa partition sonini tasodifiy tanlaydi, offset ni avtomatik commit qiladi, rebalance paytida xabarlarni ikki marta ishlaydi va dead letter topic ni hech kim o'qimaydi. Bu bob Kafka ning operatsion mexanikasini ko'rib chiqadi: ichkarida nima sodir bo'ladi, qaysi sozlama qanday raqamga ta'sir qiladi va arxitektor qaysi joyda qaror qabul qilishi kerak. To'lov servisi, buyurtma oqimi va ombor qoldig'i misollari orqali boramiz.

## 29.1 Kafka modeli: topic, partition, offset, consumer group

Topic nomdan boshqa hech narsa emas, u faqat partition ro'yxatini birlashtiradi. Haqiqiy birlik partition: u broker diskidagi append-only segment fayllar ketma-ketligi. Har bir yozuv partition ichida monoton o'suvchi `offset` oladi, va bu offset o'zgarmaydi hamda qayta ishlatilmaydi. Shuning uchun Kafka da xabar "o'chirilmaydi", u faqat `retention.ms` yoki `retention.bytes` chegarasidan oshganda segment bilan birga tashlanadi.

Consumer group ikkita vazifani bajaradi. Birinchisi: partition larni group a'zolari o'rtasida taqsimlash, bitta partition bir vaqtda bitta a'zoga tegishli. Ikkinchisi: group nomi bo'yicha offset ni `__consumer_offsets` ichki topic da saqlash. Shundan muhim xulosa chiqadi: bir xil ma'lumotni ikki xil maqsadda ishlatmoqchi bo'lsang, ikkita alohida `group.id` olasan, ularning offset lari bir-biriga aralashmaydi. To'lov tasdiqlarini bir group hisob-kitob uchun, boshqa group hisobot uchun o'qiydi va ular bir-birini sekinlashtirmaydi.

Broker hech qachon "bu xabarni kim o'qidi" ni bilmaydi. U faqat group ning commit qilgan offset ini biladi. Bu arxitektura bir nechta oqibat beradi: iste'molchi orqaga qaytib o'qishi mumkin, offset ni qo'lda siljitib reprocessing qilish mumkin, va "xabar yo'qoldi" degan muammolar deyarli har doim offset boshqaruvidagi xato bo'lib chiqadi.

## 29.2 Partition soni tanlash: parallellik chegarasi va keyin o'zgartirish qiyinligi

Bitta consumer group ichidagi samarali parallellik partition sonidan oshmaydi. Agar topic da 6 partition bo'lsa, 10 instansiya ishga tushirsang, 4 tasi bo'sh turadi. Shuning uchun partition soni kelgusidagi eng katta instansiya sonidan kamida 2-3 barobar ko'p bo'lishi kerak. Buyurtma topic uchun amaliy boshlang'ich nuqta: 12 yoki 24 partition, chunki ular 2, 3, 4, 6, 8, 12 instansiyaga teng bo'linadi.

Lekin partition bepul emas. Har bir partition broker da ochiq fayl deskriptorlari, alohida index va replikatsiya uchun fetch oqimi talab qiladi. Bitta broker da bir necha ming partition replikasi bo'lsa, controller ishi va ishga tushish vaqti sezilarli oshadi. Amaliy mo'ljal: bitta broker ga 2000-4000 partition replikasi, klaster bo'ylab 50000 dan oshmaslik. Producer tomonida ham har partition uchun alohida batch buferi ushlanadi, ya'ni `batch.size` ni partition soniga ko'paytirib xotirani hisobla.

Eng og'ir tuzoq: partition sonini oshirish mumkin, kamaytirish mumkin emas. Oshirganda esa standart partitioner `hash(key) % partitionCount` ishlatgani uchun kalitlarning partition ga tushishi o'zgaradi. Bu degani eski xabarlar bir partition da, yangi xabarlar boshqa partition da qoladi va bitta buyurtma uchun tartib buziladi. Shuning uchun partition sonini production da jimgina oshirish xavfli qaror. To'g'ri yo'l: yangi topic yaratish, ikkita topic ni parallel o'qish va ma'lum bir vaqtdan keyin eskisini o'chirish.

## 29.3 Kalit tanlash va tartib kafolati: tartib faqat partition ichida

Kafka global tartibni kafolatlamaydi. U faqat bitta partition ichida yozuv tartibini kafolatlaydi. Shuning uchun "buyurtma hodisalari to'g'ri ketma-ketlikda kelishi kerak" talabi to'g'ridan-to'g'ri kalit tanlash qaroriga aylanadi: `order_id` ni kalit qilsang, bitta buyurtmaning `CREATED`, `PAID`, `SHIPPED` hodisalari bir partition ga tushadi va tartib saqlanadi.

Kalitni juda keng tanlash ham xato. Agar kalit `tenant_id` bo'lsa va bitta yirik mijoz butun trafikning 40 foizini bersa, o'sha partition "issiq" bo'lib qoladi: bitta iste'molchi orqada qoladi, qolganlari bo'sh turadi. Bunday hollarda kalitni `tenant_id + ':' + order_id` ko'rinishida kengaytirish yoki yirik mijoz uchun alohida topic ajratish kerak bo'ladi.

Kalit `null` bo'lsa, Kafka 2.4 dan keyingi standart partitioner sticky usulda ishlaydi: batch to'lguncha bitta partition ga yozadi, keyin boshqasiga o'tadi. Bu throughput uchun yaxshi, lekin tartib kafolati umuman yo'q. Audit log yoki metrika uchun bu to'g'ri qaror, to'lov holati uchun emas.

```java
// Buyurtma hodisasi: kalit sifatida order_id, shunda tartib saqlanadi.
// Partition ichidagi tartib kafolati faqat shu kalit tanlovi bilan ishlaydi.
public void publishOrderEvent(OrderEvent event) {
    ProducerRecord<String, OrderEvent> record = new ProducerRecord<>(
            "order.events",              // topic
            event.orderId(),             // kalit: bir buyurtma -> bir partition
            event);
    // Trace id ni header ga qo'shamiz, payload ni buzmaymiz.
    record.headers().add("traceId", tracer.currentTraceId().getBytes(UTF_8));
    kafkaTemplate.send(record)
            .whenComplete((meta, ex) -> {
                if (ex != null) {
                    // Bu yerda faqat log yetarli emas: outbox qatorini qayta urinishga qoldiramiz.
                    log.error("order.events yozilmadi orderId={}", event.orderId(), ex);
                } else {
                    log.debug("yozildi partition={} offset={}",
                            meta.partition(), meta.offset());
                }
            });
}
```

## 29.4 Producer sozlamalari: acks, enable.idempotence, linger.ms, batch.size

`acks` yozuvning qachon "muvaffaqiyatli" deb hisoblanishini belgilaydi. `acks=1` leader diskka yozishini kutadi, lekin leader o'sha zahoti qulasa xabar yo'qoladi. `acks=all` barcha in-sync replika tasdiqlashini kutadi va `min.insync.replicas=2` bilan birgalikda replikatsiya faktori 3 da bitta broker yo'qolishiga chidaydi. To'lov va buyurtma hodisalari uchun yagona to'g'ri tanlov `acks=all`. Narxi: taxminan 2-5 ms qo'shimcha latency bir xil data center ichida.

`enable.idempotence=true` producer ga sequence number beradi, shunda tarmoq retry sababli paydo bo'ladigan dublikat broker tomonida tashlanadi. Kafka 3.0 dan keyin bu standart qiymat, lekin u `acks=all`, `retries>0` va `max.in.flight.requests.per.connection<=5` ni talab qiladi. Agar kimdir `acks=1` qo'ysa, idempotentlik jim o'chadi yoki konfiguratsiya xatosi beradi. Shuning uchun bu uchta parametrni birga ko'rib chiqish kerak.

`linger.ms` va `batch.size` throughput va latency o'rtasidagi tanlovni boshqaradi. Standart `linger.ms=0` degani producer kutmaydi, natijada kichik batch lar ko'p bo'ladi. `linger.ms=5` qo'yish ko'p hollarda throughput ni 2-3 barobar oshiradi va faqat 5 ms latency qo'shadi. `batch.size=16384` standart, yuqori oqim uchun 65536 ga ko'tarish va `compression.type=lz4` yoqish amaliy kombinatsiya.

```properties
# Producer: ishonchlilik birinchi, keyin throughput.
acks=all
enable.idempotence=true
max.in.flight.requests.per.connection=5
retries=2147483647
# Umumiy muddat: shu vaqt ichida yetib bormasa xato qaytadi (standart 120000).
delivery.timeout.ms=120000
request.timeout.ms=30000
# Batching: 5 ms kutish throughput ni sezilarli oshiradi.
linger.ms=5
batch.size=65536
compression.type=lz4
# Buferda joy bo'lmasa send() bloklanadi, bu backpressure.
buffer.memory=67108864
max.block.ms=10000
```

`buffer.memory` to'lib qolganda `send()` chaqiruvi `max.block.ms` gacha bloklanadi. Bu Kafka ning backpressure mexanizmi va u HTTP so'rov ishlovchisi thread ini ushlab turadi. Shuning uchun `max.block.ms` ni 60 sekundda qoldirish xavfli: Kafka sekinlashsa, web thread pool to'lib qoladi va butun servis javob bermaydi. 5-10 sekund amaliy chegara.

## 29.5 Consumer sozlamalari: max.poll.records, max.poll.interval.ms va rebalance sababi

Kafka iste'molchisi `poll()` chaqiruvi orqali ishlaydi va bitta chaqiruvda `max.poll.records` (standart 500) tagacha yozuv oladi. Keyin ularning hammasini ishlab, yana `poll()` ga qaytishi kerak. Agar ikki `poll()` orasidagi vaqt `max.poll.interval.ms` (standart 300000, ya'ni 5 daqiqa) dan oshsa, group coordinator bu a'zoni o'lik deb hisoblaydi va rebalance boshlanadi.

Bu eng ko'p uchraydigan production nosozligining ildizi. Hisoblab ko'r: 500 yozuv, har biri uchun PostgreSQL ga ikki so'rov va tashqi API chaqiruvi, har biri taxminan 700 ms. Bu 350 sekund, ya'ni 5 daqiqadan oshadi. Natija: rebalance, offset commit rad etiladi, o'sha 500 xabar boshqa instansiyada qaytadan ishlanadi, u ham ulgurmaydi va tsikl aylanadi. Bu "rebalance storm" deb ataladi va servis cheksiz bir xil xabarni ishlab turadi.

Yechim ikki tomonli. Birinchisi: `max.poll.records` ni real ishlov vaqtiga moslash. Agar bitta xabar 200 ms olsa va xavfsizlik zaxirasi 3 barobar bo'lsa, `max.poll.records=100` va `max.poll.interval.ms=120000` mos keladi. Ikkinchisi: og'ir ishni listener ichida bajarmaslik, uni alohida bajarishga topshirish, lekin unda offset commit mantig'i murakkablashadi.

`session.timeout.ms` (Kafka 3.0 dan keyin standart 45000) va `heartbeat.interval.ms` (3000) boshqa narsani kuzatadi: heartbeat thread tirikligini. Ishlov uzoq cho'zilsa heartbeat davom etadi, lekin `max.poll.interval.ms` buziladi. Shuning uchun bu ikkita timeout ni aralashtirmaslik kerak.

Rebalance narxini kamaytirish uchun `CooperativeStickyAssignor` ishlatiladi: u barcha partition ni tortib olmaydi, faqat ko'chadiganlarini qaytaradi, shunda to'xtash 10 sekunddan 1 sekundga tushadi. Kafka 4.0 da KIP-848 asosidagi yangi group protokoli (`group.protocol=consumer`) rebalance ni broker tomoniga ko'chiradi va "stop the world" pauzasini yo'q qiladi.

```properties
# Consumer: ishlov vaqtini hisoblab batch kattaligini tanlaymiz.
group.id=payment-settlement
enable.auto.commit=false
auto.offset.reset=earliest
# 100 yozuv x ~200 ms = ~20 s, 120 s chegarada 6 barobar zaxira bor.
max.poll.records=100
max.poll.interval.ms=120000
session.timeout.ms=45000
heartbeat.interval.ms=3000
fetch.min.bytes=1
fetch.max.wait.ms=500
partition.assignment.strategy=org.apache.kafka.clients.consumer.CooperativeStickyAssignor
# Faqat commit qilingan tranzaksiya xabarlarini o'qish.
isolation.level=read_committed
```

## 29.6 Offset commit strategiyasi va kamida bir marta yetkazish oqibati

`enable.auto.commit=true` har `auto.commit.interval.ms` (5000) da oxirgi `poll()` qaytargan offset ni commit qiladi, ishlov tugaganiga qaramay. Ya'ni xabarni oldin commit qilib, keyin ishlov paytida xato bersang, xabar butunlay yo'qoladi. Bu "ko'pi bilan bir marta" semantikasi va to'lov uchun yaramaydi. Shuning uchun production da `enable.auto.commit=false`.

Qo'lda commit da tartib aniq: avval ishlov, keyin commit. Bu "kamida bir marta" yetkazishni beradi. Oqibati muhim: ishlov tugagandan keyin, commit dan oldin instansiya qulasa, o'sha xabar qaytadan keladi. Bu nosozlik emas, bu Kafka ning normal rejimi. Arxitektor vazifasi dublikatni oldini olish emas, dublikatga chidamli ishlov qurish.

Spring Kafka da `AckMode` bu qarorni shakllantiradi. `BATCH` (standart) butun poll natijasi ishlangach commit qiladi, `RECORD` har yozuvdan keyin commit qiladi, `MANUAL_IMMEDIATE` esa kodga `Acknowledgment.acknowledge()` ni beradi. `RECORD` xavfsizroq, lekin har commit broker ga so'rov, 1000 yozuv uchun 1000 so'rov. Amaliy o'rta yo'l: `BATCH` plus idempotent ishlov.

## 29.7 Idempotent iste'molchi qurish: PostgreSQL da ishlov berilgan xabar jadvali

Idempotentlikning eng ishonchli shakli: ishlov natijasini va "bu xabar ishlangan" belgisini bitta PostgreSQL tranzaksiyasida yozish. Shunda ikkinchi marta kelgan xabar unique constraint ga urilib, ishlovsiz tashlanadi. Kalit sifatida biznes identifikatorni (`payment_id`) ishlatish topic va partition dan ustun, chunki partition ko'paysa yoki topic almashsa ham identifikator o'zgarmaydi.

```sql
-- Ishlov berilgan xabar jadvali: dublikatni biznes kaliti bo'yicha to'sadi.
CREATE TABLE processed_message (
    consumer_group text        NOT NULL,
    message_id     text        NOT NULL,   -- biznes kaliti, masalan payment_id
    topic          text        NOT NULL,
    partition      int         NOT NULL,
    record_offset  bigint      NOT NULL,
    processed_at   timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (consumer_group, message_id)
);

-- Jadval cheksiz o'smasligi uchun oyiga bir marta tozalash.
-- 30 kun dublikat oynasi ko'p tizim uchun yetarli.
CREATE INDEX idx_processed_message_at ON processed_message (processed_at);

DELETE FROM processed_message
WHERE processed_at < now() - interval '30 days';
```

```java
// Idempotent ishlov: belgini va natijani bitta tranzaksiyada yozamiz.
@Transactional
public void handle(PaymentConfirmed msg, String topic, int partition, long offset) {
    int inserted = jdbcTemplate.update("""
            INSERT INTO processed_message
                (consumer_group, message_id, topic, partition, record_offset)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (consumer_group, message_id) DO NOTHING
            """, "payment-settlement", msg.paymentId(), topic, partition, offset);

    if (inserted == 0) {
        // Dublikat: hech narsa qilmaymiz, lekin metrikani oshiramiz.
        duplicateCounter.increment();
        return;
    }
    // Asosiy biznes ishi shu tranzaksiya ichida, demak atomar.
    ledgerService.applyPayment(msg);
}
```

Bu yondashuvning cheklovi: ishlov PostgreSQL dan tashqariga chiqsa (tashqi API ga to'lov yuborish) atomarlik buziladi. Unda tashqi chaqiruvga idempotency key berish kerak, ya'ni idempotentlikni chegaradan tashqariga uzatish.

## 29.8 Consumer lag ni o'lchash va ogohlantirish chegarasi qo'yish

Lag bu partition ning oxirgi offset i va group commit qilgan offset i o'rtasidagi farq. U faqat sondan iborat emas: 50000 lag bir topic da 2 sekund, boshqasida 2 soat bo'lishi mumkin. Shuning uchun ogohlantirishni vaqtga o'tkazish kerak: `lag / xabarlar_sekundda`. Bu "qancha orqada" degan savolga biznes tili bilan javob beradi.

```bash
# Group holatini va har partition lag ini ko'rish.
kafka-consumer-groups.sh --bootstrap-server kafka-1:9092 \
  --describe --group payment-settlement

# Chiqishda: TOPIC PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG CONSUMER-ID
# Faqat eng katta lag ni ajratib olish (monitoring skript uchun).
kafka-consumer-groups.sh --bootstrap-server kafka-1:9092 \
  --describe --group payment-settlement 2>/dev/null \
  | awk 'NR>1 && $6 ~ /^[0-9]+$/ {if ($6>m) m=$6} END {print m+0}'

# Rebalance tez-tez bo'layotganini tekshirish: group holati Stable bo'lishi kerak.
kafka-consumer-groups.sh --bootstrap-server kafka-1:9092 \
  --describe --group payment-settlement --state
```

Spring Boot ichida Micrometer Kafka client metrikalarini chiqaradi, eng muhimi `kafka.consumer.fetch.manager.records.lag.max`. Ogohlantirish chegarasi uchun amaliy qoida: ikki pog'ona. Birinchi pog'ona lag 5 daqiqadan oshsa warning, ikkinchisi 20 daqiqadan oshsa yoki lag 15 daqiqa davomida monoton o'ssa critical. Bitta cho'qqi (spike) ogohlantirish sababi emas, trend sabab.

Alohida kuzatish kerak bo'lgan ikki narsa bor. Birinchisi: lag nolga teng, lekin iste'molchi yo'q, ya'ni group bo'sh. Ikkinchisi: bitta partition lag i qolganlaridan 10 barobar katta, bu kalit taqsimoti nosozligi. Ikkalasi ham oddiy "umumiy lag" grafigida ko'rinmaydi.

## 29.9 Xato xabar bilan nima qilish: qayta urinish topic va dead letter topic

Xatolarni ikki sinfga ajratish kerak. O'tkinchi xato (PostgreSQL connection timeout, tashqi servisning 503 javobi) qayta urinishga arziydi. Doimiy xato (JSON deserializatsiya buzilgan, majburiy maydon yo'q, biznes qoidasi rad etdi) qayta urinishda hech qachon o'zgarmaydi. Doimiy xatoni asosiy topic da cheksiz urinish "poison pill" holatini yaratadi: bitta buzilgan xabar butun partition ni to'xtatib qo'yadi.

Listener ichida blokirovkali qayta urinish qilish xavfli, chunki u `max.poll.interval.ms` ni yeydi. Shuning uchun uzoq kechikishli qayta urinishlar alohida topic larga chiqariladi: `order.events.retry.5s`, `order.events.retry.1m`, `order.events.retry.10m`, va oxirida `order.events.DLT`. Spring Kafka ning `@RetryableTopic` annotatsiyasi shu topic larni va ularning listener larini avtomatik yaratadi.

Dead letter topic ning eng katta muammosi texnik emas, tashkiliy: unga hech kim qaramaydi. DLT ni amalda ishlatish uchun uchta narsa kerak. Birinchisi: DLT ga tushgan har xabar uchun alert, chunki DLT da bitta xabar ham anomaliya. Ikkinchisi: original xato, stack trace va topic nomi header larda saqlanishi (Spring ning `DeadLetterPublishingRecoverer` buni qiladi). Uchinchisi: DLT dan asosiy topic ga qaytarish uchun ishlaydigan operator vositasi, qo'lda SQL emas.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `enable.auto.commit=true` qoldirilgan | Ishlov xato bersa ham offset commit bo'ladi, xabar yo'qoladi | `false` qo'yish, ishlovdan keyin commit |
| `max.poll.records=500` va og'ir ishlov | `max.poll.interval.ms` buziladi, rebalance storm | Batch ni 50-100 ga tushirish, interval ni hisoblash |
| Doimiy xatoda cheksiz retry | Bitta buzilgan xabar partition ni to'xtatadi | `addNotRetryableExceptions` va DLT |
| Partition sonini production da oshirish | Kalit boshqa partition ga tushadi, tartib buziladi | Yangi topic va ikki tomonlama o'qish |
| DB commit, keyin Kafka send | DB yozildi, xabar yo'qoldi, holat nomuvofiq | Outbox jadvali va alohida publisher |
| `null` kalit bilan tartibga tayanish | Sticky partitioner xabarni turli partition ga tashlaydi | Biznes kalitini majburiy qilish |
| DLT ga alert yo'q | Xabarlar bir necha hafta sezilmay yo'qoladi | DLT dagi har xabarga ogohlantirish |
| `max.block.ms` standart 60 s | Kafka sekinlashsa web thread pool to'ladi | 5-10 s va circuit breaker |

## 29.10 Sxema o'zgarishi va orqaga moslik

Kafka da xabar bir necha kun yoki hafta yashaydi, shuning uchun bitta topic da bir vaqtda eski va yangi sxemadagi yozuvlar bo'ladi. Bu degani sxema o'zgarishi deploy tartibidan ko'ra muhimroq masala. Schema registry (Confluent yoki Apicurio) sxemani markazlashtiradi va moslik qoidasini majburlaydi, shunda nomos sxema serialize bosqichida rad etiladi, production da emas.

Eng ko'p ishlatiladigan rejim `BACKWARD`: yangi sxema eski ma'lumotni o'qiy oladi. Bu iste'molchini birinchi, producer ni keyin deploy qilishni talab qiladi. `FORWARD` teskarisi. Amalda ko'pchilik jamoaga `FULL` mos keladi: faqat standart qiymati bor maydon qo'shish va faqat ixtiyoriy maydonni olib tashlash mumkin. Majburiy maydonni standart qiymatsiz qo'shish har qanday rejimda buzuvchi o'zgarish.

Avro maydon nomini o'zgartirishni qo'llab-quvvatlamaydi, lekin `aliases` beradi. JSON Schema moslashuvchanroq, ammo hajmi kattaroq va tekshiruvi kuchsizroq. Amaliy qaror: ichki, yuqori oqimli topic lar uchun Avro (yozuv taxminan 30-50 foiz kichik), tashqi integratsiya uchun JSON Schema, chunki sherik jamoalar uchun o'qish oson.

Alohida eslatma: enum. Avro enum ga yangi qiymat qo'shish eski iste'molchi uchun buzuvchi o'zgarish, chunki u noma'lum qiymatni o'qiy olmaydi. Buyurtma holati kabi o'sib boradigan ro'yxatni `string` sifatida saqlash va validatsiyani kodga qo'yish ko'pincha to'g'riroq.

## 29.11 Tranzaksiya va xabar yuborish nomuvofiqligi: nega ikki fazali commit emas

Klassik muammo: `@Transactional` metod ichida PostgreSQL ga buyurtma yoziladi va Kafka ga hodisa yuboriladi. DB commit muvaffaqiyatli, Kafka esa tarmoq uzilishi sababli yozilmadi. Natijada buyurtma bazada bor, lekin ombor servisi uni ko'rmaydi. Teskari holat ham bor: Kafka yozildi, DB rollback bo'ldi, mavjud bo'lmagan buyurtma uchun hodisa tarqaldi.

Ikki fazali commit (XA) nazariy yechim, lekin Kafka XA tranzaksiya menejerini qo'llab-quvvatlamaydi. Kafka ning o'z tranzaksiyasi (`transactional.id` plus `isolation.level=read_committed`) faqat Kafka ichida atomar, ya'ni "read-process-write" oqimida. U PostgreSQL bilan bitta atomar blokga birlashmaydi. Spring Kafka da ilgari bo'lgan `ChainedKafkaTransactionManager` eng yaxshi holatda "eng yaxshi harakat" semantikasini beradi va Spring Kafka 3.x da deprecated.

Shuning uchun amaliy yechim outbox: hodisani bitta DB tranzaksiyasida jadvalga yozish, keyin alohida publisher uning Kafka ga yuborilishini ta'minlash. Bu "kamida bir marta" yuborishni beradi, dublikat esa iste'molchi tomonidagi idempotentlik bilan yopiladi. Pattern tafsiloti dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern bo'limida.

```sql
-- Outbox: hodisa biznes o'zgarishi bilan bitta tranzaksiyada yoziladi.
CREATE TABLE outbox_event (
    id             bigserial PRIMARY KEY,
    aggregate_type text        NOT NULL,   -- 'ORDER', 'PAYMENT'
    aggregate_id   text        NOT NULL,   -- Kafka kaliti bo'ladi
    event_type     text        NOT NULL,
    payload        jsonb       NOT NULL,
    created_at     timestamptz NOT NULL DEFAULT now(),
    published_at   timestamptz
);

CREATE INDEX idx_outbox_unpublished ON outbox_event (id)
    WHERE published_at IS NULL;

-- Publisher: bir nechta instansiya parallel ishlashi uchun qulf oladi.
SELECT id, aggregate_id, event_type, payload
FROM outbox_event
WHERE published_at IS NULL
ORDER BY id
LIMIT 200
FOR UPDATE SKIP LOCKED;
```

`FOR UPDATE SKIP LOCKED` bu yerda hal qiluvchi: ikkita publisher instansiyasi bir xil qatorni olmaydi va bir-birini kutmaydi. `ORDER BY id` bitta aggregate uchun tartibni saqlaydi, chunki `bigserial` monoton o'sadi.

## 29.12 Spring Kafka da asosiy sozlamalar va xato ishlovchisi

Spring Kafka da `ConcurrentKafkaListenerContainerFactory` ning `concurrency` xossasi shu instansiyadagi iste'molchi thread lari sonini belgilaydi. Uni partition sonidan oshirish befoyda. 12 partition va 3 instansiya bo'lsa, `concurrency=4` to'g'ri tanlov: har instansiya 4 partition oladi.

```yaml
spring:
  kafka:
    bootstrap-servers: kafka-1:9092,kafka-2:9092,kafka-3:9092
    producer:
      acks: all
      properties:
        enable.idempotence: true
        linger.ms: 5
        max.block.ms: 10000
    consumer:
      group-id: payment-settlement
      enable-auto-commit: false
      auto-offset-reset: earliest
      max-poll-records: 100
      isolation-level: read_committed
      properties:
        max.poll.interval.ms: 120000
        spring.json.trusted.packages: "com.shop.payment.events"
    listener:
      ack-mode: batch
      # 12 partition / 3 instansiya = har biriga 4 thread.
      concurrency: 4
      observation-enabled: true
```

Xato ishlovchisi bo'lmasa, Spring Kafka standart `DefaultErrorHandler` bilan 10 marta urinib, keyin yozuvni log ga chiqarib tashlaydi. Bu production uchun yetarli emas: nima tashlanganini keyin topib bo'lmaydi. To'g'ri sozlash: deserializatsiya xatosini alohida ushlash, doimiy xatolarni retry qilmaslik va qolganini DLT ga yuborish.

```java
@Bean
DefaultErrorHandler kafkaErrorHandler(KafkaTemplate<Object, Object> template) {
    // DLT nomi: "<topic>-dlt", original partition ga yozmaymiz (-1).
    var recoverer = new DeadLetterPublishingRecoverer(template,
            (record, ex) -> new TopicPartition(record.topic() + "-dlt", -1));

    // 1 s dan boshlab 2 barobar o'sadi, maksimum 10 s, 4 marta urinish.
    var backOff = new ExponentialBackOffWithMaxRetries(4);
    backOff.setInitialInterval(1000L);
    backOff.setMultiplier(2.0);
    backOff.setMaxInterval(10_000L);

    var handler = new DefaultErrorHandler(recoverer, backOff);
    // Bu xatolar hech qachon o'zgarmaydi: darhol DLT ga.
    handler.addNotRetryableExceptions(
            IllegalArgumentException.class,
            JsonProcessingException.class,
            PaymentRejectedException.class);
    handler.setRetryListeners((record, ex, attempt) ->
            log.warn("retry {} topic={} offset={}", attempt, record.topic(), record.offset()));
    return handler;
}
```

Deserializatsiya xatosi alohida holat: u listener ga yetib bormaydi, shuning uchun `ErrorHandlingDeserializer` ni o'rab ishlatish kerak. Aks holda buzilgan xabar cheksiz qayta o'qiladi va partition to'xtaydi. Testlash tomonidan nimani tekshirish kerakligi [testlash qo'llanmasidagi](../testing/README.md) Testcontainers bo'limida ko'rsatilgan.

## 29.13 Qaror jadvali: oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Partition soni | 1 yoki 3, standart qoldiriladi | Kelgusi instansiya sonidan 2-3 barobar, 12 yoki 24 |
| Kalit | `null`, Kafka o'zi taqsimlasin | Biznes kaliti (`order_id`), issiq partition tekshirilgan |
| Offset commit | `enable.auto.commit=true` | Qo'lda commit, ishlovdan keyin |
| Dublikat | "Kafka exactly-once beradi" deb ishonish | `processed_message` jadvali va unique constraint |
| Batch kattaligi | Standart 500 | Ishlov vaqtidan hisoblangan 50-100 |
| DB va Kafka | Bitta `@Transactional` metodda ikkisi ham | Outbox jadvali, `SKIP LOCKED` publisher |
| Xato xabar | `try/catch` va log, keyin davom | Retry topic lar, DLT va DLT ga alert |
| Monitoring | Broker CPU va disk | Lag ni vaqtga aylantirish, rebalance soni |
| Sxema | POJO o'zgaradi, deploy qilinadi | Registry, `FULL` moslik, maydon standart qiymati bilan |
| Rebalance | Sezilmaydi, "shunchaki sekinlashdi" | `CooperativeStickyAssignor`, rebalance metrikasi |

## 29.14 Amalda qo'llash

- [ ] Har bir topic uchun partition sonini va kalit tanlovini yozib chiq, kalit bo'yicha xabar taqsimotini `kafka-consumer-groups.sh` lag chiqishi orqali tekshir va issiq partition bor-yo'qligini aniqla.
- [ ] Barcha producer da `acks=all`, `enable.idempotence=true` va `max.block.ms` 10 sekunddan oshmasligini tasdiqla, konfiguratsiyani kodga qattiq yozib qo'y.
- [ ] Har bir listener uchun bitta xabar ishlov vaqtini o'lchab, `max.poll.records` ni shunga qarab qayta hisobla va `max.poll.interval.ms` da kamida 3 barobar zaxira qoldir.
- [ ] `enable.auto.commit=true` qolgan barcha consumer ni top va ularni qo'lda commit ga o'tkaz.
- [ ] `processed_message` jadvalini joriy qilib, hech bo'lmasa to'lov va buyurtma listener larini idempotent qil, dublikat sonini metrika qilib chiqar.
- [ ] Retry topic va DLT zanjirini sozlab, `addNotRetryableExceptions` ro'yxatini to'ldir va DLT ga tushgan har xabar uchun alert yoq.
- [ ] Lag ni sondan vaqtga aylantiradigan dashboard panelini qur, 5 daqiqa warning va 20 daqiqa critical chegarasini qo'y, rebalance sonini ham shu panelga qo'sh.
- [ ] DB va Kafka ni bitta tranzaksiyada yozayotgan joylarni topib, ularni outbox jadvali va `FOR UPDATE SKIP LOCKED` publisher ga ko'chir.

---

[&larr; 28. Keshlash amaliyoti: invalidatsiya, stampede, Redis haqiqati](28-keshlash-amaliyoti-invalidatsiya-stampede.md) · [Mundarija](README.md) · [30. Kuzatuvchanlik amaliyoti: log, metrika, trace va ularning narxi &rarr;](30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md)
