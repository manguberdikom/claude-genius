<!-- doc: clean-code | chapter: 10 | part: III. Izoh va hujjat -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 10. Javadoc va API hujjati (Javadoc and API Documentation)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [10.11 Amalda qo'llash](#1011-amalda-qollash)

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

## 10.3 `@param`, `@return`, `@throws` to'liqligi

Uchta teg to'liq bo'lishi kerak yoki umuman bo'lmasligi kerak - yarim to'ldirilgan Javadoc eng yomon holat, chunki o'quvchi qolganini ham yo'q deb o'ylaydi.

Har bir teg uchun aniq talab bor. `@param` - qiymatning ma'nosi va chegarasi (`null` bo'lishi mumkinmi, diapazon qanday). `@return` - nima qaytadi va bo'sh holat qanday ifodalanadi. `@throws` - **har bir** tekshiriladigan istisno, va unchecked istisnolardan chaqiruvchi uchun ma'noli bo'lganlari.

```java
// yomon: tur nomini takrorlaydi, ma'lumot bermaydi
/** @param amount summa */

// yaxshi: ma'no, birlik, chegara
/** @param amount qaytarilayotgan summa; musbat va to'langan summadan oshmasligi kerak */
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

## 10.11 Amalda qo'llash

- [ ] Javadoc siyosatini yozib qo'ying: qaysi elementlarga majburiy, qaysilariga taqiqlangan (10.1 jadvali).
- [ ] Public API metodlarida `@param`, `@return`, `@throws` to'liqligini tekshirib, yarim to'ldirilganlarini tugating.
- [ ] Shartnomaga tranzaksiya, idempotentlik, thread-safety va yon ta'sir qatorlarini qo'shing.
- [ ] Javadoc dagi sinf nomlarini `{@link}` ga o'tkazib, havolalarni kompilyator tekshiradigan qiling.
- [ ] Barcha `@Deprecated` larga `@deprecated` tegi, almashtirish va o'chirish versiyasini qo'shing.
- [ ] Har bir public paketga `package-info.java` yozib, kirish nuqtalari va chegarani belgilang.
- [ ] `maven-javadoc-plugin` ni `doclint=all` va `failOnWarnings` bilan CI ga qo'shing.
- [ ] Javadoc dagi namuna kodlarni `{@snippet}` orqali testdagi faylga bog'lang.

---

[&larr; 9. Yomon izohlar katalogi](09-yomon-izohlar-katalogi.md) · [Mundarija](README.md) · [11. Vertikal formatlash &rarr;](11-vertikal-formatlash.md)
