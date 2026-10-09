# Parallel guruhlar va bitta to'liq suite

Ishchi papka bitta bo'lsa ikki Gradle yoki Maven bir vaqtda `build/`
va `target/` ni bir-biriga yozadi, shuning uchun guruhlar ketma-ket
yurardi. Har guruhga o'z git worktree si beriladi: o'z build papkasi,
o'z test yurishi. `~/.gradle` va `~/.m2` keshlari umumiy, bir vaqtda
ishlatishga chidaydi.

Guruh asosiy daraxtning **joriy holatidan** boshlanadi, HEAD dan emas:
`yarat` vaqtinchalik commit oladi (alohida indeks bilan `add -A`,
`write-tree`, `commit-tree -p HEAD`), asosiy branch va indeks
o'zgarmaydi. Shuning uchun oldingi partiyaning birlashtirilgan natijasi
guruhda bor, iflos daraxt to'siq emas. Reja repoda emas, hujjatlar
papkasida (`handoff.py --docs`): guruh uni mutlaq yo'l bilan o'qiydi,
worktree ga nusxalanmaydi. Guruh worktree lari `dev` dan ochiladi va
`dev` ga birlashadi. Worktree `<root>/.claude/worktrees/genius-<id>` da, loyiha ichida:
Edit va Write ruxsat so'ramaydi. Papka `.git/info/exclude` orqali
yashiriladi, `.gitignore` ga tegilmaydi.

## Qachon parallel

Ikkala shart bir vaqtda bo'lsa:

- ish ikki va undan ko'p guruhga bo'linadi va guruhlarning **fayllari
  kesishmaydi** (odatda modul bo'yicha; rejada `Guruh:` qatori);
- guruh soni chegaradan oshmaydi (`GENIUS_GURUH_MAX`, standart CPU dan:
  2 dan 4 gacha). Ortiqchasi navbatda turadi.

Biror shart bajarilmasa yoki `yarat` 0 dan boshqa qaytarsa guruhlar
ketma-ket ishlaydi. Bu savol emas: foydalanuvchidan so'ralmaydi,
hisobotda bir qator bilan aytiladi.

## Tartib

```bash
python3 tools/guruh.py yarat orders          # har guruh uchun, ish boshida
python3 tools/guruh.py yarat billing
python3 tools/guruh.py royxat                # papka, branch, fayl soni
```

`yarat` lardan keyin darhol, fonda (Bash `run_in_background`):
`python3 tools/run_tests.py --ildiz <papka> --isit`. Yangi worktree da
`build/` yo'q va birinchi yurish hammasini kompilyatsiya qiladi; aktyor
kod o'qiyotgan daqiqalarda shu kompilyatsiya tugaydi. Maven da har guruh
o'z fon buyrug'i bilan. Gradle da hammasi bitta fon buyrug'ida ketma-ket
(`...--ildiz <A> --isit; ...--ildiz <B> --isit`): birinchisi
kompilyatsiyani lokal build cache ga yozadi, keyingilari cache dan
oladi. Isitish
va aktyorning `--yurgiz` i bitta daraxtda hech qachon bir vaqtda
yurmaydi: ildiz qulfi keyingisini kutdiradi.

Har aktyor promptining boshida **guruh kartasi** turadi. Uni asosiy
sessiya bir marta yozadi va guruhning har chaqiruviga aynan ko'chiradi,
aktyor buni qayta qidirmaydi:

```
guruh: orders
papka: /abs/yo'l/app/.claude/worktrees/genius-orders
asos: 3f2a1c9e7b10
vazifa: <normallashtirilgan bir jumla>
hajm: M
fayllar: <tegiladigan ishlab chiqarish fayllari>
cheklov: <normallashtirilgan Cheklov> | yo'q
qabul mezoni: <...>
qarorlar: <tanlangan standartlar, qoida raqami bilan>
test: python3 tools/run_tests.py --ildiz <papka> --asos <asos> --yurgiz
```

`guruh:` qatori budjetni guruhga ajratadi (`budget.py`): ikki guruhning
dasturchisi bitta hisobni yemaydi. Id `guruh.py yarat` bilan
ro'yxatga olingan bo'lishi shart, aks holda chaqiruv umumiy hisobga
tushadi. `hajm`, `fayllar` va `cheklov` qatorlari umumiy topshiriq
kartasidan (`references/aktyorlar.md`, `Topshiriq kartasi`). `papka:` qatori aktyorga barcha
yo'llar shu papka ichida ekanini aytadi: Bash buyruqlari `cd <papka>`
bilan, Edit va Write mutlaq yo'l bilan. Asosiy daraxtga yozish guruh
izolyatsiyasini buzadi.

Guruhlar bir xabarda bir nechta Agent chaqiruvi bilan yurgiziladi: har
guruhning birinchi aktyori bir vaqtda.

Sessiya papkasi repo bo'lmagan ota papka bo'lsa (bir nechta repo ni
ichiga olgan workspace), hook cwd dan holat faylini topolmaydi.
`budget.py` shunda kartadagi `papka:` yo'lidan umumiy `.git` ni oladi
(worktree ham git repo), shuning uchun `papka:` qatori har chaqiruvda
bo'lishi shart: usiz parallel guruhlar umumiy hisobda 3-chaqiruvdan
boshlab to'siladi.

## Cross bosqichi: ko'p paketga tegadigan qoidalar

Issue lar paket bo'yicha kesishmaydigan guruhlarga bo'linadi. Ko'p
paketga tegadigan qoidalar guruhga berilmaydi, ular kesishmaydi degan
shartni buzadi: deprecated API ni o'chirish (`java:S1874`, `java:S1133`,
`java:S6355`, `java:S5738`, `java:S1123`) va restricted nomli metodni
qayta nomlash (`java:S6213` method). Ular alohida "cross" worktree da,
o'z branchida commit bilan bajariladi va oxirida `dev` ga haqiqiy
`git merge` (3-way) bilan qo'shiladi. Paket guruhlari patch sifatida qo'shiladi
(`guruh.py birlashtir --3way`).

