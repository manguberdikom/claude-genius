<!-- doc: clean-code | chapter: 10 | part: III. Izoh va hujjat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 10. Javadoc va API hujjati (Javadoc and API Documentation)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [10.1 Javadoc kimga yoziladi va qayerga yozilmaydi](#101-javadoc-kimga-yoziladi-va-qayerga-yozilmaydi)
- [10.2 Birinchi gap qoidasi va fe'l shakli](#102-birinchi-gap-qoidasi-va-fel-shakli)
- [10.3 `@param`, `@return`, `@throws` to'liqligi](#103-param-return-throws-toliqligi)
- [10.4 Shartnoma yozish: oldin shart, keyin shart, invariant](#104-shartnoma-yozish-oldin-shart-keyin-shart-invariant)
- [10.5 `{@link}`, `{@code}`, `@see` va havola gigiyenasi](#105-link-code-see-va-havola-gigiyenasi)
- [10.6 `@since`, `@deprecated` va almashtirish ko'rsatmasi](#106-since-deprecated-va-almashtirish-korsatmasi)
- [10.7 Paket va modul hujjati](#107-paket-va-modul-hujjati)
- [10.8 Namuna kod va uni kompilyatsiya ostida ushlash](#108-namuna-kod-va-uni-kompilyatsiya-ostida-ushlash)
- [10.9 Javadoc ni CI da tekshirish](#109-javadoc-ni-ci-da-tekshirish)
- [10.10 Kod ichidagi hujjat va repodagi hujjat bo'linishi](#1010-kod-ichidagi-hujjat-va-repodagi-hujjat-bolinishi)
- [10.11 Hujjatni tasvirlash qiyinligi (Red Flag: Hard to Describe)](#1011-hujjatni-tasvirlash-qiyinligi-red-flag-hard-to-describe)
- [10.12 Hujjatni kod kabi boshqarish: ega, kanoniklik, yangilik](#1012-hujjatni-kod-kabi-boshqarish-ega-kanoniklik-yangilik)
- [10.13 Amalda qo'llash](#1013-amalda-qollash)

</details>


Public API ni o'zini hujjatlaydigan qilish [arxitektor hujjatidagi](../architect/README.md) o'zini hujjatlaydigan API bo'limida ko'rib chiqilgan. Bu bobda Javadoc ning mexanikasi: nimani yozish, qanday shaklda, qanday tekshirish. Javadoc yagona izoh turi bo'lib, uni mashina tekshiradi va shu sababli uni toza ushlash mumkin.

## 10.1 Javadoc kimga yoziladi va qayerga yozilmaydi

Javadoc ning adresati - sinf ichini ko'rmaydigan foydalanuvchi. Shundan to'g'ri qamrov kelib chiqadi: Javadoc modul yoki kutubxona chegarasidan tashqariga chiqadigan har bir elementga yoziladi, qolgan joyga yozilmaydi.

| Element | Javadoc |
|---|---|
| Public kutubxona API si | majburiy va to'liq |
| Modullar orasidagi public interfeys | majburiy, shartnoma bilan |
| Spring `@Service` ichidagi public metod | faqat shartnoma noaniq bo'lsa |
| Controller metodi | OpenAPI annotatsiyasi, Javadoc emas |
| `private`, `package-private` | kerak emas |
| Record komponentlari | `@param` bilan, agar nom yetarli bo'lmasa |
| Getter/setter | kerak emas |
| Test metodi | kerak emas (nom aytadi) |
| Enum a'zosi | agar ma'nosi nomdan ko'rinmasa |

Jadval "qayerga" savoliga javob beradi, "kimga" savoliga esa yozishdan oldin javob topiladi. Google ning hujjat bo'yicha ko'rsatmasi: yozuvchining eng keng tarqalgan xatosi faqat o'zi uchun yozish, chunki shunda o'zi bilgan narsa aytilmay qoladi. Shuning uchun **birlamchi auditoriya** oldindan belgilanadi: kutubxona foydalanuvchisi uchun yozilgan hujjat va uni saqlovchi jamoa uchun yozilgan hujjat bir fayl emas. Implementatsiya tafsiloti va dizayn qarori saqlovchiga kerak, foydalanuvchi uni o'qimasligi kerak; dizayn sababi API hujjatida emas, alohida qaror hujjatida turadi. Auditoriya bir nechta bo'lsa hujjatni **qisqa tutish** ikki tomonni ham qondiradi: avval hammasi yoziladi, keyin tahrir o'tib takror olib tashlanadi.

Auditoriyaning ikkinchi o'lchovi - o'quvchi hujjatga qanday kelgani. **Izlovchi** (seeker) nimani qidirayotganini biladi va shu yerdan topish-topmasligini bilmoqchi: unga **izchil format** kerak, chunki u skanerlaydi. Bir fayldagi hamma metod izohi bir xil qolipda yozilsa, izlovchi faqat fe'llarni o'qib kerakli metodni ajratadi. **Qoqiluvchi** (stumbler) nimani qidirayotganini aniq bilmaydi: unga aniqlik kerak, ya'ni fayl yoki paket boshida shu kodning maqsadini aytuvchi kirish ([paket va modul hujjati](#107-paket-va-modul-hujjati)). Kirish qismi hujjat kimga mos kelmasligini ham aytishi mumkin ("bu sahifa kompilyator bilan ishlamaydigan o'quvchiga kerak emas"), bu bir qator eng foydali qatorlardan biri.

ESLATMA: `@Service` va `@Repository` ichidagi metodda birlamchi auditoriya ko'pincha o'z jamoangiz, shuning uchun u yerda Javadoc o'rniga kod ichidagi izoh va test nomi ishlaydi; korpus qo'shimchasi, Google bu misolni bermaydi.

## 10.2 Birinchi gap qoidasi va fe'l shakli

Javadoc ning birinchi gapi xulosa sifatida indeksga chiqadi, shuning uchun u mustaqil o'qilishi kerak va nuqta bilan tugashi shart. Konvensiya: metod uchun uchinchi shaxs fe'l ("Qaytaradi...", "Rezerv qiladi..."), sinf uchun ot iborasi.

```java
/**
 * Buyurtma uchun omborda qoldiqni rezerv qiladi.
 *
 * <p>Rezerv idempotent: bir xil {@code reservationKey} bilan takroriy chaqiruv
 * yangi rezerv yaratmaydi va mavjudini qaytaradi.
 *
 * @param order rezerv qilinadigan buyurtma, {@code null} bo'lmaydi
 * @param reservationKey takroriy chaqiruvni aniqlash kaliti
 * @return yaratilgan yoki mavjud rezerv
 * @throws InsufficientStockException qoldiq yetmasa
 * @throws IllegalArgumentException {@code order} bo'sh bo'lsa
 */
public Reservation reserve(Order order, ReservationKey reservationKey) { ... }
```

Birinchi gapning chegarasi mexanik: xulosa tavsifi birinchi nuqtada, agar uning ketidan bo'sh joy kelsa, tugaydi. Shuning uchun gap ichidagi qisqartma tavsifni vaqtidan oldin kesib qo'yadi va indeks sahifasida yarim jumla qoladi. Yechim ikki xil: qisqartmani `{@literal}` bilan o'rash yoki gapni qisqartmasiz qayta yozish. Bu jim xato - kompilyatsiya o'tadi, test yiqilmaydi, faqat hujjat buziladi, shuning uchun uni Javadoc chiqishini ko'rmasdan sezish qiyin (10.9).

Ikkinchi talab sinf darajasida: bir sinfda ikki a'zo yoki konstruktor bir xil xulosa tavsifiga ega bo'lmasligi kerak. Xulosalar indeks sahifasida yonma-yon chiqadi, bir xil bo'lsa o'quvchi qaysi birini tanlashni bilmaydi. Overload lar bu xatoga eng moyil, chunki ularning izohi ko'pincha ko'chirib qo'yiladi: har bir overload nima bilan farq qilishini aynan xulosa gapida aytishi kerak (5.10).

## 10.3 `@param`, `@return`, `@throws` to'liqligi

Uchta teg to'liq bo'lishi kerak yoki umuman bo'lmasligi kerak - yarim to'ldirilgan Javadoc eng yomon holat, chunki o'quvchi qolganini ham yo'q deb o'ylaydi.

Har bir teg uchun aniq talab bor. `@param` - qiymatning ma'nosi va chegarasi (`null` bo'lishi mumkinmi, diapazon qanday). `@return` - nima qaytadi va bo'sh holat qanday ifodalanadi. `@throws` - **har bir** tekshiriladigan istisno, va unchecked istisnolardan chaqiruvchi uchun ma'noli bo'lganlari.

```java
// yomon: tur nomini takrorlaydi, ma'lumot bermaydi
/** @param amount summa */

// yaxshi: ma'no, birlik, chegara
/** @param amount qaytarilayotgan summa; musbat va to'langan summadan oshmasligi kerak */
```

**To'liq teg va bitta nasr jumlasi: qaysi biri qachon.** Google ning uslub ko'rsatmasi teskari pozitsiyada turadi: ular `Returns:` va `Throws:` kabi shablon bo'limlarini zarur deb topmagan va funksiya izohini fe'l bilan boshlanadigan bitta nasriy izoh shaklida yozishni tavsiya qiladi ("Mijoz uchun berilgan nom va manzil bilan yangi yozuv yaratadi va yozuv ID sini qaytaradi, bu nomdagi yozuv allaqachon bor bo'lsa `DuplicateEntryError` tashlaydi"). Sabab: keyingi shart, parametr, qaytish qiymati va istisno holati bir-biridan mustaqil emas, ularni sun'iy bo'limlarga ajratish izohni uzaytiradi va aniqroq qilmaydi.

Ikki pozitsiyani ajratuvchi shart - **izohni kim o'qiydi va qaysi vosita ko'rsatadi**:

- **Chop etiladigan Javadoc sahifasi bo'lsa teg to'liq yoziladi.** `javadoc` chiqishi `@param` va `@throws` ni alohida jadvalga joylaydi, IDE esa parametr ustiga kursor qo'yganda aynan `@param` matnini ko'rsatadi. Nasr ichiga yashirilgan ma'lumot bu ikki joyga chiqmaydi, ya'ni izlovchi uni ko'rmaydi. Google ning misoli C++ header izohi, u yerda bunday generator yo'q.
- **Chegara noaniq bo'lsa teg to'liq yoziladi.** `null` ruxsatimi, diapazon qanday, bo'sh natija qanday ifodalanadi: bu qatorlar tegsiz nasrda yo'qoladi.
- **Shartnoma bitta gapga sig'sa nasr afzal.** `@param amount summa` kabi tur nomini takrorlovchi teg hech narsa bermaydi; bunday holatda uchta bo'sh teg o'rniga bitta to'liq jumla yoziladi. Yarim to'ldirilgan teg to'plami esa ikki pozitsiyada ham eng yomon variant.

Teg to'liq yozilganda matnining grammatik shakli ham konvensiyaga bog'langan: `@param` va `@return` dan keyingi matn ot iborasi ("qaytarilayotgan summa", "yaratilgan rezerv"), `@throws` dan keyingi matn esa "agar" bilan boshlanadigan shart ("agar qoldiq yetmasa"). Uchalasi ham nuqta bilan tugamaydi, chunki ular gap emas: generator ularni jadval yacheykasiga joylaydi.

Generik tur va metodda to'liqlik tur parametrlarini ham qamraydi: `@param <K>` va `@param <V>` har biri hujjatlanadi. Tur parametrining nomi qisqa bo'lgani uchun (3.8) uning ma'nosi faqat shu tegda aytiladi va boshqa joyda yozilmaydi.

Istisno tomonida ikki alohida qoida bor va ularni aralashtirmaslik kerak. Birinchisi `throws` e'loniga tegishli: tekshiriladigan istisnolar har biri alohida e'lon qilinadi. `throws Exception` yoki `throws Throwable` mijozga hech qanday yo'l-yo'riq bermaydi va shu kontekstda chiqadigan boshqa istisnolarni ham yashiradi; yagona asosli istisno - `main` metodi. Ikkinchisi `@throws` tegiga tegishli: har bir istisno `@throws` bilan hujjatlashtiriladi, lekin tekshirilmaydigan istisno `throws` kalit so'ziga **yozilmaydi**. Shunda `throws` siz turgan `@throws` o'quvchiga istisnoning tekshirilmaydigan ekanini vizual ko'rsatadi va bu farqni bilish uchun istisno ierarxiyasini ochish kerak bo'lmaydi.

```java
// yomon: umumiy superclass e'lon qilingan, teg matni gap shaklida
/**
 * @param amount Qaytarilayotgan summa.
 * @throws Exception Xato bo'lsa.
 */
public Refund refund(Money amount) throws Exception { ... }

// yaxshi: har bir checked istisno alohida, unchecked faqat tegda
/**
 * @param amount qaytarilayotgan summa, to'langan summadan oshmaydi
 * @return yaratilgan qaytarish yozuvi
 * @throws GatewayUnavailableException agar to'lov shlyuzi javob bermasa
 * @throws RefundLimitExceededException agar summa to'langan summadan oshsa
 * @throws IllegalArgumentException agar {@code amount} musbat bo'lmasa
 */
public Refund refund(Money amount)
        throws GatewayUnavailableException, RefundLimitExceededException { ... }
```

## 10.4 Shartnoma yozish: oldin shart, keyin shart, invariant

Javadoc ning eng qimmatli qismi - shartnoma. Uchta savolga javob berish kerak: chaqirishdan oldin nima to'g'ri bo'lishi kerak (precondition), chaqiruvdan keyin nima kafolatlanadi (postcondition), va nima har doim to'g'ri qoladi (invariant).

Spring va JPA kontekstida shartnomaga qo'shimcha to'rt element kiradi va ularning yo'qligi eng ko'p xatolarga sabab bo'ladi: tranzaksiya talabi, idempotentlik, thread-safety, va yon ta'sirlar.

```java
/**
 * To'lovni bank bilan yopadi.
 *
 * <p><b>Tranzaksiya:</b> chaqiruvchi tranzaksiya ochmasligi kerak - bu metod
 * tashqi chaqiruv qiladi va o'z tranzaksiyasini qisqa ushlaydi.
 * <p><b>Idempotentlik:</b> bir xil {@code paymentId} uchun takroriy chaqiruv xavfsiz.
 * <p><b>Thread-safety:</b> bu sinf stateless va thread-safe.
 * <p><b>Yon ta'sir:</b> muvaffaqiyatli yopilganda {@code PaymentSettled} hodisasi chiqadi.
 */
public SettlementResult settle(PaymentId paymentId) { ... }
```

## 10.5 `{@link}`, `{@code}`, `@see` va havola gigiyenasi

`{@code}` matnni kod shriftida ko'rsatadi va HTML belgilarini qochiradi - barcha tur nomlari, qiymatlar va `null` shu teg ichida yozilishi kerak. `{@link}` esa haqiqiy havola yaratadi va kompilyatsiya vaqtida tekshiriladi, shuning uchun sinf va metod nomlari uchun `{@code}` emas, `{@link}` afzal: nom o'zgarsa Javadoc buziladi va eslatadi.

```java
// yaxshi: havola tekshiriladi
/** Natijani {@link SettlementResult} sifatida qaytaradi, xato bo'lsa {@code null} emas. */

// yomon: matn sifatida yozilgan, nom o'zgarsa yolg'on qoladi
/** Natijani SettlementResult sifatida qaytaradi. */
```

`@see` ni faqat haqiqiy qo'shimcha kontekst uchun ishlatish kerak; har bir tegishli sinfga `@see` qo'yish shovqin.

Qolgan teglar kamroq uchraydi, lekin ularning har biri hujjat bilan kodni bitta joyda ushlab turish uchun kiritilgan.

| Teg | Nima qiladi | Qachon ishlatiladi |
|---|---|---|
| `{@inheritDoc}` | ota sinf yoki interfeysdagi izohni voris oladi | override qilingan metodda shartnomani ko'chirib yozish o'rniga |
| `{@value}` | `static` maydonning qiymatini hujjatga qo'yadi | konstanta qiymati hujjatda turishi kerak bo'lsa |
| `{@literal}` | matnni aynan ko'rsatadi, HTML va nuqtani neytrallaydi | qisqartma yoki `<`, `>` belgisi bo'lsa (10.2) |
| `@implSpec` | "Implementation Requirements" bo'limini yasaydi | self-use, ya'ni override qiluvchiga qaysi metod qachon chaqirilishini aytish (17.1) |
| `@serialData`, `@serial` | Javadoc ni seriyalangan shakl sahifasiga joylaydi | `writeObject` va seriyalanadigan maydonlar |

Jadvaldan ikki natija chiqadi. Birinchi: override qilingan metodda ota shartnomani qo'lda ko'chirish ikki nusxa yasaydi va ular vaqt o'tishi bilan ajralib ketadi, `{@inheritDoc}` esa bitta manbani qoldiradi; `{@value}` xuddi shu ishni konstanta uchun qiladi, qo'lda yozilgan qiymat esa maydon o'zgarganda jim yolg'onga aylanadi. Ikkinchi: `writeObject` `private` bo'lsa ham hujjat izohi oladi, chunki u sinfning seriyalangan shaklini, ya'ni tashqi shartnomaning bir qismini belgilaydi (25.4).

## 10.6 `@since`, `@deprecated` va almashtirish ko'rsatmasi

`@since` public API da versiya tarixini beradi va u kutubxona foydalanuvchisi uchun muhim. `@Deprecated` esa har doim ikki qismdan iborat bo'lishi kerak: annotatsiya (kompilyator ogohlantirishi uchun) va `@deprecated` Javadoc tegi (nima o'rniga ishlatilishi uchun).

```java
/**
 * @deprecated 2.4 dan boshlab o'rniga {@link #settle(PaymentId)} ishlatiladi:
 *     eski metod valyutani hisobga olmaydi. 3.0 da o'chiriladi.
 * @since 1.0
 */
@Deprecated(since = "2.4", forRemoval = true)
public void settleLegacy(long paymentId) { ... }
```

Almashtirish ko'rsatmasi bo'lmagan `@Deprecated` foydasiz: foydalanuvchi ogohlantirishni ko'radi, lekin nima qilishini bilmaydi.

**Ogohlantirish bajarilishi mumkin va o'z vaqtida bo'lishi kerak.** Google ning deprecation amaliyotida har ogohlantirishdan ikki xususiyat talab qiladi. Birinchisi - bajarilishi mumkinligi: ogohlantirish o'rtacha muhandis bilimi bilan bajariladigan keyingi qadamni aytadi, ya'ni `@deprecated` tegi almashtirish nomini beradi. Ikkinchisi - o'z vaqtida kelishi: ogohlantirish foydalanuvchi aynan shu amalni bajarayotgan paytda chiqadi. Eskirgan metod chaqiruvi haqida ogohlantirish eng foydali vaqt - muhandis shu qatorni yozayotgan payt, repoda bir necha hafta turgandan keyin emas.

Shundan amaliy qoida kelib chiqadi: ogohlantirishni **o'zgargan qatorlar** bilan cheklash. Tranzitiv ogohlantirish (A kutubxona B ga, B esa eskirgan C ga tayanadi va xabar A ning buildida chiqadi) foydalanuvchi hal qila olmaydigan shovqin bo'lib to'planadi va tibbiyotdan olingan atama bilan alert fatigue ga olib keladi: muhandis hamma ogohlantirishni o'qimay qo'yadi. Bog'liqlik grafigi bo'ylab tarqaladigan keng ogohlantirish faqat majburiy deprecation da, ya'ni jamoa foydalanuvchilarni faol ko'chirayotganda yoqiladi.

```xml
<!-- maven-compiler-plugin: deprecation ogohlantirishi faqat diffdagi kodda ko'rinadi -->
<configuration>
  <showDeprecation>true</showDeprecation>
  <failOnWarning>false</failOnWarning>
</configuration>
```

ESLATMA: Maven da ogohlantirishni o'zgargan qatorlar bilan cheklash tayyor holda yo'q; buni review vositasi (Sonar ning "new code" qamrovi) qiladi. Korpus qo'shimchasi.

## 10.7 Paket va modul hujjati

`package-info.java` fayli paketning maqsadini, chegarasini va qaysi sinflar kirish nuqtasi ekanini aytadi. Bu eng kam ishlatiladigan va eng foydali hujjat shakli, chunki yangi odam paketga kirganda birinchi shu faylni ochadi.

```java
/**
 * To'lov va bank bilan hisob-kitob konteksti.
 *
 * <p>Kirish nuqtalari: {@link uz.shop.payment.PaymentService} va
 * {@link uz.shop.payment.SettlementService}. Qolgan sinflar ichki va
 * {@code package-private}.
 *
 * <p>Bu paket boshqa paketlarning jadvallariga murojaat qilmaydi; tashqi
 * ma'lumot faqat {@link uz.shop.order.OrderApi} orqali olinadi.
 */
@NullMarked
package uz.shop.payment;
```

`@NullMarked` (JSpecify) kabi paket darajasidagi annotatsiyalar ham shu faylda turadi ([arxitektor hujjatidagi](../architect/README.md) null xavfsizligi bo'limi).

## 10.8 Namuna kod va uni kompilyatsiya ostida ushlash

Javadoc dagi namuna kod eng tez eskiradigan hujjat, chunki uni hech narsa tekshirmaydi. Java 18 dan beri `{@snippet}` tegi bor va u namunani tashqi faylga (yoki test kodiga) bog'lash imkonini beradi - shunda namuna kompilyatsiya va test ostida qoladi.

```java
/**
 * Mijozni rezerv bilan yaratadi.
 *
 * {@snippet file = "ReservationExamples.java" region = "simple-reserve"}
 */
public Reservation reserve(Order order) { ... }
```

Agar `{@snippet}` ishlatilmasa, ikkinchi yaxshi yechim: namunani testda saqlab, Javadoc da test metodiga `{@link}` qo'yish.

## 10.9 Javadoc ni CI da tekshirish

Javadoc toza qolishi uchun uni mashina tekshirishi kerak. `javadoc` vositasining `-Xdoclint` tekshiruvi buzilgan havolalarni, yetishmayotgan `@param` larni va noto'g'ri HTML ni topadi.

```xml
<plugin>
  <artifactId>maven-javadoc-plugin</artifactId>
  <configuration>
    <!-- Buzilgan havola va yetishmayotgan teg xato sifatida qaraladi -->
    <doclint>all</doclint>
    <failOnWarnings>true</failOnWarnings>
    <!-- Faqat public API hujjatlanadi: ichki sinflar shovqin qo'shmaydi -->
    <show>protected</show>
  </configuration>
  <executions>
    <execution>
      <id>javadoc-check</id>
      <phase>verify</phase>
      <goals><goal>jar</goal></goals>
    </execution>
  </executions>
</plugin>
```

Kutubxona bo'lmagan ilovada `doclint` ni faqat `api` paketlariga yo'naltirish mumkin, shunda ichki kod uchun Javadoc majburiyati tug'ilmaydi (9.4).

## 10.10 Kod ichidagi hujjat va repodagi hujjat bo'linishi

Hujjatning qayerda turishi uning hayot muddatini belgilaydi. Qoida: kod bilan birga o'zgaradigan ma'lumot kodda, undan sekinroq o'zgaradigan ma'lumot repoda, undan ham sekinroq o'zgaradigani wiki da turadi.

| Ma'lumot | Joyi |
|---|---|
| Metod shartnomasi | Javadoc |
| Paket maqsadi va chegarasi | `package-info.java` |
| Sinf ichidagi qaror asosi | kod ichidagi izoh (8.4) |
| Arxitektura qarori | `docs/adr/` ([arxitektor hujjatidagi](../architect/README.md) ADR va qaror hujjatlashtirish bo'limi) |
| Loyihani ishga tushirish | `README.md` |
| API shartnomasi (tashqi) | OpenAPI spetsifikatsiyasi |
| Domen lug'ati | `docs/glossary.md` (3.14) |
| Reliz o'zgarishlari | `CHANGELOG.md` (40.3) |
| Operatsion qo'llanma | runbook, repoda yoki wiki da |

## 10.11 Hujjatni tasvirlash qiyinligi (Red Flag: Hard to Describe)

10.3 va 10.4 hujjatni to'liq yozishni talab qiladi. Shu talabning teskari tomoni ham bor va u dizayn haqida gapiradi: metod yoki o'zgaruvchining izohi sodda va ayni paytda to'liq bo'lishi kerak, shunday izoh yozish qiyin bo'lsa, tasvirlanayotgan narsaning dizaynida muammo bor (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 15.3). Ousterhout izohni murakkablik koniga tushirilgan kanareykaga qiyoslaydi: metod yoki o'zgaruvchi uzun izoh talab qilsa, bu abstraksiya topilmaganining birinchi belgisi.

Mezon shu yerda aniq ko'rsatilgan. Yaxshi sinf chuqur bo'ladi: interfeysi sodda, ichida bajarayotgan ishi katta. Interfeysning murakkabligini o'lchashning eng yaxshi usuli esa uni tasvirlaydigan izoh: agar metodning interfeys izohi uni ishlatish uchun kerakli hamma narsani beradi va shu bilan birga qisqa bo'lsa, interfeys sodda; agar metodni uzun va murakkab izohsiz to'liq tasvirlash imkoni bo'lmasa, interfeys murakkab. Interfeys izohini implementatsiya bilan solishtirish chuqurlikni ko'rsatadi: izoh implementatsiyaning hamma asosiy xususiyatini aytib berishga majbur bo'lsa, metod yuzaki (shu yerda, 15.3).

| Hujjatdagi belgi | Nimani bildiradi | Harakat |
|---|---|---|
| `@param` lar soni ko'p va har biriga chegara sharti kerak | parametrlar bir-biriga bog'liq | parametr obyektiga yig'ish (32.14) |
| Shartnoma "agar ... bo'lsa boshqacha ishlaydi" bilan shoxlanadi | bitta metod ikki ishni qiladi | metodni bo'lish (4-bob) |
| `boolean` parametr ma'nosini izohlab berish kerak | bayroq xatti-harakatni tanlaydi | ikki alohida metod (5-bob) |
| `@return` bo'sh va xato holatini uzun tasvirlaydi | qaytish turi yetarli emas | `Optional` yoki natija turi (18-bob) |
| Maydon izohi uzun | maydonlarga bo'lish noto'g'ri | o'z turiga ajratish (32.15) |

```java
// yomon: shartnomani faqat uzun izoh bilan aytib berish mumkin, chunki
// metod bayroqqa qarab ikki boshqa ish qiladi
/**
 * To'lovni yopadi. {@code dryRun} true bo'lsa bank chaqirilmaydi va
 * natija faqat hisoblanadi; bu holda {@code force} e'tiborga olinmaydi.
 * {@code force} true bo'lsa muddati o'tgan to'lov ham yopiladi, lekin
 * audit yozuvi boshqa turda chiqadi va hodisa chiqmaydi.
 */
SettlementResult settle(PaymentId id, boolean dryRun, boolean force);

// yaxshi: har bir metodning izohi qisqa, chunki har biri bitta ish qiladi
/** To'lovni bank bilan yopadi; muddati o'tgan to'lovni rad etadi. */
SettlementResult settle(PaymentId id);

/** Yopish natijasini bankka murojaat qilmasdan hisoblaydi. */
SettlementEstimate estimate(PaymentId id);

/** Muddati o'tgan to'lovni majburiy yopadi va buni auditga yozadi. */
SettlementResult settleOverdue(PaymentId id, OverrideReason reason);
```

Signalning sharti bor va uni esda tutish kerak: izoh faqat to'liq va tushunarli bo'lganda murakkablikning yaxshi o'lchovi bo'ladi. Metodni chaqirish uchun kerakli ma'lumotni bermaydigan yoki tushunarsiz yozilgan qisqa izoh interfeys sodda ekanini isbotlamaydi (shu yerda, 15.3). Shuning uchun tartib bitta yo'nalishda ishlaydi: avval hujjat 10.3 va 10.4 talab qilgan darajada to'liq yoziladi, keyin uzunligiga qaraladi. Hujjatni qisqartirish bilan boshlash signalni o'chiradi, muammoni esa qoldiradi.

## 10.12 Hujjatni kod kabi boshqarish: ega, kanoniklik, yangilik

Javadoc ni CI tekshiradi, repodagi markdown hujjatni esa hech kim tekshirmaydi va u shuning uchun eskiradi. Google ning javobi: hujjatga **kod bilan bir xil apparat** beriladi. Hujjat manba nazoratida turadi, o'z egasi bor, o'zgarishi review dan o'tadi, xatosi issue sifatida kuzatiladi va u hujjatlagan kod bilan bitta o'zgarishda yangilanadi. Google da wiki modelidan voz kechish sababi aniq edi: egasi yo'q hujjat eskirdi, yangi kelgan odam xato borligini ko'rdi lekin tuzatishga bilim yetmadi, tuzatishga qurbi bor odam esa hujjatni o'qimadi.

Amalda bu quyidagi qoidalarga aylanadi.

- **Har hujjatning egasi bor.** Egasiz hujjat eskiradi. Mavzu murakkab bo'lgan sari ega muhimroq: xushyor o'quvchi eskirgan joyni sezadi, lekin tuzatish uchun kerakli tarkibiy o'zgartirishni qila olmaydi.
- **Bir mavzuda bitta kanonik hujjat.** Raqobatlashadigan nusxalar asosiysiga qo'shiladi yoki eskirgan deb belgilanadi. Kanonik qilishning eng arzon usuli - hujjatni u tasvirlagan kod yonida, manba daraxti ichida saqlash: joy o'zi egalikni belgilaydi. Tashkilot bo'yicha umumiy ko'rsatma (ishga tushirish, ish oqimi) faqat hammaga tegishli ma'lumot uchun markazlashtiriladi; bitta servisning mahalliy qo'llanmasi markazga chiqmaydi.
- **Bitta hujjat bitta maqsad.** Reference, dizayn hujjati, tutorial va konseptual hujjat aralashtirilmaydi. Havolalar, tushuntirish va API ro'yxati qo'shilgan bitta uzun sahifa hech bir maqsadga xizmat qilmaydi. Reference to'liqlikni, konseptual hujjat esa tushunarlilikni tanlaydi: konseptual hujjat hamma chegara holatini qamramasligi normal, reference esa qamraydi.
- **Birinchi ikki paragraf kim, nima, qachon, qayerda va nega ga javob beradi.** Texnik hujjat tabiiy ravishda "qanday" dan boshlaydi; qolgan savollar aytilmasa o'quvchi hujjatni noto'g'ri ishlatadi. Sana hujjatda yoziladi (manba nazoratidagi faylda u o'zi bor), joyi esa ongli tanlanadi.
- **Yangilik sanasi va egasi hujjat boshida turadi.** Google hujjatlarga "freshness date" qo'yadi: oxirgi tekshiruv sanasi va egasi, hamda uzoq tegilmaganda eslatma yuboradigan metadata. Bu hujjatni vaqti-vaqti bilan ko'rib chiqishning eng arzon vositasi.
- **Keraksiz hujjat o'chiriladi yoki eskirgan deb belgilanadi.** Belgilash bilan birga yangi joyga havola beriladi. Egasi yo'q hujjatga "bu endi ishlamaydi" degan qator qo'shish ham hech narsa demaslikdan foydali: o'quvchi aks holda eskirgan matnni haqiqat deb oladi.
- **Tutorial da har foydalanuvchi qadami raqamlanadi.** Tizim javob sifatida bajargan ishlar raqamlanmaydi, atomar amallar bitta qadamga birlashtiriladi, taxminlar esa boshida oldindan shart sifatida yoziladi. Tutorialni yozishning eng yaxshi vaqti - jamoaga yangi kelgan payt, chunki shu paytda hech qanday bilim taxmin qilinmaydi va mavjud tutorialning xatolari ham shunda topiladi.

```text
docs/payment/README.md
<!-- ega: payments-team | oxirgi tekshiruv: 2026-03-14 -->

# To'lov modulini lokal ishga tushirish

Kimga: payments jamoasiga yangi qo'shilgan muhandis.
Nima: lokal mashinada to'lovni oxirigacha o'tkazish.
Oldindan shart: JDK 21, Docker, `infra-vpn` ulanishi.

1. Reponi klon qilib `./mvnw -pl payment -am install` ni bajaring.
2. `docker compose -f payment/compose.yaml up -d` bilan PostgreSQL va
   WireMock ni ko'taring.
3. `./mvnw -pl payment spring-boot:run` ni ishga tushiring.
   Ilova migratsiyani o'zi yurgizadi va 8080 portni egallaydi.
4. To'lovni tekshiring:
   curl -X POST localhost:8080/payments -d '{"amount":"10.00"}'
```

Hujjat review ning uch turi bor va ularning maqsadi boshqa-boshqa: **texnik review** aniqlik uchun (mavzu mutaxassisi, ko'pincha kod review ning o'zi ichida), **auditoriya review** tushunarlilik uchun (domenni bilmaydigan odam, masalan yangi kelgan yoki API foydalanuvchisi), **yozuv review** izchillik uchun. Bu chegaralar amalda aralashadi va bitta review ham yo'qdan afzal; hujjat muhandislik oqimiga bog'langan bo'lsa auditoriya review o'z-o'zidan sodir bo'ladi, chunki foydalanuvchi ishlamagan joyni xabar qiladi.

## 10.13 Amalda qo'llash

- [ ] Javadoc siyosatini yozib qo'ying: qaysi elementlarga majburiy, qaysilariga taqiqlangan (10.1 jadvali).
- [ ] Public API metodlarida `@param`, `@return`, `@throws` to'liqligini tekshirib, yarim to'ldirilganlarini tugating.
- [ ] Shartnomaga tranzaksiya, idempotentlik, thread-safety va yon ta'sir qatorlarini qo'shing.
- [ ] Javadoc dagi sinf nomlarini `{@link}` ga o'tkazib, havolalarni kompilyator tekshiradigan qiling.
- [ ] Barcha `@Deprecated` larga `@deprecated` tegi, almashtirish va o'chirish versiyasini qo'shing.
- [ ] Har bir public paketga `package-info.java` yozib, kirish nuqtalari va chegarani belgilang.
- [ ] `maven-javadoc-plugin` ni `doclint=all` va `failOnWarnings` bilan CI ga qo'shing.
- [ ] Javadoc dagi namuna kodlarni `{@snippet}` orqali testdagi faylga bog'lang.
- [ ] Shartnomasi uzun va shoxlangan metodlarni ro'yxatlab, har birini hujjatni qisqartirish emas, dizaynni bo'lish bilan tuzating (10.11).

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 56 - oshkor API elementlarining hammasiga hujjat izohi yozish
- Joshua Bloch, *Effective Java* 3rd, Item 74 - har bir metod tashlaydigan istisnoni hujjatlash
- Robert C. Martin, *Clean Code*, 4-bob ("Javadocs in Public APIs", "Javadocs in Nonpublic Code") - Javadoc qayerda foydali, qayerda shovqin
- [Oracle, How to Write Doc Comments](https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html) - birinchi gap qoidasi va teg tartibi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 10-bob ("Documentation Is Like Code", "Deprecating Documents") - hujjatning kod kabi manba nazoratida turishi, egasi bo'lishi, review dan o'tishi va issue bilan kuzatilishi; kanonik hujjat tanlash va takrorlarni deprecate qilish; yangilik sanasi va "oxirgi marta kim ko'rdi" qatori. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 10-bob ("Know Your Audience", "Documentation Types", "Documentation Reviews") - birlamchi auditoriyani aniqlash, izlovchi va qoqiluvchi farqi, hujjatni qisqa tutish, bitta hujjat bitta maqsad, reference ning to'liqligi va konseptual hujjatning tushunarliligi, hujjat review ning uch turi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 10-bob ("Function Comments", "Tutorials", "Documentation Philosophy") - funksiya izohini fe'l bilan boshlash va `Returns:`/`Throws:` shablonlarini zarur deb topmaslik, tutorialda foydalanuvchi qadamlarini raqamlash va oldindan shartlarni boshida aytish, hujjatning kim/nima/qachon/qayerda/nega ga javob berishi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 3-bob ("Establishing Canonical Sources of Information") - kanonik ko'rsatma faqat butun tashkilotga tegishli ma'lumot uchun va murakkab mavzuda aniq egasi bo'lishi shart. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 15-bob ("Deprecation Warnings") - ogohlantirishdan bajarilishi mumkinlik va o'z vaqtidalik talab qilinishi, tranzitiv ogohlantirishlarning alert fatigue ga olib kelishi, keng ogohlantirish faqat majburiy deprecation da yoqilishi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press,
  2018, 15.3 - "Red Flag: Hard to Describe": izoh sodda va to'liq bo'lishi
  kerakligi, izohning murakkablik o'lchovi sifatida ishlashi, chuqur va
  yuzaki metodni interfeys izohi bilan solishtirish, hamda signalning
  faqat to'liq va tushunarli izohda ishlashi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, A-ilova (1183-bet) - `{@inheritDoc}` ning ota sinfdan izohni voris olishi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, A-ilova (1184-bet) - `{@value}` ning konstanta qiymatini hujjatga qo'yishi va maydonning `static` bo'lishi sharti
- Joshua Bloch, *Effective Java* 3rd, Item 19 (93-bet) - self-use hujjatining `@implSpec` tegi bilan "Implementation Requirements" bo'limida yozilishi
- Joshua Bloch, *Effective Java* 3rd, Item 56 (255-bet) - `@param` va `@return` dan keyingi matnning ot iborasi, `@throws` dan keyingi matnning "agar" bilan boshlanadigan shart bo'lishi va ularning nuqta bilan tugamasligi
- Joshua Bloch, *Effective Java* 3rd, Item 56 (257-bet) - bir sinfda ikki a'zo yoki konstruktorning bir xil xulosa tavsifiga ega bo'lmasligi (ayniqsa overload larda); xulosa tavsifining birinchi nuqtada tugashi va qisqartmani `{@literal}` bilan o'rash
- Joshua Bloch, *Effective Java* 3rd, Item 56 (258-bet) - generik tur va metodda barcha tur parametrlarining (`@param <K>`) hujjatlanishi
- Joshua Bloch, *Effective Java* 3rd, Item 74 (304-bet) - tekshiriladigan istisnolarning har birini alohida e'lon qilish (`throws Exception` yozmaslik, yagona istisno `main`) va tekshirilmaydigan istisnoga `throws` kalit so'zini qo'ymasdan faqat `@throws` tegini yozish
- Joshua Bloch, *Effective Java* 3rd, Item 87 (350-bet) - `writeObject` `private` bo'lsa ham hujjat izohi olishi, `@serialData` va `@serial` teglarining Javadoc ni seriyalangan shakl sahifasiga joylashi
- ESLATMA: `refund` kod misoli va teglar jadvalining "Qachon ishlatiladi" ustuni korpus qo'shimchasi; kitoblar teglarning ma'nosini beradi, qachon ishlatish tanlovini korpus yozgan

---

[&larr; 9. Yomon izohlar katalogi](09-yomon-izohlar-katalogi.md) · [Mundarija](README.md) · [11. Vertikal formatlash &rarr;](11-vertikal-formatlash.md)
