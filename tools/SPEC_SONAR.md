# Bob yozish spetsifikatsiyasi: SonarQube hujjati

Hujjat: "SonarQube: qanday ishlaydi va qanday kod bilan test undan o'tadi".
Auditoriya: Java/Spring developer, texnik yetakchi va arxitektor.
Til: O'ZBEK LOTIN YOZUVI. Kirill yoki rus tili MUTLAQO bo'lmasin.
Texnik atamalar inglizcha qoladi: quality gate, coverage, code smell, issue, rule.

## Bu hujjat qaysi o'rinni egallaydi (TAKRORLANMASLIK QOIDASI)

To'plamda uchta hujjat bor:
1. `java-spring-design-patterns.md` - 1007 dizayn pattern katalogi.
2. `java-spring-testing-handbook.md` - testlashning butun sohasi: test piramidasi,
   unit va integratsion test, Testcontainers, contract testing, test ma'lumotlari,
   E2E, performance test, ArchUnit, CI/CD test pipeline, flaky testlar, metrikalar.
3. `java-spring-architect-mindset.md` - JVM, Spring, PostgreSQL mexanikasi va qaror.

SHUNING UCHUN SEN:
- Test yozish asoslarini (JUnit 5 nima, Mockito qanday ishlaydi, test piramidasi)
  TUSHUNTIRMA. Ular testlash qo'llanmasida. Bu yerda faqat "Sonar shu qoidani
  qanday o'lchaydi va uni qondirish uchun test qanday bo'lishi kerak" darajasi.
- Dizayn pattern katalogini yozma.
- Bu hujjatning o'z ulushi: SONAR MEXANIKASI. Ya'ni Sonar nimani, qanday
  hisoblaydi, qaysi qoida qachon ishga tushadi, quality gate shartlari qanday
  tekshiriladi, va shu bilimdan kelib chiqib kod bilan testni qanday yozish.
- Boshqa hujjatga kerak bo'lsa mavzu nomi bilan havola qil: "testlash
  qo'llanmasidagi Testcontainers mavzusi". Bob RAQAMI bilan EMAS.

## Halollik talabi (muhim)

Foydalanuvchi "100% o'tadigan kod" so'ragan. Yolg'on va'da berma:
- Quality gate shartlari har loyihada boshqacha sozlanadi. "Har doim o'tadigan"
  universal retsept yo'q. Aniq shart va uni qondirish yo'lini ko'rsat.
- 100% coverage sifatni kafolatlamaydi. Qayerda bu raqam aldashini ham yoz.
- Qoida nomini va kalitini (masalan `java:S3776`) faqat ishonching komil bo'lsa yoz.
  Ishonching bo'lmasa, qoidaning mazmunini tasvirla, kalitni O'YLAB CHIQARMA.

## Format (qat'iy, buzilmasin)

- Hech qanday `#` yoki `##` sarlavha YOZMA. Faqat `### ` kichik sarlavhalar, RAQAMSIZ.
- Boshida 2-4 gapli kirish paragrafi (sarlavhasiz).
- Kod bloklari: kamida 6 ta. `java`, `xml`, `yaml`, `bash`, `properties`, `sql`.
  Har bir blok 28 qatordan oshmasin. Kod ichida izoh o'zbekcha bo'lsin.
- Kamida 2 ta Markdown jadval. Ulardan biri AYNAN shunday taqqoslash bo'lsin:
  "oddiy yondashuv" va "arxitektor yondashuvi" ustunlari, kamida 8 qator.
  Texnik boblarda yana bitta "tuzoq va yechim" jadvali bo'lsin.
- Oxirgi bo'lim AYNAN shunday nomlansin: `### Amalda qo'llash`
  Ichida 5-8 ta `- [ ] ` bandi, har biri bajariladigan aniq ish.
- Hajm: 2000-2700 so'z.

## Mazmun sifati

- "Yomon kod" va "Sonar o'tadigan kod" juftligini ko'p ishlat. Avval Sonar nima
  deb shikoyat qiladi, keyin tuzatilgan variant.
- Aniq, hayotiy misollar: to'lov servisi, buyurtma, ombor qoldig'i, hisobot.
- Faktik aniq bo'l: Java 17-25, Spring Boot 3.x, JaCoCo 0.8.x, SonarQube 9.9 LTA
  va 2025 LTA liniyasi, sonar-maven-plugin, Gradle sonarqube plugin.
- Versiyaga bog'liq narsani "versiyaga qarab farq qiladi" deb ayt, aniq
  bilmasang raqam to'qima.
- Har gapda bitta fikr. Em-dash ishlatma.

## Tezlik

Butun faylni BITTA tool chaqiruvi bilan yoz: `cat > "<path>" <<'EOF' ... EOF`.
Bu SPEC dan boshqa hech qanday faylni o'qima. Veb qidiruv qilma.
Oxirida faqat fayl yo'li va `### ` bo'limlar sonini qaytar.

## Katalog boblari uchun qo'shimcha talab (VII qism)

Katalog bobi boshqacha tuzilgan. Unda:
- Boshida bitta katta jadval: ustunlar `Kod namunasi` yoki `Holat`, `Sonar nima deydi`,
  `Toifa`, `Jiddiylik`, `Ta'siri`. Kamida 12 qator.
- Keyin har bir muhim holat alohida `### ` bo'lim: avval SHIKOYAT QILINADIGAN kod,
  keyin Sonar nima uchun shikoyat qilishi, keyin TUZATILGAN kod, keyin bir gapli tavsiya.
- Toifani aniq ayt: reliability (bug), security (vulnerability yoki hotspot),
  maintainability (code smell). Jiddiylikni ham ayt, lekin "taxminan" deb belgila,
  chunki u profilga qarab o'zgaradi.
- Qoida kalitini (masalan `java:S2259`) faqat ishonching komil bo'lsa yoz. Aks holda
  faqat qoidaning mazmunini tasvirla.
