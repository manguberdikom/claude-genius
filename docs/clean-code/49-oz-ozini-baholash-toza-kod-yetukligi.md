<!-- doc: clean-code | chapter: 49 | part: XIII. Ma'lumotnoma -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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

Bu bo'limdagi shkala hech bir kitobdan olinmagan va biror sanoat modeliga (CMM va shunga o'xshash) tayanmaydi: u shu korpusning o'z tekshiruv ro'yxatlarini o'qish usuli. Shuning uchun unda ball ham, umumiy "daraja" ham yo'q - faqat har bir mavzu uchun to'rt holat.

| Holat | Belgisi |
|---|---|
| Bilmayman | qoida mavjudligini bilmayman |
| Bilaman | qoidani bilaman, lekin eslatish kerak |
| Qo'llayman | kod yozganda avtomatik qo'llayman |
| O'rgataman | boshqalarga tushuntiraman va qoidani majburlaydigan tizim quraman |

Holatni bitta songa yig'ish noto'g'ri bo'lardi va buning sababi kitobda aytilgan. Google kitobining bilim almashish bobi malakani ikki holatli ("yangi boshlovchi yoki ekspert") deb qarashni xato deb ataydi: malaka ko'p o'lchovli vektor, har kimda turli sohada turli daraja bo'ladi. Shu bobda o'rgatish ekspertlarning monopoliyasi emasligi ham aytilgan: o'rgatiladigan narsa har kimda bor.

Shu sababli maqsad hamma mavzuda "o'rgataman" holatiga chiqish emas: kundalik ishga tegishli mavzularda "qo'llayman" yoki "o'rgataman", qolganlarida "bilaman" yetarli.

## 49.2 Nomlash va o'qilishi: o'zingizni sinash

