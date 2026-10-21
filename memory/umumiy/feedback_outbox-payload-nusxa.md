---
type: feedback
---
# Outbox payload ga bazada turgan ma'lumot nusxa qilinmaydi

- Foydalanuvchi so'radi: "shuncha ma'lumotni saqlash o'zi mantiqan to'g'rimi?".
  Payload ni kattalashgani uchun faqat bo'laklash yetarli emas: avval payload
  dagi maydonlar kerakmi, shuni tekshiring.
- Tekshiruv: (1) maydon shu tranzaksiyada boshqa jadvalga allaqachon
  yozilganmi; (2) topic ni qaysi consumer o'qiydi va u maydonni ishlatadimi
  (consumer reposining hamma branchida qidiring); (3) nusxa shaxsiy
  ma'lumot bo'lsa, uni tozalash uchun alohida kod (payload ni bo'shatish,
  retention job) yozilganmi. Uchalasi ham "ha" bo'lsa, nusxa ortiqcha.
- Odatiy yechim: payload da faqat id va manzil (username) qoladi, qolgani
  manba jadvalda. Kontrakt o'zgarsa, eski shakldagi kutayotgan qatorlar
  relay da o'qilishi uchun record ga `@JsonIgnoreProperties(ignoreUnknown =
  true)` qo'ying va testni FAIL_ON_UNKNOWN_PROPERTIES yoqilgan mapper bilan
  yozing: Spring Boot mapper i bu xatoni yashiradi.
- Bog'liq: [[feedback_pgbouncer-bad-packet-header]].
