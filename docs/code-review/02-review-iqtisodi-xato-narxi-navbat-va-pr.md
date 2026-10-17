<!-- doc: code-review | chapter: 2 | part: I. Review ning mohiyati va iqtisodi -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 2. Review iqtisodi: xato narxi, navbat va PR hajmi (The Economics of Review)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

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
- [2.11 Inspeksiya iqtisodi: kitob keltirgan raqamlar](#211-inspeksiya-iqtisodi-kitob-keltirgan-raqamlar)
- [2.12 Sifat narxni kamaytiradi: umumiy printsip va qaytarma aloqa halqasi](#212-sifat-narxni-kamaytiradi-umumiy-printsip-va-qaytarma-aloqa-halqasi)
- [2.13 Kichik o'zgarish eng xavfli: bir qatorli tuzatish](#213-kichik-ozgarish-eng-xavfli-bir-qatorli-tuzatish)
- [2.14 Amalda qo'llash](#214-amalda-qollash)

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

Reviewer ning diqqati chiziqli emas. Kichik diffda har satr ko'riladi, katta diffda ko'z yuguradi.

Raqamlar haqida halol bo'lish kerak. "Bir o'tirishda 200-400 satr" va "diqqat 60-90 daqiqadan keyin pasayadi" degan ko'rsatkichlar sanoat adabiyotida keng tarqalgan, lekin bu korpusda ularning birlamchi o'lchovi yo'q: quyidagi jadval ham o'lchov emas, amaliy mo'ljal.

Birlamchi manbada bor qism boshqacha qo'yilgan. Google ning CL muallifi uchun qo'llanmasi qattiq chegara bermaydi va shuni ochiq aytadi: "qanchasi juda katta" degan aniq qoida yo'q. Mo'ljal sifatida 100 satr odatda maqbul hajm, 1000 satr odatda juda katta. Muhimi esa yana bir o'lcham: o'zgarish nechta faylga tarqalgani. Bitta faylda 200 satrlik o'zgarish normal bo'lishi mumkin, xuddi shu 200 satr 50 faylga tarqalsa odatda juda katta. To'g'ri hajmning o'zi ham satrda emas, mazmunda o'lchanadi: CL **bitta o'zini o'zi to'ldirgan o'zgarish** bo'lishi kerak. Va oxirgi mezon reviewer da: senga maqbul ko'ringan hajm reviewer ni bosib ketishi mumkin, shuning uchun maqbul hajmni u bilan kelishib olish kerak.

| PR hajmi (o'zgargan satr) | Reviewer xulqi | Topish darajasi | Amaliy xulosa |
| --- | --- | --- | --- |
| 1-50 | Har satrni o'qiydi, kontekstni tekshiradi | Yuqori | Ideal hajm |
| 50-200 | O'qiydi, ba'zi joylarni tezlashtiradi | Yuqori | Normal hajm |
| 200-400 | Muhim joylarni tanlab o'qiydi | O'rtacha | Chegara |
| 400-1000 | Diagonal o'qiydi, dizaynga qaraydi | Past | Bo'lish kerak |
| 1000+ | "LGTM" | Nolga yaqin | Review emas, marosim |

Shu jadval qattiq qoida bermaydi va bera olmaydi: *Software Engineering at Google* ning 8-bobi Google da satr soni bo'yicha avtomatik rad etish yo'qligini va "kichik o'zgarish" ning rasmiy ta'rifi ham yo'qligini aytadi (batafsil: [40.13](../code-review/40-review-jarayonini-qurish.md#4013-qoida-va-korsatma-mashina-nimani-majburlaydi)). Amaliy mo'ljal esa shunday: mantiq qismi bir necha yuz satrdan oshganda satr-satr o'qish o'zini aldashga aylanadi. Agar bo'lish imkoni bo'lmasa (masalan, katta migratsiya yoki framework yangilanishi), review usuli o'zgaradi: satrlarni o'qish o'rniga xavf nuqtalari ro'yxati bo'yicha yuriladi va qolgani avtomatik tekshiruvga ishonib topshiriladi. Bu holat ham izohda ochiq yozilishi kerak.

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

Google ning muhandislik amaliyoti shu yerda aniq chegara qo'yadi va uni yozib qo'yish kerak, chunki u ikki tomonga ham ishlaydi.

Birinchi tomon: **javob berishning yuqori chegarasi bir ish kuni**. Fokuslangan ishning o'rtasida bo'lmasang, PR kelishi bilan o'qishga kirish kerak. Muhimi esa umumiy o'tish vaqti emas, **har bir javobning** tezligi: to'liq review ga vaqt yo'q bo'lsa ham, qachon qarashini aytgan qisqa javob, boshqa reviewer taklif qilish yoki dastlabki umumiy izoh berish jarayonni sezilarli yengillashtiradi. Hujjatning kuzatuvi shunday: review jarayoniga qilingan shikoyatlarning ko'pi aslida jarayonni tezlashtirish bilan yopiladi, qat'iylikni pasaytirish bilan emas. Turli vaqt zonasida esa qoida aniq: muallif ish kuni tugashidan oldin javob olsin, ulgurmasa ertangi ish kuni boshlanishiga tayyor bo'lsin.

Ikkinchi tomon, va bu birinchisidan ko'ra ko'proq buziladi: tezlik **yuzaki o'qishga ruxsat emas**. Hujjat shuni ham qattiq aytadi: reviewer review ga shuncha vaqt sarflashi kerak-ki, uning "LGTM" i "bu kod bizning standartimizga javob beradi" degani bo'lishiga ishonchi bo'lsin. Ya'ni "tez, lekin yuzaki" to'g'ri yechim emas; to'g'ri yechim tez va yetarli.

Fokus bilan to'qnashuvda esa ustunlik shaxsiy tezlikda. Kod yozayotgan paytda o'zini uzib review ga o'tish jamoaga PR muallifini bir oz kuttirishdan **qimmatroq** turadi, chunki uzilgandan keyin oqimga qaytish uzoq davom etadi. Shuning uchun review ishning tabiiy uzilish nuqtasida qilinadi: joriy vazifa tugaganda, tushlikdan keyin, yig'ilishdan qaytganda.

Oxirgi, amalda ko'p vaqt tejaydigan vosita: izohli LGTM. Hujjat uni uchta holatdan kamida bittasi bajarilganda beradi: reviewer muallif qolgan izohlarning hammasini to'g'ri hal qilishiga ishonchi bo'lsa; izohlarni bajarish shart bo'lmasa; yoki taklif kichik bo'lsa (import tartibi, yondosh xato, ishlatilmagan dependency). Reviewer qaysi holatni nazarda tutganini aytishi kerak. Bu ayniqsa muallif boshqa vaqt zonasida bo'lganda foydali: aks holda u faqat "LGTM" ni kutib bir kun yo'qotadi.

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

Review foydasi narxidan kam bo'lgan holatlar bor va ularni tan olish kerak. Masalan: bir qatorli konfiguratsiya o'zgarishi, versiya raqamini ko'tarish, matn tuzatish, test ma'lumotini qo'shish. Bunday o'zgarishlar uchun yengil yo'l qo'yish kerak: avtomatik approve qoidasi yoki post-commit review. Lekin "bir qatorli" degani "xavfsiz" degani emas: Code Complete ning ma'lumotiga ko'ra aynan bir qatorli tuzatishlar birinchi urinishda eng ko'p xato beradi ([2.13](#213-kichik-ozgarish-eng-xavfli-bir-qatorli-tuzatish)), shuning uchun yengil yo'l faqat mantiqqa tegmaydigan o'zgarish uchun ochiladi.

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

## 2.11 Inspeksiya iqtisodi: kitob keltirgan raqamlar

Review ning qaytimi haqidagi eng aniq raqamlar rasmiy inspeksiya bo'yicha o'lchangan va ular Code Complete ning birgalikda ishlash bobida yig'ilgan. Boshlang'ich raqam muammoning hajmini ko'rsatadi: Software Engineering Institute kuzatuvlarida dasturchi dizaynga o'rtacha soatiga 1-3 va kodga soatiga 5-8 xato kiritadi. Birgalikda ishlash amaliyotlarining butun mantiqi shunda: dasturchi o'z ishining ba'zi muammoli joylarini ko'rmaydi, boshqa odamning ko'r nuqtalari esa boshqa joyda.

| O'lchov | Natija |
| --- | --- |
| Har soat inspeksiya qancha ishni oldini oladi (IBM) | taxminan 100 soat test va tuzatish ishi |
| Har soat inspeksiya qancha maintenance ishini oldini oladi (katta programmalar kuzatuvi) | o'rtacha 33 soat; inspeksiya test dan 20 barobargacha samarali |
| Rework ulushi inspeksiyaga qaratilgan tashabbusdan keyin (Raytheon) | loyiha narxining taxminan 40 foizidan 20 foiziga tushdi |
| Bitta xatoni topish narxi (IBM) | inspeksiya bilan 3.5 odam-soat, test bilan 15-25 soat |
| Bitta xatoni topish va tuzatish narxi (Microsoft ilovalar bo'limi) | inspeksiya bilan 3 soat, test bilan 12 soat |
| Investitsiya qaytimi (700 000 qatorli programma kuzatuvi) | kod review 1.38, test 0.17 |

Topish va tuzatish narxining farqi tasodifiy emas va kitob sababini aytadi: inspeksiya bir qadamli usul, u xatoning belgisini va sababini birga ko'rsatadi; test ikki qadamli, u faqat belgini beradi va sababni qidirish alohida ish bo'ladi. Shu sababli bir qadamli usullar umumiy hisobda sezilarli arzon tushadi.

Byudjet tomoni ham o'lchangan: dizayn va kod uchun inspeksiya ishlatadigan loyihada inspeksiya loyiha byudjetining taxminan 10-15 foizini oladi va odatda umumiy loyiha narxini pasaytiradi, unumdorlikni esa taxminan 20 foizga oshiradi. [2.5](#25-review-byudjeti-haftada-qancha-vaqt) dagi "haftaning 10-15 foizi" mo'ljali aynan shu o'lchovga tayanadi.

```text
# Byudjetni kitobdagi 10-15 foiz ulushidan hisoblash.
# Jamoa: 6 muhandis, haftada 6 x 40 = 240 muhandis-soat.

Review byudjeti (10%)  = 24 soat/hafta  = kuniga ~48 daqiqa har kishiga
Review byudjeti (15%)  = 36 soat/hafta  = kuniga ~72 daqiqa har kishiga

# Shu byudjet rejaga kirmasa, u "bo'sh vaqtda" qiladigan ishga aylanadi
# va navbat vaqti o'sadi (2.3). Byudjet rejada bo'lsa, u sprintdagi
# boshqa ishlar bilan bir xil holatda turadi.
```

Diqqat: bu raqamlar 1980-1990-yillardagi rasmiy inspeksiya o'lchovlari, PR review emas. O'sha paytdan beri ishning bir qismi mashinaga o'tdi: formatlash, uslub, null yo'li va ma'lum shablon xatolar endi linter va statik tahlil ishi. Shuning uchun raqamlarni qo'lda qilinadigan qatlam uchun yuqori chegara deb o'qish to'g'ri, prognoz deb emas.

## 2.12 Sifat narxni kamaytiradi: umumiy printsip va qaytarma aloqa halqasi

Code Complete sifat haqidagi bo'limini bitta gapga yig'adi va uni "Sifatning umumiy printsipi" deb ataydi: sifatni yaxshilash ishlab chiqish narxini **kamaytiradi**. Buning ortida bitta kuzatuv turadi: unumdorlikni oshirishning eng yaxshi yo'li kodni qayta ishlashga ketadigan vaqtni qisqartirish. Kitobning o'lchovi bo'yicha an'anaviy, o'ylanmagan ishlab chiqish siklida debugging va u bilan bog'liq qayta yozish vaqtning taxminan 50 foizini yeydi.

Bu da'vo maydon ma'lumoti bilan tasdiqlangan. NASA ning Software Engineering Laboratory 50 loyihani, 400 dan ortiq odam-yil mehnatni va qariyb 3 million qator kodni qamragan tahlilida sifat ta'minotining oshishi xato darajasining pasayishi bilan birga kelgan, lekin umumiy ishlab chiqish narxini oshirmagan. IBM da o'tkazilgan kuzatuv ham shu yo'nalishda: xato darajasi eng past bo'lgan loyihalar eng qisqa muddatda tugagan va eng yuqori unumdorlik ko'rsatgan.

Nega shunday ekanini tushuntirish uchun kitob xatoning kiritilish bosqichiga qaraydi: xato qancha erta kiritilsa, u boshqa qismlarga shuncha ko'p chalkashadi, va arxitektura darajasidagi bitta xato bir necha sinf va o'nlarcha metodga ta'sir qiladi, kod darajasidagi bitta xato esa kamdan-kam bitta metod yoki sinfdan chiqadi.

Google kitobi shu zanjirni oqim sifatida chizadi: xato narxi uni qancha kech tutsangiz, deyarli eksponensial o'sadi, chunki kech topilgan xatoni o'zgarishni bilmaydigan muhandis triage qiladi, muallif kontekstni qaytadan tiklashi kerak bo'ladi va u oradan boshqalarga ta'sir qiladi. Halqalar tezligi bo'yicha tartibi ham kitobda berilgan.

```text
# Qaytarma aloqa halqalari, tez dan sekinga (Google kitobi tartibi).
# Review shu zanjirning uchinchi bo'g'inida turadi.

1. lokal edit-compile-debug            soniyalar
2. presubmit avtomatik test natijasi   daqiqalar
3. PR review                           soatlar      <- shu hujjatning mavzusi
4. postsubmit integratsiya xatosi       soatlar
5. staging da QA topgan moslik xatosi   kunlar
6. ichki foydalanuvchi xabari           kunlar
7. tashqi foydalanuvchi yoki matbuot    haftalar

# Kitobning Takeout keysi shu zanjirni bir bo'g'in chapga surishning
# natijasini o'lchagan: testlarni "kechki deploy dan keyin" dan
# presubmit ga ko'chirish noto'g'ri konfiguratsiyadan sinadigan
# serverlarning 95 foizini oldini olgan va kechki deploy nosozligini
# 50 foizga kamaytirgan; uchidan-uchiga testlarni "ikki soat ichida
# postsubmit" ga ko'chirish aybdor o'zgarishlar to'plamini 12 barobar
# qisqartirgan.
```

Shundan review uchun amaliy xulosa chiqadi: review ni chuqurlashtirishdan oldin uning halqasini tezlashtirish arziydi, chunki bir bo'g'in chapga surish topilmani ko'paytirmasdan narxni pasaytiradi. Bosqichlar bo'yicha narx jadvali [2.1](#21-xato-narxi-bosqich-boyicha-osadi) da, CI tartibi esa [40-bobda](40-review-jarayonini-qurish.md#406-avtomatik-tekshiruvlar-tartibi).

## 2.13 Kichik o'zgarish eng xavfli: bir qatorli tuzatish

[2.8](#28-review-ning-qaytimi-qachon-manfiy-boladi) da review ni yengillatish mumkin bo'lgan holatlar sanalgan. Shu ro'yxatni tor saqlash uchun kitobdagi bitta ma'lumot yetarli, va u intuitsiyaga qarshi boradi: kichik o'zgarish katta o'zgarishdan ko'proq xatoga moyil.

Code Complete ning refactoring bobi uch faktni birga qo'yadi. Birinchi: dasturchi o'zgarishni birinchi urinishda xato qilish ehtimoli 50 foizdan yuqori. Ikkinchi: o'zgargan qator soni bittadan beshtaga o'sganda noto'g'ri o'zgarish ehtimoli **oshadi**, shundan keyingina pasayishni boshlaydi. Uchinchi va sababni tushuntiradigani: dasturchilar kichik o'zgarishga beparvo munosabatda bo'ladi. Ularni qo'lda tekshirib ko'rmaydi, boshqa odamga ko'rsatmaydi va ba'zan tuzatish ishlaganini tekshirish uchun kodni ishga ham tushirmaydi. Kitobning xulosasi bir gap: oddiy o'zgarishga murakkabday munosabatda bo'ling.

Review bu ehtimolni o'zgartirishi o'lchangan. Bir qatorli o'zgarishlar uchun review joriy qilgan tashkilotda xato darajasi 55 foizdan 2 foizga tushgan. Barcha o'zgarishlar hisobga olinganda esa review dan keyin 95 foiz o'zgarish birinchi urinishda to'g'ri chiqqan, review dan oldin bu ko'rsatkich 20 foizdan past edi. Boshqa, telekommunikatsiya tashkilotida kod o'zgarishini review qilish to'g'ri o'zgarishlar ulushini 86 foizdan 99.6 foizga ko'targan.

```java
// Bitta operator o'zgardi, diff bir qator. Kunlik limit mantiqi:
// oldin limitga TENG so'rov rad etilardi, endi o'tib ketadi.
public void authorize(Money todaySpent, Money amount, Money dailyLimit) {
    Money after = todaySpent.plus(amount);
    // Oldingi shart: after.compareTo(dailyLimit) >= 0  -> teng rad etilardi
    if (after.compareTo(dailyLimit) > 0) {              // teng endi ruxsat
        throw new LimitExceededException(after, dailyLimit);
    }
    ledger.record(amount);
}
```

Shu misolning review uchun ahamiyati shundaki, uning diffi "bir belgi" bo'lib ko'rinadi va yengil yo'ldan o'tishga eng ko'p nomzod bo'ladi. Shuning uchun [2.8](#28-review-ning-qaytimi-qachon-manfiy-boladi) dagi va [40-bobdagi](40-review-jarayonini-qurish.md#408-review-ni-otkazib-yuborish-mumkin-bolgan-holatlar) yengil yo'l ro'yxati faqat xulqqa tegmaydigan yo'llarni (hujjat, CHANGELOG) qamrashi kerak: mantiq yoki konfiguratsiyaga tegadigan bir qatorli o'zgarish aynan shu ma'lumot ogohlantirgan sinf.

Kitob yondashuvni xavf darajasiga bog'lashni ham tavsiya qiladi: oson va xavfsiz o'zgarishda jarayonni qisqartirib, faqat qayta test bilan yurish mumkin; xavfli o'zgarishda esa o'zgarishlar birma-bir qilinadi va ularni boshqa odam ko'radi yoki juftlikda bajariladi. Xavf bo'yicha tabaqalash jadvali [2.9](#29-byudjetni-xavf-boyicha-taqsimlash) da.

## 2.14 Amalda qo'llash

- [ ] Oxirgi 100 merge qilingan PR uchun birinchi javobni kutish vaqtining medianasi va p90 ini hisoblang.
- [ ] PR hajmi taqsimotini chiqarib, 400 satrdan katta PR ulushini aniqlang va shu PR larda topilgan izohlar sonini taqqoslang.
- [ ] CI ga PR hajmi haqida ogohlantirish qo'shing: mantiq satrlari 400 dan oshsa, izoh yozilsin (bloklamasin).
- [ ] Jamoada kunlik ikki review oynasini kelishib oling va uni kalendarga qo'ying.
- [ ] Xavf tabaqalash jadvalini `REVIEW.md` ga qo'shing va yuqori xavfli yo'llar uchun ikki reviewer talabini sozlang.
- [ ] Stacked PR usulini bitta katta funksiyada sinab ko'ring: sxema, domen va API ni uch PR ga bo'ling.
- [ ] Uchdan ko'p tuzatish davrasidan o'tgan oxirgi uch PR ni ko'rib, sababi talabda yoki dizaynda ekanini aniqlang.
- [ ] Trivial yo'llar ro'yxatini (docs, changelog) belgilab, ularga yengil yo'l bering va bu ro'yxatga konfiguratsiya fayllari kirmasligini tasdiqlang.

## Manbalar

- [Google, Speed of Code Reviews](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/speed.md) - bir ish kunlik yuqori chegara, javob tezligining umumiy o'tish vaqtidan muhimligi, fokuslangan ishni uzmaslik qoidasi, vaqt zonasi qoidasi, izohli LGTM ning uchta sharti
- [Google, Small CLs](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/developer/small-cls.md) - qattiq hajm chegarasi yo'qligi, 100 va 1000 satr mo'ljallari, fayl soni o'lchami, "bitta o'zini o'zi to'ldirgan o'zgarish" mezoni
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.1 (480-bet) - dasturchi dizaynga soatiga 1-3, kodga soatiga 5-8 xato kiritadi; ko'r nuqtalar mantiqi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.1 (480-481-betlar) - IBM: har soat inspeksiya taxminan 100 soat ishni oldini oladi; Raytheon da rework 40 foizdan 20 foizga tushgan; katta programmalar kuzatuvi: har soat inspeksiya o'rtacha 33 soat maintenance ishini oldini oladi va test dan 20 barobargacha samarali
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20.3 "Cost of Finding Defects" va "Cost of Fixing Defects" (472-473-betlar) - IBM: bitta xatoni topish inspeksiya bilan 3.5 odam-soat, test bilan 15-25 soat; Microsoft: topish va tuzatish 3 va 12 soat; bir qadamli va ikki qadamli usul farqi; ROI 1.38 va 0.17
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "What Results Can You Expect from Inspections?" (485-bet) - inspeksiya loyiha byudjetining 10-15 foizini oladi, umumiy narxni pasaytiradi va unumdorlikni taxminan 20 foizga oshiradi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20.5 "The General Principle of Software Quality" (474-475-betlar) - sifatni yaxshilash narxni kamaytiradi; rework vaqtning taxminan 50 foizi; NASA SEL va IBM kuzatuvlari
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20.4 "When to Do Quality Assurance" (473-bet) - erta kiritilgan xato ko'proq chalkashadi; arxitektura xatosi bir necha sinf va o'nlarcha metodga ta'sir qiladi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 23-bob, "Fast Feedback Loops" - xato narxi kech tutilganda deyarli eksponensial o'sadi; halqalar tartibi; narx o'sishining uch sababi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 23-bob, "CI Case Study: Google Takeout" - presubmit ga ko'chirish sinadigan serverlarning 95 foizini oldini olgan va kechki deploy nosozligini 50 foizga kamaytirgan; postsubmit ga ko'chirish aybdor to'plamni 12 barobar qisqartirgan
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 24.4 "Refactoring Safely" va rasm 24-1 (580-581-betlar) - birinchi urinishda xato ehtimoli 50 foizdan yuqori; bittadan beshta qatorga o'tganda xato ehtimoli oshadi; kichik o'zgarishga beparvo munosabat; bir qatorli o'zgarish review i xato darajasini 55 foizdan 2 foizga, telekom tashkilotida to'g'rilikni 86 foizdan 99.6 foizga o'zgartirgan; xavf darajasiga qarab yondashuvni sozlash
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.1 (481-bet) - review dan keyin o'zgarishlarning 95 foizi birinchi urinishda to'g'ri, oldin 20 foizdan past

---

[&larr; 1. Review nima uchun bor va nimani haqiqatda beradi](01-review-nima-uchun-bor-va-nimani-haqiqatda.md) · [Mundarija](README.md) · [3. Reviewer ning tahlil apparati: niyat, invariant, xavf yuzasi &rarr;](03-reviewer-ning-tahlil-apparati-niyat.md)
