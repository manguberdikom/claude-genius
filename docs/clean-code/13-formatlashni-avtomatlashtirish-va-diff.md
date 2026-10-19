<!-- doc: clean-code | chapter: 13 | part: IV. Formatlash va kod uslubi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 13. Formatlashni avtomatlashtirish va diff gigiyenasi (Automated Formatting and Diff Hygiene)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [13.1 Bitta jamoa, bitta uslub: tanlov emas, sozlama](#131-bitta-jamoa-bitta-uslub-tanlov-emas-sozlama)
- [13.2 `.editorconfig` va IDE sozlamalarini repoda saqlash](#132-editorconfig-va-ide-sozlamalarini-repoda-saqlash)
- [13.3 Spotless va google-java-format o'rnatish](#133-spotless-va-google-java-format-ornatish)
- [13.4 Checkstyle qoidalari: faqat mashina tekshiradigani](#134-checkstyle-qoidalari-faqat-mashina-tekshiradigani)
- [13.5 Pre-commit va CI da formatlash tekshiruvi](#135-pre-commit-va-ci-da-formatlash-tekshiruvi)
- [13.6 Formatlash o'zgarishini mantiq o'zgarishidan ajratish](#136-formatlash-ozgarishini-mantiq-ozgarishidan-ajratish)
- [13.7 Katta formatlash commiti va `.git-blame-ignore-revs`](#137-katta-formatlash-commiti-va-git-blame-ignore-revs)
- [13.8 Generatsiya qilingan kodni formatlashdan chiqarish](#138-generatsiya-qilingan-kodni-formatlashdan-chiqarish)
- [13.9 Mavjud konvensiyaga moslash: When in Rome](#139-mavjud-konvensiyaga-moslash-when-in-rome)
- [13.10 Amalda qo'llash](#1310-amalda-qollash)

</details>


Formatlash haqidagi bahs code review vaqtining eng foydasiz qismi. Yechim oddiy: formatlashni mashinaga topshirish va bahsni butunlay yopish. Bu bobda shu sozlamaning aniq mexanikasi va formatlash o'zgarishlarini tarixni buzmaydigan qilib kiritish usullari.

## 13.1 Bitta jamoa, bitta uslub: tanlov emas, sozlama

Uslub tanlovida eng yaxshi variant yo'q, lekin eng yomon variant bor: har kimning o'z uslubi. Shu sababli qoida shunday: uslub bir marta tanlanadi, repoda sozlama sifatida saqlanadi va keyin muhokama qilinmaydi.

Amalda eng tez yo'l - tayyor uslubni olish va o'zgartirmaslik. google-java-format yoki Spring Java Format ikkisi ham to'liq, sozlanmaydigan (yoki kam sozlanadigan) va shu sababli bahsni yopadi. Sozlanadigan uslub tanlansa, jamoa oylar davomida qavs va bo'shliq haqida gaplashadi.

## 13.2 `.editorconfig` va IDE sozlamalarini repoda saqlash

`.editorconfig` barcha zamonaviy IDE tomonidan o'qiladi va eng arzon yechim: yangi odam repoyni ochadi va uning muharriri darhol to'g'ri sozlanadi.

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space

[*.java]
indent_size = 4
max_line_length = 100
# Wildcard import taqiqlangan (IntelliJ shu kalitni o'qiydi)
ij_java_class_count_to_use_import_on_demand = 999
ij_java_names_count_to_use_import_on_demand = 999

[*.{yml,yaml,json}]
indent_size = 2

[*.sql]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

## 13.3 Spotless va google-java-format o'rnatish

Spotless formatlashni build ning qismiga aylantiradi: `spotless:apply` tuzatadi, `spotless:check` CI da bloklaydi. Shu ikki buyruq formatlash haqidagi review izohlarini butunlay yo'qotadi.

```xml
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>2.46.1</version>
  <configuration>
    <java>
      <!-- Sozlanmaydigan formatter: uslub bahsi yopiladi -->
      <googleJavaFormat>
        <version>1.28.0</version>
        <style>AOSP</style>   <!-- AOSP = 4 bo'shliq indentatsiya -->
      </googleJavaFormat>
      <importOrder>
        <order>java,javax,jakarta,,org.springframework,uz.shop,\#</order>
      </importOrder>
      <removeUnusedImports/>
      <trimTrailingWhitespace/>
      <endWithNewline/>
      <licenseHeader>
        <content>/* Copyright (c) $YEAR Shop LLC. LICENSE faylini ko'ring. */</content>
      </licenseHeader>
    </java>
    <pom><sortPom/></pom>
    <sql><includes><include>src/main/resources/db/**/*.sql</include></includes></sql>
  </configuration>
  <executions>
    <execution>
      <!-- Har bir build da tekshiriladi: formatlash buzilgan kod merge bo'lmaydi -->
      <goals><goal>check</goal></goals>
      <phase>validate</phase>
    </execution>
  </executions>
</plugin>
```

Gradle da ekvivalenti `com.diffplug.spotless` plaginida bir xil tuzilishda yoziladi va `./gradlew spotlessApply` buyrug'i bilan ishlatiladi.

## 13.4 Checkstyle qoidalari: faqat mashina tekshiradigani

Checkstyle ning foydali qismi formatlash emas (uni Spotless qiladi), balki **uslub qoidalari**: nom shakllari, taqiqlangan konstruksiyalar, murakkablik chegaralari. Qoidalar ro'yxatini kichik va ma'noli ushlash kerak, aks holda jamoa `@SuppressWarnings` bilan to'ldiradi.

```xml
<module name="Checker">
  <module name="TreeWalker">
    <!-- Nomlash: 2-3 boblardagi qoidalarni majburlaydi -->
    <module name="MemberName">
      <property name="format" value="^[a-z][a-zA-Z0-9]*$"/>   <!-- m_ va _ taqiqlangan -->
    </module>
    <module name="ConstantName"/>
    <module name="TypeName"/>
    <module name="MethodName"/>

    <!-- Tuzilish -->
    <module name="NeedBraces"/>                    <!-- 4.8 -->
    <module name="AvoidStarImport"/>               <!-- 12.7 -->
    <module name="UnusedImports"/>
    <module name="EmptyCatchBlock">
      <property name="exceptionVariableName" value="expected|ignored"/>
    </module>
    <module name="EqualsHashCode"/>                <!-- 15.2 -->
    <module name="MissingSwitchDefault">
      <property name="severity" value="ignore"/>   <!-- 6.6: enum da default kerak emas -->
    </module>
    <module name="NestedIfDepth"><property name="max" value="2"/></module>
    <module name="BooleanExpressionComplexity"><property name="max" value="3"/></module>
    <module name="ParameterNumber"><property name="max" value="4"/></module>  <!-- 5.1 -->
    <module name="IllegalType">
      <property name="illegalClassNames" value="java.util.Date,java.util.Calendar"/>
    </module>
  </module>
  <module name="FileLength"><property name="max" value="500"/></module>  <!-- 11.1 -->
  <module name="NewlineAtEndOfFile"/>
</module>
```

## 13.5 Pre-commit va CI da formatlash tekshiruvi

Formatlash ikki joyda tekshiriladi: mahalliy (tez qaytish uchun) va CI da (kafolat uchun). Mahalliy hook ni majburiy qilmaslik kerak - u faqat qulaylik; kafolat CI da bo'ladi.

```bash
#!/bin/sh
# .githooks/pre-commit  (o'rnatish: git config core.hooksPath .githooks)
# Faqat o'zgargan Java fayllarini formatlaydi: butun repo emas, tez ishlaydi.
changed=$(git diff --cached --name-only --diff-filter=ACM | grep '\.java$')
[ -z "$changed" ] && exit 0

./mvnw -q spotless:apply -DspotlessFiles="$(echo "$changed" | paste -sd, -)" || exit 1
echo "$changed" | xargs git add
```

```yaml
# .github/workflows/build.yml dagi qadam
- name: Formatlash va uslub tekshiruvi
  run: ./mvnw -B spotless:check checkstyle:check
```

## 13.6 Formatlash o'zgarishini mantiq o'zgarishidan ajratish

Eng muhim diff qoidasi: bitta commit da ham formatlash, ham mantiq o'zgarmasligi kerak. Aks holda review da 400 qatorli diff ichida 3 qatorlik mantiq o'zgarishi ko'rinmay ketadi va xato o'tadi.

Amaliy tartib: avval mantiqni o'zgartirib commit qilish, keyin `spotless:apply` ni alohida commit qilish. Teskari tartib ham ishlaydi, muhimi - aralashtirmaslik. Review paytida esa `git diff -w` (bo'shliqlarni e'tiborsiz) bilan tekshirish mumkin.

```bash
# Review da formatlash shovqinini olib tashlab ko'rish
git diff -w --ignore-blank-lines HEAD~1

# PR da faqat mantiq o'zgargan fayllarni ajratish
git diff --stat HEAD~1 | sort -k3 -rn | head
```

## 13.7 Katta formatlash commiti va `.git-blame-ignore-revs`

Butun kod bazasini bir marta formatlash kerak bo'lganda (yangi formatter joriy qilinganda), u `git blame` ni buzadi: har bir qator shu commitga tegishli bo'lib qoladi. Git da bu muammoning rasmiy yechimi bor.

```bash
# 1) Formatlashni alohida commit qilish
./mvnw spotless:apply
git commit -am "Butun kod bazasini google-java-format (AOSP) ga keltirish"

# 2) Commit hash ini ro'yxatga qo'shish
git rev-parse HEAD >> .git-blame-ignore-revs
git commit -am "blame uchun e'tiborsiz qoldiriladigan revizlar ro'yxati"

# 3) Repo sozlamasiga ulash (har bir ishlab chiquvchi bir marta bajaradi)
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

GitHub `.git-blame-ignore-revs` faylini avtomatik o'qiydi, shuning uchun web interfeysdagi blame ham toza qoladi.

## 13.8 Generatsiya qilingan kodni formatlashdan chiqarish

Generatsiya qilingan kod (MapStruct, jOOQ, protobuf, Lombok delombok natijasi, OpenAPI klient) formatlanmaydi va tekshirilmaydi: u har build da qayta yaratiladi va uni tuzatish ma'nosiz.

```xml
<configuration>
  <java>
    <excludes>
      <exclude>target/generated-sources/**</exclude>
      <exclude>src/main/java/**/*MapperImpl.java</exclude>
    </excludes>
  </java>
</configuration>
```

Shu bilan birga, generatsiya qilingan kod `target/` ichida turishi va `git` ga tushmasligi kerak (39.6).

## 13.9 Mavjud konvensiyaga moslash: When in Rome

13.1-13.5 uslubni tanlash va uni mashinaga tekshirtirish haqida. Qolgan qism mashinaga tushmaydi: yangi faylga kirgan programmist shu fayldagi konvensiyani qanday topadi va "menda yaxshiroq g'oya bor" degan holatda nima qiladi.

Izchillik kognitiv kuch beradi: bir joyda bir narsa qanday qilinganini o'rgangan odam xuddi shu yondashuvni ishlatgan boshqa joyni darhol tushunadi. U xatoni ham kamaytiradi: izchil tizimda tanish ko'rinishga asoslangan taxmin to'g'ri bo'lib chiqadi, izchil bo'lmaganida esa bir xil ko'rinadigan ikki holat aslida boshqa bo'lib chiqadi (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 17-bob kirishi).

**When in Rome: atrofga qara.** Ousterhout eng muhim konvensiya deb shuni ataydi: yangi faylda ishlayotganda mavjud kod qanday tuzilganiga qarash kerak. Public a'zolar private lardan oldin e'lon qilinganmi, metodlar alifbo tartibidami, nomlar `camelCase` dami. Konvensiyaga o'xshagan har qanday narsa ko'rinsa, unga bo'ysuniladi. Dizayn qarori qilinayotganda esa savol beriladi: loyihada shunga o'xshash qaror allaqachon qilingan bo'lishi mumkinmi; mumkin bo'lsa, mavjud misol topiladi va yangi kodda xuddi shu yondashuv ishlatiladi (shu yerda, 17.2).

**Mavjud konvensiyani o'zgartirmaslik.** "Yaxshiroq g'oya" izchillikni buzish uchun yetarli sabab emas: yondashuvlar orasidagi farqning qiymati deyarli har doim izchillikning qiymatidan kichik. Ousterhout o'zgartirishdan oldin ikki savolga javob talab qiladi (shu yerda, 17.2):

1. Eski konvensiya o'rnatilganda mavjud bo'lmagan, sizning yondashuvingizni oqlaydigan muhim yangi ma'lumot bormi?
2. Yangi yondashuv shunchalik yaxshimi, eski ishlatishlarning HAMMASINI yangilashga vaqt sarflashga arziydimi?

Ikkisiga ham javob "ha" bo'lsa va jamoa shunga qo'shilsa, o'zgarish qilinadi va tugaganda eski konvensiyadan iz qolmasligi kerak. Shundan keyin ham xavf bor: boshqa programmistlar yangi konvensiyani bilmay, eski shaklni qaytarib kiritishi mumkin. Shuning uchun o'rnatilgan konvensiyani qayta ko'rib chiqish kamdan-kam hollarda vaqtning foydali sarfi bo'ladi.

```java
// mavjud konvensiya: value tur final, static factory `of`, tekshiruv
// private konstruktorda
public final class SettlementRow {
    private final PaymentId id;

    public static SettlementRow of(PaymentId id) {
        return new SettlementRow(id);
    }

    private SettlementRow(PaymentId id) {
        this.id = Objects.requireNonNull(id, "id");
    }
}

// yangi tur xuddi shu shaklda yoziladi. Builder yoki public konstruktor
// o'zicha yomon emas, lekin bu paketda u ikkinchi konvensiyani tug'diradi
public final class RefundRow {
    private final RefundId id;

    public static RefundRow of(RefundId id) {
        return new RefundRow(id);
    }

    private RefundRow(RefundId id) {
        this.id = Objects.requireNonNull(id, "id");
    }
}
```

**Izchillik ierarxik va "hammasi yoki hech narsa" emas.** Google ning uslub ko'rsatmalarida izchillik mahalliydan boshlanadi va shu tartibda ko'tariladi: **fayl ichidagi** norma, keyin **jamoa**, keyin **loyiha**, keyin butun kod bazasi. Yaqin doiradagi norma uzoqroq doiradagi normadan ustun turadi, va ko'rsatmalarning o'zida mahalliy konvensiyaga ataylab yo'l beradigan qoidalar bor: mahalliy izchillik ba'zi hollarda ilmiy jihatdan to'g'ri texnik tanlovdan afzal ko'riladi.

Ierarxiyaning tepasida yana bitta qatlam bor - **tashqi dunyo**. Konvensiya hamjamiyatda allaqachon mavjud bo'lsa, unga moslashish ma'qul. Google ning o'z misoli: Python kodi uchun boshida ikki bo'shliqli chekinish qabul qilingan edi, chunki o'sha paytdagi Python kodi asosan C++ loyihalariga xizmat qilardi va C++ kodi shunday formatlangan edi. Vaqt o'tib bu asos qulagan: Python yozadigan muhandis C++ dan ko'ra ko'proq Python kodini o'qiydi va yozadi, tashqi misolga qarash har safar qo'shimcha kuch talab qilgan, kodni ochiq manbaga chiqarish esa har marta ichki va tashqi shakllarni muvofiqlashtirishni talab qilgan. Starlark uchun ko'rsatma yozilganda tashqi dunyo bilan izchil bo'lish uchun to'rt bo'shliq tanlangan. Qoida: kichik, o'zi ichida yopiq va qisqa yashaydigan ish uchun ichki izchillik muhimroq; vaqt va masshtab o'yinga kirganda keng qabul qilingan standart o'zini oqlaydi.

**To'liq izchillik maqsad qilinmaydi.** Google ning C++ ko'rsatmasi bir vaqt eski kodni nomuvofiq qiladigan o'zgarishlardan voz kechishni va'da qilgan edi; kod bazasi o'sgach bu va'da olib tashlandi va C++ kod bazasi hech qachon to'liq izchil bo'lmasligi ochiq aytildi. Sabab narx: qoidalarni zamonaviy amaliyotga yangilash bir ish, shu qoidani yozilgan hamma kodga qo'llash butunlay boshqa ish, va u bir nuqtada qiymatidan qimmatroq bo'lib qoladi. Shuning uchun katta kod bazasida avtomatik o'zgarish vositalari eskini yangiga keltiradi (38-bob), lekin har burchakka yetib bormaydi va bu qabul qilinadi.

Shundan eng amaliy xulosa: muhim narsa **bitta javob borligi**, javobning o'zi emas. Chekinish bo'shliqlari soni yoki qator uzunligi chegarasi kabi qoidalarning qiymati tanlangan qiymatda emas, narsa faqat bitta usulda qilinishida. Shu sababli uslub bahsi "qaysi variant to'g'ri" dan "variant birmi" ga ko'chiriladi.

Qoidaning chegarasi ham bor: izchillik o'xshash narsalarni o'xshash qilishni talab qiladi va shu bilan birga o'xshamagan narsalarni boshqacha qilishni talab qiladi. O'xshamagan ikki narsani bitta shaklga tiqish (bir xil nom, mos kelmaydigan pattern) murakkablik va chalkashlik beradi; izchillik foyda beradigan shart - o'quvchi "x ga o'xshasa, demak u x" deb ishonishi (shu yerda, 17.3).

Bo'linish shunday: mashina tekshira oladigan qismi 13.4 va 13.5 ga, tekshira olmaydigani (e'lon tartibi, qaysi abstraksiya, qaysi pattern) review ga qoladi; review dagi talabchanlik qanchalik baland bo'lsa, jamoa konvensiyani shuncha tez o'rganadi (shu yerda, 17.2).

## 13.10 Amalda qo'llash

- [ ] `.editorconfig` faylini repoga qo'shib, kodirovka, indentatsiya va qator uzunligini belgilang.
- [ ] Spotless ni `googleJavaFormat` (yoki Spring Java Format) bilan o'rnatib, `validate` fazasida `check` qiling.
- [ ] Checkstyle qoidalarini 13.4 dagi ro'yxatdan boshlab kiritib, har bir qoidaning sababini hujjatlashtiring.
- [ ] `pre-commit` hook ni `.githooks/` da saqlab, `core.hooksPath` sozlamasini README ga yozing.
- [ ] Butun kod bazasini bir marta formatlab, alohida commit qiling va `.git-blame-ignore-revs` ga qo'shing.
- [ ] Generatsiya qilingan manbalarni formatlash va statik tahlildan chiqarib tashlang.
- [ ] "Formatlash va mantiq bir commitda bo'lmaydi" qoidasini jamoa kelishuviga kiriting.
- [ ] Review da formatlash haqidagi izohlarni taqiqlab, ularni CI xatosiga aylantiring.
- [ ] Mavjud konvensiyani o'zgartirish uchun ikki savol qoidasini (yangi ma'lumot bormi, hamma eski ishlatishni yangilashga arziydimi) jamoa kelishuviga kiriting (13.9).

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 8-bob ("Be Consistent", "Setting the Standard", "Changing the Rules") - izchillikning ierarxik tartibi (fayl, jamoa, loyiha, kod bazasi), mavjud tashqi konvensiyaga moslashishning afzalligi va Python chekinishi misoli, to'liq izchillikdan voz kechish qarori, hamda muhimi bitta javob borligi ekani. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- [Google Java Style Guide](https://raw.githubusercontent.com/google/styleguide/aee99aa581bd852c8a40814c1c8d0f8aa79a0ba2/javaguide.html) - formatlash qoidalarining mashina tekshiradigan qismi
- [SpotBugs, hujjat](https://raw.githubusercontent.com/spotbugs/spotbugs/6fc14ff38f4ebfbb4457caaa6df9a0ddd23a18c6/docs/index.rst) - CI da statik tahlilni qo'yish
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press,
  2018, 17-bob kirishi, 17.2, 17.3 - izchillikning kognitiv kuchi va xatoni
  kamaytirishi; "When in Rome" qoidasi; mavjud konvensiyani o'zgartirish
  uchun ikki savol va eski konvensiyadan iz qoldirmaslik talabi; review ning
  konvensiyani o'rgatishdagi roli; izchillikni o'xshamagan narsalarga
  majburlashning narxi

---

[&larr; 12. Gorizontal formatlash va kod uslubi](12-gorizontal-formatlash-va-kod-uslubi.md) · [Mundarija](README.md) · [14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya &rarr;](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md)
