<!-- doc: clean-code | chapter: 41 | part: XI. Kod bazasi va jarayon gigiyenasi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 41. O'zgarishni kiritish jarayoni: kichik qadamlar (Working in Small Steps)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [41.1 Ish boshlashdan oldin: muammoni yozib olish](#411-ish-boshlashdan-oldin-muammoni-yozib-olish)
- [41.2 Oldin tushunish, keyin o'zgartirish](#412-oldin-tushunish-keyin-ozgartirish)
- [41.3 Kodni o'qish texnikalari](#413-kodni-oqish-texnikalari)
- [41.4 Birinchi ishlaydigan versiya va keyin tozalash](#414-birinchi-ishlaydigan-versiya-va-keyin-tozalash)
- [41.5 Yarim ishni boshqarish va feature flag](#415-yarim-ishni-boshqarish-va-feature-flag)
- [41.6 O'zini review qilish ro'yxati](#416-ozini-review-qilish-royxati)
- [41.7 Pair va mob programming mexanikasi](#417-pair-va-mob-programming-mexanikasi)
- [41.8 Ishni tugatish ta'rifi (definition of done)](#418-ishni-tugatish-tarifi-definition-of-done)
- [41.9 Shaxsiy yozuvlar: kod xaritasi, buyruq ro'yxati va takrorlanadigan izoh](#419-shaxsiy-yozuvlar-kod-xaritasi-buyruq-royxati-va-takrorlanadigan-izoh)
- [41.10 Amalda qo'llash](#4110-amalda-qollash)

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

Evristika G21 ("Understand the Algorithm"): algoritmni **tushunish** kerak, uning ishlashini kuzatish yetarli emas. Amalda bu shunday ko'rinadi: o'zgartirish kiritishdan oldin mavjud kodning nima qilayotganini aytib bera olish kerak.

Bu yerda evristikani teskari o'qish xavfi bor va u keng tarqalgan: "test o'tdi, demak tushundim". G21 aynan shuni rad etadi. Martin ning so'zi qat'iy: funksiyani tugatgan deb hisoblashdan oldin uning qanday ishlashini tushunganingga ishonch hosil qil, "it is not good enough that it passes all the tests", yechim to'g'ri ekanini BILISH kerak. Ya'ni testning yashil bo'lishi tushunishning dalili emas, u faqat sen o'ylab topgan holatlarning o'tganini ko'rsatadi.

G21 ning o'z tavsiyasi boshqa: bu bilimni olishning eng yaxshi yo'li ko'pincha funksiyani shunchalik toza va ifodali holga refaktoring qilish, uning qanday ishlashi ko'rinib qolsin.

Shunga qaramay mavjud xatti-harakat uchun test yozish foydali, faqat boshqa maqsad bilan: u tushunishni ISBOTLAMAYDI, lekin o'zgartirish paytida nimani buzganingni ko'rsatadi, ya'ni xavfsizlik to'ri bo'lib xizmat qiladi ([arxitektor hujjatidagi](../architect/README.md) xavfsizlik to'ri va xatti-harakatni qayd etuvchi test bo'limi). Test yiqilsa, taxmin xato edi va buni o'zgartirishdan **oldin** bilish qimmatli; test o'tsa, bu faqat shu holatlar buzilmaganini bildiradi.

## 41.3 Kodni o'qish texnikalari

Katta kod bazasini o'qish alohida ko'nikma va unda ishlaydigan texnikalar bor.

| Texnika | Qanday | Qachon |
|---|---|---|
| Kirish nuqtasidan | controller yoki konsumerdan boshlash | yangi xususiyat |
| Teskari yo'nalishda | xatodan stack trace bo'yicha yuqoriga | xato tuzatish |
| Ma'lumot oqimi bo'ylab | bir maydonni kiritishdan saqlanishiga qadar kuzatish | ma'lumot xatosi |
| Test orqali | mavjud testlarni o'qib shartnomani tushunish | yangi modul |
| Tarix orqali | `git log -S` va `git log -G` bilan kod qachon va nega kiritilganini topish | sirli kod |
| Debugger bilan | nuqta qo'yib holatni ko'rish | murakkab oqim |
| Chizma orqali | chaqiruv grafini qo'lda chizish | chalkash bog'liqlik |

Tarix bo'yicha qidirishda ikkita bayroqni ajratish kerak, aks holda "bu kod tarixda yo'q" degan xato xulosa chiqadi. `-S<satr>` satrning UCHRASH SONINI o'zgartirgan commit larni topadi (qo'shilgan yoki o'chirilgan), `-G<regex>` esa patch matnida mos keladigan qator qo'shilgan yoki o'chirilgan commit larni topadi. Git hujjatidagi misol farqni aniq ko'rsatadi: bitta faylda `hit = frotz(nitfol, mf2.ptr, 1, 0);` qatori `return frotz(nitfol, two->ptr, 1, 0);` ga almashtirilgan bo'lsa, `git log -G"frotz\(nitfol"` shu commit ni ko'rsatadi, `git log -S"frotz\(nitfol" --pickaxe-regex` esa KO'RSATMAYDI, chunki satrning uchrash soni o'zgarmagan.

```bash
# Nom qachon paydo bo'lgan va qachon yo'qolgan (uchrash soni o'zgargan joylar)
git log -S 'SettlementImporter' --oneline

# Shu qatorga TEGIB o'tgan hamma commit (ko'chirish va tahrir ham)
git log -G 'SettlementImporter' --oneline

# Topilgan commit da shu faylga tegishli hamma o'zgarishni ko'rish
git log -S 'SettlementImporter' --pickaxe-all -p -- src/main/java
```

Jadvalning oxirgi qatori, chizma orqali o'qish, eng kam ishlatiladigan texnika. Uning foydasi o'lchanmagan, lekin amaliy mulohaza shu: chalkash bog'liqlikda chaqiruv grafini qo'lda chizish bir nechta debug seansini almashtiradi, chunki u butun rasmni bir vaqtda ko'rsatadi.

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

Diff ni ko'rishda uch nuqta ataylab qo'yilgan va ikki nuqta bilan almashtirilmaydi. Git hujjatiga ko'ra `git diff A...B` `git diff $(git merge-base A B) B` ga teng, ya'ni u faqat SENING branchingda qilingan ishni ko'rsatadi. Ikki nuqta (`origin/main..HEAD`) esa boshqa narsa beradi va base branchda sen ketganingdan keyin paydo bo'lgan o'zgarishlar ham diffda teskari ishorada ko'rinadi, natijada reviewer ko'rmaydigan qatorlarni o'qib chiqasan.

```bash
# O'zini review qilish uchun: PR diff ini xuddi reviewer ko'rganidek ko'rish.
# Uch nuqta: umumiy ajdoddan HEAD gacha, ya'ni faqat shu branchning ishi.
git diff origin/main...HEAD

# Qoldirilgan tafsilotlarni qidirish
git diff origin/main...HEAD | grep -nE '^\+.*(System\.out|printStackTrace|TODO|FIXME|\.only\()'
```

## 41.7 Pair va mob programming mexanikasi

Juftlikda ishlash review ning real vaqtdagi shakli va u ba'zi vazifalarda ancha samarali: murakkab domen mantiqi, yangi odamni o'qitish, incident tahlili.

| Shakl | Qanday | Qachon |
|---|---|---|
| Driver/navigator | biri yozadi, biri o'ylaydi; belgilangan oraliqda almashadi (jamoa kelishuvi, odatda chorak soat atrofida) | murakkab mantiq |
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

## 41.9 Shaxsiy yozuvlar: kod xaritasi, buyruq ro'yxati va takrorlanadigan izoh

41.2 va 41.3 dagi o'qish mehnati yozib olinmasa, keyingi safar qaytadan takrorlanadi. Orosz uch xil yozuvni tavsiya qiladi va uchalasi ham arzon.

Birinchisi kodni o'qiyotganda chiqadigan yozuv: nomuvofiqliklar va tushunish qiyin bo'lgan joylar. Bu yozuvlar shaxsiy hujjatda yoki IDE kengaytmasi orqali faqat lokal faylda saqlanishi mumkin, ya'ni repoga tushmaydi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 9-bob, 128-bet). Ikkinchisi kod xaritasi: sinf va modullarni hamda ularning bog'lanishini qo'lda yoki chizma asbobi bilan chizib, qaysi qism nima qilishini yozib qo'yish. Orosz bu xaritani jamoadoshlarga ko'rsatishni alohida maslahat beradi: u suhbatni boshlab beradi va ko'pincha xaritani tuzgan odamgina emas, boshqalar ham yangi narsa bilib qoladi (shu yerda, 10-bob, 139-bet). Uchinchisi shaxsiy "productivity cheat sheet": ichki asboblar, havolalar, buyruqlar va so'rovlar ro'yxati. Orosz Uber da shunday hujjat yuritgan va u yillar davomida foydali bo'lgan; yangi jamoadagi birinchi oylarda foydasi eng katta (shu yerda, 10-bob, 138-bet).

To'rtinchi yozuv review dan keladi: olingan izohlarni qayd qilib borish va takrorlanayotganini ko'rish. Agar reviewerlar muntazam ravishda bir xil narsani aytsa (masalan, metod juda ko'p ish qiladi yoki test unutilgan), tuzatiladigan narsa bitta qator emas, odat (shu yerda, 8-bob, 112-bet). Shu ro'yxat 41.6 dagi o'zini review qilish ro'yxatining shaxsiy qismiga aylanadi.

```markdown
# payment-service: shaxsiy yozuv (repoga tushmaydi)

## Xarita
SettlementController -> SettlementService -> SettlementImporter -> ledger
Valyuta konvertatsiyasi: CurrencyConverter, kurs kunlik keshda.

## Tushunmadim
SettlementRow.validate() da ikkita valyuta tekshiruvi bor, biri o'lik?

## Buyruqlar
./mvnw -q -pl payment -am test -Dtest=SettlementImporterTest
psql -c "select status, count(*) from settlement group by 1"

## Takrorlangan review izohlari
- metodni bo'lish (3 marta) -> PR dan oldin 30 qatordan uzun metodni qidirish
- xato yo'li uchun test yo'q (2 marta) -> DoD ro'yxatiga qo'shildi
```

Yozuv shaxsiy bo'lgani uchun unga sir, token va ishlab chiqarish ma'lumoti yozilmaydi: shaxsiy fayl `.gitignore` bilan himoyalanmaydi (39.8).

## 41.10 Amalda qo'llash

- [ ] Har bir vazifani boshlashdan oldin 41.1 shablonini to'ldirish odatini joriy qiling.
- [ ] Mavjud kodga tegishdan oldin xatti-harakatni qayd etuvchi test yozishni standart qiling.
- [ ] 41.3 jadvalidagi texnikalardan kamida uchtasini keyingi ish davomida ongli ravishda sinab ko'ring.
- [ ] Feature flag lar ro'yxatini yuritib, har biriga o'chirish sanasi va egasini belgilang.
- [ ] 41.6 ro'yxatini PR shabloniga kiritib, o'zini review qilishni majburiy qadam qiling.
- [ ] `git diff` bo'yicha qoldirilgan tafsilot (debug log, `TODO`) skriptini pre-push hook ga qo'shing.
- [ ] Juftlikda ishlash uchun mos vazifa turlarini jamoa bilan kelishib oling.
- [ ] Ishni tugatish ta'rifini yozib, jamoa kelishuviga va PR shabloniga kiriting.

## Manbalar

- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr,
  Pragmatic Engineer, 2023, 8-bob (112), 9-bob (128) va 10-bob
  (138-139) - 41.9 dagi kod o'qish yozuvlari va ularning lokal qolishi, kod
  xaritasini jamoaga ko'rsatish, shaxsiy "productivity cheat sheet",
  hamda takrorlanadigan review izohlarini qayd qilib borish.
- Robert C. Martin, *Clean Code*, 17-bob, evristika G21
  ("Understand the Algorithm") - 41.2 dagi tushunish talabi va
  testning yashil bo'lishi tushunish dalili emasligi.
- Git hujjati, `diff-options`
  ([https://github.com/git/git/blob/v2.56.0/Documentation/diff-options.adoc](https://github.com/git/git/blob/v2.56.0/Documentation/diff-options.adoc),
  tag `v2.56.0`, GPL-2.0) - 41.3 dagi `-S` ning uchrash sonini
  tekshirishi, `-G` ning patch matniga qarashi va ikkisining farqini
  ko'rsatadigan misol.
- Git hujjati, `git-diff`
  ([https://github.com/git/git/blob/v2.56.0/Documentation/git-diff.adoc](https://github.com/git/git/blob/v2.56.0/Documentation/git-diff.adoc),
  tag `v2.56.0`, GPL-2.0) - 41.6 dagi uch nuqtali diff ning
  `git diff $(git merge-base A B) B` ga tengligi.

---

[&larr; 40. Versiya nazorati gigiyenasi](40-versiya-nazorati-gigiyenasi.md) · [Mundarija](README.md) · [42. Statik tahlil va avtomatik qoidalar &rarr;](42-statik-tahlil-va-avtomatik-qoidalar.md)
