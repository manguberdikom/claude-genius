<!-- doc: clean-code | chapter: 13 | part: IV. Formatlash va kod uslubi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 13. Formatlashni avtomatlashtirish va diff gigiyenasi (Automated Formatting and Diff Hygiene)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [13.1 Bitta jamoa, bitta uslub: tanlov emas, sozlama](#131-bitta-jamoa-bitta-uslub-tanlov-emas-sozlama)
- [13.2 `.editorconfig` va IDE sozlamalarini repoda saqlash](#132-editorconfig-va-ide-sozlamalarini-repoda-saqlash)
- [13.3 Spotless va google-java-format o'rnatish](#133-spotless-va-google-java-format-ornatish)
- [13.4 Checkstyle qoidalari: faqat mashina tekshiradigani](#134-checkstyle-qoidalari-faqat-mashina-tekshiradigani)
- [13.5 Pre-commit va CI da formatlash tekshiruvi](#135-pre-commit-va-ci-da-formatlash-tekshiruvi)
- [13.6 Formatlash o'zgarishini mantiq o'zgarishidan ajratish](#136-formatlash-ozgarishini-mantiq-ozgarishidan-ajratish)
- [13.7 Katta formatlash commiti va `.git-blame-ignore-revs`](#137-katta-formatlash-commiti-va-git-blame-ignore-revs)
- [13.8 Generatsiya qilingan kodni formatlashdan chiqarish](#138-generatsiya-qilingan-kodni-formatlashdan-chiqarish)
- [13.9 Amalda qo'llash](#139-amalda-qollash)

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

## 13.9 Amalda qo'llash

- [ ] `.editorconfig` faylini repoga qo'shib, kodirovka, indentatsiya va qator uzunligini belgilang.
- [ ] Spotless ni `googleJavaFormat` (yoki Spring Java Format) bilan o'rnatib, `validate` fazasida `check` qiling.
- [ ] Checkstyle qoidalarini 13.4 dagi ro'yxatdan boshlab kiritib, har bir qoidaning sababini hujjatlashtiring.
- [ ] `pre-commit` hook ni `.githooks/` da saqlab, `core.hooksPath` sozlamasini README ga yozing.
- [ ] Butun kod bazasini bir marta formatlab, alohida commit qiling va `.git-blame-ignore-revs` ga qo'shing.
- [ ] Generatsiya qilingan manbalarni formatlash va statik tahlildan chiqarib tashlang.
- [ ] "Formatlash va mantiq bir commitda bo'lmaydi" qoidasini jamoa kelishuviga kiriting.
- [ ] Review da formatlash haqidagi izohlarni taqiqlab, ularni CI xatosiga aylantiring.

---

[&larr; 12. Gorizontal formatlash va kod uslubi](12-gorizontal-formatlash-va-kod-uslubi.md) · [Mundarija](README.md) · [14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya &rarr;](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md)
