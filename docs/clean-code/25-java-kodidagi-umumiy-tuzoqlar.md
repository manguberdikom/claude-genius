<!-- doc: clean-code | chapter: 25 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 25. Java kodidagi umumiy tuzoqlar (Common Java Pitfalls)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [25.1 `Optional` maydon, parametr va seriyalash](#251-optional-maydon-parametr-va-seriyalash)
- [25.2 Statik ishga tushirish tartibi va sinf yuklanishi](#252-statik-ishga-tushirish-tartibi-va-sinf-yuklanishi)
- [25.3 `instanceof` zanjiri va `getClass()` solishtirish](#253-instanceof-zanjiri-va-getclass-solishtirish)
- [25.4 Seriyalash: `serialVersionUID`, `readObject` va undan qochish](#254-seriyalash-serialversionuid-readobject-va-undan-qochish)
- [25.5 Refleksiya narxi va uni chegaralash](#255-refleksiya-narxi-va-uni-chegaralash)
- [25.6 `finalize`, `Cleaner` va resurs oxiri](#256-finalize-cleaner-va-resurs-oxiri)
- [25.7 Ichki sinf va yashirin tashqi havola](#257-ichki-sinf-va-yashirin-tashqi-havola)
- [25.8 Anonim sinf va lambda tanlovi](#258-anonim-sinf-va-lambda-tanlovi)
- [25.9 `enum` da xatti-harakat, `EnumMap`, `EnumSet`, `valueOf`](#259-enum-da-xatti-harakat-enummap-enumset-valueof)
- [25.10 Kompilyator ogohlantirishlari: `-Xlint`, `-Werror`, Error Prone, NullAway](#2510-kompilyator-ogohlantirishlari--xlint--werror-error-prone-nullaway)
- [25.11 `ordinal()` ga tayanmaslik, enum ni interfeys bilan kengaytirish va `@Override`](#2511-ordinal-ga-tayanmaslik-enum-ni-interfeys-bilan-kengaytirish-va-override)
- [25.12 Deseriyalashga hujum va undan himoya](#2512-deseriyalashga-hujum-va-undan-himoya)
- [25.13 Amalda qo'llash](#2513-amalda-qollash)

</details>


Bu bob oldingi boblarga sig'magan, lekin kundalik kodda uchraydigan Java tuzoqlarini yig'adi: `Optional` ning chegaralari, statik ishga tushirish, seriyalash, refleksiya, ichki sinflar, enum mexanikasi va kompilyator ogohlantirishlari.

## 25.1 `Optional` maydon, parametr va seriyalash

`Optional` qaytish qiymati uchun mo'ljallangan. Maydon sifatida ishlatish uch muammo keltiradi: `Optional` `Serializable` emas, har bir obyekt uchun qo'shimcha o'ram yaratiladi, va JPA/Jackson bilan muammo chiqadi.

```java
// yomon: Optional maydon
public class Order {
    private Optional<Discount> discount;      // Serializable emas, JPA bilan ishlamaydi
}

// yaxshi: maydon null bo'lishi mumkin, getter Optional qaytaradi
public class Order {

    private Discount discount;                // null bo'lishi mumkin

    public Optional<Discount> discount() { return Optional.ofNullable(discount); }
}

// yomon: Optional parametr - chaqiruv joyi shovqinli
void apply(Order order, Optional<Discount> discount);
apply(order, Optional.empty());

// yaxshi: overload (5.9)
void apply(Order order);
void apply(Order order, Discount discount);
```

## 25.2 Statik ishga tushirish tartibi va sinf yuklanishi

Statik initializator (`static { }`) sinf birinchi marta ishlatilganda bajariladi va uning vaqti oldindan aniq emas. Agar unda tashqi resursga murojaat bo'lsa (fayl, baza, tarmoq), xato kutilmagan joyda `ExceptionInInitializerError` sifatida chiqadi va diagnostikasi qiyin bo'ladi.

```java
// yomon: statik blokda I/O - xato ExceptionInInitializerError bo'lib chiqadi
public class TaxRates {
    private static final Map<Region, BigDecimal> RATES;
    static {
        RATES = loadFromDatabase();      // qachon bajariladi - aniq emas
    }
}

// yaxshi: yuklash oshkor, boshqariladigan joyda (Spring bean, lazy supplier)
@Component
public class TaxRates {

    private final Map<Region, BigDecimal> rates;

    TaxRates(TaxRateRepository repository) {
        this.rates = Map.copyOf(repository.loadAll());    // konteyner boshqaradi
    }
}
```

Statik blokda `try-catch` paydo bo'lishi tasodif emas, til talabi: statik
initializator va sinf o'zgaruvchisi initsializatori **tekshiriladigan
istisno tashlay olmaydi**, chunki uni ushlaydigan chaqiruv joyi yo'q.
Shuning uchun fayl yoki baza o'qishi majburan `try-catch` ga o'raladi, va
ushlangan istisno odatda `ExceptionInInitializerError` ga aylanib
chiqadi: stack trace da biznes amali emas, sinf yuklanishi ko'rinadi.
Ya'ni "statik blokda I/O qilmaslik" qoidasi uslub maslahati emas, tilning
o'zi qo'ygan chegaradan kelib chiqadi.

Statik maydonlarning ishga tushish tartibi e'lon tartibida boradi va bu tartibga bog'lanish nozik xato beradi: pastda e'lon qilingan maydon yuqoridagi initializatorda `null` bo'ladi.

**Statik a'zoga sinf nomi bilan murojaat qilinadi.** Java `static` maydon va metodga **instans havolasi** orqali ham murojaat qilishga ruxsat beradi: `order.MAX_ITEMS` yoki `clock.systemUTC()` kompilyatsiya qilinadi. Bu tavsiya etilmaydi va sababi o'qilishda: chaqiruv joyi a'zoning statik ekanini yashiradi, ya'ni o'quvchi uni instans holatiga bog'liq deb o'ylaydi. Yana bir tuzoq - havola `null` bo'lsa ham chaqiruv ishlaydi, chunki `static` a'zo uchun instans kerak emas, va bu `null` tekshiruvi haqida yolg'on xulosaga olib keladi. Qoida: `Order.MAX_ITEMS`, `Clock.systemUTC()`.

```java
Order order = null;
int max = order.MAX_ITEMS;        // qonuniy va ishlaydi: NPE yo'q, lekin chalg'ituvchi
int better = Order.MAX_ITEMS;     // statik ekani ko'rinadi
```

Statik maydonga instans metodi orqali murojaat qilish `final` bilan birga yana bir chalkashlik beradi: `static final` maydonni statik initializator o'zgartira oladi, statik metod esa yo'q (tayinlash kompilyatsiya qilinmaydi). Shu bilan birga statik metod ichida **bir xil nomli lokal o'zgaruvchi** bo'lsa, tayinlash lokalga tushadi va kompilyator xato bermaydi: shuning uchun maydon va lokal o'zgaruvchi uchun bir xil nom ishlatilmaydi (2.3).

Checkstyle da buni `IllegalInstantiation` emas, `StaticVariableName` bilan birga `RequireThis` va SpotBugs ning `ST` guruhidagi qoidalari ushlaydi; Error Prone da `StaticQualifiedUsingExpression` aynan shu holatga qo'yilgan (42.2).

## 25.3 `instanceof` zanjiri va `getClass()` solishtirish

Uzun `instanceof` zanjiri turga qarab shoxlanish hidi (6.10) va zamonaviy Java da uning to'g'ri shakli bor: `sealed` interfeys va pattern matching bilan `switch`, bunda to'liqlik kompilyator tomonidan tekshiriladi ([arxitektor hujjatidagi](../architect/README.md) sealed interfeys bo'limi).

```java
// yomon: zanjir, to'liqligi tekshirilmaydi
if (event instanceof PaymentSettled s) { ... }
else if (event instanceof PaymentRejected r) { ... }
else { throw new IllegalStateException("noma'lum hodisa"); }

// yaxshi: sealed + switch - yangi tur qo'shilsa kompilyator eslatadi
sealed interface PaymentEvent permits PaymentSettled, PaymentRejected, PaymentRefunded { }

String describe(PaymentEvent event) {
    return switch (event) {
        case PaymentSettled s -> "yopildi: " + s.amount();
        case PaymentRejected r -> "rad etildi: " + r.reason();
        case PaymentRefunded f -> "qaytarildi: " + f.amount();
    };
}
```

## 25.4 Seriyalash: `serialVersionUID`, `readObject` va undan qochish

Java seriyalash mexanizmi (`Serializable`) xavfsizlik nuqsonlari va moslik muammolari manbai: deseriyalash konstruktorni chetlab o'tadi (invariant tekshirilmaydi), va ishonchsiz ma'lumotni deseriyalash masofadan kod bajarilishiga olib keladi.

Qoida: yangi kodda `Serializable` ishlatmaslik. Ma'lumot almashish uchun JSON yoki Protobuf; kesh uchun ham seriyalanadigan format tanlanadi.

Uchinchi narx test yukida va u ko'pincha hisobga olinmaydi: seriyalanadigan
sinf uchun har relizda yangi versiyada seriyalab eski versiyada
deseriyalash va teskarisi sinalishi kerak. Ya'ni testlar hajmi
seriyalanadigan sinflar soni va relizlar soni ko'paytmasiga proporsional
o'sadi, va bu yuk hech qachon kamaymaydi, chunki bir marta chiqarilgan
seriyalangan shakl API bo'lib qoladi.

Majbur bo'lganda ham `Serializable` ni hamma sinfga qo'yib bo'lmaydi: u
faqat **ma'lumotga yo'naltirilgan** sinf uchun mos. Jarayonga
yo'naltirilgan sinfning (I/O oqimi, `Thread`, ulanish, soket) ichki holati
qisqa umrli va jarayonga bog'langan, shuning uchun uni baytga aylantirish
ma'nosiz: oqimdan tiklangan obyekt endi hech narsaga ulanmagan bo'ladi va
`NotSerializableException` dan ham yomoni, jim ishlamaydigan obyekt
beradi.

```java
// Agar Serializable majbur bo'lsa (legacy, RMI, HttpSession):
public final class SessionData implements Serializable {

    // Versiya oshkor: aks holda sinf o'zgarganda deseriyalash buziladi
    private static final long serialVersionUID = 1L;

    // Sezgir maydon seriyalanmaydi
    private transient String accessToken;

    // Invariant deseriyalashdan keyin ham tekshiriladi
    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        if (userId == null) throw new InvalidObjectException("userId bo'sh");
    }
}
```

`Serializable` majbur bo'lgan joyda yana uchta qoida bor. Birinchisi: sukut bo'yicha seriyalangan shakl sinfning **ichki tuzilishini** oqimga chiqaradi, ya'ni maydon nomi va turi public API ga aylanadi va keyin ularni o'zgartirib bo'lmaydi. Ichki tuzilma mantiqiy mazmunga mos kelmasa (ikki tomonli ro'yxat tugunlari, kesh maydonlari), `writeObject`/`readObject` bilan o'z shakli yoziladi va unda faqat mantiqiy ma'lumot qoladi.

Fizik ko'rinish mantiqiy mazmundan farq qilganda sukut shaklning zarari
bittasi bilan tugamaydi, to'rttasi bor: eksport qilingan API hozirgi ichki
ko'rinishga umrbod bog'lanadi; oqim ortiqcha joy oladi, chunki tugun,
havola va kesh maydonlari ham yoziladi; yozish va o'qish ortiqcha vaqt
oladi, chunki obyekt grafi bo'ylab qimmat yurish kerak; va chuqur graf
rekursiv yurishda `StackOverflowError` beradi, ya'ni nosozlik ma'lumot
hajmiga qarab kutilmaganda chiqadi.

Shundan `transient` intizomi kelib chiqadi: **`transient` deb e'lon
qilish mumkin bo'lgan har bir maydon shunday e'lon qilinadi.** Bunga
hosilaviy maydonlar (keshlangan `hashCode`, oldindan hisoblangan jami) va
qiymati JVM ning aynan shu ishga tushishiga bog'liq maydonlar (native
tuzilmaga ko'rsatkich, ochiq fayl deskriptori) kiradi. Yuqoridagi misol
`transient` ni sezgir maydon uchun ko'rsatadi, lekin mezon kengroq:
maydonni oqimdan tiklash shart emas bo'lsa, u oqimga chiqmaydi.

`transient` maydon deseriyalashdan keyin tur default qiymatini oladi
(`null`, `0`, `false`), chunki konstruktor ham, maydon initsializatori ham
bajarilmaydi. Bu qiymat yaroqsiz bo'lsa ikki yo'l bor: maydon `readObject`
da oshkor tiklanadi, yoki birinchi murojaatda lazy initsializatsiya
qilinadi. `static` maydon esa umuman seriyalanmaydi (`serialVersionUID`
dan boshqa), ya'ni unga `transient` qo'yish hech narsa qilmaydi va faqat
o'quvchini chalg'itadi.

Tez unutiladigan oxirgi qoida: `writeObject` `defaultWriteObject` ni,
`readObject` esa `defaultReadObject` ni **barcha maydon `transient`
bo'lgan holatda ham** chaqirishi shart. Sababi moslik: chaqiruv bor
shaklda keyingi relizda nontransient maydon qo'shilsa ham orqaga va
oldinga moslik saqlanadi, chaqiruv yo'q shaklda esa eski va yangi versiya
bir-birini o'qiy olmaydi.

Ikkinchisi: nusxa nazorati. `readObject` har chaqiruvda yangi obyekt yasaydi, shu sababli singleton deseriyalashdan keyin ikkinchi nusxa bo'lib qoladi. `readResolve` bilan tuzatish mumkin, lekin enum ishlatish ishonchliroq: enum nusxasining yagonaligini JVM kafolatlaydi va unda `readResolve` ni unutish xavfi yo'q.

Uchinchisi: seriyalash proxysi. Obyekt `writeReplace` da kichik statik ichki sinfga aylanadi, u faqat mantiqiy maydonlarni saqlaydi va `readResolve` da obyektni **konstruktor orqali** qaytaradi. Shu bilan deseriyalash konstruktorni chetlab o'tmaydi, invariant tekshiriladi va `readObject` ni himoyaviy yozish kerak bo'lmaydi.

```java
// yaxshi: seriyalash proxysi - deseriyalash konstruktordan o'tadi
private Object writeReplace() {
    return new Proxy(start, end);
}

private static final class Proxy implements Serializable {

    private static final long serialVersionUID = 1L;
    private final LocalDate start;
    private final LocalDate end;

    Proxy(LocalDate start, LocalDate end) { this.start = start; this.end = end; }

    private Object readResolve() {
        return DateRange.of(start, end);   // invariant shu yerda tekshiriladi
    }
}
```

Bitta chegarani alohida aytish kerak, chunki u bu bo'limning markaziy
da'vosini teskari aylantiradi. "Deseriyalash konstruktorni chetlab
o'tadi" qoidasi **record uchun amal qilmaydi**: record deseriyalashi
kanonik konstruktordan o'tadi, demak compact konstruktordagi validatsiya
oqimdan kelgan ma'lumotga ham qo'llanadi. Shu bilan birga record da
`writeObject`, `readObject`, `readResolve` va `Externalizable`
ishlamaydi, ya'ni seriyalangan shaklni qo'lda o'zgartirish yo'li yo'q.
Amaliy xulosa: `Serializable` majbur bo'lgan joyda ma'lumot tashuvchi tur
record bo'lsa, himoyaviy `readObject` ham, seriyalash proxysi ham kerak
bo'lmaydi; buning o'rniga oqim shakli ustidan nazorat yo'qoladi, demak
tanlov invariant qayerda tekshirilishiga qarab qilinadi.

## 25.5 Refleksiya narxi va uni chegaralash

Refleksiya tur xavfsizligini ish vaqtiga suradi: xato kompilyatsiyada emas, production da chiqadi. Bundan tashqari, refleksiya bilan yozilgan kod refaktoringga chidamsiz - nom o'zgarsa IDE uni topmaydi.

```java
// yomon: nom satrda - refaktoring buzadi, xato ish vaqtida chiqadi
Method method = service.getClass().getMethod("settle", Long.class);
method.invoke(service, paymentId);

// yaxshi: interfeys yoki funksional tur
PaymentOperation operation = service::settle;
operation.apply(paymentId);
```

Refleksiya haqli joylar: framework ichida (Spring, Jackson, JPA), test yordamchilarida, va plugin yuklashda. Biznes kodida esa deyarli har doim boshqa yechim bor.

Refleksiyadan qochib bo'lmagan joyda ikki amaliy tafsilot kodni
qisqartiradi. Birinchisi: refleksiv nusxa yaratish oltita turli istisno
tashlashi mumkin, va ularni alohida ushlash `catch` bloklarini metodning
yarmiga aylantiradi. Java 7 dan boshlab ularning umumiy superclassi bor:
bitta `catch (ReflectiveOperationException e)` oltita bandni almashtiradi
(19.2).

Ikkinchisi annotatsiyaga tegishli va u refleksiyani jim ishlamaydigan
qiladi. `@Retention` siyosati oshkor berilmasa `RetentionPolicy.CLASS`
qabul qilinadi: annotatsiya `.class` faylga tushadi, lekin ish vaqtida
refleksiya bilan ko'rinmaydi. O'z annotatsiyasi "ishlamayotganining"
birinchi sababi shu. Lokal o'zgaruvchi e'lonidagi annotatsiya esa `.class`
faylga umuman tushmaydi, demak uni ish vaqtida o'qishga bo'lgan umid
yolg'on: lokal o'zgaruvchi annotatsiyasi faqat kompilyator va statik
tahlilchi uchun ma'noga ega.

```java
// yomon: siyosat yozilmagan - ish vaqtida ko'rinmaydi
public @interface Audited { }

// yaxshi: refleksiya bilan o'qiladigan annotatsiya
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.METHOD, ElementType.TYPE})
public @interface Audited { }
```

## 25.6 `finalize`, `Cleaner` va resurs oxiri

`Object.finalize()` Java 9 dan deprecated va Java 18 dan o'chirilish yo'lida: uning bajarilishi kafolatlanmaydi, vaqti aniq emas, va GC ni sekinlashtiradi. `Cleaner` esa faqat **oxirgi himoya** sifatida haqli.

Qoida: resursni `AutoCloseable` va `try-with-resources` bilan boshqarish (19.4); `Cleaner` ni faqat native resurs (JNI buferi) uchun qo'shimcha xavfsizlik to'ri sifatida ishlatish.

"Kafolatlanmaydi" so'zi amalda nimani bildiradi, buni uch oqibat bilan
aytish kerak.

Birinchisi: finalizer yoki cleaner ga **doimiy holatni** yangilashni
ishonib topshirib bo'lmaydi. Taqsimlangan qulfni bo'shatish, hisoblagichni
kamaytirish, bazadagi "band" belgisini olib tashlash - bularning hammasi
finalizer da yozilsa, tizim o'zini jim qulflab qo'yishi mumkin, chunki
kod umuman bajarilmasligi ehtimoli bor.

Ikkinchisi: finalizer ni majburlash yo'li yo'q. `System.gc()` va
`System.runFinalization()` finalizer bajarilishini **oshirmaydi ham,
kafolatlamaydi ham**; ularni kafolat deb ishlatgan kod sinovda o'tib,
production da yiqiladi. Majburlash kafolatini bergan yagona metodlar
(`System.runFinalizersOnExit` va uning `Runtime` dagi juftligi) buzuq va
o'nlab yillardan beri deprecated.

Uchinchisi: finalizator ichida tutilmagan istisno **e'tiborsiz**
qoldiriladi va shu obyektning finalizatsiyasi o'sha joyda to'xtaydi.
Obyekt yarim tozalangan holda qoladi, log da hech narsa qolmaydi va
nosozlik faqat resurs tugaganda ko'rinadi. Boshqa hech bir joyda Java
istisnoni bu qadar jim yutmaydi.

To'rtinchi sabab xavfsizlikka tegishli va u `final` bo'lmagan sinfga
bevosita tegadi. **Finalizer hujumi** shunday ishlaydi: hujumchi sinfdan
voris oladi, vorisga finalizer yozadi, keyin konstruktorni istisno bilan
yiqitadi. Konstruktor tugamagan bo'lsa ham obyekt yaratilgan, demak GC
vaqti kelganda voris finalizeri **yarim qurilgan** obyekt ustida ishlaydi
va uning havolasini statik maydonga saqlab qolishi mumkin: shu bilan
invariant tekshiruvidan o'tmagan obyekt tizimga kiradi. `final` sinf bu
hujumga berilmaydi, chunki undan voris olinmaydi. Nofinal sinfni esa hech
narsa qilmaydigan `final` `finalize` metodi himoya qiladi: voris uni
ustiga yoza olmaydi.

```java
// Nofinal sinfni finalizer hujumidan himoya qilish
public class Account {

    // Hech narsa qilmaydi, lekin voris finalizer yozishini to'sadi
    @Override
    protected final void finalize() { }
}
```

`finalize` deprecated, shuning uchun bu himoya o'zi ogohlantirish beradi.
Birinchi tanlov boshqa: sinfni `final` qilish yoki vorislikni statik
fabrika va `private` konstruktor bilan yopish (17.1). Yuqoridagi shakl
faqat ierarxiyasi allaqachon ochiq bo'lgan eski kod uchun.

`Cleaner` ni ishlatganda bitta mexanik qoida bor va u 25.7 dagi umumiy
qoidaning aniq holati: tozalash harakatini tashiydigan holat obyekti
**tozalanadigan obyektga havola saqlamasligi** kerak, aks holda obyekt
hech qachon yig'ilmaydi va cleaner umuman ishga tushmaydi. Shuning uchun
u statik ichki sinf bo'ladi, va bu yerda lambda ishlatilmaydi: lambda
tashqi nusxani jim ushlab qoladi.

```java
public final class NativeBuffer implements AutoCloseable {

    private static final Cleaner CLEANER = Cleaner.create();

    // Statik: tashqi NativeBuffer ga havola yo'q
    private static final class State implements Runnable {

        private final long address;

        State(long address) { this.address = address; }

        @Override
        public void run() { free(address); }
    }

    private final Cleaner.Cleanable cleanable;

    public NativeBuffer(long size) {
        this.cleanable = CLEANER.register(this, new State(allocate(size)));
    }

    @Override
    public void close() { cleanable.clean(); }
}
```

## 25.7 Ichki sinf va yashirin tashqi havola

Nostatik ichki sinf (`inner class`) tashqi sinf nusxasiga yashirin havola saqlaydi. Natijada ichki sinf nusxasi yashasa, tashqi obyekt ham xotirada qoladi - bu klassik xotira oqishi (memory leak) sababi.

```java
// yomon: Listener tashqi Service ga havola saqlaydi, u GC qilinmaydi
public class SettlementService {
    class Listener implements EventListener { ... }       // nostatik
}

// yaxshi: statik ichki sinf - yashirin havola yo'q
public class SettlementService {
    static final class Listener implements EventListener { ... }
}
```

Qoida: ichki sinf tashqi nusxaga murojaat qilmasa, u `static` bo'lishi kerak. Bu qoidani Error Prone `ClassCanBeStatic` qoidasi topadi.

`static` dan tashqari yana ikki qaror bor: ichki sinf umuman kerakmi, va
qaysi turi kerak.

Birinchi savol mavjudlik mezoni bilan hal qilinadi: **ichki sinf faqat o'z
tashqi sinfiga xizmat qilishi kerak.** Agar u boshqa kontekstda ham
foydali bo'lsa, u ichki sinf emas, top-level sinf. Teskari harakat ham bor
va u kirishni kamaytiradi: `package-private` top-level sinfni faqat bitta
sinf ishlatayotgan bo'lsa, uni o'sha sinfning `private static` ichki
sinfiga aylantirish kerak, shunda tur paketdagi hamma sinfga emas, bitta
sinfga ko'rinadi.

`public` yoki `protected` ichki sinfda statik va nostatik tanlovi uslub
masalasi emas, **orqaga moslik** masalasi: tanlov API ga chiqadi va
keyingi relizda nostatikdan statikga o'tish mijoz kodini buzadi. Shu
sababli ko'rinadigan ichki sinfda bu qaror birinchi relizda to'g'ri
qilinadi.

To'rt turni tanlash qarori quyidagicha boradi.

| Shart | Tur |
|---|---|
| Metoddan tashqarida ko'rinishi kerak yoki tanasi uzun | a'zo sinf |
| A'zo sinf tashqi nusxaga havola talab qiladi | nostatik a'zo sinf |
| A'zo sinf tashqi nusxaga murojaat qilmaydi | `static` a'zo sinf |
| Metod ichida bitta joydan yaratiladi va mos tur allaqachon bor | anonim sinf yoki lambda (25.8) |
| Metod ichida yaratiladi, lekin mos tur yo'q yoki nom kerak | lokal sinf |

## 25.8 Anonim sinf va lambda tanlovi

Lambda qisqa va `this` ni tashqi sinfga bog'laydi; anonim sinf esa o'z `this` iga ega va holat saqlashi mumkin. Tanlov qoidasi oddiy.

| Ehtiyoj | Tanlov |
|---|---|
| Bitta abstrakt metod, holat yo'q | lambda |
| Bir nechta metod | anonim sinf yoki nomlangan sinf |
| Holat kerak | nomlangan sinf |
| `this` o'ziga tegishli bo'lishi kerak | anonim sinf |
| Qayta ishlatiladi | nomlangan sinf |
| Uch qatordan uzun | nomlangan metod yoki sinf (24.1) |

Jadvalga kirmagan, lekin tanlovni bir martada hal qiladigan shart ham
bor: **seriyalash.** Lambda va anonim sinfni implementatsiyalar bo'ylab
ishonchli seriyalab bo'lmaydi, chunki ularning seriyalangan shakli
kompilyator qurgan yashirin nomga bog'liq va u boshqa kompilyatorda yoki
boshqa JDK da boshqacha bo'lishi mumkin. Seriyalanadigan funksional
obyekt kerak bo'lsa (masalan `Comparator` ni seriyalanadigan sinf
maydonida saqlash), lambda emas, `private static` ichki sinf nusxasi
ishlatiladi.

## 25.9 `enum` da xatti-harakat, `EnumMap`, `EnumSet`, `valueOf`

Enum Java da oddiy konstanta to'plamidan ancha ko'proq: u xatti-harakat saqlashi mumkin (6.10) va o'ziga mos to'plamlari bor.

`EnumMap` va `EnumSet` oddiy `HashMap`/`HashSet` dan tez va kam xotira oladi, chunki ular massivga asoslangan. Enum kalit ishlatilganda ularni tanlash standart bo'lishi kerak.

```java
// yaxshi: EnumMap - tartib enum e'loni bo'yicha, tez
Map<SettlementStatus, Long> counts = new EnumMap<>(SettlementStatus.class);
Set<SettlementStatus> terminal = EnumSet.of(SETTLED, REJECTED);
```

`EnumSet` nega bit maydonni almashtiradi, buni bilib qo'yish kerak, chunki
eski kodda bit maydon hali ham uchraydi. Bit maydon (`int` ichida
bayroqlarni `|` bilan yig'ish) uch narsani yo'qotadi: chop etilganda
qiymat o'qilmaydi (`6` degan son nimani bildiradi), elementlar bo'ylab
aylanish yo'li yo'q, va API yozilganda maksimal bayroq soni oldindan
tanlanishi kerak, chunki `int` 32, `long` esa 64 dan oshmaydi. `EnumSet`
uchalasini ham yo'qotmaydi: `toString` o'qiladi, to'plam iteratsiya
qilinadi va a'zo sonining chegarasi API ga chiqmaydi.

ESLATMA: Bloch 2018 da o'zgarmas `EnumSet` yaratish yo'li yo'qligini
yozadi va vaqtinchalik yechim sifatida `Collections.unmodifiableSet`
bilan o'rashni beradi, bunda qisqalik va `EnumSet` ning tezligi
yo'qoladi. Bu holat Java 9 ga tegishli, joriy JDK da o'zgargan bo'lishi
mumkin: o'zgarmas enum to'plami kerak bo'lsa avval joriy JDK hujjatiga
qaraladi (16.3).

Ikki enum bo'yicha indekslanadigan o'tish jadvali (holat mashinasida
`from` va `to` juftligi) uchun `ordinal()` bilan ikki o'lchovli massiv
yozish namunasi ko'p uchraydi va u ikki marta sinadi: yangi konstanta
qo'shilganda massiv o'lchamini qo'lda to'g'rilash kerak bo'ladi, va
`ordinal()` siljishi jim buzilish beradi (25.11). To'g'ri shakl -
ichma-ich `EnumMap`: tashqi xarita `from` bo'yicha, ichki xarita `to`
bo'yicha.

```java
// yaxshi: ichma-ich EnumMap - yangi konstanta o'lcham tuzatishni talab qilmaydi
private static final Map<Status, Map<Status, Transition>> TRANSITIONS =
        Stream.of(Transition.values())
                .collect(groupingBy(Transition::from,
                        () -> new EnumMap<>(Status.class),
                        toMap(Transition::to, identity(),
                                (first, second) -> first,
                                () -> new EnumMap<>(Status.class))));
```

`valueOf` tuzog'i: noma'lum nom uchun `IllegalArgumentException` tashlaydi va bu tashqi ma'lumotni parslaganda kutilmagan 500 xatoga olib keladi.

```java
// yomon: tashqi qiymat uchun IllegalArgumentException
SettlementStatus status = SettlementStatus.valueOf(input);

// yaxshi: xavfsiz parslash
static Optional<SettlementStatus> parse(String input) {
    return Arrays.stream(values())
            .filter(s -> s.name().equalsIgnoreCase(input))
            .findFirst();
}
```

Enum mexanikasida yana to'rt tuzoq bor va ularning hammasi "enum ham
sinf, lekin oddiy sinf emas" degan gapdan chiqadi.

**Konstruktor yashirin `private`.** Unga `public` yoki `protected`
yozilsa kod kompilyatsiya qilinmaydi. Sabab mexanikada emas, shartnomada:
enum nusxalari faqat e'lon ichida yaratiladi.

**Konstruktor enum ning statik maydonlariga kira olmaydi** (konstanta
o'zgaruvchilardan boshqa), chunki statik maydonlar konstantalar
yaratilgandan KEYIN initsializatsiya qilinadi. Shuning uchun "kodni
konstantaga moslaydigan xaritani konstruktordan to'ldirish" namunasi
ishlamaydi; xarita statik blokda, konstantalar tayyor bo'lganidan keyin
to'ldiriladi (25.2).

```java
enum SettlementStatus {
    PENDING(10), SETTLED(20), REJECTED(30);

    private static final Map<Integer, SettlementStatus> BY_CODE = new HashMap<>();

    private final int code;

    SettlementStatus(int code) {
        this.code = code;
        // BY_CODE.put(code, this);   // kompilyatsiya xatosi: statik maydon hali yo'q
    }

    static {
        for (SettlementStatus status : values()) {
            BY_CODE.put(status.code, status);        // konstantalar tayyor
        }
    }
}
```

**Konstruktorga uzatilgan lambda statik kontekstda baholanadi**, ya'ni u
enum ning nusxa a'zolariga (`this`, `code`) kira olmaydi. Shuning uchun
konstruktorga funksiya uzatish bilan qurilgan strategiya faqat nusxa
holatiga tayanmaydigan xatti-harakat uchun ishlaydi; qolgan hollarda
konstantaga xos sinf tanasi qoladi.

**`equals` yozish kerak emas.** Enum nusxa nazoratli tur: har konstanta
yagona nusxa, demak mantiqiy tenglik identifikatsiya tengligi bilan
ustma-ust tushadi va `Object.equals` to'g'ri javob beradi. Shu sababli
enum solishtirish `==` bilan yoziladi (15.5), `equals` va `hashCode` ni
ustiga yozish esa faqat xato kiritadi.

Oxirgi qoida joylashuvga tegishli: enum ning faqat sinf yoki paket ichida
kerak bo'lgan xatti-harakati `private` yoki `package-private` metod
bo'ladi, hammasi `public` qilinmaydi. Enum ning o'zi ham shu mezon bilan
joylashtiriladi: umumiy foydali bo'lsa top-level tur, bitta sinfga
bog'liq bo'lsa shu sinfning a'zo sinfi (25.7).

## 25.10 Kompilyator ogohlantirishlari: `-Xlint`, `-Werror`, Error Prone, NullAway

Kompilyator eng arzon statik tahlilchi va u ko'pincha o'chirilgan holda qoldiriladi. Ogohlantirishlarni xatoga aylantirish eng yuqori foyda beradigan bir martalik sozlama.

```xml
<plugin>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <!-- Barcha ogohlantirishlar yoqilgan va xatoga aylantirilgan -->
      <arg>-Xlint:all</arg>
      <arg>-Werror</arg>
      <!-- Parametr nomlari saqlanadi: Spring va Jackson uchun kerak -->
      <arg>-parameters</arg>
      <!-- Error Prone va NullAway ulanishi -->
      <arg>-XDcompilePolicy=simple</arg>
      <arg>--should-stop=ifError=FLOW</arg>
      <arg>-Xplugin:ErrorProne -Xep:NullAway:ERROR -XepOpt:NullAway:AnnotatedPackages=uz.shop</arg>
    </compilerArgs>
    <annotationProcessorPaths>
      <path>
        <groupId>com.google.errorprone</groupId>
        <artifactId>error_prone_core</artifactId>
        <version>2.42.0</version>
      </path>
      <path>
        <groupId>com.uber.nullaway</groupId>
        <artifactId>nullaway</artifactId>
        <version>0.12.10</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

Bu konfiguratsiyaning o'zi JDK 16+ da ishlamaydi: Error Prone `jdk.compiler` ning ichki paketlariga murojaat qiladi, ular esa JEP 396 va JEP 403 dan beri yopiq, build `IllegalAccessError` bilan yiqiladi. Kompilyator Maven JVM ichida ishlasa (standart holat), loyiha ildizidagi `.mvn/jvm.config` fayliga quyidagilar yoziladi ([Error Prone o'rnatish hujjati](https://github.com/google/error-prone/blob/e92eb85f9ba728f07e6a49ca7732cedb4a0c64c9/docs/installation.md#maven)):

```text
--add-exports jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.main=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.model=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.processing=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED
--add-exports jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED
--add-opens jdk.compiler/com.sun.tools.javac.code=ALL-UNNAMED
--add-opens jdk.compiler/com.sun.tools.javac.comp=ALL-UNNAMED
```

Kompilyator alohida jarayonda ishlasa (`<fork>true</fork>` yoki `maven-toolchains-plugin`), xuddi shu qatorlar `compilerArgs` ichiga `-J` prefiksi bilan qo'shiladi: `<arg>-J--add-exports=jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED</arg>` va hokazo. Shu hujjatga ko'ra joriy Error Prone JDK 21 yoki undan yangi JDK da ishga tushadi, JDK 21 da esa `-XDaddTypeAnnotationsToSymbol=true` argumenti ham kerak. Versiya raqamlarini Error Prone ning joriy o'rnatish hujjatiga solishtiring.

Error Prone bu hujjatdagi ko'p qoidalarni avtomatik tekshiradi: `EqualsHashCode`, `Finally`, `ClassCanBeStatic`, `StringSplitter`, `DefaultCharset`, `JavaUtilDate`, `BigDecimalEquals`, `UnusedVariable` (42.2).

Ogohlantirishlar ushlaydigan eskirgan til xususiyatlaridan biri
`strictfp`. Bu modifikator suzuvchi nuqta ifodalarini qat'iy IEEE 754
semantikasiga majburlash uchun kerak edi; JLS uni bugun **eskirgan**
(obsolete) deb belgilaydi, chunki suzuvchi nuqta ifodalari baribir
qat'iy baholanadi, demak modifikator hech narsa qilmaydi. Qoida: yangi
kodda `strictfp` yozilmaydi, eski koddagisi esa olib tashlanadi.

## 25.11 `ordinal()` ga tayanmaslik, enum ni interfeys bilan kengaytirish va `@Override`

Enum bilan ishlashda uchta qoida ko'p xatoni to'sadi va ularning hammasi bir xil sababga ega: enum e'loni o'zgaradi, kod esa o'zgarmaganday ishlaydi.

Birinchisi `ordinal()`. U enum a'zosining e'londagi tartibini qaytaradi, ya'ni a'zolar o'rin almashsa yoki orasiga yangi a'zo qo'shilsa qiymat jim o'zgaradi. Bazaga, faylga yoki tashqi API ga `ordinal()` yozilgan bo'lsa, ma'lumot buziladi.

```java
// yomon: tartibga tayanish - yangi a'zo qo'shilsa qiymat siljiydi
int code = status.ordinal();

// yaxshi: o'z maydoni, e'lon tartibidan mustaqil
enum SettlementStatus {
    PENDING(10), SETTLED(20), REJECTED(30);

    private final int code;

    SettlementStatus(int code) { this.code = code; }

    public int code() { return code; }
}
```

Taqiqning chegarasi ham aytilishi kerak, aks holda u mutlaq ko'rinadi.
`Enum` spetsifikatsiyasi `ordinal()` ni `EnumSet` va `EnumMap` kabi
**umumiy maqsadli enum tuzilmalari** uchun mo'ljallangan deb yozadi.
Ya'ni uning yagona haqli ishlatilishi shunday tuzilmaning o'zini yozish;
siz shunday kod yozmayotgan bo'lsangiz, `ordinal()` dan butunlay voz
kechish kerak, "faqat log uchun" degan istisno ham qolmaydi.

Ikkinchisi kengaytirish. Enum dan voris olib bo'lmaydi, lekin enum interfeys implementatsiya qilishi mumkin: shu bilan bir xil shartnomani qo'shimcha enum lar ham bajaradi va chaqiruvchi kod interfeys turi bilan ishlaydi.

```java
public interface FeeRule {
    Money apply(Money amount);
}

enum StandardFeeRule implements FeeRule {
    FLAT { public Money apply(Money a) { return a.plus(Money.of("0.50")); } },
    PERCENT { public Money apply(Money a) { return a.multiply(new BigDecimal("0.015")); } }
}
```

Interfeys bilan taqlid qilingan kengaytiriladigan enum ning ikki
tafsiloti amalda chiqadi.

Birinchisi: implementatsiya bir enum dan boshqasiga **meros bo'lmaydi**,
chunki enum dan voris olinmaydi. Natijada ikki enum bir xil kodni
takrorlaydi. Agar xatti-harakat nusxa holatiga tayanmasa, u interfeysning
`default` metodiga chiqariladi; tayansa, yordamchi sinf yoki statik
yordamchi metodga chiqarilib, har enum shu metodni chaqiradi (17.7).

Ikkinchisi: kengaytma enumini **butun to'plam** sifatida metodga
uzatishning ikki shakli bor, va tanlov bitta savolga bog'liq - `EnumSet`
yoki `EnumMap` kerakmi.

| Shakl | Nima beradi | Nima yo'qotadi |
|---|---|---|
| `<T extends Enum<T> & Operation> void run(Class<T> type)` | chegaralangan tur tokeni: `EnumSet.allOf(type)` va `EnumMap` ishlatiladi | bitta chaqiruvda bitta enum turi |
| `void run(Collection<? extends Operation> ops)` | soddaroq imzo, bir nechta enum turini aralashtirishga ruxsat beradi | `EnumSet` va `EnumMap` yo'qoladi |

Uchinchisi `@Override`. Uni har bir ustiga yozilgan metodga qo'yish qoida: imzo mos kelmasa (nom xato, parametr turi boshqa) kompilyator darhol xato beradi, aks holda metod yangi metod bo'lib qoladi va hech kim chaqirmaydi. Bu ayniqsa `equals(Object)` da ko'p uchraydi: `equals(MyType)` yozilsa kod kompilyatsiya bo'ladi, lekin `HashMap` eski `equals` ni chaqiradi. Abstrakt metodni implementatsiya qilganda ham yoziladi: kompilyator talab qilmaydi, lekin niyatni qayd qiladi.

## 25.12 Deseriyalashga hujum va undan himoya

Oldingi bo'limlar natijani aytadi: yangi kodda `Serializable`
ishlatilmaydi. Bu bo'lim yo'lni aytadi, chunki eski kodda `Serializable`
qolgan bo'ladi va uni xavfsiz ushlash kerak. Markaziy fikr bitta:
**deseriyalash hujumchi yozadigan konstruktor.** `readObject` oqimdan
kelgan baytlarni obyektga aylantiradi, bayt esa hujumchi nazoratida
bo'lishi mumkin, demak `readObject` xuddi `public` konstruktor kabi
qaraladi: u har argumentni tekshiradi va hech kimga o'z ichki holatiga
havola bermaydi.

**Himoyalangan nusxa deseriyalashda ham olinadi.** Konstruktorda ichki
o'zgaradigan komponentdan nusxa olish qoidasi (14.7) `readObject` ga ham
tegishli, lekin sabab boshqa: hujumchi oqimga "yolg'on obyekt havolalari"
qo'shib, deseriyalangan obyektning ichki maydoniga tashqaridan ushlab
turiladigan havola qoldirishi mumkin. Shundan keyin obyekt o'zgarmas
bo'lib ko'rinadi, lekin uning ichidagi sana yoki ro'yxat tashqaridan
o'zgartiriladi. Qoida: **mijoz egalik qilmasligi kerak bo'lgan havolani
saqlaydigan har maydondan** `readObject` ichida himoyalangan nusxa
olinadi.

Buning uchta mexanik tafsiloti bor va har biri alohida xato manbasi:

- Nusxa **tekshiruvdan oldin** olinadi. Teskari tartibda tekshiruv
  original obyekt ustida bajariladi, hujumchi esa tekshiruvdan keyin uni
  o'zgartiradi.
- Nusxa `clone` bilan olinmaydi: `clone` voris sinfning
  implementatsiyasini, ya'ni hujumchining kodini chaqirishi mumkin
  (15.8).
- Nusxa `final` maydonga tayinlanmaydi, chunki `readObject` konstruktor
  emas. Shuning uchun himoyaviy `readObject` yozilgan sinfda shu
  maydonlarni **nofinal** qilishga to'g'ri keladi, va bu `readObject`
  ning yashirin narxlaridan biri.

```java
private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
    in.defaultReadObject();

    // 1) oldin nusxa: clone emas, konstruktor
    start = new Date(start.getTime());
    end = new Date(end.getTime());

    // 2) keyin tekshiruv - nusxa ustida
    if (start.compareTo(end) > 0) {
        throw new InvalidObjectException("start end dan keyin");
    }
}
```

**Sukut `readObject` yaroqlimi: lakmus testi.** `readObject` yozish
kerakmi yoki sukut shakl yetadimi degan savolga qisqa javob bor.
O'zingizdan so'rang: shu sinfga har nontransient maydon qiymatini **hech
qanday validatsiyasiz** qabul qiladigan `public` konstruktor qo'shishga
rozimisiz? Rozi bo'lsangiz sukut `readObject` yetadi. Rozi bo'lmasangiz
ikki yo'l qoladi: tekshiruvchi `readObject` yozish yoki seriyalash
proxysiga o'tish. Bu test review da bir chaqiruvda ishlaydi, chunki u
mexanikani emas, invariant bor-yo'qligini so'raydi.

**`readResolve` va nusxani o'g'irlash.** Seriyalanadigan singleton
`readResolve` bilan tuzatilganda bitta qo'shimcha shart paydo bo'ladi:
sinfning **barcha nusxa maydonlari `transient` bo'lishi shart.** Aks
holda hujum shunday boradi: hujumchi oqimga sinfning nusxasini va o'sha
nusxaning nontransient maydoniga ishora qiladigan havolani qo'shadi;
deseriyalash `readResolve` ni chaqirishdan OLDIN maydonlarni to'ldiradi,
demak hujumchining havolasi `readResolve` qaytargan kanonik nusxadan
boshqa, ikkinchi obyektga yetib boradi. Natijada "yagona" deb
hujjatlangan sinfdan ikki nusxa qoladi.

Shu bilan birga `readResolve` eskirgan emas. Enum afzalligi o'z o'rnida,
lekin nusxalari **kompilyatsiya vaqtida ma'lum bo'lmagan** nusxa
nazoratli seriyalanadigan sinfni enum bilan ifodalab bo'lmaydi: shunday
holda `readResolve` qoladi va yuqoridagi `transient` sharti majburiy
bo'ladi.

`readResolve` va `writeReplace` ning kirish darajasi xulqni
o'zgartiradi, shuning uchun u tasodifan tanlanmaydi.

| Sinf | Kirish darajasi | Natija |
|---|---|---|
| `final` | `private` | to'g'ri: metod faqat shu sinfga tegishli |
| nofinal | `private` | voris sinflarda qo'llanmaydi, ya'ni himoya jim yo'qoladi |
| nofinal | `protected` yoki `public`, voris override qilmagan | deseriyalash superclass nusxasini qaytaradi va chaqiruv joyida `ClassCastException` beradi |
| vorislik uchun mo'ljallangan | `protected`, voris override qiladi | to'g'ri: voris o'z shakli uchun javobgar |

**Seriyalash proxysida himoya `readObject`.** Proxy naqshi deseriyalashni
konstruktordan o'tkazadi, lekin naqsh o'z-o'zidan to'liq emas:
`writeReplace` bor bo'lsa ham hujumchi **tashqi sinfning** seriyalangan
nusxasini qo'lda yasab oqimga qo'yishi mumkin, chunki tashqi sinf hamon
`Serializable`. Shuni to'sish uchun tashqi sinfga hamisha istisno
tashlaydigan `readObject` qo'shiladi, ya'ni proxy naqshi uch metoddan
iborat: `writeReplace`, proxy ning `readResolve` i va tashqi sinfning
himoya `readObject` i.

```java
// Tashqi sinf faqat proxy orqali deseriyalanadi
private void readObject(ObjectInputStream in) throws InvalidObjectException {
    throw new InvalidObjectException("proxy talab qilinadi");
}
```

Proxy naqshining ikki cheklovi bor va ular qachon ishlatilmasligini
belgilaydi. Birinchisi: u **mijoz kengaytira oladigan** sinflar bilan
sig'ishmaydi, chunki proxy qaytaradigan tur aniq sinf bo'ladi.
Ikkinchisi: obyekt grafida aylana bo'lsa, `readResolve` ichidan obyektning
metodini chaqirish `ClassCastException` beradi, chunki o'sha paytda graf
hali to'liq tiklanmagan va havola proxy ga ishora qilib turadi.

Oxirgi hujum shakli mexanizmi bo'yicha boshqa, lekin uning himoyasi shu
yerda turadi: **deseriyalash bombasi.** Qisqa oqim ichida ichma-ich
to'plamlar grafi yasaladi, uning deseriyalashi esa amalda tugamaydi,
chunki `hashCode` chaqiruvlari soni chuqurlik bilan keskin o'sadi. Bu
yerda na `readObject`, na proxy yordam beradi: himoya faqat ishonchsiz
baytni umuman deseriyalash qilmaslik, yoki deseriyalashni filtr bilan
chegaralash (`java.io.ObjectInputFilter`). Shu sababli bu bo'limdagi
hamma qoida 25.4 ning asosiy qoidasidan keyin turadi: ular `Serializable`
ni xavfsiz qilmaydi, faqat uning narxini kamaytiradi.

Finalizer hujumi ham seriyalanadigan sinfga tegadi, lekin u
deseriyalashdan emas, konstruktordan boshlanadi, shuning uchun u 25.6 da
yozilgan.

## 25.13 Amalda qo'llash

- [ ] `Optional` tipidagi maydon va parametrlarni topib, maydonni `null` ga va getter ni `Optional` ga o'tkazing.
- [ ] Statik initializator ichidagi I/O va tashqi chaqiruvlarni bean konstruktoriga yoki lazy supplier ga ko'chiring.
- [ ] Uzun `instanceof` zanjirlarini `sealed` interfeys va `switch` pattern matching ga o'tkazing.
- [ ] `Serializable` ishlatilgan joylarni ro'yxatlab, yangi kodda taqiqlang; qolganlarida `serialVersionUID` va `transient` ni tekshiring.
- [ ] Biznes kodidagi refleksiyani interfeys yoki funksional turga almashtiring.
- [ ] Nostatik ichki sinflarni `static` qilib, Error Prone `ClassCanBeStatic` ni yoqing.
- [ ] `Enum.valueOf` tashqi ma'lumot bilan chaqirilgan joylarni xavfsiz parslashga o'tkazing.
- [ ] `-Xlint:all -Werror` va Error Prone + NullAway ni build ga qo'shib, chiqqan ogohlantirishlarni bosqichma-bosqich tuzating.
- [ ] `ordinal()` chaqiruvlarini grep bilan topib, saqlanadigan yoki uzatiladigan joylarini o'z kod maydoniga o'tkazing.
- [ ] Ustiga yozilgan metodlarda `@Override` yo'qligini linter qoidasi bilan ushlang.
- [ ] `Serializable` sinflarda `transient` qilish mumkin bo'lgan maydonlarni (keshlangan hash, hosilaviy qiymat, native ko'rsatkich) topib `transient` qiling va ularning deseriyalashdagi tiklanishini tekshiring.
- [ ] Har bir `readObject` uchun lakmus testini qo'llang: validatsiyasiz `public` konstruktorga rozimisiz; rozi bo'lmasangiz tekshiruv yoki seriyalash proxysini qo'shing.
- [ ] `readResolve` ishlatilgan sinflarda barcha nusxa maydonlari `transient` ekanini va metod kirish darajasi sinfning `final` holatiga mos ekanini tekshiring.
- [ ] Seriyalash proxysi bor sinflarga istisno tashlaydigan `readObject` qo'shilganini tekshiring.
- [ ] Nofinal sinflarda finalizer hujumi yo'lini yopib qo'ying: sinfni `final` qiling yoki vorislikni konstruktor ko'rinishi bilan cheklang.
- [ ] `System.gc()` yoki `System.runFinalization()` ni tozalash kafolati deb ishlatgan joylarni `try-with-resources` ga o'tkazing.
- [ ] `ordinal()` bilan indekslangan massivlarni `EnumMap` yoki ichma-ich `EnumMap` ga o'tkazing.

## Manbalar

- Boyarsky/Selikoff, *OCP Java SE 17 Developer Practice Tests*, 3-bob javoblari (90 va 179-savollar) - instans havolasi orqali static a'zoga murojaat qonuniy, lekin tavsiya etilmasligi; `static final` maydonni statik metodda o'zgartirish kompilyatsiya qilinmasligi va bir xil nomli lokal o'zgaruvchi holatida tayinlashning lokalga tushishi
- Joshua Bloch, *Effective Java* 3rd, Item 34, 35 - int konstanta o'rniga enum, ordinal o'rniga instance maydon
- Joshua Bloch, *Effective Java* 3rd, Item 36, 37 - `EnumSet` va `EnumMap`
- Joshua Bloch, *Effective Java* 3rd, Item 38 - enum ni interfeys bilan kengaytirish
- Joshua Bloch, *Effective Java* 3rd, Item 40 - `@Override` ni izchil ishlatish
- Joshua Bloch, *Effective Java* 3rd, Item 85, 86 - Java serializatsiyasiga alternativa va ehtiyotkorlik
- Joshua Bloch, *Effective Java* 3rd, Item 8 - finalizer va cleaner dan voz kechish
- Joshua Bloch, *Effective Java* 3rd, Item 87 - o'z seriyalangan shakli
- Joshua Bloch, *Effective Java* 3rd, Item 89 - nusxa nazorati uchun `readResolve` emas enum
- Joshua Bloch, *Effective Java* 3rd, Item 90 - seriyalash proxysi
- Joshua Bloch, *Effective Java* 3rd, Item 6, 7 - keraksiz obyekt yaratmaslik, eskirgan havolani tozalash
- Joshua Bloch, *Effective Java* 3rd, Item 8 - finalizer va cleaner dan voz kechish
- Joshua Bloch, *Effective Java* 3rd, Item 24 - statik ichki sinfni nostatikdan afzal ko'rish
- Joshua Bloch, *Effective Java* 3rd, Item 65 - refleksiya o'rniga interfeys
- Herbert Schildt, *Java The Complete Reference*, 13-bob - `try-with-resources` va boshqa mavzular
- Joshua Bloch, *Effective Java* 3rd, Item 8 (30-31, 33-betlar) - finalizer va cleaner ga doimiy holatni ishonib topshirmaslik; `System.gc` va `System.runFinalization` ning kafolat bermasligi va `runFinalizersOnExit` ning buzuqligi; finalizer hujumi, `final` sinfning himoyaligi va hech narsa qilmaydigan `final finalize` himoyasi; `Cleaner` holat obyektining tashqi obyektga havola saqlamasligi va lambda ishlatilmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 10 (38-bet) - nusxa nazoratli sinfda (enum) mantiqiy tenglik identifikatsiya tengligi bilan ustma-ust tushishi va `Object.equals` ning yetarliligi
- Joshua Bloch, *Effective Java* 3rd, Item 15 (74-bet) - faqat bitta sinf ishlatadigan `package-private` top-level sinfni `private static` ichki sinfga aylantirish
- Joshua Bloch, *Effective Java* 3rd, Item 19 (97-bet) - vorislik uchun mo'ljallangan `Serializable` sinfda `readResolve` va `writeReplace` ning `protected` bo'lishi
- Joshua Bloch, *Effective Java* 3rd, Item 24 (112, 114-betlar) - ichki sinfning faqat o'z tashqi sinfiga xizmat qilishi; ko'rinadigan ichki sinfda statik va nostatik tanlovining orqaga moslikka ta'siri; to'rt tur (statik a'zo, nostatik a'zo, anonim, lokal) uchun tanlov qoidasi
- Joshua Bloch, *Effective Java* 3rd, Item 34 (161, 164-betlar) - enum metodining va enum ning o'zining ko'rinishi va joylashuvi; enum konstruktorining statik maydonlarga kira olmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 35 (168-bet) - `ordinal()` ning yagona haqli ishlatilishi: `EnumSet` va `EnumMap` kabi umumiy maqsadli enum tuzilmalari
- Joshua Bloch, *Effective Java* 3rd, Item 36 (169-170-betlar) - bit maydonning uch kamchiligi (o'qilmaydigan chiqish, iteratsiya yo'qligi, maksimal bit sonining oldindan tanlanishi); Java 9 holatiga ko'ra o'zgarmas `EnumSet` yaratish mumkin emasligi va `Collections.unmodifiableSet` bilan o'rash
- Joshua Bloch, *Effective Java* 3rd, Item 37 (174-bet) - ikki enum bo'yicha indekslanadigan jadval uchun `ordinal` massivi o'rniga ichma-ich `EnumMap`
- Joshua Bloch, *Effective Java* 3rd, Item 38 (178-179-betlar) - kengaytma enumini butun to'plam sifatida uzatishning ikki shakli (`Class<T>` tur tokeni va `Collection<? extends Operation>`) va ularning qiyosi; implementatsiyaning bir enum dan boshqasiga meros bo'lmasligi va `default` metod yoki yordamchi sinfga chiqarish
- Joshua Bloch, *Effective Java* 3rd, Item 42 (196-bet) - enum konstruktoriga uzatilgan lambdaning statik kontekstda baholanishi; lambda va anonim sinfni implementatsiyalar bo'ylab ishonchli seriyalab bo'lmasligi va `private static` ichki sinf yechimi
- Joshua Bloch, *Effective Java* 3rd, Item 65 (284-bet) - refleksiv nusxa yaratishning oltita istisnosi va `ReflectiveOperationException` bilan bitta `catch`
- Joshua Bloch, *Effective Java* 3rd, Item 86 (344-bet) - `Serializable` ning uchinchi narxi: versiyalar bo'ylab ikki yo'nalishli moslik testi va test hajmining sinflar hamda relizlar soni ko'paytmasiga proporsionalligi
- Joshua Bloch, *Effective Java* 3rd, Item 87 (348, 350, 351-betlar) - sukut seriyalangan shaklning to'rt zarari (API ga umrbod bog'lanish, ortiqcha joy, ortiqcha vaqt, stack overflow); barcha maydon `transient` bo'lganda ham `defaultWriteObject` va `defaultReadObject` ni chaqirish sharti; `transient` qilish mumkin bo'lgan har maydonni `transient` qilish va `transient` maydonning deseriyalashda default qiymat olishi
- Joshua Bloch, *Effective Java* 3rd, Item 88 (357-358-betlar) - deseriyalashda mijoz egalik qilmasligi kerak bo'lgan har maydondan himoyalangan nusxa olish va "yolg'on obyekt havolalari" hujumi; nusxaning tekshiruvdan oldin olinishi, `clone` ishlatilmasligi va `final` maydon cheklovi; sukut `readObject` uchun lakmus testi
- Joshua Bloch, *Effective Java* 3rd, Item 89 (359, 362-betlar) - `readResolve` ishlatilganda barcha nusxa maydonlarining `transient` bo'lishi sharti va nusxani o'g'irlash hujumi; `readResolve` ning eskirgan emasligi; `readResolve` kirish darajasining `final` va nofinal sinfdagi oqibatlari
- Joshua Bloch, *Effective Java* 3rd, Item 90 (364, 366-betlar) - seriyalash proxysi bo'lsa ham tashqi sinfga istisno tashlaydigan `readObject` qo'shish zarurati; proxy naqshining ikki cheklovi (mijoz kengaytiradigan sinflar va obyekt grafidagi aylana)
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 7-bob (364-bet) - enum konstruktorining yashirin `private` ekani va unga `public` yoki `protected` yozilsa kompilyatsiya bo'lmasligi
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 14-bob (826-bet) - faqat instans a'zolarining seriyalanishi (`serialVersionUID` dan boshqa), `static` maydonga `transient` qo'yishning ma'nosizligi va `transient` instans maydonining deseriyalashda tur default qiymatini olishi
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 14-bob ("Applying the Serializable Interface" bo'limi) - `Serializable` ning faqat ma'lumotga yo'naltirilgan sinf uchun mosligi, jarayonga yo'naltirilgan sinfning (I/O oqimi, `Thread`) yomon nomzod ekani
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 12-bob (296, 303-betlar) - lokal o'zgaruvchi e'lonidagi annotatsiyaning `.class` faylga tushmasligi; `@Retention` siyosati berilmaganda `CLASS` qabul qilinishi va annotatsiyaning ish vaqtida ko'rinmasligi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 3-bob (31-bet) - `strictfp` ning eskirgan (obsolete) kalit so'z ekani
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 11-bob (429-bet) - statik initializator va sinf o'zgaruvchisi initsializatorining tekshiriladigan istisno tashlay olmasligi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 12-bob (456-bet) - finalizator ichidagi tutilmagan istisnoning e'tiborsiz qoldirilishi va shu obyekt finalizatsiyasining to'xtashi
- [JEP 395: Records](https://openjdk.org/jeps/395) - record deseriyalashining kanonik konstruktordan o'tishi; `writeObject`, `readObject`, `readResolve` va `Externalizable` ning record da ishlamasligi
- ESLATMA: deseriyalash bombasi va `java.io.ObjectInputFilter` bilan chegaralash Bloch ning Item 85 dagi umumiy ogohlantirishiga tayanadi; filtrning aniq parametrlari korpus matniga kiritilmagan, chunki ular JDK versiyasiga bog'liq
- ESLATMA: `Cleaner` ning statik holat sinfi, ichma-ich `EnumMap` ni `groupingBy` bilan qurish, himoya `readObject` va nofinal sinfni `final finalize` bilan yopish uchun berilgan Java kod misollari korpus qo'shimchasi; kitoblar qoidani beradi, bu shaklda kod bermaydi
- ESLATMA: Bloch 2018 da o'z mashinasida o'lchagan tezlanish koeffitsiyentlari korpusga ko'chirilmagan, chunki ular mashinaga, JDK ga va yuklamaga bog'liq

---

[&larr; 24. Lambda, oqim va funksional uslub tozaligi](24-lambda-oqim-va-funksional-uslub-tozaligi.md) · [Mundarija](README.md) · [26. Spring kodining tozaligi &rarr;](26-spring-kodining-tozaligi.md)