`GENIUS_GURUH_MAX` to'lgan bo'lsa cross uchun `guruh.py yarat` o'rniga
oddiy `git worktree add -b <branch> <papka>` ishlatiladi va oxirida
`git merge <branch>`. Papka guruh kartasidagi kabi `papka:` bilan beriladi.

Har `birlashtir` dan keyin kompilyatsiya: guruhlar yozgan yangi kod
cross o'chirgan yoki qayta nomlagan API ga murojaat qilishi mumkin.
Sonar API ning `sources/lines` chaqiruvi fayl boshiga sekin va timeout siz
osiladi: qatorma-qator coverage ni lokal JaCoCo XML dan oling
(`run_tests.py --coverage`).

## Birlashtirish va to'liq suite

Guruh o'z zanjirini tugatishi bilan darhol `birlashtir` (oxirgisini
kutmasdan): erta qo'shilgan guruh keyingi guruhlarning ziddiyatini
erta ko'rsatadi. To'liq suite esa hamma guruh birlashgach bir marta
yuradi:

```bash
python3 tools/guruh.py birlashtir orders     # patch indeksga, commit yo'q
python3 tools/guruh.py birlashtir billing
python3 tools/run_tests.py --hammasi --yurgiz   # fonda: Bash run_in_background
# suite natijasi kelgach: yiqilgan test qaysi guruhniki
python3 tools/guruh.py royxat --fayllar      # har guruh ostida o'z fayllari
# faqat shundan keyin, birlashtir 0 qaytargan guruh:
python3 tools/guruh.py tozala orders
```

