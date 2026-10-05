<!-- doc: code-review | chapter: 2 | part: I. Review ning mohiyati va iqtisodi -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 2. Review iqtisodi: xato narxi, navbat va PR hajmi (The Economics of Review)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [2.1 Xato narxi bosqich bo'yicha o'sadi](#21-xato-narxi-bosqich-boyicha-osadi)
- [2.2 PR hajmi va topish darajasi](#22-pr-hajmi-va-topish-darajasi)
- [2.3 Navbat nazariyasi: kutish vaqti review ning asosiy narxi](#23-navbat-nazariyasi-kutish-vaqti-review-ning-asosiy-narxi)
- [2.4 Reviewer soni: ikkinchidan keyin qaytim tushadi](#24-reviewer-soni-ikkinchidan-keyin-qaytim-tushadi)
- [2.5 Review byudjeti: haftada qancha vaqt](#25-review-byudjeti-haftada-qancha-vaqt)
- [2.6 Review ni bo'lish: stacked PR texnikasi](#26-review-ni-bolish-stacked-pr-texnikasi)
- [2.7 Rework: review ning yashirin narxi](#27-rework-review-ning-yashirin-narxi)
- [2.8 Review ning qaytimi qachon manfiy bo'ladi](#28-review-ning-qaytimi-qachon-manfiy-boladi)
- [2.9 Byudjetni xavf bo'yicha taqsimlash](#29-byudjetni-xavf-boyicha-taqsimlash)
- [2.10 Raqamlarni o'z loyihangizda o'lchash](#210-raqamlarni-oz-loyihangizda-olchash)
- [2.11 Amalda qo'llash](#211-amalda-qollash)

</details>


Review vaqt yeydi, va shu vaqt eng qimmat odamlarning vaqti. Shu sababli review ni iqtisodiy hodisa sifatida ko'rish kerak: nimaga qancha sarflanadi va qancha qaytadi. Bu bobda to'rtta raqam hisoblanadi: xatoning bosqichga qarab narxi, review ning optimal hajmi, navbat vaqti va reviewer sonining qaytimi.

## 2.1 Xato narxi bosqich bo'yicha o'sadi

Xatoni topish narxi u qancha uzoq yashagan bo'lsa, shuncha yuqori. Sabablari mexanik: kontekst yo'qoladi, xato boshqa kodga tarqaladi, ma'lumot buziladi, va tuzatish uchun relizdan tashqari yo'l kerak bo'ladi.

| Qayerda topilgan | Tuzatish ishi | Qo'shimcha narx | Nisbiy narx |
| --- | --- | --- | --- |
| IDE da yozilayotganda | Bir daqiqa | Yo'q | 1 |
| Lokal testda | Bir necha daqiqa | Yo'q | 2-3 |
| Review da | 15-60 daqiqa | Ikkinchi odam vaqti, kontekstga qaytish | 5-10 |
| CI da | 10-30 daqiqa | Pipeline vaqti, navbat | 5-10 |
| Staging da | Yarim kun | Qayta deploy, test ma'lumoti | 15-30 |
| Prodda, ta'sirsiz | Bir kun | Hotfix, reliz tartibi | 30-60 |
| Prodda, ma'lumot buzilgan | Bir hafta va ko'proq | Incident, backfill, ishonch yo'qolishi | 100 va yuqori |

Oxirgi qatorga alohida e'tibor kerak. Ma'lumot buzilishi boshqa barcha xato turidan farq qiladi: kodni qaytarsangiz, xato yo'qoladi, lekin buzilgan ma'lumot joyida qoladi. Shu sababli review da ma'lumotga yozadigan kod boshqa kodga nisbatan ko'proq vaqtga arziydi. Bu hujjatning V bo'limi aynan shu sababli eng batafsil.

## 2.2 PR hajmi va topish darajasi

Reviewer ning diqqati chiziqli emas. Kichik diffda har satr ko'riladi, katta diffda ko'z yuguradi. Kuzatuvlar bir o'tirishda taxminan 200-400 o'zgargan satr atrofida samaradorlik yuqori bo'lishini, undan keyin esa topish darajasi keskin tushishini ko'rsatadi. Sababi fiziologik: diqqat 60-90 daqiqadan keyin pasayadi.

| PR hajmi (o'zgargan satr) | Reviewer xulqi | Topish darajasi | Amaliy xulosa |
| --- | --- | --- | --- |
| 1-50 | Har satrni o'qiydi, kontekstni tekshiradi | Yuqori | Ideal hajm |
| 50-200 | O'qiydi, ba'zi joylarni tezlashtiradi | Yuqori | Normal hajm |
| 200-400 | Muhim joylarni tanlab o'qiydi | O'rtacha | Chegara |
| 400-1000 | Diagonal o'qiydi, dizaynga qaraydi | Past | Bo'lish kerak |
| 1000+ | "LGTM" | Nolga yaqin | Review emas, marosim |

Shu jadvaldan bitta qattiq qoida chiqadi: 400 satrdan katta PR ni review qilish o'zini aldash. Agar bo'lish imkoni bo'lmasa (masalan, katta migratsiya yoki framework yangilanishi), review usuli o'zgaradi: satrlarni o'qish o'rniga xavf nuqtalari ro'yxati bo'yicha yuriladi va qolgani avtomatik tekshiruvga ishonib topshiriladi. Bu holat ham izohda ochiq yozilishi kerak.

```bash
# PR hajmini o'lchash va generated/test fayllarni ajratish.
# Reviewer uchun haqiqiy yuk - qo'lda yozilgan mantiq satrlari.
BASE=origin/main
git diff --numstat $BASE...HEAD | awk '
  $3 ~ /\/generated\/|\.lock$|package-lock|\.svg$/ { gen += $1 + $2; next }
  $3 ~ /[Tt]est/                                   { tst += $1 + $2; next }
  $3 ~ /\.(md|txt|properties|ya?ml)$/              { cfg += $1 + $2; next }
                                                   { src += $1 + $2 }
  END {
    printf "mantiq:    %5d satr\n", src
    printf "test:      %5d satr\n", tst
    printf "konfig:    %5d satr\n", cfg
    printf "generated: %5d satr (tekshirilmaydi)\n", gen
    if (src > 400) print "OGOHLANTIRISH: mantiq qismi 400 satrdan katta, PR ni ajratish kerak"
  }'

# Fayl bo'yicha eng katta o'zgarishlar: review ni shulardan boshlash kerak.
git diff --numstat $BASE...HEAD | sort -rn | head -10
```

## 2.3 Navbat nazariyasi: kutish vaqti review ning asosiy narxi

Review ning haqiqiy narxi reviewer sarflagan 30 daqiqa emas. Asosiy narx - PR ning navbatda turgan vaqti. Kutayotgan PR muallifni boshqa ishga o'tishga majbur qiladi, keyin kontekstni qaytadan tiklashga majbur qiladi, va ayni paytda base branch dan uzoqlashib boradi.

Little qonuni bu yerda ham ishlaydi: tizimda kutayotgan ishlar soni = kelish tezligi x o'rtacha o'tish vaqti. Agar jamoa kuniga 10 PR ochsa va o'rtacha o'tish vaqti 2 kun bo'lsa, har doim taxminan 20 ta ochiq PR turadi. Yigirma ochiq PR esa konfliktlar, eskirgan branchlar va qayta ishlash degani.

| Birinchi javobni kutish | Muallif xulqi | Tizim oqibati |
| --- | --- | --- |
| 1 soatdan kam | Kontekstda qoladi, darhol tuzatadi | Eng tez oqim, eng kam rework |
| 4 soatgacha | O'sha kuni tugatadi | Normal |
| 1 kun | Boshqa ishga o'tadi, kontekstni yo'qotadi | Rework o'sadi |
| 2-3 kun | Branch eskiradi, konflikt chiqadi | Merge xatolari, qayta test |
| 1 hafta | PR tashlab ketiladi yoki majburan merge qilinadi | Review foydasi nolga tushadi |

Amaliy xulosa: kutish vaqtini qisqartirish review chuqurligini oshirishdan muhimroq. Ikki soatda yuzaki o'qilgan va darhol javob berilgan PR, ikki kundan keyin chuqur o'qilgan PR dan ko'proq foyda beradi, chunki muallif hali kontekstda.

## 2.4 Reviewer soni: ikkinchidan keyin qaytim tushadi

Kuzatuvlar birinchi reviewer xatolarning katta qismini topishini, ikkinchisi sezilarli qo'shimcha berishini, uchinchisidan keyin esa qaytim tez pasayishini ko'rsatadi. Sababi oddiy: ikki odam bir xil joylarga qaraydi.

Shu sababli samarali siyosat sonni emas, rolni belgilaydi. Ikki reviewer kerak bo'lsa, ularga turli vazifa beriladi: biri domen va mantiqni ko'radi, ikkinchisi operatsion xavfni (migratsiya, konfiguratsiya, monitoring) ko'radi. Aks holda ikkinchi reviewer birinchisining ishini takrorlaydi va mas'uliyat tarqaydi.

| Reviewer soni | Qo'shimcha foyda | Qo'shimcha narx | Qachon o'rinli |
| --- | --- | --- | --- |
| 1 | Asosiy foyda | 1 x vaqt | Oddiy o'zgarish |
| 2 (turli rol bilan) | Sezilarli, agar rollar ajratilgan bo'lsa | 2 x vaqt + muvofiqlashtirish | Xavfli o'zgarish |
| 3 va ko'p | Kichik | Navbat uzayadi, mas'uliyat tarqaydi | Faqat o'rganish maqsadida |

## 2.5 Review byudjeti: haftada qancha vaqt

Review vaqti rejadan tashqari emas, reja ichida bo'lishi kerak. Amaliy raqam: jamoa a'zosi haftasining taxminan 10-15 foizi review ga ketadi. Besh kunlik haftada bu kuniga taxminan 45-60 daqiqa. Agar bu vaqt rejaga kiritilmasa, review "bo'sh vaqtda" qiladigan ish bo'lib qoladi va bo'sh vaqt hech qachon kelmaydi.

Byudjetni taqsimlashning foydali usuli: kunda ikki oyna. Masalan ertalab ishni boshlashda 30 daqiqa va tushdan keyin 30 daqiqa. Bu uzluksiz kodlash vaqtini saqlaydi va ayni paytda PR ning kutish vaqtini yarim kundan oshirmaydi. Har xabarga darhol javob berish esa ikkala ishni ham buzadi.

## 2.6 Review ni bo'lish: stacked PR texnikasi

Katta o'zgarishni mayda PR larga bo'lishning eng ishlaydigan usuli - bir-birining ustiga qo'yilgan branchlar. Har bir PR o'zidan oldingisiga nisbatan diff ko'rsatadi va alohida review qilinadi.

```bash
# Katta funksiyani uchta review qilinadigan bo'lakka bo'lish.
# Qoida: har bo'lak o'zi mustaqil kompilyatsiya bo'lsin va testdan o'tsin.

git switch -c feat/payout-1-schema main
# 1-PR: faqat migratsiya va entity. Mantiq yo'q, xavf kichik.
#       Review fokusi: sxema, indeks, orqaga moslik.

git switch -c feat/payout-2-domain feat/payout-1-schema
# 2-PR: domen mantiqi va unit testlar. Baza tegmaydi.
#       Review fokusi: qoida, chegaraviy holat, invariant.

git switch -c feat/payout-3-api feat/payout-2-domain
# 3-PR: controller, DTO, validation, xato javobi.
#       Review fokusi: tashqi shakl, moslik, idempotentlik.

# Birinchi PR merge bo'lgandan keyin qolganlarini yangilash:
git switch feat/payout-2-domain && git rebase --onto main feat/payout-1-schema
# Yoki merge bilan (jamoa konvensiyasiga qarab):
#   git switch feat/payout-2-domain && git merge main
```

Bo'lishning to'g'ri chizig'i qatlam bo'yicha emas, xavf bo'yicha o'tadi. Sxema o'zgarishi alohida, chunki uni qaytarish qiyin. Domen mantiqi alohida, chunki u eng ko'p o'qishni talab qiladi. API shakli alohida, chunki u tashqi mijozga ta'sir qiladi.

## 2.7 Rework: review ning yashirin narxi

Review dan keyin qayta yozilgan kod - alohida xarajat moddasi. Agar PR uch marta tuzatish davrasidan o'tsa, bu olti kontekst almashinuvi degani. Rework ko'p bo'lsa, sabab ko'pincha review da emas: talab noaniq bo'lgan yoki dizayn muhokama qilinmagan.

Amaliy mezon: o'rtacha PR bir yoki ikki tuzatish davrasida yopilishi kerak. Uchdan ko'p davra tizimli muammo belgisi. Shu holatda yechim review ni yumshatish emas, PR dan oldingi bosqichni tuzatish: talabni aniqlashtirish yoki dizayn eskizi.

## 2.8 Review ning qaytimi qachon manfiy bo'ladi

Review foydasi narxidan kam bo'lgan holatlar bor va ularni tan olish kerak. Masalan: bir qatorli konfiguratsiya o'zgarishi, versiya raqamini ko'tarish, matn tuzatish, test ma'lumotini qo'shish. Bunday o'zgarishlar uchun yengil yo'l qo'yish kerak: avtomatik approve qoidasi yoki post-commit review.

```yaml
# .github/workflows/auto-approve-trivial.yml
# Faqat haqiqatan xavfsiz yo'llar uchun. Ro'yxat qisqa bo'lishi kerak.
name: trivial-fast-path
on: pull_request_target
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Faqat xavfsiz fayllar o'zgarganini tekshirish
        run: |
          CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          echo "$CHANGED"
          # Xavfsiz ro'yxatdan tashqari biror narsa bo'lsa - oddiy review.
          UNSAFE=$(echo "$CHANGED" | grep -vE '^(docs/|README\.md|CHANGELOG\.md)' || true)
          if [ -n "$UNSAFE" ]; then
            echo "Oddiy review kerak: $UNSAFE"
            exit 1
          fi
```

Diqqat: bu ro'yxatga `src/main/resources/application*.yml` yoki migratsiya papkasi hech qachon kirmaydi. Konfiguratsiya o'zgarishi diffda kichik, oqibatda esa eng katta incidentlarni keltirib chiqaradigan sinf.

## 2.9 Byudjetni xavf bo'yicha taqsimlash

Review vaqtini barcha PR larga teng taqsimlash - resursni isrof qilish. To'g'ri model: xavf bo'yicha tabaqalash. Kichik xavfli PR bir reviewer va yuzaki o'tish bilan ketadi, yuqori xavfli PR ikki reviewer, checklist va lokal sinovni talab qiladi.

| Xavf darajasi | Belgisi | Review rejimi |
| --- | --- | --- |
| Past | Faqat test, docs, log matni, ichki refactoring | 1 reviewer, yuzaki |
| O'rta | Yangi endpoint, biznes qoidasi o'zgarishi | 1 reviewer, satr-satr |
| Yuqori | Migratsiya, pul hisobi, autentifikatsiya, tashqi API shakli | 2 reviewer, checklist, lokal sinov |
| Juda yuqori | Ma'lumotni o'chiradigan yoki ko'chiradigan skript | 2 reviewer + dry-run natijasi + qaytish rejasi |

Shu jadvalni repoda `CODEOWNERS` va PR shabloni bilan birga saqlash kerak, shunda tabaqalash og'zaki kelishuvdan jarayonga aylanadi. CODEOWNERS mexanikasi [40-bobda](40-review-jarayonini-qurish.md).

## 2.10 Raqamlarni o'z loyihangizda o'lchash

Yuqoridagi raqamlar yo'nalish beradi, lekin qaror sizning raqamlaringizdan chiqadi. Minimal to'plam: PR ning birinchi javobni kutish vaqti (median va p90), o'zgargan satr soni taqsimoti, tuzatish davralari soni, va review dan keyin prodda topilgan xatolar soni.

```bash
# Repo tarixidan review iqtisodini o'lchash (GitHub CLI bilan).
# 1) Ochilish va birinchi review orasidagi vaqt (oxirgi 100 PR).
gh pr list --state merged --limit 100 \
  --json number,createdAt,reviews \
  --jq '.[] | select(.reviews|length>0)
        | {pr:.number,
           kutish_soat: (((.reviews[0].submittedAt|fromdate) - (.createdAt|fromdate))/3600|floor)}' \
  | head -20

# 2) PR hajmi taqsimoti: mediana va eng kattalari.
gh pr list --state merged --limit 100 --json number,additions,deletions \
  --jq 'map(.additions + .deletions) | sort
        | {median: .[length/2|floor], p90: .[length*0.9|floor], max: .[-1]}'

# 3) Tuzatish davralari: review dan keyin kelgan commitlar soni.
gh pr list --state merged --limit 50 --json number,commits,reviews \
  --jq '.[] | {pr:.number, commitlar:(.commits|length), reviewlar:(.reviews|length)}'
```

Bu raqamlar bir oyda bir marta o'lchansa yetadi. Maqsad - tendentsiyani ko'rish, dashboard qurish emas. Metrikalarning to'liq to'plami va ularning tuzogi [42-bobda](42-review-metrikalari.md).

## 2.11 Amalda qo'llash

- [ ] Oxirgi 100 merge qilingan PR uchun birinchi javobni kutish vaqtining medianasi va p90 ini hisoblang.
- [ ] PR hajmi taqsimotini chiqarib, 400 satrdan katta PR ulushini aniqlang va shu PR larda topilgan izohlar sonini taqqoslang.
- [ ] CI ga PR hajmi haqida ogohlantirish qo'shing: mantiq satrlari 400 dan oshsa, izoh yozilsin (bloklamasin).
- [ ] Jamoada kunlik ikki review oynasini kelishib oling va uni kalendarga qo'ying.
- [ ] Xavf tabaqalash jadvalini `REVIEW.md` ga qo'shing va yuqori xavfli yo'llar uchun ikki reviewer talabini sozlang.
- [ ] Stacked PR usulini bitta katta funksiyada sinab ko'ring: sxema, domen va API ni uch PR ga bo'ling.
- [ ] Uchdan ko'p tuzatish davrasidan o'tgan oxirgi uch PR ni ko'rib, sababi talabda yoki dizaynda ekanini aniqlang.
- [ ] Trivial yo'llar ro'yxatini (docs, changelog) belgilab, ularga yengil yo'l bering va bu ro'yxatga konfiguratsiya fayllari kirmasligini tasdiqlang.

---

[&larr; 1. Review nima uchun bor va nimani haqiqatda beradi](01-review-nima-uchun-bor-va-nimani-haqiqatda.md) · [Mundarija](README.md) · [3. Reviewer ning tahlil apparati: niyat, invariant, xavf yuzasi &rarr;](03-reviewer-ning-tahlil-apparati-niyat.md)
