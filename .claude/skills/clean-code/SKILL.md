---
name: clean-code
description: Decide whether the line being written is clean and fix it when it is not - naming, function size and arguments, conditionals, comments and Javadoc, formatting, encapsulation, equals/hashCode, immutability, inheritance vs composition, error handling, Java pitfalls (money, strings, dates, collections, streams), clean Spring/JPA/logging and test code, code smells and refactoring moves. Use when naming something, when a method or class has grown, when a comment is being added, when the user asks "bu nom to'g'rimi", "buni qanday refaktoring qilaman", or names a smell (long method, god class, feature envy, primitive obsession).
---

# Toza kod qoidalari

## Qoida

Bu hujjat bitta savolga javob beradi: **klaviatura ostida tug'ilayotgan shu
qator toza yoki yo'q.** Arxitektura qarori boshqa hujjatda, pattern tanlash
boshqa hujjatda.

Mezon `rules_for` chiqishidagi `# Umumiy yozish qoidalari`
(`tools/retsept/umumiy-kod.md`): avval shu ish bor metoddami (clean-code
32.2), holat bitta metoddan o'zgaradimi (clean-code 16.6), keyin nom,
funksiya, shart, izoh.

Har bob `Amalda qo'llash` tekshiruv ro'yxati bilan tugaydi.

`/manguberdi` shu sessiyada chaqirilgan bo'lsa kod o'zgarishi aktyorga
beriladi (`dasturchi`); bu skill o'shanda faqat bob jadvali.

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
| Bir qadamli build, mahalliy qaytish halqasi | `docs/clean-code/39-bir-qadamli-build-va-mahalliy-qaytish.md` |
| Versiya nazorati gigiyenasi, commit | `docs/clean-code/40-versiya-nazorati-gigiyenasi.md` |
| Kichik qadamlar bilan o'zgartirish | `docs/clean-code/41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md` |
| Statik tahlil va avtomatik qoidalar | `docs/clean-code/42-statik-tahlil-va-avtomatik-qoidalar.md` |
| Professional mas'uliyat, "yo'q" deyish, baholash va muddat, vaqt va diqqat, mentorlik | `docs/clean-code/43-professional-masuliyat.md`, `docs/clean-code/44-yoq-va-ha-deyish-majburiyat-tili.md`, `docs/clean-code/45-baholash-muddat-va-bosim.md`, `docs/clean-code/46-vaqt-diqqat-va-mashq.md`, `docs/clean-code/47-birgalikda-ishlash-va-orgatish.md` |
| Tezkor ma'lumotnoma va o'z-o'zini baholash | `docs/clean-code/48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md`, `docs/clean-code/49-oz-ozini-baholash-toza-kod-yetukligi.md` |

## Chegara

Bu hujjat qoida beradi, arxitektura qarori bermaydi:

- SOLID, GRASP (patterns 26), anti-pattern katalogi (patterns 25) - `design-patterns` skilli
- chegara, abstraksiya, murakkablik qarori - `architect-review` skilli
- diffni review qilish, PR dan oldin o'z diffini ko'rish - `code-review` skilli
- Sonar qoidasi va uning kalitlari - `sonarqube-fix` skilli

## Asboblar

```bash
python3 tools/rules_for.py --vazifa="<vazifa>" <fayl>   # Java yozishdan OLDIN majburiy
python3 tools/check_code.py <fayl>     # yozgandan keyin mexanik qoidalar
python3 tools/metod_bormi.py <src> <so'zlar>  # bor metod; --ozgartiradi <maydon>: yozuvchilar; --audit: refaktoring ro'yxati
tools/doc.sh outline clean-code <bob>    # bobdagi bo'limlar
tools/doc.sh show clean-code <bob.bo'lim> # faqat o'sha bo'lim
tools/doc.sh checklist clean-code <bob>  # shu bobning tekshiruv punktlari
```
