<!-- doc: clean-code | chapter: 38 | part: X. Hid katalogi va refaktoring harakatlari -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 38. Refaktoringni xavfsiz bajarish (Safe Refactoring Mechanics)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [38.1 Bir vaqtda bitta harakat](#381-bir-vaqtda-bitta-harakat)
- [38.2 Kompilyator va test bilan boshqarish](#382-kompilyator-va-test-bilan-boshqarish)
- [38.3 IDE refaktoringiga ishonish chegarasi](#383-ide-refaktoringiga-ishonish-chegarasi)
- [38.4 Refaktoringni mantiq o'zgarishidan ajratish](#384-refaktoringni-mantiq-ozgarishidan-ajratish)
- [38.5 Katta refaktoringni bo'lish: abstraksiya orqali shox](#385-katta-refaktoringni-bolish-abstraksiya-orqali-shox)
- [38.6 Refaktoringni to'xtatish nuqtasi](#386-refaktoringni-toxtatish-nuqtasi)
- [38.7 Refaktoring va ishlash: o'lchovsiz qadam qo'ymaslik](#387-refaktoring-va-ishlash-olchovsiz-qadam-qoymaslik)
- [38.8 Refaktoring commitlarini o'qiladigan ushlash](#388-refaktoring-commitlarini-oqiladigan-ushlash)
- [38.9 Amalda qo'llash](#389-amalda-qollash)

</details>


Refaktoring xatti-harakatni o'zgartirmasdan tuzilishni yaxshilash. "Xatti-harakatni o'zgartirmasdan" qismi uni xavfli qiladi: har bir qadam regressiya kiritishi mumkin. Bu bobda shu xavfni nolga yaqinlashtiradigan intizom. Legacy kodda chok topish va bosqichma-bosqich almashtirish strategiyasi [arxitektor hujjatidagi](../architect/README.md) legacy kod va bosqichma-bosqich refaktoring bo'limida.

## 38.1 Bir vaqtda bitta harakat

Eng muhim qoida: bir vaqtda bitta refaktoring harakati bajariladi va undan keyin kompilyatsiya va test ishga tushiriladi. Ikki harakatni birlashtirish vaqt tejaydi deb o'ylash odatiy xato - aslida xato topilganda qaysi harakat sabab bo'lganini aniqlash uchun ikkisini ham qaytarish kerak bo'ladi.

```bash
# Har bir harakatdan keyin: tez testlar (butun to'plam emas)
./mvnw -q -pl payment test -Dtest='*Test' -DfailIfNoTests=false

# Harakat ishladi: commit qilib, keyingisiga o'tish (kichik, qaytariladigan qadamlar)
git add -A && git commit -m "refactor: Payment dan TelephoneNumber ni ajratish"
```

## 38.2 Kompilyator va test bilan boshqarish

Refaktoring paytida kompilyator va testlar ikki xil rol o'ynaydi. **Kompilyator** tuzilish o'zgarishini boshqaradi: maydonni o'chirsangiz, u barcha ishlatilishlarni ko'rsatadi. **Testlar** xatti-harakatni himoya qiladi: mantiq o'zgarsa, ular yiqiladi.

Shu sababli ikki xil refaktoring bor. Kompilyator boshqaradigan harakatlar (rename, move, signature change) nisbatan xavfsiz - IDE ularni bajaradi. Mantiqqa tegadigan harakatlar (Substitute Algorithm, Replace Conditional with Polymorphism) esa **faqat** test bilan xavfsiz.

Agar testlar yo'q bo'lsa, birinchi qadam - xatti-harakatni qayd etuvchi test yozish ([arxitektor hujjatidagi](../architect/README.md) xavfsizlik to'ri va xatti-harakatni qayd etuvchi test bo'limi), refaktoring emas.

## 38.3 IDE refaktoringiga ishonish chegarasi

IDE refaktoringi qo'lda o'zgartirishdan ancha xavfsiz, lekin u hamma narsani ko'rmaydi. To'rt joyda IDE ni tekshirish kerak.

| Xavf | Nega IDE ko'rmaydi | Tekshiruv |
|---|---|---|
| Satr literalidagi nom | matn sifatida saqlangan | `grep` bilan qidirish (3.15) |
| Refleksiya va `Class.forName` | ish vaqtida hal qilinadi | grep + integratsion test |
| Spring XML va `@Value` kalitlari | kod emas | konfiguratsiyani grep |
| JPA `@Query` ichidagi maydon nomi | satr | repository testlari |
| Jackson `@JsonProperty` nomlari | API shartnomasi | contract test |
| SQL migratsiyalari | alohida fayl | migratsiya testi |

## 38.4 Refaktoringni mantiq o'zgarishidan ajratish

Bu qoida 13.6 (formatlash) ning umumiy shakli va u review sifatini belgilaydi: bitta commitda ham refaktoring, ham yangi xatti-harakat bo'lmasligi kerak.

Sababi aniq: refaktoring commitida diff katta bo'ladi, lekin reviewer "xatti-harakat o'zgarmaganini" bilib turadi va tezda o'tadi. Aralash commitda esa har bir qatorni tekshirish kerak va xato o'tib ketadi.

```bash
# Ikki commit, ikki maqsad
git commit -m "refactor: SettlementService dan import mantiqini ajratish"
git commit -m "feat: import faylida valyuta tekshiruvini qo'shish"
```

Amaliy tartib: oldin refaktoring (kodni o'zgarish uchun tayyorlash), keyin xatti-harakat o'zgarishi. Teskari tartib ham ishlaydi, lekin aralashtirish ishlamaydi.

## 38.5 Katta refaktoringni bo'lish: abstraksiya orqali shox

Katta refaktoringni bir PR da bajarish deyarli har doim muvaffaqiyatsiz bo'ladi: branch uzoq yashaydi, konfliktlar yig'iladi, review imkonsiz bo'ladi ([arxitektor hujjatidagi](../architect/README.md) katta qayta yozish bo'limi).

**Branch by abstraction** usuli katta refaktoringni kichik, merge qilinadigan qadamlarga bo'ladi:

1. Mavjud implementatsiya ustiga abstraksiya (interfeys) qo'yish va barcha chaqiruvchilarni unga o'tkazish. Merge qilinadi.
2. Yangi implementatsiyani abstraksiya ortida yozish, hali ishlatilmaydi. Merge qilinadi.
3. Konfiguratsiya yoki feature flag bilan trafikni bosqichma-bosqich yangisiga o'tkazish (41.5). Merge qilinadi.
4. Eski implementatsiyani o'chirish. Merge qilinadi.

Har bir qadam mustaqil ravishda production ga chiqadi va orqaga qaytarish oson.

## 38.6 Refaktoringni to'xtatish nuqtasi

Refaktoring cheksiz davom etishi mumkin va bu alohida xavf: "yana bir oz yaxshilayman" dan PR ikki haftaga cho'ziladi. To'xtatish uchun oldindan belgilangan shartlar kerak.

| To'xtatish sharti | Sabab |
|---|---|
| Asl vazifa bajarildi va kod toza | maqsadga erishildi |
| Refaktoring PR qamrovidan chiqdi | alohida PR ga ko'chiriladi (1.4) |
| Keyingi qadam test talab qiladi | oldin test, keyin davom |
| Qaror arxitektura darajasiga chiqdi | ADR kerak ([arxitektor hujjatidagi](../architect/README.md) ADR va qaror hujjatlashtirish bo'limi) |
| Vaqt budjeti tugadi | qolgani ro'yxatga yoziladi |
| Foyda noaniq bo'lib qoldi | to'xtash va o'lchash |

Oxirgi qator eng muhim: agar refaktoringdan keyin kod yaxshilangani haqida ishonch yo'q bo'lsa, o'zgarishni qaytarish to'g'ri qaror.

## 38.7 Refaktoring va ishlash: o'lchovsiz qadam qo'ymaslik

Refaktoring odatda ishlashga ta'sir qilmaydi, lekin ba'zi harakatlar qiladi: Replace Derived Variable with Query (35.20) hisobni har chaqiruvda bajaradi, Extract Function qo'shimcha chaqiruv qo'shadi (JIT odatda inline qiladi), Replace Loop with Pipeline qo'shimcha obyektlar yaratadi.

Qoida: refaktoringni o'qilishi uchun bajarish, keyin o'lchash. Agar o'lchov muammo ko'rsatsa, maqsadli optimizatsiya qilish va **nega** shunday qilinganini izohlash (8.4). O'lchovsiz "tezlik uchun" chirkin kod yozish esa vaqtidan oldin optimizatsiya ([patternlar hujjatidagi](../patterns/README.md) vaqtidan oldin optimizatsiya anti-patterni).

## 38.8 Refaktoring commitlarini o'qiladigan ushlash

Refaktoring tarixi keyinchalik o'qiladi: "bu sinf nega shunday bo'lgan?" savoliga javob beradi. Shu sababli commit xabari harakat nomini ishlatishi kerak (40.2).

```
refactor: Payment dan TelephoneNumber value object ini ajratish

Extract Class: officeAreaCode va officeNumber maydonlari birga sayohat
qilayotgan edi va formatlash mantiqi uch joyda takrorlangan.

Xatti-harakat o'zgarmadi; mavjud testlar o'zgartirilmagan.
```

Oxirgi qator reviewer uchun eng muhim signal: testlar o'zgarmagan bo'lsa, xatti-harakat ham o'zgarmagan.

## 38.9 Amalda qo'llash

- [ ] Refaktoring paytida har bir harakatdan keyin tez testlarni ishga tushirish odatini joriy qiling.
- [ ] Refaktoring va xatti-harakat o'zgarishini alohida commitlarga ajratish qoidasini jamoa kelishuviga kiriting.
- [ ] 38.3 jadvalidagi olti xavfni nomni o'zgartirishdan keyin har safar grep bilan tekshiring.
- [ ] Testsiz kodni refaktoring qilishdan oldin xatti-harakatni qayd etuvchi test yozishni majburiy qiling.
- [ ] Katta refaktoringlarni branch by abstraction bo'yicha to'rt qadamga bo'lib rejalashtiring.
- [ ] Har bir refaktoring PR i uchun oldindan vaqt budjeti va to'xtatish shartini belgilang.
- [ ] Refaktoring commit xabarlarida harakat nomini va "xatti-harakat o'zgarmadi" qatorini yozishni standart qiling.
- [ ] Refaktoringdan keyin ishlash o'lchovini (p99, so'rov soni) taqqoslab, sezilarli o'zgarishni tekshiring.

---

[&larr; 37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya](37-refaktoring-harakatlari-katalogi-iii-shart.md) · [Mundarija](README.md) · [39. Bir qadamli build va mahalliy qaytish halqasi &rarr;](39-bir-qadamli-build-va-mahalliy-qaytish.md)
