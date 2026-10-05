<!-- doc: architect | chapter: 37 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyyasi](README.md)

# 37. Xarajat, SLO va biznes bilan muloqot (Cost, SLO and Business Communication)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [37.1 Arxitektura qarorining pul tarafi: server, litsenziya, odam vaqti](#371-arxitektura-qarorining-pul-tarafi-server-litsenziya-odam-vaqti)
- [37.2 Bulut xarajati qayerdan keladi: hisoblash, saqlash, tarmoq chiqishi, boshqariladigan xizmat](#372-bulut-xarajati-qayerdan-keladi-hisoblash-saqlash-tarmoq-chiqishi-boshqariladigan-xizmat)
- [37.3 Bitta so'rovning narxi: oddiy hisob va uni kuzatish](#373-bitta-sorovning-narxi-oddiy-hisob-va-uni-kuzatish)
- [37.4 Xarajatni kamaytirish yo'llari va ularning sifatga ta'siri](#374-xarajatni-kamaytirish-yollari-va-ularning-sifatga-tasiri)
- [37.5 SLI, SLO va SLA farqi, ularni to'g'ri tanlash](#375-sli-slo-va-sla-farqi-ularni-togri-tanlash)
- [37.6 Xato byudjeti (error budget) va u qanday qaror qabul qilishga yordam beradi](#376-xato-byudjeti-error-budget-va-u-qanday-qaror-qabul-qilishga-yordam-beradi)
- [37.7 Mavjudlik raqamlari: 99.9 va 99.99 orasidagi amaliy farq va narxi](#377-mavjudlik-raqamlari-999-va-9999-orasidagi-amaliy-farq-va-narxi)
- [37.8 Nofunksional talabni biznes tiliga o'girish](#378-nofunksional-talabni-biznes-tiliga-ogirish)
- [37.9 Texnik qarzni biznesga tushuntirish: tezlik va xavf tilida](#379-texnik-qarzni-biznesga-tushuntirish-tezlik-va-xavf-tilida)
- [37.10 Qaror uchun arzon o'lchov: kichik tajriba va bosqichma-bosqich yoyish](#3710-qaror-uchun-arzon-olchov-kichik-tajriba-va-bosqichma-bosqich-yoyish)
- [37.11 Yetkazib berish muddati va sifat orasidagi muzokarani olib borish](#3711-yetkazib-berish-muddati-va-sifat-orasidagi-muzokarani-olib-borish)
- [37.12 Hisobot: rahbarga nima ko'rsatiladi va qanday ko'rinishda](#3712-hisobot-rahbarga-nima-korsatiladi-va-qanday-korinishda)
- [37.13 Amalda qo'llash](#3713-amalda-qollash)

</details>



Arxitektorning har bir qarori oxir-oqibat pulga aylanadi. Qo'shimcha indeks disk bandini oshiradi, qo'shimcha replika hisoblash hisobini oshiradi, qo'shimcha abstraksiya esa odam vaqtini yeydi. Bu bob texnik qarorni pul va risk tilida gapirishga, mavjudlik maqsadini raqam bilan belgilashga va rahbar bilan bir xil lug'atda muloqot qilishga bag'ishlangan.

## 37.1 Arxitektura qarorining pul tarafi: server, litsenziya, odam vaqti

Xarajatning uchta katta manbasi bor: infratuzilma, litsenziya va odam vaqti. Ko'p jamoa faqat birinchisini sanaydi, chunki u hisob-fakturada ko'rinadi. Haqiqatda o'rta hajmli to'lov servisida odam vaqti infratuzilmadan 3-10 barobar qimmat. Oyiga 8 ta developer, har biri taxminan 4000 dollar bo'lsa, jamoa oyiga 32 000 dollar turadi, serveri esa 3000 dollar.

Shuning uchun "serverni tejash uchun murakkab yechim" deyarli har doim yutqazadi. Oyiga 400 dollar tejaydigan optimizatsiya har oyda bir developer kunini olsa, siz zarar ko'rasiz. Teskari holat ham bor: noto'g'ri tanlangan instance turi yiliga 100 000 dollar yo'qotishi mumkin.

Litsenziya alohida gap. Tijorat databazasi yoki APM agenti CPU soniga bog'langan bo'lsa, gorizontal scaling narxi pog'onali o'sadi. PostgreSQL da litsenziya nol, lekin tuning va backup uchun odam bilimi kerak.

```java
// Qarorni pul bilan baholash: uchta manba bir joyda.
public record QarorNarxi(
        BigDecimal infraOylik,      // server, disk, tarmoq
        BigDecimal litsenziyaOylik, // CPU yoki node ga bog'liq
        int odamKuni,               // yozish va joylashtirish
        int yillikQollabQuvvatlashKuni) {

    private static final BigDecimal KUN_NARXI = new BigDecimal("200");

    // Uch yillik umumiy egalik narxi (TCO).
    public BigDecimal uchYillik() {
        BigDecimal oylik = infraOylik.add(litsenziyaOylik)
                .multiply(BigDecimal.valueOf(36));
        BigDecimal birMartalik = KUN_NARXI.multiply(BigDecimal.valueOf(odamKuni));
        BigDecimal qollab = KUN_NARXI
                .multiply(BigDecimal.valueOf(yillikQollabQuvvatlashKuni * 3L));
        return oylik.add(birMartalik).add(qollab);
    }
}
```

## 37.2 Bulut xarajati qayerdan keladi: hisoblash, saqlash, tarmoq chiqishi, boshqariladigan xizmat

Bulut hisobi to'rtta ustunga bo'linadi. Hisoblash odatda eng katta qism, 40-60 foiz. Saqlash 10-25 foiz. Tarmoq chiqishi (egress) 5-20 foiz, lekin kutilmaganda portlashi mumkin. Qolgan qismni boshqariladigan xizmatlar egallaydi.

Eng ko'p e'tibordan chetda qoladigan narsa egress. Zonalar orasidagi trafik ham pulli. Agar buyurtma servisi har bir so'rovda ombor servisiga 4 marta murojaat qilsa va javob 20 KB bo'lsa, kuniga 10 million so'rovda bu 800 GB zona-aro trafik. GB uchun 0.01 dollar bilan bu oyiga taxminan 240 dollar faqat shu yo'nalishda.

Saqlashda PostgreSQL ko'pincha kutilgandan katta bo'ladi. Indekslar jadval hajmining 50-150 foizini tashkil qilishi oddiy hol. WAL arxivi va PITR nusxalari ham hisobga qo'shiladi.

```sql
-- Qaysi jadval va indeks qancha joy egallaydi: xarajat tahlilining birinchi qadami.
SELECT c.relname AS obyekt,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS umumiy,
       pg_size_pretty(pg_indexes_size(c.oid))   AS indekslar,
       s.n_live_tup                             AS qatorlar
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_stat_user_tables s ON s.relid = c.oid
WHERE n.nspname = 'public' AND c.relkind = 'r'
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 15;

-- Ishlatilmayotgan indeks: sof xarajat, hech qanday foyda yo'q.
SELECT relname, indexrelname, idx_scan,
       pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes
WHERE idx_scan < 50
ORDER BY pg_relation_size(indexrelid) DESC;
```

## 37.3 Bitta so'rovning narxi: oddiy hisob va uni kuzatish

Bitta so'rovning narxini bilish muloqotni butunlay o'zgartiradi. Hisob oddiy: oylik infratuzilma xarajatini oylik so'rov soniga bo'lasiz. Servis oyiga 5000 dollar olsa va 50 million so'rovni qayta ishlasa, bitta so'rov 0.0001 dollar turadi.

Keyin bu raqamni endpoint bo'yicha taqsimlash kerak, chunki hamma so'rov teng emas. Hisobot generatsiyasi 2 soniya CPU vaqtini oladi, oddiy GET esa 5 millisekund. CPU bo'yicha vaznlaganda hisobot endpointi so'rovlarning 0.5 foizini tashkil qilib, xarajatning 40 foizini yeyayotgani ko'rinadi.

```java
// Har bir endpoint uchun CPU vaqtini yig'amiz, keyin xarajatni vaznlab taqsimlaymiz.
@Component
class SorovNarxiFiltri implements Filter {

    private final MeterRegistry registry;
    private final ThreadMXBean threads = ManagementFactory.getThreadMXBean();

    SorovNarxiFiltri(MeterRegistry registry) { this.registry = registry; }

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        long boshCpu = threads.getCurrentThreadCpuTime(); // nanosekund
        try {
            chain.doFilter(req, res);
        } finally {
            long sarf = threads.getCurrentThreadCpuTime() - boshCpu;
            String yol = ((HttpServletRequest) req).getRequestURI();
            // Counter sifatida yig'amiz: keyin narxga ko'paytiriladi.
            registry.counter("sorov.cpu.nanos", "yol", yol).increment(sarf);
        }
    }
}
```

Endpoint ulushi uning CPU nanosekundlarini umumiy yig'indiga bo'lgan nisbati. Endpoint xarajati shu ulushni oylik hisobga ko'paytirish natijasi. Databaza uchun ham shunday yondashuv bor: `pg_stat_statements` dagi `total_exec_time` bo'yicha taqsimlanadi.

## 37.4 Xarajatni kamaytirish yo'llari va ularning sifatga ta'siri

Har bir tejash usuli biror narsani qurbon qiladi, va arxitektorning vazifasi qurbonlikni ochiq aytish. Instance o'lchamini kichraytirish eng tez natija beradi, lekin CPU zaxirasi kamayganda p99 latency keskin o'sadi. 70 foiz CPU bandligi xavfsiz chegara, 85 foizdan oshsa latency ikki barobar bo'lishi mumkin.

Reserved chegirmalari 30-55 foiz tejaydi va sifatga ta'sir qilmaydi, narxi esa 1-3 yillik majburiyat. Cache qo'shish databaza yuklamasini 60-90 foiz kamaytiradi, narxi ma'lumotning eskirishi: ombor qoldig'ini 30 soniya cache'lash arziydi, hisob balansini cache'lash esa pul yo'qotadi.

| Usul | Taxminiy tejash | Sifatga ta'siri | Qachon arziydi |
|---|---|---|---|
| Instance kichraytirish | 20-40% | p99 latency o'sadi | CPU 40% dan past bo'lsa |
| Reserved/committed | 30-55% | Yo'q | Barqaror bazaviy yuk |
| Spot node | 60-80% | Node to'satdan o'chadi | Batch va stateless ish |
| Cache qatlami | DB yukida 60-90% | Ma'lumot eskirishi | Ko'p o'qilsa, kam o'zgarsa |
| Eski ma'lumot arxivi | Saqlashda 70-90% | Arxivga murojaat sekin | Audit va hisobot ma'lumoti |
| Replika sonini kamaytirish | 25-50% | Chidamlilik tushadi | SLO 99.9% dan past bo'lsa |
| Log hajmini qisqartirish | Observability'da 40-70% | Debug qiyinlashadi | DEBUG prod'da yoqilgan bo'lsa |
| Zona-aro trafikni kamaytirish | Egress'da 50-80% | Joylashuv moslashuvi kamayadi | Servislar ko'p gaplashsa |

## 37.5 SLI, SLO va SLA farqi, ularni to'g'ri tanlash

SLI bu o'lchov, ya'ni raqam. SLO bu shu raqamga qo'yilgan ichki maqsad. SLA bu mijoz bilan tuzilgan shartnoma va jarima. To'lov API uchun SLI "5xx bo'lmagan so'rovlar ulushi", SLO "30 kunlik oynada 99.95 foizdan katta", SLA "oyiga 99.9 foizdan past bo'lsa, mijoz to'lovning 10 foizini qaytaradi". SLO har doim SLA dan qattiqroq bo'lishi kerak, chunki sizga reaksiya uchun zahira kerak.

SLI tanlashda ikkita qoida bor. Birinchi, foydalanuvchi sezadigan narsani o'lchang: CPU bandligi SLI emas. Ikkinchi, SLI nisbat bo'lsin. "Kuniga 100 ta xato" yuk o'sganda ma'nosiz bo'ladi, "xato ulushi 0.1 foizdan kam" esa har doim ma'noli. Latency SLI ni chegara bilan yozing, chunki o'rtacha qiymat og'ir dumni yashiradi.

```yaml
# Prometheus recording rule: SLI ni bitta joyda ta'riflab qo'yamiz.
groups:
  - name: tolov-slo
    interval: 30s
    rules:
      # Muvaffaqiyat ulushi: 5xx bo'lmagan so'rovlar.
      - record: tolov:sli_muvaffaqiyat:ratio5m
        expr: |
          sum(rate(http_server_requests_seconds_count{
                service="tolov", status!~"5.."}[5m]))
          /
          sum(rate(http_server_requests_seconds_count{service="tolov"}[5m]))

      # Latency SLI: 300 ms dan tez javoblar ulushi.
      - record: tolov:sli_tezlik:ratio5m
        expr: |
          sum(rate(http_server_requests_seconds_bucket{
                service="tolov", le="0.3"}[5m]))
          /
          sum(rate(http_server_requests_seconds_count{service="tolov"}[5m]))

      # 30 kunlik error budget qoldig'i, 99.95% SLO uchun.
      - record: tolov:error_budget:qoldiq
        expr: |
          1 - ((1 - avg_over_time(tolov:sli_muvaffaqiyat:ratio5m[30d])) / 0.0005)
```

## 37.6 Xato byudjeti (error budget) va u qanday qaror qabul qilishga yordam beradi

Error budget bu SLO ruxsat bergan nosozlik miqdori. SLO 99.9 foiz bo'lsa, byudjet 0.1 foiz. 30 kunlik oynada 100 million so'rov bo'lsa, siz 100 000 ta so'rovni yo'qotishga haqlisiz. Bu jarima emas, balki resurs.

Byudjetning asosiy foydasi bahsni tugatishi. Byudjet bor ekan, reliz davom etadi. Byudjet tugasa, yangi funksiya to'xtaydi va jamoa barqarorlikka o'tadi. Bu qoida oldindan kelishiladi.

Byudjetni sarflanish tezligi (burn rate) bilan kuzatish kerak. Burn rate 1 degani byudjet oyning oxirida tugaydi. Burn rate 14.4 degani byudjet 50 soatda tugaydi, bu darhol alert sababi. Sekin oqish uchun 6 soatlik oynada burn rate 6 dan katta bo'lishi yetarli signal.

```bash
#!/usr/bin/env bash
# Error budget qoldig'ini hisoblash: 30 kunlik oyna, SLO = 99.95%.
SLO_UZILISH=0.0005            # ruxsat etilgan xato ulushi
JAMI=$(curl -sG "$PROM/api/v1/query" \
  --data-urlencode 'query=sum(increase(http_server_requests_seconds_count{service="tolov"}[30d]))' \
  | jq -r '.data.result[0].value[1]')
XATO=$(curl -sG "$PROM/api/v1/query" \
  --data-urlencode 'query=sum(increase(http_server_requests_seconds_count{service="tolov",status=~"5.."}[30d]))' \
  | jq -r '.data.result[0].value[1]')

RUXSAT=$(echo "$JAMI * $SLO_UZILISH" | bc -l)
QOLDIQ=$(echo "scale=1; 100 * (1 - $XATO / $RUXSAT)" | bc -l)
echo "Ruxsat etilgan xato: ${RUXSAT%.*}, sodir bo'lgan: ${XATO%.*}"
echo "Byudjet qoldigi: ${QOLDIQ}%"

# 25% dan kam qolsa reliz quvurini to'xtatamiz.
awk -v q="$QOLDIQ" 'BEGIN { exit (q < 25) ? 1 : 0 }' || {
  echo "BYUDJET TUGAYAPTI: yangi funksiya relizi to'xtatiladi"; exit 1; }
```

## 37.7 Mavjudlik raqamlari: 99.9 va 99.99 orasidagi amaliy farq va narxi

Mavjudlik foizini vaqtga aylantirmasangiz, muzokara bo'sh gap bo'lib qoladi. Jadvalda yil 365 kun, oy 30 kun deb olingan.

| Mavjudlik | Yillik uzilish | Oylik uzilish | Haftalik uzilish | Odatiy arxitektura | Narx koeffitsiyenti |
|---|---|---|---|---|---|
| 99% | 3 kun 15 soat 36 daqiqa | 7 soat 12 daqiqa | 1 soat 40.8 daqiqa | Bitta instance, qo'lda tiklash | 1x |
| 99.5% | 1 kun 19 soat 48 daqiqa | 3 soat 36 daqiqa | 50.4 daqiqa | Bitta instance, avtomatik restart | 1.2x |
| 99.9% | 8 soat 45.6 daqiqa | 43.2 daqiqa | 10.1 daqiqa | 2 instance, bitta zona, qo'lda DB failover | 1.5x |
| 99.95% | 4 soat 22.8 daqiqa | 21.6 daqiqa | 5.04 daqiqa | 3 instance, 2 zona, avtomatik failover | 2.2x |
| 99.99% | 52.6 daqiqa | 4.32 daqiqa | 1.01 daqiqa | 3 zona, replikalar, 24/7 navbatchi | 3.5x |
| 99.999% | 5.26 daqiqa | 25.9 soniya | 6.05 soniya | Ko'p mintaqa, aktiv-aktiv | 8x va yuqori |

Amaliy farq shunda. 99.9 foizda oyda 43.2 daqiqa bor, bu bitta sekin deploy yoki bitta qo'lda DB failover uchun yetadi. 99.99 foizda oyda faqat 4.32 daqiqa bor, bu odam aralashuviga vaqt qoldirmaydi. Ya'ni 99.99 foiz talab qilish butun tiklashni avtomatlashtirishga majbur qiladi.

99.9 dan 99.99 ga o'tish uchun uchta availability zone, zona-aro replikatsiya, avtomatik failover, 24/7 navbatchilik va chaos mashqi kerak. Bu infratuzilmani taxminan 2.5 barobar va odam xarajatini 2 barobar oshiradi.

Muhim ogohlantirish: zanjirdagi mavjudliklar ko'paytiriladi. To'lov servisi uchta bog'liqlikka murojaat qilsa va har biri 99.9 foiz bo'lsa, umumiy nazariy mavjudlik 99.7 foiz. Shuning uchun yuqori SLO faqat zaxira yo'li va graceful degradation bilan erishiladi.

## 37.8 Nofunksional talabni biznes tiliga o'girish

Biznes "tez bo'lsin" deydi, arxitektor esa buni o'lchanadigan shaklga aylantiradi. Tarjima formulasi: kim, nima qiladi, qanday tezlikda, qanday yuk ostida, qanday ulushda. "Katalog tez ochilsin" quyidagicha aylanadi: "mobil mijozda katalog so'rovlarining 95 foizi 400 ms ichida, 99 foizi 900 ms ichida javob oladi, sekundda 3000 so'rov yuklamasida".

Teskari tarjima ham kerak. "p99 latency 600 ms ga tushdi" o'rniga "checkout sahifasini tashlab ketish 2.1 foizdan 1.4 foizga tushdi, bu oyiga taxminan 180 000 dollar aylanma" deyish kerak.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Talab shakli | "Tizim tez va ishonchli bo'lsin" | "p99 < 400 ms, xato ulushi < 0.1%, 3000 rps da" |
| Mavjudlik | "Hech qachon o'chmasin" | "99.95%, oyiga 21.6 daqiqa byudjet bilan" |
| Xarajat | Oylik hisobni umumiy ko'rish | Endpoint bo'yicha bitta so'rov narxi |
| Optimizatsiya sababi | "Kod chiroyli bo'lmadi" | "Bu endpoint xarajatning 40% ini yeyadi" |
| Reliz qarori | Har kim o'z fikrini aytadi | Error budget qoldig'i qarorni belgilaydi |
| Texnik qarz | "Refactoring kerak" | "Bu modul har bir o'zgarishga 3 kun qo'shadi" |
| Yangi texnologiya | "Zamonaviy stack" | "2 hafta tajriba, 5% trafik, o'lchov bilan qaror" |
| Muddat muzokarasi | Hajmni saqlab, sifatni qurbon qilish | Hajmni kesib, sifat darvozasini saqlash |
| Rahbarga hisobot | Grafanadagi 30 ta grafik | 5 ta raqam, trend va bitta qaror so'rovi |
| Incident xulosasi | Kim aybdor topiladi | Byudjet sarfi va to'rtta tuzatish ishi |

## 37.9 Texnik qarzni biznesga tushuntirish: tezlik va xavf tilida

"Kod iflos" deb gapirish ishlamaydi. Biznes ikkita narsani tushunadi: tezlik va xavf. Tezlik tomoni: "buyurtma modulida har bir o'rtacha o'zgarish 2 kun emas, 6 kun oladi, chunki bitta o'zgarish 14 joyni tegishga majbur qiladi". Bu raqam Git tarixidan olinadi.

Xavf tomoni: "shu modulga tegadigan relizlarning 30 foizi hotfix bilan tugaydi, boshqa modullarda bu 4 foiz". Change failure rate modul bo'yicha ajratilsa, qaysi joy pul yo'qotayotgani ko'rinadi.

Keyin taklifni investitsiya shaklida qo'yasiz. "15 kun ish, natijada o'zgarish vaqti 6 kundan 3 kunga tushadi. Yiliga shu modulda 40 ta o'zgarish bo'ladi, ya'ni 120 kun tejaladi. To'lanish muddati taxminan 2 oy." Bu shaklda rad etish qiyin.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| SLO ni darhol 99.99% qilish | Byudjet doim tugaydi, jamoa alertga ishonmaydi | Haqiqiy o'lchovdan boshlab, bosqichma-bosqich qattiqlashtiring |
| SLI sifatida CPU olish | Mijoz azob chekadi, dashboard yashil turadi | Faqat foydalanuvchi sezadigan o'lchovni SLI qiling |
| O'rtacha latency bo'yicha SLO | Og'ir dum yashiriladi | p95 va p99 ni chegara bilan yozing |
| SLA ni SLO ga teng qilish | Bitta hodisa darhol jarimaga aylanadi | SLO ni SLA dan bir pog'ona qattiq qiling |
| Xarajatni faqat yillik ko'rish | Oqish 11 oy sezilmaydi | Oylik byudjet va 20% oshganda alert qo'ying |
| Zaxirani ko'p olish | Arxitektura o'zgarsa, to'lov behuda ketadi | Faqat barqaror bazaviy yukni majburiyatga oling |
| DEBUG log prod'da qolishi | Observability hisobi 3-5 barobar oshadi | Log darajasini konfiguratsiyadan boshqaring |
| Tajribani o'lchovsiz yoyish | Natija bor-yo'qligi noma'lum qoladi | Metrika va to'xtatish shartini oldindan yozing |

## 37.10 Qaror uchun arzon o'lchov: kichik tajriba va bosqichma-bosqich yoyish

Katta qarorni bahs bilan hal qilish qimmat. Bir hafta ishlaydigan prototip ikki oylik bahsdan tezroq javob beradi. Tajriba uchun uchta narsa oldindan yozilishi kerak: qanday metrika o'lchanadi, qanday natija "ha" deb hisoblanadi, qachon to'xtatiladi.

Prod'da yoyish bosqichli bo'lsin: 1 foiz, 5 foiz, 25 foiz, 100 foiz. Har bosqichda kamida bitta to'liq ish kuni kutiladi. Bu qoida yangi kod uchun ham, konfiguratsiya o'zgarishi va yangi indeks uchun ham amal qiladi.

```java
// Bosqichma-bosqich yoyish: foiz konfiguratsiyadan keladi, kod o'zgarmaydi.
@Service
class HisobotYonaltirgichi {

    private final HisobotYozuvchi yangi;
    private final HisobotYozuvchi eski;
    private final Environment env;

    HisobotNatija yarat(HisobotSorovi sorov) {
        int foiz = env.getProperty("hisobot.yangi-yol.foiz", Integer.class, 0);
        // Barqaror taqsimot: bir mijoz har doim bir yo'ldan o'tadi.
        int chelak = Math.floorMod(sorov.mijozId().hashCode(), 100);
        if (chelak < foiz) {
            return yangi.yarat(sorov);
        }
        return eski.yarat(sorov);
    }
}
```

```properties
# Yoyish jadvali: har bosqichda bitta ish kuni kuzatiladi.
# 1-kun: 1%, 2-kun: 5%, 4-kun: 25%, 7-kun: 100%
hisobot.yangi-yol.foiz=5

# To'xtatish sharti: p99 300 ms dan oshsa yoki xato ulushi 0.2% dan oshsa.
hisobot.yangi-yol.p99-chegara-ms=300
hisobot.yangi-yol.xato-chegara-foiz=0.2

# Yangi yo'l uchun alohida pool: eski yo'lni himoya qiladi.
spring.datasource.hikari.maximum-pool-size=20
hisobot.datasource.hikari.maximum-pool-size=6
hisobot.datasource.hikari.connection-timeout=2000
```

## 37.11 Yetkazib berish muddati va sifat orasidagi muzokarani olib borish

Muzokarada uchta o'zgaruvchi bor: hajm, muddat va sifat. Ikkitasini qotirsangiz, uchinchisi erkin qoladi. Ko'p jamoa muddat va hajmni qotiradi, keyin sifat qurbon bo'ladi. Natija hotfix to'lqini, ya'ni tejalgan vaqt qarz bilan qaytariladi.

Arxitektorning pozitsiyasi aniq bo'lsin: sifat darvozasi muzokara mavzusi emas, hajm esa muzokara mavzusi. Amalda bu "o'nta funksiyani yarim sifat bilan" o'rniga "to'rtta funksiyani to'liq sifat bilan" degan taklifga aylanadi. Eng yaxshi kesish funksiyani butunlay olib tashlash emas, balki qamrovini qisqartirish: birinchi relizda faqat oxirgi 30 kunlik ma'lumot, faqat CSV eksport, faqat ichki foydalanuvchi uchun.

Muzokaraga raqam bilan kiring. "Bu muddatda sifatni saqlash uchun hajmdan 35 foizini kesish kerak. Kesmasak, bahom: relizdan keyin 2-3 hafta hotfix, va shu davrda yangi ish bo'lmaydi." Bahoni oldingi relizlar ma'lumoti bilan tasdiqlang.

## 37.12 Hisobot: rahbarga nima ko'rsatiladi va qanday ko'rinishda

Rahbarga 30 ta grafik ko'rsatish hisobot emas. To'g'ri hisobot bir sahifa, besh raqam va bitta aniq so'rovdan iborat. Besh raqam: SLO bajarilishi va error budget qoldig'i, oylik xarajat va o'tgan oyga nisbatan o'zgarish, bitta so'rovning narxi va trendi, lead time bilan change failure rate, va ochiq qolgan eng katta xavf.

Har bir raqam yonida trend va bitta izoh bo'lsin. Izoh sabab yoki harakatni aytadi. "Xarajat 12 foiz oshdi, sababi hisobot trafigi ikki barobar bo'ldi, tungi batch'ga ko'chirish ishi boshlandi" yaxshi izoh.

Hisobot oxirida aniq so'rov bo'lishi kerak. "Ma'lumot uchun" deb tugagan hisobot foydasiz. "Hisobot SLO sini 99.9 dan 99.5 ga tushirishni taklif qilamiz, bu oyiga 2200 dollar tejaydi" deb tugasin. Incident xulosasi ham shu mantiqda: kim aybdor emas, nima byudjetni sarfladi va qaysi to'rtta ish buni qaytarilmas qiladi.

## 37.13 Amalda qo'llash

- [ ] Eng yuqori trafikli servis uchun oylik xarajatni so'rov soniga bo'lib, bitta so'rovning narxini raqam bilan yozib qo'y.
- [ ] `pg_stat_user_indexes` dan `idx_scan < 50` bo'lgan indekslarni topib, ularning umumiy hajmini va oylik saqlash narxini hisobla.
- [ ] Asosiy biznes oqimi uchun ikkita SLI ta'rifla: muvaffaqiyat ulushi va p99 latency chegarasi, ikkalasini recording rule sifatida yoz.
- [ ] SLO qiymatini tanlab, uni yillik va oylik uzilish daqiqasiga aylantir, va bu raqamni jamoa bilan kelish.
- [ ] Error budget qoldig'ini ko'rsatadigan dashboard paneli qo'sh, 25 foizdan kam qolganda reliz to'xtash qoidasini rasmiylashtir.
- [ ] Bitta nofunksional talabni o'lchanadigan shaklga aylantir: yuk, foiz va chegara bilan.
- [ ] Eng og'riqli modul uchun lead time va change failure rate ni hisoblab, texnik qarz taklifini to'lanish muddati bilan yoz.
- [ ] Rahbar uchun bir sahifali shablon tayyorla: besh raqam, trend, qisqa izoh va bitta aniq so'rov.

---

[&larr; 36. Code review va jamoada texnik yetakchilik](36-code-review-va-jamoada-texnik-yetakchilik.md) · [Mundarija](README.md) · [38. Doimiy o'rganish va texnologiya tanlash &rarr;](38-doimiy-organish-va-texnologiya-tanlash.md)
