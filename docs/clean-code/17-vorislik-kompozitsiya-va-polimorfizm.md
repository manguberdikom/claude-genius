<!-- doc: clean-code | chapter: 17 | part: V. Obyekt, ma'lumot va holat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 17. Vorislik, kompozitsiya va polimorfizm mexanikasi (Inheritance Mechanics)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [17.1 Vorislik uchun dizayn qilish yoki `final` qilish](#171-vorislik-uchun-dizayn-qilish-yoki-final-qilish)
- [17.2 Konstruktorda override qilinadigan metodni chaqirish](#172-konstruktorda-override-qilinadigan-metodni-chaqirish)
- [17.3 `protected` maydon va buzilgan inkapsulyatsiya](#173-protected-maydon-va-buzilgan-inkapsulyatsiya)
- [17.4 `super` chaqiruvi va uni unutish](#174-super-chaqiruvi-va-uni-unutish)
- [17.5 Bazaviy sinfning voris sinfga bog'liqligi](#175-bazaviy-sinfning-voris-sinfga-bogliqligi)
- [17.6 Rad etilgan meros va interfeysni bo'lish](#176-rad-etilgan-meros-va-interfeysni-bolish)
- [17.7 Abstrakt sinf va interfeys tanlovi, `default` metodlar](#177-abstrakt-sinf-va-interfeys-tanlovi-default-metodlar)
- [17.8 Konstantalarni interfeysdan voris olish](#178-konstantalarni-interfeysdan-voris-olish)
- [17.9 Delegatsiya bilan vorislikni almashtirish](#179-delegatsiya-bilan-vorislikni-almashtirish)
- [17.10 Teglangan sinf o'rniga ierarxiya yoki `sealed`](#1710-teglangan-sinf-orniga-ierarxiya-yoki-sealed)
- [17.11 Amalda qo'llash](#1711-amalda-qollash)

</details>


"Vorislikdan ustun kompozitsiya" printsipi [patternlar hujjatidagi](../patterns/README.md) vorislikdan ustun kompozitsiya printsipida berilgan. Bu bobda vorislik **ishlatilganda** uni to'g'ri bajarish mexanikasi: vorislik uchun dizayn, konstruktor tuzog'i, `protected` muammosi, va vorislikdan kompozitsiyaga o'tish yo'li.

## 17.1 Vorislik uchun dizayn qilish yoki `final` qilish

Sinf uch holatdan birida bo'lishi kerak: vorislik uchun mo'ljallangan va hujjatlashtirilgan, `final`, yoki interfeys. "Vorislik mumkin, lekin o'ylanmagan" to'rtinchi holat - xato manbasi, chunki voris sinf bazaviy sinfning ichki qoidalarini bilmaydi va ularni buzadi.

Shu sababli amaliy standart: **sinf `final` bo'lishi standart holat**, vorislik esa ongli qaror. Spring kontekstida istisno bor: `@Configuration` sinflari va CGLIB proxy qilinadigan beanlar `final` bo'lmaydi (26.1).

```java
// yaxshi: standart holat
public final class SettlementService { ... }

// yaxshi: vorislik uchun ataylab ochilgan va hujjatlashtirilgan
/**
 * Voris sinf uchun: {@link #validate(SettlementRow)} ni override qilish mumkin.
 * Bu metod {@link #importFile(Path)} ichidan har bir qator uchun chaqiriladi
 * va istisno tashlamasligi kerak - yaroqsiz qator {@code false} bilan belgilanadi.
 * Konstruktor ichidan override qilinadigan metod chaqirilmaydi.
 */
public abstract class AbstractSettlementImporter { ... }
```

## 17.2 Konstruktorda override qilinadigan metodni chaqirish

Bu Java dagi eng nozik vorislik xatosi. Bazaviy sinf konstruktori override qilinadigan metodni chaqirsa, u **voris sinf maydonlari hali tayinlanmaganda** ishga tushadi va `null` yoki nol qiymat ko'radi.

```java
// yomon: natija NullPointerException yoki 0
public class Importer {
    public Importer() {
        configure();                 // voris versiyasi chaqiriladi
    }
    protected void configure() { }
}

public class CsvImporter extends Importer {
    private final char delimiter = ';';     // hali tayinlanmagan!
    @Override protected void configure() {
        System.out.println(delimiter);       // 0 (nol belgi) chiqadi
    }
}

// yaxshi: sozlash konstruktordan tashqarida, yoki shablon parametr bilan
public class Importer {
    private final ImportSettings settings;
    protected Importer(ImportSettings settings) {
        this.settings = Objects.requireNonNull(settings);
    }
}
```

Xuddi shu qoida `clone` va `readObject` ga tegishli: ikkisi ham konstruktor rolini bajaradi.

## 17.3 `protected` maydon va buzilgan inkapsulyatsiya

`protected` maydon voris sinflarga ichki holatni to'g'ridan-to'g'ri o'zgartirish imkonini beradi, ya'ni bazaviy sinf o'z invariantini himoya qila olmaydi. Natijada bazaviy sinfni refaktoring qilish imkonsiz bo'lib qoladi: u maydonlarni o'zgartirsa, barcha voris sinflar buziladi.

```java
// yomon: voris sinf holatni to'g'ridan-to'g'ri buzadi
public abstract class AbstractBatch {
    protected List<Row> rows = new ArrayList<>();
    protected int processed;
}

// yaxshi: ichki holat private, voris sinfga protected metod berilgan
public abstract class AbstractBatch {

    private final List<Row> rows = new ArrayList<>();
    private int processed;

    protected final void recordProcessed(Row row) {    // final: shartnoma buzilmaydi
        rows.add(row);
        processed++;
    }

    protected final int processedCount() { return processed; }
}
```

Qoida: `protected` maydon bo'lmaydi; `protected` metod bo'lishi mumkin va u `final` bo'lishi afzal.

## 17.4 `super` chaqiruvi va uni unutish

Agar override qilingan metod `super.method()` ni chaqirishi **shart** bo'lsa, bu yashirin shartnoma va u buziladi: kimdir chaqirmay qo'yadi va xato uzoqda chiqadi.

To'g'ri yechim - shablon metod (template method) bilan tuzilishni teskari aylantirish: bazaviy sinf `final` metodda tartibni ushlaydi va voris sinfga faqat bo'sh joyni beradi.

```java
// yomon: super ni chaqirish majburiyati izohda
public void process(Row row) {
    super.process(row);     // voris buni unutsa, audit yozilmaydi
    doWork(row);
}

// yaxshi: tartib bazaviy sinfda, voris faqat bo'shliqni to'ldiradi
public abstract class AbstractProcessor {

    public final void process(Row row) {     // final: tartib buzilmaydi
        audit(row);
        handle(row);                         // voris shu metodni yozadi
        markDone(row);
    }

    protected abstract void handle(Row row);
}
```

## 17.5 Bazaviy sinfning voris sinfga bog'liqligi

Bazaviy sinf voris sinf nomini bilsa (`if (this instanceof CsvImporter)`), ierarxiya teskari aylangan: eng barqaror bo'lishi kerak bo'lgan sinf eng o'zgaruvchan sinfga bog'langan. Har bir yangi voris bazaviy sinfni o'zgartirishni talab qiladi.

```java
// yomon: bazaviy sinf vorislarini sanaydi
protected String separator() {
    if (this instanceof CsvImporter) return ",";
    if (this instanceof TsvImporter) return "\t";
    return ";";
}

// yaxshi: har bir voris o'zini aytadi
protected abstract String separator();
```

## 17.6 Rad etilgan meros va interfeysni bo'lish

Rad etilgan meros (refused bequest) - voris sinf bazaviy sinfdan olgan metodlarning bir qismini ishlatmaydi yoki `UnsupportedOperationException` tashlaydi. Bu Liskov printsipining buzilishi va interfeys juda keng ekanining belgisi.

```java
// yomon: voris sinf merosni rad etadi
public class ReadOnlyOrderRepository extends JpaOrderRepository {
    @Override public Order save(Order order) {
        throw new UnsupportedOperationException("faqat o'qish");
    }
}

// yaxshi: interfeys bo'lingan (Interface Segregation)
public interface OrderFinder { Optional<Order> findById(OrderId id); }
public interface OrderWriter { Order save(Order order); }

public class JpaOrderRepository implements OrderFinder, OrderWriter { ... }
public class CachedOrderFinder implements OrderFinder { ... }
```

## 17.7 Abstrakt sinf va interfeys tanlovi, `default` metodlar

Tanlov mezoni oddiy: **holat** kerak bo'lsa abstrakt sinf, faqat shartnoma kerak bo'lsa interfeys. Java da bir sinf bitta bazaviy sinfdan voris oladi, lekin ko'p interfeys amalga oshiradi, shuning uchun interfeys moslashuvchanroq.

`default` metodlar interfeysga xatti-harakat qo'shish imkonini beradi, lekin ularni ehtiyotkorlik bilan ishlatish kerak: ular holatga kira olmaydi, va ikki interfeys bir xil `default` metod bersa konflikt bo'ladi.

Uchinchi ehtiyot nuqtasi muhimroq: chiqarilgan interfeysga `default` metod qo'shish mavjud implementatsiyalarni **jim** buzishi mumkin. Kompilyatsiya o'tadi, chunki metod tayyor, lekin implementatsiya shu metodning invariantini bilmaydi. Platformaning o'zida shu holat bo'lgan: `Collection.removeIf` Java 8 da `default` bo'lib qo'shilgach, chaqiruvchi tomonda sinxronlanadigan o'ramlar uni o'zlarining qulfidan o'tkazmasdan bajaradigan bo'lib qoldi. Shu sababli interfeysni chiqarishdan oldin kamida ikki-uch mustaqil implementatsiya yozib ko'riladi, `default` metod esa faqat haqiqiy moslik ehtiyoji uchun qo'shiladi, qulaylik uchun emas.

| Ehtiyoj | Tanlov |
|---|---|
| Faqat shartnoma | interfeys |
| Umumiy holat kerak | abstrakt sinf |
| Mavjud interfeysga metod qo'shish | `default` metod (orqaga moslik) |
| Qulaylik metodi (boshqalardan hisoblanadi) | `default` metod |
| Ko'p rolni birlashtirish | bir nechta interfeys |
| Konstanta to'plami | enum yoki `final` sinf, interfeys emas (17.8) |
| Shablon tartibi | abstrakt sinf + `final` shablon metod |

Ikkisini birga ishlatadigan shakl ham bor va u ko'p holatda eng qulay: interfeys turni belgilaydi, uning yonidagi `AbstractXxx` sinfi esa qolgan metodlarni bir nechta asosiy metod ustiga quradi. Implementatsiya qiluvchi tomon xohlasa abstrakt sinfdan voris oladi va faqat asosiy metodlarni yozadi, xohlasa interfeysni o'zi to'liq implementatsiya qiladi. Java to'plamlar kutubxonasining o'zi shu shaklda: `List` va `AbstractList`, `Map` va `AbstractMap`.

## 17.8 Konstantalarni interfeysdan voris olish

Konstantalarni interfeysga qo'yib, sinflarni shu interfeysdan voris qilish (constant interface) qoldirilgan amaliyot. U konstantalarni sinfning public API siga chiqaradi, ularning manbasini yashiradi, va nomlar konflikt qiladi.

```java
// yomon: constant interface
public interface Limits {
    int MAX_RETRY = 3;
    Duration TIMEOUT = Duration.ofSeconds(30);
}
public class SettlementService implements Limits { ... }   // MAX_RETRY public bo'lib qoldi

// yaxshi: konstanta tegishli joyda yashaydi
public final class SettlementService {
    private static final int MAX_RETRY = 3;
}

// yaxshi: umumiy konstantalar - enum yoki final sinf, static import bilan
public enum RetryLimit { ... }
```

## 17.9 Delegatsiya bilan vorislikni almashtirish

Vorislikdan chiqish yo'li - delegatsiya: voris sinf bazaviy sinfni **maydon** sifatida saqlaydi va kerakli metodlarni o'ziga o'tkazadi. Shunda bazaviy sinfning butun API si meros bo'lib o'tmaydi va shartnoma buzilmaydi.

Vorislik nega sinadi: bazaviy sinf o'z metodlarini ichidan chaqiradi (self-use) va bu hujjatlashtirilmagan detal. Klassik namuna hisoblagich qo'shilgan `HashSet`: `add` va `addAll` ikkisi ham override qilinadi, uchta element `addAll` bilan qo'shilganda hisoblagich uch emas, **olti** bo'ladi, chunki `HashSet.addAll` ichida har element uchun `add` ni chaqiradi va u override qilingan versiyaga tushadi.

```java
// yomon: addAll ichida add chaqirilishi hisoblagichni ikki marta oshiradi
class InstrumentedHashSet<E> extends HashSet<E> {

    private int addCount;

    @Override public boolean add(E e) { addCount++; return super.add(e); }
    @Override public boolean addAll(Collection<? extends E> c) {
        addCount += c.size();              // + keyin har element uchun add
        return super.addAll(c);
    }
}
```

`addAll` ni override qilmaslik bilan "tuzatish" mumkin, lekin unda kod `HashSet.addAll` ning ichidan `add` ni chaqirishiga tayanib qoladi: bu kafolatlanmagan detal va reliz bilan o'zgarishi mumkin. Ikkinchi sinish yo'li: bazaviy sinfga keyingi relizda yangi metod qo'shilsa, voris sinf uni bilmasdan meros oladi va o'z invariantini u orqali buzadi.

```java
// yomon: HashMap dan voris olish - butun API meros bo'ladi, invariant himoyalanmaydi
public class StockLevels extends HashMap<Sku, Integer> { }
stockLevels.put(sku, -5);        // manfiy qoldiq - tekshirilmadi

// yaxshi: delegatsiya - faqat kerakli amallar oshkor, invariant himoyalangan
public final class StockLevels {

    private final Map<Sku, Quantity> levels = new HashMap<>();

    public void set(Sku sku, Quantity quantity) {
        if (quantity.isNegative()) {
            throw new IllegalArgumentException("qoldiq manfiy bo'lmaydi: " + sku);
        }
        levels.put(sku, quantity);
    }

    public Quantity of(Sku sku) { return levels.getOrDefault(sku, Quantity.ZERO); }
}
```

O'tish tartibi: maydon qo'shish → `extends` ni olib tashlash → kompilyator ko'rsatgan metodlarni delegatsiyaga aylantirish → keraksizlarini o'chirish ([37-bob](37-refaktoring-harakatlari-katalogi-iii-shart.md), Replace Superclass with Delegate).

## 17.10 Teglangan sinf o'rniga ierarxiya yoki `sealed`

Teglangan sinf (tagged class) - bitta sinf ichida tur belgisi maydoni va shu belgiga qarab shoxlanadigan metodlar. Shakli tanilishi oson: `type` yoki `kind` maydoni, `switch` bilan shoxlanish va faqat ba'zi turlar uchun ma'noli maydonlar.

```java
// yomon: teglangan sinf - ikki shakl bitta sinfda
final class Figure {

    enum Kind { RECTANGLE, CIRCLE }

    private final Kind kind;
    private final double width, height;   // faqat RECTANGLE uchun
    private final double radius;          // faqat CIRCLE uchun

    double area() {
        return switch (kind) {
            case RECTANGLE -> width * height;
            case CIRCLE -> Math.PI * radius * radius;
        };
    }
}
```

Narxi: har bir obyekt ishlatilmaydigan maydonlarni ko'tarib yuradi, konstruktor noto'g'ri kombinatsiyani to'sa olmaydi (radiusli to'rtburchak), yangi shakl qo'shilganda `switch` lar bo'ylab yurish kerak va biri esdan chiqsa kompilyator jim qoladi. Yechim ierarxiya: har shakl o'z sinfida, o'z maydonlari bilan.

```java
// yaxshi: sealed ierarxiya - kompilyator to'liqlikni tekshiradi
sealed interface Figure permits Rectangle, Circle {
    double area();
}

record Rectangle(double width, double height) implements Figure {
    public double area() { return width * height; }
}

record Circle(double radius) implements Figure {
    public double area() { return Math.PI * radius * radius; }
}
```

`sealed` qo'shimcha narsa beradi: ruxsat etilgan voris ro'yxati e'londa turadi, shu sababli `switch` to'liqligini kompilyator tekshiradi va `default` shoxi kerak bo'lmaydi. Yangi voris qo'shilsa, to'liq bo'lmagan `switch` lar kompilyatsiyada chiqadi. Turga qarab shoxlanishni polimorfizmga aylantirish [takrorlangan `switch`](06-shart-mantiq-va-boshqaruv-oqimi.md#610-takrorlangan-switch-va-turga-qarab-shoxlanish) da ham ko'rilgan; bu bo'lim ierarxiya shaklini belgilaydi.

## 17.11 Amalda qo'llash

- [ ] Vorislik uchun mo'ljallanmagan barcha sinflarni `final` qiling (Spring proxy talab qilgan joylardan tashqari).
- [ ] Konstruktordan chaqirilayotgan override qilinadigan metodlarni topib, sozlashni konstruktordan chiqaring.
- [ ] Barcha `protected` maydonlarni `private` ga aylantirib, voris sinfga `protected final` metod bering.
- [ ] `super.method()` chaqirilishi shart bo'lgan joylarni `final` shablon metodga aylantiring.
- [ ] Bazaviy sinflarda `instanceof` orqali voris sinf tekshiruvlarini abstrakt metodga almashtiring.
- [ ] `UnsupportedOperationException` tashlaydigan override larni topib, interfeysni bo'ling.
- [ ] Constant interface larni yo'qotib, konstantalarni tegishli sinfga yoki enum ga ko'chiring.
- [ ] `ArrayList`, `HashMap` kabi to'plamlardan voris olgan sinflarni delegatsiyaga o'tkazing.
- [ ] Tur belgisi maydoni (`type`, `kind`) bo'yicha shoxlanadigan sinflarni toping va ularni `sealed` ierarxiyaga o'tkazing.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 18, 19, 20 - kompozitsiya, vorislik uchun dizayn, interfeys va abstrakt sinf tanlovi
- Joshua Bloch, *Effective Java* 3rd, Item 22, 23 - interfeys faqat tur uchun, teglangan sinf o'rniga ierarxiya
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409) - `sealed` va `permits` semantikasi, switch to'liqligi
- Joshua Bloch, *Effective Java* 3rd, Item 21 - chiqarilgan interfeysga `default` metod qo'shishning xavfi
- Joshua Bloch, *Effective Java* 3rd, Item 18 - `InstrumentedHashSet` da `addAll` ikki marta hisoblashi, self-use ning hujjatlashtirilmagan detal ekani
- Joshua Bloch, *Effective Java* 3rd, Item 19 - vorislik uchun hujjatlash, konstruktorda override qilinadigan metodni chaqirmaslik, `clone` va `readObject` ham shunday
- Joshua Bloch, *Effective Java* 3rd, Item 20 - interfeys yonida `AbstractXxx` skelet implementatsiyasi

---

[&larr; 16. O'zgarmaslik va holat boshqaruvi kod darajasida](16-ozgarmaslik-va-holat-boshqaruvi-kod.md) · [Mundarija](README.md) · [18. Xato bilan ishlash qoidalari &rarr;](18-xato-bilan-ishlash-qoidalari.md)
