<!-- doc: code-review | chapter: 4 | part: I. Review ning mohiyati va iqtisodi -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 4. Diffni o'qish mexanikasi (Reading a Diff)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [4.1 Nega interfeys bergan tartib noto'g'ri](#41-nega-interfeys-bergan-tartib-notogri)
- [4.2 To'g'ri o'qish tartibi: sakkiz qadam](#42-togri-oqish-tartibi-sakkiz-qadam)
- [4.3 Kontekstni tiklash](#43-kontekstni-tiklash)
- [4.4 O'chirilgan kodni o'qish](#44-ochirilgan-kodni-oqish)
- [4.5 Commit tarixini o'qish](#45-commit-tarixini-oqish)
- [4.6 PR ni lokalda olib tekshirish](#46-pr-ni-lokalda-olib-tekshirish)
- [4.7 Katta PR ni xavf nuqtalari bo'yicha o'qish](#47-katta-pr-ni-xavf-nuqtalari-boyicha-oqish)
- [4.8 Izohni qayerga va qanday qo'yish](#48-izohni-qayerga-va-qanday-qoyish)
- [4.9 Izoh darajasini belgilash](#49-izoh-darajasini-belgilash)
- [4.10 O'qish tezligini oshiradigan odatlar](#410-oqish-tezligini-oshiradigan-odatlar)
- [4.11 Amalda qo'llash](#411-amalda-qollash)

</details>


Diff - mashina uchun qulay, odam uchun noqulay format. U fayllarni alifbo bo'yicha beradi, kontekstni uch satrga qisqartiradi, ko'chirilgan kodni yangi kod deb ko'rsatadi va o'chirilgan kodning kim tomonidan ishlatilganini aytmaydi. Shu sababli diffni interfeys bergan tartibda o'qish - eng keng tarqalgan review xatosi. Bu bob o'qish tartibini va instrumentlarini beradi.

## 4.1 Nega interfeys bergan tartib noto'g'ri

GitHub diffni fayl yo'li bo'yicha alifbo tartibida ko'rsatadi. Natijada reviewer `controller` dan boshlaydi, `domain` ni o'rtada ko'radi, `resources/db/migration` ni esa oxirida - charchagan holda. Ammo xavf taqsimoti teskari: migratsiya eng xavfli, controller eng arzon.

Ikkinchi muammo - uch satrli kontekst. Metodning o'rtasidagi o'zgarish ko'rinadi, lekin uning boshida qanday tekshiruv borligi ko'rinmaydi. Reviewer esa shu ko'rinmagan kontekstga asoslanib "yaxshi" deb o'ylaydi.

## 4.2 To'g'ri o'qish tartibi: sakkiz qadam

| Qadam | Nima o'qiladi | Nima izlanadi |
| --- | --- | --- |
| 1 | PR tavsifi va tiket | Niyat, qamrov, aytilmagan narsalar |
| 2 | Fayllar ro'yxati va statistika | Shakl, kutilmagan fayllar, hajm |
| 3 | Migratsiya va sxema | Qulf, orqaga moslik, indeks, constraint |
| 4 | Public API: controller shakli, DTO, event, interfeys | Tashqi moslik, breaking change |
| 5 | Domen va biznes mantiqi | Invariant, chegaraviy holat, poyga |
| 6 | Infratuzilma: repository, client, mapper | N+1, timeout, mapping yo'qotishi |
| 7 | Konfiguratsiya va bog'liqliklar | Timeout, pool, secret, yangi kutubxona |
| 8 | Testlar | To'liqlik, assertion sifati, yolg'on ishonch |

Testlar oxirida o'qiladi, lekin bu ularning muhimligi kamligini bildirmaydi. Sabab boshqa: mantiqni o'qigandan keyin reviewer qanday testlar bo'lishi kerakligini biladi, va shu bilimdan testlardagi bo'shliqni ko'radi. Teskari tartibda testlar reviewer ning fikrini bog'lab qo'yadi.

```bash
# 2-qadamni bir buyruq bilan: PR ning shaklini ko'rish.
BASE=origin/main
git diff --stat $BASE...HEAD | tail -1
echo "--- xavfli yo'llar bu PR da tegilganmi:"
git diff --name-only $BASE...HEAD | grep -E \
  'db/(migration|changelog)|SecurityConfig|application.*\.(yml|properties)|pom\.xml|build\.gradle' \
  || echo "yo'q"
echo "--- yangi fayllar:"
git diff --name-status $BASE...HEAD | awk '$1=="A"{print $2}'
echo "--- o'chirilgan fayllar:"
git diff --name-status $BASE...HEAD | awk '$1=="D"{print $2}'
echo "--- ko'chirilgan/nomi o'zgargan:"
git diff --name-status -M $BASE...HEAD | awk '$1 ~ /^R/{print $2" -> "$3}'
```

## 4.3 Kontekstni tiklash

O'zgargan satrni tushunish uchun uning atrofidagi kod kerak. Uch satr kamlik qiladi. Ikki yo'l bor: faylni to'liq ochib o'qish, yoki diffga funksiya konteksti qo'shish.

```bash
# Funksiyaning butun tanasini kontekst sifatida ko'rsatish.
git diff --function-context origin/main...HEAD -- src/main/java/.../OrderService.java

# Bo'sh joy o'zgarishini e'tiborsiz qoldirish (indentatsiya shovqinini olib tashlaydi).
git diff -w origin/main...HEAD

# Ko'chirilgan kodni "yangi" deb ko'rsatmaslik: -M nomi o'zgarishini, -C
# ko'chirishni aniqlaydi. Katta refactoringda diffni bir necha baravar kichraytiradi.
git diff -M -C --find-copies-harder origin/main...HEAD

# Faqat so'z darajasidagi farq: uzun satrlarda nima o'zgarganini ko'rish.
git diff --word-diff=color origin/main...HEAD -- '*.sql'

# Bu o'zgarish qachon va nega kirgan: satr tarixini kuzatish.
git log -L 120,160:src/main/java/com/acme/order/OrderService.java

# Shu simvol tarixda qachon qo'shilgan va olib tashlangan.
git log -S 'findTop20ByCustomerId' --oneline -- '*.java'

# Regex bo'yicha: timeout sozlamalari tarixda qanday o'zgargan.
git log -G 'connection-timeout' --oneline -p -- '*.yml' | head -40
```

`git log -S` review da alohida qimmatli: diffda bir tekshiruv olib tashlangan bo'lsa, u qachon va qanday sabab bilan qo'shilganini ko'rsatadi. Ko'p hollarda u o'tgan incidentdan keyin qo'yilgan bo'ladi, va uni olib tashlash o'sha incidentni qaytaradi.

## 4.4 O'chirilgan kodni o'qish

Qo'shilgan kod diqqatni tortadi, o'chirilgan kod esa e'tibordan chetda qoladi. Lekin review da eng xavfli o'zgarishlar aynan o'chirishlardir: olib tashlangan `if`, olib tashlangan `catch`, olib tashlangan test, kamaytirilgan log darajasi.

Har bir o'chirilgan blok uchun uch savol: bu nima uchun qo'yilgan edi (`git log -S` yoki blame), uni olib tashlash nimani ochib qo'yadi, va uning o'rniga nima keldi. Agar javob "endi kerak emas" bo'lsa, javob yetarli emas - nega kerak emas degan tushuntirish kerak.

```bash
# Faqat o'chirilgan satrlarni ko'rish: review ning eng kam qilinadigan qadami.
git diff origin/main...HEAD | grep -E '^-' | grep -vE '^---' | less

# O'chirilgan tekshiruvlar va xato ishlash joylari - alohida diqqat.
git diff origin/main...HEAD | grep -E '^-' \
  | grep -iE 'if \(|throw|catch|assert|validate|@Valid|@PreAuthorize|requireNonNull|UNIQUE|NOT NULL'

# O'chirilgan testlar: eng xavfli signal.
git diff --numstat origin/main...HEAD -- '*[Tt]est*' | awk '$2>0{print $2" satr test kodidan olib tashlangan: "$3}'
```

## 4.5 Commit tarixini o'qish

Commitlar muallifning fikr yo'lini ko'rsatadi. "Fix", "fix again", "revert fix" ketma-ketligi - muallif o'zi ham tushunmagan joy borligini bildiradi, va aynan shu joy review ning asosiy nuqtasi.

```bash
# Commitlar va ularning hajmi: fikr yo'lini ko'rish.
git log --oneline --stat origin/main..HEAD | head -60

# "fix", "wip", "revert" naqshlari: noaniqlik belgisi.
git log --oneline origin/main..HEAD | grep -icE 'fix|wip|revert|try|temp'

# Birinchi va oxirgi holatni taqqoslash: oraliq urinishlarni o'tkazib yuborish.
git diff origin/main...HEAD --stat
```

Diqqat: squash merge ishlatadigan jamoada commit tarixi review dan keyin yo'qoladi, shu sababli uni review paytida o'qish yagona imkoniyat.

## 4.6 PR ni lokalda olib tekshirish

Yuqori xavfli PR ni faqat brauzerda o'qish yetarli emas. Lokalda olish uch narsani beradi: IDE navigatsiyasi (chaqiruvchilarga o'tish), testlarni ishga tushirish, va migratsiyani real bazada sinash.

```bash
# PR ni lokalda olish va tekshirish (GitHub).
gh pr checkout 1423
# Yoki toza git bilan:
#   git fetch origin pull/1423/head:pr-1423 && git switch pr-1423

# 1) Tez tekshiruvlar: kompilyatsiya, uslub, statik tahlil.
./mvnw -q -T1C verify -DskipITs

# 2) Faqat o'zgargan modullarning testlari (vaqtni tejash).
./mvnw -q -pl order-service -am test

# 3) Migratsiyani real PostgreSQL da sinash (Testcontainers yoki docker).
docker run -d --name rv -e POSTGRES_PASSWORD=p -p 55432:5432 postgres:16
./mvnw -q flyway:migrate -Dflyway.url=jdbc:postgresql://localhost:55432/postgres \
        -Dflyway.user=postgres -Dflyway.password=p

# 4) Migratsiya qancha qulf oldi va qancha turdi - log dan ko'rish.
docker logs rv 2>&1 | grep -iE 'lock|duration|error' | tail

# 5) Tozalash.
docker rm -f rv
```

## 4.7 Katta PR ni xavf nuqtalari bo'yicha o'qish

Ba'zan katta PR ni bo'lish imkoni yo'q: framework yangilanishi, avtomatik refactoring, generated kodning qayta chiqishi. Bunday holatda satrlarni o'qish o'rniga xavf nuqtalari bo'yicha yuriladi va bu usul izohda ochiq aytiladi.

```bash
# 3000 satrli framework yangilanishini xavf nuqtalari bo'yicha o'qish.
BASE=origin/main

# 1) Faqat qo'lda yozilgan kod o'zgarishlari (generated emas).
git diff --stat $BASE...HEAD -- 'src/main/java' ':!**/generated/**'

# 2) Xulq o'zgartiradigan naqshlar: konfiguratsiya va standart qiymatlar.
git diff $BASE...HEAD | grep -E '^[+-]' \
  | grep -iE 'timeout|pool|retry|ttl|batch|fetch|isolation|readOnly|lazy|cache'

# 3) Xavfsizlikka tegadigan joylar.
git diff $BASE...HEAD -- '*Security*' '*Filter*' '*Auth*' | head -100

# 4) Bog'liqlik daraxtidagi haqiqiy o'zgarish (pom diffidan ishonchliroq).
git stash -q 2>/dev/null; ./mvnw -q dependency:tree -DoutputFile=/tmp/after.txt
git switch -q $BASE && ./mvnw -q dependency:tree -DoutputFile=/tmp/before.txt
git switch -q - ; diff /tmp/before.txt /tmp/after.txt | head -40
```

To'rtinchi qadam ayniqsa muhim: `pom.xml` da bitta versiya o'zgarsa, transitive bog'liqliklarda o'nlab o'zgarish bo'lishi mumkin va diff ularni ko'rsatmaydi.

## 4.8 Izohni qayerga va qanday qo'yish

Izohning joyi uning taqdirini belgilaydi. Satr izohi aniq, lekin kontekstdan ajralgan. Fayl izohi dizayn haqida gapirish uchun qulay. Umumiy izoh xulosa va asosiy savol uchun.

| Izoh turi | Joy | Misol |
| --- | --- | --- |
| Aniq xato | O'sha satr | "bu yerda `seats <= 0` tekshirilmagan" |
| Takrorlanadigan naqsh | Birinchi uchragan joy + "qolgan joylarda ham" | "shu mapping 3 joyda takrorlangan" |
| Dizayn savoli | Umumiy izoh | "refund tranzaksiya ichida - outbox ni muhokama qilaylik" |
| Yo'q narsa | Eng mos fayl yoki umumiy | "migratsiyaning orqaga yo'li yo'q" |
| Maqtov | O'sha satr | "bu yerda idempotentlik kaliti to'g'ri qo'yilgan" |

Oxirgi qatorni tashlab ketmaslik kerak. To'g'ri qilingan qiyin joyni ko'rsatish review ni tekshiruvdan muloqotga aylantiradi va keyingi PR da shu yondashuv takrorlanadi.

## 4.9 Izoh darajasini belgilash

Muallif izohni o'qiganida birinchi savoli: "bu majburiymi". Agar javob izohda bo'lmasa, muallif taxmin qiladi va taxmin ko'pincha noto'g'ri bo'ladi. Shu sababli har bir izoh prefiks oladi.

```text
blocker: idempotentlik kaliti bo'yicha UNIQUE indeks yo'q. Ikki parallel
         so'rov ikki bron yaratadi. Migratsiyaga unique indeks qo'shish kerak.

suggest: shu mapping uchun MapStruct ishlatsak, 40 satr qo'lda yozilgan
         setter yo'qoladi. Majburiy emas, lekin keyingi maydon qo'shilganda
         shu joy esdan chiqadi.

question: bu timeout 30 sekund qilib qo'yilgan. Tashqi servisning p99 i
          qancha? Agar 2 sekund bo'lsa, 30 sekund thread ni bekor egallaydi.

nit: `tmp` o'rniga `pendingItems` nomi aniqroq bo'ladi.

praise: `FOR UPDATE SKIP LOCKED` bu yerda to'g'ri tanlov, workerlar
        bir-birini kutmaydi.
```

`blocker` izohida har doim sabab va oqibat bo'lishi kerak, aks holda u buyruqqa o'xshaydi va qarshilik keltiradi. "Nima bo'ladi" tushuntirilsa, muallif ko'pincha o'zi yaxshiroq yechim taklif qiladi.

## 4.10 O'qish tezligini oshiradigan odatlar

Birinchi odat: fayllarni o'qish tartibini o'zgartirish (GitHub da "File filter" va "Viewed" belgilari bilan). Migratsiya va konfiguratsiyani birinchi ochish.

Ikkinchi odat: `Viewed` belgisini ishlatish - ikkinchi o'tishda nimaga qaytish kerakligini eslab turadi.

Uchinchi odat: generated va lock fayllarni filtrdan chiqarish. `package-lock.json` yoki `*.pb.java` ni o'qish - vaqtni yoqish.

To'rtinchi odat: diffni ikki oynada o'qish - biri diff, ikkinchisi to'liq fayl. Kontekst savollarining yarmi shu bilan yo'qoladi.

Beshinchi odat: review ni yozma xulosadan boshlab, keyin izohlarni yozish. Bu reviewer ni avval umumiy rasmni ko'rishga majbur qiladi.

## 4.11 Amalda qo'llash

- [ ] Sakkiz qadamli o'qish tartibini keyingi besh PR da qo'llab, migratsiya va konfiguratsiyani birinchi o'qishni odat qiling.
- [ ] `scripts/review-shape.sh` skriptini qo'shing: PR statistikasi, xavfli yo'llar, yangi/o'chirilgan fayllar.
- [ ] Har PR da faqat o'chirilgan satrlarni alohida o'qib chiqing va olib tashlangan `if`, `catch`, test uchun sabab so'rang.
- [ ] `git diff -M -C --find-copies-harder` ni refactoring PR larida ishlatib, diff hajmining qanchaga kamayishini ko'ring.
- [ ] Olib tashlangan tekshiruvlar uchun `git log -S` bilan ularning qo'shilish sababini toping.
- [ ] Yuqori xavfli PR larni lokalda `gh pr checkout` bilan olib, testlarni va migratsiyani ishga tushirishni majburiy qilib qo'ying.
- [ ] Bog'liqlik versiyasi o'zgargan PR larda `dependency:tree` farqini taqqoslang.
- [ ] Izoh prefikslari (`blocker`, `suggest`, `question`, `nit`, `praise`) ni jamoada kelishib, `REVIEW.md` ga yozing.

---

[&larr; 3. Reviewer ning tahlil apparati: niyat, invariant, xavf yuzasi](03-reviewer-ning-tahlil-apparati-niyat.md) · [Mundarija](README.md) · [5. Mashina va odam: SonarQube dan oldin topish &rarr;](05-mashina-va-odam-sonarqube-dan-oldin-topish.md)
