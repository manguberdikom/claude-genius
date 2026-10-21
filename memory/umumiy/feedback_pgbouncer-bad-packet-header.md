---
type: feedback
---
# `FATAL: bad packet header: '<hex>'`: PgBouncer paket chegarasi, kod xatosi emas

- Bu xabarni PostgreSQL emas, **PgBouncer** beradi. Kelgan protokol xabari
  uzunligi `max_packet_size` dan katta bo'lsa PgBouncer klient ulanishini
  yopadi. Spring da u `DataAccessResourceFailureException` bo'lib chiqadi,
  bitta katta INSERT yoki UPDATE bilan bog'liq bo'ladi.
- Hex ni ochish: birinchi bayt xabar turi (`42` = `B`, Bind, ya'ni
  parametrlar), keyingi 4 bayt big-endian uzunlik. Masalan
  `4200011755...` bu 0x11755 = 71 509 baytlik Bind. Uzunlik shu so'rov
  parametrlarining umumiy hajmi.
- PgBouncer sukuti 2147483647, demak serverda chegara qo'lda kichik
  qo'yilgan. Uni repo ko'rsatmaydi: PgBouncer admin konsolidagi
  `SHOW CONFIG;` buyrug'i ko'rsatadi.
- Xato faqat katta yozuvda chiqadi (masalan ro'yxatni bitta JSON ustunga
  yig'ish). Avval payload nega shuncha katta ekanini so'rang:
  [[feedback_outbox-payload-nusxa]]. Keyin bo'laklang. Chegarani oshirishni
  DevOps ga aytish alohida qadam.
