<!-- doc: clean-code | chapter: 12 | part: IV. Formatlash va kod uslubi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

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

Prioriteti yuqori operatorlarni zich yozish o'qilishga yordam beradi, lekin google-java-format bunga ruxsat bermaydi va bu to'g'ri qaror: izchillik did dan muhimroq.

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

## 12.11 Amalda qo'llash

- [ ] Qator uzunligi chegarasini tanlab (100 tavsiya etiladi), uni formatter va Checkstyle da bir xil qiymatga qo'ying.
- [ ] Gorizontal tekislangan e'lon bloklarini formatter bilan oddiy shaklga keltirib, diff shovqinini yo'qoting.
- [ ] Yulduzcha importlarni taqiqlab (Checkstyle `AvoidStarImport`), mavjudlarini IDE bilan yoyib yuboring.
- [ ] Import tartibini guruhlar bo'yicha belgilab, Spotless `importOrder` ga yozib qo'ying.
- [ ] `+` bilan bo'lingan SQL va JSON literallarini matn blokiga o'tkazing.
- [ ] `.gitattributes` va `.editorconfig` fayllarini qo'shib, kodirovka va qator oxirini normallashtiring.
- [ ] Bo'sh bloklarni (`;` bilan tugagan sikl, bo'sh `catch`) topib, qavs va izoh qo'shing.
- [ ] Uzun oqim zanjirlarini har bir bo'g'in alohida qatorda bo'ladigan shaklga keltiring.

---

[&larr; 11. Vertikal formatlash](11-vertikal-formatlash.md) · [Mundarija](README.md) · [13. Formatlashni avtomatlashtirish va diff gigiyenasi &rarr;](13-formatlashni-avtomatlashtirish-va-diff.md)
