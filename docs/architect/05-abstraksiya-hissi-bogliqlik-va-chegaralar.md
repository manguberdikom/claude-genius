<!-- doc: architect | chapter: 5 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 5. Abstraksiya hissi, bog'liqlik va chegaralar (Abstraction, Coupling and Boundaries)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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
- [5.16 Amalda qo'llash](#516-amalda-qollash)

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

Ikki holat alohida izoh talab qiladi. Ma'lumot shakli bo'yicha bog'liqlikning narxini *Clean Architecture* ning interfeys ajratish bobi bitta gapda aytadi: sizga kerak bo'lmagan yukni ko'tarib yurgan narsaga bog'lanish kutilmagan muammo keltiradi, chunki o'sha keraksiz qismdagi o'zgarish ham sizni qayta deploy qilishga majbur qiladi. Sxema bo'yicha bog'liqlik esa eng og'iri: ikki servis bitta jadvalga yozsa, hech qanday kod refaktoringi yordam bermaydi, chunki bog'liqlik ma'lumotlar bazasi darajasida (yechimi 5.9 da).

## 5.5 Koheziya: nima birga o'zgarsa, birga tursin

Koheziya bog'liqlikning teskari tomoni emas, uning sherigi. *Fundamentals of Software Architecture* koheziyani "modul qismlari bir-biriga qanchalik bog'liq" sifatida ta'riflaydi va uning darajalarini eng yaxshisidan eng yomoniga sanab beradi: funksional, ketma-ket, kommunikatsion, protsedural, vaqtga bog'liq, mantiqiy va tasodifiy koheziya. Kitob shu yerda halol ogohlantirish beradi: koheziya bog'liqlikka qaraganda kamroq aniq o'lchov, va modulning koheziya darajasini baholash ko'p holda arxitektorning qaroriga qoladi. Shu sababli amalda ishlaydigan mezon *Clean Architecture* ning Umumiy Yopilish Printsipi bo'ladi: bitta sababdan va bitta vaqtda o'zgaradigan kod bitta joyda turadi. Spring loyihalarida eng keng tarqalgan xato texnik qatlamlar bo'yicha paketlash: `controller`, `service`, `repository`, `dto`. Bu ko'rinishda chiroyli, lekin har bir biznes o'zgarishi to'rt paketga tegadi, demak koheziya past. Mantiqiy koheziyaning kanonik misoli ham shu kitobda bor va u Java dasturchisiga tanish: `StringUtils` kabi paket, ya'ni bir tipda ishlaydigan, lekin bir-biriga aloqasi yo'q statik metodlar to'plami.

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

## 5.16 Amalda qo'llash

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
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer BV, 2023, 25-bob, 367-368-betlar - masshtablanishning ikki ma'nosi (yangi biznes use case lari va yuk), to'lov usullari misoli va kengaytirish nuqtasining vaqt hisobi, framework qurish qarorini biznesning ishlash tartibi va kompaniya roadmap i belgilashi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 14-bob ("Component Coupling", "Top-Down Design" bo'limi) - komponent bog'liqlik tuzilmasi yuqoridan pastga loyihalanmasligi, u funksiya emas qurilish va texnik xizmat xaritasi ekani, grafning SRP/CCP, o'zgaruvchanlikni izolyatsiya qilish, keyin CRP va ADP bilan o'sishi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 16-bob ("Independence", "Decoupling Mode" va "Decoupling Modes (Again)" bo'limlari) - ajratishning uch rejimi (manba, deploy, servis), maqbul rejim loyiha yetilgani sayin o'zgarishi, servis darajasini standart qilib olishning narxi, servis hosil qilish imkonini ochiq qoldirib bir adres maydonida ushlab turish, rejimni teskari yo'nalishda ham o'zgartirish
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 18-bob ("Boundary Anatomy", "Threads", "Local Processes" va "Services" bo'limlari) - thread arxitektura chegarasi ham, deploy birligi ham emasligi; lokal protsess alohida adres maydonidagi kuchli chegara va aloqa socket yoki navbat orqali ketishi; ko'p tizim bir vaqtda bir nechta rejimni aralashtirishi
- Robert C. Martin, *Clean Architecture*, Prentice Hall, 2018, 25-bob ("Layers and Boundaries", "Crossing the Streams" va "Splitting the Streams" bo'limlari) - ma'lumot oqimi ikkitadan ko'p bo'lishi, oqimlarning yuqori darajadagi siyosatda yana bo'linishi, chegarani egilish nuqtasida qo'yish qoidasi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 5.3 - temporal dekompozitsiya, uning ma'lumot oqib chiqishiga olib kelishi va "Red Flag: Temporal Decomposition" qizil bayrog'i; 5.5 - HTTP so'rovini o'qish va parse qilishni ikki sinfga bo'lish misoli
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 5.2 (82-83-betlar) - dizaynning besh darajasi va quyi tizimlar o'rtasidagi aloqa qoidalarining zarurati; 5.3 (107-bet) - "markaziy boshqaruv nuqtalarini yarat" evristikasi va Plauger ning Bitta To'g'ri Joy printsipi; 5.4 (111-113-betlar) - yuqoridan pastga (dekompozitsiya) va pastdan yuqoriga (kompozitsiya) yondashuvlar
- ESLATMA: 5.4 dagi to'rtta amaliy holatga guruhlash, 5.6 dagi git buyruqlari va egalik o'lchovi, 5.9 dagi pool sozlash hisobi, 5.10 dagi belgilar ro'yxati, 5.14 dagi Spring nom belgilari ro'yxati, 5.15 dagi birinchi hafta mahsuloti haqidagi tavsiya va 5.16 dagi checklist shu korpusning amaliy tavsiyasi, kitobdan olingan emas

---

[&larr; 4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk](04-kod-muloqot-vositasi-nomlash-aniqlik.md) · [Mundarija](README.md) · [6. Murakkablikni boshqarish &rarr;](06-murakkablikni-boshqarish.md)
