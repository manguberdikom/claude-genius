# 2-bosqich: kod strukturasini analiz qilish

Maqsad - **xarita**, dump emas. Bosqich oxirida uch narsa bo'ladi: tuzilish
inventari, bog'liqlik yo'nalishi eskizi va `fayl:qator` ga bog'langan simptomlar
ro'yxati. Shu uchtasidan keyin pattern tanlashga haqli bo'lamiz.

Vaqt budjeti: kichik ish uchun 5-10 fayl, o'rta uchun o'zgaradigan modul to'liq,
katta uchun chegaralar va ularni kesib o'tuvchi oqimlar. Hamma kodni o'qish -
analiz emas, kechikish.

## Olti o'tish

### 1. Shakl: nima bor

```bash
git ls-files | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head -25
git ls-files '*.java' | wc -l
find . -name "*.java" -not -path "*/test/*" -exec wc -l {} + | sort -rn | head -15
```

Yoziladi: modullar, paketlar daraxti, eng katta fayllar, test/main nisbati.

### 2. Kirish nuqtalari: tashqaridan nima keladi

```bash
grep -rln "@RestController\|@Controller" src/main/java | head -20
grep -rn "@KafkaListener\|@RabbitListener\|@JmsListener" src/main/java | head
grep -rn "@Scheduled\|ApplicationRunner\|CommandLineRunner" src/main/java | head
grep -rn "@FeignClient\|RestTemplate\|WebClient" src/main/java | head
```

Yoziladi: HTTP endpointlar, consumerlar, scheduled ishlar, tashqi chaqiruvlar.
Har tashqi chaqiruv - keyinchalik timeout/retry/idempotentlik savoli.

### 3. Qatlamlar va bog'liqlik yo'nalishi

```bash
# controller to'g'ridan-to'g'ri repository ga tegyaptimi?
grep -rn "Repository" src/main/java --include="*Controller.java" | head
# domen paketidan infrastrukturaga import bormi?
grep -rnE --include='*.java' '^import (static )?([a-z0-9_]+\.)*(persistence|jpa|hibernate|kafka|redis|web)\.' \
  src/main/java | grep '/domain/' | head -20
# entity tashqariga chiqyaptimi (controller qaytaradigan tur)?
grep -rn "@Entity" src/main/java | wc -l
```

Yoziladi: qatlamlar ro'yxati, ruxsat etilgan yo'nalish va uni buzgan joylar.
Buzilgan har yo'nalish - alohida simptom qatori.

### 4. Ma'lumot yo'li: so'rovdan jadvalgacha

Bitta vakil oqim tanlanadi (eng muhim endpoint) va uchidan uchiga kuzatiladi:
controller -> service -> repository -> SQL -> jadval/indeks. Yo'lda yoziladi:

