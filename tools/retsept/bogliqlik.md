# bog'liqlik

Minimal shakl (code-review 33.2, clean-code 39.4):

```xml
<dependency>
  <groupId>org.postgresql</groupId>
  <artifactId>postgresql</artifactId>
  <scope>runtime</scope>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-test</artifactId>
  <scope>test</scope>
</dependency>
```

Allaqachon bor, yozmang:
- Har bog'liqlikka qo'lda `<version>` o'rniga Spring Boot BOM `spring-boot-dependencies` (`scope import`) versiyani boshqaradi (sonarqube 39.3)
- Zaif tranzitiv versiya uchun yangi to'g'ridan-to'g'ri bog'liqlik o'rniga BOM property yoki bitta `dependencyManagement` yozuvi (sonarqube 39.3)
- Bitta yordamchi metod uchun utility, collection yoki date kutubxonasi o'rniga JDK 17+ va Spring ning o'zi (sonarqube 39.11)

Tuzoqlar:
- Sababsiz qo'lda versiya BOM ni chetlab o'tadi va Boot ko'tarilganda versiyani orqaga surishi mumkin; kerak bo'lsa BOM property, izohda sabab va hozirgi BOM qiymati (code-review 33.2)
- `assertj` yoki `mockito` `compile` scope da qolsa production jar ga tushadi; test kutubxonasi faqat `test`, JDBC drayveri `runtime` (clean-code 39.4)
- Ikki BOM import qilinganda birinchisi g'olib, keyingisi kalitni almashtirmaydi; yangi BOM o'rnini ataylab tanlang (code-review 33.2)
