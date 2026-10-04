# Memory bosqichi

Ish toza tugagandan keyin bajariladi. Maqsad: keyingi sessiyada
takrorlanmasligi kerak bo'lgan narsani saqlab qo'yish.

Qoida manbai `memory-protocol.md`. Bu yerda u takrorlanmaydi, faqat
shu zanjirga tegishli qismi.

## Avval darvoza

Har nomzod `memory-protocol.md` dagi **yetti savol** darvozasidan
o'tadi. Bittasida to'xtasa, yozilmaydi. Eng ko'p to'xtatadigan uchtasi:

- Keyingi sessiyada foyda beradimi? Faqat shu vazifaga kerak bo'lsa, yo'q.
- Kodidan yoki git tarixidan chiqarib olish mumkinmi? Mumkin bo'lsa, yo'q.
- Tekshirib bo'ladigan darajada aniqmi? "Toza kod yoz" kabi bo'lsa, yo'q.

## Nomzod qayerdan chiqadi

Zanjir uchta joyda nomzod beradi:

| Qayerda | Nomzod turi |
|---|---|
| Foydalanuvchi tuzatdi yoki yondashuvni rad etdi | `feedback` |
| `review` bir xil kamchilikni ikkinchi marta topdi | `feedback` |
| Qaror sababi kodda ko'rinmaydi (nega shunday tanlandi) | `project` |
| Reja yarim qoldi, holati saqlanishi kerak | `project` |

Signal bo'lmasa, nomzod ham yo'q. "Foydali bo'lishi mumkin" signal emas.

## Qayerga yoziladi

`memory-protocol.md` dagi marshrut jadvali hal qiladi. Eng tez-tez
uchraydigan uchtasi:

- Sessiyalar orasida saqlanishi kerak va proyektga tegishli:
  `memory/<proyekt-slug>/` va indeksga bir qator.
- Barcha proyektlarga tegishli afzallik: `memory/umumiy/`.
- Har sessiyada kerak bo'ladigan qisqa qoida: loyiha `CLAUDE.md`.
- Majburiy bajarilishi shart: memory emas, **hook**. Memory kafolat
  bermaydi.

## Yozuv shakli

Bitta yozuv bitta mavzu. Fayl nomi `<tur>_<mavzu>.md`. Indeksga
(`MEMORY.md`) bitta qator qo'shiladi: fayl nomi va nima haqida ekani.

Yozuv o'zi qisqa: nima aniqlandi, qachon, qanday tekshiriladi. Uzun
tushuntirish qo'llanmada, memoryda emas.

## Yozilmaydigan narsalar

- Sir, token, parol. Faqat joyi aytiladi, qiymati emas.
- Bir martalik vazifa tafsiloti.
- Qo'llanmada allaqachon yozilgan qoida. Memory qo'llanmaning nusxasi
  emas: o'rniga bo'lim raqami keltiriladi.
- Bugungi ish hisoboti. U git tarixida.

## Oxirida

Memoryga yozilgan yoki yozilmagani **aytiladi**. Jim o'tish yomon:
foydalanuvchi nima saqlanganini bilishi kerak.

```
Memory: <N> yozuv qo'shildi (<fayl nomlari>) | yangi yozuv yo'q, sababi: <...>
```
