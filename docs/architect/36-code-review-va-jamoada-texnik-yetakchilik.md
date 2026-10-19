<!-- doc: architect | chapter: 36 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 36. Code review va jamoada texnik yetakchilik (Code Review and Technical Leadership)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

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
- [36.13 Review standarti: tasdiqlash chegarasi qayerda](#3613-review-standarti-tasdiqlash-chegarasi-qayerda)
- [36.14 "Keyin tozalaymiz" va'dasi va qat'iylikdan shikoyat](#3614-keyin-tozalaymiz-vadasi-va-qatiylikdan-shikoyat)
- [36.15 Bog'liq jamoalar xaritasi va chegaradagi takroriy ishqalanish](#3615-bogliq-jamoalar-xaritasi-va-chegaradagi-takroriy-ishqalanish)
- [36.16 Yaxshi xulqli servis standarti: nimada bir xillik majburiy](#3616-yaxshi-xulqli-servis-standarti-nimada-bir-xillik-majburiy)
- [36.17 Amalda qo'llash](#3617-amalda-qollash)

</details>



Code review arxitektorning eng arzon va eng ta'sirli vositasi. U kod birlashishdan oldin ishlaydi, shuning uchun bitta izoh keyinchalik haftalarcha ketadigan migratsiyani to'xtatishi mumkin. Lekin ko'p jamoada review bo'sh marosimga aylanadi: odamlar probel va o'zgaruvchi nomi haqida bahslashadi, tranzaksiya chegarasi va pul turini esa hech kim ko'rmaydi. Bu bob review ichida nimani qidirish kerakligini, izohni qanday yozishni va texnik yetakchi o'z vaqtini qanday taqsimlashini ko'rsatadi.

## 36.1 Code review nimani topishi kerak: xatti-harakat, chegara, nom, xavfsizlik

Google ning review qo'llanmasi review da qaraladigan narsalarni ketma-ket sanaydi va birinchisini alohida ajratadi: "The most important thing to cover in a review is the overall design of the CL." Dizayndan keyin funksionallik, murakkablik, testlar, nom, izoh, uslub, izchillik va hujjat keladi. Shu ro'yxat umumiy; Java va Spring da esa dizayndan keyingi qism amalda to'rtta savolga aylanadi. Birinchisi xatti-harakat: kod aytilgan ishni qiladimi, chegara holatlarida nima bo'ladi, xato yo'lida qanday javob qaytadi. Ikkinchisi chegara: tranzaksiya qayerda ochiladi va yopiladi, tashqi HTTP chaqiruv tranzaksiya ichida qolib ketmaganmi, cache invalidatsiyasi commit dan keyin bo'ladimi. Uchinchisi nom: metod nomi uning yon ta'sirini yashirmayaptimi, domen atamasi kodda bir xil ishlatilayaptimi. To'rtinchisi xavfsizlik: autorizatsiya tekshiruvi qayerda, log ichiga karta raqami yoki token tushmayaptimi, SQL parametrlanganmi.

Murakkablik bo'yicha manbaning ta'rifi aniq va foydali: "Too complex" usually means "can't be understood quickly by code readers", yoki "developers are likely to introduce bugs when they try to call or modify this code". Murakkablikning alohida turi over-engineering: kod kerakdan generic qilingan yoki hozir kerak bo'lmagan funksionallik qo'shilgan. Qo'llanma reviewer ni shunga ayricha hushyor bo'lishga chaqiradi va qoidani shunday beradi: dasturchi hozir hal qilinishi kerak ekani ma'lum muammoni hal qilsin, kelajakda kerak bo'lishi mumkin deb taxmin qilgan muammoni emas. Kelajakdagi muammo kelganda, haqiqiy shakli va talablari ko'ringanda hal qilinadi. Spring loyihada bu eng ko'p uchraydigan ko'rinishi bitta implementatsiyasi bor interfeys va bitta joydan chaqiriladigan strategy ro'yxati.

Parallel kod uchun manba yana bitta amaliy maslahat beradi: deadlock yoki race condition keltirib chiqarishi mumkin bo'lgan o'zgarishni ishga tushirib topib bo'lmaydi, uni muallif ham reviewer ham boshida o'ylab chiqishi kerak. Qo'llanma shu yerda teskari xulosa ham chiqaradi: bu race condition va deadlock mumkin bo'lgan concurrency modelidan umuman foydalanmaslikning yana bir sababi, chunki bunday kodni review qilish va tushunish qiyinlashadi.

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

Uslub bo'yicha qoidani Google qo'llanmasi uch bosqichda beradi va bu bosqichlar review da bahsni tugatish uchun yetadi. Birinchi: uslub masalasida style guide mutlaq hokim, style guide talab qilgan narsa bajariladi. Ikkinchi: style guide da yo'q har qanday sof uslub nuqtasi (probel va shunga o'xshash) shaxsiy xohish, uslub atrofdagi kodga mos bo'lishi kerak. Uchinchi: agar avvaldan uslub bo'lmasa, muallif uslubi qabul qilinadi. Shundan kelib chiqib, "Men bu yerda stream emas, for loop ni afzal ko'raman" degan izoh review izohi emas: qo'llanma shaxsiy uslub xohishi uchun CL ni bloklamaslikni va bunday izohga `Nit:` prefiksini qo'yishni talab qiladi.

Muhim istisno: dizayn uslub emas. Qo'llanma buni alohida ta'kidlaydi, "aspects of software design are almost never a pure style issue or just a personal preference". Dizayn qarori prinsipga tayanadi, shuning uchun "bu shunchaki ta'm masalasi" deb yopib qo'yilmaydi. Lekin agar muallif o'lchov yoki muhandislik prinsipi bilan bir necha yondashuv teng ekanini ko'rsata olsa, reviewer muallif variantini qabul qiladi.

Yana bitta qoida muallif tomoniga tegishli: katta uslub o'zgarishini funksional o'zgarish bilan birga yubormaslik kerak. Aks holda nima o'zgargani ko'rinmaydi, merge va rollback qiyinlashadi. Agar faylni qaytadan formatlash kerak bo'lsa, formatlash alohida PR da ketadi, funksional o'zgarish keyingisida.

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
| Review javob vaqti 2 kun | "Band edim" deyiladi | Chegara bitta ish kuni, javob tabiiy to'xtash nuqtasida |
| Hisobot query sekin ishlaydi | Keyin optimallashtiramiz deyiladi | PR da EXPLAIN natijasi talab qilinadi |

## 36.3 Izoh yozish uslubi: muammoni ko'rsat, qaror egasini qoldirib ket

Google qo'llanmasi izoh yozishni to'rt qatorga sig'diradi: mehribon bo'l, sababini tushuntir, aniq ko'rsatma berish bilan muammoni ko'rsatib qaror egasini muallifda qoldirish o'rtasida balans saqla, murakkablikni review da senga tushuntirish o'rniga kodni soddalashtirishga yoki kodga izoh qo'shishga undagin. Yaxshi izoh uchta qismdan iborat: nima ko'rdim, nega bu muhim, qaysi yo'nalishda o'ylash kerak. Asosiy qoida CL ni tuzatish reviewer ning emas, muallifning javobgarligi: reviewer yechimni batafsil loyihalashga yoki muallif uchun kod yozishga majbur emas. Lekin balans so'zi muhim, chunki qo'llanma "hech qachon yechim taklif qilma" demaydi: ba'zan to'g'ridan-to'g'ri ko'rsatma, taklif yoki hatto kod ko'proq yordam beradi. Muammoni ko'rsatib qarorni muallifga qoldirish esa ko'pincha o'rgatadi va yaxshiroq yechim beradi, chunki muallif kodga reviewer dan yaqin turadi. "Bu yerni ChangeStreamListener ga o'tkaz" degan izoh muallifni ijrochiga aylantiradi. "Bu listener commit dan oldin ishga tushadi, shuning uchun rollback bo'lsa cache eski emas, yangi qiymatni ushlab qoladi. Qanday hal qilsak yaxshi bo'ladi?" degan izoh muallifni o'ylashga majbur qiladi va u ko'pincha sendan yaxshiroq variant topadi.

Izohda nega ekanini ko'rsatish yagona eng muhim odat. "BigDecimal ishlat" o'rniga "to'lov summasi hisobotda tiyingacha mos kelishi kerak, suzuvchi nuqta uchta amaldan keyin farq beradi" deb yoz. Birinchi izoh bitta qatorni tuzatadi, ikkinchisi odamni o'zgartiradi va keyingi PR da shu muammo bo'lmaydi.

Savol shaklidagi izoh ikki tomonga ham xizmat qiladi. Agar sen xato qilgan bo'lsang, savol shakli sening obro'yingni saqlaydi. Agar muallif xato qilgan bo'lsa, savol unga o'zi topish imkonini beradi.

Odob qoidasining mexanik shakli bor va u juda ishlaydi: izoh kod haqida yoziladi, dasturchi haqida emas. Manbadagi misol shu farqni ko'rsatadi. Yomon: "Why did you use threads here when there's obviously no benefit to be gained from concurrency?" Yaxshi: "The concurrency model here is adding complexity to the system without any actual performance benefit that I can see." Ikkinchi shaklda bir xil texnik fikr bor, lekin unda muallifga tegadigan hech narsa qolmagan.

Oxirgi va eng ko'p o'tkazib yuboriladigan qoida: review da yozilgan tushuntirish kelajakdagi o'quvchiga yetib bormaydi. Agar sen tushunmagan kod haqida savol bersang, to'g'ri natija muallif kodni ravshanroq qayta yozishi. Ba'zan kodga izoh qo'shish ham mos javob, lekin bu izoh keragidan murakkab kodni tushuntirish uchun bo'lmasligi shart. Review oynasida qolgan tushuntirish faqat bir necha holatda yetarli: masalan sen yaxshi bilmagan sohani ko'rib chiqayotganingda, va muallif shu kodning odatdagi o'quvchisi allaqachon biladigan narsani aytayotganda.

## 36.4 Majburiy va ixtiyoriy izohlarni ajratish

PR da yigirma izoh bo'lsa, muallif qaysi biri birlashishga to'sqinlik qilayotganini bilmaydi. Google qo'llanmasida bu alohida qoida: izohning og'irligini belgilab qo'y, majburiy o'zgarishni maslahat va taklifdan ajrat. Sababi ham yozilgan: belgisiz izohlarni muallif hammasini majburiy deb o'qishi mumkin, hatto ular faqat ma'lumot uchun yoki ixtiyoriy bo'lsa ham. Manbadagi uch belgi: `Nit:` (mayda narsa, texnik jihatdan qilish kerak, lekin ta'siri katta emas), `Optional:` yoki `Consider:` (yaxshi fikr deb o'ylayman, lekin qat'iy talab emas), `FYI:` (bu CL da qilishingni kutmayman, lekin kelajak uchun o'ylab ko'rishga arziydi). Shu uchlikni to'g'ridan-to'g'ri olish ham mumkin; biz jamoada to'rtta darajani ishlatamiz, chunki bizda birlashishni bloklaydigan daraja alohida kerak. To'rtta daraja: `blocker` (bu holatda birlashtirmaymiz), `kerak` (birlashishdan oldin tuzatiladi), `fikr` (o'ylab ko'r, qaror senda), `maqtov` (yaxshi yechimni ko'rsatish). Oxirgisi bo'sh narsa emas: u review ni jazo mexanizmidan o'rgatish mexanizmiga aylantiradi.

| Prefiks | Ma'nosi | Misol |
|---|---|---|
| `blocker` | Ma'lumot yo'qoladi yoki xavfsizlik buzildi | Autorizatsiya tekshiruvi yo'q |
| `kerak` | Xatti-harakat yoki chegara noto'g'ri | Tranzaksiya ichida tashqi chaqiruv |
| `fikr` | Yaxshilash mumkin, qaror muallifda | Bu metodni ikkiga bo'lish mumkin |
| `maqtov` | Qayta ishlatilishi kerak bo'lgan yechim | Idempotency key dizayni yaxshi |

Agar PR da uchdan ko'p `blocker` bo'lsa, izoh yozishni to'xtat va 15 daqiqalik suhbat taklif qil. Ko'p blocker odatda noto'g'ri tushunilgan talab belgisi, va uni yozma izohlar bilan hal qilish bir necha kun oladi.

## 36.5 Review hajmi: katta o'zgarishni bo'lish va navbat vaqtini qisqartirish

Kichik PR tezroq va chuqurroq ko'riladi, kamroq bug keltiradi, rad etilsa kamroq ish yo'qoladi, oson merge va oson rollback bo'ladi. Hajm bo'yicha aniq chegara esa yo'q va manba buni ochiq aytadi: "There are no hard and fast rules about how large is too large. 100 lines is usually a reasonable size for a CL, and 1000 lines is usually too large, but it's up to the judgment of your reviewer." Qatorlar soni yagona o'lchov emas: o'zgarish necha faylga tarqalgani ham hajmga kiradi, bitta fayldagi 200 qatorlik o'zgarish normal bo'lishi mumkin, 50 faylga tarqalgan o'sha 200 qator esa odatda katta. To'g'ri o'lcham ta'rifi qator emas, mazmun: bitta o'zini o'zi to'ldiradigan o'zgarish, u bitta narsani hal qiladi va o'zi bilan testini olib keladi.

Ikki chekka ham xavfli. Reviewer PR ni faqat kattaligi uchun rad qilish huquqiga ega, lekin PR shunchalik kichik ham bo'lmasligi kerak, aks holda uning oqibatini tushunish qiyinlashadi: yangi API qo'shilsa, o'sha API ning ishlatilishi ham shu PR da bo'lishi kerak, aks holda reviewer uni qanday ishlatilishini ko'rmaydi va kodbazaga ishlatilmaydigan API tushadi. Ba'zi katta PR lar esa muammo emas: butun faylni o'chirish reviewer uchun bitta qatorlik ish, ishonchli avtomatik refaktoring vositasi yozgan o'zgarishda esa reviewer ning ishi natijani tasdiqlash.

Shuning uchun arxitektorning ishi review paytida boshlanmaydi, u PR tuzilishidan boshlanadi. Katta o'zgarishni uchta tabiiy qatlamga bo'lish mumkin: birinchi PR da yangi interfeys va migratsiya skripti, ikkinchisida implementatsiya, uchinchisida eski yo'lni o'chirish.

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

Navbat vaqti review ning yashirin narxi, va bu yerda manbaning qoidasi o'lchanadigan: "One business day is the maximum time it should take to respond to a code review request." Ya'ni chegara javob vaqtida, PR ning boshdan oxirgacha o'tish vaqtida emas. Qo'llanma shu farqni ataylab ta'kidlaydi: alohida javoblarning tez kelishi butun jarayonning tez tugashidan ham muhimroq, chunki dasturchining "review sekin" degan noroziligi aslida javobni kutishdan tug'iladi.

Lekin tezlik qoidasining aniq istisnosi bor va u ko'p jamoada e'tibordan chetda qoladi: diqqat talab qiladigan ish o'rtasida bo'lsang, review uchun o'zingni to'xtatmaysan. Sababi jamoa hisobida: uzilgandan keyin dasturchi ish oqimiga qaytishi uzoq vaqt oladi, shuning uchun kod yozish o'rtasida o'zini uzish jamoaga boshqa dasturchini bir oz kutishdan qimmatroq turadi. To'g'ri yo'l ishdagi tabiiy to'xtash nuqtasini kutish: joriy vazifa tugaganda, tushlikdan keyin, uchrashuvdan qaytganda. Kuniga ikki marta belgilangan review oynasi aynan shu qoidaning amaliy shakli.

Agar PR kelganda to'liq review ga vaqt bo'lmasa, bo'sh turish o'rniga qisqa javob yuborish kerak: qachon ko'raman, yoki kim tezroq ko'rishi mumkin, yoki umumiy dizayn haqida birinchi izohlar. Vaqt mintaqasi farqida esa maqsad muallif o'z ish kuni tugashidan oldin javobni olishi.

Navbatni qisqartiradigan yana bitta vosita ko'p jamoada ishlatilmaydi: izohlar bilan tasdiqlash. Qo'llanma reviewer ga hal qilinmagan izohlar qoldirib ham LGTM berishni tavsiya qiladi, agar uchta shartdan kamida bittasi bajarilsa: reviewer muallif qolgan izohlarni to'g'ri hal qilishiga ishonadi; izohlarni bajarish shart emas; takliflar mayda (import tartibi, yondagi xato yozilgan so'z, ishlatilmagan bog'liqlikni olib tashlash). Reviewer qaysi birini nazarda tutganini aytib qo'yishi kerak. Bu ayniqsa muallif bilan reviewer boshqa vaqt mintaqasida bo'lganda foydali: aks holda muallif faqat "LGTM" so'zi uchun bir kun kutadi.

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

O'lchovning ustuvorligi manbada prinsip darajasida yozilgan: "Technical facts and data overrule opinions and personal preferences." Shuning uchun birinchi harakat bahsni fikrdan o'lchovga ko'chirish.

Agar o'lchov imkonsiz bo'lsa, ikkinchi qadam vaqt chegarasi bilan prototip. Ikki tomon ham yarim kun ichida eng kichik ishlaydigan variantini yozadi va uchrashuvda ikkisini solishtiradi.

Uchinchi qadam qo'llanmada aniq ketma-ketlik bilan berilgan. Avval muallif va reviewer kelishuvga kelishga harakat qiladi. Kelishuv qiyin bo'lsa, review izohlari o'rniga yuzma-yuz yoki video uchrashuv yordam beradi, lekin natijani PR ga izoh qilib yozib qo'yish shart, aks holda kelajakdagi o'quvchi uchun qaror yo'qoladi. Bu ham yordam bermasa, eskalatsiya: kengaytirilgan jamoa muhokamasi, texnik yetakchining fikri, kod maintainer idan qaror so'rash, yoki menejerni jalb qilish. Eng muhim jumla shu yerda: "Don't let a CL sit around because the author and the reviewer can't come to an agreement." Hal qilinmagan bahs PR ni to'xtatib turishi kelishmovchilikning o'zidan qimmatroq.

Agar bahs baribir hal bo'lmasa, qaytarilishi oson variantni tanlash kerak: xato variantni bir hafta ichida qaytarish, to'g'ri variantni bir oy kutishdan arzon. Qaror qabul qilinganda uni va sababini yozib qo'y, aks holda uch oydan keyin bir xil bahs qaytadi.

## 36.7 Yangi odamga review orqali o'rgatish

Review ning o'rgatish vazifasi manbada alohida yozilgan: review tilda, framework da yoki umumiy dizayn prinsiplarida yangi narsa o'rgatishi mumkin, va bilim almashish tizim kod salomatligini uzoq muddatda yaxshilaydi. Lekin shu yerda bitta shart bor: agar izoh faqat o'rgatish uchun bo'lsa va review standartini bajarish uchun zarur bo'lmasa, unga `Nit:` prefiksi qo'yiladi yoki boshqa yo'l bilan majburiy emasligi aytiladi. Aks holda yangi odam o'rgatish izohini blocker deb o'qiydi.

Yangi odamning birinchi PR si uchun bizning jamoa amaliyotimiz: uchtadan ko'p majburiy izoh yozmaymiz, qolgan muammolarni ro'yxatga olib keyingi PR larga tarqatamiz. Bu manbadagi qoida emas, o'lchovga ham tayanmaydi: shunchaki bir vaqtda uchta narsadan ko'pini o'rganib bo'lmaydi degan taxminga asoslangan ish usuli, va jamoa boshqacha kelishishi mumkin.

Teskari yo'nalish ham manbada bor va u ko'pincha e'tibordan chetda qoladi: odamlar faqat xatodan emas, to'g'ri qilgan ishining tasdiqlanishidan ham o'rganadi. Qo'llanma buni ochiq aytadi, o'rgatish nuqtai nazaridan dasturchiga nimani to'g'ri qilganini aytish ba'zan nimani noto'g'ri qilganini aytishdan qimmatroq. Shuning uchun yaxshi yechimni ko'rsatadigan izoh ham sababini olib yurishi kerak.

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

Majburlashning MIQDORI esa alohida qaror va u ko'pincha o'ylanmaydi. Brown nazoratni ikki holatli tugma emas, richag deb ko'radi: diktatorlik va umuman yo'l-yo'riq bermaslik oralig'ida uzluksiz shkala bor, va qancha nazorat kerakligini to'rt narsa belgilaydi, ya'ni jamoa tajribasi, jamoa hamda loyihaning kattaligi, talablarning murakkabligi va kodbazaning hozirgi holati; uning tavsiyasi "bir oz nazorat bilan boshla, keyin fikr-mulohazaga qarab sozla" (Simon Brown, *Software Architecture for Developers*, Leanpub, 15-bob, 41-bet). Sozlash signallari amaliy: jamoa ko'p "nega" so'rasa yo'l-yo'riq kam berilgan, jamoa doim qarshilik qilsa ko'p berilgan. Shu richag yuqoridagi vositalarga ham tegishli, chunki ArchUnit qoidasi ham nazoratning bir shakli: barcha chegarani birinchi kundan qattiq qilib qo'yish jamoani qoidani chetlab o'tishga o'rgatadi, hech bir chegarani majburlamaslik esa qoidani yozilgan joyida qoldiradi. Tartib: qoidani avval ogohlantirish rejimida yurgizasiz, keyin takrorlangan buzilishlarni ko'rib qattiqlashtirasiz.

Mavzuning to'liq yozuvi testlash qo'llanmasidagi [arxitektura testlari va kod sifati darvozalari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bo'limida; bu yerda faqat arxitektura nuqtai nazari.

## 36.10 Jamoaning bilim xaritasi va bitta odamga bog'liqlikni kamaytirish

Har bir yetakchi o'z jamoasining bilim xaritasini yozib qo'yishi kerak: qaysi tizimni kim chuqur biladi, kim o'rtacha biladi, kim umuman bilmaydi. Xarita tayyor bo'lgach, eng xavfli hujayralar ko'rinadi: muhim tizim, uni faqat bitta odam biladi. Bu odam ta'tilga chiqsa yoki ishdan ketsa, jamoa to'xtaydi.

Kamaytirish usullari amaliy. Review ni shu sohada ikkinchi odamga berish, lekin birinchi odamni ham qo'shish. Incident dan keyin tahlilni boshqa odam yozishi. To'lov yoki ombor qoldig'i kabi kritik tizimda har chorakda bitta o'rtacha hajmli ishni "bilmaydigan" odamga berish va birinchi odamni maslahatchi qilish. Maqsad: har bir kritik tizimda kamida ikkita odam ishonchli o'zgartirish kirita olishi.

## 36.11 Texnik yetakchi va menejer roli farqi

Ikki rol aralashganda ikkisi ham buziladi. Menejer odamlar uchun javob beradi: o'sish, ish taqsimi, baho, konfliktlar. Texnik yetakchi tizim uchun javob beradi: arxitektura, sifat darvozalari, texnik qarzni boshqarish, qaror sifati. Yetakchining vakolati lavozimdan emas, ishonchdan keladi, va ishonch kod yozish bilan saqlanadi.

Eng muhim farq ta'sir usulida. Menejer qaror qabul qilib buyruq berishi mumkin. Yetakchi esa odamlarni ishontirishi kerak, chunki uning qo'lida majburlash vositasi yo'q. Shuning uchun yetakchining asosiy quroli dalil, prototip va yozma hujjat. Agar yetakchi "men shunday dedim" ga tayansa, u menejer rolini noto'g'ri o'zlashtirgan bo'ladi.

Bir xil narsada ikki rol birlashadi: ikkisi ham odamlar ishini bloklaydigan to'siqlarni olib tashlashi kerak. Yetakchi uchun bu ko'pincha review navbati, sekin build va noaniq talab.

Yetakchilik uslubining o'zi esa doimiy emas va u jamoaning yetukligiga qarab o'zgaradi. Brown bu yerda Roy Osherove ning *Elastic Leadership* modeliga ishora qiladi: omon qolish modelida, ya'ni jamoa tartibsizlik ichida bo'lganda, to'g'ridan-to'g'ri buyruq uslubi kerak bo'ladi, yetuklik oshgani sari esa uslub o'zgaradi; "o'zini tashkil qiluvchi jamoa" ga intilish yaxshi, lekin ko'p jamoa uchun bu yurishdan oldin yugurishga urinish bo'ladi (Simon Brown, *Software Architecture for Developers*, Leanpub, 18-bob, 47-48-betlar). Amaliy oqibati yuqoridagi "majburlash vositasi yo'q" qoidasini cheklaydi: tartibsizlik holatidagi jamoada ishontirish uchun vaqt yo'q va qaror aytiladi, keyin sababi yoziladi. Tartibsizlik belgilari ham kuzatiladigan: hamma qaror bir odamdan kutiladi, PR lar bir haftadan ko'p turadi, hech qanday standart bajarilmaydi. Shu holatdan chiqqandan keyin uslub [nazorat richagi](#369-standart-ornatish-linter-formatlash-archunit-qoidalari-shablon-loyiha) bo'yicha pasaytiriladi, aks holda buyruq uslubi o'z o'rnidan oshib ketadi va [huquqni qozonish](39-birinchi-90-kun-va-oz-ozini-baholash.md#393-ikkinchi-oy-kichik-korinadigan-yaxshilanish-bilan-ishonch-qozonish) mantiqini buzadi.

## 36.12 Vaqtni taqsimlash: kod, hujjat, suhbat, o'rganish

Vaqt taqsimotining to'g'ri nisbati bo'yicha o'lchov yo'q va bu yerda raqam yozish ham noto'g'ri bo'ladi: nisbat jamoa hajmiga, mahsulot bosqichiga va yetakchining boshqa majburiyatlariga qarab o'zgaradi. Aniq bo'lgani ikki chekkaning oqibati. Kod yozishni butunlay tashlab qo'ygan yetakchi ikki chorakdan keyin kodbazani bilmay qoladi va uning qarorlari xayoliy bo'lib qoladi. Kodning 100 foizini o'zi yozadigan yetakchi esa jamoani o'stirmaydi va bottleneck ga aylanadi.

Amaliy qoida: haftada kamida bitta haqiqiy PR yoz, lekin kritik yo'ldagi ishni o'zingga olma. Eng yaxshi tanlov shablon loyihaga, observability ga, yoki migratsiyaning birinchi namunasiga tegishli ish. Shunday ish ikki maqsadni bajaradi: sen kontekstni saqlaysan va jamoa nusxa oladigan namuna paydo bo'ladi. Review uchun kuniga ikki oyna ajrat va o'sha oynalarda chuqur ishlamagin, chunki review diqqat talab qiladi.

## 36.13 Review standarti: tasdiqlash chegarasi qayerda

Review da eng ko'p yo'qoladigan narsa chegara: reviewer qachon "ha" deydi.
Google qo'llanmasi buni o'zining eng katta prinsipi deb ataydi va bitta
jumlada beradi: reviewer CL ni tizimning umumiy kod salomatligini aniq
yaxshilaydigan holatga kelgandan keyin tasdiqlashni afzal ko'rishi kerak,
hatto CL mukammal bo'lmasa ham.

Prinsip ikki tomonli muvozanatdan chiqadi. Bir tomondan dasturchi o'z ishida
oldinga siljishi kerak: agar kodbazaga yaxshilanish hech qachon tushmasa,
kodbaza yaxshilanmaydi. Qo'llanma ikkinchi ta'sirni ham aytadi, agar reviewer
har qanday o'zgarishni kiritishni juda qiyinlashtirsa, dasturchilarda
kelajakda yaxshilash kiritish istagi qolmaydi. Boshqa tomondan reviewer
har bir CL ning sifati tizim kod salomatligini vaqt o'tishi bilan
pasaytirmasligini kafolatlashi kerak, chunki kodbaza aynan kichik
pasayishlar yig'indisidan buziladi, ayniqsa jamoa vaqt tanqisligida
yo'lni qisqartirish kerak deb hisoblaganda.

Shu yerdan amaliy xulosa chiqadi: "mukammal kod" degan narsa yo'q, faqat
"yaxshiroq kod" bor. Reviewer muallifdan CL ning har bir mayda qismini
yaltiratishni talab qilmasligi kerak; maqsad mukammallik emas, uzluksiz
yaxshilanish. Ta'minlanishi, o'qilishi va tushunilishi yaxshilangan CL
mukammal emasligi uchun kunlab yoki haftalab turmasligi kerak.

Prinsipning chegarasi ham bor va u ikki tomonlama. Birinchi: agar CL
reviewer o'z tizimida ko'rishni istamagan funksionallikni qo'shsa, reviewer
kod yaxshi loyihalangan bo'lsa ham tasdiqlamasligi mumkin. Ikkinchi va
muhimrog'i: bu prinsip tizim kod salomatligini aniq pasaytiradigan CL ni
kiritishni oqlamaydi.

Java loyihada chegara shunday ko'rinadi. To'rt servisdan bittasida pulni
`double` dan `BigDecimal` ga o'tkazgan PR keldi, qolgan uchtasi eski
holatda. Bu PR tizimni aniq yaxshilaydi, demak u birlashadi va qolgan
uchtasi uchun alohida ish ochiladi. Teskari misol: PR bitta joyni
tuzatib, yo'l-yo'lakay tranzaksiya chegarasini tashqi HTTP chaqiruvini
o'rab oladigan qilib kengaytirgan. Bu PR bir narsani yaxshilab ikkinchisini
buzadi, shuning uchun u tasdiqlanmaydi.

## 36.14 "Keyin tozalaymiz" va'dasi va qat'iylikdan shikoyat

Review da eng ko'p uchraydigan qarshilik texnik emas: "keling buni
birlashtiramiz, tozalashni keyingi PR da qilaman". Google qo'llanmasining
javobi tajribaga tayanadi: muallif asl CL ni yozgandan keyin qancha vaqt
o'tsa, tozalash ehtimoli shuncha kamayadi, va amalda muallif tozalashni
darhol qilmasa, u hech qachon bo'lmaydi. Buning sababi dasturchining
mas'uliyatsizligi emas: uning ishi ko'p va tozalash boshqa ishlar
oqimida yo'qoladi. Shuning uchun to'g'ri yo'l muallifdan tozalashni
hozir, kod kodbazaga tushib "tugallangan" holatga o'tishidan oldin
talab qilish. Qo'llanma buni ochiq ogohlantirish bilan yakunlaydi:
odamlarga "keyin tozalaymiz" deyishga ruxsat berish kodbazaning
buzilishining eng ko'p uchraydigan yo'li.

Lekin qoida ikkiga bo'linadi va bu farq amalda hal qiluvchi. Agar CL
yangi murakkablik keltirsa, u birlashishdan oldin tozalanadi (favqulodda
holat bundan mustasno). Agar CL atrofdagi mavjud muammoni ochib bergan
bo'lsa va uni hozir hal qilish imkoni bo'lmasa, muallif tozalash uchun
ish ochadi va uni o'ziga tayinlaydi, shunda u yo'qolmaydi; ixtiyoriy
ravishda kodda shu ishga havola qiladigan `TODO` izohi ham qoldiriladi.

| Holat | Kim keltirdi | Qaror |
|---|---|---|
| PR to'lov turlari `switch` iga beshinchi shox qo'shdi | PR ning o'zi | Hozir tozalanadi: polimorfizm yoki strategy |
| PR qo'shgan metod uchta mas'uliyatni oldi | PR ning o'zi | Hozir bo'linadi |
| PR ning query si indeks yo'qligini ko'rsatdi | Mavjud muammo | Ish ochiladi va muallifga tayinlanadi |
| PR tekkan klass avvaldan 900 qator edi | Mavjud muammo | Ish ochiladi, `TODO` havola qiladi |

Qat'iylikdan shikoyat alohida mavzu va uning javobi kutilganidan boshqa.
Agar jamoa avval yumshoq review dan qat'iy review ga o'tsa, ba'zi
dasturchilar baland ovozda shikoyat qiladi. Qo'llanmaning kuzatishi
shunday: shikoyatlarning aksariyati review tezligini yaxshilash bilan
yo'qoladi. Ya'ni "reviewer juda qattiq" degan shikoyat ko'pincha
"reviewer har uch kunda bir javob beradi va har safar katta o'zgarish
so'raydi" degan ma'noni yashiradi. Bir xil katta o'zgarishni so'ragan,
lekin har safar tez javob bergan reviewer dan shikoyat kelmaydi.

## 36.15 Bog'liq jamoalar xaritasi va chegaradagi takroriy ishqalanish

[36.10](#3610-jamoaning-bilim-xaritasi-va-bitta-odamga-bogliqlikni-kamaytirish) dagi xarita jamoa ichiga qaraydi: kim nimani biladi. Undan tashqarida ikkinchi xarita kerak, va u arxitektorga tegishli: jamoang qaysi jamoalarga bog'liq va qaysilari senga bog'liq. Kichik tashkilotda bu xarita boshda turadi, lekin Orosz ning kuzatuvi aniq: o'n ikkitadan ko'p muhandislik jamoasi bo'lgan joyda o'z jamoang kim bilan bog'liqligini aniqlash qiyinlashadi va bilim yo'qoladi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 12-bob, 177-bet).

Orosz xaritaga besh ro'yxat kiritadi, va ulardan ikkitasi texnik, qolgani mahsulot tomonidan keladi:

- sening jamoang bog'liq bo'lgan jamoalar: API yoki servisini ishlatadiganlaring;
- sening tizimingga bog'liq jamoalar. Ularni topishning amaliy yo'li oddiy: o'z jamoangga ta'sir qilgan incidentlarni ko'rib chiq va o'zgarish qaysi jamoadan kelganini qara, bog'liq jamoa ko'pincha o'sha yerdan chiqadi;
- funksiyasi ustma-ust tushish ehtimoli bor jamoalar;
- agar jamoang interfeys egasi bo'lsa, bir ekranda sening funksiyang bilan birga ko'rinadigan jamoalar;
- bilvosita bo'lsa ham ishlatadigan infratuzilma jamoalari.

Xarita tayyor bo'lgach, uni hamkasblar va menejerga ko'rsatish kerak: bo'shliq aynan shu yerda ko'rinadi (12-bob, 177-bet). Kim bilan gaplashish kerakligini topishning eng arzon usuli ham shu bobda: tegishli kod satrini oxirgi marta kim o'zgartirganini qarash va o'shanga murojaat qilish.

Xarita bog'liqlikni ko'rsatadi, lekin blokdan chiqarmaydi. Orosz bog'liqlikni kritik yo'ldan chiqarishning uch taktikasini sanaydi: bog'liqlikni mock qilib o'zingizni blokdan chiqarish va shartnoma kelgach ulanish; tashkilotda ichki open source modeli bo'lsa, kerakli ishni o'zingiz qilib berish va o'sha jamoaning review idan o'tkazish; yoki o'zingizning soddaroq variantingizni qurish (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 16-bob, 235-bet). Uchtasining narxi bir xil emas va oxirgisi eng qimmat: o'z variantingizni qurgan paytdan boshlab uni saqlash majburiyati sizga o'tadi, ya'ni CVE, migratsiya va chegaraviy holatlar ham sizning navbatingizga tushadi.

Shu sababli uchinchi taktikaga chegara kerak, va u [bog'liqliklarni kamaytirish](../sonarqube/39-bogliqlik-zaifliklari-va-litsenziya.md#3911-bogliqliklarni-kamaytirish-eng-yaxshi-himoya) bilan bir xil shaklda: kichik va tushunarli qismni o'zingiz yozasiz, murakkab yoki xavfsizlikka tegishli qismni esa kutmasdan ham boshqaga topshirasiz. Birinchi ikki taktika uchun qaror arzon: mock qilish faqat shartnoma yozma bo'lsa ishlaydi (aks holda integratsiya kuni boshqa API chiqadi), ichki open source esa review navbati va kod egalari belgilangan joyda ishlaydi.

Xaritaning arxitektura qiymati review chegarasida ochiladi. Orosz tajribali reviewer ning xulqini shunday ta'riflaydi: vaqt zonasi farqidan kelgan ishqalanishni bir necha marta uchratsa, u yechimni review jadvalida emas, review doirasidan tashqarida qidiradi, va bunday yechim ko'pincha oddiy emas: refaktoring, yangi servis yoki interfeys yaratish, instrument yaxshilash. Bog'liqlikni shu yo'l bilan hal qilish ikkala jamoaning ham ishini yengillashtiradi (12-bob, 168-bet).

| Takrorlanuvchi belgi | Noto'g'ri o'qish | Arxitektura o'qishi |
|---|---|---|
| Bir xil tashqi jamoa PR larni har hafta to'xtatib turadi | Review tezligi muammosi | Egalik chegarasi noto'g'ri joyda |
| Har o'zgarish ikki repoda bir vaqtda ketadi | Rejalashtirish muammosi | Interfeys o'rniga umumiy ichki tuzilma ishlatilgan |
| Javob kelishi doim ertangi kunga qoladi | Vaqt zonasi muammosi | Yo'lda keraksiz sinxron bog'liqlik bor |
| Ikki jamoa bir xil funksiyani yozyapti | Aloqa muammosi | Xaritadagi ustma-ust tushish ko'rilmagan |

Xulosa bitta qoidaga yig'iladi: review da takrorlanuvchi ishqalanish odam yoki jadval muammosi emas, chegara muammosining belgisi. Chegara to'g'ri qo'yilganda o'sha ishqalanish o'zidan yo'qoladi, va bu arxitektorning ishi, reviewer niki emas.

## 36.16 Yaxshi xulqli servis standarti: nimada bir xillik majburiy

[Standart o'rnatish](#369-standart-ornatish-linter-formatlash-archunit-qoidalari-shablon-loyiha) bo'limi standartni qanday majburlashni ko'rsatdi. Undan oldin keladigan savol esa boshqa: standart nimani qamrab olishi kerak. Newman buni amaliyotlar bo'yicha ishlaganda topilishi kerak bo'lgan eng muhim muvozanat deb ataydi, ya'ni tizimda qancha o'zgaruvchanlikka ruxsat berish, va javobni topishning kaliti sifatida bitta savolni qo'yadi: yaxshi xulqli, "yaxshi fuqaro" (good citizen) servis sizning tizimingizda qanday ko'rinadi? Qaysi imkoniyatlar unda bo'lishi kerak, shunda tizim boshqariladigan bo'lib qoladi va bitta yomon servis butun tizimni yiqitmaydi (Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 16-bob, "The Required Standard" bo'limi).

Newman javobning kontekstga bog'liq ekanini oldindan tan oladi: odamlarda bo'lgani kabi, bir muhitdagi "yaxshi fuqaro" boshqa joydagiga o'xshamaydi. Shunga qaramay u uchta sohani ajratadi, chunki aynan ularda juda ko'p chetga chiqish yomon natija beradi. Maqsadni esa Ben Christensen ning gapi bilan qo'yadi: bu avtonom hayot tsiklidagi ko'p kichik qismdan tashkil topgan, lekin birga keladigan yaxlit tizim bo'lishi kerak (16-bob, "The Required Standard").

| Soha | Nima majburiy bo'ladi | Nima erkin qoladi |
| --- | --- | --- |
| Monitoring | sog'liq va monitoring metrikalarini hamma servis bir xil usulda chiqarishi; log bitta joyda yig'ilishi | servis ichidagi texnologiya; monitoring tizimi quti ichini bilishi shart emas |
| Interfeys | aniqlangan integratsiya texnologiyalari soni kichik bo'lishi; HTTP/REST tanlangan bo'lsa resurs nomlanishi, sahifalash va endpoint versiyalash qoidalari | ichki implementatsiya, saqlash va kutubxona tanlovi |
| Arxitektura xavfsizligi | pastdagi sog'lom bo'lmagan chaqiruvdan o'zini himoyalash; javob kodlarini to'g'ri ishlatish | himoya mexanizmining aniq kutubxonasi |

Birinchi soha haqida Newman ning talabi aniq: tizim sog'lig'ining izchil, servislar bo'ylab kesib o'tuvchi ko'rinishi bo'lishi kerak, va bu tizim darajasidagi ko'rinish, bitta servisga xos ko'rinish emas; yakka servisning sog'lig'ini bilish ko'pincha faqat kengroq muammoni tashxis qilganda yoki umumiy tendensiyani tushunganda qiymat beradi (16-bob, "Monitoring"). Mexanizm push yoki pull bo'lishi mumkin, muhimi standartlashtirilgan bo'lishi; quti ichidagi texnologiya esa shaffof bo'lmasin, ya'ni uni qo'llab-quvvatlash uchun monitoring tizimini o'zgartirish talab qilinmasin. Korpusda majburiy metrikalar ro'yxati [qaysi metrikalar majburiy](30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md#307-qaysi-metrikalar-majburiy-sorov-soni-xato-ulushi-kechikish-taqsimoti-resurs) bo'limida.

Ikkinchi soha ko'pincha yetarlicha chuqur olinmaydi. Newman ning o'lchovi sodda: bitta standart yaxshi, ikkitasi ham yomon emas, yigirma xil integratsiya uslubi yomon. Lekin gap faqat texnologiya va protokolni tanlashda emas: HTTP/REST tanlansa, fe'l yoki ot ishlatilishi, resurslarning sahifalanishi va endpoint larning versiyalanishi ham shu standartga kiradi (16-bob, "Interfaces").

Uchinchi soha eng ko'p ko'z yumiladigani, chunki uning buzilishi faqat nosozlik paytida ko'rinadi. Newman qoidani shunday qo'yadi: bitta yomon xulqli servis hammaning bayramini buzishiga yo'l qo'yib bo'lmaydi, shuning uchun servislar pastdagi sog'lom bo'lmagan chaqiruvlardan o'zini himoyalashi kerak, va bu [zanjirni uzgich](../patterns/17-resilience-va-cloud-dizayn-patternlari.md#172-zanjirni-uzgich-circuit-breaker) kabi amaliyotlarni servislararo aloqa uchun majburiy qilish degani bo'lishi mumkin (16-bob, "Architectural Safety"). Ikkinchi qism esa javob kodlariga tegishli va u e'tibordan eng tez chiqadigan qoida: zanjirni uzgich HTTP kodlariga tayansa va bitta servis xato uchun 2XX qaytarsa yoki 4XX bilan 5XX ni aralashtirsa, himoya mexanizmlari ishdan chiqadi. HTTP ishlatilmasa ham talab o'zgarmaydi: so'rov to'g'ri bajarilgani, so'rov yomon bo'lgani uchun servis hech narsa qilmagani, va so'rov to'g'ri bo'lishi mumkin, lekin server o'chiq bo'lgani uchun aniq bo'lmagani bir-biridan ajralib turishi kerak, chunki tez yiqilish va muammoni topish shunga tayanadi (16-bob, "Architectural Safety").

Standartni yozma ro'yxat sifatida qoldirish kam ta'sir beradi. Amaliy shakl shu uchta sohani kompaniya starter iga joylashtirish: yangi servis uni bog'laganda talab qilingan xulqni avtomatik oladi.

```java
// Kompaniya starter i: "yaxshi fuqaro" talablari yangi servisda o'zi paydo bo'ladi.
// Servis faqat starter ni bog'laydi, monitoring va xato formatini o'zi yozmaydi.
@AutoConfiguration
public class GoodCitizenAutoConfiguration {

    // Monitoring: hamma servis bir xil teglar bilan chiqadi, nom qo'lda yozilmaydi.
    @Bean
    MeterRegistryCustomizer<MeterRegistry> commonTags(
            @Value("${spring.application.name}") String application,
            @Value("${app.team:unknown}") String team) {
        return registry -> registry.config().commonTags("application", application, "team", team);
    }

    // Interfeys: xato javobi yagona formatda (RFC 9457 ProblemDetail), har servis
    // o'z formatini o'ylab topmaydi.
    @Bean
    @ConditionalOnMissingBean(ApiErrorHandler.class)
    ApiErrorHandler apiErrorHandler() {
        return new ApiErrorHandler();
    }

    // Arxitektura xavfsizligi: tashqi chaqiruvlar timeout va uzgich bilan ketadi.
    @Bean
    RestClientCustomizer resilientDefaults(CircuitBreakerRegistry breakers) {
        return builder -> builder
                .requestFactory(timeoutAwareFactory())
                .requestInterceptor(new CircuitBreakerInterceptor(breakers.circuitBreaker("downstream")));
    }

    private static ClientHttpRequestFactory timeoutAwareFactory() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(Duration.ofSeconds(2));   // qiymat o'z o'lchovingizdan
        factory.setReadTimeout(Duration.ofSeconds(3));
        return factory;
    }
}
```

Standartning doirasiga texnologiya tanlovi ham kiradi va bu yerda erkinlik narxi aniq o'lchanadi. Newman jamoalarga o'z zonasi ichida boshqa texnologiya steki yoki ma'lumot omborini tanlash erkinligini berishni printsipial to'g'ri deb hisoblaydi, lekin ikki cheklovni darhol qo'shadi. Birinchisi odamlar: qo'llab-quvvatlanishi kerak bo'lgan 10 xil texnologiya steki bo'lsa, yollash ham, jamoalar orasida odam o'tkazish ham qiyinlashadi. Ikkinchisi tajriba: har jamoa butunlay boshqa ma'lumot omborini tanlasa, ularning birortasini katta masshtabda yuritish uchun yetarli tajriba yig'ilmaydi. Netflix misoli shu kelishuvni ko'rsatadi: kompaniya asosan Cassandra ga standartlashgan, va bu uning hamma holat uchun eng yaxshi tanlov bo'lgani uchun emas; Netflix Cassandra atrofida asbob va tajriba yig'ishdan keladigan qiymatni muayyan vazifalar uchun ko'proq mos bo'lishi mumkin bitta nechta platformani katta masshtabda qo'llab-quvvatlash va yuritishdan ustun deb hisoblaydi (16-bob, "Defining System Boundaries").

Shu yerda bir nozik farqni saqlash kerak. Yuqoridagi standart "servis chegarasidan tashqarida nima bo'lishi" haqida, texnologiya erkinligi esa chegara ichida. Newman ning o'z yo'riqnomasi shunday: qutilar orasida nima bo'layotganidan tashvishlanish, qutilar ichida esa erkin bo'lish. Interfeys darajasida bu qattiq qoida bo'ladi, chunki bitta servis REST, ikkinchisi gRPC, uchinchisi Java RMI ni tanlasa, integratsiya koshmarga aylanadi va iste'molchi bir necha almashinuv uslubini tushunishga va qo'llab-quvvatlashga majbur bo'ladi. Ya'ni standartning chegarasi texnologiyaning o'zida emas, uning ko'rinish darajasida: tashqariga chiqadigan narsa standart, ichkarida qolgan narsa jamoa qarori, bundan faqat yuqoridagi yollash va masshtab argumenti istisno qiladi.

ESLATMA: yuqoridagi starter, uning bean lari va timeout qiymatlari shu korpusning misoli. Newman uchta sohani va ularning talablarini sanaydi, aniq Spring konfiguratsiyasini bermaydi; timeout qiymatlari esa [timeout byudjeti](32-tarmoq-timeout-va-integratsiya-haqiqati.md#324-timeout-byudjeti-zanjirdagi-har-bir-chaqiruvga-vaqt-taqsimlash) bo'yicha o'z o'lchovingizdan chiqadi. Standartning ko'rinish darajasi bo'yicha chegarasini shunday ifodalash ham shu korpusning xulosasi.

## 36.17 Amalda qo'llash

- [ ] Review izohlari uchun to'rtta prefiks kelishib ol (`blocker`, `kerak`, `fikr`, `maqtov`) va PR shablonida ularni yoz.
- [ ] Oxirgi 30 ta PR dagi izohlarni o'qib chiq, formatlash va uslubga tegishli hamma izohni Spotless yoki static analyzer qoidasiga ko'chir.
- [ ] CI ga uchta darvoza qo'y: `spotless:check`, static analyzer, va `Arch*Test` qoidalari.
- [ ] ArchUnit da kamida uch qoida yoz: controller to'g'ridan repository ga kirmasin, domen Spring ga bog'lanmasin, pul maydoni `double` bo'lmasin.
- [ ] PR hajmi va navbat vaqtini o'lchay boshla: javob chegarasi bitta ish kuni, hajm chegarasi esa qator soni emas, bitta o'zini o'zi to'ldiradigan o'zgarish.
- [ ] Izoh og'irligi belgilarini PR shablonida yoz va o'rgatish uchun yozilgan izohga majburiy emasligini ko'rsatadigan belgi qo'y.
- [ ] "Keyin tozalaymiz" uchun qoida kelish: PR keltirgan murakkablik hozir tozalanadi, PR ochib bergan mavjud muammo uchun ish ochiladi va muallifga tayinlanadi.
- [ ] Jamoa bilim xaritasini jadval shaklida yoz va har bir kritik tizim uchun ikkinchi odamni belgila.
- [ ] Oxirgi uch arxitektura qarorini bir sahifalik hujjat qilib yoz va har biriga namuna kod joyini havola qil.
- [ ] Shablon loyiha yarat yoki yangila: pool, timeout, graceful shutdown, metrikalar, migratsiya va test bazasi tayyor bo'lsin.

## Manbalar

- Google, *Engineering Practices: The Standard of Code Review*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/standard.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/standard.md), commit `3bb3ec2`,
  CC BY 3.0) - 36.2, 36.6, 36.7, 36.13 dagi tasdiqlash chegarasi, uslub
  hokimiyati, dalil ustunligi va eskalatsiya yo'li.
- Google, *Engineering Practices: What to Look For in a Code Review*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/looking-for.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/looking-for.md), commit
  `3bb3ec2`, CC BY 3.0) - 36.1 dagi dizayn ustuvorligi, murakkablik
  ta'rifi, over-engineering va parallel kod.
- Google, *Engineering Practices: Speed of Code Reviews*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/speed.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/speed.md), commit `3bb3ec2`,
  CC BY 3.0) - 36.5 dagi bitta ish kuni chegarasi, uzilish qoidasi va
  izohlar bilan tasdiqlash.
- Google, *Engineering Practices: How to Write Code Review Comments*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/comments.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/comments.md), commit `3bb3ec2`,
  CC BY 3.0) - 36.3 dagi balans, kod haqida gapirish va 36.4 dagi izoh
  og'irligi belgilari.
- Google, *Engineering Practices: Handling Pushback in Code Reviews*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/pushback.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/pushback.md), commit `3bb3ec2`,
  CC BY 3.0) - 36.14 dagi "keyin tozalaymiz" qoidasi va qat'iylikdan
  shikoyat.
- Google, *Engineering Practices: Small CLs*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/developer/small-cls.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/developer/small-cls.md), commit
  `3bb3ec2`, CC BY 3.0) - 36.5 dagi hajm chegaralari, fayl soni ta'siri va
  katta PR qabul qilinadigan holatlar.
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr,
  Pragmatic Engineer, 2023, 12-bob, "Collaboration and Teamwork"
  (168 va 177-betlar) - 36.15 dagi bog'liq jamoalar xaritasining besh
  ro'yxati, oxirgi o'zgartirgan odamni topish usuli va takrorlanuvchi
  review ishqalanishini review dan tashqarida hal qilish.
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr,
  O'Reilly, 2021, 16-bob ("The Required Standard", "Monitoring", "Interfaces",
  "Architectural Safety" bo'limlari) - 36.16 dagi standart qamrovi: tizimda qancha
  o'zgaruvchanlikka ruxsat berish muvozanati, "yaxshi fuqaro" servis savoli, Ben
  Christensen ning avtonom hayot tsiklidagi qismlardan yaxlit tizim haqidagi gapi;
  monitoring uchun tizim darajasidagi izchil ko'rinish, bir xil chiqarish usuli,
  log ning bitta joyda yig'ilishi va quti ichidagi texnologiyaning shaffof emasligi;
  interfeys uchun texnologiya sonining kichikligi hamda fe'l yoki ot, sahifalash va
  versiyalash qoidalari; arxitektura xavfsizligi uchun pastdagi chaqiruvdan himoya,
  zanjirni uzgichni majburiy qilish imkoniyati va javob kodlarini to'g'ri ishlatish
  (xato uchun 2XX, 4XX bilan 5XX ni aralashtirish himoyani ishdan chiqarishi).
  Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning
  uchun faqat bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr,
  O'Reilly, 2021, 16-bob ("Defining System Boundaries" bo'limi) - jamoaga zonasi
  ichida texnologiya steki va ma'lumot ombori tanlash erkinligi, lekin 10 xil stek
  yollashni va jamoalar orasida odam o'tkazishni qiyinlashtirishi hamda har jamoa
  boshqa ma'lumot omborini tanlasa birortasini katta masshtabda yuritish tajribasi
  yig'ilmasligi; Netflix ning asosan Cassandra ga standartlashishi va asbob hamda
  tajriba yig'ish qiymatini ko'p platformani yuritishdan ustun qo'yishi;
  "qutilar orasida nima bo'layotganidan tashvishlanish, ichida erkin bo'lish"
  yo'riqnomasi va interfeysda REST, gRPC hamda Java RMI aralashuvining narxi.
  Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning
  uchun faqat bob va bo'lim nomi ko'rsatilgan
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 16-bob (235-bet) - boshqa jamoaga bog'liqlikni kritik yo'ldan chiqarishning uch taktikasi: bog'liqlikni mock qilish, ichki open source modelida ishni o'zingiz qilib berish, yoki o'zingizning soddaroq variantingizni qurish (oxirgisida saqlash majburiyati sizga o'tadi)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 15-bob (41-bet) - nazoratning tugma emas richag bo'lishi, diktatorlik va yo'l-yo'riq bermaslik oralig'idagi uzluksiz shkala, nazorat miqdorini belgilovchi to'rt omil (jamoa tajribasi, jamoa va loyiha kattaligi, talab murakkabligi, kodbaza holati) va "bir oz nazorat bilan boshlab keyin sozlash" tavsiyasi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 18-bob (47-48-betlar) - yetakchilik uslubini jamoa yetukligiga qarab o'zgartirish (Roy Osherove, *Elastic Leadership*): omon qolish modelida to'g'ridan-to'g'ri buyruq uslubi, yetuklik oshgani sari uslubning o'zgarishi, "o'zini tashkil qiluvchi jamoa" ga intilish ko'p jamoa uchun yurishdan oldin yugurishga urinish bo'lishi

---

[&larr; 35. Incident, on-call va post-mortem](35-incident-on-call-va-post-mortem.md) · [Mundarija](README.md) · [37. Xarajat, SLO va biznes bilan muloqot &rarr;](37-xarajat-slo-va-biznes-bilan-muloqot.md)
