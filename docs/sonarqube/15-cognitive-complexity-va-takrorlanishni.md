<!-- doc: sonarqube | chapter: 15 | part: IV. Sonar o'tadigan kod -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 15. Cognitive complexity va takrorlanishni kamaytirish (Cognitive Complexity and Duplication)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [15.1 Cognitive complexity qanday hisoblanadi: ortish va chuqurlik jarimasi](#151-cognitive-complexity-qanday-hisoblanadi-ortish-va-chuqurlik-jarimasi)
- [15.2 Cyclomatic complexity bilan farqi va nega Sonar ikkinchisini afzal ko'radi](#152-cyclomatic-complexity-bilan-farqi-va-nega-sonar-ikkinchisini-afzal-koradi)
- [15.3 Chegaradan oshgan metodni bo'lish usullari](#153-chegaradan-oshgan-metodni-bolish-usullari)
- [15.4 Shartlar daraxtini jadval yoki xaritaga aylantirish](#154-shartlar-daraxtini-jadval-yoki-xaritaga-aylantirish)
- [15.5 Qo'riqchi shart (guard clause) bilan chuqurlikni kamaytirish](#155-qoriqchi-shart-guard-clause-bilan-chuqurlikni-kamaytirish)
- [15.6 Strategiya tanlovini `switch` dan ko'rsatkichga ko'chirish](#156-strategiya-tanlovini-switch-dan-korsatkichga-kochirish)
- [15.7 Takrorlanish qanday aniqlanadi: token ketma-ketligi va eng kichik blok](#157-takrorlanish-qanday-aniqlanadi-token-ketma-ketligi-va-eng-kichik-blok)
- [15.8 Yolg'on takrorlanish: o'xshash, lekin boshqa sababga xizmat qiladigan kod](#158-yolgon-takrorlanish-oxshash-lekin-boshqa-sababga-xizmat-qiladigan-kod)
- [15.9 Takrorlanishni umumiy metodga chiqarish va qachon chiqarmaslik](#159-takrorlanishni-umumiy-metodga-chiqarish-va-qachon-chiqarmaslik)
- [15.10 Test kodidagi takrorlanish: alohida munosabat talab qiladi](#1510-test-kodidagi-takrorlanish-alohida-munosabat-talab-qiladi)
- [15.11 Murakkablikni o'lchash va uni kamaytirishni rejaga qo'yish](#1511-murakkablikni-olchash-va-uni-kamaytirishni-rejaga-qoyish)
- [15.12 Amalda qo'llash](#1512-amalda-qollash)

</details>



Cognitive complexity va takrorlanish Sonar hisobotida eng ko'p uchraydigan ikki muammo. Ikkisi ham quality gate ni Maintainability tomonidan to'xtatadi, lekin sababi boshqa: biri bitta metod ichidagi fikr yuki, ikkinchisi kod bazasidagi nusxalar. Quyida Sonar ularni qanday hisoblashini ko'rib chiqamiz, keyin bir uzun metodni bosqichma-bosqich chegaradan pastga tushiramiz. Maqsad raqamni yashirish emas, o'qilishi oson kod yozish.

## 15.1 Cognitive complexity qanday hisoblanadi: ortish va chuqurlik jarimasi

Cognitive complexity ni Sonar `java:S3776` qoidasi bilan tekshiradi, metod uchun standart chegara 15. Hisob uch qoidadan iborat.

Birinchi qoida: chiziqli oqimni buzgan har bir konstruksiya uchun +1 qo'shiladi. Bunga `if`, `else if`, `else`, uchlik operator, `switch`, `for`, `while`, `do while`, `catch`, belgiga `break` yoki `continue`, va rekursiya kiradi.

Ikkinchi qoida: ichma-ich joylashish jarimasi. Agar konstruksiya boshqa konstruksiya ichida bo'lsa, u +1 emas, +(1 + chuqurlik) oladi. Ya'ni ikkinchi qavatdagi `if` +2, uchinchi qavatdagi `if` +3 beradi. Jarima `if`, uchlik operator, `switch`, sikllar va `catch` ga tegishli.

Uchinchi qoida: ba'zi narsalar jarimadan ozod. `else` va `else if` faqat +1 oladi, chuqurlik jarimasi yo'q, chunki o'quvchi uchun ular bir xil darajadagi tanlov. `switch` butun bloki uchun +1, `case` lar soni ahamiyatsiz. Mantiqiy operatorlar ketma-ketligi uchun esa har bir operator emas, har bir ketma-ketlik +1 oladi: `a && b && c` bitta ball, `a && b || c` esa ikkita, chunki operator turi o'zgardi.

Natijada bir xil shart sonida ball juda farq qiladi. Tekis o'nta `if` 10 ball, ichma-ich beshta `if` esa 1+2+3+4+5 = 15 ball. Sonar aynan chuqurlikni jazolaydi, chunki u o'quvchidan har qavatda kontekstni yodda saqlashni talab qiladi.

## 15.2 Cyclomatic complexity bilan farqi va nega Sonar ikkinchisini afzal ko'radi

Cyclomatic complexity (McCabe) qarorlar nuqtasini sanaydi va test yo'llari sonini baholaydi. Sonar da u hozir ham `complexity` metrikasi sifatida hisoblanadi, lekin metod chegarasi qoidasi yangi Java analyzer liniyalarida ikkinchi planda qoldi. Sababi: u bir qancha holatda o'qilishni to'g'ri aks ettirmaydi.

| Holat | Cyclomatic | Cognitive | Haqiqatda o'qilishi |
|---|---|---|---|
| 10 case li tekis `switch` | 10 ga yaqin | 1 | Oson, jadvalga o'xshaydi |
| 5 qavat ichma-ich `if` | 5 ga yaqin | 15 | Juda qiyin |
| `getter` lar bilan uzun klass | Har metodda 1 | Har metodda 0 | Oson |
| `a && b && c && d` | 4 ga yaqin | 1 | Bitta fikr, oson |
| 3 qavatli sikl ichida `try/catch` | 4 ga yaqin | 10 dan ortiq | Qiyin |

`switch` cyclomatic bo'yicha jazolanadi, cognitive bo'yicha deyarli bepul. Bu to'g'ri, chunki 20 ta valyuta kodini o'girgan `switch` bir qarashda tushuniladi. Teskarisi, uch qavat sikl ichidagi shart cyclomatic bo'yicha arzon, odam uchun esa og'ir.

Amaliy xulosa: cyclomatic complexity ni test qoplamini rejalashtirishda ishlat, cognitive complexity ni refactoring navbatini tuzishda ishlat.

## 15.3 Chegaradan oshgan metodni bo'lish usullari

Mana haqiqiy chegirma hisoblash metodi. Sonar unga `java:S3776` qo'yadi, ball 24 ga chiqadi, ustiga `java:S134` (haddan ortiq ichma-ich joylashish) ham tushadi.

```java
// YOMON: cognitive complexity 24, chegara 15
public BigDecimal chegirma(Buyurtma b) {
    BigDecimal natija = BigDecimal.ZERO;
    if (b != null) {                                         // +1
        if (b.getMijoz() != null) {                          // +2
            if (b.getMijoz().getDaraja() == Daraja.GOLD) {   // +3
                if (b.getSumma().compareTo(LIMIT) > 0) {     // +4
                    natija = foiz(b, "0.15");
                } else {                                     // +1
                    natija = foiz(b, "0.10");
                }
            } else if (b.getMijoz().getDaraja() == Daraja.SILVER) { // +1
                if (b.getSumma().compareTo(LIMIT) > 0) {     // +4
                    natija = foiz(b, "0.08");
                } else {                                     // +1
                    natija = foiz(b, "0.05");
                }
            }
            for (Qator q : b.getQatorlar()) {                // +2
                if (q.aksiyada() && q.getSoni() > 10) {      // +3, && uchun +1
                    natija = natija.add(q.getNarx());
                }
            }
        }
    }
    return natija;
}
```

Birinchi qadam eng arzon: aksiya bonusi chegirma foizidan mustaqil, uni alohida metodga chiqaramiz.

```java
// 1-qadam: aksiya bonusini ajratdik. Yangi metod ball 3, asosiy metod 7 ball yengildi.
private BigDecimal aksiyaBonusi(List<Qator> qatorlar) {
    return qatorlar.stream()                                  // +0
            .filter(q -> q.aksiyada() && q.getSoni() > 10)     // +1 (lambda ichida && )
            .map(Qator::getNarx)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Metodni bo'lish ballni yashirish emas, chunki Sonar har metodni alohida o'lchaydi va chegara ham metod darajasida. Lekin suiiste'mol qilsa, 20 ta ma'nosiz `private` metod paydo bo'ladi. Mezon bitta: ajratilgan bo'lakka to'g'ri nom berish mumkinmi? `aksiyaBonusi` yaxshi nom, `qism2` esa bo'linish noto'g'ri joydan o'tgani belgisi.

## 15.4 Shartlar daraxtini jadval yoki xaritaga aylantirish

Qolgan daraxt aslida jadval: daraja va summa chegarasi bo'yicha foiz. Uni kodda emas, ma'lumot sifatida saqlash mumkin.

```java
// 2-qadam: daraxt yo'qoldi, jadval paydo bo'ldi. Metod ball 1 ga tushdi.
private static final Map<Daraja, NavigableMap<BigDecimal, BigDecimal>> JADVAL =
        Map.of(
            Daraja.GOLD,   tariff("0", "0.10", "5000000", "0.15"),
            Daraja.SILVER, tariff("0", "0.05", "5000000", "0.08"),
            Daraja.BRONZE, tariff("0", "0.00")
        );

private BigDecimal foizTopish(Daraja daraja, BigDecimal summa) {
    NavigableMap<BigDecimal, BigDecimal> qator =
            JADVAL.getOrDefault(daraja, BOSH_JADVAL);
    // floorEntry summadan kichik yoki teng eng katta chegarani beradi
    Map.Entry<BigDecimal, BigDecimal> topilgan = qator.floorEntry(summa);
    return topilgan == null ? BigDecimal.ZERO : topilgan.getValue();  // +1
}
```

Agar foizlar tez o'zgarsa, jadvalni bazaga ko'chirish mantiqiy: kod o'zgarmaydi, faqat ma'lumot o'zgaradi.

```sql
-- Chegirma tarifi: kod emas, ma'lumot. Har o'zgarishda deploy kerak emas.
CREATE TABLE chegirma_tarifi (
    id            BIGSERIAL PRIMARY KEY,
    daraja        VARCHAR(16) NOT NULL,
    min_summa     NUMERIC(19, 2) NOT NULL,
    foiz          NUMERIC(5, 4) NOT NULL,
    amal_boshlanish DATE NOT NULL,
    CONSTRAINT uq_tarif UNIQUE (daraja, min_summa, amal_boshlanish)
);

-- Eng mos tarifni bitta so'rov bilan topish: shart kodda emas, indeksda
SELECT foiz
FROM chegirma_tarifi
WHERE daraja = :daraja
  AND min_summa <= :summa
  AND amal_boshlanish <= CURRENT_DATE
ORDER BY min_summa DESC, amal_boshlanish DESC
LIMIT 1;
```

Halol bo'lish kerak: jadvalga ko'chirish murakkablikni yo'q qilmaydi, uni koddan ma'lumot bazasiga ko'chiradi. Zarari shunda: xato tarif endi compile vaqtida ushlanmaydi, migratsiya va validatsiya kerak. Tarif haftada bir marta o'zgarsa almashtirish foydali, yilda bir marta o'zgarsa `enum` da qoldirish yaxshiroq.

## 15.5 Qo'riqchi shart (guard clause) bilan chuqurlikni kamaytirish

Endi eng katta jarima manbasi qoldi: ikki qavat `null` tekshiruvi. Ular butun metod tanasini ikki qavat ichkariga surgan va har bir ichki `if` ga +2 qo'shgan. Guard clause buni tekislaydi.

```java
// 3-qadam: yakuniy variant. Cognitive complexity 2, S134 ham yo'qoldi.
public BigDecimal chegirma(Buyurtma b) {
    if (b == null || b.getMijoz() == null) {       // +1, || ketma-ketligi uchun +1
        return BigDecimal.ZERO;                     // qo'riqchi: darhol chiqamiz
    }
    BigDecimal foiz = foizTopish(b.getMijoz().getDaraja(), b.getSumma());
    BigDecimal asosiy = b.getSumma().multiply(foiz);
    return asosiy.add(aksiyaBonusi(b.getQatorlar()));
}
```

24 dan 2 ga tushdi, mantiq esa o'zgarmadi. Uch qadam ishladi: mustaqil mas'uliyatni ajratish, shart daraxtini jadvalga aylantirish, qolgan tekshiruvni qo'riqchiga chiqarish.

Guard clause da bitta tuzoq bor. Sonar `java:S1142` qoidasi bir metodda `return` soni ko'p bo'lsa shikoyat qiladi, standart chegara 3. Shuning uchun guard larni cheksiz qo'shib bo'lmaydi. Agar beshta `null` tekshiruvi kerak bo'lsa, bu metod emas, ma'lumot modeli muammosi: `Optional`, `record` ichida majburiy maydon yoki `@NotNull` validatsiyasi bilan tekshiruvni chegaraga ko'chirish to'g'riroq.

## 15.6 Strategiya tanlovini `switch` dan ko'rsatkichga ko'chirish

Katta `switch` o'zi ball oshirmaydi, lekin `case` ichida mantiq bo'lsa, ichkaridagi `if` lar jarima olib ball tez o'sadi. Ustiga har yangi to'lov usuli bir xil faylni o'zgartirishga majbur qiladi.

```java
// YOMON: har case ichida mantiq bor, ball tez o'sadi va fayl doim o'zgaradi
public Natija tola(TolovTuri turi, Tolov t) {
    switch (turi) {                                  // +1
        case KARTA:
            if (t.getSumma().compareTo(KARTA_LIMIT) > 0) { // +2
                return Natija.rad("limit");
            }
            return kartaClient.yubor(t);
        case HISOB:
            if (!t.getHisob().faol()) { return Natija.rad("faol emas"); } // +2
            return hisobClient.yubor(t);
        default:
            throw new IllegalStateException("noma'lum tur");
    }
}
```

Yechim: har usulni o'z klassiga chiqarib, tanlovni xaritaga aylantirish. Spring da konteyner `List` ni o'zi to'ldiradi.

```java
// Sonar o'tadigan variant: tanlov 0 ball, yangi tur yangi klass bilan qo'shiladi
public interface TolovStrategiyasi {
    TolovTuri turi();
    Natija bajar(Tolov t);
}

@Service
public class TolovServisi {
    private final Map<TolovTuri, TolovStrategiyasi> xarita;

    // Spring barcha implementatsiyani o'zi topadi, qo'lda ro'yxat yozilmaydi
    public TolovServisi(List<TolovStrategiyasi> strategiyalar) {
        this.xarita = strategiyalar.stream()
            .collect(toMap(TolovStrategiyasi::turi, s -> s));
    }

    public Natija tola(TolovTuri turi, Tolov t) {
        TolovStrategiyasi s = xarita.get(turi);
        if (s == null) {                             // +1
            throw new NoqonuniyTolovTuri(turi);
        }
        return s.bajar(t);
    }
}
```

Dizayn tomoni pattern katalogidagi Strategy mavzusida batafsil. Sonar hisobi bu yerda shunday: `tola` metodi 1 ball, har strategiya alohida fayl va alohida kichik ball. Yon foyda, har strategiyani alohida test qilish oson, demak coverage ham ko'tariladi.

## 15.7 Takrorlanish qanday aniqlanadi: token ketma-ketligi va eng kichik blok

Sonar takrorlanishni CPD (copy paste detector) bilan topadi: kodni token ketma-ketligiga aylantirib, bir xil ketma-ketliklarni qidiradi. Identifikator nomlari hisobga olinadi, shuning uchun nomni almashtirish ba'zan blokni chegaradan pastga tushiradi.

Java chegarasi boshqa tillardan farq qiladi: blok takrorlanish sanalishi uchun kamida 10 ta ketma-ket va bir xil statement kerak, token soni hisobga olinmaydi. Ko'p boshqa tilda chegara token va qator soniga bog'liq. Amalda bu shuni bildiradi: 8 statement li nusxa Sonar da ko'rinmaydi, lekin yaxshi kod bo'lib qolmaydi.

Hisobotda uch metrika bor: `duplicated_lines_density` (foiz), `duplicated_blocks` va `duplicated_files`. Standart "Sonar way" gate da new code uchun duplikatsiya 3 foizdan kam bo'lishi talab qilinadi, eski kod shartga kirmaydi.

```properties
# sonar-project.properties: nima tahlil qilinadi va nima CPD dan chiqariladi
sonar.projectKey=ombor-servisi
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes

# Generatsiya qilingan kod: takrorlanish bor, lekin qo'l tegmaydi
sonar.cpd.exclusions=**/generated/**,**/*MapperImpl.java,**/dto/**

# Butun tahlildan chiqarish bu boshqa narsa, ehtiyot bo'l
sonar.exclusions=**/target/**,**/*Config.java.bak
```

`sonar.cpd.exclusions` faqat takrorlanish tekshiruvini o'chiradi, boshqa qoidalar ishlaydi. `sonar.exclusions` esa faylni butunlay tahlildan chiqaradi va coverage hisobiga tegadi. Ikkisini aralashtirish ko'p uchraydigan xato.

## 15.8 Yolg'on takrorlanish: o'xshash, lekin boshqa sababga xizmat qiladigan kod

CPD matnni ko'radi, maqsadni ko'rmaydi, shuning uchun ikki mustaqil qoidani takrorlanish deb belgilaydi. Misol: buyurtma validatsiyasi va qaytarish validatsiyasi bugun bir xil, ertaga ajralib ketadi. Ularni birlashtirsang, metodga `boolean qaytarishMi` parametri qo'shiladi, keyin ikkinchi flag. Natijada bitta chalkash metod, ikki tiniq metoddan yomonroq.

Qarorni ikki savol bilan qabul qil. Birinchi savol: bu ikki joy bir sabab bilan o'zgaradimi? Agar bitta biznes qoidasi o'zgarganda ikkisi ham o'zgarishi shart bo'lsa, bu haqiqiy takrorlanish. Ikkinchi savol: umumiy metodga nom topa olamanmi? Agar nom `umumiyIshlov` yoki `tekshirHammasi` bo'lib chiqsa, demak umumiy tushuncha yo'q.

Yolg'on takrorlanishni `sonar.cpd.exclusions` bilan emas, issue ni izoh bilan yopish orqali hal qil, chunki sabab o'sha joyda qoladi. Holat nomi versiyaga qarab farq qiladi: eski liniyada `Won't Fix`, yangi liniyada `Accepted`.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Blok 9 statement, Sonar jim | Java chegarasi 10 statement | Chegaraga emas, sababga qara; nusxa bo'lsa birlashtir |
| Nom almashtirib duplikatsiyani yashirish | CPD identifikatorga sezgir | Bu texnik qarz, keyin ikki joyda bug tuzatiladi |
| `sonar.exclusions` bilan yopish | Coverage ham yo'qoladi | `sonar.cpd.exclusions` ishlat |
| Umumiy metodga flag parametri | Ikki sabab bitta metodga siqilgan | Ikki alohida metod qoldir |
| MapStruct `Impl` fayllari | Generatsiya qilingan nusxa | CPD dan chiqar, `target` ni source qilma |
| DTO va entity bir xil maydonlar | Tabiiy o'xshashlik | Birlashtirma, qatlam chegarasi muhimroq |
| Metodni mayda `private` larga maydalash | Ball tushadi, o'qilishi yomonlashadi | Faqat nom topilsa ajrat |
| Test da nusxa ko'rish | Testda nusxa ba'zan foydali | Pastdagi test bo'limiga qara |

## 15.9 Takrorlanishni umumiy metodga chiqarish va qachon chiqarmaslik

Haqiqiy takrorlanishda eng yaxshi yechim o'zgaruvchan qismni parametr qilish, qolganini o'zgarmas qoldirish. Omborda qoldiq tekshiruvi misoli.

```java
// YOMON: uchta joyda bir xil 11 statement, Sonar duplicated_blocks beradi
// (reservQil, bekorQil, inventarizatsiya metodlarida aynan shu blok bor)

// Sonar o'tadigan variant: bir xil qism bitta metodda, farq lambda da
private <T> T qoldiqBilanIshla(Long mahsulotId,
                               Function<Qoldiq, T> amal) {
    Qoldiq q = qoldiqRepo.findByMahsulotIdForUpdate(mahsulotId)
            .orElseThrow(() -> new QoldiqTopilmadi(mahsulotId));
    if (q.arxivlangan()) {                                  // +1
        throw new ArxivQoldiq(mahsulotId);
    }
    T natija = amal.apply(q);
    q.setOxirgiTegish(Instant.now());
    qoldiqRepo.save(q);
    return natija;
}

// Chaqiruv joyi qisqa va maqsadi tiniq
public void reservQil(Long mahsulotId, int soni) {
    qoldiqBilanIshla(mahsulotId, q -> {
        q.kamaytir(soni);
        return null;
    });
}
```

Chiqarmaslik kerak bo'lgan holatlar aniq. Ikki modul mustaqil deploy qilinsa, umumiy metod ular orasida keraksiz bog'liqlik yaratadi. Takrorlangan kod ikki xil qatlamda bo'lsa, masalan DTO va entity, o'xshashlik tabiiy. Umumiy metod uchta `boolean` parametr talab qilsa, u ikki maqsadni siqib turgan. Blok hali barqarorlashmagan yangi funksiya ichida bo'lsa, uchinchi nusxagacha kutish amalda yaxshi ishlaydi.

## 15.10 Test kodidagi takrorlanish: alohida munosabat talab qiladi

Sonar `sonar.tests` papkasini ham tahlil qiladi, lekin qoida to'plami boshqacha va duplikatsiya metrikasiga test kodi odatda qo'shilmaydi. Shunga qaramay testdagi nusxa real muammo, chunki o'qilishni buzadi.

Munosabat ishlab chiqarish kodidan yumshoqroq bo'lishi kerak. Test o'z holicha o'qilishi muhim: o'quvchi uchta fayl ochmasdan nima tekshirilayotganini tushunishi kerak. Shuning uchun `assert` larni "umumiy tekshiruv" metodiga yashirish ko'pincha zarar. Test ma'lumotini tayyorlash qismi boshqa gap, u takrorlanganda fixture ga chiqarish to'g'ri.

```java
// Test ma'lumotini tayyorlash: nusxa bu yerda zarar, builder yaxshi
public final class BuyurtmaFixture {
    public static Buyurtma.Builder oddiy() {
        return Buyurtma.builder()
                .mijoz(Mijoz.builder().daraja(Daraja.BRONZE).build())
                .summa(new BigDecimal("100000"))
                .qatorlar(List.of());
    }
    // Har test faqat o'zi uchun muhim maydonni o'zgartiradi
    // gold().summa(...).build() ko'rinishida chaqiriladi
    public static Buyurtma.Builder gold() {
        return oddiy().mijoz(Mijoz.builder().daraja(Daraja.GOLD).build());
    }
}
```

Parametrlangan test eng arzon usul, lekin uni faqat bir xil xatti harakat turli kirish bilan tekshirilganda ishlat. Har holat uchun boshqa `assert` kerak bo'lsa, u mos emas. Fixture ni tashkil qilishning to'liq ko'rinishi [testlash qo'llanmasidagi](../testing/README.md) test ma'lumotlari mavzusida.

## 15.11 Murakkablikni o'lchash va uni kamaytirishni rejaga qo'yish

Murakkablikni bir martalik aksiya bilan tuzatib bo'lmaydi. Birinchi qadam hozirgi holatni raqamda bilish, buni Sonar web API beradi.

```bash
# Loyiha bo'yicha umumiy ko'rsatkichlar
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/measures/component?component=ombor-servisi\
&metricKeys=cognitive_complexity,complexity,duplicated_lines_density,duplicated_blocks"

# Eng og'ir 20 metodni topish: S3776 issue larini qoldiq bo'yicha saralash
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/issues/search?componentKeys=ombor-servisi\
&rules=java:S3776&ps=20&s=FILE_LINE" | jq -r '.issues[] | "\(.component) \(.line) \(.message)"'
```

Keyingi qadam chegarani yangi kod uchun qattiq ushlash. Bu "clean as you code": eski 400 ta issue bugun tuzatilmaydi, lekin yangi kod toza bo'ladi.

```xml
<!-- pom.xml: sonar-maven-plugin versiyasini qotirib qo'y, aks holda CI beqaror -->
<plugin>
  <groupId>org.sonarsource.scanner.maven</groupId>
  <artifactId>sonar-maven-plugin</artifactId>
  <version>3.11.0.3922</version>
</plugin>

<!-- Quality gate natijasini kutish: CI tahlildan keyin to'xtamasligi uchun -->
<properties>
  <sonar.qualitygate.wait>true</sonar.qualitygate.wait>
  <!-- Faqat yangi kod shartiga tayanamiz, eski qarz alohida reja -->
  <sonar.newCode.referenceBranch>main</sonar.newCode.referenceBranch>
</properties>
```

```yaml
# CI da tartib muhim: avval test va JaCoCo hisoboti, keyin sonar
jobs:
  tahlil:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # new code hisobi uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin' }
      # verify JaCoCo report ni yaratadi, sonar uni o'qiydi
      - run: ./mvnw -B verify
      - run: ./mvnw -B sonar:sonar -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

Eski qarzni saralash mezoni: `git log` dan o'zgarish chastotasini, Sonar dan cognitive complexity ni olib ikkisini ko'paytir. Yuqori ko'paytma bergan 10 fayl refactoring navbatining boshi. Hech kim tegmaydigan 300 ballik fayl kuta turadi, uni tuzatish xavfi foydadan katta.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| S3776 chegarasi | Chegarani 25 ga ko'tarish | Chegarani qoldirib, metodni bo'lish |
| Shart daraxti | Yana bitta `else if` qo'shish | Jadval yoki `Map` ga ko'chirish |
| `null` tekshiruvi | Butun tanani `if` ichiga olish | Guard clause va chegarada validatsiya |
| Yangi to'lov turi | `switch` ga case qo'shish | Yangi strategiya klassi qo'shish |
| Takrorlanish topildi | Darhol umumiy metodga chiqarish | Avval "bir sabab bilan o'zgaradimi" savoli |
| Generatsiya qilingan kod | `sonar.exclusions` bilan yopish | `sonar.cpd.exclusions` bilan faqat CPD ni yopish |
| Eski qarz | Hammasini bitta sprintda tuzatish | New code ni toza ushlash, qarzni chastota bilan saralash |
| Test takrorlanishi | Hamma `assert` ni helper ga yashirish | Fixture ni umumlashtirish, `assert` ni testda qoldirish |
| O'lchash | Faqat gate rangiga qarash | API dan metrikani olib trend kuzatish |
| Issue ni yopish | `//NOSONAR` qo'yish | Sababni izohlab `Accepted` holatiga o'tkazish |

Oxirgi ogohlantirish: `//NOSONAR` qoidani o'chiradi, lekin sababsiz qo'yilsa keyingi o'quvchi uchun qora quti. Ishlatish zarur bo'lsa, yonida nega kerakligini bir qatorda yoz. `//NOSONAR` sonining o'sishi texnik qarzning ishonchli signali.

## 15.12 Amalda qo'llash

- [ ] Loyihada `java:S3776` bo'yicha eng yuqori ballga ega 10 metodni API orqali chiqar va ro'yxatni jamoaga ko'rsat.
- [ ] Shu ro'yxatdan bitta metodni tanlab, uch qadamni ketma-ket qo'lla: mustaqil qismni ajratish, shart daraxtini jadvalga ko'chirish, guard clause bilan tekislash.
- [ ] Refactoring dan oldin o'sha metod uchun xatti harakatni qotiradigan testlarni yoz, keyingina kodni o'zgartir.
- [ ] `sonar.cpd.exclusions` ni generatsiya qilingan kod uchun to'g'ri sozla va `sonar.exclusions` bilan aralashtirilgan joylarni tekshirib tozala.
- [ ] Katta `switch` lardan birini strategiya xaritasiga aylantir va har strategiyaga alohida test yoz.
- [ ] CI da `sonar.qualitygate.wait=true` va `fetch-depth: 0` borligini tasdiqla, aks holda new code hisobi noto'g'ri chiqadi.
- [ ] `//NOSONAR` va `Accepted` holatidagi issue larni sanab chiq, sababsizlarini sababli qil yoki tuzat.
- [ ] O'zgarish chastotasi va cognitive complexity ko'paytmasi bo'yicha refactoring navbatini tuz va uni har chorakda yangila.

---

[&larr; 14. Java va Spring da eng ko'p uchraydigan issue va ularning yechimi](14-java-va-spring-da-eng-kop-uchraydigan-issue.md) · [Mundarija](README.md) · [16. Security hotspot va vulnerability: tekshirish va tuzatish &rarr;](16-security-hotspot-va-vulnerability.md)
