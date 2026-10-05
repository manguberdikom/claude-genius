<!-- doc: sonarqube | chapter: 13 | part: IV. Sonar o'tadigan kod -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 13. Sonar o'tadigan kod yozish qoidalari (Writing Code That Passes)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [13.1 Metodni qisqa va bitta mas'uliyatli qilish: murakkablik chegarasidan oshmaslik](#131-metodni-qisqa-va-bitta-masuliyatli-qilish-murakkablik-chegarasidan-oshmaslik)
- [13.2 Parametrlar soni va ularni obyektga yig'ish](#132-parametrlar-soni-va-ularni-obyektga-yigish)
- [13.3 Ichma-ich shartlarni erta qaytish bilan yassilash](#133-ichma-ich-shartlarni-erta-qaytish-bilan-yassilash)
- [13.4 `null` ni qaytarmaslik va `Optional` ni to'g'ri ishlatish](#134-null-ni-qaytarmaslik-va-optional-ni-togri-ishlatish)
- [13.5 Istisnolarni to'g'ri ushlash: umumiy `Exception` ni ushlamaslik, yutib yubormaslik](#135-istisnolarni-togri-ushlash-umumiy-exception-ni-ushlamaslik-yutib-yubormaslik)
- [13.6 Resurslarni yopish: `try-with-resources` va yopilmagan oqim](#136-resurslarni-yopish-try-with-resources-va-yopilmagan-oqim)
- [13.7 O'zgaruvchan holatni cheklash: `final`, immutable obyekt](#137-ozgaruvchan-holatni-cheklash-final-immutable-obyekt)
- [13.8 Takrorlanuvchi literal va magic number ni konstantaga chiqarish](#138-takrorlanuvchi-literal-va-magic-number-ni-konstantaga-chiqarish)
- [13.9 To'g'ri taqqoslash: `equals`, `compareTo`, suzuvchi nuqta, `BigDecimal`](#139-togri-taqqoslash-equals-compareto-suzuvchi-nuqta-bigdecimal)
- [13.10 Loglash qoidalari: formatlangan xabar, istisno uzatish, maxfiy ma'lumot](#1310-loglash-qoidalari-formatlangan-xabar-istisno-uzatish-maxfiy-malumot)
- [13.11 Kodni Sonar nuqtai nazaridan o'qib chiqish odati](#1311-kodni-sonar-nuqtai-nazaridan-oqib-chiqish-odati)
- [13.12 Amalda qo'llash](#1312-amalda-qollash)

</details>



Sonar qoidalarining katta qismi kodning mantiqini emas, shaklini o'lchaydi. Shuning uchun "Sonar o'tadigan kod" degani sirli uslub emas, balki bir nechta o'lchanadigan xususiyatni qondiradigan kod: metod qisqa, shartlar yassi, resurs yopilgan, istisno yo'qolmagan, taqqoslash to'g'ri tipda qilingan. Quyida har bir mavzu uchun avval analizator nimadan shikoyat qiladi, keyin o'sha shikoyatni yo'q qiladigan variant keltirilgan. Misollar to'lov, buyurtma va ombor qoldig'i domenidan olingan, chunki real shikoyatlar aynan shunday servislarda to'planadi.

## 13.1 Metodni qisqa va bitta mas'uliyatli qilish: murakkablik chegarasidan oshmaslik

Sonar metod uchun ikki xil o'lchov yuritadi. Birinchisi cyclomatic complexity: shartli tarmoqlar soni. Ikkinchisi cognitive complexity (`java:S3776`): odam uchun o'qish qiyinligi, ya'ni har bir ichma-ich daraja qo'shimcha jarima oladi. Ikkinchisi muhimroq, chunki u ichma-ichlikni alohida jazolaydi: ikki daraja ichidagi `if` bir darajadagidan qimmatroq turadi. Metod qatorlari soni uchun ham alohida qoida bor (`java:S138`), lekin amalda cognitive complexity birinchi portlaydi.

```java
// Sonar shikoyat qiladigan variant: cognitive complexity chegaradan oshadi
public BigDecimal hisobla(Buyurtma b) {
    BigDecimal jami = BigDecimal.ZERO;
    if (b != null) {
        if (b.getQatorlar() != null) {
            for (Qator q : b.getQatorlar()) {
                if (q.getSoni() > 0) {
                    if (q.getChegirma() != null) {
                        if (q.getChegirma().signum() > 0) {
                            jami = jami.add(q.getNarx()
                                .multiply(BigDecimal.valueOf(q.getSoni()))
                                .subtract(q.getChegirma()));
                        } else {
                            jami = jami.add(q.getNarx());
                        }
                    } else {
                        jami = jami.add(q.getNarx());
                    }
                }
            }
        }
    }
    return jami;
}
```

Yechim murakkablikni yo'qotish emas, uni bir nechta nomli metodga taqsimlash. Har bir ajratilgan metod o'z nomi bilan nima qilayotganini aytadi va har birining murakkabligi chegaradan past bo'ladi.

```java
// O'tadigan variant: har bir metod bitta qarorni oladi
public BigDecimal hisobla(Buyurtma b) {
    return b.getQatorlar().stream()
        .filter(q -> q.getSoni() > 0)
        .map(this::qatorSummasi)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}

private BigDecimal qatorSummasi(Qator q) {
    BigDecimal xom = q.getNarx().multiply(BigDecimal.valueOf(q.getSoni()));
    return xom.subtract(chegirma(q));
}

private BigDecimal chegirma(Qator q) {
    // null va nol chegirma bir xil ishlanadi
    BigDecimal ch = q.getChegirma();
    return (ch == null || ch.signum() <= 0) ? BigDecimal.ZERO : ch;
}
```

Bu bo'linish testga ham yordam beradi. `chegirma` metodini to'g'ridan to'g'ri qoplash uchun uchta kichik test kerak, aks holda o'sha tarmoqlarni faqat katta integratsion test orqali bosib o'tish mumkin bo'ladi.

## 13.2 Parametrlar soni va ularni obyektga yig'ish

`java:S107` metod parametrlari sonini cheklaydi, standart chegara yetti (sozlanadi). Ko'p parametrning asl muammosi soni emas: bir xil tipdagi qo'shni parametrlarni chaqiruv joyida almashtirib yuborish juda oson va kompilyator buni ko'rmaydi.

```java
// Sonar shikoyat qiladigan variant: tartibni adashtirish oson
public Tolov yarat(String mijozId, String karta, String valyuta,
                  BigDecimal summa, BigDecimal komissiya,
                  String izoh, boolean takrorlash, String idempotencyKey) {
    // ...
}
```

Parametrlarni ma'nosi bo'yicha bitta immutable record ichiga yig'ish kerak. Shunda nomlar chaqiruv joyida ko'rinadi va validatsiya bir joyga to'planadi.

```java
// O'tadigan variant: nomlangan maydonlar, markazlashgan validatsiya
public record TolovSorovi(
        String mijozId, String karta, String valyuta,
        BigDecimal summa, BigDecimal komissiya,
        String izoh, boolean takrorlash, String idempotencyKey) {

    public TolovSorovi {
        // konstruktor ichida shartni bir marta tekshiramiz
        Objects.requireNonNull(mijozId, "mijozId bo'sh bo'lmasligi kerak");
        if (summa == null || summa.signum() <= 0) {
            throw new IllegalArgumentException("summa musbat bo'lishi kerak");
        }
    }
}

public Tolov yarat(TolovSorovi sorov) { /* ... */ }
```

## 13.3 Ichma-ich shartlarni erta qaytish bilan yassilash

Ichma-ichlik cognitive complexity ga eng ko'p hissa qo'shadi. Bundan tashqari bitta `if` ichida yana bitta `if` turgan holat alohida qoida bilan belgilanadi (`java:S1066`): ularni `&&` bilan birlashtirish yoki erta qaytish bilan yassilash kerak.

```java
// Sonar shikoyat qiladigan variant: uch daraja ichma-ichlik
public void jonat(Buyurtma b) {
    if (b.getHolat() == Holat.TOLANGAN) {
        if (b.getManzil() != null) {
            if (omborda(b)) {
                kuryerga.ber(b);
            }
        }
    }
}
```

Erta qaytish har bir shartni alohida gapga aylantiradi va asosiy yo'l metodning oxirida yolg'iz qoladi.

```java
// O'tadigan variant: guard clause, yassi struktura
public void jonat(Buyurtma b) {
    if (b.getHolat() != Holat.TOLANGAN) {
        return;
    }
    if (b.getManzil() == null) {
        throw new ManzilYoqException(b.getId());
    }
    if (!omborda(b)) {
        kutishGaQoy(b);
        return;
    }
    kuryerga.ber(b);
}
```

Bu yerda bitta tuzoq bor. Qaytish nuqtalari juda ko'payib ketsa, alohida qoida ishga tushadi (`java:S1142`, standart chegara uchta `return`). Demak erta qaytishni shartni soddalashtirish uchun ishlating, metodga o'nta chiqish eshigi yasash uchun emas. Agar chiqish nuqtalari ko'paysa, bu metodni bo'lish vaqti kelgani belgisi.

## 13.4 `null` ni qaytarmaslik va `Optional` ni to'g'ri ishlatish

Sonar `null` bilan ikki tomondan ishlaydi. Birinchisi bug sifatidagi tekshiruv: analizator oqimni kuzatib, `null` bo'lishi mumkin bo'lgan qiymat dereference qilinganini topadi (`java:S2259`). Ikkinchisi dizayn qoidalari: massiv yoki kolleksiya o'rniga `null` qaytarish (`java:S1168`), `Optional` ning o'zini `null` qilib qo'yish (`java:S2789`) va `isPresent()` tekshirmasdan `get()` chaqirish (`java:S3655`).

```java
// Sonar shikoyat qiladigan variant: null kolleksiya va tekshirilmagan get()
public List<Tolov> tolovlar(String mijozId) {
    Mijoz m = repo.find(mijozId);
    if (m == null) {
        return null; // chaqiruvchi NPE oladi
    }
    return m.getTolovlar();
}

public String kartaRaqami(String mijozId) {
    Optional<Mijoz> m = repo.findById(mijozId);
    return m.get().getKarta(); // isPresent() yo'q
}
```

To'g'ri variantda yo'qlik ikki xil tilda ifodalanadi: kolleksiya uchun bo'sh kolleksiya, bitta obyekt uchun `Optional`.

```java
// O'tadigan variant
public List<Tolov> tolovlar(String mijozId) {
    return repo.findById(mijozId)
        .map(Mijoz::getTolovlar)
        .orElseGet(List::of); // hech qachon null emas
}

public String kartaRaqami(String mijozId) {
    return repo.findById(mijozId)
        .map(Mijoz::getKarta)
        .orElseThrow(() -> new MijozYoqException(mijozId));
}
```

`Optional` ni maydon yoki metod parametri sifatida ishlatmaslik kerak. U faqat qaytish tipi uchun mo'ljallangan va boshqa joyda ishlatilsa Sonar ham, review ham shikoyat qiladi.

## 13.5 Istisnolarni to'g'ri ushlash: umumiy `Exception` ni ushlamaslik, yutib yubormaslik

Bu yerda bir nechta qoida birgalikda ishlaydi. Keng `Exception` yoki `RuntimeException` ni kerak bo'lmaganda ushlash (`java:S2221`), `Throwable` yoki `Error` ni ushlash (`java:S1181`), umumiy istisnoni o'zi tashlash (`java:S112`), bo'sh `catch` bloki (`java:S108`), `printStackTrace()` chaqirish (`java:S1148`) va `InterruptedException` ni qayta tiklamaslik (`java:S2142`).

```java
// Sonar shikoyat qiladigan variant: sabab yo'qoladi, xato yashiriladi
public void tolovniYubor(TolovSorovi s) {
    try {
        gateway.charge(s);
    } catch (Exception e) {
        e.printStackTrace(); // log emas, stdout
    }
}
```

Bu kodning eng yomon tomoni Sonar emas, ishlab chiqarish: to'lov muvaffaqiyatsiz bo'lsa ham chaqiruvchi hech narsa bilmaydi. To'g'ri variant aniq tiplarni ushlaydi, sababni saqlaydi va domen istisnosiga o'raydi.

```java
// O'tadigan variant: aniq tip, sabab saqlangan, interrupt tiklangan
public void tolovniYubor(TolovSorovi s) {
    try {
        gateway.charge(s);
    } catch (GatewayTimeoutException e) {
        // sabab (cause) uzatiladi, stack trace yo'qolmaydi
        throw new TolovVaqtinchaMumkinEmasException(s.idempotencyKey(), e);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt(); // flagni tiklaymiz
        throw new TolovBekorQilindiException(s.idempotencyKey(), e);
    }
}
```

Agar istisnoni chindan ham e'tiborsiz qoldirish kerak bo'lsa, buni ochiq yozish kerak: `catch` ichida izoh va kamida `log.debug` bo'lsin. Bo'sh blok bilan jim qolish review da ham, Sonar da ham eng qimmat odat.

| Tuzoq | Sonar nima deydi | Yechim |
| --- | --- | --- |
| `catch (Exception e)` hamma joyda | keng istisnoni ushlash shikoyati | aniq tiplarni alohida ushlash |
| `catch` bloki bo'sh | bo'sh blok qoidasi | log yozish yoki qayta tashlash |
| `throw new RuntimeException(msg)` | umumiy istisno tashlash | domen istisnosi yaratish |
| `new XException(e.getMessage())` | shikoyat bo'lmasligi mumkin, lekin cause yo'qoladi | `cause` ni konstruktorga uzatish |
| `InterruptedException` yutilgan | interrupt holati tiklanmagan | `Thread.currentThread().interrupt()` |
| `e.printStackTrace()` | stdout ga yozish shikoyati | logger orqali yozish |
| `finally` ichida `return` | boshqarish oqimi buzilishi | `finally` da faqat tozalash |
| oqim `close()` qilinmagan | resurs yopilmagan shikoyati | `try-with-resources` |

## 13.6 Resurslarni yopish: `try-with-resources` va yopilmagan oqim

`java:S2095` metoddan chiqishdan oldin yopilmagan `Closeable` ni topadi. Qiyin tomoni shundaki, qo'lda yozilgan `finally` ko'pincha to'liq emas: resurs yaratilishi bilan istisno orasida bo'shliq qoladi yoki ikkita resursdan ikkinchisi yopilmaydi.

```java
// Sonar shikoyat qiladigan variant: istisno bo'lsa resurs ochiq qoladi
public int hisobotYoz(String yol, List<Qator> qatorlar) throws IOException {
    BufferedWriter w = new BufferedWriter(new FileWriter(yol));
    for (Qator q : qatorlar) {
        w.write(q.toCsv());  // bu yerda istisno bo'lsa close() chaqirilmaydi
        w.newLine();
    }
    w.close();
    return qatorlar.size();
}
```

```java
// O'tadigan variant: try-with-resources, bir nechta resurs ham xavfsiz
public int hisobotYoz(Path yol, List<Qator> qatorlar) throws IOException {
    try (BufferedWriter w = Files.newBufferedWriter(yol)) {
        for (Qator q : qatorlar) {
            w.write(q.toCsv());
            w.newLine();
        }
    } // close() har qanday holatda chaqiriladi
    return qatorlar.size();
}

// Stream ham resurs: Files.lines() ni ham yopish kerak
public long qatorSoni(Path yol) throws IOException {
    try (Stream<String> satrlar = Files.lines(yol)) {
        return satrlar.filter(s -> !s.isBlank()).count();
    }
}
```

Spring kontekstida `JdbcTemplate`, `RestClient` va `EntityManager` ni o'zingiz yopmaysiz, ularni framework boshqaradi. Lekin `Files.lines`, `Stream` qaytaradigan JPA so'rovlari va qo'lda ochilgan `Connection` sizning mas'uliyatingizda qoladi.

## 13.7 O'zgaruvchan holatni cheklash: `final`, immutable obyekt

Sonar bu yerda bir nechta tomondan yondashadi: `public` o'zgaruvchan maydon (`java:S1104`), o'qilmagan qiymat tayinlash (dead store, `java:S1854`), parametrni metod ichida qayta tayinlash va kolleksiyani to'g'ridan to'g'ri tashqariga qaytarish. Asosiy g'oya bitta: obyekt yaratilgandan keyin o'zgarmasa, uning hech qanday tarmog'ini tekshirish kerak emas.

```java
// Sonar shikoyat qiladigan variant: tashqaridan buzish mumkin
public class OmborQoldigi {
    public Map<String, Integer> qoldiq = new HashMap<>(); // ochiq maydon
    public List<String> ogohlantirishlar;

    public void yukla(Map<String, Integer> manba) {
        this.qoldiq = manba;        // tashqi map ga ishonamiz
        manba = new HashMap<>();    // parametrni qayta tayinlash, foydasiz
    }
}
```

```java
// O'tadigan variant: immutable holat, nusxa olish
public final class OmborQoldigi {
    private final Map<String, Integer> qoldiq;

    public OmborQoldigi(Map<String, Integer> manba) {
        // mudofaa nusxasi: tashqi o'zgarish bizga ta'sir qilmaydi
        this.qoldiq = Map.copyOf(manba);
    }

    public int soni(String sku) {
        return qoldiq.getOrDefault(sku, 0);
    }

    public Map<String, Integer> barchasi() {
        return qoldiq; // allaqachon o'zgarmas
    }
}
```

Immutable obyektning Sonar uchun yana bir foydasi bor: concurrency qoidalari (`synchronized` yetishmasligi, ikki marta tekshirilgan lock) umuman ishga tushmaydi, chunki o'zgaradigan holat yo'q.

## 13.8 Takrorlanuvchi literal va magic number ni konstantaga chiqarish

`java:S1192` bir xil string literal bir faylda uch marta (standart sozlama) uchrasa shikoyat qiladi. `java:S109` esa izohsiz raqamlarni topadi. Ikkalasining asl zarari bir xil: qiymat o'zgarganda uni hamma joyda topish kerak bo'ladi va bitta joy esdan chiqadi.

```java
// Sonar shikoyat qiladigan variant: takrorlanuvchi literal va magic number
public void tekshir(Tolov t) {
    if (t.getValyuta().equals("UZS") && t.getSumma().compareTo(
            BigDecimal.valueOf(50000000)) > 0) {
        audit.yoz("LIMIT_OSHDI", t.getId());
    }
    if (t.getValyuta().equals("UZS") && t.getUrinish() > 3) {
        audit.yoz("LIMIT_OSHDI", t.getId());
    }
}
```

```java
// O'tadigan variant: nomlangan konstantalar ma'noni ham tushuntiradi
private static final String VALYUTA_UZS = "UZS";
private static final String AUDIT_LIMIT = "LIMIT_OSHDI";
private static final BigDecimal KUNLIK_LIMIT = new BigDecimal("50000000");
private static final int MAX_URINISH = 3;

public void tekshir(Tolov t) {
    if (!VALYUTA_UZS.equals(t.getValyuta())) {
        return;
    }
    if (t.getSumma().compareTo(KUNLIK_LIMIT) > 0 || t.getUrinish() > MAX_URINISH) {
        audit.yoz(AUDIT_LIMIT, t.getId());
    }
}
```

Agar qiymat muhitga qarab o'zgarsa, konstanta emas, konfiguratsiya kerak: `@ConfigurationProperties` yoki `application.yaml`. Konstantaga chiqarish faqat kod uchun haqiqatan o'zgarmas qiymatlarga tegishli.

## 13.9 To'g'ri taqqoslash: `equals`, `compareTo`, suzuvchi nuqta, `BigDecimal`

Taqqoslash qoidalari Sonar da bug kategoriyasida turadi, ya'ni ular quality gate ning yangi kod shartini eng tez buzadigan guruh. Eng ko'p uchraydiganlari: obyektlarni `==` bilan solishtirish (`java:S4973`), suzuvchi nuqta sonlarini tenglikka tekshirish (`java:S1244`), `equals` ni `hashCode` siz override qilish (`java:S1206`).

```java
// Sonar shikoyat qiladigan variant
boolean bir = statusKod == "OK";                 // String ni == bilan
boolean ikki = jami == 0.1 + 0.2;                // double tenglik, hech qachon rost emas
BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("1.00");
boolean uch = a.equals(b);                       // false: scale farq qiladi
BigDecimal narx = new BigDecimal(0.1);           // ikkilik xato kiradi
```

```java
// O'tadigan variant
boolean bir = "OK".equals(statusKod);            // NPE ham bo'lmaydi
boolean ikki = Math.abs(jami - 0.3) < 1e-9;      // epsilon bilan
boolean uch = a.compareTo(b) == 0;               // qiymat bo'yicha teng
BigDecimal narx = new BigDecimal("0.1");         // String konstruktor
// pul uchun doim BigDecimal va aniq scale
BigDecimal yakun = narx.multiply(BigDecimal.valueOf(3))
        .setScale(2, RoundingMode.HALF_UP);
```

Pul bilan ishlaganda `double` ni butunlay chiqarib tashlash kerak. Bu bitta Sonar qoidasi emas, ammo u bir vaqtning o'zida `java:S1244` ni, yumaloqlash bug'larini va hisobot farqlarini yo'q qiladi.

## 13.10 Loglash qoidalari: formatlangan xabar, istisno uzatish, maxfiy ma'lumot

`java:S2629` log chaqiruvida argument oldindan hisoblanishini topadi: string konkatenatsiya log darajasi o'chirilgan bo'lsa ham bajariladi. Bundan tashqari maxfiy ma'lumotni logga yozish security kategoriyasiga tushadi va foydalanuvchi kiritgan matnni to'g'ridan to'g'ri logga qo'yish log injection sifatida belgilanishi mumkin.

```java
// Sonar shikoyat qiladigan variant
log.debug("Tolov: " + sorov.toString() + " karta=" + sorov.karta());
try {
    gateway.charge(sorov);
} catch (GatewayException e) {
    log.error("xato: " + e.getMessage()); // stack trace yo'q
}
```

```java
// O'tadigan variant: placeholder, maskalangan ma'lumot, istisno obyekti
log.debug("Tolov qabul qilindi id={} karta={}", sorov.idempotencyKey(),
        maskala(sorov.karta()));
try {
    gateway.charge(sorov);
} catch (GatewayException e) {
    // istisnoni oxirgi argument sifatida uzatamiz: stack trace saqlanadi
    log.error("Gateway xatosi id={}", sorov.idempotencyKey(), e);
    throw new TolovXatosiException(sorov.idempotencyKey(), e);
}

private static String maskala(String karta) {
    return karta == null ? "null" : "****" + karta.substring(karta.length() - 4);
}
```

Yana bir muhim nuqta: `log.error` va keyin istisnoni qayta tashlash ikkita log yozuvi beradi. Qoidani bitta qilib qo'yish kerak: yoki shu joyda log yoziladi va istisno yutiladi (kamdan kam), yoki istisno tashlanadi va log eng yuqori qatlamda bir marta yoziladi.

## 13.11 Kodni Sonar nuqtai nazaridan o'qib chiqish odati

Eng samarali usul analizator natijasini kutmaslik. Pull request yuborishdan oldin o'z diff ingizni o'nta savol bilan o'qib chiqish Sonar topadigan shikoyatlarning katta qismini oldindan yo'q qiladi: metodda nechta ichma-ich daraja bor, qaysi resurs yopilmagan, qaysi `catch` jim, qaysi literal uchinchi marta takrorlanmoqda, qaysi `equals` yetishmaydi. IDE da SonarLint o'rnatilgan bo'lsa bu tekshiruv yozish paytida bo'ladi va server tahliliga faqat qoida farqlari qoladi.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Shikoyat paydo bo'ldi | tezda `//NOSONAR` qo'yiladi | sababi tuziladi, suppress faqat asoslangan holda |
| Murakkab metod | chegara sozlamasi oshiriladi | metod nomli bo'laklarga ajratiladi |
| Ko'p parametr | yangi overload qo'shiladi | parametrlar record ga yig'iladi |
| `null` qaytish | chaqiruvchida `if (x != null)` | `Optional` yoki bo'sh kolleksiya shartnomaga kiritiladi |
| Keng `catch` | `catch (Exception e)` qoldiriladi | aniq tip, cause uzatish, domen istisnosi |
| Resurs yopish | qo'lda `finally` yoziladi | `try-with-resources` majburiy qilinadi |
| Takrorlangan literal | nusxa ko'chirilib ketadi | konstanta yoki konfiguratsiya ajratiladi |
| Pul hisobi | `double` bilan ishlanadi | `BigDecimal` va aniq `RoundingMode` |
| Log yozish | string konkatenatsiya | placeholder va maskalash standarti |
| Qoida o'zgarishi | har kim o'zicha tuzatadi | quality profile versiyalanadi va jamoada kelishiladi |

Oxirgi qatorga alohida e'tibor bering. Bu bobdagi hamma narsa quality profile da yoqilgan qoidalarga bog'liq, chegaralar esa sozlanadi. Shuning uchun "bu kod Sonar dan o'tadi" degan gap faqat ma'lum profil va ma'lum chegaralar uchun to'g'ri bo'ladi. Jamoada profilni yozib qo'yish va uni o'zgartirishni ongli qaror qilib belgilash kodni tuzatishdan ko'ra ko'proq foyda beradi.

## 13.12 Amalda qo'llash

- [ ] O'z modulingizda cognitive complexity bo'yicha eng yuqori beshta metodni toping va ularni erta qaytish bilan yassilab, nomli private metodlarga ajratib chiqing.
- [ ] Beshdan ko'p parametrli public metodlarni sanab chiqing va ularning kamida bittasini immutable `record` parametrga o'tkazing, validatsiyani konstruktorga yig'ing.
- [ ] Loyihadagi `return null` holatlarini qidirib, kolleksiya qaytaradiganlarini bo'sh kolleksiyaga, bitta obyekt qaytaradiganlarini `Optional` ga o'zgartiring.
- [ ] Barcha `catch (Exception` va `catch (Throwable` joylarini ko'rib chiqing: aniq tipga toraytiring, `cause` ni uzating, bo'sh bloklarni yo'q qiling.
- [ ] `Closeable` va `Stream` qaytaradigan chaqiruvlarni tekshirib, qo'lda yozilgan `finally` bloklarini `try-with-resources` ga ko'chiring.
- [ ] Pul bilan ishlaydigan hamma joyda `double` va `float` ni `BigDecimal` ga o'tkazing, `equals` o'rniga `compareTo` ishlating va `setScale` ni aniq belgilang.
- [ ] Log chaqiruvlarini placeholder formatiga keltiring, istisnoni oxirgi argument sifatida uzating va karta, token, parol kabi maydonlar uchun maskalash yordamchisi yozing.
- [ ] IDE ga SonarLint o'rnatib, uni serverdagi quality profile ga ulang, so'ngra pull request oldidan diff ni shu bobdagi savollar ro'yxati bilan o'qib chiqish odatini jamoa qoidasiga kiriting.

---

[&larr; 12. Exclusion: nimani chiqarish halol, nimani chiqarish aldov](12-exclusion-nimani-chiqarish-halol-nimani.md) · [Mundarija](README.md) · [14. Java va Spring da eng ko'p uchraydigan issue va ularning yechimi &rarr;](14-java-va-spring-da-eng-kop-uchraydigan-issue.md)
