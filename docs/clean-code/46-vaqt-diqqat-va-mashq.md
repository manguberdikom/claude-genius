<!-- doc: clean-code | chapter: 46 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 46. Vaqt, diqqat va mashq (Time, Focus and Practice)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [46.1 Diqqat resursi va uni sarflash](#461-diqqat-resursi-va-uni-sarflash)
- [46.2 Oqim holati haqidagi afsona](#462-oqim-holati-haqidagi-afsona)
- [46.3 Uzilishlarni boshqarish](#463-uzilishlarni-boshqarish)
- [46.4 Pomodoro va vaqt bloklari](#464-pomodoro-va-vaqt-bloklari)
- [46.5 Ko'r yo'lak va botqoqdan chiqish](#465-kor-yolak-va-botqoqdan-chiqish)
- [46.6 Majlis: qachon chiqib ketish haqli](#466-majlis-qachon-chiqib-ketish-haqli)
- [46.7 Kod kata, dojo va ataylab mashq](#467-kod-kata-dojo-va-ataylab-mashq)
- [46.8 Debug vaqti: eng qimmat va eng kam hisobga olinadigan](#468-debug-vaqti-eng-qimmat-va-eng-kam-hisobga-olinadigan)
- [46.9 Amalda qo'llash](#469-amalda-qollash)

</details>


Kod sifati diqqat sifatiga bog'liq va diqqat cheklangan resurs. Bu bobda shu resursni boshqarish: uzilishlar, vaqt bloklari, ko'r yo'laklardan chiqish va ataylab mashq. Vaqtni taqsimlash yetakchi nuqtai nazaridan [arxitektor hujjatidagi](../architect/README.md) vaqtni taqsimlash bo'limida, o'rganish rejasi esa 38.12 da.

## 46.1 Diqqat resursi va uni sarflash

Kod yozish uchun kerakli diqqat kun bo'yi bir xil emas: u ertalab ko'p, kechga borib kamayadi, va har bir uzilishdan keyin tiklanishi uchun vaqt kerak. Shu resursni "diqqat-mana" deb tasavvur qilish foydali: u tugaganda kod yozishni davom ettirish zarar keltiradi (43.3).

Amaliy natijalar: eng murakkab ishni diqqat eng ko'p bo'lgan vaqtga qo'yish; diqqat tugaganda mexanik ishga o'tish (hujjat, kichik tuzatish, review); va kofe yoki irodani diqqat o'rniga ishlatmaslik.

## 46.2 Oqim holati haqidagi afsona

"Oqim" (flow) holati - vaqt sezilmaydigan, tez kod yozilayotgan holat - ko'pincha ideal deb ko'rsatiladi. Amalda u aralash natija beradi: tezlik oshadi, lekin umumiy ko'rinish torayadi. Oqimda yozilgan kod ko'pincha keyin refaktoring talab qiladi, chunki muallif katta rasmni ko'rmagan.

Amaliy tavsiya: oqimni maqsad qilmaslik; o'rniga qisqa, ongli siklda ishlash (TDD sikli, 31.1) va har sikldan keyin bir qadam orqaga chiqib qarash. Juftlikda ishlash oqimni tabiiy ravishda buzadi va bu uning foydasi (41.7).

## 46.3 Uzilishlarni boshqarish

Uzilish ikki narxga ega: uzilgan vaqt va kontekstni tiklash vaqti. Ikkinchisi ko'pincha kattaroq va u hech qayerda hisobga olinmaydi.

| Uzilish turi | Boshqarish usuli |
|---|---|
| Chat xabari | belgilangan vaqtlarda javob berish |
| "Bir daqiqaga" savol | "15 daqiqadan keyin bo'ladimi?" |
| Majlis | bloklangan ish vaqtini kalendarda belgilash |
| Incident | to'xtash shart, lekin kontekstni yozib qo'yish |
| O'z-o'zini uzish (brauzer) | muhit sozlamasi, telefon uzoqda |
| Review so'rovi | navbatga qo'yish, darhol emas |

Uzilishdan oldin kontekstni yozib qo'yish (bir-ikki qator: "shu yerda to'xtadim, keyingi qadam shu") tiklash vaqtini bir necha barobar qisqartiradi.

## 46.4 Pomodoro va vaqt bloklari

Pomodoro texnikasi: 25 daqiqa uzilmasdan ishlash, 5 daqiqa tanaffus; to'rt siklda uzun tanaffus. Uning asosiy foydasi vaqt o'lchash emas, **uzilishlardan himoya**: 25 daqiqa ichida hech narsaga javob berilmaydi.

Amaliy moslashtirish: 25 daqiqa ba'zi ishlar uchun qisqa (murakkab debug), shuning uchun 50/10 ham ishlaydi. Muhimi - blok ichida uzilish bo'lmasligi va blok oxirida ongli to'xtash.

## 46.5 Ko'r yo'lak va botqoqdan chiqish

**Ko'r yo'lak** (blind alley) - tanlangan yondashuv ishlamayotgani aniq bo'lgan holat. Professional javob: tan olish va qaytish. Sarflangan vaqt argument emas (sunk cost): u allaqachon ketgan.

**Botqoq** (marsh) - yondashuv ishlaydi, lekin sekin va qimmat; har bir qadam qiyinlashadi. Botqoq ko'r yo'lakdan xavfliroq, chunki unda qolish mumkin.

| Belgi | Harakat |
|---|---|
| Uch urinish, natija yo'q | to'xtash, boshqa yondashuvni ko'rib chiqish |
| Har bir tuzatish yangi xato beradi | yondashuvni qayta ko'rish |
| "Faqat yana bir soat" uch marta takrorlandi | tanaffus, keyin yangi ko'z bilan |
| Yechim tushunilmaydi, lekin ishlaydi | tushunmaguncha davom etmaslik (41.2) |
| Vaqt budjeti oshdi | to'xtash va yordam so'rash |

Eng arzon chiqish usuli - boshqa odamga tushuntirish. Ko'p holatda muammo tushuntirish paytida o'zi hal bo'ladi.

## 46.6 Majlis: qachon chiqib ketish haqli

Majlis vaqtni eng ko'p yo'qotadigan manba, lekin undan butunlay qochish ham ishlamaydi. Amaliy mezon: majlisda **sizdan** nimadir talab qilinmasa va siz ma'lumot olmasangiz, qatnashish keraksiz.

Qoidalar: kun tartibi bo'lmagan majlisga rozilik bermaslik; majlis maqsadi bajarilgach chiqib ketish haqli; va ko'p odam qatnashadigan uzun majlis o'rniga qisqa yozma yangilanish taklif qilish.

## 46.7 Kod kata, dojo va ataylab mashq

Mashq va ish bir narsa emas. Ishda natija muhim, mashqda **usul** muhim. Shu sababli professional ishdan tashqari mashq qiladi va mashqda ataylab noqulay narsalarni sinaydi.

| Shakl | Qanday |
|---|---|
| Kata | bir xil kichik masalani qayta-qayta yechish, har safar boshqa usulda |
| Ping-pong kata | juftlikda, biri test yozadi, ikkinchisi o'tkazadi |
| Randori | guruh bo'lib, navbat bilan klaviaturada |
| Dojo | jamoa uchun belgilangan mashq sessiyasi (haftada 1-2 soat) |
| Cheklovli mashq | "mouse ishlatmaslik", "`if` ishlatmaslik", "metod 3 qatordan oshmasin" |
| Ochiq kod o'qish | mashhur kutubxona kodini o'qib, qarorlarni tahlil qilish |

Klassik katalar: FizzBuzz, Roman Numerals, Bowling Game, Gilded Rose (refaktoring uchun), Bank OCR, Tennis Game. Gilded Rose ayniqsa foydali, chunki u aynan refaktoring mashqi uchun yozilgan.

## 46.8 Debug vaqti: eng qimmat va eng kam hisobga olinadigan

Debug vaqti rejada hech qachon ko'rinmaydi, lekin amalda ishning katta qismini oladi. Uni kamaytirish uchun ikkita eng samarali vosita bor va ikkisi ham oldindan ishlaydi: test (xato oynasi qisqaradi) va kichik qadamlar (xato manbasi aniq).

| Debug usuli | Samaradorlik |
|---|---|
| Xatoni takrorlaydigan test yozish | eng yuqori |
| `git bisect` bilan buzilgan commitni topish | yuqori (atomik commit kerak, 40.1) |
| Log va trace o'qish | yuqori (strukturali log kerak, 29.6) |
| Debugger bilan qadamlab yurish | o'rtacha |
| Boshqa odamga tushuntirish | yuqori |
| Kodni tasodifiy o'zgartirib ko'rish | eng past |

Debug vaqtini o'lchab borish foydali: u qancha ko'p bo'lsa, test va kuzatuvchanlikka investitsiya shuncha haqli.

## 46.9 Amalda qo'llash

- [ ] Bir hafta davomida kun bo'yi diqqat darajasini yozib borib, murakkab ishni eng yuqori vaqtga ko'chiring.
- [ ] Kalendarda kuniga kamida ikki soat bloklangan ish vaqtini belgilang va uni himoya qiling.
- [ ] Uzilishdan oldin kontekstni yozib qoldirish odatini joriy qiling.
- [ ] Pomodoro yoki 50/10 siklini bir hafta sinab, natijani baholang.
- [ ] Har bir murakkab vazifa uchun oldindan vaqt budjeti belgilab, oshganda to'xtash qoidasini qo'llang.
- [ ] Kun tartibi yo'q majlislarga rozilik bermaslik qoidasini joriy qiling.
- [ ] Jamoa uchun haftada bir soatlik dojo tashkil qilib, Gilded Rose katasidan boshlang.
- [ ] Debug vaqtini bir oy davomida o'lchab, eng ko'p vaqt ketgan sohaga test va log qo'shing.

---

[&larr; 45. Baholash, muddat va bosim](45-baholash-muddat-va-bosim.md) · [Mundarija](README.md) · [47. Birgalikda ishlash va o'rgatish &rarr;](47-birgalikda-ishlash-va-orgatish.md)
