<!-- doc: clean-code | chapter: 17 | part: V. Obyekt, ma'lumot va holat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 17. Vorislik, kompozitsiya va polimorfizm mexanikasi (Inheritance Mechanics)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

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
- [17.11 Interfeys evolyutsiyasi va `default` metod cheklovlari](#1711-interfeys-evolyutsiyasi-va-default-metod-cheklovlari)
- [17.12 Amalda qo'llash](#1712-amalda-qollash)

</details>


"Vorislikdan ustun kompozitsiya" printsipi [patternlar hujjatidagi](../patterns/README.md) vorislikdan ustun kompozitsiya printsipida berilgan. Bu bobda vorislik **ishlatilganda** uni to'g'ri bajarish mexanikasi: vorislik uchun dizayn, konstruktor tuzog'i, `protected` muammosi, va vorislikdan kompozitsiyaga o'tish yo'li.

## 17.1 Vorislik uchun dizayn qilish yoki `final` qilish

Sinf uch holatdan birida bo'lishi kerak: vorislik uchun mo'ljallangan va hujjatlashtirilgan, `final`, yoki interfeys. "Vorislik mumkin, lekin o'ylanmagan" to'rtinchi holat - xato manbasi, chunki voris sinf bazaviy sinfning ichki qoidalarini bilmaydi va ularni buzadi.

Shu sababli amaliy standart: **sinf `final` bo'lishi standart holat**, vorislik esa ongli qaror. Spring kontekstida istisno bor: `@Configuration` sinflari va CGLIB proxy qilinadigan beanlar `final` bo'lmaydi (26.1).

Vorislikni ochish qarorini qabul qilgandan keyin uchta amaliy talab qoladi.

**Override uchun mo'ljallangan metod `public` yoki `protected` bo'ladi.** `package-private` metod faqat bir xil ish vaqtidagi paketda override qilinadi, ya'ni paket nomi ham, sinf yuklovchisi (class loader) ham bir xil bo'lishi kerak. Boshqa paketdagi bir xil imzoli metod override qilmaydi: u butunlay boshqa metod bo'lib qoladi va bazaviy sinf o'z versiyasini chaqiradi, chaqiruv esa jim kutilmagan implementatsiyaga tushadi. Modul va kutubxona chegarasida bu xato uzoq vaqt ko'rinmaydi. Teskari tomoni kompilyator qoidasi: override qilgan metodning kirish darajasi superclass dagidan **torroq bo'lishi mumkin emas**, chunki voris nusxasi superclass turi orqali ishlatilganda metod chaqirilishi kerak (Liskov printsipi tilga qurib qo'yilgan). Shuning uchun sinf interfeysni amalga oshirsa, interfeys metodlari `public` bo'lishi shart.

**Vorislik uchun dizayn sinovdan o'tadi, va sinovning yagona yo'li - voris sinf yozish.** Hujjat yozib qo'yish yetmaydi: qaysi `protected` a'zo kerak, qaysi biri ortiqcha ekani faqat voris yozilganda ko'rinadi. Amaliy mezon: uchta voris sinf yozib ko'riladi va ulardan kamida bittasi boshqa odam tomonidan yoziladi. O'zi yozgan odam o'zining yashirin taxminlarini ko'rmaydi, boshqa odam esa birinchi kunda ularga urilib qoladi. Har bir ortiqcha `protected` a'zo esa abadiy qarz: u API ning bir qismi va keyin olib tashlanmaydi.

**Vorislikka ruxsat bersangiz, sinf o'z override qilinadigan metodlarini umuman chaqirmasligi kerak.** Self-use (sinfning o'z override qilinadigan metodini ichidan chaqirishi) voris uchun hujjatlashtirilmagan detalga aylanadi (17.9) va uni yo'qotishning mexanik retsepti bor: har bir override qilinadigan metodning tanasi `private` yordamchi metodga ko'chiriladi, keyin sinf ichidagi barcha chaqiruvlar shu yordamchiga yo'naltiriladi. Shundan keyin voris metodni override qilsa ham, bazaviy sinfning ichki ishi o'zgarmaydi.

```java
// yomon: ichki chaqiruv override qilinadigan metodga tushadi
public void importFile(Path file) {
    for (SettlementRow row : rows(file)) {
        if (validate(row)) { save(row); }      // voris versiyasi chaqiriladi
    }
}
protected boolean validate(SettlementRow row) { return row.isComplete(); }

// yaxshi: tana private yordamchiga ko'chdi, ichki chaqiruv shunga boradi
public void importFile(Path file) {
    for (SettlementRow row : rows(file)) {
        if (validateInternal(row)) { save(row); }
    }
}
private boolean validateInternal(SettlementRow row) { return row.isComplete(); }
protected boolean validate(SettlementRow row) { return validateInternal(row); }
```

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

Taqiqning chegarasi ham aniq: konstruktordan `private`, `final` va `static` metodlarni chaqirish **xavfsiz**, chunki ularning hech biri override qilinmaydi va demak voris sinf kodi konstruktor ichida ishga tushmaydi. Shuning uchun konstruktordagi sozlash ishi shu uch toifadan biriga ko'chiriladi, olib tashlanmaydi: `private void initDefaults()` yoki `static ImportSettings defaults()` qonuniy shakl.

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

Bu umumiy printsipning xususiy holati: **niyatning aniq izi kodda qoldiriladi**. Google ning uslub ko'rsatmalari o'quvchi uchun optimallashtirishni muallif uchun optimallashtirishdan ustun qo'yadi, va shundan oshkor belgilar talabi kelib chiqadi: Java, JavaScript va C++ ko'rsatmalari metod ustki sinf metodini override qilganda `@Override` annotatsiyasini yoki `override` kalit so'zini **majburiy** qiladi. Belgi bo'lmasa o'quvchi niyatni taxmin qila oladi, lekin buning uchun qo'shimcha qidirish kerak bo'ladi va bu narx har o'quvchiga qayta-qayta tushadi.

Ikkinchi shakl - niyatni **tur bilan** aytish: masalan egalik (ownership) o'tayotganini parametr turi orqali ko'rsatish, shunda chaqiruv joyini o'qigan odam qo'shimcha kodga qaramasdan mulohaza yuritadi. Java da bunga eng yaqin vositalar `Optional` qaytarish turi (bo'lmasligi mumkinligi oshkor), `@Nullable` va `@NullMarked` (42.2), yopiq ierarxiya uchun `sealed` (17.10) va o'zgarmas uzatish uchun `record`. Mezon bir xil: belgi chaqiruv yoki e'lon joyida ko'rinadi va o'quvchini boshqa faylga yubormaydi.

```java
// Niyat ko'rinmaydi: bu override mi, yangi metodmi?
public void process(Row row) { ... }

// Niyat oshkor: kompilyator ham tekshiradi
@Override
public void process(Row row) { ... }
```

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

Uchinchi ehtiyot nuqtasi muhimroq: chiqarilgan interfeysga `default` metod qo'shish mavjud implementatsiyalarni **jim** buzishi mumkin. Kompilyatsiya o'tadi, chunki metod tayyor, lekin implementatsiya shu metodning invariantini bilmaydi. Platformaning o'zida shu holat bo'lgan: `Collection.removeIf` Java 8 da `default` bo'lib qo'shilgach, chaqiruvchi tomonda sinxronlanadigan o'ramlar uni o'zlarining qulfidan o'tkazmasdan bajaradigan bo'lib qoldi. Shu sababli interfeysni chiqarishdan oldin kamida ikki-uch mustaqil implementatsiya yozib ko'riladi. Ikki holat esa bir-biridan ajratiladi va aralashtirilmaydi: interfeys **yangi yaratilayotgan** bo'lsa, `default` metod qulaylik uchun ham haqli, chunki hali hech qanday implementatsiya yo'q va shartnoma bir vaqtda e'lon qilinadi; interfeys **chiqarilgan** bo'lsa, `default` metod faqat moslik ehtiyoji kritik bo'lganda qo'shiladi (17.11).

| Ehtiyoj | Tanlov |
|---|---|
| Faqat shartnoma | interfeys |
| Umumiy holat kerak | abstrakt sinf |
| Yangi yaratilayotgan interfeysga qulaylik metodi | `default` metod |
| Chiqarilgan interfeysga metod qo'shish | `default` metod, faqat moslik ehtiyoji uchun (17.11) |
| Ko'p rolni birlashtirish | bir nechta interfeys |
| Konstanta to'plami | enum yoki `final` sinf, interfeys emas (17.8) |
| Shablon tartibi | abstrakt sinf + `final` shablon metod |

Skelet implementatsiyani yozish tartibi uch qadamli va qadamlar joyini almashtirmaydi. Birinchi: interfeysdagi qaysi metodlar **asosiy** (primitiv) ekanini aniqlash, ya'ni qolganlari shu metodlar ustiga qurilishi mumkin bo'lgan eng kichik to'plamni topish. Ikkinchi: qolgan metodlardan qaysi birini interfeysning o'zida `default` qilib yozish mumkinligini ko'rish. Uchinchi: asosiy metodlar `abstract` qoladigan, qolgan hamma metod amalga oshirilgan abstrakt sinf yozish; shu sinf hech qanday `default` qilinmagan metodni ham o'z ichiga oladi. Birinchi qadam tashlab o'tilsa, skelet implementatsiya haqiqiy skelet bo'lmaydi: voris olgan odam baribir ko'p metod yozishga majbur bo'ladi.

Skeletdan voris olish imkonsiz bo'lsa (sinf allaqachon boshqa sinfdan voris olgan), uchinchi yo'l bor: sinf interfeysni o'zi amalga oshiradi va chaqiruvlarni skeletdan voris olgan `private` ichki sinfga o'tkazadi. Bu **simulyatsiya qilingan ko'p vorislik** (simulated multiple inheritance) deb ataladi va kompozitsiyaning aniq shakli: tashqi sinf turni beradi, ichki sinf implementatsiyani.

```java
// Sinf allaqachon AbstractImporter dan voris olgan, lekin List ham bo'lishi kerak
public final class SettlementRows extends AbstractImporter implements List<Row> {

    private final class Rows extends AbstractList<Row> {
        @Override public Row get(int index) { return rows.get(index); }
        @Override public int size() { return rows.size(); }
    }

    private final Rows view = new Rows();

    @Override public Row get(int index) { return view.get(index); }
    @Override public int size() { return view.size(); }
}
```

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

"Unda hech narsani override qilmayman, faqat yangi metod qo'shaman" degan yechim ham xavfsiz emas, chunki uchinchi sinish yo'li bor: bazaviy sinfga keyingi relizda **bir xil imzoli, lekin boshqa qaytish turli** metod qo'shilsa, voris sinf umuman kompilyatsiya bo'lmaydi; qaytish turi mos kelsa esa siz bilmagan shartnomaga ega override bo'lib qoladi. Ya'ni vorislikda bazaviy sinfning har bir keyingi relizi sizning sinfingizni buzishi mumkin, kompozitsiyada esa bunday bog'liqlik yo'q.

To'rtinchi dalil dizayn tomonida: bazaviy sinf API sidagi **nuqsonlar vorisga majburan o'tadi**. Noto'g'ri nomlangan metod, ortiqcha parametr, o'rinsiz `null` qaytarish - hammasi voris sinfning public API sining bir qismi bo'lib qoladi va siz ularni yashira olmaysiz. Kompozitsiyada esa yangi API o'zingiz yozasiz: eski nuqsonlar o'ramchi ichida qoladi va tashqariga chiqmaydi.

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

Aylantirish tartibi mexanik va shu tartibda bajariladi. Birinchi: tegga bog'liq **har bir** metod uchun abstrakt ildiz sinfda (yoki interfeysda) abstrakt metod e'lon qilinadi. Ikkinchi: tegga bog'liq bo'lmagan metodlar va hamma turga umumiy maydonlar ildizda qoldiriladi; agar umumiy metod tanasi tegga qaramasa, u ildizda konkret metod bo'ladi. Uchinchi: har bir tur uchun ildizdan voris olgan konkret sinf yoziladi va unga faqat **shu** turga tegishli maydonlar hamda abstrakt metodlarning implementatsiyasi tushadi. Oxirida tur belgisi maydoni va unga qarab shoxlanadigan `switch` lar yo'qoladi: ular konstruktorlarga va polimorfizmga aylangan bo'ladi.

Ierarxiya tanlashning ikkinchi, ko'pincha e'tibordan qoladigan foydasi ham bor: u turlar orasidagi **tabiiy ierarxik munosabatni** kodda ifodalaydi. Kvadrat to'rtburchakning maxsus turi, kredit to'lovi to'lovning maxsus turi; teglangan sinfda bu munosabat `enum` konstantasining nomi bo'lib qoladi, ierarxiyada esa tur tizimining bir qismiga aylanadi. Natijada kompilyator yordam beradigan joy ko'payadi: faqat kvadratga tegishli metod faqat kvadratni qabul qiladi va noto'g'ri chaqiruv kompilyatsiyada chiqadi.

`sealed` qo'shimcha narsa beradi: ruxsat etilgan voris ro'yxati e'londa turadi, shu sababli `switch` to'liqligini kompilyator tekshiradi va `default` shoxi kerak bo'lmaydi. Yangi voris qo'shilsa, to'liq bo'lmagan `switch` lar kompilyatsiyada chiqadi. Turga qarab shoxlanishni polimorfizmga aylantirish [takrorlangan `switch`](06-shart-mantiq-va-boshqaruv-oqimi.md#610-takrorlangan-switch-va-turga-qarab-shoxlanish) da ham ko'rilgan; bu bo'lim ierarxiya shaklini belgilaydi.

## 17.11 Interfeys evolyutsiyasi va `default` metod cheklovlari

Interfeys chiqarilgandan keyin u sizga tegishli bo'lmay qoladi: uni mijozlar amalga oshirgan va har o'zgarish ularning kodiga tegadi. Shu sababli interfeysni rivojlantirishning chegaralari aniq.

**`default` metod nima uchun mo'ljallanmagan.** `default` metod interfeysdan metod **olib tashlash** yoki mavjud metod **imzosini o'zgartirish** uchun vosita emas: bu ikki o'zgarishni mijozni buzmasdan qilishning yo'li yo'q. Olib tashlangan metodni chaqirgan kod `NoSuchMethodError` bilan yiqiladi, imzo o'zgarsa esa eski implementatsiya override qilishni to'xtatadi va chaqiruv jim `default` ga tushadi. Amaldagi yo'l: eski metodni `@Deprecated` qilib qoldirish va yangisini yonida qo'shish, interfeysni ikkiga bo'lish, yoki yangi interfeys e'lon qilib eski interfeysni o'z ichiga olmaslik.

**`default` metodning qat'iy cheklovlari.** Birinchi uchtasi tilda qurilgan va ularni chetlab o'tish yo'li yo'q; to'rtinchisi intizom qoidasi:

| Cheklov | Oqibati |
|---|---|
| `Object` metodlari (`equals`, `hashCode`, `toString`) uchun `default` berilmaydi | tenglik shartnomasi interfeysda emas, sinfda yoziladi (15.1) |
| Interfeysda instans maydoni bo'lmaydi | `default` metod holat ushlay olmaydi, faqat boshqa metodlar ustiga quriladi |
| Interfeysda nopublik statik a'zo bo'lmaydi (`private static` metoddan tashqari) | yordamchi holatni yashirib bo'lmaydi |
| O'zingizga tegishli bo'lmagan interfeysga `default` qo'shilmaydi | implementatsiyalarni jim buzadi (17.7) |

**`private` interfeys metodi.** JDK 9 dan interfeysda `private` metod yozish mumkin va uning yagona vazifasi shu: bir nechta `default` metod orasidagi umumiy kodni bir joyga chiqarish. U meros olinmaydi va override qilinmaydi, ya'ni implementatsiya qiluvchi sinf uni ko'rmaydi ham: shartnomaga hech narsa qo'shmaydi. Shuning uchun `default` metodlar takrorlanib ketsa, umumiy bo'lakni `private` metodga chiqarish to'g'ri yo'l va bu `AbstractXxx` skelet sinfiga o'tish zaruratini keltirmaydi.

```java
public interface SettlementWindow {

    LocalDate from();
    LocalDate to();

    default boolean covers(LocalDate date) {
        return !date.isBefore(from()) && !date.isAfter(to());
    }

    default int lengthInDays() {
        return (int) span().toDays() + 1;
    }

    // Faqat default metodlar uchun: meros olinmaydi, override qilinmaydi
    private Duration span() {
        return Duration.between(from().atStartOfDay(), to().atStartOfDay());
    }
}
```

**Qulaylik metodining chegarasi.** `default` metod qo'shish arzon ko'rinadi, shuning uchun interfeys qulaylik metodlari bilan to'lib ketishi oson. Qoida: har bir metod o'z vaznini tortishi kerak. Metod soni o'sgani sari sinfni o'rganish, hujjatlashtirish, test qilish va qo'llab-quvvatlash qiyinlashadi, implementatsiya qiluvchilar esa har yangi metodni kuzatib borishga majbur bo'ladi. Shubha bo'lsa metod qo'shilmaydi: keyin qo'shish mumkin, olib tashlash esa yo'q.

Shu yerda 17.7 jadvalidagi "qulaylik metodi" qatorining sharti ishlaydi: interfeys **yangi yaratilayotgan** bo'lsa, boshqa metodlardan hisoblanadigan qulaylik metodini `default` qilish haqli, chunki shartnoma bir vaqtda e'lon qilinadi va hech qanday mavjud implementatsiya buzilmaydi. Interfeys allaqachon **chiqarilgan** bo'lsa, qulaylik yetarli sabab emas: `default` metod faqat moslik ehtiyoji kritik bo'lganda qo'shiladi, aks holda qulaylik metodi statik yordamchi sinfga (`SettlementWindows.lengthOf(...)`) chiqariladi.

## 17.12 Amalda qo'llash

- [ ] Vorislik uchun mo'ljallanmagan barcha sinflarni `final` qiling (Spring proxy talab qilgan joylardan tashqari).
- [ ] Konstruktordan chaqirilayotgan override qilinadigan metodlarni topib, sozlashni konstruktordan chiqaring.
- [ ] Barcha `protected` maydonlarni `private` ga aylantirib, voris sinfga `protected final` metod bering.
- [ ] `super.method()` chaqirilishi shart bo'lgan joylarni `final` shablon metodga aylantiring.
- [ ] Bazaviy sinflarda `instanceof` orqali voris sinf tekshiruvlarini abstrakt metodga almashtiring.
- [ ] `UnsupportedOperationException` tashlaydigan override larni topib, interfeysni bo'ling.
- [ ] Constant interface larni yo'qotib, konstantalarni tegishli sinfga yoki enum ga ko'chiring.
- [ ] `ArrayList`, `HashMap` kabi to'plamlardan voris olgan sinflarni delegatsiyaga o'tkazing.
- [ ] Tur belgisi maydoni (`type`, `kind`) bo'yicha shoxlanadigan sinflarni toping va ularni `sealed` ierarxiyaga o'tkazing.
- [ ] Vorislik uchun ochilgan sinflarda self-use ni topib, tanani `private` yordamchi metodga ko'chiring.
- [ ] Override uchun mo'ljallangan `package-private` metodlarni `protected` yoki `public` ga o'tkazing.
- [ ] Chiqarilgan interfeyslarga qo'shilgan `default` metodlarni ko'rib, faqat moslik uchun qo'shilganlarini qoldiring.
- [ ] `default` metodlar orasidagi takrorlangan kodni `private` interfeys metodiga chiqaring.

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 8-bob ("Optimize for the Reader") - o'quvchi uchun optimallashtirish printsipi va niyatning oshkor izini qoldirish talabi: metod ustki sinf metodini override qilganda annotatsiya yoki kalit so'zni majburiy qilish, hamda niyatni tur orqali ko'rsatish. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Joshua Bloch, *Effective Java* 3rd, Item 18, 19, 20 - kompozitsiya, vorislik uchun dizayn, interfeys va abstrakt sinf tanlovi
- Joshua Bloch, *Effective Java* 3rd, Item 15 (75-bet) - override qilgan metodning kirish darajasi superclass dagidan torroq bo'lmasligi va interfeys metodlarining `public` bo'lishi
- Joshua Bloch, *Effective Java* 3rd, Item 18 (89-bet) - faqat yangi metod qo'shish ham xavfsiz emasligi: bazaviy sinfga bir xil imzoli, boshqa qaytish turli metod qo'shilsa voris kompilyatsiya bo'lmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 18 (92-bet) - bazaviy sinf API sidagi nuqsonlarning vorisga majburan o'tishi va kompozitsiyaning ularni yashirish imkoni
- Joshua Bloch, *Effective Java* 3rd, Item 19 (95-bet) - vorislik uchun dizaynni sinashning yagona yo'li voris sinf yozish bo'lishi, uchta voris yetarli ekani va kamida bittasi boshqa odam tomonidan yozilishi
- Joshua Bloch, *Effective Java* 3rd, Item 19 (96-bet) - konstruktordan `private`, `final` va `static` metodlarni chaqirish xavfsizligi
- Joshua Bloch, *Effective Java* 3rd, Item 19 (98-bet) - self-use ni yo'qotishning mexanik yo'li: tanani `private` yordamchi metodga ko'chirib ichki chaqiruvlarni shunga yo'naltirish
- Joshua Bloch, *Effective Java* 3rd, Item 20 (100-bet) - `default` metod cheklovlari: `Object` metodlari uchun berilmasligi, interfeysda instans maydoni va nopublik statik a'zo bo'lmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 20 (102-bet) - skeletdan voris olish imkonsiz bo'lganda `private` ichki sinf orqali simulyatsiya qilingan ko'p vorislik, va skelet implementatsiyani yozish tartibi
- Joshua Bloch, *Effective Java* 3rd, Item 21 (106-bet) - `default` metod interfeysdan metod olib tashlash yoki imzoni o'zgartirish uchun mo'ljallanmaganligi
- Joshua Bloch, *Effective Java* 3rd, Item 23 (110-bet) - teglangan sinfni ierarxiyaga aylantirish tartibi: abstrakt ildiz, umumiy a'zolar ildizda, har tur uchun konkret voris
- Joshua Bloch, *Effective Java* 3rd, Item 23 (111-bet) - sinf ierarxiyasining turlar orasidagi tabiiy ierarxik munosabatni ifodalashi va kompilyatsiya vaqtidagi tur tekshiruvini kuchaytirishi
- Joshua Bloch, *Effective Java* 3rd, Item 51 (236-bet) - qulaylik metodlarini ko'paytirib yubormaslik: har metod o'z vaznini tortishi va shubha bo'lsa qo'shilmasligi
- ESLATMA: 17.7 jadvalidagi "qulaylik metodi -> `default` metod" qatori Bloch ning Item 21 dagi ogohlantirishiga qarama-qarshi ko'rinadi. Ikkisini ajratuvchi shart (interfeys YANGI yaratilayotganda `default` qulaylik uchun ham haqli, CHIQARILGAN interfeysga esa faqat moslik ehtiyoji uchun) korpus qo'shimchasi; kitob ikki holatni bu shaklda ajratmaydi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 9.4 (365-bet) - interfeysning `private` metodi meros olinmasligi va override qilinmasligi, u faqat shu interfeysning `default` metodlari uchun yordamchi bo'lishi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 9-bob (226-bet) - JDK 9 dan interfeysda `private` metod va uning `default` metodlar orasidagi umumiy kodni chiqarish uchun ishlatilishi
- *The Java Virtual Machine Specification, Java SE 25 Edition* (Lindholm, Yellin, Bracha, Buckley, Smith), 5.4.5 (395-bet) - `package-private` metodning faqat bir xil ish vaqtidagi paketda (bir xil paket nomi va bir xil sinf yuklovchisi) override qilinishi
- Joshua Bloch, *Effective Java* 3rd, Item 22, 23 - interfeys faqat tur uchun, teglangan sinf o'rniga ierarxiya
- [JEP 409: Sealed Classes](https://openjdk.org/jeps/409) - `sealed` va `permits` semantikasi, switch to'liqligi
- Joshua Bloch, *Effective Java* 3rd, Item 21 - chiqarilgan interfeysga `default` metod qo'shishning xavfi
- Joshua Bloch, *Effective Java* 3rd, Item 18 - `InstrumentedHashSet` da `addAll` ikki marta hisoblashi, self-use ning hujjatlashtirilmagan detal ekani
- Joshua Bloch, *Effective Java* 3rd, Item 19 - vorislik uchun hujjatlash, konstruktorda override qilinadigan metodni chaqirmaslik, `clone` va `readObject` ham shunday
- Joshua Bloch, *Effective Java* 3rd, Item 20 - interfeys yonida `AbstractXxx` skelet implementatsiyasi

---

[&larr; 16. O'zgarmaslik va holat boshqaruvi kod darajasida](16-ozgarmaslik-va-holat-boshqaruvi-kod.md) · [Mundarija](README.md) · [18. Xato bilan ishlash qoidalari &rarr;](18-xato-bilan-ishlash-qoidalari.md)
