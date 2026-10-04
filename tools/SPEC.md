# Bob yozish spetsifikatsiyasi (hamma agentlar uchun bir xil)

Hujjat: "Kod yozadigan arxitektorning miyyasi: Java, Spring, PostgreSQL".
Auditoriya: senior Java/Spring developer va arxitektor.
Til: O'ZBEK LOTIN YOZUVI. Kirill yoki rus tili MUTLAQO bo'lmasin.
Texnik atamalar inglizcha qoladi: bean, proxy, thread, cache, latency, planner, WAL.

## Bu hujjat qaysi o'rinni egallaydi (TAKRORLANMASLIK QOIDASI)

Bu hujjat uchlikning bir qismi. Qolgan ikkitasi allaqachon yozilgan:

1. `java-spring-design-patterns.md` — 1007 ta dizayn pattern, 30 bo'lim:
   GoF patternlari, concurrency patternlari, Spring Core patternlari, web va API
   patternlari, service va ORM patternlari, caching patternlari, DDD, microservices,
   Enterprise Integration Patterns, resilience va cloud patternlari, security
   patternlari, reactive, batch, observability patternlari, deployment patternlari,
   testing patternlari, anti-patternlar, SOLID va GRASP, monolitdan microservice'ga
   migratsiya, taqsimlangan ma'lumot, Kubernetes patternlari, Spring AI.

2. `java-spring-testing-handbook.md` — testlashning butun sohasi, 18 bob:
   test piramidasi, QA jarayoni, unit test, Spring slice testlari, Testcontainers,
   contract testing, test ma'lumotlari, xavfsizlik/tranzaksiya/async testlari,
   E2E va UI, performance va resilience testlari, ArchUnit va sifat darvozalari,
   CI/CD test pipeline, flaky testlar, test metrikalari, shablonlar.

SHUNING UCHUN SEN:
- Pattern ta'rifini va pattern katalogini YOZMA. Pattern nomini faqat qaror
  kontekstida tilga ol ("bu yerda outbox kerak bo'ladi"), uni tushuntirib o'tirma.
- Test yozish texnikasini (JUnit, Mockito, Testcontainers sozlash) TUSHUNTIRMA.
  Testlash faqat "arxitektor bu yerda nimani tekshirishi kerak" darajasida eslansin.
- Bu hujjatning o'z ulushi: MEXANIKA va QAROR. Ya'ni ichkarida nima sodir bo'ladi
  (JVM, Spring konteyner, Hibernate, PostgreSQL planner), raqamlar, sozlash
  parametrlari, tuzoqlar, va arxitektor shu bilimdan qanday qaror chiqaradi.
- Boshqa hujjatga kerak bo'lsa shunday havola qil: "dizayn patternlar hujjatidagi
  outbox pattern" yoki "testlash qo'llanmasidagi contract testing bo'limi".
  Bob RAQAMI bilan EMAS, faqat mavzu nomi bilan.

## Format (qat'iy, buzilmasin)

- Hech qanday `#` yoki `##` sarlavha YOZMA. Faqat `### ` kichik sarlavhalar, RAQAMSIZ.
- Boshida 2-4 gapli kirish paragrafi (sarlavhasiz).
- Kod bloklari: kamida 6 ta. `java`, `sql`, `yaml`, `bash` yoki `properties`.
  Har bir blok 28 qatordan oshmasin. Kod ichida izoh o'zbekcha bo'lsin.
- Kamida 2 ta Markdown jadval. Ulardan biri AYNAN shunday taqqoslash bo'lsin:
  "oddiy yondashuv" va "arxitektor yondashuvi" ustunlari, kamida 8 qator.
  Texnik boblarda yana bitta "tuzoq va yechim" jadvali bo'lsin.
- Oxirgi bo'lim AYNAN shunday nomlansin: `### Amalda qo'llash`
  Ichida 5-8 ta `- [ ] ` bandi, har biri bajariladigan aniq ish.
- Hajm: 2000-2700 so'z.

## Mazmun sifati

- Aniq, hayotiy misollar: to'lov servisi, buyurtma, hisobot, ombor qoldig'i.
  Mavhum "Foo/Bar" misollarini ishlatma.
- Faktik aniq bo'l: Java 17-25, Spring Boot 3.x/4.x, Spring Framework 6.x/7.x,
  Hibernate 6.x, PostgreSQL 15-17.
- MAVJUD BO'LMAGAN sinf, annotatsiya, flag yoki parametr nomini O'YLAB CHIQARMA.
  Ishonchsiz bo'lsang, nomni yozmay, mexanikani tushuntir.
- Raqam ber: kutilayotgan latency, xotira hajmi, pool kattaligi, timeout qiymati.
  Raqam taxminiy bo'lsa, "taxminan" deb yoz.
- Har gapda bitta fikr. Em-dash ishlatma.

## Tezlik

Butun faylni BITTA tool chaqiruvi bilan yoz: `cat > "<path>" <<'EOF' ... EOF`.
Bu SPEC dan boshqa hech qanday faylni o'qima. Veb qidiruv qilma.
Oxirida faqat fayl yo'li va `### ` bo'limlar sonini qaytar.