Tartib qat'iy: birlashtir, to'liq suite (fonda), natija kelgach egani
topish, keyin tozala. To'liq suite **partiyada bir marta** yuradi, guruh
yoki aktyor bo'yicha emas. U maqsadli tanlashning xavfsizlik to'ri:
yiqilgan test fayli (yoki u sinaydigan kod fayli) qaysi guruhniki ekani
`guruh.py royxat --fayllar` dan topiladi. Birlashgan guruhning fayllari
`birlashtir` holat fayliga yozgan `files` ro'yxatidan, qolganiniki
worktree dan. Kamchilik shu guruh egasiga qaytadi, agar egasining
budjeti qolgan bo'lsa (ikkinchi chaqiruv, o'sha `guruh:` kartasi bilan). Budjeti tugagan bo'lsa (M zanjiridagi
tuzatish aylanasi uni ishlatgan bo'lishi mumkin) yiqilgan test va
sababi hisobotga yoziladi va shu guruh zanjiri to'xtaydi.

Tozalash ikki shartdan keyin: guruhning `birlashtir` i 0 qaytargan va
to'liq suite natijasi kelgan. Suite dan oldin tozalansa yiqilgan testni
guruhga bog'laydigan worktree va holat yozuvi yo'qoladi. `birlashtir` 1
qaytargan, ziddiyatda qolgan yoki budjeti tugab to'xtagan guruh
tozalanmaydi: uning ishi faqat o'z worktree sida.

`guruh.py` buni o'zi ham ushlaydi. Birlashtirilmagan va o'zgarishi bor
guruhni `tozala` rc=1 bilan rad etadi va fayllarini aytadi, `tozala
--hammasi` faqat birlashgan yoki o'zgarishsiz guruhlarni oladi va
qolganini sanab rc=1 qaytaradi. `tozala <id> --majburiy` ishni
o'chiradi: faqat u boshqa yo'l bilan asosiy daraxtga tushgani aniq
bo'lganda (masalan `--3way` ziddiyati hal qilingach) yoki foydalanuvchi
qarori bilan. Holat fayli buzilgan bo'lsa (yo'l guruhning o'z worktree si
emas yoki branch `genius/<id>` emas) rc=2 qaytadi va hech narsa
o'chmaydi: yozuvni foydalanuvchi qo'lda tekshiradi.

Kesishgan guruh asosiy daraxtga tegmaydi: `birlashtir` kesishgan
fayllarni aytadi. Ikki yo'l: `--3way` bilan qo'llab ziddiyatni egasi
asosiy daraxtda hal qiladi, yoki shu guruh boshqalaridan keyin ketma-ket
bajariladi. `--3way` ziddiyat bilan tugasa guruh birlashgan
hisoblanmaydi: ziddiyat hal qilingach `tozala <id> --majburiy`. Kesishish reja xatosi: keyingi partiyada guruhlar fayl
bo'yicha aniqroq bo'linadi.

## Tezlikni yeydigan narsalar

- **Umumiy resurs.** Testlar qat'iy port yoki lokal baza ishlatsa
  (Testcontainers emas), parallel test yurishlari bir-birini buzadi:
  `run_tests.py ... --navbat` ularni ketma-ket qiladi, kod yozish esa
  parallel qoladi. `run_tests.py --tashxis` buni ko'rsatadi.
- **Birinchi build.** Yangi worktree da `build/` yo'q: birinchi yurish
  to'liq kompilyatsiya. Gradle da `run_tests.py` kompilyatsiyani lokal
  build cache ga yozadi (test natijasini emas) va keyingi worktree uni
  cache dan oladi. Loyiha `org.gradle.caching` ni o'zi tanlagan bo'lsa
  uning sozlamasi amal qiladi (`false` da cache yo'q, `true` da test
  natijasi ham cache dan).
- **Git da yo'q fayl.** `.env` yoki lokal sozlama worktree ga
  tushmaydi: `guruh.py yarat <id> --nusxa .env`.
