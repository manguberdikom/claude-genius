<!-- doc: code-review | chapter: 40 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 40. Review jarayonini qurish (Building the Process)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [40.1 Kim review qiladi: CODEOWNERS](#401-kim-review-qiladi-codeowners)
- [40.2 Xavf bo'yicha tabaqalash](#402-xavf-boyicha-tabaqalash)
- [40.3 SLA va navbat](#403-sla-va-navbat)
- [40.4 PR shabloni](#404-pr-shabloni)
- [40.5 Draft va bosqichli review](#405-draft-va-bosqichli-review)
- [40.6 Avtomatik tekshiruvlar tartibi](#406-avtomatik-tekshiruvlar-tartibi)
- [40.7 Merge strategiyasi va review](#407-merge-strategiyasi-va-review)
- [40.8 Review ni o'tkazib yuborish mumkin bo'lgan holatlar](#408-review-ni-otkazib-yuborish-mumkin-bolgan-holatlar)
- [40.9 Review checklisti: jarayon](#409-review-checklisti-jarayon)
- [40.10 Uch turdagi ruxsat: Google modeli va uni Java jamoasiga ko'chirish](#4010-uch-turdagi-ruxsat-google-modeli-va-uni-java-jamoasiga-kochirish)
- [40.11 Review turlari: har birida fokus boshqa](#4011-review-turlari-har-birida-fokus-boshqa)
- [40.12 Rasmiy inspeksiya anatomiyasi: rollar, bosqichlar va tezlik](#4012-rasmiy-inspeksiya-anatomiyasi-rollar-bosqichlar-va-tezlik)
- [40.13 Qoida va ko'rsatma: mashina nimani majburlaydi](#4013-qoida-va-korsatma-mashina-nimani-majburlaydi)
- [40.14 Review yetukligining ikki darajasi: diffdan tizimga](#4014-review-yetukligining-ikki-darajasi-diffdan-tizimga)
- [40.15 Amalda qo'llash](#4015-amalda-qollash)

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

Har bir o'zgarish review dan o'tishi kerak degan qoida amalda buziladi, shuning uchun istisnolarni ochiq belgilash yaxshiroq. Istisno ro'yxatini tuzishdan oldin [2.13](../code-review/02-review-iqtisodi-xato-narxi-navbat-va-pr.md#213-kichik-ozgarish-eng-xavfli-bir-qatorli-tuzatish) ni o'qing: kichik o'zgarishning xatolik darajasi eng yuqori, shuning uchun istisno hajm bo'yicha emas, mantiqqa tegishi bo'yicha beriladi.

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

## 40.10 Uch turdagi ruxsat: Google modeli va uni Java jamoasiga ko'chirish

Google ning review jarayonida bitta approve emas, uch xil ruxsat bor va ularni bir-biridan ajratish jarayonning masshtablanishini ta'minlaydi. Kitob ularni shunday sanaydi: boshqa muhandisdan keladigan to'g'rilik va tushunarlilik tekshiruvi (bu "looks good to me" biti), kod egasidan keladigan ruxsat (o'zgarish kodbazaning aynan shu qismi uchun o'rinlimi), va til bo'yicha "readability" ruxsati (kod tilning uslubi va eng yaxshi amaliyotlariga mos yozilganmi).

Muhimi: bu uch bit bir odamda to'planishi mumkin va kitobning aytishiga ko'ra ko'p review da shunday bo'ladi, shuning uchun jarayon amalda tez ishlaydi. Muallif ikkinchi va uchinchi bitni o'zi tutib tursa, unga faqat boshqa muhandisning LGTM i kerak bo'ladi. Bir nechta ruxsat kerak bo'lgan hollarda esa tartib ikki qadamli bo'ladi: avval tengdoshdan LGTM, keyin egadan yoki readability reviewer idan ruxsat. Kitob buni vaqt tejash deb izohlaydi, chunki ikki rol boshqa narsaga qaraydi: asosiy reviewer to'g'rilikka, ega esa boshqa savollarga - bu kodni saqlash oson bo'ladimi, u texnik qarzni oshiradimi, jamoada uni saqlab turish uchun bilim bormi.

Egalik modeli ham alohida belgilangan. Kitob `OWNERS` faylini mulk emas, **vakillik** (stewardship) deb ta'riflaydi: ega kodni tushunishi yoki tushunadigan odamni topa bilishi shart. Egalik ierarxik qo'shiladi, ya'ni fayl o'zidan yuqoridagi barcha `OWNERS` fayllari a'zolari birlashmasiga tegishli bo'ladi. Ro'yxat qisqa va fokuslangan bo'lishi tavsiya qilinadi, egalik esa initsiatsiya marosimi sifatida ishlatilmasligi va jamoadan ketayotgan odam egalikdan imkon qadar tez voz kechishi kerak.

| Google dagi ruxsat | Nimani tasdiqlaydi | Java/Spring loyihasida qayerda turadi |
| --- | --- | --- |
| LGTM | kod aytganini qiladi va tushunarli | PR dagi oddiy approve |
| Egalik ruxsati | o'zgarish kodbazaning shu qismi uchun o'rinli | `CODEOWNERS` ([40.1](#401-kim-review-qiladi-codeowners)) |
| Readability ruxsati | til uslubi va konvensiyaga moslik | asosan mashina: `spotless`, `checkstyle`, Error Prone; qolgani konvensiya reviewer ida |

```text
# Ikki qadamli oqim: PR da reviewer larni bir vaqtda emas, ketma-ket chaqirish.
1-qadam  tengdosh reviewer  -> to'g'rilik, tushunarlilik, testlar
2-qadam  CODEOWNERS egasi   -> saqlash narxi, texnik qarz, jamoada bilim bormi

# Foydasi: ega satr-satr o'qimaydi, u faqat "bu kod bizning
# qismimizga to'g'ri keladimi" savoliga javob beradi va tez o'tadi.
```

Readability ning o'zi Google da code review orqali o'tkaziladigan standartlashtirilgan mentorlik jarayoni; uning mazmuni va onboarding dagi joyi [toza kod hujjatida](../clean-code/47-birgalikda-ishlash-va-orgatish.md#473-yangi-odamga-toza-kod-standartini-yetkazish) ko'rilgan. Jarayonning narxi kitobda ochiq sanalgan: jamoada sertifikatlangan odam bo'lmasa tashqaridan reviewer qidirish kerak bo'ladi, qo'shimcha review davralari paydo bo'ladi va jarayon odamga tayangani uchun tashkilot o'sishiga chiziqli masshtablanadi. Ayni paytda kitob o'lchov natijasini ham keltiradi: readability olgan mualliflarning o'zgarishlari review va merge uchun statistik jihatdan sezilarli kamroq vaqt oladi.

Diqqat: kitob bu modelni Google ning o'z amaliyoti deb beradi va boshqaruvning bu darajasi "ba'zan haqiqatan og'ir" ekanini o'zi tan oladi. Sakkiz kishilik jamoa uchun uch bitni to'liq ko'chirish mantiqsiz; ko'chiriladigan narsa boshqa - **ikki rolni ajratish**: to'g'rilikni ko'radigan reviewer va qismga mas'ul ega bir xil savol bermasligi kerak.

## 40.11 Review turlari: har birida fokus boshqa

Google kitobi review ni bir xil ish deb qaramaydi va o'zgarishlarni to'rtta savatga ajratadi. Bu tabaqalash [40.2](#402-xavf-boyicha-tabaqalash) dagi xavf darajasidan boshqa o'q bo'ylab ishlaydi: xavf chuqurlikni, tur esa diqqat yo'nalishini belgilaydi.

| Tur | Diqqat | Tipik xato |
| --- | --- | --- |
| Greenfield: butunlay yangi kod | kod vaqt sinovidan o'tadimi; API kelishilgan dizaynga mosmi; egalari bormi | PR da dizaynni muhokama qilish |
| Xulq o'zgarishi, yaxshilash, optimizatsiya | o'zgarish kerakmi va kodbazani yaxshilaydimi; testlar yangi xulqqa moslashdimi | optimizatsiyani o'lchovsiz qabul qilish |
| Xato tuzatish va qaytarish (rollback) | faqat aytilgan xato; xatoni tutadigan test qo'shildimi | "shu yerda turib boshqasini ham tuzatib qo'yaman" |
| Refactoring va mashina yasagan katta o'zgarish | o'zgarish o'z kodiga nima qiladi | asbobni va jarayonni PR da muhokama qilish |

Greenfield review eng kam uchraydigan tur va kitob uni eng mas'uliyatli payt deb ataydi, chunki keyin shu kodning taxminlari vaqt va masshtab bilan o'zgaradi. Shuning uchun Google da yangi kod va yangi loyiha code review dan **alohida** keng dizayn review dan o'tadi; review esa API kelishilgan dizaynga mosligini, har bir API nuqtasida test borligini va bu testlarning kod taxminlari o'zgarganda yiqilishini, egalar belgilanganini va loyihaning CI ga ulanganini tekshiradi. Kitob yangi loyihadagi birinchi review lardan biri odatda bitta `OWNERS` faylining review i ekanini ham aytadi.

Xato tuzatishda kitobning qoidasi qisqa: boshqa muammolarga tegish vasvasasidan voz kechish kerak, chunki u PR hajmini oshiradi va regressiya testini ham, keyinchalik qaytarishni ham qiyinlashtiradi. Qaytarish o'zgarishi (rollback) soniyalarda yasaladi, lekin u ham review dan o'tadi; va aynan shu sabab har bir o'zgarish kichik va atomar bo'lishini talab qiladi, aks holda qaytarish boshqa bog'liqliklarni sindiradi.

Mashina yasagan o'zgarish alohida qoidaga ega va u [1.7](01-review-nima-uchun-bor-va-nimani-haqiqatda.md#17-qachon-review-foyda-bermaydi) dagi "generatsiya qilingan kodni o'qish vaqtni yoqish" qoidasidan farq qiladi. Bu yerda gap repodagi generatsiya natijasi haqida emas, butun kodbaza bo'ylab yuritilgan avtomatik o'zgarish haqida, va kitob uni review dan o'tkazadi. Lekin review ning qamrovi toraytiriladi: reviewer izohni faqat o'z kodiga xos tashvishlar bilan cheklaydi, asbob yoki jarayonning o'ziga tegmaydi, chunki jarayon allaqachon alohida review dan o'tgan va alohida jamoa unga veto qo'ysa bunday o'zgarishni masshtablash imkonsiz bo'ladi. Asbobga e'tiroz bo'lsa, u PR dan tashqarida, mas'ul guruhga eskalatsiya qilinadi. Qamrovni kengaytirmaslik ham talab qilinadi: asbobni yurgizgan odamda bir vaqtda yuzlab o'zgarish bo'lishi mumkin, shuning uchun bog'liq bo'lmagan savol butun ishni to'xtatadi.

```java
// Xato tuzatish PR i: avval xatoni tutadigan test, keyin bitta tuzatish.
// Review shu ikki fayldan ko'proq narsani kutmaydi.
@Test
void nolMiqdordaKomissiyaOlinmaydi() {                 // INC-102 regressiyasi
    assertThat(payoutService.fee(Money.zero("UZS")))
            .isEqualTo(Money.zero("UZS"));
}
```

Jadvaldagi to'rt savat bir o'q bo'ylab, ya'ni o'zgarishning turi bo'ylab yotadi. Review deb ataladigan yana bir tur esa boshqa o'qda turadi va uni review hisobiga qo'shish eng ko'p uchraydigan chalkashlik. McConnell unga nom beradi: dog-and-pony show, ya'ni mahsulot mijozga namoyish qilinadigan review. Bunday mijoz review lari davlat shartnomalari ostida yozilgan dasturlarda keng tarqalgan, chunki shartnoma ko'pincha talab, dizayn va kod uchun review o'tkazilishini majburiy qiladi; maqsadi esa mijozga loyihaning holati yaxshi ekanini ko'rsatish, demak bu texnik review emas, boshqaruv review i (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.4 (495-bet)).

Kitobning qoidasi qat'iy: mahsulotning texnik sifatini yaxshilash uchun dog-and-pony show ga tayanmang. Unga tayyorgarlik texnik sifatga bilvosita ta'sir qilishi mumkin, lekin odatda vaqtning ko'pi dasturning sifatini oshirishga emas, chiroyli ko'rinadigan taqdimot slaydlarini yasashga ketadi; texnik sifat uchun inspeksiya, walk-through yoki kod o'qishga tayaniladi (21.4 (495-bet)). Jarayon tilida bu ikki amaliy natija beradi: demo yoki steering ko'rsatuv PR ning approve i hisoblanmaydi va review SLA siga kirmaydi, va demo dan chiqqan texnik e'tiroz alohida issue yoki PR ga aylantiriladi, chunki uning o'z review i kerak. Texnik sifat beradigan shakl [rasmiy inspeksiya anatomiyasi](#4012-rasmiy-inspeksiya-anatomiyasi-rollar-bosqichlar-va-tezlik) bo'limida.

## 40.12 Rasmiy inspeksiya anatomiyasi: rollar, bosqichlar va tezlik

Code Complete rasmiy inspeksiyani oddiy review dan ajratadigan belgilarni sanaydi va ro'yxat PR jarayonini sozlash uchun to'g'ridan-to'g'ri foydali: tekshiruv ro'yxati diqqatni avval muammo bo'lgan joylarga qaratadi; e'tibor faqat xato topishga qaratiladi, tuzatishga emas; reviewer lar oldindan tayyorlanadi va yig'ilishga topilmalar ro'yxati bilan keladi; har qatnashchiga alohida rol beriladi; moderator muallif emas va moderatorlik bo'yicha tayyorgarlik olgan; yig'ilish hamma tayyorlangan bo'lsagina o'tkaziladi; har inspeksiyada ma'lumot yig'iladi va keyingisiga uzatiladi; menejment yig'ilishga kelmaydi.

| Rol | Ishi | PR jarayonida kim bajaradi |
| --- | --- | --- |
| Moderator | tezlikni ushlab turadi, materialni va ro'yxatni tarqatadi, natijani xabar qiladi, keyingi ishni kuzatadi | PR muallifi: javobsiz izoh qolmasligi uning ishi |
| Author (muallif) | roli ataylab kichik: kod o'zi gapirishi kerak; noaniq joyni tushuntiradi va aniqlashtirishni o'z ustiga oladi | muallif |
| Reviewer | xato topadi, asosan tayyorlanish paytida | reviewer |
| Scribe (yozuvchi) | topilmalarni va keyingi ishlarni yozadi; muallif ham, moderator ham bo'lmaydi | PR ning izoh oqimi |

Qatnashchi soni ham o'lchangan: inspeksiya uchtadan kam bo'lmaydi (alohida moderator, muallif va reviewer bo'lishi uchun), an'anaviy yuqori chegara oltita, va kuzatuvlar ikki-uchdan ko'p reviewer topilgan xato sonini oshirmasligini ko'rsatadi. Bu [2.4](02-review-iqtisodi-xato-narxi-navbat-va-pr.md#24-reviewer-soni-ikkinchidan-keyin-qaytim-tushadi) dagi qaytim pasayishining mustaqil o'lchovi.

```text
# Yuqori xavfli PR ni inspeksiya tartibida o'tkazish: vaqt rejasi.
# Kitobdagi tezlik mo'ljallari qavs ichida.

1 Planning     muallif materialni va tekshiruv ro'yxatini beradi
2 Preparation  har reviewer YAKKA o'qiydi
                 (ilova kodi ~500 qator/soat, tizim kodi ~125 qator/soat)
3 Meeting      topilmalar bo'yicha 60-90 daqiqa
                 (~150-200 bo'sh va izohsiz ifoda/soat; 2 soatdan oshmaydi)
4 Report       bir kun ichida: har topilma turi va og'irligi bilan
5 Rework       tuzatish muallifga biriktiriladi
6 Follow-up    moderator tuzatishlar bajarilganini tekshiradi
7 Third hour   YECHIMLAR shu yerda muhokama qilinadi, meetingda emas

# Kuniga bittadan ko'p inspeksiya rejalashtirilmaydi: diqqat yetmaydi.
```

Ikki qoida alohida e'tiborga arziydi. Birinchi: yig'ilishda yechim muhokama qilinmaydi, topilma tan olinishi bilan muhokama to'xtaydi va keyingisiga o'tiladi; ba'zi guruhlar hatto "bu haqiqatan xatomi" degan bahsni ham taqiqlaydi, chunki kimdir chalkashib xato deb o'ylagan bo'lsa, demak kod yoki hujjat aniqlashtirilishi kerak. Yechimlar uchun ixtiyoriy "uchinchi soat" yig'ilishi ajratiladi. Ikkinchi: kitob bosqichlarni olib tashlash yoki birlashtirishga qarshi ogohlantiradi, chunki tashkilotlar buni qilganda tejagandan ko'proq yo'qotgan.

Tekshiruv ro'yxatining o'zi uchun chegara [toza kod hujjatida](../clean-code/47-birgalikda-ishlash-va-orgatish.md#473-yangi-odamga-toza-kod-standartini-yetkazish) berilgan: bir sahifadan oshmasin.

## 40.13 Qoida va ko'rsatma: mashina nimani majburlaydi

Google kitobi jamoa qoidalarini ikki sinfga ajratadi va bu ajratish review izohining ohangini belgilaydi. Qoida (rule) qonun: u taklif emas, majburiy va hamma uchun bir xil majburlanadi. Ko'rsatma (guidance) esa tavsiya va eng yaxshi amaliyot: unga amal qilish juda maqbul, lekin og'ish uchun joy bor. Kitobning qisqa shakli: qoidalar "shart", ko'rsatmalar "yaxshi bo'lardi".

Majburlash yo'li ham tanlanadi: ijtimoiy (o'rgatish, review) yoki texnik (asbob). Kitob texnik yo'lni ustun qo'yadi va sabablarini sanaydi: tashkilot o'sganda qoida esdan chiqmaydi; yangi odam hamma qoidani bilmaydi; qoidalar vaqt bilan o'zgaradi va hamma joriy holatni eslab turmaydi; qoidaga odam qaraganda u xotiraga yoki hujjatga tayanadi, ikkisi ham ishdan chiqadi. Qo'shimcha foyda - talqin bir xil bo'ladi: skript hamma kirishni qoidaning bitta o'zgarmaydigan ta'rifiga solishtiradi, odam esa o'z moyilliklari bilan qaraydi. Masshtab tomoni ham bor: kompaniya ikki barobar o'ssa, majburlash mehnati ikki barobar o'smaydi.

Chegarasi aniq belgilangan. Birinchi: ba'zi qoidalar ataylab hukm talab qiladi, masalan "kompozitsiya ko'pincha merosdan o'rinliroq" yoki "tutilgan istisnoga javoban hech narsa qilmaslik juda kamdan-kam to'g'ri bo'ladi"; bunday qoidani asbob bajarmaydi. Ikkinchi va muhimrog'i: ba'zi qoidalar texnik emas, ijtimoiy, va kitob ijtimoiy muammoni texnik yechim bilan hal qilishga urinishni ko'pincha noto'g'ri deb ataydi.

PR hajmi aynan shu ikkinchi sinfga kiradi va kitob buni misol sifatida keltiradi. Google kichik o'zgarishni tavsiya qiladi, lekin belgilangan satr chegarasidan oshgan o'zgarishni avtomatik rad etadigan asbob **yo'q**, chunki "kichik" ning ta'rifi noaniq: yuzlab faylga tarqalgan bir xil bir qatorli o'zgarish review uchun oson bo'lishi mumkin, yigirma qatorli o'zgarish esa yon ta'siri bor murakkab mantiq kiritishi mumkin. Hajmni reviewer baholaydi va kerak bo'lsa qaytaradi.

```yaml
# Shu ajratishning CI dagi aksi: formatlash BLOKLAYDI, hajm faqat AYTADI.
name: pr-rules
on: pull_request
jobs:
  majburiy:                                   # qoida: mashina majburlaydi
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./mvnw -q -B spotless:check       # yiqilsa merge bo'lmaydi
      - run: ./mvnw -q -B checkstyle:check

  korsatma:                                   # ko'rsatma: faqat izoh
    runs-on: ubuntu-latest
    continue-on-error: true                   # hajm merge ni bloklamaydi
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: |
          N=$(git diff --numstat origin/${{ github.base_ref }}...HEAD \
              | grep -E '\.(java|kt)$' | awk '{s+=$1+$2} END {print s+0}')
          echo "mantiq satrlari: $N"
          [ "$N" -le 400 ] || echo "OGOHLANTIRISH: PR ni bo'lish tavsiya qilinadi"
```

Formatlash bo'yicha kitobning xulosasi qat'iy: avtomatik formatter o'rtacha hisobda odamdan sezilarli yaxshi ishlaydi va Google formatterni presubmit tekshiruvi bilan majburlaydi, ya'ni formatter diff bersa o'zgarish qabul qilinmaydi. Natijasi review ga bevosita tegishli: formatlash bir xil bajarilganda u review da umuman mavzu bo'lmaydi va mayda uslub izohlariga ketadigan davralar yo'qoladi. Hajm bo'yicha mo'ljallar [2.2](02-review-iqtisodi-xato-narxi-navbat-va-pr.md#22-pr-hajmi-va-topish-darajasi) da.

## 40.14 Review yetukligining ikki darajasi: diffdan tizimga

Orosz review ni "bor yoki yo'q" deb qaramaydi, ikki darajaga ajratadi. Jarayon qurishda bu farq amaliy: birinchi darajani checklist va avtomatika bilan majburlab bo'ladi, ikkinchisi esa reviewer tajribasi bilan o'sadi va uni shablonga sig'dirib bo'lmaydi.

Birinchi daraja diffning o'ziga qaraydi: sarlavha va tavsif tushunarlimi, o'zgarishning "nega" si yozilganmi, kod to'g'rimi, test qamrovi bormi, konvensiyaga mos keladimi. Shu darajada ochiq yaxshilanishlar ko'rsatiladi: tushunish qiyin kod, noaniq nom, izohga olingan o'lik kod, testsiz kod, e'tibordan qolgan chegaraviy holat. Bitta PR ga bir nechta maqsad tiqilgani ham shu darajada aytiladi va o'zgarishni bitta maqsadli bo'laklarga bo'lish taklif qilinadi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 12-bob, 165-166-bet).

Ikkinchi daraja diffdan chiqadi va o'zgarishni tizim kontekstida ko'radi: bu o'zgarish umuman kerakmi, u tizimning boshqa qismlariga nima qiladi, kiritilgan abstraksiya mavjud arxitekturaga mos tushadimi, kodni keyin saqlash osonmi. Shu darajada maintainability kuzatuvlari yoziladi: soddalashtirish mumkin bo'lgan murakkab mantiq, test tuzilishi, takrorlanish (12-bob, 166-bet).

Uchinchi va jarayon uchun eng qimmat xulosa shu ikki darajaning ustida turadi: ikkinchi darajadagi reviewer **takrorlanuvchi** muammoni review ichida emas, review dan tashqarida hal qiladi. Orosz ikkita misol beradi. Nitpick izohlari ko'payib ketsa, bu reviewer ning injiqligi emas, instrument yoki kelishilgan standart yo'qligining belgisi: bunday izohlarning aksariyati avtomatik linter bilan yopiladi, qolgani esa jamoa standart kelishib, keyinroq uni ham avtomatlashtirishi bilan (12-bob, 167-bet). Vaqt zonasi farqidan kelgan kechikish takrorlansa ham javob review jadvalida emas, tizimda: refaktoring, yangi servis yoki interfeys, instrument yaxshilash (12-bob, 168-bet).

| Daraja | Nimaga qaraydi | Jarayonda qayerda yashaydi |
| --- | --- | --- |
| Birinchi | Diff: to'g'rilik, test, nom, konvensiya | PR shabloni ([40.4](#404-pr-shabloni)), CI darvozalari ([40.6](#406-avtomatik-tekshiruvlar-tartibi)) |
| Ikkinchi | Tizim: zarurat, ta'sir, abstraksiya, saqlanuvchanlik | Xavf tabaqalashi ([40.2](#402-xavf-boyicha-tabaqalash)), ega reviewer ([40.1](#401-kim-review-qiladi-codeowners)) |
| Ustki | Takrorlanuvchi muammoning ildizi | Qoidani instrumentga ko'chirish ([40.13](#4013-qoida-va-korsatma-mashina-nimani-majburlaydi)) |

Amaliy o'lchov shundan chiqadi: agar oxirgi o'ttiz PR dagi izohlarning aksariyati birinchi darajada qolsa, muammo reviewer larda emas, avtomatikada. Birinchi darajani mashinaga berib, odam vaqtini ikkinchi darajaga bo'shatish kerak.

## 40.15 Amalda qo'llash

- [ ] `.github/CODEOWNERS` yaratib, migratsiya, xavfsizlik va to'lov yo'llariga maxsus egalar belgilang.
- [ ] Branch protection da "Require conversation resolution" va "Dismiss stale approvals" ni yoqing.
- [ ] Xavf darajasini avtomatik belgilaydigan workflow ni qo'shing.
- [ ] PR shablonini yozib, majburiy qismni 6 banddan oshirmang.
- [ ] CI ni bosqichlarga bo'ling: format va kompilyatsiya 2 daqiqada javob bersin.
- [ ] Review SLA sini kelishib, kutayotgan PR lar haqida kunlik eslatmani sozlang.
- [ ] Katta o'zgarishlar uchun dizayn eskizi va draft PR bosqichlarini joriy qiling.
- [ ] Hotfix siyosatini `REVIEW.md` ga yozib, post-review majburiyatini belgilang.

## Manbalar

- [Google, Speed of Code Reviews](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/speed.md) - bir ish kunlik chegara, javob tezligi va izohli LGTM
- [Google, The Standard of Code Review](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/standard.md) - approve mezoni va kelishmovchilikni hal qilish tartibi
- [Google, Small CLs](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/developer/small-cls.md) - hajm bo'yicha mo'ljallar va "bitta o'zini o'zi to'ldirgan o'zgarish" mezoni
- [Google, Navigating a CL in Review](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/navigate.md) - uch qadamli o'qish tartibi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, "How Code Review Works at Google" - uch turdagi ruxsat (LGTM, egalik, readability), bitlarning bir odamda to'planishi, ikki qadamli oqim va ega beradigan boshqa savollar; boshqaruvning bu darajasi ba'zan og'ir ekani
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, "Ownership" - egalik mulk emas, vakillik; ierarxik qo'shiluv; ro'yxatni qisqa saqlash; egalikni initsiatsiya marosimi qilmaslik
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 3-bob, "Readability: Standardized Mentorship Through Code Review" - jarayonning narxi (tashqi reviewer, qo'shimcha davra, chiziqli masshtablanish) va o'lchov natijasi: readability olgan muallifning o'zgarishi kamroq vaqt oladi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, "Types of Code Reviews" - to'rtta tur va har birining diqqati; greenfield da dizayn review alohida, API testlari va OWNERS fayli; xato tuzatishda boshqa muammoga tegmaslik; rollback ham review dan o'tishi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, "Refactorings and Large-Scale Changes" - mashina yasagan o'zgarish review dan o'tadi, lekin izoh o'z kodi bilan cheklanadi, jarayonga veto yo'q, e'tiroz PR dan tashqarida eskalatsiya qilinadi, qamrov kengaytirilmaydi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Formal Inspections" (485-bet) - inspeksiyani oddiy review dan ajratadigan belgilar ro'yxati
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.4 "Dog-and-Pony Shows" (495-bet) - mijozga namoyish ko'rinishidagi review, uning davlat shartnomalaridagi o'rni, maqsadi texnik emas boshqaruv review i ekani, texnik sifat uchun unga tayanmaslik va vaqtning slaydlarga ketishi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Roles During an Inspection" (486-487-betlar) - moderator, author, reviewer va scribe rollari; qatnashchi soni uchtadan kam, oltitadan ko'p bo'lmasligi; ikki-uchdan ko'p reviewer topilmani oshirmasligi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "General Procedure for an Inspection" (487-489-betlar) - bosqichlar; tayyorlanish tezligi 500 va 125 qator/soat; yig'ilish tezligi 150-200 ifoda/soat va 2 soat chegarasi; kuniga bitta inspeksiya; yechimlarni yig'ilishda muhokama qilmaslik va uchinchi soat yig'ilishi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Fine-Tuning the Inspection" (489-bet) - bosqichni olib tashlash yoki birlashtirish tejagandan ko'proq yo'qotgani
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 8-bob - qoida va ko'rsatma farqi ("shart" va "yaxshi bo'lardi")
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 8-bob, "Applying the Rules" - majburlashni avtomatlashtirish sabablari; hukm talab qiladigan qoidalar; ijtimoiy qoidani texnik yechim bilan hal qilmaslik; satr chegarasi bo'yicha avtomatik rad etish yo'qligi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 8-bob, "Code Formatters" - avtomatik formatter o'rtacha odamdan yaxshi; presubmit bilan majburlash; formatlash review da mavzu bo'lmay qolishi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 12-bob, "Code Reviews" (165-168-betlar) - review ning ikki darajasi (diff va tizim konteksti); nitpick ko'payishi instrument yoki standart yo'qligining belgisi; takrorlanuvchi muammoni review dan tashqarida hal qilish

---

[&larr; 39. Observability review](39-observability-review.md) · [Mundarija](README.md) · [41. Review madaniyati, til va kelishmovchilik &rarr;](41-review-madaniyati-til-va-kelishmovchilik.md)
