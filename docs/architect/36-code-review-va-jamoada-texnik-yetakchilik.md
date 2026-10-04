<!-- doc: architect | chapter: 36 | part: VI. Amaliyot va o'sish -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 36. Code review va jamoada texnik yetakchilik (Code Review and Technical Leadership)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [36.1 Code review nimani topishi kerak: xatti-harakat, chegara, nom, xavfsizlik](#361-code-review-nimani-topishi-kerak-xatti-harakat-chegara-nom-xavfsizlik)
- [36.2 Nimani topmasligi kerak: formatlash, uslub, mashina tekshiradigan narsalar](#362-nimani-topmasligi-kerak-formatlash-uslub-mashina-tekshiradigan-narsalar)
- [36.3 Izoh yozish uslubi: muammoni ko'rsat, qaror egasini qoldirib ket](#363-izoh-yozish-uslubi-muammoni-korsat-qaror-egasini-qoldirib-ket)
- [36.4 Majburiy va ixtiyoriy izohlarni ajratish](#364-majburiy-va-ixtiyoriy-izohlarni-ajratish)
- [36.5 Review hajmi: katta o'zgarishni bo'lish va navbat vaqtini qisqartirish](#365-review-hajmi-katta-ozgarishni-bolish-va-navbat-vaqtini-qisqartirish)
- [36.6 Kelishmovchilikni hal qilish: dalil, prototip, uchinchi fikr](#366-kelishmovchilikni-hal-qilish-dalil-prototip-uchinchi-fikr)
- [36.7 Yangi odamga review orqali o'rgatish](#367-yangi-odamga-review-orqali-orgatish)
- [36.8 Arxitektura qarorlarini jamoaga tarqatish: hujjat, ichki suhbat, namuna kod](#368-arxitektura-qarorlarini-jamoaga-tarqatish-hujjat-ichki-suhbat-namuna-kod)
- [36.9 Standart o'rnatish: linter, formatlash, ArchUnit qoidalari, shablon loyiha](#369-standart-ornatish-linter-formatlash-archunit-qoidalari-shablon-loyiha)
- [36.10 Jamoaning bilim xaritasi va bitta odamga bog'liqlikni kamaytirish](#3610-jamoaning-bilim-xaritasi-va-bitta-odamga-bogliqlikni-kamaytirish)
- [36.11 Texnik yetakchi va menejer roli farqi](#3611-texnik-yetakchi-va-menejer-roli-farqi)
- [36.12 Vaqtni taqsimlash: kod, hujjat, suhbat, o'rganish](#3612-vaqtni-taqsimlash-kod-hujjat-suhbat-organish)
- [36.13 Amalda qo'llash](#3613-amalda-qollash)

</details>


Code review arxitektorning eng arzon va eng ta'sirli vositasi. U kod birlashishdan oldin ishlaydi, shuning uchun bitta izoh keyinchalik haftalarcha ketadigan migratsiyani to'xtatishi mumkin. Lekin ko'p jamoada review bo'sh marosimga aylanadi: odamlar probel va o'zgaruvchi nomi haqida bahslashadi, tranzaksiya chegarasi va pul turini esa hech kim ko'rmaydi. Bu bob review ichida nimani qidirish kerakligini, izohni qanday yozishni va texnik yetakchi o'z vaqtini qanday taqsimlashini ko'rsatadi.

## 36.1 Code review nimani topishi kerak: xatti-harakat, chegara, nom, xavfsizlik

Review diqqati to'rtta narsaga qaratilishi kerak. Birinchisi xatti-harakat: kod aytilgan ishni qiladimi, chegara holatlarida nima bo'ladi, xato yo'lida qanday javob qaytadi. Ikkinchisi chegara: tranzaksiya qayerda ochiladi va yopiladi, tashqi HTTP chaqiruv tranzaksiya ichida qolib ketmaganmi, cache invalidatsiyasi commit dan keyin bo'ladimi. Uchinchisi nom: metod nomi uning yon ta'sirini yashirmayaptimi, domen atamasi kodda bir xil ishlatilayaptimi. To'rtinchisi xavfsizlik: autorizatsiya tekshiruvi qayerda, log ichiga karta raqami yoki token tushmayaptimi, SQL parametrlanganmi.

Eng ko'p uchraydigan muammo pul va vaqt bilan ishlashda. `double` bilan hisoblangan summa ikki yildan keyin hisobotda tiyin farqi beradi, va bu farqni topish bir hafta oladi.

```java
// REVIEW TOPISHI KERAK: pul double bilan, yaxlitlash qoidasi yo'q,
// tashqi chaqiruv tranzaksiya ichida, xatolik yutilgan.
@Transactional
public void charge(Long orderId, double amount) {
    Order order = orderRepository.findById(orderId).orElseThrow();
    double fee = amount * 0.029;              // komissiya suzuvchi nuqtada
    gatewayClient.charge(order.getCardToken(), amount + fee); // 3 sekund kutadi
    order.setStatus(PAID);
    log.info("to'lov: karta={} summa={}", order.getCardToken(), amount); // token logda
}
```

Shu o'n qatorda to'rtta alohida muammo bor va ularning har biri boshqa toifaga tegishli: hisob aniqligi, tranzaksiya chegarasi, kutish vaqti, maxfiy ma'lumot. Review izohi ham to'rtta alohida izoh bo'lishi kerak, chunki ularni bitta izohda aralashtirsang muallif faqat birinchisini tuzatadi.

```java
// TUZATILGAN: pul BigDecimal, gateway chaqiruvi tranzaksiyadan tashqarida,
// holat o'zgarishi alohida qisqa tranzaksiyada, logda faqat maskalangan qism.
public void charge(Long orderId, BigDecimal amount) {
    ChargeCommand cmd = orderService.prepareCharge(orderId, amount); // qisqa tranzaksiya
    GatewayResult result = gatewayClient.charge(cmd);                // tashqarida
    orderService.applyResult(orderId, result);                       // ikkinchi tranzaksiya
}

@Transactional
ChargeCommand prepareCharge(Long orderId, BigDecimal amount) {
    Order order = orderRepository.findByIdForUpdate(orderId).orElseThrow();
    BigDecimal fee = amount.multiply(FEE_RATE).setScale(2, RoundingMode.HALF_UP);
    order.markChargePending();
    return new ChargeCommand(order.maskedCard(), amount.add(fee), order.idempotencyKey());
}
```

## 36.2 Nimani topmasligi kerak: formatlash, uslub, mashina tekshiradigan narsalar

Odam review qilgan narsa qimmat turadi. Shuning uchun mashina topa oladigan hech narsani odam izohlamasligi kerak. Probel, qavs joyi, import tartibi, `final` qo'yish, satr uzunligi, ishlatilmagan o'zgaruvchi: bularning hammasi formatter va static analyzer ishi. Agar review da shunday izoh paydo bo'lsa, bu kod muammosi emas, pipeline muammosi. To'g'ri javob izoh yozish emas, qoidani CI ga ko'chirish.

```yaml
# .github/workflows/quality.yml - review ga kelgunga qadar ishlaydi
name: quality
on: [pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: maven
      # formatlash: buzilsa build qizil bo'ladi, odam izoh yozmaydi
      - run: ./mvnw -B spotless:check
      # statik tahlil: null yo'li, resource yopilmagan, taxminiy xatolar
      - run: ./mvnw -B verify -Perrorprone,spotbugs
      # arxitektura qoidalari: qatlam buzilishi
      - run: ./mvnw -B test -Dtest='Arch*Test'
```

Shuningdek review da uslub ta'mi haqida bahs qilmaslik kerak. "Men bu yerda stream emas, for loop ni afzal ko'raman" degan izoh muallifning vaqtini oladi va hech narsani yaxshilamaydi. Agar ikkita variant o'qilish darajasida teng bo'lsa, muallif variantini qoldir.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Import tartibi buzilgan | Review da izoh yoziladi | Spotless CI da majburlaydi, izoh yo'q |
| 900 qatorli PR keldi | Bir hafta turadi, keyin "LGTM" | Muallif bilan 3 ta PR ga bo'linadi |
| Tranzaksiya ichida HTTP chaqiruv | Ko'rinmaydi, chunki diqqat uslubda | Birinchi navbatdagi majburiy izoh |
| Muallif bilan kelishmovchilik | Kim baland ovozda gapirsa, u yengadi | O'lchov yoki prototip dalil beradi |
| Yangi odam PR yuboradi | 30 ta mayda izoh, ruhi tushadi | 3 ta muhim izoh, qolgani birga suhbat |
| Arxitektura qarori qabul qilindi | Chatda aytiladi va yo'qoladi | ADR yoziladi, shablonda namuna kod paydo bo'ladi |
| Faqat bitta odam Kafka ni biladi | Hamma unga yo'naltiriladi | Bilim xaritasi, juftlik review, rotatsiya |
| Yetakchi hamma PR ni o'zi ko'radi | Navbat yetakchiga tiqiladi | Qoidalar avtomatlashtiriladi, review tarqatiladi |
| Review javob vaqti 2 kun | "Band edim" deyiladi | Kuniga ikki marta review oynasi belgilanadi |
| Hisobot query sekin ishlaydi | Keyin optimallashtiramiz deyiladi | PR da EXPLAIN natijasi talab qilinadi |

## 36.3 Izoh yozish uslubi: muammoni ko'rsat, qaror egasini qoldirib ket

Yaxshi izoh uchta qismdan iborat: nima ko'rdim, nega bu muhim, qaysi yo'nalishda o'ylash kerak. Yechimni buyruq shaklida yozmaslik kerak, chunki kodni muallif yozadi va kontekstni u yaxshi biladi. "Bu yerni ChangeStreamListener ga o'tkaz" degan izoh muallifni ijrochiga aylantiradi. "Bu listener commit dan oldin ishga tushadi, shuning uchun rollback bo'lsa cache eski emas, yangi qiymatni ushlab qoladi. Qanday hal qilsak yaxshi bo'ladi?" degan izoh muallifni o'ylashga majbur qiladi va u ko'pincha sendan yaxshiroq variant topadi.

Izohda nega ekanini ko'rsatish yagona eng muhim odat. "BigDecimal ishlat" o'rniga "to'lov summasi hisobotda tiyingacha mos kelishi kerak, suzuvchi nuqta uchta amaldan keyin farq beradi" deb yoz. Birinchi izoh bitta qatorni tuzatadi, ikkinchisi odamni o'zgartiradi va keyingi PR da shu muammo bo'lmaydi.

Savol shaklidagi izoh ikki tomonga ham xizmat qiladi. Agar sen xato qilgan bo'lsang, savol shakli sening obro'yingni saqlaydi. Agar muallif xato qilgan bo'lsa, savol unga o'zi topish imkonini beradi.

## 36.4 Majburiy va ixtiyoriy izohlarni ajratish

PR da yigirma izoh bo'lsa, muallif qaysi biri birlashishga to'sqinlik qilayotganini bilmaydi. Shuning uchun har bir izohga prefiks qo'yish kerak. Men to'rtta darajani ishlataman: `blocker` (bu holatda birlashtirmaymiz), `kerak` (birlashishdan oldin tuzatiladi), `fikr` (o'ylab ko'r, qaror senda), `maqtov` (yaxshi yechimni ko'rsatish). Oxirgisi bo'sh narsa emas: u review ni jazo mexanizmidan o'rgatish mexanizmiga aylantiradi.

| Prefiks | Ma'nosi | Misol |
|---|---|---|
| `blocker` | Ma'lumot yo'qoladi yoki xavfsizlik buzildi | Autorizatsiya tekshiruvi yo'q |
| `kerak` | Xatti-harakat yoki chegara noto'g'ri | Tranzaksiya ichida tashqi chaqiruv |
| `fikr` | Yaxshilash mumkin, qaror muallifda | Bu metodni ikkiga bo'lish mumkin |
| `maqtov` | Qayta ishlatilishi kerak bo'lgan yechim | Idempotency key dizayni yaxshi |

Agar PR da uchdan ko'p `blocker` bo'lsa, izoh yozishni to'xtat va 15 daqiqalik suhbat taklif qil. Ko'p blocker odatda noto'g'ri tushunilgan talab belgisi, va uni yozma izohlar bilan hal qilish bir necha kun oladi.

## 36.5 Review hajmi: katta o'zgarishni bo'lish va navbat vaqtini qisqartirish

Review sifati PR hajmiga teskari proportsional. Taxminan 200 qatordan keyin odam diqqati tushadi, 400 qatordan keyin review amalda faqat imzo bo'lib qoladi. Shuning uchun arxitektorning ishi review paytida boshlanmaydi, u PR tuzilishidan boshlanadi. Katta o'zgarishni uchta tabiiy qatlamga bo'lish mumkin: birinchi PR da yangi interfeys va migratsiya skripti, ikkinchisida implementatsiya, uchinchisida eski yo'lni o'chirish.

```bash
# Katta branch ni ketma-ket PR larga bo'lish
git switch -c refactor/payment-base main
git cherry-pick <migratsiya-commit> <interfeys-commit>   # 1-PR: skelet
git push -u origin refactor/payment-base

git switch -c refactor/payment-impl refactor/payment-base
git cherry-pick <implementatsiya-commitlari>             # 2-PR: mantiq
git push -u origin refactor/payment-impl

# Review navbat vaqtini o'lchash: ochilishdan birinchi izohgacha
gh pr list --state merged --limit 50 \
  --json number,createdAt,mergedAt,additions \
  | jq -r '.[] | [.number, .additions,
      ((.mergedAt|fromdate) - (.createdAt|fromdate))/3600 | floor] | @tsv'
```

Navbat vaqti review ning yashirin narxi. Agar PR ikki kun kutsa, muallif boshqa ishga o'tadi va kontekstni yo'qotadi, qaytib kelganda tuzatish uch barobar qimmat. Kuniga ikki marta belgilangan review oynasi (masalan ertalab va tushdan keyin) navbatni odatda bir necha soatga tushiradi. 200 qatorlik PR uchun maqsad: birinchi javob 4 soat ichida.

## 36.6 Kelishmovchilikni hal qilish: dalil, prototip, uchinchi fikr

Texnik bahsning aksariyati fakt yetishmasligidan emas, bir xil faktni turlicha o'lchashdan kelib chiqadi. Birinchi qadam bahsni o'lchanadigan savolga aylantirish. "Bu query sekin" degan fikr bahsga olib keladi, `EXPLAIN (ANALYZE, BUFFERS)` natijasi bahsni tugatadi.

```sql
-- Bahsni tugatadigan dalil: rejani va haqiqiy vaqtni ko'rsat
EXPLAIN (ANALYZE, BUFFERS)
SELECT o.id, o.created_at, SUM(i.qty * i.unit_price) AS total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.warehouse_id = 42
  AND o.created_at >= now() - interval '30 days'
GROUP BY o.id, o.created_at
ORDER BY o.created_at DESC
LIMIT 100;

-- Indeks qo'yilgandan keyin rejani qayta oling va PR izohiga ikkisini qo'ying.
CREATE INDEX CONCURRENTLY idx_orders_wh_created
    ON orders (warehouse_id, created_at DESC);
```

Agar o'lchov imkonsiz bo'lsa, ikkinchi qadam vaqt chegarasi bilan prototip. Ikki tomon ham yarim kun ichida eng kichik ishlaydigan variantini yozadi va uchrashuvda ikkisini solishtiradi. Uchinchi qadam uchinchi odamni chaqirish, lekin uning roli hakam emas, savol beruvchi. Agar bahs baribir hal bo'lmasa, qaytarilishi oson variantni tanlash kerak: xato variantni bir hafta ichida qaytarish, to'g'ri variantni bir oy kutishdan arzon. Qaror qabul qilinganda uni va sababini yozib qo'y, aks holda uch oydan keyin bir xil bahs qaytadi.

## 36.7 Yangi odamga review orqali o'rgatish

Yangi odamning birinchi PR si uchun qoida oddiy: uchtadan ko'p izoh yozma. Qolgan muammolarni ro'yxatga ol va keyingi PR larga tarqat. Bu yumshoqlik emas, hisob-kitob: bir vaqtda uchta narsadan ko'pini o'rganib bo'lmaydi.

Ikkinchi qoida izoh ichida havola qoldirish. "Biz bu yerda doim idempotency key ishlatamiz, mana shu servisda namunasi bor" degan izoh kodni ham tuzatadi, ham kodbazani o'rgatadi. Uchinchi qoida teskari yo'nalish: yangi odamga katta PR ni review qilishni berish. U savol berishga majbur bo'ladi va o'sha savollar sening hujjatlaringdagi bo'shliqni ko'rsatadi.

Taxminan uch oydan keyin yangi odam o'z sohasida review qila oladigan darajaga chiqishi kerak. Agar chiqmasa, bu uning qobiliyati emas, sening o'rgatish tizimining muammosi.

## 36.8 Arxitektura qarorlarini jamoaga tarqatish: hujjat, ichki suhbat, namuna kod

Qaror uch kanalda tarqalmasa, u mavjud emas. Birinchi kanal yozma qaror hujjati: kontekst, variantlar, tanlangan yo'l, oqibatlar, qachon qayta ko'riladi. Bir sahifadan oshmasligi kerak, aks holda o'qilmaydi. Ikkinchi kanal og'zaki: 20 daqiqalik ichki suhbat, unda savollar beriladi va hujjat yaxshilanadi. Uchinchi va eng kuchli kanal namuna kod: qarorga mos keladigan bitta haqiqiy servis, odamlar undan nusxa oladi.

Faqat hujjat yozish eng ko'p uchraydigan xato. Odamlar hujjat emas, qo'shni paket kodidan nusxa oladi. Shuning uchun qaror qabul qilingandan keyin birinchi ish bitta haqiqiy joyni yangi yo'lga o'tkazish, va PR tavsifida "bu yangi standart, keyingi servislar shunday qiladi" deb yozish.

## 36.9 Standart o'rnatish: linter, formatlash, ArchUnit qoidalari, shablon loyiha

Yozma qoida esdan chiqadi, bajarilishi majburlangan qoida qolaveradi. Shuning uchun har bir takrorlanadigan review izohini mashinaga o'tkazish kerak. Qatlam chegaralari uchun ArchUnit eng arzon vosita.

```java
@AnalyzeClasses(packages = "com.shop", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureTest {

    // Controller to'g'ridan-to'g'ri repository ga kirmasin: faqat service orqali
    @ArchTest
    static final ArchRule controller_service_orqali_ishlaydi =
        noClasses().that().resideInAPackage("..web..")
            .should().dependOnClassesThat().resideInAPackage("..repository..");

    // Domen paketi Spring ga va JPA ga bog'lanmasin: toza domen qoidasi
    @ArchTest
    static final ArchRule domen_toza_qolsin =
        noClasses().that().resideInAPackage("..domain.model..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("org.springframework..", "jakarta.persistence..");

    // Pul maydonlari uchun double ishlatilmasin
    @ArchTest
    static final ArchRule pul_bigdecimal_bilan =
        noFields().that().haveNameMatching(".*(amount|price|total)")
            .should().haveRawType(Double.class).orShould().haveRawType(double.class);
}
```

Shablon loyiha standartning eng tez tarqaladigan ko'rinishi. Ichida tayyor bo'lishi kerak: observability sozlamasi, xato javobi formati, migratsiya vositasi, test bazasi konfiguratsiyasi, CI pipeline. Yangi servis birinchi kundan to'g'ri skeletda tug'iladi.

```properties
# Shablon loyihaning asosiy sozlamalari: har bir yangi servis shu yerdan boshlanadi
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.connection-timeout=3000
spring.jpa.open-in-view=false
spring.jpa.properties.hibernate.jdbc.batch_size=50
# n+1 muammosini test paytida ko'rinadigan qilish
spring.jpa.properties.hibernate.query.fail_on_pagination_over_collection_fetch=true
management.endpoints.web.exposure.include=health,info,prometheus
management.endpoint.health.probes.enabled=true
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=25s
```

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Review faqat formatlash haqida | CI da formatter yo'q | Spotless va pre-commit hook qo'yish |
| "LGTM" bilan 800 qator o'tadi | PR hajmi chegarasi yo'q | Hajm bo'yicha ogohlantirish, PR ni bo'lish |
| Bir xil izoh har hafta qaytadi | Qoida odam xotirasida | ArchUnit yoki custom lint qoidasi |
| Qaror uch oydan keyin yo'qoladi | Faqat chatda aytilgan | Qisqa qaror hujjati va namuna kod |
| Yetakchi review bottleneck | Hamma PR unga yo'naltirilgan | Soha egalari, CODEOWNERS taqsimoti |
| Yangi odam sekin o'sadi | PR da 30 izoh, prioritet yo'q | Uchta izoh qoidasi va prefikslar |
| Migratsiya yarim yo'lda qoladi | Eski yo'l o'chirilmagan | Oxirgi PR da eski kodni o'chirish sharti |
| Faqat bitta odam domenni biladi | Review doim bir odamda | Juftlik review va rotatsiya |

## 36.10 Jamoaning bilim xaritasi va bitta odamga bog'liqlikni kamaytirish

Har bir yetakchi o'z jamoasining bilim xaritasini yozib qo'yishi kerak: qaysi tizimni kim chuqur biladi, kim o'rtacha biladi, kim umuman bilmaydi. Xarita tayyor bo'lgach, eng xavfli hujayralar ko'rinadi: muhim tizim, uni faqat bitta odam biladi. Bu odam ta'tilga chiqsa yoki ishdan ketsa, jamoa to'xtaydi.

Kamaytirish usullari amaliy. Review ni shu sohada ikkinchi odamga berish, lekin birinchi odamni ham qo'shish. Incident dan keyin tahlilni boshqa odam yozishi. To'lov yoki ombor qoldig'i kabi kritik tizimda har chorakda bitta o'rtacha hajmli ishni "bilmaydigan" odamga berish va birinchi odamni maslahatchi qilish. Maqsad: har bir kritik tizimda kamida ikkita odam ishonchli o'zgartirish kirita olishi.

## 36.11 Texnik yetakchi va menejer roli farqi

Ikki rol aralashganda ikkisi ham buziladi. Menejer odamlar uchun javob beradi: o'sish, ish taqsimi, baho, konfliktlar. Texnik yetakchi tizim uchun javob beradi: arxitektura, sifat darvozalari, texnik qarzni boshqarish, qaror sifati. Yetakchining vakolati lavozimdan emas, ishonchdan keladi, va ishonch kod yozish bilan saqlanadi.

Eng muhim farq ta'sir usulida. Menejer qaror qabul qilib buyruq berishi mumkin. Yetakchi esa odamlarni ishontirishi kerak, chunki uning qo'lida majburlash vositasi yo'q. Shuning uchun yetakchining asosiy quroli dalil, prototip va yozma hujjat. Agar yetakchi "men shunday dedim" ga tayansa, u menejer rolini noto'g'ri o'zlashtirgan bo'ladi.

Bir xil narsada ikki rol birlashadi: ikkisi ham odamlar ishini bloklaydigan to'siqlarni olib tashlashi kerak. Yetakchi uchun bu ko'pincha review navbati, sekin build va noaniq talab.

## 36.12 Vaqtni taqsimlash: kod, hujjat, suhbat, o'rganish

Taxminiy nisbat haftada shunday ko'rinadi: 40 foiz kod va review, 20 foiz hujjat va qaror, 25 foiz suhbat va juftlik ishi, 15 foiz o'rganish va o'lchash. Kod yozishni butunlay tashlab qo'ygan yetakchi ikki chorakdan keyin kodbazani bilmay qoladi va uning qarorlari xayoliy bo'lib qoladi. Kodning 100 foizini o'zi yozadigan yetakchi esa jamoani o'stirmaydi va bottleneck ga aylanadi.

Amaliy qoida: haftada kamida bitta haqiqiy PR yoz, lekin kritik yo'ldagi ishni o'zingga olma. Eng yaxshi tanlov shablon loyihaga, observability ga, yoki migratsiyaning birinchi namunasiga tegishli ish. Shunday ish ikki maqsadni bajaradi: sen kontekstni saqlaysan va jamoa nusxa oladigan namuna paydo bo'ladi. Review uchun kuniga ikki oyna ajrat va o'sha oynalarda chuqur ishlamagin, chunki review diqqat talab qiladi.

## 36.13 Amalda qo'llash

- [ ] Review izohlari uchun to'rtta prefiks kelishib ol (`blocker`, `kerak`, `fikr`, `maqtov`) va PR shablonida ularni yoz.
- [ ] Oxirgi 30 ta PR dagi izohlarni o'qib chiq, formatlash va uslubga tegishli hamma izohni Spotless yoki static analyzer qoidasiga ko'chir.
- [ ] CI ga uchta darvoza qo'y: `spotless:check`, static analyzer, va `Arch*Test` qoidalari.
- [ ] ArchUnit da kamida uch qoida yoz: controller to'g'ridan repository ga kirmasin, domen Spring ga bog'lanmasin, pul maydoni `double` bo'lmasin.
- [ ] PR hajmi va navbat vaqtini o'lchay boshla, 400 qatordan katta PR uchun bo'lish talabini kelish.
- [ ] Jamoa bilim xaritasini jadval shaklida yoz va har bir kritik tizim uchun ikkinchi odamni belgila.
- [ ] Oxirgi uch arxitektura qarorini bir sahifalik hujjat qilib yoz va har biriga namuna kod joyini havola qil.
- [ ] Shablon loyiha yarat yoki yangila: pool, timeout, graceful shutdown, metrikalar, migratsiya va test bazasi tayyor bo'lsin.

---

[&larr; 35. Incident, on-call va post-mortem](35-incident-on-call-va-post-mortem.md) · [Mundarija](README.md) · [37. Xarajat, SLO va biznes bilan muloqot &rarr;](37-xarajat-slo-va-biznes-bilan-muloqot.md)
