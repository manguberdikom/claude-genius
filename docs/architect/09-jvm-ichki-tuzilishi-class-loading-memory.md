<!-- doc: architect | chapter: 9 | part: II. Java chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 9. JVM ichki tuzilishi: class loading, memory model, JIT (JVM Internals)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [9.1 JVM xotira hududlari: heap, metaspace, stack, code cache, direct buffer](#91-jvm-xotira-hududlari-heap-metaspace-stack-code-cache-direct-buffer)
- [9.2 Class loading bosqichlari va class loader ierarxiyasi](#92-class-loading-bosqichlari-va-class-loader-ierarxiyasi)
- [9.3 Spring Boot fat jar va uning class loading ga ta'siri](#93-spring-boot-fat-jar-va-uning-class-loading-ga-tasiri)
- [9.4 Bytecode va interpretatsiya: ishga tushish paytidagi sekinlik](#94-bytecode-va-interpretatsiya-ishga-tushish-paytidagi-sekinlik)
- [9.5 JIT: C1, C2, profil yig'ish, tiered compilation](#95-jit-c1-c2-profil-yigish-tiered-compilation)
- [9.6 Inlining, escape analysis va boshqa optimizatsiyalar](#96-inlining-escape-analysis-va-boshqa-optimizatsiyalar)
- [9.7 Deoptimizatsiya: nega kod birdan sekinlashadi](#97-deoptimizatsiya-nega-kod-birdan-sekinlashadi)
- [9.8 Isinish (warmup) muammosi va u deployment ga qanday ta'sir qiladi](#98-isinish-warmup-muammosi-va-u-deployment-ga-qanday-tasir-qiladi)
- [9.9 Java memory model: happens-before, volatile, final maydon kafolatlari](#99-java-memory-model-happens-before-volatile-final-maydon-kafolatlari)
- [9.10 JVM ni kuzatish uchun asosiy flaglar va `-XX:+PrintFlagsFinal` dan foydalanish](#910-jvm-ni-kuzatish-uchun-asosiy-flaglar-va--xxprintflagsfinal-dan-foydalanish)
- [9.11 AOT, CDS va GraalVM native image: qachon mantiqli](#911-aot-cds-va-graalvm-native-image-qachon-mantiqli)
- [9.12 Sinf o'zligi, `<clinit>` va initsializatsiya qulfi](#912-sinf-ozligi-clinit-va-initsializatsiya-qulfi)
- [9.13 Amalda qo'llash](#913-amalda-qollash)

</details>



Arxitektor JVM ni "qora quti" deb qarasa, ishlab chiqarishdagi har bir g'alati holat uchun tushuntirish topa olmaydi. Nega to'lov servisi deploy dan keyin birinchi 90 sekundda p99 ni 40 ms dan 900 ms ga ko'taradi, nega hisobot generatori heap da joy bor paytda ham `OutOfMemoryError` beradi, nega bitta `volatile` olib tashlansa ombor qoldig'i hisoblovi bir necha kundan keyin xato qiymat ko'rsatadi. Javob bitta joyda: JVM ichida xotira qanday bo'linadi, class qanday yuklanadi, kod qanday kompilyatsiya qilinadi va kompilyatsiya qachon bekor qilinadi. Quyida shu mexanika va undan chiqadigan qarorlar.

## 9.1 JVM xotira hududlari: heap, metaspace, stack, code cache, direct buffer

`-Xmx` konteynerning butun xotirasi emas. Process ning RSS i heap dan tashqari yana bir qancha hududni o'z ichiga oladi va ularning har biri alohida chegara bilan boshqariladi. Heap da obyektlar yashaydi. Metaspace da class metadata, method struktura, constant pool yashaydi va u native xotiradan olinadi. Har bir thread o'z stack ini oladi, 64-bit Linux da default taxminan 1 MB. Code cache da JIT chiqargan mashina kodi turadi, tiered compilation yoqilgan holatda default taxminan 240 MB rezerv qilinadi. Direct buffer esa Netty, NIO va ba'zi driver lar ishlatadigan heap dan tashqari bufer.

Amaliy hisob: 300 ta platform thread faqat stack uchun taxminan 300 MB oladi. Shuning uchun `-Xmx` ni qattiq raqam bilan emas, foiz bilan berish ishonchliroq.

```bash
# Konteynerda xotira chegaralarini foiz bilan berish
java -XX:MaxRAMPercentage=70 \
     -XX:InitialRAMPercentage=70 \
     -XX:MaxMetaspaceSize=256m \
     -XX:MaxDirectMemorySize=256m \
     -XX:ReservedCodeCacheSize=192m \
     -Xss512k \
     -XX:+AlwaysPreTouch \
     -XX:+HeapDumpOnOutOfMemoryError \
     -XX:HeapDumpPath=/var/dumps \
     -XX:+ExitOnOutOfMemoryError \
     -jar payment-service.jar

# Haqiqatda qancha native xotira ketganini ko'rish
java -XX:NativeMemoryTracking=summary -jar payment-service.jar
jcmd <pid> VM.native_memory summary
jcmd <pid> GC.heap_info
jcmd <pid> Compiler.codecache
```

`-XX:+AlwaysPreTouch` heap sahifalariga ishga tushishda bir marta tegib chiqadi. Start vaqti bir necha yuz millisekund uzayadi, lekin birinchi yuklamadagi sahifa xatolari tufayli paydo bo'ladigan latency sakrashi yo'qoladi. Uzoq yashaydigan servis uchun bu yaxshi savdo, qisqa batch job uchun yo'q.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `-Xmx` konteyner limitiga teng | Metaspace va stack qo'shilib OOMKilled | `MaxRAMPercentage=70`, qolganini native uchun qoldirish |
| Metaspace cheklanmagan | Dinamik proxy va class generatsiya sekin o'sadi, node ni yeydi | `MaxMetaspaceSize` qo'yib, `class+load` ni kuzatish |
| Direct buffer leak | Heap bo'sh, lekin process o'ladi | `MaxDirectMemorySize` va NMT bilan tekshirish |
| Code cache to'lib qoladi | "CodeCache is full" ogohlantirishi, JIT o'chadi, hamma kod sekinlashadi | `ReservedCodeCacheSize` oshirish |
| Thread pool juda katta | Faqat stack uchun yuzlab MB | `Xss` kamaytirish yoki pool qisqartirish |
| Heap dump sozlanmagan | OOM dan keyin tahlil uchun hech narsa yo'q | `HeapDumpOnOutOfMemoryError` + mount qilingan papka |
| `OmitStackTraceInFastThrow` default | Takrorlanuvchi exception stack trace siz keladi | diagnostika paytida `-XX:-OmitStackTraceInFastThrow` |
| CPU limiti noto'g'ri ko'rinadi | GC va JIT thread soni xato tanlanadi | `-XX:ActiveProcessorCount` bilan aniq berish |

## 9.2 Class loading bosqichlari va class loader ierarxiyasi

Class yuklash uch bosqichdan iborat. Loading da bytecode topiladi va `Class` obyekti yaratiladi. Linking uch qismga bo'linadi: verification bytecode ni xavfsizlik va tiplar bo'yicha tekshiradi, preparation static maydonlarga default qiymat beradi, resolution esa constant pool dagi havolalarni haqiqiy class va method ga bog'laydi. Initialization da `static` blok va `static` maydon initsializatorlari ishlaydi, aynan shu bosqich faqat bir marta va thread-safe bajariladi.

Initialization bosqichining qachon boshlanishini bilish amalda ko'p g'alati holatni tushuntiradi, chunki ro'yxat qisqa va intuitiv emas. Sinf yoki interfeys T quyidagilardan birinchisi yuz berishidan oldin ishga tushiriladi: T sinf bo'lib, uning instansiyasi yaratilganda; T e'lon qilgan statik metod chaqirilganda; T e'lon qilgan statik maydonga qiymat yozilganda; T e'lon qilgan statik maydon ishlatilganda va u constant variable bo'lmaganda. Sinf ishga tushganda uning superklasslari va `default` metod e'lon qilgan superinterfeyslari ham ishga tushadi, lekin interfeysning ishga tushishi uning superinterfeyslarini o'z-o'zidan ishga tushirmaydi (*The Java Language Specification, Java SE 25*, 12.4.1, 446-bet). Teskari tomoni ham shu yerda: sinfning initsializatsiyasi uning vorisi ishga tushganda boshlanadi, `default` metodi bor interfeys esa uni bevosita yoki bilvosita implementatsiya qilgan sinf ishga tushganda ishga tushadi (*The Java Virtual Machine Specification, Java SE 25*, 5.5, 397-bet).

Shu ro'yxatdan amalda eng ko'p adashtiradigan natija chiqadi: statik maydonga voris sinf nomi bilan murojaat qilish voris sinfni ishga tushirmaydi, faqat maydonni e'lon qilgan sinf ishga tushadi. Spetsifikatsiyaning misoli shuni ko'rsatadi: `Super` da `static int taxi = 1729` bo'lsa, `Sub` da esa statik blok bo'lsa, `Sub.taxi` o'qilganda `Sub` ning statik bloki umuman ishlamaydi, chunki `taxi` aslida `Super` da e'lon qilingan (12.4.1, 447-448-betlar).

```java
class Config {
    static final Map<String, String> VALUES = load();
}

class DevConfig extends Config {
    static { registerDevOverrides(); }        // bu blok ishlamasligi mumkin
}

// DevConfig.VALUES o'qilganda registerDevOverrides() CHAQIRILMAYDI:
// VALUES maydoni Config da e'lon qilingan, shuning uchun faqat Config ishga tushadi.
// Ro'yxatga olish kerak bo'lsa, DevConfig ning o'z statik a'zosiga tegish shart.
```

JDK 9 dan beri ierarxiya shunday: bootstrap loader platform modullarini yuklaydi, platform loader JDK ning qolgan qismini, application loader esa classpath ni. Eski `ext` mexanizmi yo'q. Qoida oddiy: bola loader avval otasidan so'raydi, faqat u topa olmasa o'zi qidiradi. Shu sabab `javax.sql.DataSource` ni classpath ga qo'shib qo'yishning ma'nosi yo'q, platform loader uni har doim birinchi topadi.

```bash
# Qaysi class qaysi manbadan yuklangani
java -Xlog:class+load=info:file=/tmp/classload.log -jar order-service.jar

# Faqat bitta class ni kuzatish
grep 'com.shop.order.OrderService' /tmp/classload.log

# Loader lar bo'yicha statistika va class unload
jcmd <pid> VM.classloader_stats
java -Xlog:class+unload=info -jar order-service.jar
```

Bundan ikkita amaliy xulosa chiqadi. Birinchisi, `class+load` logida bitta class ikkita turli jar dan ko'rinsa, bu dependency konflikti va uning oqibati runtime da `NoSuchMethodError` bo'ladi. Ikkinchisi, static blokda fayl yoki tarmoq chaqiruvi bo'lsa, bu class ga birinchi tegadigan thread qolgan thread larni initialization lock da kutishga majbur qiladi.

Shu ierarxiyaning eng ko'p uchraydigan amaliy ko'rinishi DevTools ning avtomatik restartida. DevTools faol bo'lganda ilova bitta emas, ikkita alohida class loader ga yuklanadi: biriga `src/main/` dagi hamma narsa (Java kodi va xossa fayllari), ya'ni tez o'zgaradigan qism tushadi, ikkinchisiga esa kam o'zgaradigan dependency kutubxonalari tushadi. O'zgarish sezilganda faqat birinchi loader qayta yuklanadi va Spring application context qayta ishga tushadi, ikkinchi loader bilan JVM esa o'z joyida qoladi; ishga tushish vaqti shu hisobdan qisqaradi (Walls, 1-bob, 24-bet). Bundan chiqadigan narsa qulaylik emas, chegara: build faylidagi bog'liqlik qo'shilsa, o'zgarsa yoki olib tashlansa, bu avtomatik restartda ko'rinmaydi, chunki uni ushlab turgan loader qayta yuklanmaydi; o'sha o'zgarish kuchga kirishi uchun ilovani qo'lda to'liq qayta ishga tushirish kerak.

## 9.3 Spring Boot fat jar va uning class loading ga ta'siri

Spring Boot fat jar oddiy jar emas. Ichida `BOOT-INF/classes` va `BOOT-INF/lib/*.jar` turadi, ya'ni jar ichida jar. Standart `JarFile` bunday tuzilmani ocha olmaydi, shuning uchun Boot o'z launcher ini va o'z class loader ini ishlatadi. Boot 3.2 dan beri launcher sinflari `org.springframework.boot.loader.launch` paketida va ichki jar larga `nested:` protokoli bilan murojaat qilinadi.

Bu arxitekturaga uchta amaliy ta'sir qiladi. Birinchisi, ichki jar lar siqilmagan holda saqlanadi, shuning uchun fat jar hajmi odatdagidan katta ko'rinadi. Ikkinchisi, class topish yo'li bir pog'ona uzayadi, demak ishga tushish vaqti biroz oshadi. Uchinchisi va eng muhimi, CDS va AOT kabi optimizatsiyalar fat jar ichida yaxshi ishlamaydi, ularga yoyilgan tuzilma kerak.

```bash
# Fat jar ni qatlamlarga yoyish (Docker cache uchun va CDS uchun)
java -Djarmode=tools -jar payment-service.jar list-layers
java -Djarmode=tools -jar payment-service.jar extract --destination /app

# Yoyilgan holatda ishga tushirish: launcher o'rniga oddiy classpath
java -XX:+UseG1GC -jar /app/payment-service.jar

# Dependency konfliktini oldindan ko'rish
./mvnw dependency:tree -Dverbose -Dincludes=com.fasterxml.jackson.core
```

Dependency lar alohida Docker qatlamida bo'lsa, faqat ilova kodi o'zgargan deploy da registry ga 200 MB emas, taxminan 2 MB ketadi. Bu CI vaqtini ham, rollout tezligini ham yaxshilaydi.

## 9.4 Bytecode va interpretatsiya: ishga tushish paytidagi sekinlik

Java kompilyatori bytecode chiqaradi, mashina kodi emas. JVM ishga tushganda hamma method interpreter da bajariladi, ya'ni har bir bytecode instruksiya uchun JVM alohida ish qiladi. Interpreter da bajarilish kompilyatsiya qilingan koddan taxminan 10 dan 50 barobar sekin. Ishga tushish paytida nafaqat sizning kodingiz, balki Spring konteyner, Hibernate metamodel qurilishi, Jackson reflection tahlili ham interpreter da ketadi.

Class fayl faqat bajarilish uchun kerak bo'lgan narsani saqlaydi va bitta yo'qotish amalda ko'p joyni buzadi: metod parametrining NOMI class faylda faqat `MethodParameters` atributi chiqarilgan bo'lsa saqlanadi, ya'ni kod `javac -parameters` bilan kompilyatsiya qilinganda; aks holda refleksiya parametrlarni `arg0`, `arg1` deb ko'radi (*The Java Virtual Machine Specification, Java SE 25*, 4.7.24, 175-bet). Nomga tayangan hamma bog'lanish shundan jim buziladi: `@RequestParam` va `@PathVariable` ni nomsiz yozish, konstruktor orqali bog'lanish va `@ConfigurationProperties`. Spring Boot ning rasmiy build sozlamasi (`spring-boot-starter-parent` va Spring Boot Gradle plugini) bu flagni o'zi qo'yadi, shuning uchun muammo odatda qo'lda yozilgan Maven yoki Gradle konfiguratsiyasida, IDE ning alohida kompilyatorida yoki kod generatsiya qiladigan qadamda chiqadi. Belgisi aniq: Spring argument nomini aniqlay olmaganini aytib ishga tushishdan yoki so'rovni bog'lashdan bosh tortadi, yoki parametr jim bog'lanmay qoladi.

Shu sababli 2.5 sekundlik start vaqtining katta qismi haqiqiy ish emas, balki hali qizimagan kodning sekin bajarilishi. Arxitektura xulosasi: start vaqti muhim bo'lgan joyda avval ishlar sonini kamaytirish kerak, flaglarni emas. Keraksiz avtomatik konfiguratsiyani o'chirish, classpath scanning hududini toraytirish, keyin interpretatsiya narxini CDS yoki AOT bilan kamaytirish.

## 9.5 JIT: C1, C2, profil yig'ish, tiered compilation

HotSpot ikkita kompilyatorga ega. C1 tez kompilyatsiya qiladi, lekin optimizatsiyasi yuza. C2 sekin kompilyatsiya qiladi, lekin chiqargan kodi ancha tezroq. Tiered compilation ikkalasini birlashtiradi: method avval interpreter da ishlaydi, keyin C1 ga o'tadi va u yerda profil yig'adi, yetarlicha qizigandan keyin C2 ga uzatiladi.

Beshta daraja bor. 0 bu interpreter. 1 bu C1, profil yig'masdan, trivial method lar uchun. 2 va 3 bu C1 profil bilan. 4 bu C2. Default thresholdlar: `Tier3InvocationThreshold` taxminan 200, `Tier4InvocationThreshold` taxminan 5000.

```bash
# Qaysi method qaysi darajada kompilyatsiya qilinganini ko'rish
java -XX:+PrintCompilation -jar payment-service.jar | head -200

# Faqat C1: start tez, peak sekin (CLI va qisqa job uchun)
java -XX:TieredStopAtLevel=1 -jar report-cli.jar

# Kompilyator thread soni (kichik konteynerda muhim)
java -XX:CICompilerCount=2 -jar payment-service.jar

# Kompilyatsiya thresholdlarining haqiqiy qiymatlari
java -XX:+PrintFlagsFinal -version | grep -E 'Tier[34].*Threshold'
```

`-XX:TieredStopAtLevel=1` qaror nuqtasi sifatida qiziq. Hisobot generatori 20 sekund ishlab tugaydigan CLI bo'lsa, C2 ga qizishga vaqt yetmaydi va C1 da qolish umumiy vaqtni qisqartiradi. Doimiy ishlaydigan to'lov servisida esa bu flag peak throughput ni taxminan ikki barobar tushiradi, ya'ni zarar.

## 9.6 Inlining, escape analysis va boshqa optimizatsiyalar

C2 ning eng katta kuchi inlining da. Chaqirilgan method tanasi chaqiruv joyiga ko'chiriladi va shundan keyin boshqa hamma optimizatsiya ishlay oladi. `MaxInlineSize` default taxminan 35 bytecode, tez-tez chaqiriladigan method uchun `FreqInlineSize` taxminan 325. Shuning uchun uzun method inline bo'lmaydi va u bilan birga ichidagi butun optimizatsiya zanjiri uziladi. Kichik method lar yozish uslub masalasi emas, performance masalasi.

Escape analysis obyekt method chegarasidan chiqmasligini aniqlaydi. Chiqmasa, allokatsiya umuman bajarilmaydi, maydonlar registr yoki stack da saqlanadi. Shu bilan birga lock lar ham olib tashlanadi, agar obyekt faqat bitta thread ga ko'rinsa.

```java
// Bu Money obyekti method dan chiqmaydi, escape analysis uni yo'q qiladi
private long jamiTiyin(List<OrderLine> lines) {
    long jami = 0;
    for (OrderLine line : lines) {
        Money narx = line.narx();           // allokatsiya yo'qoladi
        jami += narx.tiyin() * line.soni();
    }
    return jami;
}

// Bu esa chiqadi: havola tashqariga qaytadi, allokatsiya qoladi
public Money jami(List<OrderLine> lines) {
    return Money.ofTiyin(jamiTiyin(lines));
}

// Megamorphic chaqiruv: 3 dan ortiq implementatsiya inline bo'lmaydi
public BigDecimal komissiya(PaymentMethod m, BigDecimal summa) {
    return m.komissiya(summa);  // 7 ta implementatsiya bor bo'lsa, virtual chaqiruv
}
```

Oxirgi misol muhim. Interface ning bitta yoki ikkita implementatsiyasi bo'lsa, JIT uni monomorphic yoki bimorphic deb hisoblab inline qiladi. To'lov usullari soni ettiga chiqsa, chaqiruv megamorphic bo'ladi va inline qilinmaydi. Issiq loop da strategiyani har safar tanlash o'rniga, qarorni bir marta loop dan tashqarida qabul qilish samaraliroq.

```bash
# Inlining qarorlarini ko'rish
java -XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining \
     -XX:+PrintCompilation -jar payment-service.jar 2>&1 | grep 'too big'

# Escape analysis va allokatsiya yo'q qilish default yoqilgan, tekshirish
java -XX:+PrintFlagsFinal -version | grep -E 'DoEscapeAnalysis|EliminateAllocations|EliminateLocks'

# Inline chegaralarining haqiqiy qiymatlari
java -XX:+PrintFlagsFinal -version | grep -E 'MaxInlineSize|FreqInlineSize|MaxInlineLevel'
```

## 9.7 Deoptimizatsiya: nega kod birdan sekinlashadi

JIT optimistik taxminlar asosida kod chiqaradi. "Bu `if` hech qachon true bo'lmaydi", "bu interface ning faqat bitta implementatsiyasi bor", "bu havola null emas". Agar taxmin buzilsa, JVM uncommon trap ga tushadi va kompilyatsiya qilingan kodni bekor qiladi, bajarilish interpreter ga qaytadi. Keyin method qaytadan profil yig'adi va qayta kompilyatsiya qilinadi.

Hayotiy misol: to'lov servisi bir oy davomida faqat karta to'lovini ko'radi va JIT shunga moslashadi. Bank o'tkazmasi orqali to'lovlar kelganda o'sha issiq yo'l deoptimizatsiya bo'ladi va latency bir necha sekund ko'tariladi. Yana bir misol: ilgari yolg'iz bo'lgan interface ga ikkinchi implementatsiya qo'shilsa, class hierarchy ga asoslangan inline lar bekor qilinadi.

```bash
# Deoptimizatsiya hodisalarini log qilish
java -Xlog:deoptimization=info:file=/tmp/deopt.log:uptime,tags -jar payment-service.jar

# Eng ko'p takrorlanadigan sabablarni sanash
grep -o 'reason=[a-z_]*' /tmp/deopt.log | sort | uniq -c | sort -rn

```

Arxitektura xulosasi: exception ni oqim boshqarish uchun ishlatmaslik, issiq yo'ldan noyob holatlarni alohida method ga chiqarish. Bu JIT taxminini stabil qiladi. Monitoring uchun xulosa: latency ning sababsiz o'sishini tekshirganda GC va DB dan keyin uchinchi gipoteza deoptimizatsiya bo'lishi kerak.

## 9.8 Isinish (warmup) muammosi va u deployment ga qanday ta'sir qiladi

Yangi pod ko'tarilganda u darhol to'liq tezlikda ishlamaydi. Odatiy manzara: birinchi 5 sekundda context quriladi, keyingi taxminan 30 dan 90 sekundda JIT issiq yo'llarni C2 ga olib chiqadi, shu bilan birga Hibernate query plan cache va HikariCP connection lar to'ladi. Agar load balancer pod ni readiness dan keyin darhol to'liq trafik bilan to'ldirsa, o'sha oynada p99 bir necha barobar oshadi.

Isinishning bir qismi esa JIT emas, bog'lanish (linkage) ishi. Lambda va metod havolasining chaqiruv joyi `invokedynamic` instruksiyasiga kompilyatsiya qilinadi va u faqat BIRINCHI bajarilganda hal qilinadi: shu payt bootstrap metod chaqiriladi, bootstrap metodning sinfi ishga tushadi va chaqiruv joyi uchun implementatsiya bog'lanadi; keyingi chaqiruvlarda bu ish qaytarilmaydi (*The Java Virtual Machine Specification, Java SE 25*, 5.5, 397-bet). Amalda bu birinchi so'rovning keyingilaridan sezilarli sekin bo'lishining yana bitta sababi, va u har bir chaqiruv joyi uchun alohida to'lanadi, ya'ni stream va lambda zich ishlatilgan kod yo'lida narx bir marta emas, chaqiruv joylari soniga ko'paytirilgan holda keladi. Shundan ikki amaliy natija: [mikro o'lchovda](14-jvm-profiling-va-diagnostika-jfr-async.md#148-mikro-olchov-tuzoqlari-va-jmh-nega-kerak) warmup iteratsiyalari majburiy, aks holda o'lchov bog'lanish narxini o'lchaydi; va "birinchi so'rov sekin" hodisasini diagnoz qilganda GC va JIT dan tashqari shu bog'lanish ishi ham hisobga olinadi.

Eng arzon yechim bosqichma bosqich trafik berish.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Xotira chegarasi | `-Xmx` ni konteyner limitiga teng qo'yish | `MaxRAMPercentage` + native hudud uchun zahira, NMT bilan tekshirish |
| Start sekinligi | "Java shunchaki sekin" deb qabul qilish | Bean sonini o'lchash, lazy init, keyin CDS yoki AOT |
| Deploy paytidagi latency | Darhol 100% trafik berish | Readiness dan keyin bosqichli trafik, canary, startupProbe |
| JIT sozlash | Internetdan topilgan flag to'plamini ko'chirish | `PrintFlagsFinal` bilan default ni ko'rib, bitta flag ni o'lchab o'zgartirish |
| Konkurensiya | Hamma umumiy maydonga `synchronized` | happens-before zanjirini loyihalash, immutable va `volatile` ni to'g'ri joyda |
| Native image | "Tezroq, demak har joyda ishlatamiz" | Faqat start va xotira muhim bo'lgan servisda, peak throughput ni o'lchagandan keyin |
| Class konflikti | Runtime xatosini kutish | `class+load` logi va dependency tree ni CI da tekshirish |
| Diagnostika | Muammo chiqqanda flag qo'shish | JFR va heap dump ni oldindan doimiy sozlab qo'yish |

```yaml
# Kubernetes: isinish uchun vaqt berish va trafikni asta ko'tarish
readinessProbe:
  httpGet: { path: /actuator/health/readiness, port: 8080 }
  periodSeconds: 5
  failureThreshold: 3
startupProbe:
  httpGet: { path: /actuator/health/liveness, port: 8080 }
  periodSeconds: 5
  failureThreshold: 30        # taxminan 150 sekund start uchun ruxsat
lifecycle:
  preStop:
    exec: { command: ["sleep", "10"] }   # in-flight so'rovlar tugashi uchun
resources:
  requests: { cpu: "1", memory: "1Gi" }
  limits:   { cpu: "2", memory: "2Gi" }
```

```properties
# Isinishni tezlashtiradigan sozlamalar
spring.datasource.hikari.minimum-idle=10
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=3000
spring.jpa.properties.hibernate.query.plan_cache_max_size=2048
spring.main.lazy-initialization=false
management.endpoint.health.probes.enabled=true
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

Diqqat: `spring.main.lazy-initialization=true` start vaqtini qisqartiradi, lekin ishni birinchi so'rovga suradi. Muammoni hal qilmaydi, ko'rinmaydigan joyga ko'chiradi, shuning uchun uni faqat lokal development da yoqish mantiqli.

## 9.9 Java memory model: happens-before, volatile, final maydon kafolatlari

JMM kompilyator, JVM va protsessorga kodni qayta tartiblashga ruxsat beradi. Bitta thread ichida natija o'zgarmaydi, lekin ikki thread bir xil maydon bilan ishlaganda tartib kafolatlanmaydi. Kafolatni happens-before munosabati beradi. Asosiy manbalar: monitor ni bo'shatish va keyin shu monitor ni olish, `volatile` ga yozish va keyin shu maydonni o'qish, thread ni ishga tushirish va uning tugashini kutish, hamda `java.util.concurrent` dagi struktura lar.

```java
// Xato: flag ko'rinishi kafolatlanmagan, loop abadiy davom etishi mumkin
private boolean toxtatildi = false;          // volatile yo'q

// To'g'ri: volatile yozish va o'qish orasida happens-before bor
private volatile boolean toxtatildi = false;

public void toxtat() { toxtatildi = true; }

public void ishla() {
    while (!toxtatildi) {
        qoldiqniHisobla();
    }
}

// final maydon kafolati: konstruktor tugagach boshqa thread to'liq holatni ko'radi
public final class OmborQoldigi {
    private final long tiyin;
    private final Instant vaqt;

    public OmborQoldigi(long tiyin, Instant vaqt) {
        this.tiyin = tiyin;
        this.vaqt = vaqt;
        // DIQQAT: bu yerda this ni tashqariga bermaslik kerak, aks holda kafolat buziladi
    }
}
```

`final` maydonni konstruktordan keyin o'zgartirish alohida holat va u deserializatsiya hamda reflection da uchraydi. JLS buning uchun yagona mantiqiy semantikasi bor shaklni ko'rsatadi: obyekt quriladi, keyin uning `final` maydonlari yangilanadi, va obyekt boshqa threadlarga ko'rinadigan qilinmasligi hamda `final` maydonlari o'qilmasligi kerak, toki barcha yangilanish tugamaguncha; `final` maydonning "freeze" nuqtasi konstruktor oxirida ham, reflection yoki boshqa maxsus mexanizm bilan har bir o'zgartirishdan keyin ham yuzaga keladi (*The Java Language Specification, Java SE 25 Edition*, 17.5.3 (799-bet)).

Ikki chalkashlik qoladi. Birinchisi: `final` maydon e'londa constant expression bilan initsializatsiya qilingan bo'lsa, o'zgarish umuman ko'rinmasligi mumkin, chunki o'sha maydonning ishlatilishi kompilyatsiya vaqtida constant expression qiymati bilan almashtiriladi. Ikkinchisi: spetsifikatsiya `final` maydonlar ustida agressiv optimizatsiyaga ruxsat beradi, ya'ni bitta thread ichida `final` maydonni o'qishlarni konstruktorda bo'lmagan o'zgartirishlar bilan qayta tartiblash joiz; JLS ning misolida reflection bilan maydonni o'zgartiradigan metod chaqiruvi ikki o'qish orasida turadi va natija -1, 0 yoki 1 bo'lishi mumkin (17.5.3 (799-800-betlar)). Amaliy qoida: `final` maydonni keyin o'zgartiradigan kodni faqat deserializatsiya yo'lida qoldiring, o'zgartirish tugamaguncha obyekt havolasini hech kimga bermang, va o'qiladigan qiymat uchun constant expression dan foydalanmang.

`final` maydon kafolati shartli: konstruktor ichida `this` havolasi tashqariga chiqmasligi shart. Listener ni konstruktor ichida registratsiya qilish aynan shu kafolatni buzadi. Amaliy qoida: umumiy mutable holatni imkon qadar yo'q qilish, qolganida happens-before zanjirini ongli loyihalash. Immutable record, `AtomicLong`, `ConcurrentHashMap` va `BlockingQueue` kafolatni o'zi beradi. `volatile` faqat ko'rinishni beradi, atomiklikni emas: `counter++` ustida u hech narsa hal qilmaydi.

## 9.10 JVM ni kuzatish uchun asosiy flaglar va `-XX:+PrintFlagsFinal` dan foydalanish

Flag haqida taxmin qilmaslik kerak. `-XX:+PrintFlagsFinal` har bir flagning haqiqiy qiymatini va uning manbasini ko'rsatadi. Qiymat yonidagi `{default}` va `{ergonomic}` belgisi muhim: `ergonomic` degani JVM konteyner va CPU ga qarab o'zi tanlagan.

```bash
# Ishlayotgan konfiguratsiyaning haqiqiy qiymatlari
java -XX:+PrintFlagsFinal -version | grep -E 'MaxHeapSize|InitialHeapSize|UseG1GC|UseZGC'

# Faqat default dan farq qiladiganlar
java -XX:+PrintFlagsFinal -version | grep -v 'default'

# Jonli process dan olish, qayta ishga tushirmasdan
jcmd <pid> VM.flags -all
jcmd <pid> VM.command_line

# Doimiy yoqib qo'yiladigan minimal to'plam
java -Xlog:gc*:file=/var/log/gc.log:uptime,level,tags:filecount=5,filesize=20m \
     -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/dumps \
     -XX:StartFlightRecording:settings=profile,maxsize=256m,filename=/var/dumps/app.jfr \
     -XX:NativeMemoryTracking=summary \
     -jar payment-service.jar
```

GC log, heap dump va JFR ni muammo chiqqandan keyin yoqish kech. Narxi kichik: GC log amalda sezilmaydi, `NativeMemoryTracking=summary` taxminan 5 dan 10 foiz native xotira ustama beradi. Oldindan sozlab qo'yish incident vaqtida soatlarni tejaydi.

## 9.11 AOT, CDS va GraalVM native image: qachon mantiqli

Uchta variant bir muammoning uch yechimi va narxi butunlay boshqa. CDS class metadata ni arxivga oladi, keyingi start da verification va parsing takrorlanmaydi, start vaqti taxminan 20 dan 35 foizga qisqaradi, kod o'zgarmaydi. JDK 24 dan boshlangan AOT cache bundan ko'proq ish qiladi, link holatini ham saqlaydi. Native image butun ilovani oldindan mashina kodiga kompilyatsiya qiladi, start taxminan 50 ms ga tushadi va xotira sarfi bir necha barobar kamayadi, lekin reflection uchun metadata kerak va peak throughput odatda HotSpot dan past.

```bash
# CDS: training run, keyin arxiv bilan ishga tushirish (yoyilgan tuzilma kerak)
java -Djarmode=tools -jar payment-service.jar extract --destination /app
java -XX:ArchiveClassesAtExit=/app/app.jsa \
     -Dspring.context.exit=onRefresh -jar /app/payment-service.jar
java -XX:SharedArchiveFile=/app/app.jsa -jar /app/payment-service.jar

# AOT cache (JDK 24+): yozib olish va ishlatish
java -XX:AOTMode=record -XX:AOTConfiguration=app.aotconf -jar /app/payment-service.jar
java -XX:AOTMode=create -XX:AOTConfiguration=app.aotconf -XX:AOTCache=app.aot -jar /app/payment-service.jar
java -XX:AOTCache=app.aot -jar /app/payment-service.jar

# Spring AOT bilan native image
./mvnw -Pnative native:compile
./target/payment-service
```

Qaror mezoni oddiy. Uzoq ishlaydigan va yuqori throughput talab qiladigan to'lov servisi uchun CDS yoki AOT cache yetarli va xavfsiz tanlov. Scale-to-zero funksiya yoki kamdan kam ishlaydigan ichki yordamchi servis uchun native image mantiqli. Hibernate va keng reflection ishlatadigan monolitni native image ga ko'chirish odatda foydadan ko'p vaqt oladi.

## 9.12 Sinf o'zligi, `<clinit>` va initsializatsiya qulfi

Yuqoridagi uch bosqich sinf qanday yuklanishini aytadi, lekin ikki savolni ochiq qoldiradi: yuklangan sinf aslida KIM va uning statik qismi QACHON ishlaydi. Ikkisining javobi ham diagnostikada tez-tez kerak bo'ladi, chunki ularning buzilishi chalg'ituvchi xato xabari bilan chiqadi.

Birinchi savolning javobi qisqa: yaratilgandan keyin sinf nomi bilan emas, `(binar nom, aniqlovchi class loader)` juftligi bilan aniqlanadi (*The Java Virtual Machine Specification, Java SE 25*, 5.3, 365-bet). Ya'ni bir xil nomli sinf ikki loader da yuklangan bo'lsa, bu ikki boshqa tur va ular orasidagi cast `ClassCastException` beradi; xato matni esa "`com.shop.Order` ni `com.shop.Order` ga aylantirib bo'lmaydi" shaklida chiqadi va dasturchini butunlay noto'g'ri yo'nalishga olib ketadi. Amalda bu DevTools ning ikki loaderi, plugin yuklaydigan arxitektura, eski ilova serverlari va o'z `URLClassLoader` ini yozgan kod bilan uchrashganda chiqadi. Diagnozning to'g'ri birinchi qadami ham shundan kelib chiqadi: sinf nomini emas, loader ni solishtirish (`obj.getClass().getClassLoader()` ni kutilgan tur loaderi bilan).

Shu juftlikdan ikkinchi, kamdan-kam bilinadigan natija chiqadi: ish vaqtidagi paket ham paket nomi VA aniqlovchi loader bilan aniqlanadi (5.3, 365-bet). Demak `package private` ko'rinish class loader chegarasidan o'tmaydi: nomi bir xil paketdagi, lekin boshqa loader yuklagan sinflar bir-birining paket ichidagi a'zosini ko'rmaydi va `IllegalAccessError` chiqadi. Testni "bir xil paket" deb yozib, ishlab chiqarishda boshqa loaderga tushib qolgan kod shu yerda yiqiladi.

Spetsifikatsiya yaxshi yozilgan loader uchun uchta xossani ham sanaydi: bir xil nom uchun har doim bir xil `Class` obyektini qaytarish; L1 loader C ni yuklashni L2 ga delegatsiya qilgan bo'lsa, C ning bevosita superklassi va superinterfeyslari, maydon turlari, metod parametrlari va qaytish turlari uchun L1 ham, L2 ham bir xil `Class` qaytarishi; va oldindan yuklash (prefetch) yoki guruh bilan yuklash qilgan loader xatoni faqat prefetch bo'lmasa ham yuzaga kelishi mumkin bo'lgan nuqtada ko'rsatishi (5.3, 365-bet). Uchinchi xossa umumiy qoidaning xususiy holati: yuklashdagi xato uning yuzaga kelgan joyida emas, sinf bevosita yoki bilvosita ISHLATILGAN nuqtada tashlanadi. Shuning uchun `NoClassDefFoundError` ning stack trace i aybdor jar ni ko'rsatmaydi, u faqat qurbonni ko'rsatadi, va haqiqiy sababni `-Xlog:class+load` yoki `VM.classloader_stats` bilan izlash kerak bo'ladi.

Ikkinchi savol statik qismga tegishli. Sinfning hamma statik initializatori va statik maydon initsializatorlari bitta `<clinit>` metodiga, matn tartibida yig'iladi (*The Java Virtual Machine Specification, Java SE 25*, 2.9.2, 26-bet). Shundan ikki narsa chiqadi: statik blok bilan statik maydonning tartibi faylda yozilgan tartib bo'lib qoladi (pastdagi blok yuqoridagi maydonni ko'radi, teskarisi yo'q), va butun statik qism bitta amal sifatida, bitta qulf ostida bajariladi. Har bir sinf uchun alohida initsializatsiya qulfi bor va JVM shu qulf bilan bir vaqtdagi hamda rekursiv initsializatsiyani boshqaradi (*The Java Language Specification, Java SE 25*, 12.4.2, 449-bet).

Shu qulfning ikki oqibati amalda og'riq beradi. Birinchi: ikki thread bir-biriga murojaat qiladigan ikki sinfni bir vaqtda ishga tushirsa, klassik aylana deadlock chiqadi, va u oddiy deadlock dan yomonroq, chunki thread dump da `BLOCKED` emas, sinf initsializatsiyasini kutish holati ko'rinadi va kod ichida hech qanday `synchronized` yo'q. Ikkinchi: bitta thread o'zi ishga tushirayotgan sinfni rekursiv so'rasa, deadlock bo'lmaydi (spetsifikatsiya bu holatni "rekursiv so'rov" deb tanib, qulfni bo'shatib normal davom etadi), lekin shu threadga sinf YARIM ishga tushgan holatda ko'rinadi: statik maydonlarning bir qismi hali default qiymatda (`null`, `0`) bo'ladi.

```java
// Ikki sinf bir-birini statik initsializatsiyada chaqiradi.
class Registry {
    static final Map<String, Handler> ALL = Loader.buildAll();   // Loader ni ishga tushiradi
}

class Loader {
    static final int LIMIT = Registry.ALL.size();                // Registry ni ishga tushiradi

    static Map<String, Handler> buildAll() { return Map.of(); }
}

// Bitta thread: deadlock yo'q, lekin LIMIT yoki ALL yarim initsializatsiya qilingan
// holatda o'qiladi va natija jim noto'g'ri bo'ladi.
// Ikki thread Registry va Loader ni bir vaqtda birinchi marta ishlatsa: deadlock.
```

Shundan amaliy qoida: statik initsializatorda boshqa sinfning statik a'zosiga tegmaslik, ayniqsa o'zaro bog'liq sinflar orasida; statik blokda I/O, tarmoq va `ExecutorService` ga vazifa yuborish qilmaslik; ishga tushish tartibini sinfning statik qismiga emas, konteynerning hayot sikliga (`@PostConstruct`, `SmartLifecycle`) bermaslik. Spring da bu qoida tabiiy bajariladi, chunki bean grafini konteyner quradi, lekin statik `Holder` va statik registrlar bu himoyadan tashqarida qoladi.

## 9.13 Amalda qo'llash

- [ ] Har bir servis uchun `jcmd VM.native_memory summary` chiqarib, heap tashqarisidagi xotirani hisoblang va `MaxRAMPercentage` ni shunga qarab 65 dan 75 foizga qo'ying.
- [ ] GC log, `HeapDumpOnOutOfMemoryError` va JFR ni barcha production profilga doimiy yoqib, dump papkasini mount qiling.
- [ ] `-Xlog:class+load=info` bilan bitta start ni yozib, duplikat class va keraksiz jar larni aniqlang, dependency tree tekshiruvini CI ga qo'shing.
- [ ] Fat jar ni `-Djarmode=tools ... extract` bilan qatlamlarga bo'lib, Docker image ni dependency va kod qatlamlariga ajratib qurishga o'tkazing.
- [ ] Bitta servisda CDS arxivi tayyorlab, start vaqtini arxivsiz holat bilan taqqoslang va natijani o'lchov sifatida yozib qo'ying.
- [ ] `-Xlog:deoptimization=info` ni staging da yuklama testi vaqtida yoqib, eng ko'p takrorlanadigan deoptimizatsiya sabablarini ro'yxatga oling.
- [ ] Kubernetes manifestlariga `startupProbe`, graceful shutdown va bosqichli trafik berishni qo'shib, deploy paytidagi p99 sakrashini o'lchang.
- [ ] Umumiy mutable holat ishlatadigan har bir class ni ko'rib chiqib, uni immutable ga, `volatile` ga yoki `java.util.concurrent` strukturasiga o'tkazish bo'yicha qaror yozib qo'ying.

## Manbalar

- Craig Walls, *Spring in Action* 6th, 1-bob - DevTools ning ikki class loader bilan avtomatik restarti va dependency o'zgarishidagi chegarasi
- [OpenJDK 25, `java.util.concurrent` package javadoc](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/util/concurrent/package-info.java) - happens-before munosabati va memory model ning amaliy ko'rinishi
- [OpenJDK 25, `VirtualThread.java`](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/lang/VirtualThread.java) - thread holat mashinasi va mount/unmount mexanikasi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 17.5.3 (799-800-betlar) - `final` maydonni konstruktordan keyin reflection yoki deserializatsiya bilan o'zgartirishning yagona mantiqiy shakli: obyekt barcha yangilanish tugamaguncha boshqa threadlarga ko'rinmasligi va maydonlari o'qilmasligi; freeze nuqtasining konstruktor oxirida va har bir keyingi o'zgartirishdan keyin yuzaga kelishi; constant expression bilan initsializatsiya qilingan maydondagi o'zgarishning kompilyatsiya vaqtidagi inline sabab ko'rinmasligi; `final` maydon o'qishlarini konstruktorda bo'lmagan o'zgartirishlar bilan qayta tartiblashga ruxsat va natijaning -1, 0 yoki 1 bo'lishi (17.5.3-1-misol)
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 12.4.1 (446-448-betlar) va 12.4.2 (449-bet) - sinf yoki interfeys initsializatsiyasini boshlaydigan to'rt hodisa va constant variable ning istisno ekani; sinf ishga tushganda superklasslar va `default` metodli superinterfeyslarning ishga tushishi, interfeysning superinterfeyslarini ishga tushirmasligi; statik maydonga voris sinf nomi bilan murojaatning faqat e'lon qilgan sinfni ishga tushirishi (`Sub.taxi` misoli); har bir sinf uchun alohida initsializatsiya qulfi, boshqa thread initsializatsiya qilayotganda kutish va rekursiv so'rovda qulfni bo'shatib normal davom etish
- *The Java Virtual Machine Specification, Java SE 25 Edition* (Lindholm, Yellin, Bracha, Buckley, Smith), 2.9.2 (26-bet), 4.7.24 (175-bet), 5.3 (365-bet) va 5.5 (397-bet) - statik initializator va statik maydon initsializatorlarining bitta `<clinit>` metodiga matn tartibida yig'ilishi; `MethodParameters` atributi bo'lmasa parametr nomlarining class faylda saqlanmasligi; sinf o'zligining `(binar nom, aniqlovchi loader)` juftligi bilan aniqlanishi, ish vaqtidagi paketning paket nomi va loader bilan aniqlanishi, yaxshi yozilgan loader ning uch xossasi va yuklash xatosining sinf ishlatilgan nuqtada tashlanishi; initsializatsiyaning voris ishga tushganda va `default` metodli interfeys uchun implementatsiya qiluvchi sinf ishga tushganda boshlanishi, hamda bootstrap metod sinfining `invokedynamic` ni hal qilish paytida ishga tushishi
- ESLATMA: `Config`/`DevConfig` va `Registry`/`Loader` misollari hamda ulardan chiqadigan Spring konteksti (statik `Holder` va registrlarning konteyner hayot siklidan tashqarida qolishi, `-parameters` flagining Spring bog'lanishiga ta'siri) korpusning qo'shimchasi: spetsifikatsiyalar qoidani beradi, bu kod shakllari va amaliy xulosalar shu korpusda yozilgan
- [OpenJDK 25, `gc_globals.hpp`](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/hotspot/share/gc/shared/gc_globals.hpp) - heap va GC bilan bog'liq bayroqlarning haqiqiy defaultlari
- [OpenJDK 25, `ForkJoinPool.java`](https://raw.githubusercontent.com/openjdk/jdk/jdk-25%2B36/src/java.base/share/classes/java/util/concurrent/ForkJoinPool.java) - `commonPool` ning yadro soniga bog'lanishi

---

[&larr; 8. Ishlash va resurs hissi: napkin math](08-ishlash-va-resurs-hissi-napkin-math.md) · [Mundarija](README.md) · [10. Garbage collection va xotira sozlash &rarr;](10-garbage-collection-va-xotira-sozlash.md)
