<!-- doc: clean-code | chapter: 41 | part: XI. Kod bazasi va jarayon gigiyenasi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 41. O'zgarishni kiritish jarayoni: kichik qadamlar (Working in Small Steps)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [41.1 Ish boshlashdan oldin: muammoni yozib olish](#411-ish-boshlashdan-oldin-muammoni-yozib-olish)
- [41.2 Oldin tushunish, keyin o'zgartirish](#412-oldin-tushunish-keyin-ozgartirish)
- [41.3 Kodni o'qish texnikalari](#413-kodni-oqish-texnikalari)
- [41.4 Birinchi ishlaydigan versiya va keyin tozalash](#414-birinchi-ishlaydigan-versiya-va-keyin-tozalash)
- [41.5 Yarim ishni boshqarish va feature flag](#415-yarim-ishni-boshqarish-va-feature-flag)
- [41.6 O'zini review qilish ro'yxati](#416-ozini-review-qilish-royxati)
- [41.7 Pair va mob programming mexanikasi](#417-pair-va-mob-programming-mexanikasi)
- [41.8 Ishni tugatish ta'rifi (definition of done)](#418-ishni-tugatish-tarifi-definition-of-done)
- [41.9 Amalda qo'llash](#419-amalda-qollash)

</details>


Toza kod yozish usuli ham ahamiyatga ega: bir xil natijaga olib boradigan ikki yo'ldan biri xato ehtimolini bir necha barobar kamaytiradi. Bu bobda o'zgarish kiritishning amaliy tartibi: tushunishdan boshlash, kichik qadamlar, o'zini review qilish, va tugatish ta'rifi.

## 41.1 Ish boshlashdan oldin: muammoni yozib olish

Kodga tegishdan oldin bir-ikki gapda muammoni yozib olish eng arzon xato to'suvchi: u talabning noaniq joylarini darhol ko'rsatadi. Agar muammoni yozib bo'lmasa, u hali tushunilmagan.

```markdown
## Muammo
Bank fayli USD yozuvlarini UZS hisobiga qo'shib yuboradi (INC-2291).

## Kutilgan xatti-harakat
Valyuta mos kelmasa, qator rad etiladi, audit log'ga yoziladi, qolgan fayl davom etadi.

## Tegadigan joylar
SettlementImporter (parsing), SettlementRow (validatsiya), audit log.

## Qanday tekshiramiz
Aralash valyutali fayl bilan integratsion test; rad etilgan qatorlar soni metrikada.
```

## 41.2 Oldin tushunish, keyin o'zgartirish

Evristika G21: algoritmni **tushunish** kerak, uning ishlashini kuzatish yetarli emas. Amalda bu shunday ko'rinadi: o'zgartirish kiritishdan oldin mavjud kodning nima qilayotganini aytib bera olish kerak.

Tushunishni tekshirish usuli: mavjud xatti-harakat uchun test yozish ([arxitektor hujjatidagi](../architect/README.md) xavfsizlik to'ri va xatti-harakatni qayd etuvchi test bo'limi). Test o'tsa - tushunish to'g'ri; yiqilsa - taxmin xato edi va bu o'zgartirishdan **oldin** bilish qimmatli.

## 41.3 Kodni o'qish texnikalari

Katta kod bazasini o'qish alohida ko'nikma va unda ishlaydigan texnikalar bor.

| Texnika | Qanday | Qachon |
|---|---|---|
| Kirish nuqtasidan | controller yoki konsumerdan boshlash | yangi xususiyat |
| Teskari yo'nalishda | xatodan stack trace bo'yicha yuqoriga | xato tuzatish |
| Ma'lumot oqimi bo'ylab | bir maydonni kiritishdan saqlanishiga qadar kuzatish | ma'lumot xatosi |
| Test orqali | mavjud testlarni o'qib shartnomani tushunish | yangi modul |
| Tarix orqali | `git log -S` bilan kod qachon va nega kiritilganini topish | sirli kod |
| Debugger bilan | nuqta qo'yib holatni ko'rish | murakkab oqim |
| Chizma orqali | chaqiruv grafini qo'lda chizish | chalkash bog'liqlik |

Oxirgi texnika eng kam ishlatiladi va eng samarali: 15 daqiqa qog'ozda chizish bir soatlik debug ni almashtiradi.

## 41.4 Birinchi ishlaydigan versiya va keyin tozalash

4.10 da ko'rilgan tartib ish darajasida ham ishlaydi: oldin ishlaydigan, keyin toza. Buning sababi psixologik - toza kod yozishga urinish bir vaqtda ikki muammoni (nima qilish va qanday qilish) hal qilishni talab qiladi va ikkisi ham sekinlashadi.

Muhim shart: tozalash **o'sha ish ichida** bajariladi, keyinga qoldirilmaydi (1.3). Amaliy usul: ishlaydigan versiyani lokal commit qilib, keyin tozalash commitlari qo'shish va push dan oldin `rebase -i` bilan tartiblash (40.5).

## 41.5 Yarim ishni boshqarish va feature flag

Katta xususiyatni kichik PR larga bo'lishning asosiy vositasi - feature flag: kod merge qilinadi, lekin yoqilmaydi. Konfiguratsiya murakkabligi va har bir flag ning narxi [arxitektor hujjatidagi](../architect/README.md) konfiguratsiya murakkabligi bo'limida; bu yerda kod gigiyenasi.

```java
// yaxshi: flag bitta joyda o'qiladi, mantiq tarqalmaydi
@Service
class SettlementImporter {

    private final boolean currencyCheckEnabled;

    SettlementImporter(SettlementProperties properties) {
        this.currencyCheckEnabled = properties.currencyCheckEnabled();
    }

    private boolean isValid(SettlementRow row) {
        if (currencyCheckEnabled && !row.hasSupportedCurrency()) return false;
        return row.amount().isPositive();
    }
}
```

Flag intizomi uch qoidadan iborat: flag ning **o'chirish sanasi** bo'lishi (TODO bilan, 8.7), flag soni cheklangan bo'lishi, va flag olib tashlanganda eski yo'l ham o'chirilishi.

## 41.6 O'zini review qilish ro'yxati

PR ni boshqaga berishdan oldin uni o'zi review qilish eng arzon sifat nazorati: reviewer vaqtini tejaydi va xatolarning katta qismini topadi.

| Tekshiruv | Savol |
|---|---|
| Diff ni to'liq o'qish | har bir qator kerakmi? |
| Qoldirilgan tafsilot | debug log, izohga olingan kod, `TODO` qoldimi? |
| Nomlar | har bir yangi nom [2-bob](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md) qoidalariga mos keladimi? |
| Testlar | yangi xatti-harakatning har bir shoxi qamralganmi? |
| Chegaraviy holatlar | bo'sh, `null`, maksimal, manfiy sinalganmi? |
| Xato yo'li | istisno konteksti bormi, log bir joydami? |
| Qaytarish | bu o'zgarishni qaytarish osonmi? |
| Hujjat | public API o'zgargan bo'lsa Javadoc yangilandimi? |
| Migratsiya | sxema o'zgarishi orqaga mos keladimi? |
| Hajm | PR ni bo'lish kerakmi? (40.6) |

```bash
# O'zini review qilish uchun: PR diff ini xuddi reviewer ko'rganidek ko'rish
git diff origin/main...HEAD

# Qoldirilgan tafsilotlarni qidirish
git diff origin/main...HEAD | grep -nE '^\+.*(System\.out|printStackTrace|TODO|FIXME|\.only\()'
```

## 41.7 Pair va mob programming mexanikasi

Juftlikda ishlash review ning real vaqtdagi shakli va u ba'zi vazifalarda ancha samarali: murakkab domen mantiqi, yangi odamni o'qitish, incident tahlili.

| Shakl | Qanday | Qachon |
|---|---|---|
| Driver/navigator | biri yozadi, biri o'ylaydi; 15-25 daqiqada almashadi | murakkab mantiq |
| Ping-pong (TDD) | biri test yozadi, ikkinchisi o'tkazadi | TDD o'rganish |
| Strong-style | g'oya navigatordan, klaviatura driverda | bilim uzatish |
| Mob | butun jamoa bitta ekranda | arxitektura qarori, yangi modul |
| Solo + review | odatiy ish | kundalik vazifalar |

Juftlikda ishlash hamma vazifa uchun emas: oddiy, aniq ishlarda u resursni ikki barobar sarflaydi va foyda bermaydi.

## 41.8 Ishni tugatish ta'rifi (definition of done)

"Tayyor" so'zining ma'nosi kelishilmasa, ish hech qachon tugamaydi: kod yozildi, lekin test yo'q; test bor, lekin hujjat yo'q; hammasi bor, lekin monitoring yo'q. Yozilgan ta'rif shu noaniqlikni yopadi.

```markdown
## Ish tugadi deb hisoblanadi, agar:
- [ ] Kod yozilgan va o'zi review qilingan (41.6)
- [ ] Unit va kerakli integratsion testlar yozilgan, CI yashil
- [ ] Formatlash va statik tahlil o'tgan (13, 42)
- [ ] Public API o'zgarsa Javadoc yangilangan (10)
- [ ] Migratsiya orqaga mos va to'xtashsiz (28.9)
- [ ] Yangi xatti-harakat uchun metrika yoki log bor (29)
- [ ] Xato yo'li sinalgan va kontekst bilan log qilinadi (19)
- [ ] Feature flag bo'lsa, o'chirish sanasi yozilgan (41.5)
- [ ] PR tavsifida "nega" yozilgan (40.2)
- [ ] Review izohlari yopilgan yoki javob berilgan
```

## 41.9 Amalda qo'llash

- [ ] Har bir vazifani boshlashdan oldin 41.1 shablonini to'ldirish odatini joriy qiling.
- [ ] Mavjud kodga tegishdan oldin xatti-harakatni qayd etuvchi test yozishni standart qiling.
- [ ] 41.3 jadvalidagi texnikalardan kamida uchtasini keyingi ish davomida ongli ravishda sinab ko'ring.
- [ ] Feature flag lar ro'yxatini yuritib, har biriga o'chirish sanasi va egasini belgilang.
- [ ] 41.6 ro'yxatini PR shabloniga kiritib, o'zini review qilishni majburiy qadam qiling.
- [ ] `git diff` bo'yicha qoldirilgan tafsilot (debug log, `TODO`) skriptini pre-push hook ga qo'shing.
- [ ] Juftlikda ishlash uchun mos vazifa turlarini jamoa bilan kelishib oling.
- [ ] Ishni tugatish ta'rifini yozib, jamoa kelishuviga va PR shabloniga kiriting.

---

[&larr; 40. Versiya nazorati gigiyenasi](40-versiya-nazorati-gigiyenasi.md) · [Mundarija](README.md) · [42. Statik tahlil va avtomatik qoidalar &rarr;](42-statik-tahlil-va-avtomatik-qoidalar.md)
