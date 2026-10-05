<!-- doc: code-review | chapter: 33 | part: VI. Xavfsizlik review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 33. Bog'liqlik va supply chain review (Dependencies and Supply Chain)

<details>
<summary>Bu bobdagi 7 bo'lim</summary>

- [33.1 Yangi bog'liqlik uchun savollar](#331-yangi-bogliqlik-uchun-savollar)
- [33.2 Transitive bog'liqliklar va versiya konflikti](#332-transitive-bogliqliklar-va-versiya-konflikti)
- [33.3 Skanerlashni CI ga qo'yish](#333-skanerlashni-ci-ga-qoyish)
- [33.4 Versiya yangilash PR larini review qilish](#334-versiya-yangilash-pr-larini-review-qilish)
- [33.5 Build va CI ning o'zi](#335-build-va-ci-ning-ozi)
- [33.6 Review checklisti: bog'liqliklar](#336-review-checklisti-bogliqliklar)
- [33.7 Amalda qo'llash](#337-amalda-qollash)

</details>


`pom.xml` dagi bitta qator butun ilovaga kod qo'shadi - sizning kodingizdan ko'p bo'lishi mumkin. Shu sababli bog'liqlik o'zgarishi review da alohida e'tibor talab qiladi, lekin amalda u eng tez "LGTM" oladigan diff turi.

## 33.1 Yangi bog'liqlik uchun savollar

6.4 da arxitektura nuqtai nazaridan savollar berilgan; bu yerda xavfsizlik va yangilanish nuqtai nazari.

| Savol | Qanday tekshirish |
| --- | --- |
| Oxirgi reliz qachon | Maven Central yoki GitHub |
| Ma'lum CVE bormi | `dependency-check`, `osv-scanner` |
| Litsenziya mosmi | `license-maven-plugin` |
| Nechta transitive olib keladi | `dependency:tree` |
| Ishlab chiqaruvchisi kim | Jamoa yoki bitta odam |
| Nomi tanish paketga o'xshashmi | Typosquatting |
| Qancha kod uchun olinadi | 20 satr uchun kutubxona - savol |
| Alternativa JDK yoki Spring da bormi | Ko'pincha bor |

```bash
# Yangi bog'liqlik haqida ma'lumot to'plash: review izohi uchun dalil.
GROUP=com.example; ART=some-lib; VER=1.2.3

# 1) Oxirgi versiyalar va relizlar oralig'i.
curl -s "https://search.maven.org/solrsearch/select?q=g:$GROUP+AND+a:$ART&core=gav&rows=10&wt=json" \
  | jq -r '.response.docs[] | "\(.v)  \(.timestamp/1000 | todate)"'

# 2) Ma'lum zaifliklar (OSV - Google ning ochiq bazasi).
curl -s -X POST https://api.osv.dev/v1/query \
  -d "{\"package\":{\"ecosystem\":\"Maven\",\"name\":\"$GROUP:$ART\"},\"version\":\"$VER\"}" \
  | jq -r '.vulns[]? | "\(.id): \(.summary)"'

# 3) Nimani olib keladi.
./mvnw dependency:tree -Dincludes="$GROUP:$ART" -Dverbose

# 4) Haqiqiy o'zgarish: butun daraxt farqi (6.4 dagi usul).
```

## 33.2 Transitive bog'liqliklar va versiya konflikti

```bash
# Versiya konfliktlarini topish: Maven "eng yaqin g'olib" qoidasini
# ishlatadi, bu kutilmagan versiyaga olib kelishi mumkin.
./mvnw dependency:tree -Dverbose | grep -E 'omitted for conflict' | head -20

# Yakuniy versiyalarni ko'rish (haqiqatda nima ishlatiladi).
./mvnw dependency:list | grep -E 'jackson|netty|guava|commons' | sort -u

# Review diqqati: Spring Boot BOM versiyalarni boshqaradi. Qo'lda
# versiya ko'rsatish BOM ni chetlab o'tadi va mos kelmaslikka olib keladi.
```

```xml
<!-- Yomon: versiya qo'lda, BOM chetlab o'tilgan. -->
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
  <version>2.15.0</version>            <!-- Boot boshqa versiya kutadi -->
</dependency>

<!-- Yaxshi: BOM boshqaradi. -->
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
</dependency>

<!-- Agar aniq versiya kerak bo'lsa: sabab izoh bilan va BOM property orqali. -->
<properties>
  <!-- CVE-2026-XXXX tufayli 2.17.1 ga ko'tarildi; Boot 3.4 da 2.17.0.
       Boot 3.5 ga o'tganda bu propertyni olib tashlash kerak. -->
  <jackson-bom.version>2.17.1</jackson-bom.version>
</properties>
```

## 33.3 Skanerlashni CI ga qo'yish

```xml
<!-- OWASP Dependency-Check: ma'lum CVE larni topadi. -->
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <configuration>
    <!-- Yangi zaiflik topilsa build yiqiladi, lekin faqat yuqori darajada -
         aks holda shovqin tufayli hamma e'tiborsiz qoldiradi. -->
    <failBuildOnCVSS>7.0</failBuildOnCVSS>
    <suppressionFiles>
      <suppressionFile>.dependency-check-suppressions.xml</suppressionFile>
    </suppressionFiles>
    <nvdApiKey>${env.NVD_API_KEY}</nvdApiKey>
  </configuration>
</plugin>
```

```xml
<!-- Suppression fayli - review ning muhim obyekti.
     Har bir suppression sabab va muddat bilan bo'lishi kerak. -->
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
  <suppress until="2026-12-31Z">
    <notes>
      CVE-2026-1234: faqat XML parsing yo'lida, biz faqat JSON ishlatamiz.
      Tekshirilgan: 2026-10-04, PR #1423. Keyingi ko'rib chiqish: 2026-12-31.
    </notes>
    <packageUrl regex="true">^pkg:maven/com\.example/some-lib@.*$</packageUrl>
    <cve>CVE-2026-1234</cve>
  </suppress>
</suppressions>
<!-- Review qoidasi: izohsiz yoki `until` siz suppression qabul qilinmaydi.
     Aks holda suppression fayli "hammasini o'chirish" vositasiga aylanadi. -->
```

```bash
# Yengilroq va tezroq alternativa: osv-scanner (lockfile bo'yicha).
osv-scanner --lockfile=pom.xml

# SBOM yaratish: nima ishlatilayotganini hujjatlashtirish.
./mvnw org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom
# Natija: target/bom.json - incident paytida "bizda shu kutubxona bormi"
# savoliga tez javob beradi.
```

## 33.4 Versiya yangilash PR larini review qilish

Dependabot yoki Renovate yuborgan PR lar ko'pincha e'tiborsiz merge qilinadi. Ular uchun ham qoidalar kerak.

| Yangilanish turi | Review talabi |
| --- | --- |
| Patch (3.4.1 -> 3.4.2) | CI yashil bo'lsa yetarli |
| Minor (3.4 -> 3.5) | Reliz izohini o'qish, deprecation larni ko'rish |
| Major (3.x -> 4.x) | Migratsiya qo'llanmasi, alohida reja |
| Xavfsizlik yangilanishi | Tezkor, lekin CI majburiy |
| Transitive versiya o'zgarishi | `dependency:tree` farqini ko'rish |
| Build plugin yangilanishi | Lokalda `verify` o'tkazish |

```yaml
# Renovate konfiguratsiyasi: shovqinni kamaytirish va muhimini ajratish.
{
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "description": "Patch yangilanishlarni avtomatik birlashtirish",
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "description": "Spring Boot va Java ni alohida ko'rish",
      "matchPackagePatterns": ["^org.springframework", "^java"],
      "automerge": false,
      "labels": ["needs-careful-review"]
    },
    {
      "description": "Xavfsizlik yangilanishlari darhol",
      "matchDatasources": ["maven"],
      "vulnerabilityAlerts": { "labels": ["security"], "automerge": false }
    }
  ],
  "prConcurrentLimit": 5
}
```

## 33.5 Build va CI ning o'zi

Supply chain xavfi faqat kutubxonalarda emas - build jarayonining o'zida ham.

| Xavf | Himoya |
| --- | --- |
| Pin qilinmagan GitHub Action | SHA bilan pin qilish (`uses: actions/checkout@<sha>`) |
| `curl | bash` build ichida | Tekshirilgan artefakt, checksum |
| Ishonchsiz Maven repozitoriy | Faqat Central va ichki Nexus |
| Secret ni CI logida chop etish | Masking, `echo` dan saqlanish |
| Fork dan kelgan PR da secret | `pull_request` (emas `pull_request_target`) |
| Build artefaktining imzosi yo'q | Sigstore, checksum |
| Konteyner bazasi tag bilan | Digest bilan pin qilish |
| `latest` tag | Aniq versiya |

```yaml
# GitHub Actions: xavfsizroq shakl.
jobs:
  build:
    permissions:
      contents: read              # minimal huquq (standart: write)
    steps:
      # SHA bilan pin: tag o'zgartirilishi mumkin, SHA - yo'q.
      - uses: actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955  # v4.3.0
      - uses: actions/setup-java@c5195efecf7bdfc987ee8bae7a71cb8b11521c00  # v4.7.1
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: 'maven'
      - run: ./mvnw -B verify
```

```dockerfile
# Konteyner bazasini digest bilan pin qilish.
FROM eclipse-temurin:21-jre-alpine@sha256:abc123...
# Tag (`21-jre-alpine`) o'zgarishi mumkin - digest o'zgarmaydi.
# Review savoli: bu digest qachon yangilanadi va kim yangilaydi?

# Qo'shimcha review bandlari:
USER 10001                      # root emas
COPY --chown=10001:10001 target/app.jar /app/app.jar
# Ko'p qatlamli build: build vositalari yakuniy obrazda qolmaydi.
```

## 33.6 Review checklisti: bog'liqliklar

| Savol | Nega |
| --- | --- |
| Yangi bog'liqlik haqiqatan kerakmi | Hujum yuzasi va yangilanish yuki |
| CVE holati tekshirilganmi | Ma'lum zaiflik |
| Litsenziya mosmi | Huquqiy xavf |
| Versiya BOM orqali boshqariladimi | Mos kelmaslik |
| Qo'lda versiya ko'rsatilsa, sabab yozilganmi | Keyinchalik eskirib qoladi |
| Transitive o'zgarishlar ko'rilganmi | Yashirin yangilanish |
| Suppression lar sabab va muddat bilanmi | "Hammasini o'chirish" |
| GitHub Action lar SHA bilan pin qilinganmi | Supply chain |
| Konteyner bazasi digest bilanmi | Takrorlanuvchanlik |
| CI huquqlari minimalmi | Token o'g'irlanishi |
| SBOM yaratiladimi | Incidentda tez javob |

## 33.7 Amalda qo'llash

- [ ] `dependency-check` yoki `osv-scanner` ni CI ga qo'shib, `failBuildOnCVSS` ni 7.0 ga qo'ying.
- [ ] Mavjud suppression larni ko'rib chiqib, izohi va `until` sanasi yo'qlarini tuzating yoki olib tashlang.
- [ ] CycloneDX bilan SBOM yaratishni build ga qo'shing va natijani artefakt sifatida saqlang.
- [ ] Qo'lda versiya ko'rsatilgan bog'liqliklarni toping va har biriga sabab izohini qo'shing yoki BOM ga qaytaring.
- [ ] `dependency:tree -Dverbose` bilan versiya konfliktlarini aniqlab, ro'yxat tuzing.
- [ ] Renovate yoki Dependabot ni sozlab, patch yangilanishlarni avtomatik, major larni alohida yorliq bilan qiling.
- [ ] Barcha GitHub Action larni SHA bilan pin qiling va workflow huquqlarini `contents: read` ga tushiring.
- [ ] Konteyner bazasini digest bilan pin qilib, uni yangilash jarayonini belgilang.
- [ ] Yangi bog'liqlik qo'shadigan PR lar uchun shablonga 8 savolli ro'yxatni kiriting.

---

[&larr; 32. Secret, maxfiy ma'lumot va kriptografiya review](32-secret-maxfiy-malumot-va-kriptografiya.md) · [Mundarija](README.md) · [34. Test to'liqligini review qilish &rarr;](34-test-toliqligini-review-qilish.md)
