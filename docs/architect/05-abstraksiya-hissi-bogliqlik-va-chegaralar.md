<!-- doc: architect | chapter: 5 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 5. Abstraksiya hissi, bog'liqlik va chegaralar (Abstraction, Coupling and Boundaries)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [5.11 Amalda qo'llash](#511-amalda-qollash)

</details>



Abstraksiya hissi deganda chiroyli ierarxiya qurish qobiliyati emas, o'zgarish qayerdan kelishini oldindan sezish tushuniladi. Arxitektor har bir interfeysni savol bilan qo'yadi: "ertaga nima o'zgaradi va o'zgarish qancha faylga tegadi?". Agar javob yo'q bo'lsa, abstraksiya hali kerak emas. Bu bobda abstraksiyaning iqtisodi, bog'liqlik mexanikasi va chegarani qayerdan o'tkazish qarori ko'rib chiqiladi.

## 5.1 Abstraksiya nima uchun qo'yiladi: o'zgarishni bitta joyga to'plash

Abstraksiyaning yagona haqiqiy vazifasi bor: o'zgarish radiusini qisqartirish. Agar QQS stavkasi o'zgarganda 14 ta faylni tahrirlash kerak bo'lsa, abstraksiya yo'q. Agar bitta sinfni tahrirlab, qolgan hamma joy avtomatik to'g'ri ishlaydigan bo'lsa, abstraksiya ishlayapti. Shu sababli abstraksiyani "qayta ishlatish uchun" emas, "o'zgarishni ushlab turish uchun" qo'yish kerak.

Amalda bu ikki xil narsani ajratishdan boshlanadi: siyosat (policy) va mexanika. To'lov summasini hisoblash siyosat, HTTP orqali provayderga murojaat qilish mexanika. Siyosat biznes talabi bilan o'zgaradi, mexanika texnologiya bilan o'zgaradi. Ikkisi bir sinfda yashasa, har bir biznes o'zgarishi texnik kodga tegib ketadi.

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

## 5.2 Erta abstraksiya va takrorlanish: qaysi biri arzonroq

Ikki xato bir xil og'ir emas. Takrorlangan kodni birlashtirish mexanik ish: IDE yordamida 20 daqiqada bajariladi va natijasi testlar bilan tekshiriladi. Noto'g'ri abstraksiyani yechish esa chaqiruvchilar zanjirini buzadi, chunki hamma allaqachon o'sha interfeysga suyangan. Shuning uchun amaliy qoida: shubha bo'lsa takrorlashni tanla.

Takrorlanishning o'zi ham bir xil emas. Tasodifiy o'xshashlik (incidental duplication) ikki joyda kod hozir o'xshash, lekin sabablari boshqa. Haqiqiy takrorlanish (real duplication) bitta biznes qoidasi ikki joyda yozilgan. Birinchisini birlashtirish zarar keltiradi, ikkinchisini birlashtirmaslik xatolikka olib keladi. Tekshirish usuli oddiy: "bu ikki joy kelasi chorakda bir xil sababdan o'zgaradimi?". Javob "yo'q" bo'lsa, qo'shmang.

Raqamli chegara ham foydali. Uchinchi marta bir xil mantiq paydo bo'lganda abstraksiya qo'yish ko'pchilik jamoada yaxshi ishlaydi. Ikkinchi marta hali ma'lumot yetarli emas, to'rtinchi marta esa kech bo'lib qoladi. Spring loyihalarida yana bitta signal bor: agar bir xil `@Transactional` + repository + mapping ketma-ketligi uch xil servisda takrorlansa, u yerda yashirin domen amali turgan bo'ladi.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Ikki joyda o'xshash kod ko'rindi | Darhol umumiy `BaseService` chiqariladi | O'zgarish sababi bir xilmi, shu tekshiriladi |
| Yangi provayder qo'shilishi mumkin | Har bir servisga interfeys yoziladi | Interfeys faqat ikkinchi haqiqiy provayder kelganda chiqariladi |
| Har bir entity uchun repository | Jenerik `CrudService<T>` qatlami | Faqat haqiqiy domen amallari e'lon qilinadi |
| DTO va entity bir xil ko'rinadi | Entity to'g'ridan to'g'ri API ga chiqariladi | API shartnomasi alohida turadi, ichki model erkin o'zgaradi |
| Ikki modulga umumiy kod kerak | `common` moduli yaratiladi va o'sadi | Faqat o'zgarmas tiplar (`Money`, `OrderId`) umumiylashtiriladi |
| Bitta metodda ikki xatti-harakat | `boolean` flag parametri qo'shiladi | Ikki alohida metod yoki ikki implementatsiya |
| Modullar o'rtasida ma'lumot kerak | Boshqa modul jadvaliga `join` qilinadi | Event yoki aniq API orqali olinadi |
| Interfeys o'zgarishi kerak | Interfeysga yangi metod qo'shiladi | Avval kim foydalanayotgani va kim egasi aniqlanadi |
| Chegara noqulaylik keltiryapti | Chegara olib tashlanadi | Chegara joyi noto'g'ri qo'yilgani tekshiriladi |

## 5.3 Noto'g'ri abstraksiya narxi va undan qaytish yo'li

Noto'g'ri abstraksiya o'zini bitta belgi bilan oshkor qiladi: yangi talab kelganda interfeysga parametr qo'shiladi. Keyin ikkinchi parametr, keyin `Map<String, Object> options`. Shu paytdan boshlab abstraksiya mantiqni yashirmaydi, balki chaqiruvchidan mantiqni bilishni talab qiladi. Chaqiruvchi `if` yozib qaysi parametrni berishni tanlay boshlaydi, demak qaror chegaradan tashqariga chiqib ketgan.

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

Narxni raqamda ko'rish uchun bitta o'lchov yetarli: noto'g'ri abstraksiyaga suyangan chaqiruvchilar soni. 3 ta chaqiruvchi bo'lsa bir kunlik ish. 30 ta chaqiruvchi va 4 ta jamoa bo'lsa bu chorak davomidagi migratsiya rejasiga aylanadi. Shuning uchun abstraksiyani jamoalar o'rtasidagi chegarada qo'yishdan oldin ikki marta o'ylash kerak.

## 5.4 Bog'liqlik turlari: ma'lumot, vaqt, joylashuv, sxema bo'yicha bog'liqlik

"Coupling" degan so'z juda umumiy. Qaror chiqarish uchun uni turlarga bo'lib ko'rish kerak, chunki har bir tur boshqa yechim talab qiladi.

Ma'lumot bo'yicha bog'liqlik: modul boshqa modulning ma'lumot shaklini biladi. Agar `OrderService` to'lov javobidagi 12 ta maydondan faqat 2 tasini ishlatsa ham, butun sinfga bog'lanib qoladi. Yechim: chegarada faqat kerakli maydonlardan iborat kichik tip e'lon qilish.

Vaqt bo'yicha bog'liqlik (temporal coupling): A modul ishlashi uchun B modul aynan shu paytda tirik bo'lishi shart. Buyurtma qabul qilish to'lov servisining sinxron javobiga bog'liq bo'lsa, to'lov servisi 2 sekundga sekinlashganda buyurtma oqimi ham to'xtaydi. Yechim: javobni kutish shart bo'lmagan joyda event yoki outbox orqali asinxron qilish, shart bo'lgan joyda esa timeout va fallback bilan aniq chegara qo'yish.

Joylashuv bo'yicha bog'liqlik: kod boshqa tomonning manzilini, port raqamini yoki topologiyasini biladi. Bu konfiguratsiya va service discovery darajasida hal qilinadi, kodda qattiq yozilmaydi.

Sxema bo'yicha bog'liqlik: eng og'iri. Ikki servis bitta jadvalni o'qiydi yoki yozadi. Bu holatda hech qanday kod refaktoringi yordam bermaydi, chunki bog'liqlik ma'lumotlar bazasi darajasida.

| Bog'liqlik turi | Qanday aniqlanadi | Qanday yumshatiladi | Qoldiq xavf |
| --- | --- | --- | --- |
| Ma'lumot | Chaqiruvchi 12 maydonli tipni import qiladi | Chegarada kichik, o'zingga tegishli tip | Mapping kodi ko'payadi |
| Vaqt | Sinxron zanjir 3 va undan ko'p servisdan o'tadi | Event, outbox, timeout va fallback | Yakuniy izchillik kechikishi |
| Joylashuv | URL va port kodda yozilgan | Config, discovery, abstraksiyalangan client | Konfiguratsiya xatosi |
| Sxema | Ikki servis bitta jadvalga yozadi | Egalik bitta servisga, qolganlarga API yoki view | Migratsiya murakkabligi |

## 5.5 Koheziya: nima birga o'zgarsa, birga tursin

Koheziya bog'liqlikning teskari tomoni emas, uning sherigi. Yuqori koheziya degani bitta sababdan o'zgaradigan kod bitta joyda turadi. Spring loyihalarida eng keng tarqalgan xato texnik qatlamlar bo'yicha paketlash: `controller`, `service`, `repository`, `dto`. Bu ko'rinishda chiroyli, lekin har bir biznes o'zgarishi to'rt paketga tegadi, demak koheziya past.

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

Chegarani domen diagrammasidan emas, ikki o'lchovdan chiqarish kerak: nima qanchalik tez o'zgaradi va kim javobgar. Bir xil tezlikda va bir xil jamoa qo'li bilan o'zgaradigan kod bitta modulda yashashi kerak. Haftada o'zgaradigan aksiya qoidalari va yilda bir o'zgaradigan buxgalteriya hisobi bir modulda bo'lmasligi lozim.

O'zgarish tezligini taxmin qilish shart emas, uni git tarixidan o'lchash mumkin. Bu arxitektor uchun eng arzon ma'lumot manbai.

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

## 5.7 Interfeys kimga tegishli: foydalanuvchi tomonda e'lon qilish

Klassik xato: interfeys implementatsiya bilan bir paketda turadi. Bunda interfeys "men nimani taklif qilaman" degan ma'noni beradi. To'g'ri yondashuv teskari: interfeysni muhtoj tomon e'lon qiladi va unda "menga nima kerak" yoziladi. Shunda interfeys ehtiyoj bilan o'zgaradi, provayder bilan emas.

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

Bu joylashuvning yana bir foydasi bor: bog'liqlik yo'nalishi avtomatik to'g'ri bo'lib qoladi. `payment.acme` paketi `order.spi` paketini biladi, teskarisi yo'q. Spring konteyner `PaymentAuthorizer` ni injeksiya qilganda implementatsiya qaysi paketda ekani ahamiyatsiz, chunki bog'lanish tip bo'yicha amalga oshadi.

## 5.8 Bog'liqlik yo'nalishini boshqarish: ichki qatlam tashqarini bilmasin

Qatlamlar haqida gapirishning foydali usuli: import yo'nalishi. Domen kodida `jakarta.persistence`, `org.springframework.web` yoki `com.fasterxml.jackson` importlari paydo bo'lsa, chegara allaqachon buzilgan. Bu holat sekin-asta keladi: avval `@JsonIgnore` entity ga qo'yiladi, keyin `@Column` nomi API shartnomasiga ta'sir qiladi, va oxirida API ni o'zgartirish uchun migratsiya yozish kerak bo'ladi.

Bu qoidani sharhda yozib qo'yish yetarli emas, uni avtomatik tekshirish kerak. ArchUnit shu uchun mavjud va u [testlash qo'llanmasidagi](../testing/README.md) arxitektura qoidalari bo'limida batafsil ko'rsatilgan. Bu yerda faqat qoida shakli muhim.

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

