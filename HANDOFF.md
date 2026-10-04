# TOPSHIRIQ HUJJATI (HANDOFF)

Bu fayl ishni boshqa Claude sessiyasi uzilishsiz davom ettirishi uchun yozilgan.
Yangilangan: 2026-10-04, sessiya `calude-skill-21`.

## 1. Foydalanuvchi va uning talablari

- Til: **o'zbek lotin yozuvi**. Kirill yoki rus tili mutlaqo bo'lmasin. Texnik atamalar inglizcha qoladi (bean, proxy, thread, cache, latency).
- Uslub: **to'liqlik** eng muhim talab. "Hech qaysisi qolmasin" — foydalanuvchi qamrovni tekshiradi va yetishmaganini so'raydi.
- Tezlik ham muhim: foydalanuvchi bir marta "tezlashtir" dedi.
- Stack: **Java + Spring + PostgreSQL** va atrofidagi ekotizim.
- Ish papkasi: `/Users/manguberdi/calude_skill` (git repo EMAS).
- Scratchpad: `/private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad`

## 2. Tugallangan ishlar

| Fayl | Hajm | Mazmun |
|---|---|---|
| `java-spring-design-patterns.md` | 2.31 MB | 1007 ta dizayn pattern, 30 bo'lim |
| `java-spring-testing-handbook.md` | 447 KB | Testlash qo'llanmasi, 18 bob, 239 bo'lim |

Ikkalasi ham tekshiruvdan o'tgan: format xatosi yo'q, havolalar ishlaydi, kirill yo'q.

## 3. HOZIRGI ISH: "Arxitektor miyyasi" hujjati

Foydalanuvchi so'rovi: "arxitektor kod yozadigan dasturchi qanaqa bo'lishi kerak, nimalarni bilishi kerak — shunaqa miyya yozib ber md da. Bu eng muhim md."
Keyingi aniqlashtirish: "java spring postgres va shuning atrofiga tegishli bilimlar bo'lishi kerak, to'liq."

**Natija fayli:** `/Users/manguberdi/calude_skill/java-spring-architect-mindset.md`

**Reja:** 39 bob, 6 qism. To'liq ro'yxat mashina o'qiydigan ko'rinishda:
`/private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/mindset_plan.json`

Qismlar:
1. **I. Fikrlash va qarorlar** — boblar 1-8
2. **II. Java chuqur bilim** — boblar 9-13
3. **III. Spring chuqur bilim** — boblar 14-19
4. **IV. PostgreSQL chuqur bilim** — boblar 20-26
5. **V. Atrof ekotizim** — boblar 27-31
6. **VI. Amaliyot va o'sish** — boblar 32-39

**Holat:** boblar 1, 2, 3, 4, 5 uchun agentlar ishga tushirilgan.
Boblar **6-39 hali ishga tushirilmagan** — asosiy qolgan ish shu.

Bob fayllari: `/private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/mindset/NN.md` (01.md ... 39.md).
Qaysi bob tayyorligini bilish: `ls /private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/mindset/`.

## 4. METODIKA (aynan shunday davom ettiring)

Har bir bob uchun **bitta `general-purpose` agent** ishga tushiriladi (Agent tool, background).
Bir xabarda 15-20 tagacha agentni parallel ishga tushirish mumkin.

### Agent promptining shabloni

