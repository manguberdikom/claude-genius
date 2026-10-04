<!-- doc: clean-code | chapter: 31 | part: IX. Test kodining tozaligi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 31. TDD intizomi va kod dizayniga ta'siri (TDD Discipline)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [31.1 Uchta qoida va qisqa sikl](#311-uchta-qoida-va-qisqa-sikl)
- [31.2 Red-green-refactor: har bir qadamning maqsadi](#312-red-green-refactor-har-bir-qadamning-maqsadi)
- [31.3 Test birinchi yozilsa dizayn qanday o'zgaradi](#313-test-birinchi-yozilsa-dizayn-qanday-ozgaradi)
- [31.4 Ishlasin, to'g'ri bo'lsin, tez bo'lsin tartibi](#314-ishlasin-togri-bolsin-tez-bolsin-tartibi)
- [31.5 Test yozish qiyin bo'lsa, dizayn signal beradi](#315-test-yozish-qiyin-bolsa-dizayn-signal-beradi)
- [31.6 TDD qachon mos emas](#316-tdd-qachon-mos-emas)
- [31.7 Transformatsiya prioritet gipotezasi](#317-transformatsiya-prioritet-gipotezasi)
- [31.8 Amalda qo'llash](#318-amalda-qollash)

</details>


Test yozish texnikasi [testlash qo'llanmasida](../testing/README.md). Bu bobda boshqa narsa: test yozish **tartibi** va uning kod dizayniga ta'siri. TDD test usuli emas, dizayn usuli - va shu sababli u toza kod hujjatiga tegishli.

## 31.1 Uchta qoida va qisqa sikl

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

## 31.2 Red-green-refactor: har bir qadamning maqsadi

Uch qadamning har birining aniq va boshqa maqsadi bor; ularni aralashtirish TDD ning foydasini yo'qotadi.

| Qadam | Maqsad | Nima qilinmaydi |
|---|---|---|
| **Red** | talabni ifodalash, testning o'zi ishlashini tekshirish | ishlab chiqarish kodi yozilmaydi |
| **Green** | testni o'tkazish, eng qisqa yo'l bilan | chiroylilik, umumiylashtirish |
| **Refactor** | tuzilishni yaxshilash | yangi xatti-harakat qo'shilmaydi |

"Red" qadamining ko'pincha e'tibordan chetda qoladigan maqsadi bor: test **yiqilishini ko'rish** kerak. Yiqilmagan test hech narsa tekshirmaydi va bu xato kech aniqlanadi.

## 31.3 Test birinchi yozilsa dizayn qanday o'zgaradi

Testni birinchi yozish dizaynga bosim beradi va bu bosim bu hujjatdagi ko'p qoidalarni **majburiy** qiladi:

- Bog'liqliklar konstruktorga chiqadi, chunki testda ularni almashtirish kerak (26.1).
- `Clock` inyeksiya qilinadi, chunki vaqtni qotirish kerak (22.3).
- Statik holat yo'qoladi, chunki testlar bir-biriga ta'sir qilmasligi kerak (16.9).
- Metodlar kichik bo'ladi, chunki katta metodni test qilish qiyin (4.1).
- Yon ta'sir ajratiladi, chunki sof funksiyani test qilish oson (16.6).
- Argumentlar kamayadi, chunki har bir argumentni testda yasash kerak (5.1).

Shu sababli "test yozish qiyin" degan hissiyot dizayn signali (31.5), vaqt yo'qligi signali emas.

## 31.4 Ishlasin, to'g'ri bo'lsin, tez bo'lsin tartibi

Tartib muhim va uni buzish eng ko'p vaqt yo'qotadi. **Ishlasin** - test o'tadi, yechim chirkin bo'lishi mumkin. **To'g'ri bo'lsin** - tuzilish tozalanadi, nomlar aniqlashadi, takrorlanish yo'qoladi. **Tez bo'lsin** - faqat o'lchov muammo ko'rsatsa (1.5).

Uchinchi qadamga o'tish sharti aniq: o'lchov bor va u talabni buzayotganini ko'rsatadi. O'lchovsiz optimizatsiya vaqtidan oldin optimizatsiya ([patternlar hujjatidagi](../patterns/README.md) vaqtidan oldin optimizatsiya anti-patterni).

## 31.5 Test yozish qiyin bo'lsa, dizayn signal beradi

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

## 31.6 TDD qachon mos emas

TDD universal emas va uni majburlash zarar keltiradigan holatlar bor. Tadqiqot (spike) kodida: hali nima qurilayotgani ma'lum bo'lmaganda test yozish ma'nosiz - spike tashlab yuboriladi va keyin TDD bilan qaytadan yoziladi. UI joylashuvi va vizual dizaynda: natijani ko'z bilan baholash arzonroq. Generatsiya qilingan kodda: test generator uchun yoziladi, natija uchun emas. Shuningdek, tashqi tizim xatti-harakatini o'rganishda: bunda "learning test" yoziladi, lekin u TDD sikli emas.

Qolgan hamma joyda, ayniqsa biznes qoidalari va hisob mantiqida, TDD eng arzon yo'l.

## 31.7 Transformatsiya prioritet gipotezasi

"Green" qadamida kodni qanday o'zgartirish kerakligi haqida foydali evristika bor: eng **oddiy** transformatsiyani tanlash. Tartib soddadan murakkabga: `{}` → `null`, `null` → konstanta, konstanta → o'zgaruvchi, ifoda → shart, qiymat → massiv, massiv → to'plam, shart → sikl, sikl → rekursiya, qiymat → polimorfizm.

Amaliy foydasi: har qadamda eng oddiy transformatsiyani tanlash kodni tabiiy ravishda sodda holatda ushlab turadi va vaqtidan oldin umumiylashtirishni ([patternlar hujjatidagi](../patterns/README.md) spekulyativ umumiylik anti-patterni) to'sadi.

## 31.8 Amalda qo'llash

- [ ] Keyingi yangi biznes qoidasini to'liq TDD sikli bilan yozib, siklni ikki daqiqada ushlashga harakat qiling.
- [ ] Har bir yangi test yozilganda uning **yiqilishini** ko'rishni odat qiling.
- [ ] Refaktoring qadamida yangi xatti-harakat qo'shmaslik qoidasini commit darajasida ajratib yuring (40.1).
- [ ] 31.5 jadvalidan foydalanib, test yozish qiyin bo'lgan uch sinfni topib, dizayn muammosini tuzating.
- [ ] `Instant.now()` va statik chaqiruvlarni inyeksiyaga o'tkazib, testlarni frameworksiz ishga tushiradigan qiling.
- [ ] Spike kodini alohida branch da ushlab, uni to'g'ridan-to'g'ri merge qilmaslikni kelishib oling.
- [ ] Jamoada bir hafta TDD bilan ishlab, keyin test qarzining o'zgarishini o'lchab ko'ring.
- [ ] "Green" qadamida eng oddiy transformatsiyani tanlash qoidasini mashq sessiyasida (46.7) sinab ko'ring.

---

[&larr; 30. Test kodi ham ishlab chiqarish kodi](30-test-kodi-ham-ishlab-chiqarish-kodi.md) · [Mundarija](README.md) · [32. Kod hidlari katalogi I: nom, funksiya, ma'lumot &rarr;](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md)
