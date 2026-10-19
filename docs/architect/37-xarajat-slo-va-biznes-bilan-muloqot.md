<!-- doc: architect | chapter: 37 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 37. Xarajat, SLO va biznes bilan muloqot (Cost, SLO and Business Communication)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

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
- [37.13 Maqsadga aylangan metrika o'ynaladi: tekshirish va qarshi o'lchov](#3713-maqsadga-aylangan-metrika-oynaladi-tekshirish-va-qarshi-olchov)
- [37.14 Amalda qo'llash](#3714-amalda-qollash)

</details>

Arxitektorning har bir qarori oxir-oqibat pulga aylanadi. Nygard buni qisqa qo'yadi: dizayn va arxitektura qarorlari bir vaqtda moliyaviy qarorlar, va ular ham joriy etish narxiga, ham undan keyingi oqibat narxiga qarab qabul qilinishi kerak (Nygard, *Release It!*, 1-bob, 18-bet). Muammoning ikkinchi yarmi tilda: Richards va Ford arxitektor va biznes vakilining turli tilda gapirishini "tarjimada yo'qolish" muammosi deb ataydi, arxitektor masshtablanish va mavjudlik haqida, biznes esa bozorga chiqish vaqti va mijoz qanoati haqida gapiradi (Richards, Ford, *Fundamentals of Software Architecture*, 5-bob). Bu bob texnik qarorni pul va risk tilida gapirishga, mavjudlik maqsadini raqam bilan belgilashga va rahbar bilan bir xil lug'atda muloqot qilishga bag'ishlangan.

## 37.1 Arxitektura qarorining pul tarafi: server, litsenziya, odam vaqti

Nygard eng muhim xatoni nomlaydi: loyihaning shoshqaloq davrida ishlab chiqish narxini operatsion narx hisobidan optimallashtiradigan qarorlar osongina qabul qilinadi; bu faqat jamoa qotirilgan byudjet va muddat bo'yicha o'lchanayotgan kontekstda ma'noli, pul to'layotgan tashkilot uchun esa yomon tanlov. Sababi oddiy: tizimlar hayotining ko'proq qismini ishlab chiqishda emas, operatsiyada o'tkazadi, shuning uchun bir martalik xarajatni takrorlanuvchi operatsion xarajat orqali chetlab o'tish mantiqsiz (1-bob, 18-bet).

Shu yerda kitobdagi tayyor hisob misoli bor. Nygard yozadi: agar siz reliz paytidagi uzilishni yo'q qiladigan avtomatik build va reliz tizimiga 5 000 dollar sarflasangiz, kompaniya 200 000 dollardan qutuladi. Hisobning asosi izohda ochilgan: har reliz 10 000 dollar (ish kuchi plus rejalangan uzilish narxi), yiliga to'rt reliz va besh yillik ufq. U buni taxminan 4 000 foiz ROI deb ataydi va ko'p moliya direktori bunday xarajatni ma'qullashga qarshi bo'lmaydi deb izohlaydi (1-bob, 18-bet va 4-izoh).

Uzilish narxi ham shu yerda: Nygard mijozlarining ko'pi uchun uzilishning to'g'ridan to'g'ri narxi soatiga 100 000 dollardan oshishini aytadi, va shu raqam bilan bir yilda 98 foiz va 99.99 foiz mavjudlik orasidagi farq 17 million dollardan oshadi (1-bob, 17-18-bet). Ya'ni arxitektura qarorini pulga aylantirish uchun sizga ikki raqam kerak: uzilishning soatlik narxi va qarorning uch yoki besh yillik umumiy egalik narxi. Birinchisini biznes aytadi, ikkinchisini siz hisoblaysiz.

Litsenziya CPU yoki node soniga bog'langanda gorizontal scaling narxining pog'onali o'sishi korpusning amaliy kuzatuvi, kitobdan olingan emas; uni o'z shartnomangizdan tekshirish kerak.

```java
// Qarorni pul bilan baholash: uchta manba bir joyda.
// KUN_NARXI misol qiymati: o'z jamoangizning haqiqiy kun narxini qo'ying.
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

Hisob to'rtta ustunga bo'linadi: hisoblash, saqlash, tarmoq chiqishi va boshqariladigan xizmatlar. Ustunlarning nisbati tizimga, provayderga va yukka bog'liq, shuning uchun bu bobda ulush foizlari berilmaydi: ularni o'z hisob-fakturangizdan oling.

Taqsimotni taxmin qilmaslik kerakligi kitobdagi tavsiyadan kelib chiqadi. Nygard kuzatuv ritmida kamida oyiga bir marta ma'lumot hajmlari va so'rov statistikasini ko'rib chiqishni, eng qimmat so'rovlarni tekshirishni va reja o'zgargan bo'lsa buni ma'lumot to'planayotganidan belgi deb olishni aytadi (17-bob, 308-bet). Ya'ni xarajat tahlili ham o'lchov bilan boshlanadi, slayddagi ulush bilan emas.

Zonalar orasidagi trafik pulli ekani esa arifmetika bilan hisoblanadi, lekin narx raqami provayderdan olinadi. Misol: buyurtma servisi har so'rovda ombor servisiga 4 marta murojaat qilsa va javob 20 KB bo'lsa, kuniga 10 million so'rovda bu 4 x 20 KB x 10 000 000, ya'ni taxminan 800 GB zona-aro trafik. Oylik summani topish uchun shu hajmni provayder narx sahifasidagi GB narxiga ko'paytirasiz.

Saqlashda indekslar jadvaldan katta ulush olishi mumkin, lekin nisbat sxemaga bog'liq va u taxmin qilinmaydi, o'lchanadi.

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

Bitta so'rovning narxini bilish muloqotni butunlay o'zgartiradi, va bu metrikaning o'rni kitobda ko'rsatilgan: Nygard tarixiy kuzatuvda saqlanishi kerak bo'lgan biznes metrikalari ro'yxatiga mijozlar, buyurtmalar, konversiya ulushi, daromad bilan birga xizmat ko'rsatish narxini ham qo'shadi (17-bob, 267-bet).

Hisob oddiy bo'linish: oylik infratuzilma xarajatini oylik so'rov soniga bo'lasiz. Masalan 5 000 dollar va 50 million so'rov bo'lsa, bitta so'rov 0.0001 dollar turadi. Bu arifmetika, qoida emas: ikki raqamni o'z hisobingizdan olasiz.

Keyin raqam endpoint bo'yicha taqsimlanadi, chunki so'rovlar teng emas. Nygard kuzatuv printsipini beradi: kuzatuvchi ham trendga, ham chetga chiqqan qiymatlarga qarashi kerak, ikkisi ham tushuncha beradi (17-bob, 307-bet). Endpoint bo'yicha taqsimot aynan chetga chiqqan endpointni ko'rsatadi.

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

Har bir tejash usuli biror narsani qurbon qiladi, va buning sababi arxitektura xarakteristikalarining tabiatida. Richards va Ford yozadi: har bir arxitektura xarakteristikasi ko'pincha boshqalariga ta'sir qiladi, masalan xavfsizlikni yaxshilash deyarli har doim ishlashga salbiy tegadi, shuning uchun arxitektor hamma xarakteristikani bir vaqtda maksimallashtira oladigan holatga kam duch keladi va qaror raqobatlashuvchi talablar orasidagi tanlovga aylanadi. Ular buni qoidaga aylantiradi: eng yaxshi arxitekturaga emas, eng kam yomon arxitekturaga intilish kerak (4-bob, "Trade-Offs and Least Worst Architecture").

Instance o'lchamini kichraytirish eng tez natija beradi, lekin ta'sir chiziqli emas. Nygard aynan shu xatoni nomlaydi: sig'im bilan ishlashdagi eng qiyin narsa nochiziqli effektlar, va baribir hamma chiziqli proyeksiyaga qaytmoqchi bo'ladi; u tipik savolni keltiradi, ya'ni 10 000 foydalanuvchini 50 foiz CPU bandligida ko'tarsak, 20 000 ni ham ko'taramiz degan savol. Sababi: har bir tizimda sig'imni aynan bitta cheklov belgilaydi, u birinchi bo'lib shiftga urilgan omil, va cheklovga yetilgach tizimning qolgan qismlari ishni yo navbatga qo'yishni yo tashlab yuborishni boshlaydi (8-bob, 162-163-bet). Shuning uchun xavfsiz CPU chegarasi raqami bu bobda berilmaydi: uni o'z tizimingizdagi cheklovni topib o'lchash kerak.

Reserved yoki committed chegirmalari sifatga ta'sir qilmaydi, narxi esa muddatli majburiyat; chegirma ulushi provayder, region va muddatga bog'liq, shuning uchun raqamni provayder narx sahifasidan oling. Cache qo'shish databaza yuklamasini kamaytiradi va kamayish miqdori taxmin emas, hit rate dan kelib chiqadi (28-bobdagi arifmetika: DB ga tushgan ulush miss rate ga teng), narxi ma'lumotning eskirishi: ombor qoldig'ini qisqa muddatga cache'lash arziydi, hisob balansini cache'lash esa pul yo'qotadi.

Replika sonini kamaytirishning narxi faqat chidamlilik emas. Kleppmann aniq bir imkoniyatni nomlaydi: bitta serverli tizim mashinani qayta yuklash kerak bo'lsa rejalangan uzilishni talab qiladi, mashina nosozligini ko'taradigan tizim esa butun tizimni to'xtatmasdan tugunni birin-ketin yangilash mumkin (1-bob, 7-bet). Ya'ni replikani kesish bilan siz uzilishsiz patching imkoniyatini ham kesasiz.

Spot node arzon bo'lishining sababi ham shu yerda: Kleppmann ba'zi bulut platformalarida virtual mashina instansiyalarining ogohlantirishsiz ishdan chiqishi odatiy hol ekanini, chunki platformalar yakka mashina ishonchliligidan ko'ra moslashuvchanlikni ustun qo'yganini yozadi (1-bob, 7-bet).

| Usul | Sifatga ta'siri | Qachon arziydi |
|---|---|---|
| Instance kichraytirish | Cheklovga yaqinlashganda navbat o'sadi, ta'sir nochiziqli | Cheklov o'lchangan va zaxira ko'p bo'lsa |
| Reserved yoki committed | Yo'q, lekin muddatli majburiyat qoladi | Barqaror bazaviy yuk |
| Spot node | Node ogohlantirishsiz o'chadi | Batch va stateless ish |
| Cache qatlami | Ma'lumot eskirishi | Ko'p o'qilsa, kam o'zgarsa |
| Eski ma'lumot arxivi | Arxivga murojaat sekin | Audit va hisobot ma'lumoti |
| Replika sonini kamaytirish | Chidamlilik va uzilishsiz patching imkoni tushadi | Uzilish byudjeti keng bo'lsa |
| Log hajmini qisqartirish | Debug va post-mortem qiyinlashadi | DEBUG prod'da yoqilgan bo'lsa |
| Zona-aro trafikni kamaytirish | Joylashuv moslashuvi kamayadi | Servislar ko'p gaplashsa |

## 37.5 SLI, SLO va SLA farqi, ularni to'g'ri tanlash

Uchta atamaning ta'rifi Newman'da aniq berilgan. SLA tizimni quruvchilar va tizimdan foydalanuvchilar orasidagi kelishuv: u faqat foydalanuvchi nimani kutishi mumkinligini emas, tizim shu maqbul darajaga yetmasa nima bo'lishini ham tasvirlaydi; SLA lar odatda "eng kam darajadagi" chegarada bo'ladi, hatto tizim maqsadiga faqat yetib turgan bo'lsa ham oxirgi foydalanuvchi baxtsiz bo'lib qoladigan darajada. Misol sifatida u AWS ning hisoblash xizmatini keltiradi: yakka instansiya uchun amaliy uptime kafolati yo'q, AWS 90 foiz uptime uchun eng yaxshi harakat qilishini aytadi, bunga yetmasa esa instansiya ishlamagan soat uchun pul olmaydi (10-bob, "Service-level agreement").

SLO esa jamoa darajasidagi tushuncha: SLO jamoa nimani berishga imzo cheqkanini belgilaydi, va tashkilotdagi har jamoa o'z SLO siga yetsa, tashkilotning SLA lari qanoatlantiriladi va ehtimol ancha oshib ketadi. Newman SLO ni SLA ga erishish uchun qilinadigan ish deb qarash juda soddalashtirilgan ekanini ham aytadi: SLO SLA da ko'rsatilmagan maqsadlarga, ichki o'zgarishga yoki orzuga ham tegishli bo'lishi mumkin (10-bob, "Service-level objectives"). Shundan amaliy xulosa: SLO SLA dan qattiqroq bo'ladi, chunki sizga reaksiya uchun zaxira kerak.

SLI esa o'lchovning o'zi: Newman uni "dasturimiz qiladigan biror narsaning o'lchovi" deb ta'riflaydi va misol qiladi protsessning javob vaqti, mijozning ro'yxatdan o'tishi, mijozga xato ko'rsatilishi yoki buyurtma berilishi; SLO ga yetganimizni bilish uchun aynan shu SLI larni to'plash va ko'rinadigan qilish kerak (10-bob, "Service-level indicators").

CPU bandligi SLI emas. Newman buni to'g'ridan to'g'ri aytadi: bunday qiymatlar biz haqiqatan kuzatmoqchi bo'lgan narsadan, ya'ni "tizim ishlayaptimi" savolidan bir qadam uzoq, va servislar orasidagi o'zaro ta'sir murakkablashgani sari yakka metrikaga qarab bu savolga javob berish yanada uzoqlashadi (10-bob).

SLI nisbat va persentil bilan yozilishining sababi statistik. Kleppmann o'rtachani tanqid qiladi: o'rtacha javob vaqti "tipik" javob vaqtini bilish uchun yaxshi metrika emas, chunki u qancha foydalanuvchi shu kechikishni boshdan kechirganini aytmaydi; chetga chiqishlar qanchalik yomon ekanini bilish uchun yuqori persentillarga, ya'ni p95, p99 va p999 ga qarash kerak, va yuqori persentillar, ya'ni dum kechikishi, foydalanuvchi tajribasiga to'g'ridan to'g'ri ta'sir qiladi (1-bob, 14-15-bet). Richards va Ford ham shu tuzoqni ko'rsatadi: jamoa faqat o'rtachani o'lchasa, so'rovlarning bir foizi o'n barobar uzoq ketadigan chegara holati yuzaga chiqmay qoladi, trafik yetarli bo'lsa chetga chiqishlar umuman ko'rinmaydi, shuning uchun maksimal javob vaqtini ham o'lchash kerak (6-bob, "Operational Measures").

Persentilning SLA dagi o'rni ham Kleppmann'da yozilgan: persentillar ko'pincha SLO va SLA larda ishlatiladi, ya'ni xizmatning kutilgan ishlashi va mavjudligini belgilaydigan shartnomalarda. U misol keltiradi: SLA xizmat medianasi 200 ms dan kam va 99-persentili 1 sekunddan kam bo'lsa ishlayotgan deb hisoblanishini aytishi mumkin, va xizmat vaqtning kamida 99.9 foizida ishlashi talab qilinishi mumkin; bu metrikalar mijoz uchun kutilma belgilaydi va SLA bajarilmasa mijozga pul qaytarishni talab qilish imkonini beradi (1-bob, 15-bet).

Mavjudlik maqsadini "tizim" uchun yozmaslik kerak. Nygard bu yerda juda qat'iy: qog'ozga "tizim vaqtning 99.9 foizida ishlaydi" deb yozish yetarli emas, chunki shu gapning har bir so'zi ortida noaniqlik yashiringan. "Tizim" nima? Agar u trivial bo'lmasa, tarkibida boshqa tizimlarga chaqiruvlar bor, va siz ularning hammasi uchun javobgarlikni olmaysiz; ustiga circuit breaker kabi barqarorlik patternlari ishlatilsa, tizim butun holda ishlab turgan bo'lib, alohida funksiyalar ishlamasligi mumkin. Shuning uchun SLA ni tizim uchun emas, tizimning aniq funksiyalari uchun ta'riflash kerak (13-bob, 230-231-bet). Newman ham funksiyaga qarab farqlashni qo'llaydi: to'lov servisidan talab qilinadigan ishonchlilik ancha yuqori bo'lishi, musiqa tavsiyasi servisi uchun esa ko'proq uzilishga rozi bo'lish mumkin (9-bob, "Cross-Functional Testing").

Mavjudlik ta'rifi o'lchash usulini ham o'z ichiga oladi. Nygard yaxshi ta'rif qadab qo'yishi kerak bo'lgan o'zgaruvchilarni sanaydi: monitoring qurilmasi sintetik tranzaksiyani qanchalik tez-tez bajaradi, tranzaksiyaning har qadami uchun maksimal maqbul javob vaqti qancha, qanday javob kodi yoki matn muvaffaqiyat va qanday javob xato deb hisoblanadi, tekshiruv qancha joydan bajariladi, ma'lumot qayerga yoziladi va mavjudlik foizi qanday formula bilan hisoblanadi, vaqt bo'yichami yoki namuna soni bo'yicha (13-bob, 231-232-bet). U ta'rifning sababini ham aytadi: funksiya ishlab turib yigirma yetti yarim daqiqada javob bersa, foydalanuvchilarning ko'pi uni mavjud deb hisoblamaydi, ellik millisekundda javob berib hammaga xato qaytarsa ham bu mavjudlik emas (13-bob, 231-bet). Shundan kelib chiqib SLI juftligi hosil bo'ladi: muvaffaqiyat ulushi va tezlik ulushi.

Oxirgi nozik joy: o'lchov qayerda olinadi. Kleppmann navbat kechikishi yuqori persentillarda javob vaqtining katta qismini tashkil qilishini va shu effekt sababli javob vaqtini mijoz tomonida o'lchash muhim ekanini aytadi (1-bob, 16-bet).

```yaml
# Prometheus recording rule: SLI ni bitta joyda ta'riflab qo'yamiz.
# Chegara qiymatlari misol uchun: ularni o'z SLO ingizdan oling.
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

Availability SLI si alohida e'tibor talab qiladi, chunki uning o'lchovi so'rov oqimidan emas, sintetik tranzaksiyadan olinadi va shu sababli kelishuvda ko'p joy noaniq qoladi. Nygard SLA ga yoziladigan savollarni sanab beradi va ularning har biri keyinchalik tortishuvga aylanadigan nuqta: sintetik tranzaksiya qanday chastotada yuboriladi; har qadam uchun maksimal javob vaqti qancha; muvaffaqiyat va nosozlik qanday belgilar bilan aniqlanadi; tekshiruv qayerdan va nechta joydan yuboriladi; natija qayerga yoziladi; va availability foizi qaysi formula bilan hisoblanadi (Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 13-bob, 231-bet). Ro'yxat checklist bo'lib ishlaydi: SLA matnida shu olti band yozilmasa, uzilishdan keyin ikki tomon boshqa raqam hisoblaydi va kelishuv ishlamaydi.

| Band | Nima yoziladi | Noaniq qolsa nima bo'ladi |
|---|---|---|
| Chastota | tekshiruv oralig'i va kuzatuv oynasi | bir daqiqalik uzilish bir tomonda ko'rinadi, boshqasida yo'q |
| Qadam bo'yicha chegara | har qadam uchun maksimal javob vaqti | sekin, lekin ishlagan oqim bir tomonda nosozlik, boshqasida emas |
| Muvaffaqiyat belgisi | HTTP kodi va javob tanasidagi aniq marker | 200 qaytargan xato javob muvaffaqiyat deb sanaladi |
| Manba va soni | qaysi joylardan va nechta nuqtadan | bitta nuqtadagi tarmoq muammosi uzilish deb yoziladi |
| Natija joyi | o'lchov qayerda saqlanadi va kim o'qiydi | hisobot paytida ma'lumot topilmaydi |
| Formula | foiz qanday hisoblanadi (vaqt yoki so'rov bo'yicha) | 99.9 ikki tomonda ikki xil raqam beradi |

Sintetik monitoringning texnik tomoni [sintetik monitoring](../patterns/21-observability-patternlari.md#2118-sintetik-monitoring-synthetic-monitoring) yozuvida; bu yerdagi qism faqat kelishuvga yoziladigan bandlar.

## 37.6 Xato byudjeti (error budget) va u qanday qaror qabul qilishga yordam beradi

Newman error budget nima uchun kerakligini sabab bilan boshlaydi: yangi narsa sinaganda tizimga qo'shimcha beqarorlik kiritamiz, shuning uchun barqarorlikni saqlash yoki yaxshilash istagi o'zgarishni tormozlashi mumkin; error budget esa qancha xato maqbul ekanini ochiq aytib shu muammoni chetlab o'tish urinishi (10-bob, "Error budgets").

Hisob SLO dan to'g'ridan to'g'ri chiqadi. Newman misoli: mikroservis chorakda kechayu kunduz asosida 99.9 foiz mavjud bo'lishi kerak deylik, bu amalda chorakda 2 soat 11 daqiqa o'chib turishga ruxsat berilganini bildiradi, va shu SLO doirasida bu sizning error budget ingiz (10-bob). Oynani o'zgartirsangiz raqam o'zgaradi, hisob esa bir xil qoladi: 37.7 dagi jadval yillik, oylik va haftalik qiymatlarni beradi.

So'rov soniga aylantirish ham oddiy arifmetika: SLO 99.9 foiz bo'lsa ruxsat etilgan xato ulushi 0.1 foiz, va oynada 100 million so'rov bo'lsa shu 100 000 ta so'rovga teng.

Byudjetning asosiy foydasi qarorni bahsdan olib qo'yishi. Newman buni ikki tomonlama bayon qiladi: error budget SLO ga qanchalik yetayotganingizni ravshan ko'rsatadi va qanday xavf olishingiz haqida yaxshiroq qaror qabul qilish imkonini beradi; agar chorakda byudjetdan yaxshi pastda bo'lsangiz, ehtimol yangi tilda yozilgan mikroservisni chiqarishga rozi bo'lasiz, agar byudjetni oshirib yuborgan bo'lsangiz, ehtimol o'sha chiqarishni kechiktirib jamoa vaqtining ko'prog'ini tizim ishonchliligini yaxshilashga sarflaysiz. U xulosani shunday yopadi: error budget boshqa hamma narsadan ko'ra jamoalarga yangi narsa sinash uchun nafas olish joyini berish haqida (10-bob, "Error budgets").

Byudjetni kuzatish uchun panel va to'xtash qoidasi kerak. To'xtash chegarasining aniq raqami, ya'ni qoldiq qancha foizga tushganda reliz quvuri to'xtashi, jamoaning o'z siyosati; quyidagi skriptda u misol qiymat bilan berilgan.

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

# Jamoa tanlagan chegara, bu yerda misol uchun 25%.
awk -v q="$QOLDIQ" 'BEGIN { exit (q < 25) ? 1 : 0 }' || {
  echo "BYUDJET TUGAYAPTI: yangi funksiya relizi to'xtatiladi"; exit 1; }
```

Byudjet reliz qarorini faqat uzilish tomonidan yopadi; nuqson tomonida unga juftlik kerak bo'ladi. *Software Engineering at Google* ning boshlanish nuqtasi mukammal binar yo'qligi: o'nlab yirik xususiyatni mustaqil ishlab chiqayotgan o'nlab yoki yuzlab dasturchining ishini birlashtiradigan build da har xatoni tuzatish imkonsiz, shuning uchun har safar savollarni tortib ko'rish kerak bo'ladi, masalan chiziq ikki piksel chapga ko'chgani reklama ko'rinishiga va daromadga ta'sir qiladimi, yoki quti soyasining ozgina o'zgarishi ko'rish qobiliyati cheklangan foydalanuvchiga matnni o'qishni qiyinlashtiradimi. Kitobning javobi mexanizm shaklida: aniq chegaralari bo'lgan asosiy ko'rsatkichlar (KPI) xususiyatni mukammal bo'lmasa ham chiqarishga ruxsat beradi va aks holda bahsli bo'ladigan reliz qarorlarida tiniqlik yaratadi. Shu bog'lanish ham ochiq yozilgan: bu error budget mantiqining o'zi, ya'ni mukammallik kamdan kam eng yaxshi maqsad, qancha xatoga joy borligini tushunib, byudjetning qanchasi sarflanganiga qarab tezlik va barqarorlik o'rtasidagi kelishuv sozlanadi.

Kitobning o'z misoli chegaraning qattiq emasligini ham ko'rsatadi: Filippinda faqat bitta orolda gaplashiladigan kam tarqalgan sheva aniqlangan, unda qidiruv so'rovi berilsa javob o'rniga bo'sh sahifa qaytgan. Savol yirik yangi xususiyat relizini kechiktirishga arziydimi bo'ldi; ma'lumot yig'ilgandan keyin qaror yuqori darajada qabul qilingan va reliz kechiktirilib xato tuzatilgan. Darsi KPI ni bekor qilmaydi, uni to'g'ri joyga qo'yadi: KPI qarorni ma'lumotga asoslangan qiladi, qarorning o'zini avtomatlashtirmaydi.

Amalda bu reliz qaydida ikki qatorni bildiradi: byudjet qoldig'i (foiz) va bloklovchi nuqsonlar ro'yxati har biri uchun chegara qiymati bilan. Chegarasi yozilmagan nuqson "muhim" yoki "muhim emas" bahsiga aylanadi va bahsni tajriba emas, ovoz balandligi yechadi.

## 37.7 Mavjudlik raqamlari: 99.9 va 99.99 orasidagi amaliy farq va narxi

Nygard muzokaraning to'g'ri shaklini beradi: mavjudlik qaroriga to'g'ri yondashuv uni sodda moliyaviy atamalarda qo'yish, ya'ni haqiqiy xarajatni oldi olingan yo'qotishga qarshi qo'yish. U misol ham ko'rsatadi: 98 foiz mavjudlik har oyda 864 daqiqa uzilishga aylanadi; sayt kun cho'qqisida soatiga 1 500 dollar keltirsa, 98 foizda eng yomon holatdagi yo'qotish oyiga taxminan 21 600 dollar, mavjudlikni 99.99 foizga oshirish esa kutilgan uzilish narxini oyiga 108 dollarga tushiradi. O'sha misolda beshyillik hayot davri uchun qo'shimcha narx 98 700 dollarni tashkil qilgan, va Nygard 1 289 520 dollarni tejash uchun 98 700 dollar sarflash puxta moliyaviy tanlov ko'rinishini aytadi (13-bob, 229-230-bet).

Narxning o'sish qonuni ham shu yerda: Nygard har bir qo'shimcha "to'qqiz" joriy etish narxini taxminan o'n barobar, yillik operatsion narxni esa taxminan ikki barobar oshirishini yozadi (13-bob, 230-bet). Bu bobda shundan boshqa narx koeffitsiyenti berilmaydi.

Foizni vaqtga aylantirish arifmetika. Jadvalda yil 365 kun, oy 30 kun deb olingan.

| Mavjudlik | Yillik uzilish | Oylik uzilish | Haftalik uzilish |
|---|---|---|---|
| 99% | 3 kun 15 soat 36 daqiqa | 7 soat 12 daqiqa | 1 soat 40.8 daqiqa |
| 99.5% | 1 kun 19 soat 48 daqiqa | 3 soat 36 daqiqa | 50.4 daqiqa |
| 99.9% | 8 soat 45.6 daqiqa | 43.2 daqiqa | 10.1 daqiqa |
| 99.95% | 4 soat 22.8 daqiqa | 21.6 daqiqa | 5.04 daqiqa |
| 99.99% | 52.6 daqiqa | 4.32 daqiqa | 1.01 daqiqa |
| 99.999% | 5.26 daqiqa | 25.9 soniya | 6.05 soniya |

Amaliy farq shunda. 99.9 foizda oyda 43.2 daqiqa bor, bu bitta sekin deploy yoki bitta qo'lda failover uchun yetadi. 99.99 foizda oyda faqat 4.32 daqiqa bor, bu odam aralashuviga vaqt qoldirmaydi, ya'ni yuqori maqsad tiklashni avtomatlashtirishga majbur qiladi. Kechayu kunduz navbatchilik bunday rejimda zarur bo'lib qoladi: Nygard ta'riflagan tuzilmada saytlarni kecha va dam olish kunlarida kuzatadigan operatsiya markazi yuqori malakali injenerlar bilan kunning yigirma to'rt soati band edi (16-bob, 254-bet). Nosozlikni oldindan sinab ko'rish ham shu darajada zarur: Kleppmann nosozlikka chidamli tizimlarda nosozlik tezligini ataylab oshirish, masalan protsesslarni tasodifiy o'ldirish mantiqiy ekanini yozadi, chunki shunda chidamlilik mexanizmi doimiy mashq qiladi va Netflix Chaos Monkey shu yondashuvning misoli (1-bob, 7-bet).

Eng muhim ogohlantirish: zanjirdagi mavjudlik pasayadi, oshmaydi. Nygard buni SLA Inversion antipatterni sifatida yozadi va hisobini ko'rsatadi: agar tizim beshta tashqi xizmatni talab qilsa va har biri 99.9 foiz mavjudlikka ega bo'lsa, tizimning eng yaxshi erishishi mumkin bo'lgani 99.5 foiz. Umumiy qoidani ham beradi: har bir bog'liqligingiz siz bermoqchi bo'lgan SLA uchun loyihalanmagan bo'lsa, qila oladiganingizning eng yaxshisi eng yomon xizmat ko'rsatuvchingizning SLA si; u buni IT dagi termodinamikaning ikkinchi qonuni deb ataydi, ya'ni xizmat darajalari faqat pasayadi (4-bob, 102-105-bet). Javobi ikkita: past SLA li tizimdan ajralish, ilovani masofaviy tizimsiz ishlaydigan qilish va yumshoq degradatsiya, hamda SLA ni funksiya bo'yicha qayta ta'riflash, chunki tashqi tomonga tayanmagan funksiyalar sizning maksimal SLA ingizni olishi mumkin (4-bob, 104-105-bet).

Kechikish ham shu zanjirda kuchayadi. Kleppmann bitta oxirgi foydalanuvchi so'rovi bir necha orqa chaqiruvni talab qilsa, sekin chaqiruvga tushish ehtimoli oshishini va natijada oxirgi foydalanuvchi so'rovlarining kattaroq ulushi sekin bo'lishini "dum kechikishining kuchayishi" deb nomlaydi (1-bob, 16-bet).

Oxirgi tuzatish zanjir emas, rol haqida: mavjudlik tizim bo'ylab bir xil emas. *Fundamentals of Software Architecture* ning auksion tizimi misoli buni aniq ko'rsatadi. Auksion o'tkazuvchi (auctioneer) ulana olmasa, hech kim taklif bera olmaydi, ya'ni ta'sir butun auksionga tarqaladi. Bitta taklif beruvchi (bidder) ulana olmasa, ta'sir faqat o'shaning o'zida qoladi. Shuning uchun kitob arxitektura xarakteristikalarini butun tizim uchun emas, rol yoki quantum bo'yicha alohida belgilaydi, va natija gibrid arxitektura bo'ladi: bir qismda yuqori mavjudlik va qimmat zaxira, boshqa qismda arzonroq yechim.

SLO yozishda bu amaliy farq keltiradi. "Tizim 99.95 foiz mavjud" degan bitta raqam o'rniga rol bo'yicha jadval yoziladi, va byudjet ham rol bo'yicha hisoblanadi.

| Rol yoki funksiya | Nosozlik ta'siri | SLO va byudjet |
|---|---|---|
| Auksionni boshqarish (auctioneer) | hamma uchun taklif to'xtaydi | eng yuqori SLO, alohida zaxira, eng kichik byudjet |
| Taklif berish (bidder) | faqat shu foydalanuvchi ta'sirlanadi | o'rtacha SLO, qayta urinish va navbat |
| Tarix va hisobot | foydalanuvchi kechiktirilgan ma'lumot ko'radi | eng past SLO, degradatsiya maqbul |

Shu taqsimot [37.8](#378-nofunksional-talabni-biznes-tiliga-ogirish) dagi muloqotni ham osonlashtiradi: suhbat "tizim qancha ishonchli bo'lsin" degan abstrakt savoldan "qaysi funksiya o'chsa biznes qancha yo'qotadi" degan aniq savolga ko'chadi.

## 37.8 Nofunksional talabni biznes tiliga o'girish

Avval atama. Richards va Ford "nofunksional talab" iborasini rad etadi, chunki biror narsani nofunksional deb nomlash tilga salbiy ta'sir beradi: jamoani "nofunksional" narsaga yetarli e'tibor berishga qanday ko'ndirasiz. Ular "sifat atributi" iborasini ham yoqtirmaydi, chunki u dizayn emas, ish tugagandan keyingi sifat bahosini nazarda tutadi, shuning uchun "arxitektura xarakteristikasi" atamasini tanlaydi (4-bob). Newman xuddi shu sababdan "cross-functional requirement" iborasini afzal ko'radi, chunki bu xulqlar faqat ko'p kesishuvchi ishning natijasi sifatida yuzaga keladi (9-bob, "Cross-Functional Testing").

Tarjima muammosi kitobda nomlangan. Richards va Ford yozadi: arxitektura xarakteristikalarining ko'pi asosiy domen vakillarini tinglashdan keladi, lekin muammo shunda, arxitektor va domen vakili boshqa tilda gapiradi; arxitektor masshtablanish, o'zaro ishlash, nosozlikka chidamlilik, o'rganish qulayligi va mavjudlik haqida gapiradi, domen vakili esa qo'shilish va sotib olish, foydalanuvchi qanoati, bozorga chiqish vaqti va raqobat ustunligi haqida. Natijada "tarjimada yo'qolish" muammosi yuzaga keladi. Ular tarjima jadvalini beradi: qo'shilish va sotib olish uchun o'zaro ishlash, masshtablanish, moslashuvchanlik va kengaytirilish; bozorga chiqish vaqti uchun agility, testlanish va joylashtirilish; foydalanuvchi qanoati uchun ishlash, mavjudlik, nosozlikka chidamlilik, testlanish, joylashtirilish, agility va xavfsizlik; raqobat ustunligi uchun agility, testlanish, joylashtirilish, masshtablanish, mavjudlik va nosozlikka chidamlilik; vaqt va byudjet uchun soddalik va amalga oshirilish (5-bob, Table 5-1).

Ular tuzoqni ham ko'rsatadi: agility bozorga chiqish vaqtiga teng emas, u agility plus testlanish plus joylashtirilish, va tarkibning faqat bittasiga diqqat qilish tortga un solishni esdan chiqarishga o'xshaydi (5-bob).

Tarjimadan keyin talab o'lchanadigan shaklga keladi. Richards va Ford o'lchanmaslikning uch sababini sanaydi: ko'p xarakteristika noaniq ma'noga ega va ular fizika emas, bir tashkilot ichida ham bo'limlar ishlash kabi atamani boshqacha ta'riflaydi, va ko'p xarakteristika aslida kichikroq xarakteristikalardan tarkib topgan; obyektiv ta'riflar shu uch muammoni ham hal qiladi va jamoalarga arxitektura atrofida umumiy til beradi (6-bob, "Measuring Architecture Characteristics"). Nygard esa shu obyektivlikning yo'qligini mavjudlik misolida ko'rsatadi: "tizim vaqtning 99.9 foizida ishlaydi" gapining har bir so'zi ortida noaniqlik yashiringan (13-bob, 230-bet).

Tarjima shakli shunday: kim, nima qiladi, qanday tezlikda, qanday yuk ostida, qanday ulushda. "Katalog tez ochilsin" o'rniga: mobil mijozda katalog so'rovlarining belgilangan ulushi belgilangan chegaradan tez javob oladi, belgilangan yuklama ostida. Chegara va ulush raqamlari o'z o'lchovingizdan chiqadi; 37.5 dagi persentil qoidalari qaysi shaklda yozilishini belgilaydi.

Teskari tarjima ham kerak, va unga kitobdagi raqamlar yordam beradi. Kleppmann yuqori persentillarning biznes qiymatini ikki o'lchov bilan ko'rsatadi: Amazon javob vaqtining 100 ms oshishi sotuvni 1 foizga kamaytirishini kuzatgan, boshqalar esa 1 sekundlik sekinlashish mijoz qanoati metrikasini 16 foizga tushirishini xabar qilgan. U Amazon ning ichki servislari uchun javob vaqti talabini 99.9-persentilda ifodalashini ham aytadi, garchi bu mingdan bittasiga tegsa ham, chunki eng sekin so'rovlarga ega mijozlar odatda hisobida eng ko'p ma'lumoti bo'lganlar, ya'ni eng qimmatli mijozlar; shu bilan birga 99.99-persentilni optimallashtirish Amazon maqsadlari uchun juda qimmat va foydasi yetarli emas deb topilgan (1-bob, 15-bet).

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Talab shakli | "Tizim tez va ishonchli bo'lsin" | Obyektiv ta'rif: har bir so'z ortidagi noaniqlik yopiladi (Nygard, 13-bob, 230-bet) |
| Talab nomi | "Nofunksional talab" | Arxitektura xarakteristikasi yoki cross-functional talab (Richards, Ford, 4-bob; Newman, 9-bob) |
| Mavjudlik | "Hech qachon o'chmasin" | Funksiya bo'yicha SLO, uzilish byudjeti daqiqada (Nygard, 13-bob, 230-231-bet) |
| O'lchov | O'rtacha javob vaqti | Persentil va maksimal: o'rtacha dumni yashiradi (Kleppmann, 1-bob, 14-15-bet; Richards, Ford, 6-bob) |
| SLI tanlovi | CPU bandligi | Foydalanuvchi sezadigan o'lchov: CPU savoldan bir qadam uzoq (Newman, 10-bob) |
| Xarajat | Oylik hisobni umumiy ko'rish | Xizmat ko'rsatish narxi tarixiy metrika sifatida (Nygard, 17-bob, 267-bet) |
| Reliz qarori | Har kim o'z fikrini aytadi | Error budget qoldig'i qarorni belgilaydi (Newman, 10-bob) |
| Yangi texnologiya | "Zamonaviy stack" | Bosqichma-bosqich yoyish va metrika bilan qaror (Newman, 7-bob) |
| Rahbarga hisobot | Grafanadagi o'nlab grafik | Hisobot qaror bilan yopiladi (Nygard, 17-bob, 308-309-bet) |

## 37.9 Texnik qarzni biznesga tushuntirish: tezlik va xavf tilida

"Kod iflos" deb gapirish ishlamaydi. Biznes tushunadigan ikki o'lchov bor va ularning ikkisi ham kitobda nomlangan: yetkazib berish tezligi va o'zgarishning nosozlik ulushi. Newman *Accelerate* dagi tadqiqotga tayanib yozadi: yuqori natijali kompaniyalar past natijalilarga qaraganda tez-tez deploy qiladi va bir vaqtda ancha past change failure rate ga ega; "tez yur va narsalarni buzib ket" g'oyasi dasturiy ta'minotni chiqarishda ishlamaydi, tez-tez chiqarish va past nosozlik ulushi yonma-yon yuradi (7-bob, "Progressive Delivery"). Ya'ni texnik qarzni tushuntirishda tezlik va xavf bir-biriga qarshi emas, bir xil yo'nalishda harakat qiladi, va aynan shu gap rahbar bilan suhbatning asosi bo'ladi.

Ikki raqam ham o'zingizdan chiqadi, kitobdan emas: o'zgarishning yetkazib berish vaqti Git tarixidan va reliz quvuridan, change failure rate esa hotfix va incident yozuvlaridan. Ularni modul bo'yicha ajratish qaysi joy pul yo'qotayotganini ko'rsatadi. Bu bobda o'rtacha o'zgarish necha kun olishi yoki hotfix ulushi necha foiz bo'lishi haqida raqam berilmaydi: ular har bazada boshqacha.

Taklifni investitsiya shaklida qo'yish uchun Nygard tayyor namuna beradi: bir martalik 5 000 dollar takrorlanuvchi 200 000 dollarni yo'q qiladi, ya'ni taxminan 4 000 foiz ROI, va u ko'p moliya direktori bunday xarajatni ma'qullashga qarshi bo'lmaydi deb izohlaydi (1-bob, 18-bet). Shakl shunday: bir martalik ish kuni, undan keyin yo'qoladigan takrorlanuvchi xarajat, va to'lanish muddati. Raqamlarni o'z o'lchovingizdan qo'yasiz.

Newman diqqat nomutanosibligini ham ko'rsatadi, va bu texnik qarz suhbatida foydali: u ko'rgan tashkilotlarning ko'pi funksional test to'plamlariga vaqt sarflab, monitoringni yaxshilashga yoki nosozlikdan tiklanishga deyarli hech narsa sarflamaydi, natijada xatolarni to'liq yo'q qila olmaydi va prodda chiqqanda tayyor bo'lmaydi (9-bob).

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| SLO ni darhol 99.99% qilish | Har bir "to'qqiz" joriy etish narxini taxminan o'n barobar, operatsion narxni ikki barobar oshiradi (Nygard, 13-bob, 230-bet) | Haqiqiy o'lchovdan boshlab, bosqichma-bosqich qattiqlashtirish |
| SLI sifatida CPU olish | O'lchov "tizim ishlayaptimi" savolidan bir qadam uzoq (Newman, 10-bob) | Faqat foydalanuvchi sezadigan o'lchovni SLI qilish |
| O'rtacha latency bo'yicha SLO | Og'ir dum yashiriladi, chetga chiqishlar ko'rinmaydi (Kleppmann, 1-bob, 14-bet) | p95, p99 ni chegara bilan yozish va maksimalni ham o'lchash |
| SLA ni SLO ga teng qilish | Reaksiya uchun zaxira qolmaydi; SLO barcha jamoada bajarilsa SLA oshib ketishi kerak (Newman, 10-bob) | SLO ni SLA dan bir pog'ona qattiq qilish |
| Bog'liqlikni hisobga olmaslik | Zanjirdagi xizmat darajalari faqat pasayadi (Nygard, 4-bob, 105-bet) | Ajralish, yumshoq degradatsiya, SLA ni funksiya bo'yicha ta'riflash |
| Chiziqli proyeksiya qilish | Sig'imni bitta cheklov belgilaydi, unga yetilgach navbat o'sadi (Nygard, 8-bob, 162-163-bet) | Cheklovni topib o'lchash |
| DEBUG log prod'da qolishi | Observability xarajati va shovqin o'sadi | Log darajasini konfiguratsiyadan boshqarish |
| Tajribani o'lchovsiz yoyish | Natija bor-yo'qligi noma'lum qoladi | Metrika va to'xtatish shartini oldindan yozish (Newman, 7-bob) |

## 37.10 Qaror uchun arzon o'lchov: kichik tajriba va bosqichma-bosqich yoyish

Iterativ borish arxitektura darajasida ham tavsiya qilinadi. Richards va Ford yozadi: arxitektorlar arxitekturani imkon qadar iterativ qilishga intilishi kerak, chunki arxitekturani osonroq o'zgartira olsangiz, birinchi urinishda aniq to'g'ri narsani topish haqida kamroq tashvishlanasiz; agile ning eng muhim saboqlaridan biri iteratsiyaning qiymati, va bu dasturiy ta'minotning barcha darajasida, arxitektura ham ichida, amal qiladi (4-bob).

Prodda yoyishning shakli Newman'da bor. Canary release konchilar olib kirgan kanareykadan nomlangan: yangi funksiyani mijozlarning cheklangan qismi ko'radi, muammo chiqsa faqat shu qism ta'sirlanadi, funksiya o'sha guruhda ishlasa esa hamma ko'rguncha kengaytiriladi. Newman o'z tajribasini aytadi: birinchi canary relizni qo'lda boshqargan, yangi funksiyani ko'radigan trafik ulushini sozlagan va bir hafta davomida bu ulushni asta oshirib hammaga yetkazgan; o'sha hafta ichida xato ulushi va xato hisobotlarini kuzatib borgan. Hozir bu ko'proq avtomatik bajariladi: masalan Spinnaker metrikalarga qarab chaqiruvlar ulushini oshirib borishi, ya'ni xato ulushi maqbul darajada bo'lsa yangi versiyaga ketadigan chaqiruv foizini ko'tarishi mumkin (7-bob, "Canary Release").

Kleppmann shu amaliyotni odam xatosidan tiklanish ro'yxatiga qo'shadi: yangi kodni bosqichma-bosqich chiqarish kerak, shunda kutilmagan xato foydalanuvchilarning faqat kichik qismiga tegadi (1-bob, 9-10-bet).

Shuning uchun tajriba uchun uchta narsa oldindan yozilishi kerak: qanday metrika o'lchanadi, qanday natija "ha" deb hisoblanadi, qachon to'xtatiladi. Bosqichlarning aniq pog'onasi, ya'ni qanday foizlardan o'tish va har bosqichda qancha kutish, jamoa qarori; Newman misolida bosqichlar bir hafta ichida asta oshgan.

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
# Yoyish jadvali: pog'ona va kutish vaqti jamoa tanlovi, bu yerda misol.
hisobot.yangi-yol.foiz=5

# To'xtatish sharti oldindan yoziladi: chegaralar o'z o'lchovingizdan.
hisobot.yangi-yol.p99-chegara-ms=300
hisobot.yangi-yol.xato-chegara-foiz=0.2

# Yangi yo'l uchun alohida pool: eski yo'lni himoya qiladi.
spring.datasource.hikari.maximum-pool-size=20
hisobot.datasource.hikari.maximum-pool-size=6
hisobot.datasource.hikari.connection-timeout=2000
```

## 37.11 Yetkazib berish muddati va sifat orasidagi muzokarani olib borish

Birinchi tuzatish: tezlik va sifat avtomatik ravishda bir-birining hisobidan kelmaydi. Newman *Accelerate* tadqiqotiga tayanib yozadi: yuqori natijali kompaniyalar ham tez-tez deploy qiladi, ham ancha past change failure rate ga ega, ya'ni tez-tez chiqarish va past nosozlik ulushi yonma-yon yuradi (7-bob). Shuning uchun "muddat qisqa, demak sifatni tushiramiz" degan taklif boshidan noto'g'ri qo'yilgan savol.

Ikkinchi tuzatish: sifat darajasi kontekstdan chiqadi. Newman buni ochiq aytadi: agar siz dasturingizni umuman kimdir ishlatishini aniqlamoqchi bo'lsangiz, g'oyani yoki biznes modelini isbotlash uchun hoziroq biror narsa chiqarish ancha ma'noli bo'lishi mumkin, bunday muhitda testlash haddan ziyod bo'lishi mumkin, chunki g'oya ishlashini bilmaslikning ta'siri prodda xato bo'lishidan ancha yuqori; bunday holatda proddan oldin testlashdan butunlay voz kechish ham o'rinli bo'lishi mumkin (9-bob). Shu bilan birga u teskari tanlovni ham eslatadi: MTBF va MTTR orasidagi tanlov tashkilotga qarab o'zgaradi, va bu asosan prod muhitidagi nosozlikning haqiqiy ta'sirini tushunishga bog'liq (9-bob). Ya'ni arxitektorning vazifasi "sifat darvozasi muzokara mavzusi emas" deb turish emas, balki nosozlikning narxini ochiq qo'yish va darajani shu narxga bog'lash.

Uchinchi tuzatish: tanlovni yashirmaslik. Richards va Ford qoidani beradi: arxitektor hamma xarakteristikani maksimallashtira oladigan holatga kam duch keladi, qaror raqobatlashuvchi talablar orasidagi tanlovga aylanadi, va intilish eng yaxshi arxitekturaga emas, eng kam yomon arxitekturaga qaratiladi (4-bob). Muzokarada bu "nimani yo'qotamiz" savolini ochiq qo'yishga aylanadi.

Amalda eng yaxshi kesish funksiyani butunlay olib tashlash emas, qamrovini qisqartirish: birinchi relizda faqat qisqa davr ma'lumoti, faqat bitta eksport formati, faqat ichki foydalanuvchi uchun. Qancha kesish kerakligi va hotfix to'lqini qancha davom etishi oldingi relizlaringiz ma'lumotidan chiqadi; bu bobda bunday foiz berilmaydi.

## 37.12 Hisobot: rahbarga nima ko'rsatiladi va qanday ko'rinishda

Nygard auditoriyani ajratishdan boshlaydi: turli guruhlar turli nuqtai nazarni talab qiladi va ularning hammasi bir xil ko'rinish bilan qanoatlanmaydi; "qanday ketmoqda" savoli bosh direktordan va tizim administratoridan kelganda butunlay boshqa narsani anglatadi (17-bob, 267-bet). Clements va hammualliflar ham shu fikrni hujjat tomonidan beradi: har bir sifat atributi talabining o'ziga qiziquvchi manfaatdorlar doirasi bor va ular shu talab bajarilishini bilishni xohlaydi (Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Prolog, P.2.3).

Qaysi raqamlar ko'rsatilishi uchun tayanch bor. Nygard tarixiy kuzatuvda biznes metrikalarini, ya'ni mijozlar, buyurtmalar, konversiya ulushi, daromad va xizmat ko'rsatish narxini, tizim metrikalari bilan birga saqlashni tavsiya qiladi (17-bob, 267-bet). U ko'rinish shakli haqida ham gapiradi: tarixiy nuqtai nazar hozirning tezkorligiga ega emas va odatda dashboard ko'rinishi uchun mos emas, kelajakka proyeksiyalar esa nozik ma'lumot bo'lib, ular ham umuman dashboardga qurilmasligi kerak (17-bob, 267, 269-bet). Ya'ni rahbar uchun hisobot panel emas, sahifa.

Qancha raqam olinishi va trend bilan izoh qo'shilishi korpusning amaliy tavsiyasi. Izohning sabab yoki harakatni aytishi esa Nygard talabidan kelib chiqadi: samarali teskari aloqa jarayoni "ma'noli ma'lumotga javob berib harakat qilish" deb ta'riflanadi, tizimdagi shaffoflik faqat ma'lumotga kirish beradi, halqadagi odam esa uni ko'rib talqin qilishi kerak (17-bob, 305-bet).

Hisobot aniq so'rov bilan yopiladi. Nygard halqani yopishning nima ekanini aytadi: har bir ko'rib chiqilayotgan metrika uchun savol qo'yiladi va javob talqin va qarorni yuritishi kerak; qaror hech narsa qilmaslik, resurs qo'shish, mijozlarni haydab yuborish yoki ilova kodini optimallashtirish bo'lishi mumkin, va bu qarorlarning har biri teskari aloqa halqasining muvaffaqiyatli yakuni (17-bob, 308-309-bet). "Ma'lumot uchun" deb tugagan hisobot halqani yopmaydi. Nygard hech kim o'qimaydigan hisobotning narxini ham aytgan: u pul va vaqt yeydi, qiymat bermaydi va soxta xotirjamlik yaratadi (17-bob, 305-bet).

Incident xulosasi ham shu mantiqda: kim aybdor emas, byudjetni nima sarfladi va qaysi ishlar buni qaytarilmas qiladi. Ayblamaydigan post-mortem tuzilishi 35.8 da.

## 37.13 Maqsadga aylangan metrika o'ynaladi: tekshirish va qarshi o'lchov

Metrikani mahsulot tomoni olib keladi, muhandis esa uni so'roq qiladi. Orosz buni ajratuvchi belgi deb nomlaydi: kuchli jamoalarda muhandislar mahsulot odamlari keltirgan KPI va hatto OKR larni so'roq qiladi, va namuna bo'ladigan katta tajribali muhandis uchun bu amaliyot o'z-o'zidan tushunarli (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 21-bob, 294-bet). So'roqning uchta savoli bor: to'g'ri narsa o'lchanyaptimi, bu o'lchov yoki uning maqsadi qanday o'ynalishi mumkin, va muvozanat uchun yana nima o'lchanadi (21-bob, 294-295-bet).

Birinchi savol natijaga qaraydi. Orosz misoli: KPI endpoint kechikishi haqida bo'lsa, kechikishni kamaytirish mijoz va biznes uchun sezilarli farq beradimi, yoki xato ulushini kamaytirish muhimroqmi (21-bob, 294-bet). Bu [nofunksional talabni biznes tiliga o'girish](#378-nofunksional-talabni-biznes-tiliga-ogirish) bo'limidagi tarjimaning teskari yo'nalishi: raqam biznes natijasiga ulanmasa, u shunchaki raqam.

Ikkinchi savol eng amaliysi, chunki o'yin kodga tegmasdan bo'ladi. Orosz Uber dagi ikki holatni keltiradi. Birinchisi: tashkilot hamma endpoint uchun 99.9 foiz ishonchlilikni majburiy qilgach, ishonchliligi maqsaddan ancha past bo'lgan bir necha jamoa ishonchlilikni o'lchash usulining o'zini o'zgartirib maqsadga yetgan, kodga esa hech qanday o'zgarish kiritilmagan. Ikkinchisi: maqsad 500 javob kodlari sonini kamaytirish bo'lganda, bir jamoa mavjud 500 javoblarni 200 ga aylantirib, xato xabarini javob tanasiga ko'chirgan (21-bob, 294-bet).

Ikkala hiyla ham bitta teshikdan o'tadi: o'lchovning ta'rifi jamoa qo'lida qolgan. Himoya [SLI, SLO va SLA farqi](#375-sli-slo-va-sla-farqi-ularni-togri-tanlash) bo'limida yozilgan to'liq ta'rif: nima muvaffaqiyat va nima xato hisoblanadi, qayerdan o'lchanadi va foiz qanday formula bilan chiqadi. Ta'rif bitta joyda, recording rule ichida muzlatilsa, uni jim o'zgartirib bo'lmaydi.

Uchinchi savolning javobi qarshi o'lchov. Orosz ning misoli: maqsad median CPU bandligini 15 foizdan 25 foizga ko'tarish bo'lsa, bu resursdan yaxshiroq foydalanishning proxy metrikasi, lekin kod samarasizlashib CPU ni ko'proq yegani uchun ham raqam ko'tarilishi mumkin; shuning uchun yoniga kod ishlashining bazaviy benchmark i va endpoint larning p50 hamda p95 kechikishi qo'yiladi (21-bob, 295-bet). Oxirgi ogohlantirish ham shu yerda: tizim xarakteristikasini o'lchash mijoz qanoati, mijozning asabiylashuvi yoki nega ketib qolgani kabi narsalarni o'lchashdan ancha oson, va faqat juda aniq o'lchovlarga qarab turish shu muhim tafsilotlarni yo'qotish xavfini tug'diradi (21-bob, 295-bet).

| Maqsad qilingan metrika | Qanday o'ynaladi | Qarshi o'lchov |
|---|---|---|
| Endpoint ishonchliligi 99.9% (Orosz, 21-bob, 294-bet) | O'lchash usuli o'zgartiriladi, kod o'zgarmaydi | SLI ta'rifi bitta recording rule da muzlatiladi |
| 5xx javoblar sonini kamaytirish (o'sha yerda) | Xato 200 javobning tanasiga ko'chiriladi | Muvaffaqiyat biznes natijasi bilan sanaladi |
| Median CPU bandligi 25% (21-bob, 295-bet) | Kod samarasizlashadi, CPU "band" ko'rinadi | Benchmark hamda p50 va p95 kechikish |

```java
// Muvaffaqiyat biznes natijasi bilan o'lchanadi: HTTP status emas,
// to'lovning yakuniy holati. Xatoni 200 javob tanasiga ko'chirish
// bu hisoblagichni ko'tara olmaydi.
@Service
class PaymentOutcomeMetrics {

    private final Counter completed;
    private final Counter rejected;

    PaymentOutcomeMetrics(MeterRegistry registry) {
        this.completed = Counter.builder("payment.outcome")
                .tag("result", "completed")
                .register(registry);
        this.rejected = Counter.builder("payment.outcome")
                .tag("result", "rejected")
                .register(registry);
    }

    void record(PaymentResult result) {
        if (result.completed()) {
            completed.increment();
        } else {
            rejected.increment();
        }
    }
}
```

## 37.14 Amalda qo'llash

- [ ] Uzilishning soatlik narxini biznesdan so'rab olib yozib qo'y: mavjudlik muzokarasi shu raqamsiz bo'sh gap.
- [ ] Bitta arxitektura qarorini bir martalik va takrorlanuvchi xarajatga ajratib yoz, keyin uch yoki besh yillik umumiy egalik narxini hisobla.
- [ ] Eng yuqori trafikli servis uchun oylik xarajatni so'rov soniga bo'lib, bitta so'rovning narxini raqam bilan yozib qo'y va uni tarixiy metrika sifatida saqlay boshla.
- [ ] `pg_stat_user_indexes` dan kam ishlatiladigan indekslarni topib, ularning umumiy hajmini va oylik saqlash narxini hisobla.
- [ ] Asosiy biznes oqimi uchun ikkita SLI ta'rifla: muvaffaqiyat ulushi va persentil chegarasi, ikkalasini recording rule sifatida yoz.
- [ ] SLI ta'rifini to'liq yoz: tekshiruv qanchalik tez-tez bajariladi, maksimal maqbul javob vaqti qancha, nima muvaffaqiyat, nima xato, qancha joydan o'lchanadi va foiz qanday formula bilan hisoblanadi.
- [ ] SLO ni "tizim" uchun emas, aniq funksiyalar uchun yoz, va har bir funksiya uchun tashqi bog'liqlikning SLA sini tekshir.
- [ ] SLO qiymatini tanlab, uni yillik va oylik uzilish daqiqasiga aylantir, va bu raqamni jamoa bilan kelish.
- [ ] Error budget qoldig'ini ko'rsatadigan dashboard paneli qo'sh va reliz to'xtash chegarasini jamoa bilan rasmiylashtir.
- [ ] Bitta nofunksional talabni o'lchanadigan shaklga aylantir: yuk, ulush va chegara bilan; o'rtacha emas, persentil bilan yoz.
- [ ] Eng og'riqli modul uchun yetkazib berish vaqti va change failure rate ni Git tarixi va hotfix yozuvlaridan hisoblab, texnik qarz taklifini to'lanish muddati bilan yoz.
- [ ] Rahbar uchun bir sahifali shablon tayyorla: oz sonli raqam, trend, sabab yoki harakatni aytadigan izoh va bitta aniq qaror so'rovi.

## Manbalar

- Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 1-nashr, Pragmatic Bookshelf, 2007, 1-bob (17-18-bet) - dizayn qarori moliyaviy qaror ekani, bir martalik xarajatni takrorlanuvchi xarajat hisobidan chetlab o'tishning mantiqsizligi, 5 000 dollar va 200 000 dollar misoli hamda taxminan 4 000 foiz ROI, uzilishning soatiga 100 000 dollardan oshadigan narxi, 98 va 99.99 foiz orasidagi yillik 17 million dollar farq
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 4-bob (102-105-bet) - SLA Inversion: beshta 99.9 foizli bog'liqlik bilan eng yaxshi natija 99.5 foiz, "xizmat darajalari faqat pasayadi", javoblari ajralish, yumshoq degradatsiya va SLA ni funksiya bo'yicha ta'riflash
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 8-bob (162-163-bet) - sig'imdagi nochiziqli effektlar, chiziqli proyeksiya tuzog'i, sig'imni bitta cheklov belgilashi va cheklovga yetilgach navbat o'sishi
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 13-bob (229-232-bet) - mavjudlikni haqiqiy xarajat va oldi olingan yo'qotish sifatida qo'yish, 98 foizdan 99.99 foizga o'tish hisobi, har bir "to'qqiz" joriy etish narxini o'n barobar va operatsion narxni ikki barobar oshirishi, "tizim 99.9 foizda ishlaydi" gapining noaniqligi, SLA ni funksiya bo'yicha yozish, mavjudlik ta'rifi uchun sintetik tranzaksiya va formula o'zgaruvchilari
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 16-bob (254-bet) - kechayu kunduz ishlaydigan operatsiya markazi tuzilmasi
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 17-bob (267-269, 305-309-bet) - auditoriyaga qarab nuqtai nazar, biznes metrikalari ro'yxatida xizmat ko'rsatish narxi, tarixiy va proyeksiya ma'lumotining dashboardga mos emasligi, hech kim o'qimaydigan hisobotning soxta xotirjamligi, teskari aloqa "ma'noli ma'lumotga javob berib harakat qilish", trend va chetga chiqishni kuzatish, oyiga bir marta ma'lumot hajmi va so'rov statistikasini ko'rish, halqa qaror bilan yopilishi
- Sam Newman, *Building Microservices*, 2-nashr, O'Reilly, 2021, 7-bob - progressive delivery, *Accelerate* natijasi (tez-tez deploy va past change failure rate yonma-yon), deployment va release ni ajratish, canary release va bir hafta ichida ulushni asta oshirish, Spinnaker ning metrikaga qarab avtomatik ko'tarishi
- Sam Newman, *Building Microservices*, 2-nashr, 2021, 9-bob - "cross-functional requirement" atamasi, servisga qarab farqli ishonchlilik talabi, MTBF va MTTR tanlovi, nosozlik ta'siri past bo'lgan kontekstda proddan oldingi testni qisqartirish mumkinligi, tashkilotlarning tiklanishga kam sarflashi
- Sam Newman, *Building Microservices*, 2-nashr, 2021, 10-bob - SLA, SLO, SLI ta'riflari va AWS yakka instansiya misoli, CPU kabi o'lchovning "tizim ishlayaptimi" savolidan uzoqligi, error budget ta'rifi, chorakda 99.9 foiz uchun 2 soat 11 daqiqa, byudjet qoldig'iga qarab xavf olish va reliz kechiktirish, byudjetning "nafas olish joyi" roli
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 1-bob (6-16-bet) - bulutda instansiyaning ogohlantirishsiz ishdan chiqishi odatiyligi, tugunni birin-ketin uzilishsiz yangilash, Chaos Monkey va nosozlikni ataylab chaqirish, yangi kodni bosqichma-bosqich chiqarish, o'rtachaning tanqidi va p95/p99/p999, dum kechikishining foydalanuvchiga ta'siri, persentilning SLO va SLA dagi o'rni va pul qaytarish sharti, Amazon ning 100 ms va 1 foiz hamda 1 sekund va 16 foiz o'lchovlari, p99.9 tanlovi va p99.99 ning qimmatligi, navbat kechikishi va o'lchovni mijoz tomonida olish
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 21-bob (294-295-bet) - kuchli jamoalarda muhandislar KPI va OKR larni so'roq qilishi, uchta tekshiruv savoli (to'g'ri narsa o'lchanyaptimi, o'lchov qanday o'ynaladi, qarshi o'lchov nima), Uber dagi 99.9 foiz ishonchlilik majburiyatida o'lchash usulining o'zgartirilishi va 500 javoblarning 200 ga aylantirilishi, median CPU bandligini 15 foizdan 25 foizga ko'tarish maqsadiga benchmark hamda p50 va p95 qarshi o'lchovi, tizim xarakteristikasini o'lchash mijoz qanoatini o'lchashdan oson ekani
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 4-bob - "nofunksional talab" va "sifat atributi" atamalarining rad etilishi, arxitektura xarakteristikalarining bir-biriga ta'siri va tanlov, "eng kam yomon arxitektura", arxitekturani iterativ qilish tavsiyasi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 2020, 5-bob (Table 5-1) - arxitektor va biznes tilining "tarjimada yo'qolish" muammosi, domen tashvishlarini arxitektura xarakteristikalariga tarjima jadvali, agility bozorga chiqish vaqtiga teng emasligi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 2020, 6-bob - xarakteristikalarning noaniq, turlicha ta'riflangan va tarkibli bo'lishi, obyektiv ta'rifning shu uch muammoni hal qilishi, faqat o'rtachani o'lchash tuzog'i va maksimalni o'lchash
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2011, Prologue (P.2.3) - har sifat atributi talabining manfaatdorlar doirasi bo'lishi va ularning talab bajarilishini bilishni xohlashi, sifat chegaralarining interfeys hujjatida Quality of Service shaklida yozilishi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 24-bob ("No Binary Is Perfect" bo'limi) - mukammal binar yo'qligi va har relizda kelishuv qilish zarurati, aniq chegaralari bo'lgan asosiy ko'rsatkichlar (KPI) kamchilikli relizga ruxsat berishi va bahsli qarorlarda tiniqlik yaratishi, error budget bilan bog'lanishi, hamda Filippindagi bitta orol shevasi misolida relizni kechiktirish qarori
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 7-bob ("Case Study: Going, Going, Gone") - mavjudlik tizim bo'ylab bir xil emasligi (auksion o'tkazuvchi ulanmasa hamma uchun taklif to'xtashi, bitta taklif beruvchi ulanmasa faqat o'zi ta'sirlanishi) va xarakteristikalarni rol hamda quantum bo'yicha belgilash gibrid arxitekturaga olib kelishi. Qo'limizdagi nusxada chop etilgan bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- ESLATMA: 37.6 dagi reliz qaydidagi ikki qator tavsiyasi va 37.7 dagi rol bo'yicha SLO jadvali shu korpusning qo'shimchasi
- ESLATMA: 37.1 dagi litsenziyaning CPU yoki node soniga bog'lanishi haqidagi kuzatuv, 37.6 dagi 25 foizli to'xtash chegarasi, 37.10 dagi yoyish pog'onalari va kutish vaqti, 37.12 dagi raqam soni va bir sahifa shakli shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 37.2, 37.3, 37.4 va 37.9 dagi barcha dollar va foiz qiymatlari misol uchun berilgan arifmetika kirishlari, o'lchangan qoida emas: ularni o'z hisob-fakturangizdan va o'z o'lchovingizdan olish kerak
- Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 13-bob (231-bet) - availability ni sintetik tranzaksiya bilan avtomatik tekshirish va SLA da aniq yozilishi kerak bo'lgan bandlar: chastota, har qadam uchun maksimal javob vaqti, muvaffaqiyat va nosozlik belgilari, qayerdan va nechta joydan, natija qayerga yoziladi, foiz qaysi formula bilan hisoblanadi

---

[&larr; 36. Code review va jamoada texnik yetakchilik](36-code-review-va-jamoada-texnik-yetakchilik.md) · [Mundarija](README.md) · [38. Doimiy o'rganish va texnologiya tanlash &rarr;](38-doimiy-organish-va-texnologiya-tanlash.md)
