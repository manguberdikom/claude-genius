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

Ikki indeks o'qiladi: `memory/umumiy/MEMORY.md` va proyektniki (klonda `memory/claude-genius/`, boshqa proyektda `GENIUS_MEMORY_DIR`, sukut `<workspace>/docs-local/memory/<slug>/`).
Ikkalasini bitta chaqiruv beradi: `python3 tools/handoff.py --memory`. Yo'q indeks to'siq emas.
`user_*` yozuvlari javob uslubiga qo'llanadi, topic fayl indeksdagi tavsifga qarab faqat keragi o'qiladi.
"Qaysi versiya", "nima o'zgardi", "yangilanish ishlayaptimi" so'ralsa:
`python3 tools/versiya.py` (o'rnatilgan versiya, commit, sana, klonda
yangi commit bormi va shu versiyadagi o'zgarishlar ro'yxati).

## Proyekt qoidalari

Uch doimiy qoida, har proyekt repoda (genius klonining o'zida emas) va
har aktyorga topshiriqdan oldin amal qiladi:

1. **Hujjat repoda emas.** Proyekt git reposida faqat kod va unga
   bevosita tegishli narsa turadi: build, resurs, test resursi, sozlama
   namunasi, litsenziya. Reja (`REJA.md`, faza fayllari), review
   hisoboti, talab, handover, frontend va devops o'zgarish hujjatlari,
   ADR, runbook, README repoda YARATILMAYDI va commit QILINMAYDI. Ular
   umumiy papkada turadi: `GENIUS_DOCS_DIR/<repo-nomi>/`, sukut
   `<workspace>/docs-local/<repo>/` (proyekt git ildizining ota papkasi),
   proyekt memorysi ham shu yerda: `<workspace>/docs-local/memory/<slug>/`.
   `python3 tools/handoff.py --docs` va `--memory` papkani o'zi yaratadi
   va workspace git repo bo'lsa `docs-local/` ni `.git/info/exclude` ga
   qo'shadi: u commit ham, push ham qilinmaydi. Kompyuterning boshqa
   joyiga hech narsa yozilmaydi: `.bak`, `.orig`, `*-copy` kabi zaxira
   nusxa yaratilmaydi (o'zgarish tarixi git da), vaqtinchalik fayl ham
   `docs-local` da.
   Guruh worktree si ham shu papkani mutlaq yo'l bilan o'qiydi, nusxa
   kerak emas. `.claude/`, `.idea/` kabi lokal asbob papkalari git ga
   qo'shilmaydi; repo `.gitignore` iga tegilmaydi, `.git/info/exclude`
   ishlatiladi.
2. **Ish `dev` branchda.** Feature yoki reja branchi ochilmaydi: ish
   to'g'ridan-to'g'ri `dev` da, avval `git fetch` va
   `git merge --ff-only origin/dev` (`origin/dev` yo'q yangi repoda
   o'tkaziladi, hisobotda bir qator). Parallel guruh worktree lari `dev`
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
3. **Og'ir o'qish asbob orqali.** Uzun chiqishni asbob o'zi qisqartiradi
   (`run_tests` birinchi sabab, `schema_from_entities --only-findings`,
   `doc.sh show` bo'lim); butun modul review i `review` aktyorida.
4. **Mezon bitta.** Dasturchi, test muhandisi va reviewer ishni
   boshlashdan oldin `python3 tools/rules_for.py --vazifa="<topshiriq>" <fayllar>` chaqiradi
   (reviewer `--no-mark` bilan: belgini faqat yozuvchi qo'yadi).
   Fayllar topshiriq kartasidan olinadi, u har aktyor promptining
   boshida va zanjirning har chaqiruviga aynan ko'chiriladi:
   `hajm: S|M|L`, `fayllar: <ishlab chiqarish fayllari>`,
   `cheklov: <...>|yo'q`, `vazifa: <bir jumla>` (`--vazifa` qiymati),
   rejadan keyin `reja:` bloki (rejalashtiruvchi javobi, aynan).
   Kirish bir xil, chiqish bir xil. Ikkinchi aylana shundan kamayadi. Chiqish boshidagi
   `# Retsept` kartasi (`tools/retsept/<belgi>.md`) eng kichik to'g'ri
   shaklni, Spring yoki JDK allaqachon beradigan narsani va tuzoqlarni
   bo'lim raqami bilan beradi: yechim hajmi modelning o'z mulohazasiga
   qolmaydi, shuning uchun sonnet aktyor ham opus bilan bir xil shaklda
   yozadi.
5. **Test faqat asbob bilan.** Aktyor ish oxirida bir marta (bug
   qizilida va refaktoringda har harakatdan keyin tor `--qadam <test>`)
   `python3 tools/run_tests.py --diff --yurgiz`: o'zgarishga ta'sir
   qilgan testlar, modul bilan, log faylda. To'liq suite partiyada bir
   marta, asosiy sessiyada, fonda (`--hammasi`). Xom `./gradlew test`,
   test bilan `clean`, `--rerun-tasks`, `--no-daemon` ni `guard.py` to'sadi.
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
| "test yoz", "qoplash", flaky; xato test kodining o'zida | `test-muhandis` |
| "sekin", "N+1", "indeks", latency | `dasturchi`; avval `schema_from_entities.py <src> --only-findings`, `EXPLAIN (ANALYZE, BUFFERS)` va `pg_stat_statements` ish boshida bitta xabarda so'raladi (architect 24.12) |
| "quality gate yiqildi", sababi noma'lum | avval `sonar_local.py tahlil` (birinchi konteyner foydalanuvchi roziligi bilan), issue `dasturchi` ga, coverage `test-muhandis` ga |
| "qayerda yozilgan", "qoida nima deydi" (bir-uch bo'lim) | aktyor yo'q: taklif hookidagi raqam yoki `tools/doc.sh find`, keyin `tools/doc.sh show` |
| ko'p bo'limni o'qib taqqoslash (uchtadan ko'p) | aktyor yo'q: har bo'lim `tools/doc.sh show` bilan, qisqartmasiz |
| "nega yiqildi", "sxema qanday" | aktyor yo'q: `python3 tools/parse_test_output.py <log>`, `python3 tools/schema_from_entities.py <src> --only-findings` |

Kod vazifasida (aktyor yoki Tez yo'l) taklif hookidagi nomzod bo'limlar
`show` qilinmaydi: mezon `rules_for` kartasi va bo'lim raqamlari.
Nomzod faqat "qoida nima deydi" marshrutida o'qiladi.

Asboblar chiqishni o'zi qisqartiradi, uni asosiy sessiya o'qiydi; bo'lim
matni `doc.sh show` bilan to'liq.

Review doirasi modul yoki butun proyekt bo'lsa yoki diff bo'sh bo'lsa,
`review` ga doira va modul ro'yxati beriladi: u agent faylidagi
`Diff yo'q bo'lsa` tartibida ishlaydi (`references/review-diffsiz.md`). Doira bitta chaqiruvga sig'masa,
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
qayta yurmaydi. Budjet: `references/aktyorlar.md`; parallel guruh:
`references/parallel.md`.

## Tez yo'l

Hajm S bo'lsa qaror bitta qisqa chaqiruvdan:
`python3 tools/rules_for.py --no-mark --belgilar --vazifa="<vazifa>" <fayllar>`,
oxirgi qatori `tez_yol: ha|yo'q (<sabab>)`. `ha` bo'lsa asosiy sessiya
o'zi bajaradi (agent yo'q): `rules_for.py --vazifa=... <fayllar>`
(`--no-mark` siz; Sonar kaliti bo'lsa `tools/doc.sh rule <kalit>`) ->
test (Cheklov taqiqlamasa): bugda xatoni qayta hosil qiladigan test
`run_tests.py --qadam <test> --yurgiz` da QIZIL (clean-code 31.2), feature da
o'zgargan xatti-harakatga bitta test (sonarqube 17.2) -> Edit ->
`run_tests.py --diff --yurgiz` yashil. Yozib bo'lgach
`python3 tools/rules_for.py --no-mark --belgilar --diff` (yangi fayllar
ham kiradi) `tez_yol: yo'q` desa, diff 40 qatordan katta yoki bug
tuzatish bo'lsa (code-review 2.13) `review` chaqiriladi. `yo'q` bo'lsa zanjir `rejalashtiruvchi`
(`reja: ijro`) -> `dasturchi` (kartada `reja:` bloki bilan) -> `review`.

## Model tanlash

`rejalashtiruvchi` opus (vazifaga bir marta), `dasturchi`,
`test-muhandis` va `review` sonnet. Sabab, o'lchov va agent soni
chegarasi: `references/yakun.md`.

## Zanjir oxiri

**Partiya**: push dan oldingi commitlar to'plami. To'liq suite
(`run_tests.py --hammasi --yurgiz`) va `sonar_local.py tahlil`
foydalanuvchi commit yoki push so'raganda yoki partiya yopilganda bir
marta yuradi. Yolg'iz S vazifa `run_tests.py --diff --yurgiz` bilan
tugaydi va hisobotda `to'liq suite: partiya oxirida` deyiladi.

Zanjir oxiri tartibi (har zanjirda, budjet tugasa ham): proyekt commiti
-> partiyada to'liq suite va Sonar darvozasi (gate `OK`, yangi kodda 0 issue) ->
push (foydalanuvchi) -> memory (`memory/README.md`) -> genius saboq
yoki "yangi saboq yo'q" -> `python3 tools/tozala.py`. Har qadamning
tafsiloti `references/yakun.md` da.

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
python3 tools/sonar_local.py tahlil             # Sonar darvozasi: gate OK, yangi kodda 0 issue
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