Yo'nalishni buzadigan eng ko'p uchraydigan sabab qulaylik. Developer hisobot uchun buyurtma entity sini to'g'ridan to'g'ri olmoqchi bo'ladi, chunki shunday qilish 5 daqiqa, API orqali olish 2 soat. Arxitektorning ishi shu tanlovni arzonlashtirish: hisobot uchun aniq o'qish interfeysi va kerakli ma'lumotni beradigan proyeksiya oldindan tayyor bo'lsa, qoidani buzish ehtiyoji qolmaydi.

## 5.9 Sxema chegarasi: boshqa servisning jadvaliga tegmaslik qoidasi

Kod chegarasini ArchUnit saqlaydi, lekin ma'lumotlar bazasi chegarasini hech kim saqlamaydi. Agar ikki servis bitta `orders` jadvalini o'qisa, ularni mustaqil deploy qilish imkoni yo'q: ustun nomini o'zgartirish ikkinchi servisni sindiradi. Shuning uchun har bir modul yoki servis o'z jadvallarining yagona egasi bo'lishi kerak.

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

Migratsiyalar ham egalik qoidasiga bo'ysunadi. Har bir servis faqat o'z sxemasiga migratsiya qiladi, va bu konfiguratsiyada aniq yozilishi kerak.

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
      maximum-pool-size: 20       # 4 instance x 20 = 80, PostgreSQL max_connections 200 dan past
      connection-timeout: 3000    # ms
  jpa:
    properties:
      hibernate:
        default_schema: order_svc
