<!-- doc: architect | chapter: 35 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyyasi](README.md)

# 35. Incident, on-call va post-mortem (Incidents and Post-mortems)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [35.1 Incident darajalari va ularni belgilash mezoni](#351-incident-darajalari-va-ularni-belgilash-mezoni)
- [35.2 Incident paytidagi rollar: boshqaruvchi, tekshiruvchi, aloqachi](#352-incident-paytidagi-rollar-boshqaruvchi-tekshiruvchi-aloqachi)
- [35.3 Birinchi qadam: tiklash, sabab qidirish emas](#353-birinchi-qadam-tiklash-sabab-qidirish-emas)
- [35.4 Tiklash usullari: orqaga qaytarish, flag o'chirish, trafikni yo'naltirish](#354-tiklash-usullari-orqaga-qaytarish-flag-ochirish-trafikni-yonaltirish)
- [35.5 Diagnostika tartibi: nima o'zgardi, qachon boshlandi, nima umumiy](#355-diagnostika-tartibi-nima-ozgardi-qachon-boshlandi-nima-umumiy)
- [35.6 Muloqot: kimga, qanchalik tez-tez, qanday til bilan](#356-muloqot-kimga-qanchalik-tez-tez-qanday-til-bilan)
- [35.7 Incident jurnali va vaqt chizig'ini yozib borish](#357-incident-jurnali-va-vaqt-chizigini-yozib-borish)
- [35.8 Ayblamaydigan post-mortem: tuzilishi va yozish qoidalari](#358-ayblamaydigan-post-mortem-tuzilishi-va-yozish-qoidalari)
- [35.9 Besh marta "nega" va tizimli sabablarga yetish](#359-besh-marta-nega-va-tizimli-sabablarga-yetish)
- [35.10 Harakat bandlari: egasi, muddati, tekshiruvi bo'lsin](#3510-harakat-bandlari-egasi-muddati-tekshiruvi-bolsin)
- [35.11 On-call navbati: adolatli taqsimot, ogohlantirish charchoqini kamaytirish](#3511-on-call-navbati-adolatli-taqsimot-ogohlantirish-charchoqini-kamaytirish)
- [35.12 Ogohlantirishlar sifati: har bir alert bajariladigan ish bo'lsin](#3512-ogohlantirishlar-sifati-har-bir-alert-bajariladigan-ish-bolsin)
- [35.13 To'liq post-mortem namunasi: to'lov servisi uzilishi misolida](#3513-toliq-post-mortem-namunasi-tolov-servisi-uzilishi-misolida)
- [35.14 Amalda qo'llash](#3514-amalda-qollash)

</details>



Incident vaqtida arxitektorning qiymati kod yozishda emas, qarorni tez va to'g'ri chiqarishda ko'rinadi. Tizimni bilgan odam "nega buzildi" savolidan oldin "qanday tiklanadi" savoliga javob beradi. Bu bob darajalash, rollar, tiklash usullari, diagnostika tartibi va ayblamaydigan post-mortem mexanikasini beradi. Oxirida to'lov servisi uzilishi misolida to'liq shablon bor.

## 35.1 Incident darajalari va ularni belgilash mezoni

Daraja texnik emas, biznes ta'siriga qarab belgilanadi. "PostgreSQL replica ortda qoldi" daraja emas, "mijoz to'lovni yakunlay olmaydi" daraja. Mezon uch o'lchovdan tuziladi: qancha foydalanuvchi zarar ko'rdi, pul yoki ma'lumot yo'qolayaptimi, vaqtinchalik yechim bormi. Darajani birinchi javob beruvchi qo'yadi va oshirishga haqli, pasaytirishga esa faqat boshqaruvchi haqli.

Amalda to'rt daraja yetarli. P1: asosiy oqim ishlamaydi yoki pul yo'qolmoqda, javob 5 daqiqa, telefon bilan uyg'otish. P2: oqim qisman ishlaydi yoki jiddiy sekinlashgan, javob 15 daqiqa. P3: ikkilamchi funksiya buzilgan, ish vaqtida hal qilinadi. P4: kosmetik muammo, backlog'ga tushadi. Raqamlar yozib qo'yiladi, aks holda har kim o'z hissi bilan baholaydi.

Darajalash mezoni SLO bilan bog'lanadi. 99.9% availability bir oyda taxminan 43 daqiqa budjet beradi, 99.95% esa taxminan 22 daqiqa. Bitta P1 shu budjetning yarmini yeb qo'ysa, post-mortem majburiy. Budjet tugagan oyda yangi feature chiqarish to'xtatiladi.

## 35.2 Incident paytidagi rollar: boshqaruvchi, tekshiruvchi, aloqachi

Eng ko'p uchraydigan xato: sakkiz injener bir xil log'ni o'qiydi va hech kim qaror qabul qilmaydi. Shuning uchun P1 ochilishi bilan uch rol ovoz chiqarib e'lon qilinadi. Incident boshqaruvchi qaror chiqaradi va ishni taqsimlaydi, o'zi debug qilmaydi. Tekshiruvchi gipotezani sinaydi va o'zgarish kiritadi. Aloqachi ichki va tashqi xabarni yozadi, status page'ni yangilaydi.

Boshqaruvchi klaviaturaga tegmasligi qoida. Uning vazifasi har 10 daqiqada "hozir qanday holat, keyingi qadam nima, kim bajaradi" deb so'rash. Kichik jamoada bitta odam boshqaruvchi va aloqachi bo'lishi mumkin, lekin boshqaruvchi va tekshiruvchi hech qachon bitta odam bo'lmasin.

Rol topshirish ham oshkora bo'ladi: kim kimga nimani topshirgani kanalga yoziladi. Uzoq incidentda har 4 soatda almashish rejalashtiriladi, chunki charchagan odam xato qaror chiqaradi. Eskalatsiya zanjiri oldindan yozilgan bo'ladi: birinchi javob beruvchi, zaxira, so'ngra ma'lumotlar bazasi yoki tarmoq mutaxassisi.

## 35.3 Birinchi qadam: tiklash, sabab qidirish emas

Incident paytida maqsad bitta: ta'sirni to'xtatish. Sababni topish post-mortem ishi. Bu ikkisini aralashtirish eng qimmat xato, chunki sabab izlash daqiqalar emas, soatlar oladi. Oxirgi deploy'dan keyin xato chiqqan bo'lsa, deploy qaytariladi, sabab esa sovuq boshda o'rganiladi.

Bitta istisno bor: tiklash harakati ma'lumotni buzishi mumkin bo'lsa, oldin tushunish kerak. To'lov servisi ikki marta debet qilayotgan bo'lsa, qayta ishga tushirish muammoni yashiradi va buzilgan yozuv qoladi. Bunday holatda birinchi qadam trafikni to'xtatish.

Tartib shunday: ta'sirni cheklash, qaytarish yoki o'chirish, metrika bilan tasdiqlash, keyin tahlil. "Tuzatdim" degan ishonch metrikasiz hech narsa anglatmaydi.

## 35.4 Tiklash usullari: orqaga qaytarish, flag o'chirish, trafikni yo'naltirish

Eng tez tiklash usuli eng kam fikrlash talab qiladigani. Deploy'ni qaytarish tekshirilgan yo'l, shuning uchun birinchi variant. Shart bitta: migratsiya orqaga mos bo'lsin. Yangi versiya ustunni o'chirgan bo'lsa qaytarish ishlamaydi, shuning uchun migratsiya har doim ikki fazaga bo'linadi.

```bash
# Qaysi versiya qachon chiqqanini ko'rish
kubectl rollout history deployment/payment-service -n prod

# Oldingi versiyaga qaytarish, bu eng tez va eng xavfsiz qadam
kubectl rollout undo deployment/payment-service -n prod

# Qaytarish tugashini kuzatish, 120 sekund ichida tugamasa muammo boshqa joyda
kubectl rollout status deployment/payment-service -n prod --timeout=120s

# Ikki versiya orasidagi farqni olish, diagnostika uchun
git log --oneline v2.14.0..v2.15.0 -- src/main/java/com/shop/payment
```

Ikkinchi usul feature flag o'chirish. Flag qaytarishdan tezroq, chunki pod qayta ishga tushmaydi va effekt bir necha sekundda ko'rinadi. Shuning uchun har xavfli o'zgarish flag ostida chiqariladi, flag holati esa tashqi konfiguratsiyadan o'qiladi.

```java
// To'lov yo'nalishini tanlash: flag o'chsa eski, tekshirilgan yo'lga qaytadi.
// Flag qiymati konfiguratsiya serveridan keladi, pod qayta ishga tushmaydi.
@Service
class PaymentRouter {
    private final FeatureFlags flags;
    private final NewGatewayClient newGateway;
    private final LegacyGatewayClient legacyGateway;

    PaymentResult charge(PaymentCommand cmd) {
        // Kill switch: incident paytida birinchi bosiladigan tugma
        if (!flags.enabled("payment.new-gateway")) {
            return legacyGateway.charge(cmd);
        }
        try {
            return newGateway.charge(cmd);
        } catch (GatewayTimeoutException e) {
            // Idempotency key bor, shuning uchun qayta urinish ikki marta debet qilmaydi
            log.warn("yangi gateway timeout, eski yo'lga o'tildi, orderId={}", cmd.orderId());
            return legacyGateway.charge(cmd);
        }
    }
}
```

Uchinchi usul trafikni yo'naltirish. Bitta instansiya buzilsa, uni load balancer'dan chiqarish yetarli, region buzilsa trafik ikkinchi regionga o'tadi. Bu usul faqat oldindan tayyorlangan bo'lsa ishlaydi. Readiness probe shu usulning asosi: pod o'zini "tayyor emas" deb belgilasa, trafik avtomatik boshqa podga ketadi.

## 35.5 Diagnostika tartibi: nima o'zgardi, qachon boshlandi, nima umumiy

Diagnostika uchta savoldan boshlanadi. Birinchi: nima o'zgardi. Incidentlarning katta qismi o'zgarishdan keladi, ya'ni deploy, konfiguratsiya, migratsiya, sertifikat, flag yoki tashqi provayder yangilanishi. Ikkinchi: qachon boshlandi, chunki aniq daqiqa o'zgarish ro'yxatini filtrlaydi. Uchinchi: nima umumiy.

```sql
-- Qachon boshlandi: aktiv so'rovlar va ular nimani kutayotgani
SELECT pid, state, wait_event_type, wait_event,
       now() - query_start AS davomiyligi,
       left(query, 80) AS sorov
FROM pg_stat_activity
WHERE state <> 'idle' AND now() - query_start > interval '5 seconds'
ORDER BY davomiyligi DESC
LIMIT 20;

-- Nima umumiy: eng ko'p vaqt yeyayotgan so'rov shakllari
-- pg_stat_statements kerak, PostgreSQL 15-17 da mean_exec_time millisekundda
SELECT calls, round(mean_exec_time::numeric, 1) AS ortacha_ms,
       round(total_exec_time::numeric / 1000, 1) AS jami_sek,
       left(query, 70) AS sorov
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Kim kimni bloklayapti: lock zanjirining boshi
SELECT blocked.pid AS bloklangan, blocking.pid AS bloklovchi,
       left(blocked.query, 60) AS bloklangan_sorov
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;
```

"Nima umumiy" savoliga javob o'lchovlar bo'yicha kesish bilan topiladi: endpoint, mijoz turi, region, pod, tenant, ma'lumot shakli. Xato bitta podda bo'lsa, bu konfiguratsiya yoki resurs muammosi. Barcha podda bir vaqtda boshlangan bo'lsa, bu umumiy bog'liqlik: ma'lumotlar bazasi, cache, tashqi API yoki tarmoq.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Birinchi topilgan gipotezaga yopishib qolish | Vaqt tig'iz, miya tasdiq izlaydi | Ikki gipotezani yozib, ikkisini ham tekshirish |
| Bir vaqtda uchta o'zgarish kiritish | Har kim o'z fikrini sinaydi | Faqat boshqaruvchi ruxsat bergan bitta o'zgarish |
| Pod qayta ishga tushirish bilan "tuzatish" | Simptom yo'qoladi | Avval heap dump va thread dump olinadi |
| Log'ni grep bilan qidirish | Markazlashgan log yo'q | Trace id bo'yicha so'rovni uchidan uchiga kuzatish |
| Metrikasiz tasdiqlash | Panel yo'q yoki noto'g'ri | Tiklanishni mijoz tomonidagi metrika bilan tasdiqlash |
| Connection pool o'lchamini oshirish | "Pool tugadi" xabari ko'rinadi | Sekin so'rovni topish, pool PostgreSQL ni bo'g'adi |
| Timeout ni cheksiz qilish | Xato yo'qolgandek bo'ladi | Timeout qisqa, qayta urinish budjetli |
| Incidentni erta yopish | Metrika tiklandi, sabab qolgan | 30 daqiqa kuzatuv, keyin yopish |

## 35.6 Muloqot: kimga, qanchalik tez-tez, qanday til bilan

Muloqot ikki yo'nalishli. Ichki kanal injenerlar uchun: texnik, qisqa, gipoteza va natija bilan. Tashqi xabar mijoz uchun: atamasiz, ta'sir va keyingi yangilanish vaqti bilan. Mijozga "connection pool exhausted" deb yozish hech narsa anglatmaydi.

Ritm oldindan belgilanadi. P1 da tashqi yangilanish har 30 daqiqada, ichki holat har 10 daqiqada. Yangi ma'lumot bo'lmasa ham xabar yuboriladi: "tekshirmoqdamiz, keyingi xabar 14:30 da", chunki sukunat eng katta ishonchsizlik beradi. Tashqi xabarda uch element bor: nima ishlamayapti, kim zarar ko'rgan, keyingi yangilanish qachon. Sabab va aybdor yozilmaydi, chunki incident paytidagi taxmin keyin noto'g'ri chiqadi.

Til qoidasi sodda: faktni gipotezadan ajratib yozish. "Error rate 14:05 da 0.2 dan 38 foizga chiqdi" fakt, "menimcha yangi gateway sabab" gipoteza. Ular aralashsa, keyin qo'shilgan odam gipotezani fakt deb o'qiydi.

## 35.7 Incident jurnali va vaqt chizig'ini yozib borish

Vaqt chizig'i incident tugagandan keyin tiklanmaydi, uni real vaqtda yozish kerak. Eng arzon usul: har qaror va o'zgarish kanalga vaqt bilan yoziladi, aloqachi esa oxirida shu kanalni vaqt chizig'iga aylantiradi. Yozuv formati bir xil: vaqt, kim, nima qildi.

Log'da bog'lovchi identifikator bo'lishi shart. Incident id ni MDC ga qo'yish arzon va bitta filtr bilan barcha tegishli yozuvni beradi.

```java
// Incident paytida qo'lda ishga tushirilgan tiklash operatsiyalarini belgilash.
// MDC qiymati Logback pattern'ida %X{incidentId} bilan chiqadi.
public final class IncidentContext {
    private static final String KEY = "incidentId";

    public static <T> T runTagged(String incidentId, Supplier<T> action) {
        MDC.put(KEY, incidentId);
        long boshlandi = System.nanoTime();
        try {
            return action.get();
        } finally {
            // Operatsiya qancha davom etganini vaqt chizig'i uchun yozamiz
            long msek = (System.nanoTime() - boshlandi) / 1_000_000;
            log.info("tiklash operatsiyasi tugadi, davomiyligi={}ms", msek);
            MDC.remove(KEY);
        }
    }
}
```

Vaqt chizig'ida besh nuqta majburiy: muammo boshlanishi, birinchi signal, odam xabardor bo'lishi, birinchi tiklash harakati, to'liq tiklanish. Ular ikki raqamni beradi: aniqlash vaqti va tiklash vaqti. Aniqlash uzun bo'lsa muammo monitoringda, tiklash uzun bo'lsa runbook va avtomatlashtirishda.

## 35.8 Ayblamaydigan post-mortem: tuzilishi va yozish qoidalari

Ayblamaydigan post-mortem odamni emas, tizimni tekshiradi. Bu yumshoqlik emas, aniqlik talabi: jazolanishini bilgan injener faktni yashiradi. Shuning uchun "falonchi noto'g'ri konfiguratsiya qo'ydi" o'rniga "konfiguratsiya qiymati validatsiyasiz deploy qilindi, CI da uni tekshiradigan qadam yo'q edi" deb yoziladi.

Tuzilish barqaror bo'lsa o'qish tez bo'ladi: qisqa xulosa, ta'sir raqamlarda, vaqt chizig'i, sabab tahlili, nega tezroq aniqlanmadi, nega tezroq tiklanmadi, nima yaxshi ishladi, harakat bandlari. Oxirgidan oldingi bo'lim bejiz emas: ishlagan himoyani bilish uni kesib tashlashdan saqlaydi.

Yozish qoidalari qisqa. Ism sabab sifatida ko'rsatilmaydi, rol nomi yetarli. Taxmin "ehtimol" so'zi bilan belgilanadi. Hujjat 5 ish kuni ichida yoziladi. P1 uchun post-mortem majburiy, P2 uchun SLO budjetiga ta'siri bo'lsa majburiy.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Incident darajasi | Xato turi bo'yicha | Biznes ta'siri va SLO budjeti bo'yicha |
| Birinchi harakat | Sababni izlash | Ta'sirni to'xtatish, keyin sabab |
| Rollar | Hamma debug qiladi | Boshqaruvchi, tekshiruvchi, aloqachi ajratilgan |
| Tiklash | Qo'lda tuzatish yoziladi | Qaytarish, flag, trafik yo'naltirish tayyor |
| Muloqot | Tugagandan keyin xabar | Belgilangan ritmda, ta'sir tilida |
| Post-mortem | Kim xato qildi | Qaysi himoya yo'q edi |
| Harakat bandlari | "Ehtiyot bo'lamiz" | Egasi, muddati, tekshiruv usuli bor |
| Alert | Ko'proq alert yaxshi | Har bir alert bajariladigan ish |
| On-call | Eng biladigan odam doim navbatda | Navbat aylanadi, runbook yoziladi |

## 35.9 Besh marta "nega" va tizimli sabablarga yetish

Birinchi topilgan sabab deyarli hech qachon haqiqiy sabab bo'lmaydi. Texnika oddiy: har javobdan keyin yana so'raysiz, toki javob tizim yoki jarayon haqida bo'lgunicha. Nega to'lov ishlamadi: servis gateway javobini 60 sekund kutdi. Nega kutdi: HTTP client timeout qo'yilmagan. Nega qo'yilmagan: client qo'lda yozilgan, markazlashgan builder ishlatilmagan. Nega ishlatilmagan: builder haqida hujjat va avtomatik qoida yo'q. Nega yo'q: bu kod review'ning og'zaki an'anasi edi.

Oxirgi javob harakatga aylanadi: og'zaki an'ana avtomatik qoidaga ko'chadi, chunki avtomatik qoida charchamaydi. Testlash qo'llanmasidagi arxitektura qoidalari bo'limi bunday tekshiruvni yozishni batafsil beradi.

Ikki tuzoq bor. Birinchisi, zanjirning odamga borib to'xtashi: "beparvo edi". Savol davom etishi kerak: nega beparvolik ishlab chiqarishga yetib bordi. Ikkinchisi, bitta zanjir bilan cheklanish. Jiddiy incidentda uch sabab birlashadi: xato kod, yetishmagan alert, mavjud bo'lmagan tiklash yo'li.

## 35.10 Harakat bandlari: egasi, muddati, tekshiruvi bo'lsin

Post-mortem qiymati harakat bandlarida. Bandga to'rt shart: aniq ish, bitta egasi, aniq muddat, tekshiruv usuli. "Monitoringni yaxshilash" band emas. "Gateway p99 latency uchun 2 sekund chegarada alert qo'shish, egasi platform jamoasi, muddat 14 oktabr, tekshiruv sun'iy sekinlashtirish bilan" band.

Bandlar ikki guruhga bo'linadi. Oldini olish bandlari sababga tegadi, masalan timeout ni majburiy qilish. Zararni kamaytirish bandlari tiklash vaqtini qisqartiradi, masalan kill switch qo'shish. Ikkinchi guruh ko'pincha e'tibordan qoladi, lekin aynan u keyingi incidentda qutqaradi.

```yaml
# Harakat bandi natijasi: majburiy timeout va alert chegarasi konfiguratsiyada
spring:
  datasource:
    hikari:
      maximum-pool-size: 20          # PostgreSQL max_connections 200, 6 instansiya
      connection-timeout: 2000       # pool bo'sh bo'lmasa 2 sekundda xato, kutmaydi
      validation-timeout: 1000
      leak-detection-threshold: 20000 # 20 sekund ushlab turilgan connection log'ga tushadi
  jpa:
    properties:
      jakarta.persistence.query.timeout: 3000  # sekin so'rov tranzaksiyani ushlamaydi

management:
  endpoint:
    health:
      show-details: when-authorized
  health:
    db:
      enabled: true
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
```

Backlog'ga tushgan band yo'qoladi, shuning uchun bandlarga alohida belgi qo'yiladi va har hafta ko'rib chiqiladi. P1 bandlari 30 kun ichida bajariladi. Bajarilmagan band soni ishonchlilik qarzining eng halol metrikasi.

## 35.11 On-call navbati: adolatli taqsimot, ogohlantirish charchoqini kamaytirish

On-call tizim egaligining bir qismi, jazo emas. Uch qoida bor. Navbat aylanadi, bitta odam doimiy "qutqaruvchi" bo'lmaydi, chunki bu bilim monopoliyasi va charchoq beradi. Navbat kompensatsiya bilan bo'ladi. Navbatdagi odam o'sha hafta feature ishidan ozod, aks holda ikki ish ham sifatsiz chiqadi.

Navbatga kirish shartli: yangi odam oldin ikkilamchi navbatchi sifatida kuzatadi va runbook'ni o'qiydi. Runbook'da to'rt narsa bor: qaysi metrikaga qarash, qanday flag bor, qanday qaytarish, kimga eskalatsiya qilish. Runbook bo'lmasa navbat lotereyaga aylanadi.

Charchoqni kamaytirishning eng kuchli vositasi tungi alert sonini o'lchash. Haftada bir navbatchiga ikkitadan ko'p uyg'otish bo'lsa, bu monitoring muammosi. Shu raqam har hafta ko'rib chiqiladi va eng shovqinli alert tuzatiladi.

## 35.12 Ogohlantirishlar sifati: har bir alert bajariladigan ish bo'lsin

Alert bitta savolga javob berishi kerak: hozir odam nima qilishi kerak. Javob bo'lmasa, bu alert emas, dashboard elementi. Ikkinchi mezon: alert simptomga qo'yiladi, sababga emas. "CPU 90 foiz" ko'pincha muammo emas, "checkout error rate 5 foizdan oshdi" esa doim muammo.

```yaml
# Simptom asosidagi alert: mijoz ko'radigan xatolik ulushi
groups:
  - name: payment-slo
    rules:
      - alert: PaymentErrorRateHigh
        # 5 daqiqalik oynada xato ulushi 2 foizdan oshsa
        expr: |
          sum(rate(http_server_requests_seconds_count{uri="/api/payments",status=~"5.."}[5m]))
          / sum(rate(http_server_requests_seconds_count{uri="/api/payments"}[5m])) > 0.02
        for: 5m                      # qisqa tebranishda uyg'otmaydi
        labels:
          severity: page             # telefon bilan uyg'otish
          service: payment
        annotations:
          summary: "To'lov API xato ulushi 2 foizdan yuqori"
          impact: "Mijozlar to'lovni yakunlay olmaydi"
          action: "payment.new-gateway flag'ini o'chirish, keyin oxirgi deploy'ni qaytarish"
          runbook_url: "https://wiki.internal/runbook/payment-error-rate"
```

Har alertda runbook havolasi va birinchi harakat bo'ladi, chunki uyqudan uyg'ongan odam o'ylab emas, o'qib harakat qiladi. Alertlar har chorakda tozalanadi: 90 kunda bir marta ham to'g'ri ishga tushmagani o'chiriladi yoki chegarasi qayta hisoblanadi. Shovqinli alert haqiqiy alertni ham e'tiborsiz qoldirishga o'rgatadi.

## 35.13 To'liq post-mortem namunasi: to'lov servisi uzilishi misolida

Quyidagi shablonda real ko'rinishdagi namuna bor, uni nusxa olib har incidentda to'ldirish mumkin.

```markdown
# Post-mortem: <servis> <davomiylik> uzilishi

- Sana, daraja, boshqaruvchi, hujjat holati

## Qisqa xulosa
Uch gap: nima buzildi, nega ta'sir qildi, nima bilan tiklandi.

## Ta'sir
- Davomiyligi va aniq vaqt oralig'i
- Muvaffaqiyatsiz so'rov soni va zarar ko'rgan mijoz soni
- Ma'lumot yo'qolishi yoki buzilishi bo'ldimi
- SLO budjetining qancha ulushi sarflandi

## Vaqt chizig'i
Besh majburiy nuqta: boshlanish, birinchi signal, odam xabardor
bo'lishi, birinchi tiklash harakati, to'liq tiklanish.

## Sabab tahlili
Besh marta "nega" zanjiri, oxiri tizim yoki jarayonga borib tugaydi.

## Nega tezroq aniqlanmadi
## Nega tezroq tiklanmadi
## Nima yaxshi ishladi

## Harakat bandlari
| Ish | Tur | Egasi | Muddat | Tekshiruv |
|---|---|---|---|---|
```

Shablonning to'ldirilgan ko'rinishi quyidagicha.

```markdown
# Post-mortem: to'lov servisi 43 daqiqa uzilishi

Sana 2026-09-18, daraja P1, boshqaruvchi platform navbatchisi.

## Qisqa xulosa
Yangi gateway client'ida read timeout yo'q edi. Provayder sekinlashganda
Tomcat thread'lari band bo'ldi va /api/payments javob bermay qoldi.

## Ta'sir
- 14:07 dan 14:50 gacha, 43 daqiqa
- Taxminan 2 180 muvaffaqiyatsiz to'lov, taxminan 1 400 mijoz
- Ikki marta debet yo'q, idempotency key ishladi
- Oylik 99.9% budjetining taxminan 100 foizi sarflandi

## Vaqt chizig'i (UTC+5)
- 13:58 deploy, flag 10% trafikda; 14:07 p99 180ms dan 9s ga; 14:11 alert
- 14:29 thread dump: 198 thread socket read da kutmoqda
- 14:41 flag o'chirildi; 14:50 xato ulushi 0.1 foizga qaytdi

## Sabab tahlili
Client umumiy builder'siz tuzilgan, timeout qo'llanmagan. Izolyatsiya
yo'q edi, shuning uchun boshqa endpoint'lar ham ta'sirlandi.

## Harakat bandlari
| Ish | Tur | Egasi | Muddat | Tekshiruv |
|---|---|---|---|---|
| Client faqat umumiy builder'dan | oldini olish | payments | 02.10 | CI qoidasi |
| Gateway latency alert, 2s | aniqlash | platform | 25.09 | sekinlashtirish testi |
```

Shablonning qiymati tartibda: bir xil tuzilish o'qishni tezlashtiradi va bandlarni bir joyga yig'adi. Bir yilda yig'ilgan post-mortem'lar eng qimmat arxitektura hujjatiga aylanadi.

## 35.14 Amalda qo'llash

- [ ] Incident darajalari jadvalini yozing: har daraja uchun biznes mezoni, javob vaqti, uyg'otish usuli.
- [ ] Eng muhim uch servis uchun runbook yarating: metrika havolalari, flag nomlari, qaytarish buyrug'i, eskalatsiya ro'yxati.
- [ ] Har bir xavfli yangi yo'lni feature flag ostiga oling va flag'ni pod qayta ishga tushirmasdan o'chirib ko'ring.
- [ ] Oxirgi 90 kundagi alertlarni ko'rib chiqing, to'g'ri ishga tushmaganini o'chiring, qolganiga runbook havolasi va birinchi harakatni qo'shing.
- [ ] Barcha HTTP client va DB so'rovlariga timeout qo'yilganini tekshiradigan avtomatik qoida qo'shing.
- [ ] Post-mortem shablonini repoga joylashtiring va oxirgi P1 ni shu shablon bilan qayta yozib ko'ring.
- [ ] Tungi uyg'otish sonini har hafta o'lchang, 2 dan oshsa alertni tuzatish ishini oching va ochiq harakat bandlarini shu yig'ilishda ko'rib chiqing.

---

[&larr; 34. Legacy kod va bosqichma-bosqich refaktoring](34-legacy-kod-va-bosqichma-bosqich-refaktoring.md) · [Mundarija](README.md) · [36. Code review va jamoada texnik yetakchilik &rarr;](36-code-review-va-jamoada-texnik-yetakchilik.md)
