<!-- doc: code-review | chapter: 42 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 42. Review metrikalari (Measuring Review)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [42.1 Foydali metrikalar](#421-foydali-metrikalar)
- [42.2 Zararli metrikalar](#422-zararli-metrikalar)
- [42.3 Metrikalarni yig'ish](#423-metrikalarni-yigish)
- [42.4 Izohlarni sinflash](#424-izohlarni-sinflash)
- [42.5 Review samaradorligini o'lchash](#425-review-samaradorligini-olchash)
- [42.6 DORA metrikalari bilan bog'liqlik](#426-dora-metrikalari-bilan-bogliqlik)
- [42.7 Metrikalarni o'qish: tuzoqlar](#427-metrikalarni-oqish-tuzoqlar)
- [42.8 O'lchov checklistni yasaydi: inspeksiyaning ma'lumot halqasi](#428-olchov-checklistni-yasaydi-inspeksiyaning-malumot-halqasi)
- [42.9 Topilma qayerda tug'iladi: tayyorlanish va yig'ilish](#429-topilma-qayerda-tugiladi-tayyorlanish-va-yigilish)
- [42.10 Mashina qatlamining o'lchovi: effective false positive](#4210-mashina-qatlamining-olchovi-effective-false-positive)
- [42.11 Amalda qo'llash](#4211-amalda-qollash)

</details>


Review ni o'lchash ikki xil xavf tug'diradi: o'lchamaslik (hech narsa yaxshilanmaydi) va noto'g'ri o'lchash (odamlar raqamni yaxshilaydi, review ni emas). Bu bob qaysi raqam foydali, qaysi biri zararli va ularni qanday o'qish kerakligini beradi.

## 42.1 Foydali metrikalar

| Metrika | Nimani ko'rsatadi | Maqsad |
| --- | --- | --- |
| Birinchi javobni kutish vaqti (median, p90) | Jarayon tezligi | Median < 4 soat, p90 < 1 kun |
| PR ning umumiy o'tish vaqti | Oqim | Median < 1 kun |
| PR hajmi (mantiq satrlari) | Review sifati imkoniyati | Median < 200 |
| Tuzatish davralari soni | Talab aniqligi | Median 1, p90 <= 2 |
| Review da topilgan xatolar / prodda topilganlar | Filtr samaradorligi | Tendentsiya o'sishi |
| Izohlarning sinflar bo'yicha taqsimoti | Reviewer vaqti qayerga ketyapti | `nit` < 20% |
| Reviewer larning taqsimoti | Bilim tarqalishi | Bitta odam < 40% |
| Incidentlarda "review ko'rmadi" soni | Checklist bo'shliqlari | Har biri checklistga band qo'shadi |
| Qayta ochilgan PR / revert soni | Sifat | Kamayish |

## 42.2 Zararli metrikalar

| Metrika | Nega zararli |
| --- | --- |
| Izohlar soni (reviewer bo'yicha) | Ko'p `nit` yozishga undaydi |
| Approve lar soni | Yuzaki review ga undaydi |
| Review tezligi (daqiqada) | Shoshilishga undaydi |
| Topilgan xatolar soni (reyting sifatida) | Raqobat va bahs keltiradi |
| Coverage foizi (yagona mezon) | Assertion siz testlar yozishga undaydi (5.9) |
| Muallif bo'yicha "xatolar soni" | Qo'rquv madaniyati, kichik PR lar yashiriladi |

Umumiy qoida: metrika odamni emas, jarayonni o'lchashi kerak. Odam bo'yicha o'lchangan har qanday review metrikasi ertami-kechmi o'yinga aylanadi.

## 42.3 Metrikalarni yig'ish

```bash
#!/usr/bin/env bash
# scripts/review-metrics.sh - oyda bir marta ishga tushiriladi.
set -euo pipefail
REPO="${1:?repo kerak: owner/name}"
LIMIT=200

echo "=== Birinchi javobni kutish vaqti (soat) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" \
  --json number,createdAt,reviews \
  --jq '[.[] | select((.reviews|length) > 0)
        | ((.reviews[0].submittedAt|fromdate) - (.createdAt|fromdate)) / 3600]
        | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor], max: .[-1]}'

echo "=== PR o'tish vaqti (soat) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" \
  --json createdAt,mergedAt \
  --jq '[.[] | ((.mergedAt|fromdate) - (.createdAt|fromdate)) / 3600] | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor]}'

echo "=== PR hajmi (o'zgargan satrlar) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" \
  --json additions,deletions \
  --jq '[.[] | .additions + .deletions] | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor], max: .[-1]}'

echo "=== Reviewer taqsimoti (bilim tarqalishi) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" --json reviews \
  --jq '[.[].reviews[]?.author.login] | group_by(.)
        | map({reviewer: .[0], count: length}) | sort_by(-.count)'

echo "=== Tuzatish davralari (review dan keyingi commitlar) ==="
gh pr list --repo "$REPO" --state merged --limit 50 --json number,reviews,commits \
  --jq '[.[] | select((.reviews|length) > 0) | (.reviews|length)] | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor]}'
```

## 42.4 Izohlarni sinflash

Eng foydali va eng kam qilinadigan o'lchov: reviewer vaqti qayerga ketyapti. Buni qo'lda, bir oyda bir marta 50 izohni ko'rib bajarish mumkin.

```bash
# Izohlarni yig'ish va prefiks bo'yicha sanash (prefikslar ishlatilsa).
gh pr list --repo "$REPO" --state merged --limit 50 --json number \
  --jq '.[].number' \
  | while read -r pr; do
      gh api "repos/$REPO/pulls/$pr/comments" --jq '.[].body'
    done > /tmp/comments.txt

for p in blocker suggest question nit praise; do
  printf '%-10s %s\n' "$p" "$(grep -ci "^$p:" /tmp/comments.txt || echo 0)"
done
echo "prefikssiz: $(grep -cvE '^(blocker|suggest|question|nit|praise):' /tmp/comments.txt)"

# Mavzu bo'yicha: eng ko'p takrorlanadigan izohlar - avtomatlashtirish nomzodlari.
grep -oiE '(format|import|naming|nom|test|transaction|tranzaksiya|index|indeks|null|timeout|log)' \
  /tmp/comments.txt | sort | uniq -c | sort -rn | head -10
```

Natijadan amaliy xulosa: eng ko'p takrorlanadigan uchta mavzu avtomatlashtirish yoki konvensiya yozish uchun nomzod (5.10).

## 42.5 Review samaradorligini o'lchash

Eng muhim savol - review haqiqatan xato tutyaptimi. Buni o'lchash uchun ikki raqam kerak: review da topilgan va prodda topilgan xatolar.

```markdown
<!-- Har incident tahlilida to'ldiriladigan jadval. -->
| Incident | Sabab (kod o'zgarishi) | Review dan o'tganmi | Nega ko'rinmadi | Checklist bandi |
|---|---|---|---|---|
| INC-102 | PR #1203, idempotentlik yo'q | Ha, 1 reviewer | Poyga holati tekshirilmagan | "ikki parallel so'rov" |
| INC-108 | PR #1241, migratsiya qulfi | Ha, 2 reviewer | Jadval hajmi bilinmagan | "jadval hajmi va qulf vaqti" |
| INC-115 | Konfiguratsiya o'zgarishi | Yo'q (yengil yo'l) | Review qilinmagan | Konfiguratsiya yengil yo'ldan olib tashlandi |
```

Bu jadval review ning eng qimmatli artefakti: u checklistni taxmin bilan emas, haqiqiy nosozliklar bilan to'ldiradi (12.10).

## 42.6 DORA metrikalari bilan bog'liqlik

Review jarayoni to'rtta DORA ko'rsatkichidan ikkitasiga bevosita ta'sir qiladi.

| DORA metrikasi | Review ning ta'siri |
| --- | --- |
| Deploy chastotasi | Sekin review - kamroq deploy |
| O'zgarishning yetib borish vaqti (lead time) | Kutish vaqti to'g'ridan-to'g'ri qo'shiladi |
| O'zgarish nosozlik darajasi | Review sifati bevosita ta'sir qiladi |
| Tiklanish vaqti | Kichik PR lar tezroq qaytariladi |

Shu sababli review ni tezlashtirish deploy chastotasini oshiradi, lekin review ni yuzaki qilish nosozlik darajasini oshiradi. Muvozanat nuqtasi: tez javob, lekin xavf bo'yicha tabaqalangan chuqurlik (2.9).

## 42.7 Metrikalarni o'qish: tuzoqlar

```text
# Tuzoq 1: median yaxshi, p90 yomon.
Median kutish 2 soat, p90 - 3 kun. Bu o'rtacha holat yaxshi, lekin
PR larning 10 foizi butunlay to'xtab qolganini bildiradi. Aynan shu
10 foiz eng katta PR lar va eng xavfli o'zgarishlar bo'lishi mumkin.

# Tuzoq 2: PR hajmi kichraydi, lekin soni oshdi.
Bu yaxshi (bo'lish ishlayapti) yoki yomon (bir o'zgarish sun'iy
bo'laklangan, har biri alohida ma'nosiz) bo'lishi mumkin. Tekshirish:
stacked PR lar bir-biriga bog'liqmi.

# Tuzoq 3: izohlar soni kamaydi.
Review yaxshilandi (kod sifati o'sdi) yoki yomonlashdi (reviewer lar
charchagan). Farqni ajratish: prodda topilgan xatolar tendentsiyasi.

# Tuzoq 4: coverage o'sdi, mutatsiya balli o'smadi.
Testlar qo'shildi, lekin ular hech narsa tekshirmaydi (5.9, 34.7).
```

## 42.8 O'lchov checklistni yasaydi: inspeksiyaning ma'lumot halqasi

Code Complete rasmiy inspeksiyani oddiy review dan ajratadigan belgilar orasiga bittasini alohida qo'yadi: har inspeksiyada ma'lumot yig'iladi va u keyingi inspeksiyalarni yaxshilash uchun qaytariladi. Shu halqa bo'lmasa inspeksiya oddiy yig'ilishdan farq qilmaydi.

Halqaning mexanikasi aniq. Yig'ilishdan bir kun ichida moderator hisobot chiqaradi: har topilma, uning **turi** va **og'irligi** bilan. Hisobot ikki ish qiladi: topilmalarning tuzatilishini ta'minlaydi va tashkilotning o'ziga xos muammolariga qaratilgan tekshiruv ro'yxatini yasash uchun xom ashyo beradi. Kitob ro'yxatning o'sishini ham tasvirlaydi: tez-tez uchraydigan xato turlari ro'yxatga qo'shiladi, boshida kiritilgan va endi uchramay qolganlari esa olib tashlanadi; bir necha inspeksiyadan keyin tashkilotda o'ziga moslashgan ro'yxat paydo bo'ladi va shu bilan birga dasturchilar qaysi sohada qo'shimcha tayyorgarlik yoki yordam kerakligi ham ko'rinadi. Ro'yxat uzunligining chegarasi [toza kod hujjatida](../clean-code/47-birgalikda-ishlash-va-orgatish.md#473-yangi-odamga-toza-kod-standartini-yetkazish): bir sahifa.

Kitob vaqt va topilma sonini yozib borishning yana bir foydasini beradi va u metrikalar bobining asosiy argumenti: ma'lumot bo'lsa, review ning foydasiga bo'lgan e'tirozga raqam bilan javob berasiz; ma'lumot bo'lmasa, qo'lingizda faqat "review yaxshiroqdek ko'rinadi" degan gap qoladi, va bu "test yaxshiroqdek ko'rinadi" deb o'ylaydigan odamni ishontirmaydi. Teskari tomoni ham bor: ma'lumot review sizning muhitingizda **ishlamayotganini** ham ko'rsatadi, va shunda jarayonni o'zgartirish yoki tashlash asosli bo'ladi.

```text
# Review topilmalari jurnali: oyda bir marta to'ldiriladi, odam nomi yo'q.
# tur -> keyingi oyning checklist bandini belgilaydi.

sana        PR     tur                    og'irlik  checklist-bandi
2026-02-03  #1203  poyga-holati           blocker   ikki parallel so'rov
2026-02-05  #1211  tranzaksiya-chegarasi  blocker   tranzaksiyada tashqi chaqiruv
2026-02-05  #1211  nomlash                nit       -
2026-02-11  #1228  migratsiya-qulfi       blocker   jadval hajmi va qulf vaqti
2026-02-18  #1244  indeks-yoq             suggest   yangi so'rov uchun indeks

# Oylik xulosa: eng ko'p takrorlangan uch tur checklistga chiqadi,
# bir chorakda bir marta ham uchramagan band ro'yxatdan tushadi.
```

Kitob jarayonni o'zgartirish tartibini ham qo'yadi: o'zgarishni o'lchamasdan kiritmang. Tashkilotlar bosqichlarni olib tashlaganda yoki birlashtirganda ko'pincha tejagandan ko'proq yo'qotgan. Kitobning xulosasi shu halqani o'z-o'zini optimallashtiradigan jarayon deb ataydi: standart ro'yxat va rollar uni tizimli qiladi, o'lchangan qaytarma aloqa esa ro'yxatni yaxshilab, tayyorlanish va yig'ilish tezligini kuzatib turadi.

Shu bilan birga topilma jurnali testdan kelgan ma'lumot bilan birga o'qiladi: kitobning dasturchi testi bobi test topgan xatolarning yozuvi qaysi xato turlari eng ko'p uchrayotganini ko'rsatishini va shu yozuv kelgusi review faoliyatini yo'naltirishi kerakligini aytadi. [42.5](#425-review-samaradorligini-olchash) dagi incident jadvali ham xuddi shu halqaning bir bo'g'ini.

## 42.9 Topilma qayerda tug'iladi: tayyorlanish va yig'ilish

Agar review ning bitta qismini o'lchash kerak bo'lsa, u yig'ilish emas. Code Complete AT&T da o'tkazilgan 13 review tahlilini keltiradi: review yig'ilishining o'zining ahamiyati oshirib ko'rsatilgan, chunki topilmalarning 90 foizi yig'ilishga **tayyorlanish** paytida topilgan va faqat taxminan 10 foizi yig'ilishning o'zida.

Shu natija asinxron PR review uchun kutilganidan ham muhim, chunki PR review tuzilishi bo'yicha yig'ilishga emas, kitobning "kodni o'qish" (code reading) amaliyotiga yaqin. Kitob u haqda shunday yozadi: reviewer lar kodni mustaqil o'qiydi, keyin muallif bilan uchrashadi, uchrashuv bir-ikki soat davom etadi va topilmalarga qaratiladi; qator-qator yurish urinishi yo'q, va uchrashuvning o'zi hatto qat'iy shart emas. Kitob bu shaklni masofada joylashgan reviewer lar uchun alohida qulay deb ataydi va foydasini shunday izohlaydi: har reviewer ning vaqti guruh dinamikasini boshqarishga emas, muammo topishga ketadi.

Samarasi ham o'lchangan: NASA ning Software Engineering Laboratory kuzatuvida kodni o'qish soatiga taxminan 3.3 xato topgan, test esa soatiga taxminan 1.8; loyiha hayoti bo'ylab kodni o'qish test turlariga nisbatan 20-60 foiz ko'proq xato topgan.

```text
# Nimani o'lchash: reviewer ning O'QISH vaqti va tezligi.
# Kitobdagi mo'ljallar taqqoslash uchun qavs ichida.

PR #1244   mantiq satrlari: 180
           reviewer o'qish vaqti: 25 daqiqa  -> 432 satr/soat
           (kitob mo'ljali: ilova kodi ~500 satr/soat tayyorlanish tezligi)

PR #1251   mantiq satrlari: 620
           reviewer o'qish vaqti: 20 daqiqa  -> 1860 satr/soat
           SIGNAL: mo'ljaldan 3 barobar tez. Bu review emas, diagonal o'qish.

# Izohlar sonini sanash bu signalni bermaydi: tez o'qilgan katta PR da
# ham bir nechta izoh chiqadi (42.2).
```

Shundan ikki amaliy o'lchov chiqadi. Birinchi: reviewer haqiqatan qancha vaqt sarflaganini va o'qish tezligini kuzatish, izohlar sonini emas. Ikkinchi: ikkinchi reviewer ning foydasi takrorlashda emas, boshqa narsani ko'rishda, va buni ham o'lchash mumkin - ikki reviewer topilmalarining kesishmasi. Kitobdagi kuzatuvlarga ko'ra inspeksiyada topilgan xatolarning faqat taxminan 20 foizi bir nechta inspektor tomonidan topilgan; o'lchov shu atrofda bo'lsa, ikkinchi reviewer o'z narxini qoplayapti. Raqamning manbasi va qolgan samara ko'rsatkichlari [1-bobda](01-review-nima-uchun-bor-va-nimani-haqiqatda.md#112-xato-topish-usullarining-olchangan-samarasi).

## 42.10 Mashina qatlamining o'lchovi: effective false positive

Review metrikalari odam qatlami bilan tugamaydi: diffga qaraydigan statik tahlil ham o'lchanadi, va Google ning statik tahlil bobi shu o'lchov uchun aniq tushuncha beradi.

Avval joylashuv: kitob code review ni statik tahlil natijalari uchun eng mos nuqta deb ataydi va sabablarini sanaydi. Muallif allaqachon o'zgarish kayfiyatida, shuning uchun taklif qilingan tuzatish katta uzilish bermaydi; muallif review ni kutib boshqa ishga o'tadi, ya'ni tahlil bir necha daqiqa ishlasa ham vaqt bor; reviewer tomonidan ogohlantirishni hal qilishga tabiiy bosim keladi; va tahlil umumiy muammolarni o'zi belgilab reviewer vaqtini tejaydi.

Asosiy tushuncha esa **effective false positive**, ya'ni foydalanuvchi ko'zi bilan o'lchangan noto'g'ri signal. Kitobning ta'rifi natijaga qaraydi: agar dasturchi muammoni ko'rib hech qanday ijobiy harakat qilmagan bo'lsa, u effective false positive. Bundan ikki kutilmagan natija chiqadi. Birinchi: texnik jihatdan to'g'ri, lekin chalkash yoki ahamiyatsiz ogohlantirish ham shu sanoqqa tushadi, chunki foydalanuvchi uni xuddi noto'g'ri signal kabi qabul qiladi. Ikkinchi: tahlil xato belgilagan, lekin dasturchi o'qiluvchanlik yoki saqlash osonligi uchun tuzatishni baribir kiritgan bo'lsa, bu effective false positive **emas**.

| Mezon (yangi tekshiruv uchun) | Kitobdagi talab |
| --- | --- |
| Tushunarlilik | chiqishni har qanday muhandis tushunsin |
| Harakatga tayyorlik | natija qanday tuzatish mumkinligini ko'rsatsin |
| Effective false positive | 10 foizdan past: dasturchi hech bo'lmaganda 10 holatdan 9 tasida haqiqiy muammoni ko'rayotganini his qilsin |
| Ta'sir | muammo to'g'rilikka tegmasligi mumkin, lekin dasturchi uni ongli ravishda tuzatishga arzigulik deb hisoblasin |

Kitob o'zining umumiy ko'rsatkichini ham beradi: yuzdan ortiq analizator bo'ylab effective false positive darajasi 5 foizdan past.

```bash
# Qoida bo'yicha harakat darajasini o'lchash: ogohlantirish tuzatildimi.
# Yangi kodga tushgan va keyin yopilgan issue nisbati qoidaning
# effective false positive ko'rsatkichiga yaqin signal beradi.
SONAR=https://sonar.acme.local
KEY=com.acme:orders

# 1) Yangi kodda ochilgan qoidalar bo'yicha taqsimot.
curl -sG "$SONAR/api/issues/search" \
  --data-urlencode "componentKeys=$KEY" \
  --data-urlencode "inNewCodePeriod=true" \
  --data-urlencode "facets=rules" --data-urlencode "ps=1" \
  | jq -r '.facets[] | select(.property=="rules") | .values[]
           | "\(.val)\t\(.count)\tochilgan"'

# 2) Shu davrda FIXED holatiga o'tganlar.
curl -sG "$SONAR/api/issues/search" \
  --data-urlencode "componentKeys=$KEY" \
  --data-urlencode "inNewCodePeriod=true" \
  --data-urlencode "resolutions=FIXED" \
  --data-urlencode "facets=rules" --data-urlencode "ps=1" \
  | jq -r '.facets[] | select(.property=="rules") | .values[]
           | "\(.val)\t\(.count)\ttuzatilgan"'

# Tuzatilgan/ochilgan nisbati past qoida - o'chirish yoki
# ogohlantirish matnini aniqlashtirish nomzodi.
```

Qulaylik tomonidan kitob yana bir qoida beradi va u shu o'lchovning sharti: diqqat faqat **yangi kelgan** ogohlantirishga qaratiladi. Ishlab turgan kodda qolgan eski muammo odatda faqat alohida muhim bo'lsa (xavfsizlik yoki jiddiy xato) tuzatishga arziydi, chunki tuzatishning o'zi xato kiritishi mumkin: kitobning misolida o'lik kod haqidagi ogohlantirishni o'sha kodni chaqirish bilan "tuzatish" test qilinmagan kodni birdan ishga tushiradi. Qolgan qoida qisqa: avtomatik tuzatilishi mumkin bo'lgan hamma narsa avtomatik tuzatilsin.

Diqqat: 10 foiz va 5 foiz raqamlari Google ning o'z platformasi chegaralari, sanoat standarti emas. Shovqinni kamaytirish va izohni qoidaga aylantirish amaliyoti [5-bobda](05-mashina-va-odam-sonarqube-dan-oldin-topish.md#510-shovqinni-kamaytirish-va-izohni-qoidaga-aylantirish).

## 42.11 Amalda qo'llash

- [ ] `scripts/review-metrics.sh` ni qo'shib, oyda bir marta ishga tushirishni rejalashtiring.
- [ ] Kutish vaqtining median va p90 ini o'lchab, p90 ni alohida kuzatib boring.
- [ ] Reviewer taqsimotini chiqarib, bitta odamga 40 foizdan ko'p yuk tushmasligini ta'minlang.
- [ ] Izohlarni prefiks va mavzu bo'yicha sanab, eng ko'p takrorlanadigan uchtasini avtomatlashtiring.
- [ ] Incident tahlili shabloniga "review dan o'tganmi / nega ko'rinmadi / checklist bandi" ustunlarini kiriting.
- [ ] Odam bo'yicha o'lchanadigan review metrikalarini (izohlar soni, tezlik) ishlatmaslikni kelishib oling.
- [ ] Mutatsiya ballini coverage bilan birga kuzatib, ikkisining farqini tahlil qiling.

## Manbalar

- [Google, Speed of Code Reviews](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/speed.md) - nimani o'lchash kerakligi: javob vaqti, umumiy o'tish vaqti emas
- [Google, The Standard of Code Review](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/standard.md) - sifat mezoni o'lchovga aylantirilganda nima saqlanishi kerakligi
- [maven-surefire, `TestSuiteXmlParser.java`](https://raw.githubusercontent.com/apache/maven-surefire/0c970adeb11e8a59b449be5b3be2a50c478c2a65/surefire-report-parser/src/main/java/org/apache/maven/plugins/surefire/report/TestSuiteXmlParser.java) - CI hisobotidan avtomatik yig'iladigan ma'lumot
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Formal Inspections" va "Inspection Report" (485, 488-489-betlar) - har inspeksiyada ma'lumot yig'ilib keyingisiga uzatilishi; hisobotda topilma turi va og'irligi; ma'lumot bo'lmasa faqat "yaxshiroqdek ko'rinadi" degan gap qolishi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Fine-Tuning the Inspection" (489-490-betlar) - checklistning o'sishi va qisqarishi; o'zgarishni o'lchamasdan kiritmaslik; bosqichni olib tashlash tejagandan ko'proq yo'qotgani
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Inspection Summary" (491-bet) - o'z-o'zini optimallashtiradigan jarayon: standart ro'yxat va rollar, o'lchangan qaytarma aloqa
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.1 (502-bet) - test topgan xatolar yozuvi eng ko'p uchraydigan xato turlarini ko'rsatadi va kelgusi review faoliyatini yo'naltiradi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.4 "Code Reading" (494-bet) - AT&T da 13 review tahlili: topilmalarning 90 foizi tayyorlanishda, taxminan 10 foizi yig'ilishda; NASA SEL: kodni o'qish soatiga 3.3, test 1.8 xato topgan va loyiha hayoti bo'ylab 20-60 foiz ko'proq topgan; kodni o'qishning masofadagi reviewer lar uchun qulayligi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 20-bob, "Make Static Analysis a Part of the Core Developer Workflow" - code review statik tahlil natijalari uchun eng mos nuqta; muallif review ni kutib turgani uchun tahlilga vaqt borligi; reviewer bosimi; tahlil reviewer vaqtini tejashi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 20-bob, "Focus on Developer Happiness" - effective false positive ta'rifi: dasturchi ijobiy harakat qilmagan holat; chalkash yoki ahamiyatsiz to'g'ri ogohlantirish ham shu sanoqqa tushishi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 20-bob, "Tricorder: Google's Static Analysis Platform" - yangi tekshiruv uchun to'rtta mezon, shu qatorda 10 foizdan past effective false positive; platformaning umumiy darajasi 5 foizdan past
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 20-bob, "Usability" - diqqatni faqat yangi kelgan ogohlantirishga qaratish; o'lik kod ogohlantirishini "tuzatish" xavfi; avtomatik tuzatilishi mumkin bo'lgan narsani avtomatik tuzatish

---

[&larr; 41. Review madaniyati, til va kelishmovchilik](41-review-madaniyati-til-va-kelishmovchilik.md) · [Mundarija](README.md) · [43. AI yozgan kodni review qilish va AI bilan review qilish &rarr;](43-ai-yozgan-kodni-review-qilish-va-ai-bilan.md)