- [ ] Nom javob berishi kerak bo'lgan uchta savolni aytib bera olaman ([2.1](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#21-nom-javob-berishi-kerak-bolgan-uchta-savol)).
- [ ] `isNotEligible` nomi nega yomon ekanini tushuntiraman ([3.1](03-nom-turlari-boyicha-aniq-konvensiyalar.md#31-mantiqiy-nomlar-is-has-can-should-va-inkor-tuzogi)).
- [ ] `IOrderRepository` nomining ikki muammosini sanayman ([2.7](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#27-kodlash-va-prefikslar-hungarian-notation-m_-i-prefiksi), [3.6](03-nom-turlari-boyicha-aniq-konvensiyalar.md#36-interfeys-va-implementatsiya-nomlari-impl-qachon-haqli)).
- [ ] `timeoutMs` dan ko'ra `Duration timeout` nega afzal ([3.3](03-nom-turlari-boyicha-aniq-konvensiyalar.md#33-birlik-nomda-timeoutms-sizebytes-priceminor)).
- [ ] `get`/`find`/`fetch` taqsimotini jamoada qanday majburlash mumkin ([2.11](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#211-bitta-tushunchaga-bitta-soz), [42.4](42-statik-tahlil-va-avtomatik-qoidalar.md#424-archunit-bilan-qoidani-kodga-aylantirish)).
- [ ] Nom uzunligi qamrovga qanday bog'liq ([2.15](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#215-nom-uzunligi-qamrovga-mutanosib)).

## 49.3 Funksiya va oqim: o'zingizni sinash

- [ ] "Bitta ish qiladi" ni qanday tekshiraman ([4.2](04-funksiya-kichiklik-va-bitta-ish.md#42-bitta-ish-qiladi-ni-qanday-tekshirish)).
- [ ] Flag argumenti nega "bitta ish" qoidasini buzadi ([5.3](05-funksiya-argumentlari.md#53-flag-argumenti-va-uni-ikki-funksiyaga-bolish)).
- [ ] Chiqish argumentini nima bilan almashtiraman ([5.5](05-funksiya-argumentlari.md#55-chiqish-argumenti-va-void-dan-qaytishga-otish)).
- [ ] Enum ustidagi `switch` da `default` nega yozilmaydi ([6.6](06-shart-mantiq-va-boshqaruv-oqimi.md#66-switch-ni-toza-ishlatish-toliqlik-default-fallthrough)).
- [ ] Yashirin vaqt bog'liqligini qanday ko'rinadigan qilaman ([6.9](06-shart-mantiq-va-boshqaruv-oqimi.md#69-yashirin-vaqt-bogliqligini-korinadigan-qilish)).
- [ ] Siklni quvurga aylantirish mezonini aytib bera olaman ([7.7](07-sikl-iteratsiya-va-toplam-bilan-ishlash.md#77-sikldan-quvurga-otish-mezoni)).

## 49.4 Obyekt, holat, xato: o'zingizni sinash

- [ ] `final List` nega o'zgarmaslikni kafolatlamaydi ([16.1](16-ozgarmaslik-va-holat-boshqaruvi-kod.md#161-final-maydon-final-sinf-va-haqiqiy-ozgarmaslik)).
- [ ] `Collections.unmodifiableList` va `List.copyOf` farqi ([16.3](16-ozgarmaslik-va-holat-boshqaruvi-kod.md#163-ozgarmas-toplamlar-listof-unmodifiable-nusxa)).
- [ ] `equals` ning besh qoidasini sanayman ([15.1](15-tenglik-hash-va-obyekt-shartnomalari.md#151-equals-shartnomasi-besh-qoida)).
- [ ] Entitet va value object tengligi farqi ([15.5](15-tenglik-hash-va-obyekt-shartnomalari.md#155-entitet-va-value-object-tengligi-farqi)).
- [ ] `compareTo` va `equals` izchilligi nega muhim ([15.6](15-tenglik-hash-va-obyekt-shartnomalari.md#156-compareto-shartnomasi-va-equals-bilan-izchillik)).
- [ ] `finally` ichidagi `return` nima qiladi ([19.3](19-istisno-mexanikasi-va-resurslar.md#193-finally-ichidagi-return-va-bostirilgan-istisno)).
- [ ] `InterruptedException` tutilganda nima qilish kerak ([19.5](19-istisno-mexanikasi-va-resurslar.md#195-interruptedexception-ni-togri-qayta-tiklash)).
- [ ] Konstruktorda `this` ni tashqariga berish nega xavfli ([14.10](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#1410-this-ning-konstruktordan-qochib-ketishi)).

## 49.5 Java va Spring: o'zingizni sinash

- [ ] `new BigDecimal(0.1)` va `new BigDecimal("0.1")` farqi ([20.1](20-primitiv-son-va-pul.md#201-pul-uchun-double-ishlatmaslik)).
- [ ] `Integer` larni `==` bilan solishtirish qachon noto'g'ri natija beradi ([20.5](20-primitiv-son-va-pul.md#205-primitiv-va-boxed-tur-tanlovi--tuzogi)).
- [ ] `"ID".toLowerCase()` turk serverida nima qaytaradi ([21.4](21-satr-matn-va-regex.md#214-tolowercase-format-va-locale-tuzogi)).
- [ ] `split(".")` nega bo'sh massiv beradi ([21.5](21-satr-matn-va-regex.md#215-split-trim-strip-isblank-farqlari)).
- [ ] `Duration.ofDays(1)` va `Period.ofDays(1)` farqi ([22.5](22-sana-vaqt-va-mintaqa.md#225-davomiylik-duration-period-va-birlik-nomi)).
- [ ] `Collectors.toMap` ning ikki argumentli shakli qachon yiqiladi ([23.3](23-toplamlar-va-generiklar-gigiyenasi.md#233-collectorstomap-va-takrorlangan-kalit)).
- [ ] `parallelStream` nega deyarli har doim noto'g'ri tanlov ([24.5](24-lambda-oqim-va-funksional-uslub-tozaligi.md#245-peek-parallelstream-va-tartib)).
- [ ] Entitetda `@Data` nima qiladi ([28.2](28-jpa-va-sql-kodining-tozaligi.md#282-lombok-va-entitet-nimani-ishlatmaslik)).
- [ ] `@ManyToOne` ning standart `fetch` qiymati nima ([28.4](28-jpa-va-sql-kodining-tozaligi.md#284-fetch-cascade-orphanremoval-ni-oshkor-yozish)).
- [ ] `log.error("xato: {}", e)` nega stack trace bermaydi ([29.3](29-log-kodining-tozaligi.md#293-istisnoni-oxirgi-argument-sifatida-berish)).

## 49.6 Hid, refaktoring, jarayon: o'zingizni sinash

- [ ] Takrorlanishning uch turini va ularning yechimini sanayman ([32.2](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#322-takrorlangan-kod-duplicated-code)).
- [ ] Soxta takrorlanishni nega birlashtirmaslik kerak ([32.2](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#322-takrorlangan-kod-duplicated-code)).
- [ ] Hide Delegate va Remove Middle Man qachon qo'llanadi ([36.3](36-refaktoring-harakatlari-katalogi-ii-malumot.md#363-delegatni-yashirish-hide-delegate), [36.4](36-refaktoring-harakatlari-katalogi-ii-malumot.md#364-vositachini-olib-tashlash-remove-middle-man)).
- [ ] Katta refaktoringni to'rt qadamga qanday bo'laman ([38.5](38-refaktoringni-xavfsiz-bajarish.md#385-katta-refaktoringni-bolish-abstraksiya-orqali-shox)).
- [ ] Refaktoring commiti va mantiq commitini nega ajrataman ([38.4](38-refaktoringni-xavfsiz-bajarish.md#384-refaktoringni-mantiq-ozgarishidan-ajratish)).
- [ ] Nomni o'zgartirgandan keyin IDE ko'rmagan olti joyni sanayman ([38.3](38-refaktoringni-xavfsiz-bajarish.md#383-ide-refaktoringiga-ishonish-chegarasi)).
- [ ] Yangi lint qoidasini besh bosqichda qanday joriy qilaman ([42.6](42-statik-tahlil-va-avtomatik-qoidalar.md#426-qoidani-joriy-qilish-tartibi-ogohlantirish-keyin-xato)).
- [ ] Atomik commitning uch shartini aytaman ([40.1](40-versiya-nazorati-gigiyenasi.md#401-atomik-commit-bitta-mantiqiy-ozgarish)).

## 49.7 Professional intizom: o'zingizni sinash

- [ ] "Urinib ko'raman" nega yolg'on javob ([44.2](44-yoq-va-ha-deyish-majburiyat-tili.md#442-urinib-koraman-nega-yolgon)).
- [ ] Majburiyatning uch qismini sanayman ([44.3](44-yoq-va-ha-deyish-majburiyat-tili.md#443-majburiyat-tili-aytaman-qilaman-qachongacha)).
- [ ] Uch nuqtali bahodan kutilgan qiymatni hisoblayman ([45.2](45-baholash-muddat-va-bosim.md#452-uch-nuqtali-baho-va-pert)).
- [ ] Bosim ostida nimani qisqartiraman, nimani hech qachon ([45.7](45-baholash-muddat-va-bosim.md#457-qamrovni-qisqartirish-yoki-sifatni-qisqartirish)).
- [ ] "90% tayyor" hisobotini nima bilan almashtiraman ([45.6](45-baholash-muddat-va-bosim.md#456-kechikishni-oshkor-qilish-va-90-tayyor-tuzogi)).
- [ ] Botqoq va ko'r yo'lak farqini va chiqish usulini bilaman ([46.5](46-vaqt-diqqat-va-mashq.md#465-kor-yolak-va-botqoqdan-chiqish)).
- [ ] Review izohini o'rgatish vositasiga qanday aylantiraman ([47.4](47-birgalikda-ishlash-va-orgatish.md#474-review-ni-orgatish-vositasiga-aylantirish)).
- [ ] Yangi odamga mentor tayinlashning shartlarini aytaman ([47.2](47-birgalikda-ishlash-va-orgatish.md#472-ustoz-shogird-modeli)).

## 49.8 Kod bazasini baholash: bir sahifali audit

Shaxsiy baholashdan tashqari kod bazasining holatini ham o'lchash kerak. Quyidagi skript shu korpusning o'z yig'masi: u hech qanday kitobdagi metrikani takrorlamaydi va "yaxshi" yoki "yomon" chegara bermaydi. U faqat hidlarning sonini chiqaradi, chegarani esa jamoa o'z tarixiga qarab o'zi qo'yadi. Skript bir marta ishga tushirilib, natijasi sanasi bilan yozib qo'yiladi va chorakda bir takrorlanadi; qiymati bitta o'lchovda emas, ikki o'lchov orasidagi yo'nalishda.

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

Har bir qator o'z bo'limiga bog'lanadi: `Manager`/`Helper` sinflar [2.9](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#29-sinf-nomi-ot-metod-nomi-fel-getter-konvensiyasi), maydon inyeksiyasi [26.1](26-spring-kodining-tozaligi.md#261-konstruktor-inyeksiyasi-va-final-maydon), eski sana API [22.3](22-sana-vaqt-va-mintaqa.md#223-clock-ni-inyeksiya-qilish-va-testlanadigan-vaqt), pul `double` da [20.1](20-primitiv-son-va-pul.md#201-pul-uchun-double-ishlatmaslik), keng `catch` [19.6](19-istisno-mexanikasi-va-resurslar.md#196-throwable-error-va-outofmemoryerror-siyosati), `getMessage()` logi [29.4](29-log-kodining-tozaligi.md#294-egetmessage-bilan-stack-trace-ni-yoqotish), `return null` [18.7](18-xato-bilan-ishlash-qoidalari.md#187-null-qaytarmaslik-va-null-uzatmaslik), `TODO` va `FIXME` [8.7](08-izoh-qoidalari-yaxshi-izohlar.md#87-todo-fixme-va-ularning-hayot-muddati), yulduzcha import [12.7](12-gorizontal-formatlash-va-kod-uslubi.md#127-import-tartibi-va-yulduzcha-import), `Optional` maydon [18.7](18-xato-bilan-ishlash-qoidalari.md#187-null-qaytarmaslik-va-null-uzatmaslik), eng ko'p o'zgargan fayllar [33.1](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md#331-tarqoq-ozgarish-divergent-change).

## 49.9 Keyingi qadam: hujjatni qanday ishlatish

Bu hujjatni boshdan-oxir o'qish shart emas va samarali ham emas. Uchta ishlatish usuli bor.

**Birinchi - muammo bo'yicha.** Aniq savol tug'ilganda [48.11](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md#4811-olti-hujjat-bilan-boglanish-xaritasi) jadvalidan bo'limni topish. Bu eng ko'p ishlatiladigan usul.

**Ikkinchi - jamoa standarti sifatida.** [48-bobdagi](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md) jadvallarni jamoa kelishuviga ([47.5](47-birgalikda-ishlash-va-orgatish.md#475-jamoa-kelishuvi-working-agreement-yozish)) ko'chirish, keyin [42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md) bo'yicha ularni mashinaga topshirish. Buning sababi kitobda aytilgan: McConnell standartni yozib tarqatish bilan u bajarilmasligini ko'rsatadi, mashina esa qoidani muhokamasiz majburlaydi.

**Uchinchi - o'sish rejasi sifatida.** 49.2-49.7 bo'limlaridagi savollarga javob berib, "bilmayman" va "bilaman" holatidagi mavzularni ro'yxatlab, chorakda uch mavzuni "qo'llayman" holatiga chiqarish.

## 49.10 Amalda qo'llash

- [ ] 49.2-49.7 bo'limlaridagi savollarga halol javob berib, har bir mavzuga 49.1 dagi to'rt holatdan birini qo'ying.
- [ ] "Bilmayman" va "bilaman" holatidagi mavzulardan uchtasini tanlab, chorak maqsadi qiling.
- [ ] 49.8 dagi auditni ishga tushirib, natijani sanasi bilan repoda saqlang.
- [ ] Audit natijasidagi eng katta uch raqamni tuzatish rejasiga aylantiring.
- [ ] [48-bobdagi](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md) jadvallardan jamoa kelishuviga ko'chiriladigan qismlarni ajratib oling ([47.5](47-birgalikda-ishlash-va-orgatish.md#475-jamoa-kelishuvi-working-agreement-yozish)).
- [ ] Mashinaga topshirilishi mumkin bo'lgan qoidalarni [42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md) bo'yicha joriy qilish rejasini tuzing.
- [ ] Hujjatni jamoaga tanishtirishda [48.11](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md#4811-olti-hujjat-bilan-boglanish-xaritasi) xaritasidan boshlang: qaysi savol qaysi hujjatda.
- [ ] Chorak oxirida auditni qaytarib, raqamlar yo'nalishini (yaxshilanish yoki yomonlashish) baholang.

## Manbalar

- Bu bob korpusning o'z savollar to'plami: har bir savolning javobi havola qilingan bo'limda turadi va birlamchi manba shu bo'limda keltirilgan.
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 3-bob - malaka ikki holatli emas, ko'p o'lchovli vektor: har kimda turli sohada turli daraja bo'ladi, shu sababli umumiy bitta "daraja" qo'yish ma'nosiz
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21-bob (482-bet) - yozib tarqatilgan standart o'z-o'zidan bajarilmaydi: 49.9 dagi "qoidani mashinaga topshirish" tavsiyasining asosi
- ESLATMA: 49.1 dagi to'rt holat shu korpusning tekshiruv ro'yxatlarini o'qish usuli, kitobdagi yetuklik modeli emas; CMM yoki boshqa sanoat modeliga tayanmaydi
- ESLATMA: 49.8 dagi audit skripti va undagi grep namunalari shu korpusning amaliy yig'masi; unda "normal" deb hisoblanadigan raqam yo'q, chunki bunday chegara kitobda ham berilmagan
---

[&larr; 48. Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md) · [Mundarija](README.md)
