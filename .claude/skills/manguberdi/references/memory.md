# Memory bosqichi

Zanjir oxirida bajariladi: u toza tugadimi yoki budjet tugab to'xtadimi,
farqi yo'q. Maqsad: keyingi sessiyada takrorlanmasligi kerak bo'lgan
narsani saqlab qo'yish.

Qoida manbai `memory-protocol.md`. Bu yerda u takrorlanmaydi, faqat
shu zanjirga tegishli qismi.

Protokol katta (~24 KB), butunligicha o'qilmaydi. Nomzod bo'lmasa umuman
ochilmaydi. Nomzod bo'lsa faqat kerakli bo'lim o'qiladi. Oraliq sarlavha
matniga bog'langan, bo'limlar qayta raqamlansa ham ishlaydi:

- darvoza va marshrut: `awk '/^## [0-9]+\. Marshrut/,/^## [0-9]+\. Saqlash/' memory-protocol.md`
- yozish (D va E faza): `awk '/^### D faza/,/^### F faza/' memory-protocol.md`
- yozuv formati: `awk '/^## [0-9]+\. Yozuv formati/,/^## [0-9]+\. Hajm/' memory-protocol.md`
- yozilmaydigan narsalar: `awk '/^## [0-9]+\. Memoryga yozilmaydigan/,/^## [0-9]+\. Boshqa MD/' memory-protocol.md`
- tozalash: `awk '/^## [0-9]+\. Eskirish/,/^## [0-9]+\. Cloud/' memory-protocol.md`

## Avval darvoza

Har nomzod `memory-protocol.md` dagi **yetti savol** darvozasidan
o'tadi. Bittasida to'xtasa, yozilmaydi. Eng ko'p to'xtatadigan uchtasi:

- Keyingi sessiyada foyda beradimi? Faqat shu vazifaga kerak bo'lsa, yo'q.
- Kodidan yoki git tarixidan chiqarib olish mumkinmi? Mumkin bo'lsa, yo'q.
- Tekshirib bo'ladigan darajada aniqmi? "Toza kod yoz" kabi bo'lsa, yo'q.

## Nomzod qayerdan chiqadi

Zanjir quyidagi holatlarda nomzod beradi:

| Qayerda | Nomzod turi |
|---|---|
| Foydalanuvchi tuzatdi yoki yondashuvni rad etdi | `feedback` |
| `review` bir xil kamchilikni ikkinchi marta topdi (zanjir shu yerda to'xtaydi) | `feedback` |
| Qaror sababi kodda ko'rinmaydi (nega shunday tanlandi) | `project` |
| Reja yarim qoldi, holati saqlanishi kerak | `project` |

Signal bo'lmasa, nomzod ham yo'q. "Foydali bo'lishi mumkin" signal emas.

## Qayerga yoziladi

`memory-protocol.md` dagi marshrut jadvali hal qiladi. Eng tez-tez
uchraydiganlari:

- Sessiyalar orasida saqlanishi kerak va proyektga tegishli:
  `memory/<proyekt-slug>/` va indeksga bir qator.
- Barcha proyektlarga tegishli afzallik: `memory/umumiy/`.
- Har sessiyada kerak bo'ladigan qisqa qoida: loyiha `CLAUDE.md`. U har
  navbatda to'lanadi. Shu repoda ishlanayotgan bo'lsa, yozishdan oldin
  `python3 tools/cost_report.py` zahirasi qaraladi. Yetmasa, mavjud qator
  qisqartirilib uning o'rniga yoziladi yoki yozuv `memory/<proyekt-slug>/`
  ga boradi. Boshqa proyektda bu asbob klonning `CLAUDE.md` sini o'lchaydi,
  o'sha proyektnikini emas: u yerda fayl 200 qatordan oshmasligi
  tekshiriladi.
- Faqat ma'lum fayllarga tegishli qoida: `.claude/rules/<mavzu>.md` +
  `paths:`. `paths:` siz rules ham har sessiyada yuklanadi, lekin
  `cost_report.py` uni sanamaydi.
- Majburiy bajarilishi shart: memory emas, **hook**. Memory kafolat
  bermaydi.

## Yozuv shakli

Yozishdan oldin `git pull`, keyin indeksda shu mavzu qidiriladi. Bor
bo'lsa topic fayl yangilanadi, yangi fayl va yangi indeks qatori
ochilmaydi.

Mavzu yangi bo'lsa: bitta yozuv bitta mavzu, fayl nomi
`<tur>_<mavzu>.md`, indeksga (`MEMORY.md`) bitta qator qo'shiladi: fayl
nomi va nima haqida ekani.

Yozuv o'zi qisqa: nima aniqlandi, qachon, qanday tekshiriladi. Uzun
tushuntirish qo'llanmada, memoryda emas.

## Yozilmaydigan narsalar

- Sir, token, parol. Faqat joyi aytiladi, qiymati emas.
- Bir martalik vazifa tafsiloti.
- Qo'llanmada allaqachon yozilgan qoida. Memory qo'llanmaning nusxasi
  emas: o'rniga havola `<hujjat> <raqam> (<mavzu>)` shaklida keltiriladi,
  raqam siljisa bo'lim mavzu nomi bilan topiladi.
- Bugungi ish hisoboti. U git tarixida.

## Oxirida

Yozuv ombor qoidasidagi yozish ketma-ketligi bilan yakunlanadi
(`memory/README.md`, `Yozish ketma-ketligi`): commit va push qilinadi,
ikkalasi foydalanuvchi ruxsati bilan. Push qilinmagan yozuv cloud
konteyneri bilan yo'qoladi. Push qilinmagan bo'lsa yoki yozuv default
bo'lmagan branch'da tursa, hisobotda shu ochiq aytiladi, chunki keyingi
sessiya uni ko'rmaydi.

Memoryga yozilgan yoki yozilmagani **aytiladi**. Jim o'tish yomon:
foydalanuvchi nima saqlanganini bilishi kerak. Ikki shakldan biri:

```text
Memory: <N> qo'shildi, <M> yangilandi (<fayl nomlari>), commit <qisqa hash>, push: qilindi <branch> | kutilmoqda, sababi: <...>
Memory: yangi yozuv yo'q, sababi: <...>
```
