<!-- doc: clean-code | chapter: 9 | part: III. Izoh va hujjat -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 9. Yomon izohlar katalogi (Comments: The Bad Ones)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [9.1 G'o'ldirash (mumbling)](#91-goldirash-mumbling)
- [9.2 Ortiqcha izoh: kodni so'zma-so'z takrorlash](#92-ortiqcha-izoh-kodni-sozma-soz-takrorlash)
- [9.3 Chalg'ituvchi izoh](#93-chalgituvchi-izoh)
- [9.4 Majburiy izoh: har bir maydonga Javadoc](#94-majburiy-izoh-har-bir-maydonga-javadoc)
- [9.5 Jurnal izohlari va mualliflik imzolari](#95-jurnal-izohlari-va-mualliflik-imzolari)
- [9.6 Shovqin izohlar](#96-shovqin-izohlar)
- [9.7 Pozitsiya belgilari va qavs yopilishi izohlari](#97-pozitsiya-belgilari-va-qavs-yopilishi-izohlari)
- [9.8 Izohga olingan kod](#98-izohga-olingan-kod)
- [9.9 Nolokal ma'lumot va ortiqcha ma'lumot](#99-nolokal-malumot-va-ortiqcha-malumot)
- [9.10 Noravshan bog'liqlik](#910-noravshan-bogliqlik)
- [9.11 Funksiya sarlavhasi izohi](#911-funksiya-sarlavhasi-izohi)
- [9.12 Izohni o'chirish qarori: tekshiruv ro'yxati](#912-izohni-ochirish-qarori-tekshiruv-royxati)
- [9.13 Izoh emas, nom: funksiya yoki o'zgaruvchi bilan aytish](#913-izoh-emas-nom-funksiya-yoki-ozgaruvchi-bilan-aytish)
- [9.14 Qo'rqinchli shovqin: Javadoc shaklidagi ortiqcha izoh, HTML va ichki koddagi Javadoc](#914-qorqinchli-shovqin-javadoc-shaklidagi-ortiqcha-izoh-html-va-ichki-koddagi-javadoc)
- [9.15 Amalda qo'llash](#915-amalda-qollash)

</details>


Izohlarning katta qismi shu bobdagi toifalarga tushadi va ularning hammasi o'chirilishi kerak. Katalog shaklida berilgani ataylab: review paytida izohni toifaga solib, qaror bir necha soniyada chiqadi.

## 9.1 G'o'ldirash (mumbling)

Izoh shoshilib yozilsa, u muallifga tushunarli, o'quvchiga esa yo'q bo'ladi. Natija: o'quvchi izohni tushunish uchun boshqa kodni o'qishga majbur, ya'ni izoh ish qilmaydi, ish qo'shadi.

```java
// yomon: "defaults" nima, qaysi fayl, nega e'tiborsiz qoldirildi?
try {
    loadProperties();
} catch (IOException e) {
    // defaults yuklandi
}

// yaxshi: izoh emas, kodning o'zi aytadi
try {
    this.properties = loadPropertiesFile(CONFIG_PATH);
} catch (NoSuchFileException e) {
    this.properties = Properties.defaults();   // fayl yo'q bo'lishi normal holat
}
```

## 9.2 Ortiqcha izoh: kodni so'zma-so'z takrorlash

Kodni takrorlagan izoh o'qish vaqtini oshiradi va ma'lumot bermaydi. Bundan tashqari, u kod o'zgarganda yangilanmaydi va 9.3 ga aylanadi.

```java
// yomon
// buyurtmani saqlaydi
orderRepository.save(order);

// i ni bittaga oshiradi
i++;

// yaxshi: izoh yo'q
orderRepository.save(order);
```

## 9.3 Chalg'ituvchi izoh

Eng qimmat izoh turi: u yolg'on gapiradi va o'quvchi ishonadi. Odatda u bir vaqtlar to'g'ri bo'lgan, keyin kod o'zgargan va izoh qolgan.

```java
// yomon: izoh "kutadi" deydi, kod esa darhol qaytadi
// Thread shu yerda flag true bo'lguncha kutadi.
public void waitForClose() {
    if (!closed) {
        return;        // kutmaydi!
    }
}
```

Chalg'ituvchi izohni topish usuli: review paytida har bir izohni kod bilan taqqoslash. Avtomatik usuli yo'q, shuning uchun izohlar soni kam bo'lishi afzal.

## 9.4 Majburiy izoh: har bir maydonga Javadoc

"Har bir metod Javadoc olishi kerak" qoidasi foydadan ko'ra zarar keltiradi: u shovqin generatsiya qiladi, mazmunsiz `@param` qatorlari paydo bo'ladi va haqiqiy hujjat ularning ichida ko'rinmay qoladi.

```java
// yomon: mazmunsiz, majburiyat uchun yozilgan
/**
 * @param order buyurtma
 * @param now hozirgi vaqt
 * @return natija
 */
public Result process(Order order, Instant now) { ... }
```

To'g'ri siyosat: Javadoc faqat public API va noaniq shartnomalar uchun ([10-bob](10-javadoc-va-api-hujjati.md)), ichki metodlar uchun esa nom va imzo yetarli.

## 9.5 Jurnal izohlari va mualliflik imzolari

Fayl boshida o'zgarish tarixi yuritish `git` dan oldingi davr qoldig'i. Hozir u faqat shovqin, chunki tarix allaqachon versiya nazoratida bor va u aniqroq.

```java
// yomon: git log buni yaxshiroq aytadi
/**
 * 2019-04-11: Dilshod - birinchi versiya
 * 2020-01-02: Aziza - QQS hisobini tuzatdi
 * 2021-07-19: noma'lum - refaktoring
 */

// yomon: egalik git blame va CODEOWNERS da
/** @author Dilshod */
```

`@author` tegining yashirin zarari bor: u kodni "shaxsiy mulk" ga aylantiradi va jamoaviy egalikni susaytiradi (47.1).

## 9.6 Shovqin izohlar

Hech qanday ma'lumot bermaydigan, shunchaki bo'sh joyni to'ldiradigan izohlar.

```java
// yomon: hammasi shovqin
/** Default konstruktor. */
protected AnnualDateRule() { }

/** Oy kuni. */
private int dayOfMonth;

// Ro'yxatni qaytaradi
public List<Order> getOrders() { return orders; }
```

Bunday izohlar shu darajada ko'p bo'lsa, o'quvchi izohlarni butunlay o'qishni to'xtatadi va natijada 8.4 dagi foydali izohlar ham e'tibordan chetda qoladi.

## 9.7 Pozitsiya belgilari va qavs yopilishi izohlari

Bo'lim ajratuvchi banner va yopiladigan qavs yonidagi izoh ikkisi ham tuzilishni izoh bilan almashtirishga urinish. Ikkisi ham bir xil haqiqiy muammoni ko'rsatadi: blok juda uzun (4.3).

```java
// yomon: banner bo'lim izohi
//////////////////////////////////////////
// Validatsiya
//////////////////////////////////////////

// yomon: qavs yopilishi izohi - sikl juda uzun
        }   // while
    }       // try
}           // main
```

Yechim: bannerni metod nomiga, uzun blokni esa kichik metodlarga aylantirish.

## 9.8 Izohga olingan kod

Izohga olingan kod kod bazasidagi eng zararli artefakt: u hech kim o'chirishga jur'at qilmaydigan o'lik matn, chunki "balki kerak bo'ladi". Versiya nazorati bor kod bazasida bu argument o'z kuchini yo'qotgan.

```java
// yomon
// this.bytePos = writeBytes(pngIdBytes, 0);
// hdrPos = bytePos;
writeHeader();
// hdrBytes = ...
writeResolution();
```

Qoida: izohga olingan kod darhol o'chiriladi. Kerak bo'lsa `git log -S` yoki `git revert` bilan topiladi. Agar vaqtinchalik o'chirish kerak bo'lsa, feature flag ishlatiladi (41.5), izoh emas.

## 9.9 Nolokal ma'lumot va ortiqcha ma'lumot

**Nolokal** izoh - shu kodga tegishli bo'lmagan ma'lumotni aytadi (masalan metod izohida butun tizim konfiguratsiyasini tushuntiradi). Muammo: kod o'zgarmasa ham izoh eskiradi, chunki u boshqa joyga tegishli.

**Ortiqcha ma'lumot** - izohda tarixiy muhokama, RFC ning to'liq matni, akademik tushuntirish. Izoh yozish uchun emas, o'qish uchun mo'ljallangan: uzun matn o'qilmaydi.

```java
// yomon: nolokal - bu metodga tegishli emas
/**
 * Port: standart 8080. Konfiguratsiyani application.yml da o'zgartirish mumkin.
 * Shuningdek ingress va service portini ham moslash kerak...
 */
public void handle(Request request) { ... }

// yaxshi: havola bering, ko'chirmang
// Protokol tafsilotlari: docs/settlement-protocol.md
```

## 9.10 Noravshan bog'liqlik

Izoh kodni tushuntirishi kerak, lekin ba'zan izohning o'zi tushuntirishga muhtoj bo'lib qoladi: u qaysi qatorga, qaysi qiymatga tegishli ekani ko'rinmaydi.

```java
// yomon: "filter bytes" nima, nega +1?
// filter baytlari pikselga qo'shiladi
this.pngBytes = new byte[((width + 1) * height * 3) + 200];

// yaxshi: har bir had nomlangan
int filterByteCountPerRow = 1;
int bytesPerPixel = 3;
int headerAndTrailerBytes = 200;
this.pngBytes = new byte[(width + filterByteCountPerRow) * height * bytesPerPixel
        + headerAndTrailerBytes];
```

## 9.11 Funksiya sarlavhasi izohi

Qisqa, bitta ish qiladigan va yaxshi nomlangan funksiyaga sarlavha izohi kerak emas. Agar sarlavha izohi yozishga ehtiyoj tug'ilsa, u funksiya nomini aniqlashtirish zarurligini bildiradi (4.6).

```java
// yomon
// Qoldiqni tekshiradi va yetarli bo'lsa rezerv qiladi
public void doIt(Order o) { ... }

// yaxshi: izoh nomga ko'chdi
public void reserveStockIfAvailable(Order order) { ... }
```

## 9.12 Izohni o'chirish qarori: tekshiruv ro'yxati

Review paytida izoh uchun ketma-ket beriladigan savollar. Birinchi "yo'q" javobi izohni o'chirish qaroriga olib keladi.

| Savol | "Yo'q" bo'lsa |
|---|---|
| Izoh kodda ko'rinmaydigan ma'lumot beradimi? | o'chirish |
| Uni nomga yoki turga ko'chirib bo'lmaydimi? | ko'chirish, izohni o'chirish |
| Izoh bugun ham to'g'rimi? | tuzatish yoki o'chirish |
| Izohni o'quvchi tushunadimi? | qayta yozish yoki o'chirish |
| Kod o'zgarganda izoh yangilanadimi? | o'chirish (saqlanmaydi) |
| Izoh kodga tegishlimi (nolokal emasmi)? | hujjatga ko'chirish |
| Izohda ticket va shart bormi (`TODO` uchun)? | qo'shish yoki o'chirish |
| Izohga olingan kod emasmi? | darhol o'chirish |

## 9.13 Izoh emas, nom: funksiya yoki o'zgaruvchi bilan aytish

Izoh yozish o'rniga nom berish mumkin bo'lgan holat alohida turkum, chunki u boshqa yomon izohlardan farq qiladi: bu yerda izoh noto'g'ri emas, u shunchaki **keraksiz**, va uni keraksiz qilish qo'lingizda.

Kitobdagi misol aynan shunday ko'rinadi:

```java
// does the module from the global list <mod> depend on the
// subsystem we are part of?
if (smodule.getDependSubsystems().contains(subSysMod.getSubSystem())) { ... }
```

Izohni o'chirish uchun uni tarjima qilish kerak emas, ifodani nomlash kerak:

```java
ArrayList moduleDependees = smodule.getDependSubsystems();
String ourSubSystem = subSysMod.getSubSystem();
if (moduleDependees.contains(ourSubSystem)) { ... }
```

Natijada savol kodning o'zida javob topadi va izoh ortiqcha bo'lib qoladi. Kitobning kuzatuvi ham shunday: muallif izohni oldin yozgan bo'lishi mumkin, lekin keyin kodni refaktor qilib izohni olib tashlashi kerak edi.

Amalda bu ikki harakatdan biri bilan bajariladi: uzun shartni nomlangan lokal o'zgaruvchiga chiqarish, yoki uni nomlangan predikat metodga ajratish.

```java
// IZOH KERAK: shart nima qilayotgani ko'rinmaydi
// Mijoz oxirgi 90 kunda to'lov qilgan va bloklanmagan bo'lsa
if (c.getLastPaymentAt() != null
        && c.getLastPaymentAt().isAfter(LocalDate.now().minusDays(90))
        && !c.isBlocked()) { ... }

// IZOH KERAK EMAS: shart o'zini aytadi
if (customer.isActivePayer()) { ... }
```

Qoida sodda: izoh yozishdan oldin "buni nom bilan aytib bera olamanmi" degan savol beriladi. Javob "ha" bo'lsa, izoh emas, nom yoziladi.

## 9.14 Qo'rqinchli shovqin: Javadoc shaklidagi ortiqcha izoh, HTML va ichki koddagi Javadoc

Javadoc shakli izohni yaxshi qilmaydi. Kitob buni "qo'rqinchli shovqin" (scary noise) deb ataydi va mashhur ochiq kutubxonadan olingan misolni keltiradi:

```java
/** The name. */
private String name;
/** The version. */
private String version;
/** The licenceName. */
private String licenceName;
/** The version. */
private String info;
```

Bu izohlar hech qanday maqsadga xizmat qilmaydi, ular hujjat berish istagidan tug'ilgan ortiqcha takrorlar. Lekin eng muhim xulosa misolni **diqqat bilan** o'qiganda chiqadi: oxirgi maydon `info`, izohi esa "The version", ya'ni nusxa-ko'chirish xatosi. Kitobning savoli shu yerda: izoh yozilayotganda (yoki ko'chirilayotganda) muallif e'tibor bermasa, o'quvchi nega undan foyda ko'rishi kerak?

Review uchun bu foydali signal: bir xil shakldagi maydon izohlari ketma-ket turgan joy nusxa xatosining eng ehtimolli joyi. Shu bilan birga ikkita qoida kelib chiqadi.

Birinchi: izoh ichida HTML yozish. Kitob buni qattiq rad etadi, chunki HTML izohni aynan eng ko'p o'qiladigan joyda, muharrir va IDE da, o'qishga qiyin qiladi. Izohni veb sahifaga chiqaradigan asbob bo'lsa (Javadoc kabi), HTML qo'yish **shu asbobning** vazifasi, dasturchining emas.

Ikkinchi: Javadoc ni ommaviy bo'lmagan kodga yozish. Javadoc ommaviy API uchun foydali, lekin tashqi iste'mol uchun mo'ljallanmagan kod uchun u zararli: tizim ichidagi sinf va funksiyalar uchun javadoc sahifasi yasash odatda foyda bermaydi, javadoc shaklining qo'shimcha rasmiyatchiligi esa chalg'ituvchi yuk bo'lib qoladi.

```java
// YOMON: ichki yordamchi sinfga javadoc rasmiyatchiligi
/**
 * <p>Hisob-kitob yordamchisi.</p>
 * <pre>
 * Usage:
 *   Calculator.add(a, b)
 * </pre>
 * @param a birinchi son
 * @param b ikkinchi son
 * @return yig'indi
 */
static int add(int a, int b) { return a + b; }

// YAXSHI: ichki kod uchun izoh ham, HTML ham kerak emas
static int add(int a, int b) { return a + b; }
```

## 9.15 Amalda qo'llash

- [ ] Izohga olingan kodni butun repoda grep qilib (`^\s*//\s*\w+.*[;{}]`), hammasini o'chiring.
- [ ] `@author` va fayl boshidagi o'zgarish jurnallarini olib tashlab, egalikni CODEOWNERS ga ko'chiring.
- [ ] Banner va qavs yopilishi izohlarini topib, ular belgilagan bo'limlarni metodlarga ajratib bering.
- [ ] Mazmunsiz Javadoc bloklarini (`@param order buyurtma`) o'chirib, Javadoc siyosatini public API bilan cheklang.
- [ ] Har bir izohni kod bilan taqqoslab, chalg'ituvchilarini tuzating yoki o'chiring.
- [ ] 9.12 jadvalidagi savollar ro'yxatini review checklistiga kiritib, izoh bo'yicha qarorni standartlashtiring.
- [ ] Uzun tushuntirish izohlarini `docs/` dagi faylga ko'chirib, kodda faqat havola qoldiring.
- [ ] Checkstyle yoki custom qoida bilan `FIXME` ni CI da bloklang.
- [ ] Bobdagi har bir izohni oling va "buni nom bilan aytib bera olamanmi" savolini bering; javob "ha" bo'lsa, izohni o'chirib shartni nomlangan o'zgaruvchiga yoki predikat metodga chiqaring.
- [ ] Ketma-ket turgan bir xil shakldagi maydon izohlarini o'qib chiqing: nusxa-ko'chirish xatosi aynan shu joyda bo'ladi.
- [ ] Izoh ichidagi HTML teglarini olib tashlang va ommaviy bo'lmagan sinflardagi Javadoc bloklarini oddiy izohga yoki nomga aylantiring.

## Manbalar

- Robert C. Martin, *Clean Code*, 4-bob, "Don't Use a Comment When You Can Use a Function or a Variable"
- Robert C. Martin, *Clean Code*, 4-bob, "Scary Noise", "HTML Comments", "Javadocs in Nonpublic Code" - Javadoc shaklidagi ortiqcha izoh, nusxa xatosi, izohdagi HTML va ichki koddagi Javadoc

---

[&larr; 8. Izoh qoidalari: yaxshi izohlar](08-izoh-qoidalari-yaxshi-izohlar.md) · [Mundarija](README.md) · [10. Javadoc va API hujjati &rarr;](10-javadoc-va-api-hujjati.md)
