<!-- doc: code-review | chapter: 41 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 41. Review madaniyati, til va kelishmovchilik (Culture, Language, Disagreement)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [41.1 Izoh tili: kodga qarash, odamga emas](#411-izoh-tili-kodga-qarash-odamga-emas)
- [41.2 Savol shaklida izoh](#412-savol-shaklida-izoh)
- [41.3 Izoh darajasini ajratish](#413-izoh-darajasini-ajratish)
- [41.4 Junior va senior bilan review](#414-junior-va-senior-bilan-review)
- [41.5 Kelishmovchilikni hal qilish](#415-kelishmovchilikni-hal-qilish)
- [41.6 Review izohining narxi](#416-review-izohining-narxi)
- [41.7 Masofaviy va asinxron review](#417-masofaviy-va-asinxron-review)
- [41.8 Review ni o'rgatish](#418-review-ni-orgatish)
- [41.9 Review madaniyatining buzilish belgilari](#419-review-madaniyatining-buzilish-belgilari)
- [41.10 Amalda qo'llash](#4110-amalda-qollash)

</details>


Texnik jihatdan to'g'ri review ham zarar keltirishi mumkin, agar u odamni himoyaga o'tishga majbur qilsa. Natija: muallif izohlarni rad etadi, keyingi PR ni kichikroq va kech yuboradi, va review dan qo'rqadi. Bu bob review ni muloqot sifatida ko'radi - lekin yumshoqlik haqida emas, aniqlik haqida.

## 41.1 Izoh tili: kodga qarash, odamga emas

| Yomon shakl | Yaxshi shakl |
| --- | --- |
| "Sen nega bunday qilding?" | "Bu yerda X bo'lsa nima bo'ladi?" |
| "Bu noto'g'ri" | "Bu holatda Y oqibat chiqadi" |
| "Hamma biladi ki..." | "Bizning konvensiyamiz..." (havola bilan) |
| "Yana shu xato" | "Shu naqsh takrorlanyapti - qoidaga aylantirsakmi?" |
| "Men shunday yozmagan bo'lardim" | (sabab bo'lmasa - izoh yozmaslik) |
| "Buni tushunmadim" | "Bu metod nima qilishini nom bilan ko'rsatsak bo'ladimi?" |
| "Bu juda sodda" | "Bu yerda Z holati hisobga olinmagan" |

Asosiy mexanik qoida: izoh kod haqida bo'lsin, muallif haqida emas. "Sen" so'zi izohda deyarli har doim ortiqcha.

## 41.2 Savol shaklida izoh

Savol ikki narsani beradi: muallifga tushuntirish imkonini beradi (balki reviewer kontekstni bilmaydi) va aniqlashtiradi.

```text
# Buyruq: muallif rozi bo'lmasa, bahs boshlanadi.
"Bu yerda cache qo'shish kerak."

# Savol: kontekstni ochadi.
"Bu so'rov qanchalik tez-tez chaqiriladi? Agar har sahifa yuklanishida
bo'lsa, kesh qo'shish arziydi - lekin ma'lumot qanchalik tez eskiradi
degan savol bor. Siz qanday o'ylaysiz?"
```

Lekin savol shakli bilan haddan oshmaslik kerak. Agar aniq xato bo'lsa, savol shakli chalkashtiradi:

```text
# Yomon: aniq blocker savol shaklida - muallif uni ixtiyoriy deb o'ylaydi.
"Bu yerda unique constraint bo'lishi kerak emasmi?"

# Yaxshi: aniq va sababi bilan.
blocker: idempotentlik kaliti bo'yicha unique indeks yo'q. Ikki parallel
so'rov ikki to'lov yaratadi (15.2 naqshi). Migratsiyaga qo'shish kerak.
```

## 41.3 Izoh darajasini ajratish

4.9 da prefikslar berilgan. Ularning asosiy foydasi psixologik: muallif qaysi izohga qancha vaqt sarflashini biladi va `nit` larni rad etishi normal bo'ladi.

```text
blocker:  tuzatilmasa merge bo'lmaydi (xato, xavfsizlik, ma'lumot)
suggest:  yaxshilanish, muallif qaroriga qoldiriladi
question: javob kerak, tuzatish shart emas
nit:      did, majburiy emas (10 foizdan ko'p bo'lmasin)
praise:   to'g'ri qilingan qiyin joy
```

Qo'shimcha qoida: `blocker` lar soni cheklangan bo'lishi kerak. Agar PR da 15 blocker bo'lsa, bu alohida muammo - PR dizayn darajasida noto'g'ri yoki muallif kontekstni bilmaydi. Shu holatda 15 izoh yozish o'rniga suhbatlashish kerak.

## 41.4 Junior va senior bilan review

| Muallif | Diqqat | Tuzoq |
| --- | --- | --- |
| Junior | Nega shunday - o'rganish imkoniyati | Haddan ortiq izoh, ruhiy bosim |
| O'rta daraja | Mustaqil qaror va chegaralar | Yetarli diqqat berilmasligi |
| Senior | Dizayn qarori va alternativalar | Yuzaki review (obro'ga ishonish) |
| Boshqa jamoa | Kontekst va konvensiyalar | Yashirin bilim talab qilish |
| Yangi kelgan | Konvensiyalarni ko'rsatish | "Bizda shunday" tushuntirishsiz |

```text
# Junior PR ida: 20 izoh yozish o'rniga eng muhim 5 tasini tanlash.
# Qolganlari keyingi PR larda ko'riladi yoki juftlikda ishlash orqali.

# Aniq va o'rgatuvchi izoh shakli:
blocker: bu yerda tranzaksiya ichida SMS yuborilyapti.

Nega muhim: DB ulanishi SMS provayderining javobini kutib turadi.
Bizda pool 20 ta ulanish - ya'ni 20 parallel buyurtma butun ilovani
to'xtatadi. Bundan tashqari SMS o'tib, keyin commit yiqilsa, mijoz
tasdiq oladi, lekin buyurtma yo'q bo'ladi.

Yechim: SMS ni outbox ga yozish (shunga o'xshash misol
OrderCancellationService da bor, 45-satr).

Bu naqsh haqida: REVIEW.md -> "tranzaksiya ichida tashqi chaqiruv".
```

## 41.5 Kelishmovchilikni hal qilish

Kelishmovchilik normal va foydali - muhimi uning oxiri bo'lishi. Jamoada tartib yozilmasa, bahs PR da uch kun davom etadi.

```markdown
<!-- REVIEW.md ichida: kelishmovchilik tartibi -->
## Kelishmovchilik

1. **Dalil almashish.** Ikki tomon o'z pozitsiyasini oqibat tilida yozadi
   (did emas, raqam yoki ssenariy).
2. **Ikki davra.** Izoh almashinuvi ikki davradan oshsa, PR da yozishni
   to'xtatib, 15 daqiqalik suhbat o'tkaziladi. Yozma bahs tezda qimmatlashadi.
3. **Qaytarilish narxi.** Qaror arzon qaytarilsa (ichki kod) - muallif
   qaroriga qoldiriladi. Qimmat qaytarilsa (API, sxema, ma'lumot) -
   uchinchi odam yoki tech lead qaror qiladi.
4. **Yozib qoldirish.** Qaror ADR yoki PR izohida qoladi, shunda keyin
   bahs takrorlanmaydi.
5. **"Rozi emasman, lekin bajaraman".** Qaror qabul qilingach, ikki tomon
   uni qo'llab-quvvatlaydi. Pozitsiya ADR da qayd qilinadi.
```

Alohida holat: reviewer va muallif tajriba darajasi juda farq qilsa, kelishmovchilik teng bo'lmaydi. Bunday holatda qoida foydali: "junior reviewer senior muallifga blocker qo'yishi normal, va senior javob yozishi majburiy".

## 41.6 Review izohining narxi

Har bir izoh muallif vaqtini oladi: o'qish, tushunish, tuzatish yoki javob yozish. Shu sababli izoh yozishdan oldin savol: bu izoh o'z narxini qoplaydimi.

| Izoh | Muallif vaqti | Foyda |
| --- | --- | --- |
| Aniq xato | 10-30 daqiqa | Prodda 10 barobar ko'p |
| Xavfsizlik | 30-60 daqiqa | Juda yuqori |
| Dizayn | Soatlar | Uzoq muddatli |
| Nomlash (noto'g'ri nom) | 2 daqiqa | Har o'qishda |
| Nomlash (did) | 2 daqiqa + bahs | Deyarli nol |
| Formatlash | 5 daqiqa | Nol (instrument ishi) |
| Shaxsiy uslub | Bahs | Manfiy |

Oxirgi uch qator review ning eng ko'p isrof qiladigan qismi. Ularni yo'q qilish uchun instrument va yozilgan konvensiya kerak, bahs emas.

## 41.7 Masofaviy va asinxron review

| Muammo | Yechim |
| --- | --- |
| Vaqt zonalari farqi | Yozma izoh to'liq va mustaqil bo'lsin |
| Ohangni noto'g'ri tushunish | Sabab va kontekstni yozish, emoji ortiqcha emas |
| Uzoq davralar | Blocker larni bir martada to'liq berish |
| Kontekst yo'qolishi | PR tavsifi va izohda havolalar |
| "Kim javob beradi" noaniqligi | CODEOWNERS va aniq murojaat |
| Tezkor savollar | 15 daqiqalik qo'ng'iroq, uch kunlik yozishma emas |

Asinxron review ning asosiy qoidasi: izoh o'zini tushuntirsin. Muallif boshqa vaqt zonasida uyg'onib, izohni o'qiganda qo'shimcha savol bermasdan ishlay olishi kerak. Bu "oqibat + alternativa + havola" shaklini majburiy qiladi.

## 41.8 Review ni o'rgatish

```markdown
<!-- Yangi jamoa a'zosi uchun review ga kirish rejasi -->
## Review ga qanday kirishamiz

### 1-hafta: kuzatish
Ikki PR ni tajribali reviewer bilan birga ko'rib chiqing (ekran ulashib).
Maqsad: nimaga qaraladi va qanday tartibda.

### 2-3-hafta: ikkinchi reviewer
PR larga ikkinchi reviewer sifatida qo'shiling. Izohlaringiz birinchi
reviewer bilan solishtiriladi - nima topildi, nima o'tkazib yuborildi.

### 4-hafta: mustaqil, past xavfli PR lar
`risk:low` va `risk:medium` PR larni mustaqil review qilasiz.

### Keyin: xavf darajasini oshirish
`risk:high` PR larda ikkinchi reviewer, keyin birinchi.

### Doimiy
- Har incidentdan keyin: "review nega ko'rmadi" savoliga javob.
- Har oyda bitta review ni birga tahlil qilish (nima yaxshi, nima yo'q).
```

## 41.9 Review madaniyatining buzilish belgilari

| Belgi | Nimani bildiradi |
| --- | --- |
| "LGTM" izohsiz, 2 daqiqada | Review marosimga aylangan |
| Bir xil odam hamma PR ni ko'radi | Bilim tarqalmaydi, nuqta bo'g'in |
| PR lar 3 kundan ko'p kutadi | Review byudjeti yo'q |
| Izohlarning yarmi `nit` | Instrument yo'q |
| Muallif izohlarga javob bermaydi | Jarayon majburiy emas |
| Bahslar PR dan tashqariga chiqadi | Kelishmovchilik tartibi yo'q |
| Katta PR lar normal holat | Bo'lish madaniyati yo'q |
| Junior lar PR yuborishdan qo'rqadi | Izoh tili bilan muammo |
| Review dan keyin ham prodda ko'p xato | Checklist incidentlardan o'smaydi |
| Reviewer "men faqat ko'rib qo'ydim" deydi | Mas'uliyat tarqamagan |

## 41.10 Amalda qo'llash

- [ ] Izoh prefikslari va ularning ma'nosini `REVIEW.md` ga yozib, jamoada kelishib oling.
- [ ] Kelishmovchilik tartibini (ikki davra, keyin suhbat) yozib, uni amalda qo'llashni boshlang.
- [ ] Oxirgi 50 izohni sanab, `nit` ulushini aniqlang; 20 foizdan ko'p bo'lsa, instrumentlarga ko'chiring.
- [ ] Izoh shabloniga "oqibat + alternativa + havola" talabini kiriting.
- [ ] Yangi a'zolar uchun review ga kirish rejasini yozib, uni onboarding ga qo'shing.
- [ ] Har oyda bitta review ni jamoada birga tahlil qilishni odat qiling.
- [ ] Madaniyat buzilish belgilarini chorakda bir marta tekshirib, topilganlarini muhokama qiling.
- [ ] `praise` izohini ongli ishlatishni boshlang: to'g'ri qilingan qiyin joyni ko'rsatish.

---

[&larr; 40. Review jarayonini qurish](40-review-jarayonini-qurish.md) · [Mundarija](README.md) · [42. Review metrikalari &rarr;](42-review-metrikalari.md)
