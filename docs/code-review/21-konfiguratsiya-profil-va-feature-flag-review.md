<!-- doc: code-review | chapter: 21 | part: IV. Spring kodini review qilish -->

[Kod review](../../README.md) / [Kod review](README.md)

# 21. Konfiguratsiya, profil va feature flag review (Configuration)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [21.1 Konfiguratsiya o'zgarishi uchun qo'shimcha savollar](#211-konfiguratsiya-ozgarishi-uchun-qoshimcha-savollar)
- [21.2 Timeout va retry juftligi](#212-timeout-va-retry-juftligi)
- [21.3 Secret va maxfiy qiymatlar](#213-secret-va-maxfiy-qiymatlar)
- [21.4 Profil bo'yicha xulq farqi](#214-profil-boyicha-xulq-farqi)
- [21.5 Tipli konfiguratsiya](#215-tipli-konfiguratsiya)
- [21.6 Feature flag: vaqtinchalik bo'lishi kerak](#216-feature-flag-vaqtinchalik-bolishi-kerak)
- [21.7 Actuator va diagnostika endpointlari](#217-actuator-va-diagnostika-endpointlari)
- [21.8 Muhitlar orasidagi farqni ko'rish](#218-muhitlar-orasidagi-farqni-korish)
- [21.9 Review checklisti: konfiguratsiya](#219-review-checklisti-konfiguratsiya)
- [21.10 Amalda qo'llash](#2110-amalda-qollash)

</details>


Konfiguratsiya o'zgarishi diffda eng kichik va eng xavfli o'zgarishlar sinfi: bitta raqam incidentga olib keladi, va u kod review da ko'pincha e'tiborsiz qoladi. Sababi psixologik - `application.yml` dagi uch qator kod emasga o'xshaydi. Amalda esa prod incidentlarining sezilarli qismi aynan konfiguratsiya o'zgarishidan kelib chiqadi.

## 21.1 Konfiguratsiya o'zgarishi uchun qo'shimcha savollar

| Savol | Nega |
| --- | --- |
| Bu qiymat qaysi muhitlarda o'zgaradi | Faqat dev da sinalgan sozlama prodda boshqacha ishlaydi |
| Qiymat nimaga asoslangan | "Kattaroq yaxshiroq" qarori odatda xato |
| Qiymat chegarasi bormi | Pool, timeout, batch - hammasi resursga bog'liq |
| Standart qiymat nima edi | Framework standarti ko'pincha o'ylangan |
| Qayta ishga tushirish kerakmi | Dinamik o'zgaradigan sozlamalar boshqa xavf |
| Ikki sozlama bir-biriga bog'liqmi | Timeout va retry, pool va thread |
| O'lchov bormi | Sozlama ta'sirini qanday ko'ramiz |

```yaml
# Review da shu diff ko'rinsa, har qatorga savol bor.
spring:
  datasource:
    hikari:
      maximum-pool-size: 100        # oldin 20 edi
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 1000          # oldin 50 edi
resilience4j:
  timelimiter:
    instances:
      payment:
        timeout-duration: 60s       # oldin 3s edi
```

Review izohi har bir qiymatning tizim darajasidagi oqibatini ko'rsatadi:

```text
blocker: maximum-pool-size 20 -> 100.

PostgreSQL da har bir ulanish alohida backend protsess (taxminan 5-10 MB).
Hozir 6 pod ishlayapti: 6 x 100 = 600 ulanish. PostgreSQL max_connections
hozir 200 (tekshirdim: SHOW max_connections). Deploy dan keyin yangi
podlar ulanish ola olmaydi va butun ilova "FATAL: too many connections"
beradi.

Bundan tashqari pool kattaligi throughput ni oshirmaydi: 100 parallel
so'rov 16 yadroli bazada bir-birini kutadi va p99 yomonlashadi.

Agar pool kamligi muammo bo'lsa, avval sababni aniqlaymiz: hozir
hikaricp_connections_pending metrikasi nolga teng, ya'ni pool kutish
yo'q. Muammo boshqa joyda bo'lishi mumkin (uzoq tranzaksiyalar, 19.6).

question: timeout-duration 3s -> 60s. To'lov provayderining p99 javobi
hozir 800 ms. 60 sekundlik timeout bilan bitta sekin javob 60 sekund
thread va DB ulanishini ushlaydi. Nega 3 sekund yetarli bo'lmadi?
```

## 21.2 Timeout va retry juftligi

Konfiguratsiyadagi eng ko'p uchraydigan xato - timeout va retry ni alohida sozlash. Ularning ko'paytmasi tizimning haqiqiy kutish vaqtini belgilaydi.

```yaml
# Xavfli kombinatsiya: hisob qilinmagan.
client:
  connect-timeout: 10s
  read-timeout: 30s
retry:
  max-attempts: 5
  wait-duration: 2s
# Eng yomon holat: 5 x (10 + 30) + 4 x 2 = 208 sekund.
# Yuqoridagi qatlamda HTTP timeout 30 sekund bo'lsa, foydalanuvchi
# allaqachon ketgan, lekin thread 208 sekund ushlanadi.
```

Review qoidasi: har bir chaqiruv zanjirida umumiy byudjet yuqoridan pastga kamayib borishi kerak. Agar tashqi so'rov uchun umumiy byudjet 3 sekund bo'lsa, ichki chaqiruvlar yig'indisi shundan kichik bo'lishi shart.

| Qatlam | Byudjet |
| --- | --- |
| Foydalanuvchi so'rovi (ingress) | 10 s |
| Ilova so'rov timeout i | 8 s |
| Tashqi servis chaqiruvi (barcha urinishlar bilan) | 3 s |
| Bitta urinish | 1 s |
| DB so'rovi | 2 s |

## 21.3 Secret va maxfiy qiymatlar

```yaml
# Kodda yoki repoda secret - blocker, hech qanday istisnosiz.
spring:
  datasource:
    password: Prod_P@ssw0rd_2026        # blocker
  mail:
    password: ${MAIL_PASSWORD}          # to'g'ri: muhitdan
app:
  jwt:
    secret: ${JWT_SECRET}               # to'g'ri
```

Review da secret topilganda tartib: (1) merge ni to'xtatish, (2) secret ni rotatsiya qilish - uni repodan o'chirish yetarli emas, chunki git tarixida qoladi va fork larda ham bo'lishi mumkin, (3) tarixdan tozalash, (4) skanerlashni CI ga qo'yish.

```bash
# Secret skanerlashni review dan oldin avtomatlashtirish.
# 1) Pre-commit hook: lokalda to'xtatadi.
cat > .pre-commit-config.yaml <<'EOP'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks: [ { id: gitleaks } ]
EOP

# 2) CI da butun tarixni skanerlash (bir marta) va har PR da diffni.
gitleaks detect --source . --redact --verbose
gitleaks protect --staged --redact

# 3) Tarixda qolgan secret ni topish: faqat diffda emas.
git log -p --all -S 'BEGIN RSA PRIVATE KEY' --oneline | head
git log -p --all -G 'password\s*[:=]\s*["'"'"'][^"'"'"']{8,}' --oneline | head
```

## 21.4 Profil bo'yicha xulq farqi

```java
// Xavfli naqsh: biznes xulqi profilga bog'liq.
@Service
@Profile("!prod")
public class FakePaymentGateway implements PaymentGateway { ... }

@Service
@Profile("prod")
public class RealPaymentGateway implements PaymentGateway { ... }
// Oqibati: test va staging da hech qachon haqiqiy integratsiya sinalmaydi.
// Prodda birinchi marta ishga tushadi - eng yomon joyda.

// Yaxshiroq: muhit konfiguratsiya bilan farqlanadi, kod bir xil.
// Staging da provayderning sandbox URL i ishlatiladi:
//   payment.base-url=https://sandbox.provider.io
// Prodda:
//   payment.base-url=https://api.provider.io
// Soxta implementatsiya esa faqat test paketida qoladi (@TestConfiguration).
```

Review savoli har bir `@Profile` uchun: bu profil xulq farqini yaratadimi yoki faqat manzil farqini. Birinchi holat xavfli, chunki prodda sinalmagan yo'l paydo bo'ladi.

## 21.5 Tipli konfiguratsiya

```java
// Naqsh: @Value tarqalgan, tekshiruv yo'q.
@Value("${payment.timeout:3000}") private int timeoutMillis;   // har joyda
@Value("${payment.retries}") private int retries;              // yo'q bo'lsa - ishga tushmaydi

// To'g'ri: bitta tipli obyekt, validatsiya bilan.
@ConfigurationProperties(prefix = "payment")
@Validated
public record PaymentProperties(
        @NotNull URI baseUrl,
        @NotNull @DurationMin(millis = 100) @DurationMax(seconds = 10) Duration timeout,
        @Min(0) @Max(5) int retries,
        @NotBlank String merchantId) { }
// Foydasi: (1) noto'g'ri qiymat ishga tushishda aniqlanadi, prodda emas;
// (2) hamma sozlama bir joyda ko'rinadi; (3) IDE va metadata bilan
// avtoto'ldirish; (4) testda oson qurish.
```

## 21.6 Feature flag: vaqtinchalik bo'lishi kerak

```java
// Naqsh: flag qo'shildi, o'chirish rejasi yo'q.
if (featureFlags.isEnabled("new-pricing")) {
    return newPricing.calculate(order);
} else {
    return oldPricing.calculate(order);
}
```

Review talablari har bir yangi flag uchun:

1. Egasi va o'chirish sanasi. Flag abadiy qolmasligi kerak - har bir flag ikki kod yo'lini jonli saqlaydi va testlash yukini ikki baravar oshiradi.
2. Standart qiymat. Konfiguratsiya yetib kelmasa, qaysi yo'l ishlaydi.
3. Qamrov: butun foydalanuvchilar uchunmi yoki bir qismi. Qism bo'lsa, taqsimlash barqarormi (bir foydalanuvchi har so'rovda boshqa yo'lga tushmasligi kerak).
4. Ikki yo'l ham test bilan qoplanganmi.

```java
// Flag ni hujjatlashtirish: kodda, konfiguratsiyada emas.
public enum FeatureFlag {
    /** Egasi: pricing-team. O'chirish: 2026-12-01. Tiket: PRC-412. */
    NEW_PRICING("new-pricing", LocalDate.of(2026, 12, 1)),
    /** Egasi: payments. O'chirish: 2026-11-15. Tiket: PAY-88. */
    IDEMPOTENT_CAPTURE("idempotent-capture", LocalDate.of(2026, 11, 15));

    private final String key;
    private final LocalDate removeBy;
}

// Muddati o'tgan flag larni test bilan aniqlash: CI da gapiradi.
@Test
void noExpiredFeatureFlags() {
    List<FeatureFlag> expired = Arrays.stream(FeatureFlag.values())
        .filter(f -> f.removeBy().isBefore(LocalDate.now()))
        .toList();
    assertThat(expired)
        .as("muddati o'tgan flag lar olib tashlanishi kerak")
        .isEmpty();
}
```

## 21.7 Actuator va diagnostika endpointlari

```yaml
# Xavfli: hamma narsa ochiq.
management:
  endpoints:
    web:
      exposure:
        include: "*"              # env, configprops, heapdump, threaddump!
```

Review izohi: `/actuator/env` va `/actuator/configprops` konfiguratsiya qiymatlarini, jumladan secret larni ko'rsatadi (maskalash to'liq emas); `/actuator/heapdump` butun xotirani fayl sifatida beradi - unda tokenlar va foydalanuvchi ma'lumotlari bo'ladi; `/actuator/threaddump` ichki tuzilishni oshkor qiladi.

```yaml
# To'g'ri: minimal ro'yxat, alohida port, himoyalangan.
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      show-details: when-authorized      # detallar faqat avtorizatsiya bilan
      probes:
        enabled: true                    # /health/liveness va /readiness
  server:
    port: 9090                           # ichki port, tashqariga chiqarilmaydi
  metrics:
    tags:
      application: ${spring.application.name}
```

## 21.8 Muhitlar orasidagi farqni ko'rish

```bash
# Review da konfiguratsiya farqini aniq ko'rish: qaysi qiymat qaysi muhitda.
for env in dev staging prod; do
  echo "=== $env ==="
  diff <(grep -vE '^\s*#|^\s*$' src/main/resources/application.yml) \
       <(grep -vE '^\s*#|^\s*$' src/main/resources/application-$env.yml) \
       | grep '^>' | head -20
done

# Prodda haqiqatda qanday qiymat ishlayotganini tekshirish (secret siz).
curl -s localhost:9090/actuator/configprops | jq '.contexts.application.beans
  | to_entries[] | select(.key | test("Hikari|Payment|Resilience"))
  | {key, properties: .value.properties}'

# K8s da env dan kelgan qiymatlar kodnikini bosib ketadi - ularni ham ko'rish.
kubectl get deploy order-service -o jsonpath='{.spec.template.spec.containers[0].env}' | jq
```

Oxirgi buyruq muhim: `application.yml` dagi qiymat prodda ishlamasligi mumkin, chunki Kubernetes env o'zgaruvchisi uni bosib ketadi. Review da `yml` ni o'zgartirish yetarli emasligini aniqlash kerak.

## 21.9 Review checklisti: konfiguratsiya

| Savol | Nega |
| --- | --- |
| Yangi qiymat nimaga asoslangan | Taxminiy qiymat incident manbasi |
| Pool va thread chegaralari resursga sig'adimi | DB `max_connections`, xotira |
| Timeout va retry ko'paytmasi byudjetga sig'adimi | Kaskadli kechikish |
| Secret muhitdan olinadimi | Repoda secret bo'lmasligi |
| Profil xulq farqi yaratadimi | Prodda sinalmagan yo'l |
| `@Value` o'rniga tipli obyekt ishlatilganmi | Ishga tushishda tekshirish |
| Flag ning egasi va o'chirish sanasi bormi | Doimiy shoxlar |
| Actuator ro'yxati minimalmi | Ma'lumot oqishi |
| K8s env qiymatni bosib ketmaydimi | O'zgarish ta'sir qilmasligi |
| Sozlama ta'siri o'lchanadimi | Natijani ko'rish |

## 21.10 Amalda qo'llash

- [ ] Barcha `@Value` ishlatilgan joylarni `@ConfigurationProperties` + `@Validated` ga o'tkazish rejasini tuzing.
- [ ] Pool kattaligi x pod soni ni PostgreSQL `max_connections` bilan taqqoslab, zaxira qolganini tasdiqlang.
- [ ] Har bir tashqi integratsiya uchun timeout x urinishlar byudjetini hisoblab, yuqori qatlam timeout iga sig'ishini tekshiring.
- [ ] `gitleaks` ni pre-commit va CI ga qo'shib, butun tarixni bir marta skanerlang.
- [ ] `@Profile` ishlatilgan beanlarni ko'rib, xulq farqi yaratadiganlarni konfiguratsiya farqiga o'tkazing.
- [ ] Mavjud feature flag larni sanab, har biriga egasi va o'chirish sanasini qo'shing; muddati o'tganlarni aniqlaydigan test yozing.
- [ ] Actuator ro'yxatini `health,info,prometheus` ga qisqartirib, alohida portga chiqaring.
- [ ] Prodda haqiqatda ishlayotgan konfiguratsiyani `configprops` va K8s env orqali tekshirib, `application.yml` bilan farqini hujjatlashtiring.

---

[&larr; 20. Web qatlami review: DTO, validatsiya, xato javobi](20-web-qatlami-review-dto-validatsiya-xato.md) · [Mundarija](README.md) · [22. Tashqi integratsiya review: timeout, retry, broker &rarr;](22-tashqi-integratsiya-review-timeout-retry.md)
