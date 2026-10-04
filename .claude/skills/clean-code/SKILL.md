---
name: clean-code
description: Decide whether the line being written is clean, and fix it when it is not - naming, function size and arguments, conditionals and loops, comments and Javadoc, formatting, encapsulation, equals/hashCode contracts, immutability, inheritance vs composition, error handling, Java pitfalls (numbers and money, strings and regex, date and time, collections and generics, lambdas and streams), clean Spring/JPA/SQL/logging code, test-code cleanliness, the code-smell catalogue and refactoring moves. Use when naming something, when a method or class has grown, when a comment is being added, when reviewing one's own code before a PR, when the user asks "bu nom to'g'rimi", "buni qanday refaktoring qilaman", or names a smell (long method, god class, feature envy, primitive obsession, shotgun surgery).
---

# Toza kod qoidalari

49 bob, 533 bo'lim. To'liq hujjat: `docs/clean-code/README.md`.

## Qoida

Bu hujjat bitta savolga javob beradi: **klaviatura ostida tug'ilayotgan shu
qator toza yoki yo'q.** Arxitektura qarori boshqa hujjatda, pattern tanlash
boshqa hujjatda.

Toza kod tekshiruvi tartibi:
1. **Nom** maqsadni ochib beryaptimi, yoki implementatsiyani aytyaptimi?
2. **Funksiya** bitta ish qilyaptimi, nechta argument oladi?
3. **Shart** erta qaytish bilan yassilanadimi?
4. **Izoh** "nega" ni aytyaptimi yoki "nima" ni takrorlayaptimi?
5. **Holat** o'zgarmas bo'lishi mumkinmi?

Har bob `Amalda qo'llash` tekshiruv ro'yxati bilan tugaydi.

## Vazifa - bob jadvali

| Vazifa | Bob fayli |
|---|---|
| Toza kod nima, nega qimmat | `docs/clean-code/01-toza-kod-nima-va-nega-qimmat.md` |
| Nomlash qoidalari, nom turlari konvensiyasi | `docs/clean-code/02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md`, `docs/clean-code/03-nom-turlari-boyicha-aniq-konvensiyalar.md` |
| Funksiya kichikligi, bitta ish, argumentlar | `docs/clean-code/04-funksiya-kichiklik-va-bitta-ish.md`, `docs/clean-code/05-funksiya-argumentlari.md` |
| Shart, mantiq, erta qaytish, sikl va to'plam | `docs/clean-code/06-shart-mantiq-va-boshqaruv-oqimi.md`, `docs/clean-code/07-sikl-iteratsiya-va-toplam-bilan-ishlash.md` |
| Izoh: yaxshi va yomon katalogi, Javadoc | `docs/clean-code/08-izoh-qoidalari-yaxshi-izohlar.md`, `docs/clean-code/09-yomon-izohlar-katalogi.md`, `docs/clean-code/10-javadoc-va-api-hujjati.md` |
| Vertikal va gorizontal formatlash, diff gigiyenasi | `docs/clean-code/11-vertikal-formatlash.md`, `docs/clean-code/12-gorizontal-formatlash-va-kod-uslubi.md`, `docs/clean-code/13-formatlashni-avtomatlashtirish-va-diff.md` |
| Inkapsulyatsiya, obyekt vs ma'lumot tuzilmasi | `docs/clean-code/14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md` |
| `equals`/`hashCode`/`compareTo` shartnomalari | `docs/clean-code/15-tenglik-hash-va-obyekt-shartnomalari.md` |
| O'zgarmaslik va holat boshqaruvi | `docs/clean-code/16-ozgarmaslik-va-holat-boshqaruvi-kod.md` |
| Vorislik, kompozitsiya, polimorfizm | `docs/clean-code/17-vorislik-kompozitsiya-va-polimorfizm.md` |
| Xato bilan ishlash, istisno mexanikasi, resurslar | `docs/clean-code/18-xato-bilan-ishlash-qoidalari.md`, `docs/clean-code/19-istisno-mexanikasi-va-resurslar.md` |
| Son va pul (`BigDecimal`), satr va regex | `docs/clean-code/20-primitiv-son-va-pul.md`, `docs/clean-code/21-satr-matn-va-regex.md` |
| Sana, vaqt, mintaqa | `docs/clean-code/22-sana-vaqt-va-mintaqa.md` |
| To'plamlar, generiklar, lambda va oqim | `docs/clean-code/23-toplamlar-va-generiklar-gigiyenasi.md`, `docs/clean-code/24-lambda-oqim-va-funksional-uslub-tozaligi.md` |
| Java umumiy tuzoqlari | `docs/clean-code/25-java-kodidagi-umumiy-tuzoqlar.md` |
| Spring, REST, JPA/SQL, log kodining tozaligi | `docs/clean-code/26-spring-kodining-tozaligi.md`, `docs/clean-code/27-rest-api-kodining-oqilishi.md`, `docs/clean-code/28-jpa-va-sql-kodining-tozaligi.md`, `docs/clean-code/29-log-kodining-tozaligi.md` |
| Test kodining tozaligi, TDD intizomi | `docs/clean-code/30-test-kodi-ham-ishlab-chiqarish-kodi.md`, `docs/clean-code/31-tdd-intizomi-va-kod-dizayniga-tasiri.md` |
| **Kod hidi katalogi** | `docs/clean-code/32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md`, `docs/clean-code/33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md` |
| Evristikalarning to'liq ro'yxati | `docs/clean-code/34-toza-kod-evristikalarining-toliq-royxati.md` |
| **Refaktoring harakatlari katalogi** | `docs/clean-code/35-refaktoring-harakatlari-katalogi-i-funksiya.md`, `docs/clean-code/36-refaktoring-harakatlari-katalogi-ii-malumot.md`, `docs/clean-code/37-refaktoring-harakatlari-katalogi-iii-shart.md` |
| Refaktoringni xavfsiz bajarish | `docs/clean-code/38-refaktoringni-xavfsiz-bajarish.md` |
| Build, versiya nazorati, kichik qadamlar, statik tahlil | 39-42 boblar |
| Professional intizom, "yo'q" deyish, baholash, mentorlik | 43-47 boblar |
| Tezkor ma'lumotnoma va o'z-o'zini baholash | `docs/clean-code/48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md`, `docs/clean-code/49-oz-ozini-baholash-toza-kod-yetukligi.md` |

## Chegara

Bu hujjat qoida beradi, arxitektura qarori bermaydi:

- SOLID, GRASP, anti-pattern katalogi - `docs/patterns/README.md`
- chegara, abstraksiya, murakkablik qarori - `docs/architect/README.md`
- diffni review qilish - `docs/code-review/README.md`
- Sonar qoidasi va uning kalitlari - `docs/sonarqube/README.md`
