# Zanjir oxiri, model tanlash, Sonar va memory

`SKILL.md` dagi `Zanjir oxiri` shu faylga tayanadi. L hajmda, partiya
oxirida yoki model tanlashda o'qiladi.

## Model tanlash

To'rt aktyor bir xil bilim bilan ishlaydi; `dasturchi` opus da (kod
sifati: 2026-10-19 dagi 6 vazifali A/B da bir xil karta bilan sonnet
minimal kodda 7.3, opus 8.8; 4 vazifali sinovda opus takror metodsiz), `rejalashtiruvchi`, `test-muhandis`, `review` sonnet da (narx): qoidalar agent
faylida emas, `rules_for` chiqishida (retsept kartasi, `Umumiy yozish
qoidalari`, boblar, punktlar, avvalgi xatolar). Bir xil fayl va
`--vazifa` bilan chaqirgan har aktyor bir xil matnni oladi; agent
faylida faqat rolning tartibi turadi. Bu taqsimot `.claude/agents/` da
yozilgan, har vazifada qayta o'ylanmaydi.

Istisno, sifat uchun: reja `references/marshrut.md` dagi qaytarib
bo'lmaydigan qarorni o'z ichiga olsa (sxema migratsiyasi, API
shartnomasi, tashqi bog'liqlik, ma'lumot formati) `rejalashtiruvchi`
Agent chaqiruvida `model: "opus"` bilan, lekin **bitta** marta
chaqiriladi: butun reja bitta opus chaqiruvida, guruhlarga bo'lish
shu rejaning ichida. Guruh bo'yicha qayta rejalashtirish va oddiy reja
sonnet da. Sabab: 2026-10-06 da har guruhga alohida opus
rejalashtiruvchi (7 ta) $199 turdi; qimmat model faqat qaytarib
bo'lmaydigan qarorda o'zini oqlaydi.

Bitta so'rovda 5 tadan ko'p agent (`Explore` sanalmaydi) bo'lsa `budget.py` har 5-chaqiruvdan keyin narx taxmini
bilan tasdiq so'raydi (`GENIUS_AGENT_MAX`). Ko'p guruhli ishni boshlashdan
oldin taxminiy narx foydalanuvchiga aytiladi; review har guruhga emas,
birlashgan diffga bir marta.

## Sonar darvozasi

Zanjir oxirining tartibi: proyekt commiti -> to'liq suite (unit va
integration, jacoco bilan, partiyada bir marta) -> `sonar_local.py
tahlil` -> push (foydalanuvchi) -> memory -> genius saboq -> tozala.

```bash
python3 tools/sonar_local.py tahlil     # chiqish kodi 0 / 1 / 2, oxirida yig'ma qator
```

