<!-- doc: code-review | chapter: 28 | part: VI. Xavfsizlik review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 28. Xavfsizlik review metodikasi (How to Review for Security)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [28.1 Asosiy savol: ishonilmaydigan ma'lumot qayerga boradi](#281-asosiy-savol-ishonilmaydigan-malumot-qayerga-boradi)
- [28.2 Ishonch chegarasi diffda](#282-ishonch-chegarasi-diffda)
- [28.3 Tez tekshirish ro'yxati: har PR uchun o'n savol](#283-tez-tekshirish-royxati-har-pr-uchun-on-savol)
- [28.4 Zaiflik sinflarini tizimli ko'rish](#284-zaiflik-sinflarini-tizimli-korish)
- [28.5 Xavfsizlik izohining shakli](#285-xavfsizlik-izohining-shakli)
- [28.6 Xavfsizlik uchun avtomatlashtirish va uning chegarasi](#286-xavfsizlik-uchun-avtomatlashtirish-va-uning-chegarasi)
- [28.7 Xavfsizlik review ni jarayonga kiritish](#287-xavfsizlik-review-ni-jarayonga-kiritish)
- [28.8 Amalda qo'llash](#288-amalda-qollash)

</details>


Xavfsizlik review ni "xavfsizlik jamoasining ishi" deb hisoblash eng keng tarqalgan xato. Amalda zaifliklarning katta qismi oddiy kod review da topilishi mumkin, agar reviewer to'g'ri savollarni bersa. Bu bob metodikani beradi: ishonch chegaralarini topish, ma'lumot oqimini kuzatish va zaiflik sinflarini tizimli tekshirish. Keyingi besh bob aniq sinflarni ochadi.

## 28.1 Asosiy savol: ishonilmaydigan ma'lumot qayerga boradi

Xavfsizlik review ning yadrosi bitta savolda: tashqi manbadan kelgan ma'lumot qaysi yo'l bilan xavfli operatsiyaga yetib boradi.

Ishonilmaydigan manbalar (`source`):

| Manba | Ko'pincha e'tibordan chetda qoladigan |
| --- | --- |
| HTTP so'rov tanasi, parametrlar, yo'l | - |
| HTTP header lar | `Host`, `X-Forwarded-For`, `Referer`, `User-Agent` |
| Cookie va token tarkibi | JWT claim lari (imzolangan, lekin ma'nosi tekshirilmagan) |
| Fayl nomi va tarkibi | Yuklangan fayl metadata si |
| Boshqa servis javobi | "Ichki servis" ham buzilgan bo'lishi mumkin |
| Kafka xabari | Produser buzilgan yoki xato yuborgan |
| Ma'lumotlar bazasidagi qiymat | Avval ishonilmagan manbadan kelgan (ikkilamchi injection) |
| Muhit o'zgaruvchisi va konfiguratsiya | Konteyner buzilgan holat |
| Fayl tizimidagi fayl | Umumiy hajm (shared volume) |

Xavfli operatsiyalar (`sink`):

| Operatsiya | Zaiflik sinfi |
| --- | --- |
| SQL yoki JPQL qurish | Injection ([29-bob](29-injection-review-sql-va-boshqalar.md)) |
| Buyruq bajarish (`ProcessBuilder`) | Command injection |
| Fayl yo'li qurish | Path traversal |
| URL qurish va so'rov yuborish | SSRF |
| Deserializatsiya | RCE |
| Shablon yoki ifoda bajarish (SpEL, Thymeleaf) | Expression injection |
| HTML yoki JS ga chiqarish | XSS |
| LDAP yoki XPath so'rovi | Injection |
| Log yozish | Log injection, ma'lumot oqishi |
| Avtorizatsiya qarori | Huquq oshirish |
| Redirect manzili | Open redirect |

Review usuli: diffda yangi sink paydo bo'lsa, uning kirishini orqaga kuzatish; yangi source paydo bo'lsa, u qayerga borishini oldinga kuzatish. Ikki uchi ishonilmaydigan manba va xavfli operatsiyada tutashsa - zaiflik.

## 28.2 Ishonch chegarasi diffda

```java
// Chegara qayerda: shu metodga kelgan ma'lumot tekshirilganmi?
// Review da har bir public metod uchun javob kerak.

// Chegara 1: HTTP controller - ishonilmaydigan kirish.
@PostMapping("/orders")
public OrderResponse create(@Valid @RequestBody CreateOrderRequest req,
                            @AuthenticationPrincipal AppUser user) {
    // Bu nuqtadan keyin: req shakli tekshirilgan (@Valid), user autentifikatsiya
    // qilingan. LEKIN: req ichidagi ID lar user ga tegishliligi TEKSHIRILMAGAN.
    return orders.place(req.toCommand(user.id()));
}

// Chegara 2: Kafka listener - ishonilmaydigan kirish.
@KafkaListener(topics = "orders")
public void on(OrderEvent event) {
    // Bu ham ishonilmaydigan kirish: sxema tekshirilgan, mazmun emas.
}

// Chegara 3: ichki servis chaqiruvi - shartli ishonch.
public void applyDiscount(OrderId id, Percentage discount) {
    // Bu metod ichki, lekin kim chaqirishini bilmaydi. Agar u 100%
    // chegirma qabul qilsa va chaqiruvchi tekshirmasa - muammo.
    // Review savoli: cheklov qayerda - bu yerda yoki chaqiruvchida?
}
```

## 28.3 Tez tekshirish ro'yxati: har PR uchun o'n savol

1. Yangi endpoint bormi, va u autentifikatsiya talab qiladimi.
2. Yangi endpoint foydalanuvchi ma'lumotini qaytaradimi, va egalik tekshirilganmi.
3. Foydalanuvchi identifikatori so'rovdan olinganmi (olinmasligi kerak).
4. Tashqi ma'lumot SQL, fayl yo'li, URL yoki buyruqqa tushadimi.
5. Yangi bog'liqlik qo'shilganmi, uning CVE holati qanday.
6. Logga yangi narsa yoziladimi, unda maxfiy ma'lumot bormi.
7. Xato javobida ichki detallar bormi.
8. Yangi konfiguratsiya secret ni ochib qo'ymaydimi.
9. Deserializatsiya, shablon, ifoda bajarilishi bormi.
10. Keshlangan yoki umumiy holatga foydalanuvchi ma'lumoti tushadimi.

```bash
# Shu ro'yxatni diffda avtomatik tez skanerlash.
FILES=$(git diff --name-only origin/main...HEAD)
D=$(git diff origin/main...HEAD)

echo "=== yangi endpointlar ==="
echo "$D" | grep -E '^\+.*@(Get|Post|Put|Delete|Patch|Request)Mapping'

echo "=== avtorizatsiya annotatsiyalari ==="
echo "$D" | grep -E '^\+.*@(PreAuthorize|PostAuthorize|Secured|RolesAllowed)'

echo "=== xavfli sink lar ==="
echo "$D" | grep -nE '^\+.*(createQuery\(|createNativeQuery\(|queryForList\(|\.execute\(|ProcessBuilder|Runtime\.getRuntime|new File\(|Paths\.get\(|new URL\(|URI\.create\(|readObject|parseExpression|SpelExpression)'

echo "=== so'rovdan kelgan qiymat bilan satr qurish ==="
echo "$D" | grep -nE '^\+.*(RequestParam|PathVariable|RequestHeader).*' | head
echo "$D" | grep -nE '^\+.*(\"\s*\+\s*[a-zA-Z]|\.formatted\(|String\.format\()' | head

echo "=== secret va token ==="
echo "$D" | grep -niE '^\+.*(password|secret|token|api[_-]?key|private[_-]?key)\s*[:=]'

echo "=== logga obyekt yozish ==="
echo "$D" | grep -nE '^\+.*log\.(info|debug|warn|error)\(.*(request|user|token|card|password)'

echo "=== xavfsizlik konfiguratsiyasi ==="
echo "$D" | grep -nE '^\+.*(permitAll|csrf\(\)|\.disable\(\)|anonymous\(\)|cors\(\)|hasRole|authenticated\(\))'
```

## 28.4 Zaiflik sinflarini tizimli ko'rish

Review ni to'liq qilish uchun sinflar bo'yicha o'tish kerak, aks holda faqat tanish zaifliklar topiladi.

| Sinf | Spring/Java kontekstida | Bob |
| --- | --- | --- |
| Buzilgan kirish nazorati | `@PreAuthorize` yo'qligi, IDOR | 30 |
| Injection | SQL, JPQL, dinamik `ORDER BY`, SpEL | 29 |
| Autentifikatsiya kamchiliklari | JWT tekshiruvi, sessiya, parol siyosati | 30 |
| Xavfsiz bo'lmagan dizayn | Biznes mantiqini chetlab o'tish, narx manipulyatsiyasi | 30 |
| Noto'g'ri konfiguratsiya | Actuator, CORS, CSRF, standart parollar | 21, 30 |
| Zaif bog'liqliklar | CVE, eskirgan kutubxonalar | 33 |
| Ma'lumot oqishi | Log, xato javobi, ortiqcha maydonlar | 32 |
| Kriptografik xatolar | Zaif algoritm, tasodif, kalit boshqaruvi | 32 |
| SSRF | URL ni kirishdan qurish | 31 |
| Deserializatsiya | Jackson polimorfizmi, `ObjectInputStream` | 31 |
| Fayl operatsiyalari | Path traversal, zip slip, upload | 31 |
| Yetarsiz log va monitoring | Hujumni ko'rmaslik | 39 |
| DoS | Chegarasiz so'rov, regex, arxiv bombasi | 20, 31 |

## 28.5 Xavfsizlik izohining shakli

Xavfsizlik izohi boshqa izohlardan farq qiladi: u ko'pincha blocker bo'ladi, va uning asoslanishi aniq bo'lishi kerak - aks holda u "paranoyya" deb qabul qilinadi.

```text
# Yomon shakl: nom bilan qo'rqitish.
"Bu SQL injection, tuzatish kerak."

# Yaxshi shakl: yo'l, ta'sir, tuzatish.
blocker (xavfsizlik): ReportService.build() da sortBy parametri
to'g'ridan-to'g'ri ORDER BY ga qo'yilgan.

Yo'l: GET /reports?sortBy=... -> ReportController.build() ->
      ReportService.build() -> jdbc.queryForList(sql)
      Parametr hech qayerda tekshirilmaydi va whitelist yo'q.

Ta'sir: hujumchi ORDER BY o'rniga ifoda qo'yib, boshqa jadvallardan
ma'lumot chiqarib olishi mumkin. Masalan:
  ?sortBy=(SELECT password_hash FROM app_user LIMIT 1)
Bu xatolik xabari orqali yoki tartiblash natijasi orqali ma'lumot
beradi. Jadvalda 40 ming foydalanuvchi bor.

Tuzatish: ruxsat etilgan ustunlar enum i (quyida namuna). O'zgarish
hajmi: 1 enum + 3 satr.

  public enum OrderSort {
      CREATED_AT("o.created_at DESC"), TOTAL("o.total DESC");
      private final String sql;
      public static OrderSort of(String raw) {
          return Arrays.stream(values())
              .filter(v -> v.name().equalsIgnoreCase(raw))
              .findFirst().orElse(CREATED_AT);
      }
  }
```

## 28.6 Xavfsizlik uchun avtomatlashtirish va uning chegarasi

| Instrument | Nimani topadi | Nimani topmaydi |
| --- | --- | --- |
| Sonar / SpotBugs (SAST) | Ma'lum naqshlar: konkatenatsiya, zaif tasodif | Avtorizatsiya mantiqi, biznes qoidasi |
| Semgrep (custom qoidalar) | Loyihaga xos naqshlar | Kontekst va niyat |
| Dependency scanning | Ma'lum CVE lar | Noto'g'ri ishlatilgan xavfsiz kutubxona |
| Secret scanning | Koddagi kalitlar | Noto'g'ri saqlangan secret |
| DAST / pentest | Ishlaydigan tizimdagi zaifliklar | Kod darajasidagi sabab |
| Kod review | Avtorizatsiya, mantiq, kontekst | Konfiguratsiya va infratuzilma |

Asosiy xulosa: avtomatik instrumentlar injection va CVE larni yaxshi topadi, lekin kirish nazorati xatolarini - zaifliklarning eng ko'p uchraydigan sinfini - deyarli topmaydi. Chunki "bu foydalanuvchi shu buyurtmani ko'rishi kerakmi" degan savolga javob faqat domen bilimida bor. Shu sababli reviewer ning asosiy e'tibori [30-bobga](30-autentifikatsiya-va-avtorizatsiya-review.md) qaratiladi.

```yaml
# Loyihaga xos xavfsizlik qoidasi: Semgrep bilan.
# .semgrep/dynamic-order-by.yml
rules:
  - id: dynamic-order-by
    languages: [java]
    severity: ERROR
    message: >
      ORDER BY ga o'zgaruvchi qo'shilgan. Ruxsat etilgan ustunlar enum i
      ishlatilishi kerak (REVIEW.md: xavfsizlik, [29-bob](29-injection-review-sql-va-boshqalar.md)).
    patterns:
      - pattern-either:
          - pattern: |
              "$...ORDER BY" + $VAR
          - pattern: |
              $SB.append("ORDER BY").append($VAR)
```

## 28.7 Xavfsizlik review ni jarayonga kiritish

| Mexanizm | Nima qiladi |
| --- | --- |
| `CODEOWNERS` da xavfsizlik yo'llari | Auth, crypto, to'lov kodiga majburiy reviewer |
| PR shablonida xavfsizlik bo'limi | Muallif o'zi savol beradi |
| Yuqori xavfli yo'llar ro'yxati | Chuqur review darajasi |
| Threat model (bir sahifa) | Nimadan himoyalanamiz |
| Incident dan o'rganish | Katalogga yangi band (12.10) |
| Muntazam skanerlash | CVE va secret |

```markdown
<!-- .github/pull_request_template.md ichidagi xavfsizlik bo'limi -->
## Xavfsizlik

- [ ] Yangi endpoint yo'q, yoki bor va avtorizatsiya qoidasi yozilgan
- [ ] Tashqi ma'lumot SQL, fayl yo'li, URL yoki buyruqqa tushmaydi
- [ ] Foydalanuvchi faqat o'z ma'lumotini ko'radi (ID so'rovdan olinmaydi)
- [ ] Logga maxfiy ma'lumot yozilmaydi
- [ ] Yangi bog'liqlik yo'q, yoki bor va CVE tekshirilgan
- [ ] Xato javobida ichki detallar yo'q
```

## 28.8 Amalda qo'llash

- [ ] `scripts/review-security-scan.sh` skriptini qo'shib, uni har PR da ishga tushirishni odat qiling.
- [ ] Loyihadagi barcha ishonilmaydigan manbalar va xavfli operatsiyalar ro'yxatini bir sahifada yozing.
- [ ] O'n savolli tez ro'yxatni PR shabloniga qo'shing.
- [ ] `CODEOWNERS` da autentifikatsiya, avtorizatsiya, to'lov va kriptografiya yo'llariga majburiy reviewer belgilang.
- [ ] Loyihaga xos uchta xavfsizlik naqshini Semgrep qoidasiga aylantirib, CI ga qo'shing.
- [ ] Bir sahifali threat model yozing: kim hujum qiladi, nimaga, qanday himoya bor.
- [ ] Oxirgi uchta xavfsizlik topilmasini `REVIEW-SMELLS.md` ga "qanday qidiramiz" ustuni bilan qo'shing.
- [ ] Zaiflik sinflari jadvalini review checklistiga kiritib, har chorakda bitta sinf bo'yicha maqsadli audit o'tkazing.

---

[&larr; 27. Izolyatsiya, poyga holatlari va xabar yetkazish](27-izolyatsiya-poyga-holatlari-va-xabar.md) · [Mundarija](README.md) · [29. Injection review: SQL va boshqalar &rarr;](29-injection-review-sql-va-boshqalar.md)
