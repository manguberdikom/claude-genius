<!-- doc: code-review | chapter: 43 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 43. AI yozgan kodni review qilish va AI bilan review qilish (Reviewing AI-Generated Code)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [43.1 AI yozgan kodning xato profili](#431-ai-yozgan-kodning-xato-profili)
- [43.2 Eng xavfli naqsh: ishonchli ko'rinadigan noto'g'ri kod](#432-eng-xavfli-naqsh-ishonchli-korinadigan-notogri-kod)
- [43.3 AI yozgan kod uchun qo'shimcha review savollari](#433-ai-yozgan-kod-uchun-qoshimcha-review-savollari)
- [43.4 Kontekst bermaslikning oqibati](#434-kontekst-bermaslikning-oqibati)
- [43.5 AI ni review da ishlatish](#435-ai-ni-review-da-ishlatish)
- [43.6 AI review ni sozlash](#436-ai-review-ni-sozlash)
- [43.7 Muallif mas'uliyati o'zgarmaydi](#437-muallif-masuliyati-ozgarmaydi)
- [43.8 Review checklisti: AI yozgan kod](#438-review-checklisti-ai-yozgan-kod)
- [43.9 Amalda qo'llash](#439-amalda-qollash)

</details>


AI yordamida yozilgan kod review ga yangi sinf muammolar olib keladi. Kod sintaktik to'g'ri, uslubi toza, nomlari yaxshi va testlari bor - ya'ni yuzaki review dan osongina o'tadi. Lekin uning xatolari odam xatolaridan boshqacha taqsimlangan: kontekstni bilmaslik, ishonchli ko'rinadigan noto'g'ri taxminlar va mavjud kod bilan nomuvofiqlik. Bu bob shu farqlarni va AI ni review da ishlatishni oladi.

## 43.1 AI yozgan kodning xato profili

| Xato turi | Nega yuzaga keladi | Review da qanday topiladi |
| --- | --- | --- |
| Loyiha konvensiyasini buzish | Umumiy naqshlardan yozilgan | Mavjud kod bilan taqqoslash |
| Mavjud yordamchi kodni takrorlash | Repoda nima borligini to'liq bilmaydi | "Bu allaqachon bormi" savoli |
| Ishonchli ko'rinadigan noto'g'ri API | Mavjud bo'lmagan metod yoki parametr | Kompilyatsiya va hujjat |
| Eskirgan yondashuv | O'rganish ma'lumotlaridagi eski naqshlar | Versiya va deprecation tekshiruvi |
| Yuzaki test | Kod bilan bir xil taxminlardan | Assertion sifati (35.1) |
| Chegaraviy holatlarning yo'qligi | Talab to'liq berilmagan | Holatlar jadvali (34.1) |
| Xavfsizlik kontekstini bilmaslik | Qaysi ma'lumot ishonchli - bilmaydi | Trust boundary (28.2) |
| Ortiqcha umumiylashtirish | "To'g'ri" naqshlarga moyillik | YAGNI savoli |
| Jim o'zgargan xulq | Refactoring paytida mantiq o'zgaradi | Diffni satr-satr o'qish |
| Noto'g'ri konfiguratsiya qiymatlari | Loyiha hajmini bilmaydi | Raqamlarni tekshirish (21.1) |

## 43.2 Eng xavfli naqsh: ishonchli ko'rinadigan noto'g'ri kod

Odam yozgan noto'g'ri kod ko'pincha noto'g'ri ko'rinadi: nomlari chalkash, tuzilishi g'alati, izohlari yo'q. AI yozgan noto'g'ri kod to'g'ri ko'rinadi. Shu sababli review usuli o'zgaradi - tashqi ko'rinishga ishonch kamayadi va har bir taxmin tekshiriladi.

```java
// AI yozgan kod: toza, o'qiladigan, izohli - va noto'g'ri.
/**
 * Buyurtma summasini valyuta kursiga ko'ra hisoblaydi.
 */
public Money convertTotal(Order order, Currency target) {
    BigDecimal rate = rateService.getRate(order.currency(), target);
    return new Money(
        order.total().amount().multiply(rate).setScale(2, RoundingMode.HALF_UP),
        target);
}
// Review topilmalari (hech biri ko'rinishdan bilinmaydi):
// 1) `setScale(2)` - lekin ba'zi valyutalarda 0 yoki 3 kasr (JPY, KWD).
//    Loyihada `Money` ning o'zi `currency.getDefaultFractionDigits()`
//    ishlatadi - bu kod shu konvensiyani buzadi.
// 2) `getRate` null qaytarishi mumkin (mavjud kodda shunday) - NPE.
// 3) Yaxlitlash qoidasi HALF_UP, lekin loyihada moliyaviy hisob uchun
//    HALF_EVEN kelishilgan (ADR-14).
// 4) Teskari yo'nalishda konvertatsiya aniqlikni yo'qotadi -
//    mavjud `CurrencyConverter` bu holatni hisobga oladi, bu kod yo'q.
```

## 43.3 AI yozgan kod uchun qo'shimcha review savollari

1. Bu funksiya loyihada allaqachon bormi. AI mavjud yordamchi klassni ko'rmasligi mumkin, natijada uchinchi `DateUtils` paydo bo'ladi.
2. Ishlatilgan API haqiqatan shunday ishlaydimi. Parametr tartibi, qaytish turi, istisno xulqi tekshiriladi.
3. Loyiha konvensiyasiga mosmi. `Money`, `Clock`, xato ishlash, log formati - hammasi loyihada o'z shakliga ega.
4. Testlar kod bilan bir xil taxminga asoslanganmi. Agar kod `HALF_UP` ishlatsa va test ham `HALF_UP` bilan hisoblangan kutilgan qiymat ishlatsa, test xatoni tutmaydi (35.7).
5. Chegaraviy holatlar qamralganmi. AI odatda happy path uchun test yozadi.
6. Muallif bu kodni tushunadimi. Eng muhim savol: PR muallifi har bir qatorni tushuntirib bera oladimi.

```text
# Review izohi: muallifning tushunishini tekshirish (ayblash emas).
question: Bu yerda `setScale(2, HALF_UP)` ishlatilgan, lekin loyihada
`Money` konstruktori valyutaning kasr xonalarini o'zi qo'llaydi
(Money.java:14) va ADR-14 da moliyaviy yaxlitlash uchun HALF_EVEN
kelishilgan.

Ikki variant: (a) `Money` ning o'z mexanizmidan foydalanish, (b) bu
joyda boshqa qoida kerak bo'lsa, sababini izohda yozish.

Qaysi biri to'g'ri - konvertatsiya mantiqi haqida qanday kelishuv bor?
```

## 43.4 Kontekst bermaslikning oqibati

AI yozgan kodning sifati unga berilgan kontekstga bog'liq. Shu sababli jamoada kontekstni kodga yaqin saqlash review yukini kamaytiradi.

| Mexanizm | Nima qiladi |
| --- | --- |
| `CLAUDE.md` yoki shunga o'xshash fayl | Loyiha konvensiyalari, stek, qoidalar |
| `REVIEW.md` | Review talablari - AI ham, odam ham o'qiydi |
| `GLOSSARY.md` | Domen tili (13.7) |
| ADR lar | Nega shunday qilingan |
| ArchUnit testlari | Qoidalar bajarilishini majburlaydi (5.10) |
| ErrorProne va Semgrep qoidalari | Naqshlarni kompilyatsiyada tutadi |
| Boy domen turlari | `Money`, `OrderId` - noto'g'ri ishlatish qiyinlashadi |

Oxirgi ikki qator eng samarali: konvensiyani hujjatda yozish uni tavsiya qiladi, kod va test bilan majburlash esa buzilishni imkonsiz qiladi. Bu AI yozgan kod uchun ham, yangi jamoa a'zosi uchun ham bir xil ishlaydi.

```markdown
<!-- CLAUDE.md namunasi: AI uchun ham, odam uchun ham kontekst. -->
# Loyiha konvensiyalari

## Stek
Java 21, Spring Boot 3.4, PostgreSQL 16, Flyway, Testcontainers.

## Majburiy qoidalar
- Pul: `Money` turi (BigDecimal + Currency). `double` taqiqlanadi.
- Vaqt: `Instant` saqlashda, `Clock` inyeksiya qilinadi. `LocalDateTime.now()` yo'q.
- ID: tipli (`OrderId`, `CustomerId`), UUID v7.
- Inyeksiya: faqat konstruktor orqali. `@Autowired` maydon taqiqlanadi.
- Tranzaksiya: faqat `application` qatlamida. Ichida tashqi chaqiruv yo'q.
- Domen: `org.springframework` va `jakarta.persistence` importlari yo'q.
- Yozuv endpointlari: idempotentlik kaliti + DB unique constraint.
- Testlar: PostgreSQL (Testcontainers), H2 ishlatilmaydi.
- Xato javoblari: `ProblemDetail`, ichki detallarsiz.

## Qoidalarni majburlash
`ArchitectureRulesTest` va `.semgrep/` da. Yangi qoida qo'shilsa,
avval test, keyin hujjat.

## Nimani qayerdan izlash
- Pul va valyuta: `shared/money/`
- Tashqi integratsiyalar: `infra/adapter/` (portlar `domain/port/`)
- Migratsiyalar: `src/main/resources/db/migration/`
```

## 43.5 AI ni review da ishlatish

AI review ni almashtirmaydi, lekin uning ba'zi qismlarini arzonlashtiradi. Mehnat taqsimoti [5-bobdagi](05-mashina-va-odam-sonarqube-dan-oldin-topish.md) mantiqqa amal qiladi.

| AI yaxshi bajaradigan | AI bajarmaydigan |
| --- | --- |
| Diffni qisqacha tushuntirish | Niyat to'g'riligini baholash |
| Tanish xato naqshlarini topish | Loyiha konteksti va tarixi |
| Yo'q test holatlarini taklif qilish | Qaysi holat biznes uchun muhim |
| Nomlash va o'qiluvchanlik takliflari | Domen tili to'g'riligi |
| Hujjat va izoh yozish | Qaror sabablarini bilish |
| Takrorlangan kodni topish | Takrorlanish ongli yoki yo'qligini bilish |
| Checklist bo'yicha mexanik o'tish | Checklistda yo'q narsani sezish |
| SQL rejasini tushuntirish | Prod hajmi va yuk haqida bilim |

Amaliy yondashuv: AI birinchi o'tishni bajaradi (mexanik tekshiruvlar, yo'q testlar, tanish naqshlar), odam ikkinchi o'tishni bajaradi (niyat, dizayn, xavf, kontekst). AI topilmalari esa boshqa avtomatik instrument topilmalari kabi ko'riladi - tekshirilishi kerak bo'lgan taklif sifatida, hukm sifatida emas.

```text
# AI review topilmasini qanday ko'rish kerak.
AI aytdi: "Bu metodda null tekshiruvi yo'q."

Reviewer tekshiradi:
1) Bu parametr haqiqatan null bo'lishi mumkinmi? (chegarada @Valid bormi)
2) Loyihada null siyosati qanday? (@NullMarked, 5.6)
3) Agar chegarada tekshirilgan bo'lsa - bu topilma noto'g'ri (false positive).

AI topilmalarining katta qismi shunday: texnik jihatdan to'g'ri,
kontekstda ahamiyatsiz. Ularni filtrsiz PR ga yuborish review ni
shovqinga ko'madi va jamoa AI izohlarini e'tiborsiz qoldiradi.
```

## 43.6 AI review ni sozlash

```yaml
# AI review bot i uchun qoidalar: shovqinni kamaytirish.
# Umumiy tamoyillar (aniq vosita nomidan qat'i nazar):
#
# 1) Faqat yuqori ishonchli topilmalarni post qilish.
#    Past ishonchli topilmalar - shovqin, jamoa botni o'chiradi.
#
# 2) Loyiha kontekstini berish: CLAUDE.md, REVIEW.md, GLOSSARY.md.
#
# 3) Mexanik tekshiruvlarni takrorlamaslik: format, import, uslub
#    allaqachon CI da (5.2).
#
# 4) Diqqatni aniq sinflarga qaratish: xavfsizlik, poyga holatlari,
#    yo'q test holatlari, tranzaksiya chegarasi.
#
# 5) Topilma shakli: oqibat + joy + taklif (28.5).
#
# 6) Bot izohi `suggest` darajasida bo'ladi, `blocker` emas - blocker
#    qarorini odam qabul qiladi.
#
# 7) Bot topilmalarining qabul qilinish nisbatini o'lchash: 30 foizdan
#    past bo'lsa, sozlamani o'zgartirish yoki o'chirish kerak.
```

## 43.7 Muallif mas'uliyati o'zgarmaydi

Eng muhim qoida: kodni kim yozgani - odam, AI yoki ikkisi birga - mas'uliyatni o'zgartirmaydi. PR muallifi kodning har bir qatori uchun javob beradi: uni tushunishi, tushuntirib berishi va prodda ishlamay qolsa tuzatishi kerak.

Shu sababli review da qoida oddiy: muallif tushuntirib bera olmaydigan kod merge qilinmaydi. Bu qoida AI dan oldin ham amal qilgan (copy-paste qilingan kod uchun) va u o'zgarmaydi.

```text
# Review izohi: tushunmasdan qo'shilgan kod belgisi.
question: Bu yerda `@Transactional(isolation = SERIALIZABLE)` qo'yilgan.
Bizning boshqa kodda bu daraja faqat ikki joyda ishlatiladi va ikkisida
ham retry mexanizmi bor (27.6), chunki PostgreSQL 40001 xatosini beradi.

Bu yerda retry yo'q. Ikki savol:
1) SERIALIZABLE nega kerak bo'ldi - qaysi poyga holatidan himoya?
2) 40001 xatosi qanday ishlanadi?

Agar SERIALIZABLE kerak bo'lmasa, uni olib tashlash osonroq.
```

## 43.8 Review checklisti: AI yozgan kod

| Savol | Nega |
| --- | --- |
| Muallif har qatorni tushuntirib bera oladimi | Mas'uliyat |
| Bu funksiya loyihada allaqachon bormi | Takrorlanish |
| Loyiha konvensiyalariga mosmi | Nomuvofiqlik |
| Ishlatilgan API haqiqatan shunday ishlaydimi | Noto'g'ri taxmin |
| Testlar kod bilan bir xil taxmindan kelib chiqmaganmi | Yolg'on ishonch |
| Chegaraviy holatlar qamralganmi | Happy path |
| Xavfsizlik konteksti to'g'ri tushunilganmi | Trust boundary |
| Konfiguratsiya raqamlari loyiha hajmiga mosmi | Taxminiy qiymatlar |
| Ortiqcha umumiylashtirish yo'qmi | YAGNI |
| Refactoring paytida xulq jim o'zgarmaganmi | Regressiya |

## 43.9 Amalda qo'llash

- [ ] `CLAUDE.md` (yoki shunga o'xshash kontekst fayli) yozib, loyihaning majburiy konvensiyalarini sanab chiqing.
- [ ] Har bir yozilgan konvensiya uchun uni majburlaydigan mexanizm qo'shing: ArchUnit, ErrorProne, Semgrep yoki tipli domen turi.
- [ ] `GLOSSARY.md` va ADR larni kod bazasida saqlab, kontekstni kodga yaqin tuting.
- [ ] AI yozgan kod uchun qo'shimcha review savollarini checklistga qo'shing.
- [ ] AI review bot i ishlatilsa, uning topilmalari qabul qilinish nisbatini o'lchang va 30 foizdan past bo'lsa sozlang.
- [ ] Bot izohlarini `suggest` darajasida cheklab, `blocker` qarorini odamga qoldiring.
- [ ] "Muallif tushuntirib bera olmaydigan kod merge qilinmaydi" qoidasini `REVIEW.md` ga yozing.
- [ ] Yangi testlarda kutilgan qiymatlar qo'lda yozilganini (kod bilan hisoblanmaganini) tekshirishni review bandiga aylantiring.

---

[&larr; 42. Review metrikalari](42-review-metrikalari.md) · [Mundarija](README.md) · [44. Shablonlar, checklistlar va reviewer yetukligi &rarr;](44-shablonlar-checklistlar-va-reviewer.md)
