# Repo o'zgardi: o'rnatilgan mashinalar nima qilishi kerak

Bu fayl `manguberdi` skillini **global o'rnatgan** mashinalar uchun.
Skill o'rnatilmagan bo'lsa va siz faqat klon ichida ishlasangiz, sizga
[klon ichida ishlayotganlar](#klon-ichida-ishlayotganlar) bo'limi yetarli.

## Nima o'zgardi

Qo'llanma ombori kengaydi va manba tekshiruvi qat'iylashdi.

| | Oldin | Hozir |
|---|---|---|
| Bob | 224 | 226 |
| Bo'lim | 3303 | 3652 |
| Qamrovi kuzatiladigan manba | yo'q | 51 |

Asosiy farq uchta:

1. **Qoidalar kitobga bog'landi.** `docs/BOOKS.tsv` da har kitobning har
   bobi uchun bitta qator bor va u qoidaning korpusda qayerdaligini
   ko'rsatadi. 1155 qator: 680 `bor`, 240 `qoshildi`, 230 `tashqari`,
   5 `kirmagan`.
2. **Olti kitob bo'lim darajasida audit qilindi** (Clean Architecture,
   Code Complete, Working Effectively with Legacy Code, A Philosophy of
   Software Design, PoEAA, xUnit Test Patterns). 1218 nomlangan
   qoidadan 155 tasi korpusda yo'q edi va yozildi. Qolgan 34 kitob
   hamon bob darajasida, bu `docs/BOOKS.tsv` sarlavhasida yozilgan.
3. **Manbasiz da'volar o'chirildi.** Avvalgi matnda kitobdan emas,
   taxmindan kelgan raqamlar bor edi. Ular olib tashlandi yoki manba
   bilan almashtirildi. `tools/known_errors.tsv` ga regressiya
   naqshlari qo'shildi: tuzatilgan xato qaytsa `check_docs` qizil
   beradi.

Hook, skill nomlari, aktyor fayllari va `install/` ning ishlashi
o'zgarmadi. Ya'ni o'rnatishni noldan qaytarish shart emas.

## Global o'rnatgan mashinalar

O'rnatuvchi yo'llarni klonga mutlaq bog'laydi, shuning uchun **klonni
ko'chirmang va o'chirmang**. Faqat uning manbasini almashtiring va
yangilang.

```bash
cd <klon papkangiz>

# 1. Avvalgi holatni saqlab qo'ying (qaytish kerak bo'lsa)
git branch zaxira-$(date +%Y%m%d)

# 2. Manbani almashtiring
git remote set-url origin https://github.com/manguberdikom/claude-genius.git
git fetch origin

# 3. Yangi tarixga o'ting
git checkout main
git reset --hard origin/main

# 4. Skillni qayta o'rnating: hook yo'llari va skill mazmuni yangilanadi
python3 install/install.py --update --apply
```

Windows da to'rtinchi qadam o'rniga:

```powershell
powershell -ExecutionPolicy Bypass -File install\manguberdi.ps1 -Update -Apply
```

Uchinchi qadamdagi `reset --hard` kerak, chunki ikki omborning tarixi
umumiy emas: oddiy `git pull` "unrelated histories" bilan to'xtaydi.
Shuning uchun birinchi qadamdagi zaxira branch bekorga emas.

## Klon ichida ishlayotganlar

Hech narsa o'rnatilmagan bo'lsa, yuqoridagi 2 va 3-qadam yetarli.
Keyin indeksni yangilang va tekshiring:

```bash
tools/doc.sh toc            # index/ ni qayta yasaydi
python3 tools/check_docs.py # xatosiz o'tishi shart
```

## O'zgarishdan keyin tekshirish

```bash
python3 tools/check_docs.py      # 0 xato
python3 tools/verify_claims.py   # 0 topilma
python3 tools/test_doc.py        # 97/97
python3 tools/test_check_docs.py # 72/72
```

To'rttasi ham yashil bo'lmasa, yangilanish to'liq tushmagan: `git status`
bilan qolgan mahalliy o'zgarishni qarang.

## Ikki ombor haqida

Loyihaning ikki nusxasi bor edi va ularning git tarixi umumiy emas:

- `akaukaclaude-sys/clouude-genius` - kitob qamrovi ishi shu yerda
  bajarildi, yangi 226 bob shu yerda;
- `manguberdikom/claude-genius` - o'rnatuvchilar ishlatadigan ombor.

Yangi mazmun ikkinchisiga `kitob-qamrovi` branchi orqali kiradi.
**O'tishdan oldin o'sha branch `main` ga merge qilinganiga ishonch
hosil qiling**, aks holda siz eski 224 bobli nusxaga tushasiz.
Tekshirish oson: `README.md` ning birinchi abzasida bob va bo'lim soni
yozilgan.

Birlashtirishda `memory/` ga ehtiyot bo'ling: `manguberdikom/claude-genius`
da beshta memory fayli bor va ular ikkinchi omborda yo'q
(`memory/umumiy/feedback_*.md` to'rttasi va
`memory/claude-genius/project_run-tests-exit-kodi.md`). Majburiy push
ularni o'chiradi, shuning uchun merge qilinadi, force qilinmaydi.
