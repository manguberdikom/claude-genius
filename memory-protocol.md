# Memory protokoli: Claude nimani, qayerga va qanday saqlaydi

Bu fayl bitta ishni qiladi: memory bilan ishlaydigan har qanday MD uchun yagona
manba bo'ladi. Boshqa fayllar memory qoidalarini o'zida takrorlamaydi, shu faylga
havola qiladi. Takrorlangan qoida eskiradi, ikki joyda boshqacha bo'lib qoladi va
ziddiyat tug'diradi.

Hujjat uch savolga javob beradi:

1. **Marshrut** - qaysi bilim qaysi joyda yashaydi.
2. **Ketma-ketlik** - qanday tartibda o'qiladi, qanday tartibda yoziladi.
3. **Darvoza** - nima umuman yozilmaydi.

Uchinchisi eng muhim. Memory to'lib ketsa, o'qilmaydi: index chegaradan oshgan
qismi keyingi sessiyada umuman yuklanmaydi. Ya'ni ortiqcha yozuv faqat joy
egallamaydi, balki kerakli yozuvni sessiyadan **chiqarib tashlaydi**. Shu sababli
"yozmaslik" qarori bu hujjatda "yozish" qaroridan ko'proq joy oladi.

Tayanch holat: Claude Code memory mexanikasi, 2026-10. Versiyaga bog'liq
xususiyatlar yonida CLI versiyasi ko'rsatilgan. Mexanikaning o'zi (ikki tizim,
qatlamlar, yuklanish tartibi, audit) `memory-mexanika.md` da, bu fayl faqat
yozish qoidasini beradi.

## Mundarija

