<!-- doc: architect | chapter: 5 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 5. Abstraksiya hissi, bog'liqlik va chegaralar (Abstraction, Coupling and Boundaries)

<details>
<summary>Bu bobdagi 23 bo'lim</summary>

- [5.1 Abstraksiya nima uchun qo'yiladi: o'zgarishni bitta joyga to'plash](#51-abstraksiya-nima-uchun-qoyiladi-ozgarishni-bitta-joyga-toplash)
- [5.2 Erta abstraksiya va takrorlanish: qaysi biri arzonroq](#52-erta-abstraksiya-va-takrorlanish-qaysi-biri-arzonroq)
- [5.3 Noto'g'ri abstraksiya narxi va undan qaytish yo'li](#53-notogri-abstraksiya-narxi-va-undan-qaytish-yoli)
- [5.4 Bog'liqlik turlari: ma'lumot, vaqt, joylashuv, sxema bo'yicha bog'liqlik](#54-bogliqlik-turlari-malumot-vaqt-joylashuv-sxema-boyicha-bogliqlik)
- [5.5 Koheziya: nima birga o'zgarsa, birga tursin](#55-koheziya-nima-birga-ozgarsa-birga-tursin)
- [5.6 Modul chegarasini qayerdan o'tkazish: o'zgarish tezligi va egalik bo'yicha](#56-modul-chegarasini-qayerdan-otkazish-ozgarish-tezligi-va-egalik-boyicha)
- [5.7 Interfeys kimga tegishli: foydalanuvchi tomonda e'lon qilish](#57-interfeys-kimga-tegishli-foydalanuvchi-tomonda-elon-qilish)
- [5.8 Bog'liqlik yo'nalishini boshqarish: ichki qatlam tashqarini bilmasin](#58-bogliqlik-yonalishini-boshqarish-ichki-qatlam-tashqarini-bilmasin)
- [5.9 Sxema chegarasi: boshqa servisning jadvaliga tegmaslik qoidasi](#59-sxema-chegarasi-boshqa-servisning-jadvaliga-tegmaslik-qoidasi)
- [5.10 Chegara noto'g'ri qo'yilganini bildiradigan belgilar](#510-chegara-notogri-qoyilganini-bildiradigan-belgilar)
- [5.11 Qisman chegara: to'liq chegara narxini keyinga qoldirish](#511-qisman-chegara-toliq-chegara-narxini-keyinga-qoldirish)
- [5.12 Biznes use case o'sishi va kengaytirish nuqtasi narxi](#512-biznes-use-case-osishi-va-kengaytirish-nuqtasi-narxi)
- [5.13 Ajratish rejimi: manba, deploy va servis darajasi](#513-ajratish-rejimi-manba-deploy-va-servis-darajasi)
- [5.14 Temporal dekompozitsiya: tartib bo'yicha bo'lish va uning qizil bayrog'i](#514-temporal-dekompozitsiya-tartib-boyicha-bolish-va-uning-qizil-bayrogi)
- [5.15 Yuqoridan pastga va pastdan yuqoriga: bog'liqlik grafi loyihalanmaydi, o'sadi](#515-yuqoridan-pastga-va-pastdan-yuqoriga-bogliqlik-grafi-loyihalanmaydi-osadi)
- [5.16 Umumiy egalik: ko'p servis yozadigan jadvalga yagona ega](#516-umumiy-egalik-kop-servis-yozadigan-jadvalga-yagona-ega)
- [5.17 Birgalikda egalik: bitta jadvalga ikki yozuvchi va to'rt yechim](#517-birgalikda-egalik-bitta-jadvalga-ikki-yozuvchi-va-tort-yechim)
- [5.18 Bazani bo'lish sabablari: oltita disintegrator va ikkita integrator](#518-bazani-bolish-sabablari-oltita-disintegrator-va-ikkita-integrator)
- [5.19 O'tkazuvchi bog'liqlik: pastdagi servis uchun uzatilgan ma'lumot](#519-otkazuvchi-bogliqlik-pastdagi-servis-uchun-uzatilgan-malumot)
- [5.20 Cheklov yo'naltiruvchi sifatida: foydasi va kiritish tartibi](#520-cheklov-yonaltiruvchi-sifatida-foydasi-va-kiritish-tartibi)
- [5.21 Har darajada hikoya: ierarxiya, element soni va domen otlari](#521-har-darajada-hikoya-ierarxiya-element-soni-va-domen-otlari)
- [5.22 Dekompozitsiya strategiyasini ongli tanlash: katalog va ADD](#522-dekompozitsiya-strategiyasini-ongli-tanlash-katalog-va-add)
- [5.23 Amalda qo'llash](#523-amalda-qollash)

</details>



Abstraksiya hissi deganda chiroyli ierarxiya qurish qobiliyati emas, o'zgarish qayerdan kelishini oldindan sezish tushuniladi. Arxitektor har bir interfeysni savol bilan qo'yadi: "ertaga nima o'zgaradi va o'zgarish qancha faylga tegadi?". Agar javob yo'q bo'lsa, abstraksiya hali kerak emas. Bu bobda abstraksiyaning iqtisodi, bog'liqlik mexanikasi va chegarani qayerdan o'tkazish qarori ko'rib chiqiladi. Chuqur va yuzaki modul, ma'lumotni yashirish va murakkablikni pastga tortish mavzularining to'liq yozuvi [architect 6](06-murakkablikni-boshqarish.md#68-servislar-soni-va-operatsion-murakkablik-narxi) da; bu bob ularga tayanadi, lekin takrorlamaydi.

## 5.1 Abstraksiya nima uchun qo'yiladi: o'zgarishni bitta joyga to'plash

Abstraksiyaning ta'rifi Ousterhout da aniq: abstraksiya - obyektning soddalashtirilgan ko'rinishi, undan muhim bo'lmagan tafsilotlar olib tashlangan. Ta'rifdagi kalit so'z "muhim bo'lmagan", chunki abstraksiya ikki tomonga buzilishi mumkin: muhim bo'lmagan tafsilotni ichiga olsa, kerakmas murakkablik qo'shadi; muhim tafsilotni tashlab yuborsa, yolg'on abstraksiya bo'lib qoladi, ya'ni oddiy ko'rinadi, lekin aslida oddiy emas. Shundan kelib chiqadigan amaliy vazifa bitta: o'zgarish radiusini qisqartirish. Agar QQS stavkasi o'zgarganda o'nlab faylni tahrirlash kerak bo'lsa, abstraksiya yo'q. Agar bitta sinfni tahrirlab, qolgan hamma joy to'g'ri ishlaydigan bo'lsa, abstraksiya ishlayapti. Shu sababli abstraksiyani "qayta ishlatish uchun" emas, "o'zgarishni ushlab turish uchun" qo'yish kerak.

Amalda bu ikki xil narsani ajratishdan boshlanadi: siyosat (policy) va mexanika. Bu ajratish *Clean Architecture* ning "siyosat va daraja" bobidan keladi: tizim o'zgarish sabablariga qarab siyosatlarga bo'linadi, va bir xil sababdan bir vaqtda o'zgaradigan siyosatlar birga turadi. To'lov summasini hisoblash siyosat, HTTP orqali provayderga murojaat qilish mexanika. Siyosat biznes talabi bilan o'zgaradi, mexanika texnologiya bilan o'zgaradi. Ikkisi bir sinfda yashasa, har bir biznes o'zgarishi texnik kodga tegib ketadi.

```java
// Siyosat bitta joyda: narx qanday hisoblanadi.
// Mexanika (provayder, retry, timeout) bu sinfga umuman kirmaydi.
public final class OrderPricing {

    private final TaxPolicy taxPolicy;      // stavka o'zgarsa faqat shu implementatsiya o'zgaradi
    private final DiscountPolicy discounts; // aksiya qoidalari alohida evolyutsiya qiladi

    public Money total(OrderDraft draft) {
        Money net = draft.lines().stream()
                .map(line -> line.unitPrice().multiply(line.quantity()))
                .reduce(Money.ZERO, Money::add);
        Money afterDiscount = discounts.apply(draft.customerTier(), net);
        return afterDiscount.add(taxPolicy.taxFor(draft.region(), afterDiscount));
    }
}
```

Diqqat qiling: bu yerda `OrderPricing` uchun interfeys yaratilmadi. Narx hisoblashning bitta to'g'ri usuli bor, demak unda almashtiriladigan nuqta yo'q. Almashtiriladigan nuqtalar `TaxPolicy` va `DiscountPolicy`, chunki aynan shu ikkisi mintaqa va aksiya bo'yicha turlanadi. Abstraksiyani turlanish bor joyga qo'yish kerak, turlanish yo'q joyga emas.

Bu evristikaning kitobdagi nomi bor va u review da ishlatishga qulay. *Code Complete* uni "markaziy boshqaruv nuqtalarini yarat" (make central points of control) deb ataydi va P.J. Plauger ning "Bitta To'g'ri Joy printsipi" ga tayanadi: har qanday jiddiy kod bo'lagini izlash uchun bitta to'g'ri joy, va ehtimolli o'zgarishni kiritish uchun bitta to'g'ri joy bo'lishi kerak. Kitob markazlashtirish shakllarini ham sanaydi: sinf, rutina, `#include` fayli va hatto nomlangan konstanta ham markaziy boshqaruv nuqtasi bo'la oladi. Foyda bitta va o'lchanadigan: bir narsani qancha kam joydan qidirsangiz, uni o'zgartirish shuncha oson va xavfsiz. Spring da bu savol odatda shunday keladi: QQS stavkasi `application.yml` da, `TaxPolicy` da, migratsiya skriptida va test fixture ida, ya'ni to'rt joyda yozilgan bo'lsa, markaziy nuqta yo'q va keyingi stavka o'zgarishi to'rt pull request ga aylanadi.

## 5.2 Erta abstraksiya va takrorlanish: qaysi biri arzonroq

Ikki xato bir xil og'ir emas. Takrorlangan kodni birlashtirish mexanik ish: IDE refaktoringi bilan bajariladi va natijasi testlar bilan tekshiriladi. Noto'g'ri abstraksiyani yechish esa chaqiruvchilar zanjirini buzadi, chunki hamma allaqachon o'sha interfeysga suyangan. Shuning uchun amaliy qoida: shubha bo'lsa takrorlashni tanla.

Takrorlanishning o'zi ham bir xil emas, va ajratish mezoni *Clean Architecture* ning Umumiy Yopilish Printsipidan (Common Closure Principle) chiqadi: bir xil sabablardan va bir vaqtda o'zgaradigan sinflar bitta komponentga yig'iladi, boshqa vaqtda va boshqa sabablardan o'zgaradiganlari esa ajratiladi. Demak tekshirish savoli kodning o'xshashligi emas, o'zgarish sababi: "bu ikki joy bir xil sababdan va bir vaqtda o'zgaradimi?". Javob "yo'q" bo'lsa, kod hozir o'xshash bo'lsa ham qo'shilmaydi. Javob "ha" bo'lsa, ya'ni bitta biznes qoidasi ikki joyda yozilgan bo'lsa, birlashtirmaslik xatolikka olib keladi; Ousterhout da bunday takrorlanish alohida qizil bayroq - bir xil kod qayta-qayta uchrasa, to'g'ri abstraksiya hali topilmagan.

Ikki variant orasida tanlashning ikkinchi o'qi ham shu kitobdan keladi va u "hozir kerakmi" savolidan mustaqil. Fowler dizayn variantini tanlashda refaktoringni oldindan tasavvur qilishni maslahat beradi: bir dizayndan ikkinchisiga keyin o'tish oson bo'lsa eng soddasini oling, oson bo'lmasa dizaynga hozir ko'proq kuch sarflang (Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 2-bob, 57-bet). Mezoni arzon, chunki u hech qanday o'lchov talab qilmaydi: "bu qarorni teskari qilish uchun qancha fayl va qancha chaqiruvchi o'zgaradi" degan savolga javob bir necha daqiqada topiladi. Natija esa yuqoridagi qoidaga ziddiyatsiz qo'shiladi: takrorlash arzon bo'lgani uchun soddani olasiz, lekin keyin o'tish qimmat bo'lgan joyda (tranzaksiya chegarasi, wire formati, ID strategiyasi) soddalik yetarli dalil emas. Shu ikkinchi guruhning to'liq ro'yxati [qaytarib bo'lmaydigan qarorlar](01-arxitektorning-fikrlash-modeli.md#15-qaytarib-boladigan-va-qaytarib-bolmaydigan-qarorlar) bo'limida.

Sanoq bo'yicha chegara ham bor va u o'ylab topilgan emas: Fowler *Refactoring* da buni "uchlik qoidasi" deb ataydi (qoidani unga Don Roberts bergan) - birinchi marta shunchaki qilasiz, ikkinchi marta takrorlanishdan noqulay bo'lsangiz ham takrorlaysiz, uchinchi marta refaktoring qilasiz. Ousterhout boshqa tomondan chegara qo'yadi: yangi modulni "birmuncha umumiy" qilish kerak, ya'ni funksionallik hozirgi ehtiyojni aks ettirsin, lekin interfeys unga qotib qolmasin, va "birmuncha" so'zi muhim - juda umumiy qilib qo'yilgan narsa hozirgi ehtiyoj uchun noqulay bo'ladi. Spring loyihalarida yana bitta signal bor: agar bir xil `@Transactional` + repository + mapping ketma-ketligi uch xil servisda takrorlansa, u yerda yashirin domen amali turgan bo'ladi.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Ikki joyda o'xshash kod ko'rindi | Darhol umumiy `BaseService` chiqariladi | O'zgarish sababi bir xilmi, shu tekshiriladi |
| Yangi provayder qo'shilishi mumkin | Har bir servisga interfeys yoziladi | Interfeys faqat ikkinchi haqiqiy provayder kelganda chiqariladi |
| Har bir entity uchun repository | Jenerik `CrudService<T>` qatlami | Faqat haqiqiy domen amallari e'lon qilinadi |
| DTO va entity bir xil ko'rinadi | Entity to'g'ridan to'g'ri API ga chiqariladi | API shartnomasi alohida turadi, ichki model erkin o'zgaradi |
| Ikki modulga umumiy kod kerak | `common` moduli yaratiladi va o'sadi | Faqat o'zgarmas tiplar (`Money`, `OrderId`) umumiylashtiriladi (CRP: iste'molchini kerak bo'lmagan narsaga bog'lamaslik) |
| Bitta metodda ikki xatti-harakat | `boolean` flag parametri qo'shiladi | Ikki alohida metod yoki ikki implementatsiya |
| Modullar o'rtasida ma'lumot kerak | Boshqa modul jadvaliga `join` qilinadi | Event yoki aniq API orqali olinadi |
| Interfeys o'zgarishi kerak | Interfeysga yangi metod qo'shiladi | Avval kim foydalanayotgani va kim egasi aniqlanadi |
| Chegara noqulaylik keltiryapti | Chegara olib tashlanadi | Chegara joyi noto'g'ri qo'yilgani tekshiriladi |

## 5.3 Noto'g'ri abstraksiya narxi va undan qaytish yo'li

Noto'g'ri abstraksiya o'zini bitta belgi bilan oshkor qiladi: yangi talab kelganda interfeysga parametr qo'shiladi. Keyin ikkinchi parametr, keyin `Map<String, Object> options`. Ousterhout bu belgini aniq nomlaydi: metod sonini kamaytirish uchun ko'p qo'shimcha argument kiritish kerak bo'lsa, siz hech narsani soddalashtirmagan bo'lasiz; va interfeysi o'z mazmuniga nisbatan murakkab bo'lgan modul yuzaki modul deb ataladi, ya'ni u murakkablikka qarshi kurashda yordam bermaydi. `boolean` flag parametri alohida holat: *Clean Code* uni to'g'ridan to'g'ri yomon amaliyot deb ataydi, chunki u metodning bir nechta ish qilayotganini oshkor qiladi. Shu paytdan boshlab abstraksiya mantiqni yashirmaydi, balki chaqiruvchidan mantiqni bilishni talab qiladi. Chaqiruvchi `if` yozib qaysi parametrni berishni tanlay boshlaydi, demak qaror chegaradan tashqariga chiqib ketgan - Ousterhout atamasi bilan bu yolg'on abstraksiya.

```java
// Noto'g'ri abstraksiya: bitta metod uch xil ishni bajarmoqchi.
public interface ReportService {
    // includeDraft, groupByWarehouse, currency - bular chaqiruvchining qarori bo'lib qoldi
    Report build(LocalDate from, LocalDate to,
                 boolean includeDraft, boolean groupByWarehouse, String currency);
}

// Qaytish yo'li: har bir haqiqiy foydalanish holati o'z nomini oladi.
public interface StockReports {
    WarehouseStockReport dailyStockByWarehouse(LocalDate day);
}

public interface SalesReports {
    SalesReport monthlySales(YearMonth month, Currency currency);
}
```

Qaytish ketma-ketligi quyidagicha ishlaydi. Birinchi qadam: abstraksiyani olib tashlamasdan, chaqiruvchilarni ikki guruhga bo'lib, har biriga yangi aniq metod beriladi. Ikkinchi qadam: eski metod `@Deprecated` qilinadi va chaqiruvchilar bittalab yangi metodga ko'chiriladi. Uchinchi qadam: eski metod o'chiriladi. Bu "inline qilib, keyin to'g'ri joyda qayta ajratish" usuli, va u katta refaktoringdan ko'ra xavfsiz, chunki har bir qadam alohida deploy qilinadi.

Narxni baholash uchun bitta o'lchov yetarli: noto'g'ri abstraksiyaga suyangan chaqiruvchilar soni va ular necha jamoaga tarqalgani. Bir jamoa ichidagi bir nechta chaqiruvchi oddiy refaktoring, bir necha jamoaga tarqalgan chaqiruvchilar esa kelishilgan migratsiya rejasi. Sababi *Clean Architecture* da aytilgan: komponentga bog'langan har bir iste'molchi o'zgarishda qayta tekshirish va qayta deploy talab qiladi. Shuning uchun abstraksiyani jamoalar o'rtasidagi chegarada qo'yishdan oldin ikki marta o'ylash kerak.

## 5.4 Bog'liqlik turlari: ma'lumot, vaqt, joylashuv, sxema bo'yicha bog'liqlik

"Coupling" degan so'z juda umumiy, shuning uchun kitoblar uni ikkita o'q bo'yicha ajratadi. Birinchi o'q *Software Architecture: The Hard Parts* dan: statik bog'liqlik - qismlar bir-biriga qanday ulanib turgani, ya'ni ishga tushish uchun kerak bo'lgan shartnomalar, kutubxonalar va baza; dinamik bog'liqlik - ular ish vaqtida bir-birini qanday chaqirishi, sinxron yoki asinxron. Kitobning qisqa formulasi: statik bog'liqlik operatsion bog'liqlikni, dinamik bog'liqlik esa aloqa bog'liqligini tahlil qiladi.

Ikkinchi o'q kod darajasida va uning rasmiy taksonomiyasi bor. *Fundamentals of Software Architecture* Meilir Page-Jones ning 1996 yildagi connascence tushunchasini keltiradi: ikki komponent connascent bo'ladi, agar biridagi o'zgarish tizim to'g'riligini saqlash uchun ikkinchisini ham o'zgartirishni talab qilsa. Kitob turlarni ikki guruhga ajratadi. Statik connascence manba kodi darajasida: nom (CoN), tur (CoT), ma'no yoki kelishuv (CoM/CoC), joylashuv tartibi (CoP), algoritm (CoA). Dinamik connascence ish vaqtida: bajarilish tartibi, vaqt, qiymat va identlik bo'yicha connascence (kitob statik "tur" va dinamik "vaqt" uchun bir xil CoT qisqartmasini ishlatadi, shuning uchun bu yerda qisqartma emas, to'liq nom yozilgan). Ro'yxat kitobda to'liq keltirilgan, shuning uchun bog'liqlikni muhokama qilganda shu atamalardan foydalanish aniqroq: "bu modullar sehrli son orqali ma'no bo'yicha bog'langan" degan gap "ular qattiq bog'langan" degandan ko'p ma'lumot beradi.

Quyidagi jadval shu ikki o'qni Spring loyihasida uchraydigan to'rtta amaliy holatga bog'laydi. Jadvaldagi guruhlash shu korpusning ishchi tasnifi, kitobdagi taksonomiyaning o'zi emas: o'ng ustunda har bir holat qaysi kitob atamasiga tushishi ko'rsatilgan.

| Amaliy holat | Qanday aniqlanadi | Qanday yumshatiladi | Kitob atamasi |
| --- | --- | --- | --- |
| Ma'lumot shakli | Chaqiruvchi o'ziga kerak bo'lmagan maydonlari bor tipni import qiladi | Chegarada faqat kerakli maydonlardan iborat o'z tipi | Statik: tur va nom bo'yicha connascence; ISP ning buzilishi |
| Vaqt | Sinxron zanjir bir necha servisdan o'tadi, javob kutiladi | Event yoki outbox, kutish shart bo'lsa timeout va fallback | Dinamik bog'liqlik: sinxron aloqa |
| Joylashuv | URL va port kodda yozilgan | Config, discovery, abstraksiyalangan client | Statik bog'liqlik: operatsion bog'liqlik |
| Sxema egaligi | Ikki servis bitta jadvalga yozadi | Egalik bitta servisga, qolganlarga API yoki view | Birgalikda egalik (joint ownership) |
| O'tkazuvchi ma'lumot | Shartnomada chaqiruvchi o'zi o'qimaydigan, faqat pastdagi servisga keraklik maydon turadi | Oraliq servis o'z tilida so'rab, pastdagi shartnomani o'zi yasaydi | O'tkazuvchi bog'liqlik (pass-through coupling) |

Ikki holat alohida izoh talab qiladi. Ma'lumot shakli bo'yicha bog'liqlikning narxini *Clean Architecture* ning interfeys ajratish bobi bitta gapda aytadi: sizga kerak bo'lmagan yukni ko'tarib yurgan narsaga bog'lanish kutilmagan muammo keltiradi, chunki o'sha keraksiz qismdagi o'zgarish ham sizni qayta deploy qilishga majbur qiladi. Sxema bo'yicha bog'liqlik esa eng og'iri: ikki servis bitta jadvalga yozsa, hech qanday kod refaktoringi yordam bermaydi, chunki bog'liqlik ma'lumotlar bazasi darajasida (yechimi 5.9 da). O'tkazuvchi bog'liqlikning o'z yozuvi [o'tkazuvchi bog'liqlik](#519-otkazuvchi-bogliqlik-pastdagi-servis-uchun-uzatilgan-malumot) bo'limida.

Taksonomiya ro'yxat bo'lib qolmasligi uchun *Fundamentals of Software Architecture* connascence ga uch xossa va uchta qoida qo'shadi. Xossalar bitta bahsni tugatadi: "bu yomon bog'liqlikmi" degan savol kontekstdan ajralib javob bermaydi.

- **Kuch (strength).** Connascence kuchi uni refaktoring qilish qanchalik osonligi bilan o'lchanadi, ya'ni turlar o'zaro teng emas va bir turdan boshqasiga ongli o'tish mumkin. Kitobning aniq tavsiyasi: statik connascence ni dinamikdan afzal ko'r, chunki statikni oddiy manba kodi tahlili topadi va zamonaviy asboblar uni yaxshilashni arzonlashtiradi. Amaliy harakat ham nomlangan: ma'no bo'yicha connascence ni nom bo'yicha connascence ga aylantirish, ya'ni sehrli qiymat o'rniga nomlangan konstanta qo'yish.
- **Yaqinlik (locality).** Bir xil shakl ikki sinf bitta komponentda bo'lsa, ikki alohida komponentda bo'lganidan kam zarar qiladi. Shuning uchun kuch va yaqinlik birga baholanadi: modul ichidagi kuchli shakl modullar orasiga tarqalgan o'sha shakldan kichik hid.
- **Daraja (degree).** Ta'sir bir nechta sinfgami yoki ko'piga: kichik daraja kam zarar beradi. Kitobning ogohlantirishi shu yerda: kod bazasi o'sishga moyil, shuning uchun bugun kichik ko'ringan muammo mutanosib ravishda kattalashadi.

Page-Jones ning modullilikni yaxshilash uchun bergan uch qoidasi shu xossalardan chiqadi va ular aynan chegara haqida: tizimni inkapsulyatsiyalangan elementlarga bo'lib umumiy connascence ni kamaytir; inkapsulyatsiya chegarasini kesib o'tadigan connascence ni minimallashtir; chegara ichidagi connascence ni maksimallashtir. Uchinchi qoida ko'pincha noto'g'ri o'qiladi: modul ichida qattiq bog'lanish ayb emas, maqsad ham shu, faqat u chegaradan chiqmasin.

Servis darajasida bir belgi alohida ahamiyatli. Newman domen bog'liqligini (bir servis boshqasining funksionalligiga muhtoj bo'lishi) yengil shakl deb hisoblaydi va mikroservis arxitekturasida uni deyarli muqarrar deb ataydi, lekin minimumda ushlashni aytadi. Ogohlantirish aniq: bitta servis bir nechta quyi servisga bog'langan bo'lsa, bu o'sha servis juda ko'p ish qilayotgani yoki mantiq bir joyga markazlashib ketganiga ishora. Ya'ni uzun chaqiruv zanjiri ([5.10](#510-chegara-notogri-qoyilganini-bildiradigan-belgilar)) bilan bir qatorda tarmoqlanish kengligi ham chegara xatosining ko'rsatkichi.

## 5.5 Koheziya: nima birga o'zgarsa, birga tursin

Koheziya bog'liqlikning teskari tomoni emas, uning sherigi. *Fundamentals of Software Architecture* koheziyani "modul qismlari bir-biriga qanchalik bog'liq" sifatida ta'riflaydi va uning darajalarini eng yaxshisidan eng yomoniga sanab beradi: funksional, ketma-ket, kommunikatsion, protsedural, vaqtga bog'liq, mantiqiy va tasodifiy koheziya. Kitob shu yerda halol ogohlantirish beradi: koheziya bog'liqlikka qaraganda kamroq aniq o'lchov, va modulning koheziya darajasini baholash ko'p holda arxitektorning qaroriga qoladi. Shu sababli amalda ishlaydigan mezon *Clean Architecture* ning Umumiy Yopilish Printsipi bo'ladi: bitta sababdan va bitta vaqtda o'zgaradigan kod bitta joyda turadi. Spring loyihalarida eng keng tarqalgan xato texnik qatlamlar bo'yicha paketlash: `controller`, `service`, `repository`, `dto`. Bu ko'rinishda chiroyli, lekin har bir biznes o'zgarishi to'rt paketga tegadi, demak koheziya past. Mantiqiy koheziyaning kanonik misoli ham shu kitobda bor va u Java dasturchisiga tanish: `StringUtils` kabi paket, ya'ni bir tipda ishlaydigan, lekin bir-biriga aloqasi yo'q statik metodlar to'plami.

Koheziya subyektiv bo'lgani uchun kitob qarorni uchta savolga aylantiradi va misolni ham beradi: `Customer Maintenance` moduli `add customer`, `update customer`, `get customer`, `notify customer` bilan birga `get customer orders` va `cancel customer orders` ni ham ushlab turadi, ya'ni oxirgi ikkitasini alohida `Order Maintenance` ga chiqarish kerakmi degan savol tug'iladi. Javob uch savoldan chiqadi.

- Ikkinchi modulda **faqat shu ikki amal** bo'ladimi? Shunday bo'lsa, ularni birinchi modulga qaytarib yig'ish mantiqli: ikki metodli modul chegara emas.
- Birinchi modul **ancha kattalashishi** kutiladimi? Kutilsa, bu dasturchini xatti-harakatni ajratish imkoniyatini qidirishga undaydi, ya'ni ajratish foydasi o'sadi.
- Ajratilgan ikkinchi modul birinchisi haqida **shunchalik ko'p bilim** talab qiladimi, ishlashi uchun kuchli bog'lanish kerak bo'lib qolsinmi? Kerak bo'lsa, ajratish koheziyani emas, bog'liqlikni oshiradi.

Uchinchi savol eng muhimi, chunki u ikki o'lchovni bir qarorda uchrashtiradi: chegara koheziyani oshirsa ham, chegaradan o'tadigan bilim hajmi oshsa, umumiy natija yomonlashadi.

Strukturaviy tomonda bitta metrika yordam beradi. *Fundamentals of Software Architecture* Chidamber va Kemerer to'plamidagi LCOM (Lack of Cohesion in Methods) metrikasini keltiradi; kitobning tushunarli ta'rifi formula emas, bitta jumla: maydonlarni bo'lishish orqali bog'lanmagan metod to'plamlari yig'indisi. Amalda bu shunday ko'rinadi: sinfda `a` va `b` maydonlari bor, metodlarning bir qismi faqat `a` ga, qolgani faqat `b` ga tegadi, demak LCOM yuqori va sinf ikkiga bo'linsa xatti-harakat umuman o'zgarmaydi. Kitob metrikaning foydasini aniq joyga qo'yadi: bir arxitektura uslubidan boshqasiga o'tayotgan arxitektor uchun umumiy utility sinflari eng ko'p bosh og'rig'i beradi, va LCOM aynan tasodifiy bog'langan, boshidan bitta sinf bo'lmasligi kerak bo'lgan sinflarni topadi. Cheklov ham shu yerda yozilgan: LCOM faqat strukturaviy koheziya yo'qligini ko'radi, bo'laklar mantiqan birga turishi kerakmi degan savolga javob bera olmaydi. Shuning uchun uni yuqoridagi uch savolning o'rniga emas, ularga nomzod topuvchi sifatida ishlatish kerak.

Alternativa: xususiyat bo'yicha paketlash. `order`, `payment`, `inventory`, `reporting`. Har birining ichida o'z controller, servis va repository turadi. Bunda "buyurtmani bekor qilish" talabi bitta paket ichida bajariladi. Qo'shimcha foyda: paket darajasida ko'rinishni cheklash mumkin bo'ladi, chunki sinflarning ko'pchiligi `public` bo'lishi shart emas.

```java
// com/shop/order/OrderCancellation.java
// Paket-private: modul tashqarisidan ko'rinmaydi, demak chegara kod bilan himoyalangan.
class OrderCancellation {

    private final OrderRepository orders;
    private final ApplicationEventPublisher events;

    @Transactional
    void cancel(OrderId id, CancelReason reason) {
        Order order = orders.findForUpdate(id)      // SELECT ... FOR UPDATE
                .orElseThrow(() -> new OrderNotFound(id));
        order.cancel(reason);                        // qoida entity ichida
        orders.save(order);
        // Tashqi modullar faqat shu event'ni ko'radi, Order ni ko'rmaydi.
        events.publishEvent(new OrderCancelled(id, order.customerId(), reason));
    }
}
```

Bu yerda muhim mexanika bor: `ApplicationEventPublisher` bilan chiqarilgan event `@TransactionalEventListener` orqali commit dan keyin ishlanishi mumkin. Shunda inventar moduli buyurtma tranzaksiyasini uzaytirmaydi. Agar event tashqi tizimga chiqishi kerak bo'lsa, u holda bazaga yozib, keyin yuboradigan yondashuv kerak bo'ladi, bu dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern.

## 5.6 Modul chegarasini qayerdan o'tkazish: o'zgarish tezligi va egalik bo'yicha

Chegarani domen diagrammasidan emas, ikki o'lchovdan chiqarish kerak: nima qanchalik tez o'zgaradi va kim javobgar. Birinchi o'lchovning kitobdagi nomi bor: *Software Architecture: The Hard Parts* uni "kod o'zgarish tezligi" (code volatility) deb ataydi va bunday ajratishni "o'zgarish tezligiga asoslangan dekompozitsiya" deb nomlaydi. Kitobdagi misol aynan shu holat: xabar yuborish servisida SMS va email qismi yarim yilda bir o'zgaradi, pochta xati qismi esa har hafta, va shu farq servisni ikkiga bo'lish uchun yetarli asos bo'ladi, chunki aks holda har haftalik o'zgarish butun servisni qayta test qilish va qayta deploy qilishga majbur qiladi. Ikkinchi o'lchov, ya'ni bir xil sababdan o'zgaradigan kodni birga ushlash, *Clean Architecture* ning Umumiy Yopilish Printsipi.

O'zgarish tezligini taxmin qilish shart emas: *The Hard Parts* uni o'lchashni ham aytadi va manbani ko'rsatadi - har qanday versiya nazorati tizimining standart imkoniyatlari. Bu arxitektor uchun eng arzon ma'lumot manbai.

```bash
# Oxirgi 6 oyda qaysi paketlar eng ko'p o'zgargan: chegara nomzodlari shu yerda.
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '^src/main/java' \
  | awk -F/ '{print $4"/"$5"/"$6}' \
  | sort | uniq -c | sort -rn | head -20

# Birga o'zgaradigan fayllar juftligi: yuqori son yashirin koheziyani ko'rsatadi.
git log --since="6 months ago" --name-only --pretty=format:%H \
  | awk 'NF==0{next} /^[0-9a-f]{40}$/{c=$0; next} {print c" "$0}' \
  | sort | head -5
```

Birinchi buyruq o'zgarish zichligini beradi. Ikkinchisi birga o'zgaradigan fayllarni ko'rsatadi, va agar ikki alohida modul fayllari doim birga o'zgarsa, chegara noto'g'ri joydan o'tgan. Egalik o'lchovi ham shu tarixdan chiqadi: bitta paketga 4 xil jamoa commit qilayotgan bo'lsa, u paket chegara emas, umumiy maydon.

Yana bitta tuzatish kerak: chegara bitta chiziq emas. *Clean Architecture* ning "qatlamlar va chegaralar" bobi buni sodda o'yin misolida ko'rsatadi. Boshida ma'lumot oqimi ikkiga bo'linadi, bir tomoni foydalanuvchi bilan muloqot, ikkinchi tomoni saqlash, va ikkisi yuqorida o'yin qoidalarida uchrashadi. Tarmoq komponenti qo'shilsa oqim uchga bo'linadi, va kitob shu yerda "oqimlar bir-birini kesib o'tadi" degan xulosaga keladi: tizim murakkablashgani sayin komponent tuzilishi bir nechta bunday oqimga bo'linib ketadi. Keyin oqimlarning o'zi ham bo'linadi: o'yin qoidalari ichida xarita mexanikasi va o'yinchi holatini boshqarish ikki xil darajadagi siyosat bo'lib chiqadi, va ikkisi o'rtasida yana to'laqonli chegara paydo bo'ladi. Amaliy natija: "chegara qatlamlar o'rtasida o'tadi" degan tasvir yetarli emas, chegaralar bir necha o'lchovda bir vaqtda turadi. Shuning uchun qaror bir martalik ham emas; kitobning o'z formulasi shunday - arxitektor tizim o'sishini kuzatib turadi va chegarani aynan egilish nuqtasida qo'yadi, ya'ni uni qurish narxi uni qo'ymaslik narxidan arzonlashgan paytda.

Chegara faqat modul yoki servis atrofida bo'lishi shart emas. Newman servis chegarasidan yirikroq birlikni ham chegara deb belgilashni tavsiya qiladi: masalan marketing jamoasining mas'uliyatiga tushadigan servislar guruhi bitta zona bo'ladi. Zona ichida kelishilgan tashqi xulq saqlansa, istalgan o'zgarish erkin kiritiladi; zonalar orasidagi o'zaro ta'sirni o'zgartirish esa ancha qimmat, chunki unda boshqa jamoalar bilan muvofiqlashish bor. Bu axborotni yashirishni servis darajasidan jamoa darajasiga ko'taradi va natijasi team API deb ataladi. Zonani qayerdan o'tkazish uchun arzon ko'rsatkich bor: jamoa tuzilmasi qiyin o'zgaradigan narsalar qatoriga kiradi, shuning uchun mavjud jamoa chegarasi zona nomzodini o'zi ko'rsatib turadi. Jamoa va arxitektura munosabatining to'liq yozuvi [36-bobda](36-code-review-va-jamoada-texnik-yetakchilik.md).

Shu o'rinda bitta keng tarqalgan xatoni to'g'rilash kerak: chegarani qayta foydalanish maqsadida qo'yish. *The Hard Parts* ning formulasi qisqa: qayta foydalanish abstraksiyadan keladi, lekin uni ishga soladigan narsa o'zgarish tezligining pastligi. Operatsion tizim va tashqi ochiq kutubxonalar yaxshi bog'lanish nishoni, chunki ularning o'zgarish tezligi va yangilanish ritmi ma'lum; ichki domen qobiliyati yoki tez o'zgaradigan texnik freymvork esa yomon nishon. Kitobning misoli to'g'ridan to'g'ri shu bobga tegishli: kompaniyadagi hamma bo'limning mijoz haqidagi qarashini bitta markaziy `Customer` servisiga yig'ish mantiqli ko'rinadi, lekin natija ikki tomondan buziladi. Birinchisi, yagona joyda turgan entity har qanday domen va ssenariyni ko'tarishi uchun shunchalik murakkab bo'lishi kerak, oqibatda oddiy ish uchun ham noqulay bo'ladi. Ikkinchisi, u arxitekturani mo'rt qiladi: `CustomerService` bitta domen uchun yangi qobiliyat qo'shsa, o'zgarish qolgan hamma domenga urilib, muvofiqlashish va qayta testlash talab qiladi. Ya'ni "mijoz bitta bo'lsin" degan mezon chegara mezoni emas; mezon avvalgidek o'zgarish tezligi va egalik bo'lib qoladi.

## 5.7 Interfeys kimga tegishli: foydalanuvchi tomonda e'lon qilish

Klassik xato: interfeys implementatsiya bilan bir paketda turadi. Bunda interfeys "men nimani taklif qilaman" degan ma'noni beradi. To'g'ri yondashuv teskari: interfeysni muhtoj tomon e'lon qiladi va unda "menga nima kerak" yoziladi. Shunda interfeys ehtiyoj bilan o'zgaradi, provayder bilan emas. Buning ortida ikki printsip turadi va ikkisi ham *Clean Architecture* da yozilgan: bog'liqlikni teskari aylantirish printsipi (DIP) manba kodidagi bog'liqlik faqat abstraksiyalarga ishora qilishini talab qiladi va "o'zgaruvchan konkret sinfga bog'lanmang" degan aniq amaliy qoidani beradi; interfeys ajratish printsipi (ISP) esa iste'molchini o'ziga kerak bo'lmagan narsaga bog'lamaslikni aytadi. Printsiplarning to'liq yozuvi [patterns 26](../patterns/26-dizayn-printsiplari-solid-grasp-va-umumiy.md#261-yagona-javobgarlik-printsipi-single-responsibility-principle) da; bu yerda faqat ularning joylashuv natijasi muhim.

Farq amalda sezilarli. Agar `PaymentGateway` interfeysi to'lov adapteri paketida tursa, unda provayderning hamma imkoniyati paydo bo'ladi: `authorize`, `capture`, `void`, `partialRefund`, `tokenize`. Buyurtma moduliga esa faqat ikkitasi kerak. Interfeysni buyurtma tomonida e'lon qilsangiz, u ikki metod bilan qoladi va provayder almashganda buyurtma moduli umuman o'zgarmaydi.

```java
// com/shop/order/spi/PaymentAuthorizer.java
// Buyurtma moduli nimaga muhtoj ekanini o'zi aytadi. 2 metod, boshqa hech narsa.
public interface PaymentAuthorizer {
    AuthorizationResult authorize(OrderId orderId, Money amount, PaymentMethodRef method);
    void release(AuthorizationId authorizationId);   // bekor qilinganda bloklangan summani bo'shatish
}

// com/shop/payment/acme/AcmeAuthorizerAdapter.java
// Adapter tashqi paketda turadi va buyurtma modulining interfeysiga moslashadi.
@Component
class AcmeAuthorizerAdapter implements PaymentAuthorizer {

    private final RestClient acme;   // timeout: connect 1s, read 3s

    @Override
    public AuthorizationResult authorize(OrderId id, Money amount, PaymentMethodRef m) {
        AcmeAuthResponse res = acme.post()
                .uri("/v2/authorizations")
                .body(AcmeAuthRequest.of(id, amount, m))
                .retrieve()
                .body(AcmeAuthResponse.class);
        return AuthorizationResult.from(res);   // tashqi tip chegaradan o'tmaydi
    }
}
```

Bu joylashuvning yana bir foydasi bor: bog'liqlik yo'nalishi avtomatik to'g'ri bo'lib qoladi. `payment.acme` paketi `order.spi` paketini biladi, teskarisi yo'q. *Clean Architecture* buning sababini ham aytadi: interfeysga qilingan har bir o'zgarish implementatsiyani ham o'zgartiradi, lekin implementatsiyadagi o'zgarish interfeysni odatda o'zgartirmaydi, demak interfeys implementatsiyadan kamroq o'zgaradi va unga bog'lanish xavfsizroq. Spring konteyner `PaymentAuthorizer` ni inyeksiya qilganda implementatsiya qaysi paketda ekani ahamiyatsiz, chunki bog'lanish tip bo'yicha amalga oshadi.

Interfeys bilan birga ikkinchi, odatda unutiladigan narsa ham almashtiriladigan bo'lishi kerak: aloqa usulining o'zi. Fairbanks buni connector deb ataydi va savolni aniq qo'yadi: komponentni interfeysi bo'yicha almashtirish mumkin bo'lgani kabi, quvurni (pipe) event bus ga almashtirish ham mijozga tegmasligi kerak. Arxitektura modelida javob "ha", lekin kodga o'girilganda bu xossa yo'qoladi: komponentni amalga oshiradigan kod odatda interfeys e'lon qiladi va mijoz shu interfeysga tayanadi, connector ni amalga oshiradigan kod esa kamdan kam interfeys e'lon qiladi, natijada mijoz aniq implementatsiyaga bog'lanib qoladi, ya'ni o'zining event bus ga qo'yayotganini yoki masofaviy chaqiruv qilayotganini biladi. Kitob buni ongli tanlov deb qoldiradi: ba'zan mijozning masofaviy chaqiruv qilayotganini bilishi xato ishlovini yaxshilaydi. Lekin asosiy tavsiya boshqa yo'nalishda: bugun alohida turgan tizim ertaga kattaroq tizimga integratsiya qilinadi, shuning uchun komponentlar orasidagi aloqa uchun connector ni birinchi darajali va almashtiriladigan qilish arzon va unumli, hamda ishlashga sezilarli ta'sir qilmaydi. Komponent ichidagi aloqa bundan ta'sirlanmaydi, qoida faqat chegaradan o'tadigan aloqaga tegishli.

```java
// Buyurtma moduli xabarni qanday yuborishini bilmaydi: bu connector interfeysi.
public interface OrderEventPublisher {
    void publish(OrderCancelled event);
}

// Bugungi implementatsiya: Spring ning ichki event bus i.
@Component
class LocalOrderEventPublisher implements OrderEventPublisher {

    private final ApplicationEventPublisher delegate;

    @Override
    public void publish(OrderCancelled event) {
        delegate.publishEvent(event);
    }
}

// Ertaga Kafka ga o'tilsa faqat shu sinf qo'shiladi, buyurtma moduli o'zgarmaydi.
@Component
@Primary
class KafkaOrderEventPublisher implements OrderEventPublisher {

    private final KafkaTemplate<String, OrderCancelled> kafka;

    @Override
    public void publish(OrderCancelled event) {
        kafka.send("order.cancelled", event.orderId().value(), event);
    }
}
```

## 5.8 Bog'liqlik yo'nalishini boshqarish: ichki qatlam tashqarini bilmasin

Qatlamlar haqida gapirishning foydali usuli: import yo'nalishi. Mezon *Clean Architecture* dan keladi: manba kodidagi bog'liqlik faqat abstraksiyalarga ishora qilsin, va platformaning barqaror qismlari (masalan `java.lang`) bundan mustasno, chunki ular o'zgarmaydi; taqiq o'zgaruvchan konkret narsalarga bog'lanishga qo'yiladi. Domen kodida `jakarta.persistence`, `org.springframework.web` yoki `com.fasterxml.jackson` importlari paydo bo'lsa, chegara allaqachon buzilgan. Bu holat sekin-asta keladi: avval `@JsonIgnore` entity ga qo'yiladi, keyin `@Column` nomi API shartnomasiga ta'sir qiladi, va oxirida API ni o'zgartirish uchun migratsiya yozish kerak bo'ladi.

Bu qoidani sharhda yozib qo'yish yetarli emas, uni avtomatik tekshirish kerak. ArchUnit shu uchun mavjud va u [testing 14.2](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bo'limida batafsil ko'rsatilgan. Bu yerda faqat qoida shakli muhim.

```java
@AnalyzeClasses(packages = "com.shop", importOptions = ImportOption.DoNotIncludeTests.class)
class BoundaryRulesTest {

    @ArchTest
    static final ArchRule domen_web_ni_bilmaydi = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("..web..", "..api..", "org.springframework.web..");

    @ArchTest
    static final ArchRule modullar_bir_birining_ichiga_kirmaydi = slices()
            .matching("com.shop.(*)..")
            .should().notDependOnEachOther()
            .ignoreDependency(alwaysTrue(), resideInAPackage("com.shop.shared.."));
}
```

Yo'nalishni buzadigan eng ko'p uchraydigan sabab qulaylik. Developer hisobot uchun buyurtma entity sini to'g'ridan to'g'ri olmoqchi bo'ladi, chunki shunday qilish darhol ishlaydi, API orqali olish esa ancha ko'p ish talab qiladi. Arxitektorning ishi shu tanlovni arzonlashtirish: hisobot uchun aniq o'qish interfeysi va kerakli ma'lumotni beradigan proyeksiya oldindan tayyor bo'lsa, qoidani buzish ehtiyoji qolmaydi.

## 5.9 Sxema chegarasi: boshqa servisning jadvaliga tegmaslik qoidasi

Kod chegarasini ArchUnit saqlaydi, lekin ma'lumotlar bazasi chegarasini hech kim saqlamaydi. Egalik qoidasi *Software Architecture: The Hard Parts* da aniq yozilgan: jadvalga yozish amalini bajaradigan servis shu jadvalning egasi, va kitob darhol qo'shadi - bu oddiy qoida birgalikda egalik (bir necha servis bitta jadvalga yozadi) va umumiy egalik (ko'pchilik servis yozadi) holatlarida murakkablashadi. Agar ikki servis bitta `orders` jadvaliga yozsa, ularni mustaqil deploy qilish imkoni yo'q: ustun nomini o'zgartirish ikkinchi servisni sindiradi. Shuning uchun har bir modul yoki servis o'z jadvallarining yagona egasi bo'lishi kerak.

PostgreSQL da buni sxema va rol darajasida majburiy qilish mumkin. Bu eng ishonchli usul, chunki u niyatga emas, ruxsatga asoslanadi.

```sql
-- Har bir modul o'z sxemasida yashaydi.
CREATE SCHEMA order_svc AUTHORIZATION order_app;
CREATE SCHEMA billing_svc AUTHORIZATION billing_app;

-- Billing order_svc jadvallarini ko'rmaydi: ruxsat berilmagan.
REVOKE ALL ON SCHEMA order_svc FROM billing_app;

-- Kerakli ma'lumot faqat aniq shartnoma orqali chiqadi: tor view.
CREATE VIEW order_svc.order_billing_v AS
SELECT id AS order_id, customer_id, total_amount, currency, placed_at
FROM order_svc.orders
WHERE status IN ('PLACED', 'SHIPPED');

GRANT USAGE ON SCHEMA order_svc TO billing_app;
GRANT SELECT ON order_svc.order_billing_v TO billing_app;

-- search_path ni rolga biriktirib, tasodifiy jadval nomlanishini oldini olish.
ALTER ROLE billing_app SET search_path = billing_svc, public;
```

View bu yerda shartnoma rolini o'ynaydi. Ichki jadval tuzilishi o'zgarsa, view saqlanadi va billing hech narsani sezmaydi. Bu to'liq yechim emas, chunki baza darajasidagi sinxron o'qish baribir vaqt bo'yicha bog'liqlik qoldiradi, lekin bu "hamma hamma joyga `join` qiladi" holatidan ancha yaxshi.

Migratsiyalar ham egalik qoidasiga bo'ysunadi. Har bir servis faqat o'z sxemasiga migratsiya qiladi, va bu konfiguratsiyada aniq yozilishi kerak. *The Hard Parts* monolit bazani ajratish ketma-ketligini ham beradi va unda sxemani ajratish alohida qadam sifatida ulanishlarni ajratishdan oldin turadi: avval ma'lumot domenlarini aniqlash va jadvallarni ularga taqsimlash, keyin ulanishlarni ajratish, keyin sxemalarni alohida serverga ko'chirish.

```yaml
spring:
  flyway:
    enabled: true
    schemas: order_svc            # faqat o'z sxemasi
    default-schema: order_svc
    locations: classpath:db/migration/order
    baseline-on-migrate: false
  datasource:
    hikari:
      maximum-pool-size: 20       # misol hisob: 4 instance x 20 = 80, qolgani zaxira
      connection-timeout: 3000    # ms
  jpa:
    properties:
      hibernate:
        default_schema: order_svc
```

Pool o'lchami ham chegara masalasi. Har bir servis o'z pooliga ega bo'lishi kerak, chunki umumiy pool bir servisning sekin so'rovini boshqasining muammosiga aylantiradi. Yuqoridagi qiymatlar misol: instance soni va har biridagi pool ko'paytmasi serverning `max_connections` chegarasidan past bo'lishi va replikatsiya hamda admin ulanishlari uchun zaxira qoldirishi kerak (4.5 dagi hisob bilan bir xil mantiq). Pool to'lib qolsa `connection-timeout` cheksiz kutish o'rniga xato qaytaradi, va bu afzal. Bu paragrafdagi sozlash tavsiyasi shu korpusning amaliy qoidasi, yuqoridagi kitoblardan olingan emas.

Qoidaning yozilmagan tomoni ham bor: egasi bo'lmagan ma'lumotni **o'qish** kerak bo'lsa nima qilinadi. *The Hard Parts* bu uchun bir necha yo'lni ketma-ket sanaydi va umumiy sxemani (ma'lumot domeni) oxirgi yo'l qilib qo'yadi. Tartib shunday o'qiladi: servislararo chaqiruv ishonchlilik va kechikish sababli yaramasa, ustunni replikatsiya qilish ma'lumot izchilligi talabi sababli yaramasa, replikatsiyalangan kesh ma'lumot hajmi sababli yaramasa, qolgan yechim ikki servisning jadvallarini bitta umumiy sxemaga qo'yish bo'ladi.

Narxi aniq va u ikki tomonli. Foydasi: servislar bir-biridan butunlay ajraladi, mavjudlik va javob tezligi bog'liqligi yo'qoladi, ma'lumotni uzatish, replikatsiya qilish yoki sinxronlashtirish kerak emas, jadvallar orasida tashqi kalit cheklovi hamda view va trigger kabi baza vositalari ishlashda qoladi, va o'qish oddiy SQL `JOIN` ga aylanadi. Kamchiligi: jadval sxemasi shartnomaga aylanadi, chunki abstraksiya qatlami yo'q, demak domen ichidagi istalgan jadval tuzilishi o'zgarsa bir nechta servisni o'zgartirish kerak bo'lishi mumkin; bounded context kengayadi; va xavfsizlik riski paydo bo'ladi, chunki sxemaga ulangan servis undagi barcha ma'lumotga kirish huquqini oladi, holbuki ba'zi ma'lumotga uning kirishi kerak emas. Shuning uchun bu yo'lni tanlash chegarani qayta baholash sharti bilan boradi ([5.17](#517-birgalikda-egalik-bitta-jadvalga-ikki-yozuvchi-va-tort-yechim) dagi to'rt yechim jadvali shu qarorning kengaytirilgan shakli).

## 5.10 Chegara noto'g'ri qo'yilganini bildiradigan belgilar

Chegara to'g'ri yoki noto'g'ri ekanini nazariyadan emas, kundalik ishlashdan bilib olish mumkin. Quyidagi belgilar aniq va o'lchanadigan.

Birinchi belgi: bitta talab uchun ikki yoki uch repozitoriyga o'zgartirish kiritiladi va ularni birgalikda deploy qilish kerak. Bu "taqsimlangan monolit" ning klassik ko'rinishi. Ikkinchi belgi: pull request lar doim ikki jamoaning reviewi ni kutadi. Uchinchi belgi: integratsiya testlarisiz hech narsani ishonch bilan o'zgartirib bo'lmaydi, chunki mantiq chegaralar bo'ylab tarqalgan.

To'rtinchi belgi texnik: bitta API chaqiruvi ichida uzun sinxron zanjir bo'lsa. *Software Architecture: The Hard Parts* buni dinamik bog'liqlik deb ataydi va aloqa shaklini tanlash qaysi narsalarga ta'sir qilishini sanab beradi: sinxronlashtirish, xatoni qayta ishlash, tranzaksiyalilik, masshtablanish va ishlash tezligi. Zanjir uzunligining mavjudlik va kechikishga raqamli ta'siri [architect 6.8](06-murakkablikni-boshqarish.md#68-servislar-soni-va-operatsion-murakkablik-narxi) da hisoblangan. Beshinchi belgi: "shared" yoki "common" moduli loyihada eng tez o'sadigan modul bo'lsa. Shu kitob bu holatni ham tasvirlaydi: umumiy kutubxonani mayda bo'laklarga bo'lish o'zgarishni boshqarishni yaxshilaydi, lekin servislar va kutubxonalar orasidagi bog'liqlik matritsasi "taqsimlangan loyqa to'p", ya'ni ba'zilar taqsimlangan monolit deb ataydigan holatga aylanadi. Bu modul chegara emas, chegaradan qochish joyi.

| Tuzoq | Nimaga olib keladi | Yechim |
| --- | --- | --- |
| Entity ni API javobi sifatida qaytarish | Ustun nomini o'zgartirish API ni sindiradi | Alohida javob tipi va mapping |
| `common` moduliga hamma narsa tushadi | Har bir o'zgarish hamma modulni qayta qurishga majbur qiladi | Faqat o'zgarmas tiplar qoldiriladi |
| Boshqa servis jadvaliga `join` | Mustaqil deploy imkoni yo'qoladi | Egalik + view yoki API |
| Interfeys implementatsiya paketida | Provayder o'zgarishi iste'molchiga tegadi | Interfeys iste'molchi tomonida |
| Sinxron zanjir 4 servisdan o'tadi | p99 latency va mavjudlik buziladi | Asinxron qadamlar, timeout, fallback |
| Lazy loading chegaradan o'tib ketadi | Boshqa qatlamda `LazyInitializationException` | Chegarada to'liq yuklangan proyeksiya |
| Har modul uchun alohida `CrudService<T>` | Domen amallari nomsiz qoladi | Aniq nomli biznes metodlari |

Oxirgi va eng ishonchli tekshiruv savoli shunday: yangi developer bitta modulni o'qib, uning vazifasini boshqa modulga qaramay tushuntirib bera oladimi? Agar "buni tushunish uchun to'lov servisini ham ko'rish kerak" degan javob kelsa, chegara hali to'g'ri joyda emas.

## 5.11 Qisman chegara: to'liq chegara narxini keyinga qoldirish

To'liq chegara qimmat: ikki tomonli interfeys, ma'lumot tuzilmalarining ikki nusxasi, alohida modul, alohida qurilish va reliz. Ko'p holatda chegara kerak bo'ladimi yo'qmi hali ma'lum emas. Yo'q qilib qo'yish ham, to'liq qurish ham yomon: biri keyin qimmat, ikkinchisi hozir qimmat. O'rtadagi yo'l qisman chegara, va uning uchta shakli *Clean Architecture* ning shu nomdagi bobida sanab o'tilgan: oxirgi qadamni qoldirish, bir tomonli chegara va facade.

| Shakl | Nima qilinadi | Keyin to'liq chegaraga o'tish |
|---|---|---|
| Oxirgi qadamni qoldirish | modul to'liq ajratiladi, lekin bitta artefaktda qoladi | reliz quvurini qo'shish |
| Bir tomonli chegara | interfeys va uning bitta implementatsiyasi bor, teskari yo'nalish yo'q | ikkinchi tomonni qo'shish |
| Facade | faqat kirish nuqtasi bitta sinfga yig'iladi, abstraksiya yo'q | interfeys ajratish |

Birinchi shakl Java da paket darajasida qilinadi: modul o'z paketida, chiqadigan turlar `public`, ichi `package-private`, chegarani ArchUnit yoki Spring Modulith tekshiradi. Shu holatda kod to'liq chegaraning hamma talabini bajaradi, faqat alohida jar bo'lib chiqmaydi.

```java
// bir tomonli chegara: domen port e'lon qiladi, implementatsiya tashqarida
public interface PricingPort {
    Money priceOf(Sku sku);
}

// ArchUnit: ichki paketga tashqaridan murojaat yo'q
@ArchTest
static final ArchRule chegara = classes()
        .that().resideInAPackage("..pricing.internal..")
        .should().onlyBeAccessed().byClassesThat().resideInAPackage("..pricing..");
```

Qisman chegaraning narxi ham bor va u yashirin: kod ikki tomonli chegaraga **o'xshaydi**, lekin kafolat bermaydi. Shu sababli tanlov yozib qo'yiladi (ADR da: qaysi shakl tanlandi va to'liq chegaraga qanday signal bo'lsa o'tiladi), aks holda keyingi odam uni to'liq chegara deb o'ylab, unga tayanadi. Qaysi signal o'tishni talab qiladi: ikkinchi implementatsiya paydo bo'lishi, modul boshqa jamoaga o'tishi, yoki reliz tezligi ajralishi. Chegarani umuman qo'ymaslik qarori ham haqli bo'ladi, lekin u ham ayni shu tarzda yoziladi.

## 5.12 Biznes use case o'sishi va kengaytirish nuqtasi narxi

"Masshtablanadigan arxitektura" iborasi ikki boshqa narsani bildiradi va ularni aralashtirish noto'g'ri abstraksiyaga olib keladi. Orosz ikkiga ajratadi: yangi biznes use case larining o'sishi, va ma'lumot, foydalanish hamda trafik yukining o'sishi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 25-bob, 367-bet). Yuk tomoni korpusda [kelajak taxmini](01-arxitektorning-fikrlash-modeli.md#17-hozirgi-talab-va-kelajak-taxmini-orasidagi-muvozanat) va napkin math bo'limlarida; bu yerdagi savol boshqa: yangi variantni qo'shish narxi qancha va kengaytirish nuqtasi qayerda turishi kerak.

Orosz ning misoli to'lov usullari. Jamoa avval karta bilan to'lovni qiladi, keyin biznes PayPal, naqd, Apple Pay va PayTM so'raydi. Har birini noldan yozish mumkin, lekin bu masshtablanmaydi: biznes yangi to'lov usuli so'rashda davom etishini tan olib, bitta kengaytirish nuqtasi quriladi. Kitobdagi hisob shunday ko'rinadi: bitta to'lov usulini backend, web va mobil tomonda qo'shish taxminan bir oy olsa, bir necha oyda quriladigan qat'iy shaklli framework shu vaqtni bir necha kunga tushiradi (367-bet). Raqamlar Orosz ning misolidagi raqamlar, universal mo'ljal emas.

Kengaytirish nuqtasini qurish qarori ikki bilimsiz qilinmaydi (368-bet). Birinchisi: biznes qanday ishlashi, ya'ni to'lov holatida eng keng tarqalgan usullarni domen mutaxassisi bilan birga ko'rib chiqish. Ikkinchisi: kompaniyaning roadmap i. Agar biznes ikki yil ichida faqat bitta usul qo'shmoqchi bo'lsa, javob yo'q; agar bir yilda o'nta usul rejalashtirilgan bo'lsa, oldindan tayyorlanish oqilona. Shu ikkinchi shart korpusdagi [uchlik qoidasi](#52-erta-abstraksiya-va-takrorlanish-qaysi-biri-arzonroq) ning ustiga qo'yiladigan qo'shimcha darvoza: uchta haqiqiy holat ko'rinmaguncha abstraksiya chiqarilmaydi, lekin uchtasi ko'ringanda ham roadmap bo'sh bo'lsa, framework qurilmaydi.

Kengaytirish nuqtasi shakli oddiy: variant interfeysi va uni kod nomi bo'yicha emas, domen kaliti bo'yicha tanlaydigan registr. Spring da buni konteyner yig'ib beradi.

```java
public interface PaymentMethodHandler {

    PaymentMethodCode code();

    PaymentResult pay(PaymentRequest request);
}

@Component
public class PaymentMethodRegistry {

    private final Map<PaymentMethodCode, PaymentMethodHandler> handlers;

    // Yangi usul = yangi @Component. Registr va chaqiruvchi o'zgarmaydi.
    public PaymentMethodRegistry(List<PaymentMethodHandler> discovered) {
        this.handlers = discovered.stream()
                .collect(Collectors.toMap(PaymentMethodHandler::code, h -> h));
    }

    public PaymentMethodHandler require(PaymentMethodCode code) {
        PaymentMethodHandler handler = handlers.get(code);
        if (handler == null) {
            throw new UnsupportedPaymentMethodException(code);
        }
        return handler;
    }
}
```

Chegarani shu yerda ushlab turish kerak: registr faqat tanlash javobgarligini oladi, to'lov usuliga xos qoida handler ichida qoladi. Agar registr `if` larga to'lib ketsa yoki handler interfeysiga har yangi usul uchun yangi metod qo'shilsa, bu kengaytirish nuqtasi noto'g'ri o'qda qurilganini bildiradi, va [noto'g'ri abstraksiyadan qaytish](#53-notogri-abstraksiya-narxi-va-undan-qaytish-yoli) qoidasi ishlaydi.

## 5.13 Ajratish rejimi: manba, deploy va servis darajasi

[5.11](#511-qisman-chegara-toliq-chegara-narxini-keyinga-qoldirish) qisman chegaraning shaklini tanladi. Shundan keyin ikkinchi va ko'pincha e'tibordan qoladigan savol turadi: shu chegara fizik jihatdan qaysi darajada ushlanadi. *Clean Architecture* ning "mustaqillik" bobi buni ajratish rejimi (decoupling mode) deb ataydi va uchta rejimni sanaydi.

| Rejim | Chegara nimada ushlanadi | Aloqa | Nimadan himoya qiladi |
|---|---|---|---|
| Manba darajasi | bitta artefakt ichidagi modullar, import nazorati | bitta adres maydoni, metod chaqiruvi | bir modulni o'zgartirish boshqasini qayta kompilyatsiyaga majbur qilmaydi |
| Deploy darajasi | mustaqil deploy qilinadigan birlik (jar, DLL) | ko'pincha yana metod chaqiruvi, dinamik linklash | bir modul kodi o'zgarishi boshqasini qayta qurish va qayta deploy qilishga majbur qilmaydi |
| Servis darajasi | alohida bajarilish birligi, ya'ni protsess | faqat tarmoq paketi | bog'liqlik ma'lumot tuzilmasi darajasiga tushadi, manba va binar o'zgarishlari umuman o'tmaydi |

Qaysi rejim to'g'ri? Kitobning javobi ochiq: erta bosqichda buni bilish qiyin, va loyiha yetilgani sayin maqbul rejimning o'zi o'zgaradi. Bitta serverda bemalol ishlayotgan tizim o'sib, ba'zi komponentlari alohida serverga chiqishi kerak bo'lib qolishi mumkin; shu paytgacha manba darajasidagi ajratish yetarli edi. "Hammasini darhol servis darajasida ajratamiz" degan yechim kitobda alohida tanqid qilinadi: u yirik donali ajratishni rag'batlantiradi, qancha "mikro" bo'lsa ham ajratish yetarlicha mayda bo'lmaydi, va narxi ikki tomonlama, ishlab chiqish vaqti hamda tizim resursi, ulardan birinchisi esa arzon emas.

Shundan kitobning afzal ko'rgan strategiyasi chiqadi va u ikki qismdan iborat: ajratishni servis hosil qilish mumkin bo'ladigan nuqtaga yetkaz, lekin komponentlarni imkon boricha uzoq bir adres maydonida qoldir. Boshida komponentlar manba darajasida ajratiladi va bu loyihaning butun umri uchun yetarli bo'lishi mumkin. Deploy yoki ishlab chiqish muammosi chiqsa, ajratishning bir qismini deploy darajasiga ko'tarish bir muddat yetadi; muammolar o'sgani sayin arxitektor qaysi deploy birligini servisga aylantirishni ehtiyotkorlik bilan tanlaydi. Teskari harakat ham ruxsat etilgan: operatsion ehtiyoj pasaysa, servis darajasini talab qilgan narsa yana deploy yoki manba darajasiga qaytishi mumkin. Yaxshi arxitektura tizimga monolit bo'lib tug'ilishga va servislargacha o'sishga, keyin esa yana monolitga qaytishga imkon beradi; uning asosiy ishi manba kodining ko'p qismini shu o'zgarishlardan himoyalash.

"Chegara anatomiyasi" bobi bu ro'yxatga ikkita aralashtiriladigan narsani qo'shadi.

**Thread chegara emas.** Monolit ham, deploy komponenti ham thread ishlatishi mumkin, lekin thread arxitektura chegarasi ham, deploy birligi ham emas: u bajarilish jadvalini va tartibini tashkil qilish usuli. Thread butunlay bitta komponent ichida yashashi yoki bir nechta komponentga tarqalishi mumkin. Spring da bundan aniq natija chiqadi: `@Async`, executor yoki virtual thread qo'shish bog'liqlikni kamaytirmaydi.

```java
// Thread chegara emas: ikki qism bir xil adres maydonida va bir xil ichki holatda qoladi
@Service
public class OrderPlacement {

    private final InventoryState state;  // bog'liqlik o'zgarmadi
    private final Executor executor;     // faqat bajarilish tartibi o'zgardi

    public void place(OrderDraft draft) {
        executor.execute(() -> state.reserve(draft));
    }
}
```

**Lokal protsess jar dan kuchli, servisdan arzon.** Lokal protsess bir xil protsessorda, lekin alohida adres maydonida ishlaydi; xotira himoyasi protsesslarni xotirani bo'lishishdan to'sadi va aloqa socket yoki xabar navbati orqali ketadi. Bog'liqlik yo'nalishi qoidasi o'zgarmaydi: yuqori darajadagi protsessning manba kodida past darajadagi protsessning nomi, fizik manzili yoki registr kaliti bo'lmasligi kerak, chunki maqsad past darajani yuqori darajaga plugin qilish. Narxi o'rtacha (OS chaqiruvi, marshalling, kontekst almashinuvi), shuning uchun gapdon (chatty) aloqani cheklash kerak. Servis esa eng kuchli chegara: u fizik joylashuvga tayanmaydi va javob vaqti o'n millisekunddan sekundlargacha boradi.

Amaliy xulosa: monolitdan boshqa deyarli hamma tizim bir vaqtda bir nechta rejimni ishlatadi, shuning uchun savol "biz monolitmi yoki mikroservismi" emas, "qaysi chegara qaysi rejimda" bo'ladi. Rejim ham, uni ko'tarish signali ham 5.11 dagi ADR yozuvining bir qatori, operatsion narxi esa [6.8](06-murakkablikni-boshqarish.md#68-servislar-soni-va-operatsion-murakkablik-narxi) da hisoblangan.

Oxirgi qoida rejim tanlovining ustiga qo'yiladi: konfiguratsiyani ish vaqtida o'zgartiradigan dizayndan iloji boricha qochish kerak. Fairbanks sababini ikki qatorda beradi va ikkisi ham tahlilga tegishli. Birinchisi, statik arxitekturani dasturchi osonroq tushunadi, bu esa yaxshiroq modifiability va kamroq xatoga olib keladi. Ikkinchisi, statik arxitekturani sifat atributlari bo'yicha tahlil qilish osonroq: bitta barqaror konfiguratsiyani tekshirish ish vaqtida yuzaga keladigan barcha konfiguratsiyalarni tekshirishdan arzon. Muammoning tabiati majbur qilgan holatlar bor (peer-to-peer tizim, komponentni dinamik yuklaydigan freymvork), lekin unda arxitektor empirik ma'lumot va asbob kam bo'lgan hududda ishlayotganini bilishi kerak. Qo'shimcha eslatma: ko'p tizim komponent konfiguratsiyasini faqat ishga tushish va o'chish paytida o'zgartiradi, qolgan vaqtda barqaror turadi, va diagramma odatda shu barqaror holatni ko'rsatadi; bu soddalashtirish ekanini unutish startup va shutdown dinamikasida xato keltiradi. Konfiguratsiyani bajariladigan koddan deklarativ faylga chiqarish mantiqi ham shundan chiqadi va uning yozuvi [6.4](06-murakkablikni-boshqarish.md#64-konfiguratsiya-murakkabligi-har-bir-flag-kelajakdagi-xato) da.

## 5.14 Temporal dekompozitsiya: tartib bo'yicha bo'lish va uning qizil bayrog'i

[4.8](04-kod-muloqot-vositasi-nomlash-aniqlik.md#48-paket-tuzilishi-xususiyat-boyicha-bolish) paket tuzilishi uchun ikki variantni qarama-qarshi qo'yadi: qatlam bo'yicha va xususiyat bo'yicha. Amalda uchinchi variant ham uchraydi va u ikkisidan ham xavfliroq, chunki xususiyat bo'yicha bo'lishga o'xshab ko'rinadi. Ousterhout uni temporal dekompozitsiya deb ataydi: tizimning tuzilishi amallar bajarilish vaqti tartibiga mos qilib qo'yiladi.

Kitobning misoli sodda: ilova faylni ma'lum formatda o'qiydi, mazmunini o'zgartiradi va yana yozib qo'yadi. Temporal dekompozitsiyada bu uch sinfga bo'linadi, ya'ni o'qiydigan, o'zgartiradigan va yozadigan sinf. Natijada format bilimi o'qish va yozish sinflarining ikkisida ham bo'ladi, ya'ni ma'lumot oqib chiqadi (information leakage). Yechim ham shu yerdan chiqadi: o'qish va yozishning asosiy mexanizmini bitta sinfga yig'ish, va o'sha sinf ikki fazada ham ishlatiladi.

**Qizil bayroq: temporal dekompozitsiya.** Kod tuzilishi bajarilish tartibini aks ettirsa, ya'ni turli vaqtda sodir bo'ladigan amallar turli metod yoki sinflarda bo'lsa va shu amallar bir xil bilimga tayansa, bilim bir necha joyda kodlanadi va ma'lumot oqib chiqadi.

Kitobning ikkinchi misoli buni yanada aniq ko'rsatadi: talabalar HTTP so'rovini qabul qilishni ikki sinfga bo'lgan, biri so'rovni tarmoq ulanishidan satrga o'qiydi, ikkinchisi satrni parse qiladi. Muammo shundaki, HTTP so'rovini parse qilmasdan o'qib bo'lmaydi: `Content-Length` sarlavhasi tananing uzunligini aytadi, demak so'rovning umumiy uzunligini bilish uchun sarlavhalarni parse qilish kerak. Natijada ikki sinf ham so'rov tuzilishining ko'p qismini tushunishga majbur bo'lgan, parse kodi ikkisida takrorlangan, chaqiruvchi esa ikki sinfning ikki metodini ma'lum tartibda chaqirishga majbur bo'lgan.

Spring da bu tuzilish tanib olinadigan nomlar bilan keladi. Quyidagi misol kitobdagi fayl misolining Java ga o'tkazilgan ko'rinishi:

```java
// Yomon: tartib struktura bo'lib qolgan, format bilimi ikki joyda
@Service
public class PriceImportPipeline {
    private final Step1ReadPriceFile step1;    // CSV formatini biladi
    private final Step2AdjustPrices step2;
    private final Step3WritePriceFile step3;   // CSV formatini yana biladi
}

// Yaxshi: bilim bo'yicha bo'lingan, tartib orkestrator metodida qoldi
@Service
public class PriceImport {

    private final PriceFileCodec codec;        // o'qish ham, yozish ham bitta sinfda
    private final PriceAdjustment adjustment;

    public void run(Path source, Path target) {
        List<PriceRow> rows = codec.read(source);
        codec.write(target, adjustment.apply(rows));
    }
}
```

Belgilar ro'yxati qisqa: nomida `Step`, `Phase`, `Stage` yoki tartib raqami bor bean; `...Pipeline` yoki `...ProcessingFlow` nomli paket, uning ichida `Validator`, `Enricher` va `Persister` ketma-ket turadi; bitta domen tushunchasining formati yoki sxemasi bir nechta sinfda takrorlanishi. Ousterhout ning qoidasi esa bitta jumla: modul loyihalaganda har bir vazifani bajarish uchun kerak bo'ladigan bilimga qarang, vazifalar qanday tartibda bajarilishiga emas.

Diqqat qiling, bu tartib ahamiyatsiz degani emas. Tartib ko'pincha muhim va u ilovada baribir aks etadi; faqat u modul tuzilishida aks etmasligi kerak, agar o'sha tuzilish ma'lumotni yashirishga mos bo'lmasa. Istisnoni kitobning o'zi aytadi: fazalar butunlay boshqa bilimga tayansa, ularni ajratish temporal dekompozitsiya emas. Tekshirish savoli [5.5](#55-koheziya-nima-birga-ozgarsa-birga-tursin) ning savoliga qaytadi: formatni yoki sxemani o'zgartirsam, necha sinfga tegaman?

## 5.15 Yuqoridan pastga va pastdan yuqoriga: bog'liqlik grafi loyihalanmaydi, o'sadi

Bahsni boshlashdan oldin qaysi daraja haqida gaplashayotganingizni aytish kerak, aks holda ikki odam bir xil so'z bilan boshqa narsani himoya qiladi. *Code Complete* dizaynning besh darajasini sanab beradi: (1) butun tizim, (2) quyi tizim yoki paketlarga bo'lish, (3) paket ichida sinflarga bo'lish, (4) sinf ichida ma'lumot va rutinalarga bo'lish, (5) rutinaning ichki dizayni. Kitob ikkinchi darajani alohida ajratadi, chunki bu bobning hamma savoli shu yerda yashaydi: ikkinchi darajaning asosiy mahsuloti yirik quyi tizimlarni aniqlash va qaysi quyi tizim qaysinisidan foydalanishi mumkinligini belgilash. Ogohlantirish ham shu yerda: agar hamma quyi tizim hamma quyi tizim bilan aloqa qila olsa, ularni ajratishdan keladigan foyda butunlay yo'qoladi. Kitob bu darajadagi bo'lishni bir necha haftadan uzoq har qanday loyiha uchun zarur deb hisoblaydi.

Ikki yondashuv juftligi ham shu kitobdan keladi va farqi bitta gapda: yuqoridan pastga bu dekompozitsiya, pastdan yuqoriga bu kompozitsiya strategiyasi. Yuqoridan pastga umumiy sinflardan boshlanadi va bosqichma-bosqich tafsilotga tushadi; uning kuchi shundaki, miya bir vaqtda faqat ma'lum miqdordagi tafsilotni ushlaydi, to'xtash mezoni esa amaliy: keyingi darajani bo'lishdan ko'ra uni kodda yozish osonroq ko'ringanda to'xtatiladi. Pastdan yuqoriga yuqoridan pastga juda abstrakt bo'lib boshlash qiyin bo'lganda ishlatiladi: "bu tizim nima qilishi kerak" savolidan konkret majburiyatlar chiqariladi, keyin ular guruhlanadi. Ba'zan dizaynning katta qismi pastdan, masalan tashqi interfeys talablari bilan dikta qilinadi. Ikkisi raqobatchi emas, bitta ishning ikki yo'nalishi.

Lekin bir narsa yuqoridan pastga loyihalanmaydi, va *Clean Architecture* buni keskin aytadi: komponentlar bog'liqlik tuzilmasi yuqoridan pastga loyihalanmaydi. Sabab nomlangan: komponent bog'liqlik diagrammasi ilovaning funksiyasini tasvirlamaydi, u ilovaning qurilishi va texnik xizmatining xaritasi. Loyiha boshida quriladigan va xizmat ko'rsatiladigan hech narsa yo'q, demak bunday xaritaga ehtiyoj ham yo'q. Graf o'sadi: avval modullar yig'ilgani sayin SRP va Umumiy Yopilish Printsipi birga o'zgaradigan sinflarni birga yig'adi, va bu yerdagi asosiy tashvish o'zgaruvchanlikni izolyatsiya qilish, ya'ni GUI ning kosmetik o'zgarishi biznes qoidalariga tegmasligi. Keyin qayta ishlatish tashvishi paydo bo'lganda Umumiy Ishlatish Printsipi tarkibga ta'sir qila boshlaydi, sikl chiqqanda esa Asiklik Bog'liqliklar Printsipi qo'llanadi va graf yana siljiydi. Kitobning xulosasi aniq: sinflarni loyihalashdan oldin komponent grafini loyihalashga urinilsa, natija yomon bo'ladi, chunki umumiy yopilish haqida ma'lumot yo'q, qayta ishlatiladigan elementlar hali ko'rinmagan, va deyarli aniq sikl yaratiladi.

ESLATMA, shu korpusning amaliy tarjimasi: birinchi hafta mahsuloti modul diagrammasi emas, chegara nomzodlari ro'yxati va ularni tasdiqlaydigan o'lchov bo'ladi ([5.6](#56-modul-chegarasini-qayerdan-otkazish-ozgarish-tezligi-va-egalik-boyicha) dagi git buyruqlari shu uchun). Diagramma kodda chegara paydo bo'lgandan keyin yoziladi, ArchUnit qoidasi esa chegara haqiqatan mavjud bo'lganda qo'shiladi, aks holda qoida hali bo'lmagan narsani qotirib qo'yadi.

## 5.16 Umumiy egalik: ko'p servis yozadigan jadvalga yagona ega

[Sxema chegarasi](#59-sxema-chegarasi-boshqa-servisning-jadvaliga-tegmaslik-qoidasi) bo'limidagi qoida sodda holatda yetadi: jadvalga yozadigan servis uning egasi. Umumiy egalik (common ownership) shu qoidani buzadigan birinchi holat, ya'ni ko'pchilik yoki hamma servis bitta jadvalga yozadi. *The Hard Parts* ning misoli audit jadvali: wishlist, katalog va ombor servislari foydalanuvchi bajargan amalni shu bitta jadvalga yozadi. Kitob darhol eslatadi, misolda uch servis bor, haqiqiy tizimda esa bunday jadvalga yuzlab yoki minglab servis yozishi mumkin, shuning uchun jadvalning egasini aniqlash umuman mumkin bo'lmaydi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021, 9-bob, 252-bet).

Eng oson ko'rinadigan yechim xato. Jadvalni umumiy bazaga yoki umumiy sxemaga qo'yib, hamma servisga yozish huquqini berish ma'lumotni bo'lishishning hamma muammosini qaytarib keltiradi: o'zgarish nazorati, ulanishlarning qurib qolishi, masshtab va nosozlikka chidamlilik (9-bob, 252-bet). Shu sabablarning to'liq ro'yxati [bazani bo'lish sabablari](#518-bazani-bolish-sabablari-oltita-disintegrator-va-ikkita-integrator) da.

Kitobning yechimi boshqa: jadvalga bitta maxsus servis yagona ega qilib tayinlanadi, faqat u yozadi, qolganlari esa ma'lumotni unga uzatadi va yozish amalini ega bajaradi (9-bob, 252-bet). Audit misolida bu yangi audit servisi degani: u jadvalga yozadigan va undan o'qiydigan yagona servis bo'lib qoladi. Aloqa shaklini bitta savol belgilaydi, ya'ni chaqiruvchiga yozuv natijasidan biror ma'lumot qaytishi kerakmi.

Quyidagi jadval kitobning o'z jadvali emas: u 252-253-betlardagi ikki variantni yonma-yon qo'yadi.

| Chaqiruvchiga javob kerakmi | Aloqa shakli | Nega shunday |
| --- | --- | --- |
| Kerak emas | doimiy (persisted) navbat, asinxron fire-and-forget | chaqiruvchi yozuvni kutmaydi; broker xabarni diskka yozgani uchun servis yoki brokerning yiqilishida ham xabar yo'qolmaydi |
| Kerak, masalan tasdiq raqami yoki baza kaliti | REST, gRPC yoki request-reply messaging | javob kutiladi, demak sinxron chaqiruvning kutish narxi ataylab qabul qilinadi |

Spring tomonidan bu qoida bitta gapga aylanadi: audit yozuvini o'z tranzaksiyangda yozma, egasiga yubor. Yuborish faktini mahalliy tranzaksiya bilan atomar qilish kerak bo'lsa, xabar avval o'z sxemangdagi jadvalga yoziladi va keyin jo'natiladi; bu [tranzaksion outbox](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox) yozuvi.

```java
// Audit jadvalining yagona egasi AuditService. Wishlist servisi unga faqat
// xabar yuboradi: javob kutilmaydi, shuning uchun doimiy navbat yetarli.
@Service
public class WishlistService {

    private final WishlistRepository wishlists;
    private final ApplicationEventPublisher events;

    public WishlistService(WishlistRepository wishlists, ApplicationEventPublisher events) {
        this.wishlists = wishlists;
        this.events = events;
    }

    @Transactional
    public void addItem(long customerId, String productId) {
        wishlists.save(new WishlistItem(customerId, productId));
        // Hodisa tranzaksiya commit bo'lgandan keyin brokerga ketadi:
        // audit jadvaliga bu servis hech qachon o'zi yozmaydi.
        events.publishEvent(new WishlistItemAdded(customerId, productId));
    }
}

@Component
class WishlistAuditForwarder {

    private final KafkaTemplate<String, WishlistItemAdded> kafka;

    WishlistAuditForwarder(KafkaTemplate<String, WishlistItemAdded> kafka) {
        this.kafka = kafka;
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    void forward(WishlistItemAdded event) {
        kafka.send("audit.events", event);
    }
}
```

Qoida teskari tomonga ham ishlaydi: ega bo'lmagan servis umumiy ma'lumotni o'qishi kerak bo'lsa, bu alohida masala va kitob unga faqat o'qish uchun kirish usullarini ajratib, 10-bobda ko'rib chiqadi (9-bob, 253-bet). Ya'ni "yozish bitta egada" qoidasi o'qishni avtomatik hal qilmaydi.

## 5.17 Birgalikda egalik: bitta jadvalga ikki yozuvchi va to'rt yechim

Birgalikda egalik (joint ownership) umumiy egalikdan miqdori bilan farq qiladi: bu yerda bitta domen ichidagi bir necha servis bitta jadvalga yozadi, umumiy egalikda esa deyarli hamma servis yozadi (9-bob, 253-bet). Kitobning misoli mahsulot jadvali: katalog servisi yangi mahsulot qo'shadi, olib tashlaydi va statik ma'lumotini yangilaydi, ombor servisi esa shu jadvaldagi joriy qoldiqni o'qiydi va yangilaydi (9-bob, 254-bet). JPA bilan ishlaganda bu holat eng tez taniladi: ikki servisda bir xil `@Entity` nusxasi paydo bo'ladi va ikkisi bir jadvalga `update` yozadi.

Kitob to'rt yechim beradi va har birining kelishuvini jadval bilan sanaydi (9-bob, 254-262-betlar).

**Jadvalni bo'lish (table split).** Jadval ikkiga bo'linadi, har servis o'z bo'lagiga ega bo'ladi: mahsulot qoldig'i alohida `inventory` jadvaliga ko'chadi va `product` dan qoldiq ustuni olib tashlanadi (254-bet). Natijada birgalikda egalik yagona egalikka aylanadi, lekin yangi vazifa paydo bo'ladi: mahsulot qo'shilganda yoki o'chirilganda ikki servis bir-biri bilan gaplashishi kerak (255-bet). Shu yerda kitob to'g'ridan-to'g'ri CAP ga boradi: katalog ombor servisi ishlamayotganda ham mahsulot qo'shaversin desangiz, mavjudlikni tanlaysiz; ikki jadval doim mos tursin desangiz, izchillikni tanlaysiz va ombor ko'tarilmaganda mahsulot qo'shish amali yiqiladi (256-bet). Aloqa shakli ham shu tanlovdan chiqadi: tasdiq kerak bo'lsa sinxron, kerak bo'lmasa fire-and-forget.

```sql
-- Jadvalni bo'lish: qoldiq ustuni alohida jadvalga ko'chadi.
-- Ikki qadam alohida migratsiyada ketadi, orasida ikkala servis ishlaydi.
CREATE TABLE inventory (
    product_id text PRIMARY KEY,
    inv_cnt    integer NOT NULL DEFAULT 0
);

INSERT INTO inventory (product_id, inv_cnt)
SELECT product_id, inv_cnt FROM product;

-- Faqat ombor servisi yozadi, katalog hatto o'qimaydi ham.
GRANT SELECT, INSERT, UPDATE, DELETE ON inventory TO inventory_app;

-- Keyingi relizda, barcha o'qishlar yangi jadvalga o'tgandan keyin:
ALTER TABLE product DROP COLUMN inv_cnt;
```

**Ma'lumot domeni (data domain).** Jadval ikki servisga ham tegishli bo'lib qoladi: ular bo'lishadigan jadvallar bitta sxemaga yoki bazaga yig'iladi va servislar bilan ma'lumot orasida kengroq bounded context hosil bo'ladi (256-bet). Servislar bir-biriga bog'liq bo'lmaydi, lekin sxemaning har bir o'zgarishi ikkisiga ham tegadi (257-258-betlar). Kitob bu yechimni tanlaganda majburiy savol qo'yadi: ma'lumot ikkisiga umumiy bo'lsa, nega bu ikki servis alohida turadi? Javob masshtab farqi, nosozlikka chidamlilik, o'tkazuvchanlik farqi yoki kod o'zgarish tezligini ajratish bo'lishi kerak (257-bet).

**Delegatsiya (delegate).** Jadval bitta servisga beriladi va u delegat bo'ladi, boshqalar esa yozuvni uning nomidan bajarishini so'raydi (258-bet). Qiyin savol delegatni tanlash, va kitob ikki variantni nomlab beradi: birlamchi domen ustuvorligi jadvalni entitetning asosiy CRUD amallarini bajaradigan servisga beradi (katalog), operatsion xarakteristika ustuvorligi esa ishlash, masshtab yoki mavjudlik talabi yuqori servisga beradi (ombor, chunki qoldiq statik mahsulot ma'lumotidan tez-tez o'zgaradi) (258-259-betlar). Mualliflar odatda domen ustuvorligini tanlashni, ishlash va chidamlilik muammosini esa replikatsiyalangan yoki taqsimlangan cache bilan yumshatishni tavsiya qiladi, chunki ombor servisi mahsulot ma'lumotining baza amallari va xatolarini boshqarishga mas'ul emas (260-bet). Delegat kim bo'lishidan qat'i nazar, egasi bo'lmagan servis uchun atomar tranzaksiya yo'qoladi; shu sababli usul eventual izchillikka toqat qiladigan yozuvlarga mos keladi (260-bet).

**Servislarni birlashtirish (service consolidation).** Ikki servis bitta servisga qo'shiladi va birgalikda egalik yana yagona egalikka aylanadi (261-bet). Atomar tranzaksiya saqlanadi, lekin masshtab endi faqat birga bo'ladi: kam yuklangan katalog qismi ham ombor yuki uchun ko'tarilishi kerak (261-262-betlar).

| Yechim | Nima yutiladi | Nima yo'qotiladi |
| --- | --- | --- |
| Jadvalni bo'lish | bounded context saqlanadi, egalik yagona bo'ladi | jadvalni qayta tuzish kerak, ikki jadval orasida ACID yo'q, sinxronlash qiyin |
| Ma'lumot domeni | tez kirish, masshtab muammosi yo'q, ma'lumot izchil, servislar bog'liq emas | sxema o'zgarishi ko'p servisga tegadi, test qamrovi va deploy xavfi oshadi, yozish huquqini boshqarish kerak |
| Delegatsiya | yagona egalik hosil bo'ladi, sxema o'zgarishi nazoratda, ma'lumot tuzilishi boshqalardan yashiriladi | servislar qattiq bog'lanadi, ega bo'lmagan yozuv sekin, atomar tranzaksiya yo'q, chidamlilik past |
| Servislarni birlashtirish | atomar tranzaksiya saqlanadi, umumiy ishlash yaxshi | masshtab yiriklashadi, chidamlilik kamayadi, deploy xavfi va test qamrovi oshadi |

Kitobning o'z misolida tanlov delegatsiyaga tushadi: mahsulot jadvalining yagona egasi katalog servisi bo'ladi, ombor esa yangilash so'rovlarini unga yuboradi (9-bob, 262-bet). Bu yagona to'g'ri javob emas: yuqoridagi jadval aynan shu qaror uchun [mezon jadvali](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md#32-variantlarni-taqqoslash-mezon-jadvali-va-ogirlik-berish) o'rnida ishlatiladi.

## 5.18 Bazani bo'lish sabablari: oltita disintegrator va ikkita integrator

"Monolit bazani bo'laylik" degan taklif texnik emas, qaror: *The Hard Parts* uni oltita bo'luvchi va ikkita birlashtiruvchi kuch orasidagi muvozanat deb qo'yadi, va ikki tomonning kelishuvini tahlil qilish ma'lumot granulyarligini to'g'ri tanlashning kaliti deb ataladi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021, 6-bob, 132-bet). Dasturchi uchun buning qiymati amaliy: bu ro'yxat bazani ajratish taklifini DBA bilan muhokama qiladigan tilga aylantiradi.

Oltita disintegrator, ya'ni bo'lishni oqlaydigan sabab (6-bob, 133-bet):

- **O'zgarish nazorati (change control).** Jadval o'zgarishi nechta servisga tegadi. Ustun yoki jadvalni o'chirish, nomini yoki turini o'zgartirish buzadigan o'zgarish bo'ladi va shu jadvalga tegadigan hamma servis baza bilan birga deploy qilinishi kerak; haqiqiy xavf esa jadvalga murojaat qiladigan servisni unutib qo'yish, chunki u production da qayta deploy qilinmaguncha ishlamay turadi (6-bob, 134-135-betlar). Bounded context shuning uchun yechim: servis o'z ma'lumoti bilan birga bitta kontekstda bo'lsa, o'zgarish shu kontekst ichida qoladi, tashqariga esa shartnoma chiqadi va shartnoma sxemadan farq qilishi mumkin (6-bob, 136-137-betlar).
- **Ulanishlarni boshqarish (connection management).** Kitobning hisobi: 200 ulanishli monolit 50 servisga bo'linsa va har servisning pooli 10 ulanishdan, minimal ikki instance bilan 1000 ulanish chiqadi; servislarning yarmi o'rtacha beshta instance gacha ko'tarilsa, son 1700 ga yetadi (6-bob, 139-bet). Yechim sifatida kitob har servisga ulanish kvotasi berishni, dastlab teng taqsimlashni va keyin o'lchovga qarab farqli taqsimlashga o'tishni, kvota qiymatlarini esa tashqi konfiguratsiyada saqlashni tavsiya qiladi (6-bob, 139-140-betlar).
- **Masshtab (scalability).** Taqsimlangan tizim masshtablanishi uchun bazasi ham masshtablanishi kerak. Kitobning jadvalida 100 ulanishga moslangan kvota servislar ko'tarilgandan keyin 242 ulanishga aylanadi, ya'ni mavjud ulanishdan 142 ta ko'p (6-bob, 142-143-betlar).
- **Nosozlikka chidamlilik (fault tolerance).** Umumiy baza yagona nosozlik nuqtasi bo'lib qoladi va u yiqilganda hamma servis ishlamaydi; ma'lumot bo'linganda esa faqat o'sha bazaga bog'liq servislar ta'sirlanadi (6-bob, 143-144-betlar).
- **Arxitektura kvanti (architectural quanta).** Umumiy baza hamma servisni bitta kvantga qamab qo'yadi, demak ikki servisga boshqa arxitektura xarakteristikasi kerak bo'lsa, ularni ajratish uchun ma'lumot ham ajralishi shart (6-bob, 144-145-betlar).
- **Baza turini moslash (database type optimization).** Monolit bazada hamma ma'lumot bitta tur qoidasiga bo'ysunadi. Kitobning misoli: relyatsion bazada yashayotgan kalit-qiymat shaklidagi ma'lumotnoma (mamlakat, mahsulot, ombor kodlari) uchun kalit-qiymat baza mosroq yechim beradi (6-bob, 146-bet). Tur tanlash mezonlarining o'zi [baza turini tanlash](38-doimiy-organish-va-texnologiya-tanlash.md#3813-baza-turini-tanlash-yettita-mezon-va-nega-ular-birga-ishlaydi) bo'limida.

Qarshi tomonda ikkita integrator, ya'ni ma'lumotni birga ushlashni oqlaydigan sabab (6-bob, 146-149-betlar): **ma'lumot munosabatlari**, ya'ni foreign key, trigger, view va stored procedure jadvallarni bir-biriga bog'lab turadi va ular boshqa sxemaga ko'chganda olib tashlanishi kerak; hamda **baza tranzaksiyalari**, ya'ni bir servis bir necha jadvalga yozganda bu bitta ACID ish birligi bo'ladi, bo'linishdan keyin esa bunday birlik qolmaydi.

Qarorning o'zi shu ikki ro'yxatni to'qnashtirishdan chiqadi, va kitob savolni aynan shu shaklda beradi: o'zgarish nazorati jadvallar orasidagi foreign key ni saqlashdan muhimmi, nosozlikka chidamlilik materialized view ni saqlashdan muhimmi (6-bob, 148-bet). Qaysi biri muhimroq ekani aniq bo'lgandan keyingina bo'lish va natijadagi sxema granulyarligi haqida gapirish mumkin. Monolit bazani bosqichma-bosqich ajratish tartibi esa alohida mavzu: uning korpusdagi yozuvi [ma'lumotlar bazasini ajratish](34-legacy-kod-va-bosqichma-bosqich-refaktoring.md#348-malumotlar-bazasini-ajratish-eng-qiyin-qism-va-uning-tartibi) bo'limida.

Ulanish tomonidagi dalilni raqamga aylantirish uchun o'lchov kerak, va PostgreSQL buni o'zi beradi.

```sql
-- Har servis (alohida rol) qancha ulanish ushlab turgani va chegara.
-- Dalil shu: kvota muhokamasi taxmin bilan emas, shu jadval bilan boshlanadi.
SELECT usename                             AS servis_roli,
       count(*)                            AS hozir,
       count(*) FILTER (WHERE state = 'idle') AS bekor_turgan,
       current_setting('max_connections')::int AS server_chegarasi
FROM pg_stat_activity
WHERE backend_type = 'client backend'
GROUP BY usename
ORDER BY hozir DESC;
```

ESLATMA: yuqoridagi so'rov shu korpusning qo'shimchasi, kitobda yo'q. Kitob kvotani o'lchash uchun fitness function dan foydalanishni tavsiya qiladi (6-bob, 140-bet); bu so'rov shu o'lchovning eng arzon shakli.

## 5.19 O'tkazuvchi bog'liqlik: pastdagi servis uchun uzatilgan ma'lumot

[Bog'liqlik turlari](#54-bogliqlik-turlari-malumot-vaqt-joylashuv-sxema-boyicha-bogliqlik) jadvalidagi shakllardan biri alohida nom bilan yuradi. O'tkazuvchi bog'liqlik (pass-through coupling) shunda paydo bo'ladi: servis ma'lumotni qo'shnisiga faqat o'sha ma'lumot zanjirning pastidagi uchinchi servisga kerak bo'lgani uchun uzatadi. Newman buni implementatsiya bog'liqligining eng muammoli shakllaridan biri deb ataydi, chunki chaqiruvchi nafaqat chaqirayotgan servisning yana kimnidir chaqirishini biladi, balki o'sha bir qadam uzoqdagi servis qanday ishlashini ham bilishi kerak bo'ladi (Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 2-bob, "Pass-Through Coupling" bo'limi).

Newman ning misoli uch bo'g'inli: buyurtma protsessori omborga buyurtmani jo'natishga tayyorlashni so'raydi va so'rov tarkibida yetkazib berish varaqasini (shipping manifest) uzatadi, ombor esa varaqani o'zgartirmasdan yetkazib berish servisiga beradi. Asosiy muammo shu: pastdagi servisga kerakli ma'lumot o'zgarsa, yuqoridagi servislar ham o'zgaradi, ya'ni yetkazib berish servisi varaqaning formatini yoki tarkibini o'zgartirsa, ombor ham, buyurtma protsessori ham o'zgarishi kerak bo'ladi (2-bob).

Newman uchta chiqish yo'lini ko'rib chiqadi va hech birini bepul deb atamaydi.

| Yo'l | Nima o'zgaradi | Narxi |
| --- | --- | --- |
| Oraliq bo'g'inni chetlab o'tish | buyurtma protsessori yetkazib berish servisiga o'zi murojaat qiladi | domen bog'liqligi oshadi va ombor ichida yashiringan mantiq (avval qoldiqni band qilish, keyin jo'natish, so'ng qoldiqni yangilash) yuqoriga ko'chadi |
| Talabni yashirish | ombor o'z shartnomasida kerakli maydonlarni oladi va varaqani o'zi yasaydi | yetkazib berish shartnomasi o'zgarganda buyurtma protsessori sezmaydi, lekin ombor har o'zgarishda yangilanadi |
| Ma'lumotni shaffof blob sifatida uzatish | ombor varaqaga qaramaydi va tekshirmaydi, shunchaki o'tkazib yuboradi | format o'zgarsa buyurtma protsessori va yetkazib berish servisi o'zgaradi, ombor esa o'zgarmaydi |

Ikkinchi yo'l to'liq himoya bermaydi va Newman buni ochiq aytadi: yetkazib berish servisiga xalqaro jo'natish uchun bojxona deklaratsiyasi kerak bo'lsa va u ixtiyoriy parametr bo'lsa, faqat o'sha servis yangilanadi; majburiy bo'lsa, ombor uni yasashi kerak va buning uchun ma'lumot yetmasa, buyurtma protsessoridan qo'shimcha maydon so'raladi. Farq shundaki, uchta servisni bitta qadamda birga chiqarish (lockstep rollout) majburiyati yo'qoladi va deploy bosqichga ajratiladi (2-bob).

Java tomonida belgi aniq: shartnoma DTO sida chaqiruvchining o'ziga kerak bo'lmagan va u hech qachon o'qimaydigan maydonlar paydo bo'ladi.

```java
// Yomon shakl (shu yerda izohda qoldirilgan, chunki nom bitta bo'ladi):
// ombor shartnomasi yetkazib berish servisining tipini olib yuradi.
//
// public record PrepareOrderRequest(String orderId, List<OrderLine> lines,
//                                   ShippingManifest manifest) { }

// Yaxshi: ombor o'z tilida so'raydi va varaqani o'zi yasaydi.
public record PrepareOrderRequest(String orderId, List<OrderLine> lines,
                                  Address deliveryAddress, ShippingType shippingType) { }

@Service
public class WarehouseService {

    private final ShippingClient shipping;

    public WarehouseService(ShippingClient shipping) {
        this.shipping = shipping;
    }

    public DispatchId prepare(PrepareOrderRequest request) {
        reserveStock(request.lines());
        // Yetkazib berish shartnomasi faqat shu metod ichida ko'rinadi:
        // uning o'zgarishi PrepareOrderRequest ga tegmaydi.
        ShippingManifest manifest = new ShippingManifest(
                request.deliveryAddress(), request.shippingType());
        return shipping.dispatch(manifest);
    }
}
```

Tanlov mezoni oddiy: oraliq servis ma'lumotni **ishlatadimi**. Ishlatsa, u maydonlarni o'z tilida qabul qilib, pastdagi shartnomani o'zi yasashi kerak. Ishlatmasa va faqat o'tkazib yuborsa, ma'lumot ataylab shaffof blob bo'lib qolgani yaxshi, chunki shunda formatning o'zgarishi oraliq servisni chetlab o'tadi.

## 5.20 Cheklov yo'naltiruvchi sifatida: foydasi va kiritish tartibi

Bu bobdagi hamma qoida bitta shaklga ega: biror narsa taqiqlanadi. Import yo'nalishi bir tomonga, jadvalga bitta yozuvchi, interfeys iste'molchi tomonda. Fairbanks shu shaklning o'ziga nom beradi va uni to'siq emas, yo'naltiruvchi (guide rail) deb o'qiydi: dizaynda qilinadigan tanlov tizimni bir xil bo'lishga va boshqacha bo'lmaslikka majbur qiladi, va ba'zi tanlovlar aynan tizimni siz xohlagan manzilga olib borish uchun qo'yiladi.

Shundan bitta kuchli xulosa chiqadi: tizim **nima qilmasligi** ham nima qilishi kadar muhim. Xavfsiz tizim ishonchsiz tomon bilan ma'lumot almashmaydi, qulay tizim bekor qilish imkonini bermasdan uzoq hisobni boshlamaydi. Sabab tahlilga tegishli: cheklanmagan dizayn ta'rifi bo'yicha istalgan narsani qila oladi, demak uni tahlil qilishga umid qilish uchun avval cheklash kerak. Kitobning misoli tanish: Android kodning tizim servislariga kirishini cheklaydi, shuning uchun internetga chiqmoqchi bo'lgan kod buni e'lon qilishga majbur va foydalanuvchi ilovani ishga tushirishdan oldin shu xossani ko'ra oladi.

Cheklovning to'rt foydasi alohida sanalgan va ularning har biri arxitektorning kundalik ishiga tegadi.

- **Tajribani uzatadi.** Katta tajribali injener domenni nozik tushunadi va bu bilimni to'liq uzatish uzoq vaqt oladi. Dizaynga qo'yilgan cheklov boshqalarni qabul qilinadigan yechimga yo'naltiradi, bilimni to'liq uzatmasdan.
- **Conceptual integrity beradi.** Brooks ning fikri: izchil qo'llangan bitta yaxshi g'oya tizim bo'ylab sochilgan bir necha ajoyib g'oyadan afzal. D'Souza ning formulasi esa qisqaroq: arxitektura cheklovi "keraksiz ijodkorlikni" kamaytiradi va ijodkorlikni haqiqatan kerak bo'lgan joyga qoldiradi.
- **Murakkablikni kamaytiradi.** Cheklanmagan tizim o'xshash ishlarni turli joyda turlicha bajaradi va tushunish uchun mayda tafsilotlarni o'zlashtirishni talab qiladi. Cheklov buni kesib tashlaydi va tayanadigan narsa beradi: agar ma'lumot faqat bazaga saqlanadigan bo'lsa, uni qayerdan izlashni bilasiz.
- **Runtime xulqni oydinlashtiradi.** Manba kodini ko'rish mumkin, lekin uning ish vaqtida qanday xulq qilishini oldindan aytish qiyin. Kodni shunday cheklash mumkin, ish vaqtidagi xulqi ko'rinib turadi.

Cheklov bepul emas: u boshqa yechimlarni yopadi va siz yolg'iz dasturchi bo'lmasangiz, boshqalar o'ylab topishi mumkin bo'lgan yechimlarni ham oldindan rad etadi. Shu sababli kitob kiritish tartibini beradi va u to'rt qadam.

1. **Cheklovsiz boshlanadi.** Dastlabki holat bo'sh ro'yxat, taxmin qilingan qoidalar to'plami emas.
2. **Tizim maqsadlari aniqlanadi.** Masalan boshqa tizimlar bilan ishlash, yuqori xavfsizlik yoki tezlik. Bu maqsadlar arxitektura driver lari bilan ustma-ust tushadi.
3. **"Qanday muvaffaqiyatsiz bo'lishi mumkin" deb so'raladi.** Maqsadga qanday erishiladi, tizim maqsadini qanday bajarmay qolishi mumkin, qaysi cheklov uni muvaffaqiyatga yo'naltiradi, bu cheklov qanchalik og'ir va kelishuvlari nima.
4. **Keyin cheklov qo'yiladi**, ya'ni kerakli xossa, sifat yoki riskni ta'minlaydigan cheklov tanlanadi.

Tartibning yo'nalishi ongli: u kafolat tomoniga emas, erkinlik tomoniga xato qiladi. Kitobning kuzatuvi shu bilan bog'liq, agar shu jarayon kuzatilsa ko'p holda arxitektura uslubi tanlanadi, chunki uslublarning cheklovi nisbatan yumshoq, lekin loyihani maqsadga erishish uchun to'g'ri poydevorga qo'yadi; qattiq talabli loyihada esa qattiqroq cheklov kiritiladi.

Amalda bu shu bobdagi ArchUnit qoidalariga aniq ta'sir qiladi: qoida avval yozilmaydi. Avval maqsad ("domen kodi web freymvorkiga bog'lanmasin, chunki API o'zgarishi migratsiya talab qilmasligi kerak"), keyin nosozlik ssenariysi ("qulaylik uchun entity to'g'ridan to'g'ri controller ga qaytariladi"), keyin qoida. Teskari tartib qoidani hali mavjud bo'lmagan chegarani qotirib qo'yadigan to'siqqa aylantiradi ([5.15](#515-yuqoridan-pastga-va-pastdan-yuqoriga-bogliqlik-grafi-loyihalanmaydi-osadi) dagi eslatma bilan bir xil mantiq).

## 5.21 Har darajada hikoya: ierarxiya, element soni va domen otlari

Chegara qo'yilgandan keyin keladigan savol: nechta chegara va qaysi darajada. Fairbanks javobni tushunarlilik tilida beradi: tizim har darajada hikoya aytadigan qilib tuzilsin, ya'ni tizimni bilmagan dasturchini istalgan darajaga tushirganda u ma'no topa olsin, cho'kib ketmasin. Hikoya qurishning to'rt yo'riqnomasi sanalgan va ular ketma-ket qo'llanadi.

1. **Elementlarni ichma-ich joylab** abstraksiya darajalari yaratiladi (asosan modul, komponent va muhit elementlari).
2. **Har darajadagi element soni cheklanadi.**
3. **Har elementga yaxlit maqsad beriladi.**
4. **Har element inkapsulyatsiyalanadi** va keraksiz ichki tafsilotni ko'rsatmaydi.

Shu to'rttasi har darajada bajarilsa, dasturchi ko'zi tushadigan joyda mantiqiy miqdordagi element ko'radi va ular qanday birga ishlashi haqida hikoyani o'zi tiklaydi. Foydasi kognitiv, texnik emas: katta tizimda masshtab bilan ishlash mumkin bo'ladi, quyi komponentlar qora quti sifatida qabul qilinadi va bir vaqtda tushunilishi kerak bo'lgan murakkablik chegaralanadi.

Element sonining o'zi uchun kitob ochiq evristika beradi: bitta abstraksiya darajasida mantiqiy miqdor taxminan 5 dan 50 gacha, 50 esa allaqachon juda katta. Ya'ni komponent odatda 5 dan 50 gacha quyi komponent yoki sinfdan, modul esa 5 dan 50 gacha quyi modul yoki fayldan iborat bo'ladi. Qoida ikki tomonga ishlaydi: 50 ga yaqinlashganda sonni pasaytirish uchun refaktoring qilinadi, element juda kam bo'lsa esa darajalarni birlashtirib "o'rta menejerlarni yo'q qilish" kerak. Ikkinchi tomoni muhim, chunki ko'p daraja bepul emas: ierarxiyani ushlab turish byurokratik yuk va uni bog' kabi parvarishlash kerak, shuning uchun kognitiv foyda va texnik xizmat narxi o'rtasida kelishuv qilinadi.

Darajalar ichida nimani element qilish kerak degan savolga esa model-in-code printsipi javob beradi va uning asosi oddiy kuzatuv: domendagi otlar fe'llardan sekinroq o'zgaradi. Shuning uchun sinflarni domen turlariga (`Account`, `Address`, `Order`) moslash, funksional yoki protsedural dasturda bo'lgani kabi fe'llarga (amallarga) moslashdan kam churn beradi. Kitob halol eslatma qo'shadi: fe'llar tezroq o'zgarishini ko'rsatish qiyin, va nazorat qilingan tajriba yo'q, printsipning asosiy dalili uning dasturchilar orasida uzluksiz mashhurligi. Ikkinchi dalil kuchliroq: kodni o'qiyotgan dasturchi domen turlarini kodning o'zidan chiqarib oladi, bu tushunishga va evolyutsiyaga to'g'ridan to'g'ri yordam beradi. Shu sababli [5.5](#55-koheziya-nima-birga-ozgarsa-birga-tursin) dagi xususiyat bo'yicha paketlash tanlovi tasodifiy emas: paket nomlari domen otlari bo'lsa, daraja o'zi hikoya aytadi.

```java
// Daraja 1: domen otlari paket bo'ladi (5-50 ta), ierarxiya shu yerdan boshlanadi.
// com.shop.order
// com.shop.payment
// com.shop.inventory

// Daraja 2: paket ichida yana domen otlari, amal nomlari emas.
// com/shop/order/Order.java              otdan: entity
// com/shop/order/OrderCancellation.java  otdan: amalni nomlagan tur
// com/shop/order/spi/PaymentAuthorizer.java

// Qizil bayroq: amal nomi paket bo'lsa daraja hikoya aytmaydi.
// com.shop.create, com.shop.validate, com.shop.send  <- fe'llar bo'yicha bo'lish
```

## 5.22 Dekompozitsiya strategiyasini ongli tanlash: katalog va ADD

Loyiha oxirida qo'lda modul va komponentlar bo'ladi, ularning ichida yana modul, komponent va oxirida obyektlar. Bu bo'linishlar qanday tanlanadi degan savolga ko'p dasturchi "intuitsiya bilan" deb javob beradi. Fairbanks shu javobni almashtirish uchun strategiyalar katalogini beradi, maqsadi aniq: tajribali dasturchilarning strategiyalarini bilish taraqqiyotni tezlashtiradi va dizayn sifatini ko'taradi. Katalog quyidagicha va uning qiymati har birining qaysi elementni **dominant jihat** qilib olishida.

| Strategiya | Elementlar qayerdan keladi | Qachon tanlanadi |
|---|---|---|
| Funksionallik | bog'liq funksiyalar to'dasi | eng ko'rinadigan yo'l; sifat atributlari ekstremal bo'lmagan holatda yetarli |
| Archetype | domendagi asosiy turlar (`Contact`, `Advertisement`, `User`) | tur mustaqil mavjudligi va boshqa turga majburiy bog'lanishi kam bo'lsa |
| Arxitektura uslubi | uslub belgilagan nomlangan elementlar (filter, pipe) | sifat atributi dominant bo'lganda |
| Attribute Driven Design | sifat atributi jadvalidan olingan tactic lar | katta tizimda sifat atributi talabi qattiq bo'lsa |
| Port bo'yicha | har portga bitta element yoki mediator | kirish turlarini ajratish kerak bo'lsa (a'zo va a'zo bo'lmagan) |
| Ortogonal abstraksiya | boshqa domendan olingan formalizm (graf, matritsa) | muammoni o'rganilgan domenga o'girish mumkin bo'lsa |
| Jigsaw puzzle | mavjud komponentlar, qolgani yelim | mavjud qismlardan qaytish mumkin bo'lmasa |

Katalogdan ikki qator alohida izoh talab qiladi.

**Arxitektura uslubini dominant jihat qilish sifat atributiga eng qisqa yo'l.** Sababi: har uslubning o'zi rag'batlantiradigan ma'lum xossalari bor, masalan pipe-and-filter modifiability ni beradi. Kitob darajalarni aralashtirishga ham ruxsat beradi va bu amalda eng ko'p uchraydigan shakl: birinchi darajada bitta uslub (3-tier: interfeys, biznes mantiq, saqlash), keyin shu uslubning bitta komponenti ichida boshqa jihat bo'yicha, masalan funksionallik bo'yicha bo'lish. Spring loyihasida bu tanish ko'rinadi: tashqi daraja qatlamlar, biznes mantiq qatlami ichida esa `order`, `payment`, `inventory`.

**ADD katalogdagi boshqa strategiyalardan bir narsa bilan farq qiladi**, va bu farq jadvalga tayanish. Jarayonning o'zi uch qadam: (1) dekompozitsiya qilinadigan modulni tanlash, (2) modulni aniqlashtirish, ya'ni arxitektura driver larini tanlash, mos pattern ni tanlash yoki o'ylab topish, modullar yaratib mas'uliyatlarni taqsimlash, modul interfeyslarini belgilash, funksionallik va sifat atributi ssenariylarini tekshirish, (3) har modul uchun takrorlash. Uslubga asoslangan oddiy dekompozitsiyadan farq esa shu: ADD sifat atributini tactic larga bog'laydigan jadvaldan foydalanadi. Tactic bu dizayn patternidan kattaroq, arxitektura uslubidan kichikroq birlik, va kitobda sanalgan misollari Ping/Echo, Active Redundancy, Runtime Registration, Authenticate Users va Intrusion Detection. Jadval sifat atributidan umumiy tactic ga, undan maxsus tactic ga olib boradi, ya'ni ma'lum driver dan boshlab kerakli tactic to'plamiga chiqish mumkin bo'ladi. Shu korpusdagi mos yozuvlar: Ping/Echo va Active Redundancy uchun [7.13](07-nosozlik-haqida-fikrlash.md#713-xavfni-taqsimlash-bitta-host-bitta-fizik-quti-bitta-zona), Authenticate Users uchun [20-bob](20-spring-security-filter-chain-oauth2-jwt.md).

**Jigsaw puzzle** eng ko'p e'tibordan qoladigan va eng ko'p uchraydigan holat. Ba'zan qo'lda allaqachon bir necha quyi komponent bor va ularni qayta ishlatish istagi dizaynni yo'naltiradi: relatsion baza, vendor komponenti, oldingi loyihadan qolgan va qayta paketlanadigan kod. Bu bo'laklar talab qilingan xususiyat va sifatlarning bir qismini qoplaydi, qolganini esa yangi kod, ko'pincha connector yoki adapter shaklida to'ldiradi. Kitobning tasviri aniq: bu bo'laklari bitta to'plamdan olinmagan puzzle ni yig'ishga o'xshaydi. Tanlov yakunida ham xulosa ochiq qoldirilgan: ko'p tizim uchun istalgan dekompozitsiya qabul qilish darajasida ishlaydi, lekin sifat atributi talabiga mos tanlangani ishni osonlashtiradi, va bu talabga eng to'g'ridan to'g'ri bog'langan ikki yondashuv arxitektura uslubi va ADD.

Katalog strategiyani tanlashni beradi, lekin tanlangandan keyingi qadamlarni bermaydi. Richardson shu bo'shliqni uch qadamli jarayon bilan to'ldiradi va u servisga bo'lish uchun yozilgan. Birinchi qadam: talablardan tizim amallarini (system operation) chiqarish, ya'ni command va query larga ajratish, va har command ni abstrakt domen model ustida precondition va post-condition bilan spetsifikatsiya qilish. Ikkinchi qadam: ishni servislarga bo'lish. Uchinchi qadam: har servisning API sini, ya'ni unga ko'chgan amallar to'plamini va servislar orasidagi hamkorlikni aniqlash (Chris Richardson, *Microservices Patterns*, Manning, 2019, 2-bob, 46-bet). Kitob jarayonning tabiatini ham aytadi va bu muhim: u mexanik emas, iterativ va ijodiy, ya'ni ikkinchi qadamdagi chegara birinchi qadamdagi post-condition larni qayta ko'rishga majbur qilishi normal holat.

Birinchi qadamning qiymati eng ko'p e'tibordan qoladi. Amallarni precondition va post-condition bilan yozish chegarani tanlashdan OLDIN tranzaksiya talabini ko'rsatadi: ikki amalning post-condition i bitta invariant ga tegsa, ularni ikki servisga ajratish [saga](../patterns/14-microservices-patternlari.md#149-saga-orkestratsiya-saga-orchestration) majburiyatini keltiradi, va bu qaror chegara chizilgandan keyin emas, chizilayotganda ko'rinishi kerak. Shu sababli jarayon tartibi almashtirilmaydi: avval amallar, keyin chegara, keyin API.

Oxirgi va eng noqulay haqiqat: ba'zi masalalar tanlangan dekompozitsiyani kesib o'tadi va uni ifodalash qiyin bo'ladi. Fairbanks konkurentlikni aynan shunday masala deb ataydi. Toza varaqdan boshlanadigan dizaynda thread va jarayonlarni komponent chegarasiga mukammal moslash mumkin bo'lishi ham mumkin, shunda komponent va connector larni konkurentlikni ko'rsatish uchun annotatsiyalash yetadi. Lekin masala dekompozitsiyani kesib o'tishi bilan uni ifodalashda muammo paydo bo'ladi, va kitobning kuzatuvi bo'yicha konkurentlik bunda ayniqsa qiyin. Gorizontal masshtablanish ham shu toifada. Amaliy natija: dekompozitsiya strategiyasi tanlangandan keyin kesib o'tadigan masalalar ro'yxati alohida yuritiladi va ular diagrammada emas, [7-bob](07-nosozlik-haqida-fikrlash.md) va [11-bob](11-concurrency-thread-lock-atomic-happens.md) dagi apparat bilan hal qilinadi; dekompozitsiyani ularga moslashtirish uchun buzish deyarli har doim xato.

## 5.23 Amalda qo'llash

- [ ] Git tarixidan oxirgi 6 oylik o'zgarish zichligini paket bo'yicha hisoblab chiqing va eng ko'p o'zgaradigan 5 paketni chegara nomzodi sifatida belgilang.
- [ ] Loyihadagi har bir interfeysni ko'rib chiqing va implementatsiyasi bitta bo'lganlarini ro'yxatga oling, ularning qanchasi haqiqatan kerak ekanini qaror qiling.
- [ ] `boolean` yoki `Map<String, Object>` parametri bor public metodlarni toping va har birini aniq nomli alohida metodga ajratish rejasini yozing.
- [ ] Domen paketidan `jakarta.persistence`, `org.springframework.web` va Jackson importlarini qidirib, topilganlarini ro'yxatga oling.
- [ ] Bog'liqlik yo'nalishini tekshiradigan kamida 2 ta arxitektura qoidasini CI ga qo'shing va uni buzadigan mavjud holatlarni vaqtincha ro'yxat sifatida qayd qilib qo'ying.
- [ ] Ma'lumotlar bazasida har bir modul uchun alohida sxema va alohida rol yarating, keyin boshqa sxemalarga `SELECT` ruxsatini bekor qiling.
- [ ] Modullar o'rtasidagi har bir sinxron chaqiruvni ro'yxatga olib, har biri uchun timeout qiymatini yozib qo'ying va asinxron qilish mumkin bo'lganlarini belgilang.
- [ ] `common` yoki `shared` modulidagi sinflarni sanab chiqing va o'zgarmas tiplardan boshqa hammasini egasi bor modulga ko'chirish rejasini tuzing.
- [ ] Hozir ikkilanayotgan chegaralar uchun qisman chegara shaklini tanlab, tanlovni ADR da to'liq chegaraga o'tish signali bilan yozib qo'ying.

## Manbalar

- John Ousterhout, *A Philosophy of Software Design*, 1-nashr (v1.0), Yaknyam Press, 2018, 4.3 - abstraksiya ta'rifi ("muhim bo'lmagan tafsilotlar olib tashlangan soddalashtirilgan ko'rinish") va yolg'on abstraksiya; 4.5 - yuzaki modul, interfeysi mazmuniga nisbatan murakkab
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 6.1 va 6.5 - modulni "birmuncha umumiy" qilish; metod sonini kamaytirish uchun argument qo'shish soddalashtirish emasligi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 9.3-9.4 - takrorlanish qizil bayrog'i ("to'g'ri abstraksiya topilmagan"), umumiy va maxsus maqsadli kodni ajratish
- Robert C. Martin, *Clean Architecture*, 10-bob - ISP: iste'molchini kerak bo'lmagan narsaga bog'lamaslik, keraksiz yukning qayta deploy narxi
- Robert C. Martin, *Clean Architecture*, 11-bob - DIP: bog'liqlik faqat abstraksiyalarga, o'zgaruvchan konkret sinfga bog'lanmaslik, interfeys implementatsiyadan kam o'zgarishi
- Robert C. Martin, *Clean Architecture*, 13-bob - CCP: bir xil sababdan va bir vaqtda o'zgaradigan sinflarni birga yig'ish; CRP: umumiy modulga keraksiz narsa solmaslik
- Robert C. Martin, *Clean Architecture*, 17, 18-boblar - chegara chizish va chegara anatomiyasi
- Robert C. Martin, *Clean Architecture*, 19-bob - siyosat va daraja, bog'liqlik yo'nalishi
- Robert C. Martin, *Clean Architecture*, 24-bob - qisman chegaraning uchta shakli: oxirgi qadamni qoldirish, bir tomonli chegara, facade
- Robert C. Martin, *Clean Code*, 3-bob - `boolean` flag parametri yomon amaliyot, chunki metod bir nechta ish qilayotganini oshkor qiladi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 3-bob - koheziya darajalari (funksional dan tasodifiygacha) va koheziyaning o'lchov sifatida aniq emasligi; Page-Jones ning connascence taksonomiyasi: statik (nom, tur, ma'no, joylashuv, algoritm) va dinamik (bajarilish, vaqt, qiymat, identlik)
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 2-bob (27-30 va 38-40-betlar) - statik va dinamik bog'liqlik farqi, arxitektura kvanti, aloqa shaklini tanlash nimaga ta'sir qilishi
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 6-bob (151-161-betlar) - monolit bazani ajratish qadamlari, sxemani ajratish ulanishlarni ajratishdan oldin
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 7-bob (191-192-betlar) - kod o'zgarish tezligi (code volatility) va o'zgarish tezligiga asoslangan dekompozitsiya, o'lchov manbasi versiya nazorati
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 8-bob (224-bet) - mayda umumiy kutubxonalar bog'liqlik matritsasini "taqsimlangan loyqa to'p" ga aylantirishi
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 9-bob (250-bet) - jadvalga yozadigan servis uning egasi; birgalikda va umumiy egalik bu qoidani murakkablashtirishi
- Martin Fowler, *Refactoring*, Addison-Wesley, 1999, 2-bob - "uchlik qoidasi" (Don Roberts): uchinchi marta refaktoring qilinadi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 2-bob (57-bet) - dizayn variantini tanlashda refaktoringni oldindan tasavvur qilish: keyin o'tish oson bo'lsa eng soddasini olish, oson bo'lmasa dizaynga ko'proq kuch sarflash
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 2-bob (46-bet) - arxitekturani aniqlashning uch qadami: talablardan tizim amallarini (command va query) chiqarish va har command ni abstrakt domen model ustida precondition hamda post-condition bilan spetsifikatsiya qilish, keyin servislarga bo'lish, keyin servis API larini aniqlash; jarayonning mexanik emas, iterativ va ijodiy bo'lishi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer BV, 2023, 25-bob, 367-368-betlar - masshtablanishning ikki ma'nosi (yangi biznes use case lari va yuk), to'lov usullari misoli va kengaytirish nuqtasining vaqt hisobi, framework qurish qarorini biznesning ishlash tartibi va kompaniya roadmap i belgilashi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 14-bob ("Component Coupling", "Top-Down Design" bo'limi) - komponent bog'liqlik tuzilmasi yuqoridan pastga loyihalanmasligi, u funksiya emas qurilish va texnik xizmat xaritasi ekani, grafning SRP/CCP, o'zgaruvchanlikni izolyatsiya qilish, keyin CRP va ADP bilan o'sishi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 16-bob ("Independence", "Decoupling Mode" va "Decoupling Modes (Again)" bo'limlari) - ajratishning uch rejimi (manba, deploy, servis), maqbul rejim loyiha yetilgani sayin o'zgarishi, servis darajasini standart qilib olishning narxi, servis hosil qilish imkonini ochiq qoldirib bir adres maydonida ushlab turish, rejimni teskari yo'nalishda ham o'zgartirish
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 18-bob ("Boundary Anatomy", "Threads", "Local Processes" va "Services" bo'limlari) - thread arxitektura chegarasi ham, deploy birligi ham emasligi; lokal protsess alohida adres maydonidagi kuchli chegara va aloqa socket yoki navbat orqali ketishi; ko'p tizim bir vaqtda bir nechta rejimni aralashtirishi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 25-bob ("Layers and Boundaries", "Crossing the Streams" va "Splitting the Streams" bo'limlari) - ma'lumot oqimi ikkitadan ko'p bo'lishi, oqimlarning yuqori darajadagi siyosatda yana bo'linishi, chegarani egilish nuqtasida qo'yish qoidasi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 5.3 - temporal dekompozitsiya, uning ma'lumot oqib chiqishiga olib kelishi va "Red Flag: Temporal Decomposition" qizil bayrog'i; 5.5 - HTTP so'rovini o'qish va parse qilishni ikki sinfga bo'lish misoli
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 5.2 (82-83-betlar) - dizaynning besh darajasi va quyi tizimlar o'rtasidagi aloqa qoidalarining zarurati; 5.3 (107-bet) - "markaziy boshqaruv nuqtalarini yarat" evristikasi va Plauger ning Bitta To'g'ri Joy printsipi; 5.4 (111-113-betlar) - yuqoridan pastga (dekompozitsiya) va pastdan yuqoriga (kompozitsiya) yondashuvlar
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 6-bob (132-149-betlar) - bazani bo'lish sabablari: oltita disintegrator (o'zgarish nazorati, ulanishlarni boshqarish, masshtab, nosozlikka chidamlilik, arxitektura kvanti, baza turini moslash) va ikkita integrator (ma'lumot munosabatlari, baza tranzaksiyalari); 200 ulanishli monolitdan 1000 va 1700 ulanishga o'sish hisobi, ulanish kvotasi va uni teng hamda farqli taqsimlash, 100 kvotaning masshtabdan keyin 242 ga aylanishi, bounded context shartnomasi sxemadan farq qilishi
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 9-bob (252-253-betlar) - umumiy egalik: umumiy baza yoki sxemaga qo'yish ma'lumotni bo'lishish muammolarini qaytarishi, yagona ega servis tayinlash, javob kerak bo'lmaganda doimiy navbat bilan fire-and-forget va javob kerak bo'lganda REST, gRPC yoki request-reply
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 9-bob (253-262-betlar) - birgalikda egalik va to'rt yechim: jadvalni bo'lish (DDL qadamlari, CAP tanlovi, sinxron va asinxron aloqa), ma'lumot domeni (umumiy sxema, kengroq bounded context, servis ajratilishini qayta baholash sharti), delegatsiya (birlamchi domen ustuvorligi va operatsion xarakteristika ustuvorligi, mualliflarning domen ustuvorligi tavsiyasi), servislarni birlashtirish; har to'rttasining afzallik va kamchilik jadvali
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 2-bob ("Pass-Through Coupling" bo'limi) - o'tkazuvchi bog'liqlik ta'rifi, yetkazib berish varaqasi misoli, pastdagi format o'zgarishining yuqoriga tarqalishi va uchta chiqish yo'li (oraliqni chetlab o'tish, talabni yashirish, shaffof blob), bojxona deklaratsiyasi misoli va lockstep rollout dan qutulish. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 3-bob ("Cohesion" bo'limi) - `Customer Maintenance` misoli va modulni bo'lish-bo'lmaslikni hal qiladigan uch savol (ikkinchi modulda faqat shu ikki amalmi, birinchi modul kattalashadimi, ajratish kuchli bog'lanish talab qiladimi)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 3-bob ("Cohesion" bo'limi) - LCOM metrikasi (maydonlarni bo'lishish orqali bog'lanmagan metod to'plamlari yig'indisi), uning umumiy utility sinflarini topishdagi foydasi va faqat strukturaviy koheziyani ko'rishdagi cheklovi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 3-bob ("Connascence Properties" bo'limi) - connascence ning uch xossasi (kuch, yaqinlik, daraja), statikni dinamikdan afzal ko'rish va ma'no bo'yicha connascence ni nom bo'yicha connascence ga aylantirish; Page-Jones ning uch qoidasi (umumiy connascence ni kamaytir, chegarani kesib o'tadiganini minimallashtir, chegara ichidagisini maksimallashtir). Qo'limizdagi nusxada chop etilgan bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 2-bob ("Domain Coupling" bo'limi) - domen bog'liqligi yengil shakl ekani, uni minimumda ushlash va bitta servisning bir nechta quyi servisga bog'lanishi u juda ko'p ish qilayotgani yoki mantiq markazlashib ketgani belgisi ekani
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 16-bob ("Defining System Boundaries" bo'limi) - servis chegarasidan yirikroq zona (jamoa servislari guruhi) ham chegara bo'lishi, zona ichidagi o'zgarish zonalar orasidagi o'zgarishdan arzonligi, jamoa tuzilmasining qiyin o'zgarishi zona nomzodini ko'rsatishi va team API orqali jamoa darajasidagi axborotni yashirish
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 8-bob (243-244-betlar) - markaziy `Customer` servisining ikki tomonlama buzilishi (entity har domenni ko'tarishi kerakligi va o'zgarishning hamma domenga urilishi); qayta foydalanish abstraksiyadan kelib, o'zgarish tezligining pastligi bilan ishga solinishi
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 10-bob (293-295-betlar) - ma'lumot domeni (umumiy sxema) o'qish uchun oxirgi yo'l ekani, jadval sxemasining shartnomaga aylanishi, tashqi kalit va baza vositalarining saqlanishi hamda butun sxemaga kirishdan kelib chiqadigan xavfsizlik riski
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 2.2 - cheklov to'siq emas yo'naltiruvchi ekani, tizim nima qilmasligi muhimligi, cheklanmagan dizaynni tahlil qilib bo'lmasligi va cheklovning to'rt foydasi (tajribani uzatish, conceptual integrity, murakkablikni kamaytirish, runtime xulqni oydinlashtirish)
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 9.7 - ish vaqtida arxitektura konfiguratsiyasini o'zgartiradigan dizayndan qochish (statik arxitektura tushunish va sifat atributi tahlili uchun oson) hamda startup va shutdown dinamikasini e'tiborsiz qoldirmaslik; 12.4 - connector ni birinchi darajali va almashtiriladigan qilish, kodda connector interfeysi yo'qligi mijozni aniq implementatsiyaga bog'lashi
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 10.5 - model-in-code printsipi, domen otlarining fe'llardan sekinroq o'zgarishi va otlarga moslashning kam churn berishi
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 11.1 - har darajada hikoya aytadigan tizim va uning to'rt yo'riqnomasi, har darajada taxminan 5 dan 50 gacha element, 50 ga yaqinlashganda refaktoring va element juda kam bo'lsa darajalarni birlashtirish
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 11.3-11.3.8 - dekompozitsiya strategiyalari katalogi (funksionallik, archetype, arxitektura uslubi, ADD, port, ortogonal abstraksiya, jigsaw puzzle), uslubni dominant jihat qilishning sifat atributiga samarasi, ADD ning uch qadami va tactic jadvali, jigsaw puzzle da mavjud komponentlarni adapter bilan to'ldirish
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 16.1 - konkurentlik va gorizontal masshtablanish kabi masalalarning tanlangan dekompozitsiyani kesib o'tishi va ularni ifodalash qiyinligi; 16.4 - cheklov kiritishning to'rt qadamli tartibi va erkinlik tomoniga xato qilish
- ESLATMA: 5.4 dagi amaliy holatlarga guruhlash (o'tkazuvchi bog'liqlik qatori ham), 5.6 dagi git buyruqlari va egalik o'lchovi, 5.9 dagi pool sozlash hisobi, 5.10 dagi belgilar ro'yxati, 5.14 dagi Spring nom belgilari ro'yxati, 5.15 dagi birinchi hafta mahsuloti haqidagi tavsiya 5.18 dagi `pg_stat_activity` so'rovi, 5.7 dagi `OrderEventPublisher` kod misoli, 5.20 oxiridagi ArchUnit tartibi haqidagi tavsiya, 5.21 dagi paket nomlari misoli va 5.23 dagi checklist shu korpusning amaliy tavsiyasi, kitobdan olingan emas

---

[&larr; 4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk](04-kod-muloqot-vositasi-nomlash-aniqlik.md) · [Mundarija](README.md) · [6. Murakkablikni boshqarish &rarr;](06-murakkablikni-boshqarish.md)
