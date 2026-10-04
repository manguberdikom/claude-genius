<!-- doc: sonarqube | chapter: 17 | part: V. Sonar o'tadigan test -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 17. Sonar talablarini qondiradigan test yozish (Writing Tests That Satisfy Sonar)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [17.1 Test nimani qamrashi kerak: ishlab chiqarish kodining har bir yo'li](#171-test-nimani-qamrashi-kerak-ishlab-chiqarish-kodining-har-bir-yoli)
- [17.2 Testni qamrov uchun emas, xatti-harakat uchun yozish tamoyili](#172-testni-qamrov-uchun-emas-xatti-harakat-uchun-yozish-tamoyili)
- [17.3 Bitta test bitta xatti-harakatni tekshirsin](#173-bitta-test-bitta-xatti-harakatni-tekshirsin)
- [17.4 Assertion siz test: Sonar uni aniqlaydi va u foydasiz](#174-assertion-siz-test-sonar-uni-aniqlaydi-va-u-foydasiz)
- [17.5 Istisnoni tekshirish: `assertThrows` va xabarni ham tekshirish](#175-istisnoni-tekshirish-assertthrows-va-xabarni-ham-tekshirish)
- [17.6 Parametrik test bilan ko'p holatni kam kod bilan qoplash](#176-parametrik-test-bilan-kop-holatni-kam-kod-bilan-qoplash)
- [17.7 Mock ni o'rinli ishlatish: nimani mock qilish, nimani qilmaslik](#177-mock-ni-orinli-ishlatish-nimani-mock-qilish-nimani-qilmaslik)
- [17.8 Spring kontekstiga bog'liq testni kamaytirish va tezlikni saqlash](#178-spring-kontekstiga-bogliq-testni-kamaytirish-va-tezlikni-saqlash)
- [17.9 Vaqt, tasodif va tashqi holatga bog'liq kodni sinovga ochiq qilish](#179-vaqt-tasodif-va-tashqi-holatga-bogliq-kodni-sinovga-ochiq-qilish)
- [17.10 Testni o'qiydigan qilib yozish: nom, tuzilish, ma'lumot](#1710-testni-oqiydigan-qilib-yozish-nom-tuzilish-malumot)
- [17.11 Qamrovni oshirish uchun yozilgan bo'sh testlarni tanib olish](#1711-qamrovni-oshirish-uchun-yozilgan-bosh-testlarni-tanib-olish)
- [17.12 Amalda qo'llash](#1712-amalda-qollash)

</details>


Sonar testni ikki tomondan ko'radi. Birinchi tomon: test ishlab chiqarish kodining qancha qatorini va qancha shoxini ishga tushirdi, ya'ni coverage raqami. Ikkinchi tomon: testning o'zi ham tahlil qilinadigan kod, unda ham issue chiqadi. Shu ikki tomonni bir vaqtda qondirmasa, quality gate yoki coverage shartida yoki test fayllaridagi issue sababli yiqiladi. Bu bobda har bir mavzu ayni shu ikki tomon bilan bog'lanadi, test yozish asoslari esa [testlash qo'llanmasiga](../testing/README.md) qoldiriladi.

## 17.1 Test nimani qamrashi kerak: ishlab chiqarish kodining har bir yo'li

Sonar coverage ni o'zi o'lchamaydi, uni JaCoCo hisobotidan oladi. JaCoCo esa ikki narsani sanaydi: bajarilgan qatorlar va bajarilgan shoxlar. Shox degani `if`, `else`, `&&`, `||`, `?:`, `switch` tarmoqlari va `catch` bloklari. Shuning uchun "qator qamrovi 100%" bo'lib, "shox qamrovi 60%" bo'lishi juda oson. Quality gate odatda `New Code` ustida coverage talab qiladi, ya'ni faqat o'zgargan qatorlar hisoblanadi.

Quyidagi metod bitta test bilan 100% line coverage beradi, lekin shoxlarning yarmi ishga tushmaydi.

```java
// To'lov komissiyasini hisoblaydi. Uchta shart, demak kamida uchta shox juftligi.
public BigDecimal komissiya(Tolov tolov) {
    BigDecimal stavka = new BigDecimal("0.02");
    if (tolov.summa().compareTo(new BigDecimal("1000000")) > 0) {
        stavka = new BigDecimal("0.01"); // yirik to'lovga chegirma
    }
    if (tolov.valyuta() != Valyuta.UZS) {
        stavka = stavka.add(new BigDecimal("0.005")); // valyuta ustamasi
    }
    return tolov.summa().multiply(stavka);
}
```

Bu metodni qoplash uchun kamida to'rt holat kerak: kichik UZS, yirik UZS, kichik valyuta, yirik valyuta. Qoida sodda: har bir `if` ikki yo'l, har bir `&&` yana bitta shox, har bir `catch` alohida yo'l. Agar shoxni testda ataylab yurgizib bo'lmasa, bu kodning o'zida o'lik shart borligini ko'rsatadi va uni olib tashlash kerak, test yozib o'tirish emas.

```java
@Test
void yirikValyutaTolovigaIkkiOzgarishHamQollanadi() {
    Tolov tolov = new Tolov(new BigDecimal("2000000"), Valyuta.USD);
    // 0.01 chegirma + 0.005 ustama = 0.015 stavka
    assertEquals(new BigDecimal("30000.000"), servis.komissiya(tolov));
}
```

## 17.2 Testni qamrov uchun emas, xatti-harakat uchun yozish tamoyili

Coverage raqami oson aldanadi. Metodni chaqirib, natijaga qaramaslik ham qamrov beradi. Sonar bu holatni to'liq ushlay olmaydi, chunki u mantiqni tushunmaydi. Shu sababli coverage raqamiga ishonib, assertion ni yengil qilish quality gate ni o'tkazadi, ammo xatoni o'tkazib yuboradi. Bu hujjat boshida aytilgan halol gapning amaliy ko'rinishi: 100% coverage sifatni kafolatlamaydi.

Ishonchli mezon bitta. Har bir test uchun o'zingdan so'ra: ishlab chiqarish kodining mantiqini buzsam, bu test qizil bo'ladimi. Agar yo'q bo'lsa, u test emas, u faqat qamrov yig'adigan chaqiruv.

```java
// Yomon: qamrov bor, lekin mantiq buzilsa ham yashil qoladi.
@Test
void hisobotYaratiladi() {
    servis.hisobotYarat(2025, 10); // natija tekshirilmaydi
}

// Sonar o'tadigan va foydali: kutilgan xatti-harakat qayd etilgan.
@Test
void oyHisobotidaFaqatShuOyningBuyurtmalariBoladi() {
    Hisobot h = servis.hisobotYarat(2025, 10);
    assertEquals(2, h.qatorlar().size());
    assertEquals(new BigDecimal("450000"), h.jamiSumma());
}
```

## 17.3 Bitta test bitta xatti-harakatni tekshirsin

Sonar test metodining ichidagi cognitive complexity ni ham o'lchaydi, chunki `java:S3776` qoidasi fayl turiga qarab yumshamaydi. Ichida besh marta `if` va ikki marta tsikl bo'lgan test metodi shu qoida bilan issue oladi. Bundan tashqari bir metodda o'nta assertion bo'lsa, birinchi assertion yiqilganda qolgani ishga tushmaydi va siz nima buzilganini bilmaysiz.

Amaliy natija: tsikl va shart test ichida bo'lmasin, ular parametrik testga chiqadi. Bitta metodda bitta holat tekshiriladi, holatlar soni ko'p bo'lsa metodlar soni ko'payadi, murakkablik emas.

```java
// Yomon: bitta metodda uchta mustaqil qoida, ichida shart bor.
@Test
void omborQoldigiTekshiruvi() {
    for (int i = 0; i < 3; i++) {
        Mahsulot m = servis.topish(i);
        if (m.qoldiq() > 0) {
            assertTrue(m.sotuvdaMi());
        } else {
            assertFalse(m.sotuvdaMi());
        }
    }
}
```

```java
// Arxitektor yondashuvi: holat parametrga, shart yo'q, murakkablik past.
@ParameterizedTest
@CsvSource({"5, true", "1, true", "0, false"})
void qoldiqSotuvHolatiniBelgilaydi(int qoldiq, boolean sotuvda) {
    Mahsulot m = new Mahsulot("SKU-1", qoldiq);
    assertEquals(sotuvda, m.sotuvdaMi());
}
```

## 17.4 Assertion siz test: Sonar uni aniqlaydi va u foydasiz

Bu yerda aniq qoidalar bor. `java:S2699` assertion siz test metodini belgilaydi. `java:S2187` ichida hech qanday test metodi yo'q, ammo nomi `Test` bilan tugagan sinfni belgilaydi. Ikkisi ham Bug yoki Code Smell sifatida chiqadi va yangi kodda paydo bo'lsa quality gate ni yiqitadi.

Muhim nozik joy: Sonar assertion ni kutubxona ro'yxati bo'yicha taniydi. JUnit `Assertions`, AssertJ `assertThat`, Mockito `verify` va `Hamcrest` taniladi. Agar siz o'z yordamchi metodingiz ichiga assertion ni yashirsangiz, Sonar uni ko'rmasligi mumkin va noto'g'ri issue chiqadi. Yechim: yordamchi metodni testdan tashqariga olmaslik yoki uni AssertJ `SoftAssertions` bilan ochiq yozish.

```java
// Sonar uchun ham, odam uchun ham ravshan: assertion test metodining ichida.
@Test
void bekorQilinganBuyurtmaQoldiqniQaytaradi() {
    Buyurtma b = servis.yarat("SKU-1", 3);
    servis.bekorQil(b.id());
    assertThat(ombor.qoldiq("SKU-1")).isEqualTo(10);
    assertThat(servis.topish(b.id()).holat()).isEqualTo(Holat.BEKOR);
}
```

Yana bir tuzoq: `@Disabled` bilan o'chirilgan test. `java:S1607` uni issue qiladi va shu test qamrovga ham hissa qo'shmaydi. O'chirilgan test ikki yo'ldan birini tanlashi kerak: tuzatiladi yoki o'chiriladi.

## 17.5 Istisnoni tekshirish: `assertThrows` va xabarni ham tekshirish

`catch` bloki JaCoCo uchun alohida yo'l. Agar istisno yo'li testda hech qachon yurmasa, shu qatorlar qizil qoladi va ular ko'pincha eng xavfli qatorlar bo'ladi. Shuning uchun har bir ataylab tashlanadigan istisno uchun test bo'lishi kerak.

`java:S5778` qoidasi muhim: `assertThrows` lambdasi ichida faqat bitta tekshiriladigan chaqiruv bo'lsin. Aks holda istisno qaysi chaqiruvdan kelganini bilmaysiz.

```java
// Yomon: lambda ichida ikki chaqiruv, S5778 ishga tushadi.
assertThrows(QoldiqYetarsiz.class, () -> {
    servis.yarat("SKU-1", 100);
    servis.tasdiqla("SKU-1");
});
```

```java
// Sonar o'tadigan variant: bitta chaqiruv, tur va xabar tekshiriladi.
@Test
void qoldiqdanOshiqBuyurtmaIstisnoTashlaydi() {
    Buyurtma b = servis.yarat("SKU-1", 100); // tayyorgarlik lambdadan tashqarida
    QoldiqYetarsiz x = assertThrows(QoldiqYetarsiz.class, () -> servis.tasdiqla(b.id()));
    assertEquals("SKU-1 uchun qoldiq yetarsiz: so'rov 100, mavjud 10", x.getMessage());
    assertEquals("SKU-1", x.sku()); // tipli maydon xabardan ishonchliroq
}
```

Xabarni tekshirish ikki foyda beradi. Birinchidan, xato matnini yaratuvchi `String.format` qatori ham qamrovga kiradi. Ikkinchidan, noto'g'ri sababdan kelgan bir xil turdagi istisno testni o'tkazib yubormaydi.

## 17.6 Parametrik test bilan ko'p holatni kam kod bilan qoplash

Shox qamrovini oshirishning eng arzon yo'li parametrik test. Nusxa ko'chirilgan test metodlari esa `java:S4144` ("metodlar bir xil amalni bajarmasligi kerak") va duplication o'lchovi bilan muammo chiqaradi. Quality gate da `Duplicated Lines on New Code` sharti bo'lsa, nusxa ko'chirilgan beshta test metodi gate ni yiqitishi mumkin.

```java
@ParameterizedTest(name = "{0} summa {1} valyutada komissiya {2}")
@CsvSource({
    "kichik UZS,    500000,  UZS, 10000.00",
    "yirik UZS,    2000000,  UZS, 20000.00",
    "kichik valyuta, 500000, USD, 12500.000",
    "yirik valyuta, 2000000, USD, 30000.000"
})
void komissiyaStavkasiShartlarGaMosKelishi(String izoh, BigDecimal summa,
                                           Valyuta valyuta, BigDecimal kutilgan) {
    assertEquals(kutilgan, servis.komissiya(new Tolov(summa, valyuta)));
}
```

Chegaraviy qiymatlarni alohida yozish kerak, chunki `>` va `>=` farqi aynan chegarada ko'rinadi. `1000000` qiymati o'zi, undan bitta kichik va bitta katta qiymat uchta qator bilan beriladi. Null va bo'sh qiymat uchun `@NullAndEmptySource` ishlatiladi, shunda `if (x == null)` shoxi ham qoplanadi.

## 17.7 Mock ni o'rinli ishlatish: nimani mock qilish, nimani qilmaslik

Mock coverage ga qarshi ishlashi mumkin. Agar siz tekshirmoqchi bo'lgan mantiqni o'zini mock qilsangiz, haqiqiy kod ishga tushmaydi va qamrov pastda qoladi. Shu sababli mock chizig'i aniq: tashqi chegaradan tashqaridagi narsa mock qilinadi, domen mantiqi mock qilinmaydi.

```java
// Yomon: hisoblash mantiqi ham mock qilingan, haqiqiy kod ishga tushmaydi.
when(komissiyaHisoblagich.hisobla(any())).thenReturn(new BigDecimal("1000"));

// To'g'ri: faqat tashqi to'lov shlyuzi mock qilinadi.
when(tolovShlyuzi.yubor(any())).thenReturn(ShlyuzJavobi.muvaffaqiyat("TX-1"));
TolovNatijasi n = servis.amalgaOshir(buyruq); // haqiqiy mantiq yuradi
assertEquals(Holat.TOLANGAN, n.holat());
verify(tolovShlyuzi).yubor(argThat(s -> s.summa().equals(new BigDecimal("102000"))));
```

Sonar mock bilan bog'liq ikki narsani ushlaydi. `java:S1116` va shunga o'xshash qoidalar ishlatilmagan stub ni emas, lekin Mockito ning o'zi `strictStubs` rejimida ishlatilmagan stub uchun testni yiqitadi, bu esa ortiqcha stub ni tozalashga majbur qiladi. Ikkinchisi: faqat `verify` dan tashkil topgan test. U `java:S2699` dan o'tadi, ammo ishlab chiqarish mantiqini tekshirmaydi. Chiqish natijasi bor joyda natijani tekshiring, `verify` ni faqat tashqi ta'sir uchun qoldiring.

## 17.8 Spring kontekstiga bog'liq testni kamaytirish va tezlikni saqlash

Qamrov kontekstdan kelmaydi, kodning ishga tushishidan keladi. Shu sababli `@SpringBootTest` ni qamrov uchun ishlatish qimmat va sekin yo'l. Sonar uchun esa farqi yo'q: JaCoCo bir xil hisobni beradi, test unit yoki integratsion bo'lishidan qat'i nazar.

Amaliy qoida: domen va servis mantiqi oddiy JUnit testi bilan qoplanadi, kontekst faqat simlanish va konfiguratsiya to'g'riligini tekshiradi. Slice annotatsiyalar (`@WebMvcTest`, `@DataJpaTest`) kontekstni kichik qiladi va qamrovni aynan web yoki persistence qatlamida beradi.

```java
// Faqat controller qatlami. Servis mock, kontekst kichik, ishga tushish tez.
@WebMvcTest(BuyurtmaController.class)
class BuyurtmaControllerTest {

    @Autowired MockMvc mvc;
    @MockitoBean BuyurtmaServisi servis; // Spring Boot 3.4+ nomi

    @Test
    void notogriSumaUchun400Qaytaradi() throws Exception {
        mvc.perform(post("/api/buyurtmalar")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"sku\":\"SKU-1\",\"soni\":-1}"))
           .andExpect(status().isBadRequest())
           .andExpect(jsonPath("$.xatolar[0].maydon").value("soni"));
    }
}
```

Integratsion testning qamrovi hisobga olinishi uchun JaCoCo hisoboti ikki `exec` faylni birlashtirishi kerak. Testcontainers bilan ishlaydigan integratsion testlar odatda alohida profilda yuriladi va ularning hisoboti qo'shilmasa, coverage sun'iy ravishda past ko'rinadi.

```xml
<!-- unit va integratsion exec fayllarni bitta hisobotga birlashtirish -->
<execution>
  <id>merge-exec</id>
  <phase>verify</phase>
  <goals><goal>merge</goal></goals>
  <configuration>
    <fileSets>
      <fileSet><directory>${project.build.directory}</directory>
        <includes><include>jacoco*.exec</include></includes></fileSet>
    </fileSets>
    <destFile>${project.build.directory}/jacoco-aggregate.exec</destFile>
  </configuration>
</execution>
```

## 17.9 Vaqt, tasodif va tashqi holatga bog'liq kodni sinovga ochiq qilish

`LocalDate.now()` ni to'g'ridan to'g'ri chaqiradigan kodning ba'zi shoxlarini testda yurgizib bo'lmaydi. Masalan "oy oxiri" shoxi oyning oxirgi kunida ishlaydi va boshqa kunlari qizil qoladi. Bu holat Sonar da coverage yetishmasligi bo'lib ko'rinadi, aslida u dizayn muammosi.

```java
// Yomon: vaqt qotib qolgan, "oy oxiri" shoxini test yurgiza olmaydi.
public boolean hisobotYuborilsinmi() {
    return LocalDate.now().getDayOfMonth() == LocalDate.now().lengthOfMonth();
}

// Sonar o'tadigan dizayn: Clock injektsiya qilinadi, har ikki shox testga ochiq.
private final Clock clock;
public boolean hisobotYuborilsinmi() {
    LocalDate bugun = LocalDate.now(clock);
    return bugun.getDayOfMonth() == bugun.lengthOfMonth();
}
```

```java
@Test
void oyOxiridaHisobotYuboriladi() {
    Clock qotirilgan = Clock.fixed(Instant.parse("2025-10-31T09:00:00Z"), ZoneOffset.UTC);
    assertTrue(new HisobotServisi(qotirilgan).hisobotYuborilsinmi());
}
```

Tasodifiy qiymat uchun ham xuddi shu yo'l: `Random` yoki `UUID` generatori interfeys orqali beriladi. Qo'shimcha foyda bor: `java:S2245` qoidasi xavfsizlikka ta'sir qiladigan joyda `java.util.Random` ishlatilishini belgilaydi, generatorni ajratsangiz uni `SecureRandom` ga almashtirish bir joyda bo'ladi. `Thread.sleep` esa testda `java:S2925` bilan belgilanadi, uning o'rniga Awaitility yoki qotirilgan clock ishlatiladi.

## 17.10 Testni o'qiydigan qilib yozish: nom, tuzilish, ma'lumot

Sonar test fayllarida ham naming, murakkablik va duplication qoidalarini qo'llaydi. Shuning uchun o'qilishi oson test ko'pincha avtomatik ravishda issue siz test bo'ladi. Uchta amaliy nuqta bor.

Birinchi: metod nomi kutilgan xatti-harakatni aytsin. `test1` yoki `testHisobla` nomi naming convention qoidasidan o'tsa ham, yiqilgan testning sababini aytmaydi. Ikkinchi: tuzilish uch blokdan iborat bo'lsin va ularning orasi bo'sh qatorlar bilan ajratilsin. Uchinchi: test ma'lumoti builder orqali tayyorlansin, shunda nusxa ko'chirish kamayadi va duplication o'lchovi oshmaydi.

```java
// Test ma'lumoti builder: har testda faqat farq qiladigan maydon ko'rinadi.
static BuyurtmaBuilder buyurtma() {
    return new BuyurtmaBuilder().sku("SKU-1").soni(1).valyuta(Valyuta.UZS);
}

@Test
void valyutaBuyurtmasiUstamaBilanHisoblanadi() {
    Buyurtma b = buyurtma().valyuta(Valyuta.USD).soni(2).qur();

    BigDecimal jami = servis.jamiSumma(b);

    assertEquals(new BigDecimal("201000.000"), jami);
}
```

## 17.11 Qamrovni oshirish uchun yozilgan bo'sh testlarni tanib olish

Coverage sharti bosim qilganda jamoa ichida "qamrov testi" paydo bo'ladi. Ularni code review da tanib olish kerak, chunki Sonar ularning hammasini ushlamaydi. Quyidagi jadval eng ko'p uchraydigan shakllarni va yechimni beradi.

| Tuzoq | Sonar nima deydi | Yechim |
| --- | --- | --- |
| Assertion siz chaqiruv | `java:S2699` issue chiqaradi | Kutilgan natijani assertion qilish |
| Faqat `assertNotNull(natija)` | Hech narsa demaydi, gate o'tadi | Natijaning aniq qiymatini tekshirish |
| `assertTrue(true)` bilan yopish | Ba'zi hollarda S2699 dan o'tadi | Testni o'chirish yoki haqiqiy shart yozish |
| `@Disabled` qo'yib qoldirish | `java:S1607` issue chiqaradi | Tuzatish yoki o'chirish |
| Getter va setter uchun test | Hech narsa demaydi, coverage ko'tariladi | Generatsiya qilingan kodni exclusion ga olish |
| `toString` ni assertion qilish | Mo'rt test, qoida yo'q | Domen maydonini tekshirish |
| Mock ni mock bilan tekshirish | Qoida yo'q, qamrov yolg'on | Haqiqiy mantiqni yurgizish |
| Katta `@SpringBootTest` bilan hammasini ishga tushirish | Qoida yo'q, lekin CI sekinlashadi | Slice test va unit test ga bo'lish |
| `Thread.sleep` bilan kutish | `java:S2925` issue chiqaradi | Awaitility yoki qotirilgan clock |

Exclusion halol vosita, agar u faqat mantiqsiz kodni chetlab o'tsa. DTO, konfiguratsiya sinflari va generatsiya qilingan kod coverage hisobidan chiqarilishi mumkin. Servis yoki domen sinfini exclusion ga qo'yish esa raqamni bo'yash bo'ladi.

```properties
# Mantiqsiz kodni coverage hisobidan chiqarish. Servis sinflari bu yerda bo'lmaydi.
sonar.coverage.exclusions=\
  **/config/**,\
  **/dto/**,\
  **/*Application.java,\
  **/generated/**
# Test fayllari tahlil qilinadi, lekin coverage talabi ularga qo'llanmaydi.
sonar.tests=src/test/java
```

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Maqsad | Coverage foizini ko'tarish | Xatti-harakatni qayd etish, coverage natija sifatida kelishi |
| Holat tanlash | Baxtli yo'lni yozish | Chegara, null va istisno yo'llarini yozish |
| Istisno | `catch` ni testsiz qoldirish | `assertThrows` bilan tur va xabarni tekshirish |
| Ko'p holat | Metodni nusxa ko'chirish | `@ParameterizedTest` bilan jadval sifatida berish |
| Mock chizig'i | Qulay bo'lgan hamma narsani mock qilish | Faqat tashqi chegarani mock qilish |
| Spring | Hamma testga `@SpringBootTest` | Slice test, kontekst faqat simlanish uchun |
| Vaqt | `LocalDate.now()` to'g'ridan to'g'ri | `Clock` injektsiya, `Clock.fixed` bilan test |
| Kutish | `Thread.sleep(2000)` | Awaitility yoki deterministik vaqt |
| Exclusion | Coverage pasaysa servisni chiqarish | Faqat mantiqsiz kodni chiqarish, sababi yozilgan |
| Yiqilgan test | `@Disabled` qo'yish | Sababni tuzatish, flaky bo'lsa izolyatsiya qilish |

Integratsion test infratuzilmasi, Testcontainers va flaky testlarni barqarorlashtirish bo'yicha chuqur amaliyot [testlash qo'llanmasidagi](../testing/README.md) tegishli mavzularda beriladi. Bu yerda faqat ularning Sonar hisobiga qanday tushishi muhim edi.

## 17.12 Amalda qo'llash

- [ ] JaCoCo hisobotini ochib, shox qamrovi eng past uchta sinfni toping va ularning qoplanmagan shoxlarini sanab yozing.
- [ ] `java:S2699` va `java:S2187` issue lari ro'yxatini oling, har bir assertion siz testga kutilgan natija assertion ini qo'shing.
- [ ] `@Disabled` bilan belgilangan barcha testlarni toping, har biri uchun tuzatish yoki o'chirish qarorini qabul qiling.
- [ ] Nusxa ko'chirilgan test metodlarini bitta `@ParameterizedTest` ga yig'ib, chegaraviy qiymatlar uchun alohida qator qo'shing.
- [ ] `LocalDate.now()` va `new Random()` chaqiruvlarini loyiha bo'ylab grep qilib, ularni `Clock` va generator interfeysiga ko'chiring.
- [ ] Testlardagi `Thread.sleep` chaqiruvlarini Awaitility yoki qotirilgan vaqt bilan almashtiring.
- [ ] `sonar.coverage.exclusions` ro'yxatini ko'rib chiqing va mantiq saqlaydigan har bir sinfni undan chiqarib tashlang.
- [ ] Integratsion test `exec` faylining birlashtirilganini tekshirib, Sonar dagi coverage raqami lokal hisobot bilan mos kelishini tasdiqlang.

---

[&larr; 16. Security hotspot va vulnerability: tekshirish va tuzatish](16-security-hotspot-va-vulnerability.md) · [Mundarija](README.md) · [18. Branch va shart qamrovini to'liq yopish usullari &rarr;](18-branch-va-shart-qamrovini-toliq-yopish.md)
