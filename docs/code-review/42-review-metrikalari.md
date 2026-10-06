<!-- doc: code-review | chapter: 42 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 42. Review metrikalari (Measuring Review)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [42.1 Foydali metrikalar](#421-foydali-metrikalar)
- [42.2 Zararli metrikalar](#422-zararli-metrikalar)
- [42.3 Metrikalarni yig'ish](#423-metrikalarni-yigish)
- [42.4 Izohlarni sinflash](#424-izohlarni-sinflash)
- [42.5 Review samaradorligini o'lchash](#425-review-samaradorligini-olchash)
- [42.6 DORA metrikalari bilan bog'liqlik](#426-dora-metrikalari-bilan-bogliqlik)
- [42.7 Metrikalarni o'qish: tuzoqlar](#427-metrikalarni-oqish-tuzoqlar)
- [42.8 Amalda qo'llash](#428-amalda-qollash)

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

## 42.8 Amalda qo'llash

- [ ] `scripts/review-metrics.sh` ni qo'shib, oyda bir marta ishga tushirishni rejalashtiring.
- [ ] Kutish vaqtining median va p90 ini o'lchab, p90 ni alohida kuzatib boring.
- [ ] Reviewer taqsimotini chiqarib, bitta odamga 40 foizdan ko'p yuk tushmasligini ta'minlang.
- [ ] Izohlarni prefiks va mavzu bo'yicha sanab, eng ko'p takrorlanadigan uchtasini avtomatlashtiring.
- [ ] Incident tahlili shabloniga "review dan o'tganmi / nega ko'rinmadi / checklist bandi" ustunlarini kiriting.
- [ ] Odam bo'yicha o'lchanadigan review metrikalarini (izohlar soni, tezlik) ishlatmaslikni kelishib oling.
- [ ] Mutatsiya ballini coverage bilan birga kuzatib, ikkisining farqini tahlil qiling.

---

[&larr; 41. Review madaniyati, til va kelishmovchilik](41-review-madaniyati-til-va-kelishmovchilik.md) · [Mundarija](README.md) · [43. AI yozgan kodni review qilish va AI bilan review qilish &rarr;](43-ai-yozgan-kodni-review-qilish-va-ai-bilan.md)