Lokal SonarQube asosiy server bilan bir xil sozlanadi (versiya, profil,
gate, loyiha sozlamalari, qo'lda qo'yilgan statuslar), shuning uchun
natija serverniki bilan bir xil. Darvoza: gate `OK` va ochiq issue 0
(TO_REVIEW hotspot ham topilma) bo'lmaguncha push tavsiya qilinmaydi.
Topilma bo'lsa u egasiga (`dasturchi` yoki `test-muhandis`) qaytadi va
tahlil qayta yuradi. Exit 2 (docker, tarmoq, token yo'q) darvozani
yopmaydi: sabab hisobotda aytiladi. Coverage to'liq bo'lishi uchun suite
shu partiyada jacoco bilan yurgan bo'lishi kerak (eskirgan exec ni asbob
o'zi aytadi; `--testlar` testlarni ham yurgizadi).

Birinchi marta konteyner yaratish (`docker run`, image yuklanadi) va
`ishga --yangila` foydalanuvchi roziligi bilan: asbob docker ni
`subprocess` bilan chaqirgani uchun `guard.py` buni ko'rmaydi, shuning
uchun asbob uni oldindan bir qator bilan aytadi. Konteyner bor bo'lsa
docker ga tegilmaydi.

Serverda (asosiy Sonar) lokalda chiqmagan issue topilsa, tuzatish va
proyekt commitidan keyin ikki ish PARALLEL yuradi: (a) genius saboq
(`check_code.py` qoidasi va qo'llanma, pastdagi tartib); (b)
`sonar_local.py moslik` va o'sha commit da `solishtir`: lokal nega
o'tkazib yuborganini topish. Konfiguratsiya farqi chiqsa `moslik` uni
tuzatadi, farq asbob bilmagan joyda bo'lsa `tools/sonar_local.py` ga
qo'shiladi. Ikkalasi yakunda bitta genius commitida.

## Memory

Memory bosqichi har zanjir oxirida bajariladi: toza tugaganda ham,
budjet tugab to'xtaganda ham. Qoida bitta faylda: `memory/README.md`.
Nima yoziladi, nima yozilmaydi, qayerga va qanday format. To'rt savol
darvozasidan o'tmagan narsa yozilmaydi.

Memorydan keyin genius saboq bosqichi keladi. U zanjirning oxirida,
proyekt commiti (va so'ralgan bo'lsa pushi) tugagandan keyin bajariladi,
shuning uchun proyekt commitiga ham, pushiga ham xalaqit bermaydi.
Ishda yangi Sonar yoki test saboqi chiqqan bo'lsa (Sonar topgan,
lekin `check_code` ushlamagan holat; tuzatish yangi issue ochgani;
test infratuzilmasi tuzog'i), u klonga yoziladi:

1. Qoida `tools/check_code.py` ga musbat va manfiy test bilan yoziladi.
   Tushuntirish `docs/` dagi mos bobga yoziladi.
2. Klon ochiq repo: proyekt nomi, modul, sinf va fayl nomlari
   yozilmaydi, misol umumiy bo'ladi (`memory/README.md`).
3. Tekshiriladi: `tools/test_check_code.py`, `tools/check_docs.py`.
4. Klonning `main` branchida bitta qisqa commit qilinadi va `main` ga push
   qilinadi. Klonda `main` dan boshqa branch ochilmaydi va boshqa branchga
   push qilinmaydi: butun bilim bitta tarmoqda turadi.
5. Snapshot yangilanadi:
   `python install/install.py --genius-path <klon> --apply`.

Saboq yo'q bo'lsa bosqich bir qator bilan "yangi saboq yo'q" deb
yopiladi.

Zanjirning haqiqiy oxiri tozalash (memory va saboq bosqichidan keyin):
ish tugagan hujjatlarning boshiga `Holat: tugadi` yoziladi, keyin
avtomatik yurgiziladi:

```bash
python3 tools/tozala.py            # --quruq: hech narsa o'chirmay ro'yxat
```

U `.claude/worktrees/` dagi ro'yxatda yo'q (yetim) papkalarni,
worktree siz `genius/*` branchlarni o'chiradi. Hujjatlar papkasidagi
`Holat: tugadi` (yoki `status: done`) hujjat o'chirilmaydi: u
`<docs-local>/.arxiv/<yyyymmdd>/` ga ko'chadi va 14 kundan keyin o'chadi.
Hujjat yoki uning papkasidagi biror fayl oxirgi 3 kunda o'zgargan bo'lsa
unga tegilmaydi: faol ishning tugagan bo'lagi (review qismi, faza) joyida
qoladi. Ro'yxatdagi (faol) worktree ga va tugamagan hujjatga tegmaydi.
Workspace da bir nechta sessiya ishlashi mumkin: `tozala` ning to'liq
chiqishi (har ko'chgan fayl nomi) ko'rsatiladi, faqat yig'ma qator emas. Repoda git ga
qo'shilgan hujjat yoki asbob fayli (`*.md`, `.claude/`, `.idea/`,
`*.http`, `adr/`, `docs/`) bo'lsa o'chirmaydi, "git da ortiqcha: ..."
deb ro'yxatini beradi: ularni olib tashlash commit talab qiladi,
foydalanuvchi bilan hal qilinadi. Chiqish bir necha qator va oxirida
yig'ma qator.
