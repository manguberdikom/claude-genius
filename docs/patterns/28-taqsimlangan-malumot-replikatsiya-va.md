<!-- doc: patterns | chapter: 28 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 28. Taqsimlangan ma'lumot, replikatsiya va konsistentlik patternlari (Distributed Data, Replication & Consistency Patterns)

<details>
<summary>Bu bo'limdagi 28 bo'lim</summary>

- [28.1 Yozishdan-oldingi jurnal (Write-Ahead Log)](#281-yozishdan-oldingi-jurnal-write-ahead-log)
- [28.2 Leader asosidagi replikatsiya (Leader-based Replication)](#282-leader-asosidagi-replikatsiya-leader-based-replication)
- [28.3 Ko'p-leaderli replikatsiya (Multi-Leader Replication)](#283-kop-leaderli-replikatsiya-multi-leader-replication)
- [28.4 Leadersiz replikatsiya (Leaderless Replication)](#284-leadersiz-replikatsiya-leaderless-replication)
- [28.5 Quorum o'qish/yozish (Quorum Read/Write)](#285-quorum-oqishyozish-quorum-readwrite)
- [28.6 Konsistent xeshlash (Consistent Hashing)](#286-konsistent-xeshlash-consistent-hashing)
- [28.7 O'qishda tuzatish (Read Repair)](#287-oqishda-tuzatish-read-repair)
- [28.8 Anti-entropiya (Anti-Entropy)](#288-anti-entropiya-anti-entropy)
- [28.9 Ishora bilan topshirish (Hinted Handoff)](#289-ishora-bilan-topshirish-hinted-handoff)
- [28.10 Vektor soat (Vector Clock)](#2810-vektor-soat-vector-clock)
- [28.11 Oxirgi yozuv g'alaba qozonadi (Last Write Wins)](#2811-oxirgi-yozuv-galaba-qozonadi-last-write-wins)
- [28.12 Fencing token (Fencing Token)](#2812-fencing-token-fencing-token)
- [28.13 Linearizatsiyalanganlik (Linearizability)](#2813-linearizatsiyalanganlik-linearizability)
- [28.14 Kauzal konsistentlik (Causal Consistency)](#2814-kauzal-konsistentlik-causal-consistency)
- [28.15 O'z yozuvingni o'qish konsistentligi (Read-Your-Writes Consistency)](#2815-oz-yozuvingni-oqish-konsistentligi-read-your-writes-consistency)
- [28.16 Monoton o'qishlar (Monotonic Reads)](#2816-monoton-oqishlar-monotonic-reads)
- [28.17 Yakuniy konsistentlik (Eventual Consistency)](#2817-yakuniy-konsistentlik-eventual-consistency)
- [28.18 Snapshot izolyatsiyasi / MVCC (Snapshot Isolation / MVCC)](#2818-snapshot-izolyatsiyasi--mvcc-snapshot-isolation--mvcc)
- [28.19 Serializable snapshot izolyatsiyasi (Serializable Snapshot Isolation)](#2819-serializable-snapshot-izolyatsiyasi-serializable-snapshot-isolation)
- [28.20 Write skew anomaliyasi (Write Skew)](#2820-write-skew-anomaliyasi-write-skew)
- [28.21 Fantom o'qish (Phantom Read)](#2821-fantom-oqish-phantom-read)
- [28.22 Ikki fazali qulflash (Two-Phase Locking)](#2822-ikki-fazali-qulflash-two-phase-locking)
- [28.23 Konsensus (Consensus (Raft / Paxos))](#2823-konsensus-consensus-raft--paxos)
- [28.24 Umumiy tartibli broadcast (Total Order Broadcast)](#2824-umumiy-tartibli-broadcast-total-order-broadcast)
- [28.25 Lambda arxitekturasi (Lambda Architecture)](#2825-lambda-arxitekturasi-lambda-architecture)
- [28.26 Kappa arxitekturasi (Kappa Architecture)](#2826-kappa-arxitekturasi-kappa-architecture)
- [28.27 Split brain (Split Brain)](#2827-split-brain-split-brain)
- [28.28 Gibrid logik soat / soat siljishi (Hybrid Logical Clock / Clock Skew)](#2828-gibrid-logik-soat--soat-siljishi-hybrid-logical-clock--clock-skew)

</details>



Taqsimlangan ma'lumot patternlari bir nusxadagi ma'lumotni bir necha node o'rtasida ko'paytirish, ularni sinxron tutish va nosozlik paytida ham to'g'ri javob berishni ta'minlash uchun ishlatiladi. Arxitektor uchun bu kategoriya hal qiluvchi, chunki CAP va PACELC cheklovlari tufayli "hamma joyda kuchli konsistentlik" iqtisodiy jihatdan imkonsiz - har bir aggregate uchun konsistentlik darajasini ongli ravishda tanlash kerak. Bu patternlarning ko'pi ilova kodida emas, ma'lumotlar bazasi (PostgreSQL, Cassandra, Kafka) yoki koordinatsiya qatlami (ZooKeeper, etcd) ichida amalga oshiriladi - lekin Spring ilovasi ularning semantikasiga tayanadi, shuning uchun injener ularning kafolatlarini bilishi shart. Noto'g'ri tanlangan konsistentlik modeli production'da faqat yuklama ostida ko'rinadigan, qayta tiklash qiyin bo'lgan ma'lumot buzilishlariga olib keladi.

## 28.1 Yozishdan-oldingi jurnal (Write-Ahead Log)

**Tavsif:** Har qanday o'zgarish avval ketma-ket (append-only) durable jurnalga yoziladi, keyin esa asosiy ma'lumot strukturasiga (B-tree, heap, memtable) qo'llaniladi. Shu sababli crash paytida tizim jurnalni qaytadan o'qib (replay) tugallanmagan tranzaksiyalarni rollback yoki roll-forward qiladi - durability va atomiclikni bitta mexanizm bilan beradi. Random yozuvlar sequential yozuvga aylanganligi uchun yozish throughput'i ham oshadi. Bundan tashqari aynan shu jurnal replikatsiya va CDC uchun manba bo'lib xizmat qiladi.

**Spring'da qayerda uchraydi:** Bu infratuzilma darajasidagi pattern - PostgreSQL WAL, MySQL InnoDB redo log, Cassandra commitlog, Kafka partition segment fayllari, HBase HLog. Spring ilovasi unga bilvosita tayanadi: `@Transactional` commit qilganda `DataSourceTransactionManager` yoki `JpaTransactionManager` JDBC `Connection.commit()` ni chaqiradi, DB esa WAL fsync qilgandan keyingina muvaffaqiyat qaytaradi - ya'ni `synchronous_commit=off` qo'yilsa Spring tranzaksiya "commit bo'ldi" deydi, lekin durability yo'qoladi. Debezium (Spring Boot bilan `debezium-api` embedded engine orqali) PostgreSQL logical replication slot yoki MySQL binlog'ni, ya'ni WAL'ni o'qib CDC event'lar chiqaradi; Spring tomonda ularni `KafkaListener` iste'mol qiladi. Spring'ning o'zida ham shunga o'xshash g'oya bor: Spring Batch `BATCH_STEP_EXECUTION` jadvaliga progress yozib restart'ni ta'minlaydi, Axon Framework/Eventuate esa event store'ni append-only log sifatida ishlatadi.

**Qo'llanish keyslari:**
- PostgreSQL'da `@Transactional` to'lov operatsiyasidan keyin server o'chsa ham, commit bo'lgan yozuv WAL replay orqali qaytariladi.
- Debezium + Kafka Connect orqali `orders` jadvalidagi har bir UPDATE'ni WAL'dan o'qib search index'ga stream qilish.
- Kafka'da `acks=all` va `min.insync.replicas=2` bilan producer yozuvi faqat log'ga durable yozilgach tasdiqlanadi.
- Point-in-time recovery: WAL arxivini saqlab, bazani "kecha 14:32" holatiga qaytarish.
- Cassandra'da memtable RAM'da bo'lsa ham, commitlog crash'dan keyin yo'qolgan yozuvlarni tiklaydi.

**Ehtiyot bo'ling:** WAL faqat fsync bajarilganda haqiqiy durability beradi - `synchronous_commit=off`, `innodb_flush_log_at_trx_commit=2` yoki Kafka'da `acks=1` ishlatish "commit bo'ldi" degan yolg'on signalni keltiradi. Shuningdek logical replication slot iste'molchisi (Debezium) uzoq vaqt to'xtab qolsa, WAL tozalanmay disk to'lib ketadi va butun baza yozishni to'xtatadi.

## 28.2 Leader asosidagi replikatsiya (Leader-based Replication)

**Tavsif:** Bitta node leader (primary) deb tayinlanadi va barcha yozuvlar faqat unga boradi; leader o'z WAL/binlog'ini follower'larga (replica) uzatadi, ular esa o'z nusxasini shu tartibda qo'llaydi. O'qishlar follower'lardan ham xizmat qilishi mumkin, bu read scalability beradi. Replikatsiya sinxron (commit follower tasdiqlashini kutadi) yoki asinxron (kutmaydi, lekin lag paydo bo'ladi) bo'lishi mumkin. Leader yiqilsa failover orqali yangi leader saylanadi.

**Spring'da qayerda uchraydi:** Replikatsiyaning o'zi DB darajasida (PostgreSQL streaming replication, MySQL replication, MongoDB replica set, Redis replication). Spring tomonda esa read/write ajratish `AbstractRoutingDataSource` (ko'pincha `LazyConnectionDataSourceProxy` bilan o'ralgan) va `@Transactional(readOnly = true)` kombinatsiyasi orqali amalga oshiriladi - `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` qiymatiga qarab routing kaliti tanlanadi. MongoDB'da esa buni Spring Data `ReadPreference.secondaryPreferred()` yoki `@Query` darajasida belgilash mumkin; Spring Data Redis'da `LettuceClientConfiguration` ichida `readFrom(ReadFrom.REPLICA_PREFERRED)`. Failover'ni driver boshqaradi: PgJDBC `targetServerType=primary` bilan bir necha host, MySQL Connector/J replication URL, Redis Sentinel uchun `RedisSentinelConfiguration`.

```java
public class ReplicaRoutingDataSource extends AbstractRoutingDataSource {
    @Override protected Object determineCurrentLookupKey() {
        return TransactionSynchronizationManager.isCurrentTransactionReadOnly()
                ? "replica" : "primary";
    }
}
```

**Qo'llanish keyslari:**
- Mahsulot katalogi o'qishlarini replica'larga yuborib, primary'ni faqat buyurtma yozuvlari uchun qoldirish.
- Analitik va hisobot so'rovlarini alohida replica'da bajarib, OLTP yuklamasini himoyalash.
- Patroni/Sentinel bilan avtomatik failover: primary yiqilganda 30 soniyada yangi primary'ga o'tish.
- Geografik read replica: Yevropadagi foydalanuvchilarga mahalliy replica'dan past latency bilan o'qish.
- Zaxira (backup) va `pg_dump` ni replica'da bajarib, primary'da lock va I/O bosimini kamaytirish.

**Ehtiyot bo'ling:** Asinxron replikatsiyada "o'zi yozgan narsani o'qiy olmaslik" (read-your-writes buzilishi) klassik bug - foydalanuvchi profilni saqlagach replica'dan eski ma'lumot ko'radi, shuning uchun yozishdan keyingi o'qishni primary'ga yo'naltirish yoki `@Transactional(readOnly=true)` ni ko'r-ko'rona qo'llamaslik kerak. Split-brain xavfi tufayli failover'ni qo'lda emas, fencing bilan birga ishlaydigan koordinator (Patroni + etcd) boshqarishi lozim.

## 28.3 Ko'p-leaderli replikatsiya (Multi-Leader Replication)

**Tavsif:** Bir nechta node bir vaqtda yozuvlarni qabul qiladi va o'zgarishlarni bir-biriga asinxron tarzda uzatadi. Bu har bir datacenter yoki offline qurilmada mahalliy past latency bilan yozish imkonini beradi va bitta region yiqilsa ham yozish davom etadi. Buning narxi - yozish konfliktlari: bir xil yozuv ikki joyda parallel o'zgartirilsa, ularni aniqlash va yechish (CRDT, LWW, qo'lda merge) kerak bo'ladi. Shuning uchun u faqat konflikt ehtimoli past yoki konvergent ma'lumot modellari uchun maqsadga muvofiq.

**Spring'da qayerda uchraydi:** Spring'da bunday pattern yo'q - bu to'liq DB/infra darajasida: PostgreSQL uchun BDR yoki Bucardo, MySQL Group Replication multi-primary rejimi, CockroachDB/YugabyteDB multi-region, Oracle GoldenGate bidirectional. Kafka darajasida MirrorMaker 2 yoki Confluent Cluster Linking ikki klaster o'rtasida active-active topic replikatsiyasini beradi, Spring ilova esa `spring.kafka.consumer.group-id` va topic prefiksi (`dc1.orders`) bilan ularni iste'mol qiladi. Konflikt yechimini ilova darajasida qurish uchun JPA'da `@Version` (optimistic locking) yetarli emas, shuning uchun odatda konvergent struktura (append-only event jadvali) yoki Hazelcast/Infinispan'ning CRDT va `PNCounter` kabi tiplari ishlatiladi; Redis Enterprise CRDB (Active-Active) ham Spring Data Redis orqali shaffof ishlaydi.

**Qo'llanish keyslari:**
- Ikki regionli active-active ilova: AQSh va Yevropa foydalanuvchilari o'z regionida yozadi, ma'lumot keyin konvergatsiya qiladi.
- Mobil ilova offline rejimda mahalliy SQLite'ga yozadi, tarmoq tiklanganda server bilan sinxronlanadi.
- Kafka MirrorMaker 2 orqali DR klasterni "issiq" holatda saqlab, RTO'ni daqiqalarga tushirish.
- Hazelcast `PNCounter` bilan ko'p-klasterli like/view hisoblagichini yo'qotishsiz yuritish.
- Legacy monolit va yangi servis bir jadvalga bir muddat ikki tomonlama yozib, bosqichma-bosqich migratsiya qilish.

**Ehtiyot bo'ling:** Auto-increment ID'lar, unique constraint'lar va "oxirgi qiymat g'alaba qozonadi" qoidasi multi-leader'da jimgina ma'lumot yo'qotishga olib keladi - ID uchun UUIDv7/Snowflake, konflikt uchun esa aniq yozilgan merge strategiyasi kerak. Agar domenda haqiqiy konflikt ehtimoli bor (hisobdan pul yechish, inventar zaxirasi), multi-leader'ni umuman tanlamang: bitta leader yoki konsensus (Raft) asosidagi bazaga o'ting.

## 28.4 Leadersiz replikatsiya (Leaderless Replication)

**Tavsif:** Hech qanday leader bo'lmaydi - client (yoki koordinator node) yozuvni bir necha replikaga parallel yuboradi va o'qishda ham bir nechtasidan javob yig'adi. Node yiqilganda failover kerak emas, chunki yozuv shunchaki boshqa mavjud replikalarga tushadi - bu yuqori yozish availability beradi. Buning o'rniga ma'lumot vaqtincha divergent bo'ladi va read repair, anti-entropy, hinted handoff kabi mexanizmlar bilan tuzatiladi. Konsistentlik darajasi quorum parametrlari (R va W) bilan sozlanadi.

**Spring'da qayerda uchraydi:** Bu ma'lumotlar bazasi darajasidagi arxitektura: Apache Cassandra, ScyllaDB, Amazon DynamoDB, Riak, Voldemort. Spring ilovasi Spring Data Cassandra orqali ishlaydi - `CassandraTemplate`, `@Table`, `@PrimaryKeyClass` va `CassandraRepository`; konsistentlik darajasi `QueryOptions.builder().consistencyLevel(ConsistencyLevel.QUORUM)` yoki `application.yml`da `spring.cassandra.request.consistency: QUORUM` orqali beriladi. DynamoDB uchun Spring Boot'da AWS SDK v2 `DynamoDbEnhancedClient` bean qilib ishlatiladi, u yerda `consistentRead(true)` flagi quorum o'qishga teng. Muhim nuqta: `@Transactional` bu bazalarda ko'p-partition atomikligini bermaydi, shuning uchun Spring'ning tranzaksiya abstraksiyasiga tayanmaslik kerak.

**Qo'llanish keyslari:**
- IoT yoki telemetriya time-series yozuvlari: millionlab yozuv/sekund, bitta node yo'qolishi yozishni to'xtatmaydi.
- Foydalanuvchi faoliyati (activity feed, audit trail) uchun append-only, yuqori availability talab qiladigan saqlash.
- Ko'p-regionli sessiya yoki profil store: har bir region o'z replikasiga yozadi.
- Chat/xabar tarixi: partition key `conversation_id` bo'yicha gorizontal masshtablash.
- Mahsulot ko'rish statistikasi - aniqlik emas, availability muhim bo'lgan hisoblagichlar.

**Ehtiyot bo'ling:** Leadersiz bazalar JOIN, ad-hoc query va read-modify-write'ni yaxshi bajarmaydi - jadvalni so'rov shakliga qarab denormalizatsiya qilish kerak, aks holda `ALLOW FILTERING` bilan klaster butunlay sekinlashadi. Hisoblagichlarni `SELECT` qilib, +1 qo'shib, qaytib yozish (`read-modify-write`) leadersiz muhitda yo'qotishga olib keladi - buning uchun counter column yoki CRDT ishlating.

## 28.5 Quorum o'qish/yozish (Quorum Read/Write)

**Tavsif:** N replikadan yozuv kamida W tasiga, o'qish esa kamida R tasidan tasdiq olishi talab qiladi. Agar `R + W > N` bo'lsa, o'qish va yozish to'plamlari albatta kesishadi va o'qish eng yangi qiymatni (yoki uning bir nusxasini) ko'radi - bu kuchli konsistentlikka yaqin kafolat beradi. R va W ni o'zgartirib, latency bilan konsistentlik o'rtasidagi muvozanatni har bir so'rov uchun alohida sozlash mumkin. Masalan `N=3, W=2, R=2` eng keng tarqalgan muvozanat.

**Spring'da qayerda uchraydi:** Parametrlar DB tomonda, lekin Spring ilovasi ularni so'rov darajasida beradi. Spring Data Cassandra'da `spring.cassandra.request.consistency: QUORUM` global, yoki `CassandraTemplate.execute(statement.setConsistencyLevel(DefaultConsistencyLevel.LOCAL_QUORUM))` so'rov bo'yicha; ko'p-regionli klasterda `LOCAL_QUORUM` to'g'ri tanlov, chunki `QUORUM` cross-region latency qo'shadi. MongoDB'da Spring Data `WriteConcern.MAJORITY` (`MongoTemplate.setWriteConcern(...)` yoki `@Document` ustida `MongoTemplate` sozlamasi) va `ReadConcern.MAJORITY` bilan bir xil g'oya ishlaydi - `WriteConcernResolver` bean orqali operatsiya turiga qarab belgilash mumkin. Kafka'da ekvivalenti `acks=all` + `min.insync.replicas` (`spring.kafka.producer.acks: all`), etcd/ZooKeeper'da esa quorum Raft/ZAB ichiga qurilgan.

**Qo'llanish keyslari:**
- Moliyaviy balans yoki buyurtma holati uchun `LOCAL_QUORUM` o'qish/yozish bilan eski qiymat o'qishni oldini olish.
- Katalog ko'rinishi uchun `ONE` o'qish ishlatib, latency'ni ataylab pasaytirish.
- Kafka'da `acks=all` + `min.insync.replicas=2` bilan broker yo'qolganda ham event yo'qotmaslik.
- MongoDB `writeConcern: majority` bilan foydalanuvchi ro'yxatdan o'tishini durable qilish.
- Multi-DC Cassandra'da `EACH_QUORUM` ni faqat juda kritik yozuvlar uchun qo'llash.

**Ehtiyot bo'ling:** `R + W > N` kuchli konsistentlikni kafolatlamaydi - sloppy quorum va hinted handoff yoqilganda yozuv "noto'g'ri" node'larda turishi mumkin, shuningdek parallel yozuvlar tartibi aniqlanmaydi. Quorum'ni oshirish availability'ni pasaytiradi: `N=3, W=3` qo'ysangiz bitta node o'chishi butun yozishni to'xtatadi.

## 28.6 Konsistent xeshlash (Consistent Hashing)

**Tavsif:** Kalitlar va node'lar bir xil xesh halqasiga (ring) joylashtiriladi va har bir kalit halqa bo'ylab o'zidan keyingi node'ga tegishli bo'ladi. Node qo'shilganda yoki olib tashlanganda o'rtacha K/N kalitgina ko'chadi, oddiy `hash % N` da esa deyarli barcha kalit qayta taqsimlanadi. Yuklamani tekislash uchun har bir fizik node halqada ko'plab virtual node (vnode) sifatida ko'rsatiladi. Replikatsiya esa halqada keyingi RF ta node'ga nusxa yozish orqali tabiiy chiqadi.

**Spring'da qayerda uchraydi:** Bu kutubxona va infra darajasida. Cassandra/ScyllaDB `Murmur3Partitioner` va `num_tokens` bilan vnode'larni ishlatadi; Spring Data Cassandra driver'i `TokenAwarePolicy` orqali so'rovni to'g'ri replikaga yuboradi - ya'ni ilova halqani bilmasa ham undan foyda ko'radi. Redis Cluster 16384 hash slot'dan foydalanadi (toza consistent hashing emas, lekin bir xil maqsad) va Spring Data Redis `LettuceConnectionFactory` + `RedisClusterConfiguration` bilan ishlaydi; `RedisTemplate` kalitlarini `{user:42}` hash-tag bilan bitta slotga biriktirish mumkin. Memcached mijozlarida (`spymemcached`, `xmemcached`) ketama hashing standart; Hazelcast va Infinispan ham partitioning uchun shunga o'xshash sxemadan foydalanadi, Spring Boot ularni `@EnableCaching` bilan cache backend qilib ulaydi. Kafka'da `Partitioner` interfeysini implement qilib custom taqsimot yozish mumkin (`spring.kafka.producer.properties.partitioner.class`).

**Qo'llanish keyslari:**
- Redis Cluster'ni 6 node'dan 9 node'ga o'tkazishda cache'ning faqat uchdan birini qayta isitish.
- Cassandra klasteriga yangi node qo'shib, token range'larning kichik qismini ko'chirish.
- Sharding qilingan PostgreSQL'da `tenant_id` bo'yicha shard tanlashni `AbstractRoutingDataSource` ichida ring orqali hisoblash.
- WebSocket/sessiya affinity: foydalanuvchini doim bir xil ilova instansiyasiga yo'naltirish.
- Rate limiter counter'larini node'lar o'rtasida teng taqsimlab, bitta "hot" node'ni oldini olish.

**Ehtiyot bo'ling:** Virtual node'lar bo'lmasa yuklama juda notekis taqsimlanadi, mavjud bo'lsa ham "hot key" (masalan bitta mashhur mahsulot) bitta partition'ni bosib ketadi - bunday kalitlarga suffix qo'shib yoyish yoki local cache bilan himoyalash kerak. Replikatsiya faktori va rack/AZ-aware strategiya noto'g'ri sozlansa, bitta availability zone yiqilganda barcha nusxalar birga yo'qolishi mumkin.

## 28.7 O'qishda tuzatish (Read Repair)

**Tavsif:** O'qish so'rovi bir nechta replikadan javob oladi va ular orasida farq topilsa, koordinator eng yangi versiyani aniqlab, orqada qolgan replikalarga uni yozib qo'yadi. Ya'ni tuzatish o'qish trafigi bilan "tekinga" bajariladi va ko'p o'qiladigan ma'lumot tez konvergatsiya qiladi. Bu leadersiz replikatsiyaning asosiy konsistentlik tiklash mexanizmlaridan biri. Kamchiligi - kam o'qiladigan ma'lumot uzoq vaqt divergent qolishi mumkin.

**Spring'da qayerda uchraydi:** Spring'da ekvivalenti yo'q - bu Cassandra/DynamoDB/Riak ichidagi xatti-harakat. Cassandra'da blocking read repair `QUORUM`/`LOCAL_QUORUM` o'qishda digest mismatch bo'lganda avtomatik ishlaydi, jadval darajasida esa `read_repair = 'BLOCKING'|'NONE'` bilan boshqariladi (eski versiyalarda `read_repair_chance`). Spring Data Cassandra uchun bu shuni bildiradi: `CassandraTemplate` bilan `ONE` darajada o'qiganingizda repair kafolatlanmaydi, `QUORUM`da esa koordinator fonda replikalarni tenglashtiradi - demak konsistentlik darajasini tanlash to'g'ridan-to'g'ri repair xatti-harakatini belgilaydi. Ilova darajasida o'xshash g'oyani cache uchun qurish mumkin: `@Cacheable` bilan o'qiganda stale qiymat aniqlansa `CacheManager` orqali qayta yozish (cache refresh-ahead), lekin bu alohida pattern.

**Qo'llanish keyslari:**
- Cassandra'da mashhur foydalanuvchi profilining `QUORUM` o'qishlari replikalarni avtomatik tenglashtiradi.
- DynamoDB'da `ConsistentRead` bilan o'qish, eventual replikalarni yangilashga majburlash.
- Node uzoq downtime'dan keyin qaytganda, issiq ma'lumot repair orqali tezda to'g'rilanadi.
- Kam o'qiladigan arxiv jadvallar uchun repair'ni o'chirib, o'qish latency'sini kamaytirish.
- Monitoring: `ReadRepairRequests` metrikasi o'sishi replikatsiya muammosiga ishora beradi.

**Ehtiyot bo'ling:** Read repair o'qish latency'si va cross-node trafikni oshiradi, shuning uchun uni yagona konsistentlik mexanizmi sifatida ishlatish xato - hech qachon o'qilmaydigan yozuvlar abadiy divergent qoladi, demak anti-entropy repair ham rejalashtirilishi shart. `read_repair = 'NONE'` qo'yilgan jadvallarda tombstone resurrection (o'chirilgan yozuvning qaytib kelishi) xavfi ortadi.

## 28.8 Anti-entropiya (Anti-Entropy)

**Tavsif:** Replikalar fon rejimida bir-birining ma'lumotini muntazam taqqoslab, farqlarni sinxronlashtiradi - o'qish trafigidan mustaqil ravishda. Butun datasetni uzatmaslik uchun Merkle tree (xesh daraxti) ishlatiladi: faqat xeshi mos kelmagan subrange'lar ko'chiriladi. Bu read repair qamramaydigan "sovuq" ma'lumotni ham konvergatsiya qilishni kafolatlaydi. Odatda rejalashtirilgan repair jarayoni yoki doimiy gossip-asosidagi sinxronizatsiya sifatida ishlaydi.

**Spring'da qayerda uchraydi:** To'liq infra darajasi: Cassandra'da `nodetool repair` (yoki Cassandra Reaper bilan boshqariladigan incremental repair), ScyllaDB'da row-level repair, DynamoDB'da ichki jarayon, Riak'da active anti-entropy. Spring ilovasi buni chaqirmaydi, lekin arxitektor `gc_grace_seconds` ichida repair bajarilishini ta'minlashi kerak - aks holda o'chirilgan yozuvlar qaytib keladi va Spring Data repository'lari "yo'q bo'lgan" entity'ni qaytaradi. Ilova darajasidagi o'xshash yondashuv ham bor: ikki tizim (masalan PostgreSQL va Elasticsearch, yoki DB va Kafka) o'rtasida davriy reconciliation job'ni Spring Batch (`Step` + `ItemReader`/`ItemWriter`) yoki `@Scheduled` bilan yozib, farqlarni topib tuzatish - bu amalda application-level anti-entropy bo'ladi va outbox pattern'dagi yo'qolgan event'larni ham qutqaradi.

**Qo'llanish keyslari:**
- Cassandra klasterida haftalik incremental repair bilan replikalarni tenglashtirish.
- PostgreSQL va Elasticsearch index'ini kechasi Spring Batch job bilan taqqoslab, yo'qolgan dokumentlarni qayta indekslash.
- To'lov tizimi va buxgalteriya ledger'ini kunlik reconciliation bilan solishtirib, farqni alert qilish.
- Uzoq vaqt o'chgan node qaytganda to'liq repair bilan uni ishonchli holatga keltirish.
- Outbox jadvalida `published=false` qolgan yozuvlarni davriy skanerlab qayta yuborish.

**Ehtiyot bo'ling:** To'liq repair juda qimmat - CPU, disk I/O va tarmoqni bosib, production latency'ni buzadi, shuning uchun uni past trafik oynasida va incremental rejimda, throttling bilan bajarish kerak. Repair'ni `gc_grace_seconds` muddatidan kechiktirish esa o'chirilgan ma'lumotning tirilishiga olib keladi - bu "mijoz o'chirgan karta qaytib keldi" tipidagi GDPR muammosini tug'diradi.

## 28.9 Ishora bilan topshirish (Hinted Handoff)

**Tavsif:** Yozuv vaqtida maqsadli replika mavjud bo'lmasa, koordinator node yozuvni o'zida "hint" sifatida vaqtincha saqlaydi va yiqilgan node qaytgach unga uzatadi. Bu yozish availability'sini saqlaydi: bir necha replika o'chgan bo'lsa ham yozuv qabul qilinadi (sloppy quorum). Hintlar cheklangan muddat va hajm bilan saqlanadi; muddat o'tsa hint tashlanadi va ma'lumotni faqat anti-entropy repair tiklaydi. Ya'ni bu durability emas, availability patterni.

**Spring'da qayerda uchraydi:** Cassandra (`hinted_handoff_enabled`, `max_hint_window_in_ms`, `hints_directory`), ScyllaDB, DynamoDB va Riak ichida amalga oshiriladi; Spring ilovasi faqat natijasini ko'radi - yozuv `ONE`/`ANY` darajada muvaffaqiyatli qaytadi, lekin ma'lumot hali haqiqiy replikada emas. Shuning uchun Spring Data Cassandra'da `ConsistencyLevel.ANY` ni hech qachon muhim yozuvlar uchun ishlatmaslik kerak. Ilova darajasidagi analogi - mahalliy durable buffer: Spring Boot'da `@Retryable` (Spring Retry) + Kafka producer'ning ichki `buffer.memory`/`retries` mexanizmi, yoki outbox jadvaliga yozib keyin yuborish; Resilience4j `RateLimiter`/`Retry` bilan birga ishlatilganda bu "broker o'chgan paytda ham yozuvni qabul qilish" xatti-harakatini beradi. Kafka tomonida `acks=1` + retry ham o'xshash kompromissni yaratadi.

**Qo'llanish keyslari:**
- Cassandra node'ni rolling restart qilganda yozuvlar uzilmasdan davom etadi.
- Qisqa tarmoq uzilishi (bir necha daqiqa) paytida telemetriya yozuvlarini yo'qotmaslik.
- Rolling upgrade: har bir node navbati bilan o'chadi, hintlar uni yetib oladi.
- Spring ilovada Kafka vaqtincha ishlamaganda outbox jadvaliga yozib, keyin publisher bilan uzatish.
- AZ o'rtasida qisqa muddatli partition paytida yozish availability'sini saqlash.

**Ehtiyot bo'ling:** Hint'lar coordinator diskida to'planib uni to'ldirishi mumkin, va `max_hint_window` o'tgandan keyin jimgina tashlanadi - ya'ni uzoq downtime'da ma'lumot yo'qoladi, shuning uchun uzoq o'chgan node qaytganda albatta repair bajarish kerak. `ANY` konsistentlik darajasi bilan yozish esa "yozildi" degan javobni beradi, lekin hech bir haqiqiy replikada ma'lumot bo'lmasligi mumkin - buni moliyaviy yoki huquqiy ahamiyatli yozuvlar uchun ishlatish qo'pol xato.

## 28.10 Vektor soat (Vector Clock)

**Tavsif:** Har bir node o'z hisoblagichini yuritadi va yozuv versiyasi barcha node hisoblagichlari vektori sifatida saqlanadi. Ikki versiyani taqqoslaganda biri ikkinchisidan "keyin" (barcha komponentlari ≥) yoki ular parallel (concurrent) ekanligini aniqlash mumkin - shu bilan haqiqiy konfliktni aniqlash yo'l bilan hal qilinadi. Wall-clock vaqtdan farqli, u clock skew'ga bog'liq emas, chunki faqat sabab-natija (causality) munosabatini kuzatadi. Soddalashtirilgan variantlari - version vector va dotted version vector.

**Spring'da qayerda uchraydi:** Spring'da tayyor vector clock abstraksiyasi yo'q; buni ma'lumotlar bazasi (Riak `X-Riak-Vclock`, Voldemort, DynamoDB'ning ilk Dynamo maqolasidagi modeli) yoki ilova kodi beradi. Praktikada Spring loyihalarida ko'proq uning oddiy "skalyar" varianti ishlatiladi: JPA'da `@Version` (optimistic locking, `OptimisticLockingFailureException`), Spring Data MongoDB'da ham `@Version`, Spring Data R2DBC'da `@Version` - bu bitta-leaderli muhitda yetarli, lekin parallellikni tasvirlab bera olmaydi. Haqiqiy multi-master holatda CRDT kutubxonalari (Hazelcast `PNCounter`, Infinispan, Automerge/Yjs kabi tashqi kutubxonalar) yoki qo'lda yozilgan `Map<NodeId, Long>` versiya vektori ishlatiladi; Akka/Pekko Distributed Data esa JVM'da to'liq version vector implementatsiyasini beradi.

**Qo'llanish keyslari:**
- Offline-first mobil ilovada server va qurilma versiyalarini taqqoslab, haqiqiy konfliktni foydalanuvchiga ko'rsatish.
- Hamkorlikda tahrirlanadigan dokument yoki savatcha (shopping cart) merge logikasi.
- Ko'p-regionli profil sozlamalarini LWW'siz, parallellikni saqlab birlashtirish.
- Riak'da `siblings` olib, domen qoidasiga ko'ra avtomatik merge qilish.
- Audit: qaysi o'zgarish qaysidan sabab bo'lganini (causal zanjir) tiklash.

**Ehtiyot bo'ling:** Vektor hajmi node (yoki client) soniga qarab o'sadi va cheksiz ko'p client bo'lsa metadata portlaydi - shu sababli pruning yoki dotted version vector kerak. Shuningdek vector clock konfliktni faqat *aniqlaydi*, hal qilmaydi: merge funksiyasini domen bilan birga loyihalash shart, aks holda konfliktlarni jimgina tashlab yuborish bilan tugaydi.

## 28.11 Oxirgi yozuv g'alaba qozonadi (Last Write Wins)

**Tavsif:** Konflikt yuzaga kelganda eng katta timestamp'ga ega yozuv saqlanadi, qolganlari tashlab yuboriladi. Bu eng oddiy va eng tez konvergatsiya strategiyasi - qo'shimcha metadata yoki merge logikasi talab qilmaydi va har doim bitta yakuniy qiymatga olib keladi. Narxi - jimgina ma'lumot yo'qotish: parallel yozuvlardan biri butunlay yo'qoladi. Node'lar soatlari farq qilsa (clock skew), hatto "eski" yozuv ham g'alaba qozonishi mumkin.

**Spring'da qayerda uchraydi:** Cassandra'da bu standart konflikt yechimi - har bir cell'da yozish timestamp'i bor va eng kattasi g'alaba qozonadi; Spring Data Cassandra bilan yozganda bu avtomatik qo'llanadi, `WriteOptions.builder().timestamp(...)` bilan uni ataylab boshqarish ham mumkin. Redis replikatsiyasi, DynamoDB global table'lari va ko'pchilik cache qatlamlari ham amalda LWW ishlatadi. Spring ilovalarida LWW'ni tasodifiy tanlab qo'yish juda oson: `CrudRepository.save(entity)` to'liq entity'ni UPDATE qiladi, ya'ni ikki parallel HTTP request bir-birining maydonlarini bosib ketadi (lost update) - buning oldini olish uchun `@Version` bilan optimistic locking, `@Lock(LockModeType.PESSIMISTIC_WRITE)`, yoki JPQL'da faqat kerakli maydonni `UPDATE` qilish ishlatiladi. Shuningdek `@DynamicUpdate` (Hibernate) faqat o'zgargan maydonlarni yuboradi va "butun obyektni bosib ketish" muammosini yumshatadi.

**Qo'llanish keyslari:**
- Cache yoki sessiya ma'lumotlari: eng yangi qiymat yetarli, tarix kerak emas.
- Foydalanuvchining "oxirgi faol vaqti" yoki qurilma holati kabi monoton yangilanadigan maydonlar.
- IoT sensor o'qishlari - eng yangi o'lchov eskisini mantiqan almashtiradi.
- UI sozlamalari (til, mavzu) - konflikt narxi past, LWW qabul qilinadi.
- Materialized view yoki search index'ni yangilash: oxirgi holat manba haqiqatiga mos keladi.

**Ehtiyot bo'ling:** Pul, inventar zaxirasi, hisob balansi yoki hujjat matni kabi "yo'qotish qimmat" ma'lumotlar uchun LWW ishlatish mutlaqo yaroqsiz - u yerda optimistic locking, CRDT yoki event-sourcing kerak. Server soatlari NTP bilan sinxron bo'lmasa LWW noto'g'ri g'olibni tanlaydi; shu sababli timestamp'ni client emas, yagona ishonchli manba yoki hybrid logical clock bersin.

## 28.12 Fencing token (Fencing Token)

**Tavsif:** Lock yoki leadership berilganda unga monoton o'sadigan raqam (token) ham qo'shib beriladi, va har bir yozuv shu tokenni resursga ko'rsatadi. Resurs o'zi ko'rgan eng katta tokendan kichik tokenli so'rovni rad etadi - shu bilan "muzlab qolgan" (GC pause, tarmoq uzilishi tufayli lease'i allaqachon tugagan) eski leader ma'lumotni buza olmaydi. Bu taqsimlangan lock'ning asosiy xavfi - lease muddati tugaganini bilmaydigan client - ga yagona ishonchli yechim. Oddiy "lock oldim" tekshiruvi bundan himoya qilmaydi.

**Spring'da qayerda uchraydi:** Spring Integration `LockRegistry` (`RedisLockRegistry`, `JdbcLockRegistry`, `ZookeeperLockRegistry`) va ShedLock/Quartz lock'lari o'zidan fencing token bermaydi - ular lease asosida ishlaydi, demak `@SchedulerLock` yoki `RedisLockRegistry` bilan "faqat bitta instansiya ishlaydi" degan taxmin qat'iy kafolat emas. To'g'ri yechim: tokenni manba tomonida tekshirish. ZooKeeper'da `zxid`/znode `czxid`, etcd'da `revision`, Kafka'da `transactional.id` bilan bog'liq producer epoch (`enable.idempotence=true`, Spring Kafka `KafkaTransactionManager`) aynan fencing rolini bajaradi - eski producer `ProducerFencedException` oladi. DB darajasida esa `@Version` ustun yoki `UPDATE ... WHERE epoch < :epoch` shartli yozuv bilan token amalga oshiriladi; Spring Data `@Query` + `@Modifying` bu uchun qulay.

```java
@Modifying
@Query("UPDATE Job j SET j.state = :state, j.epoch = :epoch " +
       "WHERE j.id = :id AND j.epoch <= :epoch")
int applyIfNotFenced(@Param("id") Long id,
                     @Param("state") String state,
                     @Param("epoch") long epoch);
```

**Qo'llanish keyslari:**
- Bitta instansiya bajarishi kerak bo'lgan batch job'da epoch bilan yozib, eski instansiyaning yozuvini rad etish.
- Leader election (ZooKeeper/etcd) dan keyin fayl yoki jadvalga yozishni token bilan himoyalash.
- Kafka exactly-once: `transactional.id` bilan zombi producer avtomatik fence qilinadi.
- Taqsimlangan lock ostida S3/fayl tizimiga yozishda versiya raqamini obyekt metadata'siga kiritish.
- Database leader failover'dan keyin eski primary'ga yozishni bloklash (STONITH o'rniga mantiqiy fencing).

**Ehtiyot bo'ling:** Fencing faqat resurs tokenni *tekshirganda* ishlaydi - client tomonda token saqlash o'z-o'zidan hech narsa bermaydi, va aynan shu xato Redlock atrofidagi mashhur tanqidning o'zagi. Tokenni monoton berish uchun bitta ishonchli manba (ZooKeeper, etcd, DB sequence) kerak; uni mahalliy timestamp yoki random UUID bilan almashtirish himoyani butunlay yo'q qiladi.

## 28.13 Linearizatsiyalanganlik (Linearizability)

**Tavsif:** Eng kuchli single-object konsistentlik modeli: tizim xuddi bitta nusxa va bitta atomik operatsiyalar ketma-ketligi bordek ko'rinadi, va operatsiya tugagandan keyin barcha keyingi o'qishlar uning natijasini ko'radi. Bu "real vaqt" tartibini hurmat qiladi - shuning uchun compare-and-set, unique constraint va leader election kabi narsalar faqat linearizable store'da to'g'ri ishlaydi. Narxi: konsensus talab qiladi, demak latency yuqori va tarmoq partition'ida availability yo'qoladi (CAP'dagi CP tanlovi). Odatda faqat kichik, kritik metadata uchun ishlatiladi.

**Spring'da qayerda uchraydi:** Spring'da model emas, lekin unga tayanadigan komponentlar ko'p. Koordinatsiya uchun ZooKeeper (`spring-cloud-zookeeper`, Curator), etcd, Consul yoki Raft asosidagi DB (CockroachDB `SERIALIZABLE`) ishlatiladi; Spring Cloud Kubernetes `ConfigMap`/`Lease` orqali leader election ham etcd'ning linearizable o'qishlariga tayanadi (`spring-cloud-kubernetes-fabric8-leader`). PostgreSQL'da yagona primary'ga `SERIALIZABLE` izolyatsiya darajasi (`@Transactional(isolation = Isolation.SERIALIZABLE)`) amalda linearizable xatti-harakat beradi, lekin faqat shu primary chegarasida - asinxron replica'dan o'qish uni darhol buzadi. MongoDB'da `ReadConcern.LINEARIZABLE` + `WriteConcern.MAJORITY` kombinatsiyasi mavjud va Spring Data MongoDB `MongoTemplate` sozlamalari orqali beriladi. Muhim nuqta: `@Transactional` bir necha servis yoki bazaga tarqalganda hech qanday linearizability bermaydi - u yerda saga yoki konsensus kerak.

**Qo'llanish keyslari:**
- Leader election: butun klaster bitta leader borligiga kelishishi kerak (ZooKeeper/etcd).
- Unique username yoki hisob raqamini yaratishda ikkita bir xil qiymat paydo bo'lishini oldini olish.
- Bank hisobidan pul yechishda balansni compare-and-set bilan atomik kamaytirish.
- Taqsimlangan lock va fencing token generatsiyasi uchun monoton counter.
- Feature flag yoki konfiguratsiya o'zgarishini barcha instansiyalar bir xil tartibda ko'rishi.

**Ehtiyot bo'ling:** Linearizability'ni butun tizimga qo'llash eng keng tarqalgan over-engineering - u cross-region latency'ni o'n barobar oshiradi va partition paytida yozishni to'xtatadi, shuning uchun uni faqat haqiqiy constraint talab qiladigan kichik ma'lumotga cheklang. Shuningdek "SERIALIZABLE qo'ydim, demak hamma joyda to'g'ri" degan taxmin xato: cache, read replica, search index va event stream bu kafolatdan tashqarida qoladi.

## 28.14 Kauzal konsistentlik (Causal Consistency)

**Tavsif:** Sabab-natija bilan bog'langan operatsiyalar barcha node'larda bir xil tartibda ko'rinadi, parallel (bog'liq bo'lmagan) operatsiyalar esa har xil tartibda ko'rinishi mumkin. Bu linearizability'dan ancha arzon - konsensus kerak emas, shuning uchun partition paytida ham availability saqlanadi - lekin eng ko'p uchraydigan anomaliyalarni (javob asl xabardan oldin ko'rinishi, o'z yozuvini o'qiy olmaslik) yo'q qiladi. Amalda session guarantees (read-your-writes, monotonic reads, writes-follow-reads) sifatida beriladi. Ko'pgina ilovalar uchun bu "to'g'ri" o'rta nuqta.

**Spring'da qayerda uchraydi:** MongoDB causally consistent session'larni beradi (`ClientSession` + `causalConsistency(true)`), Spring Data MongoDB esa `MongoTemplate.withSession(...)` yoki `SessionScoped`/`MongoTransactionManager` orqali shu sessiyani ishlatadi - bu yerda `operationTime` va cluster time token'lari avtomatik tashiladi. Kafka'da kauzal tartib partition ichida kafolatlanadi: bir xil kalit (`orderId`) bir xil partition'ga tushadi, shuning uchun `KafkaTemplate.send(topic, key, payload)` da kalitni to'g'ri tanlash - kauzallikni saqlashning asosiy vositasi; Spring Cloud Stream'da bu `partitionKeyExpression` bilan beriladi. PostgreSQL read replica'da o'xshash natijaga `pg_current_wal_lsn()` ni sessiyada saqlab, replica'da `pg_wal_lsn_diff` bilan kutish (LSN-based read-your-writes) yoki oddiygina yozishdan keyingi o'qishni primary'ga routing qilish orqali erishiladi. Redis'da `WAIT` komandasi ham shunga yaqin kafolat beradi.

**Qo'llanish keyslari:**
- Izoh (comment) va unga javob: javob hech qachon asl izohdan oldin ko'rinmasligi kerak.
- Foydalanuvchi profilni yangilagach, darhol o'z yangi ma'lumotini ko'rishi (read-your-writes).
- Chat: xabarlar suhbat ichida yuborilgan tartibda yetib borishi (bir xil Kafka kaliti).
- Buyurtma holati zanjiri `CREATED → PAID → SHIPPED` tartibini saqlash.
- Monotonic reads: foydalanuvchi sahifani yangilaganda ma'lumot "orqaga qaytmasligi".

**Ehtiyot bo'ling:** Kauzal konsistentlik unique constraint, balans tekshiruvi yoki boshqa global invariantni himoya qilmaydi - parallel yozuvlarga yo'l bergani uchun "ikki kishi bir xil nickname oldi" muammosi saqlanadi, bunday joyda linearizability kerak. Shuningdek kauzallikni ta'minlash sessiya token'larini butun zanjir bo'ylab (HTTP → servis → DB) tashishni talab qiladi: load balancer yoki async worker tokenni tashlab ketsa, kafolat jimgina yo'qoladi.

## 28.15 O'z yozuvingni o'qish konsistentligi (Read-Your-Writes Consistency)

**Tavsif:** Replikatsiyalangan tizimda foydalanuvchi o'zi yozgan ma'lumotni keyingi o'qishda albatta ko'rishini kafolatlaydigan sessiya darajasidagi konsistentlik modeli. Yozuv primary nodega tushadi, lekin o'qish read replica'ga yo'naltirilsa, replikatsiya lag'i sababli foydalanuvchi o'zi saqlagan profilni eski holatda ko'rishi mumkin. Pattern buni sessiyaga bog'langan marshrutlash (sticky routing), yozuv timestamp'ini kuzatish yoki yozuvdan keyingi ma'lum oyna ichida o'qishni primary'dan olish orqali hal qiladi. Natijada global strong consistency narxini to'lamasdan foydalanuvchi uchun "to'g'ri" ko'rinadigan tajriba olinadi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x'dagi `AbstractRoutingDataSource` (`org.springframework.jdbc.datasource.lookup`) va `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` asosida yozilgan router read/write DataSource tanlashga imkon beradi; `@Transactional(readOnly = true)` bilan belgilangan metodlarni replica'ga, qolganini primary'ga yuborish keng tarqalgan yondashuv. Foydalanuvchining oxirgi yozuv vaqtini `HttpSession`da yoki Spring Session (Redis) orqali saqlab, router shu asosda primary'ga qaytishi mumkin. Spring Data MongoDB'da `ReadPreference.primaryPreferred()` ni `@Query` yoki `MongoTemplate.withReadPreference(...)` bilan belgilash, Spring Data Cassandra'da `ConsistencyLevel.LOCAL_QUORUM` tanlash shu kafolatga yaqinlashtiradi. Asosiy mexanizm ma'lumotlar bazasi/driver darajasida bo'ladi - Spring faqat marshrutlash va sessiya kontekstini boshqaradi.

**Qo'llanish keyslari:**
- Foydalanuvchi profilini tahrirlagandan so'ng profil sahifasi darhol yangi ma'lumotni ko'rsatishi kerak bo'lgan hollar.
- Kommentariya yoki post qo'shgandan keyin feed'da o'z yozuvini ko'rish (social media pattern).
- Buyurtma yaratilgandan keyin "Mening buyurtmalarim" ro'yxatida uni darhol ko'rsatish.
- Admin panelda narx o'zgartirilgandan so'ng tekshirish uchun qayta o'qish.
- Hisob sozlamalarini saqlagandan keyin shu sozlama bilan ishlovchi keyingi so'rov.

**Ehtiyot bo'ling:** Sticky session'ga tayanish load balancer o'zgarganda yoki node yiqilganda kafolatni buzadi, shuning uchun sessiyaga emas, yozuv versiyasi/LSN'ga tayanish ishonchliroq. Barcha o'qishni primary'ga yuborib "muammoni hal qilish" read replica'larning ma'nosini yo'q qiladi va primary'ni ortiqcha yuklaydi.

## 28.16 Monoton o'qishlar (Monotonic Reads)

**Tavsif:** Agar client bir marta ma'lumotning N versiyasini ko'rgan bo'lsa, keyingi o'qishlarda undan eski versiyani ko'rmasligini kafolatlaydigan sessiya konsistentligi. Buzilgan holatda foydalanuvchi sahifani yangilaganda ma'lumot "orqaga qaytib ketadi" - bir replica ilgarilab ketgan, ikkinchisi lag'da bo'lgani uchun. Yechim: bitta client doim bitta replica'ga bog'lanadi (replica affinity) yoki client ko'rgan oxirgi versiya tokenini (vector clock, timestamp) so'rov bilan jo'natadi va replica undan orqada bo'lsa so'rovni rad etadi yoki kutadi.

**Spring'da qayerda uchraydi:** Spring'ning o'zida maxsus sinf yo'q - bu infratuzilma darajasidagi kafolat. Spring ilovasida `AbstractRoutingDataSource` bilan client ID (yoki session ID) hash'i asosida doim bitta replica tanlanadi; Spring Cloud Gateway'da `LoadBalancerClient` va `RequestBasedStickySessionServiceInstanceListSupplier` orqali so'rovlarni bir instansga biriktirish mumkin. MongoDB driver'ida causal consistent session (`ClientSession` + `causallyConsistent(true)`) `MongoTemplate.withSession(...)` orqali ishlatiladi va bu monotonic reads'ni driver darajasida ta'minlaydi. Kafka consumer'larda esa bitta partition'dan o'qish tartibi tabiiy monotonlikni beradi, shuning uchun `@KafkaListener` bilan ishlovchi projeksiyalar partition kaliti to'g'ri tanlanganda bu kafolatga ega bo'ladi.

**Qo'llanish keyslari:**
- Dashboard'dagi hisoblagich yoki balans refresh'da kamayib ketmasligi kerak bo'lgan holatlar.
- Yetkazib berish holati (status) "Jo'natildi" dan yana "Qabul qilindi" ga qaytmasligi.
- Chat tarixini scroll qilganda avval ko'rilgan xabarlarning yo'qolib qolmasligi.
- Audit log yoki tranzaksiya tarixini sahifalab ko'rishda yozuvlar yo'qolmasligi.
- CQRS read model'ini bir nechta instansdan o'qiyotgan SPA uchun barqaror ko'rinish.

**Ehtiyot bo'ling:** Replica affinity bitta replica'ni "hot" qilib qo'yishi va u yiqilganda client kafolatni yo'qotishi mumkin - failover paytida versiya tokenini tekshirish shart. Timestamp asosidagi yechimda node'lar soatlari farq qilsa (clock skew) kafolat yolg'on bo'lib chiqadi, shuning uchun logical yoki hybrid logical clock ishlatiladi.

## 28.17 Yakuniy konsistentlik (Eventual Consistency)

**Tavsif:** Yangi yozuvlar bo'lmasa, barcha replicalar oxir-oqibat bir xil holatga kelishini kafolatlaydigan, lekin oraliq vaqtda nomuvofiqlikka yo'l qo'yadigan konsistentlik modeli. CAP teoremasi bo'yicha network partition sharoitida availability'ni tanlash natijasi: tizim yozuvni qabul qiladi va replikatsiyani asinxron bajaradi. Konfliktlar last-write-wins, vector clock yoki CRDT kabi strategiyalar bilan hal qilinadi. Amalda biznes domeni "qancha vaqt nomuvofiq bo'lishi mumkin" degan savolga javob berishi kerak.

**Spring'da qayerda uchraydi:** Spring'ning event-driven stack'i bu modelni tabiiy qo'llaydi: `ApplicationEventPublisher` va `@TransactionalEventListener(phase = AFTER_COMMIT)` lokal konsistentlikni, Spring for Apache Kafka (`@KafkaListener`, `KafkaTemplate`) yoki Spring AMQP (`@RabbitListener`) esa xizmatlar orasidagi yakuniy konsistentlikni ta'minlaydi. Spring Data Redis bilan qurilgan cache'lar `@Cacheable`/`@CacheEvict` orqali TTL davomida eskirgan ma'lumot qaytarishi - bu ham eventual consistency. Spring Data Cassandra va Spring Data MongoDB (`ReadPreference.secondaryPreferred()`) tunable consistency bilan ishlaydi; Spring Data Elasticsearch'da `RefreshPolicy` (`IMMEDIATE`, `WAIT_UNTIL`, `NONE`) indeks ko'rinish kechikishini boshqaradi. Spring Modulith esa event publication registry bilan domain event'larni ishonchli yetkazib, konvergentsiyani kafolatlaydi.

**Qo'llanish keyslari:**
- Mikroservislar orasida mijoz ma'lumotini denormalizatsiya qilib nusxalash (read model).
- Mahsulot katalogini Elasticsearch'ga indekslash va qidiruvda bir necha sekundlik lag'ga ruxsat berish.
- Like, ko'rishlar soni, reyting kabi aniqligi kritik bo'lmagan hisoblagichlar.
- Bir nechta regiondagi CDN yoki cache qatlamini yangilash.
- Analytics va reporting uchun operatsion bazadan data warehouse'ga ETL/CDC.

**Ehtiyot bo'ling:** Pul balansi, inventar rezervatsiyasi yoki unique constraint talab qiladigan (masalan email ro'yxatdan o'tish) joylarda eventual consistency ikki marta sarflash yoki dublikat yaratishga olib keladi - bu yerda strong consistency yoki kompensatsiya mexanizmi kerak. UI'da "hali yangilanmagan" holatni yashirish foydalanuvchini chalg'itadi, shuning uchun optimistik ko'rsatish yoki aniq status belgisi berish kerak.

## 28.18 Snapshot izolyatsiyasi / MVCC (Snapshot Isolation / MVCC)

**Tavsif:** Har bir tranzaksiya ma'lumotlar bazasining boshlanish momentidagi muvofiq "suratini" ko'radigan izolyatsiya darajasi. Multi-Version Concurrency Control (MVCC) buni qatorlarning bir nechta versiyasini saqlash orqali amalga oshiradi: o'quvchilar yozuvchilarni, yozuvchilar o'quvchilarni bloklamaydi. Natijada dirty read, non-repeatable read va ko'p hollarda phantom read yo'qoladi, lekin write skew kabi anomaliyalar qoladi. PostgreSQL, Oracle, MySQL InnoDB va SQL Server (snapshot rejimida) shu mexanizmga asoslangan.

**Spring'da qayerda uchraydi:** Spring'da bu `@Transactional(isolation = Isolation.REPEATABLE_READ)` yoki `Isolation.SERIALIZABLE` bilan deklarativ belgilanadi va `PlatformTransactionManager` (masalan `JpaTransactionManager`, `DataSourceTransactionManager`) uni JDBC `Connection.setTransactionIsolation(...)` ga tarjima qiladi. PostgreSQL'da `REPEATABLE_READ` aslida snapshot isolation beradi. JPA/Hibernate darajasidagi persistence context ham o'ziga xos "repeatable read" effektini beradi (bir sessiyada bir xil ID doim bir xil entity instansi), lekin bu DB izolyatsiyasining o'rnini bosmaydi. Optimistik boshqaruv uchun `@Version` (`jakarta.persistence.Version`) ishlatiladi va konflikt `OptimisticLockingFailureException` sifatida chiqadi; R2DBC stack'ida `R2dbcTransactionManager` va `TransactionalOperator` orqali xuddi shu izolyatsiya darajalari beriladi.

**Qo'llanish keyslari:**
- Uzoq davom etadigan hisobot so'rovi ishlayotgan vaqtda OLTP yozuvlarini bloklamaslik.
- Bir tranzaksiyada bir nechta jadvaldan muvofiq holatni o'qib, moliyaviy hisob-kitob qilish.
- Batch job ma'lumotni o'qiyotganda parallel foydalanuvchi yozuvlariga to'sqinlik qilmaslik.
- `@Version` bilan optimistik lock orqali parallel tahrirlashni aniqlash (koredaktsiya konflikti).
- Backup yoki export jarayonida izchil kesim olish.

**Ehtiyot bo'ling:** Snapshot isolation write skew'ni to'xtatmaydi - "ikki shifokor bir vaqtda navbatchilikdan chiqishi" tipidagi invariant buzilishi o'tib ketadi, buning uchun `SELECT ... FOR UPDATE`, serializable daraja yoki aniq constraint kerak. Uzoq ochiq tranzaksiyalar eski versiyalarni ushlab turib PostgreSQL'da table bloat va vacuum muammosini keltiradi, shuning uchun `@Transactional` metodlari ichida tashqi HTTP chaqiruvlar qilmaslik kerak.

## 28.19 Serializable snapshot izolyatsiyasi (Serializable Snapshot Isolation)

**Tavsif:** Snapshot isolation'ning optimistik kuchaytirilgan varianti: tranzaksiyalar lock olmasdan snapshot ustida ishlaydi, lekin DB o'qish-yozish bog'liqliklarini kuzatib boradi va serializatsiyani buzadigan konfliktni aniqlaganda tranzaksiyalardan birini abort qiladi. Shu bilan 2PL'ning bloklash narxisiz haqiqiy serializable semantikasi olinadi va write skew ham yo'qoladi. PostgreSQL'ning `SERIALIZABLE` darajasi (SSI) va CockroachDB'ning standart rejimi shu yondashuvga asoslangan.

**Spring'da qayerda uchraydi:** `@Transactional(isolation = Isolation.SERIALIZABLE)` PostgreSQL ustida ishlaganda SSI'ni yoqadi; konflikt yuz berganda driver SQLSTATE 40001 qaytaradi va Spring'ning `SQLExceptionTranslator`i uni `CannotAcquireLockException` yoki `ConcurrencyFailureException` (ikkisi ham `TransientDataAccessException`) ga aylantiradi. Bu abort'lar normal hodisa bo'lgani uchun retry qatlam majburiy: Spring Retry'ning `@Retryable(retryFor = ConcurrencyFailureException.class)` yoki Resilience4j retry dekoratori ishlatiladi. Muhim nuqta - retry `@Transactional` ning TASHQARISIDA bo'lishi kerak, aks holda abort qilingan tranzaksiya ichida qayta urinish ma'nosiz bo'ladi.

```java
@Retryable(retryFor = ConcurrencyFailureException.class, maxAttempts = 4,
           backoff = @Backoff(delay = 50, multiplier = 2.0))
public void reserve(Long roomId, LocalDate day) {
    bookingService.reserveInTx(roomId, day); // @Transactional(isolation = SERIALIZABLE)
}
```

**Qo'llanish keyslari:**
- Mehmonxona/uchrashuv xonasini band qilishda qo'shni oraliqlar kesishmasligini kafolatlash.
- Bank hisobida balans manfiy bo'lmasligi invariantini bir nechta hisob ustida tekshirish.
- Navbatchilik yoki smena jadvalida minimal xodim soni shartini saqlash.
- Cheklangan chipta/aksiya kvotasini oversell qilmasdan taqsimlash.
- Murakkab multi-row invariantli buxgalteriya yozuvlari.

**Ehtiyot bo'ling:** Yuqori konkurrensiyada abort darajasi keskin oshadi va retry bilan tizim throughput'i tushadi - tranzaksiyalarni qisqa ushlash va konflikt zonalarini kichraytirish kerak. MySQL InnoDB'da `SERIALIZABLE` SSI emas, balki har bir `SELECT`ga shared lock qo'yadigan 2PL'ga o'tadi, shuning uchun "serializable" so'zi bazaga qarab butunlay boshqa performans profilini beradi.

## 28.20 Write skew anomaliyasi (Write Skew)

**Tavsif:** Ikki tranzaksiya bir xil ma'lumot to'plamini o'qib, keyin turli qatorlarni yangilagan natijada umumiy invariant buziladigan anomaliya. Klassik misol: ikki shifokordan kamida biri navbatchilikda qolishi kerak, ikkalasi ham "boshqasi bor" deb ko'rib, ikkalasi ham chiqib ketadi. Har bir tranzaksiya alohida to'g'ri, lekin snapshot isolation ularni bloklamaydi, chunki yozuvlar bir-birining ustiga tushmaydi. Yechim: materializing conflict (sun'iy qator yoki lock jadvali), `SELECT ... FOR UPDATE` bilan o'qilgan qatorlarni bloklash, serializable (SSI) daraja yoki DB-level constraint.

**Spring'da qayerda uchraydi:** Bu Spring'ning emas, izolyatsiya darajasining xususiyati - Spring faqat uni boshqarish vositalarini beradi. Spring Data JPA'da `@Lock(LockModeType.PESSIMISTIC_WRITE)` repository metodiga qo'yiladi yoki `EntityManager.lock(entity, PESSIMISTIC_WRITE)` chaqiriladi; `@Lock(LockModeType.OPTIMISTIC_FORCE_INCREMENT)` esa o'qilgan aggregate'ning `@Version`ini majburan oshirib, konfliktni ko'rinadigan qiladi. Aggregate chegarasini to'g'ri tanlash (DDD) - eng ishonchli yechim: invariant bitta aggregate root ichida bo'lsa, uning `@Version`i write skew'ni avtomatik to'xtatadi. Alternativ sifatida `ShedLock` yoki Redis/Zookeeper distributed lock ishlatiladi, lekin bu DB tranzaksiyasi bilan atomar emasligini hisobga olish kerak.

**Qo'llanish keyslari:**
- "Kamida bitta admin qolishi kerak" tipidagi rol boshqaruvi tekshiruvlari.
- Jadval/navbatchilik tizimida minimal qoplama shartini saqlash.
- Umumiy limit (masalan jamoaning umumiy byudjeti) ostida parallel xarajat yozuvlari.
- Ikki hisob o'rtasida o'tkazmada jami summaning saqlanishi.
- Bir vaqtning o'zida ikki joydan band qilinmasligi kerak bo'lgan resurs (uskuna, zal).

**Ehtiyot bo'ling:** `@Version` faqat o'zgartirilgan qatorlarni himoya qiladi - invariant boshqa qatorlarni O'QISHga tayansa, versiya oshmaydi va skew o'tib ketadi; shuning uchun o'qilgan "guard" qatorini ham qulflash yoki force-increment qilish kerak. Application darajasida `if (count > 1) ...` tekshiruvi tranzaksiyasiz yoki noto'g'ri izolyatsiyada hech qanday kafolat bermaydi.

## 28.21 Fantom o'qish (Phantom Read)

**Tavsif:** Bir tranzaksiya ichida bir xil shart bo'yicha so'rov ikkinchi marta bajarilganda, parallel tranzaksiya qo'shgan (yoki o'chirgan) yangi qatorlar paydo bo'lishi/yo'qolishi. Non-repeatable read mavjud qatorning o'zgarishi haqida bo'lsa, phantom read natija TO'PLAMINING o'zgarishi haqida. `READ_COMMITTED` va ba'zi hollarda `REPEATABLE_READ` bunga yo'l qo'yadi; to'liq himoya range lock / predicate lock (`SERIALIZABLE`) yoki MVCC snapshot orqali olinadi.

**Spring'da qayerda uchraydi:** `@Transactional(isolation = Isolation.REPEATABLE_READ | Isolation.SERIALIZABLE)` orqali boshqariladi; PostgreSQL'da `REPEATABLE_READ` snapshot sababli phantom'ni bloklaydi, MySQL InnoDB'da esa gap lock bilan oldini oladi. Spring Data JPA'da pagination (`Pageable`, `Page`) bilan ishlaganda tranzaksiya chegarasi odatda bitta so'rovga teng bo'lgani uchun sahifalar orasida phantom paydo bo'ladi - bu holda keyset (cursor) pagination yoki `Slice` bilan barqaror kalit bo'yicha o'tish tavsiya etiladi. Spring Batch'da `JpaPagingItemReader` o'rniga `JdbcCursorItemReader` yoki sorted keyset reader ishlatish shu muammoni kamaytiradi. `COUNT` + `INSERT` tipidagi tekshiruvlarda esa unique index yoki `@Lock(PESSIMISTIC_WRITE)` ishonchli yechim.

**Qo'llanish keyslari:**
- "Shu intervalda band bo'lmagan vaqt bormi?" tekshiruvidan keyin yozuv qo'shish (double booking oldini olish).
- Hisobot ichida `COUNT` va detal ro'yxat mos kelishi kerak bo'lgan moliyaviy yakun.
- Spring Batch chunk'lari orasida yangi yozuvlar qo'shilganda element'larning ikki marta/hech qachon o'qilmasligi.
- Kvota tekshiruvi: "limitdan kam yozuv bormi?" so'rovidan keyin insert.
- Sahifalangan admin ro'yxatida bir xil yozuvning ikki sahifada ko'rinishini oldini olish.

**Ehtiyot bo'ling:** Phantom'ni to'liq yo'q qilish uchun izolyatsiyani `SERIALIZABLE`ga ko'tarish global throughput'ni pasaytiradi - ko'pincha faqat konflikt zonasida unique constraint qo'yish arzonroq va ishonchliroq. Pagination muammosini izolyatsiya darajasi bilan hal qilishga urinish noto'g'ri yondashuv, chunki HTTP so'rovlar orasidagi vaqt hech qanday DB tranzaksiyasi bilan qoplanmaydi.

## 28.22 Ikki fazali qulflash (Two-Phase Locking)

**Tavsif:** Serializatsiyani ta'minlovchi pessimistik konkurrensiya protokoli: tranzaksiya o'sish fazasida kerakli lock'larni oladi va hech birini qo'yib yubormaydi, keyin qisqarish fazasida (odatda commit paytida - strict 2PL) hammasini birdan bo'shatadi. Shared (o'qish) va exclusive (yozuv) lock'lar, shuningdek range/gap lock'lar orqali barcha anomaliyalar, shu jumladan write skew va phantom read, bloklanadi. Narxi: bloklanish, throughput pasayishi va deadlock ehtimoli.

**Spring'da qayerda uchraydi:** Spring Data JPA'da `@Lock(LockModeType.PESSIMISTIC_WRITE)` yoki `PESSIMISTIC_READ` repository metodida (`SELECT ... FOR UPDATE` generatsiya qiladi), `jakarta.persistence.lock.timeout` hint'i bilan kutish vaqtini cheklash mumkin. Dastlabki JDBC qatlamida `JdbcTemplate` bilan `FOR UPDATE SKIP LOCKED` yozish queue pattern uchun keng ishlatiladi. Deadlock yuz berganda Spring `DeadlockLoserDataAccessException` (`PessimisticLockingFailureException` ierarxiyasi) ni ko'taradi va `@Retryable` bilan qayta urinish mumkin. Spring Integration'ning `JdbcLockRegistry`, ShedLock'ning JDBC provider'i va `LockRegistryLeaderInitiator` ham mohiyatan DB lock'lariga tayanadi.

```java
public interface AccountRepository extends JpaRepository<Account, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000"))
    Optional<Account> findByIdForUpdate(Long id);
}
```

**Qo'llanish keyslari:**
- Hisob balansini o'zgartirishda qatorni qulflab, lost update'ni butunlay yo'q qilish.
- Konkurrensiyasi yuqori, lekin konflikti tez-tez bo'ladigan hot row'lar (optimistik retry samarasiz bo'lganda).
- DB jadvalini ish navbati sifatida ishlatish: `FOR UPDATE SKIP LOCKED` bilan har bir worker boshqa yozuvni oladi.
- Inventar rezervatsiyasi va oversell'ni oldini olish.
- Legacy integratsiyada tashqi tizim bilan sinxron ishlash uchun resurs lock'i.

**Ehtiyot bo'ling:** Lock'lar har xil tartibda olinsa deadlock kafolatlangan - barcha kodda resurslarni bir xil (masalan ID bo'yicha o'sish) tartibda qulflash va `lock.timeout` qo'yish shart. Lock ushlab turgan tranzaksiya ichida tashqi API chaqirish yoki uzoq hisoblash qilish butun jadvalni bloklab, cascade failure'ga olib keladi.

## 28.23 Konsensus (Consensus (Raft / Paxos))

**Tavsif:** Node'lar to'plami, ularning bir qismi yiqilgan yoki tarmoq kechikkan sharoitda ham bitta qiymat yoki operatsiyalar ketma-ketligi haqida kelishuvga erishish algoritmlari. Raft leader election, log replication va safety fazalariga bo'linib, kvorum (N/2+1) tasdig'i bilan commit qiladi; Paxos nazariy jihatdan ekvivalent, lekin amalga oshirilishi murakkabroq. Bu replikatsiyalangan state machine, linearizable yozuv va split brain'dan himoyaning asosi.

**Spring'da qayerda uchraydi:** Spring'da konsensus algoritmi implementatsiyasi yo'q - u infratuzilma komponentlarida yashaydi: Kafka (KRaft yoki ZooKeeper), etcd, Consul, ZooKeeper, MongoDB replica set election, PostgreSQL Patroni. Spring ilovasi ularga client sifatida tayanadi: Spring Cloud Consul / Spring Cloud Zookeeper discovery va `@EnableDiscoveryClient`, Spring Cloud Kubernetes (etcd ortidagi API server bilan `ConfigMap`/`Lease` orqali). Leader election uchun Spring Integration'ning `LeaderInitiator` abstraksiyasi (`spring-integration-zookeeper`'dagi `LeaderInitiator`, yoki `LockRegistryLeaderInitiator` Hazelcast/JDBC/Redis lock registry bilan) ishlatiladi va ilova `AbstractLeaderEvent` (`OnGrantedEvent`, `OnRevokedEvent`) ni `@EventListener` bilan tinglaydi. Kafka'ga yozishda `acks=all` va `min.insync.replicas` sozlamalari (`spring.kafka.producer.acks`) kvorum semantikasini ilova darajasida ko'rsatadi.

**Qo'llanish keyslari:**
- Scheduled job'ni klasterda faqat bitta instans bajarishi uchun leader tanlash.
- Service discovery va dinamik konfiguratsiyani izchil saqlash (Consul/etcd).
- Kafka partition leader'ini avtomatik failover qilish va ma'lumot yo'qolmasligini kafolatlash.
- Ma'lumotlar bazasi primary'sini avtomatik almashtirish (Patroni, MongoDB election).
- Distributed lock va lease'larni ishonchli berish (Kubernetes `Lease` obyekti).

**Ehtiyot bo'ling:** Konsensus har bir yozuvga kvorum round-trip narxini qo'shadi, shuning uchun uni yuqori hajmli ma'lumot yo'lida emas, metadata va koordinatsiya qarorlarida ishlatish kerak; juft sonli node (masalan 2 yoki 4) kvorumni yaxshilamaydi, balki fault tolerance'ni buzadi. Redis'ning oddiy `SETNX` lock'i konsensusga asoslangan emas - failover paytida ikki egalik (mutual exclusion buzilishi) bo'lishi mumkin, shuning uchun kritik mutual exclusion uchun fencing token qo'shish yoki etcd/ZooKeeper ishlatish zarur.

## 28.24 Umumiy tartibli broadcast (Total Order Broadcast)

**Tavsif:** Barcha node'lar xabarlarni bir xil ketma-ketlikda qabul qilishini kafolatlaydigan yetkazib berish abstraksiyasi (atomic broadcast). Agar har bir replica bir xil tartibda bir xil deterministik operatsiyalarni qo'llasa, ularning holati bir xil bo'ladi - bu replicated state machine asosi. Amalda konsensusga ekvivalent muammo bo'lib, append-only log (Kafka partition, Raft log) orqali amalga oshiriladi: log'ga yozilgan tartib global tartib bo'lib xizmat qiladi.

**Spring'da qayerda uchraydi:** Spring for Apache Kafka bu patternning eng keng tarqalgan amalga oshirilishi: bitta partition ichida tartib kafolatlangani uchun `KafkaTemplate.send(topic, key, payload)` da kalitni aggregate ID qilib tanlash barcha consumer'larga bir xil tartibni beradi. Tartibni saqlab qolish uchun `max.in.flight.requests.per.connection=1` yoki idempotent producer (`enable.idempotence=true`, Spring Boot 3.x'da `spring.kafka.producer.properties`) va consumer tomonda `ConcurrentKafkaListenerContainerFactory` concurrency'sini partition sonidan oshirmaslik kerak. Event sourcing stack'ida Axon Framework (Spring Boot starter bilan) global sequence number bo'yicha tartibli event stream beradi; Spring Modulith'ning event publication registry esa yetkazib berish ishonchliligini ta'minlaydi, lekin global tartibni emas.

**Qo'llanish keyslari:**
- Event sourcing'da aggregate event'larini qat'iy tartibda replay qilish.
- CQRS read model'larini bir nechta instansda bir xil holatga keltirish.
- CDC (Debezium) orqali DB o'zgarishlarini tartib bilan downstream'ga uzatish.
- Buxgalteriya/ledger yozuvlarini determinizmli tartibda qo'llash.
- Distributed cache invalidation'ni barcha node'larda bir xil ketma-ketlikda bajarish.

**Ehtiyot bo'ling:** Global tartib bitta partition/log'ni talab qilgani uchun gorizontal scaling'ni cheklaydi - tartib faqat haqiqatan kerak bo'lgan kalit chegarasida (per-aggregate) talab qilinishi kerak, aks holda throughput bo'g'ziga aylanadi. Partition sonini keyinroq oshirish mavjud kalitlarning partition'ini o'zgartiradi va o'tmishdagi tartib kafolatini buzadi, shuning uchun partitioning strategiyasini boshida to'g'ri loyihalash muhim.

## 28.25 Lambda arxitekturasi (Lambda Architecture)

**Tavsif:** Ma'lumot oqimini ikki parallel yo'lga bo'ladigan analitik arxitektura: batch layer butun tarixiy ma'lumot ustida aniq, qayta hisoblanadigan natijalarni (master dataset) tayyorlaydi, speed layer esa real vaqtda taxminiy natijani beradi, serving layer ikkisini birlashtirib so'rovga javob qaytaradi. Maqsad - kechikish va aniqlik o'rtasidagi kelishuvni hal qilish va batch qayta hisoblash orqali xatolarni tuzatish imkoniyatini saqlash.

**Spring'da qayerda uchraydi:** Spring'da bitta "Lambda" moduli yo'q - bu infratuzilma topologiyasi. Amalda Spring Boot 3.x ilovalari ikki yo'lni ham boshqaradi: speed layer uchun Spring Cloud Stream (Kafka binder) yoki Spring for Apache Kafka `@KafkaListener` bilan real vaqt agregatsiyasi, batch layer uchun Spring Batch (`Job`, `Step`, `ItemReader/ItemWriter`) yoki Spring Cloud Task bilan orkestrlanadigan Spark/Flink job'lari. Serving layer sifatida Spring Data Redis (tez, taxminiy natija) va Spring Data JDBC/JPA yoki Elasticsearch (aniq batch natijasi) ustida `@RestController` ikki manbani birlashtirib beradi. Spring Cloud Data Flow esa batch va stream pipeline'larini bitta joydan deploy va monitoring qilish uchun ishlatiladi.

**Qo'llanish keyslari:**
- Real vaqt dashboard'da taxminiy ko'rsatkich, kecha ertalab aniq moliyaviy hisobot.
- Fraud detection'da darhol signal va kechasi to'liq modelni qayta hisoblash.
- Web analytics: live visitor count va kunlik aniq unique user hisobi.
- IoT telemetriyasida darhol alert va tarixiy trend tahlili.
- Reklama hisob-kitobida tezkor taxminiy va oyma-oy aniq billing.

**Ehtiyot bo'ling:** Bir xil biznes logikani ikki marta (batch va stream kodida) yozish va sinxron ushlash - patternning asosiy narxi va eng katta xatolar manbasi. Zamonaviy stream engine'lar (Flink, Kafka Streams) exactly-once va reprocessing'ni o'zi qo'llagani uchun ko'p holatda Kappa arxitekturasi arzonroq; Lambda'ni faqat batch hisoblash haqiqatan boshqa texnologiyani talab qilganda tanlash kerak.

## 28.26 Kappa arxitekturasi (Kappa Architecture)

**Tavsif:** Lambda'ning soddalashtirilgan muqobili: yagona stream processing yo'li, batch layer yo'q. Barcha ma'lumot immutable, append-only log'ga (odatda Kafka) yoziladi va shu log yetarli uzoq saqlanadi; tarixiy qayta hisoblash kerak bo'lganda log boshidan qayta o'qiladi (replay) va yangi versiyadagi processor yangi natija jadvalini qurib, keyin trafik unga o'tadi. Shu bilan bitta kod bazasi, bitta semantika va kam operatsion murakkablik olinadi.

**Spring'da qayerda uchraydi:** Spring Cloud Stream'ning Kafka Streams binder'i (`spring-cloud-stream-binder-kafka-streams`) `Function<KStream<K,V>, KStream<K,V>>` bean'lari orqali deklarativ stream processor yozishga imkon beradi; `KTable` va interactive queries bilan materialized view to'g'ridan-to'g'ri ilovada saqlanadi. Spring for Apache Kafka'da `@KafkaListener` + consumer group offset'ini `KafkaConsumer.seekToBeginning` yoki `ConsumerSeekAware` bilan qayta o'rnatish replay'ni beradi; `ChainedKafkaTransactionManager` o'rniga Spring Boot 3.x'da `KafkaTransactionManager` va `isolation.level=read_committed` exactly-once semantikasini qo'llab-quvvatlaydi. CDC uchun Debezium Spring Boot bilan birga ishlatilib, DB o'zgarishlari shu yagona log'ga tushadi. Spring Boot Actuator metrikalari (`micrometer-core`) consumer lag monitoringi uchun zarur.

**Qo'llanish keyslari:**
- Event sourcing asosidagi tizimda read model'larni log replay orqali qayta qurish.
- Real vaqt agregatsiya (sessiya, oyna bo'yicha hisob) va tarixiy backfill'ni bir xil kod bilan bajarish.
- Yangi analitik ko'rsatkich qo'shilganda butun tarixni qayta hisoblab chiqish.
- Mikroservislar orasidagi integratsiyada Kafka'ni "haqiqat manbasi" sifatida ishlatish.
- Ma'lumot sxemasi o'zgarganda yangi versiyali projeksiyani parallel qurib, keyin almashtirish (blue/green projection).

**Ehtiyot bo'ling:** Replay'ga tayanish log'ni uzoq (ba'zan cheksiz) saqlashni talab qiladi - retention, compaction va storage xarajatini, shuningdek GDPR'ning "o'chirish huquqi" bilan immutable log ziddiyatini oldindan hal qilish kerak. Kattalashgan log'ni to'liq replay qilish soatlab davom etishi mumkin, shuning uchun snapshot mexanizmi va replay'ni ishlab chiqarish trafigidan ajratish shart.

## 28.27 Split brain (Split Brain)

**Tavsif:** Tarmoq bo'linishi (network partition) natijasida klaster ikki yoki undan ko'p mustaqil ishlayotgan bo'lakka ajralib, har biri o'zini yagona faol deb hisoblashi va ikkita leader/primary paydo bo'lishi. Natijada ikki tomonda ham yozuvlar qabul qilinadi va ular birlashganda ziddiyatli, ba'zan tiklab bo'lmaydigan ma'lumot holati yuzaga keladi. Himoya: kvorum (majority) talabi, fencing token / epoch raqami, STONITH (yiqilgan nodeni majburan o'chirish) va witness/arbiter node.

**Spring'da qayerda uchraydi:** Bu klaster va ma'lumotlar bazasi darajasidagi muammo; Spring ilovasi uning qurboni bo'ladi va to'g'ri sozlamalar bilan himoyalanadi. Leader election ishlatganda Spring Integration'ning `LeaderInitiator`i `OnRevokedEvent`ni ko'tarishi bilan ish darhol to'xtatilishi kerak - `@EventListener` ichida scheduler yoki Kafka container'ni (`MessageListenerContainer.stop()`) to'xtatish. ShedLock bilan `@SchedulerLock(lockAtMostFor = ...)` qo'yish lock egasi muzlab qolganda ikkinchi instansning ishga tushishini boshqaradi, lekin bu o'zi split brain xavfini keltiradi - shuning uchun yozuvlarni idempotent qilish yoki fencing token (epoch) ni DB'dagi conditional update bilan tekshirish kerak. Infratuzilmada Kafka'ning `min.insync.replicas` + `acks=all`, MongoDB'ning majority write concern (`WriteConcern.MAJORITY` Spring Data MongoDB'da `MongoTemplate.setWriteConcern(...)`), Hazelcast'ning split-brain protection sozlamalari ishlatiladi.

**Qo'llanish keyslari:**
- Klasterdagi scheduled job'ning ikki instansda bir vaqtda ishlab, dublikat to'lov yuborishini oldini olish.
- Ma'lumotlar bazasi failover'idan keyin eski primary'ni yozuvdan uzish (fencing).
- Ikki data center orasidagi aloqa uzilganda qaysi tomon yozuvni davom ettirishini aniqlash.
- Kubernetes'da pod network'dan uzilganda `Lease` muddati tugashi orqali leader'ni almashtirish.
- Distributed cache (Hazelcast/Ignite) klasteri bo'linib, keyin merge bo'lganda konflikt siyosatini belgilash.

**Ehtiyot bo'ling:** Faqat timeout'ga asoslangan leader detection hech qachon xavfsiz emas - GC pause yoki uzun STW ilovani "o'lik" deb ko'rsatib, ikki egalikka olib keladi, shuning uchun har bir yozuvda monoton o'suvchi fencing token tekshirilishi kerak. Juft sonli node'li klaster yoki witness'siz ikki-DC konfiguratsiyasi split brain uchun eng xavfli topologiya; availability'ni saqlash uchun kvorumni o'chirib qo'yish esa ma'lumot yo'qolishini kafolatlaydi.

## 28.28 Gibrid logik soat / soat siljishi (Hybrid Logical Clock / Clock Skew)

**Tavsif:** Jismoniy soat (wall clock) va logik soat (Lamport clock) ni birlashtirgan timestamp mexanizmi: HLC qiymati haqiqiy vaqtga yaqin bo'ladi, lekin causal tartibni ham saqlaydi va node'lar soatlari farq qilganda ham monoton o'sadi. Bu clock skew sababli kelib chiqadigan muammolarni - last-write-wins da yangi yozuvning eski timestamp bilan "yutib ketilishi", tartibsiz event log, noto'g'ri TTL - hal qiladi. CockroachDB, YugabyteDB va MongoDB (cluster time) shu yondashuvni ishlatadi.

**Spring'da qayerda uchraydi:** Spring'da HLC implementatsiyasi yo'q; ilova darajasida `java.time.Clock` ni bean sifatida inject qilish (`Clock.systemUTC()`) va `Instant.now(clock)` ishlatish test qilinadigan, bir manbadan olinadigan vaqtni beradi - bu minimal gigiyena. Spring Data JPA'ning `@CreatedDate`/`@LastModifiedDate` (`AuditingEntityListener`, `@EnableJpaAuditing`) va `DateTimeProvider` bean'i ilova serverining soatiga tayanadi, shuning uchun ko'p instansli muhitda ularni tartib manbai sifatida ishlatish xato; buning o'rniga DB'ning `CURRENT_TIMESTAMP` yoki sequence'ini yoki monoton versiya raqamini (`@Version`) ishlatish to'g'ri. Kafka'da `ConsumerRecord.timestamp()` producer soatiga (`CreateTime`) bog'liq bo'lgani uchun tartib uchun offset ishlatiladi. Observability tomonda Micrometer Tracing (Spring Boot 3.x) span'larni trace ID bilan bog'laydi, lekin turli xostlardagi span vaqtlari skew tufayli "negativ davomiylik" ko'rsatishi mumkin - shuning uchun NTP/chrony sinxronizatsiyasi infratuzilma talabi sifatida qo'yiladi.

**Qo'llanish keyslari:**
- Multi-region yozuvlarda last-write-wins konfliktini to'g'ri hal qilish.
- Event sourcing'da causal tartibni saqlagan holda inson o'qiy oladigan timestamp berish.
- Distributed tracing va log korrelyatsiyasida xostlar orasidagi vaqt farqini tushuntirish.
- Token/sessiya muddati (JWT `exp`) ni tekshirishda clock skew uchun tolerance (leeway) qo'yish.
- Idempotency va deduplikatsiya oynasini vaqtga tayanmasdan, versiyaga tayanib belgilash.

**Ehtiyot bo'ling:** Biznes qarorini (kim birinchi, kim g'olib) turli serverlarda olingan `System.currentTimeMillis()` ga qurish - klassik va juda qimmat xato; tartib kerak bo'lsa yagona manbadan (DB sequence, Kafka offset, konsensus log) olingan monoton raqam ishlatilishi kerak. NTP soatni orqaga ham suradi, shuning uchun o'tgan vaqt (davomiylik) o'lchash uchun `System.nanoTime()` yoki `Micrometer Timer` ishlatish, `Instant.now()` emas.

---

[&larr; 27. Monolitdan microservice'ga migratsiya patternlari](27-monolitdan-microservicega-migratsiya.md) · [Mundarija](README.md) · [29. Kubernetes va cloud-native patternlar &rarr;](29-kubernetes-va-cloud-native-patternlar.md)
