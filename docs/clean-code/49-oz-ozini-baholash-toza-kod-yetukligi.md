<!-- doc: clean-code | chapter: 49 | part: XIII. Ma'lumotnoma -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 49. O'z-o'zini baholash: toza kod yetukligi (Self-Assessment)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [49.1 Yetuklik darajalari](#491-yetuklik-darajalari)
- [49.2 Nomlash va o'qilishi: o'zingizni sinash](#492-nomlash-va-oqilishi-ozingizni-sinash)
- [49.3 Funksiya va oqim: o'zingizni sinash](#493-funksiya-va-oqim-ozingizni-sinash)
- [49.4 Obyekt, holat, xato: o'zingizni sinash](#494-obyekt-holat-xato-ozingizni-sinash)
- [49.5 Java va Spring: o'zingizni sinash](#495-java-va-spring-ozingizni-sinash)
- [49.6 Hid, refaktoring, jarayon: o'zingizni sinash](#496-hid-refaktoring-jarayon-ozingizni-sinash)
- [49.7 Professional intizom: o'zingizni sinash](#497-professional-intizom-ozingizni-sinash)
- [49.8 Kod bazasini baholash: bir sahifali audit](#498-kod-bazasini-baholash-bir-sahifali-audit)
- [49.9 Keyingi qadam: hujjatni qanday ishlatish](#499-keyingi-qadam-hujjatni-qanday-ishlatish)
- [49.10 Amalda qo'llash](#4910-amalda-qollash)

</details>


Bu bob hujjatni o'zingizga qo'llash uchun: qaysi mavzuda qay darajada turganingizni aniqlash va keyingi qadamni tanlash. Arxitektor hujjatidagi o'z-o'zini baholash bobi arxitektura bilimini baholaydi; bu bob toza kod amaliyotini baholaydi.

## 49.1 Yetuklik darajalari

Har bir mavzu uchun to'rt daraja bor va o'zini baholash shu shkala bo'yicha boradi.

| Daraja | Belgisi |
|---|---|
| 1 - Bilmayman | qoida mavjudligini bilmayman |
| 2 - Bilaman | qoidani bilaman, lekin eslatish kerak |
| 3 - Qo'llayman | kod yozganda avtomatik qo'llayman |
| 4 - O'rgataman | boshqalarga tushuntiraman va qoidani majburlaydigan tizim quraman |

Maqsad hamma mavzuda 4 ga chiqish emas: kundalik ishga tegishli mavzularda 3-4, qolganlarda 2 yetarli.

## 49.2 Nomlash va o'qilishi: o'zingizni sinash

- [ ] Nom javob berishi kerak bo'lgan uchta savolni aytib bera olaman (2.1).
- [ ] `isNotEligible` nomi nega yomon ekanini tushuntiraman (3.1).
- [ ] `IOrderRepository` nomining ikki muammosini sanayman (2.7).
- [ ] `timeoutMs` dan ko'ra `Duration timeout` nega afzal (3.3).
- [ ] `get`/`find`/`fetch` taqsimotini jamoada qanday majburlash mumkin (2.11, 42.4).
- [ ] Nom uzunligi qamrovga qanday bog'liq (2.15).

## 49.3 Funksiya va oqim: o'zingizni sinash

- [ ] "Bitta ish qiladi" ni qanday tekshiraman (4.2).
- [ ] Flag argumenti nega "bitta ish" qoidasini buzadi (5.3).
- [ ] Chiqish argumentini nima bilan almashtiraman (5.5).
- [ ] Enum ustidagi `switch` da `default` nega yozilmaydi (6.6).
- [ ] Yashirin vaqt bog'liqligini qanday ko'rinadigan qilaman (6.9).
- [ ] Siklni quvurga aylantirish mezonini aytib bera olaman (7.7).

## 49.4 Obyekt, holat, xato: o'zingizni sinash

- [ ] `final List` nega o'zgarmaslikni kafolatlamaydi (16.1).
- [ ] `Collections.unmodifiableList` va `List.copyOf` farqi (16.3).
- [ ] `equals` ning besh qoidasini sanayman (15.1).
- [ ] Entitet va value object tengligi farqi (15.5).
- [ ] `compareTo` va `equals` izchilligi nega muhim (15.6).
- [ ] `finally` ichidagi `return` nima qiladi (19.3).
- [ ] `InterruptedException` tutilganda nima qilish kerak (19.5).
- [ ] Konstruktorda `this` ni tashqariga berish nega xavfli (14.10).

## 49.5 Java va Spring: o'zingizni sinash

- [ ] `new BigDecimal(0.1)` va `new BigDecimal("0.1")` farqi (20.1).
- [ ] `Integer` larni `==` bilan solishtirish qachon noto'g'ri natija beradi (20.5).
- [ ] `"ID".toLowerCase()` turk serverida nima qaytaradi (21.4).
- [ ] `split(".")` nega bo'sh massiv beradi (21.5).
- [ ] `Duration.ofDays(1)` va `Period.ofDays(1)` farqi (22.5).
- [ ] `Collectors.toMap` ning ikki argumentli shakli qachon yiqiladi (23.3).
- [ ] `parallelStream` nega deyarli har doim noto'g'ri tanlov (24.5).
- [ ] Entitetda `@Data` nima qiladi (28.2).
- [ ] `@ManyToOne` ning standart `fetch` qiymati nima (28.4).
- [ ] `log.error("xato: {}", e)` nega stack trace bermaydi (29.3).

## 49.6 Hid, refaktoring, jarayon: o'zingizni sinash

- [ ] Takrorlanishning to'rt turini va ularning yechimini sanayman (32.2).
- [ ] Soxta takrorlanishni nega birlashtirmaslik kerak (32.2).
- [ ] Hide Delegate va Remove Middle Man qachon qo'llanadi (36.3-36.4).
- [ ] Katta refaktoringni to'rt qadamga qanday bo'laman (38.5).
- [ ] Refaktoring commiti va mantiq commitini nega ajrataman (38.4).
- [ ] Nomni o'zgartirgandan keyin IDE ko'rmagan olti joyni sanayman (38.3).
- [ ] Yangi lint qoidasini besh bosqichda qanday joriy qilaman (42.6).
- [ ] Atomik commitning uch shartini aytaman (40.1).

## 49.7 Professional intizom: o'zingizni sinash

- [ ] "Urinib ko'raman" nega yolg'on javob (44.2).
- [ ] Majburiyatning uch qismini sanayman (44.3).
- [ ] Uch nuqtali bahodan kutilgan qiymatni hisoblayman (45.2).
- [ ] Bosim ostida nimani qisqartiraman, nimani hech qachon (45.7).
- [ ] "90% tayyor" hisobotini nima bilan almashtiraman (45.6).
- [ ] Botqoq va ko'r yo'lak farqini va chiqish usulini bilaman (46.5).
- [ ] Review izohini o'rgatish vositasiga qanday aylantiraman (47.4).

## 49.8 Kod bazasini baholash: bir sahifali audit

Shaxsiy baholashdan tashqari kod bazasining holatini ham o'lchash kerak. Quyidagi skript bir marta ishga tushirilib, natijasi yozib qo'yiladi va chorakda bir takrorlanadi.

```bash
#!/bin/sh
# Toza kod auditi: raqamlar bilan holat. Chorakda bir ishga tushiriladi.
SRC=src/main/java

echo "== Hajm =="
find $SRC -name '*.java' | wc -l | sed 's/^/Fayllar: /'
find $SRC -name '*.java' | xargs wc -l | tail -1 | awk '{print "Qatorlar: " $1}'
find $SRC -name '*.java' | xargs wc -l | sort -rn | sed -n '2,6p'

echo "== Hidlar =="
grep -rl "class .*Manager\|class .*Helper\|class .*Util\b" $SRC | wc -l \
  | sed 's/^/Manager|Helper|Util sinflar: /'
grep -rn "@Autowired" $SRC | grep -v "(" | wc -l | sed 's/^/Maydon inyeksiyasi: /'
grep -rn "java.util.Date\|SimpleDateFormat\|Calendar" $SRC | wc -l | sed 's/^/Eski sana API: /'
grep -rnE "(double|Double) +[a-zA-Z]*([Aa]mount|[Pp]rice|[Tt]otal)" $SRC | wc -l \
  | sed 's/^/Pul double da: /'
grep -rn "catch (Exception\|catch (Throwable" $SRC | wc -l | sed 's/^/Keng catch: /'
grep -rn "e.getMessage()" $SRC | wc -l | sed 's/^/getMessage() log: /'
grep -rn "return null" $SRC | wc -l | sed 's/^/return null: /'
grep -rn "TODO\|FIXME" $SRC | wc -l | sed 's/^/TODO va FIXME: /'
grep -rn "@SuppressWarnings" $SRC | wc -l | sed 's/^/Bostirishlar: /'
grep -rn "^import .*\*;" $SRC | wc -l | sed 's/^/Yulduzcha import: /'
grep -rn "Optional<" $SRC | grep -E "private +Optional|Optional<[A-Za-z<>]+> +[a-z]+;" | wc -l \
  | sed 's/^/Optional maydon: /'

echo "== Jarayon =="
git log --since="3 months ago" --oneline | wc -l | sed 's/^/Commitlar (3 oy): /'
git log --since="3 months ago" --oneline | grep -ci revert | sed 's/^/Revertlar: /'
git log --since="3 months ago" --pretty=format: --name-only | sort | uniq -c \
  | sort -rn | head -5 | sed 's/^/Eng ko.p o.zgargan: /'
```

## 49.9 Keyingi qadam: hujjatni qanday ishlatish

Bu hujjatni boshdan-oxir o'qish shart emas va samarali ham emas. Uchta ishlatish usuli bor.

**Birinchi - muammo bo'yicha.** Aniq savol tug'ilganda 48.11 jadvalidan bo'limni topish. Bu eng ko'p ishlatiladigan usul.

**Ikkinchi - jamoa standarti sifatida.** [48-bobdagi](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md) jadvallarni jamoa kelishuviga (47.5) ko'chirish, keyin [42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md) bo'yicha ularni mashinaga topshirish. Bu hujjatning asosiy qiymati shu yerda: qoida mashinaga ko'chganda u haqiqatan ishlaydi.

**Uchinchi - o'sish rejasi sifatida.** 49.2-49.7 bo'limlaridagi savollarga javob berib, 2 dan past darajadagi mavzularni ro'yxatlab, chorakda uch mavzuni 3 darajaga chiqarish.

## 49.10 Amalda qo'llash

- [ ] 49.2-49.7 bo'limlaridagi savollarga halol javob berib, har bir mavzuga 1-4 daraja qo'ying.
- [ ] 2 va undan past darajadagi mavzulardan uchtasini tanlab, chorak maqsadi qiling.
- [ ] 49.8 dagi auditni ishga tushirib, natijani sanasi bilan repoda saqlang.
- [ ] Audit natijasidagi eng katta uch raqamni tuzatish rejasiga aylantiring.
- [ ] [48-bobdagi](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md) jadvallardan jamoa kelishuviga ko'chiriladigan qismlarni ajratib oling.
- [ ] Mashinaga topshirilishi mumkin bo'lgan qoidalarni [42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md) bo'yicha joriy qilish rejasini tuzing.
- [ ] Hujjatni jamoaga tanishtirishda 48.11 xaritasidan boshlang: qaysi savol qaysi hujjatda.
- [ ] Chorak oxirida auditni qaytarib, raqamlar yo'nalishini (yaxshilanish yoki yomonlashish) baholang.

---

[&larr; 48. Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md) · [Mundarija](README.md)
