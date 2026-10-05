# Memory mexanikasi: ikki tizim, qatlamlar, yuklanish va audit

Bu fayl Claude Code memory mexanikasini tasvirlaydi: qaysi fayl kim tomonidan
yoziladi, qachon va qaysi tartibda kontekstga yuklanadi, vaqt o'tishi bilan
nima buziladi va memory ishlamay qolganda qanday tekshiriladi. Nimani,
qayerga va qanday tartibda yozish kerakligi `memory-protocol.md` da, bu
yerda takrorlanmaydi.

Fayl kundalik yozishda o'qilmaydi. U memory yuklanmaganda, qoida
bajarilmaganda yoki CLI yangilangandan keyin mexanika o'zgarganmi deb
tekshirilganda ochiladi. Xuddi protokol kabi u ham `@` bilan import
qilinmaydi.

Tayanch holat: Claude Code memory mexanikasi, 2026-10. Versiyaga bog'liq
xususiyatlar yonida CLI versiyasi ko'rsatilgan.

## Mundarija

- [1. Ikki tizim: CLAUDE.md va auto memory](#1-ikki-tizim-claudemd-va-auto-memory)
- [2. Qatlamlar va yuklanish tartibi](#2-qatlamlar-va-yuklanish-tartibi)
- [3. Kelajakda inobatga olinadigan narsalar](#3-kelajakda-inobatga-olinadigan-narsalar)
- [4. Tekshirish va audit](#4-tekshirish-va-audit)
- [5. Amalda qo'llash](#5-amalda-qollash)

---

## 1. Ikki tizim: CLAUDE.md va auto memory

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

## 2. Qatlamlar va yuklanish tartibi

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

## 3. Kelajakda inobatga olinadigan narsalar

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

- Yangi memory bilan ishlaydigan fayl qoidani **nusxalamaydi**,
  `memory-protocol.md` ga havola qiladi: o'sha fayldagi `Boshqa MD lar uchun
  ulanish bloki` bo'limi.
- Havola teskari apostrof ichida beriladi, `@` bilan import qilinmaydi.
- Qoida o'zgarsa, faqat `memory-protocol.md` o'zgaradi. Ikkinchi joyda
  nusxasi bo'lsa, o'zgarish bir joyda qolib ketadi va ziddiyat tug'iladi.

---

## 4. Tekshirish va audit

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

## 5. Amalda qo'llash

- [ ] Muhim bilim faqat auto memoryda qolmagan: u o'chiq bo'lishi yoki
      mashinadan chiqmasligi mumkin
- [ ] Shaxsiy sozlama `CLAUDE.local.md` da va u `.gitignore` ga qo'shilgan
- [ ] `@path` import tartib uchun ishlatiladi, kontekstni tejash uchun emas
- [ ] Odam uchun izoh blok darajasidagi HTML izoh sifatida yozilgan
- [ ] Faqat suhbatda aytilgan va saqlanishi kerak ko'rsatma faylga yozilgan:
      compaction'dan keyin u qolmaydi
- [ ] Mexanika haqidagi har gap yonida CLI versiyasi ko'rsatilgan
- [ ] "Claude qoidani bajarmadi" holatida birinchi qadam `/context`
- [ ] CLI yirik yangilangandan keyin shu fayldagi versiyaga bog'liq gaplar
      va yo'llar qayta tekshirilgan
