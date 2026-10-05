<!-- doc: code-review | chapter: 40 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 40. Review jarayonini qurish (Building the Process)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [40.1 Kim review qiladi: CODEOWNERS](#401-kim-review-qiladi-codeowners)
- [40.2 Xavf bo'yicha tabaqalash](#402-xavf-boyicha-tabaqalash)
- [40.3 SLA va navbat](#403-sla-va-navbat)
- [40.4 PR shabloni](#404-pr-shabloni)
- [40.5 Draft va bosqichli review](#405-draft-va-bosqichli-review)
- [40.6 Avtomatik tekshiruvlar tartibi](#406-avtomatik-tekshiruvlar-tartibi)
- [40.7 Merge strategiyasi va review](#407-merge-strategiyasi-va-review)
- [40.8 Review ni o'tkazib yuborish mumkin bo'lgan holatlar](#408-review-ni-otkazib-yuborish-mumkin-bolgan-holatlar)
- [40.9 Review checklisti: jarayon](#409-review-checklisti-jarayon)
- [40.10 Amalda qo'llash](#4010-amalda-qollash)

</details>


Yaxshi reviewer lar bo'lgan jamoada ham review yomon ishlashi mumkin, agar jarayon bo'lmasa: PR lar kutadi, kim ko'rishi noaniq, xavfli o'zgarishlar oddiy o'zgarishlar bilan bir xil yo'ldan o'tadi. Bu bob jarayonning mexanik qismini beradi - kim, qachon, qanday chuqurlikda.

## 40.1 Kim review qiladi: CODEOWNERS

```bash
# .github/CODEOWNERS - eng kam harakat bilan eng katta foyda beradigan fayl.
# Tartib muhim: oxirgi mos kelgan qoida ishlaydi.

# Standart: har qanday o'zgarish backend jamoasiga.
*                                       @acme/backend

# Domen bo'yicha egalik: kim bilsa, shu ko'radi.
/order-service/                         @acme/orders-team
/payment-service/                       @acme/payments-team

# Yuqori xavfli yo'llar: ikki reviewer va maxsus jamoa.
/**/db/migration/                       @acme/dba @acme/backend-leads
/**/SecurityConfig.java                 @acme/security
/**/security/                           @acme/security
/**/payment/                            @acme/payments-team @acme/security

# Infratuzilma va build.
/pom.xml                                @acme/backend-leads
/.github/workflows/                     @acme/platform
/Dockerfile                             @acme/platform
/k8s/                                   @acme/platform

# Review qoidalari o'zi: o'zgartirish uchun kelishuv kerak.
/REVIEW.md                              @acme/backend-leads
/.github/CODEOWNERS                     @acme/backend-leads
```

```yaml
# Branch protection: CODEOWNERS ni majburiy qilish (GitHub sozlamalari).
# - Require review from Code Owners: yoqilgan
# - Required approvals: 1 (yuqori xavfli yo'llar uchun CODEOWNERS 2 beradi)
# - Dismiss stale approvals on push: yoqilgan (yangi commit - yangi review)
# - Require status checks: build, test, sonar, dependency-check
# - Require conversation resolution: yoqilgan (javobsiz izoh qolmaydi)
```

## 40.2 Xavf bo'yicha tabaqalash

2.9 da tabaqalash jadvali berilgan; bu yerda uni jarayonga aylantirish.

```yaml
# .github/workflows/risk-label.yml
# PR tegilgan yo'llarga qarab avtomatik yorliq oladi: reviewer
# chuqurlik darajasini darhol ko'radi.
name: risk-label
on: pull_request
jobs:
  label:
    runs-on: ubuntu-latest
    permissions: { pull-requests: write, contents: read }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - id: risk
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          LEVEL=low
          echo "$FILES" | grep -qE '\.(java|kt)$' && LEVEL=medium
          echo "$FILES" | grep -qE 'db/(migration|changelog)|Security|payment|auth|crypto' && LEVEL=high
          echo "$FILES" | grep -qE 'db/migration/.*(DROP|ALTER COLUMN|TRUNCATE)' && LEVEL=critical
          echo "level=$LEVEL" >> "$GITHUB_OUTPUT"
      - uses: actions/github-script@v7
        with:
          script: |
            const level = '${{ steps.risk.outputs.level }}';
            await github.rest.issues.addLabels({
              owner: context.repo.owner, repo: context.repo.repo,
              issue_number: context.issue.number, labels: [`risk:${level}`]
            });
            if (level === 'high' || level === 'critical') {
              await github.rest.issues.createComment({
                owner: context.repo.owner, repo: context.repo.repo,
                issue_number: context.issue.number,
                body: `Bu PR \`risk:${level}\` deb belgilandi.\n\n`
                    + `Talablar (REVIEW.md):\n`
                    + `- ikki reviewer\n`
                    + `- migratsiya uchun: qulf turi, vaqti va qaytarish rejasi\n`
                    + `- lokalda yoki stagingda sinalgani haqida izoh`
              });
            }
```

## 40.3 SLA va navbat

| Mezon | Tavsiya |
| --- | --- |
| Birinchi javob | 4 ish soati ichida |
| Tuzatishdan keyingi javob | 2 ish soati (kontekst yangi) |
| Yuqori xavfli PR | O'sha kuni, lekin shoshilmasdan |
| Kutish vaqti 24 soatdan oshsa | Jamoa kanalida eslatma |
| Kutish vaqti 48 soatdan oshsa | Tech lead aralashadi |
| Review byudjeti | Kunning 10-15 foizi (2.5) |

```yaml
# Kutayotgan PR lar haqida eslatma: shovqin emas, yordam.
name: stale-pr-reminder
on:
  schedule: [ { cron: '0 9,14 * * 1-5' } ]       # kuniga ikki marta, ish kunlari
jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const prs = await github.paginate(github.rest.pulls.list, {
              owner: context.repo.owner, repo: context.repo.repo, state: 'open'
            });
            const now = Date.now();
            for (const pr of prs) {
              if (pr.draft) continue;
              const hours = (now - new Date(pr.created_at)) / 36e5;
              const reviews = await github.rest.pulls.listReviews({
                owner: context.repo.owner, repo: context.repo.repo, pull_number: pr.number
              });
              // Birinchi javob 24 soatdan ko'p kutilgan bo'lsa.
              if (reviews.data.length === 0 && hours > 24) {
                console.log(`kutayotgan: #${pr.number} (${Math.round(hours)} soat)`);
                // Slack yoki jamoa kanaliga xabar yuborish.
              }
            }
```

## 40.4 PR shabloni

```markdown
<!-- .github/pull_request_template.md -->
## Nima o'zgardi va nega

<!-- Bir-ikki jumla. Tiket havolasi. -->

## Qanday tekshirildi

<!-- Testlar, lokal sinov, staging. "Ishlayapti" yetarli emas. -->

## Reviewer uchun

<!-- Qaysi joyga alohida qarash kerak? Qaysi qaror muhokamaga arziydi? -->

---

### Tekshiruv ro'yxati

- [ ] Yangi kod uchun testlar bor: chegaraviy holatlar va xato yo'llari
- [ ] Yo'q kod ro'yxati o'tildi: validatsiya, avtorizatsiya, timeout, indeks, log
- [ ] Tranzaksiya chegarasi ichida tashqi chaqiruv yo'q
- [ ] Ikki marta kelgan so'rov xavfsiz (idempotentlik)
- [ ] Ikki parallel so'rov xavfsiz (unique constraint, versiya yoki qulf)
- [ ] Xato holatida nima bo'lishi aniq va o'lchanadi

### Agar tegishli bo'lsa

<!-- Tegishli bo'lmasa, qatorni o'chirib tashlang. -->

**Migratsiya:**
- [ ] Qulf turi va kutilgan davomiyligi:
- [ ] Rolling deploy da eski kod ishlaydi
- [ ] Qaytarish rejasi:
- [ ] Real hajmga yaqin nusxada sinalgan, vaqti:

**API o'zgarishi:**
- [ ] Breaking emas, yoki breaking va o'tish rejasi bor:
- [ ] OpenAPI va CHANGELOG yangilangan

**Xavfsizlik:**
- [ ] Yangi endpoint avtorizatsiya qoidasiga ega
- [ ] Foydalanuvchi faqat o'z ma'lumotini ko'radi
- [ ] Tashqi ma'lumot SQL, URL, fayl yo'liga tushmaydi
- [ ] Logda maxfiy ma'lumot yo'q

**Performance:**
- [ ] Siklda DB yoki HTTP chaqiruvi yo'q
- [ ] So'rovlar soni ma'lumot hajmiga bog'liq emas
- [ ] Byudjetga sig'adi (performance-budget.yml)
```

Shablonning asosiy qoidasi: uzun shablon o'qilmaydi. Majburiy qism 6 banddan oshmasligi kerak, qolgani shartli. "Agar tegishli bo'lmasa, o'chirib tashlang" ko'rsatmasi muhim - aks holda hamma band mexanik belgilanadi.

## 40.5 Draft va bosqichli review

```text
# Katta o'zgarish uchun uch bosqich: har bosqichda narx past.
1. Dizayn eskizi (kod yo'q)        -> 1 sahifa, 2 kun ichida javob
2. Draft PR (skelet, interfeyslar) -> yo'nalish tasdiqlanadi
3. To'liq PR                        -> satr-satr review

# Draft PR ning foydasi: muallif bir hafta noto'g'ri yo'nalishda
# ishlamaydi. Review izohi draft da "bu yondashuvni o'zgartiraylik"
# deyilsa, narxi bir kun; to'liq PR da - bir hafta.
```

## 40.6 Avtomatik tekshiruvlar tartibi

Review odam vaqtini faqat mashina tuta olmaydigan narsaga sarflashi kerak ([5-bob](05-mashina-va-odam-sonarqube-dan-oldin-topish.md)). Buning uchun CI tartibi muhim: arzon va tez tekshiruvlar oldin.

```yaml
# .github/workflows/pr.yml - tez signal, keyin chuqur tekshiruv.
name: pr
on: pull_request
jobs:
  fast:                              # 1-2 daqiqa: darhol javob
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', cache: 'maven' }
      - run: ./mvnw -q -B spotless:check              # format
      - run: ./mvnw -q -B -T1C compile                # kompilyatsiya
      - run: ./mvnw -q -B checkstyle:check            # uslub
      - run: gitleaks protect --staged --redact       # secret

  unit:                              # 3-5 daqiqa
    needs: fast
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./mvnw -q -B -T1C test                   # unit testlar
      - run: ./mvnw -q -B test -Dtest='Arch*Test'     # arxitektura qoidalari

  integration:                       # 5-15 daqiqa
    needs: fast
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./mvnw -q -B verify -Pit                 # Testcontainers

  analysis:                          # parallel, bloklamaydi
    needs: fast
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }                      # Sonar uchun to'liq tarix
      - run: ./mvnw -q -B verify sonar:sonar -DskipTests
      - run: ./mvnw -q -B dependency-check:check
```

Review qoidasi: muallif CI yashil bo'lgandan keyin review so'raydi. Qizil CI bilan review so'rash reviewer vaqtini isrof qiladi.

## 40.7 Merge strategiyasi va review

| Strategiya | Review ga ta'siri |
| --- | --- |
| Squash merge | Commit tarixi yo'qoladi - review paytida o'qish kerak (4.5) |
| Merge commit | Tarix saqlanadi, lekin shovqinli |
| Rebase merge | Chiziqli tarix, lekin commitlar alohida yashil bo'lishi kerak |

```yaml
# Review natijasi commit xabarida saqlanishi uchun squash shablon:
# GitHub sozlamalarida "Default commit message: PR title and description"
# Shunda PR tavsifi (va undagi qarorlar) git tarixida qoladi.
```

## 40.8 Review ni o'tkazib yuborish mumkin bo'lgan holatlar

Har bir o'zgarish review dan o'tishi kerak degan qoida amalda buziladi, shuning uchun istisnolarni ochiq belgilash yaxshiroq.

| Holat | Yo'l |
| --- | --- |
| Prod incident, hotfix | Merge, keyin 24 soat ichida post-review |
| Faqat docs va CHANGELOG | Yengil yo'l (2.8) |
| Avtomatik bog'liqlik patch i | CI yashil bo'lsa avtomatik merge (33.4) |
| Reliz versiyasini ko'tarish | Avtomatlashtirilgan |
| Formatlash commiti | Alohida PR, diffsiz review |

```markdown
<!-- REVIEW.md ichida: hotfix siyosati -->
## Hotfix

Prod incident paytida review kutilmaydi. Shartlar:
1. Incident kanalida ikkinchi muhandis "ko'rdim" deb tasdiqlaydi (og'zaki review).
2. O'zgarish minimal bo'ladi: faqat to'xtatish, refactoring yo'q.
3. Merge dan keyin 24 soat ichida to'liq review PR ga izoh sifatida qo'shiladi.
4. Incident tahlilida shu o'zgarish ko'rib chiqiladi va kerak bo'lsa tuzatiladi.
```

## 40.9 Review checklisti: jarayon

| Savol | Nega |
| --- | --- |
| `CODEOWNERS` xavfli yo'llarni qamraydimi | Mas'uliyat |
| Branch protection sozlanganmi | Qoidalar majburiy |
| Xavf darajasi avtomatik belgilanadimi | Chuqurlik tanlovi |
| SLA kelishilgan va kuzatiladimi | Kutish vaqti |
| PR shabloni qisqa va shartlimi | O'qilishi |
| Arzon tekshiruvlar CI dami | Reviewer vaqti |
| Muallif CI yashil bo'lgach so'raydimi | Isrof |
| Draft bosqichi ishlatiladimi | Erta yo'nalish tuzatish |
| Hotfix siyosati yozilganmi | Incidentda chalkashlik |
| Javobsiz izohlar merge ni bloklaydimi | Yo'qolgan topilmalar |

## 40.10 Amalda qo'llash

- [ ] `.github/CODEOWNERS` yaratib, migratsiya, xavfsizlik va to'lov yo'llariga maxsus egalar belgilang.
- [ ] Branch protection da "Require conversation resolution" va "Dismiss stale approvals" ni yoqing.
- [ ] Xavf darajasini avtomatik belgilaydigan workflow ni qo'shing.
- [ ] PR shablonini yozib, majburiy qismni 6 banddan oshirmang.
- [ ] CI ni bosqichlarga bo'ling: format va kompilyatsiya 2 daqiqada javob bersin.
- [ ] Review SLA sini kelishib, kutayotgan PR lar haqida kunlik eslatmani sozlang.
- [ ] Katta o'zgarishlar uchun dizayn eskizi va draft PR bosqichlarini joriy qiling.
- [ ] Hotfix siyosatini `REVIEW.md` ga yozib, post-review majburiyatini belgilang.

---

[&larr; 39. Observability review](39-observability-review.md) · [Mundarija](README.md) · [41. Review madaniyati, til va kelishmovchilik &rarr;](41-review-madaniyati-til-va-kelishmovchilik.md)
