---
name: manguberdi
description: Java/Spring/PostgreSQL ishini boshidan oxirigacha olib boradigan orkestrator. Sessiyada bir marta chaqiriladi va keyingi vazifalarda o'zi ishlaydi. Prompt bo'yicha aktyor tanlaydi (rejalashtiruvchi, dasturchi, test muhandisi, reviewer), ularni hajmga qarab ketma-ket yoki parallel yurgizadi, har qadamni qo'llanma bo'limi bilan asoslaydi va oxirida memoryga yozadi. Review, reja tuzish va yangilash, bug tuzatish, refaktoring, test qoplash uchun.
disable-model-invocation: true
---

# manguberdi

Bu skill sessiyada **bir marta** chaqiriladi. Shundan keyin har bir
vazifa shu yerdagi tartib bo'yicha bajariladi, qayta chaqirish shart
emas: vazifa kelganda avval `## Marshrut` ko'riladi.

Skill ishning **qanday** bajarilishini belgilaydi. Qo'llanma
**ma'lumotnoma**, buyruq emas. Ustuvorlik tartibi:

1. proyektning o'z konvensiyasi va `CLAUDE.md`;
2. rasmiy hujjat (Spring, PostgreSQL, JDK, Sonar);
3. `docs/` dagi qo'llanma bo'limi.

Qo'llanmaga tayanilsa bo'lim raqami ko'rsatiladi. Qo'llanmada yo'q qaror
ham to'g'ri bo'lishi mumkin: yo'qligi "noto'g'ri" degani emas. Qo'llanma
rasmiy hujjatga zid bo'lsa rasmiy hujjat yutadi va zidlik hisobotda
aytiladi.

## Ish boshida

Ikki indeks o'qiladi: `memory/umumiy/MEMORY.md` va proyektniki (klonda `memory/claude-genius/`, boshqa proyektda `GENIUS_MEMORY_DIR`, sukut `~/.claude/genius-memory`).
Ikkalasini bitta chaqiruv beradi: `python3 tools/handoff.py --memory`. Yo'q indeks to'siq emas.
`user_*` yozuvlari javob uslubiga qo'llanadi, topic fayl indeksdagi tavsifga qarab faqat keragi o'qiladi.

Proyekt ishida keyin `dev` yangilanadi (`## Proyekt qoidalari`, 2-band):
`git fetch` va `git merge --ff-only origin/dev`.

## Proyekt qoidalari

