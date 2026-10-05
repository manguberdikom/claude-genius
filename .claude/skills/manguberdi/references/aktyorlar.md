# Aktyorlar zanjiri

Zanjir uzunligi vazifa hajmidan kelib chiqadi. Hammaga bir xil to'liq
zanjir (dasturchi, test muhandisi, review, keyin ikkalasi yana) bitta
guruhni 40-70 daqiqaga cho'zardi, holbuki kichik bugga u kerak emas.
Hajm `references/marshrut.md` dagi qoida bilan aniqlanadi.

| Hajm | Zanjir |
|---|---|
| S | `dasturchi` (o'zgarish va uning regressiya testi) -> `review` |
| M | `dasturchi` -> `test-muhandis` va `review` **parallel** -> bitta tuzatish aylanasi |
| L | `rejalashtiruvchi` -> har guruhga M zanjiri, guruhlar parallel (`references/parallel.md`) |

S da alohida `test-muhandis` chaqirilmaydi: bitta xatti-harakatning
regressiya testini o'zgarishni yozgan dasturchi yozadi. Topshiriqda
`hajm: S` yoziladi va `dasturchi` shu belgidan test yozishga ruxsatni
oladi. Qoplash so'ralgan bo'lsa yoki test ko'p darajali bo'lsa, bu S
emas.

M da `review` va `test-muhandis` bir xabarda ikki Agent chaqiruvi bilan
yuradi. Review faqat ishlab chiqarish kodini o'qiydi, test muhandisi esa
faqat test yozadi, shuning uchun ular bitta faylga yozmaydi va bir-birini
kutmaydi. Testlarning o'zi review siz qolmaydi: `check_code.py` ularni
mexanik tekshiradi, yiqilgani `run_tests.py` da chiqadi.

## Ikkinchi aylana: faqat haqiqiy kamchilikda

| Review topilmasi | Nima bo'ladi |
|---|---|
| `yuqori` (xato yoki xavf) | egasiga qaytadi, ikkinchi chaqiruv |
| `o'rta` | egasi baribir chaqirilayotgan bo'lsa shu chaqiruvga qo'shiladi, aks holda hisobotga |
| `past` (uslub) | faqat hisobotga |

Bitta `past` yoki `o'rta` uchun butun aylana (aktyor, test, qayta
review) ochilmaydi. Egasi ikkita bo'lsa (kod va test), ikkinchi
chaqiruvlar parallel yuradi: ular har xil faylga yozadi.

Ikkinchi chaqiruvdan keyin **review to'liq qayta yurmaydi**. Asosiy
sessiya tuzatilgan topilmalarni o'zi tekshiradi: aytilgan `fayl:qator`
ni o'qish, `check_code.py`, `run_tests.py --diff --yurgiz`. Review
ikkinchi marta faqat mexanik tekshirib bo'lmaydigan `yuqori` mantiq
topilmasi uchun chaqiriladi va promptida faqat o'sha topilmalar turadi.

## Testlar qachon va qanday

Har aktyor testni faqat asbob bilan yurgizadi:

```bash
python3 tools/run_tests.py --diff --yurgiz        # ish oxirida, bir marta
```

Asbob o'zgarishga ta'sir qilgan test sinflarini tanlaydi, modulni o'zi
qo'yadi, logni faylga yozadi va birinchi sababni beradi. Bash chaqiruvi
`timeout: 600000` bilan. Testni qayta yurgizish faqat kod o'zgargandan
keyin: o'zgarmagan kirishda Gradle test vazifasi `UP-TO-DATE` bo'ladi va
qayta yurish hech narsa bermaydi.

| Kim | Test |
|---|---|
| `dasturchi` | o'z ishining oxirida bir marta, maqsadli |
| `test-muhandis` | o'zi yozgan testlar va maqsadli tanlash, bir marta |
| `review` | yurgizmaydi: topshiriqdagi `run_tests` xulosasini o'qiydi |
| asosiy sessiya | partiya oxirida bir marta to'liq suite, fonda: `--hammasi` |

Xom `./gradlew test`, `mvn verify`, `clean`, `--rerun-tasks` va
`--no-daemon` ni `guard.py` to'sadi (`deny`) va shu asbobni ko'rsatadi.

Chiqish kodi zanjirni belgilaydi:

| Kod | Ma'nosi | Nima qilinadi |
|---|---|---|
| 0 | yashil | davom |
| 1 | yiqildi: qayta yurishda ham, kompilyatsiya, yoki test emas vazifa (coverage, lint) | egasiga qaytadi; `Boshqa yiqilish:` qatori shu vazifani aytadi |
| 3 | vaqt tugadi | to'liq suite bo'lsa fonda, aks holda tanlov juda keng: modul bo'yicha bo'lish |
| 4 | beqaror: yiqilgan sinf qayta yurishda o'tdi, boshqa yiqilish yo'q | kod tuzatilmaydi; `Beqaror:` qatori hisobotga, egasi `test-muhandis` |

Asbob yiqilgan sinflarni bir marta qayta yurgizadi (`--qayta`): flaky
test o'zgarishga yopishtirilib, dasturchi yo'q xatoni qidirmasin. Kod 4
yashil emas: o'zgargan kodga tegadigan beqaror test poyga xatosi bo'lishi
mumkin va partiya oxirida yana tekshiriladi.

Tanlov Spring orqali ta'sirni ham oladi: `@Configuration`, filter,
`@ControllerAdvice` kabi sinf o'zgarsa modulning barcha Spring testlari,
`@Entity` o'zgarsa baza testlari, abstrakt bazaviy sinfdagi
`@SpringBootTest` ham hisobga olinadi. Maqsadli yurishda jacoco o'chadi:
coverage chegarasi bir nechta test bilan yolg'on yiqilardi. Maven da
`-Djacoco.skip=true`, Gradle da init skript (`-I`, build fayliga
tegmaydi): agent, hisobot va coverage tekshiruvi o'chadi. Gradle da
kompilyatsiya natijasi lokal build cache ga tushadi, test natijasi
tushmaydi. Loyiha `org.gradle.caching` ni o'zi tanlagan bo'lsa uning
sozlamasi amal qiladi: `true` da o'zgarmagan test ham cache dan keladi.

Tezlik o'lchanadi, taxmin qilinmaydi: har yurish jurnalga tushadi,
`python3 tools/run_tests.py --hisobot` rejim bo'yicha soni va vaqtini,
kuniga to'liq suite sonini beradi. Build ga tegmaydigan qo'shimcha
bayroqlar (`--parallel --configuration-cache`, Maven da `-o -T 1C`) faqat
foydalanuvchi tanlasa: `GENIUS_TEST_FLAGS` muhit o'zgaruvchisi. Ularning
to'g'riligi build ning o'ziga bog'liq, shuning uchun standart bo'sh.

## Chaqiruv budjeti

Har aktyor bitta vazifada **ko'pi bilan ikki marta** chaqiriladi.
Birinchi chaqiruv ishni bajaradi, ikkinchisi topilmani tuzatadi.
Uchinchisi yo'q. Ikkinchi chaqiruv promptida `2-chaqiruv` deb yoziladi
va kamchilikni qaytargan aktyorning topilmalari fayl, qator va qoidasi
bilan to'liq ko'chiriladi.

Budjet tugaganda va muammo qolganda zanjir to'xtaydi. Shunda yoziladi:
nima bajarildi, nima qolgan, nega ikki urinish yetmadi, nima
yetishmayapti. Uchinchi urinish o'rniga aniq savol beriladi. Undan
keyin memory bosqichi bajariladi: ikki urinishda ham qolgan kamchilik
`feedback` nomzodi, yarim qolgan reja `project` nomzodi.

Budjet **sanaladi**, yodda saqlanmaydi: hook uni har yangi so'rovda
o'zi nolga tushiradi. Bitta so'rov ichida ikkinchi vazifa boshlansa:

```bash
python3 tools/budget.py --yangi-vazifa "<vazifa nomi>"
python3 tools/budget.py --holat          # jadval, guruhlar bilan
```

Parallel guruhda prompt `guruh: <id>` qatori bilan boshlanadi va hisob
guruh bo'yicha yuritiladi: ikki guruh bir-birining budjetini yemaydi.
Qatorsiz chaqiruv bitta umumiy hisobga tushadi.

`PreToolUse` hook har aktyor chaqiruvini hisoblaydi va uchinchisini
**to'sadi**. `qidiruv` va `tahlil` sanalmaydi: ular zanjir qadami emas,
o'qish asbobi.

Chaqiruv behuda ketgan bo'lsa (aktyor boshqa sababdan yiqildi yoki
foydalanuvchi to'xtatdi):
`python3 tools/budget.py --tiklash <aktyor> [--guruh <id>]`.

## Ikkinchi chaqiruvning oldini olish

| Sabab | Oldini olish |
|---|---|
| Aktyor qoidani bilmagan | `rules_for.py` ni ishdan oldin chaqirish |
| Reviewer boshqa mezon bilan tekshirgan | ikkalasi bir xil ro'yxatni oladi |
| "Bajarildi" nimaligi aytilmagan | qabul mezoni normalizatsiyada belgilanadi |
| Kontekst qayta qidirildi | guruh kartasi har promptga ko'chiriladi |

`rules_for.py` zanjirning birinchi qadami va u **majburlanadi**:
`check_code.py` Java fayl yozilgandan keyin (`PostToolUse`) shu fayl
uchun chaqiruv bo'lganini tekshiradi. Bo'lmasa modelga to'siq xabarini
qaytaradi. Shuning uchun `rules_for.py` yozishdan OLDIN chaqiriladi.

## Kamchilik kimga qaytadi

| Topilma turi | Egasi |
|---|---|
| Mantiq xatosi, pattern noto'g'ri qo'llangan, chegara buzilgan | `dasturchi` |
| Tranzaksiya, N+1, resurs yopilmagan, xato yutilgan | `dasturchi` |
| Test yo'q, assertion yo'q, test noto'g'ri turda, flaky | `test-muhandis` (S da `dasturchi`) |
| Reja qadami bajarilmagan yoki reja noto'g'ri | `rejalashtiruvchi` |
| Hujjat yoki havola buzilgan | `dasturchi` |

## Har aktyor nimani qaytaradi

Qaytarilgan javob keyingi aktyor uchun **kirish**, shuning uchun shakli
qat'iy: bir jumlada natija, har qaror yonida `<hujjat> <raqam>`, nima
bajarilmagani va nega, keyingi aktyor uchun aniq ma'lumot (fayl, qator,
buyruq) va `run_tests` natijasi. Javobda uzun log, to'liq fayl matni yoki
stack trace bo'lmaydi. Javob savol bilan tugamaydi: ochiq qaror
`Ochiq qaror:` qatorida standarti bilan beriladi (`references/marshrut.md`).

## Zanjir qachon qisqaradi

- Faqat savol berilgan bo'lsa (`doc.sh show`, `qidiruv`, `tahlil`),
  zanjir shu yerda tugaydi: kod o'zgarmaydi, review ishlamaydi.
- Faqat review so'ralgan bo'lsa, `dasturchi` va `test-muhandis`
  chaqirilmaydi: topilmalar hisobot sifatida beriladi.
- Hujjat o'zgarishi kod emas: `check_docs.py` tekshiradi, test
  muhandisi chaqirilmaydi.
- Bir necha modulli ish (to'liq review, keng tuzatish) ish boshida
  modullarga bo'linadi; fayllari kesishmasa ular parallel guruh.
