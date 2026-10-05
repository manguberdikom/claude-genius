<!-- doc: clean-code | chapter: 40 | part: XI. Kod bazasi va jarayon gigiyenasi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 40. Versiya nazorati gigiyenasi (Version Control Hygiene)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [40.1 Atomik commit: bitta mantiqiy o'zgarish](#401-atomik-commit-bitta-mantiqiy-ozgarish)
- [40.2 Commit xabari tuzilishi](#402-commit-xabari-tuzilishi)
- [40.3 Conventional commits va avtomatik changelog](#403-conventional-commits-va-avtomatik-changelog)
- [40.4 Branch hayoti va uzoq yashagan branch narxi](#404-branch-hayoti-va-uzoq-yashagan-branch-narxi)
- [40.5 Rebase, merge va tarixni o'qiladigan ushlash](#405-rebase-merge-va-tarixni-oqiladigan-ushlash)
- [40.6 PR hajmi va bo'lish texnikasi](#406-pr-hajmi-va-bolish-texnikasi)
- [40.7 `git blame` ni foydali ushlash](#407-git-blame-ni-foydali-ushlash)
- [40.8 Tarixdan sirni o'chirish va uning chegarasi](#408-tarixdan-sirni-ochirish-va-uning-chegarasi)
- [40.9 Amalda qo'llash](#409-amalda-qollash)

</details>


Git tarixi kod bazasining hujjati: u "nega shunday qilingan" savoliga javob beradi va incident vaqtida eng tez diagnostika vositasi bo'ladi. Iflos tarix esa foydasiz. Review hajmi va navbat vaqti [arxitektor hujjatidagi](../architect/README.md) review hajmi bo'limida; bu bobda commit va branch darajasidagi qoidalar.

## 40.1 Atomik commit: bitta mantiqiy o'zgarish

Bitta commit bitta mantiqiy o'zgarishni o'z ichiga olishi kerak: u mustaqil ravishda tushunarli, mustaqil ravishda qaytariladigan va mustaqil ravishda ishlaydigan bo'lsin. Shu uch shart `git bisect` va `git revert` ni ishlatadigan qiladi.

| Commit mazmuni | To'g'rimi |
|---|---|
| Bitta xususiyat qismi + uning testi | ha |
| Refaktoring (xatti-harakat o'zgarmagan) | ha |
| Formatlash | ha, alohida (13.6) |
| Nomni o'zgartirish | ha, alohida (3.15) |
| Xususiyat + formatlash + refaktoring | yo'q |
| Ishlamaydigan yarim ish | yo'q |
| "Turli tuzatishlar" | yo'q |
| Bog'liqlik yangilash + kod moslashi | ha (ajralmas) |

```bash
# Ishni commitlarga ajratish: faqat kerakli qismlarni staging ga
git add -p                    # bo'laklab qo'shish
git commit -m "refactor: ..."
git add -p
git commit -m "feat: ..."
```

## 40.2 Commit xabari tuzilishi

Commit xabari ikki qismdan iborat: sarlavha (nima qilindi) va tana (nega qilindi). Tana eng qimmatli qism, chunki "nima" ni diff ham ko'rsatadi, "nega" ni esa faqat muallif biladi.

```
feat: hisob-kitob faylida valyuta tekshiruvini qo'shish

Bank fayli ba'zan USD yozuvlarini UZS hisobiga qo'shib yuboradi
(incident INC-2291). Valyuta mos kelmasa, qator rad etiladi va
audit log'ga yoziladi; butun fayl to'xtamaydi, chunki qolgan
yozuvlar to'g'ri.

Muqobil variant - butun faylni rad etish - rad etildi: bir noto'g'ri
qator kunlik hisob-kitobni to'xtatib qo'yadi.

Refs: SHOP-4821
```

Sarlavha qoidalari: 50-72 belgigacha, buyruq shaklida ("qo'shish", "tuzatish" - "qo'shdim" emas), nuqta bilan tugamaydi, va prefiks bilan boshlanadi (40.3).

## 40.3 Conventional commits va avtomatik changelog

Commit sarlavhasiga standart prefiks qo'yish tarixni mashina o'qiydigan qiladi: changelog avtomatik generatsiya qilinadi va semantik versiya avtomatik hisoblanadi.

| Prefiks | Ma'nosi | Versiyaga ta'siri |
|---|---|---|
| `feat:` | yangi xususiyat | minor |
| `fix:` | xato tuzatish | patch |
| `refactor:` | tuzilish o'zgarishi | yo'q |
| `perf:` | ishlash yaxshilanishi | patch |
| `test:` | faqat testlar | yo'q |
| `docs:` | faqat hujjat | yo'q |
| `build:` | build va bog'liqliklar | yo'q |
| `ci:` | pipeline | yo'q |
| `chore:` | qolgan ish | yo'q |
| `feat!:` yoki `BREAKING CHANGE:` | moslikni buzadi | major |

## 40.4 Branch hayoti va uzoq yashagan branch narxi

Branch qancha uzoq yashasa, uni merge qilish shunchalik qimmat bo'ladi: konfliktlar yig'iladi, review hajmi oshadi, va asosiy branch dan uzoqlashish regressiya xavfini oshiradi.

Amaliy maqsad: branch bir-ikki kundan oshmasin. Buning uchun ish kichik bo'lishi kerak va bu 38.5 dagi branch by abstraction va feature flag (41.5) bilan ta'minlanadi.

| Branch yoshi | Oqibati |
|---|---|
| < 1 kun | konflikt deyarli yo'q |
| 1-3 kun | boshqarilishi mumkin |
| 1 hafta | konfliktlar, katta review |
| 2+ hafta | merge alohida loyihaga aylanadi |

## 40.5 Rebase, merge va tarixni o'qiladigan ushlash

Rebase va merge o'rtasidagi tanlov jamoa kelishuviga bog'liq, lekin bitta qoida universal: **boshqa odam ishlatayotgan branch ning tarixini qayta yozmaslik**.

| Vaziyat | To'g'ri harakat |
|---|---|
| O'z lokal branch ingizni yangilash | `git rebase origin/main` |
| Boshqa odam ham ishlagan branch | `git merge origin/main` |
| O'z branch idagi WIP commitlarni tozalash | `git rebase -i` (push dan oldin) |
| Merge qilingan branch ni tozalash | o'chirish |
| Umumiy branch ga noto'g'ri commit tushdi | `git revert` (reset emas) |

Squash merge tarixni sodda qiladi (bitta xususiyat - bitta commit), lekin oraliq qadamlarni yo'qotadi. Katta refaktoring uchun oraliq commitlarni saqlash afzal.

## 40.6 PR hajmi va bo'lish texnikasi

Review sifati PR hajmi bilan teskari proporsional: 400 qatordan katta PR da topilgan xato soni keskin tushadi. Arxitektor hujjati 36.5 review navbati va hajmini ko'rib chiqadi; bu yerda bo'lish texnikalari.

| Texnika | Qanday |
|---|---|
| Refaktoringni ajratish | oldin tuzilish PR i, keyin xususiyat PR i (38.4) |
| Qatlam bo'yicha | migratsiya → repository → service → API |
| Feature flag ortida | yarim ish merge qilinadi, yoqilmaydi (41.5) |
| Abstraksiya orqali | branch by abstraction (38.5) |
| Faqat o'qish qismi | yangi endpoint avval o'qish uchun |
| Test birinchi | test PR i, keyin implementatsiya |

## 40.7 `git blame` ni foydali ushlash

`git blame` "bu qator nega shunday?" savoliga javob beradi, lekin faqat tarix toza bo'lsa. Uni buzadigan ikki narsa: katta formatlash commitlari (13.7 dagi `.git-blame-ignore-revs` bilan hal qilinadi) va aralash commitlar (40.1).

```bash
# Qator tarixini funksiya bo'yicha kuzatish (ko'chirishni ham ko'radi)
git log -L :priceFor:src/main/java/uz/shop/payment/Pricing.java

# Kod bo'lagi qachon kiritilganini topish
git log -S "REFUND_EXCEEDS_PAYMENT" --oneline

# Formatlash commitlarini e'tiborsiz qoldirib blame
git blame --ignore-revs-file .git-blame-ignore-revs Pricing.java
```

## 40.8 Tarixdan sirni o'chirish va uning chegarasi

Sir repoga tushsa, uni tarixdan o'chirish **yetarli emas**: u allaqachon klonlarda, CI log larida va GitHub keshida bo'lishi mumkin. Shu sababli tartib aniq va o'zgarmas.

1. **Birinchi** sirni rotatsiya qilish (eski kalitni bekor qilish). Bu eng muhim qadam.
2. Keyin tarixdan o'chirish (`git filter-repo` yoki BFG), agar repo yopiq va jamoa kichik bo'lsa.
3. Barcha klonlarni qaytadan olishni talab qilish.
4. Sir skanerlashni CI ga qo'shish (39.8), takrorlanmasligi uchun.

Tarixni qayta yozish umumiy branch da jamoaga qimmat tushadi, shuning uchun qadam 2 ni faqat qadam 1 bajarilgandan keyin ko'rib chiqish kerak.

## 40.9 Amalda qo'llash

- [ ] `git add -p` bilan ishni atomik commitlarga ajratish odatini joriy qiling.
- [ ] Commit xabari shablonini (`.gitmessage`) repoga qo'shib, `commit.template` sozlamasini README ga yozing.
- [ ] Conventional commits prefikslarini kelishib, CI da sarlavha formatini tekshiring.
- [ ] Branch yoshini o'lchab (ochiq PR lar bo'yicha), bir haftadan katta branchlarni bo'lish rejasini tuzing.
- [ ] Rebase va merge siyosatini yozib qo'ying, umumiy branch tarixini qayta yozishni taqiqlang.
- [ ] 400 qatordan katta PR lar uchun ogohlantirish qo'yib, 40.6 dagi bo'lish texnikalarini qo'llang.
- [ ] `.git-blame-ignore-revs` ni sozlab, blame ni toza ushlang (13.7).
- [ ] Sir tarixga tushgan holat uchun 40.8 dagi to'rt qadamli reja (runbook) yozib qo'ying.

---

[&larr; 39. Bir qadamli build va mahalliy qaytish halqasi](39-bir-qadamli-build-va-mahalliy-qaytish.md) · [Mundarija](README.md) · [41. O'zgarishni kiritish jarayoni: kichik qadamlar &rarr;](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md)
