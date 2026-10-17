<!-- doc: architect | chapter: 32 | part: V. Atrof ekotizim: operatsion haqiqat -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 32. Tarmoq, timeout va integratsiya haqiqati (Network, Timeouts and Integration)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [32.1 Tarmoq ishonchsiz: ulanish uzilishi, paket yo'qolishi, yarim ochiq ulanish](#321-tarmoq-ishonchsiz-ulanish-uzilishi-paket-yoqolishi-yarim-ochiq-ulanish)
- [32.2 Timeout turlari: ulanish, o'qish, yozish, umumiy so'rov, va ularning farqi](#322-timeout-turlari-ulanish-oqish-yozish-umumiy-sorov-va-ularning-farqi)
- [32.3 Timeout qiymatini qanday tanlash: yuqori qatlam quyi qatlamdan uzunroq bo'lsin](#323-timeout-qiymatini-qanday-tanlash-yuqori-qatlam-quyi-qatlamdan-uzunroq-bolsin)
- [32.4 Timeout byudjeti: zanjirdagi har bir chaqiruvga vaqt taqsimlash](#324-timeout-byudjeti-zanjirdagi-har-bir-chaqiruvga-vaqt-taqsimlash)
- [32.5 Ulanish hovuzi (HTTP client va JDBC): kattalik, kutish navbati, keep-alive](#325-ulanish-hovuzi-http-client-va-jdbc-kattalik-kutish-navbati-keep-alive)
- [32.6 DNS: TTL, keshlash va JVM dagi DNS kesh sozlamalari](#326-dns-ttl-keshlash-va-jvm-dagi-dns-kesh-sozlamalari)
- [32.7 TLS: qo'l siqish narxi, sertifikat muddati, ichki CA, qayta ishlatish](#327-tls-qol-siqish-narxi-sertifikat-muddati-ichki-ca-qayta-ishlatish)
- [32.8 Qayta urinish siyosati: faqat idempotent chaqiruvda, eksponensial kechikish va jitter](#328-qayta-urinish-siyosati-faqat-idempotent-chaqiruvda-eksponensial-kechikish-va-jitter)
- [32.9 Orqaga bosim (backpressure) va navbat chuqurligini cheklash](#329-orqaga-bosim-backpressure-va-navbat-chuqurligini-cheklash)
- [32.10 Tashqi servis bilan shartnoma: versiyalash, buzilmaydigan o'zgarish, ogohlantirish](#3210-tashqi-servis-bilan-shartnoma-versiyalash-buzilmaydigan-ozgarish-ogohlantirish)
- [32.11 Yuk tarqatuvchi va proxy sozlamalari: idle timeout nomuvofiqligi tuzog'i](#3211-yuk-tarqatuvchi-va-proxy-sozlamalari-idle-timeout-nomuvofiqligi-tuzogi)
- [32.12 Integratsiyani sinash: tashqi servis sekinlashganda nima bo'ladi](#3212-integratsiyani-sinash-tashqi-servis-sekinlashganda-nima-boladi)
- [32.13 Soat ishonchsiz: monoton soat, clock skew va TTL ga tayanmaslik](#3213-soat-ishonchsiz-monoton-soat-clock-skew-va-ttl-ga-tayanmaslik)
- [32.14 Amalda qo'llash](#3214-amalda-qollash)

</details>



Tarmoq orqali chaqiruv lokal metod chaqiruvi emas, lekin kodda ikkisi bir xil ko'rinadi. Arxitektorning asosiy vazifasi shu farqni kodda ko'rinadigan qilish: har bir tashqi chaqiruvda vaqt chegarasi, qayta urinish qoidasi va to'xtash sharti bo'lsin. Quyida mexanika va raqamlar bor: TCP nima qiladi, timeout qanday ishlaydi, pool qancha bo'lishi kerak, DNS va TLS qayerda tishlaydi. Resilience pattern katalogi (circuit breaker, bulkhead, outbox) dizayn [patternlar hujjatida](../patterns/README.md), bu yerda faqat sozlash va qaror.

## 32.1 Tarmoq ishonchsiz: ulanish uzilishi, paket yo'qolishi, yarim ochiq ulanish

TCP ishonchli yetkazishni kafolatlaydi, lekin faqat ulanish tirik bo'lsa. Ikki xil uzilish bor va ularning oqibati butunlay boshqa. Birinchisi toza uzilish: peer FIN yoki RST yuboradi, socket darhol xabar beradi, `read()` bir necha mikrosekundda xato qaytaradi. Ikkinchisi yarim ochiq (half-open) ulanish: peer o'lgan, lekin hech qanday paket yubormagan. Bu `kill -9` da, VM o'chib qolganda, NAT jadvalidan yozuv tushib ketganda yoki firewall paketni jim tashlab yuborganda sodir bo'ladi.

Yarim ochiq ulanish eng qimmat holat, chunki JVM uning o'lganini bilmaydi. Linux `tcp_retries2` default 15 ga teng, va yadro hujjati buni "hypothetical timeout of 924.6 seconds" deb atab, muhim izoh qo'shadi: bu qiymat haqiqiy timeout uchun PASTKI chegara, ya'ni amalda kutish uzunroq bo'lishi mumkin. Shu 15 daqiqa davomida thread `read()` da osilib turadi. `SO_KEEPALIVE` yoqilgan bo'lsa ham default `tcp_keepalive_time` 7200 sekund, ya'ni birinchi probe 2 soatdan keyin ketadi. Xulosa: application darajasidagi read timeout yagona ishonchli himoya, OS sozlamalariga tayanib bo'lmaydi.

```bash
# Yarim ochiq ulanish belgisi: Send-Q o'smoqda, lekin ACK kelmayapti
ss -tin dst 10.20.0.15 | head -20

# Dead peer ni TCP qancha kutadi: 15 ta retry, pastki chegara 924.6 s
cat /proc/sys/net/ipv4/tcp_retries2

# Keepalive birinchi probe gacha jimlik: default 7200 sekund
cat /proc/sys/net/ipv4/tcp_keepalive_time

# Blackhole ni imitatsiya qilish: RST emas, paketni jim tashlash
sudo iptables -A OUTPUT -d 10.20.0.15 -p tcp --dport 8443 -j DROP
```

## 32.2 Timeout turlari: ulanish, o'qish, yozish, umumiy so'rov, va ularning farqi

Kutilmagan hodisalarning yarmi "timeout qo'ydim" deb o'ylab, aslida boshqa timeout ni qo'yishdan kelib chiqadi. Beshta alohida chegara bor va ular bir-birini almashtirmaydi.

Connect timeout: TCP handshake uchun. Bu faqat SYN dan SYN-ACK gacha bo'lgan vaqt, odatda bir RTT. Data-center ichida 1 ms, region oralig'ida 30 ms. Shuning uchun connect timeout 1 dan 2 sekundgacha yetarli, 30 sekund bu xato.

Connection request timeout yoki pool acquire timeout: hovuzdan bo'sh ulanish kutish vaqti. Bu eng ko'p yashiriladigan latency. Reactor Netty da `pendingAcquireTimeout` default 45 sekund, Apache HttpClient 5 da `connectionRequestTimeout` default ham katta. Servis yuklanganda butun kechikish shu yerda to'planadi.

Socket yoki read timeout: ikki ketma-ket bayt oralig'idagi jimlik. Bu umumiy so'rov vaqti EMAS. Serverda sekin oqim bo'lsa, masalan har 4 sekundda bir bayt kelsa, 5 sekundlik read timeout hech qachon ishlamaydi va chaqiruv cheksiz davom etadi.

Response timeout: so'rov yuborilgandan birinchi javob baytigacha. Write timeout: kernel send buffer to'lib, yozish bloklanganda. Umumiy so'rov timeout: butun operatsiya uchun qattiq deadline. Faqat shu oxirgisi haqiqiy kafolat beradi, va aynan shu yerda eng ko'p tarqalgan yanglishish yashiradi.

`HttpRequest.timeout()` ni "butun so'rov uchun deadline" deb o'qish noto'g'ri. JDK ning o'z kodida taymer HAR URINISH uchun alohida ro'yxatga olinadi (ichki retry va redirect yangi taymer qo'yadi), va u javob SARLAVHALARI olinganda bekor qilinadi. Body shundan keyin, taymersiz o'qiladi. Ya'ni sekin tomchilovchi javob tanasi bu timeout bilan cheklanmaydi, va zanjirdagi urinishlar yig'indisi ham cheklanmaydi.

```java
// Java HttpClient: `timeout` har urinish uchun va faqat javob
// sarlavhalarigacha. Umumiy deadline alohida qo'yiladi.
HttpClient client = HttpClient.newBuilder()
        .connectTimeout(Duration.ofSeconds(2))   // faqat TCP handshake
        .version(HttpClient.Version.HTTP_2)
        .build();

HttpRequest req = HttpRequest.newBuilder(URI.create(baseUrl + "/payments"))
        // Bir urinishning sarlavhagacha chegarasi, body va retry emas
        .timeout(Duration.ofMillis(1200))
        .header("Idempotency-Key", paymentId.toString())
        .POST(HttpRequest.BodyPublishers.ofString(body))
        .build();

// Haqiqiy umumiy deadline: body o'qishni va ichki urinishlarni ham
// qamrab oladi. Buni so'rov darajasida qo'yish kerak.
HttpResponse<String> res = client
        .sendAsync(req, HttpResponse.BodyHandlers.ofString())
        .orTimeout(1500, TimeUnit.MILLISECONDS)
        .join();
```

```properties
# Spring Boot 3.4-3.5 markazlashgan HTTP client sozlamasi
# (Boot 4 da: spring.http.clients.imperative.factory, spring.http.clients.*)
spring.http.client.factory=jdk
spring.http.client.connect-timeout=2s
spring.http.client.read-timeout=1200ms

# Tomcat tomoni: osilgan ulanishni ushlab turmaslik
server.tomcat.connection-timeout=5s
```

Spring Boot 4.0 da `spring.http.client.*` kalitlari deprecated: ular hali ulanadi va ogohlantirish beradi, o'rnini `spring.http.clients.connect-timeout`, `spring.http.clients.read-timeout` va `spring.http.clients.imperative.factory` egallaydi ([spring-boot v4.0.0, http-client metadata](https://github.com/spring-projects/spring-boot/blob/v4.0.0/module/spring-boot-http-client/src/main/resources/META-INF/additional-spring-configuration-metadata.json)).

## 32.3 Timeout qiymatini qanday tanlash: yuqori qatlam quyi qatlamdan uzunroq bo'lsin

Timeout qiymati o'rtacha latency dan emas, taqsimot dumidan chiqadi. To'lov servisiga misol: p50 40 ms, p95 120 ms, p99 180 ms, p99.9 600 ms. Read timeout ni p99.9 ga taxminan 1.5 koeffitsiyent bilan olasiz, ya'ni 900 ms dan 1 sekundgacha. Buni 30 sekund qilib qo'yish degani: bitta sekin dependency butun thread pool ni bloklaydi va o'zingiz ham o'lasiz.

Qatlamlar tartibi qattiq qoida. Tashqi qatlam ichki qatlamdan uzunroq bo'lishi kerak, aks holda ichki chaqiruv tugamasdan tashqi tomon bekor qiladi va siz natijasi bor ishni tashlab yuborasiz. Ayni paytda tashqi qatlam ichki qatlamlar yig'indisidan sezilarli kattaroq bo'lmasligi kerak, aks holda deadline ma'nosini yo'qotadi. Amalda qadam sifatida 100 dan 300 ms gacha zahira qo'yiladi.

Ikkinchi qoida: statement timeout ni ilovada emas, bazada ham qo'ying. Ilova timeout da thread ni qo'yib yuboradi, lekin PostgreSQL so'rovni davom ettiradi va CPU ni yeydi. JDBC `socketTimeout` ulanishni buzadi, `statement_timeout` esa so'rovni haqiqatda to'xtatadi.

```sql
-- Har bir rolga o'z chegarasi: hisobot OLTP ni cho'ktirmaydi
ALTER ROLE app_rw  SET statement_timeout = '3s';
ALTER ROLE app_rw  SET lock_timeout = '1s';
ALTER ROLE app_rw  SET idle_in_transaction_session_timeout = '10s';
ALTER ROLE report_ro SET statement_timeout = '45s';

-- Tekshirish: joriy sessiyada nima o'rnatilgan
SELECT name, setting FROM pg_settings
WHERE name IN ('statement_timeout','lock_timeout',
               'idle_in_transaction_session_timeout');
```

## 32.4 Timeout byudjeti: zanjirdagi har bir chaqiruvga vaqt taqsimlash

Buyurtma yaratish API si uchun SLO 2000 ms bo'lsa, bu butun zanjir uchun byudjet. Byudjetni bo'lib chiqasiz: gateway 1900 ms, order service 1700 ms, uning ichida ombor qoldig'ini tekshirish 400 ms, to'lov 800 ms, baza yozuvlari 200 ms, qolgani zahira. Har bir qism o'z chegarasini biladi va umumiy summa SLO dan oshmaydi.

Statik qiymat yetarli emas, chunki birinchi chaqiruv 700 ms yesa, keyingi chaqiruvga 800 ms berish mantiqsiz. Shuning uchun deadline uzatiladi, timeout emas. Chaqiruvchi "menda yana 480 ms qoldi" deb aytadi, chaqirilgan tomon shu chegaradan oshmaydi va qolgan vaqt yetmasa ishni boshlamasdan rad etadi. Bu bitta tarmoq chaqiruvini va bitta DB ulanishini tejaydi.

```java
// Deadline ni so'rov kontekstida olib yuring, millisekundda header orqali uzating
public record Deadline(long epochMillis) {
    static Deadline in(Duration d) {
        return new Deadline(System.currentTimeMillis() + d.toMillis());
    }
    Duration remaining() {
        return Duration.ofMillis(Math.max(0, epochMillis - System.currentTimeMillis()));
    }
    // Zahira: tarmoq va serializatsiya uchun 50 ms qoldirmasak, javob kech qoladi
    Duration budgetFor(Duration ask) {
        long left = remaining().toMillis() - 50;
        if (left <= 0) throw new DeadlineExceededException("byudjet tugadi");
        return Duration.ofMillis(Math.min(ask.toMillis(), left));
    }
}
```

| oddiy yondashuv | arxitektor yondashuvi |
| --- | --- |
| Hamma joyda default timeout, ko'pincha 30 yoki 60 sekund | Har bir chaqiruvga p99.9 asosida hisoblangan qiymat, 1 sekund atrofida |
| Faqat connect va read timeout qo'yiladi | Pool acquire, connect, read va umumiy deadline alohida; JDK klientida umumiy deadline so'rov darajasida qo'yiladi, `HttpRequest.timeout` bilan emas |
| Har bir servis o'z timeout ini mustaqil tanlaydi | Zanjir uchun yagona byudjet, qatlamlar bo'yicha taqsimlangan |
| Timeout statik konstanta | Deadline so'rov bilan uzatiladi, qolgan vaqtga qarab qisqaradi |
| Xato bo'lsa darhol 3 marta qayta uriniladi | Faqat idempotent chaqiruvda, jitter bilan, retry budjeti ostida |
| Pool kattaligi "ko'proq yaxshi" tamoyilida tanlanadi | Little qonuni bilan hisoblanadi, DB max_connections ga sig'adi |
| LB va ilova timeout lari bir-biridan xabarsiz | Tartib qattiq: client idle < LB idle < server keep-alive |
| Baza so'rovi faqat ilova tomonidan cheklanadi | `statement_timeout` rol darajasida, ilovadan mustaqil |
| Tashqi servis sekinlashishi hech qachon sinalmagan | Latency va blackhole inyeksiyasi relizdan oldin o'lchanadi |
| DNS va sertifikat "ishlayapti" deb ishoniladi | TTL, cache va amal qilish muddati monitoring da |

## 32.5 Ulanish hovuzi (HTTP client va JDBC): kattalik, kutish navbati, keep-alive

Pool kattaligini taxmin bilan emas, Little qonuni bilan tanlaysiz: zarur ulanish soni teng throughput ni latency ga ko'paytirganga. Buyurtma servisi 300 rps bersa va bitta DB so'rovi 15 ms ketsa, kerak bo'lgani 300 * 0.015 = 4.5 ulanish. Shuning uchun HikariCP uchun 10 ta ulanish ko'p hollarda yetarli, 100 ta esa zarar. Katta pool kutish navbatini yashiradi va PostgreSQL da har bir ulanish alohida backend process bo'lgani uchun xotira va context switch ni oshiradi.

PostgreSQL `max_connections` 200 bo'lsa va sizda 8 ta pod, har birida 10 ta ulanish bo'lsa, bu 80 ta, ustiga migratsiya, hisobot va admin sessiyalari qo'shiladi. Pod soni avtomatik o'sadigan bo'lsa, shu arifmetikani oldindan qiling yoki PgBouncer ni transaction pooling rejimida qo'yib, ilova va baza sonini ajratib oling.

`maxLifetime` eng ko'p e'tibordan chetda qoladigan parametr. Default 30 daqiqa va u baza yoki LB ulanishni jim o'ldirish vaqtidan KICHIK bo'lishi shart, aks holda pool allaqachon o'lgan ulanishni beradi va siz tasodifiy xatolarni ko'rasiz.

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10          # Little qonuni: 300 rps * 15 ms
      # DIQQAT: `idle-timeout` faqat `minimum-idle` `maximum-pool-size`
      # dan KICHIK bo'lganda ishlaydi. Ikkisi teng bo'lsa (pastdagi
      # holat) pool hech qachon qisqarmaydi va `idle-timeout` qatori
      # hech narsa qilmaydi. Bu ongli tanlov: biz isinish pauzasini
      # yo'q qilish uchun poolni to'liq ushlab turamiz.
      minimum-idle: 10               # bir xil qiymat, isinish pauzasi bo'lmasin
      connection-timeout: 2000       # navbatda kutish, 30 s emas
      validation-timeout: 1000
      idle-timeout: 600000           # default qiymat, bu yerda ta'sirsiz
      max-lifetime: 1500000          # 25 daqiqa, LB/PgBouncer chegarasidan kam
      keepalive-time: 120000         # 2 daqiqada bir probe, yarim ochiq ulanishga qarshi
      data-source-properties:
        socketTimeout: 5             # sekund, statement_timeout dan uzunroq
        tcpKeepAlive: true
```

```java
// Reactor Netty: default pendingAcquireTimeout 45 s, bu yashirin latency manbai
ConnectionProvider provider = ConnectionProvider.builder("payments")
        .maxConnections(50)
        .pendingAcquireTimeout(Duration.ofMillis(500)) // tez rad et
        .pendingAcquireMaxCount(100)                   // navbat chuqurligi cheklangan
        .maxIdleTime(Duration.ofSeconds(20))           // LB idle timeout dan kam
        .maxLifeTime(Duration.ofMinutes(5))            // DNS o'zgarishini ko'rish uchun
        .evictInBackground(Duration.ofSeconds(30))
        .build();
```

## 32.6 DNS: TTL, keshlash va JVM dagi DNS kesh sozlamalari

JVM o'z DNS keshini yuritadi. `InetAddress` uchun ijobiy javob keshi default 30 sekund, salbiy javob keshi 10 sekund atrofida. Bu qiymatlar `java.security` fayldagi `networkaddress.cache.ttl` va `networkaddress.cache.negative.ttl` orqali boshqariladi. Eng xavfli sozlama `networkaddress.cache.ttl=-1`, ya'ni abadiy kesh: failover da IP o'zgaradi, lekin JVM eski manzilga urinishda davom etadi va faqat restart yordam beradi.

Ikkinchi qatlam kesh connection pool ning o'zi. Pool ulanishni ushlab turganda DNS o'zgarishi hech qanday ta'sir qilmaydi, chunki yangi rezolyutsiya bo'lmaydi. Shu sababli `maxLifeTime` ni 5 dan 30 daqiqagacha qo'yish kerak: u IP rotatsiyasiga yo'l beradi.

Kubernetes da uchinchi tuzoq `ndots`. Default `ndots:5` bo'lgani uchun to'liq bo'lmagan nom har safar bir necha qidiruv domeni bilan sinaladi, bu har bir rezolyutsiyaga qo'shimcha so'rov va kechikish qo'shadi. Tashqi hostlarni nuqta bilan tugaydigan to'liq nom sifatida yozish shu ortiqcha urinishlarni yo'qotadi.

```bash
# JVM DNS kesh TTL ni ko'rish (abadiy kesh -1 bo'lmasligi kerak)
grep -n 'networkaddress.cache' "$JAVA_HOME/conf/security/java.security"

# DIQQAT: `-Dnetworkaddress.cache.ttl=...` ISHLAMAYDI. JVM bu nomni
# system property emas, XAVFSIZLIK property si deb o'qiydi, ya'ni
# `java.security` faylidan yoki `Security.setProperty` dan. Buyruq
# qatorida berilgani jimgina e'tiborsiz qoladi va TTL default 30 s
# qoladi. Uchta haqiqiy yo'l bor:

# 1) java.security faylini tahrirlash yoki o'z faylini qo'shish
java -Djava.security.properties=/app/dns.security -jar order-service.jar

# 2) Klass yuklanishidan oldin kodda qo'yish
#    java.security.Security.setProperty("networkaddress.cache.ttl", "30");

# 3) Ichki fallback nomi (JDK ning o'z nomi, barqarorligi kafolatlanmagan)
java -Dsun.net.inetaddr.ttl=30 \
     -Dsun.net.inetaddr.negative.ttl=5 \
     -jar order-service.jar

# Kubernetes ichida ortiqcha qidiruv domenlarini ko'rish
cat /etc/resolv.conf   # ndots:5 bo'lsa, FQDN ni nuqta bilan yozing
```

## 32.7 TLS: qo'l siqish narxi, sertifikat muddati, ichki CA, qayta ishlatish

TLS 1.3 to'liq handshake bitta RTT, TLS 1.2 ikkita RTT oladi. Region oralig'ida RTT 30 ms bo'lsa, bu 30 dan 60 ms gacha sof kechikish, ustiga asimmetrik imzo uchun protsessor vaqti, RSA 2048 da taxminan 1 dan 2 ms gacha, ECDSA P-256 da sezilarli kamroq. Demak har so'rovda yangi ulanish ochish p99 ni ikki baravar oshirishi mumkin. Bu yerda optimizatsiya aniq: keep-alive va ulanish hovuzini to'g'ri sozlash, session resumption ni yoqish.

Sertifikat muddati ishlab chiqarishdagi eng oldindan ko'rinadigan, lekin eng ko'p qaytariladigan avariya. Ichki CA ishlatilsa, truststore da CA sertifikati bo'lishi va uning muddati ham kuzatilishi kerak. Spring Boot 3.1 dan boshlab SSL bundle mavzusi markazlashgan, fayl o'zgarganda qayta yuklash esa 3.2 da qo'shilgan (`reload-on-update`), va u rotatsiyani restart siz qiladi. Ikki versiyani aralashtirmaslik kerak: 3.1 da bundle bor, avtomatik qayta yuklash yo'q. Hostname tekshiruvini o'chirish esa hech qachon yechim emas, u shunchaki muammoni kelasi yilga suradi.

```bash
# Sertifikat muddati va handshake vaqtini bir yo'la o'lchash
echo | openssl s_client -connect payments.internal:8443 -servername payments.internal \
  2>/dev/null | openssl x509 -noout -subject -issuer -dates

# 30 kundan kam qolganini CI da tekshirish
echo | openssl s_client -connect payments.internal:8443 2>/dev/null \
  | openssl x509 -noout -checkend 2592000 || echo "SERTIFIKAT TEZDA TUGAYDI"

# Handshake narxi: har bir urinishda sarflangan vaqt
curl -sS -o /dev/null -w 'tcp=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer}\n' \
  https://payments.internal:8443/health
```

## 32.8 Qayta urinish siyosati: faqat idempotent chaqiruvda, eksponensial kechikish va jitter

Qayta urinish faqat ikki shart bajarilganda xavfsiz. Birinchisi: operatsiya idempotent, ya'ni ikki marta bajarilsa natija bir xil. To'lovni yaratish o'z-o'zidan idempotent emas, u faqat idempotency key bilan shunday bo'ladi. Ikkinchisi: xato turi qayta urinishga arzaydi. Connect timeout da so'rov serverga yetmagan, demak xavfsiz. Read timeout da so'rov yetgan bo'lishi mumkin va javob yo'qolgan, demak yozish operatsiyasi uchun xavfli.

Kechikish eksponensial bo'lishi va albatta jitter bilan bo'lishi kerak. Jitter bo'lmasa barcha klientlar bir vaqtda qayta uradi va servis tiklanishga ulgurmaydi. Amalda ishlaydigan formula "full jitter": kutish vaqti 0 dan `min(cap, base * 2^urinish)` oralig'idagi tasodifiy son.

Eng katta xavf retry amplifikatsiyasi. Uch qatlamning har biri 3 urinish qilsa, bitta foydalanuvchi so'rovi eng chuqur servisga 27 chaqiruv bo'lib tushadi. Shuning uchun qayta urinish bitta qatlamda, odatda chetki qatlamda bo'ladi va retry ulushi umumiy trafikning 10 foizidan oshmasligi kuzatiladi.

```java
// Full jitter: urinishlar bir vaqtda to'planib qolmaydi
private Duration backoff(int attempt) {
    long base = 50;                                   // ms
    long cap  = 2_000;                                // yuqori chegara
    long expo = Math.min(cap, base * (1L << Math.min(attempt, 10)));
    return Duration.ofMillis(ThreadLocalRandom.current().nextLong(expo + 1));
}

// Qayta urinishga arzaydimi: yozish operatsiyasida read timeout xavfli.
// Tartib muhim: HttpConnectTimeoutException HttpTimeoutException ning
// BOLASI, shuning uchun u avval tekshiriladi. Teskari tartibda connect
// timeout ham "natija noaniq" deb tasniflanib, POST qayta urinmaydi.
private boolean retryable(Exception e, String method, Integer status) {
    // Ulanish o'rnatilmagan: so'rov serverga yetmagan, qayta urinish xavfsiz
    if (e instanceof HttpConnectTimeoutException) return true;
    if (e instanceof ConnectException) return true;
    // Javob kelmadi: so'rov bajarilgan bo'lishi mumkin, natija noaniq
    if (e instanceof HttpTimeoutException) return idempotent(method);
    return status != null && (status == 429 || status == 503 || status == 504);
}

// `isIdempotent()` JDK API si emas, uni o'zingiz yozasiz. JDK ning
// ichki qoidasi faqat GET va HEAD ni idempotent deb hisoblaydi; PUT va
// DELETE HTTP bo'yicha idempotent, lekin bu sizning endpointingiz
// haqiqatan shunday ekaniga bog'liq. POST faqat idempotency key bilan.
private boolean idempotent(String method) {
    return switch (method) {
        case "GET", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE" -> true;
        default -> false;
    };
}
```

Retry ni hisoblashda yana bitta qatlam borligini bilish kerak: JDK
klientining o'zi ham ulanish xatolarida qayta uriniladi (jami urinishlar
soni beshta, va bu xulqni `jdk.httpclient.disableRetryConnect` bilan
o'chirish mumkin). Demak "men bitta urinish qildim" degan taxmin
noto'g'ri bo'lishi mumkin, va quyidagi ko'paytirish hisobi ham JDK ning
ichki urinishlarini hisobga olmaydi.

Mavzuning to'liq yozuvi [idempotency](../patterns/07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 32.9 Orqaga bosim (backpressure) va navbat chuqurligini cheklash

Cheksiz navbat muammoni yo'qotmaydi, uni kechiktiradi va yomonlashtiradi. Navbatda 30 sekund yotgan so'rov allaqachon mijoz uchun o'lik, lekin u hali ham thread, ulanish va CPU yeydi. Tomcat da `max-threads` default 200, `accept-count` default 100. Bu degani og'ir paytda 300 ta so'rov tizim ichida bo'ladi va har biri deadline ni yemoqda.

To'g'ri yondashuv ikki qismdan iborat. Birinchisi: bir vaqtdagi chaqiruvlar sonini cheklash. Yana Little qonuni, sekin dependency uchun ruxsat soni teng maqsadli rps ni p99 latency ga ko'paytirganga. 50 rps va 200 ms bo'lsa 10 ta ruxsat yetarli. Ikkinchisi: navbatdan olinganda deadline ni tekshirish. Vaqti tugagan ishni bajarmasdan tashlash bepul tezlik beradi.

```java
// Navbatdan olgandan keyin deadline ni tekshirish: o'lik ishni bajarmaymiz
Semaphore permits = new Semaphore(10);     // 50 rps * 0.2 s

Optional<Quote> fetchQuote(Deadline dl) throws InterruptedException {
    Duration wait = dl.remaining();
    if (!permits.tryAcquire(wait.toMillis(), TimeUnit.MILLISECONDS)) {
        rejected.increment();              // tez rad etish, 503 va Retry-After
        return Optional.empty();
    }
    try {
        if (dl.remaining().toMillis() < 100) return Optional.empty(); // kech qoldi
        return Optional.of(client.quote(dl.budgetFor(Duration.ofMillis(800))));
    } finally {
        permits.release();
    }
}
```

## 32.10 Tashqi servis bilan shartnoma: versiyalash, buzilmaydigan o'zgarish, ogohlantirish

Integratsiya shartnomasi kod emas, kelishuv. Buzilmaydigan o'zgarishlar ro'yxati qisqa: yangi majburiy bo'lmagan maydon qo'shish, yangi endpoint qo'shish, xato matnini aniqlashtirish. Buziladigan o'zgarishlar: maydonni olib tashlash, nomini o'zgartirish, turini toraytirish, majburiy qilish, enum qiymati semantikasini o'zgartirish, default xatti-harakatni almashtirish.

Iste'molchi tomonida himoya "tolerant reader" tamoyili: notanish maydonni e'tiborsiz qoldirish va notanish enum qiymatini xatoga aylantirmaslik. Ombor servisi `RESERVED` holatini qo'shsa, sizning buyurtma servisi deserializatsiyada yiqilmasligi kerak. Ayni paytda sizga haqiqatan kerak bo'lgan maydonlar uchun tekshiruv qattiq bo'lsin, aks holda `null` ichkariga sizib kiradi.

Versiyalash yo'li muhim emas, barqarorligi muhim. URI da `/v1` ko'rinadi va keshga qulay, media type versiyalash nozikroq. Muhimi: eski versiya o'chirilishidan oldin ogohlantirish oynasi bo'lsin, odatda `Deprecation` va `Sunset` sarlavhalari bilan va kamida 90 kun. Shartnoma avtomatik tekshiruvi uchun [testlash qo'llanmasidagi](../testing/README.md) contract testing bo'limiga qara.

```java
@Configuration
class JsonContractConfig {
    @Bean
    // Spring Boot 3.x uchun. Boot 4.0 da bu interfeys deprecated
    // (4.2.0 da olib tashlanadi) va uning o'rnini Jackson 3 egallaydi,
    // shuning uchun Boot 4 ga ko'tarilishda bu bean qayta yoziladi.
    Jackson2ObjectMapperBuilderCustomizer tolerantReader() {
        return b -> b
            // Yetkazib beruvchi yangi maydon qo'shsa yiqilmaymiz
            .featuresToDisable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
            // Notanish enum qiymati default ga tushadi, xatoga emas
            .featuresToEnable(DeserializationFeature.READ_UNKNOWN_ENUM_VALUES_USING_DEFAULT_VALUE);
    }
}

enum StockStatus {
    AVAILABLE, OUT_OF_STOCK,
    @JsonEnumDefaultValue UNKNOWN   // kelasi versiyadagi yangi holatlar uchun
}
```

## 32.11 Yuk tarqatuvchi va proxy sozlamalari: idle timeout nomuvofiqligi tuzog'i

Eng ko'p uchraydigan "tushunarsiz 502" sababi idle timeout poygasi. Mijoz pool da ulanishni 60 sekund bo'sh ushlaydi, LB ham 60 sekundda bo'sh ulanishni yopadi. Mijoz 59.9 sekundda so'rov yuboradi, LB ayni o'sha payt FIN yuboradi, natijada so'rov yo'qolgan ulanishga tushadi. Bu tasodifiy, past chastotali va qidirish qiyin xato.

Qoida oddiy va qattiq: mijozning bo'sh ulanish vaqti LB dan kichik, LB esa backend keep-alive dan kichik bo'lsin. Masalan client pool idle 20 sekund, LB idle 60 sekund, Tomcat keep-alive 75 sekund. Shu tartib buzilsa, ulanishni har safar faqat yopuvchi tomon biladi va boshqa tomon kech xabar topadi.

Ikkinchi tuzoq proxy ning o'qish timeout i. Reverse proxy larda bu odatda 60 sekund atrofida. Ombor qoldig'i bo'yicha og'ir hisobot 90 sekund ishlasa, proxy mijozga 504 beradi, lekin backend so'rovni davom ettiradi va resurs yeydi. Bu yerda yechim timeout ni oshirish emas, uzoq operatsiyani asinxron qilish va holat so'rash endpoint i bilan berish.

```properties
# Tartib: client idle (20s) < LB idle (60s) < server keep-alive (75s)
server.tomcat.keep-alive-timeout=75s
server.tomcat.max-keep-alive-requests=200
server.tomcat.connection-timeout=5s
server.tomcat.threads.max=200
server.tomcat.accept-count=50

# Hikari maxLifetime PgBouncer server_idle_timeout dan kichik bo'lsin
spring.datasource.hikari.max-lifetime=1500000
```

## 32.12 Integratsiyani sinash: tashqi servis sekinlashganda nima bo'ladi

Integratsiyani sinashda asosiy savol "xato qaytsa nima bo'ladi" emas, "sekinlashsa nima bo'ladi". Toza xato oson, u darhol qaytadi. Haqiqiy avariya esa dependency 5 sekundda javob berganda boshlanadi: thread pool to'ladi, navbat o'sadi, deadline tugaydi va sizning servis ham o'ladi, garchi o'zi sog'ligi joyida bo'lsa.

Kamida beshta sahnani o'lchash kerak: dependency ga 5 sekund latency qo'shilgan, dependency paketni jim tashlaydigan blackhole, javobni sekin tomchilab yuborish, sertifikat muddati tugagan, DNS javob bermaydi. Har safar uchta raqamni yozib olasiz: birinchi xatoga qancha vaqtda yetildi, avariya paytida qancha foiz so'rov bajarildi, dependency tiklangandan keyin servis necha sekundda normaga qaytdi. Oxirgi raqam 30 sekunddan uzun bo'lsa, pool va retry sozlamalaringiz noto'g'ri. Buni avtomatlashtirish vositalari [testlash qo'llanmasidagi](../testing/README.md) resilience testlari bo'limida.

| tuzoq | yechim |
| --- | --- |
| Read timeout butun so'rov deb o'ylash | Umumiy deadline qo'shish, sekin tomchilovchi javobni sinash |
| Pool acquire timeout default 45 sekund | Aniq 300 dan 500 ms gacha, navbat chuqurligi cheklangan |
| `maxLifetime` LB yoki PgBouncer idle timeout dan katta | Pool tomonida qisqaroq qiymat, keepalive probe yoqilgan |
| `networkaddress.cache.ttl=-1` abadiy DNS kesh | 30 sekund TTL va ulanish umrini cheklash |
| Barcha xatoga 3 marta qayta urinish | Idempotentlik tekshiruvi va bitta qatlamda retry |
| Jitter siz eksponensial backoff | Full jitter, tasodifiy oraliq 0 dan cap gacha |
| Client va LB idle timeout teng | Qattiq tartib: client < LB < server keep-alive |
| Ilovada timeout bor, bazada yo'q | Rol darajasida `statement_timeout` va `lock_timeout` |
| Notanish enum deserializatsiyani buzadi | Tolerant reader va default enum qiymati |
| Sertifikat muddati faqat avariyada bilinadi | CI da `checkend` tekshiruvi va 30 kunlik ogohlantirish |

## 32.13 Soat ishonchsiz: monoton soat, clock skew va TTL ga tayanmaslik

Taqsimlangan tizimda vaqt tarmoq kabi ishonchsiz resurs. Ikki xil soat bor va ularni aralashtirish ko'p xatoning sababi: kun soati (`System.currentTimeMillis()`, `Instant.now()`) NTP bilan sozlanadi va **orqaga qaytishi** mumkin; monoton soat (`System.nanoTime()`) esa NTP sozlashidan ta'sirlanmaydi, shuning uchun davomiylik o'lchash uchun to'g'ri tanlov. Lekin uning kafolatini oshirib yubormaslik kerak: javadoc monotonlikni va aniqlikni kafolatlamaydi, qiymat manfiy bo'lishi mumkin deb ataylab ogohlantiradi, va boshlanish nuqtasi ma'nosiz. Amalda monotonlik operatsion tizimdan keladi (Linux da `CLOCK_MONOTONIC`), platformadan emas; qiymat esa faqat shu jarayon ichida solishtiriladi.

| Vazifa | Soat |
|---|---|
| Hodisa vaqtini saqlash, log, audit | kun soati (`Instant.now()`) |
| Davomiylikni o'lchash, timeout, retry kechikishi | monoton soat (`System.nanoTime()`) |
| Ikki mashina hodisasini tartiblash | hech qaysi biri yetarli emas |

```java
// yomon: kun soati NTP sozlanishida orqaga qaytsa, davomiylik manfiy chiqadi
long start = System.currentTimeMillis();
call();
long tookMs = System.currentTimeMillis() - start;

// yaxshi: davomiylik monoton soat bilan
long start = System.nanoTime();
call();
Duration took = Duration.ofNanos(System.nanoTime() - start);
```

Uchinchi qatorning ma'nosi muhim: ikki mashinaning timestamp ini solishtirib tartib chiqarish ishlamaydi, chunki soatlar orasidagi farq (clock skew) odatdagi holat. Shundan ikkita amaliy qoida kelib chiqadi. Birinchisi: tartib kerak bo'lsa, vaqt emas, ketma-ketlik ishlatiladi - baza sekvensiyasi, Kafka offseti, versiya raqami yoki mantiqiy soat. "Oxirgi yozuv g'alaba qiladi" qoidasini timestamp bilan qurish jim ma'lumot yo'qotishga olib keladi.

Ikkinchisi: taqsimlangan qulf va lease ni faqat TTL ga ishonib qurish xavfli. Qulf egasi GC pauzasi yoki uzun stop-the-world dan keyin o'zini hali ega deb o'ylab ishni davom ettirishi mumkin, holbuki TTL tugagan va qulfni boshqa olgan. Himoya - himoya belgisi (fencing token): qulf bilan birga o'sib boruvchi raqam beriladi va resurs eski raqamli yozuvni rad etadi. Shu qoida JWT va token muddati uchun ham amal qiladi: `exp` tekshiruvi mashinalar orasidagi kichik farqga toqat qiladigan oraliq (clock skew allowance) bilan yoziladi, aks holda to'g'ri token chekka holatda rad etiladi.

## 32.14 Amalda qo'llash

- [ ] Barcha tashqi HTTP klientlarni ro'yxatga oling va har biriga connect, pool acquire, read va umumiy deadline qiymatlarini aniq yozib chiqing, default qolgan joy qolmasin.
- [ ] Asosiy API lar uchun timeout byudjetini chizing: SLO dan boshlab har bir quyi chaqiruvga millisekund taqsimlang va yig'indi SLO dan kichik ekanini tekshiring.
- [ ] HikariCP va HTTP pool kattaligini Little qonuni bilan qayta hisoblang, keyin barcha podlar yig'indisini PostgreSQL `max_connections` bilan solishtiring.
- [ ] `maxLifetime`, `idleTimeout` va LB hamda PgBouncer idle timeout qiymatlarini bitta jadvalga yozib, tartib buzilmaganiga ishonch hosil qiling.
- [ ] Rol darajasida `statement_timeout`, `lock_timeout` va `idle_in_transaction_session_timeout` ni o'rnatib, OLTP va hisobot rollarini ajrating.
- [ ] Qayta urinish siyosatini audit qiling: idempotentlik kalitlari bor-yo'qligini, full jitter ishlatilganini va retry faqat bitta qatlamda bo'lishini tasdiqlang.
- [ ] Sertifikat muddatini CI da `checkend` bilan tekshiradigan qadam qo'shing va truststore dagi ichki CA muddatini ham kuzatuvga oling.
- [ ] Eng muhim dependency ga 5 sekund latency va blackhole inyeksiya qilib, birinchi xato vaqtini, bajarilgan so'rov ulushini va tiklanish vaqtini o'lchab, natijani relizga shart qilib qo'ying.
- [ ] Davomiylik o'lchaydigan kodda `currentTimeMillis` ishlatilgan joylarni `nanoTime` ga o'tkazing.
- [ ] Timestamp bilan tartiblanadigan yoki "oxirgi yozuv g'alaba qiladi" qoidasiga tayangan joylarni toping va ketma-ketlikka o'tkazing.
- [ ] Taqsimlangan qulf va lease larda himoya belgisi (fencing token) borligini tekshiring.

## Manbalar

- Martin Kleppmann, *Designing Data-Intensive Applications*, 8-bob - ishonchsiz soat, clock skew, himoya belgisi va jarayon pauzasi
- Martin Kleppmann, *Designing Data-Intensive Applications*, 9-bob - linearizability, tartib va konsensus
- Martin Kleppmann, *Designing Data-Intensive Applications*, 5-bob - replikatsiya kechikishi va o'qish kafolatlari
- OpenJDK, `MultiExchange` va `HttpRequest`
  ([https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.net.http/share/classes/jdk/internal/net/http/MultiExchange.java](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.net.http/share/classes/jdk/internal/net/http/MultiExchange.java),
  tag `jdk-25-ga`, GPLv2 + Classpath istisnosi) - 32.2 dagi
  `HttpRequest.timeout` ning har urinish uchun ro'yxatga olinishi va
  javob sarlavhalarida bekor qilinishi, 32.8 dagi ichki retry va
  `HttpConnectTimeoutException` ierarxiyasi.
- OpenJDK, `InetAddressCachePolicy` va `java.security`
  ([https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/sun/net/InetAddressCachePolicy.java](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/sun/net/InetAddressCachePolicy.java),
  tag `jdk-25-ga`) - 32.6 dagi DNS kesh TTL ning xavfsizlik property si
  bo'lishi, default 30 va 10 sekund, va `sun.net.inetaddr.ttl`
  fallback nomi.
- OpenJDK, `System.nanoTime` javadoc i
  ([https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/java/lang/System.java](https://github.com/openjdk/jdk/blob/jdk-25-ga/src/java.base/share/classes/java/lang/System.java),
  tag `jdk-25-ga`) - 32.13 dagi kafolatlar chegarasi.
- Linux, `ip-sysctl.rst`
  ([https://github.com/torvalds/linux/blob/v6.12/Documentation/networking/ip-sysctl.rst](https://github.com/torvalds/linux/blob/v6.12/Documentation/networking/ip-sysctl.rst),
  tag `v6.12`, GPL-2.0) - 32.1 dagi `tcp_retries2` ning 924.6 sekundi
  pastki chegara ekani va `tcp_keepalive_time` ning 7200 sekundi.
- HikariCP, README va `HikariConfig`
  ([https://github.com/brettwooldridge/HikariCP/blob/HikariCP-7.1.0/README.md](https://github.com/brettwooldridge/HikariCP/blob/HikariCP-7.1.0/README.md),
  tag `HikariCP-7.1.0`, Apache-2.0) - 32.5 dagi `idleTimeout` ning
  faqat `minimumIdle` kichik bo'lganda ishlashi, `maxLifetime` 30
  daqiqa, `connectionTimeout` 30 sekund, `validationTimeout` 5 sekund.
- Reactor Netty, `ConnectionProvider`
  ([https://github.com/reactor/reactor-netty/blob/v1.2.9/reactor-netty-core/src/main/java/reactor/netty/resources/ConnectionProvider.java](https://github.com/reactor/reactor-netty/blob/v1.2.9/reactor-netty-core/src/main/java/reactor/netty/resources/ConnectionProvider.java),
  tag `v1.2.9`, Apache-2.0) - 32.2 va 32.12 dagi
  `pendingAcquireTimeout` ning 45 sekundlik default i.
- Apache HttpClient 5, `RequestConfig`
  ([https://github.com/apache/httpcomponents-client/blob/rel/v5.6.5/httpclient5/src/main/java/org/apache/hc/client5/http/config/RequestConfig.java](https://github.com/apache/httpcomponents-client/blob/rel/v5.6.5/httpclient5/src/main/java/org/apache/hc/client5/http/config/RequestConfig.java),
  tag `rel/v5.6.5`, Apache-2.0) - 32.2 dagi `connectionRequestTimeout`
  ning uch daqiqalik default i.
- Spring Boot, HTTP klient, SSL va Tomcat property lari
  ([https://github.com/spring-projects/spring-boot/blob/v3.5.0/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/http/client/AbstractHttpClientProperties.java](https://github.com/spring-projects/spring-boot/blob/v3.5.0/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/http/client/AbstractHttpClientProperties.java),
  tag `v3.5.0`, Apache-2.0; SSL uchun
  [3.2.0 dagi `SslBundleProperties`](https://github.com/spring-projects/spring-boot/blob/v3.2.0/spring-boot-project/spring-boot-autoconfigure/src/main/java/org/springframework/boot/autoconfigure/ssl/SslBundleProperties.java)) -
  32.2 dagi `spring.http.client.*` kalitlari, 32.7 dagi
  `reload-on-update` ning 3.2 da paydo bo'lishi, 32.9 dagi Tomcat
  `max-threads` 200 va `accept-count` 100 default lari.
- Spring Boot 4.0, Jackson 2 avtokonfiguratsiyasining deprecation i
  ([https://github.com/spring-projects/spring-boot/blob/v4.0.0/module/spring-boot-jackson2/src/main/java/org/springframework/boot/jackson2/autoconfigure/Jackson2ObjectMapperBuilderCustomizer.java](https://github.com/spring-projects/spring-boot/blob/v4.0.0/module/spring-boot-jackson2/src/main/java/org/springframework/boot/jackson2/autoconfigure/Jackson2ObjectMapperBuilderCustomizer.java),
  tag `v4.0.0`, Apache-2.0) - 32.10 dagi interfeysning 4.2.0 da olib
  tashlanishi.
- pgjdbc hujjati va PostgreSQL GUC jadvali
  ([https://github.com/pgjdbc/pgjdbc/blob/REL42.7.7/docs/content/documentation/use.md](https://github.com/pgjdbc/pgjdbc/blob/REL42.7.7/docs/content/documentation/use.md),
  tag `REL42.7.7`, BSD-2-Clause; va
  [postgres `guc_tables.c`](https://github.com/postgres/postgres/blob/REL_17_0/src/backend/utils/misc/guc_tables.c),
  tag `REL_17_0`, PostgreSQL License) - 32.3 dagi `socketTimeout` ning
  ulanishni yopishi va sessiya darajasidagi timeout lar.
- Kubernetes, kubelet DNS sozlamasi
  ([https://github.com/kubernetes/kubernetes/blob/v1.33.9/pkg/kubelet/network/dns/dns.go](https://github.com/kubernetes/kubernetes/blob/v1.33.9/pkg/kubelet/network/dns/dns.go),
  tag `v1.33.9`, Apache-2.0) - 32.6 dagi `ndots:5` default i.
- nginx, `ngx_http_proxy_module.c`
  ([https://github.com/nginx/nginx/blob/release-1.27.5/src/http/modules/ngx_http_proxy_module.c](https://github.com/nginx/nginx/blob/release-1.27.5/src/http/modules/ngx_http_proxy_module.c),
  tag `release-1.27.5`, BSD tipidagi litsenziya) - 32.11 dagi
  `proxy_read_timeout` ning 60 sekundlik default i.

---

[&larr; 31. Deployment haqiqati: konteyner, cgroup, JVM va probe](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md) · [Mundarija](README.md) · [33. Sxema migratsiyasi va to'xtashsiz reliz &rarr;](33-sxema-migratsiyasi-va-toxtashsiz-reliz.md)