- [1. Nega bu fayl bor va u qanday ishlatiladi](#1-nega-bu-fayl-bor-va-u-qanday-ishlatiladi)
- [2. Marshrut: qaysi bilim qayerga boradi](#2-marshrut-qaysi-bilim-qayerga-boradi)
- [3. Darvoza: yozishdan oldingi yetti savol](#3-darvoza-yozishdan-oldingi-yetti-savol)
- [4. Saqlash ketma-ketligi](#4-saqlash-ketma-ketligi)
- [5. Yozuv formati va nomlash](#5-yozuv-formati-va-nomlash)
- [6. Hajm budjeti va qattiq chegaralar](#6-hajm-budjeti-va-qattiq-chegaralar)
- [7. Eskirish, ziddiyat va o'chirish](#7-eskirish-ziddiyat-va-ochirish)
- [8. Cloud va lokal sessiya farqi](#8-cloud-va-lokal-sessiya-farqi)
- [9. Memoryga yozilmaydigan narsalar](#9-memoryga-yozilmaydigan-narsalar)
- [10. Boshqa MD lar uchun ulanish bloki](#10-boshqa-md-lar-uchun-ulanish-bloki)
- [11. Git memory ombori: proyekt bo'yicha saqlash](#11-git-memory-ombori-proyekt-boyicha-saqlash)
- [12. Amalda qo'llash](#12-amalda-qollash)

---

## 1. Nega bu fayl bor va u qanday ishlatiladi

Har bir Claude sessiyasi bo'sh kontekst bilan boshlanadi. O'tgan sessiyada
aytilgan gap, kelishilgan qoida, topilgan tuzoq - hammasi sessiya tugashi bilan
yo'qoladi. Faqat **diskka yozilgani** qoladi. Memory aynan shu: sessiyalar
orasida bilimni olib o'tadigan fayllar to'plami.

Muammo shundaki, memoryni yozish arzon, o'qish esa qimmat. Har bir yozuv keyingi
har bir sessiyaning kontekstidan joy oladi. Shuning uchun memory "bo'sh joy"
emas, **budjet**. Bu hujjat o'sha budjetni boshqarish qoidasi.

### Bu faylni kim o'qiydi

| O'quvchi | Qachon o'qiydi | Nima oladi |
|---|---|---|
| Claude | memoryga yozish yoki uni tozalash kerak bo'lganda | darvoza, marshrut, format |
| Boshqa MD fayllar | o'zida memory haqida gap bo'lsa | havola, qoidaning nusxasi emas |
| Loyiha egasi | memory to'lib ketganda, yuklanmaganda yoki qoida ishlamaganda | to'lib ketsa: `Hajm budjeti va qattiq chegaralar` bo'limi; memory yuklanmasa yoki qoida ishlamasa: `memory-mexanika.md` |

### Qanday havola qilinadi

Bu fayl **`@` bilan import qilinmaydi**. `@memory-protocol.md` deb yozilsa, fayl
har sessiya boshida to'liq kontekstga yuklanadi va aynan o'zi ogohlantirayotgan
muammoni keltirib chiqaradi. To'g'ri yo'li: nomini teskari apostrof ichida
yozish, Claude kerak bo'lganda o'zi o'qiydi.

```markdown
Memoryga yozishdan oldin `memory-protocol.md` dagi darvozani qo'lla.
```

Teskari apostrof ichidagi `@path` import qilinmaydi, oddiy matn bo'lib qoladi.
Import tahlili kod bloklari va kod span larini o'tkazib yuboradi.

---

## 2. Marshrut: qaysi bilim qayerga boradi

Yozishdan oldin javob beriladigan birinchi savol "yozamanmi?" emas, **"qayerga?"**.
Noto'g'ri joyga yozilgan to'g'ri bilim ham zarar: har sessiyada yuklanadi, lekin
kerak bo'lgan paytda ishlamaydi.

| Bilim turi | Joyi | Nega aynan shu joy |
|---|---|---|
| Build, test, lint buyrug'i | loyiha `CLAUDE.md` | har sessiyada kerak, jamoa bilan bo'lishiladi |
| Nomlash va kod konvensiyasi | loyiha `CLAUDE.md` | qisqa, hamma faylga tegishli |
| Faqat ma'lum fayllarga tegishli qoida | `.claude/rules/<mavzu>.md` + `paths:` | faqat o'sha fayl ochilganda yuklanadi, kontekst tejaladi |
| Ko'p qadamli jarayon (deploy, release, hujjat yig'ish) | `.claude/skills/<nom>/SKILL.md` | faqat kerak bo'lganda yuklanadi |
| Katta bilim bazasi, qo'llanma, katalog | repodagi oddiy `.md` fayl | hech qachon avtomatik yuklanmaydi, teskari apostrofda havola qilinadi |
| Sessiyalar va mashinalar orasida saqlanishi kerak bilim | git memory ombori: faqat shu proyektga tegishlisi `memory/<proyekt-slug>/`, har proyektda bir xil amal qiladigani `memory/umumiy/` | auto memory mashinadan chiqmaydi, git chiqadi; bitta gap ikki darajada turmaydi, ikkinchi proyektga kerak bo'lsa nusxa emas, `umumiy/` ga ko'chiriladi |
| Foydalanuvchi afzalligi va roli, barcha loyihalarda amal qiladigan uslub | `memory/umumiy/user_<mavzu>.md` | git orqali hamma mashina va proyektga yetadi; `~/.claude/CLAUDE.md` ni o'rnatuvchi tozalaydi |
| Berilgan tuzatish, tasdiqlangan yondashuv | `memory/<proyekt-slug>/feedback_<mavzu>.md`, hamma proyektga tegishli bo'lsa `memory/umumiy/` | `rules_for.py` feedback ni faqat `memory/` ostidan o'qiydi |
| Davom etayotgan ish holati, qaror, muddat | `memory/<proyekt-slug>/project_<mavzu>.md` | kodidan chiqarib bo'lmaydi |
| Tashqi manba manzili | `memory/<proyekt-slug>/reference_<mavzu>.md` | |
| Shaxsiy, commit qilinmaydigan sozlama | `./CLAUDE.local.md` + `.gitignore` | jamoaga tegishli emas |
| Majburiy bajarilishi yoki bloklanishi shart | hook (`PreToolUse`, `PostToolUse`) | memory kafolat bermaydi, hook beradi |
| Sir, token, parol, maxfiy manzil | hech qayerga | joyi aytiladi, qiymati emas |
| Bir martalik vazifa tafsiloti | hech qayerga | sessiya bilan tugaydi |

Auto memory faqat zaxira: ombor ulanmagan sessiyada ishlatiladi, ombor
ulanganda yozuv `memory/` ga ko'chiriladi.

### Ikki chalkash holat

**"Qoida, lekin faqat test fayllariga tegishli"** - bu `CLAUDE.md` emas,
`paths:` bilan rules. Root faylga yozilsa, har sessiyada yuklanadi va 90%
hollarda keraksiz turadi.

```markdown
---
paths:
  - "src/test/**/*.java"
---

- Har bir test nomi `metod_holat_natija` ko'rinishida yoziladi.
- Testcontainers konteyneri sinf darajasida qayta ishlatiladi.
```

**"Jarayon, lekin qisqa"** - uzunligi emas, chaqirilish chastotasi qaror qiladi.
Har sessiyada kerak bo'lmaydigan ketma-ketlik skill'ga boradi, hatto uch qatorli
bo'lsa ham.

---

## 3. Darvoza: yozishdan oldingi yetti savol

Har bir nomzod yozuv shu yetti savoldan o'tadi. **Bittasida to'xtasa, yozilmaydi.**
Tartib muhim: arzon savol oldinda, shunda ko'p nomzod birinchi uch savolda
to'xtaydi.

| № | Savol | To'xtash sharti |
|---|---|---|
| 1 | Keyingi sessiyada bu foyda beradimi? | Faqat hozirgi vazifaga kerak bo'lsa, to'xta |
| 2 | Kodidan, fayl yo'lidan yoki git tarixidan chiqarib olish mumkinmi? | Mumkin bo'lsa, to'xta |
| 3 | CLAUDE.md yoki mavjud yozuv buni allaqachon aytganmi? | Aytgan bo'lsa, to'xta yoki **borini yangila** |
| 4 | Bu qaytalanadigan qoidami yoki bir martalik holatmi? | Bir martalik bo'lsa, to'xta |
| 5 | Gap tekshirib bo'ladigan darajada aniqmi? | "Yaxshi kod yoz" kabi mavhum bo'lsa, to'xta |
| 6 | Bir hafta ichida eskiradimi? | Eskiradigan bo'lsa, sana bilan yoz yoki to'xta |
| 7 | Ichida sir, token yoki shaxsiy ma'lumot bormi? | Bor bo'lsa, to'xta: faqat joyini ko'rsat |

### Nomzod qanday paydo bo'ladi

Yozuv uchun nomzod uchta signaldan biri bilan paydo bo'ladi:

1. **Foydalanuvchi tuzatdi.** Aytilgan gapni Claude ikkinchi marta so'ramasligi
   kerak. Eng qimmatli nomzod turi.
2. **Xato ikkinchi marta takrorlandi.** Birinchi marta tasodif, ikkinchi marta
   qoidaning yo'qligi.
3. **Kodidan topilmaydigan kontekst oshkor bo'ldi.** Nega shunday qilingani,
   kim qaror qilgani, qachon qayta ko'riladi.

Signal bo'lmasa, nomzod ham yo'q. "Foydali bo'lishi mumkin" - signal emas.

### Misollar

| Nomzod | Qaror | Nega |
|---|---|---|
| "Foydalanuvchi o'zbek lotin yozuvida javob kutadi, kirill mutlaqo bo'lmasin" | yoziladi, `type: user` | aniq, qaytalanadi, kodidan chiqmaydi |
| "Loyihada `src/main/java` papkasi bor" | yozilmaydi | `ls` bilan ko'rinadi |
| "Bugun 14-bobni yozdik" | yozilmaydi | bir martalik, git tarixida bor |
| "Hujjat 39 bobga rejalashtirilgan, 6-39 qolgan" | yoziladi, `type: project` | davom etayotgan ishning holati |
| "Agentlar lotin so'z ichiga kirill harf qo'yib yuboradi, yig'ishdan oldin tozalash kerak" | yoziladi, `type: feedback` | takrorlanadigan tuzoq, kodidan bilinmaydi |
| "Python 3.9 da f-string ichida bir xil qo'shtirnoq ishlamaydi" | muhitga bog'liq bo'lsa yoziladi, aks holda yozilmaydi | umumiy til bilimi memoryga tegishli emas |
| "API kaliti `sk-...`" | yozilmaydi | sir. O'rniga: "kalit `.env` da, `API_KEY` nomi bilan" |
| "Kod toza bo'lsin" | yozilmaydi | tekshirib bo'lmaydi |

---

## 4. Saqlash ketma-ketligi

Bu bo'lim hujjatning o'zagi. Ketma-ketlik olti fazadan iborat va faza tartibi
buzilmaydi. Eng ko'p uchraydigan xato: **4-fazani 2-fazadan oldin
bajarish**, ya'ni o'qimasdan yozish. Natijada memoryda bir xil gapning uch
xil ko'rinishi paydo bo'ladi.

### A faza. Sessiya boshi: o'qish

1. **Avtomatik yuklanganini bil.** Boshqariladigan siyosat, foydalanuvchi va
   loyiha `CLAUDE.md`, `CLAUDE.local.md`, `paths` siz rules, auto memory index.
   Bularni qayta o'qish shart emas, allaqachon kontekstda.
2. **Tekshir:** `/context` buyrug'i **Memory files** ro'yxatini ko'rsatadi.
   Fayl o'sha ro'yxatda bo'lmasa, Claude uni ko'rmaydi. Hech qanday boshqa
   tushuntirish kerak emas.
3. **Indexdan yo'l top.** `MEMORY.md` - papkaning indeksi, har yozuv bir qator.
   Vazifaga tegishli topic faylni aniqla.
4. **Faqat kerakligini o'qi.** Topic fayllar avtomatik yuklanmaydi. Hammasini
   o'qish - kontekstni behuda yoqish. Vazifaga tegishlisini o'qi, qolganini yo'q.
5. **Repo hujjatini faqat talab bo'lsa o'qi.** Katta qo'llanmalar (masalan shu
   repodagi `docs/` hujjatlari) hech qachon avtomatik yuklanmaydi va shunday
   qolishi kerak.

### B faza. Ish davomida: nomzod to'plash

6. **Signalni belgila.** Tuzatish keldi, xato takrorlandi yoki kodidan
   chiqmaydigan kontekst oshkor bo'ldi. Signalni o'sha paytda qayd et, sessiya
   oxirida eslab qolishga ishonma.
7. **Darhol yozma.** Nomzodni to'plab tur. Bitta sessiyada bir xil mavzuga uch
   marta yozish - uchta chalkash yozuv degani. Istisno: foydalanuvchi "buni
   eslab qol" deb aniq aytgan bo'lsa, darhol yoziladi.

### C faza. Yozishdan oldin: filtr

8. **Darvozadan o'tkaz.** `Darvoza` bo'limidagi yetti savol. To'xtagan nomzod tashlanadi,
   "ehtimol keyin kerak bo'ladi" degan zaxiraga olinmaydi.
9. **Marshrutni tanla.** `Marshrut` bo'limidagi jadval. Joy noto'g'ri bo'lsa, qolgan
   hamma qadam behuda.

### D faza. Yozish

10. **Avval qidir, keyin yoz.** Indexda va topic fayllarda shu mavzu bormi?
    Bor bo'lsa - **yangilanadi**, yangi yozuv qo'shilmaydi. Memory jurnal emas,
    hozirgi holatning tasviri. Eski va yangi gap birga turmaydi.
11. **Ikki darajada yoz.** Indexga bir qator, tafsilot topic faylga. Index
    "nima qayerda" degan savolga javob beradi, mazmunni o'zida saqlamaydi.
12. **Ziddiyatni tekshir.** Yangi yozuv boshqa qatlamdagi gapga qarshi
    chiqmaydimi? Chiqsa, ikkisidan biri o'chiriladi. Ikkitasini qoldirib
    "Claude to'g'risini tanlaydi" deb o'ylash - xato.

### E faza. Yozgandan keyin

13. **Hajmni tekshir.** Index 200 qator yoki 25KB ga yaqinlashsa, qisqartirish
    buyrug'i keladi: bir yozuv bir qator, tafsilot topic faylga, eskisi
    birlashtiriladi yoki o'chiriladi. Chegaradan oshsa, yozish o'tadi, lekin
    keyingi yuklanishda oshgan qismi **tushib qoladi**.
14. **Natijani tasdiqla.** Claude memoryga yozganda yoki undan o'qiganda
    interfeysda "Saved N memories" yoki "Recalled N memories" chiqadi. Bu
    signal, dalil emas: yozuv haqiqatan tushganini `/memory` bilan papkani
    ochib ko'rish tasdiqlaydi. Yozuv git memory omboriga tushgan bo'lsa,
    tasdiq commit va push: `Git memory ombori` bo'limidagi qo'shimcha qadam.

### F faza. Vaqti-vaqti bilan: tozalash

15. **Eskirganini o'chir.** Tugagan ish, bekor qilingan qaror, o'zgargan
    afzallik. O'chirish ham memory ishining bir qismi, qo'shimcha emas.
16. **Audit qil.** `/memory` papkani ochadi, `/doctor prompt-audit` ziddiyatli va
    eskirgan ko'rsatmalarni topadi (CLI v2.1.283+). Qolgan vositalar
    `memory-mexanika.md` dagi `Tekshirish va audit` bo'limida.

### Qisqa karta

```text
O'QISH:  /context -> index -> faqat kerakli topic fayl
NOMZOD:  signal bor? (tuzatish | ikkinchi xato | yashirin kontekst)
DARVOZA: 7 savol -> bittasi "yo'q" bo'lsa, tashlanadi
MARSHRUT: CLAUDE.md | rules+paths | skill | memory/ ombori | repo doc | hook | hech qayerga
YOZISH:  qidir -> yangila (qo'shma) -> index bir qator + topic tafsilot
KEYIN:   hajm -> ziddiyat -> eskirganini o'chir
```

---

## 5. Yozuv formati va nomlash

Format erkin bo'lsa, memory bir yildan keyin o'qib bo'lmaydigan holga keladi.
Shuning uchun yozuvning shakli qat'iy.

### Index: `MEMORY.md`

Index papkadagi nima qayerda turganini ko'rsatadi. Bitta yozuv - bitta qator.
Qator mazmunni **tasvirlaydi**, o'zida saqlamaydi.

```markdown
# Memory

- `user_til.md` - javob tili va yozuv uslubi talablari
- `feedback_hujjat_formati.md` - hujjat yig'ishdagi format qoidalari va tuzoqlar
- `project_handbook_holati.md` - handbook'larning hozirgi holati
- `reference_manbalar.md` - tashqi hujjat va manzillar
```

Index'da nima bo'lmaydi: kod bloki, uzun izoh, jadval, tugagan ishning tarixi.

### Topic fayl

Har bir topic fayl bitta mavzuni oladi. Frontmatter bilan boshlanadi:

```markdown
---
type: feedback
modified: 2026-10-04T12:00:00Z
---

# Hujjat yig'ish qoidalari

- Yig'ishdan oldin kirill harflarni tozalash skripti ishlatiladi: agentlar lotin
  so'z ichiga kirill harf qo'yib yuboradi.
- Sarlavhalarni filtrlashda kod bloki ichidagi `#` qatorlariga tegilmaydi.
```

Qoidalar:

- `type` to'rtta qiymatdan biri: `user`, `feedback`, `project`, `reference`.
- `modified` maydonini qo'lda yozish shart emas: frontmatter bo'lgan faylga
  Claude Code yozuv vaqtini ISO 8601 formatida o'zi qo'yadi (CLI v2.1.214+).
  Frontmatter yo'q faylga u qo'shilmaydi.
- Fayl nomi: `<type>_<mavzu>.md`, kichik harf, ostki chiziq bilan. Shunda
  papkaning o'zi tur bo'yicha saralanadi.
- Bir fayl bir mavzu. Ikki mavzu bitta faylga tiqilsa, biri hech qachon
  topilmaydi.

### Yozuvning tili

Yozuv **tekshirib bo'ladigan** gap bo'lishi kerak:

| Yomon | Yaxshi |
|---|---|
| "Hujjatlar sifatli bo'lsin" | "Har bob oxirida `## N.M Amalda qo'llash` bo'limi bo'ladi" |
| "Testlarni unutmang" | "Commit'dan oldin `mvn verify` ishlatiladi" |
| "Foydalanuvchi aniqlikni yaxshi ko'radi" | "Javob birinchi qatorida natija turadi, keyin tafsilot" |

---

## 6. Hajm budjeti va qattiq chegaralar

Chegaralar taxminiy emas, aniq raqamlar. Ularni bilmaslik memoryning jim
yo'qolishiga olib keladi.

| Narsa | Chegara | Oshsa nima bo'ladi |
|---|---|---|
| Auto memory index (`MEMORY.md`) | 200 qator yoki 25KB, qaysi biri avval kelsa | Oshgan qism keyingi sessiyada **umuman yuklanmaydi**. Yozuv o'tadi, lekin index'ni qayta yozish talab qilinadi |
| Bitta `CLAUDE.md` | tavsiya: 200 qatordan kam | Uzun fayl ko'proq kontekst yeydi va qoidaga rioya qilish pasayadi. Startda ogohlantirish chiqadi |
| `CLAUDE.md` qattiq cheklovi | 4 MiB | Fayl **butunlay o'tkazib yuboriladi** |
| `@path` import chuqurligi | 4 qadam | Undan keyingi import ishlamaydi |
| `paths:` brace expansion | bitta rules fayl uchun 1000 pattern va 4 MiB | Budjetdan oshgan pattern ochilmagan holda ishlatiladi va hech qanday faylga mos kelmaydi |

### Budjetni qanday ushlab turish

1. Index'da bir yozuv bir qator. Tafsilot doim topic faylda.
2. `CLAUDE.md` da faqat har sessiyada kerak bo'ladigan narsa. Qolgani
   `paths:` bilan rules'ga yoki skill'ga.
3. `@path` import tartib uchun, tejash uchun emas. Fayl import qilinsa, kontekst
   xarajati o'zgarmaydi.
4. Tozalash kechiktirilmaydi. "Keyin qisqartiramiz" degan index chegaraga
   yetganda eng yangi yozuvni yo'qotadi.
5. Uzun arxiv memoryda emas, repodagi oddiy hujjatda yashaydi.

---

## 7. Eskirish, ziddiyat va o'chirish

Memoryning eng katta xavfi to'lib ketish emas, **noto'g'ri bo'lib qolish**.
Eskirgan yozuv Claude'ni ishonch bilan xato yo'lga boshlaydi, chunki u yozuvni
hozirgi haqiqat deb o'qiydi.

### Eskirish turlari

| Tur | Belgisi | Qaror |
|---|---|---|
| Tugagan ish | `project` yozuvdagi vazifa bajarilgan | o'chiriladi |
| O'zgargan qaror | yangi qaror eskisiga qarshi | eskisi o'chiriladi, yangisi yoziladi |
| O'zgargan afzallik | foydalanuvchi boshqacha so'radi | yangilanadi, ikkisi birga qolmaydi |
| Yo'qolgan havola | ko'rsatilgan fayl yoki buyruq mavjud emas | o'chiriladi |
| Versiyaga bog'liq gap | mexanika yangi CLI versiyada o'zgargan | versiya raqami bilan yoziladi yoki yangilanadi |

`modified` sanasi shu yerda ishlaydi: yozuv qachon yozilganini ko'rsatadi, ya'ni
"bu gap qanchalik yangi" savoliga javob beradi.

### Ziddiyat

Ikki qatlam qarama-qarshi gap aytsa, Claude ulardan birini tanlaydi va qaysi
birini tanlashi kafolatlanmagan. Foydalanuvchi rules va loyiha rules ham
bir-birini bekor qilmaydi.

Shuning uchun ziddiyat "ustuvorlik bilan hal qilinadi" degan fikr xato. U
**yo'qotiladi**: bittasi o'chiriladi yoki ikkisi bitta aniq gapga birlashtiriladi.

### O'chirish qoidasi

- O'chirish yo'qotish emas, tozalash. Git tarixi va suhbat tarixi bor.
- Shubha bo'lsa: yozuv **hozir** to'g'rimi? Javob "bilmayman" bo'lsa, o'chiriladi.
  Noto'g'ri yozuvning zarari yo'q yozuvdan katta.
- Auto memory fayllari `cleanupPeriodDays` tozalashiga tushmaydi: ular odam yoki
  Claude o'chirmaguncha turadi. Ya'ni o'z-o'zidan yo'qolishiga ishonib bo'lmaydi.

---

## 8. Cloud va lokal sessiya farqi

Bu bo'lim shu repo uchun eng amaliy bo'limi, chunki ish cloud sessiyalarda
ketmoqda.

| | Lokal sessiya | Cloud sessiya (claude.ai/code) |
|---|---|---|
| Konteyner | mashinada, saqlanadi | vaqtinchalik, faoliyatsizlikdan keyin qaytarib olinadi |
| Repo | mavjud nusxa | sessiya boshida yangi clone qilinadi |
| Auto memory | `~/.claude/projects/<project>/memory/` da turadi | mashinalar va cloud muhitlari orasida **bo'lishilmaydi** |
| Auto memory holati | lokalda default yoqilgan | self-hosted muhitda default o'chirilgan |
| Nima saqlanadi | memory papkasi va repo | faqat **commit qilib push qilingan** fayl |

Xulosa bitta: **cloud sessiyada bilim repoga yozilmasa, yo'qoladi.** Konteyner
qaytarib olinadi, auto memory papkasi u bilan ketadi.

Shuning uchun cloud ish uslubida marshrut o'zgaradi:

1. Proyektning o'z qoidasi: `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`.
   O'sha proyekt repositoriyasida turadi va commit qilinadi.
2. Sessiyalar orasida saqlanishi kerak bilim va ishning yarim qolgan holati:
   git memory ombori, `memory/<proyekt-slug>/`. Eski `HANDOFF.md` shu vazifani
   qo'lda bajargan. `Git memory ombori` bo'limi shu haqda.
3. Faqat bitta sessiyaga tegishli narsa: scratchpad, hech qayerga saqlanmaydi.

Subagent uchun ham shu mantiq: asosiy suhbatning auto memory'si subagent'ga
yuklanmaydi (fork'dan tashqari). Ya'ni ishni agentga topshirganda kerakli
kontekst **prompt ichida** beriladi, "memoryda bor" deb o'ylab bo'lmaydi.

---

## 9. Memoryga yozilmaydigan narsalar

Darvozadan o'tmaydigan narsalarning aniq ro'yxati. Bu bo'lim "ortiqcha narsa
saqlanmasin" talabining to'g'ridan-to'g'ri javobi.

| Yozilmaydi | Nega | O'rniga |
|---|---|---|
| Papka tuzilishi, fayl yo'llari ro'yxati | `ls` bilan ko'rinadi | hech narsa |
| Dependency ro'yxati, versiyalar | `pom.xml`, `package.json` da bor | hech narsa |
| Arxitektura umumiy tavsifi | kodidan o'qiladi | faqat kodidan bilinmaydigan **nega** |
| Bugungi ish tarixi, bajarilgan qadamlar | git tarixi va suhbatda bor | faqat tugallanmagan ishning holati |
| Bitta xatoni tuzatish tafsiloti | qaytalanmaydi | agar tuzoq takrorlanadigan bo'lsa, qoida sifatida |
| Umumiy til yoki framework bilimi | Claude biladi | faqat shu loyihadagi g'ayrioddiy holat |
| Sir, token, parol, maxfiy URL | xavfsizlik. Memory fayli oddiy matn | "kalit `.env` da, `X` nomi bilan" |
| Shaxsiy ma'lumot (email, telefon) | kerak emas | hech narsa |
| Mavhum maslahat ("toza kod yoz") | tekshirib bo'lmaydi, rioyaga ta'sir qilmaydi | aniq, o'lchanadigan qoida |
| Bir martalik vazifa tafsiloti | sessiya bilan tugaydi | hech narsa |
| CLAUDE.md allaqachon aytgan gap | takror. Ziddiyat manbai | borini aniqlashtirish |
| Uzun kod bloki yoki to'liq fayl mazmuni | kontekstni yoqadi | fayl yo'li va bir qatorli izoh |
| "Keyin kerak bo'lishi mumkin" degan zaxira | signal yo'q | hech narsa |

Qo'shimcha qoida: **bir xil gapning ikkinchi nusxasi** ham ortiqcha narsa.
Memoryda bir mavzu bitta joyda yashaydi.

---

## 10. Boshqa MD lar uchun ulanish bloki

Memory bilan ishlaydigan har qanday fayl quyidagi blokni qo'yadi va memory
qoidalarini o'zida takrorlamaydi. Blok qisqa, chunki uning vazifasi qoidani
aytish emas, manbani ko'rsatish.

```markdown
## Memory

Bu faylda memory qoidalari takrorlanmaydi. Yozishdan oldin `memory-protocol.md`:

- darvoza (yetti savol) - nimani yozmaslik kerak
- marshrut jadvali - qaysi joyga yozish kerak
- ketma-ketlik - qanday tartibda o'qish va yozish
```

Loyiha `CLAUDE.md` uchun esa bitta qator yetarli:

```markdown
Memoryga yozish yoki uni tozalash kerak bo'lganda `memory-protocol.md` o'qiladi.
```

Nega shunday: `CLAUDE.md` har sessiyada yuklanadi, shuning uchun unda protokolning
o'zi emas, faqat manzili turadi. Protokol esa faqat memory bilan ishlash paytida
o'qiladi.

---

## 11. Git memory ombori: proyekt bo'yicha saqlash

Auto memory bitta mashinada yashaydi va cloud konteyneri bilan ketadi. Shu repo
o'sha bo'shliqni to'ldiradi: `memory/` papkasi filtrdan o'tgan bilimni git'da,
proyekt bo'yicha saqlaydi.

### Vazifa taqsimoti

| Qism | Roli |
|---|---|
| Protokol (shu fayl) | filtr: nima saqlanadi, qaysi joyga, qanday tartibda |
| `memory/` papkasi | ombor: filtrdan o'tgan bilim git'da yig'iladi |
| Auto memory | bitta mashinadagi tezkor qatlam, uzoq muddatli manba emas |

Ikki daraja (`umumiy/` va proyekt papkasi) `Marshrut` bo'limidagi jadvalda.
Papka nomi, ulanish bloki va proyektlar ro'yxati `memory/README.md` da. Bu
bo'lim faqat qarorga tegishli qismni beradi.

### Omborga qo'shilgan ketma-ketlik

`Saqlash ketma-ketligi` bo'limidagi umumiy ketma-ketlik o'zgarmaydi, uning
ustiga ikki qadam qo'shiladi:

- **O'qishdan oldin:** `git pull`. Eski clone eskirgan bilim beradi, bu
  yozuvning umuman yo'qligidan xavfliroq.
- **Yozgandan keyin:** commit va push. Push qilinmagan yozuv saqlanmagan
  hisoblanadi, chunki cloud konteyneri qaytarib olinadi.

---

## 12. Amalda qo'llash

- [ ] Loyiha `CLAUDE.md` da shu faylga bir qatorli havola bor, `@` import yo'q
- [ ] `/context` ishlatib yuklanadigan memory fayllar ro'yxati bir marta ko'rilgan
- [ ] `MEMORY.md` index'da har yozuv bitta qator, tafsilot topic fayllarda
- [ ] Topic fayllar `<type>_<mavzu>.md` ko'rinishida nomlangan va frontmatter'da
      `type` bor
- [ ] Index 200 qator va 25KB chegarasidan uzoq
- [ ] Har bir `CLAUDE.md` 200 qatordan qisqa
- [ ] Faqat ma'lum fayllarga tegishli qoidalar `paths:` bilan rules'ga chiqarilgan
- [ ] Ko'p qadamli jarayonlar skill'ga chiqarilgan, `CLAUDE.md` da emas
- [ ] Majburiy shartlar hook'da, memoryda emas
- [ ] Memoryda sir, token, parol yoki shaxsiy ma'lumot yo'q
- [ ] Qatlamlar orasida qarama-qarshi ko'rsatma yo'q
- [ ] Tugagan ish va bekor qilingan qarorlar o'chirilgan
- [ ] Cloud sessiyada saqlanishi kerak bilim repoga commit qilingan
- [ ] Memory haqida gap boradigan boshqa MD lar qoidani nusxalamaydi, havola qiladi
- [ ] Oxirgi auditdan keyin `/doctor prompt-audit` bir marta ishlatilgan
- [ ] Omborga yozishdan oldin `git pull`, yozgandan keyin commit va push qilingan
- [ ] Umumiy bilim `memory/umumiy/` da, proyekt bilimi proyekt papkasida, nusxa yo'q
- [ ] Yangi proyekt papkasi nomi `memory/README.md` dagi slug qoidasiga mos
- [ ] Proyekt `CLAUDE.md` idagi memory bloki qisqa: manzil bor, qoida nusxasi yo'q
