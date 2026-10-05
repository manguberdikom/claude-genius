<!-- doc: architect | chapter: 34 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyyasi](README.md)

# 34. Legacy kod va bosqichma-bosqich refaktoring (Legacy Code and Refactoring)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [34.1 Legacy kodga birinchi kun: o'qish, o'lchash, hech narsani o'zgartirmaslik](#341-legacy-kodga-birinchi-kun-oqish-olchash-hech-narsani-ozgartirmaslik)
- [34.2 Tizimni tushunish usullari: kirish nuqtalari, ma'lumot oqimi, eng ko'p o'zgargan fayllar](#342-tizimni-tushunish-usullari-kirish-nuqtalari-malumot-oqimi-eng-kop-ozgargan-fayllar)
- [34.3 Xavfsizlik to'ri qurish: xatti-harakatni qayd etuvchi test](#343-xavfsizlik-tori-qurish-xatti-harakatni-qayd-etuvchi-test)
- [34.4 Chok (seam) topish: o'zgarishni kiritish mumkin bo'lgan nuqta](#344-chok-seam-topish-ozgarishni-kiritish-mumkin-bolgan-nuqta)
- [34.5 Kichik qadamlar: har bir qadamdan keyin ishlaydigan tizim](#345-kichik-qadamlar-har-bir-qadamdan-keyin-ishlaydigan-tizim)
- [34.6 Katta qayta yozish nega deyarli har doim muvaffaqiyatsiz bo'ladi](#346-katta-qayta-yozish-nega-deyarli-har-doim-muvaffaqiyatsiz-boladi)
- [34.7 Bo'g'uvchi anjir (strangler) usuli bilan bosqichma-bosqich almashtirish](#347-boguvchi-anjir-strangler-usuli-bilan-bosqichma-bosqich-almashtirish)
- [34.8 Ma'lumotlar bazasini ajratish: eng qiyin qism va uning tartibi](#348-malumotlar-bazasini-ajratish-eng-qiyin-qism-va-uning-tartibi)
- [34.9 Refaktoringni biznes bilan kelishish: qiymat tilida tushuntirish](#349-refaktoringni-biznes-bilan-kelishish-qiymat-tilida-tushuntirish)
- [34.10 O'lchov: refaktoring ishladimi yoki yo'qligini qanday bilish](#3410-olchov-refaktoring-ishladimi-yoki-yoqligini-qanday-bilish)
- [34.11 Qachon tegmaslik kerak: ishlayotgan, o'zgarmaydigan kod](#3411-qachon-tegmaslik-kerak-ishlayotgan-ozgarmaydigan-kod)
- [34.12 Bosqichma-bosqich reja namunasi: to'lov moduli misolida](#3412-bosqichma-bosqich-reja-namunasi-tolov-moduli-misolida)
- [34.13 Amalda qo'llash](#3413-amalda-qollash)

</details>



Legacy kod degani eski kod emas. Legacy kod degani siz uning xatti-harakatini isbotlay olmaydigan kod. Shu ta'rifdan bitta amaliy xulosa chiqadi: refaktoring kodni o'zgartirishdan emas, kodning hozirgi xatti-harakatini qayd etishdan boshlanadi. Bu bobda arxitektor legacy tizimga kirib, uni to'xtatmasdan bosqichma-bosqich almashtirish ketma-ketligi ko'rib chiqiladi.

## 34.1 Legacy kodga birinchi kun: o'qish, o'lchash, hech narsani o'zgartirmaslik

Birinchi kunning maqsadi bitta: tizimni ishlab turgan holda ko'rish. "Kichik tozalash" qilinmaydi, chunki siz hali qaysi g'alati kod atayin yozilganini bilmaysiz. `OrderService` ichidagi tushunarsiz `if (status == 7 && legacyFlag)` sharti ko'pincha 2019 yildagi real incident'ning yechimi bo'lib chiqadi.

Birinchi kunda uchta narsa yig'iladi: build qanday ishlaydi, ilova qanday ko'tariladi, va production'da qaysi kod aslida chaqiriladi. Uchinchisi eng qimmatli. Spring Boot'da bu `actuator` metrikalari va log'lar orqali ko'rinadi.

```bash
# Build va ishga tushish vaqtini o'lchaymiz, keyin taqqoslash uchun asos bo'ladi
./mvnw -q -DskipTests package   # taxminan 40-90 s bo'lsa normal
# Bean'lar soni: konteyner kattaligi haqida birinchi raqam
curl -s localhost:8080/actuator/beans | jq '[.contexts[].beans | keys[]] | length'
# Eng sekin endpoint'lar: bu refaktoring uchun birinchi nomzodlar ro'yxati
curl -s localhost:8080/actuator/metrics/http.server.requests \
  | jq '.availableTags[] | select(.tag=="uri") | .values'
```

Birinchi kun oxirida sizda o'zgarish emas, o'lchov bo'lishi kerak: startup vaqti, bean soni, eng ko'p chaqirilgan 10 endpoint, eng sekin 10 SQL. Shu raqamlar keyinchalik "yaxshilandi" degan gapni dalilga aylantiradi.

## 34.2 Tizimni tushunish usullari: kirish nuqtalari, ma'lumot oqimi, eng ko'p o'zgargan fayllar

Legacy tizimni to'liq o'qib chiqish mumkin emas. 400 ming qatorli monolitda o'qish tartibi kerak: kirish nuqtalari, ma'lumot oqimi va o'zgarish tarixi.

Kirish nuqtalari deganda HTTP controller'lar, Kafka listener'lar, `@Scheduled` job'lar va JMS consumer'lar tushuniladi. Ularning soni odatda butun kod bazasining 2 foizidan kam, lekin tizim nima qilishini to'liq belgilaydi.

```bash
# Kirish nuqtalari xaritasi: tizim tashqi dunyo bilan qayerda gaplashadi
grep -rln --include=*.java -E '@(RestController|Controller)' src/main/java | wc -l
grep -rn --include=*.java -E '@(KafkaListener|RabbitListener|JmsListener)' src/main/java
grep -rn --include=*.java '@Scheduled' src/main/java

# O'zgarish tarixi: oxirgi 2 yilda eng ko'p tegilgan fayllar
git log --since="2 years ago" --name-only --pretty=format: \
  | grep '\.java$' | sort | uniq -c | sort -rn | head -30
```

Oxirgi buyruq eng muhim ro'yxatni beradi. Tez-tez o'zgaradigan va katta fayl, ya'ni yuqori churn va yuqori murakkablik kesishgan joy, aynan refaktoringdan foyda chiqadigan nuqta. Kamdan kam tegiladigan katta fayl esa odatda tinch qoldiriladi.

Ma'lumot oqimini tushunish uchun jadval darajasiga tushish kerak. PostgreSQL'da qaysi jadval haqiqatan ishlatilayotgani statistikadan ko'rinadi.

```sql
-- Jadvallar bo'yicha haqiqiy yuklama: o'qish va yozish nisbati
SELECT relname,
       seq_scan, idx_scan,
       n_tup_ins AS qoshildi,
       n_tup_upd AS ozgardi,
       n_tup_del AS ochirildi,
       pg_size_pretty(pg_total_relation_size(relid)) AS hajm
FROM pg_stat_user_tables
ORDER BY (coalesce(idx_scan,0) + seq_scan) DESC
LIMIT 20;

-- Umuman ishlatilmayotgan index'lar: ortiqcha yozish narxi
SELECT relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

Agar `pg_stat_statements` extension yoqilgan bo'lsa, `total_exec_time` bo'yicha tartiblangan birinchi 20 so'rov tizimning haqiqiy og'irlik markazini ko'rsatadi. Odatda butun yuklamaning 80 foizi 10 ta so'rovga tegishli bo'ladi.

## 34.3 Xavfsizlik to'ri qurish: xatti-harakatni qayd etuvchi test

Characterization test oddiy testdan maqsadi bilan farq qiladi. Oddiy test "kod to'g'ri ishlashini" tekshiradi. Characterization test "kod hozir nima qilayotganini" yozib oladi, hatto u noto'g'ri bo'lsa ham. Bu farq muhim, chunki legacy tizimda noto'g'ri xatti-harakat ham ko'pincha mijoz ishonib qolgan xatti-harakatdir.

Amalda bu shunday ketadi: kutilgan natijani o'zingiz o'ylab topmaysiz, kodni ishga tushirib, chiqqan natijani kutilgan deb qayd etasiz. Keyin shu qayddan chetga chiqish regressiya hisoblanadi. Masalan to'lov komissiyasini hisoblash uchun 200 ta real buyurtma ID'si olinadi, eski kod natijasi fayl sifatida saqlanadi, refaktoringdan keyin natija aynan shu fayl bilan taqqoslanadi. Texnikaning o'zi [testlash qo'llanmasidagi](../testing/README.md) mos bo'limda ko'rsatilgan, bu yerda faqat tartib muhim.

Arxitektor uchun qoida: characterization test production trafigidan olingan ma'lumotga asoslansin. Sun'iy ma'lumot legacy tizimning eng qiziq holatlarini qamramaydi, chunki legacy tizimning qiymati aynan o'sha g'alati holatlarda yashaydi. Masalan 2016 yilgi valyuta kursi bilan yozilgan buyurtmalar yoki `NULL` yetkazib berish manzili bilan yopilgan to'lovlar.

## 34.4 Chok (seam) topish: o'zgarishni kiritish mumkin bo'lgan nuqta

Seam deganda kod xatti-harakatini o'sha joyni tahrirlamasdan o'zgartirish mumkin bo'lgan nuqta tushuniladi. Spring ilovasida seam'lar odatda topish oson, chunki konteyner o'zi almashtirish mexanizmini beradi.

Amaliy seam turlari: interface orqali inject qilingan dependency, `@Bean` metodi, `@ConditionalOnProperty` bilan boshqariladigan konfiguratsiya, HTTP client abstraksiyasi, va `ApplicationEventPublisher`. Eng yomon holat esa `new PaymentGateway()` yoki `static` utility chaqiruvi, u yerda seam yo'q va avval uni yaratish kerak.

```java
// OLDIN: seam yo'q, kodni test ham, almashtirish ham mumkin emas
public class PaymentService {
    public Receipt charge(Order order) {
        var gateway = new AcquirerGateway("https://acq.example.com"); // qotib qolgan
        return gateway.charge(order.total());
    }
}

// KEYIN: minimal o'zgarish bilan seam yaratildi, mantiq tegilmadi
public class PaymentService {
    private final AcquirerClient client; // interface, almashtirish mumkin

    public PaymentService(AcquirerClient client) { this.client = client; }

    public Receipt charge(Order order) {
        return client.charge(order.total()); // xatti-harakat aynan o'sha
    }
}
```

Bu o'zgarishda mantiq bir qatorga ham tegilmadi. Faqat bog'lanish ko'chirildi. Shu turdagi qadam eng xavfsizi, chunki uni IDE avtomatik bajaradi va diff'ni o'qish oson.

## 34.5 Kichik qadamlar: har bir qadamdan keyin ishlaydigan tizim

Refaktoringning asosiy intizomi shu: har bir commit'dan keyin tizim deploy qilinishi mumkin bo'lsin. Bu "yarim ishlangan" holatni umuman yo'q qiladi. Agar qadam shunday bo'lishi mumkin bo'lmasa, qadam juda katta.

Katta o'zgarishni kichiklarga bo'lish uchun asosiy vosita feature flag va parallel ishlash. Yangi kod yoziladi, lekin dastlab u faqat soya rejimida ishlaydi: natijasini hisoblaydi, log'ga yozadi, lekin javob eski koddan qaytadi.

```java
@Service
public class FeeCalculationFacade {
    private final LegacyFeeCalculator legacy;
    private final NewFeeCalculator fresh;
    private final boolean shadow;      // soya rejimi yoqilganmi
    private final boolean useNew;      // javob qaysi koddan qaytadi

    public Money fee(Order order) {
        Money old = legacy.fee(order);
        if (shadow) {
            try {
                Money neu = fresh.fee(order);
                if (!neu.equals(old)) {
                    log.warn("fee farqi order={} eski={} yangi={}",
                             order.id(), old, neu); // farqlar metrikaga ham chiqadi
                }
                if (useNew) return neu;
            } catch (RuntimeException e) {
                log.error("yangi hisob xato berdi, eski javob qaytadi", e);
            }
        }
        return old;
    }
}
```

Soya rejimini bir hafta ishlatib, farqlar soni nolga tushganda `useNew` yoqiladi. Bu yerda muhim detal: yangi kodning exception'i mijozga chiqmasligi kerak, aks holda soya rejimi o'zi incident manbasiga aylanadi.

| Qadam | Hajm | Deploy mumkinmi | Qaytarish narxi |
|---|---|---|---|
| Interface ajratish | 1-2 fayl | Ha | Revert, 1 daqiqa |
| Metodni ko'chirish | 2-4 fayl | Ha | Revert, 1 daqiqa |
| Soya rejimi qo'shish | 3-5 fayl | Ha | Flag o'chirish, 0 daqiqa |
| Trafikni yangiga o'tkazish | 0 fayl | Ha | Flag o'chirish, 0 daqiqa |
| Eski kodni o'chirish | 5-20 fayl | Ha | Revert, 5 daqiqa |
| Jadvalni ikkiga bo'lish | migratsiya | Shartli | Backfill qayta, soatlar |
| Butun modulni qayta yozish | 100+ fayl | Yo'q | Amalda imkonsiz |

## 34.6 Katta qayta yozish nega deyarli har doim muvaffaqiyatsiz bo'ladi

Noldan qayta yozish uch sababdan qulaydi. Birinchisi, eski tizim turib qolmaydi. Siz 9 oy yangi versiyani yozganda, eski tizimga yana 300 ta o'zgarish kiradi va maqsad harakatlanadi.

Ikkinchi sabab bilimning taqsimlanishi. Legacy kodning qiymati arxitekturasida emas, o'n yil davomida yig'ilgan mayda shartlarida. Ular hujjatlashtirilmagan. Qayta yozishda ularning 10-20 foizi yo'qoladi va har biri alohida incident bo'lib qaytadi.

Uchinchi sabab iqtisodiy: qayta yozish davomida biznes qiymat olmaydi. 6 oydan keyin yangi funksiya so'rovi kelganda jamoa ikki joyda ishlashga majbur bo'ladi va ikkalasi ham sekinlashadi.

Qayta yozish asosli bo'lgan kam holatlar bor: platforma umuman qo'llab-quvvatlanmaydi, masalan Java 6 va EJB 2 ustidagi tizim; yoki modul juda kichik va chiqish nuqtalari aniq, masalan bitta hisobot generatori. Ikkinchi holatda bu qayta yozish emas, modul almashtirish.

## 34.7 Bo'g'uvchi anjir (strangler) usuli bilan bosqichma-bosqich almashtirish

Strangler yondashuvining mohiyati: yangi tizim eski tizim atrofida o'sadi va trafikni asta-sekin o'ziga tortadi. Eski tizim bitta katta kunda o'chirilmaydi, u funksiya ortidan funksiya bo'shab, oxirida bo'sh qobiq bo'lib qoladi.

Texnik asosi routing qatlami. Spring Cloud Gateway yoki oddiy nginx yetarli. Qoida yo'l bo'yicha emas, imkon qadar mijoz segmenti bo'yicha ham yozilsin, shunda yangi kod avval kichik trafikni ko'radi.

```yaml
# Gateway: /api/v1/payments faqat belgilangan header bilan yangi servisga ketadi
spring:
  cloud:
    gateway:
      routes:
        - id: payments-new
          uri: http://payment-service:8080
          predicates:
            - Path=/api/v1/payments/**
            - Header=X-Canary, true        # boshida 1-5% trafik
          filters:
            - name: CircuitBreaker
              args:
                name: paymentsCb
                fallbackUri: forward:/legacy/payments  # xato bo'lsa eskiga qaytadi
        - id: payments-legacy
          uri: http://monolith:8080
          predicates:
            - Path=/api/v1/payments/**     # qolgan hamma trafik
```

Trafikni bosqichlab oshirish tartibi odatda shunday: 1 foiz bir kun, 5 foiz uch kun, 25 foiz bir hafta, 50 foiz bir hafta, 100 foiz. Har bosqichda error rate va p99 latency taqqoslanadi. Oldingi bosqichga qaytish bitta konfiguratsiya o'zgarishi bo'lib qolishi shart.

## 34.8 Ma'lumotlar bazasini ajratish: eng qiyin qism va uning tartibi

Kodni bo'lish oson, bazani bo'lish qiyin. Sababi aniq: monolitda `orders` va `payments` jadvallari bitta tranzaksiyada yangilanadi va bitta `JOIN` bilan o'qiladi. Ajratilgandan keyin ikkalasi ham yo'qoladi.

To'g'ri tartib quyidagicha. Avval kod darajasida ajratish: har bir jadvalga faqat bitta modul yozsin, boshqalar API orqali so'rasin. Keyin `JOIN`'larni yo'qotish. Keyin schema'ni ajratish, lekin bazani bitta qoldirish. Va faqat oxirida alohida baza instance'i.

```sql
-- 1-qadam: mantiqiy ajratish, baza hali bitta
CREATE SCHEMA payment;
ALTER TABLE public.payments SET SCHEMA payment;

-- 2-qadam: faqat payment moduli yozish huquqiga ega bo'ladi
REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA payment FROM monolith_app;
GRANT  SELECT ON payment.payments TO monolith_app;  -- vaqtinchalik o'qish

-- 3-qadam: o'qish ham API orqali bo'lganda ruxsat umuman olinadi
REVOKE SELECT ON payment.payments FROM monolith_app;
```

Tranzaksiya chegarasi buzilgan joyda ikkita yozishni bitta `@Transactional` ushlab turolmaydi. Bu yerda outbox orqali ishonchli xabar yuborish kerak bo'ladi, mexanikasi dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern bo'limida bor. Arxitektorning qarori esa boshqa: qaysi joy eventual consistency'ga chidaydi. To'lov holati va buyurtma holati orasida 2-5 sekund kechikish odatda qabul qilinadi, pul qoldig'i va yechib olish orasida esa yo'q.

| Tuzoq | Natijasi | Yechim |
|---|---|---|
| Bazani avval ajratib, keyin kodni bo'lish | Ikki baza orasida distributed JOIN | Avval kod, keyin schema, oxirida instance |
| Backfill'ni bir marta katta `UPDATE` bilan qilish | Jadval lock, soatlab kutish | 5-10 ming qatorli batch, har batchdan keyin commit |
| Ikki tomonga yozib, hech qachon tekshirmaslik | Jim ketadigan ma'lumot tafovuti | Har kecha hisoblash: farq soni metrikaga chiqsin |
| Eski ustunni darhol `DROP` qilish | Rollback imkonsiz | Avval ishlatishni to'xtatish, 2 sprint kutish, keyin drop |
| Yangi kodda eski jadvalga to'g'ridan-to'g'ri yozish | Egalik chegarasi buzildi | Baza darajasida `REVOKE`, qoida kodga tayanmasin |
| `Flyway` migratsiyasini orqaga qaytarishga umid qilish | Qaytarish skripti sinovdan o'tmagan | Faqat oldinga mos migratsiya: ustun qo'shish, to'ldirish, o'tish |
| Soya rejimini ikki hafta ortiq ushlab turish | Ikki marta xarajat, chalkashlik | Flag uchun muddat belgilansin, muddatdan keyin yoki o'ting yoki qaytaring |

## 34.9 Refaktoringni biznes bilan kelishish: qiymat tilida tushuntirish

"Kod iflos" degan dalil byudjet ochmaydi. Ochadigan dalil vaqt va xavf tilida yoziladi. Masalan: "to'lov modulidagi har bir o'zgarish hozir 9 kun oladi, shundan 5 kuni qo'lda regressiya tekshiruvi. Chok ajratilgandan keyin bu 3 kunga tushadi. Yiliga 20 ta o'zgarish bo'lsa, 120 ish kuni tejaladi."

Ikkinchi ishonchli dalil incident statistikasi. Agar oxirgi 12 oyda production incident'larning 40 foizi bitta modulda bo'lgan bo'lsa, bu modul refaktoringi xavfni kamaytirish loyihasi sifatida tushuntiriladi.

Kelishuvning amaliy shakli: alohida "refaktoring sprint'i" so'ralmaydi. Har sprintning 15-20 foizi tizimni ishlashga yaroqli saqlashga ajratiladi va bu doimiy bo'ladi. Bitta katta so'rov bir marta rad etiladi, kichik doimiy ulush esa odatga aylanadi.

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| "Bu kod juda yomon, qayta yozamiz" | "Bu modul o'zgarish narxini 3 barobar oshiradi, bosqichma-bosqich almashtiramiz" |
| Refaktoringni mantiq o'zgarishi bilan birga commit qiladi | Xatti-harakat o'zgarmaydigan commit va mantiq commit'i ajratiladi |
| Avval tozalaydi, keyin o'lchaydi | Avval o'lchaydi, keyin faqat o'lchov ko'rsatgan joyni tozalaydi |
| Butun kod bazasini bir xil darajada yaxshilaydi | Yuqori churn joyga kuch beradi, tinch joyga tegmaydi |
| Bazani birinchi bo'lib bo'ladi | Kodni va egalikni birinchi bo'lib bo'ladi, baza oxirida |
| Yangi kodni darhol production javobiga qo'yadi | Soya rejimida taqqoslaydi, farq nolga tushgach o'tadi |
| Flag'larni cheksiz qoldiradi | Har flag uchun o'chirish muddati va egasi bo'ladi |
| "Yaxshilandi" deb his bilan aytadi | p99 latency, o'zgarish vaqti, incident soni raqamini ko'rsatadi |
| Eski kodni "ehtimol kerak bo'ladi" deb saqlaydi | Trafik nolga tushganini metrikada ko'rib, o'chiradi |

## 34.10 O'lchov: refaktoring ishladimi yoki yo'qligini qanday bilish

Refaktoring natijasi kod chiroyliligi bilan o'lchanmaydi. To'rt turdagi raqam ishlaydi: tezlik, xavf, ish narxi va ishlash ko'rsatkichi.

Ish narxi tomonidan eng oddiy ko'rsatkich lead time: PR ochilishidan production'ga chiqishigacha o'tgan vaqt. Refaktoringdan oldin 6-9 kun bo'lsa, keyin 2-3 kunga tushishi kutiladi. Ikkinchi ko'rsatkich change failure rate: deploy'lardan qanchasi rollback bilan tugaydi.

```bash
# Modul bo'yicha o'zgarish zichligi: refaktoringdan oldin va keyin taqqoslanadi
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '^src/main/java/com/shop/payment/' | sort -u | wc -l

# Modulga tegadigan commit'lar soni va o'rtacha diff hajmi
git log --since="6 months ago" --numstat --pretty='C' -- src/main/java/com/shop/payment/ \
  | awk '/^C/{c++} /^[0-9]/{a+=$1; d+=$2} END{printf "commit=%d +%d -%d ortacha=%.1f\n", c, a, d, (a+d)/c}'
```

Ishlash tomonidan `http.server.requests` p99 va baza so'rovlari soni kuzatiladi. Keng tarqalgan hodisa: kod toza, lekin N+1 so'rov paydo bo'lgan va p99 ikki barobar o'sgan. Shuning uchun har bosqichda so'rov soni ham o'lchanadi.

Kod sifati metrikalaridan faqat ikkitasi foydali: modullar orasidagi bog'liqlik yo'nalishi va aylanma bog'liqliklar soni. Ikkisini ham ArchUnit qoidalari bilan qulflash mumkin, batafsili [testlash qo'llanmasidagi](../testing/README.md) arxitektura qoidalari bo'limida.

## 34.11 Qachon tegmaslik kerak: ishlayotgan, o'zgarmaydigan kod

Refaktoring qilmaslik ham qaror. Agar modul oxirgi 18 oyda o'zgarmagan, incident bermagan va performance muammosi yo'q bo'lsa, uning ichidagi kod qanday ko'rinishi ahamiyatsiz. Uni tozalash sof xarajat va yangi xato manbasi.

Tegmaslik mezonlari aniq: past churn, nol incident, latency byudjet ichida, yaqin yo'l xaritasida o'zgarish yo'q. Shu to'rt shart bajarilsa, modul "muzlatilgan" deb belgilanadi va faqat xavfsizlik yangilanishlari oladi.

Alohida holat: kod yomon, lekin uni o'rab olish mumkin. Masalan 3000 qatorli hisobot generatori. Uni qayta yozish o'rniga oldiga toza interface qo'yiladi, atrofidagi kod shu interface'ga tayanadi, ichi esa qora quti bo'lib qoladi. Shunda kelgusida uni almashtirish kerak bo'lsa, faqat bitta interface implementatsiyasi yoziladi.

## 34.12 Bosqichma-bosqich reja namunasi: to'lov moduli misolida

Quyidagi reja monolitdagi to'lov modulini alohida servisga chiqarish uchun real ketma-ketlik. Har bosqich oxirida tizim ishlaydi va orqaga qaytish yo'li bor.

Birinchi bosqich, bir hafta: o'lchov. To'lov bilan bog'liq endpoint'lar, Kafka listener'lar va `@Scheduled` job'lar ro'yxati; `payments` jadvaliga kim yozayotganini `grep` va baza grant'lari bo'yicha aniqlash; p99 va kunlik hajm raqamlari.

Ikkinchi bosqich, ikki hafta: characterization testlar. Production'dan olingan 500 ta to'lov holati uchun hozirgi natija qayd etiladi, shu qatorda rad etilgan va qaytarilgan to'lovlar.

Uchinchi bosqich, ikki hafta: modul chegarasini monolit ichida chizish. Barcha to'lov mantiqi bitta paketga ko'chiriladi, tashqi kod faqat `PaymentFacade` orqali murojaat qiladi, bazaga to'g'ridan-to'g'ri murojaatlar yo'qotiladi.

```java
// Modul chegarasi: tashqi dunyo faqat shu interface'ni ko'radi
public interface PaymentFacade {
    PaymentResult authorize(OrderId orderId, Money amount);
    void capture(PaymentId paymentId);
    void refund(PaymentId paymentId, Money amount, String reason);
    Optional<PaymentView> find(PaymentId paymentId);
}
// ArchUnit qoidasi: payment.internal paketiga tashqaridan murojaat taqiqlanadi.
// Shu qoida buzilmasa, keyingi bosqichda servisga chiqarish mexanik ish bo'ladi.
```

To'rtinchi bosqich, bir hafta: schema ajratish va grant'lar. Beshinchi bosqich, uch hafta: yangi servis ko'tariladi, `PaymentFacade` implementatsiyasi HTTP client bo'ladi, soya rejimida ishlaydi. Oltinchi bosqich, ikki hafta: canary 1 foizdan 100 foizga. Yettinchi bosqich, bir hafta: monolitdagi eski kod va grant'lar o'chiriladi.

Jami taxminan 12-14 hafta, bitta kichik jamoa uchun. Muhimi muddat emas, balki har bosqich oxirida tizim ishlashi va rollback bitta flag yoki bitta revert bo'lib qolishi.

## 34.13 Amalda qo'llash

- [ ] `git log --name-only` asosida oxirgi 2 yilda eng ko'p o'zgargan 30 faylni chiqarib, ularning hajmi bilan jadval tuzing va refaktoring nomzodlarini belgilang.
- [ ] `pg_stat_user_tables` va `pg_stat_statements` bo'yicha eng og'ir 20 so'rovni va ishlatilmayotgan index'larni yozib oling, bu refaktoringdan oldingi asos bo'ladi.
- [ ] Tanlangan modulning 3 ta eng muhim stsenariysi uchun production ma'lumotidan characterization qayd fayli tayyorlang.
- [ ] Modulda `new` operatori yoki `static` chaqiruv bilan qotib qolgan 5 ta bog'lanishni toping va ularning o'rniga interface seam qo'ying, mantiqga tegmasdan.
- [ ] Bitta hisoblash mantiqi uchun soya rejimi yoqing: yangi kod natijasi log va metrikaga chiqsin, javob eski koddan qaytsin.
- [ ] Har bir feature flag uchun egasi va o'chirish muddatini yozib qo'ying, muddati o'tgan flag'lar ro'yxati sprint ko'rikida ko'rilsin.
- [ ] `REVOKE` va `GRANT` orqali tanlangan jadvalga yozish huquqini faqat bitta modulga qoldiring, qoidani kodga emas bazaga tayantiring.
- [ ] Refaktoringdan oldin va 3 oydan keyingi lead time, change failure rate va p99 latency raqamlarini bir sahifada taqqoslab, biznes bilan shu hujjat tilida gaplashing.

---

[&larr; 33. Sxema migratsiyasi va to'xtashsiz reliz](33-sxema-migratsiyasi-va-toxtashsiz-reliz.md) · [Mundarija](README.md) · [35. Incident, on-call va post-mortem &rarr;](35-incident-on-call-va-post-mortem.md)
