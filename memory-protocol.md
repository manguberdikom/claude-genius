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
xususiyatlar yonida CLI versiyasi ko'rsatilgan.

## Mundarija

- [1. Nega bu fayl bor va u qanday ishlatiladi](#1-nega-bu-fayl-bor-va-u-qanday-ishlatiladi)
- [2. Ikki tizim: CLAUDE.md va auto memory](#2-ikki-tizim-claudemd-va-auto-memory)
- [3. Qatlamlar va yuklanish tartibi](#3-qatlamlar-va-yuklanish-tartibi)
- [4. Marshrut: qaysi bilim qayerga boradi](#4-marshrut-qaysi-bilim-qayerga-boradi)
- [5. Darvoza: yozishdan oldingi yetti savol](#5-darvoza-yozishdan-oldingi-yetti-savol)
- [6. Saqlash ketma-ketligi](#6-saqlash-ketma-ketligi)
- [7. Yozuv formati va nomlash](#7-yozuv-formati-va-nomlash)
- [8. Hajm budjeti va qattiq chegaralar](#8-hajm-budjeti-va-qattiq-chegaralar)
- [9. Eskirish, ziddiyat va o'chirish](#9-eskirish-ziddiyat-va-ochirish)
- [10. Cloud va lokal sessiya farqi](#10-cloud-va-lokal-sessiya-farqi)
- [11. Kelajakda inobatga olinadigan narsalar](#11-kelajakda-inobatga-olinadigan-narsalar)
- [12. Memoryga yozilmaydigan narsalar](#12-memoryga-yozilmaydigan-narsalar)
- [13. Tekshirish va audit](#13-tekshirish-va-audit)
- [14. Boshqa MD lar uchun ulanish bloki](#14-boshqa-md-lar-uchun-ulanish-bloki)
- [15. Amalda qo'llash](#15-amalda-qollash)

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
| Loyiha egasi | memory to'lib ketganda yoki qoida ishlamaganda | audit va chegaralar bo'limi |

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

## 2. Ikki tizim: CLAUDE.md va auto memory

Memory bitta narsa emas, ikkita mustaqil tizim. Ikkalasi ham har sessiya boshida
yuklanadi, lekin boshqa maqsad uchun xizmat qiladi. Ularni aralashtirib yuborish
eng ko'p uchraydigan xato.

| | CLAUDE.md fayllar | Auto memory |
|---|---|---|
| Kim yozadi | odam | Claude o'zi |
| Nima turadi | ko'rsatma va qoida | o'rganilgan narsa va afzallik |
| Qamrov | loyiha, foydalanuvchi, tashkilot | bitta repo, barcha worktree uchun umumiy |
| Yuklanish | har sessiyada to'liq | har sessiyada index ning birinchi 200 qatori yoki 25KB |
| Nimaga mos | build buyruqlari, konvensiya, arxitektura, "har doim X" | foydalanuvchi afzalligi, tuzatishlar, kod'dan chiqarib bo'lmaydigan kontekst |
| Qayerda yashaydi | repo va `~/.claude/` | `~/.claude/projects/<project>/memory/` |
| Git | commit qilinadi (local variantidan tashqari) | commit qilinmaydi, mashinaga bog'langan |

Uchinchi mexanizm ham bor va u memory emas: **hook**. CLAUDE.md va auto memory
kontekst, ya'ni ta'sir qiladi lekin kafolat bermaydi. Bir ish **albatta**
bajarilishi yoki bloklanishi kerak bo'lsa, u memoryga emas, `PreToolUse` hook'iga
yoziladi. "Claude qoidani bajarmadi" degan shikoyatning yarmi shu chalkashlikdan
kelib chiqadi: majburiy shart kontekstga yozilgan.

### Auto memory nimani o'zi yozadi

Claude o'zi yozadigan yozuvlar to'rt turga bo'linadi. Tur `type` maydonida,
fayl frontmatter'ida turadi:

| `type` | Mazmuni | Misol |
|---|---|---|
| `user` | roli, tajribasi, ish uslubi | "O'zbek lotin yozuvida javob kutadi" |
| `feedback` | tuzatishlar va tasdiqlangan yondashuv | "Em-dash ishlatmaslik so'raldi" |
| `project` | davom etayotgan ish, qaror, muddat | "Mindset hujjati 39 bobga rejalashtirilgan" |
| `reference` | loyihadan tashqaridagi manba | "Issue tracker manzili" |

Claude kodidan, fayl yo'llaridan yoki git tarixidan chiqarib olinadigan narsani
yozmaydi. CLAUDE.md allaqachon aytgan narsani ham yozmaydi. Har sessiyada biror
narsa yozilishi shart emas: yozuv faqat kelajakdagi suhbatga foyda bersa paydo
bo'ladi.

---

## 3. Qatlamlar va yuklanish tartibi

Qatlamlar bir-birini **bekor qilmaydi**, ketma-ket ulanadi. Bu muhim: pastdagi
qatlam yuqoridagini o'chirmaydi, shuning uchun ikki qatlamda qarama-qarshi qoida
bo'lsa, Claude ulardan birini tasodifiy tanlashi mumkin. Yechim ustuvorlikni
o'rganish emas, **ziddiyatni yo'qotish**.

### CLAUDE.md qatlamlari, yuklanish tartibida

| Qatlam | Joy | Kim ko'radi |
|---|---|---|
| Boshqariladigan siyosat | Linux/WSL: `/etc/claude-code/CLAUDE.md`, macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`, Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | mashinadagi barcha foydalanuvchi |
| Foydalanuvchi | `~/.claude/CLAUDE.md` | faqat o'zi, barcha loyihada |
| Loyiha | `./CLAUDE.md` yoki `./.claude/CLAUDE.md` | jamoa, git orqali |
| Lokal | `./CLAUDE.local.md` | faqat o'zi, shu loyihada (`.gitignore` ga qo'shiladi) |

Daraxt bo'yicha tartib: fayl tizimi ildizidan ish papkasiga qarab. Ya'ni
`foo/CLAUDE.md` kontekstda `foo/bar/CLAUDE.md` dan oldin turadi, ish papkasiga
yaqin ko'rsatma **oxirgi** o'qiladi. Har bir papka ichida `CLAUDE.local.md`
`CLAUDE.md` dan keyin qo'shiladi.

Ish papkasi ostidagi papkalardagi `CLAUDE.md` sessiya boshida yuklanmaydi,
Claude o'sha papkadagi faylni o'qiganda qo'shiladi.

### Qolgan yuklanadigan narsalar

| Narsa | Joy | Qachon yuklanadi |
|---|---|---|
| Umumiy rules | `.claude/rules/*.md` (`paths` siz) | har sessiyada, `.claude/CLAUDE.md` bilan teng ustuvorlikda |
| Yo'lga bog'langan rules | `.claude/rules/*.md` (`paths:` bilan) | mos faylda Read, Write yoki Edit ishlatilganda |
| Foydalanuvchi rules | `~/.claude/rules/*.md` | har sessiyada, loyiha rules'idan oldin |
| Auto memory index | `~/.claude/projects/<project>/memory/MEMORY.md` | har sessiyada, birinchi 200 qator yoki 25KB |
| Auto memory topic fayllar | o'sha papkadagi `*.md` | yuklanmaydi, Claude kerak bo'lganda o'qiydi |
| Skill | `.claude/skills/<nom>/SKILL.md` | chaqirilganda yoki vazifaga mos kelganda |

`AGENTS.md` ham o'qilishi mumkin: ish papkasida va undan yuqorida hech qanday
`CLAUDE.md`, `.claude/CLAUDE.md` yoki `CLAUDE.local.md` bo'lmasa (CLI v2.1.277+).
Tuzoq: shaxsiy `CLAUDE.local.md` qo'shilishi `AGENTS.md` ning o'qilishini
to'xtatadi. Ikkalasini ham o'qitish kerak bo'lsa, `/config` dagi **Project
instructions** ni `claude-md-and-agents-md` ga qo'yiladi.

### Nimani esda tutish kerak

- Qatlam qo'shilganda kontekst o'sadi, hech narsa ozaymaydi.
- `@path` import tashkil qilishga yordam beradi, kontekstni **tejamaydi**:
  import qilingan fayl ham sessiya boshida yuklanadi. Maksimal chuqurlik: 4 qadam.
- Loyiha memory faylidagi import ish papkasidan tashqariga chiqsa, Claude Code
  bir marta tasdiq so'raydi. Rad etilsa, import o'chib qoladi va dialog
  qaytarilmaydi.
- Blok darajasidagi HTML izoh (`<!-- ... -->`) kontekstga kirmaydi, o'chiriladi.
  Odam uchun izohni shunday yozish tokenga tushmaydi.

---

## 4. Marshrut: qaysi bilim qayerga boradi

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
| Foydalanuvchi afzalligi va roli | auto memory, `type: user` | Claude o'zi yozadi, odam yozishi shart emas |
| Berilgan tuzatish, tasdiqlangan yondashuv | auto memory, `type: feedback` | ikkinchi marta aytilmasligi uchun |
| Davom etayotgan ish holati, qaror, muddat | auto memory `type: project`, cloud'da repo hujjati | kodidan chiqarib bo'lmaydi |
| Tashqi manba manzili | auto memory, `type: reference` | |
| Shaxsiy, commit qilinmaydigan sozlama | `./CLAUDE.local.md` + `.gitignore` | jamoaga tegishli emas |
| Barcha loyihalardagi shaxsiy afzallik | `~/.claude/CLAUDE.md`, `~/.claude/rules/` | bitta joyda, hamma repo uchun |
| Majburiy bajarilishi yoki bloklanishi shart | hook (`PreToolUse`, `PostToolUse`) | memory kafolat bermaydi, hook beradi |
| Sir, token, parol, maxfiy manzil | hech qayerga | joyi aytiladi, qiymati emas |
| Bir martalik vazifa tafsiloti | hech qayerga | sessiya bilan tugaydi |

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

## 5. Darvoza: yozishdan oldingi yetti savol

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

## 6. Saqlash ketma-ketligi

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
   repodagi to'rtta handbook) hech qachon avtomatik yuklanmaydi va shunday
   qolishi kerak.

### B faza. Ish davomida: nomzod to'plash

6. **Signalni belgila.** Tuzatish keldi, xato takrorlandi yoki kodidan
   chiqmaydigan kontekst oshkor bo'ldi. Signalni o'sha paytda qayd et, sessiya
   oxirida eslab qolishga ishonma.
7. **Darhol yozma.** Nomzodni to'plab tur. Bitta sessiyada bir xil mavzuga uch
   marta yozish - uchta chalkash yozuv degani. Istisno: foydalanuvchi "buni
   eslab qol" deb aniq aytgan bo'lsa, darhol yoziladi.

### C faza. Yozishdan oldin: filtr

8. **Darvozadan o'tkaz.** 5-bo'limdagi yetti savol. To'xtagan nomzod tashlanadi,
   "ehtimol keyin kerak bo'ladi" degan zaxiraga olinmaydi.
9. **Marshrutni tanla.** 4-bo'limdagi jadval. Joy noto'g'ri bo'lsa, qolgan
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
14. **Natijani ko'r.** Interfeysda "Saved N memories" chiqadi. Chiqmasa, yozuv
    yo'q.

### F faza. Vaqti-vaqti bilan: tozalash

15. **Eskirganini o'chir.** Tugagan ish, bekor qilingan qaror, o'zgargan
    afzallik. O'chirish ham memory ishining bir qismi, qo'shimcha emas.
16. **Audit qil.** `/memory` papkani ochadi, `/doctor prompt-audit` ziddiyatli va
    eskirgan ko'rsatmalarni topadi (CLI v2.1.283+).

### Qisqa karta

```text
O'QISH:  /context -> index -> faqat kerakli topic fayl
NOMZOD:  signal bor? (tuzatish | ikkinchi xato | yashirin kontekst)
DARVOZA: 7 savol -> bittasi "yo'q" bo'lsa, tashlanadi
MARSHRUT: CLAUDE.md | rules+paths | skill | auto memory | repo doc | hook | hech qayerga
YOZISH:  qidir -> yangila (qo'shma) -> index bir qator + topic tafsilot
KEYIN:   hajm -> ziddiyat -> eskirganini o'chir
```

---

## 7. Yozuv formati va nomlash

Format erkin bo'lsa, memory bir yildan keyin o'qib bo'lmaydigan holga keladi.
Shuning uchun yozuvning shakli qat'iy.

### Index: `MEMORY.md`

Index papkadagi nima qayerda turganini ko'rsatadi. Bitta yozuv - bitta qator.
Qator mazmunni **tasvirlaydi**, o'zida saqlamaydi.

```markdown
# Memory

- `user_til.md` - javob tili va yozuv uslubi talablari
- `feedback_hujjat_formati.md` - hujjat yig'ishdagi format qoidalari va tuzoqlar
- `project_handbook_holati.md` - to'rtta handbook'ning hozirgi holati
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
| "Hujjatlar sifatli bo'lsin" | "Har bob oxirida `### Amalda qo'llash` bo'limi bo'ladi" |
| "Testlarni unutmang" | "Commit'dan oldin `mvn verify` ishlatiladi" |
| "Foydalanuvchi aniqlikni yaxshi ko'radi" | "Javob birinchi qatorida natija turadi, keyin tafsilot" |

---

## 8. Hajm budjeti va qattiq chegaralar

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

## 9. Eskirish, ziddiyat va o'chirish

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

## 10. Cloud va lokal sessiya farqi

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

1. Jamoaga va kelajak sessiyalarga kerak bilim: `CLAUDE.md`, `.claude/rules/`,
   `.claude/skills/` yoki repodagi hujjat. Hammasi commit qilinadi.
2. Ishning yarim qolgan holati: repodagi hujjat (eski `HANDOFF.md` aynan shu
   vazifani bajargan), auto memory emas.
3. Faqat bitta sessiyaga tegishli narsa: scratchpad, hech qayerga saqlanmaydi.

Subagent uchun ham shu mantiq: asosiy suhbatning auto memory'si subagent'ga
yuklanmaydi (fork'dan tashqari). Ya'ni ishni agentga topshirganda kerakli
kontekst **prompt ichida** beriladi, "memoryda bor" deb o'ylab bo'lmaydi.

---

## 11. Kelajakda inobatga olinadigan narsalar

Quyidagilar vaqt o'tishi bilan memoryni buzadigan narsalar. Har biri bir marta
hisobga olinsa, keyin muammo bo'lmaydi.

### Mexanika o'zgaradi

- Memory xususiyatlari CLI versiyasiga bog'langan (`modified` maydoni v2.1.214+,
  `AGENTS.md` o'qish v2.1.277+, `/doctor prompt-audit` v2.1.283+). Mexanika
  haqidagi yozuvga versiya raqami qo'shiladi, aks holda u bir yildan keyin
  noto'g'ri bo'ladi.
- Yo'l va sozlama nomlari ham o'zgarishi mumkin. Shu hujjat o'zi ham audit
  obyekti: har yirik yangilanishdan keyin tekshiriladi.

### Memory o'zi ishlamay qolishi mumkin

- Auto memory o'chirilgan bo'lishi mumkin (`autoMemoryEnabled`,
  `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, self-hosted muhitda default o'chiq).
  Muhim bilim faqat auto memoryda qolmasin.
- Background sessiyada yoki Claude Code ichidan ishga tushgan sessiyada toggle
  qayta yoqilmaydi.
- `permissions.blockReadsOutsideWorkingDirectories` yoqilgan bo'lsa, repo bergan
  settings fayli ko'rsatgan memory papkasidan hech narsa o'qilmaydi va yozilmaydi.

### Kontekst va compaction

- Loyiha ildizidagi `CLAUDE.md` compaction'dan keyin qayta o'qiladi va kontekstga
  qaytariladi. Ichki papkadagi `CLAUDE.md` va `paths:` li rules esa faqat mos
  fayl ochilganda qaytadi.
- Faqat suhbatda aytilgan ko'rsatma compaction'dan keyin qolmaydi. Saqlanishi
  kerak bo'lsa, faylga yoziladi.

### O'sish bilan keladigan muammolar

- Yozuv soni o'sgani sayin index chegaraga yaqinlashadi. Chegara jim ishlaydi:
  xato chiqmaydi, shunchaki oshgan qator yuklanmaydi.
- Monorepo'da boshqa jamoaning `CLAUDE.md` fayllari ham ko'tariladi.
  `claudeMdExcludes` bilan chiqarib tashlanadi.
- Yozuvlar soni o'sganda ziddiyat ehtimoli ham o'sadi. Davriy audit shart.

### Yangi MD qo'shilganda

- Yangi memory bilan ishlaydigan fayl qoidani **nusxalamaydi**, shu faylga havola
  qiladi.
- Havola teskari apostrof ichida beriladi, `@` bilan import qilinmaydi.
- Qoida o'zgarsa, faqat shu fayl o'zgaradi. Ikkinchi joyda nusxasi bo'lsa,
  o'zgarish bir joyda qolib ketadi va ziddiyat tug'iladi.

---

## 12. Memoryga yozilmaydigan narsalar

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

## 13. Tekshirish va audit

Memory "yozdim" bilan tugamaydi. Yozuv yuklanganini va hali to'g'ri turganini
tekshirish kerak.

| Vosita | Nima qiladi | Qachon |
|---|---|---|
| `/context` | sessiyaga qaysi memory fayllar yuklanganini ko'rsatadi | qoida ishlamaganda birinchi qadam |
| `/memory` | CLAUDE.md, CLAUDE.local.md va auto memory papkasini ochadi, toggle beradi | yozuvni ko'rish va qo'lda tuzatish |
| `/doctor prompt-audit` | eskirgan, mavjud bo'lmagan faylga havola qiladigan va ziddiyatli ko'rsatmalarni topadi (v2.1.283+) | davriy audit |
| `/doctor` | commit qilingan `CLAUDE.md` uchun qisqartirish taklif qiladi (v2.1.206+) | fayl uzayib ketganda |
| `/status` | uzunlik ogohlantirishlarini ko'rsatadi | startda ogohlantirish chiqqanda |
| `InstructionsLoaded` hook | qaysi fayl qachon va nega yuklanganini log qiladi | `paths:` li rules nosozligini topishda |

### "Claude qoidani bajarmadi" tartibi

1. `/context` - fayl yuklanganmi? Yo'q bo'lsa, boshqa hech narsani tekshirmang,
   fayl joyi noto'g'ri.
2. Gap aniqmi? Mavhum ko'rsatma ishlamaydi.
3. Boshqa qatlamda qarama-qarshi gap bormi?
4. Ko'rsatma Claude Code o'zi qo'shadigan yo'riqnomaga qarshi chiqmaydimi
   (masalan commit qoidalari: `includeGitInstructions`, `attribution`).
5. Shart **majburiy** bo'lsa, u memoryda emas, hook'da bo'lishi kerak.

---

## 14. Boshqa MD lar uchun ulanish bloki

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

## 15. Amalda qo'llash

- [ ] Loyiha `CLAUDE.md` da shu faylga bir qatorli havola bor, `@` import yo'q
- [ ] `/context` ishlatib yuklanadigan memory fayllar ro'yxati bir marta ko'rilgan
- [ ] Auto memory index'da har yozuv bitta qator, tafsilot topic fayllarda
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