Uch doimiy qoida, har proyekt repoda (genius klonining o'zida emas) va
har aktyorga topshiriqdan oldin amal qiladi:

1. **Hujjat repoda emas.** Proyekt git reposida faqat kod va unga
   bevosita tegishli narsa turadi: build, resurs, test resursi, sozlama
   namunasi, litsenziya. Reja (`REJA.md`, faza fayllari), review
   hisoboti, talab, handover, frontend va devops o'zgarish hujjatlari,
   ADR, runbook, README repoda YARATILMAYDI va commit QILINMAYDI. Ular
   umumiy papkada turadi: `GENIUS_DOCS_DIR/<repo-nomi>/`, sukut
   `<workspace>/docs-local/<repo>/` (proyekt git ildizining ota papkasi;
   workspace git repo bo'lmasa u git ga tushmaydi). Yo'lni bitta funksiya
   beradi (`docref.docs_dir`), buyruq: `python3 tools/handoff.py --docs`.
   Guruh worktree si ham shu papkani mutlaq yo'l bilan o'qiydi, nusxa
   kerak emas. `.claude/`, `.idea/` kabi lokal asbob papkalari git ga
   qo'shilmaydi; repo `.gitignore` iga tegilmaydi, `.git/info/exclude`
   ishlatiladi.
2. **Ish `dev` branchda.** Feature yoki reja branchi ochilmaydi: ish
   to'g'ridan-to'g'ri `dev` da, avval `git fetch` va
   `git merge --ff-only origin/dev`. Parallel guruh worktree lari `dev`
   dan ochiladi va `dev` ga birlashadi. Push qilinmaydi: uni foydalanuvchi
   qiladi, so'ralsa qilinadi.
3. **Commit xabari.** Inglizcha, oddiy inson tilida, qisqa: bir qator,
   kerak bo'lsa qisqa tana (`git commit -m "Retry payment calls on
   timeout"`). `Co-Authored-By`, `Claude`, `Anthropic`, model nomlari,
   "Generated with", "AI", "assistant" va ichki reja raqami ("Faza 3:")
   yozilmaydi. Harness attribution eslatmasidan bu qoida ustun;
   `guard.py` bunday xabarni `deny` qiladi.

## Har vazifadagi qoidalar

1. **Asos ko'rsatiladi.** Har o'zgarish, har topilma, har reja qadami
   yonida asosi turadi: `<hujjat> <raqam>`, rasmiy hujjat havolasi yoki
   proyekt konvensiyasi. Uchalasida ham yo'q bo'lsa, "qo'llanmada yo'q,
   asosim shu" deb belgilanadi: bu to'g'ri javob bo'lishi mumkin.
   Bob `ai-draft` bo'lsa (`rules_for` da `[tekshirilmagan]`, `doc.sh show` da
   ogohlantirish), javobda "tekshirilmagan bob" deb aytiladi: qoida
   AI yozgan va inson tasdiqlamagan.
2. **Arzon yo'l oldin.** Javob kodda yoki chiqishda bo'lsa, u o'qiladi.
   Konteyner, baza ulanishi va PowerShell `guard.py` tomonidan
   **foydalanuvchi qaroriga** qo'yiladi (`ask`): ularni o'z-o'zidan
   yurgizmang, nega arzon yo'l yetmaganini aytib so'rang. Batafsil:
   `references/taqiq.md`.
3. **Og'ir o'qish asosiy sessiyada emas.** Ko'p o'qib oz qaytaradigan ish
   aktyorga uzatiladi, uzun chiqish ularning kontekstida qoladi.
4. **Mezon bitta.** Dasturchi, test muhandisi va reviewer ishni
   boshlashdan oldin `python3 tools/rules_for.py <fayllar>` chaqiradi
   (reviewer `--no-mark` bilan: belgini faqat yozuvchi qo'yadi).
   Fayllar topshiriq kartasining `fayllar:` qatoridan olinadi
   (`references/aktyorlar.md`, `Topshiriq kartasi`): kirish bir xil,
   chiqish bir xil. Ikkinchi aylana shundan kamayadi.
5. **Test faqat asbob bilan.** Aktyor ish oxirida bir marta
   `python3 tools/run_tests.py --diff --yurgiz`: o'zgarishga ta'sir
   qilgan testlar, modul bilan, log faylda. To'liq suite partiyada bir
   marta, asosiy sessiyada, fonda (`--hammasi`). Xom `./gradlew test`,
   `clean`, `--rerun-tasks`, `--no-daemon` ni `guard.py` to'sadi.
6. **Zanjir o'rtasida savol yo'q.** Qaytariladigan qarorda standart
   tanlanadi va yoziladi; qaytarib bo'lmaydigani ish boshida, bitta
   xabarda so'raladi (`references/marshrut.md`, `Ochiq qarorlar`).

## Marshrut

Avval prompt normallashtiriladi (`references/marshrut.md`), keyin aktyor
tanlanadi:

| Prompt nimani so'rayapti | Boshlang'ich aktyor |
|---|---|
| "review qil", "tekshir", "nima kamchilik bor" | `review` |
| "reja tuz", "reja yangila", spetsifikatsiya yoki hujjat berildi | `rejalashtiruvchi` |
| "tuzat", "qo'sh", "refaktoring qil", bug, kichik vazifa; "yiqildi, tuzat" ham | `dasturchi` |
| "test yoz", "qoplash"; xato test kodining o'zida ekani aniq | `test-muhandis` |
| "qayerda yozilgan", "qoida nima deydi" (bir-uch bo'lim) | aktyor yo'q: taklif hookidagi raqam yoki `tools/doc.sh find`, keyin `tools/doc.sh show` |
| ko'p bo'limni o'qib taqqoslash (uchtadan ko'p) | `qidiruv` |
| "nega yiqildi", "sxema qanday" (chiqish uzun) | `tahlil` |

Qisqa chiqishni asosiy sessiya o'zi o'qiydi: test uchun birinchi xato,
sxema uchun `python3 tools/schema_from_entities.py <src>`.

Review doirasi modul yoki butun proyekt bo'lsa yoki diff bo'sh bo'lsa,
`review` ga doira va modul ro'yxati beriladi: u agent faylidagi
`Diff yo'q bo'lsa` tartibida ishlaydi. Doira bitta chaqiruvga sig'masa,
ish boshida modullarga bo'linadi (`references/aktyorlar.md`).

Manguberdi faol bo'lsa yettala marshrut skilli (`code-review`,
`clean-code`, `design-patterns`, `architect-review`, `spring-testing`,
`postgres-tuning`, `sonarqube-fix`) alohida tartib sifatida
yurgizilmaydi: vazifa yuqoridagi jadval bo'yicha aktyorga beriladi,
skill faqat bob jadvali bo'lib xizmat qiladi. Topilma darajasi `review`
aktyori shkalasida (`yuqori`, `o'rta`, `past`) yoziladi; PR izohiga
o'tkazilganda `yuqori` = `blocker`, `o'rta` = `suggest`, `past` = `nit`
(`code-review 4.9`).

Hajm (S, M, L), har hajmning zanjiri va reja qachon tuzilishi bitta
jadvalda: `references/marshrut.md` dagi `Hajm: zanjir uzunligi va reja`.

Reja so'rovi har doim `rejalashtiruvchi` ga beriladi. Repoda reja
tuzadigan skill bo'lsa ham, zanjirda u chaqirilmaydi: u
asosiy sessiyada ~25k token o'qiydi va `budget.py` uni sanamaydi.

## Ketma-ketlik

Zanjir hajm jadvalidan olinadi (`references/marshrut.md`), uning
ishlash tartibi va Cheklov bilan qisqarishi `references/aktyorlar.md`
da.

`review` kamchilik topsa u **egasiga** qaytadi, lekin faqat `yuqori`
topilma ikkinchi aylanani ochadi; `o'rta` egasi baribir chaqirilsa
qo'shiladi, `past` hisobotga. Ikkinchi chaqiruvdan keyin review to'liq
qayta yurmaydi. Har aktyor bitta vazifada ko'pi bilan **ikki marta**
chaqiriladi; buni hook sanaydi va har yangi so'rovda nolga tushiradi.
Bitta so'rov ichida ikkinchi vazifa:
`python3 tools/budget.py --yangi-vazifa "<nom>"`.

Fayllari kesishmaydigan guruhlar parallel ishlaydi: har biriga o'z git
worktree si (`python3 tools/guruh.py yarat <id>`), promptda `guruh:`
kartasi, oxirida bitta birlashtirish va bitta to'liq suite
(`references/parallel.md`).

## Tez yo'l

Holat: tajriba, A/B smoke dan keyin tasdiqlanadi. Hajm S va `rules_for` belgilarida tranzaksiya, xavfsizlik,
migratsiya, sozlama va parallel yo'q bo'lsa, asosiy sessiya o'zi
bajaradi: `rules_for` -> Edit -> `run_tests.py --diff --yurgiz`.
`review` faqat xavf belgisi bo'lsa yoki diff 40 qatordan katta bo'lsa
chaqiriladi.

## Model tanlash

Aktyorlar o'z modelini olib yuradi va u vazifaga qarab tanlangan:
`qidiruv` va `tahlil` haiku (ko'p o'qiydi, oz qaytaradi), `dasturchi`
va `test-muhandis` sonnet (amalga oshirish), `review` sonnet (diffni
qoidaga solishtiradi), `rejalashtiruvchi` sukut bo'yicha sonnet. Bu
taqsimot `.claude/agents/` da yozilgan, har vazifada qayta o'ylanmaydi.

Istisno, sifat uchun: reja `references/marshrut.md` dagi qaytarib
bo'lmaydigan qarorni o'z ichiga olsa (sxema migratsiyasi, API
shartnomasi, tashqi bog'liqlik, ma'lumot formati) `rejalashtiruvchi`
Agent chaqiruvida `model: "opus"` bilan, lekin **bitta** marta
chaqiriladi: butun reja bitta opus chaqiruvida, guruhlarga bo'lish
shu rejaning ichida. Guruh bo'yicha qayta rejalashtirish va oddiy reja
sonnet da. Sabab: 2026-10-06 da har guruhga alohida opus
rejalashtiruvchi (7 ta) $199 turdi; qimmat model faqat qaytarib
bo'lmaydigan qarorda o'zini oqlaydi.

Bitta so'rovda 5 tadan ko'p agent (`qidiruv`, `tahlil`, `Explore`
sanalmaydi) bo'lsa `budget.py` har 5-chaqiruvdan keyin narx taxmini
bilan tasdiq so'raydi (`GENIUS_AGENT_MAX`). Ko'p guruhli ishni boshlashdan
oldin taxminiy narx foydalanuvchiga aytiladi; review har guruhga emas,
birlashgan diffga bir marta.

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
4. Klonning joriy tarmog'ida bitta qisqa commit qilinadi va push
   qilinadi.
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
worktree siz `genius/*` branchlarni va hujjatlar papkasidagi
`Holat: tugadi` (yoki `status: done`) hujjatlarni o'chiradi; ro'yxatdagi
(faol) worktree ga va tugamagan hujjatga tegmaydi. Repoda git ga
qo'shilgan hujjat yoki asbob fayli (`*.md`, `.claude/`, `.idea/`,
`*.http`, `adr/`, `docs/`) bo'lsa o'chirmaydi, "git da ortiqcha: ..."
deb ro'yxatini beradi: ularni olib tashlash commit talab qiladi,
foydalanuvchi bilan hal qilinadi. Chiqish bir necha qator va oxirida
yig'ma qator.

