<!-- doc: clean-code | chapter: 11 | part: IV. Formatlash va kod uslubi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 11. Vertikal formatlash (Vertical Formatting)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [11.1 Fayl o'lchami va sinf uzunligi](#111-fayl-olchami-va-sinf-uzunligi)
- [11.2 Gazeta metaforasi: yuqoridan pastga ma'lumot zichligi](#112-gazeta-metaforasi-yuqoridan-pastga-malumot-zichligi)
- [11.3 Tushunchalar orasida bo'sh qator](#113-tushunchalar-orasida-bosh-qator)
- [11.4 Vertikal zichlik: birga o'qiladigan qatorlarni ajratmaslik](#114-vertikal-zichlik-birga-oqiladigan-qatorlarni-ajratmaslik)
- [11.5 Vertikal masofa: e'lon va ishlatish orasidagi oraliq](#115-vertikal-masofa-elon-va-ishlatish-orasidagi-oraliq)
- [11.6 Maydonlar joylashuvi va a'zolar tartibi](#116-maydonlar-joylashuvi-va-azolar-tartibi)
- [11.7 Bog'liq funksiyalarni yonma-yon qo'yish](#117-bogliq-funksiyalarni-yonma-yon-qoyish)
- [11.8 Tushunchaviy yaqinlik](#118-tushunchaviy-yaqinlik)
- [11.9 Vertikal tartib: chaqiruvchi yuqorida](#119-vertikal-tartib-chaqiruvchi-yuqorida)
- [11.10 Amalda qo'llash](#1110-amalda-qollash)

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

## 11.10 Amalda qo'llash

- [ ] 11.1 dagi skript bilan fayl uzunligi taqsimotini chiqarib, 500 qatordan katta fayllarni bo'lish ro'yxatiga kiriting.
- [ ] Sinf a'zolari tartibini 11.6 jadvaliga keltirib, Checkstyle `DeclarationOrder` bilan mahkamlang.
- [ ] Mahalliy o'zgaruvchi e'lonlarini birinchi ishlatilishiga yaqin ko'chirib, metod boshidagi "e'lon bloki" ni yo'qoting.
- [ ] Overload qilingan metodlar yonma-yon turishini tekshirib, orasiga tushgan metodlarni ko'chiring.
- [ ] Bir-birini chaqiradigan metodlarni chaqiruvchi yuqorida bo'lgan tartibga keltiring.
- [ ] Maydonlar orasidagi keraksiz Javadoc bloklarini olib tashlab, vertikal zichlikni tiklang.
- [ ] Paket, import va sinf e'lonlari orasida bo'sh qator borligini formatter bilan ta'minlang.
- [ ] `equals`/`hashCode`/`toString` ni sinf oxiriga ko'chiring va shu konvensiyani hujjatlashtiring.

---

[&larr; 10. Javadoc va API hujjati](10-javadoc-va-api-hujjati.md) · [Mundarija](README.md) · [12. Gorizontal formatlash va kod uslubi &rarr;](12-gorizontal-formatlash-va-kod-uslubi.md)
