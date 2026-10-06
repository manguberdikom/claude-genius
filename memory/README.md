# Memory ombori

Sessiyalar orasida saqlanadigan bilim. Qoida shu faylda va boshqa joyda
takrorlanmaydi. Git da, chunki auto memory papkasi mashinaga bog'langan
va cloud konteyneri qaytarib olinadi: commit qilinmagan bilim yo'qoladi.

Bu klon ochiq git repo. Unga faqat ikki papka yoziladi: `umumiy/`
(hammaga tegishli) va `claude-genius/` (klonning o'z proyekti). Boshqa
proyekt memorysi klondan tashqarida, `GENIUS_MEMORY_DIR` da, sukut
bo'yicha `~/.claude/genius-memory/<slug>/`, push siz.

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
gap. Sir masalasida istisno yo'q.

Ochiq klonga boshqa proyektning matni yozilmaydi: proyekt nomi, vazifa
maqsadi, qarorlar, modul va fayl nomlari sir bo'lmasa ham maxfiy, git
tarixidan esa o'chirish qimmat. Klondagi begona `memory/<slug>/` ni
`git add` yoki `git commit` qilishni `tools/guard.py` foydalanuvchi
qaroriga qo'yadi.

Kontekst to'lganda yoziladigan topshiriq (handoff) memory emas, u bir
martalik: lokal sessiyada `tools/handoff.py --vazifa` uni
`.claude/.state/handoff/` ga git siz yozadi. Faqat cloud sessiyasida u
proyekt memorysiga `project_<vazifa>.md` bo'lib tushadi va ish tugagach
o'chiriladi.

## Qayerga va qanday

Hammaga tegishli bilim `umumiy/`, bitta proyektga tegishlisi
`<slug>/`. Slug `tools/docref.py` dagi `project_slug` qoidasi: repo nomi
kichik harfda, ikki egada bir xil nom bo'lsa `<egasi>__<repo>`, repo
yo'q bo'lsa ildiz papka nomi. Papka yo'q bo'lsa yaratiladi.

Proyekt papkasi qayerda (`docref.memory_dir`):

| Proyekt | Papka | Push |
|---|---|---|
| hammasi | `<klon>/memory/umumiy/` | ha |
| klonning o'zi | `<klon>/memory/claude-genius/` | ha |
| boshqa har proyekt | `$GENIUS_MEMORY_DIR/<slug>/`, sukut `~/.claude/genius-memory/<slug>/` | yo'q |

`GENIUS_MEMORY_DIR` ni xususiy git repoga qo'yish mumkin, unda commit
va push shu repoga va foydalanuvchi qaroriga ko'ra.

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

O'qish: ish boshida ikki `MEMORY.md` indeksi o'qiladi (proyektniki va
`umumiy/`), kerakli topic fayl indeksdagi tavsifga qarab o'qiladi.
`python3 tools/handoff.py --memory` ikkalasini joyidan qat'i nazar
bitta chaqiruvda beradi. Memory yo'qligi to'siq emas. `git pull` shart
emas.

Yozish: darvozadan o'tkaz, mavjud yozuvni qidir (bor bo'lsa yangilanadi,
yangi fayl qo'shilmaydi), yoz, indeksga bir qator qo'y. Keyin git
buyruqlari memory ildizida yuradi, ish proyektida emas:

```bash
git -C <memory ildizi> add -- <papka>
git -C <memory ildizi> commit -m "memory: <mavzu>"
git -C <memory ildizi> push --dry-run && git -C <memory ildizi> push
```

Memory ildizi: `umumiy/` va `claude-genius/` uchun klon, boshqa proyekt
uchun `GENIUS_MEMORY_DIR` (u git da bo'lmasa git qadami yo'q, fayl
yozilgani yetarli). Push klon uchun: cloud konteyneri qaytarib olinadi.
`push --dry-run` yiqilsa (huquq yo'q), lokal commit saqlangan
hisoblanadi va bu hisobotda aytiladi. Sessiya `main` da bo'lmasa yozuv
main ga PR bilan o'tadi, bu ham hisobotda aytiladi.

## Qachon o'chiriladi

Yozuv noto'g'ri bo'lib qolsa, takrorlansa yoki tekshirib bo'lmaydigan
bo'lsa. Ziddiyatda yangi yozuv yutadi va eskisi o'chiriladi, ikkisi
yonma-yon qoldirilmaydi. `MEMORY.md` 200 qatorga yaqinlashsa eski
yozuvlar birlashtiriladi.

Boshqa proyektdan ulanish: global o'rnatishda (`install/README.md`)
manguberdi ish boshida `tools/handoff.py --memory` bilan ikki indeksni
o'qiydi. Lokal sessiyada qo'lda ulash: bir marta clone va
`claude --add-dir <klon>`.

| Papka | Proyekt | Izoh |
|---|---|---|
| `umumiy/` | hammasi | til va uslub talablari |
| `claude-genius/` | `manguberdikom/claude-genius` | parallel agentlar bilan hujjat yozish tuzoqlari |
