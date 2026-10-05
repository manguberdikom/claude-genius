<!-- doc: clean-code | chapter: 1 | part: I. Toza kodning asosi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 1. Toza kod nima va nega qimmat (What Clean Code Is)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [1.1 Toza kodning ishlaydigan ta'rifi](#11-toza-kodning-ishlaydigan-tarifi)
- [1.2 Buzilgan deraza nazariyasi va kod bazasining eskirishi](#12-buzilgan-deraza-nazariyasi-va-kod-bazasining-eskirishi)
- [1.3 "Keyin tozalaymiz" nega hech qachon kelmaydi](#13-keyin-tozalaymiz-nega-hech-qachon-kelmaydi)
- [1.4 Skaut qoidasi va imkoniyatli refaktoring](#14-skaut-qoidasi-va-imkoniyatli-refaktoring)
- [1.5 Toza kod va tez kod qarama-qarshi emas](#15-toza-kod-va-tez-kod-qarama-qarshi-emas)
- [1.6 Toza kodning o'lchanadigan belgilari](#16-toza-kodning-olchanadigan-belgilari)
- [1.7 Qoida, evristika va did farqi](#17-qoida-evristika-va-did-farqi)
- [1.8 Toza kodni kim uchun yozamiz](#18-toza-kodni-kim-uchun-yozamiz)
- [1.9 Bu hujjat qolgan to'rttasi bilan qanday bo'linadi](#19-bu-hujjat-qolgan-torttasi-bilan-qanday-bolinadi)
- [1.10 Amalda qo'llash](#110-amalda-qollash)

</details>


Toza kod haqidagi suhbat did haqidagi bahsga aylanib ketsa, u foydasiz. Shuning uchun bu bobda toza kodning o'lchanadigan ta'rifi beriladi: kod toza bo'lsa, uni o'qish tezligi va uni o'zgartirishdagi ishonch oshadi. Qolgan 48 bob shu ikki o'lchovni oshiradigan aniq qoidalar.

## 1.1 Toza kodning ishlaydigan ta'rifi

Toza kodni ta'riflashning eng ishonchli yo'li uni kuzatiladigan xatti-harakat orqali belgilash. Kod toza, agar uni birinchi marta ko'rgan odam debuggersiz o'qib tushunsa; o'zgartirish kiritishda u nimani buzishi mumkinligini oldindan ayta olsa; va o'zgartirishdan keyin test uni tasdiqlasa yoki rad etsa. Uchta shartning hech biri estetika haqida emas.

Shundan amaliy natija chiqadi. "Menga bu uslub yoqmaydi" argumenti toza kod argumenti emas. "Bu metodni o'qish uchun ikkita boshqa faylni ochish kerak" - toza kod argumenti, chunki o'qish narxini oshiradi. "Bu nomni o'zgartirsa, uch joyda kutilmagan xatti-harakat chiqadi" - toza kod argumenti, chunki o'zgartirish ishonchini pasaytiradi.

| Savol | Iflos kod | Toza kod |
|---|---|---|
| Bu metod nima qiladi? | Kodni o'qib taxmin qilaman | Nomi aytadi |
| Nimani buzishim mumkin? | Bilmayman | Imzo va test aytadi |
| Qayerdan boshlanadi? | Qidirish kerak | Kirish nuqtasi aniq |
| Xato bo'lsa nima bo'ladi? | `null` qaytadi, balki | Istisno turi e'lon qilingan |
| O'zgartirsam kim biladi? | Hech kim | Test yiqiladi |

## 1.2 Buzilgan deraza nazariyasi va kod bazasining eskirishi

Buzilgan deraza nazariyasi kod bazasiga aniq ko'chadi: bitta tuzatilmagan hid keyingi hidga ruxsat beradi. Mexanizm psixologik, lekin oqibati o'lchanadi. Kodda 30 ta `// TODO` bo'lsa, 31-chisini qo'shish arzon ko'rinadi. Bitta 2000 qatorli sinf bo'lsa, ikkinchisini yaratish qiyin bo'lmaydi, chunki standart allaqachon shu.

Shu sababli toza kod intizomi katta tozalash kampaniyalaridan emas, kichik va to'xtovsiz tuzatishlardan yig'iladi. Har bir tegilgan fayl bir nuqta yaxshilanib qolsa, kod bazasi yaxshilanish yo'nalishida turadi. Hech narsa tuzatilmasa, u faqat bitta yo'nalishda - pastga - qarab ketadi.

## 1.3 "Keyin tozalaymiz" nega hech qachon kelmaydi

"Hozir ishlatib yuboraylik, keyin tozalaymiz" gapi iqtisodiy jihatdan ishlamaydi, chunki tozalashni haqli qiladigan vaqt hech qachon paydo bo'lmaydi. Keyingi hafta yangi talab keladi, keyingi oy reliz bo'ladi. Qarzning foizi esa darhol to'lanadi: har bir yangi xususiyat iflos kod ustiga qurilib, uni o'chirish narxini oshiradi.

Amalda qoida teskari ishlaydi: tozalash ishning qismi, alohida ish emas. Agar vazifaga 6 soat ketadigan bo'lsa, u 6 soat ichida toza holatda tugashi kerak, 4 soat ishlaydigan va keyin 2 soat qarz holatida emas. Vaqt yetmasa, qamrov qisqartiriladi, sifat emas ([45-bob](45-baholash-muddat-va-bosim.md)).

## 1.4 Skaut qoidasi va imkoniyatli refaktoring

Skaut qoidasi (Boy Scout Rule): lagerdan ketganda uni topganingdan tozaroq qoldir. Kodga tatbiqi aniq: har bir PR da tegilgan faylda kamida bitta kichik yaxshilanish bo'lsin. Nomni aniqlashtirish, bir shartni nomlash, bitta o'lik metodni o'chirish, bitta magic number ni konstanta qilish.

Muhim cheklov bor: imkoniyatli tozalash **o'sha PR ning qamrovi ichida** qolishi kerak. 40 qatorli xato tuzatish 600 qatorli refaktoringga aylanib ketsa, review sifati tushadi va reliz kechadi. Qoida: tozalash tegilgan fayllarda va alohida commitda bo'ladi; katta refaktoring alohida PR ga chiqadi (13.6 va 38.4).

## 1.5 Toza kod va tez kod qarama-qarshi emas

"Toza kod sekin ishlaydi" da'vosi deyarli har doim o'lchanmagan. Haqiqat shunday: ishlash muammosi odatda 2-3 joyda to'planadi va o'lchov bilan topiladi; qolgan 97% kodning tezligi ahamiyatsiz. Toza kod esa shu 3 joyni topishni osonlashtiradi, chunki chegaralar aniq.

Shu bilan birga, toza kod "samarasiz kod" degani emas. Bu hujjatda tezlikka ta'sir qiladigan aniq qoidalar bor: `StringBuilder` qachon kerak (21.2), avtoboxing narxi (20.6), oqim va sikl tanlovi (7.7), N+1 va keraksiz fetch (28.4). Qoida: oldin to'g'ri va o'qiladigan, keyin o'lchov, keyin maqsadli optimizatsiya.

## 1.6 Toza kodning o'lchanadigan belgilari

Toza kod haqida bahsni o'lchovga ko'chirish mumkin. Quyidagi ko'rsatkichlar kod bazasining holatini did bilan emas, son bilan ko'rsatadi.

| O'lchov | Qanday olinadi | Ogohlantirish chegarasi |
|---|---|---|
| Yangi odamning birinchi PR gacha vaqti | onboarding kuzatuvi | 2 haftadan ko'p |
| Bitta o'zgarish tekkan fayllar soni | `git show --stat` o'rtachasi | 10 fayldan ko'p |
| Eng katta sinf uzunligi | `wc -l` reytingi | 500 qatordan ko'p |
| Public metodlardagi `String` parametrlar ulushi | grep yoki ArchUnit | yuqori ulush |
| Testsiz o'zgargan fayllar ulushi | coverage diff | 0 dan katta |
| PR dagi "nima qilmoqchi edingiz" savollari soni | review tarixi | PR da 2 dan ko'p |
| Reverted commitlar ulushi | `git log --grep=Revert` | 2% dan ko'p |
| Bir xil review izohining takrorlanishi | review tarixi | har haftada qaytsa |

## 1.7 Qoida, evristika va did farqi

Uch darajani ajratish bahsni qisqartiradi. **Qoida** - mashina tekshiradi va muhokama qilinmaydi: formatlash, import tartibi, `equals`/`hashCode` juftligi, resursni yopish. **Evristika** - odatda to'g'ri, lekin istisnosi bor: "funksiya 20 qatordan oshmasin". **Did** - shaxsiy va review da vaqt sarflashga arzimaydi: o'zgaruvchi nomining ohangi, qavs joylashuvi (allaqachon formatter hal qilgan).

Jamoada eng ko'p vaqt shu uchlik aralashganda yo'qoladi. Yechim: qoidalarni CI ga ko'chirish ([42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md)), evristikalarni hujjatda yozib qo'yish ([48-bob](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)), did haqida bahsni to'xtatish.

## 1.8 Toza kodni kim uchun yozamiz

Toza kodning adresati aniq va u siz emas. U quyidagi odam: domenni yarim biladi, shu faylni birinchi marta ochadi, vaqti kam, va ehtimol production incident vaqtida o'qiyapti. Har bir qarorni shu odamni ko'z oldiga keltirib qabul qilish kerak.

Bu adresat ikkita amaliy natija beradi. Birinchi, kontekst kodda bo'lishi kerak, chatda yoki sizning xotirangizda emas. Ikkinchi, "men bilaman, shuning uchun tushunarli" argumenti kuchsiz: o'quvchi sizning bilimingizga ega emas.

## 1.9 Bu hujjat qolgan to'rttasi bilan qanday bo'linadi

Chegarani bilib turish takrorlanishni yo'qotadi va qidirishni tezlashtiradi.

| Savol | Qaysi hujjat |
|---|---|
| Bu nomni qanday yozaman? | shu hujjat, 2-3 bob |
| Nomni domen tilidan qanday olaman? | [arxitektor hujjatidagi](../architect/README.md) nomlash bo'limi |
| Bu yerda qaysi pattern kerak? | [patternlar hujjati](../patterns/README.md) |
| SOLID nimani talab qiladi? | [patternlar hujjatidagi](../patterns/README.md) dizayn printsiplari bo'limi |
| Bu anti-pattern nomi nima? | [patternlar hujjatidagi](../patterns/README.md) anti-patternlar bo'limi |
| Chegarani qayerdan o'tkazaman? | [arxitektor hujjatidagi](../architect/README.md) chegara bo'limi |
| Bu testni qanday yozaman? | [testlash qo'llanmasi](../testing/README.md) |
| Test kodi toza ko'rinishi kerak? | shu hujjat, [30-bob](30-test-kodi-ham-ishlab-chiqarish-kodi.md) |
| Sonar nega shikoyat qilyapti? | [SonarQube hujjati](../sonarqube/README.md) |
| Boshqa odamning diffida nimani ko'raman? | [review hujjati](../code-review/README.md) |
| Bu hidni qanday refaktoring qilaman? | shu hujjat, 32-38 bob |

## 1.10 Amalda qo'llash

- [ ] Kod bazasida 1.6 jadvalidagi sakkiz o'lchovni bir marta hisoblab, bugungi holatni yozib qo'ying.
- [ ] Eng katta 10 ta faylni `wc -l` bilan topib, ro'yxatni jamoaga ko'rsating va keyingi chorak maqsadini belgilang.
- [ ] Jamoa bilan qoida/evristika/did ajratimini kelishib, qoidalar ro'yxatini CI ga ko'chirish rejasini tuzing.
- [ ] Keyingi 10 ta PR da skaut qoidasini qo'llang: har birida tegilgan faylda bitta nomli yaxshilanish bo'lsin.
- [ ] "Keyin tozalaymiz" deb qoldirilgan joylarni bitta ro'yxatga yig'ib, har biriga egalik va muddat qo'ying.
- [ ] Review da "menga yoqmaydi" turidagi izohlarni to'xtatish uchun formatterni majburiy qiling ([13-bob](13-formatlashni-avtomatlashtirish-va-diff.md)).
- [ ] Yangi odamning birinchi haftasida yozib olgan savollarini to'plab, javobi kodda yo'q bo'lganlarini kodga ko'chiring.
- [ ] Ishlash haqidagi har bir da'voni o'lchovsiz qabul qilmaslikni jamoa kelishuviga kiriting.

---

[Mundarija](README.md) · [2. Nomlash qoidalari: maqsadni ochib beruvchi nom &rarr;](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md)
