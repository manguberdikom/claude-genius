<!-- doc: clean-code | chapter: 47 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 47. Birgalikda ishlash va o'rgatish (Collaboration and Mentoring)

<details>
<summary>Bu bobdagi 6 bo'lim</summary>

- [47.1 Kodga egalik: shaxsiy emas, jamoaviy](#471-kodga-egalik-shaxsiy-emas-jamoaviy)
- [47.2 Ustoz-shogird modeli](#472-ustoz-shogird-modeli)
- [47.3 Yangi odamga toza kod standartini yetkazish](#473-yangi-odamga-toza-kod-standartini-yetkazish)
- [47.4 Review ni o'rgatish vositasiga aylantirish](#474-review-ni-orgatish-vositasiga-aylantirish)
- [47.5 Jamoa kelishuvi (working agreement) yozish](#475-jamoa-kelishuvi-working-agreement-yozish)
- [47.6 Amalda qo'llash](#476-amalda-qollash)

</details>


Toza kod jamoaviy natija: bir odam yolg'iz uni saqlab qola olmaydi. Bu bobda jamoaviy egalik, ustoz-shogird munosabati, standartni yetkazish va jamoa kelishuvi. Code review mexanikasi va texnik yetakchilik [arxitektor hujjatidagi](../architect/README.md) code review va texnik yetakchilik bo'limida.

## 47.1 Kodga egalik: shaxsiy emas, jamoaviy

"Bu mening kodim" munosabati ikki zarar keltiradi: muallif tanqidni shaxsiy qabul qiladi, va boshqalar shu kodga tegishdan qochadi. Natijada bilim bir odamda to'planadi va kod o'sishdan to'xtaydi.

Jamoaviy egalik amaliy qoidalarga tayanadi: har bir fayl har qanday jamoa a'zosi tomonidan o'zgartirilishi mumkin; `@author` tegi ishlatilmaydi (9.5); va review izohlari kodga, odamga emas, qaratiladi.

```text
Yomon: "Nega sen bu yerda Optional ishlatmagansan?"
Yaxshi: "Bu metod null qaytarishi mumkinmi? Optional aniqroq bo'lardi."
```

Jamoaviy egalik "hech kim javob bermaydi" degani emas: CODEOWNERS bilan sohaga mas'ul belgilanadi ([arxitektor hujjatidagi](../architect/README.md) jamoaning bilim xaritasi bo'limi), lekin mas'ullik to'siq emas, bilim markazi bo'ladi.

## 47.2 Ustoz-shogird modeli

Dasturlash kasbini kitobdan o'rganib bo'lmaydi: uning katta qismi - qaror qabul qilish usuli, va u faqat kuzatish va qaytarma aloqa bilan uzatiladi. Shu sababli ustoz-shogird munosabati eng samarali o'qitish shakli bo'lib qolgan.

| Daraja | Nima kerak | Qanday beriladi |
|---|---|---|
| Yangi boshlovchi | aniq qoida va chegara | shablon kod, aniq vazifa, tez review |
| O'rtacha | sabablarni tushunish | "nega shunday" suhbatlari, juftlikda ishlash |
| Mustaqil | qaror sifatiga qaytarma aloqa | dizayn muhokamasi, ADR review |
| Tajribali | boshqalarni o'qitish | mentorlik, standart belgilash |

## 47.3 Yangi odamga toza kod standartini yetkazish

Standartni hujjat bilan yetkazish eng kam samarali usul: hujjat o'qiladi va esdan chiqadi. Samarali usullar tartibi boshqa.

1. **Namuna kod**: shablon loyiha va mavjud kod - yangi odam shunga qaraydi ([arxitektor hujjatidagi](../architect/README.md) standart o'rnatish bo'limi).
2. **Mashina**: formatter va linter qoidalarni darhol o'rgatadi (13, 42 boblar).
3. **Review**: birinchi besh PR da batafsil, sabab bilan izohlar.
4. **Juftlikda ishlash**: birinchi haftada bir-ikki sessiya (41.7).
5. **Hujjat**: qolgan qism uchun havola sifatida ([48-bob](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)).

Eng tez xato - yangi odamga 50 qoidadan iborat hujjat berib, keyin review da hammasini talab qilish. To'g'ri yondashuv: birinchi haftada 5 qoida, keyin bosqichma-bosqich.

## 47.4 Review ni o'rgatish vositasiga aylantirish

Review ning o'qitish funksiyasi [arxitektor hujjatidagi](../architect/README.md) review orqali o'rgatish bo'limida ko'rilgan. Bu yerda qo'shimcha amaliy qoidalar: izohda **sabab** bo'lishi, muqobil taklif bo'lishi, va izohlar soni cheklangan bo'lishi.

| Izoh shakli | Samarasi |
|---|---|
| "Bu yomon" | nol |
| "Buni o'zgartir" | past (nega?) |
| "Bu metod ikki ish qiladi; `validate` ni ajratsak testlash osonlashadi" | yuqori |
| "Shu holatda `Optional` afzal, chunki ... (hujjatda 18.7)" | yuqori |
| 30 ta izoh bir PR da | nol (prioritet yo'q) |
| 3 ta muhim izoh + "qolgani ixtiyoriy" | yuqori |

Qo'shimcha texnika: izohlarga prefiks qo'yish - `[majburiy]`, `[taklif]`, `[savol]`, `[nit]`. Bu prioritetni darhol ko'rsatadi va muallif vaqtini tejaydi.

## 47.5 Jamoa kelishuvi (working agreement) yozish

Jamoa kelishuvi - og'zaki qoidalarni yozma shaklga keltirish. Uning qiymati bahsni yopishda: "biz shunday kelishganmiz" argumenti did haqidagi muhokamani to'xtatadi.

```markdown
# Jamoa kelishuvi

## Kod
- Formatlash: Spotless (google-java-format AOSP); review da uslub muhokama qilinmaydi.
- Yangi value object lar `record` sifatida yoziladi.
- Pul `Money` turida; `double` taqiqlangan (ArchUnit tekshiradi).
- Konstruktor inyeksiyasi; maydon inyeksiyasi taqiqlangan.
- Lombok: `@Getter`, `@RequiredArgsConstructor`, `@Slf4j` ruxsat; `@Data`, `@SneakyThrows` taqiqlangan.

## Commit va PR
- Atomik commit; formatlash va mantiq alohida commitda.
- Conventional commits prefikslari.
- PR 400 qatordan katta bo'lsa bo'linadi.
- PR ochishdan oldin o'zini review qilish ro'yxati to'ldiriladi.

## Review
- Navbat: PR ochilgandan 4 ish soati ichida birinchi javob.
- Izoh prefikslari: [majburiy], [taklif], [savol], [nit].
- Majburiy izohlar soni 5 dan oshsa, juftlikda ishlashga o'tiladi.

## Tugatish
- Ishni tugatish ta'rifi: `docs/definition-of-done.md`.
- Testsiz xatti-harakat o'zgarishi merge qilinmaydi.

## Qayta ko'rish
- Bu kelishuv har chorakda ko'rib chiqiladi; oxirgi: 2026-01-15.
```

## 47.6 Amalda qo'llash

- [ ] `@author` teglarini olib tashlab, egalikni CODEOWNERS ga ko'chiring.
- [ ] Review izohlarini kodga qaratilgan shaklga o'tkazish uchun 47.1 dagi misollarni jamoaga ko'rsating.
- [ ] Izoh prefikslarini ([majburiy], [taklif], [savol], [nit]) joriy qiling.
- [ ] Yangi odam uchun birinchi hafta rejasini yozing: 5 qoida, shablon loyiha, ikki juftlik sessiyasi.
- [ ] Shablon loyihani (yoki mavjud eng toza modulni) namuna sifatida belgilang va havola bering.
- [ ] Jamoa kelishuvini 47.5 shabloni bo'yicha yozib, repoda saqlang.
- [ ] Kelishuvni har chorakda ko'rib chiqish sanasini kalendarda belgilang.
- [ ] Har bir kritik tizimda kamida ikki odam o'zgartirish kirita olishini ta'minlang ([arxitektor hujjatidagi](../architect/README.md) jamoaning bilim xaritasi bo'limi).

---

[&larr; 46. Vaqt, diqqat va mashq](46-vaqt-diqqat-va-mashq.md) · [Mundarija](README.md) · [48. Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari &rarr;](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)
