# Parallel guruhlar va bitta to'liq suite

Ishchi papka bitta bo'lsa ikki Gradle yoki Maven bir vaqtda `build/`
va `target/` ni bir-biriga yozadi, shuning uchun guruhlar ketma-ket
yurardi. Har guruhga o'z git worktree si beriladi: o'z build papkasi,
o'z test yurishi. `~/.gradle` va `~/.m2` keshlari umumiy, bir vaqtda
ishlatishga chidaydi.

## Qachon parallel

Uchala shart bir vaqtda bo'lsa:

- ish ikki va undan ko'p guruhga bo'linadi va guruhlarning **fayllari
  kesishmaydi** (odatda modul bo'yicha; rejada `Guruh:` qatori);
- asosiy daraxt toza: commit qilinmagan o'zgarish yo'q (guruh HEAD dan
  boshlanadi va uni ko'rmaydi);
- guruh soni chegaradan oshmaydi (`GENIUS_GURUH_MAX`, standart CPU dan:
  2 dan 4 gacha). Ortiqchasi navbatda turadi.

Biror shart bajarilmasa guruhlar ketma-ket ishlaydi. Bu savol emas:
foydalanuvchidan so'ralmaydi, hisobotda bir qator bilan aytiladi.

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
papka: /abs/yo'l/app.guruh-orders
asos: 3f2a1c9e7b10
vazifa: <normallashtirilgan bir jumla>
fayllar: <tegiladigan fayllar>
qabul mezoni: <...>
qarorlar: <tanlangan standartlar, qoida raqami bilan>
test: python3 tools/run_tests.py --ildiz <papka> --asos <asos> --yurgiz
```

`guruh:` qatori budjetni guruhga ajratadi (`budget.py`): ikki guruhning
dasturchisi bitta hisobni yemaydi. `papka:` qatori aktyorga barcha
yo'llar shu papka ichida ekanini aytadi: Bash buyruqlari `cd <papka>`
bilan, Edit va Write mutlaq yo'l bilan. Asosiy daraxtga yozish guruh
izolyatsiyasini buzadi.

Guruhlar bir xabarda bir nechta Agent chaqiruvi bilan yurgiziladi: har
guruhning birinchi aktyori bir vaqtda.

## Birlashtirish va to'liq suite

Hamma guruh o'z zanjirini tugatgach:

```bash
python3 tools/guruh.py birlashtir orders     # patch indeksga, commit yo'q
python3 tools/guruh.py birlashtir billing
python3 tools/run_tests.py --hammasi --yurgiz   # fonda: Bash run_in_background
python3 tools/guruh.py tozala --hammasi
```

To'liq suite **partiyada bir marta** yuradi, guruh yoki aktyor
bo'yicha emas. U maqsadli tanlashning xavfsizlik to'ri: yiqilgan test
fayli qaysi guruhniki ekani `guruh.py royxat` dagi fayllardan topiladi
va kamchilik shu guruh egasiga qaytadi (budjetning ikkinchi chaqiruvi).

Kesishgan guruh asosiy daraxtga tegmaydi: `birlashtir` kesishgan
fayllarni aytadi. Ikki yo'l: `--3way` bilan qo'llab ziddiyatni egasi
asosiy daraxtda hal qiladi, yoki shu guruh boshqalaridan keyin ketma-ket
bajariladi. Kesishish reja xatosi: keyingi partiyada guruhlar fayl
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