- tranzaksiya qayerda boshlanadi va tugaydi (`@Transactional` qayerda turgan)
- nechta DB chaqiruvi bo'ladi (N+1 belgisi: loop ichida repository chaqiruvi)
- lazy/eager munosabatlar va DTO ga qaysi joyda o'tiladi
- tranzaksiya ichida tashqi HTTP/Kafka chaqiruvi bormi (eng ko'p uchraydigan xato)

```bash
grep -rn "@Transactional" src/main/java | head -30
grep -rn "FetchType.EAGER\|@OneToMany\|@ManyToOne" src/main/java | head -20
```

### 5. Issiq nuqtalar: qayerda og'riq bor

```bash
# eng ko'p o'zgargan fayllar (churn) - muammo shu yerda yashaydi
git log --since="12 months ago" --name-only --pretty=format: -- '*.java' \
  | grep . | sort | uniq -c | sort -rn | head -15
# eng ko'p mualliflik qilingan / eng uzun metodlar taxmini
grep -rn "if \|else\|switch\|case \|&&\|||" src/main/java --include="*.java" -c \
  | sort -t: -k2 -rn | head -10
```

Churn yuqori + fayl katta + test yo'q = rejaning birinchi nishoni.

### 6. Test haqiqati

```bash
git ls-files '*Test.java' '*Tests.java' '*IT.java' | wc -l
grep -rln "@SpringBootTest" src/test | wc -l      # ko'p bo'lsa - sekin pipeline
grep -rln "Mockito\|@Mock" src/test | wc -l
grep -rn "@Disabled\|@Ignore" src/test | head
ls target/site/jacoco/index.html 2>/dev/null && echo "coverage hisoboti bor"
```

Yoziladi: test turlari nisbati, o'chirilgan testlar, coverage hisoboti bormi,
o'zgaradigan kod testlar bilan qamralganmi (bu refaktoring xavfini belgilaydi).

## Simptom yozish formati

Har simptom bitta qator, uchta majburiy bo'lagi bor: joy, nima ko'rindi, nega
muhim.

```
`OrderService.java:142-198` - bitta metodda 6 ta `if (type == ...)` tarmog'i;
har yangi to'lov turi uchta joyni o'zgartirishni talab qiladi.
```

Taqiq: "kod sifatsiz", "arxitektura yaxshi emas", "ko'p joyda muammo bor" -
bular simptom emas, taassurot.

## Simptomdan qo'llanmaga xarita

| Kodda ko'rinadigan narsa | Qarash kerak (hujjat: mavzu) |
|---|---|
| Bitta sinf hamma ishni qiladi (1000+ qator, 20+ dependency) | patternlar: `God Object`, `Dizayn printsiplari` (SRP) |
| Entity faqat getter/setter, logika servicelarda | patternlar: `Anemic Domain Model`, `Aggregate & Aggregate Root` |
| Loop ichida repository chaqiruvi, sekin ro'yxat | patternlar: `N+1 Problem Solutions`, `N+1 Queries`; arxitektor: `Spring Data JPA va Hibernate chuqur` |
| `open-in-view: true` yoki view da lazy load | patternlar: `Open Session in View`; arxitektor: `Spring Data JPA va Hibernate chuqur` |
| `ApplicationContext.getBean(...)` kod ichida | patternlar: `Service Locator` (Service Locator) |
| `new` operatori hamma joyda, test qilib bo'lmaydi | patternlar: `Factory Method` / `Abstract Factory` |
| Konstruktorda 8 parametr, yarmi optional | patternlar: `Builder, Step Builder, Lombok @Builder` (Builder) |
| Tranzaksiya ichida HTTP yoki Kafka chaqiruvi | patternlar: `Transactional Outbox`, `Dual Write Problem`; arxitektor: `Spring tranzaksiyalari va ularning chegaralari` |
| Bir xil kod ikki-uch servisda takrorlangan | sonarqube: `Cognitive complexity va takrorlanishni kamaytirish`; patternlar: `Dizayn printsiplari` |
| Timeout va retry yo'q tashqi chaqiruv | patternlar: `Retry` / `Circuit Breaker` / `Bulkhead`; arxitektor: `Tarmoq, timeout va integratsiya haqiqati` |
| Kesh bor, lekin invalidatsiya yo'q | patternlar: `Keshlash patternlari`; arxitektor: `Keshlash amaliyoti` |
| `catch (Exception e) {}` yoki log qilib yutib yuborish | sonarqube: `Xato katalogi: reliability (bug) toifasi` (reliability katalogi) |
| String concat bilan SQL | sonarqube: `Xato katalogi: security (vulnerability va hotspot)`, `Taint analysis mexanikasi` |
| Statik mutable holat, singleton ichida mutable maydon | patternlar: `Singleton abuse / Static Cling` / `Mutable State in Singleton Beans` |
| Paketlar orasida tsikl | arxitektor: `Abstraksiya hissi, bog'liqlik va chegaralar`; testlash: `Arxitektura testlari va kod sifati darvozalari` (ArchUnit) |
| Metodda cognitive complexity yuqori | sonarqube: `Cognitive complexity va takrorlanishni kamaytirish` |
| Test yo'q, lekin kod o'zgaradi | arxitektor: `Legacy kod va bosqichma-bosqich refaktoring` (legacy, seam topish) |

## Chegaralar va tsikllar

Paketlar orasidagi tsikl rejaning yo'nalishini o'zgartiradi: avval tsikl
uziladi, keyin funksiya qo'shiladi. Oddiy tekshiruv:

```bash
# A paketi B ga, B paketi A ga import qilyaptimi
grep -rn "^import com.example.billing" src/main/java/com/example/order/ | head
grep -rn "^import com.example.order"   src/main/java/com/example/billing/ | head
```

Agar loyihada ArchUnit testlari bo'lsa (`testlash: `Arxitektura testlari va kod sifati darvozalari``), ularning qoidalari
reja uchun qattiq cheklov - yangi kod ularni buzmasligi kerak.

## Bosqich artefakti

Rejaga ko'chiriladigan uch blok:

1. **Inventar:** modul/paket -> mas'uliyat -> o'zgaradimi (ha/yo'q)
2. **Bog'liqlik eskizi:** matnli ko'rinish, masalan
   `web -> application -> domain <- infrastructure (adapter)`; buzilgan
   yo'nalishlar `!` bilan belgilanadi
3. **Simptomlar jadvali:** `joy | simptom | nega muhim | qo'llanmadagi mavzu`

## Bosqich tugaganini qanday bilamiz

- O'zgaradigan har fayl o'qilgan (nafaqat nomidan taxmin qilingan)
- Har simptomda `fayl:qator` bor
- Bitta oqim uchidan uchiga kuzatilgan (tranzaksiya chegarasi aniq)
- O'zgaradigan kodning test qamrovi holati ma'lum