```
O'ZBEK TILIDA (lotin yozuvi) "Kod yozadigan arxitektorning miyyasi: Java, Spring, PostgreSQL"
hujjatining N-bobini yozasan. Auditoriya: senior Java/Spring developer va arxitektor.

Faylga yoz: /private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/mindset/NN.md

BOB N: <o'zbekcha sarlavha> (<English title>)

Qamrab ol (har biri alohida ### kichik bo'lim):
- <8-14 ta aniq mavzu bandi — mavhum emas, aniq>

FORMAT (qat'iy):
- Hech qanday `#` yoki `##` sarlavha YOZMA. Faqat `### ` kichik sarlavhalar (RAQAMSIZ).
- Boshida 2-4 gapli kirish paragrafi (sarlavhasiz).
- Kamida N ta ```java (yoki ```sql / ```yaml) kod bloki, har biri 25-28 qatordan oshmasin.
- Kamida 1-3 ta Markdown jadval; ulardan biri "oddiy yondashuv va arxitektor yondashuvi"
  taqqoslashi bo'lsin (kamida 8 qator).
- Oxirgi bo'lim AYNAN: `### Amalda qo'llash` — 5-8 ta `- [ ] ` bandi.
- Boshqa boblarga faqat MAVZU NOMI bilan havola qil, bob RAQAMI bilan EMAS.
- Aniq, hayotiy misollar (to'lov servisi, buyurtma, hisobot). Mavhum gap urmang.
- O'zbek lotin yozuvi. Kirill yoki rus tili MUTLAQO bo'lmasin.
- Faktik aniq bo'l: Java 17-25, Spring Boot 3.x/4.x, Spring Framework 6.x/7.x,
  PostgreSQL 15-17. Mavjud bo'lmagan sinf/parametr nomini O'YLAB CHIQARMA.
- Hajm: 1900-2600 so'z.
- TEZLIK: butun faylni BITTA tool chaqiruvi bilan yoz (`cat > "<path>" <<'EOF'`).
  Boshqa fayllarni o'qima.

Oxirida faqat fayl yo'li va ### bo'limlar sonini qaytar.
```

### Texnik boblar uchun qo'shimcha talab

Java, Spring va PostgreSQL boblarida **amaliy chuqurlik** bo'lishi shart:
aniq parametr nomlari, `EXPLAIN ANALYZE` chiqishi, JVM flaglari, `postgresql.conf`
parametrlari, Spring annotatsiyalari, sozlash raqamlari va "qachon qaysi" jadvallari.
Har bobda kamida bitta "tuzoq va yechim" jadvali foydali.

## 5. YIG'ISH (assembly)

Yig'uvchi skript yozilishi kerak: `/private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/assemble_mindset.py`.
Namuna sifatida tayyor skriptdan nusxa oling: `/private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/assemble_testing.py` —
u aynan shu formatda ishlaydi va sinalgan.

Skript nima qiladi:
1. `mindset/NN.md` fayllarini tartib bilan o'qiydi.
2. Har bobga `## N. <sarlavha> (<English>)` sarlavhasini qo'yadi.
3. `### ` bo'limlarni `N.k` qilib avtomatik raqamlaydi (agentlar raqam yozmaydi).
4. Qism sarlavhalarini (`# I. Fikrlash va qarorlar` kabi) joylashtiradi.
5. Mundarija (TOC) yasaydi, GitHub anchor formatida.
6. Tekshiradi: to'rtta format sharti, kirill, kod fence juftligi, havolalar.

**MUHIM TUZOQ:** sarlavhalarni filtrlashda kod bloklari ichidagi `#`, `##`, `###`
qatorlariga TEGMANG. `assemble_testing.py` dagi `infence` mantig'i aynan shu uchun yozilgan —
uni nusxa oling.

## 6. O'RGANILGAN TUZOQLAR (takrorlamang)

1. **Tarmoq xatosi:** agentlar `ENOTFOUND` bilan yiqilishi mumkin. Har bob uchun
   3 martagacha qayta urinish mantig'ini qo'ying yoki yiqilganini qayta ishga tushiring.
2. **Kirill harflar:** agentlar lotin so'zlari ichiga tasodifan kirill harf qo'yadi
   (masalan "Monolитdan"). Yig'ishdan oldin ishlatish SHART:
   `python3 /private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/fix_cyrillic.py /private/tmp/claude-501/-Users-manguberdi-calude-skill/f543fdaa-cc3a-4de6-bb45-2da1a11eb51d/scratchpad/mindset/*.md`
3. **Python 3.9:** bu mashinada f-string ichida bir xil qo'shtirnoq ishlamaydi.
   `"%s" % x` uslubini ishlating.
4. **Bob yig'ilgandan keyin o'zgarishi:** agent yakuniy tuzatish kiritishi mumkin.
   Yig'ishdan oldin fayl vaqtini tekshiring, kerak bo'lsa qayta yig'ing.
5. **Kod fence ichidagi shablonlar:** 18-bobda `# sarlavha` lar shablon ichida bo'lgan,
   ularni o'chirib yuborish hujjatni buzadi.

## 7. YAKUNIY TEKSHIRUV RO'YXATI

- [ ] 39 ta bob fayli mavjud va bo'sh emas
- [ ] `fix_cyrillic.py` ishlatilgan, hujjatda 0 ta kirill harf
- [ ] Har bobda `### Amalda qo'llash` bo'limi bor
- [ ] Bo'lim raqamlari har bobda 1 dan ketma-ket
- [ ] Mundarijadagi barcha havolalar ishlaydi (ishlamaydigan = 0)
- [ ] Kod fence soni juft
- [ ] Har bobda kamida bitta taqqoslash jadvali
- [ ] Yakuniy fayl `/Users/manguberdi/calude_skill/java-spring-architect-mindset.md`
- [ ] Foydalanuvchiga `SendUserFile` bilan yuborilgan

## 8. FOYDALANUVCHIGA HISOBOT USLUBI

Javob o'zbek tilida, qisqa va aniq. Birinchi qatorda natija. Keyin:
nima yozildi, raqamlar jadvali, tekshiruv natijasi, ochiq qolgan tanlov.
Em-dash ishlatmang. Har gapda bitta fikr.
