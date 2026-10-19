<!-- doc: clean-code | chapter: 12 | part: IV. Formatlash va kod uslubi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 12. Gorizontal formatlash va kod uslubi (Horizontal Formatting and Style)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [12.1 Qator uzunligi chegarasi va uni tanlash](#121-qator-uzunligi-chegarasi-va-uni-tanlash)
- [12.2 Gorizontal bo'shliq: operator, qavs, vergul](#122-gorizontal-boshliq-operator-qavs-vergul)
- [12.3 Gorizontal tekislash nega zarar qiladi](#123-gorizontal-tekislash-nega-zarar-qiladi)
- [12.4 Indentatsiya va uni buzmaslik](#124-indentatsiya-va-uni-buzmaslik)
- [12.5 Bo'sh blok va "dummy scope"](#125-bosh-blok-va-dummy-scope)
- [12.6 Qavs uslubi va bir qatorli `if`](#126-qavs-uslubi-va-bir-qatorli-if)
- [12.7 Import tartibi va yulduzcha import](#127-import-tartibi-va-yulduzcha-import)
- [12.8 Zanjirli chaqiruv va oqimni bo'lish](#128-zanjirli-chaqiruv-va-oqimni-bolish)
- [12.9 Uzun satr, matn bloki va SQL joylashtirish](#129-uzun-satr-matn-bloki-va-sql-joylashtirish)
- [12.10 Fayl kodirovkasi, qator oxiri va oxirgi bo'sh qator](#1210-fayl-kodirovkasi-qator-oxiri-va-oxirgi-bosh-qator)
- [12.11 Amalda qo'llash](#1211-amalda-qollash)

</details>


Gorizontal o'q bo'yicha qoidalar kamroq, lekin ulardan biri - qator uzunligi - eng ko'p bahs qo'zg'atadigan qoida. Bu bobda qator uzunligi, bo'shliq, tekislash, indentatsiya, import tartibi va zanjirli chaqiruvni bo'lish ko'rib chiqiladi.

## 12.1 Qator uzunligi chegarasi va uni tanlash

Qator uzunligi chegarasining maqsadi - gorizontal skrollni yo'qotish va yonma-yon diff ni o'qiladigan qilish. Zamonaviy ekranlarda 80 juda qisqa, 200 esa diff ni buzadi. Amalda uchta tanlov ishlatiladi: 100 (eng keng tarqalgan), 120 (Spring ekotizimida ko'p), 80 (klassik).

Muhimi - son emas, chegara borligi va uni formatter majburlashi. Chegara bo'lmasa, uzun ifodalar paydo bo'ladi va ularni o'qish uchun gorizontal skroll kerak bo'ladi, bu esa code review ni ikki marta qiyinlashtiradi.

| Chegara | Afzalligi | Kamchiligi |
|---|---|---|
| 80 | ikki fayl yonma-yon, terminalga sig'adi | Java da ko'p bo'linish |
| 100 | muvozanat, diff o'qiladi | - |
| 120 | kam bo'linish | yonma-yon diff siqiladi |
| chegarasiz | bo'linish yo'q | review buziladi |

## 12.2 Gorizontal bo'shliq: operator, qavs, vergul

Bo'shliq bog'liqlikni ko'rsatadi: zich turgan narsalar bir butun, ajratilgan narsalar alohida. Konvensiya: binar operator atrofida bo'shliq, vergul keyin bo'shliq, qavs ichida bo'shliq yo'q, metod nomi va qavs orasida bo'shliq yo'q.

Prioriteti yuqori operatorlarni zich yozish o'qilishga yordam beradi, lekin google-java-format bunga ruxsat bermaydi va bu to'g'ri qaror: izchillik did dan muhimroq. Bo'shliq bilan ustunlikni ko'rsatish baribir yetarli emas: ustunlik qavs bilan yoziladi, bo'shliq bilan emas ([murakkab mantiqni soddalashtirish](06-shart-mantiq-va-boshqaruv-oqimi.md#63-murakkab-mantiqni-soddalashtirish)).

```java
// yaxshi: standart konvensiya
int lineSize = line.length();
total = total.add(price.multiply(quantity));
settle(payment, gateway, timeout);

// yomon: izchil emas
int lineSize=line.length();
settle( payment,gateway , timeout );
```

## 12.3 Gorizontal tekislash nega zarar qiladi

E'lonlarni yoki tayinlashlarni ustun bo'yicha tekislash (vertikal tekislash) chiroyli ko'rinadi, lekin uch zarari bor: diff shovqini (bitta nom o'zgarsa butun blok o'zgaradi), o'qish adashishi (ko'z tur emas, nomga qaraydi), va formatter bilan kurash.

```java
// yomon: tekislangan - bitta uzun nom qo'shilsa butun blok o'zgaradi
private   Socket          socket;
private   InputStream     input;
private   OutputStream    output;
private   Request         request;

// yaxshi: oddiy, diff toza
private Socket socket;
private InputStream input;
private OutputStream output;
private Request request;
```

Boswell va Foucher ustun bo'yicha tekislashni "foydali bo'lganda ishlat" deb
beradi va u yuqoridagi qoidaga zid ko'rinadi. Zid emas: ikki manba boshqa
narsani tekislaydi. Kitob foyda ko'rgan misollari - bir xil shakldagi
**qatorlar jadvali**: bir xil yordamchi metodning to'rt chaqiruvi bir xil
tartibdagi argumentlar bilan, yoki `wget` kodidagi yuzdan ortiq buyruq yozuvi
(`nom`, `maydon`, `ishlovchi` ustunlari). Bunda ustun "ko'z uchun suyanch"
beradi: bitta ustunni yuqoridan pastga kuzatish mumkin bo'ladi va qatorlar
bir xil tekislanganda `equest` kabi imlo xatosi yoki tushib qolgan qiymat
ko'zga tashlanadi. Kitobning o'z tavsiyasi ham ehtiyotkor: sinab ko'r, qimmatga
tushsa to'xta - va narxi sifatida aynan qo'lda ushlab turish mehnati va
kattalashgan diff keltiriladi (Boswell/Foucher, *The Art of Readable Code*,
1-nashr, O'Reilly, 2011, 4-bob (38-39-bet)).

Ajratuvchi shart shundan chiqadi: **nima tekislanmoqda**.

| Tekislanayotgan narsa | Qaror | Sabab |
|---|---|---|
| Mustaqil e'lon va tayinlashlar | tekislanmaydi | ustun hech narsa solishtirmaydi, diff shovqini qoladi |
| Bir xil shakldagi qatorlar jadvali (parametrlangan test, kalit-ishlovchi jadvali) | tekislash haqli | ustunni yuqoridan pastga solishtirish mumkin, farq va imlo xatosi ko'rinadi |
| Formatter saqlab qolmaydigan har qanday tekislash | tekislanmaydi | qo'lda ushlab turiladi va har formatlashda qaytib keladi |

Uchinchi qatorni Java amaliyoti hal qiladi: kod formatlash avtomatlashtirilgan
bo'lsa, tekislash haqida bahs ham tugaydi, chunki
[bitta jamoa, bitta uslub](13-formatlashni-avtomatlashtirish-va-diff.md#131-bitta-jamoa-bitta-uslub-tanlov-emas-sozlama)
qoidasi bo'yicha fayl shaklini odam emas, asbob belgilaydi. Jadval shaklidagi
ma'lumot esa Java da ko'pincha koddan butunlay chiqariladi: parametrlangan
testda `@CsvSource` matniga, konfiguratsiyada esa resurs fayliga. Shunda
jadval ham o'qiladi, tekislash ham formatter bilan urishmaydi.

```java
// yaxshi: jadval shaklidagi ma'lumot tekislangan, lekin u kod emas - CSV matni
@ParameterizedTest
@CsvSource({
        "TASHKENT,   100.00, 12.00",
        "FREE_ZONE,  100.00,  0.00",
        "SAMARKAND,  100.00, 12.00"
})
void calculatesTax(Region region, String net, String expectedTax) { ... }
```

## 12.4 Indentatsiya va uni buzmaslik

Indentatsiya kodning ierarxiyasini ko'rsatadigan asosiy vosita. Java konvensiyasi: 4 bo'shliq, tab emas (tab turli muhitlarda turlicha ko'rinadi va diff ni buzadi). Ikkinchi darajali davomiy qator uchun 8 bo'shliq.

Indentatsiyani buzish - bir qatorli `if` yoki metodni indentatsiyasiz yozish - vaqt tejamaydi, lekin ierarxiyani yashiradi.

```java
// yomon: indentatsiya buzilgan, ierarxiya ko'rinmaydi
public class CommentWidget extends Widget {
    public static final String REGEXP = "^#[\r\n]";
    public CommentWidget(ParentWidget parent, String text) { super(parent, text); }
    public String render() throws Exception { return ""; }
}

// yaxshi
public class CommentWidget extends Widget {

    public static final String REGEXP = "^#[\r\n]";

    public CommentWidget(ParentWidget parent, String text) {
        super(parent, text);
    }

    public String render() throws Exception {
        return "";
    }
}
```

## 12.5 Bo'sh blok va "dummy scope"

Bo'sh blok (`while (condition);`) eng xavfli formatlash xatosi, chunki nuqta-vergul ko'rinmaydi va keyingi qator sikl tanasi deb o'qiladi. Qoida: bo'sh blok har doim qavs bilan yoziladi va ichida nega bo'shligi izohlanadi.

```java
// yomon: ; ko'rinmaydi, keyingi qator sikl tanasi emas
while (dis.read(buf, 0, readBufferSize) != -1);

// yaxshi: qavs va izoh
while (dis.read(buf, 0, readBufferSize) != -1) {
    // Oqimni oxirigacha o'qib tashlaymiz: mazmuni kerak emas, faqat
    // ulanish to'g'ri yopilishi uchun bufer bo'shatiladi.
}
```

Xuddi shu qoida bo'sh `catch` ga tegishli ([patternlar hujjatidagi](../patterns/README.md) istisnolarni yutib yuborish anti-patterni Exception Swallowing) - u hech qachon izohsiz qolmaydi.

## 12.6 Qavs uslubi va bir qatorli `if`

Java ekotizimida K&R uslubi standart: ochiluvchi qavs shu qatorda, yopiluvchi qavs alohida qatorda. Uslub tanlovi muhim emas; izchillik muhim va uni formatter ta'minlaydi.

Bir qatorli `if` (4.8 da ko'rilgan) formatlash nuqtai nazaridan ham zararli: u diff da qo'shilgan qatorni ko'rinmas qiladi va qavs qo'shishni talab qiladi.

Kvadrat qavsning joyi ham shu bo'limga kiradi, chunki Java eski shaklga ham ruxsat beradi: massiv qaytaradigan metodda qavslar parametr ro'yxatidan **keyin** yozilishi mumkin (`int f()[]`). Bu C dan kelgan sintaksis va yangi kodda ishlatilmaydi: qavs turga tegishli, shuning uchun `int[] f()` deb yoziladi. O'zgaruvchi e'lonida ham xuddi shunday - `int a[]` emas, `int[] a` (11.5).

## 12.7 Import tartibi va yulduzcha import

Importlar tartibi guruhlangan va alifbo bo'yicha saralangan bo'lishi kerak, aks holda har bir yangi import diff da tasodifiy joyga tushadi va konfliktlar ko'payadi.

Yulduzcha (`import java.util.*`) ikki zarar keltiradi: qaysi sinf qayerdan kelganini yashiradi, va ikki paketda bir xil nomli sinf bo'lsa (`java.util.Date` va `java.sql.Date`) konflikt tug'diradi. Qoida: yulduzcha import taqiqlanadi, statik import esa faqat test assertion lari va `Math` kabi aniq holatlarda ruxsat etiladi.

```java
// yaxshi: guruhlangan, aniq, saralangan
import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import uz.shop.order.OrderApi;

import static java.util.Comparator.comparing;
import static java.util.function.Predicate.not;
```

Java 25 da importning yangi shakli paydo bo'ldi va u yulduzchadan kattaroq
xavf tug'diradi: `import module M` modul `M` eksport qilgan barcha paketlarning
public top-level sinf va interfeyslarini on-demand import qiladi, qo'shimcha
ravishda `M` ni o'qish orqali joriy modul o'qiydigan modullar eksport qilgan
paketlarni ham (*The Java Language Specification, Java SE 25 Edition*, 7.5.5
(227-228-bet)). Ya'ni bitta qatorning qamrovi bir paket emas, modul grafi.

Spetsifikatsiyaning o'zi noaniqlik misollarini beradi. `import module
java.base;` va `import module java.desktop;` yonma-yon turganda `List`
nomi noaniq bo'ladi va kompilyatsiya xatosi beradi, chunki `java.util.List`
va `java.awt.List` ikkisi ham ko'rinadi. Bundan ham muhimi: **bitta** modulni
import qilish ham yetarli - `import module java.desktop;` dan keyin `Element`
nomi noaniq, chunki modul `javax.swing.text` va
`javax.swing.text.html.parser` paketlarini eksport qiladi va ikkisida ham
`Element` bor. Yechim bitta: noaniqlikni single-type-import bilan hal qilish
(`import java.util.List;`) (shu yerda, 7.5.5 (229-230-bet)).

```java
// yomon: qamrovi modul grafi, nom to'qnashuvi kompilyatsiya xatosi beradi
import module java.base;
import module java.desktop;

List<Order> orders = new ArrayList<>();   // xato: List noaniq

// yaxshi: aniq import, nom qayerdan kelgani ko'rinadi
import java.util.ArrayList;
import java.util.List;
```

ESLATMA: `import module` ni ishlab chiqarish kodida ishlatmaslik shu korpusning
tavsiyasi. Spetsifikatsiya shaklni va noaniqlik qoidalarini beradi, siyosat
bermaydi; qoida yulduzcha import bilan bir xil sababdan chiqadi - nom qayerdan
kelganini yashiradi, bu yerda esa yashirish qamrovi bir paket emas, butun modul
grafi. Qisqa skript va tajriba kodida u qulay, chunki o'sha joyda importni
qo'lda boshqarish qiymat bermaydi.

Import nomni qayerdan kelganini ko'rsatsa, chaqiruv shakli esa a'zo kimga tegishli ekanini ko'rsatadi: statik metod va statik maydonga sinf nomi va nuqta bilan murojaat qilinadi, nusxa orqali emas. `thread.sleep(100)` kompilyatsiya o'tadi, lekin o'quvchiga metod nusxaga tegishlidek ko'rinadi va `Thread.sleep(100)` ning joriy thread ni to'xtatishini yashiradi. Bu statik tahlil qoidasiga ham tushadi (42.3).

```java
// yomon: statik a'zo nusxa orqali chaqirilgan
Thread worker = new Thread(task);
worker.sleep(100);                 // aslida Thread.sleep: joriy thread uxlaydi
Integer value = 0;
value.parseInt("42");              // aslida Integer.parseInt

// yaxshi: egasi nomdan ko'rinadi
Thread.sleep(100);
Integer.parseInt("42");
```

## 12.8 Zanjirli chaqiruv va oqimni bo'lish

Oqim va builder zanjirlari uzun bo'ladi va ularni bo'lish qoidasi bor: har bir zanjir bo'g'ini alohida qatorda, nuqta qator boshida. Shunda har bir qadam ko'rinadi va diff faqat o'zgargan qadamni ko'rsatadi.

```java
// yomon: bir qatorda, qaysi qadam o'zgarganini diff ko'rsatmaydi
return orders.stream().filter(Order::isPaid).map(Order::total).reduce(Money.ZERO, Money::add);

// yaxshi: har bir qadam alohida, nuqta boshida
return orders.stream()
        .filter(Order::isPaid)
        .map(Order::total)
        .reduce(Money.ZERO, Money::add);
```

Zanjir uch bo'g'indan oshsa va har bir bo'g'in murakkab bo'lsa, oraliq natijani nomlangan o'zgaruvchiga chiqarish o'qilishni yaxshilaydi ([35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md), Extract Variable).

## 12.9 Uzun satr, matn bloki va SQL joylashtirish

Uzun satr literalini `+` bilan bo'lish o'qilmaydi va formatterni chalg'itadi. Java 15 dan beri matn bloki (`"""`) bor va SQL, JSON, XML uchun to'g'ri yechim ([arxitektor hujjatidagi](../architect/README.md) matn bloki va `var` bo'limi).

```java
// yomon: + bilan bo'lingan SQL
String sql = "select p.id, p.amount " +
             "from payment p " +
             "where p.order_id = ? and p.settled_at is not null";

// yaxshi: matn bloki, indentatsiya avtomatik olib tashlanadi
String sql = """
        select p.id, p.amount
        from payment p
        where p.order_id = ?
          and p.settled_at is not null
        """;
```

## 12.10 Fayl kodirovkasi, qator oxiri va oxirgi bo'sh qator

Bu qoidalar ko'rinmas, lekin ularning yo'qligi diff ni buzadi va cross-platform jamoada har bir commit da butun fayl o'zgargan bo'lib ko'rinadi.

```ini
# .gitattributes - repoda qator oxirini normallashtirish
*       text=auto eol=lf
*.bat   text eol=crlf
*.jar   binary
*.png   binary
```

| Sozlama | To'g'ri qiymat |
|---|---|
| Kodirovka | UTF-8 (hamma joyda, `pom.xml` da ham) |
| Qator oxiri | LF (`.gitattributes` bilan majburiy) |
| Oxirgi qator | bo'sh qator bilan tugaydi |
| Orqa bo'shliqlar | olib tashlanadi |
| Tab | bo'shliqqa aylantiriladi |
| BOM | yo'q |

### BOM Java da ko'rinmas emas: kompilyatsiyani yiqitadi

Jadvalning boshqa qatorlari diff gigiyenasi haqida, BOM esa boshqa toifada: `javac` uni oddiy belgi deb o'qiydi va fayl kompilyatsiya bo'lmaydi.

```text
A.java:1: error: illegal character: '﻿'
A.java:1: error: class, interface, enum, or record expected
A.java:3: error: class, interface, enum, or record expected
...
```

Birinchi qatordan keyin deyarli har bir qator "class, interface, enum, or record expected" beradi, shuning uchun asl sabab yuzlab xato ichida ko'rinmaydi va "nega butun fayl buzildi" degan savol tug'iladi. Faqat **fayl boshidagi** BOM muhim: satr literali ichidagi yoki o'rtadagi U+FEFF kompilyatsiyaga xalaqit bermaydi.

Qo'lda yozilganda bu kamdan-kam uchraydi, chunki IDE BOM qo'ymaydi. U fayl **skript bilan** yozilganda tushadi:

| Vosita | BOM qo'yadigan shakl | To'g'ri shakl |
|---|---|---|
| Python | `open(p, "w", encoding="utf-8-sig")` | `encoding="utf-8"` |
| PowerShell 5.1 | `Out-File`, `>`, `>>` (sukut BOM bilan) | `Set-Content -Encoding utf8NoBOM`, yoki `[IO.File]::WriteAllText` |

Tuzoq ayniqsa mavjud faylni skript bilan tahrirlaganda qo'shiladi: fayl `utf-8-sig` bilan o'qilib, keyin shu kodirovka bilan qayta yozilsa, BOM bo'lmagan faylga BOM qo'shiladi. O'qishda `utf-8-sig`, yozishda `utf-8` ishlatilsin, yoki fayl baytlar bilan o'qib yozilsin.

`.properties` faylida BOM kompilyatsiyani yiqitmaydi, lekin **birinchi kalit** nomiga qo'shilib ketadi va u kalit topilmay qoladi. Fayl oxiriga qator qo'shish esa xavfsiz.

### Fayl boshidagi sarlavha izohi: nima turadi, nima turmaydi

Fayl boshida izoh bloki bo'lishi mumkin va u ham fayl darajasidagi konvensiya. Darsliklar har bir fayl sarlavha izohida muallif nomi va sanani talab qiladi, korpus esa jurnal izohi va mualliflik imzosini [yomon izoh](09-yomon-izohlar-katalogi.md#95-jurnal-izohlari-va-mualliflik-imzolari) deb beradi. Ajratuvchi shart - ma'lumot qayerda **saqlanadi**: litsenziya va huquqiy matn faylning o'zida turishi shart, chunki fayl repodan ko'chirilganda ham u bilan birga ketadi va huquqiy kuchi shundan kelib chiqadi; mualliflik va o'zgarish tarixi esa VCS da qoladi, chunki `git log` va `git blame` ularni aniq va yangi holda beradi, qo'lda yozilgan imzo esa birinchi tahrirdan keyin eskiradi.

```java
// yaxshi: faqat litsenziya, tarix yo'q
/*
 * Copyright 2026 Shop Platform. Litsenziya: Apache-2.0.
 */
package uz.shop.payment;

// yomon: mualliflik va o'zgarish tarixi faylda
/*
 * Muallif: A. Karimov
 * Yaratilgan: 2026-03-14
 * O'zgarishlar:
 *   2026-04-02  qaytarish qo'shildi (B. Aliyev)
 */
```

## 12.11 Amalda qo'llash

- [ ] Qator uzunligi chegarasini tanlab (100 tavsiya etiladi), uni formatter va Checkstyle da bir xil qiymatga qo'ying.
- [ ] Gorizontal tekislangan e'lon bloklarini formatter bilan oddiy shaklga keltirib, diff shovqinini yo'qoting.
- [ ] Yulduzcha importlarni taqiqlab (Checkstyle `AvoidStarImport`), mavjudlarini IDE bilan yoyib yuboring.
- [ ] Import tartibini guruhlar bo'yicha belgilab, Spotless `importOrder` ga yozib qo'ying.
- [ ] `+` bilan bo'lingan SQL va JSON literallarini matn blokiga o'tkazing.
- [ ] `.gitattributes` va `.editorconfig` fayllarini qo'shib, kodirovka va qator oxirini normallashtiring.
- [ ] Bo'sh bloklarni (`;` bilan tugagan sikl, bo'sh `catch`) topib, qavs va izoh qo'shing.
- [ ] Uzun oqim zanjirlarini har bir bo'g'in alohida qatorda bo'ladigan shaklga keltiring.

## Manbalar

- [Google Java Style Guide](https://raw.githubusercontent.com/google/styleguide/aee99aa581bd852c8a40814c1c8d0f8aa79a0ba2/javaguide.html) - qator uzunligi, bo'shliq, qavs, import tartibi va yulduzcha importning taqiqlanishi
- Robert C. Martin, *Clean Code*, 5-bob - gorizontal formatlash va zichlik
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 4-bob (38-39-betlar) - ustun bo'yicha tekislashning foydali holati (bir xil shakldagi chaqiruvlar va `wget` buyruqlar jadvali), `equest` imlo xatosining ko'zga tashlanishi, va narxi sifatida qo'lda ushlab turish mehnati bilan kattalashgan diff
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 7.5.5 (227-230-betlar) - `import module M` ning qamrovi (modul eksport qilgan va transitive o'qiladigan paketlar), `java.base` bilan `java.desktop` dagi `List` noaniqligi, bitta modul ichidagi `Element` noaniqligi va single-type-import bilan hal qilish
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 8-bob (289-bet) - massiv qaytaradigan metodda kvadrat qavsni parametr ro'yxatidan keyin yozish shaklining eski sintaksis ekani
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Early Objects, Pearson, 8-bob (341-bet) - statik metodni sinf nomi va nuqta bilan chaqirish, nusxa orqali emas
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 8-bob (315-bet) - statik metod va statik maydonni sinf nomi bilan chaqirish (ikkinchi mustaqil manba)
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Early Objects, Pearson, 2-bob (37-bet) - har fayl boshida sarlavha izohi va unda muallif bilan sanani ko'rsatish talabi
- ESLATMA: fayl sarlavha izohini faqat litsenziya va huquqiy matnga cheklash, mualliflik bilan o'zgarish tarixini VCS ga qoldirish ajratuvchi sharti korpus qarori: Deitel (2-bob, 37-bet) sarlavha izohida muallif va sanani talab qiladi, korpusning yomon izohlar katalogi esa jurnal izohi va mualliflik imzosini taqiqlaydi, shart ikkisini bir-biriga qarshi qo'ymasdan ajratadi
- ESLATMA: `Thread.sleep` va litsenziya sarlavhasi kod misollari korpus qo'shimchasi

---

[&larr; 11. Vertikal formatlash](11-vertikal-formatlash.md) · [Mundarija](README.md) · [13. Formatlashni avtomatlashtirish va diff gigiyenasi &rarr;](13-formatlashni-avtomatlashtirish-va-diff.md)
