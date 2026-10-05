---
name: code-review
description: Review a diff or pull request in a Java/Spring/PostgreSQL project - find the defect, decide block or approve, and word the comment with the rule behind it. Covers design and dependency direction, clean code and patterns on a diff, Java and concurrency defects, Spring proxies and transactions, JPA/SQL, migrations and races, security, tests, API compatibility, performance, review process and AI-written code. Use when asked to review a PR or diff ("PR ni ko'rib chiq", "diffni tekshir"), to self-review before opening one, or to phrase a review comment.
---

# Kod review

44 bob, 445 bo'lim. To'liq hujjat: `docs/code-review/README.md`.

## Qoida

Savol bitta: **oldingizda diff turibdi, unda nimani ko'rasiz, nimani
so'raysiz va nimani to'xtatasiz.**

Review tartibi:
1. **Niyat** - bu o'zgarish nimani hal qilmoqchi? PR tavsifi va kod bir
   narsani aytyaptimi?
2. **Mashina topadiganini qidirmang** - avval statik tahlil va test nima
   deganini ko'ring (`tools/doc.sh show code-review 5.2`).
3. **Invariant** - diff qanday qoidani buzishi mumkin?
4. **Xavf yuzasi** - qayerga tegdi: pul, autentifikatsiya, migratsiya,
   tashqi chaqiruv? Shu joylarda sinchkovlik oshadi.
5. **To'xtatish yoki o'tkazish** - blocker va nit ni aralashtirmang.

Review izohi kodga emas, qoidaga ishora qilishi kerak: nima buzilgan, nega
muhim, qanday tuzatish mumkin. Tayyor iboralar: `tools/doc.sh show code-review 44.3`,
xulosa shablonlari `44.4`, izoh prefikslari (blocker, suggest, nit) `4.9`.

`/manguberdi` shu sessiyada chaqirilgan bo'lsa review `review` aktyoriga
beriladi va yuqoridagi tartib asosiy sessiyada alohida yurgizilmaydi; bu
skill o'shanda faqat bob jadvali.

## Vazifa - bob jadvali

