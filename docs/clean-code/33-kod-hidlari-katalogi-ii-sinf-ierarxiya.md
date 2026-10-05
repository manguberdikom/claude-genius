<!-- doc: clean-code | chapter: 33 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik (Code Smells II)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [33.1 Tarqoq o'zgarish (Divergent Change)](#331-tarqoq-ozgarish-divergent-change)
- [33.2 Ma'lumot sinfi (Data Class)](#332-malumot-sinfi-data-class)
- [33.3 Noo'rin yaqinlik (Inappropriate Intimacy / Insider Trading)](#333-noorin-yaqinlik-inappropriate-intimacy--insider-trading)
- [33.4 Muqobil sinflar, turli interfeyslar (Alternative Classes with Different Interfaces)](#334-muqobil-sinflar-turli-interfeyslar-alternative-classes-with-different-interfaces)
- [33.5 Rad etilgan meros (Refused Bequest)](#335-rad-etilgan-meros-refused-bequest)
- [33.6 Parallel ierarxiyalar (Parallel Inheritance Hierarchies)](#336-parallel-ierarxiyalar-parallel-inheritance-hierarchies)
- [33.7 To'liq bo'lmagan kutubxona sinfi (Incomplete Library Class)](#337-toliq-bolmagan-kutubxona-sinfi-incomplete-library-class)
- [33.8 Haddan tashqari ko'p ma'lumot (Too Much Information)](#338-haddan-tashqari-kop-malumot-too-much-information)
- [33.9 Izchilsizlik (Inconsistency)](#339-izchilsizlik-inconsistency)
- [33.10 Keraksizlik (Clutter)](#3310-keraksizlik-clutter)
- [33.11 Sun'iy bog'liqlik (Artificial Coupling)](#3311-suniy-bogliqlik-artificial-coupling)
- [33.12 Noto'g'ri joylashgan javobgarlik (Misplaced Responsibility)](#3312-notogri-joylashgan-javobgarlik-misplaced-responsibility)
- [33.13 Noo'rin statik (Inappropriate Static)](#3313-noorin-statik-inappropriate-static)
- [33.14 Bazaviy sinf vorisga bog'liq (Base Class Depending on Derivatives)](#3314-bazaviy-sinf-vorisga-bogliq-base-class-depending-on-derivatives)
- [33.15 Majburiy sozlash kodi (Required Setup Code)](#3315-majburiy-sozlash-kodi-required-setup-code)
- [33.16 Kombinatorik portlash (Combinatorial Explosion)](#3316-kombinatorik-portlash-combinatorial-explosion)
- [33.17 Amalda qo'llash](#3317-amalda-qollash)

</details>


Bu bob sinf darajasidagi va sinflar orasidagi hidlarni qamrab oladi. God Object, Big Ball of Mud, Circular Dependency va boshqa arxitektura darajasidagi anti-patternlar [patternlar hujjatidagi](../patterns/README.md) anti-patternlar bo'limida; bu yerda ularning kod darajasidagi qardoshlari.

## 33.1 Tarqoq o'zgarish (Divergent Change)

**Belgisi**: bitta sinf turli sabablarga ko'ra o'zgaradi - bugun soliq qoidasi uchun, ertaga ma'lumot bazasi sxemasi uchun, indinga JSON formati uchun.

**Nega muammo**: har bir o'zgarish boshqa sabablar bilan yozilgan kodga tegadi va regressiya xavfi oshadi. Bu yagona javobgarlik printsipining buzilishi ([patternlar hujjatidagi](../patterns/README.md) yagona javobgarlik printsipi).

**Tuzatish**: Extract Class, Split Phase ([36-bob](36-refaktoring-harakatlari-katalogi-ii-malumot.md)). Aniqlash usuli: `git log` bilan sinf o'zgarishlarining sabablarini sanash ([arxitektor hujjatidagi](../architect/README.md) modul chegarasini o'tkazish bo'limi chegara aniqlash texnikasini beradi).

## 33.2 Ma'lumot sinfi (Data Class)

**Belgisi**: sinfda faqat maydonlar, getter va setter lar bor; xatti-harakat yo'q. Shu sinf bilan bog'liq mantiq boshqa sinflarda tarqalgan.

**Nega muammo**: Anemik domen modelining kichik shakli ([patternlar hujjatidagi](../patterns/README.md) anemik domen modeli anti-patterni). Har bir foydalanuvchi o'z nusxasidagi qoidani yozadi va qoidalar bir-biridan farq qiladi.

**Tuzatish**: Move Function (mantiqni ma'lumot egasiga ko'chirish), Encapsulate Record, Remove Setting Method. Eslatma: DTO va `record` chegarada ataylab ma'lumot sinfi bo'ladi (14.5) - bu hid emas.

## 33.3 Noo'rin yaqinlik (Inappropriate Intimacy / Insider Trading)

**Belgisi**: ikki sinf bir-birining ichki maydonlari va private holatiga haddan tashqari ko'p murojaat qiladi; ichma-ich sinflar yoki `package-private` kirish orqali bir-birini "biladi".

**Nega muammo**: ikki sinf aslida bitta, lekin ikkiga bo'lingan; yoki chegara noto'g'ri joyda. Birini o'zgartirish ikkinchisini buzadi.

**Tuzatish**: Move Function / Move Field (sinflarni to'g'ri taqsimlash), Extract Class (umumiy qismni ajratish), Hide Delegate, yoki ikki sinfni birlashtirish (Inline Class).

## 33.4 Muqobil sinflar, turli interfeyslar (Alternative Classes with Different Interfaces)

**Belgisi**: ikki sinf bir xil ish qiladi, lekin metod nomlari va imzolari boshqa: `SmsSender.send(to, text)` va `EmailGateway.deliverMessage(address, body, subject)`.

**Nega muammo**: ularni almashtirib ishlatish imkonsiz, shuning uchun har bir chaqiruv joyi `if` bilan shoxlanadi.

**Tuzatish**: Change Function Declaration (nomlarni moslashtirish), keyin Extract Superclass yoki umumiy interfeys ajratish. Agar biri uchinchi tomon sinfi bo'lsa - adapter ([patternlar hujjati](../patterns/README.md)).

## 33.5 Rad etilgan meros (Refused Bequest)

17.6 da ko'rilgan. Hid sifatida belgisi: voris sinf meros olgan metodlarning bir qismini ishlatmaydi yoki `UnsupportedOperationException` tashlaydi.

**Tuzatish**: Push Down Method / Push Down Field (keraksizni pastga tushirish), Replace Superclass with Delegate (17.9), yoki interfeysni bo'lish.

## 33.6 Parallel ierarxiyalar (Parallel Inheritance Hierarchies)

**Belgisi**: bitta ierarxiyaga voris sinf qo'shilganda, ikkinchi ierarxiyaga ham mos sinf qo'shish kerak bo'ladi: `CardPayment`/`CardPaymentValidator`, `BankPayment`/`BankPaymentValidator`.

**Nega muammo**: ikki ierarxiya bir xil o'qni bo'yicha o'sadi va ularni sinxron ushlash qo'lda bajariladi; bittasi doim esdan chiqadi.

**Tuzatish**: ikkinchi ierarxiyani birinchisiga ko'chirish (validator mantiqini `Payment` ichiga), yoki `sealed` ierarxiya va pattern matching bilan bitta o'qga qisqartirish.

## 33.7 To'liq bo'lmagan kutubxona sinfi (Incomplete Library Class)

**Belgisi**: uchinchi tomon sinfi kerakli metodni bermaydi va kod bazasida uning atrofida yordamchi funksiyalar tarqalgan.

**Nega muammo**: bir xil yordamchi bir necha joyda yoziladi va ular bir-biridan farq qiladi.

**Tuzatish**: yordamchilarni bitta `final` utility sinfga yoki wrapper ga yig'ish (14.8, 18.3). Kutubxona turini domen kodida tarqatmaslik ham shu yechimning qismi.

## 33.8 Haddan tashqari ko'p ma'lumot (Too Much Information)

**Belgisi**: sinf yoki interfeys 20+ public metod beradi; paketdan o'nlab tur eksport qilinadi; `public` modifikatori standart tanlov.

**Nega muammo**: keng interfeys ko'p bog'liqlik yaratadi va har bir public element kelajakdagi majburiyat ([arxitektor hujjatidagi](../architect/README.md) orqaga moslik bo'limi).

**Tuzatish**: ko'rinishni toraytirish (14.6), interfeysni bo'lish, paketdan faqat API turlarini chiqarish (26.2).

## 33.9 Izchilsizlik (Inconsistency)

**Belgisi**: bir xil narsa kod bazasining turli joylarida turlicha qilinadi - bir joyda `Optional`, boshqa joyda `null`; bir joyda konstruktor inyeksiyasi, boshqa joyda maydon; bir joyda `find`, boshqa joyda `get`.

**Nega muammo**: o'quvchi har bir joyda qaytadan o'ylashi kerak va taxminlari xato bo'ladi.

**Tuzatish**: konvensiyani hujjatlashtirish ([48-bob](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)), keyin uni mashinaga topshirish ([42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md)). Izchilsizlik eng tez tarqaladigan hid, chunki har bir yangi kod mavjud namunaga qaraydi.

## 33.10 Keraksizlik (Clutter)

**Belgisi**: hech narsa qilmaydigan elementlar - bo'sh konstruktor, ishlatilmaydigan maydon, hech kim chaqirmaydigan metod, mazmunsiz izoh, ishlatilmaydigan import, `default` konstruktorni oshkor yozish.

**Nega muammo**: har bir keraksiz element o'quvchidan "bu nega bor?" savolini talab qiladi.

**Tuzatish**: Remove Dead Code ([35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md)). O'lik kodni topish uchun IDE inspeksiyasi, `-Xlint`, va kod qamrovi hisoboti ishlatiladi ([SonarQube hujjatidagi](../sonarqube/README.md) maintainability va nomlash xato katalogi o'lik kod katalogini beradi).

## 33.11 Sun'iy bog'liqlik (Artificial Coupling)

**Belgisi**: bir-biriga tegishli bo'lmagan narsalar bir joyda turadi - umumiy enum "umumiy" paketda, ichki sinf boshqa modulda e'lon qilingan, konstanta tasodifiy sinfda.

**Nega muammo**: bog'liqlik grafi sabab bilan emas, qulaylik bilan qurilgan. Har bir import keraksiz bog'lanish qo'shadi.

**Tuzatish**: Move Function / Move Field / Move Class - elementni eng ko'p ishlatiladigan joyga ko'chirish.

## 33.12 Noto'g'ri joylashgan javobgarlik (Misplaced Responsibility)

**Belgisi**: funksiya nomi bilan sinf nomi mos kelmaydi; `OrderService.calculateTax()`, `UserController.sendEmail()`, `PaymentRepository.formatReceipt()`.

**Nega muammo**: o'quvchi funksiyani topa olmaydi, chunki u mantiqan boshqa joyda bo'lishi kerak. Natijada funksiya ikkinchi marta yoziladi.

**Tuzatish**: Move Function. Aniqlash savoli: "bu funksiya qaysi ma'lumotga eng ko'p murojaat qiladi?" - javob uning uyi ([patternlar hujjatidagi](../patterns/README.md) ma'lumot egasi (Information Expert) printsipi , Information Expert).

## 33.13 Noo'rin statik (Inappropriate Static)

**Belgisi**: statik metod aslida polimorfizm talab qiladi - `Money.calculateTax(money, region)` har bir mintaqa uchun boshqa hisob qilsa, u statik bo'lmasligi kerak.

**Nega muammo**: statik metodni override qilib bo'lmaydi va mock qilish qiyin (31.5). Kelajakdagi variant qo'shish uchun butun chaqiruv zanjirini o'zgartirish kerak.

**Tuzatish**: statik metodni instans metodiga aylantirish, keyin kerak bo'lsa strategiya interfeysiga chiqarish. Haqiqiy sof funksiyalar (`Math.abs`, `Ibans.isValid`) statik qoladi (14.8).

## 33.14 Bazaviy sinf vorisga bog'liq (Base Class Depending on Derivatives)

17.5 da ko'rilgan. Hid sifatida belgisi: bazaviy sinfda voris sinf nomlari, `instanceof` tekshiruvlari yoki voris sinflarga mos `switch`.

**Tuzatish**: abstrakt metod kiritish (Replace Conditional with Polymorphism), yoki bazaviy sinfni interfeysga aylantirish.

## 33.15 Majburiy sozlash kodi (Required Setup Code)

**Belgisi**: obyektni ishlatishdan oldin bir necha metodni ma'lum tartibda chaqirish kerak (6.9); yoki testda har safar 20 qatorlik sozlash yoziladi.

**Nega muammo**: tartib hech qayerda majburlanmagan va u buzilsa xato uzoqda chiqadi.

**Tuzatish**: konstruktorda to'liq qurish (14.9), builder (16.5), yoki "o'tkazish" uslubi (6.9). Testda esa builder va object mother (30.3).

## 33.16 Kombinatorik portlash (Combinatorial Explosion)

**Belgisi**: bir xil ishning har bir kombinatsiyasi uchun alohida metod yoki sinf: `findByCustomer`, `findByCustomerAndStatus`, `findByCustomerAndStatusAndDate`, va h.k. (28.5).

**Nega muammo**: har bir yangi o'lcham metod sonini ikki barobar oshiradi.

**Tuzatish**: Introduce Parameter Object (mezon obyekti), Specification pattern, yoki builder bilan so'rov qurish.

## 33.17 Amalda qo'llash

- [ ] Eng ko'p o'zgargan 10 sinf uchun `git log` dan o'zgarish sabablarini sanab, tarqoq o'zgarishni aniqlang.
- [ ] Faqat getter/setter dan iborat domen sinflarini topib, ularga tegishli mantiqni ko'chiring.
- [ ] Bir-birining private holatiga murojaat qiladigan sinf juftliklarini topib, chegarani qayta chizing.
- [ ] Bir xil vazifani bajaradigan, lekin turli imzolarga ega sinflarni umumiy interfeysga keltiring.
- [ ] Parallel ierarxiyalarni topib, ikkinchisini birinchisiga qo'shing yoki `sealed` ierarxiyaga o'tkazing.
- [ ] 20 dan ko'p public metodi bor sinf va interfeyslarni ro'yxatlab, ko'rinishni toraytiring.
- [ ] Izchilsizlik ro'yxatini tuzib (`Optional`/`null`, nomlash, inyeksiya), har biri uchun bitta konvensiya kelishib oling.
- [ ] Ishlatilmaydigan maydon, metod va importlarni IDE inspeksiyasi bilan topib o'chiring.

---

[&larr; 32. Kod hidlari katalogi I: nom, funksiya, ma'lumot](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md) · [Mundarija](README.md) · [34. Toza kod evristikalarining to'liq ro'yxati &rarr;](34-toza-kod-evristikalarining-toliq-royxati.md)
