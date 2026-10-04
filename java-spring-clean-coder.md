# Toza kod yozuvchining qoidalari: Java, Spring, PostgreSQL

Bu hujjat toza kodning **qoidalar to'plami**. Arxitektura qarorlari, pattern katalogi va
test texnikasi boshqa hujjatlarda turadi; bu yerda faqat bitta savolga javob beriladi:
klaviatura ostida tug'ilayotgan shu qator toza yoki yo'q.

Hujjat beshlikning bir qismi va qasddan takrorlanmaydi:

- `java-spring-design-patterns.md` — pattern katalogi, SOLID va GRASP printsiplari, 83 ta anti-pattern.
- `java-spring-architect-mindset.md` — qaror, abstraksiya, chegara, murakkablik, JVM va PostgreSQL mexanikasi.
- `java-spring-testing-handbook.md` — test strategiyasi, piramida, Testcontainers, CI pipeline.
- `java-spring-sonarqube.md` — statik tahlil, quality gate, coverage, Sonar xato katalogi.

Arxitektor va pattern hujjatlarida yoritilgan mavzular bu yerda qayta yozilmaydi, faqat
nomi bilan havola qilinadi: masalan nomni domen tilidan olish, kognitiv yuk, erta qaytish,
izohning "nega" qoidasi, SOLID, GRASP, DRY, KISS, YAGNI, Demeter qonuni, God Object va
qolgan anti-patternlar.

Bu yerda ularning **qolgan qismi** bor: nomlashning to'liq qoidalar to'plami, funksiya va
argument qoidalari, shart va sikl gigiyenasi, izohlarning to'liq katalogi, formatlash,
obyekt shartnomalari, xato bilan ishlash, Java va Spring kodining mayda qoidalari, test
kodining tozaligi, hid va refaktoring kataloglari, kod bazasi gigiyenasi va professional
intizom.

Har bob `Amalda qo'llash` tekshiruv ro'yxati bilan tugaydi. Oxirgi ikki bob tezkor
ma'lumotnoma va o'z-o'zini baholash uchun.

## Mundarija

**[I. Toza kodning asosi](#i-toza-kodning-asosi)**

- [1. Toza kod nima va nega qimmat (What Clean Code Is)](#1-toza-kod-nima-va-nega-qimmat-what-clean-code-is)
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
- [2. Nomlash qoidalari: maqsadni ochib beruvchi nom (Naming: Intention-Revealing Names)](#2-nomlash-qoidalari-maqsadni-ochib-beruvchi-nom-naming-intention-revealing-names)
  - [2.1 Nom javob berishi kerak bo'lgan uchta savol](#21-nom-javob-berishi-kerak-bolgan-uchta-savol)
  - [2.2 Yolg'on ma'lumot beradigan nom](#22-yolgon-malumot-beradigan-nom)
  - [2.3 Ma'noli farq: `a1`, `a2`, `Info` va `Data`](#23-manoli-farq-a1-a2-info-va-data)
  - [2.4 Shovqin so'zlar: `Info`, `Data`, `Object`, `Variable`, `The`](#24-shovqin-sozlar-info-data-object-variable-the)
  - [2.5 Talaffuz qilinadigan nom](#25-talaffuz-qilinadigan-nom)
  - [2.6 Qidiriladigan nom va bir harfli o'zgaruvchi chegarasi](#26-qidiriladigan-nom-va-bir-harfli-ozgaruvchi-chegarasi)
  - [2.7 Kodlash va prefikslar: Hungarian notation, `m_`, `I` prefiksi](#27-kodlash-va-prefikslar-hungarian-notation-m_-i-prefiksi)
  - [2.8 Aqliy tarjimani talab qiladigan nom](#28-aqliy-tarjimani-talab-qiladigan-nom)
  - [2.9 Sinf nomi ot, metod nomi fe'l, getter konvensiyasi](#29-sinf-nomi-ot-metod-nomi-fel-getter-konvensiyasi)
  - [2.10 Hazil, jargon va madaniy havolalar](#210-hazil-jargon-va-madaniy-havolalar)
  - [2.11 Bitta tushunchaga bitta so'z](#211-bitta-tushunchaga-bitta-soz)
  - [2.12 So'z o'yini qilmaslik](#212-soz-oyini-qilmaslik)
  - [2.13 Yechim domeni va muammo domeni nomlari](#213-yechim-domeni-va-muammo-domeni-nomlari)
  - [2.14 Kontekst qo'shish va ortiqcha kontekst qo'shmaslik](#214-kontekst-qoshish-va-ortiqcha-kontekst-qoshmaslik)
  - [2.15 Nom uzunligi qamrovga mutanosib](#215-nom-uzunligi-qamrovga-mutanosib)
  - [2.16 Amalda qo'llash](#216-amalda-qollash)
- [3. Nom turlari bo'yicha aniq konvensiyalar (Naming Conventions by Kind)](#3-nom-turlari-boyicha-aniq-konvensiyalar-naming-conventions-by-kind)
  - [3.1 Mantiqiy nomlar: `is`, `has`, `can`, `should` va inkor tuzog'i](#31-mantiqiy-nomlar-is-has-can-should-va-inkor-tuzogi)
  - [3.2 To'plam, massiv va oqim nomlari](#32-toplam-massiv-va-oqim-nomlari)
  - [3.3 Birlik nomda: `timeoutMs`, `sizeBytes`, `priceMinor`](#33-birlik-nomda-timeoutms-sizebytes-priceminor)
  - [3.4 Konstanta, `static final` va enum a'zolari](#34-konstanta-static-final-va-enum-azolari)
  - [3.5 Enum turi va holat nomlari](#35-enum-turi-va-holat-nomlari)
  - [3.6 Interfeys va implementatsiya nomlari: `Impl` qachon haqli](#36-interfeys-va-implementatsiya-nomlari-impl-qachon-haqli)
  - [3.7 Abstrakt sinf va `Abstract` prefiksi](#37-abstrakt-sinf-va-abstract-prefiksi)
  - [3.8 Generik tur parametrlari](#38-generik-tur-parametrlari)
  - [3.9 Metod nomi va qaytish turi muvofiqligi](#39-metod-nomi-va-qaytish-turi-muvofiqligi)
  - [3.10 Istisno sinflari nomlari](#310-istisno-sinflari-nomlari)
  - [3.11 Paket, modul va artefakt nomlari](#311-paket-modul-va-artefakt-nomlari)
  - [3.12 Test metodi va test sinfi nomlari](#312-test-metodi-va-test-sinfi-nomlari)
  - [3.13 Fayl, resurs va konfiguratsiya kaliti nomlari](#313-fayl-resurs-va-konfiguratsiya-kaliti-nomlari)
  - [3.14 Jamoa lug'ati va uni majburlash](#314-jamoa-lugati-va-uni-majburlash)
  - [3.15 Nomni o'zgartirish intizomi](#315-nomni-ozgartirish-intizomi)
  - [3.16 Amalda qo'llash](#316-amalda-qollash)

**[II. Funksiya va boshqaruv oqimi](#ii-funksiya-va-boshqaruv-oqimi)**

- [4. Funksiya: kichiklik va bitta ish (Functions: Small and Doing One Thing)](#4-funksiya-kichiklik-va-bitta-ish-functions-small-and-doing-one-thing)
  - [4.1 Birinchi qoida: kichik; ikkinchi qoida: yana kichikroq](#41-birinchi-qoida-kichik-ikkinchi-qoida-yana-kichikroq)
  - [4.2 "Bitta ish qiladi" ni qanday tekshirish](#42-bitta-ish-qiladi-ni-qanday-tekshirish)
  - [4.3 Bo'limlari bor funksiya bitta ish qilmaydi](#43-bolimlari-bor-funksiya-bitta-ish-qilmaydi)
  - [4.4 Pastga tushish qoidasi va gazeta metaforasi](#44-pastga-tushish-qoidasi-va-gazeta-metaforasi)
  - [4.5 Funksiyadan funksiya chiqarish mexanikasi](#45-funksiyadan-funksiya-chiqarish-mexanikasi)
  - [4.6 Funksiya nomi uzunligi va aniqligi](#46-funksiya-nomi-uzunligi-va-aniqligi)
  - [4.7 Funksiya qaytish nuqtalari: bitta `return` afsonasi](#47-funksiya-qaytish-nuqtalari-bitta-return-afsonasi)
  - [4.8 Funksiya ichidagi bo'sh joy, blok va qavs](#48-funksiya-ichidagi-bosh-joy-blok-va-qavs)
  - [4.9 Yordamchi funksiyalar soni va joylashuvi](#49-yordamchi-funksiyalar-soni-va-joylashuvi)
  - [4.10 Funksiyani birinchi urinishda toza yozish mumkin emas](#410-funksiyani-birinchi-urinishda-toza-yozish-mumkin-emas)
  - [4.11 Amalda qo'llash](#411-amalda-qollash)
- [5. Funksiya argumentlari (Function Arguments)](#5-funksiya-argumentlari-function-arguments)
  - [5.1 Argument soni: nol, bir, ikki, uch va undan keyin](#51-argument-soni-nol-bir-ikki-uch-va-undan-keyin)
  - [5.2 Monadik shakllar: so'rov, o'zgartirish, hodisa](#52-monadik-shakllar-sorov-ozgartirish-hodisa)
  - [5.3 Flag argumenti va uni ikki funksiyaga bo'lish](#53-flag-argumenti-va-uni-ikki-funksiyaga-bolish)
  - [5.4 Tanlov (selector) argumenti va `enum` bilan almashtirish](#54-tanlov-selector-argumenti-va-enum-bilan-almashtirish)
  - [5.5 Chiqish argumenti va `void` dan qaytishga o'tish](#55-chiqish-argumenti-va-void-dan-qaytishga-otish)
  - [5.6 Argument obyekti va parametr guruhlari](#56-argument-obyekti-va-parametr-guruhlari)
  - [5.7 Butun obyektni berish yoki maydonini berish](#57-butun-obyektni-berish-yoki-maydonini-berish)
  - [5.8 Argument tartibi va bir xil turdagi qo'shni argumentlar](#58-argument-tartibi-va-bir-xil-turdagi-qoshni-argumentlar)
  - [5.9 Varargs, `null` argument va ixtiyoriy parametrlar](#59-varargs-null-argument-va-ixtiyoriy-parametrlar)
  - [5.10 Overload qilish tuzoqlari va nomni aniqlashtirish](#510-overload-qilish-tuzoqlari-va-nomni-aniqlashtirish)
  - [5.11 Argumentni tekshirish joyi: chegara, konstruktor, domen](#511-argumentni-tekshirish-joyi-chegara-konstruktor-domen)
  - [5.12 Amalda qo'llash](#512-amalda-qollash)
- [6. Shart, mantiq va boshqaruv oqimi (Conditionals and Control Flow)](#6-shart-mantiq-va-boshqaruv-oqimi-conditionals-and-control-flow)
  - [6.1 Shartni nomlash va inkapsulyatsiya qilish](#61-shartni-nomlash-va-inkapsulyatsiya-qilish)
  - [6.2 Inkor shartdan qochish va De Morgan qoidasi](#62-inkor-shartdan-qochish-va-de-morgan-qoidasi)
  - [6.3 Murakkab mantiqni soddalashtirish](#63-murakkab-mantiqni-soddalashtirish)
  - [6.4 `else` ni yo'q qilish usullari](#64-else-ni-yoq-qilish-usullari)
  - [6.5 Ternar operatori: qachon o'qiladi](#65-ternar-operatori-qachon-oqiladi)
  - [6.6 `switch` ni toza ishlatish: to'liqlik, `default`, fallthrough](#66-switch-ni-toza-ishlatish-toliqlik-default-fallthrough)
  - [6.7 Chegaraviy shartlarni inkapsulyatsiya qilish](#67-chegaraviy-shartlarni-inkapsulyatsiya-qilish)
  - [6.8 `null` tekshiruvi zinapoyasi va undan chiqish](#68-null-tekshiruvi-zinapoyasi-va-undan-chiqish)
  - [6.9 Yashirin vaqt bog'liqligini ko'rinadigan qilish](#69-yashirin-vaqt-bogliqligini-korinadigan-qilish)
  - [6.10 Takrorlangan `switch` va turga qarab shoxlanish](#610-takrorlangan-switch-va-turga-qarab-shoxlanish)
  - [6.11 Amalda qo'llash](#611-amalda-qollash)
- [7. Sikl, iteratsiya va to'plam bilan ishlash (Loops and Iteration)](#7-sikl-iteratsiya-va-toplam-bilan-ishlash-loops-and-iteration)
  - [7.1 Sikl tanasini chiqarish va sikl o'zgaruvchisi nomi](#71-sikl-tanasini-chiqarish-va-sikl-ozgaruvchisi-nomi)
  - [7.2 Indeksli sikl, `for-each` va iterator tanlovi](#72-indeksli-sikl-for-each-va-iterator-tanlovi)
  - [7.3 Bitta siklda bir necha ish: siklni bo'lish](#73-bitta-siklda-bir-necha-ish-siklni-bolish)
  - [7.4 `break`, `continue`, label va ulardan chiqish](#74-break-continue-label-va-ulardan-chiqish)
  - [7.5 Birdan ko'p shartli siklni qayta yozish](#75-birdan-kop-shartli-siklni-qayta-yozish)
  - [7.6 Iteratsiya vaqtida to'plamni o'zgartirish](#76-iteratsiya-vaqtida-toplamni-ozgartirish)
  - [7.7 Sikldan quvurga o'tish mezoni](#77-sikldan-quvurga-otish-mezoni)
  - [7.8 Off-by-one va chegarani hujjatlashtirish](#78-off-by-one-va-chegarani-hujjatlashtirish)
  - [7.9 Katta siklda resurs va xotira xatti-harakati](#79-katta-siklda-resurs-va-xotira-xatti-harakati)
  - [7.10 Amalda qo'llash](#710-amalda-qollash)

**[III. Izoh va hujjat](#iii-izoh-va-hujjat)**

- [8. Izoh qoidalari: yaxshi izohlar (Comments: The Good Ones)](#8-izoh-qoidalari-yaxshi-izohlar-comments-the-good-ones)
  - [8.1 Izoh - muvaffaqiyatsizlikni tan olish](#81-izoh---muvaffaqiyatsizlikni-tan-olish)
  - [8.2 O'zini kodda tushuntirish: izohni funksiyaga aylantirish](#82-ozini-kodda-tushuntirish-izohni-funksiyaga-aylantirish)
  - [8.3 Huquqiy va litsenziya izohlari](#83-huquqiy-va-litsenziya-izohlari)
  - [8.4 Ma'lumot beruvchi va maqsadni tushuntiruvchi izoh](#84-malumot-beruvchi-va-maqsadni-tushuntiruvchi-izoh)
  - [8.5 Aniqlashtiruvchi izoh va uning xavfi](#85-aniqlashtiruvchi-izoh-va-uning-xavfi)
  - [8.6 Oqibat haqida ogohlantirish](#86-oqibat-haqida-ogohlantirish)
  - [8.7 TODO, FIXME va ularning hayot muddati](#87-todo-fixme-va-ularning-hayot-muddati)
  - [8.8 Kuchaytiruvchi izoh](#88-kuchaytiruvchi-izoh)
  - [8.9 Formula, standart va huquqiy asos havolasi](#89-formula-standart-va-huquqiy-asos-havolasi)
  - [8.10 Amalda qo'llash](#810-amalda-qollash)
- [9. Yomon izohlar katalogi (Comments: The Bad Ones)](#9-yomon-izohlar-katalogi-comments-the-bad-ones)
  - [9.1 G'o'ldirash (mumbling)](#91-goldirash-mumbling)
  - [9.2 Ortiqcha izoh: kodni so'zma-so'z takrorlash](#92-ortiqcha-izoh-kodni-sozma-soz-takrorlash)
  - [9.3 Chalg'ituvchi izoh](#93-chalgituvchi-izoh)
  - [9.4 Majburiy izoh: har bir maydonga Javadoc](#94-majburiy-izoh-har-bir-maydonga-javadoc)
  - [9.5 Jurnal izohlari va mualliflik imzolari](#95-jurnal-izohlari-va-mualliflik-imzolari)
  - [9.6 Shovqin izohlar](#96-shovqin-izohlar)
  - [9.7 Pozitsiya belgilari va qavs yopilishi izohlari](#97-pozitsiya-belgilari-va-qavs-yopilishi-izohlari)
  - [9.8 Izohga olingan kod](#98-izohga-olingan-kod)
  - [9.9 Nolokal ma'lumot va ortiqcha ma'lumot](#99-nolokal-malumot-va-ortiqcha-malumot)
  - [9.10 Noravshan bog'liqlik](#910-noravshan-bogliqlik)
  - [9.11 Funksiya sarlavhasi izohi](#911-funksiya-sarlavhasi-izohi)
  - [9.12 Izohni o'chirish qarori: tekshiruv ro'yxati](#912-izohni-ochirish-qarori-tekshiruv-royxati)
  - [9.13 Amalda qo'llash](#913-amalda-qollash)
- [10. Javadoc va API hujjati (Javadoc and API Documentation)](#10-javadoc-va-api-hujjati-javadoc-and-api-documentation)
  - [10.1 Javadoc kimga yoziladi va qayerga yozilmaydi](#101-javadoc-kimga-yoziladi-va-qayerga-yozilmaydi)
  - [10.2 Birinchi gap qoidasi va fe'l shakli](#102-birinchi-gap-qoidasi-va-fel-shakli)
  - [10.3 `@param`, `@return`, `@throws` to'liqligi](#103-param-return-throws-toliqligi)
  - [10.4 Shartnoma yozish: oldin shart, keyin shart, invariant](#104-shartnoma-yozish-oldin-shart-keyin-shart-invariant)
  - [10.5 `{@link}`, `{@code}`, `@see` va havola gigiyenasi](#105-link-code-see-va-havola-gigiyenasi)
  - [10.6 `@since`, `@deprecated` va almashtirish ko'rsatmasi](#106-since-deprecated-va-almashtirish-korsatmasi)
  - [10.7 Paket va modul hujjati](#107-paket-va-modul-hujjati)
  - [10.8 Namuna kod va uni kompilyatsiya ostida ushlash](#108-namuna-kod-va-uni-kompilyatsiya-ostida-ushlash)
  - [10.9 Javadoc ni CI da tekshirish](#109-javadoc-ni-ci-da-tekshirish)
  - [10.10 Kod ichidagi hujjat va repodagi hujjat bo'linishi](#1010-kod-ichidagi-hujjat-va-repodagi-hujjat-bolinishi)
  - [10.11 Amalda qo'llash](#1011-amalda-qollash)

**[IV. Formatlash va kod uslubi](#iv-formatlash-va-kod-uslubi)**

- [11. Vertikal formatlash (Vertical Formatting)](#11-vertikal-formatlash-vertical-formatting)
  - [11.1 Fayl o'lchami va sinf uzunligi](#111-fayl-olchami-va-sinf-uzunligi)
  - [11.2 Gazeta metaforasi: yuqoridan pastga ma'lumot zichligi](#112-gazeta-metaforasi-yuqoridan-pastga-malumot-zichligi)
  - [11.3 Tushunchalar orasida bo'sh qator](#113-tushunchalar-orasida-bosh-qator)
  - [11.4 Vertikal zichlik: birga o'qiladigan qatorlarni ajratmaslik](#114-vertikal-zichlik-birga-oqiladigan-qatorlarni-ajratmaslik)
  - [11.5 Vertikal masofa: e'lon va ishlatish orasidagi oraliq](#115-vertikal-masofa-elon-va-ishlatish-orasidagi-oraliq)
  - [11.6 Maydonlar joylashuvi va a'zolar tartibi](#116-maydonlar-joylashuvi-va-azolar-tartibi)
  - [11.7 Bog'liq funksiyalarni yonma-yon qo'yish](#117-bogliq-funksiyalarni-yonma-yon-qoyish)
  - [11.8 Tushunchaviy yaqinlik](#118-tushunchaviy-yaqinlik)
  - [11.9 Vertikal tartib: chaqiruvchi yuqorida](#119-vertikal-tartib-chaqiruvchi-yuqorida)
  - [11.10 Amalda qo'llash](#1110-amalda-qollash)
- [12. Gorizontal formatlash va kod uslubi (Horizontal Formatting and Style)](#12-gorizontal-formatlash-va-kod-uslubi-horizontal-formatting-and-style)
  - [12.1 Qator uzunligi chegarasi va uni tanlash](#121-qator-uzunligi-chegarasi-va-uni-tanlash)
  - [12.2 Gorizontal bo'shliq: operator, qavs, vergul](#122-gorizontal-boshliq-operator-qavs-vergul)
  - [12.3 Gorizontal tekislash nega zarar qiladi](#123-gorizontal-tekislash-nega-zarar-qiladi)
  - [12.4 Indentatsiya va uni buzmaslik](#124-indentatsiya-va-uni-buzmaslik)
  - [12.5 Bo'sh blok va "dummy scope"](#125-bosh-blok-va-dummy-scope)
  - [12.6 Qavs uslubi va bir qatorli `if`](#126-qavs-uslubi-va-bir-qatorli-if)
  - [12.7 Import tartibi va yulduzcha import](#127-import-tartibi-va-yulduzcha-import)
  - [12.8 Zanjirli chaqiruv va oqimni bo'lish](#128-zanjirli-chaqiruv-va-oqimni-bolish)
  - [12.9 Uzun satr, matn bloki va SQL joylashtirish](#129-uzun-satr-matn-bloki-va-sql-joylashtirish)
  - [12.10 Fayl kodirovkasi, qator oxiri va oxirgi bo'sh qator](#1210-fayl-kodirovkasi-qator-oxiri-va-oxirgi-bosh-qator)
  - [12.11 Amalda qo'llash](#1211-amalda-qollash)
- [13. Formatlashni avtomatlashtirish va diff gigiyenasi (Automated Formatting and Diff Hygiene)](#13-formatlashni-avtomatlashtirish-va-diff-gigiyenasi-automated-formatting-and-diff-hygiene)
  - [13.1 Bitta jamoa, bitta uslub: tanlov emas, sozlama](#131-bitta-jamoa-bitta-uslub-tanlov-emas-sozlama)
  - [13.2 `.editorconfig` va IDE sozlamalarini repoda saqlash](#132-editorconfig-va-ide-sozlamalarini-repoda-saqlash)
  - [13.3 Spotless va google-java-format o'rnatish](#133-spotless-va-google-java-format-ornatish)
  - [13.4 Checkstyle qoidalari: faqat mashina tekshiradigani](#134-checkstyle-qoidalari-faqat-mashina-tekshiradigani)
  - [13.5 Pre-commit va CI da formatlash tekshiruvi](#135-pre-commit-va-ci-da-formatlash-tekshiruvi)
  - [13.6 Formatlash o'zgarishini mantiq o'zgarishidan ajratish](#136-formatlash-ozgarishini-mantiq-ozgarishidan-ajratish)
  - [13.7 Katta formatlash commiti va `.git-blame-ignore-revs`](#137-katta-formatlash-commiti-va-git-blame-ignore-revs)
  - [13.8 Generatsiya qilingan kodni formatlashdan chiqarish](#138-generatsiya-qilingan-kodni-formatlashdan-chiqarish)
  - [13.9 Amalda qo'llash](#139-amalda-qollash)

**[V. Obyekt, ma'lumot va holat](#v-obyekt-malumot-va-holat)**

- [14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya (Objects vs Data Structures)](#14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya-objects-vs-data-structures)
  - [14.1 Ma'lumot abstraksiyasi: getter/setter inkapsulyatsiya emas](#141-malumot-abstraksiyasi-gettersetter-inkapsulyatsiya-emas)
  - [14.2 Obyekt va ma'lumot tuzilmasining teskariligi](#142-obyekt-va-malumot-tuzilmasining-teskariligi)
  - [14.3 Gibrid tuzilma: yarim obyekt, yarim struktura](#143-gibrid-tuzilma-yarim-obyekt-yarim-struktura)
  - [14.4 Poyezd avariyasi va tuzilmani yashirish](#144-poyezd-avariyasi-va-tuzilmani-yashirish)
  - [14.5 DTO, Active Record va ularning o'rni](#145-dto-active-record-va-ularning-orni)
  - [14.6 Maydon ko'rinishi: `public` maydon, `package-private`, `final`](#146-maydon-korinishi-public-maydon-package-private-final)
  - [14.7 Ichki to'plamni oshkor qilish va himoyalangan nusxa](#147-ichki-toplamni-oshkor-qilish-va-himoyalangan-nusxa)
  - [14.8 Statik holat, utility sinf va `private` konstruktor](#148-statik-holat-utility-sinf-va-private-konstruktor)
  - [14.9 Obyekt o'z invariantini qanday himoya qiladi](#149-obyekt-oz-invariantini-qanday-himoya-qiladi)
  - [14.10 `this` ning konstruktordan qochib ketishi](#1410-this-ning-konstruktordan-qochib-ketishi)
  - [14.11 Amalda qo'llash](#1411-amalda-qollash)
- [15. Tenglik, hash va obyekt shartnomalari (Equality, Hashing and Object Contracts)](#15-tenglik-hash-va-obyekt-shartnomalari-equality-hashing-and-object-contracts)
  - [15.1 `equals` shartnomasi: besh qoida](#151-equals-shartnomasi-besh-qoida)
  - [15.2 `hashCode` shartnomasi va `equals` bilan bog'liqligi](#152-hashcode-shartnomasi-va-equals-bilan-bogliqligi)
  - [15.3 `equals` ni yozish shabloni va `instanceof` pattern matching](#153-equals-ni-yozish-shabloni-va-instanceof-pattern-matching)
  - [15.4 Vorislik ostida tenglik: `getClass()` yoki `instanceof`](#154-vorislik-ostida-tenglik-getclass-yoki-instanceof)
  - [15.5 Entitet va value object tengligi farqi](#155-entitet-va-value-object-tengligi-farqi)
  - [15.6 `compareTo` shartnomasi va `equals` bilan izchillik](#156-compareto-shartnomasi-va-equals-bilan-izchillik)
  - [15.7 `toString`: foydali, xavfsiz, mantiqda ishlatilmaydigan](#157-tostring-foydali-xavfsiz-mantiqda-ishlatilmaydigan)
  - [15.8 `clone` dan voz kechish va nusxa konstruktori](#158-clone-dan-voz-kechish-va-nusxa-konstruktori)
  - [15.9 O'zgaradigan kalit va `HashMap` dagi yo'qolgan yozuv](#159-ozgaradigan-kalit-va-hashmap-dagi-yoqolgan-yozuv)
  - [15.10 `Comparator` ni toza qurish](#1510-comparator-ni-toza-qurish)
  - [15.11 Amalda qo'llash](#1511-amalda-qollash)
- [16. O'zgarmaslik va holat boshqaruvi kod darajasida (Immutability in Code)](#16-ozgarmaslik-va-holat-boshqaruvi-kod-darajasida-immutability-in-code)
  - [16.1 `final` maydon, `final` sinf va haqiqiy o'zgarmaslik](#161-final-maydon-final-sinf-va-haqiqiy-ozgarmaslik)
  - [16.2 Chuqur va sayoz o'zgarmaslik](#162-chuqur-va-sayoz-ozgarmaslik)
  - [16.3 O'zgarmas to'plamlar: `List.of`, `unmodifiable*`, nusxa](#163-ozgarmas-toplamlar-listof-unmodifiable-nusxa)
  - [16.4 `with` uslubidagi o'zgartiruvchilar](#164-with-uslubidagi-ozgartiruvchilar)
  - [16.5 Builder: validatsiya va majburiy maydonlar](#165-builder-validatsiya-va-majburiy-maydonlar)
  - [16.6 Mutatsiyani bir joyga to'plash](#166-mutatsiyani-bir-joyga-toplash)
  - [16.7 Setter ni olib tashlash yo'li](#167-setter-ni-olib-tashlash-yoli)
  - [16.8 Vaqtinchalik maydon va uni yo'qotish](#168-vaqtinchalik-maydon-va-uni-yoqotish)
  - [16.9 Global va statik o'zgaradigan holat](#169-global-va-statik-ozgaradigan-holat)
  - [16.10 Amalda qo'llash](#1610-amalda-qollash)
- [17. Vorislik, kompozitsiya va polimorfizm mexanikasi (Inheritance Mechanics)](#17-vorislik-kompozitsiya-va-polimorfizm-mexanikasi-inheritance-mechanics)
  - [17.1 Vorislik uchun dizayn qilish yoki `final` qilish](#171-vorislik-uchun-dizayn-qilish-yoki-final-qilish)
  - [17.2 Konstruktorda override qilinadigan metodni chaqirish](#172-konstruktorda-override-qilinadigan-metodni-chaqirish)
  - [17.3 `protected` maydon va buzilgan inkapsulyatsiya](#173-protected-maydon-va-buzilgan-inkapsulyatsiya)
  - [17.4 `super` chaqiruvi va uni unutish](#174-super-chaqiruvi-va-uni-unutish)
  - [17.5 Bazaviy sinfning voris sinfga bog'liqligi](#175-bazaviy-sinfning-voris-sinfga-bogliqligi)
  - [17.6 Rad etilgan meros va interfeysni bo'lish](#176-rad-etilgan-meros-va-interfeysni-bolish)
  - [17.7 Abstrakt sinf va interfeys tanlovi, `default` metodlar](#177-abstrakt-sinf-va-interfeys-tanlovi-default-metodlar)
  - [17.8 Konstantalarni interfeysdan voris olish](#178-konstantalarni-interfeysdan-voris-olish)
  - [17.9 Delegatsiya bilan vorislikni almashtirish](#179-delegatsiya-bilan-vorislikni-almashtirish)
  - [17.10 Amalda qo'llash](#1710-amalda-qollash)

**[VI. Xato bilan ishlash](#vi-xato-bilan-ishlash)**

- [18. Xato bilan ishlash qoidalari (Error Handling Rules)](#18-xato-bilan-ishlash-qoidalari-error-handling-rules)
  - [18.1 Xato kodi emas, istisno](#181-xato-kodi-emas-istisno)
  - [18.2 `try-catch-finally` ni birinchi yozish](#182-try-catch-finally-ni-birinchi-yozish)
  - [18.3 Istisnoni chaqiruvchi ehtiyojiga qarab aniqlash](#183-istisnoni-chaqiruvchi-ehtiyojiga-qarab-aniqlash)
  - [18.4 `try` blokini alohida funksiyaga chiqarish](#184-try-blokini-alohida-funksiyaga-chiqarish)
  - [18.5 Xato bilan ishlash ham bitta ish](#185-xato-bilan-ishlash-ham-bitta-ish)
  - [18.6 Normal oqimni aniqlash va maxsus holat obyekti](#186-normal-oqimni-aniqlash-va-maxsus-holat-obyekti)
  - [18.7 `null` qaytarmaslik va `null` uzatmaslik](#187-null-qaytarmaslik-va-null-uzatmaslik)
  - [18.8 Bo'sh to'plam qaytarish qoidasi](#188-bosh-toplam-qaytarish-qoidasi)
  - [18.9 Istisnoni oqim boshqarish uchun ishlatmaslik](#189-istisnoni-oqim-boshqarish-uchun-ishlatmaslik)
  - [18.10 Tez to'xtash (fail fast) va chegarada tekshirish](#1810-tez-toxtash-fail-fast-va-chegarada-tekshirish)
  - [18.11 Amalda qo'llash](#1811-amalda-qollash)
- [19. Istisno mexanikasi va resurslar (Exception Mechanics and Resources)](#19-istisno-mexanikasi-va-resurslar-exception-mechanics-and-resources)
  - [19.1 Stack trace ni yo'qotmaslik: wrap va rethrow](#191-stack-trace-ni-yoqotmaslik-wrap-va-rethrow)
  - [19.2 Ko'p turni tutish va tutish tartibi](#192-kop-turni-tutish-va-tutish-tartibi)
  - [19.3 `finally` ichidagi `return` va bostirilgan istisno](#193-finally-ichidagi-return-va-bostirilgan-istisno)
  - [19.4 `try-with-resources` va `AutoCloseable`](#194-try-with-resources-va-autocloseable)
  - [19.5 `InterruptedException` ni to'g'ri qayta tiklash](#195-interruptedexception-ni-togri-qayta-tiklash)
  - [19.6 `Throwable`, `Error` va `OutOfMemoryError` siyosati](#196-throwable-error-va-outofmemoryerror-siyosati)
  - [19.7 Log qilish yoki tashlash: ikkisini birga qilmaslik](#197-log-qilish-yoki-tashlash-ikkisini-birga-qilmaslik)
  - [19.8 Assertion va `-ea`: qachon haqli](#198-assertion-va--ea-qachon-haqli)
  - [19.9 `Objects.requireNonNull`, Guava `Preconditions`, Bean Validation](#199-objectsrequirenonnull-guava-preconditions-bean-validation)
  - [19.10 Xato xabari matni: uch xil adresat](#1910-xato-xabari-matni-uch-xil-adresat)
  - [19.11 Xato kodi katalogi va uni barqaror ushlash](#1911-xato-kodi-katalogi-va-uni-barqaror-ushlash)
  - [19.12 Amalda qo'llash](#1912-amalda-qollash)

**[VII. Java tilining toza ishlatilishi](#vii-java-tilining-toza-ishlatilishi)**

- [20. Primitiv, son va pul (Primitives, Numbers and Money)](#20-primitiv-son-va-pul-primitives-numbers-and-money)
  - [20.1 Pul uchun `double` ishlatmaslik](#201-pul-uchun-double-ishlatmaslik)
  - [20.2 `BigDecimal` scale, rounding va `equals` tuzog'i](#202-bigdecimal-scale-rounding-va-equals-tuzogi)
  - [20.3 Butun sonning to'lib ketishi va `Math.*Exact`](#203-butun-sonning-tolib-ketishi-va-mathexact)
  - [20.4 Bo'lish, qoldiq va manfiy son xatti-harakati](#204-bolish-qoldiq-va-manfiy-son-xatti-harakati)
  - [20.5 Primitiv va boxed tur tanlovi, `==` tuzog'i](#205-primitiv-va-boxed-tur-tanlovi--tuzogi)
  - [20.6 Avtoboxing narxi va `null` unboxing](#206-avtoboxing-narxi-va-null-unboxing)
  - [20.7 Pul va o'lchovni value object bilan ifodalash](#207-pul-va-olchovni-value-object-bilan-ifodalash)
  - [20.8 Tasodifiy son, UUID va identifikator generatsiyasi](#208-tasodifiy-son-uuid-va-identifikator-generatsiyasi)
  - [20.9 Amalda qo'llash](#209-amalda-qollash)
- [21. Satr, matn va regex (Strings, Text and Regex)](#21-satr-matn-va-regex-strings-text-and-regex)
  - [21.1 `==` emas `equals`, `intern` va literal pool](#211--emas-equals-intern-va-literal-pool)
  - [21.2 Birlashtirish: `+`, `StringBuilder`, `String.join`, `formatted`](#212-birlashtirish--stringbuilder-stringjoin-formatted)
  - [21.3 Kodirovka va `Charset` ni oshkor berish](#213-kodirovka-va-charset-ni-oshkor-berish)
  - [21.4 `toLowerCase`, `format` va `Locale` tuzog'i](#214-tolowercase-format-va-locale-tuzogi)
  - [21.5 `split`, `trim`, `strip`, `isBlank` farqlari](#215-split-trim-strip-isblank-farqlari)
  - [21.6 Regexni oldindan kompilyatsiya qilish va nomlash](#216-regexni-oldindan-kompilyatsiya-qilish-va-nomlash)
  - [21.7 Katastrofik backtracking va kiritish uzunligi](#217-katastrofik-backtracking-va-kiritish-uzunligi)
  - [21.8 Satr bilan tiplash o'rniga tur](#218-satr-bilan-tiplash-orniga-tur)
  - [21.9 Matn blokida SQL va JSON](#219-matn-blokida-sql-va-json)
  - [21.10 Amalda qo'llash](#2110-amalda-qollash)
- [22. Sana, vaqt va mintaqa (Date, Time and Zone)](#22-sana-vaqt-va-mintaqa-date-time-and-zone)
  - [22.1 `Date`, `Calendar`, `SimpleDateFormat` dan voz kechish](#221-date-calendar-simpledateformat-dan-voz-kechish)
  - [22.2 To'g'ri turni tanlash](#222-togri-turni-tanlash)
  - [22.3 `Clock` ni inyeksiya qilish va testlanadigan vaqt](#223-clock-ni-inyeksiya-qilish-va-testlanadigan-vaqt)
  - [22.4 `ZoneId` va UTC siyosati](#224-zoneid-va-utc-siyosati)
  - [22.5 Davomiylik: `Duration`, `Period` va birlik nomi](#225-davomiylik-duration-period-va-birlik-nomi)
  - [22.6 Chegaralar: inklyuziv va eksklyuziv oraliq](#226-chegaralar-inklyuziv-va-eksklyuziv-oraliq)
  - [22.7 Formatlash va parslash](#227-formatlash-va-parslash)
  - [22.8 Yoz/qish vaqti, sakrash soati va oy oxiri](#228-yozqish-vaqti-sakrash-soati-va-oy-oxiri)
  - [22.9 Bazada, API da va kodda vaqt turi muvofiqligi](#229-bazada-api-da-va-kodda-vaqt-turi-muvofiqligi)
  - [22.10 Amalda qo'llash](#2210-amalda-qollash)
- [23. To'plamlar va generiklar gigiyenasi (Collections and Generics)](#23-toplamlar-va-generiklar-gigiyenasi-collections-and-generics)
  - [23.1 To'g'ri to'plam turini tanlash](#231-togri-toplam-turini-tanlash)
  - [23.2 `Map` ni toza ishlatish](#232-map-ni-toza-ishlatish)
  - [23.3 `Collectors.toMap` va takrorlangan kalit](#233-collectorstomap-va-takrorlangan-kalit)
  - [23.4 Iteratsiya tartibi](#234-iteratsiya-tartibi)
  - [23.5 `Arrays.asList`, `List.of` va o'zgartirilmaslik farqi](#235-arraysaslist-listof-va-ozgartirilmaslik-farqi)
  - [23.6 `null` kalit va qiymat siyosati](#236-null-kalit-va-qiymat-siyosati)
  - [23.7 Xom tur va `unchecked` ogohlantirish](#237-xom-tur-va-unchecked-ogohlantirish)
  - [23.8 Wildcard qoidalari: PECS](#238-wildcard-qoidalari-pecs)
  - [23.9 Generik metod, tur xulosasi va `var`](#239-generik-metod-tur-xulosasi-va-var)
  - [23.10 Massiv va generikni aralashtirmaslik](#2310-massiv-va-generikni-aralashtirmaslik)
  - [23.11 To'plamni qaytarish: nusxa, ko'rinish, oqim](#2311-toplamni-qaytarish-nusxa-korinish-oqim)
  - [23.12 Amalda qo'llash](#2312-amalda-qollash)
- [24. Lambda, oqim va funksional uslub tozaligi (Lambdas and Streams)](#24-lambda-oqim-va-funksional-uslub-tozaligi-lambdas-and-streams)
  - [24.1 Lambda uzunligi va uni metodga chiqarish](#241-lambda-uzunligi-va-uni-metodga-chiqarish)
  - [24.2 Metod havolasi qachon o'qiladi](#242-metod-havolasi-qachon-oqiladi)
  - [24.3 Standart funksional interfeyslar va o'zingiznikini yozmaslik](#243-standart-funksional-interfeyslar-va-ozingiznikini-yozmaslik)
  - [24.4 Oqim ichida yon ta'sir va `forEach` tuzog'i](#244-oqim-ichida-yon-tasir-va-foreach-tuzogi)
  - [24.5 `peek`, `parallelStream` va tartib](#245-peek-parallelstream-va-tartib)
  - [24.6 `Optional` ni zanjirda toza ishlatish](#246-optional-ni-zanjirda-toza-ishlatish)
  - [24.7 Tekshiriladigan istisno va lambda](#247-tekshiriladigan-istisno-va-lambda)
  - [24.8 `Collectors` ni o'qiladigan ushlash](#248-collectors-ni-oqiladigan-ushlash)
  - [24.9 Oqimni qaytarish yoki to'plam qaytarish](#249-oqimni-qaytarish-yoki-toplam-qaytarish)
  - [24.10 Amalda qo'llash](#2410-amalda-qollash)
- [25. Java kodidagi umumiy tuzoqlar (Common Java Pitfalls)](#25-java-kodidagi-umumiy-tuzoqlar-common-java-pitfalls)
  - [25.1 `Optional` maydon, parametr va seriyalash](#251-optional-maydon-parametr-va-seriyalash)
  - [25.2 Statik ishga tushirish tartibi va sinf yuklanishi](#252-statik-ishga-tushirish-tartibi-va-sinf-yuklanishi)
  - [25.3 `instanceof` zanjiri va `getClass()` solishtirish](#253-instanceof-zanjiri-va-getclass-solishtirish)
  - [25.4 Seriyalash: `serialVersionUID`, `readObject` va undan qochish](#254-seriyalash-serialversionuid-readobject-va-undan-qochish)
  - [25.5 Refleksiya narxi va uni chegaralash](#255-refleksiya-narxi-va-uni-chegaralash)
  - [25.6 `finalize`, `Cleaner` va resurs oxiri](#256-finalize-cleaner-va-resurs-oxiri)
  - [25.7 Ichki sinf va yashirin tashqi havola](#257-ichki-sinf-va-yashirin-tashqi-havola)
  - [25.8 Anonim sinf va lambda tanlovi](#258-anonim-sinf-va-lambda-tanlovi)
  - [25.9 `enum` da xatti-harakat, `EnumMap`, `EnumSet`, `valueOf`](#259-enum-da-xatti-harakat-enummap-enumset-valueof)
  - [25.10 Kompilyator ogohlantirishlari: `-Xlint`, `-Werror`, Error Prone, NullAway](#2510-kompilyator-ogohlantirishlari--xlint--werror-error-prone-nullaway)
  - [25.11 Amalda qo'llash](#2511-amalda-qollash)

**[VIII. Spring va ma'lumot qatlamida toza kod](#viii-spring-va-malumot-qatlamida-toza-kod)**

- [26. Spring kodining tozaligi (Clean Code in Spring)](#26-spring-kodining-tozaligi-clean-code-in-spring)
  - [26.1 Konstruktor inyeksiyasi va `final` maydon](#261-konstruktor-inyeksiyasi-va-final-maydon)
  - [26.2 Bean ko'rinishi: `package-private` konfiguratsiya va komponentlar](#262-bean-korinishi-package-private-konfiguratsiya-va-komponentlar)
  - [26.3 Konfiguratsiya: `@ConfigurationProperties` record bilan](#263-konfiguratsiya-configurationproperties-record-bilan)
  - [26.4 Konfiguratsiyani validatsiya qilish va tez to'xtash](#264-konfiguratsiyani-validatsiya-qilish-va-tez-toxtash)
  - [26.5 Controller ni yupqa ushlash](#265-controller-ni-yupqa-ushlash)
  - [26.6 DTO va domen o'rtasidagi mapping joyi](#266-dto-va-domen-ortasidagi-mapping-joyi)
  - [26.7 Service qatlamida metod nomlari va tranzaksiya chegarasi](#267-service-qatlamida-metod-nomlari-va-tranzaksiya-chegarasi)
  - [26.8 `@Qualifier`, `@Primary` va bean nomlari](#268-qualifier-primary-va-bean-nomlari)
  - [26.9 Shartli konfiguratsiya va `@Profile` ni kamaytirish](#269-shartli-konfiguratsiya-va-profile-ni-kamaytirish)
  - [26.10 Lombok siyosati: xavfsiz va xavfli annotatsiyalar](#2610-lombok-siyosati-xavfsiz-va-xavfli-annotatsiyalar)
  - [26.11 Amalda qo'llash](#2611-amalda-qollash)
- [27. REST API kodining o'qilishi (Readable REST Code)](#27-rest-api-kodining-oqilishi-readable-rest-code)
  - [27.1 Controller metodi imzosi va qaytish turi](#271-controller-metodi-imzosi-va-qaytish-turi)
  - [27.2 HTTP holat kodini bitta joyda qaror qilish](#272-http-holat-kodini-bitta-joyda-qaror-qilish)
  - [27.3 Xato javobi formati: `ProblemDetail` va `@ExceptionHandler`](#273-xato-javobi-formati-problemdetail-va-exceptionhandler)
  - [27.4 Validatsiya: `@Valid`, guruhlar, maxsus validator](#274-validatsiya-valid-guruhlar-maxsus-validator)
  - [27.5 Sahifalash, saralash va filtr parametrlari](#275-sahifalash-saralash-va-filtr-parametrlari)
  - [27.6 Seriyalash sozlamalari: Jackson, `null`, sana formati](#276-seriyalash-sozlamalari-jackson-null-sana-formati)
  - [27.7 Idempotentlik va `Idempotency-Key` kodda](#277-idempotentlik-va-idempotency-key-kodda)
  - [27.8 API versiyasi kodda qanday ko'rinadi](#278-api-versiyasi-kodda-qanday-korinadi)
  - [27.9 Amalda qo'llash](#279-amalda-qollash)
- [28. JPA va SQL kodining tozaligi (Clean JPA and SQL)](#28-jpa-va-sql-kodining-tozaligi-clean-jpa-and-sql)
  - [28.1 Entitet gigiyenasi: `equals`, `hashCode`, `toString`](#281-entitet-gigiyenasi-equals-hashcode-tostring)
  - [28.2 Lombok va entitet: nimani ishlatmaslik](#282-lombok-va-entitet-nimani-ishlatmaslik)
  - [28.3 Assotsiatsiya yordamchi metodlari va ikki tomonlilik](#283-assotsiatsiya-yordamchi-metodlari-va-ikki-tomonlilik)
  - [28.4 `fetch`, `cascade`, `orphanRemoval` ni oshkor yozish](#284-fetch-cascade-orphanremoval-ni-oshkor-yozish)
  - [28.5 Repository metod nomlari: derived query chegarasi](#285-repository-metod-nomlari-derived-query-chegarasi)
  - [28.6 `@Query`, native query va ularni o'qiladigan ushlash](#286-query-native-query-va-ularni-oqiladigan-ushlash)
  - [28.7 Projeksiya va DTO qaytarish](#287-projeksiya-va-dto-qaytarish)
  - [28.8 SQL yozish uslubi](#288-sql-yozish-uslubi)
  - [28.9 Migratsiya fayli nomlanishi va mazmuni](#289-migratsiya-fayli-nomlanishi-va-mazmuni)
  - [28.10 Amalda qo'llash](#2810-amalda-qollash)
- [29. Log kodining tozaligi (Clean Logging Code)](#29-log-kodining-tozaligi-clean-logging-code)
  - [29.1 SLF4J parametrlangan xabar va satr birlashtirmaslik](#291-slf4j-parametrlangan-xabar-va-satr-birlashtirmaslik)
  - [29.2 Daraja tanlash qoidalari](#292-daraja-tanlash-qoidalari)
  - [29.3 Istisnoni oxirgi argument sifatida berish](#293-istisnoni-oxirgi-argument-sifatida-berish)
  - [29.4 `e.getMessage()` bilan stack trace ni yo'qotish](#294-egetmessage-bilan-stack-trace-ni-yoqotish)
  - [29.5 Bir hodisa, bitta log](#295-bir-hodisa-bitta-log)
  - [29.6 Strukturali log va kalit nomlari](#296-strukturali-log-va-kalit-nomlari)
  - [29.7 Korrelyatsiya identifikatori va MDC tozalash](#297-korrelyatsiya-identifikatori-va-mdc-tozalash)
  - [29.8 Sezgir ma'lumot va maskalash](#298-sezgir-malumot-va-maskalash)
  - [29.9 Log ni test bilan mahkamlash](#299-log-ni-test-bilan-mahkamlash)
  - [29.10 Amalda qo'llash](#2910-amalda-qollash)

**[IX. Test kodining tozaligi](#ix-test-kodining-tozaligi)**

- [30. Test kodi ham ishlab chiqarish kodi (Test Code Is Production Code)](#30-test-kodi-ham-ishlab-chiqarish-kodi-test-code-is-production-code)
  - [30.1 Toza test nega kod bazasini saqlab qoladi](#301-toza-test-nega-kod-bazasini-saqlab-qoladi)
  - [30.2 DRY va DAMP muvozanati testda](#302-dry-va-damp-muvozanati-testda)
  - [30.3 Test ma'lumot quruvchilari: builder va object mother](#303-test-malumot-quruvchilari-builder-va-object-mother)
  - [30.4 Testda mantiq bo'lmasligi](#304-testda-mantiq-bolmasligi)
  - [30.5 Bir tushuncha, bir test](#305-bir-tushuncha-bir-test)
  - [30.6 Assertion o'qilishi va xato xabari](#306-assertion-oqilishi-va-xato-xabari)
  - [30.7 Test dublyorlarini nomlash va chegaralash](#307-test-dublyorlarini-nomlash-va-chegaralash)
  - [30.8 Testlar orasidagi bog'liqlik va tartib](#308-testlar-orasidagi-bogliqlik-va-tartib)
  - [30.9 Test hidlari katalogi](#309-test-hidlari-katalogi)
  - [30.10 Amalda qo'llash](#3010-amalda-qollash)
- [31. TDD intizomi va kod dizayniga ta'siri (TDD Discipline)](#31-tdd-intizomi-va-kod-dizayniga-tasiri-tdd-discipline)
  - [31.1 Uchta qoida va qisqa sikl](#311-uchta-qoida-va-qisqa-sikl)
  - [31.2 Red-green-refactor: har bir qadamning maqsadi](#312-red-green-refactor-har-bir-qadamning-maqsadi)
  - [31.3 Test birinchi yozilsa dizayn qanday o'zgaradi](#313-test-birinchi-yozilsa-dizayn-qanday-ozgaradi)
  - [31.4 Ishlasin, to'g'ri bo'lsin, tez bo'lsin tartibi](#314-ishlasin-togri-bolsin-tez-bolsin-tartibi)
  - [31.5 Test yozish qiyin bo'lsa, dizayn signal beradi](#315-test-yozish-qiyin-bolsa-dizayn-signal-beradi)
  - [31.6 TDD qachon mos emas](#316-tdd-qachon-mos-emas)
  - [31.7 Transformatsiya prioritet gipotezasi](#317-transformatsiya-prioritet-gipotezasi)
  - [31.8 Amalda qo'llash](#318-amalda-qollash)

**[X. Hid katalogi va refaktoring harakatlari](#x-hid-katalogi-va-refaktoring-harakatlari)**

- [32. Kod hidlari katalogi I: nom, funksiya, ma'lumot (Code Smells I)](#32-kod-hidlari-katalogi-i-nom-funksiya-malumot-code-smells-i)
  - [32.1 Sirli nom (Mysterious Name)](#321-sirli-nom-mysterious-name)
  - [32.2 Takrorlangan kod (Duplicated Code)](#322-takrorlangan-kod-duplicated-code)
  - [32.3 Uzun funksiya (Long Function)](#323-uzun-funksiya-long-function)
  - [32.4 Global ma'lumot (Global Data)](#324-global-malumot-global-data)
  - [32.5 O'zgaradigan ma'lumot (Mutable Data)](#325-ozgaradigan-malumot-mutable-data)
  - [32.6 Ma'lumot to'dasi (Data Clumps)](#326-malumot-todasi-data-clumps)
  - [32.7 Takrorlangan `switch` (Repeated Switches)](#327-takrorlangan-switch-repeated-switches)
  - [32.8 Sikllar (Loops)](#328-sikllar-loops)
  - [32.9 Dangasa element (Lazy Element)](#329-dangasa-element-lazy-element)
  - [32.10 Vaqtinchalik maydon (Temporary Field)](#3210-vaqtinchalik-maydon-temporary-field)
  - [32.11 Uzun xabar zanjiri (Message Chains)](#3211-uzun-xabar-zanjiri-message-chains)
  - [32.12 Vositachi (Middle Man)](#3212-vositachi-middle-man)
  - [32.13 Izohlar hid sifatida (Comments)](#3213-izohlar-hid-sifatida-comments)
  - [32.14 Bu hid emas: qachon tegmaslik kerak](#3214-bu-hid-emas-qachon-tegmaslik-kerak)
  - [32.15 Amalda qo'llash](#3215-amalda-qollash)
- [33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik (Code Smells II)](#33-kod-hidlari-katalogi-ii-sinf-ierarxiya-bogliqlik-code-smells-ii)
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
- [34. Toza kod evristikalarining to'liq ro'yxati (Clean Code Heuristics)](#34-toza-kod-evristikalarining-toliq-royxati-clean-code-heuristics)
  - [34.1 Izohlar (C1-C5)](#341-izohlar-c1-c5)
  - [34.2 Muhit (E1-E2)](#342-muhit-e1-e2)
  - [34.3 Funksiyalar (F1-F4)](#343-funksiyalar-f1-f4)
  - [34.4 Umumiy evristikalar (G1-G12)](#344-umumiy-evristikalar-g1-g12)
  - [34.5 Umumiy evristikalar (G13-G24)](#345-umumiy-evristikalar-g13-g24)
  - [34.6 Umumiy evristikalar (G25-G36)](#346-umumiy-evristikalar-g25-g36)
  - [34.7 Java ga xos evristikalar (J1-J3)](#347-java-ga-xos-evristikalar-j1-j3)
  - [34.8 Nomlar (N1-N7)](#348-nomlar-n1-n7)
  - [34.9 Testlar (T1-T9)](#349-testlar-t1-t9)
  - [34.10 Evristikani review da ishlatish](#3410-evristikani-review-da-ishlatish)
  - [34.11 Amalda qo'llash](#3411-amalda-qollash)
- [35. Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi (Refactoring Moves I)](#35-refaktoring-harakatlari-katalogi-i-funksiya-va-ozgaruvchi-refactoring-moves-i)
  - [35.1 Funksiya ajratish (Extract Function)](#351-funksiya-ajratish-extract-function)
  - [35.2 Funksiyani ichkariga kiritish (Inline Function)](#352-funksiyani-ichkariga-kiritish-inline-function)
  - [35.3 O'zgaruvchi ajratish (Extract Variable)](#353-ozgaruvchi-ajratish-extract-variable)
  - [35.4 O'zgaruvchini ichkariga kiritish (Inline Variable)](#354-ozgaruvchini-ichkariga-kiritish-inline-variable)
  - [35.5 Funksiya e'lonini o'zgartirish (Change Function Declaration)](#355-funksiya-elonini-ozgartirish-change-function-declaration)
  - [35.6 O'zgaruvchini inkapsulyatsiya qilish (Encapsulate Variable)](#356-ozgaruvchini-inkapsulyatsiya-qilish-encapsulate-variable)
  - [35.7 O'zgaruvchini qayta nomlash (Rename Variable / Rename Field)](#357-ozgaruvchini-qayta-nomlash-rename-variable--rename-field)
  - [35.8 Parametr obyektini kiritish (Introduce Parameter Object)](#358-parametr-obyektini-kiritish-introduce-parameter-object)
  - [35.9 Funksiyalarni sinfga birlashtirish (Combine Functions into Class)](#359-funksiyalarni-sinfga-birlashtirish-combine-functions-into-class)
  - [35.10 Funksiyalarni transformatsiyaga birlashtirish (Combine Functions into Transform)](#3510-funksiyalarni-transformatsiyaga-birlashtirish-combine-functions-into-transform)
  - [35.11 Bosqichlarni ajratish (Split Phase)](#3511-bosqichlarni-ajratish-split-phase)
  - [35.12 Funksiyani ko'chirish (Move Function)](#3512-funksiyani-kochirish-move-function)
  - [35.13 Gaplarni funksiyaga ko'chirish va chaqiruvchiga chiqarish](#3513-gaplarni-funksiyaga-kochirish-va-chaqiruvchiga-chiqarish)
  - [35.14 Inline kodni funksiya chaqiruviga almashtirish](#3514-inline-kodni-funksiya-chaqiruviga-almashtirish)
  - [35.15 Gaplarni surish (Slide Statements)](#3515-gaplarni-surish-slide-statements)
  - [35.16 Siklni bo'lish (Split Loop)](#3516-siklni-bolish-split-loop)
  - [35.17 Siklni quvurga almashtirish (Replace Loop with Pipeline)](#3517-siklni-quvurga-almashtirish-replace-loop-with-pipeline)
  - [35.18 O'lik kodni o'chirish (Remove Dead Code)](#3518-olik-kodni-ochirish-remove-dead-code)
  - [35.19 O'zgaruvchini bo'lish (Split Variable)](#3519-ozgaruvchini-bolish-split-variable)
  - [35.20 Hosila o'zgaruvchini so'rovga almashtirish](#3520-hosila-ozgaruvchini-sorovga-almashtirish)
  - [35.21 Amalda qo'llash](#3521-amalda-qollash)
- [36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya (Refactoring Moves II)](#36-refaktoring-harakatlari-katalogi-ii-malumot-va-inkapsulyatsiya-refactoring-moves-ii)
  - [36.1 Sinf ajratish (Extract Class)](#361-sinf-ajratish-extract-class)
  - [36.2 Sinfni ichkariga kiritish (Inline Class)](#362-sinfni-ichkariga-kiritish-inline-class)
  - [36.3 Delegatni yashirish (Hide Delegate)](#363-delegatni-yashirish-hide-delegate)
  - [36.4 Vositachini olib tashlash (Remove Middle Man)](#364-vositachini-olib-tashlash-remove-middle-man)
  - [36.5 Maydonni ko'chirish (Move Field)](#365-maydonni-kochirish-move-field)
  - [36.6 Yozuvni inkapsulyatsiya qilish (Encapsulate Record)](#366-yozuvni-inkapsulyatsiya-qilish-encapsulate-record)
  - [36.7 To'plamni inkapsulyatsiya qilish (Encapsulate Collection)](#367-toplamni-inkapsulyatsiya-qilish-encapsulate-collection)
  - [36.8 Primitivni obyektga almashtirish (Replace Primitive with Object)](#368-primitivni-obyektga-almashtirish-replace-primitive-with-object)
  - [36.9 Vaqtinchalikni so'rovga almashtirish (Replace Temp with Query)](#369-vaqtinchalikni-sorovga-almashtirish-replace-temp-with-query)
  - [36.10 Havolani qiymatga almashtirish (Change Reference to Value)](#3610-havolani-qiymatga-almashtirish-change-reference-to-value)
  - [36.11 Qiymatni havolaga almashtirish (Change Value to Reference)](#3611-qiymatni-havolaga-almashtirish-change-value-to-reference)
  - [36.12 Sozlash metodini olib tashlash (Remove Setting Method)](#3612-sozlash-metodini-olib-tashlash-remove-setting-method)
  - [36.13 Konstruktorni fabrika funksiyasiga almashtirish](#3613-konstruktorni-fabrika-funksiyasiga-almashtirish)
  - [36.14 Funksiyani buyruqqa va buyruqni funksiyaga almashtirish](#3614-funksiyani-buyruqqa-va-buyruqni-funksiyaga-almashtirish)
  - [36.15 Maydon va metodni yuqoriga/pastga ko'chirish](#3615-maydon-va-metodni-yuqorigapastga-kochirish)
  - [36.16 Amalda qo'llash](#3616-amalda-qollash)
- [37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya (Refactoring Moves III)](#37-refaktoring-harakatlari-katalogi-iii-shart-api-va-ierarxiya-refactoring-moves-iii)
  - [37.1 Shartni parchalash (Decompose Conditional)](#371-shartni-parchalash-decompose-conditional)
  - [37.2 Shartli ifodalarni birlashtirish (Consolidate Conditional Expression)](#372-shartli-ifodalarni-birlashtirish-consolidate-conditional-expression)
  - [37.3 Ichma-ich shartni guard clause ga almashtirish](#373-ichma-ich-shartni-guard-clause-ga-almashtirish)
  - [37.4 Shartni polimorfizmga almashtirish (Replace Conditional with Polymorphism)](#374-shartni-polimorfizmga-almashtirish-replace-conditional-with-polymorphism)
  - [37.5 Maxsus holatni kiritish (Introduce Special Case)](#375-maxsus-holatni-kiritish-introduce-special-case)
  - [37.6 Assertion kiritish (Introduce Assertion)](#376-assertion-kiritish-introduce-assertion)
  - [37.7 So'rovni o'zgartirishdan ajratish (Separate Query from Modifier)](#377-sorovni-ozgartirishdan-ajratish-separate-query-from-modifier)
  - [37.8 Funksiyani parametrlash (Parameterize Function)](#378-funksiyani-parametrlash-parameterize-function)
  - [37.9 Flag argumentini olib tashlash (Remove Flag Argument)](#379-flag-argumentini-olib-tashlash-remove-flag-argument)
  - [37.10 Butun obyektni saqlash (Preserve Whole Object)](#3710-butun-obyektni-saqlash-preserve-whole-object)
  - [37.11 Parametrni so'rovga va so'rovni parametrga almashtirish](#3711-parametrni-sorovga-va-sorovni-parametrga-almashtirish)
  - [37.12 Algoritmni almashtirish (Substitute Algorithm)](#3712-algoritmni-almashtirish-substitute-algorithm)
  - [37.13 Turni kodlashdan voris sinflarga almashtirish](#3713-turni-kodlashdan-voris-sinflarga-almashtirish)
  - [37.14 Voris sinfni delegatsiyaga almashtirish](#3714-voris-sinfni-delegatsiyaga-almashtirish)
  - [37.15 Voris sinfni va ierarxiyani yo'qotish](#3715-voris-sinfni-va-ierarxiyani-yoqotish)
  - [37.16 Refaktoring harakatini tanlash jadvali](#3716-refaktoring-harakatini-tanlash-jadvali)
  - [37.17 Amalda qo'llash](#3717-amalda-qollash)
- [38. Refaktoringni xavfsiz bajarish (Safe Refactoring Mechanics)](#38-refaktoringni-xavfsiz-bajarish-safe-refactoring-mechanics)
  - [38.1 Bir vaqtda bitta harakat](#381-bir-vaqtda-bitta-harakat)
  - [38.2 Kompilyator va test bilan boshqarish](#382-kompilyator-va-test-bilan-boshqarish)
  - [38.3 IDE refaktoringiga ishonish chegarasi](#383-ide-refaktoringiga-ishonish-chegarasi)
  - [38.4 Refaktoringni mantiq o'zgarishidan ajratish](#384-refaktoringni-mantiq-ozgarishidan-ajratish)
  - [38.5 Katta refaktoringni bo'lish: abstraksiya orqali shox](#385-katta-refaktoringni-bolish-abstraksiya-orqali-shox)
  - [38.6 Refaktoringni to'xtatish nuqtasi](#386-refaktoringni-toxtatish-nuqtasi)
  - [38.7 Refaktoring va ishlash: o'lchovsiz qadam qo'ymaslik](#387-refaktoring-va-ishlash-olchovsiz-qadam-qoymaslik)
  - [38.8 Refaktoring commitlarini o'qiladigan ushlash](#388-refaktoring-commitlarini-oqiladigan-ushlash)
  - [38.9 Amalda qo'llash](#389-amalda-qollash)

**[XI. Kod bazasi va jarayon gigiyenasi](#xi-kod-bazasi-va-jarayon-gigiyenasi)**

- [39. Bir qadamli build va mahalliy qaytish halqasi (One-Step Build)](#39-bir-qadamli-build-va-mahalliy-qaytish-halqasi-one-step-build)
  - [39.1 Build bitta buyruq bo'lsin](#391-build-bitta-buyruq-bolsin)
  - [39.2 Test bitta buyruq bo'lsin](#392-test-bitta-buyruq-bolsin)
  - [39.3 Takrorlanadigan build: versiya qotirish va wrapper](#393-takrorlanadigan-build-versiya-qotirish-va-wrapper)
  - [39.4 Bog'liqlik gigiyenasi: BOM, scope, keraksizni o'chirish](#394-bogliqlik-gigiyenasi-bom-scope-keraksizni-ochirish)
  - [39.5 Build fayli o'qilishi](#395-build-fayli-oqilishi)
  - [39.6 Generatsiya qilingan kodni ajratish](#396-generatsiya-qilingan-kodni-ajratish)
  - [39.7 Mahalliy tez qaytish halqasi](#397-mahalliy-tez-qaytish-halqasi)
  - [39.8 `.gitignore`, sir va konfiguratsiya fayllari](#398-gitignore-sir-va-konfiguratsiya-fayllari)
  - [39.9 Amalda qo'llash](#399-amalda-qollash)
- [40. Versiya nazorati gigiyenasi (Version Control Hygiene)](#40-versiya-nazorati-gigiyenasi-version-control-hygiene)
  - [40.1 Atomik commit: bitta mantiqiy o'zgarish](#401-atomik-commit-bitta-mantiqiy-ozgarish)
  - [40.2 Commit xabari tuzilishi](#402-commit-xabari-tuzilishi)
  - [40.3 Conventional commits va avtomatik changelog](#403-conventional-commits-va-avtomatik-changelog)
  - [40.4 Branch hayoti va uzoq yashagan branch narxi](#404-branch-hayoti-va-uzoq-yashagan-branch-narxi)
  - [40.5 Rebase, merge va tarixni o'qiladigan ushlash](#405-rebase-merge-va-tarixni-oqiladigan-ushlash)
  - [40.6 PR hajmi va bo'lish texnikasi](#406-pr-hajmi-va-bolish-texnikasi)
  - [40.7 `git blame` ni foydali ushlash](#407-git-blame-ni-foydali-ushlash)
  - [40.8 Tarixdan sirni o'chirish va uning chegarasi](#408-tarixdan-sirni-ochirish-va-uning-chegarasi)
  - [40.9 Amalda qo'llash](#409-amalda-qollash)
- [41. O'zgarishni kiritish jarayoni: kichik qadamlar (Working in Small Steps)](#41-ozgarishni-kiritish-jarayoni-kichik-qadamlar-working-in-small-steps)
  - [41.1 Ish boshlashdan oldin: muammoni yozib olish](#411-ish-boshlashdan-oldin-muammoni-yozib-olish)
  - [41.2 Oldin tushunish, keyin o'zgartirish](#412-oldin-tushunish-keyin-ozgartirish)
  - [41.3 Kodni o'qish texnikalari](#413-kodni-oqish-texnikalari)
  - [41.4 Birinchi ishlaydigan versiya va keyin tozalash](#414-birinchi-ishlaydigan-versiya-va-keyin-tozalash)
  - [41.5 Yarim ishni boshqarish va feature flag](#415-yarim-ishni-boshqarish-va-feature-flag)
  - [41.6 O'zini review qilish ro'yxati](#416-ozini-review-qilish-royxati)
  - [41.7 Pair va mob programming mexanikasi](#417-pair-va-mob-programming-mexanikasi)
  - [41.8 Ishni tugatish ta'rifi (definition of done)](#418-ishni-tugatish-tarifi-definition-of-done)
  - [41.9 Amalda qo'llash](#419-amalda-qollash)
- [42. Statik tahlil va avtomatik qoidalar (Static Analysis and Automated Rules)](#42-statik-tahlil-va-avtomatik-qoidalar-static-analysis-and-automated-rules)
  - [42.1 Kompilyator birinchi tekshiruvchi](#421-kompilyator-birinchi-tekshiruvchi)
  - [42.2 Error Prone va NullAway](#422-error-prone-va-nullaway)
  - [42.3 SpotBugs, PMD va Checkstyle rollari](#423-spotbugs-pmd-va-checkstyle-rollari)
  - [42.4 ArchUnit bilan qoidani kodga aylantirish](#424-archunit-bilan-qoidani-kodga-aylantirish)
  - [42.5 Maxsus lint qoidasi yozish](#425-maxsus-lint-qoidasi-yozish)
  - [42.6 Qoidani joriy qilish tartibi: ogohlantirish, keyin xato](#426-qoidani-joriy-qilish-tartibi-ogohlantirish-keyin-xato)
  - [42.7 False positive va bostirishni hujjatlashtirish](#427-false-positive-va-bostirishni-hujjatlashtirish)
  - [42.8 Amalda qo'llash](#428-amalda-qollash)

**[XII. Professional intizom](#xii-professional-intizom)**

- [43. Professional mas'uliyat (Professionalism)](#43-professional-masuliyat-professionalism)
  - [43.1 "Zarar qilmaslik": funksiyaga va tuzilishga](#431-zarar-qilmaslik-funksiyaga-va-tuzilishga)
  - [43.2 O'z xatosi uchun javob berish](#432-oz-xatosi-uchun-javob-berish)
  - [43.3 Ishga layoqat: charchagan holda kod yozmaslik](#433-ishga-layoqat-charchagan-holda-kod-yozmaslik)
  - [43.4 Mijoz va ishlab chiquvchi maqsadlari to'qnashuvi](#434-mijoz-va-ishlab-chiquvchi-maqsadlari-toqnashuvi)
  - [43.5 Kasbiy etika: sir, ma'lumot, xavfsizlik](#435-kasbiy-etika-sir-malumot-xavfsizlik)
  - [43.6 Amalda qo'llash](#436-amalda-qollash)
- [44. "Yo'q" va "ha" deyish: majburiyat tili (Saying No and Saying Yes)](#44-yoq-va-ha-deyish-majburiyat-tili-saying-no-and-saying-yes)
  - [44.1 "Yo'q" ni qachon va qanday aytish](#441-yoq-ni-qachon-va-qanday-aytish)
  - [44.2 "Urinib ko'raman" nega yolg'on](#442-urinib-koraman-nega-yolgon)
  - [44.3 Majburiyat tili: aytaman, qilaman, qachongacha](#443-majburiyat-tili-aytaman-qilaman-qachongacha)
  - [44.4 Passiv tavakkalchilik va uning narxi](#444-passiv-tavakkalchilik-va-uning-narxi)
  - [44.5 Jamoa bo'lib "yo'q" deyish](#445-jamoa-bolib-yoq-deyish)
  - [44.6 Amalda qo'llash](#446-amalda-qollash)
- [45. Baholash, muddat va bosim (Estimation, Deadlines and Pressure)](#45-baholash-muddat-va-bosim-estimation-deadlines-and-pressure)
  - [45.1 Baho va majburiyat farqi](#451-baho-va-majburiyat-farqi)
  - [45.2 Uch nuqtali baho va PERT](#452-uch-nuqtali-baho-va-pert)
  - [45.3 Planning poker va kattalik birligi](#453-planning-poker-va-kattalik-birligi)
  - [45.4 Katta ishni baholash va noaniqlik konusi](#454-katta-ishni-baholash-va-noaniqlik-konusi)
  - [45.5 Bosim ostida intizomni saqlash](#455-bosim-ostida-intizomni-saqlash)
  - [45.6 Kechikishni oshkor qilish va "90% tayyor" tuzog'i](#456-kechikishni-oshkor-qilish-va-90-tayyor-tuzogi)
  - [45.7 Qamrovni qisqartirish yoki sifatni qisqartirish](#457-qamrovni-qisqartirish-yoki-sifatni-qisqartirish)
  - [45.8 Amalda qo'llash](#458-amalda-qollash)
- [46. Vaqt, diqqat va mashq (Time, Focus and Practice)](#46-vaqt-diqqat-va-mashq-time-focus-and-practice)
  - [46.1 Diqqat resursi va uni sarflash](#461-diqqat-resursi-va-uni-sarflash)
  - [46.2 Oqim holati haqidagi afsona](#462-oqim-holati-haqidagi-afsona)
  - [46.3 Uzilishlarni boshqarish](#463-uzilishlarni-boshqarish)
  - [46.4 Pomodoro va vaqt bloklari](#464-pomodoro-va-vaqt-bloklari)
  - [46.5 Ko'r yo'lak va botqoqdan chiqish](#465-kor-yolak-va-botqoqdan-chiqish)
  - [46.6 Majlis: qachon chiqib ketish haqli](#466-majlis-qachon-chiqib-ketish-haqli)
  - [46.7 Kod kata, dojo va ataylab mashq](#467-kod-kata-dojo-va-ataylab-mashq)
  - [46.8 Debug vaqti: eng qimmat va eng kam hisobga olinadigan](#468-debug-vaqti-eng-qimmat-va-eng-kam-hisobga-olinadigan)
  - [46.9 Amalda qo'llash](#469-amalda-qollash)
- [47. Birgalikda ishlash va o'rgatish (Collaboration and Mentoring)](#47-birgalikda-ishlash-va-orgatish-collaboration-and-mentoring)
  - [47.1 Kodga egalik: shaxsiy emas, jamoaviy](#471-kodga-egalik-shaxsiy-emas-jamoaviy)
  - [47.2 Ustoz-shogird modeli](#472-ustoz-shogird-modeli)
  - [47.3 Yangi odamga toza kod standartini yetkazish](#473-yangi-odamga-toza-kod-standartini-yetkazish)
  - [47.4 Review ni o'rgatish vositasiga aylantirish](#474-review-ni-orgatish-vositasiga-aylantirish)
  - [47.5 Jamoa kelishuvi (working agreement) yozish](#475-jamoa-kelishuvi-working-agreement-yozish)
  - [47.6 Amalda qo'llash](#476-amalda-qollash)

**[XIII. Ma'lumotnoma](#xiii-malumotnoma)**

- [48. Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari (Quick Reference)](#48-tezkor-malumotnoma-qoidalar-va-tekshiruv-royxatlari-quick-reference)
  - [48.1 Nomlash qoidalari jadvali](#481-nomlash-qoidalari-jadvali)
  - [48.2 Funksiya qoidalari jadvali](#482-funksiya-qoidalari-jadvali)
  - [48.3 Izoh qoidalari jadvali](#483-izoh-qoidalari-jadvali)
  - [48.4 Formatlash qoidalari jadvali](#484-formatlash-qoidalari-jadvali)
  - [48.5 Xato bilan ishlash jadvali](#485-xato-bilan-ishlash-jadvali)
  - [48.6 Hid → refaktoring moslik jadvali](#486-hid--refaktoring-moslik-jadvali)
  - [48.7 Commit oldidan tekshiruv ro'yxati](#487-commit-oldidan-tekshiruv-royxati)
  - [48.8 Review paytida tekshiruv ro'yxati (toza kod qismi)](#488-review-paytida-tekshiruv-royxati-toza-kod-qismi)
  - [48.9 Yangi sinf uchun tekshiruv ro'yxati](#489-yangi-sinf-uchun-tekshiruv-royxati)
  - [48.10 Terminlar lug'ati](#4810-terminlar-lugati)
  - [48.11 Besh hujjat bilan bog'lanish xaritasi](#4811-besh-hujjat-bilan-boglanish-xaritasi)
- [49. O'z-o'zini baholash: toza kod yetukligi (Self-Assessment)](#49-oz-ozini-baholash-toza-kod-yetukligi-self-assessment)
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

---

# I. Toza kodning asosi

## 1. Toza kod nima va nega qimmat (What Clean Code Is)

Toza kod haqidagi suhbat did haqidagi bahsga aylanib ketsa, u foydasiz. Shuning uchun bu bobda toza kodning o'lchanadigan ta'rifi beriladi: kod toza bo'lsa, uni o'qish tezligi va uni o'zgartirishdagi ishonch oshadi. Qolgan 48 bob shu ikki o'lchovni oshiradigan aniq qoidalar.

### 1.1 Toza kodning ishlaydigan ta'rifi

Toza kodni ta'riflashning eng ishonchli yo'li uni kuzatiladigan xatti-harakat orqali belgilash. Kod toza, agar uni birinchi marta ko'rgan odam debuggersiz o'qib tushunsa; o'zgartirish kiritishda u nimani buzishi mumkinligini oldindan ayta olsa; va o'zgartirishdan keyin test uni tasdiqlasa yoki rad etsa. Uchta shartning hech biri estetika haqida emas.

Shundan amaliy natija chiqadi. "Menga bu uslub yoqmaydi" argumenti toza kod argumenti emas. "Bu metodni o'qish uchun ikkita boshqa faylni ochish kerak" — toza kod argumenti, chunki o'qish narxini oshiradi. "Bu nomni o'zgartirsa, uch joyda kutilmagan xatti-harakat chiqadi" — toza kod argumenti, chunki o'zgartirish ishonchini pasaytiradi.

| Savol | Iflos kod | Toza kod |
|---|---|---|
| Bu metod nima qiladi? | Kodni o'qib taxmin qilaman | Nomi aytadi |
| Nimani buzishim mumkin? | Bilmayman | Imzo va test aytadi |
| Qayerdan boshlanadi? | Qidirish kerak | Kirish nuqtasi aniq |
| Xato bo'lsa nima bo'ladi? | `null` qaytadi, balki | Istisno turi e'lon qilingan |
| O'zgartirsam kim biladi? | Hech kim | Test yiqiladi |

### 1.2 Buzilgan deraza nazariyasi va kod bazasining eskirishi

Buzilgan deraza nazariyasi kod bazasiga aniq ko'chadi: bitta tuzatilmagan hid keyingi hidga ruxsat beradi. Mexanizm psixologik, lekin oqibati o'lchanadi. Kodda 30 ta `// TODO` bo'lsa, 31-chisini qo'shish arzon ko'rinadi. Bitta 2000 qatorli sinf bo'lsa, ikkinchisini yaratish qiyin bo'lmaydi, chunki standart allaqachon shu.

Shu sababli toza kod intizomi katta tozalash kampaniyalaridan emas, kichik va to'xtovsiz tuzatishlardan yig'iladi. Har bir tegilgan fayl bir nuqta yaxshilanib qolsa, kod bazasi yaxshilanish yo'nalishida turadi. Hech narsa tuzatilmasa, u faqat bitta yo'nalishda — pastga — qarab ketadi.

### 1.3 "Keyin tozalaymiz" nega hech qachon kelmaydi

"Hozir ishlatib yuboraylik, keyin tozalaymiz" gapi iqtisodiy jihatdan ishlamaydi, chunki tozalashni haqli qiladigan vaqt hech qachon paydo bo'lmaydi. Keyingi hafta yangi talab keladi, keyingi oy reliz bo'ladi. Qarzning foizi esa darhol to'lanadi: har bir yangi xususiyat iflos kod ustiga qurilib, uni o'chirish narxini oshiradi.

Amalda qoida teskari ishlaydi: tozalash ishning qismi, alohida ish emas. Agar vazifaga 6 soat ketadigan bo'lsa, u 6 soat ichida toza holatda tugashi kerak, 4 soat ishlaydigan va keyin 2 soat qarz holatida emas. Vaqt yetmasa, qamrov qisqartiriladi, sifat emas (45-bob).

### 1.4 Skaut qoidasi va imkoniyatli refaktoring

Skaut qoidasi (Boy Scout Rule): lagerdan ketganda uni topganingdan tozaroq qoldir. Kodga tatbiqi aniq: har bir PR da tegilgan faylda kamida bitta kichik yaxshilanish bo'lsin. Nomni aniqlashtirish, bir shartni nomlash, bitta o'lik metodni o'chirish, bitta magic number ni konstanta qilish.

Muhim cheklov bor: imkoniyatli tozalash **o'sha PR ning qamrovi ichida** qolishi kerak. 40 qatorli xato tuzatish 600 qatorli refaktoringga aylanib ketsa, review sifati tushadi va reliz kechadi. Qoida: tozalash tegilgan fayllarda va alohida commitda bo'ladi; katta refaktoring alohida PR ga chiqadi (13.6 va 38.4).

### 1.5 Toza kod va tez kod qarama-qarshi emas

"Toza kod sekin ishlaydi" da'vosi deyarli har doim o'lchanmagan. Haqiqat shunday: ishlash muammosi odatda 2-3 joyda to'planadi va o'lchov bilan topiladi; qolgan 97% kodning tezligi ahamiyatsiz. Toza kod esa shu 3 joyni topishni osonlashtiradi, chunki chegaralar aniq.

Shu bilan birga, toza kod "samarasiz kod" degani emas. Bu hujjatda tezlikka ta'sir qiladigan aniq qoidalar bor: `StringBuilder` qachon kerak (21.2), avtoboxing narxi (20.6), oqim va sikl tanlovi (7.7), N+1 va keraksiz fetch (28.4). Qoida: oldin to'g'ri va o'qiladigan, keyin o'lchov, keyin maqsadli optimizatsiya.

### 1.6 Toza kodning o'lchanadigan belgilari

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

### 1.7 Qoida, evristika va did farqi

Uch darajani ajratish bahsni qisqartiradi. **Qoida** — mashina tekshiradi va muhokama qilinmaydi: formatlash, import tartibi, `equals`/`hashCode` juftligi, resursni yopish. **Evristika** — odatda to'g'ri, lekin istisnosi bor: "funksiya 20 qatordan oshmasin". **Did** — shaxsiy va review da vaqt sarflashga arzimaydi: o'zgaruvchi nomining ohangi, qavs joylashuvi (allaqachon formatter hal qilgan).

Jamoada eng ko'p vaqt shu uchlik aralashganda yo'qoladi. Yechim: qoidalarni CI ga ko'chirish (42-bob), evristikalarni hujjatda yozib qo'yish (48-bob), did haqida bahsni to'xtatish.

### 1.8 Toza kodni kim uchun yozamiz

Toza kodning adresati aniq va u siz emas. U quyidagi odam: domenni yarim biladi, shu faylni birinchi marta ochadi, vaqti kam, va ehtimol production incident vaqtida o'qiyapti. Har bir qarorni shu odamni ko'z oldiga keltirib qabul qilish kerak.

Bu adresat ikkita amaliy natija beradi. Birinchi, kontekst kodda bo'lishi kerak, chatda yoki sizning xotirangizda emas. Ikkinchi, "men bilaman, shuning uchun tushunarli" argumenti kuchsiz: o'quvchi sizning bilimingizga ega emas.

### 1.9 Bu hujjat qolgan to'rttasi bilan qanday bo'linadi

Chegarani bilib turish takrorlanishni yo'qotadi va qidirishni tezlashtiradi.

| Savol | Qaysi hujjat |
|---|---|
| Bu nomni qanday yozaman? | shu hujjat, 2-3 bob |
| Nomni domen tilidan qanday olaman? | arxitektor hujjati, 4.2 |
| Bu yerda qaysi pattern kerak? | patternlar hujjati |
| SOLID nimani talab qiladi? | patternlar hujjati, 26-bob |
| Bu anti-pattern nomi nima? | patternlar hujjati, 25-bob |
| Chegarani qayerdan o'tkazaman? | arxitektor hujjati, 5-bob |
| Bu testni qanday yozaman? | testlash qo'llanmasi |
| Test kodi toza ko'rinishi kerak? | shu hujjat, 30-bob |
| Sonar nega shikoyat qilyapti? | SonarQube hujjati |
| Bu hidni qanday refaktoring qilaman? | shu hujjat, 32-38 bob |

### 1.10 Amalda qo'llash

- [ ] Kod bazasida 1.6 jadvalidagi sakkiz o'lchovni bir marta hisoblab, bugungi holatni yozib qo'ying.
- [ ] Eng katta 10 ta faylni `wc -l` bilan topib, ro'yxatni jamoaga ko'rsating va keyingi chorak maqsadini belgilang.
- [ ] Jamoa bilan qoida/evristika/did ajratimini kelishib, qoidalar ro'yxatini CI ga ko'chirish rejasini tuzing.
- [ ] Keyingi 10 ta PR da skaut qoidasini qo'llang: har birida tegilgan faylda bitta nomli yaxshilanish bo'lsin.
- [ ] "Keyin tozalaymiz" deb qoldirilgan joylarni bitta ro'yxatga yig'ib, har biriga egalik va muddat qo'ying.
- [ ] Review da "menga yoqmaydi" turidagi izohlarni to'xtatish uchun formatterni majburiy qiling (13-bob).
- [ ] Yangi odamning birinchi haftasida yozib olgan savollarini to'plab, javobi kodda yo'q bo'lganlarini kodga ko'chiring.
- [ ] Ishlash haqidagi har bir da'voni o'lchovsiz qabul qilmaslikni jamoa kelishuviga kiriting.
## 2. Nomlash qoidalari: maqsadni ochib beruvchi nom (Naming: Intention-Revealing Names)

Nomni domen tilidan olish qoidasi arxitektor hujjatida (4.2) yoritilgan. Bu bobda qolgan qism: nomning o'zini tekshirish uchun aniq qoidalar to'plami. Har bir qoida bitta aniq xatoni to'sadi va ularning hammasini review paytida bir daqiqada qo'llash mumkin.

### 2.1 Nom javob berishi kerak bo'lgan uchta savol

Yaxshi nom uchta savolga javob beradi: bu nima, nega mavjud, qanday ishlatiladi. Agar nomni ko'rib izoh yozish ehtiyoji tug'ilsa, nom shu uchta savoldan birini javobsiz qoldirgan. Izoh yozish o'rniga nomni o'zgartirish kerak.

```java
// yomon: uchta savolning hammasi javobsiz
int d;          // kunlar
List<int[]> l;  // nima?
boolean f;

// yaxshi: nom o'zi javob beradi, izoh kerak emas
int daysSinceLastPayment;
List<Cell> flaggedCells;
boolean shipmentAlreadyDispatched;
```

Tekshiruv usuli oddiy: nomni ovoz chiqarib o'qib, keyin "bu nima?" deb so'rang. Javob nomning o'zidan kelmasa, nom ishlamaydi.

### 2.2 Yolg'on ma'lumot beradigan nom

Nom noto'g'ri ma'lumot bersa, u yo'q nomdan ham yomon, chunki o'quvchi ishonadi va xato qiladi. Eng ko'p uchraydigan to'rt shakl bor: tur haqida yolg'on (`accountList` aslida `Set`), hajm haqida yolg'on (`cache` aslida bitta qiymat), xatti-harakat haqida yolg'on (`getUser` ichida yozadi), va vaqt haqida yolg'on (`currentBalance` aslida kechagi qoldiq).

```java
// yomon: nom tur haqida yolg'on gapiradi
Map<String, Customer> customerList;
// yomon: nom o'zgartirishni yashiradi
public Order getOrder(Long id) { order.touch(); return order; }

// yaxshi: nom haqiqatni aytadi
Map<CustomerId, Customer> customersById;
public Order findOrder(OrderId id);        // faqat o'qiydi
public Order markOrderSeen(OrderId id);   // o'zgartirishi nomda ko'rinadi
```

Shunga yaqin tuzoq: `l`, `O`, `I` harflari. Ular `1` va `0` bilan aralashadi va hech qanday shriftda ishonchli farqlanmaydi.

### 2.3 Ma'noli farq: `a1`, `a2`, `Info` va `Data`

Kompilyatorni qondirish uchun qo'shilgan farq odam uchun ma'lumot bermaydi. `source` va `destination` farq beradi; `a1` va `a2` bermaydi. `Product`, `ProductInfo` va `ProductData` uchligi esa eng zararli, chunki uchtasi bir xil narsani anglatadi va o'quvchi qaysi birini ishlatishni bilmaydi.

```java
// yomon: farq bor, ma'no yo'q
void copyChars(char[] a1, char[] a2) { ... }
class Product { } class ProductInfo { } class ProductData { }

// yaxshi: farq ma'noli
void copyChars(char[] source, char[] destination) { ... }
class Product { }             // domen entiteti
class ProductSummary { }      // ro'yxat uchun qisqa ko'rinish
class ProductCatalogEntry { } // tashqi katalogdagi yozuv
```

Agar ikkita nom orasidagi farqni bir gapda aytib bera olmasangiz, ikkitasidan biri keraksiz.

### 2.4 Shovqin so'zlar: `Info`, `Data`, `Object`, `Variable`, `The`

Shovqin so'z nomga uzunlik qo'shadi, ma'no qo'shmaydi. `theCustomer` va `customer`, `CustomerObject` va `Customer`, `nameString` va `name` juftliklarida ikkinchisi har doim yaxshiroq. `Manager`, `Helper`, `Util`, `Processor` qo'shimchalari arxitektor hujjatida (4.2) ko'rilgan; bu yerdagi ro'yxat ularning qolgani.

| Shovqin | Nega keraksiz | Almashtirish |
|---|---|---|
| `Info`, `Data` | hamma narsa ma'lumot | `Summary`, `Snapshot`, `Request` |
| `Object` | tur allaqachon ma'lum | olib tashlash |
| `the`, `a`, `an` | artikl ma'no bermaydi | olib tashlash |
| `nameString` | tur imzoda ko'rinadi | `name` |
| `moneyAmount` | takrorlash | `price`, `fee`, `total` |
| `doSomething` | ma'nosi yo'q | aniq fe'l |
| `temp`, `tmp` | umri yashirin | `scaledPrice` |
| `result`, `value`, `item` | kontekstsiz | `taxedTotal`, `orderLine` |
| `flag` | nimani belgilaydi? | `stockReserved` |
| `list2`, `map2` | farq ma'nosiz | rolga qarab nom |

### 2.5 Talaffuz qilinadigan nom

Nomni ovoz chiqarib aytib bo'lmasa, u haqida gaplasha olmaysiz. `genymdhms` nomi code review da "gen-y-m-d-h-m-s" ga aylanadi va suhbat buziladi. Talaffuz qilinadigan nom esa jamoa lug'atiga qo'shiladi: "generationTimestamp ni tekshirdingmi?" degan savol bir urinishda tushuniladi.

```java
// yomon: ovoz chiqarib aytish mumkin emas
private Date genymdhms;
private String pszqint;

// yaxshi: suhbatda ishlatiladi
private Instant generatedAt;
private String quarterlyIntervalCode;
```

### 2.6 Qidiriladigan nom va bir harfli o'zgaruvchi chegarasi

Nomning qiymati uni grep bilan topish mumkinligida ham. `e` harfini qidirib bo'lmaydi; `MAX_CLASSES_PER_STUDENT` ni esa bir urinishda topasiz. Shu sababli raqamli literal va bir harfli nomlar katta qamrovda yaramaydi.

Bir harfli nom faqat bitta holatda haqli: qamrov juda kichik va ma'nosi an'anaviy. Sikl hisoblagichi `i`, `j`; lambda ichidagi bitta argument; `catch` blokidagi `e`. Qamrov bir necha qatordan oshsa, nom to'liq yoziladi (3.15 va 2.15).

```java
// yomon: qidirib bo'lmaydi, ma'no yashirin
for (int j = 0; j < 34; j++) { s += (t[j] * 4) / 5; }

// yaxshi: har bir element qidiriladi va nomlangan
static final int WORK_DAYS_PER_WEEK = 5;
static final int REAL_DAYS_PER_IDEAL_DAY = 4;
int sum = 0;
for (int task = 0; task < NUMBER_OF_TASKS; task++) {
    int realTaskDays = taskEstimate[task] * REAL_DAYS_PER_IDEAL_DAY;
    sum += (realTaskDays / WORK_DAYS_PER_WEEK);
}
```

### 2.7 Kodlash va prefikslar: Hungarian notation, `m_`, `I` prefiksi

Nomga tur yoki qamrov haqidagi ma'lumotni kodlab yozish zamonaviy IDE da keraksiz va zararli: tur o'zgarsa prefiks yolg'onga aylanadi. `strName`, `iCount`, `m_description`, `_field` shakllari shu sababli chiqib ketdi.

Interfeys prefiksi alohida holat. `IOrderRepository` nomi o'quvchiga keraksiz ma'lumot beradi (bu interfeys ekani muhim emas) va implementatsiyani nomsiz qoldiradi. To'g'ri yechim: interfeys sof domen nomini oladi, implementatsiya mexanika nomini oladi.

```java
// yomon
public interface IOrderRepository { }
public class OrderRepositoryImpl implements IOrderRepository { }

// yaxshi: interfeys domen nomini oladi, implementatsiya mexanikani aytadi
public interface OrderRepository { }
public class JdbcOrderRepository implements OrderRepository { }
public class InMemoryOrderRepository implements OrderRepository { }  // test uchun
```

`Impl` qo'shimchasi faqat bitta implementatsiya bo'lib, uning mexanikasini ayta olmaydigan kam holatda haqli (3.6).

### 2.8 Aqliy tarjimani talab qiladigan nom

Agar o'quvchi nomni o'qib, ongda boshqa nomga aylantirishi kerak bo'lsa, nom ishlamaydi. Klassik misol: `for (int i...)` ichida `i` aslida "mijoz indeksi" ekanini eslab turish. Professional farqi shu: o'quvchi uchun aniq yozadi, o'zi uchun qisqa yozmaydi.

```java
// yomon: o'quvchi r nima ekanini eslab turadi
for (var r : rows) { if (r[2] != null) process(r); }

// yaxshi: tarjima kerak emas
for (PaymentRow payment : paymentRows) {
    if (payment.settledAt() != null) {
        process(payment);
    }
}
```

### 2.9 Sinf nomi ot, metod nomi fe'l, getter konvensiyasi

Konvensiya oddiy va istisnosi kam: sinf va record nomi ot yoki ot iborasi (`Invoice`, `PaymentGateway`, `OrderLine`), metod nomi fe'l yoki fe'l iborasi (`postPayment`, `deletePage`, `save`). Fe'l bo'lmagan metod nomi (`data()`, `info()`) nima qilishini aytmaydi.

Aksessor, mutator va predikat uchun JavaBean konvensiyasi: `getName`, `setName`, `isPosted`. Record va domen obyektlarida esa `get` prefiksini tashlab, maydon nomini ishlatish qabul qilingan: `order.total()`, `payment.settledAt()`. Muhimi — bitta kod bazasida bitta uslub.

```java
// konstruktor overload o'rniga nomlangan statik fabrika (nom maqsadni aytadi)
Complex fulcrumPoint = Complex.fromRealNumber(23.0);   // yaxshi
Complex fulcrumPoint = new Complex(23.0);              // yomon: 23.0 nima?
```

### 2.10 Hazil, jargon va madaniy havolalar

Hazilli nom bir kishiga tushunarli, qolganlarga yo'q. `whack()` o'rniga `kill()`, `eatMyShorts()` o'rniga `abort()` yozish kerak. Mahalliy jargon va qisqartmalar ham shu toifada: ular jamoadan chiqqach ma'nosini yo'qotadi.

Qoida: nom ikki yildan keyin, boshqa jamoada, boshqa tilda gaplashadigan odam uchun ham ishlashi kerak. Hazil shu sinovdan o'tmaydi.

### 2.11 Bitta tushunchaga bitta so'z

`get`, `fetch`, `retrieve`, `find`, `load`, `lookup` so'zlari bir xil narsani anglatsa, kod bazasida faqat bittasi qolishi kerak. Aks holda o'quvchi har safar "farq bormi?" deb o'ylaydi va IDE avtotoldirishi foydasiz bo'lib qoladi.

Shu bilan birga, agar farq bor bo'lsa, u izchil bo'lishi kerak. Keng tarqalgan izchil taqsimot quyidagicha.

| So'z | Ma'nosi | Topilmasa |
|---|---|---|
| `findX` | izlaydi, bo'lmasligi normal | `Optional.empty()` |
| `getX` | mavjudligi kafolatlangan | istisno |
| `loadX` | tashqi manbadan oladi | istisno |
| `fetchX` | tarmoq orqali oladi | istisno yoki `Optional` |
| `listX` | ko'p natija | bo'sh ro'yxat |
| `searchX` | mezon bo'yicha, sahifalangan | bo'sh sahifa |
| `createX` | yangi yaratadi | konflikt istisnosi |
| `ensureX` | yo'q bo'lsa yaratadi | idempotent |

### 2.12 So'z o'yini qilmaslik

Bitta so'zni ikki xil ma'noda ishlatish 2.11 ning teskarisi va xatosi ham shunchalik qimmat. `add` metodi bir joyda arifmetik qo'shishni, boshqa joyda to'plamga element qo'shishni bildirsa, o'quvchi har safar kodni o'qib tekshiradi.

```java
// yomon: add ikki xil ma'noda
Money add(Money other);                 // arifmetik
void add(OrderLine line);               // to'plamga qo'shish

// yaxshi: har bir amal o'z nomini oladi
Money plus(Money other);
void appendLine(OrderLine line);
```

### 2.13 Yechim domeni va muammo domeni nomlari

Ikki xil lug'at bor va ikkisi ham o'z o'rnida to'g'ri. Yechim domeni (informatika, pattern, texnologiya) nomlari texnik kodda yaxshi ishlaydi: `JobQueue`, `RetryPolicy`, `AccountVisitor`, `ConnectionPool`. Muammo domeni (biznes) nomlari domen kodida ishlaydi: `Invoice`, `SettlementBatch`, `CreditLimit`.

Xato ikki yo'nalishda bo'ladi. Domen sinfiga texnik nom berish (`OrderStrategyFactoryBean`) biznes ma'nosini yo'qotadi. Texnik sinfga biznes nomi berish (`OrderHelper` aslida HTTP klient) o'quvchini chalg'itadi. Qoida: nomni o'quvchining kim bo'lishiga qarab tanlang.

### 2.14 Kontekst qo'shish va ortiqcha kontekst qo'shmaslik

Nom o'z-o'zidan yetarli kontekst bermasa, uni qo'shish kerak — lekin prefiks bilan emas, tur yoki paket bilan. `state` o'zi noaniq; `Address` sinfi ichidagi `state` esa aniq.

```java
// yomon: har bir maydonga prefiks qo'yilgan
class Address {
    private String addrFirstName;
    private String addrState;
}

// yaxshi: kontekst sinfdan keladi
class Address {
    private String firstName;
    private String state;
}
```

Teskari xato ham bor: ortiqcha kontekst. `GasStationDeluxe` ilovasida har bir sinfni `GSD` prefiksi bilan boshlash avtotoldirishni buzadi va hech narsa qo'shmaydi. Paket nomi allaqachon kontekst beradi.

### 2.15 Nom uzunligi qamrovga mutanosib

Amaliy qoida: nom uzunligi uning qamrovi (scope) ga mutanosib bo'lishi kerak. Uch qatorli blok ichidagi o'zgaruvchi qisqa nom ola oladi; `public static final` maydon yoki public API metodi to'liq va aniq nom talab qiladi.

| Qamrov | Nom uzunligi | Misol |
|---|---|---|
| Lambda argumenti, 1 qator | 1-2 harf | `p -> p.isSettled()` |
| Sikl hisoblagichi | 1 harf | `i`, `j` |
| Metod ichidagi mahalliy, 3-10 qator | bir so'z | `total`, `draft` |
| Metod ichidagi mahalliy, uzun | ikki-uch so'z | `taxedOrderTotal` |
| Maydon | ikki-uch so'z | `paymentRetryPolicy` |
| Public metod | to'liq ibora | `reserveStockForOrder` |
| Public konstanta | to'liq, birlik bilan | `DEFAULT_READ_TIMEOUT_MS` |
| Sinf | ot iborasi | `SettlementBatchImporter` |

### 2.16 Amalda qo'llash

- [ ] Kod bazasida `Info`, `Data`, `Object`, `temp`, `flag`, `result` so'zlarini grep qilib, har birini rolga qarab qayta nomlang.
- [ ] `IOrderRepository` turidagi interfeys prefikslarini olib tashlab, implementatsiyalarga mexanika nomini bering (`JdbcOrderRepository`).
- [ ] `get`/`find`/`fetch`/`load` so'zlarining joriy ishlatilishini sanab, 2.11 jadvalidagi bitta izchil taqsimotni kelishib oling va qolganini qayta nomlang.
- [ ] Bir harfli o'zgaruvchilarni qamrovi 5 qatordan oshganlarini topib, to'liq nomga o'tkazing.
- [ ] `m_`, `str`, `i`, `_` prefikslarini Checkstyle qoidasi bilan taqiqlang (13.4).
- [ ] Bir xil tushuncha uchun ikki nom ishlatilgan joylarni (`Product`/`ProductInfo`) birlashtiring yoki farqini bir gapda hujjatlashtiring.
- [ ] Har bir public konstanta nomida birlik borligini tekshiring (`...Ms`, `...Bytes`, `...Percent`).
- [ ] Jamoa lug'atini (glossary) fayl sifatida repoga qo'shib, har bir yangi domen atamasini shu yerda qayd eting (3.14).
## 3. Nom turlari bo'yicha aniq konvensiyalar (Naming Conventions by Kind)

Oldingi bob nomning umumiy sifatini tekshirdi. Bu bobda har bir nom turi uchun alohida konvensiya beriladi: mantiqiy qiymat, to'plam, konstanta, enum, interfeys, generik parametr, istisno, paket, fayl. Konvensiya bo'lmasa, har bir ishlab chiquvchi o'z uslubini kiritadi va kod bazasi bir necha dialektga bo'linadi.

### 3.1 Mantiqiy nomlar: `is`, `has`, `can`, `should` va inkor tuzog'i

Mantiqiy qiymat nomi gap bo'lishi kerak, shunda `if` ichida o'qilishi tabiiy chiqadi. To'rtta prefiks yetarli: `is` (holat), `has` (egalik), `can` (ruxsat yoki imkoniyat), `should` (siyosat qarori). `was`, `will` va `requires` ham qo'shiladi, lekin faqat ma'nosi aniq bo'lganda.

Eng qimmat xato — inkor nom. `isNotValid`, `disableCache`, `notFound` nomlari `if (!isNotValid)` kabi ikki marta inkorga olib keladi va o'quvchi xato o'qiydi. Qoida: nom har doim ijobiy shaklda, inkor `!` operatorida qoladi.

```java
// yomon
boolean isNotEligible;
boolean disableRetry;
if (!isNotEligible && !disableRetry) { ... }   // ikki inkor

// yaxshi
boolean eligible;
boolean retryEnabled;
if (eligible && retryEnabled) { ... }
```

| Prefiks | Ma'nosi | Misol |
|---|---|---|
| `is` | hozirgi holat | `isSettled`, `isExpired` |
| `has` | egalik, mavjudlik | `hasActiveSubscription` |
| `can` | imkoniyat, ruxsat | `canBeCancelled` |
| `should` | siyosat qarori | `shouldRetry` |
| `was` | o'tgan holat | `wasDelivered` |
| `requires` | talab | `requiresManualReview` |
| sifat | holat sifati | `empty`, `blank`, `stale` |

### 3.2 To'plam, massiv va oqim nomlari

To'plam nomi ko'plikda bo'ladi va tur nomini takrorlamaydi. `orders` yetarli; `orderList` esa `List` dan `Set` ga o'tganda yolg'onga aylanadi (2.2). Map uchun esa kalit va qiymat munosabatini nomda ko'rsatish kerak, chunki `Map<A,B>` o'zi yetarli emas.

```java
List<Order> orders;                       // yaxshi
Set<Sku> reservedSkus;                    // yaxshi
Map<CustomerId, List<Order>> ordersByCustomer;   // kalit → qiymat nomda
Map<Sku, Integer> availableQuantityBySku;        // qiymat ma'nosi nomda
Stream<Payment> settledPayments;          // oqim ham ko'plikda
```

Agar to'plamning roli alohida bo'lsa, rol nomi ko'plikdan ustun: `shippingQueue`, `auditTrail`, `priceHistory`.

### 3.3 Birlik nomda: `timeoutMs`, `sizeBytes`, `priceMinor`

Birlik nomda bo'lmasa, uni ongda saqlash kerak bo'ladi va bu eng ko'p uchraydigan production xatolarining manbai: sekundni millisekund deb berish, so'mni tiyin deb hisoblash, bayt va kilobaytni aralashtirish.

```java
// yomon: birlik yashirin
void setTimeout(long timeout);
long size;
BigDecimal price;

// yaxshi: birlik nomda yoki turda
void setReadTimeout(Duration readTimeout);     // eng yaxshi: tur birlikni ushlaydi
void setReadTimeoutMs(long readTimeoutMs);     // ikkinchi yaxshi: nomda
long sizeBytes;
long priceMinorUnits;                          // tiyin
Money price;                                   // eng yaxshi: value object
```

Qoida tartibi: birlikni turga ko'chirish (`Duration`, `Money`, `Percentage`) eng yaxshi; nomga yozish ikkinchi; hech qayerda yozmaslik xato.

### 3.4 Konstanta, `static final` va enum a'zolari

Java konvensiyasi: `UPPER_SNAKE_CASE` faqat haqiqiy konstantalar uchun, ya'ni kompilyatsiya vaqtida ma'lum va o'zgarmas qiymatlar. O'zgarmas, lekin ish vaqtida hisoblanadigan maydon (`private final Clock clock`) oddiy `camelCase` oladi.

Konstanta nomi uning ma'nosini, qiymatini emas, aytishi kerak. `THREE = 3` foydasiz; `MAX_RETRY_ATTEMPTS = 3` foydali. Qiymatni nomda takrorlash (`TIMEOUT_30 = 30`) qiymat o'zgarganda nomni yolg'onga aylantiradi.

```java
// yomon
static final int THREE = 3;
static final int TIMEOUT_30 = 30;
static final String S = "ERROR";

// yaxshi: ma'no, birlik va asos
static final int MAX_RETRY_ATTEMPTS = 3;
static final Duration GATEWAY_READ_TIMEOUT = Duration.ofSeconds(30);
static final String SETTLEMENT_FAILED_CODE = "SETTLEMENT_FAILED";
```

Konstantani interfeysga qo'yib voris olish (constant interface) qoldirilgan amaliyot (17.8). Konstantalar `enum` ga yoki `final` utility sinfga yoki eng yaxshisi tegishli domen sinfiga joylashadi.

### 3.5 Enum turi va holat nomlari

Enum turi birlikda nomlanadi, chunki u bitta qiymatning turini bildiradi: `OrderStatus`, `PaymentMethod`, `Currency` — `OrderStatuses` emas. A'zolari esa `UPPER_SNAKE_CASE` va ma'nosi domen tilida: `PENDING`, `AWAITING_SETTLEMENT`, `PARTIALLY_REFUNDED`.

Enum a'zosi nomida qisqartma va texnik kod yashirmaslik kerak. `S1`, `S2` ma'nosiz; agar bazada raqamli kod saqlanishi kerak bo'lsa, kodni enum ichidagi maydonga olib, nomni o'qiladigan qoldirish kerak.

```java
public enum SettlementStatus {
    PENDING(0),
    SETTLED(1),
    REJECTED(2),
    PARTIALLY_REFUNDED(3);

    private final int legacyCode;   // bazadagi raqam alohida maydonda

    SettlementStatus(int legacyCode) { this.legacyCode = legacyCode; }

    public int legacyCode() { return legacyCode; }
}
```

### 3.6 Interfeys va implementatsiya nomlari: `Impl` qachon haqli

Interfeys domen rolini oladi, implementatsiya esa shu rolni **qanday** bajarishini aytadi. Shunday bo'lsa, `Impl` qo'shimchasi o'z-o'zidan keraksiz bo'lib qoladi: `OrderRepository` / `JdbcOrderRepository`, `PriceCalculator` / `TieredPriceCalculator`, `NotificationSender` / `SmtpNotificationSender`.

`Impl` faqat bitta holatda haqli: implementatsiya bitta va uning mexanikasini ayta olmaydigan darajada oddiy (masalan interfeys faqat test uchun ajratilgan). Bunda ham ko'pincha yaxshiroq yechim bor: interfeysni umuman yozmaslik va sinfning o'zini ishlatish (arxitektor hujjati 5.7).

| Interfeys | Yaxshi implementatsiya nomi | Yomon |
|---|---|---|
| `OrderRepository` | `JdbcOrderRepository` | `OrderRepositoryImpl` |
| `PaymentGateway` | `StripePaymentGateway` | `PaymentGatewayImpl` |
| `ExchangeRateProvider` | `CachingExchangeRateProvider` | `DefaultExchangeRateProvider` |
| `AuditLog` | `DatabaseAuditLog` | `AuditLogImpl` |
| `Clock` | `FixedClock`, `SystemClock` | `ClockImpl` |

`Default` prefiksi ham shu toifada: u mexanikani emas, mualliflik tartibini aytadi.

### 3.7 Abstrakt sinf va `Abstract` prefiksi

`AbstractOrderProcessor` nomi o'quvchiga texnik ma'lumot beradi (bu sinfni instantiate qilib bo'lmaydi) va bu ba'zan foydali, chunki voris yozmoqchi odam darhol tushunadi. Shuning uchun Java ekotizimida `Abstract` prefiksi qabul qilingan va undan voz kechish kerak emas.

Lekin ikki qoida bor. Birinchi, `Abstract` prefiksi faqat haqiqatan voris olish uchun mo'ljallangan sinfda bo'ladi; "umumiy kodni qo'yish uchun" yaratilgan bazaviy sinf esa odatda kompozitsiyaga aylantirilishi kerak (17.9). Ikkinchi, nomning qolgan qismi hali ham rolni aytishi kerak: `AbstractTemplate` ma'nosiz.

### 3.8 Generik tur parametrlari

Bir harfli generik nomlar an'ana bo'lib qolgan va ularni saqlash kerak: `T` (type), `E` (element), `K`/`V` (key/value), `R` (result), `U` (ikkinchi tur), `N` (number). Bitta yoki ikkita parametrda bu yetarli.

Parametr soni ikkitadan oshsa yoki ma'nosi noaniq bo'lsa, to'liq nom yozish kerak. Konvensiya: bitta katta harf bilan boshlanadigan so'z yoki so'z + `T`.

```java
// an'anaviy va yetarli
public interface Repository<T, ID> { Optional<T> findById(ID id); }

// parametr soni ko'p: ma'noli nom o'qilishni saqlaydi
public interface Pipeline<InputT, OutputT, ContextT> {
    OutputT run(InputT input, ContextT context);
}
```

### 3.9 Metod nomi va qaytish turi muvofiqligi

Nom qaytish turiga mos bo'lmasa, o'quvchi chalg'iydi. `getOrders()` bitta `Order` qaytarsa, `isValid()` `String` qaytarsa, `save()` `void` emas `Long` qaytarsa — har birida yashirin shartnoma bor va u nomda ko'rinmaydi.

| Qaytish turi | Nom shakli | Misol |
|---|---|---|
| `boolean` | `is`/`has`/`can` | `isSettled()` |
| `Optional<T>` | `find` | `findByEmail()` |
| `T` (kafolatlangan) | `get`/`require` | `getById()`, `requireActive()` |
| `List<T>` | ko'plik | `findAllPending()` |
| `void` (o'zgartiradi) | buyruq fe'li | `cancel()`, `markShipped()` |
| `long`/`int` (son) | `count`/`size` | `countPending()` |
| yangi obyekt | `to`/`as`/`with` | `toDto()`, `withDiscount()` |
| yon ta'sirli va qiymatli | ikkiga bo'lish | `reserve()` + `reservationId()` |

Oxirgi qator buyruq-so'rov ajratilishiga (patternlar hujjati 26.23) ishora qiladi: bir metod ham o'zgartirsa, ham qiymat qaytarsa, nomi ikkisini ham aytolmaydi.

### 3.10 Istisno sinflari nomlari

Istisno nomi `Exception` bilan tugaydi va muammoni aytadi, sababini emas. `OrderException` nima bo'lganini aytmaydi; `OrderAlreadyShippedException` aytadi. Nom shunday aniq bo'lsa, `catch` bloki ham aniq bo'ladi va xato bilan ishlash shartlari kodda ko'rinadi.

```java
// yomon: bir istisno hamma holat uchun
throw new OrderException("xato");

// yaxshi: har bir holat o'z turida, kontekst konstruktorda
throw new OrderAlreadyShippedException(orderId, shippedAt);
throw new InsufficientStockException(sku, requested, available);
throw new PaymentDeclinedException(paymentId, gatewayCode);
```

Texnik istisnolarda `Failure` yoki `Error` emas, `Exception` qo'shimchasi qolaveradi; `Error` nomi JVM `java.lang.Error` ierarxiyasini anglatadi va chalkashtiradi.

### 3.11 Paket, modul va artefakt nomlari

Paket nomi kichik harflarda, ko'plik yoki birlikda izchil, va xususiyatni anglatadi (arxitektor hujjati 4.8 paketni xususiyat bo'yicha bo'lishni ko'rib chiqadi). Bu yerda qolgan konvensiyalar: qisqartma yo'q, kamalak (`com.company.project.service.impl.v2`) yo'q, `util` paketiga hamma narsani tashlash yo'q.

| Daraja | Konvensiya | Misol |
|---|---|---|
| Guruh | teskari domen | `uz.shop` |
| Modul | xususiyat yoki kontekst | `uz.shop.payment` |
| Ichki qatlam | rol | `uz.shop.payment.api`, `...payment.internal` |
| Artefakt (Maven) | modul nomi bilan bir xil | `shop-payment` |
| Jar/image nomi | artefakt + versiya | `shop-payment:1.4.2` |
| Test paketi | ishlab chiqarish bilan bir xil | `uz.shop.payment` |
| Konfiguratsiya prefiksi | modul nomi | `shop.payment.gateway.*` |

### 3.12 Test metodi va test sinfi nomlari

Test nomlash konvensiyalari testlash qo'llanmasida (5.3) berilgan. Bu yerda faqat nomlash nuqtai nazaridan ikki qo'shimcha qoida bor. Birinchi, test nomi texnik emas, xatti-harakat tilida bo'lishi kerak: `shouldRejectRefundExceedingSettledAmount`, `test1` emas. Ikkinchi, test sinfi nomi sinab ko'rilayotgan sinfga bog'lanadi: `OrderPricingTest`, `OrderPricingIT` (integratsion).

### 3.13 Fayl, resurs va konfiguratsiya kaliti nomlari

Kod tashqarisidagi nomlar ham o'sha qoidalarga bo'ysunadi, lekin o'z konvensiyasi bor.

| Narsa | Konvensiya | Misol |
|---|---|---|
| Java fayl | public sinf nomi | `OrderPricing.java` |
| Flyway migratsiya | `V<versiya>__<fe'l>_<obyekt>` | `V12__add_settled_at_to_payment.sql` |
| Property kaliti | `kebab-case`, modul prefiksi | `shop.payment.read-timeout` |
| Env o'zgaruvchi | `UPPER_SNAKE` | `SHOP_PAYMENT_READ_TIMEOUT` |
| Jadval, ustun | `snake_case`, birlikda jadval | `payment`, `settled_at` |
| Indeks | `ix_<jadval>_<ustunlar>` | `ix_payment_order_id` |
| Cheklov | `ck_`, `fk_`, `uq_` prefiks | `uq_payment_idempotency_key` |
| Metrika | `<domen>_<obyekt>_<birlik>` | `payment_settlement_seconds` |
| Log kaliti | `camelCase` yoki `snake_case`, izchil | `orderId` |
| Feature flag | `<modul>.<xususiyat>.enabled` | `payment.instant-refund.enabled` |

### 3.14 Jamoa lug'ati va uni majburlash

Nomlash qoidalari lug'at bo'lmasa, har bir ishlab chiquvchining xotirasiga tayanadi. Shuning uchun repoda `docs/glossary.md` fayli turishi kerak: har bir domen atamasi, uning ingliz tilidagi kod shakli, va nima **emasligi**.

```markdown
| Atama (biznes) | Kodda | Ma'nosi | Aralashtirmaslik kerak |
|---|---|---|---|
| Qoldiq | `availableQuantity` | sotishga tayyor miqdor | `onHandQuantity` bilan |
| Rezerv | `reservedQuantity` | buyurtmaga ajratilgan | `availableQuantity` bilan |
| Hisob-kitob | `settlement` | bank bilan yopilishi | `payment` bilan |
| Qaytarish | `refund` | pulni qaytarish | `cancellation` bilan |
```

Majburlash uchun ikki vosita bor: review paytida lug'atga havola qilish, va ArchUnit yoki custom lint qoidasi bilan taqiqlangan nomlarni bloklash (42.4).

### 3.15 Nomni o'zgartirish intizomi

Nomni yaxshilash eng arzon refaktoring, lekin faqat to'g'ri bajarilganda. Uch qoida: IDE refaktoringi bilan qilish (qo'lda almashtirish satr literallarini ham o'zgartirib qo'yadi), alohida commit qilish (mantiq o'zgarishi bilan aralashmasin, 40.1), va public API bo'lsa deprecate siklidan o'tish (arxitektor hujjati 13.9).

```bash
# Nomni o'zgartirish commiti faqat nom o'zgarishini o'z ichiga oladi.
# Diff ni tekshirish: mantiq o'zgarmaganiga ishonch
git show --stat HEAD
git diff HEAD~1 -- '*.java' | grep -E '^\+' | grep -vE 'rename|Rename' | head

# Satr literallari va reflektiv havolalarni alohida tekshirish
grep -rn "orderManager" --include=*.java --include=*.yml --include=*.sql src/
```

### 3.16 Amalda qo'llash

- [ ] Barcha mantiqiy maydon va metodlarni ko'rib, inkor nomlarni (`isNot...`, `disable...`) ijobiy shaklga o'tkazing.
- [ ] Vaqt, hajm va pul bilan ishlaydigan public imzolarda birlikni turga ko'chiring: `Duration`, `Money`, `Percentage`.
- [ ] `...Impl` va `Default...` nomli sinflarni topib, har biriga mexanikasini aytuvchi nom bering.
- [ ] Enum a'zolari ichida raqamli yoki qisqartma nomlar bo'lsa, kodni ichki maydonga ko'chirib nomni o'qiladigan qiling.
- [ ] `docs/glossary.md` yaratib, domen eksperti ishlatadigan 20 atamani kod shakli bilan yozib qo'ying.
- [ ] Metod nomlari va qaytish turlari muvofiqligini 3.9 jadvali bo'yicha tekshirib, mos kelmaganlarini qayta nomlang.
- [ ] Flyway, property, jadval va metrika nomlanishini 3.13 jadvaliga moslab, farqlarni bitta migratsiyada tuzating.
- [ ] Nom o'zgartirish uchun alohida commit qoidasini jamoa kelishuviga kiritib, PR shabloniga eslatma qo'shing.
# II. Funksiya va boshqaruv oqimi

## 4. Funksiya: kichiklik va bitta ish (Functions: Small and Doing One Thing)

Metod uzunligi, ichma-ich shartlar va erta qaytish arxitektor hujjatida (4.4) ko'rib chiqilgan. Bu bobda funksiya qoidalarining qolgan qismi: "bitta ish qiladi" ni qanday tekshirish, pastga tushish qoidasi, ajratib olish mexanikasi va funksiyani toza holatga keltirish tartibi.

### 4.1 Birinchi qoida: kichik; ikkinchi qoida: yana kichikroq

Funksiyaning to'g'ri uzunligi haqida aniq son berish qiyin, lekin kuzatish bor: toza kod bazalarida funksiyalarning katta qismi 4-12 qator oralig'ida bo'ladi va har biri bir ekranga sig'adi. Shu hajmda funksiya nomi uning butun mazmunini qamrab oladi, test yozish oson bo'ladi va qayta ishlatish imkoniyati paydo bo'ladi.

Kichik funksiyadan qo'rqishning odatiy sababi — "juda ko'p metod bo'lib ketadi". Amalda esa teskari natija chiqadi: metodlar soni oshadi, lekin har birining o'qish narxi tushadi va jami o'qish vaqti qisqaradi. Bundan tashqari, nomlangan kichik funksiya izohni almashtiradi (8.2).

```java
// yomon: bitta funksiya to'rt ishni bajaradi, 30+ qator
public void processOrder(Order order) {
    if (order.getItems().isEmpty()) throw new IllegalArgumentException();
    BigDecimal total = BigDecimal.ZERO;
    for (OrderItem item : order.getItems()) {
        total = total.add(item.getPrice().multiply(BigDecimal.valueOf(item.getQty())));
    }
    if (order.getCustomer().getTier().equals("GOLD")) {
        total = total.multiply(new BigDecimal("0.9"));
    }
    order.setTotal(total);
    jdbc.update("update orders set total = ? where id = ?", total, order.getId());
    mailSender.send(order.getCustomer().getEmail(), "Buyurtma qabul qilindi", "...");
}

// yaxshi: har bir qadam nomlangan, asosiy funksiya hikoyani aytadi
public void placeOrder(Order order) {
    requireNonEmpty(order);
    Money total = pricing.totalFor(order);
    order.applyTotal(total);
    orderRepository.save(order);
    notifications.orderAccepted(order);
}
```

### 4.2 "Bitta ish qiladi" ni qanday tekshirish

"Bitta ish" ta'rifi noaniq ko'rinadi, lekin aniq sinovi bor: funksiyadan ma'noli nom bilan boshqa funksiya ajratib olish mumkin bo'lsa va u shunchaki asl funksiyaning qayta ifodasi bo'lmasa, demak funksiya bir necha ish qilayotgan edi.

Ikkinchi sinov abstraksiya darajasida: funksiya ichidagi barcha gaplar nom aytgan abstraksiyadan **bir daraja pastda** bo'lishi kerak (patternlar hujjati 26.28 shu printsipni ta'riflaydi). `placeOrder` ichida `jdbc.update(...)` turishi ikki darajani buzadi, chunki SQL "buyurtma berish" dan ikki daraja past.

```java
// yomon: uchta daraja bir funksiyada (siyosat, mapping, SQL)
public Money priceFor(OrderDraft draft) {
    var rate = jdbcTemplate.queryForObject(
            "select rate from tax_rate where region = ?", BigDecimal.class, draft.region());
    Money net = draft.lines().stream().map(this::lineTotal).reduce(Money.ZERO, Money::add);
    return net.add(net.multiply(rate));
}

// yaxshi: bir funksiya - bir daraja
public Money priceFor(OrderDraft draft) {
    Money net = netAmountOf(draft);
    return net.add(taxPolicy.taxFor(draft.region(), net));
}
```

### 4.3 Bo'limlari bor funksiya bitta ish qilmaydi

Agar funksiya ichida `// --- validatsiya ---`, `// --- hisoblash ---`, `// --- saqlash ---` kabi izohli bo'limlar paydo bo'lsa, bu eng ishonchli signal: bo'limlar aslida alohida funksiyalar bo'lishi kerak va izohlar ularning nomi bo'ladi. Shu almashtirish izohni ham, uzunlikni ham bir vaqtda yo'qotadi.

Shu signalning boshqa shakllari: funksiya ichida bo'sh qatorlar bilan ajratilgan guruhlar, `region` yoki `#region` belgilari (9.7), va funksiya boshida "bu funksiya quyidagini qiladi: 1) ... 2) ..." izohi.

### 4.4 Pastga tushish qoidasi va gazeta metaforasi

Kod gazeta kabi o'qilishi kerak: sarlavha eng umumiy, keyin asosiy mazmun, oxirida mayda tafsilot. Funksiyalar uchun bu "pastga tushish qoidasi" (stepdown rule) deb ataladi: har bir funksiya o'zidan keyin keladigan funksiyalarni chaqiradi va har bir qadamda abstraksiya darajasi bir pog'ona tushadi.

```java
public final class SettlementImporter {

    // 1-daraja: butun jarayon
    public void importDailyFile(Path file) {
        List<SettlementRow> rows = parse(file);
        List<SettlementRow> valid = rejectInvalid(rows);
        apply(valid);
    }

    // 2-daraja: har bir qadamning mazmuni
    private List<SettlementRow> parse(Path file) { ... }
    private List<SettlementRow> rejectInvalid(List<SettlementRow> rows) { ... }
    private void apply(List<SettlementRow> rows) { ... }

    // 3-daraja: mayda tafsilot
    private boolean hasKnownCurrency(SettlementRow row) { ... }
}
```

Shu tartib buzilsa, o'quvchi faylni yuqoriga-pastga aylantirib o'qiydi va kontekstni yo'qotadi.

### 4.5 Funksiyadan funksiya chiqarish mexanikasi

Ajratish (extract) eng ko'p ishlatiladigan refaktoring va uning xavfsiz tartibi bor. Birinchi, ajratilayotgan qatorlarni belgilab, ular ishlatadigan mahalliy o'zgaruvchilarni aniqlash. Ikkinchi, ulardan nechtasi o'zgartirilayotganini sanash: bittasi bo'lsa qaytish qiymatiga aylanadi, bir nechtasi bo'lsa oldin o'zgaruvchilarni bo'lish kerak (35-bob). Uchinchi, IDE refaktoringi bilan bajarish. To'rtinchi, nomni mazmunga qarab emas, **maqsadga** qarab tanlash.

```java
// Ajratishdan oldin: nima qilayotgani kodda, nega qilayotgani yo'q
if (order.createdAt().isBefore(now.minusDays(30))
        && order.status() == OrderStatus.PENDING) {
    order.expire();
}

// Ajratishdan keyin: nom maqsadni aytadi
if (isStalePending(order)) {
    order.expire();
}

private boolean isStalePending(Order order) {
    return order.status() == OrderStatus.PENDING
            && order.createdAt().isBefore(clock.instant().minus(STALE_AFTER));
}
```

Ajratishdan keyin darhol tekshirish: yangi funksiya nomi `And`, `Or`, `Then` so'zlarini o'z ichiga olmasligi kerak. Olsa, u bitta ish qilmaydi.

### 4.6 Funksiya nomi uzunligi va aniqligi

Private funksiya nomi uzun bo'lishi mumkin va bo'lishi kerak, chunki u faqat bir joyda chaqiriladi va uning vazifasi izohni almashtirish. `includeSetupAndTeardownPages` nomi uzun, lekin izohdan arzon.

Nomni tanlashning amaliy usuli: funksiyani izoh bilan tasvirlab ko'ring, keyin shu izohni nomga aylantiring. Izoh "yaroqsiz qatorlarni olib tashlaydi va qolganini qaytaradi" bo'lsa, nom `rejectInvalidRows` bo'ladi.

### 4.7 Funksiya qaytish nuqtalari: bitta `return` afsonasi

"Funksiyada bitta `return` bo'lishi kerak" qoidasi strukturali dasturlash davridan qolgan va kichik funksiyalarda zarar qiladi: u guard clause ni (arxitektor hujjati 4.4) imkonsiz qiladi va ichma-ich shartlarni ko'paytiradi.

Haqiqiy qoida boshqa: funksiya kichik bo'lsa, bir necha `return` muammo emas. Muammo faqat katta funksiyada paydo bo'ladi, chunki o'quvchi chiqish nuqtalarini sanab chiqolmaydi. Shu sababli yechim `return` sonini kamaytirish emas, funksiyani kichraytirish.

```java
// yaxshi: uchta return, lekin funksiya kichik va har biri aniq
Optional<Discount> bestDiscount(Customer customer, Money total) {
    if (customer.isBlocked()) return Optional.empty();
    if (total.isLessThan(MIN_DISCOUNTABLE)) return Optional.empty();
    return discounts.stream().filter(d -> d.appliesTo(customer)).max(byAmount());
}
```

### 4.8 Funksiya ichidagi bo'sh joy, blok va qavs

`if`, `else`, `while` bloklari bir qatordan oshmasligi kerak, va o'sha bir qator ko'pincha funksiya chaqiruvi bo'ladi. Bu qoida ichma-ich chuqurlikni avtomatik ravishda bir darajada ushlab turadi.

Qavslarni tashlab yuborish (`if (x) doIt();`) esa alohida xato manbasi: keyingi o'zgartirishda ikkinchi qator qo'shiladi va shart faqat birinchisiga tegib qoladi. Qoida: har doim qavs, hatto bir qator uchun ham. Buni Checkstyle `NeedBraces` qoidasi majburlaydi.

```java
// yomon: qavssiz, keyingi o'zgartirishda xato tug'ilgan
if (!order.isPaid())
    log.warn("to'lanmagan buyurtma {}", order.id());
    reject(order);              // har doim bajariladi!

// yaxshi
if (!order.isPaid()) {
    log.warn("to'lanmagan buyurtma {}", order.id());
    reject(order);
}
```

### 4.9 Yordamchi funksiyalar soni va joylashuvi

Private yordamchi funksiyalar ko'payishi muammo emas; ularning joylashuvi muammo bo'ladi. Qoida: har bir private funksiya o'zini chaqiradigan funksiyadan **keyin**, iloji boricha yaqin turadi (11.7). Shunda o'quvchi yuqoridan pastga bir yo'nalishda o'qiydi.

Ikkinchi qoida: agar private funksiyalar guruhi o'z holicha mantiqiy butunlik hosil qilsa va sinfning asosiy vazifasiga tegishli bo'lmasa, ular alohida sinfga chiqishi kerak. Sinfda 15 ta private metod bo'lsa, ehtimol ichida yashiringan sinf bor.

### 4.10 Funksiyani birinchi urinishda toza yozish mumkin emas

Toza funksiya birdan yozilmaydi va bunga urinish vaqtni yo'qotadi. Ishlaydigan tartib: oldin ishlaydigan, chuqur va chirkin versiyani yozish; testlar bilan qotirish; keyin nomlarni aniqlashtirish, ajratish, tartiblash. Testlar bo'lmasa, bu tozalash xavfli bo'ladi.

Shu tartib TDD da tabiiy chiqadi (31-bob): yashil holatda refaktoring bepul, chunki har qadamdan keyin test tasdiqlaydi.

### 4.11 Amalda qo'llash

- [ ] Kod bazasidagi eng uzun 20 ta metodni topib (`awk` yoki IDE metrikasi), har birida 4.3 dagi "bo'lim izohi" signalini qidiring.
- [ ] Har bir topilgan bo'limni alohida private metodga chiqarib, izohni metod nomiga aylantiring.
- [ ] Sinflarda metodlar tartibini pastga tushish qoidasiga keltiring: chaqiruvchi yuqorida, chaqiriladigan pastda.
- [ ] `if`/`for`/`while` bloklarida qavs yo'q joylarni Checkstyle `NeedBraces` bilan taqiqlang va mavjudlarini tuzating.
- [ ] Nomida `And`, `Or`, `Then` bor metodlarni grep qilib, ularni ikki metodga bo'ling.
- [ ] 15 dan ko'p private metodi bor sinflarni ro'yxatlab, ichida yashiringan sinfni ajratish variantini ko'rib chiqing.
- [ ] Bir funksiya ichida SQL, HTTP va biznes qoidasi birga turgan joylarni topib, darajalarni ajratib bering.
- [ ] Yangi kod uchun "bir funksiya bir ekranga sig'adi" qoidasini review checklistiga kiritib, istisnolarni izohlashni talab qiling.
## 5. Funksiya argumentlari (Function Arguments)

Uzun parametr ro'yxati patternlar hujjatida anti-pattern sifatida sanalgan (25.22). Bu bobda argumentlarning **shakli** ko'rib chiqiladi: nechta argument haqli, flag va selector argument nega zararli, chiqish argumenti nima uchun qoldirilgan, va argument obyekti qachon kerak.

### 5.1 Argument soni: nol, bir, ikki, uch va undan keyin

Argument soni funksiyani tushunish narxini belgilaydi, chunki har bir argument o'quvchidan savol so'raydi: bu nima, qanday tartibda, `null` bo'lishi mumkinmi. Shu sababli tartib aniq: nol argument eng yaxshi, bitta yaxshi, ikkita qabul qilinadi, uchta asoslanishi kerak, to'rtta va undan ko'pi deyarli har doim xato.

| Argument soni | Nomi | Holati |
|---|---|---|
| 0 | niladik | eng yaxshi: obyekt holatidan ishlaydi |
| 1 | monadik | yaxshi: so'rov, o'zgartirish yoki hodisa |
| 2 | diadik | qabul qilinadi, tartib xavfi bor |
| 3 | triadik | asoslanishi kerak, tartib xavfi yuqori |
| 4+ | poliadik | argument obyekti kerak (5.6) |

Diadik funksiyada tabiiy tartib bo'lsa, u xavfsiz: `new Point(x, y)`, `assertEquals(expected, actual)`. Tabiiy tartib bo'lmasa, nomlangan parametr yo'qligi Java da muammo tug'diradi va yechim turni kuchaytirishda (`Money` va `Quantity` ni aralashtirib bo'lmaydi).

### 5.2 Monadik shakllar: so'rov, o'zgartirish, hodisa

Bitta argumentli funksiyalar uch shaklga bo'linadi va har birining o'z konvensiyasi bor. **So'rov**: argument haqida savol beradi va javob qaytaradi (`boolean fileExists(String path)`). **O'zgartirish**: argumentni boshqa narsaga aylantiradi va natijani **qaytaradi** (`InputStream fileOpen(String path)`). **Hodisa**: argumentni qabul qilib tizim holatini o'zgartiradi va hech narsa qaytarmaydi (`void passwordAttemptFailedNTimes(int attempts)`).

Eng ko'p uchraydigan xato — o'zgartirish shaklida argumentni o'zgartirib, uni qaytarmaslik. Bu chiqish argumentiga aylanadi (5.5) va o'quvchi natijani qayerdan olishini bilmaydi.

### 5.3 Flag argumenti va uni ikki funksiyaga bo'lish

`boolean` argument funksiyaning ikki xil ish qilishini ochiq e'lon qiladi, ya'ni "bitta ish" qoidasini buzadi (4.2). Undan ham yomoni: chaqiruv joyida `render(true)` o'qilganda `true` nimani anglatishi ko'rinmaydi va o'quvchi funksiya imzosini ochadi.

```java
// yomon: chaqiruv joyi o'qilmaydi
report.render(true);
payment.process(order, false, true);

// yaxshi: har bir xatti-harakat o'z nomida
report.renderForSuite();
report.renderForSingleTest();
payment.processWithoutRetry(order);
```

Agar flag argumenti tashqi API dan kelgan bo'lsa va olib tashlab bo'lmasa, uni enum ga aylantirish ikkinchi yaxshi yechim: `render(RenderMode.SUITE)` hech bo'lmasa chaqiruv joyida o'qiladi.

### 5.4 Tanlov (selector) argumenti va `enum` bilan almashtirish

Selector argumenti — flag argumentining umumlashgan shakli: funksiya ichida `switch` yoki `if` bilan xatti-harakatni tanlaydi. U funksiyani bir necha vazifaga birlashtirib, har bir chaqiruvchini keraksiz kontekst bilan yuklaydi.

```java
// yomon: selector argumenti funksiyani ikki vazifaga birlashtirgan
public BigDecimal calculateWeeklyPay(boolean overtime) {
    int tenthRate = getTenthRate();
    int tenthsWorked = getTenthsWorked();
    int straightTime = Math.min(400, tenthsWorked);
    int overTime = Math.max(0, tenthsWorked - straightTime);
    int straightPay = straightTime * tenthRate;
    double overtimeRate = overtime ? 1.5 : 1.0 * tenthRate;
    int overtimePay = (int) Math.round(overTime * overtimeRate);
    return BigDecimal.valueOf(straightPay + overtimePay);
}

// yaxshi: siyosat alohida turda, funksiya bitta ish qiladi
public Money weeklyPay(OvertimePolicy policy) {
    Money straight = straightTimePay();
    return straight.add(policy.overtimePay(overtimeTenths(), tenthRate()));
}
```

### 5.5 Chiqish argumenti va `void` dan qaytishga o'tish

Chiqish argumenti — funksiyaga uzatilgan obyektni funksiya o'zgartirib, natijani shu obyekt orqali qaytarishi. Bu shakl o'quvchidan imzoni tekshirishni talab qiladi, chunki argument odatda **kirish** deb o'qiladi.

```java
// yomon: s ni kim o'zgartiradi, nimaga aylanadi - imzodan ko'rinmaydi
public void appendFooter(StringBuffer report) { report.append("..."); }
appendFooter(report);

// yaxshi: obyektning o'z holati o'zgaradi yoki yangi qiymat qaytadi
report.appendFooter();
String withFooter = report.withFooter();
```

Xuddi shu qoida to'plamlarga ham tegishli: metodga `List` berib, uni to'ldirib qaytarish o'rniga yangi `List` qaytarish kerak (23.11).

### 5.6 Argument obyekti va parametr guruhlari

Uch yoki undan ko'p argument birga sayohat qilsa (data clump), ular aslida bir tushuncha. Ularni obyektga yig'ish argument sonini kamaytirmaydi — u tushunchaga nom beradi, va shu nom kod bazasida qayta ishlatiladi.

```java
// yomon: beshta argument, tartibi yodda saqlanadi
void createReservation(Long customerId, String sku, int quantity,
                       LocalDate from, LocalDate to) { ... }

// yaxshi: ikki tushuncha nomlangan
void createReservation(ReservationRequest request) { ... }

record ReservationRequest(CustomerId customer, Sku sku, Quantity quantity,
                          DateRange period) {
    ReservationRequest {
        if (quantity.isZeroOrLess()) throw new IllegalArgumentException("quantity");
        Objects.requireNonNull(period, "period");
    }
}
```

Qo'shimcha foyda: validatsiya bir joyga to'planadi (5.11) va `DateRange` o'z invariantini (`from <= to`) o'zi himoya qiladi.

### 5.7 Butun obyektni berish yoki maydonini berish

Ikki yo'nalishdagi qarorning oddiy mezoni bor. Agar funksiya obyektning uch yoki undan ko'p maydonini olsa, butun obyektni berish kerak (Preserve Whole Object, 37-bob). Agar funksiya obyektning faqat bitta maydonini olsa va obyekt haqida hech narsa bilishi shart bo'lmasa, maydonni berish bog'liqlikni kamaytiradi.

```java
// yomon: uchta maydon ajratib olingan, bog'liqlik yashirin
boolean within = range.includes(order.getCreatedAt(), order.getTimezone(), order.getRegion());

// yaxshi: butun obyekt
boolean within = range.includes(order);

// yaxshi (teskari holat): faqat bitta qiymat kerak, obyekt kerak emas
boolean expired = clock.isAfter(order.expiresAt());
```

### 5.8 Argument tartibi va bir xil turdagi qo'shni argumentlar

Eng xavfli imzo — yonma-yon turgan bir xil turdagi argumentlar, chunki ularni almashtirib yuborish kompilyatsiyadan o'tadi va faqat production da ko'rinadi.

```java
// yomon: ikki String va ikki int - almashtirsa kompilyator jim turadi
void transfer(String from, String to, int amount, int fee);
transfer(toAccount, fromAccount, fee, amount);   // xato, kompilyator sezmaydi

// yaxshi: tur o'zi xatoni to'sadi
void transfer(AccountNumber from, AccountNumber to, Money amount, Money fee);
// eng yaxshi: tushuncha obyektga yig'ilgan
void execute(TransferInstruction instruction);
```

Tartib bo'yicha konvensiya: muhimdan kam muhimga, obyekt birinchi, sozlama oxirida, `callback` eng oxirida (lambda ni chaqiruv joyida o'qiladigan qiladi).

### 5.9 Varargs, `null` argument va ixtiyoriy parametrlar

`varargs` o'qilishi uchun foydali, lekin uch tuzog'i bor: nol argument bilan chaqirish mumkin (kutilmagan bo'sh holat), avtomatik massiv yaratiladi (issiq yo'lda narx), va overload bilan birga ishlatilsa tanlov qoidalari chalkash bo'ladi. Qoida: `varargs` dan oldin kamida bitta majburiy parametr qo'yish.

`null` ni argument sifatida uzatish deyarli har doim xato (18.7). Ixtiyoriy parametr kerak bo'lsa, uch yechim bor va tartibi shunday: overload qilingan metod, builder, yoki `Optional` parametr (eng kam afzal, chunki chaqiruv joyi shovqinli bo'ladi).

```java
// yaxshi: overload bilan ixtiyoriylik
public Page<Order> search(OrderCriteria criteria) { return search(criteria, Pageable.unpaged()); }
public Page<Order> search(OrderCriteria criteria, Pageable pageable) { ... }

// yaxshi: varargs oldida majburiy parametr bor
public void audit(AuditEvent event, Tag... tags) { ... }
```

### 5.10 Overload qilish tuzoqlari va nomni aniqlashtirish

Overload qilish bir xil tushunchaning turli kirish shakllari uchun yaxshi (`of(int)`, `of(String)`). Lekin **xatti-harakat** farq qilsa, overload o'quvchini chalg'itadi: qaysi metod chaqirilayotganini tur xulosasi hal qiladi va bu kodda ko'rinmaydi.

```java
// yomon: ikkisi boshqa ish qiladi, tanlov tur orqali yashiringan
void remove(int index);        // indeks bo'yicha
void remove(Integer element);  // qiymat bo'yicha - klassik tuzoq

// yaxshi: nom farqni aytadi
void removeAt(int index);
void removeValue(Integer element);
```

Qo'shimcha qoida: overload qilingan metodlar bir xil sonli argument bilan turlicha ishlamasligi, va `null` uzatilganda qaysi biri tanlanishi aniq bo'lishi kerak.

### 5.11 Argumentni tekshirish joyi: chegara, konstruktor, domen

Validatsiyani har bir metodda takrorlash kodni shishiradi; umuman tekshirmaslik xatoni chuqurga suradi. To'g'ri yechim — tekshirishni joy bo'yicha taqsimlash.

| Daraja | Nima tekshiriladi | Vosita |
|---|---|---|
| Tashqi chegara (controller) | format, majburiylik, diapazon | Bean Validation `@Valid` |
| Value object konstruktori | invariant (`from <= to`) | `record` compact konstruktori |
| Domen metodi | biznes qoidasi, holat | domen istisnosi |
| Public kutubxona API | `null` va shartnoma | `Objects.requireNonNull` |
| Private metod | hech narsa (ishonadi) | assertion, ixtiyoriy |
| Repository | hech narsa | domen allaqachon tekshirgan |

Shu taqsimot "fail fast" ni ta'minlaydi (18.10) va ichki metodlarni toza qoldiradi: ular allaqachon to'g'ri ma'lumot oladi.

### 5.12 Amalda qo'llash

- [ ] `boolean` parametri bor barcha public metodlarni grep qilib, har birini ikki metodga yoki enum parametriga aylantiring.
- [ ] To'rt va undan ko'p parametrli metodlarni ro'yxatlab, birga sayohat qiladigan parametr guruhlarini record ga yig'ing.
- [ ] Yonma-yon bir xil turdagi parametrlar bor imzolarni topib, value object joriy qiling (`AccountNumber`, `Money`).
- [ ] Chiqish argumenti ishlatilgan joylarni (`void f(StringBuilder out)`) qaytish qiymatiga o'tkazing.
- [ ] `null` uzatilishi kutilgan parametrlarni overload yoki builder bilan almashtiring.
- [ ] Overload qilingan metodlar ro'yxatini chiqarib, xatti-harakati farq qiladiganlarini qayta nomlang.
- [ ] Validatsiya 5.11 jadvalidagi darajalarga mos taqsimlanganini tekshirib, takrorlangan tekshiruvlarni olib tashlang.
- [ ] Yangi public API uchun "3 dan ko'p parametr review da asoslanadi" qoidasini kiritib, PR shabloniga qo'shing.
## 6. Shart, mantiq va boshqaruv oqimi (Conditionals and Control Flow)

Erta qaytish va ichma-ich chuqurlik arxitektor hujjatida (4.4) berilgan. Bu bobda shartlarning qolgan qoidalari: inkor, mantiqiy soddalashtirish, `else` ni yo'qotish, `switch` ni to'g'ri ishlatish, chegaraviy shartlarni inkapsulyatsiya qilish va yashirin vaqt bog'liqligi.

### 6.1 Shartni nomlash va inkapsulyatsiya qilish

Shart ifodasi uch va undan ko'p operandga yetganda uni nomlash kerak. Nomlash ikki shaklda bo'ladi: mahalliy `boolean` o'zgaruvchi (eng arzon) yoki metod (qayta ishlatiladigan va testlanadigan). Agar shart domen qoidasini ifodalasa, u domen obyektiga ko'chishi kerak.

```java
// yomon: shart o'quvchidan to'rtta narsani ushlab turishni talab qiladi
if (payment.getStatus() == 1 && payment.getAmount().compareTo(BigDecimal.ZERO) > 0
        && payment.getSettledAt() != null
        && !payment.getCurrency().equals("UZS")) { ... }

// yaxshi: qoida domen obyektida nomlangan va testlanadi
if (payment.isForeignSettled()) { ... }

// Payment ichida:
public boolean isForeignSettled() {
    return status == SETTLED && amount.isPositive() && !currency.equals(Currency.UZS);
}
```

### 6.2 Inkor shartdan qochish va De Morgan qoidasi

Ijobiy shart inkordan tez o'qiladi, chunki ongda qo'shimcha amal talab qilmaydi. Shu sababli `if (!isNotEmpty(list))` kabi ifodalar yo'qotilishi kerak. De Morgan qoidasi bu ishni mexanik qiladi: `!(a && b)` → `!a || !b`, `!(a || b)` → `!a && !b`.

```java
// yomon: ikki inkor va bitta murakkab ifoda
if (!(order.isPaid() && order.isInStock())) {
    reject(order);
}

// yaxshi: ijobiy shart va erta qaytish
if (order.isPaid() && order.isInStock()) {
    accept(order);
    return;
}
reject(order);

// yoki: inkorni domen nomiga aylantirish
if (order.isNotReadyToShip()) { reject(order); }   // nom ijobiy o'qiladi
```

Istisno: guard clause da inkor tabiiy va to'g'ri (`if (order == null) throw ...`), chunki u erta chiqish uchun ishlatiladi.

### 6.3 Murakkab mantiqni soddalashtirish

Mantiqiy ifodalarni qisqartirish ko'pincha mexanik ish. Amaldagi uch harakat: bir xil shart ikki shoxda takrorlansa, uni tashqariga chiqarish; `if (a) return true; else return false;` ni `return a;` ga aylantirish; va bir xil natijaga olib boradigan shartlarni `||` bilan birlashtirish (Consolidate Conditional Expression, 37-bob).

```java
// yomon
if (customer.isBlocked()) {
    return true;
} else if (customer.hasOverdueInvoice()) {
    return true;
} else {
    return false;
}

// yaxshi
return customer.isBlocked() || customer.hasOverdueInvoice();

// yana yaxshiroq: nomlangan domen qoidasi
return customer.isCreditSuspended();
```

### 6.4 `else` ni yo'q qilish usullari

`else` bloki ko'pincha keraksiz va uni yo'qotish kodni tekislaydi. To'rt usul bor: guard clause bilan erta qaytish, standart qiymatni oldin belgilash, `switch` ifodasiga o'tish, va polimorfizm (patternlar hujjati 26.11).

```java
// yomon: ichma-ich if/else zinapoyasi
String label;
if (status == PENDING) {
    label = "Kutilmoqda";
} else if (status == SETTLED) {
    label = "Yopilgan";
} else {
    label = "Noma'lum";
}

// yaxshi: switch ifodasi, to'liqligi kompilyator tomonidan tekshiriladi
String label = switch (status) {
    case PENDING -> "Kutilmoqda";
    case SETTLED -> "Yopilgan";
    case REJECTED, PARTIALLY_REFUNDED -> "Muammoli";
};

// eng yaxshi: label enum ning o'zida yashaydi
String label = status.displayName();
```

### 6.5 Ternar operatori: qachon o'qiladi

Ternar operator bitta oddiy tanlovda `if/else` dan qisqa va o'qiladi. Uch holatda esa zarar qiladi: ichma-ich ishlatilganda, operandlari uzun bo'lganda, va yon ta'siri bo'lganda.

```java
// yaxshi: qisqa va bir tanlov
Money fee = order.isExpress() ? EXPRESS_FEE : STANDARD_FEE;

// yomon: ichma-ich ternar - o'qilmaydi
String tier = total > 1000 ? "GOLD" : total > 500 ? "SILVER" : total > 100 ? "BRONZE" : "NONE";

// yaxshi: tanlov domen metodiga ko'chdi
CustomerTier tier = CustomerTier.forAnnualSpend(total);
```

### 6.6 `switch` ni toza ishlatish: to'liqlik, `default`, fallthrough

Zamonaviy Java da `switch` **ifodasi** (`->` shakli) eski `switch` gapidan ustun, chunki fallthrough xatosi yo'q, har bir shox qiymat qaytaradi va `sealed` tur ustida to'liqligi kompilyator tomonidan tekshiriladi (arxitektor hujjati 13.2-13.3).

Qolgan qoidalar: enum ustida `switch` da `default` yozmaslik (shunda yangi enum a'zosi qo'shilganda kompilyator xato beradi), eski `switch` gapida har bir `case` ni `break` bilan tugatish yoki `->` shakliga o'tish, va `switch` ni past darajali kodda ushlab turish (patternlar hujjatidagi polimorfizm bilan almashtirish qoidasi).

```java
// yomon: default bor - yangi enum a'zosi jimgina "Noma'lum" ga tushadi
switch (status) {
    case PENDING: return "Kutilmoqda";
    default: return "Noma'lum";
}

// yaxshi: default yo'q, yangi a'zo kompilyatsiyani buzadi va eslatadi
return switch (status) {
    case PENDING -> "Kutilmoqda";
    case SETTLED -> "Yopilgan";
    case REJECTED -> "Rad etilgan";
    case PARTIALLY_REFUNDED -> "Qisman qaytarilgan";
};
```

### 6.7 Chegaraviy shartlarni inkapsulyatsiya qilish

`i + 1`, `level - 1`, `<=` va `<` farqlari kod bo'ylab tarqalsa, off-by-one xatolari paydo bo'ladi va ularni topish qiyin. Yechim: chegara hisobini bir joyda nomlab qo'yish.

```java
// yomon: level + 1 uch joyda takrorlangan
if (level + 1 < tags.length) {
    parts = new Parse(body, tags, level + 1, offset + endTag);
}

// yaxshi: chegara nomlangan
int nextLevel = level + 1;
if (nextLevel < tags.length) {
    parts = new Parse(body, tags, nextLevel, offset + endTag);
}

// yaxshi: oraliq o'z turiga olingan, inklyuzivlik turda hujjatlangan
record DateRange(LocalDate fromInclusive, LocalDate toExclusive) {
    boolean includes(LocalDate day) {
        return !day.isBefore(fromInclusive) && day.isBefore(toExclusive);
    }
}
```

### 6.8 `null` tekshiruvi zinapoyasi va undan chiqish

Ichma-ich `null` tekshiruvlari eng ko'p uchraydigan chuqurlik manbai. To'rtta chiqish yo'li bor va tartibi shunday: `null` ni manbada yo'qotish (18.7), `Optional` zanjiri (24.6), maxsus holat obyekti (18.6), va faqat chegarada `Objects.requireNonNull`.

```java
// yomon: zanjir bo'ylab null tekshiruvi
if (order != null) {
    Customer c = order.getCustomer();
    if (c != null) {
        Address a = c.getAddress();
        if (a != null && a.getCity() != null) {
            return a.getCity().toUpperCase();
        }
    }
}
return "NOMA'LUM";

// yaxshi: null manbada yo'q, Optional faqat haqiqiy yo'qlik uchun
return order.customer().address()
        .map(Address::city)
        .map(String::toUpperCase)
        .orElse(UNKNOWN_CITY);
```

### 6.9 Yashirin vaqt bog'liqligini ko'rinadigan qilish

Agar metodlarni faqat ma'lum tartibda chaqirish mumkin bo'lsa va bu tartib kodda ko'rinmasa, bu yashirin vaqt bog'liqligi (hidden temporal coupling; patternlar hujjatida Sequential Coupling anti-patterni, 25.17). Clean code darajasidagi yechimi: tartibni imzoga olib chiqish.

```java
// yomon: tartib faqat izohda va xotirada
public void run() {
    openConnection();
    authenticate();     // openConnection dan keyin bo'lishi shart
    sendPayload();      // authenticate dan keyin bo'lishi shart
}

// yaxshi: har bir qadam keyingisi uchun kerakli natijani qaytaradi
public void run() {
    Connection connection = openConnection();
    Session session = authenticate(connection);
    sendPayload(session);
}
```

Shu uslub "o'tkazish" (passing a baton) deb ataladi: tartibni buzish kompilyatsiyadan o'tmaydi.

### 6.10 Takrorlangan `switch` va turga qarab shoxlanish

Bir xil `switch` yoki `if/else` zanjiri uch-to'rt joyda takrorlansa, bu hid (32-bob, Repeated Switches). Har bir yangi enum a'zosi barcha takrorlarni topishni talab qiladi va bittasi doim esdan chiqadi.

Yechim darajalari: xatti-harakatni enum ichiga ko'chirish (eng arzon), `sealed` interfeys va pattern matching, yoki polimorfizm. Enum ichiga ko'chirish Java da ko'pincha yetarli.

```java
// yaxshi: har bir shox enum a'zosining o'zida
public enum ShippingMethod {
    STANDARD { public Money fee(Weight w) { return Money.of(10_000); } },
    EXPRESS   { public Money fee(Weight w) { return Money.of(25_000); } },
    FREIGHT   { public Money fee(Weight w) { return Money.of(w.kg() * 3_000); } };

    public abstract Money fee(Weight weight);
}
```

### 6.11 Amalda qo'llash

- [ ] Uch va undan ko'p operandli shart ifodalarini topib, har birini nomlangan `boolean` yoki domen metodiga chiqaring.
- [ ] `!(...)` shaklidagi inkor ifodalarni De Morgan bilan soddalashtirib, ijobiy shartga aylantiring.
- [ ] `if (x) return true; else return false;` namunalarini grep qilib, `return x;` ga qisqartiring.
- [ ] Enum ustidagi barcha `switch` lardan `default` ni olib tashlab, to'liqlikni kompilyatorga topshiring.
- [ ] Eski `switch` gaplarini `->` ifodasiga o'tkazib, fallthrough xavfini yo'qoting.
- [ ] Ichma-ich ternar operatorlarni topib, domen metodi yoki `switch` ifodasiga aylantiring.
- [ ] `null` tekshiruvi zanjirlari bor joylarni `Optional` yoki manbadagi `null` ni yo'qotish bilan tekislang.
- [ ] Ma'lum tartibda chaqirilishi shart bo'lgan metod guruhlarini topib, tartibni qaytish turlari orqali majburiy qiling.
## 7. Sikl, iteratsiya va to'plam bilan ishlash (Loops and Iteration)

Sikl o'qish narxi jihatidan shartdan qimmat, chunki o'quvchi nafaqat tanani, balki holatning vaqt bo'yicha o'zgarishini ham ushlab turishi kerak. Bu bobda siklni o'qiladigan ushlashning aniq qoidalari: tana uzunligi, o'zgaruvchi nomi, chiqish nuqtalari, siklni bo'lish va quvurga o'tish mezoni.

### 7.1 Sikl tanasini chiqarish va sikl o'zgaruvchisi nomi

Sikl tanasi uch qatordan oshsa, uni metodga chiqarish kerak. Shundan keyin sikl bir qarashda o'qiladi: "har bir element uchun shuni qil". Sikl o'zgaruvchisi nomi esa elementning rolini aytishi kerak, `item` yoki `e` emas.

```java
// yomon: tana uzun, nom ma'nosiz
for (Object[] e : rows) {
    if (e[3] != null) {
        BigDecimal amt = (BigDecimal) e[2];
        if (amt.compareTo(BigDecimal.ZERO) > 0) {
            total = total.add(amt);
            count++;
        }
    }
}

// yaxshi: tana bitta chaqiruv, nom rolni aytadi
for (SettlementRow settlement : settlements) {
    accumulate(settlement);
}
```

### 7.2 Indeksli sikl, `for-each` va iterator tanlovi

Tanlov qoidasi oddiy: indeks kerak bo'lmasa, `for-each`. Indeksli `for` faqat indeksning o'zi ma'noga ega bo'lganda yoki massiv bilan ishlaganda haqli. `Iterator` ni oshkor ishlatish faqat iteratsiya vaqtida o'chirish kerak bo'lganda qoladi (7.6).

| Holat | To'g'ri tanlov |
|---|---|
| Elementlar ustida o'tish | `for (X x : xs)` |
| Indeks ma'noga ega (qator raqami) | `for (int i = 0; ...)` |
| Ikki to'plamni parallel o'tish | indeksli `for` yoki `zip` yordamchisi |
| Iteratsiya vaqtida o'chirish | `Iterator.remove()` yoki `removeIf` |
| Transformatsiya va filtr | `stream()` (7.7) |
| Cheksiz yoki shartli | `while` |
| Kamida bir marta bajarish | `do/while` (kamdan-kam) |

### 7.3 Bitta siklda bir necha ish: siklni bo'lish

Bir sikl ichida ikki mustaqil hisob qilinsa, u ikki siklga bo'linishi kerak (Split Loop, 35-bob). "Tezlik uchun bitta siklda qilaman" argumenti deyarli har doim o'lchanmagan: ikki marta o'tish narxi minglab element uchun sezilmaydi, o'qish foydasi esa darhol keladi.

```java
// yomon: bir siklda ikki mustaqil hisob
Money total = Money.ZERO;
LocalDate earliest = null;
for (Order order : orders) {
    total = total.add(order.total());
    if (earliest == null || order.createdAt().isBefore(earliest)) {
        earliest = order.createdAt();
    }
}

// yaxshi: har bir hisob o'z nomi bilan, mustaqil testlanadi
Money total = totalOf(orders);
LocalDate earliest = earliestCreatedAt(orders);
```

Bo'lgandan keyin har bir sikl ko'pincha quvurga aylanadi va yo'qoladi (7.7).

### 7.4 `break`, `continue`, label va ulardan chiqish

`continue` guard clause ning sikl ichidagi shakli va u foydali: yaroqsiz elementni o'tkazib yuboradi, keyingi tana esa chuqurlikka tushmaydi. `break` esa qidiruvni to'xtatish uchun to'g'ri. Label bilan `break` (`break outer;`) deyarli har doim ichki siklni metodga chiqarish zarurligini bildiradi.

```java
// yomon: labelli break - ichma-ich sikl metodga chiqishi kerak
outer:
for (Warehouse warehouse : warehouses) {
    for (Stock stock : warehouse.stocks()) {
        if (stock.sku().equals(sku)) { found = stock; break outer; }
    }
}

// yaxshi: ichki qidiruv alohida metodda, chiqish return bilan
Optional<Stock> found = findStock(warehouses, sku);

private Optional<Stock> findStock(List<Warehouse> warehouses, Sku sku) {
    for (Warehouse warehouse : warehouses) {
        for (Stock stock : warehouse.stocks()) {
            if (stock.sku().equals(sku)) return Optional.of(stock);
        }
    }
    return Optional.empty();
}
```

### 7.5 Birdan ko'p shartli siklni qayta yozish

`while (a && b && !c)` shaklidagi sikl sharti o'quvchidan uch holatni bir vaqtda ushlashni talab qiladi. Yechim: shartni nomlash (6.1) yoki siklni ikki bosqichga bo'lish.

```java
// yomon
while (retries < MAX && !succeeded && clock.instant().isBefore(deadline)) { ... }

// yaxshi: shart nomlangan
while (shouldRetry(retries, succeeded, deadline)) { ... }

// yaxshi (ko'p holatda): qayta urinish siyosati alohida obyektda
retryPolicy.execute(() -> gateway.settle(payment));
```

### 7.6 Iteratsiya vaqtida to'plamni o'zgartirish

`for-each` ichida to'plamdan element o'chirish `ConcurrentModificationException` beradi va bu xato ko'pincha faqat ma'lum ma'lumotda chiqadi. Uchta to'g'ri yo'l bor: `removeIf`, `Iterator.remove()`, yoki yangi to'plam yig'ish.

```java
// yomon: ConcurrentModificationException
for (Order order : orders) {
    if (order.isExpired()) orders.remove(order);
}

// yaxshi: maqsad aniq, bir qator
orders.removeIf(Order::isExpired);

// yaxshi: manbani o'zgartirmaslik kerak bo'lsa
List<Order> active = orders.stream().filter(not(Order::isExpired)).toList();
```

Xuddi shu qoida `Map` ga tegishli: iteratsiya vaqtida `put` qilish taqiqlangan; `entrySet().removeIf` yoki `compute*` metodlari ishlatiladi (23.2).

### 7.7 Sikldan quvurga o'tish mezoni

Oqim va sikl tanlovi arxitektor hujjatida (13.6) ko'rib chiqilgan. Bu yerda amaliy mezon: quvur (`stream`) **transformatsiya va filtr** zanjirida o'qiladi; sikl esa **holat yig'ish, erta chiqish va yon ta'sir** da o'qiladi.

| Vazifa | O'qiladigan shakl |
|---|---|
| Filtr + mapping + yig'ish | `stream()` |
| Erta chiqish bilan qidiruv | `stream().filter().findFirst()` yoki sikl |
| Indeksga bog'liq hisob | sikl |
| Tashqi holatni o'zgartirish | sikl (oqimda yon ta'sir - 24.4) |
| Istisno tashlashi mumkin bo'lgan amal | sikl (24.7) |
| Ikki to'plamni birga o'tish | sikl |
| Guruhlash va agregatsiya | `Collectors.groupingBy` |
| Cheksiz ketma-ketlik | `Stream.iterate` |

### 7.8 Off-by-one va chegarani hujjatlashtirish

Off-by-one xatolarining asosiy sababi — chegaraning inklyuzivligi hech qayerda yozilmagani. Yechim ikki qatlamli: nomda yozish (`fromInclusive`, `toExclusive`) va turga olish (6.7 dagi `DateRange`).

```java
// yomon: oxirgi element kiradimi - kodni o'qib chiqarish kerak
List<Order> page(int offset, int limit);

// yaxshi: nom va tur chegarani aytadi
List<Order> page(Pageable pageable);                 // Spring konvensiyasi
List<Order> inRange(LocalDate fromInclusive, LocalDate toExclusive);
```

Test tomonida qoida: har bir chegara uchun uchta holat yozish — chegaradan oldin, chegarada, chegaradan keyin.

### 7.9 Katta siklda resurs va xotira xatti-harakati

Toza kod katta hajmda ham toza qolishi kerak. Uch qoida bor va ularning hammasi o'qilishini buzmaydi. Birinchi, siklda butun natijani xotiraga yig'maslik: `Stream` yoki kursor bilan oqim sifatida ishlash. Ikkinchi, siklda resurs ochmaslik (ulanish, fayl) — resurs sikldan tashqarida ochiladi. Uchinchi, siklda bitta-bitta so'rov yuborish o'rniga paket (batch) ishlatish; bu N+1 ning umumiy shakli (patternlar hujjati 25.43).

```java
// yomon: siklda bitta-bitta so'rov va ulanish
for (OrderId id : ids) {
    try (Connection c = dataSource.getConnection()) {      // har iteratsiyada yangi ulanish
        orderRepository.markShipped(c, id);
    }
}

// yaxshi: bitta tranzaksiya, paketli yangilash
orderRepository.markShipped(ids);     // ichida: update ... where id = any(?)
```

### 7.10 Amalda qo'llash

- [ ] Tanasi uch qatordan uzun bo'lgan sikllarni topib, tanani nomlangan metodga chiqaring.
- [ ] Sikl o'zgaruvchilari nomlarini (`e`, `o`, `item`) elementning roliga qarab qayta nomlang.
- [ ] Bir siklda bir necha mustaqil hisob qilinadigan joylarni ikki siklga yoki quvurga bo'ling.
- [ ] `break <label>` ishlatilgan joylarni ichki siklni metodga chiqarib yo'qoting.
- [ ] `for-each` ichida `remove`/`put` chaqirilgan joylarni `removeIf` yoki `Iterator` ga o'tkazing.
- [ ] Chegara parametrlari nomiga inklyuzivlikni yozing yoki oraliqni `record` ga oling.
- [ ] Siklda ulanish ochadigan yoki so'rov yuboradigan joylarni paketli amalga aylantiring.
- [ ] Har bir chegaraviy shart uchun uch holatli test (oldin, chegarada, keyin) yozilganini tekshiring.
# III. Izoh va hujjat

## 8. Izoh qoidalari: yaxshi izohlar (Comments: The Good Ones)

Izohning "nima" emas "nega" yozish qoidasi arxitektor hujjatida (4.5) berilgan. Bu bobda qolgan qism: izoh qanday holatlarda haqli ekanining to'liq ro'yxati. Keyingi bob esa yomon izohlarning katalogi. Ikkisi birga review paytida izohni qoldirish yoki o'chirish qarorini bir necha soniyada beradi.

### 8.1 Izoh - muvaffaqiyatsizlikni tan olish

Izohning har bir qo'llanishi kichik mag'lubiyat: niyatni kod bilan ifodalay olmaganimiz uchun tabiiy tilga murojaat qilyapmiz. Shu qarash izohga to'g'ri munosabat beradi — izohni yozishdan oldin ikki marta kodni o'zgartirishga urinish kerak.

Shundan kelib chiqadigan ikkinchi haqiqat: izoh eskiradi, kod esa eskirmaydi. Kompilyator izohni tekshirmaydi, test izohni tasdiqlamaydi. Shu sababli kod bazasidagi eng yosh izoh ham yolg'on bo'lishi mumkin, va o'quvchi izohga ishonib xato qiladi. Izohni saqlash uchun **egalik** kerak: kim o'zgartirsa, izohni ham o'zgartiradi.

### 8.2 O'zini kodda tushuntirish: izohni funksiyaga aylantirish

Ko'p izohlarni mexanik ravishda kodga aylantirish mumkin. Eng tez usul: izohni funksiya nomiga yoki o'zgaruvchi nomiga ko'chirish.

```java
// yomon: izoh shartni tushuntiradi
// xodim nafaqa olishga haqli ekanini tekshir
if (employee.flags & HOURLY_FLAG) != 0 && employee.age > 65) { ... }

// yaxshi: izoh metod nomiga aylandi
if (employee.isEligibleForFullBenefits()) { ... }
```

Shu almashtirishning uchta shakli bor: izoh → metod nomi, izoh → mahalliy o'zgaruvchi nomi, izoh → nomlangan konstanta. Uchtasi ham izohni yo'qotib, ma'noni kodda qoldiradi.

### 8.3 Huquqiy va litsenziya izohlari

Fayl boshidagi litsenziya, mualliflik va patent izohlari haqli va majburiy bo'lishi mumkin. Ularning qoidasi: qisqa bo'lishi va tashqi hujjatga havola qilishi, butun litsenziya matnini har faylga ko'chirmaslik.

```java
/*
 * Copyright (c) 2026 Shop LLC. Barcha huquqlar himoyalangan.
 * Litsenziya shartlari: LICENSE faylida.
 */
```

Agar litsenziya sarlavhasi majburiy bo'lsa, uni qo'lda yozish emas, Spotless `licenseHeader` qoidasi bilan avtomatlashtirish kerak (13.3).

### 8.4 Ma'lumot beruvchi va maqsadni tushuntiruvchi izoh

Ikki haqli toifa. **Ma'lumot beruvchi** izoh kodda ko'rinmaydigan faktni beradi: formatning ma'nosi, tashqi tizim xatti-harakati, kutilayotgan natija shakli. **Maqsadni tushuntiruvchi** izoh esa qarorning asosini aytadi: nega shu yondashuv tanlangan.

```java
// Format: kk:dd:ss AAA, MM-kk-yyyy  (bank fayli spetsifikatsiyasi, 3.4-bo'lim)
private static final Pattern TIME_MATCHER =
        Pattern.compile("\\d*:\\d*:\\d* \\w*, \\w*-\\d*-\\d*");

// Bu yerda tartiblash kerak: bank fayli yozuvlari tartibsiz keladi,
// lekin settlement ketma-ketligi hisobga ta'sir qiladi (shartnoma 5.1).
rows.sort(comparing(SettlementRow::sequenceNumber));
```

Ikkinchi shakl eng qimmatli izoh turi, chunki uni kodga ko'chirish mumkin emas: kod nima qilayotganini aytadi, nega shu variant tanlanganini aytmaydi.

### 8.5 Aniqlashtiruvchi izoh va uning xavfi

Ba'zan tushunarsiz, lekin o'zgartirib bo'lmaydigan kod bo'ladi: standart kutubxona chaqiruvi, tashqi API javobi, murakkab matematik ifoda. Bunda aniqlashtiruvchi izoh haqli.

```java
assertTrue(a.compareTo(a) == 0);    // a == a
assertTrue(a.compareTo(b) != 0);    // a != b
assertTrue(a.compareTo(ab) == -1);  // a < ab
```

Xavfi shunda: izoh noto'g'ri bo'lsa, u xatoni ikki marta kuchaytiradi. Shuning uchun aniqlashtiruvchi izoh yozishdan oldin savol berish kerak: shu kodni o'zgartirib tushunarli qilib bo'lmaydimi. Javob "yo'q" bo'lsa, izoh qoladi.

### 8.6 Oqibat haqida ogohlantirish

Boshqa ishlab chiquvchini xatodan to'sadigan izoh haqli, chunki u aniq va qimmat ma'lumot beradi.

```java
// Bu testni mahalliy ishga tushirmang: 5 daqiqa ketadi va real bank
// sandbox'ida 200 ta tranzaksiya yaratadi. Faqat nightly pipeline'da.
@Tag("slow")
@Test
void settlesTwoHundredPayments() { ... }

// SimpleDateFormat thread-safe emas: har bir chaqiruvda yangi nusxa kerak.
// (Bu kod legacy integratsiyada qolgan, yangi kodda DateTimeFormatter ishlatiladi.)
public static SimpleDateFormat legacyFormatter() {
    return new SimpleDateFormat("dd-MM-yyyy");
}
```

### 8.7 TODO, FIXME va ularning hayot muddati

`TODO` izohi haqli, lekin faqat uchta shart bilan: nima qilinishi kerakligi aniq yozilgan, kim mas'ul ekani ko'rinadi (yoki ticket havolasi bor), va qachongacha amal qilishi aytilgan. Shartsiz `TODO` arxeologiyaga aylanadi va yillar davomida yashaydi.

```java
// yomon
// TODO: buni tuzatish kerak

// yaxshi: ticket, sabab va olib tashlash sharti
// TODO(SHOP-4821): vaqtinchalik yechim. Bank yangi API (v3) ni 2026-Q3 da chiqaradi,
// shundan keyin bu mapping va retry kodi butunlay o'chiriladi.
```

Amaliy intizom: `TODO` lar sonini CI da o'lchash va o'sishini bloklash; `FIXME` ni esa umuman taqiqlash (u "buzilgan kod merge qilindi" degani). Har chorakda `TODO` ro'yxatini ko'rib chiqish va eskirganini o'chirish.

### 8.8 Kuchaytiruvchi izoh

Ba'zan kodning bir qismi ahamiyatsiz ko'rinadi, lekin aslida kritik. Kuchaytiruvchi izoh shu ahamiyatni ta'kidlaydi va keyingi odamni "optimizatsiya" qilib buzishdan to'sadi.

```java
// trim() shart: boshida bo'sh joy bo'lsa, bank fayli kaliti noto'g'ri
// hisoblanadi va yozuv dublikat sifatida rad etiladi. Olib tashlamang.
String key = line.substring(0, 16).trim();
```

### 8.9 Formula, standart va huquqiy asos havolasi

Hisoblash qoidasi tashqi manbadan kelganda, manbani ko'rsatish izohning eng foydali shakli: u kodni tekshirish imkonini beradi va qoida o'zgarganda qayerga qarashni aytadi.

```java
// QQS stavkasi: Soliq kodeksi 258-moddasi, 2026-01-01 dan 12%.
// O'zgarish bo'lsa qonun hujjatlari portalidan tekshiriladi va bu yerda yangilanadi.
private static final BigDecimal VAT_RATE = new BigDecimal("0.12");

// IBAN tekshiruv algoritmi: ISO 13616 va ISO 7064 MOD-97-10.
public boolean isValid(String iban) { ... }
```

### 8.10 Amalda qo'llash

- [ ] Kod bazasidagi barcha izohlarni sanab, har birini 8-9 boblardagi toifalarga ajratib belgilang.
- [ ] Shartni yoki hisobni tushuntiradigan izohlarni metod yoki o'zgaruvchi nomiga aylantirib o'chiring.
- [ ] Har bir `TODO` ga ticket havolasi, sabab va olib tashlash shartini qo'shing; shartsizlarini o'chiring.
- [ ] `FIXME` larni ro'yxatlab, har birini yo tuzating, yo ticketga aylantirib izohni olib tashlang.
- [ ] CI da `TODO` sonini o'lchab, o'sishini ogohlantirishga aylantiring.
- [ ] Soliq, tarif va huquqiy hisoblar yonida rasmiy asos havolasi borligini tekshirib, yo'qlarini qo'shing.
- [ ] Litsenziya sarlavhalarini Spotless `licenseHeader` bilan avtomatlashtiring.
- [ ] Tashqi tizim cheklovlari (limit, format, thread-safety) kodda izohlanganini tekshirib, yetishmaganini qo'shing.
## 9. Yomon izohlar katalogi (Comments: The Bad Ones)

Izohlarning katta qismi shu bobdagi toifalarga tushadi va ularning hammasi o'chirilishi kerak. Katalog shaklida berilgani ataylab: review paytida izohni toifaga solib, qaror bir necha soniyada chiqadi.

### 9.1 G'o'ldirash (mumbling)

Izoh shoshilib yozilsa, u muallifga tushunarli, o'quvchiga esa yo'q bo'ladi. Natija: o'quvchi izohni tushunish uchun boshqa kodni o'qishga majbur, ya'ni izoh ish qilmaydi, ish qo'shadi.

```java
// yomon: "defaults" nima, qaysi fayl, nega e'tiborsiz qoldirildi?
try {
    loadProperties();
} catch (IOException e) {
    // defaults yuklandi
}

// yaxshi: izoh emas, kodning o'zi aytadi
try {
    this.properties = loadPropertiesFile(CONFIG_PATH);
} catch (NoSuchFileException e) {
    this.properties = Properties.defaults();   // fayl yo'q bo'lishi normal holat
}
```

### 9.2 Ortiqcha izoh: kodni so'zma-so'z takrorlash

Kodni takrorlagan izoh o'qish vaqtini oshiradi va ma'lumot bermaydi. Bundan tashqari, u kod o'zgarganda yangilanmaydi va 9.3 ga aylanadi.

```java
// yomon
// buyurtmani saqlaydi
orderRepository.save(order);

// i ni bittaga oshiradi
i++;

// yaxshi: izoh yo'q
orderRepository.save(order);
```

### 9.3 Chalg'ituvchi izoh

Eng qimmat izoh turi: u yolg'on gapiradi va o'quvchi ishonadi. Odatda u bir vaqtlar to'g'ri bo'lgan, keyin kod o'zgargan va izoh qolgan.

```java
// yomon: izoh "kutadi" deydi, kod esa darhol qaytadi
// Thread shu yerda flag true bo'lguncha kutadi.
public void waitForClose() {
    if (!closed) {
        return;        // kutmaydi!
    }
}
```

Chalg'ituvchi izohni topish usuli: review paytida har bir izohni kod bilan taqqoslash. Avtomatik usuli yo'q, shuning uchun izohlar soni kam bo'lishi afzal.

### 9.4 Majburiy izoh: har bir maydonga Javadoc

"Har bir metod Javadoc olishi kerak" qoidasi foydadan ko'ra zarar keltiradi: u shovqin generatsiya qiladi, mazmunsiz `@param` qatorlari paydo bo'ladi va haqiqiy hujjat ularning ichida ko'rinmay qoladi.

```java
// yomon: mazmunsiz, majburiyat uchun yozilgan
/**
 * @param order buyurtma
 * @param now hozirgi vaqt
 * @return natija
 */
public Result process(Order order, Instant now) { ... }
```

To'g'ri siyosat: Javadoc faqat public API va noaniq shartnomalar uchun (10-bob), ichki metodlar uchun esa nom va imzo yetarli.

### 9.5 Jurnal izohlari va mualliflik imzolari

Fayl boshida o'zgarish tarixi yuritish `git` dan oldingi davr qoldig'i. Hozir u faqat shovqin, chunki tarix allaqachon versiya nazoratida bor va u aniqroq.

```java
// yomon: git log buni yaxshiroq aytadi
/**
 * 2019-04-11: Dilshod - birinchi versiya
 * 2020-01-02: Aziza - QQS hisobini tuzatdi
 * 2021-07-19: noma'lum - refaktoring
 */

// yomon: egalik git blame va CODEOWNERS da
/** @author Dilshod */
```

`@author` tegining yashirin zarari bor: u kodni "shaxsiy mulk" ga aylantiradi va jamoaviy egalikni susaytiradi (47.1).

### 9.6 Shovqin izohlar

Hech qanday ma'lumot bermaydigan, shunchaki bo'sh joyni to'ldiradigan izohlar.

```java
// yomon: hammasi shovqin
/** Default konstruktor. */
protected AnnualDateRule() { }

/** Oy kuni. */
private int dayOfMonth;

// Ro'yxatni qaytaradi
public List<Order> getOrders() { return orders; }
```

Bunday izohlar shu darajada ko'p bo'lsa, o'quvchi izohlarni butunlay o'qishni to'xtatadi va natijada 8.4 dagi foydali izohlar ham e'tibordan chetda qoladi.

### 9.7 Pozitsiya belgilari va qavs yopilishi izohlari

Bo'lim ajratuvchi banner va yopiladigan qavs yonidagi izoh ikkisi ham tuzilishni izoh bilan almashtirishga urinish. Ikkisi ham bir xil haqiqiy muammoni ko'rsatadi: blok juda uzun (4.3).

```java
// yomon: banner bo'lim izohi
//////////////////////////////////////////
// Validatsiya
//////////////////////////////////////////

// yomon: qavs yopilishi izohi - sikl juda uzun
        }   // while
    }       // try
}           // main
```

Yechim: bannerni metod nomiga, uzun blokni esa kichik metodlarga aylantirish.

### 9.8 Izohga olingan kod

Izohga olingan kod kod bazasidagi eng zararli artefakt: u hech kim o'chirishga jur'at qilmaydigan o'lik matn, chunki "balki kerak bo'ladi". Versiya nazorati bor kod bazasida bu argument o'z kuchini yo'qotgan.

```java
// yomon
// this.bytePos = writeBytes(pngIdBytes, 0);
// hdrPos = bytePos;
writeHeader();
// hdrBytes = ...
writeResolution();
```

Qoida: izohga olingan kod darhol o'chiriladi. Kerak bo'lsa `git log -S` yoki `git revert` bilan topiladi. Agar vaqtinchalik o'chirish kerak bo'lsa, feature flag ishlatiladi (41.5), izoh emas.

### 9.9 Nolokal ma'lumot va ortiqcha ma'lumot

**Nolokal** izoh — shu kodga tegishli bo'lmagan ma'lumotni aytadi (masalan metod izohida butun tizim konfiguratsiyasini tushuntiradi). Muammo: kod o'zgarmasa ham izoh eskiradi, chunki u boshqa joyga tegishli.

**Ortiqcha ma'lumot** — izohda tarixiy muhokama, RFC ning to'liq matni, akademik tushuntirish. Izoh yozish uchun emas, o'qish uchun mo'ljallangan: uzun matn o'qilmaydi.

```java
// yomon: nolokal - bu metodga tegishli emas
/**
 * Port: standart 8080. Konfiguratsiyani application.yml da o'zgartirish mumkin.
 * Shuningdek ingress va service portini ham moslash kerak...
 */
public void handle(Request request) { ... }

// yaxshi: havola bering, ko'chirmang
// Protokol tafsilotlari: docs/settlement-protocol.md
```

### 9.10 Noravshan bog'liqlik

Izoh kodni tushuntirishi kerak, lekin ba'zan izohning o'zi tushuntirishga muhtoj bo'lib qoladi: u qaysi qatorga, qaysi qiymatga tegishli ekani ko'rinmaydi.

```java
// yomon: "filter bytes" nima, nega +1?
// filter baytlari pikselga qo'shiladi
this.pngBytes = new byte[((width + 1) * height * 3) + 200];

// yaxshi: har bir had nomlangan
int filterByteCountPerRow = 1;
int bytesPerPixel = 3;
int headerAndTrailerBytes = 200;
this.pngBytes = new byte[(width + filterByteCountPerRow) * height * bytesPerPixel
        + headerAndTrailerBytes];
```

### 9.11 Funksiya sarlavhasi izohi

Qisqa, bitta ish qiladigan va yaxshi nomlangan funksiyaga sarlavha izohi kerak emas. Agar sarlavha izohi yozishga ehtiyoj tug'ilsa, u funksiya nomini aniqlashtirish zarurligini bildiradi (4.6).

```java
// yomon
// Qoldiqni tekshiradi va yetarli bo'lsa rezerv qiladi
public void doIt(Order o) { ... }

// yaxshi: izoh nomga ko'chdi
public void reserveStockIfAvailable(Order order) { ... }
```

### 9.12 Izohni o'chirish qarori: tekshiruv ro'yxati

Review paytida izoh uchun ketma-ket beriladigan savollar. Birinchi "yo'q" javobi izohni o'chirish qaroriga olib keladi.

| Savol | "Yo'q" bo'lsa |
|---|---|
| Izoh kodda ko'rinmaydigan ma'lumot beradimi? | o'chirish |
| Uni nomga yoki turga ko'chirib bo'lmaydimi? | ko'chirish, izohni o'chirish |
| Izoh bugun ham to'g'rimi? | tuzatish yoki o'chirish |
| Izohni o'quvchi tushunadimi? | qayta yozish yoki o'chirish |
| Kod o'zgarganda izoh yangilanadimi? | o'chirish (saqlanmaydi) |
| Izoh kodga tegishlimi (nolokal emasmi)? | hujjatga ko'chirish |
| Izohda ticket va shart bormi (`TODO` uchun)? | qo'shish yoki o'chirish |
| Izohga olingan kod emasmi? | darhol o'chirish |

### 9.13 Amalda qo'llash

- [ ] Izohga olingan kodni butun repoda grep qilib (`^\s*//\s*\w+.*[;{}]`), hammasini o'chiring.
- [ ] `@author` va fayl boshidagi o'zgarish jurnallarini olib tashlab, egalikni CODEOWNERS ga ko'chiring.
- [ ] Banner va qavs yopilishi izohlarini topib, ular belgilagan bo'limlarni metodlarga ajratib bering.
- [ ] Mazmunsiz Javadoc bloklarini (`@param order buyurtma`) o'chirib, Javadoc siyosatini public API bilan cheklang.
- [ ] Har bir izohni kod bilan taqqoslab, chalg'ituvchilarini tuzating yoki o'chiring.
- [ ] 9.12 jadvalidagi savollar ro'yxatini review checklistiga kiritib, izoh bo'yicha qarorni standartlashtiring.
- [ ] Uzun tushuntirish izohlarini `docs/` dagi faylga ko'chirib, kodda faqat havola qoldiring.
- [ ] Checkstyle yoki custom qoida bilan `FIXME` ni CI da bloklang.
## 10. Javadoc va API hujjati (Javadoc and API Documentation)

Public API ni o'zini hujjatlaydigan qilish arxitektor hujjatida (4.10 va 13.8) ko'rib chiqilgan. Bu bobda Javadoc ning mexanikasi: nimani yozish, qanday shaklda, qanday tekshirish. Javadoc yagona izoh turi bo'lib, uni mashina tekshiradi va shu sababli uni toza ushlash mumkin.

### 10.1 Javadoc kimga yoziladi va qayerga yozilmaydi

Javadoc ning adresati — sinf ichini ko'rmaydigan foydalanuvchi. Shundan to'g'ri qamrov kelib chiqadi: Javadoc modul yoki kutubxona chegarasidan tashqariga chiqadigan har bir elementga yoziladi, qolgan joyga yozilmaydi.

| Element | Javadoc |
|---|---|
| Public kutubxona API si | majburiy va to'liq |
| Modullar orasidagi public interfeys | majburiy, shartnoma bilan |
| Spring `@Service` ichidagi public metod | faqat shartnoma noaniq bo'lsa |
| Controller metodi | OpenAPI annotatsiyasi, Javadoc emas |
| `private`, `package-private` | kerak emas |
| Record komponentlari | `@param` bilan, agar nom yetarli bo'lmasa |
| Getter/setter | kerak emas |
| Test metodi | kerak emas (nom aytadi) |
| Enum a'zosi | agar ma'nosi nomdan ko'rinmasa |

### 10.2 Birinchi gap qoidasi va fe'l shakli

Javadoc ning birinchi gapi xulosa sifatida indeksga chiqadi, shuning uchun u mustaqil o'qilishi kerak va nuqta bilan tugashi shart. Konvensiya: metod uchun uchinchi shaxs fe'l ("Qaytaradi...", "Rezerv qiladi..."), sinf uchun ot iborasi.

```java
/**
 * Buyurtma uchun omborda qoldiqni rezerv qiladi.
 *
 * <p>Rezerv idempotent: bir xil {@code reservationKey} bilan takroriy chaqiruv
 * yangi rezerv yaratmaydi va mavjudini qaytaradi.
 *
 * @param order rezerv qilinadigan buyurtma, {@code null} bo'lmaydi
 * @param reservationKey takroriy chaqiruvni aniqlash kaliti
 * @return yaratilgan yoki mavjud rezerv
 * @throws InsufficientStockException qoldiq yetmasa
 * @throws IllegalArgumentException {@code order} bo'sh bo'lsa
 */
public Reservation reserve(Order order, ReservationKey reservationKey) { ... }
```

### 10.3 `@param`, `@return`, `@throws` to'liqligi

Uchta teg to'liq bo'lishi kerak yoki umuman bo'lmasligi kerak — yarim to'ldirilgan Javadoc eng yomon holat, chunki o'quvchi qolganini ham yo'q deb o'ylaydi.

Har bir teg uchun aniq talab bor. `@param` — qiymatning ma'nosi va chegarasi (`null` bo'lishi mumkinmi, diapazon qanday). `@return` — nima qaytadi va bo'sh holat qanday ifodalanadi. `@throws` — **har bir** tekshiriladigan istisno, va unchecked istisnolardan chaqiruvchi uchun ma'noli bo'lganlari.

```java
// yomon: tur nomini takrorlaydi, ma'lumot bermaydi
/** @param amount summa */

// yaxshi: ma'no, birlik, chegara
/** @param amount qaytarilayotgan summa; musbat va to'langan summadan oshmasligi kerak */
```

### 10.4 Shartnoma yozish: oldin shart, keyin shart, invariant

Javadoc ning eng qimmatli qismi — shartnoma. Uchta savolga javob berish kerak: chaqirishdan oldin nima to'g'ri bo'lishi kerak (precondition), chaqiruvdan keyin nima kafolatlanadi (postcondition), va nima har doim to'g'ri qoladi (invariant).

Spring va JPA kontekstida shartnomaga qo'shimcha to'rt element kiradi va ularning yo'qligi eng ko'p xatolarga sabab bo'ladi: tranzaksiya talabi, idempotentlik, thread-safety, va yon ta'sirlar.

```java
/**
 * To'lovni bank bilan yopadi.
 *
 * <p><b>Tranzaksiya:</b> chaqiruvchi tranzaksiya ochmasligi kerak - bu metod
 * tashqi chaqiruv qiladi va o'z tranzaksiyasini qisqa ushlaydi.
 * <p><b>Idempotentlik:</b> bir xil {@code paymentId} uchun takroriy chaqiruv xavfsiz.
 * <p><b>Thread-safety:</b> bu sinf stateless va thread-safe.
 * <p><b>Yon ta'sir:</b> muvaffaqiyatli yopilganda {@code PaymentSettled} hodisasi chiqadi.
 */
public SettlementResult settle(PaymentId paymentId) { ... }
```

### 10.5 `{@link}`, `{@code}`, `@see` va havola gigiyenasi

`{@code}` matnni kod shriftida ko'rsatadi va HTML belgilarini qochiradi — barcha tur nomlari, qiymatlar va `null` shu teg ichida yozilishi kerak. `{@link}` esa haqiqiy havola yaratadi va kompilyatsiya vaqtida tekshiriladi, shuning uchun sinf va metod nomlari uchun `{@code}` emas, `{@link}` afzal: nom o'zgarsa Javadoc buziladi va eslatadi.

```java
// yaxshi: havola tekshiriladi
/** Natijani {@link SettlementResult} sifatida qaytaradi, xato bo'lsa {@code null} emas. */

// yomon: matn sifatida yozilgan, nom o'zgarsa yolg'on qoladi
/** Natijani SettlementResult sifatida qaytaradi. */
```

`@see` ni faqat haqiqiy qo'shimcha kontekst uchun ishlatish kerak; har bir tegishli sinfga `@see` qo'yish shovqin.

### 10.6 `@since`, `@deprecated` va almashtirish ko'rsatmasi

`@since` public API da versiya tarixini beradi va u kutubxona foydalanuvchisi uchun muhim. `@Deprecated` esa har doim ikki qismdan iborat bo'lishi kerak: annotatsiya (kompilyator ogohlantirishi uchun) va `@deprecated` Javadoc tegi (nima o'rniga ishlatilishi uchun).

```java
/**
 * @deprecated 2.4 dan boshlab o'rniga {@link #settle(PaymentId)} ishlatiladi:
 *     eski metod valyutani hisobga olmaydi. 3.0 da o'chiriladi.
 * @since 1.0
 */
@Deprecated(since = "2.4", forRemoval = true)
public void settleLegacy(long paymentId) { ... }
```

Almashtirish ko'rsatmasi bo'lmagan `@Deprecated` foydasiz: foydalanuvchi ogohlantirishni ko'radi, lekin nima qilishini bilmaydi.

### 10.7 Paket va modul hujjati

`package-info.java` fayli paketning maqsadini, chegarasini va qaysi sinflar kirish nuqtasi ekanini aytadi. Bu eng kam ishlatiladigan va eng foydali hujjat shakli, chunki yangi odam paketga kirganda birinchi shu faylni ochadi.

```java
/**
 * To'lov va bank bilan hisob-kitob konteksti.
 *
 * <p>Kirish nuqtalari: {@link uz.shop.payment.PaymentService} va
 * {@link uz.shop.payment.SettlementService}. Qolgan sinflar ichki va
 * {@code package-private}.
 *
 * <p>Bu paket boshqa paketlarning jadvallariga murojaat qilmaydi; tashqi
 * ma'lumot faqat {@link uz.shop.order.OrderApi} orqali olinadi.
 */
@NullMarked
package uz.shop.payment;
```

`@NullMarked` (JSpecify) kabi paket darajasidagi annotatsiyalar ham shu faylda turadi (arxitektor hujjati 13.10).

### 10.8 Namuna kod va uni kompilyatsiya ostida ushlash

Javadoc dagi namuna kod eng tez eskiradigan hujjat, chunki uni hech narsa tekshirmaydi. Java 18 dan beri `{@snippet}` tegi bor va u namunani tashqi faylga (yoki test kodiga) bog'lash imkonini beradi — shunda namuna kompilyatsiya va test ostida qoladi.

```java
/**
 * Mijozni rezerv bilan yaratadi.
 *
 * {@snippet file = "ReservationExamples.java" region = "simple-reserve"}
 */
public Reservation reserve(Order order) { ... }
```

Agar `{@snippet}` ishlatilmasa, ikkinchi yaxshi yechim: namunani testda saqlab, Javadoc da test metodiga `{@link}` qo'yish.

### 10.9 Javadoc ni CI da tekshirish

Javadoc toza qolishi uchun uni mashina tekshirishi kerak. `javadoc` vositasining `-Xdoclint` tekshiruvi buzilgan havolalarni, yetishmayotgan `@param` larni va noto'g'ri HTML ni topadi.

```xml
<plugin>
  <artifactId>maven-javadoc-plugin</artifactId>
  <configuration>
    <!-- Buzilgan havola va yetishmayotgan teg xato sifatida qaraladi -->
    <doclint>all</doclint>
    <failOnWarnings>true</failOnWarnings>
    <!-- Faqat public API hujjatlanadi: ichki sinflar shovqin qo'shmaydi -->
    <show>protected</show>
  </configuration>
  <executions>
    <execution>
      <id>javadoc-check</id>
      <phase>verify</phase>
      <goals><goal>jar</goal></goals>
    </execution>
  </executions>
</plugin>
```

Kutubxona bo'lmagan ilovada `doclint` ni faqat `api` paketlariga yo'naltirish mumkin, shunda ichki kod uchun Javadoc majburiyati tug'ilmaydi (9.4).

### 10.10 Kod ichidagi hujjat va repodagi hujjat bo'linishi

Hujjatning qayerda turishi uning hayot muddatini belgilaydi. Qoida: kod bilan birga o'zgaradigan ma'lumot kodda, undan sekinroq o'zgaradigan ma'lumot repoda, undan ham sekinroq o'zgaradigani wiki da turadi.

| Ma'lumot | Joyi |
|---|---|
| Metod shartnomasi | Javadoc |
| Paket maqsadi va chegarasi | `package-info.java` |
| Sinf ichidagi qaror asosi | kod ichidagi izoh (8.4) |
| Arxitektura qarori | `docs/adr/` (arxitektor hujjati 3-bob) |
| Loyihani ishga tushirish | `README.md` |
| API shartnomasi (tashqi) | OpenAPI spetsifikatsiyasi |
| Domen lug'ati | `docs/glossary.md` (3.14) |
| Reliz o'zgarishlari | `CHANGELOG.md` (40.3) |
| Operatsion qo'llanma | runbook, repoda yoki wiki da |

### 10.11 Amalda qo'llash

- [ ] Javadoc siyosatini yozib qo'ying: qaysi elementlarga majburiy, qaysilariga taqiqlangan (10.1 jadvali).
- [ ] Public API metodlarida `@param`, `@return`, `@throws` to'liqligini tekshirib, yarim to'ldirilganlarini tugating.
- [ ] Shartnomaga tranzaksiya, idempotentlik, thread-safety va yon ta'sir qatorlarini qo'shing.
- [ ] Javadoc dagi sinf nomlarini `{@link}` ga o'tkazib, havolalarni kompilyator tekshiradigan qiling.
- [ ] Barcha `@Deprecated` larga `@deprecated` tegi, almashtirish va o'chirish versiyasini qo'shing.
- [ ] Har bir public paketga `package-info.java` yozib, kirish nuqtalari va chegarani belgilang.
- [ ] `maven-javadoc-plugin` ni `doclint=all` va `failOnWarnings` bilan CI ga qo'shing.
- [ ] Javadoc dagi namuna kodlarni `{@snippet}` orqali testdagi faylga bog'lang.
# IV. Formatlash va kod uslubi

## 11. Vertikal formatlash (Vertical Formatting)

Formatlash did masalasi emas, muloqot masalasi: u o'quvchining ko'zini boshqaradi. Bu bobda vertikal o'q bo'yicha qoidalar — fayl uzunligi, bo'sh qatorlar, e'lon va ishlatish orasidagi masofa, a'zolar tartibi. Bu qoidalarning katta qismi formatter bilan avtomatlashtirilmaydi, shuning uchun ularni bilish kerak (13-bob avtomatlashtirilgan qismi haqida).

### 11.1 Fayl o'lchami va sinf uzunligi

Katta kod bazalaridagi kuzatish: toza loyihalarda fayllarning katta qismi 200 qatordan kichik va eng kattasi 500 qatordan oshmaydi. Bu qoida emas, natija: sinf bitta javobgarlikni olsa, u o'z-o'zidan kichik bo'lib qoladi.

Shu sababli fayl uzunligini **belgi** sifatida ishlatish kerak, maqsad sifatida emas. 800 qatorli sinf uzunligi uchun jazolanmaydi; u ichida bir necha javobgarlik borligi uchun bo'linadi.

```bash
# Eng katta fayllar ro'yxati: bo'lish nomzodlari
find src/main/java -name '*.java' | xargs wc -l | sort -rn | head -20

# Fayl uzunligi taqsimoti: kod bazasi holatini bir qarashda ko'rsatadi
find src/main/java -name '*.java' | xargs wc -l | awk '{print $1}' \
  | awk '{ if ($1<100) a++; else if ($1<300) b++; else if ($1<500) c++; else d++ }
         END { printf "<100: %d\n100-300: %d\n300-500: %d\n500+: %d\n", a,b,c,d }'
```

### 11.2 Gazeta metaforasi: yuqoridan pastga ma'lumot zichligi

Yaxshi manba fayli gazeta maqolasiga o'xshaydi: yuqorida eng umumiy ma'lumot, pastga tushgan sari tafsilot ortadi. Fayl nomi sarlavha, yuqoridagi e'lonlar va public metodlar — kirish qismi, pastdagi private metodlar — tafsilot.

Shundan amaliy tartib chiqadi va u Java konvensiyasi bilan mos: paket, importlar, sinf Javadoc i, statik konstantalar, maydonlar, konstruktor, public metodlar, private metodlar (11.6).

### 11.3 Tushunchalar orasida bo'sh qator

Bo'sh qator o'quvchi uchun eng arzon va eng kuchli signal: "bu yerda yangi fikr boshlanadi". Paket e'lonidan keyin, importlardan keyin, har bir metod orasida bo'sh qator bo'lishi kerak.

```java
// yomon: hamma narsa bir blokda, ko'z to'xtaydigan joy yo'q
package uz.shop.payment;
import java.time.Instant;
public final class SettlementService {
    private final PaymentGateway gateway;
    SettlementService(PaymentGateway gateway) { this.gateway = gateway; }
    public SettlementResult settle(PaymentId id) { ... }
}

// yaxshi: har bir tushuncha ajratilgan
package uz.shop.payment;

import java.time.Instant;

public final class SettlementService {

    private final PaymentGateway gateway;

    SettlementService(PaymentGateway gateway) {
        this.gateway = gateway;
    }

    public SettlementResult settle(PaymentId id) { ... }
}
```

### 11.4 Vertikal zichlik: birga o'qiladigan qatorlarni ajratmaslik

Bo'sh qator ajratadi, zichlik esa bog'laydi. Bir-biriga zich bog'langan qatorlar orasiga bo'sh qator yoki izoh qo'yish bog'lanishni buzadi va o'quvchi ko'zini keraksiz sakrashga majbur qiladi.

```java
// yomon: har bir maydon izoh bilan ajratilgan, bog'liqlik ko'rinmaydi
public class ReporterConfig {
    /** Reporter listener sinfining nomi */
    private String className;

    /** Reporter listener xususiyatlari */
    private List<Property> properties = new ArrayList<>();
}

// yaxshi: uchta qator bir butun sifatida o'qiladi
public class ReporterConfig {
    private String className;
    private List<Property> properties = new ArrayList<>();
}
```

### 11.5 Vertikal masofa: e'lon va ishlatish orasidagi oraliq

Mahalliy o'zgaruvchi birinchi ishlatilishiga iloji boricha yaqin e'lon qilinishi kerak. Metod kichik bo'lsa, bu tabiiy; metod uzun bo'lsa, 40 qator yuqorida e'lon qilingan o'zgaruvchi o'quvchidan skroll qilishni talab qiladi.

Teskari qoida instans maydonlariga tegishli: ular sinf boshida, bir joyda to'planadi. Maydonni sinf o'rtasida e'lon qilish (C++ dagi ba'zi uslublar) Java da qabul qilinmaydi va o'quvchi maydonni topolmaydi.

```java
// yomon: e'lon va ishlatish orasida 30 qator
public void importFile(Path file) {
    int rejected = 0;
    ... 30 qator boshqa ish ...
    rejected++;
}

// yaxshi: e'lon ishlatish yonida; yoki butunlay yo'q (hisob alohida metodda)
public void importFile(Path file) {
    List<SettlementRow> rows = parse(file);
    long rejected = rows.stream().filter(not(this::isValid)).count();
    log.info("import tugadi: {} rad etildi", rejected);
}
```

### 11.6 Maydonlar joylashuvi va a'zolar tartibi

Sinf a'zolarining tartibi konvensiya bilan belgilanadi va u butun kod bazasida bir xil bo'lishi kerak, chunki o'quvchi odatlanadi.

| Tartib | Element |
|---|---|
| 1 | `static final` konstantalar |
| 2 | `static` maydonlar (kamdan-kam, 16.9) |
| 3 | instans maydonlari (`private final` birinchi) |
| 4 | konstruktorlar (eng umumiysi oxirida) |
| 5 | statik fabrika metodlari |
| 6 | public metodlar (chaqiruv tartibida, 4.4) |
| 7 | `package-private` metodlar |
| 8 | private metodlar (chaqiruvchidan keyin) |
| 9 | `equals`, `hashCode`, `toString` |
| 10 | ichki (nested) turlar |

Checkstyle `DeclarationOrder` va `OverloadMethodsDeclarationOrder` qoidalari shu tartibni mashinaga topshiradi.

### 11.7 Bog'liq funksiyalarni yonma-yon qo'yish

Agar bir funksiya ikkinchisini chaqirsa, ular vertikal jihatdan yaqin bo'lishi kerak va chaqiruvchi yuqorida turishi kerak. Shunda o'qish bir yo'nalishda boradi va "bu metod qayerda?" savoli tug'ilmaydi.

Overload qilingan metodlar ham yonma-yon turishi kerak, orasiga boshqa metod tushmasligi kerak — aks holda o'quvchi barcha variantlarni bir vaqtda ko'rolmaydi.

### 11.8 Tushunchaviy yaqinlik

Ba'zi kod bo'laklari bir-birini chaqirmasa ham, bir tushunchaga tegishli bo'ladi: bir xil nom shakli, bir xil vazifa, bir xil domen qoidasi. Ularni yonma-yon qo'yish o'quvchi uchun guruhni ko'rinadigan qiladi.

```java
// Bir tushuncha: assertion yordamchilari. Bir-birini chaqirmaydi, lekin birga turadi.
static void assertTrue(boolean condition) { ... }
static void assertTrue(String message, boolean condition) { ... }
static void assertFalse(boolean condition) { ... }
static void assertFalse(String message, boolean condition) { ... }
```

### 11.9 Vertikal tartib: chaqiruvchi yuqorida

Java va C# da konvensiya bir xil: chaqiruvchi funksiya chaqiriladigan funksiyadan yuqorida turadi. Bu "pastga tushish qoidasi" ning (4.4) vertikal ifodasi va o'qishni tabiiy yo'nalishda ushlab turadi.

Istisno: `equals`, `hashCode`, `toString` va boshqa shartnoma metodlari sinf oxirida to'planadi (11.6), chunki ular hikoyaning qismi emas, shartnomaning qismi.

### 11.10 Amalda qo'llash

- [ ] 11.1 dagi skript bilan fayl uzunligi taqsimotini chiqarib, 500 qatordan katta fayllarni bo'lish ro'yxatiga kiriting.
- [ ] Sinf a'zolari tartibini 11.6 jadvaliga keltirib, Checkstyle `DeclarationOrder` bilan mahkamlang.
- [ ] Mahalliy o'zgaruvchi e'lonlarini birinchi ishlatilishiga yaqin ko'chirib, metod boshidagi "e'lon bloki" ni yo'qoting.
- [ ] Overload qilingan metodlar yonma-yon turishini tekshirib, orasiga tushgan metodlarni ko'chiring.
- [ ] Bir-birini chaqiradigan metodlarni chaqiruvchi yuqorida bo'lgan tartibga keltiring.
- [ ] Maydonlar orasidagi keraksiz Javadoc bloklarini olib tashlab, vertikal zichlikni tiklang.
- [ ] Paket, import va sinf e'lonlari orasida bo'sh qator borligini formatter bilan ta'minlang.
- [ ] `equals`/`hashCode`/`toString` ni sinf oxiriga ko'chiring va shu konvensiyani hujjatlashtiring.
## 12. Gorizontal formatlash va kod uslubi (Horizontal Formatting and Style)

Gorizontal o'q bo'yicha qoidalar kamroq, lekin ulardan biri — qator uzunligi — eng ko'p bahs qo'zg'atadigan qoida. Bu bobda qator uzunligi, bo'shliq, tekislash, indentatsiya, import tartibi va zanjirli chaqiruvni bo'lish ko'rib chiqiladi.

### 12.1 Qator uzunligi chegarasi va uni tanlash

Qator uzunligi chegarasining maqsadi — gorizontal skrollni yo'qotish va yonma-yon diff ni o'qiladigan qilish. Zamonaviy ekranlarda 80 juda qisqa, 200 esa diff ni buzadi. Amalda uchta tanlov ishlatiladi: 100 (eng keng tarqalgan), 120 (Spring ekotizimida ko'p), 80 (klassik).

Muhimi — son emas, chegara borligi va uni formatter majburlashi. Chegara bo'lmasa, uzun ifodalar paydo bo'ladi va ularni o'qish uchun gorizontal skroll kerak bo'ladi, bu esa code review ni ikki marta qiyinlashtiradi.

| Chegara | Afzalligi | Kamchiligi |
|---|---|---|
| 80 | ikki fayl yonma-yon, terminalga sig'adi | Java da ko'p bo'linish |
| 100 | muvozanat, diff o'qiladi | — |
| 120 | kam bo'linish | yonma-yon diff siqiladi |
| chegarasiz | bo'linish yo'q | review buziladi |

### 12.2 Gorizontal bo'shliq: operator, qavs, vergul

Bo'shliq bog'liqlikni ko'rsatadi: zich turgan narsalar bir butun, ajratilgan narsalar alohida. Konvensiya: binar operator atrofida bo'shliq, vergul keyin bo'shliq, qavs ichida bo'shliq yo'q, metod nomi va qavs orasida bo'shliq yo'q.

Prioriteti yuqori operatorlarni zich yozish o'qilishga yordam beradi, lekin google-java-format bunga ruxsat bermaydi va bu to'g'ri qaror: izchillik did dan muhimroq.

```java
// yaxshi: standart konvensiya
int lineSize = line.length();
total = total.add(price.multiply(quantity));
settle(payment, gateway, timeout);

// yomon: izchil emas
int lineSize=line.length();
settle( payment,gateway , timeout );
```

### 12.3 Gorizontal tekislash nega zarar qiladi

E'lonlarni yoki tayinlashlarni ustun bo'yicha tekislash (vertikal tekislash) chiroyli ko'rinadi, lekin uch zarari bor: diff shovqini (bitta nom o'zgarsa butun blok o'zgaradi), o'qish adashishi (ko'z tur emas, nomga qaraydi), va formatter bilan kurash.

```java
// yomon: tekislangan - bitta uzun nom qo'shilsa butun blok o'zgaradi
private   Socket          socket;
private   InputStream     input;
private   OutputStream    output;
private   Request         request;

// yaxshi: oddiy, diff toza
private Socket socket;
private InputStream input;
private OutputStream output;
private Request request;
```

### 12.4 Indentatsiya va uni buzmaslik

Indentatsiya kodning ierarxiyasini ko'rsatadigan asosiy vosita. Java konvensiyasi: 4 bo'shliq, tab emas (tab turli muhitlarda turlicha ko'rinadi va diff ni buzadi). Ikkinchi darajali davomiy qator uchun 8 bo'shliq.

Indentatsiyani buzish — bir qatorli `if` yoki metodni indentatsiyasiz yozish — vaqt tejamaydi, lekin ierarxiyani yashiradi.

```java
// yomon: indentatsiya buzilgan, ierarxiya ko'rinmaydi
public class CommentWidget extends Widget {
    public static final String REGEXP = "^#[\r\n]";
    public CommentWidget(ParentWidget parent, String text) { super(parent, text); }
    public String render() throws Exception { return ""; }
}

// yaxshi
public class CommentWidget extends Widget {

    public static final String REGEXP = "^#[\r\n]";

    public CommentWidget(ParentWidget parent, String text) {
        super(parent, text);
    }

    public String render() throws Exception {
        return "";
    }
}
```

### 12.5 Bo'sh blok va "dummy scope"

Bo'sh blok (`while (condition);`) eng xavfli formatlash xatosi, chunki nuqta-vergul ko'rinmaydi va keyingi qator sikl tanasi deb o'qiladi. Qoida: bo'sh blok har doim qavs bilan yoziladi va ichida nega bo'shligi izohlanadi.

```java
// yomon: ; ko'rinmaydi, keyingi qator sikl tanasi emas
while (dis.read(buf, 0, readBufferSize) != -1);

// yaxshi: qavs va izoh
while (dis.read(buf, 0, readBufferSize) != -1) {
    // Oqimni oxirigacha o'qib tashlaymiz: mazmuni kerak emas, faqat
    // ulanish to'g'ri yopilishi uchun bufer bo'shatiladi.
}
```

Xuddi shu qoida bo'sh `catch` ga tegishli (patternlar hujjati 25.14 Exception Swallowing) — u hech qachon izohsiz qolmaydi.

### 12.6 Qavs uslubi va bir qatorli `if`

Java ekotizimida K&R uslubi standart: ochiluvchi qavs shu qatorda, yopiluvchi qavs alohida qatorda. Uslub tanlovi muhim emas; izchillik muhim va uni formatter ta'minlaydi.

Bir qatorli `if` (4.8 da ko'rilgan) formatlash nuqtai nazaridan ham zararli: u diff da qo'shilgan qatorni ko'rinmas qiladi va qavs qo'shishni talab qiladi.

### 12.7 Import tartibi va yulduzcha import

Importlar tartibi guruhlangan va alifbo bo'yicha saralangan bo'lishi kerak, aks holda har bir yangi import diff da tasodifiy joyga tushadi va konfliktlar ko'payadi.

Yulduzcha (`import java.util.*`) ikki zarar keltiradi: qaysi sinf qayerdan kelganini yashiradi, va ikki paketda bir xil nomli sinf bo'lsa (`java.util.Date` va `java.sql.Date`) konflikt tug'diradi. Qoida: yulduzcha import taqiqlanadi, statik import esa faqat test assertion lari va `Math` kabi aniq holatlarda ruxsat etiladi.

```java
// yaxshi: guruhlangan, aniq, saralangan
import java.time.Duration;
import java.time.Instant;
import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import uz.shop.order.OrderApi;

import static java.util.Comparator.comparing;
import static java.util.function.Predicate.not;
```

### 12.8 Zanjirli chaqiruv va oqimni bo'lish

Oqim va builder zanjirlari uzun bo'ladi va ularni bo'lish qoidasi bor: har bir zanjir bo'g'ini alohida qatorda, nuqta qator boshida. Shunda har bir qadam ko'rinadi va diff faqat o'zgargan qadamni ko'rsatadi.

```java
// yomon: bir qatorda, qaysi qadam o'zgarganini diff ko'rsatmaydi
return orders.stream().filter(Order::isPaid).map(Order::total).reduce(Money.ZERO, Money::add);

// yaxshi: har bir qadam alohida, nuqta boshida
return orders.stream()
        .filter(Order::isPaid)
        .map(Order::total)
        .reduce(Money.ZERO, Money::add);
```

Zanjir uch bo'g'indan oshsa va har bir bo'g'in murakkab bo'lsa, oraliq natijani nomlangan o'zgaruvchiga chiqarish o'qilishni yaxshilaydi (35-bob, Extract Variable).

### 12.9 Uzun satr, matn bloki va SQL joylashtirish

Uzun satr literalini `+` bilan bo'lish o'qilmaydi va formatterni chalg'itadi. Java 15 dan beri matn bloki (`"""`) bor va SQL, JSON, XML uchun to'g'ri yechim (arxitektor hujjati 13.4).

```java
// yomon: + bilan bo'lingan SQL
String sql = "select p.id, p.amount " +
             "from payment p " +
             "where p.order_id = ? and p.settled_at is not null";

// yaxshi: matn bloki, indentatsiya avtomatik olib tashlanadi
String sql = """
        select p.id, p.amount
        from payment p
        where p.order_id = ?
          and p.settled_at is not null
        """;
```

### 12.10 Fayl kodirovkasi, qator oxiri va oxirgi bo'sh qator

Bu qoidalar ko'rinmas, lekin ularning yo'qligi diff ni buzadi va cross-platform jamoada har bir commit da butun fayl o'zgargan bo'lib ko'rinadi.

```ini
# .gitattributes - repoda qator oxirini normallashtirish
*       text=auto eol=lf
*.bat   text eol=crlf
*.jar   binary
*.png   binary
```

| Sozlama | To'g'ri qiymat |
|---|---|
| Kodirovka | UTF-8 (hamma joyda, `pom.xml` da ham) |
| Qator oxiri | LF (`.gitattributes` bilan majburiy) |
| Oxirgi qator | bo'sh qator bilan tugaydi |
| Orqa bo'shliqlar | olib tashlanadi |
| Tab | bo'shliqqa aylantiriladi |
| BOM | yo'q |

### 12.11 Amalda qo'llash

- [ ] Qator uzunligi chegarasini tanlab (100 tavsiya etiladi), uni formatter va Checkstyle da bir xil qiymatga qo'ying.
- [ ] Gorizontal tekislangan e'lon bloklarini formatter bilan oddiy shaklga keltirib, diff shovqinini yo'qoting.
- [ ] Yulduzcha importlarni taqiqlab (Checkstyle `AvoidStarImport`), mavjudlarini IDE bilan yoyib yuboring.
- [ ] Import tartibini guruhlar bo'yicha belgilab, Spotless `importOrder` ga yozib qo'ying.
- [ ] `+` bilan bo'lingan SQL va JSON literallarini matn blokiga o'tkazing.
- [ ] `.gitattributes` va `.editorconfig` fayllarini qo'shib, kodirovka va qator oxirini normallashtiring.
- [ ] Bo'sh bloklarni (`;` bilan tugagan sikl, bo'sh `catch`) topib, qavs va izoh qo'shing.
- [ ] Uzun oqim zanjirlarini har bir bo'g'in alohida qatorda bo'ladigan shaklga keltiring.
## 13. Formatlashni avtomatlashtirish va diff gigiyenasi (Automated Formatting and Diff Hygiene)

Formatlash haqidagi bahs code review vaqtining eng foydasiz qismi. Yechim oddiy: formatlashni mashinaga topshirish va bahsni butunlay yopish. Bu bobda shu sozlamaning aniq mexanikasi va formatlash o'zgarishlarini tarixni buzmaydigan qilib kiritish usullari.

### 13.1 Bitta jamoa, bitta uslub: tanlov emas, sozlama

Uslub tanlovida eng yaxshi variant yo'q, lekin eng yomon variant bor: har kimning o'z uslubi. Shu sababli qoida shunday: uslub bir marta tanlanadi, repoda sozlama sifatida saqlanadi va keyin muhokama qilinmaydi.

Amalda eng tez yo'l — tayyor uslubni olish va o'zgartirmaslik. google-java-format yoki Spring Java Format ikkisi ham to'liq, sozlanmaydigan (yoki kam sozlanadigan) va shu sababli bahsni yopadi. Sozlanadigan uslub tanlansa, jamoa oylar davomida qavs va bo'shliq haqida gaplashadi.

### 13.2 `.editorconfig` va IDE sozlamalarini repoda saqlash

`.editorconfig` barcha zamonaviy IDE tomonidan o'qiladi va eng arzon yechim: yangi odam repoyni ochadi va uning muharriri darhol to'g'ri sozlanadi.

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space

[*.java]
indent_size = 4
max_line_length = 100
# Wildcard import taqiqlangan (IntelliJ shu kalitni o'qiydi)
ij_java_class_count_to_use_import_on_demand = 999
ij_java_names_count_to_use_import_on_demand = 999

[*.{yml,yaml,json}]
indent_size = 2

[*.sql]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

### 13.3 Spotless va google-java-format o'rnatish

Spotless formatlashni build ning qismiga aylantiradi: `spotless:apply` tuzatadi, `spotless:check` CI da bloklaydi. Shu ikki buyruq formatlash haqidagi review izohlarini butunlay yo'qotadi.

```xml
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>2.46.1</version>
  <configuration>
    <java>
      <!-- Sozlanmaydigan formatter: uslub bahsi yopiladi -->
      <googleJavaFormat>
        <version>1.28.0</version>
        <style>AOSP</style>   <!-- AOSP = 4 bo'shliq indentatsiya -->
      </googleJavaFormat>
      <importOrder>
        <order>java,javax,jakarta,,org.springframework,uz.shop,\#</order>
      </importOrder>
      <removeUnusedImports/>
      <trimTrailingWhitespace/>
      <endWithNewline/>
      <licenseHeader>
        <content>/* Copyright (c) $YEAR Shop LLC. LICENSE faylini ko'ring. */</content>
      </licenseHeader>
    </java>
    <pom><sortPom/></pom>
    <sql><includes><include>src/main/resources/db/**/*.sql</include></includes></sql>
  </configuration>
  <executions>
    <execution>
      <!-- Har bir build da tekshiriladi: formatlash buzilgan kod merge bo'lmaydi -->
      <goals><goal>check</goal></goals>
      <phase>validate</phase>
    </execution>
  </executions>
</plugin>
```

Gradle da ekvivalenti `com.diffplug.spotless` plaginida bir xil tuzilishda yoziladi va `./gradlew spotlessApply` buyrug'i bilan ishlatiladi.

### 13.4 Checkstyle qoidalari: faqat mashina tekshiradigani

Checkstyle ning foydali qismi formatlash emas (uni Spotless qiladi), balki **uslub qoidalari**: nom shakllari, taqiqlangan konstruksiyalar, murakkablik chegaralari. Qoidalar ro'yxatini kichik va ma'noli ushlash kerak, aks holda jamoa `@SuppressWarnings` bilan to'ldiradi.

```xml
<module name="Checker">
  <module name="TreeWalker">
    <!-- Nomlash: 2-3 boblardagi qoidalarni majburlaydi -->
    <module name="MemberName">
      <property name="format" value="^[a-z][a-zA-Z0-9]*$"/>   <!-- m_ va _ taqiqlangan -->
    </module>
    <module name="ConstantName"/>
    <module name="TypeName"/>
    <module name="MethodName"/>

    <!-- Tuzilish -->
    <module name="NeedBraces"/>                    <!-- 4.8 -->
    <module name="AvoidStarImport"/>               <!-- 12.7 -->
    <module name="UnusedImports"/>
    <module name="EmptyCatchBlock">
      <property name="exceptionVariableName" value="expected|ignored"/>
    </module>
    <module name="EqualsHashCode"/>                <!-- 15.2 -->
    <module name="MissingSwitchDefault">
      <property name="severity" value="ignore"/>   <!-- 6.6: enum da default kerak emas -->
    </module>
    <module name="NestedIfDepth"><property name="max" value="2"/></module>
    <module name="BooleanExpressionComplexity"><property name="max" value="3"/></module>
    <module name="ParameterNumber"><property name="max" value="4"/></module>  <!-- 5.1 -->
    <module name="IllegalType">
      <property name="illegalClassNames" value="java.util.Date,java.util.Calendar"/>
    </module>
  </module>
  <module name="FileLength"><property name="max" value="500"/></module>  <!-- 11.1 -->
  <module name="NewlineAtEndOfFile"/>
</module>
```

### 13.5 Pre-commit va CI da formatlash tekshiruvi

Formatlash ikki joyda tekshiriladi: mahalliy (tez qaytish uchun) va CI da (kafolat uchun). Mahalliy hook ni majburiy qilmaslik kerak — u faqat qulaylik; kafolat CI da bo'ladi.

```bash
#!/bin/sh
# .githooks/pre-commit  (o'rnatish: git config core.hooksPath .githooks)
# Faqat o'zgargan Java fayllarini formatlaydi: butun repo emas, tez ishlaydi.
changed=$(git diff --cached --name-only --diff-filter=ACM | grep '\.java$')
[ -z "$changed" ] && exit 0

./mvnw -q spotless:apply -DspotlessFiles="$(echo "$changed" | paste -sd, -)" || exit 1
echo "$changed" | xargs git add
```

```yaml
# .github/workflows/build.yml dagi qadam
- name: Formatlash va uslub tekshiruvi
  run: ./mvnw -B spotless:check checkstyle:check
```

### 13.6 Formatlash o'zgarishini mantiq o'zgarishidan ajratish

Eng muhim diff qoidasi: bitta commit da ham formatlash, ham mantiq o'zgarmasligi kerak. Aks holda review da 400 qatorli diff ichida 3 qatorlik mantiq o'zgarishi ko'rinmay ketadi va xato o'tadi.

Amaliy tartib: avval mantiqni o'zgartirib commit qilish, keyin `spotless:apply` ni alohida commit qilish. Teskari tartib ham ishlaydi, muhimi — aralashtirmaslik. Review paytida esa `git diff -w` (bo'shliqlarni e'tiborsiz) bilan tekshirish mumkin.

```bash
# Review da formatlash shovqinini olib tashlab ko'rish
git diff -w --ignore-blank-lines HEAD~1

# PR da faqat mantiq o'zgargan fayllarni ajratish
git diff --stat HEAD~1 | sort -k3 -rn | head
```

### 13.7 Katta formatlash commiti va `.git-blame-ignore-revs`

Butun kod bazasini bir marta formatlash kerak bo'lganda (yangi formatter joriy qilinganda), u `git blame` ni buzadi: har bir qator shu commitga tegishli bo'lib qoladi. Git da bu muammoning rasmiy yechimi bor.

```bash
# 1) Formatlashni alohida commit qilish
./mvnw spotless:apply
git commit -am "Butun kod bazasini google-java-format (AOSP) ga keltirish"

# 2) Commit hash ini ro'yxatga qo'shish
git rev-parse HEAD >> .git-blame-ignore-revs
git commit -am "blame uchun e'tiborsiz qoldiriladigan revizlar ro'yxati"

# 3) Repo sozlamasiga ulash (har bir ishlab chiquvchi bir marta bajaradi)
git config blame.ignoreRevsFile .git-blame-ignore-revs
```

GitHub `.git-blame-ignore-revs` faylini avtomatik o'qiydi, shuning uchun web interfeysdagi blame ham toza qoladi.

### 13.8 Generatsiya qilingan kodni formatlashdan chiqarish

Generatsiya qilingan kod (MapStruct, jOOQ, protobuf, Lombok delombok natijasi, OpenAPI klient) formatlanmaydi va tekshirilmaydi: u har build da qayta yaratiladi va uni tuzatish ma'nosiz.

```xml
<configuration>
  <java>
    <excludes>
      <exclude>target/generated-sources/**</exclude>
      <exclude>src/main/java/**/*MapperImpl.java</exclude>
    </excludes>
  </java>
</configuration>
```

Shu bilan birga, generatsiya qilingan kod `target/` ichida turishi va `git` ga tushmasligi kerak (39.6).

### 13.9 Amalda qo'llash

- [ ] `.editorconfig` faylini repoga qo'shib, kodirovka, indentatsiya va qator uzunligini belgilang.
- [ ] Spotless ni `googleJavaFormat` (yoki Spring Java Format) bilan o'rnatib, `validate` fazasida `check` qiling.
- [ ] Checkstyle qoidalarini 13.4 dagi ro'yxatdan boshlab kiritib, har bir qoidaning sababini hujjatlashtiring.
- [ ] `pre-commit` hook ni `.githooks/` da saqlab, `core.hooksPath` sozlamasini README ga yozing.
- [ ] Butun kod bazasini bir marta formatlab, alohida commit qiling va `.git-blame-ignore-revs` ga qo'shing.
- [ ] Generatsiya qilingan manbalarni formatlash va statik tahlildan chiqarib tashlang.
- [ ] "Formatlash va mantiq bir commitda bo'lmaydi" qoidasini jamoa kelishuviga kiriting.
- [ ] Review da formatlash haqidagi izohlarni taqiqlab, ularni CI xatosiga aylantiring.
# V. Obyekt, ma'lumot va holat

## 14. Obyekt va ma'lumot tuzilmasi: inkapsulyatsiya (Objects vs Data Structures)

Abstraksiya va chegara arxitektor hujjatida (5-bob) ko'rib chiqilgan, Demeter qonuni va Tell-Don't-Ask patternlar hujjatida (26.15-26.16). Bu bobda kod darajasidagi qoidalar: inkapsulyatsiyaning haqiqiy ma'nosi, obyekt va struktura farqi, ichki holatni oshkor qilmaslik, va obyektning o'z invariantini himoya qilishi.

### 14.1 Ma'lumot abstraksiyasi: getter/setter inkapsulyatsiya emas

Har bir maydonga getter va setter yozish inkapsulyatsiya emas: u maydonlarni `public` qilishning uzun yo'li. Haqiqiy inkapsulyatsiya ichki ko'rinishni yashiradi va **abstraksiya** taklif qiladi.

```java
// yomon: ichki ko'rinish to'liq oshkor, abstraksiya yo'q
public class Vehicle {
    public double getFuelTankCapacityInGallons() { ... }
    public double getGallonsOfGasoline() { ... }
}
// chaqiruvchi hisoblashni o'zi qiladi - mantiq tarqaladi

// yaxshi: abstraksiya berilgan, ichki ko'rinish yashirin
public class Vehicle {
    public Percentage getPercentFuelRemaining() { ... }
}
```

Test: agar maydon turini o'zgartirsangiz (`double` → `Money`), nechta chaqiruvchi buziladi? Javob "hammasi" bo'lsa, inkapsulyatsiya yo'q.

### 14.2 Obyekt va ma'lumot tuzilmasining teskariligi

Ikki yondashuv bir-biriga teskari va ikkisi ham o'z o'rnida to'g'ri. **Obyekt** ma'lumotini yashiradi va xatti-harakat taklif qiladi: yangi tur qo'shish oson (mavjud kodga tegmaysiz), yangi funksiya qo'shish qiyin (barcha turlarni o'zgartirasiz). **Ma'lumot tuzilmasi** ma'lumotini oshkor qiladi va xatti-harakati yo'q: yangi funksiya qo'shish oson, yangi tur qo'shish qiyin.

| Ehtiyoj | To'g'ri tanlov |
|---|---|
| Yangi tur tez-tez qo'shiladi | obyekt (polimorfizm) |
| Yangi amal tez-tez qo'shiladi | ma'lumot tuzilmasi + `switch` yoki visitor |
| Domen qoidasi bor | obyekt |
| Faqat ma'lumot tashiydi | `record` (DTO) |
| Tashqi shakl (JSON, jadval) | `record` yoki entitet |
| Hisob va siyosat | obyekt |

Eng ko'p xato — ikkisini aralashtirish, ya'ni gibrid yaratish (14.3).

### 14.3 Gibrid tuzilma: yarim obyekt, yarim struktura

Gibrid — getter va setter lari bor, lekin ichida biznes mantiqi ham bor sinf. U ikki dunyoning kamchiligini oladi: yangi tur qo'shish ham, yangi funksiya qo'shish ham qiyin.

```java
// yomon: gibrid - holat oshkor, lekin mantiq ham ichida
public class Order {
    private List<OrderItem> items;
    private BigDecimal total;

    public List<OrderItem> getItems() { return items; }      // ichki holat oshkor
    public void setTotal(BigDecimal total) { this.total = total; }
    public BigDecimal calculateTotal() { ... }               // mantiq ham shu yerda
}

// yaxshi: obyekt - holat yashirin, xatti-harakat oshkor
public final class Order {
    private final List<OrderItem> items;
    private Money total;

    public void addItem(Sku sku, Quantity quantity, Money unitPrice) {
        requireNotConfirmed();
        items.add(new OrderItem(sku, quantity, unitPrice));
        total = recalculateTotal();
    }

    public List<OrderItem> items() { return List.copyOf(items); }   // himoyalangan nusxa
    public Money total() { return total; }
}
```

### 14.4 Poyezd avariyasi va tuzilmani yashirish

`a.getB().getC().doSomething()` shaklidagi zanjir — poyezd avariyasi (train wreck) va u Demeter qonunini buzadi (patternlar hujjati 26.15). Clean code darajasidagi muhim nuqta: muammo zanjirning uzunligida emas, **kim nimani bilishi kerakligida**.

```java
// yomon: chaqiruvchi uch darajali tuzilmani biladi
String city = order.getCustomer().getAddress().getCity();

// yaxshi (obyekt bo'lsa): so'rash emas, aytish
order.shipTo(shipmentService);

// yaxshi (ma'lumot tuzilmasi bo'lsa): zanjir muammo emas
// record da getter yo'q, maydonga kirish normal
String city = orderDto.customer().address().city();
```

Shuning uchun qoida shunday: **obyekt** da zanjir hid, **ma'lumot tuzilmasi** da zanjir normal.

### 14.5 DTO, Active Record va ularning o'rni

DTO (`record`) — sof ma'lumot tuzilmasi: maydonlar, mantiq yo'q. U tashqi chegarada (HTTP, Kafka, fayl) to'g'ri tanlov va unga biznes qoidasini qo'shish xato.

Active Record — DTO ustiga `save`, `find` metodlari qo'shilgan shakl (JPA entiteti ko'pincha shunday ishlatiladi). U kichik CRUD da ishlaydi, lekin biznes qoidalari ko'payganda gibridga aylanadi. Qoida: Active Record ga biznes qoidasi qo'shila boshlasa, domen obyektini ajratish vaqti keldi.

### 14.6 Maydon ko'rinishi: `public` maydon, `package-private`, `final`

Ko'rinish darajasi eng arzon inkapsulyatsiya vositasi va u ko'pincha ishlatilmaydi. Amaliy tartib: hamma narsa eng kichik ko'rinish bilan boshlanadi va faqat ehtiyoj paydo bo'lganda kengaytiriladi.

| Element | Standart ko'rinish |
|---|---|
| Instans maydoni | `private final` |
| Konstanta | `private static final` (tashqariga kerak bo'lsa `public`) |
| Yordamchi metod | `private` |
| Sinf ichidagi API | `package-private` |
| Modul tashqarisidagi API | `public` |
| Test uchun ochilgan metod | `package-private` (`public` emas) |
| `record` komponenti | avtomatik `private final` |
| JPA entitet maydoni | `private` (Hibernate refleksiya bilan o'qiydi) |

`public` maydon faqat bir holatda haqli: `record` ichidagi komponentlar (ular allaqachon `final` va getter avtomatik).

### 14.7 Ichki to'plamni oshkor qilish va himoyalangan nusxa

Eng ko'p uchraydigan yashirin inkapsulyatsiya buzilishi: getter ichki `List` ni to'g'ridan-to'g'ri qaytaradi va chaqiruvchi uni o'zgartiradi. Obyekt invarianti buziladi va buzilish joyi stack trace da ko'rinmaydi.

```java
// yomon: tashqi kod ichki ro'yxatni o'zgartira oladi
public List<OrderItem> getItems() { return items; }
order.getItems().clear();      // invariant buzildi, Order bilmaydi

// yaxshi: o'zgartirilmas nusxa
public List<OrderItem> items() { return List.copyOf(items); }

// yaxshi: o'zgartirilmas ko'rinish (nusxa qilmaydi, lekin yozishni to'sadi)
public List<OrderItem> items() { return Collections.unmodifiableList(items); }
```

Xuddi shu qoida konstruktorga tegishli: tashqaridan kelgan to'plamni nusxa qilmasdan saqlash chaqiruvchiga ichki holatni o'zgartirish imkonini qoldiradi.

```java
public Order(List<OrderItem> items) {
    this.items = new ArrayList<>(items);   // himoyalangan nusxa, kirishda
}
```

`Date`, massiv va `Calendar` kabi o'zgaradigan turlar ham shu qoidaga kiradi (22.1 da `Date` dan voz kechish sababi).

### 14.8 Statik holat, utility sinf va `private` konstruktor

Statik metodlar to'plami (utility sinf) sof funksiyalar uchun to'g'ri: `StringUtils.capitalize`. Ikki shart bor: sinf `final` va konstruktori `private` (instantiate qilib bo'lmaydi), va ichida **statik holat yo'q**.

```java
// yaxshi: haqiqiy utility
public final class Ibans {

    private Ibans() { throw new AssertionError("instantiate qilinmaydi"); }

    public static boolean isValid(String iban) { ... }
}

// yomon: statik o'zgaradigan holat - thread xavfi va test izolyatsiyasining buzilishi
public final class Counters {
    public static int processed;          // har bir test oldingisiga ta'sir qiladi
}
```

Statik holat qachon haqli: `static final` konstantalar, `Logger`, va `Pattern` kabi thread-safe o'zgarmas obyektlar (21.6).

### 14.9 Obyekt o'z invariantini qanday himoya qiladi

Invariant — obyekt hayoti davomida har doim to'g'ri bo'lishi kerak bo'lgan shart. Uni himoya qilish uchun uch nuqta yopiladi: konstruktor (yaratishda), har bir o'zgartiruvchi metod (o'zgarishda), va seriyalash/deseriyalash (tashqi yo'ldan).

```java
public final class DateRange {

    private final LocalDate fromInclusive;
    private final LocalDate toExclusive;

    public DateRange(LocalDate fromInclusive, LocalDate toExclusive) {
        // Invariant konstruktorda: yaroqsiz obyekt umuman tug'ilmaydi
        if (!fromInclusive.isBefore(toExclusive)) {
            throw new IllegalArgumentException(
                    "boshlanish tugashdan oldin bo'lishi kerak: %s..%s"
                            .formatted(fromInclusive, toExclusive));
        }
        this.fromInclusive = fromInclusive;
        this.toExclusive = toExclusive;
    }

    // O'zgartirish yo'q: har bir amal yangi obyekt qaytaradi (16.4)
    public DateRange extendTo(LocalDate newEnd) {
        return new DateRange(fromInclusive, newEnd);
    }
}
```

Qoida: "yaroqsiz obyekt yaratib bo'lmaydi" tamoyili validatsiyani butun kod bazasidan bir joyga yig'adi.

### 14.10 `this` ning konstruktordan qochib ketishi

Konstruktor tugamasdan obyekt havolasini tashqariga berish yarim qurilgan obyektni oshkor qiladi: maydonlar hali tayinlanmagan, invariant hali tekshirilmagan. Bu xato `final` maydonlar kafolatini ham buzadi.

```java
// yomon: this konstruktordan chiqib ketdi
public class PaymentListener {
    public PaymentListener(EventBus bus) {
        bus.register(this);        // bus boshqa thread'dan darhol chaqirishi mumkin
        this.retryPolicy = new RetryPolicy();   // hali tayinlanmagan!
    }
}

// yaxshi: ro'yxatdan o'tish konstruktordan tashqarida
public final class PaymentListener {

    private final RetryPolicy retryPolicy;

    private PaymentListener(RetryPolicy retryPolicy) { this.retryPolicy = retryPolicy; }

    public static PaymentListener registeredOn(EventBus bus) {
        PaymentListener listener = new PaymentListener(new RetryPolicy());
        bus.register(listener);    // obyekt to'liq qurilgandan keyin
        return listener;
    }
}
```

Spring kontekstida bu qoida `@PostConstruct` yoki `ApplicationReadyEvent` da ro'yxatdan o'tish shaklida qo'llanadi (26.1).

### 14.11 Amalda qo'llash

- [ ] Barcha getter lari to'plam qaytaradigan sinflarni topib, `List.copyOf` yoki o'zgartirilmas ko'rinishga o'tkazing.
- [ ] Konstruktorda tashqaridan kelgan to'plam va massivlarni nusxa qilib saqlashni ta'minlang.
- [ ] Setter lari va biznes mantiqi birga turgan gibrid sinflarni ro'yxatlab, holatni yashirishga o'tkazing.
- [ ] Barcha maydonlarni `private final` qilib, faqat zarur joyda ko'rinishni kengaytiring.
- [ ] Utility sinflarini `final` va `private` konstruktor bilan yoping; statik o'zgaradigan holatni yo'qoting.
- [ ] Value object larda invariantni konstruktorga ko'chirib, tarqalgan validatsiyani olib tashlang.
- [ ] Konstruktorda `this` ni tashqariga beradigan joylarni statik fabrikaga yoki `@PostConstruct` ga ko'chiring.
- [ ] Har bir DTO da biznes mantiqi yo'qligini, har bir domen obyektida esa oshkor setter yo'qligini tekshiring.
## 15. Tenglik, hash va obyekt shartnomalari (Equality, Hashing and Object Contracts)

`equals`, `hashCode`, `compareTo` va `toString` — Java da eng ko'p noto'g'ri yoziladigan to'rt metod, va ularning xatosi eng qiyin topiladigan xatolar qatoriga kiradi: `HashMap` dan yozuv yo'qoladi, `TreeSet` tartibi buziladi, log da ma'lumot oqib ketadi. Bu bobda to'rt shartnomaning aniq talablari va ularni Java da to'g'ri bajarish.

### 15.1 `equals` shartnomasi: besh qoida

`equals` metodi matematik ekvivalentlik munosabatini amalga oshirishi kerak. Beshta qoida bor va ularning har biri buzilganda alohida muammo tug'iladi.

| Qoida | Talab | Buzilsa |
|---|---|---|
| Refleksivlik | `x.equals(x)` → `true` | `contains` ishlamaydi |
| Simmetriklik | `x.equals(y)` == `y.equals(x)` | to'plam tartibiga qarab natija o'zgaradi |
| Tranzitivlik | `x=y`, `y=z` → `x=z` | `HashSet` dublikat saqlaydi |
| Izchillik | qiymat o'zgarmasa natija o'zgarmaydi | yozuv yo'qoladi (15.9) |
| `null` | `x.equals(null)` → `false` | `NullPointerException` |

Eng ko'p buziladigani — simmetriklik, va u odatda vorislikda yoki turlar aralashganda chiqadi (`String` bilan `CaseInsensitiveString` ni solishtirish).

### 15.2 `hashCode` shartnomasi va `equals` bilan bog'liqligi

`hashCode` ning yagona majburiy qoidasi: `equals` bo'yicha teng obyektlar bir xil `hashCode` qaytarishi kerak. Teskarisi shart emas (turli obyektlar bir xil hash olishi mumkin).

Shundan eng ko'p uchraydigan xato kelib chiqadi: `equals` yozilgan, `hashCode` yozilmagan. Bunda obyekt `HashMap` ga qo'yiladi va keyin topilmaydi, chunki `Object.hashCode` identifikatsiya bo'yicha ishlaydi. Checkstyle `EqualsHashCode` qoidasi shu xatoni CI da bloklaydi (13.4).

```java
// yomon: equals bor, hashCode yo'q - HashMap ishlamaydi
public final class Sku {
    private final String code;
    @Override public boolean equals(Object o) { ... }
    // hashCode yo'q!
}

// yaxshi: ikkisi birga, bir xil maydonlardan
public final class Sku {

    private final String code;

    @Override
    public boolean equals(Object o) {
        return o instanceof Sku other && code.equals(other.code);
    }

    @Override
    public int hashCode() {
        return code.hashCode();
    }
}
```

### 15.3 `equals` ni yozish shabloni va `instanceof` pattern matching

Zamonaviy Java da `equals` ni yozish shabloni qisqargan: `instanceof` pattern matching bir qadamda tur tekshiruvini va o'zgaruvchi e'lonini bajaradi.

```java
@Override
public boolean equals(Object o) {
    // 1) O'zini o'zi bilan solishtirish - tez yo'l (ixtiyoriy, lekin arzon)
    if (this == o) return true;
    // 2) Tur tekshiruvi va cast bir qadamda; null avtomatik false beradi
    if (!(o instanceof Payment other)) return false;
    // 3) Muhim maydonlar: arzonidan boshlab solishtirish
    return amount.equals(other.amount)
            && currency == other.currency           // enum: == yetarli
            && paymentId.equals(other.paymentId);
}
```

Eng oson va eng xavfsiz yechim esa — `record` ishlatish: `equals`, `hashCode` va `toString` avtomatik generatsiya qilinadi va shartnomaga mos bo'ladi (arxitektor hujjati 13.1).

### 15.4 Vorislik ostida tenglik: `getClass()` yoki `instanceof`

Bu klassik dilemma. `getClass() != o.getClass()` tekshiruvi simmetriklikni saqlaydi, lekin Liskov printsipini buzadi: voris sinf nusxasi hech qachon bazaviy sinf nusxasiga teng bo'lmaydi (Hibernate proxy bilan muammo shu yerdan keladi). `instanceof` esa Liskov ni saqlaydi, lekin voris sinf yangi maydon qo'shsa simmetriklik buziladi.

Amaliy yechim: **tenglik kerak bo'lgan sinflarni `final` qilish** yoki `record` ishlatish. Vorislik va qiymat tengligi birga yashamaydi; kerak bo'lsa kompozitsiya ishlatiladi (17.9).

```java
// yaxshi: final sinf - dilemma yo'q
public final class Money { ... }

// yaxshi: record - final va shartnomaga mos
public record Money(BigDecimal amount, Currency currency) { }

// JPA entiteti uchun (proxy sababli instanceof kerak, identifikator bo'yicha tenglik)
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Payment other)) return false;
    return id != null && id.equals(other.id);     // 28.1
}

@Override
public int hashCode() {
    return getClass().hashCode();   // id o'zgarishi hash ni buzmasligi uchun
}
```

### 15.5 Entitet va value object tengligi farqi

Ikki xil tenglik bor va ularni aralashtirish eng ko'p uchraydigan domen xatosi. **Value object** tengligi qiymat bo'yicha: ikki `Money(1000, UZS)` bir xil. **Entitet** tengligi identifikator bo'yicha: ikki `Customer` bir xil `id` bilan teng, hatto ismlari farq qilsa ham.

| Jihat | Value object | Entitet |
|---|---|---|
| Tenglik | barcha maydonlar | faqat identifikator |
| O'zgaruvchanlik | o'zgarmas | o'zgaradi |
| `hashCode` | maydonlardan | `getClass()` yoki barqaror id |
| Java shakli | `record`, `final class` | `@Entity` sinf |
| Misol | `Money`, `Sku`, `DateRange` | `Order`, `Customer` |

### 15.6 `compareTo` shartnomasi va `equals` bilan izchillik

`Comparable` shartnomasi `equals` dan qat'iyroq: antisimmetriklik (`sgn(x.compareTo(y)) == -sgn(y.compareTo(x))`), tranzitivlik, va izchillik (`x.compareTo(y) == 0` bo'lsa, barcha `z` uchun natija bir xil).

Qo'shimcha **kuchli tavsiya**: `(x.compareTo(y) == 0)` va `x.equals(y)` bir xil natija berishi kerak. Buzilsa, `TreeSet` va `TreeMap` boshqacha ishlaydi: `BigDecimal("1.0")` va `BigDecimal("1.00")` `compareTo` bo'yicha teng, `equals` bo'yicha emas, shuning uchun `HashSet` da ikkita element, `TreeSet` da bitta bo'ladi (20.2).

```java
// yaxshi: Comparator.comparing bilan xavfsiz qurish, qo'lda hisob yo'q
public record SettlementKey(LocalDate date, String bankCode, long sequence)
        implements Comparable<SettlementKey> {

    private static final Comparator<SettlementKey> ORDER =
            Comparator.comparing(SettlementKey::date)
                    .thenComparing(SettlementKey::bankCode)
                    .thenComparingLong(SettlementKey::sequence);

    @Override
    public int compareTo(SettlementKey other) {
        return ORDER.compare(this, other);
    }
}
```

Qo'lda `a - b` yozmaslik kerak: butun son to'lib ketishi tartibni teskari aylantiradi (20.3).

### 15.7 `toString`: foydali, xavfsiz, mantiqda ishlatilmaydigan

`toString` log va debug uchun yoziladi, shuning uchun uch talab bor. Birinchi, foydali bo'lishi: sinf nomi va kalit maydonlar. Ikkinchi, xavfsiz bo'lishi: parol, token, karta raqami, shaxsiy ma'lumot chiqmasligi (29.8). Uchinchi, mantiqda ishlatilmasligi: `toString` natijasini parslash yoki solishtirish shartnomaga bog'lanish.

```java
// yomon: sezgir ma'lumot log'ga chiqadi
@Override public String toString() {
    return "Card{number=" + number + ", cvv=" + cvv + "}";
}

// yaxshi: maskalangan, foydali
@Override public String toString() {
    return "Card{last4=%s, expiry=%s}".formatted(number.last4(), expiry);
}
```

JPA entitetida `toString` ichida lazy assotsiatsiyani chaqirish `LazyInitializationException` yoki kutilmagan so'rov beradi; shuning uchun entitet `toString` ida faqat skalyar maydonlar bo'lishi kerak (28.1).

### 15.8 `clone` dan voz kechish va nusxa konstruktori

`Cloneable` interfeysi buzilgan dizayn: u metod e'lon qilmaydi, `Object.clone` `protected`, chuqur nusxa qo'lda yozilishi kerak va `final` maydonlar bilan ishlamaydi. Yechim: `clone` ni umuman yozmaslik.

```java
// yomon
public class Order implements Cloneable {
    @Override public Order clone() throws CloneNotSupportedException { ... }
}

// yaxshi: nusxa konstruktori yoki statik fabrika
public final class Order {
    public Order(Order source) { ... }
    public static Order copyOf(Order source) { ... }
}

// eng yaxshi: o'zgarmas obyekt - nusxa umuman kerak emas (16-bob)
public record Money(BigDecimal amount, Currency currency) { }
```

### 15.9 O'zgaradigan kalit va `HashMap` dagi yo'qolgan yozuv

`HashMap` kaliti sifatida ishlatilgan obyekt `put` dan keyin o'zgarsa, uning hash kodi o'zgaradi va yozuv boshqa bucket da qoladi: `get` uni topolmaydi, `containsKey` `false` qaytaradi, lekin `size()` hali ham 1. Bu xato `equals`/`hashCode` izchillik qoidasining (15.1) buzilishi.

```java
// yomon: kalit o'zgaradi
Map<MutableSku, Integer> stock = new HashMap<>();
MutableSku sku = new MutableSku("A-1");
stock.put(sku, 10);
sku.setCode("A-2");          // hash o'zgardi
stock.get(sku);              // null! yozuv yo'qoldi

// yaxshi: kalit o'zgarmas
record Sku(String code) { }
Map<Sku, Integer> stock = new HashMap<>();
```

Qoida: `Map` kaliti va `Set` elementi har doim o'zgarmas bo'lishi kerak. JPA entitetini kalit sifatida ishlatish ham xavfli, chunki `id` `persist` dan keyin tayinlanadi.

### 15.10 `Comparator` ni toza qurish

`Comparator` ni qo'lda yozish xato manbasi; `Comparator.comparing` zanjiri esa o'qiladi va xatosiz.

```java
// yomon: qo'lda, teskari tartib va null ishlovi aralashgan
orders.sort((a, b) -> {
    int c = b.getCreatedAt().compareTo(a.getCreatedAt());
    if (c != 0) return c;
    return a.getId().intValue() - b.getId().intValue();   // to'lib ketish xavfi
});

// yaxshi: deklarativ, o'qiladi, null siyosati oshkor
orders.sort(comparing(Order::createdAt).reversed()
        .thenComparing(Order::id)
        .thenComparing(Order::customerName, nullsLast(naturalOrder())));
```

Ikkinchi qoida: `Comparator` ni `static final` maydonga chiqarish — har bir chaqiruvda yangi obyekt yaratilmaydi va nom tartibni tushuntiradi (`NEWEST_FIRST`).

### 15.11 Amalda qo'llash

- [ ] `equals` yozilgan barcha sinflarda `hashCode` ham borligini Checkstyle `EqualsHashCode` bilan majburiy qiling.
- [ ] Value object larni `record` ga o'tkazib, qo'lda yozilgan `equals`/`hashCode` ni o'chiring.
- [ ] Tenglik kerak bo'lgan sinflarni `final` qilib, vorislik ostidagi simmetriklik muammosini yo'qoting.
- [ ] JPA entitetlarida tenglikni identifikator bo'yicha yozib, `hashCode` ni barqaror qiling (28.1).
- [ ] `Comparable` amalga oshirilgan sinflarda `compareTo` va `equals` izchilligini test bilan tekshiring.
- [ ] Barcha `toString` larni ko'rib, sezgir maydonlarni maskalang va lazy assotsiatsiyalarni olib tashlang.
- [ ] `Cloneable` ishlatilgan joylarni nusxa konstruktori yoki o'zgarmas turga o'tkazing.
- [ ] `Map` kaliti va `Set` elementi sifatida ishlatilgan o'zgaradigan turlarni topib, o'zgarmas turga almashtiring.
## 16. O'zgarmaslik va holat boshqaruvi kod darajasida (Immutability in Code)

Holatni kamaytirish murakkablikni boshqarish vositasi sifatida arxitektor hujjatida (6.3) ko'rib chiqilgan. Bu bobda shu qarorning kod darajasidagi mexanikasi: `final` ning haqiqiy kuchi, chuqur va sayoz o'zgarmaslik, o'zgarmas to'plamlar, nusxalab o'zgartirish, va setter larni yo'qotish yo'li.

### 16.1 `final` maydon, `final` sinf va haqiqiy o'zgarmaslik

`final` maydon faqat **havolani** qotiradi, obyektni emas. `private final List<Order> orders` maydoniga yangi ro'yxat tayinlab bo'lmaydi, lekin `orders.add(...)` ishlaydi. Shu sababli haqiqiy o'zgarmaslik uch shartni talab qiladi.

| Shart | Nega kerak |
|---|---|
| Barcha maydonlar `final` | qayta tayinlashni to'sadi |
| Maydon turlari ham o'zgarmas | ichki obyekt o'zgarmasin |
| Sinf `final` (yoki konstruktor `private`) | voris sinf o'zgaruvchanlik qo'shmasin |
| Setter yo'q | oshkor o'zgartirish yo'li yopiladi |
| To'plamlar nusxalanadi va o'zgartirilmas | 14.7 |
| `this` chiqib ketmaydi | 14.10 |

```java
// yomon: final bor, lekin obyekt o'zgaradi
public final class Order {
    private final List<OrderItem> items = new ArrayList<>();
    public List<OrderItem> items() { return items; }   // tashqi kod add qiladi
}

// yaxshi: haqiqiy o'zgarmaslik
public final class Order {

    private final List<OrderItem> items;

    public Order(List<OrderItem> items) {
        this.items = List.copyOf(items);     // nusxa + o'zgartirilmas
    }

    public List<OrderItem> items() { return items; }   // o'zgartirilmas, nusxa kerak emas
}
```

### 16.2 Chuqur va sayoz o'zgarmaslik

Sayoz o'zgarmaslik — obyektning o'zi o'zgarmas, lekin ichidagi obyektlar o'zgaradi. Bu holat eng xavfli, chunki kod o'zgarmas ko'rinadi va dasturchi himoyaga ishonadi.

```java
// yomon: record o'zgarmas ko'rinadi, lekin ichidagi Date o'zgaradi
public record Shipment(String trackingNumber, Date dispatchedAt) { }
shipment.dispatchedAt().setTime(0);    // o'zgardi!

// yaxshi: ichki turlar ham o'zgarmas
public record Shipment(TrackingNumber trackingNumber, Instant dispatchedAt) { }
```

Qoida: o'zgarmas sinf ichida faqat o'zgarmas turlar bo'lishi kerak — `String`, `Instant`, `LocalDate`, `BigDecimal`, `record`, enum, `List.of`. `Date`, `Calendar`, massiv, `ArrayList` esa chegarada nusxalanadi.

### 16.3 O'zgarmas to'plamlar: `List.of`, `unmodifiable*`, nusxa

Java da to'plam o'zgarmasligining uch darajasi bor va ularni ajratish muhim.

| Shakl | Xatti-harakat | `null` element |
|---|---|---|
| `List.of(a, b)` | haqiqiy o'zgarmas, yangi obyekt | taqiqlangan |
| `List.copyOf(src)` | manbadan nusxa, o'zgarmas | taqiqlangan |
| `Collections.unmodifiableList(src)` | **ko'rinish**: manba o'zgarsa o'zgaradi | ruxsat |
| `new ArrayList<>(src)` | nusxa, lekin o'zgaradi | ruxsat |
| `Arrays.asList(a, b)` | fiksirlangan hajm, `set` ishlaydi | ruxsat |
| `stream().toList()` | o'zgarmas | ruxsat |
| `Collectors.toList()` | kafolat yo'q | ruxsat |

Eng ko'p uchraydigan tuzoq — `Collections.unmodifiableList` ni haqiqiy o'zgarmaslik deb o'ylash: u faqat **ko'rinish** beradi va manba o'zgarsa ko'rinish ham o'zgaradi.

```java
List<String> source = new ArrayList<>(List.of("a"));
List<String> view = Collections.unmodifiableList(source);
source.add("b");
view.size();   // 2 - "o'zgarmas" ko'rinish o'zgardi
```

### 16.4 `with` uslubidagi o'zgartiruvchilar

O'zgarmas obyektni "o'zgartirish" — yangi nusxa qaytarish. Konvensiya: metod nomi `with`, `plus`, `minus` yoki domen fe'li bilan boshlanadi va `this` ni o'zgartirmaydi.

```java
public record Money(BigDecimal amount, Currency currency) {

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money withScale(int scale) {
        return new Money(amount.setScale(scale, RoundingMode.HALF_UP), currency);
    }
}

// Domen obyektida: har bir o'tish yangi holat qaytaradi
public record Order(OrderId id, OrderStatus status, List<OrderItem> items) {

    public Order confirmed() {
        if (status != DRAFT) throw new IllegalStateException("faqat DRAFT tasdiqlanadi");
        return new Order(id, CONFIRMED, items);
    }
}
```

Maydon soni ko'p bo'lsa, har bir `with` metodi uzun bo'lib ketadi; bunda builder dan nusxa olish (`toBuilder()`) ishlatiladi.

### 16.5 Builder: validatsiya va majburiy maydonlar

Builder pattern ning o'zi patternlar hujjatida; bu yerda clean code tomoni: validatsiya **qayerda** turishi. Eng ko'p uchraydigan xato — validatsiyani builder metodlarida qilish va `build()` da unutish, natijada yarim to'ldirilgan obyekt yaratiladi.

```java
public final class ReservationRequest {

    private final CustomerId customer;
    private final Sku sku;
    private final Quantity quantity;

    private ReservationRequest(Builder builder) {
        // Validatsiya bir joyda: build() yo'li orqali
        this.customer = Objects.requireNonNull(builder.customer, "customer");
        this.sku = Objects.requireNonNull(builder.sku, "sku");
        this.quantity = Objects.requireNonNull(builder.quantity, "quantity");
        if (quantity.isZeroOrLess()) {
            throw new IllegalArgumentException("quantity musbat bo'lishi kerak: " + quantity);
        }
    }

    public static Builder builder() { return new Builder(); }

    public static final class Builder {
        private CustomerId customer;
        private Sku sku;
        private Quantity quantity;

        public Builder customer(CustomerId customer) { this.customer = customer; return this; }
        public Builder sku(Sku sku) { this.sku = sku; return this; }
        public Builder quantity(Quantity quantity) { this.quantity = quantity; return this; }

        public ReservationRequest build() { return new ReservationRequest(this); }
    }
}
```

Agar majburiy maydonlar kam bo'lsa, builder o'rniga konstruktor yoki `record` yaxshiroq: builder faqat ixtiyoriy maydonlar ko'p bo'lganda haqli.

### 16.6 Mutatsiyani bir joyga to'plash

Butun tizimni o'zgarmas qilish amalda mumkin emas: ma'lumotlar bazasi, kesh, hisoblagich o'zgaradi. To'g'ri strategiya — o'zgarishni **chegaraga** siqish: hisob va qoidalar o'zgarmas obyektlarda, o'zgarish esa bir-ikki aniq joyda.

```java
// yaxshi: hisob sof, o'zgarish bitta joyda
public final class SettlementBatch {

    // Sof hisob: kirish o'zgarmas, chiqish yangi obyekt
    public SettlementPlan planFor(List<Payment> payments) {
        return new SettlementPlan(payments.stream().filter(Payment::isSettleable).toList());
    }
}

@Service
class SettlementRunner {

    // O'zgarish faqat shu yerda: tranzaksiya chegarasida
    @Transactional
    void apply(SettlementPlan plan) {
        paymentRepository.markSettled(plan.paymentIds());
    }
}
```

### 16.7 Setter ni olib tashlash yo'li

Mavjud kod bazasida setter lar ko'p bo'lsa, ularni bir kunda olib tashlab bo'lmaydi. Ishlaydigan ketma-ketlik: setter ni domen fe'liga aylantirish, keyin o'zgarmas nusxaga o'tish.

```java
// 1-qadam: setter domen fe'liga aylanadi (ma'no paydo bo'ladi, imzo torayadi)
// oldin: order.setStatus(SHIPPED);
public void markShipped(Instant shippedAt) {
    if (status != CONFIRMED) throw new IllegalStateException(...);
    this.status = SHIPPED;
    this.shippedAt = shippedAt;
}

// 2-qadam: o'zgartirish yangi obyekt qaytaradi
public Order shipped(Instant shippedAt) { ... }

// 3-qadam: entitetda saqlanadigan holat uchun o'zgarish qoladi,
// lekin faqat domen fe'llari orqali: oshkor setter yo'q
```

### 16.8 Vaqtinchalik maydon va uni yo'qotish

Vaqtinchalik maydon (temporary field) — faqat ma'lum metod ishlaganda to'ldiriladigan, qolgan vaqt `null` turadigan maydon. U o'quvchini chalg'itadi: maydonni ko'rgan odam uning har doim to'ldirilganini o'ylaydi.

```java
// yomon: ikki maydon faqat calculate() ichida ishlatiladi
public class PriceCalculator {
    private Money subtotal;      // faqat calculate() davomida to'ldiriladi
    private Money discount;      // qolgan vaqt null

    public Money calculate(Order order) {
        subtotal = subtotalOf(order);
        discount = discountFor(order, subtotal);
        return subtotal.minus(discount);
    }
}

// yaxshi: vaqtinchalik holat metod ichida yoki alohida obyektda
public final class PriceCalculator {

    public Money calculate(Order order) {
        Money subtotal = subtotalOf(order);
        Money discount = discountFor(order, subtotal);
        return subtotal.minus(discount);
    }
}
```

### 16.9 Global va statik o'zgaradigan holat

Statik o'zgaradigan maydon uch muammoni bir vaqtda keltiradi: testlar bir-biriga ta'sir qiladi (tartibga bog'liq yiqilish), thread xavfi paydo bo'ladi, va bog'liqlik kodda ko'rinmaydi.

```java
// yomon: global holat
public class CurrentUser {
    public static String username;      // kim o'rnatdi, kim o'chirdi - ko'rinmaydi
}

// yaxshi: kontekst oshkor uzatiladi yoki framework mexanizmi ishlatiladi
public record RequestContext(UserId user, TraceId trace) { }
// yoki Spring Security: SecurityContextHolder (thread-local, framework boshqaradi)
```

`ThreadLocal` ham global holatning shakli va u faqat framework darajasida (MDC, tranzaksiya konteksti) haqli; biznes kodida uzatilgan parametr har doim afzal. Ishlatilsa, `finally` da tozalash majburiy (29.7).

### 16.10 Amalda qo'llash

- [ ] Barcha maydonlarni `final` qilib, qolganlarini (o'zgarishi kerak bo'lganlarini) ro'yxatlab sababini yozib qo'ying.
- [ ] O'zgarmas deb hisoblangan sinflar ichida `Date`, massiv va `ArrayList` borligini tekshirib, o'zgarmas turga almashtiring.
- [ ] `Collections.unmodifiableList` ishlatilgan joylarni `List.copyOf` ga o'tkazib, ko'rinish tuzog'ini yo'qoting.
- [ ] Domen obyektlaridagi oshkor setter larni domen fe'llariga aylantiring (16.7 dagi uch qadam).
- [ ] Faqat bir metod davomida to'ldiriladigan maydonlarni mahalliy o'zgaruvchiga ko'chiring.
- [ ] Statik o'zgaradigan maydonlarni topib (`static` + `final` emas), kontekst parametriga yoki framework mexanizmiga o'tkazing.
- [ ] `ThreadLocal` ishlatilgan joylarda `finally` da tozalash borligini tekshiring.
- [ ] Yangi value object lar uchun `record` ni standart tanlov qilib, uni jamoa kelishuviga yozib qo'ying.
## 17. Vorislik, kompozitsiya va polimorfizm mexanikasi (Inheritance Mechanics)

"Vorislikdan ustun kompozitsiya" printsipi patternlar hujjatida (26.17) berilgan. Bu bobda vorislik **ishlatilganda** uni to'g'ri bajarish mexanikasi: vorislik uchun dizayn, konstruktor tuzog'i, `protected` muammosi, va vorislikdan kompozitsiyaga o'tish yo'li.

### 17.1 Vorislik uchun dizayn qilish yoki `final` qilish

Sinf uch holatdan birida bo'lishi kerak: vorislik uchun mo'ljallangan va hujjatlashtirilgan, `final`, yoki interfeys. "Vorislik mumkin, lekin o'ylanmagan" to'rtinchi holat — xato manbasi, chunki voris sinf bazaviy sinfning ichki qoidalarini bilmaydi va ularni buzadi.

Shu sababli amaliy standart: **sinf `final` bo'lishi standart holat**, vorislik esa ongli qaror. Spring kontekstida istisno bor: `@Configuration` sinflari va CGLIB proxy qilinadigan beanlar `final` bo'lmaydi (26.1).

```java
// yaxshi: standart holat
public final class SettlementService { ... }

// yaxshi: vorislik uchun ataylab ochilgan va hujjatlashtirilgan
/**
 * Voris sinf uchun: {@link #validate(SettlementRow)} ni override qilish mumkin.
 * Bu metod {@link #importFile(Path)} ichidan har bir qator uchun chaqiriladi
 * va istisno tashlamasligi kerak - yaroqsiz qator {@code false} bilan belgilanadi.
 * Konstruktor ichidan override qilinadigan metod chaqirilmaydi.
 */
public abstract class AbstractSettlementImporter { ... }
```

### 17.2 Konstruktorda override qilinadigan metodni chaqirish

Bu Java dagi eng nozik vorislik xatosi. Bazaviy sinf konstruktori override qilinadigan metodni chaqirsa, u **voris sinf maydonlari hali tayinlanmaganda** ishga tushadi va `null` yoki nol qiymat ko'radi.

```java
// yomon: natija NullPointerException yoki 0
public class Importer {
    public Importer() {
        configure();                 // voris versiyasi chaqiriladi
    }
    protected void configure() { }
}

public class CsvImporter extends Importer {
    private final char delimiter = ';';     // hali tayinlanmagan!
    @Override protected void configure() {
        System.out.println(delimiter);       // 0 (nol belgi) chiqadi
    }
}

// yaxshi: sozlash konstruktordan tashqarida, yoki shablon parametr bilan
public class Importer {
    private final ImportSettings settings;
    protected Importer(ImportSettings settings) {
        this.settings = Objects.requireNonNull(settings);
    }
}
```

Xuddi shu qoida `clone` va `readObject` ga tegishli: ikkisi ham konstruktor rolini bajaradi.

### 17.3 `protected` maydon va buzilgan inkapsulyatsiya

`protected` maydon voris sinflarga ichki holatni to'g'ridan-to'g'ri o'zgartirish imkonini beradi, ya'ni bazaviy sinf o'z invariantini himoya qila olmaydi. Natijada bazaviy sinfni refaktoring qilish imkonsiz bo'lib qoladi: u maydonlarni o'zgartirsa, barcha voris sinflar buziladi.

```java
// yomon: voris sinf holatni to'g'ridan-to'g'ri buzadi
public abstract class AbstractBatch {
    protected List<Row> rows = new ArrayList<>();
    protected int processed;
}

// yaxshi: ichki holat private, voris sinfga protected metod berilgan
public abstract class AbstractBatch {

    private final List<Row> rows = new ArrayList<>();
    private int processed;

    protected final void recordProcessed(Row row) {    // final: shartnoma buzilmaydi
        rows.add(row);
        processed++;
    }

    protected final int processedCount() { return processed; }
}
```

Qoida: `protected` maydon bo'lmaydi; `protected` metod bo'lishi mumkin va u `final` bo'lishi afzal.

### 17.4 `super` chaqiruvi va uni unutish

Agar override qilingan metod `super.method()` ni chaqirishi **shart** bo'lsa, bu yashirin shartnoma va u buziladi: kimdir chaqirmay qo'yadi va xato uzoqda chiqadi.

To'g'ri yechim — shablon metod (template method) bilan tuzilishni teskari aylantirish: bazaviy sinf `final` metodda tartibni ushlaydi va voris sinfga faqat bo'sh joyni beradi.

```java
// yomon: super ni chaqirish majburiyati izohda
public void process(Row row) {
    super.process(row);     // voris buni unutsa, audit yozilmaydi
    doWork(row);
}

// yaxshi: tartib bazaviy sinfda, voris faqat bo'shliqni to'ldiradi
public abstract class AbstractProcessor {

    public final void process(Row row) {     // final: tartib buzilmaydi
        audit(row);
        handle(row);                         // voris shu metodni yozadi
        markDone(row);
    }

    protected abstract void handle(Row row);
}
```

### 17.5 Bazaviy sinfning voris sinfga bog'liqligi

Bazaviy sinf voris sinf nomini bilsa (`if (this instanceof CsvImporter)`), ierarxiya teskari aylangan: eng barqaror bo'lishi kerak bo'lgan sinf eng o'zgaruvchan sinfga bog'langan. Har bir yangi voris bazaviy sinfni o'zgartirishni talab qiladi.

```java
// yomon: bazaviy sinf vorislarini sanaydi
protected String separator() {
    if (this instanceof CsvImporter) return ",";
    if (this instanceof TsvImporter) return "\t";
    return ";";
}

// yaxshi: har bir voris o'zini aytadi
protected abstract String separator();
```

### 17.6 Rad etilgan meros va interfeysni bo'lish

Rad etilgan meros (refused bequest) — voris sinf bazaviy sinfdan olgan metodlarning bir qismini ishlatmaydi yoki `UnsupportedOperationException` tashlaydi. Bu Liskov printsipining buzilishi va interfeys juda keng ekanining belgisi.

```java
// yomon: voris sinf merosni rad etadi
public class ReadOnlyOrderRepository extends JpaOrderRepository {
    @Override public Order save(Order order) {
        throw new UnsupportedOperationException("faqat o'qish");
    }
}

// yaxshi: interfeys bo'lingan (Interface Segregation)
public interface OrderFinder { Optional<Order> findById(OrderId id); }
public interface OrderWriter { Order save(Order order); }

public class JpaOrderRepository implements OrderFinder, OrderWriter { ... }
public class CachedOrderFinder implements OrderFinder { ... }
```

### 17.7 Abstrakt sinf va interfeys tanlovi, `default` metodlar

Tanlov mezoni oddiy: **holat** kerak bo'lsa abstrakt sinf, faqat shartnoma kerak bo'lsa interfeys. Java da bir sinf bitta bazaviy sinfdan voris oladi, lekin ko'p interfeys amalga oshiradi, shuning uchun interfeys moslashuvchanroq.

`default` metodlar interfeysga xatti-harakat qo'shish imkonini beradi, lekin ularni ehtiyotkorlik bilan ishlatish kerak: ular holatga kira olmaydi, va ikki interfeys bir xil `default` metod bersa konflikt bo'ladi.

| Ehtiyoj | Tanlov |
|---|---|
| Faqat shartnoma | interfeys |
| Umumiy holat kerak | abstrakt sinf |
| Mavjud interfeysga metod qo'shish | `default` metod (orqaga moslik) |
| Qulaylik metodi (boshqalardan hisoblanadi) | `default` metod |
| Ko'p rolni birlashtirish | bir nechta interfeys |
| Konstanta to'plami | enum yoki `final` sinf, interfeys emas (17.8) |
| Shablon tartibi | abstrakt sinf + `final` shablon metod |

### 17.8 Konstantalarni interfeysdan voris olish

Konstantalarni interfeysga qo'yib, sinflarni shu interfeysdan voris qilish (constant interface) qoldirilgan amaliyot. U konstantalarni sinfning public API siga chiqaradi, ularning manbasini yashiradi, va nomlar konflikt qiladi.

```java
// yomon: constant interface
public interface Limits {
    int MAX_RETRY = 3;
    Duration TIMEOUT = Duration.ofSeconds(30);
}
public class SettlementService implements Limits { ... }   // MAX_RETRY public bo'lib qoldi

// yaxshi: konstanta tegishli joyda yashaydi
public final class SettlementService {
    private static final int MAX_RETRY = 3;
}

// yaxshi: umumiy konstantalar - enum yoki final sinf, static import bilan
public enum RetryLimit { ... }
```

### 17.9 Delegatsiya bilan vorislikni almashtirish

Vorislikdan chiqish yo'li — delegatsiya: voris sinf bazaviy sinfni **maydon** sifatida saqlaydi va kerakli metodlarni o'ziga o'tkazadi. Shunda bazaviy sinfning butun API si meros bo'lib o'tmaydi va shartnoma buzilmaydi.

```java
// yomon: HashMap dan voris olish - butun API meros bo'ladi, invariant himoyalanmaydi
public class StockLevels extends HashMap<Sku, Integer> { }
stockLevels.put(sku, -5);        // manfiy qoldiq - tekshirilmadi

// yaxshi: delegatsiya - faqat kerakli amallar oshkor, invariant himoyalangan
public final class StockLevels {

    private final Map<Sku, Quantity> levels = new HashMap<>();

    public void set(Sku sku, Quantity quantity) {
        if (quantity.isNegative()) {
            throw new IllegalArgumentException("qoldiq manfiy bo'lmaydi: " + sku);
        }
        levels.put(sku, quantity);
    }

    public Quantity of(Sku sku) { return levels.getOrDefault(sku, Quantity.ZERO); }
}
```

O'tish tartibi: maydon qo'shish → `extends` ni olib tashlash → kompilyator ko'rsatgan metodlarni delegatsiyaga aylantirish → keraksizlarini o'chirish (37-bob, Replace Superclass with Delegate).

### 17.10 Amalda qo'llash

- [ ] Vorislik uchun mo'ljallanmagan barcha sinflarni `final` qiling (Spring proxy talab qilgan joylardan tashqari).
- [ ] Konstruktordan chaqirilayotgan override qilinadigan metodlarni topib, sozlashni konstruktordan chiqaring.
- [ ] Barcha `protected` maydonlarni `private` ga aylantirib, voris sinfga `protected final` metod bering.
- [ ] `super.method()` chaqirilishi shart bo'lgan joylarni `final` shablon metodga aylantiring.
- [ ] Bazaviy sinflarda `instanceof` orqali voris sinf tekshiruvlarini abstrakt metodga almashtiring.
- [ ] `UnsupportedOperationException` tashlaydigan override larni topib, interfeysni bo'ling.
- [ ] Constant interface larni yo'qotib, konstantalarni tegishli sinfga yoki enum ga ko'chiring.
- [ ] `ArrayList`, `HashMap` kabi to'plamlardan voris olgan sinflarni delegatsiyaga o'tkazing.
# VI. Xato bilan ishlash

## 18. Xato bilan ishlash qoidalari (Error Handling Rules)

Istisno dizayni, tekshiriladigan va tekshirilmaydigan istisnolar tanlovi arxitektor hujjatida (13.7), istisno orqali muloqot esa 4.6 da ko'rilgan. Bu bobda qolgan qoidalar: xato kodidan voz kechish, `try` blokini ajratish, normal oqimni aniqlash, `null` siyosati, va chegarada tez to'xtash.

### 18.1 Xato kodi emas, istisno

Xato kodini qaytarish chaqiruvchini darhol tekshirishga majbur qiladi va tekshiruv unutilsa, xato jim yo'qoladi. Bundan tashqari, xato kodi asosiy mantiqni shart bilan to'ldiradi va kodni chuqurlashtiradi.

```java
// yomon: xato kodi - tekshiruv unutilsa, xato yo'qoladi
public int deletePage(Page page) {
    if (page == null) return ERROR_NULL_PAGE;
    if (!registry.contains(page)) return ERROR_NOT_FOUND;
    registry.delete(page);
    return OK;
}
// chaqiruvchi:
if (deletePage(page) == OK) {
    if (registry.deleteReference(page.name) == OK) { ... }   // chuqurlashadi
}

// yaxshi: istisno - normal oqim toza qoladi
public void deletePage(Page page) {
    registry.delete(page);         // topilmasa PageNotFoundException tashlaydi
    references.delete(page.name());
}
```

Bitta istisno: **kutilayotgan** yo'qlik xato emas. `findById` topilmasa `Optional.empty()` qaytaradi, istisno tashlamaydi (2.11 dagi nomlash taqsimoti).

### 18.2 `try-catch-finally` ni birinchi yozish

Xato bilan ishlashni keyin qo'shish deyarli har doim yarim ishlaydi: resurslar yopilmagan, holat yarim o'zgargan bo'lib qoladi. To'g'ri tartib — `try` blokini birinchi yozish va u "qolgan kod uchun qamrov" yaratadi.

TDD kontekstida bu aniq qadamga aylanadi: oldin istisno kutadigan test yozish, keyin `try/catch` qo'shish, keyin ichini to'ldirish (31-bob).

```java
// Birinchi qadam: xato yo'lini test bilan belgilash
@Test
void throwsWhenFileMissing() {
    assertThatThrownBy(() -> importer.importFile(Path.of("yo'q.csv")))
            .isInstanceOf(SettlementFileUnavailableException.class);
}

// Ikkinchi qadam: try/catch qamrovi, keyin ichi
public void importFile(Path file) {
    try (var lines = Files.lines(file, UTF_8)) {
        apply(parse(lines));
    } catch (NoSuchFileException e) {
        throw new SettlementFileUnavailableException(file, e);
    } catch (IOException e) {
        throw new SettlementFileUnreadableException(file, e);
    }
}
```

### 18.3 Istisnoni chaqiruvchi ehtiyojiga qarab aniqlash

Istisno sinflarini **manba** bo'yicha emas, **chaqiruvchi nima qilishi** bo'yicha ajratish kerak. Agar chaqiruvchi beshta istisno turini bir xil qayta ishlasa, beshta tur kerak emas.

```java
// yomon: chaqiruvchi uchta istisnoni bir xil qayta ishlaydi
try {
    port.open();
} catch (DeviceResponseException e) {
    log.error("qurilma javobi", e); throw new PortUnavailable(e);
} catch (ATM1212UnlockedException e) {
    log.error("qulf", e); throw new PortUnavailable(e);
} catch (GMXError e) {
    log.error("gmx", e); throw new PortUnavailable(e);
}

// yaxshi: past darajali API wrapper bilan o'ralgan, bitta ma'noli istisno
try {
    port.open();          // LocalPort ichida past darajali istisnolar o'raladi
} catch (PortDeviceFailure e) {
    log.error("port ochilmadi: {}", port.name(), e);
    throw e;
}
```

Shu uslub "o'rash" (wrapping) deb ataladi va u uchinchi tomon kutubxonasiga bog'liqlikni ham kamaytiradi: kutubxona almashtirilsa, faqat wrapper o'zgaradi.

### 18.4 `try` blokini alohida funksiyaga chiqarish

`try/catch` bloki kodni chalkashtiradi, chunki u normal oqimni ham, xato oqimini ham bir funksiyada saqlaydi. Yechim: `try` blokining ichini alohida funksiyaga chiqarish, shunda tashqi funksiya faqat xato bilan ishlashni ko'rsatadi.

```java
// yaxshi: ikki funksiya, ikki javobgarlik
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    page.delete();
    registry.deleteReference(page.name());
    configKeys.deleteKey(page.name().makeKey());
}

private void logError(Exception e) {
    log.error("sahifani o'chirishda xato", e);
}
```

### 18.5 Xato bilan ishlash ham bitta ish

Agar funksiyada `try` kalit so'zi bo'lsa, u `try` dan boshlanishi va `catch`/`finally` dan keyin tugashi kerak. Ya'ni xato bilan ishlash — funksiyaning **bitta** ishi va unga biznes mantiqi qo'shilmaydi (4.2 ning tatbiqi).

```java
// yomon: try bloki ichida ham biznes mantiqi, ham xato ishlovi
public void settle(Payment payment) {
    Money fee = feeFor(payment);              // try dan tashqarida biznes mantiqi
    try {
        gateway.settle(payment, fee);
        payment.markSettled();
        auditLog.record(payment);
    } catch (GatewayTimeout e) {
        payment.markPending();
        retryQueue.add(payment);
    }
}

// yaxshi: xato ishlovi alohida, normal oqim alohida
public void settle(Payment payment) {
    try {
        settleNow(payment);
    } catch (GatewayTimeout e) {
        scheduleRetry(payment, e);
    }
}
```

### 18.6 Normal oqimni aniqlash va maxsus holat obyekti

Ba'zan istisno umuman kerak emas: "yo'q" holati normal va uni obyekt bilan ifodalash mumkin (Special Case pattern). Shunda chaqiruvchida `try/catch` ham, `null` tekshiruvi ham qolmaydi.

```java
// yomon: istisno oqim boshqarish uchun ishlatilgan
try {
    MealExpenses expenses = expenseReport.getMeals(employeeId);
    total += expenses.getTotal();
} catch (MealExpensesNotFound e) {
    total += getMealPerDiem();      // "yo'q" holati - bu xato emas
}

// yaxshi: maxsus holat obyekti standart xatti-harakatni o'zida ushlaydi
MealExpenses expenses = expenseReport.getMeals(employeeId);   // har doim obyekt qaytadi
total += expenses.getTotal();

public final class PerDiemMealExpenses implements MealExpenses {
    @Override public Money getTotal() { return PER_DIEM; }
}
```

### 18.7 `null` qaytarmaslik va `null` uzatmaslik

`null` qaytarish chaqiruvchiga ish yuklaydi va bir joyda unutilsa `NullPointerException` beradi. `null` uzatish esa undan yomoni: metod ichida uni tekshirishning ishonchli usuli yo'q.

| Holat | `null` o'rniga |
|---|---|
| Topilmasligi mumkin | `Optional<T>` |
| Bo'sh to'plam | `List.of()` (18.8) |
| Standart xatti-harakat | maxsus holat obyekti (18.6) |
| Haqiqiy xato | istisno |
| Ixtiyoriy parametr | overload yoki builder (5.9) |
| Ixtiyoriy maydon | `Optional` getter, maydon `null` (24.1 chegarasi) |
| Tashqi ma'lumot (JSON) | validatsiya chegarada |

```java
// yomon
public List<Employee> getEmployees() {
    if (noEmployees) return null;       // chaqiruvchi tekshirishga majbur
}
for (Employee e : getEmployees()) { ... }   // NPE

// yaxshi
public List<Employee> getEmployees() {
    return employees == null ? List.of() : List.copyOf(employees);
}
```

### 18.8 Bo'sh to'plam qaytarish qoidasi

Metod to'plam qaytarsa, u hech qachon `null` qaytarmasligi kerak — bu Java da eng kam bahsli qoidalardan biri. `List.of()` va `Collections.emptyList()` ikkisi ham o'zgarmas va deyarli bepul (umumiy nusxa).

Shu qoidaning `Map`, `Set`, `Stream` va massiv uchun ekvivalentlari: `Map.of()`, `Set.of()`, `Stream.empty()`, `new String[0]`.

### 18.9 Istisnoni oqim boshqarish uchun ishlatmaslik

Istisno **istisnoli** holat uchun. Normal oqimda istisno tashlash uch zarar keltiradi: stack trace yaratish qimmat (issiq yo'lda sezilarli), kod o'qilmaydi, va haqiqiy xatolar shovqin ichida ko'rinmay qoladi.

```java
// yomon: sikl oxirini istisno bilan aniqlash
try {
    int i = 0;
    while (true) {
        total += items[i++].price();
    }
} catch (ArrayIndexOutOfBoundsException e) {
    // sikl tugadi
}

// yaxshi
for (Item item : items) {
    total = total.add(item.price());
}
```

Shu qoidaning amaliy shakli: validatsiya uchun `try { Integer.parseInt(s) } catch` o'rniga oldindan tekshirish yoki `Optional` qaytaradigan parser ishlatish.

### 18.10 Tez to'xtash (fail fast) va chegarada tekshirish

Xato qanchalik manbaga yaqin aniqlansa, uni tuzatish shunchalik arzon. Shu sababli noto'g'ri ma'lumot tizimga kirishi bilan to'xtatilishi kerak, ichkariga tarqalib ketmasligi kerak.

Amalda bu 5.11 dagi validatsiya taqsimoti bilan amalga oshadi: tashqi chegarada format va majburiylik, value object konstruktorida invariant, domen metodida biznes qoidasi. Ichki metodlar esa tekshirmaydi — ular allaqachon to'g'ri ma'lumot oladi.

```java
// Chegarada: format, majburiylik, diapazon
@PostMapping("/refunds")
ResponseEntity<RefundResponse> refund(@Valid @RequestBody RefundRequest request) { ... }

// Value object: invariant - yaroqsiz obyekt tug'ilmaydi
public record Quantity(int value) {
    public Quantity {
        if (value <= 0) throw new IllegalArgumentException("quantity musbat: " + value);
    }
}

// Domen: biznes qoidasi
public void refund(Money amount) {
    if (amount.greaterThan(refundableAmount())) {
        throw new RefundExceedsPaymentException(id, amount, refundableAmount());
    }
}
```

### 18.11 Amalda qo'llash

- [ ] Xato kodi qaytaradigan metodlarni (`int` holat, `boolean` muvaffaqiyat) istisnoga yoki `Optional` ga o'tkazing.
- [ ] To'plam qaytaradigan barcha metodlarda `null` qaytarilmasligini tekshirib, `List.of()` ga o'tkazing.
- [ ] `null` parametr kutadigan public metodlarni overload yoki builder bilan almashtiring.
- [ ] Uchinchi tomon kutubxonasining istisnolarini wrapper ichida o'rab, chaqiruvchi uchun ma'noli turlar bering.
- [ ] `try` bloki ichida biznes mantiqi bor funksiyalarni ikkiga bo'lib, xato ishlovini ajratib bering.
- [ ] Oqim boshqarish uchun istisno ishlatilgan joylarni (`catch (ArrayIndexOutOfBounds)`) oddiy shartga aylantiring.
- [ ] "Yo'q" holati normal bo'lgan joylarni maxsus holat obyekti bilan ifodalab, `catch` bloklarini olib tashlang.
- [ ] Validatsiyani 5.11 taqsimoti bo'yicha chegaraga ko'chirib, ichki metodlardagi takroriy tekshiruvlarni o'chiring.
## 19. Istisno mexanikasi va resurslar (Exception Mechanics and Resources)

Oldingi bobda xato bilan ishlashning qoidalari berildi. Bu bobda Java dagi mexanika: stack trace ni saqlash, tutish tartibi, `finally` tuzoqlari, `try-with-resources`, `InterruptedException`, assertion, va xato xabarining uch xil adresati.

### 19.1 Stack trace ni yo'qotmaslik: wrap va rethrow

Istisnoni qayta tashlashning to'g'ri yo'li — asl istisnoni **sabab** (cause) sifatida uzatish. Buni unutish diagnostikani imkonsiz qiladi: log da yangi istisnoning stack trace i turadi, asl xato qayerda bo'lganini ko'rsatmaydi.

```java
// yomon: sabab yo'qoldi, asl xato qayerda bo'lgani ko'rinmaydi
catch (SQLException e) {
    throw new SettlementException("baza xatosi");
}

// yomon: faqat xabar ko'chirilgan, stack trace yo'q
catch (SQLException e) {
    throw new SettlementException(e.getMessage());
}

// yaxshi: sabab saqlangan, kontekst qo'shilgan
catch (SQLException e) {
    throw new SettlementException(
            "to'lov %s uchun hisob-kitob yozib bo'lmadi".formatted(paymentId), e);
}
```

Agar istisnoni o'zgartirmasdan qayta tashlasangiz, `throw e;` yozing — yangi istisno yaratish stack trace ni almashtiradi.

### 19.2 Ko'p turni tutish va tutish tartibi

`catch` bloklari **xususiydan umumiyga** tartibda yozilishi kerak; teskari tartib kompilyatsiya xatosi beradi (erishilmaydigan blok). Agar bir necha tur bir xil qayta ishlansa, multi-catch ishlatiladi va bu takrorlanishni yo'qotadi.

```java
// yaxshi: multi-catch, takrorlanish yo'q
try {
    gateway.settle(payment);
} catch (SocketTimeoutException | ConnectException e) {
    throw new GatewayUnavailableException(payment.id(), e);
} catch (IOException e) {
    throw new GatewayCommunicationException(payment.id(), e);
}
```

Qoida: `catch (Exception e)` faqat eng tashqi chegarada (controller advice, scheduler, konsumer) haqli. Ichki kodda u aniq istisnolarni yashiradi va `NullPointerException` kabi kodi xatolarini biznes xatosi deb qayta ishlaydi.

### 19.3 `finally` ichidagi `return` va bostirilgan istisno

`finally` blokidagi `return` yoki `throw` asl istisnoni **jimgina yo'qotadi**. Bu Java dagi eng yashirin xato shakllaridan biri: xato bo'lgan, lekin metod normal qaytgan.

```java
// yomon: istisno yo'qoladi, metod 0 qaytaradi
int count() {
    try {
        throw new IllegalStateException("baza yopilgan");
    } finally {
        return 0;          // istisno bostirildi
    }
}

// yaxshi: finally faqat tozalash qiladi, return va throw yo'q
int count() {
    try {
        return repository.count();
    } finally {
        meter.recordCallCompleted();
    }
}
```

Error Prone `Finally` qoidasi va IDE inspeksiyasi shu xatoni topadi; uni CI da bloklash kerak (42.2).

### 19.4 `try-with-resources` va `AutoCloseable`

Qo'lda `finally` ichida yopish uch xatoga olib keladi: yopishni unutish, `close()` ning o'zi istisno tashlashi (asl istisnoni bostiradi), va bir necha resursni noto'g'ri tartibda yopish. `try-with-resources` uchtasini ham hal qiladi: resurslar teskari tartibda yopiladi va `close()` istisnosi **bostirilgan** (suppressed) sifatida saqlanadi.

```java
// yomon: close() istisnosi asl istisnoni yo'qotadi
InputStream in = null;
try {
    in = Files.newInputStream(file);
    return read(in);
} finally {
    if (in != null) in.close();      // bu tashlasa, asl istisno yo'qoladi
}

// yaxshi: avtomatik yopish, bostirilgan istisno saqlanadi
try (InputStream in = Files.newInputStream(file);
     var reader = new BufferedReader(new InputStreamReader(in, UTF_8))) {
    return read(reader);
}
```

O'z resursingiz bo'lsa, `AutoCloseable` ni amalga oshirish kerak va `close()` idempotent bo'lishi lozim. `Stream` ham `AutoCloseable`: `Files.lines`, `Files.walk` va JDBC oqimlari `try-with-resources` ichida bo'lishi shart.

### 19.5 `InterruptedException` ni to'g'ri qayta tiklash

`InterruptedException` tutilganda thread ning uzilish (interrupt) belgisi tozalanadi. Agar u tiklanmasa, yuqoridagi kod uzilganini bilmaydi va to'xtatish (graceful shutdown) ishlamaydi.

```java
// yomon: uzilish belgisi yo'qoldi - executor to'xtamaydi
try {
    queue.poll(1, TimeUnit.SECONDS);
} catch (InterruptedException e) {
    log.warn("uzildi", e);
}

// yaxshi: belgi tiklandi va sikl to'xtadi
try {
    queue.poll(1, TimeUnit.SECONDS);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();     // belgini tiklash
    throw new SettlementInterruptedException("hisob-kitob uzildi", e);
}
```

### 19.6 `Throwable`, `Error` va `OutOfMemoryError` siyosati

`Error` ierarxiyasi (`OutOfMemoryError`, `StackOverflowError`, `NoClassDefFoundError`) JVM darajasidagi muammolarni bildiradi va ularni tutish deyarli har doim xato: tizim allaqachon ishonchsiz holatda.

```java
// yomon: Error ni tutish - JVM ishonchsiz holatda davom etadi
catch (Throwable t) {
    log.error("xato", t);
    return fallback();
}

// yaxshi: faqat Exception, Error yuqoriga o'tadi
catch (Exception e) {
    log.error("hisob-kitob muvaffaqiyatsiz: {}", paymentId, e);
    throw new SettlementFailedException(paymentId, e);
}
```

Yagona istisno: eng tashqi thread chegarasi (`UncaughtExceptionHandler`, scheduler) `Throwable` ni tutib log qilishi va keyin tizimni to'xtatishi mumkin — lekin davom ettirmasligi kerak.

### 19.7 Log qilish yoki tashlash: ikkisini birga qilmaslik

`catch` ichida ham log yozish, ham istisnoni qayta tashlash eng ko'p uchraydigan log shovqini manbai: bir xato log da uch-to'rt marta paydo bo'ladi va incident vaqtida haqiqiy sabab topilmaydi.

Qoida: istisnoni **qayta ishlagan** joy log yozadi; uzatib yuborgan joy log yozmaydi (29.5).

```java
// yomon: har bir qatlam log yozadi - bitta xato uch marta log'da
catch (IOException e) {
    log.error("fayl o'qilmadi", e);
    throw new ImportException(e);
}

// yaxshi: kontekst qo'shiladi, log yuqorida bir marta yoziladi
catch (IOException e) {
    throw new ImportException("fayl o'qilmadi: " + file, e);
}

// Eng tashqi chegarada bir marta:
@ExceptionHandler(ImportException.class)
ResponseEntity<ProblemDetail> handle(ImportException e) {
    log.error("import muvaffaqiyatsiz", e);         // bitta joyda
    return ResponseEntity.status(422).body(problem(e));
}
```

### 19.8 Assertion va `-ea`: qachon haqli

`assert` gapi standart holatda **o'chirilgan** (`-ea` flagi kerak), shuning uchun u hech qachon kirish ma'lumotini tekshirish uchun ishlatilmasligi kerak — production da u umuman bajarilmaydi.

Assertion faqat bitta holatda haqli: **ichki** taxminni hujjatlashtirish va test muhitida tekshirish. Public API validatsiyasi esa har doim oshkor tekshiruv bilan amalga oshadi.

```java
// yomon: kirish tekshiruvi assert bilan - production da o'chirilgan
public void refund(Money amount) {
    assert amount.isPositive();           // ishlamaydi!
}

// yaxshi: kirish tekshiruvi oshkor, ichki taxmin assert bilan
public void refund(Money amount) {
    if (!amount.isPositive()) {
        throw new IllegalArgumentException("summa musbat bo'lishi kerak: " + amount);
    }
    ...
    assert invariantHolds() : "refund dan keyin qoldiq manfiy bo'lib qoldi";
}
```

### 19.9 `Objects.requireNonNull`, Guava `Preconditions`, Bean Validation

Uch vosita, uch xil o'rin. Ularni aralashtirish kodni izchilsiz qiladi.

| Vosita | Qayerda | Nima tashlaydi |
|---|---|---|
| `Objects.requireNonNull` | konstruktor, public metod, `null` tekshiruvi | `NullPointerException` |
| Qo'lda `if` + istisno | biznes qoidasi, diapazon | domen yoki `IllegalArgumentException` |
| Guava `Preconditions` | kutubxona kodi, xabar formatlash | `IllegalArgumentException`/`State` |
| Bean Validation (`@Valid`) | HTTP va xabar chegarasi | `MethodArgumentNotValidException` |
| `record` compact konstruktori | value object invarianti | istalgan |
| `assert` | ichki taxmin, test muhiti | `AssertionError` |

```java
// yaxshi: har biri o'z o'rnida
public SettlementService(PaymentGateway gateway, Clock clock) {
    this.gateway = Objects.requireNonNull(gateway, "gateway");
    this.clock = Objects.requireNonNull(clock, "clock");
}
```

Qoida: xabar har doim **maydon nomini** ko'rsatishi kerak — `requireNonNull(gateway)` xabarsiz `NullPointerException` beradi va stack trace dan qaysi argument `null` bo'lganini aniqlash qiyin bo'ladi.

### 19.10 Xato xabari matni: uch xil adresat

Bitta xato uch joyga chiqadi va uchtasiga boshqa matn kerak. Ularni aralashtirish ikki muammo keltiradi: foydalanuvchi texnik matnni ko'radi, yoki injener foydasiz "Xatolik yuz berdi" xabarini o'qiydi.

| Adresat | Nima kerak | Nima kerak emas |
|---|---|---|
| Foydalanuvchi | nima bo'ldi, nima qilish kerak, o'z tilida | stack trace, SQL, identifikator |
| Log (injener) | obyekt identifikatori, kutilgan va haqiqiy holat, trace id | foydalanuvchi uchun xushmuomalalik |
| API klient | barqaror xato kodi, maydon nomi, qisqa izoh | ichki sinf nomi, stack trace |

```java
// Domen istisnosi: injener uchun to'liq kontekst
public class RefundExceedsPaymentException extends DomainException {
    public RefundExceedsPaymentException(PaymentId id, Money requested, Money refundable) {
        super("REFUND_EXCEEDS_PAYMENT",
              "to'lov %s uchun %s qaytarilmoqchi, lekin faqat %s qaytarish mumkin"
                      .formatted(id, requested, refundable));
    }
}

// Chegarada: API klient uchun barqaror kod, foydalanuvchi uchun xabar
@ExceptionHandler(RefundExceedsPaymentException.class)
ProblemDetail handle(RefundExceedsPaymentException e, Locale locale) {
    ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.UNPROCESSABLE_ENTITY);
    problem.setProperty("code", e.code());                       // barqaror kod
    problem.setDetail(messages.getMessage(e.code(), locale));     // foydalanuvchi tili
    return problem;
}
```

### 19.11 Xato kodi katalogi va uni barqaror ushlash

API klientlari xato **kodiga** qarab shoxlanadi, matnga qarab emas. Shuning uchun kod barqaror bo'lishi kerak: bir marta e'lon qilingan kod ma'nosini o'zgartirmaydi va o'chirilmaydi.

Amalda bu enum yoki konstanta katalogi bilan amalga oshadi va u hujjatlashtiriladi.

```java
public enum SettlementErrorCode {
    REFUND_EXCEEDS_PAYMENT("qaytarish summasi to'lovdan oshdi"),
    PAYMENT_NOT_SETTLED("to'lov hali bank tomonidan yopilmagan"),
    GATEWAY_UNAVAILABLE("bank gateway javob bermadi"),
    IDEMPOTENCY_CONFLICT("bir xil kalit bilan boshqa so'rov yuborilgan");

    private final String description;
    SettlementErrorCode(String description) { this.description = description; }
}
```

### 19.12 Amalda qo'llash

- [ ] Barcha `catch` bloklarini ko'rib, sababni (`cause`) uzatmaydiganlarini tuzating.
- [ ] `catch (Throwable)` va `catch (Error)` ni topib, eng tashqi chegaradan tashqari joylarda olib tashlang.
- [ ] `finally` ichida `return` yoki `throw` bo'lgan joylarni tuzatib, Error Prone `Finally` qoidasini yoqing.
- [ ] Qo'lda `finally` da yopiladigan resurslarni `try-with-resources` ga o'tkazing.
- [ ] `InterruptedException` tutilgan barcha joylarda `Thread.currentThread().interrupt()` borligini tekshiring.
- [ ] "Log va qayta tashlash" namunalarini topib, log ni faqat qayta ishlagan joyda qoldiring.
- [ ] `assert` bilan kirish tekshiradigan joylarni oshkor tekshiruvga o'tkazing.
- [ ] API xato kodlari katalogini enum sifatida yozib, hujjatlashtiring va barqarorlik qoidasini kelishib oling.
# VII. Java tilining toza ishlatilishi

## 20. Primitiv, son va pul (Primitives, Numbers and Money)

Son bilan ishlash Java da eng ko'p jim xato beradigan soha: natija noto'g'ri, lekin istisno tashlanmaydi. Bu bobda pul hisobining qoidalari, `BigDecimal` mexanikasi, to'lib ketish, boxing, va identifikator generatsiyasi.

### 20.1 Pul uchun `double` ishlatmaslik

`double` va `float` ikkilik kasr sifatida saqlanadi va `0.1` ni aniq ifodalay olmaydi. Pul hisobida bu darhol xatoga olib keladi va xato yillar davomida yig'iladi.

```java
// yomon: natija 0.30000000000000004
double total = 0.1 + 0.2;

// yomon: 1.03 - 0.42 = 0.6100000000000001
double change = 1.03 - 0.42;

// yaxshi: BigDecimal satr konstruktori bilan
BigDecimal total = new BigDecimal("0.10").add(new BigDecimal("0.20"));   // 0.30

// eng yaxshi: Money value object (3.3)
Money total = Money.of("0.10", UZS).plus(Money.of("0.20", UZS));
```

Qo'shimcha muhim qoida: `new BigDecimal(0.1)` **xato** — u `double` ni oladi va noaniqlikni saqlab qoladi. Har doim `new BigDecimal("0.1")` yoki `BigDecimal.valueOf(0.1)` ishlatiladi.

| Vazifa | To'g'ri tur |
|---|---|
| Pul summasi | `BigDecimal` yoki `Money` |
| Pulni butun sonda saqlash | `long` (tiyin), nomda birlik (3.3) |
| Foiz, stavka | `BigDecimal` |
| O'lchov (og'irlik, masofa) | `BigDecimal` yoki value object |
| Ilmiy hisob, grafika | `double` |
| Sanoq, identifikator | `long`, `int` |
| Bazadagi ustun | `numeric(19,4)`, `double precision` emas |

### 20.2 `BigDecimal` scale, rounding va `equals` tuzog'i

`BigDecimal` da uch tuzoq bor va uchtasi ham production da uchraydi.

**Birinchi**: `equals` scale ni hisobga oladi. `new BigDecimal("1.0").equals(new BigDecimal("1.00"))` → `false`. Solishtirish uchun `compareTo` ishlatiladi (15.6).

**Ikkinchi**: `divide` aniq bo'linmasa `ArithmeticException` tashlaydi. Har doim scale va `RoundingMode` berish kerak.

**Uchinchi**: yakkalash qoidasi (rounding) biznes qarori. `HALF_UP` odatiy, lekin bank hisobida `HALF_EVEN` (banker's rounding) talab qilinishi mumkin.

```java
// yomon: ArithmeticException: Non-terminating decimal expansion
BigDecimal share = total.divide(new BigDecimal("3"));

// yaxshi: scale va rounding oshkor, biznes qarori kodda ko'rinadi
private static final int MONEY_SCALE = 2;
private static final RoundingMode MONEY_ROUNDING = RoundingMode.HALF_UP;

BigDecimal share = total.divide(new BigDecimal("3"), MONEY_SCALE, MONEY_ROUNDING);

// yomon: equals scale ga sezgir
if (amount.equals(new BigDecimal("100.00"))) { ... }
// yaxshi
if (amount.compareTo(new BigDecimal("100.00")) == 0) { ... }
```

### 20.3 Butun sonning to'lib ketishi va `Math.*Exact`

Java da butun son to'lib ketganda istisno tashlanmaydi — natija aylanib ketadi va manfiy bo'ladi. Bu `compareTo` da (15.6), hisoblagichlarda va vaqt hisobida xatoga olib keladi.

```java
// yomon: to'lib ketish jim o'tadi
int millis = seconds * 1000;              // seconds > 2_147_483 bo'lsa manfiy
int diff = a.getId().intValue() - b.getId().intValue();   // tartib teskari aylanadi

// yaxshi: to'lib ketish istisno beradi
int millis = Math.multiplyExact(seconds, 1000);
long total = Math.addExact(current, increment);

// yaxshi: solishtirish uchun ayirish emas, compare
int order = Long.compare(a.id(), b.id());
```

Qoida: hisoblagich, identifikator va vaqt oraliqlarida `long` ishlatish; arifmetikada `Math.addExact`/`multiplyExact` ni standart qilish.

### 20.4 Bo'lish, qoldiq va manfiy son xatti-harakati

Butun sonlarni bo'lish natijani kesib tashlaydi (`7 / 2 == 3`) va bu ko'pincha kutilmagan. Qoldiq (`%`) esa manfiy sonlar bilan matematik modul emas: `-1 % 3 == -1`, `2` emas.

```java
// yomon: aylanma indeks manfiy bo'lib qoladi
int index = (current - 1) % size;          // -1 bo'lishi mumkin

// yaxshi: Math.floorMod matematik modul beradi
int index = Math.floorMod(current - 1, size);

// yomon: butun bo'lish kesib tashlaydi
int average = total / count;               // 7/2 = 3

// yaxshi: niyat oshkor
int average = Math.round((float) total / count);
BigDecimal exact = BigDecimal.valueOf(total)
        .divide(BigDecimal.valueOf(count), 2, RoundingMode.HALF_UP);
```

### 20.5 Primitiv va boxed tur tanlovi, `==` tuzog'i

`Integer` va `int` farqi `==` da ko'rinadi: `Integer` solishtirilganda havolalar solishtiriladi va `-128..127` oralig'ida kesh ishlaydi, shuning uchun kichik sonlarda to'g'ri, kattalarda noto'g'ri natija chiqadi.

```java
Integer a = 127, b = 127;
a == b;        // true  (kesh)
Integer c = 128, d = 128;
c == d;        // false (yangi obyektlar) - eng chalkash xatolardan biri

// yaxshi: boxed turlarni har doim equals bilan solishtirish
Objects.equals(c, d);
// eng yaxshi: primitiv ishlatish mumkin bo'lsa, primitiv
int c = 128, d = 128;
c == d;        // true
```

Qoida: hisob va mahalliy o'zgaruvchilarda primitiv; `null` ma'noga ega bo'lgan joyda (ixtiyoriy maydon, baza ustuni) boxed tur.

### 20.6 Avtoboxing narxi va `null` unboxing

Avtoboxing ikki muammo keltiradi. Birinchi — narx: sikl ichida har bir amal yangi obyekt yaratadi. Ikkinchi va xavflisi — `null` unboxing: `null` bo'lgan `Integer` ni `int` ga aylantirish `NullPointerException` beradi va u imzoda ko'rinmaydi.

```java
// yomon: issiq siklda million obyekt yaratiladi
Long sum = 0L;
for (long i = 0; i < 1_000_000; i++) {
    sum += i;                 // har iteratsiyada boxing/unboxing
}

// yaxshi
long sum = 0L;

// yomon: NullPointerException, sababi imzoda ko'rinmaydi
int quantity = order.getQuantity();       // getQuantity() Integer qaytaradi va null bo'lishi mumkin

// yaxshi: null siyosati oshkor
int quantity = Objects.requireNonNullElse(order.quantity(), 0);
```

`Map<String, Integer>` da `map.get(key)` topilmasa `null` qaytaradi va darhol `int` ga aylantirilsa NPE beradi; `getOrDefault` ishlatish kerak (23.2).

### 20.7 Pul va o'lchovni value object bilan ifodalash

Pul uchun value object yozish primitivlarga berilish anti-patternidan (patternlar hujjati 25.19) chiqish yo'li va u uch foyda beradi: valyuta aralashmaydi, yakkalash qoidasi bir joyda, va arifmetika domen tilida o'qiladi.

```java
public record Money(BigDecimal amount, Currency currency) implements Comparable<Money> {

    private static final int SCALE = 2;
    private static final RoundingMode ROUNDING = RoundingMode.HALF_UP;

    public Money {
        Objects.requireNonNull(currency, "currency");
        amount = amount.setScale(SCALE, ROUNDING);      // scale bir joyda normallashadi
    }

    public static Money of(String amount, Currency currency) {
        return new Money(new BigDecimal(amount), currency);
    }

    public Money plus(Money other) {
        requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency);
    }

    public Money multiply(Quantity quantity) {
        return new Money(amount.multiply(BigDecimal.valueOf(quantity.value())), currency);
    }

    public boolean greaterThan(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount) > 0;
    }

    @Override
    public int compareTo(Money other) {
        requireSameCurrency(other);
        return amount.compareTo(other.amount);
    }

    private void requireSameCurrency(Money other) {
        if (currency != other.currency) {
            throw new CurrencyMismatchException(currency, other.currency);
        }
    }
}
```

### 20.8 Tasodifiy son, UUID va identifikator generatsiyasi

Tasodifiy son uchun `Math.random()` va `new Random()` kriptografik emas va ularni token, parol yoki idempotentlik kaliti uchun ishlatish xavfsizlik nuqsoni.

| Vazifa | To'g'ri vosita |
|---|---|
| Token, sir, parol tiklash kaliti | `SecureRandom` |
| Test ma'lumoti, taqsimot | `Random`, `ThreadLocalRandom` |
| Ko'p threadli hisob | `ThreadLocalRandom.current()` |
| Tashqi identifikator | `UUID.randomUUID()` (v4) |
| Tartiblangan identifikator | UUID v7 yoki `bigserial` |
| Idempotentlik kaliti | klient beradi, server generatsiya qilmaydi |
| Baza birlamchi kaliti | `bigint identity`/`bigserial` |

```java
// yomon: Random kriptografik emas, token taxmin qilinadi
String token = Long.toHexString(new Random().nextLong());

// yaxshi
private static final SecureRandom RANDOM = new SecureRandom();

static String newToken() {
    byte[] bytes = new byte[32];
    RANDOM.nextBytes(bytes);
    return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
}
```

### 20.9 Amalda qo'llash

- [ ] Pul va stavka bilan ishlaydigan barcha `double`/`float` maydonlarni topib, `BigDecimal` yoki `Money` ga o'tkazing.
- [ ] `new BigDecimal(<double>)` chaqiruvlarini satr yoki `valueOf` shakliga almashtiring.
- [ ] `BigDecimal.divide` chaqiruvlarida scale va `RoundingMode` borligini tekshiring.
- [ ] `BigDecimal.equals` ishlatilgan joylarni `compareTo` ga o'tkazing.
- [ ] Boxed turlar `==` bilan solishtirilgan joylarni `Objects.equals` yoki primitivga o'tkazing.
- [ ] Issiq sikllardagi boxed hisoblagichlarni primitiv turlarga almashtiring.
- [ ] `new Random()` ishlatilgan xavfsizlikka tegishli joylarni `SecureRandom` ga o'tkazing.
- [ ] ArchUnit qoidasi bilan `amount`, `price`, `total` nomli maydonlarda `double` ni taqiqlang.
## 21. Satr, matn va regex (Strings, Text and Regex)

Satr Java da eng ko'p ishlatiladigan tur va shu sababli eng ko'p yashirin xato manbasi: kodirovka, locale, `==` solishtirish, regex narxi. Bu bobda shu xatolarning hammasini to'sadigan qoidalar. Satr bilan tiplash (stringly typed) anti-patterni patternlar hujjatida (25.27).

### 21.1 `==` emas `equals`, `intern` va literal pool

`==` satrlar uchun havolani solishtiradi. Literal satrlar pool da saqlanadi, shuning uchun `"a" == "a"` → `true`, lekin ish vaqtida qurilgan satrlar uchun `false`. Natija: kod testda ishlaydi, production da ishlamaydi.

```java
// yomon: foydalanuvchi kiritgan satr bilan ishlamaydi
if (status == "SETTLED") { ... }

// yaxshi
if ("SETTLED".equals(status)) { ... }              // null-xavfsiz tartib
if (Objects.equals(status, expected)) { ... }

// eng yaxshi: satr emas, enum (25.27)
if (payment.status() == SettlementStatus.SETTLED) { ... }
```

`String.intern()` ni qo'lda ishlatish deyarli hech qachon kerak emas: u xotirani tejaydi, lekin JVM ichki pool ini to'ldiradi va `==` ga asoslangan xavfli kodni rag'batlantiradi.

### 21.2 Birlashtirish: `+`, `StringBuilder`, `String.join`, `formatted`

Har bir usulning o'z o'rni bor va noto'g'ri tanlov yo o'qilishni, yo tezlikni buzadi.

| Vaziyat | To'g'ri usul |
|---|---|
| Bir-ikki qism, bir marta | `+` (kompilyator optimizatsiya qiladi) |
| Siklda yig'ish | `StringBuilder` |
| Ro'yxatni ajratgich bilan birlashtirish | `String.join` yoki `Collectors.joining` |
| Shablon bo'yicha formatlash | `"...".formatted(...)` yoki `String.format` |
| Ko'p qatorli matn (SQL, JSON) | matn bloki `"""` (12.9) |
| Log xabari | SLF4J `{}` placeholder (29.1) |
| Istisno xabari | `.formatted(...)` |

```java
// yomon: siklda + - har iteratsiyada yangi String
String csv = "";
for (Sku sku : skus) { csv += sku.code() + ","; }

// yaxshi
String csv = skus.stream().map(Sku::code).collect(joining(","));

// yomon: log'da birlashtirish - daraja o'chirilgan bo'lsa ham bajariladi
log.debug("to'lov " + paymentId + " yopildi " + settledAt);

// yaxshi
log.debug("to'lov {} yopildi {}", paymentId, settledAt);
```

### 21.3 Kodirovka va `Charset` ni oshkor berish

`new String(bytes)`, `String.getBytes()`, `new FileReader(file)` platformaning standart kodirovkasini ishlatadi. Bu mahalliy mashinada UTF-8, serverda boshqa bo'lishi mumkin va natijada kirill yoki o'zbek harflari buziladi. Java 18 dan beri standart UTF-8, lekin eski kod va eski JVM lar uchun oshkor berish qoidasi qoladi.

```java
// yomon: platformaga bog'liq
String content = new String(Files.readAllBytes(path));
byte[] bytes = text.getBytes();

// yaxshi: har doim oshkor
String content = Files.readString(path, StandardCharsets.UTF_8);
byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
```

Shu qoida build va runtime sozlamalariga ham tegishli: `pom.xml` da `project.build.sourceEncoding=UTF-8`, Docker da `LANG=C.UTF-8`, JVM da `-Dfile.encoding=UTF-8`.

### 21.4 `toLowerCase`, `format` va `Locale` tuzog'i

`toLowerCase()` va `toUpperCase()` locale ga bog'liq. Turk tilida `"I".toLowerCase()` → `"ı"` (nuqtasiz), va natijada `"ID".toLowerCase().equals("id")` → `false`. Bu xato turk serverida ishga tushgan ilovada haqiqatan uchraydi.

```java
// yomon: locale ga bog'liq
if (header.toLowerCase().equals("content-type")) { ... }
String formatted = String.format("%.2f", amount);     // kasr ajratgichi locale ga bog'liq

// yaxshi: texnik solishtirish uchun ROOT
if (header.toLowerCase(Locale.ROOT).equals("content-type")) { ... }
if (header.equalsIgnoreCase("content-type")) { ... }   // yana soddaroq

// yaxshi: mashina uchun ROOT, foydalanuvchi uchun uning locale i
String forLog = String.format(Locale.ROOT, "%.2f", amount);
String forUser = NumberFormat.getCurrencyInstance(userLocale).format(amount);
```

Qoida: **mashina** uchun `Locale.ROOT`, **foydalanuvchi** uchun uning locale i. Locale ni tashlab ketish eng yomon variant.

### 21.5 `split`, `trim`, `strip`, `isBlank` farqlari

Bu metodlarning o'xshash nomlari ortida boshqacha xatti-harakat turadi.

| Metod | Nima qiladi | Tuzoq |
|---|---|---|
| `trim()` | `<= U+0020` belgilarni olib tashlaydi | Unicode bo'shliqlarni ko'rmaydi |
| `strip()` | Unicode bo'shliqlarni olib tashlaydi | Java 11+ |
| `isEmpty()` | uzunlik 0 | `" "` uchun `false` |
| `isBlank()` | bo'sh yoki faqat bo'shliq | Java 11+ |
| `split(regex)` | **regex** qabul qiladi | `split(".")` hamma narsani bo'ladi |
| `split(regex, -1)` | oxirgi bo'sh qismlarni saqlaydi | standart shakl ularni tashlaydi |
| `replaceAll` | regex | `replace` literal ishlatadi |
| `matches` | **butun** satrni tekshiradi | qisman moslik uchun `find()` |

```java
// yomon: nuqta regex da "har qanday belgi"
String[] parts = version.split(".");        // bo'sh massiv!
// yaxshi
String[] parts = version.split("\\.");
String[] parts = version.split(Pattern.quote("."));

// yomon: oxirgi bo'sh ustunlar yo'qoladi - CSV da ustun soni o'zgaradi
String[] columns = line.split(",");         // "a,b,," -> 2 element
// yaxshi
String[] columns = line.split(",", -1);     // "a,b,," -> 4 element
```

### 21.6 Regexni oldindan kompilyatsiya qilish va nomlash

`String.matches`, `replaceAll` va `split` har bir chaqiruvda regexni qaytadan kompilyatsiya qiladi. Issiq yo'lda bu sezilarli narx. Yechim: `Pattern` ni `static final` maydonga chiqarish — bu bir vaqtda tezlikni va o'qilishni yaxshilaydi, chunki regex nom oladi.

```java
// yomon: har chaqiruvda kompilyatsiya, regex nomsiz
boolean valid = iban.matches("^[A-Z]{2}\\d{2}[A-Z0-9]{1,30}$");

// yaxshi: bir marta kompilyatsiya, nom ma'no beradi
private static final Pattern IBAN_FORMAT =
        Pattern.compile("^[A-Z]{2}\\d{2}[A-Z0-9]{1,30}$");

boolean valid = IBAN_FORMAT.matcher(iban).matches();
```

Murakkab regex uchun `Pattern.COMMENTS` flagi bilan izohli shaklga o'tish mumkin, bu uzun regexni o'qiladigan qiladi.

```java
private static final Pattern SETTLEMENT_LINE = Pattern.compile("""
        ^(?<bank>[A-Z]{4})      # bank kodi: to'rt harf
        (?<date>\\d{8})          # sana: yyyyMMdd
        (?<amount>\\d{12})       # summa: tiyinda, chapdan nol bilan
        $""", Pattern.COMMENTS);
```

Nomlangan guruhlar (`(?<bank>...)`) indeks bo'yicha murojaatdan ancha o'qiladi: `matcher.group("bank")`.

### 21.7 Katastrofik backtracking va kiritish uzunligi

Ba'zi regex shakllari (ichma-ich kvantifikatorlar: `(a+)+`, `(\\w+\\s?)*`) ma'lum kiritishda eksponensial vaqtda ishlaydi va ilovani to'xtatadi. Bu ReDoS (regex denial of service) deb ataladi va tashqi kiritishni regex bilan tekshiradigan har bir joyda xavf bor.

```java
// yomon: ichma-ich kvantifikator - ReDoS xavfi
Pattern.compile("^(\\w+\\s?)*$");

// yaxshi: aniq va chegaralangan
Pattern.compile("^[\\w ]{1,200}$");
```

Qo'shimcha himoya: tashqi kiritish uzunligini regexdan **oldin** cheklash, va murakkab parsing uchun regex o'rniga haqiqiy parser ishlatish.

### 21.8 Satr bilan tiplash o'rniga tur

Satr har qanday qiymatni ushlaydi va shu sababli hech qanday xatoni to'smaydi. Domen tushunchalarini satrda saqlash eng ko'p uchraydigan tur xatosi (patternlar hujjati 25.27).

```java
// yomon: hammasi String - almashtirish kompilyatsiyadan o'tadi
void transfer(String fromIban, String toIban, String currency, String amount);

// yaxshi
void transfer(Iban from, Iban to, Money amount);
```

Qaysi tushunchalar satrda qolishi mumkin: erkin matn (izoh, tavsif, ism), va tashqi chegaradan kelgan xom qiymat (lekin u darhol turga aylantiriladi).

### 21.9 Matn blokida SQL va JSON

Matn bloki (`"""`) indentatsiyani avtomatik normallashtiradi va qochirishni (escaping) yo'qotadi, shuning uchun SQL, JSON va XML uchun to'g'ri tanlov (12.9). Uch mexanik tafsilot bilish kerak.

Birinchi, yopiluvchi `"""` ning joylashuvi indentatsiyani belgilaydi: eng chapdagi mazmun qatori va yopiluvchi qator orasidagi eng kichik indentatsiya olib tashlanadi. Ikkinchi, `\` qator oxirida yangi qatorni bostiradi. Uchinchi, `\s` bo'shliqni saqlab qoladi (orqa bo'shliqlar aks holda olib tashlanadi).

```java
// Yopiluvchi """ chapda bo'lsa, indentatsiya saqlanadi - odatda keraksiz
String json = """
        {
          "paymentId": "%s",
          "amount": %s
        }
        """.formatted(paymentId, amount);

// Bir qatorli natija kerak bo'lsa: qator oxirida \ bilan birlashtirish
String query = """
        select p.id, p.amount from payment p \
        where p.order_id = ? and p.settled_at is not null\
        """;
```

### 21.10 Amalda qo'llash

- [ ] `==` bilan satr solishtirilgan joylarni grep qilib, `equals` yoki enum ga o'tkazing.
- [ ] `getBytes()`, `new String(byte[])` va `FileReader` chaqiruvlariga oshkor `UTF_8` qo'shing.
- [ ] `toLowerCase()`/`toUpperCase()` chaqiruvlariga `Locale.ROOT` qo'shing yoki `equalsIgnoreCase` ga o'tkazing.
- [ ] `String.format` chaqiruvlarida locale oshkor berilganini tekshiring.
- [ ] `split(",")` chaqiruvlarini CSV uchun `split(",", -1)` ga o'tkazing va regex metabelgilarni qochiring.
- [ ] Barcha inline regexlarni `static final Pattern` maydonlariga chiqarib, nom bering.
- [ ] Tashqi kiritishni tekshiradigan regexlarni ichma-ich kvantifikatorga qarshi ko'rib chiqing va uzunlik chegarasi qo'ying.
- [ ] `+` bilan qurilgan SQL va JSON literallarini matn blokiga o'tkazing.
## 22. Sana, vaqt va mintaqa (Date, Time and Zone)

Vaqt bilan ishlash xatolari odatda production da, ma'lum sanada va bir marta chiqadi: yoz vaqti o'tishida, oy oxirida, yoki boshqa mintaqadagi foydalanuvchida. Bu bobda `java.time` ni to'g'ri ishlatishning qoidalari va testlanadigan vaqt.

### 22.1 `Date`, `Calendar`, `SimpleDateFormat` dan voz kechish

Eski API uch sababdan tashlab yuborilgan: `Date` o'zgaradigan (16.2 dagi sayoz o'zgarmaslik muammosi), `Calendar` oy indeksini 0 dan boshlaydi (`JANUARY == 0`), va `SimpleDateFormat` thread-safe emas — u statik maydonda saqlansa, yuk ostida tasodifiy noto'g'ri sanalar beradi.

```java
// yomon: statik SimpleDateFormat - yuk ostida buziladi
private static final SimpleDateFormat FORMAT = new SimpleDateFormat("dd.MM.yyyy");

// yaxshi: DateTimeFormatter o'zgarmas va thread-safe
private static final DateTimeFormatter FORMAT =
        DateTimeFormatter.ofPattern("dd.MM.yyyy", Locale.ROOT);
```

Legacy API ni taqiqlash uchun Checkstyle `IllegalType` qoidasi ishlatiladi (13.4) yoki ArchUnit qoidasi (42.4).

### 22.2 To'g'ri turni tanlash

`java.time` da turlar ko'p va ularni aralashtirish eng ko'p uchraydigan xato. Tanlov savoli bitta: bu qiymat **vaqt nuqtasimi** yoki **kalendar qiymatimi**.

| Tur | Nima ifodalaydi | Qachon |
|---|---|---|
| `Instant` | mutlaq vaqt nuqtasi (UTC) | hodisa vaqti, `created_at`, log |
| `LocalDate` | mintaqasiz sana | tug'ilgan kun, hisobot kuni, muddat |
| `LocalTime` | mintaqasiz vaqt | ish boshlanishi (09:00) |
| `LocalDateTime` | mintaqasiz sana va vaqt | kamdan-kam; mintaqa yo'q - noaniq |
| `OffsetDateTime` | sana, vaqt va offset | API shartnomasi, tashqi tizim |
| `ZonedDateTime` | mintaqa qoidalari bilan | kelajakdagi rejalashtirish |
| `Duration` | vaqt oralig'i (sekund) | timeout, davomiylik |
| `Period` | kalendar oralig'i (kun, oy) | "3 oy", "1 yil" |
| `YearMonth` | yil va oy | karta muddati, hisobot davri |

Qoida: hodisa vaqti **har doim** `Instant` (bazada `timestamptz`), foydalanuvchiga ko'rsatishda esa uning mintaqasiga aylantiriladi.

### 22.3 `Clock` ni inyeksiya qilish va testlanadigan vaqt

`Instant.now()` ni kod bo'ylab chaqirish vaqtni testlanmaydigan qiladi: "30 kundan keyin muddati o'tadi" qoidasini test qilish uchun tizim vaqtini o'zgartirish kerak bo'ladi. Yechim: `Clock` ni bog'liqlik sifatida uzatish.

```java
@Service
public class OrderExpiryService {

    private final Clock clock;        // inyeksiya qilinadi

    public OrderExpiryService(Clock clock) { this.clock = clock; }

    public boolean isExpired(Order order) {
        return order.createdAt().plus(ORDER_TTL).isBefore(clock.instant());
    }
}

@Configuration
class TimeConfig {
    @Bean
    Clock clock() { return Clock.systemUTC(); }      // production
}

// Test: vaqt qotirilgan, hech qanday kutish yo'q
@Test
void expiresAfterThirtyDays() {
    Clock fixed = Clock.fixed(Instant.parse("2026-03-01T00:00:00Z"), ZoneOffset.UTC);
    var service = new OrderExpiryService(fixed);
    assertThat(service.isExpired(orderCreatedAt("2026-01-01T00:00:00Z"))).isTrue();
}
```

### 22.4 `ZoneId` va UTC siyosati

Mintaqa bilan ishlashda bitta qoida xatolarning katta qismini to'sadi: **saqlash va hisob UTC da, ko'rsatish foydalanuvchi mintaqasida**. Shu chegara aniq bo'lmasa, bir xil hodisa turli joyda turli sanada ko'rinadi.

```java
// yomon: server mintaqasiga bog'liq - serverni ko'chirsa natija o'zgaradi
LocalDate today = LocalDate.now();
ZonedDateTime now = ZonedDateTime.now();

// yaxshi: mintaqa oshkor
LocalDate today = LocalDate.now(clock);                       // clock UTC da
LocalDate userToday = LocalDate.now(clock.withZone(userZone));

// Ko'rsatish chegarasida aylantirish
String display = settledAt.atZone(userZone)
        .format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT)
                .withLocale(userLocale));
```

`ZoneId.systemDefault()` ni biznes kodida ishlatish taqiqlanishi kerak: u muhitga bog'liq va testda boshqa natija beradi.

### 22.5 Davomiylik: `Duration`, `Period` va birlik nomi

`Duration` aniq vaqt oralig'ini (sekund va nanosekund) ifodalaydi, `Period` esa kalendar oralig'ini (yil, oy, kun). Farq yoz vaqti o'tishida ko'rinadi: `Duration.ofDays(1)` har doim 24 soat, `Period.ofDays(1)` esa "ertangi kun" (23 yoki 25 soat bo'lishi mumkin).

```java
// yomon: raqam va birlik kodda tarqoq
if (order.getCreatedAt() + 30 * 24 * 60 * 60 * 1000L < now) { ... }

// yaxshi: tur birlikni ushlaydi (3.3)
private static final Duration ORDER_TTL = Duration.ofDays(30);
private static final Duration GATEWAY_TIMEOUT = Duration.ofSeconds(5);

// Konfiguratsiyada ham Duration: "30d", "5s" shaklida yoziladi
@ConfigurationProperties("shop.order")
record OrderProperties(Duration ttl, Duration gatewayTimeout) { }
```

### 22.6 Chegaralar: inklyuziv va eksklyuziv oraliq

Vaqt oraliqlarida chegara xatosi eng ko'p uchraydigan hisobot xatosi: bir kunlik hisobot oxirgi soniyani yo'qotadi yoki keyingi kunni qo'shib yuboradi.

```java
// yomon: 23:59:59 dan keyingi soniyalar yo'qoladi
between(day.atStartOfDay(), day.atTime(23, 59, 59));

// yaxshi: yarim ochiq oraliq [from, to)
Instant from = day.atStartOfDay(zone).toInstant();
Instant toExclusive = day.plusDays(1).atStartOfDay(zone).toInstant();

// SQL da ham shu shakl: >= va < (indeksni ham to'g'ri ishlatadi)
// where settled_at >= ? and settled_at < ?
```

Qoida: barcha vaqt oraliqlari **yarim ochiq** (`[from, to)`) bo'ladi va bu nomda yoziladi (6.7).

### 22.7 Formatlash va parslash

`DateTimeFormatter` o'zgarmas va thread-safe, shuning uchun `static final` maydonda saqlanadi. Ikki tafsilot muhim: locale oshkor berilishi (21.4) va shablonning to'g'ri harflari.

```java
private static final DateTimeFormatter BANK_FILE_DATE =
        DateTimeFormatter.ofPattern("yyyyMMdd", Locale.ROOT);

// Eng ko'p uchraydigan shablon xatolari:
// "YYYY" - hafta-asosli yil (yanvar boshida noto'g'ri yil beradi!)
// "DD"   - yildagi kun raqami, oydagi kun emas
// "hh"   - 12 soatlik format, "HH" 24 soatlik
// To'g'ri: "yyyy-MM-dd HH:mm:ss"
```

API shartnomasida esa shablon yozmaslik kerak: ISO-8601 (`DateTimeFormatter.ISO_INSTANT`) standart va u aniq.

### 22.8 Yoz/qish vaqti, sakrash soati va oy oxiri

Uchta kalendar hodisasi kodni buzadi va ularning hammasi testlanishi kerak.

**Yoz vaqti o'tishi**: ba'zi sana-vaqtlar mavjud bo'lmaydi (soat 02:00 dan 03:00 ga o'tganda) yoki ikki marta bo'ladi. `ZonedDateTime` bu holatlarni o'zi hal qiladi, `LocalDateTime` esa yo'q — shu sababli rejalashtirish uchun `ZonedDateTime` kerak.

**Oy oxiri**: `plusMonths` kunni moslaydi (31-yanvar + 1 oy = 28/29-fevral) va bu odatda to'g'ri xatti-harakat, lekin biznes qoidasi boshqa bo'lishi mumkin.

**Kabisa yili**: 29-fevral `LocalDate.of(2026, 2, 29)` istisno beradi; foydalanuvchi kiritgan sanani har doim `try/catch` yoki `ResolverStyle` bilan tekshirish kerak.

```java
// Testda chegaraviy sanalar majburiy
@ParameterizedTest
@ValueSource(strings = {
        "2026-03-29T01:30:00",   // yoz vaqtiga o'tish kuni (Toshkentda yo'q, Yevropada bor)
        "2026-01-31",            // oy oxiri
        "2024-02-29",            // kabisa yili
        "2026-12-31T23:59:59"    // yil oxiri
})
void handlesCalendarEdges(String input) { ... }
```

### 22.9 Bazada, API da va kodda vaqt turi muvofiqligi

Uch qatlamda vaqt turi mos bo'lishi kerak, aks holda konvertatsiya paytida mintaqa yo'qoladi.

| Qatlam | To'g'ri tur |
|---|---|
| PostgreSQL ustuni | `timestamptz` (hodisa), `date` (kalendar kuni) |
| JDBC/JPA maydoni | `Instant` yoki `OffsetDateTime`, `LocalDate` |
| Domen obyekti | `Instant`, `LocalDate` |
| JSON API | ISO-8601 satr (`2026-03-01T10:15:30Z`) |
| Konfiguratsiya | `Duration` (`30s`, `5m`) |
| Log | ISO-8601, UTC |
| Metrika | Unix epoch |

`timestamp without time zone` ustunini `Instant` ga bog'lash eng ko'p uchraydigan nomuvofiqlik: baza mintaqani saqlamaydi va qiymat server mintaqasiga qarab o'zgaradi (arxitektor hujjati 25-bob sxema dizaynini ko'rib chiqadi).

### 22.10 Amalda qo'llash

- [ ] `java.util.Date`, `Calendar` va `SimpleDateFormat` ni Checkstyle yoki ArchUnit bilan taqiqlang va qolganlarini ko'chiring.
- [ ] `Instant.now()`, `LocalDate.now()` chaqiruvlarini topib, `Clock` inyeksiyasiga o'tkazing.
- [ ] `Clock` bean ini `Clock.systemUTC()` sifatida e'lon qilib, testlarda `Clock.fixed` ishlatishni standart qiling.
- [ ] `ZoneId.systemDefault()` ishlatilgan joylarni oshkor mintaqaga almashtiring.
- [ ] Vaqt oraliqlarini yarim ochiq (`[from, to)`) shaklga keltirib, nomda inklyuzivlikni yozing.
- [ ] Timeout va TTL qiymatlarini `Duration` ga o'tkazib, konfiguratsiyada `30s` shaklida yozing.
- [ ] `DateTimeFormatter` shablonlarida `YYYY`, `DD`, `hh` xatolarini qidirib tuzating.
- [ ] Baza ustunlarini `timestamptz` ga keltirib, JPA maydonlari `Instant` ekanini tekshiring.
## 23. To'plamlar va generiklar gigiyenasi (Collections and Generics)

To'plam tanlovi va generik turlar bilan ishlash Java kodining kundalik qismi, va shu sababli kichik xatolar ko'p takrorlanadi. Bu bobda to'plam turini tanlash, `Map` ni toza ishlatish, iteratsiya tartibi, o'zgartirilmaslik darajalari (16.3 ni to'ldiradi) va generiklar qoidalari.

### 23.1 To'g'ri to'plam turini tanlash

To'plam tanlovi xatti-harakatni belgilaydi: tartib, dublikat, qidiruv tezligi, `null` siyosati. Noto'g'ri tanlov kodni ishlaydigan, lekin sekin yoki nozik xato bilan qoldiradi.

| Ehtiyoj | Tur |
|---|---|
| Tartibli ro'yxat, indeks bo'yicha kirish | `ArrayList` |
| Boshidan/oxiridan qo'shish, navbat | `ArrayDeque` |
| Dublikatsiz, tartib muhim emas | `HashSet` |
| Dublikatsiz, qo'shilish tartibida | `LinkedHashSet` |
| Dublikatsiz, saralangan | `TreeSet` |
| Kalit-qiymat, tartib muhim emas | `HashMap` |
| Kalit-qiymat, qo'shilish tartibida | `LinkedHashMap` |
| Kalit-qiymat, saralangan | `TreeMap` |
| Kalit - enum | `EnumMap` (25.9) |
| O'zgarmas, kichik | `List.of`, `Map.of`, `Set.of` |
| Ko'p threadli | `ConcurrentHashMap`, `CopyOnWriteArrayList` |

`LinkedList` ni ishlatish uchun deyarli hech qanday sabab qolmagan: `ArrayDeque` navbat uchun tezroq, `ArrayList` ro'yxat uchun tezroq.

### 23.2 `Map` ni toza ishlatish

`Map` bilan ishlashda eski shakllar (`containsKey` + `get` + `put`) uzun, ikki marta qidiradi va xatoga moyil. Zamonaviy metodlar bir chaqiruvda ishlaydi va niyatni aytadi.

```java
// yomon: uch chaqiruv, uch marta hash hisoblanadi
if (!index.containsKey(sku)) {
    index.put(sku, new ArrayList<>());
}
index.get(sku).add(order);

// yaxshi
index.computeIfAbsent(sku, k -> new ArrayList<>()).add(order);

// yomon: null tekshiruvi va NPE xavfi (20.6)
Integer count = counters.get(sku);
counters.put(sku, count == null ? 1 : count + 1);

// yaxshi
counters.merge(sku, 1, Integer::sum);

// yaxshi: standart qiymat
int available = stock.getOrDefault(sku, 0);
```

| Niyat | Metod |
|---|---|
| Yo'q bo'lsa yaratish | `computeIfAbsent` |
| Bor bo'lsa yangilash | `computeIfPresent` |
| Qiymatni yig'ish | `merge` |
| Standart qiymat o'qish | `getOrDefault` |
| Faqat yo'q bo'lsa qo'yish | `putIfAbsent` |
| Shart bo'yicha o'chirish | `entrySet().removeIf` |
| Hamma qiymatni o'zgartirish | `replaceAll` |

### 23.3 `Collectors.toMap` va takrorlangan kalit

`Collectors.toMap` ikki argumentli shakli takrorlangan kalit uchrasa `IllegalStateException` tashlaydi. Bu ko'pincha testda ko'rinmaydi va production ma'lumotida chiqadi.

```java
// yomon: dublikat kalit bo'lsa IllegalStateException
Map<Sku, Order> byTopSku = orders.stream()
        .collect(toMap(Order::topSku, identity()));

// yaxshi: birlashtirish funksiyasi oshkor - qaror kodda ko'rinadi
Map<Sku, Order> byTopSku = orders.stream()
        .collect(toMap(Order::topSku, identity(), (first, second) -> first));

// yaxshi: dublikat normal bo'lsa, guruhlash
Map<Sku, List<Order>> bySku = orders.stream().collect(groupingBy(Order::topSku));
```

Ikkinchi tuzoq: `toMap` `null` qiymatni qabul qilmaydi (`merge` ichida NPE beradi), `groupingBy` esa qabul qiladi.

### 23.4 Iteratsiya tartibi

`HashMap` va `HashSet` tartibi **kafolatlanmaydi** va JVM versiyasi yoki element soni o'zgarganda o'zgaradi. Shu sababli ularning tartibiga bog'lanish yashirin xato: kod bugun ishlaydi, keyingi reliz da boshqa tartib beradi.

```java
// yomon: tartibga bog'langan test va mantiq
Map<String, Integer> counts = new HashMap<>();
String report = counts.keySet().stream().collect(joining(", "));   // tartib tasodifiy

// yaxshi: tartib kerak bo'lsa, u oshkor tanlanadi
Map<String, Integer> counts = new LinkedHashMap<>();    // qo'shilish tartibi
Map<String, Integer> counts = new TreeMap<>();          // alifbo tartibi
String report = counts.keySet().stream().sorted().collect(joining(", "));
```

### 23.5 `Arrays.asList`, `List.of` va o'zgartirilmaslik farqi

Uch shakl o'xshash ko'rinadi, lekin uch xil xatti-harakat beradi va ularni aralashtirish `UnsupportedOperationException` ga olib keladi.

```java
List<String> a = Arrays.asList("x", "y");   // fiksirlangan hajm; set() ishlaydi, add() yo'q
List<String> b = List.of("x", "y");         // to'liq o'zgarmas; null taqiqlangan
List<String> c = new ArrayList<>(List.of("x", "y"));   // to'liq o'zgaradi

a.set(0, "z");    // ishlaydi
a.add("z");       // UnsupportedOperationException
b.set(0, "z");    // UnsupportedOperationException
```

Qoida: o'zgarmas kerak bo'lsa `List.of`/`List.copyOf`; o'zgaradigan kerak bo'lsa oshkor `new ArrayList<>(...)`. `Arrays.asList` faqat massivni ro'yxat sifatida o'qish uchun.

### 23.6 `null` kalit va qiymat siyosati

`null` ga munosabat to'plam turiga qarab farq qiladi va bu farq hujjatlanmagan xatolarning manbai.

| Tur | `null` kalit | `null` qiymat |
|---|---|---|
| `HashMap` | 1 ta ruxsat | ruxsat |
| `TreeMap` | taqiqlangan (NPE) | ruxsat |
| `ConcurrentHashMap` | taqiqlangan | taqiqlangan |
| `Map.of` | taqiqlangan | taqiqlangan |
| `HashSet` | 1 ta ruxsat | — |
| `List.of` | taqiqlangan | — |
| `ArrayList` | ruxsat | — |

Eng ko'p uchraydigan tuzoq: `HashMap` dan `ConcurrentHashMap` ga o'tish mavjud kodni buzadi, chunki `null` qiymat endi taqiqlangan. Qoida: to'plamlarda `null` ni umuman ishlatmaslik (18.7).

### 23.7 Xom tur va `unchecked` ogohlantirish

Xom tur (`List` generik parametrsiz) tur xavfsizligini butunlay o'chiradi va faqat eski kod bilan moslik uchun qolgan. `@SuppressWarnings("unchecked")` esa faqat ikki shart bilan haqli: boshqa yo'l yo'q, va sabab izohda yozilgan.

```java
// yomon: xom tur - tur tekshiruvi yo'q
List orders = repository.findAll();
orders.add("satr");           // kompilyatsiyadan o'tadi, ClassCastException keyin chiqadi

// yaxshi: generik tur
List<Order> orders = repository.findAll();

// yaxshi: bostirish eng kichik qamrovda va izohlangan
@SuppressWarnings("unchecked")   // JPA native query Object[] qaytaradi, mapping qo'lda
List<SettlementRow> rows = (List<SettlementRow>) query.getResultList();
```

Qoida: `-Xlint:all` va `-Werror` bilan ogohlantirishlarni xatoga aylantirish (25.11).

### 23.8 Wildcard qoidalari: PECS

Generik parametrlarda `? extends` va `? super` tanlovi uchun oddiy qoida bor: **PECS** — Producer Extends, Consumer Super. Agar parametr ma'lumot **beradi** (o'qiladi), `? extends`; agar ma'lumot **oladi** (yoziladi), `? super`.

```java
// Ishlab chiqaruvchi (o'qiymiz): extends
Money totalOf(List<? extends Payment> payments) {
    return payments.stream().map(Payment::amount).reduce(Money.ZERO, Money::add);
}
// Shunda List<CardPayment> ham, List<BankPayment> ham qabul qilinadi

// Iste'molchi (yozamiz): super
void collectInto(List<? super SettlementRow> target) {
    target.add(new SettlementRow(...));
}

// Ikkisi ham kerak bo'lsa: wildcard yo'q, aniq tur
void copy(List<? extends T> source, List<? super T> target) { ... }
```

Amaliy qoida: **qaytish turida** wildcard ishlatmaslik — u chaqiruvchini wildcard bilan ishlashga majbur qiladi va kod tarqaladi.

### 23.9 Generik metod, tur xulosasi va `var`

Generik metod turni argumentdan xulosa qiladi va bu kodni qisqartiradi. `var` bilan birga ishlatilganda esa tur umuman ko'rinmay qolishi mumkin — bunda o'qilish buziladi (arxitektor hujjati 13.4).

```java
// yaxshi: generik metod, tur xulosa qilinadi
static <T> List<T> firstN(List<T> source, int n) { ... }
List<Order> first10 = firstN(orders, 10);

// yomon: var + generik metod - tur hech qayerda ko'rinmaydi
var result = process(input);

// yaxshi: var faqat o'ng tomonda tur ko'rinsa
var orders = new ArrayList<Order>();
var byId = new HashMap<OrderId, Order>();
```

### 23.10 Massiv va generikni aralashtirmaslik

Massivlar kovariant (`Object[] = String[]` ruxsat) va ish vaqtida tur tekshiradi; generiklar invariant va ish vaqtida turni o'chiradi. Ikkisini aralashtirish `ArrayStoreException` yoki kompilyator ogohlantirishiga olib keladi.

```java
// yomon: massiv kovariantligi ish vaqtida xato beradi
Object[] objects = new String[1];
objects[0] = 42;              // ArrayStoreException

// yomon: generik massiv yaratib bo'lmaydi
List<String>[] lists = new List<String>[10];    // kompilyatsiya xatosi

// yaxshi: to'plam ishlatish
List<List<String>> lists = new ArrayList<>();
```

Qoida: public API da massiv qaytarmaslik (u o'zgaradi va nusxa talab qiladi, 14.7); `List` qaytarish.

### 23.11 To'plamni qaytarish: nusxa, ko'rinish, oqim

Metod to'plam qaytarganda uchta tanlov bor va ularning har biri boshqa shartnoma beradi.

| Shakl | Shartnoma | Qachon |
|---|---|---|
| `List.copyOf(internal)` | o'zgarmas nusxa | standart tanlov |
| `Collections.unmodifiableList(internal)` | o'zgarmas ko'rinish, manba o'zgarsa o'zgaradi | katta to'plam, ichki ishlatish |
| `new ArrayList<>(internal)` | chaqiruvchi o'zgartira oladi | kamdan-kam, oshkor hujjatlanadi |
| `Stream<T>` | bir marta o'qiladi | katta natija, lazy |
| `Iterable<T>` | faqat iteratsiya | API ni torroq qilish |

Hech qachon ichki to'plamni to'g'ridan-to'g'ri qaytarmaslik kerak (14.7). Qaytish turi nomda va hujjatda aniq bo'lishi kerak: `List` tartibni kafolatlaydi, `Collection` yo'q.

### 23.12 Amalda qo'llash

- [ ] `containsKey` + `get` + `put` namunalarini `computeIfAbsent`, `merge`, `getOrDefault` ga o'tkazing.
- [ ] `Collectors.toMap` ning ikki argumentli shakllarini topib, birlashtirish funksiyasini oshkor qo'shing.
- [ ] `HashMap`/`HashSet` tartibiga bog'langan mantiq va testlarni topib, `LinkedHashMap` yoki oshkor saralashga o'tkazing.
- [ ] `Arrays.asList` ishlatilgan joylarni niyatga qarab `List.of` yoki `new ArrayList<>` ga almashtiring.
- [ ] Xom generik turlarni (`List`, `Map` parametrsiz) topib, tur parametrlarini qo'shing.
- [ ] `@SuppressWarnings` larni ko'rib, qamrovini torroq qilib, sababini izohlang.
- [ ] Public API dagi massiv qaytaradigan metodlarni `List` ga o'tkazing.
- [ ] To'plam qaytaradigan getter larni 23.11 jadvaliga qarab bitta izchil shaklga keltiring.
## 24. Lambda, oqim va funksional uslub tozaligi (Lambdas and Streams)

Oqim va sikl tanlovi arxitektor hujjatida (13.6), `Optional` ning to'g'ri ishlatilishi 13.5 da berilgan. Bu bobda funksional kodning tozalik qoidalari: lambda uzunligi, metod havolasi, yon ta'sir, `Collectors` ni o'qiladigan ushlash va istisnolar.

### 24.1 Lambda uzunligi va uni metodga chiqarish

Lambda bir ifoda bo'lsa o'qiladi; blokka aylansa (qavs va `return` paydo bo'lsa) o'qilishi tushadi. Amaliy chegara: lambda uch qatordan oshsa, uni nomlangan metodga chiqarish kerak — shunda nom niyatni aytadi va metod alohida testlanadi.

```java
// yomon: oqim ichida 8 qatorli lambda
List<SettlementRow> valid = rows.stream()
        .filter(row -> {
            if (row.amount() == null) return false;
            if (row.amount().signum() <= 0) return false;
            if (row.currency() == null) return false;
            if (!SUPPORTED.contains(row.currency())) return false;
            return row.settledAt() != null;
        })
        .toList();

// yaxshi: qoida nomlangan va testlanadi
List<SettlementRow> valid = rows.stream()
        .filter(this::isValid)
        .toList();

private boolean isValid(SettlementRow row) { ... }
```

### 24.2 Metod havolasi qachon o'qiladi

Metod havolasi (`Payment::isSettled`) lambdadan qisqa va nom ma'noni aytadi, shuning uchun mavjud bo'lsa afzal. Lekin u har doim o'qiladi degani emas: argumentlar tartibi ko'rinmasa yoki konstruktor havolasi noaniq bo'lsa, lambda aniqroq.

```java
// yaxshi: metod havolasi nomni beradi
.filter(Payment::isSettled)
.map(Payment::amount)
.sorted(comparing(Payment::settledAt))

// yomon: argumentlar tartibi ko'rinmaydi
.reduce(Money::add)            // qaysi qiymat qaysi pozitsiyada?
// yaxshi: aniq
.reduce(Money.ZERO, (sum, next) -> sum.plus(next))

// yomon: konstruktor havolasi noaniq (bir nechta konstruktor bor)
.map(SettlementRow::new)
// yaxshi
.map(line -> SettlementRow.parse(line))
```

### 24.3 Standart funksional interfeyslar va o'zingiznikini yozmaslik

`java.util.function` paketi 43 ta interfeys beradi va ularning hammasi uchun o'z interfeysingizni yozish keraksiz: standart turlar bilan sizning kodingiz boshqa kutubxonalar bilan birga ishlaydi.

| Shakl | Interfeys |
|---|---|
| `T → R` | `Function<T,R>` |
| `T → boolean` | `Predicate<T>` |
| `T → void` | `Consumer<T>` |
| `() → T` | `Supplier<T>` |
| `(T,U) → R` | `BiFunction<T,U,R>` |
| `T → T` | `UnaryOperator<T>` |
| `(T,T) → T` | `BinaryOperator<T>` |
| primitiv variantlar | `IntPredicate`, `ToLongFunction` va h.k. |

O'z interfeysingizni yozish faqat ikki holatda haqli: nom domen ma'nosini beradi (`interface TaxPolicy { Money taxFor(Region r, Money net); }`), yoki tekshiriladigan istisno tashlanishi kerak (24.7).

### 24.4 Oqim ichida yon ta'sir va `forEach` tuzog'i

Oqim transformatsiya uchun mo'ljallangan; uning ichida tashqi holatni o'zgartirish ikki muammo keltiradi: parallel oqimda poyga holati, va o'qilishi — oqim nima qaytarayotgani ko'rinmaydi.

```java
// yomon: oqim ichida tashqi holat o'zgaradi
List<String> codes = new ArrayList<>();
orders.stream().forEach(order -> codes.add(order.code()));   // yon ta'sir

// yaxshi: oqim natija qaytaradi
List<String> codes = orders.stream().map(Order::code).toList();

// yomon: forEach ichida biznes amali va tranzaksiya
orders.stream().forEach(order -> {
    order.markShipped();
    repository.save(order);        // har bir element uchun alohida so'rov (7.9)
});

// yaxshi: oqim tanlaydi, sikl yoki paket amali o'zgartiradi
List<OrderId> toShip = orders.stream().filter(Order::isReadyToShip).map(Order::id).toList();
repository.markShipped(toShip);
```

### 24.5 `peek`, `parallelStream` va tartib

`peek` faqat **debug** uchun mo'ljallangan va uni mantiqda ishlatish xato: terminal amal bo'lmasa oqim umuman bajarilmaydi, va ba'zi optimizatsiyalarda `peek` chaqirilmaydi.

`parallelStream` esa deyarli har doim noto'g'ri tanlov: u umumiy `ForkJoinPool.commonPool` ni ishlatadi (butun ilova bilan birga), kichik to'plamlarda sekinroq, va yon ta'sirli kod bilan buziladi. Qoida: `parallelStream` faqat o'lchov natijasi asosida, CPU ga bog'liq, katta va mustaqil hisob uchun.

```java
// yomon: tartibni buzadi va umumiy pool ni egallaydi
orders.parallelStream().forEach(repository::save);     // I/O - parallel oqim uchun emas

// yaxshi: I/O uchun oshkor executor
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    orders.forEach(order -> executor.submit(() -> gateway.notify(order)));
}
```

`forEachOrdered` tartibni saqlaydi, lekin parallel oqimning foydasini yo'qotadi — bu ikkisining birga kerak bo'lishi parallel oqim noto'g'ri tanlov ekanini bildiradi.

### 24.6 `Optional` ni zanjirda toza ishlatish

`Optional` ning asosiy qoidalari arxitektor hujjatida (13.5): qaytish qiymati sifatida ishlatiladi, maydon va parametr sifatida emas. Bu yerda zanjirni toza ushlash qoidalari.

```java
// yomon: isPresent + get - Optional ning ma'nosi yo'qoladi
if (maybeOrder.isPresent()) {
    return maybeOrder.get().total();
}
return Money.ZERO;

// yaxshi: zanjir
return maybeOrder.map(Order::total).orElse(Money.ZERO);

// yomon: orElse ichida qimmat chaqiruv - har doim bajariladi
return findCached(id).orElse(loadFromDatabase(id));    // baza har doim o'qiladi!

// yaxshi: orElseGet lazy
return findCached(id).orElseGet(() -> loadFromDatabase(id));

// yaxshi: topilmasa istisno, xabar bilan
return repository.findById(id)
        .orElseThrow(() -> new OrderNotFoundException(id));
```

Qo'shimcha qoidalar: `Optional.get()` ni hech qachon tekshiruvsiz chaqirmaslik, `Optional` ni `null` qilmaslik, va `Optional<List<T>>` o'rniga bo'sh ro'yxat qaytarish (18.8).

### 24.7 Tekshiriladigan istisno va lambda

Standart funksional interfeyslar tekshiriladigan istisno tashlamaydi, shuning uchun oqim ichida `IOException` tashlaydigan kod kompilyatsiyadan o'tmaydi. Uch yechim bor va ularning tartibi shunday.

```java
// 1) Eng yaxshi: oqim o'rniga sikl ishlatish
List<String> contents = new ArrayList<>();
for (Path file : files) {
    contents.add(Files.readString(file, UTF_8));     // istisno tabiiy o'tadi
}

// 2) O'rash uchun yordamchi metod (istisno turini saqlab)
private String readOrThrow(Path file) {
    try {
        return Files.readString(file, UTF_8);
    } catch (IOException e) {
        throw new UncheckedIOException("fayl o'qilmadi: " + file, e);
    }
}
List<String> contents = files.stream().map(this::readOrThrow).toList();

// 3) Yomon: lambda ichida try/catch - oqim o'qilmaydi
files.stream().map(f -> { try { ... } catch (IOException e) { ... } });
```

`@SneakyThrows` (Lombok) bu muammoni yashiradi, lekin istisnoni imzodan olib tashlaydi va chaqiruvchi uni ko'rmaydi — shu sababli taqiqlanishi kerak (26.10).

### 24.8 `Collectors` ni o'qiladigan ushlash

`Collectors` zanjirlari tez murakkablashadi va ichma-ich `groupingBy` o'qilmaydigan kod beradi. Qoida: ikki darajadan chuqur guruhlashni oraliq turga chiqarish.

```java
// yomon: uch darajali ichma-ich collector - o'qilmaydi
Map<Region, Map<Currency, List<Money>>> result = payments.stream()
        .collect(groupingBy(Payment::region,
                groupingBy(Payment::currency,
                        mapping(Payment::amount, toList()))));

// yaxshi: oraliq tur ma'no beradi
record RegionCurrency(Region region, Currency currency) { }

Map<RegionCurrency, Money> totals = payments.stream()
        .collect(groupingBy(p -> new RegionCurrency(p.region(), p.currency()),
                reducing(Money.ZERO, Payment::amount, Money::plus)));
```

Statik import (`groupingBy` emas `Collectors.groupingBy`) shu kodni ancha o'qiladigan qiladi va bu `Collectors` uchun qabul qilingan istisno (12.7).

### 24.9 Oqimni qaytarish yoki to'plam qaytarish

Public metod `Stream` qaytarishi mumkin, lekin bu shartnomani o'zgartiradi: oqim bir marta o'qiladi va yopilishi kerak bo'lishi mumkin. Shuning uchun standart tanlov — `List` qaytarish; `Stream` faqat ikki holatda.

| Holat | Qaytish turi |
|---|---|
| Kichik yoki o'rta natija | `List<T>` |
| Katta natija, lazy o'qish kerak | `Stream<T>` (`@MustBeClosed` bilan) |
| Bazadan oqim (kursor) | `Stream<T>`, `try-with-resources` majburiy |
| Faqat iteratsiya kerak | `Iterable<T>` |
| Chaqiruvchi filtrlaydi | `List<T>`, keyin `.stream()` |

```java
// Bazadan oqim: yopilishi majburiy va bu hujjatlanadi
/**
 * Hisobot uchun to'lovlar oqimi. Oqim <b>yopilishi kerak</b>:
 * {@code try (var stream = ...)} ichida ishlatiladi, aks holda
 * ulanish qaytarilmaydi.
 */
@Transactional(readOnly = true)
Stream<Payment> streamSettledIn(DateRange range);
```

### 24.10 Amalda qo'llash

- [ ] Uch qatordan uzun lambdalarni topib, nomlangan metodlarga chiqaring.
- [ ] Oqim ichida tashqi to'plamga yozadigan `forEach` larni `map`/`collect` ga o'tkazing.
- [ ] `peek` ishlatilgan joylarni mantiqdan olib tashlang yoki log uchun oshkor metodga aylantiring.
- [ ] `parallelStream` chaqiruvlarini ko'rib, I/O bo'lsa oshkor executor ga, o'lchovsiz bo'lsa ketma-ket oqimga qaytaring.
- [ ] `isPresent()` + `get()` namunalarini `map`/`orElseGet`/`orElseThrow` zanjiriga aylantiring.
- [ ] `orElse(<qimmat chaqiruv>)` holatlarini `orElseGet` ga o'tkazing.
- [ ] `@SneakyThrows` ishlatilgan joylarni oshkor o'rashga almashtirib, annotatsiyani taqiqlang.
- [ ] Ikki darajadan chuqur `groupingBy` zanjirlarini oraliq record bilan tekislang.
## 25. Java kodidagi umumiy tuzoqlar (Common Java Pitfalls)

Bu bob oldingi boblarga sig'magan, lekin kundalik kodda uchraydigan Java tuzoqlarini yig'adi: `Optional` ning chegaralari, statik ishga tushirish, seriyalash, refleksiya, ichki sinflar, enum mexanikasi va kompilyator ogohlantirishlari.

### 25.1 `Optional` maydon, parametr va seriyalash

`Optional` qaytish qiymati uchun mo'ljallangan. Maydon sifatida ishlatish uch muammo keltiradi: `Optional` `Serializable` emas, har bir obyekt uchun qo'shimcha o'ram yaratiladi, va JPA/Jackson bilan muammo chiqadi.

```java
// yomon: Optional maydon
public class Order {
    private Optional<Discount> discount;      // Serializable emas, JPA bilan ishlamaydi
}

// yaxshi: maydon null bo'lishi mumkin, getter Optional qaytaradi
public class Order {

    private Discount discount;                // null bo'lishi mumkin

    public Optional<Discount> discount() { return Optional.ofNullable(discount); }
}

// yomon: Optional parametr - chaqiruv joyi shovqinli
void apply(Order order, Optional<Discount> discount);
apply(order, Optional.empty());

// yaxshi: overload (5.9)
void apply(Order order);
void apply(Order order, Discount discount);
```

### 25.2 Statik ishga tushirish tartibi va sinf yuklanishi

Statik initializator (`static { }`) sinf birinchi marta ishlatilganda bajariladi va uning vaqti oldindan aniq emas. Agar unda tashqi resursga murojaat bo'lsa (fayl, baza, tarmoq), xato kutilmagan joyda `ExceptionInInitializerError` sifatida chiqadi va diagnostikasi qiyin bo'ladi.

```java
// yomon: statik blokda I/O - xato ExceptionInInitializerError bo'lib chiqadi
public class TaxRates {
    private static final Map<Region, BigDecimal> RATES;
    static {
        RATES = loadFromDatabase();      // qachon bajariladi - aniq emas
    }
}

// yaxshi: yuklash oshkor, boshqariladigan joyda (Spring bean, lazy supplier)
@Component
public class TaxRates {

    private final Map<Region, BigDecimal> rates;

    TaxRates(TaxRateRepository repository) {
        this.rates = Map.copyOf(repository.loadAll());    // konteyner boshqaradi
    }
}
```

Statik maydonlarning ishga tushish tartibi e'lon tartibida boradi va bu tartibga bog'lanish nozik xato beradi: pastda e'lon qilingan maydon yuqoridagi initializatorda `null` bo'ladi.

### 25.3 `instanceof` zanjiri va `getClass()` solishtirish

Uzun `instanceof` zanjiri turga qarab shoxlanish hidi (6.10) va zamonaviy Java da uning to'g'ri shakli bor: `sealed` interfeys va pattern matching bilan `switch`, bunda to'liqlik kompilyator tomonidan tekshiriladi (arxitektor hujjati 13.2).

```java
// yomon: zanjir, to'liqligi tekshirilmaydi
if (event instanceof PaymentSettled s) { ... }
else if (event instanceof PaymentRejected r) { ... }
else { throw new IllegalStateException("noma'lum hodisa"); }

// yaxshi: sealed + switch - yangi tur qo'shilsa kompilyator eslatadi
sealed interface PaymentEvent permits PaymentSettled, PaymentRejected, PaymentRefunded { }

String describe(PaymentEvent event) {
    return switch (event) {
        case PaymentSettled s -> "yopildi: " + s.amount();
        case PaymentRejected r -> "rad etildi: " + r.reason();
        case PaymentRefunded f -> "qaytarildi: " + f.amount();
    };
}
```

### 25.4 Seriyalash: `serialVersionUID`, `readObject` va undan qochish

Java seriyalash mexanizmi (`Serializable`) xavfsizlik nuqsonlari va moslik muammolari manbai: deseriyalash konstruktorni chetlab o'tadi (invariant tekshirilmaydi), va ishonchsiz ma'lumotni deseriyalash masofadan kod bajarilishiga olib keladi.

Qoida: yangi kodda `Serializable` ishlatmaslik. Ma'lumot almashish uchun JSON yoki Protobuf; kesh uchun ham seriyalanadigan format tanlanadi.

```java
// Agar Serializable majbur bo'lsa (legacy, RMI, HttpSession):
public final class SessionData implements Serializable {

    // Versiya oshkor: aks holda sinf o'zgarganda deseriyalash buziladi
    private static final long serialVersionUID = 1L;

    // Sezgir maydon seriyalanmaydi
    private transient String accessToken;

    // Invariant deseriyalashdan keyin ham tekshiriladi
    private void readObject(ObjectInputStream in) throws IOException, ClassNotFoundException {
        in.defaultReadObject();
        if (userId == null) throw new InvalidObjectException("userId bo'sh");
    }
}
```

### 25.5 Refleksiya narxi va uni chegaralash

Refleksiya tur xavfsizligini ish vaqtiga suradi: xato kompilyatsiyada emas, production da chiqadi. Bundan tashqari, refleksiya bilan yozilgan kod refaktoringga chidamsiz — nom o'zgarsa IDE uni topmaydi.

```java
// yomon: nom satrda - refaktoring buzadi, xato ish vaqtida chiqadi
Method method = service.getClass().getMethod("settle", Long.class);
method.invoke(service, paymentId);

// yaxshi: interfeys yoki funksional tur
PaymentOperation operation = service::settle;
operation.apply(paymentId);
```

Refleksiya haqli joylar: framework ichida (Spring, Jackson, JPA), test yordamchilarida, va plugin yuklashda. Biznes kodida esa deyarli har doim boshqa yechim bor.

### 25.6 `finalize`, `Cleaner` va resurs oxiri

`Object.finalize()` Java 9 dan deprecated va Java 18 dan o'chirilish yo'lida: uning bajarilishi kafolatlanmaydi, vaqti aniq emas, va GC ni sekinlashtiradi. `Cleaner` esa faqat **oxirgi himoya** sifatida haqli.

Qoida: resursni `AutoCloseable` va `try-with-resources` bilan boshqarish (19.4); `Cleaner` ni faqat native resurs (JNI buferi) uchun qo'shimcha xavfsizlik to'ri sifatida ishlatish.

### 25.7 Ichki sinf va yashirin tashqi havola

Nostatik ichki sinf (`inner class`) tashqi sinf nusxasiga yashirin havola saqlaydi. Natijada ichki sinf nusxasi yashasa, tashqi obyekt ham xotirada qoladi — bu klassik xotira oqishi (memory leak) sababi.

```java
// yomon: Listener tashqi Service ga havola saqlaydi, u GC qilinmaydi
public class SettlementService {
    class Listener implements EventListener { ... }       // nostatik
}

// yaxshi: statik ichki sinf - yashirin havola yo'q
public class SettlementService {
    static final class Listener implements EventListener { ... }
}
```

Qoida: ichki sinf tashqi nusxaga murojaat qilmasa, u `static` bo'lishi kerak. Bu qoidani Error Prone `ClassCanBeStatic` qoidasi topadi.

### 25.8 Anonim sinf va lambda tanlovi

Lambda qisqa va `this` ni tashqi sinfga bog'laydi; anonim sinf esa o'z `this` iga ega va holat saqlashi mumkin. Tanlov qoidasi oddiy.

| Ehtiyoj | Tanlov |
|---|---|
| Bitta abstrakt metod, holat yo'q | lambda |
| Bir nechta metod | anonim sinf yoki nomlangan sinf |
| Holat kerak | nomlangan sinf |
| `this` o'ziga tegishli bo'lishi kerak | anonim sinf |
| Qayta ishlatiladi | nomlangan sinf |
| Uch qatordan uzun | nomlangan metod yoki sinf (24.1) |

### 25.9 `enum` da xatti-harakat, `EnumMap`, `EnumSet`, `valueOf`

Enum Java da oddiy konstanta to'plamidan ancha ko'proq: u xatti-harakat saqlashi mumkin (6.10) va o'ziga mos to'plamlari bor.

`EnumMap` va `EnumSet` oddiy `HashMap`/`HashSet` dan tez va kam xotira oladi, chunki ular massivga asoslangan. Enum kalit ishlatilganda ularni tanlash standart bo'lishi kerak.

```java
// yaxshi: EnumMap - tartib enum e'loni bo'yicha, tez
Map<SettlementStatus, Long> counts = new EnumMap<>(SettlementStatus.class);
Set<SettlementStatus> terminal = EnumSet.of(SETTLED, REJECTED);
```

`valueOf` tuzog'i: noma'lum nom uchun `IllegalArgumentException` tashlaydi va bu tashqi ma'lumotni parslaganda kutilmagan 500 xatoga olib keladi.

```java
// yomon: tashqi qiymat uchun IllegalArgumentException
SettlementStatus status = SettlementStatus.valueOf(input);

// yaxshi: xavfsiz parslash
static Optional<SettlementStatus> parse(String input) {
    return Arrays.stream(values())
            .filter(s -> s.name().equalsIgnoreCase(input))
            .findFirst();
}
```

### 25.10 Kompilyator ogohlantirishlari: `-Xlint`, `-Werror`, Error Prone, NullAway

Kompilyator eng arzon statik tahlilchi va u ko'pincha o'chirilgan holda qoldiriladi. Ogohlantirishlarni xatoga aylantirish eng yuqori foyda beradigan bir martalik sozlama.

```xml
<plugin>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <!-- Barcha ogohlantirishlar yoqilgan va xatoga aylantirilgan -->
      <arg>-Xlint:all</arg>
      <arg>-Werror</arg>
      <!-- Parametr nomlari saqlanadi: Spring va Jackson uchun kerak -->
      <arg>-parameters</arg>
      <!-- Error Prone va NullAway ulanishi -->
      <arg>-XDcompilePolicy=simple</arg>
      <arg>--should-stop=ifError=FLOW</arg>
      <arg>-Xplugin:ErrorProne -Xep:NullAway:ERROR -XepOpt:NullAway:AnnotatedPackages=uz.shop</arg>
    </compilerArgs>
    <annotationProcessorPaths>
      <path>
        <groupId>com.google.errorprone</groupId>
        <artifactId>error_prone_core</artifactId>
        <version>2.42.0</version>
      </path>
      <path>
        <groupId>com.uber.nullaway</groupId>
        <artifactId>nullaway</artifactId>
        <version>0.12.10</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

Error Prone bu hujjatdagi ko'p qoidalarni avtomatik tekshiradi: `EqualsHashCode`, `Finally`, `ClassCanBeStatic`, `StringSplitter`, `DefaultCharset`, `JavaUtilDate`, `BigDecimalEquals`, `UnusedVariable` (42.2).

### 25.11 Amalda qo'llash

- [ ] `Optional` tipidagi maydon va parametrlarni topib, maydonni `null` ga va getter ni `Optional` ga o'tkazing.
- [ ] Statik initializator ichidagi I/O va tashqi chaqiruvlarni bean konstruktoriga yoki lazy supplier ga ko'chiring.
- [ ] Uzun `instanceof` zanjirlarini `sealed` interfeys va `switch` pattern matching ga o'tkazing.
- [ ] `Serializable` ishlatilgan joylarni ro'yxatlab, yangi kodda taqiqlang; qolganlarida `serialVersionUID` va `transient` ni tekshiring.
- [ ] Biznes kodidagi refleksiyani interfeys yoki funksional turga almashtiring.
- [ ] Nostatik ichki sinflarni `static` qilib, Error Prone `ClassCanBeStatic` ni yoqing.
- [ ] `Enum.valueOf` tashqi ma'lumot bilan chaqirilgan joylarni xavfsiz parslashga o'tkazing.
- [ ] `-Xlint:all -Werror` va Error Prone + NullAway ni build ga qo'shib, chiqqan ogohlantirishlarni bosqichma-bosqich tuzating.
# VIII. Spring va ma'lumot qatlamida toza kod

## 26. Spring kodining tozaligi (Clean Code in Spring)

Spring mexanikasi arxitektor hujjatida (15-20 boblar), Spring patternlari esa patternlar hujjatida. Bu bobda Spring kodining **yozilish** qoidalari: inyeksiya shakli, bean ko'rinishi, konfiguratsiya, controller va service chegarasi, Lombok siyosati.

### 26.1 Konstruktor inyeksiyasi va `final` maydon

Maydonga inyeksiya (`@Autowired` maydonda) patternlar hujjatida anti-pattern sifatida sanalgan (25.29). Bu yerda to'g'ri shaklning aniq ko'rinishi: konstruktor inyeksiyasi, `final` maydon, `@Autowired` siz.

```java
// yaxshi: bitta konstruktor - @Autowired kerak emas (Spring 4.3+)
@Service
public class SettlementService {

    private final PaymentGateway gateway;
    private final PaymentRepository payments;
    private final Clock clock;

    SettlementService(PaymentGateway gateway, PaymentRepository payments, Clock clock) {
        this.gateway = gateway;
        this.payments = payments;
        this.clock = clock;
    }
}
```

Konstruktor inyeksiyasi to'rt foyda beradi: maydonlar `final` bo'ladi (16.1), bog'liqliklar imzoda ko'rinadi, obyekt `new` bilan testda yaratiladi (framework kerak emas), va aylanali bog'liqlik ishga tushishda darhol aniqlanadi.

Bog'liqliklar soni to'rtdan oshsa, bu sinfning juda ko'p ish qilayotgani belgisi — konstruktor parametr soni tabiiy ogohlantirish beradi (5.1).

### 26.2 Bean ko'rinishi: `package-private` konfiguratsiya va komponentlar

Spring beanlari `public` bo'lishi shart emas va `package-private` qilish paket chegarasini mustahkamlaydi (arxitektor hujjati 4.8 va 5.9). Shunda boshqa paketdan tasodifiy import qilib bo'lmaydi.

```java
// yaxshi: faqat API public, implementatsiya paket ichida
public interface PaymentApi {           // paketdan chiqadigan yagona tur
    SettlementResult settle(PaymentId id);
}

@Service
class DefaultPaymentApi implements PaymentApi { ... }    // package-private

@Configuration(proxyBeanMethods = false)
class PaymentConfiguration {                              // package-private

    @Bean
    PaymentGateway paymentGateway(PaymentProperties properties) { ... }
}
```

`proxyBeanMethods = false` konfiguratsiya sinfini proxy qilishni o'chiradi: bu tezroq ishga tushishni beradi va `@Bean` metodlari orasidagi yashirin chaqiruvlarni taqiqlaydi (ular oshkor parametr orqali uzatilishi kerak).

### 26.3 Konfiguratsiya: `@ConfigurationProperties` record bilan

`@Value` ni kod bo'ylab tarqatish property tarqoqligiga olib keladi (patternlar hujjati 25.53): sozlamalar ro'yxati hech qayerda to'liq ko'rinmaydi, validatsiya yo'q, va standart qiymatlar takrorlanadi.

```java
// yomon: tarqoq, validatsiyasiz, birligi noaniq
@Value("${shop.payment.timeout:5000}")
private long timeout;

// yaxshi: bir joyda, tipik, validatsiyalangan, birlik turda (3.3)
@ConfigurationProperties("shop.payment")
@Validated
record PaymentProperties(
        @NotNull URI gatewayUrl,
        @NotNull @DurationMin(seconds = 1) @DurationMax(seconds = 30) Duration timeout,
        @Min(0) @Max(5) int maxRetries,
        @NotBlank String merchantId) {

    // Standart qiymatlar bir joyda, kompakt konstruktorda
    PaymentProperties {
        timeout = timeout != null ? timeout : Duration.ofSeconds(5);
    }
}
```

`record` bilan ishlatish uchun `@EnableConfigurationProperties` yoki `@ConfigurationPropertiesScan` kerak, va konstruktor bog'lanishi avtomatik ishlaydi.

### 26.4 Konfiguratsiyani validatsiya qilish va tez to'xtash

Noto'g'ri konfiguratsiya ishga tushishda aniqlanishi kerak, birinchi so'rovda emas. `@Validated` bilan birga Spring Boot ishga tushishni to'xtatadi va aniq xato beradi.

```yaml
# application.yml - har bir kalit prefiks bilan, birligi ko'rinadi (3.13)
shop:
  payment:
    gateway-url: https://gateway.example.uz
    timeout: 5s          # Duration formati
    max-retries: 3
    merchant-id: ${MERCHANT_ID}      # sir muhitdan keladi, kodda emas
```

Ikkinchi qoida: sirlar (`password`, `token`, `secret`) hech qachon `application.yml` da literal sifatida turmaydi — ular muhit o'zgaruvchisi yoki secret manager dan keladi (39.8).

### 26.5 Controller ni yupqa ushlash

Semiz controller patternlar hujjatida anti-pattern (25.34). Clean code darajasida controller metodining aniq vazifasi bor va u uch qatordan oshmaydi: kirishni domen turiga aylantirish, use case ni chaqirish, natijani javobga aylantirish.

```java
// yomon: biznes mantiqi controller da
@PostMapping("/refunds")
ResponseEntity<?> refund(@RequestBody Map<String, Object> body) {
    Long paymentId = Long.valueOf(body.get("paymentId").toString());
    Payment payment = repository.findById(paymentId).orElse(null);
    if (payment == null) return ResponseEntity.notFound().build();
    if (!"SETTLED".equals(payment.getStatus())) return ResponseEntity.badRequest().build();
    ...
}

// yaxshi: yupqa, mantiq service da, xato ishlovi markazda (27.3)
@PostMapping("/refunds")
@ResponseStatus(HttpStatus.CREATED)
RefundResponse refund(@Valid @RequestBody RefundRequest request) {
    Refund refund = refunds.create(request.toCommand());
    return RefundResponse.from(refund);
}
```

### 26.6 DTO va domen o'rtasidagi mapping joyi

Mapping qayerda turishi aniq qaror bo'lishi kerak, aks holda u hamma joyda takrorlanadi. Uchta ishlaydigan joy bor va ularning tanlovi loyiha hajmiga bog'liq.

| Joy | Qachon | Shakli |
|---|---|---|
| DTO ichida statik fabrika | kichik va o'rta loyiha | `RefundResponse.from(refund)` |
| Alohida mapper sinfi | mapping murakkab, qoida bor | `RefundMapper` (`@Component`) |
| MapStruct | DTO ko'p, maydonlar bir xil | generatsiya, `@Mapper` |
| Domen ichida | hech qachon | domen DTO ni bilmasligi kerak |

Qoida: domen obyekti DTO ni bilmaydi (bog'liqlik yo'nalishi, arxitektor hujjati 5.8); shuning uchun mapping DTO tomonda yoki alohida sinfda turadi.

### 26.7 Service qatlamida metod nomlari va tranzaksiya chegarasi

Service metodlari **use case** nomini olishi kerak, CRUD nomini emas: `cancelOrder`, `reserveStock`, `settlePayment` — `update`, `process`, `handle` emas (2.4 va 3.9).

Tranzaksiya chegarasi va `@Transactional` mexanikasi arxitektor hujjatida (19-bob) berilgan. Clean code darajasidagi ikki qoida: `@Transactional` service qatlamida turadi (controller yoki repository da emas), va `readOnly = true` o'qish metodlarida oshkor belgilanadi.

```java
@Service
class DefaultRefundService implements RefundService {

    @Override
    @Transactional                                  // yozish: standart
    public Refund create(RefundCommand command) { ... }

    @Override
    @Transactional(readOnly = true)                 // o'qish: oshkor
    public Page<RefundSummary> search(RefundCriteria criteria, Pageable pageable) { ... }
}
```

### 26.8 `@Qualifier`, `@Primary` va bean nomlari

Bir interfeysning bir nechta implementatsiyasi bo'lganda tanlovni oshkor qilish kerak. `@Primary` yashirin tanlov beradi va u faqat haqiqiy "standart" bo'lganda haqli; qolgan hollarda `@Qualifier` yoki alohida tur aniqroq.

```java
// yomon: @Primary yashirin - qaysi bean inyeksiya qilinishi kodda ko'rinmaydi
@Service @Primary class StripeGateway implements PaymentGateway { }
@Service class SandboxGateway implements PaymentGateway { }

// yaxshi: tanlov oshkor va nomlangan
@Service @Qualifier("stripe") class StripeGateway implements PaymentGateway { }

SettlementService(@Qualifier("stripe") PaymentGateway gateway) { ... }

// eng yaxshi: konfiguratsiya tanlaydi, kod bitta turni ko'radi
@Bean
PaymentGateway paymentGateway(PaymentProperties properties, ...) {
    return switch (properties.provider()) {
        case STRIPE -> new StripeGateway(...);
        case SANDBOX -> new SandboxGateway(...);
    };
}
```

### 26.9 Shartli konfiguratsiya va `@Profile` ni kamaytirish

Profil tarqoqligi patternlar hujjatida anti-pattern (25.39). Clean code qoidasi: `@Profile` ni **kod** da emas, konfiguratsiyada hal qilish — xatti-harakat farqi property qiymati bilan boshqarilsa, muhitlar orasidagi farq bir faylda ko'rinadi.

```java
// yomon: profil kod bo'ylab tarqalgan, nima farq qilishi ko'rinmaydi
@Service @Profile("!prod") class FakeSmsSender implements SmsSender { }
@Service @Profile("prod") class RealSmsSender implements SmsSender { }

// yaxshi: xususiyat bayrog'i konfiguratsiyada, bitta joyda ko'rinadi
@Bean
@ConditionalOnProperty(name = "shop.sms.mode", havingValue = "real")
SmsSender realSmsSender(SmsProperties properties) { ... }

@Bean
@ConditionalOnMissingBean(SmsSender.class)
SmsSender loggingSmsSender() { ... }
```

### 26.10 Lombok siyosati: xavfsiz va xavfli annotatsiyalar

Lombok kodni qisqartiradi, lekin ba'zi annotatsiyalari yashirin xatti-harakat qo'shadi. Jamoada aniq siyosat bo'lishi kerak va u hujjatlashtirilishi lozim (SonarQube hujjati 41-bobda Lombok va generatsiya qilingan kod ko'rib chiqiladi).

| Annotatsiya | Siyosat | Sabab |
|---|---|---|
| `@Getter` | ruxsat | shaffof |
| `@RequiredArgsConstructor` | ruxsat (26.1 bilan) | konstruktor inyeksiyasi |
| `@Builder` | ruxsat, validatsiya bilan (16.5) | majburiy maydonlar tekshirilmaydi |
| `@Slf4j` | ruxsat | standart logger |
| `@Value` (Lombok) | ehtiyotkorlik | `record` afzal |
| `@Data` | **taqiqlangan** | setter + `equals` + `toString` birga |
| `@EqualsAndHashCode` entitetda | **taqiqlangan** | assotsiatsiyalarni yuklaydi (28.1) |
| `@ToString` entitetda | **taqiqlangan** | lazy yuklash, sezgir ma'lumot (15.7) |
| `@SneakyThrows` | **taqiqlangan** | istisno imzodan yashiriladi (24.7) |
| `@Setter` domenda | taqiqlangan | inkapsulyatsiyani buzadi (16.7) |

### 26.11 Amalda qo'llash

- [ ] Barcha maydon inyeksiyalarini (`@Autowired` maydonda) konstruktor inyeksiyasiga o'tkazib, maydonlarni `final` qiling.
- [ ] Beanlar va konfiguratsiya sinflarini `package-private` qilib, paketdan faqat API turlarini chiqaring.
- [ ] `@Value` chaqiruvlarini `@ConfigurationProperties` record larga birlashtirib, `@Validated` qo'shing.
- [ ] Konfiguratsiya kalitlarida birlik va prefiks borligini tekshirib, sirlarni muhit o'zgaruvchisiga ko'chiring.
- [ ] Controller metodlarini uch qatorga qisqartirib, biznes mantiqini service ga ko'chiring.
- [ ] Mapping joyini bitta konvensiyaga keltirib (DTO fabrikasi yoki mapper), takrorlangan mappinglarni birlashtiring.
- [ ] `@Primary` ishlatilgan joylarni `@Qualifier` yoki konfiguratsiyadagi oshkor tanlovga almashtiring.
- [ ] Lombok siyosatini yozib, `@Data`, `@SneakyThrows` va entitetdagi `@EqualsAndHashCode` ni ArchUnit bilan taqiqlang.
## 27. REST API kodining o'qilishi (Readable REST Code)

API dizayn patternlari patternlar hujjatida (7-bob), REST so'rov yo'li arxitektor hujjatida (17-bob). Bu bobda controller **kodining** tozaligi: imzo, holat kodi, xato javobi, validatsiya, seriyalash sozlamalari va idempotentlik.

### 27.1 Controller metodi imzosi va qaytish turi

Controller imzosi API shartnomasini ko'rsatishi kerak. `ResponseEntity<?>` va `Map<String, Object>` ikkisi ham shartnomani yashiradi: o'quvchi javob shaklini kod ichidan izlaydi.

```java
// yomon: shartnoma ko'rinmaydi
@PostMapping("/orders")
ResponseEntity<?> create(@RequestBody Map<String, Object> body) { ... }

// yaxshi: kirish va chiqish turlari oshkor, holat kodi annotatsiyada
@PostMapping("/orders")
@ResponseStatus(HttpStatus.CREATED)
OrderResponse create(@Valid @RequestBody CreateOrderRequest request) { ... }

// ResponseEntity faqat sarlavha yoki holat kodi dinamik bo'lganda
@PostMapping("/orders")
ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest request) {
    Order order = orders.place(request.toCommand());
    return ResponseEntity.created(locationOf(order)).body(OrderResponse.from(order));
}
```

### 27.2 HTTP holat kodini bitta joyda qaror qilish

Holat kodi mantiqi controller lar bo'ylab tarqalsa, bir xil xato turli endpointlarda turli kod bilan qaytadi. Yechim: holat kodini **istisno turiga** bog'lash va bitta joyda belgilash.

| Holat | Kod |
|---|---|
| Yaratildi | 201 + `Location` |
| Muvaffaqiyatli, javob yo'q | 204 |
| Validatsiya xatosi | 400 |
| Autentifikatsiya yo'q | 401 |
| Ruxsat yo'q | 403 |
| Topilmadi | 404 |
| Konflikt (idempotentlik, versiya) | 409 |
| Biznes qoidasi buzildi | 422 |
| Juda ko'p so'rov | 429 |
| Ichki xato | 500 |
| Tashqi tizim javob bermadi | 502 / 504 |

### 27.3 Xato javobi formati: `ProblemDetail` va `@ExceptionHandler`

Hammasini tutuvchi exception handler patternlar hujjatida anti-pattern (25.41). To'g'ri shakl: har bir istisno turiga aniq ishlov, bitta `@RestControllerAdvice` da, RFC 9457 (`ProblemDetail`) formatida.

```java
@RestControllerAdvice
class ApiExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);

    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail handleNotFound(OrderNotFoundException e) {
        // 404 - log kerak emas: bu normal holat
        return problem(HttpStatus.NOT_FOUND, e.code(), e.getMessage());
    }

    @ExceptionHandler(DomainRuleViolationException.class)
    ProblemDetail handleRule(DomainRuleViolationException e) {
        // 422 - biznes qoidasi; WARN yetarli
        log.warn("biznes qoidasi buzildi: {}", e.code());
        return problem(HttpStatus.UNPROCESSABLE_ENTITY, e.code(), e.getMessage());
    }

    @ExceptionHandler(GatewayUnavailableException.class)
    ProblemDetail handleGateway(GatewayUnavailableException e) {
        log.error("tashqi gateway javob bermadi", e);        // 19.7: log bir joyda
        return problem(HttpStatus.BAD_GATEWAY, e.code(), "To'lov tizimi vaqtincha ishlamayapti");
    }

    private ProblemDetail problem(HttpStatus status, String code, String detail) {
        ProblemDetail problem = ProblemDetail.forStatusAndDetail(status, detail);
        problem.setProperty("code", code);                   // barqaror kod (19.11)
        problem.setProperty("traceId", MDC.get("traceId"));  // diagnostika uchun
        return problem;
    }
}
```

Muhim qoida: xato javobida ichki sinf nomi, stack trace yoki SQL bo'lmasligi kerak (19.10).

### 27.4 Validatsiya: `@Valid`, guruhlar, maxsus validator

Validatsiya chegarada bo'ladi (5.11) va Bean Validation uning standart vositasi. Uch qoida: xabarlar kalitlar orqali lokalizatsiya qilinadi, guruhlar faqat haqiqatan kerak bo'lganda ishlatiladi, va murakkab qoidalar maxsus validator ga chiqadi.

```java
record CreateOrderRequest(
        @NotNull CustomerId customerId,
        @NotEmpty @Size(max = 100) List<@Valid OrderLineRequest> lines,
        @Pattern(regexp = "[A-Z]{3}") String currency) {

    OrderCommand toCommand() { ... }
}

// Maydonlar orasidagi qoida: maxsus validator (bitta maydonga bog'lanmaydi)
@Documented
@Constraint(validatedBy = DateRangeValidator.class)
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface ValidDateRange {
    String message() default "{shop.validation.date-range}";
    Class<?>[] groups() default { };
    Class<? extends Payload>[] payload() default { };
}
```

Validatsiya xatolarini bir xil formatda qaytarish kerak: maydon nomi, kod, xabar.

```java
@ExceptionHandler(MethodArgumentNotValidException.class)
ProblemDetail handleValidation(MethodArgumentNotValidException e) {
    ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
    problem.setProperty("errors", e.getFieldErrors().stream()
            .map(f -> Map.of("field", f.getField(), "message", f.getDefaultMessage()))
            .toList());
    return problem;
}
```

### 27.5 Sahifalash, saralash va filtr parametrlari

Sahifalanmagan ro'yxat endpointi har doim kelajakdagi incident: ma'lumot o'sadi va javob vaqti bilan birga xotira ham oshadi. Qoida: ro'yxat qaytaradigan har bir endpoint sahifalangan bo'ladi va maksimal hajm cheklanadi.

```java
@GetMapping("/orders")
Page<OrderSummary> search(
        @Valid OrderCriteria criteria,
        @PageableDefault(size = 20, sort = "createdAt", direction = Sort.Direction.DESC)
        Pageable pageable) {
    return orders.search(criteria, pageable);
}
```

```yaml
spring:
  data:
    web:
      pageable:
        max-page-size: 100        # klient 10000 so'rasa ham 100 bilan cheklanadi
        default-page-size: 20
        one-indexed-parameters: false
```

Saralash maydonlarini oq ro'yxat bilan cheklash kerak: tashqi `sort` parametri to'g'ridan-to'g'ri SQL ga tushsa, indekssiz ustun bo'yicha saralash bazani yuklaydi.

### 27.6 Seriyalash sozlamalari: Jackson, `null`, sana formati

Jackson sozlamalari bir joyda, oshkor bo'lishi kerak; aks holda javob shakli standart qiymatlarga bog'lanib qoladi va versiya yangilanganda o'zgaradi.

```yaml
spring:
  jackson:
    default-property-inclusion: non_null    # null maydonlar javobda yo'q
    serialization:
      write-dates-as-timestamps: false      # ISO-8601 (22.9)
      fail-on-empty-beans: true
    deserialization:
      fail-on-unknown-properties: true      # klient xatosi jim o'tmaydi
      fail-on-null-for-primitives: true
    time-zone: UTC
```

Qo'shimcha qoidalar: JPA entitetini API da qaytarmaslik (patternlar hujjati 25.33), `@JsonIgnore` bilan sezgir maydonlarni yopish, va DTO maydonlari nomini API shartnomasida barqaror ushlash.

### 27.7 Idempotentlik va `Idempotency-Key` kodda

Yaratish amallari (`POST`) takrorlanishi mumkin: klient timeout dan keyin qayta yuboradi. Idempotentlik kaliti shu takrorlanishni xavfsiz qiladi va u kodda ko'rinadigan bo'lishi kerak.

```java
@PostMapping("/refunds")
RefundResponse refund(
        @RequestHeader("Idempotency-Key") @NotBlank String idempotencyKey,
        @Valid @RequestBody RefundRequest request) {
    return RefundResponse.from(refunds.create(request.toCommand(), IdempotencyKey.of(idempotencyKey)));
}
```

Kalit server tomonda **generatsiya qilinmaydi** (20.8): u klientdan keladi, bazada unikal cheklov bilan saqlanadi (3.13 dagi `uq_payment_idempotency_key`), va takroriy so'rov oldingi natijani qaytaradi.

### 27.8 API versiyasi kodda qanday ko'rinadi

Versiyalash strategiyasi API dizayn masalasi, lekin kod tuzilishi unga mos bo'lishi kerak: ikki versiya bir controller da yashamasligi kerak.

```java
// yomon: ikki versiya bir sinfda, shartlar bilan
@GetMapping("/orders")
Object list(@RequestParam(defaultValue = "1") int version) {
    if (version == 2) return v2Response();
    return v1Response();
}

// yaxshi: har bir versiya o'z controlleri va DTO lari bilan
@RestController @RequestMapping("/api/v1/orders")
class OrderV1Controller { ... }

@RestController @RequestMapping("/api/v2/orders")
class OrderV2Controller { ... }
// Ikkisi ham bir xil service ni chaqiradi: mantiq takrorlanmaydi
```

### 27.9 Amalda qo'llash

- [ ] `ResponseEntity<?>` va `Map<String, Object>` qaytaradigan controller metodlarini aniq DTO turlariga o'tkazing.
- [ ] Holat kodi mantiqini controller lardan `@RestControllerAdvice` ga ko'chirib, 27.2 jadvaliga moslang.
- [ ] Xato javoblarini `ProblemDetail` formatiga keltirib, barqaror `code` va `traceId` qo'shing.
- [ ] Hammasini tutuvchi `@ExceptionHandler(Exception.class)` ni aniq turlarga bo'ling.
- [ ] Barcha ro'yxat endpointlarini sahifalangan qilib, `max-page-size` ni sozlang.
- [ ] Saralash maydonlarini oq ro'yxat bilan cheklab, indekssiz ustunlarni chiqarib tashlang.
- [ ] Jackson sozlamalarini `application.yml` da oshkor yozib, sana formatini ISO-8601 ga qotiring.
- [ ] Yaratish endpointlariga `Idempotency-Key` sarlavhasini va bazada unikal cheklovni qo'shing.
## 28. JPA va SQL kodining tozaligi (Clean JPA and SQL)

Hibernate mexanikasi va PostgreSQL chuqur bilimi arxitektor hujjatida (18, 21-27 boblar), ORM patternlari patternlar hujjatida (9-bob). Bu bobda ma'lumot qatlami **kodining** tozaligi: entitet gigiyenasi, assotsiatsiyalar, repository metodlari, SQL yozish uslubi.

### 28.1 Entitet gigiyenasi: `equals`, `hashCode`, `toString`

JPA entiteti uchun tenglik qoidalari oddiy obyektdan farq qiladi (15.4-15.5): identifikator bo'yicha tenglik, barqaror `hashCode`, va proxy bilan ishlaydigan `instanceof`.

```java
@Entity
@Table(name = "payment")
public class Payment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        // Hibernate proxy uchun instanceof kerak, getClass() emas
        if (!(o instanceof Payment other)) return false;
        // id null bo'lsa (hali saqlanmagan) obyektlar faqat o'ziga teng
        return id != null && id.equals(other.id);
    }

    @Override
    public int hashCode() {
        // Barqaror: id tayinlanganda ham hash o'zgarmaydi (15.9)
        return Payment.class.hashCode();
    }

    @Override
    public String toString() {
        // Faqat skalyar maydonlar: lazy assotsiatsiya yuklanmaydi (15.7)
        return "Payment{id=%s, amount=%s, status=%s}".formatted(id, amount, status);
    }
}
```

### 28.2 Lombok va entitet: nimani ishlatmaslik

Lombok ning ba'zi annotatsiyalari entitetda nozik xato beradi va ularning hammasi 26.10 siyosatida taqiqlangan. Sabablarini bilish muhim, chunki xato jim o'tadi.

| Annotatsiya | Entitetda nima bo'ladi |
|---|---|
| `@Data` | setter + `equals`/`hashCode` barcha maydonlardan: lazy yuklash va noto'g'ri tenglik |
| `@EqualsAndHashCode` | assotsiatsiyalarni `equals` ga qo'shadi: butun grafni yuklaydi |
| `@ToString` | lazy kolleksiyalarni yuklaydi yoki `LazyInitializationException` beradi |
| `@Builder` | `@NoArgsConstructor` ni yo'qotadi: Hibernate entitetni yarata olmaydi |
| `@AllArgsConstructor` | maydon tartibi o'zgarsa jim xato |
| `@Setter` | invariantni buzadi (16.7) |
| `@Getter` | xavfsiz |
| `@NoArgsConstructor(access = PROTECTED)` | xavfsiz va kerakli |

### 28.3 Assotsiatsiya yordamchi metodlari va ikki tomonlilik

Ikki tomonli assotsiatsiyada ikki tomonni qo'lda sinxron ushlash kerak, aks holda xotiradagi obyekt grafi bazadagi holatga mos kelmaydi. Yechim: yordamchi metod va to'g'ridan-to'g'ri kolleksiyaga kirishni yopish (14.7).

```java
@Entity
public class Order {

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private final List<OrderLine> lines = new ArrayList<>();

    // Yordamchi metod ikki tomonni birga ushlaydi
    public void addLine(OrderLine line) {
        lines.add(line);
        line.setOrder(this);
    }

    public void removeLine(OrderLine line) {
        lines.remove(line);
        line.setOrder(null);
    }

    // Tashqariga o'zgartirilmas ko'rinish
    public List<OrderLine> lines() { return Collections.unmodifiableList(lines); }
}
```

Qo'shimcha qoida: ikki tomonli assotsiatsiya faqat haqiqatan kerak bo'lganda qo'yiladi. Bir tomonli `@ManyToOne` ko'pincha yetarli va ancha kam muammo beradi.

### 28.4 `fetch`, `cascade`, `orphanRemoval` ni oshkor yozish

Standart `fetch` qiymatlari xavfli: `@ManyToOne` va `@OneToOne` standart holatda `EAGER`, ya'ni har bir so'rov butun grafni tortadi. Qoida: har bir assotsiatsiyada `fetch` oshkor yoziladi va u deyarli har doim `LAZY`.

```java
// yomon: standart EAGER - har bir Payment o'qilganda Order ham yuklanadi
@ManyToOne
private Order order;

// yaxshi: oshkor LAZY; kerak bo'lganda join fetch bilan olinadi
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "order_id", nullable = false)
private Order order;
```

`cascade` ham oshkor bo'lishi kerak: `CascadeType.ALL` `REMOVE` ni ham o'z ichiga oladi va bu kutilmagan o'chirishlarga olib keladi. Agregat ildizi va uning qismlari orasida `ALL` + `orphanRemoval` to'g'ri; mustaqil entitetlar orasida esa `cascade` umuman bo'lmasligi kerak.

| Munosabat | `cascade` | `orphanRemoval` |
|---|---|---|
| Agregat ildizi → qismi (`Order` → `OrderLine`) | `ALL` | `true` |
| Mustaqil entitetlar (`Payment` → `Customer`) | yo'q | `false` |
| Ko'pdan-ko'pga | `PERSIST`, `MERGE` | `false` |
| Audit yozuvi | yo'q | `false` |

### 28.5 Repository metod nomlari: derived query chegarasi

Spring Data derived query lari qisqa va o'qiladi, lekin faqat ma'lum uzunlikka qadar. `findByCustomerIdAndStatusInAndCreatedAtBetweenOrderByCreatedAtDesc` nomi chegarani oshib ketgan: uni o'qish SQL o'qishdan qiyin.

Qoida: metod nomi uch shartdan oshsa, `@Query` yoki Specification ga o'tish kerak.

```java
public interface PaymentRepository extends JpaRepository<Payment, Long> {

    // yaxshi: qisqa va o'qiladi
    Optional<Payment> findByIdempotencyKey(IdempotencyKey key);
    List<Payment> findByOrderId(Long orderId);

    // yomon: nom chegaradan oshgan
    // List<Payment> findByCustomerIdAndStatusInAndCreatedAtBetweenOrderByCreatedAtDesc(...)

    // yaxshi: @Query bilan oshkor, nomi niyatni aytadi
    @Query("""
            select p from Payment p
            where p.customerId = :customerId
              and p.status in :statuses
              and p.createdAt >= :from and p.createdAt < :toExclusive
            order by p.createdAt desc
            """)
    List<Payment> findRecentByCustomerAndStatus(
            @Param("customerId") CustomerId customerId,
            @Param("statuses") Set<SettlementStatus> statuses,
            @Param("from") Instant from,
            @Param("toExclusive") Instant toExclusive);
}
```

### 28.6 `@Query`, native query va ularni o'qiladigan ushlash

JPQL va native query uchun uch qoida bor. Birinchi, matn bloki ishlatish (12.9) — satr birlashtirish SQL ni o'qilmaydigan qiladi. Ikkinchi, nomlangan parametrlar (`:customerId`), pozitsion emas (`?1`). Uchinchi, parametrlarni **hech qachon** satr birlashtirish bilan qo'ymaslik (SQL injection).

```java
// yomon: SQL injection va o'qilmaydigan matn
@Query(value = "select * from payment where status = '" + status + "'", nativeQuery = true)

// yaxshi: parametr bog'langan, matn bloki, ustunlar sanalgan
@Query(value = """
        select p.id, p.amount, p.currency, p.settled_at
        from payment p
        where p.status = :status
          and p.settled_at >= :from
        """, nativeQuery = true)
List<PaymentRow> findSettledSince(@Param("status") String status, @Param("from") Instant from);
```

### 28.7 Projeksiya va DTO qaytarish

Butun entitetni o'qish kerak bo'lmasa, uni o'qimaslik kerak: projeksiya kamroq ustun oladi, lazy muammolarini yo'qotadi va entitetni tranzaksiyadan tashqariga chiqarmaydi (patternlar hujjati 25.33).

```java
// yaxshi: interfeys projeksiyasi - Spring Data o'zi amalga oshiradi
public interface PaymentSummary {
    Long getId();
    Money getAmount();
    Instant getSettledAt();
}

List<PaymentSummary> findByOrderId(Long orderId);

// yaxshi: konstruktor projeksiyasi - record ga to'g'ridan-to'g'ri
@Query("""
        select new uz.shop.payment.PaymentSummary(p.id, p.amount, p.settledAt)
        from Payment p where p.orderId = :orderId
        """)
List<PaymentSummary> summariesFor(@Param("orderId") Long orderId);
```

### 28.8 SQL yozish uslubi

Migratsiya va native query dagi SQL ham kod va u ham o'qilishi kerak. Qoidalar qisqa va ularni formatter majburlay oladi (13.3 dagi Spotless `sql` bloki).

| Qoida | Sabab |
|---|---|
| Kalit so'zlar kichik harfda (yoki izchil katta) | izchillik |
| `select *` emas, ustunlar sanaladi | sxema o'zgarsa kod buzilmaydi |
| Har bir ustun/shart alohida qatorda | diff o'qiladi |
| `join ... on` oshkor, vergulli join yo'q | shart ko'rinadi |
| Ichma-ich subquery o'rniga CTE (`with`) | o'qiladi |
| Jadval aliaslari ma'noli (`p`, `o`), bir harfli emas-chi | qisqa va aniq |
| `where` da funksiya yo'q (`lower(col) = ?`) | indeks ishlaydi |
| Sanada yarim ochiq oraliq (`>=`, `<`) | 22.6 |

```sql
-- yaxshi: o'qiladi, ustunlar sanalgan, CTE bilan tekis
with settled as (
    select p.order_id,
           sum(p.amount) as settled_amount
    from payment p
    where p.settled_at >= :from
      and p.settled_at < :to_exclusive
    group by p.order_id
)
select o.id,
       o.customer_id,
       o.total_amount,
       coalesce(s.settled_amount, 0) as settled_amount
from orders o
left join settled s on s.order_id = o.id
where o.status = 'CONFIRMED'
order by o.created_at desc;
```

### 28.9 Migratsiya fayli nomlanishi va mazmuni

Migratsiya strategiyasi va to'xtashsiz reliz arxitektor hujjatida (33-bob). Bu yerda fayl darajasidagi qoidalar: nomlanish (3.13), bir migratsiya bir maqsad, va orqaga qaytarish imkoni.

```sql
-- V12__add_settled_at_to_payment.sql
-- Maqsad: hisob-kitob vaqtini saqlash. To'xtashsiz: avval ustun qo'shiladi (nullable),
-- keyingi relizda kod yozadi, V14 da not null qo'yiladi.

alter table payment
    add column settled_at timestamptz;

-- Indeks concurrently: jadval bloklanmaydi (katta jadval uchun majburiy)
create index concurrently if not exists ix_payment_settled_at
    on payment (settled_at)
    where settled_at is not null;
```

Qoidalar: bir faylda bir mantiqiy o'zgarish, migratsiyani qo'lda tahrirlamaslik (checksum buziladi), va ma'lumot migratsiyasini sxema migratsiyasidan ajratish.

### 28.10 Amalda qo'llash

- [ ] Barcha entitetlarda `equals`/`hashCode` ni identifikator bo'yicha yozib, `hashCode` ni barqaror qiling.
- [ ] Entitetlardagi `@Data`, `@EqualsAndHashCode`, `@ToString` annotatsiyalarini olib tashlang.
- [ ] Barcha `@ManyToOne` va `@OneToOne` ga oshkor `fetch = LAZY` qo'shing.
- [ ] `cascade = ALL` ishlatilgan joylarni 28.4 jadvaliga qarab ko'rib chiqing.
- [ ] Ikki tomonli assotsiatsiyalarga yordamchi metodlar qo'shib, kolleksiya getter larini o'zgartirilmas qiling.
- [ ] Uch shartdan uzun derived query nomlarini `@Query` ga o'tkazib, matn bloki bilan yozing.
- [ ] Entitet qaytaradigan API metodlarini projeksiya yoki DTO ga o'tkazing.
- [ ] SQL fayllarini 28.8 qoidalariga keltirib, `select *` ni ustun ro'yxatiga almashtiring.
## 29. Log kodining tozaligi (Clean Logging Code)

Kuzatuvchanlik amaliyoti va log narxi arxitektor hujjatida (30-bob), observability patternlari patternlar hujjatida (21-bob). Bu bobda log **kodining** o'zi: xabar yozish shakli, daraja tanlash, istisno uzatish, takrorlanish va MDC.

### 29.1 SLF4J parametrlangan xabar va satr birlashtirmaslik

SLF4J da `{}` placeholder ikki foyda beradi: daraja o'chirilgan bo'lsa satr umuman qurilmaydi, va xabar shabloni log agregatorida guruhlanadi.

```java
// yomon: satr har doim qurilib keyin tashlanadi
log.debug("to'lov " + paymentId + " yopildi, summa: " + amount);

// yomon: toString() har doim chaqiriladi
log.debug("to'lov {}", expensiveObject.toString());

// yaxshi
log.debug("to'lov {} yopildi, summa: {}", paymentId, amount);

// yaxshi: qimmat hisob lazy supplier bilan (SLF4J 2.x fluent API)
log.atDebug().setMessage("holat: {}").addArgument(() -> expensiveSnapshot()).log();
```

`isDebugEnabled()` tekshiruvi parametrlangan xabar bilan **kerak emas** — u faqat argument hisoblash qimmat bo'lganda haqli.

### 29.2 Daraja tanlash qoidalari

Daraja noto'g'ri tanlansa, ikki muammo paydo bo'ladi: `ERROR` shovqinga aylanadi va hech kim ogohlantirishga qaramaydi, yoki haqiqiy xato `DEBUG` da yo'qoladi.

| Daraja | Qachon | Kim ko'radi |
|---|---|---|
| `ERROR` | odam aralashuvi kerak, SLO buzildi | alert, on-call |
| `WARN` | kutilmagan holat, lekin tizim ishlayapti | kundalik ko'rib chiqish |
| `INFO` | muhim biznes hodisasi, holat o'zgarishi | audit, tahlil |
| `DEBUG` | diagnostika uchun tafsilot | ishlab chiqish, incident |
| `TRACE` | juda batafsil, odatda o'chirilgan | chuqur diagnostika |

Amaliy sinov: `ERROR` yozilganda kimdir uyg'onishi kerakmi? Javob "yo'q" bo'lsa, u `WARN`. Validatsiya xatosi, topilmadi (404), biznes qoidasi buzildi — bular `ERROR` emas (27.3).

### 29.3 Istisnoni oxirgi argument sifatida berish

SLF4J istisnoni oxirgi argument sifatida qabul qiladi va stack trace ni to'liq yozadi. Istisnoni placeholder bilan uzatish stack trace ni yo'qotadi.

```java
// yomon: stack trace yo'q, faqat xabar
log.error("hisob-kitob xatosi: {}", e.getMessage());

// yomon: istisno placeholder ga tushdi, trace yo'qoldi
log.error("hisob-kitob xatosi: {}", e);

// yaxshi: kontekst placeholder da, istisno oxirgi argument
log.error("to'lov {} uchun hisob-kitob muvaffaqiyatsiz", paymentId, e);
```

### 29.4 `e.getMessage()` bilan stack trace ni yo'qotish

`e.getMessage()` eng ko'p uchraydigan diagnostika xatosi: `NullPointerException` uchun u ko'pincha `null` qaytaradi, va stack trace bo'lmasa xato qayerda bo'lganini aniqlash imkonsiz.

Qoida: log da istisno **obyekti** uzatiladi, xabari emas. Xabarni esa faqat foydalanuvchiga ko'rsatiladigan javobda ishlatish mumkin (19.10).

### 29.5 Bir hodisa, bitta log

Log takrorlanishi 19.7 da ko'rilgan muammoning amaliy natijasi: bitta xato har bir qatlamda log qilinsa, incident vaqtida bir xato uch-to'rt yozuv beradi va haqiqiy sabab shovqin ichida qoladi.

```java
// yomon: uch qatlam, uch log
// repository: log.error("SQL xatosi", e); throw ...
// service:    log.error("hisob-kitob xatosi", e); throw ...
// controller: log.error("so'rov xatosi", e); return 500

// yaxshi: kontekst har qatlamda qo'shiladi, log bir joyda
// repository: throw new SettlementStorageException("yozib bo'lmadi: " + id, e);
// service:    throw new SettlementFailedException(paymentId, e);
// controller advice: log.error("hisob-kitob muvaffaqiyatsiz: {}", paymentId, e);
```

### 29.6 Strukturali log va kalit nomlari

Agregatorda qidirish uchun log maydonlari strukturali bo'lishi kerak: matn ichidagi qiymatni qidirish emas, maydon bo'yicha filtrlash. Kalit nomlari esa izchil bo'lishi lozim (3.13).

```java
// yaxshi: strukturali maydonlar, matn ichida yashirin emas
log.atInfo()
        .addKeyValue("orderId", order.id())
        .addKeyValue("customerId", order.customerId())
        .addKeyValue("amount", order.total().amount())
        .addKeyValue("currency", order.total().currency())
        .setMessage("buyurtma tasdiqlandi")
        .log();
```

```xml
<!-- logback-spring.xml: production da JSON, mahalliy ishda o'qiladigan matn -->
<springProfile name="!local">
  <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
      <includeMdcKeyName>traceId</includeMdcKeyName>
      <includeMdcKeyName>spanId</includeMdcKeyName>
    </encoder>
  </appender>
</springProfile>
```

### 29.7 Korrelyatsiya identifikatori va MDC tozalash

Korrelyatsiya identifikatori (trace id) bo'lmasa, taqsimlangan tizimda bitta so'rovning yo'lini kuzatib bo'lmaydi. MDC uni har bir log yozuviga avtomatik qo'shadi, lekin uni **tozalash majburiy**: thread pool da thread qayta ishlatiladi va eski qiymat keyingi so'rovga o'tadi (16.9).

```java
// yaxshi: try/finally bilan kafolatlangan tozalash
@Component
class TraceIdFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        String traceId = Optional.ofNullable(request.getHeader("X-Trace-Id"))
                .orElseGet(() -> UUID.randomUUID().toString());
        MDC.put("traceId", traceId);
        try {
            response.setHeader("X-Trace-Id", traceId);
            chain.doFilter(request, response);
        } finally {
            MDC.clear();        // majburiy: thread qayta ishlatiladi
        }
    }
}
```

Asinxron kodda MDC avtomatik ko'chmaydi: `@Async` va `CompletableFuture` uchun kontekstni oshkor uzatish kerak (`MDC.getCopyOfContextMap()`).

### 29.8 Sezgir ma'lumot va maskalash

Sezgir ma'lumotni log ga yozish patternlar hujjatida anti-pattern (25.47) va u ko'pincha `toString` orqali tasodifan sodir bo'ladi (15.7). Himoya ikki qatlamli bo'lishi kerak: turda maskalash va log konfiguratsiyasida filtr.

```java
// yaxshi: tur o'zi maskalaydi - tasodifan oqib ketmaydi
public record CardNumber(String value) {

    public CardNumber {
        if (!value.matches("\\d{13,19}")) throw new IllegalArgumentException("karta raqami");
    }

    public String last4() { return value.substring(value.length() - 4); }

    @Override
    public String toString() { return "****" + last4(); }     // log xavfsiz
}
```

Log ga hech qachon chiqmasligi kerak bo'lgan ma'lumotlar ro'yxati: parol, token, `Authorization` sarlavhasi, karta raqami va CVV, shaxsiy identifikator (JSHSHIR), tibbiy ma'lumot, to'liq so'rov tanasi (ichida yuqoridagilar bo'lishi mumkin).

### 29.9 Log ni test bilan mahkamlash

Muhim log yozuvlari (audit, xavfsizlik hodisasi) shartnomaning qismi bo'lsa, ular test bilan qotirilishi kerak — aks holda refaktoring paytida jim yo'qoladi.

```java
@Test
void logsAuditEventOnRefund() {
    ListAppender<ILoggingEvent> appender = attachAppender(RefundService.class);

    refunds.create(command, idempotencyKey);

    assertThat(appender.list)
            .anySatisfy(event -> {
                assertThat(event.getLevel()).isEqualTo(Level.INFO);
                assertThat(event.getKeyValuePairs())
                        .anySatisfy(kv -> assertThat(kv.key).isEqualTo("refundId"));
            });
}
```

Bu testni har bir log uchun yozish kerak emas — faqat audit va xavfsizlik yozuvlari uchun.

### 29.10 Amalda qo'llash

- [ ] Log xabarlarida satr birlashtirish (`+`) ishlatilgan joylarni `{}` placeholder ga o'tkazing.
- [ ] `log.error("...", e.getMessage())` namunalarini istisno obyektini uzatadigan shaklga tuzating.
- [ ] `ERROR` darajasidagi yozuvlarni ko'rib, odam aralashuvi kerak bo'lmaganlarini `WARN` ga tushiring.
- [ ] Bir xatoni bir necha qatlamda log qiladigan joylarni topib, log ni faqat chegarada qoldiring.
- [ ] Strukturali log ga o'tib, kalit nomlarini (`orderId`, `traceId`) izchil qiling.
- [ ] MDC ishlatilgan filtrlarda `finally` da `MDC.clear()` borligini tekshiring.
- [ ] Karta, parol va token turlariga maskalangan `toString` qo'shib, log filtrini sozlang.
- [ ] Audit va xavfsizlik log yozuvlarini test bilan mahkamlang.
# IX. Test kodining tozaligi

## 30. Test kodi ham ishlab chiqarish kodi (Test Code Is Production Code)

Test strategiyasi, piramida, FIRST printsiplari, AAA tuzilishi va test nomlash testlash qo'llanmasida (2, 5-boblar) berilgan; Sonar ning test kodiga tegishli qoidalari SonarQube hujjatida (19-bob). Bu bobda faqat bitta mavzu: test kodining **o'qilishi va saqlanishi**.

### 30.1 Toza test nega kod bazasini saqlab qoladi

Test kodi iflos bo'lsa, u o'zgarishga qarshilik qiladi: har bir refaktoring o'nlab testni buzadi va jamoa refaktoringdan voz kechadi. Natijada ishlab chiqarish kodi ham eskiradi. Shu sababli test kodining tozaligi ishlab chiqarish kodining tozaligidan kam ahamiyatli emas.

Teskari tomoni ham bor: ishonchli test to'plami refaktoringni **bepul** qiladi. Bu hujjatdagi deyarli har bir refaktoring harakati (35-37 boblar) xavfsizlik to'rini talab qiladi, va u to'r — testlar.

### 30.2 DRY va DAMP muvozanati testda

Ishlab chiqarish kodida DRY (takrorlanmaslik) ustun; test kodida esa DAMP (Descriptive And Meaningful Phrases) ko'pincha ustun turadi. Sababi: test o'qilganda u **o'z-o'zidan tushunarli** bo'lishi kerak, boshqa fayllarga qarashga majbur qilmasligi lozim.

```java
// yomon: haqiqiy qiymatlar umumiy setup da yashirin - test nima tekshirayotgani ko'rinmaydi
@BeforeEach
void setUp() {
    order = TestData.defaultOrder();      // ichida nima bor?
}

@Test
void rejectsRefundExceedingPayment() {
    assertThatThrownBy(() -> service.refund(order, TestData.bigAmount()));
}

// yaxshi: muhim qiymatlar testda ko'rinadi, qolgani builder standartida
@Test
void rejectsRefundExceedingPayment() {
    Order order = anOrder().withSettledAmount(Money.of("100.00", UZS)).build();

    assertThatThrownBy(() -> service.refund(order, Money.of("150.00", UZS)))
            .isInstanceOf(RefundExceedsPaymentException.class);
}
```

Qoida: testga **ta'sir qiladigan** qiymatlar testda ko'rinadi; ahamiyatsiz qiymatlar builder standartida qoladi.

### 30.3 Test ma'lumot quruvchilari: builder va object mother

Test ma'lumotini qurish takrorlanishi eng katta test qarzi manbai. Ikki pattern ishlaydi va ularni birga ishlatish mumkin.

**Test data builder** — standart qiymatlar bilan to'ldirilgan builder, testda faqat muhim maydon o'zgartiriladi. **Object mother** — nomlangan tipik holatlar fabrikasi (`aSettledPayment()`, `anExpiredOrder()`).

```java
// Test data builder: standart qiymatlar + nuqtali o'zgartirish
public final class OrderBuilder {

    private OrderId id = OrderId.of("ORD-1");
    private OrderStatus status = OrderStatus.CONFIRMED;
    private Money settledAmount = Money.of("100.00", UZS);
    private Instant createdAt = Instant.parse("2026-01-01T00:00:00Z");

    public static OrderBuilder anOrder() { return new OrderBuilder(); }

    public OrderBuilder withStatus(OrderStatus status) { this.status = status; return this; }
    public OrderBuilder withSettledAmount(Money amount) { this.settledAmount = amount; return this; }

    public Order build() { return new Order(id, status, settledAmount, createdAt); }
}

// Object mother: tipik holatlar nomlangan
public final class Orders {
    public static Order settled() { return anOrder().withStatus(SETTLED).build(); }
    public static Order expired() { return anOrder().withCreatedAt(LONG_AGO).build(); }
}
```

### 30.4 Testda mantiq bo'lmasligi

Testda `if`, sikl yoki hisob bo'lsa, test o'zi xato bo'lishi mumkin va uni hech narsa tekshirmaydi. Bundan tashqari, shartli test ba'zi yo'llarni umuman sinamaydi va bu coverage hisobotida ko'rinmaydi.

```java
// yomon: testda shart - qaysi shox bajarilgani ko'rinmaydi
@Test
void calculatesTax() {
    for (Region region : Region.values()) {
        Money tax = policy.taxFor(region, net);
        if (region == Region.FREE_ZONE) {
            assertThat(tax).isEqualTo(Money.ZERO);
        } else {
            assertThat(tax).isGreaterThan(Money.ZERO);
        }
    }
}

// yaxshi: parametrlangan test, har bir holat alohida va kutilgan qiymat oshkor
@ParameterizedTest
@CsvSource({
        "TASHKENT,   100.00, 12.00",
        "FREE_ZONE,  100.00,  0.00",
        "SAMARKAND,  100.00, 12.00"
})
void calculatesTax(Region region, String net, String expectedTax) {
    assertThat(policy.taxFor(region, Money.of(net, UZS)))
            .isEqualTo(Money.of(expectedTax, UZS));
}
```

### 30.5 Bir tushuncha, bir test

"Bir testda bir assert" qoidasi juda qattiq; to'g'ri qoida — **bir testda bir tushuncha**. Bitta natijaning bir nechta jihati tekshirilsa, bir necha assert normal; ikki mustaqil xatti-harakat tekshirilsa, ikki test kerak.

```java
// yaxshi: bir tushuncha (yaratilgan refund holati), bir necha assert
@Test
void createsRefundInPendingState() {
    Refund refund = refunds.create(command, key);

    assertThat(refund.status()).isEqualTo(PENDING);
    assertThat(refund.amount()).isEqualTo(Money.of("50.00", UZS));
    assertThat(refund.requestedAt()).isEqualTo(FIXED_NOW);
}

// yaxshi: AssertJ bilan bitta assert, xato xabari to'liq
assertThat(refund)
        .extracting(Refund::status, Refund::amount)
        .containsExactly(PENDING, Money.of("50.00", UZS));
```

### 30.6 Assertion o'qilishi va xato xabari

Test yiqilganda uning xabari **sababni** aytishi kerak, aks holda diagnostika vaqti ketadi. AssertJ ning aniq assertion lari umumiylaridan ancha yaxshi xabar beradi.

```java
// yomon: "expected true but was false" - nima xato ekani ko'rinmaydi
assertTrue(refund.amount().equals(expected));
assertTrue(orders.size() == 3);

// yaxshi: xabar farqni ko'rsatadi
assertThat(refund.amount()).isEqualTo(expected);
assertThat(orders).hasSize(3);

// yaxshi: domen tilida, kontekst bilan
assertThat(orders)
        .as("tasdiqlangan buyurtmalar %s mijoz uchun", customerId)
        .extracting(Order::status)
        .containsOnly(CONFIRMED);
```

### 30.7 Test dublyorlarini nomlash va chegaralash

Test dublyorlari (mock, stub, fake) testlash qo'llanmasida batafsil. Bu yerda tozalik qoidasi: mock soni testning dizayn signali. Bir testda beshta mock bo'lsa, tekshirilayotgan sinfning bog'liqliklari juda ko'p (26.1).

Ikkinchi qoida: **o'zingiz yozmagan** turlarni mock qilmaslik. Uchinchi tomon kutubxonasining mock i uning haqiqiy xatti-harakatini takrorlamaydi va test yolg'on ishonch beradi; o'rniga wrapper yozib, uni mock qilish kerak (18.3).

```java
// yomon: tashqi kutubxona turi mock qilingan - haqiqiy xatti-harakat boshqa
@Mock RestTemplate restTemplate;

// yaxshi: o'z interfeysimiz mock qilinadi; integratsiya alohida testlanadi
@Mock PaymentGateway gateway;
```

### 30.8 Testlar orasidagi bog'liqlik va tartib

Testlar bir-biridan mustaqil bo'lishi kerak: har qanday tartibda, alohida yoki parallel ishga tushirilganda bir xil natija berishi lozim. Bog'liqlik odatda umumiy o'zgaradigan holatdan keladi: statik maydon (16.9), umumiy baza yozuvi, fayl tizimi.

```java
// yomon: statik holat testlar orasida oqib ketadi
static List<Order> created = new ArrayList<>();

// yomon: test tartibiga bog'liq
@Test @Order(1) void createsOrder() { ... }
@Test @Order(2) void findsCreatedOrder() { ... }     // birinchisiga bog'liq

// yaxshi: har bir test o'z ma'lumotini yaratadi va tozalaydi
@Test
void findsCreatedOrder() {
    Order saved = repository.save(anOrder().build());

    assertThat(repository.findById(saved.id())).contains(saved);
}
```

### 30.9 Test hidlari katalogi

Test kodidagi hidlar alohida katalogga ega va ularning har biri aniq muammoni bildiradi.

| Hid | Belgisi | Yechim |
|---|---|---|
| Qotib qolgan test (fragile) | mantiq o'zgarmasa ham yiqiladi | ichki tuzilish emas, xatti-harakat tekshirish |
| Sekin test | bir test sekundlar oladi | mock yoki slice test (testlash qo'llanmasi) |
| Shartli test | ichida `if`/sikl | parametrlangan test (30.4) |
| Assertsiz test | faqat chaqiradi | assertion qo'shish yoki o'chirish |
| Yashirin bog'liqlik | tartibga bog'liq | izolyatsiya (30.8) |
| Ko'p mock | 4+ mock | sinf bog'liqliklarini kamaytirish |
| Noaniq nom | `test1`, `testOrder` | xatti-harakat nomi (3.12) |
| Takrorlangan setup | har testda 20 qator | builder (30.3) |
| Erkin assert | `assertNotNull` bilan tugaydi | aniq kutilgan qiymat |
| `Thread.sleep` | vaqtga bog'liq | Awaitility yoki `Clock` (22.3) |
| Izohga olingan test | `// @Test` | o'chirish yoki tuzatish |
| `@Disabled` sababsiz | sababsiz o'chirilgan | sabab va ticket yozish |

### 30.10 Amalda qo'llash

- [ ] Test ma'lumoti qurish takrorlanishini topib, har bir agregat uchun test data builder yozing.
- [ ] Testlardagi `if`, sikl va hisobni topib, parametrlangan testga aylantiring.
- [ ] `assertTrue`/`assertNotNull` assertion larini AssertJ ning aniq assertion lariga o'tkazing.
- [ ] Uchinchi tomon turlarining mock larini topib, o'z wrapper interfeysingizni mock qiling.
- [ ] Statik holat va test tartibiga bog'liqlikni yo'qotib, testlarni tasodifiy tartibda ishga tushirib tekshiring.
- [ ] `Thread.sleep` ishlatilgan testlarni Awaitility yoki qotirilgan `Clock` ga o'tkazing.
- [ ] `@Disabled` testlarni ro'yxatlab, har biriga sabab va ticket qo'shing yoki o'chiring.
- [ ] 30.9 jadvalidagi hidlar bo'yicha test kodini bir marta to'liq ko'rib chiqib, ro'yxat tuzing.
## 31. TDD intizomi va kod dizayniga ta'siri (TDD Discipline)

Test yozish texnikasi testlash qo'llanmasida. Bu bobda boshqa narsa: test yozish **tartibi** va uning kod dizayniga ta'siri. TDD test usuli emas, dizayn usuli — va shu sababli u toza kod hujjatiga tegishli.

### 31.1 Uchta qoida va qisqa sikl

TDD uchta qoidaga qisqaradi. Birinchi, yiqiladigan test yozilmaguncha ishlab chiqarish kodi yozilmaydi. Ikkinchi, testni yiqitish uchun yetarlicha test yozilgach to'xtash. Uchinchi, testni o'tkazish uchun yetarlicha ishlab chiqarish kodi yozilgach to'xtash.

Natija: sikl bir-ikki daqiqa davom etadi. Shu qisqalik eng muhim xususiyat, chunki har bir qadamda ishlaydigan tizim bo'ladi va xato oynasi ikki daqiqadan oshmaydi.

```java
// 1) Yiqiladigan test (kompilyatsiya ham bo'lmasligi mumkin)
@Test
void refundReducesSettledAmount() {
    Payment payment = aPayment().withSettled("100.00").build();

    payment.refund(Money.of("30.00", UZS));

    assertThat(payment.refundableAmount()).isEqualTo(Money.of("70.00", UZS));
}

// 2) Eng oddiy o'tadigan kod
public void refund(Money amount) {
    this.refunded = this.refunded.plus(amount);
}

// 3) Keyingi test qoidani qo'shadi
@Test
void rejectsRefundExceedingSettledAmount() {
    Payment payment = aPayment().withSettled("100.00").build();

    assertThatThrownBy(() -> payment.refund(Money.of("150.00", UZS)))
            .isInstanceOf(RefundExceedsPaymentException.class);
}
```

### 31.2 Red-green-refactor: har bir qadamning maqsadi

Uch qadamning har birining aniq va boshqa maqsadi bor; ularni aralashtirish TDD ning foydasini yo'qotadi.

| Qadam | Maqsad | Nima qilinmaydi |
|---|---|---|
| **Red** | talabni ifodalash, testning o'zi ishlashini tekshirish | ishlab chiqarish kodi yozilmaydi |
| **Green** | testni o'tkazish, eng qisqa yo'l bilan | chiroylilik, umumiylashtirish |
| **Refactor** | tuzilishni yaxshilash | yangi xatti-harakat qo'shilmaydi |

"Red" qadamining ko'pincha e'tibordan chetda qoladigan maqsadi bor: test **yiqilishini ko'rish** kerak. Yiqilmagan test hech narsa tekshirmaydi va bu xato kech aniqlanadi.

### 31.3 Test birinchi yozilsa dizayn qanday o'zgaradi

Testni birinchi yozish dizaynga bosim beradi va bu bosim bu hujjatdagi ko'p qoidalarni **majburiy** qiladi:

- Bog'liqliklar konstruktorga chiqadi, chunki testda ularni almashtirish kerak (26.1).
- `Clock` inyeksiya qilinadi, chunki vaqtni qotirish kerak (22.3).
- Statik holat yo'qoladi, chunki testlar bir-biriga ta'sir qilmasligi kerak (16.9).
- Metodlar kichik bo'ladi, chunki katta metodni test qilish qiyin (4.1).
- Yon ta'sir ajratiladi, chunki sof funksiyani test qilish oson (16.6).
- Argumentlar kamayadi, chunki har bir argumentni testda yasash kerak (5.1).

Shu sababli "test yozish qiyin" degan hissiyot dizayn signali (31.5), vaqt yo'qligi signali emas.

### 31.4 Ishlasin, to'g'ri bo'lsin, tez bo'lsin tartibi

Tartib muhim va uni buzish eng ko'p vaqt yo'qotadi. **Ishlasin** — test o'tadi, yechim chirkin bo'lishi mumkin. **To'g'ri bo'lsin** — tuzilish tozalanadi, nomlar aniqlashadi, takrorlanish yo'qoladi. **Tez bo'lsin** — faqat o'lchov muammo ko'rsatsa (1.5).

Uchinchi qadamga o'tish sharti aniq: o'lchov bor va u talabni buzayotganini ko'rsatadi. O'lchovsiz optimizatsiya vaqtidan oldin optimizatsiya (patternlar hujjati 25.10).

### 31.5 Test yozish qiyin bo'lsa, dizayn signal beradi

Testning qiyinligi deyarli har doim aniq dizayn muammosini ko'rsatadi. Jadval shu signallarni tarjima qiladi.

| Test qiyinligi | Dizayn muammosi | Yechim |
|---|---|---|
| Mock soni 4+ | juda ko'p bog'liqlik | sinfni bo'lish |
| `new` ni almashtirib bo'lmaydi | qattiq bog'liqlik | inyeksiya |
| Vaqtni qotirib bo'lmaydi | `Instant.now()` tarqoq | `Clock` (22.3) |
| Statik metodni mock qilish kerak | statik bog'liqlik | interfeys |
| Private metodni test qilish kerak | sinfda yashiringan sinf | ajratish |
| Butun Spring kontekst kerak | qatlamlar chalkash | sof domen |
| Testda 30 qator setup | konstruktor juda katta | argument obyekti |
| Natijani tekshirib bo'lmaydi | metod `void` va yon ta'sirli | qiymat qaytarish |
| Testlar bir-biriga ta'sir qiladi | global holat | holatni yo'qotish |

### 31.6 TDD qachon mos emas

TDD universal emas va uni majburlash zarar keltiradigan holatlar bor. Tadqiqot (spike) kodida: hali nima qurilayotgani ma'lum bo'lmaganda test yozish ma'nosiz — spike tashlab yuboriladi va keyin TDD bilan qaytadan yoziladi. UI joylashuvi va vizual dizaynda: natijani ko'z bilan baholash arzonroq. Generatsiya qilingan kodda: test generator uchun yoziladi, natija uchun emas. Shuningdek, tashqi tizim xatti-harakatini o'rganishda: bunda "learning test" yoziladi, lekin u TDD sikli emas.

Qolgan hamma joyda, ayniqsa biznes qoidalari va hisob mantiqida, TDD eng arzon yo'l.

### 31.7 Transformatsiya prioritet gipotezasi

"Green" qadamida kodni qanday o'zgartirish kerakligi haqida foydali evristika bor: eng **oddiy** transformatsiyani tanlash. Tartib soddadan murakkabga: `{}` → `null`, `null` → konstanta, konstanta → o'zgaruvchi, ifoda → shart, qiymat → massiv, massiv → to'plam, shart → sikl, sikl → rekursiya, qiymat → polimorfizm.

Amaliy foydasi: har qadamda eng oddiy transformatsiyani tanlash kodni tabiiy ravishda sodda holatda ushlab turadi va vaqtidan oldin umumiylashtirishni (patternlar hujjati 25.25) to'sadi.

### 31.8 Amalda qo'llash

- [ ] Keyingi yangi biznes qoidasini to'liq TDD sikli bilan yozib, siklni ikki daqiqada ushlashga harakat qiling.
- [ ] Har bir yangi test yozilganda uning **yiqilishini** ko'rishni odat qiling.
- [ ] Refaktoring qadamida yangi xatti-harakat qo'shmaslik qoidasini commit darajasida ajratib yuring (40.1).
- [ ] 31.5 jadvalidan foydalanib, test yozish qiyin bo'lgan uch sinfni topib, dizayn muammosini tuzating.
- [ ] `Instant.now()` va statik chaqiruvlarni inyeksiyaga o'tkazib, testlarni frameworksiz ishga tushiradigan qiling.
- [ ] Spike kodini alohida branch da ushlab, uni to'g'ridan-to'g'ri merge qilmaslikni kelishib oling.
- [ ] Jamoada bir hafta TDD bilan ishlab, keyin test qarzining o'zgarishini o'lchab ko'ring.
- [ ] "Green" qadamida eng oddiy transformatsiyani tanlash qoidasini mashq sessiyasida (46.7) sinab ko'ring.
# X. Hid katalogi va refaktoring harakatlari

## 32. Kod hidlari katalogi I: nom, funksiya, ma'lumot (Code Smells I)

Kod hidi — xato emas, lekin muammo ehtimolini oshiradigan tuzilish. Patternlar hujjatida 83 ta anti-pattern sanalgan (25-bob); bu va keyingi bob ularni **takrorlamaydi** va qolgan hidlarni beradi. Har bir hid uchun uch qism: belgisi, nega muammo, va qaysi refaktoring harakati bilan tuzatiladi (35-37 boblar).

### 32.1 Sirli nom (Mysterious Name)

**Belgisi**: nomni o'qib nima qilayotganini aytib bo'lmaydi; `proc`, `handle`, `data2`, `tmpFlag`.

**Nega muammo**: nom eng arzon hujjat va u ishlamasa, har bir o'quvchi kodni qaytadan o'qib chiqadi. Bu eng ko'p uchraydigan va eng arzon tuzatiladigan hid.

**Tuzatish**: Rename Variable / Rename Field / Change Function Declaration (35-bob). Agar nom o'ylab chiqmasa, bu sinfning javobgarligi noaniq ekanini bildiradi — Extract Class kerak bo'lishi mumkin.

### 32.2 Takrorlangan kod (Duplicated Code)

DRY printsipi patternlar hujjatida (26.19). Bu yerda amaliy qism: takrorlanishning **uch turi** bor va ularning har biri boshqa yechim talab qiladi.

| Tur | Ko'rinishi | Yechim |
|---|---|---|
| Aynan takrorlanish | bir xil qatorlar bir sinfda | Extract Function |
| Qardosh takrorlanish | bir xil kod ikki voris sinfda | Pull Up Method |
| Shaklli takrorlanish | tuzilish bir xil, qiymatlar boshqa | Parameterize Function |
| Soxta takrorlanish | o'xshash ko'rinadi, lekin boshqa sabab bilan o'zgaradi | **tegmaslik** |

Oxirgi qator eng muhim: tasodifan o'xshash kodni birlashtirish noto'g'ri abstraksiya yaratadi va u takrorlanishdan qimmat (arxitektor hujjati 5.2-5.3).

### 32.3 Uzun funksiya (Long Function)

Metod uzunligi arxitektor hujjatida (4.4) va 4-bobda ko'rilgan. Hid sifatida uning belgisi aniq: funksiyani tushunish uchun uni bo'laklarga ajratib o'qish kerak.

**Tuzatish tartibi**: Extract Function (eng ko'p), Replace Temp with Query, Introduce Parameter Object, Decompose Conditional, Split Loop, Replace Conditional with Polymorphism.

### 32.4 Global ma'lumot (Global Data)

**Belgisi**: `public static` o'zgaradigan maydon, singleton ichidagi o'zgaradigan holat, `System.getProperties()` ni kod bo'ylab o'zgartirish.

**Nega muammo**: o'zgarishning manbasini topib bo'lmaydi — har qanday kod istalgan vaqtda o'zgartirgan bo'lishi mumkin. Debug qilish uchun butun kod bazasini ko'rish kerak.

**Tuzatish**: Encapsulate Variable (36-bob) — global ma'lumotni funksiya ortiga yashirish, keyin bog'liqlik sifatida uzatish (16.9).

### 32.5 O'zgaradigan ma'lumot (Mutable Data)

**Belgisi**: obyektning maydoni kod bo'ylab turli joylarda o'zgaradi; setter lar ko'p; bir maydonni kim o'zgartirganini kuzatish qiyin.

**Nega muammo**: o'zgarishning sabab-natija zanjiri yo'qoladi. Bu ayniqsa ko'p threadli kodda xavfli.

**Tuzatish**: Encapsulate Variable, Split Variable, Remove Setting Method, Replace Derived Variable with Query, Change Reference to Value (16-bob va 36-bob).

### 32.6 Ma'lumot to'dasi (Data Clumps)

**Belgisi**: bir xil uch-to'rt maydon bir necha sinfda va metod imzolarida birga paydo bo'ladi: `from`, `to`; `street`, `city`, `zip`; `amount`, `currency`.

**Nega muammo**: tushuncha nomsiz qolgan. Har bir yangi ishlatilish takrorlanish qo'shadi va validatsiya tarqaladi.

**Tuzatish**: Introduce Parameter Object yoki Extract Class (5.6, 36-bob). Sinov: maydonlardan birini olib tashlasa, qolganlari ma'nosini yo'qotadimi? Ha bo'lsa — bu bitta tushuncha.

### 32.7 Takrorlangan `switch` (Repeated Switches)

**Belgisi**: bir xil `switch` yoki `if/else` zanjiri kod bazasining bir necha joyida takrorlanadi (6.10).

**Nega muammo**: yangi variant qo'shilganda barcha takrorlarni topish kerak va bittasi doim esdan chiqadi — xato faqat shu variant uchrashganda chiqadi.

**Tuzatish**: xatti-harakatni enum ichiga ko'chirish, Replace Conditional with Polymorphism, yoki `sealed` + pattern matching (25.3).

### 32.8 Sikllar (Loops)

**Belgisi**: filtrlash, mapping va yig'ish qo'lda sikl bilan yozilgan.

**Nega muammo**: sikl **nima** qilayotganini aytmaydi, faqat **qanday** qilayotganini ko'rsatadi. O'quvchi niyatni o'zi chiqarib olishi kerak.

**Tuzatish**: Replace Loop with Pipeline (35-bob) — lekin 7.7 dagi mezonni hisobga olib: erta chiqish, yon ta'sir va istisno bo'lsa sikl qoladi.

### 32.9 Dangasa element (Lazy Element)

**Belgisi**: hech narsa qo'shmaydigan abstraksiya — bitta metodi bor interfeys, faqat bazaviy sinfni chaqiradigan voris sinf, bitta qatordan iborat va bir joyda chaqiriladigan funksiya nomi o'z tanasi bilan bir xil ma'noda.

**Nega muammo**: har bir qo'shimcha daraja o'qish narxini oshiradi, lekin foyda bermaydi (patternlar hujjatidagi Poltergeist va Yo-Yo bilan qardosh).

**Tuzatish**: Inline Function, Inline Class, Collapse Hierarchy (37-bob). Ehtiyot: kelgusi o'zgarish uchun qo'yilgan abstraksiya dangasa emas (arxitektor hujjati 5.1).

### 32.10 Vaqtinchalik maydon (Temporary Field)

16.8 da ko'rilgan. Hid sifatida belgisi: maydon faqat ba'zi metodlar ishlaganda to'ldirilgan, qolgan vaqt `null`.

**Tuzatish**: Extract Class (vaqtinchalik maydonlar guruhini o'z sinfiga olish) yoki mahalliy o'zgaruvchiga aylantirish; `null` holatini Introduce Special Case bilan ifodalash.

### 32.11 Uzun xabar zanjiri (Message Chains)

**Belgisi**: `a.b().c().d().e()` — chaqiruvchi tuzilmaning bir necha darajasini biladi (14.4).

**Nega muammo**: oraliq turlardan birortasi o'zgarsa, zanjir buziladi. Chaqiruvchi o'ziga kerak bo'lmagan turlarga bog'lanib qoladi.

**Tuzatish**: Hide Delegate (36-bob) — oraliq obyekt delegatsiya metodi beradi; yoki Extract Function (zanjirni bir metodga olib, uni egasiga ko'chirish — Move Function).

### 32.12 Vositachi (Middle Man)

**Belgisi**: sinfning metodlarining katta qismi boshqa obyektga delegatsiya qiladi va o'zi hech narsa qilmaydi.

**Nega muammo**: 32.11 ning teskarisi — delegatsiyani yashirishga urinish ortiqcha ketgan. Har bir yangi metod ikki joyda yoziladi.

**Tuzatish**: Remove Middle Man (chaqiruvchi to'g'ridan-to'g'ri murojaat qiladi) yoki Inline Function. Eslatma: fasad va adapter atayin "vositachi" — ular hid emas, chunki ular chegara vazifasini bajaradi.

### 32.13 Izohlar hid sifatida (Comments)

9-bobda izohlarning katalogi berilgan. Hid sifatida muhim nuqtasi: izohlar ko'p bo'lgan joy ko'pincha **yomon kodni oqlash** uchun ishlatiladi. Izoh "deodorant" vazifasini bajaradi: hidni yashiradi, lekin yo'qotmaydi.

**Tuzatish**: Extract Function (izoh nomga aylanadi, 8.2), Change Function Declaration (nom aniqlashadi), Introduce Assertion (taxmin kodga aylanadi).

### 32.14 Bu hid emas: qachon tegmaslik kerak

Hid ro'yxati faqat **nomzodlar** beradi, hukm bermaydi. To'rtta holatda hidga tegmaslik to'g'ri qaror.

| Holat | Nega tegmaslik |
|---|---|
| Kod ishlayapti va o'zgarmaydi | tuzatish narxi foydadan ko'p (arxitektor hujjati 34.11) |
| Testlar yo'q | refaktoring xavfli, oldin test kerak |
| Hid chegarada (adapter, DTO) | ataylab shunday |
| Soxta takrorlanish | birlashtirish noto'g'ri abstraksiya beradi (32.2) |

### 32.15 Amalda qo'llash

- [ ] Eng ko'p o'zgaradigan 10 faylni olib, shu bobdagi hidlar bo'yicha ro'yxat tuzing va har biriga refaktoring harakatini belgilang.
- [ ] Takrorlangan kod joylarini 32.2 jadvalidagi to'rt turga ajratib, soxta takrorlanishni alohida belgilang.
- [ ] Bir xil parametr guruhlarini (data clumps) grep bilan topib, har biriga record kiriting.
- [ ] Takrorlangan `switch` zanjirlarini sanab, xatti-harakatni enum yoki `sealed` ierarxiyaga ko'chiring.
- [ ] `public static` o'zgaradigan maydonlarni topib, inkapsulyatsiya qilib keyin bog'liqlikka aylantiring.
- [ ] Uch darajadan uzun chaqiruv zanjirlarini topib, Hide Delegate yoki Move Function qo'llang.
- [ ] Faqat delegatsiya qiladigan sinflarni ko'rib, chegara vazifasini bajarmaganlarini olib tashlang.
- [ ] Izohlar eng ko'p to'plangan uch faylni tanlab, izohlarni metod nomlariga aylantirishni sinab ko'ring.
## 33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik (Code Smells II)

Bu bob sinf darajasidagi va sinflar orasidagi hidlarni qamrab oladi. God Object, Big Ball of Mud, Circular Dependency va boshqa arxitektura darajasidagi anti-patternlar patternlar hujjatida (25-bob); bu yerda ularning kod darajasidagi qardoshlari.

### 33.1 Tarqoq o'zgarish (Divergent Change)

**Belgisi**: bitta sinf turli sabablarga ko'ra o'zgaradi — bugun soliq qoidasi uchun, ertaga ma'lumot bazasi sxemasi uchun, indinga JSON formati uchun.

**Nega muammo**: har bir o'zgarish boshqa sabablar bilan yozilgan kodga tegadi va regressiya xavfi oshadi. Bu yagona javobgarlik printsipining buzilishi (patternlar hujjati 26.1).

**Tuzatish**: Extract Class, Split Phase (36-bob). Aniqlash usuli: `git log` bilan sinf o'zgarishlarining sabablarini sanash (arxitektor hujjati 5.6 chegara aniqlash texnikasini beradi).

### 33.2 Ma'lumot sinfi (Data Class)

**Belgisi**: sinfda faqat maydonlar, getter va setter lar bor; xatti-harakat yo'q. Shu sinf bilan bog'liq mantiq boshqa sinflarda tarqalgan.

**Nega muammo**: Anemik domen modelining kichik shakli (patternlar hujjati 25.35). Har bir foydalanuvchi o'z nusxasidagi qoidani yozadi va qoidalar bir-biridan farq qiladi.

**Tuzatish**: Move Function (mantiqni ma'lumot egasiga ko'chirish), Encapsulate Record, Remove Setting Method. Eslatma: DTO va `record` chegarada ataylab ma'lumot sinfi bo'ladi (14.5) — bu hid emas.

### 33.3 Noo'rin yaqinlik (Inappropriate Intimacy / Insider Trading)

**Belgisi**: ikki sinf bir-birining ichki maydonlari va private holatiga haddan tashqari ko'p murojaat qiladi; ichma-ich sinflar yoki `package-private` kirish orqali bir-birini "biladi".

**Nega muammo**: ikki sinf aslida bitta, lekin ikkiga bo'lingan; yoki chegara noto'g'ri joyda. Birini o'zgartirish ikkinchisini buzadi.

**Tuzatish**: Move Function / Move Field (sinflarni to'g'ri taqsimlash), Extract Class (umumiy qismni ajratish), Hide Delegate, yoki ikki sinfni birlashtirish (Inline Class).

### 33.4 Muqobil sinflar, turli interfeyslar (Alternative Classes with Different Interfaces)

**Belgisi**: ikki sinf bir xil ish qiladi, lekin metod nomlari va imzolari boshqa: `SmsSender.send(to, text)` va `EmailGateway.deliverMessage(address, body, subject)`.

**Nega muammo**: ularni almashtirib ishlatish imkonsiz, shuning uchun har bir chaqiruv joyi `if` bilan shoxlanadi.

**Tuzatish**: Change Function Declaration (nomlarni moslashtirish), keyin Extract Superclass yoki umumiy interfeys ajratish. Agar biri uchinchi tomon sinfi bo'lsa — adapter (patternlar hujjati).

### 33.5 Rad etilgan meros (Refused Bequest)

17.6 da ko'rilgan. Hid sifatida belgisi: voris sinf meros olgan metodlarning bir qismini ishlatmaydi yoki `UnsupportedOperationException` tashlaydi.

**Tuzatish**: Push Down Method / Push Down Field (keraksizni pastga tushirish), Replace Superclass with Delegate (17.9), yoki interfeysni bo'lish.

### 33.6 Parallel ierarxiyalar (Parallel Inheritance Hierarchies)

**Belgisi**: bitta ierarxiyaga voris sinf qo'shilganda, ikkinchi ierarxiyaga ham mos sinf qo'shish kerak bo'ladi: `CardPayment`/`CardPaymentValidator`, `BankPayment`/`BankPaymentValidator`.

**Nega muammo**: ikki ierarxiya bir xil o'qni bo'yicha o'sadi va ularni sinxron ushlash qo'lda bajariladi; bittasi doim esdan chiqadi.

**Tuzatish**: ikkinchi ierarxiyani birinchisiga ko'chirish (validator mantiqini `Payment` ichiga), yoki `sealed` ierarxiya va pattern matching bilan bitta o'qga qisqartirish.

### 33.7 To'liq bo'lmagan kutubxona sinfi (Incomplete Library Class)

**Belgisi**: uchinchi tomon sinfi kerakli metodni bermaydi va kod bazasida uning atrofida yordamchi funksiyalar tarqalgan.

**Nega muammo**: bir xil yordamchi bir necha joyda yoziladi va ular bir-biridan farq qiladi.

**Tuzatish**: yordamchilarni bitta `final` utility sinfga yoki wrapper ga yig'ish (14.8, 18.3). Kutubxona turini domen kodida tarqatmaslik ham shu yechimning qismi.

### 33.8 Haddan tashqari ko'p ma'lumot (Too Much Information)

**Belgisi**: sinf yoki interfeys 20+ public metod beradi; paketdan o'nlab tur eksport qilinadi; `public` modifikatori standart tanlov.

**Nega muammo**: keng interfeys ko'p bog'liqlik yaratadi va har bir public element kelajakdagi majburiyat (arxitektor hujjati 13.9).

**Tuzatish**: ko'rinishni toraytirish (14.6), interfeysni bo'lish, paketdan faqat API turlarini chiqarish (26.2).

### 33.9 Izchilsizlik (Inconsistency)

**Belgisi**: bir xil narsa kod bazasining turli joylarida turlicha qilinadi — bir joyda `Optional`, boshqa joyda `null`; bir joyda konstruktor inyeksiyasi, boshqa joyda maydon; bir joyda `find`, boshqa joyda `get`.

**Nega muammo**: o'quvchi har bir joyda qaytadan o'ylashi kerak va taxminlari xato bo'ladi.

**Tuzatish**: konvensiyani hujjatlashtirish (48-bob), keyin uni mashinaga topshirish (42-bob). Izchilsizlik eng tez tarqaladigan hid, chunki har bir yangi kod mavjud namunaga qaraydi.

### 33.10 Keraksizlik (Clutter)

**Belgisi**: hech narsa qilmaydigan elementlar — bo'sh konstruktor, ishlatilmaydigan maydon, hech kim chaqirmaydigan metod, mazmunsiz izoh, ishlatilmaydigan import, `default` konstruktorni oshkor yozish.

**Nega muammo**: har bir keraksiz element o'quvchidan "bu nega bor?" savolini talab qiladi.

**Tuzatish**: Remove Dead Code (35-bob). O'lik kodni topish uchun IDE inspeksiyasi, `-Xlint`, va kod qamrovi hisoboti ishlatiladi (SonarQube hujjati 28-bobda o'lik kod katalogini beradi).

### 33.11 Sun'iy bog'liqlik (Artificial Coupling)

**Belgisi**: bir-biriga tegishli bo'lmagan narsalar bir joyda turadi — umumiy enum "umumiy" paketda, ichki sinf boshqa modulda e'lon qilingan, konstanta tasodifiy sinfda.

**Nega muammo**: bog'liqlik grafi sabab bilan emas, qulaylik bilan qurilgan. Har bir import keraksiz bog'lanish qo'shadi.

**Tuzatish**: Move Function / Move Field / Move Class — elementni eng ko'p ishlatiladigan joyga ko'chirish.

### 33.12 Noto'g'ri joylashgan javobgarlik (Misplaced Responsibility)

**Belgisi**: funksiya nomi bilan sinf nomi mos kelmaydi; `OrderService.calculateTax()`, `UserController.sendEmail()`, `PaymentRepository.formatReceipt()`.

**Nega muammo**: o'quvchi funksiyani topa olmaydi, chunki u mantiqan boshqa joyda bo'lishi kerak. Natijada funksiya ikkinchi marta yoziladi.

**Tuzatish**: Move Function. Aniqlash savoli: "bu funksiya qaysi ma'lumotga eng ko'p murojaat qiladi?" — javob uning uyi (patternlar hujjati 26.6, Information Expert).

### 33.13 Noo'rin statik (Inappropriate Static)

**Belgisi**: statik metod aslida polimorfizm talab qiladi — `Money.calculateTax(money, region)` har bir mintaqa uchun boshqa hisob qilsa, u statik bo'lmasligi kerak.

**Nega muammo**: statik metodni override qilib bo'lmaydi va mock qilish qiyin (31.5). Kelajakdagi variant qo'shish uchun butun chaqiruv zanjirini o'zgartirish kerak.

**Tuzatish**: statik metodni instans metodiga aylantirish, keyin kerak bo'lsa strategiya interfeysiga chiqarish. Haqiqiy sof funksiyalar (`Math.abs`, `Ibans.isValid`) statik qoladi (14.8).

### 33.14 Bazaviy sinf vorisga bog'liq (Base Class Depending on Derivatives)

17.5 da ko'rilgan. Hid sifatida belgisi: bazaviy sinfda voris sinf nomlari, `instanceof` tekshiruvlari yoki voris sinflarga mos `switch`.

**Tuzatish**: abstrakt metod kiritish (Replace Conditional with Polymorphism), yoki bazaviy sinfni interfeysga aylantirish.

### 33.15 Majburiy sozlash kodi (Required Setup Code)

**Belgisi**: obyektni ishlatishdan oldin bir necha metodni ma'lum tartibda chaqirish kerak (6.9); yoki testda har safar 20 qatorlik sozlash yoziladi.

**Nega muammo**: tartib hech qayerda majburlanmagan va u buzilsa xato uzoqda chiqadi.

**Tuzatish**: konstruktorda to'liq qurish (14.9), builder (16.5), yoki "o'tkazish" uslubi (6.9). Testda esa builder va object mother (30.3).

### 33.16 Kombinatorik portlash (Combinatorial Explosion)

**Belgisi**: bir xil ishning har bir kombinatsiyasi uchun alohida metod yoki sinf: `findByCustomer`, `findByCustomerAndStatus`, `findByCustomerAndStatusAndDate`, va h.k. (28.5).

**Nega muammo**: har bir yangi o'lcham metod sonini ikki barobar oshiradi.

**Tuzatish**: Introduce Parameter Object (mezon obyekti), Specification pattern, yoki builder bilan so'rov qurish.

### 33.17 Amalda qo'llash

- [ ] Eng ko'p o'zgargan 10 sinf uchun `git log` dan o'zgarish sabablarini sanab, tarqoq o'zgarishni aniqlang.
- [ ] Faqat getter/setter dan iborat domen sinflarini topib, ularga tegishli mantiqni ko'chiring.
- [ ] Bir-birining private holatiga murojaat qiladigan sinf juftliklarini topib, chegarani qayta chizing.
- [ ] Bir xil vazifani bajaradigan, lekin turli imzolarga ega sinflarni umumiy interfeysga keltiring.
- [ ] Parallel ierarxiyalarni topib, ikkinchisini birinchisiga qo'shing yoki `sealed` ierarxiyaga o'tkazing.
- [ ] 20 dan ko'p public metodi bor sinf va interfeyslarni ro'yxatlab, ko'rinishni toraytiring.
- [ ] Izchilsizlik ro'yxatini tuzib (`Optional`/`null`, nomlash, inyeksiya), har biri uchun bitta konvensiya kelishib oling.
- [ ] Ishlatilmaydigan maydon, metod va importlarni IDE inspeksiyasi bilan topib o'chiring.
## 34. Toza kod evristikalarining to'liq ro'yxati (Clean Code Heuristics)

Bu bob toza kod evristikalarining klassik ro'yxatini to'liq beradi: izohlar (C), muhit (E), funksiyalar (F), umumiy (G), Java (J), nomlar (N) va testlar (T). Ro'yxat jadval shaklida, chunki uning vazifasi — review va o'z-o'zini tekshirish paytida tez ko'rib chiqish. Har bir satrda ushbu hujjatning yoki qardosh hujjatlarning tegishli bo'limiga havola bor.

### 34.1 Izohlar (C1-C5)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| C1 | Noo'rin ma'lumot | izohda o'zgarish tarixi, mualliflik, ticket tafsiloti | 9.5 |
| C2 | Eskirgan izoh | izoh koddan orqada qolgan | 9.3 |
| C3 | Ortiqcha izoh | kodni so'zma-so'z takrorlaydi | 9.2 |
| C4 | Yomon yozilgan izoh | g'o'ldirash, noaniq, uzun | 9.1, 9.9 |
| C5 | Izohga olingan kod | o'chirilishi kerak | 9.8 |

### 34.2 Muhit (E1-E2)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| E1 | Build bir qadamdan ko'p | `git clone` dan keyin bitta buyruq yetmaydi | 39.1 |
| E2 | Test bir qadamdan ko'p | testni ishga tushirish qo'lda sozlash talab qiladi | 39.2 |

### 34.3 Funksiyalar (F1-F4)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| F1 | Juda ko'p argument | uchdan ko'p argument asoslanishi kerak | 5.1 |
| F2 | Chiqish argumenti | argument orqali natija qaytarish | 5.5 |
| F3 | Flag argumenti | `boolean` parametr funksiyani ikkiga bo'ladi | 5.3 |
| F4 | O'lik funksiya | hech kim chaqirmaydi | 33.10 |

### 34.4 Umumiy evristikalar (G1-G12)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| G1 | Bir faylda bir necha til | Java ichida SQL, HTML, JSON aralash | 12.9, 28.6 |
| G2 | Aniq xatti-harakat amalga oshirilmagan | `Day.valueOf("Monday")` kutilgandek ishlamaydi | patternlar 26.22 |
| G3 | Chegarada noto'g'ri xatti-harakat | off-by-one, bo'sh to'plam, `null` | 6.7, 7.8 |
| G4 | Xavfsizlik mexanizmlari o'chirilgan | `@SuppressWarnings`, o'chirilgan test | 23.7, 30.9 |
| G5 | Takrorlanish | DRY buzilishi, uch turi bor | 32.2 |
| G6 | Noto'g'ri abstraksiya darajasidagi kod | past darajali tafsilot yuqori darajada | 4.2 |
| G7 | Bazaviy sinf vorisga bog'liq | ierarxiya teskari | 17.5, 33.14 |
| G8 | Haddan tashqari ko'p ma'lumot | keng public API | 33.8 |
| G9 | O'lik kod | erishilmaydigan shox, chaqirilmaydigan metod | 33.10 |
| G10 | Vertikal ajralish | e'lon va ishlatish orasida masofa | 11.5 |
| G11 | Izchilsizlik | bir narsa turli joyda turlicha | 33.9 |
| G12 | Keraksizlik (clutter) | bo'sh konstruktor, ishlatilmaydigan maydon | 33.10 |

### 34.5 Umumiy evristikalar (G13-G24)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| G13 | Sun'iy bog'liqlik | tegishli bo'lmagan narsalar birga | 33.11 |
| G14 | Begona ma'lumotga havas | metod boshqa sinf ma'lumotiga qiziqadi | patternlar 25.20 |
| G15 | Tanlov argumenti | `switch` ni argumentga ko'chirish | 5.4 |
| G16 | Yashirin niyat | zich, "aqlli" kod | 1.1, 9.10 |
| G17 | Noto'g'ri joylashgan javobgarlik | funksiya noto'g'ri sinfda | 33.12 |
| G18 | Noo'rin statik | statik metod polimorfizm talab qiladi | 33.13 |
| G19 | Tushuntiruvchi o'zgaruvchi ishlatish | oraliq natijaga nom berish | 6.1, 35-bob |
| G20 | Funksiya nomi nima qilishini aytsin | nom va xatti-harakat mos kelishi | 3.9, 4.6 |
| G21 | Algoritmni tushunish | ishlagani yetarli emas, tushunish kerak | 41.2 |
| G22 | Mantiqiy bog'liqlikni fizik qilish | taxminni oshkor qilish | 6.9, 35-bob |
| G23 | `if/else` o'rniga polimorfizm | turga qarab shoxlanish | 6.10, 32.7 |
| G24 | Standart konvensiyalarga rioya | jamoa uslubi, formatter | 13-bob |

### 34.6 Umumiy evristikalar (G25-G36)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| G25 | Magic number o'rniga konstanta | nomlangan konstanta | 3.4, patternlar 25.8 |
| G26 | Aniq bo'lish | `double` bilan pul, `null` siyosati, qulflash | 20.1, 18.7 |
| G27 | Konvensiyadan ustun tuzilish | tuzilish qoidani majburlasin | 17.4, 42.4 |
| G28 | Shartni inkapsulyatsiya qilish | shartni nomlash | 6.1 |
| G29 | Inkor shartdan qochish | ijobiy shart afzal | 6.2, 3.1 |
| G30 | Funksiya bitta ish qilsin | bo'linish sinovi | 4.2 |
| G31 | Yashirin vaqt bog'liqligi | tartib imzoda ko'rinmaydi | 6.9 |
| G32 | Tasodifiy bo'lmaslik | tuzilish sabab bilan tanlangan bo'lsin | 33.11 |
| G33 | Chegaraviy shartni inkapsulyatsiya | `i+1`, `<=` tarqalmasin | 6.7 |
| G34 | Bir darajadan pastga tushish | abstraksiya darajasi izchil | 4.2, patternlar 26.28 |
| G35 | Sozlanadigan ma'lumot yuqori darajada | konstanta yuqorida, chaqiruvda uzatiladi | 26.3 |
| G36 | O'tkinchi navigatsiyadan qochish | Demeter qonuni | 14.4, patternlar 26.15 |

### 34.7 Java ga xos evristikalar (J1-J3)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| J1 | Uzun import ro'yxatidan qochish | yulduzcha import haqida: **bu hujjat taqiqlaydi** | 12.7 |
| J2 | Konstantani voris olmaslik | constant interface anti-patterni | 17.8 |
| J3 | Konstanta emas, enum | enum xatti-harakat va tur xavfsizligi beradi | 3.5, 25.9 |

J1 bo'yicha izoh: klassik ro'yxat uzun import ro'yxatidan qochish uchun yulduzcha importni tavsiya qiladi. Zamonaviy amaliyot teskari: IDE importlarni o'zi boshqaradi va yulduzcha import nom konfliktlari bilan muammo tug'diradi (12.7). Shu sababli bu hujjatda J1 ning amaliy shakli — importlarni IDE va formatter boshqarishi, yulduzchani taqiqlash.

### 34.8 Nomlar (N1-N7)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| N1 | Tavsifiy nom tanlash | nom maqsadni ochib bersin | 2.1 |
| N2 | Abstraksiya darajasiga mos nom | nom implementatsiyani oshkor qilmasin | 2.13 |
| N3 | Standart nomenklaturadan foydalanish | pattern nomlari, konvensiyalar | 2.13, 3.6 |
| N4 | Noaniq nomlardan voz kechish | `doIt`, `handle`, `data` | 2.4, 32.1 |
| N5 | Katta qamrov uchun uzun nom | nom uzunligi qamrovga mutanosib | 2.15 |
| N6 | Kodlashdan voz kechish | Hungarian notation, prefikslar | 2.7 |
| N7 | Nom yon ta'sirni aytsin | `getOos()` aslida yaratadi | 3.9, patternlar 26.23 |

### 34.9 Testlar (T1-T9)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| T1 | Yetarlicha test yo'q | har bir shart va chegara qamralgan bo'lsin | testlash qo'llanmasi |
| T2 | Qamrov vositasidan foydalanish | qamralmagan shoxlarni ko'rsatadi | SonarQube hujjati 18 |
| T3 | Mayda testni e'tiborsiz qoldirmaslik | kichik test ham qoida hujjatlaydi | 30.1 |
| T4 | O'chirilgan testni tekshirish | `@Disabled` sababsiz qolmasin | 30.9 |
| T5 | Chegaraviy shartlarni sinash | oldin, chegarada, keyin | 7.8 |
| T6 | Xato atrofini to'liq sinash | bitta xato topilsa, atrofini ham sinash | 31.1 |
| T7 | Yiqilish naqshini o'rganish | yiqilgan testlar tartibi sababni ko'rsatadi | 41.3 |
| T8 | Qamrov naqshini o'rganish | qamralmagan qatorlar nimani bildiradi | SonarQube hujjati 11 |
| T9 | Sekin testlarni tezlashtirish | sekin test ishga tushirilmaydi | 30.9, 39.7 |

### 34.10 Evristikani review da ishlatish

66 ta evristikani har bir review da ko'rib chiqish amalda mumkin emas. Ishlaydigan yondashuv — **kichik to'plam** bilan boshlash va vaqt o'tib ularni mashinaga topshirish.

| Bosqich | Nima qilinadi |
|---|---|
| 1 | Mashina tekshiradiganlarini CI ga ko'chirish (C5, G5, G9, G12, J1, F4) |
| 2 | Jamoaga eng ko'p tegishli 10 evristikani tanlab, review checklistiga kiritish |
| 3 | Har chorakda ro'yxatni ko'rib chiqish: qaysi evristika hech qachon ishlamadi |
| 4 | Takrorlangan review izohini qoidaga aylantirish (42.5) |
| 5 | Qolgan evristikalarni o'z-o'zini tekshirish uchun qoldirish (49-bob) |

### 34.11 Amalda qo'llash

- [ ] 34-bobdagi 66 evristikani bir marta to'liq o'qib, kod bazasiga eng ko'p tegishli 10 tasini belgilang.
- [ ] Mashina tekshira oladigan evristikalarni Error Prone, Checkstyle va Sonar qoidalariga ko'chiring (42-bob).
- [ ] Review checklistiga tanlangan 10 evristikani qisqa shaklda kiriting (48.8).
- [ ] C1-C5 bo'yicha izohlarni bir marta to'liq ko'rib chiqib, tozalang.
- [ ] E1 va E2 ni tekshirish uchun yangi mashinada `git clone` dan keyin build va testni bir buyruq bilan ishga tushirib ko'ring.
- [ ] G25 bo'yicha kodni magic number uchun skanerlab, nomlangan konstantalar kiriting.
- [ ] N1-N7 bo'yicha eng ko'p o'zgaradigan 5 faylning nomlarini qayta ko'rib chiqing.
- [ ] T1-T9 bo'yicha test to'plamini baholab, eng sekin 10 testni ro'yxatlab tezlashtirish rejasini tuzing.
## 35. Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi (Refactoring Moves I)

Legacy kodni refaktoring qilish strategiyasi, chok (seam) topish va strangler usuli arxitektor hujjatida (34-bob). Bu va keyingi ikki bob boshqa narsani beradi: **mexanik harakatlar katalogi**. Har bir harakat uchun nima qilinishi, qachon qo'llanishi va teskari harakati berilgan. Teskari harakat muhim, chunki refaktoring ikki yo'nalishda ham to'g'ri bo'lishi mumkin.

### 35.1 Funksiya ajratish (Extract Function)

**Qachon**: kod bo'lagi alohida nom olishga arziydi; izoh yozish ehtiyoji tug'ilgan (8.2).

**Mexanika**: yangi funksiya yaratish va unga maqsadni aytuvchi nom berish → kod bo'lagini ko'chirish → mahalliy o'zgaruvchilarni parametr yoki qaytish qiymatiga aylantirish → kompilyatsiya va test → chaqiruvchini almashtirish.

**Teskari**: Inline Function (35.2).

```java
// Oldin
void printOwing(Invoice invoice) {
    System.out.println("***********************");
    System.out.println("**** Mijoz qarzi *****");
    System.out.println("***********************");
    Money outstanding = invoice.outstanding();
    System.out.println("Nomi: " + invoice.customer());
    System.out.println("Summa: " + outstanding);
}

// Keyin
void printOwing(Invoice invoice) {
    printBanner();
    printDetails(invoice, invoice.outstanding());
}
```

### 35.2 Funksiyani ichkariga kiritish (Inline Function)

**Qachon**: funksiya tanasi nomidan ravshanroq; keraksiz vositachilik (32.9).

**Mexanika**: barcha chaqiruvchilarni topish → har birini tana bilan almashtirish → funksiyani o'chirish → test.

**Teskari**: Extract Function.

### 35.3 O'zgaruvchi ajratish (Extract Variable)

**Qachon**: ifoda tushunish uchun nom talab qiladi (6.1, G19).

**Mexanika**: ifodadan oldin `final` o'zgaruvchi e'lon qilish → ifodani ko'chirish → asl joyni o'zgaruvchi bilan almashtirish.

```java
// Oldin
return order.quantity() * order.itemPrice()
        - Math.max(0, order.quantity() - 500) * order.itemPrice() * 0.05
        + Math.min(order.quantity() * order.itemPrice() * 0.1, 100);

// Keyin
Money basePrice = order.basePrice();
Money quantityDiscount = order.quantityDiscount();
Money shipping = order.shipping();
return basePrice.minus(quantityDiscount).plus(shipping);
```

**Teskari**: Inline Variable.

### 35.4 O'zgaruvchini ichkariga kiritish (Inline Variable)

**Qachon**: o'zgaruvchi nomi ifodadan ko'proq ma'lumot bermaydi (`boolean result = order.isPaid();`).

**Mexanika**: o'zgaruvchi `final` ekanini tekshirish → har bir ishlatilishni ifoda bilan almashtirish → e'lonni o'chirish.

### 35.5 Funksiya e'lonini o'zgartirish (Change Function Declaration)

**Qachon**: nom noaniq (32.1); parametr qo'shish yoki olib tashlash kerak; parametr turini kuchaytirish kerak (21.8).

**Mexanika (migratsiya bilan)**: eski funksiya tanasini yangi nomli funksiyaga ko'chirish → eski funksiyani yangisiga delegatsiya qiluvchi qilib qoldirish va `@Deprecated` qilish → chaqiruvchilarni bosqichma-bosqich ko'chirish → eski funksiyani o'chirish.

Bu "parallel o'zgarish" usuli public API uchun majburiy (arxitektor hujjati 13.9).

### 35.6 O'zgaruvchini inkapsulyatsiya qilish (Encapsulate Variable)

**Qachon**: ma'lumotga kirish joylari ko'p va uni o'zgartirish kerak; global ma'lumot (32.4).

**Mexanika**: ma'lumot uchun getter va setter funksiya yaratish → barcha to'g'ridan-to'g'ri murojaatlarni funksiya chaqiruviga almashtirish → ma'lumot ko'rinishini toraytirish → endi turni yoki tuzilishni xavfsiz o'zgartirish mumkin.

```java
// Oldin: global ma'lumot
public static List<Order> defaultOrders = new ArrayList<>();

// Keyin: kirish inkapsulyatsiyalangan, keyingi qadam - bog'liqlikka aylantirish
private static final List<Order> defaultOrders = new ArrayList<>();

public static List<Order> defaultOrders() { return List.copyOf(defaultOrders); }

public static void addDefaultOrder(Order order) { defaultOrders.add(order); }
```

### 35.7 O'zgaruvchini qayta nomlash (Rename Variable / Rename Field)

**Qachon**: nom maqsadni aytmaydi (32.1).

**Mexanika**: IDE refaktoringi bilan bajarish (3.15) → satr literallarini va reflektiv havolalarni alohida tekshirish → alohida commit qilish.

### 35.8 Parametr obyektini kiritish (Introduce Parameter Object)

**Qachon**: parametrlar guruhi birga sayohat qiladi (32.6); argument soni to'rtdan oshgan (5.1).

**Mexanika**: yangi `record` yaratish → yangi parametr bilan overload qo'shish → eski metodni yangisiga delegatsiya qilish → chaqiruvchilarni ko'chirish → eski metodni o'chirish → validatsiyani record ga ko'chirish (5.6).

### 35.9 Funksiyalarni sinfga birlashtirish (Combine Functions into Class)

**Qachon**: bir necha funksiya bir xil ma'lumot bilan ishlaydi va har biri shu ma'lumotni parametr sifatida oladi.

**Mexanika**: umumiy ma'lumotni maydon sifatida saqlaydigan sinf yaratish → funksiyalarni sinfga ko'chirish → parametrlarni maydonga aylantirish.

```java
// Oldin: har bir funksiya bir xil ma'lumotni oladi
Money baseCharge(Reading reading) { ... }
Money taxableCharge(Reading reading) { ... }
BigDecimal calculateBaseRate(Reading reading) { ... }

// Keyin: ma'lumot va mantiq birga
public final class ReadingCalculator {
    private final Reading reading;
    ReadingCalculator(Reading reading) { this.reading = reading; }
    Money baseCharge() { ... }
    Money taxableCharge() { ... }
}
```

### 35.10 Funksiyalarni transformatsiyaga birlashtirish (Combine Functions into Transform)

**Qachon**: bir xil kirish ma'lumotidan bir necha hosila qiymat hisoblanadi va hisob bir necha joyda takrorlanadi.

**Mexanika**: kirish ma'lumotidan boyitilgan nusxa qaytaruvchi funksiya yaratish → har bir hosila hisobni shu funksiyaga ko'chirish → chaqiruvchilarni natijadan o'qishga o'tkazish.

Bu Combine Functions into Class ning funksional varianti; o'zgarmas ma'lumot bilan ishlaganda afzal (16-bob).

### 35.11 Bosqichlarni ajratish (Split Phase)

**Qachon**: funksiya ikki ketma-ket ishni bajaradi — parslash keyin hisoblash, tayyorlash keyin yuborish.

**Mexanika**: ikkinchi bosqichni alohida funksiyaga ajratish → bosqichlar orasida oraliq ma'lumot tuzilmasi kiritish → birinchi bosqichni oraliq tuzilmani qaytaradigan qilish.

```java
// Keyin: ikki bosqich va ular orasidagi oraliq tur
record PriceData(int quantity, Money itemPrice, ShippingMethod shipping) { }

Money price(Order order) {
    return applyPrices(parsePriceData(order));
}
```

### 35.12 Funksiyani ko'chirish (Move Function)

**Qachon**: funksiya o'zi turgan sinfdan boshqa sinf ma'lumotiga ko'proq murojaat qiladi (noto'g'ri joylashgan javobgarlik, 33.12; feature envy).

**Mexanika**: funksiya ishlatadigan elementlarni tekshirish → maqsad sinfga nusxa ko'chirish → asl joyni delegatsiyaga aylantirish → chaqiruvchilarni ko'chirish → asl funksiyani o'chirish.

### 35.13 Gaplarni funksiyaga ko'chirish va chaqiruvchiga chiqarish

**Move Statements into Function**: bir xil gap har bir chaqiruv joyida funksiyadan oldin/keyin takrorlanadi → uni funksiya ichiga ko'chirish.

**Move Statements to Callers**: teskari holat — funksiya ichidagi gap chaqiruvchilarning bir qismi uchun to'g'ri emas → uni chaqiruvchilarga chiqarish.

Ikkisi juft harakat va ular funksiya chegarasini aniqlashtirishga xizmat qiladi.

### 35.14 Inline kodni funksiya chaqiruviga almashtirish

**Qachon**: kod bo'lagi mavjud funksiya bilan bir xil ishni qiladi (takrorlanish, 32.2).

**Mexanika**: kod bo'lagi va funksiya aynan bir xil xatti-harakat berishini tekshirish → kodni chaqiruv bilan almashtirish → test.

### 35.15 Gaplarni surish (Slide Statements)

**Qachon**: bog'liq kod bir joyda to'planmagan; e'lon va ishlatish orasida masofa bor (11.5, G10).

**Mexanika**: ko'chirilayotgan gap va orasidagi gaplar o'rtasida bog'liqlik yo'qligini tekshirish (o'qish/yozish ziddiyati) → gapni surish → test.

Bu harakat ko'pincha Extract Function dan oldin bajariladi: oldin bog'liq kod yoniga yig'iladi, keyin ajratiladi.

### 35.16 Siklni bo'lish (Split Loop)

**Qachon**: bir sikl ikki mustaqil ishni bajaradi (7.3).

**Mexanika**: siklni nusxalash → har bir nusxada faqat bitta ishni qoldirish → test → har bir siklni Extract Function bilan nomlash.

### 35.17 Siklni quvurga almashtirish (Replace Loop with Pipeline)

**Qachon**: sikl filtrlash va mapping qiladi (32.8), va 7.7 mezoni quvurni afzal ko'rsatadi.

**Mexanika**: sikldan oldin to'plamni `stream()` ga olish → har bir sikl ichidagi amalni mos quvur amaliga aylantirish (filtr → `filter`, o'zgartirish → `map`, yig'ish → `collect`) → sikl bo'sh qolganda o'chirish.

### 35.18 O'lik kodni o'chirish (Remove Dead Code)

**Qachon**: kod chaqirilmaydi yoki shart hech qachon bajarilmaydi (33.10, G9).

**Mexanika**: IDE inspeksiyasi va qamrov hisoboti bilan tasdiqlash → o'chirish → **izohga olmaslik** (9.8) → test.

Refleksiya, Spring, Jackson va test orqali chaqirilishi mumkin bo'lgan kodni tekshirish kerak: statik tahlil ularni "o'lik" deb ko'rsatadi.

### 35.19 O'zgaruvchini bo'lish (Split Variable)

**Qachon**: bitta o'zgaruvchi bir necha maqsadda ishlatiladi (`temp` ikki marta boshqa qiymat uchun).

**Mexanika**: har bir maqsad uchun yangi `final` o'zgaruvchi kiritish → mos ishlatilishlarni almashtirish → test → nomlarni aniqlashtirish.

```java
// Oldin: temp ikki maqsadda
double temp = 2 * (height + width);
System.out.println(temp);
temp = height * width;
System.out.println(temp);

// Keyin
final double perimeter = 2 * (height + width);
final double area = height * width;
```

### 35.20 Hosila o'zgaruvchini so'rovga almashtirish

**Qachon**: maydon boshqa maydonlardan hisoblanadi, lekin alohida saqlanadi va sinxron ushlash kerak (32.5).

**Mexanika**: hosila maydonni hisoblaydigan metod yaratish → o'qish joylarini metodga o'tkazish → maydonni va uni yangilaydigan kodni o'chirish.

```java
// Oldin: total maydoni va uni yangilash mantiqi
private Money total;
public void addLine(OrderLine line) { lines.add(line); total = total.plus(line.amount()); }

// Keyin: hisob so'rov vaqtida
public Money total() {
    return lines.stream().map(OrderLine::amount).reduce(Money.ZERO, Money::plus);
}
```

Agar hisob qimmat bo'lsa va o'lchov muammo ko'rsatsa, keshlash qo'shiladi — lekin oldin o'lchov (1.5).

### 35.21 Amalda qo'llash

- [ ] Eng uzun 10 metodda Extract Function ni ketma-ket qo'llab, har qadamdan keyin test ishga tushiring.
- [ ] Murakkab ifodalarni Extract Variable bilan nomlab, keyin ularni domen metodlariga ko'chirishni ko'rib chiqing.
- [ ] Bir necha maqsadda ishlatilgan mahalliy o'zgaruvchilarni Split Variable bilan ajratib, nomlarini aniqlashtiring.
- [ ] Hosila maydonlarni (`total`, `count`) so'rov metodlariga almashtirib, sinxronlash kodini o'chiring.
- [ ] Noto'g'ri sinfda turgan funksiyalarni Move Function bilan egasiga ko'chiring.
- [ ] Ikki ishni bajaradigan sikllarni Split Loop bilan bo'lib, har birini nomlang.
- [ ] 7.7 mezoniga mos sikllarni Replace Loop with Pipeline bilan quvurga o'tkazing.
- [ ] O'lik kodni qamrov hisoboti bilan tasdiqlab o'chiring va alohida commit qiling.
## 36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya (Refactoring Moves II)

Bu bob ma'lumot tuzilishini o'zgartiradigan harakatlarni qamrab oladi: sinf ajratish va birlashtirish, to'plamni inkapsulyatsiya qilish, primitivni obyektga aylantirish, havola va qiymat o'rtasida o'tish. Bu harakatlar 14-16 boblardagi qoidalarga olib boradigan mexanik yo'l.

### 36.1 Sinf ajratish (Extract Class)

**Qachon**: sinf bir necha javobgarlikni oladi (tarqoq o'zgarish, 33.1); maydonlarning bir guruhi birga ishlatiladi; vaqtinchalik maydonlar bor (32.10).

**Mexanika**: yangi sinf yaratish → bog'liqlikni asl sinfdan yangisiga o'rnatish → maydonlarni bittadan Move Field bilan ko'chirish → har bir ko'chirishdan keyin test → metodlarni Move Function bilan ko'chirish → interfeysni ko'rib chiqib keraksizni yopish.

```java
// Oldin: Person ichida telefon ma'lumoti
class Person {
    private String name;
    private String officeAreaCode;
    private String officeNumber;
    String telephoneNumber() { return "(" + officeAreaCode + ") " + officeNumber; }
}

// Keyin: telefon o'z turida, invarianti bilan
record TelephoneNumber(String areaCode, String number) {
    @Override public String toString() { return "(%s) %s".formatted(areaCode, number); }
}

class Person {
    private String name;
    private TelephoneNumber officePhone;
}
```

### 36.2 Sinfni ichkariga kiritish (Inline Class)

**Qachon**: sinf endi javobgarligini yo'qotgan (dangasa element, 32.9); yoki ikki sinf noo'rin yaqinlikda (33.3) va ularni birlashtirish aniqroq.

**Mexanika**: maqsad sinfda manba sinfning public metodlariga mos delegatsiya metodlari yaratish → chaqiruvchilarni maqsad sinfga o'tkazish → maydon va metodlarni ko'chirish → manba sinfni o'chirish.

### 36.3 Delegatni yashirish (Hide Delegate)

**Qachon**: chaqiruvchi ikki darajali zanjir orqali murojaat qiladi (32.11).

**Mexanika**: serverga delegatsiya metodi qo'shish → chaqiruvchilarni shu metodga o'tkazish → delegatga kirishni (getter) olib tashlash.

```java
// Oldin: chaqiruvchi ikki turni biladi
Manager manager = person.department().manager();

// Keyin: Person delegatsiya qiladi, Department yashirin
Manager manager = person.manager();

class Person {
    private Department department;
    Manager manager() { return department.manager(); }
}
```

### 36.4 Vositachini olib tashlash (Remove Middle Man)

**Qachon**: 36.3 ning teskarisi — delegatsiya metodlari ko'payib ketgan va sinf vositachiga aylangan (32.12).

**Mexanika**: delegatga kirish metodi (getter) qo'shish → chaqiruvchilarni delegatga to'g'ridan-to'g'ri murojaatga o'tkazish → keraksiz delegatsiya metodlarini o'chirish.

### 36.5 Maydonni ko'chirish (Move Field)

**Qachon**: maydon boshqa sinfda ko'proq ishlatiladi; maydonlar guruhi birga o'zgaradi; bitta maydonni o'zgartirish ikki sinfga tegadi.

**Mexanika**: maydonni inkapsulyatsiya qilish (35.6) → maqsad sinfda maydon va kirish metodlarini yaratish → asl sinfni maqsad sinfga delegatsiya qilish → chaqiruvchilarni ko'chirish → asl maydonni o'chirish.

### 36.6 Yozuvni inkapsulyatsiya qilish (Encapsulate Record)

**Qachon**: o'zgaradigan ma'lumot tuzilmasi (`Map<String, Object>`, ochiq maydonlar) kod bo'ylab tarqalgan.

**Mexanika**: ma'lumotni ushlaydigan sinf yaratish → kirish metodlari qo'shish → barcha murojaatlarni metodlarga o'tkazish → ichki tuzilmani yashirish → endi turni o'zgartirish xavfsiz.

```java
// Oldin: shartnomasiz map - kalitlar hech qayerda hujjatlanmagan
Map<String, Object> organization = Map.of("name", "Shop", "country", "UZ");

// Keyin: tur shartnomani ushlaydi
record Organization(String name, CountryCode country) { }
```

### 36.7 To'plamni inkapsulyatsiya qilish (Encapsulate Collection)

**Qachon**: getter ichki to'plamni qaytaradi va tashqi kod uni o'zgartiradi (14.7).

**Mexanika**: to'plamga element qo'shish va o'chirish uchun metodlar qo'shish (`addLine`, `removeLine`) → getter ni o'zgartirilmas nusxa yoki ko'rinish qaytaradigan qilish → setter ni o'chirish → to'g'ridan-to'g'ri o'zgartirgan chaqiruvchilarni yangi metodlarga ko'chirish.

### 36.8 Primitivni obyektga almashtirish (Replace Primitive with Object)

**Qachon**: primitiv qiymat atrofida mantiq paydo bo'ladi — validatsiya, formatlash, solishtirish (patternlar hujjati 25.19; 21.8).

**Mexanika**: yangi `record` yaratish → maydon turini almashtirish → getter ni yangi tur qaytaradigan qilish → chaqiruvchilarni bosqichma-bosqich ko'chirish → mantiqni yangi turga ko'chirish.

```java
// Oldin
private String priority;          // "high", "HIGH", "urgent"? - qoida yo'q

// Keyin
private Priority priority;        // enum yoki record, invariant bilan

public enum Priority {
    LOW, NORMAL, HIGH, URGENT;

    public boolean isHigherThan(Priority other) { return ordinal() > other.ordinal(); }
}
```

### 36.9 Vaqtinchalikni so'rovga almashtirish (Replace Temp with Query)

**Qachon**: mahalliy o'zgaruvchi ifodani ushlab turadi va shu ifoda boshqa joyda ham kerak.

**Mexanika**: o'zgaruvchi `final` va bir marta tayinlanganini tekshirish → o'ng tomonni metodga chiqarish → o'zgaruvchi ishlatilishlarini metod chaqiruvi bilan almashtirish → o'zgaruvchini o'chirish.

Bu harakat Extract Function dan oldin bajariladi va uni osonlashtiradi: parametrlar soni kamayadi.

### 36.10 Havolani qiymatga almashtirish (Change Reference to Value)

**Qachon**: ichki obyekt o'zgarmas bo'lishi mumkin va u o'zi mustaqil identifikatorga ega bo'lishi shart emas (15.5).

**Mexanika**: ichki obyektni o'zgarmas qilish (barcha setter larni yo'qotish) → `equals` va `hashCode` ni qiymat bo'yicha yozish (yoki `record` ga aylantirish) → ichki obyektni almashtirishni yangi nusxa yaratishga o'tkazish.

```java
// Oldin: ichki obyekt havola bo'yicha, o'zgaradi
order.telephone().setAreaCode("71");

// Keyin: qiymat, almashtirish yangi nusxa bilan
order = order.withTelephone(new TelephoneNumber("71", "2001234"));
```

### 36.11 Qiymatni havolaga almashtirish (Change Value to Reference)

**Qachon**: bir xil mantiqiy obyektning nusxalari ko'p va ularni bir vaqtda o'zgartirish kerak (mijoz ma'lumoti har bir buyurtmada nusxalangan).

**Mexanika**: obyektlar uchun repository yoki registry yaratish → yaratish joyini repository ga o'tkazish → nusxa o'rniga havola saqlash.

Bu harakat 36.10 ning teskarisi va u kamdan-kam kerak bo'ladi: nusxani havolaga aylantirish bog'liqlik qo'shadi.

### 36.12 Sozlash metodini olib tashlash (Remove Setting Method)

**Qachon**: maydon yaratilgandan keyin o'zgarmasligi kerak (16.7).

**Mexanika**: maydonni konstruktor parametriga aylantirish → barcha setter chaqiruvchilarini konstruktorga o'tkazish → setter ni o'chirish → maydonni `final` qilish.

### 36.13 Konstruktorni fabrika funksiyasiga almashtirish

**Qachon**: yaratish mantiqi oddiy `new` dan ko'proq; nom kerak (2.9); yaratish turi dinamik tanlanadi.

**Mexanika**: statik fabrika metodi yaratish → konstruktorni chaqirish → konstruktorni `private` qilish → chaqiruvchilarni fabrikaga o'tkazish.

```java
// Keyin: nom maqsadni aytadi, invariant tekshiriladi
public static Money ofMinorUnits(long minorUnits, Currency currency) { ... }
public static Money zero(Currency currency) { ... }
public static Money parse(String text) { ... }
```

### 36.14 Funksiyani buyruqqa va buyruqni funksiyaga almashtirish

**Replace Function with Command**: funksiya murakkab, ko'p mahalliy o'zgaruvchi va bosqichga ega → uni obyektga aylantirish (maydonlar mahalliy o'zgaruvchilarni almashtiradi), keyin ichini Extract Function bilan bo'lish oson bo'ladi.

**Replace Command with Function**: teskari — buyruq obyekti faqat bitta `execute` metodidan iborat va holat saqlamaydi → oddiy funksiyaga qaytarish (32.9).

### 36.15 Maydon va metodni yuqoriga/pastga ko'chirish

Ierarxiya bilan ishlashning to'rt juft harakati bor va ularning hammasi bir xil mexanikaga ega: tekshirish, ko'chirish, test.

| Harakat | Qachon |
|---|---|
| Pull Up Method | bir xil metod bir necha vorisda (qardosh takrorlanish, 32.2) |
| Pull Up Field | bir xil maydon bir necha vorisda |
| Pull Up Constructor Body | konstruktorlar boshida bir xil kod |
| Push Down Method | metod faqat bir vorisga tegishli (rad etilgan meros, 33.5) |
| Push Down Field | maydon faqat bir vorisda ishlatiladi |

Eslatma: yuqoriga ko'chirish vorislikni kuchaytiradi; agar natijada bazaviy sinf shishsa, kompozitsiyani ko'rib chiqish kerak (17.9).

### 36.16 Amalda qo'llash

- [ ] Bir necha javobgarlikka ega sinflarni Extract Class bilan bo'lib, har bir ko'chirishdan keyin test ishga tushiring.
- [ ] Ichki to'plamni qaytaradigan getter larni Encapsulate Collection bilan yoping.
- [ ] `Map<String, Object>` tarqalgan joylarni Encapsulate Record bilan turga aylantiring.
- [ ] Atrofida mantiq to'plangan primitivlarni Replace Primitive with Object bilan value object ga o'tkazing.
- [ ] Yaratilgandan keyin o'zgarmasligi kerak bo'lgan maydonlarning setter larini olib tashlang.
- [ ] Murakkab konstruktorlarni nomlangan statik fabrikalarga o'tkazing.
- [ ] Ikki darajali chaqiruv zanjirlarini Hide Delegate bilan yopib, delegat getter larini olib tashlang.
- [ ] Voris sinflardagi takrorlangan metod va maydonlarni Pull Up bilan birlashtiring, keyin bazaviy sinf hajmini tekshiring.
## 37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya (Refactoring Moves III)

Bu bob shartli mantiqni, API shaklini va vorislik ierarxiyasini o'zgartiradigan harakatlarni qamrab oladi. Ular 6, 17 va 5 boblardagi qoidalarga olib boradigan mexanik yo'l.

### 37.1 Shartni parchalash (Decompose Conditional)

**Qachon**: `if` sharti yoki shoxlari murakkab (6.1).

**Mexanika**: shartni Extract Function bilan nomlangan metodga chiqarish → har bir shoxni ham alohida metodga chiqarish → natijada uch qatorli `if/else` qoladi.

```java
// Keyin
if (isSummerPeriod(date)) {
    charge = summerCharge(quantity);
} else {
    charge = winterCharge(quantity);
}
```

### 37.2 Shartli ifodalarni birlashtirish (Consolidate Conditional Expression)

**Qachon**: bir necha shart bir xil natijaga olib boradi (6.3).

**Mexanika**: shartlarni `||` yoki `&&` bilan birlashtirish → birlashgan shartni Extract Function bilan nomlash → test.

```java
// Oldin
if (employee.seniority() < 2) return 0;
if (employee.monthsDisabled() > 12) return 0;
if (employee.isPartTime()) return 0;

// Keyin
if (isNotEligibleForDisability(employee)) return 0;
```

### 37.3 Ichma-ich shartni guard clause ga almashtirish

Erta qaytish arxitektor hujjatida (4.4) ko'rilgan; bu yerda mexanikasi: eng tashqi shartni olib, uni teskari aylantirish va darhol qaytarish → qolgan shartlarni ketma-ket shu tarzda chiqarish → har qadamdan keyin test.

Qoida: guard clause **istisnoli** holatlar uchun, `if/else` esa teng huquqli shoxlar uchun. Ikki shox ham normal bo'lsa, guard clause ishlatilmaydi.

### 37.4 Shartni polimorfizmga almashtirish (Replace Conditional with Polymorphism)

**Qachon**: `switch` yoki `if/else` turga qarab shoxlanadi va u takrorlanadi (32.7, G23).

**Mexanika**: ierarxiya yoki enum yaratish → har bir shoxni mos turga ko'chirish → bazaviy metodni abstrakt qilish → `switch` ni polimorf chaqiruv bilan almashtirish.

Java da uch variant bor va ularning tanlovi aniq:

| Variant | Qachon |
|---|---|
| Enum ichida xatti-harakat | variantlar soni barqaror, mantiq kichik (6.10) |
| `sealed` interfeys + pattern matching | variantlar har xil ma'lumotga ega (25.3) |
| Ierarxiya va polimorfizm | variantlar o'z holatiga ega |

### 37.5 Maxsus holatni kiritish (Introduce Special Case)

**Qachon**: bir xil `null` yoki maxsus qiymat tekshiruvi kod bo'ylab takrorlanadi (18.6).

**Mexanika**: maxsus holat uchun sinf yaratish → u standart xatti-harakatni beradi → `null` qaytaradigan joyni maxsus holat obyekti qaytaradigan qilish → tekshiruvlarni bittadan o'chirish.

```java
// Maxsus holat: noma'lum mijoz
final class UnknownCustomer implements Customer {
    public String name() { return "noma'lum"; }
    public BillingPlan billingPlan() { return BillingPlan.basic(); }
    public boolean isUnknown() { return true; }
}
```

### 37.6 Assertion kiritish (Introduce Assertion)

**Qachon**: kod ma'lum taxminga asoslangan, lekin taxmin hech qayerda yozilmagan (G22).

**Mexanika**: taxminni oshkor tekshiruvga aylantirish — public chegarada istisno (18.10), ichki kodda `assert` yoki `Objects.requireNonNull` (19.8-19.9).

Qoida: assertion **hujjat** vazifasini bajaradi va u bajarilmasligi kerak — agar u ishga tushsa, kod xato.

### 37.7 So'rovni o'zgartirishdan ajratish (Separate Query from Modifier)

**Qachon**: metod ham qiymat qaytaradi, ham holatni o'zgartiradi (patternlar hujjati 26.23).

**Mexanika**: faqat so'rov qiladigan yangi metod yaratish → asl metodni so'rov metodini chaqiradigan qilish → chaqiruvchilarni ikki chaqiruvga ajratish → asl metoddan qaytish qiymatini olib tashlash.

```java
// Oldin
String alertForMiscreant(List<String> people);   // topadi va signal yuboradi

// Keyin
Optional<String> findMiscreant(List<String> people);   // faqat so'rov
void alertFor(String miscreant);                        // faqat amal
```

### 37.8 Funksiyani parametrlash (Parameterize Function)

**Qachon**: bir necha funksiya bir xil tuzilishga ega, faqat qiymatlar farq qiladi (shaklli takrorlanish, 32.2).

**Mexanika**: eng umumiy funksiyani tanlash → farq qiladigan qiymatni parametrga aylantirish → boshqa funksiyalarni yangi funksiyaga delegatsiya qilish → chaqiruvchilarni ko'chirish → eski funksiyalarni o'chirish.

```java
// Oldin
void tenPercentRaise(Employee e) { e.raiseBy(0.10); }
void fivePercentRaise(Employee e) { e.raiseBy(0.05); }

// Keyin
void raise(Employee employee, BigDecimal factor) { employee.raiseBy(factor); }
```

### 37.9 Flag argumentini olib tashlash (Remove Flag Argument)

5.3 da ko'rilgan. Mexanikasi: har bir flag qiymati uchun aniq nomlangan metod yaratish → asl metodni `private` qilish → chaqiruvchilarni yangi metodlarga ko'chirish.

### 37.10 Butun obyektni saqlash (Preserve Whole Object)

**Qachon**: chaqiruvchi obyektdan bir necha qiymat ajratib olib, ularni parametr sifatida uzatadi (5.7).

**Mexanika**: butun obyektni oladigan yangi parametr qo'shish → ichida eski parametrlardan foydalanishni obyekt metodlariga o'tkazish → eski parametrlarni olib tashlash.

### 37.11 Parametrni so'rovga va so'rovni parametrga almashtirish

**Replace Parameter with Query**: parametr qiymatini funksiya o'zi aniqlay oladi (obyekt holatidan) → parametrni olib tashlash va ichida hisoblash. Bog'liqlikni kamaytiradi, lekin funksiyani holatga bog'laydi.

**Replace Query with Parameter**: teskari — funksiya global yoki tashqi holatga murojaat qiladi → shu qiymatni parametrga chiqarish. Funksiyani sof qiladi va test qilishni osonlashtiradi (31.3).

Ikkinchisi ko'pincha afzal, chunki sof funksiya testlanadi va keshlanadi.

### 37.12 Algoritmni almashtirish (Substitute Algorithm)

**Qachon**: mavjud algoritmdan ravshanroq yoki samaraliroq variant bor.

**Mexanika**: mavjud xatti-harakatni to'liq qamrab oladigan testlar yozish → yangi algoritmni yozish → testlarni ishga tushirish → eski kodni o'chirish.

Bu harakatni test qamrovisiz bajarish mumkin emas: u xatti-harakatni saqlashi kerak, lekin ichini to'liq o'zgartiradi (arxitektor hujjati 34.3 xavfsizlik to'ri haqida).

### 37.13 Turni kodlashdan voris sinflarga almashtirish

**Qachon**: tur kodi (`String type`, `int kind`) xatti-harakatni belgilaydi va u bo'yicha shoxlanish bor.

**Mexanika**: tur kodini inkapsulyatsiya qilish → har bir qiymat uchun voris sinf yaratish (yoki enum a'zosi) → shoxli metodlarni Push Down bilan tarqatish → tur kodini o'chirish.

### 37.14 Voris sinfni delegatsiyaga almashtirish

17.9 da ko'rilgan. Mexanikasi: delegat maydon qo'shish → `extends` ni olib tashlash → kompilyator ko'rsatgan metodlarni delegatsiyaga aylantirish → keraksizlarini o'chirish → test.

**Replace Superclass with Delegate** — xuddi shu harakatning bazaviy sinf tomoni: `extends HashMap` kabi noto'g'ri vorislikni yo'qotadi.

### 37.15 Voris sinfni va ierarxiyani yo'qotish

**Remove Subclass**: voris sinf endi farq qilmaydi (bazaviy sinf bilan bir xil xatti-harakat) → maydonni bazaviy sinfga ko'chirish, voris sinfni o'chirish.

**Collapse Hierarchy**: bazaviy va voris sinf bir-biridan deyarli farq qilmaydi → birlashtirish (32.9).

**Extract Superclass**: ikki sinfda umumiy qism bor → bazaviy sinf ajratish. Eslatma: avval interfeys yoki kompozitsiya variantini ko'rib chiqish kerak (17.7).

### 37.16 Refaktoring harakatini tanlash jadvali

Hid topilganda qaysi harakatni qo'llash kerakligini tez aniqlash uchun jadval.

| Hid | Birinchi harakat | Keyingi |
|---|---|---|
| Uzun funksiya | Extract Function | Replace Temp with Query |
| Sirli nom | Rename | Change Function Declaration |
| Takrorlangan kod | Extract Function | Pull Up Method |
| Uzun parametr ro'yxati | Introduce Parameter Object | Preserve Whole Object |
| Ma'lumot to'dasi | Extract Class | Introduce Parameter Object |
| Primitivlarga berilish | Replace Primitive with Object | Extract Class |
| Takrorlangan `switch` | Replace Conditional with Polymorphism | Move Function |
| Sikllar | Replace Loop with Pipeline | Split Loop |
| Global ma'lumot | Encapsulate Variable | inyeksiya |
| O'zgaradigan ma'lumot | Remove Setting Method | Change Reference to Value |
| Tarqoq o'zgarish | Split Phase | Extract Class |
| Feature envy | Move Function | Extract Function |
| Xabar zanjiri | Hide Delegate | Move Function |
| Vositachi | Remove Middle Man | Inline Function |
| Ma'lumot sinfi | Move Function | Encapsulate Record |
| Rad etilgan meros | Push Down Method | Replace Superclass with Delegate |
| Vaqtinchalik maydon | Extract Class | Introduce Special Case |
| Dangasa element | Inline Function | Collapse Hierarchy |
| Flag argumenti | Remove Flag Argument | Parameterize Function |
| `null` tekshiruvi zanjiri | Introduce Special Case | Encapsulate Variable |

### 37.17 Amalda qo'llash

- [ ] Murakkab shartlarni Decompose Conditional va Consolidate Conditional bilan soddalashtiring.
- [ ] Takrorlangan turga qarab shoxlanishni enum, `sealed` yoki ierarxiyaga o'tkazing (37.4 jadvali).
- [ ] Takrorlangan `null` tekshiruvlarini Introduce Special Case bilan yo'qoting.
- [ ] Ham qiymat qaytaradigan, ham holatni o'zgartiradigan metodlarni ikkiga ajrating.
- [ ] Bir xil tuzilishli funksiya guruhlarini Parameterize Function bilan birlashtiring.
- [ ] Obyektdan maydon ajratib uzatadigan chaqiruvlarni Preserve Whole Object bilan soddalashtiring.
- [ ] To'plamlardan voris olgan sinflarni Replace Superclass with Delegate bilan tuzating.
- [ ] 37.16 jadvalini jamoa bilan ko'rib chiqib, review izohlarida harakat nomini ishlatishni odat qiling.
## 38. Refaktoringni xavfsiz bajarish (Safe Refactoring Mechanics)

Refaktoring xatti-harakatni o'zgartirmasdan tuzilishni yaxshilash. "Xatti-harakatni o'zgartirmasdan" qismi uni xavfli qiladi: har bir qadam regressiya kiritishi mumkin. Bu bobda shu xavfni nolga yaqinlashtiradigan intizom. Legacy kodda chok topish va bosqichma-bosqich almashtirish strategiyasi arxitektor hujjatida (34-bob).

### 38.1 Bir vaqtda bitta harakat

Eng muhim qoida: bir vaqtda bitta refaktoring harakati bajariladi va undan keyin kompilyatsiya va test ishga tushiriladi. Ikki harakatni birlashtirish vaqt tejaydi deb o'ylash odatiy xato — aslida xato topilganda qaysi harakat sabab bo'lganini aniqlash uchun ikkisini ham qaytarish kerak bo'ladi.

```bash
# Har bir harakatdan keyin: tez testlar (butun to'plam emas)
./mvnw -q -pl payment test -Dtest='*Test' -DfailIfNoTests=false

# Harakat ishladi: commit qilib, keyingisiga o'tish (kichik, qaytariladigan qadamlar)
git add -A && git commit -m "refactor: Payment dan TelephoneNumber ni ajratish"
```

### 38.2 Kompilyator va test bilan boshqarish

Refaktoring paytida kompilyator va testlar ikki xil rol o'ynaydi. **Kompilyator** tuzilish o'zgarishini boshqaradi: maydonni o'chirsangiz, u barcha ishlatilishlarni ko'rsatadi. **Testlar** xatti-harakatni himoya qiladi: mantiq o'zgarsa, ular yiqiladi.

Shu sababli ikki xil refaktoring bor. Kompilyator boshqaradigan harakatlar (rename, move, signature change) nisbatan xavfsiz — IDE ularni bajaradi. Mantiqqa tegadigan harakatlar (Substitute Algorithm, Replace Conditional with Polymorphism) esa **faqat** test bilan xavfsiz.

Agar testlar yo'q bo'lsa, birinchi qadam — xatti-harakatni qayd etuvchi test yozish (arxitektor hujjati 34.3), refaktoring emas.

### 38.3 IDE refaktoringiga ishonish chegarasi

IDE refaktoringi qo'lda o'zgartirishdan ancha xavfsiz, lekin u hamma narsani ko'rmaydi. To'rt joyda IDE ni tekshirish kerak.

| Xavf | Nega IDE ko'rmaydi | Tekshiruv |
|---|---|---|
| Satr literalidagi nom | matn sifatida saqlangan | `grep` bilan qidirish (3.15) |
| Refleksiya va `Class.forName` | ish vaqtida hal qilinadi | grep + integratsion test |
| Spring XML va `@Value` kalitlari | kod emas | konfiguratsiyani grep |
| JPA `@Query` ichidagi maydon nomi | satr | repository testlari |
| Jackson `@JsonProperty` nomlari | API shartnomasi | contract test |
| SQL migratsiyalari | alohida fayl | migratsiya testi |

### 38.4 Refaktoringni mantiq o'zgarishidan ajratish

Bu qoida 13.6 (formatlash) ning umumiy shakli va u review sifatini belgilaydi: bitta commitda ham refaktoring, ham yangi xatti-harakat bo'lmasligi kerak.

Sababi aniq: refaktoring commitida diff katta bo'ladi, lekin reviewer "xatti-harakat o'zgarmaganini" bilib turadi va tezda o'tadi. Aralash commitda esa har bir qatorni tekshirish kerak va xato o'tib ketadi.

```bash
# Ikki commit, ikki maqsad
git commit -m "refactor: SettlementService dan import mantiqini ajratish"
git commit -m "feat: import faylida valyuta tekshiruvini qo'shish"
```

Amaliy tartib: oldin refaktoring (kodni o'zgarish uchun tayyorlash), keyin xatti-harakat o'zgarishi. Teskari tartib ham ishlaydi, lekin aralashtirish ishlamaydi.

### 38.5 Katta refaktoringni bo'lish: abstraksiya orqali shox

Katta refaktoringni bir PR da bajarish deyarli har doim muvaffaqiyatsiz bo'ladi: branch uzoq yashaydi, konfliktlar yig'iladi, review imkonsiz bo'ladi (arxitektor hujjati 34.6).

**Branch by abstraction** usuli katta refaktoringni kichik, merge qilinadigan qadamlarga bo'ladi:

1. Mavjud implementatsiya ustiga abstraksiya (interfeys) qo'yish va barcha chaqiruvchilarni unga o'tkazish. Merge qilinadi.
2. Yangi implementatsiyani abstraksiya ortida yozish, hali ishlatilmaydi. Merge qilinadi.
3. Konfiguratsiya yoki feature flag bilan trafikni bosqichma-bosqich yangisiga o'tkazish (41.5). Merge qilinadi.
4. Eski implementatsiyani o'chirish. Merge qilinadi.

Har bir qadam mustaqil ravishda production ga chiqadi va orqaga qaytarish oson.

### 38.6 Refaktoringni to'xtatish nuqtasi

Refaktoring cheksiz davom etishi mumkin va bu alohida xavf: "yana bir oz yaxshilayman" dan PR ikki haftaga cho'ziladi. To'xtatish uchun oldindan belgilangan shartlar kerak.

| To'xtatish sharti | Sabab |
|---|---|
| Asl vazifa bajarildi va kod toza | maqsadga erishildi |
| Refaktoring PR qamrovidan chiqdi | alohida PR ga ko'chiriladi (1.4) |
| Keyingi qadam test talab qiladi | oldin test, keyin davom |
| Qaror arxitektura darajasiga chiqdi | ADR kerak (arxitektor hujjati 3-bob) |
| Vaqt budjeti tugadi | qolgani ro'yxatga yoziladi |
| Foyda noaniq bo'lib qoldi | to'xtash va o'lchash |

Oxirgi qator eng muhim: agar refaktoringdan keyin kod yaxshilangani haqida ishonch yo'q bo'lsa, o'zgarishni qaytarish to'g'ri qaror.

### 38.7 Refaktoring va ishlash: o'lchovsiz qadam qo'ymaslik

Refaktoring odatda ishlashga ta'sir qilmaydi, lekin ba'zi harakatlar qiladi: Replace Derived Variable with Query (35.20) hisobni har chaqiruvda bajaradi, Extract Function qo'shimcha chaqiruv qo'shadi (JIT odatda inline qiladi), Replace Loop with Pipeline qo'shimcha obyektlar yaratadi.

Qoida: refaktoringni o'qilishi uchun bajarish, keyin o'lchash. Agar o'lchov muammo ko'rsatsa, maqsadli optimizatsiya qilish va **nega** shunday qilinganini izohlash (8.4). O'lchovsiz "tezlik uchun" chirkin kod yozish esa vaqtidan oldin optimizatsiya (patternlar hujjati 25.10).

### 38.8 Refaktoring commitlarini o'qiladigan ushlash

Refaktoring tarixi keyinchalik o'qiladi: "bu sinf nega shunday bo'lgan?" savoliga javob beradi. Shu sababli commit xabari harakat nomini ishlatishi kerak (40.2).

```
refactor: Payment dan TelephoneNumber value object ini ajratish

Extract Class: officeAreaCode va officeNumber maydonlari birga sayohat
qilayotgan edi va formatlash mantiqi uch joyda takrorlangan.

Xatti-harakat o'zgarmadi; mavjud testlar o'zgartirilmagan.
```

Oxirgi qator reviewer uchun eng muhim signal: testlar o'zgarmagan bo'lsa, xatti-harakat ham o'zgarmagan.

### 38.9 Amalda qo'llash

- [ ] Refaktoring paytida har bir harakatdan keyin tez testlarni ishga tushirish odatini joriy qiling.
- [ ] Refaktoring va xatti-harakat o'zgarishini alohida commitlarga ajratish qoidasini jamoa kelishuviga kiriting.
- [ ] 38.3 jadvalidagi olti xavfni nomni o'zgartirishdan keyin har safar grep bilan tekshiring.
- [ ] Testsiz kodni refaktoring qilishdan oldin xatti-harakatni qayd etuvchi test yozishni majburiy qiling.
- [ ] Katta refaktoringlarni branch by abstraction bo'yicha to'rt qadamga bo'lib rejalashtiring.
- [ ] Har bir refaktoring PR i uchun oldindan vaqt budjeti va to'xtatish shartini belgilang.
- [ ] Refaktoring commit xabarlarida harakat nomini va "xatti-harakat o'zgarmadi" qatorini yozishni standart qiling.
- [ ] Refaktoringdan keyin ishlash o'lchovini (p99, so'rov soni) taqqoslab, sezilarli o'zgarishni tekshiring.
# XI. Kod bazasi va jarayon gigiyenasi

## 39. Bir qadamli build va mahalliy qaytish halqasi (One-Step Build)

Toza kod faqat fayllar ichida emas: kod bazasining atrofidagi mexanika ham o'qilishi va ishonchli bo'lishi kerak. Bu bobda build, bog'liqliklar va mahalliy qaytish halqasining gigiyenasi. CI/CD test pipeline i testlash qo'llanmasida (15-bob), Sonar ulanishi SonarQube hujjatida (10, 21-boblar).

### 39.1 Build bitta buyruq bo'lsin

Evristika E1 (34.2) aniq talab qo'yadi: `git clone` dan keyin bitta buyruq butun loyihani qurishi kerak. Har bir qo'shimcha qadam — qo'lda o'rnatiladigan vosita, tahrirlanishi kerak bo'lgan fayl, maxfiy bilim — yangi odamning birinchi kunini yo'qotadi va avtomatlashtirishni to'sadi.

```bash
# Maqsad: shu uchta buyruq yetarli bo'lsin
git clone git@github.com:shop/payment.git
cd payment
./mvnw verify          # yoki ./gradlew build
```

Buni ta'minlash uchun: wrapper (`mvnw`, `gradlew`) repoda, JDK versiyasi `.sdkmanrc` yoki `.tool-versions` da, Docker kerak bo'lsa `compose.yml` repoda, va hech qanday qo'lda sozlash yo'q.

### 39.2 Test bitta buyruq bo'lsin

Evristika E2: testni ishga tushirish ham bir buyruq bo'lishi kerak va u hech qanday tashqi sozlama talab qilmasligi lozim. Testcontainers shu talabni bajaradi: baza va Kafka test paytida avtomatik ko'tariladi (testlash qo'llanmasi 8-bob).

```bash
./mvnw test              # unit testlar, soniyalar
./mvnw verify            # integratsion testlar ham, Testcontainers bilan
```

Agar testni ishga tushirish uchun mahalliy PostgreSQL o'rnatish yoki `application-local.yml` ni tahrirlash kerak bo'lsa, E2 buzilgan.

### 39.3 Takrorlanadigan build: versiya qotirish va wrapper

Build takrorlanadigan bo'lishi kerak: bir xil commit bir xil natija bersin. Buni buzadigan uch narsa bor va ularning hammasini yopish mumkin.

| Buzuvchi | Yechim |
|---|---|
| Vosita versiyasi mahalliy | Maven/Gradle wrapper repoda |
| JDK versiyasi mahalliy | `.sdkmanrc`, `maven.compiler.release` |
| Bog'liqlik versiyasi ochiq (`LATEST`, `+`) | aniq versiya yoki BOM |
| Snapshot bog'liqligi | reliz versiyasiga o'tish |
| Build vaqtidagi tashqi so'rov | kerakli fayllarni repoda saqlash |
| Plagin versiyasi ko'rsatilmagan | har bir plagin versiyasini yozish |

```xml
<!-- Versiyalar bir joyda, BOM bilan boshqariladi -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>${spring-boot.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

### 39.4 Bog'liqlik gigiyenasi: BOM, scope, keraksizni o'chirish

Bog'liqlik qo'shishning yashirin narxi arxitektor hujjatida (38.5). Bu yerda kod bazasi darajasidagi qoidalar: versiyalar bir joyda, `scope` to'g'ri, va ishlatilmaydigan bog'liqliklar o'chirilgan.

```bash
# Ishlatilmaydigan va e'lon qilinmagan bog'liqliklarni topish
./mvnw dependency:analyze

# Bog'liqlik daraxti: takrorlangan va konflikt versiyalar
./mvnw dependency:tree -Dverbose | grep -E 'omitted|conflict'

# Gradle da
./gradlew dependencies --configuration runtimeClasspath
```

| `scope` | Qachon |
|---|---|
| `compile` (standart) | kodda ishlatiladi |
| `runtime` | faqat ish vaqtida kerak (JDBC drayveri) |
| `provided` | konteyner beradi |
| `test` | faqat testda |
| `import` | BOM |

Eng ko'p uchraydigan xato: test kutubxonasini (`assertj`, `mockito`) `compile` scope da qoldirish — u production jar ga tushadi.

### 39.5 Build fayli o'qilishi

`pom.xml` va `build.gradle` ham kod va ular ham o'qilishi kerak. Qoidalar: xususiyatlar (`<properties>`) yuqorida va versiyalar shu yerda, bog'liqliklar guruhlangan va saralangan, plaginlar sozlamalari izohlangan.

```xml
<properties>
  <java.version>21</java.version>
  <!-- Versiyalar bir joyda: yangilash uchun bitta fayl tahrirlanadi -->
  <spring-boot.version>3.5.6</spring-boot.version>
  <testcontainers.version>1.21.3</testcontainers.version>
  <spotless.version>2.46.1</spotless.version>
</properties>
```

Spotless `sortPom` (13.3) `pom.xml` ni avtomatik tartiblaydi va diff shovqinini yo'qotadi.

### 39.6 Generatsiya qilingan kodni ajratish

Generatsiya qilingan kod `target/generated-sources` yoki `build/generated` ichida turadi, `src/` da emas, va `git` ga tushmaydi. Sababi: u har build da qayta yaratiladi, uni tahrirlash ma'nosiz, va u diff ni to'ldiradi.

```gitignore
target/
build/
*.class
# Generatsiya qilingan kod git ga tushmaydi
src/main/generated/
```

Agar generator vositasi `src/` ga yozsa, uning sozlamasini o'zgartirish kerak; imkonsiz bo'lsa, shu papkani formatlash, statik tahlil va coverage dan chiqarish lozim (13.8, SonarQube hujjati 41-bob).

### 39.7 Mahalliy tez qaytish halqasi

Qaytish halqasining uzunligi ishlab chiqish tezligini belgilaydi. Maqsad: kod yozilgandan keyin natijani 10 sekundda ko'rish.

| Halqa | Maqsad vaqt | Vositalar |
|---|---|---|
| Kompilyatsiya | < 5 s | incremental build, IDE |
| Unit testlar (bir modul) | < 10 s | tez testlar, mocksiz domen |
| Formatlash va lint | < 5 s | pre-commit hook (13.5) |
| Integratsion testlar | < 2 min | Testcontainers qayta ishlatish |
| Butun build | < 10 min | parallel modul, test teg |
| CI pipeline | < 15 min | keshlash, parallel job |

```properties
# ~/.testcontainers.properties - konteynerlarni qayta ishlatish (mahalliy ishda)
testcontainers.reuse.enable=true
```

```bash
# Faqat o'zgargan modul testlari
./mvnw -q -pl payment -am test

# Gradle: incremental va build kesh
./gradlew test --build-cache --parallel
```

### 39.8 `.gitignore`, sir va konfiguratsiya fayllari

Sir kod bazasiga tushsa, uni tarixdan olib tashlash qiyin va u allaqachon oqib ketgan hisoblanadi (40.8). Himoya ikki qatlamli: `.gitignore` va avtomatik skanerlash.

```gitignore
# Mahalliy sozlamalar va sirlar hech qachon commit qilinmaydi
.env
*.local.yml
application-local.yml
*.p12
*.jks
*.pem
secrets/
# IDE va OS
.idea/
*.iml
.vscode/
.DS_Store
```

Qoida: `application.yml` da sir bo'lmaydi — faqat `${ENV_VAR}` havolasi (26.4). Sirlar muhit o'zgaruvchisi, Kubernetes Secret yoki secret manager dan keladi.

```yaml
# CI da sir skanerlash: tarixga tushishini to'sadi
- name: Sir skanerlash
  run: |
    docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest \
      detect --source=/repo --no-git -v
```

### 39.9 Amalda qo'llash

- [ ] Yangi (yoki tozalangan) mashinada `git clone` + bitta buyruq bilan build ishlashini tekshirib, yetishmaganini README ga emas, build ga ko'chiring.
- [ ] Testni ishga tushirish uchun qo'lda sozlash kerak bo'lsa, uni Testcontainers yoki standart konfiguratsiya bilan yo'qoting.
- [ ] `dependency:analyze` ni ishga tushirib, ishlatilmaydigan bog'liqliklarni o'chiring va e'lon qilinmaganlarini qo'shing.
- [ ] Test kutubxonalarining `scope` i `test` ekanini tekshirib, production jar mazmunini ko'rib chiqing.
- [ ] Barcha bog'liqlik va plagin versiyalarini `<properties>` yoki BOM ga ko'chiring; snapshot va ochiq versiyalarni yo'qoting.
- [ ] Generatsiya qilingan kodni `git` dan chiqarib, formatlash va tahlildan istisno qiling.
- [ ] Mahalliy qaytish halqasini 39.7 jadvaliga qarab o'lchab, eng sekin bo'g'inni tezlashtiring.
- [ ] `.gitignore` ni sir fayllari bilan to'ldirib, CI ga sir skanerlashni qo'shing.
## 40. Versiya nazorati gigiyenasi (Version Control Hygiene)

Git tarixi kod bazasining hujjati: u "nega shunday qilingan" savoliga javob beradi va incident vaqtida eng tez diagnostika vositasi bo'ladi. Iflos tarix esa foydasiz. Review hajmi va navbat vaqti arxitektor hujjatida (36.5); bu bobda commit va branch darajasidagi qoidalar.

### 40.1 Atomik commit: bitta mantiqiy o'zgarish

Bitta commit bitta mantiqiy o'zgarishni o'z ichiga olishi kerak: u mustaqil ravishda tushunarli, mustaqil ravishda qaytariladigan va mustaqil ravishda ishlaydigan bo'lsin. Shu uch shart `git bisect` va `git revert` ni ishlatadigan qiladi.

| Commit mazmuni | To'g'rimi |
|---|---|
| Bitta xususiyat qismi + uning testi | ha |
| Refaktoring (xatti-harakat o'zgarmagan) | ha |
| Formatlash | ha, alohida (13.6) |
| Nomni o'zgartirish | ha, alohida (3.15) |
| Xususiyat + formatlash + refaktoring | yo'q |
| Ishlamaydigan yarim ish | yo'q |
| "Turli tuzatishlar" | yo'q |
| Bog'liqlik yangilash + kod moslashi | ha (ajralmas) |

```bash
# Ishni commitlarga ajratish: faqat kerakli qismlarni staging ga
git add -p                    # bo'laklab qo'shish
git commit -m "refactor: ..."
git add -p
git commit -m "feat: ..."
```

### 40.2 Commit xabari tuzilishi

Commit xabari ikki qismdan iborat: sarlavha (nima qilindi) va tana (nega qilindi). Tana eng qimmatli qism, chunki "nima" ni diff ham ko'rsatadi, "nega" ni esa faqat muallif biladi.

```
feat: hisob-kitob faylida valyuta tekshiruvini qo'shish

Bank fayli ba'zan USD yozuvlarini UZS hisobiga qo'shib yuboradi
(incident INC-2291). Valyuta mos kelmasa, qator rad etiladi va
audit log'ga yoziladi; butun fayl to'xtamaydi, chunki qolgan
yozuvlar to'g'ri.

Muqobil variant - butun faylni rad etish - rad etildi: bir noto'g'ri
qator kunlik hisob-kitobni to'xtatib qo'yadi.

Refs: SHOP-4821
```

Sarlavha qoidalari: 50-72 belgigacha, buyruq shaklida ("qo'shish", "tuzatish" — "qo'shdim" emas), nuqta bilan tugamaydi, va prefiks bilan boshlanadi (40.3).

### 40.3 Conventional commits va avtomatik changelog

Commit sarlavhasiga standart prefiks qo'yish tarixni mashina o'qiydigan qiladi: changelog avtomatik generatsiya qilinadi va semantik versiya avtomatik hisoblanadi.

| Prefiks | Ma'nosi | Versiyaga ta'siri |
|---|---|---|
| `feat:` | yangi xususiyat | minor |
| `fix:` | xato tuzatish | patch |
| `refactor:` | tuzilish o'zgarishi | yo'q |
| `perf:` | ishlash yaxshilanishi | patch |
| `test:` | faqat testlar | yo'q |
| `docs:` | faqat hujjat | yo'q |
| `build:` | build va bog'liqliklar | yo'q |
| `ci:` | pipeline | yo'q |
| `chore:` | qolgan ish | yo'q |
| `feat!:` yoki `BREAKING CHANGE:` | moslikni buzadi | major |

### 40.4 Branch hayoti va uzoq yashagan branch narxi

Branch qancha uzoq yashasa, uni merge qilish shunchalik qimmat bo'ladi: konfliktlar yig'iladi, review hajmi oshadi, va asosiy branch dan uzoqlashish regressiya xavfini oshiradi.

Amaliy maqsad: branch bir-ikki kundan oshmasin. Buning uchun ish kichik bo'lishi kerak va bu 38.5 dagi branch by abstraction va feature flag (41.5) bilan ta'minlanadi.

| Branch yoshi | Oqibati |
|---|---|
| < 1 kun | konflikt deyarli yo'q |
| 1-3 kun | boshqarilishi mumkin |
| 1 hafta | konfliktlar, katta review |
| 2+ hafta | merge alohida loyihaga aylanadi |

### 40.5 Rebase, merge va tarixni o'qiladigan ushlash

Rebase va merge o'rtasidagi tanlov jamoa kelishuviga bog'liq, lekin bitta qoida universal: **boshqa odam ishlatayotgan branch ning tarixini qayta yozmaslik**.

| Vaziyat | To'g'ri harakat |
|---|---|
| O'z lokal branch ingizni yangilash | `git rebase origin/main` |
| Boshqa odam ham ishlagan branch | `git merge origin/main` |
| O'z branch idagi WIP commitlarni tozalash | `git rebase -i` (push dan oldin) |
| Merge qilingan branch ni tozalash | o'chirish |
| Umumiy branch ga noto'g'ri commit tushdi | `git revert` (reset emas) |

Squash merge tarixni sodda qiladi (bitta xususiyat — bitta commit), lekin oraliq qadamlarni yo'qotadi. Katta refaktoring uchun oraliq commitlarni saqlash afzal.

### 40.6 PR hajmi va bo'lish texnikasi

Review sifati PR hajmi bilan teskari proporsional: 400 qatordan katta PR da topilgan xato soni keskin tushadi. Arxitektor hujjati 36.5 review navbati va hajmini ko'rib chiqadi; bu yerda bo'lish texnikalari.

| Texnika | Qanday |
|---|---|
| Refaktoringni ajratish | oldin tuzilish PR i, keyin xususiyat PR i (38.4) |
| Qatlam bo'yicha | migratsiya → repository → service → API |
| Feature flag ortida | yarim ish merge qilinadi, yoqilmaydi (41.5) |
| Abstraksiya orqali | branch by abstraction (38.5) |
| Faqat o'qish qismi | yangi endpoint avval o'qish uchun |
| Test birinchi | test PR i, keyin implementatsiya |

### 40.7 `git blame` ni foydali ushlash

`git blame` "bu qator nega shunday?" savoliga javob beradi, lekin faqat tarix toza bo'lsa. Uni buzadigan ikki narsa: katta formatlash commitlari (13.7 dagi `.git-blame-ignore-revs` bilan hal qilinadi) va aralash commitlar (40.1).

```bash
# Qator tarixini funksiya bo'yicha kuzatish (ko'chirishni ham ko'radi)
git log -L :priceFor:src/main/java/uz/shop/payment/Pricing.java

# Kod bo'lagi qachon kiritilganini topish
git log -S "REFUND_EXCEEDS_PAYMENT" --oneline

# Formatlash commitlarini e'tiborsiz qoldirib blame
git blame --ignore-revs-file .git-blame-ignore-revs Pricing.java
```

### 40.8 Tarixdan sirni o'chirish va uning chegarasi

Sir repoga tushsa, uni tarixdan o'chirish **yetarli emas**: u allaqachon klonlarda, CI log larida va GitHub keshida bo'lishi mumkin. Shu sababli tartib aniq va o'zgarmas.

1. **Birinchi** sirni rotatsiya qilish (eski kalitni bekor qilish). Bu eng muhim qadam.
2. Keyin tarixdan o'chirish (`git filter-repo` yoki BFG), agar repo yopiq va jamoa kichik bo'lsa.
3. Barcha klonlarni qaytadan olishni talab qilish.
4. Sir skanerlashni CI ga qo'shish (39.8), takrorlanmasligi uchun.

Tarixni qayta yozish umumiy branch da jamoaga qimmat tushadi, shuning uchun qadam 2 ni faqat qadam 1 bajarilgandan keyin ko'rib chiqish kerak.

### 40.9 Amalda qo'llash

- [ ] `git add -p` bilan ishni atomik commitlarga ajratish odatini joriy qiling.
- [ ] Commit xabari shablonini (`.gitmessage`) repoga qo'shib, `commit.template` sozlamasini README ga yozing.
- [ ] Conventional commits prefikslarini kelishib, CI da sarlavha formatini tekshiring.
- [ ] Branch yoshini o'lchab (ochiq PR lar bo'yicha), bir haftadan katta branchlarni bo'lish rejasini tuzing.
- [ ] Rebase va merge siyosatini yozib qo'ying, umumiy branch tarixini qayta yozishni taqiqlang.
- [ ] 400 qatordan katta PR lar uchun ogohlantirish qo'yib, 40.6 dagi bo'lish texnikalarini qo'llang.
- [ ] `.git-blame-ignore-revs` ni sozlab, blame ni toza ushlang (13.7).
- [ ] Sir tarixga tushgan holat uchun 40.8 dagi to'rt qadamli reja (runbook) yozib qo'ying.
## 41. O'zgarishni kiritish jarayoni: kichik qadamlar (Working in Small Steps)

Toza kod yozish usuli ham ahamiyatga ega: bir xil natijaga olib boradigan ikki yo'ldan biri xato ehtimolini bir necha barobar kamaytiradi. Bu bobda o'zgarish kiritishning amaliy tartibi: tushunishdan boshlash, kichik qadamlar, o'zini review qilish, va tugatish ta'rifi.

### 41.1 Ish boshlashdan oldin: muammoni yozib olish

Kodga tegishdan oldin bir-ikki gapda muammoni yozib olish eng arzon xato to'suvchi: u talabning noaniq joylarini darhol ko'rsatadi. Agar muammoni yozib bo'lmasa, u hali tushunilmagan.

```markdown
## Muammo
Bank fayli USD yozuvlarini UZS hisobiga qo'shib yuboradi (INC-2291).

## Kutilgan xatti-harakat
Valyuta mos kelmasa, qator rad etiladi, audit log'ga yoziladi, qolgan fayl davom etadi.

## Tegadigan joylar
SettlementImporter (parsing), SettlementRow (validatsiya), audit log.

## Qanday tekshiramiz
Aralash valyutali fayl bilan integratsion test; rad etilgan qatorlar soni metrikada.
```

### 41.2 Oldin tushunish, keyin o'zgartirish

Evristika G21: algoritmni **tushunish** kerak, uning ishlashini kuzatish yetarli emas. Amalda bu shunday ko'rinadi: o'zgartirish kiritishdan oldin mavjud kodning nima qilayotganini aytib bera olish kerak.

Tushunishni tekshirish usuli: mavjud xatti-harakat uchun test yozish (xatti-harakatni qayd etuvchi test, arxitektor hujjati 34.3). Test o'tsa — tushunish to'g'ri; yiqilsa — taxmin xato edi va bu o'zgartirishdan **oldin** bilish qimmatli.

### 41.3 Kodni o'qish texnikalari

Katta kod bazasini o'qish alohida ko'nikma va unda ishlaydigan texnikalar bor.

| Texnika | Qanday | Qachon |
|---|---|---|
| Kirish nuqtasidan | controller yoki konsumerdan boshlash | yangi xususiyat |
| Teskari yo'nalishda | xatodan stack trace bo'yicha yuqoriga | xato tuzatish |
| Ma'lumot oqimi bo'ylab | bir maydonni kiritishdan saqlanishiga qadar kuzatish | ma'lumot xatosi |
| Test orqali | mavjud testlarni o'qib shartnomani tushunish | yangi modul |
| Tarix orqali | `git log -S` bilan kod qachon va nega kiritilganini topish | sirli kod |
| Debugger bilan | nuqta qo'yib holatni ko'rish | murakkab oqim |
| Chizma orqali | chaqiruv grafini qo'lda chizish | chalkash bog'liqlik |

Oxirgi texnika eng kam ishlatiladi va eng samarali: 15 daqiqa qog'ozda chizish bir soatlik debug ni almashtiradi.

### 41.4 Birinchi ishlaydigan versiya va keyin tozalash

4.10 da ko'rilgan tartib ish darajasida ham ishlaydi: oldin ishlaydigan, keyin toza. Buning sababi psixologik — toza kod yozishga urinish bir vaqtda ikki muammoni (nima qilish va qanday qilish) hal qilishni talab qiladi va ikkisi ham sekinlashadi.

Muhim shart: tozalash **o'sha ish ichida** bajariladi, keyinga qoldirilmaydi (1.3). Amaliy usul: ishlaydigan versiyani lokal commit qilib, keyin tozalash commitlari qo'shish va push dan oldin `rebase -i` bilan tartiblash (40.5).

### 41.5 Yarim ishni boshqarish va feature flag

Katta xususiyatni kichik PR larga bo'lishning asosiy vositasi — feature flag: kod merge qilinadi, lekin yoqilmaydi. Konfiguratsiya murakkabligi va har bir flag ning narxi arxitektor hujjatida (6.4); bu yerda kod gigiyenasi.

```java
// yaxshi: flag bitta joyda o'qiladi, mantiq tarqalmaydi
@Service
class SettlementImporter {

    private final boolean currencyCheckEnabled;

    SettlementImporter(SettlementProperties properties) {
        this.currencyCheckEnabled = properties.currencyCheckEnabled();
    }

    private boolean isValid(SettlementRow row) {
        if (currencyCheckEnabled && !row.hasSupportedCurrency()) return false;
        return row.amount().isPositive();
    }
}
```

Flag intizomi uch qoidadan iborat: flag ning **o'chirish sanasi** bo'lishi (TODO bilan, 8.7), flag soni cheklangan bo'lishi, va flag olib tashlanganda eski yo'l ham o'chirilishi.

### 41.6 O'zini review qilish ro'yxati

PR ni boshqaga berishdan oldin uni o'zi review qilish eng arzon sifat nazorati: reviewer vaqtini tejaydi va xatolarning katta qismini topadi.

| Tekshiruv | Savol |
|---|---|
| Diff ni to'liq o'qish | har bir qator kerakmi? |
| Qoldirilgan tafsilot | debug log, izohga olingan kod, `TODO` qoldimi? |
| Nomlar | har bir yangi nom 2-bob qoidalariga mos keladimi? |
| Testlar | yangi xatti-harakatning har bir shoxi qamralganmi? |
| Chegaraviy holatlar | bo'sh, `null`, maksimal, manfiy sinalganmi? |
| Xato yo'li | istisno konteksti bormi, log bir joydami? |
| Qaytarish | bu o'zgarishni qaytarish osonmi? |
| Hujjat | public API o'zgargan bo'lsa Javadoc yangilandimi? |
| Migratsiya | sxema o'zgarishi orqaga mos keladimi? |
| Hajm | PR ni bo'lish kerakmi? (40.6) |

```bash
# O'zini review qilish uchun: PR diff ini xuddi reviewer ko'rganidek ko'rish
git diff origin/main...HEAD

# Qoldirilgan tafsilotlarni qidirish
git diff origin/main...HEAD | grep -nE '^\+.*(System\.out|printStackTrace|TODO|FIXME|\.only\()'
```

### 41.7 Pair va mob programming mexanikasi

Juftlikda ishlash review ning real vaqtdagi shakli va u ba'zi vazifalarda ancha samarali: murakkab domen mantiqi, yangi odamni o'qitish, incident tahlili.

| Shakl | Qanday | Qachon |
|---|---|---|
| Driver/navigator | biri yozadi, biri o'ylaydi; 15-25 daqiqada almashadi | murakkab mantiq |
| Ping-pong (TDD) | biri test yozadi, ikkinchisi o'tkazadi | TDD o'rganish |
| Strong-style | g'oya navigatordan, klaviatura driverda | bilim uzatish |
| Mob | butun jamoa bitta ekranda | arxitektura qarori, yangi modul |
| Solo + review | odatiy ish | kundalik vazifalar |

Juftlikda ishlash hamma vazifa uchun emas: oddiy, aniq ishlarda u resursni ikki barobar sarflaydi va foyda bermaydi.

### 41.8 Ishni tugatish ta'rifi (definition of done)

"Tayyor" so'zining ma'nosi kelishilmasa, ish hech qachon tugamaydi: kod yozildi, lekin test yo'q; test bor, lekin hujjat yo'q; hammasi bor, lekin monitoring yo'q. Yozilgan ta'rif shu noaniqlikni yopadi.

```markdown
## Ish tugadi deb hisoblanadi, agar:
- [ ] Kod yozilgan va o'zi review qilingan (41.6)
- [ ] Unit va kerakli integratsion testlar yozilgan, CI yashil
- [ ] Formatlash va statik tahlil o'tgan (13, 42)
- [ ] Public API o'zgarsa Javadoc yangilangan (10)
- [ ] Migratsiya orqaga mos va to'xtashsiz (28.9)
- [ ] Yangi xatti-harakat uchun metrika yoki log bor (29)
- [ ] Xato yo'li sinalgan va kontekst bilan log qilinadi (19)
- [ ] Feature flag bo'lsa, o'chirish sanasi yozilgan (41.5)
- [ ] PR tavsifida "nega" yozilgan (40.2)
- [ ] Review izohlari yopilgan yoki javob berilgan
```

### 41.9 Amalda qo'llash

- [ ] Har bir vazifani boshlashdan oldin 41.1 shablonini to'ldirish odatini joriy qiling.
- [ ] Mavjud kodga tegishdan oldin xatti-harakatni qayd etuvchi test yozishni standart qiling.
- [ ] 41.3 jadvalidagi texnikalardan kamida uchtasini keyingi ish davomida ongli ravishda sinab ko'ring.
- [ ] Feature flag lar ro'yxatini yuritib, har biriga o'chirish sanasi va egasini belgilang.
- [ ] 41.6 ro'yxatini PR shabloniga kiritib, o'zini review qilishni majburiy qadam qiling.
- [ ] `git diff` bo'yicha qoldirilgan tafsilot (debug log, `TODO`) skriptini pre-push hook ga qo'shing.
- [ ] Juftlikda ishlash uchun mos vazifa turlarini jamoa bilan kelishib oling.
- [ ] Ishni tugatish ta'rifini yozib, jamoa kelishuviga va PR shabloniga kiriting.
## 42. Statik tahlil va avtomatik qoidalar (Static Analysis and Automated Rules)

Toza kod qoidasi odam xotirasida yashasa, u buziladi. Shu sababli har bir qoidaning oxirgi manzili — mashina. SonarQube ning mexanikasi, quality gate va xato katalogi alohida hujjatda; bu bobda qolgan vositalar va qoidani joriy qilish tartibi.

### 42.1 Kompilyator birinchi tekshiruvchi

Kompilyator eng tez va eng arzon statik tahlilchi, lekin uning ogohlantirishlari odatda o'chirilgan holda qoldiriladi. `-Xlint:all -Werror` bir martalik sozlama va u darhol o'nlab muammoni topadi (25.10).

| Vosita | Nima topadi | Narxi |
|---|---|---|
| Kompilyator `-Xlint` | xom tur, deprecation, unchecked | bepul |
| Error Prone | xatolik namunalari (300+ qoida) | kompilyatsiyaga +20% |
| NullAway | `null` xavfi | kam |
| Checkstyle | uslub va nomlash | kam |
| SpotBugs | bytecode darajasidagi xatolar | o'rtacha |
| PMD | murakkablik, o'lik kod | o'rtacha |
| ArchUnit | arxitektura qoidalari | test sifatida |
| SonarQube | hammasi + tarix va gate | server |

### 42.2 Error Prone va NullAway

Error Prone kompilyatsiya paytida ishlaydi va **xatolik namunalarini** topadi — uslub emas, haqiqiy xatolar. Bu hujjatdagi ko'p qoidalar uning qoidalariga bevosita mos keladi.

| Bu hujjatdagi qoida | Error Prone qoidasi |
|---|---|
| `equals` bor, `hashCode` yo'q (15.2) | `EqualsHashCode` |
| `finally` da `return` (19.3) | `Finally` |
| Nostatik ichki sinf (25.7) | `ClassCanBeStatic` |
| `split` regex tuzog'i (21.5) | `StringSplitter` |
| Kodirovka berilmagan (21.3) | `DefaultCharset` |
| `java.util.Date` (22.1) | `JavaUtilDate` |
| `BigDecimal.equals` (20.2) | `BigDecimalEquals` |
| Natija e'tiborsiz qoldirilgan | `ReturnValueIgnored` |
| `Optional.get` tekshiruvsiz (24.6) | `OptionalGetWithoutIsPresent` |
| Immutable obyektga yozish (16.1) | `Immutable` |
| Ishlatilmaydigan o'zgaruvchi (33.10) | `UnusedVariable` |

NullAway esa `null` xavfini kompilyatsiya vaqtida topadi va u JSpecify annotatsiyalari bilan ishlaydi (arxitektor hujjati 13.10): paketga `@NullMarked` qo'yilsa, barcha turlar standart holatda `null` bo'lmaydi va istisnolar `@Nullable` bilan belgilanadi.

```java
// package-info.java (10.7)
@NullMarked
package uz.shop.payment;

// Endi null qaytarish kompilyatsiya xatosi
Payment find(PaymentId id) { return null; }        // NullAway: ERROR

// Oshkor nullable
@Nullable Payment findOrNull(PaymentId id) { return null; }   // ruxsat
```

### 42.3 SpotBugs, PMD va Checkstyle rollari

Uch vositaning rollari qo'shilmasligi kerak, aks holda bir xil muammo uch marta xabar qilinadi va jamoa hisobotlarni o'qishni to'xtatadi.

| Vosita | Roli | Qoidalar soni |
|---|---|---|
| Checkstyle | uslub, nomlash, tuzilish chegaralari | 20-30 (tanlangan) |
| SpotBugs | bytecode darajasidagi xatolar, thread xavfi | standart to'plam |
| PMD | murakkablik, o'lik kod, takrorlanish | tanlangan |
| Error Prone | xatolik namunalari | standart + tanlangan |

Amaliy tavsiya: Checkstyle (uslub) + Error Prone (xatolar) + Sonar (umumiy) kombinatsiyasi ko'p loyihada yetarli; SpotBugs va PMD ni faqat aniq ehtiyoj bo'lganda qo'shish.

### 42.4 ArchUnit bilan qoidani kodga aylantirish

ArchUnit arxitektura va kod qoidalarini **test** sifatida yozadi va bu eng moslashuvchan usul: qoida kod bazasiga xos bo'lsa, uni hech qanday linter bilmaydi. Arxitektor hujjati 36.9 da qatlam qoidalari misoli berilgan; bu yerda shu hujjatdagi qoidalarni majburlash.

```java
@AnalyzeClasses(packages = "uz.shop", importOptions = ImportOption.DoNotIncludeTests.class)
class CleanCodeRulesTest {

    // 22.1: eski sana API si taqiqlangan
    @ArchTest
    static final ArchRule eski_sana_api_taqiqlangan =
            noClasses().should().dependOnClassesThat()
                    .haveFullyQualifiedName("java.util.Date")
                    .orShould().dependOnClassesThat()
                    .haveFullyQualifiedName("java.text.SimpleDateFormat");

    // 20.1: pul maydonlarida double bo'lmasin
    @ArchTest
    static final ArchRule pul_double_bilan_saqlanmaydi =
            noFields().that().haveNameMatching(".*(amount|price|total|fee|balance).*")
                    .should().haveRawType(double.class)
                    .orShould().haveRawType(Double.class);

    // 25.1: Optional maydon bo'lmasin
    @ArchTest
    static final ArchRule optional_maydon_bolmaydi =
            noFields().should().haveRawType(Optional.class);

    // 26.10: Lombok @Data taqiqlangan
    @ArchTest
    static final ArchRule lombok_data_taqiqlangan =
            noClasses().should().beAnnotatedWith("lombok.Data");

    // 2.4 va arxitektor 4.2: ma'nosiz sinf qo'shimchalari
    @ArchTest
    static final ArchRule manosiz_sinf_nomlari =
            noClasses().should().haveSimpleNameEndingWith("Manager")
                    .orShould().haveSimpleNameEndingWith("Helper")
                    .orShould().haveSimpleNameEndingWith("Info");

    // 26.1: field injection taqiqlangan
    @ArchTest
    static final ArchRule maydon_inyeksiyasi_taqiqlangan =
            noFields().should().beAnnotatedWith("org.springframework.beans.factory.annotation.Autowired");

    // 22.3: Instant.now() biznes kodida chaqirilmaydi, Clock ishlatiladi
    @ArchTest
    static final ArchRule vaqt_clock_orqali_olinadi =
            noClasses().that().resideInAPackage("..domain..")
                    .should().callMethod(Instant.class, "now");
}
```

### 42.5 Maxsus lint qoidasi yozish

Review da bir xil izoh har haftada qaytsa, u qoidaga aylanishi kerak (arxitektor hujjati 36.9). ArchUnit ko'p holatni qoplaydi, lekin ba'zi qoidalar AST darajasini talab qiladi — bunda Error Prone ning maxsus tekshiruvi yoziladi.

```java
// Error Prone maxsus qoidasi: log'da satr birlashtirish taqiqlangan (29.1)
@BugPattern(
        summary = "SLF4J xabarida satr birlashtirish: {} placeholder ishlatilsin",
        severity = ERROR,
        link = "docs/clean-code.md#291")
public class NoStringConcatInLog extends BugChecker implements MethodInvocationTreeMatcher {

    private static final Matcher<ExpressionTree> LOG_CALL =
            instanceMethod().onDescendantOf("org.slf4j.Logger")
                    .namedAnyOf("trace", "debug", "info", "warn", "error");

    @Override
    public Description matchMethodInvocation(MethodInvocationTree tree, VisitorState state) {
        if (!LOG_CALL.matches(tree, state)) return NO_MATCH;
        ExpressionTree first = tree.getArguments().isEmpty() ? null : tree.getArguments().get(0);
        if (first instanceof BinaryTree binary && binary.getKind() == Kind.PLUS) {
            return describeMatch(tree);
        }
        return NO_MATCH;
    }
}
```

### 42.6 Qoidani joriy qilish tartibi: ogohlantirish, keyin xato

Yangi qoidani darhol xato darajasida yoqish mavjud kod bazasida yuzlab xato beradi va jamoa uni o'chiradi. Ishlaydigan tartib bosqichli.

| Bosqich | Harakat |
|---|---|
| 1 | Qoidani ogohlantirish darajasida yoqib, sonini o'lchash |
| 2 | Yangi kod uchun xato, mavjud kod uchun ogohlantirish ("clean as you code") |
| 3 | Mavjud buzilishlarni bosqichma-bosqich tuzatish, sonini kuzatish |
| 4 | Son nolga yetganda qoidani xato darajasiga ko'tarish |
| 5 | Qoida sababini hujjatda yozib qo'yish (48-bob) |

Ikkinchi bosqich eng muhim: Sonar ning "new code" tushunchasi (SonarQube hujjati 7-bob) shu yondashuvni to'g'ridan-to'g'ri qo'llab-quvvatlaydi.

### 42.7 False positive va bostirishni hujjatlashtirish

Har bir statik tahlil vositasi noto'g'ri xabar beradi va bostirish (`@SuppressWarnings`) kerak bo'ladi. Qoida: bostirish har doim **izoh bilan** va eng kichik qamrovda bo'ladi (23.7).

```java
// yaxshi: qamrov torroq, sabab yozilgan, qoida nomi aniq
@SuppressWarnings("unchecked")   // JPA native query Object[] qaytaradi, mapping qo'lda tekshirilgan
private List<SettlementRow> mapRows(Query query) { ... }

// yomon: butun sinf uchun, sababsiz
@SuppressWarnings("all")
class SettlementImporter { ... }
```

Bostirishlar sonini CI da o'lchash kerak: u o'sib borsa, qoida noto'g'ri sozlangan yoki jamoa unga ishonmaydi.

```bash
# Bostirishlar ro'yxati va soni: o'sishini kuzatish
grep -rn "@SuppressWarnings" src/main/java | wc -l
grep -rn "@SuppressWarnings" src/main/java | grep -v "//" | head    # izohsizlarni topish
```

### 42.8 Amalda qo'llash

- [ ] `-Xlint:all -Werror` ni yoqib, chiqqan ogohlantirishlarni ro'yxatlab bosqichma-bosqich tuzating.
- [ ] Error Prone ni build ga qo'shib, 42.2 jadvalidagi qoidalarni `ERROR` darajasiga ko'taring.
- [ ] NullAway ni yoqib, paketlarga `@NullMarked` qo'shishni bosqichma-bosqich boshlang.
- [ ] Checkstyle, SpotBugs va PMD rollarini ajratib, takrorlangan qoidalarni o'chiring.
- [ ] 42.4 dagi ArchUnit qoidalarini loyihaga moslab qo'shing va CI da ishga tushiring.
- [ ] Review da takrorlanadigan uch izohni tanlab, ularni ArchUnit yoki maxsus qoidaga aylantiring.
- [ ] Yangi qoidalarni 42.6 dagi besh bosqichli tartib bo'yicha joriy qiling.
- [ ] `@SuppressWarnings` sonini o'lchab, izohsizlarini tuzatib, o'sishini CI da kuzatib turing.
# XII. Professional intizom

## 43. Professional mas'uliyat (Professionalism)

Toza kod texnik qoidalar to'plami emas, kasbiy munosabat natijasi. Bu va keyingi to'rt bob shu munosabatni ko'rib chiqadi: javobgarlik, majburiyat, baholash, vaqt va birgalikda ishlash. Texnik yetakchilik va jamoada qaror tarqatish arxitektor hujjatida (36-bob), o'rganish va texnologiya tanlash esa 38-bobda.

### 43.1 "Zarar qilmaslik": funksiyaga va tuzilishga

Professional ikki xil zarar qilmasligi kerak. **Funksiyaga zarar** — ishlaydigan narsani buzish: xato kiritish, regressiya, ma'lumot yo'qotish. **Tuzilishga zarar** — kod bazasini o'zgartirishga qarshilik qiladigan holga keltirish.

Birinchi zarar ko'rinadi va u haqida gapiradilar. Ikkinchi zarar ko'rinmaydi va shu sababli ko'proq uchraydi: har bir shoshilib yozilgan, testsiz, chalkash o'zgarish tuzilishga qarz qo'shadi. Oqibati keyin keladi — har bir yangi xususiyat sekinlashadi.

"Xato qilmayman" degan da'vo haqiqatga mos emas; to'g'ri da'vo boshqa: **xatolarim uchun javob beraman va ularni tez topadigan tizim quraman**. Shu tizimning qismlari: testlar, statik tahlil, monitoring, kichik qadamlar.

### 43.2 O'z xatosi uchun javob berish

Professionalizmning amaliy belgisi: xato chiqqanda uni tan olish, oqibatini bartaraf etish va takrorlanmasligi uchun tizim o'zgartirish. Uchinchi qism eng ko'p e'tibordan chetda qoladi.

| Xato turi | Noto'g'ri javob | To'g'ri javob |
|---|---|---|
| Production da xato | "test muhiti boshqa edi" | tuzatish + shu holatga test |
| Regressiya | "men bilmagan edim" | tuzatish + qamrovni oshirish |
| Noto'g'ri baho | "talab o'zgardi" | bahoni qayta ko'rish, sababni yozish |
| Noto'g'ri qaror | himoyalanish | qarorni qayta ko'rish (ADR yangilanishi) |
| Review da o'tkazib yuborilgan xato | "u yozgan" | jamoaviy javobgarlik, qoida qo'shish |

Incident tahlili va post-mortem mexanikasi arxitektor hujjatida (35-bob); bu yerda muhim nuqta: ayblov emas, tizim o'zgarishi.

### 43.3 Ishga layoqat: charchagan holda kod yozmaslik

Kod yozish aqliy diqqat talab qiladi va charchoq uning sifatini keskin pasaytiradi. Charchagan holda yozilgan kod odatda ikki marta qimmat tushadi: bir marta yozilganda, bir marta tuzatilganda.

Amaliy qoidalar: charchagan holda murakkab mantiq yozmaslik (o'rniga hujjat, review, oddiy vazifa); uzun kun oxirida muhim o'zgarishni merge qilmaslik; va juma kuni kech production ga chiqarmaslik (xato topilsa, hech kim yo'q).

### 43.4 Mijoz va ishlab chiquvchi maqsadlari to'qnashuvi

Mijoz tez va arzon natija xohlaydi; ishlab chiquvchi uzoq muddatli sifat uchun javob beradi. Bu to'qnashuv tabiiy va uni yashirish zarar keltiradi.

To'g'ri yondashuv: tanlovni **oshkor** qilish va qarorni narx bilan ifodalash. "Buni bir kunda qilish mumkin, lekin testsiz va keyin har bir o'zgarish ikki barobar sekin bo'ladi" — bu qaror mijoz bilan birga qabul qilinadi. Yashirin qaror esa (jim testsiz yozish) professionalizm emas.

Bir narsa muhokama qilinmaydi: **sifat me'yori**. Testsiz kod, tekshirilmagan xavfsizlik, ma'lumot yo'qotish xavfi — bular tanlov emas (44.1).

### 43.5 Kasbiy etika: sir, ma'lumot, xavfsizlik

Toza kodning etik o'lchovi bor va u uchta amaliy qoidaga qisqaradi.

**Ma'lumot**: foydalanuvchi ma'lumotiga faqat kerakli darajada tegish, log ga sezgir ma'lumot yozmaslik (29.8), production bazasidan ma'lumotni test muhitiga nusxalashdan oldin anonimlashtirish.

**Xavfsizlik**: topilgan zaiflikni yashirmaslik, hatto o'zingiz kiritgan bo'lsangiz ham; xavfsizlik tekshiruvini "vaqt yo'q" sababi bilan o'tkazib yubormaslik.

**Sir**: mijoz ma'lumoti, ichki arxitektura va kod — ular haqida tashqarida gapirmaslik; lekin texnik bilimni (pattern, yondashuv) ulashish normal.

### 43.6 Amalda qo'llash

- [ ] Oxirgi uch incidentni ko'rib chiqib, har biri uchun tizim o'zgarishi kiritilganini tekshiring.
- [ ] "Sifat me'yori muhokama qilinmaydi" ro'yxatini yozib, jamoa va menejer bilan kelishib oling.
- [ ] Charchagan holda merge va reliz qilmaslik qoidasini jamoa kelishuviga kiriting.
- [ ] Texnik qarz haqidagi suhbatni narx tilida olib borish uchun bitta misol tayyorlang (45.7).
- [ ] Production ma'lumotini test muhitiga ko'chirish tartibini (anonimlashtirish bilan) hujjatlashtiring.
- [ ] Log va `toString` larda sezgir ma'lumot yo'qligini bir marta to'liq audit qiling (29.8).
- [ ] Topilgan zaifliklarni xabar qilish kanalini (kimga, qanday) aniq belgilang.
- [ ] O'z xatolaringizni yozib boradigan shaxsiy jurnal yuritib, har chorakda naqshlarni ko'rib chiqing.
## 44. "Yo'q" va "ha" deyish: majburiyat tili (Saying No and Saying Yes)

Toza kodni buzadigan eng kuchli kuch — noto'g'ri majburiyat. "Juma kuniga bo'ladi" degan gap aytilgach, sifat birinchi qurbon bo'ladi. Bu bobda majburiyat tilining aniq qoidalari.

### 44.1 "Yo'q" ni qachon va qanday aytish

Professionalizmning eng aniq belgisi — bajarilmaydigan ishga "yo'q" deyish qobiliyati. "Yo'q" deyishdan qochish qisqa muddatda ziddiyatni yo'qotadi, uzoq muddatda ishonchni yo'qotadi.

"Yo'q" aytishning ishlaydigan shakli uchta elementdan iborat: aniq javob, sabab, va muqobil taklif.

```
Yomon: "Harakat qilaman" (majburiyat yo'q, umid bor)
Yomon: "Mumkin emas" (sabab yo'q, muqobil yo'q)

Yaxshi: "Juma kuniga to'liq xususiyat chiqmaydi: migratsiya va bank
integratsiyasi ikki hafta oladi. Juma kuniga qaytarish qismini
chiqara olaman, bank integratsiyasi keyingi sprintda. Yoki
integratsiyani sinxron qilsak juma kuniga yetadi, lekin keyin
uni qayta yozish kerak bo'ladi."
```

Muhim nuqta: "yo'q" **maqsadga** emas, aniq muddat yoki qamrovga aytiladi. Maqsad doim muhokama qilinadi; fizika muhokama qilinmaydi.

### 44.2 "Urinib ko'raman" nega yolg'on

"Urinib ko'raman" eng zararli javob, chunki tinglovchi uni "ha" deb eshitadi, aytuvchi esa "yo'q" deb o'ylaydi. Natijada reja shu "ha" ga asoslanadi va u bajarilmaydi.

"Urinib ko'raman" ning ortida uch yashirin ma'no bo'lishi mumkin va ularning har birini oshkor aytish kerak:

| Yashirin ma'no | Oshkor shakl |
|---|---|
| "Yetmaydi, lekin aytishdan qo'rqaman" | "Bu muddatda bo'lmaydi; shuni taklif qilaman..." |
| "Qo'shimcha kuch sarflashga tayyorman" | "Agar X ni olib tashlasak, yetadi" |
| "Bilmayman" | "Aniqlashim kerak; ertaga javob beraman" |
| "Boshqa ishni to'xtatsam bo'ladi" | "Y ni keyinga surib qo'ysak, bo'ladi" |

### 44.3 Majburiyat tili: aytaman, qilaman, qachongacha

Haqiqiy majburiyat uch qismdan iborat va uchtasi ham bo'lishi shart: **kim**, **nima** va **qachongacha**. Biri yo'q bo'lsa, bu majburiyat emas, niyat.

| Shakl | Majburiyatmi |
|---|---|
| "Buni qilishimiz kerak" | yo'q (kim?) |
| "Men ko'rib chiqaman" | yo'q (qachon?) |
| "Tez orada tayyor bo'ladi" | yo'q (qachon?) |
| "Agar vaqt bo'lsa qilaman" | yo'q (shart) |
| "Seshanba kuni soat 12 gacha PR ochaman" | ha |
| "Bugun kech soat 6 ga qadar javob beraman" | ha |

Majburiyat olingach, uni bajarish professionalizmning asosiy sinovidir. Bajarilmasligi aniq bo'lsa — **darhol** xabar qilish kerak (45.6), oxirgi kungacha kutmaslik.

### 44.4 Passiv tavakkalchilik va uning narxi

Passiv tavakkalchilik — "menga aytilgani shu" deb aniq xato bo'lgan yo'lni davom ettirish. Bu javobgarlikni boshqaga o'tkazishga urinish va u ishlamaydi: tizim buzilganda hamma javob beradi.

Professional xatti-harakat: xavfni **yozib** xabar qilish, muqobil taklif qilish, qaror boshqa tomondan kelsa uni qayd etish va davom etish. "Rozi emasman, lekin bajaraman" qoidasi arxitektor hujjatida (3.6) ko'rilgan.

```markdown
## Xavf haqida xabar (qisqa shakl)
**Qaror**: bank integratsiyasini sinxron qilish (muddat sababli).
**Xavf**: bank 5 sekund javob bersa, bizning p99 5 sekunddan oshadi va
checkout to'xtaydi. O'tgan chorakda bank 3 marta sekinlashgan.
**Taklif**: asinxron + holat so'rash (2 kun qo'shimcha).
**Qabul qilingan qaror**: sinqron, timeout 2s va circuit breaker bilan.
**Qayta ko'rish**: birinchi sekinlashishdan keyin yoki 2026-Q3.
```

### 44.5 Jamoa bo'lib "yo'q" deyish

Bitta odam "yo'q" deganda u to'siq bo'lib ko'rinadi; jamoa bir ovozdan "yo'q" deganda bu texnik haqiqat bo'lib eshitiladi. Shu sababli majburiyat haqidagi suhbatga jamoa bo'lib kirish ancha samarali.

Buning sharti: jamoa ichida kelishuv bo'lishi. Agar bir odam "bo'ladi" deb aytsa, qolganlarning "yo'q" i kuchini yo'qotadi. Shuning uchun baholash jamoa bo'lib qilinadi (45.3) va muddat haqida gapirishdan oldin ichki kelishuv bo'ladi.

### 44.6 Amalda qo'llash

- [ ] Keyingi hafta "urinib ko'raman" iborasini umuman ishlatmaslikni sinab ko'ring; har safar aniq shaklga aylantiring.
- [ ] Har bir majburiyatni kim/nima/qachongacha shaklida yozib boring va bajarilishini kuzating.
- [ ] 44.1 dagi uch elementli "yo'q" shaklini keyingi muddat suhbatida qo'llang.
- [ ] Rozi bo'lmagan qarorlar uchun 44.4 dagi xavf xabari shablonini ishlating.
- [ ] Muhokama qilinmaydigan sifat me'yorlari ro'yxatini jamoa bilan yozib, menejerga taqdim eting.
- [ ] Muddat haqidagi tashqi suhbatdan oldin jamoa ichida kelishuvga erishish qoidasini kiriting.
- [ ] Bajarilmaydigan majburiyat haqida darhol xabar qilish qoidasini kelishuvga yozing.
- [ ] Oxirgi uch kechikishni ko'rib chiqib, qaysi birida majburiyat aniq bo'lmaganini aniqlang.
## 45. Baholash, muddat va bosim (Estimation, Deadlines and Pressure)

Noto'g'ri baho toza kodni buzadigan ikkinchi kuch: vaqt yetmaganda test, refaktoring va hujjat birinchi qurbon bo'ladi. Bu bobda baholashning amaliy texnikalari va bosim ostida intizomni saqlash.

### 45.1 Baho va majburiyat farqi

Eng ko'p chalkashlik shu ikki tushunchani aralashtirishdan keladi. **Baho** — ehtimollik taqsimoti, u xato bo'lishi mumkin va bu normal. **Majburiyat** — bajarilishi kerak bo'lgan gap (44.3), u xato bo'lmasligi kerak.

Professional bahoni majburiyatga aylantirmasligi kerak. "Taxminan uch kun" degan baho "uch kunda qilaman" degan majburiyatga aylantirilsa, keyinchalik ayblov tug'iladi.

| Savol | To'g'ri javob turi |
|---|---|
| "Qancha vaqt oladi?" | baho (taqsimot bilan) |
| "Juma kuniga bo'ladimi?" | majburiyat (ha/yo'q) |
| "Eng tez qachon?" | optimistik baho, oshkor belgilangan |
| "Kafolat berasizmi?" | faqat majburiyat bera olgan narsaga |

### 45.2 Uch nuqtali baho va PERT

Bitta son bilan baholash ma'lumot yo'qotadi. Uch nuqtali baho noaniqlikni ham uzatadi: optimistik (O), ehtimoliy (M), pessimistik (P).

Kutilgan qiymat va standart chetlanish:

```
μ = (O + 4M + P) / 6
σ = (P - O) / 6
```

Misol: migratsiya ishi uchun O = 2 kun, M = 4 kun, P = 10 kun.
μ = (2 + 16 + 10) / 6 = 4.67 kun; σ = (10 - 2) / 6 = 1.33 kun.
Ya'ni "taxminan 5 kun, 68% ehtimol bilan 3.3-6 kun oralig'ida".

Bir necha vazifa uchun kutilgan qiymatlar qo'shiladi, chetlanishlar esa kvadratik qo'shiladi: `σ_total = √(σ₁² + σ₂² + ...)`. Natijada ko'p kichik vazifaning jami bahosi bitta katta vazifadan **aniqroq** bo'ladi — bu ishni bo'lishning matematik asosi.

### 45.3 Planning poker va kattalik birligi

Jamoa bo'lib baholashning amaliy usuli: har kim mustaqil baho beradi, keyin farqlar muhokama qilinadi. Farqning o'zi eng qimmatli ma'lumot — u kimdir boshqa narsani tushunganini ko'rsatadi.

Mutlaq vaqt o'rniga nisbiy kattalik (story point) ishlatish ikki foyda beradi: odamlar nisbatni vaqtdan yaxshiroq baholaydi, va baho odamga bog'liq bo'lmaydi.

| Kattalik | Ma'nosi |
|---|---|
| 1 | aniq, bir-ikki soat, shubha yo'q |
| 2 | aniq, yarim kun |
| 3 | tushunarli, bir kun |
| 5 | bir necha noaniq joy bor |
| 8 | bo'lish kerak |
| 13+ | bo'lish **majburiy**, hali tushunilmagan |

### 45.4 Katta ishni baholash va noaniqlik konusi

Loyiha boshida baho 4 barobar xato bo'lishi mumkin; talab aniqlashgach 2 barobar; dizayn tugagach 1.5 barobar. Bu "noaniqlik konusi" va u baholashning tabiatini ko'rsatadi: bahoni aniqlashtirishning yagona yo'li — ma'lumot to'plash.

Amaliy natija: katta ish uchun bitta son bermaslik, balki **diapazon** berish va qayta ko'rish nuqtalarini belgilash. Spike (arxitektor hujjati 3.5) noaniqlikni kamaytirishning eng arzon vositasi: ikki kunlik tajriba ikki haftalik bahoni aniqlashtiradi.

### 45.5 Bosim ostida intizomni saqlash

Bosim paytida odatiy reaksiya — intizomni tashlash: testni o'tkazib yuborish, review ni qisqartirish, kodni shoshilib yozish. Bu deyarli har doim **sekinlashtiradi**, chunki xato topilib tuzatilishi ko'proq vaqt oladi.

| Bosim ostida | To'g'ri harakat |
|---|---|
| "Test yozishga vaqt yo'q" | aynan shu paytda test eng kerak |
| "Review ni o'tkazib yuboraylik" | review eng arzon xato to'suvchi |
| "Keyin tozalaymiz" | tozalash ishning qismi (1.3) |
| "Hamma kech qolib ishlasin" | charchoq xato ko'paytiradi (43.3) |
| "Parallel qilib tezlashtiramiz" | yangi odam qo'shish dastlab sekinlashtiradi |
| "Qamrovni qisqartiramiz" | **to'g'ri yechim** (45.7) |

### 45.6 Kechikishni oshkor qilish va "90% tayyor" tuzog'i

Kechikish haqida iloji boricha ertaroq xabar berish professionalizmning asosiy belgisi: ertaroq bilingan kechikish boshqarilishi mumkin, oxirgi kunda bilingani esa yo'q.

"90% tayyor" degan hisobot eng ko'p uchraydigan yashirin kechikish shakli: qolgan 10% odatda ishning yarmini oladi (integratsiya, xato tuzatish, chegaraviy holatlar). Yechim: foiz emas, **tugallangan qismlar** bilan hisobot berish.

```
Yomon: "90% tayyor"
Yaxshi: "Qaytarish oqimi tugadi va testlari o'tyapti. Bank integratsiyasi
         yozilgan, lekin sandbox'da hali sinalmagan. Xato oqimi va
         idempotentlik qolgan: taxminan 2 kun."
```

### 45.7 Qamrovni qisqartirish yoki sifatni qisqartirish

Vaqt yetmaganda uch o'lcham bor: muddat, qamrov va sifat. Birinchisi odatda qotirilgan. Shunda tanlov ikkisi orasida qoladi va javob har doim bir xil: **qamrov qisqartiriladi, sifat qisqartirilmaydi**.

Sababi iqtisodiy: qamrovni qisqartirish bir martalik narx, sifatni qisqartirish esa doimiy foiz to'lovi. Testsiz chiqarilgan xususiyat har bir keyingi o'zgarishda qimmat tushadi.

| Qisqartirish mumkin | Qisqartirish mumkin emas |
|---|---|
| Xususiyat soni | testlar |
| Qo'llanish holatlari (edge case) | xavfsizlik tekshiruvi |
| UI silliqligi | ma'lumot butunligi |
| Avtomatlashtirish darajasi | migratsiyaning orqaga mosligi |
| Hisobot va panel | xato bilan ishlash |
| Konfiguratsiya moslashuvchanligi | monitoring |

### 45.8 Amalda qo'llash

- [ ] Keyingi uchta bahoni uch nuqtali shaklda (O/M/P) berib, PERT bilan kutilgan qiymat va chetlanishni hisoblang.
- [ ] 8 va undan katta baholangan vazifalarni majburiy bo'lish qoidasini kiriting.
- [ ] Baho va majburiyatni og'zaki suhbatda ham oshkor ajratishni odat qiling.
- [ ] Katta ish boshida ikki kunlik spike ajratib, bahoni keyin aniqlashtiring.
- [ ] "Foiz tayyor" hisobotini tugallangan qismlar ro'yxatiga almashtiring.
- [ ] Bosim paytida qisqartirilmaydigan narsalar ro'yxatini (45.7) jamoa kelishuviga kiriting.
- [ ] Oxirgi uch loyihadagi baho va haqiqiy vaqtni taqqoslab, o'z koeffitsientingizni hisoblang.
- [ ] Kechikish haqida xabar berish muddatini ("bilgan kuni") kelishuvga yozing.
## 46. Vaqt, diqqat va mashq (Time, Focus and Practice)

Kod sifati diqqat sifatiga bog'liq va diqqat cheklangan resurs. Bu bobda shu resursni boshqarish: uzilishlar, vaqt bloklari, ko'r yo'laklardan chiqish va ataylab mashq. Vaqtni taqsimlash yetakchi nuqtai nazaridan arxitektor hujjatida (36.12), o'rganish rejasi esa 38.12 da.

### 46.1 Diqqat resursi va uni sarflash

Kod yozish uchun kerakli diqqat kun bo'yi bir xil emas: u ertalab ko'p, kechga borib kamayadi, va har bir uzilishdan keyin tiklanishi uchun vaqt kerak. Shu resursni "diqqat-mana" deb tasavvur qilish foydali: u tugaganda kod yozishni davom ettirish zarar keltiradi (43.3).

Amaliy natijalar: eng murakkab ishni diqqat eng ko'p bo'lgan vaqtga qo'yish; diqqat tugaganda mexanik ishga o'tish (hujjat, kichik tuzatish, review); va kofe yoki irodani diqqat o'rniga ishlatmaslik.

### 46.2 Oqim holati haqidagi afsona

"Oqim" (flow) holati — vaqt sezilmaydigan, tez kod yozilayotgan holat — ko'pincha ideal deb ko'rsatiladi. Amalda u aralash natija beradi: tezlik oshadi, lekin umumiy ko'rinish torayadi. Oqimda yozilgan kod ko'pincha keyin refaktoring talab qiladi, chunki muallif katta rasmni ko'rmagan.

Amaliy tavsiya: oqimni maqsad qilmaslik; o'rniga qisqa, ongli siklda ishlash (TDD sikli, 31.1) va har sikldan keyin bir qadam orqaga chiqib qarash. Juftlikda ishlash oqimni tabiiy ravishda buzadi va bu uning foydasi (41.7).

### 46.3 Uzilishlarni boshqarish

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

### 46.4 Pomodoro va vaqt bloklari

Pomodoro texnikasi: 25 daqiqa uzilmasdan ishlash, 5 daqiqa tanaffus; to'rt siklda uzun tanaffus. Uning asosiy foydasi vaqt o'lchash emas, **uzilishlardan himoya**: 25 daqiqa ichida hech narsaga javob berilmaydi.

Amaliy moslashtirish: 25 daqiqa ba'zi ishlar uchun qisqa (murakkab debug), shuning uchun 50/10 ham ishlaydi. Muhimi — blok ichida uzilish bo'lmasligi va blok oxirida ongli to'xtash.

### 46.5 Ko'r yo'lak va botqoqdan chiqish

**Ko'r yo'lak** (blind alley) — tanlangan yondashuv ishlamayotgani aniq bo'lgan holat. Professional javob: tan olish va qaytish. Sarflangan vaqt argument emas (sunk cost): u allaqachon ketgan.

**Botqoq** (marsh) — yondashuv ishlaydi, lekin sekin va qimmat; har bir qadam qiyinlashadi. Botqoq ko'r yo'lakdan xavfliroq, chunki unda qolish mumkin.

| Belgi | Harakat |
|---|---|
| Uch urinish, natija yo'q | to'xtash, boshqa yondashuvni ko'rib chiqish |
| Har bir tuzatish yangi xato beradi | yondashuvni qayta ko'rish |
| "Faqat yana bir soat" uch marta takrorlandi | tanaffus, keyin yangi ko'z bilan |
| Yechim tushunilmaydi, lekin ishlaydi | tushunmaguncha davom etmaslik (41.2) |
| Vaqt budjeti oshdi | to'xtash va yordam so'rash |

Eng arzon chiqish usuli — boshqa odamga tushuntirish. Ko'p holatda muammo tushuntirish paytida o'zi hal bo'ladi.

### 46.6 Majlis: qachon chiqib ketish haqli

Majlis vaqtni eng ko'p yo'qotadigan manba, lekin undan butunlay qochish ham ishlamaydi. Amaliy mezon: majlisda **sizdan** nimadir talab qilinmasa va siz ma'lumot olmasangiz, qatnashish keraksiz.

Qoidalar: kun tartibi bo'lmagan majlisga rozilik bermaslik; majlis maqsadi bajarilgach chiqib ketish haqli; va ko'p odam qatnashadigan uzun majlis o'rniga qisqa yozma yangilanish taklif qilish.

### 46.7 Kod kata, dojo va ataylab mashq

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

### 46.8 Debug vaqti: eng qimmat va eng kam hisobga olinadigan

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

### 46.9 Amalda qo'llash

- [ ] Bir hafta davomida kun bo'yi diqqat darajasini yozib borib, murakkab ishni eng yuqori vaqtga ko'chiring.
- [ ] Kalendarda kuniga kamida ikki soat bloklangan ish vaqtini belgilang va uni himoya qiling.
- [ ] Uzilishdan oldin kontekstni yozib qoldirish odatini joriy qiling.
- [ ] Pomodoro yoki 50/10 siklini bir hafta sinab, natijani baholang.
- [ ] Har bir murakkab vazifa uchun oldindan vaqt budjeti belgilab, oshganda to'xtash qoidasini qo'llang.
- [ ] Kun tartibi yo'q majlislarga rozilik bermaslik qoidasini joriy qiling.
- [ ] Jamoa uchun haftada bir soatlik dojo tashkil qilib, Gilded Rose katasidan boshlang.
- [ ] Debug vaqtini bir oy davomida o'lchab, eng ko'p vaqt ketgan sohaga test va log qo'shing.
## 47. Birgalikda ishlash va o'rgatish (Collaboration and Mentoring)

Toza kod jamoaviy natija: bir odam yolg'iz uni saqlab qola olmaydi. Bu bobda jamoaviy egalik, ustoz-shogird munosabati, standartni yetkazish va jamoa kelishuvi. Code review mexanikasi va texnik yetakchilik arxitektor hujjatida (36-bob).

### 47.1 Kodga egalik: shaxsiy emas, jamoaviy

"Bu mening kodim" munosabati ikki zarar keltiradi: muallif tanqidni shaxsiy qabul qiladi, va boshqalar shu kodga tegishdan qochadi. Natijada bilim bir odamda to'planadi va kod o'sishdan to'xtaydi.

Jamoaviy egalik amaliy qoidalarga tayanadi: har bir fayl har qanday jamoa a'zosi tomonidan o'zgartirilishi mumkin; `@author` tegi ishlatilmaydi (9.5); va review izohlari kodga, odamga emas, qaratiladi.

```
Yomon: "Nega sen bu yerda Optional ishlatmagansan?"
Yaxshi: "Bu metod null qaytarishi mumkinmi? Optional aniqroq bo'lardi."
```

Jamoaviy egalik "hech kim javob bermaydi" degani emas: CODEOWNERS bilan sohaga mas'ul belgilanadi (arxitektor hujjati 36.10), lekin mas'ullik to'siq emas, bilim markazi bo'ladi.

### 47.2 Ustoz-shogird modeli

Dasturlash kasbini kitobdan o'rganib bo'lmaydi: uning katta qismi — qaror qabul qilish usuli, va u faqat kuzatish va qaytarma aloqa bilan uzatiladi. Shu sababli ustoz-shogird munosabati eng samarali o'qitish shakli bo'lib qolgan.

| Daraja | Nima kerak | Qanday beriladi |
|---|---|---|
| Yangi boshlovchi | aniq qoida va chegara | shablon kod, aniq vazifa, tez review |
| O'rtacha | sabablarni tushunish | "nega shunday" suhbatlari, juftlikda ishlash |
| Mustaqil | qaror sifatiga qaytarma aloqa | dizayn muhokamasi, ADR review |
| Tajribali | boshqalarni o'qitish | mentorlik, standart belgilash |

### 47.3 Yangi odamga toza kod standartini yetkazish

Standartni hujjat bilan yetkazish eng kam samarali usul: hujjat o'qiladi va esdan chiqadi. Samarali usullar tartibi boshqa.

1. **Namuna kod**: shablon loyiha va mavjud kod — yangi odam shunga qaraydi (arxitektor hujjati 36.9).
2. **Mashina**: formatter va linter qoidalarni darhol o'rgatadi (13, 42 boblar).
3. **Review**: birinchi besh PR da batafsil, sabab bilan izohlar.
4. **Juftlikda ishlash**: birinchi haftada bir-ikki sessiya (41.7).
5. **Hujjat**: qolgan qism uchun havola sifatida (48-bob).

Eng tez xato — yangi odamga 50 qoidadan iborat hujjat berib, keyin review da hammasini talab qilish. To'g'ri yondashuv: birinchi haftada 5 qoida, keyin bosqichma-bosqich.

### 47.4 Review ni o'rgatish vositasiga aylantirish

Review ning o'qitish funksiyasi arxitektor hujjatida (36.7) ko'rilgan. Bu yerda qo'shimcha amaliy qoidalar: izohda **sabab** bo'lishi, muqobil taklif bo'lishi, va izohlar soni cheklangan bo'lishi.

| Izoh shakli | Samarasi |
|---|---|
| "Bu yomon" | nol |
| "Buni o'zgartir" | past (nega?) |
| "Bu metod ikki ish qiladi; `validate` ni ajratsak testlash osonlashadi" | yuqori |
| "Shu holatda `Optional` afzal, chunki ... (hujjatda 18.7)" | yuqori |
| 30 ta izoh bir PR da | nol (prioritet yo'q) |
| 3 ta muhim izoh + "qolgani ixtiyoriy" | yuqori |

Qo'shimcha texnika: izohlarga prefiks qo'yish — `[majburiy]`, `[taklif]`, `[savol]`, `[nit]`. Bu prioritetni darhol ko'rsatadi va muallif vaqtini tejaydi.

### 47.5 Jamoa kelishuvi (working agreement) yozish

Jamoa kelishuvi — og'zaki qoidalarni yozma shaklga keltirish. Uning qiymati bahsni yopishda: "biz shunday kelishganmiz" argumenti did haqidagi muhokamani to'xtatadi.

```markdown
# Jamoa kelishuvi

## Kod
- Formatlash: Spotless (google-java-format AOSP); review da uslub muhokama qilinmaydi.
- Yangi value object lar `record` sifatida yoziladi.
- Pul `Money` turida; `double` taqiqlangan (ArchUnit tekshiradi).
- Konstruktor inyeksiyasi; maydon inyeksiyasi taqiqlangan.
- Lombok: `@Getter`, `@RequiredArgsConstructor`, `@Slf4j` ruxsat; `@Data`, `@SneakyThrows` taqiqlangan.

## Commit va PR
- Atomik commit; formatlash va mantiq alohida commitda.
- Conventional commits prefikslari.
- PR 400 qatordan katta bo'lsa bo'linadi.
- PR ochishdan oldin o'zini review qilish ro'yxati to'ldiriladi.

## Review
- Navbat: PR ochilgandan 4 ish soati ichida birinchi javob.
- Izoh prefikslari: [majburiy], [taklif], [savol], [nit].
- Majburiy izohlar soni 5 dan oshsa, juftlikda ishlashga o'tiladi.

## Tugatish
- Ishni tugatish ta'rifi: `docs/definition-of-done.md`.
- Testsiz xatti-harakat o'zgarishi merge qilinmaydi.

## Qayta ko'rish
- Bu kelishuv har chorakda ko'rib chiqiladi; oxirgi: 2026-01-15.
```

### 47.6 Amalda qo'llash

- [ ] `@author` teglarini olib tashlab, egalikni CODEOWNERS ga ko'chiring.
- [ ] Review izohlarini kodga qaratilgan shaklga o'tkazish uchun 47.1 dagi misollarni jamoaga ko'rsating.
- [ ] Izoh prefikslarini ([majburiy], [taklif], [savol], [nit]) joriy qiling.
- [ ] Yangi odam uchun birinchi hafta rejasini yozing: 5 qoida, shablon loyiha, ikki juftlik sessiyasi.
- [ ] Shablon loyihani (yoki mavjud eng toza modulni) namuna sifatida belgilang va havola bering.
- [ ] Jamoa kelishuvini 47.5 shabloni bo'yicha yozib, repoda saqlang.
- [ ] Kelishuvni har chorakda ko'rib chiqish sanasini kalendarda belgilang.
- [ ] Har bir kritik tizimda kamida ikki odam o'zgartirish kirita olishini ta'minlang (arxitektor hujjati 36.10).
# XIII. Ma'lumotnoma

## 48. Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari (Quick Reference)

Bu bob kundalik ishlatish uchun: jadvallar va tekshiruv ro'yxatlari. Hujjatning qolgan qismi "nega" ga javob beradi, bu bob "qanday" ni bir sahifada beradi.

### 48.1 Nomlash qoidalari jadvali

| Element | Qoida | Misol | Bo'lim |
|---|---|---|---|
| Sinf | ot iborasi, `Manager`/`Helper` siz | `SettlementImporter` | 2.9 |
| Interfeys | domen roli, `I` prefiksisiz | `PaymentGateway` | 2.7 |
| Implementatsiya | mexanika nomi, `Impl` siz | `StripePaymentGateway` | 3.6 |
| Metod | fe'l iborasi | `reserveStockFor` | 2.9 |
| `boolean` | `is`/`has`/`can`/`should`, inkorsiz | `settled`, `canBeCancelled` | 3.1 |
| To'plam | ko'plik, tur nomisiz | `orders`, `ordersByCustomer` | 3.2 |
| Konstanta | `UPPER_SNAKE`, birlik bilan | `MAX_RETRY_ATTEMPTS` | 3.4 |
| Enum turi | birlikda ot | `SettlementStatus` | 3.5 |
| Istisno | muammo + `Exception` | `RefundExceedsPaymentException` | 3.10 |
| Generik | `T`, `K`, `V`; ko'p bo'lsa to'liq | `Repository<T, ID>` | 3.8 |
| Paket | kichik harf, xususiyat bo'yicha | `uz.shop.payment` | 3.11 |
| Birlik | nomda yoki turda | `timeoutMs`, `Duration` | 3.3 |
| Nom uzunligi | qamrovga mutanosib | `i` → `taxedOrderTotal` | 2.15 |

### 48.2 Funksiya qoidalari jadvali

| Jihat | Qoida | Bo'lim |
|---|---|---|
| Uzunlik | bir ekranga sig'adi; 4-12 qator tipik | 4.1 |
| Javobgarlik | bitta ish; ajratib bo'lmaslik sinovi | 4.2 |
| Abstraksiya | bir funksiya - bir daraja | 4.2 |
| Tartib | chaqiruvchi yuqorida (stepdown) | 4.4, 11.9 |
| Argument soni | 0-2 yaxshi, 3 asoslanadi, 4+ obyekt | 5.1 |
| Flag argumenti | yo'q; ikki metod yoki enum | 5.3 |
| Chiqish argumenti | yo'q; qaytish qiymati | 5.5 |
| `return` soni | kichik funksiyada muhim emas | 4.7 |
| Chuqurlik | ikki darajadan oshmasin | 6-bob, arxitektor 4.4 |
| Qavs | har doim, bir qator uchun ham | 4.8 |
| `null` | qaytarilmaydi, uzatilmaydi | 18.7 |
| To'plam qaytarish | bo'sh to'plam, `null` emas | 18.8 |

### 48.3 Izoh qoidalari jadvali

| Izoh turi | Qoldiriladi? | Bo'lim |
|---|---|---|
| Litsenziya | ha, qisqa | 8.3 |
| Qaror asosi ("nega") | ha | 8.4, arxitektor 4.5 |
| Tashqi cheklov (limit, format) | ha | 8.4 |
| Oqibat haqida ogohlantirish | ha | 8.6 |
| Formula/huquqiy asos havolasi | ha | 8.9 |
| `TODO` (ticket + shart bilan) | ha | 8.7 |
| Kodni takrorlash | yo'q | 9.2 |
| Chalg'ituvchi | yo'q | 9.3 |
| Mazmunsiz Javadoc | yo'q | 9.4 |
| O'zgarish jurnali, `@author` | yo'q | 9.5 |
| Banner, qavs izohi | yo'q | 9.7 |
| Izohga olingan kod | yo'q, darhol o'chirish | 9.8 |
| `FIXME` | yo'q, CI bloklaydi | 8.7 |

### 48.4 Formatlash qoidalari jadvali

| Jihat | Qiymat | Bo'lim |
|---|---|---|
| Indentatsiya | 4 bo'shliq, tab emas | 12.4 |
| Qator uzunligi | 100 (yoki 120) | 12.1 |
| Fayl uzunligi | 500 dan kam | 11.1 |
| A'zolar tartibi | konstanta, maydon, konstruktor, metod | 11.6 |
| Import | guruhlangan, yulduzcha yo'q | 12.7 |
| Gorizontal tekislash | ishlatilmaydi | 12.3 |
| Zanjirli chaqiruv | har bo'g'in alohida qatorda | 12.8 |
| Kodirovka | UTF-8 | 12.10 |
| Qator oxiri | LF | 12.10 |
| Formatter | Spotless, majburiy | 13.3 |
| Formatlash commiti | alohida | 13.6 |

### 48.5 Xato bilan ishlash jadvali

| Vaziyat | To'g'ri harakat | Bo'lim |
|---|---|---|
| Topilmasligi normal | `Optional.empty()` | 18.1 |
| Topilmasligi xato | domen istisnosi | 18.1 |
| Istisnoni qayta tashlash | sabab bilan (`cause`) | 19.1 |
| Resurs | `try-with-resources` | 19.4 |
| `InterruptedException` | belgini tiklash | 19.5 |
| `Throwable`/`Error` | tutilmaydi | 19.6 |
| Log va tashlash | ikkisi birga qilinmaydi | 19.7 |
| Kirish tekshiruvi | oshkor istisno, `assert` emas | 19.8 |
| Validatsiya joyi | chegara, konstruktor, domen | 5.11 |
| API xatosi | `ProblemDetail` + barqaror kod | 27.3 |
| Xato xabari | adresatga qarab uch xil | 19.10 |

### 48.6 Hid → refaktoring moslik jadvali

To'liq jadval 37.16 da. Eng ko'p ishlatiladigan o'ntasi:

| Hid | Harakat |
|---|---|
| Uzun funksiya | Extract Function |
| Sirli nom | Rename |
| Uzun parametr ro'yxati | Introduce Parameter Object |
| Ma'lumot to'dasi | Extract Class |
| Primitivlarga berilish | Replace Primitive with Object |
| Takrorlangan `switch` | Replace Conditional with Polymorphism |
| Feature envy | Move Function |
| Xabar zanjiri | Hide Delegate |
| Global ma'lumot | Encapsulate Variable |
| `null` zanjiri | Introduce Special Case |

### 48.7 Commit oldidan tekshiruv ro'yxati

- [ ] Diff ni to'liq o'qib chiqdim; har bir qator kerakli.
- [ ] Debug log, `System.out`, izohga olingan kod, yangi `TODO` qolmadi.
- [ ] Formatlash va lint o'tdi (`spotless:check`, `checkstyle:check`).
- [ ] Testlar lokalda yashil; yangi xatti-harakat uchun test bor.
- [ ] Commit atomik: formatlash va mantiq aralashmagan.
- [ ] Commit xabarida "nega" yozilgan va prefiks to'g'ri.
- [ ] Sir, token, parol diff da yo'q.
- [ ] Public API o'zgargan bo'lsa Javadoc yangilangan.

### 48.8 Review paytida tekshiruv ro'yxati (toza kod qismi)

Arxitektor hujjati 36.1-36.4 review ning nimani topishi kerakligini ko'rib chiqadi. Bu ro'yxat uning toza kodga tegishli qismi.

- [ ] Nomlar maqsadni ochib beradi; qisqartma va shovqin so'z yo'q (2-3 bob).
- [ ] Funksiyalar bitta ish qiladi; chuqurlik ikki darajadan oshmaydi (4, 6 bob).
- [ ] `boolean` va chiqish argumentlari yo'q (5.3, 5.5).
- [ ] Izohlar "nega" ni aytadi; eskirgan izoh yo'q (8-9 bob).
- [ ] `null` qaytarilmaydi; bo'sh to'plam qaytariladi (18.7-18.8).
- [ ] Istisnolar kontekst bilan; sabab uzatiladi; log bir joyda (19.1, 19.7).
- [ ] Pul `BigDecimal`/`Money`; vaqt `Clock` orqali (20.1, 22.3).
- [ ] To'plam getter lari o'zgartirilmas qaytaradi (14.7).
- [ ] `equals`/`hashCode` juftlikda va to'g'ri (15.1-15.2).
- [ ] Testlar xatti-harakatni tekshiradi; mantiq yo'q (30.4).
- [ ] Yangi bog'liqlik asoslangan (arxitektor 38.4-38.5).
- [ ] O'zgarish qaytarilishi oson (atomik, feature flag).

### 48.9 Yangi sinf uchun tekshiruv ro'yxati

- [ ] Sinf nomi ot iborasi va javobgarligini cheklaydi.
- [ ] `final` (vorislik uchun mo'ljallanmagan bo'lsa).
- [ ] Barcha maydonlar `private final`.
- [ ] Konstruktor invariantni tekshiradi; yaroqsiz obyekt yaratib bo'lmaydi.
- [ ] Tashqaridan kelgan to'plam va massivlar nusxalanadi.
- [ ] Value object bo'lsa `record`; entitet bo'lsa id bo'yicha tenglik.
- [ ] `toString` sezgir ma'lumot chiqarmaydi.
- [ ] Ko'rinish eng kichik darajada (`package-private` standart).
- [ ] Javadoc faqat public API da va shartnoma bilan.
- [ ] Bog'liqliklar konstruktor orqali, soni 4 dan kam.
- [ ] Test yozish oson bo'ldi (aks holda dizayn signali, 31.5).

### 48.10 Terminlar lug'ati

| Atama | Ma'nosi |
|---|---|
| Guard clause | metod boshida yaroqsiz holatni tekshirib erta qaytish |
| Stepdown rule | har bir funksiya o'zidan keyingi funksiyalarni chaqiradi |
| DAMP | testda tavsifiy va takrorlanadigan kodga ruxsat |
| Data clump | birga sayohat qiladigan parametr guruhi |
| Train wreck | `a.b().c().d()` shaklidagi zanjir |
| Middle man | faqat delegatsiya qiladigan sinf |
| Refused bequest | voris sinf merosni ishlatmasligi |
| Seam | xatti-harakatni almashtirish mumkin bo'lgan nuqta |
| Branch by abstraction | abstraksiya ortida bosqichma-bosqich almashtirish |
| PECS | Producer Extends, Consumer Super |
| DAMP/DRY | tavsifiylik va takrorlanmaslik muvozanati |
| Boy Scout Rule | tegilgan kodni topganingdan tozaroq qoldirish |
| Flaky test | bir xil kodda ba'zan yiqiladigan test |
| Sunk cost | sarflangan vaqt; qaror uchun argument emas |
| Noaniqlik konusi | baho aniqligi ma'lumot bilan oshishi |
| Diqqat-mana | kun bo'yi cheklangan aqliy diqqat resursi |

### 48.11 Besh hujjat bilan bog'lanish xaritasi

| Savol | Hujjat va bo'lim |
|---|---|
| Nomni qanday yozaman? | shu hujjat, 2-3 |
| Nomni domen tilidan olish | arxitektor, 4.2 |
| Funksiya qanday bo'linadi? | shu hujjat, 4-5 |
| Kognitiv yuk va chuqurlik | arxitektor, 4.3-4.4 |
| Izoh qoldirilsinmi? | shu hujjat, 8-9 |
| Formatlash sozlamasi | shu hujjat, 11-13 |
| `equals`/`hashCode` | shu hujjat, 15 |
| Abstraksiya va chegara | arxitektor, 5 |
| Murakkablik va texnik qarz | arxitektor, 6 |
| Qaysi pattern kerak? | patternlar, 1-24, 27-30 |
| SOLID va GRASP | patternlar, 26 |
| Anti-pattern nomi | patternlar, 25 |
| Xato bilan ishlash | shu hujjat, 18-19 |
| Istisno ierarxiyasi dizayni | arxitektor, 13.7 |
| Pul, vaqt, satr, to'plam | shu hujjat, 20-23 |
| Record, sealed, `Optional`, Stream | arxitektor, 13 |
| Spring mexanikasi | arxitektor, 15-20 |
| Spring kodi uslubi | shu hujjat, 26-27 |
| JPA mexanikasi va N+1 | arxitektor, 18 |
| JPA kodi uslubi | shu hujjat, 28 |
| PostgreSQL ichki tuzilishi | arxitektor, 21-27 |
| Log narxi va kuzatuvchanlik | arxitektor, 30 |
| Log kodi uslubi | shu hujjat, 29 |
| Test strategiyasi va texnikasi | testlash qo'llanmasi |
| Test kodi tozaligi va TDD | shu hujjat, 30-31 |
| Kod hidi va refaktoring harakati | shu hujjat, 32-38 |
| Legacy refaktoring strategiyasi | arxitektor, 34 |
| Build va versiya nazorati | shu hujjat, 39-41 |
| Statik tahlil vositalari | shu hujjat, 42 |
| Sonar qoidalari va quality gate | SonarQube hujjati |
| Professional intizom | shu hujjat, 43-47 |
| Code review va yetakchilik | arxitektor, 36 |
| O'rganish va texnologiya tanlash | arxitektor, 38 |
## 49. O'z-o'zini baholash: toza kod yetukligi (Self-Assessment)

Bu bob hujjatni o'zingizga qo'llash uchun: qaysi mavzuda qay darajada turganingizni aniqlash va keyingi qadamni tanlash. Arxitektor hujjatining oxirgi bobi (39) arxitektura bilimini baholaydi; bu bob toza kod amaliyotini baholaydi.

### 49.1 Yetuklik darajalari

Har bir mavzu uchun to'rt daraja bor va o'zini baholash shu shkala bo'yicha boradi.

| Daraja | Belgisi |
|---|---|
| 1 - Bilmayman | qoida mavjudligini bilmayman |
| 2 - Bilaman | qoidani bilaman, lekin eslatish kerak |
| 3 - Qo'llayman | kod yozganda avtomatik qo'llayman |
| 4 - O'rgataman | boshqalarga tushuntiraman va qoidani majburlaydigan tizim quraman |

Maqsad hamma mavzuda 4 ga chiqish emas: kundalik ishga tegishli mavzularda 3-4, qolganlarda 2 yetarli.

### 49.2 Nomlash va o'qilishi: o'zingizni sinash

- [ ] Nom javob berishi kerak bo'lgan uchta savolni aytib bera olaman (2.1).
- [ ] `isNotEligible` nomi nega yomon ekanini tushuntiraman (3.1).
- [ ] `IOrderRepository` nomining ikki muammosini sanayman (2.7).
- [ ] `timeoutMs` dan ko'ra `Duration timeout` nega afzal (3.3).
- [ ] `get`/`find`/`fetch` taqsimotini jamoada qanday majburlash mumkin (2.11, 42.4).
- [ ] Nom uzunligi qamrovga qanday bog'liq (2.15).

### 49.3 Funksiya va oqim: o'zingizni sinash

- [ ] "Bitta ish qiladi" ni qanday tekshiraman (4.2).
- [ ] Flag argumenti nega "bitta ish" qoidasini buzadi (5.3).
- [ ] Chiqish argumentini nima bilan almashtiraman (5.5).
- [ ] Enum ustidagi `switch` da `default` nega yozilmaydi (6.6).
- [ ] Yashirin vaqt bog'liqligini qanday ko'rinadigan qilaman (6.9).
- [ ] Siklni quvurga aylantirish mezonini aytib bera olaman (7.7).

### 49.4 Obyekt, holat, xato: o'zingizni sinash

- [ ] `final List` nega o'zgarmaslikni kafolatlamaydi (16.1).
- [ ] `Collections.unmodifiableList` va `List.copyOf` farqi (16.3).
- [ ] `equals` ning besh qoidasini sanayman (15.1).
- [ ] Entitet va value object tengligi farqi (15.5).
- [ ] `compareTo` va `equals` izchilligi nega muhim (15.6).
- [ ] `finally` ichidagi `return` nima qiladi (19.3).
- [ ] `InterruptedException` tutilganda nima qilish kerak (19.5).
- [ ] Konstruktorda `this` ni tashqariga berish nega xavfli (14.10).

### 49.5 Java va Spring: o'zingizni sinash

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

### 49.6 Hid, refaktoring, jarayon: o'zingizni sinash

- [ ] Takrorlanishning to'rt turini va ularning yechimini sanayman (32.2).
- [ ] Soxta takrorlanishni nega birlashtirmaslik kerak (32.2).
- [ ] Hide Delegate va Remove Middle Man qachon qo'llanadi (36.3-36.4).
- [ ] Katta refaktoringni to'rt qadamga qanday bo'laman (38.5).
- [ ] Refaktoring commiti va mantiq commitini nega ajrataman (38.4).
- [ ] Nomni o'zgartirgandan keyin IDE ko'rmagan olti joyni sanayman (38.3).
- [ ] Yangi lint qoidasini besh bosqichda qanday joriy qilaman (42.6).
- [ ] Atomik commitning uch shartini aytaman (40.1).

### 49.7 Professional intizom: o'zingizni sinash

- [ ] "Urinib ko'raman" nega yolg'on javob (44.2).
- [ ] Majburiyatning uch qismini sanayman (44.3).
- [ ] Uch nuqtali bahodan kutilgan qiymatni hisoblayman (45.2).
- [ ] Bosim ostida nimani qisqartiraman, nimani hech qachon (45.7).
- [ ] "90% tayyor" hisobotini nima bilan almashtiraman (45.6).
- [ ] Botqoq va ko'r yo'lak farqini va chiqish usulini bilaman (46.5).
- [ ] Review izohini o'rgatish vositasiga qanday aylantiraman (47.4).

### 49.8 Kod bazasini baholash: bir sahifali audit

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

### 49.9 Keyingi qadam: hujjatni qanday ishlatish

Bu hujjatni boshdan-oxir o'qish shart emas va samarali ham emas. Uchta ishlatish usuli bor.

**Birinchi — muammo bo'yicha.** Aniq savol tug'ilganda 48.11 jadvalidan bo'limni topish. Bu eng ko'p ishlatiladigan usul.

**Ikkinchi — jamoa standarti sifatida.** 48-bobdagi jadvallarni jamoa kelishuviga (47.5) ko'chirish, keyin 42-bob bo'yicha ularni mashinaga topshirish. Bu hujjatning asosiy qiymati shu yerda: qoida mashinaga ko'chganda u haqiqatan ishlaydi.

**Uchinchi — o'sish rejasi sifatida.** 49.2-49.7 bo'limlaridagi savollarga javob berib, 2 dan past darajadagi mavzularni ro'yxatlab, chorakda uch mavzuni 3 darajaga chiqarish.

### 49.10 Amalda qo'llash

- [ ] 49.2-49.7 bo'limlaridagi savollarga halol javob berib, har bir mavzuga 1-4 daraja qo'ying.
- [ ] 2 va undan past darajadagi mavzulardan uchtasini tanlab, chorak maqsadi qiling.
- [ ] 49.8 dagi auditni ishga tushirib, natijani sanasi bilan repoda saqlang.
- [ ] Audit natijasidagi eng katta uch raqamni tuzatish rejasiga aylantiring.
- [ ] 48-bobdagi jadvallardan jamoa kelishuviga ko'chiriladigan qismlarni ajratib oling.
- [ ] Mashinaga topshirilishi mumkin bo'lgan qoidalarni 42-bob bo'yicha joriy qilish rejasini tuzing.
- [ ] Hujjatni jamoaga tanishtirishda 48.11 xaritasidan boshlang: qaysi savol qaysi hujjatda.
- [ ] Chorak oxirida auditni qaytarib, raqamlar yo'nalishini (yaxshilanish yoki yomonlashish) baholang.