Jadval bobni topadi. Bobni butun o'qimang: `tools/doc.sh outline code-review <bob>`
bilan bo'limni tanlab, `tools/doc.sh show code-review <bob.bo'lim>` bilan o'qing.

| Vazifa | Bob fayli |
|---|---|
| Review nega bor, iqtisodi, PR hajmi | `docs/code-review/01-review-nima-uchun-bor-va-nimani-haqiqatda.md`, `docs/code-review/02-review-iqtisodi-xato-narxi-navbat-va-pr.md` |
| Tahlil apparati: niyat, invariant, xavf yuzasi | `docs/code-review/03-reviewer-ning-tahlil-apparati-niyat.md` |
| Diffni o'qish mexanikasi | `docs/code-review/04-diffni-oqish-mexanikasi.md` |
| Mashina vs odam: Sonar dan oldin topish | `docs/code-review/05-mashina-va-odam-sonarqube-dan-oldin-topish.md` |
| Arxitektura, bog'liqlik yo'nalishi, abstraksiya | `docs/code-review/06-arxitektura-review-qatlam-chegara-bogliqlik.md`, `docs/code-review/07-bogliqlik-koheziya-va-abstraksiya-review.md` |
| Clean code va SOLID ni diffda tekshirish | `docs/code-review/08-clean-code-review-nomlash-kognitiv-yuk.md`, `docs/code-review/09-solid-va-dizayn-printsiplarini-diffda.md` |
| Yo'q pattern, noto'g'ri pattern, smell katalogi | `docs/code-review/10-dizayn-pattern-review-i-yoq-patternni-korish.md`, `docs/code-review/11-dizayn-pattern-review-ii-notogri-va.md`, `docs/code-review/12-code-smell-va-anti-pattern-katalogi-diffda.md` |
| Domen modeli: invariant, agregat, chegara | `docs/code-review/13-domen-modeli-review-invariant-agregat.md` |
| Java tili darajasidagi xatolar katalogi | `docs/code-review/14-java-tili-darajasidagi-xatolar-katalogi.md` |
| Holat, mutability, concurrency; resurs va GC | `docs/code-review/15-holat-mutability-va-concurrency-review.md`, `docs/code-review/16-resurs-xotira-va-gc-bosimi-review.md` |
| `record`, `sealed`, virtual thread review | `docs/code-review/17-zamonaviy-java-review-record-sealed-pattern.md` |
| Bean, kontekst, proxy mexanikasi | `docs/code-review/18-bean-kontekst-va-proxy-mexanikasi-review.md` |
| Tranzaksiya chegarasi | `docs/code-review/19-tranzaksiya-chegarasi-review.md` |
| Web qatlami: DTO, validatsiya, xato javobi | `docs/code-review/20-web-qatlami-review-dto-validatsiya-xato.md` |
| Konfiguratsiya, profil, feature flag | `docs/code-review/21-konfiguratsiya-profil-va-feature-flag-review.md` |
| Tashqi integratsiya: timeout, retry, broker | `docs/code-review/22-tashqi-integratsiya-review-timeout-retry.md` |
| JPA/Hibernate, SQL va indeks, migratsiya | `docs/code-review/23-jpa-va-hibernate-review.md`, `docs/code-review/24-sql-sorov-rejasi-va-indeks-review.md`, `docs/code-review/25-migratsiya-review-qulf-backfill-orqaga.md` |
| Ma'lumot to'g'riligi, izolyatsiya va poyga holatlari | `docs/code-review/26-malumot-togriligi-va-turlar-review.md`, `docs/code-review/27-izolyatsiya-poyga-holatlari-va-xabar.md` |
| **Xavfsizlik review**: metodika, injection, authn/authz | `docs/code-review/28-xavfsizlik-review-metodikasi.md`, `docs/code-review/29-injection-review-sql-va-boshqalar.md`, `docs/code-review/30-autentifikatsiya-va-avtorizatsiya-review.md` |
| SSRF, deserializatsiya, fayl; secret va kripto; supply chain | `docs/code-review/31-kirish-va-chiqish-xavfsizligi-ssrf.md`, `docs/code-review/32-secret-maxfiy-malumot-va-kriptografiya.md`, `docs/code-review/33-bogliqlik-va-supply-chain-review.md` |
| Test to'liqligi, test sifati, test turi | `docs/code-review/34-test-toliqligini-review-qilish.md`, `docs/code-review/35-test-sifati-review-assertion-izolyatsiya.md`, `docs/code-review/36-test-turi-va-integratsion-test-review.md` |
| API moslik, performance, observability diffdan | `docs/code-review/37-api-moslik-va-breaking-change-review.md`, `docs/code-review/38-performance-review-diffdan.md`, `docs/code-review/39-observability-review.md` |
| Jarayon, madaniyat va kelishmovchilik, metrikalar | `docs/code-review/40-review-jarayonini-qurish.md`, `docs/code-review/41-review-madaniyati-til-va-kelishmovchilik.md`, `docs/code-review/42-review-metrikalari.md` |
| AI yozgan kodni review qilish | `docs/code-review/43-ai-yozgan-kodni-review-qilish-va-ai-bilan.md` |
| Shablonlar, checklistlar, reviewer yetukligi | `docs/code-review/44-shablonlar-checklistlar-va-reviewer.md` |

## Chegara

- Mexanikaning o'zi kerak bo'lsa: `docs/architect/README.md`
- Pattern katalogi: `docs/patterns/README.md`
- Test yozish texnikasi: `docs/testing/README.md`
- Sonar qoidasi va kaliti: `docs/sonarqube/README.md`
- Qator darajasidagi toza kod qoidasi: `docs/clean-code/README.md`

## Asboblar

Diffni o'qishdan oldin mexanik qismni mashinaga bering, ko'z faqat
qolganiga qarasin:

```bash
python3 tools/rules_for.py --no-mark --diff [--cached]  # yoki --no-mark <fayllar>; boblar, punktlar, check_code topilmalari
python3 tools/schema_from_entities.py <src> --only-findings  # entity o'zgargan bo'lsa
tools/doc.sh outline code-review <bob>          # bobdagi bo'limlar
tools/doc.sh show code-review <bob.bo'lim>      # butun bob emas, faqat o'sha bo'lim
tools/doc.sh checklist code-review <bob>        # qolgan tekshiruv punktlari
```

Reviewer yozmaydi, shuning uchun `--no-mark`: belgini kodni yozadigan
aktyor o'zi qo'yadi, aks holda `check_code` darvozasi o'chadi.

`check_code.py` alohida yurgizilmaydi: uning topilmalari Sonar kaliti bilan
`rules_for` chiqishidagi `# Mashina topgani` bo'limida turadi. Ro'yxat
kesilgan bo'lsa (sarlavhadagi son ko'rsatilganidan ko'p), qolganini
`python3 tools/check_code.py <fayl>` bilan fayl bo'yicha oling.
