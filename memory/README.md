# Memory ombori

Bu papka Claude sessiyalari orasida saqlanadigan bilimni ushlab turadi. Ikki
qismdan iborat tizimning saqlovchi qismi:

- Filtr: `../memory-protocol.md` qaysi bilim saqlanishini va qaysi joyga
  borishini belgilaydi. Qoidalar shu faylda, bu yerda takrorlanmaydi.
- Ombor: shu papka. Filtrdan o'tgan bilim git'da, proyekt bo'yicha yig'iladi.

## Nega git

Auto memory papkasi (`~/.claude/projects/<project>/memory/`) mashinaga bog'langan:
mashinalar va cloud muhitlari orasida bo'lishilmaydi. Cloud sessiyaning
konteyneri esa faoliyatsizlikdan keyin qaytarib olinadi. Ya'ni commit
qilinmagan bilim yo'qoladi.

Git ombori bu muammoni yechadi: bilim bir marta yoziladi, har mashinada va har
sessiyada o'qiladi, tarixi saqlanadi va o'zgarishi ko'rinadi.

## Tuzilish

```text
memory/
├── README.md              # shu fayl: ombor qoidasi va proyektlar ro'yxati
├── umumiy/                # barcha proyektlarga tegishli bilim
│   ├── MEMORY.md
│   └── user_*.md
└── <proyekt-slug>/        # bitta proyektga tegishli bilim
    ├── MEMORY.md          # index: har yozuv bitta qator
    ├── user_*.md
    ├── feedback_*.md
    ├── project_*.md
    └── reference_*.md
```

Fayl nomlari va frontmatter formati protokolning `Yozuv formati va nomlash`
bo'limida. Qaysi bilim `umumiy/` ga, qaysi biri proyekt papkasiga borishi va
takrorlanmaslik qoidasi protokolning `Marshrut` bo'limidagi jadvalda.

## Papka nomi qanday aniqlanadi

Nom taxmin qilinmaydi, qoidadan chiqadi:

| Holat | Papka nomi | Misol |
|---|---|---|
| GitHub repo bor | repo nomi, kichik harfda | `claude-genius` |
| Ikki egada bir xil repo nomi | `<egasi>__<repo>` | `manguberdikom__api` |
| GitHub repo yo'q | proyekt ildiz papkasining nomi | `test-stend` |

Papka mavjud bo'lmasa, yangisi yaratiladi va `MEMORY.md` indeks bilan
boshlanadi.

## O'qish ketma-ketligi

1. Ombor yangi holatda ekanini tekshir: `git pull`. Eski clone eskirgan bilim
   beradi, bu yozuvning yo'qligidan xavfliroq.
2. `umumiy/MEMORY.md` va `<proyekt-slug>/MEMORY.md` indekslarini o'qi. Ikkisi
   ham qisqa, bir yozuv bir qator.
3. Indeksdagi tavsifga qarab **faqat kerakli** topic faylni o'qi. Papkadagi
   hamma faylni o'qish kontekstni behuda yoqadi.

Proyekt papkasi yo'q bo'lsa, ish shundayoq boshlanadi: memory yo'qligi to'siq
emas.

## Yozish ketma-ketligi

1. Nomzodni protokol darvozasidan o'tkaz (yetti savol).
2. Darajani tanla: `umumiy/` yoki proyekt papkasi.
3. Mavjud yozuvni qidir. Bor bo'lsa **yangilanadi**, yangi fayl qo'shilmaydi.
4. Topic faylni yoz yoki yangila, indeksga bir qatorli tavsif qo'y.
5. Commit qil va push qil. Push qilinmagan yozuv saqlanmagan hisoblanadi.

Commit xabari qisqa bo'ladi: nima o'zgardi va qaysi proyekt.

```text
memory: claude-genius uchun hujjat yig'ish tuzoqlari qo'shildi
```

## Boshqa proyektdan qanday ulanadi

Har bir proyektning `CLAUDE.md` fayliga bitta blok qo'yiladi. Blokda qoida emas,
manzil turadi:

```markdown
## Memory

Bu proyektning memoryasi `manguberdikom/claude-genius` repodagi
`memory/<proyekt-slug>/` papkasida, umumiy bilim `memory/umumiy/` da.
Ish boshida o'sha ikki `MEMORY.md` indeksi o'qiladi, kerakli topic fayl
indeksga qarab o'qiladi. Yozish qoidasi: o'sha repodagi `memory-protocol.md`.
```

Omborni sessiyaga ulash:

| Muhit | Qanday |
|---|---|
| Cloud sessiya (claude.ai/code) | `claude-genius` repo sessiyaga qo'shiladi va clone qilinadi |
| Lokal sessiya | bir marta clone: `git clone https://github.com/manguberdikom/claude-genius ~/claude-genius`, keyin `claude --add-dir ~/claude-genius` |

`--add-dir` bilan qo'shilgan papkadagi `CLAUDE.md` fayllari default holda
yuklanmaydi. Bu aynan kerakli xatti-harakat: ombor avtomatik yuklanmaydi,
kerak bo'lganda o'qiladi.

## Hajm

Har bir `MEMORY.md` indeksi qisqa qoladi: bir yozuv bir qator, tafsilot topic
faylda. Indeks 200 qatorga yaqinlashsa, eski yozuvlar birlashtiriladi yoki
o'chiriladi. Sabab va qolgan chegaralar protokolning `Hajm budjeti va qattiq
chegaralar` bo'limida.

## Nima bu omborga tushmaydi

Sir, token, parol, shaxsiy ma'lumot, kodidan chiqarib olinadigan narsa, bir
martalik vazifa tafsiloti. To'liq ro'yxat protokolning `Memoryga
yozilmaydigan narsalar` bo'limida. Ombor ochiq git repoda turadi, shuning
uchun sir masalasida istisno yo'q.

## Proyektlar

| Papka | Proyekt | Izoh |
|---|---|---|
| `umumiy/` | hammasi | til va uslub talablari |
| `claude-genius/` | `manguberdikom/claude-genius` | parallel agentlar bilan hujjat yozish tuzoqlari |
