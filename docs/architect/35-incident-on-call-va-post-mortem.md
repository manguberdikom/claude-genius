<!-- doc: architect | chapter: 35 | part: VI. Amaliyot va o'sish -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 35. Incident, on-call va post-mortem (Incidents and Post-mortems)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

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
- [35.14 Alert aniqligi (precision) va qamrovi (recall) ni o'lchash](#3514-alert-aniqligi-precision-va-qamrovi-recall-ni-olchash)
- [35.15 On-call zanjiri va navbat o'lchami: birlamchi, ikkilamchi, eskalatsiya](#3515-on-call-zanjiri-va-navbat-olchami-birlamchi-ikkilamchi-eskalatsiya)
- [35.16 Pre-mortem: nosozlik ro'y berishidan oldin sabablarni sanash](#3516-pre-mortem-nosozlik-roy-berishidan-oldin-sabablarni-sanash)
- [35.17 Amalda qo'llash](#3517-amalda-qollash)

</details>


Incident vaqtida arxitektorning qiymati kod yozishda emas, qarorni tez va to'g'ri chiqarishda ko'rinadi. Nygard o'z qoidasini bitta gapda beradi: har qanday incidentda birinchi ustuvorlik xizmatni tiklash, tiklash tekshiruvdan oldin turadi (Nygard, *Release It!*, 2-bob, 24-bet). Bu bob darajalash, rollar, tiklash usullari, diagnostika tartibi va ayblamaydigan post-mortem mexanikasini beradi. Oxirida post-mortem shabloni bor.

## 35.1 Incident darajalari va ularni belgilash mezoni

Daraja texnik emas, biznes ta'siriga qarab belgilanadi. Kleppmann farqni aniq qo'yadi: nosozlik (fault) tizimning bitta komponenti o'z spetsifikatsiyasidan chetga chiqishi, uzilish (failure) esa tizimning butunlay foydalanuvchiga kerakli xizmatni berishni to'xtatishi. Nosozlik ehtimolini nolga tushirish imkonsiz, shuning uchun nosozlikni uzilishga aylanishdan to'sadigan mexanizm quriladi (Kleppmann, *Designing Data-Intensive Applications*, 1-bob, 7-bet). "PostgreSQL replica ortda qoldi" nosozlik, "mijoz to'lovni yakunlay olmaydi" uzilish. Daraja ikkinchisiga qo'yiladi.

Daraja va javob vaqti shartnomadan kelib chiqadi, hisdan emas. Nygard tasvirlagan aviakompaniya incidentida kiosklar monitoring panelida qizil bo'lgan daqiqada operatsiya markazi Severity 1 ishini ochadi va mahalliy jamoani konferens-aloqaga chaqiradi; o'sha incidentda hal qilish uchun bir soatlik SLA chegarasi bor edi va aynan shu chegara yaqinlashgani uchun jamoa serverlarni qayta ishga tushirishga qaror qildi (Nygard, 2-bob, 24-25-bet). Nygard SLA ni xizmat ko'rsatuvchi va mijoz orasidagi shartnoma, buzilishi uchun odatda sezilarli moliyaviy jarima bilan deb ta'riflaydi (2-bob, 25-bet).

Pog'ona nomlari uchun tayanch bor: Nygard monitoringdagi g'ayritabiiy hodisalar odatda "low-medium-high" yoki "warn-severe-critical" sifatida toifalanishini yozadi (17-bob, 270-bet). Qancha pog'ona olinishi va har biriga qanday javob vaqti qo'yilishi jamoa qarori; muhimi mezon oldindan yozilgan bo'lishi, aks holda har kim o'z hissi bilan baholaydi. Darajalash SLO va xato byudjeti bilan bog'lanadi: byudjet qoldig'i reliz qarorini belgilashi 37.6 da ko'rsatilgan.

## 35.2 Incident paytidagi rollar: boshqaruvchi, tekshiruvchi, aloqachi

Eng ko'p uchraydigan xato koordinatsiyasiz ko'p odam. Nygard bir incidentni shunday tasvirlaydi: ertalab soat beshdagi konferens-aloqada yigirmaga yaqin odam, kimi joriy holatni aytadi, kimi xizmatni tiklash uchun qisqa muddatli yechim o'ylaydi, kimi sabab qidiradi, kimi esa shunchaki noto'g'ri ma'lumot tarqatadi (4-bob, 106-bet). Boshqa incidentda konferens-aloqada aks-sado beradigan yig'ilish xonasidagi o'n besh ovozni ajratish, ustiga odamlar stolidan ulanib "saytda muammo bor" deb xabar berishi tasvirlangan (16-bob, 257-bet).

Shuning uchun uch rolni ovoz chiqarib e'lon qilish korpusning amaliy tavsiyasi: boshqaruvchi qaror chiqaradi va ishni taqsimlaydi, tekshiruvchi gipotezani sinaydi va o'zgarish kiritadi, aloqachi ichki va tashqi xabarni yozadi. Nygard misolida bu funksiyalar amalda mavjud: operatsiya menejeri eskalatsiyani kim qilishini hal qiladi, keyin boshqa jamoadagi mutaxassis aloqaga tortiladi (16-bob, 258-260-bet).

Eskalatsiya zanjiri oldindan yozilgan bo'ladi. Nygard misolida kechayu kunduz ishlaydigan operatsiya markazi birinchi bo'lib kuzatadi, mahalliy injenerlik jamoasi esa yechimi ma'lum bo'lmagan muammo chiqqanda eskalatsiya yo'li sifatida turadi (16-bob, 254-bet).

Charchoq xavfi o'ylab topilgan emas. Aynan shu aviakompaniya incidentidan oldin o'zgarishni kiritgan mahalliy injener 22 soatlik smenadan keyin uyquga ketgan edi (2-bob, 24-bet). Uzoq incidentda almashishni rejalashtirish va boshqaruvchini tekshiruvchi bilan bitta odamga yuklamaslik shundan kelib chiqadi; aniq almashish davri korpus tanlovi.

## 35.3 Birinchi qadam: tiklash, sabab qidirish emas

Qoida kitobda to'g'ridan to'g'ri yozilgan: har qanday incidentda birinchi ustuvorlik xizmatni tiklash, tiklash tekshiruvdan oldin turadi; post-mortem uchun ma'lumot yig'ish yaxshi, lekin uzilishni uzaytirmasa (Nygard, 2-bob, 24-bet). Newman ham xuddi shu tartibni beradi: incidentdan keyingi birinchi diqqat tizimni qaytarib ishga tushirishda (Newman, *Building Microservices*, 2-nashr, 12-bob, "Blame").

Ikkinchi qoida: dalil yo'qoladi. Nygard post-mortem jinoyat tergovidan ham qiyin ekanini aytadi, chunki jasad yo'q: serverlar qayta ishga tushgan va uzilishga sabab bo'lgan holat endi mavjud emas (2-bob, 28-bet). Shu sababli u ma'lumot yig'ishning "mukammal balansi" deb oldindan yozilgan skriptlarni ko'rsatadi: barcha Java ilovalaridan thread dump va ma'lumotlar bazasi snapshotini oladigan skript improvizatsiya emas, uzilishni uzaytirmaydi, lekin keyingi tahlilga yordam beradi (2-bob, 24-bet).

Uchinchi qoida: nishonni tanlash. Nygard "dunyoni qayta yuklash", ya'ni har bir serverni qatlam-qatlam qayta ishga tushirish deyarli har doim ishlaydi, lekin uzoq davom etadi deb yozadi; ko'p holatda hammasini bo'g'ib turgan bitta aybdorni topish mumkin (2-bob, 24-bet).

To'rtinchi qoida: tasdiq metrikadan keladi. Nygard teskari aloqa halqasining oxirgi qadamini "tizimning yangi holatini kuzatish" deb qo'yadi (17-bob, 305-bet). "Tuzatdim" degan ishonch metrikasiz hech narsa anglatmaydi.

Tiklash harakati ma'lumotni buzishi mumkin bo'lgan holatlarda ketma-ketlikni o'zgartirish, ya'ni avval trafikni to'xtatish, korpusning amaliy tavsiyasi. Newman shunga yaqin ogohlantirish beradi: parallel ishlatishda bir xil buyurtma yangilanishini ikki marta yuborish yoki hisob-fakturani ikki marta to'lash xavfi borligini alohida eslatadi (7-bob, "Parallel Run").

## 35.4 Tiklash usullari: orqaga qaytarish, flag o'chirish, trafikni yo'naltirish

Kleppmann odam xatosidan tez tiklanish ro'yxatini beradi: konfiguratsiya o'zgarishini tez orqaga qaytarish mumkin bo'lsin, yangi kod bosqichma-bosqich chiqsin, shunda kutilmagan xato foydalanuvchilarning kichik qismiga tegadi (1-bob, 9-10-bet). Newman buni MTBF va MTTR orasidagi tanlov tilida aytadi: tiklash vaqtini qisqartirishning eng oddiy usuli yaxshi monitoring bilan birga juda tez orqaga qaytarish; muammo prodda erta sezilsa va erta qaytarilsa, mijozga ta'sir kamayadi (9-bob).

Shart bitta: migratsiya orqaga mos bo'lsin. Yangi versiya ustunni o'chirgan bo'lsa qaytarish ishlamaydi; migratsiyani ikki fazaga bo'lish mexanikasi 33-bobda.

```bash
# Qaysi versiya qachon chiqqanini ko'rish
kubectl rollout history deployment/payment-service -n prod

# Oldingi versiyaga qaytarish, bu eng tez va eng xavfsiz qadam
kubectl rollout undo deployment/payment-service -n prod

# Qaytarish tugashini kuzatish, belgilangan vaqtda tugamasa muammo boshqa joyda
kubectl rollout status deployment/payment-service -n prod --timeout=120s

# Ikki versiya orasidagi farqni olish, diagnostika uchun
git log --oneline v2.14.0..v2.15.0 -- src/main/java/com/shop/payment
```

Ikkinchi usul feature flag o'chirish. Nygard incidentida aynan shu g'oya qutqardi: do'kon kodida yetkazib berish jadvalini so'rash uchun alohida connection pool bor edi va uni bo'g'uv nuqtasi sifatida ishlatish mumkin bo'ldi. Nygard shuni ham yozadi: agar dasturchilar o'sha komponentga `enabled` xususiyatini qo'shgan bo'lsalar, uni `false` qilish oddiy ish bo'lardi (16-bob, 262-bet). Tezlik farqi o'lchangan: konfiguratsiya faylini o'zgartirib hamma serverni qayta ishga tushirish o'sha yuk ostida olti soatdan ko'p olardi, faqat connection pool ni dinamik qayta sozlab qayta ishga tushirish esa, nima qilish kerakligi ma'lum bo'lgach, besh daqiqadan kam vaqt oldi (16-bob, 263-bet).

Newman buni umumiy printsipga bog'laydi: deployment va release ikki alohida tushuncha, deployment kodni muhitga o'rnatish, release esa uni foydalanuvchiga ko'rsatish; ularni ajratish past xavfli relizning asosiy qoidasi (7-bob, "Separating Deployment from Release"). Flag shuning amaliy shakli.

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

Uchinchi usul trafikni yo'naltirish, va u faqat oldindan tayyorlangan bo'lsa ishlaydi. Nygard DNS round-robin ni aynan shu sababdan tanqid qiladi: mijoz serverga to'g'ridan to'g'ri ulanadi, shuning uchun bitta server o'lsa trafikni boshqa yoqqa burish imkoni yo'q, chunki DNS serverda web serverlarning sog'lig'i haqida ma'lumot yo'q va u ishlamay qolgan manzilni tarqatishda davom etadi (13-bob, 232-233-bet). Ya'ni yo'naltirish qatlami sog'liq haqida haqiqiy ma'lumotga ega bo'lishi kerak.

Sog'liq tekshiruvi mazmunli bo'lishi shart. Shu aviakompaniya incidentida monitoring CF da muammo ko'rsatmagan edi, chunki u faqat status sahifasini so'rayotgan va ilova serverlarining haqiqiy holati haqida deyarli hech narsa aytmayotgan edi (2-bob, 25-bet). Kubernetes readiness probe mexanikasi 31-bobda.

## 35.5 Diagnostika tartibi: nima o'zgardi, qachon boshlandi, nima umumiy

Birinchi savol: nima o'zgardi. Kleppmann yirik internet xizmatlari bo'yicha bir tadqiqotga tayanadi: uzilishlarning yetakchi sababi operatorlarning konfiguratsiya xatolari bo'lgan, apparat nosozliklari esa uzilishlarning faqat 10-25 foizida rol o'ynagan (1-bob, 9-bet). Nygard operatsiyada "post hoc, ergo propter hoc", ya'ni yaqin vaqt bo'yicha sababni belgilash mantiqiy xato bo'lsa ham, ko'p holatda yaxshi boshlang'ich nuqta ekanini aytadi, va buni "oxirgi bo'lib tegdingiz" deb nomlanishini eslatadi (2-bob, 27-bet). O'zgarishni topishning arzon yo'li ham shu kitobda: joriy konfiguratsiya fayllarini tungi zaxira nusxasidagi fayllar bilan solishtirish, shunda zaxiradan keyin nima o'zgargani ko'rinadi (2-bob, 28-bet).

Diagnostika paytidagi eng kam hisobga olinadigan o'zgarish manbasi esa operatorning o'zi. Nygard interaktiv murakkablik yuqori bo'lgan tizimda operatorning fikrlash modeli to'g'ri bo'lmasligini odatiy holat deb oladi, va natijasi aniq: operatorning "tuzatish" uchun qilgan harakati yashirin bog'lanishni qo'zg'atadi va incident ni kengaytiradi (Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 4-bob, 45-bet). Shuning uchun birinchi savoldagi "nima o'zgardi" ro'yxatiga incident boshlanganidan KEYIN qilingan harakatlar ham kiradi: qayta ishga tushirilgan pod, qo'lda o'chirilgan feature flag, kesh tozalash, pool kattalashtirish. Amaliy qoida ikkita. Birinchisi: har qo'lda harakat vaqti bilan incident kanaliga yoziladi, aks holda keyingi o'lchov o'zgarishi hodisaga emas, harakatga tegishli ekani bilinmaydi. Ikkinchisi: fikrlash modeli tasdiqlanmagan holatda qaytarib bo'lmaydigan harakat (ma'lumot o'chirish, failover, sxema o'zgartirish) qilinmaydi, chunki model noto'g'ri bo'lsa shu harakat yangi nosozlik qo'shadi.

Ikkinchi savol: qachon boshlandi, chunki aniq daqiqa o'zgarish ro'yxatini filtrlaydi.

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

Uchinchi savol: nima umumiy. Nygard incidentida ikki alohida ilova to'plami deyarli bir vaqtda to'liq qotib qoldi, va eng ravshan gipoteza ikkisi ham qiynalgan uchinchi narsaga bog'liq ekani bo'ldi; umumiy bog'liqlik aynan bitta servis edi (2-bob, 25-bet). Keyingi incidentda thread dump barcha front-end tugunlarida bir xil shaklni ko'rsatdi: bir nechta thread orqa tizimga murojaat qilmoqda, qolganlari esa shu murojaat uchun bo'sh ulanishni kutmoqda, shundan keyin diqqat orqa tizimga ko'chdi va u yerda ham xuddi shu shakl topildi (16-bob, 259-bet). Ya'ni xato bitta tugunda bo'lsa bu konfiguratsiya yoki resurs muammosi, hamma tugunda bir vaqtda boshlangan bo'lsa bu umumiy bog'liqlik.

Thread dump nega shu qadar kuchli: Nygard aytganidek, thread dump qo'lda bo'lsa, ilova ochiq kitob, siz manba kodini ko'rmagan ilova haqida ham qanday kutubxonalardan foydalanayotganini, qanday thread pool borligini, har birida qancha thread borligini va qaysi protokollar ishlatilayotganini bilib olasiz (2-bob, 29-bet).

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Birinchi topilgan gipotezaga yopishib qolish | Kuzatuv tasdiq izlashga moyil: Nygard OODA halqasi to'g'ri kuzatuvni talab qilishini, ya'ni orzu va tasdiq izlash (confirmation bias) bilan xiralashmagan kuzatuvni ta'kidlaydi (17-bob, 306-bet) | Ikki gipotezani yozib, ikkisini ham tekshirish |
| Bir vaqtda uchta o'zgarish kiritish | Har kim o'z fikrini sinaydi | Faqat boshqaruvchi ruxsat bergan bitta o'zgarish |
| Pod qayta ishga tushirish bilan "tuzatish" | Simptom yo'qoladi, dalil ham: tiklangan server o'zining uzilishga olib kelgan holatini saqlamaydi (2-bob, 28-bet), Nygard incidentida ketma-ket qayta ishga tushirish esa darhol yiqilib turardi (16-bob, 256-bet) | Avval oldindan yozilgan skript bilan thread dump va snapshot olinadi |
| Log'ni grep bilan qidirish | Markazlashgan log va bog'lovchi identifikator yo'q | Trace yoki tranzaksiya id bo'yicha so'rovni uchidan uchiga kuzatish (17-bob, 283-bet) |
| O'rtacha qiymat bilan tasdiqlash | Nygard incidentida sahifa javob vaqti shunchaki yuqori emas, timeout'lar sababli amalda cheksiz edi, statistika esa faqat tugagan so'rovlarning o'rtachasini ko'rsatardi; tugamagan so'rov o'rtachaga kirmaydi (16-bob, 258-259-bet) | Persentil va mijoz tomonidagi o'lchov bilan tasdiqlash |
| Soxta sog'liq tekshiruvi | Monitoring faqat status sahifasini so'raydi va ilovaning haqiqiy holati haqida hech narsa aytmaydi (2-bob, 25-bet) | Sintetik tranzaksiya: mijoz yo'lidan o'tadigan tekshiruv |
| Connection pool o'lchamini oshirish | "Pool tugadi" xabari ko'rinadi | Sekin so'rovni topish; pool va PostgreSQL bog'liqligi 27-bobda |
| Timeout qo'ymaslik | Nygard RMI ni xavfli deb bilgan sabab: chaqiruvni timeout bilan cheklash mumkin emas, natijada chaqiruvchi masofaviy serverdagi muammoga himoyasiz qoladi (2-bob, 31-bet) | Timeout qisqa, qayta urinish budjetli; tafsilot 32-bobda |

## 35.6 Muloqot: kimga, qanchalik tez-tez, qanday til bilan

Nygard muloqotni qo'shimcha ish deb emas, incidentning bir qismi deb qo'yadi: katta incidentdan keyin idrokni boshqarish incidentni boshqarishdan kam ahamiyatli emas (2-bob, 28-bet). Newman xuddi shu fikrni teskari tomondan beradi: ko'p tashkilot oqibatni noto'g'ri boshqarib incidentning ta'sirini kuchaytirgan, va bu brendga va mijoz bilan munosabatga yetgan zarar jarimadan alohida turadi (11-bob, "Respond").

Til qoidasi kitobdan keladi. Nygard post-mortem dalillarini ikkiga bo'ladi: ishonchli dalil, masalan uzilish vaqtidagi server loglari, va ishonchsiz dalil, masalan odamlarning nima ko'rganini aytishi; haqiqiy guvohlar kabi odamlar kuzatuvni taxmin bilan aralashtiradi va gipotezani fakt sifatida taqdim etadi (2-bob, 28-bet). Shundan amaliy qoida: faktni gipotezadan ajratib yozish. "Xato ulushi 14:05 da keskin oshdi" fakt, "menimcha yangi gateway sabab" gipoteza.

Taxminni sabab deb e'lon qilish narxi ham o'lchangan. Nygard noaniq yozilgan bitta log xabari ustida qanday afsona paydo bo'lganini aytadi: xabar bilan ma'lumotlar bazasining yiqilishi orasida hech qanday sababiy bog'liqlik yo'q edi, faqat vaqt bo'yicha yaqinlik bor edi, va shu yaqinlik administratorlarni olti oy davomida har hafta eng yuklangan vaqtda ma'lumotlar bazasini failover qilishga majbur qildi (17-bob, 283-bet).

Tashqi xabar ichki xabardan farq qiladi: mijozga "connection pool exhausted" deb yozish hech narsa anglatmaydi. Belgilangan ritmda xabar yuborish va yangi ma'lumot bo'lmasa ham keyingi xabar vaqtini aytish korpusning amaliy tavsiyasi; aniq intervalni jamoa tanlaydi. Ayrim holatlarda muddat tashqaridan keladi: Newman shaxsiy ma'lumot buzilishini GDPR tegishli organlarga 72 soat ichida xabar qilishni talab qilishini misol qiladi (11-bob, "Respond").

## 35.7 Incident jurnali va vaqt chizig'ini yozib borish

Vaqt chizig'i post-mortem hujjatining majburiy qismi: Google amaliyotida yaxshi post-mortem hodisaning aniqlanishidan tekshiruvga, tekshiruvdan hal qilinishiga qadar vaqt chizig'ini o'z ichiga oladi (Winters, Manshreck, Wright, *Software Engineering at Google*, 2-bob, "Blameless Postmortem Culture"). Uni keyin tiklash qiyin, chunki ishonchli dalil loglarda, ishonchsizi esa odamlarning xotirasida (Nygard, 2-bob, 28-bet). Shuning uchun yozuv real vaqtda boriladi: har qaror va o'zgarish vaqt bilan kanalga tushadi, aloqachi esa oxirida shu kanalni vaqt chizig'iga aylantiradi.

Log'da bog'lovchi identifikator bo'lishi shart. Nygard buni to'g'ridan to'g'ri talab qiladi: xabarlar tranzaksiya qadamlarini kuzatish uchun ishlatiladigan identifikatorni, masalan foydalanuvchi id, sessiya id, tranzaksiya id yoki so'rov kelganda berilgan ixtiyoriy raqamni o'z ichiga olishi kerak; uzilishdan keyin o'n ming qator log o'qish kerak bo'lganda grep qilinadigan satr juda ko'p vaqt tejaydi. U holat o'tishlarini log qilishni ham tavsiya qiladi, chunki holat o'tishlari yozuvi post-mortem tekshiruvida muhim bo'ladi (17-bob, 283-bet). Newman ham servislar orasidagi bog'liq chaqiruvlar to'plami uchun bitta correlation ID ni zarur deb biladi (6-bob va 10-bob).

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

Vaqt chizig'i ikki raqamni beradi: aniqlash vaqti va tiklash vaqti. Newman tiklash vaqtini MTTR deb nomlaydi va uni qisqartirishning eng oddiy yo'lini yaxshi monitoring bilan tez qaytarish deb ko'rsatadi (9-bob). Shundan xulosa: aniqlash uzun bo'lsa muammo monitoringda, tiklash uzun bo'lsa runbook va avtomatlashtirishda. Qaysi nuqtalarni majburiy belgilash korpus tanlovi, lekin Google ro'yxatidagi uch nuqta, ya'ni aniqlanish, tekshiruv va hal qilinish, eng kam to'plam.

## 35.8 Ayblamaydigan post-mortem: tuzilishi va yozish qoidalari

Newman ildiz sababni odamga aylantirish xavfini ochiq ko'rsatadi: "root cause analysis" iborasi bitta ildiz sabab borligini nazarda tutadi, va biz o'sha ildiz sababning odam bo'lishini qanchalik ko'p xohlashimiz hayratlanarli. U Telstra misolini keltiradi: uzilishdan bir necha soat keyin kompaniya aybni bitta xodimga yuklagan bayonot berdi, lekin bir odamning xatosi butun telekom operatorini tizzasiga keltira olsa, bu operator haqida o'sha odamdan ko'proq gapiradi; shundan keyin Telstra ketma-ket yana uzilishlarni boshdan kechirdi (12-bob, "Blame").

Ayblash mexanizmi aniq. Newman yozadi: incidentdan keyin odamlarni ayblash qisqa muddatli javobgarlikni o'zgadan o'zga surishdan boshlanib, qo'rquv madaniyatini yaratadi, odamlar nimadir buzilganini aytishga kelmay qo'yadi, natijada siz nosozlikdan o'rganish imkonini yo'qotasiz va o'sha muammolar qaytarilishiga o'zingizni tayyorlab qo'yasiz. Xatoni tan olish xavfsiz bo'lgan tashkilot esa o'rganish madaniyatining sharti (12-bob, "Blame"). Xavfsizlik incidentlari bo'limida u shu fikrni takrorlaydi: ayblash va qo'rquv madaniyati bo'lgan tashkilotlar katta incidentdan keyin yomon chiqadi, saboqlar o'rganilmaydi va hissa qo'shgan omillar yuzaga chiqmaydi (11-bob, "Respond").

Nygard shuning bahosini o'z tajribasida ko'rsatadi: uzilish ko'lami sababli ayb havoda uchib yurgan, hamma himoyada edi, va shu holat tergovchiga manba kodiga qonuniy kirishni qiyinlashtirdi (2-bob, 32-bet).

Tuzilish uchun tayanch Google amaliyotida. Yaxshi post-mortem quyidagilarni o'z ichiga oladi: hodisaning qisqa xulosasi; aniqlanishdan tekshiruvga, tekshiruvdan hal qilinishiga qadar vaqt chizig'i; hodisaning asosiy sababi; ta'sir va zarar bahosi; muammoni darhol tuzatish uchun harakat bandlari to'plami, egalari bilan; hodisa qaytarilmasligi uchun harakat bandlari to'plami; o'rganilgan saboqlar. Hujjat osongina ochiladigan joyda turishi va jamoa taklif qilingan o'zgarishlarni oxirigacha bajarishi ham shu ro'yxatning sharti (*Software Engineering at Google*, 2-bob). Google yirik prod nosozligining har birida post-mortem o'tkazadi; maqsad barmoq bilan ko'rsatish yoki keraksiz byurokratik tekshiruv kiritish emas, muammoning o'zagiga diqqat qilib uni bir marta va butunlay tuzatish (5-bob, "It's OK to fail").

Nygard tekshiruv kun tartibiga yana ikki savolni qo'shadi: nosozlikni uzilishga aylanishdan oldin aniqlash mumkin edimi, va buning qaytarilmasligi uchun nima qilinadi (2-bob, 28-bet). "Nima yaxshi ishladi" bo'limini qo'shish korpusning amaliy tavsiyasi: ishlagan himoyani bilish uni keyin kesib tashlashdan saqlaydi.

Yozish qoidalari: ism sabab sifatida ko'rsatilmaydi, rol nomi yetarli; taxmin "ehtimol" so'zi bilan belgilanadi. Hujjat qancha muddatda yozilishi va qaysi darajadan boshlab majburiy bo'lishi jamoa qarori; Google misolida chegara "yirik prod nosozligi".

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Incident darajasi | Xato turi bo'yicha | Nosozlik emas, uzilish bo'yicha: foydalanuvchiga xizmat to'xtadimi (Kleppmann, 1-bob, 7-bet) |
| Birinchi harakat | Sababni izlash | Xizmatni tiklash tekshiruvdan oldin turadi (Nygard, 2-bob, 24-bet) |
| Rollar | Hamma debug qiladi | Ajratilgan rollar: aks holda yigirma kishilik aloqada bir qismi noto'g'ri ma'lumot tarqatadi (Nygard, 4-bob, 106-bet) |
| Tiklash | Qo'lda tuzatish yoziladi | Qaytarish, flag, trafik yo'naltirish oldindan tayyor (Kleppmann, 1-bob, 9-10-bet) |
| Dalil | Qayta ishga tushirib yuboriladi | Oldindan yozilgan skript bilan dump olinadi (Nygard, 2-bob, 24-bet) |
| Post-mortem | Kim xato qildi | Qaysi himoya yo'q edi; ayblash faktni yashiradi (Newman, 12-bob) |
| Harakat bandlari | "Ehtiyot bo'lamiz" | Darhol tuzatish va qaytarilmaslik bandlari, egasi bilan (*SWE at Google*, 2-bob) |
| Alert | Ko'proq alert yaxshi | Har bir alert harakatga yo'naltiradi (Newman, 10-bob, EEMUA mezonlari) |
| On-call | Eng biladigan odam doim navbatda | Navbat aylanadi va runbook yoziladi: improvizatsiya qimmat (Nygard, 16-bob, 262-bet) |

## 35.9 Besh marta "nega" va tizimli sabablarga yetish

Savolni takrorlab tizim darajasiga chiqish korpusning amaliy tavsiyasi: har javobdan keyin yana so'raysiz, toki javob tizim yoki jarayon haqida bo'lgunicha. Misol: nega to'lov ishlamadi, servis gateway javobini uzoq kutdi; nega kutdi, HTTP client timeout qo'yilmagan; nega qo'yilmagan, client qo'lda yozilgan va markazlashgan builder ishlatilmagan; nega ishlatilmagan, builder haqida hujjat va avtomatik qoida yo'q; nega yo'q, bu kod review'ning og'zaki an'anasi edi.

Zanjirning odamga borib to'xtamasligi esa kitobda yozilgan talab. Newman ildiz sababni odam deb belgilashga moyillikni ochiq tanqid qiladi va aybdor topilgan tergovdan keyin uzilishlar davom etganini ko'rsatadi (12-bob, "Blame"). Kleppmann teskari yo'nalishni beradi: ishonchsiz odamlar bilan ishonchli tizim qurishning yo'li xato qilish imkoniyatini kamaytiradigan dizayn, odamlar ko'p xato qiladigan joyni xato uzilishga aylanadigan joydan ajratish, va odam xatosidan tez tiklanish (1-bob, 9-10-bet). Ya'ni oxirgi javob tizimdagi o'zgarishga aylanishi kerak: og'zaki an'ana avtomatik qoidaga ko'chadi, chunki avtomatik qoida charchamaydi. Bunday tekshiruvni yozish testlash qo'llanmasidagi arxitektura qoidalari bo'limida.

Ikkinchi tuzoq bitta zanjir bilan cheklanish. Newman ayblash madaniyatida "hissa qo'shgan omillar yuzaga chiqmaydi" deb yozadi, ya'ni omil bittadan ko'p (11-bob, "Respond"). Nygard aviakompaniya misolida savolni qayta qo'yadi: har bir shunday xatoni yo'q qilishni kutish xayol, xatolar bo'ladi va ularni yo'q qilish emas, ulardan omon qolish kerak; to'g'ri savol bitta tizimdagi xato qolgan hamma narsaga ta'sir qilishini qanday to'sish (2-bob, 34-bet). Jiddiy incidentda shuning uchun uch sabab birlashadi: xato kod, yetishmagan alert va mavjud bo'lmagan tiklash yo'li.

## 35.10 Harakat bandlari: egasi, muddati, tekshiruvi bo'lsin

Post-mortem qiymati harakat bandlarida. Google ro'yxati ikki guruhni ajratadi: muammoni darhol tuzatish bandlari, egalari bilan, va hodisa qaytarilmasligi uchun bandlar; hujjat osongina ochiladigan joyda turishi va jamoa taklif qilingan o'zgarishlarni oxirigacha bajarishi ham shu ro'yxatda (*Software Engineering at Google*, 2-bob). Ya'ni ega majburiy rekvizit, ikki guruh esa majburiy bo'linish.

"Monitoringni yaxshilash" band emas. Aniq ish, bitta ega va aniq muddat yozilishi, ustiga tekshiruv usuli qo'shilishi korpusning amaliy tavsiyasi: "gateway latency uchun chegarali alert qo'shish, egasi platform jamoasi, muddat belgilangan, tekshiruv sun'iy sekinlashtirish bilan" shaklida band bajarilganini isbotlash mumkin bo'ladi.

Zararni kamaytirish bandlari e'tibordan qolmasligi kerak. Newman MTBF va MTTR orasidagi tanlovni muhokama qilganda ko'rgan holatini aytadi: funksional test to'plamlariga vaqt sarflaydigan tashkilotlarning ko'pi monitoringni yaxshilashga yoki nosozlikdan tiklanishga deyarli hech narsa sarflamaydi, natijada xatolarni to'liq yo'q qila olmay, prodda chiqqanda tayyor bo'lmay qoladi (9-bob). Aynan ikkinchi guruh keyingi incidentda qutqaradi.

```yaml
# Harakat bandi natijasi: majburiy timeout va alert chegarasi konfiguratsiyada.
# Qiymatlar misol uchun: har bir chegara o'z o'lchovingizdan chiqadi.
spring:
  datasource:
    hikari:
      maximum-pool-size: 20          # pool va PostgreSQL bog'liqligi 27-bobda
      connection-timeout: 2000       # pool bo'sh bo'lmasa xato qaytadi, cheksiz kutmaydi
      validation-timeout: 1000
      leak-detection-threshold: 20000 # uzoq ushlab turilgan connection log'ga tushadi
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

Backlog'ga tushgan band yo'qoladi. Muntazam ko'rib chiqish uchun tayanch bor: Nygard har hafta o'tgan haftaning muammo ticketlarini ko'rib chiqishni, qaytarilayotgan va eng ko'p vaqt yeyayotgan muammolarni izlashni tavsiya qiladi (17-bob, 307-bet). Bajarilmagan band soni ishonchlilik qarzining eng halol metrikasi; muddat chegaralari jamoa qarori.

## 35.11 On-call navbati: adolatli taqsimot, ogohlantirish charchoqini kamaytirish

Navbat amalda aylanadi. Nygard misolida yetkazib berish jadvalini boshqaradigan jamoa kechayu kunduz navbatchi xodimga ega emas edi va pager'ni navbat bilan bir-biriga uzatardi (16-bob, 259-bet). Katta tashkilotda tuzilma ikki qatlamli: kechayu kunduz yuqori malakali injenerlar bilan ishlaydigan operatsiya markazi kuzatadi va boshqaradi, mahalliy jamoa esa zaxira va yechimi ma'lum bo'lmagan muammo uchun eskalatsiya yo'li bo'lib turadi (16-bob, 254-bet).

Navbat bitta odamga qolmasligi va kompensatsiya bilan bo'lishi korpusning amaliy tavsiyasi. Charchoqning narxi esa kitobda o'lchangan: o'zgarishni kiritgan mahalliy injener 22 soatlik smenadan keyin ketgan edi (2-bob, 24-bet), va charchagan odam qaroriga ishonish qimmat.

Runbook yo'qligining narxi ham o'lchangan. Nygard eng og'ir nuqtani shunday yozadi: sayt o'chgan, bu holat uchun qo'llanma yo'q, biz incidentning o'rtasidayik va yechimni improvizatsiya qilishimiz kerak (16-bob, 262-bet). U boshqa joyda bu fikrni qisqa qoidaga aylantiradi: ish qizigan payt improvizatsiya sizga do'st emas (2-bob, 24-bet). Runbook'ga nima kirishi, ya'ni qaysi metrikaga qarash, qanday flag bor, qanday qaytarish va kimga eskalatsiya qilish, korpusning amaliy tavsiyasi.

Charchoqni kamaytirishning eng kuchli vositasi alert sifatini o'lchash, chunki noto'g'ri alert javobni o'ldiradi. Nygard incidentida navbatdagi injener yuqori CPU haqida bir necha marta pager olgan, lekin javob bermagan edi, chunki o'sha jamoa doimo o'tkinchi CPU cho'qqilari uchun pager olardi va ular soxta signal bo'lib chiqardi; barcha soxta pozitivlar ularni yuqori CPU holatini e'tiborsiz qoldirishga juda yaxshi o'rgatib qo'ygan edi (16-bob, 261-bet). Tungi uyg'otish sonini o'lchash va eng shovqinli alertni tuzatish korpusning amaliy tavsiyasi; chegara raqami jamoa qarori.

## 35.12 Ogohlantirishlar sifati: har bir alert bajariladigan ish bo'lsin

Newman alertning maqsadini Shorrock'dan iqtibos bilan beradi: alertning vazifasi foydalanuvchi diqqatini o'z vaqtida e'tibor talab qiladigan muhim jihatlarga yo'naltirish. U yerda EEMUA tuzgan mezonlar ro'yxati keltirilgan, va Newman uni o'zi ko'rgan eng yaxshi ta'rif deb ataydi: alert tegishli (qiymati bo'lsin), takrorlanmaydigan, o'z vaqtida, ustuvorlashtirilgan, tushunarli, diagnostik (nima buzilgani ravshan bo'lsin), tavsiyaviy (operator qanday harakat qilishi kerakligini tushunishga yordam bersin) va diqqatni eng muhim masalaga qaratuvchi bo'lishi kerak (10-bob, "Toward better alerting"). "Tavsiyaviy" mezoni aynan shu bo'limning asosiy talabini beradi: javob bo'lmasa, bu alert emas, dashboard elementi.

Newman savolni ham sodda qo'yadi: bu muammo kimnidir tunda uyg'otishi kerakmi. U Google misolini keltiradi: qattiq disk nosozligi tizim uni ko'taradigan qilib qurilgani uchun odatiy ish deb qaralgan, ish vaqtidan tashqari odam chaqirishga arzimaydigan, lekin ish kunida xabar beriladigan hodisa bo'lgan (10-bob, "Some problems are worse than others").

Shovqinning narxi faqat bezovtalik emas. Newman alert charchog'ini ikki og'ir misol bilan ko'rsatadi: 1979 yildagi Three Mile Island reaktoridagi qisman eriish tergovi operatorlar ko'rgan alertlar soni ularni shunday bosib qo'yganini, qanday harakat kerakligini aniqlash imkonsiz bo'lganini ko'rsatdi, operatorlardan biri "alarm panelini uloqtirib tashlagim keldi, u bizga foydali ma'lumot bermayotgan edi" deb aytgan; yaqinroq misolda 737 Max bo'yicha hisobot bir vaqtda ishga tushgan chalkash alertlarni halokatlarga hissa qo'shgan omil deb belgilagan (10-bob, "Alert fatigue"). Nygard misolida esa soxta pozitivlar jamoani haqiqiy signalni e'tiborsiz qoldirishga o'rgatgan edi (16-bob, 261-bet).

Alert simptomga qo'yilishi shu yerdan kelib chiqadi. Nygard incidentida tashqi monitoring saytga haqiqiy mijoz kabi murojaat qilardi, va u qizil bo'lganda mijozlar xarid qila olmasligi va daromad yo'qolayotgani ma'lum bo'lardi (16-bob, 257-bet). Newman buni semantik monitoring deb nomlaydi: xato borligini izlash o'rniga doimiy bitta savolni berish kerak, tizim biz kutgandek ishlayaptimi (10-bob, "Semantic Monitoring").

```yaml
# Simptom asosidagi alert: mijoz ko'radigan xatolik ulushi.
# Chegara va oyna uzunligi misol uchun: ularni o'z o'lchovingizdan oling.
groups:
  - name: payment-slo
    rules:
      - alert: PaymentErrorRateHigh
        expr: |
          sum(rate(http_server_requests_seconds_count{uri="/api/payments",status=~"5.."}[5m]))
          / sum(rate(http_server_requests_seconds_count{uri="/api/payments"}[5m])) > 0.02
        for: 5m                      # qisqa tebranishda uyg'otmaydi
        labels:
          severity: page             # telefon bilan uyg'otish
          service: payment
        annotations:
          summary: "To'lov API xato ulushi chegaradan yuqori"
          impact: "Mijozlar to'lovni yakunlay olmaydi"
          action: "payment.new-gateway flag'ini o'chirish, keyin oxirgi deploy'ni qaytarish"
          runbook_url: "https://wiki.internal/runbook/payment-error-rate"
```

Har alertda runbook havolasi va birinchi harakat bo'lishi EEMUA ning "tavsiyaviy" mezonining bajarilishi. Alertlarni muntazam tozalash uchun ham tayanch bor: Nygard metrika foydali ma'lumot berishni to'xtatgan zahoti uni ko'rib chiqishni to'xtatishni aytadi, chunki relizdan bir oy keyin siz tayangan hisobotlar ikki yildan keyin qiymatsiz yoki hatto chalg'ituvchi bo'ladi, va har to'rt-olti oyda eski korrelyatsiyalar hali ham to'g'ri ekanini qayta tekshirishni tavsiya qiladi (17-bob, 308-bet). Hech kim o'qimaydigan hisobotning narxi haqidagi fikri alertga ham tegishli: u pul va vaqt yeydi, qiymat bermaydi va soxta xotirjamlik yaratadi, chunki dunyodagi eng yaxshi ma'lumot ham hech kim qaramasa yordam bermaydi (17-bob, 305-bet).

## 35.13 To'liq post-mortem namunasi: to'lov servisi uzilishi misolida

Shablon Google ro'yxatiga va Nygard qo'shgan ikki savolga tayanadi.

```markdown
# Post-mortem: <servis> <davomiylik> uzilishi

- Sana, daraja, boshqaruvchi, hujjat holati

## Qisqa xulosa
Uch gap: nima buzildi, nega ta'sir qildi, nima bilan tiklandi.

## Ta'sir va zarar bahosi
- Davomiyligi va aniq vaqt oralig'i
- Muvaffaqiyatsiz so'rov soni va zarar ko'rgan mijoz soni
- Ma'lumot yo'qolishi yoki buzilishi bo'ldimi
- SLO byudjetining qancha ulushi sarflandi

## Vaqt chizig'i
Aniqlanish, tekshiruv, hal qilinish.

## Asosiy sabab
Zanjir tizim yoki jarayonga borib tugaydi, odamga emas.

## Nega uzilishga aylanishdan oldin aniqlanmadi
## Nega tezroq tiklanmadi
## Nima yaxshi ishladi
## O'rganilgan saboqlar

## Harakat bandlari
| Ish | Tur (darhol tuzatish / qaytarilmaslik) | Egasi | Muddat | Tekshiruv |
|---|---|---|---|---|
```

Quyida shu shablonning to'ldirilgan ko'rinishi bor. Bu o'quv uchun o'ylab topilgan misol, haqiqiy incident hisoboti emas: raqamlar shablonni ko'rsatish uchun qo'yilgan.

```markdown
# Post-mortem: to'lov servisi uzilishi (o'quv misoli)

Daraja P1, boshqaruvchi platform navbatchisi.

## Qisqa xulosa
Yangi gateway client'ida read timeout yo'q edi. Provayder sekinlashganda
Tomcat thread'lari band bo'ldi va /api/payments javob bermay qoldi.

## Ta'sir va zarar bahosi
- Uzilish davomiyligi va aniq vaqt oralig'i yoziladi
- Muvaffaqiyatsiz to'lov va zarar ko'rgan mijoz soni yoziladi
- Ikki marta debet yo'q, idempotency key ishladi
- Oylik SLO byudjetining sarflangan ulushi yoziladi

## Vaqt chizig'i
- Deploy, flag kichik ulush trafikda; p99 keskin oshdi; alert ishga tushdi
- Thread dump: thread'larning katta qismi socket read da kutmoqda
- Flag o'chirildi; xato ulushi normaga qaytdi

## Asosiy sabab
Client umumiy builder'siz tuzilgan, timeout qo'llanmagan. Izolyatsiya
yo'q edi, shuning uchun boshqa endpoint'lar ham ta'sirlandi.

## Harakat bandlari
| Ish | Tur | Egasi | Muddat | Tekshiruv |
|---|---|---|---|---|
| Client faqat umumiy builder'dan | qaytarilmaslik | payments | belgilangan | CI qoidasi |
| Gateway latency alert | darhol tuzatish | platform | belgilangan | sekinlashtirish testi |
```

Shablonning qiymati tartibda: bir xil tuzilish o'qishni tezlashtiradi va bandlarni bir joyga yig'adi. Google amaliyoti buni ochiq aytadi: nosozlikni to'g'ri hujjatlashtirish boshqalarga, hozir va keyin ishlaydiganlarga, nima bo'lganini bilish va tarixni qaytarmaslikni osonlashtiradi (*Software Engineering at Google*, 2-bob).

## 35.14 Alert aniqligi (precision) va qamrovi (recall) ni o'lchash

35.12 alert qanday bo'lishi kerakligini aytdi. Keyingi savol o'lchov: jamoangizdagi alertlar o'sha mezonga tushyaptimi yoki yo'qmi, buni qanday bilasiz. Orosz shu yerga qidiruv sifatidan tanish ikki raqamni olib kiradi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 24-bob, 347-348-bet).

Precision alertlarning qanchasi haqiqiy muammoni ko'rsatganini o'lchaydi. Orosz misoli: precision 30 foiz bo'lgan tizimda o'nta alertning uchtasi uzilish, qolgani shovqin; 100 foiz precision faqat uzilishni ko'rsatadigan alert chiqaradi (24-bob, 347-348-bet). Recall esa uzilishlarning qanchasi uchun alert chiqqanini o'lchaydi: recall 30 foiz bo'lgan tizimda o'nta uzilishning uchtasiga alert kelgan, 100 foizda har bir uzilishga alert kelgan (24-bob, 348-bet).

Ideal on-call tizimi ikkisida ham 100 foizga ega, lekin amalda ikkisi bir-biriga qarshi turadi. Orosz almashinuvni ochiq yozadi: shovqinli alertni o'chirganda precision ko'tariladi, lekin alert chiqmagani uchun uzilishni o'tkazib yuborish xavfi paydo bo'ladi va recall tushadi; uzilishlarni ko'proq ushlash uchun yangi alert qo'shilsa recall ko'tariladi, lekin precision tushishi mumkin (24-bob, 348-bet). Shuning uchun ikkisi birga o'lchanadi: bitta raqam qaysi tomonga qarab ishlash kerakligini aytmaydi.

| Raqam | Nimani o'lchaydi | Qanday yig'iladi | Pasayishi nimani anglatadi |
|---|---|---|---|
| Precision | chiqqan alertlarning qanchasi haqiqiy uzilish | navbatchi har alertni "uzilish" yoki "shovqin" deb belgilaydi | tungi uyg'otishlar behuda, charchoq o'sadi |
| Recall | uzilishlarning qanchasiga alert chiqqan | incident ko'rigida har uzilish uchun "alert chiqdimi" savoli | uzilishni mijoz birinchi bo'lib aytadi |

O'lchashning ikkala usuli ham odam qo'li bilan bajariladi. Orosz birinchisini shunday qo'yadi: navbatchi injener har bir alert uzilish uchunmi yoki shovqinmi ekanini yozib borsin, va ko'p on-call vositasi buni kuzatishga yordam beradi, bermasa bu funksiyani qurish yoki sotib olish kerak (24-bob, 348-bet). Ikkinchisi incident ko'rigiga biriktiriladi: oxirgi uzilishlar bo'ylab o'tib, "uzilish bo'layotganini ko'rsatadigan alert chiqdimi" degan savolga javob berilsa, recall foizi chiqadi (24-bob, 348-bet). Ya'ni injenerlar alertni belgilashi, incident ko'ruvchilar esa uzilishdan oldin alert bo'lganini belgilashi kerak; mavjud on-call tizimingiz buni qo'llab-quvvatlamasa, uni kengaytirish ishi paydo bo'ladi (24-bob, 348-bet).

Amalda bu ikki raqam 35.10 dagi harakat bandlari bilan bog'lanadi. Precision past bo'lsa band "eng shovqinli uchta alertni qayta yozish yoki o'chirish" bo'ladi, recall past bo'lsa band "oxirgi uzilishni ushlagan bo'lardigan alertni qo'shish" bo'ladi. Qaysi foiz chegarasi "yetarli" deb hisoblanishi korpusda raqam bilan belgilanmaydi: Orosz ham chegara bermaydi, faqat ikkisini o'lchab qaysi tomonga ishlash kerakligini ko'rishni aytadi.

## 35.15 On-call zanjiri va navbat o'lchami: birlamchi, ikkilamchi, eskalatsiya

35.11 navbatning adolatli taqsimoti va charchoq haqida edi. Bu bo'lim navbatning mexanikasini beradi: alert kimga boradi, javob bo'lmasa nima bo'ladi va navbatda necha odam bo'lishi kerak.

Orosz tipik tuzilmani uch qismdan iborat qilib sanaydi. Birlamchi navbatchi jamoaning prod tizimlari uchun alertlarni qabul qiladigan injener. Pager ilovasi alertni o'sha birlamchi navbatchiga yo'naltiradi. Alert kelganda navbatchi uni belgilangan vaqt ichida, masalan 10 daqiqada, tasdiqlashi kerak; tasdiq bo'lmasa alert eskalatsiya qilinadi va zanjirdagi keyingi odamni, ya'ni ikkilamchi navbatchini chaqiradi, u ham tasdiqlamasa uchlamchi navbatchiga o'tadi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 24-bob, 350-bet). Orosz ko'p kompaniyada birlamchi va ikkilamchi navbat jamoa a'zolaridan tuzilishini, uchinchi qatlam esa odatda injenerlik menejerlari va undan yuqoridagi menejment zanjiri bo'lishini yozadi (24-bob, 350-bet).

Zanjir alertning shoshilinchligi bilan bog'lanadi. Orosz oddiy ikki toifani beradi: shoshilinch alert darhol tasdiqlanishi va javob berilishi kerak, u push xabar yuboradi, telefon qilishga urinadi va javob bo'lmasa zanjir bo'ylab eskalatsiya qiladi; shoshilinch bo'lmagan alert esa ish vaqtidan tashqari hech kimni bezovta qilmaydi va ish kuniga qoldiriladi (24-bob, 347-bet).

Navbat o'lchami arifmetika bilan chiqadi. Orosz hisobi: navbat odatda bir haftaga olinadi, oyda o'rtacha 4.5 hafta bor, shuning uchun hech kim oyiga bir martadan ko'p navbatda bo'lmasligi uchun jamoada kamida 5 kishi kerak; 6 kishi ta'til va kasallikni ham qoplaydi, va uning umumiy qoidasi sog'lom navbatda kamida 6 odam bo'lishi (24-bob, 350-bet). Agar o'sha odamlar birlamchi navbatdan tashqari ikkilamchi navbatchi ham bo'lsa, sog'lom navbat 10-12 kishidan iborat bo'ladi (24-bob, 350-bet). Jamoa 6 dan kichik bo'lsa, Orosz yaqin sohadagi ikki kichik jamoaning navbatini birlashtirishni keng tarqalgan yechim deb keltiradi (24-bob, 350-bet).

| Tuzilma | Orosz keltirgan o'lcham | Nega shunday |
|---|---|---|
| Faqat birlamchi navbat | kamida 5 kishi | oyda 4.5 hafta, oyiga bir martadan ko'p emas |
| Ta'til va kasallik bilan | kamida 6 kishi | umumiy qoida sifatida beriladi |
| Birlamchi va ikkilamchi birga | 10-12 kishi | bir odam ikki rolni tez-tez olmasin |
| 6 dan kichik jamoa | ikki jamoa navbatini birlashtirish | aks holda oyiga bir martadan ko'p tushadi |

Oxirgi savol navbatchi haftasida boshqa ish qiladimi. Orosz to'rt yondashuvni sanaydi: navbatni support ishi bilan birlashtirish; loyiha ishini umuman kutmaslik va faqat navbat ishini, jumladan alert shovqinini kamaytirish va runbook yozishni berish; navbatchida loyiha uchun quvvat yo'q deb hisoblash va rejani shunga qarab tuzish; yoki navbatchi quvvatining ma'lum foizini loyihaga ajratish (24-bob, 352-353-bet). Oxirgisini u eng mo'rt deb ko'rsatadi, chunki navbat yuki oldindan aytib bo'lmaydigan narsa (24-bob, 353-bet). Qaysi variant tanlanishi jamoa va menejer qarori; muhimi, variant oldindan aytilgan bo'lsin, aks holda navbatchidan ikkala ish ham kutiladi.

## 35.16 Pre-mortem: nosozlik ro'y berishidan oldin sabablarni sanash

35.8 dagi post-mortem hodisadan KEYIN yoziladi. Pre-mortem teskari yo'nalishda ishlaydi va hodisadan OLDIN bajariladi. Orosz uni katta o'zgarishni chiqarish tayyorgarligining bandi sifatida beradi: rollout barbod bo'lsa, sabablari nima bo'lishi mumkin edi degan savolni qo'yib, mumkin bo'lgan ssenariylarni xaritaga tushirish, keyin har biri uchun bunday nosozlikni qanday aniqlash va uni sodir bo'lishidan qanday to'sish mumkinligini aniqlash (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 15-bob, 215-bet).

Farq mexanikada. Post-mortem allaqachon sodir bo'lgan hodisaning hissa qo'shgan omillarini qidiradi, pre-mortem esa hali sodir bo'lmagan nosozlikni "sodir bo'ldi" deb faraz qilib, shundan orqaga qarab sabab qidiradi. Shakl ham foyda beradi: savol kimningdir rejasini tanqid qilish emas, berilgan natijaning sababini topish bo'lgani uchun "bu ishlamasligi mumkin" deyish osonlashadi. Bu 35.8 dagi ayblamaydigan yondashuvning hodisadan oldingi ko'rinishi.

Mashq uch ustunda yoziladi: faraz qilingan nosozlik, uni aniqlash usuli, uni to'sish usuli. Quyidagi misollar sxema relizi (33.14) uchun, ro'yxatning o'zi korpus tavsiyasi.

| Faraz qilingan nosozlik | Qanday aniqlaymiz | Qanday to'samiz |
| --- | --- | --- |
| Backfill replikani ortda qoldirdi | `pg_stat_replication` lag alerti | bo'lak kattaligini kamaytirish, lag bo'yicha tormoz (33.9) |
| Yangi o'qish yo'li eskisidan sekin | yo'l bo'yicha ajratilgan p99 metrikasi | feature flag bilan eski yo'lga qaytish (35.4) |
| Migratsiya DDL jadvalni bloklab qo'ydi | lock kutish alerti | `lock_timeout` va qayta urinish (33.5) |
| Dual write bir tomonda yozmay qoldi | ikki manbani solishtiradigan sanoq | contract qadamini kechiktirish (33.11) |
| Yangi xato sinfi alertga tushmadi | bake oynasida xato turlarini qo'lda ko'rish | yetishmayotgan alertni oldindan qo'shish (35.12) |

Natija ikki ro'yxat: yetishmayotgan alertlar va yetishmayotgan to'siqlar. Ikkalasi ham rollout boshlanishidan oldin bajariladigan ish va post-mortem harakat bandlari kabi egasi hamda muddati bilan yoziladi (35.10). Yozuv keyin ham qoladi: hodisa ro'y bersa, "bu ssenariy ro'yxatda bor edimi" degan savol qaysi himoya bo'g'ini yetishmaganini tez ko'rsatadi.

## 35.17 Amalda qo'llash

- [ ] Incident darajalari jadvalini yozing: har daraja uchun biznes mezoni (nosozlik emas, uzilish), javob vaqti va uyg'otish usuli.
- [ ] Barcha Java ilovalardan thread dump va DB snapshot oladigan skriptni oldindan yozib qo'ying, shunda dalil yig'ish improvizatsiya bo'lmaydi va uzilishni uzaytirmaydi.
- [ ] Eng muhim uch servis uchun runbook yarating: metrika havolalari, flag nomlari, qaytarish buyrug'i, eskalatsiya ro'yxati.
- [ ] Har bir xavfli yangi yo'lni feature flag ostiga oling va flag'ni pod qayta ishga tushirmasdan o'chirib ko'ring.
- [ ] Sog'liq tekshiruvingiz status sahifasini emas, mijoz yo'lidan o'tadigan sintetik tranzaksiyani so'rayotganini tekshiring.
- [ ] Alertlarni EEMUA mezonlari bo'yicha ko'rib chiqing: tegishli, takrorlanmaydigan, o'z vaqtida, ustuvorlashtirilgan, tushunarli, diagnostik, tavsiyaviy, diqqatni qaratuvchi. Mezonga tushmaganini o'chiring yoki qayta yozing.
- [ ] Barcha HTTP client va DB so'rovlariga timeout qo'yilganini tekshiradigan avtomatik qoida qo'shing.
- [ ] Log xabarlarida tranzaksiyani uchidan uchiga kuzatadigan identifikator borligini tekshiring, incident operatsiyalarini incident id bilan belgilang.
- [ ] Post-mortem shablonini repoga joylashtiring va oxirgi yirik uzilishni shu shablon bilan qayta yozib ko'ring.
- [ ] Har hafta o'tgan haftaning ticketlarini va ochiq harakat bandlarini ko'rib chiqing: qaytarilayotgan va eng ko'p vaqt yeyayotgan muammolarni izlang.

## Manbalar

- Michael T. Nygard, *Release It! Design and Deploy Production-Ready Software*, 1-nashr, Pragmatic Bookshelf, 2007, 2-bob (24-34-bet) - tiklash tekshiruvdan oldin turishi, Severity 1 va bir soatlik SLA chegarasi, SLA ta'rifi, oldindan yozilgan dump skripti, "dunyoni qayta yuklash" narxi, umumiy bog'liqlik gipotezasi, status sahifasiga tayangan soxta monitoring, 22 soatlik smena, post hoc xatosi, konfiguratsiyani zaxira bilan solishtirish, thread dump nima beradi, timeout qo'yilmagan chaqiruvning xavfi, ayb muhiti tergovni qiyinlashtirishi, "xatolardan omon qolish" savoli
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 4-bob (106-bet) - yigirma kishilik incident aloqasida rollar aralashishi va noto'g'ri ma'lumot tarqalishi
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 13-bob (232-233-bet) - DNS round-robin da sog'liq ma'lumoti yo'qligi sababli trafikni burish imkonsizligi
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 16-bob (254-263-bet) - ikki qatlamli navbatchilik va eskalatsiya yo'li, pager'ni navbat bilan uzatish, o'rtachaning timeout'ni yashirishi, umumiy shaklni thread dump bilan topish, soxta pozitivlar jamoani e'tiborsizlikka o'rgatishi, qo'llanma yo'qligi va improvizatsiya, `enabled` xususiyati bo'lsa edi degan xulosa, besh daqiqa va olti soat farqi, tashqi monitoring mijoz yo'lidan o'tishi
- Michael T. Nygard, *Release It!*, 1-nashr, 2007, 17-bob (270, 283, 305-308-bet) - hodisalarning "low-medium-high" va "warn-severe-critical" toifalanishi, log xabarida tranzaksiya identifikatori va holat o'tishlari, noaniq xabar olti oylik soxta amaliyot tug'dirgani, hech kim o'qimaydigan hisobotning soxta xotirjamligi, teskari aloqa halqasi va yangi holatni kuzatish, confirmation bias, haftalik ticket ko'rigi, foydasiz metrikani to'xtatish va to'rt-olti oyda korrelyatsiyani qayta tekshirish
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 1-bob (6-10-bet) - fault va failure farqi, nosozlikni uzilishga aylanishdan to'sish, operator konfiguratsiya xatolari uzilishlarning yetakchi sababi va apparat nosozligining 10-25 foiz ulushi, odam xatosidan tez tiklanish ro'yxati (tez qaytarish, bosqichma-bosqich chiqarish, xato joyini uzilish joyidan ajratish)
- Sam Newman, *Building Microservices*, 2-nashr, O'Reilly, 2021, 7-bob - deployment va release ni ajratish, parallel ishlatishda takroriy to'lov xavfi
- Sam Newman, *Building Microservices*, 2-nashr, 2021, 9-bob - MTBF va MTTR tanlovi, tez qaytarish plus monitoring tiklash vaqtini qisqartirishi, tashkilotlarning tiklanishga kam sarflashi
- Sam Newman, *Building Microservices*, 2-nashr, 2021, 10-bob - alertning maqsadi, EEMUA mezonlari, "tunda uyg'otishi kerakmi" savoli, alert charchog'i (Three Mile Island va 737 Max), semantik monitoring
- Sam Newman, *Building Microservices*, 2-nashr, 2021, 11-bob va 12-bob - incidentdan keyingi muloqotning ta'sirga qo'shadigan zarari va GDPR 72 soat misoli, ayblash madaniyatida saboq va hissa qo'shgan omillarning yuzaga chiqmasligi, "root cause" ni odamga aylantirish va Telstra misoli
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 2-bob ("Blameless Postmortem Culture") va 5-bob - post-mortem tarkibi (xulosa, vaqt chizig'i, asosiy sabab, ta'sir bahosi, egasi bor darhol tuzatish bandlari, qaytarilmaslik bandlari, saboqlar), hujjat ochiq turishi va bandlarning oxirigacha bajarilishi, har yirik prod nosozligida post-mortem o'tkazilishi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 24-bob (347-348-bet) - shoshilinch va shoshilinch bo'lmagan alert, precision va recall ta'riflari va 30 foizlik misollari, ikkisi orasidagi almashinuv, navbatchining alertni belgilashi va incident ko'rigida recall ni hisoblash usuli
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 24-bob (350, 352-353-bet) - birlamchi, ikkilamchi va uchlamchi navbat zanjiri, 10 daqiqalik tasdiq va eskalatsiya, oyda 4.5 hafta hisobi, kamida 5 va kamida 6 kishilik navbat, ikkilamchi bilan 10-12 kishi, kichik jamoalar navbatini birlashtirish, navbatchi haftasini rejalashtirishning to'rt varianti
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 15-bob (215-bet) - pre-mortem mashqi: rollout barbod bo'lsa sabablari nima bo'lishi mumkinligini sanash, ssenariylarni xaritaga tushirish, har biri uchun aniqlash va to'sish usulini topish
- ESLATMA: 35.2 dagi uch rolni ovoz chiqarib e'lon qilish va almashish davri, 35.3 dagi ma'lumot buzilishi xavfida trafikni avval to'xtatish, 35.6 dagi xabar yuborish ritmi va intervallar, 35.7 dagi majburiy nuqtalar to'plami, 35.8 dagi "nima yaxshi ishladi" bo'limi va hujjat muddati, 35.10 dagi tekshiruv usuli rekviziti, 35.11 dagi navbat kompensatsiyasi, runbook tarkibi va tungi uyg'otish chegarasi, 35.12 dagi chegara raqamlari shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 35.13 dagi to'ldirilgan post-mortem o'quv uchun o'ylab topilgan misol, haqiqiy incident hisoboti emas
- Michael T. Nygard, *Release It!*, 1-nashr, Pragmatic Bookshelf, 2007, 4-bob (45-bet) - yuqori interaktiv murakkablikda operatorning fikrlash modeli noto'g'ri bo'lishi va uning harakati yashirin bog'lanishni qo'zg'atishi

---

[&larr; 34. Legacy kod va bosqichma-bosqich refaktoring](34-legacy-kod-va-bosqichma-bosqich-refaktoring.md) · [Mundarija](README.md) · [36. Code review va jamoada texnik yetakchilik &rarr;](36-code-review-va-jamoada-texnik-yetakchilik.md)
