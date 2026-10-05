# Memory ombori

Sessiyalar orasida saqlanadigan bilim. Qoida shu faylda va boshqa joyda
takrorlanmaydi. Git da, chunki auto memory papkasi mashinaga bog'langan
va cloud konteyneri qaytarib olinadi: commit qilinmagan bilim yo'qoladi.

## Nima yoziladi

Nomzod uchta signaldan biri bilan paydo bo'ladi: foydalanuvchi tuzatdi,
xato ikkinchi marta takrorlandi, yoki kodidan topilmaydigan kontekst
oshkor bo'ldi. "Foydali bo'lishi mumkin" signal emas. Keyin to'rt savol,
bittasida to'xtasa yozilmaydi:

1. Keyingi sessiyada foyda beradimi? Faqat hozirgi vazifaga kerak bo'lsa yo'q.
2. Kod, fayl yo'li yoki git tarixidan chiqarib olinadimi? Olinsa yo'q.
3. CLAUDE.md yoki mavjud yozuv aytganmi? Aytgan bo'lsa borini yangila.
4. Tekshirib bo'ladigan darajada aniqmi? "Yaxshi kod yoz" kabi bo'lsa yo'q.

Yozilmaydi: sir, token, parol, shaxsiy ma'lumot (faqat joyi ko'rsatiladi,
masalan "kalit `.env` da, `API_KEY` nomi bilan"); bir martalik vazifa
tafsiloti; umumiy til yoki framework bilimi; bir hafta ichida eskiradigan
gap. Ombor ochiq git repoda, sir masalasida istisno yo'q.

## Qayerga va qanday

Hammaga tegishli bilim `umumiy/`, bitta proyektga tegishlisi
`<slug>/`. Slug `tools/docref.py` dagi `project_slug` qoidasi: repo nomi
kichik harfda, ikki egada bir xil nom bo'lsa `<egasi>__<repo>`, repo
yo'q bo'lsa ildiz papka nomi. Papka yo'q bo'lsa yaratiladi.

Har papkada `MEMORY.md` indeksi: bir yozuv bir qator, mazmunni
tasvirlaydi, o'zida saqlamaydi (kod bloki, jadval va tugagan ish tarixi
bo'lmaydi). Topic fayl nomi `<type>_<mavzu>.md`, kichik harf; `type`
to'rttadan biri: `user`, `feedback`, `project`, `reference`. Bir fayl
bir mavzu. `modified` ni qo'lda yozish shart emas, Claude Code o'zi
qo'yadi.

```markdown
---
type: feedback
modified: 2026-10-04T12:00:00Z
---
# Sarlavha
- Qisqa, tekshirib bo'ladigan bandlar.
```

## Ketma-ketlik

O'qish: `git pull`, keyin ikki `MEMORY.md` indeksi, keyin indeksdagi
tavsifga qarab FAQAT kerakli topic fayl. Memory yo'qligi to'siq emas.

Yozish: darvozadan o'tkaz, mavjud yozuvni qidir (bor bo'lsa yangilanadi,
yangi fayl qo'shilmaydi), yoz, indeksga bir qator qo'y, commit va push.
Push qilinmagan yozuv saqlanmagan hisoblanadi.

## Qachon o'chiriladi

Yozuv noto'g'ri bo'lib qolsa, takrorlansa yoki tekshirib bo'lmaydigan
bo'lsa. Ziddiyatda yangi yozuv yutadi va eskisi o'chiriladi, ikkisi
yonma-yon qoldirilmaydi. `MEMORY.md` 200 qatorga yaqinlashsa eski
yozuvlar birlashtiriladi.

Boshqa proyektdan ulanish: o'sha proyekt `CLAUDE.md` iga manzil qo'yiladi,
lokal sessiyada bir marta clone va `claude --add-dir <klon>`.

| Papka | Proyekt | Izoh |
|---|---|---|
| `umumiy/` | hammasi | til va uslub talablari |
| `claude-genius/` | `manguberdikom/claude-genius` | parallel agentlar bilan hujjat yozish tuzoqlari |
