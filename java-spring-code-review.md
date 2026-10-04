# Kod review: diffni o'qish, xatoni ko'rish, qarorni tekshirish

Bu hujjat kod review ni alohida muhandislik sohasi sifatida ko'radi. Savol bitta:
oldingizda diff turibdi, unda nimani ko'rasiz, nimani so'raysiz va nimani to'xtatasiz.
Tayanch stek: Java, Spring va PostgreSQL.

Hujjat beshlikning bir qismi va qolganlari bilan kesishmaydi:

- pattern katalogi - `java-spring-design-patterns.md`
- test yozish texnikasi - `java-spring-testing-handbook.md`
- JVM, Spring va PostgreSQL ichki mexanikasi - `java-spring-architect-mindset.md`
- statik tahlil qoidalari va quality gate - `java-spring-sonarqube.md`

Bu yerda ularning bilimi review stoliga olib chiqiladi: qaysi mexanika diffda qanday
belgi qoldiradi, va shu belgini ko'rgan reviewer nima deyishi kerak. Mexanikaning
o'zi kerak bo'lsa, tegishli hujjatga mavzu nomi bilan havola qilinadi.

Hujjat kimga: kod yozadigan arxitektor, tech lead, review ga kuniga vaqt ajratadigan
senior va o'z PR ini review dan o'tkazishni o'rganmoqchi bo'lgan developer.

Har bob oxirida `Amalda qo'llash` ro'yxati bor: loyihada darhol bajariladigan bandlar.
Review izohlari uchun tayyor iboralar oxirgi bobda.

## Mundarija


**[I. Review ning mohiyati va iqtisodi](#i-review-ning-mohiyati-va-iqtisodi)**

- [1. Review nima uchun bor va nimani haqiqatda beradi (Why Review Exists)](#1-review-nima-uchun-bor-va-nimani-haqiqatda-beradi-why-review-exists)
  - [1.1 Review ning uchta haqiqiy mahsuloti](#11-review-ning-uchta-haqiqiy-mahsuloti)
  - [1.2 Review nimani topmaydi](#12-review-nimani-topmaydi)
  - [1.3 Filtrlarning mehnat taqsimoti](#13-filtrlarning-mehnat-taqsimoti)
  - [1.4 Approve nimani anglatadi va nimani anglatmaydi](#14-approve-nimani-anglatadi-va-nimani-anglatmaydi)
  - [1.5 Review mas'uliyatni ko'chirmaydi](#15-review-masuliyatni-kochirmaydi)
  - [1.6 Review ning yon ta'siri: PR hajmini kichraytirishga majbur qilish](#16-review-ning-yon-tasiri-pr-hajmini-kichraytirishga-majbur-qilish)
  - [1.7 Qachon review foyda bermaydi](#17-qachon-review-foyda-bermaydi)
  - [1.8 Review arxitektura qaroridan keyin keladi](#18-review-arxitektura-qaroridan-keyin-keladi)
  - [1.9 Review maqsadini jamoada yozib qo'yish](#19-review-maqsadini-jamoada-yozib-qoyish)
  - [1.10 Review madaniyatini o'lchash uchun uchta savol](#110-review-madaniyatini-olchash-uchun-uchta-savol)
  - [1.11 Amalda qo'llash](#111-amalda-qollash)
- [2. Review iqtisodi: xato narxi, navbat va PR hajmi (The Economics of Review)](#2-review-iqtisodi-xato-narxi-navbat-va-pr-hajmi-the-economics-of-review)
  - [2.1 Xato narxi bosqich bo'yicha o'sadi](#21-xato-narxi-bosqich-boyicha-osadi)
  - [2.2 PR hajmi va topish darajasi](#22-pr-hajmi-va-topish-darajasi)
  - [2.3 Navbat nazariyasi: kutish vaqti review ning asosiy narxi](#23-navbat-nazariyasi-kutish-vaqti-review-ning-asosiy-narxi)
  - [2.4 Reviewer soni: ikkinchidan keyin qaytim tushadi](#24-reviewer-soni-ikkinchidan-keyin-qaytim-tushadi)
  - [2.5 Review byudjeti: haftada qancha vaqt](#25-review-byudjeti-haftada-qancha-vaqt)
  - [2.6 Review ni bo'lish: stacked PR texnikasi](#26-review-ni-bolish-stacked-pr-texnikasi)
  - [2.7 Rework: review ning yashirin narxi](#27-rework-review-ning-yashirin-narxi)
  - [2.8 Review ning qaytimi qachon manfiy bo'ladi](#28-review-ning-qaytimi-qachon-manfiy-boladi)
  - [2.9 Byudjetni xavf bo'yicha taqsimlash](#29-byudjetni-xavf-boyicha-taqsimlash)
  - [2.10 Raqamlarni o'z loyihangizda o'lchash](#210-raqamlarni-oz-loyihangizda-olchash)
  - [2.11 Amalda qo'llash](#211-amalda-qollash)
- [3. Reviewer ning tahlil apparati: niyat, invariant, xavf yuzasi (The Reviewer's Analytical Apparatus)](#3-reviewer-ning-tahlil-apparati-niyat-invariant-xavf-yuzasi-the-reviewers-analytical-apparatus)
  - [3.1 Review ning uch o'qishi](#31-review-ning-uch-oqishi)
  - [3.2 Niyatni koddan tiklash, tavsifdan emas](#32-niyatni-koddan-tiklash-tavsifdan-emas)
  - [3.3 Invariantni topish: nima har doim rost bo'lishi kerak](#33-invariantni-topish-nima-har-doim-rost-bolishi-kerak)
  - [3.4 Xavf yuzasi: o'zgarish nimaga tegadi](#34-xavf-yuzasi-ozgarish-nimaga-tegadi)
  - [3.5 Ko'rinmayotgan kodni ko'rish](#35-korinmayotgan-kodni-korish)
  - [3.6 Miyada ishga tushirish: beshta ssenariy](#36-miyada-ishga-tushirish-beshta-ssenariy)
  - [3.7 Chuqurlik darajasi: xavf bo'yicha triage](#37-chuqurlik-darajasi-xavf-boyicha-triage)
  - [3.8 Kognitiv tuzoqlar](#38-kognitiv-tuzoqlar)
  - [3.9 Review ni qachon to'xtatish](#39-review-ni-qachon-toxtatish)
  - [3.10 Review natijasini yozib qoldirish](#310-review-natijasini-yozib-qoldirish)
  - [3.11 Amalda qo'llash](#311-amalda-qollash)
- [4. Diffni o'qish mexanikasi (Reading a Diff)](#4-diffni-oqish-mexanikasi-reading-a-diff)
  - [4.1 Nega interfeys bergan tartib noto'g'ri](#41-nega-interfeys-bergan-tartib-notogri)
  - [4.2 To'g'ri o'qish tartibi: sakkiz qadam](#42-togri-oqish-tartibi-sakkiz-qadam)
  - [4.3 Kontekstni tiklash](#43-kontekstni-tiklash)
  - [4.4 O'chirilgan kodni o'qish](#44-ochirilgan-kodni-oqish)
  - [4.5 Commit tarixini o'qish](#45-commit-tarixini-oqish)
  - [4.6 PR ni lokalda olib tekshirish](#46-pr-ni-lokalda-olib-tekshirish)
  - [4.7 Katta PR ni xavf nuqtalari bo'yicha o'qish](#47-katta-pr-ni-xavf-nuqtalari-boyicha-oqish)
  - [4.8 Izohni qayerga va qanday qo'yish](#48-izohni-qayerga-va-qanday-qoyish)
  - [4.9 Izoh darajasini belgilash](#49-izoh-darajasini-belgilash)
  - [4.10 O'qish tezligini oshiradigan odatlar](#410-oqish-tezligini-oshiradigan-odatlar)
  - [4.11 Amalda qo'llash](#411-amalda-qollash)
- [5. Mashina va odam: SonarQube dan oldin topish (Beating the Tools)](#5-mashina-va-odam-sonarqube-dan-oldin-topish-beating-the-tools)
  - [5.1 Nega Sonar dan oldin topish kerak](#51-nega-sonar-dan-oldin-topish-kerak)
  - [5.2 Mashina deterministik tutadigan narsalar](#52-mashina-deterministik-tutadigan-narsalar)
  - [5.3 Mashina tuta olmaydigan narsalar](#53-mashina-tuta-olmaydigan-narsalar)
  - [5.4 Qo'lda statik tahlil o'tishi: o'n to'rt savol](#54-qolda-statik-tahlil-otishi-on-tort-savol)
  - [5.5 Cognitive complexity ni ko'zda hisoblash](#55-cognitive-complexity-ni-kozda-hisoblash)
  - [5.6 Null yo'lini qo'lda kuzatish](#56-null-yolini-qolda-kuzatish)
  - [5.7 Resurs oqishini ko'rish](#57-resurs-oqishini-korish)
  - [5.8 Security hotspot: mashina belgilaydi, qarorni odam qabul qiladi](#58-security-hotspot-mashina-belgilaydi-qarorni-odam-qabul-qiladi)
  - [5.9 Coverage raqami aldaganda](#59-coverage-raqami-aldaganda)
  - [5.10 Shovqinni kamaytirish va izohni qoidaga aylantirish](#510-shovqinni-kamaytirish-va-izohni-qoidaga-aylantirish)
  - [5.11 Amalda qo'llash](#511-amalda-qollash)

**[II. Arxitektura, dizayn va clean code review](#ii-arxitektura-dizayn-va-clean-code-review)**

- [6. Arxitektura review: qatlam, chegara, bog'liqlik yo'nalishi (Architecture in a Diff)](#6-arxitektura-review-qatlam-chegara-bogliqlik-yonalishi-architecture-in-a-diff)
  - [6.1 Importlar - arxitekturaning eng aniq ko'rsatkichi](#61-importlar---arxitekturaning-eng-aniq-korsatkichi)
  - [6.2 Bog'liqlik yo'nalishi: ichki qatlam tashqarini bilmaydi](#62-bogliqlik-yonalishi-ichki-qatlam-tashqarini-bilmaydi)
  - [6.3 Yangi paket va yangi modul - chegara haqida qaror](#63-yangi-paket-va-yangi-modul---chegara-haqida-qaror)
  - [6.4 Yangi tashqi bog'liqlik - eng kam baholangan arxitektura qarori](#64-yangi-tashqi-bogliqlik---eng-kam-baholangan-arxitektura-qarori)
  - [6.5 Arxitektura eroziyasini diffdan ko'rish](#65-arxitektura-eroziyasini-diffdan-korish)
  - [6.6 Qatlam o'tkazib yuborilishi (layer skipping)](#66-qatlam-otkazib-yuborilishi-layer-skipping)
  - [6.7 Chegaradan o'tadigan ma'lumot shakli](#67-chegaradan-otadigan-malumot-shakli)
  - [6.8 Hisob mantiqi qayerda turadi](#68-hisob-mantiqi-qayerda-turadi)
  - [6.9 Modullar orasidagi muloqot shakli](#69-modullar-orasidagi-muloqot-shakli)
  - [6.10 Arxitektura izohini qanday yozish](#610-arxitektura-izohini-qanday-yozish)
  - [6.11 Amalda qo'llash](#611-amalda-qollash)
- [7. Bog'liqlik, kohéziya va abstraksiya review (Coupling, Cohesion, Abstraction)](#7-bogliqlik-kohéziya-va-abstraksiya-review-coupling-cohesion-abstraction)
  - [7.1 Bog'liqlik turlarini diffda aniqlash](#71-bogliqlik-turlarini-diffda-aniqlash)
  - [7.2 Vaqt bog'liqligi: eng jim xato manbasi](#72-vaqt-bogliqligi-eng-jim-xato-manbasi)
  - [7.3 Kohéziya: nima birga o'zgarsa, birga tursin](#73-kohéziya-nima-birga-ozgarsa-birga-tursin)
  - [7.4 Soxta abstraksiya: bitta implementatsiyali interfeys](#74-soxta-abstraksiya-bitta-implementatsiyali-interfeys)
  - [7.5 DRY ning noto'g'ri qo'llanishi](#75-dry-ning-notogri-qollanishi)
  - [7.6 Oqib chiqadigan abstraksiya (leaky abstraction)](#76-oqib-chiqadigan-abstraksiya-leaky-abstraction)
  - [7.7 Feature envy va shotgun surgery](#77-feature-envy-va-shotgun-surgery)
  - [7.8 Abstraksiya darajalarining aralashuvi](#78-abstraksiya-darajalarining-aralashuvi)
  - [7.9 Konstruktor parametrlari soni - eng oson o'lchov](#79-konstruktor-parametrlari-soni---eng-oson-olchov)
  - [7.10 Abstraksiyani olib tashlash ham yaxshilanish](#710-abstraksiyani-olib-tashlash-ham-yaxshilanish)
  - [7.11 Amalda qo'llash](#711-amalda-qollash)
- [8. Clean code review: nomlash, kognitiv yuk, metod shakli (Clean Code at the Review Table)](#8-clean-code-review-nomlash-kognitiv-yuk-metod-shakli-clean-code-at-the-review-table)
  - [8.1 Nom - eng arzon hujjat va eng qimmat xato](#81-nom---eng-arzon-hujjat-va-eng-qimmat-xato)
  - [8.2 Birlik, valyuta va vaqt zonasi nomda](#82-birlik-valyuta-va-vaqt-zonasi-nomda)
  - [8.3 Metod shakli: uzunlik emas, shoxlanish](#83-metod-shakli-uzunlik-emas-shoxlanish)
  - [8.4 Boolean parametr - yashirin ikki metod](#84-boolean-parametr---yashirin-ikki-metod)
  - [8.5 Primitive obsession: domen tilini turga aylantirish](#85-primitive-obsession-domen-tilini-turga-aylantirish)
  - [8.6 Izoh qachon kerak](#86-izoh-qachon-kerak)
  - [8.7 O'lik kod va yarim ishlangan narsalar](#87-olik-kod-va-yarim-ishlangan-narsalar)
  - [8.8 Clean code bahonasida haddan oshish](#88-clean-code-bahonasida-haddan-oshish)
  - [8.9 Formatlash izohi review da bo'lmasligi kerak](#89-formatlash-izohi-review-da-bolmasligi-kerak)
  - [8.10 O'qiluvchanlikni o'lchash: review ning o'zi sinov](#810-oqiluvchanlikni-olchash-review-ning-ozi-sinov)
  - [8.11 Amalda qo'llash](#811-amalda-qollash)
- [9. SOLID va dizayn printsiplarini diffda tekshirish (Principles, Not Slogans)](#9-solid-va-dizayn-printsiplarini-diffda-tekshirish-principles-not-slogans)
  - [9.1 SRP: o'zgarish sabablarini sanash](#91-srp-ozgarish-sabablarini-sanash)
  - [9.2 OCP: yangi holat qo'shilganda nima o'zgaradi](#92-ocp-yangi-holat-qoshilganda-nima-ozgaradi)
  - [9.3 LSP: shartnomani buzgan implementatsiya](#93-lsp-shartnomani-buzgan-implementatsiya)
  - [9.4 ISP: semiz interfeys va majburiy bo'sh metodlar](#94-isp-semiz-interfeys-va-majburiy-bosh-metodlar)
  - [9.5 DIP: interfeys kimga tegishli](#95-dip-interfeys-kimga-tegishli)
  - [9.6 Demeter qonuni: zanjirli chaqiruv](#96-demeter-qonuni-zanjirli-chaqiruv)
  - [9.7 Tell, don't ask va anemik model](#97-tell-dont-ask-va-anemik-model)
  - [9.8 Kompozitsiya va meros](#98-kompozitsiya-va-meros)
  - [9.9 Command-query separation: so'rov yon ta'sir qiladimi](#99-command-query-separation-sorov-yon-tasir-qiladimi)
  - [9.10 Printsipni qurol sifatida ishlatmaslik](#910-printsipni-qurol-sifatida-ishlatmaslik)
  - [9.11 Amalda qo'llash](#911-amalda-qollash)
- [10. Dizayn pattern review I: yo'q patternni ko'rish (Missing Patterns)](#10-dizayn-pattern-review-i-yoq-patternni-korish-missing-patterns)
  - [10.1 Pattern bo'shlig'ining umumiy belgilari](#101-pattern-boshligining-umumiy-belgilari)
  - [10.2 Shoxlanishdan polimorfizmga: eng ko'p uchraydigan bo'shliq](#102-shoxlanishdan-polimorfizmga-eng-kop-uchraydigan-boshliq)
  - [10.3 Yaratish mantiqi tarqalganda: fabrika](#103-yaratish-mantiqi-tarqalganda-fabrika)
  - [10.4 Parametrlar portlashi: builder yoki parametr obyekti](#104-parametrlar-portlashi-builder-yoki-parametr-obyekti)
  - [10.5 Kesishgan vazifalar qo'lda yozilganda: decorator yoki AOP](#105-kesishgan-vazifalar-qolda-yozilganda-decorator-yoki-aop)
  - [10.6 Holat shoxlari: yashiringan holat mashinasi](#106-holat-shoxlari-yashiringan-holat-mashinasi)
  - [10.7 Tashqi tizim domen ichida: adapter va port](#107-tashqi-tizim-domen-ichida-adapter-va-port)
  - [10.8 Yozuv va xabar birga bo'lishi kerak bo'lganda: outbox](#108-yozuv-va-xabar-birga-bolishi-kerak-bolganda-outbox)
  - [10.9 Ikki marta kelgan so'rov: idempotentlik](#109-ikki-marta-kelgan-sorov-idempotentlik)
  - [10.10 Ko'p bosqichli jarayon: saga va kompensatsiya](#1010-kop-bosqichli-jarayon-saga-va-kompensatsiya)
  - [10.11 Pattern taklif qilishning narxi](#1011-pattern-taklif-qilishning-narxi)
  - [10.12 Amalda qo'llash](#1012-amalda-qollash)
- [11. Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern (Misapplied and Over-Applied Patterns)](#11-dizayn-pattern-review-ii-notogri-va-ortiqcha-qollangan-pattern-misapplied-and-over-applied-patterns)
  - [11.1 Noto'g'ri qo'llangan patternning umumiy belgilari](#111-notogri-qollangan-patternning-umumiy-belgilari)
  - [11.2 Strategy nomi bor, shoxlanish ham bor](#112-strategy-nomi-bor-shoxlanish-ham-bor)
  - [11.3 Fabrika yoki yashirin service locator](#113-fabrika-yoki-yashirin-service-locator)
  - [11.4 Repository patternining buzilgan shakllari](#114-repository-patternining-buzilgan-shakllari)
  - [11.5 Event noto'g'ri qo'llanganda](#115-event-notogri-qollanganda)
  - [11.6 Dekorator zanjiri va kuzatib bo'lmaydigan oqim](#116-dekorator-zanjiri-va-kuzatib-bolmaydigan-oqim)
  - [11.7 Singleton, statik holat va Spring](#117-singleton-statik-holat-va-spring)
  - [11.8 CQRS, event sourcing va saga: ortiqcha qo'llanish](#118-cqrs-event-sourcing-va-saga-ortiqcha-qollanish)
  - [11.9 Mapper va DTO qatlamlarining haddan oshishi](#119-mapper-va-dto-qatlamlarining-haddan-oshishi)
  - [11.10 Pattern teatri: nom bilan yashirilgan murakkablik](#1110-pattern-teatri-nom-bilan-yashirilgan-murakkablik)
  - [11.11 Pattern review jadvali: belgi, savol, javob](#1111-pattern-review-jadvali-belgi-savol-javob)
  - [11.12 Amalda qo'llash](#1112-amalda-qollash)
- [12. Code smell va anti-pattern katalogi diffda (Smells in a Diff)](#12-code-smell-va-anti-pattern-katalogi-diffda-smells-in-a-diff)
  - [12.1 Boshqaruv oqimi smell lari](#121-boshqaruv-oqimi-smell-lari)
  - [12.2 Ma'lumot va holat smell lari](#122-malumot-va-holat-smell-lari)
  - [12.3 Spring ga xos anti-patternlar](#123-spring-ga-xos-anti-patternlar)
  - [12.4 Ma'lumotlar bazasiga tegishli smell lar](#124-malumotlar-bazasiga-tegishli-smell-lar)
  - [12.5 Test smell lari](#125-test-smell-lari)
  - [12.6 Konkurentlik smell lari](#126-konkurentlik-smell-lari)
  - [12.7 Xavfsizlik smell lari (tez ro'yxat)](#127-xavfsizlik-smell-lari-tez-royxat)
  - [12.8 Operatsion smell lar](#128-operatsion-smell-lar)
  - [12.9 Smell ni oqibat tilida aytish](#129-smell-ni-oqibat-tilida-aytish)
  - [12.10 Katalogni loyihaga moslashtirish](#1210-katalogni-loyihaga-moslashtirish)
  - [12.11 Amalda qo'llash](#1211-amalda-qollash)
- [13. Domen modeli review: invariant, agregat, chegara (Reviewing the Domain Model)](#13-domen-modeli-review-invariant-agregat-chegara-reviewing-the-domain-model)
  - [13.1 Modelning asosiy savoli: invariant kim tomonidan himoyalangan](#131-modelning-asosiy-savoli-invariant-kim-tomonidan-himoyalangan)
  - [13.2 Anemik modelni ongli tanlash](#132-anemik-modelni-ongli-tanlash)
  - [13.3 Agregat chegarasi: nima birga saqlanadi](#133-agregat-chegarasi-nima-birga-saqlanadi)
  - [13.4 Value object va entity farqi diffda](#134-value-object-va-entity-farqi-diffda)
  - [13.5 Identifikator dizayni](#135-identifikator-dizayni)
  - [13.6 Domen eventlari: nima e'lon qilinadi](#136-domen-eventlari-nima-elon-qilinadi)
  - [13.7 Domen tili: kod va suhbat bir xil so'z bilan](#137-domen-tili-kod-va-suhbat-bir-xil-soz-bilan)
  - [13.8 Domen servisi qachon kerak](#138-domen-servisi-qachon-kerak)
  - [13.9 ORM domen modelini buzganda](#139-orm-domen-modelini-buzganda)
  - [13.10 Modelga tegadigan PR uchun qo'shimcha talablar](#1310-modelga-tegadigan-pr-uchun-qoshimcha-talablar)
  - [13.11 Amalda qo'llash](#1311-amalda-qollash)

**[III. Java kodini chuqur tahlil](#iii-java-kodini-chuqur-tahlil)**

- [14. Java tili darajasidagi xatolar katalogi (Language-Level Defects)](#14-java-tili-darajasidagi-xatolar-katalogi-language-level-defects)
  - [14.1 null: chegarada to'xtatish](#141-null-chegarada-toxtatish)
  - [14.2 equals, hashCode va compareTo](#142-equals-hashcode-va-compareto)
  - [14.3 Sonlar: butun bo'lish, overflow, pul](#143-sonlar-butun-bolish-overflow-pul)
  - [14.4 Satr, kodlash va formatlash](#144-satr-kodlash-va-formatlash)
  - [14.5 Vaqt va zona](#145-vaqt-va-zona)
  - [14.6 Kolleksiyalar](#146-kolleksiyalar)
  - [14.7 Stream xatolari](#147-stream-xatolari)
  - [14.8 switch, enum va sealed](#148-switch-enum-va-sealed)
  - [14.9 Istisnolar: tur va kontekst](#149-istisnolar-tur-va-kontekst)
  - [14.10 Review da tez tekshirish uchun grep to'plami](#1410-review-da-tez-tekshirish-uchun-grep-toplami)
  - [14.11 Amalda qo'llash](#1411-amalda-qollash)
- [15. Holat, mutability va concurrency review (State and Concurrency)](#15-holat-mutability-va-concurrency-review-state-and-concurrency)
  - [15.1 Umumiy holatni topish: review ning birinchi qadami](#151-umumiy-holatni-topish-review-ning-birinchi-qadami)
  - [15.2 Tekshir-keyin-yoz: eng ko'p uchraydigan poyga](#152-tekshir-keyin-yoz-eng-kop-uchraydigan-poyga)
  - [15.3 Yo'qolgan yangilanish (lost update)](#153-yoqolgan-yangilanish-lost-update)
  - [15.4 Qulf tartibi va deadlock](#154-qulf-tartibi-va-deadlock)
  - [15.5 Bir JVM dagi qulf ko'p instansda ishlamaydi](#155-bir-jvm-dagi-qulf-kop-instansda-ishlamaydi)
  - [15.6 Atomiklik illuziyasi](#156-atomiklik-illuziyasi)
  - [15.7 Thread pool va navbat review](#157-thread-pool-va-navbat-review)
  - [15.8 @Async va xatoning yo'qolishi](#158-async-va-xatoning-yoqolishi)
  - [15.9 ThreadLocal va kontekst oqishi](#159-threadlocal-va-kontekst-oqishi)
  - [15.10 Virtual thread va pinning](#1510-virtual-thread-va-pinning)
  - [15.11 Concurrency uchun review checklisti](#1511-concurrency-uchun-review-checklisti)
  - [15.12 Amalda qo'llash](#1512-amalda-qollash)
- [16. Resurs, xotira va GC bosimi review (Resources and Memory)](#16-resurs-xotira-va-gc-bosimi-review-resources-and-memory)
  - [16.1 Chegarasiz to'plam - eng ko'p uchraydigan OOM sababi](#161-chegarasiz-toplam---eng-kop-uchraydigan-oom-sababi)
  - [16.2 Hajmni diffdan baholash](#162-hajmni-diffdan-baholash)
  - [16.3 Resursni yopish](#163-resursni-yopish)
  - [16.4 Kesh - boshqarilmagan xotira](#164-kesh---boshqarilmagan-xotira)
  - [16.5 Allokatsiya bosimi: GC ni ko'p ishlashga majburlash](#165-allokatsiya-bosimi-gc-ni-kop-ishlashga-majburlash)
  - [16.6 Katta javob va serializatsiya](#166-katta-javob-va-serializatsiya)
  - [16.7 Xotira oqishining tipik manbalari Spring da](#167-xotira-oqishining-tipik-manbalari-spring-da)
  - [16.8 Connection pool: eng tez tugaydigan resurs](#168-connection-pool-eng-tez-tugaydigan-resurs)
  - [16.9 Review paytida xotirani o'lchash](#169-review-paytida-xotirani-olchash)
  - [16.10 Amalda qo'llash](#1610-amalda-qollash)
- [17. Zamonaviy Java review: record, sealed, pattern matching, virtual thread (Modern Java)](#17-zamonaviy-java-review-record-sealed-pattern-matching-virtual-thread-modern-java)
  - [17.1 record: qachon to'g'ri, qachon noto'g'ri](#171-record-qachon-togri-qachon-notogri)
  - [17.2 sealed: to'liqlikni kompilyatorga topshirish](#172-sealed-toliqlikni-kompilyatorga-topshirish)
  - [17.3 Pattern matching: shoxlanishni qisqartirish, lekin yashirmaslik](#173-pattern-matching-shoxlanishni-qisqartirish-lekin-yashirmaslik)
  - [17.4 Virtual threadlar: diffdagi bitta qator, tizimdagi katta o'zgarish](#174-virtual-threadlar-diffdagi-bitta-qator-tizimdagi-katta-ozgarish)
  - [17.5 Text block va SQL](#175-text-block-va-sql)
  - [17.6 `var`: qachon o'qishni osonlashtiradi](#176-var-qachon-oqishni-osonlashtiradi)
  - [17.7 Yangi imkoniyatlarni qabul qilish siyosati](#177-yangi-imkoniyatlarni-qabul-qilish-siyosati)
  - [17.8 Amalda qo'llash](#178-amalda-qollash)

**[IV. Spring kodini review qilish](#iv-spring-kodini-review-qilish)**

- [18. Bean, kontekst va proxy mexanikasi review (Beans, Context and Proxies)](#18-bean-kontekst-va-proxy-mexanikasi-review-beans-context-and-proxies)
  - [18.1 Proxy ishlamaydigan to'rt holat](#181-proxy-ishlamaydigan-tort-holat)
  - [18.2 Bean scope va holat](#182-bean-scope-va-holat)
  - [18.3 Konfiguratsiya va bean e'lonlari](#183-konfiguratsiya-va-bean-elonlari)
  - [18.4 Inyeksiya shakllari](#184-inyeksiya-shakllari)
  - [18.5 Ishga tushish tartibi va `@PostConstruct`](#185-ishga-tushish-tartibi-va-postconstruct)
  - [18.6 Kontekst sozlamalari diffda](#186-kontekst-sozlamalari-diffda)
  - [18.7 Spring Boot avtokonfiguratsiyasi bilan kurash belgilari](#187-spring-boot-avtokonfiguratsiyasi-bilan-kurash-belgilari)
  - [18.8 Proxy va tranzaksiyani test bilan tekshirish](#188-proxy-va-tranzaksiyani-test-bilan-tekshirish)
  - [18.9 Review checklisti: Spring konteksti](#189-review-checklisti-spring-konteksti)
  - [18.10 Amalda qo'llash](#1810-amalda-qollash)
- [19. Tranzaksiya chegarasi review (Transaction Boundaries)](#19-tranzaksiya-chegarasi-review-transaction-boundaries)
  - [19.1 Chegara qayerda turishi kerak](#191-chegara-qayerda-turishi-kerak)
  - [19.2 Tranzaksiya ichida tashqi chaqiruv - eng xavfli naqsh](#192-tranzaksiya-ichida-tashqi-chaqiruv---eng-xavfli-naqsh)
  - [19.3 readOnly: nima beradi, nima bermaydi](#193-readonly-nima-beradi-nima-bermaydi)
  - [19.4 Propagation: diffdagi ma'nosi](#194-propagation-diffdagi-manosi)
  - [19.5 Rollback qoidalari](#195-rollback-qoidalari)
  - [19.6 Tranzaksiya uzunligi va PostgreSQL ga ta'siri](#196-tranzaksiya-uzunligi-va-postgresql-ga-tasiri)
  - [19.7 Commit dan keyin bajarilishi kerak bo'lgan ish](#197-commit-dan-keyin-bajarilishi-kerak-bolgan-ish)
  - [19.8 OSIV va lazy loading](#198-osiv-va-lazy-loading)
  - [19.9 Tranzaksiya, kesh, event va async aralashuvi](#199-tranzaksiya-kesh-event-va-async-aralashuvi)
  - [19.10 Review checklisti: tranzaksiyalar](#1910-review-checklisti-tranzaksiyalar)
  - [19.11 Amalda qo'llash](#1911-amalda-qollash)
- [20. Web qatlami review: DTO, validatsiya, xato javobi (The Web Layer)](#20-web-qatlami-review-dto-validatsiya-xato-javobi-the-web-layer)
  - [20.1 Tashqi shakl va ichki model chegarasi](#201-tashqi-shakl-va-ichki-model-chegarasi)
  - [20.2 Validatsiya: qayerda va qanchalik](#202-validatsiya-qayerda-va-qanchalik)
  - [20.3 Xato javobi: ichki detallar chiqmasligi](#203-xato-javobi-ichki-detallar-chiqmasligi)
  - [20.4 HTTP semantikasi](#204-http-semantikasi)
  - [20.5 Pagination va chegarasiz ro'yxatlar](#205-pagination-va-chegarasiz-royxatlar)
  - [20.6 Serializatsiya tuzoqlari](#206-serializatsiya-tuzoqlari)
  - [20.7 Fayl yuklash](#207-fayl-yuklash)
  - [20.8 So'rov chegaralari va rate limit](#208-sorov-chegaralari-va-rate-limit)
  - [20.9 Idempotentlik va qayta yuborish](#209-idempotentlik-va-qayta-yuborish)
  - [20.10 CORS, header va kesh sozlamalari](#2010-cors-header-va-kesh-sozlamalari)
  - [20.11 Review checklisti: web qatlami](#2011-review-checklisti-web-qatlami)
  - [20.12 Amalda qo'llash](#2012-amalda-qollash)
- [21. Konfiguratsiya, profil va feature flag review (Configuration)](#21-konfiguratsiya-profil-va-feature-flag-review-configuration)
  - [21.1 Konfiguratsiya o'zgarishi uchun qo'shimcha savollar](#211-konfiguratsiya-ozgarishi-uchun-qoshimcha-savollar)
  - [21.2 Timeout va retry juftligi](#212-timeout-va-retry-juftligi)
  - [21.3 Secret va maxfiy qiymatlar](#213-secret-va-maxfiy-qiymatlar)
  - [21.4 Profil bo'yicha xulq farqi](#214-profil-boyicha-xulq-farqi)
  - [21.5 Tipli konfiguratsiya](#215-tipli-konfiguratsiya)
  - [21.6 Feature flag: vaqtinchalik bo'lishi kerak](#216-feature-flag-vaqtinchalik-bolishi-kerak)
  - [21.7 Actuator va diagnostika endpointlari](#217-actuator-va-diagnostika-endpointlari)
  - [21.8 Muhitlar orasidagi farqni ko'rish](#218-muhitlar-orasidagi-farqni-korish)
  - [21.9 Review checklisti: konfiguratsiya](#219-review-checklisti-konfiguratsiya)
  - [21.10 Amalda qo'llash](#2110-amalda-qollash)
- [22. Tashqi integratsiya review: timeout, retry, broker (Outbound Integration)](#22-tashqi-integratsiya-review-timeout-retry-broker-outbound-integration)
  - [22.1 HTTP mijoz: timeout eng birinchi savol](#221-http-mijoz-timeout-eng-birinchi-savol)
  - [22.2 Retry: qachon zarar keltiradi](#222-retry-qachon-zarar-keltiradi)
  - [22.3 Circuit breaker va bulkhead](#223-circuit-breaker-va-bulkhead)
  - [22.4 WebClient va reaktiv kod aralashuvi](#224-webclient-va-reaktiv-kod-aralashuvi)
  - [22.5 Kafka va xabar brokerlari review](#225-kafka-va-xabar-brokerlari-review)
  - [22.6 Xabar sxemasi va moslik](#226-xabar-sxemasi-va-moslik)
  - [22.7 Tashqi ma'lumotga ishonmaslik](#227-tashqi-malumotga-ishonmaslik)
  - [22.8 Review checklisti: tashqi integratsiya](#228-review-checklisti-tashqi-integratsiya)
  - [22.9 Amalda qo'llash](#229-amalda-qollash)

**[V. PostgreSQL va ma'lumot qatlami review](#v-postgresql-va-malumot-qatlami-review)**

- [23. JPA va Hibernate review (JPA and Hibernate)](#23-jpa-va-hibernate-review-jpa-and-hibernate)
  - [23.1 N+1: diffdan ko'rish](#231-n1-diffdan-korish)
  - [23.2 So'rovlar sonini test bilan qulflash](#232-sorovlar-sonini-test-bilan-qulflash)
  - [23.3 Fetch strategiyasi](#233-fetch-strategiyasi)
  - [23.4 Cascade va orphan removal](#234-cascade-va-orphan-removal)
  - [23.5 Dirty checking va ortiqcha UPDATE](#235-dirty-checking-va-ortiqcha-update)
  - [23.6 Batch yozuv](#236-batch-yozuv)
  - [23.7 Projection: entity kerak bo'lmaganda](#237-projection-entity-kerak-bolmaganda)
  - [23.8 Hibernate xulqini o'zgartiradigan nozik annotatsiyalar](#238-hibernate-xulqini-ozgartiradigan-nozik-annotatsiyalar)
  - [23.9 Entity hayot sikli va detached holat](#239-entity-hayot-sikli-va-detached-holat)
  - [23.10 Review checklisti: JPA](#2310-review-checklisti-jpa)
  - [23.11 Amalda qo'llash](#2311-amalda-qollash)
- [24. SQL, so'rov rejasi va indeks review (SQL, Plans and Indexes)](#24-sql-sorov-rejasi-va-indeks-review-sql-plans-and-indexes)
  - [24.1 Indeks ishlatilmaydigan naqshlar](#241-indeks-ishlatilmaydigan-naqshlar)
  - [24.2 Yangi indeks qo'shilganda review savollari](#242-yangi-indeks-qoshilganda-review-savollari)
  - [24.3 So'rov rejasini o'qish: review uchun minimal bilim](#243-sorov-rejasini-oqish-review-uchun-minimal-bilim)
  - [24.4 JOIN va agregat so'rovlari](#244-join-va-agregat-sorovlari)
  - [24.5 Dinamik SQL review](#245-dinamik-sql-review)
  - [24.6 Katta jadvallar bilan ishlash](#246-katta-jadvallar-bilan-ishlash)
  - [24.7 JSONB review](#247-jsonb-review)
  - [24.8 Review paytida so'rovni o'lchash](#248-review-paytida-sorovni-olchash)
  - [24.9 Review checklisti: SQL va indekslar](#249-review-checklisti-sql-va-indekslar)
  - [24.10 Amalda qo'llash](#2410-amalda-qollash)
- [25. Migratsiya review: qulf, backfill, orqaga moslik (Reviewing Migrations)](#25-migratsiya-review-qulf-backfill-orqaga-moslik-reviewing-migrations)
  - [25.1 Birinchi savol: bu operatsiya qanday qulf oladi](#251-birinchi-savol-bu-operatsiya-qanday-qulf-oladi)
  - [25.2 Qulf kutish navbati: yashirin kaskad](#252-qulf-kutish-navbati-yashirin-kaskad)
  - [25.3 Orqaga moslik: deploy tartibi](#253-orqaga-moslik-deploy-tartibi)
  - [25.4 Backfill review](#254-backfill-review)
  - [25.5 Qaytarish rejasi](#255-qaytarish-rejasi)
  - [25.6 Migratsiya fayllarining o'zi](#256-migratsiya-fayllarining-ozi)
  - [25.7 Migratsiyani sinash](#257-migratsiyani-sinash)
  - [25.8 Review checklisti: migratsiya](#258-review-checklisti-migratsiya)
  - [25.9 Amalda qo'llash](#259-amalda-qollash)
- [26. Ma'lumot to'g'riligi va turlar review (Data Correctness)](#26-malumot-togriligi-va-turlar-review-data-correctness)
  - [26.1 Constraint - yagona ishonchli himoya](#261-constraint---yagona-ishonchli-himoya)
  - [26.2 Pul: tur, aniqlik, valyuta](#262-pul-tur-aniqlik-valyuta)
  - [26.3 Vaqt: zona, tur, tartib](#263-vaqt-zona-tur-tartib)
  - [26.4 Enum: baza va kod sinxronizatsiyasi](#264-enum-baza-va-kod-sinxronizatsiyasi)
  - [26.5 NULL semantikasi](#265-null-semantikasi)
  - [26.6 Tashqi kalitlar va o'chirish qoidalari](#266-tashqi-kalitlar-va-ochirish-qoidalari)
  - [26.7 Yumshoq o'chirish (soft delete)](#267-yumshoq-ochirish-soft-delete)
  - [26.8 Ma'lumot migratsiyasidagi to'g'rilik](#268-malumot-migratsiyasidagi-togrilik)
  - [26.9 Review checklisti: ma'lumot to'g'riligi](#269-review-checklisti-malumot-togriligi)
  - [26.10 Amalda qo'llash](#2610-amalda-qollash)
- [27. Izolyatsiya, poyga holatlari va xabar yetkazish (Isolation, Races and Delivery)](#27-izolyatsiya-poyga-holatlari-va-xabar-yetkazish-isolation-races-and-delivery)
  - [27.1 PostgreSQL izolyatsiya darajalari va diffdagi ma'nosi](#271-postgresql-izolyatsiya-darajalari-va-diffdagi-manosi)
  - [27.2 Poyga holatlarini topish usuli](#272-poyga-holatlarini-topish-usuli)
  - [27.3 Qulf turlari va ularning narxi](#273-qulf-turlari-va-ularning-narxi)
  - [27.4 Optimistik yoki pessimistik: tanlov mezoni](#274-optimistik-yoki-pessimistik-tanlov-mezoni)
  - [27.5 Write skew: eng jim poyga](#275-write-skew-eng-jim-poyga)
  - [27.6 SERIALIZABLE ishlatilganda](#276-serializable-ishlatilganda)
  - [27.7 Xabar yetkazish: "kamida bir marta" ning oqibatlari](#277-xabar-yetkazish-kamida-bir-marta-ning-oqibatlari)
  - [27.8 Xabarlar tartibi](#278-xabarlar-tartibi)
  - [27.9 Outbox worker review](#279-outbox-worker-review)
  - [27.10 Review checklisti: izolyatsiya va yetkazish](#2710-review-checklisti-izolyatsiya-va-yetkazish)
  - [27.11 Amalda qo'llash](#2711-amalda-qollash)

**[VI. Xavfsizlik review](#vi-xavfsizlik-review)**

- [28. Xavfsizlik review metodikasi (How to Review for Security)](#28-xavfsizlik-review-metodikasi-how-to-review-for-security)
  - [28.1 Asosiy savol: ishonilmaydigan ma'lumot qayerga boradi](#281-asosiy-savol-ishonilmaydigan-malumot-qayerga-boradi)
  - [28.2 Ishonch chegarasi diffda](#282-ishonch-chegarasi-diffda)
  - [28.3 Tez tekshirish ro'yxati: har PR uchun o'n savol](#283-tez-tekshirish-royxati-har-pr-uchun-on-savol)
  - [28.4 Zaiflik sinflarini tizimli ko'rish](#284-zaiflik-sinflarini-tizimli-korish)
  - [28.5 Xavfsizlik izohining shakli](#285-xavfsizlik-izohining-shakli)
  - [28.6 Xavfsizlik uchun avtomatlashtirish va uning chegarasi](#286-xavfsizlik-uchun-avtomatlashtirish-va-uning-chegarasi)
  - [28.7 Xavfsizlik review ni jarayonga kiritish](#287-xavfsizlik-review-ni-jarayonga-kiritish)
  - [28.8 Amalda qo'llash](#288-amalda-qollash)
- [29. Injection review: SQL va boshqalar (Injection)](#29-injection-review-sql-va-boshqalar-injection)
  - [29.1 Parametrlashtirish: nima parametr bo'la oladi](#291-parametrlashtirish-nima-parametr-bola-oladi)
  - [29.2 Spring Data da injection yo'llari](#292-spring-data-da-injection-yollari)
  - [29.3 JdbcTemplate va JdbcClient](#293-jdbctemplate-va-jdbcclient)
  - [29.4 Ikkilamchi injection (second-order)](#294-ikkilamchi-injection-second-order)
  - [29.5 SQL dan tashqari injection sinflari](#295-sql-dan-tashqari-injection-sinflari)
  - [29.6 Shablon va hisobot injectionlari](#296-shablon-va-hisobot-injectionlari)
  - [29.7 Review paytida injection ni qidirish](#297-review-paytida-injection-ni-qidirish)
  - [29.8 Himoyani test bilan qulflash](#298-himoyani-test-bilan-qulflash)
  - [29.9 Review checklisti: injection](#299-review-checklisti-injection)
  - [29.10 Amalda qo'llash](#2910-amalda-qollash)
- [30. Autentifikatsiya va avtorizatsiya review (Authentication and Authorization)](#30-autentifikatsiya-va-avtorizatsiya-review-authentication-and-authorization)
  - [30.1 IDOR: eng ko'p uchraydigan va eng oson o'tib ketadigan xato](#301-idor-eng-kop-uchraydigan-va-eng-oson-otib-ketadigan-xato)
  - [30.2 Foydalanuvchi identifikatori qayerdan keladi](#302-foydalanuvchi-identifikatori-qayerdan-keladi)
  - [30.3 Spring Security konfiguratsiyasi review](#303-spring-security-konfiguratsiyasi-review)
  - [30.4 Metod darajasidagi xavfsizlik](#304-metod-darajasidagi-xavfsizlik)
  - [30.5 Himoyasiz qolgan endpointlarni topish](#305-himoyasiz-qolgan-endpointlarni-topish)
  - [30.6 JWT va token review](#306-jwt-va-token-review)
  - [30.7 Ko'p tenantlik (multi-tenancy)](#307-kop-tenantlik-multi-tenancy)
  - [30.8 Biznes mantiqini chetlab o'tish](#308-biznes-mantiqini-chetlab-otish)
  - [30.9 Review checklisti: kirish nazorati](#309-review-checklisti-kirish-nazorati)
  - [30.10 Amalda qo'llash](#3010-amalda-qollash)
- [31. Kirish va chiqish xavfsizligi: SSRF, deserializatsiya, fayllar (Input and Output Safety)](#31-kirish-va-chiqish-xavfsizligi-ssrf-deserializatsiya-fayllar-input-and-output-safety)
  - [31.1 SSRF: URL ni kirishdan qurish](#311-ssrf-url-ni-kirishdan-qurish)
  - [31.2 Deserializatsiya](#312-deserializatsiya)
  - [31.3 Fayl yo'li va arxivlar](#313-fayl-yoli-va-arxivlar)
  - [31.4 Rasm va hujjat qayta ishlash](#314-rasm-va-hujjat-qayta-ishlash)
  - [31.5 Regex va DoS (ReDoS)](#315-regex-va-dos-redos)
  - [31.6 Resurs charchatish (DoS) yo'llari](#316-resurs-charchatish-dos-yollari)
  - [31.7 Review checklisti: kirish va chiqish](#317-review-checklisti-kirish-va-chiqish)
  - [31.8 Amalda qo'llash](#318-amalda-qollash)
- [32. Secret, maxfiy ma'lumot va kriptografiya review (Secrets, PII and Crypto)](#32-secret-maxfiy-malumot-va-kriptografiya-review-secrets-pii-and-crypto)
  - [32.1 Logga maxfiy ma'lumot tushishi](#321-logga-maxfiy-malumot-tushishi)
  - [32.2 PII va ma'lumot minimizatsiyasi](#322-pii-va-malumot-minimizatsiyasi)
  - [32.3 Parol va token saqlash](#323-parol-va-token-saqlash)
  - [32.4 Tasodifiylik](#324-tasodifiylik)
  - [32.5 Shifrlash](#325-shifrlash)
  - [32.6 Taqqoslash va vaqt hujumlari](#326-taqqoslash-va-vaqt-hujumlari)
  - [32.7 TLS va sertifikatlar](#327-tls-va-sertifikatlar)
  - [32.8 Review checklisti: secret va kriptografiya](#328-review-checklisti-secret-va-kriptografiya)
  - [32.9 Amalda qo'llash](#329-amalda-qollash)
- [33. Bog'liqlik va supply chain review (Dependencies and Supply Chain)](#33-bogliqlik-va-supply-chain-review-dependencies-and-supply-chain)
  - [33.1 Yangi bog'liqlik uchun savollar](#331-yangi-bogliqlik-uchun-savollar)
  - [33.2 Transitive bog'liqliklar va versiya konflikti](#332-transitive-bogliqliklar-va-versiya-konflikti)
  - [33.3 Skanerlashni CI ga qo'yish](#333-skanerlashni-ci-ga-qoyish)
  - [33.4 Versiya yangilash PR larini review qilish](#334-versiya-yangilash-pr-larini-review-qilish)
  - [33.5 Build va CI ning o'zi](#335-build-va-ci-ning-ozi)
  - [33.6 Review checklisti: bog'liqliklar](#336-review-checklisti-bogliqliklar)
  - [33.7 Amalda qo'llash](#337-amalda-qollash)

**[VII. Test review](#vii-test-review)**

- [34. Test to'liqligini review qilish (Test Case Completeness)](#34-test-toliqligini-review-qilish-test-case-completeness)
  - [34.1 To'g'ri savol: qaysi holat qamralmagan](#341-togri-savol-qaysi-holat-qamralmagan)
  - [34.2 Chegaraviy qiymatlar: eng ko'p qaytim beradigan test holatlari](#342-chegaraviy-qiymatlar-eng-kop-qaytim-beradigan-test-holatlari)
  - [34.3 Shartlar kombinatsiyasi: qaror jadvali](#343-shartlar-kombinatsiyasi-qaror-jadvali)
  - [34.4 Holat o'tish matritsasi](#344-holat-otish-matritsasi)
  - [34.5 Xato yo'llari: eng ko'p qamralmay qoladigan qism](#345-xato-yollari-eng-kop-qamralmay-qoladigan-qism)
  - [34.6 Konkurentlik va idempotentlik testlari](#346-konkurentlik-va-idempotentlik-testlari)
  - [34.7 Mutatsion fikrlash: testni aldab o'tish mumkinmi](#347-mutatsion-fikrlash-testni-aldab-otish-mumkinmi)
  - [34.8 Ma'lumotga bog'liq holatlar](#348-malumotga-bogliq-holatlar)
  - [34.9 Yetishmayotgan holatni review izohida ko'rsatish](#349-yetishmayotgan-holatni-review-izohida-korsatish)
  - [34.10 Review checklisti: test to'liqligi](#3410-review-checklisti-test-toliqligi)
  - [34.11 Amalda qo'llash](#3411-amalda-qollash)
- [35. Test sifati review: assertion, izolyatsiya, beqarorlik (Test Quality)](#35-test-sifati-review-assertion-izolyatsiya-beqarorlik-test-quality)
  - [35.1 Assertion sifati](#351-assertion-sifati)
  - [35.2 Mock ni haddan ortiq ishlatish](#352-mock-ni-haddan-ortiq-ishlatish)
  - [35.3 Beqaror (flaky) testlar](#353-beqaror-flaky-testlar)
  - [35.4 Test izolyatsiyasi](#354-test-izolyatsiyasi)
  - [35.5 Test nomlari va diagnostika](#355-test-nomlari-va-diagnostika)
  - [35.6 Test ma'lumotini qurish](#356-test-malumotini-qurish)
  - [35.7 Testlardagi anti-naqshlar](#357-testlardagi-anti-naqshlar)
  - [35.8 Test ijro vaqti](#358-test-ijro-vaqti)
  - [35.9 Review checklisti: test sifati](#359-review-checklisti-test-sifati)
  - [35.10 Amalda qo'llash](#3510-amalda-qollash)
- [36. Test turi va integratsion test review (Test Types and Integration Tests)](#36-test-turi-va-integratsion-test-review-test-types-and-integration-tests)
  - [36.1 Daraja tanlash mezoni](#361-daraja-tanlash-mezoni)
  - [36.2 H2 va haqiqiy PostgreSQL](#362-h2-va-haqiqiy-postgresql)
  - [36.3 Spring test slice larini to'g'ri ishlatish](#363-spring-test-slice-larini-togri-ishlatish)
  - [36.4 Tashqi servislarni sinash](#364-tashqi-servislarni-sinash)
  - [36.5 Kontrakt testlari](#365-kontrakt-testlari)
  - [36.6 Migratsiya va sxema testlari](#366-migratsiya-va-sxema-testlari)
  - [36.7 Testlar nimani qoplamasligi kerak](#367-testlar-nimani-qoplamasligi-kerak)
  - [36.8 Review checklisti: test turlari](#368-review-checklisti-test-turlari)
  - [36.9 Amalda qo'llash](#369-amalda-qollash)

**[VIII. Kesishgan sifat](#viii-kesishgan-sifat)**

- [37. API moslik va breaking change review (API Compatibility)](#37-api-moslik-va-breaking-change-review-api-compatibility)
  - [37.1 Breaking change katalogi](#371-breaking-change-katalogi)
  - [37.2 Kim ishlatayotganini aniqlash](#372-kim-ishlatayotganini-aniqlash)
  - [37.3 Versiyalash strategiyalari](#373-versiyalash-strategiyalari)
  - [37.4 Deserializatsiya qattiqligi](#374-deserializatsiya-qattiqligi)
  - [37.5 Ichki API: modullar orasidagi shartnoma](#375-ichki-api-modullar-orasidagi-shartnoma)
  - [37.6 Event va xabar sxemasi](#376-event-va-xabar-sxemasi)
  - [37.7 Deprecation jarayoni](#377-deprecation-jarayoni)
  - [37.8 Review checklisti: API moslik](#378-review-checklisti-api-moslik)
  - [37.9 Amalda qo'llash](#379-amalda-qollash)
- [38. Performance review diffdan (Performance from a Diff)](#38-performance-review-diffdan-performance-from-a-diff)
  - [38.1 Asosiy usul: operatsiyalarni sanash](#381-asosiy-usul-operatsiyalarni-sanash)
  - [38.2 Siklda I/O: eng ko'p uchraydigan muammo](#382-siklda-io-eng-kop-uchraydigan-muammo)
  - [38.3 Hajm: nima tashiladi](#383-hajm-nima-tashiladi)
  - [38.4 Kesh: qachon foyda, qachon zarar](#384-kesh-qachon-foyda-qachon-zarar)
  - [38.5 Performance regressiyasini diffdan ko'rish](#385-performance-regressiyasini-diffdan-korish)
  - [38.6 O'lchovsiz optimallashtirishni rad etish](#386-olchovsiz-optimallashtirishni-rad-etish)
  - [38.7 Review paytida o'lchash](#387-review-paytida-olchash)
  - [38.8 Performance byudjeti](#388-performance-byudjeti)
  - [38.9 Review checklisti: performance](#389-review-checklisti-performance)
  - [38.10 Amalda qo'llash](#3810-amalda-qollash)
- [39. Observability review (Observability)](#39-observability-review-observability)
  - [39.1 Uch signal va ularning vazifasi](#391-uch-signal-va-ularning-vazifasi)
  - [39.2 Yangi kod uchun minimal signal to'plami](#392-yangi-kod-uchun-minimal-signal-toplami)
  - [39.3 Nimani o'lchash kerak: RED va USE](#393-nimani-olchash-kerak-red-va-use)
  - [39.4 Log sifati](#394-log-sifati)
  - [39.5 Korrelyatsiya va trace](#395-korrelyatsiya-va-trace)
  - [39.6 Health check va probe lar](#396-health-check-va-probe-lar)
  - [39.7 Alert sifati](#397-alert-sifati)
  - [39.8 Review checklisti: observability](#398-review-checklisti-observability)
  - [39.9 Amalda qo'llash](#399-amalda-qollash)

**[IX. Jarayon, madaniyat va o'lchov](#ix-jarayon-madaniyat-va-olchov)**

- [40. Review jarayonini qurish (Building the Process)](#40-review-jarayonini-qurish-building-the-process)
  - [40.1 Kim review qiladi: CODEOWNERS](#401-kim-review-qiladi-codeowners)
  - [40.2 Xavf bo'yicha tabaqalash](#402-xavf-boyicha-tabaqalash)
  - [40.3 SLA va navbat](#403-sla-va-navbat)
  - [40.4 PR shabloni](#404-pr-shabloni)
  - [40.5 Draft va bosqichli review](#405-draft-va-bosqichli-review)
  - [40.6 Avtomatik tekshiruvlar tartibi](#406-avtomatik-tekshiruvlar-tartibi)
  - [40.7 Merge strategiyasi va review](#407-merge-strategiyasi-va-review)
  - [40.8 Review ni o'tkazib yuborish mumkin bo'lgan holatlar](#408-review-ni-otkazib-yuborish-mumkin-bolgan-holatlar)
  - [40.9 Review checklisti: jarayon](#409-review-checklisti-jarayon)
  - [40.10 Amalda qo'llash](#4010-amalda-qollash)
- [41. Review madaniyati, til va kelishmovchilik (Culture, Language, Disagreement)](#41-review-madaniyati-til-va-kelishmovchilik-culture-language-disagreement)
  - [41.1 Izoh tili: kodga qarash, odamga emas](#411-izoh-tili-kodga-qarash-odamga-emas)
  - [41.2 Savol shaklida izoh](#412-savol-shaklida-izoh)
  - [41.3 Izoh darajasini ajratish](#413-izoh-darajasini-ajratish)
  - [41.4 Junior va senior bilan review](#414-junior-va-senior-bilan-review)
  - [41.5 Kelishmovchilikni hal qilish](#415-kelishmovchilikni-hal-qilish)
  - [41.6 Review izohining narxi](#416-review-izohining-narxi)
  - [41.7 Masofaviy va asinxron review](#417-masofaviy-va-asinxron-review)
  - [41.8 Review ni o'rgatish](#418-review-ni-orgatish)
  - [41.9 Review madaniyatining buzilish belgilari](#419-review-madaniyatining-buzilish-belgilari)
  - [41.10 Amalda qo'llash](#4110-amalda-qollash)
- [42. Review metrikalari (Measuring Review)](#42-review-metrikalari-measuring-review)
  - [42.1 Foydali metrikalar](#421-foydali-metrikalar)
  - [42.2 Zararli metrikalar](#422-zararli-metrikalar)
  - [42.3 Metrikalarni yig'ish](#423-metrikalarni-yigish)
  - [42.4 Izohlarni sinflash](#424-izohlarni-sinflash)
  - [42.5 Review samaradorligini o'lchash](#425-review-samaradorligini-olchash)
  - [42.6 DORA metrikalari bilan bog'liqlik](#426-dora-metrikalari-bilan-bogliqlik)
  - [42.7 Metrikalarni o'qish: tuzoqlar](#427-metrikalarni-oqish-tuzoqlar)
  - [42.8 Amalda qo'llash](#428-amalda-qollash)
- [43. AI yozgan kodni review qilish va AI bilan review qilish (Reviewing AI-Generated Code)](#43-ai-yozgan-kodni-review-qilish-va-ai-bilan-review-qilish-reviewing-ai-generated-code)
  - [43.1 AI yozgan kodning xato profili](#431-ai-yozgan-kodning-xato-profili)
  - [43.2 Eng xavfli naqsh: ishonchli ko'rinadigan noto'g'ri kod](#432-eng-xavfli-naqsh-ishonchli-korinadigan-notogri-kod)
  - [43.3 AI yozgan kod uchun qo'shimcha review savollari](#433-ai-yozgan-kod-uchun-qoshimcha-review-savollari)
  - [43.4 Kontekst bermaslikning oqibati](#434-kontekst-bermaslikning-oqibati)
  - [43.5 AI ni review da ishlatish](#435-ai-ni-review-da-ishlatish)
  - [43.6 AI review ni sozlash](#436-ai-review-ni-sozlash)
  - [43.7 Muallif mas'uliyati o'zgarmaydi](#437-muallif-masuliyati-ozgarmaydi)
  - [43.8 Review checklisti: AI yozgan kod](#438-review-checklisti-ai-yozgan-kod)
  - [43.9 Amalda qo'llash](#439-amalda-qollash)
- [44. Shablonlar, checklistlar va reviewer yetukligi (Templates and Maturity)](#44-shablonlar-checklistlar-va-reviewer-yetukligi-templates-and-maturity)
  - [44.1 Universal review o'tishi: 15 daqiqalik ro'yxat](#441-universal-review-otishi-15-daqiqalik-royxat)
  - [44.2 Yuqori xavfli PR uchun qo'shimcha o'tish](#442-yuqori-xavfli-pr-uchun-qoshimcha-otish)
  - [44.3 Review izohlari uchun tayyor iboralar](#443-review-izohlari-uchun-tayyor-iboralar)
  - [44.4 Review xulosasi shablonlari](#444-review-xulosasi-shablonlari)
  - [44.5 Reviewer yetukligi darajalari](#445-reviewer-yetukligi-darajalari)
  - [44.6 O'zini tekshirish savollari](#446-ozini-tekshirish-savollari)
  - [44.7 Loyihada review ni yo'lga qo'yishning birinchi 30 kuni](#447-loyihada-review-ni-yolga-qoyishning-birinchi-30-kuni)
  - [44.8 Hujjatni qanday ishlatish](#448-hujjatni-qanday-ishlatish)
  - [44.9 Amalda qo'llash](#449-amalda-qollash)

# I. Review ning mohiyati va iqtisodi

## 1. Review nima uchun bor va nimani haqiqatda beradi (Why Review Exists)

Review haqidagi eng keng tarqalgan xato - uni xato topish mashinasi deb o'ylash. Agar maqsad faqat xato topish bo'lsa, review raqamlar bilan taqqoslaganda qimmat usul: bir soat odam vaqti ketadi va xatolarning yarmidan ko'pi o'tib ketadi. Review o'z narxini boshqa narsa bilan qoplaydi: u kod ustidan egalikni tarqatadi, qarorni ikkinchi miya bilan tekshiradi va jamoaga umumiy did beradi. Shu sababli review maqsadini aniq yozmagan jamoada u tez orada marosimga aylanadi: "LGTM" bosiladi, vaqt ketadi, foyda ko'rinmaydi.

### 1.1 Review ning uchta haqiqiy mahsuloti

Birinchi mahsulot - topilgan xato. Bu eng ko'rinadigan, lekin eng kichik qismi. Modern code review bo'yicha o'tkazilgan kuzatuvlarda review izohlarining katta qismi (taxminan uchdan ikki qismi va undan ko'pi) funksional xato haqida emas, o'qiluvchanlik, nomlash, tuzilish va mavjud kod bilan moslik haqida bo'ladi. Ya'ni review amalda ko'proq maintainability filtri.

Ikkinchi mahsulot - tarqalgan bilim. PR ni ikkinchi odam o'qiganida kod ustida kamida ikki kishi biladigan holat yuzaga keladi. Bitta modulni faqat bitta odam biladigan loyihada u odam ta'tilga chiqsa, o'zgarish tezligi nolga tushadi. Review shu xavfni arzon narxda kamaytiradi.

Uchinchi mahsulot - tekshirilgan qaror. Kodda ko'rinmaydigan qaror ham bor: nega shu yerga kesh qo'yildi, nega bu jadvalga yangi ustun qo'shildi, nega retry 3 marta. Review shu qarorni ovoz chiqarib aytishga majbur qiladi. Ko'p hollarda muallif izohga javob yozayotganda o'zi xatoni topadi.

| Mahsulot | Qanday ko'rinadi | O'lchash usuli | Yo'qolsa nima bo'ladi |
| --- | --- | --- | --- |
| Topilgan xato | Blocker izoh, keyin tuzatish | Review da topilgan va prodda topilgan xato nisbati | Xato prodga chiqadi, narxi 10-100 barobar oshadi |
| Tarqalgan bilim | Savol-javob, "bu nega shunday" | Modul bo'yicha bilimli odam soni | Bitta odamga bog'liqlik, ta'til xavfi |
| Tekshirilgan qaror | Alternativa muhokamasi, ADR havolasi | Qaror yozuvlari soni | Qaror yozilmaydi, olti oydan keyin hech kim sababini bilmaydi |
| Umumiy did | Bir xil uslub, takrorlanmaydigan izoh | Bir xil izohning takrorlanish soni | Har fayl boshqa qo'l bilan yozilgan kodga o'xshaydi |
| Egalik hissi | Reviewer ham javobgar | Incidentda kim keladi | "Mening kodim emas" madaniyati |

### 1.2 Review nimani topmaydi

Reviewer diffni o'qiydi, tizimni ishlatmaydi. Shu bitta jumla review ning chegarasini belgilaydi. Diffdan ko'rinmaydigan narsalar: real yuk ostidagi xulq, ma'lumotlar bazasidagi haqiqiy taqsimot, ishlab turgan tizimdagi konfiguratsiya, boshqa servisning javob vaqti, migratsiyaning real jadvalda qancha turishi.

Statistik kuzatuvlar klassik formal inspeksiyada xato topish darajasi taxminan 50-70 foiz atrofida ekanini ko'rsatadi, zamonaviy yengil PR review da esa bundan past. Ya'ni har uchta xatodan kamida bittasi review dan o'tadi. Shundan kelib chiqadigan amaliy xulosa: review ni oxirgi himoya chizig'i deb hisoblash xato. U ko'p qatlamli filtrning bir qatlami.

Yana bir chegara: reviewer muallifning taxminlarini meros qilib oladi. Agar muallif talabni noto'g'ri tushungan bo'lsa, kod shu noto'g'ri tushunishga mos holda toza yozilgan bo'ladi va review hech narsa sezmaydi. Shu sababli talabni tushunish review da emas, undan oldin tekshiriladi.

### 1.3 Filtrlarning mehnat taqsimoti

Har bir filtr boshqa sinf xatoni tutadi. Filtrlarni bir-birining o'rniga qo'ymaslik kerak.

| Filtr | Yaxshi tutadi | Tutmaydi | Narxi |
| --- | --- | --- | --- |
| Kompilyator va tur tizimi | Tur xatosi, yo'q metod | Mantiq xatosi | Nol |
| Linter va formatter | Uslub, oddiy shablon xato | Dizayn, kontekst | Juda arzon |
| Statik tahlil | Null yo'li, resurs oqishi, ma'lum shablonlar | Biznes mantiqi | Arzon, lekin shovqin beradi |
| Unit test | Mantiq va chegaraviy holat | Integratsiya, konfiguratsiya | O'rtacha |
| Integratsion test | Sxema, tranzaksiya, mapping | Yuk ostidagi xulq | Qimmat |
| Kod review | Niyat, dizayn, yo'q kod, xavf | Yuk, real ma'lumot | Qimmat odam vaqti |
| Canary va prod monitoring | Real xulq, real taqsimot | Hech narsa oldini olmaydi, faqat aytadi | Eng qimmat |

Shu jadvaldan asosiy qoida chiqadi: review da arzon filtr tutadigan narsani qo'lda tekshirish - vaqtni yoqish. Agar PR da formatlash haqida izoh yozilayotgan bo'lsa, demak formatter sozlanmagan. Reviewer ning vaqti faqat mashina tuta olmaydigan narsaga sarflanishi kerak: niyat, dizayn, xavf va kontekst.

### 1.4 Approve nimani anglatadi va nimani anglatmaydi

Approve - "men bu kodni o'qidim, tushundim va shu holda prodga chiqishiga qarshi emasman" degani. U "kodda xato yo'q" degani emas, chunki bunday kafolatni hech kim bera olmaydi. Jamoada shu farq kelishib olinmasa, incidentdan keyin "sen approve qilgansan" degan ayblov paydo bo'ladi.

Amalda foydali shakl: approve uch darajada bo'ladi. Birinchi daraja - "o'qidim, dizayn to'g'ri, detallarni tekshirmadim". Ikkinchi daraja - "satr-satr o'qidim, chegaraviy holatlarni ko'rdim". Uchinchi daraja - "lokalda ishga tushirdim, migratsiyani sinab ko'rdim". Yuqori xavfli PR uchun uchinchi daraja talab qilinadi, oddiy PR uchun birinchi yetarli. Darajani izohda bitta jumla bilan yozish reviewer ni ham, muallifni ham himoya qiladi.

```text
# Review xulosasi uchun shablon: nimani tekshirdim, nimani tekshirmadim.

Approve (daraja 2).
Tekshirdim: tranzaksiya chegarasi, null yo'llari, yangi indeks tanlovi,
            xato javobining shakli.
Tekshirmadim: migratsiyani real hajmdagi ma'lumotda ishga tushirmadim.
Xavf: backfill 12 mln qatorga tegadi, staging da vaqtini o'lchab ko'rishni
      so'raymiz. Qolgan qismiga qarshilik yo'q.
```

### 1.5 Review mas'uliyatni ko'chirmaydi

Review dan keyin ham kod muallifning kodi bo'lib qoladi. Bu nazariy gap emas, operatsion qoida: alert kelganda birinchi chaqiriladigan odam - o'zgarishni kiritgan odam. Agar jamoa "review o'tgandan keyin bu jamoaning kodi" qoidasini qabul qilsa, egalik yo'qoladi va sifat tushadi.

Teskari tomoni ham bor: reviewer "men faqat ko'rib qo'ydim" deb o'zini chetga ola olmaydi. To'g'ri muvozanat shunday: muallif to'g'riligi uchun javob beradi, reviewer o'zi ko'rgan va o'tkazib yuborgan narsa uchun javob beradi. Incident tahlilida ikkinchi savol har doim beriladi: nega review bu xatoni ko'rmadi, va checklistga nima qo'shiladi.

### 1.6 Review ning yon ta'siri: PR hajmini kichraytirishga majbur qilish

Review jarayoni mavjud bo'lgan jamoada PR lar o'z-o'zidan kichikroq bo'ladi, chunki katta PR uzoq kutadi. Bu review ning eng kam gapiriladigan foydasi: u o'zgarishni mayda bo'laklarga bo'lishga iqtisodiy sabab yaratadi. Mayda o'zgarish esa osonroq qaytariladi, osonroq test qilinadi va incidentda tezroq topiladi.

Shu sababli review vaqtini qisqartirish uchun qoidani "katta PR ni tezroq o'qing" emas, "katta PR ni bo'lib yuboring" deb qo'yish kerak. Birinchi variant reviewer ni charchatadi, ikkinchisi tizimni yaxshilaydi.

### 1.7 Qachon review foyda bermaydi

Uch holat bor. Birinchi - mashina generatsiya qilgan kod: OpenAPI dan chiqqan client, protobuf stublar, jOOQ klasslari. Ularni o'qish vaqtni yoqish, chunki ular o'zgarmaydi va qo'lda tuzatilmaydi. Review generatsiya sozlamasiga qaratiladi, chiqqan kodga emas.

Ikkinchi - formatlash va avtomatik refactoring: IDE butun paketdagi importlarni tartiblagan PR. Bunday diffni odam o'qiy olmaydi. Qoida: formatlash o'zgarishi alohida commit va alohida PR bo'ladi, va `.git-blame-ignore-revs` ga qo'shiladi.

Uchinchi - vendor va uchinchi tomon kodi repoga ko'chirilgan holat. Uni review qilish emas, bog'liqlik sifatida boshqarish kerak.

```bash
# Generated va vendor kodni review va blame dan chiqarib tashlash.
# 1) Diffda ko'rinmasin: GitHub linguist generated deb belgilaydi.
cat > .gitattributes <<'EOA'
src/main/generated/**      linguist-generated=true
**/*.pb.go                 linguist-generated=true
src/main/java/**/jooq/**   linguist-generated=true
EOA

# 2) Formatlash commitlari blame ni buzmasin.
git log --oneline --grep='^style: ' --format='%H' > .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs

# 3) Statik tahlil ham tegmasin: shovqin review vaqtini yeydi.
#    sonar-project.properties da:
#    sonar.exclusions=src/main/generated/**,**/jooq/**
```

### 1.8 Review arxitektura qaroridan keyin keladi

PR - arxitektura muhokamasi uchun eng yomon joy. Diff ochilganida qaror allaqachon qabul qilingan, kod yozilgan, muallif unga bir hafta sarflagan. Shu nuqtada "bu yondashuv noto'g'ri" deyish ikki tomon uchun ham qimmat.

Shu sababli yetuk jamoada katta o'zgarish ikki bosqichda ko'riladi: avval bir sahifali dizayn eskizi yoki ADR qoralamasi, keyin kod. Birinchi bosqichda qarorni o'zgartirish narxi nolga yaqin. Agar PR da arxitektura darajasidagi e'tiroz paydo bo'lsa, bu ko'pincha jarayon xatosi: dizayn muhokamasi o'tkazib yuborilgan.

Amaliy chegara: diffda 5 tadan ko'p yangi fayl yoki yangi tashqi bog'liqlik yoki yangi jadval paydo bo'lsa, bu PR dizayn muhokamasini talab qilgan o'zgarish. Review izohida shuni aytish o'rinli: keyingi marta eskizdan boshlaymiz.

### 1.9 Review maqsadini jamoada yozib qo'yish

Yozilmagan maqsad har kimda boshqacha bo'ladi. Natijada bir reviewer nomlash haqida uch izoh yozadi, boshqasi tranzaksiya chegarasini ko'rmaydi. Review siyosati repoda `REVIEW.md` sifatida turishi kerak va u uzun bo'lmasligi lozim: bir sahifa yetadi.

```markdown
<!-- REVIEW.md: jamoaning review shartnomasi. Bir sahifa, ko'p emas. -->
# Review shartnomasi

## Maqsad
1. Prodga chiqadigan xavfni kamaytirish.
2. Kod ustidan egalikni ikki kishiga tarqatish.
3. Qarorni yozib qoldirish.

## Reviewer vaqtini nimaga sarflaymiz
Niyat, dizayn, yo'q kod, xavf, ma'lumot to'g'riligi, orqaga moslik.

## Nimaga sarflamaymiz
Formatlash (spotless), import tartibi, uslub (checkstyle), generated kod.

## Izoh darajalari
- `blocker:` tuzatilmasa merge bo'lmaydi.
- `suggest:` yaxshilanish, muallif qaroriga qoldiriladi.
- `nit:` did, majburiy emas.
- `question:` javob kerak, tuzatish shart emas.

## SLA
Birinchi javob: 4 ish soati. Yuqori xavfli PR: ikki reviewer.

## Xavfli o'zgarishlar ro'yxati
Migratsiya, autentifikatsiya, to'lov, tashqi API shakli, pul va vaqt hisobi.
```

### 1.10 Review madaniyatini o'lchash uchun uchta savol

Birinchi savol: oxirgi oyda review da topilgan va prodga o'tib ketgan xatolar nisbati qanday. Ikkinchi savol: PR ning birinchi javobni kutish vaqti qancha. Uchinchi savol: izohlarning qanchasi mashina tuta oladigan narsa haqida. Uchinchi raqam yuqori bo'lsa, muammo odamda emas, instrumentda.

Bu uch raqam review ni did muhokamasidan muhandislik mavzusiga olib chiqadi. Keyingi bob shu iqtisodni raqamlarda ko'rsatadi.

### 1.11 Amalda qo'llash

- [ ] Jamoa bilan bir sahifali `REVIEW.md` yozing: maqsad, izoh darajalari, SLA va xavfli o'zgarishlar ro'yxati.
- [ ] Oxirgi 50 ta PR izohini uch sinfga ajratib sanang: xato, maintainability, mashina tuta oladigan narsa. Uchinchi sinf 20 foizdan ko'p bo'lsa, linter va formatter sozlamasini tuzating.
- [ ] `spotless` yoki `google-java-format` ni CI ga qo'ying, shundan keyin formatlash haqidagi izohni taqiqlang.
- [ ] `.gitattributes` da generated kodni `linguist-generated=true` qilib belgilang va statik tahlildan chiqaring.
- [ ] Formatlash commitlarini `.git-blame-ignore-revs` ga qo'shib, `blame.ignoreRevsFile` ni sozlang.
- [ ] Approve uchun uch darajali shablonni joriy qiling va yuqori xavfli PR uchun 3-darajani majburiy qilib qo'ying.
- [ ] Oxirgi uchta incidentni olib, har biri uchun "review nega ko'rmadi" savoliga javob yozing va checklistga bitta band qo'shing.
- [ ] Katta o'zgarishlar uchun dizayn eskizi bosqichini joriy qiling: 5 dan ko'p yangi fayl yoki yangi jadval bo'lsa, avval bir sahifa.

## 2. Review iqtisodi: xato narxi, navbat va PR hajmi (The Economics of Review)

Review vaqt yeydi, va shu vaqt eng qimmat odamlarning vaqti. Shu sababli review ni iqtisodiy hodisa sifatida ko'rish kerak: nimaga qancha sarflanadi va qancha qaytadi. Bu bobda to'rtta raqam hisoblanadi: xatoning bosqichga qarab narxi, review ning optimal hajmi, navbat vaqti va reviewer sonining qaytimi.

### 2.1 Xato narxi bosqich bo'yicha o'sadi

Xatoni topish narxi u qancha uzoq yashagan bo'lsa, shuncha yuqori. Sabablari mexanik: kontekst yo'qoladi, xato boshqa kodga tarqaladi, ma'lumot buziladi, va tuzatish uchun relizdan tashqari yo'l kerak bo'ladi.

| Qayerda topilgan | Tuzatish ishi | Qo'shimcha narx | Nisbiy narx |
| --- | --- | --- | --- |
| IDE da yozilayotganda | Bir daqiqa | Yo'q | 1 |
| Lokal testda | Bir necha daqiqa | Yo'q | 2-3 |
| Review da | 15-60 daqiqa | Ikkinchi odam vaqti, kontekstga qaytish | 5-10 |
| CI da | 10-30 daqiqa | Pipeline vaqti, navbat | 5-10 |
| Staging da | Yarim kun | Qayta deploy, test ma'lumoti | 15-30 |
| Prodda, ta'sirsiz | Bir kun | Hotfix, reliz tartibi | 30-60 |
| Prodda, ma'lumot buzilgan | Bir hafta va ko'proq | Incident, backfill, ishonch yo'qolishi | 100 va yuqori |

Oxirgi qatorga alohida e'tibor kerak. Ma'lumot buzilishi boshqa barcha xato turidan farq qiladi: kodni qaytarsangiz, xato yo'qoladi, lekin buzilgan ma'lumot joyida qoladi. Shu sababli review da ma'lumotga yozadigan kod boshqa kodga nisbatan ko'proq vaqtga arziydi. Bu hujjatning V bo'limi aynan shu sababli eng batafsil.

### 2.2 PR hajmi va topish darajasi

Reviewer ning diqqati chiziqli emas. Kichik diffda har satr ko'riladi, katta diffda ko'z yuguradi. Kuzatuvlar bir o'tirishda taxminan 200-400 o'zgargan satr atrofida samaradorlik yuqori bo'lishini, undan keyin esa topish darajasi keskin tushishini ko'rsatadi. Sababi fiziologik: diqqat 60-90 daqiqadan keyin pasayadi.

| PR hajmi (o'zgargan satr) | Reviewer xulqi | Topish darajasi | Amaliy xulosa |
| --- | --- | --- | --- |
| 1-50 | Har satrni o'qiydi, kontekstni tekshiradi | Yuqori | Ideal hajm |
| 50-200 | O'qiydi, ba'zi joylarni tezlashtiradi | Yuqori | Normal hajm |
| 200-400 | Muhim joylarni tanlab o'qiydi | O'rtacha | Chegara |
| 400-1000 | Diagonal o'qiydi, dizaynga qaraydi | Past | Bo'lish kerak |
| 1000+ | "LGTM" | Nolga yaqin | Review emas, marosim |

Shu jadvaldan bitta qattiq qoida chiqadi: 400 satrdan katta PR ni review qilish o'zini aldash. Agar bo'lish imkoni bo'lmasa (masalan, katta migratsiya yoki framework yangilanishi), review usuli o'zgaradi: satrlarni o'qish o'rniga xavf nuqtalari ro'yxati bo'yicha yuriladi va qolgani avtomatik tekshiruvga ishonib topshiriladi. Bu holat ham izohda ochiq yozilishi kerak.

```bash
# PR hajmini o'lchash va generated/test fayllarni ajratish.
# Reviewer uchun haqiqiy yuk - qo'lda yozilgan mantiq satrlari.
BASE=origin/main
git diff --numstat $BASE...HEAD | awk '
  $3 ~ /\/generated\/|\.lock$|package-lock|\.svg$/ { gen += $1 + $2; next }
  $3 ~ /[Tt]est/                                   { tst += $1 + $2; next }
  $3 ~ /\.(md|txt|properties|ya?ml)$/              { cfg += $1 + $2; next }
                                                   { src += $1 + $2 }
  END {
    printf "mantiq:    %5d satr\n", src
    printf "test:      %5d satr\n", tst
    printf "konfig:    %5d satr\n", cfg
    printf "generated: %5d satr (tekshirilmaydi)\n", gen
    if (src > 400) print "OGOHLANTIRISH: mantiq qismi 400 satrdan katta, PR ni ajratish kerak"
  }'

# Fayl bo'yicha eng katta o'zgarishlar: review ni shulardan boshlash kerak.
git diff --numstat $BASE...HEAD | sort -rn | head -10
```

### 2.3 Navbat nazariyasi: kutish vaqti review ning asosiy narxi

Review ning haqiqiy narxi reviewer sarflagan 30 daqiqa emas. Asosiy narx - PR ning navbatda turgan vaqti. Kutayotgan PR muallifni boshqa ishga o'tishga majbur qiladi, keyin kontekstni qaytadan tiklashga majbur qiladi, va ayni paytda base branch dan uzoqlashib boradi.

Little qonuni bu yerda ham ishlaydi: tizimda kutayotgan ishlar soni = kelish tezligi x o'rtacha o'tish vaqti. Agar jamoa kuniga 10 PR ochsa va o'rtacha o'tish vaqti 2 kun bo'lsa, har doim taxminan 20 ta ochiq PR turadi. Yigirma ochiq PR esa konfliktlar, eskirgan branchlar va qayta ishlash degani.

| Birinchi javobni kutish | Muallif xulqi | Tizim oqibati |
| --- | --- | --- |
| 1 soatdan kam | Kontekstda qoladi, darhol tuzatadi | Eng tez oqim, eng kam rework |
| 4 soatgacha | O'sha kuni tugatadi | Normal |
| 1 kun | Boshqa ishga o'tadi, kontekstni yo'qotadi | Rework o'sadi |
| 2-3 kun | Branch eskiradi, konflikt chiqadi | Merge xatolari, qayta test |
| 1 hafta | PR tashlab ketiladi yoki majburan merge qilinadi | Review foydasi nolga tushadi |

Amaliy xulosa: kutish vaqtini qisqartirish review chuqurligini oshirishdan muhimroq. Ikki soatda yuzaki o'qilgan va darhol javob berilgan PR, ikki kundan keyin chuqur o'qilgan PR dan ko'proq foyda beradi, chunki muallif hali kontekstda.

### 2.4 Reviewer soni: ikkinchidan keyin qaytim tushadi

Kuzatuvlar birinchi reviewer xatolarning katta qismini topishini, ikkinchisi sezilarli qo'shimcha berishini, uchinchisidan keyin esa qaytim tez pasayishini ko'rsatadi. Sababi oddiy: ikki odam bir xil joylarga qaraydi.

Shu sababli samarali siyosat sonni emas, rolni belgilaydi. Ikki reviewer kerak bo'lsa, ularga turli vazifa beriladi: biri domen va mantiqni ko'radi, ikkinchisi operatsion xavfni (migratsiya, konfiguratsiya, monitoring) ko'radi. Aks holda ikkinchi reviewer birinchisining ishini takrorlaydi va mas'uliyat tarqaydi.

| Reviewer soni | Qo'shimcha foyda | Qo'shimcha narx | Qachon o'rinli |
| --- | --- | --- | --- |
| 1 | Asosiy foyda | 1 x vaqt | Oddiy o'zgarish |
| 2 (turli rol bilan) | Sezilarli, agar rollar ajratilgan bo'lsa | 2 x vaqt + muvofiqlashtirish | Xavfli o'zgarish |
| 3 va ko'p | Kichik | Navbat uzayadi, mas'uliyat tarqaydi | Faqat o'rganish maqsadida |

### 2.5 Review byudjeti: haftada qancha vaqt

Review vaqti rejadan tashqari emas, reja ichida bo'lishi kerak. Amaliy raqam: jamoa a'zosi haftasining taxminan 10-15 foizi review ga ketadi. Besh kunlik haftada bu kuniga taxminan 45-60 daqiqa. Agar bu vaqt rejaga kiritilmasa, review "bo'sh vaqtda" qiladigan ish bo'lib qoladi va bo'sh vaqt hech qachon kelmaydi.

Byudjetni taqsimlashning foydali usuli: kunda ikki oyna. Masalan ertalab ishni boshlashda 30 daqiqa va tushdan keyin 30 daqiqa. Bu uzluksiz kodlash vaqtini saqlaydi va ayni paytda PR ning kutish vaqtini yarim kundan oshirmaydi. Har xabarga darhol javob berish esa ikkala ishni ham buzadi.

### 2.6 Review ni bo'lish: stacked PR texnikasi

Katta o'zgarishni mayda PR larga bo'lishning eng ishlaydigan usuli - bir-birining ustiga qo'yilgan branchlar. Har bir PR o'zidan oldingisiga nisbatan diff ko'rsatadi va alohida review qilinadi.

```bash
# Katta funksiyani uchta review qilinadigan bo'lakka bo'lish.
# Qoida: har bo'lak o'zi mustaqil kompilyatsiya bo'lsin va testdan o'tsin.

git switch -c feat/payout-1-schema main
# 1-PR: faqat migratsiya va entity. Mantiq yo'q, xavf kichik.
#       Review fokusi: sxema, indeks, orqaga moslik.

git switch -c feat/payout-2-domain feat/payout-1-schema
# 2-PR: domen mantiqi va unit testlar. Baza tegmaydi.
#       Review fokusi: qoida, chegaraviy holat, invariant.

git switch -c feat/payout-3-api feat/payout-2-domain
# 3-PR: controller, DTO, validation, xato javobi.
#       Review fokusi: tashqi shakl, moslik, idempotentlik.

# Birinchi PR merge bo'lgandan keyin qolganlarini yangilash:
git switch feat/payout-2-domain && git rebase --onto main feat/payout-1-schema
# Yoki merge bilan (jamoa konvensiyasiga qarab):
#   git switch feat/payout-2-domain && git merge main
```

Bo'lishning to'g'ri chizig'i qatlam bo'yicha emas, xavf bo'yicha o'tadi. Sxema o'zgarishi alohida, chunki uni qaytarish qiyin. Domen mantiqi alohida, chunki u eng ko'p o'qishni talab qiladi. API shakli alohida, chunki u tashqi mijozga ta'sir qiladi.

### 2.7 Rework: review ning yashirin narxi

Review dan keyin qayta yozilgan kod - alohida xarajat moddasi. Agar PR uch marta tuzatish davrasidan o'tsa, bu olti kontekst almashinuvi degani. Rework ko'p bo'lsa, sabab ko'pincha review da emas: talab noaniq bo'lgan yoki dizayn muhokama qilinmagan.

Amaliy mezon: o'rtacha PR bir yoki ikki tuzatish davrasida yopilishi kerak. Uchdan ko'p davra tizimli muammo belgisi. Shu holatda yechim review ni yumshatish emas, PR dan oldingi bosqichni tuzatish: talabni aniqlashtirish yoki dizayn eskizi.

### 2.8 Review ning qaytimi qachon manfiy bo'ladi

Review foydasi narxidan kam bo'lgan holatlar bor va ularni tan olish kerak. Masalan: bir qatorli konfiguratsiya o'zgarishi, versiya raqamini ko'tarish, matn tuzatish, test ma'lumotini qo'shish. Bunday o'zgarishlar uchun yengil yo'l qo'yish kerak: avtomatik approve qoidasi yoki post-commit review.

```yaml
# .github/workflows/auto-approve-trivial.yml
# Faqat haqiqatan xavfsiz yo'llar uchun. Ro'yxat qisqa bo'lishi kerak.
name: trivial-fast-path
on: pull_request_target
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Faqat xavfsiz fayllar o'zgarganini tekshirish
        run: |
          CHANGED=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          echo "$CHANGED"
          # Xavfsiz ro'yxatdan tashqari biror narsa bo'lsa - oddiy review.
          UNSAFE=$(echo "$CHANGED" | grep -vE '^(docs/|README\.md|CHANGELOG\.md)' || true)
          if [ -n "$UNSAFE" ]; then
            echo "Oddiy review kerak: $UNSAFE"
            exit 1
          fi
```

Diqqat: bu ro'yxatga `src/main/resources/application*.yml` yoki migratsiya papkasi hech qachon kirmaydi. Konfiguratsiya o'zgarishi diffda kichik, oqibatda esa eng katta incidentlarni keltirib chiqaradigan sinf.

### 2.9 Byudjetni xavf bo'yicha taqsimlash

Review vaqtini barcha PR larga teng taqsimlash - resursni isrof qilish. To'g'ri model: xavf bo'yicha tabaqalash. Kichik xavfli PR bir reviewer va yuzaki o'tish bilan ketadi, yuqori xavfli PR ikki reviewer, checklist va lokal sinovni talab qiladi.

| Xavf darajasi | Belgisi | Review rejimi |
| --- | --- | --- |
| Past | Faqat test, docs, log matni, ichki refactoring | 1 reviewer, yuzaki |
| O'rta | Yangi endpoint, biznes qoidasi o'zgarishi | 1 reviewer, satr-satr |
| Yuqori | Migratsiya, pul hisobi, autentifikatsiya, tashqi API shakli | 2 reviewer, checklist, lokal sinov |
| Juda yuqori | Ma'lumotni o'chiradigan yoki ko'chiradigan skript | 2 reviewer + dry-run natijasi + qaytish rejasi |

Shu jadvalni repoda `CODEOWNERS` va PR shabloni bilan birga saqlash kerak, shunda tabaqalash og'zaki kelishuvdan jarayonga aylanadi. CODEOWNERS mexanikasi 40-bobda.

### 2.10 Raqamlarni o'z loyihangizda o'lchash

Yuqoridagi raqamlar yo'nalish beradi, lekin qaror sizning raqamlaringizdan chiqadi. Minimal to'plam: PR ning birinchi javobni kutish vaqti (median va p90), o'zgargan satr soni taqsimoti, tuzatish davralari soni, va review dan keyin prodda topilgan xatolar soni.

```bash
# Repo tarixidan review iqtisodini o'lchash (GitHub CLI bilan).
# 1) Ochilish va birinchi review orasidagi vaqt (oxirgi 100 PR).
gh pr list --state merged --limit 100 \
  --json number,createdAt,reviews \
  --jq '.[] | select(.reviews|length>0)
        | {pr:.number,
           kutish_soat: (((.reviews[0].submittedAt|fromdate) - (.createdAt|fromdate))/3600|floor)}' \
  | head -20

# 2) PR hajmi taqsimoti: mediana va eng kattalari.
gh pr list --state merged --limit 100 --json number,additions,deletions \
  --jq 'map(.additions + .deletions) | sort
        | {median: .[length/2|floor], p90: .[length*0.9|floor], max: .[-1]}'

# 3) Tuzatish davralari: review dan keyin kelgan commitlar soni.
gh pr list --state merged --limit 50 --json number,commits,reviews \
  --jq '.[] | {pr:.number, commitlar:(.commits|length), reviewlar:(.reviews|length)}'
```

Bu raqamlar bir oyda bir marta o'lchansa yetadi. Maqsad - tendentsiyani ko'rish, dashboard qurish emas. Metrikalarning to'liq to'plami va ularning tuzogi 42-bobda.

### 2.11 Amalda qo'llash

- [ ] Oxirgi 100 merge qilingan PR uchun birinchi javobni kutish vaqtining medianasi va p90 ini hisoblang.
- [ ] PR hajmi taqsimotini chiqarib, 400 satrdan katta PR ulushini aniqlang va shu PR larda topilgan izohlar sonini taqqoslang.
- [ ] CI ga PR hajmi haqida ogohlantirish qo'shing: mantiq satrlari 400 dan oshsa, izoh yozilsin (bloklamasin).
- [ ] Jamoada kunlik ikki review oynasini kelishib oling va uni kalendarga qo'ying.
- [ ] Xavf tabaqalash jadvalini `REVIEW.md` ga qo'shing va yuqori xavfli yo'llar uchun ikki reviewer talabini sozlang.
- [ ] Stacked PR usulini bitta katta funksiyada sinab ko'ring: sxema, domen va API ni uch PR ga bo'ling.
- [ ] Uchdan ko'p tuzatish davrasidan o'tgan oxirgi uch PR ni ko'rib, sababi talabda yoki dizaynda ekanini aniqlang.
- [ ] Trivial yo'llar ro'yxatini (docs, changelog) belgilab, ularga yengil yo'l bering va bu ro'yxatga konfiguratsiya fayllari kirmasligini tasdiqlang.

## 3. Reviewer ning tahlil apparati: niyat, invariant, xavf yuzasi (The Reviewer's Analytical Apparatus)

Yaxshi reviewer diffni o'qimaydi, u diffni tahlil qiladi. Farq shunda: o'qish satrlarni ko'radi, tahlil esa kodning ortidagi uchta narsani tiklaydi - muallif nimani nazarda tutgan, kod qanday qoidani buzmasligi kerak va bu o'zgarish nimaga tegib ketadi. Shu uchlik topilmasa, qolgan hamma izoh didga aylanadi. Bu bob shu apparatni beradi, keyingi boblar esa uni Java, Spring va PostgreSQL ga qo'llaydi.

### 3.1 Review ning uch o'qishi

Bitta diffni uch marta o'qish kerak, har safar boshqa savol bilan. Uchini birlashtirgan reviewer ikkinchi faylda chalg'iydi va uchinchi faylda faqat nomlash haqida yozadi.

Birinchi o'qish - niyat. Bu o'zgarish qanday muammoni yechadi, va shu muammo shu joyda yechilishi kerakmi. Satrlarga qaramaydi, fayllar ro'yxati va umumiy shaklga qaraydi. Odatda 5 daqiqa.

Ikkinchi o'qish - mexanika. Kod aytganini qiladimi: null yo'llari, chegaraviy qiymatlar, tur konversiyasi, tranzaksiya chegarasi, poyga holati, resurs yopilishi. Bu eng uzun qism.

Uchinchi o'qish - xavf. Bu kod prodda birinchi marta ishga tushganda nima bo'ladi: eski ma'lumot bilan, ikki instansda, yuk ostida, tashqi servis javob bermaganda, migratsiya yarim qolganda.

| O'qish | Savol | Nimaga qaraydi | Vaqt ulushi |
| --- | --- | --- | --- |
| 1. Niyat | Nima uchun va nega shu yerda | PR tavsifi, fayllar ro'yxati, public API | 15% |
| 2. Mexanika | Kod aytganini qiladimi | Satrlar, shartlar, turlar, chegaralar | 55% |
| 3. Xavf | Prodda nima bo'ladi | Migratsiya, konfiguratsiya, yuk, nosozlik | 30% |

### 3.2 Niyatni koddan tiklash, tavsifdan emas

PR tavsifi muallifning o'zi haqida aytgan gapi. Kod esa haqiqat. Tajribali reviewer avval tavsifni o'qiydi, keyin uni unutib, koddan niyatni mustaqil tiklaydi va ikkisini taqqoslaydi. Farq chiqsa - bu eng qimmatli topilma.

Uch xil farq uchraydi. Birinchi: tavsifda aytilgan, kodda yo'q (masalan "idempotentlik qo'shildi" deyilgan, lekin kalit bo'yicha unique constraint yo'q). Ikkinchi: kodda bor, tavsifda yo'q (yo'l-yo'lakay o'zgartirilgan timeout, olib tashlangan tekshiruv). Ikkinchisi xavfliroq, chunki uni hech kim kutmagan. Uchinchi: ikkisi ham bor, lekin kod boshqa narsani qiladi.

```java
// PR tavsifi: "Buyurtma bekor qilishni qo'shdim".
// Koddan tiklangan niyat: buyurtma statusini CANCELLED ga o'tkazish.
// Farq: tavsifda pul qaytarish haqida bir og'iz gap yo'q, kodda esa bor.
@Transactional
public void cancel(long orderId, String reason) {
    Order order = orders.findById(orderId).orElseThrow();
    order.setStatus(CANCELLED);
    order.setCancelReason(reason);
    // Bu satr tavsifda yo'q edi. Reviewer uchun bu asosiy savol:
    // to'lov qaytarish shu tranzaksiya ichida sinxron chaqirilyaptimi?
    paymentClient.refund(order.getPaymentId(), order.getTotal());
    orders.save(order);
}
// Review izohi (blocker): tashqi to'lov chaqiruvi DB tranzaksiyasi ichida.
// refund 30 sekund javob bermasa, DB ulanishi va qulf shu vaqt egallanadi.
// Bundan tashqari refund o'tib, keyin commit yiqilsa, pul qaytgan, status
// hali ACTIVE bo'lib qoladi. Outbox yoki ikki qadamli holat kerak.
```

### 3.3 Invariantni topish: nima har doim rost bo'lishi kerak

Invariant - tizim holati haqida har doim rost bo'lishi kerak bo'lgan gap. "Buyurtma summasi qatorlar summasiga teng", "hisobdagi qoldiq manfiy bo'lmaydi", "bitta idempotentlik kaliti bitta to'lovga tegishli", "yetkazilgan buyurtma bekor qilinmaydi". Xatolarning katta qismi - buzilgan invariant.

Reviewer ning ishi: diffdan ta'sirlangan invariantlar ro'yxatini tuzish va har biri uchun himoya qayerda ekanini topish. Himoya uch joyda bo'lishi mumkin - domen obyekti ichida, ma'lumotlar bazasi constraint ida, yoki hech qayerda. Uchinchi javob eng ko'p uchraydi.

| Invariant | Eng ishonchli himoya | Yetarsiz himoya |
| --- | --- | --- |
| Qoldiq manfiy emas | DB `CHECK (balance >= 0)` + domen tekshiruvi | Faqat servisdagi `if` |
| Kalit yagona | DB `UNIQUE` indeks | `findBy` keyin `save` (poyga) |
| Status o'tishi qoidali | Domen ichida state machine | Controller dagi `switch` |
| Summalar mosligi | Agregat ichida hisoblash | Alohida `update` so'rovlari |
| Sana oralig'i to'g'ri | DB `CHECK (ends_at > starts_at)` | Faqat frontend validation |

Shu jadvalning asosiy xabari: ikki instansda ishlaydigan ilovada faqat Java kodidagi `if` invariantni himoya qilmaydi. Tekshiruv va yozuv orasida boshqa instans o'zgartirishi mumkin. Shu sababli har bir invariant uchun review savoli bitta: "ikki parallel so'rov bu tekshiruvni chetlab o'ta oladimi".

### 3.4 Xavf yuzasi: o'zgarish nimaga tegadi

Diff o'zgargan satrlarni ko'rsatadi, lekin xavf o'zgarmagan kodda yashaydi. Xavf yuzasi - shu o'zgarish ta'sir qiladigan hamma narsa: chaqiruvchilar, bir xil jadvalga yozadigan boshqa kod, kesh, tashqi mijozlar, batch ishlar, hisobotlar.

```bash
# Xavf yuzasini git bilan o'lchash. Diffda yo'q, lekin ta'sirlangan joylar.
BASE=origin/main

# 1) O'zgargan public metodlarning chaqiruvchilarini topish.
git diff -U0 $BASE...HEAD -- '*.java' \
  | grep -oE '^\+.*(public|protected) [A-Za-z<>,\[\] ]+ ([a-z][A-Za-z0-9]*)\(' \
  | grep -oE '[a-z][A-Za-z0-9]*\($' | tr -d '(' | sort -u \
  | while read -r m; do
      n=$(grep -rln --include='*.java' "\.$m(" src/main/java | wc -l)
      printf '%-35s %s ta faylda chaqiriladi\n' "$m" "$n"
    done

# 2) O'zgargan jadvalga yozadigan boshqa joylarni topish.
git diff $BASE...HEAD -- 'src/main/resources/db/**' \
  | grep -ioE '(alter|create) table ([a-z_]+)' | awk '{print $3}' | sort -u \
  | while read -r t; do
      echo "--- $t jadvaliga tegadigan kod:"
      grep -rln --include='*.java' --include='*.sql' -i "$t" src/main | head
    done

# 3) Shu fayllar bilan tarixda birga o'zgargan fayllar (yashirin bog'liqlik).
for f in $(git diff --name-only $BASE...HEAD -- '*.java'); do
  git log --format='%H' -20 -- "$f" \
    | xargs -I{} git show --name-only --format= {} 2>/dev/null
done | sort | uniq -c | sort -rn | head -15
```

Uchinchi buyruq eng foydali: tarixda shu fayl bilan birga o'zgargan fayllar - yashirin bog'liqlik xaritasi. Agar `OrderService.java` tarixda 20 marta `InvoiceMapper.java` bilan birga o'zgargan bo'lsa, lekin bu PR da `InvoiceMapper` tegilmagan bo'lsa, bu savol: nega bu safar kerak bo'lmadi.

### 3.5 Ko'rinmayotgan kodni ko'rish

Eng qimmat xatolar diffda bor narsada emas, yo'q narsada yashaydi. Diff yo'q narsani ko'rsatmaydi, shu sababli reviewer uni ro'yxat bo'yicha so'raydi.

| Yo'q bo'lishi mumkin bo'lgan narsa | Savol | Oqibati |
| --- | --- | --- |
| Validation | Tashqi kirish qayerda tekshirilgan | Buzilgan ma'lumot bazaga tushadi |
| Avtorizatsiya | Bu endpointni kim chaqira oladi | Boshqa foydalanuvchi ma'lumotiga kirish |
| Timeout | Tashqi chaqiruvda chegara bormi | Thread va pool to'lib qoladi |
| Index | Yangi `WHERE` ustuni indekslanganmi | Seq scan, sekin so'rov |
| Test | Chegaraviy holat qamralganmi | Regressiya keyingi PR da chiqadi |
| Log va metrika | Xato bo'lsa, qanday bilamiz | Ko'r incident |
| Migratsiyaning orqaga yo'li | Qaytarish rejasi bormi | Reliz qaytarilmaydi |
| Idempotentlik | Ikki marta kelsa nima bo'ladi | Ikki marta to'lov, dublikat qator |
| Null holati | Bu maydon bo'sh kelsa | NPE yoki jim noto'g'ri hisob |
| Bo'sh to'plam holati | Ro'yxat bo'sh bo'lsa | `get(0)`, noto'g'ri o'rtacha, 0 ga bo'lish |

Bu jadval review ning asosiy quroli. Har bir PR uchun o'ninchi qatorga tushmasdan kamida birinchi oltitasini o'tish kerak.

### 3.6 Miyada ishga tushirish: beshta ssenariy

Tajribali reviewer kodni o'qiyotganida uni ishga tushiradi. Beshta ssenariy har doim qo'llaniladi va ularning har biri boshqa sinf xatoni ochadi.

Birinchi: happy path. Hamma narsa yaxshi ishlagan holat. Muallif odatda shuni test qilgan.

Ikkinchi: bo'sh va chegaraviy kirish. Null, bo'sh satr, bo'sh ro'yxat, nol, manfiy son, juda uzun satr, `Integer.MAX_VALUE`, kelasi sanadagi vaqt.

Uchinchi: ikki marta. Bir xil so'rov ikki marta keldi (foydalanuvchi ikki marta bosdi, retry ishladi, Kafka xabarni qayta yetkazdi).

To'rtinchi: ikki parallel. Ikki so'rov bir vaqtda, ikki instansda. Tekshiruv va yozuv orasida nima o'zgarishi mumkin.

Beshinchi: o'rtada yiqilish. Kod yarmida protsess o'ldi, yoki tashqi chaqiruv timeout bo'ldi, yoki commit yiqildi. Qaysi holat qoladi.

```java
// Shu beshta ssenariyni qo'llash uchun misol. Kod bir qarashda to'g'ri.
@Transactional
public Reservation reserve(long eventId, int seats, String idemKey) {
    Event event = events.findById(eventId).orElseThrow();
    if (event.getAvailable() < seats) {                 // (1)
        throw new NotEnoughSeatsException();
    }
    event.setAvailable(event.getAvailable() - seats);   // (2)
    return reservations.save(new Reservation(eventId, seats, idemKey));
}
// 1-ssenariy: ishlaydi.
// 2-ssenariy: seats = 0 yoki manfiy bo'lsa? Tekshiruv yo'q. Manfiy seats
//             bilan available oshib ketadi - joy "yaratiladi".
// 3-ssenariy: idemKey bo'yicha UNIQUE yo'q. Ikki marta kelsa - ikki bron.
// 4-ssenariy: (1) va (2) orasida boshqa instans ham o'qidi. Ikkisi ham
//             o'tadi, available manfiyga tushadi. Optimistik versiya yoki
//             atomik UPDATE kerak.
// 5-ssenariy: save o'tib, commit yiqilsa - butun tranzaksiya qaytadi, bu
//             to'g'ri. Lekin bu yerda tashqi chaqiruv bo'lsa, bo'lmaydi.
```

Shu beshlikdan ikkinchi, uchinchi va to'rtinchisi - review ning eng ko'p qaytim beradigan qismi, chunki ularni testlar odatda qamramaydi va statik tahlil ko'rmaydi.

### 3.7 Chuqurlik darajasi: xavf bo'yicha triage

Hamma PR ni bir xil chuqurlikda o'qish - resursni noto'g'ri sarflash. Reviewer birinchi 2 daqiqada chuqurlik darajasini tanlashi kerak va buni ongli qilishi lozim.

| Daraja | Qachon | Nima qilinadi | Vaqt |
| --- | --- | --- | --- |
| Skim | Docs, log matni, test qo'shish, lokalizatsiya | Niyat va shakl | 5 daqiqa |
| Normal | Ichki mantiq, yangi endpoint, refactoring | Uch o'qish, chegaraviy holatlar | 20-40 daqiqa |
| Deep | Migratsiya, pul, auth, concurrency, tashqi API | Uch o'qish + 5 ssenariy + checklist | 1-2 soat |
| Audit | Ma'lumot ko'chirish, kriptografiya, ko'p modulga tegadigan refactoring | Deep + lokal ishga tushirish + qaytish rejasi | Yarim kun |

Chuqurlikni tanlash mezoni - "xato bo'lsa, qaytarish qancha turadi" degan savol. Qaytarish arzon bo'lsa (kod o'zgarishi, qayta deploy), Normal yetadi. Qaytarish qimmat bo'lsa (ma'lumot o'zgargan, tashqi mijoz moslashgan, pul ko'chgan), Deep yoki Audit.

### 3.8 Kognitiv tuzoqlar

Reviewer ham odam, va uning diqqati bir necha tanish tarzda aldanadi.

Birinchi tuzoq - birinchi taassurot (anchoring). Diffning boshida ko'rilgan uslub xatosi diqqatni uslubga qulflaydi va keyingi fayldagi tranzaksiya xatosi ko'rinmaydi. Qarshi chora: birinchi o'qishda hech qanday izoh yozmaslik.

Ikkinchi tuzoq - muallif obro'si (authority bias). Senior yozgan kodni yuzaki o'qish va junior kodini satr-satr tekshirish. Amalda senior ham xuddi shunday xato qiladi, lekin uning xatosi ko'proq joyga tarqaydi. Qarshi chora: muallif ismini ko'rmasdan o'qishga urinish, yoki checklistni har ikki holatda bir xil qo'llash.

Uchinchi tuzoq - charchoq. Birinchi fayl batafsil, oltinchi fayl "LGTM". Qarshi chora: katta PR ni ikki o'tirishga bo'lish, yoki eng xavfli fayldan boshlash.

To'rtinchi tuzoq - tanishlik (mere exposure). Kod uslubi o'ziga tanish bo'lsa, u to'g'ri ko'rinadi. Shu sababli "men shunday yozmagan bo'lardim" degan hissiyot izohga aylanmasligi kerak, agar ortida aniq sabab bo'lmasa.

Beshinchi tuzoq - tugatish istagi (sunk cost). Muallif ikki hafta ishlagan PR ni rad qilish qiyin. Lekin yondashuv noto'g'ri bo'lsa, ikki hafta allaqachon ketgan va uni "saqlash" uchun yana ikki oy to'lash mantiqsiz.

### 3.9 Review ni qachon to'xtatish

Review tugadi deb hisoblash uchun uchta shart bor: uch o'qish bajarildi, ko'rinmayotgan kod ro'yxati o'tildi, va qolgan savollar yozib qoldirildi. To'rtinchi shart yo'q - mukammallik shart emas.

Review ni to'xtatish kerak bo'lgan ikki holat alohida. Birinchi: diff juda katta yoki tuzilmagan - bu holda satrlarni o'qishni boshlamasdan, "bo'lib yuborish" deb javob berish to'g'ri va halol. Ikkinchi: PR da asosiy dizayn savoli ochiq - detallarga izoh yozish ma'nosiz, chunki yondashuv o'zgarsa, kod ham o'zgaradi. Bu holda bitta savol yozib, javobni kutish kerak.

```text
# Dizayn savoli ochiq bo'lganda review javobi: detallarga tushmaslik.

Hozircha satrlarga izoh yozmadim, chunki bitta asosiy savol bor.

Bu yerda refund DB tranzaksiyasi ichida sinxron chaqirilgan. Shu qaror
o'zgarsa (outbox yoki ikki qadamli holat), quyidagi 4 fayl ham o'zgaradi,
shuning uchun avval shuni kelishib olsak foydali.

Variantlar:
1) Outbox: status o'zgaradi + outbox qatori, worker refund chaqiradi.
   Narxi: bir jadval va worker. Foyda: tranzaksiya qisqa, retry bepul.
2) Sinxron qoldirish + qisqa timeout + idempotentlik kaliti.
   Narxi: tranzaksiya tashqi servisga bog'liq qoladi.

Men 1-variantni taklif qilaman. Qaysi birini tanlasak, keyin satr-satr
o'qib chiqaman.
```

### 3.10 Review natijasini yozib qoldirish

Review ning chiqishi - izohlar emas, xulosa. Xulosa to'rt qismdan iborat: nimani tekshirdim, nimani tekshirmadim, bloklaydigan narsalar, va qolgan xavf. Bu to'rtlik keyingi incidentda juda qimmat bo'ladi, chunki u o'sha paytda nima bilinganini ko'rsatadi.

Xulosa yozishning yon foydasi ham bor: u reviewer ni o'z ishini baholashga majbur qiladi. "Tekshirmadim" ro'yxati bo'sh bo'lsa, demak reviewer o'ziga haddan ortiq ishongan.

### 3.11 Amalda qo'llash

- [ ] Keyingi review da uch o'qishni ongli ajratib bajaring va birinchi o'qishda hech qanday izoh yozmang.
- [ ] Har bir PR uchun ta'sirlangan invariantlar ro'yxatini yozing va har biri uchun himoya qayerda ekanini (domen, DB constraint, hech qayerda) belgilang.
- [ ] Faqat Java kodidagi `if` bilan himoyalangan invariantlarni toping va ularga DB darajasidagi `UNIQUE` yoki `CHECK` qo'shishni talab qiling.
- [ ] Xavf yuzasini o'lchaydigan git skriptini repoga `scripts/review-impact.sh` sifatida qo'shing.
- [ ] Ko'rinmayotgan kod jadvalini (10 band) PR shabloniga reviewer uchun ro'yxat sifatida qo'shing.
- [ ] Beshta ssenariyni (happy, chegara, ikki marta, ikki parallel, o'rtada yiqilish) oxirgi uchta PR ga qo'llab, nechta yangi savol chiqqanini sanang.
- [ ] Chuqurlik darajalari jadvalini `REVIEW.md` ga kiritib, har PR da darajani izohda ko'rsatishni odat qiling.
- [ ] Review xulosasi shablonini (tekshirdim / tekshirmadim / blocker / qolgan xavf) joriy qiling.

## 4. Diffni o'qish mexanikasi (Reading a Diff)

Diff - mashina uchun qulay, odam uchun noqulay format. U fayllarni alifbo bo'yicha beradi, kontekstni uch satrga qisqartiradi, ko'chirilgan kodni yangi kod deb ko'rsatadi va o'chirilgan kodning kim tomonidan ishlatilganini aytmaydi. Shu sababli diffni interfeys bergan tartibda o'qish - eng keng tarqalgan review xatosi. Bu bob o'qish tartibini va instrumentlarini beradi.

### 4.1 Nega interfeys bergan tartib noto'g'ri

GitHub diffni fayl yo'li bo'yicha alifbo tartibida ko'rsatadi. Natijada reviewer `controller` dan boshlaydi, `domain` ni o'rtada ko'radi, `resources/db/migration` ni esa oxirida - charchagan holda. Ammo xavf taqsimoti teskari: migratsiya eng xavfli, controller eng arzon.

Ikkinchi muammo - uch satrli kontekst. Metodning o'rtasidagi o'zgarish ko'rinadi, lekin uning boshida qanday tekshiruv borligi ko'rinmaydi. Reviewer esa shu ko'rinmagan kontekstga asoslanib "yaxshi" deb o'ylaydi.

### 4.2 To'g'ri o'qish tartibi: sakkiz qadam

| Qadam | Nima o'qiladi | Nima izlanadi |
| --- | --- | --- |
| 1 | PR tavsifi va tiket | Niyat, qamrov, aytilmagan narsalar |
| 2 | Fayllar ro'yxati va statistika | Shakl, kutilmagan fayllar, hajm |
| 3 | Migratsiya va sxema | Qulf, orqaga moslik, indeks, constraint |
| 4 | Public API: controller shakli, DTO, event, interfeys | Tashqi moslik, breaking change |
| 5 | Domen va biznes mantiqi | Invariant, chegaraviy holat, poyga |
| 6 | Infratuzilma: repository, client, mapper | N+1, timeout, mapping yo'qotishi |
| 7 | Konfiguratsiya va bog'liqliklar | Timeout, pool, secret, yangi kutubxona |
| 8 | Testlar | To'liqlik, assertion sifati, yolg'on ishonch |

Testlar oxirida o'qiladi, lekin bu ularning muhimligi kamligini bildirmaydi. Sabab boshqa: mantiqni o'qigandan keyin reviewer qanday testlar bo'lishi kerakligini biladi, va shu bilimdan testlardagi bo'shliqni ko'radi. Teskari tartibda testlar reviewer ning fikrini bog'lab qo'yadi.

```bash
# 2-qadamni bir buyruq bilan: PR ning shaklini ko'rish.
BASE=origin/main
git diff --stat $BASE...HEAD | tail -1
echo "--- xavfli yo'llar bu PR da tegilganmi:"
git diff --name-only $BASE...HEAD | grep -E \
  'db/(migration|changelog)|SecurityConfig|application.*\.(yml|properties)|pom\.xml|build\.gradle' \
  || echo "yo'q"
echo "--- yangi fayllar:"
git diff --name-status $BASE...HEAD | awk '$1=="A"{print $2}'
echo "--- o'chirilgan fayllar:"
git diff --name-status $BASE...HEAD | awk '$1=="D"{print $2}'
echo "--- ko'chirilgan/nomi o'zgargan:"
git diff --name-status -M $BASE...HEAD | awk '$1 ~ /^R/{print $2" -> "$3}'
```

### 4.3 Kontekstni tiklash

O'zgargan satrni tushunish uchun uning atrofidagi kod kerak. Uch satr kamlik qiladi. Ikki yo'l bor: faylni to'liq ochib o'qish, yoki diffga funksiya konteksti qo'shish.

```bash
# Funksiyaning butun tanasini kontekst sifatida ko'rsatish.
git diff --function-context origin/main...HEAD -- src/main/java/.../OrderService.java

# Bo'sh joy o'zgarishini e'tiborsiz qoldirish (indentatsiya shovqinini olib tashlaydi).
git diff -w origin/main...HEAD

# Ko'chirilgan kodni "yangi" deb ko'rsatmaslik: -M nomi o'zgarishini, -C
# ko'chirishni aniqlaydi. Katta refactoringda diffni bir necha baravar kichraytiradi.
git diff -M -C --find-copies-harder origin/main...HEAD

# Faqat so'z darajasidagi farq: uzun satrlarda nima o'zgarganini ko'rish.
git diff --word-diff=color origin/main...HEAD -- '*.sql'

# Bu o'zgarish qachon va nega kirgan: satr tarixini kuzatish.
git log -L 120,160:src/main/java/com/acme/order/OrderService.java

# Shu simvol tarixda qachon qo'shilgan va olib tashlangan.
git log -S 'findTop20ByCustomerId' --oneline -- '*.java'

# Regex bo'yicha: timeout sozlamalari tarixda qanday o'zgargan.
git log -G 'connection-timeout' --oneline -p -- '*.yml' | head -40
```

`git log -S` review da alohida qimmatli: diffda bir tekshiruv olib tashlangan bo'lsa, u qachon va qanday sabab bilan qo'shilganini ko'rsatadi. Ko'p hollarda u o'tgan incidentdan keyin qo'yilgan bo'ladi, va uni olib tashlash o'sha incidentni qaytaradi.

### 4.4 O'chirilgan kodni o'qish

Qo'shilgan kod diqqatni tortadi, o'chirilgan kod esa e'tibordan chetda qoladi. Lekin review da eng xavfli o'zgarishlar aynan o'chirishlardir: olib tashlangan `if`, olib tashlangan `catch`, olib tashlangan test, kamaytirilgan log darajasi.

Har bir o'chirilgan blok uchun uch savol: bu nima uchun qo'yilgan edi (`git log -S` yoki blame), uni olib tashlash nimani ochib qo'yadi, va uning o'rniga nima keldi. Agar javob "endi kerak emas" bo'lsa, javob yetarli emas - nega kerak emas degan tushuntirish kerak.

```bash
# Faqat o'chirilgan satrlarni ko'rish: review ning eng kam qilinadigan qadami.
git diff origin/main...HEAD | grep -E '^-' | grep -vE '^---' | less

# O'chirilgan tekshiruvlar va xato ishlash joylari - alohida diqqat.
git diff origin/main...HEAD | grep -E '^-' \
  | grep -iE 'if \(|throw|catch|assert|validate|@Valid|@PreAuthorize|requireNonNull|UNIQUE|NOT NULL'

# O'chirilgan testlar: eng xavfli signal.
git diff --numstat origin/main...HEAD -- '*[Tt]est*' | awk '$2>0{print $2" satr test kodidan olib tashlangan: "$3}'
```

### 4.5 Commit tarixini o'qish

Commitlar muallifning fikr yo'lini ko'rsatadi. "Fix", "fix again", "revert fix" ketma-ketligi - muallif o'zi ham tushunmagan joy borligini bildiradi, va aynan shu joy review ning asosiy nuqtasi.

```bash
# Commitlar va ularning hajmi: fikr yo'lini ko'rish.
git log --oneline --stat origin/main..HEAD | head -60

# "fix", "wip", "revert" naqshlari: noaniqlik belgisi.
git log --oneline origin/main..HEAD | grep -icE 'fix|wip|revert|try|temp'

# Birinchi va oxirgi holatni taqqoslash: oraliq urinishlarni o'tkazib yuborish.
git diff origin/main...HEAD --stat
```

Diqqat: squash merge ishlatadigan jamoada commit tarixi review dan keyin yo'qoladi, shu sababli uni review paytida o'qish yagona imkoniyat.

### 4.6 PR ni lokalda olib tekshirish

Yuqori xavfli PR ni faqat brauzerda o'qish yetarli emas. Lokalda olish uch narsani beradi: IDE navigatsiyasi (chaqiruvchilarga o'tish), testlarni ishga tushirish, va migratsiyani real bazada sinash.

```bash
# PR ni lokalda olish va tekshirish (GitHub).
gh pr checkout 1423
# Yoki toza git bilan:
#   git fetch origin pull/1423/head:pr-1423 && git switch pr-1423

# 1) Tez tekshiruvlar: kompilyatsiya, uslub, statik tahlil.
./mvnw -q -T1C verify -DskipITs

# 2) Faqat o'zgargan modullarning testlari (vaqtni tejash).
./mvnw -q -pl order-service -am test

# 3) Migratsiyani real PostgreSQL da sinash (Testcontainers yoki docker).
docker run -d --name rv -e POSTGRES_PASSWORD=p -p 55432:5432 postgres:16
./mvnw -q flyway:migrate -Dflyway.url=jdbc:postgresql://localhost:55432/postgres \
        -Dflyway.user=postgres -Dflyway.password=p

# 4) Migratsiya qancha qulf oldi va qancha turdi - log dan ko'rish.
docker logs rv 2>&1 | grep -iE 'lock|duration|error' | tail

# 5) Tozalash.
docker rm -f rv
```

### 4.7 Katta PR ni xavf nuqtalari bo'yicha o'qish

Ba'zan katta PR ni bo'lish imkoni yo'q: framework yangilanishi, avtomatik refactoring, generated kodning qayta chiqishi. Bunday holatda satrlarni o'qish o'rniga xavf nuqtalari bo'yicha yuriladi va bu usul izohda ochiq aytiladi.

```bash
# 3000 satrli framework yangilanishini xavf nuqtalari bo'yicha o'qish.
BASE=origin/main

# 1) Faqat qo'lda yozilgan kod o'zgarishlari (generated emas).
git diff --stat $BASE...HEAD -- 'src/main/java' ':!**/generated/**'

# 2) Xulq o'zgartiradigan naqshlar: konfiguratsiya va standart qiymatlar.
git diff $BASE...HEAD | grep -E '^[+-]' \
  | grep -iE 'timeout|pool|retry|ttl|batch|fetch|isolation|readOnly|lazy|cache'

# 3) Xavfsizlikka tegadigan joylar.
git diff $BASE...HEAD -- '*Security*' '*Filter*' '*Auth*' | head -100

# 4) Bog'liqlik daraxtidagi haqiqiy o'zgarish (pom diffidan ishonchliroq).
git stash -q 2>/dev/null; ./mvnw -q dependency:tree -DoutputFile=/tmp/after.txt
git switch -q $BASE && ./mvnw -q dependency:tree -DoutputFile=/tmp/before.txt
git switch -q - ; diff /tmp/before.txt /tmp/after.txt | head -40
```

To'rtinchi qadam ayniqsa muhim: `pom.xml` da bitta versiya o'zgarsa, transitive bog'liqliklarda o'nlab o'zgarish bo'lishi mumkin va diff ularni ko'rsatmaydi.

### 4.8 Izohni qayerga va qanday qo'yish

Izohning joyi uning taqdirini belgilaydi. Satr izohi aniq, lekin kontekstdan ajralgan. Fayl izohi dizayn haqida gapirish uchun qulay. Umumiy izoh xulosa va asosiy savol uchun.

| Izoh turi | Joy | Misol |
| --- | --- | --- |
| Aniq xato | O'sha satr | "bu yerda `seats <= 0` tekshirilmagan" |
| Takrorlanadigan naqsh | Birinchi uchragan joy + "qolgan joylarda ham" | "shu mapping 3 joyda takrorlangan" |
| Dizayn savoli | Umumiy izoh | "refund tranzaksiya ichida - outbox ni muhokama qilaylik" |
| Yo'q narsa | Eng mos fayl yoki umumiy | "migratsiyaning orqaga yo'li yo'q" |
| Maqtov | O'sha satr | "bu yerda idempotentlik kaliti to'g'ri qo'yilgan" |

Oxirgi qatorni tashlab ketmaslik kerak. To'g'ri qilingan qiyin joyni ko'rsatish review ni tekshiruvdan muloqotga aylantiradi va keyingi PR da shu yondashuv takrorlanadi.

### 4.9 Izoh darajasini belgilash

Muallif izohni o'qiganida birinchi savoli: "bu majburiymi". Agar javob izohda bo'lmasa, muallif taxmin qiladi va taxmin ko'pincha noto'g'ri bo'ladi. Shu sababli har bir izoh prefiks oladi.

```text
blocker: idempotentlik kaliti bo'yicha UNIQUE indeks yo'q. Ikki parallel
         so'rov ikki bron yaratadi. Migratsiyaga unique indeks qo'shish kerak.

suggest: shu mapping uchun MapStruct ishlatsak, 40 satr qo'lda yozilgan
         setter yo'qoladi. Majburiy emas, lekin keyingi maydon qo'shilganda
         shu joy esdan chiqadi.

question: bu timeout 30 sekund qilib qo'yilgan. Tashqi servisning p99 i
          qancha? Agar 2 sekund bo'lsa, 30 sekund thread ni bekor egallaydi.

nit: `tmp` o'rniga `pendingItems` nomi aniqroq bo'ladi.

praise: `FOR UPDATE SKIP LOCKED` bu yerda to'g'ri tanlov, workerlar
        bir-birini kutmaydi.
```

`blocker` izohida har doim sabab va oqibat bo'lishi kerak, aks holda u buyruqqa o'xshaydi va qarshilik keltiradi. "Nima bo'ladi" tushuntirilsa, muallif ko'pincha o'zi yaxshiroq yechim taklif qiladi.

### 4.10 O'qish tezligini oshiradigan odatlar

Birinchi odat: fayllarni o'qish tartibini o'zgartirish (GitHub da "File filter" va "Viewed" belgilari bilan). Migratsiya va konfiguratsiyani birinchi ochish.

Ikkinchi odat: `Viewed` belgisini ishlatish - ikkinchi o'tishda nimaga qaytish kerakligini eslab turadi.

Uchinchi odat: generated va lock fayllarni filtrdan chiqarish. `package-lock.json` yoki `*.pb.java` ni o'qish - vaqtni yoqish.

To'rtinchi odat: diffni ikki oynada o'qish - biri diff, ikkinchisi to'liq fayl. Kontekst savollarining yarmi shu bilan yo'qoladi.

Beshinchi odat: review ni yozma xulosadan boshlab, keyin izohlarni yozish. Bu reviewer ni avval umumiy rasmni ko'rishga majbur qiladi.

### 4.11 Amalda qo'llash

- [ ] Sakkiz qadamli o'qish tartibini keyingi besh PR da qo'llab, migratsiya va konfiguratsiyani birinchi o'qishni odat qiling.
- [ ] `scripts/review-shape.sh` skriptini qo'shing: PR statistikasi, xavfli yo'llar, yangi/o'chirilgan fayllar.
- [ ] Har PR da faqat o'chirilgan satrlarni alohida o'qib chiqing va olib tashlangan `if`, `catch`, test uchun sabab so'rang.
- [ ] `git diff -M -C --find-copies-harder` ni refactoring PR larida ishlatib, diff hajmining qanchaga kamayishini ko'ring.
- [ ] Olib tashlangan tekshiruvlar uchun `git log -S` bilan ularning qo'shilish sababini toping.
- [ ] Yuqori xavfli PR larni lokalda `gh pr checkout` bilan olib, testlarni va migratsiyani ishga tushirishni majburiy qilib qo'ying.
- [ ] Bog'liqlik versiyasi o'zgargan PR larda `dependency:tree` farqini taqqoslang.
- [ ] Izoh prefikslari (`blocker`, `suggest`, `question`, `nit`, `praise`) ni jamoada kelishib, `REVIEW.md` ga yozing.

## 5. Mashina va odam: SonarQube dan oldin topish (Beating the Tools)

Reviewer uchun eng past hurmat keltiradigan holat - Sonar topgan narsani review ham topmaganligi. Eng yuqori qiymat keltiradigan holat - Sonar hech qachon topa olmaydigan narsani topish. Shu ikki qutb orasida reviewer ning haqiqiy darajasi aniqlanadi. Bu bob ikki narsani beradi: mashinadan oldinda yurish uchun qo'lda bajariladigan statik tahlil o'tishi, va mashina tuta olmaydigan sinflarning aniq ro'yxati. SonarQube ning ichki mexanikasi va qoidalar katalogi `java-spring-sonarqube.md` da, bu yerda faqat review stoli nuqtai nazari.

### 5.1 Nega Sonar dan oldin topish kerak

Birinchi sabab - vaqt. Sonar natijasi PR ochilgandan keyin 3-15 daqiqada keladi, ba'zi loyihalarda yarim soatdan keyin. Agar reviewer shu vaqtni kutsa, u kontekstni yo'qotadi. Agar kutmasa va keyin Sonar 12 ta issue chiqarsa, muallif ikkinchi davraga kiradi.

Ikkinchi sabab - signal sifati. Sonar `S2095` (resurs yopilmagan) deb aytadi, lekin "bu resurs yuk ostida 200 ta ulanishni egallaydi va pool ni to'ldiradi" demaydi. Qoida raqami xatoni ko'rsatadi, oqibatni ko'rsatmaydi. Muallif oqibatni bilmasa, u xatoni tuzatadi, lekin shu sinf xatoni qaytarmaslikni o'rganmaydi.

Uchinchi sabab - ishonch. Agar reviewer Sonar dan keyin hech narsa qo'shmasa, jamoa review ni kerak emas deb hisoblashni boshlaydi, va bu to'g'ri xulosa bo'ladi.

### 5.2 Mashina deterministik tutadigan narsalar

Bu ro'yxatni reviewer bilishi kerak, chunki unga vaqt sarflash - isrof. Bu narsalar PR ochilishidan oldin lokal `verify` da tutilishi kerak.

| Sinf | Misol | Instrument |
| --- | --- | --- |
| Uslub va format | Qavs joyi, import tartibi, satr uzunligi | spotless, checkstyle |
| Ishlatilmaydigan kod | O'qilmagan o'zgaruvchi, yetib bo'lmaydigan kod | kompilyator, Sonar |
| Aniq null yo'li | `null` qaytaradigan metod natijasi tekshirilmagan | Sonar, ErrorProne, SpotBugs |
| Resurs yopilmaganligi | `InputStream`, `Stream`, `Connection` | Sonar S2095 |
| Shubhali taqqoslash | `==` bilan `String`, `equals` bilan turli tur | ErrorProne |
| Mantiqiy doimiy shart | Har doim rost bo'lgan `if` | Sonar |
| Takroriy kod bloklari | Copy-paste bloklar | Sonar CPD |
| Murakkablik chegarasi | Cognitive complexity > 15 | Sonar |
| Ma'lum CVE | Zaif kutubxona versiyasi | dependency-check, Dependabot |
| Oddiy injection naqshlari | SQL satriga konkatenatsiya | Sonar, Semgrep |
| Qattiq yozilgan secret | Koddagi parol satri | gitleaks, Sonar |
| Standart API noto'g'ri ishlatilishi | `Optional.get()` tekshirmasdan | Sonar, ErrorProne |

Xulosa: bu jadvaldagi hech narsa review izohiga aylanmasligi kerak. Agar aylansa, muammo instrumentda, odamda emas. To'g'ri javob - qoidani CI ga qo'yish, izoh yozmaslik.

### 5.3 Mashina tuta olmaydigan narsalar

Bu reviewer ning haqiqiy ish maydoni. Hamma bandning umumiy xususiyati bor: ularni topish uchun niyat, domen yoki tizim konteksti kerak, ya'ni koddan tashqaridagi bilim.

| Sinf | Misol | Nega mashina ko'rmaydi |
| --- | --- | --- |
| Noto'g'ri biznes qoidasi | Chegirma 10% emas, 15% bo'lishi kerak | Talab kodda yo'q |
| Buzilgan invariant | Qoldiq manfiyga tushishi mumkin | Invariant e'lon qilinmagan |
| Yo'q kod | Avtorizatsiya tekshiruvi qo'yilmagan | Yo'q narsani ko'rsatish uchun model kerak |
| Poyga holati | Tekshir-keyin-yoz ikki instansda | Ish vaqti xulqi, statik emas |
| Noto'g'ri abstraksiya | Interfeysning bitta implementatsiyasi va soxta moslashuvchanlik | Dizayn qarori |
| Pattern noto'g'ri qo'llanishi | Strategy o'rniga `if` zinapoyasi, yoki teskarisi | Kontekstga bog'liq |
| Tranzaksiya chegarasi noto'g'ri | Tashqi chaqiruv tranzaksiya ichida | Semantika, qoida emas |
| Ma'lumot modeli xatosi | Pul `double` da, vaqt `LocalDateTime` da | Domen bilimi |
| Yetarsiz test holati | Test bor, lekin chegaraviy qiymat yo'q | Qamrov o'lchanadi, to'g'rilik o'lchanmaydi |
| Yolg'on test | Assertion yo'q yoki `assertNotNull` bilan tugaydi | Test kompilyatsiya bo'ladi va o'tadi |
| Avtorizatsiya mantiqi teshigi | Foydalanuvchi boshqa ID ni so'rasa | Faqat domen bilan aniqlanadi |
| Migratsiya operatsion xavfi | `ALTER` 12 mln qatorni qulflaydi | Jadval hajmi kodda yo'q |
| Observability bo'shlig'i | Xato bo'lsa, bilib bo'lmaydi | O'lchov talabi kodda yo'q |
| Orqaga moslik buzilishi | Maydon nomi o'zgargan, eski mijoz bor | Mijozlar kodda yo'q |
| Performance regressiyasi | Siklda tashqi chaqiruv | Yuk va hajmga bog'liq |

### 5.4 Qo'lda statik tahlil o'tishi: o'n to'rt savol

Bu ro'yxat Sonar dan oldin bajariladi va taxminan 10 daqiqa oladi. Maqsad - Sonar chiqaradigan issue larning katta qismini oldin ko'rish va ularni oqibat bilan birga aytish.

1. Har bir yangi `public` metod kirishini tekshiradimi, yoki tekshirish chaqiruvchida qoldirilganmi.
2. Qaytarilgan `null` bormi, va u `Optional` bilan almashtirilishi kerakmi.
3. Tashqi manbadan kelgan qiymat `Optional.get()`, `orElseThrow()` yoki `charAt(0)` bilan to'g'ridan-to'g'ri ishlatilganmi.
4. Yangi ochilgan resurs (`Stream`, `InputStream`, `Connection`, `ExecutorService`) `try-with-resources` ichida yoki `close` yo'li borligi ko'rinadimi.
5. `catch` bloklari qanday: `Exception` ni yutib yuborgan yoki kontekstsiz qayta tashlagan joy bormi.
6. Siklda tashqi chaqiruv (DB, HTTP, kesh) bormi.
7. Shartlar soni: eng katta metodda nechta shoxlanish bor, 15 dan oshadimi.
8. Takrorlangan blok bormi: xuddi shu 10 satr boshqa faylda ham turganmi.
9. `String` konkatenatsiyasi bilan quriladigan so'rov yoki buyruq bormi.
10. Sanab o'tiladigan holatlar to'liqmi: `switch` da `default` bormi, yangi enum qiymati qo'shilsa nima bo'ladi.
11. Taqqoslashlar: `equals`/`hashCode` juftligi buzilmaganmi, `compareTo` bilan `equals` mos keladimi.
12. Sonlar: butun sonlar bo'linishi, `int` ga sig'may qolish, pul uchun `double` ishlatilishi bormi.
13. Vaqt: `new Date()`, `LocalDateTime.now()` to'g'ridan-to'g'ri ishlatilganmi (test qilinmaydigan va zonasiz).
14. Mutable holat: statik o'zgaruvchi, umumiy `HashMap`, `SimpleDateFormat` bean sifatida bormi.

```java
// Shu o'n to'rt savolni bitta misolda ko'rish. Sonar bu kodda 6-7 issue
// topadi, lekin reviewer ularni oqibat bilan aytadi.
@Service
public class ReportService {

    // (14) Mutable umumiy holat: SimpleDateFormat thread-safe emas.
    //      Ikki parallel so'rov buzilgan sana beradi yoki istisno tashlaydi.
    private static final SimpleDateFormat FMT = new SimpleDateFormat("yyyy-MM-dd");

    private final JdbcTemplate jdbc;
    private final RateClient rates;

    public ReportService(JdbcTemplate jdbc, RateClient rates) {
        this.jdbc = jdbc;
        this.rates = rates;
    }

    public List<Row> build(String from, String to, String sortBy) {
        // (1) Kirish tekshirilmagan, (9) so'rov konkatenatsiya bilan qurilgan.
        //     sortBy foydalanuvchidan kelsa - SQL injection.
        String sql = "SELECT id, amount, currency, created_at FROM payments "
                   + "WHERE created_at BETWEEN '" + from + "' AND '" + to + "' "
                   + "ORDER BY " + sortBy;

        List<Map<String, Object>> raw = jdbc.queryForList(sql);
        List<Row> out = new ArrayList<>();

        for (Map<String, Object> r : raw) {
            // (6) Siklda tashqi HTTP chaqiruvi: 10 000 qator = 10 000 so'rov.
            //     p99 30 ms bo'lsa ham, bu 5 daqiqa.
            BigDecimal rate = rates.rateFor((String) r.get("currency"));

            // (12) Pul hisobi double orqali o'tyapti: aniqlik yo'qoladi.
            double amount = ((Number) r.get("amount")).doubleValue()
                          * rate.doubleValue();

            // (13) Zona yo'q: server zonasiga bog'liq natija.
            out.add(new Row(FMT.format(r.get("created_at")), amount));
        }
        return out;
    }
}
```

Shu kodga review izohi Sonar tilida emas, oqibat tilida yoziladi:

```text
blocker: sortBy to'g'ridan-to'g'ri ORDER BY ga qo'yilgan. Agar u so'rov
         parametridan kelsa, bu SQL injection: `1; DROP TABLE ...` emas,
         lekin `(SELECT ...)` bilan ma'lumot chiqarib olish mumkin.
         Yechim: ruxsat etilgan ustunlar ro'yxati (whitelist) + enum.

blocker: rates.rateFor sikl ichida chaqirilgan. 10 000 qatorli hisobotda bu
         10 000 HTTP so'rov. Valyutalar soni 10 tadan oshmaydi - oldin bir
         marta olib, Map ga joylash kerak.

blocker: pul hisobi double da. 0.1 + 0.2 muammosi hisobotda markazlashgan
         xatoga olib keladi. BigDecimal va aniq scale kerak.

suggest: SimpleDateFormat static - thread-safe emas. DateTimeFormatter
         (immutable) ga o'tkazish kerak.

question: created_at BETWEEN ikki satr bilan solishtirilgan. Ustun turi
          timestamptz bo'lsa, zona qanday hisobga olinadi?
```

### 5.5 Cognitive complexity ni ko'zda hisoblash

Sonar `cognitive complexity` ni hisoblaydi, lekin reviewer uni chamalab bilishi kerak. Hisob oddiy: har bir shoxlanish bir ball, ichma-ich joylashgan shoxlanish chuqurligicha ko'p ball, `else if` zanjiri har bir bo'g'in uchun ball, `catch` bir ball, uzilish operatorlari (`break`, `continue` yorliq bilan) ball.

Amaliy mezon: bitta ekranga sig'maydigan va uch darajadan chuqur ichma-ich shartga ega metod allaqachon chegaradan o'tgan. Sonar aytishini kutish shart emas.

Muhim nuans: murakkablikni kamaytirish uchun metodni ikkiga bo'lish ko'rsatkichni yaxshilaydi, lekin tushunarlilikni yaxshilamasligi mumkin. Agar ajratilgan metod `part1`, `part2` deb nomlangan bo'lsa, bu ko'rsatkichni aldash. To'g'ri yechim - domen tilidagi nom bilan ajratish yoki shoxlanishni polimorfizm bilan almashtirish (10-bobga qarang).

### 5.6 Null yo'lini qo'lda kuzatish

Statik tahlil null ni faqat bitta metod ichida ishonchli kuzatadi. Metoddan metodga o'tgan null uchun annotatsiya kerak. Shu sababli reviewer null ni chegaralarda kuzatadi.

```java
// Null chegaralarini aniq qilish: review da shu uch naqsh talab qilinadi.

// 1) Paket darajasida standart: hamma narsa null bo'lmaydi, istisno belgilanadi.
//    package-info.java
@NullMarked
package com.acme.order.domain;   // JSpecify (yoki @NonNullApi - Spring)

// 2) Qaytish turida null yo'q: Optional yoki bo'sh to'plam.
public interface OrderRepository {
    Optional<Order> findByNumber(String number);   // yaxshi
    List<Order> findOpen();                        // bo'sh ro'yxat, null emas
    // Order findByNumber(String n);               // yomon: null qaytarishi mumkin
}

// 3) Kirishda tekshiruv chegarada bir marta, keyin ishonch.
public Receipt charge(ChargeCommand cmd) {
    Objects.requireNonNull(cmd, "cmd");
    // Domen obyekti ichida null bo'lmasligi konstruktorda kafolatlanadi,
    // shuning uchun quyidagi kodda null tekshiruvi takrorlanmaydi.
    return gateway.charge(cmd.amount(), cmd.card());
}

// Review savoli: tashqi JSON dan kelgan DTO da @NotNull bormi, yoki null
// domenga kirib ketadimi? Jackson bo'sh maydonni null qilib qoldiradi.
public record ChargeRequest(
        @NotNull @Positive BigDecimal amount,
        @NotBlank String currency,
        @NotNull @Valid CardRequest card) { }
```

### 5.7 Resurs oqishini ko'rish

Sonar yopilmagan `Stream` ni topadi, lekin "yopildi, lekin kech yopildi" holatini topmaydi. Review da uch savol beriladi: resurs kim tomonidan ochildi, kim yopadi, va yopilish istisno bo'lganda ham kafolatlanganmi.

```java
// PostgreSQL bilan oqimli o'qish: resurs oqishining klassik joyi.

// Yomon: Stream yopilmaydi, kursor va ulanish ushlab qolinadi.
@Transactional(readOnly = true)
public void exportAll(Writer out) {
    orders.streamAllByStatus(OPEN)        // Stream<Order> qaytaradi
          .forEach(o -> write(out, o));   // istisno bo'lsa - oqim ochiq qoladi
}

// Yaxshi: try-with-resources + fetch size + statelessSession/clear.
@Transactional(readOnly = true)
public void exportAll(Writer out) {
    try (Stream<Order> rows = orders.streamAllByStatus(OPEN)) {
        rows.forEach(o -> {
            write(out, o);
            // Hibernate birinchi darajali keshi o'smasligi uchun: aks holda
            // 2 mln qator heap ga to'planadi va OOM bo'ladi.
            em.detach(o);
        });
    }
}
// Review izohi: @Transactional(readOnly = true) va fetchSize birga kerak.
// PostgreSQL JDBC kursor rejimiga faqat autoCommit=false da o'tadi,
// aks holda butun natija klientga tortiladi (hujjat: architect, JDBC bo'limi).
```

### 5.8 Security hotspot: mashina belgilaydi, qarorni odam qabul qiladi

Sonar da "security hotspot" degan toifa bor: bu xato emas, qaror talab qiladigan joy. Masalan `Random` ishlatilishi, HTTP header o'qilishi, fayl yo'li qurilishi. Mashina ularni belgilaydi, lekin xavfli yoki xavfsiz ekanini kontekst hal qiladi.

Reviewer uchun qoida: hotspot ko'rsatilganda "bu yerda tashqi, ishonilmaydigan ma'lumot bormi" degan savolga javob yozib qoldirish kerak. Javob izohda qolsa, keyingi reviewer o'sha ishni qaytadan qilmaydi. Xavfsizlik review ning to'liq metodikasi VI bo'limda.

### 5.9 Coverage raqami aldaganda

Coverage - kod bajarildimi degan savolga javob beradi, to'g'ri ishladimi degan savolga javob bermaydi. Shu sababli reviewer coverage foiziga qaramaydi, assertion larga qaraydi.

```java
// 100% line coverage beradigan, lekin hech narsani tekshirmaydigan test.
@Test
void calculatesDiscount() {
    Order order = new Order(BigDecimal.valueOf(1000), CustomerTier.GOLD);
    BigDecimal result = calculator.discountFor(order);
    assertThat(result).isNotNull();          // yolg'on ishonch
}

// Review izohi (blocker): assertion qiymatni tekshirmaydi. Bu test
// discountFor ichidagi har qanday o'zgarishda ham o'tadi. Kutilgan qiymat
// yozilishi kerak, va GOLD/SILVER/chegaraviy summalar uchun alohida holat.

// To'g'ri shakl: aniq qiymat va chegaralar.
@ParameterizedTest
@CsvSource({
    "999.99, GOLD,   0.00",   // chegaradan past: chegirma yo'q
    "1000.00, GOLD, 150.00",  // chegara aynan: 15%
    "1000.00, SILVER, 50.00", // boshqa daraja
    "0.00,   GOLD,   0.00"    // nol summa
})
void discountMatchesTable(BigDecimal total, CustomerTier tier, BigDecimal expected) {
    assertThat(calculator.discountFor(new Order(total, tier)))
        .isEqualByComparingTo(expected);
}
```

Coverage raqami foydali bo'ladigan bitta holat bor: yangi kod uchun coverage nolga teng bo'lsa, demak test umuman yozilmagan. Qolgan hamma holatda raqam emas, test holatlarining to'liqligi muhim. Test to'liqligini review qilish VII bo'limda batafsil.

### 5.10 Shovqinni kamaytirish va izohni qoidaga aylantirish

Reviewer bir xil izohni uchinchi marta yozayotgan bo'lsa, u noto'g'ri ish qilyapti. To'g'ri harakat - izohni avtomatik qoidaga aylantirish. Bu review ning eng yuqori qaytimli ishi: bir marta sarflangan vaqt keyingi barcha PR larda tejaladi.

```java
// Takrorlanadigan arxitektura izohini ArchUnit qoidasiga aylantirish.
// "Controller to'g'ridan-to'g'ri repository ga murojaat qilmasligi kerak"
// izohini uchinchi marta yozish o'rniga:
@AnalyzeClasses(packages = "com.acme", importOptions = DoNotIncludeTests.class)
class ArchitectureRulesTest {

    @ArchTest
    static final ArchRule controllers_do_not_touch_repositories =
        noClasses().that().resideInAPackage("..web..")
                   .should().dependOnClassesThat().resideInAPackage("..repository..")
                   .because("web qatlami application servis orqali o'tishi kerak");

    @ArchTest
    static final ArchRule domain_is_framework_free =
        noClasses().that().resideInAPackage("..domain..")
                   .should().dependOnClassesThat()
                   .resideInAnyPackage("org.springframework..", "jakarta.persistence..")
                   .because("domen frameworkdan mustaqil bo'lsin");

    @ArchTest
    static final ArchRule no_field_injection =
        noFields().should().beAnnotatedWith(Autowired.class)
                  .because("konstruktor orqali inyeksiya: testlanadigan va immutable");

    @ArchTest
    static final ArchRule transactional_only_in_application_layer =
        methodsThat(are(annotatedWith(Transactional.class)))
            .should().beDeclaredInClassesThat().resideInAPackage("..application..")
            .because("tranzaksiya chegarasi bitta qatlamda turishi kerak");
}
```

```xml
<!-- Takrorlanadigan Java darajasidagi izohni kompilyatsiya xatosiga aylantirish.
     ErrorProne review dan oldin, kompilyatsiya paytida gapiradi. -->
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <arg>-XDcompilePolicy=simple</arg>
      <arg>--should-stop=ifError=FLOW</arg>
      <!-- Pul double da, Date ishlatilishi, == bilan String taqqoslash -->
      <arg>-Xplugin:ErrorProne
           -Xep:MissingOverride:ERROR
           -Xep:ReferenceEquality:ERROR
           -Xep:FallThrough:ERROR
           -Xep:OptionalGetWithoutIsPresent:ERROR
           -Xep:StreamResourceLeak:ERROR</arg>
    </compilerArgs>
  </configuration>
</plugin>
```

Qoidaga aylantirishning chegarasi ham bor: kontekstga bog'liq qarorni qoida qilib qo'yish shovqin keltiradi va jamoa qoidani o'chirib tashlaydi. Mezon oddiy - agar istisno 10 foizdan ko'p holatda kerak bo'lsa, bu qoida emas, muhokama mavzusi.

### 5.11 Amalda qo'llash

- [ ] Oxirgi 20 PR dagi Sonar issue larini sanab, ularning qanchasi review izohida ham aytilganini tekshiring. Nisbat past bo'lsa, 14 savolli o'tishni joriy qiling.
- [ ] 14 savolli qo'lda statik tahlil ro'yxatini `REVIEW.md` ga qo'shing va uni yuqori xavfli PR larda majburiy qiling.
- [ ] ErrorProne ni `maven-compiler-plugin` ga ulab, kamida `ReferenceEquality`, `OptionalGetWithoutIsPresent`, `StreamResourceLeak` ni `ERROR` darajasiga qo'ying.
- [ ] Takrorlanadigan uchta arxitektura izohini ArchUnit testiga aylantirib, CI ga qo'shing.
- [ ] Loyihadagi `SimpleDateFormat`, `new Date()`, `double` bilan pul hisobini grep bilan topib, ro'yxat tuzing va qoidaga aylantiring.
- [ ] `package-info.java` ga `@NullMarked` (yoki `@NonNullApi`) qo'yib, null chegarasini e'lon qiling.
- [ ] Yangi kod coverage i emas, yangi testlardagi assertion sifatini tekshirishni review bandiga aylantiring: `assertNotNull` bilan tugaydigan testlarni toping.
- [ ] Sonar hotspot lari uchun "tashqi ma'lumot bormi" javobini izohda yozib qoldirish qoidasini joriy qiling.

# II. Arxitektura, dizayn va clean code review

## 6. Arxitektura review: qatlam, chegara, bog'liqlik yo'nalishi (Architecture in a Diff)

Arxitektura PR da bitta diagramma sifatida ko'rinmaydi. U mayda belgilar orqali ko'rinadi: yangi import, yangi konstruktor parametri, yangi paket, bir qatlamdan boshqasiga o'tgan chaqiruv. Arxitektura buzilishi hech qachon bitta PR da sodir bo'lmaydi - u yuzta PR da bittadan satr bilan sodir bo'ladi. Shu sababli arxitektura review ning asosiy quroli - yo'nalishni kuzatish. Arxitektura qarorlarining o'zi (chegarani qayerdan o'tkazish, monolit yoki servis) `java-spring-architect-mindset.md` da, bu yerda faqat diffdan o'qish.

### 6.1 Importlar - arxitekturaning eng aniq ko'rsatkichi

Fayl boshidagi importlar ro'yxati shu klassning tizimdagi o'rnini aytadi. Domen klassida `org.springframework.web` importi bo'lsa, qatlam buzilgan. Repository da `javax.servlet` bo'lsa, so'rov konteksti ma'lumot qatlamiga tushgan. Entity da `com.fasterxml.jackson` bo'lsa, tashqi shakl ma'lumot modeliga yopishgan.

```bash
# Diffda yangi qo'shilgan importlarni ko'rish: arxitektura review ning
# eng tez va eng foydali qadami.
git diff origin/main...HEAD -- '*.java' \
  | grep -E '^\+import' | sort | uniq -c | sort -rn

# Qatlam buzilishini qidirish.
git diff origin/main...HEAD -- 'src/main/java/**/domain/**' \
  | grep -E '^\+import (org\.springframework|jakarta\.persistence|com\.fasterxml)'

# Teskari yo'nalish: ichki qatlam tashqarini bilib qolgan.
grep -rn --include='*.java' 'import .*\.web\.' src/main/java/**/domain/ 2>/dev/null
```

| Diffda ko'rilgan import | Qayerda | Nimani bildiradi |
| --- | --- | --- |
| `org.springframework.web.*` | domain | Qatlam buzilgan, domen HTTP ni biladi |
| `jakarta.persistence.*` | domain | Domen ORM ga yopishgan (agar toza domen tanlangan bo'lsa) |
| `com.fasterxml.jackson.*` | entity | Tashqi JSON shakli jadval modeliga bog'langan |
| `...repository.*` | web/controller | Servis qatlami chetlab o'tilgan |
| Boshqa modulning `internal` paketi | har qanday joy | Modul chegarasi teshilgan |
| `java.sql.*` | service | Ma'lumot qatlami oqib chiqqan |
| `org.apache.http.*` | domain | Tashqi integratsiya domenga kirgan |

### 6.2 Bog'liqlik yo'nalishi: ichki qatlam tashqarini bilmaydi

Qatlamli arxitekturaning yagona qattiq qoidasi - bog'liqlik ichkariga qarab yo'naladi. Web application ni biladi, application domenni biladi, domen hech kimni bilmaydi. Infratuzilma domen e'lon qilgan interfeysni amalga oshiradi.

Review da bu qoida bitta savol bilan tekshiriladi: yangi `import` yoki konstruktor parametri bog'liqlikni ichkariga yoki tashqariga yo'naltirdimi.

```java
// Buzilish: domen servis infratuzilma klassiga bog'langan.
package com.acme.order.domain;

import com.acme.order.infra.sms.TwilioSmsClient;   // yo'nalish tashqariga

public class OrderNotifier {
    private final TwilioSmsClient sms;             // domen vendorni biladi
    public void notifyShipped(Order order) {
        sms.send(order.getPhone(), "Buyurtma jo'natildi");
    }
}

// To'g'ri: domen o'z ehtiyojini interfeys bilan e'lon qiladi (port),
// implementatsiya tashqarida turadi (adapter). Interfeys foydalanuvchi
// tomonda e'lon qilinadi - shuning uchun u domain paketida.
package com.acme.order.domain;

public interface CustomerNotifications {               // port, domen tilida
    void shipped(OrderId orderId, PhoneNumber to);
}

package com.acme.order.infra.sms;

@Component
class TwilioNotifications implements CustomerNotifications {   // adapter
    private final TwilioClient client;
    @Override public void shipped(OrderId orderId, PhoneNumber to) {
        client.send(to.value(), messages.shipped(orderId));
    }
}
// Review foydasi: domen testda soxta implementatsiya bilan ishlaydi,
// vendor almashtirilsa domen tegilmaydi, va interfeys nomi domen tilida.
```

Diqqat: bu yerda muhimi interfeys borligi emas, interfeys qayerda turgani. `infra` paketidagi interfeys va uning yonidagi yagona implementatsiyasi hech narsani yechmaydi - bu 7-bobdagi "soxta abstraksiya" holati.

### 6.3 Yangi paket va yangi modul - chegara haqida qaror

Diffda yangi paket paydo bo'lishi arxitektura qarori. Review savollari: bu paket nima bo'yicha ajratilgan (texnik qatlam yoki biznes xususiyati), uning tashqi yuzasi qanday, va kim unga kirish huquqiga ega.

Amaliy mezon - paket ichidagi klasslarning qanchasi `public`. Agar hammasi `public` bo'lsa, paket chegara emas, shunchaki papka. Haqiqiy chegara bir-ikki `public` tur va qolgan hammasi paket-private bo'lgan holatda paydo bo'ladi.

```java
// Modul chegarasini kod bilan majburlash: Spring Modulith yoki
// paket-private ko'rinish. Review da shu belgilar izlanadi.

// com/acme/billing/package-info.java
@ApplicationModule(
    allowedDependencies = { "shared::money", "customer::api" }   // aniq ro'yxat
)
package com.acme.billing;

// Modul ichidagi klasslar: faqat API public.
package com.acme.billing;
public interface BillingApi {                   // yagona kirish nuqtasi
    Invoice issue(IssueInvoiceCommand cmd);
}

package com.acme.billing.internal;
class InvoiceNumberGenerator { }                // paket-private: tashqaridan ko'rinmaydi
class VatCalculator { }                         // ichki detal

// Chegarani test bilan tekshirish (ArchUnit yoki Modulith).
@Test
void moduleBoundariesAreRespected() {
    ApplicationModules.of(Application.class).verify();   // Spring Modulith
}
```

### 6.4 Yangi tashqi bog'liqlik - eng kam baholangan arxitektura qarori

`pom.xml` ga bitta qator qo'shilishi diffda eng kichik o'zgarish, lekin oqibati eng uzoq muddatli: yangi kutubxona yangilanish majburiyati, CVE xavfi, transitive konflikt va litsenziya masalasi olib keladi.

| Review savoli | Nega muhim |
| --- | --- |
| Shu vazifa mavjud bog'liqlik bilan bajariladimi | Ko'pincha Spring yoki JDK da allaqachon bor |
| Kutubxona qancha faol: oxirgi reliz qachon | Tashlab ketilgan kutubxona kelajakdagi muammo |
| Transitive nimani olib keladi | Konflikt va kattalik |
| Litsenziya mos keladimi | GPL/AGPL yuridik masala |
| Necha satr kod uchun olinyapti | 20 satr uchun kutubxona - noto'g'ri savdo |
| Kim yangilaydi | Egasi yo'q bog'liqlik eskiradi |

```bash
# Yangi bog'liqlik haqiqatda nimani olib keldi.
./mvnw -q dependency:tree -Dincludes=':::' | grep -A20 'yangi-kutubxona'

# Konflikt bormi va qaysi versiya g'olib chiqqan.
./mvnw dependency:tree -Dverbose | grep -E 'omitted|conflict' | head -20

# Mavjud imkoniyatlar bilan bajariladimi: JDK va Spring da bormi.
# Masalan JSON uchun Jackson allaqachon bor, HTTP uchun RestClient bor,
# retry uchun Spring Retry yoki Resilience4j allaqachon loyihada bo'lishi mumkin.
grep -rn 'artifactId' pom.xml | sort | uniq | head -40
```

### 6.5 Arxitektura eroziyasini diffdan ko'rish

Eroziya bitta PR da ko'rinmaydi, lekin uning belgilari ko'rinadi. Quyidagi belgilar har biri alohida zararsiz, birgalikda esa tizim yo'nalishini o'zgartiradi.

| Belgi | Nimani bildiradi | Review javobi |
| --- | --- | --- |
| Konstruktor parametrlari soni 6 dan oshdi | Klass juda ko'p narsani biladi | Mas'uliyatni bo'lish yoki agregat kiritish |
| `@Autowired` maydon yoki `ApplicationContext` inyeksiyasi | Bog'liqlik yashiringan | Konstruktor inyeksiyasi |
| `static` yordamchi klassga yangi metod | Holatsiz "xudo klass" o'sib boryapti | Domen obyektiga ko'chirish |
| `util`, `common`, `helper`, `manager` paketi o'sdi | Egasi yo'q kod to'planyapti | Domen tilida nomlangan joyga ko'chirish |
| `shared` moduldagi klass biznes qoidasini bildi | Umumiy modul domenga aylanyapti | Qoidani egasiga qaytarish |
| Entity ga yangi `@Transient` hisob maydoni | Ma'lumot modeli hisob mantiqini yutyapti | Domen servisi yoki value object |
| DTO va entity bir xil klass | Tashqi shakl va saqlash bir-biriga qulflangan | Ajratish |
| Yangi `if (featureEnabled)` shoxlari | Vaqtinchalik flag doimiy bo'lib qolyapti | Flag ning o'chirilish sanasi |
| Boshqa modul jadvaliga `JOIN` | Sxema chegarasi teshilgan | API orqali o'qish yoki o'qish modeli |
| Sikl bog'liqlik (A -> B -> A) | Modullar aslida bitta | Birlashtirish yoki event bilan uzish |

```java
// Sikl bog'liqlikni ArchUnit bilan taqiqlash: eroziyaning eng aniq shakli.
@ArchTest
static final ArchRule no_cycles =
    slices().matching("com.acme.(*)..").should().beFreeOfCycles();

// "Util" to'planishini cheklash: yangi util klass qo'shilishini sekinlashtirish.
@ArchTest
static final ArchRule no_new_util_classes =
    noClasses().that().haveSimpleNameEndingWith("Util")
               .or().haveSimpleNameEndingWith("Helper")
               .or().haveSimpleNameEndingWith("Manager")
               .should().bePublic()
               .because("domen tilida nomlangan joyga tegishli bo'lsin");
```

### 6.6 Qatlam o'tkazib yuborilishi (layer skipping)

Controller to'g'ridan-to'g'ri repository ga murojaat qilsa, kod ishlaydi va test ham o'tadi. Muammo keyinroq chiqadi: tranzaksiya chegarasi yo'qoladi, avtorizatsiya tekshiruvi chetlab o'tiladi, va biznes qoidasi ikki joyda takrorlanadi.

```java
// Diffda uchraydigan shakl: tezkor yechim.
@RestController
class OrderController {
    private final OrderRepository orders;          // qatlam o'tkazib yuborilgan

    @GetMapping("/orders/{id}")
    OrderDto get(@PathVariable long id) {
        // Avtorizatsiya yo'q: har kim har qanday buyurtmani ko'radi.
        // Lazy maydon ochilsa - LazyInitializationException yoki N+1.
        return OrderDto.from(orders.findById(id).orElseThrow());
    }
}

// Review izohi: ikkita oqibat bor, ikkisi ham diffda ko'rinmaydi.
// 1) Avtorizatsiya: shu buyurtma so'rovchiga tegishlimi - tekshirilmagan.
// 2) Tranzaksiya: controller da tranzaksiya yo'q, OSIV yopilgan bo'lsa
//    lazy kolleksiya istisno tashlaydi, ochiq bo'lsa ulanish view gacha
//    egallanadi.

// To'g'ri: application servis chegarani egallaydi.
@Service
class OrderQueries {
    @Transactional(readOnly = true)
    @PreAuthorize("@orderAccess.canRead(#id, authentication)")
    public OrderDto byId(long id) {
        return orders.findProjectionById(id).orElseThrow(OrderNotFound::new);
    }
}
```

### 6.7 Chegaradan o'tadigan ma'lumot shakli

Arxitektura chegarasi ma'lumot shaklida ham ko'rinadi. Entity ni controller dan qaytarish - chegarani yo'q qilish: jadval ustuni nomi tashqi API shakliga aylanadi va keyin uni o'zgartirish breaking change bo'ladi.

| Chegaradan o'tayotgan narsa | Xavf | To'g'ri shakl |
| --- | --- | --- |
| JPA entity controller javobida | Jadval sxemasi API ga yopishadi, lazy proxy serializatsiyasi | Alohida DTO yoki record |
| Entity Kafka xabarida | Boshqa servis sxemangizga bog'lanadi | Aniq event sxemasi |
| `Map<String,Object>` servis chegarasida | Shartnoma yo'q, xato kompilyatsiyada tutilmaydi | Tipli record |
| Enum ordinal qiymati tashqariga | Tartib o'zgarsa ma'no o'zgaradi | Nom bo'yicha satr |
| Ichki istisno turlari tashqariga | Implementatsiya oqib chiqadi | Xato kodi va shakli |
| `LocalDateTime` API da (zonasiz) | Mijoz zonani bilmaydi | `Instant` yoki `OffsetDateTime` |

### 6.8 Hisob mantiqi qayerda turadi

Bitta hisob uch joyda bajarilishi mumkin: SQL da, Java da, yoki frontendda. Diffda yangi hisob paydo bo'lsa, review savoli - nega shu joyda.

| Joy | Qachon to'g'ri | Xavf |
| --- | --- | --- |
| SQL (aggregate, window) | Katta hajmni filtrlash va yig'ish | Mantiq yashiringan, test qiyin, portativ emas |
| Domen (Java) | Biznes qoidasi, invariant | Katta hajmni Java ga tortish |
| View/DTO mapping | Faqat formatlash | Biznes qoidasi taqdimotga tushib qolishi |
| Frontend | Faqat ko'rinish | Qoida ikki joyda, mos kelmaydi |

Qattiq qoida: pul, soliq, chegirma va huquq (kim nimani ko'rishi) hisobi hech qachon frontendda yoki faqat SQL da bo'lmaydi. Ular domen ichida, test bilan qoplangan joyda turishi kerak.

### 6.9 Modullar orasidagi muloqot shakli

Diffda yangi modullar aro chaqiruv paydo bo'lsa, uning shakli arxitektura qarori: sinxron chaqiruv, event, yoki umumiy ma'lumot.

```java
// Uch shakl va ularning review savollari.

// 1) Sinxron chaqiruv: eng oson, eng qattiq bog'liqlik.
//    Review savoli: chaqirilgan modul yiqilsa, bu operatsiya to'xtashi kerakmi?
Invoice invoice = billingApi.issue(cmd);     // billing yiqilsa - order ham yiqiladi

// 2) Domen eventi: bo'shashgan bog'liqlik, lekin yetkazish kafolati kerak.
//    Review savoli: event yo'qolsa nima bo'ladi? Tranzaksiya bilan atomikmi?
events.publish(new OrderPlaced(order.id(), order.total()));
// Agar bu @TransactionalEventListener(AFTER_COMMIT) bilan ishlanmasa va
// outbox bo'lmasa - commit o'tib, event yo'qolishi mumkin (27-bob).

// 3) Umumiy jadval: eng yomon shakl, eng tez yechim.
//    Review javobi: boshqa modulning jadvaliga yozish - chegarani yo'q qilish.
jdbc.update("UPDATE billing_invoice SET status = ? WHERE id = ?", ...);  // blocker
```

### 6.10 Arxitektura izohini qanday yozish

Arxitektura izohi eng ko'p qarshilik keltiradigan izoh turi, chunki u ko'p ishni qayta qilishni talab qiladi. Shu sababli uning shakli muhim: oqibatni raqamda ko'rsatish, bitta alternativani taklif qilish va kelishuv nuqtasini aytish.

```text
# Yomon shakl: baholash, oqibat yo'q, alternativa yo'q.
"Bu dizayn noto'g'ri, clean architecture ga mos emas."

# Yaxshi shakl: belgi -> oqibat -> alternativa -> kelishuv.
suggest (arxitektura): OrderNotifier domen paketida TwilioSmsClient ga
bog'langan.

Oqibati: (1) domen testi uchun Twilio mock kerak bo'ladi, hozir 3 ta testda
shunday qilingan; (2) SMS provayderi almashtirilsa, domen kodi o'zgaradi;
(3) ArchUnit qoidamiz "domain framework-free" buni keyinroq bloklaydi.

Alternativa: domenda CustomerNotifications interfeysi, infra da Twilio
adapteri. O'zgarish hajmi: 1 interfeys + 1 klass ko'chirish, taxminan 30 satr.

Agar bu PR da qilish katta bo'lsa, tiket ochib shu sprintda yopsak bo'ladi -
lekin yangi kod shu yo'nalishda yozilmasa, keyingi oyda 10 joyda shunday
bo'ladi.
```

### 6.11 Amalda qo'llash

- [ ] Review ning birinchi qadamiga "diffdagi yangi importlar" tekshiruvini qo'shing va qatlam buzilishini grep bilan avtomatlashtiring.
- [ ] Qatlam qoidalarini ArchUnit testiga yozing: `domain` framework-free, `web` repository ga tegmaydi, `@Transactional` faqat application qatlamida.
- [ ] `slices().should().beFreeOfCycles()` qoidasini qo'shib, mavjud sikl bog'liqliklar ro'yxatini chiqaring.
- [ ] Loyihadagi paketlarni ko'rib, har birida nechta `public` klass borligini sanang: chegara bo'lishi kerak bo'lgan paketlarda ortiqcha `public` larni paket-private ga o'tkazing.
- [ ] Yangi bog'liqlik uchun PR shabloniga 6 savolli ro'yxat qo'shing (mavjud imkoniyat, faollik, transitive, litsenziya, hajm, egasi).
- [ ] Controller javoblarida JPA entity qaytarilgan joylarni toping va DTO ga o'tkazishni rejalashtiring.
- [ ] Eroziya belgilari jadvalidan uchtasini tanlab, repoda qanchaligini o'lchang: konstruktor parametrlari 6 dan ko'p klasslar, `Util`/`Helper` klasslar soni, `@Autowired` maydonlar.
- [ ] Modullar aro umumiy jadvalga yozadigan joylarni toping va ularni API yoki event ga o'tkazish tiketini ochingg.

## 7. Bog'liqlik, kohéziya va abstraksiya review (Coupling, Cohesion, Abstraction)

Arxitektura buzilishi odatda bitta klassning ichida boshlanadi: klass o'ziga tegishli bo'lmagan narsani bilib qoladi, yoki bir-biriga aloqasi yo'q ikki narsa bir joyga tushadi. Bu bob shu ikki kuchni - bog'liqlik va kohéziyani - diffdan o'qishni beradi. Nazariy ta'rif `java-spring-architect-mindset.md` da, bu yerda faqat ko'rinadigan belgilar va review javoblari.

### 7.1 Bog'liqlik turlarini diffda aniqlash

Bog'liqlik bir xil emas. Uning har bir turi boshqa belgi qoldiradi va boshqa narx keltiradi.

| Tur | Diffdagi belgisi | Narxi | Review javobi |
| --- | --- | --- | --- |
| Ma'lumot (parametr orqali) | Oddiy parametr | Eng arzon, normal | Qabul qilinadi |
| Shakl (DTO strukturasi) | Boshqa modulning DTO si import qilingan | O'rtacha | O'z turiga aylantirish |
| Boshqaruv (boolean flag) | `doWork(true, false)` | Yuqori | Ikki alohida metod |
| Vaqt (chaqiruv tartibi) | `init()` keyin `run()` majburiy | Yuqori | Konstruktor yoki bitta metod |
| Joylashuv (URL, yo'l) | Qattiq yozilgan manzil | O'rtacha | Konfiguratsiya |
| Sxema (umumiy jadval) | Boshqa modul jadvaliga `JOIN` | Juda yuqori | API yoki o'qish modeli |
| Umumiy mutable holat | `static` to'plam, singleton kesh | Juda yuqori | Holatni egasiga berish |
| Implementatsiya (ichki detal) | Boshqa modulning `internal` klassi | Juda yuqori | Chegara orqali o'tish |

### 7.2 Vaqt bog'liqligi: eng jim xato manbasi

Vaqt bog'liqligi - obyektdan foydalanish uchun metodlarni ma'lum tartibda chaqirish kerak bo'lgan holat. Kompilyator buni tekshirmaydi, test odatda to'g'ri tartibda yozilgan bo'ladi, va xato faqat yangi chaqiruv joyi paydo bo'lganda chiqadi.

```java
// Vaqt bog'liqligi: ikki qadam majburiy, lekin hech narsa buni majburlamaydi.
public class ReportBuilder {
    private List<Row> rows;

    public void load(LocalDate from, LocalDate to) {   // birinchi chaqirilishi shart
        this.rows = repository.rows(from, to);
    }

    public byte[] render() {                           // ikkinchi
        return pdf.render(rows);                       // load chaqirilmasa - NPE
    }
}
// Review izohi: render() ni load() dan oldin chaqirish kompilyatsiyada
// tutilmaydi. Yangi chaqiruvchi shu tartibni bilmasligi mumkin.
// Yechim: holatni konstruktorga olib kirish yoki bitta metod qilish.

// To'g'ri: obyekt yaratilgan paytdan to'liq ishga tayyor (immutable).
public record ReportRequest(LocalDate from, LocalDate to) { }

public class ReportService {
    public byte[] render(ReportRequest request) {      // bitta kirish nuqtasi
        List<Row> rows = repository.rows(request.from(), request.to());
        return pdf.render(rows);
    }
}
```

Spring kodida bu naqsh ko'p uchraydi: `@PostConstruct` da bir narsa to'ldiriladi, keyin metodlar unga tayanadi. Review savoli - bean to'liq qurilgandan keyin ishlatilishi kafolatlanganmi, va `@PostConstruct` ichida tashqi chaqiruv bo'lsa, ishga tushish buzilmaydimi.

### 7.3 Kohéziya: nima birga o'zgarsa, birga tursin

Past kohéziya belgisi - bitta klassda bir-biriga aloqasi yo'q bo'lgan metodlar to'plami. Uning eng aniq ko'rsatkichi: klass maydonlarining qanchasi har bir metodda ishlatiladi. Agar klassda 8 maydon bo'lsa va har metod ulardan ikkitasini ishlatsa, bu aslida to'rt xil klass.

```java
// Past kohéziya: "OrderService" ichida to'rt xil mas'uliyat.
@Service
public class OrderService {
    private final OrderRepository orders;      // 1-guruh
    private final PaymentClient payments;      // 2-guruh
    private final PdfRenderer pdf;             // 3-guruh
    private final SmsSender sms;               // 4-guruh
    private final ExcelExporter excel;         // 3-guruh
    private final FraudScoreClient fraud;      // 2-guruh

    public Order place(PlaceOrder cmd) { /* orders, payments, fraud */ }
    public byte[] invoicePdf(long id) { /* orders, pdf */ }
    public byte[] monthlyExcel(int m) { /* orders, excel */ }
    public void remind(long id) { /* orders, sms */ }
}
// Review izohi: konstruktorda 6 bog'liqlik, lekin hech bir metod uchtadan
// ko'pini ishlatmaydi. Bu klass to'rt sababga ko'ra o'zgaradi: buyurtma
// qoidasi, hujjat shakli, hisobot formati, xabar matni.
// Natijasi: PDF shablonini o'zgartirish uchun to'lov mantiqi bor faylga
// tegiladi, va shu fayl har sprintda konflikt beradi.
// Yechim: OrderPlacement, OrderDocuments, OrderReports, OrderReminders.
```

```bash
# Kohéziyani o'lchash: tarixda birga o'zgargan fayllar (change coupling).
# Agar ikki fayl har doim birga o'zgarsa, ular bitta modul bo'lishi kerak.
# Agar bitta fayl turli sabablar bilan o'zgarsa, u bo'linishi kerak.
git log --format='%H' --since='12 months ago' \
  | while read -r c; do git show --name-only --format= "$c"; echo "---"; done \
  | awk '/^---$/{for(i in f) for(j in f) if(i<j) print i" + "j; delete f; next}
         /\.java$/{f[$0]=1}' \
  | sort | uniq -c | sort -rn | head -20

# Bitta faylning o'zgarish sabablarini ko'rish: commit sarlavhalari.
git log --oneline --since='6 months ago' -- src/main/java/.../OrderService.java | head -30
```

Ikkinchi buyruq review da juda foydali: agar bitta faylning oxirgi 30 commit sarlavhasi to'rt xil mavzuda bo'lsa (to'lov, PDF, hisobot, SMS), klassni bo'lish kerakligi dalil bilan ko'rsatiladi.

### 7.4 Soxta abstraksiya: bitta implementatsiyali interfeys

Loyihalarda eng ko'p uchraydigan ortiqcha abstraksiya - har bir servis uchun interfeys yozish odati. `OrderService` va `OrderServiceImpl` juftligi hech qanday moslashuvchanlik bermaydi: almashtirish nuqtasi yo'q, test uchun ham kerak emas (Mockito klasslarni ham mock qiladi).

```java
// Soxta abstraksiya: faqat nom takrorlanishi, foyda nol.
public interface OrderService {                 // bitta implementatsiya
    Order place(PlaceOrder cmd);
}
@Service
public class OrderServiceImpl implements OrderService { /* ... */ }

// Review savoli: ikkinchi implementatsiya qachon paydo bo'ladi?
// Javob "hech qachon" bo'lsa - interfeys olib tashlanadi.

// Haqiqiy abstraksiya: almashtirish nuqtasi real.
public interface PaymentGateway {               // Stripe, Payme, test uchun soxta
    AuthResult authorize(Money amount, Card card);
}
// Bu yerda interfeys kerak, chunki:
// 1) ikki provayder ham prodda ishlaydi (marshrutlash bor);
// 2) testda tarmoqqa chiqmaydigan implementatsiya kerak;
// 3) domen vendor turlarini bilmasligi kerak.
```

Mezon uchta savolda: hozir ikkinchi implementatsiya bormi, testda almashtirish zarurmi (integratsion test bilan yopib bo'lmaydimi), va bu chegarada bog'liqlik yo'nalishini teskari qilish kerakmi. Uchiga ham "yo'q" bo'lsa, interfeys ortiqcha.

### 7.5 DRY ning noto'g'ri qo'llanishi

Takrorlanishni olib tashlash har doim yaxshi emas. Ikki kod bloki bir xil ko'rinishi mumkin, lekin turli sabablarga ko'ra o'zgaradi. Ularni birlashtirish - ikki mustaqil narsani bir-biriga qulflash.

```java
// Tasodifiy o'xshashlik: ikki validatsiya bir xil ko'rinadi.
void validateCustomerPhone(String phone) {
    if (phone == null || !phone.matches("\\+998\\d{9}")) throw new Invalid();
}
void validateCourierPhone(String phone) {
    if (phone == null || !phone.matches("\\+998\\d{9}")) throw new Invalid();
}

// Noto'g'ri "yaxshilash": birlashtirish.
void validatePhone(String phone) { ... }        // ikkisi ham shuni chaqiradi

// Nega noto'g'ri: kuryer telefoni kelasi oyda xalqaro raqam bo'lishi mumkin
// (chet el kuryerlari), mijoz telefoni esa faqat mahalliy qoladi. Shunda
// umumiy metodga flag qo'shiladi - va boshqaruv bog'liqligi paydo bo'ladi.

// To'g'ri yondashuv: tur bilan ajratish, umumiy qism primitiv darajada qoladi.
public record PhoneNumber(String value) {
    public PhoneNumber {
        if (value == null || !value.matches("\\+\\d{7,15}")) throw new Invalid();
    }
}
public record UzPhoneNumber(String value) { /* +998 qoidasi */ }
```

Review mezoni: takrorlangan kod bir xil sababga ko'ra o'zgaradimi. Javob "ha" bo'lsa - birlashtirish. "Yo'q" yoki "bilmayman" bo'lsa - takrorlanish arzonroq. Uchinchi marta takrorlanganda qaytib ko'rish qoidasi amalda yaxshi ishlaydi.

### 7.6 Oqib chiqadigan abstraksiya (leaky abstraction)

Abstraksiya ichidagi detal tashqariga chiqib qolsa, u foyda bermaydi, lekin narx keltiradi: foydalanuvchi ikki narsani - abstraksiyani va uning ichini - bilishi kerak bo'ladi.

| Oqish belgisi | Misol | Oqibati |
| --- | --- | --- |
| Istisno turi implementatsiyadan | `PaymentGateway` `HttpClientErrorException` tashlaydi | Chaqiruvchi HTTP ni biladi |
| Qaytish turida vendor klassi | `StripeCharge` qaytariladi | Vendor almashtirilmaydi |
| Konfiguratsiya nomlari oqib chiqqan | `setStripeApiVersion` port interfeysida | Abstraksiya soxta |
| Tartiblash/pagination detali | `Pageable` domen portida | Spring domenga kirgan |
| `null` ning maxsus ma'nosi | "null = topilmadi, bo'sh = xato" | Hujjatsiz shartnoma |
| Ketma-ketlikka bog'liqlik | "avval `prepare` chaqiring" | Vaqt bog'liqligi |

```java
// Oqadigan port: domen HTTP va Stripe ni biladi.
public interface PaymentGateway {
    StripeChargeResponse charge(String json) throws HttpClientErrorException;
}

// Yopiq port: faqat domen tillari.
public interface PaymentGateway {
    /** Xato holatlari: DECLINED, NETWORK, INVALID_CARD. */
    AuthResult authorize(Money amount, Card card);
}
public sealed interface AuthResult {
    record Approved(String authCode) implements AuthResult { }
    record Declined(DeclineReason reason) implements AuthResult { }
    record Failed(FailureKind kind, String detail) implements AuthResult { }
}
// Review foydasi: chaqiruvchi hamma holatni hisobga olishga majbur
// (sealed + switch), va vendor istisnolari adapter ichida qoladi.
```

### 7.7 Feature envy va shotgun surgery

Feature envy - metod o'z klassining maydonlaridan ko'ra boshqa obyektning maydonlari bilan ko'proq ishlaydigan holat. Diffda belgisi: yangi metodda `other.getX()`, `other.getY()`, `other.getZ()` ketma-ketligi.

```java
// Feature envy: hisob Order ning ichki ma'lumotidan quriladi, lekin
// Order dan tashqarida bajariladi.
public class ShippingCalculator {
    public Money cost(Order order) {
        BigDecimal weight = BigDecimal.ZERO;
        for (OrderLine line : order.getLines()) {          // ichkiga kirish
            weight = weight.add(line.getProduct().getWeight()
                                    .multiply(BigDecimal.valueOf(line.getQty())));
        }
        if (order.getCustomer().getTier() == GOLD) { ... } // yana ichkiga
        return ...;
    }
}
// Review izohi: bu metod Order ning uch darajali ichki tuzilishini biladi.
// Order o'zgarsa, shu hisob ham sinadi. Og'irlik hisobini Order ga
// ko'chirish kerak: order.totalWeight(). Qoidaning o'zi (narx jadvali)
// kalkulyatorda qolishi mumkin.
```

Shotgun surgery - bitta mantiqiy o'zgarish uchun ko'p faylga tegish kerak bo'lgan holat. Diffda belgisi: 12 faylda bittadan satr o'zgargan va hammasi bir xil o'zgarish.

```bash
# Shotgun surgery belgisini o'lchash: bir xil o'zgarish necha faylda.
git diff --numstat origin/main...HEAD \
  | awk '$1<=3 && $2<=3 {n++} END {print n" ta faylda uchdan kam satr tegilgan"}'

# Agar bu son 8 dan oshsa va o'zgarishlar bir xil bo'lsa, abstraksiya yo'q:
git diff origin/main...HEAD | grep -E '^\+' | sort | uniq -c | sort -rn | head
```

Birinchi buyruq "bir xil satr ko'p joyda takrorlangan" holatini ko'rsatadi. Review javobi - bu o'zgarish bitta joyda bo'lishi uchun nima kerak degan savol.

### 7.8 Abstraksiya darajalarining aralashuvi

Bir metod ichida turli darajadagi gaplar bo'lsa, o'qish qiyinlashadi: biznes qoidasi bilan bayt bufferi yoki satr formatlash bir qatorda turadi.

```java
// Aralash darajalar: "nima" va "qanday" bir joyda.
public void publishDailyReport(LocalDate date) {
    List<Row> rows = repository.rows(date);                    // yuqori daraja
    ByteArrayOutputStream bos = new ByteArrayOutputStream();   // past daraja
    try (ZipOutputStream zip = new ZipOutputStream(bos)) {     // past daraja
        zip.putNextEntry(new ZipEntry("report.csv"));
        for (Row r : rows) {
            zip.write((r.id() + ";" + r.amount() + "\n").getBytes(UTF_8));
        }
    } catch (IOException e) { throw new UncheckedIOException(e); }
    mailer.send(recipients(), "Kunlik hisobot", bos.toByteArray());  // yuqori
}

// Bir darajada o'qiladigan shakl: har qatori bir xil balandlikda.
public void publishDailyReport(LocalDate date) {
    List<Row> rows = repository.rows(date);
    byte[] archive = csvArchive(rows);
    mailer.send(recipients(), "Kunlik hisobot", archive);
}
// Review mezoni: metodni o'qiganda "nima bo'layotgani" bir o'qishda
// tushunarli bo'lsa, daraja to'g'ri. Zip va baytlar pastki metodda.
```

### 7.9 Konstruktor parametrlari soni - eng oson o'lchov

Bog'liqlikni o'lchashning eng tez usuli - konstruktorga qarash. Besh-oltidan ko'p bog'liqlik klassning juda ko'p narsani bilishini bildiradi. Bu qoida qattiq emas, lekin savol berish uchun yetarli sabab.

```bash
# Konstruktor parametrlari ko'p bo'lgan klasslarni topish.
grep -rn --include='*.java' -A4 'public [A-Z][A-Za-z]*(' src/main/java \
  | grep -oE '\(([^)]*,){5,}[^)]*\)' | wc -l

# Diffda yangi qo'shilgan konstruktor parametrlarini ko'rish.
git diff origin/main...HEAD -- '*.java' | grep -E '^\+.*private final '
```

Diffda yangi `private final` maydon qo'shilishi - har doim savol: bu klassning mas'uliyati o'sdimi, yoki yangi mas'uliyat boshqa joyga tegishlimi.

### 7.10 Abstraksiyani olib tashlash ham yaxshilanish

Review izohlari odatda abstraksiya qo'shishni so'raydi. Teskari yo'nalish ham xuddi shunday qimmatli: ortiqcha qatlamni olib tashlash.

| Olib tashlashga arziydigan narsa | Belgisi |
| --- | --- |
| Bitta implementatsiyali interfeys | `XxxImpl` nomlash |
| Hech narsa qo'shmaydigan mapper | DTO va entity maydonlari bir xil, mapping 1:1 |
| O'tkazib yuboruvchi servis | Metod faqat repository ga delegatsiya qiladi |
| Hech kim tashlamaydigan custom istisno | Faqat e'lon qilingan |
| Ishlatilmaydigan konfiguratsiya flag i | Har doim bir qiymatda |
| Generics ortiqcha | `<T extends Object>` real polimorfizm yo'q |
| Abstract base class | Bitta vorisi bor |

```bash
# Bitta implementatsiyali interfeyslarni topish.
for i in $(grep -rl --include='*.java' 'public interface' src/main/java); do
  name=$(basename "$i" .java)
  impl=$(grep -rl --include='*.java' "implements .*$name" src/main/java | wc -l)
  [ "$impl" = "1" ] && echo "$name: 1 implementatsiya"
done | head -20

# Faqat delegatsiya qiladigan metodlarni topish (bir satrli servis metodlari).
grep -rn --include='*.java' -A2 'public .* [a-z].*(' src/main/java/**/service \
  | grep -B1 'return [a-z]*\.[a-z]*(' | head -20
```

### 7.11 Amalda qo'llash

- [ ] Bog'liqlik turlari jadvalini review checklistiga qo'shib, har PR da "qaysi tur qo'shildi" savolini bering.
- [ ] Vaqt bog'liqligi bor klasslarni toping (`init`/`load` keyin ishlatiladigan) va ularni immutable konstruktorga o'tkazish tiketini ochingg.
- [ ] Change coupling skriptini ishga tushirib, har doim birga o'zgaradigan 10 juft faylni aniqlang va ularni bitta moduldami yoki yo'qligini tekshiring.
- [ ] Oxirgi 6 oyda bitta faylga kelgan commit sarlavhalarini mavzu bo'yicha guruhlab, to'rtdan ko'p mavzuli klasslarni bo'lishni rejalashtiring.
- [ ] Bitta implementatsiyali interfeyslar ro'yxatini chiqarib, real almashtirish nuqtasi yo'qlarini olib tashlang.
- [ ] Portlardan oqib chiqadigan detallarni toping: `HttpClientErrorException`, `Pageable`, vendor turlari domen interfeyslarida.
- [ ] Konstruktorida 6 dan ko'p bog'liqlik bo'lgan klasslarni sanab, ularning har bir metodi nechta maydonni ishlatishini tekshiring.
- [ ] Faqat delegatsiya qiladigan servis qatlamlari va 1:1 mapperlarni toping va olib tashlash taklifini kiritiladigan PR ga qo'shing.

## 8. Clean code review: nomlash, kognitiv yuk, metod shakli (Clean Code at the Review Table)

Clean code review ning eng ko'p noto'g'ri bajariladigan qismi, chunki u didga eng yaqin. Natijada review ikki qutbga ketadi: yoki uslub haqida uzun bahs, yoki hech qanday izoh. To'g'ri yo'l o'rtada: nomlash va shakl haqidagi izoh faqat kelajakdagi o'qish narxini oshiradigan holatlarda yoziladi va har doim sabab bilan birga keladi.

### 8.1 Nom - eng arzon hujjat va eng qimmat xato

Kod bir marta yoziladi, o'nlab marta o'qiladi. Nom esa o'qishning har safarida ishlaydi. Shu sababli nom haqidagi izoh "did" emas - u o'qish narxini kamaytiradi. Lekin mezon kerak: nom qachon yomon.

| Yomon nom belgisi | Misol | Nega muammo |
| --- | --- | --- |
| Turini aytadi, ma'nosini aytmaydi | `List<String> list`, `Map<String,String> map` | O'qiyotgan odam yana koddan izlaydi |
| Qisqartma domen tilida emas | `ordNum`, `custTp`, `amtUsd` | Yangi odam dekodlashga vaqt sarflaydi |
| Yolg'on nom | `validateOrder` ichida saqlaydi ham | Noto'g'ri taxmin, keyin xato |
| Juda umumiy | `data`, `info`, `process`, `handle`, `manager` | Hech narsa aytmaydi |
| Raqam bilan ajratilgan | `result1`, `result2`, `temp2` | Farqi kodni o'qimasdan bilinmaydi |
| Inkor bilan | `isNotInactive` | Ikki marta inkor, miyada aylantirish kerak |
| Birlik yo'q | `timeout = 30`, `size = 5` | 30 nima: sekund, millisekund? |
| Domen tiliga qarshi | Biznes "invoys" deydi, kodda `bill` | Suhbat va kod tili ajraladi |

```java
// Nom orqali bilimni kodga kiritish. Birinchi variant: nom hech narsa aytmaydi.
public boolean check(Order o, int d) {
    return o.getCreated().plusDays(d).isAfter(LocalDate.now());
}

// Ikkinchi variant: nom qoidani aytadi, izoh kerak emas.
public boolean isWithinReturnWindow(Order order, int returnWindowDays) {
    return order.placedOn().plusDays(returnWindowDays).isAfter(today());
}

// Uchinchi variant: birlik va domen tur bilan kiritilgan - noto'g'ri
// qiymat uzatish kompilyatsiyada tutiladi.
public boolean isWithinReturnWindow(Order order, ReturnWindow window) { ... }
public record ReturnWindow(Period period) { }
```

Review da nom haqidagi izohning foydali shakli: yangi nomni taklif qilish, shunda muallif o'ylab topishga vaqt sarflamaydi. "Nomi tushunarsiz" degan izoh ish qo'shadi, "`pendingShipments` desak, keyingi o'qiyotgan odam ro'yxat nimadan iboratligini bilib turadi" degan izoh ishni kamaytiradi.

### 8.2 Birlik, valyuta va vaqt zonasi nomda

Eng qimmat nomlash xatolari o'lchov birligi bilan bog'liq. `timeout = 30` satri ikki xil o'qiladi va noto'g'ri o'qish prodda chiqadi.

```java
// Yomon: birlik nomda yo'q, tur hech narsa kafolatlamaydi.
public void retry(int delay, int timeout) { ... }
retry(30, 5);                                  // 30 nima? 5 nima?

// Yaxshiroq: birlik nomda.
public void retry(long delayMillis, long timeoutMillis) { ... }

// Eng yaxshi: tur birlikni ushlab turadi, aralashtirib bo'lmaydi.
public void retry(Duration delay, Duration timeout) { ... }
retry(Duration.ofSeconds(30), Duration.ofSeconds(5));

// Pul uchun ham xuddi shunday: valyuta turning ichida.
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("valyutalar mos emas");
        }
        return new Money(amount.add(other.amount), currency);
    }
}
// Review izohi: BigDecimal total parametri valyutani ushlamaydi. Ikki
// valyutadagi summalarni qo'shib qo'yish kompilyatsiyada tutilmaydi va
// hisobot noto'g'ri bo'ladi.
```

### 8.3 Metod shakli: uzunlik emas, shoxlanish

"Metod 20 satrdan oshmasin" qoidasi mexanik va foydasi kam. Haqiqiy mezon - metodni tushunish uchun miyada qancha narsa ushlab turish kerak. 40 satrli chiziqli metod 12 satrli uch darajali ichma-ich shartli metoddan osonroq o'qiladi.

```java
// Uch darajali ichma-ich shart: har qadamda kontekst to'planadi.
public Result process(Order order) {
    if (order != null) {
        if (order.getStatus() == NEW) {
            if (order.getLines() != null && !order.getLines().isEmpty()) {
                if (inventory.hasStock(order)) {
                    return doProcess(order);
                } else {
                    return Result.outOfStock();
                }
            } else {
                return Result.empty();
            }
        } else {
            return Result.wrongStatus();
        }
    }
    return Result.invalid();
}

// Erta qaytish: har satrdan keyin kontekst kamayadi, oxirida faqat
// "hammasi yaxshi" holati qoladi.
public Result process(Order order) {
    if (order == null)              return Result.invalid();
    if (order.status() != NEW)      return Result.wrongStatus();
    if (order.lines().isEmpty())    return Result.empty();
    if (!inventory.hasStock(order)) return Result.outOfStock();
    return doProcess(order);
}
```

Review mezonlari shakl uchun: ichma-ich chuqurlik 2 dan oshmasin, bitta metodda `if` zanjiri 5 dan oshmasin, va `else` bloki bo'sh yoki faqat qaytarishdan iborat bo'lsa, erta qaytishga aylantirilsin.

### 8.4 Boolean parametr - yashirin ikki metod

Metod chaqiruvida `true` yoki `false` ko'rilsa, chaqiruv joyi hech narsa aytmaydi. Bundan tashqari bu boshqaruv bog'liqligi: chaqiruvchi chaqirilgan metodning ichidagi shoxni tanlaydi.

```java
// Chaqiruv joyi o'qilmaydi.
exporter.export(orders, true, false, true);

// Variant 1: alohida metodlar - eng aniq.
exporter.exportWithHeaders(orders);
exporter.exportRaw(orders);

// Variant 2: nomlangan sozlama obyekti - parametrlar ko'p bo'lsa.
exporter.export(orders, ExportOptions.builder()
                                     .withHeaders(true)
                                     .delimiter(';')
                                     .compress(false)
                                     .build());

// Variant 3: enum - ikkidan ko'p holat bo'lsa.
exporter.export(orders, ExportFormat.CSV_WITH_HEADERS);
```

### 8.5 Primitive obsession: domen tilini turga aylantirish

Hamma narsa `String` va `long` bo'lgan kodda kompilyator hech narsa himoya qilmaydi. `userId` va `orderId` ni almashtirib qo'yish - kompilyatsiya bo'ladigan, lekin xato kod.

```java
// Xavfli: ikki long ni almashtirib qo'yish mumkin, kompilyator jim.
public void transfer(long fromAccount, long toAccount, BigDecimal amount) { }
transfer(toId, fromId, amount);                 // xato, lekin kompilyatsiya bo'ladi

// Xavfsiz: tur almashtirishni taqiqlaydi.
public record AccountId(UUID value) {
    public AccountId { Objects.requireNonNull(value); }
}
public void transfer(AccountId from, AccountId to, Money amount) { }

// Domen qoidasi turning ichida: noto'g'ri qiymat yaratilmaydi.
public record Email(String value) {
    private static final Pattern RE = Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");
    public Email {
        if (value == null || !RE.matcher(value).matches()) {
            throw new IllegalArgumentException("email shakli noto'g'ri");
        }
        value = value.toLowerCase(Locale.ROOT);   // normalizatsiya bir joyda
    }
}
// Review foydasi: email tekshiruvi 7 joyda takrorlanmaydi, va bazaga
// normalizatsiya qilinmagan email tushmaydi.
```

Review da mezon: qiymat domen qoidasiga egami (email, telefon, pul, identifikator, status) va u noto'g'ri bo'lishi mumkinmi. Ikkisiga "ha" bo'lsa, u o'z turiga arziydi. Oddiy texnik qiymat (hisoblash natijasi, ichki indeks) uchun primitiv yetadi.

### 8.6 Izoh qachon kerak

Izoh kodni takrorlasa - u ikki marta qarishadi. Izoh sababni aytsa - u kodda bo'lmagan bilimni saqlaydi.

```java
// Foydasiz izoh: kod aytganini takrorlaydi.
// Buyurtmani saqlaydi
orders.save(order);

// Foydali izoh: nega shunday qilingani, va nima bo'lsa o'zgartirish mumkinligi.
// PostgreSQL da bu jadval 40 mln qator. created_at bo'yicha indeks bor,
// lekin status bo'yicha yo'q: qiymatlar notekis taqsimlangan (99% CLOSED),
// shuning uchun planner indeksni ishlatmaydi. Partial indeks qo'shilsa,
// bu filtr ham indeksga tushadi: INDEX ... WHERE status <> 'CLOSED'.
List<Order> open = orders.findOpenCreatedAfter(since);

// Foydali izoh: tashqi tizim xulqi haqida, kodda ko'rinmaydigan bilim.
// To'lov provayderi 409 ni "allaqachon bajarilgan" ma'nosida qaytaradi,
// hujjatda 409 "konflikt" deb yozilgan. 2026-02 da support bilan
// tasdiqlangan. Shuning uchun 409 muvaffaqiyat deb hisoblanadi.
if (response.statusCode() == 409) return AuthResult.approved(idemKey);
```

Review qoidasi: har bir `// hack`, `// vaqtincha`, `// TODO` izohiga egasi va sanasi kerak, aks holda u abadiy qoladi.

```bash
# Egasi yo'q TODO larni topish: ular texnik qarzning yashirin qismi.
grep -rn --include='*.java' -E 'TODO|FIXME|HACK|XXX' src/main/java \
  | grep -vE 'TODO\([a-z.]+,[ ]*[0-9]{4}-[0-9]{2}\)' | head -20
# Konvensiya: TODO(ism, 2026-06): sabab va shart.
```

### 8.7 O'lik kod va yarim ishlangan narsalar

Diffda qo'shilgan, lekin hech kim chaqirmaydigan kod - kelajakdagi chalg'itish manbasi. Keyingi odam uni ishlaydi deb o'ylaydi.

```bash
# Yangi qo'shilgan public metodlar chaqirilyaptimi.
git diff origin/main...HEAD -- '*.java' \
  | grep -oE '^\+\s+(public|protected).* ([a-zA-Z][a-zA-Z0-9]*)\(' \
  | grep -oE '[a-zA-Z][a-zA-Z0-9]*\($' | tr -d '(' | sort -u \
  | while read -r m; do
      c=$(grep -rn --include='*.java' "\.$m(\|::$m" src/ | wc -l)
      [ "$c" -eq 0 ] && echo "CHAQIRILMAYDI: $m"
    done

# Kommentga olingan kod bloklari: review da darhol olib tashlash so'raladi.
git diff origin/main...HEAD | grep -E '^\+\s*//\s*[a-zA-Z].*[;{)]' | head
```

Kommentga olingan kod uchun javob har doim bitta: o'chirish. Git tarixi uni saqlaydi, va kommentdagi kod hech qachon yangilanmaydi.

### 8.8 Clean code bahonasida haddan oshish

Review ning teskari xatosi ham bor: toza kod nomidan ortiqcha talab qo'yish. Buning belgilari: har bir uch satrli bo'lak alohida metodga ajratish, har bir `if` ni Strategy ga aylantirish, har bir klassga interfeys, har bir konstantaga enum.

Mezon: o'zgarish o'qish narxini kamaytiradimi yoki faqat qoidaga moslashtiradimi. Ikkinchi holatda izoh `nit` darajasida qoladi va majburiy bo'lmaydi.

| Haddan oshish shakli | Natija |
| --- | --- |
| Har 3 satr alohida metod | Metodlar zanjiri, bitta mantiqni o'qish uchun 8 joyga sakrash |
| Har joyda interfeys | Navigatsiya qiyinlashadi, foyda nol |
| Har `if` uchun Strategy | Ikki holat uchun 5 klass |
| Har konstanta uchun enum | Ortiqcha ceremony |
| Har metodda Javadoc | Takrorlangan matn, qarishadi |
| Har DTO uchun builder | Record bilan osonroq |

### 8.9 Formatlash izohi review da bo'lmasligi kerak

Agar PR da formatlash haqida izoh yozilayotgan bo'lsa, bu instrument yo'qligini bildiradi. Bitta marta sozlangan formatter shu izohlarning hammasini abadiy yo'q qiladi.

```xml
<!-- spotless: formatlash muhokamasini butunlay tugatish. -->
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <configuration>
    <java>
      <googleJavaFormat><style>AOSP</style></googleJavaFormat>
      <removeUnusedImports/>
      <importOrder><order>java,javax,jakarta,org,com,</order></importOrder>
      <trimTrailingWhitespace/>
      <endWithNewline/>
    </java>
    <sql><dbeaver/></sql>
  </configuration>
  <executions>
    <execution>
      <!-- CI da tekshiradi, lokalda `mvn spotless:apply` tuzatadi. -->
      <goals><goal>check</goal></goals>
      <phase>validate</phase>
    </execution>
  </executions>
</plugin>
```

### 8.10 O'qiluvchanlikni o'lchash: review ning o'zi sinov

O'qiluvchanlikning eng yaxshi sinovi - review ning o'zi. Agar reviewer kodni tushunish uchun savol berishga majbur bo'lsa, demak kod yetarlicha aytmagan. Shu holatda to'g'ri javob - izohda tushuntirish emas, kodni tushunarli qilish.

Foydali odat: muallif review savoliga javob yozganida o'zidan so'rashi kerak - shu javob kodda bo'lishi kerakmidi. Ko'p hollarda javob "ha" bo'ladi va u nom, tur yoki qisqa izohga aylanadi. Shu bilan review bir martalik suhbatdan doimiy bilimga aylanadi.

### 8.11 Amalda qo'llash

- [ ] `spotless` yoki `google-java-format` ni CI ga qo'shib, formatlash izohlarini butunlay taqiqlang.
- [ ] Loyihada birlik ko'rsatilmagan vaqt va hajm parametrlarini toping (`int timeout`, `long delay`) va `Duration` ga o'tkazishni rejalashtiring.
- [ ] Pul hisobida `BigDecimal` valyutasiz ishlatilgan joylarni toping va `Money` turini kiriting.
- [ ] Boolean parametrli public metodlarni grep bilan toping va ularni alohida metod yoki enum ga ajratish ro'yxatini tuzing.
- [ ] Email, telefon, identifikator kabi domen qiymatlari uchun value object kiritib, takrorlangan validatsiyalarni bitta joyga yig'ing.
- [ ] `TODO(ism, sana)` konvensiyasini joriy qilib, egasi yo'q TODO larni CI da ogohlantirishga chiqaring.
- [ ] Yangi qo'shilgan, lekin chaqirilmaydigan public metodlarni aniqlaydigan skriptni review oqimiga qo'shing.
- [ ] Review izohlarining qanchasi `nit` ekanini sanab, ularning 20 foizdan ko'pi bo'lsa, instrumentlarga ko'chirish mumkinligini tekshiring.

## 9. SOLID va dizayn printsiplarini diffda tekshirish (Principles, Not Slogans)

SOLID review da ikki xil ishlatiladi. Birinchi usul - shior sifatida: "bu SRP ni buzadi". Bu izoh hech narsa bermaydi, chunki muallif nimani o'zgartirishni bilmaydi. Ikkinchi usul - diagnostika sifatida: har bir printsipning diffda ko'rinadigan aniq belgisi bor, va shu belgini ko'rsatish mumkin. Bu bob har bir printsip uchun belgini, oqibatni va review javobini beradi.

### 9.1 SRP: o'zgarish sabablarini sanash

Single responsibility "klass bitta ish qiladi" degani emas. U "klass bitta sababga ko'ra o'zgaradi" degani. Shu sababli SRP ni tekshirish usuli - o'zgarish sabablarini sanash, metodlarni sanash emas.

Amaliy savol: shu klassni o'zgartirishni kim so'raydi. Agar javobda ikki xil manfaatdor bo'lsa (buxgalteriya soliq qoidasini o'zgartiradi, marketing xabar matnini o'zgartiradi), klass bo'linishi kerak.

```java
// Ikki egasi bor klass: soliq qoidasi va hujjat shakli bir joyda.
@Service
public class InvoiceService {
    public Invoice create(Order order) {
        BigDecimal vat = order.total().multiply(new BigDecimal("0.12"));  // buxgalteriya
        Invoice inv = new Invoice(order.id(), order.total(), vat);
        String html = "<h1>Invoys #" + inv.number() + "</h1>"             // dizayn
                    + "<p>Jami: " + inv.total() + " so'm</p>";
        inv.setRenderedHtml(html);
        return inv;
    }
}
// Review izohi: soliq foizi o'zgarsa va hujjat shakli o'zgarsa - bitta
// faylga ikki xil jamoa tegadi. Shu fayl har ikki talabda konflikt beradi
// va har o'zgarishda ikki xil testni ishga tushirish kerak bo'ladi.
// Ajratish: VatCalculator (qoida) va InvoiceRenderer (shakl).
```

### 9.2 OCP: yangi holat qo'shilganda nima o'zgaradi

Open-closed ni tekshirishning aniq usuli bor: "ertaga yangi to'lov usuli (yoki yangi hujjat turi, yangi status) qo'shilsa, nechta faylga tegiladi" degan savol. Javob bitta fayl bo'lsa - yopiq. Besh fayl bo'lsa - har qo'shilishda beshta joyni esdan chiqarmaslik kerak.

```java
// Yopilmagan dizayn: yangi turi qo'shilsa, uch joy o'zgaradi.
switch (payment.type()) {
    case CARD -> cardFee(payment);
    case WALLET -> walletFee(payment);
}                                                  // 1-joy: komissiya
switch (payment.type()) { ... }                    // 2-joy: tekshiruv
switch (payment.type()) { ... }                    // 3-joy: hisobot

// Yopiq dizayn: yangi tur bitta klass qo'shish bilan keladi.
public interface PaymentMethod {
    PaymentType type();
    Money fee(Money amount);
    void validate(PaymentRequest request);
}
// Spring hamma implementatsiyani o'zi yig'adi.
@Service
public class PaymentMethods {
    private final Map<PaymentType, PaymentMethod> byType;

    public PaymentMethods(List<PaymentMethod> all) {       // konstruktorga ro'yxat
        this.byType = all.stream()
            .collect(toMap(PaymentMethod::type, identity()));
    }
    public PaymentMethod of(PaymentType type) {
        PaymentMethod m = byType.get(type);
        if (m == null) throw new UnsupportedPaymentType(type);
        return m;
    }
}
```

Diqqat: OCP ni oldindan qo'llash erta abstraksiyaga olib keladi. Mezon - haqiqatda yangi turlar qo'shilayotganini tarixda ko'rish. Agar tarixda ikki yil ichida uchta yangi to'lov usuli qo'shilgan bo'lsa, abstraksiya o'zini oqlaydi. Agar hech qachon qo'shilmagan bo'lsa, `switch` yetadi.

```bash
# Tarixdan OCP ni asoslash: shu enum ga qancha marta yangi qiymat qo'shilgan.
git log -p --follow -- '**/PaymentType.java' | grep -cE '^\+\s+[A-Z_]+,'
# Agar bu son yuqori bo'lsa, polimorfizm qo'shish dalil bilan asoslanadi.
```

### 9.3 LSP: shartnomani buzgan implementatsiya

Liskov buzilishi Java da ikki shaklda ko'rinadi: implementatsiya kutilmagan istisno tashlaydi, yoki kutilgan narsani qilmaydi (jim o'tkazib yuboradi).

```java
// Buzilish 1: implementatsiya shartnomani bajarmaydi.
public interface NotificationChannel {
    void send(Message message);        // shartnoma: xabarni yetkazadi
}
class NoopChannel implements NotificationChannel {
    @Override public void send(Message m) { }     // jim hech narsa qilmaydi
}
// Review izohi: bu implementatsiya chaqiruvchini aldaydi. Agar u test
// uchun kerak bo'lsa, test paketida bo'lishi kerak. Agar prodda
// "o'chirilgan kanal" ma'nosida bo'lsa, buni tur bilan ko'rsatish kerak:
// Optional<NotificationChannel> yoki isEnabled().

// Buzilish 2: shartnomada yo'q istisno.
class SmsChannel implements NotificationChannel {
    @Override public void send(Message m) {
        if (m.body().length() > 160) {
            throw new IllegalArgumentException("juda uzun");   // yangi shart
        }
    }
}
// Review izohi: chaqiruvchi kanal turini bilmaydi, lekin endi uzunlik
// cheklovini bilishi kerak. Shartnomaga `MessageTooLong` ni qo'shish yoki
// kanal imkoniyatlarini e'lon qilish kerak (maxLength()).
```

Spring kontekstida LSP buzilishining tipik joyi - `@Override` qilingan metod `super` ni chaqirmasligi, va `@Transactional` metodni vorisda qayta e'lon qilish (proxy xulqi o'zgaradi, 18-bob).

### 9.4 ISP: semiz interfeys va majburiy bo'sh metodlar

Interface segregation buzilishining belgisi aniq: implementatsiyada bo'sh metodlar yoki `UnsupportedOperationException` paydo bo'ladi.

```java
// Semiz interfeys: hamma implementatsiya hammasini qila olmaydi.
public interface FileStorage {
    void upload(String key, byte[] data);
    byte[] download(String key);
    void delete(String key);
    String presignedUrl(String key, Duration ttl);   // faqat S3 da bor
    void setAcl(String key, Acl acl);                // faqat S3 da bor
}
class LocalDiskStorage implements FileStorage {
    @Override public String presignedUrl(String k, Duration t) {
        throw new UnsupportedOperationException();   // ISP buzilishi belgisi
    }
}

// Ajratilgan interfeyslar: chaqiruvchi faqat kerakligiga bog'lanadi.
public interface FileStorage {
    void upload(String key, byte[] data);
    byte[] download(String key);
    void delete(String key);
}
public interface PresignedUrls {                     // qo'shimcha imkoniyat
    String presignedUrl(String key, Duration ttl);
}
// Review foydasi: lokal disk bilan ishlaydigan test muhitida presigned URL
// chaqiradigan kod kompilyatsiya paytida ko'rinadi.
```

### 9.5 DIP: interfeys kimga tegishli

Dependency inversion ko'pincha "interfeys ishlatish" deb tushuniladi, lekin uning mohiyati boshqa: interfeys foydalanuvchi tomonda e'lon qilinadi va implementatsiya unga moslashadi. Agar interfeys implementatsiya bilan bir paketda turgan bo'lsa va uning metodlari implementatsiya detallarini aks ettirsa, inversiya bo'lmagan.

| Belgi | Inversiya bormi |
| --- | --- |
| Interfeys domen paketida, implementatsiya infra da | Ha |
| Interfeys metodlari domen tilida (`shipped`, `authorize`) | Ha |
| Interfeys infra paketida, yonida `XxxImpl` | Yo'q |
| Interfeys metodlari vendor atamalarida (`callStripeApi`) | Yo'q |
| Domen `@Repository` annotatsiyasini biladi | Yo'q |

### 9.6 Demeter qonuni: zanjirli chaqiruv

`a.getB().getC().getD()` zanjiri ikki narsani bildiradi: chaqiruvchi uch darajali tuzilishni biladi, va o'rtadagi har qanday o'zgarish uni sindiradi. Bundan tashqari har bir `get` da null xavfi bor.

```java
// Zanjir: uch obyekt tuzilishiga bog'liqlik + uch null xavfi.
String city = order.getCustomer().getAddress().getCity().toUpperCase();

// Review javobi: so'rashni obyektning o'ziga topshirish.
String city = order.deliveryCity();     // Order o'z ichidagini biladi

// Order ichida:
public String deliveryCity() {
    return customer.address().city();    // bitta daraja, null konstruktorda yo'q
}
```

Istisno: fluent API va builder zanjirlari (`Stream`, `WebClient`, `builder()`) Demeter qonuniga kirmaydi, chunki ular har qadamda bir xil turni qaytaradi va tuzilish haqida bilim talab qilmaydi.

### 9.7 Tell, don't ask va anemik model

Anemik model - ma'lumot bir joyda (entity), qoidalar boshqa joyda (service) bo'lgan holat. Bu Spring loyihalarida eng keng tarqalgan dizayn. U har doim xato emas, lekin uning narxi bor: invariant hech kim tomonidan himoya qilinmaydi, chunki setterlar hammaga ochiq.

```java
// Anemik: har kim har qanday holatga o'tkaza oladi.
order.setStatus(SHIPPED);
order.setShippedAt(now());
// Qoida (faqat PAID dan SHIPPED ga o'tish mumkin) servisda, va u uch
// joyda takrorlanadi yoki bir joyda esdan chiqadi.

// Boy model: o'tish qoidasi obyekt ichida, noto'g'ri holat yaratilmaydi.
public class Order {
    private OrderStatus status;
    private Instant shippedAt;

    public void markShipped(Instant when, TrackingNumber tracking) {
        if (status != PAID) {
            throw new IllegalStateTransition(status, SHIPPED);
        }
        this.status = SHIPPED;
        this.shippedAt = when;
        this.tracking = tracking;
        registerEvent(new OrderShipped(id, tracking));   // domen eventi
    }
    // setStatus yo'q: tashqaridan holatni buzib bo'lmaydi.
}
```

Review mezoni: diffda `setX` ketma-ketligi ko'rinsa va ular birgalikda biznes holatini o'zgartirsa, bu operatsiya domen metodi bo'lishi kerak. Agar obyekt faqat ma'lumot tashuvchi bo'lsa (DTO, projection), setterlar normal.

### 9.8 Kompozitsiya va meros

Diffda yangi `extends` paydo bo'lsa, review savoli: bu "turi" munosabatimi yoki shunchaki kodni qayta ishlatishmi. Ikkinchi holda kompozitsiya to'g'ri.

```java
// Meros kodni qayta ishlatish uchun ishlatilgan: mo'rt bog'liqlik.
public class CachedOrderRepository extends JpaOrderRepositoryImpl {
    @Override public Optional<Order> findById(long id) {
        return cache.get(id, () -> super.findById(id));
    }
    // Muammo: boshqa findBy metodlar keshlanmaydi, va ota klassga yangi
    // metod qo'shilsa, u ham keshsiz o'tadi - jim nomuvofiqlik.
}

// Kompozitsiya: shartnoma aniq, qamrov to'liq ko'rinadi.
public class CachedOrderRepository implements OrderRepository {
    private final OrderRepository delegate;
    private final Cache cache;
    // Har metod ongli yoziladi: nima keshlanadi, nima o'tkaziladi.
}
```

Spring da bu masalaning yana bir tomoni bor: `@Transactional` yoki `@Cacheable` bo'lgan klassni meros qilish proxy xulqini o'zgartiradi va `super` chaqiruvi proxy orqali o'tmaydi. Shu sababli AOP ishtirok etadigan joyda meros qo'shimcha xavf keltiradi (18-bob).

### 9.9 Command-query separation: so'rov yon ta'sir qiladimi

Nomi so'rovga o'xshagan metod holatni o'zgartirsa, bu eng jim xato manbalaridan biri: chaqiruvchi uni xavfsiz deb o'ylaydi va kerakli joyda ikki marta chaqiradi.

```java
// Yolg'on so'rov: getter yozadi.
public Token getToken() {
    if (token == null || token.isExpired()) {
        token = authClient.fetchNewToken();     // tashqi chaqiruv va holat o'zgarishi
    }
    return token;
}
// Review izohi: `getToken()` nomi bepul o'qishni bildiradi, lekin bu metod
// tarmoqqa chiqadi va umumiy holatni o'zgartiradi. Ikki thread bir vaqtda
// chaqirsa - ikki marta token olinadi. Nomi `currentToken()` yoki
// `refreshIfNeeded()` bo'lishi, va sinxronizatsiya qo'shilishi kerak.

// Aniq shakl: niyat nomda, poyga himoyalangan.
private final AtomicReference<Token> cached = new AtomicReference<>();

public Token currentToken() {
    Token t = cached.get();
    if (t != null && !t.isExpired()) return t;
    synchronized (this) {
        t = cached.get();
        if (t != null && !t.isExpired()) return t;
        Token fresh = authClient.fetchNewToken();
        cached.set(fresh);
        return fresh;
    }
}
```

### 9.10 Printsipni qurol sifatida ishlatmaslik

Printsip nomi bilan yozilgan izoh muallifni himoyasiz qoldiradi: u printsip nomini bilmasa, bahslashish imkoni yo'q. Bu review ni muhandislikdan ierarxiyaga aylantiradi.

Shu sababli qoida: printsip nomi izohda bo'lishi mumkin, lekin yolg'iz bo'lmasligi kerak. Har doim belgi, oqibat va o'zgarish hajmi bilan birga keladi.

```text
# Yomon: shior.
"SRP buzilgan, bo'lish kerak."

# Yaxshi: belgi -> oqibat -> taklif -> hajm.
suggest: InvoiceService ichida soliq hisobi va HTML shakli bir joyda.

Belgi: create() metodi ikki xil sababga ko'ra o'zgaradi - soliq foizi
(buxgalteriya) va hujjat ko'rinishi (dizayn).

Oqibati: shu fayl oxirgi 6 oyda 14 marta o'zgargan, 9 tasi shablon
uchun, 5 tasi soliq uchun. Konfliktlar shu faylda eng ko'p.

Taklif: VatCalculator va InvoiceRenderer ga ajratish. Hajmi: ikki klass,
taxminan 60 satr ko'chirish, mavjud testlar o'zgarmaydi.
```

### 9.11 Amalda qo'llash

- [ ] SRP uchun "o'zgarish sabablarini sanash" savolini checklistga qo'shing va eng ko'p o'zgargan 10 faylni `git log` bilan aniqlab, ularning sabablarini guruhlang.
- [ ] Loyihadagi barcha `switch`/`if` zinapoyalarini enum turi bo'yicha toping va ularning qanchasi uch joydan ko'proq takrorlanganini aniqlang.
- [ ] Enum larga tarixda qancha yangi qiymat qo'shilganini o'lchab, polimorfizm qo'shish kerak bo'lgan joylarni dalil bilan belgilang.
- [ ] `UnsupportedOperationException` tashlaydigan implementatsiyalarni toping - har biri ISP buzilishining belgisi.
- [ ] Domen paketidagi interfeyslarning metodlari domen tilida nomlanganini tekshiring, vendor atamalarini toping.
- [ ] Uch va undan ko'p bo'g'inli `get` zanjirlarini grep bilan topib, ularni obyekt metodiga ko'chirish ro'yxatini tuzing.
- [ ] Entity larda ketma-ket chaqiriladigan `setX` guruhlarini aniqlab, ularni domen metodlariga aylantirishni rejalashtiring.
- [ ] Nomi `get`/`is` bilan boshlanadigan, lekin holat o'zgartiradigan yoki tarmoqqa chiqadigan metodlarni toping va nomini tuzating.

## 10. Dizayn pattern review I: yo'q patternni ko'rish (Missing Patterns)

Review ning eng yuqori qiymatli qismi - kodda pattern o'rni bo'sh qolganini ko'rish. Bu "pattern ishlatish kerak" degan talab emas: pattern o'zi maqsad emas. Mohiyat boshqa - takrorlanadigan muammoning ma'lum yechimi bor, va muallif uni qo'lda, yarim holda, xatolari bilan qayta yozyapti. Reviewer ning ishi shu holatni belgi orqali tanib olish va tayyor yechimni ko'rsatish. Patternlarning to'liq katalogi `java-spring-design-patterns.md` da, bu yerda faqat diffdagi belgilar va review javoblari.

### 10.1 Pattern bo'shlig'ining umumiy belgilari

| Diffdagi belgi | Nimani bildiradi | Qaysi yechim |
| --- | --- | --- |
| Enum bo'yicha `switch` uch va ko'p joyda | Xulq ma'lumot bilan birga turmaydi | Strategy, polimorfizm, enum ichida xulq |
| `if (type == A) ... else if (type == B)` o'sib boryapti | Yangi tur har joyda eslanishi kerak | Strategy registri |
| Obyekt yaratish mantiqi uch joyda takrorlangan | Yaratish qoidasi tarqalgan | Factory, statik fabrika metodi |
| Konstruktorda 6+ parametr, ko'pi ixtiyoriy | Chaqiruv joyi o'qilmaydi | Builder, parametr obyekti |
| Har metodda bir xil `try/catch/log/metric` o'rami | Kesishgan vazifa qo'lda yozilgan | Decorator, AOP, `@Retryable` |
| `status` bo'yicha `if` lar va qo'lda o'tishlar | Holat mashinasi yashiringan | State pattern, aniq state machine |
| Tashqi API chaqiruvi domen ichida | Chegara yo'q | Adapter, port, Gateway |
| DB yozuvi va keyin xabar yuborish | Atomiklik yo'q | Transactional Outbox |
| Bir xil so'rov ikki marta kelsa dublikat | Idempotentlik yo'q | Idempotency key + unique |
| Ko'p bosqichli jarayon bitta metodda | Qaytarish va kuzatish imkoni yo'q | Saga, Pipeline, Chain |
| Har joyda `new RestClient(...)` | Konfiguratsiya tarqalgan | Bitta sozlangan bean, Builder |
| Katta `Map<String,Object>` konfiguratsiya | Shartnoma yo'q | `@ConfigurationProperties` tipli obyekt |

### 10.2 Shoxlanishdan polimorfizmga: eng ko'p uchraydigan bo'shliq

Belgi aniq: bir xil `switch` ikki yoki uch joyda takrorlangan. Oqibati ham aniq: yangi qiymat qo'shilganda uchinchi joy esdan chiqadi, va xato prodda chiqadi.

```java
// Belgi: bir xil enum bo'yicha uch joyda shoxlanish.
// DiscountService.java
switch (tier) { case GOLD -> 0.15; case SILVER -> 0.05; case BRONZE -> 0.0; }
// ShippingService.java
switch (tier) { case GOLD -> Money.ZERO; case SILVER -> fee(50); ... }
// SupportService.java
switch (tier) { case GOLD -> Priority.HIGH; ... }

// Review javobi 1: xulqni enum ichiga olish (eng oddiy, Java da tabiiy).
public enum CustomerTier {
    GOLD(new BigDecimal("0.15"), Money.ZERO, Priority.HIGH),
    SILVER(new BigDecimal("0.05"), Money.of(50), Priority.NORMAL),
    BRONZE(BigDecimal.ZERO, Money.of(100), Priority.LOW);

    private final BigDecimal discountRate;
    private final Money shippingFee;
    private final Priority supportPriority;
    // konstruktor va getterlar

    public Money discountOn(Money total) { return total.multiply(discountRate); }
}
// Foydasi: yangi daraja qo'shilganda kompilyator uch joyni emas, bir joyni
// talab qiladi va hech narsa esdan chiqmaydi.

// Review javobi 2: qoida murakkab bo'lsa (tashqi bog'liqlik kerak) - Strategy.
public interface TierPolicy {
    CustomerTier tier();
    Money discountOn(Money total);
    Money shippingFee(Weight weight);
}
@Component
class GoldPolicy implements TierPolicy { /* ... */ }
// Spring List<TierPolicy> ni o'zi yig'adi; registr 9.2 da ko'rsatilgan.
```

Qachon `switch` qoldiriladi: bitta joyda, kichik va barqaror to'plam uchun. `sealed interface` bilan birga ishlatilsa, kompilyator to'liqligini tekshiradi - bu holat polimorfizmdan ham yaxshiroq bo'lishi mumkin (17-bob).

### 10.3 Yaratish mantiqi tarqalganda: fabrika

Belgi: bir xil obyektni qurish uchun kerak bo'lgan to'rt qator uch joyda takrorlangan, va ularning biri boshqalaridan farq qiladi (xato shu farqda).

```java
// Belgi: audit yozuvini qurish uch joyda takrorlangan, biri zonani
// boshqacha qo'ygan - hisobotlarda bir soatlik siljish.
AuditEvent e = new AuditEvent();
e.setUserId(currentUser.getId());
e.setAt(LocalDateTime.now());                 // boshqa joyda Instant.now()
e.setAction("ORDER_CANCELLED");
e.setDetails(objectMapper.writeValueAsString(order));

// Review javobi: yaratish qoidasi bitta joyda, nomlangan fabrika metodi bilan.
public record AuditEvent(UserId userId, Instant at, AuditAction action, String payloadJson) {

    public static AuditEvent of(UserId user, AuditAction action, Object payload, Clock clock) {
        return new AuditEvent(user, clock.instant(), action, Json.write(payload));
    }
}
// Foydasi: vaqt manbasi bitta (Clock - testlanadi), serializatsiya bitta,
// va yangi majburiy maydon qo'shilsa kompilyator hamma joyni ko'rsatadi.
```

### 10.4 Parametrlar portlashi: builder yoki parametr obyekti

Belgi: konstruktor yoki metodda 6+ parametr, ularning bir nechtasi bir xil turda. Oqibati: parametrlarni almashtirib qo'yish kompilyatsiyada tutilmaydi.

```java
// Xavfli: besh String ketma-ket. Almashtirilsa, kompilyator jim.
new ShipmentRequest(orderId, address, city, region, postalCode, phone, note);

// Yechim 1: domen turlari (eng ishonchli).
new ShipmentRequest(new OrderId(id), new Address(city, region, postalCode), new Phone(phone), note);

// Yechim 2: builder (ixtiyoriy maydonlar ko'p bo'lsa).
ShipmentRequest.builder()
    .orderId(orderId)
    .address(address)
    .phone(phone)
    .note(note)                     // ixtiyoriy
    .build();                       // build() ichida majburiy maydonlar tekshiriladi

// Review diqqati: builder ishlatilsa, majburiy maydonlar tekshirilishi
// shart. Aks holda builder konstruktordan xavfsizroq emas - u faqat
// xatoni kompilyatsiyadan ish vaqtiga ko'chiradi.
```

### 10.5 Kesishgan vazifalar qo'lda yozilganda: decorator yoki AOP

Belgi: o'nta metodda bir xil `try { ... } catch { log; metric }` o'rami. Oqibati: o'n birinchi metodda o'ram esdan chiqadi va xato ko'rinmay qoladi.

```java
// Belgi: har metodda qo'lda retry va o'lchov.
public PaymentResult charge(ChargeCommand cmd) {
    int attempt = 0;
    while (true) {
        long start = System.nanoTime();
        try {
            PaymentResult r = gateway.charge(cmd);
            meter.timer("gateway.charge").record(System.nanoTime() - start, NANOSECONDS);
            return r;
        } catch (GatewayTimeout e) {
            if (++attempt >= 3) throw e;
            sleep(100L * attempt);            // qo'lda backoff, jitter yo'q
        }
    }
}

// Review javobi: tayyor mexanizmlardan foydalanish. Retry siyosati
// deklarativ, o'lchov avtomatik, kod faqat biznes qismini saqlaydi.
@Service
public class PaymentService {

    @Retry(name = "gateway")                  // Resilience4j: backoff + jitter
    @CircuitBreaker(name = "gateway", fallbackMethod = "queueForLater")
    @Timed(value = "gateway.charge")          // Micrometer
    public PaymentResult charge(ChargeCommand cmd) {
        return gateway.charge(cmd);
    }

    private PaymentResult queueForLater(ChargeCommand cmd, CallNotPermittedException e) {
        outbox.enqueue(cmd);
        return PaymentResult.pending();
    }
}
```

```yaml
# Siyosat konfiguratsiyada: review da raqamlar muhokama qilinadi, kod emas.
resilience4j:
  retry:
    instances:
      gateway:
        max-attempts: 3
        wait-duration: 200ms
        enable-exponential-backoff: true
        exponential-backoff-multiplier: 2
        enable-randomized-wait: true          # jitter: retry bo'ronini oldini oladi
        retry-exceptions:
          - java.net.SocketTimeoutException   # faqat qayta urinishga arziydiganlar
        ignore-exceptions:
          - com.acme.payment.CardDeclined     # biznes rad etishi - retry qilinmaydi
  circuitbreaker:
    instances:
      gateway:
        sliding-window-size: 50
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
```

Review da asosiy savol konfiguratsiyaga qaratiladi: qaysi istisnolar retry qilinadi. `retry-exceptions` ga biznes xatolari (karta rad etildi, yetarli mablag' yo'q) kirib qolsa, tizim bir xil rad etishni uch marta takrorlaydi va foydalanuvchiga uch marta SMS keladi.

### 10.6 Holat shoxlari: yashiringan holat mashinasi

Belgi: `status` maydoni bo'yicha `if` lar turli joylarda, va holat o'tishlari `setStatus` bilan qo'lda qilinadi. Oqibati: taqiqlangan o'tish (bekor qilingan buyurtmani jo'natish) hech narsa bilan to'xtatilmaydi.

```java
// Review javobi: o'tishlarni aniq e'lon qilish. Oddiy va o'qiladigan shakl.
public enum OrderStatus {
    NEW(EnumSet.of(PAID, CANCELLED)),
    PAID(EnumSet.of(SHIPPED, REFUNDED)),
    SHIPPED(EnumSet.of(DELIVERED)),
    DELIVERED(EnumSet.noneOf(OrderStatus.class)),   // terminal
    CANCELLED(EnumSet.noneOf(OrderStatus.class)),
    REFUNDED(EnumSet.noneOf(OrderStatus.class));

    private final Set<OrderStatus> allowed;
    OrderStatus(Set<OrderStatus> allowed) { this.allowed = allowed; }

    public void checkTransitionTo(OrderStatus next) {
        if (!allowed.contains(next)) {
            throw new IllegalStateTransition(this, next);
        }
    }
}
// Order ichida:
public void transitionTo(OrderStatus next) {
    status.checkTransitionTo(next);
    this.status = next;
}
// Foydasi: taqiqlangan o'tish bitta joyda to'xtatiladi, va o'tishlar
// jadvali kodda hujjat sifatida turadi. Testda ham o'tish matritsasini
// to'liq tekshirish mumkin (34-bob).
```

Qo'shimcha review savoli: holat o'tishi ma'lumotlar bazasida ham himoyalanganmi. Ikki parallel so'rov bir vaqtda `PAID` dan `SHIPPED` va `REFUNDED` ga o'tkazishi mumkin. Shu sababli o'tish `UPDATE ... WHERE status = 'PAID'` shaklida yoki optimistik versiya bilan bajarilishi kerak (27-bob).

### 10.7 Tashqi tizim domen ichida: adapter va port

Belgi: domen yoki servis kodida `RestClient`, `WebClient`, SDK klassi yoki `HttpHeaders` ko'rinadi. Oqibati: domen testi tarmoqqa bog'liq bo'ladi, vendor almashtirilsa biznes kodi o'zgaradi, va vendor xato formatlari biznes mantiqiga tarqaydi.

```java
// Belgi: biznes metodi HTTP detallarini biladi.
public Order place(PlaceOrder cmd) {
    HttpHeaders h = new HttpHeaders();
    h.setBearerAuth(tokenStore.get());
    ResponseEntity<Map> resp = restTemplate.exchange(
        "https://fraud.vendor.io/v2/score", POST, new HttpEntity<>(body, h), Map.class);
    if (((Number) resp.getBody().get("score")).intValue() > 80) {   // "magic" 80
        throw new FraudSuspected();
    }
    ...
}

// Review javobi: port domen tilida, adapter detallarni yashiradi.
public interface FraudScoring {                      // domen porti
    FraudVerdict score(OrderDraft draft);
}
public enum FraudVerdict { ALLOW, REVIEW, BLOCK }

@Component
class VendorFraudScoring implements FraudScoring {   // infra adapteri
    @Override public FraudVerdict score(OrderDraft draft) {
        ScoreResponse r = client.post()... .body(ScoreResponse.class);
        return r.score() > blockThreshold ? BLOCK
             : r.score() > reviewThreshold ? REVIEW : ALLOW;
    }
}
// Foydasi: chegara raqamlari bitta joyda va konfiguratsiyada; domen
// faqat uch holatni biladi; test uchun tarmoq kerak emas.
```

### 10.8 Yozuv va xabar birga bo'lishi kerak bo'lganda: outbox

Belgi: bitta metodda `repository.save(...)` va keyin `kafkaTemplate.send(...)` yoki tashqi HTTP chaqiruvi. Oqibati: ikkisidan biri bajarilib, ikkinchisi bajarilmasligi mumkin, va tizim holatlari ajralib ketadi.

```java
// Belgi: ikki tizimga yozuv, atomiklik yo'q.
@Transactional
public void place(PlaceOrder cmd) {
    Order order = orders.save(Order.from(cmd));
    kafka.send("orders", new OrderPlaced(order.id()));   // commit dan oldin!
}
// Uch xil nosozlik: (1) kafka o'tdi, commit yiqildi - xabar bor, buyurtma
// yo'q; (2) commit o'tdi, kafka yiqildi - buyurtma bor, xabar yo'q;
// (3) kafka sekin - DB tranzaksiyasi va qulf uzoq ushlanadi.

// Review javobi: xabar bir xil tranzaksiyada jadvalga yoziladi.
@Transactional
public void place(PlaceOrder cmd) {
    Order order = orders.save(Order.from(cmd));
    outbox.save(OutboxMessage.of("orders", new OrderPlaced(order.id())));  // atomik
}
```

```sql
-- Outbox jadvali va uning indeksi: workerlar bir-birini kutmaydi.
CREATE TABLE outbox_message (
    id           bigserial PRIMARY KEY,
    topic        text        NOT NULL,
    payload      jsonb       NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now(),
    published_at timestamptz,
    attempts     int         NOT NULL DEFAULT 0
);
-- Faqat yuborilmaganlar uchun partial indeks: jadval o'sganda ham kichik.
CREATE INDEX outbox_pending_idx ON outbox_message (created_at)
    WHERE published_at IS NULL;
```

Review ning qo'shimcha savollari: outbox tozalanadimi (aks holda jadval cheksiz o'sadi), xabar tartibi muhimmi (bo'lsa, agregat bo'yicha ketma-ketlik kerak), va iste'molchi dublikatga tayyormi (outbox "kamida bir marta" yetkazadi).

### 10.9 Ikki marta kelgan so'rov: idempotentlik

Belgi: tashqaridan keladigan yozuv operatsiyasida (to'lov, buyurtma, xabar iste'moli) takrorlanishga qarshi himoya yo'q. Oqibati: foydalanuvchi ikki marta bosganida ikki to'lov, retry dan keyin ikki buyurtma, Kafka qayta yetkazganida ikki yozuv.

```java
// Review javobi: kalit tashqaridan keladi, yagonalik bazada majburlanadi.
@PostMapping("/payments")
public ResponseEntity<PaymentResponse> pay(
        @RequestHeader("Idempotency-Key") @NotBlank String idemKey,
        @Valid @RequestBody PaymentRequest req) {
    return ResponseEntity.ok(payments.charge(idemKey, req));
}

@Transactional
public PaymentResponse charge(String idemKey, PaymentRequest req) {
    // 1) Avval kalitni band qilish: DB unique constraint - yagona ishonchli
    //    himoya (ikki instans, ikki thread, retry - hammasi uchun).
    try {
        idempotency.save(new IdempotencyRecord(idemKey, hash(req)));
        em.flush();                       // konfliktni shu yerda bilish uchun
    } catch (DataIntegrityViolationException dup) {
        // 2) Takroriy so'rov: oldingi natijani qaytaramiz, ikki marta
        //    to'lamaymiz. So'rov tanasi boshqacha bo'lsa - 409.
        IdempotencyRecord prev = idempotency.getByKey(idemKey);
        if (!prev.requestHash().equals(hash(req))) {
            throw new IdempotencyKeyReused(idemKey);
        }
        return prev.storedResponse();
    }
    PaymentResponse resp = gateway.charge(req);
    idempotency.storeResponse(idemKey, resp);
    return resp;
}
```

```sql
CREATE TABLE idempotency_record (
    key           text        PRIMARY KEY,          -- yagonalik kafolati
    request_hash  text        NOT NULL,
    response      jsonb,
    created_at    timestamptz NOT NULL DEFAULT now()
);
-- Oyna: eski kalitlar tozalanadi, aks holda jadval cheksiz o'sadi.
CREATE INDEX idempotency_created_idx ON idempotency_record (created_at);
```

Review ning asosiy diqqati: kalit qayerda tekshiriladi. Agar `findByKey` keyin `save` qilinsa, bu poyga - ikki parallel so'rov ikkisi ham "topilmadi" deb o'tadi. Faqat unique constraint ishonchli.

### 10.10 Ko'p bosqichli jarayon: saga va kompensatsiya

Belgi: bitta metodda uch-to'rt tashqi tizim ketma-ket chaqiriladi. Oqibati: uchinchisi yiqilganda birinchi ikkisi bajarilgan holda qoladi, va tizim nomuvofiq holatda.

```java
// Belgi: to'rt qadam, qaytarish yo'q.
public void checkout(Cart cart) {
    inventory.reserve(cart);          // 1
    Payment p = payments.charge(cart);// 2  - bu yiqilsa, 1 qaytarilmaydi
    shipping.schedule(cart);          // 3  - bu yiqilsa, 1 va 2 qoladi
    notifications.send(cart);         // 4
}

// Review javobi: har qadamning kompensatsiyasi aniq, holat saqlanadi.
// Oddiy shakl: holat jadvalida qadamlarni belgilash va worker bilan davom
// ettirish (to'liq saga freymvorki kerak emas).
public enum CheckoutStep { RESERVED, PAID, SCHEDULED, NOTIFIED }

@Transactional
public void advance(CheckoutId id) {
    Checkout c = checkouts.lockById(id);          // SELECT ... FOR UPDATE
    switch (c.nextStep()) {
        case RESERVED  -> { inventory.reserve(c); c.mark(RESERVED); }
        case PAID      -> { payments.charge(c);   c.mark(PAID); }
        case SCHEDULED -> { shipping.schedule(c); c.mark(SCHEDULED); }
        case NOTIFIED  -> { notifications.send(c); c.complete(); }
    }
}
// Kompensatsiya: PAID dan keyin SCHEDULED uch marta yiqilsa,
// payments.refund(c) chaqiriladi va inventory.release(c) bajariladi.
```

Review da saga uchun uch savol: har qadam idempotentmi (worker qayta urinadi), kompensatsiya ham yiqilishi mumkinmi (ikkinchi darajali himoya kerak), va jarayon qotib qolganini qanday bilamiz (eng muhim savol - metrika va alert, 39-bob).

### 10.11 Pattern taklif qilishning narxi

Pattern taklif qilgan reviewer uning narxini ham aytishi kerak. Har bir pattern kod hajmini oshiradi, navigatsiyani uzaytiradi va yangi odam uchun o'rganish yuki qo'shadi.

| Pattern | Tipik narxi | Qachon arzimaydi |
| --- | --- | --- |
| Strategy | 1 interfeys + N klass + registr | Ikki holat, o'zgarmaydi |
| Builder | 30-60 satr (yoki kutubxona) | Record va 3 parametr yetadi |
| Outbox | Jadval, worker, tozalash, monitoring | Xabar yo'qolishi muhim emas |
| Saga | Holat jadvali, worker, kompensatsiya | Bir tizimli tranzaksiya yetadi |
| CQRS | Ikki model, sinxronizatsiya | O'qish yuki kichik |
| Event sourcing | Event do'koni, proyeksiya, migratsiya | Tarix talab qilinmaydi |
| Adapter/port | 1 interfeys + 1 klass | Vendor almashtirilmaydi va test oson |

Shu sababli review izohining to'g'ri shakli: "bu yerda Strategy kerak" emas, balki "shu `switch` uchinchi joyda takrorlandi, yangi tur qo'shilganda uchtasini eslash kerak; enum ichiga xulqni olsak, bitta joy qoladi, narxi 20 satr". Birinchi shakl buyruq, ikkinchisi muhandislik taklifi.

### 10.12 Amalda qo'llash

- [ ] Loyihadagi barcha enum larni sanab, har biri bo'yicha nechta joyda `switch`/`if` borligini aniqlang; uchdan ko'p joy bo'lsa, xulqni enum ga yoki Strategy ga ko'chirishni rejalashtiring.
- [ ] `repository.save` va `kafka.send` (yoki tashqi HTTP) bir metodda uchraydigan joylarni grep bilan topib, har biri uchun outbox kerakligini baholang.
- [ ] Tashqaridan kelgan barcha yozuv endpointlarini sanab, ularning qanchasida idempotentlik kaliti borligini jadvalga yozing.
- [ ] Idempotentlik `findBy` + `save` orqali qilingan joylarni toping - ularni unique constraint ga o'tkazish majburiy.
- [ ] Qo'lda yozilgan retry sikllarini toping va ularni Resilience4j yoki Spring Retry ga o'tkazing; `retry-exceptions` ro'yxatida biznes xatolari yo'qligini tasdiqlang.
- [ ] `status` bo'yicha shoxlanishlarni toping va o'tish matritsasini enum ichida e'lon qiling.
- [ ] Domen va servis paketlarida `RestClient`, `WebClient`, SDK importlarini qidirib, ularni adapter ortiga ko'chirish ro'yxatini tuzing.
- [ ] Ko'p qadamli jarayonlarni (uchdan ko'p tashqi chaqiruv) aniqlab, har biri uchun "uchinchi qadam yiqilsa nima bo'ladi" savoliga yozma javob oling.

## 11. Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern (Misapplied and Over-Applied Patterns)

Pattern bo'shlig'idan ko'ra xavfliroq holat bor: pattern qo'llangan, nomi to'g'ri, lekin mexanikasi buzilgan. Bunday kod review dan osongina o'tadi, chunki u tanish nomlar bilan bezatilgan. Reviewer `Strategy`, `Factory`, `Repository` so'zini ko'radi va ishonadi. Bu bob shu ishonchni tekshirishni o'rgatadi: pattern nomi ostida nima ishlayotganini ko'rish.

### 11.1 Noto'g'ri qo'llangan patternning umumiy belgilari

| Belgi | Nimani bildiradi |
| --- | --- |
| Pattern nomi klass nomida, lekin mexanikasi yo'q | Nom bezak sifatida ishlatilgan |
| Strategy bor, lekin tanlash `if` bilan | Shoxlanish ko'chmagan, faqat ko'paygan |
| Factory ichida `switch` va `new` | Yaratish markazlashgan, lekin yopiq emas |
| Interfeys bor, bitta implementatsiya | Soxta abstraksiya (7-bob) |
| Builder majburiy maydonlarni tekshirmaydi | Xato kompilyatsiyadan ish vaqtiga ko'chgan |
| Repository ichida biznes qoidasi | Qatlam aralashgan |
| Event yuborilgan, lekin tranzaksiya bilan bog'lanmagan | Yetkazish kafolati yo'q |
| Observer tartibga tayanadi | Yashirin vaqt bog'liqligi |
| Singleton `getInstance()` Spring loyihasida | Ikki xil hayot sikli, test qiyin |
| Decorator zanjiri uch darajadan chuqur | Nosozlikni kuzatish imkonsiz |
| Abstract base class bitta vorisi bilan | Meros kodni qayta ishlatish uchun |
| Generic parametr hech qayerda almashmaydi | Ortiqcha ceremony |

### 11.2 Strategy nomi bor, shoxlanish ham bor

Eng ko'p uchraydigan yarim qo'llanish: interfeys va implementatsiyalar yozilgan, lekin ularni tanlash joyida yana `switch` turadi. Natijada kod hajmi oshdi, lekin OCP qo'lga kirmadi - yangi tur qo'shilganda yana shu `switch` ni topish kerak.

```java
// Yarim qo'llanish: Strategy bor, lekin tanlash qo'lda.
@Service
public class FeeService {
    private final CardFee cardFee;
    private final WalletFee walletFee;
    private final CryptoFee cryptoFee;

    public Money fee(Payment p) {
        switch (p.type()) {                       // yangi tur = shu joyni tuzatish
            case CARD -> { return cardFee.of(p); }
            case WALLET -> { return walletFee.of(p); }
            case CRYPTO -> { return cryptoFee.of(p); }
            default -> throw new IllegalStateException();
        }
    }
}

// To'liq qo'llanish: tanlash ham ko'chgan, yangi tur faqat yangi klass.
public interface FeePolicy {
    PaymentType appliesTo();
    Money of(Payment payment);
}

@Service
public class FeeService {
    private final Map<PaymentType, FeePolicy> policies;

    public FeeService(List<FeePolicy> all) {
        this.policies = all.stream().collect(toMap(FeePolicy::appliesTo, identity()));
        // Ishga tushishda to'liqlikni tekshirish: har enum qiymatiga policy bormi.
        EnumSet<PaymentType> missing = EnumSet.allOf(PaymentType.class);
        missing.removeAll(policies.keySet());
        if (!missing.isEmpty()) {
            throw new IllegalStateException("FeePolicy yo'q: " + missing);
        }
    }
    public Money fee(Payment p) { return policies.get(p.type()).of(p); }
}
// Review foydasi: yangi PaymentType qo'shilsa va policy yozilmasa, ilova
// ishga tushishda yiqiladi - prodda jim xato bo'lmaydi. Bu "fail fast"
// yondashuvi Strategy ni polimorfizmdan ham ishonchli qiladi.
```

### 11.3 Fabrika yoki yashirin service locator

`Factory` nomi ostida ko'pincha service locator yashiringan bo'ladi: klass o'z bog'liqliklarini kontekstdan o'zi oladi. Bu bog'liqlikni yashiradi, testni qiyinlashtiradi va ishga tushish vaqtidagi xatoni ish vaqtiga ko'chiradi.

```java
// Service locator: bog'liqlik konstruktorda ko'rinmaydi.
@Component
public class HandlerFactory {
    private final ApplicationContext ctx;          // hamma narsaga kirish

    public Handler forType(String type) {
        return ctx.getBean(type + "Handler", Handler.class);   // satr bo'yicha!
    }
}
// Muammolar: (1) bog'liqlik grafigi ko'rinmaydi, (2) yo'q bean faqat
// chaqiruv paytida xato beradi, (3) bean nomi satr konkatenatsiyasi bilan
// qurilgan - refactoring uni buzadi va kompilyator sezmaydi,
// (4) testda butun kontekst kerak.

// To'g'ri: bog'liqliklar aniq, xato ishga tushishda chiqadi.
@Component
public class Handlers {
    private final Map<EventType, Handler> byType;
    public Handlers(List<Handler> handlers) {
        this.byType = handlers.stream().collect(toMap(Handler::handles, identity()));
    }
    public Handler forType(EventType type) {
        Handler h = byType.get(type);
        if (h == null) throw new NoHandlerFor(type);
        return h;
    }
}
```

### 11.4 Repository patternining buzilgan shakllari

`Repository` eng ko'p noto'g'ri ishlatiladigan nom. Uning mohiyati - domen obyektlari to'plamiga kirish, ma'lumotlar bazasi API si emas. Review da uch xil buzilish uchraydi.

```java
// Buzilish 1: repository ichida biznes qoidasi.
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("""
        select o from Order o
        where o.status = 'PAID'
          and o.total > 1000000
          and o.customer.tier = 'GOLD'
        """)
    List<Order> findEligibleForBonus();      // "bonus huquqi" - biznes qoidasi
}
// Review izohi: bonus shartlari JPQL satrida yashiringan. Qoida o'zgarsa,
// uni domen testida emas, repository testida tekshirish kerak bo'ladi, va
// shart kodda qidirilmaydi. Shartni domen (yoki spetsifikatsiya) ga
// ko'chirish, repository ga esa faqat kerakli ma'lumotni olish qoldirish.

// Buzilish 2: repository ichida N+1 keltiradigan qulay metod.
List<Order> findAll();                        // 200 000 qator - keyin filtr Java da

// Buzilish 3: repository tashqariga JPA turlarini chiqaradi.
Page<Order> search(Specification<Order> spec, Pageable page);
// Domen Spring Data turlarini bilib qoladi - port oqib chiqdi (7.6).

// To'g'ri shakl: domen tilida so'rovlar va aniq qaytish turlari.
public interface Orders {                     // domen porti
    Optional<Order> byNumber(OrderNumber number);
    List<Order> awaitingShipment(ShippingWindow window, int limit);
    void save(Order order);
}
```

### 11.5 Event noto'g'ri qo'llanganda

Spring `ApplicationEvent` lari bilan ishlash osonligi tufayli eng ko'p xato shu yerda bo'ladi. Uch xil xato uchraydi va ularning hammasi jim ishlaydi.

```java
// Xato 1: event tranzaksiya ichida sinxron ishlanadi va uni buzadi.
@EventListener
public void on(OrderPlaced e) {
    mailer.send(...);           // tranzaksiya ichida, sekin tashqi chaqiruv
}
// Standart @EventListener sinxron: publish chaqirilgan thread da ishlaydi,
// ya'ni tranzaksiya ichida. Mail serveri sekin bo'lsa, DB tranzaksiyasi
// shuncha uzoq turadi.

// Xato 2: AFTER_COMMIT ishlatilgan, lekin xato yutiladi.
@TransactionalEventListener(phase = AFTER_COMMIT)
public void on(OrderPlaced e) {
    inventory.reserve(e.orderId());   // bu yiqilsa - hech kim bilmaydi,
}                                     // tranzaksiya allaqachon commit bo'lgan

// Xato 3: event ichida entity uzatilgan.
events.publish(new OrderPlaced(order));   // detached entity, lazy maydonlar
// Listener boshqa thread da bo'lsa - LazyInitializationException yoki
// eskirgan holat. Eventda identifikator va immutable qiymatlar bo'lishi kerak.

// To'g'ri shakllar:
// (a) Ichki, muhim bo'lmagan ish - AFTER_COMMIT + xato ishlash.
@TransactionalEventListener(phase = AFTER_COMMIT)
public void sendConfirmation(OrderPlaced e) {
    try { mailer.send(e.orderId()); }
    catch (Exception ex) { log.warn("tasdiq xati yuborilmadi: {}", e.orderId(), ex);
                           meter.counter("mail.failed").increment(); }
}
// (b) Muhim ish (inventar, to'lov) - event emas, outbox (10.8).
// (c) Eventda faqat identifikator va qiymat obyektlari.
public record OrderPlaced(OrderId orderId, Money total, Instant at) { }
```

Review savoli har doim bitta: bu event yo'qolsa, tizim nomuvofiq holatda qoladimi. Javob "ha" bo'lsa, event yetarli emas - kafolatli mexanizm kerak.

### 11.6 Dekorator zanjiri va kuzatib bo'lmaydigan oqim

Dekorator foydali, lekin uch darajadan chuqur zanjir nosozlikni tushunishni imkonsiz qiladi: stack trace da o'nta `invoke` ko'rinadi va qaysi daraja qaror qabul qilganini bilib bo'lmaydi.

```java
// Juda chuqur: beshta o'ram, har biri xulqni o'zgartiradi.
new LoggingRepo(new CachingRepo(new RetryingRepo(new MetricsRepo(new JpaRepo()))));
// Review savollari: kesh retry dan oldinmi yoki keyinmi? Retry keshlangan
// xatoni qaytaradimi? Metrika qaysi darajada o'lchanadi - keshdan oldin
// yoki keyin? Bu savollarning javobi tartibga bog'liq, lekin tartib hech
// qayerda hujjatlashtirilmagan.

// Yaxshiroq: kesishgan vazifalarni framework mexanizmiga topshirish
// (@Cacheable, @Retryable, @Timed) va zanjirni ikki darajada ushlab turish.
// Yoki tartibni aniq e'lon qilish va sabab bilan izohlash:
@Bean
Orders orders(JpaOrders jpa, CacheManager cm, RetryTemplate rt) {
    // Tartib ahamiyatli: retry keshdan ICHKARIDA - keshlangan natija
    // uchun qayta urinish bo'lmaydi, faqat haqiqiy DB xatosi uchun.
    return new CachingOrders(cm, new RetryingOrders(rt, jpa));
}
```

### 11.7 Singleton, statik holat va Spring

Spring loyihasida `getInstance()` ko'rilsa, bu ikki xil hayot sikli degani: Spring bean lari va qo'lda boshqarilgan statik holat. Oqibatlari: testlar bir-biriga ta'sir qiladi, konfiguratsiya ikki joydan keladi, va ishga tushish tartibi aniqlanmaydi.

```java
// Muammo: statik singleton va Spring bean aralashgan.
public class RateCache {
    private static final RateCache INSTANCE = new RateCache();
    public static RateCache getInstance() { return INSTANCE; }
    private final Map<String, BigDecimal> rates = new HashMap<>();  // thread-safe emas
    public void put(String c, BigDecimal r) { rates.put(c, r); }
}
// Review izohlari: (1) HashMap bir vaqtda o'qilib va yozilsa - buzilish
// yoki cheksiz sikl; (2) testlar orasida holat saqlanadi, test tartibi
// natijaga ta'sir qiladi; (3) kesh hajmi cheklanmagan - xotira o'sadi.

// To'g'ri: bean, aniq kesh, cheklangan hajm va TTL.
@Configuration
class CacheConfig {
    @Bean
    Cache<String, BigDecimal> rateCache() {
        return Caffeine.newBuilder()
                       .maximumSize(1_000)            // hajm cheklangan
                       .expireAfterWrite(Duration.ofMinutes(10))   // yangilik oynasi
                       .recordStats()                 // metrikaga ulanadi
                       .build();
    }
}
```

### 11.8 CQRS, event sourcing va saga: ortiqcha qo'llanish

Bu uchlik eng qimmat patternlar va eng ko'p asossiz qo'llanadigan patternlar. Review da ularning har biri uchun aniq shart bor; shart bajarilmasa, narx foydadan katta.

| Pattern | Qo'llashga asos bo'ladigan shart | Shart yo'q bo'lsa narxi |
| --- | --- | --- |
| CQRS (alohida o'qish modeli) | O'qish yuki yozuvdan bir necha baravar katta, yoki o'qish shakli yozuvdan tubdan farq qiladi | Ikki model sinxronizatsiyasi, eventual consistency bilan bog'liq xatolar, ikki baravar kod |
| Event sourcing | Tarix va auditning o'zi biznes talabi; holatni qayta hisoblash kerak | Migratsiya murakkabligi, so'rovlar uchun proyeksiya, yangi odam uchun yuqori yuk |
| Saga | Bir operatsiya uch va ko'p mustaqil tizimga tegadi | Holat jadvali, worker, kompensatsiya, kuzatish - oddiy tranzaksiya yetadigan joyda |
| Microservice ajratish | Mustaqil deploy va mustaqil masshtablash kerak | Tarmoq, kuzatish, taqsimlangan tranzaksiya muammolari |
| Hexagonal to'liq shakli | Bir nechta tashqi adapter real almashtiriladi | Har oddiy maydon uchun to'rt klass |

```text
# Review izohi: ortiqcha patternni rad etishning to'g'ri shakli.
question: Bu PR da buyurtma o'qish uchun alohida proyeksiya jadvali va
uni to'ldiradigan listener qo'shilgan (CQRS). Uch savol:

1) Hozirgi o'qish yuki qancha? Metrikada buyurtma o'qish p99 = 40 ms,
   kuniga 12 ming so'rov - bu bitta jadval uchun katta yuk emas.
2) Proyeksiya kechikishi biznes uchun qabul qilinadimi? Foydalanuvchi
   buyurtma yaratib, darhol ro'yxatda ko'rmasligi mumkin.
3) Proyeksiya buzilsa (listener xatosi), uni qanday qayta quramiz?

Agar maqsad faqat so'rovni tezlashtirish bo'lsa, avval indeks va
projection interfeysi bilan o'lchab ko'rsak - narxi nol. CQRS ga o'tish
uchun o'lchangan dalil bo'lsa, qaytib kelamiz va ADR yozamiz.
```

### 11.9 Mapper va DTO qatlamlarining haddan oshishi

Har qatlam uchun alohida model yaratish qoidasi mexanik qo'llanganda, bitta maydon qo'shish uchun olti faylga tegish kerak bo'ladi.

```text
Request DTO -> Command -> Domain -> Entity -> Projection -> Response DTO
```

Review mezoni - har bir model alohida sababga ko'ra o'zgaradimi. Agar `Command` va `Request DTO` har doim birga o'zgarsa va maydonlari bir xil bo'lsa, ular bitta model. Teskarisi ham to'g'ri: tashqi API shakli va jadval sxemasi mustaqil o'zgarsa, ularni ajratish zarur.

| Chegara | Ajratish kerakmi | Sabab |
| --- | --- | --- |
| Tashqi API va domen | Ha | API shartnomasi, versiyalash, orqaga moslik |
| Domen va jadval | Odatda ha | Sxema migratsiyasi, ORM talablari |
| Request DTO va Command | Odatda yo'q | Bir xil sababga ko'ra o'zgaradi |
| O'qish javobi va entity | Ha | Projection samaraliroq, ortiqcha maydon chiqmaydi |
| Ichki servislar orasida | Yo'q | Bir xil deploy birligi |

### 11.10 Pattern teatri: nom bilan yashirilgan murakkablik

Eng qiyin holat - kod pattern nomlari bilan to'lgan, lekin hech bir pattern o'z vazifasini bajarmaydi. Belgilari: `AbstractBaseServiceFactoryProvider` tipidagi nomlar, uch daraja meros, har bir interfeysga bitta implementatsiya, va eng oddiy operatsiya uchun o'n faylga sakrash.

Bunday PR ni review qilishning to'g'ri usuli - bitta oddiy ssenariyni oxirigacha kuzatish va necha faylga sakrash kerakligini sanash. Keyin shu sonni izohda ko'rsatish: "bitta buyurtma yaratish yo'lini tushunish uchun 11 fayl ochish kerak bo'ldi". Bu raqam did bahsidan ko'ra ishonchliroq dalil.

```bash
# Murakkablikni raqamda ko'rsatish: bitta operatsiya yo'lidagi fayllar.
# Chaqiruv zanjirini kuzatish (IDE bo'lmaganda ham ishlaydi).
start='placeOrder'
for i in 1 2 3 4 5; do
  echo "--- daraja $i: $start"
  grep -rn --include='*.java' "$start(" src/main/java | head -5
  # keyingi darajaga qo'lda o'tiladi; maqsad - sakrash sonini sanash
done

# Meros chuqurligi: uch darajadan chuqur ierarxiyalar.
grep -rn --include='*.java' 'extends Abstract' src/main/java | wc -l
```

### 11.11 Pattern review jadvali: belgi, savol, javob

| Ko'rilgan narsa | Review savoli | Yaxshi javob bo'lmasa |
| --- | --- | --- |
| Yangi interfeys | Ikkinchi implementatsiya bormi yoki rejadami | Interfeysni olib tashlash |
| Yangi `Abstract` klass | Nechta vorisi bo'ladi, umumiy kod shartnomaga tegishlimi | Kompozitsiya |
| Strategy + `switch` | Tanlash nega ko'chmagan | Registr yoki enum xulqi |
| Factory + `ApplicationContext` | Bog'liqliklar nega ko'rinmaydi | Konstruktor inyeksiyasi |
| Builder | Majburiy maydonlar qayerda tekshiriladi | `build()` da tekshirish yoki record |
| Event | Yo'qolsa nima bo'ladi | Outbox yoki sinxron chaqiruv |
| `@Async` | Xato qayerga boradi, pool qaysi | `AsyncUncaughtExceptionHandler` va aniq pool |
| Kesh | Invalidatsiya qachon, hajmi cheklanganmi | TTL, maksimal hajm, metrika |
| Yangi proyeksiya jadvali | Qayta qurish yo'li bormi | Oddiy indeks bilan boshlash |
| Saga | Har qadam idempotentmi | Holatni jadvalga yozish |
| Decorator zanjiri | Tartib nega shunday | Framework mexanizmiga o'tkazish |
| Generic parametr | Qayerda almashadi | Konkret turga tushirish |

### 11.12 Amalda qo'llash

- [ ] Loyihada `Strategy`, `Factory`, `Provider`, `Manager` nomli klasslarni toping va har birida pattern mexanikasi haqiqatda ishlayotganini tekshiring.
- [ ] `ApplicationContext` yoki `BeanFactory` inyeksiya qilingan joylarni toping - har biri yashirin service locator.
- [ ] `getBean("..." + suffix)` shaklidagi satr bilan bean izlashni butunlay olib tashlang.
- [ ] Strategy registrlariga ishga tushish vaqtidagi to'liqlik tekshiruvini qo'shing (har enum qiymatiga implementatsiya bormi).
- [ ] Repository interfeyslarini ko'rib chiqing: JPQL ichida biznes sharti bor metodlarni aniqlab, qoidani domenga ko'chirishni rejalashtiring.
- [ ] Barcha `@EventListener` larni sanab, qaysilari `@TransactionalEventListener` bo'lishi kerakligini va qaysilari outbox ga o'tishi kerakligini belgilang.
- [ ] Eventlarda entity uzatilgan joylarni toping va ularni identifikator va qiymat obyektlariga o'tkazing.
- [ ] `getInstance()` va statik mutable holatni grep bilan topib, bean ga o'tkazish ro'yxatini tuzing.
- [ ] Hajmi va TTL si cheklanmagan keshlarni toping - har biri potensial xotira muammosi.

## 12. Code smell va anti-pattern katalogi diffda (Smells in a Diff)

Bu bob review ning tez ishlatiladigan ma'lumotnomasi: belgi, oqibat va javob. Maqsad - diffda ko'rinadigan naqshni tanib olish va uni oqibat tilida aytish. Smell o'zi xato emas, u xato ehtimolini oshiradigan shakl, shu sababli har bandda "qachon qabul qilinadi" ustuni ham bor.

### 12.1 Boshqaruv oqimi smell lari

| Smell | Diffdagi belgisi | Oqibati | Qachon qabul qilinadi |
| --- | --- | --- | --- |
| Ichma-ich shartlar | Uch va ko'p daraja `if` | Chegaraviy holat ko'rinmaydi | Qisqa va chiziqli bo'lsa |
| Bo'sh `catch` | `catch (Exception e) { }` | Xato yo'qoladi, incident ko'r bo'ladi | Deyarli hech qachon |
| `catch (Exception)` keng | Barcha xatolar bir xil ishlanadi | Dasturlash xatosi biznes xatosi kabi ko'rinadi | Chegara qatlamida, log bilan |
| Bayroq parametr | `process(order, true)` | Chaqiruv joyi o'qilmaydi | Ichki private metodda |
| `null` qaytarish | `return null;` | Chaqiruvchida NPE xavfi | Ichki, tez yo'lda (hujjatlangan) |
| Istisno bilan boshqaruv | `try { parse() } catch { default }` | Sekin va niyat yashirin | Tashqi API shunday bo'lsa |
| Mantiqsiz standart | `default -> {}` jim o'tkazish | Yangi enum qiymati jim yo'qoladi | Hech qachon |
| Takroriy shart | Bir xil `if` ikki joyda | Bittasi o'zgarmay qoladi | Qisqa va ochiq bo'lsa |

```java
// Eng xavfli naqsh: jim yutilgan xato va jim o'tkazilgan enum.
try {
    inventory.reserve(order);
} catch (Exception e) {              // nima bo'lsa ham davom etadi
    // keyinroq tuzatamiz
}

switch (event.type()) {
    case CREATED -> handleCreated(event);
    case UPDATED -> handleUpdated(event);
    default -> { }                   // DELETED qo'shilsa - jim yo'qoladi
}

// Review javobi: ikkisi ham oqibat bilan aytiladi.
// blocker: inventar band qilish xatosi yutilgan. Buyurtma yaratiladi,
//          lekin tovar band qilinmaydi - ikki mijoz bir mahsulotni oladi.
//          Hech qanday log yoki metrika yo'q, shuning uchun bu holatni
//          mijoz shikoyat qilgandan keyin bilamiz.
// blocker: default -> {} yangi hodisa turini jim yutadi. sealed interface
//          yoki default -> throw qo'yilsa, yangi tur kompilyatsiyada yoki
//          birinchi testda ko'rinadi.
```

### 12.2 Ma'lumot va holat smell lari

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Mutable umumiy holat | `static Map`, `static List` | Poyga, buzilgan ma'lumot, test ta'siri |
| Mutable obyekt kalit sifatida | `HashMap<Order,...>` o'zgaruvchan `Order` | Yo'qolgan yozuvlar |
| `equals` bor, `hashCode` yo'q | Faqat bittasi override qilingan | `HashSet` da dublikatlar |
| JPA entity da `equals` ID bo'yicha, ID generated | Yangi obyekt `hashCode` i o'zgaradi | `Set` da g'alati xulq |
| Ochiq setterlar domenda | `setStatus`, `setTotal` public | Invariant himoyasiz |
| Kolleksiyani tashqariga qaytarish | `return this.lines;` | Tashqaridan o'zgartirish |
| Primitiv obsessiya | Hamma narsa `String`/`long` | Almashtirib qo'yish, validatsiya tarqalishi |
| `Optional` maydon sifatida | `private Optional<X> x;` | Serializatsiya muammosi, ortiqcha o'ram |
| Nullable bo'lgan boolean | `Boolean active` | Uch holatli mantiq |
| Pul `double` da | `double amount` | Yig'ilgan aniqlik xatosi |
| Zonasiz vaqt | `LocalDateTime` saqlashda | Yozgi vaqt va server zonasi muammolari |

```java
// Kolleksiyani himoyalash: eng ko'p o'tkazib yuboriladigan joy.
public class Order {
    private final List<OrderLine> lines = new ArrayList<>();

    // Yomon: tashqaridan o'zgartirish mumkin, invariant buziladi.
    public List<OrderLine> getLines() { return lines; }

    // Yaxshi: o'qish uchun himoyalangan ko'rinish, o'zgartirish metod orqali.
    public List<OrderLine> lines() { return List.copyOf(lines); }

    public void addLine(ProductId product, Quantity qty, Money price) {
        if (status != NEW) throw new IllegalStateException("tasdiqlangan buyurtma");
        if (lines.size() >= MAX_LINES) throw new TooManyLines(MAX_LINES);
        lines.add(new OrderLine(product, qty, price));
        recalculateTotal();                  // invariant: total = qatorlar summasi
    }
}
```

### 12.3 Spring ga xos anti-patternlar

| Anti-pattern | Belgisi | Oqibati |
| --- | --- | --- |
| Maydon inyeksiyasi | `@Autowired` maydonda | Testda konteksttsiz qurilmaydi, immutable emas |
| `@Autowired` bilan setter | Setter orqali bog'liqlik | Yarim qurilgan bean |
| `ApplicationContext` inyeksiyasi | Service locator | Yashirin bog'liqlik |
| Katta `@Configuration` | Yuzlab satrli bean e'lonlari | O'qilmaydi, sinov qiyin |
| `@Transactional` controller da | Tranzaksiya web qatlamida | Uzoq tranzaksiya, OSIV |
| `@Transactional` private metodda | Proxy ishlamaydi | Tranzaksiya yo'q, jim |
| Shu klass ichidan `this.method()` | Proxy chetlab o'tilgan | `@Cacheable`, `@Async` ishlamaydi |
| `@Value` ko'p joyda | Konfiguratsiya tarqalgan | Tipli tekshiruv yo'q |
| Profil bo'yicha biznes mantiqi | `@Profile("prod")` servisda | Prod va test xulqi boshqacha |
| `@ComponentScan` juda keng | Butun paket daraxti | Ishga tushish sekin, kutilmagan beanlar |
| `JpaRepository` controller da | Qatlam o'tkazib yuborilgan | Avtorizatsiya va tranzaksiya yo'q |
| Entity DTO sifatida | Entity controller javobida | Sxema API ga yopishadi, lazy xatolar |
| `@Async` natijasi tashlab ketilgan | `void` qaytaradi, xato yo'qoladi | Jim nosozlik |
| `CommandLineRunner` da migratsiya | Ishga tushishda ma'lumot o'zgartirish | Ikki instansda poyga |

```java
// Eng jim xato: shu klass ichidan chaqiruv proxy ni chetlab o'tadi.
@Service
public class OrderService {

    @Transactional
    public void placeAll(List<PlaceOrder> commands) {
        for (PlaceOrder cmd : commands) {
            place(cmd);          // this.place(...) - proxy ishlamaydi!
        }
    }

    @Transactional(propagation = REQUIRES_NEW)   // e'lon qilingan, lekin ishlamaydi
    public void place(PlaceOrder cmd) { ... }
}
// Review izohi (blocker): place() ichki chaqiruv orqali ishga tushadi,
// shuning uchun REQUIRES_NEW qo'llanmaydi - hammasi bitta tranzaksiyada
// ketadi. Bitta buyurtma xatosi butun paketni qaytaradi, niyat esa teskari
// bo'lgan. Yechim: ikki bean ga ajratish (OrderBatch -> OrderService) yoki
// TransactionTemplate ni aniq chaqirish.
```

### 12.4 Ma'lumotlar bazasiga tegishli smell lar

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Siklda so'rov | `for` ichida `repository.findById` | N+1, p99 portlashi |
| `findAll()` keyin Java da filtr | Butun jadval tortiladi | Xotira va kechikish |
| Pagination yo'q | Ro'yxat endpointi limitsiz | Katta javob, OOM |
| `ORDER BY` indekssiz | Yangi tartiblash ustuni | Disk sort, sekin so'rov |
| Dinamik SQL konkatenatsiyasi | `"... WHERE " + field` | SQL injection |
| Tranzaksiya ichida tashqi chaqiruv | HTTP yoki Kafka `@Transactional` ichida | Qulf uzoq, ulanish band |
| `@Transactional` juda keng | Butun servis metodida | Qulflar to'planadi |
| Qulf tartibi turlicha | Ikki joyda teskari tartibda `FOR UPDATE` | Deadlock |
| Migratsiyada `UPDATE` butun jadvalga | Katta jadvalda bir `UPDATE` | Uzoq qulf, replikatsiya lag |
| `SELECT *` | Yangi ustun qo'shilsa ham tortiladi | Tarmoq va xotira |
| Vaqt filtri funksiya bilan | `WHERE date(created_at) = ?` | Indeks ishlatilmaydi |

```sql
-- Review da tez tanib olinadigan ikki naqsh.

-- 1) Indeks ishlatilmaydigan filtr: ustun funksiya ichida.
SELECT * FROM orders WHERE date(created_at) = '2026-10-01';   -- seq scan
-- To'g'risi: oraliq bilan, indeks ishlaydi.
SELECT id, total FROM orders
 WHERE created_at >= '2026-10-01' AND created_at < '2026-10-02';

-- 2) Katta jadvalga "bitta" UPDATE: 12 mln qator, uzoq qulf va WAL to'lishi.
UPDATE orders SET tier = 'BRONZE' WHERE tier IS NULL;
-- To'g'risi: bo'laklab, har bo'lak alohida tranzaksiyada (25-bob).
```

### 12.5 Test smell lari

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Assertion yo'q | Faqat chaqiruv va `assertNotNull` | Hech narsa tekshirilmaydi |
| Mock ni tekshirish | `verify(repo).save(any())` yolg'iz | Implementatsiya tekshirilgan, xulq emas |
| `Thread.sleep` test ichida | Vaqtga tayanish | Beqaror test, sekin pipeline |
| Testlar o'zaro bog'liq | Tartibga tayanish, umumiy holat | Jim buziladi |
| Haqiqiy vaqt ishlatilishi | `LocalDate.now()` | Oyning oxirida yiqiladi |
| Haqiqiy tashqi servis | Tarmoqqa chiqish | Beqaror, sekin |
| Bitta testda o'nta assertion | Har xil holatlar birga | Xato joyi noaniq |
| Test nomi ma'nosiz | `test1`, `shouldWork` | Nosozlikda nima buzilganini bilmaslik |
| Faqat happy path | Chegaraviy holat yo'q | Regressiya tutilmaydi |
| Hamma narsa `@SpringBootTest` | Butun kontekst har testda | Sekin, xatoni lokalizatsiya qilish qiyin |

Test review ning to'liq metodikasi VII bo'limda (34-36-boblar), chunki test to'liqligi alohida tahlil apparatini talab qiladi.

### 12.6 Konkurentlik smell lari

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Tekshir-keyin-yoz | `if (!exists) save()` | Ikki parallel so'rov ikki yozuv |
| `synchronized` bitta instansda | Qulf faqat shu JVM da | Ikki instansda ishlamaydi |
| `ConcurrentHashMap` ichida murakkab yangilash | `get` keyin `put` | Atomik emas |
| `volatile` bilan hisoblash | `volatile int counter; counter++` | Yo'qolgan yangilanishlar |
| Yangi `ExecutorService` har chaqiruvda | `newFixedThreadPool` metod ichida | Thread portlashi |
| Pool yopilmaydi | `shutdown()` yo'q | Thread oqishi |
| `ThreadLocal` tozalanmaydi | `remove()` yo'q | Xotira oqishi, ma'lumot aralashuvi |
| Cheksiz navbat | `new LinkedBlockingQueue<>()` | OOM, orqaga bosim yo'q |
| `CompletableFuture` xatosi tashlab ketilgan | `exceptionally` yo'q | Jim nosozlik |
| Virtual thread ichida `synchronized` bilan uzoq blok | Pinning | Carrier thread band |

### 12.7 Xavfsizlik smell lari (tez ro'yxat)

| Smell | Belgisi |
| --- | --- |
| Koddagi secret | Parol, token satr sifatida |
| Logda maxfiy ma'lumot | `log.info("req={}", request)` to'liq obyekt |
| Avtorizatsiya ID bo'yicha emas | `@PreAuthorize("isAuthenticated()")` yolg'iz |
| Foydalanuvchi ID so'rovdan olinadi | `@RequestParam userId` |
| So'rovdan kelgan ustun nomi | Dinamik `ORDER BY` |
| Fayl yo'li kirishdan quriladi | Path traversal |
| URL kirishdan quriladi | SSRF |
| Deserializatsiya ishonilmagan ma'lumotdan | `ObjectInputStream`, polimorfik Jackson |
| `permitAll` keng naqsh bilan | `/api/**` ochiq |
| CSRF o'chirilgan sababsiz | `csrf().disable()` |
| Xato javobida stack trace | Ichki detallar tashqariga |
| Zaif tasodif | `Math.random()`, `new Random()` token uchun |

Xavfsizlik review ning to'liq metodikasi VI bo'limda (28-33-boblar).

### 12.8 Operatsion smell lar

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Timeout yo'q | `RestClient` yoki `WebClient` sozlamasiz | Thread va pool to'lishi |
| Retry chegarasiz | `while(true)` qayta urinish | Retry bo'roni |
| Log in sikl ichida | Har qator uchun `log.info` | Disk va kechikish |
| Metrika yo'q | Yangi tashqi integratsiya o'lchovsiz | Ko'r incident |
| Health check yuzaki | Faqat "UP" qaytaradi | Yiqilgan bog'liqlik ko'rinmaydi |
| Konfiguratsiya kodda | Qattiq yozilgan URL va chegara | Deploy kerak bo'ladi |
| Feature flag o'chirish sanasi yo'q | Flag doimiy bo'lib qoladi | Shoxlar to'planadi |
| Migratsiya qaytarish rejasi yo'q | Faqat `up` skripti | Reliz qaytarilmaydi |
| Batch ish qulf olmaydi | Ikki instansda bir vaqtda | Ikki marta bajarish |
| Graceful shutdown yo'q | Pod o'ldirilganda ish yarim qoladi | Yo'qolgan xabarlar |

### 12.9 Smell ni oqibat tilida aytish

Katalogdan foydalanishning to'g'ri usuli - nomini aytmaslik, oqibatini aytish. "Bu feature envy" degan izoh muallifni lug'at qidirishga majbur qiladi. "Bu metod Order ning uch darajali ichki tuzilishini biladi, shuning uchun Order o'zgarsa shu hisob sinadi" degan izoh darhol tushunarli.

| Smell nomi (ichki fikr) | Izohda aytiladigan gap |
| --- | --- |
| Feature envy | "Bu hisob Order ning ichki tuzilishiga tayanadi" |
| Shotgun surgery | "Bu o'zgarish 9 faylga bittadan satr qo'shdi" |
| Primitive obsession | "Ikki `long` ni almashtirib qo'ysa, kompilyator sezmaydi" |
| Temporal coupling | "`render()` ni `load()` dan oldin chaqirish NPE beradi" |
| God class | "Bu klass to'rt xil sababga ko'ra o'zgaradi" |
| Anemic model | "Status o'tish qoidasi uch joyda takrorlangan" |
| Leaky abstraction | "Port `HttpClientErrorException` tashlaydi" |

### 12.10 Katalogni loyihaga moslashtirish

Umumiy katalog boshlanish nuqtasi, lekin eng foydali katalog - loyihaning o'z incidentlaridan yozilgani. Har bir incidentdan keyin bitta satr qo'shiladi: belgi, oqibat, qanday topish.

```markdown
<!-- REVIEW-SMELLS.md - loyihaning o'z katalogi, incidentlardan o'sadi. -->
| Sana | Incident | Diffda qanday ko'rinardi | Qanday qidiramiz |
|---|---|---|---|
| 2026-03-11 | To'lov ikki marta o'tdi | `findByKey` keyin `save`, unique yo'q | `grep -rn "findBy.*Key"` + migratsiyada unique |
| 2026-05-02 | Hisobot 40 daqiqa ishladi | Siklda `rateFor()` chaqiruvi | `for` ichida client chaqiruvi |
| 2026-06-19 | Prod qotib qoldi | Tranzaksiya ichida HTTP, timeout yo'q | `@Transactional` + client chaqiruvi |
| 2026-08-07 | Mijoz boshqa buyurtmani ko'rdi | `@PreAuthorize("isAuthenticated()")` | ID bo'yicha tekshiruvsiz endpointlar |
```

Shu jadval review checklistining eng ishonchli qismiga aylanadi, chunki uning har bir bandi loyihada haqiqatan sodir bo'lgan.

### 12.11 Amalda qo'llash

- [ ] `REVIEW-SMELLS.md` faylini yarating va oxirgi beshta incidentni "belgi / oqibat / qanday qidiramiz" shaklida yozing.
- [ ] Bo'sh `catch` va `catch (Exception e)` bloklarini loyihada sanab, ularning har biri uchun log yoki qayta tashlash qo'shing.
- [ ] `default -> { }` va `default: break;` holatlarini toping va ularni istisno tashlashga yoki `sealed` ga o'tkazing.
- [ ] Domen klasslarida tashqariga qaytarilgan mutable kolleksiyalarni toping (`return this.list`) va himoyalangan ko'rinishga o'tkazing.
- [ ] Shu klass ichidan chaqiriladigan `@Transactional`, `@Cacheable`, `@Async` metodlarni toping - ularning hammasi ishlamaydi.
- [ ] `static` mutable maydonlarni (`static Map`, `static List`, `SimpleDateFormat`) grep bilan topib ro'yxat tuzing.
- [ ] Timeout sozlanmagan HTTP mijozlarini aniqlang va har biriga ulanish va o'qish timeout i qo'ying.
- [ ] Smell nomlarini izohda ishlatishni to'xtatib, oqibat tilidagi iboralar jadvalini jamoaga tarqating.

## 13. Domen modeli review: invariant, agregat, chegara (Reviewing the Domain Model)

Domen modeli - tizimning eng uzoq yashaydigan qismi. Controller qayta yoziladi, ORM almashtiriladi, lekin "buyurtma nima" degan savolning javobi yillar davomida qoladi. Shu sababli domen modeliga tegadigan PR boshqa PR lardan chuqurroq o'qiladi: bu yerdagi xato keyinchalik yuzta joyda ko'rinadi. DDD atamalarining ta'rifi `java-spring-design-patterns.md` va `java-spring-architect-mindset.md` da; bu yerda faqat review savollari.

### 13.1 Modelning asosiy savoli: invariant kim tomonidan himoyalangan

Domen modelini review qilish bitta savoldan boshlanadi: bu obyektni noto'g'ri holatda yaratish yoki noto'g'ri holatga o'tkazish mumkinmi. Agar mumkin bo'lsa, qayerda bo'lsa ham bir kun shunday bo'ladi.

```java
// Himoyasiz model: har qanday holat yaratilishi mumkin.
@Entity
public class Subscription {
    @Id @GeneratedValue private Long id;
    private LocalDate startsAt;
    private LocalDate endsAt;
    private BigDecimal monthlyPrice;
    private SubscriptionStatus status;
    // setterlar hammasi public, no-arg konstruktor public
}
// Shu model bilan quyidagilar hammasi mumkin:
//  - endsAt < startsAt (manfiy davr)
//  - monthlyPrice manfiy
//  - status = ACTIVE, lekin endsAt o'tgan
//  - startsAt null

// Himoyalangan model: noto'g'ri holat tuzilmaydi.
@Entity
public class Subscription {
    @Id @GeneratedValue private Long id;
    @Embedded private DateRange period;         // o'z invariantini saqlaydi
    @Embedded private Money monthlyPrice;       // valyuta va manfiylik tekshirilgan
    @Enumerated(STRING) private SubscriptionStatus status;

    protected Subscription() { }                // JPA uchun, protected

    public Subscription(DateRange period, Money monthlyPrice) {
        this.period = Objects.requireNonNull(period);
        this.monthlyPrice = monthlyPrice.requirePositive();
        this.status = PENDING;
    }

    public void activate(LocalDate on) {
        if (status != PENDING) throw new IllegalStateTransition(status, ACTIVE);
        if (!period.contains(on)) throw new OutsideSubscriptionPeriod(on, period);
        this.status = ACTIVE;
    }
}

public record DateRange(LocalDate from, LocalDate to) {
    public DateRange {
        if (from == null || to == null) throw new IllegalArgumentException("sana null");
        if (to.isBefore(from)) throw new IllegalArgumentException("to < from");
    }
    public boolean contains(LocalDate d) {
        return !d.isBefore(from) && !d.isAfter(to);
    }
}
```

Review savollari ketma-ketligi: konstruktor to'liq holat talab qiladimi, setterlar qanchasi `public`, va holat o'tishlari metod orqali o'tadimi.

### 13.2 Anemik modelni ongli tanlash

Anemik model har doim xato emas. CRUD ustun bo'lgan modulda (ma'lumotnoma jadvallar, sozlamalar, admin panel) boy model ortiqcha. Xato - tanlovning ongsizligi: biznes qoidalari ko'p bo'lgan modulda anemik modeldan foydalanish.

| Modul turi | Mos model | Review kutilmasi |
| --- | --- | --- |
| Ma'lumotnoma, sozlama | Anemik + validation | Setterlar normal, DTO = entity bo'lishi mumkin |
| Hisobot va o'qish | Projection, DTO | Entity umuman kerak emas |
| Biznes jarayoni (buyurtma, to'lov) | Boy model | Setterlar yo'q, holat metodlari bor |
| Integratsiya (adapter) | Oddiy struktura | Mapping va tashqi shakl |

Xavfli belgi: bitta modulda ikki yondashuv aralashgan - qoidalarning yarmi entity da, yarmi servisda. Shu holatda invariantni hech kim to'liq himoya qilmaydi.

### 13.3 Agregat chegarasi: nima birga saqlanadi

Agregat - birga o'zgaradigan va birga tekshiriladigan obyektlar guruhi. Chegara review da ikki savol bilan tekshiriladi: qaysi invariant tranzaksiya ichida kafolatlanishi kerak, va agregat qanchalik katta bo'ladi.

```java
// Juda katta agregat: buyurtmaga 50 000 qator ilashishi mumkin.
@Entity
public class Customer {
    @OneToMany(mappedBy = "customer", cascade = ALL, fetch = EAGER)
    private List<Order> orders = new ArrayList<>();      // yillar davomida o'sadi
}
// Review izohlari: (1) EAGER - mijozni yuklash barcha buyurtmalarni
// tortadi; (2) cascade ALL - mijozni o'chirish barcha buyurtmalarni
// o'chiradi, bu biznes qoidasimi?; (3) yangi buyurtma qo'shish uchun butun
// kolleksiya yuklanadi - xotira va qulf.
// Yechim: Order alohida agregat, Customer faqat CustomerId bilan bog'lanadi.

// To'g'ri chegara: agregatlar ID orqali bog'lanadi.
@Entity
public class Order {
    @Id @GeneratedValue private Long id;
    @Embedded private CustomerId customerId;        // boshqa agregatga havola
    @ElementCollection                              // buyurtma qatorlari esa ichida
    private List<OrderLine> lines = new ArrayList<>();
}
```

Chegara mezoni: invariant tranzaksiya ichida kafolatlanishi kerakmi. "Buyurtma summasi qatorlar summasiga teng" - ha, demak qatorlar agregat ichida. "Mijozning umumiy xaridi 10 mln dan oshmaydi" - bu boshqa agregatga tegadi, uni tranzaksiya emas, jarayon bilan ta'minlash kerak (yoki ongli ravishda eventual consistency qabul qilinadi).

### 13.4 Value object va entity farqi diffda

Value object qiymati bilan aniqlanadi va o'zgarmaydi (`Money`, `Address`, `DateRange`, `Email`). Entity identifikatori bilan aniqlanadi va holati o'zgaradi. Review da aralashtirish belgisi: value object da `id` paydo bo'lishi yoki setterlar qo'shilishi.

```java
// Value object: immutable, equals qiymat bo'yicha, validatsiya ichida.
public record Money(BigDecimal amount, Currency currency) implements Comparable<Money> {
    public Money {
        Objects.requireNonNull(amount); Objects.requireNonNull(currency);
        // Scale ni normalizatsiya qilish: 10.00 va 10.0 teng bo'lishi uchun.
        amount = amount.setScale(currency.getDefaultFractionDigits(), HALF_UP);
    }
    public Money plus(Money other) { requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency); }
    public Money times(int n) { return new Money(amount.multiply(valueOf(n)), currency); }
    @Override public int compareTo(Money o) { requireSameCurrency(o);
        return amount.compareTo(o.amount); }
}
// Review diqqati: record da `equals` avtomatik, lekin BigDecimal da
// 10.00 va 10.0 teng EMAS (scale farqi). Shu sababli konstruktorda
// setScale qilinmasa, teng summalar teng emas deb chiqadi - jadvalda
// va Set da jim xato beradi.
```

### 13.5 Identifikator dizayni

ID turini tanlash qaytarib bo'lmaydigan qarorlar qatoriga kiradi: u API ga, indekslarga va tashqi tizimlarga tarqaydi.

| Variant | Foydasi | Narxi | Review savoli |
| --- | --- | --- | --- |
| `bigserial` (ketma-ket) | Kichik indeks, tabiiy tartib | Raqamni taxmin qilish mumkin, merge qiyin | ID tashqariga chiqadimi |
| `uuid` v4 | Taxmin qilinmaydi, taqsimlangan yaratish | Indeks katta va tasodifiy, insert sekinroq | Hajm va insert tezligi muhimmi |
| UUID v7 / ULID | Vaqt bo'yicha tartibli, taqsimlangan | Yangi, kutubxona kerak | Indeks lokalligi kerakmi |
| Tabiiy kalit (`order_number`) | Biznes uchun ma'noli | O'zgarishi mumkin, formati qotib qoladi | Qiymat o'zgarishi mumkinmi |

```java
// Tipli ID: almashtirib qo'yish kompilyatsiyada tutiladi (8.5).
public record OrderId(UUID value) {
    public static OrderId newId() { return new OrderId(UuidCreator.getTimeOrderedEpoch()); }
    @Override public String toString() { return value.toString(); }
}

// JPA bilan ishlatish uchun converter (yoki @Embedded).
@Converter(autoApply = true)
class OrderIdConverter implements AttributeConverter<OrderId, UUID> {
    @Override public UUID convertToDatabaseColumn(OrderId id) {
        return id == null ? null : id.value();
    }
    @Override public OrderId convertToEntityAttribute(UUID db) {
        return db == null ? null : new OrderId(db);
    }
}
```

Review da alohida savol: ichki ID tashqi API da ko'rinadimi. Ketma-ket ID tashqariga chiqsa, raqobatchi buyurtmalar sonini biladi va mijozlar bir-birining resursini taxmin qila oladi (IDOR xavfi, 30-bob).

### 13.6 Domen eventlari: nima e'lon qilinadi

Domen eventi o'tgan zamonda nomlanadi va o'zgarmas faktni bildiradi: `OrderPlaced`, `PaymentCaptured`. Review da uch xato uchraydi: event buyruq kabi nomlangan (`SendEmail`), eventda mutable obyekt uzatilgan, va event tranzaksiyadan oldin e'lon qilingan.

```java
// Agregat ichida event yig'ish, publish qilish - saqlashdan keyin.
@Entity
public class Order extends AbstractAggregateRoot<Order> {   // Spring Data
    public void markPaid(PaymentId paymentId, Instant when) {
        if (status != NEW) throw new IllegalStateTransition(status, PAID);
        this.status = PAID;
        this.paidAt = when;
        registerEvent(new OrderPaid(new OrderId(id), paymentId, total, when));
    }
}
// Spring Data repository.save() dan keyin eventlar e'lon qiladi, ya'ni
// agregat holati bilan birga. Qabul qiluvchi tomonda:
@TransactionalEventListener(phase = AFTER_COMMIT)
void on(OrderPaid e) { /* commit dan keyin, yetkazish kafolati kerak bo'lsa outbox */ }
```

### 13.7 Domen tili: kod va suhbat bir xil so'z bilan

Agar biznes "aktivatsiya" deyotgan bo'lsa, kodda `enable`, `turnOn` va `activate` aralash ishlatilsa, har suhbatda tarjima qilish kerak bo'ladi. Review da bu arzon tuzatiladi, keyinroq esa qimmat.

```bash
# Domen tilining izchilligini tekshirish: bitta tushuncha necha xil nom bilan.
for term in activate enable turnOn start; do
  printf '%-10s %s\n' "$term" "$(grep -rn --include='*.java' -c "$term" src/main/java | wc -l)"
done
# Natijada bir tushuncha uchun to'rt nom chiqsa, lug'atni kelishib olish kerak.
```

Foydali amal: `GLOSSARY.md` faylida 20-40 asosiy tushuncha va ularning yagona kodli nomi. Review da yangi nom paydo bo'lganda shu faylga qarash kifoya.

### 13.8 Domen servisi qachon kerak

Qoida mavjud obyektga sig'maydigan holatlar uchun domen servisi ishlatiladi: qoida ikki agregatga tegadi, yoki tashqi ma'lumot kerak. Review da belgisi: servis nomi "nima qilishi" bilan nomlangan va holatsiz.

| Qoida qayerda turadi | Misol |
| --- | --- |
| Agregat ichida | "Buyurtma summasi qatorlar summasiga teng" |
| Value object ichida | "Email shakli to'g'ri" |
| Domen servisida | "Mijozning kredit limiti yetadimi" (hisob + mijoz) |
| Application servisida | Tranzaksiya, avtorizatsiya, chaqiruvlar ketma-ketligi |
| Infra da | SQL, HTTP, serializatsiya |

Belgi: application servis ichida 50 satrli biznes hisobi paydo bo'lsa, u domenga tushishi kerak. Teskari belgi: domen servisi `@Transactional` yoki repository bilan ishlasa, u aslida application servis.

### 13.9 ORM domen modelini buzganda

JPA talablari domen modeliga ta'sir qiladi: no-arg konstruktor, mutable maydonlar, `@Id`. Review savoli - qaysi murosaga ongli kelingan.

| JPA talabi | Domen uchun oqibati | Murosa |
| --- | --- | --- |
| No-arg konstruktor | To'liq bo'lmagan obyekt yaratilishi mumkin | `protected` qilish |
| Maydonlar `final` bo'lmaydi | Immutable emas | Setterlarni olib tashlash |
| Kolleksiyalar mutable | Tashqaridan o'zgartirish | Himoyalangan ko'rinish qaytarish |
| Lazy proxy | Domen tashqarisida istisno | Agregat chegarasida yuklash |
| `@Id` generated | `equals`/`hashCode` muammosi | Biznes kalit yoki oldindan yaratilgan UUID |
| Dirty checking | Har `set` yozuvga aylanadi | Domen metodlari orqali o'zgartirish |

```java
// JPA entity uchun equals/hashCode: eng ko'p xato qilinadigan joy.
@Entity
public class Order {
    @Id private UUID id = UUID.randomUUID();   // oldindan yaratilgan: generated emas

    // ID oldindan ma'lum bo'lgani uchun equals barqaror: obyekt saqlanishdan
    // oldin ham keyin ham bir xil hashCode beradi.
    @Override public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Order other)) return false;
        return id.equals(other.id);
    }
    @Override public int hashCode() { return id.hashCode(); }
}
// Agar @GeneratedValue ishlatilsa: saqlashdan oldin id = null, keyin 42.
// Shu obyekt HashSet ga qo'yilgandan keyin saqlangan bo'lsa, u Set ichida
// "yo'qoladi" - hashCode o'zgargan. Review da bu holat alohida tekshiriladi.
```

### 13.10 Modelga tegadigan PR uchun qo'shimcha talablar

Domen modeli o'zgarishi boshqa o'zgarishlardan ko'proq narsani talab qiladi, chunki u ma'lumotga va API ga tarqaydi.

| Talab | Nega |
| --- | --- |
| Migratsiya bilan birga keladi | Model va sxema bir-biriga mos bo'lishi kerak |
| Invariant testi bor | Noto'g'ri holat yaratilmasligini tekshirish |
| Holat o'tish matritsasi testi | Taqiqlangan o'tishlar rad etilishi |
| Mavjud ma'lumot bilan moslik | Eski qatorlar yangi qoidani buzmaydimi |
| API ta'siri baholangan | Yangi majburiy maydon mijozni sindiradimi |
| Terminologiya `GLOSSARY.md` da | Nom izchil |

Ayniqsa beshinchi band: yangi `NOT NULL` maydon qo'shilsa, mavjud 4 mln qator uchun qiymat qayerdan keladi. Bu savolga javob migratsiya review da emas, model review da berilishi kerak (25-bob).

### 13.11 Amalda qo'llash

- [ ] Domen entity larida `public` setterlar sonini sanang va biznes jarayoni modullarida ularni domen metodlariga aylantirish ro'yxatini tuzing.
- [ ] Har bir agregat uchun "qaysi invariant tranzaksiya ichida kafolatlanadi" degan javobni bir satrda yozing.
- [ ] `EAGER` va `cascade = ALL` ishlatilgan `@OneToMany` larni toping va agregat chegarasini qayta ko'rib chiqing.
- [ ] `BigDecimal` ishlatadigan value object larda `setScale` normalizatsiyasi borligini tekshiring.
- [ ] `@GeneratedValue` bilan ishlaydigan entity larning `equals`/`hashCode` ini ko'rib chiqing va UUID ga o'tish variantini baholang.
- [ ] Ichki ketma-ket ID lar tashqi API da ko'rinadigan joylarni aniqlab, IDOR xavfini baholang.
- [ ] `GLOSSARY.md` yaratib, 20 asosiy tushuncha uchun yagona kodli nomni kelishib oling.
- [ ] Domen modeliga tegadigan PR lar uchun qo'shimcha talablar jadvalini PR shabloniga kiriting.

# III. Java kodini chuqur tahlil

## 14. Java tili darajasidagi xatolar katalogi (Language-Level Defects)

Bu bob review ning eng tez ishlatiladigan qismi: Java ning o'zi beradigan tuzoqlar. Ularning ko'pini statik tahlil topadi, lekin reviewer ularni oldin ko'rishi va oqibatini aytishi kerak (5-bob). Har bo'limda naqsh, nima bo'lishi va review javobi bor.

### 14.1 null: chegarada to'xtatish

Null bilan ishlashning yagona ishonchli strategiyasi - null ni tizim chegarasida to'xtatish va ichkarida null yo'qligini kafolatlash.

```java
// Naqsh 1: tashqi ma'lumot ichkariga null olib kiradi.
public OrderResponse create(@RequestBody OrderRequest req) {   // @Valid yo'q
    // req.customerId() null bo'lishi mumkin: JSON da maydon yo'q edi.
    Order order = orders.place(req.customerId(), req.lines());
    ...
}
// Review javobi: @Valid va @NotNull bilan chegarada to'xtatish; aks holda
// null domenga kiradi va NPE uch qatlam pastda, boshqa stack trace bilan
// chiqadi - diagnostika qiyin.

// Naqsh 2: Optional noto'g'ri ishlatilishi.
Optional<Customer> c = customers.findById(id);
if (c.isPresent()) { use(c.get()); }               // ishlaydi, lekin ortiqcha
customers.findById(id).ifPresent(this::use);       // niyat aniqroq

String name = customers.findById(id).get().name(); // NoSuchElementException
String name = customers.findById(id)
                       .map(Customer::name)
                       .orElseThrow(() -> new CustomerNotFound(id));   // to'g'ri

// Naqsh 3: Optional ni noto'g'ri joyda ishlatish.
public record Customer(String name, Optional<Email> email) { }   // yomon: maydon
public record Customer(String name, @Nullable Email email) {     // yaxshi
    public Optional<Email> email() { return Optional.ofNullable(email); }
}
// Sabab: Optional serializatsiya, JPA va equals bilan yaxshi ishlamaydi;
// u qaytish turi uchun mo'ljallangan.

// Naqsh 4: null bilan boolean mantiq.
Boolean active = settings.get("active");      // null bo'lishi mumkin
if (active) { ... }                           // NPE: avtounboxing
if (Boolean.TRUE.equals(active)) { ... }      // xavfsiz
```

### 14.2 equals, hashCode va compareTo

Bu uchlikdagi xatolar jim ishlaydi: kod kompilyatsiya bo'ladi, testlar o'tadi, va xato faqat `HashMap` yoki `TreeSet` ishlatilganda chiqadi.

| Xato | Oqibati |
| --- | --- |
| `equals` bor, `hashCode` yo'q | `HashSet` da dublikat, `HashMap` da yozuv topilmaydi |
| `hashCode` da mutable maydon | Obyekt o'zgargach `Map` dan yo'qoladi |
| `equals` da `getClass()` o'rniga `instanceof` meros bilan | Nosimmetrik tenglik |
| `compareTo` va `equals` mos emas | `TreeSet` va `HashSet` turlicha xulq |
| `equals` da `BigDecimal` to'g'ridan-to'g'ri | `10.0` va `10.00` teng emas |
| JPA entity da generated ID bilan `equals` | Saqlashdan keyin `hashCode` o'zgaradi |
| Array `equals` | Havola taqqoslanadi, `Arrays.equals` kerak |

```java
// compareTo va equals mos kelmasligi: TreeSet elementni "bor" deb hisoblaydi.
public record Version(int major, int minor, String qualifier) implements Comparable<Version> {
    @Override public int compareTo(Version o) {
        return Comparator.comparingInt(Version::major)
                         .thenComparingInt(Version::minor)
                         .compare(this, o);         // qualifier hisobga olinmaydi
    }
}
// record equals qualifier ni hisobga oladi, compareTo esa yo'q.
// TreeSet<Version> da 1.0-alpha va 1.0-beta bir xil element sanaladi,
// HashSet da ikki xil. Review izohi: compareTo ga qualifier qo'shish yoki
// Comparator ni alohida berish, record ichida emas.
```

### 14.3 Sonlar: butun bo'lish, overflow, pul

```java
// Xato 1: butun sonlar bo'linishi - natija 0.
int percent = count / total * 100;              // count < total bo'lsa 0
double percent = (double) count / total * 100;  // to'g'ri
// Review izohi: bu formula hisobotda 0% ko'rsatadi. Nol bilan bo'lish
// xavfi ham bor: total = 0 bo'lsa ArithmeticException (int) yoki
// Infinity (double) - ikkisi ham tekshirilmagan.

// Xato 2: int overflow jim aylanadi.
int totalBytes = fileCount * bytesPerFile;      // 100_000 * 50_000 manfiy bo'ladi
long totalBytes = (long) fileCount * bytesPerFile;
// Yoki aniq tekshiruv bilan: Math.multiplyExact tashlaydi, jim aylanmaydi.
long totalBytes = Math.multiplyExact((long) fileCount, bytesPerFile);

// Xato 3: pul double da.
double total = 0.1 + 0.2;                        // 0.30000000000000004
BigDecimal total = new BigDecimal("0.1").add(new BigDecimal("0.2"));   // 0.3
// Diqqat: BigDecimal.valueOf(0.1) ham xavfli - double dan o'tadi.
// new BigDecimal("0.1") - satr orqali, aniq.

// Xato 4: BigDecimal da scale va yakkalash e'lon qilinmagan.
BigDecimal vat = total.multiply(new BigDecimal("0.12"));   // scale o'sadi
BigDecimal vat = total.multiply(new BigDecimal("0.12"))
                      .setScale(2, RoundingMode.HALF_UP);  // qoida aniq
// Review savoli: yakkalash qoidasi biznes bilan kelishilganmi? Soliq
// hisobida HALF_UP va HALF_EVEN farqi yiliga sezilarli summa beradi.

// Xato 5: BigDecimal taqqoslashda equals.
if (price.equals(BigDecimal.ZERO)) { }           // 0.00 uchun false
if (price.compareTo(BigDecimal.ZERO) == 0) { }   // to'g'ri
```

### 14.4 Satr, kodlash va formatlash

```java
// Xato 1: kodlash ko'rsatilmagan - platformaga bog'liq natija.
byte[] bytes = text.getBytes();                       // JVM standart kodlashi
byte[] bytes = text.getBytes(StandardCharsets.UTF_8); // aniq
new String(bytes);                                    // yana platformaga bog'liq
new String(bytes, StandardCharsets.UTF_8);

// Xato 2: Locale ko'rsatilmagan - turk tilidagi "i" muammosi.
if (code.toUpperCase().equals("TITLE")) { }                 // tr_TR da buziladi
if (code.toUpperCase(Locale.ROOT).equals("TITLE")) { }      // barqaror

// Xato 3: formatlash Locale siz - o'nlik ajratgich o'zgaradi.
String s = String.format("%.2f", amount);                   // "1,50" yoki "1.50"
String s = String.format(Locale.ROOT, "%.2f", amount);      // har doim "1.50"

// Xato 4: siklda satr qo'shish.
String csv = "";
for (Row r : rows) { csv += r.id() + ";"; }      // O(n^2), 100k qatorda muammo
StringBuilder sb = new StringBuilder();          // yoki Collectors.joining()

// Xato 5: satr taqqoslash == bilan.
if (status == "ACTIVE") { }                      // intern ga bog'liq, xavfli
if ("ACTIVE".equals(status)) { }                 // null-xavfsiz tartib
```

### 14.5 Vaqt va zona

Vaqt bilan ishlash eng ko'p yashirin xato beradigan soha, chunki xatolar faqat ma'lum sharoitda (yozgi vaqt o'tishi, oyning oxiri, boshqa zonadagi foydalanuvchi) ko'rinadi.

```java
// Xato 1: zonasiz vaqt saqlash.
@Column private LocalDateTime createdAt;        // qaysi zonada?
@Column private Instant createdAt;              // UTC nuqta, aniq
// PostgreSQL da: timestamptz (timestamp with time zone) ishlatish kerak,
// timestamp emas. Ikkisi diffda bir xil ko'rinadi, lekin xulqi boshqa.

// Xato 2: hozirgi vaqtni to'g'ridan-to'g'ri olish - test qilinmaydi.
public boolean isExpired() { return expiresAt.isBefore(Instant.now()); }
// Review javobi: Clock ni inyeksiya qilish.
public boolean isExpired(Clock clock) { return expiresAt.isBefore(clock.instant()); }
// Testda: Clock.fixed(Instant.parse("2026-10-04T12:00:00Z"), ZoneOffset.UTC)

// Xato 3: kun hisobi vaqt bilan.
long days = Duration.between(from, to).toDays();          // 23:30 -> 00:30 = 0 kun
long days = ChronoUnit.DAYS.between(fromDate, toDate);    // kalendar kunlari

// Xato 4: kun boshini hisoblash zona bilan.
Instant dayStart = date.atStartOfDay().toInstant(ZoneOffset.UTC);  // noto'g'ri zona
Instant dayStart = date.atStartOfDay(ZoneId.of("Asia/Tashkent")).toInstant();

// Xato 5: yozgi vaqtda mavjud bo'lmagan vaqt.
// Ba'zi zonalarda 02:30 mavjud emas (soat oldinga suriladi).
// ZonedDateTime bu holatni o'zi tuzatadi, LocalDateTime esa jim o'tadi.

// Xato 6: tashqi API ga zonasiz vaqt yuborish.
public record Response(LocalDateTime createdAt) { }     // mijoz zonani bilmaydi
public record Response(OffsetDateTime createdAt) { }    // ofset bilan
```

### 14.6 Kolleksiyalar

```java
// Xato 1: o'zgarmas kolleksiyani o'zgartirishga urinish.
List<String> list = List.of("a", "b");
list.add("c");                                   // UnsupportedOperationException
List<String> list = new ArrayList<>(List.of("a", "b"));   // o'zgartirsa bo'ladi

// Xato 2: Arrays.asList yarim o'zgarmas.
List<String> l = Arrays.asList("a", "b");
l.set(0, "c");                                   // ishlaydi
l.add("c");                                      // istisno - kutilmagan

// Xato 3: null bilan Map.of va List.of.
Map.of("k", maybeNull);                          // NullPointerException
// HashMap null ni qabul qiladi, Map.of yo'q - almashtirishda jim buziladi.

// Xato 4: iteratsiya paytida o'zgartirish.
for (Order o : orders) {
    if (o.isExpired()) orders.remove(o);         // ConcurrentModificationException
}
orders.removeIf(Order::isExpired);               // to'g'ri

// Xato 5: tartib kafolati haqida taxmin.
Map<String, Integer> counts = new HashMap<>();   // tartib yo'q
// Agar javobda tartib muhim bo'lsa - LinkedHashMap yoki TreeMap.
// Review izohi: API javobida HashMap ishlatilgan, mijoz tartibni
// barqaror deb o'ylashi mumkin - JVM versiyasi o'zgarganda tartib o'zgaradi.

// Xato 6: Set ga mutable obyekt qo'yish.
Set<Order> set = new HashSet<>();
set.add(order);
order.setStatus(PAID);                           // hashCode o'zgardi
set.contains(order);                             // false - obyekt "yo'qoldi"
```

### 14.7 Stream xatolari

```java
// Xato 1: oqimda yon ta'sir.
List<Order> result = new ArrayList<>();
orders.parallelStream().forEach(result::add);    // thread-safe emas, buziladi
List<Order> result = orders.parallelStream().toList();   // to'g'ri

// Xato 2: Optional va oqim aralashuvi - jim yo'qotish.
orders.stream().map(this::findCustomer)          // Optional<Customer>
      .filter(Optional::isPresent).map(Optional::get)   // eski uslub
      .toList();
orders.stream().map(this::findCustomer).flatMap(Optional::stream).toList();
// Review savoli: topilmagan mijozlar jim tashlab ketilyapti. Bu niyatmi
// yoki xato? Agar har buyurtmaga mijoz bo'lishi kerak bo'lsa, bu yerda
// istisno tashlanishi kerak.

// Xato 3: toMap da dublikat kalit.
Map<String, Order> byNumber = orders.stream()
    .collect(toMap(Order::number, identity()));   // dublikat bo'lsa IllegalState
// Review: raqamlar yagona ekani kafolatlanganmi? Agar yo'q bo'lsa, merge
// funksiyasi berilishi kerak: toMap(k, v, (a, b) -> b)

// Xato 4: parallelStream bloklaydigan operatsiya bilan.
orders.parallelStream().forEach(o -> httpClient.send(o));  // common pool bloklanadi
// Butun ilovadagi boshqa parallel oqimlar ham sekinlashadi.

// Xato 5: oqimni ikki marta ishlatish.
Stream<Order> s = orders.stream();
long n = s.count();
List<Order> l = s.toList();                      // IllegalStateException

// Xato 6: peek bilan mantiq.
orders.stream().peek(o -> o.setChecked(true)).toList();   // peek kafolatsiz
// peek faqat diagnostika uchun; optimizatsiya uni o'tkazib yuborishi mumkin.
```

### 14.8 switch, enum va sealed

```java
// Xato 1: enum ordinal saqlash.
@Enumerated(EnumType.ORDINAL)                    // 0, 1, 2 saqlanadi
private OrderStatus status;
// Enum da yangi qiymat o'rtaga qo'shilsa, mavjud qatorlar ma'nosi o'zgaradi.
@Enumerated(EnumType.STRING)                     // "PAID" saqlanadi - barqaror
private OrderStatus status;

// Xato 2: enum valueOf tashqi ma'lumot bilan.
OrderStatus s = OrderStatus.valueOf(request.status());   // IllegalArgumentException
// Review: noma'lum qiymat 500 beradi, 400 bermaydi. Xavfsiz o'qish:
Optional<OrderStatus> parsed = Arrays.stream(OrderStatus.values())
    .filter(v -> v.name().equalsIgnoreCase(request.status())).findFirst();

// Xato 3: default bilan yangi qiymatni jim o'tkazish (12.1).
// Yechim: sealed bilan kompilyator tekshiradi.
public sealed interface PaymentResult {
    record Approved(String authCode) implements PaymentResult { }
    record Declined(DeclineReason reason) implements PaymentResult { }
    record Pending(Instant retryAt) implements PaymentResult { }
}
// Pattern matching switch: yangi holat qo'shilsa, kompilyator xato beradi.
String message = switch (result) {
    case Approved a -> "tasdiqlandi: " + a.authCode();
    case Declined d -> "rad etildi: " + d.reason().message();
    case Pending p  -> "kutilmoqda: " + p.retryAt();
    // default yo'q - va bo'lmasligi kerak: to'liqlik kompilyatorda.
};

// Xato 4: enum da mutable holat.
public enum Config {
    INSTANCE;
    private Map<String, String> values = new HashMap<>();   // umumiy mutable holat
}
```

### 14.9 Istisnolar: tur va kontekst

```java
// Xato 1: kontekst yo'qoladi.
catch (SQLException e) {
    throw new ServiceException("xatolik");       // original sabab yo'qoldi
}
catch (SQLException e) {
    throw new ServiceException("buyurtma saqlanmadi: id=" + id, e);   // sabab bor
}

// Xato 2: istisno turi ma'no bermaydi.
throw new RuntimeException("mijoz topilmadi");   // chaqiruvchi ajrata olmaydi
throw new CustomerNotFound(customerId);          // tur bo'yicha ishlash mumkin

// Xato 3: istisno bilan boshqaruv oqimi.
try { return Integer.parseInt(s); }
catch (NumberFormatException e) { return 0; }    // jim 0 - xato yashiringan
// Review savoli: noto'g'ri kirish 0 ga aylanishi biznesga to'g'rimi?
// Pul miqdori bo'lsa, bu jim ma'lumot buzilishi.

// Xato 4: checked istisnoni o'rash va ma'nosini yo'qotish.
catch (IOException e) { throw new RuntimeException(e); }   // ma'no yo'q
catch (IOException e) { throw new ReportGenerationFailed(reportId, e); }

// Xato 5: InterruptedException yutilishi.
catch (InterruptedException e) { }               // thread to'xtatish signali yo'qoldi
catch (InterruptedException e) {
    Thread.currentThread().interrupt();          // signalni qaytarish
    throw new OperationCancelled(e);
}

// Xato 6: finally ichida return yoki istisno.
try { return compute(); }
finally { cleanup(); }                           // cleanup istisno tashlasa,
                                                 // asosiy istisno yo'qoladi
```

### 14.10 Review da tez tekshirish uchun grep to'plami

```bash
# Tilga tegishli xatolarning tez skanerlanishi: PR dagi o'zgargan fayllarda.
FILES=$(git diff --name-only origin/main...HEAD -- '*.java')
[ -z "$FILES" ] && exit 0

echo "=== pul double da ==="
grep -nE '(double|float)\s+\w*(amount|price|total|sum|fee|balance)' $FILES

echo "=== kodlash va Locale ko'rsatilmagan ==="
grep -nE 'getBytes\(\)|new String\([^,)]*\)|toUpperCase\(\)|toLowerCase\(\)|String\.format\("' $FILES

echo "=== zonasiz vaqt va test qilinmaydigan now() ==="
grep -nE 'LocalDateTime\.now\(\)|new Date\(\)|Instant\.now\(\)|System\.currentTimeMillis' $FILES

echo "=== Optional noto'g'ri ishlatilishi ==="
grep -nE '\.get\(\)|isPresent\(\)|Optional<[A-Za-z]+>\s+\w+;' $FILES

echo "=== enum ORDINAL va valueOf ==="
grep -nE 'EnumType\.ORDINAL|\.valueOf\(' $FILES

echo "=== BigDecimal equals va scale ==="
grep -nE 'BigDecimal.*\.equals\(|BigDecimal\.valueOf\([0-9]+\.[0-9]' $FILES

echo "=== jim yutilgan istisno ==="
grep -nA2 -E 'catch\s*\(' $FILES | grep -B1 -E '^\S+[-:]\s*\}' 

echo "=== satr konkatenatsiyasi sikl ichida ==="
grep -nE '\+=\s*"' $FILES
```

Bu skriptni CI da ogohlantirish sifatida ishlatish mumkin, lekin bloklamaslik kerak: har bir naqshning qonuniy holatlari bor. Maqsad - reviewer diqqatini yo'naltirish.

### 14.11 Amalda qo'llash

- [ ] `scripts/review-java-scan.sh` skriptini qo'shing va uni PR da o'zgargan fayllarga ishlatishni review oqimiga kiriting.
- [ ] Loyihadagi pul maydonlarini tekshirib, `double`/`float` ishlatilgan joylarni `BigDecimal` yoki `Money` ga o'tkazish tiketini ochingg.
- [ ] `setScale` va `RoundingMode` ko'rsatilmagan pul hisoblarini toping va yakkalash qoidasini biznes bilan kelishib yozib qo'ying.
- [ ] `@Enumerated(EnumType.ORDINAL)` ishlatilgan joylarni toping - har biri kelajakdagi ma'lumot buzilishi.
- [ ] `Instant.now()` va `LocalDateTime.now()` to'g'ridan-to'g'ri ishlatilgan domen kodini `Clock` inyeksiyasiga o'tkazing.
- [ ] `LocalDateTime` saqlanadigan ustunlarni aniqlab, PostgreSQL da `timestamptz` ga o'tish rejasini tuzing.
- [ ] `toMap` ishlatilgan joylarda kalit yagonaligi kafolatlanganini tekshiring va merge funksiyasini qo'shing.
- [ ] `catch (InterruptedException)` bloklarida `Thread.currentThread().interrupt()` borligini tekshiring.

## 15. Holat, mutability va concurrency review (State and Concurrency)

Concurrency xatolari review ning eng qiymatli topilmalari, chunki ularni boshqa hech bir filtr ishonchli tutmaydi: test ularni 99 marta o'tkazadi va 100-marta yiqiladi, statik tahlil faqat eng oddiy naqshlarni ko'radi, prod monitoringi esa ularni "tushunarsiz incident" sifatida ko'rsatadi. Reviewer ning qo'lida bitta ishonchli usul bor: har bir umumiy holat uchun "ikki thread bu yerda bir vaqtda bo'lsa nima bo'ladi" savolini berish.

### 15.1 Umumiy holatni topish: review ning birinchi qadami

Spring ilovasida umumiy holat uchta joyda bo'ladi, va reviewer uchalasini ham biladi.

| Qayerda | Belgisi | Nega xavfli |
| --- | --- | --- |
| Singleton bean maydonlari | `private` maydon, `final` emas | Har so'rov shu maydonni ko'radi |
| `static` maydonlar | `static Map`, `static int` | Butun JVM bo'ylab umumiy |
| Tashqi holat | Baza qatori, kesh, fayl | Ko'p instans bo'ylab umumiy |

```java
// Eng ko'p uchraydigan xato: singleton bean ichida so'rov holati.
@Service
public class InvoiceService {
    private BigDecimal runningTotal = BigDecimal.ZERO;    // umumiy maydon!
    private Order current;                                // umumiy maydon!

    public Invoice generate(Order order) {
        this.current = order;                   // ikkinchi so'rov buni almashtiradi
        this.runningTotal = BigDecimal.ZERO;
        for (OrderLine line : order.lines()) {
            this.runningTotal = this.runningTotal.add(line.amount());
        }
        return new Invoice(current.id(), runningTotal);   // boshqa buyurtmaning summasi!
    }
}
// Review izohi (blocker): Spring bean standart holatda singleton. Bu
// maydonlar barcha so'rovlar uchun umumiy. Ikki parallel so'rovda biri
// ikkinchisining summasini oladi - ya'ni mijozga boshqa odamning invoysi
// ko'rsatiladi. Yuk kichik bo'lganda bu deyarli hech qachon ko'rinmaydi,
// shu sababli testda ham chiqmaydi.
// Yechim: holat metodning lokal o'zgaruvchisi bo'lishi kerak.

// To'g'ri: holatsiz bean, hamma narsa lokal.
@Service
public class InvoiceService {
    public Invoice generate(Order order) {
        BigDecimal total = order.lines().stream()
            .map(OrderLine::amount)
            .reduce(Money.ZERO, Money::plus);
        return new Invoice(order.id(), total);
    }
}
```

Review qoidasi: singleton bean ichidagi har bir `final` bo'lmagan maydon savol tug'diradi. Agar u konfiguratsiya yoki kesh bo'lsa - thread-safe bo'lishi kerak. Agar u so'rov holati bo'lsa - xato.

### 15.2 Tekshir-keyin-yoz: eng ko'p uchraydigan poyga

Bu naqsh shunchalik tabiiy ko'rinadi, kod review da osongina o'tadi. Uning belgisi: `if (!exists)` keyin `create`, yoki `if (balance >= amount)` keyin `withdraw`.

```java
// Naqsh: ikki parallel so'rov ikkisi ham "yo'q" deb ko'radi.
@Transactional
public Customer register(String email) {
    if (customers.existsByEmail(email)) {           // T1 va T2: false
        throw new EmailAlreadyUsed(email);
    }
    return customers.save(new Customer(email));     // ikki qator yaratiladi
}
// Review izohi: READ COMMITTED da (PostgreSQL standarti) ikki tranzaksiya
// bir-birining yozilmagan qatorini ko'rmaydi, shuning uchun ikkisi ham
// o'tadi. Test bitta thread da o'tadi, prodda ikki dublikat paydo bo'ladi.

// Yechim 1 (eng ishonchli): unique constraint, xatoni ushlash.
@Transactional
public Customer register(String email) {
    try {
        Customer c = customers.saveAndFlush(new Customer(email));   // flush shart
        return c;
    } catch (DataIntegrityViolationException e) {
        throw new EmailAlreadyUsed(email);          // poyga g'olibi aniq
    }
}
```

```sql
-- Himoya bazada: normalizatsiya bilan birga.
CREATE UNIQUE INDEX customer_email_uniq ON customer (lower(email));
-- lower() bilan: "Ali@x.com" va "ali@x.com" bir xil hisoblanadi.
-- Review savoli: email normalizatsiyasi Java va SQL da bir xilmi?
```

```java
// Yechim 2: qulf bilan (hisob qoldig'i kabi hollarda).
@Transactional
public void withdraw(AccountId id, Money amount) {
    // SELECT ... FOR UPDATE: ikkinchi tranzaksiya kutadi.
    Account acc = accounts.lockById(id).orElseThrow();
    if (acc.balance().isLessThan(amount)) throw new InsufficientFunds();
    acc.debit(amount);
}

// Yechim 3: atomik UPDATE (eng tez, qulf olmaydi).
@Modifying
@Query("""
    update Account a set a.balance = a.balance - :amount
     where a.id = :id and a.balance >= :amount
    """)
int debitIfEnough(@Param("id") UUID id, @Param("amount") BigDecimal amount);
// Qaytgan qiymat 0 bo'lsa - mablag' yetmagan. Bitta atomik operatsiya,
// hech qanday poyga yo'q. Review da shu shakl afzal ko'riladi.
```

### 15.3 Yo'qolgan yangilanish (lost update)

Belgi: obyekt o'qiladi, o'zgartiriladi va saqlanadi, versiya nazorati yo'q. Ikki parallel so'rovda ikkinchisi birinchisining o'zgarishini bosib ketadi.

```java
// Naqsh: ikki admin bir vaqtda mahsulot narxini o'zgartiradi.
Product p = products.findById(id).orElseThrow();
p.setPrice(newPrice);                    // ikkinchi saqlash birinchisini o'chiradi
products.save(p);

// Yechim: optimistik qulf - konflikt aniqlanadi.
@Entity
public class Product {
    @Version private long version;        // Hibernate avtomatik boshqaradi
}
// Ikkinchi saqlash OptimisticLockingFailureException beradi.

// Review savoli: bu istisno qanday ishlanadi? Foydalanuvchiga 409 bilan
// "ma'lumot o'zgargan, qayta yuklang" deyilishi kerak, 500 emas.
@ExceptionHandler(OptimisticLockingFailureException.class)
ResponseEntity<ProblemDetail> onConflict(OptimisticLockingFailureException e) {
    ProblemDetail pd = ProblemDetail.forStatus(CONFLICT);
    pd.setDetail("Yozuv boshqa foydalanuvchi tomonidan o'zgartirildi");
    return ResponseEntity.of(pd).build();
}
```

Review da `@Version` ning yo'qligi har doim savol: bu entity ni ikki foydalanuvchi bir vaqtda o'zgartirishi mumkinmi. Admin paneldan boshqariladigan har qanday ma'lumot uchun javob "ha".

### 15.4 Qulf tartibi va deadlock

Deadlock diffda ko'rinmaydi, chunki u ikki turli kod yo'lining o'zaro ta'siridan paydo bo'ladi. Reviewer uni faqat "bu kod boshqa qanday qulflar bilan uchrashadi" savolini berib topadi.

```java
// Yo'l A: avval hisob, keyin buyurtma.
@Transactional
public void settle(AccountId acc, OrderId ord) {
    accounts.lockById(acc);
    orders.lockById(ord);
}
// Yo'l B (boshqa faylda): avval buyurtma, keyin hisob.
@Transactional
public void cancel(OrderId ord, AccountId acc) {
    orders.lockById(ord);
    accounts.lockById(acc);
}
// Ikki tranzaksiya bir vaqtda ishga tushsa - deadlock. PostgreSQL bittasini
// o'ldiradi (deadlock detected), foydalanuvchi 500 oladi.

// Review javobi: qulf tartibini loyiha bo'ylab bitta qilib belgilash.
// Masalan: har doim identifikator bo'yicha o'sish tartibida qulflash.
List<UUID> ids = Stream.of(accId, ordId).sorted().toList();   // barqaror tartib
ids.forEach(this::lockById);
```

```sql
-- Deadlock larni topish: prodda sodir bo'lgach loglardan.
-- postgresql.conf: log_lock_waits = on, deadlock_timeout = 1s
-- Hozirgi qulf kutishlarini ko'rish:
SELECT blocked.pid AS blocked_pid, blocked.query AS blocked_query,
       blocking.pid AS blocking_pid, blocking.query AS blocking_query
  FROM pg_stat_activity blocked
  JOIN pg_stat_activity blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
 WHERE blocked.wait_event_type = 'Lock';
```

### 15.5 Bir JVM dagi qulf ko'p instansda ishlamaydi

`synchronized` va `ReentrantLock` faqat bitta JVM ichida ishlaydi. Kubernetes da uch pod bo'lsa, uch mustaqil qulf bo'ladi va himoya yo'q.

```java
// Naqsh: bitta instans uchun yozilgan himoya.
@Scheduled(cron = "0 0 2 * * *")
public synchronized void nightlyBilling() {       // uch podda uch marta ishlaydi
    invoices.generateForAll();
}

// Yechim 1: ma'lumotlar bazasidagi advisory lock (qo'shimcha tizim kerak emas).
@Scheduled(cron = "0 0 2 * * *")
public void nightlyBilling() {
    // pg_try_advisory_lock darhol qaytadi: false bo'lsa boshqa pod ishlayapti.
    Boolean acquired = jdbc.queryForObject(
        "SELECT pg_try_advisory_lock(?)", Boolean.class, BILLING_LOCK_ID);
    if (!Boolean.TRUE.equals(acquired)) {
        log.info("tungi billing boshqa instansda ishlayapti, o'tkazib yuborildi");
        return;
    }
    try { invoices.generateForAll(); }
    finally {
        jdbc.update("SELECT pg_advisory_unlock(?)", BILLING_LOCK_ID);
    }
}
// Diqqat: advisory lock sessiyaga bog'langan. Pool dan olingan ulanish
// qaytarilsa, lock ham qoladi - shuning uchun finally shart, va ulanish
// uzilganda PostgreSQL uni o'zi bo'shatadi.

// Yechim 2: ShedLock yoki Quartz klasterli rejimi (tayyor mexanizm).
@Scheduled(cron = "0 0 2 * * *")
@SchedulerLock(name = "nightlyBilling", lockAtMostFor = "30m", lockAtLeastFor = "1m")
public void nightlyBilling() { invoices.generateForAll(); }
```

Review savoli har bir `@Scheduled` uchun: bu ish ikki instansda bir vaqtda ishga tushsa nima bo'ladi. Javob "ikki marta hisob-faktura" yoki "ikki marta SMS" bo'lsa, qulf majburiy.

### 15.6 Atomiklik illuziyasi

Thread-safe kolleksiya uning ustidagi operatsiyalar ketma-ketligini atomik qilmaydi.

```java
// Naqsh: ConcurrentHashMap, lekin operatsiya atomik emas.
if (!cache.containsKey(key)) {          // T1 va T2: ikkisi ham "yo'q"
    cache.put(key, expensiveLoad(key)); // ikki marta yuklanadi
}
// To'g'ri: atomik birlashtirilgan operatsiya.
cache.computeIfAbsent(key, this::expensiveLoad);   // bir marta yuklanadi

// Naqsh: hisoblagich.
private volatile int counter;
counter++;                              // o'qish-qo'shish-yozish: atomik emas
// volatile ko'rinishni kafolatlaydi, atomiklikni emas.
private final AtomicInteger counter = new AtomicInteger();
counter.incrementAndGet();              // atomik
// Yoki yuqori yukda: LongAdder (kamroq raqobat).
private final LongAdder counter = new LongAdder();

// Naqsh: ikki maydonni birga o'zgartirish.
private volatile Instant from;
private volatile Instant to;
// Har biri alohida volatile, lekin juftlik nomuvofiq ko'rinishi mumkin:
// boshqa thread yangi from va eski to ni ko'radi.
// Yechim: ikkisini bitta immutable obyektga joylash.
private volatile DateRange range;       // bitta atomik almashtirish
```

### 15.7 Thread pool va navbat review

```java
// Naqsh 1: har chaqiruvda yangi pool - thread portlashi.
public void processAll(List<Order> orders) {
    ExecutorService ex = Executors.newFixedThreadPool(10);   // har chaqiruvda 10 thread
    orders.forEach(o -> ex.submit(() -> process(o)));
    // shutdown() yo'q: threadlar abadiy qoladi, OOM gacha o'sadi
}

// Naqsh 2: cheksiz navbat - orqaga bosim yo'q.
new ThreadPoolExecutor(4, 4, 0L, MILLISECONDS, new LinkedBlockingQueue<>());
// Navbat cheksiz: yuk oshganda xotira to'ladi va kechikish cheksiz o'sadi.
// Tez xato berish yaxshiroq.

// To'g'ri: bean sifatida, chegaralangan navbat, aniq rad etish siyosati.
@Bean(destroyMethod = "shutdown")
ThreadPoolTaskExecutor orderExecutor(MeterRegistry registry) {
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setCorePoolSize(8);
    ex.setMaxPoolSize(16);
    ex.setQueueCapacity(500);                 // chegara bor
    ex.setThreadNamePrefix("order-");         // thread dump da o'qiladi
    // Navbat to'lsa: chaqiruvchi o'zi bajaradi - tabiiy orqaga bosim.
    ex.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
    ex.setWaitForTasksToCompleteOnShutdown(true);
    ex.setAwaitTerminationSeconds(30);        // graceful shutdown
    ex.initialize();
    // Metrikaga ulash: navbat uzunligi va aktiv threadlar ko'rinadi.
    ExecutorServiceMetrics.monitor(registry, ex.getThreadPoolExecutor(), "order");
    return ex;
}
```

Review savollari pool uchun: hajmi nimaga asoslangan (CPU yoki I/O), navbat chegarasi bormi, rad etish siyosati nima, shutdown qanday, va navbat uzunligi o'lchanadimi.

### 15.8 @Async va xatoning yo'qolishi

```java
// Naqsh: @Async void - xato hech qayerga bormaydi.
@Async
public void sendReceipt(OrderId id) {
    mailer.send(id);                    // istisno jim yutiladi
}

// Yechim 1: CompletableFuture qaytarish va xatoni ishlash.
@Async("orderExecutor")
public CompletableFuture<Void> sendReceipt(OrderId id) {
    return CompletableFuture.runAsync(() -> mailer.send(id));
}

// Yechim 2: global ishlovchi (void metodlar uchun yagona yo'l).
@Configuration
@EnableAsync
class AsyncConfig implements AsyncConfigurer {
    @Override public Executor getAsyncExecutor() { return orderExecutor; }
    @Override public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> {
            log.error("async xato: {} args={}", method.getName(), params, ex);
            meter.counter("async.failed", "method", method.getName()).increment();
        };
    }
}
```

Qo'shimcha review savoli: `@Async` metod `@Transactional` bilan birga ishlatilganmi. Async thread da yangi tranzaksiya boshlanadi, chaqiruvchining tranzaksiyasi uzatilmaydi; va agar async ishi commit dan oldin ishga tushsa, u hali saqlanmagan ma'lumotni o'qishga urinadi.

### 15.9 ThreadLocal va kontekst oqishi

```java
// ThreadLocal pool dagi thread da qoladi: keyingi so'rov eski qiymatni ko'radi.
public class TenantContext {
    private static final ThreadLocal<TenantId> CURRENT = new ThreadLocal<>();
    public static void set(TenantId id) { CURRENT.set(id); }
    public static TenantId get() { return CURRENT.get(); }
    public static void clear() { CURRENT.remove(); }        // majburiy!
}
// Filter da tozalash finally ichida bo'lishi shart:
try { TenantContext.set(tenantFrom(request)); chain.doFilter(req, res); }
finally { TenantContext.clear(); }
// Aks holda: A tenant so'rovidan keyin B tenant so'rovi A ning ma'lumotini
// ko'radi - bu xavfsizlik incidenti, nafaqat xato.
```

Virtual threadlar bilan bu muammo shakli o'zgaradi: har vazifa uchun yangi thread bo'lgani uchun oqish kamroq, lekin `ScopedValue` afzal ko'riladi. Review da `MDC` (log konteksti) ham xuddi shu tekshiruvni talab qiladi: async chegarasida u ko'chiriladimi.

### 15.10 Virtual thread va pinning

Java 21 dan keyin `spring.threads.virtual.enabled=true` bitta qator bilan xulqni tubdan o'zgartiradi. Review da uch narsa tekshiriladi.

```java
// 1) Pool kattaligi endi throughput ni cheklamaydi - lekin DB pool cheklaydi.
//    10 000 virtual thread 20 ta DB ulanishini kutadi: navbat DB da paydo bo'ladi.
//    Review savoli: Hikari pool va timeout qiymatlari qayta ko'rildimi?

// 2) synchronized bloki ichida uzoq bloklanish carrier thread ni band qiladi
//    (pinning). ReentrantLock esa virtual thread ni to'g'ri "parklaydi".
// Yomon:
public synchronized Token refresh() { return http.fetchToken(); }   // pinning
// Yaxshi:
private final ReentrantLock lock = new ReentrantLock();
public Token refresh() {
    lock.lock();
    try { return http.fetchToken(); } finally { lock.unlock(); }
}

// 3) ThreadLocal keshlari endi foyda bermaydi: har vazifa yangi thread.
//    Pool ga tayangan kesh (ThreadLocal<SimpleDateFormat>) ma'nosiz bo'ladi.
```

### 15.11 Concurrency uchun review checklisti

| Savol | Nimaga qaraladi |
| --- | --- |
| Bean ichida `final` bo'lmagan maydon bormi | Singleton da so'rov holati |
| `static` mutable holat bormi | Butun JVM bo'ylab umumiy |
| Tekshir-keyin-yoz naqshi bormi | Unique constraint yoki atomik UPDATE kerak |
| Entity da `@Version` bormi | Parallel tahrirlash mumkinmi |
| Bir necha qulf olinadimi, tartibi barqarormi | Deadlock xavfi |
| `@Scheduled` ikki instansda ishlaydimi | Taqsimlangan qulf kerak |
| Pool chegaralanganmi, navbat cheklanganmi | Orqaga bosim va OOM |
| `@Async` xatosi qayerga boradi | Jim nosozlik |
| `ThreadLocal` tozalanadimi | Ma'lumot aralashuvi |
| Virtual thread yoqilgan bo'lsa, `synchronized` uzoq bloklaydimi | Pinning |
| Kolleksiya operatsiyalari atomikmi | `computeIfAbsent` va boshqalar |
| Timeout har bir bloklanadigan chaqiruvda bormi | Thread to'planishi |

### 15.12 Amalda qo'llash

- [ ] Barcha `@Service`, `@Component` bean larini skanerlab, `final` bo'lmagan maydonlari borlarini ro'yxatga oling va har birini tekshiring.
- [ ] Tekshir-keyin-yoz naqshlarini toping (`existsBy` yoki `findBy` keyin `save`) va ularga unique constraint yoki atomik `UPDATE` qo'shing.
- [ ] Admin paneldan tahrirlanadigan entity larga `@Version` qo'shing va `OptimisticLockingFailureException` uchun 409 javob handleri yozing.
- [ ] Barcha `@Scheduled` metodlarni sanab, ularning har birida taqsimlangan qulf borligini tekshiring (advisory lock yoki ShedLock).
- [ ] Barcha `ExecutorService` va `TaskExecutor` konfiguratsiyalarini ko'rib, navbat chegarasi va rad etish siyosati borligini tasdiqlang.
- [ ] `ExecutorServiceMetrics` orqali pool metrikalarini Prometheus ga ulang va navbat uzunligi uchun alert qo'ying.
- [ ] `@Async` void metodlarni toping va `AsyncUncaughtExceptionHandler` sozlanganini tekshiring.
- [ ] `ThreadLocal` ishlatilgan joylarda `remove()` ning `finally` ichida chaqirilganini tasdiqlang.
- [ ] Virtual thread yoqilgan bo'lsa, uzoq bloklanadigan `synchronized` bloklarini `ReentrantLock` ga o'tkazing.

## 16. Resurs, xotira va GC bosimi review (Resources and Memory)

Xotira muammolari diffda deyarli ko'rinmaydi: bitta qator kod 2 million obyekt yaratishi mumkin. Shu sababli bu bobning asosiy savoli hajm haqida: shu kod eng katta real kirishda nechta obyekt yaratadi va nechtasini bir vaqtda ushlab turadi. JVM xotira hududlari va GC mexanikasi `java-spring-architect-mindset.md` da; bu yerda diffdan hajmni baholash.

### 16.1 Chegarasiz to'plam - eng ko'p uchraydigan OOM sababi

```java
// Naqsh: butun jadvalni xotiraga yuklash. Diffda bir qator, prodda OOM.
List<Order> all = orders.findAll();                       // 4 mln qator
Map<String, Order> byNumber = all.stream()
    .collect(toMap(Order::number, identity()));           // yana 4 mln yozuv

// Review izohi: `orders` jadvalida hozir 4.2 mln qator (DB da tekshirdim).
// Har bir Order taxminan 400 bayt + kolleksiyalar bilan ko'proq, ya'ni
// kamida 1.7 GB. Pod limiti 1 GB - bu kod birinchi ishga tushishda OOM.

// Yechim 1: so'rovda filtrlash va chegaralash.
List<Order> recent = orders.findTop500ByStatusOrderByCreatedAtDesc(OPEN);

// Yechim 2: bo'laklab ishlash (katta hajm uchun).
int page = 0;
Slice<Order> slice;
do {
    slice = orders.findByStatus(OPEN, PageRequest.of(page++, 1_000));
    process(slice.getContent());
    em.clear();                      // birinchi daraja keshni bo'shatish
} while (slice.hasNext());
// Diqqat: Page emas, Slice - Page har safar COUNT(*) so'rovini bajaradi.

// Yechim 3: kursor bilan oqim (eng tejamli, 5.7 da ko'rsatilgan).
```

### 16.2 Hajmni diffdan baholash

Reviewer bir nechta oddiy raqamni yodda tutsa, hajmni tez chamalay oladi.

| Narsa | Taxminiy hajm |
| --- | --- |
| Obyekt sarlavhasi | 12-16 bayt |
| `Long` o'rami | ~16 bayt (primitiv 8) |
| `String` (n belgi, lotin) | ~40 + n bayt |
| `ArrayList` elementi | 4-8 bayt havola + obyekt |
| `HashMap` yozuvi | ~32-48 bayt + kalit va qiymat |
| JPA entity (10 maydon) | 200-500 bayt |
| JSON matn (entity) | 2-5 baravar entity dan katta |

```bash
# Review paytida haqiqiy hajmni tekshirish: taxmin qilmaslik.
psql -c "SELECT relname,
                to_char(n_live_tup, '999G999G999') AS qatorlar,
                pg_size_pretty(pg_total_relation_size(relid)) AS hajm
           FROM pg_stat_user_tables
          ORDER BY n_live_tup DESC LIMIT 10;"

# Pod xotira limiti va hozirgi heap sozlamasi.
kubectl get deploy order-service -o jsonpath='{.spec.template.spec.containers[0].resources}'
# JVM konteynerda limitning qanchasini oladi (standart 25%):
java -XX:+PrintFlagsFinal -version | grep -E 'MaxRAMPercentage|MaxHeapSize'
```

Review izohining kuchi aynan shu raqamlarda: "jadval katta bo'lishi mumkin" degan gap bahs tug'diradi, "jadvalda 4.2 mln qator, pod limiti 1 GB" degan gap qarorni hal qiladi.

### 16.3 Resursni yopish

```java
// Naqsh 1: Stream yopilmaydi (5.7 da ko'rilgan).
// Naqsh 2: javax/jakarta resurslari.
InputStream in = s3.getObject(key);           // yopilmasa - ulanish pool i tugaydi
// try-with-resources majburiy:
try (InputStream in = s3.getObject(key)) { ... }

// Naqsh 3: javadagi ichki resurs e'tibordan chetda.
Files.lines(path).forEach(this::process);     // fayl deskriptori yopilmaydi
try (Stream<String> lines = Files.lines(path, UTF_8)) { lines.forEach(this::process); }

// Naqsh 4: HttpClient javob tanasi o'qilmaydi yoki yopilmaydi.
// Spring RestClient/WebClient o'zi boshqaradi, lekin quyi darajada:
try (Response r = okHttp.newCall(req).execute()) { ... }   // yopilmasa pool oqadi

// Naqsh 5: ExecutorService yopilmaydi (15.7).
// Naqsh 6: temporary fayl o'chirilmaydi.
Path tmp = Files.createTempFile("report", ".pdf");
try { ... } finally { Files.deleteIfExists(tmp); }   // disk to'lishi oldini oladi
```

### 16.4 Kesh - boshqarilmagan xotira

Kesh xotira muammolarining ikkinchi eng katta manbasi, chunki u ongli ravishda ma'lumotni ushlab turadi.

```java
// Naqsh: chegarasiz kesh.
private final Map<String, Report> cache = new HashMap<>();   // o'sishi cheksiz

// To'g'ri: hajm, TTL, metrika va yakkalash siyosati.
@Bean
Cache<ReportKey, Report> reportCache(MeterRegistry registry) {
    Cache<ReportKey, Report> cache = Caffeine.newBuilder()
        .maximumWeight(50 * 1024 * 1024)                 // 50 MB chegarasi
        .weigher((ReportKey k, Report v) -> v.sizeInBytes())
        .expireAfterWrite(Duration.ofMinutes(15))
        .recordStats()
        .build();
    CaffeineCacheMetrics.monitor(registry, cache, "report");   // hit rate ko'rinadi
    return cache;
}
```

Kesh uchun review savollari: hajmi cheklanganmi, qachon eskiradi, invalidatsiya qanday ishlaydi, hit rate o'lchanadimi, va eng muhimi - keshlangan ma'lumot foydalanuvchiga bog'liqmi. Oxirgi savol xavfsizlik bilan bog'liq: kalitda `tenantId` yoki `userId` bo'lmasa, bir foydalanuvchi boshqasining ma'lumotini oladi.

```java
// Xavfsizlik xatosi keshda: kalit foydalanuvchini hisobga olmaydi.
@Cacheable(value = "orders", key = "#page")                  // xato!
public List<OrderDto> myOrders(int page) {
    return orders.findByCustomer(currentUser().id(), page);  // natija har kimga boshqa
}
// To'g'ri: kalitda foydalanuvchi bor.
@Cacheable(value = "orders", key = "#root.target.currentUser().id() + ':' + #page")
```

### 16.5 Allokatsiya bosimi: GC ni ko'p ishlashga majburlash

Xotira yetarli bo'lsa ham, ko'p obyekt yaratish latency ga ta'sir qiladi: young GC tez-tez ishlaydi, p99 o'sadi.

| Naqsh | Nima bo'ladi |
| --- | --- |
| Siklda yangi `StringBuilder`, `SimpleDateFormat`, `ObjectMapper` | Har iteratsiyada ortiqcha obyekt |
| Siklda satr konkatenatsiyasi | O(n^2) allokatsiya |
| Autoboxing siklda (`Map<Integer,...>` kalitlar) | Har operatsiyada `Integer` o'rami |
| Katta `byte[]` ni to'liq xotiraga o'qish | Humongous allokatsiya (G1 da alohida muammo) |
| Logda `String.format` yoki konkatenatsiya | Log o'chirilgan bo'lsa ham hisob bajariladi |
| Ortiqcha DTO zanjiri | Har qatlamda yangi obyekt |

```java
// Log allokatsiyasi: eng ko'p e'tibordan chetda qoladigan joy.
log.debug("buyurtma qayta ishlandi: " + order.toString() + " " + total);   // har doim
log.debug("buyurtma qayta ishlandi: {} {}", order.id(), total);            // lazy
// Birinchi variantda DEBUG o'chirilgan bo'lsa ham satr quriladi.
// Katta kolleksiya uchun esa:
if (log.isTraceEnabled()) log.trace("qatorlar: {}", expensiveDump(rows));
```

### 16.6 Katta javob va serializatsiya

```java
// Naqsh: butun natija xotirada JSON ga aylanadi.
@GetMapping("/export")
public List<OrderDto> export() {                    // 500k qator -> ~300 MB JSON
    return orders.findAll().stream().map(OrderDto::from).toList();
}

// Yechim: oqimli javob, xotirada bir vaqtda bir qator.
@GetMapping(value = "/export", produces = "text/csv")
public void export(HttpServletResponse response) throws IOException {
    response.setHeader("Content-Disposition", "attachment; filename=orders.csv");
    try (PrintWriter out = response.getWriter();
         Stream<Order> rows = orders.streamAll()) {       // kursor
        out.println("id;number;total");
        rows.forEach(o -> {
            out.printf("%s;%s;%s%n", o.id(), o.number(), o.total());
            em.detach(o);                                 // keshni o'stirmaslik
        });
    }
}
// Review qo'shimcha savollari: timeout (nginx/ingress), mijoz uzilsa nima
// bo'ladi, va bu endpoint uchun rate limit bormi.
```

### 16.7 Xotira oqishining tipik manbalari Spring da

| Manba | Belgisi |
| --- | --- |
| `static` kolleksiyaga qo'shish | `static List.add` hech qachon tozalanmaydi |
| Listener ro'yxatdan chiqarilmaydi | `addListener` bor, `removeListener` yo'q |
| `ThreadLocal` tozalanmaydi | `remove()` yo'q (15.9) |
| Chegarasiz kesh | `HashMap` kesh sifatida |
| Class loader oqishi | Hot reload, ko'p deploy |
| Hibernate birinchi daraja keshi | Katta sikl ichida `clear()` yo'q |
| Ulanish/kursor yopilmaydi | `Stream`, `ResultSet` |
| Katta sessiya ma'lumoti | `HttpSession` ga katta obyektlar |
| Metrika teglarida cheksiz qiymat | `tag("userId", id)` - kardinallik portlashi |

Oxirgi band alohida e'tiborga loyiq: Micrometer teglarida foydalanuvchi ID si yoki URL yo'li bo'lsa, metrikalar soni cheksiz o'sadi va Prometheus ham, ilova xotirasi ham to'ladi.

```java
// Kardinallik portlashi: har foydalanuvchi uchun alohida metrika.
meter.counter("orders.created", "userId", userId.toString()).increment();   // xato
// To'g'ri: teglar cheklangan to'plamdan.
meter.counter("orders.created", "tier", customer.tier().name()).increment();
```

### 16.8 Connection pool: eng tez tugaydigan resurs

Xotiradan oldin tugaydigan resurs - DB ulanishlari. Review da har bir uzoq operatsiya uchun "bu ulanishni qancha ushlab turadi" savoli beriladi.

```java
// Naqsh: tranzaksiya ichida tashqi chaqiruv - ulanish 30 sekund band.
@Transactional
public void confirm(OrderId id) {
    Order o = orders.findById(id).orElseThrow();
    smsGateway.send(o.phone(), "tasdiqlandi");     // tashqi, sekin
    o.markConfirmed();
}
// 20 ta ulanishli pool da 20 parallel so'rov butun ilovani to'xtatadi:
// yangi so'rovlar connection-timeout gacha kutadi va 500 oladi.

// Yechim: tranzaksiyani qisqartirish, tashqi chaqiruvni tashqariga olish.
public void confirm(OrderId id) {
    Order o = orderTx.markConfirmed(id);           // qisqa tranzaksiya
    outbox.enqueueSms(o.phone(), "tasdiqlandi");   // yoki outbox ichida
}
```

```properties
# Pool sozlamalarini review da tekshirish uchun minimal to'plam.
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.connection-timeout=2000        # tez xato
spring.datasource.hikari.max-lifetime=1200000
spring.datasource.hikari.leak-detection-threshold=10000 # ushlab qolingan ulanish logi
spring.jpa.properties.hibernate.jdbc.batch_size=50
# PostgreSQL tomonda ham chegara bor: max_connections va har ulanish uchun
# ~5-10 MB. Ko'p pod x katta pool = DB da ulanish tugashi (PgBouncer kerak).
```

### 16.9 Review paytida xotirani o'lchash

```bash
# Yuqori xavfli PR ni lokalda ishga tushirib, haqiqiy raqamni olish.
# 1) Heap holati va obyekt taqsimoti.
jcmd <pid> GC.heap_info
jcmd <pid> GC.class_histogram | head -25          # eng ko'p obyektlar

# 2) GC bosimi: qancha vaqt GC da ketgan.
jcmd <pid> VM.native_memory summary 2>/dev/null | head -20
java -Xlog:gc*:file=/tmp/gc.log -jar app.jar      # keyin gc.log tahlili

# 3) Oqish borligini tekshirish: ikki snapshot farqi.
jcmd <pid> GC.class_histogram > /tmp/h1.txt
# yuk berish
jcmd <pid> GC.class_histogram > /tmp/h2.txt
diff <(awk '{print $2, $4}' /tmp/h1.txt) <(awk '{print $2, $4}' /tmp/h2.txt) | head

# 4) Konteynerda limit va haqiqiy ishlatish.
kubectl top pod -l app=order-service
```

### 16.10 Amalda qo'llash

- [ ] `findAll()` chaqiruvlarini loyihada toping va har biri uchun jadval hajmini `pg_stat_user_tables` dan tekshiring.
- [ ] Chegarasiz kesh sifatida ishlatilgan `HashMap` va `ConcurrentHashMap` larni toping va Caffeine ga (hajm + TTL + metrika bilan) o'tkazing.
- [ ] Kesh kalitlarida foydalanuvchi yoki tenant identifikatori borligini tekshiring - yo'q bo'lsa, bu xavfsizlik xatosi.
- [ ] Barcha `Stream` qaytaradigan repository metodlarini toping va ularning `try-with-resources` ichida ishlatilganini tasdiqlang.
- [ ] Log chaqiruvlarida konkatenatsiya ishlatilgan joylarni platsholder ga o'tkazing.
- [ ] Micrometer teglarida yuqori kardinallikdagi qiymatlarni (ID, URL, email) toping va olib tashlang.
- [ ] `@Transactional` metodlar ichida tashqi chaqiruvlarni grep bilan aniqlab, har biri uchun tranzaksiyani qisqartirish rejasini yozing.
- [ ] `leak-detection-threshold` ni yoqib, ushlab qolingan ulanishlar haqidagi loglarni bir hafta kuzatib boring.
- [ ] Eksport va hisobot endpointlarini oqimli javobga o'tkazing va ularga rate limit qo'ying.

## 17. Zamonaviy Java review: record, sealed, pattern matching, virtual thread (Modern Java)

Yangi til imkoniyatlari review ga ikki xil ta'sir qiladi. Biri foydali: `record` va `sealed` xatolarni kompilyatsiyaga ko'chiradi, ya'ni reviewer ularni tekshirishdan ozod bo'ladi. Ikkinchisi xavfli: yangi imkoniyat noto'g'ri joyda ishlatilsa, muammo ko'rinmas bo'ladi. Bu bob har ikki tomonni ko'radi.

### 17.1 record: qachon to'g'ri, qachon noto'g'ri

```java
// To'g'ri ishlatilish: immutable qiymat, tenglik qiymat bo'yicha.
public record Money(BigDecimal amount, Currency currency) { }        // value object
public record PlaceOrder(CustomerId customer, List<LineItem> lines) { }  // command
public record OrderView(UUID id, String number, String total) { }    // o'qish modeli

// Noto'g'ri: JPA entity. Record maydonlari final, no-arg konstruktor yo'q,
// proxy yaratilmaydi - Hibernate buni boshqara olmaydi.
public record Order(Long id, String number) { }                      // entity emas

// Diqqat 1: record "sayoz" immutable. Kolleksiya ichi o'zgarishi mumkin.
public record Basket(List<Item> items) {
    public Basket {
        items = List.copyOf(items);          // nusxa olish majburiy
    }
    // Aks holda: tashqaridagi ro'yxatga element qo'shilsa, Basket o'zgaradi.
}

// Diqqat 2: record ichida validatsiya - kompakt konstruktor.
public record Quantity(int value) {
    public Quantity {
        if (value <= 0) throw new IllegalArgumentException("qiymat musbat bo'lsin");
    }
}

// Diqqat 3: record ning equals i hamma maydonni oladi. Agar maydonlardan
// biri array bo'lsa - havola taqqoslanadi (14.2).
public record Payload(byte[] data) { }       // equals ishlamaydi, review da e'tibor
```

### 17.2 sealed: to'liqlikni kompilyatorga topshirish

`sealed` review ning ishini kamaytiradigan eng foydali imkoniyat: yangi holat qo'shilganda barcha `switch` lar kompilyatsiyada xato beradi, ya'ni reviewer "hamma joy yangilandimi" savolini bermasa ham bo'ladi.

```java
// Natija turini sealed qilish: chaqiruvchi hamma holatni ko'rishga majbur.
public sealed interface TransferResult {
    record Completed(TransactionId id, Instant at) implements TransferResult { }
    record Rejected(RejectReason reason) implements TransferResult { }
    record RequiresApproval(ApprovalId id, Money threshold) implements TransferResult { }
}

// Chaqiruvchi tomonda: default yo'q, kompilyator to'liqlikni ta'minlaydi.
ResponseEntity<?> response = switch (transfers.execute(cmd)) {
    case Completed c -> ResponseEntity.ok(new TransferResponse(c.id(), c.at()));
    case Rejected r  -> ResponseEntity.unprocessableEntity().body(problem(r.reason()));
    case RequiresApproval a -> ResponseEntity.accepted()
            .body(new ApprovalRequired(a.id(), a.threshold()));
};
// Review foydasi: yangi holat (masalan Pending) qo'shilsa, bu switch
// kompilyatsiya bo'lmaydi. Istisnolar bilan qilingan dizaynda bu
// kafolat yo'q - yangi istisno turini hech kim ushlamasligi mumkin.
```

Review savoli: natija "muvaffaqiyat yoki istisno" shaklida yetarli ifodalanadimi. Biznes rad etishi (karta rad etildi, limit oshdi) istisno emas - bu normal natija, va `sealed` bilan ifodalanishi yaxshiroq. Istisno esa kutilmagan holatlar uchun qoladi.

### 17.3 Pattern matching: shoxlanishni qisqartirish, lekin yashirmaslik

```java
// Foydali: tur tekshiruvi va ajratish bir qadamda.
if (event instanceof OrderPaid paid && paid.total().isGreaterThan(LIMIT)) {
    review.flag(paid.orderId());
}

// Record pattern bilan ichki qiymatni olish.
switch (command) {
    case PlaceOrder(CustomerId customer, List<LineItem> lines) when lines.isEmpty() ->
        throw new EmptyOrder();
    case PlaceOrder(CustomerId customer, List<LineItem> lines) ->
        orders.place(customer, lines);
    case CancelOrder(OrderId id, String reason) ->
        orders.cancel(id, reason);
}

// Review diqqati: `when` shartlari ko'payib ketsa, bu yashirin biznes
// qoidalari to'planishi. Uch-to'rtdan ko'p `when` bo'lsa, qoidalar
// domen obyektiga ko'chirilishi kerak - aks holda qoida `switch` ichida
// yashiringan bo'ladi va test qilish qiyin.
```

### 17.4 Virtual threadlar: diffdagi bitta qator, tizimdagi katta o'zgarish

```properties
# Bitta qator butun ijro modelini o'zgartiradi.
spring.threads.virtual.enabled=true
```

Review da shu qator uchun to'rt savol beriladi:

1. DB pool qayta hisoblanganmi. Virtual threadlar cheksiz, lekin Hikari pool emas: 10 000 so'rov 20 ta ulanishni kutadi. Navbat va `connection-timeout` yangi sharoitda qayta ko'riladi.
2. `synchronized` bilan uzoq bloklanish bormi (15.10 dagi pinning).
3. `ThreadLocal` ga tayangan kesh bormi - endi foyda bermaydi.
4. Tashqi servislar bu yukni ko'taradimi. Virtual threadlar sizning ilovangizni tez qiladi, keyingi servisni esa yuk bilan ko'madi - rate limit va bulkhead kerak.

```java
// Strukturali konkurentlik (Java 21+ preview/22+): parallel chaqiruvlarni
// bitta hayot sikli bilan boshqarish. Review da afzal ko'riladi, chunki
// xato va bekor qilish aniq.
public OrderPage load(OrderId id) throws InterruptedException {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Subtask<Order> order = scope.fork(() -> orders.byId(id));
        Subtask<List<Shipment>> ships = scope.fork(() -> shipments.forOrder(id));
        Subtask<Invoice> invoice = scope.fork(() -> invoices.forOrder(id));

        scope.joinUntil(Instant.now().plusSeconds(2));   // umumiy deadline
        scope.throwIfFailed(OrderPageFailed::new);        // biri yiqilsa - hammasi

        return new OrderPage(order.get(), ships.get(), invoice.get());
    }
}
// Qiyoslash: uchta CompletableFuture bilan yozilganda timeout har biriga
// alohida, bekor qilish qo'lda, va bitta xato qolganlarini to'xtatmaydi.
```

### 17.5 Text block va SQL

```java
// Text block SQL ni o'qiladigan qiladi, lekin injection xavfini
// o'zgartirmaydi. Review da shu farq muhim.
String sql = """
    SELECT o.id, o.number, o.total
      FROM orders o
     WHERE o.customer_id = ?
       AND o.created_at >= ?
     ORDER BY o.created_at DESC
     LIMIT 100
    """;                                    // parametrlar bilan - xavfsiz

// Xavfli variant text block da ham xuddi shunday xavfli:
String sql = """
    SELECT * FROM orders ORDER BY %s
    """.formatted(sortBy);                  // injection (29-bob)
```

### 17.6 `var`: qachon o'qishni osonlashtiradi

```java
// Foydali: tur o'ng tomondan aniq ko'rinadi.
var orders = new ArrayList<Order>();
var entry = Map.entry(key, value);

// Zararli: tur ko'rinmaydi va o'qiyotgan odam IDE siz tushunmaydi.
var result = service.process(input);        // nima qaytdi?
var x = compute();                          // Optional? List? int?

// Review mezoni: diffni brauzerda o'qiyotgan odam turni bila oladimi.
// Bila olmasa - aniq tur yoziladi.
```

### 17.7 Yangi imkoniyatlarni qabul qilish siyosati

Review da takrorlanadigan bahsni oldini olish uchun jamoa yangi imkoniyatlar bo'yicha pozitsiyani yozib qo'yishi kerak.

```markdown
<!-- REVIEW.md ichida: til imkoniyatlari bo'yicha pozitsiya -->
## Til imkoniyatlari

| Imkoniyat | Pozitsiya |
|---|---|
| `record` | DTO, command, event, value object uchun standart. Entity uchun emas. |
| `sealed` | Natija turlari va domen holatlari uchun afzal. |
| Pattern matching `switch` | `instanceof` zanjiri o'rniga afzal. 4+ `when` bo'lsa - domenga ko'chirish. |
| `var` | Tur o'ng tomonda ko'rinsa - ha. Metod natijasida - yo'q. |
| Text block | SQL va JSON uchun standart. |
| Virtual threads | Yoqilgan. `synchronized` uzoq bloklash taqiqlanadi. |
| `Optional` | Qaytish turi sifatida. Maydon va parametr sifatida emas. |
| Stream `parallel()` | Faqat o'lchangan dalil bilan, bloklanmaydigan ish uchun. |
```

### 17.8 Amalda qo'llash

- [ ] `REVIEW.md` ga til imkoniyatlari pozitsiyasi jadvalini qo'shib, takrorlanadigan bahslarni to'xtating.
- [ ] Kolleksiya maydoni bo'lgan `record` larni toping va kompakt konstruktorda `List.copyOf` qilinganini tekshiring.
- [ ] Istisno bilan ifodalangan biznes rad etishlarini aniqlab, ularni `sealed` natija turiga o'tkazish variantini baholang.
- [ ] `default` bilan tugaydigan enum `switch` larini `sealed` yoki to'liq `switch` ga o'tkazing.
- [ ] `spring.threads.virtual.enabled=true` yoqilgan bo'lsa, Hikari pool va timeout qiymatlarini yuk sinovi bilan qayta tekshiring.
- [ ] `var` ishlatilgan joylarni ko'rib, metod natijasida turi ko'rinmaydiganlarni aniq turga o'tkazing.
- [ ] Parallel tashqi chaqiruvlarni `StructuredTaskScope` yoki umumiy deadline bilan qayta yozishni rejalashtiring.

# IV. Spring kodini review qilish

## 18. Bean, kontekst va proxy mexanikasi review (Beans, Context and Proxies)

Spring kodidagi eng jim xatolar annotatsiya ishlamaganda paydo bo'ladi: `@Transactional` qo'yilgan, lekin tranzaksiya yo'q; `@Cacheable` bor, lekin kesh ishlamaydi; `@Async` yozilgan, lekin kod sinxron ketadi. Kompilyator jim, test ko'pincha o'tadi, va xato prodda yuk ostida chiqadi. Sababi bitta: proxy mexanikasi. Shu sababli bu bob review ning Spring bo'limida birinchi turadi. Proxy ichki tuzilishi `java-spring-architect-mindset.md` da; bu yerda diffda ko'rinadigan buzilishlar.

### 18.1 Proxy ishlamaydigan to'rt holat

| Holat | Nega ishlamaydi | Diffdagi belgisi |
| --- | --- | --- |
| Shu klass ichidan chaqiruv | Proxy chetlab o'tiladi | `this.method()` yoki oddiy `method()` |
| `private` metod | Proxy uni o'ramaydi | `@Transactional private void` |
| `final` metod yoki klass | CGLIB meros qila olmaydi | `final` + annotatsiya |
| `static` metod | Instansga bog'liq emas | `@Cacheable static` |
| Konstruktor yoki `@PostConstruct` ichida | Proxy hali qurilmagan | `@PostConstruct` ichida `@Transactional` chaqiruvi |
| `new` bilan yaratilgan obyekt | Spring boshqarmaydi | `new OrderService(...)` |

```java
// Eng ko'p uchraydigan: ichki chaqiruv (12.3 da ko'rilgan, bu yerda yechimlar).
@Service
public class ImportService {

    public ImportReport importAll(List<Row> rows) {
        List<Failure> failures = new ArrayList<>();
        for (Row row : rows) {
            try {
                importOne(row);                    // proxy chetlab o'tiladi!
            } catch (Exception e) { failures.add(new Failure(row, e)); }
        }
        return new ImportReport(failures);
    }

    @Transactional(propagation = REQUIRES_NEW)     // ishlamaydi
    public void importOne(Row row) { ... }
}

// Yechim 1 (afzal): ikki bean ga ajratish - chegara ko'rinadi.
@Service
public class ImportService {                       // tranzaksiyasiz koordinator
    private final RowImporter importer;
    public ImportReport importAll(List<Row> rows) {
        ...
        importer.importOne(row);                   // proxy orqali, REQUIRES_NEW ishlaydi
    }
}
@Service
public class RowImporter {
    @Transactional(propagation = REQUIRES_NEW)
    public void importOne(Row row) { ... }
}

// Yechim 2: TransactionTemplate bilan aniq chegara - annotatsiya sehridan xoli.
@Service
public class ImportService {
    private final TransactionTemplate tx;          // propagation REQUIRES_NEW bilan sozlangan
    public ImportReport importAll(List<Row> rows) {
        for (Row row : rows) {
            tx.executeWithoutResult(status -> importOne(row));   // aniq, ko'rinadigan
        }
    }
}

// Yechim 3 (eng yomon, lekin uchraydi): o'z-o'ziga inyeksiya.
@Lazy @Autowired private ImportService self;       // self.importOne(row)
// Review izohi: ishlaydi, lekin niyatni yashiradi va sikl bog'liqlik
// yaratadi. Faqat refactoring imkoni bo'lmaganda vaqtinchalik.
```

### 18.2 Bean scope va holat

```java
// Naqsh: prototype bean singleton ga inyeksiya qilingan.
@Component
@Scope("prototype")
public class ReportBuilder { private List<Row> rows; }

@Service
public class ReportService {
    private final ReportBuilder builder;           // bir marta olinadi!
    // Prototype bo'lishiga qaramay, singleton ichida bitta instans qoladi
    // va holat so'rovlar orasida saqlanadi - 15.1 dagi xato.
}
// Yechim: ObjectProvider yoki fabrika.
private final ObjectProvider<ReportBuilder> builders;
ReportBuilder b = builders.getObject();            // har chaqiruvda yangi

// Naqsh: request scope bean background thread da ishlatilgan.
@Component @Scope(value = "request", proxyMode = TARGET_CLASS)
public class RequestContext { }
// @Async metodda bu bean ga murojaat - IllegalStateException:
// "No thread-bound request found". Review da @Async va request scope
// birga ishlatilishi har doim xato.
```

### 18.3 Konfiguratsiya va bean e'lonlari

```java
// Naqsh 1: @Configuration ichida bean metodini to'g'ridan-to'g'ri chaqirish.
@Configuration
class AppConfig {
    @Bean DataSource dataSource() { return new HikariDataSource(hikariConfig()); }
    @Bean HikariConfig hikariConfig() { return new HikariConfig(); }
    // dataSource() ichidan hikariConfig() chaqirilganda, @Configuration
    // proxy si uni ushlaydi va singleton qaytaradi (proxyBeanMethods=true).
    // Lekin @Configuration(proxyBeanMethods = false) bo'lsa - har chaqiruvda
    // yangi obyekt. Ikki xil xulq, diffda bir xil ko'rinadi.
}
// Review javobi: bog'liqlikni parametr orqali olish - xulq aniq bo'ladi.
@Bean DataSource dataSource(HikariConfig config) { return new HikariDataSource(config); }

// Naqsh 2: @ConditionalOnProperty bilan yashirin xulq.
@Bean
@ConditionalOnProperty(name = "feature.newPricing", havingValue = "true")
PricingStrategy newPricing() { ... }
// Review savoli: property yo'q bo'lsa nima bo'ladi? Agar boshqa
// PricingStrategy bean i bo'lmasa, ilova ishga tushmaydi yoki
// @ConditionalOnMissingBean bilan jim boshqa implementatsiya olinadi.
// Ikki holat ham diffda ko'rinmaydi - test bilan tekshirilishi kerak.

// Naqsh 3: bir xil turdagi ikki bean - qaysi biri olinadi noaniq.
@Bean RestClient paymentClient() { ... }
@Bean RestClient fraudClient() { ... }
// Inyeksiyada: RestClient client - NoUniqueBeanDefinitionException yoki
// maydon nomi bo'yicha tasodifiy mos kelish. @Qualifier majburiy.
```

### 18.4 Inyeksiya shakllari

```java
// Review da talab qilinadigan shakl: konstruktor inyeksiyasi.
@Service
public class OrderService {
    private final Orders orders;                   // final: o'zgarmaydi
    private final Clock clock;

    OrderService(Orders orders, Clock clock) {     // bitta konstruktor - @Autowired kerak emas
        this.orders = orders;
        this.clock = clock;
    }
}
// Foydasi: (1) testda `new OrderService(fakeOrders, fixedClock)` - kontekst
// kerak emas; (2) majburiy bog'liqliklar ko'rinadi; (3) sikl bog'liqlik
// ishga tushishda aniqlanadi, ish vaqtida emas.

// Taqiqlanadigan shakl: maydon inyeksiyasi.
@Autowired private Orders orders;                  // testda refleksiya kerak
// ArchUnit bilan taqiqlash (5.10 da ko'rsatilgan).

// Ixtiyoriy bog'liqlik: Optional yoki ObjectProvider, null emas.
OrderService(Orders orders, Optional<AuditSink> audit) { ... }
```

### 18.5 Ishga tushish tartibi va `@PostConstruct`

```java
// Naqsh: ishga tushishda tashqi tizimga murojaat.
@Component
public class RateLoader {
    @PostConstruct
    void load() {
        rates.putAll(rateClient.fetchAll());       // tashqi servis yiqilsa - ilova
    }                                              // ishga tushmaydi
}
// Review savollari: (1) bu ma'lumot ishga tushish uchun majburiymi?
// (2) tashqi servis javob bermasa, pod CrashLoopBackOff ga tushadimi?
// (3) timeout bormi? (4) readiness probe bilan munosabati qanday?

// Yaxshiroq: ishga tushish bloklanmaydi, ma'lumot keyin yuklanadi,
// holat health check da ko'rinadi.
@Component
public class RateLoader implements HealthIndicator {
    private final AtomicReference<Rates> rates = new AtomicReference<>();

    @Scheduled(fixedDelay = 60_000, initialDelay = 0)
    void refresh() {
        try { rates.set(rateClient.fetchAll()); }
        catch (Exception e) { log.warn("kurslar yangilanmadi", e); }
    }
    @Override public Health health() {
        Rates r = rates.get();
        return r == null ? Health.down().withDetail("rates", "yuklanmagan").build()
                         : Health.up().withDetail("asOf", r.asOf()).build();
    }
}
```

### 18.6 Kontekst sozlamalari diffda

| Belgi | Review savoli |
| --- | --- |
| `@ComponentScan` paketi kengaytirilgan | Qanday beanlar qo'shimcha topildi, ishga tushish vaqti o'zgardimi |
| `@EnableAsync`, `@EnableScheduling` qo'shilgan | Pool qaysi, xato ishlovchi bormi |
| `@EnableAspectJAutoProxy(exposeProxy = true)` | Nega kerak - bu self-invocation ni yashiradi |
| `spring.main.allow-bean-definition-overriding=true` | Qaysi bean almashtirilyapti va nega |
| `@Primary` qo'shilgan | Boshqa inyeksiya joylari ta'sirlandimi |
| `@Order` o'zgargan | Filter yoki aspekt tartibi muhimmi |
| `BeanPostProcessor` qo'shilgan | Barcha beanlarga ta'sir qiladi - juda kuchli mexanizm |
| `@Lazy` qo'shilgan | Nega: ishga tushish tezligi yoki sikl bog'liqlikni yashirish |

Oxirgi uchtasi alohida diqqat talab qiladi: ular global ta'sirga ega va diffda kichik ko'rinadi. `@Lazy` ning sikl bog'liqlikni yashirish uchun qo'yilishi tipik holat - bu muammoni yechmaydi, faqat ish vaqtiga ko'chiradi.

### 18.7 Spring Boot avtokonfiguratsiyasi bilan kurash belgilari

```java
// Belgi: avtokonfiguratsiyani o'chirish.
@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
// Review savoli: nega? Odatda bu konfiguratsiya muammosini yashirish
// uchun qilinadi va keyinroq boshqa joyda chiqadi.

// Belgi: bean ni qo'lda qayta e'lon qilish.
@Bean ObjectMapper objectMapper() { return new ObjectMapper(); }
// Review izohi: Spring Boot ning ObjectMapper i Jackson modullarini,
// JavaTimeModule ni va `spring.jackson.*` sozlamalarini hisobga oladi.
// Qo'lda yaratilgan ObjectMapper ularni yo'qotadi: natijada sanalar
// massiv sifatida serializatsiya bo'ladi va null lar javobga chiqadi.
// To'g'risi: Jackson2ObjectMapperBuilder yoki Jackson2ObjectMapperBuilderCustomizer.
@Bean Jackson2ObjectMapperBuilderCustomizer customizer() {
    return b -> b.serializationInclusion(JsonInclude.Include.NON_NULL)
                 .featuresToDisable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
}
```

### 18.8 Proxy va tranzaksiyani test bilan tekshirish

Review izohida "proxy ishlamaydi" degan gapni dalil bilan quvvatlash mumkin: test yoziladi va u mavjud kodda yiqiladi.

```java
// Tranzaksiya chegarasi haqiqatda qanday ishlayotganini ko'rsatadigan test.
@SpringBootTest
class TransactionBoundaryTest {

    @Autowired ImportService service;

    @Test
    void failingRowShouldNotRollbackOthers() {
        List<Row> rows = List.of(validRow(), invalidRow(), validRow());

        service.importAll(rows);

        // Niyat: ikki qator saqlanishi kerak (REQUIRES_NEW).
        // Mavjud kodda: 0 qator - hammasi qaytadi, chunki proxy chetlab
        // o'tilgan va bitta tranzaksiya rollback bo'ladi.
        assertThat(repository.count()).isEqualTo(2);
    }

    @Test
    void transactionIsActuallyActive() {
        // Tranzaksiya haqiqatda bor-yo'qligini tekshirishning to'g'ridan-to'g'ri yo'li.
        service.doWork(() ->
            assertThat(TransactionSynchronizationManager.isActualTransactionActive())
                .as("tranzaksiya aktiv bo'lishi kerak")
                .isTrue());
    }
}
```

```java
// Arxitektura testi bilan takrorlanishni oldini olish.
@ArchTest
static final ArchRule no_transactional_on_private_or_final =
    methodsThat(are(annotatedWith(Transactional.class)))
        .should().notBePrivate()
        .andShould().notBeFinal()
        .because("proxy private va final metodlarni o'ramaydi");

@ArchTest
static final ArchRule no_self_injection =
    noFields().should().haveRawType(DescribedPredicate.describe(
            "o'z klassi turida", f -> f.getRawType().equals(f.getOwner())))
        .because("o'z-o'ziga inyeksiya niyatni yashiradi");
```

### 18.9 Review checklisti: Spring konteksti

| Savol | Nega |
| --- | --- |
| Annotatsiyali metod shu klass ichidan chaqirilmaydimi | Proxy chetlab o'tiladi |
| Annotatsiyali metod `public` va `final` emasmi | Proxy o'rashi uchun |
| Konstruktor inyeksiyasi ishlatilganmi | Testlanadigan va immutable |
| Bir xil turdagi beanlar uchun `@Qualifier` bormi | Noaniqlik |
| `@PostConstruct` tashqi tizimga chiqmaydimi | Ishga tushish mo'rtligi |
| Prototype/request scope singleton ga inyeksiya qilinmaganmi | Holat oqishi |
| Avtokonfiguratsiya o'chirilgan bo'lsa, sabab yozilganmi | Yashirin muammo |
| `ObjectMapper`, `RestClient` qo'lda yaratilgan bo'lsa, sozlamalar saqlanganmi | Konfiguratsiya yo'qolishi |
| `@Primary`, `@Order`, `BeanPostProcessor` ta'siri baholanganmi | Global o'zgarish |
| Yangi `@Enable*` annotatsiyasi uchun pool va xato ishlovchi bormi | Jim nosozlik |

### 18.10 Amalda qo'llash

- [ ] `@Transactional`, `@Cacheable`, `@Async`, `@Retryable` annotatsiyali metodlarning shu klass ichidan chaqirilgan joylarini toping - hammasi ishlamaydi.
- [ ] `private` yoki `final` metodlarga qo'yilgan proxy annotatsiyalarini aniqlab, ArchUnit qoidasi bilan taqiqlang.
- [ ] Maydon inyeksiyasini (`@Autowired` maydonda) butunlay konstruktor inyeksiyasiga o'tkazing.
- [ ] `@PostConstruct` ichida tashqi tizimga murojaat qiladigan joylarni toping va ularni `@Scheduled` + `HealthIndicator` ga o'tkazing.
- [ ] Qo'lda yaratilgan `ObjectMapper` larni `Jackson2ObjectMapperBuilder` ga o'tkazib, sana formatlarini tekshiring.
- [ ] `spring.main.allow-bean-definition-overriding` yoqilgan bo'lsa, qaysi beanlar almashtirilayotganini aniqlang.
- [ ] Prototype va request scope bean larning singleton ga inyeksiya qilinganini tekshiring.
- [ ] Tranzaksiya chegarasi uchun `isActualTransactionActive()` tekshiruvi bilan kamida bitta test yozing.

## 19. Tranzaksiya chegarasi review (Transaction Boundaries)

Tranzaksiya chegarasi - Spring loyihasida eng ko'p xato qilinadigan dizayn qarori, va eng qimmat oqibat beradigan joy: noto'g'ri chegara ma'lumot nomuvofiqligi, uzoq qulflar yoki butun ilovaning to'xtashiga olib keladi. Bu bob chegarani diffdan baholashni beradi. Izolyatsiya darajalari va PostgreSQL MVCC mexanikasi 27-bobda va `java-spring-architect-mindset.md` da.

### 19.1 Chegara qayerda turishi kerak

Qoida: tranzaksiya biznes operatsiyasining chegarasi bo'ladi - bitta foydalanuvchi niyatining chegarasi. Amalda bu application servis metodi.

| Joy | Chegara bo'lishi | Sabab |
| --- | --- | --- |
| Controller | Yo'q | Web detallari tranzaksiyani uzaytiradi, OSIV muammolari |
| Application servis | Ha | Biznes operatsiyasi chegarasi |
| Domen servis | Odatda yo'q | Domen tranzaksiyani bilmasligi kerak |
| Repository | Yo'q (faqat o'z ichida) | Juda mayda chegara, invariant himoyalanmaydi |
| `@Scheduled` metod | Ha, lekin bo'laklab | Katta tranzaksiya qulflarni to'playdi |
| Kafka listener | Ha | Xabarni qayta ishlash chegarasi |

```java
// Chegara juda mayda: har repository chaqiruvi alohida tranzaksiyada.
public void transfer(AccountId from, AccountId to, Money amount) {
    accounts.debit(from, amount);      // tranzaksiya 1 - commit bo'ldi
    accounts.credit(to, amount);       // tranzaksiya 2 - yiqilsa, pul yo'qoladi
}
// Review izohi (blocker): bu ikki operatsiya atomik bo'lishi shart.
// Ikkinchisi yiqilsa, birinchisi qaytmaydi va hisobdan pul ketadi.

// Chegara juda keng: butun import bitta tranzaksiyada.
@Transactional
public void importAll(List<Row> rows) {     // 100 000 qator
    rows.forEach(this::importOne);
}
// Review izohlari: (1) bitta noto'g'ri qator butun importni qaytaradi;
// (2) 100k qator uchun qulflar tranzaksiya oxirigacha ushlanadi;
// (3) Hibernate birinchi daraja keshi 100k obyektni ushlaydi - OOM;
// (4) PostgreSQL da uzoq tranzaksiya VACUUM ni bloklaydi va jadval
//     bo'rtadi (bloat).
```

### 19.2 Tranzaksiya ichida tashqi chaqiruv - eng xavfli naqsh

Bu naqsh shu hujjatda bir necha marta uchraydi, chunki u review da eng ko'p topiladigan va eng qimmat xato.

```java
@Transactional
public void confirmOrder(OrderId id) {
    Order order = orders.findById(id).orElseThrow();
    order.confirm();                                  // DB qulfi olindi
    PaymentResult result = paymentGateway.capture(order.paymentId());  // tashqi!
    if (result.isDeclined()) throw new PaymentDeclined();
    notifications.send(order.customerEmail());        // yana tashqi!
}
```

Review izohi to'rt oqibatni sanab o'tadi:

1. DB ulanishi tashqi servis javobini kutib turadi. Pool 20 ta bo'lsa, 20 parallel so'rov butun ilovani to'xtatadi.
2. Qator qulfi shu vaqt ushlanadi: boshqa so'rovlar shu buyurtmaga tegishi kutadi.
3. To'lov o'tib, keyin commit yiqilsa - pul olingan, buyurtma tasdiqlanmagan. Teskarisi ham mumkin.
4. Tashqi servis timeout i DB tranzaksiya timeout idan katta bo'lsa, tranzaksiya avval uziladi va holat noaniq bo'ladi.

```java
// Yechim: tranzaksiyani uchga bo'lish - tashqi chaqiruv tashqarida.
public void confirmOrder(OrderId id) {
    // 1-tranzaksiya: niyatni qayd qilish (qisqa).
    Order order = orderTx.markConfirming(id);

    // Tranzaksiyadan tashqarida: tashqi chaqiruv, timeout bilan.
    PaymentResult result = paymentGateway.capture(order.paymentId());

    // 2-tranzaksiya: natijani yozish (qisqa).
    orderTx.applyPaymentResult(id, result);
    // Xabar yuborish outbox orqali (10.8) - commit bilan atomik.
}
```

### 19.3 readOnly: nima beradi, nima bermaydi

```java
@Transactional(readOnly = true)
public List<OrderView> recent(CustomerId id) { ... }
```

`readOnly = true` nima beradi: Hibernate flush ni o'tkazib yuboradi va dirty checking qilmaydi (tezlik), ba'zi marshrutlovchilar so'rovni replikaga yuboradi, va PostgreSQL da tranzaksiya `READ ONLY` sifatida belgilanadi.

Nima bermaydi: u yozuvni taqiqlashning ishonchli usuli emas - JDBC orqali to'g'ridan-to'g'ri yozuv o'tishi mumkin, va `readOnly` bilan belgilangan metod ichidan boshqa yozadigan metod chaqirilsa, xulq propagation ga bog'liq.

Review savollari: o'qish metodlarida `readOnly` qo'yilganmi (katta o'qishlarda sezilarli farq beradi), va `readOnly` metod ichida yozuv yo'qligi tasdiqlanganmi.

### 19.4 Propagation: diffdagi ma'nosi

| Propagation | Ma'nosi | Review diqqati |
| --- | --- | --- |
| `REQUIRED` (standart) | Bor bo'lsa qo'shiladi, yo'q bo'lsa boshlaydi | Ichkarida istisno tashlansa, tashqi tranzaksiya ham rollback-only bo'ladi |
| `REQUIRES_NEW` | Har doim yangi tranzaksiya | Ikki ulanish egallanadi; proxy orqali chaqirilishi shart |
| `NESTED` | Savepoint | PostgreSQL da savepoint narxi bor; JPA bilan cheklovlar |
| `SUPPORTS` | Bor bo'lsa qo'shiladi, yo'q bo'lsa tranzaksiyasiz | Noaniq xulq: ikki rejimda ishlaydi |
| `NOT_SUPPORTED` | Tranzaksiyani to'xtatib turadi | Uzoq o'qish uchun foydali |
| `MANDATORY` | Tranzaksiya bo'lishi shart | Domen qoidasini majburlash uchun yaxshi |
| `NEVER` | Tranzaksiya bo'lmasligi shart | Kam ishlatiladi |

```java
// Eng ko'p uchraydigan yashirin xato: REQUIRED ichida ushlangan istisno.
@Transactional
public ImportReport importAll(List<Row> rows) {
    List<String> errors = new ArrayList<>();
    for (Row row : rows) {
        try {
            importOne(row);                 // @Transactional(REQUIRED) - bir xil tranzaksiya
        } catch (DataIntegrityViolationException e) {
            errors.add(row.id());           // istisno ushlandi, davom etamiz
        }
    }
    return new ImportReport(errors);        // bu nuqtada tranzaksiya rollback-only!
}
// Oqibati: metod oxirida commit urinilganda
// UnexpectedRollbackException: "Transaction silently rolled back" -
// hamma narsa qaytadi, hatto muvaffaqiyatli qatorlar ham.
// Sabab: ichki tranzaksiya REQUIRED bo'lgani uchun bir xil fizik
// tranzaksiyada ishlaydi va istisno uni rollback-only deb belgilaydi.
// Yechim: REQUIRES_NEW (alohida bean orqali) yoki qatorlarni oldin
// validatsiya qilib, keyin yozish.
```

### 19.5 Rollback qoidalari

```java
// Standart xulq: RuntimeException va Error - rollback;
// checked Exception - COMMIT (ko'pchilik buni bilmaydi).
@Transactional
public void process() throws IOException {
    orders.save(order);
    throw new IOException("fayl yozilmadi");     // tranzaksiya COMMIT bo'ladi!
}
// Review izohi: checked istisno tashlanganda Spring standart holatda
// rollback qilmaydi. Buyurtma saqlanadi, lekin fayl yozilmagan - holatlar
// ajralib ketadi. Agar rollback kerak bo'lsa, aniq ko'rsatish shart:
@Transactional(rollbackFor = Exception.class)

// Teskari holat: biznes istisnosida rollback kerak emas.
@Transactional(noRollbackFor = InsufficientFundsException.class)
public void withdraw(...) {
    attempts.record(accountId);           // urinish yozuvi saqlanishi kerak
    if (balance < amount) throw new InsufficientFundsException();
}
// Diqqat: bu nozik naqsh. Review da savol - urinish yozuvi haqiqatan
// saqlanishi kerakmi, va u alohida tranzaksiyada (REQUIRES_NEW) bo'lishi
// aniqroq bo'lmaydimi.
```

### 19.6 Tranzaksiya uzunligi va PostgreSQL ga ta'siri

Uzoq tranzaksiya nafaqat qulf ushlaydi, balki butun bazaga ta'sir qiladi: `VACUUM` eski versiyalarni tozalay olmaydi va jadvallar bo'rtadi.

```sql
-- Review paytida tekshirish: eng uzoq ishlayotgan tranzaksiyalar.
SELECT pid, now() - xact_start AS davomiyligi, state,
       left(query, 80) AS sorov
  FROM pg_stat_activity
 WHERE xact_start IS NOT NULL
   AND now() - xact_start > interval '30 seconds'
 ORDER BY xact_start;

-- Idle in transaction - eng xavfli holat: ulanish band, qulf bor, ish yo'q.
-- Bu deyarli har doim kod xatosi: tranzaksiya ochilib, tashqi chaqiruv
-- kutilyapti yoki commit chaqirilmagan.
SELECT count(*) FROM pg_stat_activity WHERE state = 'idle in transaction';
```

```properties
# Himoya chegaralarini qo'yish: review da shu sozlamalar borligini tekshirish.
# Ilova tomonda:
spring.transaction.default-timeout=10            # sekund
# PostgreSQL tomonda (foydalanuvchi yoki ulanish darajasida):
#   SET statement_timeout = '10s';
#   SET idle_in_transaction_session_timeout = '30s';
#   SET lock_timeout = '3s';
# Bu uchlik nazoratdan chiqqan tranzaksiyani o'zi to'xtatadi.
```

Review da `@Transactional(timeout = ...)` ning yo'qligi uzoq operatsiyalar uchun savol: agar bu metod odatda 100 ms ishlasa va bir kun 10 daqiqa ishlab qolsa, nima bo'ladi.

### 19.7 Commit dan keyin bajarilishi kerak bo'lgan ish

```java
// Xato: commit dan oldin tashqi ta'sir.
@Transactional
public void place(PlaceOrder cmd) {
    Order o = orders.save(Order.from(cmd));
    cache.evict("orders");                   // commit yiqilsa - kesh bekorga tozalangan
    searchIndex.index(o);                    // commit yiqilsa - indeksda yo'q buyurtma
}

// To'g'ri: commit dan keyin, aniq mexanizm bilan.
@Transactional
public void place(PlaceOrder cmd) {
    Order o = orders.save(Order.from(cmd));
    TransactionSynchronizationManager.registerSynchronization(
        new TransactionSynchronization() {
            @Override public void afterCommit() {
                cache.evict("orders");
                searchIndex.index(o);        // bu yiqilsa - log va metrika kerak
            }
        });
}
// Yoki deklarativ: @TransactionalEventListener(phase = AFTER_COMMIT) (11.5).
// Muhim ma'lumot uchun esa outbox (10.8) - afterCommit kafolat bermaydi:
// protsess shu oraliqda o'lsa, ish bajarilmaydi.
```

### 19.8 OSIV va lazy loading

```properties
# Spring Boot da standart holatda YOQILGAN:
spring.jpa.open-in-view=true
# Bu nima qiladi: Hibernate sessiyasi butun HTTP so'rov davomida ochiq
# qoladi, shuning uchun view (yoki JSON serializatsiya) paytida lazy
# maydonlarni yuklash mumkin.
```

Review da bu sozlama uchun aniq pozitsiya bo'lishi kerak:

| `open-in-view` | Foydasi | Narxi |
| --- | --- | --- |
| `true` (standart) | `LazyInitializationException` chiqmaydi | DB ulanishi so'rov oxirigacha band; serializatsiya paytida yashirin so'rovlar (N+1); xatolar javob yozilayotganda chiqadi |
| `false` | Ulanish tranzaksiya bilan birga bo'shaydi; so'rovlar ko'rinadigan joyda | Lazy maydonlarga tegilsa istisno - DTO yoki `JOIN FETCH` majburiy |

Review tavsiyasi: `false` qilib qo'yish va DTO/projection ishlatish. Bu N+1 muammolarini review paytida ko'rinadigan qiladi, chunki ular test yoki lokal ishga tushirishda darhol istisno bilan chiqadi.

### 19.9 Tranzaksiya, kesh, event va async aralashuvi

| Aralashuv | Xavf |
| --- | --- |
| `@Cacheable` + `@Transactional` | Rollback bo'lsa kesh eski qiymatni ushlab qoladi yoki yangi noto'g'ri qiymatni keshlaydi |
| `@CacheEvict` commit dan oldin | Rollback bo'lsa kesh bekorga tozalangan (zararsiz) yoki teskarisi (xavfli) |
| `@Async` + `@Transactional` | Async thread yangi tranzaksiya oladi; chaqiruvchi hali commit qilmagan ma'lumotni o'qiy olmaydi |
| `@EventListener` sinxron | Tranzaksiya ichida ishlaydi, uni uzaytiradi |
| `@Retryable` + `@Transactional` | Tartib muhim: retry tranzaksiyadan tashqarida bo'lishi kerak, aks holda rollback-only tranzaksiyada qayta urinish |
| `@Scheduled` + `@Transactional` | Ikki instansda bir vaqtda; qulf kerak (15.5) |

```java
// Retry va tranzaksiya tartibi: eng ko'p xato qilinadigan kombinatsiya.
// Yomon: retry tranzaksiya ichida - rollback bo'lgan tranzaksiyada qayta urinish.
@Transactional
@Retryable(retryFor = OptimisticLockingFailureException.class)
public void update(OrderId id) { ... }        // ishlamaydi: tranzaksiya allaqachon o'lgan

// To'g'ri: retry tashqarida, har urinishda yangi tranzaksiya.
@Service
public class OrderUpdater {                   // tashqi bean: retry chegarasi
    @Retryable(retryFor = OptimisticLockingFailureException.class, maxAttempts = 3)
    public void update(OrderId id) { tx.update(id); }
}
@Service
public class OrderTx {                        // ichki bean: tranzaksiya chegarasi
    @Transactional
    public void update(OrderId id) { ... }
}
```

### 19.10 Review checklisti: tranzaksiyalar

| Savol | Nega |
| --- | --- |
| Chegara application servisdami | Controller va repository da bo'lmasligi kerak |
| Tranzaksiya ichida tashqi chaqiruv bormi | Ulanish va qulf ushlanishi |
| Tashqi chaqiruvda timeout bormi | Tranzaksiya cheksiz cho'zilmasligi |
| O'qish metodlarida `readOnly` bormi | Tezlik va replika marshrutlash |
| `REQUIRES_NEW` proxy orqali chaqirilyaptimi | Aks holda ishlamaydi |
| Ichkarida ushlangan istisno bormi | `UnexpectedRollbackException` xavfi |
| Checked istisno uchun `rollbackFor` kerakmi | Standart xulq commit qiladi |
| Commit dan keyingi ish to'g'ri mexanizm bilanmi | `afterCommit` yoki outbox |
| `open-in-view` pozitsiyasi aniqmi | N+1 va ulanish ushlanishi |
| Uzoq operatsiyada `timeout` bormi | Nazoratdan chiqishni oldini olish |
| Batch ishlarda tranzaksiya bo'laklanganmi | Qulf va xotira |
| `@Version` yoki qulf bormi | Parallel yangilanish (15.3) |

### 19.11 Amalda qo'llash

- [ ] `@Transactional` metodlar ichida tashqi chaqiruvlarni (HTTP mijoz, Kafka, SMS, S3) grep bilan toping va ro'yxat tuzing.
- [ ] Barcha o'qish metodlariga `readOnly = true` qo'shilganini tekshiring.
- [ ] `@Transactional` bilan belgilangan controller metodlarini toping va chegarani servis qatlamiga ko'chiring.
- [ ] Ichkarida istisno ushlaydigan tranzaksion metodlarni aniqlab, `UnexpectedRollbackException` xavfini baholang.
- [ ] `throws` ro'yxatida checked istisno bo'lgan tranzaksion metodlarda `rollbackFor` ko'rsatilganini tekshiring.
- [ ] `spring.transaction.default-timeout`, `statement_timeout`, `lock_timeout` va `idle_in_transaction_session_timeout` qiymatlarini sozlang.
- [ ] `spring.jpa.open-in-view` bo'yicha jamoa pozitsiyasini `REVIEW.md` ga yozing (tavsiya: `false`).
- [ ] `pg_stat_activity` dan 30 sekunddan uzoq tranzaksiyalar va `idle in transaction` holatlarini bir hafta kuzatib boring.
- [ ] `@Retryable` va `@Transactional` birga ishlatilgan joylarda tartibni tekshirib, retry ni tashqi bean ga chiqaring.

## 20. Web qatlami review: DTO, validatsiya, xato javobi (The Web Layer)

Web qatlami - tizimning tashqi yuzasi. Bu yerdagi xato ikki tomonga qaraydi: tashqariga (mijoz sinadi, ma'lumot oqib chiqadi) va ichkariga (tekshirilmagan ma'lumot domenga kiradi). Review ning asosiy savoli: ishonilmaydigan kirish qayerda ishonchli ma'lumotga aylanadi, va javobda nima chiqib ketadi.

### 20.1 Tashqi shakl va ichki model chegarasi

```java
// Naqsh: entity to'g'ridan-to'g'ri qabul qilinadi va qaytariladi.
@PostMapping("/orders")
public Order create(@RequestBody Order order) {        // entity kirishda!
    return orders.save(order);                         // entity chiqishda!
}
```

Review izohi uchta aniq xavfni sanaydi:

1. Mass assignment: mijoz `{"id": 999, "status": "PAID", "total": 0}` yuborishi mumkin. Jackson barcha maydonlarni to'ldiradi, shu bilan mijoz o'z buyurtmasini to'langan deb belgilaydi.
2. Ichki maydonlar tashqariga chiqadi: `internalNote`, `costPrice`, `fraudScore`, boshqa foydalanuvchi ma'lumoti.
3. Jadval sxemasi API shartnomasiga aylanadi: ustun nomini o'zgartirish mijozni sindiradi.

```java
// To'g'ri: aniq kirish va chiqish shakllari, faqat ruxsat etilgan maydonlar.
public record CreateOrderRequest(
        @NotNull @Valid CustomerRef customer,
        @NotEmpty @Size(max = 100) @Valid List<LineRequest> lines,
        @Size(max = 500) String comment) { }

public record OrderResponse(
        UUID id, String number, String status,
        BigDecimal total, String currency,
        OffsetDateTime createdAt) {                    // ichki maydonlar yo'q
    static OrderResponse from(Order o) { ... }
}

@PostMapping("/orders")
public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
    Order order = orders.place(req.toCommand(currentUser()));
    return ResponseEntity.created(URI.create("/orders/" + order.id()))
                         .body(OrderResponse.from(order));
}
```

Qo'shimcha review diqqati: `customerId` so'rov tanasidan olinmasligi kerak - u autentifikatsiya kontekstidan olinadi. Aks holda foydalanuvchi boshqa mijoz nomidan buyurtma yaratadi (30-bob).

### 20.2 Validatsiya: qayerda va qanchalik

```java
// Review talabi: @Valid chegarada, va ichki obyektlarga ham tarqalgan.
public record LineRequest(
        @NotNull UUID productId,
        @Min(1) @Max(1000) int quantity) { }

public record CreateOrderRequest(
        @NotEmpty @Valid List<LineRequest> lines) { }   // @Valid ichkariga tarqaydi
// @Valid bo'lmasa: ichki obyektlarning annotatsiyalari tekshirilmaydi -
// bu eng ko'p o'tkazib yuboriladigan joy.

// Validatsiyaning uch darajasi va ularning joyi:
// 1) Shakl (format, uzunlik, diapazon) - DTO annotatsiyalari.
// 2) Domen qoidasi (status o'tishi, limit) - domen obyekti ichida.
// 3) Ma'lumot to'g'riligi (mavjudlik, yagonalik) - DB constraint + so'rov.
```

| Tekshiriladigan narsa | Qayerda | Nega |
| --- | --- | --- |
| Majburiy maydon, uzunlik, diapazon | DTO annotatsiyasi | Erta rad etish, aniq xato javobi |
| Format (email, telefon) | Value object konstruktori | Bir joyda, domenga kirmaydi |
| Biznes qoidasi | Domen metodi | Invariant himoyasi |
| Mavjudlik (`productId` bor) | Servis + FK | Poyga va yagona haqiqat |
| Yagonalik | DB unique indeks | Faqat u ishonchli (15.2) |
| Avtorizatsiya | Servis yoki metod security | Kirish huquqi |

```java
// Diqqat: @Validated va @Valid farqi - review da tez-tez chalkashtiriladi.
@RestController
@Validated                          // metod parametrlarini tekshirish uchun (@PathVariable, @RequestParam)
public class OrderController {
    @GetMapping("/orders")
    public List<OrderResponse> list(
            @RequestParam @Min(0) int page,                   // @Validated kerak
            @RequestParam @Max(100) int size) { ... }

    @PostMapping("/orders")
    public OrderResponse create(@Valid @RequestBody CreateOrderRequest req) { ... }
}                                   // @RequestBody uchun @Valid yetadi
```

### 20.3 Xato javobi: ichki detallar chiqmasligi

```java
// Naqsh: istisno xabari to'g'ridan-to'g'ri mijozga.
@ExceptionHandler(Exception.class)
public ResponseEntity<String> onError(Exception e) {
    return ResponseEntity.status(500).body(e.getMessage());   // ichki detallar!
}
// Oqibati: SQL so'rov matni, jadval nomlari, fayl yo'llari, kutubxona
// versiyalari mijozga ko'rinadi. Bu razvedka uchun tayyor ma'lumot.

// To'g'ri: standart shakl, ichki detal yo'q, korrelyatsiya ID bor.
@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ProblemDetail onValidation(MethodArgumentNotValidException e) {
        ProblemDetail pd = ProblemDetail.forStatus(BAD_REQUEST);
        pd.setTitle("Validatsiya xatosi");
        pd.setProperty("errors", e.getFieldErrors().stream()
            .map(f -> Map.of("field", f.getField(), "message", f.getDefaultMessage()))
            .toList());
        return pd;
    }

    @ExceptionHandler(OrderNotFound.class)
    ProblemDetail onNotFound(OrderNotFound e) {
        ProblemDetail pd = ProblemDetail.forStatus(NOT_FOUND);
        pd.setTitle("Buyurtma topilmadi");
        return pd;                               // ID ni qaytarmaymiz: enumeratsiya
    }

    @ExceptionHandler(Exception.class)
    ProblemDetail onUnexpected(Exception e) {
        String traceId = MDC.get("traceId");
        log.error("kutilmagan xato traceId={}", traceId, e);   // detallar logda
        ProblemDetail pd = ProblemDetail.forStatus(INTERNAL_SERVER_ERROR);
        pd.setTitle("Ichki xatolik");
        pd.setProperty("traceId", traceId);      // support uchun yetarli
        return pd;
    }
}
```

```properties
# Standart Spring xato javobidan ichki detallarni olib tashlash.
server.error.include-message=never
server.error.include-stacktrace=never
server.error.include-binding-errors=never
server.error.include-exception=false
```

### 20.4 HTTP semantikasi

| Belgi | Review savoli |
| --- | --- |
| `GET` holatni o'zgartiradi | Keshlanadi, prefetch qilinadi, retry qilinadi - xavfli |
| `POST` o'rniga `GET` bilan parametrlar | Maxfiy ma'lumot URL da va loglarda qoladi |
| `PUT` idempotent emas | Qayta yuborish dublikat yaratadi |
| `DELETE` ikki marta 404 beradi | Idempotentlik buzilgan - 204 bo'lishi kerak |
| Hamma xato 200 bilan `{"error": ...}` | Mijoz retry mantiqini qura olmaydi |
| 500 biznes rad etishi uchun | Monitoring shovqinga to'ladi |
| Yangi 4xx kod | Mijoz uni biladimi, hujjatlashtirilganmi |
| `Location` header yo'q `201` da | Mijoz yangi resurs manzilini bilmaydi |

```java
// Status kodlarining to'g'ri taqsimoti: review da shu jadval bo'yicha tekshiriladi.
// 400 - shakl xatosi (validatsiya)
// 401 - autentifikatsiya yo'q yoki yaroqsiz
// 403 - autentifikatsiya bor, huquq yo'q
// 404 - resurs yo'q (yoki ko'rish huquqi yo'q - enumeratsiyani oldini olish)
// 409 - konflikt (optimistik qulf, idempotentlik kaliti qayta ishlatilgan)
// 410 - resurs o'chirilgan (versiyalashda foydali)
// 422 - shakl to'g'ri, biznes qoidasi rad etdi
// 429 - rate limit
// 503 + Retry-After - vaqtincha ishlamaydi (circuit breaker ochiq)
```

### 20.5 Pagination va chegarasiz ro'yxatlar

```java
// Naqsh: chegarasiz ro'yxat.
@GetMapping("/orders")
public List<OrderResponse> all() { return orders.findAll()...; }   // 4 mln qator

// To'g'ri: majburiy chegara, maksimal qiymat, barqaror tartib.
@GetMapping("/orders")
public PageResponse<OrderResponse> list(
        @RequestParam(defaultValue = "0") @Min(0) int page,
        @RequestParam(defaultValue = "20") @Min(1) @Max(100) int size,
        @RequestParam(required = false) String cursor) {
    ...
}
```

Review da pagination uchun uch savol:

1. Maksimal `size` cheklanganmi. Cheklanmasa, `size=1000000` bilan ilovani yiqitish mumkin.
2. Tartib barqarormi. `ORDER BY created_at` da bir xil vaqtli qatorlar bo'lsa, sahifalar orasida qatorlar takrorlanadi yoki yo'qoladi. To'g'risi: `ORDER BY created_at DESC, id DESC` - yagona kalit bilan tugash.
3. Offset yoki kursor. Katta offset (`OFFSET 100000`) PostgreSQL da sekin: baza barcha oldingi qatorlarni o'qib tashlab yuboradi. Chuqur pagination uchun kursor (keyset) kerak.

```sql
-- Offset pagination: 100 000-sahifada sekin.
SELECT id, number FROM orders ORDER BY created_at DESC, id DESC
 LIMIT 20 OFFSET 100000;                  -- 100 020 qator o'qiladi

-- Keyset pagination: har doim tez, indeksdan foydalanadi.
SELECT id, number FROM orders
 WHERE (created_at, id) < (:lastCreatedAt, :lastId)   -- kursor
 ORDER BY created_at DESC, id DESC
 LIMIT 20;                                -- 20 qator o'qiladi
-- Indeks: CREATE INDEX ON orders (created_at DESC, id DESC);
```

### 20.6 Serializatsiya tuzoqlari

```java
// Tuzoq 1: lazy proxy serializatsiyasi.
// Entity qaytarilganda Jackson lazy kolleksiyaga tegadi va N+1 so'rov
// yuzaga keladi (yoki OSIV o'chirilgan bo'lsa istisno). Javob yozilayotganda
// xato chiqsa, HTTP status allaqachon 200 yuborilgan bo'ladi.

// Tuzoq 2: null va yo'q maydon farqi.
@JsonInclude(JsonInclude.Include.NON_NULL)    // null maydonlar chiqmaydi
public record OrderResponse(UUID id, String comment) { }
// Review savoli: mijoz "maydon yo'q" va "maydon null" ni ajrata oladimi?
// PATCH semantikasida bu farq muhim (JsonNullable yoki Optional kerak).

// Tuzoq 3: sana formati.
// Standart holatda Spring Boot `Instant` ni ISO-8601 satr sifatida yozadi,
// lekin WRITE_DATES_AS_TIMESTAMPS yoqilgan bo'lsa - raqam sifatida.
// Review da javob namunasini ko'rish kerak, kodga ishonmaslik.

// Tuzoq 4: BigDecimal serializatsiyasi.
// 1000.00 -> 1000.0 yoki 1000 bo'lib chiqishi mumkin, bu mijozda
// formatlash muammosi beradi. Pul uchun satr sifatida yuborish xavfsizroq.
@JsonSerialize(using = ToStringSerializer.class)
BigDecimal total;

// Tuzoq 5: polimorfik serializatsiya.
// @JsonTypeInfo bilan tur nomi JSON ga yoziladi - bu ichki klass nomlarini
// oshkor qiladi va deserializatsiyada xavf tug'diradi (31-bob).
```

### 20.7 Fayl yuklash

```java
// Review checklisti fayl yuklash uchun - har bir band alohida xavf.
@PostMapping(value = "/documents", consumes = MULTIPART_FORM_DATA_VALUE)
public DocumentResponse upload(@RequestPart("file") MultipartFile file) {
    // 1) Hajm chegarasi: konfiguratsiyada (quyida) va bu yerda ham.
    if (file.getSize() > MAX_SIZE) throw new FileTooLarge(MAX_SIZE);

    // 2) Tur tekshiruvi: Content-Type ga ishonmaslik - u mijozdan keladi.
    //    Haqiqiy turni baytlardan aniqlash (magic bytes).
    MediaType actual = fileTypeDetector.detect(file.getInputStream());
    if (!ALLOWED.contains(actual)) throw new UnsupportedFileType(actual);

    // 3) Nomni ishlatmaslik: path traversal va XSS manbasi.
    String storedName = UUID.randomUUID() + extensionFor(actual);   // o'z nomimiz

    // 4) Saqlash joyi: web root ichida emas, bajarilmaydigan joyda.
    storage.put(storedName, file.getInputStream());

    // 5) Antivirus yoki sandbox: ishonilmaydigan fayl uchun.
    return new DocumentResponse(storedName);
}
```

```properties
# Hajm chegaralari: ikki darajada.
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=12MB
server.tomcat.max-swallow-size=2MB        # rad etilgan so'rovni tez uzish
server.tomcat.max-http-form-post-size=2MB
```

### 20.8 So'rov chegaralari va rate limit

| Chegara | Nega kerak |
| --- | --- |
| So'rov tanasi hajmi | Xotira va parsing xarajati |
| Ro'yxat elementlari soni (`@Size(max=...)`) | 1 mln elementli massiv so'rovi |
| Ichma-ich JSON chuqurligi | Parser ni yiqitish |
| Rate limit (foydalanuvchi va IP bo'yicha) | Zo'ravonlik va tasodifiy retry bo'roni |
| So'rov timeout i | Sekin mijozlar thread ushlashi |
| Bir foydalanuvchiga parallel so'rov chegarasi | Resurs monopoliyasi |

```java
// Chuqur ichma-ich JSON va katta massivlardan himoya: Jackson chegaralari.
@Bean
Jackson2ObjectMapperBuilderCustomizer limits() {
    return builder -> builder.postConfigurer(mapper ->
        mapper.getFactory().setStreamReadConstraints(
            StreamReadConstraints.builder()
                .maxNestingDepth(50)
                .maxStringLength(1_000_000)
                .maxNumberLength(1_000)
                .build()));
}
```

### 20.9 Idempotentlik va qayta yuborish

Web qatlamida idempotentlik ikki joyda kerak: mijoz retry qilganda va foydalanuvchi ikki marta bosganda. Mexanizm 10.9 da ko'rsatilgan; bu yerda review savollari:

- Qaysi endpointlar idempotentlik kalitini talab qiladi (barcha pul va tashqi ta'sirli operatsiyalar).
- Kalit qayerdan keladi (mijoz yuboradi, server yaratmaydi).
- Takroriy so'rovga qanday javob qaytadi (bir xil natija, 409 emas, agar tana bir xil bo'lsa).
- Kalit qancha saqlanadi va kim tozalaydi.

### 20.10 CORS, header va kesh sozlamalari

```java
// Naqsh: hamma narsaga ruxsat.
@CrossOrigin(origins = "*")                   // credentials bilan birga - xavfli
// Review izohi: `*` va `allowCredentials=true` birga ishlamaydi (brauzer
// rad etadi), lekin `*` ning o'zi ham ichki API uchun ortiqcha ochiqlik.

// To'g'ri: aniq ro'yxat, konfiguratsiyadan.
@Bean
CorsConfigurationSource corsConfigurationSource(@Value("${app.cors.origins}") List<String> origins) {
    CorsConfiguration c = new CorsConfiguration();
    c.setAllowedOrigins(origins);                       // aniq domenlar
    c.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    c.setAllowedHeaders(List.of("Authorization", "Content-Type", "Idempotency-Key"));
    c.setAllowCredentials(true);
    c.setMaxAge(Duration.ofMinutes(30));
    UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/api/**", c);
    return src;
}
```

Keshlash header lari uchun review savoli: maxfiy ma'lumot qaytaradigan javobda `Cache-Control: no-store` bormi. Aks holda javob brauzer keshida yoki proksi keshida qoladi.

### 20.11 Review checklisti: web qatlami

| Savol | Nega |
| --- | --- |
| Entity kirish yoki chiqishda ishlatilmaydimi | Mass assignment, ma'lumot oqishi |
| `@Valid` bormi va ichki obyektlarga tarqaladimi | Tekshirilmagan ma'lumot |
| Foydalanuvchi identifikatori so'rovdan olinmaydimi | Boshqa nomidan harakat |
| Xato javobida ichki detal yo'qmi | Razvedka ma'lumoti |
| Status kodlari semantikaga mosmi | Mijoz mantiqi va monitoring |
| Ro'yxatlarda majburiy va maksimal `size` bormi | Resurs tugashi |
| Tartib barqarormi (yagona kalit bilan) | Pagination takrorlanishi |
| Pul va sana formati aniqmi | Mijoz tomonda xato |
| Fayl yuklashda tur, hajm, nom tekshirilganmi | Xavfsizlik |
| Yozuv operatsiyalarida idempotentlik bormi | Dublikat |
| CORS ro'yxati aniqmi | Ortiqcha ochiqlik |
| Maxfiy javoblarda `no-store` bormi | Kesh oqishi |

### 20.12 Amalda qo'llash

- [ ] Barcha controller metodlarini skanerlab, JPA entity kirish yoki chiqish turi sifatida ishlatilgan joylarni toping.
- [ ] `@RequestBody` parametrlarida `@Valid` yo'q joylarni va ichki obyektlarda `@Valid` tarqalmagan joylarni aniqlang.
- [ ] `server.error.include-*` sozlamalarini `never` qilib qo'ying va xato javoblarini `ProblemDetail` ga o'tkazing.
- [ ] Ro'yxat qaytaradigan endpointlarni sanab, `size` uchun maksimal chegara va barqaror tartib borligini tekshiring.
- [ ] Chuqur pagination ishlatiladigan joylarni keyset pagination ga o'tkazishni rejalashtiring.
- [ ] Pul maydonlarining JSON dagi ko'rinishini real javob namunasida tekshirib, satr sifatida yuborishni ko'rib chiqing.
- [ ] Fayl yuklash endpointlarida magic bytes bo'yicha tur tekshiruvi va o'z nomi bilan saqlash borligini tasdiqlang.
- [ ] Jackson `StreamReadConstraints` chegaralarini sozlang.
- [ ] `@CrossOrigin(origins = "*")` ishlatilgan joylarni aniq domen ro'yxatiga o'tkazing.
- [ ] Maxfiy ma'lumot qaytaradigan endpointlarda `Cache-Control: no-store` header ini qo'shing.

## 21. Konfiguratsiya, profil va feature flag review (Configuration)

Konfiguratsiya o'zgarishi diffda eng kichik va eng xavfli o'zgarishlar sinfi: bitta raqam incidentga olib keladi, va u kod review da ko'pincha e'tiborsiz qoladi. Sababi psixologik - `application.yml` dagi uch qator kod emasga o'xshaydi. Amalda esa prod incidentlarining sezilarli qismi aynan konfiguratsiya o'zgarishidan kelib chiqadi.

### 21.1 Konfiguratsiya o'zgarishi uchun qo'shimcha savollar

| Savol | Nega |
| --- | --- |
| Bu qiymat qaysi muhitlarda o'zgaradi | Faqat dev da sinalgan sozlama prodda boshqacha ishlaydi |
| Qiymat nimaga asoslangan | "Kattaroq yaxshiroq" qarori odatda xato |
| Qiymat chegarasi bormi | Pool, timeout, batch - hammasi resursga bog'liq |
| Standart qiymat nima edi | Framework standarti ko'pincha o'ylangan |
| Qayta ishga tushirish kerakmi | Dinamik o'zgaradigan sozlamalar boshqa xavf |
| Ikki sozlama bir-biriga bog'liqmi | Timeout va retry, pool va thread |
| O'lchov bormi | Sozlama ta'sirini qanday ko'ramiz |

```yaml
# Review da shu diff ko'rinsa, har qatorga savol bor.
spring:
  datasource:
    hikari:
      maximum-pool-size: 100        # oldin 20 edi
  jpa:
    properties:
      hibernate:
        jdbc:
          batch_size: 1000          # oldin 50 edi
resilience4j:
  timelimiter:
    instances:
      payment:
        timeout-duration: 60s       # oldin 3s edi
```

Review izohi har bir qiymatning tizim darajasidagi oqibatini ko'rsatadi:

```text
blocker: maximum-pool-size 20 -> 100.

PostgreSQL da har bir ulanish alohida backend protsess (taxminan 5-10 MB).
Hozir 6 pod ishlayapti: 6 x 100 = 600 ulanish. PostgreSQL max_connections
hozir 200 (tekshirdim: SHOW max_connections). Deploy dan keyin yangi
podlar ulanish ola olmaydi va butun ilova "FATAL: too many connections"
beradi.

Bundan tashqari pool kattaligi throughput ni oshirmaydi: 100 parallel
so'rov 16 yadroli bazada bir-birini kutadi va p99 yomonlashadi.

Agar pool kamligi muammo bo'lsa, avval sababni aniqlaymiz: hozir
hikaricp_connections_pending metrikasi nolga teng, ya'ni pool kutish
yo'q. Muammo boshqa joyda bo'lishi mumkin (uzoq tranzaksiyalar, 19.6).

question: timeout-duration 3s -> 60s. To'lov provayderining p99 javobi
hozir 800 ms. 60 sekundlik timeout bilan bitta sekin javob 60 sekund
thread va DB ulanishini ushlaydi. Nega 3 sekund yetarli bo'lmadi?
```

### 21.2 Timeout va retry juftligi

Konfiguratsiyadagi eng ko'p uchraydigan xato - timeout va retry ni alohida sozlash. Ularning ko'paytmasi tizimning haqiqiy kutish vaqtini belgilaydi.

```yaml
# Xavfli kombinatsiya: hisob qilinmagan.
client:
  connect-timeout: 10s
  read-timeout: 30s
retry:
  max-attempts: 5
  wait-duration: 2s
# Eng yomon holat: 5 x (10 + 30) + 4 x 2 = 208 sekund.
# Yuqoridagi qatlamda HTTP timeout 30 sekund bo'lsa, foydalanuvchi
# allaqachon ketgan, lekin thread 208 sekund ushlanadi.
```

Review qoidasi: har bir chaqiruv zanjirida umumiy byudjet yuqoridan pastga kamayib borishi kerak. Agar tashqi so'rov uchun umumiy byudjet 3 sekund bo'lsa, ichki chaqiruvlar yig'indisi shundan kichik bo'lishi shart.

| Qatlam | Byudjet |
| --- | --- |
| Foydalanuvchi so'rovi (ingress) | 10 s |
| Ilova so'rov timeout i | 8 s |
| Tashqi servis chaqiruvi (barcha urinishlar bilan) | 3 s |
| Bitta urinish | 1 s |
| DB so'rovi | 2 s |

### 21.3 Secret va maxfiy qiymatlar

```yaml
# Kodda yoki repoda secret - blocker, hech qanday istisnosiz.
spring:
  datasource:
    password: Prod_P@ssw0rd_2026        # blocker
  mail:
    password: ${MAIL_PASSWORD}          # to'g'ri: muhitdan
app:
  jwt:
    secret: ${JWT_SECRET}               # to'g'ri
```

Review da secret topilganda tartib: (1) merge ni to'xtatish, (2) secret ni rotatsiya qilish - uni repodan o'chirish yetarli emas, chunki git tarixida qoladi va fork larda ham bo'lishi mumkin, (3) tarixdan tozalash, (4) skanerlashni CI ga qo'yish.

```bash
# Secret skanerlashni review dan oldin avtomatlashtirish.
# 1) Pre-commit hook: lokalda to'xtatadi.
cat > .pre-commit-config.yaml <<'EOP'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks: [ { id: gitleaks } ]
EOP

# 2) CI da butun tarixni skanerlash (bir marta) va har PR da diffni.
gitleaks detect --source . --redact --verbose
gitleaks protect --staged --redact

# 3) Tarixda qolgan secret ni topish: faqat diffda emas.
git log -p --all -S 'BEGIN RSA PRIVATE KEY' --oneline | head
git log -p --all -G 'password\s*[:=]\s*["'"'"'][^"'"'"']{8,}' --oneline | head
```

### 21.4 Profil bo'yicha xulq farqi

```java
// Xavfli naqsh: biznes xulqi profilga bog'liq.
@Service
@Profile("!prod")
public class FakePaymentGateway implements PaymentGateway { ... }

@Service
@Profile("prod")
public class RealPaymentGateway implements PaymentGateway { ... }
// Oqibati: test va staging da hech qachon haqiqiy integratsiya sinalmaydi.
// Prodda birinchi marta ishga tushadi - eng yomon joyda.

// Yaxshiroq: muhit konfiguratsiya bilan farqlanadi, kod bir xil.
// Staging da provayderning sandbox URL i ishlatiladi:
//   payment.base-url=https://sandbox.provider.io
// Prodda:
//   payment.base-url=https://api.provider.io
// Soxta implementatsiya esa faqat test paketida qoladi (@TestConfiguration).
```

Review savoli har bir `@Profile` uchun: bu profil xulq farqini yaratadimi yoki faqat manzil farqini. Birinchi holat xavfli, chunki prodda sinalmagan yo'l paydo bo'ladi.

### 21.5 Tipli konfiguratsiya

```java
// Naqsh: @Value tarqalgan, tekshiruv yo'q.
@Value("${payment.timeout:3000}") private int timeoutMillis;   // har joyda
@Value("${payment.retries}") private int retries;              // yo'q bo'lsa - ishga tushmaydi

// To'g'ri: bitta tipli obyekt, validatsiya bilan.
@ConfigurationProperties(prefix = "payment")
@Validated
public record PaymentProperties(
        @NotNull URI baseUrl,
        @NotNull @DurationMin(millis = 100) @DurationMax(seconds = 10) Duration timeout,
        @Min(0) @Max(5) int retries,
        @NotBlank String merchantId) { }
// Foydasi: (1) noto'g'ri qiymat ishga tushishda aniqlanadi, prodda emas;
// (2) hamma sozlama bir joyda ko'rinadi; (3) IDE va metadata bilan
// avtoto'ldirish; (4) testda oson qurish.
```

### 21.6 Feature flag: vaqtinchalik bo'lishi kerak

```java
// Naqsh: flag qo'shildi, o'chirish rejasi yo'q.
if (featureFlags.isEnabled("new-pricing")) {
    return newPricing.calculate(order);
} else {
    return oldPricing.calculate(order);
}
```

Review talablari har bir yangi flag uchun:

1. Egasi va o'chirish sanasi. Flag abadiy qolmasligi kerak - har bir flag ikki kod yo'lini jonli saqlaydi va testlash yukini ikki baravar oshiradi.
2. Standart qiymat. Konfiguratsiya yetib kelmasa, qaysi yo'l ishlaydi.
3. Qamrov: butun foydalanuvchilar uchunmi yoki bir qismi. Qism bo'lsa, taqsimlash barqarormi (bir foydalanuvchi har so'rovda boshqa yo'lga tushmasligi kerak).
4. Ikki yo'l ham test bilan qoplanganmi.

```java
// Flag ni hujjatlashtirish: kodda, konfiguratsiyada emas.
public enum FeatureFlag {
    /** Egasi: pricing-team. O'chirish: 2026-12-01. Tiket: PRC-412. */
    NEW_PRICING("new-pricing", LocalDate.of(2026, 12, 1)),
    /** Egasi: payments. O'chirish: 2026-11-15. Tiket: PAY-88. */
    IDEMPOTENT_CAPTURE("idempotent-capture", LocalDate.of(2026, 11, 15));

    private final String key;
    private final LocalDate removeBy;
}

// Muddati o'tgan flag larni test bilan aniqlash: CI da gapiradi.
@Test
void noExpiredFeatureFlags() {
    List<FeatureFlag> expired = Arrays.stream(FeatureFlag.values())
        .filter(f -> f.removeBy().isBefore(LocalDate.now()))
        .toList();
    assertThat(expired)
        .as("muddati o'tgan flag lar olib tashlanishi kerak")
        .isEmpty();
}
```

### 21.7 Actuator va diagnostika endpointlari

```yaml
# Xavfli: hamma narsa ochiq.
management:
  endpoints:
    web:
      exposure:
        include: "*"              # env, configprops, heapdump, threaddump!
```

Review izohi: `/actuator/env` va `/actuator/configprops` konfiguratsiya qiymatlarini, jumladan secret larni ko'rsatadi (maskalash to'liq emas); `/actuator/heapdump` butun xotirani fayl sifatida beradi - unda tokenlar va foydalanuvchi ma'lumotlari bo'ladi; `/actuator/threaddump` ichki tuzilishni oshkor qiladi.

```yaml
# To'g'ri: minimal ro'yxat, alohida port, himoyalangan.
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      show-details: when-authorized      # detallar faqat avtorizatsiya bilan
      probes:
        enabled: true                    # /health/liveness va /readiness
  server:
    port: 9090                           # ichki port, tashqariga chiqarilmaydi
  metrics:
    tags:
      application: ${spring.application.name}
```

### 21.8 Muhitlar orasidagi farqni ko'rish

```bash
# Review da konfiguratsiya farqini aniq ko'rish: qaysi qiymat qaysi muhitda.
for env in dev staging prod; do
  echo "=== $env ==="
  diff <(grep -vE '^\s*#|^\s*$' src/main/resources/application.yml) \
       <(grep -vE '^\s*#|^\s*$' src/main/resources/application-$env.yml) \
       | grep '^>' | head -20
done

# Prodda haqiqatda qanday qiymat ishlayotganini tekshirish (secret siz).
curl -s localhost:9090/actuator/configprops | jq '.contexts.application.beans
  | to_entries[] | select(.key | test("Hikari|Payment|Resilience"))
  | {key, properties: .value.properties}'

# K8s da env dan kelgan qiymatlar kodnikini bosib ketadi - ularni ham ko'rish.
kubectl get deploy order-service -o jsonpath='{.spec.template.spec.containers[0].env}' | jq
```

Oxirgi buyruq muhim: `application.yml` dagi qiymat prodda ishlamasligi mumkin, chunki Kubernetes env o'zgaruvchisi uni bosib ketadi. Review da `yml` ni o'zgartirish yetarli emasligini aniqlash kerak.

### 21.9 Review checklisti: konfiguratsiya

| Savol | Nega |
| --- | --- |
| Yangi qiymat nimaga asoslangan | Taxminiy qiymat incident manbasi |
| Pool va thread chegaralari resursga sig'adimi | DB `max_connections`, xotira |
| Timeout va retry ko'paytmasi byudjetga sig'adimi | Kaskadli kechikish |
| Secret muhitdan olinadimi | Repoda secret bo'lmasligi |
| Profil xulq farqi yaratadimi | Prodda sinalmagan yo'l |
| `@Value` o'rniga tipli obyekt ishlatilganmi | Ishga tushishda tekshirish |
| Flag ning egasi va o'chirish sanasi bormi | Doimiy shoxlar |
| Actuator ro'yxati minimalmi | Ma'lumot oqishi |
| K8s env qiymatni bosib ketmaydimi | O'zgarish ta'sir qilmasligi |
| Sozlama ta'siri o'lchanadimi | Natijani ko'rish |

### 21.10 Amalda qo'llash

- [ ] Barcha `@Value` ishlatilgan joylarni `@ConfigurationProperties` + `@Validated` ga o'tkazish rejasini tuzing.
- [ ] Pool kattaligi x pod soni ni PostgreSQL `max_connections` bilan taqqoslab, zaxira qolganini tasdiqlang.
- [ ] Har bir tashqi integratsiya uchun timeout x urinishlar byudjetini hisoblab, yuqori qatlam timeout iga sig'ishini tekshiring.
- [ ] `gitleaks` ni pre-commit va CI ga qo'shib, butun tarixni bir marta skanerlang.
- [ ] `@Profile` ishlatilgan beanlarni ko'rib, xulq farqi yaratadiganlarni konfiguratsiya farqiga o'tkazing.
- [ ] Mavjud feature flag larni sanab, har biriga egasi va o'chirish sanasini qo'shing; muddati o'tganlarni aniqlaydigan test yozing.
- [ ] Actuator ro'yxatini `health,info,prometheus` ga qisqartirib, alohida portga chiqaring.
- [ ] Prodda haqiqatda ishlayotgan konfiguratsiyani `configprops` va K8s env orqali tekshirib, `application.yml` bilan farqini hujjatlashtiring.

## 22. Tashqi integratsiya review: timeout, retry, broker (Outbound Integration)

Har bir tashqi chaqiruv - tizimingizga kirgan begona nosozlik manbasi. Review ning vazifasi: shu nosozlik sizning ilovangizni o'ziga tortib ketmasligini tekshirish. Bitta sozlanmagan timeout butun ilovani to'xtatishi mumkin, va bu diffda bir qator ko'rinadi.

### 22.1 HTTP mijoz: timeout eng birinchi savol

```java
// Naqsh: timeout sozlanmagan mijoz.
@Bean
RestClient paymentClient() {
    return RestClient.create("https://api.provider.io");   // timeout yo'q!
}
// Standart holatda JDK HttpClient da ulanish timeout i cheksiz bo'lishi
// mumkin. Provayder TCP ulanishni qabul qilib, javob bermasa, thread
// abadiy kutadi. 200 thread li ilovada 200 sekin so'rov butun ilovani
// to'xtatadi - klassik kaskadli nosozlik.

// To'g'ri: har bir mijoz uchun aniq timeout va o'lchov.
@Bean
RestClient paymentClient(RestClient.Builder builder,
                         PaymentProperties props,
                         MeterRegistry registry) {
    ClientHttpRequestFactorySettings settings = ClientHttpRequestFactorySettings.DEFAULTS
        .withConnectTimeout(Duration.ofMillis(500))     // ulanish: tez xato
        .withReadTimeout(props.timeout());              // o'qish: byudjetdan

    return builder
        .baseUrl(props.baseUrl().toString())
        .requestFactory(ClientHttpRequestFactories.get(settings))
        .requestInterceptor(new MetricsInterceptor(registry, "payment"))
        .defaultStatusHandler(HttpStatusCode::isError, (req, res) -> {
            // Xato javobini domen istisnosiga aylantirish (7.6).
            throw PaymentGatewayException.from(res.getStatusCode(), res.getBody());
        })
        .build();
}
```

Review savollari har bir yangi HTTP mijoz uchun: ulanish timeout i, o'qish timeout i, umumiy byudjet, retry siyosati, circuit breaker, metrika, va xato javobining aylantirilishi.

### 22.2 Retry: qachon zarar keltiradi

```java
// Xato 1: hamma narsani retry qilish.
@Retryable(retryFor = Exception.class, maxAttempts = 5)      // juda keng
public PaymentResult charge(ChargeCommand cmd) { ... }
// Oqibati: karta rad etilgan (biznes javobi) ham besh marta takrorlanadi.
// Provayder tomonda bu "shubhali xulq" sifatida belgilanadi va hisob
// bloklanishi mumkin. Foydalanuvchiga besh SMS keladi.

// Xato 2: idempotent bo'lmagan operatsiyani retry qilish.
// POST /payments ni timeout dan keyin qayta yuborish: birinchi so'rov
// provayderga yetib borgan bo'lishi mumkin. Natija - ikki marta to'lov.
// Qoida: retry faqat idempotentlik kaliti bilan birga (10.9).

// To'g'ri: tor ro'yxat, jitter bilan backoff, idempotentlik kaliti.
@Retryable(
    retryFor = { PaymentGatewayUnavailable.class, SocketTimeoutException.class },
    noRetryFor = { CardDeclined.class, InsufficientFunds.class, InvalidCard.class },
    maxAttempts = 3,
    backoff = @Backoff(delay = 200, multiplier = 2, random = true))
public PaymentResult charge(ChargeCommand cmd) {
    return gateway.charge(cmd, cmd.idempotencyKey());   // kalit har urinishda bir xil
}
```

| Retry qilinadi | Retry qilinmaydi |
| --- | --- |
| Ulanish xatosi, timeout | 4xx (so'rov xatosi) |
| 502, 503, 504 | 401, 403 (huquq) |
| `Retry-After` bilan 429 | 422 (biznes rad etishi) |
| Deadlock, serializatsiya xatosi (DB) | Validatsiya xatosi |
| Optimistik qulf konflikti | Ma'lumot topilmadi |

### 22.3 Circuit breaker va bulkhead

Retry nosozlikni kuchaytiradi: tashqi servis yiqilganda uch barobar ko'p so'rov yuboriladi. Shu sababli retry yolg'iz emas, circuit breaker bilan birga keladi.

```yaml
resilience4j:
  circuitbreaker:
    instances:
      payment:
        sliding-window-type: COUNT_BASED
        sliding-window-size: 50
        minimum-number-of-calls: 20          # kam chaqiruvda qaror qabul qilmaslik
        failure-rate-threshold: 50           # 50% xato - ochiladi
        slow-call-duration-threshold: 1s
        slow-call-rate-threshold: 50         # sekin javoblar ham nosozlik
        wait-duration-in-open-state: 30s
        permitted-number-of-calls-in-half-open-state: 5
        record-exceptions:
          - com.acme.payment.PaymentGatewayUnavailable
        ignore-exceptions:
          - com.acme.payment.CardDeclined    # biznes javobi nosozlik emas
  bulkhead:
    instances:
      payment:
        max-concurrent-calls: 20             # bu integratsiya butun pool ni yemasin
        max-wait-duration: 100ms
  timelimiter:
    instances:
      payment:
        timeout-duration: 2s
        cancel-running-future: true
```

Review savollari: `ignore-exceptions` da biznes xatolari bormi (bo'lishi kerak), `minimum-number-of-calls` juda kichik emasmi (aks holda ikki xatodan keyin ochiladi), circuit ochilganda nima bo'ladi (fallback, navbat, yoki foydalanuvchiga xato), va bu holat o'lchanadimi.

```java
// Fallback - review ning asosiy diqqati: u nima qiladi?
@CircuitBreaker(name = "payment", fallbackMethod = "chargeFallback")
public PaymentResult charge(ChargeCommand cmd) { return gateway.charge(cmd); }

// Yomon fallback: muvaffaqiyat qaytaradi.
private PaymentResult chargeFallback(ChargeCommand cmd, Exception e) {
    return PaymentResult.approved();            // blocker: pul olinmagan!
}
// To'g'ri fallback: holatni rost ko'rsatadi va keyin davom etish yo'li beradi.
private PaymentResult chargeFallback(ChargeCommand cmd, Exception e) {
    meter.counter("payment.fallback").increment();
    outbox.enqueueRetry(cmd);                   // keyin qayta urinamiz
    return PaymentResult.pending(cmd.idempotencyKey());
}
```

### 22.4 WebClient va reaktiv kod aralashuvi

```java
// Naqsh: reaktiv mijoz blokirovka qilib ishlatilgan.
public Rate rate(String currency) {
    return webClient.get().uri("/rates/{c}", currency)
                    .retrieve().bodyToMono(Rate.class)
                    .block();                   // event loop threadida bo'lsa - deadlock
}
// Review izohi: `block()` ni reaktiv thread da chaqirish ilovani
// qotirishi mumkin. Agar reaktiv stek kerak bo'lmasa, RestClient
// ishlatish kerak - u sinxron va shu maqsad uchun.
// Qo'shimcha: block() da timeout yo'q - cheksiz kutish.
.block(Duration.ofSeconds(2));                  // minimal tuzatish
```

### 22.5 Kafka va xabar brokerlari review

```java
// Iste'molchi tomonidagi review savollari - har biri alohida xavf.
@KafkaListener(topics = "payments", groupId = "order-service")
public void onPayment(PaymentEvent event, Acknowledgment ack) {
    orders.applyPayment(event.orderId(), event.amount());
    ack.acknowledge();
}
```

| Savol | Nega muhim |
| --- | --- |
| Xabar ikki marta kelsa nima bo'ladi | Kafka "kamida bir marta" yetkazadi - idempotentlik majburiy |
| Xabar tartibi muhimmi | Tartib faqat bitta partition ichida kafolatlanadi; kalit to'g'ri tanlanganmi |
| Xato bo'lsa nima bo'ladi | Cheksiz qayta urinish (poison pill) yoki DLQ |
| `ack` qachon chaqiriladi | Ishdan oldin bo'lsa - xabar yo'qoladi |
| Tranzaksiya bilan munosabat | DB commit va `ack` atomik emas |
| Sxema o'zgarsa | Eski iste'molchi yangi xabarni o'qiy oladimi |
| Lag o'lchanadimi | Iste'molchi orqada qolsa, qanday bilamiz |
| Qayta ishlash qancha vaqt oladi | `max.poll.interval.ms` dan oshsa, guruhdan chiqariladi |

```yaml
# Review da tekshiriladigan minimal sozlamalar.
spring:
  kafka:
    consumer:
      enable-auto-commit: false            # qo'lda ack: ish bajarilgandan keyin
      isolation-level: read_committed
      max-poll-records: 50                 # bir martada ko'p olmaslik
      properties:
        max.poll.interval.ms: 300000       # ishlov vaqtidan katta bo'lsin
    producer:
      acks: all                            # yetkazish kafolati
      enable-idempotence: true             # dublikatsiz yozish
      properties:
        max.in.flight.requests.per.connection: 5
    listener:
      ack-mode: manual_immediate
```

```java
// DLQ va cheklangan qayta urinish: poison pill butun iste'molchini to'xtatmasin.
@Bean
DefaultErrorHandler errorHandler(KafkaTemplate<String, Object> template) {
    // 3 urinishdan keyin xabarni .DLT topikiga yuborish.
    DeadLetterPublishingRecoverer recoverer = new DeadLetterPublishingRecoverer(template);
    ExponentialBackOffWithMaxRetries backoff = new ExponentialBackOffWithMaxRetries(3);
    backoff.setInitialInterval(500);
    backoff.setMultiplier(2.0);
    DefaultErrorHandler handler = new DefaultErrorHandler(recoverer, backoff);
    // Deserializatsiya xatosi - qayta urinish ma'nosiz, darhol DLQ ga.
    handler.addNotRetryableExceptions(DeserializationException.class,
                                      MessageConversionException.class);
    return handler;
}
// Review savoli: DLQ ni kim o'qiydi va u haqida alert bormi? O'qilmaydigan
// DLQ - ma'lumotni jim yo'qotishning chiroyli shakli.
```

### 22.6 Xabar sxemasi va moslik

```java
// Review talabi: event sxemasi o'zgarishi orqaga mos bo'lishi kerak.
// Mos o'zgarishlar: ixtiyoriy maydon qo'shish, standart qiymat bilan.
public record OrderPlaced(
        UUID orderId,
        BigDecimal total,
        String currency,
        @Nullable String promoCode) { }          // yangi, ixtiyoriy - mos

// Mos bo'lmagan o'zgarishlar (37-bob ro'yxatiga qarang):
// - maydon nomini o'zgartirish
// - maydon turini o'zgartirish
// - majburiy maydon qo'shish
// - maydon olib tashlash
// - enum qiymatini olib tashlash

// Review savoli: iste'molchilar kim? Ular yangilanmasdan eski xabarni
// o'qiy oladimi, va yangi xabarni ham? Schema registry bormi?
```

### 22.7 Tashqi ma'lumotga ishonmaslik

```java
// Naqsh: tashqi javob tekshirilmasdan domenga kiradi.
PaymentResponse r = client.get().retrieve().body(PaymentResponse.class);
order.applyPayment(r.amount(), r.currency());    // amount null yoki manfiy bo'lishi mumkin

// To'g'ri: tashqi javob ham ishonilmaydigan kirish - adapter ichida tekshiriladi.
PaymentResponse r = client.get().retrieve().body(PaymentResponse.class);
if (r == null || r.amount() == null || r.amount().signum() < 0) {
    throw new InvalidGatewayResponse("amount: " + (r == null ? "null" : r.amount()));
}
Money amount = new Money(r.amount(), Currency.getInstance(r.currency()));
order.applyPayment(amount);
```

Review da bu naqsh ko'pincha e'tibordan chetda qoladi, chunki "o'z provayderimiz" ishonchli deb hisoblanadi. Amalda esa tashqi API versiyasini o'zgartirishi, xato holatda `null` qaytarishi yoki boshqa valyutada javob berishi mumkin.

### 22.8 Review checklisti: tashqi integratsiya

| Savol | Nega |
| --- | --- |
| Ulanish va o'qish timeout i bormi | Thread va pool to'lishi |
| Retry ro'yxati tor va idempotentlik bormi | Dublikat va retry bo'roni |
| Backoff da jitter bormi | Sinxron urinishlar to'lqini |
| Circuit breaker va bulkhead bormi | Kaskadli nosozlik |
| Fallback rost holatni qaytaradimi | Yolg'on muvaffaqiyat |
| Tashqi javob tekshiriladimi | Buzilgan ma'lumot domenda |
| Vendor istisnolari domen istisnolariga aylanadimi | Oqib chiqadigan abstraksiya |
| Metrika va trace bormi | Ko'r integratsiya |
| Kafka da idempotentlik va DLQ bormi | Yo'qolgan yoki takrorlangan xabar |
| `ack` ish bajarilgandan keyinmi | Yo'qolgan xabar |
| Sxema o'zgarishi orqaga mosmi | Iste'molchilar sinishi |
| Secret va kalitlar muhitdanmi | Oshkor qilish |

### 22.9 Amalda qo'llash

- [ ] Barcha HTTP mijoz bean larini sanab, ulanish va o'qish timeout i sozlanmaganlarini aniqlang va tuzating.
- [ ] Har bir integratsiya uchun umumiy byudjet jadvalini tuzing (urinishlar x timeout) va yuqori qatlam chegarasiga sig'ishini tasdiqlang.
- [ ] `@Retryable` va Resilience4j `retry-exceptions` ro'yxatlarida biznes istisnolari yo'qligini tekshiring.
- [ ] Barcha retry siyosatlarida jitter (`random = true` yoki `enable-randomized-wait`) yoqilganini tasdiqlang.
- [ ] Fallback metodlarini ko'rib, yolg'on muvaffaqiyat qaytaradiganlarini tuzating.
- [ ] Vendor istisnolarini domen istisnolariga aylantiradigan adapter qatlamini qo'shing.
- [ ] Kafka iste'molchilarida `enable-auto-commit: false`, DLQ va deserializatsiya xatosi uchun `addNotRetryableExceptions` borligini tekshiring.
- [ ] DLQ uchun alert va uni o'qish jarayonini belgilang.
- [ ] Consumer lag va circuit breaker holati uchun dashboard paneli va alert qo'shing.

# V. PostgreSQL va ma'lumot qatlami review

## 23. JPA va Hibernate review (JPA and Hibernate)

JPA ning xavfi shundaki, u yozgan SQL ni ko'rsatmaydi. Diffda bitta annotatsiya o'zgaradi, prodda esa so'rovlar soni yuzga ko'payadi. Shu sababli JPA kodini review qilish bitta malakani talab qiladi: annotatsiyadan SQL ni tiklab ko'rish. Hibernate ichki mexanikasi (dirty checking, flush tartibi, ikkinchi daraja kesh) `java-spring-architect-mindset.md` da; bu yerda diffdan so'rovlar sonini baholash.

### 23.1 N+1: diffdan ko'rish

N+1 ning belgisi diffda uchta shaklda ko'rinadi: yangi lazy maydonga sikl ichida tegish, DTO mapping ichida bog'liq obyektni o'qish, va `toString`/serializatsiya orqali tasodifiy yuklash.

```java
// Belgi 1: sikl ichida lazy kolleksiyaga tegish.
List<Order> orders = repository.findByStatus(OPEN);        // 1 so'rov
for (Order o : orders) {
    total = total.add(o.getLines().stream()                // har buyurtmaga 1 so'rov
                       .map(OrderLine::getAmount).reduce(ZERO, Money::plus));
}
// 500 buyurtma = 501 so'rov. Har biri 1 ms bo'lsa ham, 500 ms.

// Yechim 1: JOIN FETCH - bitta so'rov.
@Query("select distinct o from Order o join fetch o.lines where o.status = :s")
List<Order> findByStatusWithLines(@Param("s") OrderStatus status);
// Diqqat: JOIN FETCH va pagination birga ishlamaydi - Hibernate hamma
// qatorni xotiraga olib, keyin sahifalaydi (HHH000104 ogohlantirishi).

// Yechim 2: @EntityGraph - deklarativ, pagination bilan ham ishlaydi
// (lekin Hibernate ikkinchi so'rov bilan to'ldiradi).
@EntityGraph(attributePaths = { "lines", "customer" })
List<Order> findByStatus(OrderStatus status);

// Yechim 3 (eng tezi): agregatni SQL da hisoblash, entity yuklamaslik.
@Query("""
    select new com.acme.order.OrderTotal(o.id, sum(l.amount))
      from Order o join o.lines l
     where o.status = :s
     group by o.id
    """)
List<OrderTotal> totalsByStatus(@Param("s") OrderStatus status);
```

```yaml
# N+1 ni test va lokal ishga tushirishda ko'rinadigan qilish.
spring:
  jpa:
    properties:
      hibernate:
        generate_statistics: true           # so'rovlar soni logga chiqadi
    open-in-view: false                     # lazy xatolari darhol ko'rinadi
logging:
  level:
    org.hibernate.SQL: debug
    org.hibernate.orm.jdbc.bind: trace      # parametr qiymatlari
```

### 23.2 So'rovlar sonini test bilan qulflash

Review izohida "N+1 bor" degan gapni dalil bilan quvvatlash va kelajakda regressiyani oldini olish usuli - so'rovlar sonini test bilan belgilash.

```java
// So'rov sonini tekshiradigan test: review ning eng kuchli argumenti.
@SpringBootTest
@AutoConfigureTestDatabase(replace = NONE)
class OrderQueryCountTest {

    @Autowired OrderService service;
    @Autowired EntityManagerFactory emf;

    @Test
    void listingOrdersUsesConstantQueryCount() {
        Statistics stats = emf.unwrap(SessionFactory.class).getStatistics();
        stats.clear();

        service.openOrdersWithTotals();      // 500 buyurtma bor

        // Niyat: so'rovlar soni ma'lumot hajmiga bog'liq bo'lmasin.
        assertThat(stats.getPrepareStatementCount())
            .as("so'rovlar soni")
            .isLessThanOrEqualTo(3);
    }
}
// Alternativa: datasource-proxy yoki QuickPerf kutubxonasi
// (@ExpectSelect(3) annotatsiyasi bilan).
```

### 23.3 Fetch strategiyasi

| Annotatsiya | Standart fetch | Review talabi |
| --- | --- | --- |
| `@ManyToOne` | EAGER | Deyarli har doim `LAZY` qilish kerak |
| `@OneToOne` | EAGER | `LAZY` + `optional = false` |
| `@OneToMany` | LAZY | To'g'ri standart, `JOIN FETCH` bilan ishlatish |
| `@ManyToMany` | LAZY | Ko'pincha alohida entity ga ajratish kerak |
| `@ElementCollection` | LAZY | Kichik to'plamlar uchun |

```java
// Eng ko'p uchraydigan muammo: @ManyToOne standart EAGER.
@Entity
public class OrderLine {
    @ManyToOne                               // EAGER: har OrderLine bilan Product yuklanadi
    private Product product;

    @ManyToOne(fetch = FetchType.LAZY)       // to'g'ri
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;
}
// Oqibati: 1000 qatorli buyurtma yuklanganda 1000 Product ham yuklanadi,
// ularning har birida yana EAGER bog'liqlik bo'lsa - zanjir bo'ylab
// butun baza xotiraga tortiladi.

// Diqqat: LAZY @ManyToOne bilan `line.getProduct().getId()` ham so'rov
// yuboradi (agar proxy bo'lmasa). ID kerak bo'lsa, uni alohida ustun
// sifatida saqlash foydali:
@Column(name = "product_id", insertable = false, updatable = false)
private UUID productId;                      // so'rovsiz ID
```

### 23.4 Cascade va orphan removal

```java
// Xavfli: cascade = ALL mijozdan buyurtmaga.
@OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
private List<Order> orders;
// Oqibati: customers.delete(customer) butun buyurtma tarixini o'chiradi.
// Buxgalteriya va audit nuqtai nazaridan bu deyarli har doim xato.
// Bundan tashqari kolleksiyadan element olib tashlash uni DB dan o'chiradi -
// bu kutilmagan xulq bo'lishi mumkin.

// Review savollari har bir cascade uchun:
// 1) Ota obyekt o'chirilganda bola haqiqatan o'chirilishi kerakmi?
// 2) Yoki bu agregat chegarasi xato qo'yilganmi (13.3)?
// 3) `ON DELETE` qoidasi DB da ham mosmi (FK)?

// Mos shakl: haqiqiy agregat ichidagi qatorlar uchun.
@Entity
public class Order {
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderLine> lines;           // qatorlar buyurtmasiz mavjud emas
}
```

### 23.5 Dirty checking va ortiqcha UPDATE

```java
// Naqsh: o'qish metodida tasodifiy yozuv.
@Transactional                               // readOnly yo'q!
public List<OrderView> list() {
    List<Order> orders = repository.findAll();
    orders.forEach(o -> o.setLastViewedAt(now()));    // har o'qishda UPDATE!
    return orders.stream().map(OrderView::from).toList();
}
// Oqibati: ro'yxatni ochish 500 UPDATE yuboradi, replikatsiya lag o'sadi,
// va `updated_at` triggerlari ishga tushadi.

// Naqsh: entity ni o'zgartirmasdan ham UPDATE chiqishi.
// Sabab: mutable tur (Date, kolleksiya) yoki noto'g'ri equals/hashCode,
// yoki AttributeConverter har flush da boshqa natija berishi.
// Tekshirish: hibernate.generate_statistics va EntityUpdateCount.

// Review qoidasi: o'qish metodlari @Transactional(readOnly = true) bilan -
// Hibernate dirty checking qilmaydi va tasodifiy UPDATE chiqmaydi.
```

### 23.6 Batch yozuv

```java
// Naqsh: 10 000 qatorni bitta-bitta saqlash.
for (Row row : rows) { repository.save(toEntity(row)); }     // 10 000 INSERT

// To'g'ri: batch yozuv sozlangan va tartib buzilmagan.
```

```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc.batch_size: 50
        order_inserts: true              # bir xil jadval INSERT lari guruhlanadi
        order_updates: true
        batch_versioned_data: true       # @Version bilan ham batch ishlaydi
  datasource:
    hikari:
      data-source-properties:
        reWriteBatchedInserts: true      # PostgreSQL JDBC: multi-row INSERT
```

```java
// Diqqat: batch IDENTITY generatsiyasi bilan ISHLAMAYDI - Hibernate har
// INSERT dan keyin ID ni olishi kerak.
@Id @GeneratedValue(strategy = GenerationType.IDENTITY)      // batch o'chadi
private Long id;

// Batch ishlashi uchun: SEQUENCE + allocationSize yoki UUID.
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "order_seq")
@SequenceGenerator(name = "order_seq", sequenceName = "order_seq", allocationSize = 50)
private Long id;
// Review izohi: allocationSize DB sequence ning INCREMENT BY bilan mos
// bo'lishi shart, aks holda ID konfliktlari bo'ladi.

// Katta import uchun esa Hibernate umuman kerak emas:
jdbcTemplate.batchUpdate(
    "INSERT INTO import_row (id, payload) VALUES (?, ?::jsonb)",
    rows, 500, (ps, row) -> { ps.setObject(1, row.id()); ps.setString(2, row.json()); });
// Yoki eng tez yo'l - PostgreSQL COPY (millionlab qator uchun).
```

### 23.7 Projection: entity kerak bo'lmaganda

```java
// Naqsh: ro'yxat uchun to'liq entity yuklanadi.
List<Order> orders = repository.findByStatus(OPEN);   // 40 ustun, lazy proxy lar
return orders.stream().map(o -> new OrderRow(o.getId(), o.getNumber())).toList();

// To'g'ri: faqat kerakli ustunlar o'qiladi.
// Variant 1: interfeys projection (Spring Data o'zi amalga oshiradi).
public interface OrderRow {
    UUID getId();
    String getNumber();
    BigDecimal getTotal();
}
List<OrderRow> findByStatus(OrderStatus status);

// Variant 2: record + konstruktor ifodasi (aniqroq va tipli).
@Query("select new com.acme.order.OrderRow(o.id, o.number, o.total) from Order o where o.status = :s")
List<OrderRow> rowsByStatus(@Param("s") OrderStatus status);

// Variant 3: murakkab hisob uchun - JdbcClient, entity umuman yo'q.
List<OrderRow> rows = jdbcClient.sql("""
        SELECT o.id, o.number, o.total,
               count(l.id) AS line_count
          FROM orders o LEFT JOIN order_line l ON l.order_id = o.id
         WHERE o.status = :status
         GROUP BY o.id, o.number, o.total
         ORDER BY o.created_at DESC
         LIMIT 100
        """)
    .param("status", status.name())
    .query(OrderRow.class)
    .list();
```

Review qoidasi: ma'lumot o'zgartirilmasa, entity kerak emas. Projection kamroq ustun o'qiydi, dirty checking qilmaydi, birinchi daraja keshni to'ldirmaydi va lazy xatolaridan xoli.

### 23.8 Hibernate xulqini o'zgartiradigan nozik annotatsiyalar

| Annotatsiya | Ta'siri | Review diqqati |
| --- | --- | --- |
| `@DynamicUpdate` | Faqat o'zgargan ustunlar yangilanadi | Har flush da SQL qayta quriladi (narx); keng jadvalda foydali |
| `@Immutable` | O'zgarishlar e'tiborsiz qoldiriladi | Jim ishlamaydigan `set` lar |
| `@NaturalId` | Tabiiy kalit bo'yicha kesh | Kalit o'zgarmasligi kafolatlanganmi |
| `@BatchSize` | Lazy yuklashni guruhlash | N+1 ni N/batch ga kamaytiradi |
| `@Formula` | Hisoblangan maydon SQL da | Har o'qishda hisob, indekssiz |
| `@Where` | Global filtr | Jim yashirin shart - juda xavfli |
| `@SQLDelete` | Yumshoq o'chirish | O'chirilgan qatorlar hamma joyda filtrlanadimi |
| `@Cacheable` (2-daraja) | Klaster bo'ylab kesh | Invalidatsiya, klasterda mos kelish |
| `@LazyCollection(EXTRA)` | `size()` uchun alohida so'rov | Ko'pincha noto'g'ri qo'llanadi |
| `@OrderBy` vs `@OrderColumn` | SQL tartibi vs saqlangan indeks | `@OrderColumn` qo'shimcha UPDATE lar beradi |

```java
// @Where - eng xavfli: shart hamma so'rovga jim qo'shiladi.
@Entity
@Where(clause = "deleted = false")
public class Customer { }
// Oqibati: (1) o'chirilgan mijozni hech qanday so'rov bilan ola olmaysiz
// (hatto admin paneldan ham); (2) native so'rovlarga bu shart qo'shilmaydi,
// shuning uchun JPQL va SQL natijalari farq qiladi; (3) JOIN larda
// kutilmagan natija. Review tavsiyasi: shartni aniq so'rovlarda yozish.
```

### 23.9 Entity hayot sikli va detached holat

```java
// Naqsh: detached entity ni saqlash - jim ustun yo'qotilishi.
public void update(OrderDto dto) {
    Order order = new Order();               // detached, hamma maydon null
    order.setId(dto.id());
    order.setComment(dto.comment());
    repository.save(order);                  // merge: boshqa maydonlar null bo'ladi!
}
// Oqibati: `total`, `status`, `created_at` null ga yoziladi yoki NOT NULL
// xatosi chiqadi. Bu ma'lumot yo'qotishning klassik yo'li.

// To'g'ri: yuklash, o'zgartirish, tranzaksiya commit i bilan saqlash.
@Transactional
public void update(OrderDto dto) {
    Order order = repository.findById(dto.id()).orElseThrow(OrderNotFound::new);
    order.changeComment(dto.comment());      // domen metodi
    // save() chaqirish shart emas: boshqarilayotgan entity avtomatik flush bo'ladi.
}
```

### 23.10 Review checklisti: JPA

| Savol | Nega |
| --- | --- |
| Yangi lazy maydonga sikl ichida tegilmaydimi | N+1 |
| `@ManyToOne` LAZY qilinganmi | Yashirin EAGER zanjiri |
| `JOIN FETCH` pagination bilan ishlatilmaganmi | Xotirada sahifalash |
| O'qish metodlari `readOnly` mi | Tasodifiy UPDATE |
| `cascade = ALL` oqibati baholanganmi | Ma'lumot yo'qolishi |
| Batch sozlangan va IDENTITY ishlatilmaganmi | Sekin import |
| Ro'yxat uchun projection ishlatilganmi | Ortiqcha ustun va xotira |
| Detached entity `save` qilinmaydimi | Maydon yo'qolishi |
| `@Where`, `@SQLDelete` kabi global filtrlar bormi | Jim yashirin shart |
| Katta natijalar oqim yoki bo'lak bilan o'qiladimi | OOM |
| `@Version` kerakli joyda bormi | Yo'qolgan yangilanish |
| So'rov soni test bilan qulflangangmi | Regressiya |

### 23.11 Amalda qo'llash

- [ ] `hibernate.generate_statistics` ni test profilida yoqib, asosiy endpointlar uchun so'rov sonini o'lchang.
- [ ] Eng muhim uchta ro'yxat endpointi uchun so'rov sonini qulflaydigan test yozing.
- [ ] Barcha `@ManyToOne` va `@OneToOne` larni toping va `fetch = LAZY` qo'yilganini tasdiqlang.
- [ ] `spring.jpa.open-in-view=false` qilib, chiqadigan `LazyInitializationException` larni DTO yoki `JOIN FETCH` bilan tuzating.
- [ ] `cascade = ALL` va `orphanRemoval = true` ishlatilgan joylarni ko'rib, agregat chegarasini qayta baholang.
- [ ] Batch sozlamalarini (`batch_size`, `order_inserts`, `reWriteBatchedInserts`) qo'shing va `IDENTITY` ishlatadigan entity larni sequence ga o'tkazishni rejalashtiring.
- [ ] Ro'yxat qaytaradigan so'rovlarni projection ga o'tkazib, o'qilayotgan ustun sonini kamaytiring.
- [ ] `@Where` va `@SQLDelete` ishlatilgan joylarni aniq so'rov shartlariga o'tkazishni ko'rib chiqing.
- [ ] `new Entity()` + `setId()` + `save()` naqshini grep bilan topib, barchasini tuzating.

## 24. SQL, so'rov rejasi va indeks review (SQL, Plans and Indexes)

Review stolida so'rov rejasini ko'rish imkoni bo'lmaydi, lekin uni taxmin qilish imkoni bor. Bu bob shu malakani beradi: SQL ga qarab PostgreSQL nima qilishini aytish, va qachon `EXPLAIN` so'rash kerakligini bilish. PostgreSQL planner mexanikasi `java-spring-architect-mindset.md` da.

### 24.1 Indeks ishlatilmaydigan naqshlar

Bu ro'yxat review ning eng tez qaytim beradigan qismi: har bir naqsh indeksni o'chiradi va seq scan keltiradi.

| Naqsh | Nega indeks ishlamaydi | To'g'ri shakl |
| --- | --- | --- |
| `WHERE date(created_at) = ?` | Ustun funksiya ichida | Oraliq: `>= ? AND < ?` |
| `WHERE lower(email) = ?` | Funksiya | Ifoda indeksi: `ON t (lower(email))` |
| `WHERE amount::text LIKE '1%'` | Tur konversiyasi | Raqamli taqqoslash |
| `WHERE name LIKE '%abc%'` | Boshida wildcard | Trigram indeks (`pg_trgm`) yoki FTS |
| `WHERE status != 'CLOSED'` | Selektivlik past | Partial indeks |
| `WHERE col + 0 = ?` | Ustun ifodada | Shartni teskari yozish |
| `WHERE id IN (juda katta ro'yxat)` | Planner rejani o'zgartiradi | `= ANY(?)` massiv yoki vaqtinchalik jadval |
| `ORDER BY` indeks tartibiga mos emas | Sort kerak | Indeksni tartibga moslash |
| `WHERE a = ? OR b = ?` | Ikki indeksni birlashtirish qiyin | `UNION ALL` yoki ikki so'rov |
| Tur mos kelmasligi (`uuid` va `text`) | Implicit cast | Turlarni moslash |
| `WHERE nullable_col = ?` NULL bilan | `= NULL` hech narsa topmaydi | `IS NULL` |
| Timezone konversiyasi ustunda | Funksiya | Parametrni konvertatsiya qilish |

```sql
-- Review da bu farqni ko'rsatish: ikkisi bir xil natija, boshqa reja.
-- Yomon: har qator uchun date() hisoblanadi.
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM orders WHERE date(created_at) = '2026-10-01';
-- Seq Scan on orders (cost=... rows=...) actual time=1250ms

-- Yaxshi: indeks oralig'i.
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM orders
 WHERE created_at >= '2026-10-01' AND created_at < '2026-10-02';
-- Index Only Scan using orders_created_at_idx ... actual time=3ms
```

### 24.2 Yangi indeks qo'shilganda review savollari

```sql
-- Diffda yangi indeks. Review da yetti savol.
CREATE INDEX orders_customer_status_idx ON orders (customer_id, status);
```

1. Ustunlar tartibi to'g'rimi. Tenglik shartidagi ustunlar oldinda, oraliq shartidagi keyin. `WHERE customer_id = ? AND created_at > ?` uchun `(customer_id, created_at)`, teskarisi emas.
2. Bu indeks mavjud indeksning prefiksi emasmi. `(customer_id)` indeksi bo'lsa, `(customer_id, status)` uni o'z ichiga oladi - eskisini olib tashlash kerak.
3. Selektivlik qanday. `status` ustunida 3 qiymat bo'lsa va 95% `CLOSED` bo'lsa, planner bu indeksni ishlatmaydi. Partial indeks kerak.
4. Yozuv narxi hisobga olinganmi. Har indeks `INSERT`/`UPDATE` ni sekinlashtiradi va joy egallaydi.
5. `CONCURRENTLY` ishlatilganmi. Katta jadvalda `CREATE INDEX` yozuvni bloklaydi.
6. Hajmi qancha bo'ladi. 40 mln qatorli jadvalda indeks gigabaytlarga chiqadi.
7. Qaysi so'rov buni ishlatadi va reja tasdiqlanganmi.

```sql
-- Partial indeks: kichik va samarali.
CREATE INDEX CONCURRENTLY orders_open_idx ON orders (customer_id, created_at DESC)
    WHERE status IN ('NEW', 'PAID');
-- 40 mln qatorli jadvalda ochiq buyurtmalar 50 ming bo'lsa, indeks
-- 1000 baravar kichik va keshda to'liq turadi.

-- Covering indeks: Index Only Scan uchun (jadvalga tegmaydi).
CREATE INDEX CONCURRENTLY orders_lookup_idx ON orders (number) INCLUDE (status, total);

-- Mavjud indekslarni va ularning ishlatilishini ko'rish: review dalili.
SELECT indexrelname, idx_scan, idx_tup_read,
       pg_size_pretty(pg_relation_size(indexrelid)) AS hajm
  FROM pg_stat_user_indexes
 WHERE relname = 'orders'
 ORDER BY idx_scan;
-- idx_scan = 0 bo'lgan indekslar - o'lik yuk, olib tashlanishi kerak.

-- Dublikat va bir-birini qoplaydigan indekslarni topish.
SELECT a.indexrelid::regclass AS ortiqcha, b.indexrelid::regclass AS qoplaydi
  FROM pg_index a JOIN pg_index b
    ON a.indrelid = b.indrelid AND a.indexrelid <> b.indexrelid
   AND array_to_string(a.indkey, ' ') LIKE array_to_string(b.indkey, ' ') || '%'
 WHERE NOT a.indisprimary;
```

### 24.3 So'rov rejasini o'qish: review uchun minimal bilim

| Rejada ko'rilgan | Ma'nosi | Qachon muammo |
| --- | --- | --- |
| `Seq Scan` | Butun jadval o'qiladi | Katta jadvalda filtr bilan |
| `Index Scan` | Indeks + jadval | Normal |
| `Index Only Scan` | Faqat indeks | Eng yaxshi |
| `Bitmap Heap Scan` | Ko'p qator, indeks orqali | Odatda normal |
| `Nested Loop` | Har qator uchun ichki so'rov | Tashqi qatorlar ko'p bo'lsa |
| `Hash Join` | Hash jadval quriladi | `work_mem` yetmasa diskka tushadi |
| `Merge Join` | Ikki tartiblangan oqim | Normal |
| `Sort` + `Disk` | Saralash diskka tushgan | `work_mem` oshirish yoki indeks |
| `rows=1000` vs `actual rows=500000` | Statistika xato | `ANALYZE` kerak yoki shart murakkab |
| `Filter: ... Rows Removed by Filter: 2000000` | Ortiqcha qator o'qilgan | Indeks yo'q |
| `Buffers: read=50000` | Diskdan o'qish | Kesh yetmaydi |

```sql
-- Review da so'rash kerak bo'lgan to'liq shakl: BUFFERS va ANALYZE bilan.
EXPLAIN (ANALYZE, BUFFERS, VERBOSE, SETTINGS)
SELECT ...;
-- SETTINGS - standart bo'lmagan planner sozlamalarini ko'rsatadi.
-- Review izohi: "EXPLAIN (ANALYZE, BUFFERS) natijasini qo'shsangiz,
-- rejani birga ko'ramiz" - bu eng foydali so'rov.
```

### 24.4 JOIN va agregat so'rovlari

```sql
-- Naqsh: JOIN natijasida qatorlar ko'payib, SUM noto'g'ri bo'lishi.
SELECT o.id, sum(l.amount) AS total, sum(p.amount) AS paid
  FROM orders o
  JOIN order_line l ON l.order_id = o.id        -- 3 qator
  JOIN payment p ON p.order_id = o.id           -- 2 qator
 GROUP BY o.id;
-- Natija: 6 qator (3 x 2), total 2 baravar, paid 3 baravar katta!
-- Bu eng ko'p uchraydigan SQL xatosi va test bilan tutilmasligi mumkin
-- (bitta to'lov va bitta qator bo'lsa, natija to'g'ri chiqadi).

-- To'g'ri: alohida agregatlar yoki lateral.
SELECT o.id,
       (SELECT sum(amount) FROM order_line WHERE order_id = o.id) AS total,
       (SELECT sum(amount) FROM payment    WHERE order_id = o.id) AS paid
  FROM orders o;
-- Yoki LATERAL bilan (ko'p ustun kerak bo'lsa):
SELECT o.id, l.total, p.paid
  FROM orders o
  LEFT JOIN LATERAL (SELECT sum(amount) AS total FROM order_line WHERE order_id = o.id) l ON true
  LEFT JOIN LATERAL (SELECT sum(amount) AS paid  FROM payment    WHERE order_id = o.id) p ON true;
```

```sql
-- Naqsh: LEFT JOIN WHERE bilan INNER JOIN ga aylanadi.
SELECT o.* FROM orders o
  LEFT JOIN payment p ON p.order_id = o.id
 WHERE p.status = 'OK';          -- to'lovsiz buyurtmalar tushib qoladi!
-- To'g'ri: shart JOIN ichida.
 LEFT JOIN payment p ON p.order_id = o.id AND p.status = 'OK';

-- Naqsh: NOT IN va NULL.
SELECT * FROM orders WHERE customer_id NOT IN (SELECT id FROM blocked_customer);
-- Agar blocked_customer.id da bitta NULL bo'lsa - natija BO'SH bo'ladi.
-- To'g'ri: NOT EXISTS (NULL ga chidamli va odatda tezroq).
SELECT * FROM orders o WHERE NOT EXISTS (
    SELECT 1 FROM blocked_customer b WHERE b.id = o.customer_id);
```

### 24.5 Dinamik SQL review

```java
// Naqsh: shartlar satr qo'shish bilan quriladi.
StringBuilder sql = new StringBuilder("SELECT * FROM orders WHERE 1=1");
if (status != null) sql.append(" AND status = '").append(status).append("'");   // injection
if (from != null)   sql.append(" AND created_at >= '").append(from).append("'");
if (sortBy != null) sql.append(" ORDER BY ").append(sortBy);                   // injection

// To'g'ri: parametrlar bilan, tartiblash whitelist orqali (29-bob).
var sql = new StringBuilder("SELECT id, number, total FROM orders WHERE 1=1");
var params = new MapSqlParameterSource();
if (status != null) { sql.append(" AND status = :status"); params.addValue("status", status.name()); }
if (from != null)   { sql.append(" AND created_at >= :from"); params.addValue("from", from); }
sql.append(" ORDER BY ").append(SortColumn.of(sortBy).sql());    // enum: xavfsiz
sql.append(" LIMIT :limit");                                     // chegara majburiy
params.addValue("limit", Math.min(size, 100));

// Yoki JPA Criteria / jOOQ / QueryDSL - tipli qurish.
// Review tavsiyasi: uchdan ko'p ixtiyoriy shart bo'lsa, satr qurish
// o'rniga tipli qurilma ishlatish - injection xavfi strukturaviy
// ravishda yo'qoladi.
```

### 24.6 Katta jadvallar bilan ishlash

```sql
-- Naqsh: COUNT(*) katta jadvalda har sahifada.
SELECT count(*) FROM orders WHERE status = 'CLOSED';   -- 38 mln qator sanaladi
-- Review izohi: Spring Data `Page` har so'rovda COUNT bajaradi. Bu
-- 38 mln qatorli jadvalda 2-4 sekund. Yechimlar:
--   1) `Slice` ishlatish (COUNT yo'q, faqat "keyingi sahifa bormi");
--   2) taxminiy son: pg_class.reltuples;
--   3) alohida keshlangan hisoblagich.
SELECT reltuples::bigint AS taxminiy FROM pg_class WHERE relname = 'orders';

-- Naqsh: DELETE katta hajmda - uzoq qulf va WAL to'lishi.
DELETE FROM audit_log WHERE created_at < now() - interval '1 year';   -- 50 mln qator
-- To'g'ri: bo'laklab.
DO $$
DECLARE deleted int;
BEGIN
  LOOP
    DELETE FROM audit_log WHERE id IN (
        SELECT id FROM audit_log
         WHERE created_at < now() - interval '1 year'
         LIMIT 10000);
    GET DIAGNOSTICS deleted = ROW_COUNT;
    EXIT WHEN deleted = 0;
    COMMIT;                      -- har bo'lak alohida tranzaksiyada
    PERFORM pg_sleep(0.1);       -- replikatsiyaga nafas berish
  END LOOP;
END $$;
-- Eng yaxshi yechim: partitsiyalash va DROP PARTITION (bir zumda).
```

### 24.7 JSONB review

```sql
-- JSONB qulay, lekin review da uch savol bor.
-- 1) Nega JSONB va nega oddiy ustun emas?
--    Agar maydon har doim bor va u bo'yicha filtrlanadi - ustun bo'lishi kerak.
-- 2) Indeks bormi?
CREATE INDEX orders_meta_gin ON orders USING gin (metadata jsonb_path_ops);
-- Yoki aniq yo'l uchun ifoda indeksi (kichikroq va tezroq):
CREATE INDEX orders_channel_idx ON orders ((metadata->>'channel'));
-- 3) Sxema qanday nazorat qilinadi?
ALTER TABLE orders ADD CONSTRAINT metadata_shape CHECK (
    jsonb_typeof(metadata) = 'object'
    AND metadata ? 'channel'                     -- majburiy kalit
    AND metadata->>'channel' IN ('WEB', 'APP', 'POS')
);
-- JSONB da sxema bo'lmasa, u "nima bo'lsa shu" maydoniga aylanadi va
-- bir yildan keyin undagi ma'lumotni hech kim ishonchli o'qiy olmaydi.
```

### 24.8 Review paytida so'rovni o'lchash

```bash
# Review da dalil to'plash: eng qimmat so'rovlar va yangi so'rovning rejasi.
# 1) Prodda eng ko'p vaqt oladigan so'rovlar (pg_stat_statements kerak).
psql -c "SELECT calls,
                round(mean_exec_time::numeric, 1) AS avg_ms,
                round(total_exec_time::numeric/1000, 1) AS total_s,
                rows/greatest(calls,1) AS rows_per_call,
                left(query, 90) AS sorov
           FROM pg_stat_statements
          ORDER BY total_exec_time DESC LIMIT 15;"

# 2) Indekssiz skanerlar ko'p bo'lgan jadvallar.
psql -c "SELECT relname, seq_scan, seq_tup_read, idx_scan,
                seq_tup_read / greatest(seq_scan, 1) AS avg_rows_per_scan
           FROM pg_stat_user_tables
          WHERE seq_scan > 100
          ORDER BY seq_tup_read DESC LIMIT 10;"

# 3) PR dagi yangi so'rovning rejasini staging da olish.
psql -c "EXPLAIN (ANALYZE, BUFFERS) <yangi so'rov>"

# 4) Ilova yuborayotgan haqiqiy SQL ni ko'rish (lokal).
#    logging.level.org.hibernate.SQL=debug yoki
psql -c "ALTER SYSTEM SET log_min_duration_statement = '200ms';" -c "SELECT pg_reload_conf();"
```

### 24.9 Review checklisti: SQL va indekslar

| Savol | Nega |
| --- | --- |
| Filtr ustuni funksiya ichida emasmi | Indeks ishlamaydi |
| Yangi `WHERE`/`ORDER BY` ustuni indekslanganmi | Seq scan |
| Indeks ustunlari tartibi to'g'rimi | Prefiks qoidasi |
| Indeks mavjudining dublikati emasmi | Ortiqcha yozuv narxi |
| Katta jadvalda `CONCURRENTLY` ishlatilganmi | Yozuv bloklanishi |
| `LIMIT` majburiymi | Chegarasiz natija |
| Pagination tartibida yagona kalit bormi | Takrorlanish |
| Ko'p `JOIN` da agregat ko'paymaydimi | Noto'g'ri `SUM` |
| `LEFT JOIN` sharti `ON` dami | Jim `INNER JOIN` |
| `NOT IN` da NULL xavfi bormi | Bo'sh natija |
| Dinamik SQL parametrlar bilanmi | Injection |
| Katta `DELETE`/`UPDATE` bo'laklanganmi | Qulf va WAL |
| JSONB da indeks va sxema nazorati bormi | O'qilmaydigan ma'lumot |
| `COUNT(*)` har sahifada bajarilmaydimi | Sekin pagination |

### 24.10 Amalda qo'llash

- [ ] `pg_stat_statements` ni yoqib, eng qimmat 15 so'rovni oling va ularning har biri kodda qayerdan kelayotganini aniqlang.
- [ ] `pg_stat_user_indexes` dan `idx_scan = 0` bo'lgan indekslarni toping va olib tashlashni rejalashtiring.
- [ ] Bir-birini qoplaydigan indekslarni aniqlaydigan so'rovni ishga tushirib, ortiqchalarini belgilang.
- [ ] Filtrda funksiya ishlatilgan so'rovlarni (`date(...)`, `lower(...)`) toping va oraliq yoki ifoda indeksiga o'tkazing.
- [ ] Ko'p `JOIN` va `SUM` ishlatadigan hisobotlarni tekshirib, qatorlar ko'payishi natijani buzmasligini test bilan tasdiqlang.
- [ ] Dinamik SQL quruvchi joylarni toping va tartiblash ustunlarini enum whitelist ga o'tkazing.
- [ ] `Page` ishlatadigan katta jadval so'rovlarini `Slice` yoki keyset pagination ga o'tkazing.
- [ ] Yangi indeks qo'shadigan PR lar uchun `EXPLAIN (ANALYZE, BUFFERS)` natijasini majburiy talab qilib qo'ying.
- [ ] JSONB ustunlari uchun `CHECK` constraint va indeks borligini tekshiring.

## 25. Migratsiya review: qulf, backfill, orqaga moslik (Reviewing Migrations)

Migratsiya - review ning eng yuqori xavfli qismi. Sababi oddiy: kodni qaytarish mumkin, ma'lumotni qaytarish ko'pincha mumkin emas. Bundan tashqari migratsiya diffda zararsiz ko'rinadi - bitta `ALTER TABLE` qatori. Shu qator 12 million qatorli jadvalda 8 daqiqa davomida barcha yozuvlarni bloklashi mumkin, ya'ni to'liq to'xtash. Shu sababli migratsiyaga tegadigan PR har doim eng chuqur review darajasini oladi.

### 25.1 Birinchi savol: bu operatsiya qanday qulf oladi

PostgreSQL da har bir DDL operatsiyasi qulf oladi, va qulf turi hamma narsani belgilaydi. `ACCESS EXCLUSIVE` qulfi jadvalga har qanday murojaatni - hatto `SELECT` ni ham - bloklaydi.

| Operatsiya | Qulf | Davomiyligi | Xavf |
| --- | --- | --- | --- |
| `ADD COLUMN` (standart qiymatsiz, nullable) | ACCESS EXCLUSIVE | Bir zumda (metadata) | Past |
| `ADD COLUMN ... DEFAULT <const>` (PG 11+) | ACCESS EXCLUSIVE | Bir zumda | Past |
| `ADD COLUMN ... DEFAULT <volatile>` | ACCESS EXCLUSIVE | Jadvalni qayta yozadi | Juda yuqori |
| `ADD COLUMN ... NOT NULL` qiymatsiz | ACCESS EXCLUSIVE | Xato beradi (mavjud qatorlar) | - |
| `DROP COLUMN` | ACCESS EXCLUSIVE | Bir zumda (mantiqiy) | O'rtacha (kod moslik) |
| `ALTER COLUMN TYPE` | ACCESS EXCLUSIVE | Jadvalni qayta yozadi | Juda yuqori |
| `ALTER COLUMN SET NOT NULL` | ACCESS EXCLUSIVE | To'liq skan | Yuqori |
| `ADD CONSTRAINT CHECK` | ACCESS EXCLUSIVE | To'liq skan | Yuqori |
| `ADD CONSTRAINT ... NOT VALID` | ACCESS EXCLUSIVE | Bir zumda | Past |
| `VALIDATE CONSTRAINT` | SHARE UPDATE EXCLUSIVE | To'liq skan, lekin yozuv o'tadi | Past |
| `ADD FOREIGN KEY` | Ikki jadvalda SHARE ROW EXCLUSIVE | Skan | Yuqori |
| `CREATE INDEX` | SHARE (yozuv bloklanadi) | Uzoq | Yuqori |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Uzoqroq, lekin yozuv o'tadi | Past |
| `DROP INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Tez | Past |
| `RENAME COLUMN` | ACCESS EXCLUSIVE | Bir zumda | Yuqori (kod moslik) |
| `TRUNCATE` | ACCESS EXCLUSIVE | Tez | Juda yuqori (ma'lumot) |

```sql
-- Review da to'xtatiladigan migratsiya: diffda bir qator.
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2) NOT NULL DEFAULT random();
-- Uch muammo: (1) volatile default - 12 mln qator qayta yoziladi;
-- (2) ACCESS EXCLUSIVE qulfi shu vaqt davomida hamma so'rovni bloklaydi;
-- (3) jadval hajmi ikki baravar oshadi (eski versiyalar VACUUM gacha qoladi).

-- Xavfsiz ketma-ketlik: uch qadam, har biri tez.
-- 1-qadam (bu reliz): nullable ustun qo'shish - bir zumda.
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);

-- 2-qadam (alohida ish): bo'laklab to'ldirish, qulfsiz.
--   UPDATE orders SET risk_score = ... WHERE risk_score IS NULL AND id IN (...)
--   har 10 000 qator, alohida tranzaksiya.

-- 3-qadam (keyingi reliz): NOT NULL ni arzon qo'shish.
ALTER TABLE orders ADD CONSTRAINT risk_score_not_null
    CHECK (risk_score IS NOT NULL) NOT VALID;      -- bir zumda
ALTER TABLE orders VALIDATE CONSTRAINT risk_score_not_null;  -- yozuvni bloklamaydi
-- (PG 12+ da: constraint validatsiya qilingach SET NOT NULL arzon bo'ladi)
```

### 25.2 Qulf kutish navbati: yashirin kaskad

Eng ko'p e'tibordan chetda qoladigan mexanizm: `ACCESS EXCLUSIVE` qulfini kutayotgan DDL o'zidan keyingi barcha so'rovlarni ham bloklaydi, hatto ular `SELECT` bo'lsa ham.

```text
T1: uzoq SELECT ishlayapti (30 sekund, hisobot)        -> ACCESS SHARE qulfi
T2: ALTER TABLE ... kutadi (T1 tugashini)              -> ACCESS EXCLUSIVE so'raydi
T3: oddiy SELECT                                        -> T2 ortida navbatda qoladi!
T4..T200: barcha so'rovlar navbatda                     -> ilova to'xtaydi
```

Shu sababli migratsiya uchun `lock_timeout` majburiy: DDL qulfni darhol olmasa, voz kechadi va keyin qayta urinadi, navbat yaratmaydi.

```sql
-- Har bir xavfli migratsiyaning boshida: qulfni kutmaslik.
SET lock_timeout = '3s';
SET statement_timeout = '30s';
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);
-- Qulf 3 sekundda olinmasa: "canceling statement due to lock timeout"
-- Migratsiya yiqiladi, lekin ilova to'xtamaydi. Keyin qayta urinish mumkin.
```

```sql
-- Flyway da har migratsiya uchun sozlash (yoki alohida fayl boshida).
-- V42__add_risk_score.sql
SET lock_timeout = '3s';
ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);
```

### 25.3 Orqaga moslik: deploy tartibi

Migratsiya va kod bir vaqtda ishga tushmaydi. Rolling deploy da eski va yangi kod bir necha daqiqa (yoki soat) birga ishlaydi. Shu sababli migratsiya har doim ikki tomonga mos bo'lishi kerak.

| O'zgarish | Eski kod bilan ishlaydimi | To'g'ri ketma-ketlik |
| --- | --- | --- |
| Nullable ustun qo'shish | Ha | Bitta reliz |
| `NOT NULL` ustun qo'shish | Yo'q (eski kod uni to'ldirmaydi) | Nullable qo'shish -> kod -> NOT NULL |
| Ustun olib tashlash | Yo'q (eski kod o'qiydi) | Kodni tozalash -> keyingi relizda DROP |
| Ustun nomini o'zgartirish | Yo'q | Yangi ustun -> ikkisiga yozish -> ko'chirish -> eskisini olib tashlash |
| Turni o'zgartirish | Ko'pincha yo'q | Yangi ustun bilan ko'chirish |
| Jadval nomini o'zgartirish | Yo'q | View bilan o'tish davri |
| Enum qiymati qo'shish | Ha (eski kod uni bilmaydi, lekin o'qiydi) | Avval DB, keyin kod |
| Enum qiymatini olib tashlash | Yo'q | Avval kod, keyin DB |
| Unique constraint qo'shish | Faqat ma'lumot toza bo'lsa | Dublikatlarni tozalash -> `CONCURRENTLY` indeks -> constraint |

```sql
-- Ustun nomini o'zgartirish: to'rt relizli naqsh ("expand and contract").
-- Review da bitta RENAME ko'rilsa, bu blocker.

-- RELIZ 1: yangi ustun qo'shish (nullable).
ALTER TABLE customer ADD COLUMN phone_e164 text;

-- RELIZ 1 kodi: ikkisiga ham yozadi, eskisidan o'qiydi.
--   customer.setPhone(p); customer.setPhoneE164(normalize(p));

-- RELIZ 2: eski ma'lumotni ko'chirish (bo'laklab, migratsiyadan tashqarida).
--   UPDATE customer SET phone_e164 = normalize(phone)
--    WHERE phone_e164 IS NULL AND id BETWEEN ? AND ?;

-- RELIZ 2 kodi: yangisidan o'qiydi, ikkisiga yozadi.

-- RELIZ 3 kodi: faqat yangisi bilan ishlaydi.

-- RELIZ 4: eski ustunni olib tashlash.
ALTER TABLE customer DROP COLUMN phone;
```

Review izohining shakli bunday holatda: "`RENAME COLUMN` rolling deploy da eski podlarni darhol sindiradi. Bizda 6 pod va deploy 4 daqiqa davom etadi - shu vaqt ichida barcha so'rovlar `column phone does not exist` beradi. Expand-and-contract ketma-ketligi kerak."

### 25.4 Backfill review

Katta jadvaldagi ma'lumotni to'ldirish - alohida xavf sinfi. Uni migratsiya fayliga qo'yish deyarli har doim xato.

```sql
-- Blocker: migratsiya ichida butun jadvalga UPDATE.
UPDATE orders SET risk_score = 0 WHERE risk_score IS NULL;   -- 12 mln qator
-- Oqibatlari: (1) bitta tranzaksiya, 12 mln qator qulflanadi;
-- (2) WAL hajmi gigabaytlarga chiqadi, replikatsiya lag o'sadi;
-- (3) migratsiya 20 daqiqa ishlaydi, deploy timeout iga tushadi;
-- (4) yarmida yiqilsa, hammasi qaytadi va qaytadan boshlanadi;
-- (5) jadval bo'rtadi (bloat) - har qator yangi versiya oladi.
```

```java
// To'g'ri: backfill alohida, boshqarilishi mumkin, kuzatiladigan ish.
@Component
public class RiskScoreBackfill {

    private static final int BATCH = 5_000;

    @Scheduled(fixedDelay = 1_000)
    public void run() {
        if (!enabled) return;
        // Idempotent: faqat to'ldirilmagan qatorlar, ID bo'yicha oldinga yurish.
        int updated = jdbc.update("""
            UPDATE orders SET risk_score = 0
             WHERE id IN (SELECT id FROM orders
                           WHERE risk_score IS NULL
                           ORDER BY id
                           LIMIT ?)
            """, BATCH);
        processed.addAndGet(updated);
        meter.gauge("backfill.remaining", remainingCount());
        if (updated == 0) { enabled = false; log.info("backfill tugadi"); }
    }
}
// Review talablari backfill uchun:
// 1) bo'lak hajmi va tezlik boshqariladi (to'xtatish imkoni bor);
// 2) idempotent - qayta ishga tushirish xavfsiz;
// 3) progress o'lchanadi va alert bor;
// 4) replikatsiya lag kuzatiladi va kerak bo'lsa sekinlashtiriladi;
// 5) yangi yozuvlar ham to'g'ri qiymat oladi (kod yoki DEFAULT).
```

### 25.5 Qaytarish rejasi

```sql
-- Review savoli har bir migratsiya uchun: qaytarish qanday?
-- Flyway da `undo` faqat tijorat versiyasida, shu sababli qaytarish
-- rejasi yozma bo'lishi kerak, kodda emas.
```

| Migratsiya turi | Qaytarish |
| --- | --- |
| Ustun qo'shish | `DROP COLUMN` - xavfsiz, lekin ma'lumot ketadi |
| Indeks qo'shish | `DROP INDEX CONCURRENTLY` - xavfsiz |
| Ustun olib tashlash | Qaytarilmaydi - ma'lumot yo'q |
| Turni o'zgartirish | Qaytarilmaydi - aniqlik yo'qolgan bo'lishi mumkin |
| Ma'lumot ko'chirish | Faqat eski ma'lumot saqlangan bo'lsa |
| `DROP TABLE` | Faqat backup dan |
| Constraint qo'shish | `DROP CONSTRAINT` - xavfsiz |

Review qoidasi: qaytarilmaydigan migratsiya (ustun yoki jadval o'chirish, tur o'zgartirish) alohida relizda va alohida tasdiq bilan boriladi. Bundan tashqari o'chirish oldidan kutish davri bo'lishi kerak: ustun kodda ishlatilmay qolgandan keyin kamida bir reliz kutiladi, shunda qaytarish imkoni saqlanadi.

```sql
-- Qaytarish imkonini saqlash: o'chirish o'rniga ko'chirish.
-- Jadvalni darhol o'chirish o'rniga:
ALTER TABLE legacy_orders RENAME TO legacy_orders_deprecated_20261004;
-- Bir oydan keyin, hech kim shikoyat qilmagach:
DROP TABLE legacy_orders_deprecated_20261004;
```

### 25.6 Migratsiya fayllarining o'zi

| Review savoli | Nega |
| --- | --- |
| Fayl nomi konvensiyaga mosmi | `V42__add_risk_score.sql` - raqam va tavsif |
| Mavjud migratsiya o'zgartirilmaganmi | Checksum buziladi, Flyway yiqiladi |
| Raqam konflikti bormi (ikki branch) | Ikki PR da `V42` - merge dan keyin xato |
| Migratsiya idempotentmi | `IF NOT EXISTS` kerak bo'lgan joylarda |
| Tranzaksiyada bajariladimi | PostgreSQL DDL tranzaksion, lekin `CONCURRENTLY` emas |
| `CONCURRENTLY` alohida faylda bormi | Tranzaksiya ichida ishlamaydi |
| Ma'lumot o'zgartirish bormi | Backfill alohida bo'lishi kerak |
| Sinalganmi va qancha vaqt oldi | Real hajmdagi nusxada |

```sql
-- CREATE INDEX CONCURRENTLY tranzaksiya ichida ishlamaydi.
-- Flyway da bu fayl uchun tranzaksiyani o'chirish kerak:
-- V43__add_orders_index.sql
-- flyway:executeInTransaction=false
CREATE INDEX CONCURRENTLY IF NOT EXISTS orders_open_idx
    ON orders (customer_id, created_at DESC)
    WHERE status IN ('NEW', 'PAID');
-- Diqqat: CONCURRENTLY yiqilsa, yaroqsiz (invalid) indeks qoladi va u
-- so'rovlarda ishlatilmaydi, lekin yozuvni sekinlashtiradi. Tekshirish:
--   SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
```

```bash
# Migratsiya raqami konfliktini CI da tutish.
# Ikki branch bir xil versiya raqamini ishlatsa, merge dan keyin bilinadi.
ls src/main/resources/db/migration/V*.sql \
  | sed -E 's/.*\/V([0-9]+)__.*/\1/' | sort | uniq -d \
  | while read -r dup; do echo "XATO: V$dup takrorlangan"; exit 1; done

# Mavjud migratsiya o'zgartirilganini tutish (checksum buzilishi).
git diff --name-status origin/main...HEAD -- 'src/main/resources/db/migration/' \
  | awk '$1=="M" {print "XATO: mavjud migratsiya tahrirlangan: "$2}'
```

### 25.7 Migratsiyani sinash

```bash
# Review da talab qilinadigan dalil: migratsiya real hajmda sinalgan.
# 1) Prod nusxasida (yoki shunga yaqin hajmda) vaqtni o'lchash.
pg_dump --schema-only prod_db > schema.sql
psql -c "CREATE DATABASE migration_test;"
psql migration_test < schema.sql
# Ma'lumot hajmini generatsiya qilish (yoki anonimlashtirilgan nusxa).
psql migration_test -c "INSERT INTO orders SELECT ... FROM generate_series(1, 12000000);"

# 2) Migratsiyani o'lchash va qulfni kuzatish.
psql migration_test -c "\timing on" -f src/main/resources/db/migration/V42__add_risk_score.sql

# 3) Migratsiya ishlayotganda boshqa sessiyada yozuv o'tadimi - tekshirish.
#    1-terminal: migratsiya; 2-terminal:
psql migration_test -c "INSERT INTO orders (id, number) VALUES (gen_random_uuid(), 'test');"
#    Agar bu buyruq kutsa - migratsiya yozuvni bloklaydi.

# 4) Tozalash.
psql -c "DROP DATABASE migration_test;"
```

```java
// Testcontainers bilan avtomatik tekshiruv: migratsiyalar toza bazada
// va mavjud ma'lumot bilan ishlaydimi.
@Test
void migrationsRunOnSchemaWithExistingData() {
    try (PostgreSQLContainer<?> pg = new PostgreSQLContainer<>("postgres:16")) {
        pg.start();
        // 1) Avvalgi relizning sxemasiga ko'chish.
        Flyway.configure().dataSource(pg.getJdbcUrl(), pg.getUsername(), pg.getPassword())
              .target(MigrationVersion.fromVersion("41"))
              .load().migrate();
        // 2) Mavjud ma'lumotni qo'yish (eski kod yozadigan shakl).
        insertLegacyRows(pg, 10_000);
        // 3) Yangi migratsiyalarni qo'llash - xatosiz o'tishi kerak.
        MigrateResult r = Flyway.configure()
              .dataSource(pg.getJdbcUrl(), pg.getUsername(), pg.getPassword())
              .load().migrate();
        assertThat(r.success).isTrue();
        // 4) Ma'lumot buzilmaganini tekshirish.
        assertThat(countRows(pg, "orders")).isEqualTo(10_000);
    }
}
```

### 25.8 Review checklisti: migratsiya

| Savol | Nega |
| --- | --- |
| Qanday qulf oladi va qancha vaqt | To'liq to'xtash xavfi |
| `lock_timeout` qo'yilganmi | Navbat kaskadi |
| Jadval qayta yozilmaydimi | Uzoq qulf va hajm |
| Rolling deploy da eski kod ishlaydimi | Deploy paytida xatolar |
| Backfill alohida va bo'laklanganmi | WAL, lag, bloat |
| Yangi yozuvlar to'g'ri qiymat oladimi | Yarim to'ldirilgan ustun |
| Qaytarish rejasi yozilganmi | Reliz qaytarilmasligi |
| `CONCURRENTLY` alohida, tranzaksiyasiz faylmi | Xato |
| Versiya raqami konflikti yo'qmi | Merge dan keyin yiqilish |
| Mavjud migratsiya o'zgartirilmaganmi | Checksum |
| Real hajmda sinalganmi va vaqti o'lchanganmi | Taxminiy xavf |
| Ma'lumot yo'qotadigan operatsiya alohida relizdami | Qaytarib bo'lmaslik |
| FK va unique qo'shishda mavjud ma'lumot tozami | Migratsiya yiqilishi |

### 25.9 Amalda qo'llash

- [ ] Migratsiya fayllarini o'zgartiradigan PR lar uchun `CODEOWNERS` da majburiy reviewer belgilang.
- [ ] Qulf turlari jadvalini `REVIEW.md` ga qo'shing va har migratsiya PR ida shu jadval bo'yicha javob talab qiling.
- [ ] Barcha migratsiya fayllariga `SET lock_timeout` qo'yish konvensiyasini joriy qiling.
- [ ] Migratsiya versiya raqami konflikti va mavjud fayl o'zgarishini tutadigan CI tekshiruvini qo'shing.
- [ ] Yaroqsiz indekslarni (`NOT indisvalid`) kuzatadigan monitoring so'rovini qo'shing.
- [ ] Testcontainers bilan "avvalgi versiyaga ko'chish -> ma'lumot qo'yish -> yangi migratsiyalar" testini yozing.
- [ ] Eng katta beshta jadval hajmini `REVIEW.md` ga yozib qo'ying - reviewer qulf xavfini tez baholashi uchun.
- [ ] Ma'lumot yo'qotadigan migratsiyalar uchun "ko'chirib nomlash va bir oy kutish" konvensiyasini kelishib oling.
- [ ] Backfill lar uchun standart shablon (bo'lak, idempotentlik, progress metrikasi, to'xtatish kaliti) tayyorlang.

## 26. Ma'lumot to'g'riligi va turlar review (Data Correctness)

Bu bob ma'lumotning o'zi haqida: qaysi qiymat bazaga tushishi mumkin va qaysi biri mumkin emas. Kod xatosini tuzatish arzon, buzilgan ma'lumotni tuzatish qimmat va ba'zan imkonsiz. Shu sababli review da yangi ustun yoki yangi yozuv yo'li paydo bo'lganda, birinchi savol himoya haqida bo'ladi.

### 26.1 Constraint - yagona ishonchli himoya

Ilova kodidagi tekshiruv ikki instansda, migratsiyada, qo'lda `UPDATE` da va eski kod versiyasida ishlamaydi. Faqat ma'lumotlar bazasidagi constraint har doim ishlaydi.

```sql
-- Review da talab qilinadigan minimal himoya to'plami.
CREATE TABLE payment (
    id              uuid        PRIMARY KEY,
    order_id        uuid        NOT NULL REFERENCES orders(id),
    idempotency_key text        NOT NULL,
    amount          numeric(19,4) NOT NULL,
    currency        char(3)     NOT NULL,
    status          text        NOT NULL,
    created_at      timestamptz NOT NULL DEFAULT now(),
    captured_at     timestamptz,

    -- Pul manfiy bo'lmaydi va nol ham bo'lmaydi.
    CONSTRAINT payment_amount_positive CHECK (amount > 0),
    -- Valyuta kodi shakli.
    CONSTRAINT payment_currency_shape CHECK (currency ~ '^[A-Z]{3}$'),
    -- Status faqat ma'lum qiymatlardan.
    CONSTRAINT payment_status_valid
        CHECK (status IN ('PENDING', 'CAPTURED', 'DECLINED', 'REFUNDED')),
    -- Mantiqiy bog'liqlik: captured_at faqat CAPTURED holatida bo'ladi.
    CONSTRAINT payment_captured_consistency
        CHECK ((status = 'CAPTURED') = (captured_at IS NOT NULL)),
    -- Vaqt tartibi.
    CONSTRAINT payment_time_order CHECK (captured_at IS NULL OR captured_at >= created_at)
);

-- Idempotentlik: faqat unique indeks ishonchli (10.9).
CREATE UNIQUE INDEX payment_idem_uniq ON payment (idempotency_key);

-- Biznes qoidasi: bitta buyurtmaga bitta aktiv to'lov.
CREATE UNIQUE INDEX payment_one_active_per_order ON payment (order_id)
    WHERE status IN ('PENDING', 'CAPTURED');
```

Oxirgi indeks - review da kam uchraydigan, lekin juda kuchli vosita: partial unique indeks biznes qoidasini bazada majburlaydi va poyga holatlarini butunlay yo'q qiladi.

### 26.2 Pul: tur, aniqlik, valyuta

| Qaror | To'g'ri | Xato |
| --- | --- | --- |
| Java turi | `BigDecimal` + valyuta (`Money`) | `double`, `float` |
| PostgreSQL turi | `numeric(19,4)` yoki butun son (tiyin) | `float8`, `money` |
| Yakkalash | Aniq `RoundingMode`, biznes bilan kelishilgan | Standartga tashlab qo'yish |
| Valyuta | Alohida ustun, har summa bilan | Taxmin qilish |
| Taqqoslash | `compareTo` | `equals` |
| Yig'indi | SQL `sum(numeric)` yoki `Money::plus` | `double` yig'indisi |

```sql
-- PostgreSQL `money` turi ishlatilmaydi: u lokalga bog'liq va aniqligi
-- sozlamalardan keladi. numeric aniq va portativ.
amount numeric(19,4) NOT NULL          -- to'g'ri
amount money NOT NULL                  -- review da rad etiladi
amount double precision NOT NULL       -- blocker: aniqlik yo'qoladi

-- Valyuta aralashuvini bazada taqiqlash: agregatlarda ham xavfsiz.
CREATE TABLE invoice_line (
    invoice_id uuid NOT NULL,
    amount     numeric(19,4) NOT NULL,
    currency   char(3) NOT NULL
);
-- Invoys ichidagi hamma qator bir valyutada bo'lishi kerak:
-- trigger yoki denormalizatsiya (invoice.currency + FK) bilan majburlanadi.
```

### 26.3 Vaqt: zona, tur, tartib

```sql
-- timestamp va timestamptz: diffda bir harf farq, xulqda katta farq.
created_at timestamp                   -- zonasiz: "2026-10-04 12:00" - qaysi zonada?
created_at timestamptz                 -- UTC nuqta, zona bilan to'g'ri ishlaydi

-- Review qoidasi: hodisa vaqti har doim timestamptz.
-- Kalendar sanasi (tug'ilgan kun, bayram) esa date - zonasiz to'g'ri.
birth_date date                        -- to'g'ri: zona ma'nosiz
holiday_on date                        -- to'g'ri

-- Vaqt manbasi: ilova yoki baza?
created_at timestamptz NOT NULL DEFAULT now()
-- now() tranzaksiya boshlanish vaqtini beradi (clock_timestamp() - haqiqiy).
-- Review savoli: ikki serverning vaqti farq qilsa, tartib buziladimi?
-- Agar tartib muhim bo'lsa, ketma-ketlik (sequence) yoki bazadagi vaqt
-- ishlatiladi, ilova vaqti emas.
```

### 26.4 Enum: baza va kod sinxronizatsiyasi

| Variant | Foydasi | Narxi |
| --- | --- | --- |
| `text` + `CHECK IN (...)` | Qiymat qo'shish oson (`ALTER CONSTRAINT`) | Constraint ni yangilash kerak |
| PostgreSQL `enum` turi | Tipli, kichik saqlanadi | Qiymat olib tashlash qiyin, `ALTER TYPE` cheklovlari |
| Ma'lumotnoma jadval + FK | Metadata qo'shish mumkin | JOIN kerak |
| Hech qanday himoya | - | Bazaga har qanday satr tushadi |

```sql
-- Eng amaliy variant: text + CHECK. Yangi qiymat qo'shish:
ALTER TABLE orders DROP CONSTRAINT orders_status_valid;
ALTER TABLE orders ADD CONSTRAINT orders_status_valid
    CHECK (status IN ('NEW','PAID','SHIPPED','DELIVERED','CANCELLED','REFUNDED'))
    NOT VALID;                                       -- bir zumda
ALTER TABLE orders VALIDATE CONSTRAINT orders_status_valid;   -- bloklamaydi

-- Review diqqati: deploy tartibi. Yangi status kodda ishlatilishidan
-- OLDIN constraint yangilanishi kerak, aks holda yangi kod yozganda
-- constraint xatosi chiqadi (25.3 jadvaliga qarang).
```

```java
// Kod va baza o'rtasidagi mosligni test bilan qulflash.
@Test
void databaseConstraintCoversAllEnumValues() {
    // Bazadagi CHECK dan qiymatlarni o'qib, enum bilan solishtirish.
    String check = jdbc.queryForObject("""
        SELECT pg_get_constraintdef(oid) FROM pg_constraint
         WHERE conname = 'orders_status_valid'
        """, String.class);
    for (OrderStatus s : OrderStatus.values()) {
        assertThat(check)
            .as("baza constraint i %s qiymatini qabul qilishi kerak", s)
            .contains("'" + s.name() + "'");
    }
}
// Bu test enum ga yangi qiymat qo'shilib, migratsiya yozilmaganini tutadi -
// aks holda bu xato faqat prodda chiqadi.
```

### 26.5 NULL semantikasi

```sql
-- NULL ning ma'nosi yozilishi kerak: "bilinmaydi", "qo'llanmaydi" yoki "hali yo'q".
-- Review savoli: bu ustun nega nullable?

-- Xavfli naqsh: nullable boolean - uch holatli mantiq.
is_verified boolean                    -- true, false, NULL - NULL nima?
is_verified boolean NOT NULL DEFAULT false   -- aniq

-- NULL va unique: PostgreSQL da NULL lar bir-biriga teng emas.
CREATE UNIQUE INDEX ON customer (email);
-- Ikki qator email = NULL bilan - ikkisi ham o'tadi (dublikat emas).
-- Agar faqat bitta NULL bo'lishi kerak bo'lsa (PG 15+):
CREATE UNIQUE INDEX ON customer (email) NULLS NOT DISTINCT;

-- NULL va taqqoslash: eng ko'p uchraydigan mantiq xatosi.
SELECT * FROM orders WHERE cancelled_at <> '2026-01-01';
-- cancelled_at IS NULL bo'lgan qatorlar natijaga TUSHMAYDI.
-- To'g'ri: WHERE (cancelled_at IS NULL OR cancelled_at <> '2026-01-01')
-- yoki: WHERE cancelled_at IS DISTINCT FROM '2026-01-01'

-- NULL va agregat:
SELECT avg(risk_score) FROM orders;    -- NULL lar hisobga olinmaydi
-- Agar NULL ni 0 deb hisoblash kerak bo'lsa - coalesce aniq yozilishi kerak.
```

### 26.6 Tashqi kalitlar va o'chirish qoidalari

```sql
-- FK qoidasi ongli tanlanishi kerak, standartga tashlab qo'yilmasligi.
order_id uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE
-- CASCADE: buyurtma o'chirilsa, to'lovlar ham o'chadi. Buxgalteriya uchun xato.
order_id uuid NOT NULL REFERENCES orders(id) ON DELETE RESTRICT
-- RESTRICT: to'lovi bor buyurtmani o'chirib bo'lmaydi. Odatda to'g'ri.

-- Diqqat: FK ustunida indeks AVTOMATIK yaratilmaydi (PostgreSQL da).
-- Ota jadvaldan o'chirish yoki yangilash har bola jadvalda skan qiladi.
CREATE INDEX ON payment (order_id);   -- FK uchun indeks majburiy

-- FK ni mavjud katta jadvalga qo'shish: ikki qadamli xavfsiz yo'l (25.1).
ALTER TABLE payment ADD CONSTRAINT payment_order_fk
    FOREIGN KEY (order_id) REFERENCES orders(id) NOT VALID;    -- bir zumda
ALTER TABLE payment VALIDATE CONSTRAINT payment_order_fk;      -- bloklamaydi
```

```bash
# Indekssiz FK larni topish: review ning tez g'alabasi.
psql -c "
SELECT c.conrelid::regclass AS jadval, a.attname AS ustun
  FROM pg_constraint c
  JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = c.conkey[1]
 WHERE c.contype = 'f'
   AND NOT EXISTS (
       SELECT 1 FROM pg_index i
        WHERE i.indrelid = c.conrelid AND i.indkey[0] = c.conkey[1])
 ORDER BY 1;"
```

### 26.7 Yumshoq o'chirish (soft delete)

```sql
-- Yumshoq o'chirish review da uch savol tug'diradi.
deleted_at timestamptz

-- 1) Hamma so'rov bu shartni hisobga oladimi? Bitta esdan chiqsa,
--    o'chirilgan ma'lumot foydalanuvchiga ko'rinadi.
--    Himoya: view yoki RLS, @Where emas (23.8).
CREATE VIEW active_customer AS SELECT * FROM customer WHERE deleted_at IS NULL;

-- 2) Unique constraint qanday ishlaydi? O'chirilgan va yangi qator
--    bir xil email bilan bo'lishi kerakmi?
CREATE UNIQUE INDEX customer_email_active_uniq ON customer (lower(email))
    WHERE deleted_at IS NULL;          -- faqat aktivlar orasida yagona

-- 3) GDPR yoki ma'lumotni haqiqatan o'chirish talabi bormi?
--    Yumshoq o'chirish "o'chirish huquqi" ni bajarmaydi - anonimlashtirish
--    yoki haqiqiy o'chirish kerak bo'lishi mumkin (32-bob).
```

### 26.8 Ma'lumot migratsiyasidagi to'g'rilik

```sql
-- Review da ma'lumot ko'chirish uchun uchta talab.
-- 1) Qancha qator ta'sirlanadi - oldin sanash.
SELECT count(*) FROM customer WHERE phone IS NOT NULL AND phone_e164 IS NULL;

-- 2) Namuna bilan tekshirish - ko'chirish qoidasi to'g'rimi.
SELECT phone, normalize_phone(phone) AS natija
  FROM customer WHERE phone IS NOT NULL
 ORDER BY random() LIMIT 20;
-- Review izohi: shu 20 qatorni PR ga qo'shing - qoida to'g'ri ishlashini
-- ko'rsatish uchun eng arzon dalil.

-- 3) Ko'chirib bo'lmaydigan qatorlar bilan nima qilinadi?
SELECT count(*) FROM customer
 WHERE phone IS NOT NULL AND normalize_phone(phone) IS NULL;
-- Javob "jim tashlab yuboriladi" bo'lsa - bu blocker. Bu qatorlar
-- hisobotga yozilishi va qo'lda ko'rilishi kerak.
```

### 26.9 Review checklisti: ma'lumot to'g'riligi

| Savol | Nega |
| --- | --- |
| Yangi ustun uchun `NOT NULL` va `DEFAULT` to'g'rimi | Noma'lum holat |
| `CHECK` constraint lar bormi | Kod tekshiruvi yetarli emas |
| Yagonalik unique indeks bilan majburlanganmi | Poyga |
| Biznes qoidasi partial unique bilan ifodalanishi mumkinmi | Eng kuchli himoya |
| Pul `numeric` va valyuta bilanmi | Aniqlik va aralashuv |
| Vaqt `timestamptz` mi | Zona xatolari |
| Enum qiymatlari baza va kodda mosmi | Deploy xatosi |
| NULL ning ma'nosi aniqmi | Uch holatli mantiq |
| FK qoidasi (`CASCADE`/`RESTRICT`) ongli tanlanganmi | Ma'lumot yo'qolishi |
| FK ustunida indeks bormi | Sekin o'chirish |
| Soft delete hamma so'rovda hisobga olinadimi | Ma'lumot oqishi |
| Ma'lumot ko'chirish namuna bilan tekshirilganmi | Jim buzilish |
| Ko'chirilmaydigan qatorlar hisobotga tushadimi | Jim yo'qotish |

### 26.10 Amalda qo'llash

- [ ] Eng muhim beshta jadval uchun invariantlar ro'yxatini yozib, ularning qanchasi DB constraint bilan himoyalanganini aniqlang.
- [ ] Idempotentlik va yagonalik talab qiladigan barcha joylarda unique indeks borligini tasdiqlang.
- [ ] Pul ustunlarini `numeric` ga va `double precision`/`money` dan o'tkazish rejasini tuzing.
- [ ] `timestamp` (zonasiz) ustunlarni toping va `timestamptz` ga migratsiya rejasini yozing.
- [ ] Enum va DB constraint mosligini tekshiradigan testni qo'shing.
- [ ] Indekssiz FK larni topadigan so'rovni ishga tushirib, kerakli indekslarni qo'shing.
- [ ] Nullable ustunlar uchun NULL ning ma'nosini `GLOSSARY.md` yoki jadval izohida (`COMMENT ON COLUMN`) yozib qo'ying.
- [ ] Soft delete ishlatiladigan jadvallar uchun aktiv qatorlar view ini yoki RLS ni joriy qiling.
- [ ] Ma'lumot ko'chiradigan PR lar uchun "20 qator namuna + ko'chirilmaydiganlar soni" talabini kiriting.

## 27. Izolyatsiya, poyga holatlari va xabar yetkazish (Isolation, Races and Delivery)

Bu bob ma'lumot qatlamining eng qiyin qismini oladi: bir vaqtda ishlayotgan tranzaksiyalar va bir martadan ko'p yetkaziladigan xabarlar. Ularning umumiy xususiyati bor - testda ko'rinmaydi, yuk ostida ko'rinadi, va oqibati ma'lumot nomuvofiqligi bo'ladi. Reviewer uchun bitta tayanch savol: "ikki narsa bir vaqtda sodir bo'lsa yoki bir narsa ikki marta sodir bo'lsa, natija to'g'ri bo'ladimi".

### 27.1 PostgreSQL izolyatsiya darajalari va diffdagi ma'nosi

PostgreSQL ning standarti `READ COMMITTED`, va u Java kodidagi ko'p taxminlarni buzadi.

| Daraja | Nimani oldini oladi | Nimani oldini olmaydi |
| --- | --- | --- |
| `READ COMMITTED` (standart) | Yozilmagan ma'lumotni o'qish | Takrorlanmaydigan o'qish, fantom, lost update, write skew |
| `REPEATABLE READ` | Takrorlanmaydigan o'qish, fantom (PG da) | Write skew; konflikt bo'lsa xato beradi |
| `SERIALIZABLE` | Hammasi | Hech narsa, lekin xato (`40001`) berib retry talab qiladi |

```java
// READ COMMITTED da bitta tranzaksiya ichida ikki o'qish turli natija beradi.
@Transactional                                   // READ COMMITTED
public Report build(CustomerId id) {
    Money total = orders.sumByCustomer(id);      // 1 000 000
    int count = orders.countByCustomer(id);      // 11 - boshqa tranzaksiya qo'shdi
    // total 10 buyurtmaga, count 11 ga tegishli - hisobot nomuvofiq.
    return new Report(total, count, total.divide(count));   // noto'g'ri o'rtacha
}
// Review izohi: ikki so'rov orasida ma'lumot o'zgarishi mumkin. Agar
// hisobot ichki nomuvofiqligi qabul qilinmasa, bitta so'rovda hisoblash
// yoki REPEATABLE READ kerak.

// Yechim 1 (afzal): bitta so'rov - atomik ko'rinish.
@Query("select new ReportRow(sum(o.total), count(o)) from Order o where o.customer.id = :id")
ReportRow report(@Param("id") UUID id);

// Yechim 2: izolyatsiyani ko'tarish - lekin narxi bor.
@Transactional(isolation = Isolation.REPEATABLE_READ)
```

### 27.2 Poyga holatlarini topish usuli

Review da poyga holatini topishning tizimli usuli bor: har bir yozuv operatsiyasi uchun "o'qish va yozish orasida nima o'zgarishi mumkin" degan savol.

| Naqsh | Poyga turi | Himoya |
| --- | --- | --- |
| `exists` keyin `insert` | Fantom / dublikat | Unique indeks |
| `select` keyin `update` (hisoblab) | Lost update | `@Version` yoki atomik `UPDATE` |
| `select` qoldiq, keyin `update` | Write skew | `FOR UPDATE` yoki `SERIALIZABLE` |
| Ikki jadvaldan o'qib, qoida tekshirish | Write skew | Qulf yoki `SERIALIZABLE` |
| Hisoblagichni o'qib, oshirib yozish | Lost update | `UPDATE ... SET n = n + 1` |
| `delete` keyin `insert` (almashtirish) | Oraliq bo'shliq | Bitta `UPSERT` |
| Fayl yoki kesh tekshiruvi keyin yozuv | Umumiy resurs | Atomik operatsiya |

```java
// UPSERT: "bor bo'lsa yangila, yo'q bo'lsa qo'sh" - poygasiz yo'l.
@Modifying
@Query(value = """
    INSERT INTO daily_counter (day, metric, value)
    VALUES (:day, :metric, 1)
    ON CONFLICT (day, metric)
    DO UPDATE SET value = daily_counter.value + 1
    """, nativeQuery = true)
void increment(@Param("day") LocalDate day, @Param("metric") String metric);
// Bu bitta atomik operatsiya: hech qanday tekshir-keyin-yoz yo'q, hech
// qanday qulf navbati yo'q. Review da bu shakl afzal ko'riladi.
```

### 27.3 Qulf turlari va ularning narxi

```sql
-- FOR UPDATE: qator qulflanadi, boshqalar kutadi.
SELECT * FROM account WHERE id = ? FOR UPDATE;
-- Xavf: kutish cheksiz bo'lishi mumkin (lock_timeout kerak).

-- FOR UPDATE NOWAIT: kutmaydi, darhol xato.
SELECT * FROM account WHERE id = ? FOR UPDATE NOWAIT;
-- Foydali: foydalanuvchiga "hozir band, qayta urinib ko'ring" deyish.

-- FOR UPDATE SKIP LOCKED: qulflangan qatorlarni o'tkazib yuboradi.
SELECT * FROM job_queue WHERE status = 'NEW'
 ORDER BY created_at LIMIT 10 FOR UPDATE SKIP LOCKED;
-- Navbat uchun ideal: workerlar bir-birini kutmaydi.

-- FOR SHARE: o'qish qulfi - boshqalar o'qiydi, yozmaydi.
-- Kam ishlatiladi; ko'pincha FOR UPDATE yoki hech narsa to'g'ri.
```

```java
// Spring Data da qulf turlari.
public interface AccountRepository extends JpaRepository<Account, UUID> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)                    // FOR UPDATE
    @Query("select a from Account a where a.id = :id")
    Optional<Account> lockById(@Param("id") UUID id);

    // Timeout bilan: cheksiz kutmaslik.
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000"))
    @Query("select a from Account a where a.id = :id")
    Optional<Account> lockByIdWithTimeout(@Param("id") UUID id);
}
// Review savollari: qulf qancha vaqt ushlanadi (tranzaksiya oxirigacha),
// uning ichida tashqi chaqiruv bormi (19.2), va qulf tartibi barqarormi
// (15.4 - deadlock).
```

### 27.4 Optimistik yoki pessimistik: tanlov mezoni

| Mezon | Optimistik (`@Version`) | Pessimistik (`FOR UPDATE`) |
| --- | --- | --- |
| Konflikt ehtimoli | Past | Yuqori |
| Foydalanuvchi tajribasi | "Ma'lumot o'zgardi, qayta yuklang" | Kutish |
| Narxi | Konfliktda ish qaytariladi | Qulf va navbat |
| Uzoq tahrirlash (forma) | Mos | Mos emas (qulf soatlab turadi) |
| Qisqa hisob (qoldiq) | Retry ko'p bo'lishi mumkin | Mos |
| Ko'p instans | Ishlaydi | Ishlaydi |

Review qoidasi: foydalanuvchi formasi orqali tahrirlash - optimistik; pul va qoldiq hisobi - atomik `UPDATE` yoki pessimistik qulf; navbat va worker - `SKIP LOCKED`.

### 27.5 Write skew: eng jim poyga

Write skew - ikki tranzaksiya turli qatorlarni o'zgartiradi, lekin birgalikda biznes qoidasini buzadi. `FOR UPDATE` ham bu holda yordam bermaydi, chunki qulflanadigan qator yo'q.

```java
// Qoida: har bir smenada kamida bitta shifokor navbatchi bo'lishi kerak.
@Transactional
public void requestLeave(DoctorId doctor, ShiftId shift) {
    long onCall = schedule.countOnCall(shift);       // T1: 2, T2: 2
    if (onCall <= 1) throw new MinimumStaffingViolated();
    schedule.removeFromShift(doctor, shift);         // T1 va T2 turli qator
}
// Ikki shifokor bir vaqtda ta'til so'rasa: ikkisi ham "2 ta bor" deb
// ko'radi, ikkisi ham o'tadi, va smenada 0 navbatchi qoladi.
// FOR UPDATE yordam bermaydi: ular turli qatorlarni o'zgartiradi.

// Yechim 1: SERIALIZABLE + retry. PostgreSQL buni aniqlaydi (40001).
@Transactional(isolation = Isolation.SERIALIZABLE)
@Retryable(retryFor = CannotAcquireLockException.class, maxAttempts = 3,
           backoff = @Backoff(delay = 50, random = true))
public void requestLeave(DoctorId doctor, ShiftId shift) { ... }
// Review diqqati: retry tranzaksiyadan TASHQARIDA bo'lishi kerak (19.9).

// Yechim 2: umumiy qatorni qulflash - "smena" qatorini qulflash.
Shift s = shifts.lockById(shift);                    // ikkisi ham shu qatorda
long onCall = schedule.countOnCall(shift);
...

// Yechim 3: qoidani bazaga ko'chirish (eng ishonchli, lekin har doim mumkin emas).
-- Hisoblangan ustun + CHECK, yoki trigger, yoki exclusion constraint.
```

### 27.6 SERIALIZABLE ishlatilganda

```java
// SERIALIZABLE da ilova retry ni ko'tarishi SHART - bu majburiy shart.
// PostgreSQL "could not serialize access due to read/write dependencies"
// xatosini beradi (SQLState 40001). Bu xato emas, normal signal.
@Service
public class TransferService {

    @Retryable(retryFor = { CannotSerializeTransactionException.class,
                            CannotAcquireLockException.class },
               maxAttempts = 5,
               backoff = @Backoff(delay = 20, multiplier = 2, random = true))
    public void transfer(TransferCommand cmd) {
        tx.doTransfer(cmd);                     // ichki bean: @Transactional(SERIALIZABLE)
    }

    @Recover
    public void onRepeatedConflict(CannotSerializeTransactionException e, TransferCommand cmd) {
        meter.counter("transfer.serialization.exhausted").increment();
        throw new TemporarilyUnavailable("qayta urinib ko'ring", e);   // 503
    }
}
// Review savollari: retry bormi, backoff da jitter bormi, urinishlar
// tugaganda nima bo'ladi, va bu holat o'lchanadimi (metrika).
// Qo'shimcha: retry qilinadigan operatsiya idempotent bo'lishi kerak -
// aks holda retry ikki marta ta'sir qiladi.
```

### 27.7 Xabar yetkazish: "kamida bir marta" ning oqibatlari

Kafka, RabbitMQ, SQS va outbox - hammasi "kamida bir marta" yetkazadi. "Aniq bir marta" yetkazish amalda iste'molchi tomonidagi idempotentlik bilan quriladi, broker bilan emas.

```java
// Review talabi: iste'molchi dublikatga chidamli bo'lishi kerak.
@KafkaListener(topics = "payments")
@Transactional
public void onPaymentCaptured(PaymentCaptured event, Acknowledgment ack) {
    // 1) Qayta ishlangan xabarlarni belgilash: unique kalit bilan.
    try {
        processed.save(new ProcessedMessage(event.messageId()));
        em.flush();                                  // konflikt shu yerda chiqadi
    } catch (DataIntegrityViolationException dup) {
        log.debug("xabar allaqachon qayta ishlangan: {}", event.messageId());
        ack.acknowledge();                           // dublikat - jim o'tkazamiz
        return;
    }
    // 2) Asosiy ish - bir xil tranzaksiyada.
    orders.applyPayment(event.orderId(), event.amount());
    ack.acknowledge();
}
```

```sql
-- Qayta ishlangan xabarlar jadvali: oyna bilan, cheksiz o'smaydi.
CREATE TABLE processed_message (
    message_id text PRIMARY KEY,
    processed_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX processed_message_at_idx ON processed_message (processed_at);
-- Tozalash: 7 kundan eski yozuvlar (broker retention dan uzunroq bo'lsin).
```

Alternativa - tabiiy idempotentlik: operatsiyaning o'zi takrorlanganda zarar keltirmasligi. `UPDATE orders SET status = 'PAID' WHERE id = ? AND status = 'NEW'` ikki marta bajarilsa, ikkinchisi 0 qator o'zgartiradi. Bu eng toza yechim, lekin har doim mumkin emas.

### 27.8 Xabarlar tartibi

```java
// Review savoli: tartib muhimmi, va u qanday kafolatlanadi?
// Kafka da tartib FAQAT bitta partition ichida kafolatlanadi.
kafkaTemplate.send("orders", order.id().toString(), event);
//                            ^^^^^^^^^^^^^^^^^^^ kalit: bir buyurtmaning
// hamma hodisasi bitta partition ga tushadi, ya'ni tartibda keladi.

// Kalit berilmasa - round-robin, tartib yo'q:
kafkaTemplate.send("orders", event);           // OrderShipped, OrderPaid dan
                                               // oldin kelishi mumkin!

// Review izohi: `OrderPaid` va `OrderShipped` turli partition larga tushsa,
// iste'molchi ularni teskari tartibda qabul qilishi mumkin va buyurtmani
// to'lanmagan holda jo'natilgan deb belgilaydi.
// Yechim: agregat ID ni kalit sifatida ishlatish.

// Qo'shimcha himoya: iste'molchi tomonda tartibdan tashqari xabarni aniqlash.
if (event.version() <= order.lastAppliedVersion()) {
    log.debug("eski yoki takroriy hodisa, o'tkazib yuborildi");
    return;                                    // monotonik versiya tekshiruvi
}
```

### 27.9 Outbox worker review

Outbox naqshi 10.8 da kiritilgan; bu yerda worker tomonidagi review savollari.

```java
@Component
public class OutboxPublisher {

    @Scheduled(fixedDelay = 500)
    @SchedulerLock(name = "outboxPublisher")         // ikki instans emas (15.5)
    public void publish() {
        // SKIP LOCKED: bir necha worker parallel ishlashi mumkin.
        List<OutboxMessage> batch = outbox.lockPendingBatch(100);
        for (OutboxMessage m : batch) {
            try {
                broker.send(m.topic(), m.key(), m.payload());
                outbox.markPublished(m.id());
            } catch (Exception e) {
                outbox.markFailed(m.id(), e.getMessage());   // attempts++
                meter.counter("outbox.failed").increment();
                // Diqqat: bu yerda break qilmaslik kerak - bitta xabar
                // boshqalarni bloklamasligi uchun (poison pill).
            }
        }
    }
}
```

| Review savoli | Nega |
| --- | --- |
| Jadval tozalanadimi | Cheksiz o'sish |
| Ikki instans parallel ishlasa to'g'rimi | `SKIP LOCKED` yoki qulf |
| Bitta xato xabar oqimni bloklaydimi | Poison pill |
| Urinishlar soni cheklanganmi | Cheksiz retry |
| Yetkazilmagan xabarlar uchun alert bormi | Jim yo'qotish |
| Kechikish o'lchanadimi | Eng qadimgi yetkazilmagan xabar yoshi |
| Tartib kerak bo'lsa, ta'minlanganmi | Agregat bo'yicha ketma-ketlik |
| Payload sxemasi versiyalanganmi | Iste'molchi moslik |

```sql
-- Outbox holati uchun monitoring so'rovi: review da shu metrika talab qilinadi.
SELECT count(*) AS kutayotgan,
       max(now() - created_at) AS eng_qadimgi,
       count(*) FILTER (WHERE attempts > 3) AS muammoli
  FROM outbox_message WHERE published_at IS NULL;
-- Alert: eng_qadimgi > 5 daqiqa yoki muammoli > 0.
```

### 27.10 Review checklisti: izolyatsiya va yetkazish

| Savol | Nega |
| --- | --- |
| Tekshir-keyin-yoz naqshi himoyalanganmi | Dublikat |
| Hisoblab yozish atomikmi | Lost update |
| Write skew ehtimoli baholanganmi | Jim qoida buzilishi |
| `SERIALIZABLE` ishlatilsa, retry bormi | 40001 xatosi |
| Retry idempotent operatsiyadami | Ikki marta ta'sir |
| Qulf tartibi barqarormi | Deadlock |
| Qulf ichida tashqi chaqiruv yo'qmi | Uzoq qulf |
| `lock_timeout` qo'yilganmi | Cheksiz kutish |
| Iste'molchi dublikatga chidamlimi | Kamida bir marta yetkazish |
| Xabar kaliti tartibni ta'minlaydimi | Teskari tartib |
| Outbox kechikishi o'lchanadimi | Jim to'xtash |
| Poison pill oqimni bloklamaydimi | To'xtab qolgan iste'molchi |

### 27.11 Amalda qo'llash

- [ ] Barcha yozuv operatsiyalari uchun "o'qish va yozish orasida nima o'zgarishi mumkin" savolini o'tkazib, poyga xavfi bor joylarni ro'yxatga oling.
- [ ] Hisoblagich va qoldiq yangilashlarini atomik `UPDATE` yoki `UPSERT` ga o'tkazing.
- [ ] Write skew ehtimoli bor biznes qoidalarini (minimal shtat, limit, kvota) aniqlab, ularga `SERIALIZABLE` + retry yoki umumiy qator qulfi qo'shing.
- [ ] `SERIALIZABLE` ishlatilgan joylarda retry, jitter, `@Recover` va metrika borligini tasdiqlang.
- [ ] Navbat va worker so'rovlarini `FOR UPDATE SKIP LOCKED` ga o'tkazing.
- [ ] Barcha Kafka produserlarida xabar kaliti agregat ID si ekanini tekshiring.
- [ ] Iste'molchilarda qayta ishlangan xabarlar jadvali yoki tabiiy idempotentlik borligini tasdiqlang va tozalash ishini qo'shing.
- [ ] Outbox uchun kutayotgan xabarlar soni va eng qadimgi xabar yoshi metrikalarini va alertni qo'shing.
- [ ] `lock_timeout` va `deadlock_timeout` qiymatlarini sozlab, deadlock loglarini bir hafta kuzatib boring.

# VI. Xavfsizlik review

## 28. Xavfsizlik review metodikasi (How to Review for Security)

Xavfsizlik review ni "xavfsizlik jamoasining ishi" deb hisoblash eng keng tarqalgan xato. Amalda zaifliklarning katta qismi oddiy kod review da topilishi mumkin, agar reviewer to'g'ri savollarni bersa. Bu bob metodikani beradi: ishonch chegaralarini topish, ma'lumot oqimini kuzatish va zaiflik sinflarini tizimli tekshirish. Keyingi besh bob aniq sinflarni ochadi.

### 28.1 Asosiy savol: ishonilmaydigan ma'lumot qayerga boradi

Xavfsizlik review ning yadrosi bitta savolda: tashqi manbadan kelgan ma'lumot qaysi yo'l bilan xavfli operatsiyaga yetib boradi.

Ishonilmaydigan manbalar (`source`):

| Manba | Ko'pincha e'tibordan chetda qoladigan |
| --- | --- |
| HTTP so'rov tanasi, parametrlar, yo'l | - |
| HTTP header lar | `Host`, `X-Forwarded-For`, `Referer`, `User-Agent` |
| Cookie va token tarkibi | JWT claim lari (imzolangan, lekin ma'nosi tekshirilmagan) |
| Fayl nomi va tarkibi | Yuklangan fayl metadata si |
| Boshqa servis javobi | "Ichki servis" ham buzilgan bo'lishi mumkin |
| Kafka xabari | Produser buzilgan yoki xato yuborgan |
| Ma'lumotlar bazasidagi qiymat | Avval ishonilmagan manbadan kelgan (ikkilamchi injection) |
| Muhit o'zgaruvchisi va konfiguratsiya | Konteyner buzilgan holat |
| Fayl tizimidagi fayl | Umumiy hajm (shared volume) |

Xavfli operatsiyalar (`sink`):

| Operatsiya | Zaiflik sinfi |
| --- | --- |
| SQL yoki JPQL qurish | Injection (29-bob) |
| Buyruq bajarish (`ProcessBuilder`) | Command injection |
| Fayl yo'li qurish | Path traversal |
| URL qurish va so'rov yuborish | SSRF |
| Deserializatsiya | RCE |
| Shablon yoki ifoda bajarish (SpEL, Thymeleaf) | Expression injection |
| HTML yoki JS ga chiqarish | XSS |
| LDAP yoki XPath so'rovi | Injection |
| Log yozish | Log injection, ma'lumot oqishi |
| Avtorizatsiya qarori | Huquq oshirish |
| Redirect manzili | Open redirect |

Review usuli: diffda yangi sink paydo bo'lsa, uning kirishini orqaga kuzatish; yangi source paydo bo'lsa, u qayerga borishini oldinga kuzatish. Ikki uchi ishonilmaydigan manba va xavfli operatsiyada tutashsa - zaiflik.

### 28.2 Ishonch chegarasi diffda

```java
// Chegara qayerda: shu metodga kelgan ma'lumot tekshirilganmi?
// Review da har bir public metod uchun javob kerak.

// Chegara 1: HTTP controller - ishonilmaydigan kirish.
@PostMapping("/orders")
public OrderResponse create(@Valid @RequestBody CreateOrderRequest req,
                            @AuthenticationPrincipal AppUser user) {
    // Bu nuqtadan keyin: req shakli tekshirilgan (@Valid), user autentifikatsiya
    // qilingan. LEKIN: req ichidagi ID lar user ga tegishliligi TEKSHIRILMAGAN.
    return orders.place(req.toCommand(user.id()));
}

// Chegara 2: Kafka listener - ishonilmaydigan kirish.
@KafkaListener(topics = "orders")
public void on(OrderEvent event) {
    // Bu ham ishonilmaydigan kirish: sxema tekshirilgan, mazmun emas.
}

// Chegara 3: ichki servis chaqiruvi - shartli ishonch.
public void applyDiscount(OrderId id, Percentage discount) {
    // Bu metod ichki, lekin kim chaqirishini bilmaydi. Agar u 100%
    // chegirma qabul qilsa va chaqiruvchi tekshirmasa - muammo.
    // Review savoli: cheklov qayerda - bu yerda yoki chaqiruvchida?
}
```

### 28.3 Tez tekshirish ro'yxati: har PR uchun o'n savol

1. Yangi endpoint bormi, va u autentifikatsiya talab qiladimi.
2. Yangi endpoint foydalanuvchi ma'lumotini qaytaradimi, va egalik tekshirilganmi.
3. Foydalanuvchi identifikatori so'rovdan olinganmi (olinmasligi kerak).
4. Tashqi ma'lumot SQL, fayl yo'li, URL yoki buyruqqa tushadimi.
5. Yangi bog'liqlik qo'shilganmi, uning CVE holati qanday.
6. Logga yangi narsa yoziladimi, unda maxfiy ma'lumot bormi.
7. Xato javobida ichki detallar bormi.
8. Yangi konfiguratsiya secret ni ochib qo'ymaydimi.
9. Deserializatsiya, shablon, ifoda bajarilishi bormi.
10. Keshlangan yoki umumiy holatga foydalanuvchi ma'lumoti tushadimi.

```bash
# Shu ro'yxatni diffda avtomatik tez skanerlash.
FILES=$(git diff --name-only origin/main...HEAD)
D=$(git diff origin/main...HEAD)

echo "=== yangi endpointlar ==="
echo "$D" | grep -E '^\+.*@(Get|Post|Put|Delete|Patch|Request)Mapping'

echo "=== avtorizatsiya annotatsiyalari ==="
echo "$D" | grep -E '^\+.*@(PreAuthorize|PostAuthorize|Secured|RolesAllowed)'

echo "=== xavfli sink lar ==="
echo "$D" | grep -nE '^\+.*(createQuery\(|createNativeQuery\(|queryForList\(|\.execute\(|ProcessBuilder|Runtime\.getRuntime|new File\(|Paths\.get\(|new URL\(|URI\.create\(|readObject|parseExpression|SpelExpression)'

echo "=== so'rovdan kelgan qiymat bilan satr qurish ==="
echo "$D" | grep -nE '^\+.*(RequestParam|PathVariable|RequestHeader).*' | head
echo "$D" | grep -nE '^\+.*(\"\s*\+\s*[a-zA-Z]|\.formatted\(|String\.format\()' | head

echo "=== secret va token ==="
echo "$D" | grep -niE '^\+.*(password|secret|token|api[_-]?key|private[_-]?key)\s*[:=]'

echo "=== logga obyekt yozish ==="
echo "$D" | grep -nE '^\+.*log\.(info|debug|warn|error)\(.*(request|user|token|card|password)'

echo "=== xavfsizlik konfiguratsiyasi ==="
echo "$D" | grep -nE '^\+.*(permitAll|csrf\(\)|\.disable\(\)|anonymous\(\)|cors\(\)|hasRole|authenticated\(\))'
```

### 28.4 Zaiflik sinflarini tizimli ko'rish

Review ni to'liq qilish uchun sinflar bo'yicha o'tish kerak, aks holda faqat tanish zaifliklar topiladi.

| Sinf | Spring/Java kontekstida | Bob |
| --- | --- | --- |
| Buzilgan kirish nazorati | `@PreAuthorize` yo'qligi, IDOR | 30 |
| Injection | SQL, JPQL, dinamik `ORDER BY`, SpEL | 29 |
| Autentifikatsiya kamchiliklari | JWT tekshiruvi, sessiya, parol siyosati | 30 |
| Xavfsiz bo'lmagan dizayn | Biznes mantiqini chetlab o'tish, narx manipulyatsiyasi | 30 |
| Noto'g'ri konfiguratsiya | Actuator, CORS, CSRF, standart parollar | 21, 30 |
| Zaif bog'liqliklar | CVE, eskirgan kutubxonalar | 33 |
| Ma'lumot oqishi | Log, xato javobi, ortiqcha maydonlar | 32 |
| Kriptografik xatolar | Zaif algoritm, tasodif, kalit boshqaruvi | 32 |
| SSRF | URL ni kirishdan qurish | 31 |
| Deserializatsiya | Jackson polimorfizmi, `ObjectInputStream` | 31 |
| Fayl operatsiyalari | Path traversal, zip slip, upload | 31 |
| Yetarsiz log va monitoring | Hujumni ko'rmaslik | 39 |
| DoS | Chegarasiz so'rov, regex, arxiv bombasi | 20, 31 |

### 28.5 Xavfsizlik izohining shakli

Xavfsizlik izohi boshqa izohlardan farq qiladi: u ko'pincha blocker bo'ladi, va uning asoslanishi aniq bo'lishi kerak - aks holda u "paranoyya" deb qabul qilinadi.

```text
# Yomon shakl: nom bilan qo'rqitish.
"Bu SQL injection, tuzatish kerak."

# Yaxshi shakl: yo'l, ta'sir, tuzatish.
blocker (xavfsizlik): ReportService.build() da sortBy parametri
to'g'ridan-to'g'ri ORDER BY ga qo'yilgan.

Yo'l: GET /reports?sortBy=... -> ReportController.build() ->
      ReportService.build() -> jdbc.queryForList(sql)
      Parametr hech qayerda tekshirilmaydi va whitelist yo'q.

Ta'sir: hujumchi ORDER BY o'rniga ifoda qo'yib, boshqa jadvallardan
ma'lumot chiqarib olishi mumkin. Masalan:
  ?sortBy=(SELECT password_hash FROM app_user LIMIT 1)
Bu xatolik xabari orqali yoki tartiblash natijasi orqali ma'lumot
beradi. Jadvalda 40 ming foydalanuvchi bor.

Tuzatish: ruxsat etilgan ustunlar enum i (quyida namuna). O'zgarish
hajmi: 1 enum + 3 satr.

  public enum OrderSort {
      CREATED_AT("o.created_at DESC"), TOTAL("o.total DESC");
      private final String sql;
      public static OrderSort of(String raw) {
          return Arrays.stream(values())
              .filter(v -> v.name().equalsIgnoreCase(raw))
              .findFirst().orElse(CREATED_AT);
      }
  }
```

### 28.6 Xavfsizlik uchun avtomatlashtirish va uning chegarasi

| Instrument | Nimani topadi | Nimani topmaydi |
| --- | --- | --- |
| Sonar / SpotBugs (SAST) | Ma'lum naqshlar: konkatenatsiya, zaif tasodif | Avtorizatsiya mantiqi, biznes qoidasi |
| Semgrep (custom qoidalar) | Loyihaga xos naqshlar | Kontekst va niyat |
| Dependency scanning | Ma'lum CVE lar | Noto'g'ri ishlatilgan xavfsiz kutubxona |
| Secret scanning | Koddagi kalitlar | Noto'g'ri saqlangan secret |
| DAST / pentest | Ishlaydigan tizimdagi zaifliklar | Kod darajasidagi sabab |
| Kod review | Avtorizatsiya, mantiq, kontekst | Konfiguratsiya va infratuzilma |

Asosiy xulosa: avtomatik instrumentlar injection va CVE larni yaxshi topadi, lekin kirish nazorati xatolarini - zaifliklarning eng ko'p uchraydigan sinfini - deyarli topmaydi. Chunki "bu foydalanuvchi shu buyurtmani ko'rishi kerakmi" degan savolga javob faqat domen bilimida bor. Shu sababli reviewer ning asosiy e'tibori 30-bobga qaratiladi.

```yaml
# Loyihaga xos xavfsizlik qoidasi: Semgrep bilan.
# .semgrep/dynamic-order-by.yml
rules:
  - id: dynamic-order-by
    languages: [java]
    severity: ERROR
    message: >
      ORDER BY ga o'zgaruvchi qo'shilgan. Ruxsat etilgan ustunlar enum i
      ishlatilishi kerak (REVIEW.md: xavfsizlik, 29-bob).
    patterns:
      - pattern-either:
          - pattern: |
              "$...ORDER BY" + $VAR
          - pattern: |
              $SB.append("ORDER BY").append($VAR)
```

### 28.7 Xavfsizlik review ni jarayonga kiritish

| Mexanizm | Nima qiladi |
| --- | --- |
| `CODEOWNERS` da xavfsizlik yo'llari | Auth, crypto, to'lov kodiga majburiy reviewer |
| PR shablonida xavfsizlik bo'limi | Muallif o'zi savol beradi |
| Yuqori xavfli yo'llar ro'yxati | Chuqur review darajasi |
| Threat model (bir sahifa) | Nimadan himoyalanamiz |
| Incident dan o'rganish | Katalogga yangi band (12.10) |
| Muntazam skanerlash | CVE va secret |

```markdown
<!-- .github/pull_request_template.md ichidagi xavfsizlik bo'limi -->
## Xavfsizlik

- [ ] Yangi endpoint yo'q, yoki bor va avtorizatsiya qoidasi yozilgan
- [ ] Tashqi ma'lumot SQL, fayl yo'li, URL yoki buyruqqa tushmaydi
- [ ] Foydalanuvchi faqat o'z ma'lumotini ko'radi (ID so'rovdan olinmaydi)
- [ ] Logga maxfiy ma'lumot yozilmaydi
- [ ] Yangi bog'liqlik yo'q, yoki bor va CVE tekshirilgan
- [ ] Xato javobida ichki detallar yo'q
```

### 28.8 Amalda qo'llash

- [ ] `scripts/review-security-scan.sh` skriptini qo'shib, uni har PR da ishga tushirishni odat qiling.
- [ ] Loyihadagi barcha ishonilmaydigan manbalar va xavfli operatsiyalar ro'yxatini bir sahifada yozing.
- [ ] O'n savolli tez ro'yxatni PR shabloniga qo'shing.
- [ ] `CODEOWNERS` da autentifikatsiya, avtorizatsiya, to'lov va kriptografiya yo'llariga majburiy reviewer belgilang.
- [ ] Loyihaga xos uchta xavfsizlik naqshini Semgrep qoidasiga aylantirib, CI ga qo'shing.
- [ ] Bir sahifali threat model yozing: kim hujum qiladi, nimaga, qanday himoya bor.
- [ ] Oxirgi uchta xavfsizlik topilmasini `REVIEW-SMELLS.md` ga "qanday qidiramiz" ustuni bilan qo'shing.
- [ ] Zaiflik sinflari jadvalini review checklistiga kiritib, har chorakda bitta sinf bo'yicha maqsadli audit o'tkazing.

## 29. Injection review: SQL va boshqalar (Injection)

SQL injection eng qadimgi zaiflik sinfi, lekin u hali ham topiladi - chunki parametrlashtirish qoidasi bir joyda buzilsa yetarli. Spring va JPA ko'p holatda himoya beradi, lekin ularda ham teshiklar bor: so'rovning strukturaviy qismi (ustun nomi, tartib, jadval) parametr bo'la olmaydi, va aynan shu yerda xatolar to'planadi. Bu bob SQL injection ning Java/Spring dagi hamma yo'lini va qolgan injection sinflarini ko'radi.

### 29.1 Parametrlashtirish: nima parametr bo'la oladi

Bu farqni tushunmaslik barcha SQL injection larning sababi.

| So'rov qismi | Parametr bo'la oladimi | Xavfsiz yo'l |
| --- | --- | --- |
| Qiymat (`WHERE id = ?`) | Ha | `?` yoki `:name` |
| Qiymatlar ro'yxati (`IN`) | Ha | `= ANY(?)` massiv yoki `IN (:ids)` |
| `LIKE` naqshi | Ha (qiymat sifatida) | Parametr + escape |
| `LIMIT`/`OFFSET` | Ha | Parametr yoki tekshirilgan butun son |
| Ustun nomi | Yo'q | Whitelist (enum) |
| Jadval nomi | Yo'q | Whitelist |
| `ORDER BY` ifodasi | Yo'q | Whitelist (enum) |
| `ASC`/`DESC` | Yo'q | Enum |
| Operator (`>`, `<`) | Yo'q | Enum |
| Sxema nomi | Yo'q | Whitelist |

```java
// Eng ko'p uchraydigan zaiflik: tartiblash va yo'nalish.
// Zaif:
String sql = "SELECT * FROM orders ORDER BY " + sortBy + " " + direction;

// Xavfsiz: ikkisi ham enum, foydalanuvchi qiymati kodga aylanadi.
public enum OrderSortColumn {
    CREATED_AT("o.created_at"), TOTAL("o.total"), NUMBER("o.number");
    private final String sql;
    OrderSortColumn(String sql) { this.sql = sql; }
    public String sql() { return sql; }
    public static OrderSortColumn of(String raw) {
        for (OrderSortColumn c : values()) {
            if (c.name().equalsIgnoreCase(raw)) return c;
        }
        return CREATED_AT;                      // xavfsiz standart
    }
}
public enum SortDirection { ASC, DESC;
    public static SortDirection of(String raw) {
        return "desc".equalsIgnoreCase(raw) ? DESC : ASC;
    }
}
// Ishlatilishi: tashqi satr hech qachon SQL ga tushmaydi.
String sql = "SELECT id, number, total FROM orders ORDER BY %s %s LIMIT :limit"
    .formatted(OrderSortColumn.of(sortBy).sql(), SortDirection.of(direction));
```

### 29.2 Spring Data da injection yo'llari

Spring Data xavfsiz deb hisoblanadi, lekin uchta teshigi bor.

```java
// Teshik 1: nativeQuery da konkatenatsiya (odatda SpEL yoki satr bilan).
@Query(value = "SELECT * FROM orders WHERE status = '?1'", nativeQuery = true)
List<Order> byStatus(String status);
// Diqqat: qo'shtirnoq ichidagi ?1 PARAMETR EMAS - u satr literali ichida
// va JDBC uni parametr deb ko'rmaydi. To'g'risi: qo'shtirnoqsiz `?1`.

// Teshik 2: SpEL ifodasi orqali qiymat qo'yish.
@Query(value = "SELECT * FROM #{#entityName} WHERE name = :#{#filter.name}",
       nativeQuery = true)
// SpEL natijasi SQL matniga QO'SHILADI, parametr sifatida emas -
// ya'ni bu injection yo'li. Parametrlar uchun oddiy `:name` ishlatiladi.

// Teshik 3: Sort va Pageable orqali.
repository.findAll(PageRequest.of(0, 20, Sort.by(userProvidedField)));
// Spring Data `Sort` da property nomini tekshiradi (entity maydonlari
// bilan solishtiradi) - shuning uchun bu nisbatan xavfsiz. LEKIN
// `JpaSort.unsafe(...)` tekshiruvni chetlab o'tadi:
Sort.by(JpaSort.unsafe("(SELECT ...)"));        // injection - nomi ham shuni aytadi
// Review qoidasi: `JpaSort.unsafe` loyihada taqiqlanadi.

// Xavfsiz shakl: ro'yxatlar uchun.
@Query("select o from Order o where o.status in :statuses")
List<Order> byStatuses(@Param("statuses") Collection<OrderStatus> statuses);
// PostgreSQL massiv bilan (ko'p elementda tezroq, reja barqaror):
@Query(value = "SELECT * FROM orders WHERE id = ANY(:ids)", nativeQuery = true)
List<Order> byIds(@Param("ids") UUID[] ids);
```

### 29.3 JdbcTemplate va JdbcClient

```java
// Zaif: queryForList satr bilan.
jdbc.queryForList("SELECT * FROM orders WHERE number = '" + number + "'");

// Xavfsiz: parametrlar.
jdbc.queryForList("SELECT * FROM orders WHERE number = ?", number);

// Spring 6.1+ JdbcClient: o'qiladigan va xavfsiz.
List<OrderRow> rows = jdbcClient
    .sql("""
         SELECT id, number, total FROM orders
          WHERE customer_id = :customerId
            AND created_at >= :from
          ORDER BY created_at DESC
          LIMIT :limit
         """)
    .param("customerId", customerId)
    .param("from", from)
    .param("limit", Math.min(limit, 100))
    .query(OrderRow.class)
    .list();

// LIKE bilan ishlash: foydalanuvchi kiritgan `%` va `_` ni escape qilish.
String pattern = search.replace("\\", "\\\\")
                       .replace("%", "\\%")
                       .replace("_", "\\_");
jdbc.queryForList("SELECT * FROM customer WHERE name LIKE ? ESCAPE '\\'",
                  "%" + pattern + "%");
// Escape qilinmasa: injection emas, lekin `%` bilan butun jadval
// skanerlanadi - DoS yo'li (31.8).
```

### 29.4 Ikkilamchi injection (second-order)

Eng ko'p e'tibordan chetda qoladigan shakl: ma'lumot avval bazaga xavfsiz yoziladi, keyin undan so'rov quriladi.

```java
// 1-qadam: foydalanuvchi "filtr" saqlaydi - parametr bilan, xavfsiz.
jdbc.update("INSERT INTO saved_filter (user_id, expr) VALUES (?, ?)", userId, expr);

// 2-qadam: saqlangan filtr so'rovga qo'shiladi - zaiflik shu yerda.
String expr = jdbc.queryForObject(
    "SELECT expr FROM saved_filter WHERE id = ?", String.class, filterId);
List<Map<String,Object>> rows = jdbc.queryForList(
    "SELECT * FROM orders WHERE " + expr);      // injection!

// Review qoidasi: bazadan kelgan qiymat ham ishonilmaydigan ma'lumot,
// agar u avval tashqaridan kelgan bo'lsa. Yechim: filtrni strukturaviy
// shaklda saqlash (JSON: maydon, operator, qiymat) va uni whitelist
// bo'yicha SQL ga aylantirish.
public record FilterCriterion(FilterField field, FilterOp op, String value) { }
// field va op - enum, value - parametr. Injection yo'li yo'q.
```

### 29.5 SQL dan tashqari injection sinflari

```java
// 1) Command injection: shell orqali bajarish.
Runtime.getRuntime().exec("convert " + fileName + " out.png");     // zaif
// Xavfsiz: shell yo'q, argumentlar massiv sifatida.
new ProcessBuilder("convert", fileName, "out.png").start();
// Lekin fileName hali ham tekshirilishi kerak: "-write" kabi flaglar
// bilan boshlangan nom ImageMagick uchun buyruqqa aylanadi.
if (!fileName.matches("[A-Za-z0-9._-]{1,100}")) throw new InvalidFileName();

// 2) SpEL injection: eng xavfli, chunki RCE beradi.
ExpressionParser parser = new SpelExpressionParser();
parser.parseExpression(userInput).getValue();                       // RCE!
// Review qoidasi: foydalanuvchi kiritgan SpEL hech qachon bajarilmaydi.
// @PreAuthorize ichida ham ehtiyot: @PreAuthorize("hasRole('" + role + "')")
// shaklidagi dinamik qurish xavfli.

// 3) Log injection va forging.
log.info("Foydalanuvchi kirdi: " + username);
// username = "admin\n2026-10-04 12:00:00 INFO Foydalanuvchi kirdi: root"
// Natija: logda yolg'on yozuv. JSON log formati bu muammoni yo'q qiladi.
log.info("Foydalanuvchi kirdi: {}", username);   // structured, xavfsizroq

// 4) Header injection (CRLF).
response.setHeader("X-Trace", userValue);        // \r\n bo'lsa yangi header
// Spring zamonaviy versiyalarida bu bloklangan, lekin qo'lda yozilgan
// javoblarda tekshirish kerak.

// 5) Open redirect.
return "redirect:" + request.getParameter("next");                  // zaif
// Xavfsiz: nisbiy yo'llar yoki whitelist.
if (!next.startsWith("/") || next.startsWith("//")) next = "/";

// 6) XSS: API da ham muhim.
// JSON javob odatda xavfsiz, LEKIN:
//  - `Content-Type: text/html` bilan qaytarilsa - XSS;
//  - frontend `innerHTML` ga qo'ysa - XSS;
//  - PDF yoki email shabloniga qo'shilsa - shablon injection.
// Review savoli: bu qiymat qayerda ko'rsatiladi va u yerda escape qilinadimi?
```

### 29.6 Shablon va hisobot injectionlari

```java
// Thymeleaf: ifoda injectioni mumkin.
// Zaif: shablon nomi foydalanuvchidan.
return "redirect:" + page;                       // yoki
return userProvidedTemplateName;                 // SSTI yo'li
// Review qoidasi: shablon nomi faqat kod ichidagi konstantalardan.

// Thymeleaf da matn chiqarish:
// th:text  - escape qiladi (xavfsiz)
// th:utext - escape QILMAYDI (xavfli, faqat ishonchli HTML uchun)
// Review da har `th:utext` uchun savol: bu kontent qayerdan keladi?

// CSV injection (formula injection): Excel da ochilganda bajariladi.
// Foydalanuvchi ismi "=cmd|'/c calc'!A1" bo'lsa, eksport qilingan CSV
// Excel da ochilganda buyruq bajarilishi mumkin.
static String csvSafe(String value) {
    if (value == null) return "";
    // =, +, -, @, tab, CR bilan boshlangan qiymatni neytrallash.
    if (value.matches("^[=+\\-@\\t\\r].*")) return "'" + value;
    return value;
}
```

### 29.7 Review paytida injection ni qidirish

```bash
# Injection xavfini tizimli qidirish.
SRC=src/main/java

echo "=== SQL satr qurish ==="
grep -rnE '("(SELECT|INSERT|UPDATE|DELETE|WHERE|ORDER BY|FROM)[^"]*"\s*\+|\+\s*"\s*(WHERE|AND|OR|ORDER))' $SRC

echo "=== formatted va String.format bilan SQL ==="
grep -rnE '(SELECT|UPDATE|DELETE|INSERT)[^;]*(\.formatted\(|String\.format\()' $SRC

echo "=== nativeQuery va createNativeQuery ==="
grep -rnE 'nativeQuery\s*=\s*true|createNativeQuery\(|createQuery\(' $SRC

echo "=== JpaSort.unsafe - har doim taqiqlanadi ==="
grep -rn 'JpaSort.unsafe' $SRC

echo "=== SpEL va ifoda bajarish ==="
grep -rnE 'SpelExpressionParser|parseExpression|ExpressionParser|ScriptEngine' $SRC

echo "=== buyruq bajarish ==="
grep -rnE 'Runtime\.getRuntime\(\)\.exec|new ProcessBuilder' $SRC

echo "=== th:utext (escape qilinmagan HTML) ==="
grep -rn 'th:utext' src/main/resources/templates 2>/dev/null

echo "=== ORDER BY ga o'zgaruvchi ==="
grep -rnE 'ORDER BY"\s*\+|append\("ORDER BY"\)' $SRC
```

### 29.8 Himoyani test bilan qulflash

```java
// Injection himoyasini test bilan tasdiqlash: review izohidan ko'ra ishonchli.
@ParameterizedTest
@ValueSource(strings = {
    "created_at; DROP TABLE orders",
    "(SELECT password_hash FROM app_user LIMIT 1)",
    "1 UNION SELECT NULL, password_hash, NULL FROM app_user",
    "created_at/**/DESC,(SELECT 1)",
    "../../etc/passwd"
})
void malformedSortIsRejectedOrIgnored(String evilSort) {
    // Natija: xato yoki standart tartib. Hech qanday holatda ham
    // so'rov bajarilmasligi va ma'lumot chiqmasligi kerak.
    assertThatCode(() -> service.list(evilSort))
        .doesNotThrowAnyException();
    assertThat(service.list(evilSort))
        .as("standart tartibga tushishi kerak")
        .isEqualTo(service.list("created_at"));
}

// Injection himoyasi arxitektura testi bilan: yangi joyda takrorlanmasligi.
@ArchTest
static final ArchRule no_string_concatenation_in_queries =
    noClasses().should().callMethodWhere(
        JavaCall.Predicates.target(nameMatching("createNativeQuery")))
        .because("native so'rovlar faqat repository qatlamida va parametrlar bilan");
```

### 29.9 Review checklisti: injection

| Savol | Nega |
| --- | --- |
| SQL satr konkatenatsiyasi bormi | Injection |
| `ORDER BY`, ustun, jadval nomi whitelist dami | Parametr bo'la olmaydi |
| `nativeQuery` da parametrlar to'g'ri ishlatilganmi | Qo'shtirnoq ichidagi `?1` parametr emas |
| `JpaSort.unsafe` ishlatilmaganmi | Tekshiruvni chetlab o'tish |
| SpEL yoki skript foydalanuvchi kirishi bilan bajarilmaydimi | RCE |
| `exec` shell orqali chaqirilmaydimi | Command injection |
| `LIKE` naqshi escape qilinganmi | DoS va kutilmagan natija |
| Bazadan kelgan qiymat so'rovga qo'shilmaydimi | Ikkilamchi injection |
| `th:utext` va HTML chiqarish xavfsizmi | XSS |
| CSV eksportda formula neytrallanganmi | CSV injection |
| Redirect manzili tekshirilganmi | Open redirect |
| Himoya test bilan qulflangangmi | Regressiya |

### 29.10 Amalda qo'llash

- [ ] Injection qidiruv skriptini ishga tushirib, topilgan har bir joy uchun kirish manbasini kuzatib chiqing.
- [ ] Barcha dinamik tartiblash joylarini enum whitelist ga o'tkazing.
- [ ] `JpaSort.unsafe` ni ArchUnit yoki Semgrep qoidasi bilan taqiqlang.
- [ ] `nativeQuery` ishlatilgan barcha so'rovlarda parametrlar qo'shtirnoq ichida emasligini tekshiring.
- [ ] `LIKE` ishlatadigan qidiruvlarda escape va minimal uzunlik talabini qo'shing.
- [ ] Saqlanadigan filtr yoki ifoda bo'lsa, uni strukturaviy shaklga (enum + parametr) o'tkazing.
- [ ] CSV va Excel eksportida formula neytrallash funksiyasini qo'shing.
- [ ] Injection himoyasi uchun parametrlashtirilgan testni yozib, zararli kirish namunalarini CI ga kiriting.

## 30. Autentifikatsiya va avtorizatsiya review (Authentication and Authorization)

Kirish nazorati xatolari zaifliklarning eng ko'p uchraydigan sinfi, va avtomatik instrumentlar ularni deyarli topmaydi. Sababi: "bu foydalanuvchi shu ma'lumotni ko'rishi kerakmi" degan savolga javob faqat domen bilimida bor. Shu sababli bu bob reviewer ning eng muhim xavfsizlik vazifasi haqida.

### 30.1 IDOR: eng ko'p uchraydigan va eng oson o'tib ketadigan xato

```java
// Zaiflik: ID so'rovdan keladi, egalik tekshirilmaydi.
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id) {
    return OrderResponse.from(orders.findById(id).orElseThrow());
}
// Har qanday autentifikatsiya qilingan foydalanuvchi boshqa odamning
// buyurtmasini ko'radi. `@PreAuthorize("isAuthenticated()")` bu yerda
// hech narsa bermaydi - u faqat "kirgan" ekanini tekshiradi.

// Yechim 1 (eng ishonchli): so'rovda egalik sharti.
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id, @AuthenticationPrincipal AppUser user) {
    return orders.findByIdAndCustomerId(id, user.customerId())
                 .map(OrderResponse::from)
                 .orElseThrow(OrderNotFound::new);     // 404, 403 emas
}
// Nega 404: 403 "bu buyurtma bor, lekin sizga tegishli emas" degan
// ma'lumot beradi - bu enumeratsiya uchun foydali signal.

// Yechim 2: aniq avtorizatsiya tekshiruvi (murakkab qoidalar uchun).
@PreAuthorize("@orderAccess.canRead(#id, authentication)")
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id) { ... }

@Component("orderAccess")
public class OrderAccessPolicy {
    public boolean canRead(UUID orderId, Authentication auth) {
        AppUser user = (AppUser) auth.getPrincipal();
        if (user.hasRole("SUPPORT")) return true;              // qo'llab-quvvatlash
        return orders.existsByIdAndCustomerId(orderId, user.customerId());
    }
}
```

Review usuli: har bir endpoint uchun "bu resursni kim ko'rishi kerak" va "kod shuni qanday ta'minlaydi" savollari. Javob "`isAuthenticated()`" bo'lsa va resurs foydalanuvchiga tegishli bo'lsa - zaiflik.

### 30.2 Foydalanuvchi identifikatori qayerdan keladi

```java
// Blocker: foydalanuvchi o'z identifikatorini aytadi.
@PostMapping("/transfers")
public void transfer(@RequestBody TransferRequest req) {
    accounts.transfer(req.fromAccountId(), req.toAccountId(), req.amount());
}
// Hujumchi `fromAccountId` ga boshqa odamning hisobini qo'yadi.

// To'g'ri: identifikator autentifikatsiya kontekstidan, so'rovdan emas.
@PostMapping("/transfers")
public void transfer(@RequestBody @Valid TransferRequest req,
                     @AuthenticationPrincipal AppUser user) {
    // Hisob foydalanuvchiga tegishliligi tekshiriladi.
    Account from = accounts.findByIdAndOwner(req.fromAccountId(), user.id())
                           .orElseThrow(AccountNotFound::new);
    accounts.transfer(from.id(), req.toAccountId(), req.amount());
}
```

| So'rovdan olinmasligi kerak | Qayerdan olinadi |
| --- | --- |
| `userId`, `customerId` | `Authentication` principal |
| `tenantId` | Token claim yoki domen (subdomen) |
| Rol va huquqlar | Token yoki bazadan |
| Narx va chegirma | Serverda hisoblanadi |
| Buyurtma summasi | Serverda qatorlardan hisoblanadi |
| Status va holat | Server qoidasi bilan |
| `isAdmin` kabi bayroqlar | Hech qachon mijozdan |

### 30.3 Spring Security konfiguratsiyasi review

```java
// Review da diqqat bilan o'qiladigan kod: qoidalar tartibi muhim.
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a
            // DIQQAT: tartib muhim - birinchi mos kelgan qoida ishlaydi.
            .requestMatchers("/api/public/**").permitAll()
            .requestMatchers(HttpMethod.GET, "/api/orders/**").hasRole("USER")
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())          // standart: yopiq
        .csrf(csrf -> csrf.disable())               // nega? (quyida)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}
```

Review savollari shu konfiguratsiya uchun:

| Savol | Xavf |
| --- | --- |
| `anyRequest().authenticated()` oxirida bormi | Yangi endpoint himoyasiz ochiladi |
| `permitAll` naqshlari tor emasmi | `/api/**` ochiq qolishi |
| Qoidalar tartibi to'g'rimi | Keng qoida torini soya qiladi |
| `csrf.disable()` asoslanganmi | Sessiya bilan ishlasa - CSRF xavfi |
| Metod bo'yicha farq hisobga olinganmi | `GET` ochiq, `POST` yopiq |
| `permitAll` da `/actuator` yo'qmi | Diagnostika oshkor (21.7) |
| JWT tekshiruvi to'liqmi | Imzo, muddat, issuer, audience |
| Standart `anonymous` xulqi tushunilganmi | Autentifikatsiyasiz kirish |

```java
// CSRF: qachon o'chirish mumkin.
// - Agar autentifikatsiya FAQAT `Authorization` header orqali bo'lsa
//   (JWT, Bearer) - CSRF xavfi yo'q, o'chirish mumkin.
// - Agar cookie da sessiya yoki token bo'lsa - CSRF KERAK.
// Review izohi: "csrf disabled" bilan "cookie da token" birga bo'lsa -
// bu blocker. Cookie ni `SameSite=Strict` qilish qo'shimcha himoya,
// lekin yetarli emas.
```

### 30.4 Metod darajasidagi xavfsizlik

```java
// @PreAuthorize ning tipik xatolari.

// Xato 1: faqat autentifikatsiya tekshirilgan.
@PreAuthorize("isAuthenticated()")              // IDOR dan himoya qilmaydi

// Xato 2: rol tekshirilgan, egalik emas.
@PreAuthorize("hasRole('USER')")                // har qanday USER kira oladi

// Xato 3: `hasAuthority` va `hasRole` chalkashtirilgan.
@PreAuthorize("hasAuthority('ADMIN')")          // "ROLE_ADMIN" ni topmaydi
@PreAuthorize("hasRole('ADMIN')")               // "ROLE_" prefiksini o'zi qo'shadi

// Xato 4: annotatsiya proxy orqali o'tmaydigan joyda (18.1).
// private metod yoki shu klass ichidan chaqiruv - tekshiruv ishlamaydi.

// Xato 5: `@PostAuthorize` bilan ma'lumot allaqachon o'qilgan.
@PostAuthorize("returnObject.customerId == authentication.principal.customerId")
public Order find(UUID id) { ... }
// Ishlaydi, lekin: (1) ma'lumot bazadan o'qilgan va loglarda bo'lishi
// mumkin; (2) yon ta'sirli metodda kech bo'ladi; (3) ro'yxatlar uchun
// ishlamaydi. Afzal: so'rovda filtrlash.

// To'g'ri shakl: domen policy bean i, test bilan qoplangan.
@PreAuthorize("@orderAccess.canModify(#id, authentication)")
public void cancel(UUID id, String reason) { ... }
```

```java
// Avtorizatsiya qoidalarini test bilan qoplash: review ning talabi.
@SpringBootTest
@AutoConfigureMockMvc
class OrderAuthorizationTest {

    @Test
    @WithMockUser(username = "ali", roles = "USER")
    void userCannotReadAnotherCustomersOrder() throws Exception {
        UUID otherOrder = seedOrderFor("vali");
        mvc.perform(get("/api/orders/{id}", otherOrder))
           .andExpect(status().isNotFound());      // 404, 403 emas
    }

    @Test
    void anonymousIsRejected() throws Exception {
        mvc.perform(get("/api/orders/{id}", UUID.randomUUID()))
           .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "USER")
    void userCannotAccessAdminEndpoints() throws Exception {
        mvc.perform(post("/api/admin/refunds"))
           .andExpect(status().isForbidden());
    }
}
```

### 30.5 Himoyasiz qolgan endpointlarni topish

```java
// Eng foydali test: har bir endpoint himoyalanganini tekshirish.
// Yangi endpoint qo'shilib, avtorizatsiya yozilmasa - CI gapiradi.
@SpringBootTest
class EndpointSecurityCoverageTest {

    @Autowired RequestMappingHandlerMapping mappings;

    // Ongli ravishda ochiq qoldirilgan yo'llar - aniq ro'yxat.
    private static final Set<String> PUBLIC = Set.of(
        "/api/public/health", "/api/public/version", "/api/auth/login");

    @Test
    void everyEndpointIsEitherPublicOrSecured() {
        List<String> unprotected = new ArrayList<>();
        mappings.getHandlerMethods().forEach((info, method) -> {
            String path = info.getPathPatternsCondition().getPatternValues()
                              .stream().findFirst().orElse("?");
            if (PUBLIC.contains(path)) return;
            boolean hasMethodSecurity =
                method.hasMethodAnnotation(PreAuthorize.class)
                || method.hasMethodAnnotation(PostAuthorize.class)
                || method.getBeanType().isAnnotationPresent(PreAuthorize.class);
            // Agar metod darajasida ham, filter chain da ham qoida bo'lmasa:
            if (!hasMethodSecurity && !coveredByFilterChain(path)) {
                unprotected.add(method.getMethod().getName() + " -> " + path);
            }
        });
        assertThat(unprotected)
            .as("himoyalanmagan endpointlar")
            .isEmpty();
    }
}
```

```bash
# Review paytida tez tekshirish: yangi endpointlar va ularning himoyasi.
git diff origin/main...HEAD -- '*.java' \
  | grep -E '^\+.*@(Get|Post|Put|Delete|Patch)Mapping' -A6 \
  | grep -E '^\+' \
  | grep -B6 -E 'public .*\(' \
  | grep -cE '@PreAuthorize|@Secured|@RolesAllowed' \
  || echo "OGOHLANTIRISH: yangi endpointlarda avtorizatsiya annotatsiyasi topilmadi"
```

### 30.6 JWT va token review

```java
// Review savollari har bir token tekshiruvi uchun.
@Bean
JwtDecoder jwtDecoder(@Value("${auth.issuer}") String issuer,
                      @Value("${auth.audience}") String audience) {
    NimbusJwtDecoder decoder = JwtDecoders.fromIssuerLocation(issuer);
    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
        new JwtTimestampValidator(Duration.ofSeconds(30)),   // muddat + clock skew
        new JwtIssuerValidator(issuer),                      // kim bergan
        new JwtClaimValidator<List<String>>("aud",           // kimga berilgan
            aud -> aud != null && aud.contains(audience)),
        new JwtClaimValidator<String>("scope",               // qanday huquq
            scope -> scope != null)
    ));
    return decoder;
}
```

| Tekshiriladigan | Nega |
| --- | --- |
| Imzo va algoritm | `alg: none` yoki `HS256` bilan `RS256` almashtirish hujumi |
| `exp` va `nbf` | Muddati o'tgan token |
| `iss` | Boshqa provayder tokeni |
| `aud` | Boshqa servis uchun berilgan token |
| `scope`/`roles` | Huquqlar |
| Bekor qilish | Chiqib ketgan foydalanuvchi tokeni hali amal qiladi |
| Muddat uzunligi | 24 soatlik access token - juda uzun |
| Saqlash joyi | `localStorage` da XSS bilan o'g'irlanadi |

```java
// Token dagi ma'lumotga ishonish chegarasi.
// Token imzolangan, ya'ni tarkibi o'zgartirilmagan. LEKIN:
// - undagi rol eskirgan bo'lishi mumkin (foydalanuvchi huquqi olib tashlangan);
// - undagi `customerId` boshqa tizimdan kelgan va tekshirilmagan bo'lishi mumkin.
// Review savoli: kritik huquqlar (to'lov, admin) har safar bazadan
// tekshiriladimi yoki tokenga ishonamizmi?
```

### 30.7 Ko'p tenantlik (multi-tenancy)

```java
// Eng xavfli xato sinfi: tenant filtri bitta joyda esdan chiqadi.
// Natijada bir mijoz boshqa mijozning ma'lumotini ko'radi.

// Zaif: tenant filtri qo'lda, har so'rovda.
List<Order> orders = repository.findByStatus(OPEN);   // tenant filtri YO'Q!

// Himoya 1: PostgreSQL Row Level Security - eng ishonchli.
```

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY orders_tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
-- Ilova har tranzaksiya boshida tenant ni o'rnatadi:
--   SET LOCAL app.tenant_id = '...';
-- Filtr esdan chiqsa ham, baza ma'lumot bermaydi. Bu "fail closed" dizayn.
```

```java
// Tenant ni tranzaksiya boshida o'rnatish.
@Component
public class TenantConnectionInitializer {
    @EventListener
    public void onTransactionStart(TransactionStartedEvent e) {
        jdbc.update("SET LOCAL app.tenant_id = ?", TenantContext.require().value());
    }
}
// Review savollari: (1) tenant qayerdan keladi (token, subdomen - so'rov
// tanasidan EMAS); (2) o'rnatilmagan bo'lsa nima bo'ladi (so'rov yiqilishi
// kerak, hamma ma'lumot qaytmasligi); (3) `SET LOCAL` pool da oqib
// ketmaydimi (LOCAL tranzaksiya oxirida tozalanadi - shuning uchun LOCAL);
// (4) keshlar tenant bo'yicha ajratilganmi (16.4);
// (5) batch va worker ishlar tenant kontekstini to'g'ri o'rnatadimi.
```

### 30.8 Biznes mantiqini chetlab o'tish

Bu zaiflik sinfi avtomatik instrumentlar uchun ko'rinmas, chunki kodda hech qanday "xavfli funksiya" yo'q.

```java
// Naqsh 1: narx mijozdan keladi.
public record CheckoutRequest(List<LineRequest> lines, BigDecimal totalPrice) { }
// Hujumchi `totalPrice = 0.01` yuboradi. Review: narx serverda hisoblanadi.

// Naqsh 2: holat o'tishi tekshirilmaydi.
@PostMapping("/orders/{id}/ship")
public void ship(@PathVariable UUID id) {
    orders.markShipped(id);                     // to'lanmagan buyurtmani jo'natish
}
// Review: holat o'tish qoidasi domen ichida (10.6).

// Naqsh 3: qadamlar tartibi majburlanmaydi.
// Ko'p qadamli jarayonda (ro'yxatdan o'tish, buyurtma) hujumchi oraliq
// qadamni o'tkazib yuborishi mumkin: /checkout/confirm ni to'lovdan oldin.
// Review savoli: har qadam oldingi qadam bajarilganini tekshiradimi?

// Naqsh 4: chegara va kvota tekshirilmaydi.
// Chegirma kodini 1000 marta ishlatish, bitta aksiyadan 500 marta foyda olish.
// Review savoli: ishlatish soni qayerda hisoblanadi va u poygaga chidamlimi
// (27.2)?

// Naqsh 5: salbiy va chegaraviy qiymatlar.
public void refund(OrderId id, Money amount) { ... }
// amount manfiy bo'lsa - pul olish. amount buyurtma summasidan katta
// bo'lsa - ortiqcha qaytarish. Review: ikkisi ham tekshirilishi kerak.
```

### 30.9 Review checklisti: kirish nazorati

| Savol | Nega |
| --- | --- |
| Har endpoint avtorizatsiya qoidasiga egami | Himoyasiz endpoint |
| Resurs egaligi tekshiriladimi | IDOR |
| Foydalanuvchi ID si so'rovdan olinmaydimi | O'zgalar nomidan harakat |
| Ro'yxatlar foydalanuvchi bo'yicha filtrlanganmi | Ommaviy ma'lumot oqishi |
| `404` yoki `403` tanlovi ongli qilinganmi | Enumeratsiya |
| `anyRequest().authenticated()` oxirida bormi | Yangi endpoint ochiq |
| `permitAll` naqshlari tormi | Ortiqcha ochiqlik |
| CSRF holati autentifikatsiya shakliga mosmi | CSRF hujumi |
| JWT da `iss`, `aud`, `exp` tekshiriladimi | Boshqa tokenni qabul qilish |
| Kritik huquqlar bazadan tekshiriladimi | Eskirgan token |
| Tenant izolyatsiyasi majburlanganmi (RLS) | Tenant orasida oqish |
| Narx, summa, status serverda hisoblanadimi | Biznes mantiqini chetlab o'tish |
| Manfiy va chegaraviy qiymatlar tekshirilganmi | Pul yo'nalishini teskari qilish |
| Avtorizatsiya qoidalari test bilan qoplanganmi | Regressiya |

### 30.10 Amalda qo'llash

- [ ] Barcha endpointlarni ro'yxatga olib, har biri uchun "kim kira oladi" va "kod buni qanday ta'minlaydi" ustunlarini to'ldiring.
- [ ] `isAuthenticated()` yoki faqat rol bilan himoyalangan, lekin foydalanuvchi resursiga tegadigan endpointlarni toping - har biri IDOR.
- [ ] So'rov tanasidan yoki parametrdan `userId`, `customerId`, `tenantId` oladigan joylarni toping va autentifikatsiya kontekstiga o'tkazing.
- [ ] Himoyalanmagan endpointlarni aniqlaydigan testni (30.5) qo'shib, CI ga kiriting.
- [ ] JWT dekoder sozlamalarida `iss`, `aud`, `exp` va algoritm tekshiruvi borligini tasdiqlang.
- [ ] Ko'p tenantli bo'lsa, PostgreSQL RLS ni yoqib, tenant filtri esdan chiqishiga chidamli dizayn qiling.
- [ ] Narx, chegirma va summa mijozdan keladigan joylarni toping va serverda hisoblashga o'tkazing.
- [ ] Har bir holat o'tishi va ko'p qadamli jarayon uchun oldingi qadam tekshiruvini qo'shing.
- [ ] Avtorizatsiya uchun kamida uchta test yozing: egasi ko'radi, boshqa foydalanuvchi ko'rmaydi, anonim rad etiladi.

## 31. Kirish va chiqish xavfsizligi: SSRF, deserializatsiya, fayllar (Input and Output Safety)

Bu bob tashqi dunyo bilan aloqa qiladigan qolgan yo'llarni oladi: tizim boshqa manzilga so'rov yuborganda, baytlarni obyektga aylantirganda va fayl bilan ishlaganda. Har uchida umumiy xato bor - tashqi ma'lumotning strukturaviy qismiga ishonish.

### 31.1 SSRF: URL ni kirishdan qurish

```java
// Zaiflik: foydalanuvchi bergan URL ga so'rov yuborish.
@PostMapping("/import")
public ImportResult importFrom(@RequestParam String url) {
    String body = restClient.get().uri(url).retrieve().body(String.class);
    return parse(body);
}
// Hujumchi quyidagilarni so'raydi:
//   http://169.254.169.254/latest/meta-data/iam/...  (cloud metadata, kalitlar)
//   http://localhost:9090/actuator/env                (ichki actuator)
//   http://postgres:5432                              (ichki servislar skanerlash)
//   file:///etc/passwd                                (fayl o'qish)
//   http://internal-admin.svc.cluster.local/          (ichki tarmoq)
```

```java
// Himoya: whitelist birinchi tanlov, blacklist ikkinchi.
@Component
public class SafeUrlResolver {

    private final Set<String> allowedHosts;      // konfiguratsiyadan

    public URI validate(String raw) {
        URI uri = URI.create(raw);

        // 1) Faqat https (yoki http, agar kerak bo'lsa). file:, gopher:, ftp: yo'q.
        if (!"https".equalsIgnoreCase(uri.getScheme())) {
            throw new UnsafeUrl("faqat https ruxsat etilgan");
        }
        // 2) Host whitelist da bo'lishi kerak.
        if (!allowedHosts.contains(uri.getHost())) {
            throw new UnsafeUrl("ruxsat etilmagan host: " + uri.getHost());
        }
        // 3) DNS ni hal qilib, IP ni tekshirish (DNS rebinding dan himoya
        //    to'liq emas, lekin oddiy hujumlarni to'xtatadi).
        for (InetAddress addr : InetAddress.getAllByName(uri.getHost())) {
            if (addr.isLoopbackAddress() || addr.isSiteLocalAddress()
                || addr.isLinkLocalAddress() || addr.isAnyLocalAddress()) {
                throw new UnsafeUrl("ichki manzil: " + addr);
            }
        }
        return uri;
    }
}
// Qo'shimcha himoyalar (review da so'raladi):
// - redirect larni kuzatmaslik yoki ularni ham tekshirish;
// - chiqish trafigi uchun alohida proksi va tarmoq siyosati (eng ishonchli);
// - javob hajmi va timeout chegarasi;
// - metadata servisiga kirishni infratuzilma darajasida bloklash.
```

```java
// Redirect: eng ko'p o'tkazib yuboriladigan nuqta.
// Hujumchi ruxsat etilgan hostdan 302 bilan ichki manzilga yo'naltiradi.
HttpClient client = HttpClient.newBuilder()
    .followRedirects(HttpClient.Redirect.NEVER)       // review talabi
    .connectTimeout(Duration.ofSeconds(2))
    .build();
```

### 31.2 Deserializatsiya

```java
// Eng xavfli: Java native deserializatsiya ishonilmaydigan ma'lumotdan.
ObjectInputStream in = new ObjectInputStream(request.getInputStream());
Object obj = in.readObject();                    // RCE yo'li
// Review qoidasi: `readObject` ishonilmaydigan ma'lumot bilan hech qachon.
// Agar meros kod shunday ishlatsa: ObjectInputFilter bilan cheklash
// (JDK 9+) yoki butunlay JSON ga o'tish.
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "com.acme.dto.*;java.util.*;!*");            // whitelist, qolgani rad etiladi
in.setObjectInputFilter(filter);

// Jackson: polimorfik deserializatsiya xavfi.
ObjectMapper mapper = new ObjectMapper();
mapper.enableDefaultTyping();                    // taqiqlanadi (eski API)
mapper.activateDefaultTyping(LaissezFaireSubTypeValidator.instance);   // xavfli
// Hujumchi JSON ga `"@class": "..."` qo'yib, gadget zanjirini ishga tushiradi.

// Xavfsiz polimorfizm: aniq ro'yxat bilan.
@JsonTypeInfo(use = Id.NAME, include = As.PROPERTY, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = CardPayment.class, name = "CARD"),
    @JsonSubTypes.Type(value = WalletPayment.class, name = "WALLET")
})
public sealed interface PaymentMethod { }
// Faqat sanab o'tilgan turlar yaratiladi. `sealed` bilan birga -
// kompilyator ham to'liqlikni tekshiradi.

// XML: XXE himoyasi.
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
// Review qoidasi: har bir XML parser yaratilgan joyda shu sozlamalar bo'lishi
// kerak - standart holatda XXE mumkin.

// YAML: SnakeYAML da ham deserializatsiya xavfi bor.
Yaml yaml = new Yaml(new SafeConstructor(new LoaderOptions()));   // ixtiyoriy turlar yo'q
```

### 31.3 Fayl yo'li va arxivlar

```java
// Path traversal: fayl nomi kirishdan.
@GetMapping("/files/{name}")
public Resource download(@PathVariable String name) {
    return new FileSystemResource("/var/data/" + name);   // ../../etc/passwd
}

// Himoya: yo'lni normalizatsiya qilib, baza katalog ichida ekanini tekshirish.
private static final Path BASE = Paths.get("/var/data").toAbsolutePath().normalize();

public Resource download(String name) {
    Path target = BASE.resolve(name).normalize();
    if (!target.startsWith(BASE)) {               // majburiy tekshiruv
        throw new InvalidPath(name);
    }
    if (!Files.isRegularFile(target)) throw new FileNotFound(name);
    return new FileSystemResource(target);
}
// Yana yaxshiroq: fayl nomini foydalanuvchi bermasligi - ID bo'yicha
// bazadan haqiqiy nomni olish (20.7).

// Zip slip: arxiv ichidagi yo'l `../` bo'lishi mumkin.
try (ZipInputStream zis = new ZipInputStream(input)) {
    ZipEntry entry;
    long totalSize = 0;
    int entryCount = 0;
    while ((entry = zis.getNextEntry()) != null) {
        // 1) Yo'l tekshiruvi (zip slip).
        Path out = BASE.resolve(entry.getName()).normalize();
        if (!out.startsWith(BASE)) throw new InvalidArchive(entry.getName());
        // 2) Zip bomba himoyasi: hajm va element soni chegarasi.
        if (++entryCount > 1_000) throw new InvalidArchive("juda ko'p element");
        totalSize += entry.getSize() < 0 ? 0 : entry.getSize();
        if (totalSize > 100L * 1024 * 1024) throw new InvalidArchive("juda katta");
        // 3) Symlink va katalog e'tibor bilan.
        if (entry.isDirectory()) { Files.createDirectories(out); continue; }
        Files.copy(zis, out, StandardCopyOption.REPLACE_EXISTING);
    }
}
// Diqqat: entry.getSize() arxiv metadata sidan keladi va yolg'on bo'lishi
// mumkin - haqiqiy hajmni o'qish paytida ham cheklash kerak (BoundedInputStream).
```

### 31.4 Rasm va hujjat qayta ishlash

```java
// Tashqi fayl bilan ishlaydigan kutubxonalar - alohida xavf manbasi.
// ImageMagick, Ghostscript, LibreOffice tarixan RCE zaifliklariga ega.
// Review savollari:
// 1) Fayl sandbox da (alohida konteyner, cheklangan huquq) qayta ishlanadimi?
// 2) Kutubxona versiyasi yangilanadimi (33-bob)?
// 3) Hajm, o'lcham va vaqt chegarasi bormi?
// 4) Rasm o'lchami tekshiriladimi (decompression bomba)?

// Rasm o'lchamini ochmasdan tekshirish: "piksel bombasi" dan himoya.
try (ImageInputStream iis = ImageIO.createImageInputStream(file)) {
    Iterator<ImageReader> readers = ImageIO.getImageReaders(iis);
    if (!readers.hasNext()) throw new UnsupportedFileType("rasm emas");
    ImageReader reader = readers.next();
    reader.setInput(iis);
    int w = reader.getWidth(0), h = reader.getHeight(0);
    // 10 000 x 10 000 rasm = 400 MB xotira (4 bayt/piksel).
    if ((long) w * h > 50_000_000L) throw new ImageTooLarge(w, h);
}
```

### 31.5 Regex va DoS (ReDoS)

```java
// Katastrofik backtracking: kichik kirish, cheksiz vaqt.
Pattern.compile("^(a+)+$").matcher("aaaaaaaaaaaaaaaaaaaaaaaaaaaaX").matches();
// Bu kod minutlarga cho'ziladi va CPU ni to'liq egallaydi.

// Xavfli naqshlar: ichma-ich kvantifikatorlar `(a+)+`, `(a|a)*`,
// va kirish uzunligi cheklanmagan `.*` zanjirlari.
// Review qoidasi: (1) foydalanuvchi regex bermasligi kerak;
// (2) kirish uzunligi oldin cheklanadi; (3) murakkab validatsiya uchun
// regex o'rniga parser.

// Email validatsiyasi: murakkab regex o'rniga oddiy tekshiruv.
// Zaif: internetdan olingan "to'liq RFC 5322" regex - ReDoS manbasi.
// Yaxshi: oddiy shakl tekshiruvi + haqiqiy tasdiqlash (email yuborish).
private static final Pattern EMAIL = Pattern.compile("^[^@\\s]{1,64}@[^@\\s]{1,255}$");

// Kirish uzunligini oldin cheklash - eng oddiy va eng samarali himoya.
if (input.length() > 256) throw new InputTooLong();
```

### 31.6 Resurs charchatish (DoS) yo'llari

| Yo'l | Himoya |
| --- | --- |
| Katta so'rov tanasi | `max-http-request-header-size`, multipart chegaralari |
| Chuqur JSON | `StreamReadConstraints` (20.8) |
| Katta massiv parametri | `@Size(max = ...)` |
| Chegarasiz `size` parametri | `@Max(100)` |
| ReDoS | Kirish uzunligi, oddiy regex |
| Zip/rasm bombasi | Hajm va o'lcham chegarasi |
| Ko'p parallel so'rov | Rate limit, bulkhead |
| Sekin mijoz (slowloris) | Ulanish timeout i, reverse proxy |
| Qimmat so'rov (hisobot) | Navbat, kesh, rate limit |
| Log to'lishi | Log darajasi, rate limit, disk alert |

```java
// Rate limit: review da so'raladigan minimal himoya.
// Bucket4j bilan, foydalanuvchi va IP bo'yicha.
@Component
public class RateLimitFilter extends OncePerRequestFilter {

    private final Cache<String, Bucket> buckets = Caffeine.newBuilder()
        .maximumSize(100_000)                           // kesh ham chegaralangan
        .expireAfterAccess(Duration.ofMinutes(10))
        .build();

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws IOException, ServletException {
        String key = keyFor(req);                       // user ID yoki IP
        Bucket bucket = buckets.get(key, k -> Bucket.builder()
            .addLimit(limit -> limit.capacity(100).refillGreedy(100, Duration.ofMinutes(1)))
            .build());
        if (!bucket.tryConsume(1)) {
            res.setStatus(429);
            res.setHeader("Retry-After", "60");
            return;
        }
        chain.doFilter(req, res);
    }
}
// Review savollari: kalit nima (IP proksi ortida ishonchli emas),
// chegara qanday tanlangan, va qimmat endpointlar uchun alohida
// (qattiqroq) chegara bormi.
```

### 31.7 Review checklisti: kirish va chiqish

| Savol | Nega |
| --- | --- |
| Tashqi URL ga so'rov bormi, whitelist bormi | SSRF |
| Redirect kuzatilmaydimi | SSRF chetlab o'tish |
| `readObject` ishonilmaydigan ma'lumot bilan ishlatilmaydimi | RCE |
| Jackson polimorfizmi aniq ro'yxat bilanmi | Deserializatsiya hujumi |
| XML parser XXE dan himoyalanganmi | Fayl o'qish, SSRF |
| Fayl yo'li normalizatsiya qilinib tekshiriladimi | Path traversal |
| Arxiv ichidagi yo'l va hajm tekshiriladimi | Zip slip, zip bomba |
| Rasm o'lchami ochishdan oldin tekshiriladimi | Xotira charchatish |
| Regex da ichma-ich kvantifikator yo'qmi | ReDoS |
| Kirish uzunligi cheklanganmi | DoS |
| Rate limit bormi | Zo'ravonlik va bo'ron |
| Tashqi jarayon sandbox dami | RCE ta'sirini cheklash |

### 31.8 Amalda qo'llash

- [ ] Tashqi URL ga so'rov yuboradigan barcha joylarni toping va ularga whitelist, sxema va IP tekshiruvini qo'shing.
- [ ] HTTP mijozlarda `followRedirects` ni o'chiring yoki redirect manzilini ham tekshiring.
- [ ] `ObjectInputStream` ishlatilgan joylarni toping va ularni JSON ga o'tkazish yoki `ObjectInputFilter` qo'shish rejasini tuzing.
- [ ] `activateDefaultTyping` va `enableDefaultTyping` ishlatilgan joylarni butunlay olib tashlang.
- [ ] Barcha XML parser yaratilgan joylarga XXE himoyasini qo'shing va buni yordamchi fabrika metodiga yig'ing.
- [ ] Fayl yo'li quruvchi kodni `normalize()` + `startsWith(BASE)` tekshiruvi bilan himoyalang.
- [ ] Arxiv ochadigan kodga element soni, umumiy hajm va yo'l tekshiruvini qo'shing.
- [ ] Loyihadagi regex larni ko'rib chiqib, ichma-ich kvantifikatorli naqshlarni toping va kirish uzunligini cheklang.
- [ ] Qimmat endpointlar (hisobot, eksport, qidiruv) uchun alohida rate limit qo'ying.

## 32. Secret, maxfiy ma'lumot va kriptografiya review (Secrets, PII and Crypto)

Bu bob ma'lumotning oshkor bo'lish yo'llarini va kriptografik xatolarni oladi. Ularning umumiy xususiyati: ular sodir bo'lganda hech narsa buzilmaydi, tizim normal ishlaydi, va muammo faqat keyinroq - ma'lumot tashqarida paydo bo'lganda - bilinadi.

### 32.1 Logga maxfiy ma'lumot tushishi

Bu eng ko'p uchraydigan ma'lumot oqishi yo'li, va review da eng oson topiladigan.

```java
// Naqsh 1: butun so'rovni logga yozish.
log.info("So'rov keldi: {}", request);           // parol, karta, token - hammasi
log.debug("Foydalanuvchi: {}", user);            // toString() da nima bor?

// Naqsh 2: istisno xabarida maxfiy ma'lumot.
throw new InvalidCardException("Karta raqami yaroqsiz: " + cardNumber);
// Bu istisno logga tushadi va karta raqami logda qoladi - PCI DSS buzilishi.

// Naqsh 3: HTTP mijoz loglari.
logging.level.org.springframework.web.client=DEBUG   // Authorization header logda

// Naqsh 4: SQL parametrlari logi.
logging.level.org.hibernate.orm.jdbc.bind=TRACE      // parol hash, PII
// Bu sozlama lokalda foydali, prodda - ma'lumot oqishi.

// Himoya 1: toString ni maskalash - eng ishonchli, chunki bir joyda.
public record PaymentRequest(String cardNumber, String cvv, Money amount) {
    @Override public String toString() {
        return "PaymentRequest[card=%s, cvv=***, amount=%s]"
               .formatted(mask(cardNumber), amount);
    }
    private static String mask(String card) {
        if (card == null || card.length() < 4) return "****";
        return "*".repeat(card.length() - 4) + card.substring(card.length() - 4);
    }
}

// Himoya 2: tipga maskalashni yashirish - unutish imkonsiz bo'ladi.
public final class Secret {
    private final String value;
    public Secret(String value) { this.value = value; }
    public String reveal() { return value; }         // aniq niyat bilan
    @Override public String toString() { return "***"; }   // log va xatolarda
}
// Ishlatilishi: Secret apiKey - uni tasodifan logga yozib bo'lmaydi.
```

```xml
<!-- Himoya 3: log darajasida maskalash (oxirgi himoya chizig'i). -->
<!-- logback-spring.xml -->
<configuration>
  <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
      <!-- Karta raqami naqshini maskalash -->
      <jsonGeneratorDecorator class="net.logstash.logback.decorate.MaskingJsonGeneratorDecorator">
        <defaultMask>****</defaultMask>
        <path>password</path>
        <path>cvv</path>
        <path>cardNumber</path>
        <path>authorization</path>
        <valueMask>
          <value>\b\d{13,19}\b</value>        <!-- karta raqamiga o'xshash -->
        </valueMask>
      </jsonGeneratorDecorator>
    </encoder>
  </appender>
</configuration>
```

### 32.2 PII va ma'lumot minimizatsiyasi

| Review savoli | Nega |
| --- | --- |
| Bu maydon haqiqatan kerakmi | Saqlanmagan ma'lumot oqib ketmaydi |
| Qancha vaqt saqlanadi | Saqlash muddati siyosati |
| Kim ko'ra oladi | Rol va audit |
| Eksport va hisobotlarda bormi | Oqish yo'li |
| Test ma'lumotida haqiqiy PII yo'qmi | Prod nusxasi test muhitida |
| Analitikaga yuboriladimi | Uchinchi tomon |
| Shifrlanganmi (saqlashda) | Baza nusxasi oqsa |
| O'chirish talabi bajariladimi | Huquqiy talab (26.7) |

```sql
-- PII ustunlarini belgilash: review va audit uchun.
COMMENT ON COLUMN customer.phone IS 'PII: telefon, saqlash muddati 3 yil';
COMMENT ON COLUMN customer.passport_number IS 'PII: sezgir, shifrlangan';

-- PII ustunlarini topish: audit so'rovi.
SELECT c.table_name, c.column_name, pd.description
  FROM information_schema.columns c
  LEFT JOIN pg_description pd
    ON pd.objoid = (quote_ident(c.table_schema)||'.'||quote_ident(c.table_name))::regclass
   AND pd.objsubid = c.ordinal_position
 WHERE pd.description LIKE 'PII%'
 ORDER BY 1, 2;
```

### 32.3 Parol va token saqlash

```java
// Parol: faqat moslashuvchan hash funksiyasi bilan.
@Bean
PasswordEncoder passwordEncoder() {
    // Argon2 yoki bcrypt. SHA-256 va MD5 - parol uchun TAQIQLANADI
    // (ular tez, ya'ni brute force ham tez).
    return new Argon2PasswordEncoder(16, 32, 1, 19 * 1024, 2);
    // Yoki: new BCryptPasswordEncoder(12);
}
// Review savollari: (1) parametrlar yetarlimi (bcrypt da cost >= 10);
// (2) migratsiya yo'li bormi (DelegatingPasswordEncoder eski hash larni
// qo'llab-quvvatlaydi va kirish paytida yangilaydi);
// (3) parol uzunligi chegarasi bormi (bcrypt 72 baytdan keyin kesadi).

// Token va API kalit: hash qilib saqlash (parol kabi).
// Bazada ochiq token saqlanmasligi kerak - baza nusxasi oqsa, hamma
// token ishlatilishi mumkin.
public record ApiKey(String id, String hashedSecret) {
    public static ApiKey generate(PasswordEncoder encoder) {
        byte[] raw = new byte[32];
        new SecureRandom().nextBytes(raw);                  // SecureRandom!
        String secret = Base64.getUrlEncoder().withoutPadding().encodeToString(raw);
        return new ApiKey(UUID.randomUUID().toString(), encoder.encode(secret));
        // `secret` faqat bir marta foydalanuvchiga ko'rsatiladi.
    }
}
```

### 32.4 Tasodifiylik

```java
// Zaif: taxmin qilinadigan.
new Random().nextInt();                          // seed vaqtdan, taxmin qilinadi
Math.random();                                   // xuddi shunday
UUID.randomUUID();                               // kriptografik (SecureRandom) - to'g'ri

// Kuchli: token, kalit, parol tiklash kodi uchun.
SecureRandom random = new SecureRandom();
byte[] token = new byte[32];
random.nextBytes(token);

// Review qoidasi: xavfsizlikka tegishli har qanday tasodifiy qiymat
// (token, parol tiklash kodi, sessiya ID, nonce, salt, OTP)
// SecureRandom bilan yaratiladi.

// Diqqat: OTP uchun 6 raqam - bu 10^6 variant. Brute force dan himoya
// urinishlar chegarasi bilan ta'minlanadi, tasodifiylik bilan emas.
int otp = random.nextInt(1_000_000);             // tasodifiy, lekin qisqa
// Review savoli: urinishlar soni cheklanganmi va kod qancha amal qiladi?
```

### 32.5 Shifrlash

```java
// Zaif: ECB rejimi (naqshlarni saqlaydi) va qattiq yozilgan IV.
Cipher c = Cipher.getInstance("AES/ECB/PKCS5Padding");          // taqiqlanadi
Cipher c = Cipher.getInstance("AES/CBC/PKCS5Padding");          // IV kerak, autentifikatsiya yo'q

// To'g'ri: autentifikatsiyalangan shifrlash (AEAD), har marta yangi nonce.
public final class FieldEncryption {
    private static final int GCM_TAG_BITS = 128;
    private static final int NONCE_BYTES = 12;
    private final SecretKey key;
    private final SecureRandom random = new SecureRandom();

    public byte[] encrypt(byte[] plaintext, byte[] associatedData) throws Exception {
        byte[] nonce = new byte[NONCE_BYTES];
        random.nextBytes(nonce);                      // HAR SAFAR yangi
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(GCM_TAG_BITS, nonce));
        if (associatedData != null) cipher.updateAAD(associatedData);
        byte[] ct = cipher.doFinal(plaintext);
        return ByteBuffer.allocate(nonce.length + ct.length)
                         .put(nonce).put(ct).array();   // nonce ochiq saqlanadi
    }
}
// Review savollari: (1) nonce qayta ishlatilmaydimi (GCM da nonce
// takrorlanishi kalitni ochadi - eng xavfli xato); (2) kalit qayerdan
// keladi (KMS, Vault - koddan emas); (3) kalit rotatsiyasi qanday
// (shifrlangan ma'lumotga kalit versiyasi yozilganmi); (4) nima
// shifrlangan va nega aynan shu.
```

### 32.6 Taqqoslash va vaqt hujumlari

```java
// Zaif: token taqqoslash `equals` bilan - vaqt bo'yicha ma'lumot beradi.
if (providedToken.equals(storedToken)) { ... }
// `String.equals` birinchi farqda to'xtaydi, ya'ni bajarilish vaqti
// to'g'ri belgilar soniga bog'liq. Masofadan bu farqni o'lchash qiyin,
// lekin mumkin.

// To'g'ri: doimiy vaqtli taqqoslash.
if (MessageDigest.isEqual(provided.getBytes(UTF_8), stored.getBytes(UTF_8))) { ... }

// HMAC tekshirish (webhook imzosi) - eng ko'p uchraydigan joy.
public boolean verifyWebhook(byte[] body, String signatureHeader) throws Exception {
    Mac mac = Mac.getInstance("HmacSHA256");
    mac.init(new SecretKeySpec(webhookSecret, "HmacSHA256"));
    byte[] expected = mac.doFinal(body);
    byte[] provided = Hex.decode(signatureHeader);
    return MessageDigest.isEqual(expected, provided);      // doimiy vaqt
}
// Review savollari: (1) imzo tekshiriladimi umuman (ko'p loyihada webhook
// tekshirilmaydi - har kim xabar yuborishi mumkin); (2) xom tana bo'yicha
// tekshiriladimi (JSON qayta serializatsiya qilinsa imzo buziladi);
// (3) takrorlanishdan himoya bormi (timestamp va nonce).
```

### 32.7 TLS va sertifikatlar

```java
// Taqiqlanadi: sertifikat tekshiruvini o'chirish.
TrustManager[] trustAll = new TrustManager[]{ new X509TrustManager() {
    public void checkServerTrusted(X509Certificate[] c, String a) { }   // hech narsa
    ...
}};
// Review izohi: bu kod MITM hujumini to'liq ochib beradi. "Test uchun"
// yoki "staging da sertifikat yo'q" sababi qabul qilinmaydi - to'g'ri
// yechim: ichki CA ni truststore ga qo'shish.

// To'g'ri: ichki CA bilan.
// JVM ga: -Djavax.net.ssl.trustStore=/etc/ssl/internal-truststore.jks
// Yoki kodda aniq truststore:
SSLContext ctx = SSLContextBuilder.create()
    .loadTrustMaterial(new File("/etc/ssl/internal-ca.jks"), password)
    .build();
```

### 32.8 Review checklisti: secret va kriptografiya

| Savol | Nega |
| --- | --- |
| Logga maxfiy ma'lumot tushmaydimi | Eng ko'p uchraydigan oqish |
| `toString` maskalanganmi | Tasodifiy log |
| Istisno xabarida PII yo'qmi | Log va javob orqali oqish |
| Secret muhitdan yoki Vault danmi | Repoda kalit |
| Parol Argon2/bcrypt bilanmi | Tez hash brute force ga ochiq |
| Token hash qilib saqlanadimi | Baza nusxasi |
| `SecureRandom` ishlatilganmi | Taxmin qilinadigan token |
| Shifrlash AEAD (GCM) mi | Yaxlit emas shifrlash |
| Nonce har safar yangimi | GCM da halokatli xato |
| Kalit rotatsiyasi rejasi bormi | Kalit oqsa |
| Token taqqoslash doimiy vaqtlimi | Vaqt hujumi |
| Webhook imzosi tekshiriladimi | Yolg'on xabar |
| TLS tekshiruvi o'chirilmaganmi | MITM |
| PII saqlash muddati belgilanganmi | Huquqiy talab |

### 32.9 Amalda qo'llash

- [ ] Maxfiy ma'lumot tashuvchi barcha DTO va domen turlarida `toString` maskalanganini tekshiring.
- [ ] `Secret` yoki shunga o'xshash o'ram turini kiritib, API kalitlari va tokenlarni unga o'tkazing.
- [ ] Logback da maskalash dekoratorini sozlab, karta raqami va `authorization` naqshlarini maskalang.
- [ ] Prod log darajalarini tekshirib, `hibernate.orm.jdbc.bind` va web client DEBUG loglarini o'chiring.
- [ ] Parol enkoderini Argon2 yoki bcrypt (cost >= 12) ga o'tkazing va `DelegatingPasswordEncoder` bilan migratsiya yo'lini qo'ying.
- [ ] Bazada ochiq saqlanayotgan token va API kalitlarni hash ga o'tkazing.
- [ ] `new Random()` va `Math.random()` ishlatilgan xavfsizlikka tegishli joylarni `SecureRandom` ga o'tkazing.
- [ ] Shifrlash ishlatilgan joylarda rejim (GCM), nonke yangiligi va kalit manbasini tekshiring.
- [ ] Webhook qabul qiluvchilarda imzo tekshiruvi va doimiy vaqtli taqqoslash borligini tasdiqlang.
- [ ] PII ustunlarini `COMMENT ON COLUMN` bilan belgilab, saqlash muddati siyosatini yozing.

## 33. Bog'liqlik va supply chain review (Dependencies and Supply Chain)

`pom.xml` dagi bitta qator butun ilovaga kod qo'shadi - sizning kodingizdan ko'p bo'lishi mumkin. Shu sababli bog'liqlik o'zgarishi review da alohida e'tibor talab qiladi, lekin amalda u eng tez "LGTM" oladigan diff turi.

### 33.1 Yangi bog'liqlik uchun savollar

6.4 da arxitektura nuqtai nazaridan savollar berilgan; bu yerda xavfsizlik va yangilanish nuqtai nazari.

| Savol | Qanday tekshirish |
| --- | --- |
| Oxirgi reliz qachon | Maven Central yoki GitHub |
| Ma'lum CVE bormi | `dependency-check`, `osv-scanner` |
| Litsenziya mosmi | `license-maven-plugin` |
| Nechta transitive olib keladi | `dependency:tree` |
| Ishlab chiqaruvchisi kim | Jamoa yoki bitta odam |
| Nomi tanish paketga o'xshashmi | Typosquatting |
| Qancha kod uchun olinadi | 20 satr uchun kutubxona - savol |
| Alternativa JDK yoki Spring da bormi | Ko'pincha bor |

```bash
# Yangi bog'liqlik haqida ma'lumot to'plash: review izohi uchun dalil.
GROUP=com.example; ART=some-lib; VER=1.2.3

# 1) Oxirgi versiyalar va relizlar oralig'i.
curl -s "https://search.maven.org/solrsearch/select?q=g:$GROUP+AND+a:$ART&core=gav&rows=10&wt=json" \
  | jq -r '.response.docs[] | "\(.v)  \(.timestamp/1000 | todate)"'

# 2) Ma'lum zaifliklar (OSV - Google ning ochiq bazasi).
curl -s -X POST https://api.osv.dev/v1/query \
  -d "{\"package\":{\"ecosystem\":\"Maven\",\"name\":\"$GROUP:$ART\"},\"version\":\"$VER\"}" \
  | jq -r '.vulns[]? | "\(.id): \(.summary)"'

# 3) Nimani olib keladi.
./mvnw dependency:tree -Dincludes="$GROUP:$ART" -Dverbose

# 4) Haqiqiy o'zgarish: butun daraxt farqi (6.4 dagi usul).
```

### 33.2 Transitive bog'liqliklar va versiya konflikti

```bash
# Versiya konfliktlarini topish: Maven "eng yaqin g'olib" qoidasini
# ishlatadi, bu kutilmagan versiyaga olib kelishi mumkin.
./mvnw dependency:tree -Dverbose | grep -E 'omitted for conflict' | head -20

# Yakuniy versiyalarni ko'rish (haqiqatda nima ishlatiladi).
./mvnw dependency:list | grep -E 'jackson|netty|guava|commons' | sort -u

# Review diqqati: Spring Boot BOM versiyalarni boshqaradi. Qo'lda
# versiya ko'rsatish BOM ni chetlab o'tadi va mos kelmaslikka olib keladi.
```

```xml
<!-- Yomon: versiya qo'lda, BOM chetlab o'tilgan. -->
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
  <version>2.15.0</version>            <!-- Boot boshqa versiya kutadi -->
</dependency>

<!-- Yaxshi: BOM boshqaradi. -->
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
</dependency>

<!-- Agar aniq versiya kerak bo'lsa: sabab izoh bilan va BOM property orqali. -->
<properties>
  <!-- CVE-2026-XXXX tufayli 2.17.1 ga ko'tarildi; Boot 3.4 da 2.17.0.
       Boot 3.5 ga o'tganda bu propertyni olib tashlash kerak. -->
  <jackson-bom.version>2.17.1</jackson-bom.version>
</properties>
```

### 33.3 Skanerlashni CI ga qo'yish

```xml
<!-- OWASP Dependency-Check: ma'lum CVE larni topadi. -->
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <configuration>
    <!-- Yangi zaiflik topilsa build yiqiladi, lekin faqat yuqori darajada -
         aks holda shovqin tufayli hamma e'tiborsiz qoldiradi. -->
    <failBuildOnCVSS>7.0</failBuildOnCVSS>
    <suppressionFiles>
      <suppressionFile>.dependency-check-suppressions.xml</suppressionFile>
    </suppressionFiles>
    <nvdApiKey>${env.NVD_API_KEY}</nvdApiKey>
  </configuration>
</plugin>
```

```xml
<!-- Suppression fayli - review ning muhim obyekti.
     Har bir suppression sabab va muddat bilan bo'lishi kerak. -->
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
  <suppress until="2026-12-31Z">
    <notes>
      CVE-2026-1234: faqat XML parsing yo'lida, biz faqat JSON ishlatamiz.
      Tekshirilgan: 2026-10-04, PR #1423. Keyingi ko'rib chiqish: 2026-12-31.
    </notes>
    <packageUrl regex="true">^pkg:maven/com\.example/some-lib@.*$</packageUrl>
    <cve>CVE-2026-1234</cve>
  </suppress>
</suppressions>
<!-- Review qoidasi: izohsiz yoki `until` siz suppression qabul qilinmaydi.
     Aks holda suppression fayli "hammasini o'chirish" vositasiga aylanadi. -->
```

```bash
# Yengilroq va tezroq alternativa: osv-scanner (lockfile bo'yicha).
osv-scanner --lockfile=pom.xml

# SBOM yaratish: nima ishlatilayotganini hujjatlashtirish.
./mvnw org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom
# Natija: target/bom.json - incident paytida "bizda shu kutubxona bormi"
# savoliga tez javob beradi.
```

### 33.4 Versiya yangilash PR larini review qilish

Dependabot yoki Renovate yuborgan PR lar ko'pincha e'tiborsiz merge qilinadi. Ular uchun ham qoidalar kerak.

| Yangilanish turi | Review talabi |
| --- | --- |
| Patch (3.4.1 -> 3.4.2) | CI yashil bo'lsa yetarli |
| Minor (3.4 -> 3.5) | Reliz izohini o'qish, deprecation larni ko'rish |
| Major (3.x -> 4.x) | Migratsiya qo'llanmasi, alohida reja |
| Xavfsizlik yangilanishi | Tezkor, lekin CI majburiy |
| Transitive versiya o'zgarishi | `dependency:tree` farqini ko'rish |
| Build plugin yangilanishi | Lokalda `verify` o'tkazish |

```yaml
# Renovate konfiguratsiyasi: shovqinni kamaytirish va muhimini ajratish.
{
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "description": "Patch yangilanishlarni avtomatik birlashtirish",
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "description": "Spring Boot va Java ni alohida ko'rish",
      "matchPackagePatterns": ["^org.springframework", "^java"],
      "automerge": false,
      "labels": ["needs-careful-review"]
    },
    {
      "description": "Xavfsizlik yangilanishlari darhol",
      "matchDatasources": ["maven"],
      "vulnerabilityAlerts": { "labels": ["security"], "automerge": false }
    }
  ],
  "prConcurrentLimit": 5
}
```

### 33.5 Build va CI ning o'zi

Supply chain xavfi faqat kutubxonalarda emas - build jarayonining o'zida ham.

| Xavf | Himoya |
| --- | --- |
| Pin qilinmagan GitHub Action | SHA bilan pin qilish (`uses: actions/checkout@<sha>`) |
| `curl | bash` build ichida | Tekshirilgan artefakt, checksum |
| Ishonchsiz Maven repozitoriy | Faqat Central va ichki Nexus |
| Secret ni CI logida chop etish | Masking, `echo` dan saqlanish |
| Fork dan kelgan PR da secret | `pull_request` (emas `pull_request_target`) |
| Build artefaktining imzosi yo'q | Sigstore, checksum |
| Konteyner bazasi tag bilan | Digest bilan pin qilish |
| `latest` tag | Aniq versiya |

```yaml
# GitHub Actions: xavfsizroq shakl.
jobs:
  build:
    permissions:
      contents: read              # minimal huquq (standart: write)
    steps:
      # SHA bilan pin: tag o'zgartirilishi mumkin, SHA - yo'q.
      - uses: actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955  # v4.3.0
      - uses: actions/setup-java@c5195efecf7bdfc987ee8bae7a71cb8b11521c00  # v4.7.1
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: 'maven'
      - run: ./mvnw -B verify
```

```dockerfile
# Konteyner bazasini digest bilan pin qilish.
FROM eclipse-temurin:21-jre-alpine@sha256:abc123...
# Tag (`21-jre-alpine`) o'zgarishi mumkin - digest o'zgarmaydi.
# Review savoli: bu digest qachon yangilanadi va kim yangilaydi?

# Qo'shimcha review bandlari:
USER 10001                      # root emas
COPY --chown=10001:10001 target/app.jar /app/app.jar
# Ko'p qatlamli build: build vositalari yakuniy obrazda qolmaydi.
```

### 33.6 Review checklisti: bog'liqliklar

| Savol | Nega |
| --- | --- |
| Yangi bog'liqlik haqiqatan kerakmi | Hujum yuzasi va yangilanish yuki |
| CVE holati tekshirilganmi | Ma'lum zaiflik |
| Litsenziya mosmi | Huquqiy xavf |
| Versiya BOM orqali boshqariladimi | Mos kelmaslik |
| Qo'lda versiya ko'rsatilsa, sabab yozilganmi | Keyinchalik eskirib qoladi |
| Transitive o'zgarishlar ko'rilganmi | Yashirin yangilanish |
| Suppression lar sabab va muddat bilanmi | "Hammasini o'chirish" |
| GitHub Action lar SHA bilan pin qilinganmi | Supply chain |
| Konteyner bazasi digest bilanmi | Takrorlanuvchanlik |
| CI huquqlari minimalmi | Token o'g'irlanishi |
| SBOM yaratiladimi | Incidentda tez javob |

### 33.7 Amalda qo'llash

- [ ] `dependency-check` yoki `osv-scanner` ni CI ga qo'shib, `failBuildOnCVSS` ni 7.0 ga qo'ying.
- [ ] Mavjud suppression larni ko'rib chiqib, izohi va `until` sanasi yo'qlarini tuzating yoki olib tashlang.
- [ ] CycloneDX bilan SBOM yaratishni build ga qo'shing va natijani artefakt sifatida saqlang.
- [ ] Qo'lda versiya ko'rsatilgan bog'liqliklarni toping va har biriga sabab izohini qo'shing yoki BOM ga qaytaring.
- [ ] `dependency:tree -Dverbose` bilan versiya konfliktlarini aniqlab, ro'yxat tuzing.
- [ ] Renovate yoki Dependabot ni sozlab, patch yangilanishlarni avtomatik, major larni alohida yorliq bilan qiling.
- [ ] Barcha GitHub Action larni SHA bilan pin qiling va workflow huquqlarini `contents: read` ga tushiring.
- [ ] Konteyner bazasini digest bilan pin qilib, uni yangilash jarayonini belgilang.
- [ ] Yangi bog'liqlik qo'shadigan PR lar uchun shablonga 8 savolli ro'yxatni kiriting.

# VII. Test review

## 34. Test to'liqligini review qilish (Test Case Completeness)

Review ning eng kam bajariladigan qismi - testlarni jiddiy o'qish. Ko'pincha reviewer "test bor" degan faktga qaraydi va mazmunini o'qimaydi. Natijada yolg'on ishonch paydo bo'ladi: coverage 85 foiz, lekin eng xavfli holatlar qamralmagan. Bu bob testlar to'liqligini tizimli baholashni beradi - qamrov foizini emas, holatlar to'plamini tekshirish. Test yozish texnikasi va test piramidasi `java-spring-testing-handbook.md` da; bu yerda faqat review nuqtai nazari.

### 34.1 To'g'ri savol: qaysi holat qamralmagan

Coverage "bu satr bajarildimi" degan savolga javob beradi. Review esa boshqa savolni beradi: "qaysi kirish uchun bu kod noto'g'ri ishlaydi va test buni tutadimi". Ikkinchi savolga javob berish uchun tizimli usul kerak, aks holda reviewer faqat o'zi o'ylab topgan holatlarni so'raydi.

Usul to'rt qadamdan iborat:

1. Kirishlarni ekvivalentlik sinflariga bo'lish.
2. Har sinf uchun chegaralarni topish.
3. Shartlar kombinatsiyasini jadvalga yozish.
4. Xato yo'llari va holat o'tishlarini sanash.

```java
// Review qilinayotgan kod: chegirma hisobi.
public Money discountFor(Order order, Customer customer, LocalDate on) {
    if (order.total().isLessThan(MIN_TOTAL)) return Money.ZERO;      // 1
    BigDecimal rate = customer.tier().discountRate();                 // 2
    if (customer.registeredBefore(on.minusYears(1))) {                // 3
        rate = rate.add(LOYALTY_BONUS);
    }
    if (rate.compareTo(MAX_RATE) > 0) rate = MAX_RATE;                // 4
    return order.total().multiply(rate);
}
```

Shu 6 satr uchun holatlar to'plami:

| Sinf | Holatlar |
| --- | --- |
| `order.total` | `MIN_TOTAL` dan past, aynan `MIN_TOTAL`, yuqori, nol, manfiy(?), juda katta |
| `customer.tier` | Har bir enum qiymati (hammasi) |
| Ro'yxatdan o'tish sanasi | Bir yildan kam, aynan bir yil, ko'p, kelasi sana(?) |
| Natija chegarasi | `MAX_RATE` dan past, aynan, undan yuqori (kesiladi) |
| `on` | Bugun, o'tgan, kelasi |
| Null lar | `order`, `customer`, `on` null bo'lsa |

Bu 6 ta `if` uchun kamida 12-15 ta test holati. Agar PR da 2 ta test bo'lsa, review izohi aniq bo'ladi: "aynan `MIN_TOTAL` chegarasi va `MAX_RATE` kesilishi qamralmagan - ikkisi ham bitta `>` yoki `>=` xatosi bilan buziladi".

### 34.2 Chegaraviy qiymatlar: eng ko'p qaytim beradigan test holatlari

Xatolarning katta qismi chegaralarda yashaydi, chunki `<` va `<=` farqi eng ko'p qilinadigan xato. Shu sababli har bir sonli yoki tartibli shart uchun uch nuqta tekshiriladi: chegaradan bir past, aynan chegara, bir yuqori.

| Kirish turi | Tekshirilishi kerak bo'lgan qiymatlar |
| --- | --- |
| Butun son | 0, 1, -1, chegara, chegara ± 1, `MIN_VALUE`, `MAX_VALUE` |
| Pul | 0, eng kichik birlik (0.01), chegara, manfiy, juda katta |
| Satr | bo'sh, bitta belgi, maksimal uzunlik, maksimal + 1, bo'sh joy, unicode, emoji |
| Ro'yxat | bo'sh, bitta element, maksimal, maksimal + 1 |
| Sana | bugun, kecha, ertaga, chegara sana, 29-fevral, yil oxiri, yozgi vaqt o'tishi |
| Vaqt oralig'i | nol davomiylik, teskari (oxiri boshidan oldin), bir xil |
| Enum | har bir qiymat, va "yangi qiymat qo'shilsa" holati |
| Optional/null | mavjud, bo'sh, null |

```java
// To'g'ri shakl: chegaralar jadval sifatida, o'qiladigan nomlar bilan.
@ParameterizedTest(name = "{0} so'm, {1} -> {2} so'm chegirma")
@CsvSource({
    //  summa,     daraja,  kutilgan
    "  99999.99,  GOLD,     0.00",     // chegaradan bir tiyin past
    " 100000.00,  GOLD, 15000.00",     // AYNAN chegara
    " 100000.01,  GOLD, 15000.00",     // chegaradan bir tiyin yuqori
    "      0.00,  GOLD,     0.00",     // nol
    " 100000.00,  BRONZE,   0.00",     // chegirmasiz daraja
    "1000000.00,  GOLD, 150000.00"     // katta summa
})
void discountAtBoundaries(BigDecimal total, CustomerTier tier, BigDecimal expected) {
    Order order = order(total);
    Customer customer = customer(tier, registeredAt(LAST_MONTH));
    assertThat(calculator.discountFor(order, customer, TODAY))
        .isEqualByComparingTo(expected);
}

// Enum to'liqligi: yangi qiymat qo'shilsa test yiqiladi.
@ParameterizedTest
@EnumSource(CustomerTier.class)
void everyTierHasDefinedDiscount(CustomerTier tier) {
    Money result = calculator.discountFor(order(BIG_TOTAL), customer(tier), TODAY);
    assertThat(result).isNotNull();
    assertThat(result.amount()).isBetween(ZERO, BIG_TOTAL.amount());
}
```

### 34.3 Shartlar kombinatsiyasi: qaror jadvali

Ikki yoki uchdan ko'p shart birgalikda qarorga ta'sir qilsa, holatlarni bitta-bitta sanash xato: kombinatsiyalar o'tkazib yuboriladi. Qaror jadvali bu muammoni yechadi.

```text
Qoida: buyurtma bekor qilinishi mumkinmi?
Shartlar: (A) status NEW yoki PAID, (B) jo'natilmagan, (C) 24 soat ichida

| A | B | C | Natija        | Test bormi |
|---|---|---|---------------|------------|
| T | T | T | Bekor qilinadi| ha         |
| T | T | F | Rad etiladi   | YO'Q       |  <- review topilmasi
| T | F | T | Rad etiladi   | ha         |
| T | F | F | Rad etiladi   | yo'q (A=T,B=F allaqachon qamralgan) |
| F | T | T | Rad etiladi   | YO'Q       |  <- review topilmasi
| F | * | * | Rad etiladi   | -          |
```

Review izohining shakli: "Bekor qilish uchun uch shart bor, testlarda ulardan ikkitasining kombinatsiyasi yo'q: (status PAID, jo'natilmagan, lekin 24 soatdan keyin) va (status SHIPPED, 24 soat ichida). Ikkinchisi ayniqsa muhim - u mijoz jo'natilgan buyurtmani bekor qilishiga yo'l qo'ymaslik kerakligini tekshiradi."

```java
// Qaror jadvalini testda ifodalash.
@ParameterizedTest(name = "status={0}, shipped={1}, hours={2} -> {3}")
@CsvSource({
    "NEW,       false,  1, true",
    "PAID,      false,  1, true",
    "PAID,      false, 25, false",      // vaqt o'tgan
    "PAID,      true,   1, false",      // jo'natilgan
    "SHIPPED,   true,   1, false",
    "DELIVERED, true,   1, false",
    "CANCELLED, false,  1, false"       // allaqachon bekor
})
void cancellationRules(OrderStatus status, boolean shipped, int hoursAgo, boolean expected) {
    Order order = orderWith(status, shipped, clock.instant().minus(hoursAgo, HOURS));
    assertThat(order.isCancellable(clock.instant())).isEqualTo(expected);
}
```

### 34.4 Holat o'tish matritsasi

Holat mashinasi bo'lgan domen (buyurtma, to'lov, obuna) uchun to'liqlik mezoni aniq: har bir o'tish ruxsat etilgan yoki taqiqlangan ekani tekshiriladi. N holatda N x N kombinatsiya bor, va ularning hammasini bitta test bilan qoplash mumkin.

```java
// Butun matritsani bitta testda qoplash: 36 kombinatsiya (6x6).
@ParameterizedTest
@MethodSource("allTransitions")
void transitionMatrix(OrderStatus from, OrderStatus to) {
    Order order = orderInStatus(from);
    boolean allowed = ALLOWED.contains(entry(from, to));   // kutilgan jadval

    if (allowed) {
        assertThatCode(() -> order.transitionTo(to)).doesNotThrowAnyException();
        assertThat(order.status()).isEqualTo(to);
    } else {
        assertThatThrownBy(() -> order.transitionTo(to))
            .isInstanceOf(IllegalStateTransition.class);
        assertThat(order.status()).as("rad etilgan o'tishda holat o'zgarmasin")
                                  .isEqualTo(from);
    }
}

static Stream<Arguments> allTransitions() {
    return Arrays.stream(OrderStatus.values())
        .flatMap(f -> Arrays.stream(OrderStatus.values()).map(t -> arguments(f, t)));
}
// Review foydasi: yangi status qo'shilganda test avtomatik 13 yangi
// kombinatsiyani tekshiradi va `ALLOWED` jadvalini to'ldirishni talab qiladi.
```

### 34.5 Xato yo'llari: eng ko'p qamralmay qoladigan qism

Testlar odatda muvaffaqiyatli yo'lni qoplaydi. Xato yo'llari esa prodda tez-tez bajariladi va ularda xato qilish osonroq, chunki ular kamroq sinaladi.

| Xato yo'li | Tekshirilishi kerak |
| --- | --- |
| Tashqi servis timeout | Qanday istisno, retry, foydalanuvchiga javob |
| Tashqi servis 500 | Fallback ishlaydimi, holat to'g'rimi |
| Tashqi servis noto'g'ri javob | Validatsiya, istisno |
| DB constraint buzilishi | Istisno aylantirilganmi (409) |
| Optimistik qulf konflikti | Foydalanuvchiga tushunarli javob |
| Tranzaksiya rollback | Holat qaytdimi, yon ta'sir qolmadimi |
| Yarim bajarilgan jarayon | Kompensatsiya yoki qayta boshlash |
| Validatsiya xatosi | To'g'ri status va xabar |
| Avtorizatsiya rad etishi | 403/404 va ma'lumot oqmasligi |
| Bo'sh natija | Bo'sh ro'yxat, `Optional.empty()`, 404 |

```java
// Xato yo'lini test qilish: tashqi servis nosozligi.
@Test
void paymentTimeoutLeavesOrderInPendingAndSchedulesRetry() {
    when(gateway.capture(any())).thenThrow(new GatewayTimeout());

    assertThatThrownBy(() -> service.confirm(orderId))
        .isInstanceOf(PaymentPending.class);

    // Eng muhimi: holat nima bo'ldi?
    Order order = orders.findById(orderId).orElseThrow();
    assertThat(order.status()).isEqualTo(CONFIRMING);        // oraliq holat
    assertThat(outbox.pendingFor(orderId)).hasSize(1);       // qayta urinish rejalashtirilgan
    assertThat(order.paidAt()).isNull();                     // to'lanmagan deb belgilanmagan
}
// Review izohi: timeout testi bor, lekin "gateway 500 qaytardi" va
// "gateway noto'g'ri formatda javob berdi" holatlari yo'q. Uchinchisi
// ayniqsa muhim: provayder o'tgan oy `amount` ni satr sifatida
// yuborishni boshlagan edi.
```

### 34.6 Konkurentlik va idempotentlik testlari

Bu holatlar deyarli hech qachon test qilinmaydi, lekin ularni test qilish mumkin va review da so'rash kerak.

```java
// Idempotentlik testi: aniq va oson.
@Test
void sameIdempotencyKeyChargesOnce() {
    PaymentRequest req = request(Money.of(100_000));

    PaymentResponse first = service.charge("key-1", req);
    PaymentResponse second = service.charge("key-1", req);   // takroriy

    assertThat(second).isEqualTo(first);                     // bir xil natija
    verify(gateway, times(1)).charge(any());                 // bir marta chaqirilgan
    assertThat(payments.countByOrder(req.orderId())).isEqualTo(1);
}

// Poyga testi: ikki parallel so'rov.
@Test
void concurrentRegistrationCreatesSingleCustomer() throws Exception {
    String email = "ali@example.com";
    int threads = 8;
    var latch = new CountDownLatch(1);
    var pool = Executors.newFixedThreadPool(threads);
    var results = new ArrayList<Future<?>>();

    for (int i = 0; i < threads; i++) {
        results.add(pool.submit(() -> {
            latch.await();                       // hammasi bir vaqtda boshlansin
            return service.register(email);
        }));
    }
    latch.countDown();

    long ok = 0, conflicts = 0;
    for (Future<?> f : results) {
        try { f.get(); ok++; }
        catch (ExecutionException e) {
            assertThat(e.getCause()).isInstanceOf(EmailAlreadyUsed.class);
            conflicts++;
        }
    }
    assertThat(ok).as("faqat bitta muvaffaqiyat").isEqualTo(1);
    assertThat(conflicts).isEqualTo(threads - 1);
    assertThat(customers.countByEmail(email)).isEqualTo(1);
    pool.shutdown();
}
// Diqqat: bu test haqiqiy PostgreSQL bilan (Testcontainers) ishlashi kerak -
// H2 da unique constraint xulqi farq qiladi (36-bob).
```

### 34.7 Mutatsion fikrlash: testni aldab o'tish mumkinmi

Eng kuchli review texnikasi: "bu kodni qanday buzsam, testlar hali ham o'tadi" degan savol. Agar javob topilsa, test yetarli emas.

| Mutatsiya | Test tutadimi |
| --- | --- |
| `<` ni `<=` ga almashtirish | Faqat chegara testi bo'lsa |
| Shartni teskari qilish | Ikki tomon testi bo'lsa |
| Qaytish qiymatini `null` qilish | Assertion qiymatni tekshirsa |
| `if` blokini o'chirish | Shart bajarilgan holat testi bo'lsa |
| Arifmetik amalni almashtirish (`+` -> `-`) | Aniq qiymat tekshirilsa |
| Metod chaqiruvini o'chirish | Natija yoki yon ta'sir tekshirilsa |
| Konstantani o'zgartirish (15% -> 25%) | Aniq qiymat tekshirilsa |
| Istisno turini almashtirish | Tur tekshirilsa |

```java
// Review da shu savolni qo'llash: testlar quyidagi mutatsiyalarni tutadimi?
// Kod: if (order.total().isLessThan(MIN_TOTAL)) return Money.ZERO;
//
// Mutatsiya 1: isLessThan -> isLessThanOrEqual
//   Tutish uchun: total = MIN_TOTAL aynan bo'lgan test kerak.
// Mutatsiya 2: return Money.ZERO -> return null
//   Tutish uchun: natija qiymati tekshirilishi kerak (isNotNull yetarli emas,
//   lekin isEqualByComparingTo(ZERO) tutadi).
// Mutatsiya 3: butun `if` ni o'chirish
//   Tutish uchun: MIN_TOTAL dan past summa testi kerak.

// Avtomatlashtirish: PIT (pitest) mutatsion testlashni o'lchaydi.
// mvn org.pitest:pitest-maven:mutationCoverage
// Natija: "mutation score 62%" - ya'ni mutatsiyalarning 38 foizini
// testlar tutmaydi. Bu coverage dan ancha ishonchli ko'rsatkich.
```

```xml
<!-- Mutatsion testlash: eng muhim paketlar uchun, butun loyihaga emas
     (u sekin ishlaydi). -->
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <configuration>
    <targetClasses>
      <param>com.acme.order.domain.*</param>      <!-- faqat domen -->
      <param>com.acme.pricing.*</param>
    </targetClasses>
    <mutationThreshold>80</mutationThreshold>     <!-- domen uchun yuqori talab -->
    <timestampedReports>false</timestampedReports>
  </configuration>
</plugin>
```

### 34.8 Ma'lumotga bog'liq holatlar

```java
// Review da so'raladigan ma'lumot holatlari.
// 1) Bo'sh to'plam: ro'yxat bo'sh bo'lsa hisob to'g'rimi?
@Test void totalOfEmptyOrderIsZero() { ... }
// Ko'pincha bu yerda 0 ga bo'lish yoki `get(0)` xatosi chiqadi.

// 2) Bitta element: o'rtacha, mediana, birinchi/oxirgi.
@Test void singleLineOrderTotal() { ... }

// 3) Dublikatlar: bir xil mahsulot ikki marta.
@Test void duplicateProductLinesAreMerged() { ... }

// 4) Katta hajm: chegaralar ishlaydimi.
@Test void orderWithMaxLinesIsRejected() { ... }

// 5) Eski ma'lumot: migratsiyadan oldin yaratilgan qatorlar.
@Test void handlesLegacyRowsWithNullRiskScore() { ... }
// Bu eng ko'p o'tkazib yuboriladigan holat: yangi kod toza ma'lumotda
// ishlaydi, lekin prodda eski shakldagi qatorlar bor (25.3).

// 6) Unicode va maxsus belgilar.
@Test void customerNameWithApostropheAndCyrillic() { ... }
// O'zbek tilidagi ismlar (G'ayrat, O'ktam) apostrof bilan - SQL, JSON,
// CSV va URL da alohida tekshirish talab qiladi.
```

### 34.9 Yetishmayotgan holatni review izohida ko'rsatish

Review izohi "testlar yetarli emas" shaklida bo'lsa, muallif nima qilishni bilmaydi. To'g'ri shakl - aniq holatni va nega muhimligini aytish.

```text
# Yomon shakl.
"Test coverage past, ko'proq test kerak."

# Yaxshi shakl: aniq holat, sabab, kutilgan natija.
suggest (test): discountFor uchun uch holat qamralmagan.

1. total = MIN_TOTAL aynan (100000.00).
   Nega: hozir `isLessThan` ishlatilgan. Agar u `isLessThanOrEqual` ga
   o'zgarsa (yoki teskari), hech bir test buni tutmaydi. Chegirma
   chegarasi biznes uchun aniq raqam - uni qulflash kerak.
   Kutilgan: 15000.00 chegirma.

2. rate MAX_RATE dan oshadigan holat: GOLD (15%) + loyalty (10%) = 25%,
   MAX_RATE = 20%.
   Nega: 4-satrdagi kesish mantiqi hech qachon bajarilmaydi hozirgi
   testlarda. Kutilgan: 20% ga kesiladi.

3. customer.registeredAt aynan bir yil oldin.
   Nega: `registeredBefore` da `<` yoki `<=` farqi. Biznes bilan
   aniqlashtirish kerak: aynan bir yil - bonus beriladimi?

Birinchi ikkisi @CsvSource ga ikki qator qo'shish bilan hal bo'ladi.
```

### 34.10 Review checklisti: test to'liqligi

| Savol | Nega |
| --- | --- |
| Har sonli shart uchun uch chegara testi bormi | `<` va `<=` xatosi |
| Enum ning hamma qiymati qamralganmi | Yangi qiymat |
| Shartlar kombinatsiyasi jadval bilan tekshirilganmi | O'tkazib yuborilgan kombinatsiya |
| Holat o'tish matritsasi to'liqmi | Taqiqlangan o'tish |
| Bo'sh to'plam va bitta element holati bormi | 0 ga bo'lish, `get(0)` |
| Null va bo'sh kirish testlari bormi | NPE |
| Xato yo'llari (timeout, 500, noto'g'ri javob) qamralganmi | Prodda tez-tez bajariladi |
| Idempotentlik testi bormi | Dublikat |
| Poyga testi bormi (kritik joylarda) | Konkurentlik xatosi |
| Eski shakldagi ma'lumot bilan test bormi | Migratsiyadan keyingi holat |
| Mutatsiya bilan testni aldab o'tish mumkinmi | Yolg'on ishonch |
| Unicode va apostrof bilan test bormi | Mahalliy ma'lumot |

### 34.11 Amalda qo'llash

- [ ] Eng muhim uchta domen klassi uchun holatlar jadvalini tuzib, mavjud testlar bilan taqqoslang va bo'shliqlarni ro'yxatga oling.
- [ ] Barcha sonli chegaralar uchun "chegaradan past / aynan / yuqori" testlarini qo'shing.
- [ ] Holat mashinasi bo'lgan domen obyektlari uchun to'liq o'tish matritsasi testini yozing.
- [ ] `@EnumSource` bilan har bir enum qiymati qamralganini ta'minlang.
- [ ] Ikki va undan ko'p shartli qarorlar uchun qaror jadvalini `@CsvSource` ga aylantiring.
- [ ] Har bir tashqi integratsiya uchun kamida uch xato yo'li testini qo'shing: timeout, 5xx, noto'g'ri javob.
- [ ] Idempotentlik talab qiladigan har bir operatsiya uchun "ikki marta chaqirish" testini yozing.
- [ ] Kritik poyga holatlari uchun parallel test yozing (haqiqiy PostgreSQL bilan).
- [ ] PIT ni domen paketlariga sozlab, mutatsiya ballini o'lchang va 80 foizdan past bo'lsa bo'shliqlarni to'ldiring.

## 35. Test sifati review: assertion, izolyatsiya, beqarorlik (Test Quality)

To'liqlikdan keyingi savol - testning o'zi ishonchlimi. Yomon test ikki xil zarar keltiradi: o'tib ketadigan xatoni yashiradi (yolg'on ishonch) yoki sababsiz yiqiladi (beqarorlik) va jamoa testlarga ishonishni to'xtatadi. Ikkinchisi birinchisidan ham xavfli, chunki u butun test to'plamini qadrsizlantiradi.

### 35.1 Assertion sifati

```java
// Daraja 1: hech narsa tekshirmaydi (eng ko'p uchraydi).
@Test void createsOrder() {
    Order o = service.place(cmd);
    assertThat(o).isNotNull();                   // har qanday o'zgarishda o'tadi
}

// Daraja 2: mock chaqirilganini tekshiradi (implementatsiyaga bog'liq).
@Test void createsOrder() {
    service.place(cmd);
    verify(repository).save(any());              // nima saqlandi - ma'lum emas
}

// Daraja 3: natijani tekshiradi (yaxshi).
@Test void placedOrderHasCalculatedTotal() {
    Order o = service.place(cmdWithLines(line(2, Money.of(50_000))));
    assertThat(o.total()).isEqualByComparingTo(Money.of(100_000));
    assertThat(o.status()).isEqualTo(NEW);
}

// Daraja 4: natija va yon ta'sirni tekshiradi (eng yaxshi).
@Test void placedOrderIsPersistedWithEventPublished() {
    Order o = service.place(cmdWithLines(line(2, Money.of(50_000))));

    Order stored = orders.findById(o.id()).orElseThrow();   // haqiqatan saqlandi
    assertThat(stored.total()).isEqualByComparingTo(Money.of(100_000));
    assertThat(stored.status()).isEqualTo(NEW);
    assertThat(publishedEvents()).containsExactly(new OrderPlaced(o.id(), o.total()));
}
```

Review mezoni: testni o'qib, "qanday o'zgarish bu testni yiqitadi" degan savolga javob berish. Javob "faqat NPE" bo'lsa, test qiymatsiz.

```bash
# Kuchsiz assertion larni topish: review ning tez qadami.
grep -rn --include='*Test.java' -E \
  'assertThat\([^)]*\)\.isNotNull\(\);|assertNotNull\(|assertTrue\(true\)|assertThat\([^)]*\)\.isNotEmpty\(\);$' \
  src/test/java | head -20

# Assertion siz testlarni topish (faqat chaqiruvdan iborat).
for f in $(grep -rl --include='*Test.java' '@Test' src/test/java); do
  tests=$(grep -c '@Test' "$f")
  asserts=$(grep -cE 'assert|verify|expect|should' "$f")
  [ "$asserts" -lt "$tests" ] && echo "$f: $tests test, $asserts assertion"
done
```

### 35.2 Mock ni haddan ortiq ishlatish

```java
// Naqsh: hamma narsa mock, test faqat o'z mocklarini tekshiradi.
@Test
void calculatesInvoice() {
    when(taxService.vatFor(any())).thenReturn(Money.of(12_000));
    when(discountService.discountFor(any())).thenReturn(Money.of(5_000));
    when(repository.save(any())).thenAnswer(i -> i.getArgument(0));

    Invoice inv = service.create(order);

    verify(taxService).vatFor(order);
    verify(discountService).discountFor(order);
    verify(repository).save(any());
}
// Bu test nimani tekshiradi? Faqat chaqiruvlar ketma-ketligini. Agar
// `create` ichidagi arifmetika xato bo'lsa (vat ni ayirish o'rniga
// qo'shish), test o'tadi. Review izohi: natija qiymati tekshirilishi kerak.

// Yaxshiroq: haqiqiy hisob mantiqini sinash, faqat chegarani mock qilish.
@Test
void invoiceTotalIncludesVatMinusDiscount() {
    // Haqiqiy kalkulyatorlar - ular sof funksiya, mock kerak emas.
    InvoiceService service = new InvoiceService(new VatCalculator(), new DiscountCalculator());

    Invoice inv = service.create(orderWithTotal(Money.of(100_000), GOLD));

    assertThat(inv.net()).isEqualByComparingTo(Money.of(100_000));
    assertThat(inv.vat()).isEqualByComparingTo(Money.of(12_000));
    assertThat(inv.discount()).isEqualByComparingTo(Money.of(15_000));
    assertThat(inv.total()).isEqualByComparingTo(Money.of(97_000));   // 100000+12000-15000
}
```

Review qoidasi: mock faqat chegarada (tashqi servis, tarmoq, vaqt, tasodif) ishlatiladi. Domen obyektlari va sof hisob mantiqi mock qilinmaydi - ular tez va determinantli.

### 35.3 Beqaror (flaky) testlar

Beqaror test - o'zgarmagan kodda ba'zan o'tadigan, ba'zan yiqiladigan test. Ularning sabablari cheklangan ro'yxatda va review da aniqlash mumkin.

| Sabab | Belgisi diffda | Yechim |
| --- | --- | --- |
| Haqiqiy vaqt | `LocalDate.now()`, `Instant.now()` | `Clock` inyeksiyasi |
| Uyqu bilan kutish | `Thread.sleep(100)` | Awaitility yoki sinxron signal |
| Tartibga tayanish | `assertThat(list).containsExactly(...)` tartibsiz manbadan | `containsExactlyInAnyOrder` |
| Umumiy holat | `static` maydon, umumiy baza | Har test uchun izolyatsiya |
| Test tartibi | Bir test ikkinchisiga tayanadi | `@DirtiesContext` yoki tozalash |
| Tasodifiy ma'lumot | `Random` seed siz | Belgilangan seed |
| Parallel ijro | Bir xil resursga tegish | Alohida ma'lumot yoki `@Isolated` |
| Tarmoq | Haqiqiy tashqi servis | Mock server (WireMock) |
| Vaqt zonasi | Server zonasiga tayanish | Aniq zona |
| Portga bog'lanish | Qattiq port | Tasodifiy port |

```java
// Eng ko'p uchraydigan beqarorlik: sleep bilan kutish.
@Test
void sendsNotificationAsync() throws Exception {
    service.place(cmd);
    Thread.sleep(500);                           // ba'zan yetmaydi, har doim sekin
    verify(mailer).send(any());
}

// To'g'ri: shartni kutish, belgilangan vaqt oynasida.
@Test
void sendsNotificationAsync() {
    service.place(cmd);
    await().atMost(Duration.ofSeconds(5))
           .pollInterval(Duration.ofMillis(50))
           .untilAsserted(() -> verify(mailer).send(any()));
}
// Foydasi: tez holatda darhol o'tadi, sekin holatda 5 sekund kutadi,
// va yiqilganda aniq xabar beradi.

// Vaqt: Clock bilan to'liq nazorat.
@Test
void subscriptionExpiresAfterOneYear() {
    Clock clock = Clock.fixed(Instant.parse("2026-10-04T00:00:00Z"), ZoneOffset.UTC);
    Subscription s = new Subscription(period(2025, 10, 4, 2026, 10, 3), price);
    assertThat(s.isExpired(clock)).isTrue();
    // Hech qachon o'zgarmaydi: bugungi sanaga bog'liq emas.
}
```

### 35.4 Test izolyatsiyasi

```java
// Naqsh: testlar umumiy bazani ishlatadi va bir-biriga ta'sir qiladi.
@SpringBootTest
class OrderServiceTest {
    @Test void test1() { service.place(cmd); assertThat(orders.count()).isEqualTo(1); }
    @Test void test2() { service.place(cmd); assertThat(orders.count()).isEqualTo(1); }
    // Ikkinchi test birinchisidan keyin yiqiladi: count = 2.
}

// Yechim 1: @Transactional - har test oxirida rollback (eng tez).
@SpringBootTest
@Transactional
class OrderServiceTest { }
// Diqqat: bu yondashuv tranzaksiya xulqini yashiradi - commit bo'lmagani
// uchun `AFTER_COMMIT` listener lar ishlamaydi va poyga testlari mumkin
// emas. Shu sababli tranzaksiya mantiqini sinaydigan testlar uchun
// boshqa usul kerak.

// Yechim 2: har test oldidan tozalash (aniq va ishonchli).
@BeforeEach
void cleanDatabase() {
    jdbc.execute("TRUNCATE orders, order_line, payment CASCADE");
}

// Yechim 3: har test o'z ma'lumotini yaratadi (unique kalitlar bilan).
private String uniqueEmail() { return "test-" + UUID.randomUUID() + "@example.com"; }
// Bu usul parallel ijroga ham imkon beradi - eng masshtablanadigan yo'l.
```

### 35.5 Test nomlari va diagnostika

```java
// Nomi hech narsa aytmaydi: yiqilganda nima buzilganini bilmaymiz.
@Test void test1() { }
@Test void orderTest() { }
@Test void shouldWork() { }

// Nomi xulqni aytadi: CI loglarida o'qiladi.
@Test void cancellingShippedOrderIsRejected() { }
@Test void totalIncludesVatForDomesticCustomers() { }
@Test void duplicateIdempotencyKeyReturnsOriginalResponse() { }

// Assertion xabari: yiqilganda kontekst beradi.
assertThat(order.total())
    .as("buyurtma %s uchun jami summa (2 qator x 50000)", order.number())
    .isEqualByComparingTo(Money.of(100_000));
// Yiqilganda: "buyurtma ORD-123 uchun jami summa (2 qator x 50000)
// expected: 100000 but was: 50000" - sabab darhol ko'rinadi.
```

### 35.6 Test ma'lumotini qurish

```java
// Naqsh: har testda uzun qurilish kodi - test maqsadi ko'rinmaydi.
@Test void test() {
    Customer c = new Customer();
    c.setName("Ali"); c.setEmail("ali@x.com"); c.setTier(GOLD);
    c.setRegisteredAt(LocalDate.of(2020, 1, 1)); c.setPhone("+998901234567");
    Order o = new Order();
    o.setCustomer(c); o.setStatus(NEW); o.setCreatedAt(Instant.now());
    // ... 15 qator; asl maqsad: GOLD mijoz uchun chegirma
}

// To'g'ri: test ma'lumoti quruvchisi, faqat muhim qism ko'rinadi.
@Test void goldCustomerGetsFifteenPercent() {
    Order order = anOrder()
        .forCustomer(aCustomer().withTier(GOLD))     // qolgani standart
        .withLine(2, Money.of(50_000))
        .build();

    assertThat(calculator.discountFor(order)).isEqualByComparingTo(Money.of(15_000));
}
// Review foydasi: testni o'qiyotgan odam darhol ko'radi - GOLD va summa
// muhim, qolgani ahamiyatsiz. Builder esa yangi majburiy maydon
// qo'shilganda bitta joyda tuzatiladi.
```

### 35.7 Testlardagi anti-naqshlar

| Anti-naqsh | Nega yomon |
| --- | --- |
| Testdagi mantiq (`if`, sikl) | Test o'zi xato bo'lishi mumkin |
| Kutilgan qiymatni hisoblash | Kod bilan bir xil xatoni takrorlaydi |
| Bitta testda ko'p stsenariy | Yiqilganda joy noaniq |
| Tasodifiy ma'lumot (seed siz) | Takrorlanmaydigan yiqilish |
| `@Disabled` izohsiz | Abadiy o'chirilgan test |
| `try/catch` bilan istisnoni yutish | Test har doim o'tadi |
| Prod bazasiga ulanish | Xavfli va beqaror |
| Juda ko'p `@SpringBootTest` | Sekin pipeline |
| Testni tuzatish uchun kodni o'zgartirish | Niyat buziladi |
| Assertion dan keyin kod | Yetib bo'lmaydigan tekshiruvlar |

```java
// Kutilgan qiymatni hisoblash: eng nozik anti-naqsh.
@Test void calculatesVat() {
    BigDecimal expected = total.multiply(new BigDecimal("0.12"));   // kod bilan bir xil
    assertThat(calculator.vat(total)).isEqualByComparingTo(expected);
}
// Agar stavka noto'g'ri bo'lsa (0.12 o'rniga 0.15 bo'lishi kerak bo'lsa),
// test ham xato stavka bilan hisoblaydi va o'tadi.
// To'g'ri: kutilgan qiymat qo'lda yozilgan konstanta.
assertThat(calculator.vat(Money.of(100_000))).isEqualByComparingTo(Money.of(12_000));

// try/catch bilan yutish: test hech narsa tekshirmaydi.
@Test void test() {
    try { service.doSomething(); }
    catch (Exception e) { /* ignore */ }         // istisno bo'lsa ham o'tadi
}
```

### 35.8 Test ijro vaqti

Sekin test to'plami - jarayon muammosi: jamoa testlarni lokalda ishga tushirishni to'xtatadi va xatolar CI ga ko'chadi.

```bash
# Eng sekin testlarni topish: review va optimizatsiya uchun.
./mvnw test
# Surefire hisobotlaridan vaqtni chiqarish:
for f in target/surefire-reports/*.xml; do
  awk -F'"' '/<testsuite /{print $(NF-1)" "$2}' "$f" 2>/dev/null
done | sort -rn | head -15

# Spring kontekst necha marta qurilgan (eng katta sekinlik manbasi).
grep -rc 'Starting .*Test' target/surefire-reports/*.txt 2>/dev/null | head

# Review izohi: har xil @MockBean kombinatsiyasi YANGI kontekst yaratadi.
# 20 xil kombinatsiya = 20 kontekst = 20 x ishga tushish vaqti.
# Yechim: @MockBean larni umumiy bazaviy klassga yig'ish.
```

| Test turi | Maqbul vaqt | Chegara |
| --- | --- | --- |
| Unit (domen) | < 10 ms | 50 ms |
| Spring slice (`@WebMvcTest`) | < 1 s | 3 s |
| Integratsion (Testcontainers) | < 5 s | 15 s |
| Butun unit to'plami | < 1 daqiqa | 3 daqiqa |
| Butun CI pipeline | < 10 daqiqa | 20 daqiqa |

### 35.9 Review checklisti: test sifati

| Savol | Nega |
| --- | --- |
| Assertion qiymatni tekshiradimi | Yolg'on ishonch |
| `isNotNull` yolg'iz ishlatilmaydimi | Hech narsa tekshirilmaydi |
| Mock faqat chegarada ishlatilganmi | Implementatsiya testi |
| `Thread.sleep` bormi | Beqarorlik va sekinlik |
| Vaqt `Clock` orqalimi | Sana bilan bog'liq yiqilish |
| Testlar bir-biridan mustaqilmi | Tartibga bog'liqlik |
| Test nomi xulqni aytadimi | Diagnostika |
| Kutilgan qiymat qo'lda yozilganmi | Bir xil xatoni takrorlash |
| Testda mantiq (`if`, sikl) yo'qmi | Test xatosi |
| `@Disabled` sabab va tiket bilanmi | O'lik test |
| Test ma'lumoti builder bilanmi | O'qiluvchanlik va yangilash |
| Ijro vaqti chegaradami | Lokalda ishlatilmaslik |

### 35.10 Amalda qo'llash

- [ ] Kuchsiz assertion larni (`isNotNull` yolg'iz, `assertNotNull`) topib, ularni qiymat tekshiruviga aylantiring.
- [ ] `Thread.sleep` ishlatilgan testlarni Awaitility ga o'tkazing.
- [ ] Domen kodida `Instant.now()` va `LocalDate.now()` ni `Clock` inyeksiyasiga o'tkazib, testlarni `Clock.fixed` ga asoslang.
- [ ] Faqat `verify(...)` bilan tugaydigan testlarni toping va natija tekshiruvini qo'shing.
- [ ] Test izolyatsiyasi strategiyasini kelishib oling (tranzaksion rollback, truncate yoki unique ma'lumot) va `REVIEW.md` ga yozing.
- [ ] Test ma'lumoti uchun builder yoki fabrika klasslarini kiritib, uzun qurilish kodini olib tashlang.
- [ ] `@Disabled` testlarni sanab, har biriga tiket va sabab qo'shing yoki o'chirib tashlang.
- [ ] Eng sekin 15 testni aniqlab, Spring kontekst kombinatsiyalarini kamaytirishni rejalashtiring.
- [ ] Beqaror testlarni aniqlash uchun CI da testlarni kuniga bir marta 3 takror ishga tushirib, natijani kuzatib boring.

## 36. Test turi va integratsion test review (Test Types and Integration Tests)

Uchinchi test savoli - to'g'ri daraja tanlanganmi. Bitta xato ikki shaklda bo'ladi: mantiqni integratsion testda sinash (sekin va mo'rt) yoki integratsiyani unit testda sinash (hech narsa tekshirilmaydi). Review da bu tanlovni baholash oson, chunki belgilar aniq.

### 36.1 Daraja tanlash mezoni

| Nima sinaladi | To'g'ri daraja | Belgisi noto'g'ri tanlanganining |
| --- | --- | --- |
| Hisob, qoida, shart | Unit (domen) | `@SpringBootTest` bilan sinash |
| Validatsiya annotatsiyalari | `@WebMvcTest` yoki validator unit | Butun kontekst |
| So'rov mapping, status, JSON shakli | `@WebMvcTest` | Haqiqiy baza bilan |
| JPA mapping, so'rov, migratsiya | `@DataJpaTest` + Testcontainers | H2 yoki mock |
| Tranzaksiya chegarasi, qulf, poyga | Integratsion (haqiqiy PostgreSQL) | Mock repository |
| Tashqi HTTP integratsiya | WireMock bilan | Haqiqiy servis |
| Butun oqim (bir necha komponent) | Integratsion, kam sonli | Hamma narsa shu darajada |
| Xavfsizlik qoidalari | `@SpringBootTest` + MockMvc | Faqat unit |

```java
// Noto'g'ri daraja: sof hisob butun kontekst bilan sinalgan.
@SpringBootTest                                  // 8 sekund ishga tushish
class DiscountCalculatorTest {
    @Autowired DiscountCalculator calculator;
    @Test void goldGetsFifteenPercent() { ... }  // hech qanday bog'liqlik kerak emas
}
// Review izohi: DiscountCalculator ning bog'liqligi yo'q (yoki faqat sof
// funksiyalar). `new DiscountCalculator()` bilan sinash 10 ms oladi va
// 8 sekund tejaydi. 50 shunday test = pipeline da 7 daqiqa.

// To'g'ri: oddiy unit test.
class DiscountCalculatorTest {
    private final DiscountCalculator calculator = new DiscountCalculator();
    @Test void goldGetsFifteenPercent() { ... }
}
```

### 36.2 H2 va haqiqiy PostgreSQL

Bu review da eng ko'p bahs tug'diradigan mavzu, lekin javob aniq: PostgreSQL ishlatadigan loyihada testlar ham PostgreSQL da ishlashi kerak.

| Farq | H2 da | PostgreSQL da |
| --- | --- | --- |
| `jsonb` | Yo'q yoki taqlid | To'liq |
| Massiv turlari | Cheklangan | To'liq |
| `ON CONFLICT` | Qisman | To'liq |
| Partial va ifoda indekslari | Yo'q | Bor |
| `FOR UPDATE SKIP LOCKED` | Yo'q | Bor |
| Izolyatsiya xulqi | Boshqacha | Haqiqiy MVCC |
| Tur konversiyalari | Yumshoqroq | Qattiq |
| `timestamptz` semantikasi | Farq qiladi | Haqiqiy |
| Migratsiyalar | Ba'zilari ishlamaydi | Haqiqiy |
| Reja va indeks ishlashi | Ma'nosiz | Haqiqiy |
| Window funksiyalar, CTE | Qisman | To'liq |
| `citext`, `pg_trgm`, kengaytmalar | Yo'q | Bor |

```java
// To'g'ri shakl: Testcontainers, bir marta ishga tushadigan konteyner.
@TestConfiguration(proxyBeanMethods = false)
public class PostgresTestConfig {

    // @ServiceConnection: Spring Boot 3.1+ - URL va kalitlarni o'zi ulaydi.
    @Bean
    @ServiceConnection
    PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>(DockerImageName.parse("postgres:16-alpine"))
            // Qayta ishlatish: lokalda testlar orasida konteyner saqlanadi
            // (~/.testcontainers.properties da testcontainers.reuse.enable=true).
            .withReuse(true);
    }
}

// Bazaviy klass: bitta kontekst, bitta konteyner - butun to'plam uchun.
@SpringBootTest
@Import(PostgresTestConfig.class)
public abstract class IntegrationTest {
    @Autowired protected MockMvcTester mvc;
    // Tozalash strategiyasi bir joyda (35.4).
    @AfterEach void clean() { jdbc.execute("TRUNCATE orders, payment CASCADE"); }
}
// Review foydasi: har test klassi o'z konfiguratsiyasini yozmaydi, ya'ni
// Spring kontekst bir marta quriladi va pipeline tez ishlaydi.
```

### 36.3 Spring test slice larini to'g'ri ishlatish

```java
// @WebMvcTest: faqat web qatlam, servis mock qilinadi - tez.
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    @Autowired MockMvcTester mvc;
    @MockitoBean OrderService service;           // Spring Boot 3.4+ nomi

    @Test
    void returnsValidationErrorForEmptyLines() {
        assertThat(mvc.post().uri("/api/orders")
                      .contentType(APPLICATION_JSON)
                      .content("""
                               {"customer": {"id": "..."}, "lines": []}
                               """))
            .hasStatus(HttpStatus.BAD_REQUEST)
            .bodyJson().extractingPath("$.errors[0].field").isEqualTo("lines");
    }
    // Bu test aynan web qatlamni sinaydi: validatsiya, status, JSON shakli.
}

// @DataJpaTest: faqat JPA, haqiqiy baza bilan.
@DataJpaTest
@Import(PostgresTestConfig.class)
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)   // H2 ni almashtirmaslik
class OrderRepositoryTest {
    @Test
    void findsOpenOrdersWithLinesInSingleQuery() { ... }
}
// Diqqat: @DataJpaTest standart holatda @Transactional - har test rollback.
// Bu poyga va qulf testlari uchun yaroqsiz (35.4).

// @JsonTest: serializatsiya shaklini qulflash.
@JsonTest
class OrderResponseJsonTest {
    @Autowired JacksonTester<OrderResponse> json;

    @Test
    void serializesMoneyAsStringAndDateAsIso() throws Exception {
        OrderResponse r = new OrderResponse(ID, "ORD-1", "NEW",
                new BigDecimal("1000.00"), "UZS", OffsetDateTime.parse("2026-10-04T12:00:00Z"));
        assertThat(json.write(r)).isEqualToJson("""
            {"id":"...","number":"ORD-1","status":"NEW",
             "total":"1000.00","currency":"UZS","createdAt":"2026-10-04T12:00:00Z"}
            """);
    }
    // Review foydasi: API shakli test bilan qulflangan. Jackson
    // sozlamasi tasodifan o'zgarsa yoki maydon qo'shilsa, test gapiradi
    // (37-bob: orqaga moslik).
}
```

### 36.4 Tashqi servislarni sinash

```java
// Noto'g'ri: haqiqiy tashqi servisga murojaat.
@Test void fetchesRate() {
    Rate rate = client.rateFor("USD");           // internetga chiqadi
    assertThat(rate).isNotNull();                // beqaror va ma'nosiz
}

// To'g'ri: WireMock bilan - xulqni to'liq nazorat qilish.
@SpringBootTest
@AutoConfigureWireMock(ports = 0)                // tasodifiy port
class RateClientTest {

    @Test
    void parsesSuccessfulResponse() {
        stubFor(get("/rates/USD").willReturn(okJson("""
            {"currency":"USD","rate":"12750.00","asOf":"2026-10-04"}
            """)));
        assertThat(client.rateFor("USD").value()).isEqualByComparingTo("12750.00");
    }

    @Test
    void retriesOnServerErrorThenSucceeds() {
        stubFor(get("/rates/USD").inScenario("retry")
            .whenScenarioStateIs(STARTED)
            .willReturn(serverError()).willSetStateTo("second"));
        stubFor(get("/rates/USD").inScenario("retry")
            .whenScenarioStateIs("second")
            .willReturn(okJson("""{"rate":"12750.00"}""")));

        assertThat(client.rateFor("USD")).isNotNull();
        verify(2, getRequestedFor(urlEqualTo("/rates/USD")));   // retry ishladi
    }

    @Test
    void failsFastOnTimeout() {
        stubFor(get("/rates/USD").willReturn(ok().withFixedDelay(5_000)));
        long start = System.nanoTime();
        assertThatThrownBy(() -> client.rateFor("USD"))
            .isInstanceOf(RateServiceUnavailable.class);
        // Timeout 2 sekund bo'lishi kerak: 5 sekund kutmaydi.
        assertThat(Duration.ofNanos(System.nanoTime() - start))
            .isLessThan(Duration.ofSeconds(3));
    }

    @Test
    void rejectsMalformedResponse() {
        stubFor(get("/rates/USD").willReturn(okJson("""{"rate":"not-a-number"}""")));
        assertThatThrownBy(() -> client.rateFor("USD"))
            .isInstanceOf(InvalidGatewayResponse.class);
    }
}
// Review talabi: har bir tashqi integratsiya uchun kamida shu to'rt test -
// muvaffaqiyat, xato, timeout, noto'g'ri javob (34.5).
```

### 36.5 Kontrakt testlari

```java
// Review savoli: ichki servislar orasidagi shartnoma qanday himoyalangan?
// Variant 1: iste'molchi tomonidan boshqariladigan kontrakt (Pact).
// Variant 2: sxema registri (Avro, Protobuf, JSON Schema).
// Variant 3: provayder tomonda shaklni qulflaydigan test (eng oddiy).

// Variant 3 ning amaliy shakli: API javobi shaklini snapshot qilish.
@Test
void orderResponseContractIsStable() throws Exception {
    String actual = mvc.get().uri("/api/orders/{id}", KNOWN_ID)
                       .exchange().getResponse().getContentAsString();
    // Fayl: src/test/resources/contracts/order-response.json
    assertThat(actual).isEqualToIgnoringWhitespace(
        Files.readString(Path.of("src/test/resources/contracts/order-response.json")));
}
// Review foydasi: javob shakli o'zgarsa, test yiqiladi va muallif
// ongli qaror qabul qilishga majbur bo'ladi: bu breaking change mi?
// Snapshot ni yangilash - ongli harakat, tasodifiy emas.
```

### 36.6 Migratsiya va sxema testlari

```java
// Review talabi: migratsiyalar test bilan qoplangan (25.7).
@Test
void jpaEntitiesMatchFlywaySchema() {
    // Hibernate sxema validatsiyasi: entity va jadval mos kelmasa,
    // kontekst ishga tushmaydi.
    // spring.jpa.hibernate.ddl-auto=validate (test profilida)
    // Bu test kontekst qurilishining o'zi bilan bajariladi.
}

// Qo'shimcha: ortiqcha ustun va indekslarni aniqlash.
@Test
void noUnusedColumnsInCriticalTables() {
    List<String> columns = jdbc.queryForList("""
        SELECT column_name FROM information_schema.columns
         WHERE table_name = 'orders'
        """, String.class);
    // Entity maydonlari bilan solishtirish: bazada bor, kodda yo'q
    // ustunlar - yoki meros, yoki esdan chiqqan migratsiya.
    assertThat(columns).doesNotContain("legacy_status", "temp_flag");
}
```

```yaml
# Test profilida majburiy sozlamalar: review da shu ro'yxat tekshiriladi.
spring:
  jpa:
    hibernate:
      ddl-auto: validate        # entity va sxema mosligini tekshiradi
    open-in-view: false         # lazy xatolari testda chiqadi
    properties:
      hibernate:
        generate_statistics: true    # so'rov sonini o'lchash uchun
  flyway:
    enabled: true               # sxema migratsiyalardan quriladi, ddl-auto dan emas
  sql:
    init:
      mode: never               # schema.sql bilan chalkashmaslik
```

### 36.7 Testlar nimani qoplamasligi kerak

Review da teskari xato ham bo'ladi: ortiqcha test yozish. Ortiqcha testlar qo'llab-quvvatlash yuki beradi va refactoringni qiyinlashtiradi.

| Qoplanmasligi kerak | Nega |
| --- | --- |
| Getter va setter | Hech qanday mantiq yo'q |
| Framework xulqi | Spring ni sinash bizning ishimiz emas |
| Generated kod | Mapper, DTO, protobuf |
| Konfiguratsiya qiymatlari | `@Value` ning o'qilishi |
| Bir xil mantiq ikki darajada | Unit va integratsion bir xil shartni |
| Shaxsiy metodlar to'g'ridan-to'g'ri | Public xulq orqali |
| Log xabarlari matni | Mo'rt va qiymatsiz |
| `toString` natijasi | Maskalash tashqari (32.1) |

Review mezoni: test yiqilsa, u haqiqiy xatoni ko'rsatadimi yoki shunchaki kod o'zgarganini. Ikkinchi holatda test qiymat bermaydi, lekin refactoring narxini oshiradi.

### 36.8 Review checklisti: test turlari

| Savol | Nega |
| --- | --- |
| Sof mantiq unit testdami | Sekin pipeline |
| Baza testlari haqiqiy PostgreSQL dami | H2 farqlari |
| `@SpringBootTest` soni cheklanganmi | Kontekst qurilishi |
| Kontekst kombinatsiyalari kamaytirilganmi | Har kombinatsiya yangi kontekst |
| Tashqi servis WireMock bilanmi | Beqarorlik |
| Har integratsiya uchun 4 xato yo'li bormi | Qamralmagan xato holatlari |
| Migratsiyalar test bilan qoplanganmi | Deploy xatosi |
| `ddl-auto: validate` yoqilganmi | Entity va sxema farqi |
| API javob shakli qulflangangmi | Tasodifiy breaking change |
| Tranzaksiya testlari rollback siz ishlaydimi | Yashirin xulq |
| Getter va framework xulqi sinalmayaptimi | Ortiqcha yuk |

### 36.9 Amalda qo'llash

- [ ] `@SpringBootTest` ishlatadigan testlarni sanab, ularning qanchasi sof mantiqni sinayotganini aniqlang va unit testga o'tkazing.
- [ ] H2 ishlatilayotgan bo'lsa, Testcontainers + PostgreSQL ga o'tish rejasini tuzing.
- [ ] Bitta bazaviy integratsion test klassini yaratib, barcha integratsion testlarni unga asoslang (bitta kontekst).
- [ ] Testcontainers `withReuse(true)` ni lokal ishlab chiqish uchun yoqing.
- [ ] Har bir tashqi integratsiya uchun WireMock bilan to'rt test (muvaffaqiyat, xato, timeout, noto'g'ri javob) yozing.
- [ ] Test profilida `ddl-auto: validate` va `open-in-view: false` ni yoqing.
- [ ] Asosiy API javoblari uchun shakl snapshot testlarini qo'shing.
- [ ] Getter/setter va framework xulqini sinaydigan testlarni toping va olib tashlang.
- [ ] Spring kontekst necha marta qurilayotganini o'lchab, kombinatsiyalarni kamaytirish rejasini tuzing.

# VIII. Kesishgan sifat

## 37. API moslik va breaking change review (API Compatibility)

API o'zgarishi diffda oddiy ko'rinadi: maydon nomi tuzatildi, tur aniqlashtirildi, ortiqcha maydon olib tashlandi. Lekin API ning narxi tashqarida: mobil ilovaning eski versiyasi, hamkor integratsiyasi, boshqa jamoaning servisi. Shu sababli API ga tegadigan PR da reviewer bitta narsani aniqlashi kerak - kim sinadi va qachon.

### 37.1 Breaking change katalogi

| O'zgarish | Breaking mi | Izoh |
| --- | --- | --- |
| Yangi ixtiyoriy maydon javobda | Yo'q | Qattiq deserializatsiya ishlatadigan mijoz sinishi mumkin |
| Yangi majburiy maydon so'rovda | Ha | Eski mijoz yubormaydi |
| Yangi ixtiyoriy maydon so'rovda | Yo'q | - |
| Maydon olib tashlash javobdan | Ha | Mijoz o'qiyotgan bo'lishi mumkin |
| Maydon nomini o'zgartirish | Ha | Ikkisi ham (olib tashlash + qo'shish) |
| Maydon turini o'zgartirish | Ha | `"1000"` va `1000` farqi |
| Maydonni nullable qilish | Ha | Mijoz null ni kutmaydi |
| Maydonni majburiy qilish | Ha | Eski so'rovlar rad etiladi |
| Enum ga yangi qiymat (javobda) | Ehtimol | Mijoz `switch` da `default` siz bo'lsa |
| Enum dan qiymat olib tashlash | Ha | - |
| Status kodini o'zgartirish | Ha | Mijoz mantiqi unga tayanadi |
| Xato javob shaklini o'zgartirish | Ha | Xato ishlash kodi sinadi |
| Validatsiyani qattiqlashtirish | Ha | Avval o'tgan so'rovlar rad etiladi |
| Validatsiyani yumshatish | Yo'q | - |
| Standart qiymatni o'zgartirish | Ha | Jim xulq o'zgarishi - eng xavfli |
| Tartiblashni o'zgartirish | Ehtimol | Mijoz tartibga tayanishi mumkin |
| Pagination standartini o'zgartirish | Ha | `size=20` dan `size=10` ga |
| Endpoint URL ini o'zgartirish | Ha | - |
| Rate limit qo'shish | Ehtimol | Yuqori yukli mijoz sinadi |
| Autentifikatsiya talabini qo'shish | Ha | - |

Eng xavfli qator - standart qiymatni o'zgartirish, chunki u hech qanday xato bermaydi: mijoz ishlaydi, lekin boshqa natija oladi.

### 37.2 Kim ishlatayotganini aniqlash

Review izohida "bu breaking change" deyish yetarli emas - kim sinishini bilish kerak.

```bash
# Endpoint dan kim foydalanayotganini aniqlash: dalil to'plash.
# 1) Access loglardan: User-Agent va versiya bo'yicha.
#    (ELK, Loki yoki CloudWatch da)
#    sum by (user_agent) (rate(http_requests_total{uri="/api/orders"}[7d]))

# 2) Mijoz versiyalari bo'yicha: agar header yuborilsa.
#    sum by (client_version) (rate(http_requests_total{uri=~"/api/orders.*"}[30d]))

# 3) Kod bazasida: boshqa servislar shu endpointni chaqiradimi.
#    (monorepo bo'lsa)
grep -rn '/api/orders' --include='*.java' --include='*.ts' --include='*.kt' .. | grep -v test

# 4) API gateway yoki service mesh statistikasi.
```

Review izohining shakli: "`total` maydonini satrdan raqamga o'zgartirish - breaking change. Oxirgi 30 kunda bu endpointni uch mijoz ishlatgan: mobil ilova 2.x (so'rovlarning 40 foizi), mobil 3.x (55 foizi) va hamkor integratsiyasi (5 foizi). Mobil 2.x yangilanmaydi - ya'ni foydalanuvchilarning 40 foizida buyurtma ekrani sinadi."

### 37.3 Versiyalash strategiyalari

| Strategiya | Qachon mos | Narxi |
| --- | --- | --- |
| Hech qanday versiyalash (faqat mos o'zgarishlar) | Ichki API, nazoratdagi mijozlar | Qattiq disiplina |
| URL versiyasi (`/v1/`, `/v2/`) | Ommaviy API | Ikki kod yo'li |
| Header versiyasi (`Accept: ...v2+json`) | Nozik versiyalash | Keshlash murakkabligi |
| Maydon darajasida evolyutsiya | Barcha holatlar | Eski maydonlarni saqlash |
| Yangi endpoint | Shakl tubdan o'zgarganda | Ikki endpoint |

```java
// Eng amaliy yondashuv: maydon darajasida evolyutsiya (expand and contract).
public record OrderResponse(
        UUID id,
        String number,
        @Deprecated(since = "2026-10", forRemoval = true)
        String total,                            // eski: satr
        BigDecimal totalAmount,                  // yangi: raqam
        String currency) {

    // Ikkisi ham to'ldiriladi: eski mijoz `total` ni, yangi
    // `totalAmount` ni o'qiydi. Olib tashlash sanasi e'lon qilinadi.
    public static OrderResponse from(Order o) {
        return new OrderResponse(o.id().value(), o.number().value(),
                                 o.total().amount().toPlainString(),
                                 o.total().amount(), o.total().currency().getCurrencyCode());
    }
}
// Review talabi: deprecation uchun sana, e'lon qilish yo'li va
// o'chirish shartlari (masalan "mobil 2.x foydalanuvchilari 1 foizdan
// kam bo'lganda") yozilishi kerak.
```

### 37.4 Deserializatsiya qattiqligi

```java
// Mijoz tomonda: qattiq deserializatsiya yangi maydonga sindiradi.
ObjectMapper mapper = new ObjectMapper();
mapper.enable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);   // standart yoqilgan!
// Agar sizning servisingiz javobga yangi maydon qo'shsa, shunday
// sozlangan mijoz sinadi - ya'ni "mos" o'zgarish ham breaking bo'ladi.

// Review tavsiyasi ikki tomonga:
// 1) Iste'molchi sifatida: noma'lum maydonlarga chidamli bo'lish.
spring.jackson.deserialization.fail-on-unknown-properties=false
// 2) Provayder sifatida: mijozlarning qattiqligini bilish va
//    yangi maydon qo'shishni ham e'lon qilish.
```

### 37.5 Ichki API: modullar orasidagi shartnoma

```java
// Ichki modullar orasidagi shartnoma ham API: uning o'zgarishi
// boshqa jamoaning ishini to'xtatadi.
// Review savoli: bu metodni kim chaqiradi va u xabardor qilinganmi?

// Yordam: deprecation va kompilyatsiya ogohlantirishi.
@Deprecated(since = "2026-10", forRemoval = true)
public Money calculateTotal(Order order) {
    return calculateTotal(order, TaxContext.domestic());    // yangi shakl
}
// Foydasi: chaqiruvchilar kompilyatsiya paytida ogohlantirish oladi va
// migratsiya uchun vaqt bo'ladi.

// Katta loyihada: API moslikni avtomatik tekshirish.
// japicmp yoki revapi plugini mos kelmaydigan o'zgarishni build da tutadi.
```

```xml
<!-- japicmp: public API da breaking change ni build da tutish. -->
<plugin>
  <groupId>com.github.siom79.japicmp</groupId>
  <artifactId>japicmp-maven-plugin</artifactId>
  <configuration>
    <oldVersion>
      <dependency>
        <groupId>${project.groupId}</groupId>
        <artifactId>${project.artifactId}</artifactId>
        <version>LATEST_RELEASE</version>
      </dependency>
    </oldVersion>
    <parameter>
      <onlyModified>true</onlyModified>
      <breakBuildOnBinaryIncompatibleModifications>true</breakBuildOnBinaryIncompatibleModifications>
      <includes><include>com.acme.api</include></includes>   <!-- faqat public API -->
    </parameter>
  </configuration>
</plugin>
```

### 37.6 Event va xabar sxemasi

Xabar sxemasi API dan ham qattiqroq: iste'molchilar mustaqil deploy qilinadi va eski xabarlar navbatda turgan bo'lishi mumkin.

| O'zgarish | Orqaga mos (eski iste'molchi yangi xabarni o'qiydi) | Oldinga mos (yangi iste'molchi eski xabarni o'qiydi) |
| --- | --- | --- |
| Standart qiymatli maydon qo'shish | Ha | Ha |
| Majburiy maydon qo'shish | Ha | Yo'q |
| Ixtiyoriy maydon olib tashlash | Yo'q (agar o'qilsa) | Ha |
| Maydon nomini o'zgartirish | Yo'q | Yo'q |
| Turni kengaytirish (`int` -> `long`) | Ehtimol | Yo'q |
| Enum qiymat qo'shish | Iste'molchiga bog'liq | Ha |

```java
// Event sxemasini versiyalash: eng oddiy ishlaydigan shakl.
public record OrderPlacedV2(
        UUID orderId,
        Money total,
        @Nullable PromoCode promoCode,           // yangi, ixtiyoriy
        int schemaVersion) {                     // aniq versiya raqami

    public static final int VERSION = 2;
}
// Iste'molchi tomonda:
if (event.schemaVersion() > SUPPORTED_VERSION) {
    // Noma'lum versiya: DLQ ga yuborish yoki ogohlantirish bilan
    // mavjud maydonlar bo'yicha ishlash. Jim tashlab yuborish - xato.
    log.warn("qo'llab-quvvatlanmaydigan sxema versiyasi: {}", event.schemaVersion());
    meter.counter("event.unsupported.version").increment();
}
```

### 37.7 Deprecation jarayoni

```markdown
<!-- API o'zgarishi uchun PR shabloni bo'limi -->
## API o'zgarishi

- O'zgarish turi: [ ] mos  [ ] breaking  [ ] deprecation
- Ta'sirlangan endpointlar:
- Oxirgi 30 kundagi chaqiruvlar soni va mijozlar:
- Breaking bo'lsa:
  - [ ] Mijozlar xabardor qilingan (qayerda, qachon)
  - [ ] O'tish davri muddati:
  - [ ] Eski shakl saqlanadi (qancha vaqt):
  - [ ] Monitoring: eski shakl ishlatilishi o'lchanadi
- [ ] API hujjati (OpenAPI) yangilangan
- [ ] CHANGELOG ga yozilgan
```

```java
// Eski maydon ishlatilishini o'lchash: o'chirish qarori uchun dalil.
// Agar mijoz eski maydonni o'qiyotganini bilib bo'lmasa, uning
// ishlatilishini so'rov darajasida o'lchash mumkin:
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id,
                         @RequestHeader(value = "X-Client-Version", required = false) String clientVersion) {
    meter.counter("api.orders.get", "client", clientVersion == null ? "unknown" : clientVersion)
         .increment();
    return ...;
}
// Yoki eski endpoint uchun alohida hisoblagich: o'chirish vaqtini
// raqam bilan asoslash imkonini beradi.
```

### 37.8 Review checklisti: API moslik

| Savol | Nega |
| --- | --- |
| Bu o'zgarish breaking katalogida bormi | Jim sinish |
| Kim ishlatadi va qancha trafik | Ta'sir hajmi |
| Standart qiymat o'zgardimi | Xatosiz xulq o'zgarishi |
| Validatsiya qattiqlashdimi | Avval o'tgan so'rovlar |
| Enum ga yangi qiymat qo'shildimi | Mijoz `switch` i |
| Xato javob shakli o'zgardimi | Mijoz xato ishlash kodi |
| Deprecation sanasi va rejasi bormi | Abadiy ikki shakl |
| OpenAPI hujjati yangilandimi | Mijoz noto'g'ri ma'lumot oladi |
| Event sxemasi ikki tomonga mosmi | Iste'molchi sinishi |
| Eski shakl ishlatilishi o'lchanadimi | O'chirish qarori |
| Mijozlar xabardor qilindimi | Kutilmagan uzilish |

### 37.9 Amalda qo'llash

- [ ] Breaking change katalogini `REVIEW.md` ga qo'shib, API ga tegadigan PR larda uni tekshirishni majburiy qiling.
- [ ] PR shablonida API o'zgarishi bo'limini qo'shing (o'zgarish turi, mijozlar, o'tish davri).
- [ ] Asosiy endpointlar uchun mijoz versiyasi bo'yicha trafik metrikasini qo'shing.
- [ ] `spring.jackson.deserialization.fail-on-unknown-properties=false` ni iste'molchi tomonda tekshiring.
- [ ] Public API modullari uchun japicmp yoki revapi ni build ga qo'shing.
- [ ] Event sxemalariga aniq versiya maydonini kiritib, iste'molchida noma'lum versiya uchun xulq belgilang.
- [ ] Deprecated maydon va endpointlar ro'yxatini o'chirish sanasi bilan yuritib boring.
- [ ] API javob shakllari uchun snapshot testlarini qo'shib (36.5), tasodifiy o'zgarishlarni tuting.

## 38. Performance review diffdan (Performance from a Diff)

Reviewer yuk sinovini o'tkaza olmaydi, lekin ikki narsani qila oladi: operatsiyalar sonini sanash va hajmni chamalash. Performance xatolarining katta qismi aynan shu ikki o'lchovda ko'rinadi - kod N marta ko'p ish qiladi yoki N marta ko'p ma'lumot tashiydi. Ishlash mexanikasi va napkin math `java-spring-architect-mindset.md` da; bu yerda diffdan baholash.

### 38.1 Asosiy usul: operatsiyalarni sanash

Har bir yangi kod yo'li uchun uch savol: nechta DB so'rovi, nechta tarmoq chaqiruvi, nechta obyekt yaratiladi. Javob "ma'lumot hajmiga bog'liq" bo'lsa, bu muammo belgisi.

| Operatsiya | Taxminiy narx | 1000 marta bajarilganda |
| --- | --- | --- |
| Xotiradagi hisob | nanosekundlar | sezilmaydi |
| Log yozish (buferlangan) | mikrosekundlar | millisekundlar |
| Keshdan o'qish (lokal) | mikrosekundlar | millisekundlar |
| Redis chaqiruvi (bir xil DC) | 0.2-1 ms | 0.2-1 sekund |
| DB so'rovi (indeks bilan, bir xil DC) | 0.5-3 ms | 0.5-3 sekund |
| DB so'rovi (seq scan, katta jadval) | 100 ms - sekundlar | daqiqalar |
| HTTP chaqiruvi (ichki servis) | 5-50 ms | 5-50 sekund |
| HTTP chaqiruvi (tashqi provayder) | 50-500 ms | daqiqalar |
| Fayl yozish (disk) | 1-10 ms | sekundlar |
| JSON serializatsiya (1 KB) | mikrosekundlar | millisekundlar |

Shu jadvaldan review ning asosiy qoidasi chiqadi: siklda turgan har qanday I/O - diqqat markazida. Review izohida esa raqam ko'rsatiladi: "1000 qatorli hisobotda bu 1000 HTTP chaqiruv, provayderning p99 i 200 ms - ya'ni 3 daqiqa".

### 38.2 Siklda I/O: eng ko'p uchraydigan muammo

```java
// Naqsh: har element uchun so'rov.
List<OrderDto> enrich(List<Order> orders) {
    return orders.stream().map(o -> new OrderDto(
        o.id(),
        customers.findById(o.customerId()).orElseThrow().name(),   // N so'rov
        products.nameFor(o.firstProductId())                        // yana N
    )).toList();
}

// Yechim: ommaviy yuklash (batch loading) - 2 so'rov.
List<OrderDto> enrich(List<Order> orders) {
    Set<UUID> customerIds = orders.stream().map(Order::customerId).collect(toSet());
    Map<UUID, String> names = customers.findAllById(customerIds).stream()
        .collect(toMap(Customer::id, Customer::name));

    Set<UUID> productIds = orders.stream().map(Order::firstProductId).collect(toSet());
    Map<UUID, String> products = this.products.namesByIds(productIds);

    return orders.stream()
        .map(o -> new OrderDto(o.id(), names.get(o.customerId()),
                               products.get(o.firstProductId())))
        .toList();
}
// Review diqqati: `findAllById` ham chegarasiz bo'lmasligi kerak -
// 100 000 ID bilan `IN` so'rovi PostgreSQL da rejani buzadi. Bo'laklash
// kerak: Lists.partition(ids, 1000).
```

### 38.3 Hajm: nima tashiladi

```java
// Naqsh 1: ortiqcha ustunlar.
SELECT * FROM orders WHERE ...               // 40 ustun, 3 tasi kerak
// 100 000 qator x 2 KB = 200 MB tarmoq va xotira. Projection bilan
// 100 000 x 100 bayt = 10 MB (23.7).

// Naqsh 2: ortiqcha qatorlar.
List<Order> all = orders.findByCustomer(id);     // 5000 buyurtma
return all.stream().filter(o -> o.isOpen()).limit(20).toList();   // 20 kerak
// Filtr va chegara so'rovda bo'lishi kerak.

// Naqsh 3: ortiqcha javob.
public record OrderResponse(Order order, Customer customer, List<Payment> payments,
                            List<Shipment> shipments, List<AuditEntry> audit) { }
// Mijoz ro'yxat ekranida faqat raqam va summani ko'rsatadi, lekin
// server har buyurtma uchun audit tarixini ham yuboradi.
// Review savoli: mijoz bu maydonlarning qaysilarini ishlatadi?

// Naqsh 4: ortiqcha serializatsiya.
String json = mapper.writeValueAsString(bigObject);   // satr sifatida xotirada
// Oqimli yozish: mapper.writeValue(outputStream, bigObject)
```

### 38.4 Kesh: qachon foyda, qachon zarar

```java
// Review savollari har bir yangi kesh uchun.
@Cacheable(value = "rates", key = "#currency")
public Rate rateFor(String currency) { return client.fetch(currency); }
```

1. Ma'lumot qanchalik tez eskiradi va eskirgan qiymat qabul qilinadimi. Valyuta kursi 10 daqiqa - ha; hisob qoldig'i - yo'q.
2. Hit rate qanday bo'ladi. Kalitlar soni ko'p va har biri bir marta so'ralsa, kesh faqat xotira yeydi.
3. Hajmi va TTL si bormi (16.4).
4. Kalitda foydalanuvchi yoki tenant bormi (xavfsizlik, 16.4).
5. Invalidatsiya qanday ishlaydi va ikki instansda mos keladimi.
6. Kesh to'ldirilishi momenti (cache stampede): TTL tugaganda 100 parallel so'rov bir vaqtda tashqi servisga ketadimi.

```java
// Cache stampede dan himoya: bitta so'rov to'ldiradi, qolganlar kutadi.
private final Cache<String, Rate> cache = Caffeine.newBuilder()
    .maximumSize(200)
    .refreshAfterWrite(Duration.ofMinutes(5))     // fonda yangilaydi
    .expireAfterWrite(Duration.ofMinutes(30))     // qattiq chegara
    .recordStats()
    .build(this::loadFromProvider);               // LoadingCache: bitta yuklash

// refreshAfterWrite va expireAfterWrite farqi:
// - refresh: eski qiymat qaytariladi, fonda yangilanadi (foydalanuvchi kutmaydi);
// - expire: qiymat o'chadi, keyingi so'rov kutadi.
// Review tavsiyasi: tashqi servisga bog'liq keshda ikkisi birga.
```

### 38.5 Performance regressiyasini diffdan ko'rish

| Diffdagi belgi | Nimani bildiradi |
| --- | --- |
| Yangi `@OneToMany` EAGER | Yashirin qo'shimcha so'rovlar |
| Yangi `JOIN` | Qatorlar ko'payishi, reja o'zgarishi |
| `ORDER BY` yangi ustun bo'yicha | Indeks yo'q bo'lsa - sort |
| `DISTINCT` qo'shilgan | Ko'pincha noto'g'ri `JOIN` belgisi |
| Yangi `LEFT JOIN` ko'p qatorli jadvalga | Natija portlashi |
| Siklda `save()` | Batch yo'q |
| Yangi tashqi chaqiruv | Latency qo'shiladi |
| `findAll()` | Chegarasiz yuklash |
| Yangi regex murakkab naqsh bilan | CPU va ReDoS |
| Yangi serializatsiya qatlami | Ortiqcha nusxalash |
| `parallelStream()` | Common pool bloklash |
| Sinxron chaqiruv tranzaksiyada | Ulanish ushlanishi |
| Yangi log `INFO` darajada siklda | Disk va kechikish |

```bash
# Performance xavfini diffdan qidirish.
D=$(git diff origin/main...HEAD)

echo "=== siklda DB yoki HTTP chaqiruvi (qo'lda tekshirish kerak) ==="
git diff -U10 origin/main...HEAD -- '*.java' \
  | awk '/^\+.*(for|while|\.forEach|\.stream\(\).*map)/ {inloop=1; n=0}
         inloop && /^\+.*(repository\.|repo\.|client\.|jdbc\.|restClient|webClient|\.findBy|\.save\()/ {
           print "EHTIMOLIY N+1: " $0; inloop=0 }
         inloop && ++n > 12 { inloop=0 }'

echo "=== findAll va chegarasiz so'rovlar ==="
echo "$D" | grep -nE '^\+.*(findAll\(\)|\.toList\(\)\s*;\s*$)' | head

echo "=== yangi EAGER ==="
echo "$D" | grep -nE '^\+.*FetchType\.EAGER|^\+.*@(ManyToOne|OneToOne)\s*$'

echo "=== siklda log ==="
echo "$D" | grep -nE '^\+.*log\.(info|debug)' | head
```

### 38.6 O'lchovsiz optimallashtirishni rad etish

Review ning teskari vazifasi ham bor: asossiz optimallashtirishni to'xtatish. Murakkab optimallashtirish o'qish narxini oshiradi va ko'pincha hech narsa bermaydi.

```java
// PR da: "performance uchun" qo'lda kesh va murakkab mantiq qo'shilgan.
private final Map<String, BigDecimal> precomputed = new ConcurrentHashMap<>();
private final int[] lookupTable = buildLookupTable();           // 200 satr

// Review savollari:
// 1) Bu kod qancha marta chaqiriladi? (metrikada: kuniga 400 marta)
// 2) Hozirgi vaqti qancha? (p99 = 3 ms)
// 3) Yangi vaqti qancha? (o'lchanmagan)
// 4) Bu yo'l profilda ko'rindimi? (yo'q)
// Xulosa: kuniga 400 marta chaqiriladigan 3 ms lik kod uchun 200 satr
// murakkablik - foyda kuniga bir sekunddan kam, narx esa doimiy.

// Review izohi: "Optimallashtirishdan oldin o'lchov kerak. Agar bu yo'l
// haqiqatan muammo bo'lsa, profil natijasini (async-profiler yoki JFR)
// qo'shsangiz, birga ko'ramiz. Hozirgi metrikada bu endpoint p99 = 40 ms
// va uning 35 ms i DB so'roviga ketadi - optimallashtirish shu yerda
// qaytim beradi."
```

### 38.7 Review paytida o'lchash

```bash
# Yuqori xavfli PR uchun: lokalda o'lchash va dalil to'plash.
# 1) Endpoint ni yuk bilan sinash (oldin va keyin).
#    Base branch da:
git switch main && ./mvnw -q spring-boot:run &
hey -n 2000 -c 20 -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/orders
#    PR branchda bir xil o'lchov:
git switch pr-1423 && ./mvnw -q spring-boot:run &
hey -n 2000 -c 20 -H "Authorization: Bearer $TOKEN" http://localhost:8080/api/orders
# Taqqoslash: p50, p95, p99 va so'rovlar/sekund.

# 2) So'rovlar sonini taqqoslash (eng tez signal).
#    hibernate.generate_statistics=true bilan loglardan:
grep -c 'select ' app.log

# 3) Profil olish: CPU vaqti qayerga ketadi.
#    async-profiler (eng foydali vosita):
java -agentpath:/opt/async-profiler/libasyncProfiler.so=start,event=cpu,file=/tmp/cpu.html \
     -jar target/app.jar
# Yoki JFR:
java -XX:StartFlightRecording=duration=60s,filename=/tmp/rec.jfr -jar target/app.jar
jfr summary /tmp/rec.jfr
jfr print --events jdk.ExecutionSample /tmp/rec.jfr | head -50

# 4) Allokatsiya profili: GC bosimi manbasi.
java -agentpath:/opt/async-profiler/libasyncProfiler.so=start,event=alloc,file=/tmp/alloc.html \
     -jar target/app.jar
```

### 38.8 Performance byudjeti

Review ni did bahsidan chiqarish uchun endpointlar uchun byudjet belgilanadi va PR shu byudjetga nisbatan baholanadi.

```yaml
# performance-budget.yml - loyihada saqlanadi, review da havola qilinadi.
endpoints:
  - path: GET /api/orders
    p99_ms: 300
    max_db_queries: 3
    max_external_calls: 0
    max_response_kb: 50
  - path: POST /api/orders
    p99_ms: 500
    max_db_queries: 6
    max_external_calls: 1      # to'lov provayderi
    max_response_kb: 5
  - path: GET /api/reports/monthly
    p99_ms: 5000               # og'ir hisobot, ongli qabul qilingan
    max_db_queries: 2
    max_external_calls: 0
    async: true                # natija fayl sifatida beriladi
```

```java
// Byudjetni test bilan qulflash: so'rovlar soni (23.2) va javob hajmi.
@Test
void orderListStaysWithinBudget() {
    seedOrders(500);
    Statistics stats = statistics(); stats.clear();

    MvcTestResult result = mvc.get().uri("/api/orders?size=20").exchange();

    assertThat(stats.getPrepareStatementCount()).as("DB so'rovlari").isLessThanOrEqualTo(3);
    assertThat(result.getResponse().getContentAsByteArray().length / 1024)
        .as("javob hajmi (KB)").isLessThanOrEqualTo(50);
}
```

### 38.9 Review checklisti: performance

| Savol | Nega |
| --- | --- |
| Siklda DB yoki HTTP chaqiruvi bormi | N+1 |
| So'rovlar soni ma'lumot hajmiga bog'liqmi | Masshtablanmaydi |
| Chegarasiz yuklash bormi | Xotira va kechikish |
| Faqat kerakli ustunlar o'qiladimi | Ortiqcha tashish |
| Yangi `JOIN` natijani ko'paytirmaydimi | Qatorlar portlashi |
| Yangi `ORDER BY` indeksli ustundami | Sort |
| Kesh TTL, hajm va kalit to'g'rimi | Eskirgan yoki oqadigan ma'lumot |
| Cache stampede himoyasi bormi | Tashqi servisga to'lqin |
| Tranzaksiya ichida tashqi chaqiruv bormi | Ulanish ushlanishi |
| Optimallashtirish o'lchov bilan asoslanganmi | Ortiqcha murakkablik |
| Byudjetga sig'adimi | Regressiya |
| Og'ir operatsiyalar async mi | Timeout va thread |

### 38.10 Amalda qo'llash

- [ ] Eng muhim 5-10 endpoint uchun performance byudjetini (p99, so'rovlar soni, javob hajmi) yozib, repoda saqlang.
- [ ] Byudjetni test bilan qulflang: so'rovlar soni va javob hajmi tekshiruvi.
- [ ] Diffda siklda I/O ni qidiradigan skriptni review oqimiga qo'shing.
- [ ] `findAll()` va chegarasiz so'rovlarni toping va ularga `LIMIT` yoki bo'laklash qo'shing.
- [ ] Barcha keshlar uchun hit rate metrikasini yoqib, foyda bermayotganlarini aniqlang.
- [ ] Tashqi servisga bog'liq keshlarda `refreshAfterWrite` + `expireAfterWrite` kombinatsiyasini qo'ying.
- [ ] Yuqori xavfli PR lar uchun `hey` yoki `k6` bilan oldin/keyin o'lchov qilish amaliyotini joriy qiling.
- [ ] Prodda async-profiler yoki JFR bilan muntazam profil olishni sozlab, optimallashtirish qarorlarini dalilga asoslang.

## 39. Observability review (Observability)

Kod prodda ishlaganda uning holati faqat chiqargan signallar orqali ko'rinadi. Shu sababli har bir yangi kod yo'li uchun savol beriladi: bu yo'l xato ishlasa, qanday bilamiz. Agar javob "mijoz shikoyat qilganda" bo'lsa, kod to'liq emas. Observability review ning afzalligi shundaki, u incident paytida eng ko'p qaytim beradi va eng arzon qo'shiladi.

### 39.1 Uch signal va ularning vazifasi

| Signal | Savolga javob beradi | Qachon qo'shiladi |
| --- | --- | --- |
| Metrika | Nima sodir bo'layapti, qancha, qanchalik tez | Har bir muhim operatsiya |
| Log | Nega shunday bo'ldi (bitta holat uchun) | Xato va muhim qarorlar |
| Trace | Vaqt qayerga ketdi (bitta so'rov bo'ylab) | Ko'p komponentli oqim |

Review da eng ko'p uchraydigan xato - ikkisini aralashtirish: metrikada bo'lishi kerak narsa logga yoziladi (har so'rov uchun `log.info`), yoki logda bo'lishi kerak kontekst metrikaga tegga aylanadi (kardinallik portlashi, 16.7).

### 39.2 Yangi kod uchun minimal signal to'plami

```java
// Review talabi: har bir muhim operatsiya uchun uchlik.
@Service
public class PaymentService {

    private final Counter attempts;
    private final Counter failures;
    private final Timer duration;

    public PaymentService(MeterRegistry registry) {
        this.attempts = Counter.builder("payments.attempt")
            .description("to'lov urinishlari soni")
            .register(registry);
        this.failures = Counter.builder("payments.failed")
            .register(registry);
        this.duration = Timer.builder("payments.duration")
            .publishPercentiles(0.5, 0.95, 0.99)
            .register(registry);
    }

    public PaymentResult charge(ChargeCommand cmd) {
        attempts.increment();
        Timer.Sample sample = Timer.start();
        try {
            PaymentResult result = gateway.charge(cmd);
            // Natija turi teg sifatida: rad etishlar alohida ko'rinadi.
            registry.counter("payments.result", "outcome", result.kind().name()).increment();
            return result;
        } catch (Exception e) {
            failures.increment();
            // Log: bitta holat uchun kontekst. Korrelyatsiya ID bilan.
            log.error("to'lov yiqildi orderId={} idemKey={} provider={}",
                      cmd.orderId(), cmd.idempotencyKey(), cmd.provider(), e);
            throw e;
        } finally {
            sample.stop(duration);
        }
    }
}
```

Diqqat: `@Timed` annotatsiyasi va `@Observed` (Micrometer Observation) bu kodni qisqartiradi. Review da muhimi mexanizm emas, uchta savolga javob borligi: nechta urinish, nechtasi yiqildi, qancha vaqt oldi.

### 39.3 Nimani o'lchash kerak: RED va USE

| Model | Nimani o'lchaydi | Qachon |
| --- | --- | --- |
| RED (Rate, Errors, Duration) | So'rovlar oqimi | Endpoint, integratsiya, iste'molchi |
| USE (Utilization, Saturation, Errors) | Resurslar | Pool, navbat, thread, disk |
| Biznes metrikalari | Natija | Buyurtmalar, to'lovlar, konversiya |

```java
// Review da eng ko'p esdan chiqadigan: to'yinganlik (saturation).
// So'rovlar tez ishlayapti, lekin navbat o'syapti - bu yiqilishdan oldingi holat.
@Bean
MeterBinder queueMetrics(OutboxRepository outbox, ThreadPoolTaskExecutor executor) {
    return registry -> {
        // Outbox navbati: kutayotgan xabarlar va eng qadimgi yoshi (27.9).
        Gauge.builder("outbox.pending", outbox, OutboxRepository::countPending)
             .register(registry);
        Gauge.builder("outbox.oldest.seconds", outbox,
                      r -> r.oldestPendingAgeSeconds()).register(registry);
        // Thread pool to'yinganligi.
        Gauge.builder("executor.queue.size", executor,
                      e -> e.getThreadPoolExecutor().getQueue().size()).register(registry);
    };
}
// Biznes metrikasi: eng qimmatli signal.
// Agar to'lovlar soni oyning shu kunidagi o'rtachadan 40 foiz past bo'lsa,
// bu texnik metrikalar yashil bo'lsa ham incident.
```

### 39.4 Log sifati

```java
// Daraja 1: kontekstsiz log - incidentda foydasiz.
log.error("Xatolik yuz berdi");
log.error("Xato: " + e.getMessage());            // stack trace yo'q

// Daraja 2: istisno bor, kontekst yo'q.
log.error("To'lov yiqildi", e);                  // qaysi to'lov?

// Daraja 3: kontekst va istisno bor.
log.error("to'lov yiqildi orderId={} amount={} provider={}",
          orderId, amount, provider, e);

// Daraja 4: strukturali log - qidirish va agregatsiya mumkin.
// (logstash-logback-encoder bilan JSON)
log.atError()
   .setMessage("to'lov yiqildi")
   .addKeyValue("orderId", orderId)
   .addKeyValue("amount", amount.toPlainString())
   .addKeyValue("provider", provider)
   .setCause(e)
   .log();
// Natija: {"message":"to'lov yiqildi","orderId":"...","amount":"100000",
//          "provider":"payme","traceId":"...","stack_trace":"..."}
// Bu logda `orderId` bo'yicha qidirish va `provider` bo'yicha guruhlash mumkin.
```

| Log darajasi | Qachon | Review diqqati |
| --- | --- | --- |
| `ERROR` | Odam aralashuvi kerak | Alert ga ulanganmi; shovqin bo'lmasin |
| `WARN` | Kutilmagan, lekin tiklandi | Retry, fallback, degradatsiya |
| `INFO` | Muhim biznes hodisasi | Har so'rov uchun emas |
| `DEBUG` | Diagnostika | Prodda o'chirilgan |
| `TRACE` | Batafsil | Faqat lokalda |

```java
// Review izohi: xato darajasining noto'g'ri tanlanishi.
// Biznes rad etishi ERROR emas:
log.error("Karta rad etildi: {}", orderId);      // kuniga 5000 marta -> alert shovqini
log.info("karta rad etildi orderId={} reason={}", orderId, reason);   // to'g'ri
// Lekin: rad etishlar nisbati keskin oshsa - bu metrika va alert ishi,
// log emas.
```

### 39.5 Korrelyatsiya va trace

```java
// Review talabi: har log satrida so'rovni aniqlash imkoni bo'lishi kerak.
// Spring Boot 3 + Micrometer Tracing avtomatik traceId va spanId qo'shadi.
```

```yaml
management:
  tracing:
    sampling:
      probability: 0.1                 # 10% - prod uchun maqbul
  otlp:
    tracing:
      endpoint: http://collector:4318/v1/traces
logging:
  pattern:
    level: "%5p [${spring.application.name},%X{traceId:-},%X{spanId:-}]"
```

```java
// Asinxron chegaralarda kontekst ko'chishi - eng ko'p buziladigan joy.
// @Async, ExecutorService va Kafka listener larda traceId yo'qoladi.
@Bean
TaskDecorator contextPropagatingDecorator() {
    // Micrometer Context Propagation: MDC va trace kontekstini ko'chiradi.
    return new ContextPropagatingTaskDecorator();
}
@Bean
ThreadPoolTaskExecutor orderExecutor(TaskDecorator decorator) {
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setTaskDecorator(decorator);              // aks holda traceId yo'qoladi
    ...
}
// Review savoli: async ishda xato bo'lsa, uni asl so'rov bilan
// bog'lash mumkinmi? Javob "yo'q" bo'lsa, incident tahlili juda qiyin.

// Kafka da: traceId xabar header ida ko'chiriladi.
// Review savoli: produser va iste'molchi loglarini bir-biriga bog'lash
// mumkinmi?
```

### 39.6 Health check va probe lar

```java
// Naqsh: yuzaki health check - har doim "UP".
@GetMapping("/health")
public String health() { return "OK"; }
// Bu Kubernetes ga "ishlayapman" deydi, lekin DB yiqilgan bo'lsa ham.

// To'g'ri: bog'liqliklar holati bilan, lekin probe larni ajratib.
```

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true                  # /health/liveness va /health/readiness
      group:
        liveness:
          include: livenessState       # FAQAT "protsess tirikmi"
        readiness:
          include: readinessState,db   # "trafik qabul qila olamanmi"
      show-details: when-authorized
```

Review da asosiy farq: `liveness` ga tashqi bog'liqliklarni QO'SHMASLIK kerak. Agar DB vaqtincha yiqilsa va liveness unga bog'liq bo'lsa, Kubernetes barcha podlarni qayta ishga tushiradi va tiklanishni qiyinlashtiradi (kaskadli nosozlik). `readiness` esa bog'liqliklarni hisobga olishi mumkin - pod trafikdan chiqadi, lekin o'ldirilmaydi.

```java
// Maxsus health indicator: review da uning narxi tekshiriladi.
@Component
public class PaymentGatewayHealth implements HealthIndicator {
    @Override
    public Health health() {
        // DIQQAT: bu metod har health so'rovida chaqiriladi (Kubernetes
        // har 10 sekundda). Tashqi servisga so'rov yuborish - yuk.
        // To'g'ri: oxirgi muvaffaqiyatli chaqiruv vaqtiga qarash.
        Instant last = gateway.lastSuccessfulCall();
        if (last == null || last.isBefore(Instant.now().minusSeconds(120))) {
            return Health.down().withDetail("lastSuccess", last).build();
        }
        return Health.up().build();
    }
}
```

### 39.7 Alert sifati

Review da yangi alert ham ko'riladi, chunki yomon alert jamoani charchatadi va yaxshi alertlar ham e'tibordan qoladi.

| Alert mezoni | Yaxshi alert | Yomon alert |
| --- | --- | --- |
| Harakatga chaqiradi | "To'lov xatolari 5% dan oshdi" | "CPU 80%" |
| Foydalanuvchiga ta'siri bor | SLO buzilishi | Ichki texnik holat |
| Aniq egasi bor | Jamoa belgilangan | "Kimdir ko'rsin" |
| Runbook bor | Nima qilish yozilgan | Faqat ogohlantirish |
| Shovqin emas | Haftada 0-2 marta | Kuniga 20 marta |
| Oldini olish mumkin | Navbat o'syapti (saturation) | Tizim allaqachon yiqilgan |

```yaml
# Prometheus alert: review da shu shakl talab qilinadi.
groups:
  - name: payments
    rules:
      - alert: PaymentFailureRateHigh
        # Nisbat, absolyut son emas: yuk o'zgarishiga chidamli.
        expr: |
          sum(rate(payments_result_total{outcome="FAILED"}[5m]))
            / sum(rate(payments_result_total[5m])) > 0.05
        for: 10m                       # qisqa to'lqinlarda uyg'otmaydi
        labels:
          severity: critical
          team: payments               # egasi aniq
        annotations:
          summary: "To'lov xatolari 5% dan oshdi ({{ $value | humanizePercentage }})"
          runbook: "https://wiki/runbooks/payment-failures"
          dashboard: "https://grafana/d/payments"

      - alert: OutboxBacklogGrowing
        # Saturation alerti: yiqilishdan OLDIN ogohlantiradi.
        expr: outbox_oldest_seconds > 300
        for: 5m
        labels: { severity: warning, team: orders }
        annotations:
          summary: "Outbox da 5 daqiqadan ortiq kutayotgan xabar bor"
          runbook: "https://wiki/runbooks/outbox"
```

### 39.8 Review checklisti: observability

| Savol | Nega |
| --- | --- |
| Yangi operatsiya uchun urinish/xato/vaqt metrikasi bormi | Ko'r kod |
| Xato logida kontekst va istisno bormi | Diagnostika |
| Log darajasi to'g'ri tanlanganmi | Alert shovqini |
| Har so'rov uchun `INFO` log yozilmaydimi | Disk va narx |
| Metrika teglarida yuqori kardinallik yo'qmi | Xotira va narx |
| traceId async chegarasida ko'chadimi | Incident tahlili |
| Yangi tashqi integratsiya o'lchanadimi | Ko'r integratsiya |
| Navbat va pool to'yinganligi o'lchanadimi | Oldini olish |
| Biznes metrikasi bormi | Texnik yashil, biznes qizil |
| `liveness` tashqi bog'liqliklarga bog'lanmaganmi | Kaskadli qayta ishga tushish |
| Yangi alert harakatga chaqiradimi va runbook bormi | Shovqin |
| Maxfiy ma'lumot logga tushmaydimi | Oqish (32.1) |

### 39.9 Amalda qo'llash

- [ ] Har bir muhim operatsiya uchun urinish, natija (teg bilan) va davomiylik metrikalarini qo'shishni review talabiga aylantiring.
- [ ] Strukturali (JSON) logga o'tib, `traceId` va `spanId` ni log patterniga kiriting.
- [ ] `ContextPropagatingTaskDecorator` ni barcha executor larga qo'shib, async da traceId yo'qolmasligini tasdiqlang.
- [ ] Barcha navbatlar (outbox, thread pool, Kafka lag) uchun to'yinganlik metrikalarini qo'shing.
- [ ] `liveness` guruhidan tashqi bog'liqliklarni olib tashlang va `readiness` ga ko'chiring.
- [ ] Health indicator larning narxini tekshirib, tashqi so'rov yuboradiganlarini keshlangan holatga o'tkazing.
- [ ] Mavjud alertlarni ko'rib chiqib, harakatga chaqirmaydiganlarini o'chiring yoki `warning` ga tushiring.
- [ ] Har bir `critical` alert uchun egasi va runbook havolasi borligini tasdiqlang.
- [ ] Kamida uchta biznes metrikasi (buyurtmalar, to'lovlar, ro'yxatdan o'tish) va ularga anomaliya alertini qo'shing.

# IX. Jarayon, madaniyat va o'lchov

## 40. Review jarayonini qurish (Building the Process)

Yaxshi reviewer lar bo'lgan jamoada ham review yomon ishlashi mumkin, agar jarayon bo'lmasa: PR lar kutadi, kim ko'rishi noaniq, xavfli o'zgarishlar oddiy o'zgarishlar bilan bir xil yo'ldan o'tadi. Bu bob jarayonning mexanik qismini beradi - kim, qachon, qanday chuqurlikda.

### 40.1 Kim review qiladi: CODEOWNERS

```bash
# .github/CODEOWNERS - eng kam harakat bilan eng katta foyda beradigan fayl.
# Tartib muhim: oxirgi mos kelgan qoida ishlaydi.

# Standart: har qanday o'zgarish backend jamoasiga.
*                                       @acme/backend

# Domen bo'yicha egalik: kim bilsa, shu ko'radi.
/order-service/                         @acme/orders-team
/payment-service/                       @acme/payments-team

# Yuqori xavfli yo'llar: ikki reviewer va maxsus jamoa.
/**/db/migration/                       @acme/dba @acme/backend-leads
/**/SecurityConfig.java                 @acme/security
/**/security/                           @acme/security
/**/payment/                            @acme/payments-team @acme/security

# Infratuzilma va build.
/pom.xml                                @acme/backend-leads
/.github/workflows/                     @acme/platform
/Dockerfile                             @acme/platform
/k8s/                                   @acme/platform

# Review qoidalari o'zi: o'zgartirish uchun kelishuv kerak.
/REVIEW.md                              @acme/backend-leads
/.github/CODEOWNERS                     @acme/backend-leads
```

```yaml
# Branch protection: CODEOWNERS ni majburiy qilish (GitHub sozlamalari).
# - Require review from Code Owners: yoqilgan
# - Required approvals: 1 (yuqori xavfli yo'llar uchun CODEOWNERS 2 beradi)
# - Dismiss stale approvals on push: yoqilgan (yangi commit - yangi review)
# - Require status checks: build, test, sonar, dependency-check
# - Require conversation resolution: yoqilgan (javobsiz izoh qolmaydi)
```

### 40.2 Xavf bo'yicha tabaqalash

2.9 da tabaqalash jadvali berilgan; bu yerda uni jarayonga aylantirish.

```yaml
# .github/workflows/risk-label.yml
# PR tegilgan yo'llarga qarab avtomatik yorliq oladi: reviewer
# chuqurlik darajasini darhol ko'radi.
name: risk-label
on: pull_request
jobs:
  label:
    runs-on: ubuntu-latest
    permissions: { pull-requests: write, contents: read }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - id: risk
        run: |
          FILES=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          LEVEL=low
          echo "$FILES" | grep -qE '\.(java|kt)$' && LEVEL=medium
          echo "$FILES" | grep -qE 'db/(migration|changelog)|Security|payment|auth|crypto' && LEVEL=high
          echo "$FILES" | grep -qE 'db/migration/.*(DROP|ALTER COLUMN|TRUNCATE)' && LEVEL=critical
          echo "level=$LEVEL" >> "$GITHUB_OUTPUT"
      - uses: actions/github-script@v7
        with:
          script: |
            const level = '${{ steps.risk.outputs.level }}';
            await github.rest.issues.addLabels({
              owner: context.repo.owner, repo: context.repo.repo,
              issue_number: context.issue.number, labels: [`risk:${level}`]
            });
            if (level === 'high' || level === 'critical') {
              await github.rest.issues.createComment({
                owner: context.repo.owner, repo: context.repo.repo,
                issue_number: context.issue.number,
                body: `Bu PR \`risk:${level}\` deb belgilandi.\n\n`
                    + `Talablar (REVIEW.md):\n`
                    + `- ikki reviewer\n`
                    + `- migratsiya uchun: qulf turi, vaqti va qaytarish rejasi\n`
                    + `- lokalda yoki stagingda sinalgani haqida izoh`
              });
            }
```

### 40.3 SLA va navbat

| Mezon | Tavsiya |
| --- | --- |
| Birinchi javob | 4 ish soati ichida |
| Tuzatishdan keyingi javob | 2 ish soati (kontekst yangi) |
| Yuqori xavfli PR | O'sha kuni, lekin shoshilmasdan |
| Kutish vaqti 24 soatdan oshsa | Jamoa kanalida eslatma |
| Kutish vaqti 48 soatdan oshsa | Tech lead aralashadi |
| Review byudjeti | Kunning 10-15 foizi (2.5) |

```yaml
# Kutayotgan PR lar haqida eslatma: shovqin emas, yordam.
name: stale-pr-reminder
on:
  schedule: [ { cron: '0 9,14 * * 1-5' } ]       # kuniga ikki marta, ish kunlari
jobs:
  remind:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const prs = await github.paginate(github.rest.pulls.list, {
              owner: context.repo.owner, repo: context.repo.repo, state: 'open'
            });
            const now = Date.now();
            for (const pr of prs) {
              if (pr.draft) continue;
              const hours = (now - new Date(pr.created_at)) / 36e5;
              const reviews = await github.rest.pulls.listReviews({
                owner: context.repo.owner, repo: context.repo.repo, pull_number: pr.number
              });
              // Birinchi javob 24 soatdan ko'p kutilgan bo'lsa.
              if (reviews.data.length === 0 && hours > 24) {
                console.log(`kutayotgan: #${pr.number} (${Math.round(hours)} soat)`);
                // Slack yoki jamoa kanaliga xabar yuborish.
              }
            }
```

### 40.4 PR shabloni

```markdown
<!-- .github/pull_request_template.md -->
## Nima o'zgardi va nega

<!-- Bir-ikki jumla. Tiket havolasi. -->

## Qanday tekshirildi

<!-- Testlar, lokal sinov, staging. "Ishlayapti" yetarli emas. -->

## Reviewer uchun

<!-- Qaysi joyga alohida qarash kerak? Qaysi qaror muhokamaga arziydi? -->

---

### Tekshiruv ro'yxati

- [ ] Yangi kod uchun testlar bor: chegaraviy holatlar va xato yo'llari
- [ ] Yo'q kod ro'yxati o'tildi: validatsiya, avtorizatsiya, timeout, indeks, log
- [ ] Tranzaksiya chegarasi ichida tashqi chaqiruv yo'q
- [ ] Ikki marta kelgan so'rov xavfsiz (idempotentlik)
- [ ] Ikki parallel so'rov xavfsiz (unique constraint, versiya yoki qulf)
- [ ] Xato holatida nima bo'lishi aniq va o'lchanadi

### Agar tegishli bo'lsa

<!-- Tegishli bo'lmasa, qatorni o'chirib tashlang. -->

**Migratsiya:**
- [ ] Qulf turi va kutilgan davomiyligi:
- [ ] Rolling deploy da eski kod ishlaydi
- [ ] Qaytarish rejasi:
- [ ] Real hajmga yaqin nusxada sinalgan, vaqti:

**API o'zgarishi:**
- [ ] Breaking emas, yoki breaking va o'tish rejasi bor:
- [ ] OpenAPI va CHANGELOG yangilangan

**Xavfsizlik:**
- [ ] Yangi endpoint avtorizatsiya qoidasiga ega
- [ ] Foydalanuvchi faqat o'z ma'lumotini ko'radi
- [ ] Tashqi ma'lumot SQL, URL, fayl yo'liga tushmaydi
- [ ] Logda maxfiy ma'lumot yo'q

**Performance:**
- [ ] Siklda DB yoki HTTP chaqiruvi yo'q
- [ ] So'rovlar soni ma'lumot hajmiga bog'liq emas
- [ ] Byudjetga sig'adi (performance-budget.yml)
```

Shablonning asosiy qoidasi: uzun shablon o'qilmaydi. Majburiy qism 6 banddan oshmasligi kerak, qolgani shartli. "Agar tegishli bo'lmasa, o'chirib tashlang" ko'rsatmasi muhim - aks holda hamma band mexanik belgilanadi.

### 40.5 Draft va bosqichli review

```text
# Katta o'zgarish uchun uch bosqich: har bosqichda narx past.
1. Dizayn eskizi (kod yo'q)        -> 1 sahifa, 2 kun ichida javob
2. Draft PR (skelet, interfeyslar) -> yo'nalish tasdiqlanadi
3. To'liq PR                        -> satr-satr review

# Draft PR ning foydasi: muallif bir hafta noto'g'ri yo'nalishda
# ishlamaydi. Review izohi draft da "bu yondashuvni o'zgartiraylik"
# deyilsa, narxi bir kun; to'liq PR da - bir hafta.
```

### 40.6 Avtomatik tekshiruvlar tartibi

Review odam vaqtini faqat mashina tuta olmaydigan narsaga sarflashi kerak (5-bob). Buning uchun CI tartibi muhim: arzon va tez tekshiruvlar oldin.

```yaml
# .github/workflows/pr.yml - tez signal, keyin chuqur tekshiruv.
name: pr
on: pull_request
jobs:
  fast:                              # 1-2 daqiqa: darhol javob
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', cache: 'maven' }
      - run: ./mvnw -q -B spotless:check              # format
      - run: ./mvnw -q -B -T1C compile                # kompilyatsiya
      - run: ./mvnw -q -B checkstyle:check            # uslub
      - run: gitleaks protect --staged --redact       # secret

  unit:                              # 3-5 daqiqa
    needs: fast
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./mvnw -q -B -T1C test                   # unit testlar
      - run: ./mvnw -q -B test -Dtest='Arch*Test'     # arxitektura qoidalari

  integration:                       # 5-15 daqiqa
    needs: fast
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./mvnw -q -B verify -Pit                 # Testcontainers

  analysis:                          # parallel, bloklamaydi
    needs: fast
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }                      # Sonar uchun to'liq tarix
      - run: ./mvnw -q -B verify sonar:sonar -DskipTests
      - run: ./mvnw -q -B dependency-check:check
```

Review qoidasi: muallif CI yashil bo'lgandan keyin review so'raydi. Qizil CI bilan review so'rash reviewer vaqtini isrof qiladi.

### 40.7 Merge strategiyasi va review

| Strategiya | Review ga ta'siri |
| --- | --- |
| Squash merge | Commit tarixi yo'qoladi - review paytida o'qish kerak (4.5) |
| Merge commit | Tarix saqlanadi, lekin shovqinli |
| Rebase merge | Chiziqli tarix, lekin commitlar alohida yashil bo'lishi kerak |

```yaml
# Review natijasi commit xabarida saqlanishi uchun squash shablon:
# GitHub sozlamalarida "Default commit message: PR title and description"
# Shunda PR tavsifi (va undagi qarorlar) git tarixida qoladi.
```

### 40.8 Review ni o'tkazib yuborish mumkin bo'lgan holatlar

Har bir o'zgarish review dan o'tishi kerak degan qoida amalda buziladi, shuning uchun istisnolarni ochiq belgilash yaxshiroq.

| Holat | Yo'l |
| --- | --- |
| Prod incident, hotfix | Merge, keyin 24 soat ichida post-review |
| Faqat docs va CHANGELOG | Yengil yo'l (2.8) |
| Avtomatik bog'liqlik patch i | CI yashil bo'lsa avtomatik merge (33.4) |
| Reliz versiyasini ko'tarish | Avtomatlashtirilgan |
| Formatlash commiti | Alohida PR, diffsiz review |

```markdown
<!-- REVIEW.md ichida: hotfix siyosati -->
## Hotfix

Prod incident paytida review kutilmaydi. Shartlar:
1. Incident kanalida ikkinchi muhandis "ko'rdim" deb tasdiqlaydi (og'zaki review).
2. O'zgarish minimal bo'ladi: faqat to'xtatish, refactoring yo'q.
3. Merge dan keyin 24 soat ichida to'liq review PR ga izoh sifatida qo'shiladi.
4. Incident tahlilida shu o'zgarish ko'rib chiqiladi va kerak bo'lsa tuzatiladi.
```

### 40.9 Review checklisti: jarayon

| Savol | Nega |
| --- | --- |
| `CODEOWNERS` xavfli yo'llarni qamraydimi | Mas'uliyat |
| Branch protection sozlanganmi | Qoidalar majburiy |
| Xavf darajasi avtomatik belgilanadimi | Chuqurlik tanlovi |
| SLA kelishilgan va kuzatiladimi | Kutish vaqti |
| PR shabloni qisqa va shartlimi | O'qilishi |
| Arzon tekshiruvlar CI dami | Reviewer vaqti |
| Muallif CI yashil bo'lgach so'raydimi | Isrof |
| Draft bosqichi ishlatiladimi | Erta yo'nalish tuzatish |
| Hotfix siyosati yozilganmi | Incidentda chalkashlik |
| Javobsiz izohlar merge ni bloklaydimi | Yo'qolgan topilmalar |

### 40.10 Amalda qo'llash

- [ ] `.github/CODEOWNERS` yaratib, migratsiya, xavfsizlik va to'lov yo'llariga maxsus egalar belgilang.
- [ ] Branch protection da "Require conversation resolution" va "Dismiss stale approvals" ni yoqing.
- [ ] Xavf darajasini avtomatik belgilaydigan workflow ni qo'shing.
- [ ] PR shablonini yozib, majburiy qismni 6 banddan oshirmang.
- [ ] CI ni bosqichlarga bo'ling: format va kompilyatsiya 2 daqiqada javob bersin.
- [ ] Review SLA sini kelishib, kutayotgan PR lar haqida kunlik eslatmani sozlang.
- [ ] Katta o'zgarishlar uchun dizayn eskizi va draft PR bosqichlarini joriy qiling.
- [ ] Hotfix siyosatini `REVIEW.md` ga yozib, post-review majburiyatini belgilang.

## 41. Review madaniyati, til va kelishmovchilik (Culture, Language, Disagreement)

Texnik jihatdan to'g'ri review ham zarar keltirishi mumkin, agar u odamni himoyaga o'tishga majbur qilsa. Natija: muallif izohlarni rad etadi, keyingi PR ni kichikroq va kech yuboradi, va review dan qo'rqadi. Bu bob review ni muloqot sifatida ko'radi - lekin yumshoqlik haqida emas, aniqlik haqida.

### 41.1 Izoh tili: kodga qarash, odamga emas

| Yomon shakl | Yaxshi shakl |
| --- | --- |
| "Sen nega bunday qilding?" | "Bu yerda X bo'lsa nima bo'ladi?" |
| "Bu noto'g'ri" | "Bu holatda Y oqibat chiqadi" |
| "Hamma biladi ki..." | "Bizning konvensiyamiz..." (havola bilan) |
| "Yana shu xato" | "Shu naqsh takrorlanyapti - qoidaga aylantirsakmi?" |
| "Men shunday yozmagan bo'lardim" | (sabab bo'lmasa - izoh yozmaslik) |
| "Buni tushunmadim" | "Bu metod nima qilishini nom bilan ko'rsatsak bo'ladimi?" |
| "Bu juda sodda" | "Bu yerda Z holati hisobga olinmagan" |

Asosiy mexanik qoida: izoh kod haqida bo'lsin, muallif haqida emas. "Sen" so'zi izohda deyarli har doim ortiqcha.

### 41.2 Savol shaklida izoh

Savol ikki narsani beradi: muallifga tushuntirish imkonini beradi (balki reviewer kontekstni bilmaydi) va aniqlashtiradi.

```text
# Buyruq: muallif rozi bo'lmasa, bahs boshlanadi.
"Bu yerda cache qo'shish kerak."

# Savol: kontekstni ochadi.
"Bu so'rov qanchalik tez-tez chaqiriladi? Agar har sahifa yuklanishida
bo'lsa, kesh qo'shish arziydi - lekin ma'lumot qanchalik tez eskiradi
degan savol bor. Siz qanday o'ylaysiz?"
```

Lekin savol shakli bilan haddan oshmaslik kerak. Agar aniq xato bo'lsa, savol shakli chalkashtiradi:

```text
# Yomon: aniq blocker savol shaklida - muallif uni ixtiyoriy deb o'ylaydi.
"Bu yerda unique constraint bo'lishi kerak emasmi?"

# Yaxshi: aniq va sababi bilan.
blocker: idempotentlik kaliti bo'yicha unique indeks yo'q. Ikki parallel
so'rov ikki to'lov yaratadi (15.2 naqshi). Migratsiyaga qo'shish kerak.
```

### 41.3 Izoh darajasini ajratish

4.9 da prefikslar berilgan. Ularning asosiy foydasi psixologik: muallif qaysi izohga qancha vaqt sarflashini biladi va `nit` larni rad etishi normal bo'ladi.

```text
blocker:  tuzatilmasa merge bo'lmaydi (xato, xavfsizlik, ma'lumot)
suggest:  yaxshilanish, muallif qaroriga qoldiriladi
question: javob kerak, tuzatish shart emas
nit:      did, majburiy emas (10 foizdan ko'p bo'lmasin)
praise:   to'g'ri qilingan qiyin joy
```

Qo'shimcha qoida: `blocker` lar soni cheklangan bo'lishi kerak. Agar PR da 15 blocker bo'lsa, bu alohida muammo - PR dizayn darajasida noto'g'ri yoki muallif kontekstni bilmaydi. Shu holatda 15 izoh yozish o'rniga suhbatlashish kerak.

### 41.4 Junior va senior bilan review

| Muallif | Diqqat | Tuzoq |
| --- | --- | --- |
| Junior | Nega shunday - o'rganish imkoniyati | Haddan ortiq izoh, ruhiy bosim |
| O'rta daraja | Mustaqil qaror va chegaralar | Yetarli diqqat berilmasligi |
| Senior | Dizayn qarori va alternativalar | Yuzaki review (obro'ga ishonish) |
| Boshqa jamoa | Kontekst va konvensiyalar | Yashirin bilim talab qilish |
| Yangi kelgan | Konvensiyalarni ko'rsatish | "Bizda shunday" tushuntirishsiz |

```text
# Junior PR ida: 20 izoh yozish o'rniga eng muhim 5 tasini tanlash.
# Qolganlari keyingi PR larda ko'riladi yoki juftlikda ishlash orqali.

# Aniq va o'rgatuvchi izoh shakli:
blocker: bu yerda tranzaksiya ichida SMS yuborilyapti.

Nega muhim: DB ulanishi SMS provayderining javobini kutib turadi.
Bizda pool 20 ta ulanish - ya'ni 20 parallel buyurtma butun ilovani
to'xtatadi. Bundan tashqari SMS o'tib, keyin commit yiqilsa, mijoz
tasdiq oladi, lekin buyurtma yo'q bo'ladi.

Yechim: SMS ni outbox ga yozish (shunga o'xshash misol
OrderCancellationService da bor, 45-satr).

Bu naqsh haqida: REVIEW.md -> "tranzaksiya ichida tashqi chaqiruv".
```

### 41.5 Kelishmovchilikni hal qilish

Kelishmovchilik normal va foydali - muhimi uning oxiri bo'lishi. Jamoada tartib yozilmasa, bahs PR da uch kun davom etadi.

```markdown
<!-- REVIEW.md ichida: kelishmovchilik tartibi -->
## Kelishmovchilik

1. **Dalil almashish.** Ikki tomon o'z pozitsiyasini oqibat tilida yozadi
   (did emas, raqam yoki ssenariy).
2. **Ikki davra.** Izoh almashinuvi ikki davradan oshsa, PR da yozishni
   to'xtatib, 15 daqiqalik suhbat o'tkaziladi. Yozma bahs tezda qimmatlashadi.
3. **Qaytarilish narxi.** Qaror arzon qaytarilsa (ichki kod) - muallif
   qaroriga qoldiriladi. Qimmat qaytarilsa (API, sxema, ma'lumot) -
   uchinchi odam yoki tech lead qaror qiladi.
4. **Yozib qoldirish.** Qaror ADR yoki PR izohida qoladi, shunda keyin
   bahs takrorlanmaydi.
5. **"Rozi emasman, lekin bajaraman".** Qaror qabul qilingach, ikki tomon
   uni qo'llab-quvvatlaydi. Pozitsiya ADR da qayd qilinadi.
```

Alohida holat: reviewer va muallif tajriba darajasi juda farq qilsa, kelishmovchilik teng bo'lmaydi. Bunday holatda qoida foydali: "junior reviewer senior muallifga blocker qo'yishi normal, va senior javob yozishi majburiy".

### 41.6 Review izohining narxi

Har bir izoh muallif vaqtini oladi: o'qish, tushunish, tuzatish yoki javob yozish. Shu sababli izoh yozishdan oldin savol: bu izoh o'z narxini qoplaydimi.

| Izoh | Muallif vaqti | Foyda |
| --- | --- | --- |
| Aniq xato | 10-30 daqiqa | Prodda 10 barobar ko'p |
| Xavfsizlik | 30-60 daqiqa | Juda yuqori |
| Dizayn | Soatlar | Uzoq muddatli |
| Nomlash (noto'g'ri nom) | 2 daqiqa | Har o'qishda |
| Nomlash (did) | 2 daqiqa + bahs | Deyarli nol |
| Formatlash | 5 daqiqa | Nol (instrument ishi) |
| Shaxsiy uslub | Bahs | Manfiy |

Oxirgi uch qator review ning eng ko'p isrof qiladigan qismi. Ularni yo'q qilish uchun instrument va yozilgan konvensiya kerak, bahs emas.

### 41.7 Masofaviy va asinxron review

| Muammo | Yechim |
| --- | --- |
| Vaqt zonalari farqi | Yozma izoh to'liq va mustaqil bo'lsin |
| Ohangni noto'g'ri tushunish | Sabab va kontekstni yozish, emoji ortiqcha emas |
| Uzoq davralar | Blocker larni bir martada to'liq berish |
| Kontekst yo'qolishi | PR tavsifi va izohda havolalar |
| "Kim javob beradi" noaniqligi | CODEOWNERS va aniq murojaat |
| Tezkor savollar | 15 daqiqalik qo'ng'iroq, uch kunlik yozishma emas |

Asinxron review ning asosiy qoidasi: izoh o'zini tushuntirsin. Muallif boshqa vaqt zonasida uyg'onib, izohni o'qiganda qo'shimcha savol bermasdan ishlay olishi kerak. Bu "oqibat + alternativa + havola" shaklini majburiy qiladi.

### 41.8 Review ni o'rgatish

```markdown
<!-- Yangi jamoa a'zosi uchun review ga kirish rejasi -->
## Review ga qanday kirishamiz

### 1-hafta: kuzatish
Ikki PR ni tajribali reviewer bilan birga ko'rib chiqing (ekran ulashib).
Maqsad: nimaga qaraladi va qanday tartibda.

### 2-3-hafta: ikkinchi reviewer
PR larga ikkinchi reviewer sifatida qo'shiling. Izohlaringiz birinchi
reviewer bilan solishtiriladi - nima topildi, nima o'tkazib yuborildi.

### 4-hafta: mustaqil, past xavfli PR lar
`risk:low` va `risk:medium` PR larni mustaqil review qilasiz.

### Keyin: xavf darajasini oshirish
`risk:high` PR larda ikkinchi reviewer, keyin birinchi.

### Doimiy
- Har incidentdan keyin: "review nega ko'rmadi" savoliga javob.
- Har oyda bitta review ni birga tahlil qilish (nima yaxshi, nima yo'q).
```

### 41.9 Review madaniyatining buzilish belgilari

| Belgi | Nimani bildiradi |
| --- | --- |
| "LGTM" izohsiz, 2 daqiqada | Review marosimga aylangan |
| Bir xil odam hamma PR ni ko'radi | Bilim tarqalmaydi, nuqta bo'g'in |
| PR lar 3 kundan ko'p kutadi | Review byudjeti yo'q |
| Izohlarning yarmi `nit` | Instrument yo'q |
| Muallif izohlarga javob bermaydi | Jarayon majburiy emas |
| Bahslar PR dan tashqariga chiqadi | Kelishmovchilik tartibi yo'q |
| Katta PR lar normal holat | Bo'lish madaniyati yo'q |
| Junior lar PR yuborishdan qo'rqadi | Izoh tili bilan muammo |
| Review dan keyin ham prodda ko'p xato | Checklist incidentlardan o'smaydi |
| Reviewer "men faqat ko'rib qo'ydim" deydi | Mas'uliyat tarqamagan |

### 41.10 Amalda qo'llash

- [ ] Izoh prefikslari va ularning ma'nosini `REVIEW.md` ga yozib, jamoada kelishib oling.
- [ ] Kelishmovchilik tartibini (ikki davra, keyin suhbat) yozib, uni amalda qo'llashni boshlang.
- [ ] Oxirgi 50 izohni sanab, `nit` ulushini aniqlang; 20 foizdan ko'p bo'lsa, instrumentlarga ko'chiring.
- [ ] Izoh shabloniga "oqibat + alternativa + havola" talabini kiriting.
- [ ] Yangi a'zolar uchun review ga kirish rejasini yozib, uni onboarding ga qo'shing.
- [ ] Har oyda bitta review ni jamoada birga tahlil qilishni odat qiling.
- [ ] Madaniyat buzilish belgilarini chorakda bir marta tekshirib, topilganlarini muhokama qiling.
- [ ] `praise` izohini ongli ishlatishni boshlang: to'g'ri qilingan qiyin joyni ko'rsatish.

## 42. Review metrikalari (Measuring Review)

Review ni o'lchash ikki xil xavf tug'diradi: o'lchamaslik (hech narsa yaxshilanmaydi) va noto'g'ri o'lchash (odamlar raqamni yaxshilaydi, review ni emas). Bu bob qaysi raqam foydali, qaysi biri zararli va ularni qanday o'qish kerakligini beradi.

### 42.1 Foydali metrikalar

| Metrika | Nimani ko'rsatadi | Maqsad |
| --- | --- | --- |
| Birinchi javobni kutish vaqti (median, p90) | Jarayon tezligi | Median < 4 soat, p90 < 1 kun |
| PR ning umumiy o'tish vaqti | Oqim | Median < 1 kun |
| PR hajmi (mantiq satrlari) | Review sifati imkoniyati | Median < 200 |
| Tuzatish davralari soni | Talab aniqligi | Median 1, p90 <= 2 |
| Review da topilgan xatolar / prodda topilganlar | Filtr samaradorligi | Tendentsiya o'sishi |
| Izohlarning sinflar bo'yicha taqsimoti | Reviewer vaqti qayerga ketyapti | `nit` < 20% |
| Reviewer larning taqsimoti | Bilim tarqalishi | Bitta odam < 40% |
| Incidentlarda "review ko'rmadi" soni | Checklist bo'shliqlari | Har biri checklistga band qo'shadi |
| Qayta ochilgan PR / revert soni | Sifat | Kamayish |

### 42.2 Zararli metrikalar

| Metrika | Nega zararli |
| --- | --- |
| Izohlar soni (reviewer bo'yicha) | Ko'p `nit` yozishga undaydi |
| Approve lar soni | Yuzaki review ga undaydi |
| Review tezligi (daqiqada) | Shoshilishga undaydi |
| Topilgan xatolar soni (reyting sifatida) | Raqobat va bahs keltiradi |
| Coverage foizi (yagona mezon) | Assertion siz testlar yozishga undaydi (5.9) |
| Muallif bo'yicha "xatolar soni" | Qo'rquv madaniyati, kichik PR lar yashiriladi |

Umumiy qoida: metrika odamni emas, jarayonni o'lchashi kerak. Odam bo'yicha o'lchangan har qanday review metrikasi ertami-kechmi o'yinga aylanadi.

### 42.3 Metrikalarni yig'ish

```bash
#!/usr/bin/env bash
# scripts/review-metrics.sh - oyda bir marta ishga tushiriladi.
set -euo pipefail
REPO="${1:?repo kerak: owner/name}"
LIMIT=200

echo "=== Birinchi javobni kutish vaqti (soat) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" \
  --json number,createdAt,reviews \
  --jq '[.[] | select((.reviews|length) > 0)
        | ((.reviews[0].submittedAt|fromdate) - (.createdAt|fromdate)) / 3600]
        | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor], max: .[-1]}'

echo "=== PR o'tish vaqti (soat) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" \
  --json createdAt,mergedAt \
  --jq '[.[] | ((.mergedAt|fromdate) - (.createdAt|fromdate)) / 3600] | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor]}'

echo "=== PR hajmi (o'zgargan satrlar) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" \
  --json additions,deletions \
  --jq '[.[] | .additions + .deletions] | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor], max: .[-1]}'

echo "=== Reviewer taqsimoti (bilim tarqalishi) ==="
gh pr list --repo "$REPO" --state merged --limit "$LIMIT" --json reviews \
  --jq '[.[].reviews[]?.author.login] | group_by(.)
        | map({reviewer: .[0], count: length}) | sort_by(-.count)'

echo "=== Tuzatish davralari (review dan keyingi commitlar) ==="
gh pr list --repo "$REPO" --state merged --limit 50 --json number,reviews,commits \
  --jq '[.[] | select((.reviews|length) > 0) | (.reviews|length)] | sort
        | {median: .[(length/2)|floor], p90: .[(length*0.9)|floor]}'
```

### 42.4 Izohlarni sinflash

Eng foydali va eng kam qilinadigan o'lchov: reviewer vaqti qayerga ketyapti. Buni qo'lda, bir oyda bir marta 50 izohni ko'rib bajarish mumkin.

```bash
# Izohlarni yig'ish va prefiks bo'yicha sanash (prefikslar ishlatilsa).
gh pr list --repo "$REPO" --state merged --limit 50 --json number \
  --jq '.[].number' \
  | while read -r pr; do
      gh api "repos/$REPO/pulls/$pr/comments" --jq '.[].body'
    done > /tmp/comments.txt

for p in blocker suggest question nit praise; do
  printf '%-10s %s\n' "$p" "$(grep -ci "^$p:" /tmp/comments.txt || echo 0)"
done
echo "prefikssiz: $(grep -cvE '^(blocker|suggest|question|nit|praise):' /tmp/comments.txt)"

# Mavzu bo'yicha: eng ko'p takrorlanadigan izohlar - avtomatlashtirish nomzodlari.
grep -oiE '(format|import|naming|nom|test|transaction|tranzaksiya|index|indeks|null|timeout|log)' \
  /tmp/comments.txt | sort | uniq -c | sort -rn | head -10
```

Natijadan amaliy xulosa: eng ko'p takrorlanadigan uchta mavzu avtomatlashtirish yoki konvensiya yozish uchun nomzod (5.10).

### 42.5 Review samaradorligini o'lchash

Eng muhim savol - review haqiqatan xato tutyaptimi. Buni o'lchash uchun ikki raqam kerak: review da topilgan va prodda topilgan xatolar.

```markdown
<!-- Har incident tahlilida to'ldiriladigan jadval. -->
| Incident | Sabab (kod o'zgarishi) | Review dan o'tganmi | Nega ko'rinmadi | Checklist bandi |
|---|---|---|---|---|
| INC-102 | PR #1203, idempotentlik yo'q | Ha, 1 reviewer | Poyga holati tekshirilmagan | "ikki parallel so'rov" |
| INC-108 | PR #1241, migratsiya qulfi | Ha, 2 reviewer | Jadval hajmi bilinmagan | "jadval hajmi va qulf vaqti" |
| INC-115 | Konfiguratsiya o'zgarishi | Yo'q (yengil yo'l) | Review qilinmagan | Konfiguratsiya yengil yo'ldan olib tashlandi |
```

Bu jadval review ning eng qimmatli artefakti: u checklistni taxmin bilan emas, haqiqiy nosozliklar bilan to'ldiradi (12.10).

### 42.6 DORA metrikalari bilan bog'liqlik

Review jarayoni to'rtta DORA ko'rsatkichidan ikkitasiga bevosita ta'sir qiladi.

| DORA metrikasi | Review ning ta'siri |
| --- | --- |
| Deploy chastotasi | Sekin review - kamroq deploy |
| O'zgarishning yetib borish vaqti (lead time) | Kutish vaqti to'g'ridan-to'g'ri qo'shiladi |
| O'zgarish nosozlik darajasi | Review sifati bevosita ta'sir qiladi |
| Tiklanish vaqti | Kichik PR lar tezroq qaytariladi |

Shu sababli review ni tezlashtirish deploy chastotasini oshiradi, lekin review ni yuzaki qilish nosozlik darajasini oshiradi. Muvozanat nuqtasi: tez javob, lekin xavf bo'yicha tabaqalangan chuqurlik (2.9).

### 42.7 Metrikalarni o'qish: tuzoqlar

```text
# Tuzoq 1: median yaxshi, p90 yomon.
Median kutish 2 soat, p90 - 3 kun. Bu o'rtacha holat yaxshi, lekin
PR larning 10 foizi butunlay to'xtab qolganini bildiradi. Aynan shu
10 foiz eng katta PR lar va eng xavfli o'zgarishlar bo'lishi mumkin.

# Tuzoq 2: PR hajmi kichraydi, lekin soni oshdi.
Bu yaxshi (bo'lish ishlayapti) yoki yomon (bir o'zgarish sun'iy
bo'laklangan, har biri alohida ma'nosiz) bo'lishi mumkin. Tekshirish:
stacked PR lar bir-biriga bog'liqmi.

# Tuzoq 3: izohlar soni kamaydi.
Review yaxshilandi (kod sifati o'sdi) yoki yomonlashdi (reviewer lar
charchagan). Farqni ajratish: prodda topilgan xatolar tendentsiyasi.

# Tuzoq 4: coverage o'sdi, mutatsiya balli o'smadi.
Testlar qo'shildi, lekin ular hech narsa tekshirmaydi (5.9, 34.7).
```

### 42.8 Amalda qo'llash

- [ ] `scripts/review-metrics.sh` ni qo'shib, oyda bir marta ishga tushirishni rejalashtiring.
- [ ] Kutish vaqtining median va p90 ini o'lchab, p90 ni alohida kuzatib boring.
- [ ] Reviewer taqsimotini chiqarib, bitta odamga 40 foizdan ko'p yuk tushmasligini ta'minlang.
- [ ] Izohlarni prefiks va mavzu bo'yicha sanab, eng ko'p takrorlanadigan uchtasini avtomatlashtiring.
- [ ] Incident tahlili shabloniga "review dan o'tganmi / nega ko'rinmadi / checklist bandi" ustunlarini kiriting.
- [ ] Odam bo'yicha o'lchanadigan review metrikalarini (izohlar soni, tezlik) ishlatmaslikni kelishib oling.
- [ ] Mutatsiya ballini coverage bilan birga kuzatib, ikkisining farqini tahlil qiling.

## 43. AI yozgan kodni review qilish va AI bilan review qilish (Reviewing AI-Generated Code)

AI yordamida yozilgan kod review ga yangi sinf muammolar olib keladi. Kod sintaktik to'g'ri, uslubi toza, nomlari yaxshi va testlari bor - ya'ni yuzaki review dan osongina o'tadi. Lekin uning xatolari odam xatolaridan boshqacha taqsimlangan: kontekstni bilmaslik, ishonchli ko'rinadigan noto'g'ri taxminlar va mavjud kod bilan nomuvofiqlik. Bu bob shu farqlarni va AI ni review da ishlatishni oladi.

### 43.1 AI yozgan kodning xato profili

| Xato turi | Nega yuzaga keladi | Review da qanday topiladi |
| --- | --- | --- |
| Loyiha konvensiyasini buzish | Umumiy naqshlardan yozilgan | Mavjud kod bilan taqqoslash |
| Mavjud yordamchi kodni takrorlash | Repoda nima borligini to'liq bilmaydi | "Bu allaqachon bormi" savoli |
| Ishonchli ko'rinadigan noto'g'ri API | Mavjud bo'lmagan metod yoki parametr | Kompilyatsiya va hujjat |
| Eskirgan yondashuv | O'rganish ma'lumotlaridagi eski naqshlar | Versiya va deprecation tekshiruvi |
| Yuzaki test | Kod bilan bir xil taxminlardan | Assertion sifati (35.1) |
| Chegaraviy holatlarning yo'qligi | Talab to'liq berilmagan | Holatlar jadvali (34.1) |
| Xavfsizlik kontekstini bilmaslik | Qaysi ma'lumot ishonchli - bilmaydi | Trust boundary (28.2) |
| Ortiqcha umumiylashtirish | "To'g'ri" naqshlarga moyillik | YAGNI savoli |
| Jim o'zgargan xulq | Refactoring paytida mantiq o'zgaradi | Diffni satr-satr o'qish |
| Noto'g'ri konfiguratsiya qiymatlari | Loyiha hajmini bilmaydi | Raqamlarni tekshirish (21.1) |

### 43.2 Eng xavfli naqsh: ishonchli ko'rinadigan noto'g'ri kod

Odam yozgan noto'g'ri kod ko'pincha noto'g'ri ko'rinadi: nomlari chalkash, tuzilishi g'alati, izohlari yo'q. AI yozgan noto'g'ri kod to'g'ri ko'rinadi. Shu sababli review usuli o'zgaradi - tashqi ko'rinishga ishonch kamayadi va har bir taxmin tekshiriladi.

```java
// AI yozgan kod: toza, o'qiladigan, izohli - va noto'g'ri.
/**
 * Buyurtma summasini valyuta kursiga ko'ra hisoblaydi.
 */
public Money convertTotal(Order order, Currency target) {
    BigDecimal rate = rateService.getRate(order.currency(), target);
    return new Money(
        order.total().amount().multiply(rate).setScale(2, RoundingMode.HALF_UP),
        target);
}
// Review topilmalari (hech biri ko'rinishdan bilinmaydi):
// 1) `setScale(2)` - lekin ba'zi valyutalarda 0 yoki 3 kasr (JPY, KWD).
//    Loyihada `Money` ning o'zi `currency.getDefaultFractionDigits()`
//    ishlatadi - bu kod shu konvensiyani buzadi.
// 2) `getRate` null qaytarishi mumkin (mavjud kodda shunday) - NPE.
// 3) Yakkalash qoidasi HALF_UP, lekin loyihada moliyaviy hisob uchun
//    HALF_EVEN kelishilgan (ADR-14).
// 4) Teskari yo'nalishda konvertatsiya aniqlikni yo'qotadi -
//    mavjud `CurrencyConverter` bu holatni hisobga oladi, bu kod yo'q.
```

### 43.3 AI yozgan kod uchun qo'shimcha review savollari

1. Bu funksiya loyihada allaqachon bormi. AI mavjud yordamchi klassni ko'rmasligi mumkin, natijada uchinchi `DateUtils` paydo bo'ladi.
2. Ishlatilgan API haqiqatan shunday ishlaydimi. Parametr tartibi, qaytish turi, istisno xulqi tekshiriladi.
3. Loyiha konvensiyasiga mosmi. `Money`, `Clock`, xato ishlash, log formati - hammasi loyihada o'z shakliga ega.
4. Testlar kod bilan bir xil taxminga asoslanganmi. Agar kod `HALF_UP` ishlatsa va test ham `HALF_UP` bilan hisoblangan kutilgan qiymat ishlatsa, test xatoni tutmaydi (35.7).
5. Chegaraviy holatlar qamralganmi. AI odatda happy path uchun test yozadi.
6. Muallif bu kodni tushunadimi. Eng muhim savol: PR muallifi har bir qatorni tushuntirib bera oladimi.

```text
# Review izohi: muallifning tushunishini tekshirish (ayblash emas).
question: Bu yerda `setScale(2, HALF_UP)` ishlatilgan, lekin loyihada
`Money` konstruktori valyutaning kasr xonalarini o'zi qo'llaydi
(Money.java:14) va ADR-14 da moliyaviy yakkalash uchun HALF_EVEN
kelishilgan.

Ikki variant: (a) `Money` ning o'z mexanizmidan foydalanish, (b) bu
joyda boshqa qoida kerak bo'lsa, sababini izohda yozish.

Qaysi biri to'g'ri - konvertatsiya mantiqi haqida qanday kelishuv bor?
```

### 43.4 Kontekst bermaslikning oqibati

AI yozgan kodning sifati unga berilgan kontekstga bog'liq. Shu sababli jamoada kontekstni kodga yaqin saqlash review yukini kamaytiradi.

| Mexanizm | Nima qiladi |
| --- | --- |
| `CLAUDE.md` yoki shunga o'xshash fayl | Loyiha konvensiyalari, stek, qoidalar |
| `REVIEW.md` | Review talablari - AI ham, odam ham o'qiydi |
| `GLOSSARY.md` | Domen tili (13.7) |
| ADR lar | Nega shunday qilingan |
| ArchUnit testlari | Qoidalar bajarilishini majburlaydi (5.10) |
| ErrorProne va Semgrep qoidalari | Naqshlarni kompilyatsiyada tutadi |
| Boy domen turlari | `Money`, `OrderId` - noto'g'ri ishlatish qiyinlashadi |

Oxirgi ikki qator eng samarali: konvensiyani hujjatda yozish uni tavsiya qiladi, kod va test bilan majburlash esa buzilishni imkonsiz qiladi. Bu AI yozgan kod uchun ham, yangi jamoa a'zosi uchun ham bir xil ishlaydi.

```markdown
<!-- CLAUDE.md namunasi: AI uchun ham, odam uchun ham kontekst. -->
# Loyiha konvensiyalari

## Stek
Java 21, Spring Boot 3.4, PostgreSQL 16, Flyway, Testcontainers.

## Majburiy qoidalar
- Pul: `Money` turi (BigDecimal + Currency). `double` taqiqlanadi.
- Vaqt: `Instant` saqlashda, `Clock` inyeksiya qilinadi. `LocalDateTime.now()` yo'q.
- ID: tipli (`OrderId`, `CustomerId`), UUID v7.
- Inyeksiya: faqat konstruktor orqali. `@Autowired` maydon taqiqlanadi.
- Tranzaksiya: faqat `application` qatlamida. Ichida tashqi chaqiruv yo'q.
- Domen: `org.springframework` va `jakarta.persistence` importlari yo'q.
- Yozuv endpointlari: idempotentlik kaliti + DB unique constraint.
- Testlar: PostgreSQL (Testcontainers), H2 ishlatilmaydi.
- Xato javoblari: `ProblemDetail`, ichki detallarsiz.

## Qoidalarni majburlash
`ArchitectureRulesTest` va `.semgrep/` da. Yangi qoida qo'shilsa,
avval test, keyin hujjat.

## Nimani qayerdan izlash
- Pul va valyuta: `shared/money/`
- Tashqi integratsiyalar: `infra/adapter/` (portlar `domain/port/`)
- Migratsiyalar: `src/main/resources/db/migration/`
```

### 43.5 AI ni review da ishlatish

AI review ni almashtirmaydi, lekin uning ba'zi qismlarini arzonlashtiradi. Mehnat taqsimoti 5-bobdagi mantiqqa amal qiladi.

| AI yaxshi bajaradigan | AI bajarmaydigan |
| --- | --- |
| Diffni qisqacha tushuntirish | Niyat to'g'riligini baholash |
| Tanish xato naqshlarini topish | Loyiha konteksti va tarixi |
| Yo'q test holatlarini taklif qilish | Qaysi holat biznes uchun muhim |
| Nomlash va o'qiluvchanlik takliflari | Domen tili to'g'riligi |
| Hujjat va izoh yozish | Qaror sabablarini bilish |
| Takrorlangan kodni topish | Takrorlanish ongli yoki yo'qligini bilish |
| Checklist bo'yicha mexanik o'tish | Checklistda yo'q narsani sezish |
| SQL rejasini tushuntirish | Prod hajmi va yuk haqida bilim |

Amaliy yondashuv: AI birinchi o'tishni bajaradi (mexanik tekshiruvlar, yo'q testlar, tanish naqshlar), odam ikkinchi o'tishni bajaradi (niyat, dizayn, xavf, kontekst). AI topilmalari esa boshqa avtomatik instrument topilmalari kabi ko'riladi - tekshirilishi kerak bo'lgan taklif sifatida, hukm sifatida emas.

```text
# AI review topilmasini qanday ko'rish kerak.
AI aytdi: "Bu metodda null tekshiruvi yo'q."

Reviewer tekshiradi:
1) Bu parametr haqiqatan null bo'lishi mumkinmi? (chegarada @Valid bormi)
2) Loyihada null siyosati qanday? (@NullMarked, 5.6)
3) Agar chegarada tekshirilgan bo'lsa - bu topilma noto'g'ri (false positive).

AI topilmalarining katta qismi shunday: texnik jihatdan to'g'ri,
kontekstda ahamiyatsiz. Ularni filtrsiz PR ga yuborish review ni
shovqinga ko'madi va jamoa AI izohlarini e'tiborsiz qoldiradi.
```

### 43.6 AI review ni sozlash

```yaml
# AI review bot i uchun qoidalar: shovqinni kamaytirish.
# Umumiy tamoyillar (aniq vosita nomidan qat'i nazar):
#
# 1) Faqat yuqori ishonchli topilmalarni post qilish.
#    Past ishonchli topilmalar - shovqin, jamoa botni o'chiradi.
#
# 2) Loyiha kontekstini berish: CLAUDE.md, REVIEW.md, GLOSSARY.md.
#
# 3) Mexanik tekshiruvlarni takrorlamaslik: format, import, uslub
#    allaqachon CI da (5.2).
#
# 4) Diqqatni aniq sinflarga qaratish: xavfsizlik, poyga holatlari,
#    yo'q test holatlari, tranzaksiya chegarasi.
#
# 5) Topilma shakli: oqibat + joy + taklif (28.5).
#
# 6) Bot izohi `suggest` darajasida bo'ladi, `blocker` emas - blocker
#    qarorini odam qabul qiladi.
#
# 7) Bot topilmalarining qabul qilinish nisbatini o'lchash: 30 foizdan
#    past bo'lsa, sozlamani o'zgartirish yoki o'chirish kerak.
```

### 43.7 Muallif mas'uliyati o'zgarmaydi

Eng muhim qoida: kodni kim yozgani - odam, AI yoki ikkisi birga - mas'uliyatni o'zgartirmaydi. PR muallifi kodning har bir qatori uchun javob beradi: uni tushunishi, tushuntirib berishi va prodda ishlamay qolsa tuzatishi kerak.

Shu sababli review da qoida oddiy: muallif tushuntirib bera olmaydigan kod merge qilinmaydi. Bu qoida AI dan oldin ham amal qilgan (copy-paste qilingan kod uchun) va u o'zgarmaydi.

```text
# Review izohi: tushunmasdan qo'shilgan kod belgisi.
question: Bu yerda `@Transactional(isolation = SERIALIZABLE)` qo'yilgan.
Bizning boshqa kodda bu daraja faqat ikki joyda ishlatiladi va ikkisida
ham retry mexanizmi bor (27.6), chunki PostgreSQL 40001 xatosini beradi.

Bu yerda retry yo'q. Ikki savol:
1) SERIALIZABLE nega kerak bo'ldi - qaysi poyga holatidan himoya?
2) 40001 xatosi qanday ishlanadi?

Agar SERIALIZABLE kerak bo'lmasa, uni olib tashlash osonroq.
```

### 43.8 Review checklisti: AI yozgan kod

| Savol | Nega |
| --- | --- |
| Muallif har qatorni tushuntirib bera oladimi | Mas'uliyat |
| Bu funksiya loyihada allaqachon bormi | Takrorlanish |
| Loyiha konvensiyalariga mosmi | Nomuvofiqlik |
| Ishlatilgan API haqiqatan shunday ishlaydimi | Noto'g'ri taxmin |
| Testlar kod bilan bir xil taxmindan kelib chiqmaganmi | Yolg'on ishonch |
| Chegaraviy holatlar qamralganmi | Happy path |
| Xavfsizlik konteksti to'g'ri tushunilganmi | Trust boundary |
| Konfiguratsiya raqamlari loyiha hajmiga mosmi | Taxminiy qiymatlar |
| Ortiqcha umumiylashtirish yo'qmi | YAGNI |
| Refactoring paytida xulq jim o'zgarmaganmi | Regressiya |

### 43.9 Amalda qo'llash

- [ ] `CLAUDE.md` (yoki shunga o'xshash kontekst fayli) yozib, loyihaning majburiy konvensiyalarini sanab chiqing.
- [ ] Har bir yozilgan konvensiya uchun uni majburlaydigan mexanizm qo'shing: ArchUnit, ErrorProne, Semgrep yoki tipli domen turi.
- [ ] `GLOSSARY.md` va ADR larni kod bazasida saqlab, kontekstni kodga yaqin tuting.
- [ ] AI yozgan kod uchun qo'shimcha review savollarini checklistga qo'shing.
- [ ] AI review bot i ishlatilsa, uning topilmalari qabul qilinish nisbatini o'lchang va 30 foizdan past bo'lsa sozlang.
- [ ] Bot izohlarini `suggest` darajasida cheklab, `blocker` qarorini odamga qoldiring.
- [ ] "Muallif tushuntirib bera olmaydigan kod merge qilinmaydi" qoidasini `REVIEW.md` ga yozing.
- [ ] Yangi testlarda kutilgan qiymatlar qo'lda yozilganini (kod bilan hisoblanmaganini) tekshirishni review bandiga aylantiring.

## 44. Shablonlar, checklistlar va reviewer yetukligi (Templates and Maturity)

Bu bob hujjatning ma'lumotnoma qismi: tayyor checklistlar, izoh iboralari va o'zini baholash mezonlari. U boshidan oxirigacha o'qilishi uchun emas, review paytida ochib ishlatish uchun yozilgan.

### 44.1 Universal review o'tishi: 15 daqiqalik ro'yxat

Har qanday PR uchun, xavf darajasidan qat'i nazar:

```text
1.  PR tavsifi va tiket: niyat aniqmi?
2.  Fayllar ro'yxati: kutilmagan fayl bormi? Migratsiya, konfiguratsiya,
    xavfsizlik, bog'liqlik o'zgardimi?
3.  Hajm: mantiq satrlari 400 dan oshdimi? (oshsa - bo'lish taklifi)
4.  Migratsiya va sxema (agar bor): qulf, orqaga moslik, qaytarish.
5.  Public API (agar o'zgargan): breaking change katalogi (37.1).
6.  Domen mantiqi: invariantlar, chegaraviy holatlar, holat o'tishlari.
7.  Yo'q kod ro'yxati: validatsiya, avtorizatsiya, timeout, indeks, test,
    log, idempotentlik, null, bo'sh to'plam, qaytarish rejasi (3.5).
8.  Beshta ssenariy: happy, chegara, ikki marta, ikki parallel,
    o'rtada yiqilish (3.6).
9.  Tranzaksiya chegarasi: ichida tashqi chaqiruv bormi?
10. So'rovlar soni: siklda I/O bormi? Hajm ma'lumotga bog'liqmi?
11. Testlar: assertion qiymatni tekshiradimi? Chegaralar va xato yo'llari?
12. Observability: xato bo'lsa qanday bilamiz?
13. O'chirilgan satrlar: olib tashlangan tekshiruv yoki test bormi?
14. Xulosa: nimani tekshirdim, nimani tekshirmadim, qolgan xavf.
```

### 44.2 Yuqori xavfli PR uchun qo'shimcha o'tish

```text
Migratsiya:
[ ] Qulf turi aniqlandi (25.1 jadvali)
[ ] `lock_timeout` qo'yilgan
[ ] Jadval hajmi tekshirildi (pg_stat_user_tables)
[ ] Rolling deploy da eski kod ishlaydi (25.3)
[ ] Backfill alohida va bo'laklangan
[ ] Qaytarish rejasi yozilgan
[ ] Real hajmga yaqin nusxada sinalgan, vaqti ma'lum

Xavfsizlik:
[ ] Yangi endpoint uchun avtorizatsiya qoidasi va test
[ ] Resurs egaligi tekshiriladi (IDOR, 30.1)
[ ] Foydalanuvchi ID si so'rovdan olinmaydi
[ ] Tashqi ma'lumot SQL, URL, fayl yo'li, buyruqqa tushmaydi
[ ] Logda va xato javobida maxfiy ma'lumot yo'q
[ ] Yangi bog'liqlik CVE tekshirildi

Pul va hisob:
[ ] `BigDecimal`/`Money`, `double` yo'q
[ ] Yakkalash qoidasi aniq va kelishilgan
[ ] Valyuta har summa bilan
[ ] Manfiy va chegaraviy qiymatlar tekshirilgan
[ ] Idempotentlik kaliti va unique constraint
[ ] Audit yozuvi qoladi

Konkurentlik:
[ ] Tekshir-keyin-yoz himoyalangan (unique yoki atomik UPDATE)
[ ] `@Version` yoki qulf kerakli joyda
[ ] Qulf tartibi barqaror
[ ] `@Scheduled` uchun taqsimlangan qulf
[ ] Pool va navbat chegaralangan
```

### 44.3 Review izohlari uchun tayyor iboralar

```text
# N+1
blocker: `{metod}` sikl ichida chaqirilgan, ya'ni {N} element uchun {N}
so'rov. {jadval} da hozir {hajm} qator. `JOIN FETCH` yoki ommaviy
yuklash (38.2) kerak. So'rov sonini test bilan qulflashni ham taklif
qilaman.

# Tranzaksiya ichida tashqi chaqiruv
blocker: `{servis}.{metod}` tranzaksiya ichida chaqirilgan. DB ulanishi
va qator qulfi tashqi javobni kutib turadi. Pool {N} ta - {N} parallel
so'rov butun ilovani to'xtatadi. Tranzaksiyani qisqartirish yoki outbox
(10.8) kerak.

# Poyga holati
blocker: `{tekshiruv}` va `{yozuv}` orasida boshqa so'rov o'zgartirishi
mumkin. READ COMMITTED da ikki parallel so'rov ikkisi ham o'tadi.
Himoya: `{jadval}` da unique indeks (eng ishonchli) yoki atomik UPDATE.

# IDOR
blocker: `{endpoint}` da `{id}` so'rovdan keladi va egalik tekshirilmaydi.
Har qanday autentifikatsiya qilingan foydalanuvchi boshqa odamning
ma'lumotini ko'radi. So'rovga egalik sharti qo'shish kerak, va topilmasa
404 qaytarish (403 emas - enumeratsiya).

# SQL injection
blocker: `{parametr}` to'g'ridan-to'g'ri SQL ga qo'shilgan. {Yo'l:
endpoint -> metod -> so'rov}. Ruxsat etilgan qiymatlar enum i kerak
(29.1), chunki ustun nomi va ORDER BY parametr bo'la olmaydi.

# Migratsiya qulfi
blocker: `{operatsiya}` `{jadval}` da ACCESS EXCLUSIVE qulf oladi.
Jadvalda {hajm} qator - bu taxminan {vaqt} to'liq to'xtash. Xavfsiz
ketma-ketlik: {qadamlar} (25.1).

# Yo'q test
suggest: `{holat}` qamralmagan. Nega muhim: {oqibat}. Bu `@CsvSource` ga
bir qator qo'shish bilan hal bo'ladi: `{namuna}`.

# Yolg'on test
blocker: bu test `assertNotNull` bilan tugaydi, ya'ni `{metod}` ichidagi
har qanday o'zgarishda ham o'tadi. Kutilgan qiymat aniq yozilishi kerak.

# Kesh xavfsizligi
blocker: kesh kalitida foydalanuvchi identifikatori yo'q. Birinchi
so'rovning natijasi barcha foydalanuvchilarga qaytariladi.

# Timeout yo'q
blocker: `{mijoz}` da timeout sozlanmagan. Tashqi servis javob bermasa,
thread cheksiz kutadi va pool to'ladi. Ulanish uchun 500 ms, o'qish
uchun {byudjet} taklif qilaman (22.1).

# Breaking change
blocker: `{maydon}` o'zgarishi breaking change (37.1). Oxirgi 30 kunda
bu endpointni {mijozlar} ishlatgan. O'tish rejasi kerak: yangi maydon
qo'shish, ikkisini to'ldirish, eski maydonni {sana} da olib tashlash.

# Arxitektura
suggest: `{klass}` `{paket}` da `{bog'liqlik}` ga bog'langan. Oqibati:
{1,2,3}. Alternativa: {yechim}. Hajmi: {taxmin}. Bu PR da katta bo'lsa,
tiket ochib keyingi sprintda yopsak bo'ladi.

# Katta PR
Bu PR da {N} satr mantiq o'zgargan. Shu hajmda satr-satr review samarasiz
(2.2) - men xavf nuqtalari bo'yicha o'qidim va buni ochiq aytaman.
Keyingi marta bo'lib yuborsak: {taklif qilingan bo'laklar}. Hozir
to'xtatmayman, lekin {aniq joy} ni alohida ko'rib chiqishni so'raymiz.

# Maqtov
praise: bu yerda idempotentlik kaliti unique constraint bilan
himoyalangan - aynan shunday bo'lishi kerak. `FOR UPDATE SKIP LOCKED`
tanlovi ham to'g'ri: workerlar bir-birini kutmaydi.
```

### 44.4 Review xulosasi shablonlari

```text
# Approve
Approve (daraja 2).
Tekshirdim: {ro'yxat}.
Tekshirmadim: {ro'yxat}.
Qolgan xavf: {bor bo'lsa}. Yo'q bo'lsa: "sezilarli xavf ko'rmadim".

# O'zgarish so'rash
{N} blocker bor, qolgani ixtiyoriy.

Blocker lar:
1. {qisqa} - {satr havolasi}
2. {qisqa} - {satr havolasi}

Umumiy: yondashuv to'g'ri, {aniq joy} ni tuzatgandan keyin merge qilamiz.

# Dizayn savoli (detallarga tushmasdan)
Satrlarga izoh yozmadim, chunki bitta asosiy savol bor: {savol}.

Bu qaror o'zgarsa, {N} fayl ham o'zgaradi. Variantlar: {1}, {2}.
Men {tanlov} ni taklif qilaman, chunki {sabab}. Kelishib olgandan keyin
satr-satr o'qib chiqaman.

# Bo'lishni so'rash
Bu PR {N} satr. Review ni foydali qilish uchun bo'lishni so'raymiz:
1. {bo'lak 1} - mustaqil merge qilinadi
2. {bo'lak 2} - birinchisiga tayanadi
3. {bo'lak 3}

Birinchi bo'lakni bugun ko'rib chiqaman.
```

### 44.5 Reviewer yetukligi darajalari

| Daraja | Nimani ko'radi | Nimani hali ko'rmaydi |
| --- | --- | --- |
| 1. Uslub | Format, nomlash, uslub | Mantiq xatolari |
| 2. Mantiq | Null, chegara, shartlar, test holatlari | Tizim darajasidagi oqibatlar |
| 3. Tizim | Tranzaksiya, poyga, N+1, migratsiya qulfi, xavfsizlik | Uzoq muddatli oqibatlar |
| 4. Arxitektura | Chegara, bog'liqlik yo'nalishi, eroziya, API evolyutsiyasi | - |
| 5. Jarayon | Takrorlanadigan izohni qoidaga aylantirish, checklistni incidentlardan o'stirish, jamoani o'rgatish | - |

Yuqori darajaga o'tish mezoni - oldingi darajani avtomatlashtirish. Uslub izohlarini formatter ga, mantiq izohlarini statik tahlil va testga, tizim izohlarini ArchUnit va monitoringga ko'chirgan reviewer keyingi darajada ishlaydi.

### 44.6 O'zini tekshirish savollari

```text
Fikrlash va jarayon:
1.  Oxirgi 10 review da nechtasida uch o'qishni (niyat, mexanika, xavf)
    ongli ajratdim?
2.  Nechtasida "nimani tekshirmadim" ro'yxatini yozdim?
3.  Qaysi izohimni uchinchi marta yozdim va uni qoidaga aylantirdimmi?

Java va JVM:
4.  Diffda thread-safe emas holatni ko'ra olamanmi (singleton bean maydoni,
    statik kolleksiya, SimpleDateFormat)?
5.  Resurs oqishi va chegarasiz to'plamni hajm hisobi bilan ko'rsata olamanmi?
6.  `equals`/`hashCode`/`compareTo` nomuvofiqligini topa olamanmi?

Spring:
7.  Proxy ishlamaydigan to'rt holatni yoddan bilamanmi?
8.  Tranzaksiya ichidagi tashqi chaqiruvning to'rt oqibatini sanab bera olamanmi?
9.  `REQUIRED` ichida ushlangan istisno nega `UnexpectedRollbackException`
    berishini tushuntirib bera olamanmi?

PostgreSQL:
10. `ALTER TABLE` ning qaysi shakllari jadvalni qayta yozishini bilamanmi?
11. Diffdagi so'rovga qarab indeks ishlatiladimi yoki yo'qligini aytib bera olamanmi?
12. Write skew nima va uni qanday himoyalash kerakligini bilamanmi?

Xavfsizlik:
13. IDOR ni diffda ko'ra olamanmi va 404/403 tanlovini tushuntira olamanmi?
14. SQL da nima parametr bo'la olmasligini sanab bera olamanmi?
15. Tenant izolyatsiyasini majburlashning eng ishonchli yo'lini bilamanmi?

Testlar:
16. Test holatlari to'liqligini ekvivalentlik sinflari bilan baholay olamanmi?
17. Mutatsion fikrlashni qo'llab, testni aldab o'tish yo'lini topa olamanmi?
18. Yolg'on testni (assertion siz, mock ni tekshiradigan) tanib olamanmi?

Madaniyat:
19. Oxirgi izohlarimda oqibat va alternativa bormidi, yoki faqat baho?
20. Kelishmovchilikni ikki davradan oshirdimmi?
```

### 44.7 Loyihada review ni yo'lga qo'yishning birinchi 30 kuni

```text
1-hafta: asos
[ ] `REVIEW.md` yozish: maqsad, izoh darajalari, SLA, xavfli yo'llar
[ ] `CODEOWNERS` yaratish
[ ] Branch protection: conversation resolution, stale approvals
[ ] `spotless` yoki formatter ni CI ga qo'yish

2-hafta: instrumentlar
[ ] ErrorProne ni yoqish (3-5 muhim qoida ERROR darajasida)
[ ] ArchUnit testlari: qatlam, sikl, inyeksiya, tranzaksiya chegarasi
[ ] `gitleaks` ni pre-commit va CI ga qo'shish
[ ] CI ni bosqichlarga bo'lish: tez signal 2 daqiqada

3-hafta: o'lchov va kontekst
[ ] Review metrikalarini bir marta o'lchash (kutish vaqti, hajm, taqsimot)
[ ] `GLOSSARY.md` va `CLAUDE.md` yozish
[ ] Eng katta 5 jadval hajmini `REVIEW.md` ga yozish
[ ] Performance byudjetini uchta asosiy endpoint uchun belgilash

4-hafta: checklist va madaniyat
[ ] PR shabloni (majburiy qism 6 band)
[ ] Xavf darajasini avtomatik belgilash
[ ] Oxirgi 3 incidentni `REVIEW-SMELLS.md` ga kiritish
[ ] Jamoada bitta review ni birga tahlil qilish
```

### 44.8 Hujjatni qanday ishlatish

| Vaziyat | Qaysi bob |
| --- | --- |
| Review ni qanday boshlash kerakligini bilmayman | 3, 4, 44.1 |
| Sonar topadigan narsani oldin ko'rmoqchiman | 5 |
| Arxitektura buzilishini diffda ko'rmoqchiman | 6, 7 |
| Pattern kerak yoki kerak emasligini aniqlash | 10, 11 |
| Java tilidagi tuzoqlar | 14, 15, 16, 17 |
| Spring annotatsiyasi ishlamayapti | 18 |
| Tranzaksiya chegarasi to'g'rimi | 19 |
| Controller va DTO review | 20 |
| Konfiguratsiya o'zgarishi xavfli ko'rinadi | 21 |
| Tashqi integratsiya qo'shilyapti | 22 |
| N+1 va JPA muammolari | 23 |
| So'rov sekin ishlaydi | 24, 38 |
| Migratsiya PR i keldi | 25 |
| Ma'lumot to'g'riligi | 26 |
| Poyga holati bormi | 27 |
| Xavfsizlik review | 28-33 |
| Testlar yetarlimi | 34, 35, 36 |
| API o'zgarishi mijozni sindiradimi | 37 |
| Incidentda ko'r qolmaslik | 39 |
| Jarayon va madaniyat | 40, 41, 42 |
| AI yozgan kod | 43 |
| Tayyor iboralar va checklistlar | 44 |

### 44.9 Amalda qo'llash

- [ ] 15 daqiqalik universal o'tish ro'yxatini chop etib, ish joyingizda saqlang yoki IDE snippet qilib qo'ying.
- [ ] Yuqori xavfli PR checklistlarini `REVIEW.md` ga kiriting.
- [ ] Tayyor iboralarni jamoa wiki siga yoki GitHub saved replies ga qo'shing.
- [ ] Review xulosasi shablonlarini ishlatishni boshlang - ayniqsa "tekshirmadim" ro'yxatini.
- [ ] O'z yetuklik darajangizni belgilab, keyingi darajaga o'tish uchun bitta avtomatlashtirish ishini tanlang.
- [ ] 20 savolli o'zini tekshirish ro'yxatini bajarib, javob bera olmagan savollar bo'yicha tegishli bobni o'qing.
- [ ] 30 kunlik rejani jamoa bilan kelishib, birinchi haftadan boshlang.
- [ ] Har incidentdan keyin bu hujjatdagi tegishli checklistga bitta band qo'shing - eng qimmatli checklist loyihaning o'z tarixidan o'sadi.