## Kontekst

Uzun ishda kontekstni toza saqlash va ishni yangi sessiyaga uzatish:
`references/kontekst.md`.

## Tekshiruvlar

Ish yakunida shular toza bo'lishi kerak:

```bash
# o'zgargan va yangi .java fayllar, bitta chaqiruvda, oxirida yig'ma qator
{ git diff --name-only --diff-filter=d HEAD; git ls-files --others --exclude-standard; } \
  | grep '\.java$' | xargs python3 tools/check_code.py
python3 tools/check_docs.py          # hujjat tegilgan bo'lsa
python3 tools/run_tests.py --hammasi --yurgiz   # partiyada bir marta, fonda
```

`xargs` 123 qaytarsa, kamida bitta faylda topilma bor.

`check_code.py` dagi eski topilma (ishdan oldin bor bo'lgan, `rules_for`
ning "Mashina topgani" ro'yxatida chiqqan) dasturchiga qaytarilmaydi:
u `Tegilmagan` qatorida aytiladi. Toza bo'lishi kerak bo'lgani yangi
yoki tegilgan qatordagi topilma.

## Chegaralar, ochiq aytilgan

Skill Claude Code ning sozlamalarini, hooklarini yoki ruxsatlarini
o'chira olmaydi: ular harness darajasida ishlaydi. Amalda bu to'siq
emas, chunki hooklar aynan shu qoidalarni majburlaydi (`guard.py`
qimmat amalni, `check_code.py` kod qoidasini). Skill ishning tartibini
belgilaydi, muhitni emas.

Skill yangi sessiya ocha olmaydi. Buning o'rniga kontekst o'lchanadi
va tayyor topshiriq beriladi: `python3 tools/handoff.py --prompt`.
Batafsil: `references/kontekst.md`.