```

Pool o'lchami ham chegara masalasi. Har bir servis o'z pooliga ega bo'lishi kerak, chunki umumiy pool bir servisning sekin so'rovini boshqasining muammosiga aylantiradi. 4 ta instance va har birida 20 ulanish 80 ulanishni beradi, va bu `max_connections` 200 bo'lgan serverda xavfsiz. Pool to'lib qolsa `connection-timeout` 3 sekundda xato qaytaradi, bu cheksiz kutishdan afzal.

## 5.10 Chegara noto'g'ri qo'yilganini bildiradigan belgilar

Chegara to'g'ri yoki noto'g'ri ekanini nazariyadan emas, kundalik ishlashdan bilib olish mumkin. Quyidagi belgilar aniq va o'lchanadigan.

Birinchi belgi: bitta talab uchun ikki yoki uch repozitoriyga o'zgartirish kiritiladi va ularni birgalikda deploy qilish kerak. Bu "taqsimlangan monolit" ning klassik ko'rinishi. Ikkinchi belgi: pull request lar doim ikki jamoaning reviewi ni kutadi. Uchinchi belgi: integratsiya testlarisiz hech narsani ishonch bilan o'zgartirib bo'lmaydi, chunki mantiq chegaralar bo'ylab tarqalgan.

To'rtinchi belgi texnik: bitta API chaqiruvi ichida 4 va undan ortiq sinxron tashqi murojaat bo'lsa. Har biri taxminan 50 ms bo'lsa ham, yakuniy p99 latency 500 ms dan oshadi va mavjudlik ko'paytmaga aylanadi. Beshinchi belgi: "shared" yoki "common" moduli loyihada eng tez o'sadigan modul bo'lsa. Bu modul chegara emas, chegaradan qochish joyi.

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

## 5.11 Amalda qo'llash

- [ ] Git tarixidan oxirgi 6 oylik o'zgarish zichligini paket bo'yicha hisoblab chiqing va eng ko'p o'zgaradigan 5 paketni chegara nomzodi sifatida belgilang.
- [ ] Loyihadagi har bir interfeysni ko'rib chiqing va implementatsiyasi bitta bo'lganlarini ro'yxatga oling, ularning qanchasi haqiqatan kerak ekanini qaror qiling.
- [ ] `boolean` yoki `Map<String, Object>` parametri bor public metodlarni toping va har birini aniq nomli alohida metodga ajratish rejasini yozing.
- [ ] Domen paketidan `jakarta.persistence`, `org.springframework.web` va Jackson importlarini qidirib, topilganlarini ro'yxatga oling.
- [ ] Bog'liqlik yo'nalishini tekshiradigan kamida 2 ta arxitektura qoidasini CI ga qo'shing va uni buzadigan mavjud holatlarni vaqtincha ro'yxat sifatida qayd qilib qo'ying.
- [ ] Ma'lumotlar bazasida har bir modul uchun alohida sxema va alohida rol yarating, keyin boshqa sxemalarga `SELECT` ruxsatini bekor qiling.
- [ ] Modullar o'rtasidagi har bir sinxron chaqiruvni ro'yxatga olib, har biri uchun timeout qiymatini yozib qo'ying va asinxron qilish mumkin bo'lganlarini belgilang.
- [ ] `common` yoki `shared` modulidagi sinflarni sanab chiqing va o'zgarmas tiplardan boshqa hammasini egasi bor modulga ko'chirish rejasini tuzing.

---

[&larr; 4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk](04-kod-muloqot-vositasi-nomlash-aniqlik.md) · [Mundarija](README.md) · [6. Murakkablikni boshqarish &rarr;](06-murakkablikni-boshqarish.md)
