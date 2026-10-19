<!-- doc: clean-code | chapter: 11 | part: IV. Formatlash va kod uslubi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 11. Vertikal formatlash (Vertical Formatting)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [11.1 Fayl o'lchami va sinf uzunligi](#111-fayl-olchami-va-sinf-uzunligi)
- [11.2 Gazeta metaforasi: yuqoridan pastga ma'lumot zichligi](#112-gazeta-metaforasi-yuqoridan-pastga-malumot-zichligi)
- [11.3 Tushunchalar orasida bo'sh qator](#113-tushunchalar-orasida-bosh-qator)
- [11.4 Vertikal zichlik: birga o'qiladigan qatorlarni ajratmaslik](#114-vertikal-zichlik-birga-oqiladigan-qatorlarni-ajratmaslik)
- [11.5 Vertikal masofa: e'lon va ishlatish orasidagi oraliq](#115-vertikal-masofa-elon-va-ishlatish-orasidagi-oraliq)
- [11.6 Maydonlar joylashuvi va a'zolar tartibi](#116-maydonlar-joylashuvi-va-azolar-tartibi)
- [11.7 Bog'liq funksiyalarni yonma-yon qo'yish](#117-bogliq-funksiyalarni-yonma-yon-qoyish)
- [11.8 Tushunchaviy yaqinlik](#118-tushunchaviy-yaqinlik)
- [11.9 Vertikal tartib: chaqiruvchi yuqorida](#119-vertikal-tartib-chaqiruvchi-yuqorida)
- [11.10 Lokal o'zgaruvchi qamrovini kichik ushlash va faylda bitta top-level sinf](#1110-lokal-ozgaruvchi-qamrovini-kichik-ushlash-va-faylda-bitta-top-level-sinf)
- [11.11 Formatlashning asosiy teoremasi va yaxshi joylashuv maqsadlari](#1111-formatlashning-asosiy-teoremasi-va-yaxshi-joylashuv-maqsadlari)
- [11.12 Amalda qo'llash](#1112-amalda-qollash)

</details>


Formatlash did masalasi emas, muloqot masalasi: u o'quvchining ko'zini boshqaradi. Bu bobda vertikal o'q bo'yicha qoidalar - fayl uzunligi, bo'sh qatorlar, e'lon va ishlatish orasidagi masofa, a'zolar tartibi. Bu qoidalarning katta qismi formatter bilan avtomatlashtirilmaydi, shuning uchun ularni bilish kerak ([13-bob](13-formatlashni-avtomatlashtirish-va-diff.md) avtomatlashtirilgan qismi haqida).

## 11.1 Fayl o'lchami va sinf uzunligi

Katta kod bazalaridagi kuzatish: toza loyihalarda fayllarning katta qismi 200 qatordan kichik va eng kattasi 500 qatordan oshmaydi. Bu qoida emas, natija: sinf bitta javobgarlikni olsa, u o'z-o'zidan kichik bo'lib qoladi.

Shu sababli fayl uzunligini **belgi** sifatida ishlatish kerak, maqsad sifatida emas. 800 qatorli sinf uzunligi uchun jazolanmaydi; u ichida bir necha javobgarlik borligi uchun bo'linadi.

```bash
# Eng katta fayllar ro'yxati: bo'lish nomzodlari
find src/main/java -name '*.java' | xargs wc -l | sort -rn | head -20

# Fayl uzunligi taqsimoti: kod bazasi holatini bir qarashda ko'rsatadi
find src/main/java -name '*.java' | xargs wc -l | awk '{print $1}' \
  | awk '{ if ($1<100) a++; else if ($1<300) b++; else if ($1<500) c++; else d++ }
         END { printf "<100: %d\n100-300: %d\n300-500: %d\n500+: %d\n", a,b,c,d }'
```

## 11.2 Gazeta metaforasi: yuqoridan pastga ma'lumot zichligi

Yaxshi manba fayli gazeta maqolasiga o'xshaydi: yuqorida eng umumiy ma'lumot, pastga tushgan sari tafsilot ortadi. Fayl nomi sarlavha, yuqoridagi e'lonlar va public metodlar - kirish qismi, pastdagi private metodlar - tafsilot.

Shundan amaliy tartib chiqadi va u Java konvensiyasi bilan mos: paket, importlar, sinf Javadoc i, statik konstantalar, maydonlar, konstruktor, public metodlar, private metodlar (11.6).

## 11.3 Tushunchalar orasida bo'sh qator

Bo'sh qator o'quvchi uchun eng arzon va eng kuchli signal: "bu yerda yangi fikr boshlanadi". Paket e'lonidan keyin, importlardan keyin, har bir metod orasida bo'sh qator bo'lishi kerak.

```java
// yomon: hamma narsa bir blokda, ko'z to'xtaydigan joy yo'q
package uz.shop.payment;
import java.time.Instant;
public final class SettlementService {
    private final PaymentGateway gateway;
    SettlementService(PaymentGateway gateway) { this.gateway = gateway; }
    public SettlementResult settle(PaymentId id) { ... }
}

// yaxshi: har bir tushuncha ajratilgan
package uz.shop.payment;

import java.time.Instant;

public final class SettlementService {

    private final PaymentGateway gateway;

    SettlementService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public SettlementResult settle(PaymentId id) { ... }
}
```

## 11.4 Vertikal zichlik: birga o'qiladigan qatorlarni ajratmaslik

Bo'sh qator ajratadi, zichlik esa bog'laydi. Bir-biriga zich bog'langan qatorlar orasiga bo'sh qator yoki izoh qo'yish bog'lanishni buzadi va o'quvchi ko'zini keraksiz sakrashga majbur qiladi.

```java
// yomon: har bir maydon izoh bilan ajratilgan, bog'liqlik ko'rinmaydi
public class ReporterConfig {
    /** Reporter listener sinfining nomi */
    private String className;

    /** Reporter listener xususiyatlari */
    private List<Property> properties = new ArrayList<>();
}

// yaxshi: uchta qator bir butun sifatida o'qiladi
public class ReporterConfig {
    private String className;
    private List<Property> properties = new ArrayList<>();
}
```

## 11.5 Vertikal masofa: e'lon va ishlatish orasidagi oraliq

Mahalliy o'zgaruvchi birinchi ishlatilishiga iloji boricha yaqin e'lon qilinishi kerak. Metod kichik bo'lsa, bu tabiiy; metod uzun bo'lsa, 40 qator yuqorida e'lon qilingan o'zgaruvchi o'quvchidan skroll qilishni talab qiladi.

Teskari qoida instans maydonlariga tegishli: ular sinf boshida, bir joyda to'planadi. Maydonni sinf o'rtasida e'lon qilish (C++ dagi ba'zi uslublar) Java da qabul qilinmaydi va o'quvchi maydonni topolmaydi.

```java
// yomon: e'lon va ishlatish orasida 30 qator
public void importFile(Path file) {
    int rejected = 0;
    ... 30 qator boshqa ish ...
    rejected++;
}

// yaxshi: e'lon ishlatish yonida; yoki butunlay yo'q (hisob alohida metodda)
public void importFile(Path file) {
    List<SettlementRow> rows = parse(file);
    long rejected = rows.stream().filter(not(this::isValid)).count();
    log.info("import tugadi: {} rad etildi", rejected);
}
```

E'lonning shakli ham qoida: bir e'londa bitta o'zgaruvchi, har biri o'z qatorida. Shunda har bir o'zgaruvchi yoniga izoh sig'adi va diff da bitta o'zgaruvchining o'zgarishi bitta qatorga tushadi. Massivda bu qoida yana bir xatoni oldini oladi: `int[] a, b, c;` e'lonida kvadrat qavs faqat birinchi nomga tegadi deb o'ylash oson, holbuki turga yozilgan qavs uchalasiga ham tegadi. Shuning uchun massiv o'zgaruvchilari bitta e'londa birga e'lon qilinmaydi.

```java
// yomon: bitta e'londa uchta nom, qavs qaysi biriga tegadi - o'quvchi o'ylab chiqaradi
int[] rowCounts, columnCounts, totals;
int page = 0, limit = 50;

// yaxshi: har e'lon o'z qatorida, izoh yoniga sig'adi
int[] rowCounts;         // har bir sahifadagi qator soni
int[] columnCounts;
int page = 0;
int limit = 50;
```

## 11.6 Maydonlar joylashuvi va a'zolar tartibi

Sinf a'zolarining tartibi konvensiya bilan belgilanadi va u butun kod bazasida bir xil bo'lishi kerak, chunki o'quvchi odatlanadi.

| Tartib | Element |
|---|---|
| 1 | `static final` konstantalar |
| 2 | `static` maydonlar (kamdan-kam, 16.9) |
| 3 | instans maydonlari (`private final` birinchi) |
| 4 | konstruktorlar (eng umumiysi oxirida) |
| 5 | statik fabrika metodlari |
| 6 | public metodlar (chaqiruv tartibida, 4.4) |
| 7 | `package-private` metodlar |
| 8 | private metodlar (chaqiruvchidan keyin) |
| 9 | `equals`, `hashCode`, `toString` |
| 10 | ichki (nested) turlar |

Checkstyle `DeclarationOrder` va `OverloadMethodsDeclarationOrder` qoidalari shu tartibni mashinaga topshiradi.

**Bir xil elementlar ro'yxati hamma joyda bir xil tartibda.** Yuqoridagi jadval sinf a'zolarining tartibini belgiladi; qoida kengroq ishlaydi: maydon, parametr, tayinlash, konstruktor argumenti, JSON kalitlari kabi istalgan bir turdagi ro'yxat **ma'noli tartibda** yoziladi va shu tartib kod bazasining hamma joyida takrorlanadi. Tartib tanlovining uch asosli variantini Boswell va Foucher sanaydi: formadagi maydonlar tartibiga moslash (o'quvchi ikki joyni yonma-yon solishtira oladi), muhimlikdan kamayib borish, yoki alifbo tartibi.

Tartibning o'zi emas, **izchilligi** qiymat beradi. Bir joyda `details, location, phone, email, url` yozilib, boshqa joyda `details, phone, email, url, location` yozilsa, o'quvchi "location qayerga ketdi" degan savol bilan to'xtaydi va unutilgan maydonni tekshirish uchun qo'shimcha kuch sarflaydi. Yonma-yon tekislangan ro'yxatda esa teskari foyda bor: tartib buzilishi va yozuv xatosi darhol ko'zga tashlanadi.

```java
// Yomon: bir joyda bir tartib, boshqa joyda boshqa
public record ContactForm(String details, String location, String phone,
                          String email, String url) {}

Contact toContact(ContactForm form) {
    return new Contact(form.details(), form.phone(), form.email(),
                       form.url(), form.location());   // location oxirga ketdi
}

// Yaxshi: bitta tartib, hamma joyda
Contact toContact(ContactForm form) {
    return new Contact(form.details(), form.location(), form.phone(),
                       form.email(), form.url());
}
```

## 11.7 Bog'liq funksiyalarni yonma-yon qo'yish

Agar bir funksiya ikkinchisini chaqirsa, ular vertikal jihatdan yaqin bo'lishi kerak va chaqiruvchi yuqorida turishi kerak. Shunda o'qish bir yo'nalishda boradi va "bu metod qayerda?" savoli tug'ilmaydi.

Overload qilingan metodlar ham yonma-yon turishi kerak, orasiga boshqa metod tushmasligi kerak - aks holda o'quvchi barcha variantlarni bir vaqtda ko'rolmaydi.

## 11.8 Tushunchaviy yaqinlik

Ba'zi kod bo'laklari bir-birini chaqirmasa ham, bir tushunchaga tegishli bo'ladi: bir xil nom shakli, bir xil vazifa, bir xil domen qoidasi. Ularni yonma-yon qo'yish o'quvchi uchun guruhni ko'rinadigan qiladi.

```java
// Bir tushuncha: assertion yordamchilari. Bir-birini chaqirmaydi, lekin birga turadi.
static void assertTrue(boolean condition) { ... }
static void assertTrue(String message, boolean condition) { ... }
static void assertFalse(boolean condition) { ... }
static void assertFalse(String message, boolean condition) { ... }
```

## 11.9 Vertikal tartib: chaqiruvchi yuqorida

Java va C# da konvensiya bir xil: chaqiruvchi funksiya chaqiriladigan funksiyadan yuqorida turadi. Bu "pastga tushish qoidasi" ning (4.4) vertikal ifodasi va o'qishni tabiiy yo'nalishda ushlab turadi.

Istisno: `equals`, `hashCode`, `toString` va boshqa shartnoma metodlari sinf oxirida to'planadi (11.6), chunki ular hikoyaning qismi emas, shartnomaning qismi.

## 11.10 Lokal o'zgaruvchi qamrovini kichik ushlash va faylda bitta top-level sinf

Oldingi bo'limlar e'lon va ishlatish orasidagi masofani o'lchadi. Buning teskari tomoni ham qoida: o'zgaruvchi birinchi ishlatiladigan joyda e'lon qilinadi, metod boshida emas. Metod boshida e'lon qilingan o'zgaruvchi metod oxirigacha yashaydi, qiymati esa orada o'zgarishi mumkin va o'quvchi uni butun metod bo'ylab kuzatishi kerak.

```java
// yomon: uchta o'zgaruvchi metod boshida, qiymati keyin to'ladi
void settle(List<Payment> payments) {
    Money total;
    Instant settledAt;
    SettlementResult result;
    // ... yigirma qator ...
}

// yaxshi: har biri birinchi ishlatilishida, deyarli hammasi final
void settle(List<Payment> payments) {
    Money total = payments.stream().map(Payment::amount).reduce(Money.ZERO, Money::plus);
    Instant settledAt = clock.instant();
    SettlementResult result = ledger.record(total, settledAt);
}
```

Shu qoidaning amaliy foydasi: o'zgaruvchi e'lon joyida ishga tushirilsa, uni `final` qilib qo'yish mumkin bo'ladi va kompilyator keyingi o'zgartirishni to'sadi. Sikl o'zgaruvchisi ham shunga kiradi: `for` va `for-each` da e'lon qilingan o'zgaruvchi sikldan tashqarida ko'rinmaydi, `while` dan oldin e'lon qilingani esa ko'rinadi va keyin tasodifan ishlatiladi.

Qamrovni kichik ushlashning ikkinchi yarmi: **bitta o'zgaruvchi bitta maqsad uchun**. Bir o'zgaruvchini metod ichida ikki xil ish uchun qayta ishlatish uni ikki marta yashatadi, lekin o'quvchiga ikki ishning orasida bog'liqlik bor degan yolg'on ishora beradi. Ikkinchi shakli yashirinroq: o'zgaruvchining ayrim qiymatlari **boshqa ma'no** tashiydi. `pageCount` chop etilgan betlar soni, `-1` bo'lsa esa xato belgisi; `customerId` mijoz raqami, `500000` dan katta bo'lsa esa qarzdor hisobning raqami. Bunday o'zgaruvchi ikki ishga cho'zilgan va shu ikkitadan kamida biri uchun turi noto'g'ri: `pageCount` ning `-1` i butun son qiyofasida yurgan `boolean`. Bu holatning atamasi **hybrid coupling** (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 10.8 (255-257-bet)). Java da yechim arzon: ikkinchi ma'no o'z o'zgaruvchisiga, `Optional` ga, enum ga yoki istisnoga chiqadi.

```java
// yomon: temp ikki ishda, pageCount ning -1 i esa qiymat emas, xato belgisi
double temp = Math.sqrt(b * b - 4 * a * c);
double[] root = { (-b + temp) / (2 * a), (-b - temp) / (2 * a) };
temp = root[0];                     // butunlay boshqa ish: ildizlarni almashtirish
root[0] = root[1];
root[1] = temp;
int pageCount = render(doc);        // -1 qaytishi mumkin, u "xato" degani

// yaxshi: har ma'no o'z nomida, xato esa qiymat emas
double discriminant = Math.sqrt(b * b - 4 * a * c);
double[] roots = { (-b + discriminant) / (2 * a), (-b - discriminant) / (2 * a) };
double firstRoot = roots[0];
roots[0] = roots[1];
roots[1] = firstRoot;
int pageCount = render(doc);        // xatoda istisno tashlaydi, -1 qaytarmaydi
```

Qamrovning nom tomoni ham bor: lokal o'zgaruvchiga yoki metod parametriga maydon nomini bermaslik. Java bunga ruxsat beradi va lokal nom maydonni **yashiradi**, shuning uchun metod ichidagi nom maydonga emas, lokal o'zgaruvchiga tegadi. Xato jim chiqadi: kompilyatsiya o'tadi, metod ishlaydi, faqat maydon hech qachon o'zgarmaydi. Yagona an'anaviy istisno - konstruktor va setter dagi `this.amount = amount` shakli, u yerda yashirish ataylab qilingan va o'quvchiga tanish; qolgan joyda nomlar farq qiladi.

```java
// yomon: lokal o'zgaruvchi maydonni yashiradi, maydon eski qiymatda qoladi
class Cart {
    private Money total = Money.ZERO;

    void add(Item item) {
        Money total = this.total.plus(item.price());   // lokal nom, maydon o'zgarmadi
    }
}

// yaxshi: nomlar to'qnashmaydi
class Cart {
    private Money total = Money.ZERO;

    void add(Item item) {
        this.total = total.plus(item.price());
    }
}
```

Qamrov qoidasining xotira tomonidagi natijasi ham shu yerda turadi: havolani `null` qilib qo'yish qoida emas, istisno bo'lishi kerak. O'zgaruvchi eng tor qamrovda e'lon qilinsa, u qamrovdan chiqishi bilan havola ham yo'qoladi va `null` tayinlashga hojat qolmaydi. Qo'lda `null` qilish faqat o'z xotirasini o'zi boshqaradigan tuzilmalarda asosli bo'ladi, masalan massiv ustida qurilgan stekda element olingandan keyin bo'shagan katakda; qolgan joylarda u kodni shovqinli qiladi va o'quvchiga mavjud bo'lmagan muammo borligini ishora qiladi.

Fayl darajasidagi qoida ham shu mantiqdan chiqadi: bitta `.java` faylda bitta top-level sinf turadi. Java bir faylda bir nechta package-private sinfga ruxsat beradi, lekin unda sinfni qaysi fayldan topish kerakligi noaniq bo'ladi va bir xil nomdagi sinf ikki faylda paydo bo'lsa kompilyatsiya natijasi fayl tartibiga bog'liq bo'lib qoladi. Yordamchi tur kerak bo'lsa, u ichki statik sinf bo'ladi (shunda uning egasi nomdan ko'rinadi) yoki o'z fayliga chiqadi.

## 11.11 Formatlashning asosiy teoremasi va yaxshi joylashuv maqsadlari

Bu bobdagi qoidalarning hammasi bitta da'vodan chiqadi va uning nomi bor: **Formatlashning asosiy teoremasi** (Fundamental Theorem of Formatting) - yaxshi joylashuv programmaning **mantiqiy tuzilishini** ko'rsatadi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 31.1 (732-bet)). Kodning chiroyli ko'rinishi ham qadrga ega, lekin tuzilishni ko'rsatishdan arzonroq: bir usul tuzilishni yaxshiroq ko'rsatsa, boshqasi chiroyliroq ko'rinsa, tuzilishni ko'rsatadigani tanlanadi. McConnell shu o'lchovni yana bir tomondan beradi: hamma kodni chiroyli ko'rsatadigan usuldan, yaxshi kodni yaxshi va yomon kodni yomon ko'rsatadigan usul foydaliroq.

Teoremaning amaliy ma'nosi: joylashuv kompilyatorga va odamga **bir xil** gapni aytishi kerak. Ikkisi ajralgan joy xato tug'adi.

```java
// yomon: indentatsiya uch qator bir blok deb aytadi, kompilyator esa
// faqat birinchi qatorni takrorlaydi
int left = 0;
int i;
for (i = 0; i < size; i++)
    left = leftValues[i];
    leftValues[i] = rightValues[i];
    rightValues[i] = left;

// yomon: bo'shliq (3+4) * (2+7) = 63 deb aytadi, kompilyator 3 + 8 + 7 = 18 hisoblaydi
int x = 3+4 * 2+7;

// yaxshi: qavs va qavs juftligi ikki o'quvchiga bitta gapni aytadi
for (int i = 0; i < size; i++) {
    int left = leftValues[i];
    leftValues[i] = rightValues[i];
    rightValues[i] = left;
}
int x = (3 + 4) * (2 + 7);
```

Teorema uslub bahsini hal qilmaydi, lekin uni oshkor qiladi: McConnell joylashuv sxemasiga qo'yiladigan talablarni sanab beradi va shu talablar bahsni "menga shunisi yoqadi" dan chiqaradi (31.1 (735-736-bet)):

- **Mantiqiy tuzilishni aniq ko'rsatsin.** Bu teoremaning o'zi. Amalda buni indentatsiya va bo'sh qator qiladi ([tushunchalar orasida bo'sh qator](#113-tushunchalar-orasida-bosh-qator), [indentatsiya va uni buzmaslik](12-gorizontal-formatlash-va-kod-uslubi.md#124-indentatsiya-va-uni-buzmaslik)).
- **Tuzilishni izchil ko'rsatsin.** Istisnolari shunchalik ko'p bo'lgan sxema izchil qo'llanmaydi; yaxshi sxema holatlarning katta qismiga tegishli bo'ladi.
- **O'qilishni yaxshilasin.** Mantiqan to'g'ri, lekin o'qishni qiyinlashtiradigan sxema foydasiz: faqat kompilyator talab qilgan joyda bo'shliq qo'yadigan uslub mantiqan nuqsonsiz va o'qilmaydi.
- **O'zgarishga bardosh bersin.** Eng yaxshi sxemada bitta qatorni o'zgartirish boshqa bir necha qatorni o'zgartirishni talab qilmaydi.

McConnell beshinchi mezonni ham eslatadi, lekin uni ixtiyoriy deb beradi: oddiy gap yoki blok uchun sarflanadigan qator sonini kamaytirish. Mezonlarni boshqa-boshqa vaznlash boshqa-boshqa xulosaga olib boradi, shuning uchun bahs mezon ustida boriladi, did ustida emas.

Shu ro'yxat korpusdagi bir qancha qoidaning sababini bir joyda tushuntiradi. [Gorizontal tekislash nega zarar qiladi](12-gorizontal-formatlash-va-kod-uslubi.md#123-gorizontal-tekislash-nega-zarar-qiladi) bo'limidagi uch zarar aslida shu mezonlarning uchtasi buzilgani: tekislangan ustun o'zgarishga bardosh bermaydi (bitta nom o'zgarsa blok o'zgaradi), o'qishni yaxshilamaydi (ko'z turga emas, nomga tushadi) va formatter bilan izchil emas. [Bitta jamoa, bitta uslub](13-formatlashni-avtomatlashtirish-va-diff.md#131-bitta-jamoa-bitta-uslub-tanlov-emas-sozlama) qarori esa ikkinchi mezonni mashinaga topshirish: izchillikni odam emas, formatter ta'minlaydi.

## 11.12 Amalda qo'llash

- [ ] 11.1 dagi skript bilan fayl uzunligi taqsimotini chiqarib, 500 qatordan katta fayllarni bo'lish ro'yxatiga kiriting.
- [ ] Sinf a'zolari tartibini 11.6 jadvaliga keltirib, Checkstyle `DeclarationOrder` bilan mahkamlang.
- [ ] Mahalliy o'zgaruvchi e'lonlarini birinchi ishlatilishiga yaqin ko'chirib, metod boshidagi "e'lon bloki" ni yo'qoting.
- [ ] Overload qilingan metodlar yonma-yon turishini tekshirib, orasiga tushgan metodlarni ko'chiring.
- [ ] Bir-birini chaqiradigan metodlarni chaqiruvchi yuqorida bo'lgan tartibga keltiring.
- [ ] Maydonlar orasidagi keraksiz Javadoc bloklarini olib tashlab, vertikal zichlikni tiklang.
- [ ] Paket, import va sinf e'lonlari orasida bo'sh qator borligini formatter bilan ta'minlang.
- [ ] `equals`/`hashCode`/`toString` ni sinf oxiriga ko'chiring va shu konvensiyani hujjatlashtiring.
- [ ] Metod boshida e'lon qilinib keyin to'ladigan o'zgaruvchilarni birinchi ishlatilish joyiga ko'chirib, `final` qo'yib ko'ring.
- [ ] Bir faylda bir nechta top-level sinf bor fayllarni toping va ularni ajratish yoki ichki statik sinfga aylantirish qarorini qabul qiling.
- [ ] Ikki ishda ishlatilgan `temp` turidagi o'zgaruvchilarni va `-1` kabi yashirin ma'noli qiymatlarni topib, har ma'noni o'z nomiga chiqaring.
- [ ] Uslub bahsini mezon ustiga ko'chiring: taklif qilingan sxema mantiqiy tuzilishni, izchillikni, o'qilishni va o'zgarishga bardoshni qanday o'zgartirishini yozib qo'ying.

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 4-bob (39-40-betlar) - bir xil elementlar ro'yxatini ma'noli tartibda yozish (forma maydonlari tartibi, muhimlik, alifbo) va shu tartibni hamma joyda saqlash; tekislangan ro'yxatda tartib buzilishi va yozuv xatosining ko'zga tashlanishi
- Joshua Bloch, *Effective Java* 3rd, Item 57 - lokal o'zgaruvchi qamrovini kichik ushlash
- Joshua Bloch, *Effective Java* 3rd, Item 25 - manba faylda bitta top-level sinf
- Robert C. Martin, *Clean Code*, 5-bob - vertikal masofa, gazeta metaforasi, tushunchaviy yaqinlik
- Robert C. Martin, *Clean Code*, 5-bob ("Vertical Formatting") - gazeta metaforasi, tushunchalar orasidagi bo'shliq, vertikal zichlik va masofa
- Robert C. Martin, *Clean Code*, 5-bob ("Vertical Ordering") - chaqiruvchi chaqiriladigandan yuqorida
- Joshua Bloch, *Effective Java* 3rd, Item 57 - lokal o'zgaruvchini birinchi ishlatilish joyida e'lon qilish
- Joshua Bloch, *Effective Java* 3rd, Item 25 - manba faylda bitta top-level sinf
- Steve McConnell, *Code Complete*, 2-nashr, 10.8 (255-257-bet) - bitta o'zgaruvchi bitta maqsad uchun, yashirin ma'no va hybrid coupling
- Steve McConnell, *Code Complete*, 2-nashr, 31.1 (732-bet) - Formatlashning asosiy teoremasi
- Steve McConnell, *Code Complete*, 2-nashr, 31.1 (735-736-bet) - yaxshi joylashuvning mezonlari
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Early Objects, Pearson, 2-bob (47-bet) - har o'zgaruvchini alohida e'londa va alohida qatorda e'lon qilish, shunda yoniga izoh sig'ishi
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Early Objects, Pearson, 7-bob (247-bet) - bitta e'londa bir necha massiv o'zgaruvchisini e'lon qilmaslik (ikkinchi, massivga xos shakli)
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 10-bob (372-bet) - lokal o'zgaruvchiga instans yoki statik maydon nomini bermaslik (metod parametridan tashqari)
- Paul Deitel va Harvey Deitel, *Java How to Program*, 9-nashr, Pearson, 6-bob (220-bet) va 8-bob (319-bet) - maydon va lokal o'zgaruvchiga har xil nom berish, nomlar bir xil bo'lsa metod chaqirilganda chiqadigan nozik mantiq xatosi (uchinchi mustaqil manba)
- Joshua Bloch, *Effective Java* 3rd, Item 7 (27-bet) - havolani `null` qilish qoida emas istisno bo'lishi, eng to'g'ri yo'lning o'zgaruvchini eng tor qamrovda e'lon qilib qamrovdan chiqarish ekani
- ESLATMA: `Cart` va `rowCounts` kod misollari korpus qo'shimchasi; kitoblar qoidani boshqa misollarda beradi

---

[&larr; 10. Javadoc va API hujjati](10-javadoc-va-api-hujjati.md) · [Mundarija](README.md) · [12. Gorizontal formatlash va kod uslubi &rarr;](12-gorizontal-formatlash-va-kod-uslubi.md)
