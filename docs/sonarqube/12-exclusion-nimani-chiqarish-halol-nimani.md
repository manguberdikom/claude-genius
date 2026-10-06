<!-- doc: sonarqube | chapter: 12 | part: III. Qamrov (coverage) -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 12. Exclusion: nimani chiqarish halol, nimani chiqarish aldov (Exclusions, Honest and Dishonest)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [12.1 Exclusion turlari: tahlildan, qamrovdan, takrorlanishdan, muayyan qoidadan](#121-exclusion-turlari-tahlildan-qamrovdan-takrorlanishdan-muayyan-qoidadan)
- [12.2 `sonar.exclusions`, `sonar.coverage.exclusions`, `sonar.cpd.exclusions` farqi](#122-sonarexclusions-sonarcoverageexclusions-sonarcpdexclusions-farqi)
- [12.3 Generatsiya qilingan kodni chiqarish: nega bu halol qaror](#123-generatsiya-qilingan-kodni-chiqarish-nega-bu-halol-qaror)
- [12.4 DTO, entity va konfiguratsiya klasslarini chiqarish: qachon o'rinli](#124-dto-entity-va-konfiguratsiya-klasslarini-chiqarish-qachon-orinli)
- [12.5 Migratsiya skriptlari va qolip (template) fayllari](#125-migratsiya-skriptlari-va-qolip-template-fayllari)
- [12.6 `@Generated` annotatsiyasi va JaCoCo ning unga munosabati](#126-generated-annotatsiyasi-va-jacoco-ning-unga-munosabati)
- [12.7 Kod ichida bostirish: `@SuppressWarnings` va Sonar ning maxsus izohi](#127-kod-ichida-bostirish-suppresswarnings-va-sonar-ning-maxsus-izohi)
- [12.8 Bostirishni majburan asoslash: izoh talab qilish qoidasi](#128-bostirishni-majburan-asoslash-izoh-talab-qilish-qoidasi)
- [12.9 Aldov belgilari: butun paketni chiqarish, murakkab klassni chiqarish](#129-aldov-belgilari-butun-paketni-chiqarish-murakkab-klassni-chiqarish)
- [12.10 Exclusion ro'yxatini ko'rib chiqish tartibi va uni kim tasdiqlaydi](#1210-exclusion-royxatini-korib-chiqish-tartibi-va-uni-kim-tasdiqlaydi)
- [12.11 Exclusion siyosatini hujjatlashtirish namunasi](#1211-exclusion-siyosatini-hujjatlashtirish-namunasi)
- [12.12 Amalda qo'llash](#1212-amalda-qollash)

</details>



Exclusion Sonarda eng kuchli va ayni paytda eng xavfli sozlama. Bir qator konfiguratsiya bilan siz minglab satrni tahlildan chiqarib, quality gate ni yashil qilib qo'yishingiz mumkin. Farq shundaki, ba'zi exclusion lar o'lchovni aniqroq qiladi, boshqalari esa o'lchovni soxtalashtiradi. Bu bob shu ikki holatni ajratishga, va qaysi biri ekanini kod review da isbotlashga qaratilgan.

## 12.1 Exclusion turlari: tahlildan, qamrovdan, takrorlanishdan, muayyan qoidadan

Sonarda "chiqarish" bitta tugma emas, balki to'rtta mustaqil qatlam. Birinchisi tahlildan chiqarish: fayl umuman skanerlanmaydi, uning issue lari ham, satrlari ham loyiha metrikasida yo'q. Ikkinchisi coverage dan chiqarish: fayl tahlil qilinadi va code smell lari ko'rinadi, lekin "qoplanishi kerak bo'lgan satrlar" hisobiga kirmaydi. Uchinchisi duplication dan chiqarish: fayl tahlilda ham, coverage da ham qoladi, faqat takrorlanish detektori uni ko'rmaydi. To'rtinchisi eng nozik qatlam: muayyan qoidani muayyan fayl naqshi uchun o'chirish, qolgan hamma qoida esa ishlashda davom etadi.

Bu to'rtta qatlamni bilish amaliy ahamiyatga ega. Ko'pchilik jamoa aslida bitta qoidadan bezor bo'lib, butun faylni tahlildan chiqarib tashlaydi. Natijada o'sha faylda keyin paydo bo'ladigan haqiqiy nuqsonlar ham abadiy ko'rinmas bo'lib qoladi. To'g'ri reaksiya eng tor qatlamni tanlash: avval bitta qoida, keyin coverage, keyin duplication, va faqat oxirgi chora sifatida butun fayl.

## 12.2 `sonar.exclusions`, `sonar.coverage.exclusions`, `sonar.cpd.exclusions` farqi

Uchala kalit fayl naqshini qabul qiladi, lekin ta'siri butunlay boshqacha. `sonar.exclusions` faylni manba kodi to'plamidan olib tashlaydi, shuning uchun Lines of Code kamayadi va o'sha fayl hech qanday metrikada qatnashmaydi. `sonar.coverage.exclusions` faqat coverage o'lchoviga ta'sir qiladi: fayldagi satrlar "uncovered" deb hisoblanmaydi, chunki ular umuman "to cover" ro'yxatiga tushmaydi. `sonar.cpd.exclusions` esa copy-paste detektorini o'chiradi va bu generatsiya qilingan yoki qolip asosidagi kodda o'rinli.

```properties
# sonar-project.properties: har bir qatlam o'z vazifasi uchun
sonar.projectKey=payment-service
sonar.java.binaries=target/classes

# Tahlildan butunlay chiqarish: faqat generatsiya qilingan kod
sonar.exclusions=\
  target/generated-sources/**/*, \
  **/generated/**/*Grpc.java, \
  **/*MapperImpl.java

# Tahlilda qoladi, lekin coverage talab qilinmaydi
sonar.coverage.exclusions=\
  **/config/**/*Config.java, \
  **/PaymentServiceApplication.java, \
  **/dto/**/*Request.java

# Takrorlanish detektoridan chiqarish: qolip asosidagi fayllar
sonar.cpd.exclusions=\
  **/dto/**/*.java, \
  **/*Entity.java

sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

Muhim halollik nuqtasi: `sonar.exclusions` coverage foizining maxrajini ham kichraytiradi. Ya'ni siz testlanmagan katta faylni tahlildan chiqarsangiz, coverage raqami o'z-o'zidan ko'tariladi. Bu raqam yaxshilanishi emas, o'lchov maydonining qisqarishi. Shu sababli coverage ni ko'tarish uchun `sonar.exclusions` ga tegish eng ko'p uchraydigan aldov usuli.

Muayyan qoidani tor doirada o'chirish uchun multicriteria mexanizmi ishlatiladi. Bu eng aniq vosita, chunki u "qaysi qoida" va "qaysi fayl" degan ikki savolga aniq javob beradi.

```xml
<!-- pom.xml: bitta qoidani bitta fayl naqshi uchun o'chirish -->
<properties>
  <!-- Har bir ignore uchun alohida kalit, vergul bilan ro'yxat -->
  <sonar.issue.ignore.multicriteria>e1,e2</sonar.issue.ignore.multicriteria>

  <!-- e1: migratsiya testlarida "magic number" qoidasi mantiqsiz -->
  <sonar.issue.ignore.multicriteria.e1.ruleKey>java:S109</sonar.issue.ignore.multicriteria.e1.ruleKey>
  <sonar.issue.ignore.multicriteria.e1.resourceKey>
    **/migration/*MigrationTest.java
  </sonar.issue.ignore.multicriteria.e1.resourceKey>

  <!-- e2: qator takrorlanishi qolip fayllarida kutilgan hol -->
  <sonar.issue.ignore.multicriteria.e2.ruleKey>java:S1192</sonar.issue.ignore.multicriteria.e2.ruleKey>
  <sonar.issue.ignore.multicriteria.e2.resourceKey>
    **/support/TestFixtures.java
  </sonar.issue.ignore.multicriteria.e2.resourceKey>
</properties>
```

## 12.3 Generatsiya qilingan kodni chiqarish: nega bu halol qaror

Generatsiya qilingan kod uchun exclusion halol, chunki uning muallifi odam emas. MapStruct ning `MapperImpl` fayli, gRPC yoki Protobuf stublari, OpenAPI dan chiqqan klient klasslari, QueryDSL ning `Q` klasslari, JOOQ sxemasi: bularning hech birini developer qo'li bilan tuzatmaydi. Sonar bu fayllarda "uzun metod" yoki "takrorlangan blok" deb shikoyat qilsa, bu shikoyatga javob yo'q, chunki tuzatish keyingi build da yo'q bo'ladi.

Ikkinchi dalil texnik: generatsiya qilingan kod `target/` yoki `build/` ichida yotadi va versiya nazoratida bo'lmaydi. Uni tahlilga qo'shish quality gate ni generator versiyasiga bog'lab qo'yadi. Generator yangilansa, hech kim kod yozmagan holda yuzlab yangi issue paydo bo'ladi. Bu "new code" o'lchovini ma'nosiz qiladi, chunki new code endi odamning o'zgarishini emas, bog'liqlik yangilanishini aks ettiradi.

Uchinchi dalil mas'uliyat haqida. Generatorning o'zi kutubxona bo'lib, uning sifatini sizning jamoangiz emas, uning muallifi nazorat qiladi. Sizning mas'uliyatingiz generatorga beradigan kirish: mapper interfeysi, `.proto` fayli, OpenAPI spetsifikatsiyasi. Shu kirish fayllari esa tahlilda qolishi kerak, chunki ularni odam yozadi.

## 12.4 DTO, entity va konfiguratsiya klasslarini chiqarish: qachon o'rinli

Bu yerda javob "shartli". DTO va entity ni coverage dan chiqarish o'rinli, qachonki ularda mantiq bo'lmasa. Faqat maydon, getter, setter, `equals` va `hashCode` bo'lgan klass uchun test yozish hech narsani isbotlamaydi. Lekin entity ichida `addItem` metodi invariant tekshirsa, yoki DTO ichida `toDomain` konvertatsiyasi bo'lsa, u endi mantiq va coverage dan chiqarilmasligi kerak.

```java
// YOMON: entity ichida mantiq bor, lekin coverage dan chiqarilgan
@Entity
public class Order {
    @Id private Long id;
    private BigDecimal total;
    private OrderStatus status;

    // Bu invariant: bekor qilingan buyurtmaga qator qo'shilmaydi.
    // Shu shart testsiz qolsa, regressiya jim o'tadi.
    public void addItem(OrderItem item) {
        if (status == OrderStatus.CANCELLED) {
            throw new IllegalStateException("Bekor qilingan buyurtma o'zgarmaydi");
        }
        total = total.add(item.getLineTotal());
    }
}
```

Amaliy qoida oddiy: coverage exclusion ni paket nomiga emas, mantiq mavjudligiga bog'lang. Agar `**/dto/**` naqshini yozsangiz, keyin kimdir o'sha paketga validatsiya yoki hisob-kitob qo'shsa, u avtomatik ravishda nazoratdan chiqadi. Xavfsizroq yo'l: DTO larni `record` qilish va mantiqni servis qatlamiga chiqarish. Shunda exclusion naqshi tabiiy ravishda faqat mantiqsiz turlarni qamrab oladi.

Konfiguratsiya klasslari uchun vaziyat biroz boshqacha. `@Configuration` klassidagi `@Bean` metodini unit test qilish Spring kontekstini qayta yozishga teng va bu ortiqcha ish. Lekin kontekst haqiqatan ko'tarilishini bitta integratsion test tekshirishi shart. Shu testning qanday yozilishi [testlash qo'llanmasidagi](../testing/README.md) Spring Boot test slice lari mavzusida bor.

## 12.5 Migratsiya skriptlari va qolip (template) fayllari

Flyway yoki Liquibase migratsiyalari Java tahlilining predmeti emas, shuning uchun ular `sonar.sources` ga tushsa ham Java qoidalari ularga tegmaydi. Muammo boshqa joyda: migratsiya skripti o'zgarmas artefakt. U bir marta ishlab, keyin faqat tarix bo'lib qoladi. Shu sababli migratsiya papkasini duplication dan chiqarish mantiqiy, chunki ketma-ket skriptlar bir-biriga tabiiy o'xshaydi.

```sql
-- V12__order_payment_status.sql: ishlab ketgan migratsiya, endi o'zgarmaydi
-- Duplication dan chiqarilgan, chunki V11 bilan struktura o'xshash.
-- Lekin mazmuni integratsion test bilan tekshirilgan.
ALTER TABLE orders
    ADD COLUMN payment_status VARCHAR(32) NOT NULL DEFAULT 'PENDING';

-- Mavjud qatorlarni to'lov jurnalidan to'ldirish
UPDATE orders o
SET payment_status = 'PAID'
WHERE EXISTS (
    SELECT 1 FROM payments p
    WHERE p.order_id = o.id AND p.state = 'SETTLED'
);

-- Indeks: hisobot so'rovi status bo'yicha filtrlaydi
CREATE INDEX idx_orders_payment_status ON orders (payment_status);
```

Qolip fayllari, ya'ni Thymeleaf shablonlari, HTML parchalari, `freemarker` fayllari, o'z qoidalar to'plamiga ega. Agar jamoada frontend uchun alohida linter bor bo'lsa, bu fayllarni Sonar tahlilidan chiqarish takrorlanishni kamaytiradi. Lekin bu qarorni yozib qo'yish kerak, aks holda keyin "nega template da XSS tekshirilmadi" degan savol javobsiz qoladi.

Migratsiya skriptining mazmuni esa albatta testlanishi kerak. Yuqoridagi `UPDATE` noto'g'ri yozilsa, baza buzuladi va Sonar bu haqda hech narsa aytmaydi. Haqiqiy baza ustida migratsiyani ishlatib tekshirish yo'li [testlash qo'llanmasidagi](../testing/README.md) Testcontainers mavzusida tasvirlangan.

## 12.6 `@Generated` annotatsiyasi va JaCoCo ning unga munosabati

JaCoCo 0.8.2 dan boshlab filtr mexanizmiga ega. U nomi `Generated` so'zini o'z ichiga olgan annotatsiya bilan belgilangan klass va metodlarni coverage hisobidan chiqaradi. Bu juda qulay, chunki konfiguratsiya fayliga naqsh yozish kerak emas, belgi kodning o'zida turadi.

Lekin bitta shart bor va u ko'pchilikni chalg'itadi: annotatsiyaning retention i `CLASS` yoki `RUNTIME` bo'lishi kerak. `javax.annotation.processing.Generated` retention i `SOURCE`, shuning uchun u bytecode ga tushmaydi va JaCoCo uni mutlaqo ko'rmaydi. Lombok ning `lombok.Generated` annotatsiyasi esa `CLASS` retention bilan keladi va ishlaydi.

```java
// Loyiha ildizidagi lombok.config fayliga:
//   lombok.addLombokGeneratedAnnotation = true
// Shundan keyin @Data dan chiqqan getter coverage da hisoblanmaydi.

// O'z generatoringiz bo'lsa, retention ni to'g'ri tanlang
@Retention(RetentionPolicy.CLASS)   // SOURCE bo'lsa JaCoCo ko'rmaydi
@Target({ElementType.TYPE, ElementType.METHOD})
public @interface Generated { }

// Generator chiqargan klass shu belgini oladi
@Generated
public final class OrderMapperImpl implements OrderMapper {
    @Override
    public OrderDto toDto(Order order) {
        return new OrderDto(order.getId(), order.getTotal());
    }
}
```

SonarQube ning o'zi bu annotatsiyani exclusion sifatida qabul qilmaydi. Ya'ni coverage JaCoCo tomonidan filtrlanadi, lekin code smell lar baribir ko'rinishi mumkin. Shuning uchun generatsiya qilingan kod uchun ikki qatlam kerak: JaCoCo filtri coverage uchun va `sonar.exclusions` yoki `sonar.cpd.exclusions` issue lar uchun. Lombok holatida qo'shimcha nuqta bor: Lombok yaratgan metodlar manba kodida yo'q, shuning uchun Sonar ularda issue ochmaydi.

## 12.7 Kod ichida bostirish: `@SuppressWarnings` va Sonar ning maxsus izohi

Kod ichida bostirishning ikki yo'li bor. Birinchisi `@SuppressWarnings("java:SXXXX")`: aniq qoida kalitini ko'rsatadi, faqat shu element uchun ishlaydi va IDE da ham ko'rinadi. Ikkinchisi satr oxiriga qo'yiladigan `// NOSONAR` izohi: u o'sha satrdagi barcha issue larni o'chiradi va aynan shu kengligi uchun xavfli.

```java
public class PaymentGatewayClient {

    // To'g'ri usul: aniq qoida kaliti va sababi yonida
    // Reflection bu yerda shart, chunki gateway SDK si public API bermaydi.
    // Jira: PAY-1841. Qayta ko'rish: SDK 4.x chiqqanda olib tashlanadi.
    @SuppressWarnings("java:S3011")
    private void forceAccessible(Field field) {
        field.setAccessible(true);
    }

    // YOMON usul: NOSONAR barcha qoidani o'chiradi, sabab yo'q
    public BigDecimal parse(String raw) {
        return new BigDecimal(raw); // NOSONAR
    }

    // YAXSHI: muammoni bostirish emas, hal qilish
    public BigDecimal parseSafely(String raw) {
        try {
            return new BigDecimal(raw);
        } catch (NumberFormatException e) {
            // Noto'g'ri format biznes xatosi, texnik xato emas
            throw new InvalidAmountException("Summa formati noto'g'ri: " + raw, e);
        }
    }
}
```

`@SuppressWarnings` ning ustunligi shundaki, u versiya nazoratida ko'rinadi va kod review da muhokama qilinadi. Konfiguratsiya faylidagi exclusion esa bir marta yoziladi, keyin hamma uni unutadi. Shu sababli tor doirali bostirish uchun annotatsiya deyarli har doim konfiguratsiyadan yaxshiroq.

NOSONAR ning yana bir xususiyati bor: Sonar uning ishlatilishini kuzatuvchi qoidaga ega va bu qoidani profilda yoqib qo'yish mumkin. Shunda har bir NOSONAR o'zi issue sifatida ko'rinadi va jim qolmaydi. Agar jamoa NOSONAR ni umuman taqiqlashni xohlasa, bu qoidani blocker darajasiga ko'tarish eng sodda yechim.

## 12.8 Bostirishni majburan asoslash: izoh talab qilish qoidasi

Asoslanmagan bostirish texnik qarzni yashiradi, shuning uchun jamoa darajasida bitta mexanik qoida kiritish kerak: har bir bostirish yonida sabab, egasi va muddati bo'lishi shart. Buni odamning yaxshi niyatiga qoldirmang, CI da tekshiring. Grep darajasidagi tekshiruv ham yetarli natija beradi.

```bash
#!/usr/bin/env bash
# scripts/check-suppressions.sh: asoslanmagan bostirishni topadi
set -euo pipefail

# Har bir NOSONAR satridan oldin izoh borligini talab qilamiz
bad=$(grep -rn --include="*.java" "NOSONAR" src/main \
  | grep -v "NOSONAR \[" || true)

if [ -n "$bad" ]; then
  echo "Asoslanmagan NOSONAR topildi. Format: // NOSONAR [PAY-123: sabab]"
  echo "$bad"
  exit 1
fi

# Bostirish sonini kuzatish: o'sib borsa, review da savol bo'ladi
grep -rc --include="*.java" "@SuppressWarnings(\"java:" src/main \
  | awk -F: '{s+=$2} END {print "Bostirish soni:", s+0}' 
```

Bu skriptni pipeline ning lint bosqichiga qo'ying. Natijada bostirish qo'shish mumkin, lekin arzon emas: muallif sabab yozishi va tiket ochishi kerak. Amalda shu kichik to'siq bostirish sonini sezilarli kamaytiradi, chunki ko'p holatda muammoni tuzatish sabab yozishdan oson bo'lib chiqadi.

## 12.9 Aldov belgilari: butun paketni chiqarish, murakkab klassni chiqarish

Aldovni tanib olish uchun bitta savol yetarli: "Bu exclusion olib tashlansa, qaysi issue qaytib keladi, va u haqiqiy muammomi?" Agar javob "bizning asosiy to'lov hisoblash klassidagi cognitive complexity" bo'lsa, bu exclusion emas, yashirish. Agar javob "generatorning uzun switch i" bo'lsa, bu o'rinli.

| Halol exclusion | Aldov exclusion |
|---|---|
| `target/generated-sources/**` tahlildan chiqarilgan | `**/service/**` tahlildan chiqarilgan |
| `**/*MapperImpl.java` MapStruct chiqargani uchun | `PaymentCalculator.java` testi qiyin bo'lgani uchun |
| `**/config/*Config.java` coverage dan chiqarilgan | `**/*Service.java` coverage dan chiqarilgan |
| `java:S1192` faqat test fixture faylida o'chirilgan | `java:S3776` butun loyihada o'chirilgan |
| Migratsiya papkasi duplication dan chiqarilgan | Domen paketi duplication dan chiqarilgan |
| `@SuppressWarnings` bitta metodda, Jira kaliti bilan | Klass ustida `@SuppressWarnings("all")` |
| Exclusion sababi va egasi hujjatda bor | Exclusion kim va qachon qo'shganini hech kim bilmaydi |
| Gate yashil bo'ldi, chunki test yozildi | Gate yashil bo'ldi, chunki maxraj kichraydi |

Uchta eng xavfli naqsh borki, ularni review da avtomatik rad etish kerak. Birinchisi `**/*Service.java` yoki `**/*Impl.java` kabi butun qatlamni qamrab oluvchi naqsh. Ikkinchisi global qoida o'chirish, ya'ni `resourceKey` o'rniga `**/*` yozish. Uchinchisi gate tushgandan keyin bir soat ichida qo'shilgan har qanday exclusion, chunki uning motivi texnik emas, muddatga bog'liq.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Coverage ni ko'tarish uchun `sonar.exclusions` ishlatish | Maxraj kichrayadi, sifat o'zgarmaydi | `coverage.exclusions` dan foydalanish yoki test yozish |
| `**/dto/**` coverage dan chiqarish | Keyin DTO ga qo'shilgan mantiq nazoratsiz qoladi | Mantiqni servisga chiqarish, DTO ni `record` qilish |
| `javax.annotation.processing.Generated` ga ishonish | Retention `SOURCE`, JaCoCo filtrlamaydi | `CLASS` retention li annotatsiya yoki Lombok konfiguratsiyasi |
| Satr oxirida sabab yozilmagan `// NOSONAR` | Qaysi muammo yashirilgani bilinmaydi | Formatni CI da majburlash, NOSONAR qoidasini yoqish |
| Exclusion ni faqat lokal `sonar-project.properties` da saqlash | Server tomonidagi sozlama bilan ziddiyat | Bitta manba: repozitoriydagi fayl, serverda bo'sh |
| Gradle va Maven da turlicha exclusion | Lokal va CI natijasi mos kelmaydi | Sozlamani bitta joyda, build fayliga ko'chirish |
| Exclusion naqshi juda keng, masalan `**/*Util*` | Tasodifiy fayllar ham chiqib ketadi | Naqshni fayl nomiga aniqlashtirish |
| Exclusion hech qachon olib tashlanmaydi | Yillar o'tib kod yarmi nazoratdan tashqarida | Har bir yozuvga amal qilish muddati qo'yish |

## 12.10 Exclusion ro'yxatini ko'rib chiqish tartibi va uni kim tasdiqlaydi

Exclusion ni oddiy kod o'zgarishi deb qarash xato, chunki u o'lchov tizimini o'zgartiradi. Shuning uchun uni qo'shish alohida tartibga ega bo'lishi kerak. Minimal tartib shunday: exclusion faqat alohida pull request da keladi, biznes kodi bilan birga emas. Bu review ni osonlashtiradi, chunki reviewer diff da faqat sozlamani ko'radi.

Tasdiqlovchi masalasi aniq bo'lishi kerak. Coverage va duplication exclusion ini texnik yetakchi tasdiqlashi yetarli. Tahlildan butunlay chiqarish va global qoida o'chirish esa arxitektor tasdig'ini talab qiladi, chunki bu quality gate ning ma'nosini o'zgartiradi. Security kategoriyasidagi qoidani o'chirish alohida holat va unga security mas'uli ham qo'shilishi kerak.

```yaml
# .github/workflows/sonar.yml dan parcha: exclusion o'zgarishini ajratib ushlash
name: sonar
on: [pull_request]
jobs:
  guard-exclusions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      # Exclusion sozlamasi o'zgargan bo'lsa, alohida egani talab qilamiz
      - name: Exclusion diff tekshiruvi
        run: |
          changed=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          if echo "$changed" | grep -qE 'sonar-project.properties|sonar-exclusions.yml'; then
            echo "Exclusion o'zgargan: arxitektor review i shart"
          fi
      - name: Tahlil
        run: ./mvnw -B verify sonar:sonar
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Davriy ko'rib chiqish ham kerak. Chorakda bir marta ro'yxatni ochib, har bir yozuv uchun uchta savolga javob bering: sababi hali ham kuchdami, egasi hali jamoadami, naqsh hali ham mavjud fayllarga mos keladimi. Mos kelmaydigan naqshlar eng xavfli, chunki ular jim turib keyin kutilmagan fayllarni qamrab oladi.

## 12.11 Exclusion siyosatini hujjatlashtirish namunasi

Konfiguratsiya fayli "nima" degan savolga javob beradi, lekin "nega" degan savolga javob bermaydi. Shu sababli har bir exclusion uchun strukturalangan yozuv saqlash kerak. Eng amaliy shakl: repozitoriyda yotgan YAML fayl, unda sabab, egasi, qatlam va amal qilish muddati bor.

```yaml
# docs/sonar-exclusions.yml: exclusion registri, review da o'qiladigan manba
policy:
  review_cycle: quarterly          # Chorakda bir marta ko'rib chiqiladi
  approver_full_exclusion: architect
  approver_coverage: tech_lead

entries:
  - pattern: "target/generated-sources/**/*"
    layer: analysis                # analysis | coverage | cpd | rule
    reason: "MapStruct va OpenAPI generatori chiqargan kod, odam yozmaydi"
    owner: "payments-team"
    added: 2025-02-11
    expires: never                 # Generator bor ekan, doimiy
  - pattern: "**/config/**/*Config.java"
    layer: coverage
    reason: "@Bean metodlari kontekst testida bilvosita tekshiriladi"
    owner: "a.karimov"
    expires: never
  - pattern: "**/report/LegacyReportBuilder.java"
    layer: coverage
    reason: "Eski hisobot moduli, 2026 Q2 da olib tashlanadi"
    owner: "d.yusupova"
    added: 2025-06-20
    expires: 2026-06-30            # Muddatdan keyin CI ogohlantiradi
    ticket: "REP-908"
```

`expires: never` qiymati faqat tabiatan o'zgarmas holatlar uchun, masalan generatsiya qilingan kod. Vaqtinchalik yon berishlar uchun aniq sana bo'lishi shart va CI shu sanani tekshirishi kerak. Muddati o'tgan yozuv build ni yiqitmasligi mumkin, lekin ogohlantirish berishi va chorakli review ro'yxatiga tushishi kerak.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Exclusion maqsadi | Gate ni yashil qilish | O'lchovni haqiqatga yaqinlashtirish |
| Qatlam tanlash | Darhol `sonar.exclusions` | Eng tor qatlamdan boshlash |
| Naqsh kengligi | Paket darajasida `**/service/**` | Fayl nomi darajasida aniq naqsh |
| Sabab | Diff da izohsiz qator | Registrda sabab, ega va muddat |
| Tasdiqlash | Muallif o'zi qo'shadi | Qatlamga qarab yetakchi yoki arxitektor |
| Bostirish shakli | Satr oxirida `// NOSONAR` | Aniq kalitli `@SuppressWarnings` va tiket |
| Generatsiya qilingan kod | Hamma narsani exclusion ga tiqish | JaCoCo filtri va kirish faylini tahlilda qoldirish |
| Davriylik | Bir marta yozilib unutiladi | Chorakli ko'rib chiqish va muddat nazorati |
| Coverage pasayganda | Exclusion naqshini kengaytirish | Yetishmayotgan test holatini yozish |
| CI nazorati | Hech qanday tekshiruv yo'q | Exclusion diff i va bostirish formati tekshiriladi |

## 12.12 Amalda qo'llash

- [ ] Loyihadagi barcha exclusion sozlamalarini bitta `sonar-project.properties` ga yig'ing va serverdagi dublikat sozlamalarni o'chiring.
- [ ] Har bir mavjud exclusion yonida qaysi qatlamga tegishli ekanini belgilang: tahlil, coverage, duplication yoki muayyan qoida.
- [ ] `sonar.exclusions` ichidagi har bir naqshni tekshirib, generatsiya qilinmagan kodni qamrab olganlarini `coverage.exclusions` ga ko'chiring yoki butunlay olib tashlang.
- [ ] `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'shib, JaCoCo hisobotida coverage farqini o'lchab ko'ring.
- [ ] `docs/sonar-exclusions.yml` registrini yarating: har bir yozuvda sabab, ega, sana va muddat bo'lsin.
- [ ] CI ga bostirish formatini tekshiradigan skript qo'shing va asoslanmagan `NOSONAR` uchun build ni yiqitadigan qiling.
- [ ] CODEOWNERS ga exclusion fayllarini kiritib, arxitektor review ini majburiy qilib qo'ying.
- [ ] Chorakli ko'rib chiqish uchun kalendarga takrorlanuvchi uchrashuv qo'yib, birinchi majlisda muddati o'tgan yozuvlar ro'yxatini chiqaring.

---

[&larr; 11. Qamralmay qoladigan kod va unga test yozish](11-qamralmay-qoladigan-kod-va-unga-test-yozish.md) · [Mundarija](README.md) · [13. Sonar o'tadigan kod yozish qoidalari &rarr;](13-sonar-otadigan-kod-yozish-qoidalari.md)
